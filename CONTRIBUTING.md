# Contributing

## Adding a task

1. Create `tasks/<category>/<your-task-id>.json`.
2. Follow `tasks/schema.json`.
3. Use kebab-case ids; keep them short and descriptive.
4. `expected_steps` should be 3–8 entries, each starting with a verb (`navigate`, `search`, `click`, `extract`, `note`, `submit`, ...).
5. `critical_actions` should be 2–5 substring needles that must appear somewhere in the agent's trace (action + target + detail joined).
6. For fully-spec'd golden tasks, also include:
   - `final_answer`: a sample/reference answer (used as a smoke test only).
   - `final_answer_check`: `{ "mode": "contains_all|contains_any|exact|regex", "value": ... }`.
7. Run `python3 -m pytest tests/ -q` to make sure nothing breaks.

### Categories

- `search` — lookups, definitions, factual retrieval
- `shopping` — constraint-bound product search
- `research` — paper/reading-comprehension tasks
- `productivity` — calendar, mail, drive, recipes, translation
- `developer` — github, npm, pypi, docker, kubectl, regex, error reading

## Adding an agent

Subclass `agents.base.Agent`. Implement `run(self, task) -> AgentResult`. Register the class in `run_benchmark.py:AGENT_REGISTRY`. The agent must populate `trace.steps` and `trace.final_answer`.

## Adding an evaluator check

Subclass or write a function in `evaluators/checks/` that takes a `Trace` and a `task` dict and returns `(score, reason)`. Wire it into `evaluators/evaluator.py:evaluate()`.

## Style

- Python 3.10+.
- Type hints everywhere.
- No `print` in library code; `print` only in `run_benchmark.py` CLI.
- Keep dependencies minimal. `browser-use`, `playwright`, `openai`, `langchain-openai` are optional and only imported inside agent wrappers.
