#!/usr/bin/env python3
"""Build and validate the formal R0.69F endpoint-scaling figure package."""

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
CERTIFICATE = (
    ROOT
    / "research/certificates/r069f/"
    "critical-resolvent-endpoint-scaling.json"
)
CERTIFICATE_SHA = (
    "96e66ff755aa0cc57379ac6582b72c149f7bf290ce44a3de8a9777162dfcc9e3"
)
SOURCE_COMMIT = "c3f3d94620f6852e48e07525cc81f2c94ee1511d"
CERTIFICATE_COMMIT = "53aa9dfc5a58264df349e219c5a3cfe97c80dbe8"
FIGURE_ID = "fig-r069f-endpoint-scaling"
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


def solve_theta(amplitude: mp.mpf) -> mp.mpf:
    low = mp.mpf(0)
    high = mp.mpf(1)
    for _ in range(500):
        middle = (low + high) / 2
        if middle**3 < 2 * amplitude * (1 - middle):
            low = middle
        else:
            high = middle
    return (low + high) / 2


def prepare_data() -> tuple[dict[str, object], float]:
    started = time.perf_counter()
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("the pinned R0.69F certificate hash does not match")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("the R0.69F certificate did not pass")

    mp.mp.dps = 100
    amplitudes = np.logspace(-3, 3, 241)
    gain_rows: list[dict[str, object]] = []
    for amplitude_float in amplitudes:
        amplitude = mp.mpf(str(amplitude_float))
        theta = solve_theta(amplitude)
        exact_log = amplitude + mp.log(mp.erfc(-mp.sqrt(amplitude)))
        optimized_log = amplitude / theta**2 - mp.log(1 - theta)
        asymptotic_log = amplitude + mp.log(2 * mp.e * amplitude)
        gain_rows.append(
            {
                "A": mp.nstr(amplitude, 30),
                "thetaOptimizer": mp.nstr(theta, 35),
                "exactLogGain": mp.nstr(exact_log, 35),
                "exactLogGainMinusA": mp.nstr(exact_log - amplitude, 35),
                "optimizedBieleckiLog": mp.nstr(optimized_log, 35),
                "optimizedBieleckiLogMinusA": mp.nstr(
                    optimized_log - amplitude, 35
                ),
                "bieleckiAsymptoticLog": mp.nstr(asymptotic_log, 35),
                "bieleckiAsymptoticLogMinusA": mp.nstr(
                    asymptotic_log - amplitude, 35
                ),
                "stationarityResidual": mp.nstr(
                    abs(theta**3 - 2 * amplitude * (1 - theta)), 12
                ),
            }
        )
    write_rows(
        "gain-comparison.csv",
        [
            "A",
            "thetaOptimizer",
            "exactLogGain",
            "exactLogGainMinusA",
            "optimizedBieleckiLog",
            "optimizedBieleckiLogMinusA",
            "bieleckiAsymptoticLog",
            "bieleckiAsymptoticLogMinusA",
            "stationarityResidual",
        ],
        gain_rows,
    )

    constants = certificate["theorem"]["packetConstants"]
    c_rho = mp.mpf(constants["cRho"])
    x_rho = mp.mpf(constants["xRho"])
    threshold_rows: list[dict[str, object]] = []
    for x_float in np.linspace(0, 0.24, 241):
        x = mp.mpf(str(x_float))
        phi = x**2 + 2 * x / mp.sqrt(mp.pi)
        threshold_rows.append(
            {
                "x": mp.nstr(x, 25),
                "phi": mp.nstr(phi, 30),
                "cRho": mp.nstr(c_rho, 30),
                "aboveThreshold": int(phi >= c_rho),
            }
        )
    write_rows(
        "shell-threshold.csv",
        ["x", "phi", "cRho", "aboveThreshold"],
        threshold_rows,
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
        "gainSamples": len(gain_rows),
        "thresholdSamples": len(threshold_rows),
        "cRho": constants["cRho"],
        "xRho": constants["xRho"],
        "xRhoOverTwoSqrtPi": constants["xRhoOverTwoSqrtPi"],
        "claimBoundary": certificate["classification"],
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
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
    gain = read_rows("gain-comparison.csv")
    threshold = read_rows("shell-threshold.csv")
    c_rho = mp.mpf(str(metadata["cRho"]))
    x_rho = mp.mpf(str(metadata["xRho"]))
    phi_at_threshold = x_rho**2 + 2 * x_rho / mp.sqrt(mp.pi)
    stationarity = [
        mp.mpf(row["stationarityResidual"]) for row in gain
    ]
    exact_remainders = [
        mp.mpf(row["exactLogGainMinusA"]) for row in gain
    ]
    optimized_remainders = [
        mp.mpf(row["optimizedBieleckiLogMinusA"]) for row in gain
    ]
    checks = {
        "gainGridHasTwoHundredFortyOneSamples": len(gain) == 241,
        "thresholdGridHasTwoHundredFortyOneSamples": len(threshold) == 241,
        "allOptimizersSatisfyStationarity": max(stationarity) < mp.mpf("1e-80"),
        "optimizedBieleckiBoundExceedsExactGain": all(
            optimized >= exact
            for optimized, exact in zip(optimized_remainders, exact_remainders)
        ),
        "exactRemainderApproachesLogTwo": (
            abs(exact_remainders[-1] - mp.log(2)) < mp.mpf("1e-30")
        ),
        "bieleckiRemainderKeepsOnlyPolynomialLoss": (
            abs(
                optimized_remainders[-1]
                - mp.log(2 * mp.e * mp.mpf(gain[-1]["A"]))
            )
            < mp.mpf("0.002")
        ),
        "shellThresholdInvertsPacketRate": (
            abs(phi_at_threshold - c_rho) < mp.mpf("1e-45")
        ),
        "formalCertificatePassedTwentyTwoChecks": (
            metadata["checksPassed"] == metadata["checksTotal"] == 22
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
            line.rstrip()
            for line in path.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )


def blossom(figure) -> None:
    center = (0.946, 0.925)
    for dx, dy, angle in (
        (0, 0.010, 0),
        (0, -0.010, 0),
        (0.008, 0, 90),
        (-0.008, 0, 90),
    ):
        figure.add_artist(
            Ellipse(
                (center[0] + dx, center[1] + dy),
                0.010,
                0.018,
                angle=angle,
                transform=figure.transFigure,
                facecolor="#ead9b8",
                edgecolor=GOLD,
                linewidth=0.35,
            )
        )


def draw(metadata: dict[str, object]) -> float:
    started = time.perf_counter()
    gain = read_rows("gain-comparison.csv")
    threshold = read_rows("shell-threshold.csv")
    amplitudes = np.array([float(row["A"]) for row in gain])
    exact = np.array([float(row["exactLogGainMinusA"]) for row in gain])
    optimized = np.array([
        float(row["optimizedBieleckiLogMinusA"]) for row in gain
    ])
    asymptotic = np.array([
        float(row["bieleckiAsymptoticLogMinusA"]) for row in gain
    ])
    x_values = np.array([float(row["x"]) for row in threshold])
    phi_values = np.array([float(row["phi"]) for row in threshold])
    c_rho = float(metadata["cRho"])
    x_rho = float(metadata["xRho"])
    normalized_threshold = float(metadata["xRhoOverTwoSqrtPi"])

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 92 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            2,
            left=0.080,
            right=0.958,
            bottom=0.20,
            top=0.76,
            width_ratios=(1.08, 0.92),
            wspace=0.30,
        )
        gain_axis = figure.add_subplot(grid[0, 0])
        shell_axis = figure.add_subplot(grid[0, 1])
        figure.suptitle(
            "Exact resolvent optimization reaches only the classical type-I scale",
            x=0.055,
            y=0.947,
            ha="left",
            fontsize=8.0,
            color=INK,
        )
        figure.text(
            0.055,
            0.884,
            r"fractional Volterra gain  ·  optimized Bielecki weight  ·  $\beta=256$ endpoint shells",
            ha="left",
            fontsize=3.8,
            color=MUTED,
        )
        blossom(figure)

        gain_axis.set_title(
            "(a) The exponential cannot be optimized away",
            loc="left",
            pad=5,
        )
        gain_axis.semilogx(
            amplitudes,
            exact,
            color=BLUE,
            linestyle="-",
            linewidth=1.2,
            label=r"exact: $\log E_{1/2}(\sqrt{A})-A$",
        )
        gain_axis.semilogx(
            amplitudes,
            optimized,
            color=RUST,
            linestyle="--",
            linewidth=1.1,
            label=r"optimized Bielecki: $\log F_A-A$",
        )
        mask = amplitudes >= 0.1
        gain_axis.semilogx(
            amplitudes[mask],
            asymptotic[mask],
            color=GREEN,
            linestyle=":",
            linewidth=0.9,
            label=r"asymptotic: $\log(2eA)$",
        )
        gain_axis.axhline(
            math.log(2),
            color=INK,
            linewidth=0.55,
            linestyle=(0, (2, 2)),
        )
        gain_axis.text(
            1.4e-3,
            math.log(2) + 0.22,
            r"exact remainder $\to\log 2$",
            fontsize=3.1,
            color=INK,
        )
        gain_axis.set_xlabel(
            r"scale-invariant amplitude $A=4\pi C_S^2V^2h$"
        )
        gain_axis.set_ylabel(r"log gain after subtracting $A$")
        gain_axis.set_xlim(1e-3, 1e3)
        gain_axis.set_ylim(-0.15, 9.15)
        gain_axis.grid(color=GRID, linewidth=0.3)
        gain_axis.legend(loc="upper left", frameon=False, fontsize=3.15)

        shell_axis.set_title(
            "(b) Only a type-I shell threshold remains",
            loc="left",
            pad=5,
        )
        shell_axis.plot(
            x_values,
            phi_values,
            color=BLUE,
            linestyle="-",
            linewidth=1.2,
            label=r"$\phi(x)=x^2+2x/\sqrt{\pi}$",
        )
        shell_axis.axhline(
            c_rho,
            color=RUST,
            linestyle="--",
            linewidth=1.0,
            label=rf"$c_\rho={c_rho:.4f}$",
        )
        shell_axis.axvline(
            x_rho,
            color=GOLD,
            linestyle="-.",
            linewidth=1.0,
            label=rf"$x_\rho={x_rho:.4f}$",
        )
        shell_axis.fill_between(
            x_values,
            0,
            phi_values,
            where=x_values >= x_rho,
            color=PALE_BLUE,
            alpha=0.75,
        )
        shell_axis.plot(
            [x_rho],
            [c_rho],
            marker="o",
            markersize=3.1,
            markerfacecolor="white",
            markeredgecolor=INK,
            markeredgewidth=0.7,
            linestyle="none",
        )
        shell_axis.set_xlabel(
            r"local shell variable $x=2C_S\sqrt{\pi h}\,V$"
        )
        shell_axis.set_ylabel(r"rate majorant $\phi(x)$")
        shell_axis.set_xlim(0, 0.24)
        shell_axis.set_ylim(0, 0.34)
        shell_axis.grid(color=GRID, linewidth=0.3)
        shell_axis.legend(loc="upper left", frameon=False, fontsize=3.15)
        shell_axis.text(
            0.48,
            0.08,
            r"certificate: $\limsup V_j\sqrt{h_j}$" + "\n"
            + rf"$\geq {normalized_threshold:.5f}/C_S$"
            + "\nclassical continuation: every late shell",
            transform=shell_axis.transAxes,
            fontsize=3.0,
            color=INK,
            bbox={
                "facecolor": PALE_GOLD,
                "edgecolor": "none",
                "pad": 2.2,
            },
        )

        figure.text(
            0.055,
            0.065,
            "Claim boundary: a certified no-go result for scalar resolvent optimization; no singularity is excluded or constructed.",
            fontsize=3.15,
            color=MUTED,
        )
        export_metadata = {
            "Creator": "R0.69F fractional-Volterra endpoint scaling",
            "Date": None,
        }
        figure.savefig(HERE / "figure.pdf", metadata=export_metadata)
        figure.savefig(HERE / "figure.svg", metadata=export_metadata)
        figure.savefig(
            HERE / "figure.png",
            dpi=600,
            metadata=export_metadata,
        )
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
            ["sysctl", "-n", name],
            check=True,
            capture_output=True,
            text=True,
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
        "createdAt": "2026-08-21T06:45:00+08:00",
        "analyticalQuestion": (
            "Can optimizing the positive-time resolvent produce an endpoint "
            "blow-up rate beyond classical continuation theory?"
        ),
        "supportedClaim": (
            "The exact scalar gain and the optimized Bielecki certificate "
            "share the exponent A=4 pi C_S^2 V^2 h; packet-gate failure "
            "therefore forces only a type-I shell threshold."
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
            }
        ],
        "data": [
            record(
                HERE / "gain-comparison.csv",
                format="csv",
                schema="A, exact log gain, optimized Bielecki log gain, asymptotic",
            ),
            record(
                HERE / "shell-threshold.csv",
                format="csv",
                schema="x, phi(x), certified packet log rate, threshold flag",
            ),
            record(
                HERE / "figure-data-metadata.json",
                format="json",
                schema="pinned certificate and theorem metadata",
            ),
            record(
                HERE / "validation.json",
                format="json",
                schema="eight figure-data validation checks",
            ),
            record(
                HERE / "figure-data-resources.csv",
                format="csv",
                schema="data extraction resources",
            ),
            record(
                HERE / "plot-resources.csv",
                format="csv",
                schema="rendering resources",
            ),
        ],
        "computation": {
            "kind": "exact-audit plus high-precision presentation sampling",
            "configuration": (
                "241 logarithmic amplitude samples and 241 shell-threshold samples"
            ),
            "precision": "mpmath 100 decimal digits",
            "solver": (
                "bisection for the unique Bielecki cubic root and closed "
                "Mittag-Leffler complementary-error-function identity"
            ),
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
            "pillow": (
                Image.__version__
                if hasattr(Image, "__version__")
                else "bundled"
            ),
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
                record(
                    HERE / "figure.png",
                    dpi=600,
                    pixels=f"{png.width} by {png.height}",
                ),
            ],
        },
        "chartContract": {
            "family": "log-amplitude comparison plus exact shell threshold",
            "takeaway": (
                "scalar endpoint-resolvent optimization cannot improve the "
                "classical type-I scale"
            ),
            "nonColorEncoding": (
                "distinct line styles, direct threshold lines, marker, and "
                "formula callout"
            ),
            "outputFootprint": (
                "double-column 178 by 92 millimetres with PDF, SVG, and "
                "600 dpi PNG"
            ),
        },
        "qa": {
            "status": "passed",
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "notes": (
                "The final-size color and grayscale renders were inspected; "
                "line styles, threshold marker, formulas, and claim boundary "
                "remain legible without color."
            ),
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    started = time.perf_counter()
    metadata, _ = prepare_data()
    validate_data(metadata)
    draw(metadata)
    build_manifest(metadata, time.perf_counter() - started)


if __name__ == "__main__":
    main()
