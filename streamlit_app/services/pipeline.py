from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PIPELINE_SCRIPT = ROOT / "docs" / "05_mlops" / "run_pipeline.py"


def run_pipeline(model: str = "all") -> tuple[bool, str]:
    completed = subprocess.run(
        [sys.executable, str(PIPELINE_SCRIPT), "--model", model],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    return completed.returncode == 0, output
