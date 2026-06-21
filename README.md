# agentB

[![CI](https://github.com/beme08/agentb/actions/workflows/benchmark.yml/badge.svg)](https://github.com/beme08/agentb/actions/workflows/benchmark.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status: v0.2](https://img.shields.io/badge/status-v0.2-blueviolet.svg)](CHANGELOG.md)

**A benchmark for evaluating open web agents on realistic knowledge-worker tasks.**

> "How well can open models actually complete useful browser tasks?"
> — not "Can I invent AGI?"

agentB is a 60-task benchmark spanning search, shopping, research, productivity, and developer workflows. Each task ships with a starting URL, expected step sequence, critical actions, and a rubric. A pluggable `Agent` interface lets you swap in any chat-completion model via OpenRouter.

## Quick start

```bash
# Install (editable + dev + openai + validate extras)
pip install -e .[dev,validate,openai]

# Or just the minimum
pip install -e .
```

```bash
# Run the stub agent against the search category
python3 run_benchmark.py --agent stub --category search

# Run a single task
python3 run_benchmark.py --agent stub --task wikipedia-population-tokyo

# Run everything
python3 run_benchmark.py --agent stub --all

# Run an OpenRouter model (requires OPENROUTER_API_KEY)
export OPENROUTER_API_KEY=sk-or-...
python3 run_benchmark.py --agent openrouter --model anthropic/claude-3.5-sonnet --all
```

Or via the console script (after `pip install -e .`):

```bash
agentb --agent stub --all
```

Or via the Makefile:

```bash
make install
make test
make bench-stub
make bench-model MODEL=anthropic/claude-3.5-sonnet
make leaderboard
```

Results are written to `traces/results.json`. The leaderboard is regenerated with `python3 leaderboard/generate.py traces/results.json`.

## Quick tour

Try the 12-line example in [`examples/quickstart.py`](examples/quickstart.py):

```bash
python3 examples/quickstart.py
```

It loads one task, runs the stub agent, evaluates the result, and prints the score breakdown. No API keys required.

## Status: v0.2 (open-source ready)

| Phase | Status |
| --- | --- |
| 1. Task dataset (60 tasks) | done |
| 2. Golden traces / reference answers | done (5 fully-spec'd, 55 specimen answers) |
| 3. Framework (agent interface, runner) | done |
| 4. Model evaluations | tooling ready; runs pending |
| 5. Failure taxonomy | done (in evaluator) |
| 6. Analysis / plots | `scripts/analyze_results.py` |
| 7. Docker + CI + leaderboard | done |
| 8. Report | `REPORT.md` |

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

See [`tasks/schema.json`](tasks/schema.json). Each task is a single JSON file under `tasks/<category>/<id>.json`.

**About the `final_answer` field:** every task carries a `final_answer` string that represents what a knowledgeable human would write. This is **illustrative, not ground truth** — the authoritative grader is `final_answer_check`. If you add a new task, write a specimen `final_answer` matching the needles in `final_answer_check.value`; if the real-world answer drifts, the check still catches the right thing.

## Adding a new agent

Subclass `agents.base.Agent` and implement `run(self, task) -> AgentResult`. Register the agent in `run_benchmark.py:_build_agent` and add it to the `--agent` choices list.

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

The two shipped agents are `stub` and `openrouter`. Two further agents (Browser-Use, OpenAI CUA) were deferred — see [`docs/PLANNED_AGENTS.md`](docs/PLANNED_AGENTS.md) for the design notes.

## Adding a new task

Create `tasks/<category>/<your-task-id>.json` and follow `tasks/schema.json`. Use kebab-case ids. `expected_steps` should be 3–8 entries, each starting with a verb (`navigate`, `search`, `click`, `extract`, `note`, `submit`, ...). `critical_actions` should be 2–5 substring needles that must appear in the trace. Then add a specimen `final_answer` and a `final_answer_check`, and re-run `make validate`.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full guide.

## How to cite

```bibtex
@software{agentb_2026,
  title  = {agentB: A Benchmark for Evaluating Open Web Agents on Realistic Knowledge Work},
  version = {0.2.0},
  year   = {2026},
  url    = {https://github.com/beme08/agentb},
}
```

See [`CITATION.cff`](CITATION.cff) for the machine-readable version.

## Roadmap

See [`docs/ROADMAP.md`](docs/ROADMAP.md). The full report is in [`REPORT.md`](REPORT.md).
