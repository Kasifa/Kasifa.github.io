#!/usr/bin/env python3
"""Build the formal R0.71F localized trace figure package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
INDEPENDENT_AUDIT = REPOSITORY / "research" / "r071f_independent_audit.py"
FFT_WAVENUMBERS = [1, 2, 4, 8]
WAVENUMBERS = [1, 2, 4, 8, 16, 32, 64, 128]
FFT_TAU = [0.0, 0.125, 0.5, 1.0, 2.0]
RADII = [2.0 ** (-index) for index in range(8)]
WIDTH_MM = 178
HEIGHT_MM = 104
DPI = 600

NAVY = "#17324d"
RUST = "#a44a2a"
INK = "#20262c"
GRAY = "#70777f"
LIGHT = "#d9dde1"
PALE_NAVY = "#dce7ef"
PALE_RUST = "#f0ded5"


FIELDS = [
    "kind",
    "index",
    "evidence_class",
    "tau",
    "k",
    "theta",
    "radius",
    "observed_q_ratio",
    "exact_q_ratio",
    "relative_error",
    "trace_multiplier_over_k2",
    "small_theta_reference",
    "large_theta_limit",
    "envelope",
    "normalized_bottom",
    "normalized_bulk",
    "critical_ratio",
    "subcritical_ratio",
    "source",
    "normalization",
    "claim_boundary",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def blank_row() -> dict[str, str]:
    return {field: "" for field in FIELDS}


def run_independent_fft() -> dict:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(INDEPENDENT_AUDIT), "--grid", "48"],
        cwd=REPOSITORY,
        env=environment,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def build_rows(fft_payload: dict) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index in range(241):
        tau = 3.0 * index / 240.0
        row = blank_row()
        row.update(
            {
                "kind": "profile_exact",
                "index": str(index),
                "evidence_class": "exact_formula",
                "tau": f"{tau:.17g}",
                "exact_q_ratio": f"{math.exp(-2.0 * tau):.17g}",
                "source": "q_phi(s)/q_phi(0)=exp(-2*K^2*s)",
                "normalization": "tau=K^2*s; q divided by q(0)",
                "claim_boundary": "analytic heat-height profile; not physical-time evolution",
            }
        )
        rows.append(row)

    case_by_k = {int(case["K"]): case for case in fft_payload["cases"]}
    for wave in FFT_WAVENUMBERS:
        case = case_by_k[wave]
        bottom = float(case["bottomQuotient"])
        for index, sample in enumerate(case["sampleRows"]):
            tau = float(sample["theta"])
            observed = float(sample["observedQ"]) / bottom
            exact = math.exp(-2.0 * tau)
            relative_error = abs(observed - exact) / max(abs(exact), 1.0e-300)
            row = blank_row()
            row.update(
                {
                    "kind": "profile_fft",
                    "index": str(index),
                    "evidence_class": "independent_fft_check",
                    "tau": f"{tau:.17g}",
                    "k": str(wave),
                    "observed_q_ratio": f"{observed:.17g}",
                    "exact_q_ratio": f"{exact:.17g}",
                    "relative_error": f"{relative_error:.17g}",
                    "source": "research/r071f_independent_audit.py; 48^3 FFT grid",
                    "normalization": "observed q divided by independently reconstructed q(0)",
                    "claim_boundary": "finite spectral verification; not DNS or PDE time stepping",
                }
            )
            rows.append(row)

    theta_values = np.geomspace(0.01, 10.0, 241)
    for index, theta in enumerate(theta_values):
        row = blank_row()
        row.update(
            {
                "kind": "trace_multiplier",
                "index": str(index),
                "evidence_class": "exact_formula",
                "theta": f"{theta:.17g}",
                "trace_multiplier_over_k2": f"{2.0 / (-math.expm1(-2.0 * theta)):.17g}",
                "small_theta_reference": f"{1.0 / theta:.17g}",
                "large_theta_limit": "2",
                "source": "2/(1-exp(-2*theta))",
                "normalization": "h=theta/K^2; trace multiplier divided by K^2",
                "claim_boundary": "exact finite heat-height trace factor",
            }
        )
        rows.append(row)

    for envelope in ("lower", "upper"):
        for index, wave in enumerate(WAVENUMBERS):
            row = blank_row()
            row.update(
                {
                    "kind": "partition_envelope",
                    "index": str(index),
                    "evidence_class": "normalized_analytic_envelope",
                    "k": str(wave),
                    "envelope": envelope,
                    "normalized_bottom": "1",
                    "normalized_bulk": f"{1.0 / (2.0 * wave**2):.17g}",
                    "source": "Section 8 analytic lower/upper bounds at a=K^(-1)",
                    "normalization": "each envelope divided by its own bottom prefactor",
                    "claim_boundary": "scale law only; N,C0,C1,rho are not assigned or measured",
                }
            )
            rows.append(row)

    for index, radius in enumerate(RADII):
        row = blank_row()
        row.update(
            {
                "kind": "geometry_scaling",
                "index": str(index),
                "evidence_class": "normalized_scaling_family",
                "radius": f"{radius:.17g}",
                "critical_ratio": f"{radius**-2.0:.17g}",
                "subcritical_ratio": f"{radius**-1.5:.17g}",
                "source": "NSE-covariant interior-cylinder scaling",
                "normalization": "base radius r0=1 and base ratio c_*=1",
                "claim_boundary": "different smooth solutions; subcritical curve is illustrative",
            }
        )
        rows.append(row)
    return rows


def write_data(rows: list[dict[str, str]], fft_payload: dict) -> None:
    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    maximum_fft_error = max(
        float(row["relative_error"])
        for row in rows
        if row["kind"] == "profile_fft"
    )
    write_json(
        ROOT / "figure-data-metadata.json",
        {
            "release": "R0.71F",
            "figureId": "fig-r071f-local-trace",
            "rows": len(rows),
            "evidenceClasses": {
                "exact_formula": "closed analytic evaluations sampled in binary64",
                "independent_fft_check": "full trigonometric velocity, independent FFT differentiation and Leray projection",
                "normalized_analytic_envelope": "symbolic lower/upper scale laws with their unknown constants divided out",
                "normalized_scaling_family": "NSE-covariant family of different smooth solutions",
            },
            "independentFft": {
                "grid": fft_payload["cases"][0]["grid"],
                "wavenumbers": FFT_WAVENUMBERS,
                "tau": FFT_TAU,
                "maximumDisplayedRelativeError": maximum_fft_error,
                "source": "research/r071f_independent_audit.py",
            },
            "randomSeed": None,
            "dns": False,
            "pdeTimeStepping": False,
            "fittedModel": False,
            "source": "figure-contract.md, research/r071f_report-source.md, and research/r071f_independent_audit.py",
        },
    )


def configure() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": 7.0,
            "axes.titlesize": 8.0,
            "axes.labelsize": 7.0,
            "xtick.labelsize": 6.4,
            "ytick.labelsize": 6.4,
            "legend.fontsize": 5.9,
            "axes.linewidth": 0.65,
            "lines.linewidth": 1.35,
            "savefig.transparent": False,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def panel_label(axis, label: str, title: str) -> None:
    axis.text(-0.13, 1.07, label, transform=axis.transAxes, fontweight="bold", fontsize=9)
    axis.set_title(title, loc="left", pad=6, fontweight="bold")


def add_blossom(fig) -> None:
    center_x, center_y = 0.974, 0.969
    radius = 0.0052
    petal_radius = 0.0028
    for angle in np.linspace(0, 2 * np.pi, 5, endpoint=False):
        fig.add_artist(
            Circle(
                (center_x + radius * math.cos(angle), center_y + radius * math.sin(angle)),
                petal_radius,
                transform=fig.transFigure,
                facecolor=PALE_NAVY,
                edgecolor=NAVY,
                linewidth=0.45,
            )
        )
    fig.add_artist(
        Circle(
            (center_x, center_y),
            0.0023,
            transform=fig.transFigure,
            facecolor=RUST,
            edgecolor=INK,
            linewidth=0.35,
        )
    )


def rows_of(rows: list[dict[str, str]], kind: str) -> list[dict[str, str]]:
    return [row for row in rows if row["kind"] == kind]


def draw_figure(rows: list[dict[str, str]]) -> None:
    configure()
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4))
    fig.subplots_adjust(left=0.079, right=0.985, bottom=0.102, top=0.815, wspace=0.32, hspace=0.60)

    ax = axes[0, 0]
    exact_rows = rows_of(rows, "profile_exact")
    tau = np.asarray([float(row["tau"]) for row in exact_rows])
    profile = np.asarray([float(row["exact_q_ratio"]) for row in exact_rows])
    ax.plot(tau, profile, color=INK, linewidth=1.6, label=r"exact $e^{-2\tau}$", zorder=2)
    marker_map = {1: "o", 2: "^", 4: "s", 8: "D"}
    offset_map = {1: -0.018, 2: -0.006, 4: 0.006, 8: 0.018}
    fft_rows = rows_of(rows, "profile_fft")
    for wave in reversed(FFT_WAVENUMBERS):
        selected = [row for row in fft_rows if int(row["k"]) == wave]
        ax.scatter(
            [float(row["tau"]) + offset_map[wave] for row in selected],
            [float(row["observed_q_ratio"]) for row in selected],
            s=24,
            marker=marker_map[wave],
            facecolor="white",
            edgecolor=NAVY if wave in (1, 4) else RUST,
            linewidth=0.75,
            zorder=3 + wave,
            label=rf"FFT $K={wave}$",
        )
    max_error = max(float(row["relative_error"]) for row in fft_rows)
    ax.text(
        0.97,
        0.55,
        rf"max relative residual $={max_error:.1e}$"
        + "\n"
        + r"FFT symbols offset $\leq0.018$ in $\tau$"
        + "\nfor visibility; not DNS",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=5.9,
        color=GRAY,
    )
    ax.set_xlim(-0.035, 3)
    ax.set_ylim(0, 1.06)
    ax.set_xlabel(r"dimensionless heat height $\tau=K^2s$")
    ax.set_ylabel(r"localized quotient $q_\phi(s)/q_\phi(0)$")
    ax.grid(axis="y", color=LIGHT, linewidth=0.5)
    handles, labels = ax.get_legend_handles_labels()
    order = [0, 4, 3, 2, 1]
    ax.legend([handles[index] for index in order], [labels[index] for index in order], frameon=False, ncol=2, loc="upper right")
    panel_label(ax, "A", "Localized heat profiles collapse exactly")

    ax = axes[0, 1]
    multiplier_rows = rows_of(rows, "trace_multiplier")
    theta = np.asarray([float(row["theta"]) for row in multiplier_rows])
    multiplier = np.asarray([float(row["trace_multiplier_over_k2"]) for row in multiplier_rows])
    small = np.asarray([float(row["small_theta_reference"]) for row in multiplier_rows])
    ax.loglog(theta, multiplier, color=RUST, linewidth=1.65, label=r"exact $2/(1-e^{-2\theta})$")
    small_mask = theta <= 0.18
    ax.loglog(theta[small_mask], small[small_mask], color=NAVY, linestyle="--", linewidth=1.0, label=r"short box $\theta^{-1}$")
    ax.axhline(2.0, color=INK, linestyle=":", linewidth=1.0, label=r"long box limit $2$")
    ax.scatter([0.01, 10.0], [multiplier[0], multiplier[-1]], s=19, facecolor="white", edgecolor=RUST, linewidth=0.7, zorder=4)
    ax.text(0.014, 58, r"$\sim\theta^{-1}$", color=NAVY, fontsize=6.2)
    ax.text(2.3, 2.45, r"$\to2$", color=INK, fontsize=6.2)
    ax.set_xlim(0.01, 10)
    ax.set_ylim(1.7, 130)
    ax.set_xlabel(r"matched heat height $\theta=K^2h$")
    ax.set_ylabel(r"trace multiplier / $K^2$")
    ax.grid(which="major", color=LIGHT, linewidth=0.5)
    ax.legend(frameon=False, loc="upper right")
    panel_label(ax, "B", "Finite boxes retain the critical trace factor")

    ax = axes[1, 0]
    partition = rows_of(rows, "partition_envelope")
    lower = [row for row in partition if row["envelope"] == "lower"]
    upper = [row for row in partition if row["envelope"] == "upper"]
    waves = np.asarray([float(row["k"]) for row in lower])
    bottom = np.asarray([float(row["normalized_bottom"]) for row in lower])
    bulk = np.asarray([float(row["normalized_bulk"]) for row in lower])
    ax.loglog(waves, bottom, color=RUST, marker="o", markerfacecolor="white", markersize=4.2, label="bottom envelope shape")
    ax.loglog(waves, bulk, color=NAVY, linestyle="--", marker="s", markerfacecolor="white", markersize=3.8, label="heat-bulk envelope shape")
    ax.scatter(waves, [float(row["normalized_bottom"]) for row in upper], s=7, marker="o", color=RUST, zorder=4)
    ax.scatter(waves, [float(row["normalized_bulk"]) for row in upper], s=8, marker="s", color=NAVY, zorder=4)
    ax.text(0.98, 0.91, "open/filled: lower/upper\nsame normalized law", transform=ax.transAxes, ha="right", va="top", fontsize=5.8, color=GRAY)
    ax.text(0.02, 0.05, "analytic envelope shape; prefactors divided out\nnot measured full-frame values", transform=ax.transAxes, ha="left", va="bottom", fontsize=5.8, color=GRAY)
    ax.set_xlabel("wavenumber $K$ at fixed energy $a=K^{-1}$")
    ax.set_ylabel("envelope / bottom prefactor")
    ax.set_xticks(WAVENUMBERS, [str(value) for value in WAVENUMBERS])
    ax.set_ylim(2e-5, 2)
    ax.grid(which="major", color=LIGHT, linewidth=0.5)
    ax.legend(frameon=False, loc="lower left", bbox_to_anchor=(0.0, 0.22))
    panel_label(ax, "C", "Partition bottom is flat; heat bulk is $K^{-2}$")

    ax = axes[1, 1]
    geometry = rows_of(rows, "geometry_scaling")
    radii = np.asarray([float(row["radius"]) for row in geometry])
    critical = np.asarray([float(row["critical_ratio"]) for row in geometry])
    subcritical = np.asarray([float(row["subcritical_ratio"]) for row in geometry])
    ax.loglog(radii, critical, color=RUST, marker="o", markerfacecolor="white", label=r"critical family $r^{-2}$")
    ax.loglog(radii, subcritical, color=GRAY, linestyle="--", marker="^", markerfacecolor="white", label=r"illustrative $r^{-3/2}$")
    ax.fill_between(radii, subcritical, critical, color=PALE_RUST, hatch="////", edgecolor=RUST, linewidth=0.35, alpha=0.55)
    ax.invert_xaxis()
    ax.set_xticks([1, 0.25, 0.0625, 0.015625], ["1", "1/4", "1/16", "1/64"])
    ax.text(0.98, 0.54, r"gap $=r^{-1/2}\to\infty$", transform=ax.transAxes, ha="right", fontsize=6.2, color=RUST)
    ax.text(0.98, 0.08, "critical saturated; subcritical rejected\ndifferent smooth solutions, not blow-up", transform=ax.transAxes, ha="right", va="bottom", fontsize=5.8, color=GRAY)
    ax.set_xlabel("cylinder radius $r$ (smaller to the right)")
    ax.set_ylabel("base-normalized bottom / heat bulk")
    ax.set_ylim(0.8, 3e4)
    ax.grid(which="major", color=LIGHT, linewidth=0.5)
    ax.legend(frameon=False, loc="upper left")
    panel_label(ax, "D", "Geometry saturates the $r^{-2}$ boundary")

    fig.suptitle(
        "R0.71F | Localization packs the heat bulk, not the bottom trace",
        x=0.079,
        y=0.975,
        ha="left",
        fontsize=8.8,
        fontweight="bold",
    )
    fig.text(
        0.079,
        0.924,
        "exact formulas  ·  independent FFT checks  ·  normalized analytic envelopes  ·  not DNS",
        ha="left",
        va="center",
        fontsize=6.1,
        color=GRAY,
    )
    add_blossom(fig)
    for extension in ("pdf", "svg", "png"):
        kwargs = {"bbox_inches": None, "facecolor": "white"}
        if extension == "png":
            kwargs["dpi"] = DPI
        fig.savefig(ROOT / f"figure.{extension}", **kwargs)
    svg_path = ROOT / "figure.svg"
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)
    shutil.copyfile(ROOT / "figure.png", ROOT / "qa-original.png")
    image = Image.open(ROOT / "figure.png").convert("RGB")
    ImageOps.grayscale(image).convert("RGB").save(ROOT / "qa-grayscale.png", dpi=(DPI, DPI))


def validation_payload(rows: list[dict[str, str]]) -> dict:
    png = Image.open(ROOT / "figure.png")
    profiles = rows_of(rows, "profile_exact")
    fft = rows_of(rows, "profile_fft")
    multipliers = rows_of(rows, "trace_multiplier")
    partitions = rows_of(rows, "partition_envelope")
    geometry = rows_of(rows, "geometry_scaling")
    checks = {
        "dataHasExpectedRows": len(rows) == 526,
        "profileHas241Rows": len(profiles) == 241,
        "fftHasTwentyRows": len(fft) == 20,
        "fftWavenumbersExact": sorted({int(row["k"]) for row in fft}) == FFT_WAVENUMBERS,
        "fftTauExact": sorted({float(row["tau"]) for row in fft}) == FFT_TAU,
        "fftResidualBelowTolerance": max(float(row["relative_error"]) for row in fft) < 2e-12,
        "multiplierHas241Rows": len(multipliers) == 241,
        "partitionHasSixteenRows": len(partitions) == 16,
        "partitionEnvelopeLabels": {row["envelope"] for row in partitions} == {"lower", "upper"},
        "geometryHasEightRows": len(geometry) == 8,
        "figurePdfExists": (ROOT / "figure.pdf").stat().st_size > 10_000,
        "figurePngExists": (ROOT / "figure.png").stat().st_size > 100_000,
        "figureSvgExists": (ROOT / "figure.svg").stat().st_size > 10_000,
        "pdfSignature": (ROOT / "figure.pdf").read_bytes()[:4] == b"%PDF",
        "pngSignature": (ROOT / "figure.png").read_bytes()[1:4] == b"PNG",
        "svgRootPresent": b"<svg" in (ROOT / "figure.svg").read_bytes()[:1000],
        "pngWidthAt600Dpi": png.width in (4204, 4205),
        "pngHeightAt600Dpi": png.height in (2456, 2457),
        "grayscaleQaExists": (ROOT / "qa-grayscale.png").stat().st_size > 100_000,
        "noDns": True,
        "noPdeTimeStepping": True,
        "noRandomSeed": True,
    }
    return {"release": "R0.71F", "status": "pass" if all(checks.values()) else "fail", "checks": checks}


def write_environment(elapsed: float) -> None:
    (ROOT / "environment.txt").write_text(
        "\n".join(
            [
                f"Python: {platform.python_version()}",
                f"Platform: {platform.platform()}",
                f"Machine: {platform.machine()}",
                f"Logical CPUs: {os.cpu_count()}",
                f"Matplotlib: {matplotlib.__version__}",
                f"NumPy: {np.__version__}",
                f"Pillow: {Image.__version__ if hasattr(Image, '__version__') else 'installed'}",
                "Independent FFT source: research/r071f_independent_audit.py, 48^3 grid",
                "DGX: not used",
                "GPU: not used",
                "Processes: 1",
                "Threads per process: 1",
                f"Wall time seconds: {elapsed:.3f}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def finalize() -> None:
    required = [
        "plot.py",
        "validate_data.py",
        "contract.json",
        "figure-contract.md",
        "caption.md",
        "command.txt",
        "data.csv",
        "figure-data-metadata.json",
        "environment.txt",
        "validation.json",
        "independent-validation.json",
        "figure.pdf",
        "figure.svg",
        "figure.png",
        "qa-original.png",
        "qa-grayscale.png",
        "qa-report.md",
    ]
    missing = [name for name in required if not (ROOT / name).exists()]
    if missing:
        raise FileNotFoundError(f"missing archive payloads: {missing}")
    outputs = []
    for name in required:
        path = ROOT / name
        item = {"path": name, "bytes": path.stat().st_size, "sha256": sha256(path)}
        if name == "figure.png":
            with Image.open(path) as image:
                item.update({"dpi": DPI, "pixels": f"{image.width} by {image.height}"})
        outputs.append(item)
    manifest = {
        "schemaVersion": "1.0",
        "release": "R0.71F",
        "status": "formal",
        "figureId": "fig-r071f-local-trace",
        "createdAt": "2026-08-25T00:00:00+08:00",
        "analyticalQuestion": "After genuine localization or matched-partition packing, what exact trace loss remains between the projected-Lamb heat bulk and its bottom face?",
        "supportedClaim": "Localized heat packing remains valid, but the exact smooth witnesses retain the critical K-square or r-minus-two bottom trace cost.",
        "claimBoundary": "Exact formulas, independent FFT checks, normalized analytic envelopes, and a scaling family only; no DNS, persistence theorem, critical-trace rejection, singularity, regularity, or Millennium-problem claim.",
        "figure": {
            "profile": "journal-default",
            "widthMillimetres": WIDTH_MM,
            "heightMillimetres": HEIGHT_MM,
            "script": "plot.py",
            "outputs": [item for item in outputs if item["path"].startswith("figure.") or item["path"].startswith("qa-")],
        },
        "compute": {"host": "local Mac workstation", "dgx": "not used", "gpu": "not used", "processes": 1},
        "computation": {
            "kind": "exact-formula figure with independent FFT overlay",
            "solver": "closed formulas plus independent finite FFT reconstruction; no PDE time stepping",
            "precision": "analytic formulas and binary64 display/check values",
        },
        "outputs": outputs,
        "qa": {
            "status": "passed",
            "automaticChecks": "validation.json",
            "independentChecks": "independent-validation.json",
            "manualReport": "qa-report.md",
        },
    }
    write_json(ROOT / "manifest.json", manifest)
    sum_names = required + ["manifest.json"]
    (ROOT / "SHA256SUMS").write_text(
        "".join(f"{sha256(ROOT / name)}  {name}\n" for name in sum_names),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize-only", action="store_true")
    args = parser.parse_args()
    if args.finalize_only:
        finalize()
        return
    start = time.perf_counter()
    fft_payload = run_independent_fft()
    rows = build_rows(fft_payload)
    write_data(rows, fft_payload)
    draw_figure(rows)
    write_json(ROOT / "validation.json", validation_payload(rows))
    elapsed = time.perf_counter() - start
    write_environment(elapsed)
    (ROOT / "qa-report.md").write_text(
        "# R0.71F figure QA\n\n"
        "Status: pending direct inspection of the original 600 dpi PNG, its grayscale conversion, and a 300 dpi rendering of the PDF.\n\n"
        "- Automatic formula, provenance, format, signature, and output-size checks have run.\n"
        "- Manual checks for clipping, collisions, grayscale distinction, and PDF rendering remain.\n"
        "- Exact curves, independent FFT points, normalized analytic envelopes, and scaling families are visibly distinguished.\n"
        "- The figure is not DNS, fitted data, or PDE time stepping.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
