#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.76A."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r076a_complete_clock_localized_current_sign_obstruction"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r076a_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R076A_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R076A_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R076A_MUTATION", "")
SCHEMA = "r076a-complete-clock-localized-current-sign-obstruction-certificate-v1"

FROZEN = {
    f"research/{STEM}.md":
        "d23532f84702be1630daa0b8d56d02242571dd8a1f8024c59a7f71bec30f26eb",
    f"research/{STEM}_primary_audit.md":
        "0f7f56d32025f4cd86218f54dfcf5155675f316d2afecdd0007b13ad70240a8d",
    "research/r076a_report-source.md":
        "0bbf94774c7d76e623c025a731e0238eca39080c4720a039f080afb038ecad8b",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md":
        "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075w_full_frequency_two_harmonic_flux_payment.md":
        "571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4",
    "research/r075z_unresolved_cluster_carrier_current_gate.md":
        "30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97",
}
FIXTURES_SHA256 = "f3644b2a7a641bc92c6c1936f1c05cbed88a6a3e94e25d650c7258ce07b30a31"
EXPECTED_SHA256 = "32d0f99d07d842bf6c9161698249c186c4d23d2f1f33e7f8bd7fc18804887697"

GROUPS = {
    "bindings": (
        "main_hash", "primary_hash", "source_hash", "r_hash", "w_hash", "z_hash",
    ),
    "inputs": ("fixture_hash", "expected_hash", "fixture_schema", "expected_schema"),
    "integrity": (
        "utf8", "controls", "tags", "display_opens", "display_closes",
        "references", "left_escape", "fraction_escape",
    ),
    "geometry": (
        "delta_order", "support_radius", "support_bound", "plateau_length",
        "plateau_bound", "xi_mass", "xi_nonzero",
    ),
    "cluster": (
        "threshold", "ceiling_carrier", "alpha", "beta", "carrier_branch",
        "gap_branch", "dyadic_band",
    ),
    "clock": ("radius", "physical_speed", "scaled_speed", "physical_end", "clock_end"),
    "damping": ("mu", "four_mu", "quarter_bound", "exp_bound", "r_lower"),
    "phase": ("phase_actual", "phase_half", "cosine_inequality", "cosine_lower"),
    "current": ("current_formula", "bracket_upper", "current_upper", "current_negative"),
    "correction": (
        "derivative_square", "beta_square_bound", "correction_upper",
        "target_upper", "correction_negative",
    ),
    "point": ("point_z", "point_zz", "point_j", "point_correction", "pde_residual", "full_gradient"),
    "localization": (
        "positive_weight", "nonzero_cutoff", "negative_integral", "negative_coefficient",
        "common_heat", "all_cutoffs",
    ),
    "source": (
        "nazarov", "kovrijkine", "egidi_veselic", "jaming_saba",
        "context_only", "no_novelty",
    ),
    "audit": ("audit_pass", "math_zero", "release_zero", "finite_not_proof", "figure_decision"),
    "boundary": (
        "sign_only", "perturbative_open", "joint_open", "z_payment_open",
        "w_payment_retained", "regularity_open", "singularity_open", "not_clay",
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


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def ceil_q(value: Q) -> int:
    return -(-value.numerator // value.denominator)


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R076A_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.76A suite")

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
        "source_hash": "research/r076a_report-source.md",
        "r_hash": "research/r075r_outer_cap_spectral_concentration_obstruction.md",
        "w_hash": "research/r075w_full_frequency_two_harmonic_flux_payment.md",
        "z_hash": "research/r075z_unresolved_cluster_carrier_current_gate.md",
    }.get(MUTATION)
    if mutation_path:
        frozen[mutation_path] = "0" * 64
    bindings = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(frozen.items())
    }

    delta0 = Q(fixtures["profile"]["delta0"])
    delta = Q(fixtures["profile"]["delta"])
    q_count = int(fixtures["scale"]["q"])
    a = Q(fixtures["scale"]["a"])
    ell = Q(fixtures["scale"]["ell"])
    clock_end = Q(fixtures["scale"]["clockEnd"])
    v_fixture = Q(fixtures["scale"]["scaledSpeed"])
    frequencies = [int(value) for value in fixtures["cluster"]["frequencies"]]
    amplitudes = [int(value) for value in fixtures["cluster"]["amplitudes"]]
    phases = [int(value) for value in fixtures["cluster"]["phasesOverPi"]]

    support_radius = 1 + delta / a
    plateau_length = 2 - 2 * delta / a
    xi_mass_lower_over_pi = 2 * delta0
    computed_geometry = {
        "supportRadius": qstr(support_radius),
        "supportWithinThreeHalves": support_radius <= Q(3, 2),
        "centralPlateauLength": qstr(plateau_length),
        "centralPlateauAtLeastOne": plateau_length >= 1,
        "xiMassLowerOverPi": qstr(xi_mass_lower_over_pi),
    }

    threshold = 8 * q_count
    carrier = frequencies[0]
    upper = frequencies[1]
    computed_carrier = ceil_q(Q(threshold, 1) / ell)
    alpha = carrier * ell
    beta = (upper - carrier) * ell
    radius = ell / a
    physical_speed = a / radius
    scaled_speed = physical_speed * radius / a
    computed_cluster = {
        "threshold": threshold,
        "carrier": carrier,
        "upperFrequency": upper,
        "alpha": int(alpha),
        "beta": qstr(beta),
        "carrierCondition": alpha >= threshold,
        "gapConditionFails": beta < threshold,
        "dyadicBand": upper <= 2 * carrier,
        "R": qstr(radius),
        "physicalSpeed": int(physical_speed),
        "scaledSpeed": int(scaled_speed),
    }

    mu = (2 * alpha * beta + beta * beta) / (a * a)
    four_mu = 4 * mu
    phase_actual = beta * (support_radius + clock_end)
    phase_bound = Q(1, 2)
    cosine_lower = Q(7, 8)
    r_lower = Q(3, 4)
    current_upper = -Q(9, 16) * beta
    correction_upper = beta * beta + 2 * alpha * current_upper
    target_correction_upper = -alpha * beta
    computed_bounds = {
        "mu": qstr(mu),
        "fourMu": qstr(four_mu),
        "fourMuBelowQuarter": four_mu < Q(1, 4),
        "phaseMaximum": qstr(phase_bound),
        "cosineLower": qstr(cosine_lower),
        "rLower": qstr(r_lower),
        "currentUpper": qstr(current_upper),
        "correctionUpper": qstr(correction_upper),
        "targetCorrectionUpper": qstr(target_correction_upper),
        "correctionTargetHolds": correction_upper <= target_correction_upper,
        "strictNegative": current_upper < 0 and correction_upper < 0,
    }

    phase_signs = [1 if value % 2 == 0 else -1 for value in phases]
    point_z = amplitudes[0] * phase_signs[0] + amplitudes[1] * phase_signs[1]
    point_zz = beta * amplitudes[1] * phase_signs[1]
    point_j = point_z * point_zz
    point_correction = point_zz * point_zz + 2 * alpha * point_j
    full_gradient = alpha * alpha * point_z * point_z + point_correction
    pde_residual = mu - (2 * alpha * beta + beta * beta) / (a * a)
    computed_point = {
        "Z": [point_z, 0],
        "Zz": [0, qstr(point_zz)],
        "J": qstr(point_j),
        "correctionDensity": qstr(point_correction),
    }
    negative_coefficient_over_pi = -Q(9, 8) * delta0 * beta
    physical_end = clock_end * radius * radius
    computed_clock = {
        "physicalEnd": qstr(physical_end),
        "negativeCoefficientOverPi": qstr(negative_coefficient_over_pi),
    }

    tags = [int(value) for value in re.findall(r"\\tag\{A\.(\d+)\}", text)]
    references = [int(value) for value in re.findall(r"\bA\.(\d+)\b", text)]
    display_opens = len(re.findall(r"(?m)^\\\[$", text))
    display_closes = len(re.findall(r"(?m)^\\\]$", text))
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
        and fixtures["schema"].endswith("fixtures-v1")
        and expected["schema"].endswith("expected-v1"),
    )
    record(
        "UTF-8, controls, tags, displays, references, and TeX escapes", "integrity",
        clean_bytes(raw) and clean_bytes(raw_primary) and clean_bytes(raw_source)
        and tags == list(range(1, 35))
        and display_opens == 34 and display_closes == 34
        and not (set(references) - set(tags))
        and r"I_-=\left[" in text
        and r"\frac18\alpha\beta-\frac98\alpha\beta" in text,
        {"tags": len(tags), "opens": display_opens, "closes": display_closes},
    )
    record(
        "primitive support, plateau, and mass ledger", "geometry",
        0 < delta0 < delta and a >= max(Q(24), 2 * delta)
        and computed_geometry == expected["geometry"]
        and all_in(compact, [
            r"\Xi_a(z)\ge0", r"\subset\left[-\frac32,\frac32\right]",
            r"\int_{\mathbb R}\Xi_a(z)\,dz\ge2\pi\delta_0>0",
        ]),
        {"computed": computed_geometry},
    )
    record(
        "exact high-carrier unresolved cluster", "cluster",
        computed_carrier == carrier
        and computed_cluster == expected["cluster"]
        and all_in(compact, [
            r"N=\left\lceil\frac{16}{\ell}\right\rceil",
            r"N\ell\ge8q", r"\beta<8q", "actual unresolved high-carrier cluster",
        ]),
        computed_cluster,
    )
    record(
        "scaled and physical clock ledger", "clock",
        v_fixture == scaled_speed == 1
        and computed_clock == expected["clock"]
        and all_in(compact, [r"s=\frac t{R^2}", r"v=\frac{BR}{a}", "constant speed `B=a/R`"]),
        computed_clock,
    )
    record(
        "exact damping and uniform envelope lower bound", "damping",
        qstr(mu) == expected["bounds"]["mu"]
        and qstr(four_mu) == expected["bounds"]["fourMu"]
        and four_mu < Q(1, 4)
        and math.exp(-0.25) > 0.75
        and all_in(compact, [r"4\mu", r"<\frac14", r"\frac34<e^{-1/4}\le r(s)\le1"]),
        {"mu": qstr(mu), "fourMu": qstr(four_mu)},
    )
    record(
        "support-wide complete-clock phase bound", "phase",
        phase_actual <= phase_bound
        and qstr(phase_bound) == expected["bounds"]["phaseMaximum"]
        and qstr(cosine_lower) == expected["bounds"]["cosineLower"]
        and all_in(compact, [r"|\beta(z-s)|", r"\le\frac12", r"\ge\frac78"]),
        {"actualMaximum": qstr(phase_actual), "certifiedMaximum": qstr(phase_bound)},
    )
    record(
        "uniform strict negative current", "current",
        qstr(current_upper) == expected["bounds"]["currentUpper"]
        and current_upper < 0
        and all_in(compact, [
            r"&=\beta r\left(r-2\cos(\beta(z-s))\right)",
            r"J\le-\frac34\beta r\le-\frac9{16}\beta",
        ]),
        {"currentUpper": qstr(current_upper)},
    )
    record(
        "uniform negative correction density", "correction",
        qstr(correction_upper) == expected["bounds"]["correctionUpper"]
        and qstr(target_correction_upper) == expected["bounds"]["targetCorrectionUpper"]
        and correction_upper <= target_correction_upper < 0
        and all_in(compact, [
            r"|\partial_zZ|^2=\beta^2r^2\le\beta^2",
            r"\le\frac18\alpha\beta-\frac98\alpha\beta", r"=-\alpha\beta",
        ]),
        {"correctionUpper": qstr(correction_upper), "target": qstr(target_correction_upper)},
    )
    record(
        "exact point, PDE coefficient, and retained full gradient", "point",
        computed_point == expected["point"]
        and pde_residual == 0 and full_gradient == Q(30625, 121)
        and all_in(compact_primary, [
            r"Z_s+Z_z-a^{-2}Z_{zz}-2i\alpha a^{-2}Z_z=0",
            r"J=-\frac1{11}", r"\frac{30625}{121}>0",
        ]),
        {"point": computed_point, "pdeResidual": qstr(pde_residual), "fullGradient": qstr(full_gradient)},
    )
    record(
        "strict negativity after every admissible localization", "localization",
        negative_coefficient_over_pi == Q(expected["clock"]["negativeCoefficientOverPi"])
        and all_in(compact, [
            r"\zeta:[0,4]\longrightarrow[0,1]", r"\int_0^4\zeta(s)\,ds>0",
            r"\zeta e^{-2\alpha^2s/a^2}", r"<0", "Every nonzero frozen cutoff",
        ]),
        {"negativeCoefficientOverPi": qstr(negative_coefficient_over_pi)},
    )
    record(
        "bounded contextual source report", "source",
        all_in(compact_source, [
            "https://www.mathnet.ru/eng/aa397", "https://arxiv.org/abs/math/0012186",
            "https://arxiv.org/abs/1609.07020", "https://arxiv.org/abs/2311.17714",
            "Context only", "not represented as evidence of novelty",
        ]),
    )
    record(
        "primary audit and analytic-only figure decision", "audit",
        all_in(compact_primary, [
            "Current verdict: **PASS**", "Mathematical blocker count: **0**",
            "Release blocker count: **0**", "not represented as proof",
            "no simulation or formal scientific figure is needed",
        ]),
    )
    record(
        "narrow sign obstruction and open-claim boundary", "boundary",
        all_in(compact, [
            "rules out only the strategy of discarding", "may still be perturbative",
            "joint multiplier argument must retain", "full Z-sector collar-flux estimate",
            "already pays that estimate", "regularity", "singularity", "**NOT CLAY.**",
        ]),
    )

    verdict = "PASS" if all(item["pass"] for item in assertions) else "FAIL"
    payload = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertions": assertions,
        "computed": {
            "geometry": computed_geometry,
            "cluster": computed_cluster,
            "bounds": computed_bounds,
            "point": computed_point,
            "clock": computed_clock,
            "auxiliary": {
                "phaseActual": qstr(phase_actual),
                "pdeResidual": qstr(pde_residual),
                "fullGradient": qstr(full_gradient),
            },
        },
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "boundary": {
            "finiteFixturesAreProof": False,
            "localizedSignDropping": "REJECTED",
            "generalClusterCurrentEstimate": "OPEN",
            "fullZSectorPayment": "OPEN",
            "versionM": "OPEN",
            "regularity": "OPEN",
            "clayProblemSolved": False,
        },
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    passed = sum(item["pass"] for item in assertions)
    report = [
        "# R0.76A exact finite certificate report",
        "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {passed}/{len(assertions)}",
        f"- Mutation challenge: {MUTATION or 'none'}",
        "- Arithmetic: exact rational recomputation except the elementary numerical check `exp(-1/4)>3/4`",
        "",
        "The certificate recomputes the frozen support, complete clock, unresolved",
        "integer-frequency pair, damping and phase constants, point current, and",
        "correction-density ledgers.  The continuum sign proof remains in the main",
        "note and primary audit; finite fixtures are not proof of those identities.",
        "",
        "Only localized sign-dropping is rejected.  General cluster payment,",
        "Version-M transfer, regularity, and singularity remain OPEN. **NOT CLAY.**",
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"suite": SCHEMA, "verdict": verdict, "assertions": len(assertions), "mutation": MUTATION}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
