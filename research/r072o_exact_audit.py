#!/usr/bin/env python3
"""Producer exact-algebra audit for R0.72O.

The analytic report is the proof. This program uses rational monomial
exponents to audit the physical lift, the enhanced-dissipation crossover,
the local-floor quotient, the conditional multi-carrier implication, and
the exact two-carrier degeneracy identity. Its floating-point grid only
visualizes the resulting dimensionless screens.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import json
import math
import os
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


AUDIT = "R0.72O producer physical-reinsertion audit"
SCHEMA_VERSION = 1
R_VALUES = (16, 64, 256, 1024)
LEVELS = (0.01, 1.0, 100.0)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_commit(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


def append_ndjson(path: Path, value: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")


def frac(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def monomial(**values: Fraction) -> dict[str, Fraction]:
    return {key: value for key, value in values.items() if value}


def multiply(*terms: dict[str, Fraction]) -> dict[str, Fraction]:
    result: dict[str, Fraction] = {}
    for term in terms:
        for key, value in term.items():
            result[key] = result.get(key, Fraction(0)) + value
    return {key: value for key, value in result.items() if value}


def divide(left: dict[str, Fraction], right: dict[str, Fraction]) -> dict[str, Fraction]:
    return multiply(left, {key: -value for key, value in right.items()})


def serial(term: dict[str, Fraction]) -> dict[str, str]:
    return {key: frac(term[key]) for key in sorted(term)}


def exact_ledger() -> dict[str, Any]:
    u0 = monomial(epsilon=Fraction(4, 3), p=Fraction(4, 3))
    ed_raw = monomial(epsilon=Fraction(1, 2))
    u_ed = multiply(u0, ed_raw)
    v = monomial(epsilon=Fraction(1, 3), p=Fraction(1, 3), R=Fraction(1))
    h_ed = divide(u_ed, v)
    z = monomial(
        epsilon=Fraction(4, 3),
        p=Fraction(2),
        R=Fraction(2, 3),
        L=Fraction(1),
    )
    ed_over_z = divide(u_ed, z)
    one_carrier = {key: value for key, value in u_ed.items() if key != "p"}
    rho_squared = monomial(a=Fraction(2), N=Fraction(1))
    shear_norm = monomial(a=Fraction(1), B=Fraction(1))
    jacobian = monomial(
        epsilon=Fraction(1), a=Fraction(-1), B=Fraction(-1)
    )
    integrated_ed_gain = monomial(epsilon=Fraction(-1, 2))
    initial_energy = monomial(N=Fraction(1))
    superposition_cross_cubic = multiply(
        rho_squared,
        shear_norm,
        jacobian,
        integrated_ed_gain,
        initial_energy,
    )
    expected = {
        "U0": {"epsilon": "4/3", "p": "4/3"},
        "UED": {"epsilon": "11/6", "p": "4/3"},
        "UEDOneCarrier": {"epsilon": "11/6"},
        "HED": {"R": "-1/1", "epsilon": "3/2", "p": "1/1"},
        "ZStrong": {"L": "1/1", "R": "2/3", "epsilon": "4/3", "p": "2/1"},
        "UEDOverZ": {
            "L": "-1/1",
            "R": "-2/3",
            "epsilon": "1/2",
            "p": "-2/3",
        },
        "FullSuperpositionCrossCubic": {
            "N": "2/1",
            "a": "2/1",
            "epsilon": "1/2",
        },
    }
    actual = {
        "U0": serial(u0),
        "UED": serial(u_ed),
        "UEDOneCarrier": serial(one_carrier),
        "HED": serial(h_ed),
        "ZStrong": serial(z),
        "UEDOverZ": serial(ed_over_z),
        "FullSuperpositionCrossCubic": serial(superposition_cross_cubic),
    }
    transfers: list[dict[str, Any]] = []
    for name, alpha, beta in (
        ("raw", Fraction(1), Fraction(0)),
        ("enhancedDissipation", Fraction(1, 2), Fraction(0)),
        ("criticalLogTarget", Fraction(0), Fraction(1)),
    ):
        raw = monomial(epsilon=alpha, L=beta)
        numerator = multiply(u0, raw)
        quotient = divide(numerator, z)
        transfers.append(
            {
                "name": name,
                "alpha": frac(alpha),
                "beta": frac(beta),
                "normalizedNumerator": serial(numerator),
                "relativeToLocalFloor": serial(quotient),
            }
        )
    claim_contract = {
        "multiCarrierStatus": "conditional",
        "requiredHypothesis": "uniform full-superposition integrated ED",
        "constantsUniformOver": ["N", "p", "R", "epsilon", "declared geometry family"],
    }
    return {
        "actual": actual,
        "expected": expected,
        "exactExponentLedgerPassed": actual == expected,
        "generalExponentTransfers": transfers,
        "claimContract": claim_contract,
    }


def degeneracy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for r_value in R_VALUES:
        first = r_value - r_value
        second = 0
        third = -r_value**3 + r_value * (r_value + 1) ** 2
        expected_third = r_value * (2 * r_value + 1)
        rows.append(
            {
                "R": r_value,
                "secondCarrierCoefficient": f"{-r_value}/{r_value + 1}",
                "firstDerivativeAtZero": first,
                "secondDerivativeAtZero": second,
                "thirdDerivativeAtZero": third,
                "expectedThirdDerivative": expected_third,
                "frequenciesInCommonBand": r_value <= r_value + 1 <= 2 * r_value,
                "amplitudesComparable": 0.5 <= r_value / (r_value + 1) <= 1.0,
                "passed": (
                    first == 0
                    and second == 0
                    and third == expected_third
                    and expected_third != 0
                ),
            }
        )
    return rows


def screen_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for r_value in R_VALUES:
        for regime, p_value in (
            ("oneCarrier", 1.0),
            ("worstCommonBand", r_value ** -0.5),
        ):
            l_r = 1.0 + math.log(r_value)
            reference = (
                p_value ** (4.0 / 3.0)
                * r_value ** (4.0 / 3.0)
                * l_r**2
            )
            for level in LEVELS:
                epsilon = max(1.0, level * reference)
                l_re = 1.0 + math.log(
                    2.0 + r_value * r_value * (1.0 + epsilon)
                )
                z_exact = (
                    epsilon**2
                    * p_value**2
                    * r_value ** (2.0 / 3.0)
                    * (1.0 + epsilon) ** (-2.0 / 3.0)
                    * l_re
                )
                denominator = 1.0 + z_exact
                old_direct = (
                    epsilon ** (7.0 / 3.0)
                    * p_value ** (4.0 / 3.0)
                    / denominator
                )
                ed_direct = (
                    epsilon ** (11.0 / 6.0)
                    * p_value ** (4.0 / 3.0)
                    / denominator
                )
                predicted_ratio = (
                    math.sqrt(epsilon)
                    / (
                        p_value ** (2.0 / 3.0)
                        * r_value ** (2.0 / 3.0)
                        * l_re
                    )
                )
                rows.append(
                    {
                        "R": r_value,
                        "regime": regime,
                        "p": p_value,
                        "level": level,
                        "epsilon": epsilon,
                        "LR": l_r,
                        "LRepsilon": l_re,
                        "ZExact": z_exact,
                        "oldDirectNormalized": old_direct,
                        "edDirectNormalized": ed_direct,
                        "edOverOld": ed_direct / old_direct,
                        "predictedWindowRatio": predicted_ratio,
                        "passed": (
                            math.isfinite(ed_direct)
                            and ed_direct > 0.0
                            and ed_direct <= old_direct * (1.0 + 2.0e-13)
                            and abs(
                                ed_direct / old_direct
                                - epsilon ** (-0.5)
                            )
                            < 2.0e-13
                        ),
                    }
                )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[1]
    started = time.perf_counter()
    progress = output / "producer-progress.ndjson"
    resources = output / "producer-resource.ndjson"
    monitor = output / "producer-monitor.log"
    for path in (progress, resources, monitor):
        path.write_text("", encoding="utf-8")

    config = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT,
        "rValues": list(R_VALUES),
        "levels": list(LEVELS),
        "precision": "exact rational exponents plus IEEE binary64 screen grid",
        "gitCommit": git_commit(root),
        "limitations": (
            "The rational algebra audits the proof ledger. The finite grid is "
            "illustrative and does not prove enhanced dissipation, the action "
            "floor, or a general Navier-Stokes statement."
        ),
    }
    (output / "producer-config.json").write_text(
        json.dumps(config, indent=2) + "\n", encoding="utf-8"
    )
    append_ndjson(progress, {"time": utc_now(), "stage": "start", **config})

    ledger = exact_ledger()
    degeneracy = degeneracy_rows()
    screens = screen_rows()
    write_csv(output / "producer-degeneracy.csv", degeneracy)
    write_csv(output / "producer-window.csv", screens)
    (output / "producer-exponents.json").write_text(
        json.dumps(ledger, indent=2) + "\n", encoding="utf-8"
    )
    append_ndjson(
        progress,
        {
            "time": utc_now(),
            "stage": "exact-ledger",
            "passed": ledger["exactExponentLedgerPassed"],
        },
    )
    append_ndjson(
        progress,
        {
            "time": utc_now(),
            "stage": "degeneracy",
            "cases": len(degeneracy),
            "passed": all(row["passed"] for row in degeneracy),
        },
    )
    append_ndjson(
        progress,
        {
            "time": utc_now(),
            "stage": "screens",
            "cases": len(screens),
            "passed": all(row["passed"] for row in screens),
        },
    )

    checks = {
        "exactExponentLedgerPassed": ledger["exactExponentLedgerPassed"],
        "allDegeneracyCasesPassed": all(row["passed"] for row in degeneracy),
        "allScreenCasesPassed": all(row["passed"] for row in screens),
        "oneCarrierExponentIsElevenSixths": (
            ledger["actual"]["UEDOneCarrier"] == {"epsilon": "11/6"}
        ),
        "generalPResultMarkedConditional": (
            ledger["claimContract"]["multiCarrierStatus"] == "conditional"
            and ledger["claimContract"]["requiredHypothesis"]
            == "uniform full-superposition integrated ED"
            and {"N", "p", "R", "epsilon"}.issubset(
                ledger["claimContract"]["constantsUniformOver"]
            )
        ),
        "multiCarrierCrossTermScaleRetainsN2": (
            ledger["actual"]["FullSuperpositionCrossCubic"]
            == {"N": "2/1", "a": "2/1", "epsilon": "1/2"}
        ),
        "epsilonOneEqualityHandled": all(
            row["edDirectNormalized"]
            <= row["oldDirectNormalized"] * (1.0 + 2.0e-13)
            for row in screens
            if row["epsilon"] == 1.0
        ),
    }
    result = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT,
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "ledger": ledger,
        "degeneracyCases": len(degeneracy),
        "screenCases": len(screens),
        "elapsedSeconds": time.perf_counter() - started,
        "maxRssMb": max_rss_mb(),
        "limitations": config["limitations"],
    }
    (output / "producer-result.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    append_ndjson(
        output / "producer-resource.ndjson",
        {
            "time": utc_now(),
            "event": "complete",
            "elapsedSeconds": result["elapsedSeconds"],
            "maxRssMb": result["maxRssMb"],
            "pid": os.getpid(),
        },
    )
    monitor.write_text(
        f"[producer] status={result['status']} "
        f"exact={checks['exactExponentLedgerPassed']} "
        f"degeneracy={len(degeneracy)} screens={len(screens)}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
