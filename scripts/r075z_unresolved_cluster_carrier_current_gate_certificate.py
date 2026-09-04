#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75Z."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r075z_unresolved_cluster_carrier_current_gate"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r075z_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R075Z_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R075Z_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R075Z_MUTATION", "")
SCHEMA = "r075z-unresolved-cluster-carrier-current-gate-certificate-v1"

FROZEN = {
    f"research/{STEM}.md":
        "30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97",
    f"research/{STEM}_primary_audit.md":
        "895d09e0b403c0a6bcf216624527dd6c2bf76f15d7ce5f6b6b0a31b6f64a1eb0",
    "research/r075z_report-source.md":
        "9b071b3e020210922834435ea7e5806620479d400eb044f48f34e7b02c259d4c",
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md":
        "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075x_fixed_finite_mode_low_carrier_payment.md":
        "8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763",
    "research/r075y_strongly_separated_multimode_flux_payment.md":
        "74790f910b596c86b204291d997ef723cabbc85d14a89e3fe900814fcd88b0a6",
}
FIXTURES_SHA256 = "9bd703f41f4b4823a4b6fe38136bf2a5bef126cf15edb3b54036cf1b80e4f4b0"
EXPECTED_SHA256 = "6043f94b70b6068a58d7716877a5319edc9edfc90b47bfee23ea7baee0ad58d4"

GROUPS = {
    "bindings": (
        "main_hash", "primary_hash", "source_hash", "b_hash", "r_hash",
        "x_hash", "y_hash",
    ),
    "inputs": ("fixture_hash", "expected_hash", "fixture_schema"),
    "integrity": ("utf8", "controls", "tags", "displays", "references", "tex_spacing"),
    "partition": (
        "x_strict", "high_equality", "y_gap_equality", "z_strict_gap",
        "signed_minimum", "disjoint", "exhaustive",
    ),
    "cluster": (
        "separator_equality", "maximal_blocks", "offset_zero", "strict_width",
        "dyadic_width", "nontrivial_z",
    ),
    "modulation": (
        "analytic_signal", "heat_factor", "carrier_factor", "pde_sign",
        "pde_factor_two", "unbounded_decay",
    ),
    "flux": (
        "real_square", "density_half", "carrier_half", "flux_quarters",
        "cross_cluster_open",
    ),
    "current": (
        "q_identity", "current_sign", "current_factor_four", "gradient_identity",
        "full_period_only",
    ),
    "obstruction": (
        "example_phase", "point_values", "weighted_current", "negative_density",
        "n_independent_boundary", "young_not_denied",
    ),
    "source": (
        "nazarov", "kovrijkine", "egidi_veselic", "friedland_yomdin",
        "jaming_saba", "context_only", "no_novelty",
    ),
    "audit": ("audit_pass", "math_zero", "release_zero", "finite_not_proof"),
    "figure": ("analytic_only", "no_simulation", "no_formal_figure"),
    "boundary": (
        "fixed_q_only", "cluster_payment_open", "cross_cluster_open_boundary",
        "packets_open", "version_m_open", "regularity_open", "not_clay",
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


def pair(value: complex) -> list[int]:
    real = round(value.real)
    imag = round(value.imag)
    if abs(value.real - real) > 1e-12 or abs(value.imag - imag) > 1e-12:
        raise ValueError(f"nonintegral complex fixture value: {value}")
    return [int(real), int(imag)]


def signed_minimum_gap(modes: list[int]) -> int:
    signed = sorted([-mode for mode in modes] + modes)
    return min(right - left for left, right in zip(signed, signed[1:]))


def clusters(modes: list[int], ell: Q, threshold: int) -> list[list[int]]:
    result = [[modes[0]]]
    for left, right in zip(modes, modes[1:]):
        if (right - left) * ell >= threshold:
            result.append([right])
        else:
            result[-1].append(right)
    return result


def classify(modes: list[int], ell: Q, threshold: int) -> str:
    if modes[0] * ell < threshold:
        return "X"
    if all((right - left) * ell >= threshold for left, right in zip(modes, modes[1:])):
        return "Y"
    return "Z"


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075Z_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.75Z suite")

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
        "source_hash": "research/r075z_report-source.md",
        "b_hash": "research/r075b_bulk_clock_outer_padding_gate.md",
        "r_hash": "research/r075r_outer_cap_spectral_concentration_obstruction.md",
        "x_hash": "research/r075x_fixed_finite_mode_low_carrier_payment.md",
        "y_hash": "research/r075y_strongly_separated_multimode_flux_payment.md",
    }.get(MUTATION)
    if mutation_path:
        frozen[mutation_path] = "0" * 64
    bindings = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(frozen.items())
    }

    q_count = int(fixtures["q"])
    ell = Q(fixtures["ell"])
    threshold = int(fixtures["thresholdMultiplier"]) * q_count
    cases = fixtures["partitionCases"]
    computed_partition: dict[str, Any] = {}
    for name, values in cases.items():
        modes = [int(value) for value in values]
        item: dict[str, Any] = {
            "sector": classify(modes, ell, threshold),
            "dyadicBand": modes[-1] <= 2 * modes[0],
        }
        if name != "x":
            item.update({
                "signedMinimumGap": signed_minimum_gap(modes),
                "separationProduct": int(ell * signed_minimum_gap(modes)),
                "clusters": clusters(modes, ell, threshold),
            })
        computed_partition[name] = item

    cluster_fixture = fixtures["cluster"]
    carrier = int(cluster_fixture["carrier"])
    offsets = [int(value) for value in cluster_fixture["offsets"]]
    amplitudes = [int(value) for value in cluster_fixture["amplitudes"]]
    phase_signs = [1 if int(value) % 2 == 0 else -1 for value in cluster_fixture["phasesOverPi"]]
    speed = int(cluster_fixture["transportSpeed"])
    coeffs = [complex(amplitude * sign, 0) for amplitude, sign in zip(amplitudes, phase_signs)]
    z_value = sum(coeffs)
    zy_value = sum(1j * offset * coeff for offset, coeff in zip(offsets, coeffs))
    q_value = int(round(abs(z_value) ** 2))
    j_value = int(round((z_value.conjugate() * zy_value).imag))

    residual = 0j
    for offset, coeff in zip(offsets, coeffs):
        zt = complex(-2 * carrier * offset - offset * offset, -speed * offset) * coeff
        zy = 1j * offset * coeff
        zyy = -offset * offset * coeff
        residual += zt + speed * zy - zyy - 2j * carrier * zy

    full_gradient = sum((carrier + offset) ** 2 * amplitude ** 2 for offset, amplitude in zip(offsets, amplitudes))
    current = sum(offset * amplitude ** 2 for offset, amplitude in zip(offsets, amplitudes))
    offset_gradient = sum(offset ** 2 * amplitude ** 2 for offset, amplitude in zip(offsets, amplitudes))
    modulated_dissipation = offset_gradient + 2 * carrier * current
    computed_cluster = {
        "carrier": carrier,
        "offsets": offsets,
        "scaledWidth": int((offsets[-1] - offsets[0]) * ell),
        "strictWidthBound": threshold * (len(offsets) - 1),
        "widthBoundHolds": (offsets[-1] - offsets[0]) * ell < threshold * (len(offsets) - 1),
        "widthBelowCarrier": offsets[-1] <= carrier,
    }
    computed_point = {
        "Z": pair(z_value),
        "Zy": pair(zy_value),
        "Q": q_value,
        "J": j_value,
        "unweightedAbsorber": q_value + int(round(abs(zy_value) ** 2)),
        "weightedCurrent": 2 * carrier * abs(j_value),
        "modulatedDissipationDensity": int(round(abs(zy_value) ** 2)) + 2 * carrier * j_value,
    }
    computed_global = {
        "currentOver2Pi": current,
        "offsetGradientOver2Pi": offset_gradient,
        "modulatedDissipationOver2Pi": modulated_dissipation,
        "fullGradientOver2Pi": full_gradient,
    }
    square_left = int(round(z_value.real ** 2))
    square_right = int(round((abs(z_value) ** 2 + (z_value * z_value).real) / 2))
    computed_identity = {
        "pdeResidual": pair(residual),
        "squareLeft": square_left,
        "squareRight": square_right,
    }

    tags = [int(value) for value in re.findall(r"\\tag\{Z\.(\d+)\}", text)]
    references = [int(value) for value in re.findall(r"\bZ\.(\d+)\b", text)]
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
        "UTF-8, controls, tags, displays, references, and TeX spacing", "integrity",
        clean_bytes(raw)
        and clean_bytes(raw_primary)
        and clean_bytes(raw_source)
        and tags == list(range(1, 32))
        and display_opens == 31
        and display_closes == 31
        and not (set(references) - set(tags))
        and not re.findall(r"(?<![\\A-Za-z])(?:quad|qquad|mathcal)\b", text),
        {"tags": len(tags), "opens": display_opens, "closes": display_closes},
    )
    record(
        "strict X branch, equality Y branch, and unresolved Z branch", "partition",
        threshold == expected["threshold"]
        and computed_partition == expected["partition"]
        and all_in(compact, [
            r"n_1\ell<8q", r"n_1\ell\ge8q", r"(n_{j+1}-n_j)\ell\ge8q",
            r"(n_{j+1}-n_j)\ell<8q", r"\ell\delta_{\boldsymbol n}\ge8q",
            "disjoint and cover all possibilities",
        ]),
        computed_partition,
    )
    record(
        "maximal cluster convention and exact width ledger", "cluster",
        computed_cluster == expected["clusterLedger"]
        and all_in(compact, [
            "place a cut", r"\ge8q", "Maximality makes", r"d_s\ell<8q(s-r)",
            r"d_s\le N", "at least one non-singleton cluster",
        ]),
        computed_cluster,
    )
    record(
        "carrier-envelope representation and exact PDE", "modulation",
        computed_identity["pdeResidual"] == [0, 0]
        and all_in(compact, [
            r"e^{-N^2t}e^{iN(y-Bt)}Z_C", "2Nd_j+d_j^2",
            r"\partial_tZ_C+B\partial_yZ_C-\partial_y^2Z_C",
            r"-2iN\partial_yZ_C=0", "remain unbounded",
        ]),
        computed_identity,
    )
    record(
        "exact real square and one-cluster flux split", "flux",
        computed_identity["squareLeft"] == computed_identity["squareRight"] == 1
        and all_in(compact, [
            "F_C^2", r"\frac12e^{-2N^2t}|Z_C|^2",
            r"\mathcal T_C^{\rm den}", r"\mathcal T_C^{\rm car}",
            "cross-cluster products must still be added",
        ]),
        computed_identity,
    )
    record(
        "local current and unmodulated gradient identities", "current",
        all_in(compact, [
            "Q=|Z|^2", r"J=\operatorname {Im}(\overline Z\,\partial_yZ)",
            r"=-2|\partial_yZ_C|^2-4NJ_C", r"N^2Q+|\partial_yZ|^2+2NJ",
        ]),
    )
    record(
        "full-period current sign and dissipation ledger", "current",
        computed_global == expected["globalLedger"]
        and computed_global["currentOver2Pi"] >= 0
        and computed_global["modulatedDissipationOver2Pi"] >= 0
        and all_in(compact, [
            r"=2\pi\sum_{j=r}^s d_jA_j^2", r"\ge0", "full-period integration",
            "cannot simply be substituted",
        ]),
        computed_global,
    )
    record(
        "carrier-weighted pointwise obstruction", "obstruction",
        computed_point == expected["pointLedger"]
        and all_in(compact, [
            r"Z^{(N)}(y)=2-e^{iy}", "J(0)=-1", "2N|J(y)|",
            "N<=C", "1-2N<0", "does not rule out",
        ]),
        computed_point,
    )
    record(
        "fixed-q and black-box-recursion boundary", "boundary",
        all_in(compact, [
            "For fixed `q`", "does not put the envelope into",
            "No full Z-sector flux payment is claimed", "full Z-sector collar-flux estimate",
        ]),
    )
    record(
        "bounded primary-source collision report", "source",
        all_in(compact_source, [
            "https://www.mathnet.ru/eng/aa397", "https://arxiv.org/abs/math/0012186",
            "https://arxiv.org/abs/1609.07020", "https://arxiv.org/abs/1107.0039",
            "https://arxiv.org/abs/2311.17714", "context and possible tools",
            "No novelty, priority, or completeness claim",
        ]),
    )
    record(
        "primary audit verdict and finite-evidence boundary", "audit",
        all_in(compact_primary, [
            "Current verdict: **PASS**", "Mathematical blocker count: **0**",
            "Release blocker count: **0**", "not represented as proof",
            "full clustered-sector flux payment | **OPEN**",
        ]),
    )
    record(
        "analytic-only figure decision", "figure",
        all_in(compact, [
            "No simulation or formal scientific figure is needed",
            "exact identities",
        ]),
    )
    record(
        "open-claim and NOT CLAY boundary", "boundary",
        all_in(compact, [
            "cross-cluster aggregation", "arbitrary growing packets",
            "complete Version-M extraction", "regularity", "singularity",
            "**NOT CLAY.**",
        ]),
    )

    verdict = "PASS" if all(item["pass"] for item in assertions) else "FAIL"
    payload = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertions": assertions,
        "computed": {
            "threshold": threshold,
            "partition": computed_partition,
            "clusterLedger": computed_cluster,
            "pointLedger": computed_point,
            "globalLedger": computed_global,
            "identityLedger": computed_identity,
        },
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "boundary": {
            "finiteFixturesAreProof": False,
            "fullClusterPayment": "OPEN",
            "crossClusterAggregation": "OPEN",
            "versionM": "OPEN",
            "regularity": "OPEN",
            "clayProblemSolved": False,
        },
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    passed_count = sum(bool(item["pass"]) for item in assertions)
    report = [
        "# R0.75Z exact finite certificate report",
        "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {passed_count}/{len(assertions)}",
        f"- Negative mutation classes: {len(NEGATIVE_MUTATIONS)}",
        "- Fixture: q=2, ell=1; strict X case, equality Y case, and clustered Z case",
        "- Exact point test: Z=2-exp(iy) at y=0",
        "",
        "## Computed ledgers",
        "",
        "```json",
        json.dumps(payload["computed"], indent=2, sort_keys=True),
        "```",
        "",
        "The finite fixture checks branch inequalities, the equality cut, algebraic signs,",
        "and exact integer ledgers.  It is not proof of the continuum identities.",
        "The full clustered-sector flux payment and all regularity claims remain OPEN.",
        "**NOT CLAY.**",
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({
        "suite": SCHEMA,
        "verdict": verdict,
        "assertions": len(assertions),
        "mutations": len(NEGATIVE_MUTATIONS),
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
