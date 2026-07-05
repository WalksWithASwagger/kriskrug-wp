#!/usr/bin/env python3
"""Package a WordPress theme or plugin for manual wp-admin upload."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "https://kriskrug.co"
SKIP_NAMES = {
    ".DS_Store",
    ".git",
    ".github",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "vendor",
}


@dataclass(frozen=True)
class ArtifactInfo:
    kind: str
    slug: str
    version: str
    zip_path: Path
    checksum: str


def run(command: list[str], *, cwd: Path = REPO_ROOT, capture: bool = True) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    return result.stdout.strip() if capture else ""


def sanitize(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    return value.strip("-") or "release"


def repo_relative(path: Path) -> Path:
    return path.resolve().relative_to(REPO_ROOT)


def parse_header_value(text: str, field: str) -> str | None:
    match = re.search(rf"^\s*\*?\s*{re.escape(field)}:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def theme_version_from_files(style_css: str, functions_php: str | None = None) -> tuple[str, list[str]]:
    version = parse_header_value(style_css, "Version")
    if not version:
        raise ValueError("theme style.css is missing a Version header")

    notes: list[str] = []
    if functions_php is not None:
        match = re.search(r"define\(\s*['\"]KK_AURORA_VERSION['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)", functions_php)
        if match and match.group(1) != version:
            raise ValueError(f"style.css Version {version} does not match KK_AURORA_VERSION {match.group(1)}")
        if not match:
            notes.append("KK_AURORA_VERSION define not found; checked style.css only")

    return version, notes


def plugin_version_from_files(slug: str, files: dict[str, str]) -> tuple[str, list[str]]:
    candidates = [f"{slug}.php"] + sorted(name for name in files if name.endswith(".php") and "/" not in name)
    for name in candidates:
        text = files.get(name)
        if not text:
            continue
        if parse_header_value(text, "Plugin Name"):
            version = parse_header_value(text, "Version")
            if not version:
                raise ValueError(f"{name} is missing a Version header")
            return version, []
    raise ValueError("could not find a root plugin PHP file with a Plugin Name header")


def version_from_directory(kind: str, slug: str, source: Path) -> tuple[str, list[str]]:
    if kind == "theme":
        style = (source / "style.css").read_text(encoding="utf-8")
        functions_path = source / "functions.php"
        functions = functions_path.read_text(encoding="utf-8") if functions_path.exists() else None
        return theme_version_from_files(style, functions)

    files = {
        path.relative_to(source).as_posix(): path.read_text(encoding="utf-8", errors="replace")
        for path in source.glob("*.php")
    }
    return plugin_version_from_files(slug, files)


def version_from_zip(kind: str, slug: str, path: Path) -> tuple[str, list[str]]:
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"{path} failed zip integrity check at {bad}")

        if kind == "theme":
            style = archive.read(f"{slug}/style.css").decode("utf-8")
            try:
                functions = archive.read(f"{slug}/functions.php").decode("utf-8")
            except KeyError:
                functions = None
            return theme_version_from_files(style, functions)

        files = {
            name.removeprefix(f"{slug}/"): archive.read(name).decode("utf-8", errors="replace")
            for name in archive.namelist()
            if name.startswith(f"{slug}/") and name.endswith(".php") and "/" not in name.removeprefix(f"{slug}/")
        }
        return plugin_version_from_files(slug, files)


def should_skip(path: Path) -> bool:
    return any(part in SKIP_NAMES for part in path.parts) or path.suffix == ".pyc"


def zip_directory(source: Path, destination: Path, slug: str) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            relative = path.relative_to(source)
            if should_skip(relative) or path.is_dir():
                continue
            archive.write(path, Path(slug) / relative)


def zip_git_tree(ref: str, source: Path, destination: Path, slug: str) -> None:
    treeish = f"{ref}:{repo_relative(source).as_posix()}"
    run(["git", "archive", "--format=zip", f"--prefix={slug}/", "-o", str(destination), treeish])


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_clean_source(source: Path) -> None:
    status = run(["git", "status", "--short", "--", str(repo_relative(source))])
    if status:
        raise SystemExit(
            "Refusing to package dirty source files. Commit/stash them first, or rerun with --allow-dirty.\n"
            + status
        )


def admin_url(kind: str, base_url: str) -> str:
    base = base_url.rstrip("/")
    if kind == "theme":
        return f"{base}/wp-admin/theme-install.php?browse=upload"
    return f"{base}/wp-admin/plugin-install.php?tab=upload"


def maybe_copy_path(path: Path) -> str | None:
    if not shutil.which("pbcopy"):
        return "pbcopy not found; path was not copied to clipboard"
    subprocess.run(["pbcopy"], input=str(path), text=True, check=True)
    return None


def maybe_open_admin(url: str) -> str | None:
    if not shutil.which("open"):
        return "open command not found; admin page was not opened"
    subprocess.run(["open", url], check=False)
    return None


def build_markdown(
    *,
    deploy: ArtifactInfo,
    rollback: ArtifactInfo | None,
    source: Path,
    base_url: str,
    label: str,
    notes: list[str],
    copied: bool,
    opened: bool,
) -> str:
    upload_url = admin_url(deploy.kind, base_url)
    lines = [
        f"# WordPress {deploy.kind.title()} Upload Package",
        "",
        f"- Source: `{source}`",
        f"- Slug: `{deploy.slug}`",
        f"- Label: `{label}`",
        f"- Version: `{deploy.version}`",
        f"- Deploy zip: `{deploy.zip_path}`",
        f"- Deploy SHA256: `{deploy.checksum}`",
    ]
    if rollback:
        lines.extend([
            f"- Rollback zip: `{rollback.zip_path}`",
            f"- Rollback version: `{rollback.version}`",
            f"- Rollback SHA256: `{rollback.checksum}`",
        ])
    else:
        lines.append("- Rollback zip: not built; pass `--rollback-ref <git-ref>` when you need one.")
    lines.extend([
        f"- wp-admin upload URL: {upload_url}",
        f"- Clipboard: {'deploy zip path copied' if copied else 'not requested'}",
        f"- Browser: {'wp-admin upload URL opened' if opened else 'not requested'}",
    ])
    if notes:
        lines.append("")
        lines.append("## Notes")
        lines.extend(f"- {note}" for note in notes)
    lines.extend([
        "",
        "## Manual Upload Gate",
        "",
        "1. Open the wp-admin upload URL.",
        f"2. Upload `{deploy.zip_path.name}`.",
        "3. Choose the WordPress replace/update flow for the existing artifact.",
        "4. Confirm WordPress reports the expected uploaded version.",
        "5. Purge PressCACHE/cache layers and run the route-specific verification for the change.",
    ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="theme/kk-aurora", help="Theme or plugin directory to package.")
    parser.add_argument("--kind", choices=("theme", "plugin"), default="", help="Artifact kind. Inferred when omitted.")
    parser.add_argument("--slug", default="", help="Zip root folder name. Defaults to the source directory name.")
    parser.add_argument("--label", default="release", help="Filename label, e.g. homepage-contrast.")
    parser.add_argument("--output-dir", default=str(Path.home() / "Desktop"), help="Where zip files are written.")
    parser.add_argument("--date", default=datetime.now(timezone.utc).strftime("%Y%m%d"), help="Filename date stamp.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--rollback-ref", default="", help="Git ref to archive as a rollback zip.")
    parser.add_argument("--rollback-label", default="rollback")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow packaging uncommitted source files.")
    parser.add_argument("--copy-path", action="store_true", help="Copy the deploy zip path to the macOS clipboard.")
    parser.add_argument("--open-admin", action="store_true", help="Open the wp-admin upload URL in the default browser.")
    parser.add_argument("--report", default="", help="Optional markdown report path to write.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = (REPO_ROOT / args.source).resolve()
    if not source.is_dir():
        raise SystemExit(f"source directory not found: {source}")

    try:
        source.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise SystemExit("source must live inside this repo") from exc

    kind = args.kind or ("plugin" if "plugins" in source.parts else "theme")
    slug = args.slug or source.name
    label = sanitize(args.label)
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if not args.allow_dirty:
        ensure_clean_source(source)

    version, notes = version_from_directory(kind, slug, source)
    deploy_path = output_dir / f"{slug}-{label}-{sanitize(version)}-{args.date}.zip"
    if deploy_path.exists():
        deploy_path.unlink()
    zip_directory(source, deploy_path, slug)
    packaged_version, zip_notes = version_from_zip(kind, slug, deploy_path)
    notes.extend(zip_notes)
    if packaged_version != version:
        raise SystemExit(f"packaged version {packaged_version} did not match source version {version}")
    deploy = ArtifactInfo(kind, slug, version, deploy_path, sha256(deploy_path))

    rollback: ArtifactInfo | None = None
    if args.rollback_ref:
        with tempfile.TemporaryDirectory(prefix="wp-artifact-rollback-") as temp:
            temp_zip = Path(temp) / "rollback.zip"
            zip_git_tree(args.rollback_ref, source, temp_zip, slug)
            rollback_version, rollback_notes = version_from_zip(kind, slug, temp_zip)
            notes.extend(f"rollback {note}" for note in rollback_notes)
            rollback_path = output_dir / f"{slug}-{sanitize(args.rollback_label)}-{sanitize(rollback_version)}-{args.date}.zip"
            if rollback_path.exists():
                rollback_path.unlink()
            shutil.copy2(temp_zip, rollback_path)
            rollback = ArtifactInfo(kind, slug, rollback_version, rollback_path, sha256(rollback_path))

    if args.copy_path:
        note = maybe_copy_path(deploy_path)
        if note:
            notes.append(note)
    if args.open_admin:
        note = maybe_open_admin(admin_url(kind, args.base_url))
        if note:
            notes.append(note)

    markdown = build_markdown(
        deploy=deploy,
        rollback=rollback,
        source=source,
        base_url=args.base_url,
        label=label,
        notes=notes,
        copied=args.copy_path,
        opened=args.open_admin,
    )
    if args.report:
        report = (REPO_ROOT / args.report).resolve()
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(markdown, encoding="utf-8")
    sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
