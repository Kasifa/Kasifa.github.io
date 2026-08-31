#!/usr/bin/env python3
"""Render the formal R0.73O finite Kolmogorov spectrum diagnostic."""

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
import shutil
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
from matplotlib.ticker import ScalarFormatter  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image, ImageOps  # noqa: E402
import pypdfium2 as pdfium  # noqa: E402


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CERTIFICATE = ROOT / "research/certificates/r073o"
INDEPENDENT = CERTIFICATE / "independent_validation.json"
START = time.monotonic()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def load_json(path: Path) -> dict:
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
                "gpu": "not used",
                "executionHost": "local workstation",
            }, sort_keys=True) + "\n")


def configure_style(config: dict) -> None:
    palette = config["palette"]
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.2,
        "axes.titlesize": 8.2,
        "axes.labelsize": 6.8,
        "axes.edgecolor": palette["midGrey"],
        "axes.linewidth": 0.65,
        "axes.facecolor": palette["paper"],
        "figure.facecolor": palette["paper"],
        "savefig.facecolor": palette["paper"],
        "xtick.labelsize": 5.9,
        "ytick.labelsize": 5.9,
        "xtick.color": palette["ink"],
        "ytick.color": palette["ink"],
        "text.color": palette["ink"],
        "axes.labelcolor": palette["ink"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "lines.solid_capstyle": "round",
    })


def panel_heading(ax: plt.Axes, letter: str, title: str) -> None:
    ax.text(-0.12, 1.08, letter, transform=ax.transAxes, fontsize=9.4,
            fontweight="bold", va="bottom")
    ax.text(-0.015, 1.08, title, transform=ax.transAxes, fontsize=7.8,
            fontweight="bold", va="bottom")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def render(config: dict, contract: dict, diagnostic: dict, rows: list[dict[str, str]]) -> None:
    configure_style(config)
    palette = config["palette"]
    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    fig, axes = plt.subplots(1, 2, figsize=(width, height))
    fig.subplots_adjust(left=0.085, right=0.982, bottom=0.245, top=0.73, wspace=0.36)
    fig.text(
        0.06, 0.935,
        "R0.73O | finite Kolmogorov spectrum diagnostic",
        fontsize=11.0, fontweight="bold", color=palette["blueDark"],
    )
    fig.text(
        0.06, 0.867,
        r"Exact cube embedding: $N=10$, $m=7$, $\alpha=0.7$, $R=3.012$; "
        "published interval certificate remains the theorem-level input",
        fontsize=6.8, color=palette["midGrey"],
    )

    sweep = [row for row in rows if row["record_type"] == "sweep"]
    convergence = [row for row in rows if row["record_type"] == "convergence"]
    if len(sweep) != 121 or len(convergence) != 10:
        raise RuntimeError("source-data row inventory drift")

    critical_low, critical_high = diagnostic["externalRigorousInput"]["criticalInterval"]
    critical_mid = (critical_low + critical_high) / 2.0
    target_r = diagnostic["parameters"]["targetReynolds"]
    finite_crossing = diagnostic["finiteResults"]["finiteCriticalCrossing"]
    target_sigma = diagnostic["finiteResults"]["leadingEigenvalueReal"]

    ax = axes[0]
    reynolds = np.array([float(row["reynolds"]) for row in sweep])
    abscissa = np.array([float(row["spectral_abscissa"]) for row in sweep])
    ax.plot(reynolds, abscissa, color=palette["blueDark"], lw=1.8)
    ax.fill_between(
        reynolds, 0, abscissa, where=abscissa >= 0,
        color=palette["blueLight"], alpha=0.22, interpolate=True,
    )
    ax.axhline(0, color=palette["midGrey"], lw=0.75, ls="--")
    ax.axvline(critical_mid, color=palette["gold"], lw=1.5,
               label="rigorous critical interval")
    ax.axvline(target_r, color=palette["blue"], lw=1.15, ls=":",
               label=r"target $R=3.012$")
    ax.scatter([target_r], [target_sigma], s=25, facecolor=palette["gold"],
               edgecolor=palette["paper"], lw=0.65, zorder=5)
    ax.annotate(
        r"$\sigma_{\max}=3.7327\times10^{-5}$",
        xy=(target_r, target_sigma), xytext=(3.018, 0.0012),
        fontsize=5.8, color=palette["ink"],
        arrowprops={"arrowstyle": "-", "lw": 0.55, "color": palette["midGrey"]},
    )
    ax.text(
        0.025, 0.955,
        "critical width $2\\times10^{-12}$\n(below plot resolution)",
        transform=ax.transAxes, va="top", fontsize=5.5, color=palette["midGrey"],
        bbox={"boxstyle": "round,pad=0.22", "fc": palette["paper"],
              "ec": palette["lightGrey"], "lw": 0.5},
    )
    ax.set_xlim(reynolds.min(), reynolds.max())
    ax.set_xlabel("Reynolds parameter $R$")
    ax.set_ylabel(r"finite spectral abscissa $\max\Re\sigma$")
    formatter = ScalarFormatter(useMathText=True)
    formatter.set_powerlimits((-2, 2))
    ax.yaxis.set_major_formatter(formatter)
    ax.grid(axis="y", color=palette["lightGrey"], lw=0.45, alpha=0.8)
    ax.legend(frameon=False, fontsize=5.4, loc="lower right", handlelength=2.4)
    ax.text(
        0.025, 0.055,
        f"finite crossing {finite_crossing:.13f}",
        transform=ax.transAxes, ha="left", va="bottom", fontsize=5.4,
        color=palette["midGrey"],
    )
    panel_heading(ax, "A", "Local spectral crossing")

    ax = axes[1]
    truncation = np.array([int(row["truncation"]) for row in convergence])
    sigma = np.array([float(row["spectral_abscissa"]) for row in convergence])
    residual = np.array([float(row["relative_residual"]) for row in convergence])
    reference = sigma[-1]
    error = np.abs(sigma - reference)
    positive_error = np.maximum(error, np.finfo(float).eps * abs(reference))
    ax.semilogy(
        truncation, positive_error, color=palette["blueDark"], marker="o",
        ms=3.6, lw=1.35, label=r"$|\sigma_M-\sigma_{120}|$",
    )
    ax.semilogy(
        truncation, residual, color=palette["gold"], marker="s", mfc=palette["paper"],
        ms=3.2, lw=1.05, ls="--", label="relative eigen-residual",
    )
    ax.set_xlabel("Fourier half-width $M$ (matrix size $2M+1$)")
    ax.set_ylabel("absolute scale")
    ax.set_xlim(6, 124)
    lower = min(positive_error.min(), residual.min()) / 3
    upper = max(positive_error.max(), residual.max()) * 4
    ax.set_ylim(max(lower, 1e-19), min(upper, 1e-10))
    ax.grid(axis="y", which="both", color=palette["lightGrey"], lw=0.45, alpha=0.8)
    ax.legend(frameon=False, fontsize=5.5, loc="upper right", handlelength=2.3)
    physical_growth = diagnostic["finiteResults"]["physicalGrowthRate"]
    efolding = diagnostic["finiteResults"]["physicalEfoldingTime"]
    ax.text(
        0.035, 0.06,
        "$M=120$ finite value\n"
        f"$\\sigma={reference:.10e}$\n"
        f"$\\lambda=AN\\sigma={physical_growth:.8f}$\n"
        f"e-fold time $={efolding:.2f}$",
        transform=ax.transAxes, fontsize=5.45, va="bottom",
        bbox={"boxstyle": "round,pad=0.28", "fc": palette["paper"],
              "ec": palette["lightGrey"], "lw": 0.55},
    )
    panel_heading(ax, "B", "Truncation and residual check")

    fig.text(
        0.06, 0.092,
        "FINITE / ILLUSTRATIVE: the blue computation independently reproduces the sign and scaling; "
        "the gold critical interval is imported from the computer-assisted proof.",
        fontsize=5.65, color=palette["midGrey"],
    )
    fig.text(
        0.06, 0.043,
        "This figure does not certify the infinite-dimensional spectrum, nonlinear escape, a 3D mode, "
        "singularity, turbulence, or the Clay conclusion.",
        fontsize=5.55, color=palette["midGrey"],
    )
    metadata = {
        "Title": "R0.73O finite Kolmogorov spectrum diagnostic",
        "Author": "ChuiKuan Zeng",
        "Subject": contract["evidenceClass"],
    }
    fig.savefig(HERE / "figure.pdf", metadata=metadata)
    fig.savefig(HERE / "figure.svg", metadata={"Title": metadata["Title"]})
    fig.savefig(HERE / "figure.png", dpi=int(config["pngDpi"]),
                metadata={"Title": metadata["Title"]})
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
    independent = load_json(INDEPENDENT)
    if diagnostic.get("status") != "passed" or diagnostic.get("allChecksPass") is not True:
        raise RuntimeError("upstream diagnostic did not pass")
    if independent.get("status") != "passed" or independent.get("allChecksPass") is not True:
        raise RuntimeError("independent finite recomputation did not pass")
    if config["claimBoundary"] != contract["claimBoundary"]:
        raise RuntimeError("figure claim-boundary drift")
    if diagnostic["claimBoundary"] != contract["claimBoundary"]:
        raise RuntimeError("diagnostic/figure claim-boundary drift")

    monitor = Monitor()
    monitor.event("start")
    source = CERTIFICATE / "source-data.csv"
    shutil.copyfile(source, HERE / "source-data.csv")
    rows = read_rows(HERE / "source-data.csv")
    monitor.event("source-data", rows=len(rows))
    render(config, contract, diagnostic, rows)
    monitor.event("rendered", formats=3)
    make_qa(config)
    monitor.event("qa-renders", surfaces=3)

    outputs = [
        HERE / "source-data.csv",
        HERE / "figure.pdf",
        HERE / "figure.svg",
        HERE / "figure.png",
        HERE / "qa-final-size.png",
        HERE / "qa-grayscale.png",
        HERE / "qa-pdf.png",
    ]
    environment = {
        "schemaVersion": "r073o-kolmogorov-spectrum-figure-environment-v1",
        "createdUtc": utc_now(),
        "python": platform.python_version(),
        "matplotlib": package_version("matplotlib"),
        "numpy": np.__version__,
        "pillow": package_version("pillow"),
        "pypdfium2": package_version("pypdfium2"),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "compute": {
            "processes": 1,
            "gpu": "not used",
            "executionHost": "local workstation",
            "wallTimeSeconds": time.monotonic() - START,
            "maximumResidentSetMiB": rss_mib(),
        },
        "inputs": [
            {
                "path": str(path.relative_to(ROOT)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in (
                CERTIFICATE / "config.json",
                CERTIFICATE / "diagnostic.json",
                INDEPENDENT,
                CERTIFICATE / "source-data.csv",
            )
        ],
    }
    (HERE / "environment.json").write_text(canonical(environment), encoding="utf-8")
    results = {
        "schemaVersion": "r073o-kolmogorov-spectrum-figure-results-v1",
        "status": "rendered",
        "figureId": contract["figureId"],
        "release": contract["release"],
        "sourceRows": len(rows),
        "finiteResults": diagnostic["finiteResults"],
        "independentFiniteResults": independent["independentFiniteResults"],
        "producerComparison": independent["producerComparison"],
        "claimBoundary": contract["claimBoundary"],
        "outputs": [
            {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in outputs
        ],
    }
    (HERE / "results.json").write_text(canonical(results), encoding="utf-8")
    monitor.event("complete", allRenderChecksPass=True)
    print(canonical({
        "status": "rendered",
        "figureId": contract["figureId"],
        "sourceRows": len(rows),
        "outputs": [path.name for path in outputs[1:]],
    }), end="")


if __name__ == "__main__":
    main()
