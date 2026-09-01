#!/usr/bin/env python3
"""Render the reproducible R0.73X exterior-tail ledger journal figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import platform
import re
import resource
import socket
import subprocess
import sys
import time
from typing import Any

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
import numpy as np
from PIL import Image, ImageOps
import pypdfium2 as pdfium


HERE = Path(__file__).resolve().parent
DEFAULT_REPOSITORY = HERE.parents[2]
FIGURE_ID = "fig-r073x-exterior-tail-ledger"
CSV_FIELDS = (
    "panel", "series", "record", "x", "y", "x_name", "y_name",
    "formula", "evidence_class", "source_path", "source_sha256",
    "normalization", "note", "raw_value",
)
EXPECTED_PACKAGES = {
    "matplotlib": "3.10.6",
    "numpy": "2.5.2",
    "pillow": "12.3.0",
    "pypdf": "6.10.0",
    "pypdfium2": "5.13.0",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def compact(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    need(isinstance(value, dict), "JSON root must be an object: " + str(path))
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def number(value: float) -> str:
    return format(float(value), ".17g")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def package_versions() -> dict[str, str]:
    return {name: importlib.metadata.version(name) for name in EXPECTED_PACKAGES}


def memory_gib() -> float:
    try:
        return round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / (1024 ** 3), 3)
    except (ValueError, OSError, AttributeError):
        return 0.0


def git_bytes(repository: Path, revision_path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repository), "show", revision_path],
        check=True,
        capture_output=True,
    ).stdout


def verify_inputs(repository: Path, contract: dict[str, Any]) -> dict[str, Any]:
    source_commit = contract["sourceCommit"]
    for source in contract["sources"]:
        path = repository / source["path"]
        need(path.is_file() and not path.is_symlink(), "missing source: " + source["path"])
        need(sha256(path) == source["sha256"], "source hash drift: " + source["path"])
        need(
            git_bytes(repository, f"{source_commit}:{source['path']}") == path.read_bytes(),
            "source differs from immutable Git blob: " + source["path"],
        )
        dirty = subprocess.run(
            ["git", "-C", str(repository), "status", "--porcelain=v1", "--", source["path"]],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        need(not dirty, "source path is dirty: " + source["path"])

    proof = (repository / "research/r073x_exterior_tail_freeze.md").read_text(encoding="utf-8")
    gaussian_match = re.search(r"\\frac\{4\^\{m-1\}\}\{(\d+)\\theta\}", proof)
    pressure_match = re.search(r"\(2\^mR\)\^\{-(\d+)\}", proof)
    need(gaussian_match is not None, "cannot parse Gaussian denominator")
    need(pressure_match is not None, "cannot parse pressure exponent")
    gaussian_denominator = int(gaussian_match.group(1))
    pressure_power = int(pressure_match.group(1))
    need(gaussian_denominator == contract["parsedConstants"]["gaussianDenominator"], "Gaussian parsed constant drift")
    need(pressure_power == contract["parsedConstants"]["harmonicPressurePower"], "pressure parsed constant drift")

    certificate = load_json(repository / "research/r073x_gaussian_tail_certificate.json")
    need(certificate["overall"] == "PASS", "Gaussian certificate not PASS")
    need(certificate["payload_sha256"] == contract["certificate"]["payloadSha256"], "Gaussian payload drift")
    need(certificate["claim_boundary"]["pde_regularization"] is False, "PDE claim boundary widened")
    audit = (repository / "research/r073x_gaussian_tail_independent_audit.md").read_text(encoding="utf-8")
    pressure_audit = (repository / "research/r073x_pressure_tail_independent_audit.md").read_text(encoding="utf-8")
    need("PASS WITH THE ORIGINAL CLAIM BOUNDARY" in audit, "Gaussian final audit verdict missing")
    need("PASS_FOR_POSITIVE_SCALE_ABSOLUTE_SIZE_ONLY" in pressure_audit, "pressure final audit verdict missing")
    return {
        "certificate": certificate,
        "gaussianDenominator": gaussian_denominator,
        "pressurePower": pressure_power,
    }


def row(
    panel: str,
    series: str,
    record: str,
    x: float,
    y: float,
    x_name: str,
    y_name: str,
    formula: str,
    evidence_class: str,
    source_path: str,
    source_sha256: str,
    normalization: str,
    note: str,
    raw_value: float,
) -> dict[str, str]:
    return {
        "panel": panel,
        "series": series,
        "record": record,
        "x": number(x),
        "y": number(y),
        "x_name": x_name,
        "y_name": y_name,
        "formula": formula,
        "evidence_class": evidence_class,
        "source_path": source_path,
        "source_sha256": source_sha256,
        "normalization": normalization,
        "note": note,
        "raw_value": number(raw_value),
    }


def generate_rows(
    repository: Path,
    config: dict[str, Any],
    contract: dict[str, Any],
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    verified = verify_inputs(repository, contract)
    denominator = verified["gaussianDenominator"]
    pressure_power = verified["pressurePower"]
    certificate = verified["certificate"]
    source_map = {source["path"]: source["sha256"] for source in contract["sources"]}
    proof_path = "research/r073x_exterior_tail_freeze.md"
    cert_path = "research/r073x_gaussian_tail_certificate.json"
    rows: list[dict[str, str]] = []

    a = config["panelA"]
    for theta in a["thetaValues"]:
        theta = float(theta)
        for m in range(int(a["annulusMinimum"]), int(a["annulusMaximum"]) + 1):
            value = theta ** -2.0 * math.exp(-(4.0 ** (m - 1)) / (denominator * theta))
            rows.append(row(
                "A", f"theta-{theta:g}", f"m-{m:02d}", m, value,
                "annulus index m", "gamma_m(theta)",
                f"theta^(-2)*exp(-4^(m-1)/({denominator}*theta))",
                "analytic formula", proof_path, source_map[proof_path],
                "none", f"theta={theta:g}; renderer coordinate", value,
            ))

    b = config["panelB"]
    first = int(b["normalizationAnnulus"])
    theta = float(b["theta"])
    gaussian_first = theta ** -2.0 * math.exp(-(4.0 ** (first - 1)) / (denominator * theta))
    algebraic_first = 2.0 ** (-pressure_power * first)
    for m in range(int(b["annulusMinimum"]), int(b["annulusMaximum"]) + 1):
        gaussian_raw = theta ** -2.0 * math.exp(-(4.0 ** (m - 1)) / (denominator * theta))
        gaussian_value = gaussian_raw / gaussian_first
        rows.append(row(
            "B", "gaussian-normalized", f"m-{m:02d}", m, gaussian_value,
            "annulus index m", "normalized decay factor",
            f"exp(-4^(m-1)/({denominator}*theta)); theta=1",
            "analytic formula", proof_path, source_map[proof_path],
            f"divided by value at m={first}",
            "Gaussian heat-tail shape; not interchangeable with pressure row",
            gaussian_raw,
        ))
        algebraic_raw = 2.0 ** (-pressure_power * m)
        algebraic_value = algebraic_raw / algebraic_first
        rows.append(row(
            "B", "pressure-algebraic-normalized", f"m-{m:02d}", m, algebraic_value,
            "annulus index m", "normalized decay factor",
            f"(2^m*R)^(-{pressure_power}); R factor cancels under normalization",
            "analytic formula", proof_path, source_map[proof_path],
            f"divided by value at m={first}",
            "harmonic-pressure shape; pays a different quantity",
            algebraic_raw,
        ))

    packet = certificate["packet_concentration"]
    packet_rows = packet["numeric_rows"]
    normalization_delta = float(config["panelC"]["normalizationDelta"])
    base = next(item for item in packet_rows if float(item["delta"]) == normalization_delta)
    for item in packet_rows:
        delta = float(item["delta"])
        l3_raw = float(item["weighted_L3"])
        l2_raw = float(item["weighted_L2_to_three_halves"])
        rows.append(row(
            "C", "weighted-L3", f"delta-{delta:g}", delta,
            l3_raw / float(base["weighted_L3"]), "packet scale delta",
            "normalized functional", "direct packet quadrature; expected delta^3",
            "static functional diagnostic", cert_path, source_map[cert_path],
            f"divided by weighted_L3 at delta={normalization_delta:g}",
            "smooth static divergence-free packet; NOT DNS", l3_raw,
        ))
        rows.append(row(
            "C", "weighted-L2-to-3/2", f"delta-{delta:g}", delta,
            l2_raw / float(base["weighted_L2_to_three_halves"]), "packet scale delta",
            "normalized functional", "direct packet quadrature; expected delta^(9/2)",
            "static functional diagnostic", cert_path, source_map[cert_path],
            f"divided by weighted_L2_to_three_halves at delta={normalization_delta:g}",
            "velocity-only L2 proxy; NOT DNS", l2_raw,
        ))
    smallest = min(packet_rows, key=lambda item: float(item["delta"]))
    rows.append(row(
        "C", "ratio-landmark", "smallest-delta-ratio", float(smallest["delta"]),
        float(smallest["ratio"]), "packet scale delta", "raw L3 / L2^(3/2)",
        "weighted_L3 / weighted_L2_to_three_halves",
        "static functional diagnostic", cert_path, source_map[cert_path],
        "unscaled ratio from audited certificate",
        "annotation landmark only; unconstrained velocity-functional quantifier",
        float(smallest["ratio"]),
    ))
    return rows, verified


def write_csv(rows: list[dict[str, str]]) -> None:
    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def selected(rows: list[dict[str, str]], panel: str, series: str) -> list[dict[str, str]]:
    return [item for item in rows if item["panel"] == panel and item["series"] == series]


def xy(rows: list[dict[str, str]], panel: str, series: str) -> tuple[np.ndarray, np.ndarray]:
    items = selected(rows, panel, series)
    return (
        np.asarray([float(item["x"]) for item in items], dtype=float),
        np.asarray([float(item["y"]) for item in items], dtype=float),
    )


def configure_matplotlib(palette: dict[str, str]) -> None:
    matplotlib.rcParams.update({
        "axes.edgecolor": palette["midGrey"],
        "axes.facecolor": palette["paper"],
        "axes.labelcolor": palette["ink"],
        "axes.linewidth": 0.7,
        "axes.titlecolor": palette["ink"],
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "font.size": 7.2,
        "mathtext.fontset": "dejavusans",
        "pdf.compression": 9,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.facecolor": palette["paper"],
        "svg.fonttype": "none",
        "svg.hashsalt": FIGURE_ID,
        "text.color": palette["ink"],
        "xtick.color": palette["midGrey"],
        "ytick.color": palette["midGrey"],
    })


def style_axis(ax: Any, palette: dict[str, str]) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", which="major", labelsize=6.2, length=2.5, width=0.6, pad=2.0)
    ax.grid(True, which="major", color=palette["gridGrey"], linewidth=0.55, alpha=0.95)
    ax.grid(True, which="minor", color=palette["gridGrey"], linewidth=0.35, alpha=0.4)
    ax.set_axisbelow(True)


def panel_header(ax: Any, label: str, title: str, subtitle: str) -> None:
    ax.text(0.0, 1.17, f"{label}  {title}", transform=ax.transAxes, ha="left", va="bottom",
            fontsize=8.25, fontweight="semibold", clip_on=False)
    ax.text(0.0, 1.07, subtitle, transform=ax.transAxes, ha="left", va="bottom",
            fontsize=5.65, color="#66717b", clip_on=False)


def add_research_blossom(fig: Any, palette: dict[str, str]) -> None:
    center_x, center_y = 0.969, 0.947
    for index in range(5):
        angle = 90.0 + 72.0 * index
        radians = math.radians(angle)
        petal = Ellipse(
            (center_x + 0.0085 * math.cos(radians), center_y + 0.014 * math.sin(radians)),
            width=0.0125, height=0.024, angle=angle - 90.0,
            transform=fig.transFigure,
            facecolor=matplotlib.colors.to_rgba(palette["blue"], 0.17),
            edgecolor=palette["blue"], linewidth=0.5, zorder=20,
        )
        petal.set_gid(f"research-blossom-petal-{index + 1}")
        fig.add_artist(petal)
    center = Circle(
        (center_x, center_y), 0.0035, transform=fig.transFigure,
        facecolor=palette["gold"], edgecolor=palette["paper"], linewidth=0.35, zorder=21,
    )
    center.set_gid("research-blossom-center")
    fig.add_artist(center)


def render(rows: list[dict[str, str]], config: dict[str, Any]) -> dict[str, Any]:
    palette = config["palette"]
    configure_matplotlib(palette)
    mm = 1.0 / 25.4
    width = float(config["widthMillimetres"]) * mm
    height = float(config["heightMillimetres"]) * mm
    fig, axes = plt.subplots(1, 3, figsize=(width, height), facecolor=palette["paper"])
    # The active macOS backend quantizes the constructor size to 0.01 inch.
    # Reapply the exact dimensions before layout/export so PDF and 600 dpi PNG
    # encode the declared 178 mm by 92 mm physical footprint.
    fig.set_size_inches(width, height, forward=False)
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.205, top=0.755, wspace=0.38)
    fig.text(0.075, 0.955, "Exterior-tail ledger", ha="left", va="top",
             fontsize=11.0, fontweight="semibold", color=palette["ink"])
    fig.text(0.928, 0.955, "R0.73X  ·  formula / certificate evidence",
             ha="right", va="top", fontsize=6.1, color=palette["midGrey"])
    add_research_blossom(fig, palette)
    fig.text(0.5, 0.028,
             "A–B analytic formula  ·  C static functional diagnostic  ·  NOT DNS  ·  NOT CLAY",
             ha="center", va="bottom", fontsize=5.7, color=palette["midGrey"])

    ax = axes[0]
    style_axis(ax, palette)
    panel_header(ax, "A", "Gaussian annular decay", "analytic formula  ·  log scale")
    styles = [
        ("theta-1", palette["blue"], "-", "o", palette["blue"], r"$\theta=1$"),
        ("theta-0.5", palette["gold"], (0, (4, 2)), "s", palette["paper"], r"$\theta=1/2$"),
        ("theta-0.25", palette["midGrey"], (0, (1.2, 1.5)), "^", palette["paper"], r"$\theta=1/4$"),
    ]
    for series, color, line_style, marker, face, label in styles:
        xs, ys = xy(rows, "A", series)
        ax.plot(xs, ys, color=color, linestyle=line_style, linewidth=1.35,
                marker=marker, markersize=3.8, markerfacecolor=face,
                markeredgecolor=color, markeredgewidth=0.8, label=label, zorder=3)
    ax.set_yscale("log")
    ax.set_ylim(float(config["panelA"]["yMinimum"]), float(config["panelA"]["yMaximum"]))
    ax.set_yticks([10.0 ** exponent for exponent in config["panelA"]["majorTickExponents"]])
    ax.set_xlim(0.8, 7.2)
    ax.set_xticks(range(1, 8))
    ax.set_xlabel("annulus index  $m$", fontsize=6.6)
    ax.set_ylabel(r"$\gamma_m(\theta)$", fontsize=6.6)
    ax.legend(loc="lower left", fontsize=5.7, frameon=False, handlelength=2.8,
              borderaxespad=0.2, labelspacing=0.35)

    ax = axes[1]
    style_axis(ax, palette)
    panel_header(ax, "B", "Heat vs pressure tail", "analytic formula  ·  normalized at $m=1$")
    xs, ys = xy(rows, "B", "gaussian-normalized")
    ax.plot(xs, ys, color=palette["blue"], linewidth=1.45, linestyle="-",
            marker="o", markersize=3.8, markerfacecolor=palette["blue"],
            markeredgecolor=palette["blue"], label="Gaussian heat", zorder=3)
    xs2, ys2 = xy(rows, "B", "pressure-algebraic-normalized")
    ax.plot(xs2, ys2, color=palette["gold"], linewidth=1.35, linestyle=(0, (4, 2)),
            marker="s", markersize=3.8, markerfacecolor=palette["paper"],
            markeredgecolor=palette["gold"], markeredgewidth=0.9,
            label=r"pressure  $2^{-4(m-1)}$", zorder=3)
    ax.set_yscale("log")
    ax.set_ylim(float(config["panelB"]["yMinimum"]), float(config["panelB"]["yMaximum"]))
    ax.set_yticks([10.0 ** exponent for exponent in config["panelB"]["majorTickExponents"]])
    ax.set_xlim(0.8, 7.2)
    ax.set_xticks(range(1, 8))
    ax.set_xlabel("annulus index  $m$", fontsize=6.6)
    ax.set_ylabel("normalized decay factor", fontsize=6.6)
    ax.legend(loc="lower left", fontsize=5.55, frameon=False, handlelength=2.8,
              borderaxespad=0.2, labelspacing=0.35)
    ax.text(0.97, 0.47, "shape only\nnot interchangeable",
            transform=ax.transAxes, ha="right", va="center", fontsize=5.25,
            color=palette["midGrey"],
            bbox={"boxstyle": "square,pad=0.22", "facecolor": palette["paper"],
                  "edgecolor": palette["lightGrey"], "linewidth": 0.55})

    ax = axes[2]
    style_axis(ax, palette)
    panel_header(ax, "C", "Packet scaling", "static functional diagnostic  ·  NOT DNS")
    xs, ys = xy(rows, "C", "weighted-L3")
    order = np.argsort(xs)
    ax.plot(xs[order], ys[order], color=palette["blue"], linewidth=1.45,
            linestyle="-", marker="o", markersize=4.0,
            markerfacecolor=palette["blue"], markeredgecolor=palette["blue"],
            label=r"weighted $L^3$  ($\delta^3$)", zorder=4)
    xs2, ys2 = xy(rows, "C", "weighted-L2-to-3/2")
    order2 = np.argsort(xs2)
    ax.plot(xs2[order2], ys2[order2], color=palette["gold"], linewidth=1.35,
            linestyle=(0, (4, 2)), marker="s", markersize=4.0,
            markerfacecolor=palette["paper"], markeredgecolor=palette["gold"],
            markeredgewidth=0.9, label=r"$L^2$ proxy  ($\delta^{9/2}$)", zorder=4)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ticks = [1/64, 1/32, 1/16, 1/8, 1/4]
    ax.set_xticks(ticks, ["1/64", "1/32", "1/16", "1/8", "1/4"])
    ax.set_xlim(1/72, 0.29)
    ax.set_xlabel(r"packet scale  $\delta$", fontsize=6.6)
    ax.set_ylabel("normalized functional", fontsize=6.6)
    ax.legend(loc="upper left", fontsize=5.45, frameon=False, handlelength=2.6,
              borderaxespad=0.2, labelspacing=0.35)
    landmark = selected(rows, "C", "ratio-landmark")[0]
    delta = float(landmark["x"])
    ratio = float(landmark["y"])
    l3_at_delta = float(next(item["y"] for item in selected(rows, "C", "weighted-L3")
                             if abs(float(item["x"]) - delta) < 1e-15))
    ax.annotate(
        f"raw ratio = {ratio:.1f}", xy=(delta, l3_at_delta), xycoords="data",
        xytext=(0.33, 0.37), textcoords="axes fraction", fontsize=5.35,
        color=palette["midGrey"], ha="left", va="center",
        arrowprops={"arrowstyle": "->", "color": palette["midGrey"], "linewidth": 0.65},
        bbox={"boxstyle": "square,pad=0.18", "facecolor": palette["paper"],
              "edgecolor": palette["lightGrey"], "linewidth": 0.5},
    )

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    figure_box = fig.bbox
    bounds_failures: list[str] = []
    for artist in fig.findobj(match=lambda item: isinstance(item, matplotlib.text.Text)):
        if not artist.get_visible() or not artist.get_text().strip():
            continue
        box = artist.get_window_extent(renderer=renderer)
        if box.x0 < figure_box.x0 - 3 or box.y0 < figure_box.y0 - 3 or box.x1 > figure_box.x1 + 3 or box.y1 > figure_box.y1 + 3:
            bounds_failures.append(artist.get_text())

    metadata = {"Creator": "R0.73X deterministic figure renderer", "Date": None}
    fig.savefig(HERE / "figure.svg", format="svg", metadata=metadata)
    svg_path = HERE / "figure.svg"
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    fig.savefig(HERE / "figure.pdf", format="pdf", metadata={"Creator": metadata["Creator"], "CreationDate": None, "ModDate": None})
    fig.savefig(HERE / "figure.png", format="png", dpi=int(config["pngDpi"]),
                metadata={"Software": metadata["Creator"]})
    plt.close(fig)

    with Image.open(HERE / "figure.png") as opened:
        master = opened.convert("RGB")
        qa_width = min(int(config["qaMaximumWidthPixels"]), master.width)
        qa_height = round(master.height * qa_width / master.width)
        final_size = master.resize((qa_width, qa_height), Image.Resampling.LANCZOS)
        final_size.save(HERE / "qa-final-size.png")
        ImageOps.grayscale(final_size).convert("RGB").save(HERE / "qa-grayscale.png")

    document = pdfium.PdfDocument(str(HERE / "figure.pdf"))
    need(len(document) == 1, "rendered PDF is not one page")
    page = document[0]
    width_points, _ = page.get_size()
    pdf_image = page.render(scale=int(config["qaMaximumWidthPixels"]) / float(width_points)).to_pil().convert("RGB")
    pdf_image.save(HERE / "qa-pdf.png")
    pdf_pixels = [pdf_image.width, pdf_image.height]
    page.close()
    document.close()
    return {
        "artistBoundsFailures": bounds_failures,
        "artistBoundsPass": not bounds_failures,
        "figureInches": [width, height],
        "masterPngPixels": list(master.size),
        "qaFinalSizePixels": list(final_size.size),
        "pdfQaPixels": pdf_pixels,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=DEFAULT_REPOSITORY)
    parser.add_argument("--render-preseal", action="store_true")
    parser.add_argument("--data-only", action="store_true")
    args = parser.parse_args()
    need(args.render_preseal != args.data_only, "choose exactly one of --render-preseal or --data-only")
    started = time.perf_counter()
    started_utc = utc_now()
    events: list[dict[str, object]] = []

    def event(name: str, **extra: object) -> None:
        events.append({"elapsedSeconds": round(time.perf_counter() - started, 6), "event": name, **extra})

    event("start", mode="render-preseal" if args.render_preseal else "data-only")
    repository = args.repository.resolve()
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    need(config["figureId"] == FIGURE_ID and contract["figureId"] == FIGURE_ID, "figure id drift")
    versions = package_versions()
    need(versions == EXPECTED_PACKAGES, "dependency version drift: " + repr(versions))
    rows, verified = generate_rows(repository, config, contract)
    event("inputs-verified", sourceCommit=contract["sourceCommit"], parsedGaussianDenominator=verified["gaussianDenominator"], parsedPressurePower=verified["pressurePower"])
    write_csv(rows)
    panel_counts = {panel: sum(item["panel"] == panel for item in rows) for panel in ("A", "B", "C")}
    event("source-data-written", rows=len(rows), panelCounts=panel_counts)
    render_report: dict[str, Any] = {"skipped": True}
    if args.render_preseal:
        render_report = render(rows, config)
        event("render-complete", outputs=["figure.svg", "figure.pdf", "figure.png"], qaAssets=["qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"])

    certificate = verified["certificate"]
    results = {
        "schemaVersion": "r073x-exterior-tail-ledger-results-v1",
        "allSourceChecksPass": True,
        "parsedConstants": {
            "gaussianDenominator": verified["gaussianDenominator"],
            "harmonicPressurePower": verified["pressurePower"],
        },
        "certificate": {
            "overall": certificate["overall"],
            "payloadSha256": certificate["payload_sha256"],
            "derivedExponents": certificate["packet_concentration"]["derived_exponents"],
            "finalNumericSlopes": {key: values[-1] for key, values in certificate["packet_concentration"]["numeric_slopes"].items()},
            "smallestDeltaRatio": certificate["packet_concentration"]["numeric_rows"][-1]["ratio"],
        },
        "panelRowCounts": panel_counts,
        "sourceDataRows": len(rows),
        "render": render_report,
        "scope": {
            "analyticFormulaPanels": ["A", "B"],
            "staticFunctionalDiagnosticPanels": ["C"],
            "navierStokesSimulation": False,
            "dns": False,
            "associatedPressureCounterexample": False,
            "dgxUsed": False,
            "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
            "notClay": True,
        },
    }
    (HERE / "results.json").write_text(canonical(results), encoding="utf-8")
    environment = {
        "schemaVersion": "r073x-exterior-tail-ledger-environment-v1",
        "createdUtc": started_utc,
        "execution": {
            "cpu": f"{platform.machine()} / {os.cpu_count() or 1} logical CPUs",
            "dgxUsed": False,
            "gpu": "not used",
            "host": socket.gethostname(),
            "memoryGiB": memory_gib(),
            "network": "not used",
            "operatingSystem": platform.platform(),
            "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
            "processes": 1,
            "python": platform.python_version(),
            "threadsPerProcess": 1,
        },
        "packages": versions,
        "runtime": {
            "pythonExecutable": sys.executable,
            "pythonPathEnvironment": os.environ.get("PYTHONPATH", ""),
            "imports": {
                "matplotlib": str(Path(matplotlib.__file__).resolve()),
                "numpy": str(Path(np.__file__).resolve()),
            },
        },
    }
    (HERE / "environment.json").write_text(canonical(environment), encoding="utf-8")
    event("metadata-written", status="hash-bound-prepublication")
    (HERE / "progress.ndjson").write_text("\n".join(compact(item) for item in events) + "\n", encoding="utf-8")
    resource_row = {
        "elapsedSeconds": round(time.perf_counter() - started, 6),
        "maximumResidentSetSizeRaw": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "processes": 1,
        "threadsPerProcess": 1,
    }
    (HERE / "resource-log.ndjson").write_text(compact(resource_row) + "\n", encoding="utf-8")
    print(canonical({"figureId": FIGURE_ID, "panelRowCounts": panel_counts, "rows": len(rows), "status": "ok"}), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
