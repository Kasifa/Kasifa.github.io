#!/usr/bin/env python3
"""Generate the R0.73Q closed-form figure data and unsealed figure assets."""

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
FIGURE_ID = "fig-r073q-heat-flow-separation"
CSV_FIELDS = (
    "record_type",
    "sample_index",
    "j",
    "N",
    "l2_norm",
    "heat_trace_norm",
    "hhalf_seminorm",
    "heat_to_l2_ratio",
    "hhalf_to_l2_ratio",
    "hhalf_to_heat_ratio",
    "n",
    "g_l4_fourth",
    "g_l4_norm",
    "fractional_output",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--data-only", action="store_true")
    modes.add_argument("--render-preseal", action="store_true")
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
        progress = {
            "stage": stage,
            "timestampUtc": now,
            "elapsedSeconds": elapsed,
            **fields,
        }
        resources = {
            "stage": stage,
            "timestampUtc": now,
            "elapsedSeconds": elapsed,
            "maximumResidentSetMiB": rss_mib(),
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "executionHost": platform.node(),
        }
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(progress, sort_keys=True) + "\n")
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(resources, sort_keys=True) + "\n")


def exponent_grid(settings: dict[str, Any]) -> list[int]:
    minimum = int(settings["minimumExponent"])
    maximum = int(settings["maximumExponent"])
    step = int(settings["exponentStep"])
    if not (0 <= minimum <= maximum and step >= 1):
        raise RuntimeError("invalid exponent grid")
    return list(range(minimum, maximum + 1, step))


def generate_rows(config: dict[str, Any], monitor: Monitor) -> tuple[list[dict[str, str]], dict[str, Any]]:
    rows: list[dict[str, str]] = []
    c6 = (5.0 / 16.0) ** (1.0 / 6.0)
    heat_constant = c6 / (4.0 ** 0.25)
    l2_constant = 2.0 ** -0.5

    shear_exponents = exponent_grid(config["panelA"])
    shear_values: list[tuple[float, float, float]] = []
    for index, exponent in enumerate(shear_exponents):
        frequency = 2**exponent
        l2 = l2_constant * frequency ** -0.25
        heat_trace = heat_constant * frequency ** -0.75
        hhalf = l2_constant * frequency ** 0.25
        row = {field: "" for field in CSV_FIELDS}
        row.update({
            "record_type": "shear_norm",
            "sample_index": str(index),
            "j": str(exponent),
            "N": str(frequency),
            "l2_norm": format(l2, ".17g"),
            "heat_trace_norm": format(heat_trace, ".17g"),
            "hhalf_seminorm": format(hhalf, ".17g"),
            "heat_to_l2_ratio": format(heat_trace / l2, ".17g"),
            "hhalf_to_l2_ratio": format(hhalf / l2, ".17g"),
            "hhalf_to_heat_ratio": format(hhalf / heat_trace, ".17g"),
        })
        rows.append(row)
        shear_values.append((l2, heat_trace, hhalf))
    monitor.event("shear-formulas", rowCount=len(shear_exponents))

    endpoint_exponents = exponent_grid(config["panelC"])
    endpoint_values: list[tuple[float, float]] = []
    log_two = math.log(2.0)
    for index, exponent in enumerate(endpoint_exponents):
        n = 2**exponent
        g_fourth = 1.0 - log_two / n
        g_norm = g_fourth ** 0.25
        output = n ** 0.75 - n ** -0.25 * log_two
        row = {field: "" for field in CSV_FIELDS}
        row.update({
            "record_type": "endpoint_counterexample",
            "sample_index": str(index),
            "j": str(exponent),
            "n": str(n),
            "g_l4_fourth": format(g_fourth, ".17g"),
            "g_l4_norm": format(g_norm, ".17g"),
            "fractional_output": format(output, ".17g"),
        })
        rows.append(row)
        endpoint_values.append((g_norm, output))
    monitor.event("endpoint-formulas", rowCount=len(endpoint_exponents))

    facts = {
        "constants": {
            "c6": c6,
            "l2Constant": l2_constant,
            "heatTraceConstant": heat_constant,
        },
        "shear": {
            "rowCount": len(shear_exponents),
            "exponentRange": [min(shear_exponents), max(shear_exponents)],
            "frequencyRange": [2 ** min(shear_exponents), 2 ** max(shear_exponents)],
            "l2StrictlyDecreasing": all(
                a[0] > b[0] for a, b in zip(shear_values, shear_values[1:])
            ),
            "heatTraceStrictlyDecreasing": all(
                a[1] > b[1] for a, b in zip(shear_values, shear_values[1:])
            ),
            "hhalfStrictlyIncreasing": all(
                a[2] < b[2] for a, b in zip(shear_values, shear_values[1:])
            ),
            "asymptoticPowers": {
                "l2": -0.25,
                "heatTrace": -0.75,
                "hhalf": 0.25,
            },
        },
        "endpoint": {
            "rowCount": len(endpoint_exponents),
            "exponentRange": [min(endpoint_exponents), max(endpoint_exponents)],
            "nRange": [2 ** min(endpoint_exponents), 2 ** max(endpoint_exponents)],
            "gNormBelowOne": all(value[0] < 1.0 for value in endpoint_values),
            "gNormStrictlyIncreasing": all(
                a[0] < b[0] for a, b in zip(endpoint_values, endpoint_values[1:])
            ),
            "fractionalOutputStrictlyIncreasing": all(
                a[1] < b[1] for a, b in zip(endpoint_values, endpoint_values[1:])
            ),
            "inputLimit": 1.0,
            "outputAsymptoticPower": 0.75,
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
        "font.size": 6.6,
        "axes.titlesize": 7.5,
        "axes.labelsize": 6.2,
        "axes.edgecolor": palette["midGrey"],
        "axes.linewidth": 0.65,
        "axes.facecolor": palette["paper"],
        "figure.facecolor": palette["paper"],
        "savefig.facecolor": palette["paper"],
        "xtick.labelsize": 5.3,
        "ytick.labelsize": 5.3,
        "xtick.color": palette["ink"],
        "ytick.color": palette["ink"],
        "text.color": palette["ink"],
        "axes.labelcolor": palette["ink"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "lines.solid_capstyle": "round",
    })


def panel_heading(ax: Any, letter: str, title: str) -> None:
    ax.text(-0.12, 1.09, letter, transform=ax.transAxes, fontsize=9.1,
            fontweight="bold", va="bottom")
    ax.text(-0.015, 1.09, title, transform=ax.transAxes, fontsize=7.1,
            fontweight="bold", va="bottom")


def render(rows: list[dict[str, str]], config: dict[str, Any]) -> None:
    import matplotlib as mpl  # type: ignore

    mpl.use("Agg")
    import matplotlib.pyplot as plt  # type: ignore
    from PIL import Image, ImageOps  # type: ignore

    palette = config["palette"]
    configure_style(mpl, palette)
    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    fig, axes = plt.subplots(1, 3, figsize=(width, height))
    fig.subplots_adjust(left=0.067, right=0.988, bottom=0.215, top=0.73, wspace=0.43)
    fig.text(0.055, 0.938, "R0.73Q | heat-flow separation",
             fontsize=10.6, fontweight="bold", color=palette["blueDark"])
    fig.text(
        0.055, 0.875,
        "Exact closed formulas on the normalized torus · not a Navier--Stokes simulation",
        fontsize=6.65, color=palette["midGrey"],
    )
    fig.text(0.949, 0.937, "✦", ha="right", va="top", fontsize=12,
             color=palette["gold"])

    shear = [row for row in rows if row["record_type"] == "shear_norm"]
    endpoint = [row for row in rows if row["record_type"] == "endpoint_counterexample"]

    frequencies = [int(row["N"]) for row in shear]
    l2 = [float(row["l2_norm"]) for row in shear]
    heat_trace = [float(row["heat_trace_norm"]) for row in shear]
    hhalf = [float(row["hhalf_seminorm"]) for row in shear]

    ax = axes[0]
    ax.loglog(frequencies, heat_trace, color=palette["blueDark"], lw=1.55,
              marker="o", ms=2.25, markevery=4,
              label=r"heat trace $\mathfrak{X}$: $N^{-3/4}$")
    ax.loglog(frequencies, l2, color=palette["midGrey"], lw=1.25, ls=":",
              marker="^", ms=2.25, markevery=4,
              label=r"$L^2$: $N^{-1/4}$")
    ax.loglog(frequencies, hhalf, color=palette["gold"], lw=1.45, ls="--",
              marker="s", mfc=palette["paper"], ms=2.25, markevery=4,
              label=r"$H^{1/2}$: $N^{1/4}$")
    ax.set_xlim(min(frequencies), max(frequencies))
    ax.set_xlabel(r"frequency $N=2^j$")
    ax.set_ylabel("exact norm (dimensionless)")
    ax.grid(which="major", color=palette["lightGrey"], lw=0.45, alpha=0.85)
    ax.legend(frameon=False, fontsize=4.9, loc="best", handlelength=2.45)
    ax.text(
        0.96, 0.35,
        r"$\mathfrak{X},L^2\to0$" "\n" r"$H^{1/2}\to\infty$",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=5.2,
        fontweight="bold", color=palette["ink"],
        bbox={"boxstyle": "round,pad=0.22", "fc": palette["paper"],
              "ec": palette["lightGrey"], "lw": 0.55},
    )
    panel_heading(ax, "A", "Exact shear norms")

    ax = axes[1]
    ax.loglog(heat_trace, hhalf, color=palette["blueDark"], lw=1.55,
              marker="o", ms=2.35, mfc=palette["paper"])
    labels = set(int(value) for value in config["panelB"]["labelExponents"])
    for row in shear:
        exponent = int(row["j"])
        if exponent in labels:
            x = float(row["heat_trace_norm"])
            y = float(row["hhalf_seminorm"])
            offset = (3, 3) if exponent not in {0, 32} else (
                (-4, 6) if exponent == 0 else (3, -2)
            )
            ax.annotate(
                rf"$2^{{{exponent}}}$", (x, y), xytext=offset,
                textcoords="offset points", fontsize=4.8,
                ha="right" if exponent == 0 else "left",
            )
    start_index = 4
    end_index = 12
    ax.annotate(
        "increasing $N$",
        xy=(heat_trace[end_index], hhalf[end_index]),
        xytext=(heat_trace[start_index], hhalf[start_index]),
        arrowprops={"arrowstyle": "->", "color": palette["gold"], "lw": 0.9},
        fontsize=5.0, color=palette["gold"], ha="left", va="bottom",
    )
    ax.set_xlabel(r"heat-flow trace $\|w_N\|_{\mathfrak{X}}$")
    ax.set_ylabel(r"critical size $|w_N|_{1/2}$")
    ax.grid(which="major", color=palette["lightGrey"], lw=0.45, alpha=0.85)
    ax.text(
        0.5, 0.95, "NO RADIUS ORDERING\nTHE STABLE SET IS A UNION",
        transform=ax.transAxes, ha="center", va="top", fontsize=4.95,
        linespacing=1.12, fontweight="bold", color=palette["ink"],
        bbox={"boxstyle": "round,pad=0.24", "fc": palette["paper"],
              "ec": palette["gold"], "lw": 0.7},
    )
    panel_heading(ax, "B", "Parametric domain separation")

    ax = axes[2]
    n_values = [int(row["n"]) for row in endpoint]
    g_norm = [float(row["g_l4_norm"]) for row in endpoint]
    fractional = [float(row["fractional_output"]) for row in endpoint]
    ax.loglog(n_values, g_norm, color=palette["blueDark"], lw=1.45,
              marker="o", ms=2.25, markevery=2,
              label=r"input $\|g_n\|_4\to1$")
    ax.loglog(n_values, fractional, color=palette["gold"], lw=1.5, ls="--",
              marker="s", mfc=palette["paper"], ms=2.25, markevery=2,
              label=r"output $I_{1/4}g_n(1)\to\infty$")
    ax.set_xlim(min(n_values), max(n_values))
    ax.set_xlabel(r"counterexample index $n=2^j$")
    ax.set_ylabel("exact dimensionless value")
    ax.grid(which="major", color=palette["lightGrey"], lw=0.45, alpha=0.85)
    ax.legend(frameon=False, fontsize=4.85, loc="best", handlelength=2.4)
    ax.text(
        0.96, 0.19, "BARE ENDPOINT MAP ONLY\nNOT KOCH--TATARU THEORY",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=4.9,
        linespacing=1.12, fontweight="bold", color=palette["ink"],
        bbox={"boxstyle": "round,pad=0.24", "fc": palette["paper"],
              "ec": palette["gold"], "lw": 0.7},
    )
    panel_heading(ax, "C", "Time-endpoint obstruction")

    fig.text(
        0.055, 0.058,
        "Formula diagnostic only. No arbitrary-L2 safety, nonlinear PDE certificate, or Clay conclusion is inferred.",
        fontsize=5.35, color=palette["midGrey"],
    )

    svg = HERE / "figure.svg"
    pdf = HERE / "figure.pdf"
    png = HERE / "figure.png"
    fig.savefig(svg, format="svg")
    fig.savefig(pdf, format="pdf")
    fig.savefig(png, format="png", dpi=int(config["pngDpi"]))
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

    import pypdfium2 as pdfium  # type: ignore

    document = pdfium.PdfDocument(str(pdf))
    if len(document) != 1:
        raise RuntimeError("figure PDF must contain exactly one page")
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
    mode = "render-preseal" if args.render_preseal else "data-only"
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    if config.get("figureId") != FIGURE_ID or contract.get("figureId") != FIGURE_ID:
        raise RuntimeError("config/contract figureId mismatch")

    monitor = Monitor()
    monitor.event("start", mode=mode, evidenceClass=contract["evidenceClass"])
    rows, facts = generate_rows(config, monitor)
    write_source_data(rows)
    monitor.event("source-data-written", rowCount=len(rows))

    if mode == "render-preseal":
        render(rows, config)
        monitor.event("figure-rendered", mode=mode, pdfGenerated=True)

    environment = {
        "schemaVersion": "r073q-heat-flow-separation-environment-v1",
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
        "dgxUsed": False,
    }
    (HERE / "environment.json").write_text(canonical(environment), encoding="utf-8")
    monitor.event("complete", mode=mode, pdfGenerated=(HERE / "figure.pdf").is_file())

    output_names = (
        "source-data.csv",
        "figure.pdf",
        "figure.svg",
        "figure.png",
        "qa-final-size.png",
        "qa-grayscale.png",
        "qa-pdf.png",
        "environment.json",
        "progress.ndjson",
        "resource-log.ndjson",
    )
    outputs = [record for name in output_names if (record := record_if_present(HERE / name))]
    results = {
        "schemaVersion": "r073q-heat-flow-separation-results-v1",
        "figureId": FIGURE_ID,
        "createdAt": utc_now(),
        "mode": mode,
        "evidenceClass": contract["evidenceClass"],
        "isNavierStokesSimulation": False,
        "isFormulaDiagnostic": True,
        "isNonlinearPdeCertificate": False,
        "dgxUsed": False,
        "formulas": {
            "l2Norm": "2^-1/2 N^-1/4",
            "heatTraceNorm": "(5/16)^(1/6) 4^-1/4 N^-3/4",
            "hhalfSeminorm": "2^-1/2 N^1/4",
            "endpointInputFourthPower": "1-log(2)/n",
            "endpointInputNorm": "(1-log(2)/n)^1/4",
            "endpointOutput": "n^3/4-n^-1/4 log(2)",
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
