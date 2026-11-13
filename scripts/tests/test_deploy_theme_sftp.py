"""Offline host-key trust tests for scripts/deploy_theme_sftp.py (#1034).

No network, no credentials: paramiko's Transport is mocked, and paramiko
itself is stubbed when it is not installed (CI does not install it). The
Keychain is faked at subprocess.run by FakeSecurity, which answers each argv
the way security(1) does, so no test reads a real Keychain item.
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
            mock.patch.object(
                dts, "_credentials", return_value=("synthetic-user", "synthetic-pw")
            ),
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
            mock.patch.object(
                dts, "_credentials", return_value=("synthetic-user", "synthetic-pw")
            ),
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
                mock.patch.object(dts, "_credentials") as credentials,
                mock.patch.object(dts.subprocess, "run") as run,
                mock.patch.object(dts, "KNOWN_HOSTS", missing),
            ):
                with self.assertRaises(SystemExit) as ctx:
                    dts._connect()
            credentials.assert_not_called()
            run.assert_not_called()
        self.assertIn("No trusted SFTP host keys", str(ctx.exception.code))


SERVICE = "pagely-sftp-kriskrug"
FIND = ["security", "find-generic-password", "-s", SERVICE]
DUMP = ["security", "dump-keychain"]
NOT_FOUND = (
    "security: SecKeychainSearchCopyNext: The specified item could not be "
    "found in the keychain.\n"
)


def item_attributes(service: str, account: str | None) -> str:
    acct = "<NULL>" if account is None else f'"{account}"'
    return (
        'keychain: "/fake/login.keychain-db"\n'
        "version: 512\n"
        'class: "genp"\n'
        "attributes:\n"
        f'    0x00000007 <blob>="{service}"\n'
        f'    "acct"<blob>={acct}\n'
        f'    "svce"<blob>="{service}"\n'
    )


class FakeSecurity:
    """subprocess.run stand-in that answers each argv the way security(1) does.

    items are (account, password) for the SFTP service, in Keychain order.
    find-generic-password returns the first match when -a is absent and the
    matching item when it is present; dump-keychain lists every item's
    attributes, plus one unrelated service, and never a password.
    """

    def __init__(self, *items, installed: bool = True):
        self.items = items
        self.installed = installed
        self.calls: list[tuple[list[str], dict]] = []

    def __call__(self, argv, **kwargs):
        self.calls.append((list(argv), kwargs))
        if not self.installed:
            raise FileNotFoundError("security")
        tool, command, *rest = argv
        if tool != "security":
            raise AssertionError(f"unexpected program: {tool}")
        if command == "dump-keychain":
            if rest:
                raise AssertionError(f"dump-keychain takes no flags here: {rest}")
            listing = item_attributes("some-other-service", "unrelated-account")
            listing += "".join(item_attributes(SERVICE, acct) for acct, _ in self.items)
            return subprocess.CompletedProcess(argv, 0, listing, "")
        if command == "find-generic-password":
            return self._find(argv, rest)
        raise AssertionError(f"unexpected security command: {command}")

    def _find(self, argv, rest):
        flags = dict(zip(rest[::2], rest[1::2]))
        want_password = rest[-1:] == ["-w"]
        if flags.get("-s") != SERVICE or "-g" in rest:
            raise AssertionError(f"unexpected find-generic-password args: {rest}")
        matches = [
            item for item in self.items if "-a" not in flags or item[0] == flags["-a"]
        ]
        if not matches:
            return subprocess.CompletedProcess(argv, 44, "", NOT_FOUND)
        account, password = matches[0]
        out = f"{password}\n" if want_password else item_attributes(SERVICE, account)
        return subprocess.CompletedProcess(argv, 0, out, "")

    @property
    def argvs(self) -> list[list[str]]:
        return [argv for argv, _ in self.calls]


OLD_ITEM = ("stale-sftp-user", "stale-pw")
NEW_ITEM = ("synthetic-sftp-user", "synthetic-pw")


def sftp_env(**values):
    env = {
        k: v
        for k, v in os.environ.items()
        if k not in ("WP_SFTP_USER", "WP_SFTP_PASSWORD")
    }
    env.update(values)
    return mock.patch.dict(os.environ, env, clear=True)


class _FakeKeychainCase(unittest.TestCase):
    def keychain(self, *items, installed: bool = True) -> FakeSecurity:
        fake = FakeSecurity(*items, installed=installed)
        patcher = mock.patch.object(dts.subprocess, "run", fake)
        patcher.start()
        self.addCleanup(patcher.stop)
        return fake

    def assert_safe_calls(self, fake: FakeSecurity):
        """Output is captured as text, and only an -a lookup may ask for a password."""
        for argv, kwargs in fake.calls:
            self.assertEqual(kwargs, {"capture_output": True, "text": True}, argv)
            self.assertNotIn("-d", argv)
            self.assertNotIn("-g", argv)
            if "-w" in argv:
                self.assertIn("-a", argv)

    def exit_message(self) -> str:
        with self.assertRaises(SystemExit) as ctx:
            dts._credentials()
        return str(ctx.exception.code)


class SftpCredentialSourceTests(_FakeKeychainCase):
    """User and password come from one source: the env pair, else one Keychain item."""

    def test_env_pair_wins_without_touching_the_keychain(self):
        fake = self.keychain(NEW_ITEM)
        with sftp_env(WP_SFTP_USER="env-user", WP_SFTP_PASSWORD="env-pw"):
            self.assertEqual(dts._credentials(), ("env-user", "env-pw"))
        self.assertEqual(fake.calls, [])

    def test_env_password_without_env_user_never_borrows_the_keychain_account(self):
        fake = self.keychain(NEW_ITEM)
        for env in (
            {"WP_SFTP_PASSWORD": "env-pw"},
            {"WP_SFTP_PASSWORD": "env-pw", "WP_SFTP_USER": "  "},
        ):
            with self.subTest(env=sorted(env)), sftp_env(**env):
                message = self.exit_message()
                self.assertIn("WP_SFTP_USER", message)
                self.assertNotIn("env-pw", message)
                self.assertNotIn(NEW_ITEM[0], message)
        self.assertEqual(fake.calls, [])

    def test_no_env_reads_account_and_password_from_the_single_item(self):
        for env in ({}, {"WP_SFTP_USER": "", "WP_SFTP_PASSWORD": "  "}):
            with self.subTest(env=env), sftp_env(**env):
                fake = self.keychain(NEW_ITEM)
                self.assertEqual(dts._credentials(), NEW_ITEM)
                self.assertEqual(
                    fake.argvs, [DUMP, FIND, [*FIND, "-a", NEW_ITEM[0], "-w"]]
                )
                self.assert_safe_calls(fake)

    def test_two_items_for_the_service_are_refused_without_reading_either(self):
        fake = self.keychain(OLD_ITEM, NEW_ITEM)
        with sftp_env():
            message = self.exit_message()
        self.assertIn("More than one Keychain item", message)
        self.assertIn("WP_SFTP_USER", message)
        for secret in (*OLD_ITEM, *NEW_ITEM):
            self.assertNotIn(secret, message)
        # Counted from the attribute listing; no account or password lookup ran.
        self.assertEqual(fake.argvs, [DUMP])
        self.assert_safe_calls(fake)

    def test_first_match_is_the_stale_item_which_is_why_two_items_are_refused(self):
        """The fake models security(1): without -a the first item answers."""
        fake = FakeSecurity(OLD_ITEM, NEW_ITEM)
        first = fake(FIND, capture_output=True, text=True)
        self.assertIn(f'"acct"<blob>="{OLD_ITEM[0]}"', first.stdout)
        picked = fake([*FIND, "-a", NEW_ITEM[0], "-w"], capture_output=True, text=True)
        self.assertEqual(picked.stdout, f"{NEW_ITEM[1]}\n")

    def test_env_user_picks_its_own_item_when_two_exist(self):
        fake = self.keychain(OLD_ITEM, NEW_ITEM)
        with sftp_env(WP_SFTP_USER=NEW_ITEM[0]):
            self.assertEqual(dts._credentials(), NEW_ITEM)
        self.assertEqual(fake.argvs, [[*FIND, "-a", NEW_ITEM[0], "-w"]])
        self.assert_safe_calls(fake)

    def test_env_user_with_no_matching_item_exits_without_echoing_the_account(self):
        fake = self.keychain(OLD_ITEM)
        with sftp_env(WP_SFTP_USER="someone-else"):
            message = self.exit_message()
        self.assertIn("WP_SFTP_PASSWORD", message)
        for secret in ("someone-else", *OLD_ITEM):
            self.assertNotIn(secret, message)
        self.assertEqual(fake.argvs, [[*FIND, "-a", "someone-else", "-w"]])
        self.assert_safe_calls(fake)

    def test_no_env_and_no_usable_keychain_item_exits(self):
        cases = {
            "item missing": {"items": ()},
            "account empty": {"items": ((None, "orphan-pw"),)},
            "not macOS": {"items": (NEW_ITEM,), "installed": False},
        }
        for name, case in cases.items():
            with self.subTest(name), sftp_env():
                fake = self.keychain(
                    *case["items"], installed=case.get("installed", True)
                )
                message = self.exit_message()
                self.assertIn("WP_SFTP_USER", message)
                self.assertIn("WP_SFTP_PASSWORD", message)
                self.assertNotIn("orphan-pw", message)
                self.assertFalse(any("-w" in argv for argv in fake.argvs))
                self.assert_safe_calls(fake)

    def test_dump_failure_is_treated_as_no_item(self):
        failed = subprocess.CompletedProcess(DUMP, 1, "", "security: cannot dump\n")
        with (
            sftp_env(),
            mock.patch.object(dts.subprocess, "run", return_value=failed) as run,
        ):
            message = self.exit_message()
        self.assertIn("No SFTP credentials", message)
        run.assert_called_once_with(DUMP, capture_output=True, text=True)


class ConnectResolutionOrderTests(_FakeKeychainCase):
    def connect(self, transport):
        fake_paramiko = mock.MagicMock()
        fake_paramiko.Transport.return_value = transport
        with (
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
            return dts._connect()

    def trusted_transport(self):
        transport = mock.MagicMock(name="Transport")
        transport.get_remote_server_key.return_value = TRUSTED
        return transport

    def test_keychain_account_feeds_the_password_lookup_and_login(self):
        transport = self.trusted_transport()
        fake = self.keychain(NEW_ITEM)
        with sftp_env():
            self.connect(transport)
        self.assertEqual(fake.argvs, [DUMP, FIND, [*FIND, "-a", NEW_ITEM[0], "-w"]])
        self.assert_safe_calls(fake)
        transport.auth_password.assert_called_once_with(*NEW_ITEM)

    def test_env_password_is_never_sent_with_a_keychain_account(self):
        transport = self.trusted_transport()
        fake = self.keychain(OLD_ITEM)
        with sftp_env(WP_SFTP_PASSWORD="env-pw"), self.assertRaises(SystemExit):
            self.connect(transport)
        transport.auth_password.assert_not_called()
        self.assertEqual(fake.calls, [])

    def test_two_keychain_items_never_reach_a_login(self):
        transport = self.trusted_transport()
        self.keychain(OLD_ITEM, NEW_ITEM)
        with sftp_env(), self.assertRaises(SystemExit):
            self.connect(transport)
        transport.auth_password.assert_not_called()


if __name__ == "__main__":
    unittest.main()
