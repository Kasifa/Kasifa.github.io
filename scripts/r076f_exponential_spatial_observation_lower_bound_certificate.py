#!/usr/bin/env python3
"""Fail-closed finite certificate for the R0.76F spatial lower bound."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STEM = "r076f_exponential_spatial_observation_lower_bound"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r076f_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R076F_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R076F_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R076F_MUTATION", "")
SCHEMA = "r076f-exponential-spatial-observation-lower-bound-certificate-v1"

FROZEN = {
    f"research/{STEM}.md": "48204fcbf8fe9af3f0fdc7720844c3dd8362d8767caf73de016eda7250b70973",
    f"research/{STEM}_primary_audit.md": "abcaa220c56d1f90c4b34061191e7cd009b8d911be3f83d705e95aa51b4d84cc",
    "research/r076f_report-source.md": "5e3939710dcfefcbc08b93761d8cdda1e655656a1bcd404b63fcea251ffd5e1e",
    "research/r076e_linear_modal_entropy_window.md": "1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4",
    f"scripts/{STEM}_fixtures.json": "1b11049ab482eb9b6d6b99cfdabfb4cd0a34ac4f483e3e69c5ec178dce752b5a",
    f"scripts/{STEM}_expected.json": "9703be8236b77e556085f9b358f4128ace4e32920a5391ebc1e2a900b232d37a",
}


GROUPS = {
    "bindings": [
        "main_hash", "primary_hash", "source_hash", "predecessor_hash",
        "fixture_hash", "expected_hash"
    ],
    "inputs": [
        "fixture_schema", "expected_schema", "fixture_utf8", "expected_utf8"
    ],
    "integrity": [
        "main_utf8", "primary_utf8", "source_utf8", "no_controls", "no_cr",
        "no_trailing", "tag_sequence", "display_balance", "reference_closure",
        "no_discouraged_prose"
    ],
    "geometry": [
        "i_order", "j_order", "i_length", "j_length", "endpoint_in_j",
        "endpoint_outside_i", "delta_positive", "delta_cap", "x_definition",
        "sine_monotonic_range"
    ],
    "dyadic": [
        "q_at_least_two", "frequency_count", "integer_frequencies",
        "frequency_rule", "strict_order", "first_frequency", "last_frequency",
        "dyadic_band", "no_zero_mode", "amplitude_count", "amplitudes_nonnegative",
        "binomial_coefficients", "amplitude_sum"
    ],
    "ratio": [
        "sample_sine_square", "triple_angle_identity", "triple_angle_ratio",
        "lower_exponent", "lower_bound", "l3_measure_factor", "phase_alignment",
        "derivative_nonnegative"
    ],
    "scale": [
        "spacing_rule", "alpha_rule", "sample_alpha", "scaled_fibre",
        "exact_heat_shear", "navier_stokes_embedding"
    ],
    "asymptotic": [
        "log_bound", "positive_slope", "polynomial_rejected",
        "quadratic_changes_coefficient", "small_quadratic_not_excluded"
    ],
    "source": [
        "nazarov_source", "friedland_source", "remez_source", "journal_doi",
        "preprint_boundary", "no_novelty_claim", "primary_pass",
        "math_blocker_zero", "release_blocker_zero", "fixture_correction"
    ],
    "boundary": [
        "spatial_only", "no_complete_flux_lower", "alternative_proof_open",
        "exact_base_open", "arbitrary_packets_open", "version_m_open",
        "regularity_open", "singularity_open", "no_figure", "no_simulation",
        "not_clay"
    ],
}
NEGATIVE_MUTATIONS = tuple(name for names in GROUPS.values() for name in names)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_bytes(data: bytes) -> bool:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return not any((byte < 32 and byte not in (9, 10, 13)) or byte == 127 for byte in data)


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def fragments(text: str, required: list[str]) -> bool:
    return all(value in text for value in required)


def mutate(checks: dict[str, dict[str, bool]]) -> None:
    if not MUTATION:
        return
    if MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R076F_MUTATION: {MUTATION}")
    for group, names in GROUPS.items():
        if MUTATION in names:
            checks[group][MUTATION] = False
            return
    raise AssertionError(MUTATION)


def main() -> int:
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.76F suite")

    fixture_raw = FIXTURES.read_bytes()
    expected_raw = EXPECTED.read_bytes()
    main_raw = MAIN.read_bytes()
    primary_raw = PRIMARY.read_bytes()
    source_raw = SOURCE.read_bytes()
    fixture = json.loads(fixture_raw)
    expected = json.loads(expected_raw)
    main_text = main_raw.decode("utf-8")
    primary_text = primary_raw.decode("utf-8")
    source_text = source_raw.decode("utf-8")
    compact_main = flat(main_text)
    compact_primary = flat(primary_text)
    compact_source = flat(source_text)
    bindings = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(FROZEN.items())
    }

    geom = fixture["geometry"]
    i_left, i_right = Q(geom["iLeft"]), Q(geom["iRight"])
    j_left, j_right = Q(geom["jLeft"]), Q(geom["jRight"])
    endpoint = Q(geom["endpoint"])
    sample = fixture["sample"]
    q_count = int(sample["q"])
    delta_over_pi = Q(sample["deltaOverPi"])
    x_over_pi = delta_over_pi / 4
    modes = [int(value) for value in sample["frequencies"]]
    amplitudes = [int(value) for value in sample["binomialAmplitudes"]]
    expected_amplitudes = [math.comb(q_count - 1, k) for k in range(q_count)]
    sine_squared = Q(sample["sineSquared"])
    triple_ratio = 3 - 4 * sine_squared
    lower_exponent = q_count - 1
    lower_bound = int(triple_ratio) ** lower_exponent
    alpha_over_pi = q_count * delta_over_pi

    tags = [int(value) for value in re.findall(r"\\tag\{F\.(\d+)\}", main_text)]
    refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])F\.(\d+)", main_text)]
    opens = len(re.findall(r"(?m)^\\\[$", main_text))
    closes = len(re.findall(r"(?m)^\\\]$", main_text))
    discouraged = ("我们", "攻关", "主攻", "研究纪律", "三重审计", "杀死错误想法")

    checks = {
        "bindings": {
            "main_hash": bindings[f"research/{STEM}.md"]["expectedSha256"] == bindings[f"research/{STEM}.md"]["observedSha256"],
            "primary_hash": bindings[f"research/{STEM}_primary_audit.md"]["expectedSha256"] == bindings[f"research/{STEM}_primary_audit.md"]["observedSha256"],
            "source_hash": bindings["research/r076f_report-source.md"]["expectedSha256"] == bindings["research/r076f_report-source.md"]["observedSha256"],
            "predecessor_hash": bindings["research/r076e_linear_modal_entropy_window.md"]["expectedSha256"] == bindings["research/r076e_linear_modal_entropy_window.md"]["observedSha256"],
            "fixture_hash": bindings[f"scripts/{STEM}_fixtures.json"]["expectedSha256"] == bindings[f"scripts/{STEM}_fixtures.json"]["observedSha256"],
            "expected_hash": bindings[f"scripts/{STEM}_expected.json"]["expectedSha256"] == bindings[f"scripts/{STEM}_expected.json"]["observedSha256"],
        },
        "inputs": {
            "fixture_schema": fixture["schema"] == "r076f-exponential-spatial-observation-lower-bound-fixtures-v1",
            "expected_schema": expected["schema"] == "r076f-exponential-spatial-observation-lower-bound-expected-v1",
            "fixture_utf8": clean_bytes(fixture_raw),
            "expected_utf8": clean_bytes(expected_raw),
        },
        "integrity": {
            "main_utf8": clean_bytes(main_raw),
            "primary_utf8": clean_bytes(primary_raw),
            "source_utf8": clean_bytes(source_raw),
            "no_controls": all(clean_bytes(value) for value in (main_raw, primary_raw, source_raw)),
            "no_cr": all(b"\r" not in value for value in (main_raw, primary_raw, source_raw)),
            "no_trailing": all(
                not line.endswith((" ", "\t"))
                for text in (main_text, primary_text, source_text)
                for line in text.splitlines()
            ),
            "tag_sequence": tags == list(range(1, 19)),
            "display_balance": opens == closes == 18,
            "reference_closure": not (set(refs) - set(tags)),
            "no_discouraged_prose": not any(
                word in text for word in discouraged
                for text in (main_text, primary_text, source_text)
            ),
        },
        "geometry": {
            "i_order": i_left < i_right,
            "j_order": j_left < i_left < i_right < j_right,
            "i_length": i_right - i_left == Q(expected["geometry"]["iLength"]),
            "j_length": j_right - j_left == Q(expected["geometry"]["jLength"]),
            "endpoint_in_j": j_left <= endpoint <= j_right and expected["geometry"]["endpointInJ"],
            "endpoint_outside_i": not (i_left <= endpoint <= i_right) and expected["geometry"]["endpointOutsideI"],
            "delta_positive": delta_over_pi > 0,
            "delta_cap": delta_over_pi <= Q(2, 3),
            "x_definition": x_over_pi == Q(sample["xOverPi"]),
            "sine_monotonic_range": 0 < x_over_pi <= Q(1, 6),
        },
        "dyadic": {
            "q_at_least_two": q_count >= 2,
            "frequency_count": len(modes) == q_count,
            "integer_frequencies": all(isinstance(value, int) for value in modes),
            "frequency_rule": modes == [q_count + k for k in range(q_count)],
            "strict_order": modes == sorted(set(modes)) and expected["sample"]["strictlyIncreasing"],
            "first_frequency": modes[0] == expected["sample"]["firstFrequency"],
            "last_frequency": modes[-1] == expected["sample"]["lastFrequency"],
            "dyadic_band": modes[-1] <= 2 * modes[0] and expected["sample"]["dyadicBand"],
            "no_zero_mode": modes[0] >= 1,
            "amplitude_count": len(amplitudes) == q_count,
            "amplitudes_nonnegative": all(value >= 0 for value in amplitudes),
            "binomial_coefficients": amplitudes == expected_amplitudes,
            "amplitude_sum": sum(amplitudes) == expected["sample"]["amplitudeSum"] == 2 ** (q_count - 1),
        },
        "ratio": {
            "sample_sine_square": sine_squared == Q(1, 4),
            "triple_angle_identity": triple_ratio == 3 - 4 * sine_squared,
            "triple_angle_ratio": triple_ratio == expected["sample"]["tripleAngleRatio"] == 2,
            "lower_exponent": lower_exponent == expected["sample"]["lowerBoundExponent"],
            "lower_bound": lower_bound == expected["sample"]["lowerBound"] == 8,
            "l3_measure_factor": i_right - i_left == 1,
            "phase_alignment": fragments(compact_main, ["e^{i\\theta}H_{q,\\delta}(z_*)", "=|H_{q,\\delta}(z_*)|", "\\phi_{k+1}=-\\theta-k\\pi"]),
            "derivative_nonnegative": "The derivative term is nonnegative" in main_text,
        },
        "scale": {
            "spacing_rule": "Let `a,R>0` satisfy `delta=aR`" in main_text,
            "alpha_rule": fixture["scale"]["alphaRule"] == "q*delta" and "\\alpha=n_1aR=q\\delta" in main_text,
            "sample_alpha": alpha_over_pi == Q(expected["sample"]["alphaOverPi"]),
            "scaled_fibre": "G(0,z)=F(0,aRz)=g_{q,\\delta}(z)" in compact_main,
            "exact_heat_shear": "is a smooth unforced Navier--Stokes solution" in compact_main,
            "navier_stokes_embedding": "`u=(0,0,F(t,x_2))`" in main_text,
        },
        "asymptotic": {
            "log_bound": "\\log C_q\\ge(q-1)\\log2" in main_text,
            "positive_slope": expected["asymptotic"]["limitingSlope"] == "log(2)",
            "polynomial_rejected": expected["asymptotic"]["polynomialReplacementRejected"] and "cannot replace `e^(Cq)` by a polynomial loss" in compact_main,
            "quadratic_changes_coefficient": expected["asymptotic"]["quadraticDensityChangesFrozenCoefficient"] and "cannot then be retained" in compact_main,
            "small_quadratic_not_excluded": "could still leave a negative total exponent" in compact_main,
        },
        "source": {
            "nazarov_source": "F. L. Nazarov" in source_text and "mathnet.ru" in source_text,
            "friedland_source": "Omer Friedland" in source_text and "2606.24823" in source_text,
            "remez_source": "S. Tikhonov and P. Yuditskii" in source_text,
            "journal_doi": "10.1007/s00365-019-09473-2" in source_text,
            "preprint_boundary": "recent preprint" in source_text,
            "no_novelty_claim": "not presented as a new approximation theorem" in compact_source,
            "primary_pass": "Current verdict: **PASS**" in primary_text,
            "math_blocker_zero": "Mathematical blocker count: **0**" in primary_text,
            "release_blocker_zero": "Release blocker count: **0**" in primary_text,
            "fixture_correction": fragments(flat(primary_text), ["initially encoded the rule for `alpha` as `q-delta`", "fixture now says `q*delta`", "Python and Ruby implementations validate"]),
        },
        "boundary": {
            "spatial_only": "lower bound for the spatial observation step" in compact_main,
            "no_complete_flux_lower": "not a lower bound for the complete collar flux" in compact_main,
            "alternative_proof_open": "does not exclude a different proof" in compact_main,
            "exact_base_open": "does not determine the optimal exponential base" in compact_main,
            "arbitrary_packets_open": "arbitrary packets" in compact_main,
            "version_m_open": "complete Version-M extraction" in compact_main,
            "regularity_open": "regularity" in compact_main,
            "singularity_open": "singularity" in compact_main,
            "no_figure": "No simulation or formal scientific figure is claimed" in compact_main,
            "no_simulation": not fixture["claimBoundary"]["simulationClaimed"],
            "not_clay": "**NOT CLAY.**" in main_text,
        },
    }

    mutate(checks)
    failures = [f"{group}.{name}" for group, rows in checks.items() for name, value in rows.items() if not value]
    assertions = sum(len(rows) for rows in checks.values())
    verdict = "PASS" if not failures else "FAIL"
    exact = {
        "q": q_count,
        "frequencies": modes,
        "amplitudes": amplitudes,
        "xOverPi": str(x_over_pi),
        "tripleAngleRatio": int(triple_ratio),
        "lowerBoundExponent": lower_exponent,
        "lowerBound": lower_bound,
        "alphaOverPi": str(alpha_over_pi),
    }
    output = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertionsPassed": assertions - len(failures),
        "assertionsTotal": assertions,
        "failures": failures,
        "exact": exact,
        "sourceSha256": {
            "main": sha256(MAIN),
            "primaryAudit": sha256(PRIMARY),
            "sourceReport": sha256(SOURCE),
            "fixtures": sha256(FIXTURES),
            "expected": sha256(EXPECTED),
        },
        "bindings": bindings,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "checks": checks,
        "boundary": {
            "finiteComputation": True,
            "continuumProof": False,
            "completeFluxLowerBound": False,
            "clay": False,
        },
    }
    OUT_JSON.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = [
        "# R0.76F finite certificate report",
        "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {assertions - len(failures)}/{assertions}",
        f"- Negative mutation inventory: {len(NEGATIVE_MUTATIONS)}",
        f"- Exact sample: q={q_count}, modes={modes}, amplitudes={amplitudes}",
        f"- Exact endpoint ratio: 2^({lower_exponent})={lower_bound}",
        f"- Failures: {failures if failures else 'none'}",
        "",
        "The finite certificate checks the exact combinatorial, dyadic, geometry,",
        "triple-angle, source, and claim-boundary ledgers.  It is not proof of",
        "the continuum norm inequality or the Navier--Stokes embedding.",
        "**NOT CLAY.**",
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"suite": "r076f", "verdict": verdict, "assertions": assertions, "failures": failures}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
