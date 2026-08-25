#!/usr/bin/env python3
"""Independent numerical audit for the R0.71L collar/tangent gate.

This checker is deliberately standalone.  It imports neither an R0.71K
module nor an exact producer.  It reconstructs the finite Fourier witness,
the fixed tensor cutoff, and all rows of the pure-heat limiting joint source.

The output is a numerical diagnostic, not a continuous sign certificate and
not a finite-K NSE trajectory.  In particular, the checker computes only the
pure-heat leading coefficient.  Any finite-K O_nu(K^-3) transfer recorded in
the output comes from the separate R0.71J fixed-window weighted-Sobolev
argument and is not measured or verified by this quadrature.  The default
180-point spatial and 48-point time rules are chosen to finish quickly on a
workstation; both orders are configurable from the command line.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np


ComplexVector = tuple[complex, complex, complex]
Frequency = tuple[int, int, int]
Field = dict[Frequency, ComplexVector]

RADIUS = 1.5 * math.pi
THETA_STAR = math.log(2.0) / 18.0
NORMALIZATION = (2.0 * math.pi) ** 3


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def frequency_add(left: Frequency, right: Frequency) -> Frequency:
    return tuple(a + b for a, b in zip(left, right))  # type: ignore[return-value]


def complex_cross(left: ComplexVector, right: ComplexVector) -> ComplexVector:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def field_add(left: Field, right: Field) -> Field:
    result: Field = {}
    for frequency in set(left) | set(right):
        value = tuple(
            left.get(frequency, (0j, 0j, 0j))[index]
            + right.get(frequency, (0j, 0j, 0j))[index]
            for index in range(3)
        )
        if sum(abs(entry) ** 2 for entry in value) > 1.0e-28:
            result[frequency] = value  # type: ignore[assignment]
    return result


def field_scale(field: Field, scalar: float) -> Field:
    return {
        frequency: tuple(scalar * entry for entry in value)  # type: ignore[misc]
        for frequency, value in field.items()
    }


def field_derivative(field: Field, axis: int) -> Field:
    return {
        frequency: tuple(
            1j * frequency[axis] * entry for entry in value
        )  # type: ignore[misc]
        for frequency, value in field.items()
    }


def field_curl(field: Field) -> Field:
    result: Field = {}
    for frequency, value in field.items():
        crossed = complex_cross(
            tuple(complex(entry) for entry in frequency),  # type: ignore[arg-type]
            value,
        )
        result[frequency] = tuple(1j * entry for entry in crossed)  # type: ignore[assignment]
    return result


def field_cross(left: Field, right: Field) -> Field:
    result: Field = {}
    for left_frequency, left_value in left.items():
        for right_frequency, right_value in right.items():
            frequency = frequency_add(left_frequency, right_frequency)
            term = complex_cross(left_value, right_value)
            previous = result.get(frequency, (0j, 0j, 0j))
            result[frequency] = tuple(
                a + b for a, b in zip(previous, term)
            )  # type: ignore[assignment]
    return result


def leray(field: Field) -> Field:
    result: Field = {}
    for frequency, value in field.items():
        radius_squared = sum(entry * entry for entry in frequency)
        if radius_squared == 0:
            projected = value
        else:
            k_dot = sum(
                frequency[index] * value[index] for index in range(3)
            )
            projected = tuple(
                value[index] - frequency[index] * k_dot / radius_squared
                for index in range(3)
            )
        if sum(abs(entry) ** 2 for entry in projected) > 1.0e-28:
            result[frequency] = projected  # type: ignore[assignment]
    return result


def restrict_parent(field: Field) -> Field:
    return {
        frequency: value
        for frequency, value in field.items()
        if 16 <= sum(entry * entry for entry in frequency) <= 32
    }


def field_norm_squared(field: Field) -> float:
    return sum(abs(entry) ** 2 for value in field.values() for entry in value)


def field_pair(left: Field, right: Field) -> complex:
    frequencies = set(left) | set(right)
    return sum(
        left.get(frequency, (0j, 0j, 0j))[index].conjugate()
        * right.get(frequency, (0j, 0j, 0j))[index]
        for frequency in frequencies
        for index in range(3)
    )


def initial_velocity() -> Field:
    e2 = (0j, 1 + 0j, 0j)
    e3 = (0j, 0j, 1 + 0j)
    velocity: Field = {
        (1, 0, 0): e2,
        (-1, 0, 0): e2,
        (0, 4, 0): (0j, 0j, 0.25j),
        (0, -4, 0): (0j, 0j, -0.25j),
        (0, 5, 0): (0j, 0j, -0.2j),
        (0, -5, 0): (0j, 0j, 0.2j),
    }
    for channel in (4, 5):
        for horizontal_sign in (-1, 1):
            velocity[(horizontal_sign, channel, 0)] = e3
            velocity[(-horizontal_sign, -channel, 0)] = e3
    return velocity


def pure_heat_fields(theta: float) -> tuple[Field, Field, Field, Field, Field, Field]:
    velocity = {
        frequency: tuple(
            entry
            * math.exp(
                -sum(component * component for component in frequency) * theta
            )
            for entry in value
        )
        for frequency, value in initial_velocity().items()
    }
    velocity_theta = {
        frequency: tuple(
            -sum(component * component for component in frequency) * entry
            for entry in value
        )
        for frequency, value in velocity.items()
    }
    omega = field_curl(velocity)
    omega_theta = field_curl(velocity_theta)
    projected_lamb = leray(field_cross(velocity, omega))
    projected_lamb_theta = leray(
        field_add(
            field_cross(velocity_theta, omega),
            field_cross(velocity, omega_theta),
        )
    )
    return (
        restrict_parent(projected_lamb),
        restrict_parent(projected_lamb_theta),
        restrict_parent(omega),
        restrict_parent(omega_theta),
        omega,
        omega_theta,
    )


def bump_jet(value: float) -> tuple[float, float, float]:
    if abs(value) >= RADIUS:
        return 0.0, 0.0, 0.0
    denominator = 1.0 - (value / RADIUS) ** 2
    exponent_first = -2.0 * value / (RADIUS**2 * denominator**2)
    exponent_second = (
        -2.0 / (RADIUS**2 * denominator**2)
        - 8.0 * value**2 / (RADIUS**4 * denominator**3)
    )
    bump = math.exp(-1.0 / denominator)
    return (
        bump,
        bump * exponent_first,
        bump * (exponent_second + exponent_first**2),
    )


def periodic_denominator_jet(value: float) -> tuple[float, float, float]:
    center = int(round(value / (2.0 * math.pi)))
    jets = [
        bump_jet(value - 2.0 * math.pi * shift)
        for shift in range(center - 2, center + 3)
    ]
    return tuple(sum(jet[index] for jet in jets) for index in range(3))  # type: ignore[return-value]


def partition_jet(value: float) -> tuple[float, float, float]:
    bump, bump_first, bump_second = bump_jet(value)
    denominator, denominator_first, denominator_second = (
        periodic_denominator_jet(value)
    )
    require(denominator > 0.0, "partition denominator")
    atom = bump / denominator
    atom_first = (
        bump_first / denominator
        - bump * denominator_first / denominator**2
    )
    atom_second = (
        bump_second / denominator
        - bump * denominator_second / denominator**2
        - 2.0 * bump_first * denominator_first / denominator**2
        + 2.0 * bump * denominator_first**2 / denominator**3
    )
    return atom, atom_first, atom_second


@dataclass
class CellRows:
    theta: float
    work: float
    denominator: float
    enstrophy: float
    zeta: float
    radial: float
    heat_main_tangent: float
    viscous_collar: float
    projective_tangent: float
    normalization: float
    fused_joint: float
    tangent_fusion_residual: float
    scalar_differential_residual: float


class CellQuadrature:
    def __init__(self, order: int) -> None:
        require(order >= 64, "spatial quadrature order must be at least 64")
        self.order = order
        nodes, weights = np.polynomial.legendre.leggauss(order)
        self.nodes = RADIUS * nodes
        self.weights = RADIUS * weights
        jets = [partition_jet(float(value)) for value in self.nodes]
        h = np.array([jet[0] for jet in jets])
        hp = np.array([jet[1] for jet in jets])
        hpp = np.array([jet[2] for jet in jets])
        self.x_grid, self.y_grid = np.meshgrid(
            self.nodes, self.nodes, indexing="ij"
        )
        self.weights_2d = self.weights[:, None] * self.weights[None, :]
        self.hx = h[:, None]
        self.hy = h[None, :]
        self.hpx = hp[:, None]
        self.hpy = hp[None, :]
        self.hppx = hpp[:, None]
        self.hppy = hpp[None, :]
        self.integral_h = float(np.sum(self.weights * h))
        self.integral_hp = float(np.sum(self.weights * hp))
        self.integral_h2 = float(np.sum(self.weights * h**2))
        self.integral_hp2 = float(np.sum(self.weights * hp**2))
        self.integral_hpp2 = float(np.sum(self.weights * hpp**2))

    def evaluate_field(self, field: Field) -> np.ndarray:
        result = np.zeros((3, *self.x_grid.shape), dtype=np.complex128)
        for (frequency_x, frequency_y, frequency_z), coefficient in field.items():
            require(frequency_z == 0, "2D3C frequency")
            phase = np.exp(
                1j
                * (
                    frequency_x * self.x_grid
                    + frequency_y * self.y_grid
                )
            )
            for component in range(3):
                result[component] += coefficient[component] * phase
        return result

    def real_integral_2d(self, values: np.ndarray) -> float:
        return float(
            np.sum(self.weights_2d * np.real(values)) / NORMALIZATION
        )

    def cell_components(
        self, field: Field
    ) -> tuple[
        tuple[np.ndarray, np.ndarray, np.ndarray],
        tuple[np.ndarray, np.ndarray, np.ndarray],
        tuple[np.ndarray, np.ndarray, np.ndarray],
    ]:
        values = self.evaluate_field(field)
        values_x = self.evaluate_field(field_derivative(field, 0))
        values_y = self.evaluate_field(field_derivative(field, 1))
        curl = field_curl(field)
        curl_values = self.evaluate_field(curl)
        curl_x = self.evaluate_field(field_derivative(curl, 0))
        curl_y = self.evaluate_field(field_derivative(curl, 1))

        w1, w2 = values[0], values[1]
        w1x, w2x = values_x[0], values_x[1]
        w1y, w2y = values_y[0], values_y[1]
        c3 = curl_values[2]
        c3x = curl_x[2]
        c3y = curl_y[2]

        components = (
            -self.hx * self.hy * w2,
            self.hx * self.hy * w1,
            self.hx * self.hy * c3
            + self.hpx * self.hy * w2
            - self.hx * self.hpy * w1,
        )
        components_x = (
            -(self.hpx * self.hy * w2 + self.hx * self.hy * w2x),
            self.hpx * self.hy * w1 + self.hx * self.hy * w1x,
            self.hpx * self.hy * c3
            + self.hx * self.hy * c3x
            + self.hppx * self.hy * w2
            + self.hpx * self.hy * w2x
            - self.hpx * self.hpy * w1
            - self.hx * self.hpy * w1x,
        )
        components_y = (
            -(self.hx * self.hpy * w2 + self.hx * self.hy * w2y),
            self.hx * self.hpy * w1 + self.hx * self.hy * w1y,
            self.hx * self.hpy * c3
            + self.hx * self.hy * c3y
            + self.hpx * self.hpy * w2
            + self.hpx * self.hy * w2y
            - self.hx * self.hppy * w1
            - self.hx * self.hpy * w1y,
        )
        return components, components_x, components_y

    def cell_pair(
        self,
        left: tuple[np.ndarray, np.ndarray, np.ndarray],
        right: tuple[np.ndarray, np.ndarray, np.ndarray],
    ) -> float:
        return self.real_integral_2d(
            self.integral_hp2
            * (
                np.conjugate(left[0]) * right[0]
                + np.conjugate(left[1]) * right[1]
            )
            + self.integral_h2 * np.conjugate(left[2]) * right[2]
        )

    def field_cell_pair(
        self,
        field: Field,
        cell: tuple[np.ndarray, np.ndarray, np.ndarray],
    ) -> float:
        values = self.evaluate_field(field)
        return self.real_integral_2d(
            self.integral_hp
            * (
                np.conjugate(values[0]) * cell[0]
                + np.conjugate(values[1]) * cell[1]
            )
            + self.integral_h * np.conjugate(values[2]) * cell[2]
        )

    def gradient_field_cell_pair(
        self,
        field: Field,
        cell_x: tuple[np.ndarray, np.ndarray, np.ndarray],
        cell_y: tuple[np.ndarray, np.ndarray, np.ndarray],
    ) -> float:
        field_x = self.evaluate_field(field_derivative(field, 0))
        field_y = self.evaluate_field(field_derivative(field, 1))
        return self.real_integral_2d(
            self.integral_hp
            * (
                np.conjugate(field_x[0]) * cell_x[0]
                + np.conjugate(field_x[1]) * cell_x[1]
                + np.conjugate(field_y[0]) * cell_y[0]
                + np.conjugate(field_y[1]) * cell_y[1]
            )
            + self.integral_h
            * (
                np.conjugate(field_x[2]) * cell_x[2]
                + np.conjugate(field_y[2]) * cell_y[2]
            )
        )

    def gradient_cell_norm_squared(
        self,
        cell: tuple[np.ndarray, np.ndarray, np.ndarray],
        cell_x: tuple[np.ndarray, np.ndarray, np.ndarray],
        cell_y: tuple[np.ndarray, np.ndarray, np.ndarray],
    ) -> float:
        horizontal_xy = sum(
            np.abs(component) ** 2
            for component in (
                cell_x[0],
                cell_x[1],
                cell_y[0],
                cell_y[1],
            )
        )
        vertical_xy = np.abs(cell_x[2]) ** 2 + np.abs(cell_y[2]) ** 2
        vertical_derivative = (
            self.integral_hpp2
            * (np.abs(cell[0]) ** 2 + np.abs(cell[1]) ** 2)
            + self.integral_hp2 * np.abs(cell[2]) ** 2
        )
        return self.real_integral_2d(
            self.integral_hp2 * horizontal_xy
            + self.integral_h2 * vertical_xy
            + vertical_derivative
        )

    def rows(self, theta: float) -> CellRows:
        f_field, f_theta, w_field, w_theta, omega, omega_theta = (
            pure_heat_fields(theta)
        )
        cell, cell_x, cell_y = self.cell_components(w_field)
        cell_theta, _, _ = self.cell_components(w_theta)

        denominator = self.cell_pair(cell, cell)
        work = self.field_cell_pair(f_field, cell)
        enstrophy = field_norm_squared(omega)
        enstrophy_theta = 2.0 * field_pair(omega, omega_theta).real
        require(denominator > 0.0, "positive cell denominator")
        require(enstrophy > 0.0, "positive enstrophy")

        projection_coefficient = work / denominator
        cell_cell_theta = self.cell_pair(cell, cell_theta)
        field_cell_theta = self.field_cell_pair(f_field, cell_theta)
        tangent_pair = (
            field_cell_theta
            - projection_coefficient * cell_cell_theta
        )

        gradient_pf_c = (
            self.gradient_field_cell_pair(f_field, cell_x, cell_y)
            - projection_coefficient
            * self.gradient_cell_norm_squared(cell, cell_x, cell_y)
        )
        heat_main_pair = -gradient_pf_c
        # Weak evaluation of <PF,C_theta-Delta C>.  It needs only h'', while
        # a strong evaluation of curl(K_eta W) would need h'''.
        viscous_collar_pair = tangent_pair + gradient_pf_c

        common_denominator = math.sqrt(denominator * enstrophy)
        zeta = work / common_denominator
        radial = self.field_cell_pair(
            field_add(f_theta, field_scale(f_field, 16.0)), cell
        ) / common_denominator
        heat_main_tangent = heat_main_pair / common_denominator
        viscous_collar = viscous_collar_pair / common_denominator
        projective_tangent = tangent_pair / common_denominator
        normalization = -0.5 * enstrophy_theta / enstrophy * zeta
        fused_joint = radial + projective_tangent + normalization

        work_theta = (
            self.field_cell_pair(f_theta, cell)
            + self.field_cell_pair(f_field, cell_theta)
        )
        denominator_theta = 2.0 * cell_cell_theta
        zeta_theta = (
            work_theta / common_denominator
            - 0.5
            * zeta
            * (
                denominator_theta / denominator
                + enstrophy_theta / enstrophy
            )
        )
        return CellRows(
            theta=theta,
            work=work,
            denominator=denominator,
            enstrophy=enstrophy,
            zeta=zeta,
            radial=radial,
            heat_main_tangent=heat_main_tangent,
            viscous_collar=viscous_collar,
            projective_tangent=projective_tangent,
            normalization=normalization,
            fused_joint=fused_joint,
            tangent_fusion_residual=(
                projective_tangent
                - heat_main_tangent
                - viscous_collar
            ),
            scalar_differential_residual=(
                fused_joint - (zeta_theta + 16.0 * zeta)
            ),
        )


def row_payload(row: CellRows) -> dict[str, float]:
    return {
        "theta": row.theta,
        "work": row.work,
        "denominator": row.denominator,
        "enstrophy": row.enstrophy,
        "zeta": row.zeta,
        "radial": row.radial,
        "heatMainTangent": row.heat_main_tangent,
        "viscousCollar": row.viscous_collar,
        "projectiveTangent": row.projective_tangent,
        "normalization": row.normalization,
        "fusedJoint": row.fused_joint,
        "tangentFusionResidual": row.tangent_fusion_residual,
        "scalarDifferentialResidual": row.scalar_differential_residual,
    }


def integrate_rows(
    quadrature: CellQuadrature, time_order: int
) -> tuple[dict[str, object], list[CellRows]]:
    require(time_order >= 16, "time quadrature order must be at least 16")
    nodes, weights = np.polynomial.legendre.leggauss(time_order)
    theta_nodes = 0.5 * THETA_STAR * (nodes + 1.0)
    theta_weights = 0.5 * THETA_STAR * weights
    rows = [quadrature.rows(float(theta)) for theta in theta_nodes]
    zeta_positive = np.array([max(row.zeta, 0.0) for row in rows])

    accessors: dict[str, Callable[[CellRows], float]] = {
        "radial": lambda row: row.radial,
        "heatMainTangent": lambda row: row.heat_main_tangent,
        "viscousCollar": lambda row: row.viscous_collar,
        "projectiveTangent": lambda row: row.projective_tangent,
        "normalization": lambda row: row.normalization,
        "fusedJoint": lambda row: row.fused_joint,
    }
    coefficients: dict[str, object] = {}
    for label, accessor in accessors.items():
        values = np.array([accessor(row) for row in rows])
        raw_signed = float(np.sum(theta_weights * zeta_positive * values))
        raw_absolute = float(
            np.sum(theta_weights * zeta_positive * np.abs(values))
        )
        coefficients[label] = {
            "rawThetaIntegralSigned": raw_signed,
            "aggregateKMinus2CoefficientSigned": raw_signed / 16.0,
            "aggregateKMinus2CoefficientAbsolute": raw_absolute / 16.0,
        }

    initial = quadrature.rows(0.0)
    endpoint = quadrature.rows(THETA_STAR)
    zeta_squared_integral = float(
        np.sum(theta_weights * zeta_positive**2)
    )
    joint_integral = float(
        np.sum(
            theta_weights
            * zeta_positive
            * np.array([row.fused_joint for row in rows])
        )
    )
    integrated_identity_right = (
        0.5 * (endpoint.zeta**2 - initial.zeta**2)
        + 16.0 * zeta_squared_integral
    )
    identity_residual = joint_integral - integrated_identity_right

    return (
        {
            "definition": (
                "diagnostic pure-heat leading coefficient=(1/16)*"
                "integral_0^thetaStar zeta^+*row dtheta"
            ),
            "rows": coefficients,
            "zetaSquaredIntegral": zeta_squared_integral,
            "jointRawIntegral": joint_integral,
            "integratedScalarIdentityRight": integrated_identity_right,
            "integratedScalarIdentityResidual": identity_residual,
        },
        rows,
    )


def main(
    output: Path | None = None,
    spatial_order: int = 180,
    time_order: int = 48,
) -> None:
    quadrature = CellQuadrature(spatial_order)
    integrated, sampled_rows = integrate_rows(quadrature, time_order)
    initial = quadrature.rows(0.0)
    endpoint = quadrature.rows(THETA_STAR)

    maximum_fusion_residual = max(
        abs(row.tangent_fusion_residual)
        for row in [initial, endpoint, *sampled_rows]
    )
    maximum_scalar_residual = max(
        abs(row.scalar_differential_residual)
        for row in [initial, endpoint, *sampled_rows]
    )
    integrated_residual = abs(
        float(integrated["integratedScalarIdentityResidual"])
    )

    global_initial_f, _, global_initial_w, _, global_omega, _ = (
        pure_heat_fields(0.0)
    )
    global_initial_c = field_curl(global_initial_w)
    global_initial_work = field_pair(global_initial_f, global_initial_c).real
    require(abs(global_initial_work) < 2.0e-12, "exact Fourier zero entry")
    require(
        abs(quadrature.integral_h - 2.0 * math.pi) < 2.0e-5,
        "partition atom mass diagnostic",
    )
    require(
        abs(quadrature.integral_hp) < 2.0e-12,
        "partition derivative mass diagnostic",
    )
    require(maximum_fusion_residual < 2.0e-12, "tangent fusion")
    require(maximum_scalar_residual < 2.0e-11, "scalar differential identity")
    require(integrated_residual < 2.0e-10, "integrated scalar identity")
    require(endpoint.work > 0.0, "positive endpoint work")
    require(
        min(row.fused_joint for row in sampled_rows) > 0.0,
        "positive sampled fused joint source",
    )

    heat_upper_coefficient = 8.0 * (1.0 - 2.0 ** (-1.0 / 9.0)) / 2.0
    collar_absolute_coefficient = float(
        integrated["rows"]["viscousCollar"][  # type: ignore[index]
            "aggregateKMinus2CoefficientAbsolute"
        ]
    )
    tangent_absolute_coefficient = float(
        integrated["rows"]["projectiveTangent"][  # type: ignore[index]
            "aggregateKMinus2CoefficientAbsolute"
        ]
    )

    payload = {
        "status": "diagnostic-passed",
        "diagnosticOnly": True,
        "configuration": {
            "spatialGaussLegendreOrder": spatial_order,
            "timeGaussLegendreOrder": time_order,
            "thetaStar": THETA_STAR,
            "selectedParent": "kappa=4*K",
            "selectedCellCount": "K^3",
            "cutoff": "fixed R=3*pi/2 normalized tensor bump",
            "importsEarlierAuditOrExactProducer": False,
        },
        "partitionDiagnostics": {
            "atomMass": quadrature.integral_h,
            "atomMassResidual": quadrature.integral_h - 2.0 * math.pi,
            "atomDerivativeMass": quadrature.integral_hp,
            "atomSquareIntegral": quadrature.integral_h2,
            "atomDerivativeSquareIntegral": quadrature.integral_hp2,
            "atomSecondDerivativeSquareIntegral": quadrature.integral_hpp2,
        },
        "fourierWitness": {
            "globalInitialWork": global_initial_work,
            "globalInitialDenominator": field_norm_squared(global_initial_c),
            "globalInitialEnstrophy": field_norm_squared(global_omega),
            "pureHeatLimitOnly": True,
        },
        "initialCell": row_payload(initial),
        "thetaStarCell": row_payload(endpoint),
        "integratedContributions": integrated,
        "sampledSignDiagnostics": {
            "sampleCount": len(sampled_rows),
            "continuousSignCertified": False,
            "projectiveTangentMinimum": min(
                row.projective_tangent for row in sampled_rows
            ),
            "projectiveTangentMaximum": max(
                row.projective_tangent for row in sampled_rows
            ),
            "viscousCollarMinimum": min(
                row.viscous_collar for row in sampled_rows
            ),
            "viscousCollarMaximum": max(
                row.viscous_collar for row in sampled_rows
            ),
            "fusedJointMinimum": min(row.fused_joint for row in sampled_rows),
            "fusedJointMaximum": max(row.fused_joint for row in sampled_rows),
        },
        "identityDiagnostics": {
            "maximumTangentFusionResidual": maximum_fusion_residual,
            "maximumScalarDifferentialResidual": maximum_scalar_residual,
            "integratedScalarIdentityResidual": integrated_residual,
            "tangentFusion": "projectiveTangent=heatMainTangent+viscousCollar",
            "scalarIdentity": "fusedJoint=zeta_theta+16*zeta",
            "integratedIdentity": (
                "integral zeta*fusedJoint = "
                "(zeta(thetaStar)^2-zeta(0)^2)/2 + 16*integral zeta^2"
            ),
        },
        "scaling": {
            "pureHeatLeadingAggregate": "diagnostic coefficient*K^-2",
            "finiteKTransfer": {
                "zCell": "K^-3/2*(zeta+O_nu(K^-1))",
                "sourceCell": "nu*K^1/2*(tau+O_nu(K^-1))",
                "weightedTimeIntegratedCell": "K^-5",
                "statement": (
                    "selected aggregate=coefficient*K^-2+O_nu(K^-3)"
                ),
                "analyticSource": (
                    "R0.71J fixed-window convergence in a sufficiently "
                    "high weighted Sobolev norm, followed by fixed-cutoff "
                    "product and pairing estimates"
                ),
                "verifiedByThisChecker": False,
            },
        },
        "heatComparisonDiagnostic": {
            "localHeatUpper": (
                f"{heat_upper_coefficient:.17g}*nu^-1*K^-4"
            ),
            "collarAbsoluteOverHeatLowerCoefficientIfSignCertified": (
                collar_absolute_coefficient / heat_upper_coefficient
            ),
            "tangentAbsoluteOverHeatLowerCoefficientIfSignCertified": (
                tangent_absolute_coefficient / heat_upper_coefficient
            ),
            "ratioScaling": "nu*K^2",
        },
        "claims": {
            "fixedAlignedPartitionDiagnostic": True,
            "selectedParentOnly": True,
            "allThreeVectorComponentsRetained": True,
            "viscousCollarRetained": True,
            "continuousCollarSignCertified": False,
            "arbitraryPartitionsChecked": False,
            "movingPartitionsChecked": False,
            "signedFullFrameCancellationChecked": False,
            "finiteKNSETrajectoryComputed": False,
            "finiteKAsymptoticRemainderChecked": False,
            "lerayEnergyOnlyPaymentRejected": False,
            "regularityTheoremClaimed": False,
        },
        "claimBoundary": (
            "Standalone physical-space/Fourier quadrature of the pure-heat "
            "leading limit for one fixed aligned tensor partition and the "
            "selected parent.  Floating-point samples and small identity "
            "residuals are diagnostics, not interval proofs of continuous "
            "signs. The finite-K O_nu(K^-3) transfer is imported from the "
            "separate analytic R0.71J convergence argument and is not checked "
            "numerically here. The audit does not cover arbitrary or moving partitions, "
            "faces, refresh, a signed full-frame identity, a finite-K DNS, a "
            "Leray-limit theorem, or Navier-Stokes regularity."
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
    parser.add_argument("--spatial-order", type=int, default=180)
    parser.add_argument("--time-order", type=int, default=48)
    arguments = parser.parse_args()
    main(
        output=arguments.output,
        spatial_order=arguments.spatial_order,
        time_order=arguments.time_order,
    )
