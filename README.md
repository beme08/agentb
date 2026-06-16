# AgentBench-K

**A benchmark for evaluating open web agents on realistic knowledge-worker tasks.**

> "How well can open models actually complete useful browser tasks?"
> — not "Can I invent AGI?"

AgentBench-K is a 60-task benchmark spanning search, shopping, research, productivity, and developer workflows. Each task ships with a starting URL, expected step sequence, critical actions, and a rubric. A pluggable `Agent` interface lets you swap in Browser-Use, OpenAI CUA, LangGraph agents, or your own implementation.

## Status: v0.1 (foundation)

| Phase | Status |
| --- | --- |
| 1. Task dataset (60 tasks) | done |
| 2. Golden traces | partial (5 fully-spec'd, 55 skeletons) |
| 3. Framework (agent interface, runner) | done |
| 4. Model evaluations | not started |
| 5. Failure taxonomy | done (in evaluator) |
| 6. Analysis / plots | not started |
| 7. Docker + leaderboard | not started |
| 8. Report | not started |

## Quick start

```bash
# Run the stub agent against the search category
python3 run_benchmark.py --agent stub --category search

# Run a single task
python3 run_benchmark.py --agent stub --task wikipedia-population-tokyo

# Run everything
python3 run_benchmark.py --agent stub --all

# Run the test suite
python3 -m pytest tests/ -q
```

Results are written to `traces/results.json`.

## Categories

| Category     | Tasks | Notes |
| --- | --- | --- |
| search       | 15    | Wikipedia, weather, prices, definitions |
| shopping     | 10    | Constraint-bound product search |
| research     | 10    | ArXiv / paper retrieval & summarization |
| productivity | 10    | Calendar, Gmail, Drive, recipes, translation |
| developer    | 15    | GitHub, npm, PyPI, Docker, kubectl, regex, error reading |
| **Total**    | **60**| |

## How scoring works

The evaluator returns a score in `[0, 1]` combining three components with default weights `0.4 / 0.4 / 0.2`:

- **steps** — fraction of `expected_steps` whose first verb appears in the agent's action sequence.
- **critical_actions** — fraction of substring needles (action + target + detail) found somewhere in the trace.
- **final_answer** — passes if the final answer satisfies the task's `final_answer_check` (modes: `exact`, `contains_all`, `contains_any`, `regex`).

A failure taxonomy label is also produced:

- `constraint_failure` — missed a hard requirement (low critical_actions).
- `retrieval_failure` — got to the right area, didn't find it.
- `planning_failure` — wrong action sequence (low steps).
- `hallucination` — right steps, wrong final answer.
- `execution_failure` — partial coverage on multiple components.
- `None` — score >= 0.7 on every component.

## Task schema

See `tasks/schema.json`. Each task is a single JSON file under `tasks/<category>/<id>.json`. Five tasks (`wikipedia-population-tokyo`, `cheap-nonstop-nyc-london`, `mechanical-keyboard-under-120`, `three-asr-low-resource-papers`, `good-first-issue-transcription-repo`) are fully spec'd with `final_answer_check`; the rest are skeletons ready to fill in.

## Adding a new agent

Subclass `agents.base.Agent` and implement `run(self, task) -> AgentResult`. Register the agent in `run_benchmark.py:AGENT_REGISTRY`.

```python
from agents.base import Agent, AgentResult, Trace, Step

class MyAgent(Agent):
    name = "my-agent"

    def run(self, task):
        return AgentResult(
            trace=Trace(task_id=task["id"], steps=[Step(action="navigate", target=task["start_url"])]),
            success=True,
        )
```

## Adding a new task

Create `tasks/<category>/<id>.json` and follow `tasks/schema.json`. Include `expected_steps` (verbs as the first word) and `critical_actions` (substring needles). For fully-spec'd golden tasks, also include `final_answer` and `final_answer_check`.

## Roadmap

See `docs/ROADMAP.md` for the full 8-phase plan.
