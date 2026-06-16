# AgentBench-K Leaderboard

> Auto-generated from `traces/results.json` via `python3 leaderboard/generate.py`.

This file is a placeholder. Run the benchmark with one or more agents and regenerate:

```bash
python3 run_benchmark.py --agent browser-use --all
python3 run_benchmark.py --agent openai-cua --all
python3 leaderboard/generate.py traces/results.json > leaderboard/LEADERBOARD.md
```

## Latest stub run (sanity check)

| Agent | Mean score | Perfect (1.0) | Mean latency (s) | Total cost (USD) |
| --- | --- | --- | --- | --- |
| stub | 0.922 | 27/60 | 0.01 | $0.0000 |

The stub agent does not browse the web; it produces a synthetic trace from the task's `expected_steps` so the framework can be exercised end-to-end. Real agents will score lower on the 55 skeleton tasks that lack `final_answer_check`.
