#!/usr/bin/env python3
"""Rebuild the exact finite R0.73T no-go witnesses.

Every mathematical value is evaluated with fractions.Fraction.  The script
uses no floating point, third-party package, network service, GPU, or DGX.
It exits nonzero if an identity or the fixed audit checklist fails.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CHECKLIST_PATH = HERE / "audit-checklist.json"
RESULTS_PATH = HERE / "results.json"

F = Fraction
Mode = tuple[int, int, int]
Gaussian = tuple[Fraction, Fraction]
CVector = tuple[Gaussian, Gaussian, Gaussian]

ZERO: Gaussian = (F(0), F(0))
I_UNIT: Gaussian = (F(0), F(1))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        require(key not in output, "duplicate JSON key: " + key)
        output[key] = value
    return output


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: Fraction | int) -> str:
    return str(F(value))


def mode_key(mode: Mode) -> str:
    return ",".join(str(value) for value in mode)


def add_mode(left: Mode, right: Mode) -> Mode:
    return tuple(left[index] + right[index] for index in range(3))  # type: ignore[return-value]


def negate_mode(mode: Mode) -> Mode:
    return tuple(-value for value in mode)  # type: ignore[return-value]


def mode_dot(left: Mode, right: Mode) -> int:
    return sum(left[index] * right[index] for index in range(3))


def z(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    return F(real), F(imag)


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gneg(value: Gaussian) -> Gaussian:
    return -value[0], -value[1]


def gsub(left: Gaussian, right: Gaussian) -> Gaussian:
    return gadd(left, gneg(right))


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gscale(value: Gaussian, scalar: int | Fraction) -> Gaussian:
    factor = F(scalar)
    return value[0] * factor, value[1] * factor


def gdivide(value: Gaussian, scalar: int | Fraction) -> Gaussian:
    denominator = F(scalar)
    require(denominator != 0, "Gaussian division by zero")
    return value[0] / denominator, value[1] / denominator


def gconj(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def gabs2(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def gzero(value: Gaussian) -> bool:
    return value == ZERO


def gjson(value: Gaussian) -> dict[str, str]:
    return {"im": q(value[1]), "re": q(value[0])}


def vconj(vector: CVector) -> CVector:
    return tuple(gconj(value) for value in vector)  # type: ignore[return-value]


def vdot(left: CVector, right: CVector, conjugate_right: bool = False) -> Gaussian:
    total = ZERO
    for left_value, right_value in zip(left, right):
        if conjugate_right:
            right_value = gconj(right_value)
        total = gadd(total, gmul(left_value, right_value))
    return total


def mode_vector_dot(mode: Mode, vector: CVector) -> Gaussian:
    total = ZERO
    for scalar, value in zip(mode, vector):
        total = gadd(total, gscale(value, scalar))
    return total


def vjson(vector: CVector) -> list[dict[str, str]]:
    return [gjson(value) for value in vector]


def clean_scalar(values: dict[Mode, Gaussian]) -> dict[Mode, Gaussian]:
    return {mode: value for mode, value in values.items() if not gzero(value)}


def scalar_json(values: dict[Mode, Gaussian], real_only: bool = False) -> dict[str, object]:
    output: dict[str, object] = {}
    for mode, value in sorted(values.items()):
        if real_only:
            require(value[1] == 0, "expected real coefficient at " + mode_key(mode))
            output[mode_key(mode)] = q(value[0])
        else:
            output[mode_key(mode)] = gjson(value)
    return output


def velocity_json(velocity: dict[Mode, CVector]) -> dict[str, object]:
    return {mode_key(mode): vjson(vector) for mode, vector in sorted(velocity.items())}


def conjugate_completion(positive: dict[Mode, CVector]) -> dict[Mode, CVector]:
    output = dict(positive)
    for mode, vector in positive.items():
        negative = negate_mode(mode)
        require(negative not in output, "positive support contains a conjugate collision")
        output[negative] = vconj(vector)
    return output


def reality_check(velocity: dict[Mode, CVector]) -> bool:
    return all(
        negate_mode(mode) in velocity
        and velocity[negate_mode(mode)] == vconj(vector)
        for mode, vector in velocity.items()
    )


def divergence_check(velocity: dict[Mode, CVector]) -> bool:
    return all(gzero(mode_vector_dot(mode, vector)) for mode, vector in velocity.items())


def autocorrelation_shifted(velocity: dict[Mode, CVector]) -> dict[Mode, Gaussian]:
    output: dict[Mode, Gaussian] = {}
    for left_mode, left_vector in velocity.items():
        for right_mode, right_vector in velocity.items():
            shift = add_mode(left_mode, negate_mode(right_mode))
            value = vdot(left_vector, right_vector, conjugate_right=True)
            output[shift] = gadd(output.get(shift, ZERO), value)
    return clean_scalar(output)


def modulus_squared_coefficients(velocity: dict[Mode, CVector]) -> dict[Mode, Gaussian]:
    output: dict[Mode, Gaussian] = {}
    for left_mode, left_vector in velocity.items():
        for right_mode, right_vector in velocity.items():
            mode = add_mode(left_mode, right_mode)
            value = vdot(left_vector, right_vector)
            output[mode] = gadd(output.get(mode, ZERO), value)
    return clean_scalar(output)


def pressure_coefficients(velocity: dict[Mode, CVector]) -> dict[Mode, Gaussian]:
    """Return p-hat for Delta p = -partial_i partial_j(u_i u_j)."""
    output: dict[Mode, Gaussian] = {}
    for left_mode, left_vector in velocity.items():
        for right_mode, right_vector in velocity.items():
            mode = add_mode(left_mode, right_mode)
            norm_squared = mode_dot(mode, mode)
            if norm_squared == 0:
                continue
            contraction = gmul(
                mode_vector_dot(mode, left_vector),
                mode_vector_dot(mode, right_vector),
            )
            contribution = gneg(gdivide(contraction, norm_squared))
            output[mode] = gadd(output.get(mode, ZERO), contribution)
    return clean_scalar(output)


def gradient_energy_coefficients(velocity: dict[Mode, CVector]) -> dict[Mode, Gaussian]:
    output: dict[Mode, Gaussian] = {}
    for left_mode, left_vector in velocity.items():
        for right_mode, right_vector in velocity.items():
            mode = add_mode(left_mode, right_mode)
            contribution = gscale(
                vdot(left_vector, right_vector),
                -mode_dot(left_mode, right_mode),
            )
            output[mode] = gadd(output.get(mode, ZERO), contribution)
    return clean_scalar(output)


def advective_coefficients(velocity: dict[Mode, CVector]) -> dict[Mode, CVector]:
    output: dict[Mode, list[Gaussian]] = {}
    for left_mode, left_vector in velocity.items():
        for right_mode, right_vector in velocity.items():
            mode = add_mode(left_mode, right_mode)
            multiplier = gmul(I_UNIT, mode_vector_dot(right_mode, left_vector))
            contribution = [gmul(multiplier, value) for value in right_vector]
            if mode not in output:
                output[mode] = [ZERO, ZERO, ZERO]
            output[mode] = [
                gadd(output[mode][index], contribution[index])
                for index in range(3)
            ]
    return {
        mode: tuple(vector)  # type: ignore[arg-type]
        for mode, vector in output.items()
        if any(not gzero(value) for value in vector)
    }


def pressure_work(
    velocity: dict[Mode, CVector],
    correlation: dict[Mode, Gaussian],
    pressure: dict[Mode, Gaussian],
) -> Gaussian:
    total = ZERO
    for velocity_mode, vector in velocity.items():
        for pressure_mode, pressure_value in pressure.items():
            correlation_mode = negate_mode(add_mode(velocity_mode, pressure_mode))
            correlation_value = correlation.get(correlation_mode, ZERO)
            derivative_pairing = gmul(
                I_UNIT,
                gmul(pressure_value, mode_vector_dot(pressure_mode, vector)),
            )
            total = gadd(total, gmul(correlation_value, derivative_pairing))
    return total


def odd_energy_density_evolution(
    velocity: dict[Mode, CVector],
    correlation: dict[Mode, Gaussian],
    pressure: dict[Mode, Gaussian],
) -> dict[Mode, Gaussian]:
    """Return -u.grad(|u|^2)-2u.grad(p), the part odd under u -> -u."""
    output: dict[Mode, Gaussian] = {}
    for velocity_mode, vector in velocity.items():
        for scalar_mode, scalar_value in correlation.items():
            mode = add_mode(velocity_mode, scalar_mode)
            term = gmul(
                I_UNIT,
                gmul(mode_vector_dot(scalar_mode, vector), scalar_value),
            )
            output[mode] = gsub(output.get(mode, ZERO), term)
        for scalar_mode, scalar_value in pressure.items():
            mode = add_mode(velocity_mode, scalar_mode)
            term = gscale(
                gmul(
                    I_UNIT,
                    gmul(mode_vector_dot(scalar_mode, vector), scalar_value),
                ),
                2,
            )
            output[mode] = gsub(output.get(mode, ZERO), term)
    return clean_scalar(output)


def scalar_product_constant(
    left: dict[Mode, Gaussian], right: dict[Mode, Gaussian]
) -> Gaussian:
    total = ZERO
    for mode, value in left.items():
        total = gadd(total, gmul(value, right.get(negate_mode(mode), ZERO)))
    return total


def group_q_heat(correlation: dict[Mode, Gaussian]) -> dict[str, str]:
    groups: dict[int, Fraction] = {}
    for mode, value in correlation.items():
        norm_squared = mode_dot(mode, mode)
        groups[norm_squared] = groups.get(norm_squared, F(0)) + gabs2(value)
    return {str(key): q(value) for key, value in sorted(groups.items())}


def group_a_heat(correlation: dict[Mode, Gaussian]) -> dict[str, str]:
    groups: dict[int, Fraction] = {}
    for mode, value in correlation.items():
        require(value[1] == 0, "A_tau grouping expects real six-mode C")
        norm_squared = mode_dot(mode, mode)
        groups[norm_squared] = groups.get(norm_squared, F(0)) + abs(value[0])
    return {str(key): q(value) for key, value in sorted(groups.items())}


def group_signed_heat_derivative_difference(
    correlation: dict[Mode, Gaussian], odd_part: dict[Mode, Gaussian]
) -> dict[str, str]:
    groups: dict[int, Fraction] = {}
    for mode, correlation_value in correlation.items():
        product = gmul(odd_part.get(mode, ZERO), gconj(correlation_value))
        require(product[1] == 0, "weighted signed derivative group is not real")
        norm_squared = mode_dot(mode, mode)
        groups[norm_squared] = groups.get(norm_squared, F(0)) + 4 * product[0]
    return {
        str(key): q(value)
        for key, value in sorted(groups.items())
        if value != 0
    }


def six_mode_velocity() -> dict[Mode, CVector]:
    return conjugate_completion({
        (1, 0, 0): (z(), z(0, -2), z()),
        (0, 1, 0): (z(0, -3), z(), z()),
        (1, 1, 0): (z(0, 2), z(0, -2), z()),
    })


def simple_shear_velocity() -> dict[Mode, CVector]:
    return conjugate_completion({
        (1, 0, 0): (z(), z(0, F(-1, 2)), z()),
    })


def rotating_shear_velocity() -> dict[Mode, CVector]:
    return conjugate_completion({
        (1, 0, 0): (z(), z(F(1, 2)), z(0, F(-1, 2))),
    })


def field_invariants(velocity: dict[Mode, CVector]) -> dict[str, object]:
    shifted = autocorrelation_shifted(velocity)
    product = modulus_squared_coefficients(velocity)
    require(shifted == product, "shifted autocorrelation/product convolution mismatch")
    pressure = pressure_coefficients(velocity)
    gradient_energy = gradient_energy_coefficients(velocity)
    work = pressure_work(velocity, shifted, pressure)
    require(work[1] == 0, "pressure work is not real")
    x_squared = sum(F(mode_dot(mode, mode)) * gabs2(value) for mode, value in shifted.items())
    y_value = scalar_product_constant(shifted, gradient_energy)
    require(y_value[1] == 0, "Y is not real")
    energy = shifted.get((0, 0, 0), ZERO)
    require(energy[1] == 0, "energy is not real")
    q_value = sum(gabs2(value) for value in shifted.values())
    if all(value[1] == 0 for value in shifted.values()):
        a_value: str | None = q(sum(abs(value[0]) for value in shifted.values()))
    else:
        a_value = None
    return {
        "autocorrelation": shifted,
        "autocorrelationA": a_value,
        "autocorrelationQ": q(q_value),
        "autocorrelationSupport": len(shifted),
        "divergenceFree": divergence_check(velocity),
        "energy": q(energy[0]),
        "gradientEnergy": gradient_energy,
        "meanZero": (0, 0, 0) not in velocity,
        "modeCount": len(velocity),
        "pressure": pressure,
        "pressureWorkJ": q(work[0]),
        "realConjugacy": reality_check(velocity),
        "velocity": velocity,
        "xSquared": q(x_squared),
        "y": q(y_value[0]),
    }


def six_mode_record() -> dict[str, object]:
    values = field_invariants(six_mode_velocity())
    correlation = values["autocorrelation"]
    pressure = values["pressure"]
    velocity = values["velocity"]
    require(isinstance(correlation, dict), "internal correlation type drift")
    require(isinstance(pressure, dict), "internal pressure type drift")
    require(isinstance(velocity, dict), "internal velocity type drift")
    odd_part = odd_energy_density_evolution(velocity, correlation, pressure)
    nonlinear = -4 * F(str(values["pressureWorkJ"]))
    viscous_coefficient = -4 * F(str(values["y"])) - 2 * F(str(values["xSquared"]))
    return {
        "annulus": {
            "baseNormSquared": sorted({mode_dot(mode, mode) for mode in velocity}),
            "scaledMax": "sqrt(2)*L",
            "scaledMin": "L",
        },
        "autocorrelation": {
            "coefficients": scalar_json(correlation, real_only=True),
            "definitionAgreement": True,
            "siteCount": values["autocorrelationSupport"],
        },
        "dilation": {
            "autocorrelation": "C_L(L*h)=C(h); C_L(n)=0 for n not in L*Z^3",
            "minusUNonlinearPressure": q(-nonlinear) + "*L",
            "qDerivativeDifference": q(2 * nonlinear) + "*L",
            "qDerivativeMinusU": q(viscous_coefficient) + "*nu*L^2+" + q(-nonlinear) + "*L",
            "qDerivativeU": q(viscous_coefficient) + "*nu*L^2" + q(nonlinear) + "*L",
            "uNonlinearPressure": q(nonlinear) + "*L",
        },
        "finiteIdentities": {
            "A": values["autocorrelationA"],
            "D_C": values["autocorrelationSupport"],
            "E": values["energy"],
            "J": values["pressureWorkJ"],
            "N4": q(nonlinear),
            "N4MinusU": q(-nonlinear),
            "Q": values["autocorrelationQ"],
            "X2": values["xSquared"],
            "Y": values["y"],
            "viscousQDerivativeCoefficient": q(viscous_coefficient),
        },
        "heatWeights": {
            "aTauByNormSquared": group_a_heat(correlation),
            "aTauFormula": "sum_m a_m*exp(-tau*m)",
            "qTauByNormSquared": group_q_heat(correlation),
            "qTauFormula": "sum_m q_m*exp(-2*tau*m)",
            "signedDerivativeDifferenceByNormSquared":
                group_signed_heat_derivative_difference(correlation, odd_part),
            "signedDerivativeDifferenceFormula":
                "sum_m d_m*exp(-2*tau*m)",
            "scaledSignedDerivativeDifference": "-768*L*exp(-8*tau*L^2)",
        },
        "physicalField": [
            "6*sin(x2)-4*sin(x1+x2)",
            "4*sin(x1)+4*sin(x1+x2)",
            "0",
        ],
        "pressure": {
            "coefficients": scalar_json(pressure, real_only=True),
            "fourierFormula":
                "p_hat(n)=-(n_i*n_j/|n|^2)*sum_k u_hat_i(k)*u_hat_j(n-k)",
            "siteCount": len(pressure),
        },
        "velocity": {
            "coefficients": velocity_json(velocity),
            "divergenceFree": values["divergenceFree"],
            "meanZero": values["meanZero"],
            "realConjugacy": values["realConjugacy"],
            "siteCount": values["modeCount"],
        },
    }


def simple_shear_record() -> dict[str, object]:
    values = field_invariants(simple_shear_velocity())
    correlation = values["autocorrelation"]
    pressure = values["pressure"]
    velocity = values["velocity"]
    require(isinstance(correlation, dict), "simple shear C type drift")
    require(isinstance(pressure, dict), "simple shear pressure type drift")
    require(isinstance(velocity, dict), "simple shear velocity type drift")
    require(not pressure, "simple shear pressure must vanish")
    require(not advective_coefficients(velocity), "simple shear advection must vanish")
    q_value = F(str(values["autocorrelationQ"]))
    viscous_coefficient = -4 * F(str(values["y"])) - 2 * F(str(values["xSquared"]))
    evolution_exponent = viscous_coefficient / q_value
    return {
        "advectionZero": True,
        "autocorrelationAtL1": scalar_json(correlation, real_only=True),
        "dilationFormula": "C_L(0)=1/2; C_L(plus_or_minus_2L*e1)=-1/4",
        "exactSolution": "s_L(t)=exp(-nu*L^2*t)*s_L(0)",
        "field": ["0", "sin(L*x1)", "0"],
        "finiteIdentities": {
            "A": values["autocorrelationA"],
            "D_C": values["autocorrelationSupport"],
            "E": values["energy"],
            "N4": "0",
            "Q": values["autocorrelationQ"],
            "X2AtL1": values["xSquared"],
            "YAtL1": values["y"],
        },
        "pressureZero": True,
        "qDerivative": q(viscous_coefficient) + "*nu*L^2",
        "qEvolution": q(q_value) + "*exp(" + q(evolution_exponent) + "*nu*L^2*t)",
        "velocityChecks": {
            "divergenceFree": values["divergenceFree"],
            "meanZero": values["meanZero"],
            "realConjugacy": values["realConjugacy"],
            "siteCount": values["modeCount"],
        },
    }


def rotating_shear_record() -> dict[str, object]:
    values = field_invariants(rotating_shear_velocity())
    correlation = values["autocorrelation"]
    pressure = values["pressure"]
    velocity = values["velocity"]
    require(isinstance(correlation, dict), "rotating shear C type drift")
    require(isinstance(pressure, dict), "rotating shear pressure type drift")
    require(isinstance(velocity, dict), "rotating shear velocity type drift")
    require(not pressure, "rotating shear pressure must vanish")
    require(not advective_coefficients(velocity), "rotating shear advection must vanish")
    q_value = F(str(values["autocorrelationQ"]))
    viscous_coefficient = -4 * F(str(values["y"])) - 2 * F(str(values["xSquared"]))
    evolution_exponent = viscous_coefficient / q_value
    gradient_energy = values["gradientEnergy"]
    require(isinstance(gradient_energy, dict), "rotating shear gradient type drift")
    gradient_zero = gradient_energy.get((0, 0, 0), ZERO)
    require(gradient_zero[1] == 0, "rotating shear gradient energy is not real")
    c0_derivative_coefficient = -2 * gradient_zero[0]
    return {
        "advectionZero": True,
        "autocorrelationAtN1": scalar_json(correlation, real_only=True),
        "c0Derivative": q(c0_derivative_coefficient) + "*nu*N^2",
        "completeAutocorrelation": "C_N(h)=1 if h=0, otherwise 0",
        "exactSolution": "v_N(t)=exp(-nu*N^2*t)*v_N(0)",
        "field": ["0", "cos(N*x1)", "sin(N*x1)"],
        "finiteIdentities": {
            "A": values["autocorrelationA"],
            "D_C": values["autocorrelationSupport"],
            "E": values["energy"],
            "N4": "0",
            "Q": values["autocorrelationQ"],
            "X2AtN1": values["xSquared"],
            "YAtN1": values["y"],
        },
        "pressureZero": True,
        "qDerivative": q(viscous_coefficient) + "*nu*N^2",
        "qEvolution": q(q_value) + "*exp(" + q(evolution_exponent) + "*nu*N^2*t)",
        "velocityChecks": {
            "divergenceFree": values["divergenceFree"],
            "meanZero": values["meanZero"],
            "realConjugacy": values["realConjugacy"],
            "siteCount": values["modeCount"],
        },
    }


def get_path(value: object, path: str) -> object:
    current = value
    for segment in path.split("."):
        require(isinstance(current, dict), "check path enters non-object at " + segment)
        require(segment in current, "missing check path: " + path)
        current = current[segment]
    return current


def load_checklist() -> dict[str, Any]:
    require(CHECKLIST_PATH.is_file() and not CHECKLIST_PATH.is_symlink(),
            "missing regular audit checklist")
    value = json.loads(
        CHECKLIST_PATH.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
    )
    require(isinstance(value, dict), "audit checklist root must be an object")
    require(value.get("schemaVersion") == 1, "audit checklist schema drift")
    checks = value.get("requiredChecks")
    require(isinstance(checks, list) and checks, "audit checklist has no checks")
    identifiers = [check.get("id") for check in checks if isinstance(check, dict)]
    require(len(identifiers) == len(checks), "audit checklist contains a non-object check")
    require(len(set(identifiers)) == len(identifiers), "duplicate audit check id")
    return value


def build_results() -> dict[str, object]:
    checklist = load_checklist()
    core: dict[str, object] = {
        "arithmetic": "Python standard-library fractions.Fraction; no floating point",
        "certificate": "R0.73T exact dynamic-autocorrelation no-go witnesses",
        "normalization": {
            "domain": "T^3=[0,2*pi]^3",
            "fourier": "f_hat(k)=integral f(x)*exp(-i*k.x) dmu",
            "measure": "normalized Haar probability measure",
            "navierStokes":
                "partial_t u+(u.grad)u+grad p=nu*Delta u; div u=0",
        },
        "rotatingShear": rotating_shear_record(),
        "schemaVersion": 1,
        "simpleShear": simple_shear_record(),
        "sixMode": six_mode_record(),
    }
    checks: list[dict[str, object]] = []
    for specification in checklist["requiredChecks"]:
        require(isinstance(specification, dict), "invalid check specification")
        check_id = specification.get("id")
        path = specification.get("path")
        require(isinstance(check_id, str) and check_id, "check id is invalid")
        require(isinstance(path, str) and path, "check path is invalid")
        actual = get_path(core, path)
        expected = specification.get("expected")
        passed = actual == expected
        checks.append({
            "actual": actual,
            "expected": expected,
            "id": check_id,
            "pass": passed,
            "path": path,
        })
    require(all(bool(check["pass"]) for check in checks), "fixed audit checklist failed")
    core["audit"] = {
        "checklistPath": CHECKLIST_PATH.relative_to(ROOT).as_posix(),
        "checklistSha256": sha256(CHECKLIST_PATH),
        "passed": len(checks),
        "required": len(checks),
        "results": checks,
    }
    core["producer"] = {
        "gpu": "not used",
        "network": "not used",
        "scriptPath": Path(__file__).resolve().relative_to(ROOT).as_posix(),
        "scriptSha256": sha256(Path(__file__).resolve()),
        "standardLibraryOnly": True,
    }
    return core


def parse_arguments(arguments: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="recompute and require byte-equivalent JSON content without writing",
    )
    return parser.parse_args(list(arguments))


def main(arguments: Iterable[str] | None = None) -> int:
    options = parse_arguments(sys.argv[1:] if arguments is None else arguments)
    results = build_results()
    rendered = canonical(results)
    if options.check_only:
        require(RESULTS_PATH.is_file() and not RESULTS_PATH.is_symlink(),
                "missing regular results.json")
        require(RESULTS_PATH.read_text(encoding="utf-8") == rendered,
                "results.json differs from exact reconstruction")
        print(
            "R073T_EXACT_CERTIFICATE=PASS mode=check-only "
            f"checks={results['audit']['passed']}/{results['audit']['required']}"
        )
        return 0
    RESULTS_PATH.write_text(rendered, encoding="utf-8")
    print(
        "R073T_EXACT_CERTIFICATE=PASS mode=write "
        f"checks={results['audit']['passed']}/{results['audit']['required']} "
        f"output={RESULTS_PATH.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"R073T_EXACT_CERTIFICATE=FAIL {error}", file=sys.stderr)
        raise SystemExit(1)
