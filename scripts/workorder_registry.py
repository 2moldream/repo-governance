#!/usr/bin/env python3
"""Manage the shared, lock-protected repository workorder registry."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator


SCHEMA = "repo-governance.workorder_registry.v1"
STATUSES = {"reserved", "active", "completed", "abandoned"}
RECORD_FIELDS = {
    "workorder_id",
    "todo_id",
    "status",
    "owner",
    "base",
    "branch",
    "worktree",
    "placeholder",
    "external_id",
    "created_at",
    "updated_at",
}
ID_PATTERN = re.compile(r"^(WO|TD)-(\d+)$")
PLACEHOLDER_PATTERN = re.compile(r"^[0-9a-f]{40}$")
SLUG_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class RegistryError(RuntimeError):
    pass


def run_git(repo: Path, args: list[str]) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RegistryError(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout


def registry_paths(repo: Path) -> tuple[Path, Path]:
    repo = repo.resolve()
    common_dir_value = run_git(repo, ["rev-parse", "--git-common-dir"]).strip()
    common_dir = (repo / common_dir_value).resolve()
    directory = common_dir / "repo-governance"
    return directory / "workorder-registry.json", directory / "workorder.lock"


def now_text() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def empty_registry() -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "sequence": {"workorder": 0, "todo": 0},
        "records": [],
    }


def load_registry(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RegistryError(f"registry does not exist: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise RegistryError(f"cannot read registry {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise RegistryError("registry root must be an object")
    return payload


@contextmanager
def registry_lock(lock_path: Path) -> Iterator[None]:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_name = temporary.name
            json.dump(payload, temporary, ensure_ascii=False, indent=2)
            temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        os.chmod(temporary_name, 0o600)
        os.replace(temporary_name, path)
        temporary_name = None
    finally:
        if temporary_name is not None:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass


def parse_id(value: str, prefix: str) -> int:
    match = ID_PATTERN.fullmatch(value)
    if not match or match.group(1) != prefix:
        raise RegistryError(f"invalid {prefix} id: {value}")
    number = int(match.group(2))
    if number < 1:
        raise RegistryError(f"invalid {prefix} id: {value}")
    return number


def canonical_placeholder(repo: Path, placeholder: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{7,40}", placeholder):
        raise RegistryError("placeholder must be a 7-40 character hex commit id")
    try:
        full = run_git(repo, ["rev-parse", "--verify", f"{placeholder}^{{commit}}"]).strip()
    except RegistryError as exc:
        raise RegistryError(f"placeholder commit does not exist: {placeholder}") from exc
    if not re.fullmatch(r"[0-9a-f]{40}", full):
        raise RegistryError(f"git returned an invalid commit id: {full}")
    return full


def resolved_worktree(repo: Path, worktree: Path) -> str:
    value = worktree if worktree.is_absolute() else repo.resolve() / worktree
    return value.resolve().as_posix()


def validate_payload(payload: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    if payload.get("schema") != SCHEMA:
        findings.append(f"schema must be {SCHEMA}")

    sequence = payload.get("sequence")
    if not isinstance(sequence, dict) or set(sequence) != {"workorder", "todo"}:
        findings.append("sequence must contain only workorder and todo")
        sequence = sequence if isinstance(sequence, dict) else {}
    for key in ("workorder", "todo"):
        value = sequence.get(key) if isinstance(sequence, dict) else None
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            findings.append(f"sequence.{key} must be a non-negative integer")

    records = payload.get("records")
    if not isinstance(records, list):
        findings.append("records must be an array")
        return findings

    workorder_numbers: list[int] = []
    todo_numbers: list[int] = []
    branches: dict[str, str] = {}
    previous_number = 0
    for index, raw in enumerate(records):
        prefix = f"records[{index}]"
        if not isinstance(raw, dict):
            findings.append(f"{prefix} must be an object")
            continue
        if set(raw) != RECORD_FIELDS:
            missing = sorted(RECORD_FIELDS - set(raw))
            extra = sorted(set(raw) - RECORD_FIELDS)
            if missing:
                findings.append(f"{prefix} missing fields: {', '.join(missing)}")
            if extra:
                findings.append(f"{prefix} has unknown fields: {', '.join(extra)}")
            continue

        try:
            workorder_number = parse_id(str(raw["workorder_id"]), "WO")
            todo_number = parse_id(str(raw["todo_id"]), "TD")
        except RegistryError as exc:
            findings.append(str(exc))
            continue
        if workorder_number != todo_number:
            findings.append(
                f"{raw['workorder_id']} and {raw['todo_id']} must use the same number"
            )
        if workorder_number <= previous_number:
            findings.append(f"record order is not monotonic at {raw['workorder_id']}")
        previous_number = workorder_number
        workorder_numbers.append(workorder_number)
        todo_numbers.append(todo_number)

        status = raw["status"]
        if status not in STATUSES:
            findings.append(f"{raw['workorder_id']}: invalid status: {status}")
        if not isinstance(raw["owner"], str) or not raw["owner"].strip():
            findings.append(f"{raw['workorder_id']}: owner is required")
        if raw["base"] is not None and (
            not isinstance(raw["base"], str) or not raw["base"].strip()
        ):
            findings.append(f"{raw['workorder_id']}: base must be null or a non-empty string")

        branch = raw["branch"]
        if not isinstance(branch, str) or not branch.strip() or any(char.isspace() for char in branch):
            findings.append(f"{raw['workorder_id']}: branch must be a non-empty path without whitespace")
        elif branch in {"main", "master", "develop"}:
            findings.append(f"{raw['workorder_id']}: implementation branch cannot be the integration branch")
        elif branch in branches:
            findings.append(
                f"{raw['workorder_id']}: duplicate branch {branch}; first used by {branches[branch]}"
            )
        else:
            branches[branch] = str(raw["workorder_id"])

        worktree = raw["worktree"]
        if worktree is not None:
            if not isinstance(worktree, str) or not Path(worktree).is_absolute():
                findings.append(f"{raw['workorder_id']}: worktree must be null or an absolute path")
            elif not Path(worktree).exists():
                findings.append(f"{raw['workorder_id']}: worktree does not exist: {worktree}")

        placeholder = raw["placeholder"]
        if status == "reserved" and placeholder is not None:
            findings.append(f"{raw['workorder_id']}: reserved record must not have a placeholder")
        if status in {"active", "completed"} and (
            not isinstance(placeholder, str) or not PLACEHOLDER_PATTERN.fullmatch(placeholder)
        ):
            findings.append(
                f"{raw['workorder_id']}: {status} record requires a 40-character placeholder commit"
            )
        if status == "abandoned" and placeholder is not None and (
            not isinstance(placeholder, str) or not PLACEHOLDER_PATTERN.fullmatch(placeholder)
        ):
            findings.append(f"{raw['workorder_id']}: abandoned placeholder must be null or a full commit id")

        external_id = raw["external_id"]
        if external_id is not None and (
            not isinstance(external_id, str) or not external_id.strip()
        ):
            findings.append(f"{raw['workorder_id']}: external_id must be null or a non-empty string")

        for field in ("created_at", "updated_at"):
            value = raw[field]
            valid_time = False
            if isinstance(value, str):
                try:
                    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
                    valid_time = parsed.tzinfo is not None
                except ValueError:
                    valid_time = False
            if not valid_time:
                findings.append(f"{raw['workorder_id']}: {field} must be an ISO-8601 timestamp with timezone")

    sequence_workorder = sequence.get("workorder") if isinstance(sequence, dict) else None
    sequence_todo = sequence.get("todo") if isinstance(sequence, dict) else None
    if isinstance(sequence_workorder, int) and workorder_numbers and sequence_workorder != max(workorder_numbers):
        findings.append("sequence.workorder must equal the latest allocated WO number")
    if isinstance(sequence_todo, int) and todo_numbers and sequence_todo != max(todo_numbers):
        findings.append("sequence.todo must equal the latest allocated TD number")
    if isinstance(sequence_workorder, int) and not workorder_numbers and sequence_workorder != 0:
        findings.append("sequence.workorder must be 0 when records are empty")
    if isinstance(sequence_todo, int) and not todo_numbers and sequence_todo != 0:
        findings.append("sequence.todo must be 0 when records are empty")

    object_records = [row for row in records if isinstance(row, dict)]
    if len({str(row.get("workorder_id")) for row in object_records}) != len(object_records):
        findings.append("duplicate workorder_id")
    if len({str(row.get("todo_id")) for row in object_records}) != len(object_records):
        findings.append("duplicate todo_id")
    return findings


def require_record(payload: dict[str, Any], workorder_id: str) -> dict[str, Any]:
    for record in payload.get("records", []):
        if isinstance(record, dict) and record.get("workorder_id") == workorder_id:
            return record
    raise RegistryError(f"workorder does not exist: {workorder_id}")


def cmd_init(args: argparse.Namespace) -> int:
    registry_path, lock_path = registry_paths(args.repo)
    with registry_lock(lock_path):
        existed = registry_path.exists()
        if existed:
            payload = load_registry(registry_path)
        else:
            payload = empty_registry()
            atomic_write_json(registry_path, payload)
    findings = validate_payload(payload)
    if findings:
        for finding in findings:
            print(f"ERROR: {finding}", file=sys.stderr)
        return 1
    print(json.dumps({"result": "exists" if existed else "initialized", "path": str(registry_path)}, ensure_ascii=False))
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    registry_path, _ = registry_paths(args.repo)
    payload = load_registry(registry_path)
    findings = validate_payload(payload)
    if findings:
        for finding in findings:
            print(f"ERROR: {finding}", file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_allocate(args: argparse.Namespace) -> int:
    if not SLUG_PATTERN.fullmatch(args.slug):
        raise RegistryError("slug must contain only lowercase ASCII letters, digits, and hyphens")
    registry_path, lock_path = registry_paths(args.repo)
    with registry_lock(lock_path):
        payload = load_registry(registry_path)
        findings = validate_payload(payload)
        if findings:
            raise RegistryError("registry is invalid: " + "; ".join(findings))
        sequence = payload["sequence"]
        number = int(sequence["workorder"]) + 1
        if int(sequence["todo"]) + 1 != number:
            raise RegistryError("workorder and todo sequences have diverged")
        branch = f"wo/{number:03d}-{args.slug}"
        record = {
            "workorder_id": f"WO-{number:03d}",
            "todo_id": f"TD-{number:03d}",
            "status": "reserved",
            "owner": args.owner,
            "base": args.base,
            "branch": branch,
            "worktree": resolved_worktree(args.repo, args.worktree) if args.worktree else None,
            "placeholder": None,
            "external_id": args.external_id,
            "created_at": now_text(),
            "updated_at": now_text(),
        }
        sequence["workorder"] = number
        sequence["todo"] = number
        payload["records"].append(record)
        findings = validate_payload(payload)
        if findings:
            raise RegistryError("new record is invalid: " + "; ".join(findings))
        atomic_write_json(registry_path, payload)
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def cmd_activate(args: argparse.Namespace) -> int:
    registry_path, lock_path = registry_paths(args.repo)
    placeholder = canonical_placeholder(args.repo, args.placeholder)
    with registry_lock(lock_path):
        payload = load_registry(registry_path)
        findings = validate_payload(payload)
        if findings:
            raise RegistryError("registry is invalid: " + "; ".join(findings))
        record = require_record(payload, args.workorder)
        if record["status"] != "reserved":
            raise RegistryError(f"only reserved workorder can activate: {args.workorder}")
        record["status"] = "active"
        record["placeholder"] = placeholder
        if args.base is not None:
            record["base"] = args.base
        if args.branch is not None:
            record["branch"] = args.branch
        if args.worktree is not None:
            record["worktree"] = resolved_worktree(args.repo, args.worktree)
        record["updated_at"] = now_text()
        findings = validate_payload(payload)
        if findings:
            raise RegistryError("activation is invalid: " + "; ".join(findings))
        atomic_write_json(registry_path, payload)
        result = dict(record)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    registry_path, lock_path = registry_paths(args.repo)
    with registry_lock(lock_path):
        payload = load_registry(registry_path)
        findings = validate_payload(payload)
        if findings:
            raise RegistryError("registry is invalid: " + "; ".join(findings))
        record = require_record(payload, args.workorder)
        if record["status"] != "active":
            raise RegistryError(f"only active workorder can complete: {args.workorder}")
        record["status"] = "completed"
        record["updated_at"] = now_text()
        atomic_write_json(registry_path, payload)
        result = dict(record)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_abandon(args: argparse.Namespace) -> int:
    registry_path, lock_path = registry_paths(args.repo)
    with registry_lock(lock_path):
        payload = load_registry(registry_path)
        findings = validate_payload(payload)
        if findings:
            raise RegistryError("registry is invalid: " + "; ".join(findings))
        record = require_record(payload, args.workorder)
        if record["status"] not in {"reserved", "active"}:
            raise RegistryError(f"completed or abandoned workorder cannot abandon: {args.workorder}")
        record["status"] = "abandoned"
        record["updated_at"] = now_text()
        atomic_write_json(registry_path, payload)
        result = dict(record)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    registry_path, _ = registry_paths(args.repo)
    payload = load_registry(registry_path)
    findings = validate_payload(payload)
    if args.workorder:
        try:
            require_record(payload, args.workorder)
        except RegistryError as exc:
            findings.append(str(exc))
    if findings:
        for finding in findings:
            print(f"ERROR: {finding}", file=sys.stderr)
        return 1
    print("workorder registry: pass")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="create an empty shared registry")
    init_parser.set_defaults(handler=cmd_init)

    show_parser = subparsers.add_parser("show", help="show and validate the registry")
    show_parser.set_defaults(handler=cmd_show)

    allocate_parser = subparsers.add_parser("allocate", help="allocate the next WO/TD pair")
    allocate_parser.add_argument("--owner", required=True)
    allocate_parser.add_argument("--slug", required=True)
    allocate_parser.add_argument("--base")
    allocate_parser.add_argument("--worktree", type=Path)
    allocate_parser.add_argument("--external-id")
    allocate_parser.set_defaults(handler=cmd_allocate)

    activate_parser = subparsers.add_parser("activate", help="record the placeholder commit")
    activate_parser.add_argument("--workorder", required=True)
    activate_parser.add_argument("--placeholder", required=True)
    activate_parser.add_argument("--base")
    activate_parser.add_argument("--branch")
    activate_parser.add_argument("--worktree", type=Path)
    activate_parser.set_defaults(handler=cmd_activate)

    complete_parser = subparsers.add_parser("complete", help="mark an active workorder completed")
    complete_parser.add_argument("--workorder", required=True)
    complete_parser.set_defaults(handler=cmd_complete)

    abandon_parser = subparsers.add_parser("abandon", help="permanently abandon a work item")
    abandon_parser.add_argument("--workorder", required=True)
    abandon_parser.set_defaults(handler=cmd_abandon)

    validate_parser = subparsers.add_parser("validate", help="validate registry invariants")
    validate_parser.add_argument("--workorder")
    validate_parser.set_defaults(handler=cmd_validate)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except (RegistryError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
