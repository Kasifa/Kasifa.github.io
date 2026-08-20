#!/usr/bin/env python3
"""Build the formal R0.69G signed-kernel robustness figure package."""

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
    / "research/certificates/r069g/"
    "signed-vorticity-kernel-robustness.json"
)
CERTIFICATE_SHA = (
    "9731713f62632dddfd2da71280c1543c889c5d69e841cd9950c7641614493af8"
)
SOURCE_COMMIT = "ae328c0b02905bf48d12468ea11bbd27e3664959"
CERTIFICATE_COMMIT = "fed7a927c5732ba92e9ca70bff0edf43a463a7aa"
FIGURE_ID = "fig-r069g-signed-kernel"
TILT = 0.73
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


def prepare_data() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, dict[str, object]]:
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("the pinned R0.69G certificate hash does not match")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("the R0.69G certificate did not pass")

    azimuth = np.linspace(0, 2 * math.pi, 241)
    mu = np.linspace(-1, 1, 181)
    phi_grid, mu_grid = np.meshgrid(azimuth, mu)
    kernel = (
        -math.sin(TILT)
        * np.sqrt(np.maximum(0, 1 - mu_grid**2))
        * np.sin(phi_grid)
        * mu_grid
    )
    angular_rows = []
    for row in range(mu_grid.shape[0]):
        for column in range(mu_grid.shape[1]):
            angular_rows.append(
                {
                    "azimuthOverPi": f"{phi_grid[row, column] / math.pi:.12g}",
                    "mu": f"{mu_grid[row, column]:.12g}",
                    "D": f"{kernel[row, column]:.17g}",
                    "sign": int(np.sign(kernel[row, column])),
                }
            )
    write_csv(
        "angular-kernel.csv",
        ["azimuthOverPi", "mu", "D", "sign"],
        angular_rows,
    )

    eta = np.linspace(0, 0.95, 96)
    exact_absolute_mean = 2 * math.sin(TILT) / (3 * math.pi)
    response = eta * exact_absolute_mean
    certified = certificate["angularAudit"]["magnitudeBiasScenarios"]
    certified_eta = np.asarray([row["eta"] for row in certified], dtype=float)
    certified_response = np.asarray(
        [float(row["observedWeightedMean"]) for row in certified],
        dtype=float,
    )
    write_csv(
        "bias-response.csv",
        ["eta", "exactWeightedMean"],
        [
            {"eta": f"{x:.12g}", "exactWeightedMean": f"{y:.17g}"}
            for x, y in zip(eta, response, strict=True)
        ],
    )
    write_csv(
        "certified-bias-nodes.csv",
        ["eta", "quadratureWeightedMean"],
        [
            {"eta": f"{x:.12g}", "quadratureWeightedMean": f"{y:.17g}"}
            for x, y in zip(certified_eta, certified_response, strict=True)
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
        "checksPassed": sum(bool(value) for value in certificate["checks"].values()),
        "checksTotal": len(certificate["checks"]),
        "tiltRadians": TILT,
        "angularGrid": "181 by 241",
        "biasSamples": len(eta),
        "certifiedBiasNodes": len(certified_eta),
        "exactAbsoluteAngularMean": exact_absolute_mean,
        "claimBoundary": certificate["classification"],
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return phi_grid, mu_grid, kernel, eta, response, {
        **metadata,
        "certifiedEta": certified_eta,
        "certifiedResponse": certified_response,
    }


def validate_data(
    kernel: np.ndarray,
    eta: np.ndarray,
    response: np.ndarray,
    metadata: dict[str, object],
) -> None:
    exact_supremum = math.sin(TILT) / 2
    sampled_supremum = float(np.max(np.abs(kernel)))
    checks = {
        "certificatePassedFourteenChecks": (
            metadata["checksPassed"] == metadata["checksTotal"] == 14
        ),
        "kernelGridHasExpectedShape": kernel.shape == (181, 241),
        "kernelChangesSign": float(np.min(kernel)) < 0 < float(np.max(kernel)),
        "uniformAzimuthalMeanCancels": float(np.max(np.abs(np.mean(kernel, axis=1)))) < 1e-16,
        "sampledSupremumMatchesHalfSine": abs(sampled_supremum - exact_supremum) < 3e-5,
        "uniformMagnitudeResponseIsZero": bool(response[0] == 0),
        "positiveBiasCreatesPositiveStretching": bool(np.all(response[1:] > 0)),
        "biasResponseIsExactlyLinear": float(np.max(np.abs(np.diff(response, 2)))) < 1e-15,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "checks": checks,
                "sampledSupremum": sampled_supremum,
                "exactSupremum": exact_supremum,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def render(
    phi_grid: np.ndarray,
    mu_grid: np.ndarray,
    kernel: np.ndarray,
    eta: np.ndarray,
    response: np.ndarray,
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
        gridspec_kw={"width_ratios": [1.15, 0.85], "wspace": 0.34},
    )

    scale = math.sin(TILT) / 2
    levels = np.linspace(-scale, scale, 13)
    field = left.contourf(
        phi_grid / math.pi,
        mu_grid,
        kernel,
        levels=levels,
        cmap="RdBu_r",
        extend="both",
    )
    negative_levels = [-0.25, -0.12]
    positive_levels = [0.12, 0.25]
    left.contour(
        phi_grid / math.pi,
        mu_grid,
        kernel,
        levels=negative_levels,
        colors=INK,
        linewidths=0.55,
        linestyles="dashed",
    )
    left.contour(
        phi_grid / math.pi,
        mu_grid,
        kernel,
        levels=[0],
        colors=INK,
        linewidths=0.9,
    )
    left.contour(
        phi_grid / math.pi,
        mu_grid,
        kernel,
        levels=positive_levels,
        colors=INK,
        linewidths=0.55,
        linestyles="solid",
    )
    left.text(0.50, 0.52, "+", color=INK, fontsize=10, fontweight="bold")
    left.text(1.50, 0.52, "−", color=INK, fontsize=10, fontweight="bold")
    left.text(0.50, -0.52, "−", color=INK, fontsize=10, fontweight="bold")
    left.text(1.50, -0.52, "+", color=INK, fontsize=10, fontweight="bold")
    left.set_xlabel(r"azimuth $\phi/\pi$")
    left.set_ylabel(r"$\mu=\widehat z_3$")
    left.set_xticks([0, 0.5, 1, 1.5, 2])
    left.set_title("a  Signed angular kernel")
    left.text(
        0.025,
        0.97,
        r"$D=-\sin(0.73)\,\widehat z_2\widehat z_3$",
        transform=left.transAxes,
        ha="left",
        va="top",
        fontsize=7.1,
        color=MUTED,
    )
    colorbar = figure.colorbar(field, ax=left, fraction=0.045, pad=0.025)
    colorbar.set_label(r"signed $D$")

    right.plot(
        eta,
        response,
        color=RUST,
        linewidth=1.7,
        label=r"exact $\eta\,2\sin(0.73)/(3\pi)$",
    )
    right.scatter(
        metadata["certifiedEta"],
        metadata["certifiedResponse"],
        s=22,
        facecolors="white",
        edgecolors=BLUE,
        linewidths=1.0,
        zorder=3,
        label="certified quadrature",
    )
    right.axhline(0, color=INK, linewidth=0.8, linestyle=(0, (4, 3)))
    right.annotate(
        "uniform magnitude\nexactly cancels",
        xy=(0, 0),
        xytext=(0.08, 0.055),
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        color=MUTED,
        fontsize=7.4,
    )
    right.annotate(
        "magnitude bias\nselects a sign lobe",
        xy=(0.78, response[np.searchsorted(eta, 0.78)]),
        xytext=(0.44, 0.115),
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        color=MUTED,
        fontsize=7.4,
    )
    right.set_xlim(-0.025, 0.98)
    right.set_ylim(-0.008, 0.15)
    right.set_xlabel(r"magnitude bias $\eta$")
    right.set_ylabel(r"normalized signed mean")
    right.set_title("b  Cancellation is not robust")
    right.grid(True, color=GRID, linewidth=0.45, alpha=0.8)
    right.legend(loc="lower right", frameon=False, fontsize=6.8)

    figure.subplots_adjust(left=0.075, right=0.98, bottom=0.17, top=0.88)
    figure.savefig(
        HERE / "figure.pdf",
        metadata={"Creator": "R0.69G reproducible figure", "CreationDate": None},
    )
    figure.savefig(
        HERE / "figure.svg",
        metadata={"Creator": "R0.69G reproducible figure", "Date": None},
    )
    figure.savefig(HERE / "figure.png", dpi=600)
    plt.close(figure)
    normalize_svg(HERE / "figure.svg")


def build_manifest(elapsed: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        "angular-kernel.csv",
        "bias-response.csv",
        "certified-bias-nodes.csv",
        "figure-data-metadata.json",
        "validation.json",
        "resources.csv",
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T07:10:00+08:00",
        "analyticalQuestion": (
            "Can sign changes of the vorticity-direction kernel provide a "
            "uniform annular gain without controlling vorticity magnitude?"
        ),
        "supportedClaim": (
            "uniform angular averaging cancels in the two-lobe model, but any "
            "positive magnitude bias selects a sign lobe; the general positive-"
            "weight supremum equals the L-infinity norm of the kernel"
        ),
        "claimBoundary": (
            "structural no-go for direction-only uniform cancellation; no "
            "Navier-Stokes regularity conclusion"
        ),
        "git": {
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "repository": "Kasifa/Kasifa.github.io",
            "dirtyAtCertifiedRun": False,
        },
        "sourceData": [{
            "fileName": CERTIFICATE.name,
            "location": str(CERTIFICATE.relative_to(ROOT)),
            "bytes": CERTIFICATE.stat().st_size,
            "sha256": CERTIFICATE_SHA,
            "extractionCommand": "python3 plot.py",
        }],
        "data": [
            {
                "path": name,
                "bytes": (HERE / name).stat().st_size,
                "sha256": sha256(HERE / name),
                "schema": {
                    "angular-kernel.csv": "azimuthOverPi, mu, D, sign",
                    "bias-response.csv": "eta, exactWeightedMean",
                    "certified-bias-nodes.csv": "eta, quadratureWeightedMean",
                    "figure-data-metadata.json": "pinned certificate and grid metadata",
                    "validation.json": "eight figure-data validation checks",
                    "resources.csv": "elapsedSeconds, maximumRssMiB, status",
                }[name],
            }
            for name in data_files
        ],
        "computation": {
            "kind": "exact-audit",
            "configuration": "181 by 241 angular grid and 96 bias samples",
            "precision": "IEEE binary64 presentation sampling from exact formulas",
            "solver": "closed angular kernel and linear magnitude-bias response",
            "command": "python3 plot.py",
            "wallTimeSeconds": elapsed,
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": platform.platform(),
            "cpu": "Apple M5 Max",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": 1,
            "maximumRssMiB": rss_mib(),
        },
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "pillow": Image.__version__,
            "packagesLock": "requirements-research.txt",
        },
        "figure": {
            "script": "plot.py",
            "widthMillimetres": 178,
            "heightMillimetres": 86,
            "profile": "journal-default",
            "outputs": [
                {
                    "path": name,
                    "bytes": (HERE / name).stat().st_size,
                    "sha256": sha256(HERE / name),
                    **(
                        {"dpi": 600, "pixels": f"{image.width} by {image.height}"}
                        if name.endswith(".png")
                        else {}
                    ),
                }
                for name in outputs
            ],
        },
        "chartContract": {
            "family": "signed angular map plus magnitude-bias response",
            "takeaway": (
                "direction-only signed cancellation is destroyed by positive "
                "magnitude selection"
            ),
            "nonColorEncoding": (
                "signed contour styles, explicit plus/minus labels, exact line, "
                "and open quadrature markers"
            ),
            "outputFootprint": (
                "double-column 178 by 86 millimetres with PDF, SVG, and 600 dpi PNG"
            ),
        },
        "qa": {
            "status": "pending visual inspection",
            "dataCrossChecked": True,
            "finalSizeInspected": False,
            "grayscaleInspected": False,
            "labelsAndLegendsInspected": False,
            "scalesAndUnitsInspected": True,
        },
        "caption": {"english": "caption.md"},
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    started = time.perf_counter()
    phi_grid, mu_grid, kernel, eta, response, metadata = prepare_data()
    validate_data(kernel, eta, response, metadata)
    render(phi_grid, mu_grid, kernel, eta, response, metadata)
    elapsed = time.perf_counter() - started
    write_csv(
        "resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{
            "elapsedSeconds": f"{elapsed:.6f}",
            "maximumRssMiB": f"{rss_mib():.3f}",
            "status": "passed",
        }],
    )
    build_manifest(elapsed)
    print(json.dumps({
        "status": "passed",
        "figureId": FIGURE_ID,
        "elapsedSeconds": elapsed,
        "outputs": {
            name: sha256(HERE / name)
            for name in ("figure.pdf", "figure.svg", "figure.png")
        },
    }, indent=2))


if __name__ == "__main__":
    main()
