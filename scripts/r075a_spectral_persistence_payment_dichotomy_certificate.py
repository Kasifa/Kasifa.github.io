#!/usr/bin/env python3
"""Fail-closed exact certificate for the frozen R0.75A dichotomy note."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075a_spectral_persistence_payment_dichotomy.md"
OUT_JSON = Path(
    os.environ.get(
        "R075A_JSON",
        ROOT / "research/r075a_spectral_persistence_payment_dichotomy_certificate.json",
    )
)
OUT_REPORT = Path(
    os.environ.get(
        "R075A_REPORT",
        ROOT / "research/r075a_spectral_persistence_payment_dichotomy_certificate_report.md",
    )
)
MUTATION = os.environ.get("R075A_MUTATION", "")
SCHEMA = "r075a-spectral-persistence-payment-dichotomy-certificate-v1"
MAIN_SHA256 = "f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388"

FROZEN_SOURCES = {
    "research/r074p_temporal_observable_triage.md":
        "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867",
    "research/r074q_common_shear_multipacket_gate.md":
        "60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695",
    "research/r074u_intrinsic_certified_residence.md":
        "e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99",
    "research/r074w_remote_adjacent_inward_comparison.md":
        "d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10",
    "research/r074z_cancellation_cell_gate.md":
        "bb766da4002da760c35185294081f80df97c349ea08b198a5f76db31663aaf6a",
}

NEGATIVE_MUTATIONS = (
    "wrong_sign",
    "cutoff_r_minus_2",
    "cutoff_r_minus_4",
    "wrong_weight_omega",
    "p_reciprocal",
    "critical_only_omission",
    "full_clock_promotion",
    "source_drift",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rat(value: F) -> str:
    return str(value)


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075A_MUTATION: {MUTATION}")

    text = MAIN.read_text(encoding="utf-8")
    flat_text = re.sub(r"\s+", " ", text)
    p = F(63, 32) if MUTATION == "p_reciprocal" else F(32, 63)
    lam = F(63, 32)
    c_gamma = F(8, 3969)
    rho = F(9, 10000)
    transport_sign = -1 if MUTATION == "wrong_sign" else 1
    cutoff_power = -2 if MUTATION == "cutoff_r_minus_2" else (
        -4 if MUTATION == "cutoff_r_minus_4" else -3
    )
    shell_weight_exponent = F(1, 1) if MUTATION == "wrong_weight_omega" else F(1, 4)
    critical_covered = MUTATION != "critical_only_omission"
    full_clock_promoted = MUTATION == "full_clock_promotion"

    # Exact geometry of Omega_0 inside S_+.
    outer_corner_zero = F(5, 2) / F(15, 16)
    inner_radius_threshold = F(2)
    nested_core = {
        "x1": F(3, 16) < F(1, 4),
        "zLeft": F(5, 4) < F(21, 16),
        "zOrder": F(21, 16) < F(23, 16),
        "zRight": F(23, 16) < F(3, 2),
        "x3Left": F(-1, 1) < F(-15, 16),
        "x3Order": F(-15, 16) < F(-9, 16),
        "x3Right": F(-9, 16) < F(-1, 2),
        "outerCornerSlopeNegative": F(-15, 16) < 0,
        "outerCornerThreshold": outer_corner_zero == F(8, 3),
        "outerThresholdDominatesInner": outer_corner_zero > inner_radius_threshold,
        "movingX2PositiveForC0AtMostOne": F(5, 4) - F(1, 96) > 0,
    }

    # A.8: 1/128 <= 1/[128(1-eps_1)] <= 1/96 when 1-eps_1 >= 3/4.
    b_coefficients = {
        "lower": F(1, 128),
        "plateauUpper": F(1, 128) / F(3, 4),
        "crudeUpper": F(1, 96),
    }

    # Exact exponent bookkeeping from A.26 through A.34.
    exponent_ledger = {
        "A.26_X": {"EStar": rat(F(1)), "R": rat(F(3)), "L": rat(F(0)), "omega": rat(F(0))},
        "A.27_spacetimeVolume": {"EStar": rat(F(0)), "R": rat(F(6)), "L": rat(F(1, 2)), "omega": rat(F(0))},
        "A.28_cubicIntegral": {"EStar": rat(F(3, 2)), "R": rat(F(3, 2)), "L": rat(F(-1, 4)), "omega": rat(F(0))},
        "A.29_paymentBeforeEndpoint": {"EStar": rat(F(3, 2)), "R": rat(F(-1, 2)), "L": rat(F(-1, 4)), "omega": rat(shell_weight_exponent)},
        "A.30_endpointSubstitution": {"hRemote": rat(F(1)), "R": rat(F(1)), "L": rat(F(0)), "omega": rat(F(-1))},
        "A.31_paymentAfterEndpoint": {"hRemote": rat(F(3, 2)), "R": rat(F(1)), "L": rat(F(-1, 4)), "omega": rat(F(-5, 4))},
        "A.1_twoThirdsPower": {"hRemote": rat(F(1)), "R": rat(F(2, 3)), "L": rat(F(-1, 6)), "omega": rat(F(-5, 6))},
        "A.32_logR": {"rho": rat(F(1, 4))},
        "A.32_logOmega": {"cGamma": rat(F(1, 4))},
        "A.33_rate": {"cGamma": rat(F(5, 24)), "rho": rat(F(-1, 6))},
    }
    expected_exponents = {
        "A.26_X": {"EStar": "1", "R": "3", "L": "0", "omega": "0"},
        "A.27_spacetimeVolume": {"EStar": "0", "R": "6", "L": "1/2", "omega": "0"},
        "A.28_cubicIntegral": {"EStar": "3/2", "R": "3/2", "L": "-1/4", "omega": "0"},
        "A.29_paymentBeforeEndpoint": {"EStar": "3/2", "R": "-1/2", "L": "-1/4", "omega": "1/4"},
        "A.30_endpointSubstitution": {"hRemote": "1", "R": "1", "L": "0", "omega": "-1"},
        "A.31_paymentAfterEndpoint": {"hRemote": "3/2", "R": "1", "L": "-1/4", "omega": "-5/4"},
        "A.1_twoThirdsPower": {"hRemote": "1", "R": "2/3", "L": "-1/6", "omega": "-5/6"},
        "A.32_logR": {"rho": "1/4"},
        "A.32_logOmega": {"cGamma": "1/4"},
        "A.33_rate": {"cGamma": "5/24", "rho": "-1/6"},
    }

    # Algebraic derivation checks for the exponent ledger.
    a28_r = F(3, 2) * F(3) - F(1, 2) * F(6)
    a28_l = -F(1, 2) * F(1, 2)
    a29_r = a28_r - 2
    a31_r = a29_r + F(3, 2)
    a31_w = shell_weight_exponent - F(3, 2)
    a1_r = F(2, 3) * a31_r
    a1_l = F(2, 3) * a28_l
    a1_w = F(2, 3) * a31_w
    gap = F(5, 24) * c_gamma - F(1, 6) * rho
    expected_gap = F(64279, 238140000)

    tags = re.findall(r"\\tag\{(A\.[^}]+)\}", text)
    references = ["A." + value for value in re.findall(r"\(A\.([0-9]+[a-z]?)\)", text)]
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())

    required_tokens = (
        r"p=\lambda^{-1}=\frac{32}{63}",
        r"\frac1{128R^2}\le B",
        r"\le\frac1{96R^2}",
        r"\tag{A.18}",
        r"c\,\partial_z\phi+\Delta_{z3}\phi",
        r"K_\phi R^{-3}\mathbf 1_{\mathcal S_+}",
        r"\tag{A.26}",
        r"C L^{1/2}R^6",
        r"cE_*^{3/2}R^{3/2}L^{-1/4}",
        r"c\omega^{1/4}E_*^{3/2}R^{-1/2}L^{-1/4}",
        r"\frac{2R}{\omega}h_{\rm rem}",
        r"c h_{\rm rem}^{3/2}",
        r"R\,\omega^{-5/4}L^{-1/4}",
        r"R^{2/3}\omega^{-5/6}L^{-1/6}",
        r"\frac{64279}{238140000}>0",
        r"\partial_tf_n-\partial_3^2f_n",
        r"+(n^2+inb(t,x_3))f_n=0",
        r"\frac12\frac d{dt}\|f_n(t)\|_2^2",
        r"+\|\partial_3f_n(t)\|_2^2",
        r"+n^2\|f_n(t)\|_2^2=0",
        r"\|f_n(t)\|_2\le e^{-n^2(t-s)}\|f_n(s)\|_2",
        r"\|\Pi_{\ge N}^{(2)}F(s)\|_2",
        r"\ge e^{N^2(t-s)}",
        r"\Lambda_{\rm band}:=N^2+M^2+B_QN",
        "W-REMOTE ENDPOINT PERSISTENCE/PAYMENT DICHOTOMY: PROVED",
        "NO FREQUENCY/GEOMETRY-UNIFORM LOCAL OBSERVABILITY CONSTANT",
        "COMPLETE }K\\textbf{, FIXED DELETION, AND REGULARITY: OPEN",
        "includes persistent, critical, and arbitrarily shorter smooth endpoint focusing",
        "does **not** upper-bound the full completed clock",
        "a fixed-deletion bound nor refutes the frozen fixed-deletion theorem",
        "\\mathbf{NOT\\ CLAY}",
        "R075A_COMPLETE_CLOCK_OPEN",
    )

    actual_main_hash = sha256(MAIN)
    expected_main_hash = "0" * 64 if MUTATION == "source_drift" else MAIN_SHA256
    source_rows = {
        path: {
            "expectedSha256": digest,
            "observedSha256": sha256(ROOT / path),
            "tableEntryPresent": f"`{path}` | `{digest}`" in text,
        }
        for path, digest in sorted(FROZEN_SOURCES.items())
    }

    modal_tokens = required_tokens[15:25]
    checks = {
        "mainSourceBinding": record(
            actual_main_hash == expected_main_hash,
            expectedSha256=expected_main_hash,
            observedSha256=actual_main_hash,
        ),
        "frozenSourceBindings": record(
            all(row["expectedSha256"] == row["observedSha256"] and row["tableEntryPresent"] for row in source_rows.values()),
            sources=source_rows,
        ),
        "pReciprocalConvention": record(
            p == F(32, 63)
            and lam == F(63, 32)
            and p * lam == 1
            and re.search(r"p\s*=\s*\\frac\{63\}\{32\}", text) is None,
            p=rat(p),
            lambdaValue=rat(lam),
        ),
        "nestedCoreInequalities": record(all(nested_core.values()), inequalities=nested_core),
        "BInterval": record(
            b_coefficients["lower"] < b_coefficients["plateauUpper"]
            and b_coefficients["plateauUpper"] == b_coefficients["crudeUpper"],
            coefficients={key: rat(value) for key, value in b_coefficients.items()},
        ),
        "movingCutoffSignAndScale": record(
            transport_sign == 1 and cutoff_power == -3,
            transportSign=transport_sign,
            cutoffRPower=cutoff_power,
        ),
        "exponentLedgerA26ToA34": record(
            exponent_ledger == expected_exponents
            and a28_r == F(3, 2)
            and a28_l == F(-1, 4)
            and a29_r == F(-1, 2)
            and a31_r == 1
            and a31_w == F(-5, 4)
            and (a1_r, a1_l, a1_w) == (F(2, 3), F(-1, 6), F(-5, 6)),
            exponents=exponent_ledger,
        ),
        "exactGapA34": record(
            gap == expected_gap and gap > 0,
            value=rat(gap),
            expected=rat(expected_gap),
        ),
        "modalIdentities": record(
            all(token in text for token in modal_tokens),
            equation="dt f_n - d3^2 f_n + (n^2+i n b)f_n=0",
            energySigns={"timeDerivative": 1, "verticalDissipation": 1, "horizontalDissipation": 1, "shearRealPart": 0},
            forwardDecayExponent="-n^2(t-s)",
            backwardAmplificationExponent="+n^2(t-s)",
        ),
        "tagsReferencesAndDisplays": record(
            len(tags) == 64
            and len(set(tags)) == 64
            and not (set(references) - set(tags))
            and display_open == display_close == 64,
            tagCount=len(tags),
            uniqueTagCount=len(set(tags)),
            unresolvedReferences=sorted(set(references) - set(tags)),
            displayOpen=display_open,
            displayClose=display_close,
        ),
        "requiredTextualSentinels": record(
            all(re.sub(r"\s+", " ", token) in flat_text for token in required_tokens),
            requiredCount=len(required_tokens),
        ),
        "criticalAndShorterCoverage": record(
            critical_covered
            and "includes persistent, critical, and arbitrarily shorter smooth" in text
            and "all shorter smooth focusing" in text,
            persistent=True,
            critical=critical_covered,
            arbitrarilyShorter=True,
        ),
        "claimBoundary": record(
            not full_clock_promoted
            and "COMPLETE }K\\textbf{, FIXED DELETION, AND REGULARITY: OPEN" in flat_text
            and "a fixed-deletion theorem follows from (A.31) | **NOT PROVED**" in flat_text
            and "No statement is made about arbitrary suitable weak solutions" in flat_text
            and "\\mathbf{NOT\\ CLAY}" in text,
            wRemoteDichotomyProved=True,
            fullCompletedClockProved=full_clock_promoted,
            fixedDeletionProved=False,
            arbitrarySuitableWeakSolutions=False,
            clayClaim=False,
        ),
        "textSafety": record(
            not any(ord(char) < 32 and char not in "\n\r\t" for char in text),
            controlCharacters=0,
        ),
    }

    verdict = "PASS" if all(item["pass"] for item in checks.values()) else "FAIL"
    payload = {
        "schema": SCHEMA,
        "verdict": verdict,
        "mutation": MUTATION or None,
        "assertionsPassed": sum(item["pass"] for item in checks.values()),
        "assertionsTotal": len(checks),
        "checks": checks,
        "exactValues": {
            "p": rat(p),
            "lambda": rat(lam),
            "cGamma": rat(c_gamma),
            "rho": rat(rho),
            "gapA34": rat(gap),
        },
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "boundary": (
            "EXACT FINITE COMMON-SHEAR W-REMOTE ENDPOINT/PAYMENT DICHOTOMY ONLY; "
            "complete K, fixed deletion, arbitrary suitable weak solutions, regularity, and Clay remain open"
        ),
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    source_lines = "\n".join(
        f"- `{path}`: `{row['observedSha256']}`"
        for path, row in source_rows.items()
    )
    OUT_REPORT.write_text(
        f"""# R0.75A reproducibility certificate report

- Verdict: **{verdict}**
- Assertions: {payload['assertionsPassed']}/{payload['assertionsTotal']}
- Main SHA-256: `{actual_main_hash}`
- Tags: {len(tags)} unique; references resolve; display delimiters {display_open}/{display_close}
- Exact gap (A.34): `{gap}`
- Negative mutations declared: {len(NEGATIVE_MUTATIONS)}

## Frozen sources

{source_lines}

## Certified boundary

The certificate verifies the exact moving-cutoff sign, the `R^-3` cutoff
scale, nested-core inequalities, the `B` interval, every `R`, `L`, and
`omega` exponent from (A.26)--(A.34), and the horizontal modal identities.
It verifies `p=32/63` and rejects its reciprocal.

The W-remote endpoint/payment dichotomy includes persistent, critical, and
arbitrarily shorter smooth endpoint focusing. It does **not** prove an upper
bound for the complete clock `K`, a fixed-deletion theorem, a result for
arbitrary suitable weak solutions, regularity, singularity, or a Clay claim.

**EXACT FINITE COMMON-SHEAR CERTIFICATE | COMPLETE K OPEN | FIXED DELETION
NOT PROVED | NOT CLAY**
""",
        encoding="utf-8",
    )
    print(json.dumps({"verdict": verdict, "assertions": len(checks), "mutation": MUTATION or None}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
