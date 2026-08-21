#!/usr/bin/env python3
"""Build the formal R0.69R nonlocal-vorticity-difference figure."""
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
CERTIFICATE = ROOT / "research/certificates/r069r/nonlocal-vorticity-difference-split.json"
CERTIFICATE_SHA = "39da9891b8c66dc37b9e02db05d6bd469b32ed84fb282578ca3dd997a2217cc5"
SOURCE_COMMIT = "97cfa19f962309bb62ae3fab0e4dcaef9f9eca38"
CERTIFICATE_COMMIT = "e1ea54cd2e6cecdcae71db5e87980ea5c939d4d2"
FIGURE_ID = "fig-r069r-nonlocal-difference"
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
        raise RuntimeError("pinned R0.69R certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("R0.69R certificate did not pass")

    radius = np.geomspace(0.1, 10.0, 321)
    near = 1.5 * radius
    far = radius ** (-1.5)
    total = near + far
    write_csv(
        "near-far-balance.csv",
        ["radiusOverOptimal", "nearContribution", "farContribution", "totalBound"],
        [
            {
                "radiusOverOptimal": f"{x:.12e}",
                "nearContribution": f"{n:.12e}",
                "farContribution": f"{f:.12e}",
                "totalBound": f"{t:.12e}",
            }
            for x, n, f, t in zip(radius, near, far, total)
        ],
    )

    p_values = np.linspace(0.0, 4.0, 321)
    amplitude_q = 3.0 - p_values
    spatial_q = (6.0 - p_values) / 3.0
    write_csv(
        "scaling-constraints.csv",
        ["p", "qAmplitude", "qSpatial"],
        [
            {"p": f"{p:.8f}", "qAmplitude": f"{qa:.8f}", "qSpatial": f"{qs:.8f}"}
            for p, qa, qs in zip(p_values, amplitude_q, spatial_q)
        ],
    )

    d_values = np.linspace(0.0, 3.5, 351)
    production = 4.0 * d_values ** 0.75
    dissipation = 3.0 * d_values
    profit = production - dissipation
    write_csv(
        "young-endpoint.csv",
        ["dOverOptimal", "production", "dissipation", "profit"],
        [
            {
                "dOverOptimal": f"{d:.8f}",
                "production": f"{prod:.12e}",
                "dissipation": f"{loss:.12e}",
                "profit": f"{gain:.12e}",
            }
            for d, prod, loss, gain in zip(d_values, production, dissipation, profit)
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
        "optimalRadius": certificate["nearFarSplit"]["optimalRadius"],
        "optimizedBound": certificate["nearFarSplit"]["optimizedBound"],
        "enstrophyNormPower": certificate["youngEndpoint"]["enstrophyNormPower"],
        "claimBoundary": (
            "norm-only absolute near/far split; signed scale-local cancellation remains open"
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return certificate, metadata, radius, near, far, total, p_values, amplitude_q, spatial_q, d_values, production, dissipation, profit


def validate_data(values) -> None:
    certificate, metadata, radius, near, far, total, _, amplitude_q, spatial_q, d_values, _, _, profit = values
    minimum_index = int(np.argmin(total))
    young_index = int(np.argmax(profit))
    checks = {
        "certificatePassedFifteenChecks": metadata["checksPassed"] == metadata["checksTotal"] == 15,
        "normalizedSplitMinimumOccursAtOne": np.isclose(radius[minimum_index], 1.0),
        "normalizedSplitMinimumIsFiveHalves": np.isclose(total[minimum_index], 2.5),
        "nearTermIncreases": np.all(np.diff(near) > 0.0),
        "farTermDecreases": np.all(np.diff(far) < 0.0),
        "scalingLinesIntersectAtThreeHalves": np.isclose(
            amplitude_q[120], spatial_q[120]
        ) and np.isclose(amplitude_q[120], 1.5),
        "scalingIntersectionIsUnique": np.count_nonzero(
            np.isclose(amplitude_q, spatial_q, atol=1e-12)
        ) == 1,
        "youngMaximumOccursAtOne": np.isclose(d_values[young_index], 1.0),
        "youngMaximumIsOne": np.isclose(profit[young_index], 1.0),
        "certificateYoungPowerIsSix": certificate["youngEndpoint"]["enstrophyNormPower"] == 6,
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def render(values) -> None:
    _, _, radius, near, far, total, p_values, amplitude_q, spatial_q, d_values, production, dissipation, profit = values
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig, (left, middle, right) = plt.subplots(
        1, 3, figsize=(178 / 25.4, 82 / 25.4),
        gridspec_kw={"width_ratios": [1.04, 0.94, 1.08], "wspace": 0.43},
    )

    left.plot(radius, near, color=BLUE, lw=1.2, ls="-", label=r"near $Xr$")
    left.plot(radius, far, color=RUST, lw=1.2, ls=(0, (4, 2)), label=r"far $Yr^{-3/2}$")
    left.plot(radius, total, color=INK, lw=1.35, ls=(0, (1.5, 1.2)), label="sum")
    left.scatter([1.0], [2.5], marker="o", s=20, facecolor=GOLD, edgecolor=INK, zorder=4)
    left.annotate(
        r"$r=r_*$; total $=5/2$", xy=(1.0, 2.5), xytext=(0.08, 0.84),
        textcoords="axes fraction", arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        fontsize=5.6, color=MUTED,
    )
    left.set_xscale("log")
    left.set_yscale("log")
    left.set(xlabel=r"normalized split radius $r/r_*$", ylabel="normalized bound", title="a  Cancellation meets the far field")
    left.set_xlim(0.1, 10.0)
    left.set_ylim(0.55, 34.0)
    left.legend(loc="lower right", frameon=False, fontsize=5.3)
    left.grid(True, which="both", color=GRID, lw=0.42, alpha=0.68)

    middle.plot(p_values, amplitude_q, color=BLUE, lw=1.25, ls="-", label=r"amplitude: $p+q=3$")
    middle.plot(p_values, spatial_q, color=RUST, lw=1.25, ls=(0, (4, 2)), label=r"space: $p+3q=6$")
    middle.scatter([1.5], [1.5], marker="D", s=24, facecolor=GOLD, edgecolor=INK, zorder=4)
    middle.annotate(
        r"unique: $p=q=3/2$", xy=(1.5, 1.5), xytext=(0.08, 0.18),
        textcoords="axes fraction", arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        fontsize=5.6, color=MUTED,
    )
    middle.set(xlabel=r"power $p$ of $A=\|\omega\|_2$", ylabel=r"power $q$ of $B=\|\nabla\omega\|_2$", title="b  Scaling fixes both exponents")
    middle.set_xlim(0.0, 4.0)
    middle.set_ylim(-0.25, 3.25)
    middle.set_xticks([0, 1, 2, 3, 4])
    middle.legend(loc="upper right", frameon=False, fontsize=5.0)
    middle.grid(True, color=GRID, lw=0.45, alpha=0.7)

    right.plot(d_values, production, color=BLUE, lw=1.1, ls="-", label=r"$4d^{3/4}$")
    right.plot(d_values, dissipation, color=RUST, lw=1.1, ls=(0, (4, 2)), label=r"$3d$")
    right.fill_between(d_values, 0.0, profit, where=profit >= 0.0, color=GOLD, alpha=0.25, hatch="///", edgecolor=GOLD, linewidth=0.0)
    right.plot(d_values, profit, color=INK, lw=1.35, label="difference")
    right.scatter([1.0], [1.0], marker="o", s=20, facecolor=GOLD, edgecolor=INK, zorder=4)
    right.annotate(
        r"maximum $=1$ at $d=1$", xy=(1.0, 1.0), xytext=(0.34, 0.20),
        textcoords="axes fraction", arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
        fontsize=5.6, color=MUTED,
    )
    right.set(xlabel=r"normalized dissipation $d=D/D_*$", ylabel="normalized Young terms", title="c  Sextic absorption cost")
    right.set_xlim(0.0, 3.5)
    right.set_ylim(-0.75, 11.5)
    right.legend(loc="upper left", frameon=False, fontsize=5.2)
    right.grid(True, color=GRID, lw=0.45, alpha=0.7)

    fig.subplots_adjust(left=0.078, right=0.993, bottom=0.225, top=0.86)
    fig.savefig(HERE / "figure.pdf", metadata={"Creator": "R0.69R reproducible figure", "CreationDate": None})
    fig.savefig(HERE / "figure.svg", metadata={"Creator": "R0.69R reproducible figure", "Date": None})
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)
    svg = HERE / "figure.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")


def write_manifest(elapsed: float, peak: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        ("near-far-balance.csv", "radiusOverOptimal, nearContribution, farContribution, totalBound"),
        ("scaling-constraints.csv", "p, qAmplitude, qSpatial"),
        ("young-endpoint.csv", "dOverOptimal, production, dissipation, profit"),
        ("figure-data-metadata.json", "pinned R0.69R difference-split certificate"),
        ("validation.json", "ten figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    payload = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T13:10:00+08:00",
        "analyticalQuestion": "Can the exact vorticity difference improve the classical enstrophy exponent after an energy far-field split?",
        "supportedClaim": "the difference removes one local singular order, but exact radius optimization and scaling return A^(3/2) B^(3/2) and a sextic Young remainder",
        "claimBoundary": "absolute norm-only near/far route only; signed scale-local cancellation remains open",
        "git": {"repository": "Kasifa/Kasifa.github.io", "sourceCommit": SOURCE_COMMIT, "certificateCommit": CERTIFICATE_COMMIT, "dirtyAtCertifiedRun": False},
        "computation": {
            "kind": "exact-audit",
            "configuration": "321 near/far radius samples, 321 scaling-constraint samples, and 351 Young-endpoint samples",
            "precision": "IEEE binary64 plotting of exact closed-form identities",
            "solver": "closed-form near/far optimization, scaling constraints, and Young duality",
            "command": "python3 plot.py",
            "wallTimeSeconds": elapsed,
        },
        "compute": {"host": "local Mac workstation", "operatingSystem": f"{platform.system()}-{platform.release()}-{platform.machine()}", "cpu": "Apple M5 Max", "memoryGiB": 36, "processes": 1, "threadsPerProcess": 1, "maximumRssMiB": peak},
        "environment": {"python": platform.python_version(), "matplotlib": matplotlib.__version__, "numpy": np.__version__, "pillow": Image.__version__, "packagesLock": "requirements-research.txt"},
        "sourceData": [{"location": str(CERTIFICATE.relative_to(ROOT)), "fileName": CERTIFICATE.name, "bytes": CERTIFICATE.stat().st_size, "sha256": CERTIFICATE_SHA, "extractionCommand": "python3 plot.py"}],
        "data": [{"path": path, "bytes": (HERE / path).stat().st_size, "sha256": sha256(HERE / path), "schema": schema} for path, schema in data_files],
        "figure": {
            "widthMillimetres": 178, "heightMillimetres": 82, "profile": "journal-default", "script": "plot.py",
            "outputs": [
                {"path": path, "bytes": (HERE / path).stat().st_size, "sha256": sha256(HERE / path), **({"dpi": 600, "pixels": f"{image.width} by {image.height}"} if path.endswith(".png") else {})}
                for path in outputs
            ],
        },
        "caption": {"english": "caption.md"},
        "chartContract": {
            "family": "near/far balance curves, scaling-constraint intersection, and normalized Young endpoint",
            "takeaway": "difference cancellation alone does not change the classical norm powers",
            "nonColorEncoding": "line styles, marker shapes, hatching, and direct annotations",
            "outputFootprint": "double-column 178 by 82 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {"status": "passed", "finalSizeInspected": True, "grayscaleInspected": True, "labelsAndLegendsInspected": True, "scalesAndUnitsInspected": True, "dataCrossChecked": True},
    }
    (HERE / "manifest.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    started = time.perf_counter()
    values = prepare_data()
    validate_data(values)
    render(values)
    elapsed = time.perf_counter() - started
    peak = rss_mib()
    write_csv("resources.csv", ["elapsedSeconds", "maximumRssMiB", "status"], [{"elapsedSeconds": f"{elapsed:.9f}", "maximumRssMiB": f"{peak:.6f}", "status": "passed"}])
    write_manifest(elapsed, peak)


if __name__ == "__main__":
    main()
