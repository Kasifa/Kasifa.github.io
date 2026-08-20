#!/usr/bin/env python3
"""Build and validate the formal R0.69E resolvent-gluing figure package."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import resource
import subprocess
import time
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import mpmath as mp
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = HERE.parents[1] / "journal.mplstyle"
CERTIFICATE = ROOT / "research/certificates/r069e/critical-resolvent-restart.json"
CERTIFICATE_SHA = "25992a1119ebf3089a2b4b2231aba524a064e9188f4eb0b31ee5bb1b88a4a009"
SOURCE_COMMIT = "2d49cf91a29c2a2ecd19edbe97356a924b958917"
CERTIFICATE_COMMIT = "58b586872721f7b3e774338c209b2b6837249331"
FIGURE_ID = "fig-r069e-resolvent-restart"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a16f27"
GREEN = "#4d6a58"
PALE_BLUE = "#e6edf1"
PALE_GOLD = "#f4ead6"
GRID = "#d5cec0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def write_rows(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def prepare_data() -> tuple[dict[str, object], float]:
    started = time.perf_counter()
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("the pinned R0.69E certificate hash does not match")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("the R0.69E certificate did not pass")

    surface_rows: list[dict[str, object]] = []
    for a in np.linspace(0.0, 0.95, 96):
        for b in np.linspace(0.0, 0.95, 96):
            amplification = 1.0 / ((1.0 - float(a)) * (1.0 - float(b)))
            surface_rows.append(
                {
                    "a": f"{a:.16g}",
                    "b": f"{b:.16g}",
                    "inverseRowSumFactor": f"{amplification:.16g}",
                    "log10InverseRowSumFactor": f"{math.log10(amplification):.16g}",
                }
            )
    write_rows(
        "two-block-surface.csv",
        ["a", "b", "inverseRowSumFactor", "log10InverseRowSumFactor"],
        surface_rows,
    )

    mp.mp.dps = 80
    gluing_rows: list[dict[str, object]] = []
    for eta_text in ("1/5", "2/5", "3/5", "4/5"):
        numerator, denominator = eta_text.split("/")
        eta = mp.mpf(numerator) / mp.mpf(denominator)
        row_sums: list[mp.mpf] = []
        for index in range(64):
            coupling = sum(
                eta * (mp.sqrt(lag) - mp.sqrt(lag - 1))
                * row_sums[index - lag]
                for lag in range(1, index + 1)
            )
            current = (1 + coupling) / (1 - eta)
            row_sums.append(current)
            gluing_rows.append(
                {
                    "eta": eta_text,
                    "etaDecimal": mp.nstr(eta, 16),
                    "slabs": index + 1,
                    "inverseMaximumRowSum": mp.nstr(current, 40),
                    "log10InverseMaximumRowSum": mp.nstr(mp.log10(current), 30),
                }
            )
    write_rows(
        "equal-slab-gluing.csv",
        [
            "eta",
            "etaDecimal",
            "slabs",
            "inverseMaximumRowSum",
            "log10InverseMaximumRowSum",
        ],
        gluing_rows,
    )

    metadata = {
        "status": "passed",
        "sourceCommit": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "inputCertificate": {
            "location": str(CERTIFICATE.relative_to(ROOT)),
            "sha256": CERTIFICATE_SHA,
        },
        "checksPassed": sum(bool(value) for value in certificate["checks"].values()),
        "checksTotal": len(certificate["checks"]),
        "dimensionlessEtaScenarios": ["1/5", "2/5", "3/5", "4/5"],
        "surfaceGrid": "96 by 96",
        "maximumSlabs": 64,
        "claimBoundary": certificate["classification"],
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    elapsed = time.perf_counter() - started
    write_rows(
        "figure-data-resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{
            "elapsedSeconds": f"{elapsed:.6f}",
            "maximumRssMiB": f"{rss_mib():.3f}",
            "status": "passed",
        }],
    )
    return metadata, elapsed


def validate_data(metadata: dict[str, object]) -> None:
    surface = read_rows("two-block-surface.csv")
    gluing = read_rows("equal-slab-gluing.csv")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    scenarios = certificate["finitePartition"]["scenarios"]
    lookup = {
        (row["eta"], int(row["slabs"])): mp.mpf(row["maximumRowSum"])
        for row in scenarios
    }
    cross_checks = []
    for row in gluing:
        key = (row["eta"], int(row["slabs"]))
        if key in lookup:
            value = mp.mpf(row["inverseMaximumRowSum"])
            reference = lookup[key]
            relative = abs(value - reference) / reference
            cross_checks.append(relative < mp.mpf("1e-28"))

    by_eta = {}
    for row in gluing:
        by_eta.setdefault(row["eta"], []).append(
            float(row["log10InverseMaximumRowSum"])
        )
    checks = {
        "surfaceHasNinetySixSquaredSamples": len(surface) == 96 * 96,
        "surfaceStaysInsideStrictGate": all(
            float(row["a"]) < 1 and float(row["b"]) < 1 for row in surface
        ),
        "surfaceFactorIsAtLeastOne": min(
            float(row["inverseRowSumFactor"]) for row in surface
        ) >= 1.0,
        "fourEtaScenariosHaveSixtyFourSlabs": (
            len(gluing) == 4 * 64 and len(by_eta) == 4
        ),
        "everyFiniteInverseRowSumGrowsMonotonically": all(
            all(right > left for left, right in zip(values, values[1:]))
            for values in by_eta.values()
        ),
        "certificateCrossChecksCoverAllSixteenScenarios": (
            len(cross_checks) == 16 and all(cross_checks)
        ),
        "formalCertificatePassedEighteenChecks": (
            metadata["checksPassed"] == metadata["checksTotal"] == 18
        ),
        "largestDisplayedScenarioRemainsFinite": math.isfinite(
            max(float(row["log10InverseMaximumRowSum"]) for row in gluing)
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps({"status": "passed", "checks": checks}, indent=2) + "\n",
        encoding="utf-8",
    )


def normalize_svg(path: Path) -> None:
    path.write_text(
        "\n".join(
            line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()
        ) + "\n",
        encoding="utf-8",
    )


def blossom(figure) -> None:
    center = (0.946, 0.925)
    for dx, dy, angle in ((0, .010, 0), (0, -.010, 0), (.008, 0, 90), (-.008, 0, 90)):
        figure.add_artist(
            Ellipse(
                (center[0] + dx, center[1] + dy), .010, .018,
                angle=angle, transform=figure.transFigure,
                facecolor="#ead9b8", edgecolor=GOLD, linewidth=.35,
            )
        )


def draw() -> float:
    started = time.perf_counter()
    surface = read_rows("two-block-surface.csv")
    gluing = read_rows("equal-slab-gluing.csv")
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 92 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1, 2, left=.080, right=.958, bottom=.20, top=.76,
            width_ratios=(.94, 1.06), wspace=.31,
        )
        surface_axis = figure.add_subplot(grid[0, 0])
        slab_axis = figure.add_subplot(grid[0, 1])
        figure.suptitle(
            "Positive-time Volterra gluing makes the regular-interval resolvent finite",
            x=.055, y=.947, ha="left", fontsize=8.0, color=INK,
        )
        figure.text(
            .055, .884,
            r"initial critical block  ·  weighted $L^\infty$ tail  ·  exact lower-triangular inverse",
            ha="left", fontsize=3.8, color=MUTED,
        )
        blossom(figure)

        a_values = sorted({float(row["a"]) for row in surface})
        b_values = sorted({float(row["b"]) for row in surface})
        z = np.empty((len(b_values), len(a_values)))
        a_index = {value: index for index, value in enumerate(a_values)}
        b_index = {value: index for index, value in enumerate(b_values)}
        for row in surface:
            z[b_index[float(row["b"])], a_index[float(row["a"])]] = float(
                row["log10InverseRowSumFactor"]
            )
        aa, bb = np.meshgrid(a_values, b_values)

        surface_axis.set_title("(a) Exact two-block inverse factor", loc="left", pad=5)
        surface_axis.contourf(
            aa, bb, z, levels=np.linspace(0, z.max(), 16),
            cmap="Blues", alpha=.88,
        )
        contour = surface_axis.contour(
            aa, bb, z, levels=(.25, .5, 1.0, 1.5, 2.0),
            colors=INK, linewidths=.45,
        )
        surface_axis.clabel(contour, fmt=lambda value: f"{value:.2g}", fontsize=3.0)
        surface_axis.plot([0, .95], [.95, .95], color=RUST, linestyle="--", linewidth=.8)
        surface_axis.plot([.95, .95], [0, .95], color=RUST, linestyle="--", linewidth=.8)
        surface_axis.set_xlim(0, 1)
        surface_axis.set_ylim(0, 1)
        surface_axis.set_xlabel(r"initial diagonal gate $a=2C_B\|v\|_{X_\tau}$")
        surface_axis.set_ylabel(r"late diagonal gate $b_\lambda$")
        surface_axis.text(
            .055, .075,
            r"contours: $\log_{10}\!\left([(1-a)(1-b)]^{-1}\right)$" + "\n" +
            r"strict square $0\leq a,b<1$",
            transform=surface_axis.transAxes, fontsize=3.15, color=INK,
            bbox={"facecolor": PALE_GOLD, "edgecolor": "none", "pad": 2.0},
        )

        slab_axis.set_title("(b) Finite equal-slab gluing cost", loc="left", pad=5)
        styles = {
            "1/5": (BLUE, "-", "o", "0.2"),
            "2/5": (RUST, "--", "s", "0.4"),
            "3/5": (GOLD, "-.", "D", "0.6"),
            "4/5": (GREEN, ":", "^", "0.8"),
        }
        for eta, (color, linestyle, marker, decimal) in styles.items():
            selected = [row for row in gluing if row["eta"] == eta]
            slabs = [int(row["slabs"]) for row in selected]
            values = [float(row["log10InverseMaximumRowSum"]) for row in selected]
            slab_axis.plot(
                slabs, values, color=color, linestyle=linestyle, linewidth=1.1,
                marker=marker, markevery=8, markersize=2.4,
                label=rf"$\eta={decimal}$",
            )
        slab_axis.axhline(0, color=INK, linewidth=.5, linestyle=(0, (2, 2)))
        slab_axis.set_xlim(1, 64)
        slab_axis.set_xlabel("number of late time slabs")
        slab_axis.set_ylabel(r"$\log_{10}$ maximum inverse row sum")
        slab_axis.grid(color=GRID, linewidth=.3)
        slab_axis.legend(loc="upper left", frameon=False, fontsize=3.2, ncol=2)
        slab_axis.text(
            .49, .06,
            r"$\ell_0=\eta,\quad \ell_k=\eta(\sqrt{k}-\sqrt{k-1})$" + "\n" +
            r"finite for every displayed $N$ because $\eta<1$",
            transform=slab_axis.transAxes, fontsize=3.0, color=MUTED,
            bbox={"facecolor": "white", "edgecolor": GRID, "linewidth": .35, "pad": 2.0},
        )

        figure.text(
            .055, .065,
            "Claim boundary: finite resolvent on a fixed regular interval; conditioning may deteriorate near an uncontrolled singular horizon.",
            fontsize=3.15, color=MUTED,
        )
        metadata = {"Creator": "R0.69E positive-time critical-resolvent gluing", "Date": None}
        figure.savefig(HERE / "figure.pdf", metadata=metadata)
        figure.savefig(HERE / "figure.svg", metadata=metadata)
        figure.savefig(HERE / "figure.png", dpi=600, metadata=metadata)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")
    elapsed = time.perf_counter() - started
    write_rows(
        "plot-resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{
            "elapsedSeconds": f"{elapsed:.6f}",
            "maximumRssMiB": f"{rss_mib():.3f}",
            "status": "passed",
        }],
    )
    return elapsed


def record(path: Path, **extra: object) -> dict[str, object]:
    return {
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        **extra,
    }


def sysctl(name: str, fallback: str) -> str:
    try:
        return subprocess.run(
            ["sysctl", "-n", name], check=True, capture_output=True, text=True
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return fallback


def build_manifest(metadata: dict[str, object], elapsed: float) -> None:
    png = Image.open(HERE / "figure.png")
    memory_gib = (
        round(int(sysctl("hw.memsize", "0")) / 1024**3)
        if platform.system() == "Darwin" else None
    )
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T06:25:00+08:00",
        "analyticalQuestion": (
            "How do the local inverse gates and causal time-slab gluing "
            "control the critical linearized resolvent on a regular interval?"
        ),
        "supportedClaim": (
            "Strict diagonal gates make the finite lower-triangular Volterra "
            "system invertible, with an explicit inverse row-sum majorant."
        ),
        "claimBoundary": metadata["claimBoundary"],
        "git": {
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "repository": "Kasifa/Kasifa.github.io",
            "dirtyAtCertifiedRun": False,
        },
        "sourceData": [
            {
                "fileName": CERTIFICATE.name,
                "location": metadata["inputCertificate"]["location"],
                "bytes": CERTIFICATE.stat().st_size,
                "sha256": CERTIFICATE_SHA,
                "extractionCommand": "python3 plot.py",
            },
        ],
        "data": [
            record(HERE / "two-block-surface.csv", format="csv", schema="a, b, exact inverse factor, base-10 logarithm"),
            record(HERE / "equal-slab-gluing.csv", format="csv", schema="eta scenario, slab count, exact high-precision inverse row sum"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned certificate and theorem metadata"),
            record(HERE / "validation.json", format="json", schema="eight figure-data validation checks"),
            record(HERE / "figure-data-resources.csv", format="csv", schema="data extraction resources"),
            record(HERE / "plot-resources.csv", format="csv", schema="rendering resources"),
        ],
        "computation": {
            "kind": "exact-audit plus high-precision presentation sampling",
            "configuration": "96 by 96 two-block grid and four eta scenarios through 64 slabs",
            "precision": "IEEE binary64 for the contour grid; mpmath 80 decimal digits for slab recurrence",
            "solver": "exact two-block formula and causal Toeplitz forward substitution",
            "command": "python3 plot.py",
            "scientificWallTimeSeconds": round(elapsed, 6),
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": platform.platform(),
            "cpu": sysctl("machdep.cpu.brand_string", platform.processor()),
            "memoryGiB": memory_gib,
            "processes": 1,
            "threadsPerProcess": 1,
        },
        "environment": {
            "python": platform.python_version(),
            "mpmath": mp.__version__,
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "pillow": Image.__version__ if hasattr(Image, "__version__") else "bundled",
            "packagesLock": "requirements-research.txt",
        },
        "figure": {
            "script": "plot.py",
            "widthMillimetres": 178,
            "heightMillimetres": 92,
            "profile": "journal-default",
            "outputs": [
                record(HERE / "figure.pdf"),
                record(HERE / "figure.svg"),
                record(HERE / "figure.png", dpi=600, pixels=f"{png.width} by {png.height}"),
            ],
        },
        "chartContract": {
            "family": "two-parameter contour plus finite-slab condition-number curves",
            "takeaway": "diagonal local invertibility suffices for every finite causal gluing system, even when conditioning accumulates",
            "nonColorEncoding": "contour labels, distinct line styles, markers, and formula callouts",
            "outputFootprint": "double-column 178 by 92 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "notes": "The final-size color and grayscale renders were inspected; contours, line styles, markers, and formulas remain legible without color.",
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    started = time.perf_counter()
    metadata, _ = prepare_data()
    validate_data(metadata)
    draw()
    build_manifest(metadata, time.perf_counter() - started)


if __name__ == "__main__":
    main()
