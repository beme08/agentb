# Planned Agents

This release ships two agents:

- **`stub`** — synthesizes a trace from `expected_steps` for tests and as a framework sanity check.
- **`openrouter`** — a chat-completions loop with `web_search` (DuckDuckGo HTML) and `fetch_url` (urllib) tool calls. Routes to any model on OpenRouter.

Two further agents were considered and **deferred** to a follow-up release because they require either a heavy dependency stack or a custom browser harness that is not yet implemented in this repo.

## Why these were deferred

| Agent | Why deferred |
| --- | --- |
| **Browser-Use** | Browser-Use ([browser-use](https://github.com/browser-use/browser-use)) is a moving target: the public API has shifted across releases, and it requires a LangChain LLM object plus a Playwright install. The original wrapper here was a 64-line sketch that imported Browser-Use and fell back to `llm=None`, which would have failed at runtime. Shipping a broken wrapper would mislead users. |
| **OpenAI CUA** | The Computer-Use Agent API requires a Playwright sandbox that returns screenshots to the model and applies the model-emitted actions back to the page. That harness is non-trivial (DOM diffing, action validation, screenshot sizing) and was intentionally left as a `success=False` scaffold rather than a half-working implementation. |

If you want either agent now, see "Reimplementing" below.

## The contract

All agents implement:

```python
class Agent(ABC):
    name: str

    @abstractmethod
    def run(self, task: dict) -> AgentResult: ...
```

`AgentResult` carries:

- `trace.steps` — list of `Step(action, target, detail)` observations
- `trace.final_answer` — the agent's final textual answer
- `latency_s`, `tokens_in`, `tokens_out`, `cost_usd`, `tool_calls`
- `success` (bool) and `error` (str | None) for fast failure reporting

The evaluator (`evaluators/evaluator.py`) consumes these and produces a `score` in `[0, 1]` plus a `failure_type` label.

## Reimplementing Browser-Use

```python
from browser_use import Agent as BUAgent
from langchain_openai import ChatOpenAI
from agents.base import Agent, AgentResult, Trace, Step

class BrowserUseAgent(Agent):
    name = "browser-use"

    def __init__(self, model: str = "gpt-4o"):
        self.model = model

    def run(self, task: dict) -> AgentResult:
        import time
        t0 = time.time()
        llm = ChatOpenAI(model=self.model)
        bu = BUAgent(task=task["goal"], llm=llm)
        history = bu.run()
        steps = [
            Step(
                action=getattr(item, "action", "step"),
                target=str(getattr(item, "url", "")),
                detail=str(getattr(item, "content", ""))[:200],
            )
            for item in (getattr(history, "history", []) or [])
        ]
        return AgentResult(
            trace=Trace(task_id=task["id"], steps=steps, final_answer=str(getattr(history, "final_result", ""))),
            success=True,
            latency_s=time.time() - t0,
        )
```

Then add it to `run_benchmark.py:_build_agent` and to the `--agent` choices.

## Reimplementing OpenAI CUA

A working CUA loop needs four pieces:

1. A Playwright browser that returns screenshots at a fixed resolution (e.g. 1024x768).
2. A loop that POSTs `{screenshot, goal, last_n_actions}` to the OpenAI Responses API with `tools=[{"type": "computer_use_preview", "display_width": 1024, "display_height": 768}]`.
3. An action dispatcher that translates the model-emitted `click(x, y)`, `type(text)`, `keypress(k)` calls back into Playwright commands.
4. A safety check that refuses to navigate to URLs not on an allow-list (CUA can otherwise type arbitrary URLs into the address bar).

The `openai` Python SDK supports the Responses API; see [OpenAI Computer-Use docs](https://platform.openai.com/docs/guides/tools-computer-use) for the action schema.

## A note on scope

The benchmark's value comes from the **tasks**, not the agents. The current 60 tasks are designed to be solvable with the openrouter agent's search + fetch tool pair; tasks that require real browser interaction (e.g. "apply this filter on Amazon") will fail the openrouter agent in informative ways — they show up in the leaderboard as `constraint_failure` or `execution_failure`, which is itself a useful signal.

If a browser-using agent is added, those same tasks will start passing. That's a feature, not a bug: the failure-type breakdown tells you what each agent can and cannot do.
