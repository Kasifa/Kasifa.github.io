#!/usr/bin/env python3
"""Generate the R0.73S formal analytic figure and preseal artifacts."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from fractions import Fraction
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
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
START = time.monotonic()
FIGURE_ID = "fig-r073s-quadratic-certificate"
CERTIFICATE_CSV = ROOT / "research/certificates/r073s/source-data.csv"
CERTIFICATE_VALIDATOR = ROOT / "research/certificates/r073s/validate_certificate.py"
CSV_FIELDS = (
    "panel", "series", "parameter", "x", "y", "quantity_class",
    "source_origin", "source_record_type", "source_family", "formula",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--output-dir", default=str(HERE))
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--data-only", action="store_true")
    modes.add_argument("--render-preseal", action="store_true")
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root is not an object: {path}")
    return value


def installed_version(name: str) -> str | None:
    try:
        return package_version(name)
    except PackageNotFoundError:
        return None


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
    return None


class Monitor:
    def __init__(self, output_dir: Path) -> None:
        self.progress = output_dir / "progress.ndjson"
        self.resources = output_dir / "resource-log.ndjson"
        self.progress.write_text("", encoding="utf-8")
        self.resources.write_text("", encoding="utf-8")

    def event(self, stage: str, **fields: object) -> None:
        event = {
            "stage": stage,
            "timestampUtc": utc_now(),
            "elapsedSeconds": time.monotonic() - START,
            **fields,
        }
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, sort_keys=True) + "\n")
        resource_event = {
            "stage": stage,
            "timestampUtc": event["timestampUtc"],
            "elapsedSeconds": event["elapsedSeconds"],
            "maximumResidentSetMiB": rss_mib(),
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "executionHost": platform.node(),
        }
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(resource_event, sort_keys=True) + "\n")


def verify_source_certificate() -> None:
    if not CERTIFICATE_CSV.is_file() or not CERTIFICATE_VALIDATOR.is_file():
        raise RuntimeError("sealed R0.73S certificate source is missing")
    completed = subprocess.run(
        [sys.executable, str(CERTIFICATE_VALIDATOR), "--verify-only"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("R0.73S certificate verification failed: " + completed.stderr[-1000:])


def read_certificate_rows() -> list[dict[str, str]]:
    with CERTIFICATE_CSV.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def row(
    panel: str,
    series: str,
    parameter: int,
    x: float,
    y: float,
    quantity_class: str,
    source_origin: str,
    source_record_type: str,
    source_family: str,
    formula: str,
) -> dict[str, str]:
    return {
        "panel": panel,
        "series": series,
        "parameter": str(parameter),
        "x": format(x, ".17g"),
        "y": format(y, ".17g"),
        "quantity_class": quantity_class,
        "source_origin": source_origin,
        "source_record_type": source_record_type,
        "source_family": source_family,
        "formula": formula,
    }


def generate_rows(config: dict[str, Any], certificate: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    spikes = {
        int(item["parameter"]): item
        for item in certificate
        if item["record_type"] in {
            "fixed_quartic_spike",
            "bounded_quartic_spike",
            "asymptotically_fixed_quartic_spike",
        }
    }
    for m_value in config["panelA"]["mValues"]:
        source = spikes[int(m_value)]
        gamma = float(Fraction(source["l4_fourth"]))
        theta = float(Fraction(source["l6_sixth"]))
        support = int(source.get("autocorrelation_support") or source.get("difference_support", ""))
        rows.extend((
            row("A", "exact_theta", m_value, support, theta, "exact",
                "sealed-r073s-certificate", source["record_type"], source["family"], "Theta_m"),
            row("A", "autocorrelation_certificate", m_value, support,
                gamma * math.sqrt(support * gamma), "rigorous-upper-bound",
                "sealed-r073s-certificate", source["record_type"], source["family"],
                "Gamma_m^(3/2)*sqrt(D_C)"),
            row("A", "sharp_asymptotic_guide", m_value, support,
                11.0 / 40.0 * math.sqrt(support), "analytic-asymptotic-guide",
                "exact-formula", source["record_type"], source["family"],
                "(11/40)*sqrt(D_C)"),
        ))

    matched = {
        (item["family"], int(item["parameter"])): item
        for item in certificate if item["record_type"] == "matched_r073r"
    }
    minimum = int(config["panelB"]["minimumExponent"])
    maximum = int(config["panelB"]["maximumExponent"])
    for exponent in range(minimum, maximum + 1):
        m_value = 2**exponent
        for family in ("D", "RS"):
            source = matched[(family, exponent)]
            theta = float(Fraction(source["l6_sixth"]))
            exact = m_value ** (-2.0 / 3.0) * theta ** (1.0 / 6.0)
            certificate_value = float(source["scaled_heat_proxy"])
            rows.extend((
                row("B", f"{family}_certificate", exponent, m_value, certificate_value,
                    "rigorous-upper-bound", "sealed-r073s-certificate", source["record_type"],
                    family, "m^(-2/3)*(A*Q)^(1/6)"),
                row("B", f"{family}_exact", exponent, m_value, exact, "exact",
                    "sealed-r073s-certificate", source["record_type"], family,
                    "m^(-2/3)*Theta^(1/6)"),
            ))

    panel_c = config["panelC"]
    no_go_counts: dict[int, set[str]] = {}
    for item in certificate:
        if item["record_type"] == "riesz_product_no_go":
            no_go_counts.setdefault(int(item["parameter"]), set()).add(item["family"])
    sealed_depths = {depth for depth, families in no_go_counts.items() if families == {"A", "B"}}
    for depth in range(
        int(panel_c["minimumDepth"]),
        int(panel_c["maximumDepth"]) + 1,
        int(panel_c["depthStep"]),
    ):
        ratio = (323.0 / 311.0) ** (depth / 6.0)
        origin = "sealed-r073s-certificate" if depth in sealed_depths else "exact-formula"
        rows.append(row(
            "C", "l6_norm_ratio", depth, depth, ratio, "exact",
            origin, "riesz_product_no_go", "B/A", "(323/311)^(r/6)",
        ))
    return rows


def write_rows(rows: list[dict[str, str]], output_dir: Path) -> None:
    with (output_dir / "source-data.csv").open("w", encoding="utf-8", newline="") as stream:
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
    ax.text(-0.12, 1.075, letter, transform=ax.transAxes, fontsize=9.0,
            fontweight="bold", va="bottom")
    ax.text(-0.015, 1.075, title, transform=ax.transAxes, fontsize=6.9,
            fontweight="bold", va="bottom")


def clean_axis(ax: Any, palette: dict[str, str]) -> None:
    ax.grid(which="major", color=palette["lightGrey"], lw=0.45, alpha=0.88)
    ax.grid(which="minor", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def series(rows: list[dict[str, str]], panel: str, name: str) -> tuple[list[float], list[float]]:
    selected = [item for item in rows if item["panel"] == panel and item["series"] == name]
    return [float(item["x"]) for item in selected], [float(item["y"]) for item in selected]


def render(rows: list[dict[str, str]], config: dict[str, Any], output_dir: Path) -> None:
    import matplotlib as mpl  # type: ignore
    mpl.use("Agg")
    import matplotlib.pyplot as plt  # type: ignore
    from matplotlib.ticker import LogFormatterMathtext  # type: ignore

    palette = config["palette"]
    configure_style(mpl, palette)
    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    fig = plt.figure(figsize=(width, height))
    grid = fig.add_gridspec(
        1, 3, left=0.058, right=0.985, bottom=0.205, top=0.73,
        wspace=0.36, width_ratios=(1.04, 1.08, 0.98),
    )
    axes = [fig.add_subplot(grid[0, index]) for index in range(3)]

    fig.text(0.058, 0.94, "R0.73S | quadratic autocorrelation: reach and limits",
             fontsize=10.3, fontweight="bold", color=palette["blueDark"])
    fig.text(
        0.058, 0.875,
        "Exact finite formulas and rigorous upper bounds · normalized Haar measure · not simulation",
        fontsize=6.5, color=palette["midGrey"],
    )
    fig.text(0.98, 0.944, "✦", ha="right", va="top", fontsize=12, color=palette["gold"])

    ax = axes[0]
    x_exact, y_exact = series(rows, "A", "exact_theta")
    x_bound, y_bound = series(rows, "A", "autocorrelation_certificate")
    x_guide, y_guide = series(rows, "A", "sharp_asymptotic_guide")
    ax.plot(x_bound, y_bound, color=palette["gold"], lw=1.45, marker="s",
            mfc=palette["paper"], ms=2.9, label=r"certificate $\Gamma^{3/2}\sqrt{D_C}$")
    ax.plot(x_exact, y_exact, color=palette["blueDark"], lw=1.5, marker="o",
            ms=2.7, label=r"exact $\Theta_m$")
    ax.plot(x_guide, y_guide, color=palette["ink"], lw=1.05, ls=":", marker="^",
            mfc=palette["paper"], ms=2.6, label=r"$(11/40)\sqrt{D_C}$")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.xaxis.set_major_formatter(LogFormatterMathtext(base=2))
    ax.yaxis.set_major_formatter(LogFormatterMathtext(base=2))
    selected_ticks = [x_exact[index] for index in (0, 2, 4, 5)]
    ax.set_xticks(selected_ticks)
    ax.set_xticklabels([str(round(value)) for value in selected_ticks])
    ax.set_xlabel(r"autocorrelation support $D_C=4m-1$")
    ax.set_ylabel("dimensionless sixth-moment scale")
    ax.legend(frameon=False, fontsize=5.0, loc="upper left", handlelength=2.2)
    clean_axis(ax, palette)
    panel_heading(ax, "A", r"The $D_C^{1/2}$ loss is sharp")

    ax = axes[1]
    styles = {
        "D_certificate": (palette["blueDark"], "-", "o", True, r"Dirichlet $AQ$ certificate"),
        "D_exact": (palette["blueDark"], ":", "o", False, r"Dirichlet exact $L^6$"),
        "RS_certificate": (palette["gold"], "-", "s", True, r"Rudin–Shapiro $AQ$ certificate"),
        "RS_exact": (palette["gold"], "--", "s", False, r"Rudin–Shapiro exact $L^6$"),
    }
    for name, (colour, line_style, marker, filled, label) in styles.items():
        x_values, y_values = series(rows, "B", name)
        ax.plot(
            x_values, y_values, color=colour, lw=1.35 if "certificate" in name else 1.05,
            ls=line_style, marker=marker, ms=2.55,
            mfc=colour if filled else palette["paper"], mec=colour, mew=0.6, label=label,
        )
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.set_xticks([1, 4, 16, 64, 128])
    ax.set_xticklabels(["1", "4", "16", "64", "128"])
    ax.yaxis.set_major_formatter(LogFormatterMathtext(base=2))
    ax.set_xlabel(r"packet width $m=2^r$")
    ax.set_ylabel(r"scaled shell moment / $AQ$ upper proxy")
    ax.legend(frameon=False, fontsize=4.9, loc="lower left", handlelength=2.35)
    clean_axis(ax, palette)
    panel_heading(ax, "B", "Matched support, separated phase")

    ax = axes[2]
    x_ratio, y_ratio = series(rows, "C", "l6_norm_ratio")
    sealed_depth = int(config["panelC"]["sealedMaximumDepth"])
    ax.axvspan(1, sealed_depth + 0.5, color=palette["blueLight"], alpha=0.32, lw=0)
    ax.axhline(1.0, color=palette["midGrey"], lw=1.0, ls=":",
               label=r"matched low summaries $=1$")
    ax.plot(x_ratio, y_ratio, color=palette["gold"], lw=1.55, marker="s",
            markevery=4, ms=2.7, mfc=palette["paper"], label=r"exact $L^6$ norm ratio")
    ax.scatter([sealed_depth], [(323.0 / 311.0) ** (sealed_depth / 6.0)],
               color=palette["blueDark"], marker="o", s=13, zorder=4)
    ax.text(0.05, 0.72, r"sealed rows $1\leq r\leq8$", transform=ax.transAxes,
            fontsize=4.8, color=palette["blueDark"], fontweight="bold")
    ax.text(0.98, 0.06, r"$(323/311)^{r/6}$", transform=ax.transAxes,
            ha="right", fontsize=5.0, color=palette["gold"])
    ax.set_xlim(0, int(config["panelC"]["maximumDepth"]))
    ax.set_ylim(0.95, max(y_ratio) * 1.07)
    ax.set_xticks([0, 32, 64, 96, 128])
    ax.set_xlabel(r"lacunary product depth $r$")
    ax.set_ylabel(r"$\|G_r\|_6/\|F_r\|_6$")
    ax.legend(frameon=False, fontsize=5.0, loc="upper left", handlelength=2.2)
    clean_axis(ax, palette)
    panel_heading(ax, "C", r"Low summaries miss $L^6$")

    fig.text(
        0.058, 0.045,
        "Line and marker meanings are panel-specific (see legends). No fit, runtime lower bound, PDE solve, instability inference, or Clay conclusion.",
        fontsize=5.15, color=palette["midGrey"],
    )
    metadata = {
        "Title": "R0.73S quadratic autocorrelation: reach and limits",
        "Creator": "R0.73S analytic figure source",
        "Subject": "Exact formulas and rigorous upper bounds; not a simulation",
    }
    fig.savefig(output_dir / "figure.svg", format="svg")
    svg_path = output_dir / "figure.svg"
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
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
    bitmap.to_pil().convert("RGB").save(output_dir / "qa-pdf.png", dpi=(qa_dpi, qa_dpi))
    page.close()
    document.close()


def record_if_present(path: Path) -> dict[str, object] | None:
    if not path.is_file():
        return None
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    if config.get("figureId") != FIGURE_ID or contract.get("figureId") != FIGURE_ID:
        raise RuntimeError("figure id mismatch")
    monitor = Monitor(output_dir)
    mode = "render-preseal" if args.render_preseal else "data-only"
    monitor.event("start", mode=mode, evidenceClass=contract["evidenceClass"])
    verify_source_certificate()
    monitor.event("source-certificate-verified", sha256=sha256(CERTIFICATE_CSV))
    rows = generate_rows(config, read_certificate_rows())
    write_rows(rows, output_dir)
    monitor.event("source-data-written", rowCount=len(rows))
    if args.render_preseal:
        render(rows, config, output_dir)
        monitor.event("figure-rendered", pdfGenerated=True, qaRasterCount=3)

    environment = {
        "schemaVersion": "r073s-quadratic-certificate-environment-v1",
        "createdAt": utc_now(),
        "mode": mode,
        "host": platform.node(),
        "operatingSystem": platform.platform(),
        "machine": platform.machine(),
        "logicalCpuCount": os.cpu_count(),
        "memoryGiB": total_memory_gib(),
        "python": sys.version,
        "pythonExecutable": sys.executable,
        "packages": {name: installed_version(name) for name in
                     ("matplotlib", "numpy", "pillow", "pypdf", "pypdfium2")},
        "processes": 1,
        "threadsPerProcess": 1,
        "gpu": "not used",
        "dgxUsed": False,
    }
    (output_dir / "environment.json").write_text(canonical(environment), encoding="utf-8")
    monitor.event("complete", mode=mode)
    output_names = (
        "source-data.csv", "figure.pdf", "figure.svg", "figure.png",
        "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "environment.json",
        "progress.ndjson", "resource-log.ndjson",
    )
    results = {
        "schemaVersion": "r073s-quadratic-certificate-results-v1",
        "figureId": FIGURE_ID,
        "createdAt": utc_now(),
        "mode": mode,
        "evidenceClass": contract["evidenceClass"],
        "certificateSource": {
            "path": str(CERTIFICATE_CSV.relative_to(ROOT)),
            "sha256": sha256(CERTIFICATE_CSV),
        },
        "rowCount": len(rows),
        "panelRowCounts": {panel: sum(item["panel"] == panel for item in rows) for panel in "ABC"},
        "isFittedScalingLaw": False,
        "isNavierStokesSimulation": False,
        "isComplexityLowerBound": False,
        "solver": "none",
        "randomSeed": "not applicable",
        "dgxUsed": False,
        "scientificWallTimeSeconds": time.monotonic() - START,
        "outputs": [item for name in output_names
                    if (item := record_if_present(output_dir / name)) is not None],
    }
    (output_dir / "results.json").write_text(canonical(results), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
