#!/usr/bin/env python3
"""Compare the R0.5 packet with the R0.6 fixed-injection leakage candidate."""

from __future__ import annotations

import json

import numpy as np

from critical_packet_dynamics import AMPLITUDES, evolve


FIXED_INJECTION_CANDIDATE = np.asarray(
    [
        [0.0, 0.4199676960322196, -2.383859931814685],
        [0.4199676960322196, 0.0, -2.383859931814685],
        [0.0, 0.0, -0.4994285721928156j],
    ],
    dtype=np.complex128,
)


def run_comparison() -> dict[str, object]:
    common = {
        "scale": 10,
        "delta": 0.12,
        "grid": 48,
        "cutoff": 15,
        "viscosity": 1.0,
        "gamma": 1.2,
        "step": 0.00125,
        "final_time": 0.1,
        "checkpoints": [0.00125, 0.0025, 0.005, 0.01, 0.025, 0.05, 0.1],
    }
    original = evolve(amplitudes=AMPLITUDES, **common)
    candidate = evolve(amplitudes=FIXED_INJECTION_CANDIDATE, **common)
    candidate_smaller_step = evolve(
        amplitudes=FIXED_INJECTION_CANDIDATE,
        **{**common, "step": 0.000625},
    )
    candidate_larger_grid = evolve(
        amplitudes=FIXED_INJECTION_CANDIDATE,
        **{**common, "grid": 64},
    )
    candidate_smaller_cutoff = evolve(
        amplitudes=FIXED_INJECTION_CANDIDATE,
        **{**common, "cutoff": 13},
    )
    compared_fields = [
        "hHalfSquared",
        "transfer",
        "outsideHHalfFraction",
        "heatPhaseAlignment",
    ]

    def relative_differences(left: dict[str, float], right: dict[str, float]) -> dict[str, float]:
        return {
            field: abs(left[field] - right[field])
            / max(abs(left[field]), abs(right[field]), 1e-300)
            for field in compared_fields
        }

    return {
        "statement": (
            "same unscaled profile H^(1/2) norm and trilinear transfer; "
            "each run uses 1.2 times its own viscous threshold; finite-dimensional comparison only"
        ),
        "original": original,
        "fixedInjectionCandidate": candidate,
        "convergence": {
            "timeStepHalvingAtTau005": relative_differences(
                candidate["trajectory"][-2],
                candidate_smaller_step["trajectory"][-2],
            ),
            "gridEmbeddingAtTau005": relative_differences(
                candidate["trajectory"][-2],
                candidate_larger_grid["trajectory"][-2],
            ),
            "cutoff13Versus15AtTau005": relative_differences(
                candidate["trajectory"][-2],
                candidate_smaller_cutoff["trajectory"][-2],
            ),
            "smallerStepTau005": candidate_smaller_step["trajectory"][-2],
            "largerGridTau005": candidate_larger_grid["trajectory"][-2],
            "smallerCutoffTau005": candidate_smaller_cutoff["trajectory"][-2],
        },
    }


def validate(audit: dict[str, object]) -> None:
    original = audit["original"]
    candidate = audit["fixedInjectionCandidate"]
    assert candidate["parameters"]["criticalAmplitude"] < original["parameters"]["criticalAmplitude"]
    original_initial = original["trajectory"][0]
    candidate_initial = candidate["trajectory"][0]
    assert abs(original_initial["hHalfSquared"] / candidate_initial["hHalfSquared"] - 1) < 1e-6
    assert abs(original_initial["transfer"] / candidate_initial["transfer"] - 1) < 1e-12
    assert candidate["trajectory"][3]["heatPhaseAlignment"] > original["trajectory"][3]["heatPhaseAlignment"]
    assert candidate["trajectory"][4]["outsideHHalfFraction"] < original["trajectory"][4]["outsideHHalfFraction"]
    assert candidate["trajectory"][-2]["hHalfSquared"] > 1.1 * candidate_initial["hHalfSquared"]
    assert candidate["trajectory"][-2]["transfer"] < 0
    assert candidate["trajectory"][-1]["transfer"] > 0
    for run in (original, candidate):
        for snapshot in run["trajectory"]:
            assert snapshot["divergenceResidual"] < 1e-9
            assert snapshot["realityResidual"] < 1e-9
            assert snapshot["l2SkewResidual"] < 1e-8
    convergence = audit["convergence"]
    assert max(convergence["timeStepHalvingAtTau005"].values()) < 1e-4
    assert max(convergence["gridEmbeddingAtTau005"].values()) < 2e-10
    assert convergence["smallerCutoffTau005"]["hHalfSquared"] > 1.05 * candidate_initial["hHalfSquared"]
    assert convergence["smallerCutoffTau005"]["transfer"] < 0


def main() -> None:
    audit = run_comparison()
    validate(audit)
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
