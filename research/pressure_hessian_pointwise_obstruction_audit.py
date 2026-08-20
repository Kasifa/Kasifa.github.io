#!/usr/bin/env python3
"""R0.69H exact audit for the pressure-Hessian pointwise-sign obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "research/pressure_hessian_pointwise_obstruction_note.md"
AUDIT = ROOT / "research/pressure_hessian_pointwise_obstruction_audit.py"
Mode = tuple[int, int]
Series = dict[Mode, sp.Expr]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def clean(series: Series) -> Series:
    result: Series = {}
    for mode, coefficient in series.items():
        simplified = sp.simplify(coefficient)
        if simplified != 0:
            result[mode] = simplified
    return result


def add(first: Series, second: Series) -> Series:
    result = dict(first)
    for mode, coefficient in second.items():
        result[mode] = result.get(mode, sp.Integer(0)) + coefficient
    return clean(result)


def scale(series: Series, factor: sp.Expr | int) -> Series:
    return clean({mode: factor * value for mode, value in series.items()})


def derivative(series: Series, axis: int, order: int = 1) -> Series:
    return clean(
        {
            mode: coefficient * (sp.I * mode[axis]) ** order
            for mode, coefficient in series.items()
        }
    )


def multiply(first: Series, second: Series) -> Series:
    result: Series = {}
    for left_mode, left_value in first.items():
        for right_mode, right_value in second.items():
            mode = (
                left_mode[0] + right_mode[0],
                left_mode[1] + right_mode[1],
            )
            result[mode] = (
                result.get(mode, sp.Integer(0))
                + left_value * right_value
            )
    return clean(result)


def base_stream_function() -> Series:
    # -sin(x)sin(y) = (cos(x+y)-cos(x-y))/2.
    quarter = sp.Rational(1, 4)
    return {
        (1, 1): quarter,
        (-1, -1): quarter,
        (1, -1): -quarter,
        (-1, 1): -quarter,
    }


def perturbation_stream_function(m: int, n: int) -> Series:
    # (1-cos(mx))(1-cos(ny)).
    result: Series = {
        (0, 0): sp.Integer(1),
        (m, 0): -sp.Rational(1, 2),
        (-m, 0): -sp.Rational(1, 2),
        (0, n): -sp.Rational(1, 2),
        (0, -n): -sp.Rational(1, 2),
    }
    for sign_x in (-1, 1):
        for sign_y in (-1, 1):
            result[(sign_x * m, sign_y * n)] = sp.Rational(1, 4)
    return result


def velocity_coefficients(stream_function: Series) -> dict[Mode, sp.Matrix]:
    return {
        mode: sp.Matrix(
            [
                -sp.I * mode[1] * coefficient,
                sp.I * mode[0] * coefficient,
                sp.Integer(0),
            ]
        )
        for mode, coefficient in stream_function.items()
        if mode != (0, 0)
    }


def gradient_at_origin(stream_function: Series) -> sp.Matrix:
    velocity = velocity_coefficients(stream_function)
    gradient = sp.zeros(3)
    for (kx, ky), coefficient in velocity.items():
        wavevector = (kx, ky, 0)
        for i in range(3):
            for j in range(3):
                gradient[i, j] += sp.I * wavevector[j] * coefficient[i]
    return gradient.applyfunc(sp.simplify)


def divergence_residual(stream_function: Series) -> list[sp.Expr]:
    residuals = []
    for (kx, ky), coefficient in velocity_coefficients(
        stream_function
    ).items():
        residuals.append(
            sp.simplify(kx * coefficient[0] + ky * coefficient[1])
        )
    return residuals


def q_components(
    base: Series, perturbation: Series
) -> tuple[Series, Series, Series]:
    base_xx = derivative(base, 0, 2)
    base_yy = derivative(base, 1, 2)
    base_xy = derivative(derivative(base, 0), 1)
    pert_xx = derivative(perturbation, 0, 2)
    pert_yy = derivative(perturbation, 1, 2)
    pert_xy = derivative(derivative(perturbation, 0), 1)

    q_base = scale(
        add(
            multiply(base_xx, base_yy),
            scale(multiply(base_xy, base_xy), -1),
        ),
        -2,
    )
    q_cross = scale(
        add(
            add(
                multiply(base_xx, pert_yy),
                multiply(pert_xx, base_yy),
            ),
            scale(multiply(base_xy, pert_xy), -2),
        ),
        -2,
    )
    q_pert = scale(
        add(
            multiply(pert_xx, pert_yy),
            scale(multiply(pert_xy, pert_xy), -1),
        ),
        -2,
    )
    return q_base, q_cross, q_pert


def value_at_origin(series: Series) -> sp.Expr:
    return sp.simplify(sum(series.values(), sp.Integer(0)))


def pressure_hessian_component(
    source: Series, i: int, j: int
) -> sp.Expr:
    result = sp.Integer(0)
    for (kx, ky), coefficient in source.items():
        wavevector = (kx, ky, 0)
        norm_square = kx * kx + ky * ky
        if norm_square == 0:
            continue
        result -= (
            sp.Rational(wavevector[i] * wavevector[j], norm_square)
            * coefficient
        )
    return sp.simplify(result)


def matrix_checks() -> tuple[dict[str, bool], dict[str, str]]:
    s11, s22, s12, s13, s23 = sp.symbols(
        "s11 s22 s12 s13 s23", real=True
    )
    wx, wy, wz = sp.symbols("wx wy wz", real=True)
    strain = sp.Matrix(
        [
            [s11, s12, s13],
            [s12, s22, s23],
            [s13, s23, -s11 - s22],
        ]
    )
    rotation = sp.Matrix(
        [
            [0, -wz / 2, wy / 2],
            [wz / 2, 0, -wx / 2],
            [-wy / 2, wx / 2, 0],
        ]
    )
    gradient = strain + rotation
    symmetric_square = (
        gradient * gradient
        + (gradient * gradient).T
    ) / 2
    omega = sp.Matrix([wx, wy, wz])
    expected_rotation_square = (
        omega * omega.T
        - (omega.dot(omega)) * sp.eye(3)
    ) / 4

    c = sp.symbols("c", real=True)
    quadrupole = 3 * c**2 - 1
    quadrupole_mean = sp.integrate(quadrupole, (c, -1, 1)) / 2
    finite_kernel = [
        -sp.Integer(1),
        -sp.Rational(1, 4),
        sp.Rational(1, 2),
        sp.Integer(2),
    ]
    selector = [
        -sp.Rational(1, 2),
        sp.Integer(0),
        sp.Integer(0),
        sp.Rational(1, 2),
    ]
    selector_pairing = sum(
        kernel * weight
        for kernel, weight in zip(finite_kernel, selector, strict=True)
    )

    checks = {
        "symmetricGradientSquareSplitsExactly": all(
            sp.simplify(entry) == 0
            for entry in (
                symmetric_square - strain**2 - rotation**2
            )
        ),
        "rotationSquareMatchesVorticityFormula": all(
            sp.simplify(entry) == 0
            for entry in (rotation**2 - expected_rotation_square)
        ),
        "quadrupoleAngularMeanVanishes": (
            sp.simplify(quadrupole_mean) == 0
        ),
        "quadrupoleRangeIsMinusOneToTwo": (
            quadrupole.subs(c, 0) == -1
            and quadrupole.subs(c, 1) == 2
        ),
        "finiteMeanZeroSelectorRecoversHalfOscillation": (
            sum(selector) == 0
            and sum(abs(value) for value in selector) == 1
            and selector_pairing == sp.Rational(3, 2)
        ),
    }
    data = {
        "strainEquation": (
            "(D_t-Delta)S+S^2+(omega tensor omega"
            "-|omega|^2 I)/4+Hess(p)=0"
        ),
        "pressureSource": "q=tr(A^2)=|S|^2-|omega|^2/2",
        "quadrupole": "Q_e(theta)=3(e dot theta)^2-1",
        "meanZeroDuality": (
            "sup_{int g=0, ||g||_1=1}|int K g|=osc(K)/2"
        ),
    }
    return checks, data


def witness_checks() -> tuple[dict[str, bool], dict[str, object]]:
    base = base_stream_function()
    perturbations = {
        "minus": perturbation_stream_function(1, 2),
        "plus": perturbation_stream_function(2, 1),
    }
    base_gradient = gradient_at_origin(base)
    expected_gradient = sp.diag(1, -1, 0)

    records: dict[str, object] = {}
    all_divergence_free = all(
        residual == 0
        for residual in divergence_residual(base)
    )
    perturbations_divergence_free = True
    perturbation_gradients_vanish = True
    source_means_vanish = True
    pressure_trace_matches = True
    base_hxx_values: list[sp.Expr] = []
    cross_hxx_values: list[sp.Expr] = []
    perturbation_hxx_values: dict[str, sp.Expr] = {}

    for label, perturbation in perturbations.items():
        perturbations_divergence_free = (
            perturbations_divergence_free
            and all(
                residual == 0
                for residual in divergence_residual(perturbation)
            )
        )
        perturbation_gradient = gradient_at_origin(perturbation)
        perturbation_gradients_vanish = (
            perturbation_gradients_vanish
            and perturbation_gradient == sp.zeros(3)
        )

        q_base, q_cross, q_pert = q_components(base, perturbation)
        components = (q_base, q_cross, q_pert)
        source_means_vanish = source_means_vanish and all(
            source.get((0, 0), sp.Integer(0)) == 0
            for source in components
        )
        hxx = [
            pressure_hessian_component(source, 0, 0)
            for source in components
        ]
        hyy = [
            pressure_hessian_component(source, 1, 1)
            for source in components
        ]
        pressure_trace_matches = pressure_trace_matches and all(
            sp.simplify(
                hxx_value + hyy_value + value_at_origin(source)
            )
            == 0
            for source, hxx_value, hyy_value in zip(
                components, hxx, hyy, strict=True
            )
        )
        base_hxx_values.append(hxx[0])
        cross_hxx_values.append(hxx[1])
        perturbation_hxx_values[label] = hxx[2]
        records[label] = {
            "perturbationFrequencies": (
                [1, 2] if label == "minus" else [2, 1]
            ),
            "perturbationGradientAtOrigin": [
                [str(entry) for entry in row]
                for row in perturbation_gradient.tolist()
            ],
            "sourceMeanCoefficients": [
                str(source.get((0, 0), sp.Integer(0)))
                for source in components
            ],
            "sourceValuesAtOrigin": [
                str(value_at_origin(source))
                for source in components
            ],
            "pressureH11Coefficients": [str(value) for value in hxx],
            "pressureH22Coefficients": [str(value) for value in hyy],
        }

    minus_at_two = (
        base_hxx_values[0]
        + 2 * cross_hxx_values[0]
        + 4 * perturbation_hxx_values["minus"]
    )
    plus_at_two = (
        base_hxx_values[1]
        + 2 * cross_hxx_values[1]
        + 4 * perturbation_hxx_values["plus"]
    )

    checks = {
        "baseStreamFieldIsDivergenceFree": all_divergence_free,
        "perturbationFieldsAreDivergenceFree": (
            perturbations_divergence_free
        ),
        "perturbationGradientsVanishAtOrigin": (
            perturbation_gradients_vanish
        ),
        "commonLocalGradientIsDiagOneMinusOneZero": (
            base_gradient == expected_gradient
        ),
        "allPressureSourcesHaveZeroSpatialMean": source_means_vanish,
        "pressureTraceMatchesPoissonEquationAtOrigin": (
            pressure_trace_matches
        ),
        "basePressureCoefficientIsMinusOne": all(
            value == -1 for value in base_hxx_values
        ),
        "crossPressureCoefficientsVanish": all(
            value == 0 for value in cross_hxx_values
        ),
        "perturbationPressureCoefficientsAreExactOpposites": (
            perturbation_hxx_values["minus"] == -sp.Rational(54, 85)
            and perturbation_hxx_values["plus"] == sp.Rational(54, 85)
        ),
        "pressureSignsReverseAboveExactThreshold": (
            minus_at_two < 0
            and plus_at_two > 0
            and sp.Rational(85, 54) < 4
        ),
    }
    data = {
        "baseGradientAtOrigin": [
            [str(entry) for entry in row]
            for row in base_gradient.tolist()
        ],
        "exactThresholdTSquared": "85/54",
        "pressureAtTEqualsTwo": {
            "minus": str(sp.simplify(minus_at_two)),
            "plus": str(sp.simplify(plus_at_two)),
        },
        "families": records,
    }
    return checks, data


def build_payload(source_commit: str) -> dict[str, object]:
    algebra_checks, formulas = matrix_checks()
    witness_check_values, witness_data = witness_checks()
    checks = {
        key: bool(value)
        for key, value in {
            **algebra_checks,
            **witness_check_values,
        }.items()
    }
    return {
        "schemaVersion": "1.0",
        "study": "R0.69H",
        "status": "passed" if all(checks.values()) else "failed",
        "classification": (
            "rigorous pointwise-sign obstruction for pressure-Hessian "
            "closures based only on local strain and vorticity; not a "
            "Navier-Stokes regularity theorem"
        ),
        "checks": checks,
        "formulas": formulas,
        "witnessAudit": witness_data,
        "theorem": {
            "commonLocalData": (
                "S(0)=diag(1,-1,0), omega(0)=0, principal direction=e1"
            ),
            "oppositePressureFamilies": (
                "H11_minus(0)=-1-(54/85)t^2; "
                "H11_plus(0)=-1+(54/85)t^2"
            ),
            "scope": (
                "rules out only pointwise pressure-Hessian sign or closure "
                "rules that depend solely on the local pair (S,omega)"
            ),
        },
        "literatureBoundary": {
            "publishedInputs": [
                "Miller 2020 strain equation and middle-eigenvalue criterion",
                "Chevillard et al. 2011 local/nonlocal pressure Hessian",
                "Wilczek-Meneveau 2014 statistical pressure closure",
            ],
            "noveltyClaim": (
                "exact audited periodic witness and route decision only; "
                "pressure-Hessian nonlocality itself is known"
            ),
        },
        "decision": {
            "closedBranch": (
                "pointwise pressure compensation determined by local "
                "strain and vorticity"
            ),
            "nextBranch": (
                "localized strain-space orthogonality and weighted pressure "
                "commutators"
            ),
        },
        "provenance": {
            "sourceCommit": source_commit,
            "python": sys.version.split()[0],
            "sympy": sp.__version__,
            "sourceFiles": {
                str(NOTE.relative_to(ROOT)): sha256(NOTE),
                str(AUDIT.relative_to(ROOT)): sha256(AUDIT),
            },
        },
    }


def main() -> int:
    args = parse_args()
    payload = build_payload(args.source_commit)
    indent = 2 if args.pretty else None
    rendered = json.dumps(payload, indent=indent, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if (not args.check or payload["status"] == "passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
