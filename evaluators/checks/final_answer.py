"""Final answer scoring.

Supports three modes declared on the task:
  - exact        : normalized string equality
  - contains_all : every required token/phrase present in final_answer
  - contains_any : at least one required token/phrase present
  - regex        : full regex match against final_answer

Scoring is binary per task (1.0 / 0.0) for the final answer component.
"""
from __future__ import annotations

import re


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def final_answer_score(trace, task: dict) -> tuple[float, str]:
    spec = task.get("final_answer_check", {}) or {}
    mode = spec.get("mode", "contains_all")
    answer = trace.final_answer or ""

    if mode == "exact":
        target = spec.get("value", "")
        ok = _norm(answer) == _norm(target)
        return (1.0 if ok else 0.0), f"exact match: {ok}"

    if mode == "contains_any":
        tokens = [t.lower() for t in spec.get("value", [])]
        hit = next((t for t in tokens if t in _norm(answer)), None)
        return (1.0 if hit else 0.0), f"contains_any hit: {hit!r}"

    if mode == "regex":
        pattern = spec.get("value", "")
        m = re.search(pattern, answer, re.IGNORECASE | re.DOTALL)
        return (1.0 if m else 0.0), f"regex hit: {bool(m)}"

    # default: contains_all
    tokens = [t.lower() for t in spec.get("value", [])]
    if not tokens:
        return 1.0, "no required tokens"
    missing = [t for t in tokens if t not in _norm(answer)]
    if not missing:
        return 1.0, f"contains_all: ok ({len(tokens)} tokens)"
    return 0.0, f"contains_all missing: {missing[:3]}"
