"""Offline host-key trust tests for scripts/deploy_theme_sftp.py (#1034).

No network, no credentials: paramiko's Transport is mocked, and paramiko
itself is stubbed when it is not installed (CI does not install it). The
Keychain is faked at subprocess.run, so no test reads a real Keychain item.
"""

import importlib
import os
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))


def _import_module():
    try:
        import paramiko  # noqa: F401

        return importlib.import_module("deploy_theme_sftp")
    except ImportError:
        stub = types.ModuleType("paramiko")
        stub.Transport = mock.MagicMock(name="Transport")
        stub.SFTPClient = mock.MagicMock(name="SFTPClient")
        stub.HostKeys = mock.MagicMock(name="HostKeys")
        with mock.patch.dict(sys.modules, {"paramiko": stub}):
            sys.modules.pop("deploy_theme_sftp", None)
            return importlib.import_module("deploy_theme_sftp")


dts = _import_module()


class FakeKey:
    def __init__(self, name: str, blob: bytes):
        self._name = name
        self._blob = blob

    def get_name(self):
        return self._name

    def asbytes(self):
        return self._blob


class FakeHostKeys:
    """Mirrors paramiko.HostKeys.lookup/check semantics."""

    def __init__(self, entries: dict[str, list[FakeKey]]):
        self._entries = entries

    def lookup(self, name):
        keys = self._entries.get(name)
        return {k.get_name(): k for k in keys} if keys else None

    def check(self, name, key):
        entry = self.lookup(name)
        if entry is None or key.get_name() not in entry:
            return False
        return entry[key.get_name()].asbytes() == key.asbytes()


TRUSTED = FakeKey("ssh-ed25519", b"trusted-blob")
EVIL = FakeKey("ssh-ed25519", b"attacker-blob")


class ConnectTrustTests(unittest.TestCase):
    def _connect(self, hosts, trusted, server_keys, port=22):
        """Run _connect with per-host server keys; return (result, transports)."""
        transports = {}

        def make_transport(addr):
            host, _port = addr
            t = mock.MagicMock(name=f"Transport({host})")
            key = server_keys.get(host)
            if isinstance(key, Exception):
                t.start_client.side_effect = key
            else:
                t.get_remote_server_key.return_value = key
            transports[host] = t
            return t

        fake_paramiko = mock.MagicMock()
        fake_paramiko.Transport.side_effect = make_transport
        fake_paramiko.SFTPClient.from_transport.side_effect = lambda t: ("sftp", t)
        with (
            mock.patch.object(dts, "paramiko", fake_paramiko),
            mock.patch.object(dts, "HOSTS", hosts),
            mock.patch.object(dts, "PORT", port),
            mock.patch.object(dts, "_trusted_host_keys", return_value=trusted),
            mock.patch.object(dts, "_sftp_user", return_value="synthetic-user"),
            mock.patch.object(dts, "_password", return_value="synthetic-pw"),
            mock.patch("builtins.print"),
        ):
            try:
                result = dts._connect()
            except SystemExit as exc:
                result = exc
        return result, transports

    def test_trusted_key_authenticates(self):
        trusted = FakeHostKeys({"a.example": [TRUSTED]})
        result, ts = self._connect(["a.example"], trusted, {"a.example": TRUSTED})
        self.assertEqual(result, ("sftp", ts["a.example"]))
        ts["a.example"].auth_password.assert_called_once_with(
            "synthetic-user", "synthetic-pw"
        )
        ts["a.example"].connect.assert_not_called()  # hostkey=None path is gone
        ts["a.example"].close.assert_not_called()

    def test_unknown_host_never_authenticates(self):
        trusted = FakeHostKeys({})
        result, ts = self._connect(["a.example"], trusted, {"a.example": TRUSTED})
        self.assertIsInstance(result, SystemExit)
        self.assertIn("not in the trusted known_hosts", str(result.code))
        ts["a.example"].auth_password.assert_not_called()
        ts["a.example"].close.assert_called_once()

    def test_mismatched_key_never_authenticates(self):
        trusted = FakeHostKeys({"a.example": [TRUSTED]})
        result, ts = self._connect(["a.example"], trusted, {"a.example": EVIL})
        self.assertIsInstance(result, SystemExit)
        self.assertIn("does not match", str(result.code))
        ts["a.example"].auth_password.assert_not_called()
        ts["a.example"].close.assert_called_once()

    def test_key_type_not_enrolled_is_rejected(self):
        trusted = FakeHostKeys({"a.example": [TRUSTED]})
        rsa = FakeKey("ssh-rsa", b"trusted-blob")
        result, ts = self._connect(["a.example"], trusted, {"a.example": rsa})
        self.assertIsInstance(result, SystemExit)
        ts["a.example"].auth_password.assert_not_called()

    def test_fallback_host_must_be_trusted_in_its_own_right(self):
        # Primary fails to connect; fallback is not enrolled -> no auth anywhere.
        trusted = FakeHostKeys({"a.example": [TRUSTED]})
        result, ts = self._connect(
            ["a.example", "b.example"],
            trusted,
            {"a.example": OSError("refused"), "b.example": TRUSTED},
        )
        self.assertIsInstance(result, SystemExit)
        for t in ts.values():
            t.auth_password.assert_not_called()
            t.close.assert_called_once()

    def test_fallback_after_mismatch_uses_only_trusted_fallback(self):
        trusted = FakeHostKeys({"a.example": [TRUSTED], "b.example": [TRUSTED]})
        result, ts = self._connect(
            ["a.example", "b.example"],
            trusted,
            {"a.example": EVIL, "b.example": TRUSTED},
        )
        self.assertEqual(result, ("sftp", ts["b.example"]))
        ts["a.example"].auth_password.assert_not_called()
        ts["a.example"].close.assert_called_once()
        ts["b.example"].auth_password.assert_called_once()

    def test_trust_entry_is_port_qualified(self):
        trusted = FakeHostKeys({"a.example": [TRUSTED]})
        result, ts = self._connect(
            ["a.example"], trusted, {"a.example": TRUSTED}, port=2222
        )
        self.assertIsInstance(result, SystemExit)
        ts["a.example"].auth_password.assert_not_called()

        trusted = FakeHostKeys({"[a.example]:2222": [TRUSTED]})
        result, ts = self._connect(
            ["a.example"], trusted, {"a.example": TRUSTED}, port=2222
        )
        self.assertEqual(result, ("sftp", ts["a.example"]))

    def test_failed_auth_closes_transport(self):
        trusted = FakeHostKeys({"a.example": [TRUSTED]})

        def make_transport(addr):
            t = mock.MagicMock()
            t.get_remote_server_key.return_value = TRUSTED
            t.auth_password.side_effect = Exception("auth failed")
            holder.append(t)
            return t

        holder = []
        fake_paramiko = mock.MagicMock()
        fake_paramiko.Transport.side_effect = make_transport
        with (
            mock.patch.object(dts, "paramiko", fake_paramiko),
            mock.patch.object(dts, "HOSTS", ["a.example"]),
            mock.patch.object(dts, "_trusted_host_keys", return_value=trusted),
            mock.patch.object(dts, "_sftp_user", return_value="synthetic-user"),
            mock.patch.object(dts, "_password", return_value="synthetic-pw"),
            mock.patch("builtins.print"),
        ):
            with self.assertRaises(SystemExit):
                dts._connect()
        holder[0].close.assert_called_once()


class TrustedHostKeysFileTests(unittest.TestCase):
    def test_missing_known_hosts_exits_before_any_credential_lookup(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = os.path.join(tmp, "nope")
            with (
                mock.patch.object(dts, "_sftp_user") as user,
                mock.patch.object(dts, "_password") as pw,
                mock.patch.object(dts, "KNOWN_HOSTS", missing),
            ):
                with self.assertRaises(SystemExit) as ctx:
                    dts._connect()
            user.assert_not_called()
            pw.assert_not_called()
        self.assertIn("No trusted SFTP host keys", str(ctx.exception.code))


SECURITY = ["security", "find-generic-password", "-s", "pagely-sftp-kriskrug"]
KEYCHAIN_ATTRIBUTES = (
    'keychain: "/fake/login.keychain-db"\n'
    'class: "genp"\n'
    "attributes:\n"
    '    0x00000007 <blob>="pagely-sftp-kriskrug"\n'
    '    "acct"<blob>="synthetic-sftp-user"\n'
    '    "svce"<blob>="pagely-sftp-kriskrug"\n'
)


def sftp_env(**values):
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("WP_SFTP_USER", "WP_SFTP_PASSWORD")
    }
    env.update(values)
    return mock.patch.dict(os.environ, env, clear=True)


def keychain_returns(*results):
    """Fake subprocess.run: each result is (returncode, stdout) or an exception."""
    outcomes = [
        r if isinstance(r, Exception) else subprocess.CompletedProcess([], *r, "")
        for r in results
    ]
    return mock.patch.object(dts.subprocess, "run", side_effect=outcomes)


class SftpUserResolutionTests(unittest.TestCase):
    """User: WP_SFTP_USER, else the Keychain item's account. There is no default."""

    def test_env_user_wins_without_touching_the_keychain(self):
        with sftp_env(WP_SFTP_USER="env-user"), keychain_returns() as run:
            self.assertEqual(dts._sftp_user(), "env-user")
        run.assert_not_called()

    def test_unset_or_blank_env_user_reads_the_keychain_account(self):
        for env in ({}, {"WP_SFTP_USER": ""}, {"WP_SFTP_USER": "  "}):
            with (
                self.subTest(env=env),
                sftp_env(**env),
                keychain_returns((0, KEYCHAIN_ATTRIBUTES)) as run,
            ):
                self.assertEqual(dts._sftp_user(), "synthetic-sftp-user")
                argv = run.call_args.args[0]
                self.assertEqual(argv, SECURITY)
                self.assertNotIn("-w", argv)
                self.assertNotIn("-g", argv)

    def test_no_env_user_and_no_keychain_account_exits(self):
        cases = {
            "item missing": (44, ""),
            "account empty": (
                0,
                KEYCHAIN_ATTRIBUTES.replace('="synthetic-sftp-user"', "=<NULL>"),
            ),
            "not macOS": FileNotFoundError("security"),
        }
        for name, result in cases.items():
            with self.subTest(name), sftp_env(), keychain_returns(result):
                with self.assertRaises(SystemExit) as ctx:
                    dts._sftp_user()
                self.assertIn("WP_SFTP_USER", str(ctx.exception.code))


class SftpPasswordResolutionTests(unittest.TestCase):
    def test_env_password_wins_without_touching_the_keychain(self):
        with sftp_env(WP_SFTP_PASSWORD="env-pw"), keychain_returns() as run:
            self.assertEqual(dts._password("synthetic-sftp-user"), "env-pw")
        run.assert_not_called()

    def test_keychain_password_is_read_for_the_resolved_account(self):
        with sftp_env(), keychain_returns((0, "synthetic-pw\n")) as run:
            self.assertEqual(dts._password("synthetic-sftp-user"), "synthetic-pw")
        self.assertEqual(
            run.call_args.args[0], [*SECURITY, "-a", "synthetic-sftp-user", "-w"]
        )

    def test_missing_password_exits_without_echoing_the_account(self):
        with (
            sftp_env(),
            keychain_returns((44, "")),
            self.assertRaises(SystemExit) as ctx,
        ):
            dts._password("synthetic-sftp-user")
        message = str(ctx.exception.code)
        self.assertIn("WP_SFTP_PASSWORD", message)
        self.assertNotIn("synthetic-sftp-user", message)


class ConnectResolutionOrderTests(unittest.TestCase):
    def test_keychain_account_feeds_the_password_lookup_and_login(self):
        transport = mock.MagicMock(name="Transport")
        transport.get_remote_server_key.return_value = TRUSTED
        fake_paramiko = mock.MagicMock()
        fake_paramiko.Transport.return_value = transport
        with (
            sftp_env(),
            keychain_returns((0, KEYCHAIN_ATTRIBUTES), (0, "synthetic-pw\n")) as run,
            mock.patch.object(dts, "paramiko", fake_paramiko),
            mock.patch.object(dts, "HOSTS", ["a.example"]),
            mock.patch.object(dts, "PORT", 22),
            mock.patch.object(
                dts,
                "_trusted_host_keys",
                return_value=FakeHostKeys({"a.example": [TRUSTED]}),
            ),
            mock.patch("builtins.print"),
        ):
            dts._connect()
        self.assertEqual(
            [c.args[0] for c in run.call_args_list],
            [SECURITY, [*SECURITY, "-a", "synthetic-sftp-user", "-w"]],
        )
        transport.auth_password.assert_called_once_with(
            "synthetic-sftp-user", "synthetic-pw"
        )


if __name__ == "__main__":
    unittest.main()
