#!/usr/bin/env python3
"""High-precision producer audit for the R0.72D root-ledger family.

The accompanying report contains the proof.  This program reconstructs the
finite Rudin--Shapiro algebra, the shifted carrier moments, the row-aligned
launch identity, the Abel heat envelope, and the dimensionless launch-root
and rotational-charge scalings.  ``mpmath`` is used without directed
rounding, so the JSON output corroborates the proof but is not an interval
certificate or a Navier--Stokes regularity proof.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import resource
import sys
import time

import mpmath as mp


MP_DIGITS = 90
mp.mp.dps = MP_DIGITS

K_Z = mp.mpf("1.25")
KAPPA = mp.mpf("0.4")
GAMMA = mp.mpf("0.3")
AMPLITUDE = mp.mpf("1")
Q_SCALE = mp.mpf("1")
ODD_GENERATIONS = tuple(range(3, 16, 2))
ALL_GENERATIONS = tuple(range(0, 16))
ABEL_GENERATIONS = (3, 5, 7, 9, 11)
ABEL_TIMES = (mp.mpf("0"), mp.mpf("0.2"), mp.mpf("1"), mp.mpf("4"))
ABEL_ANGLES = tuple(2 * mp.pi * j / 17 for j in range(17))
RS_PREFIX_CONSTANT = 2 + mp.sqrt(2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--resource-log", type=Path)
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit(message: str) -> None:
    print(f"[{utc_now()}] {message}", file=sys.stderr, flush=True)


def append_json(path: Path | None, payload: dict[str, object]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True) + "\n")


def progress(path: Path | None, stage: str, **fields: object) -> None:
    append_json(path, {"timestampUtc": utc_now(), "stage": stage, **fields})


def resource_snapshot(
    path: Path | None, stage: str, started: float, **fields: object
) -> None:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_json(
        path,
        {
            "timestampUtc": utc_now(),
            "stage": stage,
            "elapsedSeconds": time.perf_counter() - started,
            "userCpuSeconds": usage.ru_utime,
            "systemCpuSeconds": usage.ru_stime,
            "maximumResidentSetRaw": usage.ru_maxrss,
            "logicalCpuCount": os.cpu_count(),
            **fields,
        },
    )


def mtext(value: mp.mpf | mp.mpc, digits: int = 45) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


def check(
    name: str, passed: bool, value: object, requirement: str
) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def rudin_shapiro_pair(generation: int) -> tuple[list[int], list[int]]:
    p = [1]
    q = [1]
    for _ in range(generation):
        p, q = p + q, p + [-value for value in q]
    return p, q


def binary_eleven_sign(index: int) -> int:
    return -1 if (index & (index >> 1)).bit_count() % 2 else 1


def carrier_moment(m_value: int) -> int:
    return sum(index * index for index in range(m_value, 2 * m_value))


def carrier_moment_closed(m_value: int) -> int:
    return m_value * (2 * m_value - 1) * (7 * m_value - 1) // 6


def regression_power(m_values: list[mp.mpf], values: list[mp.mpf]) -> mp.mpf:
    xs = [mp.log(value) for value in m_values]
    ys = [mp.log(value) for value in values]
    x_mean = mp.fsum(xs) / len(xs)
    y_mean = mp.fsum(ys) / len(ys)
    return mp.fsum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(xs, ys, strict=True)
    ) / mp.fsum((x_value - x_mean) ** 2 for x_value in xs)


def recursion_ledger() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for generation in ALL_GENERATIONS:
        p, q = rudin_shapiro_pair(generation)
        m_value = 1 << generation
        binary = [binary_eleven_sign(index) for index in range(m_value)]
        rows.append(
            {
                "generation": generation,
                "M": m_value,
                "allCoefficientsAreSigns": all(abs(value) == 1 for value in p + q),
                "binaryElevenMatch": p == binary,
                "PAtOne": sum(p),
                "QAtOne": sum(q),
                "oddEndpointSquareResidual": (
                    sum(p) ** 2 - 2 * m_value if generation % 2 else None
                ),
            }
        )
    return {
        "recursion": {
            "Pnext": "P_n+z^(2^n)Q_n",
            "Qnext": "P_n-z^(2^n)Q_n",
            "binaryRule": "epsilon_j=(-1)^(overlapping binary 11 pairs)",
        },
        "rows": rows,
    }


def abel_sample_ledger() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    maximum_identity_residual = mp.mpf("0")
    maximum_weighted_over_bound = mp.mpf("0")
    maximum_prefix_over_bound = mp.mpf("0")

    for generation in ABEL_GENERATIONS:
        signs, _ = rudin_shapiro_pair(generation)
        m_value = 1 << generation
        m = mp.mpf(m_value)
        for scaled_time in ABEL_TIMES:
            time_value = scaled_time / (KAPPA * m**2)
            weights = [
                mp.exp(-KAPPA * (m_value + index) ** 2 * time_value)
                for index in range(m_value)
            ]
            for theta in ABEL_ANGLES:
                z_value = mp.e ** (mp.j * theta)
                partials: list[mp.mpc] = []
                running = mp.mpc("0")
                for index, sign in enumerate(signs):
                    running += sign * z_value**index
                    partials.append(running)
                direct = mp.fsum(
                    signs[index] * weights[index] * z_value**index
                    for index in range(m_value)
                )
                abel = weights[-1] * partials[-1] + mp.fsum(
                    (weights[index] - weights[index + 1]) * partials[index]
                    for index in range(m_value - 1)
                )
                prefix_max = max(abs(value) for value in partials)
                prefix_bound = RS_PREFIX_CONSTANT * mp.sqrt(m)
                weighted_bound = prefix_bound * weights[0]
                identity_residual = abs(direct - abel)
                maximum_identity_residual = max(
                    maximum_identity_residual, identity_residual
                )
                maximum_weighted_over_bound = max(
                    maximum_weighted_over_bound,
                    abs(direct) / weighted_bound,
                )
                maximum_prefix_over_bound = max(
                    maximum_prefix_over_bound, prefix_max / prefix_bound
                )
            rows.append(
                {
                    "generation": generation,
                    "M": m_value,
                    "scaledTime": mtext(scaled_time),
                    "firstWeight": mtext(weights[0]),
                }
            )

    l1_scaled = (
        2 * abs(K_Z) * RS_PREFIX_CONSTANT * AMPLITUDE / KAPPA
    )
    l2_square_scaled = (
        2 * K_Z**2 * RS_PREFIX_CONSTANT**2 * AMPLITUDE**2 / KAPPA
    )
    return {
        "prefixTheorem": {
            "constant": mtext(RS_PREFIX_CONSTANT),
            "statement": "sup_theta max_(k<M)|sum_(j<=k) epsilon_j exp(i*j*theta)| <= (2+sqrt(2))*sqrt(M)",
            "proofMechanism": "recursive dyadic block decomposition and the P/Q parallelogram bound",
        },
        "weightedAbelIdentity": (
            "sum epsilon_j*w_j*z^j = w_(M-1)S_(M-1) + "
            "sum_(j<M-1)(w_j-w_(j+1))S_j"
        ),
        "heatEnvelope": (
            "||V(t)|| <= 2|Kz|a(2+sqrt(2))*sqrt(M)*exp(-kappa*M^2*t)"
        ),
        "l1IntegralBound": (
            "int_0^infty ||V(t)||dt <= "
            "[2|Kz|a(2+sqrt(2))/kappa]*M^(-3/2)"
        ),
        "l2SquareIntegralBound": (
            "int_0^infty ||V(t)||^2dt <= "
            "[2Kz^2*a^2*(2+sqrt(2))^2/kappa]*M^(-1)"
        ),
        "scaledL1BoundConstant": mtext(l1_scaled),
        "scaledL2SquareBoundConstant": mtext(l2_square_scaled),
        "maximumSampledAbelIdentityResidual": mtext(maximum_identity_residual),
        "maximumSampledWeightedOverAnalyticBound": mtext(
            maximum_weighted_over_bound
        ),
        "maximumSampledPrefixOverAnalyticBound": mtext(
            maximum_prefix_over_bound
        ),
        "sampleRows": rows,
    }


def family_ledger() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    m_values: list[mp.mpf] = []
    phis: list[mp.mpf] = []
    etas: list[mp.mpf] = []
    h0_squares: list[mp.mpf] = []
    atom_ratios: list[mp.mpf] = []
    charge_uppers: list[mp.mpf] = []

    for generation in ODD_GENERATIONS:
        signs, q_signs = rudin_shapiro_pair(generation)
        m_value = 1 << generation
        m = mp.mpf(m_value)
        k_s_integer = carrier_moment(m_value)
        k_s = mp.mpf(k_s_integer)
        k_v = AMPLITUDE**2 * k_s

        omega = 2 * abs(K_Z) * AMPLITUDE * mp.sqrt(2 * m)
        omega_square = omega**2
        rho_square = 2 * K_Z**2 * AMPLITUDE**2 * m
        chi = rho_square / omega_square
        phi = (m / k_s) * chi * (omega_square / k_v) ** (mp.mpf(1) / 3)

        delta = GAMMA * m ** (mp.mpf(3) / 2) / AMPLITUDE
        eta = delta * omega
        h0 = mp.sqrt(2) * abs(K_Z) * AMPLITUDE * m
        h0_square = h0**2

        p_amplitude = delta * Q_SCALE**2
        s_square = 3 * p_amplitude**2 * AMPLITUDE**2
        energy = s_square * k_s + p_amplitude**2 * k_v
        atom = (
            s_square
            * p_amplitude**2
            * h0_square
            / (Q_SCALE**2 * energy)
        )
        dissipation_one_third = (Q_SCALE**2 * energy) ** (mp.mpf(1) / 3)
        atom_over_d13 = atom / dissipation_one_third
        charge_upper = (
            p_amplitude**2
            * s_square
            * AMPLITUDE**2
            / (Q_SCALE**4 * energy)
        )

        explicit_row_sum = mp.fsum(
            -mp.j
            * K_Z
            * AMPLITUDE
            * signs[index]
            * (
                mp.j
                * mp.sign(K_Z)
                * signs[index]
                / mp.sqrt(2)
                + mp.j
                * mp.sign(K_Z)
                * signs[index]
                / mp.sqrt(2)
            )
            for index in range(m_value)
        )

        rows.append(
            {
                "generation": generation,
                "M": m_value,
                "carrierRange": [m_value, 2 * m_value - 1],
                "Ks": k_s_integer,
                "KsClosed": carrier_moment_closed(m_value),
                "KsOverM3": mtext(k_s / m**3),
                "Kv": mtext(k_v),
                "PAtOne": sum(signs),
                "QAtOne": sum(q_signs),
                "Omega0": mtext(omega),
                "Omega0Squared": mtext(omega_square),
                "rho0Squared": mtext(rho_square),
                "chi0": mtext(chi),
                "Phi": mtext(phi),
                "MToEightThirdsTimesPhi": mtext(m ** (mp.mpf(8) / 3) * phi),
                "delta": mtext(delta),
                "deltaTimesA": mtext(delta * AMPLITUDE),
                "eta": mtext(eta),
                "etaOverGammaM2": mtext(eta / (GAMMA * m**2)),
                "launchVectorNormSquared": m_value,
                "activeMomentKf": k_s_integer,
                "h0": mtext(h0),
                "h0Squared": mtext(h0_square),
                "rowAlignmentResidual": mtext(abs(explicit_row_sum - h0)),
                "S2KfOverP2Kv": mtext(s_square * k_s / (p_amplitude**2 * k_v)),
                "E": mtext(energy),
                "launchAtomOverDOneThirdModel": mtext(atom_over_d13),
                "atomOverGammaFourThirds": mtext(atom_over_d13 / GAMMA ** (mp.mpf(4) / 3)),
                "fullChargeUpperModel": mtext(charge_upper),
                "chargeOverGammaSquared": mtext(charge_upper / GAMMA**2),
                "tau": mtext(m ** (-3)),
                "predictedZetaScale": "O(M^-1/2)",
            }
        )
        m_values.append(m)
        phis.append(phi)
        etas.append(eta)
        h0_squares.append(h0_square)
        atom_ratios.append(atom_over_d13)
        charge_uppers.append(charge_upper)

    atom_limit = (
        mp.mpf(3)
        / 2
        * K_Z**2
        / (mp.root(4, 3) * (mp.mpf(7) / 3) ** (mp.mpf(4) / 3))
    )
    return {
        "definition": {
            "M": "2^n, odd n for the exact endpoint identity",
            "carriers": "r_j=M+j, 0<=j<M",
            "coefficients": "w_j=a*epsilon_j",
            "launchVector": "G_(+/-r_j)=i*sgn(Kz)*epsilon_j/sqrt(2)",
            "coupling": "delta*a=gamma*M^(3/2)",
            "amplitudeBalance": "S^2*Kf=3*P^2*Kv with P=q^2*delta",
        },
        "exactFormulas": {
            "Ks": "M(2M-1)(7M-1)/6",
            "Kv": "a^2*Ks",
            "rho0Squared": "2*Kz^2*a^2*M",
            "Omega0Squared": "8*Kz^2*a^2*M (odd generations)",
            "Phi": "(M/Ks)*(rho0^2/Omega0^2)*(Omega0^2/Kv)^(1/3)",
            "h0Squared": "2*Kz^2*a^2*M^2",
            "eta": "2*sqrt(2)*|Kz|*gamma*M^2",
            "chargeUpper": "(3/4)*(delta*a)^2/Ks",
        },
        "fittedPowers": {
            "Phi": mtext(regression_power(m_values[-5:], phis[-5:])),
            "eta": mtext(regression_power(m_values[-5:], etas[-5:])),
            "h0Squared": mtext(
                regression_power(m_values[-5:], h0_squares[-5:])
            ),
            "launchAtomOverDOneThird": mtext(
                regression_power(m_values[-5:], atom_ratios[-5:])
            ),
            "fullChargeUpper": mtext(
                regression_power(m_values[-5:], charge_uppers[-5:])
            ),
        },
        "asymptoticConstants": {
            "KsOverM3": mtext(mp.mpf(7) / 3),
            "etaOverGammaM2": mtext(2 * mp.sqrt(2) * abs(K_Z)),
            "launchAtomOverDOneThirdPerGammaFourThirds": mtext(atom_limit),
            "fullChargeUpperPerGammaSquared": mtext(mp.mpf(9) / 28),
        },
        "rows": rows,
    }


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    emit("R0.72D producer audit started")
    progress(args.progress_log, "producer-start", mpDigits=MP_DIGITS)
    resource_snapshot(args.resource_log, "producer-start", started)

    recursion = recursion_ledger()
    emit("Rudin--Shapiro recursion and binary parity path complete")
    progress(args.progress_log, "recursion-complete")

    abel = abel_sample_ledger()
    emit("weighted Abel identities and heat envelopes complete")
    progress(args.progress_log, "abel-envelope-complete")
    resource_snapshot(args.resource_log, "abel-envelope-complete", started)

    family = family_ledger()
    emit("shifted-carrier launch and normalized ledgers complete")
    progress(args.progress_log, "family-ledger-complete")

    recursion_rows = recursion["rows"]
    family_rows = family["rows"]
    powers = family["fittedPowers"]
    limits = family["asymptoticConstants"]
    terminal = family_rows[-1]

    checks = [
        check(
            "Rudin--Shapiro recursion agrees with binary-eleven parity",
            all(
                bool(row["allCoefficientsAreSigns"])
                and bool(row["binaryElevenMatch"])
                for row in recursion_rows
            ),
            {"generations": len(recursion_rows), "terminalM": recursion_rows[-1]["M"]},
            "recursive P coefficients equal (-1)^(overlapping binary 11 pairs)",
        ),
        check(
            "odd generations have the exact endpoint",
            all(
                row["oddEndpointSquareResidual"] == 0 and row["QAtOne"] == 0
                for row in recursion_rows
                if row["generation"] % 2 == 1
            ),
            {"oddGenerations": list(ODD_GENERATIONS)},
            "P_n(1)^2=2M and Q_n(1)=0 for odd n",
        ),
        check(
            "shifted carrier moment identity is exact",
            all(row["Ks"] == row["KsClosed"] for row in family_rows),
            terminal["Ks"],
            "sum_(r=M)^(2M-1) r^2=M(2M-1)(7M-1)/6",
        ),
        check(
            "row-aligned launch identity is exact to working precision",
            all(mp.mpf(row["rowAlignmentResidual"]) < mp.mpf("1e-78") for row in family_rows)
            and all(mp.mpf(row["S2KfOverP2Kv"]) == 3 for row in family_rows),
            {
                "terminalResidual": terminal["rowAlignmentResidual"],
                "h0Squared": terminal["h0Squared"],
                "launchNormSquared": terminal["launchVectorNormSquared"],
            },
            "||G||^2=M, Kf=Ks, h0^2=2Kz^2a^2M^2, and S^2Kf=3P^2Kv",
        ),
        check(
            "sampled weighted Abel identity closes",
            mp.mpf(abel["maximumSampledAbelIdentityResidual"]) < mp.mpf("1e-75")
            and mp.mpf(abel["maximumSampledWeightedOverAnalyticBound"]) <= 1,
            {
                "identityResidual": abel["maximumSampledAbelIdentityResidual"],
                "weightedOverBound": abel["maximumSampledWeightedOverAnalyticBound"],
            },
            "Abel summation and the dyadic prefix theorem imply the displayed heat envelope",
        ),
        check(
            "heat envelope has the M^-3/2 L1 scale",
            mp.mpf(abel["scaledL1BoundConstant"]) > 0,
            abel["scaledL1BoundConstant"],
            "M^(3/2)*int ||V(t)||dt/a is bounded independently of M",
        ),
        check(
            "heat envelope has the M^-1 L2-square scale",
            mp.mpf(abel["scaledL2SquareBoundConstant"]) > 0,
            abel["scaledL2SquareBoundConstant"],
            "M*int ||V(t)||^2dt/a^2 is bounded independently of M",
        ),
        check(
            "phase prefactor keeps the sharp M^-8/3 power",
            abs(mp.mpf(powers["Phi"]) + mp.mpf(8) / 3) < mp.mpf("0.002"),
            {"fittedPower": powers["Phi"], "terminalScaledPhi": terminal["MToEightThirdsTimesPhi"]},
            "Phi=(M/Ks)*chi*(Omega0^2/Kv)^(1/3)=Theta(M^-8/3)",
        ),
        check(
            "strong coupling has eta proportional to M^2",
            abs(mp.mpf(powers["eta"]) - 2) < mp.mpf("1e-75")
            and abs(mp.mpf(terminal["etaOverGammaM2"]) - mp.mpf(limits["etaOverGammaM2"])) < mp.mpf("1e-75"),
            {"fittedPower": powers["eta"], "scaledEta": terminal["etaOverGammaM2"]},
            "delta*a=gamma*M^(3/2) and Omega0=Theta(a*sqrt(M)) give eta=Theta(gamma*M^2)",
        ),
        check(
            "launch-root atom over D^(1/3) stays at constant scale",
            abs(mp.mpf(powers["launchAtomOverDOneThird"])) < mp.mpf("0.002")
            and abs(
                mp.mpf(terminal["atomOverGammaFourThirds"])
                - mp.mpf(limits["launchAtomOverDOneThirdPerGammaFourThirds"])
            ) < mp.mpf("0.001"),
            {
                "fittedPower": powers["launchAtomOverDOneThird"],
                "terminalScaledValue": terminal["atomOverGammaFourThirds"],
                "limit": limits["launchAtomOverDOneThirdPerGammaFourThirds"],
            },
            "the row-aligned launch atom divided by the model D^(1/3) tends to a positive multiple of gamma^(4/3)",
        ),
        check(
            "full rotational-charge comparison stays bounded",
            abs(mp.mpf(powers["fullChargeUpper"])) < mp.mpf("0.001")
            and abs(
                mp.mpf(terminal["chargeOverGammaSquared"])
                - mp.mpf(limits["fullChargeUpperPerGammaSquared"])
            ) < mp.mpf("0.001"),
            {
                "fittedPower": powers["fullChargeUpper"],
                "terminalScaledValue": terminal["chargeOverGammaSquared"],
                "limit": limits["fullChargeUpperPerGammaSquared"],
            },
            "(3/4)*(delta*a)^2/Ks tends to (9/28)*gamma^2",
        ),
    ]
    all_passed = all(bool(row["passed"]) for row in checks)

    payload = {
        "schemaVersion": "r072d-dynamical-ledger-producer-v1",
        "release": "R0.72D",
        "generatedAtUtc": utc_now(),
        "allPassed": all_passed,
        "checkCount": len(checks),
        "passedCheckCount": sum(bool(row["passed"]) for row in checks),
        "arithmetic": {
            "engine": "mpmath arbitrary precision",
            "decimalDigits": MP_DIGITS,
            "intervalArithmetic": False,
            "role": "finite exact-integer identities and high-precision scaling diagnostics",
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "mpmath": mp.__version__,
        },
        "parameters": {
            "Kz": mtext(K_Z),
            "kappa": mtext(KAPPA),
            "gamma": mtext(GAMMA),
            "a": mtext(AMPLITUDE),
            "q": mtext(Q_SCALE),
            "oddGenerations": list(ODD_GENERATIONS),
            "abelGenerations": list(ABEL_GENERATIONS),
            "randomness": False,
        },
        "rudinShapiro": recursion,
        "abelHeatEnvelope": abel,
        "normalizedFamily": family,
        "checks": checks,
        "scope": {
            "analyticProofInJson": False,
            "intervalArithmetic": False,
            "finiteMatrixDNS": False,
            "corroboratesInteriorRootConstruction": False,
            "corroboratesNormalizedScaling": True,
            "provesNSERegularity": False,
            "note": (
                "The report proves the Abel envelope and perturbative interior-root construction. "
                "This producer checks their finite algebra and asymptotic bookkeeping only."
            ),
        },
        "elapsedSeconds": time.perf_counter() - started,
    }

    if not all_passed:
        failed = [row["name"] for row in checks if not row["passed"]]
        raise AssertionError(f"producer checks failed: {failed}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    progress(
        args.progress_log,
        "producer-complete",
        allPassed=all_passed,
        checkCount=len(checks),
        elapsedSeconds=payload["elapsedSeconds"],
    )
    resource_snapshot(
        args.resource_log,
        "producer-complete",
        started,
        allPassed=all_passed,
        checkCount=len(checks),
    )
    emit(f"R0.72D producer audit passed in {payload['elapsedSeconds']:.2f}s")


if __name__ == "__main__":
    main()
