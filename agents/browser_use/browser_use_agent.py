"""Browser-Use agent wrapper.

Browser-Use is an open-source web agent framework. Install with:
    pip install browser-use
Set OPENAI_API_KEY (or any supported provider) in your env.
"""
from __future__ import annotations

import time
from ..base import Agent, AgentResult, Trace, Step


class BrowserUseAgent(Agent):
    name = "browser-use"

    def __init__(self, model: str = "gpt-4o", llm_provider: str = "openai"):
        self.model = model
        self.llm_provider = llm_provider

    def run(self, task: dict) -> AgentResult:
        t0 = time.time()
        try:
            from browser_use import Agent as BUAgent  # type: ignore
        except ImportError as e:
            return AgentResult(
                trace=Trace(task_id=task["id"]),
                success=False,
                error=f"browser-use not installed: {e}",
            )

        try:
            from langchain_openai import ChatOpenAI  # type: ignore
            llm = ChatOpenAI(model=self.model)
        except ImportError:
            llm = None  # type: ignore

        try:
            bu = BUAgent(task=task["goal"], llm=llm) if llm else BUAgent(task=task["goal"])
            history = bu.run()
        except Exception as e:
            return AgentResult(
                trace=Trace(task_id=task["id"]),
                success=False,
                error=f"browser-use run failed: {e}",
                latency_s=time.time() - t0,
            )

        steps = []
        for item in getattr(history, "history", []) or []:
            steps.append(Step(
                action=getattr(item, "action", "step"),
                target=str(getattr(item, "url", "")),
                detail=str(getattr(item, "content", ""))[:200],
            ))

        return AgentResult(
            trace=Trace(
                task_id=task["id"],
                steps=steps,
                final_answer=str(getattr(history, "final_result", "")),
            ),
            success=True,
            latency_s=time.time() - t0,
        )
