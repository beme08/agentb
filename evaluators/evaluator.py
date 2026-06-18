"""Combine individual checks into a single 0..1 score per task."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .checks import critical_action_compliance, final_answer_score, step_coverage


@dataclass
class EvaluationResult:
    task_id: str
    score: float
    breakdown: dict[str, float] = field(default_factory=dict)
    reasons: dict[str, str] = field(default_factory=dict)
    failure_type: str | None = None  # populated by failure classifier

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate(trace, task: dict, weights: dict[str, float] | None = None) -> EvaluationResult:
    """Run all checks and combine into a single weighted score.

    Default weights: steps 0.4, critical 0.4, final_answer 0.2.
    """
    w = weights or {"steps": 0.4, "critical": 0.4, "final_answer": 0.2}

    s_score, s_reason = step_coverage(trace, task)
    c_score, c_reason = critical_action_compliance(trace, task)
    f_score, f_reason = final_answer_score(trace, task)

    total = (
        w["steps"] * s_score
        + w["critical"] * c_score
        + w["final_answer"] * f_score
    )

    return EvaluationResult(
        task_id=task["id"],
        score=round(total, 3),
        breakdown={
            "steps": round(s_score, 3),
            "critical": round(c_score, 3),
            "final_answer": round(f_score, 3),
        },
        reasons={
            "steps": s_reason,
            "critical": c_reason,
            "final_answer": f_reason,
        },
        failure_type=_classify_failure(s_score, c_score, f_score),
    )


def _classify_failure(s: float, c: float, f: float) -> str | None:
    """Map a (steps, critical, final_answer) tuple to a failure taxonomy label.

    Returns None if all three are above 0.7.
    """
    if min(s, c, f) >= 0.7:
        return None
    if f < 0.5 and s >= 0.7:
        return "hallucination"  # did the right things, wrong answer
    if c < 0.5:
        return "constraint_failure"  # missed a hard requirement
    if s < 0.4:
        return "planning_failure"  # wrong action sequence
    if s < 0.7:
        return "retrieval_failure"  # got somewhere, didn't quite find it
    return "execution_failure"
