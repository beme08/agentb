.PHONY: help install test lint bench-stub bench-model leaderboard snapshot validate clean

help:
	@echo "AgentBench-K make targets:"
	@echo "  install         pip install -e .[dev,validate,openai]"
	@echo "  test            run pytest"
	@echo "  lint            run ruff check"
	@echo "  validate        run JSON Schema validation on all task files"
	@echo "  bench-stub      run the stub agent on all 60 tasks"
	@echo "  bench-model     run an OpenRouter model (MODEL=anthropic/claude-3.5-sonnet)"
	@echo "  leaderboard     regenerate leaderboard/LEADERBOARD.md from traces/results.json"
	@echo "  snapshot        capture webpage snapshots (TASK=<id> or ALL=1)"
	@echo "  clean           remove caches and traces"

install:
	pip install -e .[dev,validate,openai]

test:
	python3 -m pytest tests/ -q

lint:
	ruff check .

validate:
	python3 scripts/validate_tasks.py

bench-stub:
	python3 run_benchmark.py --agent stub --all

bench-model:
	@test -n "$(MODEL)" || (echo "set MODEL=<id>, e.g. make bench-model MODEL=anthropic/claude-3.5-sonnet" && exit 1)
	python3 run_benchmark.py --agent openrouter --model $(MODEL) --all

leaderboard:
	python3 leaderboard/generate.py traces/results.json > leaderboard/LEADERBOARD.md

snapshot:
	@if [ -n "$(TASK)" ]; then \
		python3 scripts/snapshot_task.py --task $(TASK); \
	elif [ "$(ALL)" = "1" ]; then \
		python3 scripts/snapshot_task.py --all; \
	else \
		echo "set TASK=<id> or ALL=1"; \
	fi

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__ */__pycache__ */*/__pycache__
	rm -f traces/results.json
