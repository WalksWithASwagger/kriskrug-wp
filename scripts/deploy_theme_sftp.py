#!/usr/bin/env python3
"""Hands-off kk-aurora theme deploy to Pagely over SFTP (PressFTP gateway).

Password source (never argv/chat logs):
    1. Env WP_SFTP_PASSWORD (Cloud / non-macOS agents)
    2. Else macOS Keychain:
       security add-generic-password -a wpadmin5102 -s pagely-sftp-kriskrug -w "$(pbpaste)" -U

Subcommands:
    probe   Connect, print the working dir, and locate wp-content/themes.
    deploy  Upload theme/kk-aurora to a staging dir, then atomically swap it
            in (rename old -> .bak-<ver>, rename new -> kk-aurora). Instant
            rollback = swap the names back.

Deploy never deletes the previous theme; it renames it aside.
"""

import argparse
import os
import posixpath
import subprocess
import sys
import time

import paramiko

HOSTS = os.environ.get("WP_SFTP_HOST", "sftp.pressftp.com,sftp.pagely.com").split(",")
PORT = int(os.environ.get("WP_SFTP_PORT", "22"))
USER = os.environ.get("WP_SFTP_USER", "ftp51ZjdGhm02eAOQe")
KEYCHAIN_SERVICE = "pagely-sftp-kriskrug"
LOCAL_THEME = os.path.join(os.path.dirname(__file__), "..", "theme", "kk-aurora")


def _password() -> str:
    # Cloud / CI: prefer explicit env (never log it). Laptop: macOS Keychain.
    env_pw = os.environ.get("WP_SFTP_PASSWORD", "").strip()
    if env_pw:
        return env_pw
    out = subprocess.run(
        ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-a", USER, "-w"],
        capture_output=True,
        text=True,
    )
    if out.returncode != 0 or not out.stdout.strip():
        sys.exit(
            "No SFTP password. Set WP_SFTP_PASSWORD, or store Keychain "
            f"service '{KEYCHAIN_SERVICE}' account '{USER}'."
        )
    return out.stdout.rstrip("\n")


def _connect() -> paramiko.SFTPClient:
    pw = _password()
    last = None
    for host in [h.strip() for h in HOSTS if h.strip()]:
        try:
            t = paramiko.Transport((host, PORT))
            t.connect(username=USER, password=pw)
            print(f"connected via {host}")
            return paramiko.SFTPClient.from_transport(t)
        except Exception as e:
            last = f"{host}: {e}"
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
