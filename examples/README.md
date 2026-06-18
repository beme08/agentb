# Examples

Small, runnable examples that exercise AgentBench-K from a Python script.

## quickstart.py

The minimal end-to-end loop: load one task, run the stub agent, score the result, and print the breakdown.

```bash
python3 examples/quickstart.py
```

Expected output:

```
Task: wikipedia-population-tokyo
Agent: stub
Score: 1.000
  steps:        1.000
  critical:     1.000
  final_answer: 1.000
Failure type: None
```

This works without any API keys. For a real model, see the README's [Quick start](../README.md#quick-start).
