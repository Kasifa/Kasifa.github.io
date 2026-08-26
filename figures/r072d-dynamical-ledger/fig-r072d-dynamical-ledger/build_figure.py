#!/usr/bin/env python3
"""Build the formal R0.72D shifted-block dynamical-ledger figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import time
from zoneinfo import ZoneInfo

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def log(stage: str, **fields: object) -> None:
    row = {
        "timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"),
        "stage": stage,
        **fields,
    }
    with (ROOT / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, sort_keys=True) + "\n")


def binary_rudin_shapiro(count: int) -> np.ndarray:
    signs = np.empty(count, dtype=np.int8)
    for index in range(count):
        signs[index] = -1 if (index & (index >> 1)).bit_count() % 2 else 1
    return signs


def carrier_moment(count: int) -> int:
    return count * (2 * count - 1) * (7 * count - 1) // 6


def multiplier_norm(
    count: int, signs: np.ndarray, scaled_time: float, phase_points: int
) -> float:
    carriers = np.arange(count, 2 * count, dtype=int)
    weights = np.exp(-scaled_time * (carriers.astype(float) / count) ** 2)
    packed = np.zeros(phase_points, dtype=np.complex128)
    packed[carriers] = signs.astype(float) * weights
    values = np.fft.ifft(packed) * float(phase_points)
    # The common factor 2|K_z|a cancels in every plotted normalization.
    return float(np.max(np.abs(values.real)))


def mixed_exposure_proxy(
    count: int,
    signs: np.ndarray,
    phase_points: int,
    scaled_time_maximum: float,
    scaled_time_points: int,
) -> tuple[float, float]:
    scaled_time = np.linspace(0.0, scaled_time_maximum, scaled_time_points)
    carriers = np.arange(count, 2 * count, dtype=float)
    omega = np.asarray(
        [multiplier_norm(count, signs, float(s), phase_points) for s in scaled_time]
    )
    rho = np.sqrt(
        2.0
        * np.sum(
            np.exp(
                -2.0
                * scaled_time[:, None]
                * (carriers[None, :] / float(count)) ** 2
            ),
            axis=1,
        )
    )
    rho0 = math.sqrt(2.0 * count)
    omega0 = float(omega[0])
    truncated = float(np.trapezoid(rho * omega, scaled_time) / (rho0 * omega0))
    rs_prefix_constant = 2.0 + math.sqrt(2.0)
    # rho <= rho0 exp(-s), Omega <= C_RS sqrt(M) exp(-s).
    tail = float(
        rs_prefix_constant
        * math.sqrt(count)
        / omega0
        * math.exp(-2.0 * scaled_time_maximum)
        / 2.0
    )
    return truncated, tail


def rows_and_results(
    config: dict[str, object], producer: dict[str, object], independent: dict[str, object]
) -> tuple[list[dict[str, object]], dict[str, object]]:
    heat = config["heatPanel"]
    counts = [int(value) for value in heat["carrierCounts"]]
    plot_time = np.linspace(
        float(heat["scaledTimeMinimum"]),
        float(heat["scaledTimeMaximum"]),
        int(heat["scaledTimePoints"]),
    )
    phase_points = int(heat["phaseGridSize"])
    rows: list[dict[str, object]] = []
    exposure_rows: dict[int, dict[str, float]] = {}
    initial_values: dict[int, float] = {}

    for count in counts:
        signs = binary_rudin_shapiro(count)
        values = np.asarray(
            [multiplier_norm(count, signs, float(s), phase_points) for s in plot_time]
        ) / math.sqrt(count)
        initial_values[count] = float(values[0])
        for s_value, value in zip(plot_time, values, strict=True):
            rows.append(
                {
                    "panel": "A",
                    "series": f"M={count}",
                    "x": float(s_value),
                    "y": float(value),
                    "M": count,
                    "scaledTime": float(s_value),
                    "normalization": "||V_M||/(2|K_z|a*sqrt(M))",
                    "evidence": "deterministic FFT phase-grid sample",
                    "source": "direct shifted Rudin--Shapiro reconstruction",
                    "note": f"phaseGrid={phase_points}; r_j={count}+j",
                }
            )

        exposure, tail = mixed_exposure_proxy(
            count,
            signs,
            phase_points,
            float(heat["integrationScaledTimeMaximum"]),
            int(heat["integrationScaledTimePoints"]),
        )
        exposure_rows[count] = {
            "truncated": exposure,
            "analyticTailUpper": tail,
        }
        rows.append(
            {
                "panel": "B",
                "series": "scaled mixed-exposure grid proxy",
                "x": count,
                "y": exposure,
                "M": count,
                "scaledTime": "",
                "normalization": "M^2*ell_cross (s-grid proxy)",
                "evidence": "deterministic FFT grid plus declared omitted-tail bound",
                "source": "direct shifted Rudin--Shapiro reconstruction",
                "note": f"s<=16; analyticTailUpper={tail:.6e}",
            }
        )

    ode_rows = independent["finiteODE"]["rows"]
    expected_root_counts = [int(value) for value in config["rootPanel"]["expectedCarrierCounts"]]
    selected_ode = [row for row in ode_rows if int(row["M"]) in expected_root_counts]
    if [int(row["M"]) for row in selected_ode] != expected_root_counts:
        raise RuntimeError("independent finite-ODE rows do not match configured M values")

    root_specs = (
        (
            "interior-root slope ratio",
            "hTauAbsoluteOverH0",
            "|h(tau_M)|/(sqrt(2)|K_z|aM)",
        ),
        (
            "normalized root-atom proxy",
            "atomOverGammaFourThirds",
            "(atom/D^(1/3))/gamma^(4/3)",
        ),
        (
            "normalized full-charge proxy",
            "chargeOverGammaSquared",
            "fullChargeUpperModel/gamma^2",
        ),
    )
    for series, field, normalization in root_specs:
        for source_index, source_row in enumerate(selected_ode):
            rows.append(
                {
                    "panel": "B",
                    "series": series,
                    "x": int(source_row["M"]),
                    "y": float(source_row[field]),
                    "M": int(source_row["M"]),
                    "scaledTime": "",
                    "normalization": normalization,
                    "evidence": "independent finite-lattice DOP853 diagnostic",
                    "source": "research/certificates/r072d/independent-result.json",
                    "note": (
                        f"finiteODE.rows[{source_index}]; radius={source_row['radiusFactor']}M; "
                        f"relativeRootResidual={source_row['relativeRootResidual']:.3e}"
                    ),
                }
            )

    k_z = float(independent["parameters"]["Kz"])
    atom_limit = (9.0 * k_z**2 / 14.0) * (3.0 / 28.0) ** (1.0 / 3.0)
    reference_specs = (
        ("slope asymptotic reference", 1.0, "analytic M-to-infinity reference"),
        ("root-atom asymptotic reference", atom_limit, "analytic model reference"),
        ("full-charge asymptotic reference", 9.0 / 28.0, "exact moment reference"),
    )
    for series, value, evidence in reference_specs:
        for count in (min(counts), max(counts)):
            rows.append(
                {
                    "panel": "B",
                    "series": series,
                    "x": count,
                    "y": value,
                    "M": count,
                    "scaledTime": "",
                    "normalization": "dimensionless",
                    "evidence": evidence,
                    "source": "R0.72D analytic scale ledger",
                    "note": "reference level, not a fitted line",
                }
            )

    independent_heat = {
        int(row["M"]): row for row in independent["heatMultiplierFFT"]["rows"]
    }
    shared = sorted(set(counts).intersection(independent_heat))
    initial_cross_defects = []
    independent_k_z = float(independent["parameters"]["Kz"])
    independent_a = float(independent["parameters"]["a"])
    for count in shared:
        source_value = float(independent_heat[count]["initialMultiplierNorm"])
        normalized_source = source_value / (
            2.0 * abs(independent_k_z) * independent_a * math.sqrt(count)
        )
        initial_cross_defects.append(abs(initial_values[count] - normalized_source))

    results = {
        "schemaVersion": "r072d-figure-results-v1",
        "sourceStatus": {
            "producerAllPassed": bool(producer["allPassed"]),
            "independentAllPassed": bool(independent["allPassed"]),
        },
        "heatPanel": {
            "carrierCounts": counts,
            "scaledTimeRange": [float(plot_time[0]), float(plot_time[-1])],
            "scaledTimePoints": int(plot_time.size),
            "phaseGridSize": phase_points,
            "normalization": "||V_M||/(2|K_z|a*sqrt(M))",
            "sharedIndependentCounts": shared,
            "maximumInitialCrossAuditAbsoluteDefect": max(initial_cross_defects),
        },
        "mixedExposure": {
            "definition": "integral rho(s)Omega(s) ds /(rho(0)Omega(0)); equals M^2 ell_cross when s=M^2 x",
            "rows": {str(key): value for key, value in exposure_rows.items()},
            "scope": "finite phase-grid proxy on s<=16 plus a separate analytic tail upper bound",
        },
        "rootPanel": {
            "carrierCounts": expected_root_counts,
            "latticeRadiusFactor": int(config["rootPanel"]["finiteLatticeRadiusFactor"]),
            "maximumRelativeRootResidual": max(float(row["relativeRootResidual"]) for row in selected_ode),
            "minimumSlopeRatio": min(float(row["hTauAbsoluteOverH0"]) for row in selected_ode),
            "terminalSlopeRatio": float(selected_ode[-1]["hTauAbsoluteOverH0"]),
            "atomReference": atom_limit,
            "chargeReference": 9.0 / 28.0,
        },
        "rowCount": len(rows),
        "panelCounts": {
            "A": sum(row["panel"] == "A" for row in rows),
            "B": sum(row["panel"] == "B" for row in rows),
        },
        "randomness": False,
        "regressionUsedForPlottedClaim": False,
    }
    return rows, results


def write_data(rows: list[dict[str, object]], results: dict[str, object]) -> None:
    fields = [
        "panel",
        "series",
        "x",
        "y",
        "M",
        "scaledTime",
        "normalization",
        "evidence",
        "source",
        "note",
    ]
    with (ROOT / "data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def select(rows: list[dict[str, object]], panel: str, series: str) -> tuple[np.ndarray, np.ndarray]:
    selected = sorted(
        (row for row in rows if row["panel"] == panel and row["series"] == series),
        key=lambda row: float(row["x"]),
    )
    return (
        np.asarray([float(row["x"]) for row in selected]),
        np.asarray([float(row["y"]) for row in selected]),
    )


def configure(palette: dict[str, str]) -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 6.6,
            "axes.titlesize": 7.25,
            "axes.labelsize": 6.15,
            "xtick.labelsize": 5.35,
            "ytick.labelsize": 5.35,
            "legend.fontsize": 4.75,
            "axes.edgecolor": palette["ink"],
            "axes.labelcolor": palette["ink"],
            "text.color": palette["ink"],
            "xtick.color": palette["ink"],
            "ytick.color": palette["ink"],
            "axes.facecolor": palette["paper"],
            "figure.facecolor": palette["paper"],
            "savefig.facecolor": palette["paper"],
            "axes.linewidth": 0.65,
            "lines.linewidth": 1.05,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "r072d-dynamical-ledger",
        }
    )


def blossom(fig: plt.Figure, palette: dict[str, str]) -> None:
    center_x, center_y = 0.977, 0.952
    colors = (palette["navy"], palette["rust"], palette["teal"], palette["gray"], palette["navy"])
    for index, color in enumerate(colors):
        angle = 2.0 * np.pi * index / 5.0 + np.pi / 2.0
        fig.add_artist(
            Circle(
                (center_x + 0.0085 * np.cos(angle), center_y + 0.0085 * np.sin(angle)),
                0.0058,
                transform=fig.transFigure,
                facecolor=color,
                edgecolor=palette["paper"],
                linewidth=0.3,
                alpha=0.84,
                zorder=20,
            )
        )
    fig.add_artist(
        Circle(
            (center_x, center_y),
            0.0045,
            transform=fig.transFigure,
            facecolor=palette["ink"],
            edgecolor=palette["paper"],
            linewidth=0.3,
            zorder=21,
        )
    )


def render(rows: list[dict[str, object]], config: dict[str, object]) -> None:
    palette = config["palette"]
    configure(palette)
    figure_config = config["figure"]
    width = float(figure_config["widthMillimetres"]) / 25.4
    height = float(figure_config["heightMillimetres"]) / 25.4
    fig = plt.figure(figsize=(width, height), constrained_layout=False)
    grid = fig.add_gridspec(
        1,
        2,
        left=0.076,
        right=0.985,
        bottom=0.225,
        top=0.765,
        wspace=0.30,
        width_ratios=(1.08, 1.0),
    )
    axa, axb = [fig.add_subplot(grid[0, index]) for index in range(2)]

    fig.suptitle(
        "Shifted Rudin–Shapiro heat profile and root-ledger diagnostics",
        x=0.076,
        y=0.955,
        ha="left",
        fontsize=9.7,
        fontweight="bold",
    )
    fig.text(
        0.076,
        0.894,
        r"$r_j=M+j$  $\cdot$  $M=2^n$  $\cdot$  $\tau_M=M^{-3}$  $\cdot$  deterministic finite diagnostics",
        ha="left",
        fontsize=5.85,
        color=palette["gray"],
    )
    blossom(fig, palette)

    counts = [int(value) for value in config["heatPanel"]["carrierCounts"]]
    colors = [palette["navy"], palette["rust"], palette["teal"], palette["gray"], palette["ink"]]
    styles = ["-", "--", ":", "-.", (0, (4.5, 1.5, 1.0, 1.5))]
    markers = ["o", "s", "^", "D", "v"]
    for count, color, style, marker in zip(counts, colors, styles, markers, strict=True):
        x_value, y_value = select(rows, "A", f"M={count}")
        axa.plot(
            x_value,
            y_value,
            color=color,
            linestyle=style,
            marker=marker,
            markevery=20,
            markersize=2.5,
            markerfacecolor=palette["paper"] if count in (16, 64) else color,
            markeredgecolor=color,
            markeredgewidth=0.55,
            label=rf"$M={count}$",
        )
    axa.set_yscale("log")
    axa.set_xlim(0.0, float(config["heatPanel"]["scaledTimeMaximum"]))
    axa.set_ylim(1.0e-3, 2.0)
    axa.set_xticks([0, 1, 2, 3, 4, 5, 6])
    axa.set_xlabel(r"scaled heat time $s=M^2x$  ($x=\kappa t$)")
    axa.set_ylabel(r"$\|V_M(x)\|/(2|K_z|a\sqrt{M})$")
    axa.grid(True, which="major", color=palette["light"], linewidth=0.35)
    axa.grid(True, which="minor", axis="y", color=palette["light"], linewidth=0.2, alpha=0.42)
    axa.legend(loc="upper right", frameon=False, ncol=2, handlelength=2.3, columnspacing=0.7)
    axa.set_title("A   Heat-weighted multiplier collapse", loc="left", fontweight="bold", pad=4.0)
    axa.text(
        0.03,
        0.07,
        "32,768-point phase grid",
        transform=axa.transAxes,
        fontsize=4.85,
        color=palette["gray"],
    )

    panel_b_specs = (
        ("interior-root slope ratio", palette["navy"], "-", "o", r"slope $|h(\tau_M)|/h_0$"),
        ("scaled mixed-exposure grid proxy", palette["rust"], "--", "s", r"$M^2\ell_\times$ grid proxy"),
        ("normalized root-atom proxy", palette["teal"], "-.", "^", r"root atom$/\gamma^{4/3}$"),
        ("normalized full-charge proxy", palette["gray"], ":", "D", r"full charge$/\gamma^2$"),
    )
    for series, color, style, marker, label in panel_b_specs:
        x_value, y_value = select(rows, "B", series)
        axb.plot(
            x_value,
            y_value,
            color=color,
            linestyle=style,
            marker=marker,
            markersize=3.0,
            markerfacecolor=palette["paper"] if marker in ("s", "D") else color,
            markeredgecolor=color,
            markeredgewidth=0.65,
            label=label,
            zorder=4,
        )
    for series, label, offset in (
        ("slope asymptotic reference", r"$1$", 0.013),
        ("root-atom asymptotic reference", r"$C_{\rm atom}$", 0.012),
        ("full-charge asymptotic reference", r"$9/28$", -0.041),
    ):
        x_value, y_value = select(rows, "B", series)
        axb.plot(x_value, y_value, color=palette["ink"], linestyle=(0, (2, 2)), linewidth=0.48, alpha=0.60, zorder=1)
        axb.text(132, float(y_value[-1]) + offset, label, ha="right", fontsize=4.6, color=palette["ink"])
    axb.set_xscale("log", base=2)
    axb.set_xlim(7.2, 145)
    axb.set_ylim(0.0, 1.08)
    axb.set_xticks(counts)
    axb.set_xticklabels([str(value) for value in counts])
    axb.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
    axb.set_xlabel(r"carrier count $M$  (log base 2)")
    axb.set_ylabel("dimensionless diagnostic")
    axb.grid(True, color=palette["light"], linewidth=0.35)
    axb.legend(loc="upper left", frameon=False, ncol=1, handlelength=2.2, labelspacing=0.25)
    axb.set_title("B   Interior root and complete-ledger scales", loc="left", fontweight="bold", pad=4.0)
    axb.text(
        0.97,
        0.055,
        r"finite ODE radius $6M$",
        transform=axb.transAxes,
        ha="right",
        fontsize=4.85,
        color=palette["gray"],
    )

    fig.text(
        0.076,
        0.091,
        "FFT grids and finite-lattice roots corroborate the theorem; they are not interval proofs, PDE DNS, or a Navier–Stokes endpoint result.",
        ha="left",
        fontsize=4.9,
        color=palette["gray"],
    )
    fig.text(0.985, 0.091, "R0.72D-1", ha="right", fontsize=5.1, color=palette["gray"])

    metadata = {"Creator": "R0.72D deterministic figure workflow", "Date": None}
    output = ROOT / "figure"
    fig.savefig(output.with_suffix(".pdf"), metadata=metadata, bbox_inches=None)
    fig.savefig(output.with_suffix(".svg"), metadata=metadata, bbox_inches=None)
    fig.savefig(
        output.with_suffix(".png"),
        dpi=int(figure_config["pngDpi"]),
        metadata={"Software": "R0.72D deterministic figure workflow"},
        bbox_inches=None,
    )
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config.json")
    args = parser.parse_args()
    config_path = args.config if args.config.is_absolute() else Path.cwd() / args.config
    if not config_path.exists():
        config_path = ROOT / args.config
    config = load_json(config_path)
    producer_path = REPOSITORY / config["sourceCertificates"]["producer"]
    independent_path = REPOSITORY / config["sourceCertificates"]["independent"]
    producer = load_json(producer_path)
    independent = load_json(independent_path)
    if not bool(producer["allPassed"]) or not bool(independent["allPassed"]):
        raise RuntimeError("source R0.72D certificate did not pass")

    started = time.perf_counter()
    (ROOT / "progress.ndjson").write_text("", encoding="utf-8")
    log("figure-build-start", randomness=False)
    rows, results = rows_and_results(config, producer, independent)
    write_data(rows, results)
    log("figure-data-complete", rowCount=len(rows), panelCounts=results["panelCounts"])
    render(rows, config)
    log("figure-render-complete", outputs=["figure.pdf", "figure.svg", "figure.png"])

    contract_path = ROOT / "contract.json"
    metadata = {
        "schemaVersion": "r072d-figure-data-metadata-v1",
        "generatedAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "sourceFiles": [
            {"path": str(path.relative_to(REPOSITORY)), "sha256": sha256(path)}
            for path in (producer_path, independent_path, contract_path, config_path)
        ],
        "dataFiles": {name: sha256(ROOT / name) for name in ("data.csv", "results.json")},
        "rowCount": len(rows),
        "randomness": False,
        "claimBoundary": load_json(contract_path)["claimBoundary"],
    }
    (ROOT / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    elapsed = time.perf_counter() - started
    log("figure-build-complete", elapsedSeconds=elapsed)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    resource_row = {
        "timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"),
        "stage": "figure-build-complete",
        "elapsedSeconds": elapsed,
        "processUserCpuSeconds": usage.ru_utime,
        "processSystemCpuSeconds": usage.ru_stime,
        "maximumResidentSetRaw": usage.ru_maxrss,
        "logicalCpuCount": os.cpu_count(),
        "gpu": False,
        "dgx": False,
    }
    (ROOT / "resource-log.ndjson").write_text(
        json.dumps(resource_row, sort_keys=True) + "\n", encoding="utf-8"
    )
    environment = (
        f"generatedAt={datetime.now(TIMEZONE).isoformat(timespec='seconds')}\n"
        f"python={platform.python_version()}\n"
        f"platform={platform.platform()}\n"
        f"numpy={np.__version__}\n"
        f"matplotlib={mpl.__version__}\n"
        "randomness=false\nintervalArithmetic=false\ngpu=false\ndgx=false\n"
    )
    (ROOT / "environment.txt").write_text(environment, encoding="utf-8")
    print(f"R0.72D figure build passed in {elapsed:.2f}s; rows={len(rows)}")


if __name__ == "__main__":
    main()
