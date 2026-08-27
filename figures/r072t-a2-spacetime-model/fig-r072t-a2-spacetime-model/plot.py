#!/usr/bin/env python3
"""Package entry point for the canonical R0.72T figure generator."""

from pathlib import Path
import runpy


runpy.run_path(
    str(Path(__file__).resolve().parents[3] / "scripts/generate_r072t_figure.py"),
    run_name="__main__",
)
