#!/usr/bin/env python3
"""Generate the R0.73T dynamic-autocorrelation formal figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
from importlib.metadata import PackageNotFoundError, version as package_version
import json
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
FIGURE_ID = "fig-r073t-dynamic-autocorrelation"
CERTIFICATE_SCRIPT = ROOT / "research/certificates/r073t/compute_exact_certificate.py"
CERTIFICATE_RESULTS = ROOT / "research/certificates/r073t/results.json"
CSV_FIELDS = (
    "panel", "series", "parameter", "x", "y", "quantity_class",
    "source_origin", "source_record_type", "formula", "normalization",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--output-dir", default=str(HERE))
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--data-only", action="store_true")
    modes.add_argument("--render-preseal", action="store_true")
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError("JSON root is not an object: " + str(path))
    return value


def installed_version(name: str) -> str | None:
    try:
        return package_version(name)
    except PackageNotFoundError:
        return None


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


class Monitor:
    def __init__(self, output: Path) -> None:
        self.progress = output / "progress.ndjson"
        self.resources = output / "resource-log.ndjson"
        self.progress.write_text("", encoding="utf-8")
        self.resources.write_text("", encoding="utf-8")

    def event(self, stage: str, **fields: object) -> None:
        stamp = utc_now()
        elapsed = time.monotonic() - START
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({
                "elapsedSeconds": elapsed,
                "stage": stage,
                "timestampUtc": stamp,
                **fields,
            }, sort_keys=True) + "\n")
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({
                "elapsedSeconds": elapsed,
                "executionHost": platform.node(),
                "gpu": "not used",
                "maximumResidentSetMiB": rss_mib(),
                "processes": 1,
                "stage": stage,
                "threadsPerProcess": 1,
                "timestampUtc": stamp,
            }, sort_keys=True) + "\n")


def verify_certificate() -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(CERTIFICATE_SCRIPT), "--check-only"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("R0.73T exact certificate failed: " + completed.stderr[-1200:])
    results = load_json(CERTIFICATE_RESULTS)
    audit = results.get("audit", {})
    if audit.get("passed") != audit.get("required") or audit.get("required") != 55:
        raise RuntimeError("R0.73T exact certificate check-count drift")
    six = results["sixMode"]["finiteIdentities"]
    required = {
        "E": "42", "Q": "2918", "A": "164", "D_C": 15,
        "X2": "4296", "Y": "1986", "N4": "-384",
        "N4MinusU": "384", "viscousQDerivativeCoefficient": "-16536",
    }
    for key, expected in required.items():
        if six.get(key) != expected:
            raise RuntimeError(f"certificate constant drift: {key}")
    rotating = results["rotatingShear"]
    if rotating.get("c0Derivative") != "-2*nu*N^2":
        raise RuntimeError("rotating-shear derivative drift")
    return results


def row(
    panel: str, series: str, parameter: int, x: float, y: float,
    quantity_class: str, source_record_type: str, formula: str,
    normalization: str,
) -> dict[str, str]:
    return {
        "panel": panel,
        "series": series,
        "parameter": str(parameter),
        "x": format(x, ".17g"),
        "y": format(y, ".17g"),
        "quantity_class": quantity_class,
        "source_origin": (
            "r073t-analytic-proof"
            if panel == "A"
            else "r073t-exact-certificate-results"
        ),
        "source_record_type": source_record_type,
        "formula": formula,
        "normalization": normalization,
    }


def generate_rows(config: dict[str, Any]) -> list[dict[str, str]]:
    rows = [
        row("A", "exact_quartic_balance", 1, 1, 1, "exact-identity",
            "analytic-chain", "Q'+4nuY+2nuX^2=4<p,u.grad w>", "normalized Haar"),
        row("A", "pressure_absorption", 2, 2, 1, "classical-upper-bound",
            "analytic-chain", "4|<p,u.grad w>|<=nuX^2+4CR^2/nu*||u||_6^6",
            "periodic Riesz L3"),
        row("A", "static_autocorrelation", 3, 3, 1, "rigorous-upper-bound",
            "analytic-chain", "||u||_6^6<=A*Q", "R0.73S"),
        row("A", "dynamic_AQ", 4, 4, 1, "rigorous-upper-bound",
            "analytic-chain", "Q'+4nuY+nuX^2<=4CR^2/nu*A*Q", "normalized Haar"),
    ]
    for carrier in range(int(config["carrierMinimum"]), int(config["carrierMaximum"]) + 1):
        rows.append(row(
            "B", "carrier_dissipation", carrier, carrier, carrier * carrier,
            "exact", "rotating-shear", "abs(Cdot_0(0))/(2nu)=N^2",
            "C(h,0)=delta_0 for every N",
        ))
    for dilation in range(int(config["dilationMinimum"]), int(config["dilationMaximum"]) + 1):
        rows.extend((
            row("C", "u_L", dilation, dilation, -384 * dilation, "exact",
                "six-mode-sign-pair", "Qdot(0)+16536nuL^2=-384L",
                "common initial viscous term removed"),
            row("C", "minus_u_L", dilation, dilation, 384 * dilation, "exact",
                "six-mode-sign-pair", "Qdot(0)+16536nuL^2=+384L",
                "common initial viscous term removed"),
        ))
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def render(output: Path, config: dict[str, Any], rows: list[dict[str, str]]) -> None:
    import matplotlib as mpl  # type: ignore
    mpl.use("Agg")
    import matplotlib.pyplot as plt  # type: ignore
    from matplotlib.patches import Circle, FancyBboxPatch  # type: ignore

    palette = config["palette"]
    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.0,
        "axes.titlesize": 8.4,
        "axes.labelsize": 7.2,
        "axes.edgecolor": palette["ink"],
        "axes.linewidth": 0.7,
        "xtick.labelsize": 6.7,
        "ytick.labelsize": 6.7,
        "text.color": palette["ink"],
        "axes.labelcolor": palette["ink"],
        "xtick.color": palette["ink"],
        "ytick.color": palette["ink"],
        "svg.hashsalt": "r073t-dynamic-autocorrelation",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
    figure = plt.figure(figsize=(width, height), facecolor=palette["paper"])
    grid = figure.add_gridspec(
        1, 3, left=0.052, right=0.985, bottom=0.22, top=0.79,
        wspace=0.34, width_ratios=(1.42, 0.96, 1.08),
    )
    ax_a = figure.add_subplot(grid[0, 0])
    ax_b = figure.add_subplot(grid[0, 1])
    ax_c = figure.add_subplot(grid[0, 2])

    figure.text(0.052, 0.94, "Dynamic autocorrelation: one upper estimate, two missing variables",
                fontsize=11.2, fontweight="bold", ha="left", va="top")
    figure.text(0.055, 0.885,
                "Normalized periodic torus · exact identities and Fraction witnesses · no PDE simulation",
                fontsize=7.1, color=palette["midGrey"], ha="left", va="top")
    for x, y, radius, color in (
        (0.948, 0.934, 0.010, palette["blueLight"]),
        (0.965, 0.934, 0.008, palette["goldLight"]),
        (0.9565, 0.951, 0.007, palette["blue"]),
    ):
        figure.add_artist(Circle((x, y), radius, transform=figure.transFigure,
                                 facecolor=color, edgecolor="none", alpha=0.9))

    # Panel A: an equation flow, not a numerical chart.
    ax_a.set_axis_off()
    ax_a.set_title("A  One-sided AQ budget", loc="left", fontweight="bold",
                   y=1.075, pad=0)
    ax_a.text(0.0, 1.01, "exact balance → classical pressure bound → R0.73S",
              transform=ax_a.transAxes, fontsize=6.5, color=palette["midGrey"], va="bottom")
    boxes = [
        (0.08, 0.73, 0.84, 0.16, palette["paper"], palette["lightGrey"],
         r"$Q'+4\nu Y+2\nu X^2=4\int p\,u\!\cdot\!\nabla w$", "exact quartic balance"),
        (0.08, 0.49, 0.84, 0.16, palette["paper"], palette["lightGrey"],
         r"$4|\int p\,u\!\cdot\!\nabla w|\leq\nu X^2+\frac{4C_R^2}{\nu}\|u\|_6^6$",
         "Riesz + Hölder + Young"),
        (0.22, 0.27, 0.56, 0.12, palette["goldLight"], palette["gold"],
         r"$\|u\|_6^6\leq A\,Q$", "R0.73S static bound"),
        (0.05, 0.02, 0.90, 0.16, palette["blueLight"], palette["blueDark"],
         r"$Q'+4\nu Y+\nu X^2\leq\frac{4C_R^2}{\nu}\,A\,Q$",
         "valid one-sided dynamic estimate"),
    ]
    for x, y, w, h, fill, edge, equation, label in boxes:
        box = FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.018",
            transform=ax_a.transAxes, linewidth=0.9, facecolor=fill,
            edgecolor=edge, clip_on=False,
        )
        ax_a.add_patch(box)
        ax_a.text(x + w / 2, y + h * 0.61, equation, transform=ax_a.transAxes,
                  ha="center", va="center", fontsize=6.8,
                  fontweight="bold" if y < 0.2 else "normal")
        ax_a.text(x + w / 2, y + h * 0.18, label, transform=ax_a.transAxes,
                  ha="center", va="center", fontsize=5.7, color=palette["midGrey"])
    for y0, y1 in ((0.73, 0.65), (0.49, 0.39), (0.27, 0.18)):
        ax_a.annotate("", xy=(0.5, y1), xytext=(0.5, y0), xycoords=ax_a.transAxes,
                      arrowprops={"arrowstyle": "-|>", "color": palette["midGrey"],
                                  "linewidth": 0.8})

    # Panel B: exact carrier-scale loss.
    b_rows = [item for item in rows if item["panel"] == "B"]
    bx = [float(item["x"]) for item in b_rows]
    by = [float(item["y"]) for item in b_rows]
    ax_b.set_title("B  Carrier-scale loss", loc="left", fontweight="bold",
                   y=1.075, pad=0)
    ax_b.text(0.0, 1.01, r"at $t=0$: same $C(h,0)=\delta_{h0}$ for all $N$",
              transform=ax_b.transAxes, fontsize=6.5, color=palette["midGrey"], va="bottom")
    ax_b.plot(bx, by, color=palette["blue"], linewidth=1.6, marker="o",
              markersize=3.7, markerfacecolor=palette["paper"],
              markeredgewidth=1.0, markeredgecolor=palette["blueDark"])
    ax_b.set_xlabel(r"carrier $N$")
    ax_b.set_ylabel(r"$|\dot C_0(0)|/(2\nu)$")
    ax_b.set_xticks(range(1, 9))
    ax_b.set_ylim(0, 70)
    ax_b.grid(axis="y", color=palette["lightGrey"], linewidth=0.55)
    ax_b.spines[["top", "right"]].set_visible(False)
    ax_b.annotate(r"$N^2$", xy=(8, 64), xytext=(6.45, 57),
                  fontsize=7.1, fontweight="bold", color=palette["blueDark"],
                  arrowprops={"arrowstyle": "-", "color": palette["blueDark"],
                              "linewidth": 0.8})

    # Panel C: exact pressure-polarization separation after centering viscosity.
    c_positive = [item for item in rows if item["panel"] == "C" and item["series"] == "minus_u_L"]
    c_negative = [item for item in rows if item["panel"] == "C" and item["series"] == "u_L"]
    cx = [float(item["x"]) for item in c_positive]
    cy_pos = [float(item["y"]) for item in c_positive]
    cy_neg = [float(item["y"]) for item in c_negative]
    ax_c.set_title("C  Signed pairing phase", loc="left", fontweight="bold",
                   fontsize=7.8, y=1.075, pad=0)
    ax_c.text(0.0, 1.01, r"same $C$ at $t=0$; viscous term removed",
              transform=ax_c.transAxes, fontsize=5.7, color=palette["midGrey"], va="bottom")
    ax_c.axhline(0, color=palette["midGrey"], linewidth=0.75)
    ax_c.plot(cx, cy_pos, color=palette["gold"], linewidth=1.6, marker="s",
              markersize=3.5, markerfacecolor=palette["goldLight"],
              markeredgecolor=palette["gold"], label=r"$-u_L$: $+384L$")
    ax_c.plot(cx, cy_neg, color=palette["blueDark"], linewidth=1.5, linestyle="--",
              marker="o", markersize=3.6, markerfacecolor=palette["paper"],
              markeredgecolor=palette["blueDark"], label=r"$u_L$: $-384L$")
    ax_c.set_xlabel(r"dilation $L$")
    ax_c.set_ylabel(r"$Q'(0)+16536\nu L^2$")
    ax_c.set_xticks(range(1, 9))
    ax_c.set_ylim(-3450, 3450)
    ax_c.grid(axis="y", color=palette["lightGrey"], linewidth=0.55)
    ax_c.spines[["top", "right"]].set_visible(False)
    ax_c.legend(loc="upper left", frameon=False, fontsize=6.4, handlelength=2.4)

    figure.text(0.052, 0.085,
                r"Boundary: $\int A\,dt$ is critical and $A\geq\|u\|_\infty^2$; exact scalar $C$ is not autonomous.",
                fontsize=7.0, fontweight="bold", ha="left", va="bottom")
    figure.text(0.052, 0.037,
                "Exact analytic / rational finite evidence only · smooth witnesses · not a simulation · NOT CLAY",
                fontsize=6.3, color=palette["midGrey"], ha="left", va="bottom")

    metadata = {
        "Title": "R0.73T | Dynamic autocorrelation and the pressure-tensor barrier",
        "Author": "ChuiKuan Zeng",
        "Subject": "Exact Navier-Stokes autocorrelation identities and finite witnesses",
        "Keywords": "Navier-Stokes, autocorrelation, pressure, Fourier, exact certificate",
    }
    svg_path = output / "figure.svg"
    figure.savefig(svg_path, format="svg", facecolor=palette["paper"],
                   metadata={"Title": metadata["Title"], "Description": metadata["Subject"]})
    # Matplotlib emits spaces at the ends of multiline path-data rows.  Strip
    # them deterministically so the generated SVG passes Git's whitespace gate
    # and has a stable text representation without changing its geometry.
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    figure.savefig(output / "figure.pdf", format="pdf", facecolor=palette["paper"],
                   metadata=metadata)
    figure.savefig(output / "figure.png", format="png", facecolor=palette["paper"],
                   dpi=int(config["pngDpi"]), metadata={"Title": metadata["Title"]})
    plt.close(figure)

    from PIL import Image  # type: ignore
    with Image.open(output / "figure.png") as image:
        reduced = image.copy()
        reduced.thumbnail((1800, 1200))
        reduced.convert("RGB").save(output / "qa-final-size.png")
        reduced.convert("L").save(output / "qa-grayscale.png")

    import pypdfium2 as pdfium  # type: ignore
    document = pdfium.PdfDocument(str(output / "figure.pdf"))
    if len(document) != 1:
        raise RuntimeError("figure PDF is not one page")
    page = document[0]
    bitmap = page.render(scale=2.5)
    bitmap.to_pil().convert("RGB").save(output / "qa-pdf.png")
    page.close()
    document.close()


def main() -> None:
    args = parse_args()
    output = Path(args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    monitor = Monitor(output)
    monitor.event("start", mode="data-only" if args.data_only else "render-preseal")
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    results = verify_certificate()
    monitor.event("certificate-verified", checks=results["audit"]["required"])
    rows = generate_rows(config)
    if len(rows) != 28:
        raise RuntimeError("source-data row count drift")
    write_csv(output / "source-data.csv", rows)
    monitor.event("source-data-written", rows=len(rows))
    if not args.data_only:
        render(output, config, rows)
        monitor.event("render-complete", outputs=6)
    environment = {
        "schemaVersion": "r073t-dynamic-autocorrelation-environment-v1",
        "createdUtc": utc_now(),
        "execution": {
            "dgxUsed": False,
            "gpu": "not used",
            "host": platform.node(),
            "network": "not used",
            "processes": 1,
            "python": platform.python_version(),
            "threadsPerProcess": 1,
        },
        "packages": {name: installed_version(name) for name in
                     ("matplotlib", "numpy", "pillow", "pypdf", "pypdfium2")},
    }
    (output / "environment.json").write_text(canonical(environment), encoding="utf-8")
    result_summary = {
        "schemaVersion": "r073t-dynamic-autocorrelation-figure-results-v1",
        "allSourceChecksPass": True,
        "certificateChecks": results["audit"]["required"],
        "claimBoundary": contract["claimBoundary"],
        "figureId": FIGURE_ID,
        "rowCount": len(rows),
        "series": {
            "analyticChain": 4,
            "carrier": 8,
            "pressurePair": 16,
        },
    }
    (output / "results.json").write_text(canonical(result_summary), encoding="utf-8")
    monitor.event("complete", rows=len(rows))
    print(canonical({
        "figureId": FIGURE_ID,
        "mode": "data-only" if args.data_only else "render-preseal",
        "rows": len(rows),
        "status": "PASS",
    }), end="")


if __name__ == "__main__":
    main()
