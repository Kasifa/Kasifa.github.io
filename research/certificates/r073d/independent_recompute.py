#!/usr/bin/env python3
"""Independent stdlib-only recomputation of R0.73D exact sentinels."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/certificates/r073d/independent_recompute.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    proof = (ROOT / "research/r073d_viscous_persistence_proof.md").read_text()
    gaps = (ROOT / "research/r073d_gap_matrix.md").read_text()
    finite = json.loads((ROOT / "experiments/r073d/viscous_cluster_diagnostic.json").read_text())
    independent = json.loads((ROOT / "experiments/r073d/independent_validation.json").read_text())

    commutator_sum = (
        2 * Fraction(1, 1) * Fraction(1, 4)
        + 2 * Fraction(2, 1) * Fraction(1, 8)
    )
    l_inverse_half_norm = Fraction(2, 1)
    wxx_bound = Fraction(3, 2)
    gamma = Fraction(1, 2)
    rough_k_bound = gamma * (
        l_inverse_half_norm * commutator_sum
        + l_inverse_half_norm * l_inverse_half_norm * wxx_bound
    )
    checks = {
        "commutatorFourierL1SumEqualsOne": commutator_sum == 1,
        "roughCompactTermBoundEqualsFour": rough_k_bound == 4,
        "domainJumpRecorded": "D(H_0)=L^2" in proof and "\\varepsilon>0" in proof,
        "projectionNormLimitRecorded": "P_\\varepsilon-P_0" in proof,
        "fixedClusterStatusesClosed": all(
            token in gaps
            for token in (
                "staticVanishingViscosityPersistence=CLOSED",
                "fixedClusterRieszProjectionNormConvergence=CLOSED",
                "fixedClusterAlgebraicMultiplicityPreservation=CLOSED",
            )
        ),
        "finitePrimaryPass": all(finite["checks"].values()),
        "finiteIndependentPass": independent["allChecksPass"] is True,
        "finiteClaimBoundary": finite["claimBoundary"]["infiniteDimensionalPersistenceProvedHere"] is False,
        "fastTimeOpen": "logFastTimeTransfer=OPEN" in gaps,
        "clayOpen": "Clay=OPEN" in gaps,
    }
    output = {
        "schemaVersion": "r073d-independent-analytic-recompute-v1",
        "release": "R0.73D",
        "sourceCommit": commit,
        "implementation": {
            "stdlibOnly": True,
            "importsPrimaryCertificateGenerator": False,
            "scriptSha256": sha256(Path(__file__).resolve()),
        },
        "exactSentinels": {
            "commutatorFourierL1Sum": [commutator_sum.numerator, commutator_sum.denominator],
            "roughCompactTermBound": [rough_k_bound.numerator, rough_k_bound.denominator],
        },
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "claimBoundary": {
            "recomputesAnalyticSentinelsOnly": True,
            "doesNotProveSimplicity": True,
            "doesNotProveFastTimeTransfer": True,
            "doesNotProveNonlinearNavierStokes": True,
        },
    }
    OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"event": "independent-recompute", "allChecksPass": output["allChecksPass"]}, sort_keys=True))
    return 0 if output["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
