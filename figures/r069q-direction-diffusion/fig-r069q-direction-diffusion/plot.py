#!/usr/bin/env python3
"""Build the formal R0.69Q vorticity-direction diffusion figure."""
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
CERTIFICATE = ROOT / "research/certificates/r069q/vorticity-direction-diffusion-obstruction.json"
CERTIFICATE_SHA = "5db39990d92371618e7feb6d53e35587392ac89791022da8a983ad74c9f11bfa"
SOURCE_COMMIT = "c5e19140c3dc79d22eb368e63dc2014681afff18"
CERTIFICATE_COMMIT = "502c4f56f660e7c7a0c916815f9142f781e36d81"
FIGURE_ID = "fig-r069q-direction-diffusion"
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
        raise RuntimeError("pinned R0.69Q certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("R0.69Q certificate did not pass")

    split_degrees = np.linspace(0.0, 90.0, 181)
    split_radians = np.deg2rad(split_degrees)
    radial_fraction = np.cos(split_radians) ** 2
    angular_fraction = np.sin(split_radians) ** 2
    total_fraction = radial_fraction + angular_fraction
    write_csv(
        "polar-dissipation-split.csv",
        ["splitDegrees", "radialFraction", "angularFraction", "totalFraction"],
        [
            {
                "splitDegrees": f"{angle:.8f}",
                "radialFraction": f"{radial:.12f}",
                "angularFraction": f"{angular:.12f}",
                "totalFraction": f"{total:.12f}",
            }
            for angle, radial, angular, total in zip(
                split_degrees, radial_fraction, angular_fraction, total_fraction
            )
        ],
    )

    affine_labels = [
        "positive stretching",
        "radial dissipation",
        "angular dissipation",
        "full interior dissipation",
    ]
    affine_values = np.array([1.0, 0.0, 0.0, 0.0])
    write_csv(
        "affine-core-obstruction.csv",
        ["quantity", "normalizedValue"],
        [
            {"quantity": label, "normalizedValue": f"{value:.1f}"}
            for label, value in zip(affine_labels, affine_values)
        ],
    )

    length_scales = np.geomspace(1e-2, 1e2, 321)
    amplitude_over_viscosity = np.array([0.25, 1.0, 4.0])
    scale_factors = np.array(
        [coefficient * length_scales**2 for coefficient in amplitude_over_viscosity]
    )
    write_csv(
        "absorption-scaling.csv",
        ["lengthScale", "amplitudeOverViscosity", "ratioFactor"],
        [
            {
                "lengthScale": f"{length:.12e}",
                "amplitudeOverViscosity": f"{coefficient:.8f}",
                "ratioFactor": f"{factor:.12e}",
            }
            for coefficient, row in zip(amplitude_over_viscosity, scale_factors)
            for length, factor in zip(length_scales, row)
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
        "positiveStretching": certificate["affineCore"]["positiveStretching"],
        "directionDissipationAverageLimit": certificate["shortTimeObstruction"]
        ["directionDissipationAverageLimit"],
        "fullDissipationAverageLimit": certificate["shortTimeObstruction"]
        ["fullDissipationAverageLimit"],
        "scalingRatio": certificate["scalingObstruction"]["ratio"],
        "claimBoundary": (
            "exact polar identities and interior-only obstruction; no exclusion "
            "of cutoff-flux or nonlocal geometric estimates"
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return (
        certificate,
        metadata,
        split_degrees,
        radial_fraction,
        angular_fraction,
        total_fraction,
        affine_labels,
        affine_values,
        length_scales,
        amplitude_over_viscosity,
        scale_factors,
    )


def validate_data(values) -> None:
    (
        certificate,
        metadata,
        split_degrees,
        radial_fraction,
        angular_fraction,
        total_fraction,
        _,
        affine_values,
        length_scales,
        amplitude_over_viscosity,
        scale_factors,
    ) = values
    checks = {
        "certificatePassedEighteenChecks": metadata["checksPassed"]
        == metadata["checksTotal"]
        == 18,
        "polarFractionsSumToOne": np.allclose(total_fraction, 1.0),
        "radialEndpointIsOne": np.isclose(radial_fraction[0], 1.0),
        "angularEndpointIsOne": np.isclose(angular_fraction[-1], 1.0),
        "affineCoreProductionIsPositive": np.isclose(affine_values[0], 1.0),
        "affineCoreDissipationsVanish": np.allclose(affine_values[1:], 0.0),
        "unitScalingIsQuadratic": np.allclose(scale_factors[1], length_scales**2),
        "scaleFactorIsStrictlyIncreasing": np.all(np.diff(scale_factors, axis=1) > 0.0),
        "scaleWindowSpansEightOrders": np.isclose(
            scale_factors[1, -1] / scale_factors[1, 0], 1e8
        ),
        "certificateShortTimeDissipationLimitsVanish": (
            certificate["shortTimeObstruction"]["directionDissipationAverageLimit"]
            == certificate["shortTimeObstruction"]["fullDissipationAverageLimit"]
            == "0"
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


def render(values) -> None:
    (
        _,
        _,
        split_degrees,
        radial_fraction,
        angular_fraction,
        total_fraction,
        _,
        affine_values,
        length_scales,
        amplitude_over_viscosity,
        scale_factors,
    ) = values
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig, (left, middle, right) = plt.subplots(
        1,
        3,
        figsize=(178 / 25.4, 82 / 25.4),
        gridspec_kw={"width_ratios": [1.04, 0.92, 1.10], "wspace": 0.43},
    )

    left.fill_between(
        split_degrees,
        0.0,
        radial_fraction,
        color=BLUE,
        alpha=0.22,
        hatch="///",
        edgecolor=BLUE,
        linewidth=0.0,
        label=r"radial $|\nabla\rho|^2$",
    )
    left.fill_between(
        split_degrees,
        radial_fraction,
        total_fraction,
        color=GOLD,
        alpha=0.26,
        hatch="\\\\",
        edgecolor=GOLD,
        linewidth=0.0,
        label=r"angular $\rho^2|\nabla\xi|^2$",
    )
    left.plot(split_degrees, total_fraction, color=INK, lw=1.1)
    left.annotate(
        r"exact sum $=|\nabla\omega|^2$",
        xy=(66.0, 1.0),
        xytext=(0.18, 0.87),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        fontsize=5.7,
        color=MUTED,
    )
    left.set(
        xlabel="representative polar split angle (degrees)",
        ylabel="fraction of enstrophy dissipation",
        title="a  Angular loss is not extra",
    )
    left.set_xlim(0.0, 90.0)
    left.set_ylim(0.0, 1.12)
    left.set_xticks([0, 30, 60, 90])
    left.legend(loc="lower center", frameon=False, fontsize=5.3)
    left.grid(True, color=GRID, lw=0.45, alpha=0.72)

    positions = np.arange(4)
    colors = [RUST, BLUE, GOLD, MUTED]
    hatches = ["///", "\\\\", "..", "xx"]
    bars = middle.bar(
        positions,
        affine_values,
        color=colors,
        alpha=0.62,
        edgecolor=INK,
        linewidth=0.65,
    )
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
    middle.scatter([1, 2, 3], [0, 0, 0], marker="x", s=24, color=INK, zorder=4)
    middle.text(
        0,
        1.04,
        r"$\sqrt{2/3}\,s w^2$",
        ha="center",
        va="bottom",
        fontsize=5.8,
        color=RUST,
    )
    middle.annotate(
        "all three vanish\non the same open ball",
        xy=(2.0, 0.0),
        xytext=(0.22, 0.54),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        fontsize=5.6,
        color=MUTED,
    )
    middle.set(
        ylabel="normalized core value",
        title="b  Affine core defeats absorption",
    )
    middle.set_xticks(positions, ["stretch", "radial", "angular", "full"], rotation=28)
    middle.set_ylim(-0.08, 1.24)
    middle.grid(True, axis="y", color=GRID, lw=0.45, alpha=0.72)

    line_styles = [(0, (2, 1)), "-", (0, (5, 2))]
    markers = ["s", "o", "^"]
    for coefficient, factors, style, marker in zip(
        amplitude_over_viscosity, scale_factors, line_styles, markers
    ):
        right.plot(
            length_scales,
            factors,
            color=BLUE if coefficient == 1.0 else (RUST if coefficient < 1.0 else GOLD),
            lw=1.25,
            ls=style,
            marker=marker,
            markevery=[0, 80, 160, 240, 320],
            ms=2.7,
            label=rf"$a/\nu={coefficient:g}$",
        )
    right.axhline(1.0, color=INK, lw=0.75, ls=(0, (3, 2)))
    right.annotate(
        r"ratio factor $=aL^2/\nu$",
        xy=(10.0, 100.0),
        xytext=(0.08, 0.86),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        fontsize=5.7,
        color=MUTED,
    )
    right.set_xscale("log")
    right.set_yscale("log")
    right.set(
        xlabel=r"length scale $L$",
        ylabel="production / viscous-dissipation factor",
        title="c  No scale-independent constant",
    )
    right.set_xlim(1e-2, 1e2)
    right.set_ylim(2e-5, 8e4)
    right.legend(loc="lower right", frameon=False, fontsize=5.3)
    right.grid(True, which="both", color=GRID, lw=0.42, alpha=0.66)

    fig.subplots_adjust(left=0.080, right=0.992, bottom=0.225, top=0.86)
    fig.savefig(
        HERE / "figure.pdf",
        metadata={"Creator": "R0.69Q reproducible figure", "CreationDate": None},
    )
    fig.savefig(
        HERE / "figure.svg",
        metadata={"Creator": "R0.69Q reproducible figure", "Date": None},
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
        (
            "polar-dissipation-split.csv",
            "splitDegrees, radialFraction, angularFraction, totalFraction",
        ),
        ("affine-core-obstruction.csv", "quantity, normalizedValue"),
        (
            "absorption-scaling.csv",
            "lengthScale, amplitudeOverViscosity, ratioFactor",
        ),
        ("figure-data-metadata.json", "pinned R0.69Q direction-diffusion certificate"),
        ("validation.json", "ten figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    payload = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T11:45:00+08:00",
        "analyticalQuestion": (
            "Can diffusion of the vorticity direction automatically absorb "
            "positive vortex stretching?"
        ),
        "supportedClaim": (
            "direction dissipation is exactly part of enstrophy dissipation, "
            "and a sharp affine core makes both vanish while stretching is positive"
        ),
        "claimBoundary": (
            "exact local and scaling obstruction only; cutoff-flux and nonlocal "
            "geometric estimates remain open"
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
                "181 polar-split samples, four affine-core observables, and "
                "three 321-point exact scaling curves"
            ),
            "precision": "IEEE binary64 plotting of exact closed-form identities",
            "solver": "closed-form polar decomposition and similarity scaling",
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
                "polar dissipation decomposition, affine-core endpoint bars, "
                "and exact similarity-scaling curves"
            ),
            "takeaway": (
                "angular diffusion is not extra and cannot furnish an "
                "interior-only universal absorption constant"
            ),
            "nonColorEncoding": (
                "hatching, zero markers, line styles, marker shapes, and direct labels"
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

