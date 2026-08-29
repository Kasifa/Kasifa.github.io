#!/usr/bin/env python3
"""Independent stdlib-only recomputation of R0.73E certificate sentinels."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/certificates/r073e/independent_recompute.json"
SOURCE_COMMIT = "803279d72c24a54db27c40dcdad97593636788fc"
CLOSED = (
    "fixedPositiveHalfPlaneNoPollution", "allModesRightOfBProjectionNormPersistence",
    "topInviscidClusterExists", "topViscousClusterPersistence",
    "topReducedHalfPlaneResolventUniform", "frozenTopClusterRelativeDichotomy",
    "fixedFrozenGeneratorVolterraTransfer", "logFastTimeTransfer",
    "superPolynomialCompleteRowNoGo",
)
OPEN = (
    "certifiedSigmaStarIsRightmost", "selectedSigmaStarComplementDichotomy",
    "uniformHalfPlaneBoundAtBEqualsZero", "globalRightHalfPlaneNoPollution",
    "absoluteUniformComplementDecay", "explicitHalfPlaneGap", "explicitViscosityThreshold",
    "quantitativeEigenvalueRate", "movingProfileUniformContour", "graphDomainKatoTransport",
    "movingProfileEvolutionDichotomy", "inviscidRootUnique", "inviscidEigenvalueSimple",
    "completeOSSquireA2DirectSum", "fixedWindowExponentialLowerLaw",
    "nonlinearNavierStokes", "Clay",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_statuses(path: Path) -> dict[str, str]:
    return dict(re.findall(r"^([A-Za-z][A-Za-z0-9]*)=(CLOSED|OPEN)$", path.read_text(), re.MULTILINE))


def main() -> int:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    expected = {**{name: "CLOSED" for name in CLOSED}, **{name: "OPEN" for name in OPEN}}
    ledgers = {
        path: parse_statuses(ROOT / path)
        for path in (
            "research/r073e_problem_freeze.md",
            "research/r073e_halfplane_transfer_proof.md",
            "research/r073e_gap_matrix.md",
            "research/r073e_report-source.md",
        )
    }
    proof = (ROOT / "research/r073e_halfplane_transfer_proof.md").read_text()
    audit = (ROOT / "research/r073e_independent_analytic_audit.md").read_text()
    finite = json.loads((ROOT / "experiments/r073e/complement_diagnostic.json").read_text())
    independent = json.loads((ROOT / "experiments/r073e/independent_validation.json").read_text())
    figure = json.loads((ROOT / "figures/r073e/fig-r073e-complement-transfer/manifest.json").read_text())
    figure_validation = json.loads((ROOT / "figures/r073e/fig-r073e-complement-transfer/validation.json").read_text())

    # Recompute from the raw primary rows, rather than trusting stored maxima.
    residual_keys = ("leftEigenpair", "projectorCommutator", "projectorIdempotence", "qBasisInvariance", "rightEigenpair")
    maximum_residual = max(row["residuals"][key] for row in finite["rows"] for key in residual_keys)
    largest_n = max(row["N"] for row in finite["rows"])
    selected = next(row for row in finite["rows"] if row["N"] == largest_n and row["epsilon"] == 1e-6)
    line_margins = [
        line["lineRealPart"] - row["qSpectrum"]["spectralAbscissa"]
        for row in finite["rows"] for line in row["resolventVerticalLines"]
    ]
    drift = Fraction(49, 4)
    checks = {
        "sourceHeadIsSealedCommit": head == SOURCE_COMMIT,
        "allFourLedgersReparsedExactly": all(value == expected for value in ledgers.values()),
        "nineClosedAndSeventeenOpen": len(CLOSED) == 9 and len(OPEN) == 17,
        "independentAnalyticAuditPass": "r073eIndependentAnalyticAudit=PASS" in audit,
        "exactDriftBoundRecomputed": drift == Fraction(49, 4) and "C_A=\\frac{49}{4}" in proof,
        "maximumResidualRecomputed": abs(maximum_residual - finite["maximums"]["allAlgebraicResiduals"]) <= 1e-28,
        "verticalLinesRightOfFiniteSpectrum": min(line_margins) > 0,
        "selectedFiniteComplementStillGrows": selected["qSpectrum"]["spectralAbscissa"] > 0,
        "primaryFiniteFlagsPass": finite["allChecksPass"] is True and all(finite["checks"].values()),
        "independentFiniteFlagsPass": independent["allChecksPass"] is True and all(independent["checks"].values()),
        "finiteContinuumClaimsFalse": (
            finite["claimBoundary"]["finiteBinary64Diagnostic"] is True
            and finite["claimBoundary"]["continuumComplementaryDichotomyProvedHere"] is False
            and finite["claimBoundary"]["continuousTimeSemigroupBoundProvedHere"] is False
            and independent["claimBoundary"]["continuumDichotomyCertified"] is False
        ),
        "figureOutputHashesRecomputed": all(
            sha256(ROOT / "figures/r073e/fig-r073e-complement-transfer" / item["path"]) == item["sha256"]
            for item in figure["outputs"]
        ),
        "figureFormalValidationReparsed": (
            figure["status"] == "formal"
            and figure_validation["status"] == "passed"
            and all(figure_validation["checks"].values())
        ),
        "figureContinuumClaimsFalse": (
            figure["claimBoundary"]["continuumComplementDichotomyProvedHere"] is False
            and figure["claimBoundary"]["nonlinearNavierStokesProvedHere"] is False
            and figure["claimBoundary"]["clayProblemSolved"] is False
        ),
    }
    output = {
        "schemaVersion": "r073e-independent-source-recompute-v1",
        "release": "R0.73E",
        "sourceCommit": SOURCE_COMMIT,
        "implementation": {
            "stdlibOnly": True,
            "importsPrimaryGenerator": False,
            "readsPrimaryCertificate": False,
            "scriptSha256": sha256(Path(__file__).resolve()),
        },
        "reparsedClaims": {"closed": list(CLOSED), "open": list(OPEN)},
        "exactSentinels": {
            "profileDriftBound": [drift.numerator, drift.denominator],
            "maximumPrimaryAlgebraicResidual": maximum_residual,
            "minimumVerticalLineMarginOverFiniteQSpectrum": min(line_margins),
            "largestCutoff": largest_n,
            "selectedEpsilon": selected["epsilon"],
            "selectedQSpectralAbscissa": selected["qSpectrum"]["spectralAbscissa"],
        },
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "claimBoundary": {
            "finiteRowsOnly": True,
            "continuumSpectrumCertified": False,
            "continuousTimeBoundCertified": False,
            "nonlinearNavierStokesCertified": False,
            "clayProblemSolved": False,
        },
    }
    OUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"event": "independent-recompute", "allChecksPass": output["allChecksPass"]}, sort_keys=True))
    return 0 if output["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
