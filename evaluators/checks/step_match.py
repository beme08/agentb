"""Step coverage check.

Compares the agent's action sequence against the task's expected_steps.
Each expected step is matched if the agent's action sequence contains a
matching action verb (case-insensitive substring).
"""
from __future__ import annotations


def step_coverage(trace, task: dict) -> tuple[float, str]:
    expected = task.get("expected_steps", []) or []
    if not expected:
        return 1.0, "no expected steps defined"

    actions = trace.action_sequence()
    if not actions:
        return 0.0, "no actions recorded"

    matched = 0
    missing: list[str] = []
    for step in expected:
        verb = step.split(" ", 1)[0].lower().strip()
        if any(verb in a for a in actions):
            matched += 1
        else:
            missing.append(step)

    score = matched / len(expected)
    reason = f"matched {matched}/{len(expected)} expected steps"
    if missing:
        reason += f"; missing: {missing[:3]}"
    return score, reason
