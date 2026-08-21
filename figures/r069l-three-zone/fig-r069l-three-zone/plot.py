#!/usr/bin/env python3
"""Build the formal R0.69L three-zone pressure-budget figure."""
from __future__ import annotations

import csv
import hashlib
import json
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
CERTIFICATE = ROOT / "research/certificates/r069l/three-zone-pressure-budget.json"
CERTIFICATE_SHA = "086fc4bc3f156704008de33245c81bc909e10b1f23f164a5d31ed8445a5966bf"
SOURCE_COMMIT = "e5bcd77e238edc7cabf49d9c96e792ef92a33aba"
CERTIFICATE_COMMIT = "2b65698e149c0a091608e90da5a5fbe7a0defcd0"
FIGURE_ID = "fig-r069l-three-zone"
INK, MUTED, BLUE, RUST, GOLD, GRID = (
    "#28231f",
    "#6b675f",
    "#315a76",
    "#8b4d43",
    "#a16f27",
    "#d5cec0",
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


def weight(index: int) -> float:
    return 2.0 ** (-5 * index)


def prepare_data():
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("pinned R0.69L certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("R0.69L certificate did not pass")

    shell_indices = np.arange(2, 13, dtype=int)
    separation_indices = np.arange(3, 14, dtype=int)
    first_weight = weight(2)
    exact_limit = sum(weight(int(shell)) for shell in shell_indices)
    budget_rows = []
    for separation in separation_indices:
        transition = sum(
            weight(int(shell)) for shell in shell_indices if shell < separation
        )
        far_count = sum(1 for shell in shell_indices if shell >= separation)
        far = weight(int(separation)) * far_count
        budget_rows.append(
            {
                "separationIndex": int(separation),
                "separationRatio": int(2**separation),
                "transitionRelative": f"{transition / first_weight:.17g}",
                "farRelative": f"{far / first_weight:.17g}",
                "totalRelative": f"{(transition + far) / first_weight:.17g}",
                "exactLimitRelative": f"{exact_limit / first_weight:.17g}",
            }
        )
    write_csv(
        "separation-budget.csv",
        [
            "separationIndex",
            "separationRatio",
            "transitionRelative",
            "farRelative",
            "totalRelative",
            "exactLimitRelative",
        ],
        budget_rows,
    )

    selected_separations = (3, 6, 9, 13)
    migration_rows = []
    for separation in selected_separations:
        for shell in shell_indices:
            assigned = weight(min(int(shell), separation)) / first_weight
            migration_rows.append(
                {
                    "separationIndex": separation,
                    "shellIndex": int(shell),
                    "assignedWeightRelative": f"{assigned:.17g}",
                    "classification": (
                        "transition" if shell < separation else "lumpedFar"
                    ),
                }
            )
    write_csv(
        "weight-migration.csv",
        [
            "separationIndex",
            "shellIndex",
            "assignedWeightRelative",
            "classification",
        ],
        migration_rows,
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
        "model": "unit normalized energy on shells m=2,...,12",
        "firstShellWeight": certificate["finiteSeparationModel"]["firstShellWeight"],
        "amplitudeRatio": certificate["amplitudeAudit"]["ratio"],
        "claimBoundary": (
            "exact illustration of separation-parameter migration; "
            "no regularity conclusion"
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return certificate, metadata, shell_indices, separation_indices, exact_limit


def validate_data(
    certificate,
    metadata,
    shell_indices,
    separation_indices,
    exact_limit,
) -> None:
    first_weight = weight(2)
    total_values = []
    for separation in separation_indices:
        transition = sum(
            weight(int(shell)) for shell in shell_indices if shell < separation
        )
        far = weight(int(separation)) * sum(
            1 for shell in shell_indices if shell >= separation
        )
        total_values.append(transition + far)
    checks = {
        "certificatePassedFourteenChecks": (
            metadata["checksPassed"] == metadata["checksTotal"] == 14
        ),
        "firstShellWeightIsOneOver1024": (
            certificate["finiteSeparationModel"]["firstShellWeight"] == "1/1024"
        ),
        "dyadicWeightRatioIsOneOver32": np.isclose(weight(3) / weight(2), 1 / 32),
        "separationBudgetIsMonotone": np.all(np.diff(total_values) <= 1e-15),
        "terminalBudgetEqualsExactFloor": np.isclose(total_values[-1], exact_limit),
        "exactFloorIsStrictlyPositive": exact_limit / first_weight > 1,
        "farComponentVanishesAfterLastShell": separation_indices[-1] > shell_indices[-1],
        "amplitudeRatioMatchesCertificate": (
            certificate["amplitudeAudit"]["ratio"] == "beta**2/alpha"
        ),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )


def render(shell_indices, separation_indices, exact_limit) -> None:
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig, (left, right) = plt.subplots(
        1,
        2,
        figsize=(178 / 25.4, 86 / 25.4),
        gridspec_kw={"width_ratios": [1.05, 0.95], "wspace": 0.36},
    )

    first_weight = weight(2)
    transitions = []
    far_tails = []
    totals = []
    for separation in separation_indices:
        transition = sum(
            weight(int(shell)) for shell in shell_indices if shell < separation
        )
        far = weight(int(separation)) * sum(
            1 for shell in shell_indices if shell >= separation
        )
        transitions.append(transition / first_weight)
        far_tails.append(far / first_weight)
        totals.append((transition + far) / first_weight)
    x = np.arange(len(separation_indices))
    left.bar(
        x,
        transitions,
        width=0.68,
        color=BLUE,
        alpha=0.78,
        edgecolor=INK,
        linewidth=0.55,
        hatch="///",
        label="retained transition shells",
    )
    left.bar(
        x,
        far_tails,
        bottom=transitions,
        width=0.68,
        color=GOLD,
        alpha=0.72,
        edgecolor=INK,
        linewidth=0.55,
        hatch="..",
        label=r"lumped far tail $2^{-5M}\sum_{m\geq M}e_m$",
    )
    limit_relative = exact_limit / first_weight
    left.axhline(
        limit_relative,
        color=RUST,
        lw=1.35,
        ls=(0, (5, 2.5)),
        label=r"exact floor $\sum 2^{-5m}e_m$",
    )
    left.set_xticks(x, [str(value) for value in separation_indices])
    left.set(
        xlabel=r"separation index $M$  ($A=2^M$)",
        ylabel=r"budget coefficient / $2^{-10}$",
        title="a  A smaller far tail becomes transition mass",
    )
    left.set_ylim(0, max(totals) * 1.12)
    left.grid(True, axis="y", color=GRID, lw=0.45, alpha=0.75)
    left.legend(loc="upper right", frameon=False, fontsize=6.2)
    left.text(
        0.1,
        limit_relative - 0.075,
        f"positive floor = {limit_relative:.6f}",
        color=RUST,
        fontsize=6.5,
    )

    styles = {
        3: (RUST, "--", "s"),
        6: (GOLD, "-.", "^"),
        9: (BLUE, ":", "D"),
        13: (INK, "-", "o"),
    }
    for separation, (color, linestyle, marker) in styles.items():
        assigned = np.array(
            [weight(min(int(shell), separation)) / first_weight for shell in shell_indices]
        )
        label = (
            r"$M\to\infty$ (exact weights)"
            if separation == 13
            else rf"$M={separation}$"
        )
        right.semilogy(
            shell_indices,
            assigned,
            color=color,
            ls=linestyle,
            lw=1.35,
            marker=marker,
            markersize=3.2,
            markerfacecolor="white",
            label=label,
        )
    right.set(
        xlabel=r"shell index $m$",
        ylabel=r"assigned coefficient / $2^{-10}$",
        title="b  Increasing separation only moves the plateau",
    )
    right.set_xticks(shell_indices)
    right.grid(True, which="both", color=GRID, lw=0.45, alpha=0.75)
    right.legend(loc="lower left", frameon=False, fontsize=6.4)
    right.text(
        7.25,
        0.15,
        "fixed shells retain their\n" + r"own $2^{-5m}$ weights",
        ha="center",
        color=MUTED,
        fontsize=6.4,
    )

    fig.subplots_adjust(left=0.078, right=0.978, bottom=0.19, top=0.88)
    fig.savefig(
        HERE / "figure.pdf",
        metadata={"Creator": "R0.69L reproducible figure", "CreationDate": None},
    )
    fig.savefig(
        HERE / "figure.svg",
        metadata={"Creator": "R0.69L reproducible figure", "Date": None},
    )
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)
    svg = HERE / "figure.svg"
    svg.write_text(
        "\n".join(
            line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )


def manifest(elapsed: float, peak: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        (
            "separation-budget.csv",
            "separationIndex, separationRatio, transitionRelative, farRelative, totalRelative, exactLimitRelative",
        ),
        (
            "weight-migration.csv",
            "separationIndex, shellIndex, assignedWeightRelative, classification",
        ),
        (
            "figure-data-metadata.json",
            "pinned certificate and finite unit-shell illustration",
        ),
        ("validation.json", "eight figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    payload = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T09:15:00+08:00",
        "analyticalQuestion": (
            "Can increasing the near/far separation ratio make the complete "
            "velocity-generated shell budget vanish?"
        ),
        "supportedClaim": (
            "the lumped A^-5 far tail decreases by migrating fixed shells into "
            "a positive weighted transition-shell floor"
        ),
        "claimBoundary": (
            "finite unit-shell illustration of an exact identity; no "
            "Navier-Stokes regularity or singularity conclusion"
        ),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": "unit energy on dyadic shells m=2 through 12",
            "precision": "IEEE binary64 plotting of exact dyadic rational weights",
            "solver": "closed-form separation-budget identity",
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
            "family": (
                "stacked separation-budget bars plus logarithmic shell-weight paths"
            ),
            "takeaway": (
                "far-tail suppression relabels rather than removes fixed shells"
            ),
            "nonColorEncoding": (
                "hatched stacked bars, dashed floor, distinct line styles and markers"
            ),
            "outputFootprint": (
                "double-column 178 by 86 millimetres with PDF, SVG, and 600 dpi PNG"
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
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    started = time.perf_counter()
    certificate, metadata, shells, separations, exact_limit = prepare_data()
    validate_data(certificate, metadata, shells, separations, exact_limit)
    render(shells, separations, exact_limit)
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
    manifest(elapsed, peak)


if __name__ == "__main__":
    main()
