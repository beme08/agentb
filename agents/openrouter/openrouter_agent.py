"""OpenRouter agent.

OpenRouter exposes a single OpenAI-compatible endpoint with one env var:
    OPENROUTER_API_KEY
and a single base URL: https://openrouter.ai/api/v1

We use the chat completions endpoint directly. The agent is a *planner*
that emits a sequence of tool calls against a simple web-search + page-fetch
tool pair, NOT a full browser-use loop. It scores on tasks where the
information is one or two hops away (search/research) and acts as a
realistic upper bound for the no-browser baseline.

For tasks that need real browser interaction, use `BrowserUseAgent` or
`OpenAICuaAgent` instead.
"""
from __future__ import annotations

import json
import os
import time
from typing import Any

from ..base import Agent, AgentResult, Trace, Step


WEB_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web and return the top 10 results with URL, title, snippet.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_url",
            "description": "Fetch the contents of a URL and return a plain-text excerpt (first ~4000 chars).",
            "parameters": {
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"],
            },
        },
    },
]


SYSTEM_PROMPT = """You are a web agent. You solve tasks by calling tools in a loop.
Use web_search to find information, then fetch_url to read the relevant page.
When you have enough information to answer, respond with a single line:

ANSWER: <your concise answer>

Do not be verbose. Do not explain your reasoning. Just call tools and produce
the final ANSWER line."""


class OpenRouterAgent(Agent):
    name = "openrouter"

    def __init__(self, model: str = "openai/gpt-4o-mini", max_steps: int = 6):
        self.model = model
        self.max_steps = max_steps

    def _client(self):
        from openai import OpenAI
        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ["OPENROUTER_API_KEY"],
        )

    def run(self, task: dict) -> AgentResult:
        t0 = time.time()
        steps: list[Step] = [Step(action="navigate", target=task.get("start_url", ""))]
        tokens_in = 0
        tokens_out = 0
        cost = 0.0
        tool_calls = 0
        final = ""

        if not os.environ.get("OPENROUTER_API_KEY"):
            return AgentResult(
                trace=Trace(task_id=task["id"], steps=steps),
                success=False,
                error="OPENROUTER_API_KEY not set",
                latency_s=time.time() - t0,
            )

        try:
            client = self._client()
            messages: list[dict[str, Any]] = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Start URL: {task.get('start_url','')}\n\nTask: {task['goal']}\n\nConstraints: {task.get('constraints',[])}"},
            ]
            for _ in range(self.max_steps):
                resp = client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=WEB_TOOLS,
                    tool_choice="auto",
                    max_tokens=512,
                )
                msg = resp.choices[0].message
                tokens_in += resp.usage.prompt_tokens if resp.usage else 0
                tokens_out += resp.usage.completion_tokens if resp.usage else 0
                if hasattr(resp, "usage") and getattr(resp.usage, "cost", None):
                    cost += resp.usage.cost
                messages.append(msg)
                if msg.content and "ANSWER:" in msg.content:
                    final = msg.content.split("ANSWER:", 1)[1].strip()
                    steps.append(Step(action="answer", detail=final))
                    break
                if not msg.tool_calls:
                    if msg.content:
                        final = msg.content.strip()
                        steps.append(Step(action="answer", detail=final))
                    break
                for call in msg.tool_calls:
                    tool_calls += 1
                    args = json.loads(call.function.arguments or "{}")
                    if call.function.name == "web_search":
                        out = _web_search(args.get("query", ""))
                        steps.append(Step(action="search", target=args.get("query", ""), detail=out[:200]))
                        messages.append({"role": "tool", "tool_call_id": call.id, "content": out})
                    elif call.function.name == "fetch_url":
                        out = _fetch_url(args.get("url", ""))
                        steps.append(Step(action="fetch", target=args.get("url", ""), detail=out[:200]))
                        messages.append({"role": "tool", "tool_call_id": call.id, "content": out})
        except Exception as e:
            return AgentResult(
                trace=Trace(task_id=task["id"], steps=steps, final_answer=final),
                success=False,
                error=f"openrouter run failed: {e}",
                latency_s=time.time() - t0,
                tokens_in=tokens_in, tokens_out=tokens_out, cost_usd=cost, tool_calls=tool_calls,
            )

        return AgentResult(
            trace=Trace(task_id=task["id"], steps=steps, final_answer=final),
            success=True,
            latency_s=time.time() - t0,
            tokens_in=tokens_in, tokens_out=tokens_out, cost_usd=cost, tool_calls=tool_calls,
        )


def _web_search(query: str) -> str:
    """Best-effort web search via DuckDuckGo HTML; no API key required."""
    import urllib.parse
    import urllib.request
    url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"search error: {e}"
    # Cheap extract of result blocks.
    import re
    results = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.*?)</a>.*?<a class="result__snippet"[^>]*>(.*?)</a>', html, re.S)
    out = []
    for href, title, snippet in results[:8]:
        title = re.sub(r"<[^>]+>", "", title).strip()
        snippet = re.sub(r"<[^>]+>", "", snippet).strip()
        out.append(f"- {title}\n  {href}\n  {snippet}")
    return "\n".join(out) or "no results"


def _fetch_url(url: str) -> str:
    import urllib.request
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return f"fetch error: {e}"
    import re
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.S | re.I)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:4000]
