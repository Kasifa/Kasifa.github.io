#!/usr/bin/env python3
"""Capture the Python and JavaScript environments for the R0.72P audit."""

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
NODE = Path(os.environ.get("R072P_NODE") or shutil.which("node") or BUNDLED_NODE)


def node_version() -> str:
    return subprocess.check_output([NODE, "--version"], text=True).strip()


def common() -> list[str]:
    git_executable = subprocess.check_output(["which", "git"], text=True).strip()
    return [
        f"platform={platform.platform()}",
        f"machine={platform.machine()}",
        f"cpuCount={os.cpu_count()}",
        f"gitExecutable={git_executable}",
    ]


def main() -> None:
    producer = [
        "route=producer Python Fraction exact two-carrier audit",
        f"pythonExecutable={sys.executable}",
        f"pythonVersion={sys.version.replace(chr(10), ' ')}",
        *common(),
    ]
    independent = [
        "route=independent JavaScript BigInt exact two-carrier audit",
        f"nodeExecutable={NODE}",
        f"nodeVersion={node_version()}",
        *common(),
    ]
    (ROOT / "environment.txt").write_text(
        "\n".join(producer) + "\n", encoding="utf-8", newline="\n"
    )
    (ROOT / "independent-environment.txt").write_text(
        "\n".join(independent) + "\n", encoding="utf-8", newline="\n"
    )
    print("R0.72P producer and independent environment records written")


if __name__ == "__main__":
    main()
