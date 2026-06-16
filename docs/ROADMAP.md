# AgentBench-K Roadmap

## Phase 1 — Task Dataset (Weeks 1–2)

- [x] 60 tasks across 5 categories (15 / 10 / 10 / 10 / 15)
- [x] JSON Schema for task specs (`tasks/schema.json`)
- [x] Five fully-spec'd golden-trace tasks with `final_answer_check`
- [ ] Flesh out `final_answer_check` for the remaining 55 tasks
- [ ] Per-task webpage snapshots for reproducibility (stretch)

## Phase 2 — Golden Traces (Weeks 2–3)

- [x] Schema supports `expected_steps` and `critical_actions`
- [x] Evaluator that compares trace → spec
- [ ] Hand-author golden traces for 5 priority tasks per category
- [ ] Validate: stub agent vs hand-authored trace gives score ~1.0

## Phase 3 — Framework (Weeks 3–5)

- [x] Common `Agent` interface (`agents/base.py`)
- [x] Stub agent for tests (`agents/stub/`)
- [x] Browser-Use wrapper (`agents/browser_use/`)
- [x] OpenAI CUA scaffold (`agents/openai_cua/`)
- [ ] LangGraph wrapper
- [ ] OpenHands / OpenManus wrappers
- [ ] Docker sandbox for safe execution
- [ ] Cost / latency / token tracking on `AgentResult`

## Phase 4 — Model Evaluations (Weeks 5–6)

- [ ] OpenRouter integration (one config switch per model)
- [ ] Together / Fireworks integrations
- [ ] Local Ollama for small models
- [ ] Run all 60 tasks per model
- [ ] Capture traces + per-task scores

**Target model shortlist:** Gemma 4 27B, Qwen 3, Hermes, Kimi K2, DeepSeek, Llama Nemotron.

## Phase 5 — Failure Taxonomy (Weeks 6–7)

- [x] Built-in classifier in evaluator (`constraint_failure`, `retrieval_failure`, `planning_failure`, `hallucination`, `execution_failure`)
- [ ] Distribute failure types per model
- [ ] Qualitative analysis of representative traces

## Phase 6 — Analysis (Weeks 7–8)

- [ ] Per-model accuracy bar chart
- [ ] Cost-efficiency scatter (accuracy per dollar)
- [ ] Failure breakdown heatmap
- [ ] Per-category score breakdown
- [ ] Latency & token usage distributions

## Phase 7 — Open Source (Week 8)

- [ ] `Dockerfile` + `docker-compose.yml`
- [ ] CI to regenerate leaderboard on PR
- [ ] Leaderboard JSON + static site generator
- [ ] Example outputs in `traces/`
- [ ] `CONTRIBUTING.md` with task submission template

## Phase 8 — Report (Week 8)

- [ ] Write the report (see `docs/REPORT_OUTLINE.md`)
- [ ] Host on GitHub Pages
- [ ] Share on X, LinkedIn, Reddit, Hacker News

## Working principles

- **Tasks over agents.** The dataset is the artifact that outlasts any single agent.
- **Reference answers over live grading.** Live web breaks; snapshots + final-answer checks don't.
- **Pluggable, not monolithic.** Every agent speaks the same `Agent` interface.
- **Failure labels are research.** The taxonomy turns "it failed" into "it failed because X" — that's the actual contribution.
