# Report Outline

Working title: **AgentBench-K: Evaluating Open Web Agents on Realistic Knowledge Work**

## 1. Motivation

- Pass/fail metrics miss the interesting failures.
- Open-source model quality on web tasks is under-measured compared to coding/math.
- We need a benchmark that:
  - Spans realistic knowledge-work categories.
  - Reports **why** an agent failed, not just whether it did.
  - Lets the community swap in new agents and models with zero glue code.

## 2. Benchmark Design

- 60 tasks across 5 categories (search, shopping, research, productivity, developer).
- Each task: `goal`, `constraints`, `start_url`, `expected_steps`, `critical_actions`, `rubric`.
- Reference-answer evaluation. Live grading would decay as pages change; we grade against the rubric.
- Five fully-spec'd golden-trace tasks anchor the dataset; the rest are skeletons to be filled in by the community.

## 3. Experimental Setup

- Agents: Browser-Use, OpenAI CUA, LangGraph wrapper, OpenHands/OpenManus.
- Models: open shortlist (Gemma, Qwen, Hermes, Kimi, DeepSeek, Llama Nemotron) routed through OpenRouter; local Ollama for small models.
- Metrics: mean score, perfect-rate, per-category accuracy, latency, tokens, cost, failure-type distribution.
- Hardware + cost ceiling for one full run.

## 4. Results

- Per-model accuracy bar.
- Cost-efficiency scatter (accuracy per $).
- Per-category heatmap.
- Latency distribution.

## 5. Failure Analysis

- Failure-type counts per model.
- Representative traces for each failure class.
- The qualitative story: which models fail at planning vs. constraint adherence vs. retrieval.

## 6. Limitations

- Skeleton tasks don't have a `final_answer_check` yet — the leaderboard over-estimates performance on them.
- The expected-step matching is verb-based and intentionally lenient.
- "Constraint" matching is substring, not semantic — false positives are possible.
- Web pages drift; we record the snapshot date and warn graders.

## 7. Future Work

- 200+ tasks with full golden traces.
- Snapshot-and-archive grading.
- Multi-turn / multi-step agent loops.
- Per-step human-rated rubric on a 10% sample.
