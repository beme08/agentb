"""Benchmark runner.

Usage:
    python run_benchmark.py --agent stub --category search
    python run_benchmark.py --agent stub --task wikipedia-population-tokyo
    python run_benchmark.py --agent stub --all
    python run_benchmark.py --agent openrouter --model anthropic/claude-3.5-sonnet --all
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from agents.base import AgentResult, Trace
from agents.openrouter import OpenRouterAgent
from agents.stub import StubAgent
from evaluators import evaluate
from tasks import iter_tasks, load_task


def _build_agent(name: str, model: str | None):
    if name == "stub":
        return StubAgent()
    if name == "openrouter":
        return OpenRouterAgent(model=model or "openai/gpt-4o-mini")
    raise SystemExit(f"unknown agent: {name}")


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
    p.add_argument("--agent", required=True, choices=["stub", "openrouter"])
    p.add_argument("--model", default=None, help="Model id (for openrouter)")
    p.add_argument("--category")
    p.add_argument("--task")
    p.add_argument("--all", action="store_true")
    p.add_argument("--out", default="traces/results.json")
    p.add_argument("--limit", type=int, default=None, help="Cap number of tasks (for smoke tests)")
    args = p.parse_args()

    agent = _build_agent(args.agent, args.model)
    tasks = select_tasks(args)
    if args.limit:
        tasks = tasks[: args.limit]
    print(f"[bench] agent={agent.name} model={getattr(agent, 'model', '-')} tasks={len(tasks)}")

    rows: list[dict] = []
    for t in tasks:
        t0 = time.time()
        try:
            result = agent.run(t)
        except Exception as e:
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
            "model": getattr(agent, "model", None),
            "score": eval_result.score,
            "breakdown": eval_result.breakdown,
            "failure_type": eval_result.failure_type,
            "latency_s": round(result.latency_s, 3),
            "tokens_in": result.tokens_in,
            "tokens_out": result.tokens_out,
            "cost_usd": round(result.cost_usd, 6),
            "tool_calls": result.tool_calls,
            "error": result.error,
        }
        rows.append(row)
        print(f"  {t['id']:<40} score={eval_result.score:.2f}  fail={eval_result.failure_type}  cost=${row['cost_usd']}")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(rows, indent=2))

    if rows:
        avg = sum(r["score"] for r in rows) / len(rows)
        print(f"[bench] mean score: {avg:.3f}  results: {out_path}")


if __name__ == "__main__":
    main()
