#!/usr/bin/env python3
"""Generate the R0.73U tensor heat-hierarchy formal figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version as package_version
import json
import math
from pathlib import Path
import platform
import resource
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
FIGURE_ID = "fig-r073u-tensor-heat-hierarchy"
CSV_FIELDS = (
    "panel", "series", "record", "component_i", "component_j", "parameter",
    "x", "y", "exact_value", "quantity_class", "source_origin", "formula",
    "normalization",
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
                "dgxUsed": False,
                "elapsedSeconds": elapsed,
                "executionHost": platform.node(),
                "gpu": "not used",
                "maximumResidentSetMiB": rss_mib(),
                "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
                "processes": 1,
                "stage": stage,
                "threadsPerProcess": 1,
                "timestampUtc": stamp,
            }, sort_keys=True) + "\n")


def row(
    panel: str, series: str, record: str, component_i: str, component_j: str,
    parameter: str, x: float | None, y: float | None, exact_value: str,
    quantity_class: str, source_origin: str, formula: str, normalization: str,
) -> dict[str, str]:
    return {
        "panel": panel,
        "series": series,
        "record": record,
        "component_i": component_i,
        "component_j": component_j,
        "parameter": parameter,
        "x": "" if x is None else format(x, ".17g"),
        "y": "" if y is None else format(y, ".17g"),
        "exact_value": exact_value,
        "quantity_class": quantity_class,
        "source_origin": source_origin,
        "formula": formula,
        "normalization": normalization,
    }


def generate_rows(config: dict[str, Any]) -> list[dict[str, str]]:
    rows = [
        row("A", "tensor_state", "local-product", "", "", "s>=0", None, None,
            "Theta_s=P_s(u tensor u)", "exact-identity", "r073u-analytic-proof",
            "Theta_s=P_s T", "normalized periodic heat semigroup"),
        row("A", "pressure_reconstruction", "same-scale-pressure", "i", "j", "s>=0",
            None, None, "p_s=R_i R_j Theta_s,ij", "exact-identity",
            "r073u-analytic-proof", "p_s=R_i R_j Theta_s,ij", "mean-zero pressure"),
        row("A", "cubic_tangent", "odd-cubic-transport", "i", "j", "s>=0",
            None, None, "-P_s partial_k(u_k u_i u_j)", "exact-identity",
            "r073u-analytic-proof", "odd under u->-u", "physical-time tangent"),
        row("A", "pressure_velocity_tangent", "odd-pressure-velocity", "i", "j", "s>=0",
            None, None, "-P_s(u_j partial_i p+u_i partial_j p)", "exact-identity",
            "r073u-analytic-proof", "odd under u->-u", "physical-time tangent"),
    ]
    matrices = {
        "cubic_A": ((-2, 3), (3, -4)),
        "pressure_velocity_B": ((0, -2), (-2, 4)),
        "total_K": ((-2, 1), (1, 0)),
        "local_tensor_T": ((0, 0), (0, 0)),
        "viscous_V": ((0, 0), (0, 0)),
    }
    formulas = {
        "cubic_A": "A=-i h_k Fourier(u_k u_i u_j)",
        "pressure_velocity_B": "B=-Fourier(u_j partial_i p+u_i partial_j p)",
        "total_K": "K=A+B",
        "local_tensor_T": "Fourier(u_i u_j)(h*)=0",
        "viscous_V": "V=Delta T-2 sum_l partial_l u tensor partial_l u",
    }
    for series, matrix in matrices.items():
        for i in range(2):
            for j in range(2):
                value = matrix[i][j]
                rows.append(row(
                    "B", series, f"{series}-{i + 1}{j + 1}", str(i + 1), str(j + 1),
                    "t=0; h*=(1,2,0)", float(i + 1), float(value), str(value),
                    "exact-finite-fourier", "r073u-four-site-diagnostic", formulas[series],
                    "2x2 active block; normalized Fourier coefficient",
                ))
    rows.extend((
        row("B", "tangent_separation", "matrix-coefficient", "i", "j", "t=0; s>=0",
            None, None, "2*exp(-5s)*K", "exact-finite-fourier",
            "r073u-four-site-diagnostic",
            "partial_t Theta_s(0;u)-partial_t Theta_s(0;-u)=2 exp(-5s) K",
            "same initial time t=0; h*=(1,2,0); not trajectory symmetry"),
        row("B", "tangent_separation_norm", "frobenius", "", "", "t=0; s>=0",
            None, None, "2*sqrt(6)*exp(-5s)", "exact-finite-fourier",
            "r073u-four-site-diagnostic", "norm_F(2 exp(-5s) K)",
            "same initial time t=0; coefficient-level Frobenius norm"),
    ))
    z_min = float(config["curveMinimum"])
    z_max = float(config["curveMaximum"])
    step = float(config["curveStep"])
    count = int(round((z_max - z_min) / step))
    for index in range(count + 1):
        z = z_min + index * step
        value = z * math.exp(-5.0 * z * z)
        rows.append(row(
            "C", "universal_curve", f"analytic-sample-{index:03d}", "", "",
            f"z={format(z, '.2f')}", z, value, "z*exp(-5*z^2)",
            "analytic-function-sample", "r073u-analytic-proof",
            "f(z)=z exp(-5 z^2)", "sqrt(s)*D_L(s)/(2*sqrt(6))",
        ))
    peak_x = 1.0 / math.sqrt(10.0)
    peak_y = math.exp(-0.5) / math.sqrt(10.0)
    rows.append(row(
        "C", "exact_peak", "unique-positive-maximum", "", "", "z*=1/sqrt(10)",
        peak_x, peak_y, "exp(-1/2)/sqrt(10)", "exact-analytic-value",
        "r073u-analytic-proof", "f'(z)=exp(-5z^2)(1-10z^2)",
        "f(z)=z exp(-5z^2)",
    ))
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add_box(ax: Any, x: float, y: float, w: float, h: float, face: str, edge: str,
            title: str, body: str, title_color: str, body_size: float = 6.4) -> None:
    from matplotlib.patches import FancyBboxPatch  # type: ignore
    patch = FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.018",
        transform=ax.transAxes, linewidth=0.9, facecolor=face, edgecolor=edge,
        clip_on=False,
    )
    ax.add_patch(patch)
    ax.text(x + 0.035 * w, y + 0.73 * h, title, transform=ax.transAxes,
            ha="left", va="center", fontsize=5.7, fontweight="bold",
            color=title_color)
    ax.text(x + 0.5 * w, y + 0.38 * h, body, transform=ax.transAxes,
            ha="center", va="center", fontsize=body_size, color=title_color)


def render(output: Path, config: dict[str, Any], rows: list[dict[str, str]]) -> None:
    import matplotlib as mpl  # type: ignore
    mpl.use("Agg")
    import matplotlib.pyplot as plt  # type: ignore
    from matplotlib.patches import Circle  # type: ignore

    palette = config["palette"]
    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.0,
        "axes.titlesize": 8.2,
        "axes.labelsize": 7.0,
        "axes.edgecolor": palette["ink"],
        "axes.linewidth": 0.7,
        "xtick.labelsize": 6.5,
        "ytick.labelsize": 6.5,
        "text.color": palette["ink"],
        "axes.labelcolor": palette["ink"],
        "xtick.color": palette["ink"],
        "ytick.color": palette["ink"],
        "svg.hashsalt": "r073u-tensor-heat-hierarchy",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
    figure = plt.figure(figsize=(width, height), facecolor=palette["paper"])
    grid = figure.add_gridspec(
        1, 3, left=0.045, right=0.985, bottom=0.225, top=0.79,
        wspace=0.26, width_ratios=(1.13, 1.35, 1.12),
    )
    ax_a = figure.add_subplot(grid[0, 0])
    ax_b = figure.add_subplot(grid[0, 1])
    ax_c = figure.add_subplot(grid[0, 2])

    figure.text(0.045, 0.94,
                "Tensor heat hierarchy: pressure recovered, signed tangent still missing",
                fontsize=10.8, fontweight="bold", ha="left", va="top")
    figure.text(0.048, 0.885,
                "Normalized periodic torus | exact identities and a four-site Fourier diagnostic | no PDE simulation",
                fontsize=6.8, color=palette["midGrey"], ha="left", va="top")
    for x, y, radius, color in (
        (0.948, 0.934, 0.010, palette["blueLight"]),
        (0.965, 0.934, 0.008, palette["goldLight"]),
        (0.9565, 0.951, 0.007, palette["blue"]),
    ):
        figure.add_artist(Circle((x, y), radius, transform=figure.transFigure,
                                 facecolor=color, edgecolor="none", alpha=0.9))

    # Panel A: exact map and parity obstruction.
    ax_a.set_axis_off()
    ax_a.set_title("A  Exact map / parity barrier", loc="left", fontweight="bold",
                   y=1.075, pad=0)
    ax_a.text(0.0, 1.01, "local-product tensor, not KHM covariance",
              transform=ax_a.transAxes, fontsize=5.9, color=palette["midGrey"], va="bottom")
    add_box(ax_a, 0.04, 0.72, 0.92, 0.18, palette["paper"], palette["lightGrey"],
            "EVEN QUADRATIC STATE", r"$T=u\otimes u,\quad \Theta_s=P_sT$",
            palette["ink"], 7.0)
    add_box(ax_a, 0.12, 0.43, 0.76, 0.17, palette["blueLight"], palette["blueDark"],
            "EXACT SAME-SCALE RECOVERY", r"$p_s=R_iR_j\Theta_{s,ij}$",
            palette["blueDark"], 7.2)
    ax_a.annotate("", xy=(0.5, 0.61), xytext=(0.5, 0.72), xycoords=ax_a.transAxes,
                  arrowprops={"arrowstyle": "-|>", "color": palette["blueDark"],
                              "linewidth": 1.1})
    ax_a.text(0.55, 0.66, r"$T\ \to\ p$", transform=ax_a.transAxes,
              fontsize=6.4, fontweight="bold", color=palette["blueDark"], va="center")
    add_box(ax_a, 0.04, 0.04, 0.92, 0.23, palette["goldLight"], palette["gold"],
            "SIGNED ODD TANGENT", r"$-P_s\nabla\!\cdot(u^{\otimes3})$" + "\n" +
            r"$-P_s(u\otimes\nabla p+\nabla p\otimes u)$",
            palette["ink"], 6.2)
    ax_a.annotate("", xy=(0.5, 0.28), xytext=(0.5, 0.43), xycoords=ax_a.transAxes,
                  arrowprops={"arrowstyle": "-[", "color": palette["gold"],
                              "linewidth": 1.2, "linestyle": "--",
                              "mutation_scale": 11})
    ax_a.text(0.55, 0.355, r"$T\ \not\to$ signed tangent",
              transform=ax_a.transAxes, fontsize=6.0, fontweight="bold",
              color=palette["gold"], va="center")
    ax_a.text(0.5, -0.01, r"$\Theta_s(-u)=\Theta_s(u)$, but odd terms change sign",
              transform=ax_a.transAxes, fontsize=5.8, color=palette["midGrey"],
              ha="center", va="top")

    # Panel B: exact finite matrices and parity separation.
    ax_b.set_axis_off()
    ax_b.set_title(r"B  Exact witness at $h_*=(1,2,0)$", loc="left",
                   fontweight="bold", y=1.075, pad=0)
    ax_b.text(0.0, 1.01, "initial time t=0 | four Fourier sites | exact integers",
              transform=ax_b.transAxes, fontsize=5.9, color=palette["midGrey"], va="bottom")
    ax_b.text(0.5, 0.895,
              r"$u=(2\sin(x+y),\ 2\sin x-2\sin(x+y),\ 0)$",
              transform=ax_b.transAxes, fontsize=6.1, ha="center", va="center")
    matrix_specs = [
        (0.01, "CUBIC  A", "[-2   3]\n[ 3  -4]", palette["paper"], palette["blue"]),
        (0.35, "PRESSURE  B", "[ 0  -2]\n[-2   4]", palette["paper"], palette["gold"]),
        (0.69, "TOTAL  K", "[-2   1]\n[ 1   0]", palette["blueLight"], palette["blueDark"]),
    ]
    for x, label, matrix, face, edge in matrix_specs:
        add_box(ax_b, x, 0.53, 0.30, 0.27, face, edge, label, matrix,
                palette["ink"], 7.2)
    ax_b.text(0.325, 0.665, "+", transform=ax_b.transAxes, fontsize=11.0,
              fontweight="bold", ha="center", va="center")
    ax_b.text(0.665, 0.665, "=", transform=ax_b.transAxes, fontsize=10.0,
              fontweight="bold", ha="center", va="center")
    ax_b.text(0.5, 0.475,
              r"$V:=\Delta T-2\sum_\ell\partial_\ell u\otimes\partial_\ell u$",
              transform=ax_b.transAxes, fontsize=5.8, ha="center", va="center")
    ax_b.text(0.5, 0.415,
              r"$\widehat T(h_*)=\widehat V(h_*)=0,\qquad \|K\|_F=\sqrt{6}$",
              transform=ax_b.transAxes, fontsize=6.0, ha="center", va="center")
    add_box(ax_b, 0.04, 0.11, 0.40, 0.20, palette["paper"], palette["blueDark"],
            "STATE u, t=0", r"$\partial_t\widehat\Theta_s=+e^{-5s}K$",
            palette["blueDark"], 6.1)
    add_box(ax_b, 0.56, 0.11, 0.40, 0.20, palette["paper"], palette["gold"],
            "STATE -u, t=0", r"$\partial_t\widehat\Theta_s=-e^{-5s}K$",
            palette["ink"], 6.1)
    ax_b.text(0.5, 0.21, "vs", transform=ax_b.transAxes, fontsize=5.8,
              fontweight="bold", color=palette["midGrey"], ha="center", va="center")
    ax_b.text(0.5, 0.03, r"at $t=0$: separation $=2e^{-5s}K$; norm $=2\sqrt{6}e^{-5s}$",
              transform=ax_b.transAxes, fontsize=6.0, fontweight="bold",
              ha="center", va="center")

    # Panel C: universal analytic profile.
    curve = [item for item in rows if item["panel"] == "C" and item["series"] == "universal_curve"]
    x_values = [float(item["x"]) for item in curve]
    y_values = [float(item["y"]) for item in curve]
    peak = next(item for item in rows if item["panel"] == "C" and item["series"] == "exact_peak")
    peak_x = float(peak["x"])
    peak_y = float(peak["y"])
    ax_c.set_title("C  Universal heat profile", loc="left", fontweight="bold",
                   y=1.075, pad=0)
    ax_c.text(0.0, 1.01, r"exact $f(z)=ze^{-5z^2}$, $z=\sqrt{s}L$",
              transform=ax_c.transAxes, fontsize=5.9, color=palette["midGrey"], va="bottom")
    ax_c.plot(x_values, y_values, color=palette["blue"], linewidth=1.7)
    ax_c.fill_between(x_values, y_values, 0, color=palette["blueLight"], alpha=0.22)
    ax_c.axvline(peak_x, color=palette["gold"], linewidth=0.85, linestyle="--")
    ax_c.axhline(peak_y, color=palette["lightGrey"], linewidth=0.65, linestyle=":")
    ax_c.plot([peak_x], [peak_y], color=palette["gold"], linestyle="None",
              marker="o", markersize=4.8,
              markerfacecolor=palette["goldLight"], markeredgecolor=palette["gold"],
              markeredgewidth=1.0)
    ax_c.annotate(r"$z_*=1/\sqrt{10}$" + "\n" + r"$f_*=e^{-1/2}/\sqrt{10}$",
                  xy=(peak_x, peak_y), xytext=(0.54, 0.89), textcoords=ax_c.transAxes,
                  fontsize=6.0, ha="left", va="top", color=palette["ink"],
                  arrowprops={"arrowstyle": "-", "color": palette["gold"],
                              "linewidth": 0.8})
    ax_c.set_xlim(0, float(config["curveMaximum"]))
    ax_c.set_ylim(0, 0.215)
    ax_c.set_xlabel(r"$z=\sqrt{s}\,L$")
    ax_c.set_ylabel(r"$\sqrt{s}\,D_L(s)/(2\sqrt{6})$")
    ax_c.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])
    ax_c.set_yticks([0.00, 0.05, 0.10, 0.15, 0.20])
    ax_c.grid(axis="y", color=palette["lightGrey"], linewidth=0.55)
    ax_c.spines[["top", "right"]].set_visible(False)
    ax_c.text(0.98, 0.08,
              r"$D_L(s)=2\sqrt{6}L e^{-5sL^2}$" + "\n" +
              r"$=2\sqrt{6}s^{-1/2}f(\sqrt{s}L)$",
              transform=ax_c.transAxes, fontsize=5.9, ha="right", va="bottom",
              bbox={"boxstyle": "round,pad=0.25", "facecolor": palette["paper"],
                    "edgecolor": palette["lightGrey"], "linewidth": 0.7})

    figure.text(0.045, 0.092,
                r"Parabolic boundary: $s=\theta L^{-2}$ gives $D_L(s)=2\sqrt{6\theta}e^{-5\theta}s^{-1/2}$ - coefficient-level one-derivative cost at a fixed slice.",
                fontsize=6.8, fontweight="bold", ha="left", va="bottom")
    figure.text(0.045, 0.039,
                "Exact analytic / finite Fourier diagnostic | coefficient-level | not a simulation or fitted law | NOT CLAY",
                fontsize=6.1, color=palette["midGrey"], ha="left", va="bottom")

    metadata = {
        "Title": "R0.73U | Tensor heat hierarchy and the signed-flux boundary",
        "Author": "ChuiKuan Zeng",
        "Subject": "Exact tensor heat identities, finite Fourier parity witness, and analytic heat-scale profile",
        "Keywords": "Navier-Stokes, heat filter, stress tensor, pressure, Fourier, exact diagnostic",
        "CreationDate": datetime(2026, 9, 1, tzinfo=timezone.utc),
        "ModDate": datetime(2026, 9, 1, tzinfo=timezone.utc),
    }
    svg_path = output / "figure.svg"
    figure.savefig(svg_path, format="svg", facecolor=palette["paper"],
                   metadata={"Title": metadata["Title"], "Description": metadata["Subject"]})
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text("\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
                        encoding="utf-8")
    figure.savefig(output / "figure.pdf", format="pdf", facecolor=palette["paper"],
                   metadata=metadata)
    figure.savefig(output / "figure.png", format="png", facecolor=palette["paper"],
                   dpi=int(config["pngDpi"]),
                   metadata={"Title": metadata["Title"], "Description": metadata["Subject"]})
    plt.close(figure)

    from PIL import Image  # type: ignore
    with Image.open(output / "figure.png") as image:
        reduced = image.copy()
        reduced.thumbnail((int(config["qaMaximumWidthPixels"]), 1200))
        reduced.convert("RGB").save(output / "qa-final-size.png")
        reduced.convert("L").save(output / "qa-grayscale.png")

    import pypdfium2 as pdfium  # type: ignore
    document = pdfium.PdfDocument(str(output / "figure.pdf"))
    if len(document) != 1:
        raise RuntimeError("figure PDF is not one page")
    page = document[0]
    page.render(scale=2.5).to_pil().convert("RGB").save(output / "qa-pdf.png")
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
    rows = generate_rows(config)
    if len(rows) != 138:
        raise RuntimeError("source-data row count drift")
    write_csv(output / "source-data.csv", rows)
    monitor.event("source-data-written", rows=len(rows))
    if not args.data_only:
        render(output, config, rows)
        monitor.event("render-complete", outputs=6)
    environment = {
        "schemaVersion": "r073u-tensor-heat-hierarchy-environment-v1",
        "createdUtc": utc_now(),
        "execution": {
            "dgxUsed": False,
            "gpu": "not used",
            "host": platform.node(),
            "logicalCpuCount": None if not hasattr(__import__("os"), "cpu_count") else __import__("os").cpu_count(),
            "machine": platform.machine(),
            "network": "not used",
            "operatingSystem": platform.platform(),
            "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
            "processes": 1,
            "python": platform.python_version(),
            "threadsPerProcess": 1,
        },
        "packages": {name: installed_version(name) for name in
                     ("matplotlib", "numpy", "pillow", "pypdf", "pypdfium2")},
    }
    (output / "environment.json").write_text(canonical(environment), encoding="utf-8")
    result_summary = {
        "schemaVersion": "r073u-tensor-heat-hierarchy-figure-results-v1",
        "allSourceChecksPass": True,
        "claimBoundary": contract["claimBoundary"],
        "evaluation": {
            "time": "t=0",
            "comparison": "same initial time",
            "trajectorySymmetryClaim": False,
        },
        "exactConstants": {
            "cubicMatrixA": [[-2, 3], [3, -4]],
            "pressureVelocityMatrixB": [[0, -2], [-2, 4]],
            "totalMatrix": [[-2, 1], [1, 0]],
            "totalMatrixFrobeniusSquared": 6,
            "heatExponentAtWitness": 5,
            "viscousTensorDefinition": "V=Delta T-2 sum_l partial_l u tensor partial_l u",
            "peakZExact": "1/sqrt(10)",
            "peakValueExact": "exp(-1/2)/sqrt(10)",
        },
        "figureId": FIGURE_ID,
        "rowCount": len(rows),
        "series": {
            "analyticSchematic": 4,
            "exactFiniteDiagnostic": 22,
            "analyticCurveSamples": 111,
            "exactPeak": 1,
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
