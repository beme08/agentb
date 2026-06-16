"""Task loading utilities."""
from pathlib import Path
import json
from typing import Iterator, Union


TASKS_ROOT = Path(__file__).parent

# Files at the tasks/ root that are not single-task specs.
_NON_TASK_FILES = {"schema.json", "all_tasks.json"}


def load_task(task_id: str) -> dict:
    for path in TASKS_ROOT.rglob(f"{task_id}.json"):
        return json.loads(path.read_text())
    raise FileNotFoundError(f"No task with id {task_id!r}")


def iter_tasks() -> Iterator[dict]:
    """Yield every individual task spec, one dict at a time."""
    for path in sorted(TASKS_ROOT.rglob("*.json")):
        if path.name in _NON_TASK_FILES:
            continue
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            yield data


def tasks_by_category() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for t in iter_tasks():
        out.setdefault(t["category"], []).append(t)
    return out
