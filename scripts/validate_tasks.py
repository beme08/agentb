"""Validate every task file against tasks/schema.json.

Usage:
    python3 scripts/validate_tasks.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

try:
    import jsonschema  # type: ignore
except ImportError:
    jsonschema = None

from tasks import iter_tasks


SCHEMA = json.loads((ROOT / "tasks" / "schema.json").read_text())


def _check_required(task: dict, path: Path, errors: list[str]) -> None:
    for key in SCHEMA["required"]:
        if key not in task:
            errors.append(f"{path.name}: missing required key {key!r}")
    if "id" in task and not re.match(r"^[a-z0-9-]+$", task["id"]):
        errors.append(f"{path.name}: id {task['id']!r} must match ^[a-z0-9-]+$")
    if "category" in task and task["category"] not in SCHEMA["properties"]["category"]["enum"]:
        errors.append(f"{path.name}: category {task['category']!r} not in enum")
    if "expected_steps" in task:
        for s in task["expected_steps"]:
            if not s or " " not in s:
                errors.append(f"{path.name}: expected_step {s!r} should be a verb phrase")
    if "final_answer_check" in task:
        fac = task["final_answer_check"]
        if fac.get("mode") not in {"exact", "contains_all", "contains_any", "regex"}:
            errors.append(f"{path.name}: invalid final_answer_check.mode {fac.get('mode')!r}")


def main() -> int:
    errors: list[str] = []
    total = 0
    cats: dict[str, int] = {}
    for t in iter_tasks():
        total += 1
        cats[t["category"]] = cats.get(t["category"], 0) + 1
        path = next(ROOT.rglob(f"{t['id']}.json"))
        if jsonschema is not None:
            try:
                jsonschema.validate(t, SCHEMA)
            except jsonschema.ValidationError as e:
                errors.append(f"{path.name}: {e.message}")
        else:
            _check_required(t, path, errors)

    print(f"Validated {total} tasks across {len(cats)} categories.")
    for c, n in sorted(cats.items()):
        print(f"  {c}: {n}")
    if errors:
        print(f"\n{len(errors)} errors:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nAll tasks valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
