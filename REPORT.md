# agentB: Evaluating Open Web Agents on Realistic Knowledge Work

**A 60-task benchmark for measuring how well open models complete useful browser tasks.**

## TL;DR

- **60 tasks** across search, shopping, research, productivity, and developer workflows.
- A pluggable `Agent` interface lets you swap in Browser-Use, OpenAI CUA, LangGraph, OpenHands, or your own implementation.
- Scoring is **0–1 with three weighted components** (steps 0.4, critical actions 0.4, final answer 0.2) plus a built-in **failure-type classifier** (`constraint_failure`, `retrieval_failure`, `planning_failure`, `hallucination`, `execution_failure`).
- Reference-answer evaluation against the task rubric. No live web grading — `traces/snapshots/<task>.html` captures the page state at task-creation time for diff-based grading.
- Run the leaderboard with one CLI: `python3 run_benchmark.py --agent openrouter --model anthropic/claude-3.5-sonnet --all`.

## 1. Motivation

Pass/fail metrics dominate agent benchmarks, but the interesting question is *why* an agent failed. Did it miss a constraint, plan a bad sequence, retrieve the wrong page, or just hallucinate an answer? The failure mode is the actual signal, and that signal is what tells you which model to deploy for which task.

Open models in particular are under-measured on web tasks. Most evaluation effort has gone into coding, math, and chat. We treat "use a browser" as a first-class capability that deserves a benchmark.

## 2. Benchmark Design

### 2.1 Task distribution

| Category     | Tasks | Examples |
| --- | --- | --- |
| search       | 15    | Wikipedia lookups, weather, prices, definitions |
| shopping     | 10    | Constraint-bound product search (flights, keyboards, headphones) |
| research     | 10    | ArXiv paper retrieval & summarization |
| productivity | 10    | Calendar, Gmail, Drive, recipes, translation |
| developer    | 15    | GitHub, npm, PyPI, Docker, kubectl, regex, error reading |
| **Total**    | **60**| |

### 2.2 Task schema

Every task is a single JSON file under `tasks/<category>/<id>.json` with this contract (`tasks/schema.json`):

```json
{
  "id": "kebab-case-id",
  "category": "search|shopping|research|productivity|developer",
  "title": "Short human title",
  "difficulty": "easy|medium|hard",
  "goal": "Natural-language task",
  "constraints": ["Hard requirements the agent must respect"],
  "start_url": "Where the agent should start",
  "expected_steps": ["navigate ...", "search ...", "extract ..."],
  "critical_actions": ["substring needles that must appear in the trace"],
  "final_answer_check": { "mode": "contains_all|contains_any|exact|regex", "value": [...] },
  "rubric": "Plain-language grading criteria"
}
```

The `expected_steps` are reference actions, not the only valid path. The grader gives partial credit for getting the verbs right. The `critical_actions` are the hard requirements — the agent's trace must contain those substrings somewhere. The `final_answer_check` is the only binary part of the score.

### 2.3 Why reference answers

Live web pages change. A flight price, a stock quote, or a Wikipedia population number drifts daily. We anchor grading to:

- A `final_answer_check` (usually `contains_all` against stable tokens like author names, years, license types).
- A `traces/snapshots/<task>.html` snapshot of the start page at task-creation time, useful for human grading.

Tasks that ask for live prices or inventory include explicit drift tolerance in the rubric ("price within $20 of reference"). The grader doesn't penalize small drift; it penalizes missing the constraints entirely.

### 2.4 Scoring

```
score = 0.4 * step_coverage
      + 0.4 * critical_action_compliance
      + 0.2 * final_answer_score
```

Each component returns a 0–1 float. The final score is a 0–1 float rounded to three decimals. We also emit a `failure_type` label:

| Label | Trigger |
| --- | --- |
| `constraint_failure` | `critical_actions < 0.5` |
| `retrieval_failure` | `steps` and `critical` both > 0.5 but < 0.7 |
| `planning_failure` | `steps < 0.4` |
| `hallucination` | `steps ≥ 0.7` and `final_answer < 0.5` |
| `execution_failure` | partial coverage on multiple components |
| `None` | all components ≥ 0.7 |

## 3. Experimental Setup

### 3.1 Agent interface

```python
class Agent(ABC):
    name: str

    @abstractmethod
    def run(self, task: dict) -> AgentResult: ...
```

`AgentResult` carries the `Trace` (list of `Step`s + `final_answer`), `latency_s`, `tokens_in/out`, `cost_usd`, and `tool_calls`. The same interface backs Browser-Use, OpenAI CUA, OpenRouter chat agents, and the stub.

Three agents ship in this repo:

- **stub** — synthesizes a trace from `expected_steps` for testing the framework.
- **openrouter** — chat-completions loop with `web_search` and `fetch_url` tool calls. Routes to any model on OpenRouter (Gemma, Qwen, Hermes, Kimi, DeepSeek, Llama Nemotron, Claude, GPT, etc.) with one config switch.
- **browser-use** — wraps the Browser-Use open-source framework.
- **openai-cua** — scaffold for OpenAI's Computer-Use Agent (Playwright loop is a TODO).

### 3.2 Model shortlist

Open models on OpenRouter:

- `google/gemma-3-27b-it`
- `qwen/qwen-2.5-72b-instruct`
- `nousresearch/hermes-3-llama-3.1-405b`
- `moonshotai/kimi-k2`
- `deepseek/deepseek-chat-v3`
- `nvidia/llama-3.1-nemotron-70b-instruct`

Plus proprietary baselines: `openai/gpt-4o`, `openai/gpt-4o-mini`, `anthropic/claude-3.5-sonnet`.

### 3.3 Metrics tracked per run

- Mean score and perfect-rate (1.0 across all components).
- Per-category mean score.
- Per-failure-type counts.
- Latency (seconds).
- Token usage (in / out).
- Cost (USD; OpenRouter returns this on the response).
- Tool-call count.

## 4. Results

### 4.1 Stub baseline (sanity check)

`python3 run_benchmark.py --agent stub --all`

| Agent | Mean score | Perfect | Mean latency | Total cost |
| --- | --- | --- | --- | --- |
| stub | 0.741 | 4/60 | 0.01s | $0.00 |

Per-category:

| developer | productivity | research | search | shopping |
| --- | --- | --- | --- | --- |
| 0.71 | 0.71 | 0.77 | 0.75 | 0.78 |

The stub gets step coverage and critical actions for free (it copies them from the spec) but never produces a `final_answer`, so it scores 0.20 on that component and lands in the `hallucination` bucket for the 55 non-golden tasks. This is the framework's "perfect tool-use, no knowledge" ceiling and gives us a meaningful lower bound — a real agent that does worse than this is broken.

The 4 perfect-score tasks are the 4 tasks that *also* have a `final_answer` string the stub echoes back. The 5th golden task (`good-first-issue-transcription-repo`) uses `contains_all` needles that the stub's `final_answer` already happens to include.

### 4.2 Real-agent results

The full evaluation matrix is out of scope for this report's scope. See `reports/` for per-model breakdowns. Each run writes `traces/results.json` and `python3 leaderboard/generate.py` produces `leaderboard/LEADERBOARD.md`.

## 5. Failure Analysis

### 5.1 Failure taxonomy

The classifier in `evaluators/evaluator.py` produces one of five labels per task. The interesting research question is **which failure type dominates per model**:

- *Planning failures* — wrong action sequence. Typically means the agent over-thinks, repeats itself, or skips a key step. We expect this from smaller open models.
- *Constraint failures* — agent missed a hard requirement ("under $120", "nonstop", "from 2024"). This is the failure mode that hurts the most in production: a confident wrong answer.
- *Retrieval failures* — agent got to the right neighborhood but didn't surface the specific data point. Often a search-query problem.
- *Hallucinations* — right steps, wrong final answer. Common with chat models that try to answer from memory instead of fetching.
- *Execution failures* — partial coverage everywhere; usually timeout or budget exhaustion.

### 5.2 Per-failure insight

The headline result we expect from real model runs: **constraint adherence is the gap that separates open models from proprietary ones.** Open models are getting close on retrieval and planning; the failure mode is "I'll ignore the price filter" or "I'll skip the year constraint". The most actionable research is to test whether tool-use fine-tuning or constraint-aware prompting closes that gap.

## 6. Limitations

- **Skeleton tasks, 55 of 60**, have a `final_answer_check` but the spec `final_answer` strings are illustrative. Graders should treat them as smoke tests, not ground truth.
- **Expected-step matching is verb-based and intentionally lenient.** A real trace with a more efficient route that doesn't include the literal reference verbs will lose partial credit.
- **Constraint matching is substring, not semantic.** A agent that paraphrases "less than $120" as "below 120 dollars" may pass; one that writes "$120 or less" will too. We accept the false-positive risk because the alternative (semantic matching) is unreproducible.
- **Web pages drift.** The snapshot mechanism captures the page at task-creation time. Tasks created after a major site redesign need re-snapshotting.
- **No multi-turn tasks yet.** Every task is a single user prompt. Multi-step agent loops (clarify-then-act, plan-then-execute) are future work.

## 7. Future Work

- **200+ tasks** with full golden traces.
- **Live snapshot-and-archive grading** via a Dockerized Playwright harness.
- **Multi-turn** tasks where the agent must ask clarifying questions.
- **Per-step human-rated rubric** on a 10% sample to validate the automatic grader.
- **Cost-aware leaderboard** that ranks by accuracy per dollar.
- **Continuous integration** that runs the full benchmark on every PR and updates the leaderboard automatically.

## Appendix A — Running the benchmark

```bash
# 1. Install
pip install -r requirements.txt

# 2. Validate tasks
python3 scripts/validate_tasks.py

# 3. Run unit tests
python3 -m pytest tests/ -q

# 4. Run the stub baseline
python3 run_benchmark.py --agent stub --all

# 5. Run an OpenRouter model (requires OPENROUTER_API_KEY)
python3 run_benchmark.py --agent openrouter --model anthropic/claude-3.5-sonnet --all

# 6. Generate leaderboard
python3 leaderboard/generate.py traces/results.json > leaderboard/LEADERBOARD.md

# 7. Analyze
python3 scripts/analyze_results.py traces/results.json
```

## Appendix B — Adding a task

```bash
cat > tasks/search/my-new-task.json << 'JSON'
{
  "id": "my-new-task",
  "category": "search",
  "title": "...",
  "difficulty": "easy",
  "goal": "Find X.",
  "constraints": ["..."],
  "start_url": "https://...",
  "expected_steps": ["navigate ...", "search ...", "extract ..."],
  "critical_actions": ["...", "..."],
  "final_answer_check": { "mode": "contains_all", "value": ["...", "..."] },
  "rubric": "Plain-language grading criteria"
}
JSON

python3 scripts/validate_tasks.py
python3 run_benchmark.py --agent stub --task my-new-task
```

## Appendix C — Repository layout

```
agentb/
├── agents/                 # Pluggable agent implementations
│   ├── base.py             #   Agent ABC + Trace/Step/AgentResult
│   ├── stub/               #   Synthetic trace for tests
│   ├── openrouter/         #   Chat completions + web tools
│   ├── browser_use/        #   Browser-Use wrapper
│   └── openai_cua/         #   OpenAI Computer-Use scaffold
├── evaluators/             # Scoring
│   ├── evaluator.py        #   Weighted score + failure classifier
│   └── checks/             #   step_coverage, critical_actions, final_answer
├── tasks/                  # 60 task specs across 5 categories
│   ├── schema.json
│   ├── all_tasks.json      #   Bundled dataset
│   ├── search/             #   15 tasks
│   ├── shopping/           #   10 tasks
│   ├── research/           #   10 tasks
│   ├── productivity/       #   10 tasks
│   └── developer/          #   15 tasks
├── scripts/                # validate_tasks, snapshot_task, analyze_results
├── tests/                  # pytest suite
├── traces/                 # results.json + per-task snapshots
├── reports/                # generated analysis
├── leaderboard/            # Markdown leaderboard generator
├── docs/                   # ROADMAP, REPORT_OUTLINE
├── run_benchmark.py        # CLI
├── Dockerfile              # Reproducible environment
└── README.md
```
