#!/usr/bin/env python3
"""R0.24 exact N=3 sharp-label audit on the minimal-leaf boundary face.

At leaf count L, every generated cube label satisfies m_2 >= -L.  The R0.22
sharp labels a_N, b_N, and a_N+b_N attain equality at their minimal leaf
counts.  Equality forces every contributing input leaf to have second cube
coordinate -1.  It also forces equality in both children of every root split.
Hence the graded faces m_2=-L form an exact closed recurrence for these
coefficients; no off-face Taylor history can contribute.

This script uses the quadratic-field cone recurrence from R0.23 with a GMP
rational backend.  It first reproduces the complete N=2 R0.23 coefficients
exactly, then computes the N=3 input orders 8 and 7 and output order 16.  It
also checks convergence of an independent finite-delta Leray recurrence.

The calculation supplies two finite data points.  It does not prove an all-N
asymptotic estimate, analytic closure, or a Navier--Stokes regularity theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time

import generated_subspace_sharpness_audit as base


Rational = base.Rational
Label = base.Label
Quadratic = base.Quadratic
ConeCoefficient = base.ConeCoefficient
Field = base.Field

MAXIMUM_ORDER = 16
R023_CERTIFICATE = Path(
    "research/certificates/r023/generated-subspace-sharpness.json"
)
CHECKPOINT_SCHEMA = 1


def progress(enabled: bool, started: float, message: str) -> None:
    if enabled:
        elapsed = time.perf_counter() - started
        print(f"[R0.24 +{elapsed:8.2f}s] {message}", file=sys.stderr, flush=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def serialize_coefficient(coefficient: ConeCoefficient) -> list[list[str]]:
    return [[str(component[0]), str(component[1])] for component in coefficient]


def deserialize_coefficient(payload: list[list[str]]) -> ConeCoefficient:
    if len(payload) != 4 or any(len(component) != 2 for component in payload):
        raise ValueError("invalid checkpoint coefficient")
    return tuple(
        (Rational(component[0]), Rational(component[1])) for component in payload
    )  # type: ignore[return-value]


def serialize_field(field: Field) -> list[dict[str, object]]:
    return [
        {
            "label": list(label),
            "coefficient": serialize_coefficient(field[label]),
        }
        for label in sorted(field)
    ]


def deserialize_field(payload: list[dict[str, object]]) -> Field:
    result: Field = {}
    for record in payload:
        label = tuple(int(value) for value in record["label"])
        if len(label) != 3:
            raise ValueError("invalid checkpoint label")
        coefficient = deserialize_coefficient(record["coefficient"])
        result[label] = coefficient  # type: ignore[index]
    return result


def checkpoint_path(directory: Path, order: int) -> Path:
    return directory / f"order-{order:02d}.json"


def atomic_json_write(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".tmp-{os.getpid()}")
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    with temporary.open("w", encoding="utf-8") as target:
        target.write(serialized)
        target.write("\n")
        target.flush()
        os.fsync(target.fileno())
    os.replace(temporary, path)


def checkpoint_record(
    order: int,
    field: Field,
    summary: dict[str, object],
    root_hash: str,
    radicand: Rational,
    source_commit: str,
) -> dict[str, object]:
    return {
        "schema": CHECKPOINT_SCHEMA,
        "timeOrder": order,
        "leafCount": order + 1,
        "rootCertificateSha256": root_hash,
        "radicand": str(radicand),
        "sourceCommit": source_commit,
        "summary": summary,
        "field": serialize_field(field),
    }


def load_checkpoint(
    path: Path,
    expected_order: int,
    root_hash: str,
    radicand: Rational,
    source_commit: str,
) -> tuple[Field, dict[str, object]]:
    payload = json.loads(path.read_text())
    if payload["schema"] != CHECKPOINT_SCHEMA:
        raise ValueError(f"unsupported checkpoint schema in {path}")
    if payload["timeOrder"] != expected_order:
        raise ValueError(f"checkpoint order mismatch in {path}")
    if payload["rootCertificateSha256"] != root_hash:
        raise ValueError(f"root certificate mismatch in {path}")
    if Rational(payload["radicand"]) != radicand:
        raise ValueError(f"quadratic radicand mismatch in {path}")
    if payload["sourceCommit"] != source_commit:
        raise ValueError(f"source commit mismatch in {path}")
    field = deserialize_field(payload["field"])
    validate_boundary_field(expected_order, field)
    return field, payload["summary"]


def validate_boundary_field(order: int, field: Field) -> None:
    leaf_count = order + 1
    for label, coefficient in field.items():
        if label[1] != -leaf_count:
            raise AssertionError(
                f"label {label} left the m_2=-{leaf_count} boundary face"
            )
        if base.radius(label) > leaf_count:
            raise AssertionError(f"label {label} exceeds its leaf radius")
        if base.constraint(label, coefficient) != base.ZERO_Q:
            raise AssertionError(f"constraint failed at boundary label {label}")


def boundary_initial_field(
    center: dict[str, Rational],
    radicand: Rational,
) -> Field:
    field = {
        label: coefficient
        for label, coefficient in base.initial_field(center, radicand).items()
        if label[1] == -1
    }
    if set(field) != {
        (1, -1, 1),
        (1, -1, -1),
        (-1, -1, -1),
        (-1, -1, 1),
    }:
        raise AssertionError("unexpected minimal-face input generators")
    validate_boundary_field(0, field)
    return field


def boundary_taylor(
    initial: Field,
    radicand: Rational,
    maximum_order: int,
    root_hash: str,
    source_commit: str,
    checkpoint_directory: Path | None,
    show_progress: bool,
    started: float,
) -> tuple[list[Field], list[dict[str, object]], int]:
    coefficients: list[Field] = []
    summaries: list[dict[str, object]] = []
    resumed_through = -1

    if checkpoint_directory is not None:
        for order in range(maximum_order + 1):
            path = checkpoint_path(checkpoint_directory, order)
            if not path.exists():
                break
            field, summary = load_checkpoint(
                path, order, root_hash, radicand, source_commit
            )
            coefficients.append(field)
            summaries.append(summary)
            resumed_through = order
        if coefficients:
            if coefficients[0] != initial:
                raise AssertionError("checkpoint initial field does not match")
            progress(
                show_progress,
                started,
                f"resumed exact boundary fields through order {resumed_through}",
            )

    if not coefficients:
        coefficients = [initial]
        summaries = [
            {
                "timeOrder": 0,
                "leafCount": 1,
                "supportSize": len(initial),
                "faceCapacity": 4,
                "orderedInteractions": 0,
                "stageSeconds": 0.0,
            }
        ]
        if checkpoint_directory is not None:
            atomic_json_write(
                checkpoint_path(checkpoint_directory, 0),
                checkpoint_record(
                    0,
                    initial,
                    summaries[0],
                    root_hash,
                    radicand,
                    source_commit,
                ),
            )

    for next_order in range(len(coefficients), maximum_order + 1):
        stage_started = time.perf_counter()
        output: Field = {}
        interaction_count = 0
        for left_order in range(next_order):
            right_order = next_order - 1 - left_order
            for left_label, left in coefficients[left_order].items():
                for right_label, right in coefficients[right_order].items():
                    interaction_count += 1
                    output_label, value = base.cone_bilinear(
                        left_label,
                        left,
                        right_label,
                        right,
                        radicand,
                    )
                    base.field_add(
                        output,
                        output_label,
                        base.coefficient_scale(Rational(-1, next_order), value),
                    )
        validate_boundary_field(next_order, output)
        face_capacity = (next_order + 2) ** 2
        if len(output) > face_capacity:
            raise AssertionError(
                f"order {next_order} has {len(output)} boundary labels, "
                f"exceeding face capacity {face_capacity}"
            )
        summary = {
            "timeOrder": next_order,
            "leafCount": next_order + 1,
            "supportSize": len(output),
            "faceCapacity": face_capacity,
            "orderedInteractions": interaction_count,
            "stageSeconds": time.perf_counter() - stage_started,
        }
        coefficients.append(output)
        summaries.append(summary)
        if checkpoint_directory is not None:
            atomic_json_write(
                checkpoint_path(checkpoint_directory, next_order),
                checkpoint_record(
                    next_order,
                    output,
                    summary,
                    root_hash,
                    radicand,
                    source_commit,
                ),
            )
        progress(
            show_progress,
            started,
            f"order {next_order:2d}: face support {len(output):3d}, "
            f"ordered interactions {interaction_count:6d}, "
            f"stage {summary['stageSeconds']:.2f}s",
        )
    return coefficients, summaries, resumed_through


def certificate_coefficient(record: dict[str, object]) -> ConeCoefficient:
    return tuple(
        (Rational(component["basis"][0]), Rational(component["basis"][1]))
        for component in record["coefficient"]
    )  # type: ignore[return-value]


def r023_regression(coefficients: list[Field]) -> dict[str, object]:
    payload = json.loads(R023_CERTIFICATE.read_text())
    encounter = payload["sharpFamilyFirstEncounter"]
    specifications = (
        ("left", (2, -6, 4), 5),
        ("right", (-1, -5, -5), 4),
        ("fullOutput", (1, -11, -1), 10),
    )
    records = []
    for name, label, order in specifications:
        expected = certificate_coefficient(encounter[name])
        actual = coefficients[order].get(label)
        records.append(
            {
                "name": name,
                "label": list(label),
                "timeOrder": order,
                "exactBasisMatch": actual == expected,
            }
        )
    return {
        "certificate": str(R023_CERTIFICATE),
        "certificateSha256": sha256(R023_CERTIFICATE),
        "records": records,
        "allExactBasisMatches": all(record["exactBasisMatch"] for record in records),
    }


def mode_norm(coefficient: ConeCoefficient, radicand: Rational) -> float:
    return base.coefficient_mode_norm(coefficient, radicand)


def transverse_norm(coefficient: ConeCoefficient, radicand: Rational) -> float:
    values = [base.q_float(component, radicand) for component in coefficient[:3]]
    return math.sqrt(sum(value * value for value in values))


def parameter_analysis(
    parameter: int,
    coefficients: list[Field],
    radicand: Rational,
) -> dict[str, object]:
    left_label, right_label, output_label = base.sharp_labels(parameter)
    left_order = base.radius(left_label) - 1
    right_order = base.radius(right_label) - 1
    output_order = base.radius(output_label) - 1
    left = coefficients[left_order][left_label]
    right = coefficients[right_order][right_label]
    full_output = coefficients[output_order][output_label]

    _, left_right = base.cone_bilinear(
        left_label, left, right_label, right, radicand
    )
    _, right_left = base.cone_bilinear(
        right_label, right, left_label, left, radicand
    )
    symmetrized = base.coefficient_add(left_right, right_left)
    root_contribution = base.coefficient_scale(
        Rational(-1, output_order), symmetrized
    )
    generated_gain = mode_norm(symmetrized, radicand) / (
        mode_norm(left, radicand) * mode_norm(right, radicand)
    )
    sharp_gain = base.sharp_benchmark(left_label, right_label)

    root_values = [base.q_float(value, radicand) for value in root_contribution[:3]]
    full_values = [base.q_float(value, radicand) for value in full_output[:3]]
    root_squared = sum(value * value for value in root_values)
    full_squared = sum(value * value for value in full_values)
    root_full_dot = sum(
        root_values[index] * full_values[index] for index in range(3)
    )

    return {
        "parameter": parameter,
        "orders": {
            "left": left_order,
            "right": right_order,
            "output": output_order,
        },
        "left": base.coefficient_record(left_label, left, radicand),
        "right": base.coefficient_record(right_label, right, radicand),
        "fullOutput": base.coefficient_record(output_label, full_output, radicand),
        "symmetrizedRootOperatorOutput": base.coefficient_record(
            output_label, symmetrized, radicand
        ),
        "timeTaylorRootContribution": base.coefficient_record(
            output_label, root_contribution, radicand
        ),
        "comparison": {
            "generatedSymmetrizedOperatorGain": generated_gain,
            "generatedGainOverRadiusProduct": generated_gain
            / (base.radius(left_label) * base.radius(right_label)),
            "R022SharpPolarizationGain": sharp_gain,
            "generatedToSharpGainRatio": generated_gain / sharp_gain,
            "rootContributionToFullOutputModeNorm": mode_norm(
                root_contribution, radicand
            )
            / mode_norm(full_output, radicand),
            "rootContributionToFullOutputTransverseNorm": math.sqrt(
                root_squared / full_squared
            ),
            "squaredCosineRootContributionVsFullOutput": root_full_dot
            * root_full_dot
            / (root_squared * full_squared),
            "leftLongitudinalToTransverseRatio": abs(
                base.q_float(left[3], radicand)
            )
            / transverse_norm(left, radicand),
            "rightLongitudinalToTransverseRatio": abs(
                base.q_float(right[3], radicand)
            )
            / transverse_norm(right, radicand),
        },
    }


def finite_boundary_taylor(
    center: dict[str, Rational],
    delta: float,
    maximum_order: int,
) -> list[dict[Label, tuple[float, float, float]]]:
    initial = {
        label: coefficient
        for label, coefficient in base.finite_initial_field(center, delta).items()
        if label[1] == -1
    }
    coefficients = [initial]
    for next_order in range(1, maximum_order + 1):
        output: dict[Label, tuple[float, float, float]] = {}
        for left_order in range(next_order):
            right_order = next_order - 1 - left_order
            for left_label, left in coefficients[left_order].items():
                for right_label, right in coefficients[right_order].items():
                    output_label, value = base.finite_bilinear(
                        left_label, left, right_label, right, delta
                    )
                    old = output.get(output_label, (0.0, 0.0, 0.0))
                    output[output_label] = tuple(
                        old[index] - value[index] / next_order for index in range(3)
                    )
        coefficients.append(output)
    return coefficients


def finite_boundary_convergence(
    center: dict[str, Rational],
    radicand: Rational,
    analysis: dict[str, object],
    levels: tuple[int, ...] = (3, 5, 7),
) -> list[dict[str, object]]:
    pump_scale = 1.0 / math.sqrt(
        6.0 * (1.0 + float(center["p"]) ** 2 / 12.0)
    )
    targets = []
    for name in ("left", "right", "fullOutput"):
        record = analysis[name]
        targets.append(
            (
                name,
                tuple(record["label"]),
                analysis["orders"]["output" if name == "fullOutput" else name],
                certificate_coefficient(record),
            )
        )

    records = []
    for level in levels:
        delta = 4.0 ** (-level)
        coefficients = finite_boundary_taylor(center, delta, MAXIMUM_ORDER)
        target_records = []
        for name, label, order, cone_value in targets:
            finite_value = coefficients[order][label]
            scaled = tuple(
                component / pump_scale ** (order + 1) for component in finite_value
            )
            cone_transverse = tuple(
                base.q_float(component, radicand) for component in cone_value[:3]
            )
            cone_longitudinal = base.q_float(cone_value[3], radicand)
            transverse_error = math.sqrt(
                sum(
                    (scaled[index] - cone_transverse[index]) ** 2
                    for index in range(3)
                )
            ) / math.sqrt(sum(value * value for value in cone_transverse))
            finite_longitudinal = sum(scaled) / delta
            longitudinal_error = abs(
                finite_longitudinal - cone_longitudinal
            ) / abs(cone_longitudinal)
            target_records.append(
                {
                    "name": name,
                    "label": list(label),
                    "timeOrder": order,
                    "relativeTransverseError": transverse_error,
                    "relativeLongitudinalError": longitudinal_error,
                }
            )
        records.append({"level": level, "delta": delta, "targets": target_records})
    return records


def trend_record(
    second: dict[str, object],
    third: dict[str, object],
) -> dict[str, object]:
    second_values = second["comparison"]
    third_values = third["comparison"]

    def ratio(key: str) -> float:
        return third_values[key] / second_values[key]

    return {
        "generatedGainN3OverN2": ratio("generatedSymmetrizedOperatorGain"),
        "sharpBenchmarkN3OverN2": ratio("R022SharpPolarizationGain"),
        "generatedToSharpRatioN3OverN2": ratio("generatedToSharpGainRatio"),
        "radiusNormalizedGainN3OverN2": ratio("generatedGainOverRadiusProduct"),
        "rootModeShareN3OverN2": ratio("rootContributionToFullOutputModeNorm"),
        "observedInterpretation": (
            "from N=2 to N=3 the generated gain remains order one while the "
            "sharp benchmark grows; the evidence favors suppression, but two "
            "finite points do not prove an all-N bound"
        ),
    }


def audit(
    checkpoint_directory: Path | None,
    show_progress: bool,
) -> dict[str, object]:
    started = time.perf_counter()
    if not base.RATIONAL_BACKEND.startswith("gmpy2.mpq"):
        raise RuntimeError(
            "R0.24 requires gmpy2; install requirements-research.txt before running"
        )
    center, root_radius, root_hash = base.load_root_center()
    pump_norm_squared = Rational(1) + center["p"] * center["p"] / 12
    catalyst_norm_squared = Rational(1) + center["q"] * center["q"] / 3
    radicand = center["x"] * pump_norm_squared / (4 * catalyst_norm_squared)
    source_state = base.git_source_state()
    progress(show_progress, started, f"using {base.RATIONAL_BACKEND}")

    initial = boundary_initial_field(center, radicand)
    coefficients, summaries, resumed_through = boundary_taylor(
        initial,
        radicand,
        MAXIMUM_ORDER,
        root_hash,
        source_state["commit"],
        checkpoint_directory,
        show_progress,
        started,
    )
    regression = r023_regression(coefficients)
    if not regression["allExactBasisMatches"]:
        raise AssertionError("the boundary recurrence failed the R0.23 regression")
    progress(show_progress, started, "matched all three R0.23 N=2 coefficients exactly")

    second = parameter_analysis(2, coefficients, radicand)
    third = parameter_analysis(3, coefficients, radicand)
    finite_convergence = finite_boundary_convergence(center, radicand, third)
    progress(show_progress, started, "finished finite-shell levels 3, 5, and 7")

    return {
        "scope": {
            "result": "exact N=3 generated sharp-label audit on the minimal-leaf boundary face",
            "proved": [
                "the m_2=-L faces form a closed graded recurrence for minimal-leaf targets",
                "the restricted recurrence reproduces all three R0.23 N=2 coefficients exactly",
                "the N=3 sharp-direction projections and symmetrized root interaction are exactly nonzero",
            ],
            "notClaimed": [
                "an all-N asymptotic estimate",
                "uniformity throughout the R0.20 root box",
                "one-radius analytic closure",
                "a Navier--Stokes regularity or singularity result",
            ],
        },
        "boundarySelection": {
            "face": "at leaf count L, m_2=-L",
            "inputGenerators": [list(label) for label in sorted(initial)],
            "proof": (
                "each leaf has second coordinate at least -1; equality at total "
                "leaf count L forces every leaf, and both children of every "
                "split, to attain their lower bounds"
            ),
            "fullSupportScale": "(L+1)^3",
            "restrictedSupportScale": "(L+1)^2",
        },
        "root": {
            "center": {key: str(value) for key, value in center.items()},
            "boxRadius": str(root_radius),
            "certificate": str(base.ROOT_CERTIFICATE),
            "certificateSha256": root_hash,
        },
        "quadraticField": {
            "radicand": str(radicand),
            "generatorDecimal": math.sqrt(float(radicand)),
            "radicandIsRationalSquare": base.rational_is_square(radicand),
        },
        "recurrence": {
            "equation": "(k+1) U_(k+1) = -sum_(j=0)^k B(U_j,U_(k-j))",
            "maximumTimeOrder": MAXIMUM_ORDER,
            "support": summaries,
            "checkpointDirectory": (
                str(checkpoint_directory) if checkpoint_directory is not None else None
            ),
            "resumedThroughOrder": resumed_through,
        },
        "r023Regression": regression,
        "parameterAudits": {"N2": second, "N3": third},
        "trend": trend_record(second, third),
        "finiteShellConvergenceN3": finite_convergence,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "arithmetic": base.RATIONAL_BACKEND,
        },
        "git": source_state,
        "wallSeconds": time.perf_counter() - started,
    }


def validate(result: dict[str, object]) -> None:
    assert result["r023Regression"]["allExactBasisMatches"] is True
    support = result["recurrence"]["support"]
    assert support[-1]["timeOrder"] == 16
    assert support[-1]["supportSize"] == 320
    assert support[-1]["orderedInteractions"] == 68576
    assert result["quadraticField"]["radicandIsRationalSquare"] is False

    third = result["parameterAudits"]["N3"]
    assert third["orders"] == {"left": 8, "right": 7, "output": 16}
    for name in ("left", "right"):
        assert third[name]["constraint"]["isExactlyZero"] is True
        assert third[name]["sharpProjectionIsNonzero"] is True
        assert third[name]["longitudinalJetIsNonzero"] is True
    assert (
        third["symmetrizedRootOperatorOutput"]["coefficient"][0]["isExactlyZero"]
        is False
    )
    comparison = third["comparison"]
    assert 0.36 < comparison["generatedSymmetrizedOperatorGain"] < 0.37
    assert 0.0019 < comparison["generatedToSharpGainRatio"] < 0.0021
    assert 7.0e-7 < comparison["rootContributionToFullOutputModeNorm"] < 8.5e-7

    trend = result["trend"]
    assert 1.1 < trend["generatedGainN3OverN2"] < 1.3
    assert trend["generatedToSharpRatioN3OverN2"] < 0.5
    assert trend["radiusNormalizedGainN3OverN2"] < 0.51
    assert trend["rootModeShareN3OverN2"] < 0.002

    final_convergence = result["finiteShellConvergenceN3"][-1]
    for target in final_convergence["targets"]:
        assert target["relativeTransverseError"] < 0.003
        assert target["relativeLongitudinalError"] < 0.00002


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--checkpoint-dir", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    result = audit(arguments.checkpoint_dir, arguments.progress)
    if arguments.check:
        validate(result)
    serialized = json.dumps(
        result,
        ensure_ascii=False,
        indent=2 if arguments.pretty else None,
        sort_keys=True,
    )
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(serialized + "\n")
    print(serialized)


if __name__ == "__main__":
    main()
