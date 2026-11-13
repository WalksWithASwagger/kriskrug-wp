#!/usr/bin/env python3
"""Fail when a change adds a large file, or media outside the allowlist.

Compares the merge base of BASE_REF and HEAD with HEAD. Only blobs that are
new to the repository count: a file that already exists in the base tree, or
was moved or copied from one that does, adds nothing to history.
"""

from __future__ import annotations

import argparse
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path


MAX_BYTES = 5 * 1024 * 1024

# Media may be committed only where code ships or reads it. Anything else
# belongs in the WordPress media library or the private knowledge-base repo.
ALLOWED_MEDIA_PREFIXES = (
    "theme/kk-aurora/assets/",
    "plugins/kk-practice/tests/",
    # Events catalog rows point at repo:scripts/events_page/heroes/... and
    # the renderer reads them from there.
    "scripts/events_page/heroes/",
)

MEDIA_EXTENSIONS = frozenset(
    {
        # Images
        ".avif",
        ".bmp",
        ".dng",
        ".gif",
        ".heic",
        ".heif",
        ".ico",
        ".jpeg",
        ".jpg",
        ".png",
        ".psd",
        ".svg",
        ".tif",
        ".tiff",
        ".webp",
        # Video
        ".avi",
        ".m4v",
        ".mkv",
        ".mov",
        ".mp4",
        ".mpeg",
        ".mpg",
        ".webm",
        ".wmv",
        # Audio
        ".aac",
        ".aif",
        ".aiff",
        ".flac",
        ".m4a",
        ".mp3",
        ".oga",
        ".ogg",
        ".opus",
        ".wav",
    }
)

REGULAR_FILE_MODES = ("100644", "100755")


@dataclass(frozen=True)
class Violation:
    path: str
    size: int
    reason: str


def _git(repo_root: Path, *args: str, stdin: bytes | None = None) -> bytes:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        input=stdin,
        check=True,
        capture_output=True,
    ).stdout


def merge_base(repo_root: Path, base_ref: str, head_ref: str = "HEAD") -> str:
    return _git(repo_root, "merge-base", base_ref, head_ref).decode().strip()


def _new_blobs(repo_root: Path, base: str, head_ref: str) -> list[tuple[str, str]]:
    """(path, blob) for every regular file added or changed from base."""
    raw = _git(
        repo_root, "diff", "--raw", "--no-abbrev", "--no-renames", "-z", base, head_ref
    )
    fields = raw.split(b"\0")
    blobs = []
    # -z --raw emits ":<old mode> <new mode> <old sha> <new sha> <status>"
    # followed by the path as the next NUL-separated field.
    for meta, path in zip(fields[0::2], fields[1::2]):
        if not meta:
            continue
        _, new_mode, _, new_sha, status = meta.decode().lstrip(":").split(" ")
        if status == "D" or new_mode not in REGULAR_FILE_MODES:
            continue
        blobs.append((os.fsdecode(path), new_sha))
    return blobs


def _blobs_in_tree(repo_root: Path, ref: str) -> set[str]:
    listing = _git(repo_root, "ls-tree", "-r", "-z", ref)
    return {
        entry.split(b"\t")[0].split(b" ")[2].decode()
        for entry in listing.split(b"\0")
        if entry
    }


def _blob_sizes(repo_root: Path, shas: list[str]) -> dict[str, int]:
    if not shas:
        return {}
    out = _git(
        repo_root,
        "cat-file",
        "--batch-check=%(objectname) %(objectsize)",
        stdin="".join(f"{sha}\n" for sha in shas).encode(),
    )
    sizes = {}
    for line in out.decode().splitlines():
        sha, size = line.split(" ")
        sizes[sha] = int(size)
    return sizes


def is_media(path: str) -> bool:
    return Path(path).suffix.lower() in MEDIA_EXTENSIONS


def is_allowed_media_path(path: str) -> bool:
    return path.startswith(ALLOWED_MEDIA_PREFIXES)


def find_violations(
    repo_root: Path, base_ref: str, head_ref: str = "HEAD"
) -> list[Violation]:
    base = merge_base(repo_root, base_ref, head_ref)
    existing = _blobs_in_tree(repo_root, base)
    candidates = [
        (path, sha)
        for path, sha in _new_blobs(repo_root, base, head_ref)
        if sha not in existing
    ]
    sizes = _blob_sizes(repo_root, sorted({sha for _, sha in candidates}))

    violations = []
    for path, sha in sorted(candidates):
        size = sizes[sha]
        if size > MAX_BYTES:
            violations.append(Violation(path, size, "over the 5 MB limit"))
        elif is_media(path) and not is_allowed_media_path(path):
            violations.append(Violation(path, size, "media outside the allowlist"))
    return violations


def format_size(size: int) -> str:
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    return f"{size / 1024:.1f} KB"


def report(violations: list[Violation], base_ref: str) -> int:
    if not violations:
        print(
            f"large-file check: no new large files or media outside the allowlist (base {base_ref})"
        )
        return 0
    print(f"large-file check: {len(violations)} file(s) blocked (base {base_ref})")
    for item in violations:
        print(f"  {item.path}  {format_size(item.size)}  {item.reason}")
    print()
    print("Files over 5 MB are blocked everywhere. Images, video and audio may be")
    print("committed only under: " + ", ".join(ALLOWED_MEDIA_PREFIXES))
    print(
        "Put media in the WordPress media library or the private knowledge-base repo."
    )
    print("See CONTRIBUTING.md, 'Large files and media'.")
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--head-ref", default="HEAD")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    return report(
        find_violations(repo_root, args.base_ref, args.head_ref), args.base_ref
    )


if __name__ == "__main__":
    raise SystemExit(main())
