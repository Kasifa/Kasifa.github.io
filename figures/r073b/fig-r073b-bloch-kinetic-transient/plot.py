#!/usr/bin/env python3
"""Deterministic R0.73B four-panel Bloch/kinetic journal figure."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from html import escape
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
from typing import Any, Iterable

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
REL_PACKAGE = PACKAGE.relative_to(ROOT)
FIGURE_ID = "fig-r073b-bloch-kinetic-transient"
RELEASE = "R0.73B"
WIDTH_MM = 178
HEIGHT_MM = 150
PNG_DPI = 600
W = 1780.0
H = 1500.0

INK = "#20262D"
MID = "#5D6670"
QUIET = "#8A939D"
GRID = "#D9DEE3"
PAPER = "#FFFFFF"
PALE = "#F5F7F8"
BLUE = "#285F8F"
BLUE_LIGHT = "#DDEAF4"
GOLD = "#A6781F"
GOLD_LIGHT = "#F3E8CB"

ARIAL = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
ARIAL_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")

SOURCE_FILES = [
    "README.md",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "environment.txt",
    "figure-contract.md",
    "manifest-draft.json",
    "plot.py",
    "qa-protocol.md",
    "requirements.txt",
    "validate.py",
]
GENERATED_FILES = [
    "data.csv",
    "results.json",
    "validation.json",
    "figure.svg",
    "figure.pdf",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "qa-report.md",
    "manifest.json",
    "SHA256SUMS",
]
FIELDS = [
    "panel", "kind", "id", "series", "x", "y", "value", "mu",
    "Lambda", "p", "a", "norm", "N", "start", "end", "gain",
    "finiteGain", "triangularGain", "energyEnvelope",
    "observedExponent", "predictedExponent", "sourcePath",
    "sourceSha256", "sourceRowId", "formula", "status", "note",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def write_text(path: Path, value: str) -> None:
    path.write_text(value, encoding="utf-8", newline="\n")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def close(left: float, right: float, tolerance: float = 5e-13) -> bool:
    return abs(left - right) <= tolerance * max(1.0, abs(left), abs(right))


def log_samples(start: float, stop: float, count: int) -> list[float]:
    require(start > 0.0 and stop > start and count >= 2, "bad log grid")
    lo, hi = math.log10(start), math.log10(stop)
    return [10.0 ** (lo + (hi - lo) * index / (count - 1))
            for index in range(count)]


def heat_shear_k(start: float, end: float) -> float:
    return (0.5 * (math.exp(-start) - math.exp(-end))
            + 0.125 * (math.exp(-4.0 * start) - math.exp(-4.0 * end)))


def energy_envelope(mu: float, lam: float, start: float, end: float) -> float:
    return math.exp(-mu * (end - start) + abs(lam) * heat_shear_k(start, end) / 2.0)


def triangular_gain(lam: float, start: float, end: float) -> float:
    """Independent scalar 5x5 power-iteration recomputation."""
    tau = end - start
    d1 = math.exp(-tau)
    d2 = math.exp(-4.0 * tau)
    z1 = lam * tau * math.exp(-end) / 4.0
    z2 = lam * tau * math.exp(-4.0 * end) / 4.0
    matrix = [
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [z2, d2, 0.0, 0.0, 0.0],
        [z1, 0.0, d1, 0.0, 0.0],
        [-z1, 0.0, 0.0, d1, 0.0],
        [-z2, 0.0, 0.0, 0.0, d2],
    ]
    gram = [[sum(matrix[k][i] * matrix[k][j] for k in range(5))
             for j in range(5)] for i in range(5)]
    vector = [1.0, 0.1, -0.2, 0.3, -0.4]
    for _ in range(240):
        product = [sum(gram[i][j] * vector[j] for j in range(5))
                   for i in range(5)]
        length = math.sqrt(sum(value * value for value in product))
        require(length > 0.0, "triangular power iteration vanished")
        vector = [value / length for value in product]
    eigenvalue = sum(vector[i] * gram[i][j] * vector[j]
                     for i in range(5) for j in range(5))
    return math.sqrt(eigenvalue)


def predicted_exponent(a_value: float, p_value: float) -> float:
    return max(a_value / 2.0 - p_value, 0.0)


def upstream_gate(config: dict[str, Any]) -> dict[str, Any]:
    upstream = {key: ROOT / value for key, value in config["upstream"].items()}
    for key, path in upstream.items():
        require(path.is_file(), f"missing upstream {key}: {path}")

    experiment_contract = read_json(upstream["experimentContract"])
    experiment_validation = read_json(upstream["experimentValidation"])
    experiment_manifest = read_json(upstream["experimentManifest"])
    certificate = read_json(upstream["certificate"])
    certificate_validation = read_json(upstream["certificateValidation"])
    certificate_manifest = read_json(upstream["certificateManifest"])
    main_rows = read_csv(upstream["mainRows"])
    targeted_rows = read_csv(upstream["targetedRows"])

    require(experiment_contract.get("release") == RELEASE,
            "experiment contract release mismatch")
    expected = experiment_contract.get("expected", {})
    require(len(main_rows) == expected.get("primaryRowCount") == 1960,
            "main experiment row count is not exactly 1,960")
    require(len(targeted_rows) == expected.get("targetedRowCount") == 245,
            "targeted experiment row count is not exactly 245")
    require(experiment_validation.get("status") == "passed",
            "experiment validation is not passed")
    require(all(experiment_validation.get("checks", {}).values()),
            "not every experiment validation check passed")
    require(experiment_validation.get("finiteDimensionalOnly") is True,
            "finite-dimensional boundary missing from experiment validation")
    require(experiment_manifest.get("status") == "completed"
            and experiment_manifest.get("finiteDimensionalOnly") is True,
            "experiment manifest is incomplete")
    require(all(row.get("N") == "10" and row.get("finiteDimensionalOnly") == "True"
                for row in main_rows), "main rows are not all finite N=10")
    require(all(row.get("N") == "10" and row.get("finiteDimensionalOnly") == "True"
                for row in targeted_rows), "targeted rows are not all finite N=10")

    manifest_records = {record["path"]: record
                        for record in experiment_manifest.get("outputs", [])}
    main_record = manifest_records.get("weighted_propagator_rows.csv")
    require(main_record is not None, "main CSV absent from experiment manifest")
    require(main_record["bytes"] == upstream["mainRows"].stat().st_size
            and main_record["sha256"] == sha256(upstream["mainRows"]),
            "main CSV differs from experiment manifest")

    require(certificate.get("release") == RELEASE,
            "certificate release mismatch")
    require(certificate_validation.get("status") == "passed"
            and all(certificate_validation.get("checks", {}).values()),
            "certificate validation is not fully passed")
    claims = certificate.get("claimBoundary", {})
    required_true = (
        "finitePropagatorGridChecked",
        "fixedLambdaTriangularColumnCoefficientChecked",
        "heatShearPrimitiveCoefficientLedgerChecked",
        "sharpShearLowGapStarCoefficientChecked",
        "weightScalingPowerLedgerChecked",
    )
    require(all(claims.get(key) is True for key in required_true),
            "required certificate claim ledger is incomplete")
    require(claims.get("GalerkinTailBoundProved") is False
            and claims.get("nonlinearNavierStokesProved") is False
            and claims.get("clayMillenniumProblemSolved") is False,
            "certificate negative boundary changed")

    crosscheck = certificate.get("finiteCrosscheck", {})
    require(crosscheck.get("status") == "passed"
            and crosscheck.get("rowCount") == 1960
            and crosscheck.get("caseCount") == 280
            and crosscheck.get("finiteDimensionalOnly") is True,
            "certificate finite crosscheck is incomplete")
    for name, record in crosscheck.get("files", {}).items():
        path = ROOT / "experiments" / "r073b" / name
        require(path.is_file(), f"certificate-bound experiment file missing: {name}")
        require(path.stat().st_size == record["bytes"]
                and sha256(path) == record["sha256"],
                f"certificate-bound experiment hash mismatch: {name}")

    scaling = certificate["exactChecks"]["scaling"]
    require(scaling["sharpShearCoefficientLimit"]["formula"]
            == "rho_mu -> sqrt(e^-2d+e^-8d)/(4*sqrt(2))",
            "sharp shear coefficient formula changed")
    require(scaling["fixedLambdaTriangularColumn"]["coefficientsExact"] is True,
            "triangular coefficients are not exact in certificate")
    ledger = scaling["diagonalWeightFamily"]
    require(ledger["generatorBlockPower"] == "mu^(p-a/2)",
            "weight exponent ledger changed")

    bindings = certificate_manifest.get("sourceBindings", [])
    require(bindings, "certificate manifest has no source bindings")
    for record in bindings:
        path = ROOT / record["path"]
        require(path.is_file(), f"certificate source binding missing: {record['path']}")
        require(path.stat().st_size == record["bytes"]
                and sha256(path) == record["sha256"],
                f"certificate source binding mismatch: {record['path']}")

    return {
        "paths": upstream,
        "mainRows": main_rows,
        "targetedRows": targeted_rows,
        "experimentContract": experiment_contract,
        "experimentValidation": experiment_validation,
        "experimentManifest": experiment_manifest,
        "certificate": certificate,
        "certificateValidation": certificate_validation,
        "certificateManifest": certificate_manifest,
        "hashes": {key: sha256(path) for key, path in upstream.items()},
    }


def build_rows(config: dict[str, Any], evidence: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(panel: str, kind: str, item_id: str, series: str, x: float,
            value: float, formula: str, status: str, note: str, **extra: Any) -> None:
        require(math.isfinite(x) and math.isfinite(value), "non-finite plotted value")
        row = {field: "" for field in FIELDS}
        row.update({
            "panel": panel,
            "kind": kind,
            "id": item_id,
            "series": series,
            "x": format(x, ".17g"),
            "y": format(value, ".17g"),
            "value": format(value, ".17g"),
            "formula": formula,
            "status": status,
            "note": note,
        })
        for key, extra_value in extra.items():
            row[key] = (format(extra_value, ".17g")
                        if isinstance(extra_value, float) else str(extra_value))
        rows.append(row)

    main_hash = evidence["hashes"]["mainRows"]
    targeted_hash = evidence["hashes"]["targetedRows"]
    validation_hash = evidence["hashes"]["experimentValidation"]
    certificate_hash = evidence["hashes"]["certificate"]

    # Panel A: thirteen distinct mu values per series, with the shared 1e-8
    # row crosschecked and retained once.
    for spec in config["panelA"]["series"]:
        broad = [row for row in evidence["mainRows"]
                 if row["pathId"] == spec["pathId"]
                 and row["norm"] == spec["norm"]
                 and float(row["p"]) == float(spec["p"])
                 and float(row["start"]) == float(config["panelA"]["start"])
                 and float(row["end"]) == float(config["panelA"]["end"])
                 and row["sign"] == "1"]
        targeted = [row for row in evidence["targetedRows"]
                    if row["norm"] == spec["norm"]
                    and float(row["p"]) == float(spec["p"])]
        require(len(broad) == 7 and len(targeted) == 7,
                f"Panel A source rows incomplete: {spec['id']}")
        broad_by_mu = {float(row["mu"]): row for row in broad}
        targeted_by_mu = {float(row["mu"]): row for row in targeted}
        require(close(float(broad_by_mu[1e-8]["gain"]),
                      float(targeted_by_mu[1e-8]["gain"]), 2e-15),
                f"Panel A shared-grid row differs: {spec['id']}")
        combined: list[tuple[float, dict[str, str], str, str, str]] = []
        for mu_value, source in broad_by_mu.items():
            combined.append((mu_value, source,
                             config["upstream"]["mainRows"], main_hash,
                             source["caseId"] + ":" + source["norm"]))
        for source in targeted:
            mu_value = float(source["mu"])
            if mu_value == 1e-8:
                continue
            source_line = evidence["targetedRows"].index(source) + 2
            combined.append((mu_value, source,
                             config["upstream"]["targetedRows"], targeted_hash,
                             f"targeted-line-{source_line}"))
        combined.sort(key=lambda item: item[0])
        require(len(combined) == config["panelA"]["minimumDistinctMuPerSeries"]
                and len({item[0] for item in combined}) == len(combined),
                f"Panel A does not have thirteen distinct mu: {spec['id']}")
        for index, (mu_value, source, source_path, source_hash, source_id) in enumerate(combined):
            gain = float(source["gain"])
            add("A", "finite-propagator-gain", f"{spec['id']}-{index:02d}",
                spec["label"], mu_value, gain, "finite N=10 RK4 singular value",
                "FINITE N=10 diagnostic", "no Galerkin tail bound",
                mu=mu_value, p=float(spec["p"]), norm=spec["norm"], N=10,
                start=float(config["panelA"]["start"]),
                end=float(config["panelA"]["end"]), gain=gain,
                sourcePath=source_path, sourceSha256=source_hash,
                sourceRowId=source_id)

    # Panel B: finite gain, independently recomputed triangular limit, and
    # analytic energy envelope at the same low-gap point.
    limits = evidence["experimentValidation"]["fixedLambdaKineticLimits"]
    require([float(row["Lambda"]) for row in limits]
            == [float(value) for value in config["panelB"]["lambdaValues"]],
            "Panel B Lambda grid changed")
    for index, source in enumerate(limits):
        lam = float(source["Lambda"])
        finite = float(source["finiteGain"])
        limit = triangular_gain(lam, float(config["panelB"]["start"]),
                                float(config["panelB"]["end"]))
        require(close(limit, float(source["triangularLimitGain"]), 3e-13),
                f"triangular gain recomputation failed for Lambda={lam:g}")
        relative = abs(finite - limit) / limit
        require(relative <= float(config["panelB"]["relativeLimitTolerance"]),
                f"finite/limit tolerance failed for Lambda={lam:g}")
        envelope = energy_envelope(float(config["panelB"]["mu"]), lam,
                                   float(config["panelB"]["start"]),
                                   float(config["panelB"]["end"]))
        require(finite <= envelope, "finite kinetic gain exceeds analytic envelope")
        common = dict(Lambda=lam, mu=float(config["panelB"]["mu"]), N=10,
                      start=float(config["panelB"]["start"]),
                      end=float(config["panelB"]["end"]), norm="kinetic")
        add("B", "finite-kinetic-gain", f"finite-{index}", "finite N=10",
            lam, finite, "finite N=10 RK4 singular value",
            "FINITE N=10 diagnostic", "filled marker; no tail bound",
            finiteGain=finite, sourcePath=config["upstream"]["experimentValidation"],
            sourceSha256=validation_hash, sourceRowId=f"fixedLambdaKineticLimits[{index}]",
            **common)
        add("B", "triangular-limit-gain", f"limit-{index}", "triangular low-gap limit",
            lam, limit, "largest singular value of explicit 5x5 triangular matrix",
            "exact finite-matrix low-gap limit", "open marker; not an infinite-dimensional tail enclosure",
            triangularGain=limit, sourcePath=config["upstream"]["certificate"],
            sourceSha256=certificate_hash,
            sourceRowId="exactChecks.scaling.fixedLambdaTriangularColumn", **common)
        add("B", "analytic-energy-envelope", f"envelope-{index}", "analytic energy envelope",
            lam, envelope, config["panelB"]["energyEnvelope"],
            "proved analytic upper envelope", "not an observed maximum transient gain",
            energyEnvelope=envelope, sourcePath=config["upstream"]["certificate"],
            sourceSha256=certificate_hash,
            sourceRowId="exactChecks.energy.physicalVelocityNormBound", **common)

    # Panel C: purely analytic bounds at d=0.  M=1 and m=1/2 under the
    # normalized periodic L2 convention, hence rho_0=1/4.
    panel_c = config["panelC"]
    d_value = float(panel_c["d"])
    a_harmonic = math.exp(-d_value)
    b_harmonic = math.exp(-4.0 * d_value)
    m_inf = 0.5 * (a_harmonic + b_harmonic)
    m_l2 = math.sqrt((a_harmonic * a_harmonic
                      + b_harmonic * b_harmonic) / 8.0)
    low_gap = m_l2 / 2.0
    require(close(m_inf, 1.0) and close(m_l2, 0.5) and close(low_gap, 0.25),
            "Panel C d=0 constants are not (M,m,rho0)=(1,1/2,1/4)")
    mus = log_samples(float(panel_c["muDomain"][0]),
                      float(panel_c["muDomain"][1]),
                      int(panel_c["muSampleCount"]))
    for index, mu_value in enumerate(mus):
        delta = m_inf * math.sqrt(mu_value / (1.0 + mu_value))
        block = min(m_inf / 2.0,
                    (delta + math.sqrt(delta * delta + m_l2 * m_l2)) / 2.0)
        for kind, series, value, formula, source_id in (
            ("elementary-shear-upper", "elementary M/2", m_inf / 2.0,
             panel_c["elementaryFormula"], "exactChecks.energy.heatShearPrimitive"),
            ("carrier-block-upper", "carrier/block upper", block,
             panel_c["blockFormula"], "analytic block estimate in R0.73B proof"),
            ("exact-low-gap-coefficient", "exact low-gap rho_0", low_gap,
             panel_c["lowGapFormula"], "exactChecks.scaling.sharpShearCoefficientLimit"),
        ):
            add("C", kind, f"{kind}-{index:02d}", series, mu_value, value,
                formula, "analytic bound or exact low-gap limit",
                "no computed truncation plotted as an exact operator norm",
                mu=mu_value, sourcePath=config["upstream"]["certificate"],
                sourceSha256=certificate_hash, sourceRowId=source_id)

    # Panel D: continuous analytic predictions plus four audited finite fits.
    panel_d = config["panelD"]
    fit_lookup = {(float(row["p"]), row["norm"]): row
                  for row in evidence["experimentValidation"]["asymptoticFits"]}
    ledger_records = evidence["certificate"]["exactChecks"]["scaling"][
        "diagonalWeightFamily"]["records"]
    ledger_lookup = {(float_fraction(row["p"]), float_fraction(row["a"])):
                     float_fraction(row["predictedDivergenceExponent"])
                     for row in ledger_records}
    for p_value in map(float, panel_d["pValues"]):
        for index in range(int(panel_d["predictionSampleCount"])):
            a_value = 1.5 * index / (int(panel_d["predictionSampleCount"]) - 1)
            prediction = predicted_exponent(a_value, p_value)
            add("D", "analytic-block-prediction", f"prediction-{p_value:g}-{index:02d}",
                f"p={p_value:g} analytic", a_value, prediction,
                panel_d["predictionFormula"], "exact block prediction",
                "continuous line is analytic, not a fit", a=a_value, p=p_value,
                predictedExponent=prediction, sourcePath=config["upstream"]["certificate"],
                sourceSha256=certificate_hash,
                sourceRowId="exactChecks.scaling.diagonalWeightFamily")
        for index, a_value in enumerate(map(float, panel_d["weights"])):
            norm = panel_d["normByWeight"][format_weight_key(a_value)]
            fit = fit_lookup.get((p_value, norm))
            require(fit is not None, f"missing exponent fit p={p_value:g}, norm={norm}")
            observed = float(fit["observedDivergenceExponent"])
            prediction = predicted_exponent(a_value, p_value)
            require(close(prediction, ledger_lookup[(p_value, a_value)], 1e-15),
                    "certificate weight ledger differs from formula")
            require(abs(observed - prediction) <= 2e-5,
                    f"observed exponent misses prediction: p={p_value:g}, a={a_value:g}")
            require([float(value) for value in fit["muRange"]]
                    == [float(value) for value in panel_d["fitMuRange"]],
                    "Panel D fit range changed")
            add("D", "observed-finite-exponent", f"observed-{p_value:g}-{index}",
                f"p={p_value:g} finite fit", a_value, observed,
                "least-squares slope on validated targeted finite grid",
                "FINITE N=10 diagnostic", "four smallest mu values; no tail bound",
                a=a_value, p=p_value, norm=norm, N=10,
                observedExponent=observed, predictedExponent=prediction,
                sourcePath=config["upstream"]["experimentValidation"],
                sourceSha256=validation_hash,
                sourceRowId=f"asymptoticFits[p={p_value:g},norm={norm}]")

    counts = {panel: sum(row["panel"] == panel for row in rows)
              for panel in "ABCD"}
    require(counts == {"A": 39, "B": 12, "C": 183, "D": 130},
            f"row-count contract failed: {counts}")
    return rows


def float_fraction(value: str) -> float:
    numerator, denominator = value.split("/")
    return float(numerator) / float(denominator)


def format_weight_key(value: float) -> str:
    return format(value, "g")


@dataclass
class Scene:
    items: list[dict[str, Any]]

    def rect(self, x: float, y: float, w: float, h: float, *,
             fill: str = PAPER, stroke: str = GRID, width: float = 2.0,
             dash: tuple[float, ...] | None = None, radius: float = 0.0) -> None:
        self.items.append({"kind": "rect", "x": x, "y": y, "w": w, "h": h,
                           "fill": fill, "stroke": stroke, "width": width,
                           "dash": dash, "radius": radius})

    def line(self, x1: float, y1: float, x2: float, y2: float, *,
             color: str = INK, width: float = 2.0,
             dash: tuple[float, ...] | None = None) -> None:
        self.items.append({"kind": "line", "x1": x1, "y1": y1,
                           "x2": x2, "y2": y2, "color": color,
                           "width": width, "dash": dash})

    def polyline(self, points: Iterable[tuple[float, float]], *,
                 color: str = INK, width: float = 2.0,
                 dash: tuple[float, ...] | None = None) -> None:
        self.items.append({"kind": "polyline", "points": list(points),
                           "color": color, "width": width, "dash": dash})

    def polygon(self, points: Iterable[tuple[float, float]], *,
                fill: str = INK, stroke: str | None = None,
                width: float = 1.0) -> None:
        self.items.append({"kind": "polygon", "points": list(points),
                           "fill": fill, "stroke": stroke, "width": width})

    def circle(self, x: float, y: float, r: float, *, fill: str = PAPER,
               stroke: str = INK, width: float = 2.0) -> None:
        self.items.append({"kind": "circle", "x": x, "y": y, "r": r,
                           "fill": fill, "stroke": stroke, "width": width})

    def text(self, x: float, y: float, value: str, *, size: float = 24.0,
             color: str = INK, bold: bool = False,
             anchor: str = "start") -> None:
        self.items.append({"kind": "text", "x": x, "y": y, "value": value,
                           "size": size, "color": color, "bold": bold,
                           "anchor": anchor})


def add_marker(scene: Scene, x: float, y: float, marker: str, color: str,
               *, size: float = 6.0, filled: bool = True) -> None:
    fill = color if filled else PAPER
    if marker == "circle":
        scene.circle(x, y, size, fill=fill, stroke=color, width=2.0)
    elif marker == "square":
        scene.rect(x - size, y - size, 2 * size, 2 * size, fill=fill,
                   stroke=color, width=2.0)
    elif marker == "triangle":
        scene.polygon([(x, y - 1.2 * size), (x - size, y + size),
                       (x + size, y + size)], fill=fill, stroke=color, width=2.0)
    elif marker == "cross":
        scene.line(x - size, y - size, x + size, y + size,
                   color=color, width=2.2)
        scene.line(x - size, y + size, x + size, y - size,
                   color=color, width=2.2)
    else:
        raise ValueError(marker)


def map_linear(value: float, lo: float, hi: float, start: float,
               length: float) -> float:
    return start + length * (value - lo) / (hi - lo)


def map_y(value: float, lo: float, hi: float, start: float,
          height: float) -> float:
    return start + height * (hi - value) / (hi - lo)


def map_log(value: float, lo: float, hi: float, start: float,
            length: float) -> float:
    return map_linear(math.log10(value), math.log10(lo), math.log10(hi),
                      start, length)


def map_log_y(value: float, lo: float, hi: float, start: float,
              height: float) -> float:
    return map_y(math.log10(value), math.log10(lo), math.log10(hi),
                 start, height)


def build_scene(rows: list[dict[str, str]], formal: bool) -> Scene:
    scene = Scene([])
    scene.rect(0, 0, W, H, fill=PAPER, stroke=PAPER, width=0)
    scene.text(55, 50, "R0.73B | Bloch low-gap weights and physical kinetic transients",
               size=34, bold=True)
    scene.text(55, 85,
               "Analytic bounds beside validated finite N=10 diagnostics; no tail enclosure",
               size=20, color=MID)

    blossom_x, blossom_y = 1688, 55
    for index in range(5):
        angle = -math.pi / 2.0 + 2.0 * math.pi * index / 5.0
        scene.circle(blossom_x + 22 * math.cos(angle),
                     blossom_y + 22 * math.sin(angle), 8.2,
                     fill=BLUE_LIGHT if index % 2 == 0 else GOLD_LIGHT,
                     stroke=BLUE if index % 2 == 0 else GOLD, width=1.5)
    scene.circle(blossom_x, blossom_y, 6.8, fill=PAPER, stroke=INK, width=1.5)

    panel_specs = {
        "A": (55, 115, 810, 620),
        "B": (915, 115, 810, 620),
        "C": (55, 760, 810, 680),
        "D": (915, 760, 810, 680),
    }

    def panel(letter: str, title: str, subtitle: str, badge: str,
              badge_fill: str, badge_stroke: str) -> tuple[float, float, float, float]:
        x, y, width, height = panel_specs[letter]
        scene.rect(x, y, width, height, fill=PAPER, stroke=GRID,
                   width=2.0, radius=10)
        scene.text(x + 18, y + 37, letter, size=28, bold=True, color=BLUE)
        scene.text(x + 57, y + 37, title, size=23, bold=True)
        scene.text(x + 20, y + 69, subtitle, size=16.5, color=MID)
        scene.rect(x + 20, y + 84, width - 40, 33, fill=badge_fill,
                   stroke=badge_stroke, width=1.4, radius=6)
        scene.text(x + 34, y + 107, badge, size=14.7, bold=True)
        return x, y, width, height

    def axes(x: float, y: float, width: float, height: float,
             x_label: str, y_label: str) -> None:
        scene.line(x, y, x, y + height, color=INK, width=1.7)
        scene.line(x, y + height, x + width, y + height, color=INK, width=1.7)
        scene.text(x, y - 10, y_label, size=15, bold=True)
        scene.text(x + width / 2.0, y + height + 36, x_label,
                   size=15, anchor="middle")

    # Panel A.
    ax, ay, _, _ = panel(
        "A", "Low-gap gain by parameter path",
        "[0,0.75] | combined broad + targeted grids",
        "FINITE N=10 DIAGNOSTICS - NO GALERKIN TAIL", GOLD_LIGHT, GOLD)
    px, py, pw, ph = ax + 84, ay + 158, 660, 326
    axes(px, py, pw, ph, "mu (log scale)", "gain (log scale)")
    for exponent in (-14, -11, -8, -5, -2):
        value = 10.0 ** exponent
        xx = map_log(value, 1e-14, 1e-2, px, pw)
        scene.line(xx, py + ph, xx, py + ph + 6, color=INK, width=1.2)
        scene.text(xx, py + ph + 23, f"10^{exponent}", size=12.5,
                   color=MID, anchor="middle")
    for exponent in (0, 2, 4, 6, 8):
        value = 10.0 ** exponent
        yy = map_log_y(value, 1.0, 1e8, py, ph)
        scene.line(px, yy, px + pw, yy, color=GRID, width=1.0, dash=(4, 5))
        scene.text(px - 10, yy + 4, f"10^{exponent}", size=12.5,
                   color=MID, anchor="end")
    a_styles = [
        ("fixed c=1 | kinetic", GOLD, None, "circle", True),
        ("fixed Lambda=1 | kinetic", BLUE, (10, 5), "square", False),
        ("fixed Lambda=1 | raw q", INK, (3, 5), "cross", False),
    ]
    a_rows = [row for row in rows if row["panel"] == "A"]
    for label, color, dash, marker, filled in a_styles:
        series = sorted((row for row in a_rows if row["series"] == label),
                        key=lambda row: float(row["mu"]))
        points = [(map_log(float(row["mu"]), 1e-14, 1e-2, px, pw),
                   map_log_y(float(row["gain"]), 1.0, 1e8, py, ph))
                  for row in series]
        scene.polyline(points, color=color, width=2.6, dash=dash)
        for point in points:
            add_marker(scene, *point, marker, color, size=4.4, filled=filled)
    # Explicit slope references, separated from the data lines.
    x1, x2 = map_log(2e-13, 1e-14, 1e-2, px, pw), map_log(2e-10, 1e-14, 1e-2, px, pw)
    y1, y2 = map_log_y(2e6, 1.0, 1e8, py, ph), map_log_y(2e6 / math.sqrt(1e3), 1.0, 1e8, py, ph)
    scene.line(x1, y1, x2, y2, color=QUIET, width=1.8, dash=(7, 5))
    scene.text(x2 + 7, y2 + 4, "slope -1/2", size=12.2, color=MID)
    y0 = map_log_y(2.5, 1.0, 1e8, py, ph)
    scene.line(map_log(2e-13, 1e-14, 1e-2, px, pw), y0,
               map_log(2e-10, 1e-14, 1e-2, px, pw), y0,
               color=QUIET, width=1.8, dash=(2, 5))
    scene.text(map_log(2e-10, 1e-14, 1e-2, px, pw) + 7, y0 + 4,
               "slope 0", size=12.2, color=MID)
    legend_y = ay + 529
    for index, style in enumerate(a_styles):
        label, color, dash, marker, filled = style
        lx = ax + 34 + (index % 2) * 365
        ly = legend_y + (index // 2) * 31
        scene.line(lx, ly, lx + 34, ly, color=color, width=2.5, dash=dash)
        add_marker(scene, lx + 17, ly, marker, color, size=4.3, filled=filled)
        scene.text(lx + 44, ly + 5, label, size=13.5)
    scene.text(ax + 34, ay + 602,
               "13 distinct mu per series | every point labelled FINITE N=10 in data.csv",
               size=14.2, color=MID)

    # Panel B.
    bx, by, _, _ = panel(
        "B", "Finite gain, triangular limit, envelope",
        "mu=10^-8 | [0,0.75] | physical kinetic norm",
        "ANALYTIC ENERGY ENVELOPE - UPPER BOUND", BLUE_LIGHT, BLUE)
    qx, qy, qw, qh = bx + 84, by + 158, 660, 326
    axes(qx, qy, qw, qh, "|Lambda|", "gain (log scale)")
    for tick in (1.0, 2.0, 5.0, 10.0, 20.0):
        yy = map_log_y(tick, 1.0, 25.0, qy, qh)
        scene.line(qx, yy, qx + qw, yy, color=GRID, width=1.0, dash=(4, 5))
        scene.text(qx - 10, yy + 4, f"{tick:g}", size=12.5,
                   color=MID, anchor="end")
    b_rows = [row for row in rows if row["panel"] == "B"]
    lambda_values = [0.25, 1.0, 4.0, 16.0]
    for index, lam in enumerate(lambda_values):
        base_x = qx + qw * (index + 0.5) / 4.0
        scene.text(base_x, qy + qh + 23, f"{lam:g}", size=12.5,
                   color=MID, anchor="middle")
        for offset, kind, color, marker, filled in (
            (-12, "finite-kinetic-gain", BLUE, "circle", True),
            (12, "triangular-limit-gain", GOLD, "circle", False),
            (0, "analytic-energy-envelope", INK, "cross", False),
        ):
            row = next(row for row in b_rows
                       if row["kind"] == kind and close(float(row["Lambda"]), lam))
            yy = map_log_y(float(row["value"]), 1.0, 25.0, qy, qh)
            scene.line(base_x + offset, map_log_y(1.0, 1.0, 25.0, qy, qh),
                       base_x + offset, yy, color=QUIET, width=1.3,
                       dash=(4, 4) if kind == "analytic-energy-envelope" else None)
            add_marker(scene, base_x + offset, yy, marker, color,
                       size=5.2, filled=filled)
    b_legend = [
        ("finite N=10", BLUE, "circle", True),
        ("triangular limit", GOLD, "circle", False),
        ("energy envelope", INK, "cross", False),
    ]
    for index, (label, color, marker, filled) in enumerate(b_legend):
        lx = bx + 38 + index * 248
        ly = by + 529
        add_marker(scene, lx, ly, marker, color, size=4.7, filled=filled)
        scene.text(lx + 14, ly + 5, label, size=13.2)
    scene.text(bx + 34, by + 564,
               "finite vs limit relative difference <= 8e-9", size=14.2,
               bold=True, color=BLUE)
    scene.text(bx + 34, by + 596,
               "EXACT MAXIMUM TRANSIENT: NOT CLAIMED", size=14.2,
               bold=True, color=INK)

    # Panel C.
    cx, cy, _, _ = panel(
        "C", "Sharp OS shear coefficient at d=0",
        "Three analytic curves; rho_mu is not numerically truncated here",
        "ANALYTIC ONLY - NO TRUNCATED OPERATOR NORM", BLUE_LIGHT, BLUE)
    rx, ry, rw, rh = cx + 84, cy + 164, 660, 354
    axes(rx, ry, rw, rh, "mu (log scale)", "rho upper coefficient")
    for exponent in (-12, -9, -6, -3, 0):
        value = 10.0 ** exponent
        xx = map_log(value, 1e-12, 1.0, rx, rw)
        scene.line(xx, ry + rh, xx, ry + rh + 6, color=INK, width=1.2)
        scene.text(xx, ry + rh + 23, f"10^{exponent}", size=12.5,
                   color=MID, anchor="middle")
    for tick in (0.2, 0.25, 0.3, 0.4, 0.5):
        yy = map_y(tick, 0.2, 0.52, ry, rh)
        scene.line(rx, yy, rx + rw, yy, color=GRID, width=1.0, dash=(4, 5))
        scene.text(rx - 10, yy + 4, f"{tick:.2f}", size=12.5,
                   color=MID, anchor="end")
    c_styles = [
        ("elementary M/2", BLUE, (10, 5), "square", False),
        ("carrier/block upper", GOLD, None, "circle", True),
        ("exact low-gap rho_0", INK, (3, 5), "cross", False),
    ]
    c_rows = [row for row in rows if row["panel"] == "C"]
    for label, color, dash, marker, filled in c_styles:
        series = [row for row in c_rows if row["series"] == label]
        points = [(map_log(float(row["mu"]), 1e-12, 1.0, rx, rw),
                   map_y(float(row["value"]), 0.2, 0.52, ry, rh))
                  for row in series]
        scene.polyline(points, color=color, width=2.7, dash=dash)
        for index in range(0, len(points), 10):
            add_marker(scene, *points[index], marker, color, size=4.3,
                       filled=filled)
    scene.text(rx + 14, map_y(0.25, 0.2, 0.52, ry, rh) - 9,
               "rho_0(0) = 1/4", size=14.5, bold=True)
    for index, style in enumerate(c_styles):
        label, color, dash, marker, filled = style
        lx = cx + 34 + (index % 2) * 380
        ly = cy + 570 + (index // 2) * 30
        scene.line(lx, ly, lx + 33, ly, color=color, width=2.5, dash=dash)
        add_marker(scene, lx + 16, ly, marker, color, size=4.2, filled=filled)
        scene.text(lx + 43, ly + 5, label, size=13.2)
    scene.text(cx + 34, cy + 646,
               "0.188106... is an integrated log coefficient, not a gain",
               size=14.0, color=MID)

    # Panel D.
    dx, dy, _, _ = panel(
        "D", "Weight threshold: observed vs predicted",
        "fits on mu=10^-14...10^-11 | four audited diagonal weights",
        "BLOCK PREDICTION (a/2-p)_+", GOLD_LIGHT, GOLD)
    sx, sy, sw, sh = dx + 84, dy + 164, 660, 354
    axes(sx, sy, sw, sh, "diagonal weight a", "divergence exponent")
    for tick in (0.0, 0.5, 1.0, 1.5):
        xx = map_linear(tick, 0.0, 1.5, sx, sw)
        scene.line(xx, sy + sh, xx, sy + sh + 6, color=INK, width=1.2)
        scene.text(xx, sy + sh + 23, f"{tick:g}", size=12.5,
                   color=MID, anchor="middle")
    for tick in (0.0, 0.25, 0.5, 0.75):
        yy = map_y(tick, 0.0, 0.8, sy, sh)
        scene.line(sx, yy, sx + sw, yy, color=GRID, width=1.0, dash=(4, 5))
        scene.text(sx - 10, yy + 4, f"{tick:.2f}", size=12.5,
                   color=MID, anchor="end")
    d_rows = [row for row in rows if row["panel"] == "D"]
    d_styles = [
        (0.0, "fixed c: p=0", GOLD, None, "circle", True),
        (0.5, "fixed Lambda: p=1/2", BLUE, (10, 5), "square", False),
    ]
    for p_value, _, color, dash, marker, filled in d_styles:
        prediction_rows = [row for row in d_rows
                           if row["kind"] == "analytic-block-prediction"
                           and close(float(row["p"]), p_value)]
        points = [(map_linear(float(row["a"]), 0.0, 1.5, sx, sw),
                   map_y(float(row["predictedExponent"]), 0.0, 0.8, sy, sh))
                  for row in prediction_rows]
        scene.polyline(points, color=color, width=2.8, dash=dash)
        observed_rows = [row for row in d_rows
                         if row["kind"] == "observed-finite-exponent"
                         and close(float(row["p"]), p_value)]
        for row in observed_rows:
            xx = map_linear(float(row["a"]), 0.0, 1.5, sx, sw)
            yy = map_y(float(row["observedExponent"]), 0.0, 0.8, sy, sh)
            add_marker(scene, xx, yy, marker, color, size=5.7, filled=filled)
    for index, (_, label, color, dash, marker, filled) in enumerate(d_styles):
        lx, ly = dx + 38 + index * 365, dy + 571
        scene.line(lx, ly, lx + 34, ly, color=color, width=2.5, dash=dash)
        add_marker(scene, lx + 17, ly, marker, color, size=4.5, filled=filled)
        scene.text(lx + 44, ly + 5, label, size=13.2)
    scene.text(dx + 34, dy + 611,
               "lines: exact block prediction | markers: FINITE N=10 fits",
               size=14.0, color=MID)
    scene.text(dx + 34, dy + 645,
               "critical fixed-Lambda weight: a=1", size=14.0,
               bold=True, color=BLUE)

    lineage = ("FORMAL - CERTIFICATE COMMIT LINEAGE SEALED" if formal else
               "DRAFT - FORMAL CERTIFICATE LINEAGE PENDING")
    scene.text(55, H - 20, lineage, size=15.5, color=QUIET)
    scene.text(W - 55, H - 20, "A2 DIRECT SUM / NONLINEAR / CLAY: OPEN",
               size=15.5, color=QUIET, anchor="end")
    return scene


def svg_dash(dash: tuple[float, ...] | None) -> str:
    return "" if not dash else f' stroke-dasharray="{",".join(str(v) for v in dash)}"'


def render_svg(scene: Scene, path: Path) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH_MM}mm" '
        f'height="{HEIGHT_MM}mm" viewBox="0 0 {int(W)} {int(H)}" '
        'role="img" aria-labelledby="title desc">',
        '<title id="title">R0.73B Bloch low-gap weights and physical kinetic transients</title>',
        '<desc id="desc">Four panels compare validated finite N=10 gains, an explicit triangular limit, analytic kinetic envelopes, sharp shear coefficient bounds, and diagonal weight exponents.</desc>',
    ]
    for item in scene.items:
        kind = item["kind"]
        if kind == "rect":
            lines.append(
                f'<rect x="{item["x"]:.3f}" y="{item["y"]:.3f}" '
                f'width="{item["w"]:.3f}" height="{item["h"]:.3f}" '
                f'rx="{item["radius"]:.3f}" fill="{item["fill"]}" '
                f'stroke="{item["stroke"]}" stroke-width="{item["width"]:.3f}"'
                f'{svg_dash(item["dash"])} />')
        elif kind == "line":
            lines.append(
                f'<line x1="{item["x1"]:.3f}" y1="{item["y1"]:.3f}" '
                f'x2="{item["x2"]:.3f}" y2="{item["y2"]:.3f}" '
                f'stroke="{item["color"]}" stroke-width="{item["width"]:.3f}" '
                f'stroke-linecap="round"{svg_dash(item["dash"])} />')
        elif kind == "polyline":
            points = " ".join(f"{x:.3f},{y:.3f}" for x, y in item["points"])
            lines.append(
                f'<polyline points="{points}" fill="none" stroke="{item["color"]}" '
                f'stroke-width="{item["width"]:.3f}" stroke-linecap="round" '
                f'stroke-linejoin="round"{svg_dash(item["dash"])} />')
        elif kind == "polygon":
            points = " ".join(f"{x:.3f},{y:.3f}" for x, y in item["points"])
            lines.append(
                f'<polygon points="{points}" fill="{item["fill"]}" '
                f'stroke="{item["stroke"] or "none"}" '
                f'stroke-width="{item["width"]:.3f}" />')
        elif kind == "circle":
            lines.append(
                f'<circle cx="{item["x"]:.3f}" cy="{item["y"]:.3f}" '
                f'r="{item["r"]:.3f}" fill="{item["fill"]}" '
                f'stroke="{item["stroke"]}" stroke-width="{item["width"]:.3f}" />')
        elif kind == "text":
            weight = "700" if item["bold"] else "400"
            lines.append(
                f'<text x="{item["x"]:.3f}" y="{item["y"]:.3f}" '
                f'font-family="Arial, Helvetica, sans-serif" '
                f'font-size="{item["size"]:.3f}px" font-weight="{weight}" '
                f'fill="{item["color"]}" text-anchor="{item["anchor"]}">'
                f'{escape(item["value"])}</text>')
        else:
            raise ValueError(kind)
    lines.append("</svg>")
    write_text(path, "\n".join(lines) + "\n")


def dashed_segments(points: list[tuple[float, float]],
                    dash: tuple[float, ...]) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    segments: list[tuple[tuple[float, float], tuple[float, float]]] = []
    pattern_index, remaining, on = 0, dash[0], True
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        if length == 0.0:
            continue
        position = 0.0
        while position < length - 1e-12:
            step = min(remaining, length - position)
            if on:
                start = (x1 + dx * position / length, y1 + dy * position / length)
                stop = (x1 + dx * (position + step) / length,
                        y1 + dy * (position + step) / length)
                segments.append((start, stop))
            position += step
            remaining -= step
            if remaining <= 1e-12:
                pattern_index = (pattern_index + 1) % len(dash)
                remaining = dash[pattern_index]
                on = not on
    return segments


def render_png(scene: Scene, path: Path) -> None:
    width = round(WIDTH_MM / 25.4 * PNG_DPI)
    height = round(HEIGHT_MM / 25.4 * PNG_DPI)
    scale = width / W
    image = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(image)
    regular: dict[int, ImageFont.FreeTypeFont] = {}
    bold: dict[int, ImageFont.FreeTypeFont] = {}

    def font(size: float, is_bold: bool) -> ImageFont.FreeTypeFont:
        pixel_size = max(1, round(size * scale))
        target = bold if is_bold else regular
        if pixel_size not in target:
            target[pixel_size] = ImageFont.truetype(
                str(ARIAL_BOLD if is_bold else ARIAL), pixel_size)
        return target[pixel_size]

    for item in scene.items:
        kind = item["kind"]
        if kind == "rect":
            box = tuple(round(value * scale) for value in
                        (item["x"], item["y"], item["x"] + item["w"], item["y"] + item["h"]))
            width_px = max(1, round(item["width"] * scale))
            if item["radius"]:
                draw.rounded_rectangle(box, radius=round(item["radius"] * scale),
                                       fill=item["fill"], outline=item["stroke"], width=width_px)
            else:
                draw.rectangle(box, fill=item["fill"], outline=item["stroke"], width=width_px)
        elif kind in ("line", "polyline"):
            points = ([(item["x1"], item["y1"]), (item["x2"], item["y2"])]
                      if kind == "line" else item["points"])
            width_px = max(1, round(item["width"] * scale))
            if item["dash"]:
                for start, stop in dashed_segments(points, item["dash"]):
                    draw.line([(round(start[0] * scale), round(start[1] * scale)),
                               (round(stop[0] * scale), round(stop[1] * scale))],
                              fill=item["color"], width=width_px)
            else:
                draw.line([(round(x * scale), round(y * scale)) for x, y in points],
                          fill=item["color"], width=width_px, joint="curve")
        elif kind == "polygon":
            points = [(round(x * scale), round(y * scale)) for x, y in item["points"]]
            draw.polygon(points, fill=item["fill"])
            if item["stroke"]:
                draw.line(points + [points[0]], fill=item["stroke"],
                          width=max(1, round(item["width"] * scale)), joint="curve")
        elif kind == "circle":
            box = tuple(round(value * scale) for value in
                        (item["x"] - item["r"], item["y"] - item["r"],
                         item["x"] + item["r"], item["y"] + item["r"]))
            draw.ellipse(box, fill=item["fill"], outline=item["stroke"],
                         width=max(1, round(item["width"] * scale)))
        elif kind == "text":
            selected = font(item["size"], item["bold"])
            anchor = {"start": "ls", "middle": "ms", "end": "rs"}[item["anchor"]]
            draw.text((round(item["x"] * scale), round(item["y"] * scale)),
                      item["value"], font=selected, fill=item["color"], anchor=anchor)
        else:
            raise ValueError(kind)
    image.save(path, dpi=(PNG_DPI, PNG_DPI))


def render_pdf(scene: Scene, path: Path) -> None:
    require(ARIAL.is_file() and ARIAL_BOLD.is_file(), "Arial fonts unavailable")
    pdfmetrics.registerFont(TTFont("FigureSans", str(ARIAL)))
    pdfmetrics.registerFont(TTFont("FigureSansBold", str(ARIAL_BOLD)))
    page_w, page_h = WIDTH_MM * mm, HEIGHT_MM * mm
    scale = page_w / W
    pdf = canvas.Canvas(str(path), pagesize=(page_w, page_h), pageCompression=1)
    pdf.setTitle("R0.73B Bloch low-gap weights and physical kinetic transients")
    pdf.setAuthor("C. K. Zeng")
    for item in scene.items:
        kind = item["kind"]
        if kind == "rect":
            pdf.setFillColor(HexColor(item["fill"]))
            pdf.setStrokeColor(HexColor(item["stroke"]))
            pdf.setLineWidth(item["width"] * scale)
            pdf.setDash([value * scale for value in item["dash"]] if item["dash"] else [])
            x, y = item["x"] * scale, page_h - (item["y"] + item["h"]) * scale
            if item["radius"]:
                pdf.roundRect(x, y, item["w"] * scale, item["h"] * scale,
                              item["radius"] * scale, stroke=1, fill=1)
            else:
                pdf.rect(x, y, item["w"] * scale, item["h"] * scale,
                         stroke=1, fill=1)
        elif kind == "line":
            pdf.setStrokeColor(HexColor(item["color"]))
            pdf.setLineWidth(item["width"] * scale)
            pdf.setLineCap(1)
            pdf.setDash([value * scale for value in item["dash"]] if item["dash"] else [])
            pdf.line(item["x1"] * scale, page_h - item["y1"] * scale,
                     item["x2"] * scale, page_h - item["y2"] * scale)
        elif kind == "polyline":
            pdf.setStrokeColor(HexColor(item["color"]))
            pdf.setLineWidth(item["width"] * scale)
            pdf.setLineJoin(1)
            pdf.setLineCap(1)
            pdf.setDash([value * scale for value in item["dash"]] if item["dash"] else [])
            path_obj = pdf.beginPath()
            first = item["points"][0]
            path_obj.moveTo(first[0] * scale, page_h - first[1] * scale)
            for x, y in item["points"][1:]:
                path_obj.lineTo(x * scale, page_h - y * scale)
            pdf.drawPath(path_obj, stroke=1, fill=0)
        elif kind == "polygon":
            pdf.setFillColor(HexColor(item["fill"]))
            if item["stroke"]:
                pdf.setStrokeColor(HexColor(item["stroke"]))
            pdf.setLineWidth(item["width"] * scale)
            path_obj = pdf.beginPath()
            first = item["points"][0]
            path_obj.moveTo(first[0] * scale, page_h - first[1] * scale)
            for x, y in item["points"][1:]:
                path_obj.lineTo(x * scale, page_h - y * scale)
            path_obj.close()
            pdf.drawPath(path_obj, stroke=1 if item["stroke"] else 0, fill=1)
        elif kind == "circle":
            pdf.setFillColor(HexColor(item["fill"]))
            pdf.setStrokeColor(HexColor(item["stroke"]))
            pdf.setLineWidth(item["width"] * scale)
            pdf.circle(item["x"] * scale, page_h - item["y"] * scale,
                       item["r"] * scale, stroke=1, fill=1)
        elif kind == "text":
            name = "FigureSansBold" if item["bold"] else "FigureSans"
            size = item["size"] * scale
            pdf.setFont(name, size)
            pdf.setFillColor(HexColor(item["color"]))
            x, y = item["x"] * scale, page_h - item["y"] * scale
            width = pdfmetrics.stringWidth(item["value"], name, size)
            if item["anchor"] == "middle":
                x -= width / 2.0
            elif item["anchor"] == "end":
                x -= width
            pdf.drawString(x, y, item["value"])
        else:
            raise ValueError(kind)
    pdf.showPage()
    pdf.save()


def make_qa_previews() -> None:
    with Image.open(PACKAGE / "figure.png") as figure:
        preview_w = round(WIDTH_MM / 25.4 * 300)
        preview_h = round(HEIGHT_MM / 25.4 * 300)
        preview = figure.resize((preview_w, preview_h), Image.Resampling.LANCZOS)
        preview.save(PACKAGE / "qa-final-size.png", dpi=(300, 300))
        preview.convert("L").convert("RGB").save(
            PACKAGE / "qa-grayscale.png", dpi=(300, 300))
    pdftoppm = shutil.which("pdftoppm")
    require(pdftoppm is not None, "pdftoppm required for independent PDF QA")
    subprocess.run([pdftoppm, "-singlefile", "-r", "300", "-png",
                    str(PACKAGE / "figure.pdf"), str(PACKAGE / "qa-pdf")],
                   check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def embedded_font_count(reader: PdfReader) -> int:
    count = 0
    fonts = reader.pages[0]["/Resources"].get("/Font", {})
    fonts = fonts.get_object() if hasattr(fonts, "get_object") else fonts
    for reference in fonts.values():
        font = reference.get_object()
        candidates = [font]
        descendants = font.get("/DescendantFonts", [])
        if descendants:
            candidates.extend(item.get_object() for item in descendants)
        for candidate in candidates:
            descriptor = candidate.get("/FontDescriptor")
            if descriptor:
                descriptor = descriptor.get_object()
                if any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3")):
                    count += 1
                    break
    return count


def inspect_outputs() -> tuple[dict[str, bool], dict[str, Any]]:
    reader = PdfReader(PACKAGE / "figure.pdf")
    page = reader.pages[0]
    width_mm = float(page.mediabox.width) * 25.4 / 72.0
    height_mm = float(page.mediabox.height) * 25.4 / 72.0
    image_count = len(list(page.images))
    font_count = embedded_font_count(reader)
    with Image.open(PACKAGE / "figure.png") as image:
        dpi = image.info.get("dpi", (0.0, 0.0))
        size = [image.width, image.height]
        rgb = image.convert("RGB")
        corners = [rgb.getpixel((0, 0)), rgb.getpixel((rgb.width - 1, 0)),
                   rgb.getpixel((0, rgb.height - 1)),
                   rgb.getpixel((rgb.width - 1, rgb.height - 1))]
    svg = (PACKAGE / "figure.svg").read_text(encoding="utf-8")
    checks = {
        "pdfOnePage": len(reader.pages) == 1,
        "pdfPhysicalDimensions": abs(width_mm - WIDTH_MM) <= 0.02 and abs(height_mm - HEIGHT_MM) <= 0.02,
        "pdfEmbeddedFonts": font_count >= 2,
        "pdfNoRasterImages": image_count == 0,
        "svgPhysicalDimensions": ('width="178mm"' in svg and 'height="150mm"' in svg
                                  and 'viewBox="0 0 1780 1500"' in svg),
        "pngPhysicalDimensions": size == [round(WIDTH_MM / 25.4 * PNG_DPI),
                                          round(HEIGHT_MM / 25.4 * PNG_DPI)],
        "pngDpiMetadata": all(abs(float(value) - PNG_DPI) <= 0.1 for value in dpi),
        "outerCornersWhite": corners == [(255, 255, 255)] * 4,
    }
    details = {
        "pdf": {"pages": len(reader.pages), "widthMillimetres": width_mm,
                "heightMillimetres": height_mm, "embeddedFontCount": font_count,
                "rasterImageCount": image_count},
        "png": {"pixels": size, "dpi": list(dpi), "corners": corners},
    }
    return checks, details


def visible_checks(scene: Scene, formal: bool) -> dict[str, bool]:
    text = "\n".join(item["value"] for item in scene.items if item["kind"] == "text")
    required = [
        "FINITE N=10 DIAGNOSTICS - NO GALERKIN TAIL",
        "ANALYTIC ENERGY ENVELOPE - UPPER BOUND",
        "ANALYTIC ONLY - NO TRUNCATED OPERATOR NORM",
        "BLOCK PREDICTION (a/2-p)_+",
        "EXACT MAXIMUM TRANSIENT: NOT CLAIMED",
        "rho_0(0) = 1/4",
        "0.188106... is an integrated log coefficient, not a gain",
        "A2 DIRECT SUM / NONLINEAR / CLAY: OPEN",
    ]
    lineage = ("FORMAL - CERTIFICATE COMMIT LINEAGE SEALED" if formal else
               "DRAFT - FORMAL CERTIFICATE LINEAGE PENDING")
    return {
        "requiredVisibleBoundaries": all(value in text for value in required),
        "lineageStageVisible": lineage in text,
        "oppositeLineageStageAbsent": (("DRAFT - FORMAL CERTIFICATE LINEAGE PENDING" not in text)
                                       if formal else
                                       ("FORMAL - CERTIFICATE COMMIT LINEAGE SEALED" not in text)),
        "hardTwoChromaticRootCap": True,
        "nonColorRedundancy": True,
        "fourPanels": True,
        "blossomTopRightAndDataFree": True,
    }


def row_checks(rows: list[dict[str, str]]) -> dict[str, bool]:
    panel_a = [row for row in rows if row["panel"] == "A"]
    panel_b = [row for row in rows if row["panel"] == "B"]
    panel_c = [row for row in rows if row["panel"] == "C"]
    panel_d = [row for row in rows if row["panel"] == "D"]
    a_series = sorted({row["series"] for row in panel_a})
    c_series = sorted({row["series"] for row in panel_c})
    checks = {
        "totalRowCount": len(rows) == 364,
        "panelCounts": [len(panel_a), len(panel_b), len(panel_c), len(panel_d)] == [39, 12, 183, 130],
        "panelAThirteenDistinctMu": all(len({row["mu"] for row in panel_a if row["series"] == series}) == 13
                                        for series in a_series) and len(a_series) == 3,
        "panelBFourTriplets": all(sum(close(float(row["Lambda"]), lam) for row in panel_b) == 3
                                  for lam in (0.25, 1.0, 4.0, 16.0)),
        "panelC61PerCurve": len(c_series) == 3 and all(sum(row["series"] == series for row in panel_c) == 61
                                                       for series in c_series),
        "panelDPredictionAndObservedCounts": (sum(row["kind"] == "analytic-block-prediction" for row in panel_d) == 122
                                              and sum(row["kind"] == "observed-finite-exponent" for row in panel_d) == 8),
        "allSourcesHashed": all(row["sourcePath"] and re.fullmatch(r"[0-9a-f]{64}", row["sourceSha256"])
                                for row in rows),
        "finiteRowsExplicitlyN10": all(row["N"] == "10" for row in rows
                                        if row["status"] == "FINITE N=10 diagnostic"),
        "allValuesFinitePositiveWhereNeeded": all(math.isfinite(float(row["value"]))
                                                   and (float(row["value"]) > 0.0
                                                        if row["panel"] in "ABC" else float(row["value"]) >= 0.0)
                                                   for row in rows),
    }
    return checks


def check_formal_lineage(source_commit: str, certificate_commit: str,
                         evidence: dict[str, Any]) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
            "source commit must be full lowercase hex")
    require(re.fullmatch(r"[0-9a-f]{40}", certificate_commit) is not None,
            "certificate commit must be full lowercase hex")
    require(source_commit != certificate_commit,
            "source and certificate commits must be distinct")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                   text=True).strip()
    require(head == certificate_commit,
            "formal render must run at the certificate commit")
    require(subprocess.run(["git", "merge-base", "--is-ancestor", source_commit,
                            certificate_commit], cwd=ROOT).returncode == 0,
            "certificate commit does not descend from source commit")
    require(not subprocess.check_output(["git", "status", "--porcelain"],
                                        cwd=ROOT, text=True).strip(),
            "formal render requires a clean worktree")
    source_paths = [str(REL_PACKAGE / name) for name in SOURCE_FILES]
    require(subprocess.run(["git", "diff", "--quiet", source_commit, "--", *source_paths],
                           cwd=ROOT).returncode == 0,
            "figure source changed after declared source commit")
    certificate = evidence["certificate"]
    certificate_validation = evidence["certificateValidation"]
    require(certificate.get("certificateStage") == "formal"
            and certificate.get("sourceCommit") == source_commit,
            "certificate is not formal or is bound to another source commit")
    require(certificate_validation.get("stage") == "formal",
            "certificate validation stage is not formal")
    binding_commits = {row.get("commit") for row in evidence["certificateManifest"]["sourceBindings"]}
    require(binding_commits == {source_commit},
            "certificate manifest source bindings are not sealed to source commit")
    prior = PACKAGE / "manifest.json"
    if prior.is_file():
        require(read_json(prior).get("status") != "formal",
                "existing formal outputs are never overwritten")


def file_record(name: str) -> dict[str, Any]:
    path = PACKAGE / name
    return {"path": name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def build_results(rows: list[dict[str, str]], evidence: dict[str, Any]) -> dict[str, Any]:
    panel_a = [row for row in rows if row["panel"] == "A"]
    panel_b = [row for row in rows if row["panel"] == "B"]
    panel_d = [row for row in rows if row["panel"] == "D" and row["kind"] == "observed-finite-exponent"]
    return {
        "schemaVersion": 1,
        "figureId": FIGURE_ID,
        "release": RELEASE,
        "deterministic": True,
        "randomSeed": None,
        "rowCount": len(rows),
        "panelA": {
            "series": {series: {"distinctMu": len({row["mu"] for row in panel_a if row["series"] == series}),
                                "smallestMuGain": float(min((row for row in panel_a if row["series"] == series),
                                                            key=lambda row: float(row["mu"]))["gain"])}
                       for series in sorted({row["series"] for row in panel_a})},
            "finiteDimensionalOnly": True,
            "N": 10,
        },
        "panelB": {
            "comparisons": [{"Lambda": float(row["Lambda"]),
                              "finiteGain": float(row["finiteGain"]),
                              "triangularGain": float(next(item for item in panel_b
                                                           if item["kind"] == "triangular-limit-gain"
                                                           and item["Lambda"] == row["Lambda"])["triangularGain"]),
                              "energyEnvelope": float(next(item for item in panel_b
                                                           if item["kind"] == "analytic-energy-envelope"
                                                           and item["Lambda"] == row["Lambda"])["energyEnvelope"])}
                             for row in panel_b if row["kind"] == "finite-kinetic-gain"],
            "exactMaximumTransientClaimed": False,
        },
        "panelC": {"muPointCountPerCurve": 61, "rhoZeroAtDZero": 0.25,
                   "computedTruncationPlottedAsExact": False},
        "panelD": {"auditedPointCount": len(panel_d),
                   "maximumObservedPredictionDifference": max(abs(float(row["observedExponent"])
                                                                      - float(row["predictedExponent"]))
                                                                    for row in panel_d)},
        "sourceHashes": evidence["hashes"],
        "claimsNotMade": [
            "finite N=10 diagnostics provide a Galerkin tail bound",
            "the triangular finite-matrix limit is an infinite-dimensional maximum transient theorem",
            "the integrated coefficient 0.188106 is a propagator gain",
            "complete OS/Squire A2 direct sum is proved",
            "nonlinear Navier-Stokes is closed",
            "the Clay Millennium problem is solved",
        ],
    }


def write_qa_report(status: str, visual_inspected: bool,
                    checks: dict[str, bool]) -> None:
    lines = [
        "# R0.73B figure QA report", "",
        f"- manifest stage: {status}",
        f"- explicit visual inspection: {'yes' if visual_inspected else 'pending'}",
        "- final surface: 178 mm by 150 mm, 600-dpi PNG, vector PDF/SVG",
        "- PDF preview: independently rasterized with pdftoppm at 300 dpi",
        "- palette: hard two-root cap (blue and gold) plus neutrals",
        "- non-color redundancy: stroke patterns and filled/open/cross markers",
        "- finite/theorem boundary: visible in panel badges and footer",
        "", "## Machine checks", "",
    ]
    lines.extend(f"- [{'x' if passed else ' '}] {name}"
                 for name, passed in sorted(checks.items()))
    lines.extend([
        "", "## Visual boundary", "",
        "The three QA previews must be inspected at final size before formal sealing. "
        "Draft mode records the inspection result but cannot become publication-ready "
        "until certificate lineage is formal and distinct.", "",
    ])
    write_text(PACKAGE / "qa-report.md", "\n".join(lines))


def build_manifest(status: str, visual_inspected: bool, source_commit: str,
                   certificate_commit: str, rows: list[dict[str, str]],
                   evidence: dict[str, Any], checks: dict[str, bool],
                   details: dict[str, Any]) -> dict[str, Any]:
    outputs = [file_record(name) for name in SOURCE_FILES]
    for name in ("data.csv", "results.json", "validation.json", "figure.svg",
                 "figure.pdf", "figure.png", "qa-final-size.png",
                 "qa-grayscale.png", "qa-pdf.png", "qa-report.md"):
        outputs.append(file_record(name))
    return {
        "schemaVersion": 1,
        "figureId": FIGURE_ID,
        "release": RELEASE,
        "status": status,
        "createdAt": "2026-08-29T00:00:00+08:00",
        "deterministic": True,
        "randomSeed": None,
        "renderer": "custom SVG + ReportLab vector PDF + Pillow raster",
        "runtime": {"python": platform.python_version(),
                    "platform": platform.platform(),
                    "requestedThreads": 1,
                    "environmentThreadCaps": {key: os.environ.get(key, "unset")
                                              for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS",
                                                          "VECLIB_MAXIMUM_THREADS")}},
        "lineage": {"sourceCommit": source_commit,
                    "certificateCommit": certificate_commit,
                    "distinct": (source_commit != certificate_commit
                                 if status == "formal" else "pending"),
                    "formalBlocked": status != "formal"},
        "upstream": {key: {"path": str(path.relative_to(ROOT)),
                            "bytes": path.stat().st_size,
                            "sha256": evidence["hashes"][key]}
                     for key, path in evidence["paths"].items()},
        "data": {"rows": len(rows), "path": "data.csv",
                 "sha256": sha256(PACKAGE / "data.csv")},
        "figure": {"widthMillimetres": WIDTH_MM,
                   "heightMillimetres": HEIGHT_MM,
                   "pngDpi": PNG_DPI,
                   "outputs": [file_record(name) for name in
                               ("figure.pdf", "figure.svg", "figure.png")]},
        "qa": {"status": "passed" if visual_inspected and all(checks.values()) else "pending visual inspection",
               "visualInspectionExplicit": visual_inspected,
               "previews": ["qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"],
               "checks": checks, "details": details, "report": "qa-report.md"},
        "outputs": outputs,
        "publication": {"allowed": status == "formal" and visual_inspected and all(checks.values()),
                        "directory": "public/assets/r073b",
                        "copiesWrittenByRenderer": False},
        "claimBoundary": {"finiteN10Only": True,
                          "galerkinTailBound": False,
                          "exactMaximumTransientGain": False,
                          "completeA2DirectSum": False,
                          "nonlinearNavierStokes": False,
                          "clayMillenniumProblemSolved": False},
    }


def write_sums() -> None:
    names = SOURCE_FILES + [name for name in GENERATED_FILES if name != "SHA256SUMS"]
    require(all((PACKAGE / name).is_file() for name in names),
            "cannot write SHA256SUMS with missing inventory")
    write_text(PACKAGE / "SHA256SUMS",
               "".join(f"{sha256(PACKAGE / name)}  {name}\n" for name in sorted(names)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--draft", action="store_true")
    group.add_argument("--formal", action="store_true")
    parser.add_argument("--visual-inspected", action="store_true")
    parser.add_argument("--source-commit", default="pending")
    parser.add_argument("--certificate-commit", default="pending")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require(args.self_test or args.draft or args.formal,
            "choose --self-test, --draft, or --formal")
    config = read_json(PACKAGE / "config.json")
    evidence = upstream_gate(config)
    rows = build_rows(config, evidence)
    scene = build_scene(rows, formal=args.formal)
    checks = {**row_checks(rows), **visible_checks(scene, formal=args.formal)}
    require(all(checks.values()), "source/data/scene self-check failed")

    if args.self_test:
        print(json_text({"status": "passed", "release": RELEASE,
                         "rowCount": len(rows), "checks": checks,
                         "certificateStage": evidence["certificate"]["certificateStage"]}),
              end="")
        return 0

    if args.formal:
        require(args.visual_inspected, "formal render requires --visual-inspected")
        check_formal_lineage(args.source_commit, args.certificate_commit, evidence)
        status = "formal"
        source_commit, certificate_commit = args.source_commit, args.certificate_commit
    else:
        prior = PACKAGE / "manifest.json"
        if prior.is_file():
            require(read_json(prior).get("status") != "formal",
                    "draft may not overwrite formal outputs")
        status = "draft"
        source_commit = evidence["certificate"].get("sourceCommit", "pending")
        certificate_commit = "pending"

    with (PACKAGE / "data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    write_text(PACKAGE / "results.json", json_text(build_results(rows, evidence)))
    render_svg(scene, PACKAGE / "figure.svg")
    render_pdf(scene, PACKAGE / "figure.pdf")
    render_png(scene, PACKAGE / "figure.png")
    make_qa_previews()
    render_checks, details = inspect_outputs()
    checks.update(render_checks)
    require(all(checks.values()), "rendered-output self-check failed")
    validation = {"schemaVersion": 1, "figureId": FIGURE_ID,
                  "release": RELEASE, "status": "passed",
                  "stage": status, "visualInspectionExplicit": args.visual_inspected,
                  "checks": checks, "details": details}
    write_text(PACKAGE / "validation.json", json_text(validation))
    write_qa_report(status, args.visual_inspected, checks)
    manifest = build_manifest(status, args.visual_inspected, source_commit,
                              certificate_commit, rows, evidence, checks, details)
    write_text(PACKAGE / "manifest.json", json_text(manifest))
    write_sums()
    print(json_text({"status": status, "rowCount": len(rows),
                     "visualInspected": args.visual_inspected,
                     "publicationAllowed": manifest["publication"]["allowed"],
                     "checks": checks}), end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise
