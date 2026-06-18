---
name: Task submission
about: Propose a new task for the benchmark
title: "[task] "
labels: ["task", "enhancement"]
---

## Task spec

```json
{
  "id": "kebab-case-id",
  "category": "search|shopping|research|productivity|developer",
  "title": "...",
  "difficulty": "easy|medium|hard",
  "goal": "...",
  "constraints": ["..."],
  "start_url": "https://...",
  "expected_steps": ["navigate ...", "search ...", "extract ..."],
  "critical_actions": ["...", "..."],
  "final_answer_check": { "mode": "contains_all|contains_any|exact|regex", "value": [...] },
  "rubric": "..."
}
```

## Why this task?

<!-- What knowledge-work skill does it exercise? Why isn't it covered by an existing task? -->

## Drift considerations

<!-- Is the expected answer stable (author/year/version) or does it shift (prices, rankings)?
If it shifts, document the snapshot date and the tolerance. -->
