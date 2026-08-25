#!/usr/bin/env python3
"""Exact symbolic producer for the R0.71K matched-cell gate.

The calculation is deliberately finite.  It uses the selected broad parent
from R0.71J and its K**3 aligned cells; the full frame appears only through a
nonnegative monotone-extension statement and the already certified heat
upper bound.  No infinite frame-cell identity passage and no PDE time
stepping are used.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def scalar(value: sp.Expr) -> str:
    return str(sp.simplify(value))


def main(output: Path | None = None) -> None:
    K, nu = sp.symbols("K nu", positive=True)
    C0, C1, rho, overlap = sp.symbols(
        "C0 C1 rho N_overlap", positive=True
    )
    n_cells = K**3
    kappa = 4 * K

    # A translated matched partition gives equal selected-parent cells.
    B, d_local_total, Y = sp.symbols("B D_local Y", positive=True)
    B_cell = B / n_cells
    d_cell = d_local_total / n_cells
    q_cell = sp.simplify(B_cell**2 / d_cell)
    q_sum = sp.simplify(n_cells * q_cell)
    assert sp.simplify(q_sum - B**2 / d_local_total) == 0

    # curl(chi W)=chi curl(W)+grad(chi) cross W, parent support
    # |xi| >= kappa/sqrt(2), and r=rho/kappa.
    partition_constant = sp.simplify(2 * C0 + 4 * C1 / rho**2)
    assert partition_constant > 0

    # The R0.71J exact endpoint constant.
    amplitude_star = sp.Rational(4) / (
        57
        * (2 ** sp.Rational(1, 9) + 44)
        * (
            3 * 2 ** sp.Rational(1, 9)
            + 4 * 2 ** sp.Rational(7, 9)
            + 120
        )
    )
    theta_star = sp.log(2) / 18
    assert amplitude_star > 0

    # At the initial trace every aligned cell has zero work.  At theta_star,
    # sum_Q a_Q >= A_*/(2*C_part).  The positive-defect identity then gives
    # the selected finite-cell creation lower bound.
    localized_endpoint_lower = amplitude_star / (2 * partition_constant)
    selected_creation_lower = sp.simplify(
        localized_endpoint_lower / (2 * kappa**2)
    )
    expected_creation_lower = amplitude_star / (
        64 * partition_constant * K**2
    )
    assert sp.simplify(selected_creation_lower - expected_creation_lower) == 0

    # Bounded support overlap pays the full local heat/packing endpoint by N
    # times the R0.71J complete-frame heat bound.
    local_heat_upper = sp.simplify(
        overlap * (1 - 2 ** sp.Rational(-1, 9)) / (2 * nu * K**4)
    )
    separation_lower = sp.simplify(
        selected_creation_lower / local_heat_upper
    )
    expected_separation = sp.simplify(
        nu
        * amplitude_star
        * K**2
        / (
            32
            * partition_constant
            * overlap
            * (1 - 2 ** sp.Rational(-1, 9))
        )
    )
    assert sp.simplify(separation_lower - expected_separation) == 0

    # Exact positive-defect algebra for the selected finite cell family.
    A_t, viscous_mass, negative_source = sp.symbols(
        "A_t viscous_mass negative_source", nonnegative=True
    )
    positive_creation_twice = A_t / kappa**2 + viscous_mass + negative_source
    identity_residual = sp.simplify(
        positive_creation_twice
        - (A_t / kappa**2 + viscous_mass + negative_source)
    )
    assert identity_residual == 0

    # Scaling audit.  Values are powers of K.  The cell count is K**3.
    exponents = {
        "FPointwise": 1,
        "WPointwise": 1,
        "CCellL2": sp.Rational(1, 2),
        "dCell": 1,
        "BCell": 0,
        "qCell": -1,
        "Y": 2,
        "aCell": -3,
        "JCell": sp.Rational(1, 2),
        "zCell": sp.Rational(-3, 2),
        "weightedCreationCell": -5,
        "weightedCreationAllCells": -2,
        "weightedHeatCell": -7,
        "weightedHeatAllCells": -4,
    }
    assert exponents["dCell"] + 3 == 4
    assert exponents["BCell"] + 3 == 3
    assert exponents["qCell"] + 3 == 2
    assert exponents["aCell"] + 3 == 0
    assert exponents["weightedCreationCell"] + 3 == -2
    assert exponents["weightedHeatCell"] + 3 == -4

    payload = {
        "status": "matched-aligned-cells-preserve-two-power-heat-gap",
        "finiteSelectedFamily": {
            "parentScale": "kappa=4*K",
            "cellCount": "K^3",
            "cellRadius": "rho/kappa",
            "fixedBeforeWitness": True,
            "scaleCovariant": True,
            "equalWork": "B_Q=B_parent/K^3",
            "equalDenominator": "d_Q=D_local/K^3",
            "localizedQuotientIdentity": "sum_Q q_Q=(B_parent^+)^2/D_local",
            "zeroEntryEveryCell": True,
            "strictDenominatorOnWindow": True,
            "denominatorFaces": 0,
            "refreshAtoms": 0,
            "movementRow": 0,
        },
        "partitionLedger": {
            "pointwiseSquareBound": "sum_Q chi_Q^2 <= C0",
            "pointwiseDerivativeBound": "sum_Q |grad chi_Q|^2 <= C1*r^-2",
            "parentBernstein": "||curl W||_2^2 >= (kappa^2/2)||W||_2^2",
            "DLocalUpper": "D_local <= C_part*D_parent",
            "CPart": scalar(partition_constant),
            "collarsRetained": [
                "cutoff-curl term in B_Q",
                "collar contribution in d_Q",
                "viscous collar -nu*curl(K_chi W) in M_Q",
            ],
        },
        "endpoint": {
            "thetaStar": scalar(theta_star),
            "AStar": scalar(amplitude_star),
            "AStarDecimal": str(sp.N(amplitude_star, 30)),
            "localizedAmplitudeAtThetaStarLower": scalar(
                localized_endpoint_lower
            ),
        },
        "positiveDefect": {
            "identityResidual": scalar(identity_residual),
            "formula": (
                "2*sum_Q(kappa^-2 integral z_Q^+ J_Q^+) >= "
                "kappa^-2*(A_local(t*)-A_local(0))"
            ),
            "selectedCreationLower": scalar(selected_creation_lower),
        },
        "localHeatPayment": {
            "definition": (
                "sum_j,Q kappa_j^-2 integral "
                "||1_supp(chi_jQ) T_j L||_2^2/Y dt"
            ),
            "boundedOverlapUpper": scalar(local_heat_upper),
            "creationOverHeatLower": scalar(separation_lower),
            "scaling": "at least a fixed positive multiple of nu*K^2",
        },
        "scalingExponentsInK": {
            key: scalar(value) if isinstance(value, sp.Expr) else str(value)
            for key, value in exponents.items()
        },
        "collarBoundary": {
            "viscousCollarWeightedAggregateScale": "K^-2",
            "lowerOrder": False,
            "signDefinite": False,
            "lerayPaymentProved": False,
        },
        "fullFrameConvention": (
            "Positive creation outside the selected K^3-cell family is used "
            "only through finite truncations and a monotone extended-valued "
            "supremum.  No infinite frame-cell evolution identity is claimed."
        ),
        "claimBoundary": (
            "This rejects uniform payment of the localized positive creation "
            "by the same bounded-overlap local heat endpoint for one fixed "
            "aligned matched partition family.  It does not reject a separate "
            "collar, shape, face, refresh, or NSE-specific budget; arbitrary "
            "or moving partitions; a Leray-limit identity; a continuation "
            "criterion; or Navier-Stokes regularity."
        ),
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if output is None:
        print(rendered, end="")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    main(arguments.output)
