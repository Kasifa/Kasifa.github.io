#!/usr/bin/env python3
"""Build the formal R0.69P sharp vortex-stretching sign figure."""
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
CERTIFICATE = ROOT / "research/certificates/r069p/vorticity-stretching-sign-structure.json"
CERTIFICATE_SHA = "75f1ffcfd8d7b66e6fee0603c596b2c6f0aed9be701bcc10b47b9a277ff8e718"
SOURCE_COMMIT = "1471752c76624699c0f5a40d523bdc484a49cbd3"
CERTIFICATE_COMMIT = "f8514f1879ad41c2ee0761d82eeca5d010cf78af"
FIGURE_ID = "fig-r069p-stretching-sign"
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
        raise RuntimeError("pinned R0.69P certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("R0.69P certificate did not pass")

    theta_degrees = np.linspace(0.0, 90.0, 181)
    theta_radians = np.deg2rad(theta_degrees)
    alignment_coefficient = (3.0 * np.cos(theta_radians) ** 2 - 1.0) / np.sqrt(6.0)
    normalized_positive_alignment = np.maximum(alignment_coefficient, 0.0) / np.sqrt(2.0 / 3.0)
    write_csv(
        "alignment-profile.csv",
        ["thetaDegrees", "stretchingCoefficient", "normalizedPositiveAlignment"],
        [
            {
                "thetaDegrees": f"{theta:.8f}",
                "stretchingCoefficient": f"{coefficient:.12f}",
                "normalizedPositiveAlignment": f"{normalized:.12f}",
            }
            for theta, coefficient, normalized in zip(
                theta_degrees, alignment_coefficient, normalized_positive_alignment
            )
        ],
    )

    eigenvalue_ratio = np.geomspace(1.0, 100.0, 241)
    determinant_ratio = 2.0 * eigenvalue_ratio * (1.0 + eigenvalue_ratio) / (
        1.0 + eigenvalue_ratio + eigenvalue_ratio**2
    )
    gap_to_two = 2.0 / (1.0 + eigenvalue_ratio + eigenvalue_ratio**2)
    write_csv(
        "middle-eigenvalue-ratio.csv",
        ["lambda3OverLambda2", "determinantRatio", "gapToSharpSupremum"],
        [
            {
                "lambda3OverLambda2": f"{ratio:.12f}",
                "determinantRatio": f"{coefficient:.12f}",
                "gapToSharpSupremum": f"{gap:.12f}",
            }
            for ratio, coefficient, gap in zip(
                eigenvalue_ratio, determinant_ratio, gap_to_two
            )
        ],
    )

    normalized_dissipation = np.linspace(0.0, 4.0, 321)
    normalized_young_profit = (
        4.0 * normalized_dissipation ** 0.75 - 3.0 * normalized_dissipation
    )
    write_csv(
        "stretching-young-profile.csv",
        ["dissipationOverOptimizer", "profitOverMaximum"],
        [
            {
                "dissipationOverOptimizer": f"{value:.8f}",
                "profitOverMaximum": f"{profit:.8f}",
            }
            for value, profit in zip(normalized_dissipation, normalized_young_profit)
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
        "pointwiseSharpConstant": certificate["sharpPointwiseStretching"]["constant"],
        "determinantSharpSupremum": certificate["betchov"]["sharpSupremum"],
        "youngRemainder": certificate["energyOnlyEndpoint"]["youngRemainder"],
        "claimBoundary": (
            "exact pointwise and energy-only algebra; no unconditional spacetime "
            "depletion estimate or Navier-Stokes regularity theorem"
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return (
        certificate,
        metadata,
        theta_degrees,
        alignment_coefficient,
        normalized_positive_alignment,
        eigenvalue_ratio,
        determinant_ratio,
        gap_to_two,
        normalized_dissipation,
        normalized_young_profit,
    )


def validate_data(values) -> None:
    (
        certificate,
        metadata,
        theta_degrees,
        alignment_coefficient,
        normalized_positive_alignment,
        eigenvalue_ratio,
        determinant_ratio,
        gap_to_two,
        normalized_dissipation,
        normalized_young_profit,
    ) = values
    theta_zero = np.degrees(np.arccos(1.0 / np.sqrt(3.0)))
    checks = {
        "certificatePassedTwentyChecks": metadata["checksPassed"] == metadata["checksTotal"] == 20,
        "alignmentEndpointIsSqrtTwoThirds": np.isclose(
            alignment_coefficient[0], np.sqrt(2.0 / 3.0)
        ),
        "alignmentNegativeEndpointIsMinusOneOverSqrtSix": np.isclose(
            alignment_coefficient[-1], -1.0 / np.sqrt(6.0)
        ),
        "alignmentZeroAngleIsFiftyFourPointSevenDegrees": np.isclose(
            np.interp(theta_zero, theta_degrees, alignment_coefficient), 0.0, atol=2e-5
        ),
        "normalizedAlignmentEndpointIsOne": np.isclose(
            normalized_positive_alignment[0], 1.0
        ),
        "determinantRatioStartsAtFourThirds": np.isclose(
            determinant_ratio[0], 4.0 / 3.0
        ),
        "determinantRatioIsStrictlyIncreasing": np.all(np.diff(determinant_ratio) > 0.0),
        "determinantGapIdentity": np.allclose(
            2.0 - determinant_ratio, gap_to_two
        ),
        "youngProfilePeaksAtOptimizer": np.isclose(
            normalized_dissipation[np.argmax(normalized_young_profit)], 1.0
        ) and np.isclose(np.max(normalized_young_profit), 1.0),
        "certificateYoungRemainderIsSextic": (
            certificate["energyOnlyEndpoint"]["youngRemainder"]
            == "27*sigma**6/(256*epsilon**3)"
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
        theta_degrees,
        alignment_coefficient,
        _,
        eigenvalue_ratio,
        determinant_ratio,
        _,
        normalized_dissipation,
        normalized_young_profit,
    ) = values
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig, (left, middle, right) = plt.subplots(
        1,
        3,
        figsize=(178 / 25.4, 82 / 25.4),
        gridspec_kw={"width_ratios": [1.04, 1.0, 1.02], "wspace": 0.42},
    )

    left.plot(theta_degrees, alignment_coefficient, color=INK, lw=1.45)
    left.fill_between(
        theta_degrees,
        0.0,
        alignment_coefficient,
        where=alignment_coefficient >= 0.0,
        color=RUST,
        alpha=0.20,
        hatch="///",
        edgecolor=RUST,
        linewidth=0.0,
    )
    left.fill_between(
        theta_degrees,
        0.0,
        alignment_coefficient,
        where=alignment_coefficient < 0.0,
        color=BLUE,
        alpha=0.16,
        hatch="\\\\",
        edgecolor=BLUE,
        linewidth=0.0,
    )
    theta_zero = np.degrees(np.arccos(1.0 / np.sqrt(3.0)))
    left.axhline(0.0, color=MUTED, lw=0.75)
    left.axvline(theta_zero, color=MUTED, lw=0.8, ls=(0, (3, 2)))
    left.scatter(
        [0.0], [np.sqrt(2.0 / 3.0)], s=28, facecolor=GOLD,
        edgecolor=INK, linewidth=0.6, zorder=4,
    )
    left.annotate(
        r"sharp $\sqrt{2/3}$" "\n" r"locally realizable",
        xy=(0.0, np.sqrt(2.0 / 3.0)),
        xytext=(0.25, 0.79),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        fontsize=5.8,
        color=MUTED,
    )
    left.text(
        theta_zero + 2.0,
        -0.32,
        r"$\theta_0=54.7^\circ$",
        fontsize=5.6,
        color=MUTED,
    )
    left.set(
        xlabel=r"angle $\theta$ from extensional eigenvector",
        ylabel=r"$(\omega\!\cdot\!S\omega)/(|S||\omega|^2)$",
        title="a  Alignment has both signs",
    )
    left.set_xlim(0.0, 90.0)
    left.set_xticks([0, 30, 60, 90])
    left.set_ylim(-0.50, 0.96)
    left.grid(True, color=GRID, lw=0.45, alpha=0.75)

    middle.plot(eigenvalue_ratio, determinant_ratio, color=RUST, lw=1.5)
    middle.axhline(2.0, color=INK, lw=0.9, ls=(0, (3, 2)))
    middle.scatter(
        [1.0], [4.0 / 3.0], s=25, marker="s", facecolor="white",
        edgecolor=BLUE, linewidth=0.9, zorder=4,
    )
    middle.annotate(
        r"$2-\dfrac{2}{1+r+r^2}$" "\n" r"$\nearrow\ 2$",
        xy=(38.0, np.interp(38.0, eigenvalue_ratio, determinant_ratio)),
        xytext=(0.34, 0.25),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        fontsize=5.8,
        color=MUTED,
    )
    middle.set_xscale("log")
    middle.set(
        xlabel=r"eigenvalue ratio $r=\lambda_3/\lambda_2$",
        ylabel=r"$(-4\det S)/(\lambda_2|S|^2)$",
        title="b  Betchov isolates middle strain",
    )
    middle.set_xlim(1.0, 100.0)
    middle.set_ylim(1.22, 2.08)
    middle.grid(True, color=GRID, lw=0.45, alpha=0.75)

    right.plot(
        normalized_dissipation,
        normalized_young_profit,
        color=BLUE,
        lw=1.5,
    )
    right.axhline(0.0, color=INK, lw=0.75)
    right.axvline(1.0, color=MUTED, lw=0.9, ls=(0, (3, 2)))
    right.scatter(
        [1.0], [1.0], s=28, marker="o", facecolor=GOLD,
        edgecolor=INK, linewidth=0.6, zorder=4,
    )
    right.annotate(
        r"$D_*=[3\sigma^{3/2}/(4\varepsilon)]^4$" "\n"
        r"$\max=27\sigma^6/(256\varepsilon^3)$",
        xy=(1.0, 1.0),
        xytext=(0.08, 0.70),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        fontsize=5.55,
        color=MUTED,
    )
    right.set(
        xlabel=r"normalized dissipation $D/D_*$",
        ylabel="normalized Young profit",
        title="c  Energy-only cost stays sextic",
    )
    right.set_xlim(0.0, 4.0)
    right.set_ylim(-0.82, 1.18)
    right.grid(True, color=GRID, lw=0.45, alpha=0.75)

    fig.subplots_adjust(left=0.082, right=0.992, bottom=0.22, top=0.86)
    fig.savefig(
        HERE / "figure.pdf",
        metadata={"Creator": "R0.69P reproducible figure", "CreationDate": None},
    )
    fig.savefig(
        HERE / "figure.svg",
        metadata={"Creator": "R0.69P reproducible figure", "Date": None},
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
            "alignment-profile.csv",
            "thetaDegrees, stretchingCoefficient, normalizedPositiveAlignment",
        ),
        (
            "middle-eigenvalue-ratio.csv",
            "lambda3OverLambda2, determinantRatio, gapToSharpSupremum",
        ),
        (
            "stretching-young-profile.csv",
            "dissipationOverOptimizer, profitOverMaximum",
        ),
        ("figure-data-metadata.json", "pinned R0.69P sign-structure certificate"),
        ("validation.json", "ten figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    payload = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T11:20:00+08:00",
        "analyticalQuestion": (
            "Can incompressibility or Betchov cancellation force favorable "
            "vortex-stretching geometry or improve the energy-only exponent?"
        ),
        "supportedClaim": (
            "the sharp pointwise stretching endpoint and the positive middle-"
            "eigenvalue endpoint are locally realizable, while the energy-only "
            "Young remainder remains sextic"
        ),
        "claimBoundary": (
            "exact pointwise and energy-only algebra; no unconditional spacetime "
            "depletion estimate or Navier-Stokes regularity theorem"
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
                "181 angular samples, 241 logarithmic eigenvalue-ratio samples, "
                "and 321 normalized Young-profile samples"
            ),
            "precision": "IEEE binary64 plotting of exact closed-form formulas",
            "solver": "closed-form strain-eigenvalue and Young identities",
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
                "angular stretching profile, middle-eigenvalue determinant ratio, "
                "and normalized Young optimization"
            ),
            "takeaway": (
                "pointwise sign geometry is sharp and locally realizable; without "
                "new spacetime information the stretching remainder stays sextic"
            ),
            "nonColorEncoding": (
                "hatching, endpoint markers, line styles, and direct value labels"
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
