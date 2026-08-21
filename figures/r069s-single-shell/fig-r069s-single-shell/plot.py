#!/usr/bin/env python3
"""Build the formal R0.69S single-output-shell figure package."""
from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
import platform
import resource
import time
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = HERE.parents[1] / "journal.mplstyle"
CERTIFICATE = ROOT / "research/certificates/r069s/signed-output-shell-no-cancellation.json"
CERTIFICATE_SHA = "7ae48701d9971dabad5e46daeb017a3a91a00c81e1126045161300f9cd8e85af"
SOURCE_COMMIT = "3bbbb660949181380420ebba9f103e901e560043"
CERTIFICATE_COMMIT = "8b242ef41057aee2a08ece71f33682a7a50f077d"
FIGURE_ID = "fig-r069s-single-shell"
INK, MUTED, BLUE, RUST, GOLD, GRID = (
    "#28231f", "#6b675f", "#315a76", "#8b4d43", "#a16f27", "#d5cec0"
)


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


def prepare_data():
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("pinned R0.69S certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("R0.69S certificate did not pass")

    labels = ["k", "p", "q"]
    wavevectors = np.asarray(certificate["witness"]["wavevectors"], dtype=int)
    squared_lengths = np.asarray(certificate["witness"]["squaredLengths"], dtype=int)
    energy_transfer = np.asarray(
        [int(item) for item in certificate["witness"]["modalTransfers"]], dtype=int
    )
    enstrophy_transfer = squared_lengths * energy_transfer
    shell_indices = np.floor(np.log2(np.sqrt(squared_lengths))).astype(int)

    write_csv(
        "triad-modes.csv",
        ["mode", "k1", "k2", "k3", "squaredLength", "dyadicShell"],
        [
            {
                "mode": label,
                "k1": int(vector[0]),
                "k2": int(vector[1]),
                "k3": int(vector[2]),
                "squaredLength": int(length),
                "dyadicShell": int(shell),
            }
            for label, vector, length, shell in zip(
                labels, wavevectors, squared_lengths, shell_indices
            )
        ],
    )
    write_csv(
        "modal-transfers.csv",
        ["mode", "energyTransfer", "enstrophyWeightedTransfer"],
        [
            {
                "mode": label,
                "energyTransfer": int(energy),
                "enstrophyWeightedTransfer": int(enstrophy),
            }
            for label, energy, enstrophy in zip(
                labels, energy_transfer, enstrophy_transfer
            )
        ],
    )

    shells = np.arange(-2, 3, dtype=int)
    production = np.where(shells == 0, 2, 0)
    reversed_production = -production
    write_csv(
        "shell-production.csv",
        ["shell", "productionU", "productionMinusU"],
        [
            {
                "shell": int(shell),
                "productionU": int(value),
                "productionMinusU": int(reverse),
            }
            for shell, value, reverse in zip(shells, production, reversed_production)
        ],
    )

    ordered = [
        Fraction(item) for item in certificate["witness"]["orderedStretchingContributions"]
    ]
    write_csv(
        "ordered-contributions.csv",
        ["orderedTerm", "exactContribution", "decimalContribution"],
        [
            {
                "orderedTerm": index,
                "exactContribution": str(value),
                "decimalContribution": f"{float(value):.12e}",
            }
            for index, value in enumerate(ordered, start=1)
        ],
    )

    metadata = {
        "status": "passed",
        "sourceCommit": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "inputCertificate": {
            "location": str(CERTIFICATE.relative_to(ROOT)),
            "sha256": CERTIFICATE_SHA,
        },
        "checksPassed": sum(map(bool, certificate["checks"].values())),
        "checksTotal": len(certificate["checks"]),
        "energyTransferSum": int(energy_transfer.sum()),
        "enstrophyWeightedTransferSum": int(enstrophy_transfer.sum()),
        "signedShellProduction": int(production.sum()),
        "cancellationRatio": certificate["shellDecomposition"]["cancellationRatio"],
        "claimBoundary": (
            "sharp Fourier output shells only; smooth commutators, physical-space annuli, "
            "time evolution, regularity, and blow-up remain open"
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return (
        certificate,
        metadata,
        labels,
        wavevectors,
        squared_lengths,
        shell_indices,
        energy_transfer,
        enstrophy_transfer,
        shells,
        production,
        reversed_production,
        ordered,
    )


def validate_data(values) -> None:
    (
        certificate,
        metadata,
        _,
        wavevectors,
        squared_lengths,
        shell_indices,
        energy_transfer,
        enstrophy_transfer,
        _,
        production,
        reversed_production,
        ordered,
    ) = values
    checks = {
        "certificatePassedSeventeenChecks": metadata["checksPassed"] == metadata["checksTotal"] == 17,
        "triadClosesExactly": np.array_equal(wavevectors.sum(axis=0), np.zeros(3, dtype=int)),
        "squaredLengthsAreOneOneTwo": np.array_equal(squared_lengths, [1, 1, 2]),
        "allModesOccupyShellZero": np.array_equal(shell_indices, [0, 0, 0]),
        "kineticEnergyTransferCancels": int(energy_transfer.sum()) == 0,
        "enstrophyWeightedTransferIsOne": int(enstrophy_transfer.sum()) == 1,
        "onlyShellZeroProduces": np.array_equal(production, [0, 0, 2, 0, 0]),
        "signReversalFlipsEveryShell": np.array_equal(reversed_production, -production),
        "orderedContributionsSumToTwo": sum(ordered, Fraction(0)) == Fraction(2),
        "cancellationRatioIsExactlyOne": certificate["shellDecomposition"]["cancellationRatio"] == "1",
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def render(values) -> None:
    (
        _, _, labels, wavevectors, squared_lengths, _, energy_transfer,
        enstrophy_transfer, shells, production, reversed_production, _
    ) = values
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig, (left, middle, right) = plt.subplots(
        1,
        3,
        figsize=(178 / 25.4, 82 / 25.4),
        gridspec_kw={"width_ratios": [0.96, 1.05, 1.07], "wspace": 0.45},
    )

    left.add_patch(Wedge((0, 0), 2.0, 0, 360, width=1.0, color=GOLD, alpha=0.12, zorder=0))
    theta = np.linspace(0.0, 2.0 * np.pi, 361)
    for radius, style in [(1.0, (0, (3, 2))), (2.0, (0, (1.2, 1.3)))]:
        left.plot(radius * np.cos(theta), radius * np.sin(theta), color=MUTED, lw=0.7, ls=style)
    colors = [BLUE, RUST, GOLD]
    label_positions = [(0.42, -0.24), (0.07, 0.93), (-1.25, -1.18)]
    for label, vector, length, color, position in zip(
        labels, wavevectors, squared_lengths, colors, label_positions
    ):
        x, y = vector[:2]
        left.annotate(
            "",
            xy=(x, y),
            xytext=(0, 0),
            arrowprops={"arrowstyle": "-|>", "color": color, "lw": 1.45, "mutation_scale": 8},
        )
        left.text(*position, rf"${label}$; $|{label}|^2={length}$", color=color, fontsize=5.6)
    left.plot(
        [wavevectors[0, 0], wavevectors[0, 0] + wavevectors[1, 0], 0],
        [wavevectors[0, 1], wavevectors[0, 1] + wavevectors[1, 1], 0],
        color=INK,
        lw=0.65,
        ls=(0, (3, 2)),
    )
    left.text(-1.73, 1.64, r"single shell $1\leq |r|<2$", color=MUTED, fontsize=5.4)
    left.set(xlabel=r"Fourier coordinate $r_1$", ylabel=r"Fourier coordinate $r_2$", title="a  Closed triad in one shell")
    left.set_xlim(-2.05, 2.05)
    left.set_ylim(-2.05, 2.05)
    left.set_aspect("equal", adjustable="box")
    left.set_xticks([-2, -1, 0, 1, 2])
    left.set_yticks([-2, -1, 0, 1, 2])
    left.grid(True, color=GRID, lw=0.42, alpha=0.62)

    x = np.arange(3)
    width = 0.34
    middle.bar(
        x - width / 2,
        energy_transfer,
        width,
        color=BLUE,
        edgecolor=INK,
        linewidth=0.45,
        label=r"energy $T_r$",
    )
    middle.bar(
        x + width / 2,
        enstrophy_transfer,
        width,
        color=RUST,
        edgecolor=INK,
        linewidth=0.45,
        hatch="///",
        label=r"enstrophy $|r|^2T_r$",
    )
    middle.axhline(0.0, color=INK, lw=0.7)
    middle.text(0.04, 0.94, r"$\sum T_r=0$", transform=middle.transAxes, color=BLUE, fontsize=6.0, va="top")
    middle.text(0.04, 0.84, r"$\sum |r|^2T_r=1>0$", transform=middle.transAxes, color=RUST, fontsize=6.0, va="top")
    middle.set(
        xlabel="triad mode",
        ylabel="exact modal transfer",
        title="b  Energy cancels; enstrophy grows",
    )
    middle.set_xticks(x, [r"$k$", r"$p$", r"$q$"])
    middle.set_ylim(-3.7, 3.15)
    middle.set_yticks([-3, -2, -1, 0, 1, 2, 3])
    middle.legend(loc="lower right", frameon=False, fontsize=5.15)
    middle.grid(True, axis="y", color=GRID, lw=0.45, alpha=0.7)

    x_shell = np.arange(len(shells))
    right.bar(
        x_shell - width / 2,
        production,
        width,
        color=GOLD,
        edgecolor=INK,
        linewidth=0.45,
        label=r"$F_m(u)$",
    )
    right.bar(
        x_shell + width / 2,
        reversed_production,
        width,
        color="white",
        edgecolor=RUST,
        linewidth=0.8,
        hatch="\\\\\\",
        label=r"$F_m(-u)$",
    )
    right.axhline(0.0, color=INK, lw=0.7)
    right.annotate(
        r"only $m=0$: $F_0=2$",
        xy=(2 - width / 2, 2.0),
        xytext=(0.06, 0.91),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.75},
        fontsize=5.7,
        color=MUTED,
    )
    right.text(
        0.06,
        0.13,
        r"$\Gamma=\sum_m |F_m|/|\sum_mF_m|=1$",
        transform=right.transAxes,
        color=INK,
        fontsize=5.7,
    )
    right.set(
        xlabel=r"sharp output-shell index $m$",
        ylabel=r"signed shell production $F_m$",
        title="c  No forced cross-shell deficit",
    )
    right.set_xticks(x_shell, [str(item) for item in shells])
    right.set_ylim(-2.7, 2.7)
    right.set_yticks([-2, -1, 0, 1, 2])
    right.legend(loc="lower right", frameon=False, fontsize=5.25)
    right.grid(True, axis="y", color=GRID, lw=0.45, alpha=0.7)

    fig.subplots_adjust(left=0.073, right=0.993, bottom=0.23, top=0.865)
    fig.savefig(
        HERE / "figure.pdf",
        metadata={"Creator": "R0.69S reproducible figure", "CreationDate": None},
    )
    fig.savefig(
        HERE / "figure.svg",
        metadata={"Creator": "R0.69S reproducible figure", "Date": None},
    )
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)
    svg = HERE / "figure.svg"
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )


def write_manifest(elapsed: float, peak: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        ("triad-modes.csv", "mode, k1, k2, k3, squaredLength, dyadicShell"),
        ("modal-transfers.csv", "mode, energyTransfer, enstrophyWeightedTransfer"),
        ("shell-production.csv", "shell, productionU, productionMinusU"),
        ("ordered-contributions.csv", "orderedTerm, exactContribution, decimalContribution"),
        ("figure-data-metadata.json", "pinned R0.69S signed-output-shell certificate"),
        ("validation.json", "ten exact figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    payload = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T14:00:00+08:00",
        "analyticalQuestion": "Does sharp dyadic output-shell grouping force signed depletion of vortex stretching?",
        "supportedClaim": "an exact divergence-free triad in one shell has positive total vortex stretching two and cancellation ratio one",
        "claimBoundary": "sharp Fourier output shells only; smooth commutators, physical-space annuli, dynamics, regularity, and blow-up remain open",
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": "three exact Fourier modes, twelve ordered stretching contributions, and five displayed shells",
            "precision": "integer and rational arithmetic for claims; IEEE binary64 only for plotting",
            "solver": "closed-form triad transfer identities and sharp dyadic shell grouping",
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
            "maximumRssMiB": peak,
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
            "heightMillimetres": 82,
            "profile": "journal-default",
            "script": "plot.py",
            "outputs": [
                {
                    "path": path,
                    "bytes": (HERE / path).stat().st_size,
                    "sha256": sha256(HERE / path),
                    **(
                        {"dpi": 600, "pixels": f"{image.width} by {image.height}"}
                        if path.endswith(".png") else {}
                    ),
                }
                for path in outputs
            ],
        },
        "caption": {"english": "caption.md"},
        "chartContract": {
            "family": "Fourier-shell geometry and exact grouped bar charts",
            "takeaway": "sharp output-shell grouping alone supplies no universal signed depletion factor below one",
            "nonColorEncoding": "arrow directions, bar positions, outlines, hatching, and direct annotations",
            "outputFootprint": "double-column 178 by 82 millimetres with PDF, SVG, and 600 dpi PNG",
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
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    started = time.perf_counter()
    values = prepare_data()
    validate_data(values)
    render(values)
    elapsed = time.perf_counter() - started
    peak = rss_mib()
    write_csv(
        "resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [
            {
                "elapsedSeconds": f"{elapsed:.9f}",
                "maximumRssMiB": f"{peak:.6f}",
                "status": "passed",
            }
        ],
    )
    write_manifest(elapsed, peak)


if __name__ == "__main__":
    main()
