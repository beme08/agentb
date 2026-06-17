# Changelog

## v0.1 (2026-06-17) — Foundation

- 60 task specs across 5 categories (15 / 10 / 10 / 10 / 15)
- 5 fully-spec'd golden-trace tasks with `final_answer_check`; 55 skeleton tasks now also have a `final_answer_check` with stable, drift-resistant needles
- Agent interface (`Agent`, `Trace`, `Step`, `AgentResult`) and three implementations: stub, openrouter, browser-use, openai-cua
- Evaluator with weighted score (steps 0.4, critical 0.4, final 0.2) and built-in failure-type classifier
- `run_benchmark.py` CLI with per-agent / per-task / per-category filters
- `scripts/validate_tasks.py` — JSON Schema validation
- `scripts/snapshot_task.py` — per-task webpage snapshot for reproducibility
- `scripts/analyze_results.py` — per-category / per-failure / cost-efficiency breakdown
- `leaderboard/generate.py` — Markdown leaderboard generator
- 6 pytest tests, all passing
- Dockerfile + docker-compose + .dockerignore
- GitHub Actions CI workflow
- README, ROADMAP, REPORT, REPORT_OUTLINE, CONTRIBUTING
- GitHub Pages landing page (`docs/index.html`)

## v0.0 (2026-06-16) — Initial scaffold

- Empty repo + initial commit message
