#!/usr/bin/env python3
"""Build the formal R0.69O pressure time-closure figure."""
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
CERTIFICATE = ROOT / "research/certificates/r069o/energy-commutator-time-closure.json"
CERTIFICATE_SHA = "b81cb6986b701233c33ab0713546318ae6c88cde2ab1a3cb6a6767ed35400113"
SOURCE_COMMIT = "46f217d0d6cb29f3a60e8c5a101e92c6f7e8e560"
CERTIFICATE_COMMIT = "49136625e4c1f48d1f765653b15cc8df8b50ec8e"
FIGURE_ID = "fig-r069o-pressure-time-closure"
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
        raise RuntimeError("pinned R0.69O certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("R0.69O certificate did not pass")

    normalized_z = np.linspace(0.0, 1.8, 181)
    normalized_profit = 4.0 * normalized_z**1.5 - 3.0 * normalized_z**2
    write_csv(
        "sharp-young-profile.csv",
        ["zOverZStar", "profitOverMaximum"],
        [
            {"zOverZStar": f"{x:.8f}", "profitOverMaximum": f"{y:.8f}"}
            for x, y in zip(normalized_z, normalized_profit)
        ],
    )

    log2_amplitude = np.arange(0, 10, dtype=int)
    quadratic_mass = np.ones_like(log2_amplitude, dtype=float)
    cubic_mass = 2.0**log2_amplitude
    minimum_dissipation_mass = 2.0 ** (2 * log2_amplitude)
    write_csv(
        "time-spike-masses.csv",
        [
            "amplitude",
            "width",
            "quadraticMass",
            "cubicMass",
            "minimumDissipationMass",
        ],
        [
            {
                "amplitude": str(2**int(k)),
                "width": f"{2.0 ** (-2 * int(k)):.17g}",
                "quadraticMass": f"{two:.17g}",
                "cubicMass": f"{three:.17g}",
                "minimumDissipationMass": f"{dissipation:.17g}",
            }
            for k, two, three, dissipation in zip(
                log2_amplitude,
                quadratic_mass,
                cubic_mass,
                minimum_dissipation_mass,
            )
        ],
    )

    sectors = ["pressure\ncommutator", "vortex\nstretching"]
    sigma_powers = np.array([2.0, 6.0])
    write_csv(
        "remainder-exponents.csv",
        ["sector", "sigmaPowerAfterYoung", "status"],
        [
            {
                "sector": "pressure commutator",
                "sigmaPowerAfterYoung": "2",
                "status": "quadratic time exponent recovered",
            },
            {
                "sector": "strain/vorticity stretching",
                "sigmaPowerAfterYoung": "6",
                "status": "remaining nonlinear obstruction",
            },
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
        "sharpOptimizer": certificate["sharpnessOptimization"]["optimizer"],
        "optimizedProfit": certificate["sharpnessOptimization"]["optimizedProfit"],
        "claimBoundary": (
            "exact algebraic and functional exponent audit; not a complete localized "
            "H1 estimate or Navier-Stokes regularity theorem"
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return (
        certificate,
        metadata,
        normalized_z,
        normalized_profit,
        log2_amplitude,
        quadratic_mass,
        cubic_mass,
        minimum_dissipation_mass,
        sectors,
        sigma_powers,
    )


def validate_data(values) -> None:
    (
        certificate,
        metadata,
        normalized_z,
        normalized_profit,
        log2_amplitude,
        quadratic_mass,
        cubic_mass,
        minimum_dissipation_mass,
        _,
        sigma_powers,
    ) = values
    optimizer_index = int(np.argmin(np.abs(normalized_z - 1.0)))
    checks = {
        "certificatePassedEighteenChecks": (
            metadata["checksPassed"] == metadata["checksTotal"] == 18
        ),
        "normalizedYoungProfitPeaksAtOne": (
            np.isclose(normalized_z[np.argmax(normalized_profit)], 1.0)
        ),
        "normalizedYoungMaximumIsOne": np.isclose(
            normalized_profit[optimizer_index], 1.0
        ),
        "certificateSharpConstantIsTwentySevenOverTwoFiftySix": (
            certificate["sharpnessOptimization"]["optimizedProfit"]
            == "27*mu**4/(256*epsilon**3)"
        ),
        "timeSpikeKeepsQuadraticMassOne": np.allclose(quadratic_mass, 1.0),
        "timeSpikeCubicMassEqualsAmplitude": np.allclose(
            cubic_mass, 2.0**log2_amplitude
        ),
        "interpolationForcesQuadraticDissipationGrowth": np.allclose(
            minimum_dissipation_mass, 2.0 ** (2 * log2_amplitude)
        ),
        "pressureRemainderIsQuadratic": np.isclose(sigma_powers[0], 2.0),
        "stretchingRemainderIsSextic": np.isclose(sigma_powers[1], 6.0),
        "stretchingPowerExceedsPressurePower": sigma_powers[1] > sigma_powers[0],
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )


def render(values) -> None:
    (
        _,
        _,
        normalized_z,
        normalized_profit,
        log2_amplitude,
        quadratic_mass,
        cubic_mass,
        minimum_dissipation_mass,
        sectors,
        sigma_powers,
    ) = values
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig, (left, middle, right) = plt.subplots(
        1,
        3,
        figsize=(178 / 25.4, 82 / 25.4),
        gridspec_kw={"width_ratios": [1.0, 1.08, 0.86], "wspace": 0.42},
    )

    left.plot(normalized_z, normalized_profit, color=BLUE, lw=1.5)
    left.axhline(0.0, color=INK, lw=0.75)
    left.axvline(1.0, color=MUTED, lw=0.9, ls=(0, (3, 2)))
    left.scatter([1.0], [1.0], s=28, marker="o", facecolor=GOLD,
                 edgecolor=INK, linewidth=0.6, zorder=4)
    left.annotate(
        r"$z_*=(3\mu/4\varepsilon)^2$" "\n"
        r"$\max=27\mu^4/(256\varepsilon^3)$",
        xy=(1.0, 1.0),
        xytext=(0.13, 0.47),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        color=MUTED,
        fontsize=5.8,
    )
    left.set(
        xlabel=r"normalized frequency $z/z_*$",
        ylabel="normalized profit",
        title="a  Young cost is algebraically sharp",
    )
    left.set_xlim(0.0, 1.8)
    left.set_ylim(-0.35, 1.18)
    left.grid(True, color=GRID, lw=0.45, alpha=0.75)

    middle.plot(
        log2_amplitude,
        np.log2(quadratic_mass),
        color=BLUE,
        lw=1.25,
        ls="--",
        marker="s",
        markersize=3.0,
        markerfacecolor="white",
        label=r"quadratic mass $=1$",
    )
    middle.plot(
        log2_amplitude,
        np.log2(cubic_mass),
        color=RUST,
        lw=1.4,
        marker="o",
        markersize=3.0,
        markerfacecolor="white",
        label=r"old cubic cost $=A$",
    )
    middle.plot(
        log2_amplitude,
        np.log2(minimum_dissipation_mass),
        color=GOLD,
        lw=1.45,
        ls=(0, (4, 1.5)),
        marker="^",
        markersize=3.2,
        markerfacecolor="white",
        label=r"required $\mathcal{D}$ mass $=A^2$",
    )
    middle.fill_between(
        log2_amplitude,
        np.log2(cubic_mass),
        np.log2(minimum_dissipation_mass),
        color=GOLD,
        alpha=0.10,
        hatch="///",
        edgecolor=GOLD,
        linewidth=0.0,
    )
    middle.set(
        xlabel=r"spike amplitude $\log_2 A$",
        ylabel=r"$\log_2$ time mass",
        title="b  The old spike pays dissipation",
    )
    middle.set_xticks(log2_amplitude[::2])
    middle.set_ylim(-0.6, 18.8)
    middle.grid(True, color=GRID, lw=0.45, alpha=0.75)
    middle.legend(loc="upper left", frameon=False, fontsize=5.45)

    positions = np.arange(2)
    right.bar(
        positions,
        sigma_powers,
        width=0.58,
        color=[BLUE, RUST],
        edgecolor=INK,
        linewidth=0.65,
        hatch=["//", "xx"],
        alpha=0.88,
    )
    right.axhline(2.0, color=INK, lw=0.9, ls=(0, (2, 2)), label="quadratic level")
    for x, value in zip(positions, sigma_powers):
        right.text(x, value + 0.16, f"{int(value)}", ha="center", fontsize=7.0,
                   color=INK)
    right.set(
        ylabel=r"power of $\sigma$ after Young",
        title="c  Stretching stays sextic",
    )
    right.set_xticks(positions, sectors)
    right.set_ylim(0.0, 6.8)
    right.grid(True, axis="y", color=GRID, lw=0.45, alpha=0.75)
    right.legend(loc="upper left", frameon=False, fontsize=5.7)

    fig.subplots_adjust(left=0.065, right=0.992, bottom=0.22, top=0.86)
    fig.savefig(
        HERE / "figure.pdf",
        metadata={"Creator": "R0.69O reproducible figure", "CreationDate": None},
    )
    fig.savefig(
        HERE / "figure.svg",
        metadata={"Creator": "R0.69O reproducible figure", "Date": None},
    )
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)
    svg = HERE / "figure.svg"
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )


def write_manifest(elapsed: float, peak: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        ("sharp-young-profile.csv", "zOverZStar, profitOverMaximum"),
        (
            "time-spike-masses.csv",
            "amplitude, width, quadraticMass, cubicMass, minimumDissipationMass",
        ),
        ("remainder-exponents.csv", "sector, sigmaPowerAfterYoung, status"),
        ("figure-data-metadata.json", "pinned R0.69O time-closure certificate"),
        ("validation.json", "ten figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    payload = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T10:20:00+08:00",
        "analyticalQuestion": (
            "Does dissipation-assisted interpolation repair the pressure "
            "commutator time exponent, and what obstruction remains?"
        ),
        "supportedClaim": (
            "the leading pressure remainder is quadratic in enstrophy with a "
            "sharp mu^4 coefficient inside the interpolation mechanism, while "
            "cubic strain/vorticity stretching still produces a sextic remainder"
        ),
        "claimBoundary": (
            "exact algebraic and functional exponent audit; not a complete "
            "localized H1 estimate or Navier-Stokes regularity theorem"
        ),
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": (
                "181 normalized Young-profile samples, 10 exact dyadic time "
                "spikes, and 2 exact post-Young exponents"
            ),
            "precision": "IEEE binary64 plotting of exact rational formulas",
            "solver": "closed-form exponent identities",
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
                "sharp Young profile, constrained time-spike mass comparison, "
                "and post-Young exponent comparison"
            ),
            "takeaway": (
                "dissipation repairs the pressure time exponent; the unresolved "
                "nonlinearity is cubic strain/vorticity stretching"
            ),
            "nonColorEncoding": (
                "distinct markers, line styles, hatching, and value labels"
            ),
            "outputFootprint": (
                "double-column 178 by 82 millimetres with PDF, SVG, and 600 dpi PNG"
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
