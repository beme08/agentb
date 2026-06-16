"""Critical action compliance.

A critical action is a must-have observation in the trace — e.g. agent
must have visited `google.com/flights` or applied a `price < 120` filter.
We match by substring against the joined (action + target + detail) text
of each step.
"""
from __future__ import annotations


def critical_action_compliance(trace, task: dict) -> tuple[float, str]:
    critical = task.get("critical_actions", []) or []
    if not critical:
        return 1.0, "no critical actions defined"

    corpus = " ".join(
        f"{s.action} {s.target} {s.detail}".lower()
        for s in trace.steps
    )

    matched = 0
    missing: list[str] = []
    for c in critical:
        needle = c.lower()
        if needle in corpus:
            matched += 1
        else:
            missing.append(c)

    score = matched / len(critical)
    reason = f"matched {matched}/{len(critical)} critical actions"
    if missing:
        reason += f"; missing: {missing[:3]}"
    return score, reason
