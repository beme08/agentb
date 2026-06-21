# Running agentB against a local model server

agentB works with **any OpenAI-compatible chat completions endpoint**.
That includes OpenRouter (the shipped `--agent openrouter` path) and a
wide range of local servers: omlx, LM Studio, llama.cpp, vLLM, Ollama,
LocalAI. This document shows the pattern.

> The shipped `--agent` choices are `stub` and `openrouter`. We
> intentionally do not ship a `--agent local` choice because the URL,
> API key, and model id depend on which local server you run. Adding
> one to the public registry would mean committing to a particular
> default that would not work for most users. The pattern below is five
> lines and works for everyone.

## Pattern: subclass `OpenRouterAgent`

`OpenRouterAgent` is a thin wrapper around `openai.OpenAI` with a
custom `base_url`. The same class works against any
OpenAI-compatible server:

```python
# my_local_agent.py
from agents.openrouter import OpenRouterAgent


class MyLocalAgent(OpenRouterAgent):
    name = "my-local"

    def _client(self):
        from openai import OpenAI
        return OpenAI(
            base_url="http://127.0.0.1:8001/v1",   # omlx, LM Studio, llama.cpp, etc.
            api_key="not-needed",                  # most local servers ignore this
        )
```

Then wire it into `run_benchmark.py:_build_agent` (one new branch) and
add it to the `--agent` choices list. Total change: ~10 lines.

## What works where

| Server | OpenAI-compat? | Tool calling? | Notes |
| --- | --- | --- | --- |
| omlx (MLX)        | yes | depends on model | Apple Silicon, auto-shuts-down on idle |
| LM Studio         | yes | yes                | Cross-platform, has a built-in UI |
| llama.cpp server  | yes | model-dependent     | `--host 0.0.0.0 --port 8080` |
| vLLM              | yes | yes                | NVIDIA / AMD GPU, fastest throughput |
| Ollama            | yes (via `/v1`) | model-dependent | `OLLAMA_ORIGINS=* ollama serve` |
| LocalAI           | yes | yes                | Multi-model, gallery install |

For agentB, you need a model that supports tool calls on the chat
completions endpoint. A 7B+ model fine-tuned for tool use (Qwen 2.5
Instruct, Llama 3.1 Instruct, Mistral Nemo) will work. Sub-3B models
will struggle.

## What to do when it does not work

1. Check the server is reachable from the same machine:
   `curl http://127.0.0.1:8001/v1/models`
2. Check the model id is one the server actually serves. List it via
   the same `/v1/models` endpoint.
3. Check the server has tool-calling enabled. Most do by default; some
   need a flag.
4. Read the OpenAI SDK trace if you set `OPENAI_LOG=debug` in the
   shell before running agentB.

## What this document is not

- It is not a tutorial for omlx, LM Studio, llama.cpp, vLLM, or any
  other server. Each has its own docs.
- It is not a recommendation. Pick the server that fits your hardware
  and your model of choice.
- It does not change the shipped `--agent` choices on `main`. The
  pattern above is a 5-line subclass; ship it as a local helper or as
  a third-party agent, your call.
