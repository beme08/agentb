# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :x:                |

## Reporting a Vulnerability

Please do **not** file a public GitHub issue for security vulnerabilities.

Email the maintainers or open a [private security advisory][adv] on GitHub.
We aim to acknowledge new reports within 3 business days and to ship a fix
within 30 days for critical issues, longer for lower-severity ones.

## Scope

The benchmark itself is read-only research infrastructure: it loads task
specs from JSON, runs agents against URLs, and writes traces to disk. The
attack surface is:

- The `start_url` field on each task (pointed to by an attacker-controlled
  task submission).
- The `model` argument to the runner (passed through to the OpenRouter API).
- The `OPENROUTER_API_KEY` environment variable.

We do not currently:

- Execute downloaded code.
- Open local files based on task content.
- Run a server of any kind.

## Out of Scope

- Vulnerabilities in upstream dependencies (openai, jsonschema, etc.).
  Report those upstream.
- Prompt-injection attacks against the agent under test. Those are part of
  what we're benchmarking.

[adv]: https://github.com/agentbench-k/agentbench-k/security/advisories/new
