"""Capture a webpage snapshot for a task.

This is the reproducibility anchor for agentB. Each task's `start_url`
gets fetched once and saved to `traces/snapshots/<task_id>.html` along with
metadata. Graders can then compare what the agent saw against the snapshot
at task-creation time.

Usage:
    python3 scripts/snapshot_task.py --task wikipedia-population-tokyo
    python3 scripts/snapshot_task.py --all
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tasks import iter_tasks, load_task

SNAPSHOT_ROOT = Path("traces/snapshots")
USER_AGENT = "agentB/0.1 (research; +https://github.com/beme08)"


def capture(task: dict) -> dict:
    SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)
    out = SNAPSHOT_ROOT / f"{task['id']}.html"
    meta_path = SNAPSHOT_ROOT / f"{task['id']}.json"

    url = task.get("start_url", "")
    captured = {
        "task_id": task["id"],
        "url": url,
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": None,
        "bytes": 0,
    }
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read()
            captured["status"] = r.status
            captured["bytes"] = len(body)
            out.write_bytes(body)
    except Exception as e:
        captured["error"] = str(e)

    meta_path.write_text(json.dumps(captured, indent=2))
    return captured


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--task")
    p.add_argument("--all", action="store_true")
    args = p.parse_args()

    if args.task:
        tasks = [load_task(args.task)]
    elif args.all:
        tasks = list(iter_tasks())
    else:
        p.error("provide --task <id> or --all")

    ok, fail = 0, 0
    for t in tasks:
        c = capture(t)
        status = c.get("status", "err")
        if status == 200:
            ok += 1
        else:
            fail += 1
        print(f"  {t['id']:<40} {status}  {c.get('bytes', 0)} bytes")
    print(f"[snapshot] ok={ok} fail={fail}")


if __name__ == "__main__":
    main()
