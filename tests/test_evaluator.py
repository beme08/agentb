"""Smoke tests for the evaluator. Run with: python -m pytest tests/ -q"""
import json
from pathlib import Path

from agents.base import Step, Trace
from evaluators import evaluate
from tasks import load_task, tasks_by_category


def _trace(steps, final=""):
    return Trace(task_id="t", steps=[Step(**s) if isinstance(s, dict) else s for s in steps], final_answer=final)


def test_all_tasks_load_and_validate_categories():
    cats = tasks_by_category()
    assert set(cats) == {"search", "shopping", "research", "productivity", "developer"}
    counts = {k: len(v) for k, v in cats.items()}
    assert counts == {"search": 15, "shopping": 10, "research": 10, "productivity": 10, "developer": 15}


def test_schema_files_are_valid_json():
    for path in Path("tasks").rglob("*.json"):
        json.loads(path.read_text())


def test_golden_task_perfect_score():
    task = load_task("wikipedia-population-tokyo")
    trace = _trace(
        [
            {"action": "navigate", "target": "https://en.wikipedia.org/wiki/Tokyo"},
            {"action": "extract", "detail": "Tokyo population 41.0 million 2023"},
            {"action": "note", "detail": "Year: 2023"},
        ],
        final="Tokyo population: 41.0 million (2023 estimate).",
    )
    result = evaluate(trace, task)
    assert result.score == 1.0
    assert result.failure_type is None


def test_missing_critical_action_classifies_as_failure():
    task = load_task("wikipedia-population-tokyo")
    trace = _trace(
        [
            {"action": "navigate", "target": "https://example.com"},
            {"action": "extract", "detail": "no wikipedia, no t"},
        ],
        final="",
    )
    result = evaluate(trace, task)
    assert result.score < 1.0
    assert result.failure_type in {"constraint_failure", "retrieval_failure"}


def test_final_answer_check_modes():
    task = {
        "id": "t",
        "category": "search",
        "goal": "",
        "start_url": "",
        "expected_steps": [],
        "critical_actions": [],
        "final_answer_check": {"mode": "contains_all", "value": ["a", "b"]},
    }
    assert evaluate(_trace([], "a and b"), task).breakdown["final_answer"] == 1.0
    assert evaluate(_trace([], "a only"), task).breakdown["final_answer"] == 0.0

    task["final_answer_check"] = {"mode": "contains_any", "value": ["x", "y"]}
    assert evaluate(_trace([], "x wins"), task).breakdown["final_answer"] == 1.0
    assert evaluate(_trace([], "neither"), task).breakdown["final_answer"] == 0.0

    task["final_answer_check"] = {"mode": "regex", "value": r"price \$(\d+)"}
    assert evaluate(_trace([], "the price $42 today"), task).breakdown["final_answer"] == 1.0
    assert evaluate(_trace([], "no price here"), task).breakdown["final_answer"] == 0.0


def test_step_coverage_handles_no_expected_steps():
    task = {
        "id": "t",
        "category": "search",
        "goal": "",
        "start_url": "",
        "expected_steps": [],
        "critical_actions": [],
    }
    assert evaluate(_trace([]), task).breakdown["steps"] == 1.0
