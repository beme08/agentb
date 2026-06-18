"""Base agent interface and trace data structures."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Step:
    """A single observed action in a trace.

    action: short verb (e.g. "search", "click", "extract")
    target: url or element the action was applied to
    detail: free-form extra context
    """
    action: str
    target: str = ""
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Trace:
    """Full record of an agent's run on a task."""
    task_id: str
    steps: list[Step] = field(default_factory=list)
    final_answer: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def action_sequence(self) -> list[str]:
        return [s.action.lower().strip() for s in self.steps]

    def visited_urls(self) -> list[str]:
        return [s.target for s in self.steps if s.target]

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "steps": [s.to_dict() for s in self.steps],
            "final_answer": self.final_answer,
            "metadata": self.metadata,
        }


@dataclass
class AgentResult:
    trace: Trace
    success: bool
    error: str | None = None
    latency_s: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0
    tool_calls: int = 0

    def to_dict(self) -> dict[str, Any]:
        d = self.trace.to_dict()
        d.update({
            "success": self.success,
            "error": self.error,
            "latency_s": self.latency_s,
            "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
            "cost_usd": self.cost_usd,
            "tool_calls": self.tool_calls,
        })
        return d


class Agent(ABC):
    """Common interface every concrete agent must implement."""

    name: str = "base"

    @abstractmethod
    def run(self, task: dict) -> AgentResult:
        """Execute a task and return a structured AgentResult.

        task is the parsed task spec (see tasks/schema.json).
        Implementations MUST populate `trace.steps` and `trace.final_answer`.
        """
        raise NotImplementedError
