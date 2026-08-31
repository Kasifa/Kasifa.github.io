#!/usr/bin/env python3
"""Render the formal R0.73N finite-strain bracket figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version as package_version
import json
import math
import platform
from pathlib import Path
import resource
import sys
import time


def bootstrap() -> None:
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()
import matplotlib as mpl  # noqa: E402

mpl.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageOps  # noqa: E402
import pypdfium2 as pdfium  # noqa: E402


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CERTIFICATE = ROOT / "research/certificates/r073n"
INPUTS = (
    CERTIFICATE / "diagnostic.json",
    CERTIFICATE / "source-data.csv",
    CERTIFICATE / "independent_validation.json",
    CERTIFICATE / "certificate.json",
    CERTIFICATE / "validation.json",
    CERTIFICATE / "manifest.json",
)
START = time.monotonic()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("JSON root is not an object: " + str(path))
    return value


def input_record(path: Path) -> dict[str, object]:
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


class Monitor:
    def __init__(self) -> None:
        self.progress = HERE / "progress.ndjson"
        self.resources = HERE / "resource-log.ndjson"
        self.progress.write_text("", encoding="utf-8")
        self.resources.write_text("", encoding="utf-8")

    def event(self, stage: str, **fields: object) -> None:
        timestamp = utc_now()
        elapsed = time.monotonic() - START
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({
                "stage": stage,
                "timestampUtc": timestamp,
                "elapsedSeconds": elapsed,
                **fields,
            }, sort_keys=True) + "\n")
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({
                "stage": stage,
                "timestampUtc": timestamp,
                "elapsedSeconds": elapsed,
                "maximumResidentSetMiB": rss_mib(),
                "processes": 1,
                "gpu": "not used",
            }, sort_keys=True) + "\n")


def configure_style(config: dict) -> None:
    palette = config["palette"]
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.2,
        "axes.titlesize": 8.2,
        "axes.labelsize": 6.7,
        "axes.edgecolor": palette["midGrey"],
        "axes.linewidth": 0.65,
        "axes.facecolor": palette["paper"],
        "figure.facecolor": palette["paper"],
        "savefig.facecolor": palette["paper"],
        "xtick.labelsize": 5.8,
        "ytick.labelsize": 5.8,
        "xtick.color": palette["ink"],
        "ytick.color": palette["ink"],
        "text.color": palette["ink"],
        "axes.labelcolor": palette["ink"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "lines.solid_capstyle": "round",
    })


def panel_heading(ax: plt.Axes, letter: str, title: str) -> None:
    ax.text(-0.13, 1.085, letter, transform=ax.transAxes, fontsize=9.5,
            fontweight="bold", va="bottom")
    ax.text(-0.01, 1.085, title, transform=ax.transAxes, fontsize=7.7,
            fontweight="bold", va="bottom")


def draw_figure(config: dict, rows: list[dict[str, str]], diagnostic: dict) -> None:
    configure_style(config)
    palette = config["palette"]
    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    fig, axes = plt.subplots(1, 3, figsize=(width, height))
    fig.subplots_adjust(left=0.072, right=0.985, bottom=0.225, top=0.745, wspace=0.39)
    fig.text(0.058, 0.938, "R0.73N | finite strain and marked-basepoint exponent bracket",
             fontsize=11.0, fontweight="bold", color=palette["blueDark"])
    fig.text(
        0.058, 0.875,
        "Exact heat-shear formulas; high-precision endpoint audit; no PDE solve and no sharp-modulus claim",
        fontsize=6.8, color=palette["midGrey"],
    )

    strain_rows = [row for row in rows if row["record_type"] == "strain_sample"]
    cumulative_rows = [row for row in rows if row["record_type"] == "cumulative_sample"]
    basepoint_rows = [row for row in rows if row["record_type"] == "marked_basepoint_sample"]
    if (len(strain_rows), len(cumulative_rows), len(basepoint_rows)) != (241, 243, 121):
        raise RuntimeError("source-data row inventory drift")

    ax = axes[0]
    t = np.array([float(row["t"]) for row in strain_rows])
    slow = np.array([float(row["slow_strain_component"]) for row in strain_rows])
    fast = np.array([float(row["fast_strain_component"]) for row in strain_rows])
    envelope = np.array([
        float(row["normalized_half_strain_envelope"]) for row in strain_rows
    ])
    ax.fill_between(t, 0, envelope, color=palette["blueLight"], alpha=0.22, linewidth=0)
    ax.plot(t, envelope, color=palette["blueDark"], lw=1.8,
            label=r"$e^{-4t}+e^{-16t}$")
    ax.plot(t, slow, color=palette["blue"], lw=1.0, ls="--", label=r"$e^{-4t}$")
    ax.plot(t, fast, color=palette["gold"], lw=1.0, ls=":", label=r"$e^{-16t}$")
    ax.scatter([0], [2], s=16, facecolor=palette["gold"], edgecolor="white", lw=0.5, zorder=5)
    ax.annotate("exact at $y=\\pi/2$", xy=(0, 2), xytext=(0.18, 1.73),
                fontsize=5.8, color=palette["midGrey"],
                arrowprops={"arrowstyle": "-", "lw": 0.55, "color": palette["midGrey"]})
    ax.set_xlim(0, float(config["displayTimeEnd"]))
    ax.set_ylim(0, 2.08)
    ax.set_xlabel("physical time $t$")
    ax.set_ylabel(r"$\|\partial_yF_\Lambda\|_\infty/(2\Lambda)$")
    ax.grid(axis="y", color=palette["lightGrey"], lw=0.45, alpha=0.8)
    ax.legend(frameon=False, fontsize=5.5, loc="upper right", handlelength=2.3)
    panel_heading(ax, "A", "Exact strain envelope")

    ax = axes[1]
    positive = [row for row in cumulative_rows if float(row["t"]) > 0]
    tc = np.array([float(row["t"]) for row in positive])
    jc = np.array([float(row["cumulative_j"]) for row in positive])
    j_inf = float(diagnostic["highPrecision"]["jInfinity"])
    j_star = float(diagnostic["highPrecision"]["jStar"])
    t_star = 1 / 1800
    ax.plot(tc, jc, color=palette["blueDark"], lw=1.8, label="$j(t)$")
    ax.axhline(j_inf, color=palette["gold"], lw=1.1, ls="--", label=r"$j(\infty)=5/16$")
    ax.scatter([t_star], [j_star], s=23, color=palette["gold"], edgecolor="white",
               lw=0.55, zorder=5)
    ax.annotate(
        "$T_*=1/1800$\n$j_*=1.108032\\times10^{-3}$",
        xy=(t_star, j_star), xytext=(0.0021, 0.083), fontsize=5.6,
        arrowprops={"arrowstyle": "-", "lw": 0.55, "color": palette["midGrey"]},
        color=palette["ink"],
    )
    ax.set_xscale("log")
    ax.set_xlim(1e-6, float(config["displayCumulativeTimeEnd"]))
    ax.set_ylim(0, 0.326)
    ax.set_xlabel("physical time $t$ (log scale)")
    ax.set_ylabel("cumulative $j(t)$")
    ax.grid(axis="y", color=palette["lightGrey"], lw=0.45, alpha=0.8)
    ax.legend(frameon=False, fontsize=5.5, loc="lower right", handlelength=2.3)
    ax.text(0.02, 0.045, "$j(0)=0$ (off log axis)", transform=ax.transAxes,
            fontsize=5.3, color=palette["midGrey"])
    panel_heading(ax, "B", "Finite cumulative strain")

    ax = axes[2]
    lambdas = np.array([float(row["lambda"]) for row in basepoint_rows])
    action_low = np.array([
        float(row["log10_action_factor_lower"]) for row in basepoint_rows
    ])
    action_high = np.array([
        float(row["log10_action_factor_upper"]) for row in basepoint_rows
    ])
    strain_upper = np.array([
        float(row["log10_strain_factor_upper"]) for row in basepoint_rows
    ])
    ax.fill_between(lambdas, action_low, action_high, color=palette["blue"], alpha=0.22,
                    label=r"inherited $\mathcal{A}_*$ interval")
    ax.plot(lambdas, action_low, color=palette["blue"], lw=0.85, ls="--")
    ax.plot(lambdas, action_high, color=palette["blueDark"], lw=1.25)
    ax.plot(lambdas, strain_upper, color=palette["gold"], lw=1.8,
            label=r"finite-strain $j_*$ factor")
    rational_lower = 359 / 324000
    rational_curve = lambdas * rational_lower / math.log(10)
    ax.plot(lambdas, rational_curve, color=palette["gold"], lw=0.9, ls=":",
            label=r"analytic $359/324000$")
    ax.set_xlim(0, float(config["displayLambdaEnd"]))
    ax.set_ylim(0, max(strain_upper) * 1.03)
    ax.set_xlabel(r"marked $\Lambda$ (top: exact $\|\overline{U}_\Lambda(0)\|_2$)")
    ax.set_ylabel(r"$\log_{10}$ exponent factor")
    ax.grid(axis="y", color=palette["lightGrey"], lw=0.45, alpha=0.8)
    ax.legend(frameon=False, fontsize=5.15, loc="upper left", handlelength=2.0)
    ax.text(
        0.98, 0.05,
        "$j_*>359/324000$\n$>173/450000>\\mathcal{A}_*$",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=5.6,
        bbox={"boxstyle": "round,pad=0.25", "fc": palette["paper"],
              "ec": palette["lightGrey"], "lw": 0.55},
    )
    norm_factor = math.sqrt(5 / 8)
    secondary = ax.secondary_xaxis(
        "top", functions=(lambda value: value * norm_factor,
                          lambda value: value / norm_factor),
    )
    secondary.set_xlabel("")
    secondary.tick_params(labelsize=5.2, pad=1.5)
    panel_heading(ax, "C", "Marked-basepoint bracket")

    fig.text(
        0.058, 0.075,
        "FINITE / ILLUSTRATIVE: exact-formula evaluations at different marked basepoints; "
        "not a sharp flow-map modulus or arbitrary fixed-background instability.",
        fontsize=5.7, color=palette["midGrey"],
    )
    fig.text(
        0.058, 0.035,
        "The action interval is inherited from sealed R0.73M analysis. Arbitrary fixed-background instability, full 3D FPS H3-L2, singularity, and Clay claims remain open.",
        fontsize=5.45, color=palette["midGrey"],
    )
    metadata = {
        "Title": "R0.73N finite strain and marked-basepoint exponent bracket",
        "Author": "ChuiKuan Zeng",
        "Subject": "Finite illustrative diagnostic; no continuum proof by computation",
    }
    fig.savefig(HERE / "figure.pdf", metadata=metadata)
    fig.savefig(HERE / "figure.svg", metadata={"Title": metadata["Title"]})
    fig.savefig(HERE / "figure.png", dpi=int(config["pngDpi"]), metadata={
        "Title": metadata["Title"],
    })
    plt.close(fig)


def make_qa(config: dict) -> None:
    target = (
        round(float(config["widthMillimetres"]) / 25.4 * int(config["qaDpi"])),
        round(float(config["heightMillimetres"]) / 25.4 * int(config["qaDpi"])),
    )
    with Image.open(HERE / "figure.png") as image:
        final = image.convert("RGB").resize(target, Image.Resampling.LANCZOS)
        final.save(HERE / "qa-final-size.png", dpi=(int(config["qaDpi"]),) * 2)
        ImageOps.grayscale(final).save(
            HERE / "qa-grayscale.png", dpi=(int(config["qaDpi"]),) * 2
        )
    document = pdfium.PdfDocument(str(HERE / "figure.pdf"))
    if len(document) != 1:
        raise RuntimeError("figure PDF must have exactly one page")
    page = document[0]
    bitmap = page.render(scale=int(config["qaDpi"]) / 72.0)
    bitmap.to_pil().convert("RGB").save(
        HERE / "qa-pdf.png", dpi=(int(config["qaDpi"]),) * 2
    )
    page.close()
    document.close()


def main() -> None:
    parse_args()
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    diagnostic = load_json(CERTIFICATE / "diagnostic.json")
    independent = load_json(CERTIFICATE / "independent_validation.json")
    certificate = load_json(CERTIFICATE / "certificate.json")
    validation = load_json(CERTIFICATE / "validation.json")
    manifest = load_json(CERTIFICATE / "manifest.json")
    if not all(payload.get("allChecksPass") is True for payload in (
        diagnostic, independent, certificate, validation,
    )):
        raise RuntimeError("upstream certificate inputs did not pass")
    if manifest.get("allPrerequisiteChecksPass") is not True:
        raise RuntimeError("upstream certificate manifest did not pass")
    source_commit_assigned = manifest.get("sourceCommitAssigned")
    if source_commit_assigned is True:
        if (
            manifest.get("status") != "sealed"
            or manifest.get("finalSeal") is not True
            or not isinstance(manifest.get("sourceCommit"), str)
            or len(manifest["sourceCommit"]) != 40
        ):
            raise RuntimeError("upstream certificate final-seal status drift")
    elif source_commit_assigned is False:
        if manifest.get("status") != "hash-bound-uncommitted" or manifest.get("finalSeal") is not False:
            raise RuntimeError("upstream certificate pre-seal status drift")
    else:
        raise RuntimeError("upstream certificate source-commit state drift")
    if config.get("claimBoundary") != contract.get("claimBoundary"):
        raise RuntimeError("figure claim boundary drift")
    monitor = Monitor()
    monitor.event("start", upstreamInputs=len(INPUTS))
    upstream_csv = CERTIFICATE / "source-data.csv"
    upstream_hash = sha256(upstream_csv)
    with upstream_csv.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        upstream_rows = list(reader)
        fields = list(reader.fieldnames or [])
    if len(upstream_rows) != 605:
        raise RuntimeError("upstream row count drift")
    figure_fields = fields + ["upstream_path", "upstream_sha256"]
    figure_rows = [
        {
            **row,
            "upstream_path": str(upstream_csv.relative_to(ROOT)),
            "upstream_sha256": upstream_hash,
        }
        for row in upstream_rows
    ]
    with (HERE / "source-data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=figure_fields)
        writer.writeheader()
        writer.writerows(figure_rows)
    monitor.event("source-data", rows=len(figure_rows))
    draw_figure(config, figure_rows, diagnostic)
    monitor.event("exports", pdf=True, svg=True, pngDpi=config["pngDpi"])
    make_qa(config)
    monitor.event("qa-surfaces", count=3)
    outputs = []
    for name in ("figure.pdf", "figure.svg", "figure.png"):
        path = HERE / name
        record = {"path": name, "bytes": path.stat().st_size, "sha256": sha256(path)}
        if name == "figure.png":
            with Image.open(path) as image:
                record["pixels"] = list(image.size)
                record["dpi"] = int(config["pngDpi"])
        outputs.append(record)
    counts = {
        "strainSamples": sum(row["record_type"] == "strain_sample" for row in figure_rows),
        "cumulativeSamples": sum(
            row["record_type"] == "cumulative_sample" for row in figure_rows
        ),
        "markedBasepointSamples": sum(
            row["record_type"] == "marked_basepoint_sample" for row in figure_rows
        ),
        "totalRows": len(figure_rows),
    }
    results = {
        "schemaVersion": "r073n-finite-strain-figure-results-v1",
        "release": "R0.73N",
        "figureId": config["figureId"],
        "status": "rendered-pending-visual-qa",
        "allComputationalChecksPass": True,
        "sourceRows": counts,
        "summary": {
            "jStar": diagnostic["highPrecision"]["jStar"],
            "jInfinity": diagnostic["highPrecision"]["jInfinity"],
            "jStarRationalLower": diagnostic["highPrecision"]["jStarRationalLower"],
            "inheritedActionLower": diagnostic["highPrecision"]["inheritedActionLower"],
            "inheritedActionUpper": diagnostic["highPrecision"]["inheritedActionUpper"],
            "margins": diagnostic["highPrecision"]["margins"],
            "maximumDisplayedLog10StrainFactor": max(
                float(row["log10_strain_factor_upper"])
                for row in figure_rows if row["record_type"] == "marked_basepoint_sample"
            ),
        },
        "figure": {
            "widthMillimetres": config["widthMillimetres"],
            "heightMillimetres": config["heightMillimetres"],
            "pngDpi": config["pngDpi"],
            "layout": "three-panel exact envelope, cumulative saturation, and exponent bracket",
            "outputs": outputs,
        },
        "claimBoundary": config["claimBoundary"],
    }
    (HERE / "results.json").write_text(canonical(results), encoding="utf-8")
    environment = {
        "schemaVersion": "r073n-finite-strain-figure-environment-v1",
        "createdUtc": utc_now(),
        "python": platform.python_version(),
        "matplotlib": mpl.__version__,
        "numpy": np.__version__,
        "Pillow": Image.__version__,
        "pypdf": package_version("pypdf"),
        "pypdfium2": package_version("pypdfium2"),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "inputs": [input_record(path) for path in INPUTS],
        "sourceCommitAssigned": source_commit_assigned,
        "compute": {
            "processes": 1,
            "gpu": "not used",
            "wallTimeSeconds": time.monotonic() - START,
        },
    }
    if source_commit_assigned:
        environment["sourceCommit"] = manifest["sourceCommit"]
    (HERE / "environment.json").write_text(canonical(environment), encoding="utf-8")
    monitor.event("complete", status="rendered-pending-visual-qa")
    print(canonical({
        "status": "rendered-pending-visual-qa",
        "rows": counts["totalRows"],
        "outputs": [row["path"] for row in outputs],
    }), end="")


if __name__ == "__main__":
    main()
