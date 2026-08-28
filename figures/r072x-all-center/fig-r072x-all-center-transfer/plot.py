#!/usr/bin/env python3
"""Delegate this archived package to the repository-bound generator."""

from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[3]
runpy.run_path(str(ROOT / "scripts/generate_r072x_figure.py"), run_name="__main__")
