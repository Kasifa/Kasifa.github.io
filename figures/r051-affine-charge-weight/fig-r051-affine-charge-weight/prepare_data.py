#!/usr/bin/env python3
"""Prepare R0.51 journal-figure tables from pinned exact certificates."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

import gmpy2
import mpmath


Q = gmpy2.mpq
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESEARCH = ROOT / "research"
sys.path.insert(0, str(RESEARCH))

import edge_affine_charge_weight_audit as r051  # noqa: E402
import edge_charge_degree_lattice_audit as r047  # noqa: E402
import edge_rational_asymptotic_audit as r028  # noqa: E402
import edge_short_continuation_audit as r036  # noqa: E402
import edge_weighted_restart_audit as r037  # noqa: E402


CERTIFICATES = {
    "r048": RESEARCH / "certificates/r048/edge-charge-threshold-root.json",
    "r049": RESEARCH / "certificates/r049/edge-charge-character-weight.json",
    "r050": RESEARCH
    / "certificates/r050/edge-charge-character-optimization.json",
    "r051": RESEARCH / "certificates/r051/edge-affine-charge-weight.json",
}
EXPECTED_SHA256 = {
    "r048": "246bcfa6623b1050511554312c32e9973b42b620a20ff571a1b5f340041c9af0",
    "r049": "e36fce33f8a5edeb144cdbeda00a568b972d9a3a8ac0e96c04d7651e71a64578",
    "r050": "fc173a2108ef881d21d9d54046085f0d5daf5cc33ed50e024ca32ec867f7b79a",
    "r051": "db72d40ee304d1a6ce5dd96d9f5971e78037675e79c837e409c5691bb8aa582f",
}


def progress(started: float, stage: str, **details: object) -> None:
    suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
    print(
        f"[R0.51 figure +{time.perf_counter() - started:7.2f}s] {stage}{suffix}",
        file=sys.stderr,
        flush=True,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decimal(value: Q, digits: int = 32) -> str:
    return mpmath.nstr(
        mpmath.mpf(int(value.numerator)) / int(value.denominator),
        digits,
    )


def write_csv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, object]],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=fieldnames,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def load_certificates() -> dict[str, dict[str, object]]:
    result = {}
    for key, path in CERTIFICATES.items():
        if sha256(path) != EXPECTED_SHA256[key]:
            raise SystemExit(f"{key} certificate hash mismatch")
        result[key] = json.loads(path.read_text(encoding="utf-8"))
    return result


def root_bounds(
    certificate: dict[str, object],
    key: str,
) -> tuple[Q, Q]:
    if key == "r050":
        theorem = certificate["globalOptimizationTheorem"]
        return (
            Q(theorem["optimalRadiusLower"]["exact"]),
            Q(theorem["optimalRadiusUpper"]["exact"]),
        )
    theorem = certificate["thresholdTheorem"]["rootIsolation"]
    return Q(theorem["lower"]["exact"]), Q(theorem["upper"]["exact"])


def main() -> None:
    started = time.perf_counter()
    mpmath.mp.dps = 80
    certificates = load_certificates()
    r051_certificate = certificates["r051"]
    if len(r051_certificate["checks"]) != 26 or not all(
        r051_certificate["checks"].values()
    ):
        raise SystemExit("R0.51 certificate checks are incomplete")

    progress(started, "reconstructing exact degree-80 center")
    active_field, _, _, _ = r028.rational_edge_recurrence(80, False, started)
    polynomial = r036.field_to_polynomial(active_field, 80)
    if r037.polynomial_digest(polynomial) != r051_certificate[
        "finiteConstruction"
    ]["degreeEightyPolynomialSha256"]:
        raise SystemExit("degree-80 polynomial hash mismatch")
    character = Q(r051_certificate["input"]["character"]["exact"])
    radius_lower = Q(
        r051_certificate["thresholdTheorem"]["rootIsolation"]["lower"]["exact"]
    )
    radius_upper = Q(
        r051_certificate["thresholdTheorem"]["rootIsolation"]["upper"]["exact"]
    )
    terms = r051.charge_scaled_terms(polynomial, character)

    progress(started, "sampling conservative active/zero switch", points=126)
    switch_rows = []
    lambda_lower = Q(7652, 10000)
    lambda_step = Q(1, 500000)
    for index in range(126):
        lam = lambda_lower + index * lambda_step
        active_poly = r051.exact_affine_column_polynomial(
            terms,
            80,
            81,
            162,
            lam,
        )
        zero_poly = r051.affine_zero_sector_polynomial(terms, 80, lam)
        active_lower = r047.poly_evaluate(active_poly, radius_lower)
        zero_upper = r047.poly_evaluate(zero_poly, radius_upper)
        gap = active_lower - zero_upper
        switch_rows.append(
            {
                "sampleIndex": index,
                "lambdaExact": str(lam),
                "lambdaDecimal": decimal(lam, 18),
                "activeLowerDecimal": decimal(active_lower, 32),
                "zeroUpperDecimal": decimal(zero_upper, 32),
                "activeMinusZeroPpmDecimal": decimal(gap * 1_000_000, 28),
                "isCertifiedChoice": str(lam == Q(7653, 10000)).lower(),
                "classification": (
                    "exact-rational presentation sample of the conservative "
                    "R0.51 root-box constraint gap"
                ),
            }
        )
    write_csv(
        HERE / "constraint-switch.csv",
        list(switch_rows[0]),
        switch_rows,
    )

    progress(started, "computing exact incremental gain factors")
    bounds = {
        key: root_bounds(certificate, key)
        for key, certificate in certificates.items()
    }
    stage_specs = [
        ("R0.49 / R0.48", "multiplicative c=4/5", "r049", "r048"),
        ("R0.50 / R0.49", "optimized multiplicative c", "r050", "r049"),
        ("R0.51 / R0.50", "fixed affine factor", "r051", "r050"),
    ]
    gain_rows = []
    for order, (label, refinement, new_key, old_key) in enumerate(
        stage_specs,
        start=1,
    ):
        factor = bounds[new_key][0] / bounds[old_key][1]
        ppm = (factor - 1) * 1_000_000
        gain_rows.append(
            {
                "order": order,
                "label": label,
                "refinement": refinement,
                "newLowerExact": str(bounds[new_key][0]),
                "previousUpperExact": str(bounds[old_key][1]),
                "strictGainFactorExact": str(factor),
                "strictGainPpmDecimal": decimal(ppm, 24),
                "classification": (
                    "formal lower gain from the new exact lower root divided "
                    "by the preceding exact upper root"
                ),
            }
        )
    write_csv(HERE / "incremental-gains.csv", list(gain_rows[0]), gain_rows)

    progress(started, "extracting all exact competitor gaps", competitors=243)
    ordered_competitors = sorted(
        r051_certificate["competitorDominance"]["records"],
        key=lambda record: Q(record["gapBelowActiveAtRootBoxLeft"]["exact"]),
    )
    competitor_rows = []
    for rank, record in enumerate(ordered_competitors, start=1):
        gap = Q(record["gapBelowActiveAtRootBoxLeft"]["exact"])
        competitor_rows.append(
            {
                "rankByGap": rank,
                "label": record["label"],
                "sector": record["sector"],
                "gapExact": str(gap),
                "gapDecimal": decimal(gap, 24),
                "isNearest": str(rank == 1).lower(),
                "classification": (
                    "formal exact competitor gap on the complete R0.51 root box"
                ),
            }
        )
    write_csv(
        HERE / "competitor-gaps.csv",
        list(competitor_rows[0]),
        competitor_rows,
    )

    shutil.copyfile(
        RESEARCH / "certificates/r051/progress.ndjson",
        HERE / "progress.ndjson",
    )
    shutil.copyfile(
        RESEARCH / "certificates/r051/resources.csv",
        HERE / "resources.csv",
    )
    sign_changes = sum(
        float(left["activeMinusZeroPpmDecimal"])
        * float(right["activeMinusZeroPpmDecimal"])
        < 0
        for left, right in zip(switch_rows, switch_rows[1:], strict=False)
    )
    metadata = {
        "createdAtUtc": datetime.now(timezone.utc).isoformat(),
        "arithmetic": "gmpy2.mpq exact rationals; decimal strings for display",
        "certificateSha256": EXPECTED_SHA256["r051"],
        "switchSamples": len(switch_rows),
        "switchSignChanges": sign_changes,
        "gainRows": len(gain_rows),
        "competitors": len(competitor_rows),
        "lambdaRange": [str(lambda_lower), str(lambda_lower + 125 * lambda_step)],
        "lambdaStep": str(lambda_step),
        "wallSeconds": time.perf_counter() - started,
        "randomness": False,
    }
    (HERE / "sampling-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    progress(
        started,
        "figure tables complete",
        switchSamples=len(switch_rows),
        gainRows=len(gain_rows),
        competitors=len(competitor_rows),
        signChanges=sign_changes,
    )


if __name__ == "__main__":
    main()
