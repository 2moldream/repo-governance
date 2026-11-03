#!/usr/bin/env python3
"""Install repo-governance into a Codex skills directory without overwriting."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1]
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
COPY_IGNORE = shutil.ignore_patterns(
    ".git",
    "__pycache__",
    "*.py[cod]",
    ".DS_Store",
    ".venv",
    ".pytest_cache",
)


class DeployError(RuntimeError):
    pass


def source_version() -> str:
    version_path = SOURCE / "VERSION"
    skill_path = SOURCE / "SKILL.md"
    if not skill_path.is_file():
        raise DeployError(f"source skill entry is missing: {skill_path}")
    if not version_path.is_file():
        raise DeployError(f"source version file is missing: {version_path}")
    version = version_path.read_text(encoding="utf-8").strip()
    if not VERSION_PATTERN.fullmatch(version):
        raise DeployError(f"invalid semantic version: {version}")
    return version


def deploy(destination: Path, mode: str, dry_run: bool = False) -> dict[str, str]:
    version = source_version()
    destination = destination.expanduser().resolve()
    if os.path.lexists(destination):
        raise DeployError(f"destination already exists; refusing to overwrite: {destination}")
    if destination.parent == destination:
        raise DeployError("destination cannot be the filesystem root")

    result = {
        "result": "would-install" if dry_run else "installed",
        "version": version,
        "mode": mode,
        "source": SOURCE.as_posix(),
        "destination": destination.as_posix(),
    }
    if dry_run:
        return result

    destination.parent.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        relative_source = os.path.relpath(SOURCE, destination.parent)
        destination.symlink_to(relative_source, target_is_directory=True)
    else:
        shutil.copytree(SOURCE, destination, ignore=COPY_IGNORE)

    if not (destination / "SKILL.md").is_file() or not (destination / "VERSION").is_file():
        raise DeployError("installation verification failed")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--destination",
        type=Path,
        default=Path("~/.codex/skills/repo-governance"),
    )
    parser.add_argument("--mode", choices=("symlink", "copy"), default="symlink")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = deploy(args.destination, args.mode, args.dry_run)
    except (DeployError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
