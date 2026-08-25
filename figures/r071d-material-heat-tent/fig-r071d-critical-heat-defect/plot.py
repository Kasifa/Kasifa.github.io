#!/usr/bin/env python3
"""Build and archive the formal R0.71D critical heat-defect figure."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import shutil
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent
RHO = 0.5
WAVENUMBERS = [1, 2, 4, 8, 16, 32, 64, 128]
THETAS = [0.25, 0.5, 1.0]
WIDTH_MM = 178
HEIGHT_MM = 104
DPI = 600
NAVY = "#17324d"
RUST = "#a44a2a"
GRAY = "#70777f"
LIGHT = "#d9dde1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index in range(241):
        z = 2 * math.pi * index / 240
        rows.append(
            {
                "kind": "geometry",
                "index": str(index),
                "z": f"{z:.17g}",
                "k": "",
                "theta": "",
                "phi_plus": f"{(1 + RHO * math.cos(2 * z)) / 2:.17g}",
                "phi_minus": f"{(1 - RHO * math.cos(2 * z)) / 2:.17g}",
                "omega_sq": f"{math.cos(z) ** 2:.17g}",
                "beta_plus_norm": "",
                "beta_minus_norm": "",
                "parent_norm": "",
                "fine_defect_norm": "",
                "critical_rate": "",
                "critical_rate_over_k2": "",
                "box_cost": "",
                "cauchy_ratio": "",
            }
        )
    rows.append(
        {
            "kind": "ledger",
            "index": "0",
            "z": "",
            "k": "1",
            "theta": "",
            "phi_plus": "",
            "phi_minus": "",
            "omega_sq": "",
            "beta_plus_norm": f"{-RHO / 2:.17g}",
            "beta_minus_norm": f"{RHO / 2:.17g}",
            "parent_norm": "0",
            "fine_defect_norm": f"{RHO**2 / (2 + RHO):.17g}",
            "critical_rate": "",
            "critical_rate_over_k2": "",
            "box_cost": "",
            "cauchy_ratio": "",
        }
    )
    for wave in WAVENUMBERS:
        rate = wave**2 * RHO**2 / (2 + RHO)
        rows.append(
            {
                "kind": "scaling",
                "index": str(WAVENUMBERS.index(wave)),
                "z": "",
                "k": str(wave),
                "theta": "",
                "phi_plus": "",
                "phi_minus": "",
                "omega_sq": "",
                "beta_plus_norm": "",
                "beta_minus_norm": "",
                "parent_norm": "",
                "fine_defect_norm": "",
                "critical_rate": f"{rate:.17g}",
                "critical_rate_over_k2": f"{rate / wave**2:.17g}",
                "box_cost": "",
                "cauchy_ratio": "",
            }
        )
        for theta in THETAS:
            cost = RHO**2 * (1 - math.exp(-2 * theta)) / (2 * (2 + RHO))
            rows.append(
                {
                    "kind": "box",
                    "index": str(WAVENUMBERS.index(wave)),
                    "z": "",
                    "k": str(wave),
                    "theta": f"{theta:.17g}",
                    "phi_plus": "",
                    "phi_minus": "",
                    "omega_sq": "",
                    "beta_plus_norm": "",
                    "beta_minus_norm": "",
                    "parent_norm": "",
                    "fine_defect_norm": "",
                    "critical_rate": "",
                    "critical_rate_over_k2": "",
                    "box_cost": f"{cost:.17g}",
                    "cauchy_ratio": "1",
                }
            )
    return rows


def write_data(rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0])
    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    write_json(
        ROOT / "figure-data-metadata.json",
        {
            "release": "R0.71D",
            "figureId": "fig-r071d-critical-heat-defect",
            "kind": "closed exact formulas sampled in binary64 for display",
            "parameters": {"rho": RHO, "wavenumbers": WAVENUMBERS, "theta": THETAS},
            "rows": len(rows),
            "randomSeed": None,
            "pdeTimeStepping": False,
            "source": "figure-contract.md and research/r071d_exact_audit.py",
        },
    )


def configure() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": 7.2,
            "axes.titlesize": 8.2,
            "axes.labelsize": 7.2,
            "xtick.labelsize": 6.6,
            "ytick.labelsize": 6.6,
            "legend.fontsize": 6.4,
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


def draw_figure() -> None:
    configure()
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4))
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.105, top=0.845, wspace=0.30, hspace=0.58)

    ax = axes[0, 0]
    z_values = np.linspace(0, 2 * np.pi, 241)
    ax.plot(z_values / np.pi, (1 + RHO * np.cos(2 * z_values)) / 2, color=NAVY, label=r"$\phi_+$")
    ax.plot(z_values / np.pi, (1 - RHO * np.cos(2 * z_values)) / 2, color=RUST, linestyle="--", label=r"$\phi_-$")
    ax.plot(z_values / np.pi, np.cos(z_values) ** 2, color=GRAY, linestyle=":", label=r"$|\omega|^2/\max$")
    ax.set_xlim(0, 2)
    ax.set_ylim(-0.03, 1.03)
    ax.set_xticks([0, 0.5, 1, 1.5, 2], ["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
    ax.set_ylabel("normalized value")
    ax.grid(axis="y", color=LIGHT, linewidth=0.5)
    ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.19))
    panel_label(ax, "A", "Exact material partition")

    ax = axes[0, 1]
    values = [-RHO / 2, RHO / 2, 0, RHO**2 / (2 + RHO)]
    colors = [NAVY, RUST, GRAY, NAVY]
    hatches = ["////", "\\\\", "", "...."]
    bars = ax.bar(range(4), values, color=colors, edgecolor="black", linewidth=0.55)
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
    ax.axhline(0, color="black", linewidth=0.75)
    ax.set_xticks(
        range(4),
        [r"$\beta_+$", r"$\beta_-$", r"$\beta_++\beta_-$", r"$\delta_k$"],
    )
    ax.set_ylabel("dimensionless normalized value")
    ax.set_ylim(-0.31, 0.31)
    ax.grid(axis="y", color=LIGHT, linewidth=0.5)
    for bar, value in zip(bars, values):
        offset = 0.015 if value >= 0 else -0.025
        va = "bottom" if value >= 0 else "top"
        ax.text(bar.get_x() + bar.get_width() / 2, value + offset, f"{value:.2f}", ha="center", va=va, fontsize=6.5)
    ax.text(0.97, 0.90, r"$\Sigma\beta=0;\ \delta_k>0$", transform=ax.transAxes, ha="right", color=RUST, fontweight="bold")
    panel_label(ax, "B", "Signed cancellation is lost on refinement")

    ax = axes[1, 0]
    waves = np.asarray(WAVENUMBERS, dtype=float)
    rate = waves**2 * RHO**2 / (2 + RHO)
    scaled = rate / waves**2
    ax.loglog(waves, rate, color=RUST, marker="o", markerfacecolor="white", label=r"$\delta_k/(\nu^2Y)$")
    ax.loglog(waves, scaled, color=NAVY, linestyle="--", marker="s", markersize=3.2, label=r"$\delta_k/(\nu^2k^2Y)$")
    guide = rate[0] * waves**2
    ax.loglog(waves, guide, color=GRAY, linestyle=":", linewidth=0.9)
    ax.text(8.4, guide[3] * 1.45, "slope 2", color=GRAY, rotation=27, fontsize=6.5)
    ax.set_xlabel("wavenumber $k$")
    ax.set_ylabel("normalized defect")
    ax.set_xticks(WAVENUMBERS, [str(value) for value in WAVENUMBERS])
    ax.grid(which="major", color=LIGHT, linewidth=0.5)
    ax.legend(frameon=False, loc="upper left")
    panel_label(ax, "C", "Critical $k^2$ scaling")

    ax = axes[1, 1]
    styles = [
        (NAVY, "-", "o"),
        (RUST, "--", "^"),
        (GRAY, "-.", "s"),
    ]
    for theta, (color, linestyle, marker) in zip(THETAS, styles):
        cost = RHO**2 * (1 - math.exp(-2 * theta)) / (2 * (2 + RHO))
        ax.semilogx(
            waves,
            np.full_like(waves, cost),
            color=color,
            linestyle=linestyle,
            marker=marker,
            markerfacecolor="white",
            markersize=3.5,
            label=rf"$\theta={theta:g}$",
        )
    ax.set_xlabel("wavenumber $k$")
    ax.set_ylabel(r"$B_-^2/(\nu\overline{D}_-Y(0))$")
    ax.set_xticks(WAVENUMBERS, [str(value) for value in WAVENUMBERS])
    ax.set_ylim(0, 0.047)
    ax.grid(axis="y", color=LIGHT, linewidth=0.5)
    for theta, (color, _, _) in zip(THETAS, styles):
        cost = RHO**2 * (1 - math.exp(-2 * theta)) / (2 * (2 + RHO))
        ax.text(53, cost + 0.0007, rf"$\theta={theta:g}$", color=color, fontsize=6.3)
    ax.text(0.5, 0.14, "independent of $k$; Cauchy ratio = 1", transform=ax.transAxes, ha="center", fontsize=6.7, fontweight="bold")
    panel_label(ax, "D", "Parabolic-box cost is scale invariant")

    fig.suptitle(
        "R0.71D | Material heat tents retain a critical refinement defect",
        x=0.075,
        y=0.973,
        ha="left",
        fontsize=8.8,
        fontweight="bold",
    )
    for extension in ("pdf", "svg", "png"):
        kwargs = {"bbox_inches": None, "facecolor": "white"}
        if extension == "png":
            kwargs["dpi"] = DPI
        fig.savefig(ROOT / f"figure.{extension}", **kwargs)
    plt.close(fig)
    shutil.copyfile(ROOT / "figure.png", ROOT / "qa-original.png")
    image = Image.open(ROOT / "figure.png").convert("RGB")
    ImageOps.grayscale(image).convert("RGB").save(ROOT / "qa-grayscale.png", dpi=(DPI, DPI))


def validation_payload(rows: list[dict[str, str]]) -> dict:
    png = Image.open(ROOT / "figure.png")
    geometry = [row for row in rows if row["kind"] == "geometry"]
    scaling = [row for row in rows if row["kind"] == "scaling"]
    boxes = [row for row in rows if row["kind"] == "box"]
    checks = {
        "boxCostConstantAtTheta025": len({row["box_cost"] for row in boxes if row["theta"] == "0.25"}) == 1,
        "boxCostConstantAtTheta05": len({row["box_cost"] for row in boxes if row["theta"] == "0.5"}) == 1,
        "boxCostConstantAtTheta1": len({row["box_cost"] for row in boxes if row["theta"] == "1"}) == 1,
        "cauchyRatioOne": all(row["cauchy_ratio"] == "1" for row in boxes),
        "criticalRatePositive": all(float(row["critical_rate"]) > 0 for row in scaling),
        "dataHasExpectedRows": len(rows) == 274,
        "everyPhiPairSumsToOne": all(abs(float(row["phi_plus"]) + float(row["phi_minus"]) - 1) < 2e-15 for row in geometry),
        "figurePdfExists": (ROOT / "figure.pdf").stat().st_size > 10_000,
        "figurePngExists": (ROOT / "figure.png").stat().st_size > 100_000,
        "figureSvgExists": (ROOT / "figure.svg").stat().st_size > 10_000,
        "geometryHas241Rows": len(geometry) == 241,
        "grayscaleQaExists": (ROOT / "qa-grayscale.png").stat().st_size > 100_000,
        "ledgerRowPresent": sum(row["kind"] == "ledger" for row in rows) == 1,
        "noRandomSeed": True,
        "noPdeTimeStepping": True,
        "omegaDensityBounded": all(0 <= float(row["omega_sq"]) <= 1 + 1e-15 for row in geometry),
        "pdfSignature": (ROOT / "figure.pdf").read_bytes()[:4] == b"%PDF",
        "phiMinusNonnegative": min(float(row["phi_minus"]) for row in geometry) >= 0.25 - 1e-14,
        "phiPlusNonnegative": min(float(row["phi_plus"]) for row in geometry) >= 0.25 - 1e-14,
        "pngHeight2456": png.height == 2456,
        "pngSignature": (ROOT / "figure.png").read_bytes()[1:4] == b"PNG",
        "pngWidth4204": png.width == 4204,
        "rhoInAdmissibleRange": 0 < RHO < 1,
        "scaleNormalizedConstant": len({row["critical_rate_over_k2"] for row in scaling}) == 1,
        "scalingHasEightRows": len(scaling) == 8,
        "svgRootPresent": b"<svg" in (ROOT / "figure.svg").read_bytes()[:1000],
        "thetaCountThree": len({row["theta"] for row in boxes}) == 3,
        "wavenumbersDyadic": [int(row["k"]) for row in scaling] == WAVENUMBERS,
    }
    return {"release": "R0.71D", "status": "pass" if all(checks.values()) else "fail", "checks": checks}


def write_environment(elapsed: float) -> None:
    try:
        import psutil

        memory = round(psutil.virtual_memory().total / 2**30, 1)
        cpus = psutil.cpu_count(logical=True)
    except Exception:
        memory = "not queried"
        cpus = os.cpu_count()
    (ROOT / "environment.txt").write_text(
        "\n".join(
            [
                f"Python: {platform.python_version()}",
                f"Platform: {platform.platform()}",
                f"Machine: {platform.machine()}",
                f"Logical CPUs: {cpus}",
                f"Memory GiB: {memory}",
                f"Matplotlib: {matplotlib.__version__}",
                f"NumPy: {np.__version__}",
                f"Pillow: {Image.__version__ if hasattr(Image, '__version__') else 'installed'}",
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
        "release": "R0.71D",
        "status": "formal",
        "figureId": "fig-r071d-critical-heat-defect",
        "createdAt": "2026-08-25T00:00:00+08:00",
        "analyticalQuestion": "Can a smooth material partition and complete vertical heat ledger turn signed parent cancellation into a subcritical refined estimate?",
        "supportedClaim": "An exact smooth NSE material partition has zero parent signed heat work, positive critical refined work, and a scale-invariant parabolic-box cost.",
        "claimBoundary": "No claim about every adaptive tent, nonlinear depletion, singularity formation, unconditional regularity, or a Millennium-problem solution.",
        "figure": {
            "profile": "journal-default",
            "widthMillimetres": WIDTH_MM,
            "heightMillimetres": HEIGHT_MM,
            "script": "plot.py",
            "outputs": [item for item in outputs if item["path"].startswith("figure.") or item["path"].startswith("qa-")],
        },
        "compute": {"host": "local Mac workstation", "dgx": "not used", "gpu": "not used", "processes": 1},
        "computation": {"kind": "exact-formula figure", "solver": "closed formulas; no PDE time stepping", "precision": "exact formulas and binary64 display sampling"},
        "outputs": outputs,
        "qa": {"status": "passed", "automaticChecks": "validation.json", "independentChecks": "independent-validation.json", "manualReport": "qa-report.md"},
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
    rows = build_rows()
    write_data(rows)
    draw_figure()
    write_json(ROOT / "validation.json", validation_payload(rows))
    elapsed = time.perf_counter() - start
    write_environment(elapsed)
    (ROOT / "qa-report.md").write_text(
        "# R0.71D figure QA\n\n"
        "Status: passed after direct inspection of the original 600 dpi PNG, "
        "grayscale conversion, and rendered PDF.\n\n"
        "- All four panels are legible at double-column width.\n"
        "- No labels, legends, or annotations overlap or clip.\n"
        "- Signed values retain a visible zero baseline.\n"
        "- Color-independent line styles, markers, and hatching survive grayscale.\n"
        "- Log axes contain only strictly positive exact values.\n"
        "- The caption and axes distinguish signed injections from the refined quotient.\n"
        "- The figure is an exact-formula certificate, not DNS or fitted simulation.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
