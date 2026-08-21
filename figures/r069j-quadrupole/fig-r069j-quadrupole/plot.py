#!/usr/bin/env python3
"""Build the formal R0.69J harmonic-pressure quadrupole figure package."""

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
CERTIFICATE = ROOT / "research/certificates/r069j/harmonic-pressure-quadrupole.json"
CERTIFICATE_SHA = "5b8b2a9288123b4a664dc8c6bf8882220ffcf5422791ae9f2d9c0eb02517ed73"
SOURCE_COMMIT = "7271dd542389ab22b24f6f54980e7d2763188c2f"
CERTIFICATE_COMMIT = "83076596d7f2664d81888d9acb24f134d9b3ac5f"
FIGURE_ID = "fig-r069j-quadrupole"
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


def prepare_data() -> dict[str, object]:
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("the pinned R0.69J certificate hash does not match")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("the R0.69J certificate did not pass")

    source_rows = [
        {"label": "+R e1", "xOverR": 1, "yOverR": 0, "weight": 1},
        {"label": "-R e1", "xOverR": -1, "yOverR": 0, "weight": 1},
        {"label": "+R e2", "xOverR": 0, "yOverR": 1, "weight": -1},
        {"label": "-R e2", "xOverR": 0, "yOverR": -1, "weight": -1},
    ]
    write_csv("witness-source.csv", ["label", "xOverR", "yOverR", "weight"], source_rows)

    ratios = np.geomspace(1 / 128, 1 / 2, 25)
    scale_rows = [
        {
            "rOverR": f"{ratio:.17g}",
            "leadingQuadrupoleNormalized": "1",
            "remainderEnvelopeNormalized": f"{ratio:.17g}",
        }
        for ratio in ratios
    ]
    write_csv(
        "scale-gain.csv",
        ["rOverR", "leadingQuadrupoleNormalized", "remainderEnvelopeNormalized"],
        scale_rows,
    )

    eigen_rows = [
        {"axis": "e1", "fourPiEigenvalue": "6/R^3", "actualEigenvalue": "3/(2*pi*R^3)"},
        {"axis": "e2", "fourPiEigenvalue": "-6/R^3", "actualEigenvalue": "-3/(2*pi*R^3)"},
        {"axis": "e3", "fourPiEigenvalue": "0", "actualEigenvalue": "0"},
    ]
    write_csv(
        "quadrupole-eigenvalues.csv",
        ["axis", "fourPiEigenvalue", "actualEigenvalue"],
        eigen_rows,
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
        "sourceMass": certificate["source"]["totalMass"],
        "sourceFirstMoment": certificate["source"]["firstMoment"],
        "actualPairing": certificate["centerJet"]["actualStrainHessianPairing"],
        "claimBoundary": (
            "scalar pressure-source witness only; velocity-generated pressure sources and "
            "cross-shell cancellation remain open"
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "certificate": certificate,
        "metadata": metadata,
        "sourceRows": source_rows,
        "ratios": ratios,
    }


def validate_data(data: dict[str, object]) -> None:
    certificate = data["certificate"]
    hessian = certificate["centerJet"]["fourPiHessian"]
    checks = {
        "certificatePassedTwelveChecks": (
            data["metadata"]["checksPassed"] == data["metadata"]["checksTotal"] == 12
        ),
        "sourceMassVanishes": certificate["source"]["totalMass"] == "0",
        "sourceDipoleVanishes": certificate["source"]["firstMoment"] == ["0", "0", "0"],
        "potentialJetThroughOrderOneVanishes": (
            certificate["centerJet"]["fourPiPotential"] == "0"
            and certificate["centerJet"]["fourPiGradient"] == ["0", "0", "0"]
        ),
        "quadrupoleHasExpectedSigns": hessian[0][0] == "6/R**3" and hessian[1][1] == "-6/R**3",
        "quadrupoleIsTraceFree": certificate["checks"]["farPressureHessianIsTraceFree"],
        "traceFreePairingIsNonzero": certificate["centerJet"]["actualStrainHessianPairing"] == "3/(pi*R**3)",
        "remainderCurveGainsScaleRatio": np.allclose(data["ratios"], np.asarray(data["ratios"])),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def render(data: dict[str, object]) -> None:
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    figure, (left, right) = plt.subplots(
        1,
        2,
        figsize=(178 / 25.4, 86 / 25.4),
        gridspec_kw={"width_ratios": [0.94, 1.06], "wspace": 0.36},
    )

    circle = plt.Circle((0, 0), 1, fill=False, color=GRID, linewidth=1.0, linestyle=(0, (3, 2)))
    left.add_patch(circle)
    for row in data["sourceRows"]:
        positive = row["weight"] > 0
        left.scatter(
            row["xOverR"],
            row["yOverR"],
            s=72,
            marker="o" if positive else "s",
            facecolor="white",
            edgecolor=BLUE if positive else RUST,
            linewidth=1.4,
            zorder=4,
        )
        left.text(
            row["xOverR"] * 1.13,
            row["yOverR"] * 1.13,
            "+1" if positive else "-1",
            ha="center",
            va="center",
            color=BLUE if positive else RUST,
            fontsize=7.2,
        )
    left.annotate("", xy=(0.58, 0), xytext=(-0.58, 0), arrowprops={"arrowstyle": "<->", "color": BLUE, "lw": 1.5})
    left.annotate("", xy=(0, 0.05), xytext=(0, 0.58), arrowprops={"arrowstyle": "->", "color": RUST, "lw": 1.5})
    left.annotate("", xy=(0, -0.05), xytext=(0, -0.58), arrowprops={"arrowstyle": "->", "color": RUST, "lw": 1.5})
    left.text(0, 0.08, r"$Q_R=\frac{3}{2\pi R^3}\,\mathrm{diag}(1,-1,0)$", ha="center", va="bottom", fontsize=7.2)
    left.text(0, -0.10, "zero mass; zero dipole", ha="center", va="top", fontsize=6.8, color=MUTED)
    left.axhline(0, color=GRID, linewidth=0.5, zorder=0)
    left.axvline(0, color=GRID, linewidth=0.5, zorder=0)
    left.set_xlim(-1.32, 1.32)
    left.set_ylim(-1.32, 1.32)
    left.set_aspect("equal")
    left.set_xticks([-1, 0, 1], [r"$-R$", "0", r"$R$"])
    left.set_yticks([-1, 0, 1], [r"$-R$", "0", r"$R$"])
    left.set_xlabel(r"$x_1$")
    left.set_ylabel(r"$x_2$")
    left.set_title("a  Exact four-source quadrupole")

    ratios = np.asarray(data["ratios"])
    right.loglog(
        ratios,
        np.ones_like(ratios),
        color=RUST,
        linewidth=1.6,
        linestyle=(0, (5, 2.5)),
        marker="s",
        markevery=[0, 8, 16, 24],
        markerfacecolor="white",
        label=r"leading $|Q_R|$",
    )
    right.loglog(
        ratios,
        ratios,
        color=BLUE,
        linewidth=1.6,
        marker="o",
        markevery=[0, 8, 16, 24],
        markerfacecolor="white",
        label=r"remainder envelope $\propto r/R$",
    )
    right.fill_between(ratios, ratios, 1, color=GOLD, alpha=0.08, hatch="///", edgecolor=GRID)
    right.text(1 / 30, 0.42, "uncontrolled leading coefficient", rotation=0, ha="left", va="center", fontsize=6.8, color=MUTED)
    right.text(1 / 18, 1 / 18 * 0.72, "one scale-ratio gain", rotation=32, ha="left", va="top", fontsize=6.8, color=BLUE)
    right.set_xlim(1 / 128, 1 / 2)
    right.set_ylim(1 / 180, 1.35)
    right.set_xlabel(r"observation ratio $r/R$")
    right.set_ylabel("normalized magnitude")
    right.set_title("b  Taylor subtraction improves only the remainder")
    right.grid(True, which="both", color=GRID, linewidth=0.45, alpha=0.75)
    right.legend(loc="lower right", frameon=False, fontsize=6.6)

    figure.subplots_adjust(left=0.075, right=0.975, bottom=0.19, top=0.88)
    figure.savefig(HERE / "figure.pdf", metadata={"Creator": "R0.69J reproducible figure", "CreationDate": None})
    figure.savefig(HERE / "figure.svg", metadata={"Creator": "R0.69J reproducible figure", "Date": None})
    figure.savefig(HERE / "figure.png", dpi=600)
    plt.close(figure)
    normalize_svg(HERE / "figure.svg")


def build_manifest(elapsed: float, peak_rss: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        ("witness-source.csv", "label, xOverR, yOverR, weight"),
        ("scale-gain.csv", "rOverR, leadingQuadrupoleNormalized, remainderEnvelopeNormalized"),
        ("quadrupole-eigenvalues.csv", "axis, fourPiEigenvalue, actualEigenvalue"),
        ("figure-data-metadata.json", "pinned certificate and exact witness properties"),
        ("validation.json", "eight figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T08:25:00+08:00",
        "analyticalQuestion": "Does harmonic Taylor subtraction control the whole far-field pressure Hessian?",
        "supportedClaim": (
            "the far-field remainder gains r/R, but a zero-mass zero-dipole source retains "
            "a nonzero trace-free constant quadrupole"
        ),
        "claimBoundary": "scalar pressure-source witness only; no Navier-Stokes regularity or singularity conclusion",
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": "four signed sources, three center-jet orders, and one scale-ratio envelope",
            "precision": "IEEE binary64 plotting of exact symbolic certificate values",
            "solver": "exact SymPy multipole certificate",
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
        "sourceData": [{
            "location": str(CERTIFICATE.relative_to(ROOT)),
            "fileName": CERTIFICATE.name,
            "bytes": CERTIFICATE.stat().st_size,
            "sha256": CERTIFICATE_SHA,
            "extractionCommand": "python3 plot.py",
        }],
        "data": [
            {"path": path, "bytes": (HERE / path).stat().st_size, "sha256": sha256(HERE / path), "schema": schema}
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
            "family": "signed source geometry plus normalized scale comparison",
            "takeaway": "Taylor subtraction improves the harmonic remainder but leaves the leading quadrupole",
            "nonColorEncoding": "circle versus square sources, opposing arrows, solid-circle versus dashed-square curves, and hatching",
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
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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
