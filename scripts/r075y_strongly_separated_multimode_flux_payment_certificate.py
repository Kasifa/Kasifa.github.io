#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75Y."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r075y_strongly_separated_multimode_flux_payment"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r075y_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R075Y_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R075Y_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R075Y_MUTATION", "")
SCHEMA = "r075y-strongly-separated-multimode-flux-payment-certificate-v1"

FROZEN = {
    f"research/{STEM}.md":
        "74790f910b596c86b204291d997ef723cabbc85d14a89e3fe900814fcd88b0a6",
    f"research/{STEM}_primary_audit.md":
        "f7e1feedd1fa359877554eff4fa20c470f727ae7743c990136525ad22d6cdf3b",
    "research/r075y_report-source.md":
        "e6d6b1ed2830b46fc901a9ab09ef368f258f13dfc8c0961076baedd5b46e1589",
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md":
        "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075u_two_harmonic_difference_frequency_payment.md":
        "f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4",
    "research/r075x_fixed_finite_mode_low_carrier_payment.md":
        "8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763",
}
FIXTURES_SHA256 = "45448bf75c867b3f9654db79c77ae52b9bd35d7e781b240f564a9d871faab32b"
EXPECTED_SHA256 = "324e92dd32d6e1ca76b22c47a201206e1c924e1100b92de1c8429ffd17ac25d3"

GROUPS = {
    "bindings": (
        "main_hash", "primary_hash", "source_hash", "b_hash", "r_hash",
        "u_hash", "x_hash",
    ),
    "inputs": ("fixture_hash", "expected_hash", "fixture_schema"),
    "integrity": ("utf8", "controls", "tags", "displays", "references", "tex_spacing"),
    "clock": ("clock_length", "cutoff_range", "cutoff_onset", "cutoff_derivative"),
    "geometry": ("plateau_widths", "central_chart", "fibre_area"),
    "family": ("positive_modes", "ordered_modes", "dyadic_band", "signed_gap", "separation"),
    "gram": (
        "signed_count", "minimum_gap", "offdiagonal_factor", "strict_margin",
        "l2_coefficient", "l3_coefficient", "signed_two_n1",
    ),
    "time": (
        "slow_phase", "fast_phase", "large_heat", "zero_shear",
        "physical_r", "physical_r_power",
    ),
    "flux": (
        "self_rows", "difference_rows", "sum_rows", "total_rows",
        "positive_row_frequencies", "phase_signs", "radial_quotient",
    ),
    "payment": ("modal_domination", "row_payment", "mass_payment"),
    "scale": ("clock_scale", "radial_scale", "row_scale", "mass_scale", "target_scale"),
    "normalization": ("p_definition", "x_definition", "r_cancel", "omega_power", "rate"),
    "q_boundary": (
        "explicit_q_square", "forced_carrier", "subexponential_q",
        "sparse_not_dense", "r_obstruction",
    ),
    "source": ("source_urls", "classical_boundary", "bounded_search", "no_novelty"),
    "audit": ("audit_pass", "math_zero", "release_zero", "deletion_tests", "finite_boundary"),
    "figure": ("analytic_only", "no_simulation_claim", "no_formal_figure"),
    "boundary": (
        "clusters_open", "packets_open", "e24_open", "version_m_conditional",
        "actual_component", "regularity_open", "not_clay",
    ),
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


def flat(value: str) -> str:
    return re.sub(r"\s+", " ", value)


def all_in(value: str, fragments: list[str]) -> bool:
    return all(fragment in value for fragment in fragments)


def qtext(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def encoded(values: dict[str, Q]) -> dict[str, str | int]:
    return {
        key: int(value) if value.denominator == 1 else str(value)
        for key, value in values.items()
    }


def add_powers(*rows: dict[str, Q]) -> dict[str, Q]:
    keys = set().union(*(row.keys() for row in rows))
    return {key: sum((row.get(key, Q(0)) for row in rows), Q(0)) for key in keys}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075Y_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.75Y suite")

    raw = MAIN.read_bytes()
    raw_primary = PRIMARY.read_bytes()
    raw_source = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    primary = raw_primary.decode("utf-8")
    source = raw_source.decode("utf-8")
    compact = flat(text)
    compact_primary = flat(primary)
    compact_source = flat(source)
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    frozen = dict(FROZEN)
    mutation_path = {
        "main_hash": f"research/{STEM}.md",
        "primary_hash": f"research/{STEM}_primary_audit.md",
        "source_hash": "research/r075y_report-source.md",
        "b_hash": "research/r075b_bulk_clock_outer_padding_gate.md",
        "r_hash": "research/r075r_outer_cap_spectral_concentration_obstruction.md",
        "u_hash": "research/r075u_two_harmonic_difference_frequency_payment.md",
        "x_hash": "research/r075x_fixed_finite_mode_low_carrier_payment.md",
    }.get(MUTATION)
    if mutation_path:
        frozen[mutation_path] = "0" * 64
    bindings = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(frozen.items())
    }

    clock = fixtures["clock"]
    radius = Q(clock["R"])
    duration = Q(clock["durationCoefficient"]) * radius ** int(clock["durationRPower"])
    computed_clock = {"T": qtext(duration)}

    case = fixtures["separatedCase"]
    q_count = int(case["q"])
    modes = [int(value) for value in case["frequencies"]]
    a_value = Q(case["a"])
    radius = Q(case["R"])
    ell = a_value * radius
    signed = sorted([-mode for mode in modes] + modes)
    minimum_gap = min(right - left for left, right in zip(signed, signed[1:]))
    threshold = int(case["separationMultiplier"]) * q_count
    separation_product = ell * minimum_gap
    offdiag = Q(2 * (2 * q_count - 1), minimum_gap)
    half_diagonal = ell / 2
    retained_diagonal = ell - offdiag
    computed_case = {
        "ell": qtext(ell),
        "signedFrequencies": signed,
        "minimumSignedGap": minimum_gap,
        "threshold": threshold,
        "separationProduct": int(separation_product) if separation_product.denominator == 1 else qtext(separation_product),
        "condition": bool(separation_product >= threshold),
        "dyadicBand": bool(modes[-1] <= 2 * modes[0]),
        "forcedCarrierFloor": int(case["separationMultiplier"]) * q_count * (q_count - 1),
    }
    computed_gram = {
        "signedModeCount": len(signed),
        "offDiagonalCoefficient": qtext(offdiag),
        "halfDiagonalCoefficient": qtext(half_diagonal),
        "retainedDiagonalCoefficient": qtext(retained_diagonal),
        "theoremL2Coefficient": qtext(ell / 4),
        "theoremL3Coefficient": qtext(ell / 8),
    }

    row_inputs = fixtures["rowLedger"]
    pairs = q_count * (q_count - 1) // 2
    computed_rows = {
        "selfRows": q_count * int(row_inputs["selfRowsPerMode"]),
        "differenceRows": pairs * int(row_inputs["differenceRowsPerPair"]),
        "sumRows": pairs * int(row_inputs["sumRowsPerPair"]),
        "totalRows": q_count + 2 * pairs,
    }

    clock_scale = {"r": Q(-1), "R": Q(-4, 3), "P3Integral": Q(2, 3)}
    radial_scale = {"r": Q(1), "a": Q(2), "R": Q(3)}
    row_scale = add_powers(clock_scale, radial_scale)
    row_scale.pop("r")
    row_scale["S3Integral"] = row_scale.pop("P3Integral")
    mass_scale = {"a": Q(2), "R": Q(3), "S3Integral": Q(1)}
    target_scale = add_powers(
        {"q": Q(2), **row_scale},
        {"a": Q(-4, 3), "R": Q(-2), "S3Integral": Q(-2, 3), "M": Q(2, 3)},
    )
    target_scale = {key: value for key, value in target_scale.items() if value}
    normalized = add_powers(
        target_scale,
        {"omega": Q(1), "R": Q(-1)},
        {"R": Q(4, 3), "omega": Q(-2, 3), "p": Q(2, 3), "M": Q(-2, 3)},
    )
    normalized = {
        key: normalized.get(key, Q(0))
        for key in ("q", "a", "R", "omega", "p")
    }
    computed_scale = {
        "clockRow": encoded(clock_scale),
        "radialQuotient": encoded(radial_scale),
        "afterRow": encoded(row_scale),
        "mass": encoded(mass_scale),
        "target": encoded(target_scale),
        "normalized": encoded(normalized),
        "frozenRate": qtext(-Q(fixtures["frozenScales"]["cGamma"]) / 12),
    }

    tags = [int(value) for value in re.findall(r"\\tag\{Y\.(\d+)\}", text)]
    refs = [int(value) for value in re.findall(r"\bY\.(\d+)\b", text)]
    assertions: list[dict[str, Any]] = []

    def record(name: str, group: str, ok: bool, details: Any = None) -> None:
        passed = bool(ok) and MUTATION not in GROUPS[group]
        assertions.append({"name": name, "group": group, "pass": passed, "details": details})

    record(
        "frozen source bindings", "bindings",
        all(item["expectedSha256"] == item["observedSha256"] for item in bindings.values()),
        bindings,
    )
    record(
        "fixture and expected bindings", "inputs",
        sha256(FIXTURES) == FIXTURES_SHA256
        and sha256(EXPECTED) == EXPECTED_SHA256
        and fixtures["schema"].endswith("fixtures-v1"),
    )
    record(
        "UTF-8, controls, tags, displays, references, and TeX spacing", "integrity",
        clean_bytes(raw)
        and clean_bytes(raw_primary)
        and clean_bytes(raw_source)
        and tags == list(range(1, 40))
        and text.count("\\[") == 39
        and text.count("\\]") == 39
        and not (set(refs) - set(tags))
        and not re.findall(r"(?<![\\A-Za-z])(?:quad|qquad)\b", text),
    )
    record(
        "complete clock and cutoff onset", "clock",
        computed_clock == expected["clock"]
        and all_in(compact, ["T_R=4R^2", "\\eta_R(0)=0", "C_\\eta R^{-2}"]),
        computed_clock,
    )
    record(
        "plateau geometry and central chart", "geometry",
        all_in(compact, ["0<\\delta_0<\\delta", "a\\ge4\\delta_0", "(a+\\delta)R<\\frac\\pi2", "4\\pi a\\delta_0R^2"]),
    )
    record(
        "ordered dyadic family and exact signed separation fixture", "family",
        computed_case == expected["separatedCase"]
        and modes == sorted(set(modes))
        and minimum_gap == int(case["minimumSignedGap"]),
        computed_case,
    )
    record(
        "Gram ledger and strict half-diagonal margin", "gram",
        computed_gram == expected["gramLedger"]
        and separation_product >= threshold
        and offdiag <= half_diagonal
        and all_in(compact, ["\\{2n_1\\}\\cup", "\\ell\\delta_{\\boldsymbol n}\\ge8q", "\\ge\\frac\\ell4S(t)^2", "\\ge\\frac\\ell8S(t)^3"]),
        computed_gram,
    )
    record(
        "phase-free slow/fast complete-clock lemma", "time",
        all_in(compact, ["|\\sigma|\\tau\\le1", "|\\sigma|\\tau\\ge1", "\\zeta(s)\\le C_\\eta s", "|w(4)|+\\int_0^4|w'(s)|", "\\frac{C}{rR^{4/3}}"]),
    )
    record(
        "exact positive-frequency row ledger", "flux",
        computed_rows == expected["rowLedger"]
        and all_in(compact, ["J_{2n_j,R}", "J_{n_j-n_i,R}", "J_{n_i+n_j,R}", "\\sin(\\phi_j(t)-\\phi_i(t))", "\\frac{|J_{r,R}|}{r}\\le Ca^2R^3"]),
        computed_rows,
    )
    record(
        "modal, row, and plateau payment", "payment",
        all_in(compact, ["P(t)^{3/2}\\le S(t)^3", "Cq^2a^2R^{5/3}", "\\frac{\\pi\\delta_0}{2}a^2R^3"]),
    )
    record(
        "exact a, R, q, and mass scale ledger", "scale",
        computed_scale["clockRow"] == expected["scaleLedger"]["clockRow"]
        and computed_scale["radialQuotient"] == expected["scaleLedger"]["radialQuotient"]
        and computed_scale["afterRow"] == expected["scaleLedger"]["afterRow"]
        and computed_scale["mass"] == expected["scaleLedger"]["mass"]
        and computed_scale["target"] == expected["scaleLedger"]["target"],
        computed_scale,
    )
    record(
        "normalization and frozen logarithmic rate", "normalization",
        computed_scale["normalized"] == expected["scaleLedger"]["normalized"]
        and computed_scale["frozenRate"] == expected["scaleLedger"]["frozenRate"]
        and all_in(compact, ["R^{-2}\\omega M", "\\frac{\\omega}{R}", "-\\frac2{11907}"]),
    )
    record(
        "explicit q-square and sparse growing-q boundary", "q_boundary",
        all_in(compact, ["q+2\\binom q2=q^2", "n_1\\ell>=8q(q-1)", "\\log q=o(L^2)", "not a dense-packet hypothesis", "outer-cap packet obstruction of R0.75R"]),
    )
    record(
        "bounded source and collision boundary", "source",
        all_in(compact_source, ["https://arxiv.org/abs/2311.17714", "https://arxiv.org/abs/1705.11017", "No external paper is used as proof", "not evidence of completeness, novelty, or priority"]),
    )
    record(
        "primary audit and adversarial deletion tests", "audit",
        all_in(compact_primary, ["Current verdict: **PASS**", "Mathematical blocker count: **0**", "Release blocker count: **0**", "If `2n_1` is deleted", "If `eta_R(0)=0` is deleted", "not represented as proof"]),
    )
    record(
        "analytic-only figure boundary", "figure",
        all_in(compact, ["proof is analytic", "no simulation or formal scientific figure is needed"]),
    )
    record(
        "open-problem and Version-M boundary", "boundary",
        all_in(compact, ["unresolved high-carrier clusters", "arbitrary dyadic packets", "arbitrary-field E.24", "Version-M measurement row", "actual component", "regularity; and singularity", "**NOT CLAY.**"]),
    )

    failures = [item["name"] for item in assertions if not item["pass"]]
    verdict = "PASS" if not failures else "FAIL"
    result = {
        "schema": SCHEMA,
        "bindings": bindings,
        "fixturesSha256": sha256(FIXTURES),
        "expectedSha256": sha256(EXPECTED),
        "computed": {
            "clock": computed_clock,
            "separatedCase": computed_case,
            "gramLedger": computed_gram,
            "rowLedger": computed_rows,
            "scaleLedger": computed_scale,
        },
        "assertions": assertions,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "summary": {
            "assertions": len(assertions),
            "passed": len(assertions) - len(failures),
            "failed": len(failures),
            "failures": failures,
            "verdict": verdict,
        },
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUT_REPORT.write_text(
        "\n".join(
            [
                "# R0.75Y exact certificate report",
                "",
                f"- Verdict: **{verdict}**",
                f"- Assertions: {len(assertions) - len(failures)}/{len(assertions)}",
                f"- Mutation mode: `{MUTATION or 'none'}`",
                f"- Exact q=3 separation product: `{qtext(separation_product)}`",
                f"- Exact off-diagonal Gram coefficient: `{qtext(offdiag)}`",
                f"- Exact retained diagonal coefficient: `{qtext(retained_diagonal)}`",
                f"- Exact Fourier-row count: `{computed_rows['totalRows']}`",
                f"- Frozen logarithmic rate: `{computed_scale['frozenRate']}`",
                "",
                "Finite checks bind the source bytes, exact rational ledgers, formula structure,",
                "and claim boundary. They are not proof of the continuum Gram or complete-clock",
                "lemmas. Unresolved clusters and the Navier--Stokes regularity problem remain open.",
                "**NOT CLAY.**",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps(result["summary"], sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
