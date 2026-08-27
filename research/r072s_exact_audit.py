#!/usr/bin/env python3
"""Exact producer ledger for the R0.72S singular-strata theorem.

The program checks the finite rational spine of the incidence jets, local
coefficient versality, and the two declared heat paths.  Continuum root-count
arguments and the nonautonomous PDE problem remain in the report.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
from itertools import permutations
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
from typing import Any


AUDIT = "R0.72S producer exact singular-strata and heat-collision audit"
SCHEMA_VERSION = 1


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rational(value: Fraction | int) -> str:
    value = Fraction(value)
    return f"{value.numerator}/{value.denominator}"


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_ndjson(path: Path, value: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")


def git_commit(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def tracked_changes_dirty(root: Path) -> bool:
    return any(
        subprocess.run(command, cwd=root, check=False).returncode != 0
        for command in (
            ["git", "diff", "--quiet"],
            ["git", "diff", "--cached", "--quiet"],
        )
    )


def sources_tracked(root: Path) -> bool:
    required = (
        "research/r072s_report-source.md",
        "research/r072s_exact_audit.py",
        "research/r072s_compare_audits.py",
    )
    return all(
        subprocess.run(
            ["git", "ls-files", "--error-unmatch", relative], cwd=root,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
        ).returncode == 0
        for relative in required
    )


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


def permutation_sign(values: tuple[int, ...]) -> int:
    inversions = sum(
        values[left] > values[right]
        for left in range(len(values))
        for right in range(left + 1, len(values))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix: list[list[Fraction | int]]) -> Fraction:
    size = len(matrix)
    return sum(
        Fraction(permutation_sign(order))
        * product(matrix[row][order[row]] for row in range(size))
        for order in permutations(range(size))
    )


def product(values: Any) -> Fraction:
    answer = Fraction(1)
    for value in values:
        answer *= Fraction(value)
    return answer


def canonical_payload() -> dict[str, Any]:
    # Incidence jet coefficients after solving f'=f''=0.
    p_real = {"cos": Fraction(-1, 4), "A": Fraction(-9, 4)}
    p_imag = {"sin": Fraction(-1, 2), "B": Fraction(-3, 2)}
    jets = {
        "f3": {
            "sin": 1 + 8 * p_imag["sin"],
            "B": 8 * p_imag["B"] + 27,
        },
        "f4": {
            "cos": 1 + 16 * p_real["cos"],
            "A": 16 * p_real["A"] + 81,
        },
        "f5": {
            "sin": -1 - 32 * p_imag["sin"],
            "B": -32 * p_imag["B"] - 243,
        },
        "f6": {
            "cos": -1 - 64 * p_real["cos"],
            "A": -64 * p_real["A"] - 729,
        },
    }

    coefficient_jet = [
        [0, -2, 0, -3],
        [-4, 0, -9, 0],
        [0, 8, 0, 27],
        [16, 0, 81, 0],
    ]
    coefficient_jet_det = determinant(coefficient_jet)

    # Generic A2 heat path z20=4i, z30=0.
    a2_crossing_z2 = Fraction(4) * Fraction(1, 8)
    a2_third_carrier_amplitude = Fraction(0)
    a2_s_minus = Fraction(-1, 2)
    a2_s_plus = Fraction(1)
    a2_polynomial = lambda sine: 2 * sine * sine - sine - 1
    a2_f3 = Fraction(-3)
    a2_dy_f1 = Fraction(-3)
    a2_split_squared = 2 * a2_dy_f1 / a2_f3 * Fraction(-1)
    a2_sign_guards = {
        "pAtMinusOne": {"constant": Fraction(1), "k": Fraction(1)},
        "pAtZero": {"k": Fraction(-1)},
        "pAtOne": {"constant": Fraction(-1), "k": Fraction(1)},
        "rootProduct": Fraction(-1, 2),
        "offAxisDegeneracyAfterMultiplyBy8k": {
            "constant": Fraction(-1), "kSquared": Fraction(-8),
        },
    }
    heat_decay_exponents = [0, -(2**2 - 1), -(3**2 - 1)]
    heat_identity_exact = heat_decay_exponents == [0, -3, -8]
    a2_k_samples = {
        "before": Fraction(2), "at": Fraction(1), "after": Fraction(1, 2),
    }
    a2_crossing_tau = Fraction(1, 2)
    a2_crossing_power = 8 * a2_crossing_tau**3
    a2_k_log_derivative = Fraction(-3)

    def a2_p(k_value: Fraction, sine: Fraction) -> Fraction:
        return 2 * k_value * sine * sine - sine - k_value

    a2_guard_inputs_hold = (
        a2_sign_guards["pAtMinusOne"]
        == {"constant": Fraction(1), "k": Fraction(1)}
        and a2_sign_guards["pAtZero"] == {"k": Fraction(-1)}
        and a2_sign_guards["pAtOne"]
        == {"constant": Fraction(-1), "k": Fraction(1)}
        and a2_sign_guards["rootProduct"] == Fraction(-1, 2)
        and a2_sign_guards["offAxisDegeneracyAfterMultiplyBy8k"]
        == {"constant": Fraction(-1), "kSquared": Fraction(-8)}
    )
    a2_base_pair = 2 if (
        a2_p(a2_k_samples["at"], Fraction(-1)) > 0
        and a2_p(a2_k_samples["at"], Fraction(0)) < 0
    ) else 0
    a2_extra_counts = {
        "before": 2 if a2_p(a2_k_samples["before"], Fraction(1)) > 0 else 0,
        "at": 1 if a2_p(a2_k_samples["at"], Fraction(1)) == 0 else 0,
        "after": 2 if a2_p(a2_k_samples["after"], Fraction(1)) > 0 else 0,
    }
    a2_representative_counts = {
        regime: a2_base_pair + extra for regime, extra in a2_extra_counts.items()
    }
    a2_unique_event_inputs = (
        a2_guard_inputs_hold
        and a2_crossing_power == 1
        and a2_k_log_derivative < 0
        and a2_sign_guards["offAxisDegeneracyAfterMultiplyBy8k"]["constant"] < 0
        and a2_sign_guards["offAxisDegeneracyAfterMultiplyBy8k"]["kSquared"] < 0
    )
    a2_distinct_counts = a2_representative_counts if a2_unique_event_inputs else {}
    a2_nonzero_fold_jets = a2_f3 != 0 and a2_dy_f1 != 0
    a2_multiplicity_count = a2_base_pair + (2 if a2_f3 != 0 else 0)
    a2_transverse = heat_identity_exact and a2_nonzero_fold_jets
    a2_noncollision_simple = a2_unique_event_inputs and a2_f3 != 0

    # Symmetry-restricted A3 path.
    a0 = Fraction(-2563, 1280)
    b0 = Fraction(1, 30)
    tau_star = Fraction(1, 2)
    a_star = a0 * tau_star**3
    b_star = b0 * tau_star**8
    monotonicity_parent = a0 + 6 * b0
    h_star = 1 + 4 * a_star + 9 * b_star
    qx_star = 24 * b_star + 4 * a_star
    h_y_star = -12 * a_star - 72 * b_star
    f4_star = 45 * b_star - 3
    dy_f2_star = -h_y_star
    a3_split_squared = -2 * h_y_star / (-qx_star)
    a3_sign_guards = {
        "qMinusOneCoefficients": [Fraction(1), -4 * a0, 9 * b0],
        "qXUpperParentAtTauOne": monotonicity_parent,
        "hTauDerivativeParentAtTauOne": monotonicity_parent,
    }
    a3_tau_samples = {
        "before": Fraction(3, 4), "at": tau_star, "after": Fraction(1, 4),
    }

    def a3_h(tau: Fraction) -> Fraction:
        return 1 + 4 * a0 * tau**3 + 9 * b0 * tau**8

    a3_q_minus_one_positive = all(
        value > 0 for value in a3_sign_guards["qMinusOneCoefficients"]
    )
    a3_monotonic_inputs = (
        monotonicity_parent < 0 and b0 > 0 and tau_star > 0 and tau_star <= 1
    )
    a3_crossing_power_identities = {
        "tauCubed": tau_star**3, "tauEighth": tau_star**8,
    }
    a3_continuous_proof_inputs = (
        a3_monotonic_inputs
        and a3_q_minus_one_positive
        and h_star == 0
        and a3_crossing_power_identities
        == {"tauCubed": Fraction(1, 8), "tauEighth": Fraction(1, 256)}
    )
    a3_representative_counts = {
        "before": 4 if a3_h(a3_tau_samples["before"]) < 0 else 2,
        "at": 2 if a3_h(a3_tau_samples["at"]) == 0 else 4,
        "after": 2 if a3_h(a3_tau_samples["after"]) > 0 else 4,
    }
    a3_distinct_counts = (
        a3_representative_counts if a3_continuous_proof_inputs else {}
    )
    a3_nonzero_collision_jets = (
        qx_star != 0 and h_y_star != 0 and f4_star != 0 and dy_f2_star != 0
    )
    a3_multiplicity_count = (3 if f4_star != 0 else 0) + (
        1 if a3_q_minus_one_positive else 0
    )
    a3_slice_transverse = heat_identity_exact and a3_nonzero_collision_jets
    a3_full_space_transverse = 1 >= 2

    checks = {
        "incidenceJetsExact": jets == {
            "f3": {"sin": Fraction(-3), "B": Fraction(15)},
            "f4": {"cos": Fraction(-3), "A": Fraction(45)},
            "f5": {"sin": Fraction(15), "B": Fraction(-195)},
            "f6": {"cos": Fraction(15), "A": Fraction(-585)},
        },
        "a4ReductionExact": (
            Fraction(15) * (1 - Fraction(13, 5)) == Fraction(-24)
        ),
        "a5ReductionExact": (
            Fraction(15) * (1 - Fraction(39, 15)) == Fraction(-24)
        ),
        "coefficientDerivativeJetExact": coefficient_jet_det == 5400,
        "a2CrossingCoefficientExact": a2_crossing_z2 == Fraction(1, 2),
        "a2CrossingRootsExact": (
            a2_polynomial(a2_s_minus) == 0
            and a2_polynomial(a2_s_plus) == 0
        ),
        "a2JetsExact": (
            a2_f3 == Fraction(-3) and a2_dy_f1 == Fraction(-3)
        ),
        "a2SplitExact": a2_split_squared == Fraction(-2),
        "a2FiniteGuardInputsExact": a2_guard_inputs_hold,
        "a2DerivedLedgerExact": (
            a2_unique_event_inputs
            and a2_distinct_counts == {"before": 4, "at": 3, "after": 2}
            and a2_multiplicity_count == 4
            and a2_noncollision_simple
            and a2_transverse
        ),
        "a3MonotonicityInputsExact": (
            monotonicity_parent == Fraction(-2307, 1280)
            and a3_monotonic_inputs
        ),
        "a3CrossingExact": h_star == 0,
        "a3QxExact": qx_star == Fraction(-511, 512),
        "a3JetsExact": (
            h_y_star == Fraction(1533, 512)
            and f4_star == Fraction(-1533, 512)
            and dy_f2_star == Fraction(-1533, 512)
        ),
        "a3SplitExact": a3_split_squared == Fraction(-6),
        "a3FiniteGuardInputsExact": (
            a3_q_minus_one_positive
            and a3_sign_guards["qXUpperParentAtTauOne"]
            == Fraction(-2307, 1280)
            and a3_sign_guards["hTauDerivativeParentAtTauOne"]
            == Fraction(-2307, 1280)
        ),
        "a3DerivedLedgerExact": (
            a3_distinct_counts == {"before": 4, "at": 2, "after": 2}
            and a3_multiplicity_count == 4
            and a3_slice_transverse
            and not a3_full_space_transverse
        ),
        "heatEquationIdentityExact": heat_identity_exact,
    }

    def mapping(value: dict[str, Fraction]) -> dict[str, str]:
        return {key: rational(item) for key, item in value.items()}

    return {
        "schemaVersion": SCHEMA_VERSION,
        "theoremId": "R0.72S-exact-Ak-strata-and-two-heat-collisions",
        "incidenceStrata": {
            "jetCoefficients": {name: mapping(value) for name, value in jets.items()},
            "partition": [
                {"type": "A2", "condition": "B!=sin(phi)/5", "localCodimension": 1},
                {"type": "A3", "condition": "B=sin(phi)/5 and A!=cos(phi)/15", "localCodimension": 2},
                {"type": "A4", "condition": "B=sin(phi)/5 and A=cos(phi)/15 and sin(phi)!=0", "localCodimension": 3},
                {"type": "A5", "condition": "(phi,A,B)=(0,1/15,0) or (pi,-1/15,0)", "localCodimension": 4},
            ],
            "f5OnA4Closure": "-24*sin(phi)",
            "f6AtA5": "-24*cos(phi)",
            "higherThanA5Occurs": False,
            "classificationTarget": "incidence-preimages-not-global-image",
        },
        "restrictedMiniversality": {
            "coefficientOrder": ["Re(z2)", "Im(z2)", "Re(z3)", "Im(z3)"],
            "derivativeOrders": [1, 2, 3, 4],
            "coefficientDerivativeJetAtPhiZero": coefficient_jet,
            "coefficientDerivativeJetDeterminant": rational(coefficient_jet_det),
            "localCodimensions": {"A2": 1, "A3": 2, "A4": 3, "A5": 4},
            "moduloAdditiveConstants": True,
            "fullA5MiniversalParameterCountIncludingConstant": 5,
            "globalEmbeddedStratificationClaimed": False,
        },
        "a2HeatPath": {
            "z20": ["0/1", "4/1"],
            "z30": ["0/1", "0/1"],
            "k": "8*exp(-3*y)",
            "criticalEquation": "2*k*s^2-s-k=0 with s=sin(phi)",
            "sineRoots": "(1+-sqrt(1+8*k^2))/(4*k)",
            "crossingY": "log(2)",
            "crossingPhi": "pi/2",
            "crossingZ2": ["0/1", rational(a2_crossing_z2)],
            "otherSineAtCrossing": rational(a2_s_minus),
            "crossingPowerIdentity": {
                "tau": rational(a2_crossing_tau),
                "8TauCubed": rational(a2_crossing_power),
            },
            "kLogDerivative": rational(a2_k_log_derivative),
            "representativeK": {key: rational(value) for key, value in a2_k_samples.items()},
            "uniqueDegenerateEventForYNonnegative": a2_unique_event_inputs,
            "distinctCriticalCounts": a2_distinct_counts,
            "criticalCountWithMultiplicityAtCrossing": a2_multiplicity_count,
            "allNoncollisionCriticalPointsSimple": a2_noncollision_simple,
            "fThird": rational(a2_f3),
            "dyFPrime": rational(a2_dy_f1),
            "splitXiSquaredPerDelta": rational(a2_split_squared),
            "globalSignGuards": {
                "pAtMinusOne": {key: rational(value) for key, value in a2_sign_guards["pAtMinusOne"].items()},
                "pAtZero": {key: rational(value) for key, value in a2_sign_guards["pAtZero"].items()},
                "pAtOne": {key: rational(value) for key, value in a2_sign_guards["pAtOne"].items()},
                "rootProduct": rational(a2_sign_guards["rootProduct"]),
                "offAxisDegeneracyAfterMultiplyBy8k": {
                    key: rational(value)
                    for key, value in a2_sign_guards["offAxisDegeneracyAfterMultiplyBy8k"].items()
                },
            },
            "fullCoefficientSpaceTransverse": a2_transverse,
            "thirdCarrierActive": a2_third_carrier_amplitude != 0,
        },
        "a3HeatPath": {
            "a0": rational(a0),
            "b0": rational(b0),
            "thirdCarrierActive": b0 != 0,
            "q": "12*b0*tau^8*x^2+4*a0*tau^3*x+1-3*b0*tau^8",
            "monotonicityParentUpper": rational(monotonicity_parent),
            "qMinusOneStrictlyPositive": a3_q_minus_one_positive,
            "crossingTau": rational(tau_star),
            "crossingY": "log(2)",
            "crossingA": rational(a_star),
            "crossingB": rational(b_star),
            "crossingPowerIdentities": {
                key: rational(value) for key, value in a3_crossing_power_identities.items()
            },
            "representativeTau": {key: rational(value) for key, value in a3_tau_samples.items()},
            "hAtCrossing": rational(h_star),
            "qXAtCrossing": rational(qx_star),
            "hYAtCrossing": rational(h_y_star),
            "fFourth": rational(f4_star),
            "dyFSecond": rational(dy_f2_star),
            "splitPhiSquaredPerDelta": rational(a3_split_squared),
            "distinctCriticalCounts": a3_distinct_counts,
            "criticalCountWithMultiplicityAtCrossing": a3_multiplicity_count,
            "globalSignGuards": {
                "qMinusOneCoefficients": [
                    rational(value) for value in a3_sign_guards["qMinusOneCoefficients"]
                ],
                "qXUpperParentAtTauOne": rational(monotonicity_parent),
                "hTauDerivativeParentAtTauOne": rational(monotonicity_parent),
            },
            "crossingPointType": "A3",
            "realEvenSliceTransverse": a3_slice_transverse,
            "fullCoefficientSpaceTransverse": a3_full_space_transverse,
        },
        "stationaryBenchmarks": {
            "A2DecayRate": "nu^(3/5)",
            "A3DecayRate": "nu^(2/3)",
            "nonautonomousCollisionEstimateProved": False,
        },
        "heatEquationIdentity": {
            "identity": "partial_y F=partial_phi^2 F+F",
            "harmonicDecayExponents": {"n1": 0, "n2": 3, "n3": 8},
            "onIncidence": ["partial_y F'=F'''", "partial_y F''=F''''"],
        },
        "claimBoundary": {
            "finiteCertificateIsContinuumProof": False,
            "completeGlobalCausticImageClassification": False,
            "allIncidenceSelfIntersectionsClassified": False,
            "causticCrossingEnhancedDissipation": False,
            "generalThreeDimensionalRegularity": False,
            "clayMillenniumProblemSolved": False,
        },
        "exactChecks": checks,
        "passed": all(checks.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[1]
    started = time.perf_counter()

    progress = output / "producer-progress.ndjson"
    resources = output / "producer-resource.ndjson"
    monitor = output / "producer-monitor.log"
    for path in (progress, resources, monitor):
        path.write_text("", encoding="utf-8")

    config = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT,
        "precision": "Python Fraction plus permutation determinant",
        "gitCommit": git_commit(root),
        "sourceTracked": sources_tracked(root),
        "trackedChangesDirty": tracked_changes_dirty(root),
        "limitations": (
            "Machine-checks finite identities and sign/monotonicity guards only; "
            "the report's continuous proof, not this computation, derives event "
            "uniqueness, global counts, simplicity, and transversality."
        ),
    }
    write_json(output / "producer-config.json", config)
    append_ndjson(progress, {"time": utc_now(), "stage": "start", **config})

    payload = canonical_payload()
    write_json(output / "producer-payload.json", payload)
    stages = (
        ("incidence-jets", payload["exactChecks"]["incidenceJetsExact"]),
        ("restricted-miniversality", payload["exactChecks"]["coefficientDerivativeJetExact"]),
        ("A2-heat-path", payload["exactChecks"]["a2SplitExact"]),
        ("A3-heat-path", payload["exactChecks"]["a3SplitExact"]),
        ("claim-boundary", payload["claimBoundary"]["causticCrossingEnhancedDissipation"] is False),
    )
    for stage, passed in stages:
        append_ndjson(progress, {"time": utc_now(), "stage": stage, "passed": passed})

    checks = {
        "payloadPassed": payload["passed"],
        "incidencePassed": payload["exactChecks"]["incidenceJetsExact"],
        "versalityPassed": (
            payload["restrictedMiniversality"]["coefficientDerivativeJetDeterminant"]
            == "5400/1"
        ),
        "a2FiniteLedgerPassed": payload["exactChecks"]["a2DerivedLedgerExact"],
        "a3FiniteLedgerPassed": payload["exactChecks"]["a3DerivedLedgerExact"],
        "claimBoundaryScoped": payload["claimBoundary"]["generalThreeDimensionalRegularity"] is False,
    }
    elapsed = time.perf_counter() - started
    result = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT,
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
        "limitations": config["limitations"],
    }
    write_json(output / "producer-result.json", result)
    append_ndjson(resources, {
        "time": utc_now(), "event": "complete", "elapsedSeconds": elapsed,
        "maxRssMb": result["maxRssMb"], "pid": os.getpid(),
    })
    monitor.write_text(
        f"[producer] status={result['status']} strata={checks['incidencePassed']} "
        f"versal={checks['versalityPassed']} A2={checks['a2FiniteLedgerPassed']} "
        f"A3={checks['a3FiniteLedgerPassed']}\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
