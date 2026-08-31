#!/usr/bin/env python3
"""Generate R0.73R analytic figure data and source-unsealed assets."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
from importlib.metadata import PackageNotFoundError, version as package_version
import json
import math
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
from typing import Any


def bootstrap() -> None:
    """Allow the repository's bundled dependency directory on sys.path."""
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
FIGURE_ID = "fig-r073r-phase-coherence"
CSV_FIELDS = (
    "record_type",
    "family",
    "m",
    "N",
    "q",
    "s",
    "k1",
    "k2",
    "k3",
    "coefficient_sign",
    "coefficient_modulus",
    "r",
    "unscaled_dirichlet_guide",
    "unscaled_rudin_shapiro_guide",
    "unscaled_ratio_guide",
    "scaled_l2_guide",
    "scaled_dirichlet_heat_guide",
    "scaled_rudin_shapiro_heat_guide",
    "scaled_hhalf_guide",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="", help="optional Python package root")
    parser.add_argument(
        "--output-dir",
        default=str(HERE),
        help="directory for generated data and figure assets",
    )
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--data-only", action="store_true")
    modes.add_argument("--render-preseal", action="store_true")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root is not an object: {path}")
    return value


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


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
    def __init__(self, output_dir: Path) -> None:
        self.progress = output_dir / "progress.ndjson"
        self.resources = output_dir / "resource-log.ndjson"
        self.progress.write_text("", encoding="utf-8")
        self.resources.write_text("", encoding="utf-8")

    def event(self, stage: str, **fields: object) -> None:
        now = utc_now()
        elapsed = time.monotonic() - START
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({
                "stage": stage,
                "timestampUtc": now,
                "elapsedSeconds": elapsed,
                **fields,
            }, sort_keys=True) + "\n")
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({
                "stage": stage,
                "timestampUtc": now,
                "elapsedSeconds": elapsed,
                "maximumResidentSetMiB": rss_mib(),
                "processes": 1,
                "threadsPerProcess": 1,
                "gpu": "not used",
                "executionHost": platform.node(),
            }, sort_keys=True) + "\n")


def blank_row() -> dict[str, str]:
    return {field: "" for field in CSV_FIELDS}


def is_power_of_two(value: int) -> bool:
    return value >= 1 and value & (value - 1) == 0


def rudin_shapiro(m: int) -> tuple[list[int], list[int]]:
    """Return coefficient lists for P_m and Q_m from the exact recursion."""
    if not is_power_of_two(m):
        raise ValueError("Rudin--Shapiro length must be a positive power of two")
    p = [1]
    q = [1]
    while len(p) < m:
        old_p = p
        old_q = q
        p = old_p + old_q
        q = old_p + [-value for value in old_q]
    if len(p) != m or any(value not in {-1, 1} for value in p + q):
        raise RuntimeError("Rudin--Shapiro recursion invariant failed")
    return p, q


def exponent_grid(config: dict[str, Any]) -> list[int]:
    settings = config["scaling"]
    minimum = int(settings["minimumExponent"])
    maximum = int(settings["maximumExponent"])
    step = int(settings["exponentStep"])
    if minimum < 0 or maximum < minimum or step < 1:
        raise ValueError("invalid analytic exponent grid")
    return list(range(minimum, maximum + 1, step))


def generate_rows(config: dict[str, Any]) -> list[dict[str, str]]:
    """Generate exact support/sign rows and normalized analytic power guides."""
    panel_a = config["panelA"]
    m = int(panel_a["m"])
    carrier_factor = int(panel_a["carrierFactor"])
    if carrier_factor < 8 or not is_power_of_two(m):
        raise ValueError("Panel A requires power-of-two m and carrier factor >= 8")
    n = carrier_factor * m
    p, _ = rudin_shapiro(m)
    coefficient_modulus = 1.0 / (math.sqrt(2.0) * m)
    rows: list[dict[str, str]] = []

    for family, coefficients in (("Dirichlet", [1] * m), ("Rudin-Shapiro", p)):
        for q_index in range(m):
            for s_index in range(m):
                row = blank_row()
                row.update({
                    "record_type": "positive_fourier_packet",
                    "family": family,
                    "m": str(m),
                    "N": str(n),
                    "q": str(q_index),
                    "s": str(s_index),
                    "k1": str(n + q_index),
                    "k2": str(s_index),
                    "k3": "0",
                    "coefficient_sign": str(coefficients[q_index] * coefficients[s_index]),
                    "coefficient_modulus": format(coefficient_modulus, ".17g"),
                })
                rows.append(row)

    for exponent in exponent_grid(config):
        shell_size = 2**exponent
        row = blank_row()
        row.update({
            "record_type": "analytic_scaling_guide",
            "m": str(shell_size),
            "N": str(8 * shell_size),
            "r": str(exponent),
            "unscaled_dirichlet_guide": format(shell_size ** (1.0 / 6.0), ".17g"),
            "unscaled_rudin_shapiro_guide": format(shell_size ** (-1.0 / 2.0), ".17g"),
            "unscaled_ratio_guide": format(shell_size ** (2.0 / 3.0), ".17g"),
            "scaled_l2_guide": format(shell_size ** (-1.0 / 6.0), ".17g"),
            "scaled_dirichlet_heat_guide": "1",
            "scaled_rudin_shapiro_heat_guide": format(shell_size ** (-2.0 / 3.0), ".17g"),
            "scaled_hhalf_guide": format(shell_size ** (1.0 / 3.0), ".17g"),
        })
        rows.append(row)
    return rows


def write_rows(rows: list[dict[str, str]], output_dir: Path) -> None:
    with (output_dir / "source-data.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def configure_style(mpl: Any, palette: dict[str, str]) -> None:
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 6.4,
        "axes.titlesize": 7.2,
        "axes.labelsize": 6.0,
        "axes.edgecolor": palette["midGrey"],
        "axes.linewidth": 0.65,
        "axes.facecolor": palette["paper"],
        "figure.facecolor": palette["paper"],
        "savefig.facecolor": palette["paper"],
        "xtick.labelsize": 5.1,
        "ytick.labelsize": 5.1,
        "xtick.color": palette["ink"],
        "ytick.color": palette["ink"],
        "text.color": palette["ink"],
        "axes.labelcolor": palette["ink"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "lines.solid_capstyle": "round",
    })


def panel_heading(ax: Any, letter: str, title: str) -> None:
    ax.text(
        -0.11, 1.07, letter, transform=ax.transAxes, fontsize=9.0,
        fontweight="bold", va="bottom",
    )
    ax.text(
        -0.01, 1.07, title, transform=ax.transAxes, fontsize=6.9,
        fontweight="bold", va="bottom",
    )


def style_log_axis(ax: Any, palette: dict[str, str], m_values: list[int]) -> None:
    from matplotlib.ticker import LogFormatterMathtext  # type: ignore

    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    tick_values = [m_values[index] for index in (0, 4, 8, 12)]
    ax.set_xticks(tick_values)
    ax.set_xticklabels([str(value) for value in tick_values])
    ax.yaxis.set_major_formatter(LogFormatterMathtext(base=2))
    ax.grid(which="major", color=palette["lightGrey"], lw=0.45, alpha=0.88)
    ax.grid(which="minor", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def render(rows: list[dict[str, str]], config: dict[str, Any], output_dir: Path) -> None:
    import matplotlib as mpl  # type: ignore

    mpl.use("Agg")
    import matplotlib.pyplot as plt  # type: ignore
    from matplotlib.lines import Line2D  # type: ignore

    palette = config["palette"]
    configure_style(mpl, palette)
    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    fig = plt.figure(figsize=(width, height))
    grid = fig.add_gridspec(
        1, 3, left=0.052, right=0.985, bottom=0.205, top=0.73,
        wspace=0.34, width_ratios=(1.15, 1.0, 1.08),
    )
    axes = [fig.add_subplot(grid[0, index]) for index in range(3)]

    fig.text(
        0.052, 0.94, "R0.73R | phase concentration and shell scaling",
        fontsize=10.4, fontweight="bold", color=palette["blueDark"],
    )
    fig.text(
        0.052, 0.875,
        "Matched Dirichlet/Rudin–Shapiro tensors · exact support facts and analytic scaling laws · not simulation",
        fontsize=6.5, color=palette["midGrey"],
    )
    fig.text(
        0.98, 0.944, "✦", ha="right", va="top", fontsize=12,
        color=palette["gold"],
    )

    packet_rows = [row for row in rows if row["record_type"] == "positive_fourier_packet"]
    analytic_rows = [row for row in rows if row["record_type"] == "analytic_scaling_guide"]

    ax = axes[0]
    offsets = {"Dirichlet": 0.0, "Rudin-Shapiro": 10.0}
    for family in ("Dirichlet", "Rudin-Shapiro"):
        selected = [row for row in packet_rows if row["family"] == family]
        positive = [row for row in selected if row["coefficient_sign"] == "1"]
        negative = [row for row in selected if row["coefficient_sign"] == "-1"]
        offset = offsets[family]
        ax.scatter(
            [int(row["q"]) + offset for row in positive],
            [int(row["s"]) for row in positive],
            s=12.0, marker="o", facecolor=palette["blue"],
            edgecolor=palette["blueDark"], linewidth=0.35, zorder=3,
        )
        if negative:
            ax.scatter(
                [int(row["q"]) + offset for row in negative],
                [int(row["s"]) for row in negative],
                s=13.0, marker="s", facecolor=palette["paper"],
                edgecolor=palette["gold"], linewidth=0.75, zorder=3,
            )
        rectangle = plt.Rectangle(
            (offset - 0.58, -0.58), 8.16, 8.16, fill=False,
            edgecolor=palette["lightGrey"], linewidth=0.65, zorder=1,
        )
        ax.add_patch(rectangle)

    ax.text(3.5, 8.18, r"$D_m$: all $+$", ha="center", fontsize=5.5,
            color=palette["blueDark"], fontweight="bold")
    ax.text(13.5, 8.18, r"$P_m$: signs $\pm$", ha="center", fontsize=5.5,
            color=palette["ink"], fontweight="bold")
    ax.set_xlim(-1.1, 18.1)
    ax.set_ylim(-1.25, 8.65)
    ax.set_aspect("equal", adjustable="box")
    ax.set_anchor("N")
    ax.set_xticks([0, 7, 10, 17])
    ax.set_xticklabels(["0", "7", "0", "7"])
    ax.set_yticks([0, 7])
    ax.set_yticklabels(["0", "7"])
    ax.set_xlabel(r"packet indices $q$ (left/right blocks)", labelpad=1.0)
    ax.set_ylabel(r"$s$", rotation=0, labelpad=6)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0, pad=1.0)
    handles = [
        Line2D([], [], marker="o", linestyle="none", ms=4.0,
               mfc=palette["blue"], mec=palette["blueDark"], mew=0.4,
               label="coefficient +1"),
        Line2D([], [], marker="s", linestyle="none", ms=4.0,
               mfc=palette["paper"], mec=palette["gold"], mew=0.75,
               label="coefficient -1"),
    ]
    ax.legend(
        handles=handles, frameon=False, fontsize=4.55, ncol=2,
        loc="lower center", bbox_to_anchor=(0.5, -0.29),
        handletextpad=0.35, columnspacing=0.9,
    )
    ax.text(
        0.5, -0.43,
        r"$m=8$, $N=64$; same sites and $|\widehat W|=1/(\sqrt{2}m)$" "\n"
        "positive packet shown · conjugate reflection omitted",
        transform=ax.transAxes, ha="center", va="top", fontsize=4.65,
        color=palette["midGrey"], linespacing=1.25,
    )
    panel_heading(ax, "A", "Matched Fourier packets")

    m_values = [int(row["m"]) for row in analytic_rows]
    unscaled_d = [float(row["unscaled_dirichlet_guide"]) for row in analytic_rows]
    unscaled_p = [float(row["unscaled_rudin_shapiro_guide"]) for row in analytic_rows]
    ratio = [float(row["unscaled_ratio_guide"]) for row in analytic_rows]

    ax = axes[1]
    ax.plot(
        m_values, unscaled_d, color=palette["blueDark"], lw=1.45,
        marker="o", ms=2.4, markevery=2,
        label=r"Dirichlet $\propto m^{1/6}$",
    )
    ax.plot(
        m_values, unscaled_p, color=palette["gold"], lw=1.35, ls="--",
        marker="s", mfc=palette["paper"], ms=2.5, markevery=2,
        label=r"Rudin–Shapiro $\propto m^{-1/2}$",
    )
    ax.plot(
        m_values, ratio, color=palette["ink"], lw=1.15, ls=":",
        marker="^", mfc=palette["paper"], ms=2.6, markevery=2,
        label=r"ratio $\propto m^{2/3}$",
    )
    style_log_axis(ax, palette, m_values)
    ax.set_xlim(m_values[0], m_values[-1])
    ax.set_xlabel(r"shell width $m=2^r$")
    ax.set_ylabel("relative analytic scale")
    ax.legend(frameon=False, fontsize=4.55, loc="upper left", handlelength=2.25)
    panel_heading(ax, "B", "Unscaled analytic scaling")

    scaled_l2 = [float(row["scaled_l2_guide"]) for row in analytic_rows]
    scaled_d = [float(row["scaled_dirichlet_heat_guide"]) for row in analytic_rows]
    scaled_p = [float(row["scaled_rudin_shapiro_heat_guide"]) for row in analytic_rows]
    scaled_hhalf = [float(row["scaled_hhalf_guide"]) for row in analytic_rows]

    ax = axes[2]
    ax.plot(
        m_values, scaled_l2, color=palette["midGrey"], lw=1.15, ls=":",
        marker="^", mfc=palette["paper"], ms=2.5, markevery=2,
        label=r"shared $L^2\propto m^{-1/6}$",
    )
    ax.plot(
        m_values, scaled_d, color=palette["blueDark"], lw=1.45,
        marker="o", ms=2.3, markevery=2,
        label=r"Dirichlet $\mathfrak{X}\propto1$",
    )
    ax.plot(
        m_values, scaled_p, color=palette["gold"], lw=1.35, ls="--",
        marker="s", mfc=palette["paper"], ms=2.4, markevery=2,
        label=r"Rudin–Shapiro $\mathfrak{X}\propto m^{-2/3}$",
    )
    ax.plot(
        m_values, scaled_hhalf, color=palette["ink"], lw=1.05, ls="-.",
        marker="D", mfc=palette["paper"], ms=2.2, markevery=2,
        label=r"shared $\dot H^{1/2}\propto m^{1/3}$",
    )
    style_log_axis(ax, palette, m_values)
    ax.set_xlim(m_values[0], m_values[-1])
    ax.set_xlabel(r"shell width $m=2^r$")
    ax.set_ylabel(r"relative scale after $\alpha_m$")
    ax.legend(frameon=False, fontsize=4.28, loc="lower left", handlelength=2.25)
    panel_heading(ax, "C", r"Analytic scaling after $\alpha_m$")

    fig.text(
        0.052, 0.045,
        "Panels B–C are analytic exponent guides normalized at m=1; no fit, PDE solve, safety inference, or Clay conclusion.",
        fontsize=5.25, color=palette["midGrey"],
    )

    metadata = {
        "Title": "R0.73R phase concentration and shell scaling",
        "Creator": "R0.73R analytic figure source",
        "Subject": "Analytic formula diagnostic; not a numerical simulation",
    }
    fig.savefig(output_dir / "figure.svg", format="svg")
    fig.savefig(output_dir / "figure.pdf", format="pdf", metadata=metadata)
    fig.savefig(output_dir / "figure.png", format="png", dpi=int(config["pngDpi"]))
    plt.close(fig)

    from PIL import Image, ImageOps  # type: ignore

    qa_dpi = int(config["qaDpi"])
    qa_size = (
        round(float(config["widthMillimetres"]) / 25.4 * qa_dpi),
        round(float(config["heightMillimetres"]) / 25.4 * qa_dpi),
    )
    with Image.open(output_dir / "figure.png") as image:
        final_size = image.convert("RGB").resize(qa_size, Image.Resampling.LANCZOS)
        final_size.save(output_dir / "qa-final-size.png", dpi=(qa_dpi, qa_dpi))
        ImageOps.grayscale(final_size).convert("RGB").save(
            output_dir / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi)
        )

    import pypdfium2 as pdfium  # type: ignore

    document = pdfium.PdfDocument(str(output_dir / "figure.pdf"))
    if len(document) != 1:
        raise RuntimeError("figure PDF must contain exactly one page")
    page = document[0]
    bitmap = page.render(scale=qa_dpi / 72.0)
    pdf_image = bitmap.to_pil().convert("RGB")
    pdf_image.save(output_dir / "qa-pdf.png", dpi=(qa_dpi, qa_dpi))
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

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    monitor = Monitor(output_dir)
    monitor.event("start", mode=mode, evidenceClass=contract["evidenceClass"])
    rows = generate_rows(config)
    write_rows(rows, output_dir)
    packet_rows = [row for row in rows if row["record_type"] == "positive_fourier_packet"]
    scaling_rows = [row for row in rows if row["record_type"] == "analytic_scaling_guide"]
    monitor.event(
        "source-data-written",
        rowCount=len(rows),
        positivePacketRowCount=len(packet_rows),
        analyticScalingRowCount=len(scaling_rows),
    )
    if args.render_preseal:
        render(rows, config, output_dir)
        monitor.event("figure-rendered", pdfGenerated=True, qaRasterCount=3)

    environment = {
        "schemaVersion": "r073r-phase-coherence-environment-v1",
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
    (output_dir / "environment.json").write_text(
        canonical(environment), encoding="utf-8"
    )
    monitor.event("complete", mode=mode, pdfGenerated=(output_dir / "figure.pdf").is_file())

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
    outputs = [
        item for name in output_names
        if (item := record_if_present(output_dir / name)) is not None
    ]
    results = {
        "schemaVersion": "r073r-phase-coherence-results-v1",
        "figureId": FIGURE_ID,
        "createdAt": utc_now(),
        "mode": mode,
        "evidenceClass": contract["evidenceClass"],
        "isAnalyticScalingGuide": True,
        "isFittedScalingLaw": False,
        "isNavierStokesSimulation": False,
        "isNonlinearPdeCertificate": False,
        "solver": "none",
        "randomSeed": "not applicable",
        "dgxUsed": False,
        "formulas": {
            "coefficientModulus": "1/(sqrt(2)*m)",
            "unscaledDirichletGuide": "m^(1/6)",
            "unscaledRudinShapiroGuide": "m^(-1/2)",
            "unscaledRatioGuide": "m^(2/3)",
            "scaledL2Guide": "m^(-1/6)",
            "scaledDirichletHeatGuide": "1",
            "scaledRudinShapiroHeatGuide": "m^(-2/3)",
            "scaledHhalfGuide": "m^(1/3)",
        },
        "facts": {
            "panelA": {
                "m": int(config["panelA"]["m"]),
                "carrier": int(config["panelA"]["carrierFactor"]) * int(config["panelA"]["m"]),
                "positivePacketRowCount": len(packet_rows),
                "rowCountPerFamily": len(packet_rows) // 2,
                "fullSupportSizePerFamily": 2 * int(config["panelA"]["m"]) ** 2,
                "supportAndModuliMatched": True,
            },
            "scaling": {
                "rowCount": len(scaling_rows),
                "exponentRange": [
                    int(config["scaling"]["minimumExponent"]),
                    int(config["scaling"]["maximumExponent"]),
                ],
                "allGuidesNormalizedAtM1": True,
                "phaseSeparationPower": 2.0 / 3.0,
            },
        },
        "rowCount": len(rows),
        "scientificWallTimeSeconds": time.monotonic() - START,
        "pdfGenerated": (output_dir / "figure.pdf").is_file(),
        "outputs": outputs,
    }
    (output_dir / "results.json").write_text(
        canonical(results), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
