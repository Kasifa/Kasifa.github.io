#!/usr/bin/env python3
"""Finite certificate for R0.74S Step 6 cross-channel recombination.

The certificate checks exact finite algebra, stopped-family genealogy,
sampled cutoff monotonicity, the scalar saturation witness, and statement
sentinels.  It does not machine-prove the local-energy calculation, a PDE
sign theorem, or any Navier--Stokes realization of the scalar witness.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import re
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
NOTE = Path(
    os.environ.get(
        "R074S_CROSS_NOTE",
        REPO / "research/r074s_cross_channel_recombination_no_gain.md",
    )
)
JSON_OUT = Path(
    os.environ.get(
        "R074S_CROSS_JSON",
        REPO / "research/r074s_cross_channel_recombination_certificate.json",
    )
)
REPORT_OUT = Path(
    os.environ.get(
        "R074S_CROSS_REPORT",
        REPO / "research/r074s_cross_channel_recombination_certificate_report.md",
    )
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fs(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def exact(identifier: str, left: Fraction, right: Fraction, note: str) -> dict:
    return {
        "id": identifier,
        "left": fs(left),
        "right": fs(right),
        "margin": fs(left - right),
        "note": note,
        "pass": left == right,
    }


def gamma_proxy(shell_max: int, ratio: Fraction = Fraction(3, 5)) -> dict[int, Fraction]:
    return {k: ratio ** (k - 1) for k in range(1, shell_max + 2)}


def internal_edges(shells: set[int], shell_max: int) -> set[int]:
    return {
        m
        for m in range(2, shell_max + 1)
        if m - 1 in shells and m in shells
    }


def components(shells: set[int]) -> list[tuple[int, int]]:
    ordered = sorted(shells)
    if not ordered:
        return []
    result: list[tuple[int, int]] = []
    first = last = ordered[0]
    for shell in ordered[1:]:
        if shell == last + 1:
            last = shell
        else:
            result.append((first, last))
            first = last = shell
    result.append((first, last))
    return result


def ball_plus(time: int, shell: int) -> Fraction:
    """Deterministic rational endpoint fixture; positivity is not needed."""
    return Fraction(((17 * time + 7 * shell * shell + 3 * shell) % 37) - 11, 19)


def ball_minus(time: int, shell: int) -> Fraction:
    """A second deterministic rational endpoint fixture."""
    return Fraction(((13 * time + 5 * shell * shell + 11 * shell) % 41) - 13, 23)


def shell_row(
    gamma: dict[int, Fraction], shell: int, time: int
) -> Fraction:
    return gamma[shell] * (
        ball_plus(time, shell + 1) - ball_minus(time, shell)
    )


def boundary_row(
    gamma: dict[int, Fraction], boundary: int, time: int
) -> Fraction:
    return gamma[boundary] * (
        ball_plus(time, boundary) - ball_minus(time, boundary)
    )


def stopped_channel_value(
    shell_set: set[int],
    stops: dict[int, int],
    shell_max: int,
    *,
    include_mismatch: bool,
    outer_shift: int = 1,
    gap_sign: int = 1,
    root_sign: int = 1,
    overlap_rule: str = "max",
) -> Fraction:
    """Evaluate S.114, with switches used by the negative mutations."""
    tau = 3
    gamma = gamma_proxy(shell_max)
    value = Fraction(0)
    for shell in sorted(shell_set):
        rho = (
            tau
            if shell == 1 or shell - 1 not in shell_set
            else stops[shell - 1]
        )
        lam = tau if shell + 1 not in shell_set else stops[shell + 1]
        if stops[shell] < rho:
            value += root_sign * -gamma[shell] * (
                ball_minus(rho, shell) - ball_minus(stops[shell], shell)
            )
        if stops[shell] < lam:
            ball_index = shell + outer_shift
            value += gamma[shell] * (
                ball_plus(lam, ball_index)
                - ball_plus(stops[shell], ball_index)
            )
    for boundary in sorted(internal_edges(shell_set, shell_max)):
        if overlap_rule == "max":
            start = max(stops[boundary - 1], stops[boundary])
        elif overlap_rule == "min":
            start = min(stops[boundary - 1], stops[boundary])
        else:
            raise ValueError(f"unknown overlap rule: {overlap_rule}")
        d_m = gamma[boundary - 1] - gamma[boundary]
        value += gap_sign * d_m * (
            ball_plus(tau, boundary) - ball_plus(start, boundary)
        )
        if include_mismatch:
            value += boundary_row(gamma, boundary, tau) - boundary_row(
                gamma, boundary, start
            )
    return value


def stopped_row_recombination_check() -> dict:
    """Exhaust S.115 over all five-shell masks and three-level stop maps."""
    shell_max = 5
    tau = 3
    gamma = gamma_proxy(shell_max)
    failures = []
    configurations = 0
    for mask in range(1 << shell_max):
        shell_set = {
            k for k in range(1, shell_max + 1) if mask & (1 << (k - 1))
        }
        ordered = sorted(shell_set)
        for assignment in itertools.product(range(3), repeat=len(ordered)):
            stops = dict(zip(ordered, assignment))
            configurations += 1
            left = stopped_channel_value(
                shell_set,
                stops,
                shell_max,
                include_mismatch=True,
            )
            right = sum(
                (
                    shell_row(gamma, shell, tau)
                    - shell_row(gamma, shell, stops[shell])
                    for shell in ordered
                ),
                Fraction(0),
            )
            if left != right and len(failures) < 20:
                failures.append(
                    {
                        "mask": mask,
                        "stops": stops,
                        "four_channel_row": fs(left),
                        "stopped_shell_row": fs(right),
                    }
                )
    return {
        "id": "exact_rational_stopped_row_recombination_with_ties",
        "shell_max": shell_max,
        "configurations_checked": configurations,
        "failures": failures,
        "pass": not failures,
    }


def theta_piecewise(value: Fraction) -> Fraction:
    """Exact monotone transition proxy used only on the finite grid."""
    if value <= -1:
        return Fraction(0)
    if value >= 0:
        return Fraction(1)
    return value + 1


def chi_minus(shell: int, radius: Fraction) -> Fraction:
    delta = Fraction(1, 8)
    hard_radius = Fraction(2**shell)
    return 1 - theta_piecewise((radius - hard_radius) / delta)


def chi_plus(shell: int, radius: Fraction) -> Fraction:
    delta = Fraction(1, 8)
    hard_radius = Fraction(2**shell)
    return theta_piecewise((hard_radius - radius) / delta)


def beta(shell: int, radius: Fraction) -> Fraction:
    delta = Fraction(1, 8)
    hard_radius = Fraction(2**shell)
    return theta_piecewise((radius - hard_radius) / delta) * theta_piecewise(
        (hard_radius - radius) / delta
    )


def psi(shell: int, radius: Fraction) -> Fraction:
    delta = Fraction(1, 8)
    inner = Fraction(2**shell)
    outer = Fraction(2 ** (shell + 1))
    return theta_piecewise((radius - inner) / delta) * theta_piecewise(
        (outer - radius) / delta
    )


def omega_value(
    shell_set: set[int],
    radius: Fraction,
    gamma: dict[int, Fraction],
    shell_max: int,
) -> Fraction:
    shell_part = sum(
        (gamma[k] * psi(k, radius) for k in shell_set), Fraction(0)
    )
    boundary_part = sum(
        (
            gamma[m] * beta(m, radius)
            for m in internal_edges(shell_set, shell_max)
        ),
        Fraction(0),
    )
    return shell_part - boundary_part


def omega_insertion_monotonicity_check() -> dict:
    """Sample S.132--S.133 exactly on a rational lift grid."""
    shell_max = 6
    gamma = gamma_proxy(shell_max, Fraction(32, 35))
    samples = {Fraction(0)}
    for boundary in range(1, shell_max + 2):
        hard_radius = Fraction(2**boundary)
        samples.update(hard_radius + Fraction(offset, 64) for offset in range(-12, 13))
    for shell in range(1, shell_max + 1):
        samples.add(Fraction(3 * 2 ** (shell - 1)))
    samples = {value for value in samples if value >= 0}

    pair_failures = []
    pair_comparisons = 0
    for shell in range(1, shell_max + 1):
        for radius in sorted(samples):
            cutoff_identity_left = psi(shell, radius) - beta(
                shell, radius
            ) - beta(shell + 1, radius)
            cutoff_identity_right = chi_minus(shell + 1, radius) - chi_plus(
                shell, radius
            )
            weighted_left = (
                gamma[shell] * beta(shell, radius)
                + gamma[shell + 1] * beta(shell + 1, radius)
            )
            weighted_right = gamma[shell] * psi(shell, radius)
            pair_comparisons += 3
            if (
                cutoff_identity_left != cutoff_identity_right
                or cutoff_identity_left < 0
                or weighted_left > weighted_right
            ) and len(pair_failures) < 20:
                pair_failures.append(
                    {
                        "shell": shell,
                        "radius_over_R": fs(radius),
                        "identity_left": fs(cutoff_identity_left),
                        "identity_right": fs(cutoff_identity_right),
                        "weighted_left": fs(weighted_left),
                        "weighted_right": fs(weighted_right),
                    }
                )

    insertion_failures = []
    insertion_comparisons = 0
    for mask in range(1 << shell_max):
        shell_set = {
            k for k in range(1, shell_max + 1) if mask & (1 << (k - 1))
        }
        for shell in range(1, shell_max + 1):
            if shell in shell_set:
                continue
            enlarged = shell_set | {shell}
            for radius in sorted(samples):
                before = omega_value(shell_set, radius, gamma, shell_max)
                after = omega_value(enlarged, radius, gamma, shell_max)
                insertion_comparisons += 1
                if (before < 0 or after < before) and len(insertion_failures) < 20:
                    insertion_failures.append(
                        {
                            "mask": mask,
                            "inserted_shell": shell,
                            "radius_over_R": fs(radius),
                            "before": fs(before),
                            "after": fs(after),
                        }
                    )
    return {
        "id": "exact_rational_omega_pair_and_insertion_monotonicity_grid",
        "shell_max": shell_max,
        "radii_checked": len(samples),
        "pair_comparisons": pair_comparisons,
        "insertion_comparisons": insertion_comparisons,
        "pair_failures": pair_failures,
        "insertion_failures": insertion_failures,
        "pass": not pair_failures and not insertion_failures,
    }


def phi_value(
    shell_set: set[int],
    time: int,
    gamma: dict[int, Fraction],
    shell_max: int,
) -> Fraction:
    return sum(
        (shell_row(gamma, shell, time) for shell in shell_set), Fraction(0)
    ) - sum(
        (
            boundary_row(gamma, boundary, time)
            for boundary in internal_edges(shell_set, shell_max)
        ),
        Fraction(0),
    )


def event_jump_identity_check() -> dict:
    """Exhaust the three-channel event identity, including tied epochs."""
    shell_max = 5
    tau = 3
    gamma = gamma_proxy(shell_max)
    failures = []
    configurations = 0
    events_checked = 0
    for mask in range(1 << shell_max):
        shell_set = {
            k for k in range(1, shell_max + 1) if mask & (1 << (k - 1))
        }
        ordered = sorted(shell_set)
        for assignment in itertools.product(range(3), repeat=len(ordered)):
            stops = dict(zip(ordered, assignment))
            configurations += 1
            direct = stopped_channel_value(
                shell_set,
                stops,
                shell_max,
                include_mismatch=False,
            )
            genealogy = phi_value(shell_set, tau, gamma, shell_max)
            for event in sorted(set(stops.values())):
                before = {k for k in shell_set if stops[k] < event}
                after = {k for k in shell_set if stops[k] <= event}
                genealogy -= phi_value(after, event, gamma, shell_max) - phi_value(
                    before, event, gamma, shell_max
                )
                events_checked += 1
            expanded = sum(
                (
                    shell_row(gamma, shell, tau)
                    - shell_row(gamma, shell, stops[shell])
                    for shell in ordered
                ),
                Fraction(0),
            )
            expanded -= sum(
                (
                    boundary_row(gamma, boundary, tau)
                    - boundary_row(
                        gamma,
                        boundary,
                        max(stops[boundary - 1], stops[boundary]),
                    )
                    for boundary in internal_edges(shell_set, shell_max)
                ),
                Fraction(0),
            )
            if (direct != genealogy or direct != expanded) and len(failures) < 20:
                failures.append(
                    {
                        "mask": mask,
                        "stops": stops,
                        "three_channel_row": fs(direct),
                        "event_genealogy": fs(genealogy),
                        "shell_minus_boundary": fs(expanded),
                    }
                )
    return {
        "id": "exact_rational_three_channel_event_jump_identity_with_ties",
        "shell_max": shell_max,
        "configurations_checked": configurations,
        "events_checked": events_checked,
        "failures": failures,
        "pass": not failures,
    }


def dissipation_corrected_s137_check() -> dict:
    """Exhaust the strengthened S.137 on exact discrete density fixtures.

    The cutoff values are sampled exactly on a rational radial grid.  At each
    sample, E is a nonnegative time-dependent density, D is a nonnegative
    cumulative density, and Q is one of three signed rational fixtures.  The
    check does not assume the desired inequality: it reconstructs the direct
    root/outer/gap rows and the event-insertion rows independently.
    """
    shell_max = 4
    tau = 3
    gamma = gamma_proxy(shell_max, Fraction(5, 8))
    samples = {Fraction(0)}
    for boundary in range(1, shell_max + 2):
        hard_radius = Fraction(2**boundary)
        samples.update(
            hard_radius + offset
            for offset in (
                Fraction(-1, 8),
                Fraction(-1, 16),
                Fraction(0),
                Fraction(1, 16),
                Fraction(1, 8),
            )
        )
    for shell in range(1, shell_max + 1):
        samples.add(Fraction(3 * 2 ** (shell - 1)))
    radii = sorted(value for value in samples if value >= 0)

    def energy_density(time: int) -> tuple[Fraction, ...]:
        return tuple(
            Fraction(((11 * time + 7 * index * index + 3 * index) % 23) + 1, 17)
            for index in range(len(radii))
        )

    def dissipation_density(time: int) -> tuple[Fraction, ...]:
        values = []
        for index in range(len(radii)):
            value = Fraction(((5 * index + 2) % 11) + 1, 19)
            for step in range(time):
                value += Fraction(
                    ((7 * step + 3 * index * index + index) % 13) + 1,
                    29,
                )
            values.append(value)
        return tuple(values)

    def quadratic_density(time: int, variant: int) -> tuple[Fraction, ...]:
        denominator = 17 + 2 * variant
        return tuple(
            Fraction(
                ((13 * time + 5 * index * index + 7 * index + 11 * variant) % 29)
                - 14,
                denominator,
            )
            for index in range(len(radii))
        )

    def pair(cutoff: tuple[Fraction, ...], density: tuple[Fraction, ...]) -> Fraction:
        return sum(
            (cutoff[index] * density[index] for index in range(len(radii))),
            Fraction(0),
        )

    def omega_vector(shell_set: set[int]) -> tuple[Fraction, ...]:
        return tuple(
            omega_value(shell_set, radius, gamma, shell_max) for radius in radii
        )

    def ball_vector(shell: int, side: str) -> tuple[Fraction, ...]:
        if side == "plus":
            return tuple(chi_plus(shell, radius) for radius in radii)
        if side == "minus":
            return tuple(chi_minus(shell, radius) for radius in radii)
        raise ValueError(f"unknown ball side: {side}")

    energy = {time: energy_density(time) for time in range(tau + 1)}
    dissipation = {
        time: dissipation_density(time) for time in range(tau + 1)
    }

    failures = []
    configurations = 0
    stopped_configurations = 0
    tied_configurations = 0
    event_insertions = 0
    density_pairings = 0
    for mask in range(1 << shell_max):
        shell_set = {
            k for k in range(1, shell_max + 1) if mask & (1 << (k - 1))
        }
        ordered = sorted(shell_set)
        for assignment in itertools.product(range(3), repeat=len(ordered)):
            stops = dict(zip(ordered, assignment))
            stopped_configurations += 1
            events = sorted(set(stops.values()))
            has_tie = len(events) < len(ordered)
            omega_terminal = omega_vector(shell_set)
            delta_rows = []
            delta_sum = [Fraction(0) for _ in radii]
            insertion_nonnegative = True
            for event in events:
                before = {k for k in shell_set if stops[k] < event}
                after = {k for k in shell_set if stops[k] <= event}
                before_vector = omega_vector(before)
                after_vector = omega_vector(after)
                delta = tuple(
                    after_vector[index] - before_vector[index]
                    for index in range(len(radii))
                )
                insertion_nonnegative = insertion_nonnegative and all(
                    value >= 0 for value in delta
                )
                for index, value in enumerate(delta):
                    delta_sum[index] += value
                delta_rows.append((event, delta))
                event_insertions += 1
            delta_partition = tuple(delta_sum) == omega_terminal

            for variant in range(3):
                configurations += 1
                if has_tie:
                    tied_configurations += 1
                quadratic = {
                    time: quadratic_density(time, variant)
                    for time in range(tau + 1)
                }
                flux = {
                    time: tuple(
                        energy[time][index]
                        + dissipation[time][index]
                        - quadratic[time][index]
                        for index in range(len(radii))
                    )
                    for time in range(tau + 1)
                }
                densities = {
                    "E": energy,
                    "D": dissipation,
                    "Q": quadratic,
                    "F": flux,
                }

                def ball_row(
                    row: str, time: int, shell: int, side: str
                ) -> Fraction:
                    nonlocal density_pairings
                    density_pairings += 1
                    return pair(ball_vector(shell, side), densities[row][time])

                def direct_three_channel(row: str) -> Fraction:
                    value = Fraction(0)
                    for shell in ordered:
                        rho = (
                            tau
                            if shell == 1 or shell - 1 not in shell_set
                            else stops[shell - 1]
                        )
                        lam = (
                            tau if shell + 1 not in shell_set else stops[shell + 1]
                        )
                        if stops[shell] < rho:
                            value -= gamma[shell] * (
                                ball_row(row, rho, shell, "minus")
                                - ball_row(row, stops[shell], shell, "minus")
                            )
                        if stops[shell] < lam:
                            value += gamma[shell] * (
                                ball_row(row, lam, shell + 1, "plus")
                                - ball_row(
                                    row, stops[shell], shell + 1, "plus"
                                )
                            )
                    for boundary in sorted(
                        internal_edges(shell_set, shell_max)
                    ):
                        start = max(stops[boundary - 1], stops[boundary])
                        weight_drop = gamma[boundary - 1] - gamma[boundary]
                        value += weight_drop * (
                            ball_row(row, tau, boundary, "plus")
                            - ball_row(row, start, boundary, "plus")
                        )
                    return value

                event_values = {}
                insertion_energy_values = []
                for row in ("E", "D", "Q", "F"):
                    terminal = pair(omega_terminal, densities[row][tau])
                    insertions = [
                        pair(delta, densities[row][event])
                        for event, delta in delta_rows
                    ]
                    density_pairings += 1 + len(insertions)
                    event_values[row] = terminal - sum(
                        insertions, Fraction(0)
                    )
                    if row == "E":
                        insertion_energy_values = insertions

                d_post_sum = sum(
                    (
                        pair(delta, dissipation[tau])
                        - pair(delta, dissipation[event])
                        for event, delta in delta_rows
                    ),
                    Fraction(0),
                )
                density_pairings += 2 * len(delta_rows)
                phi_e = pair(omega_terminal, energy[tau])
                phi_d = pair(omega_terminal, dissipation[tau])
                q_event = event_values["Q"]
                w_three = direct_three_channel("F")
                direct_rows = {
                    row: direct_three_channel(row) for row in ("E", "D", "Q")
                }
                identity_rhs = (
                    phi_e
                    - sum(insertion_energy_values, Fraction(0))
                    + d_post_sum
                    - q_event
                )
                first_bound = phi_e + d_post_sum + abs(q_event)
                terminal_bound = phi_e + phi_d + abs(q_event)
                conditions = {
                    "delta_omega_partitions_terminal_omega": delta_partition,
                    "delta_omega_nonnegative": insertion_nonnegative,
                    "insertion_energy_nonnegative": all(
                        value >= 0 for value in insertion_energy_values
                    ),
                    "d_post_exact_event_decomposition": (
                        d_post_sum == event_values["D"]
                    ),
                    "d_post_nonnegative": d_post_sum >= 0,
                    "d_post_bounded_by_terminal_d": (
                        d_post_sum <= phi_d
                    ),
                    "direct_E_event_identity": (
                        direct_rows["E"] == event_values["E"]
                    ),
                    "direct_D_event_identity": (
                        direct_rows["D"] == event_values["D"]
                    ),
                    "direct_Q_event_identity": (
                        direct_rows["Q"] == event_values["Q"]
                    ),
                    "direct_F_event_identity": (
                        w_three == event_values["F"]
                    ),
                    "E_plus_D_minus_Q_identity": (
                        w_three == identity_rhs
                    ),
                    "strengthened_one_sided_bound": (
                        max(w_three, Fraction(0)) <= first_bound
                    ),
                    "terminal_clock_corollary": (
                        first_bound <= terminal_bound
                    ),
                }
                if not all(conditions.values()) and len(failures) < 20:
                    failures.append(
                        {
                            "mask": mask,
                            "stops": stops,
                            "Q_variant": variant,
                            "W_three": fs(w_three),
                            "identity_rhs": fs(identity_rhs),
                            "D_post": fs(d_post_sum),
                            "Phi_I_E": fs(phi_e),
                            "Phi_I_D": fs(phi_d),
                            "Q_event": fs(q_event),
                            "conditions": conditions,
                        }
                    )
    return {
        "id": "exact_rational_dissipation_corrected_S137_with_ties",
        "shell_max": shell_max,
        "radii_checked": len(radii),
        "stopped_configurations_checked": stopped_configurations,
        "Q_density_variants": 3,
        "configurations_checked": configurations,
        "tied_configurations_checked": tied_configurations,
        "event_insertions_checked": event_insertions,
        "density_pairings_checked": density_pairings,
        "failures": failures,
        "pass": not failures,
    }


def block_residual_abel_check() -> dict:
    """Check S.138--S.139 for every block in the first twelve shells."""
    shell_max = 12
    gamma = gamma_proxy(shell_max, Fraction(7, 10))
    plus = {
        m: Fraction(m * m + 3 * m + 5, 11)
        for m in range(1, shell_max + 2)
    }
    minus = {m: Fraction(2, 3) * plus[m] for m in plus}
    boundary = {
        m: gamma[m] * (plus[m] - minus[m])
        for m in range(1, shell_max + 1)
    }
    residual = {
        m: gamma[m] * (plus[m + 1] - plus[m])
        for m in range(1, shell_max + 1)
    }
    shell = {
        m: gamma[m] * (plus[m + 1] - minus[m])
        for m in range(1, shell_max + 1)
    }
    failures = []
    rows = []
    for first in range(1, shell_max + 1):
        for last in range(first, shell_max + 1):
            ball_form = -gamma[first] * minus[first]
            ball_form += gamma[last] * plus[last + 1]
            ball_form += sum(
                (
                    (gamma[m - 1] - gamma[m]) * plus[m]
                    for m in range(first + 1, last + 1)
                ),
                Fraction(0),
            )
            residual_form = boundary[first] + sum(
                (residual[m] for m in range(first, last + 1)),
                Fraction(0),
            )
            root_shell_form = shell[first] + sum(
                (residual[m] for m in range(first + 1, last + 1)),
                Fraction(0),
            )
            passed = ball_form == residual_form == root_shell_form
            rows.append(
                {
                    "block": [first, last],
                    "ball_form": fs(ball_form),
                    "boundary_plus_residual": fs(residual_form),
                    "root_shell_plus_residual": fs(root_shell_form),
                    "pass": passed,
                }
            )
            if not passed and len(failures) < 20:
                failures.append(rows[-1])
    return {
        "id": "exact_rational_blockwise_residual_abel_all_blocks_through_12",
        "blocks_checked": len(rows),
        "rows": rows,
        "failures": failures,
        "pass": not failures,
    }


def genealogy_count_check() -> dict:
    """Exhaust S.141 over all eight-shell masks and tied stop maps."""
    shell_max = 8
    tau = 3
    failures = []
    configurations = 0
    for mask in range(1 << shell_max):
        shell_set = {
            k for k in range(1, shell_max + 1) if mask & (1 << (k - 1))
        }
        ordered = sorted(shell_set)
        for assignment in itertools.product(range(3), repeat=len(ordered)):
            stops = dict(zip(ordered, assignment))
            configurations += 1
            edge_set = internal_edges(shell_set, shell_max)
            component_count = len(components(shell_set))
            tie_count = sum(
                stops[m - 1] == stops[m] for m in edge_set
            )
            root_count = 0
            outer_count = 0
            for shell in ordered:
                rho = (
                    tau
                    if shell == 1 or shell - 1 not in shell_set
                    else stops[shell - 1]
                )
                lam = tau if shell + 1 not in shell_set else stops[shell + 1]
                root_count += stops[shell] < rho
                outer_count += stops[shell] < lam
            n_value = len(shell_set)
            conditions = {
                "internal_edges": len(edge_set) == n_value - component_count,
                "root_outer": (
                    root_count + outer_count
                    == n_value + component_count - tie_count
                ),
                "all_three_families": (
                    root_count + outer_count + len(edge_set)
                    == 2 * n_value - tie_count
                ),
            }
            if not all(conditions.values()) and len(failures) < 20:
                failures.append(
                    {
                        "mask": mask,
                        "stops": stops,
                        "n": n_value,
                        "components": component_count,
                        "ties": tie_count,
                        "roots": root_count,
                        "outers": outer_count,
                        "internal": len(edge_set),
                        "conditions": conditions,
                    }
                )
    return {
        "id": "exhaustive_eight_shell_genealogy_count_with_ties",
        "configurations_checked": configurations,
        "failures": failures,
        "pass": not failures,
    }


def scalar_witness_check() -> dict:
    """Check the one-block scalar witness exactly for N=1,...,64."""
    rows = []
    failures = []
    for n_value in range(1, 65):
        shell_set = set(range(1, n_value + 1))
        activation_time = 1
        tau = 2
        stops = {shell: activation_time for shell in shell_set}
        event_times = sorted(set(stops.values()))
        active_sets = {
            time: {
                shell
                for shell in shell_set
                if stops[shell] < time <= tau
            }
            for time in range(tau + 1)
        }
        component_counts = {
            time: len(components(active))
            for time, active in active_sets.items()
        }
        merger_count = 0
        for event in event_times:
            before = {
                shell for shell in shell_set if stops[shell] < event
            }
            after = {
                shell for shell in shell_set if stops[shell] <= event
            }
            before_components = components(before)
            for first, last in components(after):
                inherited_components = sum(
                    first <= old_first and old_last <= last
                    for old_first, old_last in before_components
                )
                merger_count += max(0, inherited_components - 1)

        gamma = gamma_proxy(n_value, Fraction(1, 2))
        balls = {1: Fraction(0)}
        for shell in range(1, n_value + 1):
            balls[shell + 1] = balls[shell] + 1 / gamma[shell]
        outer = gamma[n_value] * balls[n_value + 1]
        gap = sum(
            (
                (gamma[m - 1] - gamma[m]) * balls[m]
                for m in range(2, n_value + 1)
            ),
            Fraction(0),
        )
        root = Fraction(0)
        mismatch = Fraction(0)
        total = root + outer + gap + mismatch
        clock_at_stop = {shell: Fraction(0) for shell in shell_set}
        clock_at_terminal = {
            shell: Fraction(1) for shell in shell_set
        }
        positive_variations = {
            shell: max(
                clock_at_terminal[shell] - clock_at_stop[shell],
                Fraction(0),
            )
            for shell in shell_set
        }
        stopped_shell_work = sum(
            positive_variations.values(), Fraction(0)
        )
        y2_squared = sum(
            (
                variation * variation
                for variation in positive_variations.values()
            ),
            Fraction(0),
        )
        epsilon = outer - 1
        conditions = {
            "same_nonnegative_sign": outer >= 0 and gap >= 0,
            "finite_telescoping": total == stopped_shell_work,
            "matched_square_for_unit_positive_variations": (
                y2_squared == stopped_shell_work
            ),
            "unit_positive_variations": all(
                variation == 1
                for variation in positive_variations.values()
            ),
            "strict_upcrossing": all(
                positive_variations[shell]
                > Fraction(1, 4) * clock_at_terminal[shell]
                for shell in shell_set
            ),
            "one_block": max(component_counts.values()) == 1,
            "one_epoch": len(event_times) == 1,
            "zero_mergers": merger_count == 0,
            "outer_split": outer == 1 + epsilon,
            "gap_split": (
                gap == stopped_shell_work - 1 - epsilon
            ),
        }
        row = {
            "N": n_value,
            "root": fs(root),
            "outer": fs(outer),
            "weight_drop": fs(gap),
            "mismatch": fs(mismatch),
            "total_stopped_work": fs(total),
            "Y2_squared": fs(y2_squared),
            "positive_variations_checked": len(positive_variations),
            "active_time_cells_checked": len(active_sets),
            "activation_epochs": len(event_times),
            "maximum_active_components": max(component_counts.values()),
            "block_mergers": merger_count,
            "conditions": conditions,
            "pass": all(conditions.values()),
        }
        rows.append(row)
        if not row["pass"]:
            failures.append(row)
    return {
        "id": "exact_one_block_scalar_witness_N_1_through_64",
        "weight_ratio_proxy": "1/2",
        "stopped_work_symbol": "W_N^sc",
        "pde_realization_asserted": False,
        "rows": rows,
        "failures": failures,
        "pass": not failures,
    }


def epsilon_exponent_gap_check() -> dict:
    """Check the exact exponent gap behind the epsilon_N upper bound."""
    rows = []
    failures = []
    comparisons = 0
    for n_value in range(2, 65):
        gaps = []
        for shell in range(1, n_value):
            gap = Fraction(4 ** (n_value - 1) - 4 ** (shell - 1), 32)
            gaps.append(gap)
            comparisons += 1
        minimum_gap = min(gaps)
        expected_gap = Fraction(3 * 4 ** (n_value - 2), 32)
        conditions = {
            "minimum_at_adjacent_shell": minimum_gap == gaps[-1],
            "adjacent_gap_exact": gaps[-1] == expected_gap,
            "all_ratios_have_claimed_exponent_gap": all(
                gap >= expected_gap for gap in gaps
            ),
            "epsilon_has_N_minus_one_terms": len(gaps) == n_value - 1,
        }
        row = {
            "N": n_value,
            "minimum_exponent_gap": fs(minimum_gap),
            "claimed_exponent_gap": fs(expected_gap),
            "terms_in_epsilon": len(gaps),
            "conditions": conditions,
            "pass": all(conditions.values()),
        }
        rows.append(row)
        if not row["pass"]:
            failures.append(row)
    return {
        "id": "exact_epsilon_N_super_gaussian_exponent_gap_N_2_through_64",
        "comparisons_checked": comparisons,
        "rows": rows,
        "failures": failures,
        "pass": not failures,
    }


def compact(body: str) -> str:
    return re.sub(r"\s+", "", body)


def structural_checks(body: str) -> list[dict]:
    tags = re.findall(r"\\tag\{S\.(\d+)\}", body)
    expected = [str(k) for k in range(112, 142)]
    compressed = compact(body)
    prose = re.sub(r"\s+", " ", body)
    checks = [
        {
            "id": "tags_consecutive",
            "actual": tags,
            "expected": expected,
            "pass": tags == expected,
        },
        {
            "id": "tags_unique",
            "actual_count": len(tags),
            "unique_count": len(set(tags)),
            "pass": len(tags) == len(set(tags)) == len(expected),
        },
    ]
    required_text = (
        "For \(Q,F,K\), these are identities of their canonical representatives",
        "For \(E,D\), they are used only at the good stopping and terminal times.",
        "no time differentiability of the \(E,D\) rows is used",
        "has not made the difficult term smaller",
        "This is a rigorous route rejection inside the scalar completed-clock algebra.",
        "It is not a Navier--Stokes solution or a PDE counterexample.",
        "The root and mismatch completed rows vanish.",
        "the outer and gap contributions have the same nonnegative sign",
        r"The symbol \(W_N^{\rm sc}\) is not the work of a constructed PDE solution.",
        "no disjointness of different periodic copies is required.",
        "All shells with stop \(a\) may be inserted one at a time in any order.",
        "Each summand is nonnegative because \(\delta\Omega_a\ge0\) and the dissipation row is nondecreasing.",
        r"the dissipation bracket is exactly \(D_{\rm post}\).",
        "all starting and merge-time completed clocks",
        "The remaining terminal clock, however, has no hidden cancellation.",
        "complete \(\ell^1\) residual mass",
        "not a dimension-free \(\ell^2\) packing",
        "The witness does **not** rule out a theorem",
        "A PDE-weighted genealogy theorem",
        "remain **OPEN / NOT CLAIMED**",
        "**NOT CLAY.**",
    )
    required_compact = (
        "X_{k,R}&=\\gamma_k(\\mathscrX_{k+1,R}^+-\\mathscrX_{k,R}^-)",
        "X_{m,R}^{\\partial}&=\\gamma_m(\\mathscrX_{m,R}^+-\\mathscrX_{m,R}^-)",
        "\\mathfrakC_X=\\sum_{k\\inI}\\Delta_{\\sigma_k}^{\\tau}X_{k,R}",
        "\\mathfrakC_F=W_R^M(\\tau;I,\\boldsymbol\\sigma)",
        "\\mathfrakC_K=\\sum_{k\\inI}\\Delta_{\\sigma_k}^{\\tau}K_{k,R}",
        "I_N=\\{1,\\ldots,N\\}",
        "\\gamma_NB_{N+1}(\\tau)+\\sum_{m=2}^{N}d_mB_m(\\tau)=N",
        "W_N^{\\rmsc}=\\mathfrakC_F=\\mathfrakC_K=N",
        "Y_{2,R}^{\\rmsf}=\\sqrtN",
        "\\varepsilon_N:=\\sum_{j=1}^{N-1}\\frac{\\gamma_N}{\\gamma_j}",
        "\\varepsilon_N\\le(N-1)\\exp\\!\\left(-\\frac{3\\cdot4^{N-2}}{32}\\right)",
        "\\Omega_A^R:=\\sum_{k\\inA}\\gamma_k\\Psi_k^R-\\sum_{m\\inA^\\partial}\\gamma_mB_m^R",
        "0\\le\\gamma_kB_k^R+\\gamma_{k+1}B_{k+1}^R\\le\\gamma_k\\Psi_k^R",
        "\\Omega_{A\\cup\\{k\\}}^R-\\Omega_A^R",
        "\\Phi_A(t):=\\mathscrK_R[\\Omega_A^R](t)",
        "\\Phi_{A_a^+}(a)-\\Phi_{A_a^-}(a)\\ge0",
        "W_{R,3}^M=\\Phi_I^F(\\tau)-\\sum_a[\\Phi_{A_a^+}^F(a)-\\Phi_{A_a^-}^F(a)]",
        "D_{\\rmpost}:=\\sum_a\\left(\\mathscrD_R[\\delta\\Omega_a](\\tau)-\\mathscrD_R[\\delta\\Omega_a](a)\\right)",
        "0\\leD_{\\rmpost}\\le\\Phi_I^D(\\tau)",
        "[W_{R,3}^M]_+\\le\\Phi_I^E(\\tau)+D_{\\rmpost}+CA_R",
        "\\le\\Phi_I(\\tau)+CA_R",
        "r_m(t):=K_{m,R}(t)-K_{m,R}^{\\partial}(t)\\ge0",
        "K_{a,R}^{\\partial}(t)+\\sum_{m=a}^{b}r_m(t)",
        "|I^\\partial|&=n-c(I)",
        "|I_{\\rmrt}|+|I_{\\rmout}|+|I^\\partial|&=2n-",
    )
    forbidden = (
        "global regularity is proved",
        "the Millennium problem is solved",
        "the scalar witness is a Navier--Stokes solution",
        "W_N^{\\rm sc} is the work of a Navier--Stokes solution",
        "the PDE sign theorem is proved",
        "the dissipation-dominated branch is proved",
    )
    for sentinel in required_text:
        checks.append(
            {
                "id": "required_text_" + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
                "sentinel": sentinel,
                "pass": sentinel in prose,
            }
        )
    for sentinel in required_compact:
        checks.append(
            {
                "id": "required_formula_" + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
                "sentinel": sentinel,
                "pass": sentinel in compressed,
            }
        )
    for phrase in forbidden:
        checks.append(
            {
                "id": "forbidden_" + hashlib.sha256(phrase.encode()).hexdigest()[:12],
                "phrase": phrase,
                "pass": phrase not in body,
            }
        )
    checks.extend(
        [
            {
                "id": "display_math_balanced",
                "left_count": body.count("\\["),
                "right_count": body.count("\\]"),
                "pass": body.count("\\[") == body.count("\\]"),
            },
            {
                "id": "inline_math_balanced",
                "left_count": body.count("\\("),
                "right_count": body.count("\\)"),
                "pass": body.count("\\(") == body.count("\\)"),
            },
            {
                "id": "no_disallowed_control_characters",
                "pass": not any(ord(ch) < 32 and ch not in "\n\t" for ch in body),
            },
            {
                "id": "no_malformed_mathscr_command",
                "forbidden_fragment": "=mathscr",
                "pass": "=mathscr" not in body,
            },
        ]
    )
    return checks


def mutation_failure_count(
    *,
    outer_shift: int = 1,
    gap_sign: int = 1,
    root_sign: int = 1,
    overlap_rule: str = "max",
) -> tuple[int, dict | None]:
    """Count counterexamples to a deliberately mutated S.115 row."""
    shell_max = 5
    tau = 3
    gamma = gamma_proxy(shell_max)
    failures = 0
    first_failure = None
    for mask in range(1 << shell_max):
        shell_set = {
            k for k in range(1, shell_max + 1) if mask & (1 << (k - 1))
        }
        ordered = sorted(shell_set)
        for assignment in itertools.product(range(3), repeat=len(ordered)):
            stops = dict(zip(ordered, assignment))
            left = stopped_channel_value(
                shell_set,
                stops,
                shell_max,
                include_mismatch=True,
                outer_shift=outer_shift,
                gap_sign=gap_sign,
                root_sign=root_sign,
                overlap_rule=overlap_rule,
            )
            right = sum(
                (
                    shell_row(gamma, shell, tau)
                    - shell_row(gamma, shell, stops[shell])
                    for shell in ordered
                ),
                Fraction(0),
            )
            if left != right:
                failures += 1
                if first_failure is None:
                    first_failure = {
                        "mask": mask,
                        "stops": stops,
                        "mutated": fs(left),
                        "correct_target": fs(right),
                    }
    return failures, first_failure


def d_post_sign_reversal_mutation_check() -> dict:
    """Reject a reversed post-dissipation increment on an exact fixture.

    The three-channel work is reconstructed directly from its root, outer,
    and weight-drop rows.  The desired one-sided estimate is never used as
    input.  Only the sign of each D(tau)-D(a) post increment is then reversed.
    """
    shell_max = 3
    tau = 3
    gamma = gamma_proxy(shell_max, Fraction(5, 8))
    radii = sorted(
        {
            Fraction(0),
            Fraction(15, 8),
            Fraction(2),
            Fraction(33, 16),
            Fraction(31, 8),
            Fraction(4),
            Fraction(65, 16),
            Fraction(63, 8),
            Fraction(8),
            Fraction(129, 16),
            Fraction(12),
        }
    )
    shell_set = {1, 2}
    stops = {1: 0, 2: 1}
    ordered = sorted(shell_set)

    def pair(
        cutoff: tuple[Fraction, ...],
        density: tuple[Fraction, ...],
    ) -> Fraction:
        return sum(
            (
                cutoff[index] * density[index]
                for index in range(len(radii))
            ),
            Fraction(0),
        )

    def omega_vector(shells: set[int]) -> tuple[Fraction, ...]:
        return tuple(
            omega_value(shells, radius, gamma, shell_max)
            for radius in radii
        )

    def ball_vector(shell: int, side: str) -> tuple[Fraction, ...]:
        if side == "plus":
            return tuple(chi_plus(shell, radius) for radius in radii)
        if side == "minus":
            return tuple(chi_minus(shell, radius) for radius in radii)
        raise ValueError(f"unknown ball side: {side}")

    energy = {
        time: tuple(
            Fraction((time + 1) * (index + 2), 13)
            for index in range(len(radii))
        )
        for time in range(tau + 1)
    }
    dissipation = {
        time: tuple(
            Fraction(time * (index + 1), 11)
            for index in range(len(radii))
        )
        for time in range(tau + 1)
    }
    quadratic = {
        time: tuple(
            Fraction((-1) ** index * (3 * time + index - 4), 17)
            for index in range(len(radii))
        )
        for time in range(tau + 1)
    }
    flux = {
        time: tuple(
            energy[time][index]
            + dissipation[time][index]
            - quadratic[time][index]
            for index in range(len(radii))
        )
        for time in range(tau + 1)
    }

    delta_rows = []
    for event in sorted(set(stops.values())):
        before = {
            shell for shell in shell_set if stops[shell] < event
        }
        after = {
            shell for shell in shell_set if stops[shell] <= event
        }
        before_vector = omega_vector(before)
        after_vector = omega_vector(after)
        delta_rows.append(
            (
                event,
                tuple(
                    after_vector[index] - before_vector[index]
                    for index in range(len(radii))
                ),
            )
        )

    def ball_row(
        density: dict[int, tuple[Fraction, ...]],
        time: int,
        shell: int,
        side: str,
    ) -> Fraction:
        return pair(ball_vector(shell, side), density[time])

    def direct_three_channel(
        density: dict[int, tuple[Fraction, ...]],
    ) -> Fraction:
        value = Fraction(0)
        for shell in ordered:
            rho = (
                tau
                if shell == 1 or shell - 1 not in shell_set
                else stops[shell - 1]
            )
            lam = (
                tau
                if shell + 1 not in shell_set
                else stops[shell + 1]
            )
            if stops[shell] < rho:
                value -= gamma[shell] * (
                    ball_row(density, rho, shell, "minus")
                    - ball_row(
                        density, stops[shell], shell, "minus"
                    )
                )
            if stops[shell] < lam:
                value += gamma[shell] * (
                    ball_row(density, lam, shell + 1, "plus")
                    - ball_row(
                        density, stops[shell], shell + 1, "plus"
                    )
                )
        for boundary in sorted(
            internal_edges(shell_set, shell_max)
        ):
            start = max(stops[boundary - 1], stops[boundary])
            d_m = gamma[boundary - 1] - gamma[boundary]
            value += d_m * (
                ball_row(density, tau, boundary, "plus")
                - ball_row(density, start, boundary, "plus")
            )
        return value

    omega_terminal = omega_vector(shell_set)
    w_three = direct_three_channel(flux)
    w_three_event = pair(omega_terminal, flux[tau]) - sum(
        (
            pair(delta, flux[event])
            for event, delta in delta_rows
        ),
        Fraction(0),
    )
    phi_e = pair(omega_terminal, energy[tau])
    insertion_e = sum(
        (
            pair(delta, energy[event])
            for event, delta in delta_rows
        ),
        Fraction(0),
    )
    q_event = pair(omega_terminal, quadratic[tau]) - sum(
        (
            pair(delta, quadratic[event])
            for event, delta in delta_rows
        ),
        Fraction(0),
    )
    post_increment_terms = [
        pair(delta, dissipation[tau])
        - pair(delta, dissipation[event])
        for event, delta in delta_rows
    ]
    d_post = sum(post_increment_terms, Fraction(0))
    mutated_post_increment_terms = [
        -term for term in post_increment_terms
    ]
    mutated_d_post = sum(
        mutated_post_increment_terms, Fraction(0)
    )
    correct_reconstruction = (
        phi_e - insertion_e + d_post - q_event
    )
    mutated_reconstruction = (
        phi_e - insertion_e + mutated_d_post - q_event
    )
    counterexample_found = (
        w_three == w_three_event == correct_reconstruction
        and d_post > 0
        and mutated_reconstruction != w_three
    )
    exact_rational_values = [
        *radii,
        *gamma.values(),
        *(
            value
            for _, delta in delta_rows
            for value in delta
        ),
        *(
            value
            for density in (energy, dissipation, quadratic, flux)
            for values in density.values()
            for value in values
        ),
        *post_increment_terms,
        *mutated_post_increment_terms,
        d_post,
        mutated_d_post,
        w_three,
        w_three_event,
        correct_reconstruction,
        mutated_reconstruction,
    ]
    conditions = {
        "all_arithmetic_exact_rational": all(
            isinstance(value, Fraction)
            for value in exact_rational_values
        ),
        "cutoff_fixture_nonempty": (
            bool(shell_set)
            and bool(delta_rows)
            and all(
                any(value != 0 for value in delta)
                for _, delta in delta_rows
            )
        ),
        "delta_omega_nonnegative": all(
            value >= 0
            for _, delta in delta_rows
            for value in delta
        ),
        "density_fixture_nonempty": all(
            any(
                value != 0
                for values in density.values()
                for value in values
            )
            for density in (energy, dissipation, quadratic)
        ),
        "energy_nonnegative": all(
            value >= 0
            for values in energy.values()
            for value in values
        ),
        "dissipation_cumulative": all(
            dissipation[time + 1][index]
            >= dissipation[time][index]
            for time in range(tau)
            for index in range(len(radii))
        ),
        "quadratic_density_signed": (
            any(
                value < 0
                for values in quadratic.values()
                for value in values
            )
            and any(
                value > 0
                for values in quadratic.values()
                for value in values
            )
        ),
        "direct_and_event_W3_agree": w_three == w_three_event,
        "correct_D_post_strictly_positive": d_post > 0,
        "correct_reconstruction_matches_W3": (
            correct_reconstruction == w_three
        ),
        "reversed_post_increment_breaks_reconstruction": (
            mutated_reconstruction != w_three
        ),
        "mutation_gap_is_twice_D_post": (
            w_three - mutated_reconstruction == 2 * d_post
        ),
    }
    return {
        "id": "d_post_post_increment_sign_reversed_exact_fixture",
        "arithmetic": "fractions.Fraction",
        "target_inequality_used_as_input": False,
        "shells": ordered,
        "stops": stops,
        "terminal_time": tau,
        "radii_checked": len(radii),
        "event_insertions_checked": len(delta_rows),
        "nonzero_delta_omega_entries": sum(
            value != 0
            for _, delta in delta_rows
            for value in delta
        ),
        "post_increment_terms": [
            fs(term) for term in post_increment_terms
        ],
        "correct_D_post": fs(d_post),
        "mutated_D_post": fs(mutated_d_post),
        "W_three_from_channels": fs(w_three),
        "W_three_from_event_definition": fs(w_three_event),
        "correct_reconstruction": fs(correct_reconstruction),
        "mutated_reconstruction": fs(mutated_reconstruction),
        "counterexamples_found": int(counterexample_found),
        "conditions": conditions,
        "pass": counterexample_found and all(conditions.values()),
    }


def negative_mutation_checks(body: str) -> list[dict]:
    """Require dangerous coefficient, orientation, and sign mutations to fail."""
    variants = (
        ("outer_k_plus_one_shift_removed", {"outer_shift": 0}),
        ("weight_drop_coefficient_sign_reversed", {"gap_sign": -1}),
        ("root_completed_clock_sign_reversed", {"root_sign": -1}),
        ("internal_overlap_max_replaced_by_min", {"overlap_rule": "min"}),
    )
    checks = []
    for identifier, options in variants:
        failure_count, first_failure = mutation_failure_count(**options)
        checks.append(
            {
                "id": identifier,
                "counterexamples_found": failure_count,
                "first_counterexample": first_failure,
                "pass": failure_count > 0,
            }
        )

    checks.append(d_post_sign_reversal_mutation_check())

    structural_mutations = (
        (
            "event_jump_terminal_minus_sign_mutation_rejected",
            "=\\Phi_I^F(\\tau)\n  -\\sum_a",
            "=\\Phi_I^F(\\tau)\n  +\\sum_a",
        ),
        (
            "residual_sign_mutation_rejected",
            "r_m(t):=K_{m,R}(t)-K_{m,R}^{\\partial}(t)\\ge0",
            "r_m(t):=K_{m,R}^{\\partial}(t)-K_{m,R}(t)\\ge0",
        ),
        (
            "d_post_upper_bound_reversal_rejected",
            "0\\le D_{\\rm post}\\le\\Phi_I^D(\\tau).",
            "0\\le \\Phi_I^D(\\tau)\\le D_{\\rm post}.",
        ),
        (
            "scalar_work_pde_boundary_mutation_rejected",
            r"The symbol \(W_N^{\rm sc}\) is not the work",
            r"The symbol \(W_N^{\rm sc}\) is the work",
        ),
        (
            "epsilon_exponent_gap_mutation_rejected",
            "\\frac{3\\cdot4^{N-2}}{32}",
            "\\frac{4\\cdot4^{N-2}}{32}",
        ),
    )
    for identifier, correct, wrong in structural_mutations:
        mutated_body = body.replace(correct, wrong, 1)
        mutation_checks = structural_checks(mutated_body)
        checks.append(
            {
                "id": identifier,
                "correct_sentinel_present": correct in body,
                "wrong_sentinel_inserted": wrong in mutated_body,
                "mutated_structural_result": (
                    "PASS" if all(item["pass"] for item in mutation_checks) else "FAIL"
                ),
                "pass": (
                    correct in body
                    and wrong in mutated_body
                    and not all(item["pass"] for item in mutation_checks)
                ),
            }
        )
    return checks


def build_report(payload: dict) -> str:
    summary = payload["summary"]
    finite = {item["id"]: item for item in payload["finite_checks"]}
    lines = [
        "# R0.74S cross-channel recombination certificate report",
        "",
        "## Result",
        "",
        f"**{summary['result']}** — {summary['exact_passed']}/"
        f"{summary['exact_total']} exact ledger rows, "
        f"{summary['finite_passed']}/{summary['finite_total']} finite checks, "
        f"{summary['structural_passed']}/{summary['structural_total']} structural checks, "
        f"and {summary['negative_passed']}/{summary['negative_total']} negative mutations passed.",
        "",
        "## Exact ledger",
        "",
        "| Check | Left | Right | Margin |",
        "|---|---:|---:|---:|",
    ]
    for item in payload["exact_checks"]:
        lines.append(
            f"| {item['id']} | {item['left']} | {item['right']} | {item['margin']} |"
        )
    recombination = finite["exact_rational_stopped_row_recombination_with_ties"]
    omega = finite["exact_rational_omega_pair_and_insertion_monotonicity_grid"]
    event = finite["exact_rational_three_channel_event_jump_identity_with_ties"]
    corrected = finite["exact_rational_dissipation_corrected_S137_with_ties"]
    abel = finite["exact_rational_blockwise_residual_abel_all_blocks_through_12"]
    count = finite["exhaustive_eight_shell_genealogy_count_with_ties"]
    witness = finite["exact_one_block_scalar_witness_N_1_through_64"]
    epsilon_gap = finite[
        "exact_epsilon_N_super_gaussian_exponent_gap_N_2_through_64"
    ]
    d_post_mutation = next(
        item
        for item in payload["negative_mutation_checks"]
        if item["id"]
        == "d_post_post_increment_sign_reversed_exact_fixture"
    )
    lines.extend(
        [
            "",
            "## Finite checks",
            "",
            f"- Full stopped-row recombination passes {recombination['configurations_checked']} exact rational configurations through five shells, including tied stops.",
            f"- The genealogy-cutoff grid passes {omega['pair_comparisons']} pair comparisons and {omega['insertion_comparisons']} insertion comparisons on {omega['radii_checked']} rational radii.",
            f"- The three-channel event-jump identity passes {event['configurations_checked']} stopped configurations and {event['events_checked']} grouped activation epochs.",
            f"- The dissipation-corrected S.137 check passes {corrected['configurations_checked']} exact rational density configurations ({corrected['tied_configurations_checked']} with tied stops), verifying the delta-Omega partition, nonnegative insertion energy, the exact D_post split and bounds, and both E+D-Q one-sided inequalities.",
            f"- The residual Abel decomposition passes all {abel['blocks_checked']} blocks in the first twelve shells.",
            f"- The exact genealogy counts pass {count['configurations_checked']} eight-shell configurations, with tied stops included.",
            f"- The one-block scalar witness passes every N from 1 through {witness['rows'][-1]['N']}; its matched square is computed from the unit positive variations, while its one-block, one-epoch, and zero-merger statistics are derived from the stopped active sets.  No PDE realization is asserted.",
            f"- The super-Gaussian epsilon exponent gap passes {epsilon_gap['comparisons_checked']} exact comparisons for N=2 through {epsilon_gap['rows'][-1]['N']}.",
            "",
            "## Negative mutations",
            "",
            "- Removing the outer k+1 shift is rejected.",
            "- Reversing the weight-drop coefficient sign is rejected.",
            "- Reversing the root completed-clock sign is rejected.",
            "- Replacing the internal max-stop by the min-stop is rejected.",
            f"- Reversing the post-dissipation increments is rejected by a nonempty exact rational cutoff/density fixture: correct D_post is {d_post_mutation['correct_D_post']}, mutated D_post is {d_post_mutation['mutated_D_post']}, and the mutated reconstruction differs from the directly computed W3.  The target inequality is not used as an input.",
            "- Structural sentinels reject the wrong event-jump and residual signs.",
            "- Structural sentinels reject reversal of the D_post upper bound.",
            "- Structural sentinels reject promotion of W_N^sc to PDE work.",
            "- Structural sentinels reject enlargement of the epsilon exponent gap.",
            "",
            "## Boundary",
            "",
            "This certificate checks finite exact algebra, sampled lifted-cutoff",
            "monotonicity, stopped genealogy, statement integrity, and explicit",
            "counterexamples to dangerous mutations.  The periodized cutoff",
            "inequality and local-energy clock positivity are analytic arguments,",
            "not machine proofs.  D_post is checked only on finite rational",
            "density fixtures.  The saturation symbol W_N^sc is scalar, not a",
            "Navier--Stokes velocity, pressure, work, or dissipation measure.",
            "",
            "**FINITE ONLY. ABSTRACT NO-GO ONLY. NOT CLAY.**",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    body = NOTE.read_text(encoding="utf-8")
    exact_checks = [
        exact(
            "weight_drop_coefficient_recombination",
            (Fraction(1) - Fraction(3, 5)) + Fraction(3, 5),
            Fraction(1),
            "d_m plus gamma_m reconstructs gamma_(m-1)",
        ),
        exact(
            "singleton_genealogy_row_count",
            Fraction(1 + 1 + 0),
            Fraction(2),
            "one singleton is both a root and an outer edge",
        ),
        exact(
            "one_block_internal_edge_count",
            Fraction(64 - 1),
            Fraction(63),
            "a 64-shell block has 63 internal boundaries",
        ),
        exact(
            "witness_matched_square_scaling",
            Fraction(64),
            Fraction(8 * 8),
            "Y2 squared equals N at N=64",
        ),
    ]
    finite_checks = [
        stopped_row_recombination_check(),
        omega_insertion_monotonicity_check(),
        event_jump_identity_check(),
        dissipation_corrected_s137_check(),
        block_residual_abel_check(),
        genealogy_count_check(),
        scalar_witness_check(),
        epsilon_exponent_gap_check(),
    ]
    structural = structural_checks(body)
    negative = negative_mutation_checks(body)
    passed = (
        all(item["pass"] for item in exact_checks)
        and all(item["pass"] for item in finite_checks)
        and all(item["pass"] for item in structural)
        and all(item["pass"] for item in negative)
    )
    try:
        note_field = str(NOTE.relative_to(REPO))
    except ValueError:
        note_field = str(NOTE)
    payload = {
        "schema": "r074s-cross-channel-recombination-certificate-v2",
        "scope": (
            "FINITE ONLY: exact rational stopped-row recombination, sampled "
            "genealogy-cutoff monotonicity, event jumps, blockwise residual Abel "
            "algebra, the dissipation-corrected S.137 density fixture, genealogy "
            "counts with ties, scalar saturation, the super-Gaussian epsilon "
            "exponent gap, tags, claim boundaries, and deliberate coefficient/"
            "orientation/dissipation-sign mutations"
        ),
        "note": note_field,
        "note_sha256": sha256(NOTE),
        "exact_checks": exact_checks,
        "finite_checks": finite_checks,
        "structural_checks": structural,
        "negative_mutation_checks": negative,
        "claim_boundary": {
            "four_channel_recombination": "PROVED_FINITE_ALGEBRA",
            "three_channel_genealogy_identity": "PROVED_FINITE_ALGEBRA",
            "d_post_one_sided_decomposition": "PROVED_ANALYTICALLY_AND_CHECKED_ON_FINITE_RATIONAL_DENSITIES",
            "omega_cutoff_nonnegativity": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "quadratic_Q_ledger": "INHERITED_AND_PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "blockwise_residual_abel": "PROVED_FINITE_ALGEBRA",
            "scalar_one_block_no_go": "PROVED_ABSTRACT_NOT_PDE",
            "W_N_sc_is_pde_work": False,
            "epsilon_N_exponent_gap": "PROVED_EXACT_FINITE_EXPONENT_ALGEBRA",
            "pde_weighted_genealogy_theorem": "OPEN",
            "cross_channel_dynamical_sign_theorem": "OPEN",
            "dissipation_dominated_branch": "OPEN",
            "r074r_persistence_hypotheses": "OPEN",
            "fixed_scale_Q1_unconditional": "OPEN",
            "scale_contraction": "OPEN",
            "regularity": "OPEN",
            "singularity_formation": "OPEN",
            "clay_millennium_problem_solved": False,
        },
        "summary": {
            "result": "PASS" if passed else "FAIL",
            "exact_passed": sum(bool(item["pass"]) for item in exact_checks),
            "exact_total": len(exact_checks),
            "finite_passed": sum(bool(item["pass"]) for item in finite_checks),
            "finite_total": len(finite_checks),
            "structural_passed": sum(bool(item["pass"]) for item in structural),
            "structural_total": len(structural),
            "negative_passed": sum(bool(item["pass"]) for item in negative),
            "negative_total": len(negative),
        },
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    REPORT_OUT.write_text(build_report(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
