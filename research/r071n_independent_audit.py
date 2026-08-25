#!/usr/bin/env python3
"""Standalone Fourier audit for the R0.71N fixed-cell scalar fusion.

The checker constructs two deterministic smooth periodic velocity fields and
their exact Navier--Stokes time jets at t=0.  It does not import either the
R0.71N exact producer or an earlier release checker.  No time stepping,
fitting, or random sampling is performed.

For each witness, the audit compares four representations of

    J_Q = z_{Q,t} + nu*kappa_j**2*z_Q,

checks the local filtered-enstrophy balance, and verifies the radial and
projective cancellations.  The calculation is repeated on 48^3, 64^3, and
80^3 Fourier grids whose relevant low-frequency outputs and quadratures are
alias-safe for this declared finite support.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


Frequency = tuple[int, int, int]
RawVector = tuple[complex, complex, complex]

KAPPA = 4.0
VISCOSITY = 0.2
GRID_ORDERS = (48, 64, 80)

VELOCITY_FREQUENCIES: tuple[Frequency, ...] = (
    (4, 0, 0),
    (0, 4, 1),
    (3, -2, 1),
    (9, 1, 0),
    (1, 10, 0),
)

# These are explicit deterministic coefficients.  Their labels retain the
# seeds used during the exploratory search, but this certificate does not use
# a random-number generator.
WITNESS_COEFFICIENTS: dict[str, tuple[RawVector, ...]] = {
    "positiveJ_seed49": (
        (
            0.5706560135801596 - 1.519366234849682j,
            1.3826081419979863 + 0.12016342330057792j,
            0.23885375802866166 + 0.10904085180674628j,
        ),
        (
            -0.5880047304878186 - 1.916230725399971j,
            -1.6378478153894873 - 0.16797497525754362j,
            -0.07022033568558819 - 0.016111082805851815j,
        ),
        (
            2.4387058312696266 + 0.5024721669981611j,
            1.0948981886035902 - 0.233435260229981j,
            0.8904387141346845 - 0.2831370029594785j,
        ),
        (
            -0.545842977489812 - 0.31626708479437887j,
            0.8160870408747694 - 0.08780224754323758j,
            1.39831438274304 + 0.7272231502471338j,
        ),
        (
            1.456685244498161 + 0.7260894458715481j,
            1.5286335388537755 + 0.7856793607175923j,
            2.2018273556190704 + 1.272185823954233j,
        ),
    ),
    "negativeJ_seed5": (
        (
            -0.8019314252534474 + 0.4204452380655215j,
            -1.324358995628145 + 1.1360465324896427j,
            -0.24836162209524854 + 0.10970639932180819j,
        ),
        (
            -0.5526473205362324 + 1.6347830429585775j,
            -0.7847803553442784 + 0.27276877584472176j,
            0.7487457707345911 - 1.2333286640307717j,
        ),
        (
            -0.9582652054360887 - 1.7321348424395848j,
            1.6000190889991115 - 0.08369619281702581j,
            0.2028824405086084 - 1.1632259734447485j,
        ),
        (
            -0.6292880940615545 + 0.5533784703532895j,
            -0.48800582327685743 - 0.06308597192528916j,
            -0.7133133716322436 - 0.5894312580326048j,
        ),
        (
            0.40963782655711695 - 0.256730126365494j,
            0.8298553070613239 - 0.9807473560440125j,
            -1.643023371405677 - 0.17315522486203205j,
        ),
    ),
}

CUTOFF_TERMS: tuple[tuple[str, Frequency, float], ...] = (
    ("cos", (1, 0, 0), 0.15),
    ("sin", (0, 1, 0), 0.10),
    ("cos", (1, 0, 1), 0.07),
    ("sin", (0, 1, -1), 0.05),
    ("cos", (0, 4, 1), 0.09),
    ("sin", (3, -2, 1), 0.06),
)

ALGEBRA_TOLERANCE = 5.0e-11
RESOLUTION_TOLERANCE = 5.0e-11
SIGN_Z_MARGIN = 1.0e-4
SIGN_J_MARGIN = 5.0e-1


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


class FourierAudit:
    """Minimal periodic Fourier implementation with normalized Haar means."""

    def __init__(self, order: int, kappa: float) -> None:
        self.order = order
        self.kappa = kappa
        frequency = np.fft.fftfreq(order, d=1.0 / order)
        self.kx, self.ky, self.kz = np.meshgrid(
            frequency, frequency, frequency, indexing="ij"
        )
        self.radius_squared = self.kx**2 + self.ky**2 + self.kz**2
        self.radius = np.sqrt(self.radius_squared)

        ratio = self.radius / kappa
        multiplier = np.zeros_like(ratio)
        core = (ratio >= 0.8) & (ratio <= 1.2)
        low = (ratio > 0.55) & (ratio < 0.8)
        high = (ratio > 1.2) & (ratio < 1.45)
        multiplier[core] = 1.0
        multiplier[low] = 0.5 * (
            1.0 - np.cos(math.pi * (ratio[low] - 0.55) / 0.25)
        )
        multiplier[high] = 0.5 * (
            1.0 + np.cos(math.pi * (ratio[high] - 1.2) / 0.25)
        )
        multiplier[self.radius == 0.0] = 0.0
        self.multiplier = multiplier

    def to_grid(self, field_hat: np.ndarray) -> np.ndarray:
        return np.fft.ifftn(field_hat, axes=(0, 1, 2)) * self.order**3

    def to_hat(self, field: np.ndarray) -> np.ndarray:
        return np.fft.fftn(field, axes=(0, 1, 2)) / self.order**3

    def curl(self, field_hat: np.ndarray) -> np.ndarray:
        kvec = np.stack([self.kx, self.ky, self.kz], axis=-1)
        return 1j * np.cross(kvec, field_hat)

    def derivative(self, field_hat: np.ndarray, axis: int) -> np.ndarray:
        frequency = (self.kx, self.ky, self.kz)[axis]
        return 1j * frequency[..., None] * field_hat

    def laplacian(self, field_hat: np.ndarray) -> np.ndarray:
        return -self.radius_squared[..., None] * field_hat

    def scalar_laplacian(self, scalar_hat: np.ndarray) -> np.ndarray:
        return -self.radius_squared * scalar_hat

    def leray(self, field_hat: np.ndarray) -> np.ndarray:
        kvec = np.stack([self.kx, self.ky, self.kz], axis=-1)
        dot = np.sum(kvec * field_hat, axis=-1)
        correction = np.zeros_like(field_hat)
        nonzero = self.radius_squared > 0.0
        correction[nonzero] = kvec[nonzero] * (
            dot[nonzero] / self.radius_squared[nonzero]
        )[..., None]
        return field_hat - correction

    def filter(self, field_hat: np.ndarray) -> np.ndarray:
        return self.multiplier[..., None] * field_hat

    @staticmethod
    def inner(left: np.ndarray, right: np.ndarray) -> complex:
        return np.mean(np.sum(np.conjugate(left) * right, axis=-1))

    def norm_squared(self, field: np.ndarray) -> float:
        return float(self.inner(field, field).real)

    def weighted_inner(
        self, left: np.ndarray, right: np.ndarray, weight: np.ndarray
    ) -> float:
        return float(self.inner(left, weight[..., None] * right).real)

    def weighted_norm_squared(
        self, field: np.ndarray, weight: np.ndarray
    ) -> float:
        return self.weighted_inner(field, field, weight)


def signed_support(frequencies: set[Frequency]) -> set[Frequency]:
    result: set[Frequency] = set()
    for frequency in frequencies:
        result.add(frequency)
        result.add(tuple(-component for component in frequency))
    return result


def minkowski_sum(
    left: set[Frequency], right: set[Frequency]
) -> set[Frequency]:
    return {
        tuple(
            left_component + right_component
            for left_component, right_component in zip(
                left_frequency, right_frequency, strict=True
            )
        )
        for left_frequency in left
        for right_frequency in right
    }


def annular_multiplier_value(frequency: Frequency, kappa: float) -> float:
    radius = math.sqrt(sum(component * component for component in frequency))
    if radius == 0.0:
        return 0.0
    ratio = radius / kappa
    if 0.8 <= ratio <= 1.2:
        return 1.0
    if 0.55 < ratio < 0.8:
        return 0.5 * (1.0 - math.cos(math.pi * (ratio - 0.55) / 0.25))
    if 1.2 < ratio < 1.45:
        return 0.5 * (1.0 + math.cos(math.pi * (ratio - 1.2) / 0.25))
    return 0.0


def filtered_support(
    support: set[Frequency], kappa: float
) -> set[Frequency]:
    return {
        frequency
        for frequency in support
        if annular_multiplier_value(frequency, kappa) > 0.0
    }


def coordinate_bound(support: set[Frequency]) -> tuple[int, int, int]:
    return tuple(
        max((abs(frequency[axis]) for frequency in support), default=0)
        for axis in range(3)
    )


def wrap_frequency(frequency: Frequency, order: int) -> Frequency:
    half = order // 2
    return tuple(((component + half) % order) - half for component in frequency)


def validate_alias_safety(order: int, kappa: float) -> dict[str, object]:
    """Validate all supports that can affect the checked low-frequency jets."""

    require(order > 0 and order % 2 == 0, "positive even Fourier order")
    velocity = signed_support(set(VELOCITY_FREQUENCIES))
    quadratic = minkowski_sum(velocity, velocity)
    cubic = minkowski_sum(quadratic, velocity)
    cutoff = {(0, 0, 0)} | signed_support(
        {frequency for _, frequency, _ in CUTOFF_TERMS}
    )

    quadratic_bound = coordinate_bound(quadratic)
    require(
        all(2 * bound < order for bound in quadratic_bound),
        "quadratic NSE jet is not represented below Nyquist",
    )

    # The cubic L_t product need not be globally represented at order 48.
    # It is used only after T_j.  Enumerate every true cubic frequency and
    # reject any wrapped high mode that could enter the selected annulus.
    low_aliases: list[dict[str, Frequency]] = []
    for frequency in cubic:
        wrapped = wrap_frequency(frequency, order)
        if wrapped != frequency and annular_multiplier_value(wrapped, kappa) > 0.0:
            low_aliases.append({"true": frequency, "wrapped": wrapped})
    require(not low_aliases, "cubic alias enters the annular output")

    filtered_velocity = filtered_support(velocity, kappa)
    filtered_quadratic = filtered_support(quadratic, kappa)
    filtered_cubic = filtered_support(cubic, kappa)
    final_fields = filtered_velocity | filtered_quadratic | filtered_cubic
    final_bound = coordinate_bound(final_fields)
    cutoff_bound = coordinate_bound(cutoff)
    quadrature_bound = tuple(
        2 * field_component + cutoff_component
        for field_component, cutoff_component in zip(
            final_bound, cutoff_bound, strict=True
        )
    )
    require(
        all(bound < order for bound in quadrature_bound),
        "checked cutoff-weighted zero-mode quadrature can alias",
    )

    return {
        "order": order,
        "quadraticCoordinateBound": quadratic_bound,
        "cubicCoordinateBound": coordinate_bound(cubic),
        "filteredFinalCoordinateBound": final_bound,
        "cutoffCoordinateBound": cutoff_bound,
        "quadratureCoordinateBound": quadrature_bound,
        "cubicAliasesIntoAnnulus": 0,
        "passed": True,
    }


def add_real_mode(
    field_hat: np.ndarray, frequency: Frequency, raw: RawVector
) -> None:
    order = field_hat.shape[0]
    kvec = np.asarray(frequency, dtype=float)
    vector = np.asarray(raw, dtype=complex)
    vector -= kvec * np.dot(kvec, vector) / np.dot(kvec, kvec)
    positive = tuple(component % order for component in frequency)
    negative = tuple((-component) % order for component in frequency)
    field_hat[positive] += vector
    field_hat[negative] += np.conjugate(vector)


def deterministic_velocity(
    order: int, coefficients: tuple[RawVector, ...]
) -> np.ndarray:
    require(
        len(coefficients) == len(VELOCITY_FREQUENCIES),
        "one coefficient vector per velocity frequency",
    )
    field_hat = np.zeros((order, order, order, 3), dtype=complex)
    for frequency, raw in zip(
        VELOCITY_FREQUENCIES, coefficients, strict=True
    ):
        add_real_mode(field_hat, frequency, raw)
    return field_hat


def build_cutoff(audit: FourierAudit) -> np.ndarray:
    coordinate = 2.0 * math.pi * np.arange(audit.order) / audit.order
    x, y, z = np.meshgrid(coordinate, coordinate, coordinate, indexing="ij")
    coordinates = (x, y, z)
    cutoff = np.full_like(x, 1.1)
    for kind, frequency, coefficient in CUTOFF_TERMS:
        phase = sum(
            component * coordinate_component
            for component, coordinate_component in zip(
                frequency, coordinates, strict=True
            )
        )
        cutoff += coefficient * (
            np.cos(phase) if kind == "cos" else np.sin(phase)
        )
    require(float(cutoff.min()) > 0.0, "strictly positive cutoff")
    return cutoff


def scalar_relative_residual(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0)


def vector_relative_residual(left: np.ndarray, right: np.ndarray) -> float:
    difference = np.asarray(left) - np.asarray(right)
    return float(
        np.linalg.norm(difference.ravel())
        / max(
            float(np.linalg.norm(np.asarray(left).ravel())),
            float(np.linalg.norm(np.asarray(right).ravel())),
            1.0,
        )
    )


def real_grid(audit: FourierAudit, field_hat: np.ndarray, label: str) -> np.ndarray:
    value = audit.to_grid(field_hat)
    reality_residual = float(np.max(np.abs(value.imag)))
    require(reality_residual < 2.0e-11, f"real grid reconstruction: {label}")
    return value.real


def evaluate_witness(
    order: int, label: str, coefficients: tuple[RawVector, ...]
) -> dict[str, object]:
    alias_certificate = validate_alias_safety(order, KAPPA)
    audit = FourierAudit(order, KAPPA)
    nu = VISCOSITY
    lam = nu * KAPPA**2

    u_hat = deterministic_velocity(order, coefficients)
    u = real_grid(audit, u_hat, "u")
    divergence_hat = 1j * (
        audit.kx * u_hat[..., 0]
        + audit.ky * u_hat[..., 1]
        + audit.kz * u_hat[..., 2]
    )
    divergence_residual = float(np.max(np.abs(divergence_hat)))
    require(divergence_residual < 1.0e-12, "divergence-free velocity")

    omega_hat = audit.curl(u_hat)
    omega = real_grid(audit, omega_hat, "omega")
    lamb_hat = audit.to_hat(np.cross(u, omega))
    l_hat = audit.leray(lamb_hat)
    l_field = real_grid(audit, l_hat, "L")

    # Exact physical-time NSE jet at t=0.
    u_t_hat = l_hat + nu * audit.laplacian(u_hat)
    u_t = real_grid(audit, u_t_hat, "u_t")
    omega_t_hat = audit.curl(l_hat) + nu * audit.laplacian(omega_hat)
    omega_t = real_grid(audit, omega_t_hat, "omega_t")
    omega_t_from_u = audit.curl(u_t_hat)
    omega_jet_residual = vector_relative_residual(
        omega_t_hat, omega_t_from_u
    )
    require(omega_jet_residual < ALGEBRA_TOLERANCE, "omega_t NSE jet")

    lamb_t = np.cross(u_t, omega) + np.cross(u, omega_t)
    l_t_hat = audit.leray(audit.to_hat(lamb_t))

    f_hat = audit.filter(l_hat)
    f = real_grid(audit, f_hat, "F")
    f_t_hat = audit.filter(l_t_hat)
    f_t = real_grid(audit, f_t_hat, "F_t")
    g_hat = audit.curl(f_hat)
    g = real_grid(audit, g_hat, "G")
    g_t_hat = audit.curl(f_t_hat)
    g_t = real_grid(audit, g_t_hat, "G_t")

    w_hat = audit.filter(omega_hat)
    w = real_grid(audit, w_hat, "W")
    w_t_hat = audit.filter(omega_t_hat)
    w_t = real_grid(audit, w_t_hat, "W_t")
    w_tt_hat = g_t_hat + nu * audit.laplacian(w_t_hat)
    w_tt = real_grid(audit, w_tt_hat, "W_tt")

    cutoff = build_cutoff(audit)
    cutoff_hat = audit.to_hat(cutoff)
    cutoff_laplacian = real_grid(
        audit, audit.scalar_laplacian(cutoff_hat), "Delta chi"
    )
    cutoff_minimum = float(cutoff.min())

    c_hat = audit.curl(audit.to_hat(cutoff[..., None] * w))
    c = real_grid(audit, c_hat, "C")
    c_t_hat = audit.curl(audit.to_hat(cutoff[..., None] * w_t))
    c_t = real_grid(audit, c_t_hat, "C_t")

    h_hat = (KAPPA**2 - audit.radius_squared)[..., None] * w_hat
    h = real_grid(audit, h_hat, "H")
    s_field = g + nu * h
    m_hat = audit.curl(audit.to_hat(cutoff[..., None] * s_field))
    m = real_grid(audit, m_hat, "M")
    m_from_c_t = c_t + lam * c
    m_fusion_residual = vector_relative_residual(m, m_from_c_t)
    require(m_fusion_residual < ALGEBRA_TOLERANCE, "M=C_t+lambda*C")

    y_value = audit.norm_squared(omega)
    y_t = 2.0 * float(audit.inner(omega, omega_t).real)
    d_value = audit.norm_squared(c)
    d_t = 2.0 * float(audit.inner(c, c_t).real)
    b_value = float(audit.inner(f, c).real)
    root = math.sqrt(y_value * d_value)
    radius = math.sqrt(d_value)
    z_value = b_value / root
    require(y_value > 0.0 and d_value > 0.0, "hard denominators")

    curl_l = real_grid(audit, audit.curl(l_hat), "curl L")
    omega_gradient_squared = 0.0
    for axis in range(3):
        omega_derivative = real_grid(
            audit, audit.derivative(omega_hat, axis), f"grad omega {axis}"
        )
        omega_gradient_squared += audit.norm_squared(omega_derivative)
    y_t_nse = (
        2.0 * float(audit.inner(omega, curl_l).real)
        - 2.0 * nu * omega_gradient_squared
    )
    y_t_residual = scalar_relative_residual(y_t, y_t_nse)
    require(y_t_residual < ALGEBRA_TOLERANCE, "global enstrophy derivative")

    # Three independent forms of B_t.
    b_t_product = float(audit.inner(f_t, c).real) + float(
        audit.inner(f, c_t).real
    )
    b_t_curl_product = audit.weighted_inner(g_t, w, cutoff) + (
        audit.weighted_inner(g, w_t, cutoff)
    )
    i_value = audit.weighted_inner(g, s_field, cutoff)
    acceleration = audit.weighted_inner(g_t, w, cutoff)
    b_t_fused = acceleration + i_value - lam * b_value
    b_t_product_residual = scalar_relative_residual(
        b_t_product, b_t_curl_product
    )
    b_t_fused_residual = scalar_relative_residual(b_t_product, b_t_fused)
    require(b_t_product_residual < ALGEBRA_TOLERANCE, "B_t product rule")
    require(b_t_fused_residual < ALGEBRA_TOLERANCE, "B_t fused jet")

    normalization = 0.5 * b_value * (
        y_t / y_value + d_t / d_value
    )
    j_direct = (b_t_product + lam * b_value - normalization) / root

    # Projective representation.
    direction = c / radius
    projected_f = f - (b_value / d_value) * c
    m_radial_coefficient = float(audit.inner(m, c).real) / d_value
    projected_m = m - m_radial_coefficient * c
    projective_pairing = float(audit.inner(projected_f, projected_m).real)
    n_field = f_t + lam * f
    j_projective = (
        float(audit.inner(n_field, direction).real) / math.sqrt(y_value)
        + projective_pairing / root
        - 0.5 * z_value * y_t / y_value
    )

    radial_pairing = i_value - (b_value / d_value) * (
        0.5 * d_t + lam * d_value
    )
    radial_pairing_residual = scalar_relative_residual(
        projective_pairing, radial_pairing
    )
    require(
        radial_pairing_residual < ALGEBRA_TOLERANCE,
        "radial projective pairing",
    )

    b_t_projective = (
        float(audit.inner(n_field, c).real)
        + projective_pairing
        + b_value * d_t / (2.0 * d_value)
        - lam * b_value
    )
    b_t_projective_residual = scalar_relative_residual(
        b_t_product, b_t_projective
    )
    require(
        b_t_projective_residual < ALGEBRA_TOLERANCE,
        "B_t radial/projective recombination",
    )

    j_radial_n = (
        float(audit.inner(n_field, c).real) / root
        + i_value / root
        - z_value * (d_t / (2.0 * d_value) + lam)
        - 0.5 * z_value * y_t / y_value
    )
    lambda_cancellation_residual = scalar_relative_residual(
        float(audit.inner(n_field, c).real) / root - lam * z_value,
        float(audit.inner(f_t, c).real) / root,
    )
    require(
        lambda_cancellation_residual < ALGEBRA_TOLERANCE,
        "lambda cancellation in N radial form",
    )

    # Nonnegative square plus explicit signed residual.
    square_field = g + 0.5 * nu * h
    positive_square = audit.weighted_norm_squared(square_field, cutoff)
    h_square = audit.weighted_norm_squared(h, cutoff)
    viscous_mismatch = 0.25 * nu**2 * h_square
    signed_residual = acceleration - viscous_mismatch - normalization
    j_square_residual = (positive_square + signed_residual) / root

    # Local filtered-enstrophy and second-jet representation.
    e_value = 0.5 * audit.weighted_norm_squared(w, cutoff)
    e_t = audit.weighted_inner(w, w_t, cutoff)
    e_tt = audit.weighted_norm_squared(w_t, cutoff) + (
        audit.weighted_inner(w, w_tt, cutoff)
    )
    lap_w = real_grid(audit, audit.laplacian(w_hat), "Delta W")
    lap_w_t = real_grid(audit, audit.laplacian(w_t_hat), "Delta W_t")
    d_chi = -audit.weighted_inner(w, lap_w, cutoff)
    d_chi_t = -audit.weighted_inner(w_t, lap_w, cutoff) - (
        audit.weighted_inner(w, lap_w_t, cutoff)
    )

    gradient_w_squared = np.zeros_like(cutoff)
    for axis in range(3):
        derivative = real_grid(
            audit, audit.derivative(w_hat, axis), f"grad W {axis}"
        )
        gradient_w_squared += np.sum(derivative**2, axis=-1)
    d_chi_gradient = float(
        np.mean(
            cutoff * gradient_w_squared
            - 0.5 * cutoff_laplacian * np.sum(w**2, axis=-1)
        )
    )
    curl_w = real_grid(audit, audit.curl(w_hat), "curl W")
    d_chi_curl = float(audit.inner(c, curl_w).real)
    d_chi_h = 2.0 * KAPPA**2 * e_value - (
        audit.weighted_inner(w, h, cutoff)
    )

    local_balance = e_t + nu * d_chi
    local_balance_residual = scalar_relative_residual(b_value, local_balance)
    local_d_gradient_residual = scalar_relative_residual(
        d_chi, d_chi_gradient
    )
    local_d_curl_residual = scalar_relative_residual(d_chi, d_chi_curl)
    local_d_h_residual = scalar_relative_residual(d_chi, d_chi_h)
    b_t_second_jet = e_tt + nu * d_chi_t
    b_t_second_jet_residual = scalar_relative_residual(
        b_t_product, b_t_second_jet
    )
    for value, check_label in (
        (local_balance_residual, "local enstrophy B=e_t+nu*D_chi"),
        (local_d_gradient_residual, "D_chi gradient form"),
        (local_d_curl_residual, "D_chi cutoff-curl form"),
        (local_d_h_residual, "D_chi annular-mismatch form"),
        (b_t_second_jet_residual, "B_t local second jet"),
    ):
        require(value < ALGEBRA_TOLERANCE, check_label)

    second_jet_numerator = (
        e_tt
        + nu * d_chi_t
        + lam * (e_t + nu * d_chi)
        - normalization
    )
    j_second_jet = second_jet_numerator / root
    residual_rewritten = -positive_square + second_jet_numerator
    square_cancellation_residual = scalar_relative_residual(
        signed_residual, residual_rewritten
    )
    require(
        square_cancellation_residual < ALGEBRA_TOLERANCE,
        "positive square cancels inside signed residual",
    )

    j_representations = {
        "direct": j_direct,
        "projective": j_projective,
        "radialN": j_radial_n,
        "squarePlusResidual": j_square_residual,
        "localSecondJet": j_second_jet,
    }
    j_reference = j_direct
    j_representation_residuals = {
        representation: scalar_relative_residual(value, j_reference)
        for representation, value in j_representations.items()
    }
    max_j_residual = max(j_representation_residuals.values())
    require(max_j_residual < ALGEBRA_TOLERANCE, "all J representations")

    require(z_value > SIGN_Z_MARGIN, f"positive z witness: {label}")
    if label.startswith("positiveJ"):
        require(j_direct > SIGN_J_MARGIN, "strict positive J witness")
    else:
        require(j_direct < -SIGN_J_MARGIN, "strict negative J witness")

    return {
        "label": label,
        "order": order,
        "aliasSafety": alias_certificate,
        "cutoffMinimum": cutoff_minimum,
        "cell": {
            "Y": y_value,
            "Y_t": y_t,
            "B": b_value,
            "B_t": b_t_product,
            "d": d_value,
            "d_t": d_t,
            "z": z_value,
            "e": e_value,
            "e_t": e_t,
            "e_tt": e_tt,
            "DChi": d_chi,
            "DChi_t": d_chi_t,
        },
        "signedFusion": {
            "positiveSquare": positive_square,
            "acceleration": acceleration,
            "viscousMismatch": viscous_mismatch,
            "normalization": normalization,
            "signedResidual": signed_residual,
            "positiveSquarePlusResidual": positive_square + signed_residual,
            "secondJetNumerator": second_jet_numerator,
        },
        "J": j_representations,
        "checks": {
            "divergenceResidual": divergence_residual,
            "omegaJetRelativeResidual": omega_jet_residual,
            "YtNseRelativeResidual": y_t_residual,
            "MViscousFusionRelativeResidual": m_fusion_residual,
            "BtProductRuleRelativeResidual": b_t_product_residual,
            "BtFusedJetRelativeResidual": b_t_fused_residual,
            "radialPairingRelativeResidual": radial_pairing_residual,
            "BtProjectiveRecombinationRelativeResidual": (
                b_t_projective_residual
            ),
            "lambdaCancellationRelativeResidual": (
                lambda_cancellation_residual
            ),
            "localBalanceRelativeResidual": local_balance_residual,
            "DChiGradientRelativeResidual": local_d_gradient_residual,
            "DChiCurlRelativeResidual": local_d_curl_residual,
            "DChiMismatchRelativeResidual": local_d_h_residual,
            "BtSecondJetRelativeResidual": b_t_second_jet_residual,
            "squareCancellationRelativeResidual": (
                square_cancellation_residual
            ),
            "JRepresentationRelativeResiduals": (
                j_representation_residuals
            ),
            "maxJRepresentationRelativeResidual": max_j_residual,
        },
    }


def complex_vector_payload(vector: RawVector) -> list[list[float]]:
    return [[float(value.real), float(value.imag)] for value in vector]


def compare_resolutions(
    results: list[dict[str, object]], label: str
) -> dict[str, object]:
    scalar_paths = {
        "Y": ("cell", "Y"),
        "Y_t": ("cell", "Y_t"),
        "B": ("cell", "B"),
        "B_t": ("cell", "B_t"),
        "d": ("cell", "d"),
        "d_t": ("cell", "d_t"),
        "z": ("cell", "z"),
        "J": ("J", "direct"),
        "positiveSquare": ("signedFusion", "positiveSquare"),
        "signedResidual": ("signedFusion", "signedResidual"),
        "secondJetNumerator": ("signedFusion", "secondJetNumerator"),
    }

    def extract(result: dict[str, object], path: tuple[str, str]) -> float:
        section = result[path[0]]
        require(isinstance(section, dict), "resolution comparison section")
        return float(section[path[1]])

    agreement: dict[str, float] = {}
    for quantity, path in scalar_paths.items():
        values = [extract(result, path) for result in results]
        reference = values[-1]
        agreement[quantity] = max(
            scalar_relative_residual(value, reference) for value in values
        )

    maximum = max(agreement.values())
    require(
        maximum < RESOLUTION_TOLERANCE,
        f"48/64/80 resolution agreement: {label}",
    )
    return {
        "relativeResidualsAgainstOrder80": agreement,
        "maximumRelativeResidual": maximum,
        "tolerance": RESOLUTION_TOLERANCE,
        "passed": True,
    }


def run() -> dict[str, object]:
    witness_results: dict[str, list[dict[str, object]]] = {}
    resolution_checks: dict[str, dict[str, object]] = {}
    for label, coefficients in WITNESS_COEFFICIENTS.items():
        results = [
            evaluate_witness(order, label, coefficients)
            for order in GRID_ORDERS
        ]
        witness_results[label] = results
        resolution_checks[label] = compare_resolutions(results, label)

    return {
        "release": "R0.71N",
        "status": "passed",
        "configuration": {
            "domain": "T^3 with normalized Haar measure",
            "gridOrders": list(GRID_ORDERS),
            "kappa": KAPPA,
            "viscosity": VISCOSITY,
            "time": 0.0,
            "timeStepping": False,
            "randomness": False,
            "velocityFrequencies": [list(value) for value in VELOCITY_FREQUENCIES],
            "witnessCoefficients": {
                label: [complex_vector_payload(vector) for vector in vectors]
                for label, vectors in WITNESS_COEFFICIENTS.items()
            },
            "cutoffConstant": 1.1,
            "cutoffTerms": [
                {
                    "kind": kind,
                    "frequency": list(frequency),
                    "coefficient": coefficient,
                }
                for kind, frequency, coefficient in CUTOFF_TERMS
            ],
            "thresholds": {
                "algebraRelativeResidual": ALGEBRA_TOLERANCE,
                "resolutionRelativeResidual": RESOLUTION_TOLERANCE,
                "positiveZMargin": SIGN_Z_MARGIN,
                "signedJMargin": SIGN_J_MARGIN,
            },
        },
        "witnesses": witness_results,
        "resolutionAgreement": resolution_checks,
        "checkedObservations": {
            "bothWitnessesHavePositiveZ": True,
            "positiveJ_seed49HasPositiveJ": True,
            "negativeJ_seed5HasNegativeJ": True,
            "positiveSquareIsCanceledInCompleteSecondJetLedger": True,
        },
        "claimBoundary": (
            "Standalone finite Fourier initial-jet audit only.  It checks "
            "exact identities for two declared smooth periodic fields at "
            "t=0 and shows that the complete signed scalar can have either "
            "sign while z_Q is positive.  It performs no time stepping and "
            "proves no sign theorem on a time interval, continuation "
            "criterion, Leray-limit estimate, regularity result, singularity "
            "result, originality claim, or Millennium-problem conclusion."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    payload = run()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output is None:
        print(rendered, end="")
    else:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
