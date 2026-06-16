"""Benchmark runner.

Usage:
    python run_benchmark.py --agent stub --category search
    python run_benchmark.py --agent stub --task wikipedia-population-tokyo
    python run_benchmark.py --agent stub --all
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from tasks import iter_tasks, load_task
from evaluators import evaluate
from agents.stub import StubAgent
from agents.browser_use import BrowserUseAgent
from agents.openai_cua import OpenAICuaAgent


AGENT_REGISTRY = {
    "stub": StubAgent,
    "browser-use": BrowserUseAgent,
    "openai-cua": OpenAICuaAgent,
}


def select_tasks(args) -> list[dict]:
    if args.task:
        return [load_task(args.task)]
    if args.category:
        return [t for t in iter_tasks() if t["category"] == args.category]
    if args.all:
        return list(iter_tasks())
    return list(iter_tasks())


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--agent", required=True, choices=list(AGENT_REGISTRY))
    p.add_argument("--category")
    p.add_argument("--task")
    p.add_argument("--all", action="store_true")
    p.add_argument("--out", default="traces/results.json")
    args = p.parse_args()

    agent = AGENT_REGISTRY[args.agent]()
    tasks = select_tasks(args)
    print(f"[bench] agent={agent.name} tasks={len(tasks)}")

    rows: list[dict] = []
    for t in tasks:
        t0 = time.time()
        try:
            result = agent.run(t)
        except Exception as e:
            from agents.base import Trace, AgentResult
            result = AgentResult(
                trace=Trace(task_id=t["id"]),
                success=False,
                error=f"agent crashed: {e}",
                latency_s=time.time() - t0,
            )
        eval_result = evaluate(result.trace, t)
        row = {
            "task_id": t["id"],
            "category": t["category"],
            "agent": agent.name,
            "score": eval_result.score,
            "breakdown": eval_result.breakdown,
            "failure_type": eval_result.failure_type,
            "latency_s": round(result.latency_s, 3),
            "tokens_in": result.tokens_in,
            "tokens_out": result.tokens_out,
            "cost_usd": result.cost_usd,
            "error": result.error,
        }
        rows.append(row)
        print(f"  {t['id']:<40} score={eval_result.score:.2f}  failure={eval_result.failure_type}")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(rows, indent=2))

    # Quick summary
    if rows:
        avg = sum(r["score"] for r in rows) / len(rows)
        print(f"[bench] mean score: {avg:.3f}  results: {out_path}")


if __name__ == "__main__":
    main()
