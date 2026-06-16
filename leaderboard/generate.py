"""Generate a Markdown leaderboard from traces/results.json.

Usage:
    python3 leaderboard/generate.py traces/results.json > leaderboard/LEADERBOARD.md
"""
import json
import sys
from collections import defaultdict
from pathlib import Path


def main(path: str) -> None:
    rows = json.loads(Path(path).read_text())

    by_agent = defaultdict(list)
    for r in rows:
        by_agent[r["agent"]].append(r)

    print("# AgentBench-K Leaderboard\n")
    print(f"Tasks evaluated: {len(rows)}\n")
    print("| Agent | Mean score | Perfect (1.0) | Mean latency (s) | Total cost (USD) |")
    print("| --- | --- | --- | --- | --- |")

    for agent, agent_rows in sorted(by_agent.items()):
        n = len(agent_rows)
        mean = sum(r["score"] for r in agent_rows) / n
        perfect = sum(1 for r in agent_rows if r["score"] == 1.0)
        mean_latency = sum(r["latency_s"] for r in agent_rows) / n
        total_cost = sum(r["cost_usd"] for r in agent_rows)
        print(f"| {agent} | {mean:.3f} | {perfect}/{n} | {mean_latency:.2f} | ${total_cost:.4f} |")

    # Per-category breakdown
    by_agent_cat = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by_agent_cat[r["agent"]][r["category"]].append(r["score"])

    cats = sorted({r["category"] for r in rows})
    print("\n## Per-category accuracy\n")
    print("| Agent | " + " | ".join(cats) + " |")
    print("| --- | " + " --- |" * len(cats))
    for agent, cat_scores in sorted(by_agent_cat.items()):
        cells = []
        for c in cats:
            scores = cat_scores.get(c, [])
            mean = sum(scores) / len(scores) if scores else 0.0
            cells.append(f"{mean:.2f}")
        print(f"| {agent} | " + " | ".join(cells) + " |")

    # Failure breakdown
    from collections import Counter
    print("\n## Failure breakdown\n")
    print("| Agent | " + " | ".join(["execution", "constraint", "retrieval", "planning", "hallucination", "ok"]) + " |")
    print("| --- | " + " --- |" * 6)
    for agent, agent_rows in sorted(by_agent.items()):
        c = Counter(r["failure_type"] or "ok" for r in agent_rows)
        cells = [str(c.get(k, 0)) for k in ["execution_failure", "constraint_failure", "retrieval_failure", "planning_failure", "hallucination", "ok"]]
        print(f"| {agent} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "traces/results.json")
