#!/usr/bin/env python3
"""Primary exact R0.73W certificate: sparse complex Fourier arithmetic.

All coefficients are finite q-polynomials over Gaussian rationals.  The
script uses no floating point and no package outside the Python standard
library.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results.json"
CHECKLIST = HERE / "audit-checklist.json"

F = Fraction
Mode = tuple[int, int, int]
Gaussian = tuple[Fraction, Fraction]
Poly = dict[int, Gaussian]
Field = dict[Mode, Poly]

ZERO: Gaussian = (F(0), F(0))
ONE: Gaussian = (F(1), F(0))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    require(isinstance(value, dict), "JSON root must be an object: " + str(path))
    return value


def g(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    return F(real), F(imag)


def gadd(a: Gaussian, b: Gaussian) -> Gaussian:
    return a[0] + b[0], a[1] + b[1]


def gneg(a: Gaussian) -> Gaussian:
    return -a[0], -a[1]


def gmul(a: Gaussian, b: Gaussian) -> Gaussian:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def gconj(a: Gaussian) -> Gaussian:
    return a[0], -a[1]


def gtext(a: Gaussian) -> str:
    real, imag = a
    if imag == 0:
        return str(real)
    if real == 0:
        if imag == 1:
            return "i"
        if imag == -1:
            return "-i"
        return str(imag) + "*i"
    sign = "+" if imag > 0 else "-"
    magnitude = abs(imag)
    return str(real) + sign + ("i" if magnitude == 1 else str(magnitude) + "*i")


def pclean(a: Poly) -> Poly:
    return {power: value for power, value in a.items() if value != ZERO}


def pconst(value: Gaussian) -> Poly:
    return {} if value == ZERO else {0: value}


def padd(a: Poly, b: Poly) -> Poly:
    result = dict(a)
    for power, value in b.items():
        result[power] = gadd(result.get(power, ZERO), value)
    return pclean(result)


def pneg(a: Poly) -> Poly:
    return {power: gneg(value) for power, value in a.items()}


def pscale(a: Poly, value: Gaussian) -> Poly:
    return pclean({power: gmul(coefficient, value) for power, coefficient in a.items()})


def pmul(a: Poly, b: Poly) -> Poly:
    result: Poly = {}
    for left_power, left_value in a.items():
        for right_power, right_value in b.items():
            power = left_power + right_power
            result[power] = gadd(result.get(power, ZERO), gmul(left_value, right_value))
    return pclean(result)


def pshift(a: Poly, count: int) -> Poly:
    return {power + count: value for power, value in a.items()}


def poly_json(a: Poly) -> dict[str, object]:
    require(all(value[1] == 0 for value in a.values()), "expected a real polynomial")
    return {
        "coefficients": {
            str(power): str(value[0]) for power, value in sorted(a.items())
        }
    }


def mode_add(a: Mode, b: Mode) -> Mode:
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def mode_neg(a: Mode) -> Mode:
    return -a[0], -a[1], -a[2]


def norm2(a: Mode) -> int:
    return a[0] * a[0] + a[1] * a[1] + a[2] * a[2]


def fclean(a: Field) -> Field:
    return {mode: pclean(poly) for mode, poly in a.items() if pclean(poly)}


def fadd(a: Field, b: Field) -> Field:
    result = {mode: dict(poly) for mode, poly in a.items()}
    for mode, poly in b.items():
        result[mode] = padd(result.get(mode, {}), poly)
    return fclean(result)


def fneg(a: Field) -> Field:
    return {mode: pneg(poly) for mode, poly in a.items()}


def fscale(a: Field, value: Gaussian) -> Field:
    return fclean({mode: pscale(poly, value) for mode, poly in a.items()})


def fmul(a: Field, b: Field) -> Field:
    result: Field = {}
    for left_mode in sorted(a):
        for right_mode in sorted(b):
            mode = mode_add(left_mode, right_mode)
            result[mode] = padd(
                result.get(mode, {}), pmul(a[left_mode], b[right_mode])
            )
    return fclean(result)


def heat(a: Field) -> Field:
    return {mode: pshift(poly, norm2(mode)) for mode, poly in a.items()}


def derivative(a: Field, coordinate: int) -> Field:
    return fclean({
        mode: pscale(poly, g(0, mode[coordinate]))
        for mode, poly in a.items()
        if mode[coordinate] != 0
    })


def mean(a: Field) -> Poly:
    return a.get((0, 0, 0), {})


def vector_neg(a: list[Field]) -> list[Field]:
    return [fneg(component) for component in a]


def make_2d3c_velocity() -> list[Field]:
    """Return exact Fourier coefficients of the locked 2D3C field."""
    positive: dict[Mode, tuple[Gaussian, Gaussian, Gaussian]] = {
        (1, 0, 0): (g(), g(-1), g(F(-1, 2))),
        (0, 1, 0): (g(-1), g(), g(F(-1, 2))),
        (1, 1, 0): (g(0, 1), g(0, -1), g(0, F(1, 2))),
    }
    result: list[Field] = [{}, {}, {}]
    for mode, vector in positive.items():
        negative = mode_neg(mode)
        for component in range(3):
            result[component][mode] = pconst(vector[component])
            result[component][negative] = pconst(gconj(vector[component]))
    return result


def make_coordinate_three_variable_triad() -> list[Field]:
    """Return the x,y,z-coordinate-dependent, frequency-rank-two triad."""
    positive: dict[Mode, tuple[Gaussian, Gaussian, Gaussian]] = {
        (0, 1, 1): (g(F(1, 2)), g(), g()),
        (1, 0, 0): (g(), g(F(1, 2)), g()),
        (1, 1, 1): (g(0, F(1, 2)), g(0, F(-1, 2)), g()),
    }
    result: list[Field] = [{}, {}, {}]
    for mode, vector in positive.items():
        negative = mode_neg(mode)
        for component in range(3):
            result[component][mode] = pconst(vector[component])
            result[component][negative] = pconst(gconj(vector[component]))
    return result


def make_rank_three_extension() -> list[Field]:
    """Add (1,0,0) cos(2z) to the triad and return a rank-three field."""
    result = [
        {mode: dict(poly) for mode, poly in component.items()}
        for component in make_coordinate_three_variable_triad()
    ]
    mode = (0, 0, 2)
    result[0][mode] = pconst(g(F(1, 2)))
    result[0][mode_neg(mode)] = pconst(g(F(1, 2)))
    return result


def frequency_rank(u: list[Field]) -> int:
    """Compute the Q-rank of the nonzero Fourier support by exact elimination."""
    rows = [
        [F(value) for value in mode]
        for mode in sorted(set().union(*(component.keys() for component in u)))
        if mode != (0, 0, 0)
    ]
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


def tensor_stress(u: list[Field]) -> list[list[Field]]:
    v = [heat(component) for component in u]
    return [[
        fadd(heat(fmul(u[i], u[j])), fneg(fmul(v[i], v[j])))
        for j in range(3)
    ] for i in range(3)]


def production(u: list[Field]) -> Poly:
    v = [heat(component) for component in u]
    tau = tensor_stress(u)
    total: Field = {}
    for i in range(3):
        for j in range(3):
            total = fadd(total, fmul(tau[i][j], derivative(v[i], j)))
    return pneg(mean(total))


def gradient_energy(u: list[Field], filtered: bool) -> Poly:
    vector = [heat(component) for component in u] if filtered else u
    total: Field = {}
    for component in range(3):
        for coordinate in range(3):
            gradient = derivative(vector[component], coordinate)
            total = fadd(total, fmul(gradient, gradient))
    return mean(total)


def divergence(u: list[Field]) -> Field:
    total: Field = {}
    for component in range(3):
        total = fadd(total, derivative(u[component], component))
    return total


def evaluate_path(root: dict[str, object], path: str) -> object:
    value: object = root
    for part in path.split("."):
        if isinstance(value, dict):
            require(part in value, "missing audit path: " + path)
            value = value[part]
        elif isinstance(value, list):
            value = value[int(part)]
        else:
            raise RuntimeError("audit path enters scalar: " + path)
    return value


def audit(common: dict[str, object]) -> list[dict[str, object]]:
    checklist = load_json(CHECKLIST)
    rows = checklist["requiredChecks"]
    require(isinstance(rows, list), "requiredChecks must be a list")
    report: list[dict[str, object]] = []
    for raw in rows:
        require(isinstance(raw, dict), "audit row must be an object")
        actual = evaluate_path(common, str(raw["path"]))
        passed = actual == raw["expected"]
        report.append({
            "actual": actual,
            "expected": raw["expected"],
            "id": raw["id"],
            "pass": passed,
            "path": raw["path"],
        })
        require(passed, "audit failure: " + str(raw["id"]))
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
    defect = padd(grad0, pneg(grad))
    defect_minus = padd(
        gradient_energy(minus_u, filtered=False),
        pneg(gradient_energy(minus_u, filtered=True)),
    )

    require(divergence(u) == {}, "locked field is not divergence-free")
    require(all(mean(component) == {} for component in u), "locked field has nonzero mean")
    require(pi == {2: g(-1), 4: g(1)}, "unexpected production polynomial")
    require(grad0 == {0: g(14)}, "unexpected unfiltered gradient energy")
    require(grad == {2: g(5), 4: g(9)}, "unexpected filtered gradient energy")
    require(defect == {0: g(14), 2: g(-5), 4: g(-9)}, "unexpected defect")
    require(tau_minus == tau, "stress parity failed")
    require(pi_minus == pneg(pi), "production parity failed")
    require(defect_minus == defect, "gradient-defect parity failed")

    w = make_coordinate_three_variable_triad()
    minus_w = vector_neg(w)
    w_tau = tensor_stress(w)
    w_tau_minus = tensor_stress(minus_w)
    w_pi = production(w)
    w_pi_minus = production(minus_w)
    w_grad0 = gradient_energy(w, filtered=False)
    w_grad = gradient_energy(w, filtered=True)
    w_defect = padd(w_grad0, pneg(w_grad))
    w_defect_minus = padd(
        gradient_energy(minus_w, filtered=False),
        pneg(gradient_energy(minus_w, filtered=True)),
    )
    require(divergence(w) == {}, "coordinate-three-variable triad is not divergence-free")
    require(all(mean(component) == {} for component in w), "triad has nonzero mean")
    require(w_pi == {2: g(F(1, 4)), 4: g(F(-1, 4))}, "unexpected triad production")
    require(w_grad0 == {0: g(F(9, 2))}, "unexpected triad unfiltered energy")
    require(
        w_grad == {2: g(F(1, 2)), 4: g(1), 6: g(3)},
        "unexpected triad filtered energy",
    )
    require(
        w_defect == {0: g(F(9, 2)), 2: g(F(-1, 2)), 4: g(-1), 6: g(-3)},
        "unexpected triad defect",
    )
    require(w_tau_minus == w_tau, "triad stress parity failed")
    require(w_pi_minus == pneg(w_pi), "triad production parity failed")
    require(w_defect_minus == w_defect, "triad defect parity failed")
    require(frequency_rank(w) == 2, "triad frequency rank is not two")

    r = make_rank_three_extension()
    minus_r = vector_neg(r)
    r_tau = tensor_stress(r)
    r_tau_minus = tensor_stress(minus_r)
    r_pi = production(r)
    r_pi_minus = production(minus_r)
    r_grad0 = gradient_energy(r, filtered=False)
    r_grad = gradient_energy(r, filtered=True)
    r_defect = padd(r_grad0, pneg(r_grad))
    r_defect_minus = padd(
        gradient_energy(minus_r, filtered=False),
        pneg(gradient_energy(minus_r, filtered=True)),
    )
    require(divergence(r) == {}, "rank-three extension is not divergence-free")
    require(all(mean(component) == {} for component in r), "rank-three extension has nonzero mean")
    require(frequency_rank(r) == 3, "rank-three extension support does not have rank three")
    require(r_pi == {2: g(F(1, 4)), 4: g(F(-1, 4))}, "unexpected rank-three production")
    require(r_grad0 == {0: g(F(13, 2))}, "unexpected rank-three unfiltered energy")
    require(
        r_grad == {2: g(F(1, 2)), 4: g(1), 6: g(3), 8: g(2)},
        "unexpected rank-three filtered energy",
    )
    require(
        r_defect == {
            0: g(F(13, 2)), 2: g(F(-1, 2)), 4: g(-1), 6: g(-3), 8: g(-2)
        },
        "unexpected rank-three defect",
    )
    require(r_tau_minus == r_tau, "rank-three stress parity failed")
    require(r_pi_minus == pneg(r_pi), "rank-three production parity failed")
    require(r_defect_minus == r_defect, "rank-three defect parity failed")

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
                "frequencyRank": 2,
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
                "defectPerA2": poly_json(w_defect),
                "filteredPerA2": poly_json(w_grad),
                "unfilteredPerA2": poly_json(w_grad0),
            },
            "parity": {
                "gradientDefectEven": w_defect_minus == w_defect,
                "productionOdd": w_pi_minus == pneg(w_pi),
                "stressEven": w_tau_minus == w_tau,
            },
            "signedProduction": {
                "factored": "1/4*q^2*(1-q^2)",
                "perA3": poly_json(w_pi),
                "recomputedMinusWPerA3": poly_json(w_pi_minus),
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
            "defectPerA2": poly_json(defect),
            "filteredPerA2": poly_json(grad),
            "unfilteredPerA2": poly_json(grad0),
        },
        "parity": {
            "gradientDefectEven": defect_minus == defect,
            "productionOdd": pi_minus == pneg(pi),
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
                "defectPerA2": poly_json(r_defect),
                "filteredPerA2": poly_json(r_grad),
                "unfilteredPerA2": poly_json(r_grad0),
            },
            "parity": {
                "gradientDefectEven": r_defect_minus == r_defect,
                "productionOdd": r_pi_minus == pneg(r_pi),
                "stressEven": r_tau_minus == r_tau,
            },
            "signedProduction": {
                "factored": "1/4*q^2*(1-q^2)",
                "perA3": poly_json(r_pi),
                "recomputedMinusRPerA3": poly_json(r_pi_minus),
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
            "perA3": poly_json(pi),
            "recomputedMinusUPerA3": poly_json(pi_minus),
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
            "basis": "sparse complex Fourier modes",
            "polynomialRepresentation": "sparse exponent-to-Gaussian-rational dictionary",
            "script": "compute_fourier_certificate.py",
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
        require(RESULTS.is_file(), "missing generated results.json")
        require(RESULTS.read_text(encoding="utf-8") == encoded, "results.json is stale")
    else:
        RESULTS.write_text(encoded, encoding="utf-8")
    print("R073W_FOURIER_CERTIFICATE=PASS")
    print("R073W_PRIMARY_FREQUENCY_RANK=3")
    print("R073W_PRIMARY_PRODUCTION=1/4*q^2*(1-q^2)")
    print("R073W_PRIMARY_GRADIENT_DEFECT=1/2*(1-q^2)*(13+12*q^2+10*q^4+4*q^6)")
    print("R073W_DIAGNOSTIC_2D3C_PRODUCTION=-q^2*(1-q^2)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
