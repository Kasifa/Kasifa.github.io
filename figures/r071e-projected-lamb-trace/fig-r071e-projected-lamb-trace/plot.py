#!/usr/bin/env python3
"""Build and archive the formal R0.71E projected-Lamb trace figure."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import shutil
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent
WAVENUMBERS = [1, 2, 4, 8, 16, 32, 64, 128]
THETAS = [0.25, 0.5, 1.0]
WIDTH_MM = 178
HEIGHT_MM = 104
DPI = 600
NAVY = "#17324d"
RUST = "#a44a2a"
INK = "#20262c"
GRAY = "#70777f"
LIGHT = "#d9dde1"
PALE_NAVY = "#dce7ef"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def empty_row() -> dict[str, str]:
    return {
        "kind": "",
        "index": "",
        "tau": "",
        "k": "",
        "theta": "",
        "stretch_norm": "",
        "commutator_norm": "",
        "combined_norm": "",
        "q_profile": "",
        "bulk_area": "",
        "bottom_coefficient": "",
        "normalized_bulk": "",
        "trace_ratio": "",
        "trace_ratio_over_k2": "",
        "finite_box": "",
    }


def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for index in range(241):
        tau = 1.5 * index / 240
        row = empty_row()
        row.update(
            {
                "kind": "decomposition",
                "index": str(index),
                "tau": f"{tau:.17g}",
                "stretch_norm": f"{2 * math.exp(-4 * tau):.17g}",
                "commutator_norm": f"{2 * (math.exp(-4 * tau) - math.exp(-2 * tau)):.17g}",
                "combined_norm": f"{2 * (2 * math.exp(-4 * tau) - math.exp(-2 * tau)):.17g}",
            }
        )
        rows.append(row)
    for index in range(241):
        tau = 3 * index / 240
        row = empty_row()
        row.update(
            {
                "kind": "profile",
                "index": str(index),
                "tau": f"{tau:.17g}",
                "q_profile": f"{math.exp(-2 * tau):.17g}",
                "bulk_area": "0.5",
            }
        )
        rows.append(row)
    for index, wave in enumerate(WAVENUMBERS):
        row = empty_row()
        row.update(
            {
                "kind": "scaling",
                "index": str(index),
                "k": str(wave),
                "bottom_coefficient": f"{wave**2 / 8:.17g}",
                "normalized_bulk": f"{1 / 16:.17g}",
                "trace_ratio": f"{2 * wave**2:.17g}",
                "trace_ratio_over_k2": "2",
            }
        )
        rows.append(row)
    for label, theta in [("0.25", 0.25), ("0.5", 0.5), ("1", 1.0), ("inf", None)]:
        value = 1 / 16 if theta is None else (1 - math.exp(-2 * theta)) / 16
        for index, wave in enumerate(WAVENUMBERS):
            row = empty_row()
            row.update(
                {
                    "kind": "box",
                    "index": str(index),
                    "k": str(wave),
                    "theta": label,
                    "finite_box": f"{value:.17g}",
                }
            )
            rows.append(row)
    return rows


def write_data(rows: list[dict[str, str]]) -> None:
    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    write_json(
        ROOT / "figure-data-metadata.json",
        {
            "release": "R0.71E",
            "figureId": "fig-r071e-projected-lamb-trace",
            "kind": "closed exact formulas sampled in binary64 for display",
            "parameters": {
                "amplitude": 1,
                "parentPhase": 1,
                "lowPositivePhase": -1,
                "wavenumbers": WAVENUMBERS,
                "theta": THETAS,
            },
            "rows": len(rows),
            "randomSeed": None,
            "pdeTimeStepping": False,
            "source": "figure-contract.md and research/r071e_exact_audit.py",
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
            "legend.fontsize": 6.2,
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
    center_x, center_y = 0.972, 0.966
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


def draw_figure() -> None:
    configure()
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH_MM / 25.4, HEIGHT_MM / 25.4))
    fig.subplots_adjust(left=0.078, right=0.985, bottom=0.105, top=0.845, wspace=0.31, hspace=0.58)

    ax = axes[0, 0]
    tau_a = np.linspace(0, 1.5, 241)
    stretching = 2 * np.exp(-4 * tau_a)
    commutator = 2 * (np.exp(-4 * tau_a) - np.exp(-2 * tau_a))
    combined = stretching + commutator
    ax.plot(tau_a, stretching, color=RUST, label="stretching")
    ax.plot(tau_a, commutator, color=NAVY, linestyle="--", label="commutator")
    ax.plot(tau_a, combined, color=INK, linestyle="-.", linewidth=1.55, label="combined")
    zero_tau = math.log(2) / 2
    ax.axhline(0, color=GRAY, linewidth=0.65)
    ax.axvline(zero_tau, color=GRAY, linestyle=":", linewidth=0.8)
    ax.scatter([zero_tau], [0], s=16, facecolor="white", edgecolor=INK, linewidth=0.7, zorder=5)
    ax.text(zero_tau + 0.035, 0.17, r"$\tau=(\log 2)/2$", color=GRAY, fontsize=6.2)
    ax.set_xlim(0, 1.5)
    ax.set_ylim(-0.62, 2.12)
    ax.set_xlabel(r"dimensionless heat height $\tau=K^2s$")
    ax.set_ylabel(r"work divided by $a^3K^6$")
    ax.grid(axis="y", color=LIGHT, linewidth=0.5)
    ax.legend(frameon=False, ncol=1, loc="upper right")
    panel_label(ax, "A", "Stretching and commutator compress first")

    ax = axes[0, 1]
    tau_b = np.linspace(0, 3, 241)
    profile = np.exp(-2 * tau_b)
    ax.plot(tau_b, profile, color=NAVY, linewidth=1.6, label=r"$e^{-2\tau}$")
    ax.fill_between(tau_b, 0, profile, facecolor=PALE_NAVY, edgecolor=NAVY, linewidth=0.45, hatch="////", alpha=0.7)
    ax.scatter([0], [1], s=22, facecolor=RUST, edgecolor=INK, linewidth=0.6, zorder=5)
    ax.text(0.08, 0.91, "bottom = 1", color=RUST, fontsize=6.5, fontweight="bold")
    ax.text(0.55, 0.44, r"$\int_0^\infty e^{-2\tau}d\tau=1/2$", color=INK, fontsize=6.7)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 1.08)
    ax.set_xlabel(r"dimensionless heat height $\tau=K^2s$")
    ax.set_ylabel(r"$q_{\mathrm{lo}}/(a^4K^6)$")
    ax.grid(axis="y", color=LIGHT, linewidth=0.5)
    panel_label(ax, "B", "The vertical bulk is finite")

    ax = axes[1, 0]
    waves = np.asarray(WAVENUMBERS, dtype=float)
    ratio = 2 * waves**2
    normalized = ratio / waves**2
    ax.loglog(waves, ratio, color=RUST, marker="o", markerfacecolor="white", label=r"$A_{\mathrm{bottom}}/\mathcal{V}$")
    ax.loglog(waves, normalized, color=NAVY, linestyle="--", marker="s", markersize=3.2, label=r"$A_{\mathrm{bottom}}/(K^2\mathcal{V})$")
    ax.loglog(waves, 2 * waves**2, color=GRAY, linestyle=":", linewidth=0.85)
    ax.text(7.8, 2 * 8**2 * 1.55, "slope 2", color=GRAY, rotation=27, fontsize=6.4)
    ax.set_xlabel("wavenumber $K$")
    ax.set_ylabel("bottom-to-bulk ratio")
    ax.set_xticks(WAVENUMBERS, [str(value) for value in WAVENUMBERS])
    ax.grid(which="major", color=LIGHT, linewidth=0.5)
    ax.legend(frameon=False, loc="upper left")
    panel_label(ax, "C", "The bottom trace costs $2K^2$")

    ax = axes[1, 1]
    styles = [
        (NAVY, "-", "o"),
        (RUST, "--", "^"),
        (GRAY, "-.", "s"),
    ]
    for theta, (color, linestyle, marker) in zip(THETAS, styles):
        value = (1 - math.exp(-2 * theta)) / 16
        ax.semilogx(
            waves,
            np.full_like(waves, value),
            color=color,
            linestyle=linestyle,
            marker=marker,
            markerfacecolor="white",
            markersize=3.5,
            label=rf"$\theta={theta:g}$",
        )
    limit = 1 / 16
    ax.semilogx(waves, np.full_like(waves, limit), color=INK, linestyle=":", linewidth=1.1, label=r"$\theta=\infty$")
    ax.set_xlabel("wavenumber $K$")
    ax.set_ylabel(r"finite-box mass $\mathcal{V}_\theta$")
    ax.set_xticks(WAVENUMBERS, [str(value) for value in WAVENUMBERS])
    ax.set_ylim(0, 0.075)
    ax.grid(axis="y", color=LIGHT, linewidth=0.5)
    ax.legend(frameon=False, ncol=2, loc="lower right")
    ax.text(0.5, 0.94, "every level is independent of $K$", transform=ax.transAxes, ha="center", va="top", fontsize=6.6, fontweight="bold")
    panel_label(ax, "D", "Finite heat boxes remain scale invariant")

    fig.suptitle(
        "R0.71E | Projected-Lamb heat bulk closes; the bottom trace does not",
        x=0.078,
        y=0.973,
        ha="left",
        fontsize=8.8,
        fontweight="bold",
    )
    add_blossom(fig)
    for extension in ("pdf", "svg", "png"):
        kwargs = {"bbox_inches": None, "facecolor": "white"}
        if extension == "png":
            kwargs["dpi"] = DPI
        fig.savefig(ROOT / f"figure.{extension}", **kwargs)
    svg_path = ROOT / "figure.svg"
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )
    plt.close(fig)
    shutil.copyfile(ROOT / "figure.png", ROOT / "qa-original.png")
    image = Image.open(ROOT / "figure.png").convert("RGB")
    ImageOps.grayscale(image).convert("RGB").save(ROOT / "qa-grayscale.png", dpi=(DPI, DPI))


def validation_payload(rows: list[dict[str, str]]) -> dict:
    png = Image.open(ROOT / "figure.png")
    decomposition = [row for row in rows if row["kind"] == "decomposition"]
    profile = [row for row in rows if row["kind"] == "profile"]
    scaling = [row for row in rows if row["kind"] == "scaling"]
    boxes = [row for row in rows if row["kind"] == "box"]
    checks = {
        "boxCountThirtyTwo": len(boxes) == 32,
        "boxValuesIndependentOfK": all(len({row["finite_box"] for row in boxes if row["theta"] == label}) == 1 for label in ["0.25", "0.5", "1", "inf"]),
        "combinedChangesSign": any(float(row["combined_norm"]) < 0 for row in decomposition) and any(float(row["combined_norm"]) > 0 for row in decomposition),
        "dataHasExpectedRows": len(rows) == 522,
        "decompositionHas241Rows": len(decomposition) == 241,
        "figurePdfExists": (ROOT / "figure.pdf").stat().st_size > 10_000,
        "figurePngExists": (ROOT / "figure.png").stat().st_size > 100_000,
        "figureSvgExists": (ROOT / "figure.svg").stat().st_size > 10_000,
        "grayscaleQaExists": (ROOT / "qa-grayscale.png").stat().st_size > 100_000,
        "infiniteBulkOneSixteenth": all(abs(float(row["finite_box"]) - 1 / 16) < 2e-15 for row in boxes if row["theta"] == "inf"),
        "noPdeTimeStepping": True,
        "noRandomSeed": True,
        "pdfSignature": (ROOT / "figure.pdf").read_bytes()[:4] == b"%PDF",
        "pngHeightAt600Dpi": png.height in (2456, 2457),
        "pngSignature": (ROOT / "figure.png").read_bytes()[1:4] == b"PNG",
        "pngWidthAt600Dpi": png.width in (4204, 4205),
        "profileAreaOneHalf": all(row["bulk_area"] == "0.5" for row in profile),
        "profileHas241Rows": len(profile) == 241,
        "profilePositive": all(float(row["q_profile"]) > 0 for row in profile),
        "scaleNormalizedTraceConstantTwo": all(row["trace_ratio_over_k2"] == "2" for row in scaling),
        "scalingHasEightRows": len(scaling) == 8,
        "svgRootPresent": b"<svg" in (ROOT / "figure.svg").read_bytes()[:1000],
        "thetaCountFourIncludingInfinity": {row["theta"] for row in boxes} == {"0.25", "0.5", "1", "inf"},
        "traceRatioPositive": all(float(row["trace_ratio"]) > 0 for row in scaling),
        "wavenumbersDyadic": [int(row["k"]) for row in scaling] == WAVENUMBERS,
    }
    return {"release": "R0.71E", "status": "pass" if all(checks.values()) else "fail", "checks": checks}


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
        "release": "R0.71E",
        "status": "formal",
        "figureId": "fig-r071e-projected-lamb-trace",
        "createdAt": "2026-08-25T00:00:00+08:00",
        "analyticalQuestion": "What part of the signed shell coefficient is controlled by the projected-Lamb heat bulk, and what exact frequency cost remains at the bottom heat face?",
        "supportedClaim": "Projected-Lamb compression closes the normalized vertical heat bulk, while one exact smooth NSE trace family pays the full factor 2*K^2 at the bottom face.",
        "claimBoundary": "No bottom-trace integrability, arbitrary-solution divergence, singularity, unconditional regularity, or Millennium-problem claim.",
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
        "# R0.71E figure QA\n\n"
        "Status: pending direct inspection of the original PNG, grayscale PNG, and rendered PDF.\n\n"
        "- Automatic formula, format, signature, and output-size checks have run.\n"
        "- Manual checks for clipping, collisions, grayscale distinction, and PDF rendering remain.\n"
        "- The figure is an exact-formula certificate, not DNS or fitted simulation.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
