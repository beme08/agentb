# Changelog

## v0.2.0 (2026-06-18) — open-source readiness

Packaging
- `LICENSE` (MIT) added.
- `pyproject.toml` with `[project]` metadata, optional-dependency groups (`openai`, `validate`, `dev`), and a `console_scripts` entry point `agentb = run_benchmark:main`.
- `Makefile` with `install`, `test`, `lint`, `validate`, `bench-stub`, `bench-model MODEL=<id>`, `leaderboard`, `snapshot`, `clean`.
- `ruff.toml` (line-length 100, target py310, rules E/F/W/I/B/UP).
- `requirements.txt` rewritten to point at the optional-dependency groups.

Repo hygiene
- `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1).
- `SECURITY.md` (supported versions + reporting channel).
- `CITATION.cff` (CFF 1.2.0, machine-readable citation).
- `.gitattributes` (line endings + linguist overrides + binary snapshots).
- `.github/ISSUE_TEMPLATE/{bug,feature,task-submission}.md`.
- `.github/pull_request_template.md`.
- `examples/{README.md, quickstart.py}` populated.
- `docs/PLANNED_AGENTS.md` documents the deferred Browser-Use and OpenAI CUA agents.

Agent consolidation
- Removed `agents/browser_use/` and `agents/openai_cua/`. The shipped agents are now `stub` and `openrouter` only.
- `run_benchmark.py:AGENT_REGISTRY` and the `--agent` choices shrink to match.
- `agents/openrouter/openrouter_agent.py` docstring updated to point at `docs/PLANNED_AGENTS.md`.

Tasks
- 55 skeleton tasks now have hand-authored specimen `final_answer` strings, applied via the idempotent `scripts/finalize_tasks.py`. The 5 v0.1/v0.2 golden tasks are preserved.
- `tasks/all_tasks.json` regenerated to 60 tasks.

Tests
- `tests/test_agents.py` added (4 tests: stub returns steps, openrouter handles missing key, model param passes through, interface contract).
- `tests/test_run_benchmark.py` added (2 tests: golden task scores 1.0, results.json is written).
- 12/12 tests pass.

CI
- `.github/workflows/benchmark.yml` unchanged structurally; local `make lint` adds ruff to the developer workflow.

## v0.1 (2026-06-16) — initial scaffold

Empty repo + initial commit message.

## v0.2-pre (2026-06-17) — foundation

- 60 task specs across 5 categories (15 search, 10 shopping, 10 research, 10 productivity, 15 developer)
- JSON Schema for task specs (`tasks/schema.json`)
- 5 fully-spec'd golden-trace tasks with `final_answer_check`
- Agent interface (`agents/base.py`) with Step, Trace, AgentResult, Agent ABC
- Stub agent for tests, Browser-Use wrapper, OpenAI CUA scaffold
- Evaluator combining step coverage (0.4), critical actions (0.4), final answer (0.2) with built-in failure-type classifier
- `run_benchmark.py` CLI
- pytest suite: 6 tests
- Leaderboard generator
- Docs: README, ROADMAP, REPORT_OUTLINE, CONTRIBUTING
- Dockerfile + docker-compose + GitHub Actions CI

> Note: the v0.2-pre entry is intentionally undated; the v0.2.0 release above
> supersedes it as the official open-source release.
