#!/usr/bin/env python3
"""Independent fail-closed validator for the R0.73H certificate package."""

from __future__ import annotations

import argparse
import ast
import csv
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import re
import struct
import subprocess
from typing import Iterable, Mapping
import zipfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_FILES = (
    "research/certificates/r073h/README.md",
    "research/certificates/r073h/command.txt",
    "research/certificates/r073h/config.json",
    "research/certificates/r073h/requirements.txt",
    "research/certificates/r073h/exact_q2_certificate.py",
    "research/certificates/r073h/independent_exact_q2.py",
    "research/certificates/r073h/primary_diagnostic.py",
    "research/certificates/r073h/independent_validate.py",
    "research/certificates/r073h/generate_certificate.py",
    "research/certificates/r073h/validate_certificate.py",
    "research/certificates/r073h/seal_package.py",
)
PRE_CERTIFICATE_FILES = (
    "exact_q2_certificate.json",
    "independent_exact_q2.json",
    "primary_rows.csv",
    "cutoff_convergence.csv",
    "step_convergence.csv",
    "coefficient_snapshots.npz",
    "environment.json",
    "primary_summary.json",
    "progress.ndjson",
    "primary_manifest.json",
    "independent_validation.json",
    "independent_progress.ndjson",
)
PRE_SEAL_GENERATED = PRE_CERTIFICATE_FILES + ("certificate.json", "validation.json")
ROW_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "smokeMode",
    "gridKind", "archivePrefix", "N", "dimensionPerKz", "viscousEpsilon",
    "absoluteLambda", "profileTime", "fastTime", "fastStep",
    "topEigenvalueFastReal", "topEigenvalueFastImag", "topClusterDimension",
    "topRealGap", "topEigenResidualRelative", "generatorRelativeDefect",
    "unitRealLaunchL2", "v1L2", "v1PositiveKzL2", "v2MeanL2",
    "v2DoublePairL2", "v2L2", "v3MeanPathTargetL2",
    "v3DoublePathTargetL2", "v3TargetPairL2", "v3TriplePairL2", "v3L2",
    "quadraticNaturalResponse", "targetCubicNaturalResponse",
    "tripleCubicNaturalResponse", "quadraticCompensated",
    "targetCubicCompensated", "tripleCubicCompensated",
    "meanPathSignedNaturalParallel", "doublePathSignedNaturalParallel",
    "totalSignedNaturalParallel", "meanPathSignedCompensated",
    "doublePathSignedCompensated", "totalSignedCompensated",
    "meanPathCosineWithLinear", "doublePathCosineWithLinear",
    "totalCubicCosineWithLinear", "v1OuterThreeMassFraction",
    "v2OuterThreeMassFraction", "v3OuterThreeMassFraction",
    "maximumDivergenceRelative", "maximumRealityRelative",
    "forbiddenParityRelative", "caseChecksPass",
)
CONVERGENCE_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "viscousEpsilon",
    "absoluteLambda", "coarseN", "fineN", "linearGainRelativeChange",
    "quadraticNaturalRelativeChange", "targetCubicNaturalRelativeChange",
    "tripleCubicNaturalRelativeChange", "signedCubicRelativeChange",
    "maximumRelativeChange", "finestCutoffGateApplied", "passCheck",
    "ordinaryCutoffAgreementIsTailProof",
)
STEP_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "N",
    "viscousEpsilon", "absoluteLambda", "coarseFastStep", "fineFastStep",
    "linearGainRelativeChange", "quadraticNaturalRelativeChange",
    "targetCubicNaturalRelativeChange", "tripleCubicNaturalRelativeChange",
    "signedCubicRelativeChange", "maximumRelativeChange", "passCheck",
)
METRIC_SOURCE = {
    "linearGainRelativeChange": "v1L2",
    "quadraticNaturalRelativeChange": "quadraticNaturalResponse",
    "targetCubicNaturalRelativeChange": "targetCubicNaturalResponse",
    "tripleCubicNaturalRelativeChange": "tripleCubicNaturalResponse",
    "signedCubicRelativeChange": "totalSignedNaturalParallel",
}
NPZ_ENDPOINT_FIELDS = (
    "v1L2", "v1PositiveKzL2", "v2MeanL2", "v2DoublePairL2", "v2L2",
    "v3MeanPathTargetL2", "v3DoublePathTargetL2", "v3TargetPairL2",
    "v3TriplePairL2", "v3L2", "quadraticNaturalResponse",
    "targetCubicNaturalResponse", "tripleCubicNaturalResponse",
    "quadraticCompensated", "targetCubicCompensated", "tripleCubicCompensated",
    "meanPathSignedNaturalParallel", "doublePathSignedNaturalParallel",
    "totalSignedNaturalParallel", "meanPathSignedCompensated",
    "doublePathSignedCompensated", "totalSignedCompensated",
    "meanPathCosineWithLinear", "doublePathCosineWithLinear",
    "totalCubicCosineWithLinear", "v1OuterThreeMassFraction",
    "v2OuterThreeMassFraction", "v3OuterThreeMassFraction",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--package-dir", type=Path, default=HERE)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    return parser.parse_args()


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def no_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def loads_json(text: str) -> object:
    return json.loads(
        text, object_pairs_hook=no_duplicate_pairs, parse_constant=reject_constant
    )


def load_json(path: Path) -> dict[str, object]:
    value = loads_json(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"top-level JSON value is not an object: {path.name}")
    return value


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path: Path, base: Path) -> dict[str, object]:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"expected regular non-symlink file: {path}")
    return {
        "path": path.resolve().relative_to(base.resolve()).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def verify_bindings(value: object, base: Path, expected: set[str]) -> bool:
    if not isinstance(value, list) or len(value) != len(expected):
        return False
    seen: set[str] = set()
    for row in value:
        if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256"}:
            return False
        name = row.get("path")
        if not isinstance(name, str) or name not in expected or name in seen:
            return False
        if Path(name).is_absolute() or ".." in Path(name).parts:
            return False
        seen.add(name)
        if binding(base / name, base) != row:
            return False
    return seen == expected


def parse_fraction(text: object) -> Fraction:
    if not isinstance(text, str) or not re.fullmatch(r"-?[0-9]+/[1-9][0-9]*", text):
        raise ValueError(f"noncanonical rational: {text!r}")
    numerator, denominator = text.split("/")
    value = Fraction(int(numerator), int(denominator))
    if f"{value.numerator}/{value.denominator}" != text:
        raise ValueError(f"unreduced rational: {text}")
    return value


def close(left: float, right: float, tolerance: float = 5.0e-12) -> bool:
    return math.isfinite(left) and math.isfinite(right) and abs(left - right) <= tolerance * max(
        1.0, abs(left), abs(right)
    )


def source_gate(source_commit: str, smoke: bool) -> dict[str, object]:
    if smoke:
        return {"enforced": False, "sourceCommit": None, "allSourceBlobsMatch": False}
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("formal validation requires a full lowercase source commit")
    resolved = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", f"{source_commit}^{{commit}}"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if resolved != source_commit:
        raise RuntimeError("source commit did not resolve exactly")
    head = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", source_commit, head],
        check=False,
    ).returncode != 0:
        raise RuntimeError("source commit is not an ancestor of HEAD")
    bindings = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        tree = subprocess.run(
            ["git", "-C", str(ROOT), "ls-tree", source_commit, relative],
            check=True, capture_output=True, text=True,
        ).stdout.split()
        if len(tree) < 3 or tree[0] not in {"100644", "100755"}:
            raise RuntimeError(f"source is not a regular Git blob: {relative}")
        committed = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{source_commit}:{relative}"],
            check=True, capture_output=True,
        ).stdout
        working = path.read_bytes()
        if committed != working:
            raise RuntimeError(f"working source differs from source commit: {relative}")
        bindings.append({
            "path": relative,
            "gitMode": tree[0],
            "bytes": len(working),
            "sha256": hashlib.sha256(working).hexdigest(),
        })
    return {
        "enforced": True,
        "sourceCommit": source_commit,
        "headAtValidation": head,
        "sourceCommitIsAncestorOfHead": True,
        "allSourceBlobsMatch": True,
        "bindings": bindings,
    }


def provenance_matches(value: object, smoke: bool, source_commit: str) -> bool:
    if not isinstance(value, dict):
        return False
    if smoke:
        return value.get("enforced") is False and value.get("sourceCommit") is None
    return (
        value.get("enforced") is True
        and value.get("sourceCommit") == source_commit
        and value.get("allSourceBlobsMatch") is True
    )


def expected_matrix() -> list[list[Fraction]]:
    modes = range(-4, 5)
    potential = {
        0: Fraction(-9, 16),
        1: Fraction(9, 32), -1: Fraction(9, 32),
        2: Fraction(-9, 64), -2: Fraction(-9, 64),
        3: Fraction(9, 32), -3: Fraction(9, 32),
        4: Fraction(-9, 64), -4: Fraction(-9, 64),
    }
    return [[
        potential.get(i - j, Fraction(0))
        + (Fraction(i * i + 1) - Fraction(1, 5) if i == j else Fraction(0))
        for j in modes
    ] for i in modes]


def bareiss(integer_matrix: list[list[int]]) -> int:
    size = len(integer_matrix)
    if size == 0:
        return 1
    work = [row[:] for row in integer_matrix]
    previous = 1
    sign = 1
    for k in range(size - 1):
        if work[k][k] == 0:
            swap = next((index for index in range(k + 1, size) if work[index][k]), None)
            if swap is None:
                return 0
            work[k], work[swap] = work[swap], work[k]
            sign *= -1
        pivot = work[k][k]
        for i in range(k + 1, size):
            for j in range(k + 1, size):
                numerator = work[i][j] * pivot - work[i][k] * work[k][j]
                if numerator % previous:
                    raise ArithmeticError("non-exact Bareiss division")
                work[i][j] = numerator // previous
        previous = pivot
    return sign * work[-1][-1]


def validate_exact(primary: Mapping[str, object], independent: Mapping[str, object]) -> dict[str, bool]:
    expected_primary_keys = {
        "schemaVersion", "release", "evidenceClass", "finiteGalerkinPdeProof",
        "sourceProvenance", "fourierBlock", "tailCrossSchur", "profilePerturbation",
        "rateMargins", "checks", "allChecksPass", "claimBoundary",
    }
    expected_independent_keys = {
        "schemaVersion", "release", "evidenceClass", "method",
        "usedPrimaryLdlImplementation", "sourceProvenance", "commonIntegerDenominator",
        "leadingPrincipalMinors", "schurShiftDeterminant", "perturbedLower",
        "twoRateMargin", "threeRateMargin", "checks", "allChecksPass", "claimBoundary",
    }
    block = primary["fourierBlock"]
    assert isinstance(block, dict)
    matrix = [[parse_fraction(value) for value in row] for row in block["matrix"]]
    lower = [[parse_fraction(value) for value in row] for row in block["ldlUnitLower"]]
    pivots = [parse_fraction(value) for value in block["ldlPivots"]]
    target = expected_matrix()
    shape = len(matrix) == len(lower) == len(pivots) == 9 and all(
        len(row) == 9 for row in matrix + lower
    )
    ldl = shape and all(
        lower[i][i] == 1
        and all(lower[i][j] == 0 for j in range(i + 1, 9))
        and pivots[i] > 0
        for i in range(9)
    )
    reconstructed = shape and all(
        matrix[i][j] == sum(lower[i][k] * pivots[k] * lower[j][k] for k in range(9))
        for i in range(9) for j in range(9)
    )
    denominator = math.lcm(*(value.denominator for row in target for value in row))
    integers = [[int(value * denominator) for value in row] for row in target]
    minors = [
        Fraction(bareiss([row[:size] for row in integers[:size]]), denominator**size)
        for size in range(1, 10)
    ]
    stored_minors = [parse_fraction(value) for value in independent["leadingPrincipalMinors"]]
    tail = primary["tailCrossSchur"]
    perturb = primary["profilePerturbation"]
    rates = primary["rateMargins"]
    assert isinstance(tail, dict) and isinstance(perturb, dict) and isinstance(rates, dict)
    shifted = [[parse_fraction(value) for value in row] for row in tail["shiftedTwoByTwo"]]
    constants = (
        parse_fraction(tail["lowBlockLower"]) == Fraction(1, 5)
        and parse_fraction(tail["tailLower"]) == Fraction(95, 4)
        and parse_fraction(tail["crossNormUpper"]) == Fraction(27, 16)
        and parse_fraction(tail["targetLower"]) == Fraction(1, 20)
        and shifted == [[Fraction(3, 20), Fraction(-27, 16)], [Fraction(-27, 16), Fraction(237, 10)]]
        and parse_fraction(tail["shiftedDeterminant"]) == Fraction(4527, 6400)
        and parse_fraction(perturb["maximumProfileTime"]) == Fraction(1, 450)
        and parse_fraction(perturb["operatorDifferenceUpper"]) == Fraction(1, 40)
        and parse_fraction(perturb["hdLower"]) == Fraction(1, 40)
        and parse_fraction(rates["twoRMinusOneThirdStrictlyGreaterThan"]) == Fraction(221, 30000)
        and parse_fraction(rates["threeRMinusOneHalfStrictlyGreaterThan"]) == Fraction(221, 20000)
        and parse_fraction(independent["schurShiftDeterminant"]) == Fraction(4527, 6400)
        and parse_fraction(independent["perturbedLower"]) == Fraction(1, 40)
        and parse_fraction(independent["twoRateMargin"]) == Fraction(221, 30000)
        and parse_fraction(independent["threeRateMargin"]) == Fraction(221, 20000)
    )
    return {
        "exactPrimaryTopLevelSchema": set(primary) == expected_primary_keys,
        "exactIndependentTopLevelSchema": set(independent) == expected_independent_keys,
        "storedMatrixEqualsIndependentlyRebuiltMatrix": matrix == target,
        "storedLdlExactlyReconstructsMatrixWithPositivePivots": ldl and reconstructed,
        "independentBareissDenominatorIs320": denominator == 320 and independent["commonIntegerDenominator"] == 320,
        "independentBareissMinorsRecomputedAndPositive": stored_minors == minors and all(value > 0 for value in minors),
        "schurPerturbationAndRateConstantsRecomputed": constants,
        "bothExactProducersPassed": primary["allChecksPass"] is True and independent["allChecksPass"] is True,
        "exactEvidenceBoundaryIsExplicit": (
            primary["finiteGalerkinPdeProof"] is False
            and independent["usedPrimaryLdlImplementation"] is False
            and independent["claimBoundary"]["finiteGalerkinPdeProof"] is False
        ),
    }


def read_csv(path: Path, fields: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != fields or len(fields) != len(set(fields)):
            raise ValueError(f"unexpected CSV header: {path.name}")
        rows = list(reader)
    if any(None in row or set(row) != set(fields) for row in rows):
        raise ValueError(f"malformed CSV row: {path.name}")
    return rows


def strict_bool(value: str) -> bool:
    if value not in {"true", "false"}:
        raise ValueError(f"invalid CSV boolean: {value!r}")
    return value == "true"


def finite_float(value: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"nonfinite CSV number: {value!r}")
    return result


def relative_change(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def log_slope(rows: list[Mapping[str, str]], field: str) -> float:
    x = [math.log(finite_float(row["viscousEpsilon"])) for row in rows]
    y = [math.log(finite_float(row[field])) for row in rows]
    x0, y0 = sum(x) / len(x), sum(y) / len(y)
    return sum((a - x0) * (b - y0) for a, b in zip(x, y)) / sum((a - x0) ** 2 for a in x)


def validate_progress(path: Path, smoke: bool, source_commit: str, independent: bool) -> bool:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        value = loads_json(line)
        if not isinstance(value, dict):
            return False
        records.append(value)
    if not records or [row.get("sequence") for row in records] != list(range(1, len(records) + 1)):
        return False
    if records[0].get("event") != "start" or records[-1].get("event") != "complete":
        return False
    if records[-1].get("allChecksPass") is not True:
        return False
    if not independent:
        return (
            records[0].get("smokeMode") is smoke
            and records[0].get("sourceCommit") == (None if smoke else source_commit)
        )
    return records[0].get("smokeMode") is smoke


def parse_npy(raw: bytes) -> tuple[dict[str, object], bytes]:
    if len(raw) < 10 or raw[:6] != b"\x93NUMPY":
        raise ValueError("invalid NPY magic")
    major, minor = raw[6], raw[7]
    if (major, minor) == (1, 0):
        header_length = struct.unpack("<H", raw[8:10])[0]
        start = 10
    elif major in {2, 3}:
        if len(raw) < 12:
            raise ValueError("truncated NPY header")
        header_length = struct.unpack("<I", raw[8:12])[0]
        start = 12
    else:
        raise ValueError("unsupported NPY version")
    end = start + header_length
    if end > len(raw):
        raise ValueError("truncated NPY header body")
    metadata = ast.literal_eval(raw[start:end].decode("latin1").strip())
    if not isinstance(metadata, dict) or set(metadata) != {"descr", "fortran_order", "shape"}:
        raise ValueError("invalid NPY metadata")
    return metadata, raw[end:]


def l2(values: Iterable[complex]) -> float:
    return math.sqrt(max(0.0, sum(value.real * value.real + value.imag * value.imag for value in values)))


def add(left: list[complex], right: list[complex]) -> list[complex]:
    return [a + b for a, b in zip(left, right)]


def restrict_kz(field: list[complex], n_modes: int, indices: tuple[int, ...]) -> list[complex]:
    width = n_modes * 2
    return [
        field[index * width + offset]
        for index in indices for offset in range(width)
    ]


def outer_fraction(field: list[complex], n_cut: int) -> float:
    n_modes = 2 * n_cut + 1
    total = sum(abs(value) ** 2 for value in field)
    outer = 0.0
    for kz_index in range(7):
        for n_index, n_mode in enumerate(range(-n_cut, n_cut + 1)):
            if abs(n_mode) >= n_cut - 2:
                for component in range(2):
                    outer += abs(field[(kz_index * n_modes + n_index) * 2 + component]) ** 2
    return outer / max(total, 1.0e-300)


def endpoint_metrics(data: bytes, shape: tuple[int, ...], n_cut: int, epsilon: float) -> dict[str, float]:
    snapshots, state_count, kz_count, n_modes, components = shape
    if state_count != 5 or kz_count != 7 or n_modes != 2 * n_cut + 1 or components != 2:
        raise ValueError("unexpected coefficient shape")
    complex_per_state = kz_count * n_modes * components
    complex_per_snapshot = state_count * complex_per_state
    offset = (snapshots - 1) * complex_per_snapshot * 16
    endpoint = [complex(real, imag) for real, imag in struct.iter_unpack("<dd", data[offset:])]
    if len(endpoint) != complex_per_snapshot:
        raise ValueError("invalid endpoint byte count")
    states = [
        endpoint[index * complex_per_state:(index + 1) * complex_per_state]
        for index in range(state_count)
    ]
    first, second0, second2, third0, third2 = states
    second = add(second0, second2)
    third = add(third0, third2)
    target_indices = (2, 4)
    triple_indices = (0, 6)
    first_target = restrict_kz(first, n_modes, target_indices)
    third0_target = restrict_kz(third0, n_modes, target_indices)
    third2_target = restrict_kz(third2, n_modes, target_indices)
    third_target = add(third0_target, third2_target)
    third_triple = restrict_kz(third, n_modes, triple_indices)
    gain = l2(first_target)
    gain2, gain3, gain4 = gain**2, gain**3, gain**4

    def alignment(value: list[complex]) -> tuple[float, float, float]:
        inner_real = sum((a.conjugate() * b).real for a, b in zip(first_target, value))
        value_norm = l2(value)
        natural = inner_real / max(gain4, 1.0e-300)
        return natural, natural / epsilon**2, inner_real / max(gain * value_norm, 1.0e-300)

    mean_natural, mean_compensated, mean_cosine = alignment(third0_target)
    double_natural, double_compensated, double_cosine = alignment(third2_target)
    total_natural, total_compensated, total_cosine = alignment(third_target)
    quadratic = l2(second) / max(gain2, 1.0e-300)
    target_cubic = l2(third_target) / max(gain3, 1.0e-300)
    triple_cubic = l2(third_triple) / max(gain3, 1.0e-300)
    return {
        "v1L2": gain,
        "v1PositiveKzL2": l2(restrict_kz(first, n_modes, (4,))),
        "v2MeanL2": l2(second0),
        "v2DoublePairL2": l2(second2),
        "v2L2": l2(second),
        "v3MeanPathTargetL2": l2(third0_target),
        "v3DoublePathTargetL2": l2(third2_target),
        "v3TargetPairL2": l2(third_target),
        "v3TriplePairL2": l2(third_triple),
        "v3L2": l2(third),
        "quadraticNaturalResponse": quadratic,
        "targetCubicNaturalResponse": target_cubic,
        "tripleCubicNaturalResponse": triple_cubic,
        "quadraticCompensated": quadratic / epsilon,
        "targetCubicCompensated": target_cubic / epsilon**2,
        "tripleCubicCompensated": triple_cubic / epsilon**2,
        "meanPathSignedNaturalParallel": mean_natural,
        "doublePathSignedNaturalParallel": double_natural,
        "totalSignedNaturalParallel": total_natural,
        "meanPathSignedCompensated": mean_compensated,
        "doublePathSignedCompensated": double_compensated,
        "totalSignedCompensated": total_compensated,
        "meanPathCosineWithLinear": mean_cosine,
        "doublePathCosineWithLinear": double_cosine,
        "totalCubicCosineWithLinear": total_cosine,
        "v1OuterThreeMassFraction": outer_fraction(first, n_cut),
        "v2OuterThreeMassFraction": outer_fraction(second, n_cut),
        "v3OuterThreeMassFraction": outer_fraction(third, n_cut),
    }


def validate_npz(
    path: Path,
    archive_index: object,
    endpoint_rows: Mapping[tuple[str, int, float], Mapping[str, str]],
    snapshot_count: int,
) -> tuple[bool, float]:
    if not isinstance(archive_index, list):
        return False, math.inf
    expected_names = {f"{row['archivePrefix']}_states.npy" for row in archive_index}
    maximum_relative = 0.0
    valid = True
    with zipfile.ZipFile(path, "r") as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        valid = valid and len(names) == len(set(names)) and set(names) == expected_names
        for info in infos:
            valid = valid and not info.is_dir()
            valid = valid and Path(info.filename).name == info.filename
        for row in archive_index:
            name = f"{row['archivePrefix']}_states.npy"
            metadata, data = parse_npy(archive.read(name))
            shape = tuple(metadata["shape"])
            n_cut = int(row["N"])
            expected_shape = (snapshot_count, 5, 7, 2 * n_cut + 1, 2)
            valid = valid and metadata["descr"] == "<c16"
            valid = valid and metadata["fortran_order"] is False
            valid = valid and shape == expected_shape and tuple(row["shape"]) == expected_shape
            valid = valid and row["stateOrder"] == [
                "V1", "V2_Kz0", "V2_KzPlusMinus2", "V3_via_Kz0", "V3_via_KzPlusMinus2"
            ]
            expected_bytes = math.prod(expected_shape) * 16
            valid = valid and len(data) == expected_bytes
            finite = all(math.isfinite(value) for pair in struct.iter_unpack("<dd", data) for value in pair)
            valid = valid and finite
            epsilon = float(row["viscousEpsilon"])
            csv_row = endpoint_rows.get((str(row["gridKind"]), n_cut, epsilon))
            if csv_row is None:
                valid = False
                continue
            recomputed = endpoint_metrics(data, expected_shape, n_cut, epsilon)
            for field in NPZ_ENDPOINT_FIELDS:
                actual = finite_float(csv_row[field])
                difference = abs(recomputed[field] - actual) / max(abs(recomputed[field]), abs(actual), 1.0e-300)
                maximum_relative = max(maximum_relative, difference)
                valid = valid and close(recomputed[field], actual)
    return valid, maximum_relative


def validate_finite(
    package: Path,
    config: Mapping[str, object],
    summary: Mapping[str, object],
    manifest: Mapping[str, object],
    independent: Mapping[str, object],
    smoke: bool,
    source_commit: str,
) -> tuple[dict[str, bool], dict[str, object]]:
    rows = read_csv(package / "primary_rows.csv", ROW_FIELDS)
    convergence = read_csv(package / "cutoff_convergence.csv", CONVERGENCE_FIELDS)
    steps = read_csv(package / "step_convergence.csv", STEP_FIELDS)
    grid = summary["formalGrid"]
    assert isinstance(grid, dict)
    cutoffs = [int(value) for value in grid["cutoffs"]]
    epsilons = [float(value) for value in grid["viscousEpsilons"]]
    snapshots = [float(value) for value in grid["profileTimeSnapshots"]]
    holdout = summary["holdout"]["configuration"]
    expected_sequence = [
        ("formal", n_cut, epsilon, profile_time)
        for n_cut in cutoffs for epsilon in epsilons for profile_time in snapshots
    ] + [
        ("holdout", int(holdout["cutoff"]), float(holdout["viscousEpsilon"]), profile_time)
        for profile_time in snapshots
    ]
    actual_sequence = []
    rows_valid = True
    row_lookup: dict[tuple[str, int, float, float], dict[str, str]] = {}
    boolean_fields = {"diagnosticOnly", "smokeMode", "caseChecksPass"}
    string_fields = {"schemaVersion", "evidenceClass", "gridKind", "archivePrefix"}
    for row in rows:
        key = (
            row["gridKind"], int(row["N"]), finite_float(row["viscousEpsilon"]),
            finite_float(row["profileTime"]),
        )
        actual_sequence.append(key)
        rows_valid = rows_valid and key not in row_lookup
        row_lookup[key] = row
        for field in boolean_fields:
            strict_bool(row[field])
        for field in set(ROW_FIELDS) - boolean_fields - string_fields:
            finite_float(row[field])
        rows_valid = rows_valid and strict_bool(row["diagnosticOnly"])
        rows_valid = rows_valid and strict_bool(row["smokeMode"]) is smoke
        rows_valid = rows_valid and strict_bool(row["caseChecksPass"])
        rows_valid = rows_valid and int(row["dimensionPerKz"]) == 2 * int(row["N"]) + 1
        rows_valid = rows_valid and close(finite_float(row["absoluteLambda"]), 1.0 / finite_float(row["viscousEpsilon"]))
        rows_valid = rows_valid and close(finite_float(row["fastTime"]), finite_float(row["profileTime"]) / finite_float(row["viscousEpsilon"]))
    rows_valid = rows_valid and actual_sequence == expected_sequence
    d_end = snapshots[-1]
    endpoint_rows = {
        (kind, n_cut, epsilon): row_lookup[(kind, n_cut, epsilon, d_end)]
        for kind, n_cut, epsilon, _ in expected_sequence if (kind, n_cut, epsilon, d_end) in row_lookup
    }

    convergence_valid = len(convergence) == len(epsilons) * (len(cutoffs) - 1)
    expected_convergence_keys = [
        (epsilon, coarse, fine)
        for epsilon in epsilons for coarse, fine in zip(cutoffs, cutoffs[1:])
    ]
    actual_convergence_keys = []
    for row in convergence:
        key = (finite_float(row["viscousEpsilon"]), int(row["coarseN"]), int(row["fineN"]))
        actual_convergence_keys.append(key)
        left = endpoint_rows[("formal", key[1], key[0])]
        right = endpoint_rows[("formal", key[2], key[0])]
        values = {
            metric: relative_change(finite_float(left[source]), finite_float(right[source]))
            for metric, source in METRIC_SOURCE.items()
        }
        maximum = max(values.values())
        applied = (not smoke) and key[2] == max(cutoffs)
        passed = (not applied) or maximum <= float(config["tolerances"]["finestCutoffRelative"])
        convergence_valid = convergence_valid and all(close(finite_float(row[name]), value) for name, value in values.items())
        convergence_valid = convergence_valid and close(finite_float(row["maximumRelativeChange"]), maximum)
        convergence_valid = convergence_valid and strict_bool(row["finestCutoffGateApplied"]) is applied
        convergence_valid = convergence_valid and strict_bool(row["passCheck"]) is passed
        convergence_valid = convergence_valid and not strict_bool(row["ordinaryCutoffAgreementIsTailProof"])
    convergence_valid = convergence_valid and actual_convergence_keys == expected_convergence_keys

    step_valid = len(steps) == (2 if smoke else 6)
    step_seen: set[tuple[int, float, float, float]] = set()
    for row in steps:
        key = (
            int(row["N"]), finite_float(row["viscousEpsilon"]),
            finite_float(row["coarseFastStep"]), finite_float(row["fineFastStep"]),
        )
        step_valid = step_valid and key not in step_seen and key[2] > key[3] > 0.0
        step_seen.add(key)
        values = [finite_float(row[name]) for name in METRIC_SOURCE]
        maximum = max(values)
        passed = maximum <= float(config["tolerances"]["stepRelative"])
        step_valid = step_valid and all(value >= 0.0 for value in values)
        step_valid = step_valid and close(finite_float(row["maximumRelativeChange"]), maximum)
        step_valid = step_valid and strict_bool(row["passCheck"]) is passed

    finest = max(cutoffs)
    fit_epsilons = [float(value) for value in summary["scaling"]["fitWindowViscousEpsilons"]]
    fit_rows = [endpoint_rows[("formal", finest, epsilon)] for epsilon in fit_epsilons]
    quadratic_slope = log_slope(fit_rows, "quadraticNaturalResponse")
    cubic_slope = log_slope(fit_rows, "targetCubicNaturalResponse")
    slope_gate = not smoke
    slope_expected = {
        "quadraticSlopeInFrozenWindow": (
            not slope_gate or float(config["tolerances"]["quadraticSlopeMinimum"])
            <= quadratic_slope <= float(config["tolerances"]["quadraticSlopeMaximum"])
        ),
        "targetCubicSlopeInFrozenWindow": (
            not slope_gate or float(config["tolerances"]["targetCubicSlopeMinimum"])
            <= cubic_slope <= float(config["tolerances"]["targetCubicSlopeMaximum"])
        ),
    }
    slope_valid = (
        summary["scaling"]["gateApplied"] is slope_gate
        and summary["scaling"]["checks"] == slope_expected
        and close(float(summary["scaling"]["quadraticNaturalLogSlope"]), quadratic_slope)
        and close(float(summary["scaling"]["targetCubicNaturalLogSlope"]), cubic_slope)
    )

    holdout_row = endpoint_rows[("holdout", int(holdout["cutoff"]), float(holdout["viscousEpsilon"]))]
    observed = {
        "quadraticCompensated": finite_float(holdout_row["quadraticCompensated"]),
        "targetCubicCompensated": finite_float(holdout_row["targetCubicCompensated"]),
        "totalSignedCompensated": finite_float(holdout_row["totalSignedCompensated"]),
    }
    predictions = holdout["predictions"]
    holdout_expected = {
        "quadraticCompensatedPrediction": smoke or float(predictions["quadraticCompensatedMinimum"]) <= observed["quadraticCompensated"] <= float(predictions["quadraticCompensatedMaximum"]),
        "targetCubicCompensatedPrediction": smoke or float(predictions["targetCubicCompensatedMinimum"]) <= observed["targetCubicCompensated"] <= float(predictions["targetCubicCompensatedMaximum"]),
        "signedParallelCompensatedPrediction": smoke or float(predictions["signedParallelCompensatedMinimum"]) <= observed["totalSignedCompensated"] <= float(predictions["signedParallelCompensatedMaximum"]),
    }
    holdout_valid = (
        summary["holdout"]["gateApplied"] is (not smoke)
        and summary["holdout"]["checks"] == holdout_expected
        and all(close(float(summary["holdout"]["endpoint"][field]), observed[field]) for field in observed)
    )

    outer_maximum = max(
        finite_float(endpoint_rows[("formal", finest, epsilon)][field])
        for epsilon in epsilons
        for field in ("v1OuterThreeMassFraction", "v2OuterThreeMassFraction", "v3OuterThreeMassFraction")
    )
    outer_valid = (
        close(float(summary["verification"]["finestOuterThreeMassMaximum"]), outer_maximum)
        and (smoke or outer_maximum <= float(config["tolerances"]["outerThreeMassFraction"]))
    )

    archive_valid, archive_maximum = validate_npz(
        package / "coefficient_snapshots.npz", summary["archiveIndex"], endpoint_rows, len(snapshots)
    )
    data_bindings_valid = verify_bindings(
        summary["dataBindings"], package,
        {"primary_rows.csv", "cutoff_convergence.csv", "step_convergence.csv", "coefficient_snapshots.npz", "environment.json"},
    )
    manifest_bindings_valid = verify_bindings(
        manifest["files"], package,
        {"primary_rows.csv", "cutoff_convergence.csv", "step_convergence.csv", "coefficient_snapshots.npz", "environment.json", "primary_summary.json", "progress.ndjson"},
    )
    independent_bindings_valid = verify_bindings(
        independent["primaryBindings"], package,
        {"primary_summary.json", "primary_manifest.json", "coefficient_snapshots.npz"},
    )
    validations = independent["validations"]
    independent_valid = (
        isinstance(validations, list) and len(validations) == (3 if smoke else 5)
        and all(isinstance(row, dict) and row.get("pass") is True for row in validations)
        and independent["allChecksPass"] is True
        and independent["methods"]["importsPrimaryProducer"] is False
        and float(independent["maximumCoefficientRelativeError"]) <= float(config["tolerances"]["independentCoefficientRelative"])
        and float(independent["maximumForbiddenParityRelative"]) <= float(config["tolerances"]["independentForbiddenParityRelative"])
    )
    verification_counts = summary["verification"]
    expected_case_count = len(cutoffs) * len(epsilons)
    counts_valid = (
        verification_counts["caseCount"] == expected_case_count
        and verification_counts["rowCount"] == len(rows)
        and verification_counts["cutoffComparisonCount"] == len(convergence)
        and verification_counts["stepComparisonCount"] == len(steps)
        and len(summary["archiveIndex"]) == expected_case_count + 1
    )
    checks = {
        "primaryTopLevelSchema": set(summary) == {
            "schemaVersion", "release", "evidenceClass", "diagnosticOnly", "smokeMode",
            "pilotInformed", "sourceProvenance", "configBinding", "formalGrid", "holdout",
            "scaling", "verification", "archiveIndex", "dataBindings", "allChecksPass",
            "claimBoundary", "continuumConclusion",
        },
        "primaryRowsExactOrderUniqueFiniteAndPassing": rows_valid,
        "primaryCountsAndArchiveIndexMatch": counts_valid,
        "cutoffComparisonsIndependentlyRecomputed": convergence_valid,
        "stepComparisonsInternallyRecomputedWithoutRawStepClaim": step_valid,
        "scalingSlopesIndependentlyRecomputed": slope_valid,
        "holdoutPredictionsIndependentlyRecomputed": holdout_valid,
        "outerMassGateIndependentlyRecomputed": outer_valid,
        "rawComplexNpzStructureFiniteAndEndpointsRecomputed": archive_valid,
        "primarySummaryDataBindingsMatch": data_bindings_valid,
        "primaryManifestBindingsMatch": manifest_bindings_valid,
        "independentPrimaryBindingsMatch": independent_bindings_valid,
        "progressLedgersComplete": (
            validate_progress(package / "progress.ndjson", smoke, source_commit, False)
            and validate_progress(package / "independent_progress.ndjson", smoke, source_commit, True)
        ),
        "primaryAndIndependentRunsPassed": summary["allChecksPass"] is True and manifest["allChecksPass"] is True and independent_valid,
        "finiteEvidenceBoundaryExplicit": (
            summary["diagnosticOnly"] is True
            and summary["claimBoundary"]["ordinaryCutoffAgreementIsTailProof"] is False
            and summary["claimBoundary"]["finiteTopEqualsContinuumTop"] is False
            and summary["claimBoundary"]["generalThreeDimensionalRegularityConclusion"] is False
        ),
    }
    observations = {
        "rowCount": len(rows),
        "cutoffComparisonCount": len(convergence),
        "stepComparisonCount": len(steps),
        "archiveMemberCount": len(summary["archiveIndex"]),
        "maximumNpzEndpointMetricRelativeError": archive_maximum,
        "quadraticNaturalLogSlope": quadratic_slope,
        "targetCubicNaturalLogSlope": cubic_slope,
        "holdout": observed,
        "finestOuterThreeMassMaximum": outer_maximum,
    }
    return checks, observations


def validate_seal(package: Path, smoke: bool) -> dict[str, bool]:
    manifest = load_json(package / "manifest.json")
    expected_names = set(PRE_SEAL_GENERATED)
    if not smoke:
        expected_names |= {Path(name).name for name in SOURCE_FILES}
    files_valid = verify_bindings(manifest.get("files"), package, expected_names)
    actual_regular = {
        path.name for path in package.iterdir()
        if path.is_file() and not path.is_symlink()
    }
    actual_symlinks = {path.name for path in package.iterdir() if path.is_symlink()}
    expected_all = expected_names | {"manifest.json", "SHA256SUMS"}
    checksum_lines = (package / "SHA256SUMS").read_text(encoding="ascii").splitlines()
    checksum_expected = [
        f"{sha256(package / name)}  {name}" for name in sorted(expected_names | {"manifest.json"})
    ]
    return {
        "sealManifestSchema": set(manifest) == {
            "schemaVersion", "release", "smokeMode", "sourceCommit", "inventory",
            "files", "allPrerequisiteChecksPass", "claimBoundary",
        },
        "sealManifestInventoryExact": (
            manifest.get("inventory") == {
                "sourceFileCount": 0 if smoke else 11,
                "generatedFileCount": 14,
                "manifestFileCount": len(expected_names),
                "sha256SumsLineCount": len(expected_names) + 1,
            }
            and files_valid
        ),
        "sealDirectoryHasExactRegularInventoryAndNoSymlinks": actual_regular == expected_all and not actual_symlinks,
        "sha256SumsExactSortedAndComplete": checksum_lines == checksum_expected,
        "sealPrerequisitesPassed": manifest.get("allPrerequisiteChecksPass") is True,
    }


def main() -> int:
    args = parse_args()
    package = args.package_dir.resolve()
    if args.smoke:
        if is_within(package, HERE):
            raise RuntimeError("smoke validation package must be outside the formal source tree")
    elif package != HERE.resolve():
        raise RuntimeError("formal validation must use research/certificates/r073h")
    output = args.output.resolve() if args.output else package / "validation.json"
    if output != package / "validation.json":
        raise RuntimeError("validation output must be package-dir/validation.json")
    if not args.verify_only:
        if output.exists() and not args.overwrite:
            raise RuntimeError("refusing to overwrite validation.json without --overwrite")
        if (package / "manifest.json").exists() or (package / "SHA256SUMS").exists():
            raise RuntimeError("refusing to create validation beneath a stale seal")
    provenance = source_gate(args.source_commit, args.smoke)
    required = PRE_CERTIFICATE_FILES + ("certificate.json",)
    for name in required:
        if not (package / name).is_file() or (package / name).is_symlink():
            raise RuntimeError(f"missing regular validation input: {name}")

    config = load_json(HERE / "config.json")
    exact = load_json(package / "exact_q2_certificate.json")
    independent_exact = load_json(package / "independent_exact_q2.json")
    summary = load_json(package / "primary_summary.json")
    primary_manifest = load_json(package / "primary_manifest.json")
    independent = load_json(package / "independent_validation.json")
    certificate = load_json(package / "certificate.json")
    exact_checks = validate_exact(exact, independent_exact)
    finite_checks, observations = validate_finite(
        package, config, summary, primary_manifest, independent,
        args.smoke, args.source_commit,
    )
    source_checks = {
        "validatorSourceGate": args.smoke or provenance["allSourceBlobsMatch"] is True,
        "exactPrimarySourceProvenance": provenance_matches(exact["sourceProvenance"], args.smoke, args.source_commit),
        "exactIndependentSourceProvenance": provenance_matches(independent_exact["sourceProvenance"], args.smoke, args.source_commit),
        "numericPrimarySourceProvenance": provenance_matches(summary["sourceProvenance"], args.smoke, args.source_commit),
        "numericIndependentSourceProvenance": provenance_matches(independent["sourceProvenance"], args.smoke, args.source_commit),
        "certificateSourceProvenance": provenance_matches(certificate["sourceProvenance"], args.smoke, args.source_commit),
    }
    config_binding = binding(HERE / "config.json", ROOT)
    certificate_checks = {
        "certificateTopLevelSchema": set(certificate) == {
            "schemaVersion", "release", "evidenceClass", "smokeMode", "sourceProvenance",
            "configBinding", "inputBindings", "exactContinuumSubcertificate",
            "finiteHarmonicDiagnostic", "preregistration", "checks", "allChecksPass",
            "claimLedger",
        },
        "certificateConfigBindingMatches": certificate.get("configBinding") == config_binding and summary.get("configBinding") == config_binding,
        "certificateInputBindingsMatch": verify_bindings(certificate.get("inputBindings"), package, set(PRE_CERTIFICATE_FILES)),
        "certificateModeAndSchemasMatch": (
            certificate.get("schemaVersion") == "r073h-combined-certificate-v1"
            and certificate.get("smokeMode") is args.smoke
            and certificate.get("allChecksPass") is True
        ),
        "certificateExactSectionMatchesRecomputation": (
            certificate.get("exactContinuumSubcertificate", {}).get("status") == "PASS_EXACT_SUBCERTIFICATE"
            and isinstance(certificate.get("exactContinuumSubcertificate", {}).get("checks"), dict)
            and all(certificate.get("exactContinuumSubcertificate", {}).get("checks", {}).values())
            and certificate.get("exactContinuumSubcertificate", {}).get("h0Lower") == "1/20"
            and certificate.get("exactContinuumSubcertificate", {}).get("hdLowerForDAtMostOneOver450") == "1/40"
            and certificate.get("exactContinuumSubcertificate", {}).get("twoRateStrictMargin") == "221/30000"
            and certificate.get("exactContinuumSubcertificate", {}).get("threeRateStrictMargin") == "221/20000"
            and certificate.get("exactContinuumSubcertificate", {}).get("finiteGalerkinPdeProof") is False
            and all(exact_checks.values())
        ),
        "certificateFiniteSectionMatchesRecomputation": (
            certificate.get("finiteHarmonicDiagnostic", {}).get("status") == "PASS_FINITE_DIAGNOSTIC"
            and isinstance(certificate.get("finiteHarmonicDiagnostic", {}).get("checks"), dict)
            and all(certificate.get("finiteHarmonicDiagnostic", {}).get("checks", {}).values())
            and certificate.get("finiteHarmonicDiagnostic", {}).get("continuumConclusion") == "none"
            and certificate.get("finiteHarmonicDiagnostic", {}).get("observations", {}).get("primaryRowCount") == observations["rowCount"]
            and certificate.get("finiteHarmonicDiagnostic", {}).get("observations", {}).get("cutoffComparisonCount") == observations["cutoffComparisonCount"]
            and certificate.get("finiteHarmonicDiagnostic", {}).get("observations", {}).get("stepComparisonCount") == observations["stepComparisonCount"]
            and close(
                float(certificate.get("finiteHarmonicDiagnostic", {}).get("observations", {}).get("quadraticNaturalLogSlope")),
                observations["quadraticNaturalLogSlope"],
            )
            and close(
                float(certificate.get("finiteHarmonicDiagnostic", {}).get("observations", {}).get("targetCubicNaturalLogSlope")),
                observations["targetCubicNaturalLogSlope"],
            )
            and all(finite_checks.values())
        ),
        "certificateOpenClaimsRemainOpen": (
            certificate.get("claimLedger", {}).get("fullContinuumHarmonicResolvedSemigroupEstimate") == "OPEN"
            and certificate.get("claimLedger", {}).get("fourthAndHigherAmplitudeOrders") == "OPEN"
            and certificate.get("claimLedger", {}).get("generalThreeDimensionalRegularity") == "OPEN"
            and certificate.get("claimLedger", {}).get("ClayProblem") == "OPEN"
        ),
    }
    checks = {
        **source_checks,
        **{f"exact::{key}": value for key, value in exact_checks.items()},
        **{f"finite::{key}": value for key, value in finite_checks.items()},
        **certificate_checks,
    }
    result = {
        "schemaVersion": "r073h-independent-package-validation-v1",
        "release": "R0.73H",
        "smokeMode": args.smoke,
        "sourceProvenance": provenance,
        "configBinding": config_binding,
        "packageBindings": [binding(package / name, package) for name in required],
        "recomputedObservations": observations,
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "evidenceBoundary": {
            "exactFiniteRationalBlockIsContinuumProofSubcertificateOnly": True,
            "npzEndpointsRecomputed": True,
            "stepRowsHaveNoArchivedRawEndpointsForIndependentRecomputation": True,
            "finiteCutoffAgreementIsNotTailProof": True,
            "generalThreeDimensionalRegularityConclusion": False,
            "Clay": False,
        },
    }
    if args.verify_only:
        recorded = load_json(output)
        recorded_checks = {
            "recordedValidationSchema": set(recorded) == set(result),
            "recordedValidationPassed": recorded.get("allChecksPass") is True,
            "recordedValidationMode": recorded.get("smokeMode") is args.smoke,
            "recordedValidationSourceCommit": recorded.get("sourceProvenance", {}).get("sourceCommit") == (None if args.smoke else args.source_commit),
            "recordedValidationBindings": verify_bindings(recorded.get("packageBindings"), package, set(required)),
            "recordedValidationChecksMatchFreshRecomputation": recorded.get("checks") == checks,
        }
        seal_checks = validate_seal(package, args.smoke)
        all_pass = result["allChecksPass"] and all(recorded_checks.values()) and all(seal_checks.values())
        print(canonical({
            "schemaVersion": "r073h-verify-only-v1",
            "allChecksPass": all_pass,
            "freshChecks": checks,
            "recordedValidationChecks": recorded_checks,
            "sealChecks": seal_checks,
        }), end="")
        return 0 if all_pass else 2
    temporary = output.with_name(f".{output.name}.tmp")
    temporary.write_text(canonical(result), encoding="utf-8")
    os.replace(temporary, output)
    return 0 if result["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
