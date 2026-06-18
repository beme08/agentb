"""Stub agent used for tests and as a runnable example.

Reads `task["expected_steps"]` and produces a synthetic trace. This lets the
evaluator and benchmark loop be exercised end-to-end without hitting the web.
"""
from __future__ import annotations

from ..base import Agent, AgentResult, Step, Trace


class StubAgent(Agent):
    name = "stub"

    def run(self, task: dict) -> AgentResult:
        steps = [Step(action="navigate", target=task.get("start_url", ""))]
        for s in task.get("expected_steps", []):
            action = s.split(" ", 1)[0].lower() if s else "step"
            steps.append(Step(action=action, detail=s))
        steps.append(Step(action="answer"))
        return AgentResult(
            trace=Trace(task_id=task["id"], steps=steps, final_answer=task.get("final_answer", "")),
            success=True,
            latency_s=0.01,
        )
