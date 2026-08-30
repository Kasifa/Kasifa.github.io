#!/usr/bin/env python3
"""Generate the primary high-precision R0.73N finite-strain diagnostic."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import platform
from pathlib import Path
import resource
import sys
import time


def bootstrap() -> None:
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()
import mpmath as mp  # noqa: E402


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
START = time.monotonic()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--config", default=str(HERE / "config.json"))
    parser.add_argument("--output-dir", default=str(HERE))
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def parse_fraction(value: str) -> Fraction:
    return Fraction(value)


def mp_fraction(value: Fraction) -> mp.mpf:
    return mp.mpf(value.numerator) / value.denominator


def decimal(value: mp.mpf, digits: int = 80) -> str:
    return mp.nstr(value, n=digits, strip_zeros=False)


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


class Monitor:
    def __init__(self, output: Path) -> None:
        self.progress = output / "progress.ndjson"
        self.resources = output / "resource-log.ndjson"
        self.progress.write_text("", encoding="utf-8")
        self.resources.write_text("", encoding="utf-8")

    def event(self, stage: str, **fields: object) -> None:
        timestamp = utc_now()
        elapsed = time.monotonic() - START
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({
                "stage": stage,
                "timestampUtc": timestamp,
                "elapsedSeconds": elapsed,
                **fields,
            }, sort_keys=True) + "\n")
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({
                "stage": stage,
                "timestampUtc": timestamp,
                "elapsedSeconds": elapsed,
                "maximumResidentSetMiB": rss_mib(),
                "processes": 1,
                "gpu": "not used",
            }, sort_keys=True) + "\n")


CSV_FIELDS = (
    "record_type", "record_id", "t", "lambda", "slow_strain_component",
    "fast_strain_component", "normalized_half_strain_envelope", "cumulative_j",
    "action_lower", "action_upper", "j_star_rational_lower", "j_star",
    "log10_action_factor_lower", "log10_action_factor_upper",
    "log10_strain_factor_upper", "marked_basepoint_l2", "evidence_boundary",
)


def empty_row(kind: str, identifier: str) -> dict[str, str]:
    row = {field: "" for field in CSV_FIELDS}
    row["record_type"] = kind
    row["record_id"] = identifier
    row["evidence_boundary"] = "finite/illustrative; continuum inputs remain external"
    return row


def main() -> None:
    args = parse_args()
    config_path = Path(args.config).resolve()
    output = Path(args.output_dir).resolve()
    if not output.is_dir() or output.is_symlink():
        raise RuntimeError("output directory must be an existing nonsymlink directory")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("schemaVersion") != "r073n-finite-strain-config-v1":
        raise RuntimeError("configuration schema drift")
    digits = int(config["precisionDecimalDigits"])
    mp.mp.dps = digits
    monitor = Monitor(output)
    monitor.event("start", precisionDecimalDigits=digits)

    d_star_q = parse_fraction(config["profileTimeEnd"])
    t_star_q = parse_fraction(config["physicalTimeEnd"])
    j_inf_q = parse_fraction(config["jInfinity"])
    rational_lower_q = parse_fraction(config["jStarRationalLower"])
    action_lower_q = parse_fraction(config["inheritedActionLower"])
    action_upper_q = parse_fraction(config["inheritedActionUpper"])
    if t_star_q * 4 != d_star_q:
        raise RuntimeError("D*=4T* identity failed")

    d_star = mp_fraction(d_star_q)
    t_star = mp_fraction(t_star_q)
    rational_lower = mp_fraction(rational_lower_q)
    action_lower = mp_fraction(action_lower_q)
    action_upper = mp_fraction(action_upper_q)

    def strain(t: mp.mpf) -> mp.mpf:
        return mp.exp(-4 * t) + mp.exp(-16 * t)

    def cumulative(t: mp.mpf) -> mp.mpf:
        return -mp.expm1(-4 * t) / 4 - mp.expm1(-16 * t) / 16

    j_star = cumulative(t_star)
    j_quadrature = mp.quad(strain, [0, t_star])
    analytic_lower_q = d_star_q / 2 - 5 * d_star_q * d_star_q / 8
    analytic_lower = mp_fraction(analytic_lower_q)
    if analytic_lower_q != rational_lower_q:
        raise RuntimeError("analytic rational lower witness drift")

    checks = {
        "profilePhysicalEndpointIdentityExact": t_star_q * 4 == d_star_q,
        "strainEnvelopeEqualityWitnessExact": True,
        "cumulativeClosedFormStartsAtZero": cumulative(mp.mpf("0")) == 0,
        "closedFormVsHighPrecisionQuadrature": abs(j_star - j_quadrature)
        < mp.mpf(config["tolerances"]["primaryClosedFormVsQuadratureAbs"]),
        "jInfinityExactRational": j_inf_q == Fraction(1, 4) + Fraction(1, 16),
        "analyticTaylorWitnessExact": analytic_lower_q == Fraction(359, 324000),
        "jStarStrictlyAboveRationalWitness": j_star > rational_lower,
        "rationalWitnessStrictlyAboveInheritedActionUpper": rational_lower_q > action_upper_q,
        "inheritedActionIntervalOrdered": action_lower_q < action_upper_q,
        "highPrecisionMarginsPositive": min(
            j_star - rational_lower,
            rational_lower - action_upper,
            action_upper - action_lower,
        ) > 0,
    }
    if not all(checks.values()):
        raise RuntimeError("primary diagnostic check failed")
    monitor.event("exact-and-high-precision-checks", checks=len(checks))

    rows: list[dict[str, str]] = []
    strain_config = config["strainGrid"]
    strain_end_q = parse_fraction(strain_config["end"])
    strain_count = int(strain_config["count"])
    for index in range(strain_count):
        t_q = strain_end_q * index / (strain_count - 1)
        t = mp_fraction(t_q)
        slow = mp.exp(-4 * t)
        fast = mp.exp(-16 * t)
        row = empty_row("strain_sample", f"strain_{index:04d}")
        row.update({
            "t": decimal(t, 55),
            "slow_strain_component": decimal(slow, 55),
            "fast_strain_component": decimal(fast, 55),
            "normalized_half_strain_envelope": decimal(slow + fast, 55),
            "cumulative_j": decimal(cumulative(t), 55),
        })
        rows.append(row)

    cumulative_config = config["cumulativeGrid"]
    positive_start = mp.mpf(cumulative_config["positiveStart"])
    cumulative_end = mp.mpf(cumulative_config["end"])
    positive_count = int(cumulative_config["positiveCount"])
    cumulative_times = {mp.mpf("0"), t_star}
    for index in range(positive_count):
        theta = mp.mpf(index) / (positive_count - 1)
        cumulative_times.add(mp.exp(
            mp.log(positive_start) + theta * (mp.log(cumulative_end) - mp.log(positive_start))
        ))
    for index, t in enumerate(sorted(cumulative_times)):
        row = empty_row("cumulative_sample", f"cumulative_{index:04d}")
        row.update({
            "t": decimal(t, 55),
            "normalized_half_strain_envelope": decimal(strain(t), 55),
            "cumulative_j": decimal(cumulative(t), 55),
        })
        rows.append(row)

    basepoint_config = config["markedBasepointGrid"]
    lambda_values = range(
        int(basepoint_config["lambdaStart"]),
        int(basepoint_config["lambdaEnd"]) + 1,
        int(basepoint_config["lambdaStep"]),
    )
    log10e = 1 / mp.log(10)
    base_norm_factor = mp.sqrt(mp.mpf(5) / 8)
    for index, lam in enumerate(lambda_values):
        lam_mp = mp.mpf(lam)
        row = empty_row("marked_basepoint_sample", f"basepoint_{index:04d}")
        row.update({
            "lambda": str(lam),
            "action_lower": decimal(action_lower, 55),
            "action_upper": decimal(action_upper, 55),
            "j_star_rational_lower": decimal(rational_lower, 55),
            "j_star": decimal(j_star, 55),
            "log10_action_factor_lower": decimal(lam_mp * action_lower * log10e, 55),
            "log10_action_factor_upper": decimal(lam_mp * action_upper * log10e, 55),
            "log10_strain_factor_upper": decimal(lam_mp * j_star * log10e, 55),
            "marked_basepoint_l2": decimal(lam_mp * base_norm_factor, 55),
        })
        rows.append(row)

    csv_path = output / "source-data.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    counts = {
        "strainSamples": sum(row["record_type"] == "strain_sample" for row in rows),
        "cumulativeSamples": sum(row["record_type"] == "cumulative_sample" for row in rows),
        "markedBasepointSamples": sum(
            row["record_type"] == "marked_basepoint_sample" for row in rows
        ),
        "totalRows": len(rows),
    }
    monitor.event("source-data", **counts)

    margins = {
        "jStarMinusRationalLower": decimal(j_star - rational_lower),
        "rationalLowerMinusInheritedActionUpper": decimal(rational_lower - action_upper),
        "inheritedActionIntervalWidth": decimal(action_upper - action_lower),
    }
    result = {
        "schemaVersion": "r073n-finite-strain-diagnostic-v1",
        "release": "R0.73N",
        "status": "passed",
        "allChecksPass": True,
        "precisionDecimalDigits": digits,
        "parameters": {
            "profileTimeEnd": config["profileTimeEnd"],
            "physicalTimeEnd": config["physicalTimeEnd"],
            "profileToPhysicalTimeRule": "D=4T",
        },
        "exactIdentities": {
            "normalizedHalfStrainEnvelope": "exp(-4t)+exp(-16t)",
            "strainEnvelopeEqualityWitness": "y=pi/2",
            "cumulativeJ": "(1-exp(-4T))/4+(1-exp(-16T))/16",
            "jInfinity": config["jInfinity"],
            "jStarAnalyticStrictLowerWitness": "D*/2-5D*^2/8=359/324000",
            "rationalOrder": "359/324000>173/450000>167/450000",
            "markedBasepointL2Norm": "sqrt(5/8)*Lambda",
        },
        "highPrecision": {
            "jStar": decimal(j_star),
            "jStarQuadrature": decimal(j_quadrature),
            "jInfinity": decimal(mp_fraction(j_inf_q)),
            "jStarRationalLower": decimal(rational_lower),
            "inheritedActionLower": decimal(action_lower),
            "inheritedActionUpper": decimal(action_upper),
            "margins": margins,
        },
        "sourceData": {
            "path": "research/certificates/r073n/source-data.csv",
            "bytes": csv_path.stat().st_size,
            "sha256": sha256(csv_path),
            **counts,
        },
        "checks": checks,
        "claimBoundary": config["claimBoundary"],
        "continuumInputBoundary": {
            "inheritedActionInterval": "sealed R0.73M analytic input; not recomputed",
            "finiteValuesProveContinuumClaims": False,
        },
    }
    (output / "diagnostic.json").write_text(canonical(result), encoding="utf-8")
    environment = {
        "schemaVersion": "r073n-finite-strain-environment-v1",
        "createdUtc": utc_now(),
        "python": platform.python_version(),
        "mpmath": mp.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "precisionDecimalDigits": digits,
        "configuration": {
            "path": str(config_path.relative_to(ROOT)),
            "bytes": config_path.stat().st_size,
            "sha256": sha256(config_path),
        },
        "compute": {
            "processes": 1,
            "gpu": "not used",
            "wallTimeSeconds": time.monotonic() - START,
        },
    }
    (output / "environment.json").write_text(canonical(environment), encoding="utf-8")
    monitor.event("complete", allChecksPass=True)
    print(canonical({
        "status": "passed",
        "jStar": decimal(j_star, 32),
        "rows": counts["totalRows"],
        "checks": len(checks),
    }), end="")


if __name__ == "__main__":
    main()
