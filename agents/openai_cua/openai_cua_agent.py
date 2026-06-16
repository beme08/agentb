"""OpenAI Computer-Use Agent (CUA) wrapper.

This is a scaffold. The real implementation needs a Playwright sandbox
that returns screenshots to the responses API and applies the model-emitted
actions back to the page.
"""
from __future__ import annotations

import time
from ..base import Agent, AgentResult, Trace, Step


class OpenAICuaAgent(Agent):
    name = "openai-cua"

    def __init__(self, model: str = "computer-use-preview"):
        self.model = model

    def run(self, task: dict) -> AgentResult:
        t0 = time.time()
        try:
            from openai import OpenAI  # type: ignore  # noqa: F401
        except ImportError as e:
            return AgentResult(
                trace=Trace(task_id=task["id"]),
                success=False,
                error=f"openai not installed: {e}",
            )

        return AgentResult(
            trace=Trace(
                task_id=task["id"],
                steps=[Step(action="navigate", target=task.get("start_url", ""))],
            ),
            success=False,
            error="CUA loop not yet wired up. Provide a Playwright sandbox + responses API loop.",
            latency_s=time.time() - t0,
        )
