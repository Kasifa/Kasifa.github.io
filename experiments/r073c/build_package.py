#!/usr/bin/env python3
"""Build and fail-closed validate the deterministic R0.73C evidence package.

This script uses only the Python standard library.  It does not import either
interval integrator or either finite Fourier producer.  The theorem-bearing
evidence is the endpoint sign bracket for the infinite-dimensional periodic
Rayleigh ODE.  Fourier data are bound only as finite diagnostics.
"""

from __future__ import annotations

import ast
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

RAW_OUTPUTS = [
    "interval_run_a.json",
    "interval_run_b.json",
    "decimal_interval_validation.json",
    "fourier_screen.json",
    "independent_fourier_validation.json",
]
CANONICAL_OUTPUTS = [
    "canonical_interval_run_a.json",
    "canonical_interval_run_b.json",
    "canonical_decimal_interval_validation.json",
    "canonical_fourier_screen.json",
    "canonical_independent_fourier_validation.json",
]
RAW_PROGRESS = [
    "interval_progress_a.ndjson",
    "interval_progress_b.ndjson",
    "decimal_progress.ndjson",
    "fourier_progress.ndjson",
]
SOURCE_FILES = [
    "research/r073c_interval_monodromy.py",
    "experiments/r073c/independent_decimal_monodromy_validator.py",
    "research/r073c_spectral_screen_agent.py",
    "experiments/r073c/independent_fourier_spectral_validator.py",
]
STATIC_FILES = [
    "experiments/r073c/README.md",
    "experiments/r073c/command.txt",
    "experiments/r073c/contract.json",
    "experiments/r073c/requirements.txt",
    "experiments/r073c/build_package.py",
]
GENERATED_FILES = [
    "environment.json",
    "summary.json",
    "validation.json",
    "progress.ndjson",
]
PACKAGE_FILES = [
    "README.md",
    "build_package.py",
    "command.txt",
    "contract.json",
    "canonical_decimal_interval_validation.json",
    "canonical_fourier_screen.json",
    "canonical_independent_fourier_validation.json",
    "canonical_interval_run_a.json",
    "canonical_interval_run_b.json",
    "environment.json",
    "independent_decimal_monodromy_validator.py",
    "independent_fourier_spectral_validator.py",
    "manifest.json",
    "progress.ndjson",
    "requirements.txt",
    "summary.json",
    "validation.json",
]

EXPECTED_KERNELS = {
    "ctx_iv.py": (17211, "b6a74cafe1837e4664d4486819e0806a3cbba50bfe456b6b56a8588df23caf88"),
    "libmp/libmpi.py": (27622, "bb4239122c24a9afb8f9d5c44e2e64eccb9ac417996ef0803c5b65f7753d605d"),
    "libmp/libmpf.py": (45021, "be93f490d56449c6c2568668809e166ad97823b09ed1de1dcc75637d57b9eeca"),
    "libmp/libelefun.py": (43861, "8e80593f814e7713df89e5aca352cfb52afa747c9da46fcb42217f6d841858c8"),
}


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def compact(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path, display: str | None = None) -> dict[str, Any]:
    return {
        "bytes": path.stat().st_size,
        "path": display if display is not None else path.name,
        "sha256": sha256(path),
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> Any:
    def reject_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON constant {value} in {path}")

    return json.loads(path.read_text(), parse_constant=reject_constant)


def all_finite(value: Any) -> bool:
    if isinstance(value, bool) or value is None or isinstance(value, (str, int)):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, list):
        return all(all_finite(item) for item in value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and all_finite(item)
                   for key, item in value.items())
    return False


def decimal_fraction(value: str) -> Fraction:
    return Fraction(Decimal(value))


def parse_decimal_interval(text: str) -> tuple[Fraction, Fraction]:
    require(text.startswith("[") and text.endswith("]"),
            f"invalid interval text: {text}")
    pieces = text[1:-1].split(",")
    require(len(pieces) == 2, f"invalid interval pair: {text}")
    lower, upper = (decimal_fraction(piece.strip()) for piece in pieces)
    require(lower <= upper, f"reversed interval: {text}")
    return lower, upper


def binary_value(record_: dict[str, Any]) -> Fraction:
    require(set(record_) == {"bitcount", "exponent", "mantissa", "sign"},
            "unexpected binary-endpoint fields")
    mantissa = record_["mantissa"]
    exponent = record_["exponent"]
    sign = record_["sign"]
    bitcount = record_["bitcount"]
    require(type(mantissa) is int and mantissa > 0, "invalid mantissa")
    require(type(exponent) is int, "invalid exponent")
    require(type(bitcount) is int, "invalid bitcount")
    require(type(sign) is int and sign in (0, 1), "invalid sign bit")
    require(bitcount == mantissa.bit_length(), "bitcount mismatch")
    magnitude = (Fraction(mantissa) * (2 ** exponent) if exponent >= 0
                 else Fraction(mantissa, 2 ** (-exponent)))
    return -magnitude if sign else magnitude


def primary_interval(record_: dict[str, Any], key: str) -> tuple[Fraction, Fraction]:
    item = record_[key]
    displayed = parse_decimal_interval(item["decimal"])
    binary = tuple(binary_value(endpoint) for endpoint in item["binaryEndpoints"])
    require(len(binary) == 2 and binary[0] <= binary[1],
            f"invalid exact binary interval for {key}")
    # mpmath's human-readable interval string is rounded for display and is
    # not itself the proof object.  Require close agreement, but decide every
    # sign and containment question from the exact binary endpoint tuples.
    display_tolerance = Fraction(1, 10 ** 35)
    require(abs(displayed[0] - binary[0]) <= display_tolerance
            and abs(displayed[1] - binary[1]) <= display_tolerance,
            f"displayed interval disagrees with binary endpoints for {key}")
    return binary[0], binary[1]


def decimal_interval(record_: dict[str, Any], key: str) -> tuple[Fraction, Fraction]:
    item = record_[key]
    lower = decimal_fraction(item["lower"])
    upper = decimal_fraction(item["upper"])
    require(lower <= upper, f"reversed Decimal interval for {key}")
    return lower, upper


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def canonicalize_evidence(value: Any) -> Any:
    """Remove machine-local presentation fields without changing evidence.

    The original producer files remain untouched as local audit/telemetry.
    Formal manifests bind only this normalized representation.
    """
    timing_keys = {"elapsedSeconds", "runtimeSeconds"}
    known_paths = (
        "research/r073c_interval_monodromy.py",
        "experiments/r073c/independent_decimal_monodromy_validator.py",
        "experiments/r073c/fourier_screen.json",
        "experiments/r073c/independent_fourier_spectral_validator.py",
    )
    if isinstance(value, list):
        return [canonicalize_evidence(item) for item in value]
    if not isinstance(value, dict):
        return value
    result: dict[str, Any] = {}
    for key, item in value.items():
        if key in timing_keys or key == "platform":
            continue
        if key == "path" and isinstance(item, str) and item.startswith("/"):
            matches = [relative for relative in known_paths
                       if item == str(ROOT / relative) or item.endswith("/" + relative)]
            require(len(matches) == 1, f"unrecognized absolute evidence path: {item}")
            result[key] = matches[0]
        else:
            result[key] = canonicalize_evidence(item)
    return result


def validate_primary_run(
    data: dict[str, Any],
    *,
    run_id: str,
    steps: int,
    order: int,
    dps: int,
    source_sha: str,
) -> dict[str, tuple[Fraction, Fraction]]:
    require(data["schemaVersion"] == "r073c-interval-monodromy-v2",
            f"{run_id}: schema mismatch")
    require(data["status"] == "passed" and data["runId"] == run_id,
            f"{run_id}: run status/id mismatch")
    require(data["dps"] == dps, f"{run_id}: precision mismatch")
    require(data["arithmetic"].startswith("mpmath 1.3.0 iv directed"),
            f"{run_id}: arithmetic mismatch")
    environment = data["environment"]
    require(environment["mpmath"] == "1.3.0", f"{run_id}: mpmath mismatch")
    require(environment["source"]["sha256"] == source_sha,
            f"{run_id}: producer hash mismatch")
    require(environment["source"]["bytes"] == (ROOT / "research/r073c_interval_monodromy.py").stat().st_size,
            f"{run_id}: producer size mismatch")
    kernels = {
        row["path"]: (row["bytes"], row["sha256"])
        for row in environment["arithmeticSources"]
    }
    require(kernels == EXPECTED_KERNELS, f"{run_id}: arithmetic kernel ledger mismatch")
    require(len(data["results"]) == 2, f"{run_id}: expected two endpoints")

    result: dict[str, tuple[Fraction, Fraction]] = {}
    expected_signs = {"0.3407": "negative", "0.3410": "positive"}
    for row in data["results"]:
        eta = row["eta"]
        require(eta in expected_signs and eta not in result,
                f"{run_id}: unexpected/repeated eta")
        require(row["gamma"] == "1/2" and row["steps"] == steps
                and row["order"] == order,
                f"{run_id}: parameter mismatch at eta={eta}")
        require(row["infiniteDimensionalPeriodicOde"] is True
                and row["fourierTruncationUsed"] is False,
                f"{run_id}: theorem-scope mismatch at eta={eta}")
        trace = primary_interval(row, "traceMinusTwo")
        imag = primary_interval(row, "traceImag")
        step_interval = primary_interval(row, "step")
        primary_interval(row, "traceReal")
        require(step_interval[0] > 0, f"{run_id}: nonpositive step")
        require(imag[0] <= 0 <= imag[1]
                and row["traceImagContainsZero"] is True,
                f"{run_id}: trace-imag sentinel failed at eta={eta}")
        sign = "negative" if trace[1] < 0 else "positive" if trace[0] > 0 else "unresolved"
        require(sign == expected_signs[eta] == row["sign"],
                f"{run_id}: endpoint sign failed at eta={eta}")
        result[eta] = trace
    require(set(result) == set(expected_signs), f"{run_id}: endpoint inventory mismatch")
    return result


def main() -> int:
    contract = load_json(HERE / "contract.json")
    primary_a = load_json(HERE / "interval_run_a.json")
    primary_b = load_json(HERE / "interval_run_b.json")
    decimal_data = load_json(HERE / "decimal_interval_validation.json")
    finite_data = load_json(HERE / "fourier_screen.json")
    finite_validation = load_json(HERE / "independent_fourier_validation.json")
    datasets = [contract, primary_a, primary_b, decimal_data, finite_data, finite_validation]
    require(all(all_finite(data) for data in datasets), "non-finite number in JSON input")

    checks: dict[str, bool] = {}
    checks["contractRelease"] = contract["release"] == "R0.73C"
    checks["contractBracket"] = contract["formalBracket"] == {
        "etaLeft": "0.3407",
        "etaRight": "0.3410",
        "gamma": "1/2",
        "requiredLeftSign": "negative",
        "requiredRightSign": "positive",
        "sigmaOpenInterval": ["0.17035", "0.17050"],
    }
    checks["contractClaimBoundary"] = (
        contract["claimBoundary"]["infiniteDimensionalFrozenEigenvalueProvedAfterAnalyticBridge"] is True
        and contract["claimBoundary"]["finiteFourierCutoffConvergenceIsProof"] is False
        and contract["claimBoundary"]["rootUniquenessProved"] is False
        and contract["claimBoundary"]["algebraicSimplicityProved"] is False
        and contract["claimBoundary"]["viscousSpectralPersistenceProved"] is False
        and contract["claimBoundary"]["nonautonomousTransferProved"] is False
        and contract["claimBoundary"]["nonlinearNavierStokesProved"] is False
        and contract["claimBoundary"]["clayProblemSolved"] is False
    )

    primary_source = ROOT / "research/r073c_interval_monodromy.py"
    primary_sha = sha256(primary_source)
    intervals_a = validate_primary_run(
        primary_a, run_id="partition-a", steps=1024, order=10, dps=40,
        source_sha=primary_sha,
    )
    intervals_b = validate_primary_run(
        primary_b, run_id="partition-b", steps=768, order=12, dps=55,
        source_sha=primary_sha,
    )
    checks["primarySourceHash"] = primary_sha == "b1bdd458a75608c01f0fca64b95c217bb9f1fc01e084e14d641650e7e2b6a1fc"
    checks["primaryIndependentPartitions"] = (
        primary_a["dps"] != primary_b["dps"]
        and primary_a["results"][0]["steps"] != primary_b["results"][0]["steps"]
        and primary_a["results"][0]["order"] != primary_b["results"][0]["order"]
    )
    checks["primaryEndpointSigns"] = all(
        intervals["0.3407"][1] < 0 < intervals["0.3410"][0]
        for intervals in (intervals_a, intervals_b)
    )

    decimal_source = HERE / "independent_decimal_monodromy_validator.py"
    decimal_sha = sha256(decimal_source)
    decimal_imports = imported_roots(decimal_source)
    checks["decimalSourceHash"] = decimal_sha == decimal_data["source"]["sha256"]
    checks["decimalSourceSize"] = decimal_source.stat().st_size == decimal_data["source"]["bytes"]
    checks["decimalIndependentImports"] = not ({"mpmath", "numpy", "scipy", "research"} & decimal_imports)
    checks["decimalRuntimeGate"] = (
        decimal_data["status"] == "passed"
        and decimal_data["arithmetic"]["lowerRounding"] == "ROUND_FLOOR"
        and decimal_data["arithmetic"]["upperRounding"] == "ROUND_CEILING"
        and decimal_data["arithmetic"]["transcendentalLibraryUsed"] is False
        and all(decimal_data["arithmetic"]["checks"].values())
        and all(decimal_data["checks"].values())
    )
    checks["decimalParameters"] = decimal_data["parameters"] == {
        "etaHigh": "0.3410",
        "etaLow": "0.3407",
        "maxPicardAttempts": 12,
        "order": 8,
        "precision": 80,
        "runId": "decimal-independent",
        "steps": 256,
    }
    decimal_intervals: dict[str, tuple[Fraction, Fraction]] = {}
    for row in decimal_data["results"]:
        eta = row["eta"]
        require(eta in {"0.3407", "0.3410"} and eta not in decimal_intervals,
                "Decimal endpoint inventory mismatch")
        trace = decimal_interval(row, "traceMinusTwo")
        imag = decimal_interval(row, "traceImag")
        det_real = decimal_interval(row, "determinantReal")
        det_imag = decimal_interval(row, "determinantImag")
        require(imag[0] <= 0 <= imag[1], f"Decimal trace imaginary miss at {eta}")
        require(det_real[0] <= 1 <= det_real[1]
                and det_imag[0] <= 0 <= det_imag[1],
                f"Decimal determinant sentinel miss at {eta}")
        expected = "negative" if eta == "0.3407" else "positive"
        sign = "negative" if trace[1] < 0 else "positive" if trace[0] > 0 else "unresolved"
        require(sign == expected == row["sign"], f"Decimal sign failed at {eta}")
        require(all(row["checks"].values()), f"Decimal row checks failed at {eta}")
        decimal_intervals[eta] = trace
    checks["decimalEndpointSigns"] = (
        decimal_intervals["0.3407"][1] < 0 < decimal_intervals["0.3410"][0]
    )
    checks["primaryContainedInDecimal"] = all(
        decimal_intervals[eta][0] <= interval[0] <= interval[1] <= decimal_intervals[eta][1]
        for eta in decimal_intervals
        for interval in (intervals_a[eta], intervals_b[eta])
    )
    consequence = decimal_data["theoremConsequence"]
    checks["decimalClaimBoundary"] = (
        consequence["conditionalOnAnalyticMonodromyLemma"] is True
        and consequence["positiveRealPointSpectrumExists"] is True
        and consequence["rootUniquenessProved"] is False
        and consequence["eigenvalueSimplicityProved"] is False
        and decimal_data["claimBoundary"]["nonautonomousTransferProved"] is False
        and decimal_data["claimBoundary"]["nonlinearNavierStokesProved"] is False
        and decimal_data["claimBoundary"]["clayProblemSolved"] is False
    )

    finite_primary_path = HERE / "fourier_screen.json"
    finite_validator_path = HERE / "independent_fourier_spectral_validator.py"
    checks["finitePrimaryInventory"] = (
        finite_data["schemaVersion"] == 1
        and len(finite_data["leadingGalerkinRows"]) == 54
        and len(finite_data["finiteRankApproximationRows"]) == 7
        and finite_data["randomness"] == "none"
    )
    finite_boundary = finite_data["claimBoundary"]
    checks["finitePrimaryBoundary"] = (
        finite_boundary["finiteFourierSpectrumComputed"] is True
        and finite_boundary["fredholmContourSampled"] is True
        and finite_boundary["infiniteDimensionalEigenvalueEnclosed"] is False
        and finite_boundary["determinantWindingIntervalValidated"] is False
        and finite_boundary["fredholmInverseIntervalValidated"] is False
        and finite_boundary["quadratureIntervalValidated"] is False
        and finite_boundary["ordinaryCutoffConvergenceIsProof"] is False
        and finite_boundary["nonautonomousTransferProved"] is False
    )
    checks["finiteValidationStatus"] = (
        finite_validation["status"] == "passed"
        and all(finite_validation["checks"].values())
    )
    checks["finiteSourceBindings"] = (
        finite_validation["primary"]["sha256"] == sha256(finite_primary_path)
        and finite_validation["primary"]["bytes"] == finite_primary_path.stat().st_size
        and finite_validation["validator"]["sha256"] == sha256(finite_validator_path)
        and finite_validation["validator"]["bytes"] == finite_validator_path.stat().st_size
    )
    validation_boundary = finite_validation["claimBoundary"]
    checks["finiteValidationBoundary"] = (
        validation_boundary["independentFiniteMatrixAgreement"] is True
        and validation_boundary["sampledFredholmWindingAgreement"] is True
        and validation_boundary["infiniteDimensionalSpectrumProved"] is False
        and validation_boundary["continuousContourEnclosed"] is False
        and validation_boundary["fourierTailRieszCertificateValidated"] is False
        and validation_boundary["intervalMonodromyValidated"] is False
        and validation_boundary["nonautonomousTransferProved"] is False
        and validation_boundary["nonlinearNavierStokesProved"] is False
        and validation_boundary["clayProblemSolved"] is False
    )
    contour = finite_data["fredholmContourScreen"]
    independent_contour = finite_validation["independentWindingScreen"]
    checks["finiteWindingDiagnostic"] = (
        contour["sampledDeterminantWinding"] == 1.0
        and contour["sampledMinimumSingularValue"] > 0.056
        and independent_contour["winding"] == 1.0
        and independent_contour["minimumSingular"] > 0.056
    )
    candidate = next(row for row in finite_validation["recomputedSentinels"] if row["N"] == 128)
    checks["finiteCandidateInsideCertifiedBracket"] = (
        0.17035 < candidate["leadingReal"] < 0.17050
        and abs(candidate["leadingImag"]) < 1e-12
    )

    require(all(checks.values()), "failed checks: " + ", ".join(
        key for key, passed in checks.items() if not passed
    ))

    canonical_payloads = {
        "canonical_interval_run_a.json": canonicalize_evidence(primary_a),
        "canonical_interval_run_b.json": canonicalize_evidence(primary_b),
        "canonical_decimal_interval_validation.json": canonicalize_evidence(decimal_data),
        "canonical_fourier_screen.json": canonicalize_evidence(finite_data),
        "canonical_independent_fourier_validation.json": canonicalize_evidence(finite_validation),
    }
    for name, payload in canonical_payloads.items():
        rendered = canonical(payload)
        require(str(ROOT) not in rendered and "/Users/" not in rendered,
                f"absolute path survived canonicalization: {name}")
        require("elapsedSeconds" not in rendered and "runtimeSeconds" not in rendered,
                f"wall-time survived canonicalization: {name}")
        (HERE / name).write_text(rendered)

    environment = {
        "builder": {
            "localRuntimeEncoded": False,
            "stdlibOnly": True,
        },
        "independentDecimal": decimal_data["arithmetic"],
        "primaryInterval": {
            "arithmetic": primary_a["arithmetic"],
            "arithmeticSources": primary_a["environment"]["arithmeticSources"],
            "mpmath": primary_a["environment"]["mpmath"],
            "python": primary_a["environment"]["python"],
        },
        "finiteDiagnostics": {
            "numpy": finite_data["numpy"],
            "python": finite_validation["environment"]["python"],
            "scipy": finite_data["scipy"],
            "threadEnvironment": finite_validation["environment"]["threadEnvironment"],
        },
        "schemaVersion": "r073c-experiment-environment-v1",
    }
    (HERE / "environment.json").write_text(canonical(environment))

    def exact_decimal(value: Fraction) -> str:
        # Every bound here has a denominator that is a power of 2 or 10, so
        # 180 digits are ample for an exact terminating representation.
        with localcontext() as context:
            context.prec = 180
            return format(Decimal(value.numerator) / Decimal(value.denominator), "f")

    def interval_text(interval: tuple[Fraction, Fraction]) -> list[str]:
        return [exact_decimal(interval[0]), exact_decimal(interval[1])]

    summary = {
        "analyticBridgeRequired": [
            "det(M)=1",
            "trace(M) is real",
            "periodic solution iff trace(M)=2",
            "continuity in eta>0",
            "sigma=gamma*eta",
        ],
        "claimBoundary": {
            "algebraicSimplicityProved": False,
            "clayProblemSolved": False,
            "finiteFourierDataUsedAsProof": False,
            "nonautonomousTransferProved": False,
            "nonlinearNavierStokesProved": False,
            "rootUniquenessProved": False,
            "viscousSpectralPersistenceProved": False,
        },
        "finiteDiagnostic": {
            "candidateAtN128": candidate["leadingReal"],
            "independentMinimumSampledSingular": independent_contour["minimumSingular"],
            "independentSampledWinding": independent_contour["winding"],
            "leadingGalerkinRows": len(finite_data["leadingGalerkinRows"]),
            "primaryMinimumSampledSingular": contour["sampledMinimumSingularValue"],
            "primarySampledWinding": contour["sampledDeterminantWinding"],
            "scope": "finite matrices and sampled contour only",
        },
        "formalBracket": {
            "etaOpenInterval": ["0.3407", "0.3410"],
            "gamma": "1/2",
            "independentDecimal": {
                "etaLeft": interval_text(decimal_intervals["0.3407"]),
                "etaRight": interval_text(decimal_intervals["0.3410"]),
            },
            "primaryPartitionA": {
                "etaLeft": interval_text(intervals_a["0.3407"]),
                "etaRight": interval_text(intervals_a["0.3410"]),
            },
            "primaryPartitionB": {
                "etaLeft": interval_text(intervals_b["0.3407"]),
                "etaRight": interval_text(intervals_b["0.3410"]),
            },
            "sigmaOpenInterval": ["0.17035", "0.17050"],
        },
        "release": "R0.73C",
        "schemaVersion": "r073c-experiment-summary-v1",
        "status": "passed",
        "theoremEvidence": "two primary interval partitions plus an independent Decimal interval kernel",
    }
    (HERE / "summary.json").write_text(canonical(summary))

    validation = {
        "checks": checks,
        "claimBoundary": summary["claimBoundary"],
        "schemaVersion": "r073c-experiment-validation-v1",
        "status": "passed",
        "validator": record(HERE / "build_package.py", "experiments/r073c/build_package.py"),
    }
    (HERE / "validation.json").write_text(canonical(validation))

    joined: list[dict[str, Any]] = []
    for stream_name in RAW_PROGRESS:
        path = HERE / stream_name
        for index, line in enumerate(path.read_text().splitlines()):
            if not line.strip():
                continue
            event = json.loads(line)
            require(all_finite(event), f"non-finite progress event in {stream_name}")
            event.pop("elapsedSeconds", None)
            event["eventIndex"] = index
            event["sourceStream"] = stream_name
            joined.append(event)
    joined.append({
        "checksPassed": len(checks),
        "event": "package-complete",
        "eventIndex": 0,
        "sourceStream": "build_package.py",
        "status": "passed",
    })
    (HERE / "progress.ndjson").write_text("".join(compact(event) + "\n" for event in joined))

    source_paths = [ROOT / path for path in SOURCE_FILES + STATIC_FILES]
    canonical_paths = [HERE / name for name in CANONICAL_OUTPUTS]
    output_paths = [HERE / name for name in GENERATED_FILES]
    require(all(path.is_file() for path in source_paths + canonical_paths + output_paths),
            "manifest inventory is incomplete")
    manifest = {
        "builder": record(HERE / "build_package.py", "experiments/r073c/build_package.py"),
        "claimBoundary": summary["claimBoundary"],
        "generatedOutputs": [record(path) for path in output_paths],
        "excludedLocalInputs": [{
            "path": name,
            "reason": "raw producer artifact or wall-time telemetry; normalized evidence is bound instead",
        } for name in RAW_OUTPUTS + RAW_PROGRESS],
        "rawEvidence": [record(path) for path in canonical_paths],
        "release": "R0.73C",
        "schemaVersion": "r073c-experiment-manifest-v1",
        "sourceBindings": [record(path, str(path.relative_to(ROOT))) for path in source_paths],
        "status": "passed",
    }
    (HERE / "manifest.json").write_text(canonical(manifest))

    require(all((HERE / name).is_file() for name in PACKAGE_FILES),
            "SHA256SUMS inventory is incomplete")
    sums = [f"{sha256(HERE / name)}  {name}" for name in sorted(PACKAGE_FILES)]
    (HERE / "SHA256SUMS").write_text("\n".join(sums) + "\n")
    print(canonical({
        "checksPassed": len(checks),
        "manifestSha256": sha256(HERE / "manifest.json"),
        "status": "passed",
        "summarySha256": sha256(HERE / "summary.json"),
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
