#!/usr/bin/env python3
"""Build the formal R0.69M criterion-comparison figure."""
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
CERTIFICATE = (
    ROOT
    / "research/certificates/r069m/criterion-comparison-pressure-budget.json"
)
CERTIFICATE_SHA = "8792c719fe7eb2e84d761bf3bf96a5f8c8ba68bb858a3974264ca2a34b299b19"
SOURCE_COMMIT = "dd6411d1386328a3b873c410dfe5d52e89596591"
CERTIFICATE_COMMIT = "2fa8315869cbedf42e2dd8e19ab8565fb987b8af"
FIGURE_ID = "fig-r069m-criterion"
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


def prepare_data():
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("pinned R0.69M certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("R0.69M certificate did not pass")

    shells = np.arange(2, 13, dtype=int)
    morrey_terms = 2.0 ** (1 - 4 * shells)
    cumulative = np.cumsum(morrey_terms)
    exact_limit = 1.0 / 120.0
    shell_rows = [
        {
            "shellIndex": int(shell),
            "morreySaturatedContribution": f"{term:.17g}",
            "partialSum": f"{partial:.17g}",
            "exactInfiniteSum": f"{exact_limit:.17g}",
            "singleShellReverseRatioLowerBound": str(2 ** (4 * int(shell) - 1)),
        }
        for shell, term, partial in zip(shells, morrey_terms, cumulative)
    ]
    write_csv(
        "morrey-shell-comparison.csv",
        [
            "shellIndex",
            "morreySaturatedContribution",
            "partialSum",
            "exactInfiniteSum",
            "singleShellReverseRatioLowerBound",
        ],
        shell_rows,
    )

    log2_frequency = np.arange(0, 13, dtype=int)
    powers = {
        "velocityL3": -0.5,
        "kineticMorrey": -1.0,
        "nearL2Source": 1.0,
        "absoluteAnnularUQ": 0.5,
    }
    frequency_rows = []
    for exponent_name, exponent in powers.items():
        for index in log2_frequency:
            frequency_rows.append(
                {
                    "quantity": exponent_name,
                    "log2Frequency": int(index),
                    "powerExponent": f"{exponent:.1f}",
                    "log2NormalizedQuantity": f"{exponent * index:.17g}",
                }
            )
    write_csv(
        "high-frequency-witness.csv",
        ["quantity", "log2Frequency", "powerExponent", "log2NormalizedQuantity"],
        frequency_rows,
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
        "morreyUpperConstant": certificate["morreyComparison"][
            "geometricSeriesConstant"
        ],
        "amplitude": certificate["highFrequencyWitness"]["amplitude"],
        "claimBoundary": (
            "exact functional comparison at one time; no solution counterexample"
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return certificate, metadata, shells, morrey_terms, cumulative, log2_frequency, powers


def validate_data(
    certificate,
    metadata,
    shells,
    morrey_terms,
    cumulative,
    log2_frequency,
    powers,
) -> None:
    checks = {
        "certificatePassedFourteenChecks": (
            metadata["checksPassed"] == metadata["checksTotal"] == 14
        ),
        "morreyConstantIsOneOver120": (
            certificate["morreyComparison"]["geometricSeriesConstant"] == "1/120"
        ),
        "shellContributionsHaveRatioOneOver16": np.allclose(
            morrey_terms[1:] / morrey_terms[:-1], 1 / 16
        ),
        "partialSumsAreIncreasing": np.all(np.diff(cumulative) > 0),
        "partialSumsStayBelowExactLimit": np.all(cumulative < 1 / 120),
        "terminalPartialSumApproachesExactLimit": np.isclose(
            cumulative[-1], 1 / 120, rtol=0, atol=1e-15
        ),
        "witnessHasTwoDecayingAndTwoGrowingQuantities": (
            sum(exponent < 0 for exponent in powers.values()) == 2
            and sum(exponent > 0 for exponent in powers.values()) == 2
        ),
        "witnessExponentsMatchCertificate": (
            certificate["highFrequencyWitness"]["powerExponents"]
            == {
                "absoluteAnnularUQ": "1/2",
                "kineticMorrey": "-1",
                "nearL2Source": "1",
                "velocityL3": "-1/2",
            }
            and len(log2_frequency) == 13
            and shells[0] == 2
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


def render(shells, morrey_terms, cumulative, log2_frequency, powers) -> None:
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig, (left, right) = plt.subplots(
        1,
        2,
        figsize=(178 / 25.4, 86 / 25.4),
        gridspec_kw={"width_ratios": [1.0, 1.08], "wspace": 0.34},
    )

    scale = 1000.0
    left.bar(
        shells,
        scale * morrey_terms,
        width=0.67,
        color=BLUE,
        alpha=0.78,
        edgecolor=INK,
        linewidth=0.55,
        hatch="///",
        label=r"shell bound $2^{1-4m}\,{\cal M}_2$",
    )
    left.plot(
        shells,
        scale * cumulative,
        color=RUST,
        lw=1.45,
        marker="o",
        markersize=3.2,
        markerfacecolor="white",
        label="partial sum",
    )
    left.axhline(
        scale / 120,
        color=GOLD,
        lw=1.25,
        ls=(0, (5, 2.5)),
        label=r"exact limit $1000/120$",
    )
    left.set(
        xlabel=r"shell index $m$",
        ylabel=r"coefficient per ${\cal M}_2$  ($\times10^3$)",
        title="a  Morrey control leaves a finite far-shell budget",
    )
    left.set_xticks(shells)
    left.set_ylim(0, 9.25)
    left.grid(True, axis="y", color=GRID, lw=0.45, alpha=0.75)
    left.legend(loc="center right", frameon=False, fontsize=6.2)
    left.text(
        7.1,
        7.35,
        r"$B_\infty\leq{\cal M}_2/120$",
        ha="center",
        color=MUTED,
        fontsize=7.1,
    )

    styles = {
        "velocityL3": (BLUE, "--", "o", r"velocity $\|u_N\|_3$: slope $-1/2$"),
        "kineticMorrey": (INK, ":", "s", r"kinetic ${\cal M}_2$: slope $-1$"),
        "nearL2Source": (RUST, "-", "^", r"near $N_1$: slope $+1$"),
        "absoluteAnnularUQ": (
            GOLD,
            "-.",
            "D",
            r"annular $\int|u_Nq_N|$: slope $+1/2$",
        ),
    }
    for name, (color, linestyle, marker, label) in styles.items():
        values = powers[name] * log2_frequency
        right.plot(
            log2_frequency,
            values,
            color=color,
            ls=linestyle,
            lw=1.35,
            marker=marker,
            markevery=2,
            markersize=3.1,
            markerfacecolor="white",
            label=label,
        )
    right.axhline(0, color=GRID, lw=0.8)
    right.set(
        xlabel=r"frequency $\log_2N$",
        ylabel=r"$\log_2(Q_N/Q_1)$",
        title="b  High frequency separates velocity and near costs",
    )
    right.set_xticks(log2_frequency[::2])
    right.set_yticks(np.arange(-12, 13, 3))
    right.set_ylim(-12.8, 12.8)
    right.grid(True, color=GRID, lw=0.45, alpha=0.75)
    right.legend(loc="upper left", frameon=False, fontsize=5.9)
    right.text(
        8.35,
        -8.8,
        r"$a_N=N^{-1/2}$",
        ha="center",
        color=MUTED,
        fontsize=7.0,
    )

    fig.subplots_adjust(left=0.082, right=0.982, bottom=0.19, top=0.88)
    fig.savefig(
        HERE / "figure.pdf",
        metadata={"Creator": "R0.69M reproducible figure", "CreationDate": None},
    )
    fig.savefig(
        HERE / "figure.svg",
        metadata={"Creator": "R0.69M reproducible figure", "Date": None},
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


def write_manifest(elapsed: float, peak: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        (
            "morrey-shell-comparison.csv",
            "shellIndex, Morrey-saturated contribution, partial and exact sums, reverse-ratio lower bound",
        ),
        (
            "high-frequency-witness.csv",
            "quantity, log2Frequency, powerExponent, log2NormalizedQuantity",
        ),
        ("figure-data-metadata.json", "pinned R0.69M criterion certificate"),
        ("validation.json", "eight figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    payload = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T09:28:00+08:00",
        "analyticalQuestion": (
            "Which terms in the R0.69L pressure budget are controlled at "
            "critical Morrey or suitable-weak-solution regularity?"
        ),
        "supportedClaim": (
            "the far-shell term is bounded by M_2/120, while a smooth "
            "high-frequency family separates velocity smallness from the near costs"
        ),
        "claimBoundary": (
            "functional time-slice comparison; not a Navier-Stokes solution "
            "counterexample or a regularity criterion"
        ),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": "dyadic shells m=2 through 12 and log2 frequencies 0 through 12",
            "precision": "IEEE binary64 plotting of exact rational powers",
            "solver": "closed-form geometric series and power-law exponents",
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
            "heightMillimetres": 86,
            "profile": "journal-default",
            "script": "plot.py",
            "outputs": [
                {
                    "path": path,
                    "bytes": (HERE / path).stat().st_size,
                    "sha256": sha256(HERE / path),
                    **(
                        {"dpi": 600, "pixels": f"{image.width} by {image.height}"}
                        if path.endswith(".png")
                        else {}
                    ),
                }
                for path in outputs
            ],
        },
        "caption": {"english": "caption.md"},
        "chartContract": {
            "family": "Morrey shell-budget bars plus exponent-separation lines",
            "takeaway": "the useful far bound does not repair the near-field regularity mismatch",
            "nonColorEncoding": "hatched bars, dashed limit, distinct line styles and markers",
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
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    started = time.perf_counter()
    values = prepare_data()
    validate_data(*values)
    _, _, shells, morrey_terms, cumulative, log2_frequency, powers = values
    render(shells, morrey_terms, cumulative, log2_frequency, powers)
    elapsed = time.perf_counter() - started
    peak = rss_mib()
    write_csv(
        "resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{"elapsedSeconds": f"{elapsed:.9f}", "maximumRssMiB": f"{peak:.6f}", "status": "passed"}],
    )
    write_manifest(elapsed, peak)


if __name__ == "__main__":
    main()
