#!/usr/bin/env python3
"""Deterministic exact-algebra certificate for R0.73Z.

The exact lane works in the finite Fourier group algebra
Q[i][A,B,r][Z^2].  Here A and B are the crossed-family amplitudes and
r=exp(-n^2 s) is the positive-scale multiplier after normalizing n=1.
The analytic notes carry all quantifiers and proofs.  This executable checks
the normalized identities, records the endpoint sequence arithmetic, and
fails closed if any source binding or stored payload drifts.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "research/r073z_covariance_certificate.json"
REPORT_PATH = ROOT / "research/r073z_covariance_certificate_report.md"
SOURCE_PATHS = (
    "research/r073z_finiteness_obstruction_and_repair.md",
    "research/r073z_finiteness_independent_audit.md",
    "research/r073z_pressure_active_kernel.md",
    "research/r073z_primary_literature_audit.md",
    "research/r073z_evidence_gap_matrix.md",
    "research/r073z_report-source.md",
)

QComplex = tuple[Fraction, Fraction]
Monomial = tuple[int, int, int]  # powers of A, B, r
Polynomial = dict[Monomial, QComplex]
Mode = tuple[int, int]
Field = dict[Mode, Polynomial]

QZERO: QComplex = (Fraction(0), Fraction(0))
QONE: QComplex = (Fraction(1), Fraction(0))
PONE: Polynomial = {(0, 0, 0): QONE}
FZERO: Field = {}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(
        value,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def qc_add(left: QComplex, right: QComplex) -> QComplex:
    return (left[0] + right[0], left[1] + right[1])


def qc_neg(value: QComplex) -> QComplex:
    return (-value[0], -value[1])


def qc_mul(left: QComplex, right: QComplex) -> QComplex:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def qc_scale(value: QComplex, scalar: Fraction) -> QComplex:
    return (value[0] * scalar, value[1] * scalar)


def qc_is_zero(value: QComplex) -> bool:
    return value == QZERO


def poly_clean(value: Polynomial) -> Polynomial:
    return {key: coefficient for key, coefficient in value.items() if not qc_is_zero(coefficient)}


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    result = dict(left)
    for key, coefficient in right.items():
        result[key] = qc_add(result.get(key, QZERO), coefficient)
    return poly_clean(result)


def poly_neg(value: Polynomial) -> Polynomial:
    return {key: qc_neg(coefficient) for key, coefficient in value.items()}


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for (a1, b1, r1), coefficient1 in left.items():
        for (a2, b2, r2), coefficient2 in right.items():
            key = (a1 + a2, b1 + b2, r1 + r2)
            result[key] = qc_add(
                result.get(key, QZERO),
                qc_mul(coefficient1, coefficient2),
            )
    return poly_clean(result)


def poly_scale(value: Polynomial, scalar: Fraction) -> Polynomial:
    return poly_clean(
        {key: qc_scale(coefficient, scalar) for key, coefficient in value.items()}
    )


def monomial(a_power: int = 0, b_power: int = 0, r_power: int = 0) -> Polynomial:
    return {(a_power, b_power, r_power): QONE}


def field_clean(value: Field) -> Field:
    return {mode: poly_clean(polynomial) for mode, polynomial in value.items() if poly_clean(polynomial)}


def field_add(left: Field, right: Field) -> Field:
    result = {mode: dict(polynomial) for mode, polynomial in left.items()}
    for mode, polynomial in right.items():
        result[mode] = poly_add(result.get(mode, {}), polynomial)
    return field_clean(result)


def field_neg(value: Field) -> Field:
    return {mode: poly_neg(polynomial) for mode, polynomial in value.items()}


def field_sub(left: Field, right: Field) -> Field:
    return field_add(left, field_neg(right))


def field_mul(left: Field, right: Field) -> Field:
    result: Field = {}
    for (k1, l1), polynomial1 in left.items():
        for (k2, l2), polynomial2 in right.items():
            mode = (k1 + k2, l1 + l2)
            result[mode] = poly_add(
                result.get(mode, {}),
                poly_mul(polynomial1, polynomial2),
            )
    return field_clean(result)


def field_scale_poly(value: Field, polynomial: Polynomial) -> Field:
    return field_clean(
        {mode: poly_mul(coefficient, polynomial) for mode, coefficient in value.items()}
    )


def field_scale_fraction(value: Field, scalar: Fraction) -> Field:
    return field_clean(
        {mode: poly_scale(polynomial, scalar) for mode, polynomial in value.items()}
    )


def field_derivative(value: Field, axis: int) -> Field:
    result: Field = {}
    for mode, polynomial in value.items():
        wave = mode[axis]
        factor: QComplex = (Fraction(0), Fraction(wave))
        result[mode] = {
            key: qc_mul(coefficient, factor)
            for key, coefficient in polynomial.items()
        }
    return field_clean(result)


def heat(value: Field) -> Field:
    result: Field = {}
    for (k, l), polynomial in value.items():
        result[(k, l)] = {
            (a_power, b_power, r_power + k * k + l * l): coefficient
            for (a_power, b_power, r_power), coefficient in polynomial.items()
        }
    return field_clean(result)


def field_sum(values: list[Field]) -> Field:
    result: Field = {}
    for value in values:
        result = field_add(result, value)
    return result


def constant_field(polynomial: Polynomial | None = None) -> Field:
    return {(0, 0): dict(PONE if polynomial is None else polynomial)}


def sin_field(k: int, l: int) -> Field:
    return {
        (k, l): {(0, 0, 0): (Fraction(0), Fraction(-1, 2))},
        (-k, -l): {(0, 0, 0): (Fraction(0), Fraction(1, 2))},
    }


def cos_field(k: int, l: int) -> Field:
    return {
        (k, l): {(0, 0, 0): (Fraction(1, 2), Fraction(0))},
        (-k, -l): {(0, 0, 0): (Fraction(1, 2), Fraction(0))},
    }


def field_square(value: Field) -> Field:
    return field_mul(value, value)


def field_equal(left: Field, right: Field) -> bool:
    return field_clean(left) == field_clean(right)


def field_is_zero(value: Field) -> bool:
    return not field_clean(value)


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def complex_json(value: QComplex) -> dict[str, str]:
    return {"real": fraction_text(value[0]), "imag": fraction_text(value[1])}


def field_json(value: Field) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for mode in sorted(field_clean(value)):
        polynomial = field_clean(value)[mode]
        terms = []
        for powers in sorted(polynomial):
            terms.append(
                {
                    "powers": {"A": powers[0], "B": powers[1], "r": powers[2]},
                    "coefficient": complex_json(polynomial[powers]),
                }
            )
        records.append({"mode": [mode[0], mode[1]], "terms": terms})
    return records


def field_hash(value: Field) -> str:
    return sha256_bytes(canonical(field_json(value)).encode("utf-8"))


def build_exact_lane() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    amplitude_a = monomial(a_power=1)
    amplitude_b = monomial(b_power=1)
    pressure_ab = monomial(a_power=1, b_power=1)

    u = [
        field_scale_poly(sin_field(0, 1), amplitude_a),
        field_scale_poly(sin_field(1, 0), amplitude_b),
        {},
    ]
    pressure = field_scale_poly(
        field_mul(cos_field(1, 0), cos_field(0, 1)),
        pressure_ab,
    )

    convection: list[Field] = []
    for component in range(3):
        terms = []
        for axis in range(2):
            terms.append(field_mul(u[axis], field_derivative(u[component], axis)))
        convection.append(field_sum(terms))
    residual = [
        field_add(convection[component], field_derivative(pressure, component))
        if component < 2
        else convection[component]
        for component in range(3)
    ]

    v = [heat(component) for component in u]
    tau: list[list[Field]] = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(field_sub(heat(field_mul(u[i], u[j])), field_mul(v[i], v[j])))
        tau.append(row)

    production_terms = []
    for i in range(3):
        for j in range(2):
            production_terms.append(field_mul(tau[i][j], field_derivative(v[i], j)))
    production = field_neg(field_sum(production_terms))

    absolute_u_squared = field_sum([field_square(component) for component in u])
    filtered_absolute_u_squared = heat(absolute_u_squared)
    filtered_second = [
        [heat(field_mul(u[i], u[j])) for j in range(3)]
        for i in range(3)
    ]
    velocity_square_filtered = field_sum([field_square(component) for component in v])

    third_flux: list[Field] = []
    for j in range(3):
        term = heat(field_mul(absolute_u_squared, u[j]))
        term = field_sub(term, field_mul(filtered_absolute_u_squared, v[j]))
        correction = field_sum(
            [field_mul(filtered_second[i][j], v[i]) for i in range(3)]
        )
        term = field_sub(term, field_scale_fraction(correction, Fraction(2)))
        term = field_add(
            term,
            field_scale_fraction(
                field_mul(velocity_square_filtered, v[j]),
                Fraction(2),
            ),
        )
        third_flux.append(field_scale_fraction(term, Fraction(1, 2)))
    divergence_third_flux = field_sum(
        [field_derivative(third_flux[axis], axis) for axis in range(2)]
    )
    centered_production = field_sub(production, divergence_third_flux)

    filtered_pressure = heat(pressure)
    pressure_covariance = [
        field_sub(heat(field_mul(pressure, u[i])), field_mul(filtered_pressure, v[i]))
        for i in range(3)
    ]

    q1_expected = field_scale_poly(
        field_mul(cos_field(1, 0), sin_field(0, 2)),
        poly_scale(
            poly_add(monomial(2, 1, 5), poly_neg(monomial(2, 1, 3))),
            Fraction(1, 2),
        ),
    )
    q2_expected = field_scale_poly(
        field_mul(sin_field(2, 0), cos_field(0, 1)),
        poly_scale(
            poly_add(monomial(1, 2, 5), poly_neg(monomial(1, 2, 3))),
            Fraction(1, 2),
        ),
    )

    gradient_energy = field_sum(
        [
            field_square(field_derivative(u[i], axis))
            for i in range(3)
            for axis in range(2)
        ]
    )
    filtered_gradient_energy = heat(gradient_energy)
    resolved_gradient_energy = field_sum(
        [
            field_square(field_derivative(v[i], axis))
            for i in range(3)
            for axis in range(2)
        ]
    )
    gradient_covariance = field_sub(filtered_gradient_energy, resolved_gradient_energy)

    d_expected = field_sum(
        [
            constant_field(
                poly_scale(
                    poly_add(monomial(2, 0, 0), poly_neg(monomial(2, 0, 2))),
                    Fraction(1, 2),
                )
            ),
            field_scale_poly(
                cos_field(0, 2),
                poly_scale(
                    poly_add(monomial(2, 0, 4), poly_neg(monomial(2, 0, 2))),
                    Fraction(1, 2),
                ),
            ),
            constant_field(
                poly_scale(
                    poly_add(monomial(0, 2, 0), poly_neg(monomial(0, 2, 2))),
                    Fraction(1, 2),
                )
            ),
            field_scale_poly(
                cos_field(2, 0),
                poly_scale(
                    poly_add(monomial(0, 2, 4), poly_neg(monomial(0, 2, 2))),
                    Fraction(1, 2),
                ),
            ),
        ]
    )

    subfilter_energy = field_scale_fraction(
        field_sub(filtered_absolute_u_squared, velocity_square_filtered),
        Fraction(1, 2),
    )
    k_expected = field_sum(
        [
            constant_field(
                poly_scale(
                    poly_add(monomial(2, 0, 0), poly_neg(monomial(2, 0, 2))),
                    Fraction(1, 4),
                )
            ),
            field_scale_poly(
                cos_field(0, 2),
                poly_scale(
                    poly_add(monomial(2, 0, 2), poly_neg(monomial(2, 0, 4))),
                    Fraction(1, 4),
                ),
            ),
            constant_field(
                poly_scale(
                    poly_add(monomial(0, 2, 0), poly_neg(monomial(0, 2, 2))),
                    Fraction(1, 4),
                )
            ),
            field_scale_poly(
                cos_field(2, 0),
                poly_scale(
                    poly_add(monomial(0, 2, 2), poly_neg(monomial(0, 2, 4))),
                    Fraction(1, 4),
                ),
            ),
        ]
    )

    raw_checks = [
        ("nse_residual_zero", all(field_is_zero(value) for value in residual)),
        ("cross_stress_tau12_zero", field_is_zero(tau[0][1]) and field_is_zero(tau[1][0])),
        ("signed_production_zero", field_is_zero(production)),
        ("third_central_flux_divergence_zero", field_is_zero(divergence_third_flux)),
        ("centered_production_zero", field_is_zero(centered_production)),
        ("pressure_covariance_q1_formula", field_equal(pressure_covariance[0], q1_expected)),
        ("pressure_covariance_q2_formula", field_equal(pressure_covariance[1], q2_expected)),
        ("pressure_covariance_q3_zero", field_is_zero(pressure_covariance[2])),
        ("pressure_covariance_nonzero", not field_is_zero(pressure_covariance[0])),
        ("gradient_covariance_formula", field_equal(gradient_covariance, d_expected)),
        ("gradient_covariance_nonzero", not field_is_zero(gradient_covariance)),
        ("subfilter_energy_formula", field_equal(subfilter_energy, k_expected)),
    ]
    checks = [{"id": identifier, "pass": passed} for identifier, passed in raw_checks]
    for check in checks:
        require(bool(check["pass"]), "exact check failed: " + str(check["id"]))

    hashes = {
        "gradient_covariance": field_hash(gradient_covariance),
        "pressure_covariance_q1": field_hash(pressure_covariance[0]),
        "pressure_covariance_q2": field_hash(pressure_covariance[1]),
        "subfilter_energy": field_hash(subfilter_energy),
        "third_central_flux_x": field_hash(third_flux[0]),
        "third_central_flux_y": field_hash(third_flux[1]),
    }
    inventory = {
        "gradientCovarianceModeCount": len(gradient_covariance),
        "pressureCovarianceQ1ModeCount": len(pressure_covariance[0]),
        "pressureCovarianceQ2ModeCount": len(pressure_covariance[1]),
        "subfilterEnergyModeCount": len(subfilter_energy),
    }
    return checks, {"field_hashes": hashes, "inventory": inventory}


def build_endpoint_lane() -> dict[str, Any]:
    records = []
    partial_l2 = Fraction(0)
    partial_divergence = 0
    for index in range(1, 17):
        frequency = 8**index
        amplitude = Fraction(1, 2**index)
        partial_l2 += amplitude * amplitude
        cubic_frequency = amplitude**3 * frequency
        require(cubic_frequency == 1, "lacunary arithmetic drift")
        partial_divergence += 1
        records.append(
            {
                "index": index,
                "frequency": frequency,
                "amplitude": fraction_text(amplitude),
                "amplitudeCubedTimesFrequency": fraction_text(cubic_frequency),
                "partialL2CoefficientSum": fraction_text(partial_l2),
                "partialDivergenceUnitSum": partial_divergence,
            }
        )
    require(partial_l2 < Fraction(1, 3) + Fraction(1, 10**12), "unexpected L2 sum")
    return {
        "highFrequencyEnergyNormalizedByPiCubed": {
            "supremumL2Squared": 4,
            "viscousIntegratedGradientSquared": 2,
            "total": 6,
            "independentOfFrequency": True,
        },
        "lacunaryDefinition": {
            "frequency": "N_j=8^j",
            "amplitude": "a_j=2^(-j)=N_j^(-1/3)",
            "l2CoefficientSeriesLimit": "1/3",
            "divergentLowerBoundTerm": "a_j^3 N_j=1",
        },
        "partialSums": records,
    }


def build_payload() -> dict[str, Any]:
    source_bindings = []
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        require(path.is_file(), "source binding missing: " + relative)
        source_bindings.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": sha256_path(path),
            }
        )
    exact_checks, exact_artifacts = build_exact_lane()
    payload: dict[str, Any] = {
        "schema": "r073z-covariance-certificate-v1",
        "release": "R0.73Z",
        "status": "PASS",
        "source_bindings": source_bindings,
        "exact_lane": {
            "algebra": "Q[i][A,B,r][Z^2]",
            "normalization": "n=1; general n and physical-time amplitudes are analytic-note quantifiers",
            "checks": exact_checks,
            **exact_artifacts,
        },
        "endpoint_lane": build_endpoint_lane(),
        "claim_boundary": {
            "analyticNotesCarryProof": True,
            "certificateRole": "exact normalized algebra and arithmetic cross-check",
            "interiorSuitableWeakFiniteness": "OPEN",
            "localCknCoercivity": "OPEN",
            "epsilonRegularity": "OPEN",
            "globalRegularity": "OPEN",
            "clayProblemSolved": False,
            "notClay": True,
        },
    }
    payload["payload_sha256"] = sha256_bytes(canonical(payload).encode("utf-8"))
    return payload


def report_text(payload: dict[str, Any]) -> str:
    checks = payload["exact_lane"]["checks"]
    lines = [
        "# R0.73Z covariance certificate report",
        "",
        "**Status:** PASS",
        "",
        "**Role:** exact normalized Fourier-algebra and lacunary-arithmetic",
        "cross-check.  The analytic notes carry the proofs and quantifiers.",
        "",
        "## Exact crossed-family checks",
        "",
    ]
    for check in checks:
        lines.append(f"- {check['id']}: PASS")
    lines.extend(
        [
            "",
            "The exact lane uses the finite group algebra",
            r"\(\mathbb Q[i][A,B,r][\mathbb Z^2]\), with",
            r"\(r=e^{-n^2s}\) after normalizing \(n=1\).",
            "",
            "It verifies the Navier--Stokes residual, zero cross stress, zero",
            "signed production, zero centered production, the two explicit",
            "pressure-covariance components, the gradient-covariance formula,",
            "and the subfilter-energy formula.",
            "",
            "## Endpoint arithmetic",
            "",
            r"The smooth one-mode energy, normalized by \(\pi^3\), is",
            r"\(4+2=6\), independent of frequency.  For the exact lacunary",
            r"choice \(N_j=8^j\), \(a_j=2^{-j}\),",
            r"\(\sum_j a_j^2=1/3\) while \(a_j^3N_j=1\) for every \(j\).",
            "Thus the executable reproduces the finite-energy/divergent-lower-",
            "sum arithmetic used in the analytic proof.",
            "",
            "## Claim boundary",
            "",
            "- No numerical result is used as proof.",
            "- Interior suitable-weak finiteness remains open.",
            "- Local CKN coercivity and epsilon regularity remain open.",
            "- This certificate does not solve the Clay problem.",
            "",
            f"Payload SHA-256: {payload['payload_sha256']}",
            "",
            "**NOT CLAY.**",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    payload = build_payload()
    report = report_text(payload)
    if args.check_only:
        require(RESULT_PATH.is_file(), "stored result missing")
        require(REPORT_PATH.is_file(), "stored report missing")
        stored = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
        require(canonical(stored) == canonical(payload), "stored result drift")
        require(REPORT_PATH.read_text(encoding="utf-8") == report, "stored report drift")
        print(
            "PASS: R0.73Z covariance certificate "
            f"({len(payload['exact_lane']['checks'])} exact checks)"
        )
        return

    RESULT_PATH.write_text(canonical(payload), encoding="utf-8")
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(
        "PASS: wrote R0.73Z covariance certificate "
        f"({len(payload['exact_lane']['checks'])} exact checks)"
    )


if __name__ == "__main__":
    main()
