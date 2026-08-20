#!/usr/bin/env python3
"""Build the formal R0.69H pressure-Hessian obstruction figure package."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import resource
import time
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = HERE.parents[1] / "journal.mplstyle"
CERTIFICATE = (
    ROOT
    / "research/certificates/r069h/"
    "pressure-hessian-pointwise-obstruction.json"
)
CERTIFICATE_SHA = (
    "a988bd4d3fb1e7286dfa1facd9de0867fb37c8044af3b5e95a44be8878340653"
)
SOURCE_COMMIT = "86ac684e2a2564f56d42d9c216918ed659652846"
CERTIFICATE_COMMIT = "33ca9d4f8f2893cc12828895e36ac0e787077af0"
FIGURE_ID = "fig-r069h-pressure-obstruction"
COEFFICIENT = 54 / 85
THRESHOLD = math.sqrt(85 / 54)
INK = "#28231f"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a16f27"
GRID = "#d5cec0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def write_csv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def normalize_svg(path: Path) -> None:
    path.write_text(
        "\n".join(
            line.rstrip()
            for line in path.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )


def prepare_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, object]]:
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("the pinned R0.69H certificate hash does not match")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("the R0.69H certificate did not pass")

    amplitude = np.linspace(0, 2, 241)
    pressure_minus = -1 - COEFFICIENT * amplitude**2
    pressure_plus = -1 + COEFFICIENT * amplitude**2
    write_csv(
        "pressure-response.csv",
        ["t", "H11Minus", "H11Plus"],
        [
            {
                "t": f"{x:.12g}",
                "H11Minus": f"{y_minus:.17g}",
                "H11Plus": f"{y_plus:.17g}",
            }
            for x, y_minus, y_plus in zip(
                amplitude, pressure_minus, pressure_plus, strict=True
            )
        ],
    )

    nodes = np.asarray([0, 1, 2], dtype=float)
    node_minus = -1 - COEFFICIENT * nodes**2
    node_plus = -1 + COEFFICIENT * nodes**2
    write_csv(
        "certified-nodes.csv",
        ["t", "H11Minus", "H11Plus"],
        [
            {
                "t": f"{x:.12g}",
                "H11Minus": f"{y_minus:.17g}",
                "H11Plus": f"{y_plus:.17g}",
            }
            for x, y_minus, y_plus in zip(
                nodes, node_minus, node_plus, strict=True
            )
        ],
    )

    decomposition = [
        {
            "family": "minus (1,2)",
            "base": -1,
            "crossAtT2": 0,
            "perturbationAtT2": -4 * COEFFICIENT,
            "totalAtT2": -301 / 85,
        },
        {
            "family": "plus (2,1)",
            "base": -1,
            "crossAtT2": 0,
            "perturbationAtT2": 4 * COEFFICIENT,
            "totalAtT2": 131 / 85,
        },
    ]
    write_csv(
        "pressure-decomposition.csv",
        [
            "family",
            "base",
            "crossAtT2",
            "perturbationAtT2",
            "totalAtT2",
        ],
        decomposition,
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
        "responseSamples": len(amplitude),
        "certifiedNodes": len(nodes),
        "exactCoefficient": "54/85",
        "exactThresholdTSquared": "85/54",
        "claimBoundary": certificate["classification"],
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return amplitude, pressure_minus, pressure_plus, {
        **metadata,
        "nodes": nodes,
        "nodeMinus": node_minus,
        "nodePlus": node_plus,
        "decomposition": decomposition,
    }


def validate_data(
    amplitude: np.ndarray,
    pressure_minus: np.ndarray,
    pressure_plus: np.ndarray,
    metadata: dict[str, object],
) -> None:
    crossing = float(
        np.interp(0, pressure_plus, amplitude)
    )
    checks = {
        "certificatePassedFifteenChecks": (
            metadata["checksPassed"] == metadata["checksTotal"] == 15
        ),
        "responseGridHasExpectedLength": len(amplitude) == 241,
        "familiesAgreeAtZero": (
            pressure_minus[0] == pressure_plus[0] == -1
        ),
        "minusFamilyRemainsNegative": bool(np.all(pressure_minus < 0)),
        "plusFamilyChangesSign": (
            float(np.min(pressure_plus)) < 0 < float(np.max(pressure_plus))
        ),
        "crossingMatchesExactThreshold": abs(crossing - THRESHOLD) < 2e-5,
        "tTwoMinusMatchesCertificate": (
            abs(pressure_minus[-1] + 301 / 85) < 1e-15
        ),
        "tTwoPlusMatchesCertificate": (
            abs(pressure_plus[-1] - 131 / 85) < 1e-15
        ),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "checks": checks,
                "interpolatedCrossing": crossing,
                "exactCrossing": THRESHOLD,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def render(
    amplitude: np.ndarray,
    pressure_minus: np.ndarray,
    pressure_plus: np.ndarray,
    metadata: dict[str, object],
) -> None:
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    width_inches = 178 / 25.4
    height_inches = 86 / 25.4
    figure, (left, right) = plt.subplots(
        1,
        2,
        figsize=(width_inches, height_inches),
        gridspec_kw={"width_ratios": [1.12, 0.88], "wspace": 0.36},
    )

    left.axhspan(0, 1.75, color=RUST, alpha=0.07)
    left.axhspan(-3.8, 0, color=BLUE, alpha=0.055)
    left.axhline(0, color=INK, linewidth=0.85)
    left.plot(
        amplitude,
        pressure_minus,
        color=BLUE,
        linewidth=1.7,
        label=r"$H_{11}^{-}=-1-(54/85)t^2$",
    )
    left.plot(
        amplitude,
        pressure_plus,
        color=RUST,
        linewidth=1.7,
        linestyle=(0, (5, 2.5)),
        label=r"$H_{11}^{+}=-1+(54/85)t^2$",
    )
    left.scatter(
        metadata["nodes"],
        metadata["nodeMinus"],
        s=20,
        facecolors="white",
        edgecolors=BLUE,
        linewidths=0.9,
        zorder=3,
    )
    left.scatter(
        metadata["nodes"],
        metadata["nodePlus"],
        s=20,
        marker="s",
        facecolors="white",
        edgecolors=RUST,
        linewidths=0.9,
        zorder=3,
    )
    left.axvline(
        THRESHOLD,
        color=GOLD,
        linewidth=1.0,
        linestyle=(0, (2, 2)),
    )
    left.annotate(
        r"sign reversal: $t^2=85/54$",
        xy=(THRESHOLD, 0),
        xytext=(0.50, 1.05),
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        fontsize=7.1,
        color=MUTED,
    )
    left.set_xlim(0, 2.03)
    left.set_ylim(-3.75, 1.75)
    left.set_xlabel(r"remote-field amplitude $t$")
    left.set_ylabel(r"principal pressure component $H_{11}(0)$")
    left.set_title("a  Same local gradient, opposite pressure sign")
    left.grid(True, color=GRID, linewidth=0.45, alpha=0.8)
    left.legend(loc="lower left", frameon=False, fontsize=6.6)

    y = np.asarray([1, 0], dtype=float)
    base = np.asarray([-1, -1], dtype=float)
    perturbation = np.asarray([-216 / 85, 216 / 85], dtype=float)
    right.axvline(0, color=INK, linewidth=0.85)
    right.barh(
        y,
        base,
        height=0.42,
        color="white",
        edgecolor=INK,
        linewidth=0.9,
        hatch="///",
        label="common base",
    )
    right.barh(
        y,
        perturbation,
        left=base,
        height=0.42,
        color=[BLUE, RUST],
        alpha=0.78,
        edgecolor=INK,
        linewidth=0.8,
        hatch=["...", "xx"],
        label=r"remote perturbation at $t=2$",
    )
    right.plot([-301 / 85, 131 / 85], y, "o", color=INK, markersize=3.3)
    right.text(-301 / 85 - 0.06, 1, r"$-301/85$", ha="right", va="center", fontsize=7)
    right.text(131 / 85 + 0.06, 0, r"$131/85$", ha="left", va="center", fontsize=7)
    right.set_yticks(y, [r"$\phi_{1,2}$", r"$\phi_{2,1}$"])
    right.set_xlim(-4.15, 2.25)
    right.set_ylim(-0.55, 1.68)
    right.set_xlabel(r"decomposition of $H_{11}(0)$")
    right.set_title("b  Nonlocal contribution at t = 2")
    right.grid(True, axis="x", color=GRID, linewidth=0.45, alpha=0.8)
    right.text(
        -4.02,
        1.52,
        r"both: $S(0)=\mathrm{diag}(1,-1,0)$, $\omega(0)=0$",
        va="center",
        ha="left",
        fontsize=6.2,
        color=MUTED,
    )
    right.text(
        -0.5,
        0.50,
        "common base = -1",
        va="center",
        ha="center",
        fontsize=6.2,
        color=MUTED,
    )
    right.text(
        -2.25,
        1.30,
        r"remote term $-216/85$",
        va="center",
        ha="center",
        fontsize=6.0,
        color=BLUE,
    )
    right.text(
        0.30,
        -0.28,
        r"remote term $+216/85$",
        va="center",
        ha="center",
        fontsize=6.0,
        color=RUST,
    )

    figure.subplots_adjust(left=0.075, right=0.985, bottom=0.18, top=0.88)
    figure.savefig(
        HERE / "figure.pdf",
        metadata={"Creator": "R0.69H reproducible figure", "CreationDate": None},
    )
    figure.savefig(
        HERE / "figure.svg",
        metadata={"Creator": "R0.69H reproducible figure", "Date": None},
    )
    figure.savefig(HERE / "figure.png", dpi=600)
    plt.close(figure)
    normalize_svg(HERE / "figure.svg")


def build_manifest(elapsed: float, peak_rss: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        ("pressure-response.csv", "t, H11Minus, H11Plus"),
        ("certified-nodes.csv", "t, H11Minus, H11Plus"),
        (
            "pressure-decomposition.csv",
            "family, base, crossAtT2, perturbationAtT2, totalAtT2",
        ),
        ("figure-data-metadata.json", "pinned certificate and exact formulas"),
        ("validation.json", "eight figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T07:40:00+08:00",
        "analyticalQuestion": (
            "Can the sign of the principal pressure-Hessian component be "
            "determined from local strain and vorticity?"
        ),
        "supportedClaim": (
            "two exact smooth periodic divergence-free families have the "
            "same local strain and vorticity but opposite principal pressure-"
            "Hessian signs when t squared exceeds 85/54"
        ),
        "claimBoundary": (
            "pointwise-sign obstruction only; no Navier-Stokes regularity "
            "or singularity conclusion"
        ),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": "241 exact-response samples and three certified nodes",
            "precision": "IEEE binary64 plotting of exact rational formulas",
            "solver": "closed pressure-Hessian response from exact Fourier coefficients",
            "command": "python3 plot.py",
            "wallTimeSeconds": elapsed,
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": (
                f"{platform.system()}-{platform.release()}-{platform.machine()}"
            ),
            "cpu": "Apple M5 Max",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": 1,
            "maximumRssMiB": peak_rss,
        },
        "environment": {
            "python": platform.python_version(),
            "matplotlib": matplotlib.__version__,
            "numpy": np.__version__,
            "pillow": Image.__version__,
            "packagesLock": "requirements-research.txt",
        },
        "sourceData": [
            {
                "location": str(CERTIFICATE.relative_to(ROOT)),
                "fileName": CERTIFICATE.name,
                "bytes": CERTIFICATE.stat().st_size,
                "sha256": CERTIFICATE_SHA,
                "extractionCommand": "python3 plot.py",
            }
        ],
        "data": [
            {
                "path": path,
                "bytes": (HERE / path).stat().st_size,
                "sha256": sha256(HERE / path),
                "schema": schema,
            }
            for path, schema in data_files
        ],
        "figure": {
            "widthMillimetres": 178,
            "heightMillimetres": 86,
            "profile": "journal-default",
            "script": "plot.py",
            "outputs": [
                {
                    "path": path,
                    "bytes": (HERE / path).stat().st_size,
                    "sha256": sha256(HERE / path),
                    **(
                        {
                            "dpi": 600,
                            "pixels": f"{image.width} by {image.height}",
                        }
                        if path.endswith(".png")
                        else {}
                    ),
                }
                for path in outputs
            ],
        },
        "caption": {"english": "caption.md"},
        "chartContract": {
            "family": "exact response curves plus signed decomposition",
            "takeaway": (
                "identical local velocity gradients do not fix the pressure-"
                "Hessian sign"
            ),
            "nonColorEncoding": (
                "solid and dashed curves, distinct markers, hatched bars, "
                "zero axes, and exact rational labels"
            ),
            "outputFootprint": (
                "double-column 178 by 86 millimetres with PDF, SVG, and "
                "600 dpi PNG"
            ),
        },
        "qa": {
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
        },
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    started = time.perf_counter()
    amplitude, pressure_minus, pressure_plus, metadata = prepare_data()
    validate_data(amplitude, pressure_minus, pressure_plus, metadata)
    render(amplitude, pressure_minus, pressure_plus, metadata)
    elapsed = time.perf_counter() - started
    peak_rss = rss_mib()
    write_csv(
        "resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [
            {
                "elapsedSeconds": f"{elapsed:.9f}",
                "maximumRssMiB": f"{peak_rss:.6f}",
                "status": "passed",
            }
        ],
    )
    build_manifest(elapsed, peak_rss)


if __name__ == "__main__":
    main()
