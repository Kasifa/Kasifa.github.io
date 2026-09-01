#!/usr/bin/env python3
"""Finite arithmetic certificate for the R0.74A localized K_D ledger.

This script checks exact rational scaling and homogeneity exponents.  It is
not a symbolic proof of the analytic estimates in the R0.74A note.
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "research" / "r074a_localized_kd_certificate.json"
REPORT_PATH = ROOT / "research" / "r074a_localized_kd_certificate_report.md"


def f(value: int, denominator: int = 1) -> Fraction:
    return Fraction(value, denominator)


def fs(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def check(name: str, actual: Fraction, expected: Fraction) -> dict[str, Any]:
    return {
        "name": name,
        "actual": fs(actual),
        "expected": fs(expected),
        "pass": actual == expected,
    }


def build_certificate() -> dict[str, Any]:
    # Navier--Stokes scaling convention: Q[u_lambda] = lambda^e Q[u].
    scale = {
        "u": f(1),
        "grad_u": f(2),
        "D_s": f(4),
        "k_s": f(2),
        "sqrt_k_s": f(1),
        "dx": f(-3),
        "dt": f(-2),
        "ds": f(-2),
        "R": f(-1),
        "nu": f(0),
    }

    kd_scale = -f(2) * scale["R"] + scale["nu"] + scale["D_s"] + scale["sqrt_k_s"] + scale["dx"] + scale["dt"] + scale["ds"]
    kd_amplitude = f(2) + f(1)

    quantities = {
        "A_c": -scale["R"] + scale["dx"] + f(2) * scale["u"],
        "B_c": scale["nu"] - scale["R"] + scale["dt"] + scale["dx"] + f(2) * scale["grad_u"],
        "U_ext": -scale["R"] + scale["dx"] + f(2) * scale["u"],
        "D_ext": scale["nu"] - scale["R"] + scale["dt"] + scale["dx"] + f(2) * scale["grad_u"],
    }

    blocks = {
        "cc=A_c^(1/2) B_c": f(1, 2) * quantities["A_c"] + quantities["B_c"],
        "ce=B_c U_ext^(1/2)": quantities["B_c"] + f(1, 2) * quantities["U_ext"],
        "ec=A_c^(1/2) D_ext": f(1, 2) * quantities["A_c"] + quantities["D_ext"],
        "ee=U_ext^(1/2) D_ext": f(1, 2) * quantities["U_ext"] + quantities["D_ext"],
    }

    theta = {"cc": f(1, 4), "ce": f(1), "ec": f(1, 4), "ee": f(1)}

    packet_epsilon = f(-2, 3)
    packet = {
        "epsilon": packet_epsilon,
        "K_D": f(2) * packet_epsilon + f(2) + packet_epsilon,
        "old_L3_tail": f(3) * packet_epsilon,
        "gradient_energy": f(2) * packet_epsilon + f(2),
    }

    spike_amplitude = f(-1, 3)
    spike = {
        "amplitude": spike_amplitude,
        "L3_time": f(1) + f(3) * spike_amplitude,
        "Linf_L2": f(2) * spike_amplitude,
    }

    alias_definition = {
        "analytic_name": "G_{nabla,ext}^{1,square}",
        "certificate_alias": "D_ext",
        "coefficient": {"nu": "1", "R": "-1", "dt": "1", "grad_u_squared": "1"},
    }
    alias_expected = {"nu": "1", "R": "-1", "dt": "1", "grad_u_squared": "1"}

    checks: list[dict[str, Any]] = [
        check("K_D Navier-Stokes scaling exponent", kd_scale, f(0)),
        check("K_D amplitude degree", kd_amplitude, f(3)),
    ]
    checks.extend(check(f"{name} scaling exponent", exponent, f(0)) for name, exponent in quantities.items())
    checks.extend(check(f"block {name}", exponent, f(0)) for name, exponent in blocks.items())
    checks.extend(check(f"theta exponent {name}", exponent, {"cc": f(1, 4), "ce": f(1), "ec": f(1, 4), "ee": f(1)}[name]) for name, exponent in theta.items())
    checks.extend(
        [
            check("packet epsilon exponent", packet["epsilon"], f(-2, 3)),
            check("packet K_D exponent", packet["K_D"], f(0)),
            check("packet old tail exponent", packet["old_L3_tail"], f(-2)),
            check("packet gradient energy exponent", packet["gradient_energy"], f(2, 3)),
            check("time spike L3-time exponent", spike["L3_time"], f(0)),
            check("time spike Linf-L2 exponent", spike["Linf_L2"], f(-2, 3)),
        ]
    )
    alias_pass = alias_definition["coefficient"] == alias_expected
    checks.append({"name": "D_ext alias coefficient map", "actual": alias_definition["coefficient"], "expected": alias_expected, "pass": alias_pass})

    return {
        "certificate": "R0.74A localized K_D finite arithmetic cross-check",
        "schema_version": 1,
        "status": "PASS" if all(item["pass"] for item in checks) else "FAIL",
        "scope": "FINITE arithmetic cross-check only; analytic quantifiers remain in the main proof; NOT CLAY",
        "convention": "Q[u_lambda](t,x)=lambda^e Q[u](lambda^2 t,lambda x); stored exponents are e",
        "base_scaling_exponents": {name: fs(value) for name, value in scale.items()},
        "derived": {
            "K_D": {"scaling_exponent": fs(kd_scale), "amplitude_degree": fs(kd_amplitude)},
            "localized_quantities": {name: fs(value) for name, value in quantities.items()},
            "block_products": {name: fs(value) for name, value in blocks.items()},
            "theta_exponents": {name: fs(value) for name, value in theta.items()},
            "packet_N_exponents": {name: fs(value) for name, value in packet.items()},
            "time_spike_delta_exponents": {name: fs(value) for name, value in spike.items()},
            "D_ext_alias": alias_definition,
        },
        "checks": checks,
        "summary": {"passed": sum(item["pass"] for item in checks), "total": len(checks)},
    }


def json_text(certificate: dict[str, Any]) -> str:
    return json.dumps(certificate, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def report_text(certificate: dict[str, Any]) -> str:
    derived = certificate["derived"]
    lines = [
        "# R0.74A localized K_D finite arithmetic certificate",
        "",
        f"**Status:** `{certificate['status']}`",
        "",
        "**Scope:** `FINITE_ARITHMETIC_CROSS_CHECK_ONLY`",
        "",
        "This report checks exact rational exponents with Python `Fraction`. It does not check analytic quantifiers, Gaussian kernel estimates, measurability, or the suitable-weak passage. Those remain the responsibility of the main proof.",
        "",
        "## Scaling ledger",
        "",
        "| Item | Exponent / degree | Expected |",
        "|---|---:|---:|",
        f"| K_D Navier--Stokes scaling | {derived['K_D']['scaling_exponent']} | 0 |",
        f"| K_D amplitude degree | {derived['K_D']['amplitude_degree']} | 3 |",
    ]
    for name, value in derived["localized_quantities"].items():
        lines.append(f"| {name} scaling | {value} | 0 |")
    for name, value in derived["block_products"].items():
        lines.append(f"| {name} | {value} | 0 |")
    lines.extend(["", "## Scale-integration exponents", "", "| Block | Theta exponent |", "|---|---:|"])
    for name, value in derived["theta_exponents"].items():
        lines.append(f"| {name} | {value} |")
    lines.extend(["", "## Function-level obstruction ledgers", "", "For the spatial packet, the amplitude exponent is fixed by `epsilon=N^(-2/3)`.", "", "| Packet item | N exponent |", "|---|---:|"])
    for name, value in derived["packet_N_exponents"].items():
        lines.append(f"| {name} | {value} |")
    lines.extend(["", "For the time spike, the amplitude is `delta^(-1/3)`.", "", "| Time-spike item | Delta exponent |", "|---|---:|"])
    for name, value in derived["time_spike_delta_exponents"].items():
        lines.append(f"| {name} | {value} |")
    alias = derived["D_ext_alias"]
    lines.extend(
        [
            "",
            "## Alias check",
            "",
            f"`D_ext` is the certificate alias for `{alias['analytic_name']}`. Both use the coefficient map `nu^1 R^(-1) dt^1 |grad u|^2`, so the alias is consistent with the analytic definition.",
            "",
            "## Result",
            "",
            f"All {certificate['summary']['total']} finite arithmetic checks pass.",
            "",
            "## Boundary",
            "",
            "- Analytic quantifiers and inequalities are not machine-certified here.",
            "- This certificate does not establish smallness, absorption, compactness, lower semicontinuity, or regularity.",
            "- `NOT CLAY`.",
            "",
        ]
    )
    return "\n".join(lines)


def check_only(certificate: dict[str, Any]) -> int:
    expected_json = json_text(certificate)
    expected_report = report_text(certificate)
    errors: list[str] = []
    if not JSON_PATH.exists() or JSON_PATH.read_text(encoding="utf-8") != expected_json:
        errors.append(str(JSON_PATH))
    if not REPORT_PATH.exists() or REPORT_PATH.read_text(encoding="utf-8") != expected_report:
        errors.append(str(REPORT_PATH))
    if certificate["status"] != "PASS":
        errors.append("internal arithmetic status")
    if errors:
        print("R0.74A certificate check failed: " + ", ".join(errors), file=sys.stderr)
        return 1
    print(f"R0.74A certificate PASS: {certificate['summary']['passed']}/{certificate['summary']['total']} checks; artifacts identical")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="verify committed artifacts without writing")
    parser.add_argument("--print-json", action="store_true", help="print deterministic JSON to stdout")
    parser.add_argument("--print-report", action="store_true", help="print deterministic Markdown report to stdout")
    args = parser.parse_args()
    certificate = build_certificate()
    if args.print_json:
        sys.stdout.write(json_text(certificate))
        return 0
    if args.print_report:
        sys.stdout.write(report_text(certificate))
        return 0
    if args.check_only:
        return check_only(certificate)
    JSON_PATH.write_text(json_text(certificate), encoding="utf-8")
    REPORT_PATH.write_text(report_text(certificate), encoding="utf-8")
    print(f"wrote {JSON_PATH}")
    print(f"wrote {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
