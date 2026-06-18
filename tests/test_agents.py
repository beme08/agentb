"""Tests for the agent implementations.

These tests cover the deterministic, non-network paths: the stub agent and
the OpenRouter agent's behavior when the API key is missing or invalid.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents.stub import StubAgent

SAMPLE_TASK = {
    "id": "sample-task",
    "category": "search",
    "goal": "Find X.",
    "start_url": "https://example.com",
    "expected_steps": ["navigate Example", "search X", "extract X"],
    "critical_actions": ["example.com", "x"],
    "constraints": [],
    "rubric": "...",
    "final_answer": "Found X.",
    "final_answer_check": {"mode": "contains_all", "value": ["x"]},
}


def test_stub_agent_returns_steps_and_answer():
    agent = StubAgent()
    result = agent.run(SAMPLE_TASK)
    assert result.success is True
    assert result.trace.task_id == "sample-task"
    assert len(result.trace.steps) >= 3
    actions = result.trace.action_sequence()
    assert "navigate" in actions
    assert "search" in actions
    assert "extract" in actions
    assert result.trace.final_answer == "Found X."


def test_openrouter_agent_handles_missing_key(monkeypatch):
    """With no API key, OpenRouterAgent must return a clear error, not crash."""
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    from agents.openrouter import OpenRouterAgent

    agent = OpenRouterAgent(model="openai/gpt-4o-mini")
    result = agent.run(SAMPLE_TASK)
    assert result.success is False
    assert result.error is not None
    assert "OPENROUTER_API_KEY" in result.error
    # The trace should at least record a navigate step.
    assert result.trace.steps[0].action == "navigate"


def test_openrouter_agent_passes_for_model_param():
    """Constructor accepts and remembers the model param."""
    from agents.openrouter import OpenRouterAgent

    agent = OpenRouterAgent(model="anthropic/claude-3.5-sonnet")
    assert agent.model == "anthropic/claude-3.5-sonnet"
    assert agent.name == "openrouter"


def test_agent_interface_contract():
    """All shipped agents expose `name` and a callable `run`."""
    from agents.openrouter import OpenRouterAgent
    from agents.stub import StubAgent

    for cls in (StubAgent, OpenRouterAgent):
        assert hasattr(cls, "name")
        assert callable(cls.run)
