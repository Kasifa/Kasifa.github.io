#!/usr/bin/env python3
"""Capture the shared runtime environment for the R0.72S exact audit."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUNDLED_NODE = Path(
    "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/"
    "dependencies/node/bin/node"
)
NODE = Path(os.environ.get("R072S_NODE") or shutil.which("node") or BUNDLED_NODE)


def checked_output(arguments: list[str]) -> str:
    return subprocess.check_output(arguments, text=True).strip()


def main() -> None:
    if not NODE.is_file():
        raise RuntimeError(f"R0.72S Node executable is absent: {NODE}")
    lines = [
        "bundle=R0.72S Python Fraction plus independent JavaScript BigInt audit",
        f"pythonExecutable={sys.executable}",
        f"pythonVersion={sys.version.replace(chr(10), ' ')}",
        f"nodeExecutable={NODE}",
        f"nodeVersion={checked_output([str(NODE), '--version'])}",
        f"platform={platform.platform()}",
        f"machine={platform.machine()}",
        f"cpuCount={os.cpu_count()}",
        f"gitExecutable={checked_output(['which', 'git'])}",
    ]
    (ROOT / "environment.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("R0.72S shared producer/independent environment record written")


if __name__ == "__main__":
    main()
