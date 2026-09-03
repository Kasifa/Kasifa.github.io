#!/usr/bin/env python3
"""Import the frozen R0.74S Step 18 package without altering its bytes."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R074S_STEP18_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
CORE_COMMIT = "5a9c172e1db8886d49fdf15b8676b4810b002ae3"
FIGURE_COMMIT = "50c17eedde4774fddb8c9e80ae1df4c04f0509f0"
SEAL_COMMIT = "963613d54303eb240c1daa40c57ffc106a92535b"

FILES = {
    "research/r074s_fixed_deletion_certificate.json": "3594d71f53c60e9e2b03c139ac1be79fba9a93c71f11d2cd73a9c85aa30ebe00",
    "research/r074s_fixed_deletion_certificate_report.md": "9fd733deff824fe856c41879d130d753770b0e88fa1d03f90cac67ed29ef4283",
    "research/r074s_fixed_deletion_independent_audit.md": "93ecdb2457d77fb945abe2bd71891c0d115fcaf2c3c8280ddf790ea4944a9324",
    "research/r074s_fixed_deletion_literature_audit.md": "fea7470814c0c21399c6e2b25961e8b3791e584cc24612ac37e9d1be7ce707ce",
    "research/r074s_fixed_deletion_primary_audit.md": "dd9abf2e818ef096aa7fe9e2218b88c55ffb94fa6882a572f85f0f08ed31bab8",
    "research/r074s_fixed_deletion_qa_report.md": "7c53c59053204d3a3e4fce6184ca94b0f5693e37ccaa3d37647c8f5d0ceb2587",
    "research/r074s_fixed_deletion_simultaneous_height.md": "305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1",
    "scripts/r074s_fixed_deletion_certificate.py": "a2700804af8b292b86596b23cd19ccd2d9f2cdde723c95b1ce6d0bfa0d09f035",
    "scripts/r074s_fixed_deletion_certificate_independent.rb": "f21eb45ef39bc4f10211cc1a5852e8b1d22c671a5eab52377ddf867647b4009f",
    "scripts/r074s_fixed_deletion_qa.sh": "d6985c1dbaf843095478044ebfe38d79a641205b500f0cdc738a12ae97b87e5f",
}

FIGURE_ID = "fig-r074s-fixed-deletion-quantifier-gap"
FIGURE_SOURCE = SOURCE / "research/figures/r074s" / FIGURE_ID


def sha256(file_path: Path) -> str:
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def git(*arguments: str) -> str:
    return subprocess.check_output(["git", *arguments], cwd=SOURCE, text=True).strip()


def main() -> None:
    head = git("rev-parse", "HEAD")
    if head != SEAL_COMMIT:
        raise SystemExit(f"frozen source HEAD drift: {head} != {SEAL_COMMIT}")
    for frozen_commit in (CORE_COMMIT, FIGURE_COMMIT):
        subprocess.check_call(["git", "merge-base", "--is-ancestor", frozen_commit, SEAL_COMMIT], cwd=SOURCE)

    for relative, expected in FILES.items():
        source_file = SOURCE / relative
        if sha256(source_file) != expected:
            raise SystemExit(f"frozen source hash drift: {relative}")
        target_file = ROOT / relative
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)
        if sha256(target_file) != expected:
            raise SystemExit(f"import hash drift: {relative}")

    figure_files = sorted(item.name for item in FIGURE_SOURCE.iterdir() if item.is_file())
    if len(figure_files) != 25:
        raise SystemExit(f"figure inventory drift: {len(figure_files)} != 25")
    for relative_target in (
        f"figures/r074s/{FIGURE_ID}",
        f"research/figures/r074s/{FIGURE_ID}",
    ):
        target_directory = ROOT / relative_target
        if target_directory.exists():
            shutil.rmtree(target_directory)
        target_directory.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(FIGURE_SOURCE, target_directory)

    sums = (FIGURE_SOURCE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    for line in sums:
        expected, name = line.split(maxsplit=1)
        name = name.lstrip("* ")
        for relative_target in (
            f"figures/r074s/{FIGURE_ID}",
            f"research/figures/r074s/{FIGURE_ID}",
        ):
            if sha256(ROOT / relative_target / name) != expected:
                raise SystemExit(f"figure archive hash drift: {relative_target}/{name}")

    print(f"R0.74S Step 18 frozen import PASS at {head}")


if __name__ == "__main__":
    main()
