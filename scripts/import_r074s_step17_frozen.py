#!/usr/bin/env python3
"""Import the frozen R0.74S Step 17 package without altering its bytes."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R074S_STEP17_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
EXPECTED_HEAD = "b0bba3bc965ecf616028d50c28615a486ac30a70"

FILES = {
    "research/r074s_recurrent_streamline_temporal_tail_obstruction.md": "7d204b326be45a82bc0d8531ea2f2d894c0c125b76e3ccbf02fdc1978a6011c5",
    "research/r074s_recurrent_streamline_primary_audit.md": "1efc7a520570c22952d7b06b0486865a767981f5303f102380eb9963754a1d4c",
    "research/r074s_recurrent_streamline_independent_audit.md": "255eea01cea10367b1d4051ea960214112ca8473a8b6df47ead4e199727afff3",
    "research/r074s_recurrent_streamline_literature_audit.md": "6c7c58da5250263e2509aa7c66f66bd7b02ef9fc7b920ce5c409661879a73ec8",
    "research/r074s_recurrent_streamline_certificate.json": "a4acf1769e9b56f372b15bfa0155755cb9f0a55a9a314f431d3df0add6f99c0c",
    "research/r074s_recurrent_streamline_certificate_report.md": "efb25a4068957b17910fdf9c345ad92f383d5525c316cad98d763e642c44d202",
    "research/r074s_recurrent_streamline_independent_report.md": "c3b33e4289ecb69f7958174569b55321cfec029fa1fd004c0fde996296742dc8",
    "scripts/r074s_recurrent_streamline_certificate.py": "139a5ce3d36d11b9480f246cc8f7c5297dd3ca86edb5938849e04b7f9f2eddab",
    "scripts/r074s_recurrent_streamline_independent.rb": "6c5181f64d6db424fa280a1a0886005049863a1eef602202631895ab0b95fadb",
}

FIGURE_DIRECTORY = "research/figures/r074s/fig-r074s-recurrent-tail-obstruction"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=SOURCE, text=True).strip()
    if head != EXPECTED_HEAD:
        raise SystemExit(f"frozen source HEAD drift: {head} != {EXPECTED_HEAD}")

    for relative, expected in FILES.items():
        source = SOURCE / relative
        if sha256(source) != expected:
            raise SystemExit(f"frozen source hash drift: {relative}")
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if sha256(target) != expected:
            raise SystemExit(f"import hash drift: {relative}")

    source_figure = SOURCE / FIGURE_DIRECTORY
    for relative_target in (
        "figures/r074s/fig-r074s-recurrent-tail-obstruction",
        FIGURE_DIRECTORY,
    ):
        target = ROOT / relative_target
        if target.exists():
            shutil.rmtree(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_figure, target)

    sums = (source_figure / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    for line in sums:
        expected, name = line.split(maxsplit=1)
        name = name.lstrip("* ")
        for base in (
            ROOT / "figures/r074s/fig-r074s-recurrent-tail-obstruction",
            ROOT / FIGURE_DIRECTORY,
        ):
            if sha256(base / name) != expected:
                raise SystemExit(f"figure archive hash drift: {base / name}")

    print(f"R0.74S Step 17 frozen import PASS at {head}")


if __name__ == "__main__":
    main()
