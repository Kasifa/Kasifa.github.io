#!/usr/bin/env python3
"""Generate the R0.73W signed-production four-panel journal figure."""

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
import socket
import subprocess
import sys
import time
from typing import Any, Iterable


def bootstrap() -> None:
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()

import matplotlib  # type: ignore  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # type: ignore  # noqa: E402
from matplotlib.patches import Circle, Ellipse  # type: ignore  # noqa: E402
from matplotlib.text import Text  # type: ignore  # noqa: E402
import numpy as np  # type: ignore  # noqa: E402
from PIL import Image, ImageOps  # type: ignore  # noqa: E402
import pypdfium2 as pdfium  # type: ignore  # noqa: E402


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FIGURE_ID = "fig-r073w-signed-production"
CSV_FIELDS = [
    "panel", "series", "record", "x", "y", "x_name", "y_name", "formula",
    "evidence_class", "source_primary_path", "source_independent_path",
    "normalization", "note",
]
EXPECTED_PACKAGES = {
    "matplotlib": "3.10.6",
    "numpy": "2.5.2",
    "pillow": "12.3.0",
    "pypdf": "6.10.0",
    "pypdfium2": "5.13.0",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--render-preseal", action="store_true")
    parser.add_argument("--data-only", action="store_true")
    args = parser.parse_args()
    if not args.render_preseal and not args.data_only:
        parser.error("choose --render-preseal or --data-only")
    if args.render_preseal and args.data_only:
        parser.error("render modes are mutually exclusive")
    return args


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def canonical_compact(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=False) + "\n").encode("utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root is not an object: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def number(value: float) -> str:
    value = float(value)
    if value == 0.0:
        return "0"
    return format(value, ".17g")


def package_versions() -> dict[str, str]:
    output: dict[str, str] = {}
    for name in EXPECTED_PACKAGES:
        try:
            output[name] = package_version(name)
        except PackageNotFoundError:
            output[name] = "missing"
    return output


def memory_gib() -> float:
    try:
        result = subprocess.run(
            ["sysctl", "-n", "hw.memsize"], capture_output=True, text=True,
            check=False,
        )
        if result.returncode == 0:
            return round(int(result.stdout.strip()) / (1024 ** 3), 3)
    except (OSError, ValueError):
        pass
    return 0.001


class Monitor:
    def __init__(self) -> None:
        self.started = time.perf_counter()
        self.events: list[dict[str, object]] = []

    def event(self, name: str, **details: object) -> None:
        row: dict[str, object] = {
            "elapsedSeconds": round(time.perf_counter() - self.started, 6),
            "event": name,
            "timestampUtc": utc_now(),
        }
        row.update(details)
        self.events.append(row)

    def write(self) -> None:
        with (HERE / "progress.ndjson").open("w", encoding="utf-8") as stream:
            for row in self.events:
                stream.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
        usage = resource.getrusage(resource.RUSAGE_SELF)
        resource_row = {
            "elapsedSeconds": round(time.perf_counter() - self.started, 6),
            "logicalCpuCount": os.cpu_count() or 1,
            "maximumResidentSetSizeRaw": usage.ru_maxrss,
            "processes": 1,
            "threadsPerProcess": 1,
            "timestampUtc": utc_now(),
        }
        (HERE / "resource-log.ndjson").write_text(
            json.dumps(resource_row, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


def verify_inputs(
    contract: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    for entry in contract["analyticSources"]:
        path = ROOT / entry["path"]
        require(path.is_file(), "missing analytic source: " + entry["path"])
        require(sha256(path) == entry["sha256"],
                "analytic source hash drift: " + entry["path"])

    certificate = contract["certificate"]
    primary_path = ROOT / certificate["primaryPath"]
    independent_path = ROOT / certificate["independentPath"]
    require(sha256(primary_path) == certificate["primarySha256"],
            "primary certificate hash drift")
    require(sha256(independent_path) == certificate["independentSha256"],
            "independent certificate hash drift")
    primary = load_json(primary_path)
    independent = load_json(independent_path)
    require(primary["commonCore"] == independent["commonCore"],
            "two certificate commonCore objects differ")
    common = primary["commonCore"]
    common_digest = hashlib.sha256(canonical(common).encode("utf-8")).hexdigest()
    require(common_digest == certificate["commonCoreSha256"],
            "commonCore digest drift")
    compact_digest = hashlib.sha256(canonical_compact(common)).hexdigest()
    require(compact_digest == certificate["commonCoreCompactSha256"],
            "compact commonCore digest drift")

    manifest_path = ROOT / certificate["manifestPath"]
    require(sha256(manifest_path) == certificate["manifestSha256"],
            "certificate manifest hash drift")
    manifest = load_json(manifest_path)
    require(manifest.get("status") == "SEALED_COMMIT_BOUND"
            and manifest.get("finalSeal") is True,
            "certificate is not final commit-bound")
    require(manifest.get("sourceCommit") == certificate["sourceCommit"],
            "certificate source commit drift")
    require(manifest.get("comparison", {}).get("commonCoreSha256")
            == certificate["commonCoreSha256"],
            "certificate manifest commonCore digest drift")
    for commit_key in ("sourceCommit", "certificatePackageCommit"):
        completed = subprocess.run(
            ["git", "cat-file", "-e", certificate[commit_key] + "^{commit}"],
            cwd=ROOT, capture_output=True, check=False,
        )
        require(completed.returncode == 0, f"{commit_key} does not resolve")
    for path, expected in (
        (certificate["primaryPath"], certificate["primarySha256"]),
        (certificate["independentPath"], certificate["independentSha256"]),
        (certificate["manifestPath"], certificate["manifestSha256"]),
    ):
        committed = subprocess.run(
            ["git", "cat-file", "blob",
             certificate["certificatePackageCommit"] + ":" + path],
            cwd=ROOT, capture_output=True, check=False,
        )
        require(committed.returncode == 0, "certificate package blob absent: " + path)
        require(hashlib.sha256(committed.stdout).hexdigest() == expected,
                "certificate package blob hash drift: " + path)
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all", "--",
         "research/certificates/r073w"], cwd=ROOT, capture_output=True,
        check=False,
    )
    require(status.returncode == 0 and not status.stdout,
            "sealed certificate scope is dirty")

    rank_three = common["rankThreeExtension"]
    require(rank_three["field"]["frequencyRank"] == 3,
            "primary witness frequency rank drift")
    require(rank_three["field"]["divergenceFree"] is True,
            "primary witness is not certificate-marked divergence free")
    require(rank_three["signedProduction"]["factored"] == "1/4*q^2*(1-q^2)",
            "positive signed-production formula drift")
    require(rank_three["signedProduction"]["recomputedMinusRPerA3"]["coefficients"]
            == {"2": "-1/4", "4": "1/4"},
            "negative parity branch drift")
    require(rank_three["gradient"]["defectFactored"]
            == "1/2*(1-q^2)*(13+12*q^2+10*q^4+4*q^6)",
            "gradient-defect factorization drift")
    require(rank_three["absorptionRatio"]["cancelledFormula"]
            == "A*q^2/(2*nu*(13+12*q^2+10*q^4+4*q^6))",
            "absorption formula drift")
    require(rank_three["absorptionRatio"]["qToOneCoefficient"] == "1/(78*nu)",
            "zero-scale absorption coefficient drift")
    require(rank_three["parity"] == {
        "gradientDefectEven": True, "productionOdd": True, "stressEven": True,
    }, "parity certificate drift")
    return primary, independent, rank_three


def make_row(
    panel: str, series: str, record: str, x: float, y: float,
    x_name: str, y_name: str, formula: str, evidence_class: str,
    source_primary_path: str, source_independent_path: str,
    normalization: str, note: str,
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
        "source_primary_path": source_primary_path,
        "source_independent_path": source_independent_path,
        "normalization": normalization,
        "note": note,
    }


def absorption_coefficient(s_value: float) -> float:
    z = math.exp(-2.0 * float(s_value))
    return z / (2.0 * (13.0 + 12.0 * z + 10.0 * z * z + 4.0 * z ** 3))


def absorption_stationary_point() -> tuple[float, float, float]:
    # dc/dz=0 iff 13-10*z^2-8*z^3=0.  Bisection is deterministic
    # and the bracket contains the unique root in (0,1).
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2.0
        value = 8.0 * mid ** 3 + 10.0 * mid ** 2 - 13.0
        if value < 0.0:
            lo = mid
        else:
            hi = mid
    z = (lo + hi) / 2.0
    s_value = -0.5 * math.log(z)
    return s_value, z, absorption_coefficient(s_value)


def generate_rows(config: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    a = config["panelA"]
    nu = float(a["nuDrawing"])
    for c_value in a["characteristicConstants"]:
        c_value = float(c_value)
        t_end = min(float(a["tMaximum"]), c_value / nu)
        for index, t_value in enumerate(np.linspace(0.0, t_end,
                                                    int(a["samplesPerCharacteristic"]))):
            s_value = c_value - nu * float(t_value)
            rows.append(make_row(
                "A", f"characteristic-c-{number(c_value)}", f"sample-{index:03d}",
                float(t_value), s_value, "t", "s", "s+nu*t=c",
                "exact-characteristic-renderer-coordinate",
                "research/r073w_signed_production_heat_characteristic.md#eq-3.5",
                "research/r073w_independent_analytic_audit.md#section-2",
                "drawing nu=1; identity valid for nu>0",
                "neutral characteristic guide",
            ))
    c_selected = float(a["selectedConstant"])
    t0 = float(a["selectedT0"])
    t1 = float(a["selectedT1"])
    for index, t_value in enumerate(np.linspace(t0, t1,
                                                int(a["samplesSelectedSegment"]))):
        rows.append(make_row(
            "A", "selected-characteristic", f"sample-{index:03d}", float(t_value),
            c_selected - nu * float(t_value), "t", "s", "s+nu*t=c; s'=-nu",
            "exact-characteristic-renderer-coordinate",
            "research/r073w_signed_production_heat_characteristic.md#eq-3.5",
            "research/r073w_independent_analytic_audit.md#section-2",
            "drawing nu=1; identity valid for nu>0", "highlighted payment path",
        ))
    for label, t_value, note in (
        ("initial-endpoint", t0, "E_initial"),
        ("final-endpoint", t1, "E_final"),
    ):
        rows.append(make_row(
            "A", "payment-endpoint", label, t_value, c_selected - nu * t_value,
            "t", "s", "integral(mean Pi_s(t),t0,t1)=E_initial-E_final",
            "internal-exact-audited-spatial-mean-identity",
            "research/r073w_signed_production_heat_characteristic.md#eq-3.6",
            "research/r073w_independent_analytic_audit.md#section-2",
            "periodic or boundary-decaying transport", note,
        ))

    b = config["panelB"]
    scales = np.linspace(float(b["scaleMinimum"]), float(b["scaleMaximum"]),
                         int(b["samples"]))
    normalization_scale = float(b["normalizationScale"])
    for series, exponent, variable, formula, note in (
        ("fixed-scale-upper", -0.25, "s", "(s/1)^(-1/4)",
         "fixed-scale L1 upper-bound shape"),
        ("cumulative-upper", 0.75, "S", "(S/1)^(3/4)",
         "cumulative-in-scale upper-bound shape"),
    ):
        for index, scale in enumerate(scales):
            y_value = (float(scale) / normalization_scale) ** exponent
            rows.append(make_row(
                "B", series, f"sample-{index:03d}", float(scale), y_value,
                variable, "normalized upper bound", formula,
                "analytic-upper-bound-shape-not-data",
                "research/r073w_signed_production_heat_characteristic.md#section-4",
                "research/r073w_independent_analytic_audit.md#section-3",
                "each envelope equals 1 at unit heat scale",
                note + "; not observations; no sharpness claim",
            ))

    c = config["panelC"]
    c_scales = np.linspace(float(c["sMinimum"]), float(c["sMaximum"]),
                           int(c["samples"]))
    for sign, series, formula, note in (
        (1.0, "plus-R", "+1/4*q^2*(1-q^2)", "u_A=+A*R"),
        (-1.0, "minus-R", "-1/4*q^2*(1-q^2)", "u_A=-A*R"),
    ):
        for index, s_value in enumerate(c_scales):
            q_value = math.exp(-float(s_value))
            y_value = sign * 0.25 * q_value ** 2 * (1.0 - q_value ** 2)
            rows.append(make_row(
                "C", series, f"sample-{index:03d}", float(s_value), y_value,
                "s", "mean(Pi_s)/A^3", formula,
                "two-path-exact-finite-certificate-renderer-sample",
                "research/certificates/r073w/results.json#commonCore.rankThreeExtension.signedProduction",
                "research/certificates/r073w/independent-results.json#commonCore.rankThreeExtension.signedProduction",
                "q=exp(-s); normalized Haar mean on T^3", note,
            ))
    peak_s = 0.5 * math.log(2.0)
    for sign, record in ((1.0, "positive-extremum"), (-1.0, "negative-extremum")):
        rows.append(make_row(
            "C", "exact-extremum", record, peak_s, sign / 16.0,
            "s", "mean(Pi_s)/A^3", "s=log(2)/2; y=+/-1/16",
            "exact-closed-form-landmark",
            "research/certificates/r073w/results.json#commonCore.rankThreeExtension.signedProduction",
            "research/certificates/r073w/independent-results.json#commonCore.rankThreeExtension.signedProduction",
            "q=exp(-s); normalized Haar mean on T^3", "parity-paired extrema",
        ))

    d = config["panelD"]
    d_scales = np.linspace(float(d["sMinimum"]), float(d["sMaximum"]),
                           int(d["samples"]))
    for index, s_value in enumerate(d_scales):
        rows.append(make_row(
            "D", "absorption-coefficient", f"sample-{index:03d}", float(s_value),
            absorption_coefficient(float(s_value)), "s", "c_abs(s)",
            "q^2/(2*(13+12*q^2+10*q^4+4*q^6))",
            "two-path-exact-finite-certificate-renderer-sample",
            "research/certificates/r073w/results.json#commonCore.rankThreeExtension.absorptionRatio",
            "research/certificates/r073w/independent-results.json#commonCore.rankThreeExtension.absorptionRatio",
            "q=exp(-s); coefficient of A/nu", "exact formula; not a fit",
        ))
    rows.append(make_row(
        "D", "exact-landmark", "zero-scale-limit", 0.0, 1.0 / 78.0,
        "s", "c_abs(s)", "lim(s->0+) c_abs(s)=1/78",
        "exact-closed-form-landmark",
        "research/certificates/r073w/results.json#commonCore.rankThreeExtension.absorptionRatio.qToOneCoefficient",
        "research/certificates/r073w/independent-results.json#commonCore.rankThreeExtension.absorptionRatio.qToOneCoefficient",
        "coefficient of A/nu", "exact endpoint",
    ))
    stationary_s, stationary_z, stationary_y = absorption_stationary_point()
    rows.append(make_row(
        "D", "exact-landmark", "interior-maximum", stationary_s, stationary_y,
        "s", "c_abs(s)", "8*z^3+10*z^2-13=0; z=exp(-2*s)",
        "independently-derived-closed-form-stationary-landmark",
        "research/r073w_finite_diagnostic_audit.md#eq-3.6",
        "plot.py#absorption_stationary_point",
        "coefficient of A/nu", "z=" + number(stationary_z),
    ))
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    with (HERE / "source-data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def selected(rows: Iterable[dict[str, str]], panel: str, series: str) -> list[dict[str, str]]:
    return [row for row in rows if row["panel"] == panel and row["series"] == series]


def xy(rows: Iterable[dict[str, str]], panel: str, series: str) -> tuple[np.ndarray, np.ndarray]:
    values = selected(rows, panel, series)
    return (np.array([float(row["x"]) for row in values]),
            np.array([float(row["y"]) for row in values]))


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


def panel_header(ax: Any, label: str, title: str, subtitle: str) -> None:
    ax.text(0.0, 1.195, f"{label}  {title}", transform=ax.transAxes,
            ha="left", va="bottom", fontsize=9.0, fontweight="semibold",
            clip_on=False)
    ax.text(0.0, 1.095, subtitle, transform=ax.transAxes,
            ha="left", va="bottom", fontsize=6.45, color="#66717b",
            clip_on=False)


def style_axis(ax: Any, palette: dict[str, str]) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", which="major", labelsize=6.4, length=2.5,
                   width=0.6, pad=2.0)
    ax.grid(True, color=palette["gridGrey"], linewidth=0.55, alpha=0.9,
            zorder=0)
    ax.set_axisbelow(True)


def add_research_blossom(fig: Any, palette: dict[str, str]) -> None:
    """Locked, data-free research blossom used by the repository figure family."""
    center_x, center_y = 0.966, 0.957
    for index in range(5):
        angle = 90.0 + 72.0 * index
        radians = math.radians(angle)
        petal = Ellipse(
            (center_x + 0.0095 * math.cos(radians),
             center_y + 0.016 * math.sin(radians)),
            width=0.014,
            height=0.028,
            angle=angle - 90.0,
            transform=fig.transFigure,
            facecolor=matplotlib.colors.to_rgba(palette["blue"], 0.18),
            edgecolor=palette["blue"],
            linewidth=0.55,
            zorder=20,
        )
        petal.set_gid(f"research-blossom-petal-{index + 1}")
        fig.add_artist(petal)
    center = Circle(
        (center_x, center_y), 0.0039, transform=fig.transFigure,
        facecolor=palette["orange"], edgecolor=palette["paper"],
        linewidth=0.4, zorder=21,
    )
    center.set_gid("research-blossom-center")
    fig.add_artist(center)


def render(rows: list[dict[str, str]], config: dict[str, Any]) -> dict[str, Any]:
    palette = config["palette"]
    configure_matplotlib(palette)
    mm = 1.0 / 25.4
    width = float(config["widthMillimetres"]) * mm
    height = float(config["heightMillimetres"]) * mm
    fig, axes = plt.subplots(2, 2, figsize=(width, height), facecolor=palette["paper"])
    fig.subplots_adjust(left=0.086, right=0.985, bottom=0.118, top=0.858,
                        wspace=0.31, hspace=0.72)
    fig.text(0.086, 0.965, "Signed production across the heat scale",
             ha="left", va="top", fontsize=11.1, fontweight="semibold",
             color=palette["ink"])
    fig.text(0.936, 0.965, "R0.73W  ·  exact identities and finite witness",
             ha="right", va="top", fontsize=6.3, color=palette["midGrey"])
    add_research_blossom(fig, palette)
    fig.text(0.5, 0.018,
             "Exact/audited formulas · analytic renderer samples, no DNS or fit · "
             "reproducible journal-figure package · NOT CLAY",
             ha="center", va="bottom", fontsize=5.65, color=palette["midGrey"])

    ax = axes[0, 0]
    style_axis(ax, palette)
    panel_header(ax, "A", "Heat-plane endpoint payment",
                 r"$s+\nu t=c$,  $s'(t)=-\nu$  (drawing coordinates: $\nu=1$)")
    for c_value in config["panelA"]["characteristicConstants"]:
        xs, ys = xy(rows, "A", f"characteristic-c-{number(float(c_value))}")
        ax.plot(xs, ys, color=palette["midGrey"], linewidth=0.85,
                linestyle=(0, (3.2, 2.4)), alpha=0.78, zorder=1)
        if float(c_value) != float(config["panelA"]["selectedConstant"]):
            x_label = min(0.055, xs[-1] * 0.35)
            y_label = float(c_value) - x_label
            ax.text(x_label, y_label + 0.03, f"c={float(c_value):.2g}",
                    fontsize=5.5, color=palette["midGrey"], rotation=-36,
                    ha="left", va="bottom")
    xs, ys = xy(rows, "A", "selected-characteristic")
    ax.plot(xs, ys, color=palette["blue"], linewidth=2.15, solid_capstyle="round",
            zorder=4)
    endpoints = selected(rows, "A", "payment-endpoint")
    x0, y0 = float(endpoints[0]["x"]), float(endpoints[0]["y"])
    x1, y1 = float(endpoints[1]["x"]), float(endpoints[1]["y"])
    ax.scatter([x0], [y0], s=31, marker="o", facecolor=palette["blue"],
               edgecolor=palette["paper"], linewidth=0.8, zorder=6)
    ax.scatter([x1], [y1], s=34, marker="s", facecolor=palette["paper"],
               edgecolor=palette["orange"], linewidth=1.4, zorder=6)
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops={"arrowstyle": "-|>", "color": palette["blue"],
                            "linewidth": 1.2, "mutation_scale": 8.0}, zorder=5)
    ax.text(x0 - 0.015, y0 + 0.095, r"$E_0$", fontsize=6.6,
            color=palette["blue"], ha="center")
    ax.text(x1 + 0.025, y1 - 0.11, r"$E_1$", fontsize=6.6,
            color=palette["orange"], ha="left")
    ax.text(0.96, 0.91,
            r"$\int_{t_0}^{t_1}\!\langle\Pi_{s(t)}\rangle\,dt$" "\n"
            r"$=\ E_0-E_1$",
            transform=ax.transAxes, ha="right", va="top", fontsize=7.1,
            linespacing=1.35,
            bbox={"boxstyle": "round,pad=0.28", "facecolor": palette["paper"],
                  "edgecolor": palette["lightGrey"], "linewidth": 0.7})
    ax.text(0.62, 0.61, r"signed mean payment", transform=ax.transAxes,
            ha="center", va="center", fontsize=5.5, color=palette["blue"],
            rotation=-29)
    ax.set_xlim(0.0, float(config["panelA"]["tMaximum"]))
    ax.set_ylim(0.0, float(config["panelA"]["sMaximum"]))
    ax.set_xlabel(r"physical time  $t$", fontsize=6.8, labelpad=2.5)
    ax.set_ylabel(r"heat scale  $s$", fontsize=6.8, labelpad=2.5)

    ax = axes[0, 1]
    style_axis(ax, palette)
    panel_header(ax, "B", "Energy-class scale envelopes",
                 "ANALYTIC BOUNDS · UNIT-SCALE NORMALIZED · NOT DATA")
    x_fixed, y_fixed = xy(rows, "B", "fixed-scale-upper")
    x_cumulative, y_cumulative = xy(rows, "B", "cumulative-upper")
    ax.plot(x_fixed, y_fixed, color=palette["blue"], linewidth=1.9,
            linestyle="-", marker="o", markersize=2.8, markevery=24,
            markerfacecolor=palette["blue"], markeredgewidth=0.0,
            label=r"fixed scale  $s^{-1/4}$", zorder=3)
    ax.plot(x_cumulative, y_cumulative, color=palette["orange"], linewidth=1.8,
            linestyle=(0, (5.0, 2.2)), marker="s", markersize=3.0, markevery=24,
            markerfacecolor=palette["paper"], markeredgecolor=palette["orange"],
            markeredgewidth=0.9, label=r"cumulative  $S^{3/4}$", zorder=3)
    ax.axvline(1.0, color=palette["lightGrey"], linewidth=0.8,
               linestyle=(0, (1.5, 2.0)), zorder=1)
    ax.axhline(1.0, color=palette["lightGrey"], linewidth=0.8,
               linestyle=(0, (1.5, 2.0)), zorder=1)
    ax.scatter([1.0], [1.0], marker="D", s=22, facecolor=palette["paper"],
               edgecolor=palette["midGrey"], linewidth=0.8, zorder=5)
    ax.annotate("unit-scale normalization", xy=(1.0, 1.0), xytext=(1.45, 0.28),
                fontsize=5.3, color=palette["midGrey"], ha="right", va="bottom",
                arrowprops={"arrowstyle": "-", "color": palette["midGrey"],
                            "linewidth": 0.65})
    ax.set_xlim(float(config["panelB"]["scaleMinimum"]),
                float(config["panelB"]["scaleMaximum"]))
    ax.set_xticks([0.02, 0.3, 0.6, 0.9, 1.2, 1.5])
    ax.set_xticklabels(["0.02", ".3", ".6", ".9", "1.2", "1.5"])
    ax.set_ylim(0.0, max(float(y_fixed.max()), float(y_cumulative.max())) * 1.08)
    ax.set_xlabel("normalized heat scale", fontsize=6.8, labelpad=2.5)
    ax.set_ylabel("normalized bound shape", fontsize=6.8, labelpad=2.5)
    ax.legend(loc="upper right", frameon=True, fancybox=False, framealpha=0.96,
              facecolor=palette["paper"], edgecolor=palette["lightGrey"],
              fontsize=5.8, handlelength=2.7, borderpad=0.35, labelspacing=0.35)

    ax = axes[1, 0]
    style_axis(ax, palette)
    panel_header(ax, "C", "Exact rank-three sign pair",
                 r"$u_A=\pm A R$,  $q=e^{-s}$  ·  two-path finite certificate")
    x_plus, y_plus = xy(rows, "C", "plus-R")
    x_minus, y_minus = xy(rows, "C", "minus-R")
    ax.plot(x_plus, y_plus, color=palette["blue"], linewidth=1.9,
            linestyle="-", marker="o", markersize=2.7, markevery=30,
            markerfacecolor=palette["blue"], markeredgewidth=0,
            label=r"$+R$: $+\frac{1}{4}q^2(1-q^2)$", zorder=3)
    ax.plot(x_minus, y_minus, color=palette["orange"], linewidth=1.8,
            linestyle=(0, (5.0, 2.1)), marker="s", markersize=3.0, markevery=30,
            markerfacecolor=palette["paper"], markeredgecolor=palette["orange"],
            markeredgewidth=0.9, label=r"$-R$: $-\frac{1}{4}q^2(1-q^2)$", zorder=3)
    extrema = selected(rows, "C", "exact-extremum")
    peak_s = float(extrema[0]["x"])
    ax.scatter([peak_s], [1.0 / 16.0], marker="o", s=31,
               facecolor=palette["blue"], edgecolor=palette["paper"],
               linewidth=0.8, zorder=5)
    ax.scatter([peak_s], [-1.0 / 16.0], marker="s", s=34,
               facecolor=palette["paper"], edgecolor=palette["orange"],
               linewidth=1.25, zorder=5)
    ax.axhline(0.0, color=palette["midGrey"], linewidth=0.75, zorder=1)
    ax.annotate(r"$|\mathrm{peak}|=1/16$" "\n" r"$s=\frac{1}{2}\log 2$",
                xy=(peak_s, 1.0 / 16.0), xytext=(0.76, 0.0505),
                fontsize=5.7, ha="left", va="center",
                arrowprops={"arrowstyle": "-", "color": palette["midGrey"],
                            "linewidth": 0.7})
    ax.set_xlim(float(config["panelC"]["sMinimum"]),
                float(config["panelC"]["sMaximum"]))
    ax.set_ylim(-0.073, 0.073)
    ax.set_xlabel(r"heat scale  $s$", fontsize=6.8, labelpad=2.5)
    ax.set_ylabel(r"$\langle\Pi_s\rangle/A^3$", fontsize=6.8, labelpad=2.5)
    ax.legend(loc="lower right", frameon=True, fancybox=False, framealpha=0.96,
              facecolor=palette["paper"], edgecolor=palette["lightGrey"],
              fontsize=5.55, handlelength=2.7, borderpad=0.35, labelspacing=0.32)

    ax = axes[1, 1]
    style_axis(ax, palette)
    panel_header(ax, "D", "Dimensionless absorption coefficient",
                 r"$c_{\rm abs}=q^2/[2(13+12q^2+10q^4+4q^6)]$  ·  exact, not fit")
    x_abs, y_abs = xy(rows, "D", "absorption-coefficient")
    ax.plot(x_abs, y_abs, color=palette["blue"], linewidth=2.0,
            linestyle="-", marker="o", markersize=2.6, markevery=30,
            markerfacecolor=palette["blue"], markeredgewidth=0, zorder=3,
            label=r"coefficient of $A/\nu$")
    landmarks = selected(rows, "D", "exact-landmark")
    endpoint = next(row for row in landmarks if row["record"] == "zero-scale-limit")
    maximum = next(row for row in landmarks if row["record"] == "interior-maximum")
    endpoint_xy = float(endpoint["x"]), float(endpoint["y"])
    maximum_xy = float(maximum["x"]), float(maximum["y"])
    ax.axhline(1.0 / 78.0, color=palette["midGrey"], linewidth=0.8,
               linestyle=(0, (2.0, 2.0)), zorder=1)
    ax.scatter([endpoint_xy[0]], [endpoint_xy[1]], marker="s", s=38,
               facecolor=palette["paper"], edgecolor=palette["orange"],
               linewidth=1.35, zorder=5)
    ax.scatter([maximum_xy[0]], [maximum_xy[1]], marker="D", s=25,
               facecolor=palette["blue"], edgecolor=palette["paper"],
               linewidth=0.7, zorder=5)
    ax.annotate(r"$s\downarrow0:\ 1/78$", xy=endpoint_xy,
                xytext=(0.34, 0.01125), fontsize=6.0, color=palette["orange"],
                ha="left", va="center",
                arrowprops={"arrowstyle": "->", "color": palette["orange"],
                            "linewidth": 0.85, "mutation_scale": 8.0})
    ax.annotate("small interior maximum", xy=maximum_xy,
                xytext=(0.46, 0.01385), fontsize=5.25,
                color=palette["midGrey"], ha="left", va="bottom",
                arrowprops={"arrowstyle": "-", "color": palette["midGrey"],
                            "linewidth": 0.65})
    ax.set_xlim(float(config["panelD"]["sMinimum"]),
                float(config["panelD"]["sMaximum"]))
    ax.set_ylim(0.0, max(float(y_abs.max()) * 1.11, 0.0144))
    ax.set_xlabel(r"heat scale  $s$", fontsize=6.8, labelpad=2.5)
    ax.set_ylabel(r"$c_{\rm abs}(s)$", fontsize=6.8, labelpad=2.5)
    ax.legend(loc="upper right", frameon=True, fancybox=False, framealpha=0.96,
              facecolor=palette["paper"], edgecolor=palette["lightGrey"],
              fontsize=5.65, handlelength=2.6, borderpad=0.35)

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bounds_failures: list[dict[str, object]] = []
    figure_box = fig.bbox
    tolerance = 0.5
    for artist in fig.findobj(match=lambda item: isinstance(item, Text)):
        if not artist.get_visible() or not artist.get_text().strip():
            continue
        box = artist.get_window_extent(renderer=renderer)
        if (box.x0 < figure_box.x0 - tolerance or box.y0 < figure_box.y0 - tolerance
                or box.x1 > figure_box.x1 + tolerance
                or box.y1 > figure_box.y1 + tolerance):
            bounds_failures.append({
                "text": artist.get_text(),
                "bboxPixels": [box.x0, box.y0, box.x1, box.y1],
            })
    require(not bounds_failures, "text artist outside figure bounds: " + repr(bounds_failures))

    pdf_metadata = {
        "Title": "R0.73W signed production across the heat scale",
        "Author": "R0.73W research package",
        "Subject": "Exact identities, energy-class envelopes, and rank-three witness",
        "Creator": "Matplotlib deterministic local renderer",
        "CreationDate": None,
        "ModDate": None,
    }
    svg_metadata = {
        "Title": "R0.73W signed production across the heat scale",
        "Description": "Exact heat-plane identity and finite rank-three witness",
        "Creator": "Matplotlib deterministic local renderer",
        "Date": None,
    }
    fig.savefig(HERE / "figure.svg", format="svg", facecolor=palette["paper"],
                metadata=svg_metadata)
    fig.savefig(HERE / "figure.pdf", format="pdf", facecolor=palette["paper"],
                metadata=pdf_metadata)
    fig.savefig(HERE / "figure.png", format="png", dpi=int(config["pngDpi"]),
                facecolor=palette["paper"],
                metadata={"Software": "Matplotlib deterministic local renderer"})
    plt.close(fig)

    with Image.open(HERE / "figure.png") as master_open:
        master = master_open.convert("RGB")
        qa_width = min(int(config["qaMaximumWidthPixels"]), master.width)
        qa_height = round(master.height * qa_width / master.width)
        final_size = master.resize((qa_width, qa_height), Image.Resampling.LANCZOS)
        final_size.save(HERE / "qa-final-size.png", format="PNG", optimize=True)
        ImageOps.grayscale(final_size).convert("RGB").save(
            HERE / "qa-grayscale.png", format="PNG", optimize=True,
        )
        master_size = [master.width, master.height]

    document = pdfium.PdfDocument(str(HERE / "figure.pdf"))
    require(len(document) == 1, "rendered PDF is not one page")
    page = document[0]
    page_width, page_height = page.get_size()
    scale = int(config["qaMaximumWidthPixels"]) / float(page_width)
    pdf_bitmap = page.render(scale=scale)
    pdf_image = pdf_bitmap.to_pil().convert("RGB")
    pdf_image.save(HERE / "qa-pdf.png", format="PNG", optimize=True)
    pdf_size = [pdf_image.width, pdf_image.height]
    page.close()
    document.close()

    return {
        "artistBoundsFailures": bounds_failures,
        "artistBoundsPass": not bounds_failures,
        "figureInches": [width, height],
        "masterPngPixels": master_size,
        "pdfQaPixels": pdf_size,
        "qaFinalSizePixels": [qa_width, qa_height],
    }


def main() -> int:
    args = parse_args()
    monitor = Monitor()
    monitor.event("start", mode="data-only" if args.data_only else "render-preseal")
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    require(config["figureId"] == FIGURE_ID and contract["figureId"] == FIGURE_ID,
            "figure id drift")
    versions = package_versions()
    require(versions == EXPECTED_PACKAGES,
            "dependency version drift: " + repr(versions))
    primary, independent, rank_three = verify_inputs(contract)
    monitor.event("inputs-verified", commonCoreEqual=primary["commonCore"] == independent["commonCore"])
    rows = generate_rows(config)
    write_csv(rows)
    panel_counts = {panel: sum(row["panel"] == panel for row in rows)
                    for panel in ("A", "B", "C", "D")}
    monitor.event("source-data-written", rows=len(rows), panelCounts=panel_counts)
    render_report: dict[str, Any] = {"skipped": True}
    if args.render_preseal:
        render_report = render(rows, config)
        monitor.event("render-complete", outputs=["figure.svg", "figure.pdf", "figure.png"],
                      qaAssets=["qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"])

    stationary_s, stationary_z, stationary_y = absorption_stationary_point()
    results = {
        "schemaVersion": "r073w-signed-production-figure-results-v1",
        "allSourceChecksPass": True,
        "certificate": {
            "commonCoreByteIdentical": primary["commonCore"] == independent["commonCore"],
            "commonCoreSha256": contract["certificate"]["commonCoreSha256"],
            "independentSha256": contract["certificate"]["independentSha256"],
            "primarySha256": contract["certificate"]["primarySha256"],
            "rankThreeFrequencySupport": rank_three["field"]["frequencyRank"],
        },
        "exactConstants": {
            "absorptionInteriorMaximum": {
                "coefficient": stationary_y,
                "s": stationary_s,
                "z": stationary_z,
                "stationaryEquation": "8*z^3+10*z^2-13=0",
            },
            "absorptionZeroScaleLimit": "1/78",
            "productionPeakMagnitude": "1/16",
            "productionPeakScale": "log(2)/2",
        },
        "panelRowCounts": panel_counts,
        "render": render_report,
        "sourceDataRows": len(rows),
        "scope": {
            "dgxUsed": False,
            "fittedScalingLaw": False,
            "navierStokesSimulation": False,
            "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
            "notClay": True,
        },
    }
    (HERE / "results.json").write_text(canonical(results), encoding="utf-8")

    environment = {
        "schemaVersion": "r073w-signed-production-environment-v1",
        "createdUtc": utc_now(),
        "execution": {
            "cpu": f"{platform.machine()} / {os.cpu_count() or 1} logical CPUs",
            "dgxUsed": False,
            "gpu": "not used",
            "host": socket.gethostname(),
            "logicalCpuCount": os.cpu_count() or 1,
            "machine": platform.machine(),
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
            "dependencyPath": str(Path(args.deps).resolve()) if args.deps else "active environment",
            "pythonExecutable": sys.executable,
        },
    }
    (HERE / "environment.json").write_text(canonical(environment), encoding="utf-8")
    monitor.event("metadata-written", status="prepublication")
    monitor.write()
    print(json.dumps({
        "figureId": FIGURE_ID,
        "mode": "data-only" if args.data_only else "render-preseal",
        "panelRowCounts": panel_counts,
        "rows": len(rows),
        "status": "ok",
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
