#!/usr/bin/env python3
"""Generate deterministic source data for the R0.71P journal figure."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import time
from fractions import Fraction
from pathlib import Path


FIELDS = (
    "panel",
    "series",
    "case",
    "component",
    "N",
    "x",
    "y",
    "value",
    "unit",
    "formula",
    "evidenceClass",
    "note",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(left: float, right: float, tolerance: float = 2.0e-11) -> bool:
    return abs(left - right) <= tolerance * max(1.0, abs(left), abs(right))


def number(value: str | int | float) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    return float(Fraction(value))


def add(
    rows: list[dict[str, str]],
    panel: str,
    series: str,
    *,
    case: str = "",
    component: str = "",
    frequency: int | str = "",
    x: float = 0.0,
    y: float = 0.0,
    value: float = 0.0,
    unit: str = "",
    formula: str = "",
    evidence: str = "",
    note: str = "",
) -> None:
    rows.append(
        {
            "panel": panel,
            "series": series,
            "case": case,
            "component": component,
            "N": str(frequency),
            "x": f"{float(x):.17g}",
            "y": f"{float(y):.17g}",
            "value": f"{float(value):.17g}",
            "unit": unit,
            "formula": formula,
            "evidenceClass": evidence,
            "note": note,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact-certificate", type=Path, default=Path("exact-certificate.json"))
    parser.add_argument("--independent-certificate", type=Path, default=Path("independent-certificate.json"))
    parser.add_argument("--output", type=Path, default=Path("data.csv"))
    parser.add_argument("--metadata", type=Path, default=Path("figure-data-metadata.json"))
    args = parser.parse_args()
    started = time.perf_counter()

    exact = json.loads(args.exact_certificate.read_text(encoding="utf-8"))
    independent = json.loads(args.independent_certificate.read_text(encoding="utf-8"))
    if exact.get("release") != "R0.71P" or exact.get("status") != "passed":
        raise RuntimeError("exact R0.71P certificate must pass")
    if independent.get("release") != "R0.71P" or independent.get("status") != "passed":
        raise RuntimeError("independent R0.71P certificate must pass")

    rows: list[dict[str, str]] = []
    exact_face = "exact finite-order segmented/soft theorem"
    exact_batch = "exact Cauchy and bounded-overlap batching theorem"
    abstract = "exact abstract Hilbert-path separation; not NSE"
    nse_jet = "exact NSE initial jet; standalone FFT cross-check"

    # Panel A: take the soft positive part component by component.  This
    # relaxed entry measure need not equal the positive Jordan part of a
    # signed aggregate.  The even touch is the minimal discrepancy.
    for index, (case, a_plus, a_minus) in enumerate(
        (("odd crossing m=1", 1.0, 0.0), ("even touch m=2", 1.0, 1.0))
    ):
        hard_positive = max(a_plus - a_minus, 0.0)
        for component, value, formula in (
            ("segmentedSoftEntry", a_plus, "A_plus"),
            ("ordinaryHardPositiveAtom", hard_positive, "max(A_plus-A_minus,0)"),
            ("missingTouchMass", min(a_plus, a_minus), "min(A_plus,A_minus)"),
        ):
            add(
                rows,
                "A",
                "positiveAtomComparison",
                case=case,
                component=component,
                x=index,
                value=value,
                unit="normalized positive atom mass",
                formula=formula,
                evidence=exact_face,
                note="trace amplitudes normalized to one",
            )

    # Panel B: exact finite overlap-two ledger from the symbolic producer.
    overlap = exact["checks"]["sharpProjectionAndOverlap"]["finiteOverlapExample"]
    for index, record in enumerate(overlap["rows"], start=1):
        entry = number(record["entryAtom"])
        budget = number(record["localBudget"])
        for component, value, formula in (
            ("entryAtom", entry, "(<F,c>^+)^2/(Y*||c||^2)"),
            ("localSupportBudget", budget, "||1_supp(chi_Q)F||^2/Y"),
        ):
            add(
                rows,
                "B",
                "cellLedger",
                case=f"cell Q{index}",
                component=component,
                x=index,
                value=value,
                unit="normalized batch mass",
                formula=formula,
                evidence=exact_batch,
                note=f"support={record['support']}; overlap constant M_chi=2",
            )
    summaries = (
        ("entrySum", number(overlap["entrySum"]), "sum_Q A_plus"),
        ("localEnergySum", number(overlap["localEnergySum"]), "sum_Q ||1_supp F||^2/Y"),
        ("overlapGlobalBudget", number(overlap["overlapGlobalBudget"]), "M_chi*||F||^2/Y"),
    )
    for index, (component, value, formula) in enumerate(summaries):
        add(
            rows,
            "B",
            "batchSummary",
            case="simultaneous three-cell batch",
            component=component,
            x=index,
            value=value,
            unit="normalized batch mass",
            formula=formula,
            evidence=exact_batch,
            note="exact rational finite-overlap audit",
        )

    # Panel C: exact temporal-packing family with independent entry detection
    # and soft-layer quadrature at the same frequency grid.
    exact_samples = exact["checks"]["oscillatoryTemporalPacking"]["samples"]
    independent_rows = {
        int(record["N"]): record
        for record in independent["checks"]["oscillatoryEntries"]["rows"]
    }
    frequencies: list[int] = []
    for sample in exact_samples:
        frequency = int(sample["N"])
        frequencies.append(frequency)
        hard = float(frequency)
        soft = frequency / (1.0 + frequency ** -2)
        dt_budget = 2.0 * math.pi
        derivative_budget = math.pi
        denominator_mass = math.pi / frequency**2
        check = independent_rows[frequency]
        if int(check["detectedEntryCount"]) != frequency:
            raise RuntimeError(f"independent entry count mismatch at N={frequency}")
        if not close(float(check["softPositiveMass"]), soft):
            raise RuntimeError(f"independent soft mass mismatch at N={frequency}")
        if not close(float(check["denominatorMass"]), denominator_mass):
            raise RuntimeError(f"independent denominator mismatch at N={frequency}")
        for series, value, unit, formula, note in (
            ("hardEntryMass", hard, "positive entry mass", "N", "distinct entry-time count"),
            ("softEntryMass", soft, "positive entry mass", "N/(1+N^(-2))", "epsilon_N=N^(-4); plotted data, not a separate claim"),
            ("ordinaryTimeBudget", dt_budget, "time integral", "2*pi", "integral_0^(2*pi) 1 dt"),
            ("CtSquareMass", derivative_budget, "time integral", "pi", "integral_0^(2*pi) ||C_(N,t)||^2 dt"),
            ("denominatorMass", denominator_mass, "time integral", "pi/N^2", "integral_0^(2*pi) d_N dt"),
        ):
            add(
                rows,
                "C",
                series,
                case="C_N=N^(-1) sin(Nt)e on [0,2*pi)",
                frequency=frequency,
                x=frequency,
                y=value,
                value=value,
                unit=unit,
                formula=formula,
                evidence=abstract,
                note=(note + "; left endpoint included, right endpoint excluded; exactly N positive atoms"),
            )

    # Panel D: exact sharp NSE initial jet and its four target modes.
    exact_nse = exact["checks"]["nseSharpInitialBatch"]
    independent_nse = independent["checks"]["nseSharpInitialEntry"]
    for mode in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        add(
            rows,
            "D",
            "targetMode",
            case="filtered Lamb field",
            component=f"({mode[0]},{mode[1]},0)",
            x=mode[0],
            y=mode[1],
            value=0.25,
            unit="Fourier coefficient magnitude",
            formula="|F_hat(k)|=1/4",
            evidence=nse_jet,
            note="one of four exact target modes",
        )
    nse_metrics = (
        ("Y0", number(exact_nse["Y0"]), "||omega_0||_2^2"),
        ("F2", number(exact_nse["normFSquared"]), "||F(0)||_2^2"),
        ("c2", number(exact_nse["normLeadingDirectionSquared"]), "||c||_2^2"),
        ("pairing", number(exact_nse["leadingPairing"]), "<F(0),c>"),
        ("entryAtom", number(exact_nse["rightEntryAtom"]), "A_plus"),
        ("projectionBudget", number(exact_nse["oneCellProjectionBudget"]), "||F||_2^2/Y"),
        ("sharpnessRatio", number(exact_nse["sharpnessRatio"]), "A_plus/(||F||_2^2/Y)"),
    )
    for index, (component, value, formula) in enumerate(nse_metrics):
        add(
            rows,
            "D",
            "nseMetric",
            case="one-sided initial jet",
            component=component,
            x=index,
            value=value,
            unit="exact normalized scalar",
            formula=formula,
            evidence=nse_jet,
            note="exact Fourier result and standalone order-32 FFT cross-check",
        )
    add(
        rows,
        "D",
        "claimBoundary",
        case="one-sided initial jet",
        component="scope",
        evidence=nse_jet,
        note=exact_nse["claimBoundary"],
    )

    # Cross-check every independently reconstructed NSE scalar used above.
    independent_map = {
        "Y0": float(independent_nse["Y0"]),
        "F2": float(independent_nse["F2"]),
        "c2": float(independent_nse["leadingDirection2"]),
        "pairing": float(independent_nse["leadingPairing"]),
        "entryAtom": float(independent_nse["rightEntryAtom"]),
        "projectionBudget": float(independent_nse["projectionBudget"]),
        "sharpnessRatio": float(independent_nse["sharpnessRatio"]),
    }
    for component, value, _formula in nse_metrics:
        if not close(value, independent_map[component], 2.0e-12):
            raise RuntimeError(f"independent NSE mismatch for {component}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "release": "R0.71P",
        "rows": len(rows),
        "frequencies": frequencies,
        "exactCertificateSha256": digest(args.exact_certificate),
        "independentCertificateSha256": digest(args.independent_certificate),
        "independentRandomSeed": independent["checks"]["randomOverlapLedgers"]["seed"],
        "independentTrialCount": independent["checks"]["randomOverlapLedgers"]["trialCount"],
        "independentMaximumCellRatio": independent["checks"]["randomOverlapLedgers"]["maximumCellRatio"],
        "independentMaximumEntryToOverlapRatio": independent["checks"]["randomOverlapLedgers"]["maximumEntryToOverlapRatio"],
        "independentMaximumEntryCountError": independent["checks"]["oscillatoryEntries"]["maximumEntryCountError"],
        "independentMaximumSoftRelativeError": independent["checks"]["oscillatoryEntries"]["maximumSoftRelativeError"],
        "independentNseMaximumResidual": independent_nse["maximumResidual"],
        "dns": False,
        "pdeTimeStepping": False,
        "fittedData": False,
        "intervalCertified": False,
        "evidenceMap": {"A": exact_face, "B": exact_batch, "C": abstract, "D": nse_jet},
        "claimBoundary": (
            "Panel C uses [0,2*pi), includes the left endpoint, excludes the right endpoint, and has exactly N positive atoms. It is an abstract smooth Hilbert path, not a coupled NSE multiple-face construction. "
            "Panel D is one one-sided smooth NSE initial jet, not an internal or repeated NSE face theorem."
        ),
        "generationWallSeconds": time.perf_counter() - started,
    }
    args.metadata.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
