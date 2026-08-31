#!/usr/bin/env python3
"""Generate the R0.73V signed-third-order interface formal figure."""

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
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
START = time.monotonic()
FIGURE_ID = "fig-r073v-signed-third-order-interface"
PRIMARY_RELATIVE = Path("research/certificates/r073v/results.json")
INDEPENDENT_RELATIVE = Path("research/certificates/r073v/independent-results.json")
CSV_FIELDS = (
    "panel", "series", "record", "component_i", "component_j", "mode",
    "parameter", "x", "y", "exact_value", "q_polynomial",
    "coefficient_map", "small_s_order", "leading_coefficient",
    "evidence_class", "source_primary_path", "source_independent_path",
    "normalization", "primary_sha256", "independent_sha256",
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


def compact(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


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


def memory_gib() -> float:
    completed = subprocess.run(
        ["sysctl", "-n", "hw.memsize"], capture_output=True, check=False, text=True,
    )
    if completed.returncode == 0 and completed.stdout.strip().isdigit():
        return round(int(completed.stdout.strip()) / (1024.0 ** 3), 3)
    pages = os.sysconf("SC_PHYS_PAGES") if hasattr(os, "sysconf") else 0
    page_size = os.sysconf("SC_PAGE_SIZE") if hasattr(os, "sysconf") else 0
    return round(float(pages * page_size) / (1024.0 ** 3), 3) if pages and page_size else 1.0


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


def certificate_pair(contract: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    primary_path = ROOT / PRIMARY_RELATIVE
    independent_path = ROOT / INDEPENDENT_RELATIVE
    primary = load_json(primary_path)
    independent = load_json(independent_path)
    cert = contract["certificate"]
    if sha256(primary_path) != cert["primarySha256"]:
        raise RuntimeError("primary certificate hash drift")
    if sha256(independent_path) != cert["independentSha256"]:
        raise RuntimeError("independent certificate hash drift")
    if primary.get("commonCore") != independent.get("commonCore"):
        raise RuntimeError("two-path commonCore mismatch")
    common_text = canonical(primary["commonCore"])
    if hashlib.sha256(common_text.encode("utf-8")).hexdigest() != cert["commonCoreSha256"]:
        raise RuntimeError("commonCore canonical digest drift")
    if primary["commonCore"].get("tableDigest") != cert["completeTableDigest"]:
        raise RuntimeError("complete-table digest drift")
    return primary, independent


def csv_row(
    hashes: tuple[str, str], panel: str, series: str, record: str,
    component_i: str = "", component_j: str = "", mode: str = "",
    parameter: str = "", x: float | None = None, y: float | None = None,
    exact_value: str = "", q_polynomial: str = "", coefficient_map: object = "",
    small_s_order: object = "", leading_coefficient: str = "",
    evidence_class: str = "exact-two-path-certificate",
    source_primary_path: str = "", source_independent_path: str = "",
    normalization: str = "q=exp(-s); normalized Haar measure on T^3",
) -> dict[str, str]:
    return {
        "panel": panel,
        "series": series,
        "record": record,
        "component_i": component_i,
        "component_j": component_j,
        "mode": mode,
        "parameter": parameter,
        "x": "" if x is None else format(x, ".17g"),
        "y": "" if y is None else format(y, ".17g"),
        "exact_value": exact_value,
        "q_polynomial": q_polynomial,
        "coefficient_map": compact(coefficient_map) if isinstance(coefficient_map, (dict, list)) else str(coefficient_map),
        "small_s_order": str(small_s_order),
        "leading_coefficient": leading_coefficient,
        "evidence_class": evidence_class,
        "source_primary_path": source_primary_path,
        "source_independent_path": source_independent_path,
        "normalization": normalization,
        "primary_sha256": hashes[0],
        "independent_sha256": hashes[1],
    }


def active_matrix_rows(
    rows: list[dict[str, str]], hashes: tuple[str, str], panel: str,
    series: str, matrix: list[list[dict[str, Any]]], primary_path: str,
    independent_path: str, mode: str, q_polynomial: str,
) -> None:
    for i in range(2):
        for j in range(2):
            entry = matrix[i][j]
            rows.append(csv_row(
                hashes, panel, series, f"{series}-{i + 1}{j + 1}",
                component_i=str(i + 1), component_j=str(j + 1), mode=mode,
                exact_value=compact(entry), q_polynomial=q_polynomial,
                coefficient_map=entry["coefficients"],
                small_s_order=entry["smallS"]["order"],
                leading_coefficient=entry["smallS"]["leadingCoefficient"],
                source_primary_path=f"{primary_path}.{i}.{j}",
                source_independent_path=f"{independent_path}.{i}.{j}",
            ))


def generate_rows(
    config: dict[str, Any], contract: dict[str, Any],
    primary: dict[str, Any], independent: dict[str, Any],
) -> list[dict[str, str]]:
    hashes = (contract["certificate"]["primarySha256"], contract["certificate"]["independentSha256"])
    core = primary["commonCore"]
    rows: list[dict[str, str]] = [
        csv_row(hashes, "META", "two_path", "common-core-equality",
                exact_value="TRUE", coefficient_map={"sha256": contract["certificate"]["commonCoreSha256"]},
                source_primary_path="commonCore", source_independent_path="commonCore"),
        csv_row(hashes, "META", "two_path", "complete-table-digest",
                exact_value=core["tableDigest"],
                source_primary_path="commonCore.tableDigest",
                source_independent_path="commonCore.tableDigest"),
        csv_row(hashes, "A", "definition", "pressure-aware-nonlinearity",
                mode="continuum", exact_value="N=P div(u tensor u)",
                source_primary_path="compressedLift.definition",
                source_independent_path="commonCore.compressedTarget"),
        csv_row(hashes, "A", "definition", "raw-lift",
                mode="continuum", exact_value="Ccal_s=P_s(u odot N)",
                source_primary_path="compressedLift.definition",
                source_independent_path="commonCore.compressedTarget.Ccal"),
        csv_row(hashes, "A", "definition", "signed-residual",
                mode="continuum", exact_value=primary["compressedLift"]["definition"],
                source_primary_path="compressedLift.definition",
                source_independent_path="commonCore.compressedTarget.chi"),
    ]

    compressed = core["compressedTarget"]
    active_matrix_rows(rows, hashes, "A", "Ccal", compressed["Ccal"],
                       "commonCore.compressedTarget.Ccal", "commonCore.compressedTarget.Ccal",
                       "h*=(1,2,0)", "-q^5*K")
    active_matrix_rows(rows, hashes, "A", "resolved", compressed["resolved"],
                       "commonCore.compressedTarget.resolved", "commonCore.compressedTarget.resolved",
                       "h*=(1,2,0)", "-q^3*K")
    active_matrix_rows(rows, hashes, "A", "chi", compressed["chi"],
                       "commonCore.compressedTarget.chi", "commonCore.compressedTarget.chi",
                       "h*=(1,2,0)", "(q^3-q^5)*K")
    active_matrix_rows(rows, hashes, "A", "chiSignPairDifference", compressed["signPairDifference"],
                       "commonCore.compressedTarget.signPairDifference",
                       "commonCore.compressedTarget.signPairDifference",
                       "h*=(1,2,0)", "2*(q^3-q^5)*K")

    four = core["fourSiteTarget"]
    b_specs = (
        ("localKappaFlux", "q^3*(1-q^2)^2*(q^2+2)*[[2,-3],[-3,4]]"),
        ("pressureDiffusion", "q^3*(1-q^2)*[[4,2],[2,-8]]"),
        ("pressureStrainXi", "q^3*(1-q^2)*[[-4,0],[0,4]]"),
    )
    for series, formula in b_specs:
        active_matrix_rows(rows, hashes, "B", series, four[series],
                           f"commonCore.fourSiteTarget.{series}",
                           f"commonCore.fourSiteTarget.{series}",
                           "h*=(1,2,0)", formula)
    combined: list[list[dict[str, Any]]] = []
    for i in range(3):
        combined_row = []
        for j in range(3):
            left = four["pressureDiffusion"][i][j]
            right = four["pressureStrainXi"][i][j]
            coefficients: dict[str, str] = {}
            for exponent in sorted(set(left["coefficients"]) | set(right["coefficients"]), key=int):
                value = int(left["coefficients"].get(exponent, "0")) + int(right["coefficients"].get(exponent, "0"))
                if value:
                    coefficients[exponent] = str(value)
            if coefficients:
                leading = sum(int(value) * ((-int(exponent)) ** 1) for exponent, value in coefficients.items())
                small = {"order": 1, "leadingCoefficient": str(leading)}
            else:
                small = {"order": "infinity", "leadingCoefficient": "0"}
            combined_row.append({"coefficients": coefficients, "smallS": small})
        combined.append(combined_row)
    active_matrix_rows(rows, hashes, "B", "combinedPressure", combined,
                       "derived:commonCore.fourSiteTarget.pressureDiffusion+pressureStrainXi",
                       "derived:commonCore.fourSiteTarget.pressureDiffusion+pressureStrainXi",
                       "h*=(1,2,0)", "q^3*(1-q^2)*[[0,2],[2,-4]]")

    six = core["sixSiteZeroMode"]
    for series in ("contractedKappaFlux", "pressureDiffusion", "pressureStrainXi"):
        formula = {
            "contractedKappaFlux": "0",
            "pressureDiffusion": "0",
            "pressureStrainXi": "(1-q^4)*diag(-48,48,0)",
        }[series]
        active_matrix_rows(rows, hashes, "C", series, six[series],
                           f"commonCore.sixSiteZeroMode.{series}",
                           f"commonCore.sixSiteZeroMode.{series}",
                           "h=(0,0,0)", formula)

    quartic = core["quarticSelected"]
    coeff = quartic["coefficient"]
    rows.append(csv_row(
        hashes, "D", "quarticSelected", "q-polynomial", component_i="112",
        mode="h=(0,2,0)", exact_value="2*i*q^2*(1-q^2)^2",
        q_polynomial="2*i*q^2-4*i*q^4+2*i*q^6",
        coefficient_map=coeff["coefficients"], small_s_order=coeff["smallS"]["order"],
        leading_coefficient=coeff["smallS"]["leadingCoefficient"],
        source_primary_path="commonCore.quarticSelected.coefficient",
        source_independent_path="commonCore.quarticSelected.coefficient",
    ))
    finite = quartic["finiteEpsilonAtQHalf"]
    for epsilon, value in finite["samples"].items():
        rows.append(csv_row(
            hashes, "D", "finiteEpsilon", f"epsilon-{epsilon}", parameter=f"epsilon={epsilon}",
            exact_value=value, source_primary_path=f"commonCore.quarticSelected.finiteEpsilonAtQHalf.samples.{epsilon}",
            source_independent_path=f"commonCore.quarticSelected.finiteEpsilonAtQHalf.samples.{epsilon}",
        ))
    rows.append(csv_row(
        hashes, "D", "finiteEpsilon", "extracted-linear-coefficient",
        parameter="q=1/2", exact_value=finite["extractedLinearCoefficient"],
        source_primary_path="commonCore.quarticSelected.finiteEpsilonAtQHalf.extractedLinearCoefficient",
        source_independent_path="commonCore.quarticSelected.finiteEpsilonAtQHalf.extractedLinearCoefficient",
    ))
    rows.append(csv_row(
        hashes, "D", "dilation", "selected-quartic-parabolic",
        parameter="s=theta*L^(-2)", exact_value=primary["dilation"]["quarticSelected"],
        q_polynomial="2*i*L*exp(-2*theta)*(1-exp(-2*theta))^2",
        source_primary_path="dilation.quarticSelected",
        source_independent_path="commonCore.quarticSelected.coefficient",
        normalization="u_L(x)=u(L*x); mode=L*(0,2,0); s=theta*L^(-2)",
    ))
    rows.append(csv_row(
        hashes, "D", "dilation", "compressed-sign-pair-frobenius",
        parameter="s=theta*L^(-2)",
        exact_value=primary["compressedLift"]["dilationAtSThetaOverLSquaredFrobeniusSignDifference"],
        source_primary_path="compressedLift.dilationAtSThetaOverLSquaredFrobeniusSignDifference",
        source_independent_path="commonCore.compressedTarget.signPairDifference",
        normalization="Frobenius norm; h*=L*(1,2,0); s=theta*L^(-2)",
    ))
    start = float(config["quarticThetaMinimum"])
    stop = float(config["quarticThetaMaximum"])
    step = float(config["quarticThetaStep"])
    count = int(round((stop - start) / step))
    for index in range(count + 1):
        theta = start + index * step
        value = 2.0 * math.exp(-2.0 * theta) * (1.0 - math.exp(-2.0 * theta)) ** 2
        rows.append(csv_row(
            hashes, "D", "quarticProfile", f"analytic-sample-{index:03d}",
            parameter=f"theta={theta:.2f}", x=theta, y=value,
            exact_value="2*exp(-2*theta)*(1-exp(-2*theta))^2",
            evidence_class="analytic-renderer-sample-from-exact-certificate-formula",
            source_primary_path="dilation.quarticSelected",
            source_independent_path="commonCore.quarticSelected.coefficient",
            normalization="absolute coefficient divided by L; s=theta*L^(-2)",
        ))
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def add_box(
    ax: Any, x: float, y: float, w: float, h: float, face: str, edge: str,
    title: str, body: str, title_color: str, body_size: float = 5.8,
    align: str = "center",
) -> None:
    from matplotlib.patches import FancyBboxPatch  # type: ignore
    patch = FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.010,rounding_size=0.018",
        transform=ax.transAxes, linewidth=0.85, facecolor=face, edgecolor=edge,
        clip_on=False,
    )
    ax.add_patch(patch)
    text_x = x + (0.045 * w if align == "left" else 0.5 * w)
    ha = "left" if align == "left" else "center"
    ax.text(text_x, y + 0.77 * h, title, transform=ax.transAxes,
            ha=ha, va="center", fontsize=5.3, fontweight="bold", color=title_color)
    ax.text(text_x, y + 0.38 * h, body, transform=ax.transAxes,
            ha=ha, va="center", fontsize=body_size, color=title_color,
            family="DejaVu Sans Mono" if "[" in body else "DejaVu Sans")


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
        "font.size": 6.8,
        "axes.titlesize": 7.8,
        "axes.labelsize": 6.4,
        "axes.edgecolor": palette["ink"],
        "axes.linewidth": 0.65,
        "xtick.labelsize": 5.8,
        "ytick.labelsize": 5.8,
        "text.color": palette["ink"],
        "axes.labelcolor": palette["ink"],
        "xtick.color": palette["ink"],
        "ytick.color": palette["ink"],
        "svg.hashsalt": "r073v-signed-third-order-interface",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })
    figure = plt.figure(figsize=(width, height), facecolor=palette["paper"])
    grid = figure.add_gridspec(
        2, 2, left=0.047, right=0.982, bottom=0.125, top=0.815,
        wspace=0.20, hspace=0.43, width_ratios=(1.0, 1.0),
    )
    ax_a = figure.add_subplot(grid[0, 0])
    ax_b = figure.add_subplot(grid[0, 1])
    ax_c = figure.add_subplot(grid[1, 0])
    ax_d = figure.add_subplot(grid[1, 1])

    figure.text(0.047, 0.952,
                "Pressure-aware signed third-order heat lift: exact coefficient interfaces",
                fontsize=10.2, fontweight="bold", ha="left", va="top")
    figure.text(0.049, 0.898,
                "Two independent exact Fourier producers | q = exp(-s) | coefficientwise evidence | no PDE simulation",
                fontsize=6.45, color=palette["midGrey"], ha="left", va="top")
    for x, y, radius, color in (
        (0.947, 0.945, 0.010, palette["blueLight"]),
        (0.965, 0.945, 0.008, palette["goldLight"]),
        (0.956, 0.963, 0.007, palette["blue"]),
    ):
        figure.add_artist(Circle((x, y), radius, transform=figure.transFigure,
                                 facecolor=color, edgecolor="none", alpha=0.9))

    # Panel A: pressure-aware signed lift interface.
    ax_a.set_axis_off()
    ax_a.set_title("A  Exact pressure-aware interface", loc="left", fontweight="bold",
                   y=1.075, pad=0)
    ax_a.text(0.0, 1.01, r"four-site target $h_*=(1,2,0)$ | exact $q$-polynomials",
              transform=ax_a.transAxes, fontsize=5.55, color=palette["midGrey"], va="bottom")
    ax_a.text(0.5, 0.91,
              r"$N=\mathbb{P}\nabla\!\cdot(u\otimes u),\quad \chi_s=P_s(u\odot N)-v_s\odot N_s$",
              transform=ax_a.transAxes, fontsize=6.0, ha="center", va="center")
    add_box(ax_a, 0.01, 0.49, 0.29, 0.28, palette["paper"], palette["blue"],
            "RAW LIFT", r"$\widehat{\mathcal{C}}_s=-q^5K$", palette["blueDark"], 6.3)
    add_box(ax_a, 0.355, 0.49, 0.29, 0.28, palette["paper"], palette["midGrey"],
            "RESOLVED", r"$\widehat{v_s\odot N_s}=-q^3K$", palette["ink"], 5.85)
    add_box(ax_a, 0.70, 0.49, 0.29, 0.28, palette["goldLight"], palette["gold"],
            "SIGNED RESIDUAL", r"$\widehat\chi_s=(q^3-q^5)K$", palette["ink"], 5.75)
    ax_a.text(0.328, 0.63, "−", transform=ax_a.transAxes, fontsize=11,
              fontweight="bold", ha="center", va="center")
    ax_a.text(0.673, 0.63, "=", transform=ax_a.transAxes, fontsize=10,
              fontweight="bold", ha="center", va="center")
    ax_a.text(0.5, 0.39,
              r"$K=[[-2,1,0],[1,0,0],[0,0,0]],\qquad \|K\|_F=\sqrt{6}$",
              transform=ax_a.transAxes, fontsize=6.0, ha="center", va="center")
    add_box(ax_a, 0.10, 0.05, 0.80, 0.22, palette["blueLight"], palette["blueDark"],
            "SIGN-PAIR DIFFERENCE",
            r"$\widehat\chi_s(u)-\widehat\chi_s(-u)=2(q^3-q^5)K$",
            palette["blueDark"], 6.2)
    ax_a.text(0.5, -0.015, "exact target coefficient; distinct from the Germano stress source",
              transform=ax_a.transAxes, fontsize=5.3, color=palette["midGrey"],
              ha="center", va="top")

    # Panel B: exact four-site mode decomposition and orders.
    ax_b.set_axis_off()
    ax_b.set_title("B  Four-site mode decomposition", loc="left", fontweight="bold",
                   y=1.075, pad=0)
    ax_b.text(0.0, 1.01, r"$h_*=(1,2,0)$ | exact matrices and certified bottom-scale orders",
              transform=ax_b.transAxes, fontsize=5.55, color=palette["midGrey"], va="bottom")
    add_box(ax_b, 0.01, 0.54, 0.48, 0.34, palette["paper"], palette["blue"],
            r"CUMULANT FLUX  $O(s^2)$",
            "$q^3(1-q^2)^2(q^2+2)$\n[ 2  -3]\n[-3   4]", palette["ink"], 5.55)
    add_box(ax_b, 0.52, 0.54, 0.47, 0.34, palette["paper"], palette["gold"],
            r"PRESSURE DIFFUSION  $O(s)$",
            "$q^3(1-q^2)$\n[4   2]\n[2  -8]", palette["ink"], 5.55)
    add_box(ax_b, 0.01, 0.13, 0.48, 0.31, palette["paper"], palette["gold"],
            r"PRESSURE STRAIN  $O(s)$",
            "$q^3(1-q^2)$\n[-4   0]\n[ 0   4]", palette["ink"], 5.55)
    add_box(ax_b, 0.52, 0.13, 0.47, 0.31, palette["goldLight"], palette["gold"],
            r"COMBINED PRESSURE  $O(s)$",
            "$q^3(1-q^2)$\n[0   2]\n[2  -4]", palette["ink"], 5.55)
    ax_b.text(0.5, 0.015,
              r"exact orders: $s^2$ vs $s$ $\Rightarrow$ coefficientwise absorption costs at least $s^{-1}$",
              transform=ax_b.transAxes, fontsize=5.65, fontweight="bold",
              ha="center", va="bottom")

    # Panel C: six-site coefficientwise witness.
    ax_c.set_axis_off()
    ax_c.set_title("C  Six-site zero-mode witness", loc="left", fontweight="bold",
                   y=1.075, pad=0)
    ax_c.text(0.0, 1.01, r"same output coefficient $h=0$ | exact cancellation / survival",
              transform=ax_c.transAxes, fontsize=5.55, color=palette["midGrey"], va="bottom")
    ax_c.text(0.5, 0.895,
              r"$u=(6\sin y-4\sin(x+y),\ 4\sin x+4\sin(x+y),\ 0)$",
              transform=ax_c.transAxes, fontsize=5.55, ha="center", va="center")
    add_box(ax_c, 0.01, 0.47, 0.29, 0.29, palette["paper"], palette["blue"],
            "CONTRACTED FLUX", r"$-\widehat{\partial_k\kappa_{kij}}(0)=0$",
            palette["blueDark"], 5.6)
    add_box(ax_c, 0.355, 0.47, 0.29, 0.29, palette["paper"], palette["midGrey"],
            "PRESSURE DIFFUSION", r"$-\widehat{\partial_iQ_j+\partial_jQ_i}(0)=0$",
            palette["ink"], 5.05)
    add_box(ax_c, 0.70, 0.47, 0.29, 0.29, palette["goldLight"], palette["gold"],
            "PRESSURE STRAIN", "$\\widehat\\Xi(0)=(1-q^4)$\n$\\mathrm{diag}(-48,48,0)$",
            palette["ink"], 5.35)
    ax_c.annotate("", xy=(0.845, 0.36), xytext=(0.845, 0.47), xycoords=ax_c.transAxes,
                  arrowprops={"arrowstyle": "-|>", "color": palette["gold"], "linewidth": 1.0})
    ax_c.text(0.845, 0.29, r"nonzero for $0<s<\infty$",
              transform=ax_c.transAxes, fontsize=5.7, fontweight="bold",
              color=palette["gold"], ha="center", va="center")
    add_box(ax_c, 0.09, 0.03, 0.82, 0.17, palette["paper"], palette["lightGrey"],
            "INTERPRETATION BOUNDARY",
            "coefficientwise witness only — not a whole-field information collision",
            palette["midGrey"], 5.45)

    # Panel D: selected quartic remainder and parabolic dilation.
    curve = [item for item in rows if item["panel"] == "D" and item["series"] == "quarticProfile"]
    x_values = [float(item["x"]) for item in curve]
    y_values = [float(item["y"]) for item in curve]
    ax_d.set_title("D  Selected quartic remainder", loc="left", fontweight="bold",
                   y=1.075, pad=0)
    ax_d.text(0.0, 1.01, r"$\kappa_{112}$ at $(0,2,0)$ | exact formula; line is not a fit",
              transform=ax_d.transAxes, fontsize=5.55, color=palette["midGrey"], va="bottom")
    ax_d.plot(x_values, y_values, color=palette["blue"], linewidth=1.55)
    ax_d.fill_between(x_values, y_values, 0, color=palette["blueLight"], alpha=0.23)
    ax_d.set_xlim(0, float(config["quarticThetaMaximum"]))
    ax_d.set_ylim(0, 0.315)
    ax_d.set_xlabel(r"parabolic parameter $\theta$ in $s=\theta L^{-2}$")
    ax_d.set_ylabel(r"$|\partial_t\widehat\kappa_{112}|/L$")
    ax_d.set_xticks([0.0, 0.5, 1.0, 1.5, 2.0])
    ax_d.set_yticks([0.0, 0.1, 0.2, 0.3])
    ax_d.grid(axis="y", color=palette["lightGrey"], linewidth=0.5)
    ax_d.spines[["top", "right"]].set_visible(False)
    ax_d.text(0.97, 0.95,
              r"$2iq^2(1-q^2)^2$" + "\n" +
              r"$\to\ 2iL e^{-2\theta}(1-e^{-2\theta})^2$",
              transform=ax_d.transAxes, fontsize=5.65, ha="right", va="top",
              bbox={"boxstyle": "round,pad=0.23", "facecolor": palette["paper"],
                    "edgecolor": palette["blue"], "linewidth": 0.75})
    ax_d.text(0.97, 0.51, r"finite-$\varepsilon$ check at $q=1/2$: $9i/32$",
              transform=ax_d.transAxes, fontsize=5.35, ha="right", va="center",
              color=palette["gold"], fontweight="bold",
              bbox={"boxstyle": "round,pad=0.22", "facecolor": palette["goldLight"],
                    "edgecolor": palette["gold"], "linewidth": 0.7})
    ax_d.text(0.02, 0.06, "exact nonzero selected coefficient for θ > 0",
              transform=ax_d.transAxes, fontsize=5.4, fontweight="bold",
              color=palette["blueDark"], ha="left", va="bottom")

    figure.text(0.047, 0.066,
                r"Parabolic lift: $\|\Delta\widehat\chi\|_F=2\sqrt{6}L(e^{-3\theta}-e^{-5\theta})$; selected quartic tangent $=2iLe^{-2\theta}(1-e^{-2\theta})^2$.",
                fontsize=6.25, fontweight="bold", ha="left", va="bottom")
    figure.text(0.047, 0.026,
                "Exact two-path finite Fourier certificate | coefficientwise / selected-coefficient scope | no simulation, fit, closure theorem, or global regularity result | NOT CLAY",
                fontsize=5.55, color=palette["midGrey"], ha="left", va="bottom")

    metadata = {
        "Title": "R0.73V | Pressure-aware signed third-order heat-lift interface",
        "Author": "ChuiKuan Zeng",
        "Subject": "Exact two-path Fourier certificate for pressure-aware third-order heat lift and selected quartic ascent",
        "Keywords": "Navier-Stokes, heat filter, cumulant, pressure strain, Fourier, exact certificate",
        "CreationDate": datetime(2026, 9, 1, tzinfo=timezone.utc),
        "ModDate": datetime(2026, 9, 1, tzinfo=timezone.utc),
    }
    svg_path = output / "figure.svg"
    figure.savefig(svg_path, format="svg", facecolor=palette["paper"],
                   metadata={"Title": metadata["Title"], "Description": metadata["Subject"],
                             "Date": "2026-09-01"})
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text("\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
                        encoding="utf-8")
    figure.savefig(output / "figure.pdf", format="pdf", facecolor=palette["paper"], metadata=metadata)
    figure.savefig(output / "figure.png", format="png", facecolor=palette["paper"],
                   dpi=int(config["pngDpi"]),
                   metadata={"Title": metadata["Title"], "Description": metadata["Subject"],
                             "dpi": str(config["pngDpi"])})
    plt.close(figure)

    from PIL import Image  # type: ignore
    with Image.open(output / "figure.png") as image:
        reduced = image.copy()
        reduced.thumbnail((int(config["qaMaximumWidthPixels"]), 1400))
        reduced.convert("RGB").save(output / "qa-final-size.png")
        reduced.convert("L").save(output / "qa-grayscale.png")

    import pypdfium2 as pdfium  # type: ignore
    document = pdfium.PdfDocument(str(output / "figure.pdf"))
    if len(document) != 1:
        raise RuntimeError("figure PDF is not one page")
    page = document[0]
    page.render(scale=3.0).to_pil().convert("RGB").save(output / "qa-pdf.png")
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
    primary, independent = certificate_pair(contract)
    monitor.event("two-path-certificate-validated", commonCoreEqual=True)
    rows = generate_rows(config, contract, primary, independent)
    if len(rows) != 158:
        raise RuntimeError(f"source-data row count drift: {len(rows)}")
    write_csv(output / "source-data.csv", rows)
    monitor.event("source-data-written", rows=len(rows))
    if not args.data_only:
        render(output, config, rows)
        monitor.event("render-complete", outputs=6)
    cpu_count = os.cpu_count() or 1
    environment = {
        "schemaVersion": "r073v-signed-third-order-interface-environment-v1",
        "createdUtc": utc_now(),
        "execution": {
            "cpu": f"{platform.machine()} / {cpu_count} logical CPUs",
            "dgxUsed": False,
            "gpu": "not used",
            "host": platform.node(),
            "logicalCpuCount": cpu_count,
            "machine": platform.machine(),
            "memoryGiB": memory_gib(),
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
        "schemaVersion": "r073v-signed-third-order-interface-figure-results-v1",
        "allSourceChecksPass": True,
        "certificate": {
            "commonCoreByteIdentical": primary["commonCore"] == independent["commonCore"],
            "commonCoreSha256": contract["certificate"]["commonCoreSha256"],
            "completeTableDigest": primary["commonCore"]["tableDigest"],
            "independentImportsPrimaryProducer": independent["independence"]["importsPrimaryProducer"],
            "primarySha256": contract["certificate"]["primarySha256"],
            "independentSha256": contract["certificate"]["independentSha256"],
        },
        "claimBoundary": contract["claimBoundary"],
        "exactConstants": {
            "compressedChi": "(q^3-q^5)*K",
            "fourSiteKappaOrder": 2,
            "fourSitePressureOrder": 1,
            "sixSitePressureStrain": "(1-q^4)*diag(-48,48,0)",
            "quarticSelected": "2*i*q^2*(1-q^2)^2",
            "quarticFiniteEpsilon": "9/32*i",
            "quarticParabolicDilation": "2*i*L*exp(-2*theta)*(1-exp(-2*theta))^2",
        },
        "figureId": FIGURE_ID,
        "rowCount": len(rows),
        "series": {
            "metadataAndDefinitions": 5,
            "compressedInterfaceEntries": 16,
            "fourSiteEntries": 16,
            "sixSiteEntries": 12,
            "quarticExactAndFiniteRows": 6,
            "analyticRendererSamples": 101,
            "dilationRows": 2,
            "total": len(rows),
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
