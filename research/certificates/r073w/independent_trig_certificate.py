#!/usr/bin/env python3
"""Independent exact R0.73W certificate in a real trigonometric basis.

This script does not import the primary producer.  It starts from real sine
and cosine coefficients, applies product-to-sum identities, and stores each
q-polynomial as a dense tuple of fractions.Fraction coefficients.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "independent-results.json"
CHECKLIST = HERE / "audit-checklist.json"

F = Fraction
Mode = tuple[int, int, int]
Basis = tuple[str, Mode]
Dense = tuple[Fraction, ...]
Field = dict[Basis, Dense]
ZERO_MODE: Mode = (0, 0, 0)


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    need(isinstance(value, dict), "JSON root must be an object: " + str(path))
    return value


def trim(values: Iterable[Fraction]) -> Dense:
    result = list(values)
    while result and result[-1] == 0:
        result.pop()
    return tuple(result)


def dconst(value: int | Fraction) -> Dense:
    value = F(value)
    return () if value == 0 else (value,)


def dadd(a: Dense, b: Dense) -> Dense:
    size = max(len(a), len(b))
    return trim(
        (a[index] if index < len(a) else F(0))
        + (b[index] if index < len(b) else F(0))
        for index in range(size)
    )


def dneg(a: Dense) -> Dense:
    return tuple(-value for value in a)


def dscale(a: Dense, value: int | Fraction) -> Dense:
    value = F(value)
    return trim(coefficient * value for coefficient in a)


def dmul(a: Dense, b: Dense) -> Dense:
    if not a or not b:
        return ()
    result = [F(0)] * (len(a) + len(b) - 1)
    for left_index, left in enumerate(a):
        for right_index, right in enumerate(b):
            result[left_index + right_index] += left * right
    return trim(result)


def dshift(a: Dense, count: int) -> Dense:
    return () if not a else tuple([F(0)] * count + list(a))


def dense_json(a: Dense) -> dict[str, object]:
    return {
        "coefficients": {
            str(index): str(value)
            for index, value in enumerate(a)
            if value != 0
        }
    }


def plus(a: Mode, b: Mode) -> Mode:
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def minus(a: Mode, b: Mode) -> Mode:
    return a[0] - b[0], a[1] - b[1], a[2] - b[2]


def opposite(a: Mode) -> Mode:
    return -a[0], -a[1], -a[2]


def square(a: Mode) -> int:
    return a[0] * a[0] + a[1] * a[1] + a[2] * a[2]


def normalize(kind: str, mode: Mode, coefficient: Dense) -> tuple[Basis, Dense] | None:
    need(kind in ("C", "S"), "unknown trigonometric basis")
    if mode == ZERO_MODE:
        if kind == "S":
            return None
        return ("C", ZERO_MODE), coefficient
    first = next(value for value in mode if value != 0)
    if first < 0:
        mode = opposite(mode)
        if kind == "S":
            coefficient = dneg(coefficient)
    return (kind, mode), coefficient


def fclean(a: Field) -> Field:
    return {basis: trim(poly) for basis, poly in a.items() if trim(poly)}


def add_term(result: Field, kind: str, mode: Mode, coefficient: Dense) -> None:
    normalized = normalize(kind, mode, coefficient)
    if normalized is None:
        return
    basis, poly = normalized
    result[basis] = dadd(result.get(basis, ()), poly)
    if not result[basis]:
        del result[basis]


def fadd(a: Field, b: Field) -> Field:
    result = dict(a)
    for basis, poly in b.items():
        result[basis] = dadd(result.get(basis, ()), poly)
    return fclean(result)


def fneg(a: Field) -> Field:
    return {basis: dneg(poly) for basis, poly in a.items()}


def fscale(a: Field, value: int | Fraction) -> Field:
    return fclean({basis: dscale(poly, value) for basis, poly in a.items()})


def basis_product(left: Basis, right: Basis) -> list[tuple[str, Mode, Fraction]]:
    left_kind, a = left
    right_kind, b = right
    half = F(1, 2)
    if left_kind == "C" and right_kind == "C":
        return [("C", minus(a, b), half), ("C", plus(a, b), half)]
    if left_kind == "S" and right_kind == "S":
        return [("C", minus(a, b), half), ("C", plus(a, b), -half)]
    if left_kind == "S" and right_kind == "C":
        return [("S", plus(a, b), half), ("S", minus(a, b), half)]
    need(left_kind == "C" and right_kind == "S", "unreachable basis pair")
    return [("S", plus(a, b), half), ("S", minus(b, a), half)]


def product(a: Field, b: Field) -> Field:
    result: Field = {}
    for left_basis in sorted(a):
        for right_basis in sorted(b):
            polynomial = dmul(a[left_basis], b[right_basis])
            for kind, mode, factor in basis_product(left_basis, right_basis):
                add_term(result, kind, mode, dscale(polynomial, factor))
    return fclean(result)


def heat(a: Field) -> Field:
    return {
        basis: dshift(poly, square(basis[1]))
        for basis, poly in a.items()
    }


def derivative(a: Field, coordinate: int) -> Field:
    result: Field = {}
    for (kind, mode), poly in a.items():
        wave = mode[coordinate]
        if wave == 0:
            continue
        if kind == "C":
            add_term(result, "S", mode, dscale(poly, -wave))
        else:
            add_term(result, "C", mode, dscale(poly, wave))
    return fclean(result)


def mean(a: Field) -> Dense:
    return a.get(("C", ZERO_MODE), ())


def make_2d3c_velocity() -> list[Field]:
    cx: Basis = ("C", (1, 0, 0))
    cy: Basis = ("C", (0, 1, 0))
    sxy: Basis = ("S", (1, 1, 0))
    return [
        {cy: dconst(-2), sxy: dconst(-2)},
        {cx: dconst(-2), sxy: dconst(2)},
        {cx: dconst(-1), cy: dconst(-1), sxy: dconst(-1)},
    ]


def make_coordinate_three_variable_triad() -> list[Field]:
    cyz: Basis = ("C", (0, 1, 1))
    cx: Basis = ("C", (1, 0, 0))
    sxyz: Basis = ("S", (1, 1, 1))
    return [
        {cyz: dconst(1), sxyz: dconst(-1)},
        {cx: dconst(1), sxyz: dconst(1)},
        {},
    ]


def make_rank_three_extension() -> list[Field]:
    result = [dict(component) for component in make_coordinate_three_variable_triad()]
    result[0][("C", (0, 0, 2))] = dconst(1)
    return result


def frequency_rank(u: list[Field]) -> int:
    """Compute the Q-rank of actual nonconstant trigonometric support."""
    modes = {
        mode
        for component in u
        for (_, mode) in component
        if mode != ZERO_MODE
    }
    rows = [[F(value) for value in mode] for mode in sorted(modes)]
    rank = 0
    for column in range(3):
        pivot = next((index for index in range(rank, len(rows)) if rows[index][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for index in range(len(rows)):
            if index == rank or rows[index][column] == 0:
                continue
            factor = rows[index][column]
            rows[index] = [
                rows[index][entry] - factor * rows[rank][entry]
                for entry in range(3)
            ]
        rank += 1
    return rank


def vector_neg(a: list[Field]) -> list[Field]:
    return [fneg(component) for component in a]


def tensor_stress(u: list[Field]) -> list[list[Field]]:
    v = [heat(component) for component in u]
    return [[
        fadd(heat(product(u[i], u[j])), fneg(product(v[i], v[j])))
        for j in range(3)
    ] for i in range(3)]


def production(u: list[Field]) -> Dense:
    v = [heat(component) for component in u]
    tau = tensor_stress(u)
    total: Field = {}
    for i in range(3):
        for j in range(3):
            total = fadd(total, product(tau[i][j], derivative(v[i], j)))
    return dneg(mean(total))


def gradient_energy(u: list[Field], filtered: bool) -> Dense:
    vector = [heat(component) for component in u] if filtered else u
    total: Field = {}
    for component in range(3):
        for coordinate in range(3):
            grad = derivative(vector[component], coordinate)
            total = fadd(total, product(grad, grad))
    return mean(total)


def divergence(u: list[Field]) -> Field:
    result: Field = {}
    for component in range(3):
        result = fadd(result, derivative(u[component], component))
    return result


def evaluate_path(root: dict[str, object], path: str) -> object:
    value: object = root
    for part in path.split("."):
        if isinstance(value, dict):
            need(part in value, "missing audit path: " + path)
            value = value[part]
        elif isinstance(value, list):
            value = value[int(part)]
        else:
            raise RuntimeError("audit path enters scalar: " + path)
    return value


def audit(common: dict[str, object]) -> list[dict[str, object]]:
    checklist = load_json(CHECKLIST)
    rows = checklist["requiredChecks"]
    need(isinstance(rows, list), "requiredChecks must be a list")
    report: list[dict[str, object]] = []
    for raw in rows:
        need(isinstance(raw, dict), "audit row must be an object")
        actual = evaluate_path(common, str(raw["path"]))
        passed = actual == raw["expected"]
        report.append({
            "actual": actual,
            "expected": raw["expected"],
            "id": raw["id"],
            "pass": passed,
            "path": raw["path"],
        })
        need(passed, "audit failure: " + str(raw["id"]))
    return report


def build() -> dict[str, object]:
    u = make_2d3c_velocity()
    minus_u = vector_neg(u)
    tau = tensor_stress(u)
    tau_minus = tensor_stress(minus_u)
    pi = production(u)
    pi_minus = production(minus_u)
    grad0 = gradient_energy(u, filtered=False)
    grad = gradient_energy(u, filtered=True)
    defect = dadd(grad0, dneg(grad))
    defect_minus = dadd(
        gradient_energy(minus_u, filtered=False),
        dneg(gradient_energy(minus_u, filtered=True)),
    )

    need(divergence(u) == {}, "locked real-trigonometric field is not divergence-free")
    need(all(mean(component) == () for component in u), "locked field has nonzero mean")
    need(pi == (F(0), F(0), F(-1), F(0), F(1)), "unexpected production")
    need(grad0 == (F(14),), "unexpected unfiltered gradient energy")
    need(grad == (F(0), F(0), F(5), F(0), F(9)), "unexpected filtered gradient energy")
    need(defect == (F(14), F(0), F(-5), F(0), F(-9)), "unexpected defect")
    need(tau_minus == tau, "stress parity failed")
    need(pi_minus == dneg(pi), "production parity failed")
    need(defect_minus == defect, "gradient-defect parity failed")

    w = make_coordinate_three_variable_triad()
    minus_w = vector_neg(w)
    w_tau = tensor_stress(w)
    w_tau_minus = tensor_stress(minus_w)
    w_pi = production(w)
    w_pi_minus = production(minus_w)
    w_grad0 = gradient_energy(w, filtered=False)
    w_grad = gradient_energy(w, filtered=True)
    w_defect = dadd(w_grad0, dneg(w_grad))
    w_defect_minus = dadd(
        gradient_energy(minus_w, filtered=False),
        dneg(gradient_energy(minus_w, filtered=True)),
    )
    need(divergence(w) == {}, "coordinate-three-variable triad is not divergence-free")
    need(all(mean(component) == () for component in w), "triad has nonzero mean")
    need(w_pi == (F(0), F(0), F(1, 4), F(0), F(-1, 4)), "unexpected triad production")
    need(w_grad0 == (F(9, 2),), "unexpected triad unfiltered energy")
    need(
        w_grad == (F(0), F(0), F(1, 2), F(0), F(1), F(0), F(3)),
        "unexpected triad filtered energy",
    )
    need(
        w_defect == (F(9, 2), F(0), F(-1, 2), F(0), F(-1), F(0), F(-3)),
        "unexpected triad defect",
    )
    need(w_tau_minus == w_tau, "triad stress parity failed")
    need(w_pi_minus == dneg(w_pi), "triad production parity failed")
    need(w_defect_minus == w_defect, "triad defect parity failed")
    need(frequency_rank(w) == 2, "triad frequency rank is not two")

    r = make_rank_three_extension()
    minus_r = vector_neg(r)
    r_tau = tensor_stress(r)
    r_tau_minus = tensor_stress(minus_r)
    r_pi = production(r)
    r_pi_minus = production(minus_r)
    r_grad0 = gradient_energy(r, filtered=False)
    r_grad = gradient_energy(r, filtered=True)
    r_defect = dadd(r_grad0, dneg(r_grad))
    r_defect_minus = dadd(
        gradient_energy(minus_r, filtered=False),
        dneg(gradient_energy(minus_r, filtered=True)),
    )
    need(divergence(r) == {}, "rank-three extension is not divergence-free")
    need(all(mean(component) == () for component in r), "rank-three extension has nonzero mean")
    need(frequency_rank(r) == 3, "rank-three extension support does not have rank three")
    need(r_pi == (F(0), F(0), F(1, 4), F(0), F(-1, 4)), "unexpected rank-three production")
    need(r_grad0 == (F(13, 2),), "unexpected rank-three unfiltered energy")
    need(
        r_grad == (
            F(0), F(0), F(1, 2), F(0), F(1), F(0), F(3), F(0), F(2)
        ),
        "unexpected rank-three filtered energy",
    )
    need(
        r_defect == (
            F(13, 2), F(0), F(-1, 2), F(0), F(-1), F(0), F(-3), F(0), F(-2)
        ),
        "unexpected rank-three defect",
    )
    need(r_tau_minus == r_tau, "rank-three stress parity failed")
    need(r_pi_minus == dneg(r_pi), "rank-three production parity failed")
    need(r_defect_minus == r_defect, "rank-three defect parity failed")

    common: dict[str, object] = {
        "absorptionRatio": {
            "cancelledFormula": "A*q^2/(nu*(14+9*q^2))",
            "conditions": "A>0, nu>0, 0<q<1",
            "linearInAmplitude": True,
            "qToOneCoefficient": "1/(23*nu)",
            "unboundedAsAtoInfinity": True,
        },
        "arithmetic": "exact finite q-polynomials; no floating point",
        "coordinateThreeVariableRankTwoTriad": {
            "absorptionRatio": {
                "cancelledFormula": "A*q^2/(2*nu*(9+8*q^2+6*q^4))",
                "conditions": "A>0, nu>0, 0<q<1",
                "linearInAmplitude": True,
                "qToOneCoefficient": "1/(46*nu)",
                "unboundedAsAtoInfinity": True,
            },
            "field": {
                "coordinateDependence": ["x", "y", "z"],
                "directionalInvariance": "(partial_y-partial_z)W=0",
                "divergenceFree": True,
                "frequencyRank": frequency_rank(w),
                "meanZero": True,
                "physical": [
                    "cos(y+z)-sin(x+y+z)",
                    "cos(x)+sin(x+y+z)",
                    "0",
                ],
                "real": True,
            },
            "gradient": {
                "defectExpanded": "1/2*(1-q^2)+(1-q^4)+3*(1-q^6)",
                "defectFactored": "1/2*(1-q^2)*(9+8*q^2+6*q^4)",
                "defectPerA2": dense_json(w_defect),
                "filteredPerA2": dense_json(w_grad),
                "unfilteredPerA2": dense_json(w_grad0),
            },
            "parity": {
                "gradientDefectEven": w_defect_minus == w_defect,
                "productionOdd": w_pi_minus == dneg(w_pi),
                "stressEven": w_tau_minus == w_tau,
            },
            "signedProduction": {
                "factored": "1/4*q^2*(1-q^2)",
                "perA3": dense_json(w_pi),
                "recomputedMinusWPerA3": dense_json(w_pi_minus),
                "signForAnegative": "negative for 0<q<1",
                "signForApositive": "positive for 0<q<1",
            },
        },
        "field": {
            "divergenceFree": True,
            "meanZero": True,
            "physical": [
                "-2*cos(y)-2*sin(x+y)",
                "-2*cos(x)+2*sin(x+y)",
                "-cos(x)-cos(y)-sin(x+y)",
            ],
            "real": True,
            "subclass": "2D3C",
        },
        "gradient": {
            "defectFactored": "(1-q^2)*(14+9*q^2)",
            "defectPerA2": dense_json(defect),
            "filteredPerA2": dense_json(grad),
            "unfilteredPerA2": dense_json(grad0),
        },
        "parity": {
            "gradientDefectEven": defect_minus == defect,
            "productionOdd": pi_minus == dneg(pi),
            "stressEven": tau_minus == tau,
        },
        "rankThreeExtension": {
            "absorptionRatio": {
                "cancelledFormula": "A*q^2/(2*nu*(13+12*q^2+10*q^4+4*q^6))",
                "conditions": "A>0, nu>0, 0<q<1",
                "linearInAmplitude": True,
                "qToOneCoefficient": "1/(78*nu)",
                "unboundedAsAtoInfinity": True,
            },
            "field": {
                "coordinateDependence": ["x", "y", "z"],
                "divergenceFree": True,
                "frequencyRank": frequency_rank(r),
                "meanZero": True,
                "physical": [
                    "cos(y+z)-sin(x+y+z)+cos(2*z)",
                    "cos(x)+sin(x+y+z)",
                    "0",
                ],
                "real": True,
            },
            "gradient": {
                "defectExpanded": "1/2*(1-q^2)+(1-q^4)+3*(1-q^6)+2*(1-q^8)",
                "defectFactored": "1/2*(1-q^2)*(13+12*q^2+10*q^4+4*q^6)",
                "defectPerA2": dense_json(r_defect),
                "filteredPerA2": dense_json(r_grad),
                "unfilteredPerA2": dense_json(r_grad0),
            },
            "parity": {
                "gradientDefectEven": r_defect_minus == r_defect,
                "productionOdd": r_pi_minus == dneg(r_pi),
                "stressEven": r_tau_minus == r_tau,
            },
            "signedProduction": {
                "factored": "1/4*q^2*(1-q^2)",
                "perA3": dense_json(r_pi),
                "recomputedMinusRPerA3": dense_json(r_pi_minus),
                "signForAnegative": "negative for 0<q<1",
                "signForApositive": "positive for 0<q<1",
            },
        },
        "scope": {
            "arbitraryThreeDimensionalGlobalRegularity": "OPEN",
            "clayConclusion": "OPEN",
            "dgxUsed": False,
            "notClay": True,
            "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
            "primaryWitnessFrequencyRank": 3,
            "retainedLowerDimensionalDiagnostic": "2D3C",
            "universalAmplitudeIndependentMeanAbsorptionDisproved": True,
            "universalPointwiseOneSidedSignRuleDisproved": True,
        },
        "signedProduction": {
            "factored": "-q^2*(1-q^2)",
            "perA3": dense_json(pi),
            "recomputedMinusUPerA3": dense_json(pi_minus),
            "signForAnegative": "positive for 0<q<1",
            "signForApositive": "negative for 0<q<1",
        },
    }
    checks = audit(common)
    return {
        "audit": {
            "passed": len(checks),
            "required": len(checks),
            "rows": checks,
        },
        "commonCore": common,
        "producer": {
            "basis": "canonical real cosine-sine modes with product-to-sum rules",
            "polynomialRepresentation": "dense rational coefficient tuple",
            "script": "independent_trig_certificate.py",
        },
        "schemaVersion": 1,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    result = build()
    encoded = canonical(result)
    if args.check_only:
        need(OUTPUT.is_file(), "missing generated independent-results.json")
        need(OUTPUT.read_text(encoding="utf-8") == encoded, "independent-results.json is stale")
    else:
        OUTPUT.write_text(encoded, encoding="utf-8")
    print("R073W_INDEPENDENT_TRIG_CERTIFICATE=PASS")
    print("R073W_PRIMARY_FREQUENCY_RANK=3")
    print("R073W_PRIMARY_PRODUCTION=1/4*q^2*(1-q^2)")
    print("R073W_PRIMARY_GRADIENT_DEFECT=1/2*(1-q^2)*(13+12*q^2+10*q^4+4*q^6)")
    print("R073W_DIAGNOSTIC_2D3C_PRODUCTION=-q^2*(1-q^2)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
