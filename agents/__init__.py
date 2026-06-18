"""Agent interface for AgentBench-K.

All agents must implement `run(task) -> AgentResult` so the evaluator and
benchmark runner are agent-agnostic.
"""
from .base import Agent, AgentResult, Step, Trace

__all__ = ["Agent", "AgentResult", "Trace", "Step"]
