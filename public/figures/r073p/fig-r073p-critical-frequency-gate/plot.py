#!/usr/bin/env python3
"""Generate the R0.73P formula data and optionally render the figure.

The default and ``--data-only`` paths cannot export a figure.  The
``--render-nonpdf`` path exports SVG and PNG only.  PDF export is isolated
behind ``--render-final`` so the non-PDF preflight can be audited directly.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
from importlib.metadata import PackageNotFoundError, version as package_version
import json
import math
import os
import platform
from pathlib import Path
import resource
import subprocess
import sys
import time
from typing import Any


def bootstrap() -> None:
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()

HERE = Path(__file__).resolve().parent
START = time.monotonic()
PDF_ASSETS = (HERE / "figure.pdf", HERE / "qa-pdf.png")
CSV_FIELDS = (
    "record_type",
    "sample_index",
    "N",
    "h3_threshold",
    "hhalf_threshold",
    "gamma",
    "l2_power",
    "hhalf_power",
    "h3_power",
    "tau",
    "discrete_heat",
    "continuous_heat_bound",
    "discrete_to_continuous",
    "maximizer_norm_squared",
    "k1",
    "k2",
    "k3",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--data-only", action="store_true")
    modes.add_argument("--render-nonpdf", action="store_true")
    modes.add_argument("--render-final", action="store_true")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("JSON root is not an object: " + str(path))
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


def total_memory_gib() -> float | None:
    if sys.platform == "darwin":
        try:
            output = subprocess.check_output(
                ["/usr/sbin/sysctl", "-n", "hw.memsize"], text=True
            ).strip()
            return int(output) / (1024.0**3)
        except (OSError, subprocess.SubprocessError, ValueError):
            return None
    meminfo = Path("/proc/meminfo")
    if meminfo.is_file():
        for line in meminfo.read_text(encoding="utf-8").splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) / (1024.0**2)
    return None


def installed_version(name: str) -> str | None:
    try:
        return package_version(name)
    except PackageNotFoundError:
        return None


class Monitor:
    def __init__(self) -> None:
        self.progress = HERE / "progress.ndjson"
        self.resources = HERE / "resource-log.ndjson"
        self.progress.write_text("", encoding="utf-8")
        self.resources.write_text("", encoding="utf-8")

    def event(self, stage: str, **fields: object) -> None:
        now = utc_now()
        elapsed = time.monotonic() - START
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(canonical({
                "stage": stage,
                "timestampUtc": now,
                "elapsedSeconds": elapsed,
                **fields,
            }).replace("\n", "") + "\n")
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(canonical({
                "stage": stage,
                "timestampUtc": now,
                "elapsedSeconds": elapsed,
                "maximumResidentSetMiB": rss_mib(),
                "processes": 1,
                "threadsPerProcess": 1,
                "gpu": "not used",
                "executionHost": platform.node(),
            }).replace("\n", "") + "\n")


def log_grid(minimum: float, maximum: float, count: int) -> list[float]:
    if not (minimum > 0.0 and maximum > minimum and count >= 2):
        raise RuntimeError("invalid logarithmic grid")
    lo = math.log(minimum)
    hi = math.log(maximum)
    return [math.exp(lo + (hi - lo) * index / (count - 1)) for index in range(count)]


def linear_grid(minimum: float, maximum: float, count: int) -> list[float]:
    if not (maximum > minimum and count >= 2):
        raise RuntimeError("invalid linear grid")
    return [minimum + (maximum - minimum) * index / (count - 1) for index in range(count)]


def frequency_grid(settings: dict[str, Any]) -> list[int]:
    raw = log_grid(
        float(settings["minimumFrequency"]),
        float(settings["maximumFrequency"]),
        int(settings["logSamples"]),
    )
    values = {int(round(value)) for value in raw}
    values.add(int(settings["minimumFrequency"]))
    values.add(int(settings["maximumFrequency"]))
    return sorted(values)


def lattice_radii(half_width: int) -> dict[int, tuple[int, int, int]]:
    """Return one nonnegative vector for every three-square radius n<=K^2."""
    if half_width < 1:
        raise RuntimeError("lattice half-width must be positive")
    cutoff = half_width * half_width
    representatives: dict[int, tuple[int, int, int]] = {}
    for i in range(half_width + 1):
        i2 = i * i
        for j in range(half_width + 1):
            ij2 = i2 + j * j
            if ij2 > cutoff:
                break
            k_max = math.isqrt(cutoff - ij2)
            for k in range(k_max + 1):
                n = ij2 + k * k
                if n and n not in representatives:
                    representatives[n] = (i, j, k)
    if cutoff not in representatives:
        raise RuntimeError("lattice cutoff radius is not represented")
    return representatives


def heat_value(norm_squared: int, tau: float) -> float:
    return norm_squared**1.5 * math.exp(-tau * norm_squared)


def generate_rows(config: dict[str, Any], monitor: Monitor) -> tuple[list[dict[str, str]], dict[str, Any]]:
    rows: list[dict[str, str]] = []
    panel_a = config["panelA"]
    h3_radius = float(panel_a["normalizedH3Radius"])
    critical_radius = float(panel_a["normalizedCriticalRadius"])
    frequencies = frequency_grid(panel_a)
    for index, frequency in enumerate(frequencies):
        row = {field: "" for field in CSV_FIELDS}
        row.update({
            "record_type": "threshold",
            "sample_index": str(index),
            "N": str(frequency),
            "h3_threshold": format(h3_radius * frequency ** -3.0, ".17g"),
            "hhalf_threshold": format(critical_radius * frequency ** -0.5, ".17g"),
        })
        rows.append(row)
    monitor.event("panel-a-data", rowCount=len(frequencies))

    panel_b = config["panelB"]
    gammas = linear_grid(
        float(panel_b["minimumGamma"]),
        float(panel_b["maximumGamma"]),
        int(panel_b["samples"]),
    )
    for index, gamma in enumerate(gammas):
        row = {field: "" for field in CSV_FIELDS}
        row.update({
            "record_type": "sobolev_power",
            "sample_index": str(index),
            "gamma": format(gamma, ".17g"),
            "l2_power": format(-gamma, ".17g"),
            "hhalf_power": format(0.5 - gamma, ".17g"),
            "h3_power": format(3.0 - gamma, ".17g"),
        })
        rows.append(row)
    monitor.event("panel-b-data", rowCount=len(gammas))

    panel_c = config["panelC"]
    minimum_tau = float(panel_c["minimumTau"])
    half_width = int(panel_c["latticeHalfWidth"])
    radii = lattice_radii(half_width)
    taus = log_grid(minimum_tau, float(panel_c["maximumTau"]), int(panel_c["logSamples"]))
    radius_values = sorted(radii)
    ratios: list[float] = []
    maximizing_radii: list[int] = []
    for index, tau in enumerate(taus):
        best_n = max(radius_values, key=lambda n: heat_value(n, tau))
        discrete = heat_value(best_n, tau)
        continuous = (3.0 / (2.0 * math.e * tau)) ** 1.5
        ratio = discrete / continuous
        k1, k2, k3 = radii[best_n]
        row = {field: "" for field in CSV_FIELDS}
        row.update({
            "record_type": "heat_lattice",
            "sample_index": str(index),
            "tau": format(tau, ".17g"),
            "discrete_heat": format(discrete, ".17g"),
            "continuous_heat_bound": format(continuous, ".17g"),
            "discrete_to_continuous": format(ratio, ".17g"),
            "maximizer_norm_squared": str(best_n),
            "k1": str(k1),
            "k2": str(k2),
            "k3": str(k3),
        })
        rows.append(row)
        ratios.append(ratio)
        maximizing_radii.append(best_n)
    monitor.event(
        "panel-c-data",
        rowCount=len(taus),
        representableRadii=len(radii),
        latticeHalfWidth=half_width,
    )

    cutoff_squared = half_width * half_width
    continuous_peak_at_minimum_tau = 3.0 / (2.0 * minimum_tau)
    facts = {
        "panelA": {
            "rowCount": len(frequencies),
            "minimumFrequency": min(frequencies),
            "maximumFrequency": max(frequencies),
            "maximumH3NormalizationError": max(
                abs((h3_radius * n ** -3.0) * n**3 / h3_radius - 1.0)
                for n in frequencies
            ),
            "maximumCriticalNormalizationError": max(
                abs((critical_radius * n ** -0.5) * n**0.5 / critical_radius - 1.0)
                for n in frequencies
            ),
        },
        "panelB": {
            "rowCount": len(gammas),
            "criticalBoundary": float(panel_b["criticalIndex"]),
            "highBoundary": float(panel_b["highIndex"]),
            "openStrip": [float(panel_b["criticalIndex"]), float(panel_b["highIndex"])],
            "endpointPrefactorConditionRetained": True,
        },
        "panelC": {
            "rowCount": len(taus),
            "representableRadiusCountThroughCutoff": len(radii),
            "latticeHalfWidth": half_width,
            "cutoffNormSquared": cutoff_squared,
            "continuousPeakNormSquaredAtMinimumTau": continuous_peak_at_minimum_tau,
            "tailStrictlyDecreasing": cutoff_squared > continuous_peak_at_minimum_tau,
            "minimumDiscreteToContinuousRatio": min(ratios),
            "maximumDiscreteToContinuousRatio": max(ratios),
            "allDiscreteValuesBelowContinuousBound": max(ratios) <= 1.0 + 2e-15,
            "minimumMaximizerNormSquared": min(maximizing_radii),
            "maximumMaximizerNormSquared": max(maximizing_radii),
        },
    }
    return rows, facts


def write_source_data(rows: list[dict[str, str]]) -> None:
    with (HERE / "source-data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def configure_style(mpl: Any, palette: dict[str, str]) -> None:
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 6.7,
        "axes.titlesize": 7.8,
        "axes.labelsize": 6.4,
        "axes.edgecolor": palette["midGrey"],
        "axes.linewidth": 0.65,
        "axes.facecolor": palette["paper"],
        "figure.facecolor": palette["paper"],
        "savefig.facecolor": palette["paper"],
        "xtick.labelsize": 5.4,
        "ytick.labelsize": 5.4,
        "xtick.color": palette["ink"],
        "ytick.color": palette["ink"],
        "text.color": palette["ink"],
        "axes.labelcolor": palette["ink"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "lines.solid_capstyle": "round",
    })


def panel_heading(ax: Any, letter: str, title: str) -> None:
    ax.text(-0.12, 1.085, letter, transform=ax.transAxes, fontsize=9.1,
            fontweight="bold", va="bottom")
    ax.text(-0.015, 1.085, title, transform=ax.transAxes, fontsize=7.2,
            fontweight="bold", va="bottom")


def render(rows: list[dict[str, str]], config: dict[str, Any], *, include_pdf: bool) -> None:
    import matplotlib as mpl  # type: ignore

    mpl.use("Agg")
    import matplotlib.pyplot as plt  # type: ignore
    from PIL import Image, ImageOps  # type: ignore

    palette = config["palette"]
    configure_style(mpl, palette)
    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    fig, axes = plt.subplots(1, 3, figsize=(width, height))
    fig.subplots_adjust(left=0.066, right=0.988, bottom=0.205, top=0.72, wspace=0.40)
    fig.text(0.055, 0.935, "R0.73P | critical-frequency gate",
             fontsize=10.7, fontweight="bold", color=palette["blueDark"])
    fig.text(
        0.055, 0.868,
        "Closed formulas and exact lattice enumeration · not a Navier–Stokes simulation",
        fontsize=6.7, color=palette["midGrey"],
    )

    threshold = [row for row in rows if row["record_type"] == "threshold"]
    sobolev = [row for row in rows if row["record_type"] == "sobolev_power"]
    heat = [row for row in rows if row["record_type"] == "heat_lattice"]

    ax = axes[0]
    frequencies = [int(row["N"]) for row in threshold]
    h3 = [float(row["h3_threshold"]) for row in threshold]
    hhalf = [float(row["hhalf_threshold"]) for row in threshold]
    mark_every = max(1, len(frequencies) // 9)
    ax.loglog(frequencies, h3, color=palette["blueDark"], lw=1.65,
              marker="o", ms=2.2, markevery=mark_every,
              label=r"direct $H^3$: $N^{-3}$")
    ax.loglog(frequencies, hhalf, color=palette["gold"], lw=1.45, ls="--",
              marker="s", mfc=palette["paper"], ms=2.2, markevery=mark_every,
              label=r"critical $\dot H^{1/2}$: $N^{-1/2}$")
    ax.fill_between(frequencies, h3, hhalf, color=palette["blueLight"], alpha=0.16)
    ax.set_xlim(min(frequencies), max(frequencies))
    ax.set_ylim(3e-16, 2.0)
    ax.set_xlabel("Fourier cutoff $N$")
    ax.set_ylabel("normalized $L^2$ amplitude threshold")
    ax.grid(which="major", color=palette["lightGrey"], lw=0.45, alpha=0.85)
    ax.legend(frameon=False, fontsize=5.2, loc="lower left", handlelength=2.5)
    ax.text(
        0.96, 0.94, r"gap $=N^{5/2}$", transform=ax.transAxes,
        ha="right", va="top", fontsize=5.7, color=palette["midGrey"],
        bbox={"boxstyle": "round,pad=0.22", "fc": palette["paper"],
              "ec": palette["lightGrey"], "lw": 0.5},
    )
    panel_heading(ax, "A", "Normalized frequency penalties")

    ax = axes[1]
    gamma = [float(row["gamma"]) for row in sobolev]
    l2_power = [float(row["l2_power"]) for row in sobolev]
    hhalf_power = [float(row["hhalf_power"]) for row in sobolev]
    h3_power = [float(row["h3_power"]) for row in sobolev]
    lower = float(config["panelB"]["criticalIndex"])
    upper = float(config["panelB"]["highIndex"])
    ax.axvspan(lower, upper, facecolor=palette["blueLight"], alpha=0.15,
               hatch="////", edgecolor=palette["midGrey"], linewidth=0.0)
    ax.plot(gamma, h3_power, color=palette["blueDark"], lw=1.55,
            label=r"$\dot H^3$: $3-\gamma$")
    ax.plot(gamma, hhalf_power, color=palette["gold"], lw=1.4, ls="--",
            label=r"$\dot H^{1/2}$: $1/2-\gamma$")
    ax.plot(gamma, l2_power, color=palette["midGrey"], lw=1.2, ls=":",
            label=r"$L^2$: $-\gamma$")
    ax.axhline(0.0, color=palette["ink"], lw=0.65)
    ax.axvline(lower, color=palette["gold"], lw=0.8, ls="--")
    ax.axvline(upper, color=palette["blueDark"], lw=0.8, ls="--")
    ax.text(lower, 3.14, r"$1/2$", ha="center", va="bottom", fontsize=5.6)
    ax.text(upper, 3.14, r"$3$", ha="center", va="bottom", fontsize=5.6)
    ax.text((lower + upper) / 2.0, 2.72, "OPEN STRIP",
            ha="center", va="center", fontsize=5.8, fontweight="bold",
            color=palette["blueDark"])
    ax.text(0.985, 0.055, "$p<0$: decays", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=5.1, color=palette["midGrey"])
    ax.text(
        0.04, 0.055,
        r"$\gamma>1/2$: enters for large $N$" "\n"
        r"$\gamma=1/2$: prefactor $<R_{1/2}$",
        transform=ax.transAxes, ha="left", va="bottom", fontsize=4.95,
        bbox={"boxstyle": "round,pad=0.22", "fc": palette["paper"],
              "ec": palette["lightGrey"], "lw": 0.5},
    )
    ax.set_xlim(min(gamma), max(gamma))
    ax.set_ylim(-3.65, 3.35)
    ax.set_xlabel(r"amplitude exponent $\gamma$ in $a_N=cN^{-\gamma}$")
    ax.set_ylabel(r"power $p$ in $\|a_Ne_N\|_{\dot H^s}=cN^p$")
    ax.grid(axis="y", color=palette["lightGrey"], lw=0.45, alpha=0.85)
    ax.legend(frameon=False, fontsize=4.95, loc="upper right", handlelength=2.4)
    panel_heading(ax, "B", "Pure-mode Sobolev powers")

    ax = axes[2]
    taus = [float(row["tau"]) for row in heat]
    discrete = [float(row["discrete_heat"]) for row in heat]
    continuous = [float(row["continuous_heat_bound"]) for row in heat]
    heat_mark_every = max(1, len(taus) // 10)
    ax.loglog(taus, discrete, color=palette["blueDark"], lw=1.55,
              marker="o", ms=2.2, markevery=heat_mark_every,
              label=r"lattice maximum $H_{\rm disc}$")
    ax.loglog(taus, continuous, color=palette["gold"], lw=1.4, ls="--",
              label=r"continuous bound $(3/(2e\tau))^{3/2}$")
    ax.fill_between(taus, discrete, continuous, color=palette["goldLight"], alpha=0.15)
    ax.set_xlim(min(taus), max(taus))
    ax.set_xlabel(r"heat time $\tau$")
    ax.set_ylabel(r"$|k|^3e^{-\tau|k|^2}$ multiplier")
    ax.grid(which="major", color=palette["lightGrey"], lw=0.45, alpha=0.85)
    ax.legend(frameon=False, fontsize=4.9, loc="lower left", handlelength=2.4)
    ax.text(
        0.5, 0.965, "LINEAR ONLY —\nNOT A NONLINEAR ENTRY CERTIFICATE",
        transform=ax.transAxes, ha="center", va="top", fontsize=5.05,
        linespacing=1.12, fontweight="bold", color=palette["ink"],
        bbox={"boxstyle": "round,pad=0.25", "fc": palette["paper"],
              "ec": palette["gold"], "lw": 0.75},
    )
    ax.text(
        0.965, 0.18, r"exact lattice search" "\n" r"$|k|^2\leq64^2$",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=5.1,
        color=palette["midGrey"],
    )
    panel_heading(ax, "C", "Linear heat benchmark")

    fig.text(
        0.055, 0.060,
        r"Formula diagnostic only.  Critical-radius constants are normalized in A; C does not estimate the nonlinear Duhamel term.",
        fontsize=5.45, color=palette["midGrey"],
    )

    svg = HERE / "figure.svg"
    png = HERE / "figure.png"
    fig.savefig(svg, format="svg")
    fig.savefig(png, format="png", dpi=int(config["pngDpi"]))
    if include_pdf:
        fig.savefig(HERE / "figure.pdf", format="pdf")
    plt.close(fig)

    qa_dpi = int(config["qaDpi"])
    qa_size = (
        round(float(config["widthMillimetres"]) / 25.4 * qa_dpi),
        round(float(config["heightMillimetres"]) / 25.4 * qa_dpi),
    )
    with Image.open(png) as image:
        final_size = image.convert("RGB").resize(qa_size, Image.Resampling.LANCZOS)
        final_size.save(HERE / "qa-final-size.png", dpi=(qa_dpi, qa_dpi))
        ImageOps.grayscale(final_size).convert("RGB").save(
            HERE / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi)
        )

    if include_pdf:
        import pypdfium2 as pdfium  # type: ignore

        document = pdfium.PdfDocument(str(HERE / "figure.pdf"))
        if len(document) != 1:
            raise RuntimeError("formal figure PDF must contain exactly one page")
        page = document[0]
        bitmap = page.render(scale=qa_dpi / 72.0)
        pdf_image = bitmap.to_pil().convert("RGB")
        pdf_image.save(HERE / "qa-pdf.png", dpi=(qa_dpi, qa_dpi))
        page.close()
        document.close()


def record_if_present(path: Path) -> dict[str, object] | None:
    if not path.is_file():
        return None
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def main() -> int:
    args = parse_args()
    mode = "render-final" if args.render_final else (
        "render-nonpdf" if args.render_nonpdf else "data-only"
    )
    if mode != "render-final":
        present = [path.name for path in PDF_ASSETS if path.exists()]
        if present:
            raise RuntimeError("non-PDF mode refuses a package containing: " + ", ".join(present))

    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    if config.get("figureId") != contract.get("figureId"):
        raise RuntimeError("config/contract figureId mismatch")

    monitor = Monitor()
    monitor.event("start", mode=mode, evidenceClass=contract["evidenceClass"])
    rows, facts = generate_rows(config, monitor)
    write_source_data(rows)
    monitor.event("source-data-written", rowCount=len(rows))

    if mode in {"render-nonpdf", "render-final"}:
        render(rows, config, include_pdf=mode == "render-final")
        monitor.event("figure-rendered", mode=mode)

    environment = {
        "schemaVersion": "r073p-critical-frequency-gate-environment-v1",
        "createdAt": utc_now(),
        "mode": mode,
        "host": platform.node(),
        "operatingSystem": platform.platform(),
        "machine": platform.machine(),
        "cpu": platform.processor() or "not reported by platform",
        "logicalCpuCount": os.cpu_count(),
        "memoryGiB": total_memory_gib(),
        "python": sys.version,
        "pythonExecutable": sys.executable,
        "packages": {
            name: installed_version(name)
            for name in ("matplotlib", "numpy", "pillow", "pypdf", "pypdfium2")
        },
        "processes": 1,
        "threadsPerProcess": 1,
        "gpu": "not used",
    }
    (HERE / "environment.json").write_text(canonical(environment), encoding="utf-8")
    monitor.event("complete", mode=mode, pdfGenerated=(HERE / "figure.pdf").is_file())

    output_names = (
        "source-data.csv",
        "figure.svg",
        "figure.png",
        "qa-final-size.png",
        "qa-grayscale.png",
        "figure.pdf",
        "qa-pdf.png",
        "environment.json",
        "progress.ndjson",
        "resource-log.ndjson",
    )
    outputs = [record for name in output_names if (record := record_if_present(HERE / name))]
    results = {
        "schemaVersion": "r073p-critical-frequency-gate-results-v1",
        "figureId": contract["figureId"],
        "createdAt": utc_now(),
        "mode": mode,
        "evidenceClass": contract["evidenceClass"],
        "isNavierStokesSimulation": False,
        "isFormulaDiagnostic": True,
        "formulas": {
            "directH3Threshold": "N^-3 after normalized radius",
            "criticalHhalfThreshold": "N^-1/2 after normalized radius",
            "pureModeHomogeneousSobolev": "||c N^-gamma e_N||_{Hdot^s}=c N^(s-gamma)",
            "discreteLinearHeat": "max_{k in Z^3 minus {0}} |k|^3 exp(-tau |k|^2)",
            "continuousLinearHeatBound": "(3/(2 e tau))^(3/2)",
        },
        "facts": facts,
        "rowCount": len(rows),
        "scientificWallTimeSeconds": time.monotonic() - START,
        "pdfGenerated": (HERE / "figure.pdf").is_file(),
        "outputs": outputs,
    }
    (HERE / "results.json").write_text(canonical(results), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
