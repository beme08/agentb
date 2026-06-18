"""End-to-end test of the benchmark runner.

Spawns `python3 run_benchmark.py --agent stub --task wikipedia-population-tokyo`
as a subprocess and checks the score is 1.0 for the golden task.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_run_benchmark_golden_task():
    proc = subprocess.run(
        [sys.executable, "run_benchmark.py", "--agent", "stub", "--task", "wikipedia-population-tokyo"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, f"runner exited {proc.returncode}\nstdout: {proc.stdout}\nstderr: {proc.stderr}"
    # Score line should be present and equal to 1.00.
    assert "wikipedia-population-tokyo" in proc.stdout
    m = re.search(r"score=(\d+\.\d+)", proc.stdout)
    assert m is not None
    assert float(m.group(1)) == pytest.approx(1.0)


def test_run_benchmark_writes_results_json(tmp_path):
    out = tmp_path / "results.json"
    proc = subprocess.run(
        [sys.executable, "run_benchmark.py", "--agent", "stub", "--task", "wikipedia-population-tokyo", "--out", str(out)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0
    assert out.exists()
    data = json.loads(out.read_text())
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["task_id"] == "wikipedia-population-tokyo"
    assert data[0]["score"] == pytest.approx(1.0)
    assert data[0]["agent"] == "stub"
