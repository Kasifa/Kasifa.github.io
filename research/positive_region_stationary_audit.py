#!/usr/bin/env python3
"""Compactify and audit the positive stationary region from R0.18.

The antisymmetric fifth-order model has the target fraction

    S(p,q,x) = T(p,q,x) / (T(p,q,x) + E(p,q,x)),

where ``T`` and ``E`` are exact rational polynomials.  Maximizing ``S`` is
equivalent to minimizing the external/target quotient used in R0.18.  This
script starts the global finite-model audit by compactifying the full positive
orthant with

    u = p/(1+p),  v = q/(1+q),  w = x/(1+x).

Thus positive finite parameters lie in the open unit cube and the six faces
represent zero or infinity in one chart variable.  The script reconstructs
the exact polynomials, records their boundary valuations and leading forms,
and optionally writes a compressed exact coefficient cache for later root
enumeration.  Numerical scans based on that cache generate candidates only;
they are not completeness proofs.

This remains a finite fifth-order algebraic calculation.  It does not control
a Taylor remainder or prove a Navier--Stokes regularity or singularity result.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time
import sympy as sp

import antisymmetric_symbolic_quotient_audit as anti


EXPECTED_DIGESTS = {
    "target": "9ee7c5be4b4efcc4e7dbf56cbe07070216d307ebe3530486044f7c5082f3d9d2",
    "external": "6b7e745619c5bff2df88c45e41154ba4033d3bbdbaaca21ba6e4479d4087130e",
}
VARIABLES = anti.VARIABLES


def progress(stage: str, started: float) -> None:
    """Write a timestamped, flush-safe progress record to stderr."""

    record = {
        "timestampUtc": datetime.now(timezone.utc).isoformat(),
        "elapsedSeconds": round(time.perf_counter() - started, 3),
        "stage": stage,
    }
    print(json.dumps(record, ensure_ascii=False), file=sys.stderr, flush=True)


def coefficient_digest(polynomial: sp.Poly) -> str:
    payload = "\n".join(
        f"{powers[0]},{powers[1]},{powers[2]}:{coefficient}"
        for powers, coefficient in polynomial.terms()
    )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def polynomial_record(polynomial: sp.Poly) -> dict[str, object]:
    terms = polynomial.terms()
    exponents = tuple(zip(*(powers for powers, _ in terms), strict=True))
    coefficients = [coefficient for _, coefficient in terms]
    numerator_bits = [abs(int(value.p)).bit_length() for value in coefficients]
    denominator_bits = [int(value.q).bit_length() for value in coefficients]
    return {
        "termCount": len(terms),
        "degrees": [polynomial.degree(variable) for variable in VARIABLES],
        "valuations": [min(axis) for axis in exponents],
        "maxNumeratorBits": max(numerator_bits),
        "maxDenominatorBits": max(denominator_bits),
        "exactDigest": coefficient_digest(polynomial),
    }


def coefficient_form(polynomial: sp.Poly, axis: int, power: int) -> sp.Poly:
    expression = sp.Add(*(
        coefficient
        * sp.prod(
            VARIABLES[index] ** powers[index]
            for index in range(3)
            if index != axis
        )
        for powers, coefficient in polynomial.terms()
        if powers[axis] == power
    ))
    remaining = tuple(
        variable for index, variable in enumerate(VARIABLES) if index != axis
    )
    return sp.Poly(expression, *remaining, domain=sp.QQ)


def lower_degree(polynomial: sp.Poly, axis: int) -> int:
    return min(powers[axis] for powers, _ in polynomial.terms())


def form_record(polynomial: sp.Poly) -> dict[str, object]:
    return {
        "termCount": len(polynomial.terms()),
        "degrees": [polynomial.degree(variable) for variable in polynomial.gens],
        "exactDigest": hashlib.sha256(
            "\n".join(
                f"{','.join(map(str, powers))}:{coefficient}"
                for powers, coefficient in polynomial.terms()
            ).encode("ascii")
        ).hexdigest(),
        "identicallyZero": polynomial.is_zero,
    }


def factorization_record(polynomial: sp.Poly) -> dict[str, object]:
    unit, factors = sp.factor_list(polynomial.as_expr())
    return {
        "unit": str(unit),
        "factors": [
            {
                "multiplicity": multiplicity,
                **polynomial_record(
                    sp.Poly(factor, *VARIABLES, domain=sp.QQ)
                ),
            }
            for factor, multiplicity in factors
        ],
    }


def boundary_profile(
    target: sp.Poly,
    total: sp.Poly,
) -> dict[str, object]:
    profile: dict[str, object] = {}
    for axis, variable in enumerate(VARIABLES):
        target_low = lower_degree(target, axis)
        total_low = lower_degree(total, axis)
        target_high = target.degree(variable)
        total_high = total.degree(variable)
        faces: dict[str, object] = {}
        for side, target_power, total_power in (
            ("zero", target_low, total_low),
            ("infinity", target_high, total_high),
        ):
            if side == "zero":
                order_difference = target_power - total_power
            else:
                order_difference = total_power - target_power
            if order_difference > 0:
                limit_type = "target fraction tends to zero"
            elif order_difference == 0:
                limit_type = "finite rational face"
            else:
                limit_type = "singular degree ordering"
            target_form = coefficient_form(target, axis, target_power)
            total_form = coefficient_form(total, axis, total_power)
            faces[side] = {
                "targetPower": target_power,
                "totalPower": total_power,
                "orderDifference": order_difference,
                "limitType": limit_type,
                "targetForm": form_record(target_form),
                "totalForm": form_record(total_form),
                "commonFormGcd": form_record(sp.gcd(target_form, total_form)),
            }
        profile[str(variable)] = faces
    return profile


def serialize_polynomial(polynomial: sp.Poly) -> list[list[object]]:
    return [
        [*powers, str(int(coefficient.p)), str(int(coefficient.q))]
        for powers, coefficient in polynomial.terms()
    ]


def write_cache(
    path: Path,
    target: sp.Poly,
    external: sp.Poly,
    stationary: dict[str, sp.Poly],
    stationary_gcd: sp.Poly,
    reduced_stationary: dict[str, sp.Poly],
    target_square_factor: sp.Poly,
    saturated_stationary: dict[str, sp.Poly],
) -> dict[str, object]:
    payload = {
        "schemaVersion": 2,
        "variables": [str(variable) for variable in VARIABLES],
        "coordinateMap": {
            "u": "p/(1+p)",
            "v": "q/(1+q)",
            "w": "x/(1+x)",
        },
        "polynomials": {
            "target": serialize_polynomial(target),
            "external": serialize_polynomial(external),
            "stationary_gcd": serialize_polynomial(stationary_gcd),
            "target_square_factor": serialize_polynomial(target_square_factor),
            **{
                f"stationary_{name}": serialize_polynomial(polynomial)
                for name, polynomial in stationary.items()
            },
            **{
                f"reduced_stationary_{name}": serialize_polynomial(polynomial)
                for name, polynomial in reduced_stationary.items()
            },
            **{
                f"saturated_stationary_{name}": serialize_polynomial(polynomial)
                for name, polynomial in saturated_stationary.items()
            },
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8", compresslevel=9) as stream:
        json.dump(payload, stream, separators=(",", ":"))
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {
        "path": str(path),
        "sizeBytes": path.stat().st_size,
        "sha256": digest,
    }


def write_homotopy_terms(
    path: Path,
    reduced_stationary: dict[str, sp.Poly],
) -> dict[str, object]:
    """Write normalized Float64 terms for numerical candidate generation."""

    path.parent.mkdir(parents=True, exist_ok=True)
    scales: dict[str, str] = {}
    underflow_count = 0
    line_count = 0
    with path.open("w", encoding="ascii", newline="") as stream:
        stream.write("equation\tp\tq\tx\tcoefficient\n")
        for equation, name in enumerate(("p", "q", "x"), start=1):
            polynomial = reduced_stationary[name]
            scale = max(abs(coefficient) for coefficient in polynomial.coeffs())
            scales[name] = str(scale)
            for powers, coefficient in polynomial.terms():
                normalized = float(coefficient / scale)
                if normalized == 0.0 and coefficient != 0:
                    underflow_count += 1
                stream.write(
                    f"{equation}\t{powers[0]}\t{powers[1]}\t{powers[2]}\t"
                    f"{normalized:.17g}\n"
                )
                line_count += 1
    return {
        "path": str(path),
        "sizeBytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "termCount": line_count,
        "underflowCount": underflow_count,
        "exactEquationScales": scales,
    }


def audit(
    cache_path: Path | None = None,
    homotopy_terms_path: Path | None = None,
) -> dict[str, object]:
    started = time.perf_counter()
    progress("reconstructing exact fifth-order system", started)
    frequency_count, pole_count, target, external, stationary = anti.exact_system()
    progress("exact fifth-order system reconstructed", started)

    total = target + external
    progress("computing exact polynomial and boundary profiles", started)
    global_gcd = sp.gcd(target, total)
    stationary_gcd = sp.gcd(
        sp.gcd(stationary["p"], stationary["q"]),
        stationary["x"],
    )
    reduced_stationary = {
        name: sp.exquo(polynomial, stationary_gcd)
        for name, polynomial in stationary.items()
    }
    target_after_x2 = sp.exquo(
        target,
        sp.Poly(anti.X_VAR**2, *VARIABLES, domain=sp.QQ),
    )
    _target_unit, target_factors = sp.factor_list(target_after_x2.as_expr())
    target_square_factor = sp.Poly(1, *VARIABLES, domain=sp.QQ)
    for factor, multiplicity in target_factors:
        if multiplicity % 2:
            raise AssertionError("The target factorization was not a square.")
        target_square_factor *= (
            sp.Poly(factor, *VARIABLES, domain=sp.QQ)
            ** (multiplicity // 2)
        )
    d_expression = target_square_factor.as_expr()
    e_expression = external.as_expr()
    saturated_stationary = {
        "p": sp.Poly(
            sp.expand(
                d_expression * external.diff(anti.P_VAR).as_expr()
                - 2 * e_expression * target_square_factor.diff(anti.P_VAR).as_expr()
            ),
            *VARIABLES,
            domain=sp.QQ,
        ),
        "q": sp.Poly(
            sp.expand(
                d_expression * external.diff(anti.Q_VAR).as_expr()
                - 2 * e_expression * target_square_factor.diff(anti.Q_VAR).as_expr()
            ),
            *VARIABLES,
            domain=sp.QQ,
        ),
        "x": sp.Poly(
            sp.expand(anti.X_VAR * external.diff(anti.X_VAR).as_expr() - 2 * e_expression),
            *VARIABLES,
            domain=sp.QQ,
        ),
    }
    saturated_gcd = sp.gcd(
        sp.gcd(saturated_stationary["p"], saturated_stationary["q"]),
        saturated_stationary["x"],
    )
    profile = boundary_profile(target, total)
    progress("boundary profiles completed", started)

    cache = None
    if cache_path is not None:
        progress("writing compressed exact coefficient cache", started)
        cache = write_cache(
            cache_path,
            target,
            external,
            stationary,
            stationary_gcd,
            reduced_stationary,
            target_square_factor,
            saturated_stationary,
        )
        progress("coefficient cache completed", started)

    homotopy_terms = None
    if homotopy_terms_path is not None:
        progress("writing normalized homotopy terms", started)
        homotopy_terms = write_homotopy_terms(
            homotopy_terms_path,
            saturated_stationary,
        )
        progress("normalized homotopy terms completed", started)

    return {
        "scope": "projective compactification of the R0.18 positive orthant",
        "coordinateMap": {
            "u": "p/(1+p)",
            "v": "q/(1+q)",
            "w": "x/(1+x)",
            "openRegion": "0<u,v,w<1",
        },
        "aggregatedFrequencyCount": frequency_count,
        "uncancelledLaurentMonomialCount": pole_count,
        "polynomials": {
            "target": polynomial_record(target),
            "external": polynomial_record(external),
            "total": polynomial_record(total),
            "stationary": {
                name: polynomial_record(polynomial)
                for name, polynomial in stationary.items()
            },
            "stationaryGcd": {
                **polynomial_record(stationary_gcd),
                "factorization": factorization_record(stationary_gcd),
            },
            "reducedStationary": {
                name: polynomial_record(polynomial)
                for name, polynomial in reduced_stationary.items()
            },
            "targetSquareFactor": polynomial_record(target_square_factor),
            "saturatedStationary": {
                name: polynomial_record(polynomial)
                for name, polynomial in saturated_stationary.items()
            },
            "saturatedStationaryGcd": polynomial_record(saturated_gcd),
            "targetTotalGcd": polynomial_record(global_gcd),
            "targetAfterX2Factorization": factorization_record(target_after_x2),
        },
        "boundaryProfile": profile,
        "cache": cache,
        "homotopyTerms": homotopy_terms,
        "wallSeconds": time.perf_counter() - started,
    }


def validate(result: dict[str, object]) -> None:
    assert result["aggregatedFrequencyCount"] == 332
    assert result["uncancelledLaurentMonomialCount"] == 0
    polynomials = result["polynomials"]
    assert polynomials["target"]["exactDigest"] == EXPECTED_DIGESTS["target"]
    assert polynomials["external"]["exactDigest"] == EXPECTED_DIGESTS["external"]
    assert polynomials["stationaryGcd"]["degrees"] == [6, 8, 1]
    assert polynomials["stationaryGcd"]["termCount"] == 63
    assert polynomials["reducedStationary"]["p"]["degrees"] == [16, 16, 7]
    assert polynomials["reducedStationary"]["q"]["degrees"] == [18, 14, 7]
    assert polynomials["reducedStationary"]["x"]["degrees"] == [18, 16, 6]
    assert polynomials["targetSquareFactor"]["degrees"] == [6, 6, 0]
    assert polynomials["saturatedStationary"]["p"]["degrees"] == [16, 18, 6]
    assert polynomials["saturatedStationary"]["q"]["degrees"] == [18, 16, 6]
    assert polynomials["saturatedStationary"]["x"]["degrees"] == [12, 12, 6]
    assert polynomials["saturatedStationaryGcd"]["degrees"] == [0, 0, 0]
    for variable in ("p", "q", "x"):
        for side in ("zero", "infinity"):
            record = result["boundaryProfile"][variable][side]
            assert record["limitType"] != "singular degree ordering"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path)
    parser.add_argument("--homotopy-terms", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    result = audit(arguments.cache, arguments.homotopy_terms)
    if arguments.check:
        validate(result)
    print(json.dumps(result, indent=2 if arguments.pretty else None))


if __name__ == "__main__":
    main()
