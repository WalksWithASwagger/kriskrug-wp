#!/usr/bin/env python3
"""Check the theme and each plugin against the PHP version its header declares.

phpcs.xml.dist's testVersion covers code with no Requires PHP header of its
own (fixes/, inc/). This runs PHPCompatibilityWP once per component, with that
component's Requires PHP as the floor, so a header that promises an older PHP
than the code supports fails.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path


REQUIRES_PHP = re.compile(r"^[\s*#/]*Requires PHP:\s*(\d+\.\d+)", re.MULTILINE)

# Tests run on the CI interpreter and never ship, so they are not held to the
# component's floor.
IGNORE = "*/tests/*,*/vendor/*,*/node_modules/*"


def requires_php(text: str) -> str | None:
    match = REQUIRES_PHP.search(text)
    return match.group(1) if match else None


def components(repo_root: Path) -> list[tuple[Path, str]]:
    """(directory, Requires PHP) for every theme and plugin that declares one."""
    headers = sorted(repo_root.glob("theme/*/style.css")) + sorted(
        repo_root.glob("plugins/*/*.php")
    )
    found: dict[Path, str] = {}
    for header in headers:
        version = requires_php(header.read_text(encoding="utf-8"))
        if version and header.parent not in found:
            found[header.parent] = version
    return list(found.items())


def default_phpcs(repo_root: Path) -> str:
    local = repo_root / "vendor/bin/phpcs"
    return str(local) if local.exists() else "phpcs"


def check(repo_root: Path, phpcs: str) -> int:
    if shutil.which(phpcs) is None:
        print(f"php-compat: {phpcs} not found. Run composer install.")
        return 1
    found = components(repo_root)
    if not found:
        print("php-compat: no Requires PHP header found under theme/ or plugins/")
        return 1

    status = 0
    for directory, version in found:
        relative = directory.relative_to(repo_root).as_posix()
        result = subprocess.run(
            [
                phpcs,
                "--standard=PHPCompatibilityWP",
                "--runtime-set",
                "testVersion",
                f"{version}-",
                "--extensions=php",
                f"--ignore={IGNORE}",
                "-q",
                "-s",
                relative,
            ],
            cwd=repo_root,
            check=False,
        )
        verdict = "ok  " if result.returncode == 0 else "FAIL"
        print(f"php-compat: {verdict} {relative} (Requires PHP {version})")
        if result.returncode != 0:
            status = 1
    if status:
        print(
            "php-compat: the code above needs a newer PHP than its Requires PHP "
            "header declares. Raise the header or change the code."
        )
    return status


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phpcs", help="phpcs binary (default: vendor/bin/phpcs)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    return check(repo_root, args.phpcs or default_phpcs(repo_root))


if __name__ == "__main__":
    raise SystemExit(main())
