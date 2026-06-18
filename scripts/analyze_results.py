"""Analyze benchmark results: per-category, per-failure-type, cost-efficiency.

Usage:
    python3 scripts/analyze_results.py traces/results.json
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def analyze(path: str) -> None:
    rows = json.loads(Path(path).read_text())
    if not rows:
        print("no rows")
        return

    print(f"# Analysis of {len(rows)} runs\n")

    # Per-agent summary
    by_agent = defaultdict(list)
    for r in rows:
        by_agent[r["agent"]].append(r)

    print("## Per-agent summary\n")
    print("| Agent | Runs | Mean | Perfect | Mean latency | Total cost | Mean tokens |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for a, rs in sorted(by_agent.items()):
        n = len(rs)
        mean = sum(r["score"] for r in rs) / n
        perfect = sum(1 for r in rs if r["score"] == 1.0)
        lat = sum(r["latency_s"] for r in rs) / n
        cost = sum(r["cost_usd"] for r in rs)
        tok = sum(r["tokens_in"] + r["tokens_out"] for r in rs) / n
        print(f"| {a} | {n} | {mean:.3f} | {perfect}/{n} | {lat:.2f}s | ${cost:.4f} | {tok:.0f} |")

    # Per-category
    print("\n## Per-category mean score\n")
    cats = sorted({r["category"] for r in rows})
    print("| Agent | " + " | ".join(cats) + " |")
    print("| --- | " + " --- |" * len(cats))
    for a, rs in sorted(by_agent.items()):
        cells = []
        for c in cats:
            scores = [r["score"] for r in rs if r["category"] == c]
            cells.append(f"{sum(scores)/len(scores):.2f}" if scores else "-")
        print(f"| {a} | " + " | ".join(cells) + " |")

    # Failure breakdown
    print("\n## Failure-type breakdown\n")
    labels = ["execution_failure", "constraint_failure", "retrieval_failure", "planning_failure", "hallucination", "ok"]
    print("| Agent | " + " | ".join(labels) + " |")
    print("| --- | " + " --- |" * len(labels))
    for a, rs in sorted(by_agent.items()):
        c = Counter((r["failure_type"] or "ok") for r in rs)
        cells = [str(c.get(k, 0)) for k in labels]
        print(f"| {a} | " + " | ".join(cells) + " |")

    # Cost efficiency (accuracy per $)
    print("\n## Cost efficiency (accuracy per $)\n")
    for a, rs in sorted(by_agent.items()):
        cost = sum(r["cost_usd"] for r in rs)
        mean = sum(r["score"] for r in rs) / len(rs)
        if cost > 0:
            eff = mean / cost
            print(rf"- {a}: {eff:.1f} acc/$ on \${cost:.4f} total")
        else:
            print(rf"- {a}: \${cost:.4f} total (no cost data)")

    # Token efficiency
    print("\n## Token efficiency (accuracy per 1k tokens)\n")
    for a, rs in sorted(by_agent.items()):
        tok = sum(r["tokens_in"] + r["tokens_out"] for r in rs) / 1000
        mean = sum(r["score"] for r in rs) / len(rs)
        if tok > 0:
            print(f"- {a}: {mean/tok:.2f} acc/kTok on {tok:.1f}k tokens")
        else:
            print(f"- {a}: 0 tokens recorded")

    # Hardest tasks
    print("\n## 10 hardest tasks (lowest mean score across agents)\n")
    by_task = defaultdict(list)
    for r in rows:
        by_task[r["task_id"]].append(r["score"])
    hard = sorted(((tid, sum(s) / len(s)) for tid, s in by_task.items()), key=lambda x: x[1])[:10]
    for tid, s in hard:
        print(f"- `{tid}`: mean {s:.2f} across {len(by_task[tid])} runs")

    # Easiest tasks
    print("\n## 5 easiest tasks\n")
    easy = sorted(((tid, sum(s) / len(s)) for tid, s in by_task.items()), key=lambda x: -x[1])[:5]
    for tid, s in easy:
        print(f"- `{tid}`: mean {s:.2f} across {len(by_task[tid])} runs")


if __name__ == "__main__":
    analyze(sys.argv[1] if len(sys.argv) > 1 else "traces/results.json")
