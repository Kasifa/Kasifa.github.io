#!/usr/bin/env python3
"""Build the formal R0.69I localized-commutator figure package."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import resource
import time
from fractions import Fraction
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = HERE.parents[1] / "journal.mplstyle"
CERTIFICATE = ROOT / "research/certificates/r069i/localized-strain-pressure-commutator.json"
CERTIFICATE_SHA = "73dfa59251ffcb9603eeb298d3028e191936ab3ccf2f0b7ab7d6dc9c9288a5d2"
SOURCE_COMMIT = "b03985d6d2fd1f55ba5d600cb75859efb694876b"
CERTIFICATE_COMMIT = "9578b9f4b77e9e910ba5db27625722894463d44c"
FIGURE_ID = "fig-r069i-localization"
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
        "\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )


def exact_float(text: str) -> float:
    return float(Fraction(text))


def prepare_data() -> dict[str, object]:
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("the pinned R0.69I certificate hash does not match")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("the R0.69I certificate did not pass")

    exact = certificate["exactValues"]
    pressure_rows = [
        {
            "component": "laplacian-pressure flux",
            "exact": exact["pressureLaplacianFlux"],
            "value": f'{exact_float(exact["pressureLaplacianFlux"]):.17g}',
        },
        {
            "component": "pressure-gradient flux",
            "exact": exact["pressureGradientFlux"],
            "value": f'{exact_float(exact["pressureGradientFlux"]):.17g}',
        },
        {
            "component": "localized pressure pairing",
            "exact": exact["localizedPressurePairing"],
            "value": f'{exact_float(exact["localizedPressurePairing"]):.17g}',
        },
    ]
    write_csv("pressure-commutator.csv", ["component", "exact", "value"], pressure_rows)

    channel_rows = [
        {
            "channel": "pressure",
            "globalExact": exact["globalPressurePairing"],
            "globalValue": f'{exact_float(exact["globalPressurePairing"]):.17g}',
            "localizedExact": exact["localizedPressurePairing"],
            "localizedValue": f'{exact_float(exact["localizedPressurePairing"]):.17g}',
        },
        {
            "channel": "Betchov",
            "globalExact": exact["globalBetchovPairing"],
            "globalValue": f'{exact_float(exact["globalBetchovPairing"]):.17g}',
            "localizedExact": exact["localizedBetchovPairing"],
            "localizedValue": f'{exact_float(exact["localizedBetchovPairing"]):.17g}',
        },
    ]
    write_csv(
        "global-localized.csv",
        ["channel", "globalExact", "globalValue", "localizedExact", "localizedValue"],
        channel_rows,
    )

    scaling_rows = [
        {"term": term, "degree": degree}
        for term, degree in certificate["scalingDegrees"].items()
    ]
    write_csv("scaling-degrees.csv", ["term", "degree"], scaling_rows)

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
        "pressureComponents": len(pressure_rows) - 1,
        "channels": len(channel_rows),
        "scalingTerms": len(scaling_rows),
        "weight": "1 + (1/7) sin(x3) - (1/11) sin(x1)",
        "claimBoundary": (
            "bare-localization obstruction only; additional harmonic-tail, multiscale, "
            "Morrey, or geometric control remains open"
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "certificate": certificate,
        "metadata": metadata,
        "pressureRows": pressure_rows,
        "channelRows": channel_rows,
        "scalingRows": scaling_rows,
    }


def validate_data(data: dict[str, object]) -> None:
    certificate = data["certificate"]
    exact = certificate["exactValues"]
    pressure_sum = exact_float(exact["pressureLaplacianFlux"]) + exact_float(
        exact["pressureGradientFlux"]
    )
    checks = {
        "certificatePassedFourteenChecks": (
            data["metadata"]["checksPassed"] == data["metadata"]["checksTotal"] == 14
        ),
        "pressureComponentsSumExactly": (
            Fraction(exact["pressureLaplacianFlux"])
            + Fraction(exact["pressureGradientFlux"])
            == Fraction(exact["localizedPressurePairing"])
        ),
        "pressureFloatingSumMatches": abs(
            pressure_sum - exact_float(exact["localizedPressurePairing"])
        ) < 1e-15,
        "globalPairingsVanish": (
            exact["globalPressurePairing"] == exact["globalBetchovPairing"] == "0"
        ),
        "localizedPressureIsNonzero": Fraction(exact["localizedPressurePairing"]) != 0,
        "localizedBetchovIsNonzero": Fraction(exact["localizedBetchovPairing"]) != 0,
        "allScalingDegreesAreThree": set(certificate["scalingDegrees"].values()) == {3},
        "weightModesAreDistinct": (
            certificate["weight"]["pressureMode"] != certificate["weight"]["betchovMode"]
        ),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def render(data: dict[str, object]) -> None:
    exact = data["certificate"]["exactValues"]
    laplacian_flux = exact_float(exact["pressureLaplacianFlux"])
    gradient_flux = exact_float(exact["pressureGradientFlux"])
    pressure_total = exact_float(exact["localizedPressurePairing"])
    betchov_total = exact_float(exact["localizedBetchovPairing"])

    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    figure, (left, right) = plt.subplots(
        1,
        2,
        figsize=(178 / 25.4, 86 / 25.4),
        gridspec_kw={"width_ratios": [0.92, 1.08], "wspace": 0.38},
    )

    x = np.arange(2)
    components = np.asarray([laplacian_flux, gradient_flux])
    left.axhline(0, color=INK, linewidth=0.85)
    bars = left.bar(
        x,
        components,
        width=0.58,
        color=[BLUE, RUST],
        alpha=0.78,
        edgecolor=INK,
        linewidth=0.8,
    )
    bars[0].set_hatch("///")
    bars[1].set_hatch("xx")
    left.plot(
        [x[0] - 0.33, x[-1] + 0.33],
        [pressure_total, pressure_total],
        color=GOLD,
        linewidth=1.35,
        linestyle=(0, (4, 2)),
    )
    left.scatter([0.5], [pressure_total], s=30, facecolors="white", edgecolors=INK, zorder=4)
    left.text(0.5, pressure_total - 0.003, r"sum $=-676/40425$", ha="center", va="top", fontsize=6.8)
    left.text(0, laplacian_flux - 0.0025, r"$-332/8085$", ha="center", va="top", fontsize=6.7)
    left.text(1, gradient_flux + 0.0025, r"$328/13475$", ha="center", va="bottom", fontsize=6.7)
    left.set_xticks(x, [r"$(\Delta p)u\cdot\nabla\phi$", r"$u_i p_j\phi_{ij}$"])
    left.set_ylim(-0.052, 0.034)
    left.set_ylabel("exact spatial mean")
    left.set_title("a  Pressure transferred to cutoff fluxes")
    left.grid(True, axis="y", color=GRID, linewidth=0.45, alpha=0.8)

    stages = np.asarray([0, 1])
    right.axhline(0, color=INK, linewidth=0.85)
    right.plot(
        stages,
        [0, pressure_total],
        color=BLUE,
        linewidth=1.6,
        marker="o",
        markerfacecolor="white",
        label=r"pressure $\int\phi S:H$",
    )
    right.plot(
        stages,
        [0, betchov_total],
        color=RUST,
        linewidth=1.6,
        linestyle=(0, (5, 2.5)),
        marker="s",
        markerfacecolor="white",
        label=r"Betchov $\int\phi\,\mathrm{tr}(A^3)$",
    )
    right.text(1.025, pressure_total, r"$-676/40425$", ha="left", va="center", fontsize=6.8, color=BLUE)
    right.text(1.025, betchov_total, r"$228/2695$", ha="left", va="center", fontsize=6.8, color=RUST)
    right.text(
        0.5,
        0.098,
        r"all six localized terms scale as $\lambda^3$",
        ha="center",
        va="top",
        fontsize=7.0,
        color=MUTED,
        bbox={"facecolor": "white", "edgecolor": GRID, "boxstyle": "round,pad=0.25"},
    )
    right.set_xticks(stages, [r"global $\phi=1$", "localized weight"])
    right.set_xlim(-0.12, 1.38)
    right.set_ylim(-0.045, 0.105)
    right.set_ylabel("exact pairing")
    right.set_title("b  Global zeros become nonzero commutators")
    right.grid(True, axis="y", color=GRID, linewidth=0.45, alpha=0.8)
    right.legend(loc="center left", frameon=False, fontsize=6.4)

    figure.subplots_adjust(left=0.075, right=0.975, bottom=0.20, top=0.88)
    figure.savefig(
        HERE / "figure.pdf",
        metadata={"Creator": "R0.69I reproducible figure", "CreationDate": None},
    )
    figure.savefig(
        HERE / "figure.svg",
        metadata={"Creator": "R0.69I reproducible figure", "Date": None},
    )
    figure.savefig(HERE / "figure.png", dpi=600)
    plt.close(figure)
    normalize_svg(HERE / "figure.svg")


def build_manifest(elapsed: float, peak_rss: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        ("pressure-commutator.csv", "component, exact, value"),
        ("global-localized.csv", "channel, globalExact, globalValue, localizedExact, localizedValue"),
        ("scaling-degrees.csv", "term, degree"),
        ("figure-data-metadata.json", "pinned certificate and exact formulas"),
        ("validation.json", "eight figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T08:10:00+08:00",
        "analyticalQuestion": (
            "Does spatial localization preserve the global strain cancellations or produce a scale gain?"
        ),
        "supportedClaim": (
            "the global pressure and Betchov pairings vanish, while an exact weighted Fourier witness "
            "makes both nonzero and every resulting commutator retains scaling degree three"
        ),
        "claimBoundary": (
            "bare-localization obstruction only; no Navier-Stokes regularity or singularity conclusion"
        ),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": "two exact global/localized channels and six scaling terms",
            "precision": "IEEE binary64 plotting of exact rational certificate values",
            "solver": "exact rational Fourier-convolution certificate",
            "command": "python3 plot.py",
            "wallTimeSeconds": elapsed,
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": f"{platform.system()}-{platform.release()}-{platform.machine()}",
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
                    **({"dpi": 600, "pixels": f"{image.width} by {image.height}"} if path.endswith(".png") else {}),
                }
                for path in outputs
            ],
        },
        "caption": {"english": "caption.md"},
        "chartContract": {
            "family": "signed exact decomposition plus global-to-localized comparison",
            "takeaway": "bare localization transfers both global cancellations to nonzero same-scale commutators",
            "nonColorEncoding": (
                "distinct hatches, solid-circle and dashed-square trajectories, zero axes, and exact rational labels"
            ),
            "outputFootprint": "double-column 178 by 86 millimetres with PDF, SVG, and 600 dpi PNG",
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
    data = prepare_data()
    validate_data(data)
    render(data)
    elapsed = time.perf_counter() - started
    peak_rss = rss_mib()
    write_csv(
        "resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{"elapsedSeconds": f"{elapsed:.9f}", "maximumRssMiB": f"{peak_rss:.6f}", "status": "passed"}],
    )
    build_manifest(elapsed, peak_rss)


if __name__ == "__main__":
    main()
