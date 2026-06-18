"""Minimal end-to-end example: load a task, run the stub agent, print the score.

Run from the project root:
    python3 examples/quickstart.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents.stub import StubAgent  # noqa: E402
from evaluators import evaluate  # noqa: E402
from tasks import load_task  # noqa: E402


def main() -> None:
    task = load_task("wikipedia-population-tokyo")
    agent = StubAgent()
    result = agent.run(task)
    evald = evaluate(result.trace, task)

    print(f"Task: {task['id']}")
    print(f"Agent: {agent.name}")
    print(f"Score: {evald.score:.3f}")
    for k, v in evald.breakdown.items():
        print(f"  {k:<14} {v:.3f}")
    print(f"Failure type: {evald.failure_type}")


if __name__ == "__main__":
    main()
