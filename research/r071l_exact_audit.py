#!/usr/bin/env python3
"""Exact algebra producer for the R0.71L fixed-cell ledger.

The producer is deliberately finite and structural. It verifies the
fixed-cutoff viscous commutator fusion, the normalized/projective quotient
identity on an exact finite-dimensional path, a Fourier Helmholtz
cancellation, the aligned cutoff--curl numerator cancellation, the
two-sided denominator scaling, and the precise Cauchy--Young remainder left
by a rowwise tangent estimate.

The final remainder is recorded as unpaid by the estimates checked here.
That is not a theorem that no Leray-level estimate can exist.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def clean(value: sp.Expr | sp.MatrixBase) -> sp.Expr | sp.MatrixBase:
    """Apply exact simplification componentwise."""

    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda entry: sp.factor(sp.simplify(entry)))
    return sp.factor(sp.simplify(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def vector_is_zero(value: sp.MatrixBase) -> bool:
    return all(clean(entry) == 0 for entry in value)


def vector_strings(value: sp.MatrixBase) -> list[str]:
    return [str(clean(entry)) for entry in value]


def fixed_cutoff_viscous_fusion() -> dict[str, object]:
    """Verify the product-rule commutator before and after one curl derivative.

    One coordinate is sufficient: the Laplacian product rule is componentwise,
    and curl is a constant-coefficient first-order operator commuting with the
    Laplacian. Thus the scalar check below verifies every vector component of
    the three-dimensional identity.
    """

    coordinate = sp.symbols("x", real=True)
    viscosity, kappa = sp.symbols("nu kappa", positive=True)
    cutoff = sp.Function("chi")(coordinate)
    field = sp.Function("W")(coordinate)

    commutator = (
        2 * sp.diff(cutoff, coordinate) * sp.diff(field, coordinate)
        + sp.diff(cutoff, coordinate, 2) * field
    )
    product_rule_residual = clean(
        sp.diff(cutoff * field, coordinate, 2)
        - cutoff * sp.diff(field, coordinate, 2)
        - commutator
    )
    require(product_rule_residual == 0, "Laplacian product rule")

    localized_curl_surrogate = sp.diff(cutoff * field, coordinate)
    expanded = viscosity * (
        sp.diff(localized_curl_surrogate, coordinate, 2)
        + kappa**2 * localized_curl_surrogate
    ) - viscosity * sp.diff(commutator, coordinate)
    fused = viscosity * sp.diff(
        cutoff * (sp.diff(field, coordinate, 2) + kappa**2 * field),
        coordinate,
    )
    fusion_residual = clean(expanded - fused)
    require(fusion_residual == 0, "fixed-cutoff viscous fusion")

    # A nonconstant positive cutoff can make both expanded viscous rows
    # nonzero even when the underlying field lies in one Laplace eigenspace.
    # The two rows must then cancel exactly before absolute values are taken.
    epsilon = sp.symbols("epsilon", positive=True)
    explicit_cutoff = 1 + epsilon * sp.cos(coordinate)
    explicit_field = sp.sin(coordinate)
    explicit_commutator = clean(
        2
        * sp.diff(explicit_cutoff, coordinate)
        * sp.diff(explicit_field, coordinate)
        + sp.diff(explicit_cutoff, coordinate, 2) * explicit_field
    )
    explicit_localized_curl = clean(
        sp.diff(explicit_cutoff * explicit_field, coordinate)
    )
    explicit_interior = clean(
        sp.diff(explicit_localized_curl, coordinate, 2)
        + explicit_localized_curl
    )
    explicit_curl_commutator = clean(
        sp.diff(explicit_commutator, coordinate)
    )
    explicit_residual = clean(
        explicit_interior - explicit_curl_commutator
    )
    require(
        clean(explicit_interior + 3 * epsilon * sp.cos(2 * coordinate)) == 0,
        "explicit localized Laplacian row",
    )
    require(
        clean(
            explicit_curl_commutator
            + 3 * epsilon * sp.cos(2 * coordinate)
        )
        == 0,
        "explicit raw commutator row",
    )
    require(explicit_residual == 0, "explicit nontrivial collar cancellation")

    return {
        "passed": True,
        "laplacianProductRuleResidual": str(product_rule_residual),
        "fusionResidual": str(fusion_residual),
        "explicitSingleEigenspaceCancellation": {
            "field": "W=(0,sin(x_1),0)",
            "cutoff": "chi=1+epsilon*cos(x_1), 0<epsilon<1",
            "localizedCurl": str(explicit_localized_curl),
            "localizedLaplacianRow": str(explicit_interior),
            "curlCommutatorRow": str(explicit_curl_commutator),
            "expandedResidual": str(explicit_residual),
            "bothExpandedRowsNonzero": True,
        },
        "threeDimensionalIdentity": (
            "nu*(Delta+kappa^2)curl(chi*W) "
            "- nu*curl(2*grad(chi).grad(W)+Delta(chi)*W) "
            "= nu*curl(chi*(Delta+kappa^2)*W)"
        ),
        "canonicalFixedCellRemainder": (
            "M_Q=curl(chi_Q*(nu*(Delta+kappa^2)*W+G))"
        ),
        "boundary": (
            "The separately named viscous collar is a commutator component; "
            "the identity gives no sign or coercive defect."
        ),
    }


def normalization_projective_identity() -> dict[str, object]:
    """Check every normalized/projective row with exact rational data."""

    field = sp.Matrix([3, -1, 4])
    field_t = sp.Matrix([-2, 3, 1])
    localized = sp.Matrix([1, 2, 2])
    localized_t = sp.Matrix([2, 0, -1])
    enstrophy = sp.Integer(25)
    enstrophy_t = sp.Integer(-6)
    rate = sp.Rational(7, 5)

    radius = clean(sp.sqrt(localized.dot(localized)))
    require(radius == 3, "chosen denominator radius")
    direction = clean(localized / radius)
    projector = clean(sp.eye(3) - direction * direction.T)

    radius_t = clean(localized.dot(localized_t) / radius)
    direction_t = clean(
        localized_t / radius - localized * radius_t / radius**2
    )
    nominal_localized = clean(localized_t + rate * localized)
    projective_direction_t = clean(projector * nominal_localized / radius)
    require(
        vector_is_zero(clean(direction_t - projective_direction_t)),
        "E_t=P M/r",
    )

    normalized_field = clean(field / sp.sqrt(enstrophy))
    normalized_field_t = clean(
        field_t / sp.sqrt(enstrophy)
        - enstrophy_t * normalized_field / (2 * enstrophy)
    )
    nominal_field = clean(field_t + rate * field)
    normalization_fusion = clean(
        nominal_field / sp.sqrt(enstrophy)
        - enstrophy_t * normalized_field / (2 * enstrophy)
        - (normalized_field_t + rate * normalized_field)
    )
    require(vector_is_zero(normalization_fusion), "normalization fusion")

    coefficient = clean(normalized_field.dot(direction))
    require(bool(coefficient > 0), "positive branch in finite example")
    coefficient_t = clean(
        normalized_field_t.dot(direction)
        + normalized_field.dot(direction_t)
    )
    source = clean(
        (nominal_field / sp.sqrt(enstrophy)).dot(direction)
        + (projector * field).dot(projector * nominal_localized)
        / (radius * sp.sqrt(enstrophy))
        - enstrophy_t * coefficient / (2 * enstrophy)
    )
    scalar_residual = clean(coefficient_t + rate * coefficient - source)
    require(scalar_residual == 0, "z_t+lambda*z=J")

    amplitude = clean(coefficient**2)
    amplitude_t = clean(2 * coefficient * coefficient_t)
    amplitude_residual = clean(
        amplitude_t + 2 * rate * amplitude - 2 * coefficient * source
    )
    require(amplitude_residual == 0, "a_t+2*lambda*a=2*z*J")

    tangent_from_m = clean(
        (projector * normalized_field).dot(projector * nominal_localized)
        / radius
    )
    tangent_from_direction = clean(
        (projector * normalized_field).dot(direction_t)
    )
    require(
        clean(tangent_from_m - tangent_from_direction) == 0,
        "projective tangent equivalence",
    )

    return {
        "passed": True,
        "exactInput": {
            "F": vector_strings(field),
            "F_t": vector_strings(field_t),
            "C": vector_strings(localized),
            "C_t": vector_strings(localized_t),
            "Y": str(enstrophy),
            "Y_t": str(enstrophy_t),
            "lambda": str(rate),
        },
        "radius": str(radius),
        "direction": vector_strings(direction),
        "directionDerivative": vector_strings(direction_t),
        "normalizationFusionResidual": vector_strings(normalization_fusion),
        "z": str(coefficient),
        "z_t": str(coefficient_t),
        "J": str(source),
        "scalarResidual": str(scalar_residual),
        "amplitude": str(amplitude),
        "amplitudeResidual": str(amplitude_residual),
        "tangentResidual": str(clean(tangent_from_m - tangent_from_direction)),
    }


def helmholtz_exact_cancellation() -> dict[str, object]:
    """Give an exact one-mode Fourier Helmholtz cancellation example."""

    frequency = sp.Matrix([1, 2, 2])
    raw = sp.Matrix([3, -1, 4])
    frequency_squared = clean(frequency.dot(frequency))
    projector = clean(
        sp.eye(3) - frequency * frequency.T / frequency_squared
    )
    solenoidal = clean(projector * raw)
    gradient = clean(raw - solenoidal)

    divergence = clean(frequency.dot(solenoidal))
    gradient_curl = clean(frequency.cross(gradient))
    curl_residual = clean(
        frequency.cross(raw) - frequency.cross(solenoidal)
    )
    require(divergence == 0, "Helmholtz solenoidal divergence")
    require(vector_is_zero(gradient_curl), "gradient is curl-free")
    require(vector_is_zero(curl_residual), "curl ignores gradient component")

    return {
        "passed": True,
        "frequency": vector_strings(frequency),
        "rawVector": vector_strings(raw),
        "solenoidalProjection": vector_strings(solenoidal),
        "gradientRemainder": vector_strings(gradient),
        "frequencyDotSolenoidal": str(divergence),
        "frequencyCrossGradient": vector_strings(gradient_curl),
        "curlCancellationResidual": vector_strings(curl_residual),
        "identity": "k cross V = k cross P_k V",
        "boundary": (
            "This is a Fourier Helmholtz identity. Multiplication by a "
            "nonconstant cutoff can reintroduce a boundary term."
        ),
    }


def aligned_cutoff_curl_cancellation() -> dict[str, object]:
    """Check a translated smooth partition and the general equal-cell logic."""

    coordinate = sp.symbols("x", real=True)
    cutoff_zero = (1 + sp.cos(coordinate)) / 2
    cutoff_one = (1 - sp.cos(coordinate)) / 2
    field = sp.cos(2 * coordinate)
    vorticity_block = sp.sin(2 * coordinate)

    partition_residual = clean(cutoff_zero + cutoff_one - 1)
    translation_residual = clean(
        sp.trigsimp(
            cutoff_zero.subs(coordinate, coordinate - sp.pi) - cutoff_one
        )
    )
    field_translation = clean(
        sp.trigsimp(field.subs(coordinate, coordinate + sp.pi) - field)
    )
    block_translation = clean(
        sp.trigsimp(
            vorticity_block.subs(coordinate, coordinate + sp.pi)
            - vorticity_block
        )
    )
    require(partition_residual == 0, "two-cell partition")
    require(translation_residual == 0, "translated cutoff")
    require(field_translation == 0, "translated field invariance")
    require(block_translation == 0, "translated W invariance")

    def normalized_integral(expression: sp.Expr) -> sp.Expr:
        return clean(
            sp.integrate(
                sp.expand_trig(expression), (coordinate, 0, 2 * sp.pi)
            )
            / (2 * sp.pi)
        )

    boundary_work_zero = normalized_integral(
        field * sp.diff(cutoff_zero, coordinate) * vorticity_block
    )
    boundary_work_one = normalized_integral(
        field * sp.diff(cutoff_one, coordinate) * vorticity_block
    )
    require(boundary_work_zero == 0, "first aligned boundary work")
    require(boundary_work_one == 0, "second aligned boundary work")
    require(
        clean(boundary_work_zero + boundary_work_one) == 0,
        "partition derivative cancellation",
    )

    cell_count = sp.symbols("N_cells", positive=True, integer=True)
    common_boundary_work = sp.symbols("b_boundary", real=True)
    common_work_solutions = sp.solve(
        sp.Eq(cell_count * common_boundary_work, 0),
        common_boundary_work,
    )
    require(common_work_solutions == [0], "solve equal-cell zero sum")
    inferred_common_work = clean(common_work_solutions[0])
    require(inferred_common_work == 0, "equal cells plus zero total")

    return {
        "passed": True,
        "finiteExample": {
            "partitionResidual": str(partition_residual),
            "translationResidual": str(translation_residual),
            "fieldTranslationResidual": str(field_translation),
            "blockTranslationResidual": str(block_translation),
            "cellBoundaryWorks": [
                str(boundary_work_zero),
                str(boundary_work_one),
            ],
        },
        "generalAlignedLogic": {
            "equalCellHypothesis": f"b_Q={common_boundary_work}",
            "partitionDerivativeSum": "sum_Q grad(chi_Q)=0",
            "totalBoundaryWork": f"{cell_count}*{common_boundary_work}=0",
            "inferredCellBoundaryWork": str(inferred_common_work),
        },
        "conclusion": (
            "For the R0.71K aligned translation-invariant witness, "
            "<F,grad(chi_Q) cross W>=0 in every selected cell."
        ),
        "boundary": (
            "The same cutoff--curl term remains in d_Q and in the dynamic "
            "projective row; only its static numerator work cancels. The "
            "conclusion is for the finite selected aligned family at the "
            "declared parent, not arbitrary partitions or a full frame."
        ),
    }


def denominator_bounds_and_scaling() -> dict[str, object]:
    """Verify the algebra and powers in the two-sided denominator ledger."""

    frequency, overlap, partition_constant = sp.symbols(
        "K N_overlap C_part", positive=True
    )
    denominator_lower, denominator_upper = sp.symbols(
        "D_minus D_plus", positive=True
    )
    denominator_model, work_constant, enstrophy_constant = sp.symbols(
        "D_model B0 Y0", positive=True
    )
    cell_count = frequency**3
    parent_lower = denominator_lower * frequency**4
    parent_upper = denominator_upper * frequency**4
    local_lower = clean(parent_lower / overlap)
    local_upper = clean(partition_constant * parent_upper)
    cell_lower = clean(local_lower / cell_count)
    cell_upper = clean(local_upper / cell_count)

    require(
        clean(cell_lower / frequency - denominator_lower / overlap) == 0,
        "cell denominator lower K power",
    )
    require(
        clean(
            cell_upper / frequency
            - partition_constant * denominator_upper
        )
        == 0,
        "cell denominator upper K power",
    )

    parent_work = work_constant * frequency**3
    enstrophy = enstrophy_constant * frequency**2
    cell_work = clean(parent_work / cell_count)
    model_cell_denominator = denominator_model * frequency
    quotient = clean(cell_work**2 / model_cell_denominator)
    normalized_amplitude = clean(quotient / enstrophy)
    normalized_coefficient = clean(sp.sqrt(normalized_amplitude))

    expected = {
        "BCell": work_constant,
        "dCell": denominator_model * frequency,
        "qCell": work_constant**2 / (denominator_model * frequency),
        "aCell": work_constant**2
        / (denominator_model * enstrophy_constant * frequency**3),
        "zCell": work_constant
        / (
            sp.sqrt(denominator_model)
            * sp.sqrt(enstrophy_constant)
            * frequency ** sp.Rational(3, 2)
        ),
    }
    actual = {
        "BCell": cell_work,
        "dCell": model_cell_denominator,
        "qCell": quotient,
        "aCell": normalized_amplitude,
        "zCell": normalized_coefficient,
    }
    for label, value in expected.items():
        require(clean(actual[label] - value) == 0, f"{label} scale")

    return {
        "passed": True,
        "proofInputs": {
            "overlapCauchy": "D_parent <= N_overlap*D_local",
            "partitionUpper": "D_local <= C_part*D_parent",
            "equalCell": "d_Q=D_local/K^3",
            "parentScale": (
                "D_minus*K^4 <= D_parent <= D_plus*K^4"
            ),
        },
        "twoSidedLocalBound": (
            "D_parent/N_overlap <= D_local <= C_part*D_parent"
        ),
        "twoSidedCellBound": (
            "D_minus*K/N_overlap <= d_Q <= C_part*D_plus*K"
        ),
        "cellLower": str(cell_lower),
        "cellUpper": str(cell_upper),
        "scalingExponentsInK": {
            "BCell": "0",
            "dCell": "1",
            "qCell": "-1",
            "aCell": "-3",
            "zCell": "-3/2",
            "cellCount": "3",
            "weightedCreationCell": "-5",
            "weightedCreationAllCells": "-2",
        },
        "boundary": (
            "The quantitative d_Q~K conclusion uses distinct R0.71J "
            "fixed-window constants D_minus and D_plus. D_model is only a "
            "generic positive O(1) coefficient for the exponent ledger; it "
            "is not either bound constant. Mere strict positivity is not "
            "enough for division in a scale audit."
        ),
    }


def leray_payment_boundary() -> dict[str, object]:
    """Separate the paid denominator mass from the unpaid tangent product."""

    viscosity, kappa = sp.symbols("nu kappa", positive=True)
    partition_constant, annulus_constant = sp.symbols(
        "C_part C_ann", positive=True
    )
    w_squared = sp.symbols("W2", nonnegative=True)
    local_denominator_upper = (
        partition_constant * annulus_constant * kappa**2 * w_squared
    )
    weighted_denominator = clean(
        viscosity * kappa ** (-2) * local_denominator_upper
    )
    paid_density = clean(
        viscosity * partition_constant * annulus_constant * w_squared
    )
    require(
        clean(weighted_denominator - paid_density) == 0,
        "weighted denominator mass reduction",
    )

    amplitude = sp.symbols("a", nonnegative=True)
    local_pf_squared, projected_m_squared = sp.symbols(
        "PF2 PM2", nonnegative=True
    )
    denominator, enstrophy = sp.symbols("d Y", positive=True)
    tangent_product = clean(
        local_pf_squared * projected_m_squared / (denominator * enstrophy)
    )
    young_left = clean(
        2
        * kappa ** (-2)
        * sp.sqrt(amplitude)
        * sp.sqrt(tangent_product)
    )
    young_right = clean(
        viscosity * amplitude
        + tangent_product / (viscosity * kappa**4)
    )
    exact_square = clean(
        (
            sp.sqrt(viscosity * amplitude)
            - sp.sqrt(tangent_product)
            / (sp.sqrt(viscosity) * kappa**2)
        )
        ** 2
    )
    young_residual = clean(young_right - young_left - exact_square)
    require(young_residual == 0, "exact Young remainder square")

    return {
        "passed": True,
        "lerayPaidDenominatorMass": {
            "shellwiseInput": (
                "D_local <= C_part*C_ann*kappa^2*||W_j||_2^2"
            ),
            "weightedDensity": str(weighted_denominator),
            "frameTimeConclusion": (
                "nu*integral sum_j kappa_j^-2 D_local,j "
                "<= constant*nu*integral Y <= constant*||u_0||_2^2"
            ),
            "requires": (
                "bounded overlap, annular Bernstein, frame square bound, "
                "and the standard Leray energy inequality"
            ),
        },
        "rowwiseTangentYoungStep": {
            "left": str(young_left),
            "right": str(young_right),
            "rightMinusLeft": str(exact_square),
            "identityResidual": str(young_residual),
            "unpaidProduct": str(
                clean(tangent_product / (viscosity * kappa**4))
            ),
            "unpaidFactors": [
                "local normalized projected Lamb amplitude PF2/Y",
                "projective angular ratio PM2/d",
            ],
        },
        "normalizationBoundary": {
            "separatedPositiveRow": "(a/2)*(Y_t/Y)^-",
            "standardLerayLogEnstrophyBVProved": False,
        },
        "claimBoundary": (
            "The exact checks show that the recorded denominator-mass "
            "estimate does not algebraically bound the displayed tangent "
            "product. They do not prove that no other Leray-level NSE "
            "estimate or signed nonlinear cancellation can control it."
        ),
    }


def main(output: Path | None = None) -> None:
    payload = {
        "status": "fixed-cell-fusion-ledger-exact-algebra-passed",
        "checks": {
            "fixedCutoffViscousFusion": fixed_cutoff_viscous_fusion(),
            "normalizationProjectiveFiniteAlgebra": (
                normalization_projective_identity()
            ),
            "helmholtzExactCancellation": helmholtz_exact_cancellation(),
            "alignedCutoffCurlNumerator": (
                aligned_cutoff_curl_cancellation()
            ),
            "denominatorTwoSidedScaleLedger": (
                denominator_bounds_and_scaling()
            ),
            "lerayPaymentBoundary": leray_payment_boundary(),
        },
        "claimBoundary": (
            "This producer proves finite exact algebra and the direct "
            "energy-estimate boundary recorded in its checks. It does not "
            "prove a Leray-level no-go, an unconditional weighted-BV bound, "
            "a continuation criterion, singularity, global regularity, "
            "originality, or a Millennium-problem result."
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
