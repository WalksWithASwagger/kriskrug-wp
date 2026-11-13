#!/usr/bin/env python3
"""Hands-off kk-aurora theme deploy to Pagely over SFTP (PressFTP gateway).

Credential sources (never argv/chat logs):
    User:     env WP_SFTP_USER, else the account of the Keychain item below.
    Password: env WP_SFTP_PASSWORD (Cloud / non-macOS agents), else that item:
       security add-generic-password -a <sftp-user> -s pagely-sftp-kriskrug -w "$(pbpaste)" -U
    <sftp-user> is the Pagely SFTP username, not the WordPress login. To see
    which account the item holds (attributes only, no password):
       security find-generic-password -s pagely-sftp-kriskrug

Subcommands:
    probe   Connect, print the working dir, and locate wp-content/themes.
    deploy  Upload theme/kk-aurora to a staging dir, then atomically swap it
            in (rename old -> .bak-<ver>, rename new -> kk-aurora). Instant
            rollback = swap the names back.

Deploy never deletes the previous theme; it renames it aside.

Host-key trust (#1034): every host is verified against an explicitly trusted
OpenSSH known_hosts file BEFORE the password is sent. Unknown or changed keys
abort that host; a fallback host is only used if it is trusted in its own
right. The file is WP_SFTP_KNOWN_HOSTS (default ~/.ssh/known_hosts). Enrol or
rotate a key out of band only, after confirming the fingerprint with Pagely:

    ssh-keyscan sftp.pressftp.com sftp.pagely.com > /tmp/scan   # all key types
    ssh-keygen -lf /tmp/scan   # compare fingerprints with Pagely before trusting
    cat /tmp/scan >> ~/.ssh/known_hosts

Never commit the known_hosts file, passwords or private keys to this repo.
"""

import argparse
import os
import posixpath
import re
import subprocess
import sys
import time

import paramiko

HOSTS = os.environ.get("WP_SFTP_HOST", "sftp.pressftp.com,sftp.pagely.com").split(",")
PORT = int(os.environ.get("WP_SFTP_PORT", "22"))
KEYCHAIN_SERVICE = "pagely-sftp-kriskrug"
KNOWN_HOSTS = os.environ.get(
    "WP_SFTP_KNOWN_HOSTS", os.path.expanduser("~/.ssh/known_hosts")
)
CONNECT_TIMEOUT = 30
LOCAL_THEME = os.path.join(os.path.dirname(__file__), "..", "theme", "kk-aurora")


def _keychain(*args: str) -> str:
    """stdout of `security find-generic-password` for the SFTP item, "" if absent."""
    try:
        out = subprocess.run(
            ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, *args],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:  # no `security` tool off macOS
        return ""
    return out.stdout if out.returncode == 0 else ""


def _sftp_user() -> str:
    env_user = os.environ.get("WP_SFTP_USER", "").strip()
    if env_user:
        return env_user
    # Attributes only: -w or -g would print the password as well.
    match = re.search(r'^\s*"acct"<blob>="(.+)"\s*$', _keychain(), re.M)
    if not match:
        sys.exit(
            "No SFTP user. Set WP_SFTP_USER, or store the Keychain item for "
            f"service '{KEYCHAIN_SERVICE}' under the SFTP user's account."
        )
    return match.group(1)


def _password(user: str) -> str:
    # Cloud / CI: prefer explicit env (never log it). Laptop: macOS Keychain.
    env_pw = os.environ.get("WP_SFTP_PASSWORD", "").strip()
    if env_pw:
        return env_pw
    pw = _keychain("-a", user, "-w").rstrip("\n")
    if not pw.strip():
        sys.exit(
            "No SFTP password. Set WP_SFTP_PASSWORD, or store it in Keychain "
            f"service '{KEYCHAIN_SERVICE}' under the SFTP user's account."
        )
    return pw


class HostKeyError(Exception):
    """The server's host key is not explicitly trusted; do not authenticate."""


def _trusted_host_keys(path: str = "") -> paramiko.HostKeys:
    path = path or KNOWN_HOSTS
    if not os.path.isfile(path):
        sys.exit(
            f"No trusted SFTP host keys at {path}. Enrol the Pagely host key out "
            "of band (see this script's docstring) or set WP_SFTP_KNOWN_HOSTS."
        )
    return paramiko.HostKeys(path)


def _known_hosts_name(host: str, port: int) -> str:
    return host if port == 22 else f"[{host}]:{port}"


def _verify_host_key(
    transport: paramiko.Transport, trusted: paramiko.HostKeys, host: str, port: int
) -> None:
    name = _known_hosts_name(host, port)
    if trusted.lookup(name) is None:
        raise HostKeyError(f"{name}: host key is not in the trusted known_hosts")
    remote = transport.get_remote_server_key()
    if not trusted.check(name, remote):
        raise HostKeyError(
            f"{name}: server {remote.get_name()} key does not match the trusted "
            "known_hosts entry (changed key or impersonation); refusing to log in"
        )


def _connect() -> paramiko.SFTPClient:
    trusted = _trusted_host_keys()
    user = _sftp_user()
    pw = _password(user)
    last = None
    for host in [h.strip() for h in HOSTS if h.strip()]:
        t = None
        try:
            t = paramiko.Transport((host, PORT))
            t.start_client(timeout=CONNECT_TIMEOUT)
            # Trust check happens before any credential leaves this machine.
            _verify_host_key(t, trusted, host, PORT)
            t.auth_password(user, pw)
            sftp = paramiko.SFTPClient.from_transport(t)
            print(f"connected via {host} (host key verified)")
            return sftp
        except Exception as e:
            if t is not None:
                t.close()
            last = f"{host}: {e}"
            print(f"SFTP host rejected -> {last}", file=sys.stderr)
    sys.exit(f"SFTP connect failed on all hosts -> {last}")


def _find_themes_dir(sftp: paramiko.SFTPClient) -> str | None:
    for base in (".", "sites", "public", "htdocs"):
        for candidate in (
            posixpath.join(base, "wp-content", "themes"),
            posixpath.join(base, "*", "wp-content", "themes"),
        ):
            try:
                sftp.listdir(candidate)
                return candidate
            except IOError:
                pass
    # walk two levels deep looking for wp-content/themes
    try:
        for entry in sftp.listdir("."):
            p = posixpath.join(entry, "wp-content", "themes")
            try:
                sftp.listdir(p)
                return p
            except IOError:
                continue
    except IOError:
        pass
    return None


def cmd_probe(_args) -> None:
    sftp = _connect()
    print("cwd:", sftp.normalize("."))
    print("home listing:", sorted(sftp.listdir(".")))
    themes = _find_themes_dir(sftp)
    print("themes dir:", themes)
    if themes:
        print("themes:", sorted(sftp.listdir(themes)))
    sftp.close()


def _local_version() -> str:
    with open(os.path.join(LOCAL_THEME, "style.css"), encoding="utf-8") as fh:
        for line in fh:
            if line.strip().lower().startswith("version:"):
                return line.split(":", 1)[1].strip()
    return "unknown"


def _upload_tree(sftp: paramiko.SFTPClient, local_root: str, remote_root: str) -> int:
    count = 0
    try:
        sftp.mkdir(remote_root)
    except IOError:
        pass
    for dirpath, dirnames, filenames in os.walk(local_root):
        dirnames[:] = [
            d
            for d in dirnames
            if d not in {".git", "__pycache__"} and not d.endswith(".bak")
        ]
        rel = os.path.relpath(dirpath, local_root)
        rdir = (
            remote_root
            if rel == "."
            else posixpath.join(remote_root, rel.replace(os.sep, "/"))
        )
        try:
            sftp.mkdir(rdir)
        except IOError:
            pass
        for fn in filenames:
            if fn == ".DS_Store":
                continue
            sftp.put(os.path.join(dirpath, fn), posixpath.join(rdir, fn))
            count += 1
    return count


def cmd_deploy(args) -> None:
    ver = _local_version()
    sftp = _connect()
    themes = args.remote_themes or _find_themes_dir(sftp)
    if not themes:
        sys.exit("Could not locate wp-content/themes; pass --remote-themes.")
    live = posixpath.join(themes, "kk-aurora")
    staging = posixpath.join(themes, f"kk-aurora-deploy-{ver}")
    backup = posixpath.join(themes, f"kk-aurora.bak-{int(time.time())}")

    print(f"deploying local {ver} -> {live}")
    print(f"staging upload to {staging}")
    n = _upload_tree(sftp, LOCAL_THEME, staging)
    print(f"uploaded {n} files")

    # sanity: staged style.css version matches
    with sftp.open(posixpath.join(staging, "style.css")) as fh:
        head = fh.read(4000).decode("utf-8", "replace")
    if f"Version: {ver}" not in head and f"Version:{ver}" not in head:
        sys.exit("staged style.css version mismatch; aborting before swap")

    if args.no_swap:
        print("--no-swap set; staged only, no swap performed")
        sftp.close()
        return

    print(f"swap: {live} -> {backup}, {staging} -> {live}")
    sftp.rename(live, backup)
    try:
        sftp.rename(staging, live)
    except Exception:
        sftp.rename(backup, live)  # instant rollback if the second rename fails
        raise
    print(f"done. previous theme preserved at {backup}")
    sftp.close()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe")
    dp = sub.add_parser("deploy")
    dp.add_argument(
        "--remote-themes", default=None, help="explicit wp-content/themes path"
    )
    dp.add_argument(
        "--no-swap", action="store_true", help="upload staging dir only, skip the swap"
    )
    args = ap.parse_args()
    {"probe": cmd_probe, "deploy": cmd_deploy}[args.cmd](args)


if __name__ == "__main__":
    main()
