#!/usr/bin/env python3
"""Low-cost fixed-ratio sensitivity pilot around the R0.69W ratio four.

This script deliberately does not modify or regenerate the published R0.69W
certificate.  For each positive rational ``rho`` it reuses the source-locked
R0.69W interval integrator after setting ``epsilon = 1/rho`` in memory, builds
a fresh radial partition, and reports fixed-rho interval enclosures for the
four amplitude coefficients on annuli zero and minus two.

The fixed-rho enclosures are rigorous for the selected (usually coarse) grid.
Finite-difference slopes between distinct rho values are diagnostics only:
they do not bound the derivative throughout the intervening rho interval.
Their purpose is to size a later interval-in-rho certificate.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import time

from flint import ctx

import two_scale_annular_interval as r069w


def configure_ratio(rho: Fraction) -> Fraction:
    if rho <= 0:
        raise ValueError("rho must be positive")
    epsilon = 1 / rho
    if epsilon * r069w.ACTIVE_HIGH >= r069w.ACTIVE_LOW:
        raise ValueError(
            "rho is too small for the fixed-core/intermediate-plateau partition"
        )
    r069w.EPSILON = epsilon
    r069w.INNER_ACTIVE_LOW = epsilon * r069w.ACTIVE_LOW
    r069w.INNER_ACTIVE_HIGH = epsilon * r069w.ACTIVE_HIGH
    return epsilon


def midpoint(interval: r069w.Interval) -> float:
    return (float(interval.lower) + float(interval.upper)) / 2.0


def width(interval: r069w.Interval) -> float:
    return float(interval.upper) - float(interval.lower)


def interval_payload(interval: r069w.Interval) -> dict[str, object]:
    return {
        "interval": interval.scalar(),
        "midpoint": midpoint(interval),
        "width": width(interval),
    }


def compute_ratio(
    rho: Fraction,
    cutoff: r069w.CutoffCertificate,
    generic_function,
    core_function,
    moment_certificates: dict[int, r069w.AnnularMomentCertificate],
    core_cells: int,
    plateau_cells: int,
    transition_cells: int,
    boundary_refinement: int,
) -> dict[str, object]:
    started = time.perf_counter()
    epsilon = configure_ratio(rho)
    radial_cells = r069w.build_radial_cells(
        cutoff,
        core_cells,
        plateau_cells,
        boundary_refinement,
        transition_cells,
    )
    coefficients: dict[int, list[r069w.Interval]] = {}
    audits: dict[int, dict[str, object]] = {}
    for annulus in (0, -2):
        angular = moment_certificates[annulus].annular
        values, audit = r069w.integrate_coefficients_moment_taylor4(
            radial_cells,
            cutoff,
            angular,
            moment_certificates[annulus],
            generic_function,
            core_function,
            None,
            0,
            1,
        )
        coefficients[annulus] = values
        audits[annulus] = audit

    c1, c2, c3 = coefficients[0][1:]
    discriminant = c2 * c2 - 4 * c1 * c3
    midpoint_discriminant = midpoint(c2) ** 2 - 4 * midpoint(c1) * midpoint(c3)
    endpoint = coefficients[-2][0]
    return {
        "rho": str(rho),
        "rhoFloat": float(rho),
        "epsilon": str(epsilon),
        "epsilonFloat": float(epsilon),
        "j0": {
            f"c{degree}": interval_payload(value)
            for degree, value in enumerate(coefficients[0])
        },
        "jMinus2": {
            f"c{degree}": interval_payload(value)
            for degree, value in enumerate(coefficients[-2])
        },
        "decisionQuantities": {
            "c3": interval_payload(c3),
            "discriminant": interval_payload(discriminant),
            "discriminantFromCoefficientMidpoints": {
                "midpoint": midpoint_discriminant,
                "certificationStatus": (
                    "diagnostic only; this is not the midpoint of the rigorous "
                    "discriminant interval"
                ),
            },
            "endpointJMinus2AtA0": interval_payload(endpoint),
        },
        "coarseFixedRatioSignsCertified": {
            "c3Negative": float(c3.upper) < 0.0,
            "discriminantNegative": float(discriminant.upper) < 0.0,
            "endpointNegative": float(endpoint.upper) < 0.0,
        },
        "radialCells": len(radial_cells),
        "evaluatedRadialBoxes": {
            str(index): audits[index]["evaluatedRadialBoxes"] for index in (0, -2)
        },
        "elapsedSeconds": time.perf_counter() - started,
    }


def secant_diagnostics(records: list[dict[str, object]]) -> list[dict[str, object]]:
    keys = (
        ("c1", "j0", "c1"),
        ("c2", "j0", "c2"),
        ("c3", "j0", "c3"),
        (
            "discriminantFromCoefficientMidpoints",
            "decisionQuantities",
            "discriminantFromCoefficientMidpoints",
        ),
        (
            "endpointJMinus2AtA0",
            "decisionQuantities",
            "endpointJMinus2AtA0",
        ),
    )
    result = []
    for left, right in zip(records, records[1:]):
        delta = float(right["rhoFloat"]) - float(left["rhoFloat"])
        slopes = {}
        for label, group, key in keys:
            left_value = float(left[group][key]["midpoint"])
            right_value = float(right[group][key]["midpoint"])
            slopes[label] = (right_value - left_value) / delta
        result.append(
            {
                "rhoInterval": [left["rhoFloat"], right["rhoFloat"]],
                "midpointSecantSlopesPerUnitRho": slopes,
                "certificationStatus": (
                    "diagnostic only; fixed-rho enclosures do not bound the "
                    "derivative between endpoints"
                ),
            }
        )
    return result


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--rhos", default="3.8,3.9,4,4.1,4.2")
    parser.add_argument("--raw-moment-power", type=int, default=14)
    parser.add_argument("--cutoff-cells", type=int, default=64)
    parser.add_argument("--moment-power", type=int, default=14)
    parser.add_argument("--core-cells", type=int, default=4)
    parser.add_argument("--plateau-cells", type=int, default=8)
    parser.add_argument("--transition-cells", type=int, default=8)
    parser.add_argument("--boundary-refinement", type=int, default=1)
    parser.add_argument("--arb-precision", type=int, default=128)
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    rhos = sorted({Fraction(token.strip()) for token in arguments.rhos.split(",")})
    if not rhos:
        raise SystemExit("--rhos must contain at least one positive rational")
    ctx.prec = arguments.arb_precision
    setup_started = time.perf_counter()
    raw = r069w.RawMomentTable(arguments.raw_moment_power)
    cutoff = r069w.CutoffCertificate(raw, arguments.cutoff_cells)
    generic, core, _direct, _direct_core, symbolic = r069w.derive_radial_functions()
    moment_certificates = {}
    for annulus in (0, -2):
        angular = r069w.AnnularAngularKernel(cutoff, annulus)
        moment_certificates[annulus] = r069w.AnnularMomentCertificate(
            cutoff, angular, arguments.moment_power
        )
    setup_seconds = time.perf_counter() - setup_started
    records = [
        compute_ratio(
            rho,
            cutoff,
            generic,
            core,
            moment_certificates,
            arguments.core_cells,
            arguments.plateau_cells,
            arguments.transition_cells,
            arguments.boundary_refinement,
        )
        for rho in rhos
    ]
    payload = {
        "release": "R0.70A-pilot",
        "status": "diagnostic",
        "claimBoundary": (
            "rigorous coarse enclosures at each listed rational rho; secant "
            "slopes and any inferred open rho interval are not certificates"
        ),
        "configuration": {
            "rawMomentPower": arguments.raw_moment_power,
            "cutoffCells": arguments.cutoff_cells,
            "momentPower": arguments.moment_power,
            "coreCells": arguments.core_cells,
            "plateauCells": arguments.plateau_cells,
            "transitionCells": arguments.transition_cells,
            "boundaryRefinement": arguments.boundary_refinement,
            "arbPrecisionBits": arguments.arb_precision,
            "workers": 1,
        },
        "setupSeconds": setup_seconds,
        "symbolicAudits": {
            "spherePolynomialTerms": symbolic["spherePolynomialTerms"],
            "angularDegree": symbolic["angularDegree"],
            "commonRotationSquareRootEliminated": symbolic[
                "commonRotationSquareRootEliminated"
            ],
            "coreCoreExactlyZero": symbolic["coreCoreExactlyZero"],
            "distanceMomentReductionExact": symbolic[
                "directAngularToDistanceMomentsExact"
            ],
        },
        "records": records,
        "secantDiagnostics": secant_diagnostics(records),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(arguments.output), "records": len(records)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
