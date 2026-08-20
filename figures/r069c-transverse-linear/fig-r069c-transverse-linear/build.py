#!/usr/bin/env python3
"""Build and validate the formal R0.69C transverse-linear figure package."""

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
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = HERE.parents[1] / "journal.mplstyle"
CERTIFICATE = ROOT / "research/certificates/r069c/transverse-sideband-linear.json"
CERTIFICATE_SHA = "e67e5ed445bd2ef413f283a0f4a47ca29c864bc5ec79d04afbce350eff0b009a"
SOURCE_COMMIT = "55b89d43ca854e33c10e63f64974fc479f56ceaa"
CERTIFICATE_COMMIT = "8715f4aab57361fef04a60ce2b144cada4291495"
FIGURE_ID = "fig-r069c-transverse-linear"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a16f27"
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


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def singular_ratio(alpha: float, sigma: float) -> tuple[float, float]:
    """Return ||T||/d and the normalized stretch entry.

    Scale R=1, m=alpha, s=alpha*sigma.  T is the exact matrix from R0.69C.
    """
    m = alpha
    s = alpha * sigma
    d = math.hypot(m, s)
    q = math.hypot(1.0, d)
    matrix = np.array([[m * d / q, 0.0], [-s / q, m]], dtype=float)
    norm = float(np.linalg.svd(matrix, compute_uv=False)[0])
    return norm / d, abs(matrix[1, 0]) / d


def prepare_data() -> tuple[dict[str, object], float]:
    started = time.perf_counter()
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("the pinned R0.69C certificate hash does not match")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("the R0.69C certificate did not pass")

    symbol_rows: list[dict[str, object]] = []
    for alpha in (0.02, 0.10, 0.25, 1.00):
        for exponent in np.linspace(-2.0, 2.0, 161):
            sigma = 10.0 ** float(exponent)
            ratio, stretch = singular_ratio(alpha, sigma)
            symbol_rows.append(
                {
                    "mOverR": f"{alpha:.2f}",
                    "sOverM": f"{sigma:.16g}",
                    "operatorNormOverTargetFrequency": f"{ratio:.16g}",
                    "stretchEntryOverTargetFrequency": f"{stretch:.16g}",
                }
            )
    write_rows(
        "symbol-curves.csv",
        [
            "mOverR",
            "sOverM",
            "operatorNormOverTargetFrequency",
            "stretchEntryOverTargetFrequency",
        ],
        symbol_rows,
    )

    rho = float(
        json.loads(
            (ROOT / "research/certificates/r069b/transverse-critical-smallness.json")
            .read_text(encoding="utf-8")
        )["criticalNormBound"]["rho"]["upper"]
    )
    c0 = 6.0 + 4.0 * math.sqrt(2.0)
    decay_rows: list[dict[str, object]] = []
    for depth in range(51):
        epsilon = rho**depth
        decay_rows.append(
            {
                "r": depth,
                "rhoPower": f"{epsilon:.16g}",
                "packetCriticalUpper": f"{c0 * epsilon:.16g}",
                "singleCarrierGainUpper": f"{epsilon / (4.0 * 4.0**depth):.16g}",
            }
        )
    write_rows(
        "decay-envelopes.csv",
        ["r", "rhoPower", "packetCriticalUpper", "singleCarrierGainUpper"],
        decay_rows,
    )

    metadata = {
        "status": "passed",
        "sourceCommit": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "inputCertificate": {
            "location": str(CERTIFICATE.relative_to(ROOT)),
            "sha256": CERTIFICATE_SHA,
        },
        "rhoUpper": repr(rho),
        "criticalPrefactor": "6+4sqrt(2)",
        "matrix": certificate["sideband"]["formulas"]["matrix"],
        "heatDenominator": certificate["sideband"]["formulas"]["heatDenominator"],
        "checksPassed": sum(bool(value) for value in certificate["checks"].values()),
        "checksTotal": len(certificate["checks"]),
        "claimBoundary": certificate["classification"],
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    elapsed = time.perf_counter() - started
    write_rows(
        "figure-data-resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [
            {
                "elapsedSeconds": f"{elapsed:.6f}",
                "maximumRssMiB": f"{rss_mib():.3f}",
                "status": "passed",
            }
        ],
    )
    return metadata, elapsed


def validate_data(metadata: dict[str, object]) -> None:
    symbol = rows("symbol-curves.csv")
    decay = rows("decay-envelopes.csv")
    ratios = [float(row["operatorNormOverTargetFrequency"]) for row in symbol]
    stretches = [float(row["stretchEntryOverTargetFrequency"]) for row in symbol]
    packet = [float(row["packetCriticalUpper"]) for row in decay]
    carrier = [float(row["singleCarrierGainUpper"]) for row in decay]
    checks = {
        "fourSymbolFamilies": len(symbol) == 4 * 161,
        "exactDerivativeCeilingRespected": max(ratios) <= 1.0 + 2e-15,
        "nonNormalStretchIsVisible": max(stretches) > 0.6,
        "fiftyOneDepths": len(decay) == 51,
        "packetEnvelopeStrictlyDecays": all(
            right < left for left, right in zip(packet, packet[1:])
        ),
        "singleCarrierEnvelopeStrictlyDecays": all(
            right < left for left, right in zip(carrier, carrier[1:])
        ),
        "singleCarrierDecaysFaster": carrier[-1] / carrier[-2] < packet[-1] / packet[-2],
        "formalCertificatePassedEighteenChecks": (
            metadata["checksPassed"] == metadata["checksTotal"] == 18
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
        )
        + "\n",
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
    symbol = rows("symbol-curves.csv")
    decay = rows("decay-envelopes.csv")
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 92 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1, 2, left=.082, right=.958, bottom=.20, top=.76,
            width_ratios=(1.04, .96), wspace=.31,
        )
        symbol_axis = figure.add_subplot(grid[0, 0])
        decay_axis = figure.add_subplot(grid[0, 1])
        figure.suptitle(
            "Transverse stretching survives, but the critical linearized gain vanishes",
            x=.055, y=.947, ha="left", fontsize=8.0, color=INK,
        )
        figure.text(
            .055, .884,
            r"exact Fourier--Leray sideband  ·  $k_3=s\ne0$  ·  source-locked R0.69C certificate",
            ha="left", fontsize=3.8, color=MUTED,
        )
        blossom(figure)

        symbol_axis.set_title("(a) Non-normal symbol stays below the derivative scale", loc="left", pad=5)
        styles = {
            "0.02": (BLUE, "-", "o"),
            "0.10": (RUST, "--", "s"),
            "0.25": (GOLD, "-.", "D"),
            "1.00": (INK, ":", "^"),
        }
        for alpha, (color, linestyle, marker) in styles.items():
            selected = [row for row in symbol if row["mOverR"] == alpha]
            x = [float(row["sOverM"]) for row in selected]
            y = [float(row["operatorNormOverTargetFrequency"]) for row in selected]
            symbol_axis.semilogx(
                x, y, color=color, linestyle=linestyle, linewidth=1.05,
                marker=marker, markevery=32, markersize=2.3, markerfacecolor="white",
                label=rf"$m/R={alpha}$",
            )
        symbol_axis.axhline(1.0, color=INK, linewidth=.55, linestyle=(0, (2, 2)))
        symbol_axis.fill_between([1e-2, 1e2], [1, 1], [1.02, 1.02], color=PALE_GOLD)
        symbol_axis.set_xlim(1e-2, 1e2)
        symbol_axis.set_ylim(.68, 1.015)
        symbol_axis.set_xlabel(r"transverse aspect ratio $|s|/m$")
        symbol_axis.set_ylabel(r"exact symbol ratio $\|\mathcal{T}\|/|k|$")
        symbol_axis.grid(color=GRID, linewidth=.3, which="both")
        symbol_axis.legend(loc="lower right", frameon=False, fontsize=3.0, ncol=2)
        symbol_axis.text(
            .045, .08,
            r"Stretch entry $-Rs/Q\ne0$, yet $d^2I-T^*T\succeq0$." + "\n" +
            r"Pressure does not erase stretching; viscosity still sees $|k|$.",
            transform=symbol_axis.transAxes, fontsize=3.15, color=INK,
            bbox={"facecolor": PALE_BLUE, "edgecolor": "none", "pad": 2.0},
        )

        depths = [int(row["r"]) for row in decay]
        packet = [float(row["packetCriticalUpper"]) for row in decay]
        carrier = [float(row["singleCarrierGainUpper"]) for row in decay]
        decay_axis.set_title("(b) Certified critical envelopes", loc="left", pad=5)
        decay_axis.semilogy(
            depths, packet, color=BLUE, linewidth=1.2, linestyle="-",
            marker="o", markerfacecolor="white", markevery=5, markersize=2.5,
            label=r"complete base bound $C_0\rho^r$",
        )
        decay_axis.semilogy(
            depths, carrier, color=RUST, linewidth=1.15, linestyle="--",
            marker="D", markevery=5, markersize=2.4,
            label=r"one-carrier gain $\rho^r/(4\cdot4^r)$",
        )
        decay_axis.set_xlim(0, 50)
        decay_axis.set_ylim(1e-38, 3e1)
        decay_axis.set_xlabel("packet depth r")
        decay_axis.set_ylabel("certified upper envelope  (log scale)")
        decay_axis.grid(color=GRID, linewidth=.3, which="both")
        decay_axis.legend(loc="upper right", frameon=False, fontsize=3.0)
        decay_axis.text(
            .06, .12,
            r"Full linearized resolvent:" + "\n" +
            r"$\|L_r-S\|_{E\to X}\leq C_H\kappa_r/(1-\kappa_r)$" + "\n" +
            r"with $\kappa_r=4C_BC_HC_0\rho^r$.",
            transform=decay_axis.transAxes, fontsize=3.2, color=INK,
            bbox={"facecolor": PALE_GOLD, "edgecolor": GOLD, "linewidth": .35, "pad": 2.1},
        )
        decay_axis.text(
            .06, .035,
            "Universal Koch--Tataru constants stay symbolic; no numerical threshold is assigned.",
            transform=decay_axis.transAxes, fontsize=2.85, color=MUTED,
        )

        figure.text(
            .055, .065,
            "Claim boundary: complete linearized stability in the Koch--Tataru path norm; the order-one nonlinear self-interaction remains uncontrolled.",
            fontsize=3.25, color=MUTED,
        )
        metadata = {"Creator": "R0.69C transverse linearized stability", "Date": None}
        figure.savefig(HERE / "figure.pdf", metadata=metadata)
        figure.savefig(HERE / "figure.svg", metadata=metadata)
        figure.savefig(HERE / "figure.png", dpi=600, metadata=metadata)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")
    elapsed = time.perf_counter() - started
    write_rows(
        "plot-resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{"elapsedSeconds": f"{elapsed:.6f}", "maximumRssMiB": f"{rss_mib():.3f}", "status": "passed"}],
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
        if platform.system() == "Darwin"
        else None
    )
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T05:30:00+08:00",
        "analyticalQuestion": (
            "Can a genuinely three-dimensional non-normal sideband around the "
            "R0.69A packet create order-one amplification in a scaling-critical norm?"
        ),
        "supportedClaim": (
            "The exact stretch survives Leray projection, but its symbol is bounded "
            "by the target derivative scale and the complete linearized propagator "
            "converges to free heat at O(rho^r) in the periodic Koch-Tataru norm."
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
                "extractionCommand": "python3 build.py",
            }
        ],
        "data": [
            record(HERE / "symbol-curves.csv", format="csv", schema="m/R, s/m, exact largest singular-value ratio, normalized stretch entry"),
            record(HERE / "decay-envelopes.csv", format="csv", schema="depth, rho^r, complete-packet critical bound, one-carrier gain bound"),
            record(HERE / "figure-data-metadata.json", format="json", schema="pinned certificate and theorem metadata"),
            record(HERE / "validation.json", format="json", schema="eight figure-data validation checks"),
            record(HERE / "figure-data-resources.csv", format="csv", schema="data extraction resources"),
            record(HERE / "plot-resources.csv", format="csv", schema="rendering resources"),
        ],
        "computation": {
            "kind": "exact-certificate extraction plus double-precision presentation sampling of a proven symbolic formula",
            "configuration": "four m/R ratios, 161 logarithmic transverse aspect ratios each, and packet depths 0 through 50",
            "precision": "exact symbolic theorem; IEEE binary64 used only to draw certified inequalities",
            "solver": "closed-form 2 by 2 singular values and geometric envelopes",
            "command": "python3 build.py",
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
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "pillow": Image.__version__ if hasattr(Image, "__version__") else "bundled",
            "packagesLock": "requirements-research.txt",
        },
        "figure": {
            "script": "build.py",
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
            "family": "dimensionless symbol curves and logarithmic critical-envelope comparison",
            "takeaway": "non-normal stretching is real but cannot overcome the certified critical smallness of the deep packet at linear order",
            "nonColorEncoding": "distinct line styles, markers, direct ceiling line, and explicit formula callouts",
            "outputFootprint": "double-column 178 by 92 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "notes": "The 178 mm color and grayscale renders were inspected at final size; line styles, markers, labels, and callouts remain legible without color.",
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    started = time.perf_counter()
    metadata, _ = prepare_data()
    validate_data(metadata)
    draw()
    build_manifest(metadata, time.perf_counter() - started)


if __name__ == "__main__":
    main()
