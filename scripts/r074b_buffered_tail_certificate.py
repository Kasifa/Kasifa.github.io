#!/usr/bin/env python3
"""Fail-closed finite certificate for the R0.74B bookkeeping ledger.

Only elementary finite algebra is certified here. The suitable-local-energy
argument, infinite sums, pressure estimates, and limiting arguments remain in
the analytic note and its independent audit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = Path(__file__).resolve()
SOURCE_PATH = ROOT / "research" / "r074b_buffered_tail_closure.md"
AUDIT_PATH = ROOT / "research" / "r074b_independent_audit.md"
LITERATURE_PATH = ROOT / "research" / "r074b_primary_literature_audit.md"
JSON_PATH = ROOT / "research" / "r074b_buffered_tail_certificate.json"
REPORT_PATH = ROOT / "research" / "r074b_buffered_tail_certificate_report.md"
FREEZE_MANIFEST_PATH = ROOT / "research" / "r074b_certificate_freeze.json"


def F(n: int, d: int = 1) -> Fraction:
    return Fraction(n, d)


def S(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def encode(x: Any) -> Any:
    if isinstance(x, Fraction):
        return S(x)
    if isinstance(x, dict):
        return {str(encode(k)): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(check_id: str, name: str, actual: Any, expected: Any, detail: str = "") -> dict[str, Any]:
    row = {
        "id": check_id,
        "name": name,
        "actual": encode(actual),
        "expected": encode(expected),
        "pass": actual == expected,
    }
    if detail:
        row["detail"] = detail
    return row


def annulus(m: int, scale: Fraction = F(1)) -> tuple[Fraction, Fraction]:
    """Endpoint ledger in units of R; null boundaries are immaterial."""
    return scale * F(2) ** m, scale * F(2) ** (m + 1)


def support_interval(m: int) -> tuple[Fraction, Fraction]:
    return F(2) ** m - F(1, 8), F(2) ** (m + 1) + F(1, 8)


def sparse_add(a: dict[Fraction, Fraction], b: dict[Fraction, Fraction]) -> dict[Fraction, Fraction]:
    out = dict(a)
    for exponent, coefficient in b.items():
        out[exponent] = out.get(exponent, F(0)) + coefficient
        if out[exponent] == 0:
            del out[exponent]
    return out


def sparse_mul(a: dict[Fraction, Fraction], b: dict[Fraction, Fraction]) -> dict[Fraction, Fraction]:
    out: dict[Fraction, Fraction] = {}
    for ea, ca in a.items():
        for eb, cb in b.items():
            out[ea + eb] = out.get(ea + eb, F(0)) + ca * cb
    return {e: c for e, c in out.items() if c}


def monomial_power(a: dict[Fraction, Fraction], exponent: Fraction) -> dict[Fraction, Fraction]:
    if len(a) != 1:
        raise ValueError("fractional power is only used on one unit-coefficient monomial")
    ((power, coefficient),) = a.items()
    if coefficient != 1:
        raise ValueError("non-unit coefficient is outside the exact sparse-power ledger")
    return {power * exponent: F(1)}


def sparse_rows(a: dict[Fraction, Fraction]) -> list[dict[str, str]]:
    return [
        {"nu_exponent": S(exponent), "coefficient": S(coefficient)}
        for exponent, coefficient in sorted(a.items())
    ]


def leaf_paths(value: Any, prefix: str = "") -> set[str]:
    """Treat lists as one displayed field and recurse through dictionaries."""
    if not isinstance(value, dict):
        return {prefix}
    out: set[str] = set()
    for key, child in value.items():
        child_prefix = f"{prefix}.{key}" if prefix else str(key)
        out.update(leaf_paths(child, child_prefix))
    return out


def build() -> dict[str, Any]:
    for path in (SOURCE_PATH, AUDIT_PATH, LITERATURE_PATH, SCRIPT_PATH, FREEZE_MANIFEST_PATH):
        if not path.is_file():
            raise FileNotFoundError(path)

    source_sha = sha256(SOURCE_PATH)
    audit_sha = sha256(AUDIT_PATH)
    literature_sha = sha256(LITERATURE_PATH)
    script_sha = sha256(SCRIPT_PATH)
    freeze_manifest_sha = sha256(FREEZE_MANIFEST_PATH)
    freeze_manifest = json.loads(FREEZE_MANIFEST_PATH.read_text(encoding="utf-8"))
    expected_hashes = freeze_manifest.get("expected_sha256", {})
    audit_text = AUDIT_PATH.read_text(encoding="utf-8")
    match = re.search(r"\*\*Audited source SHA256:\*\*\s*`([0-9a-f]{64})`", audit_text)
    audited_source_sha = match.group(1) if match else "MISSING"

    # NSE scaling convention: Q[u_lambda] = lambda^e Q[u].
    base = {
        "u": F(1), "grad_u": F(2), "p": F(2), "dx": F(-3),
        "dt": F(-2), "R": F(-1), "nu": F(0),
    }
    scaling = {
        "standard_clock": 2 * base["R"],
        "viscosity_clock": 2 * base["R"] - base["nu"],
        "U_ext": -base["R"] + base["dx"] + 2 * base["u"],
        "D_ext": base["nu"] - base["R"] + base["dt"] + base["dx"] + 2 * base["grad_u"],
        "E_endpoint": -base["R"] + base["dx"] + 2 * base["u"],
        "E_gradient": base["nu"] - base["R"] + base["dt"] + base["dx"] + 2 * base["grad_u"],
        "G_u": -2 * base["R"] + base["dt"] + base["dx"] + 3 * base["u"],
        "G_p": -2 * base["R"] + base["dt"] + base["dx"] + F(3, 2) * base["p"],
        "Lambda_R": base["R"] - 4 * base["R"] + base["dx"] + 2 * base["u"],
    }
    scaling["H_u"] = base["R"] + base["dt"] + F(3, 2) * scaling["Lambda_R"]
    scaling_expected = {
        "standard_clock": F(-2), "viscosity_clock": F(-2),
        "U_ext": F(0), "D_ext": F(0), "E_endpoint": F(0),
        "E_gradient": F(0), "G_u": F(0), "G_p": F(0),
        "Lambda_R": F(2), "H_u": F(0),
    }
    shell_scaling = {
        "R^-1_dx_u2": -base["R"] + base["dx"] + 2 * base["u"],
        "nu_R^-1_dt_dx_grad2": base["nu"] - base["R"] + base["dt"] + base["dx"] + 2 * base["grad_u"],
        "R^-3_dt_dx_u2": -3 * base["R"] + base["dt"] + base["dx"] + 2 * base["u"],
        "R^-2_dt_dx_u3": -2 * base["R"] + base["dt"] + base["dx"] + 3 * base["u"],
        "R^-2_dt_dx_p3over2": -2 * base["R"] + base["dt"] + base["dx"] + F(3, 2) * base["p"],
    }

    # Symbolic neighbor offsets d=-1,0,1 remove an arbitrary m cutoff.
    neighbor_offsets: dict[str, dict[str, Any]] = {}
    gaussian_exponent_ratios: dict[str, Fraction] = {}
    for offset in (-1, 0, 1):
        target_relative = annulus(offset, F(1))
        doubled_relative = annulus(offset - 1, F(2))
        neighbor_offsets[str(offset)] = {
            "R_endpoints_over_2^mR": encode(target_relative),
            "2R_endpoints_over_2^mR": encode(doubled_relative),
        }
        # beta_j/beta_m, j=m+offset-1; gamma_m <= gamma_j iff ratio <= 1.
        gaussian_exponent_ratios[str(offset)] = F(4) ** (offset - 1)

    core_ball_hi = F(4)
    outer_payment_hi = F(16)  # A_1(2R) union A_2(2R) = [4R,16R].
    core_geometry: dict[str, dict[str, Any]] = {}
    for m in (1, 2, 3):
        lo, hi = support_interval(m)
        row: dict[str, Any] = {
            "support": encode((lo, hi)),
            "intersects_B4R": lo < core_ball_hi,
        }
        if m <= 2:
            row["outside_core_covered"] = max(lo, core_ball_hi) >= core_ball_hi and hi <= outer_payment_hi
        core_geometry[str(m)] = row

    boundary_m = 4
    summability_delta = F(3 * 4 ** (boundary_m - 1), 32)
    exp6_partial_sum = F(1) + F(6) + F(6) ** 2 / F(2)

    # Amplitude degrees derived from u -> alpha u and p -> alpha^2 p.
    amp_u = F(1)
    amp_grad_u = amp_u
    amp_p = 2 * amp_u
    amplitude = {
        "E": 2 * amp_u,
        "E^(3/2)": F(3, 2) * (2 * amp_u),
        "Lambda_R": 2 * amp_u,
        "H_u": F(3, 2) * (2 * amp_u),
        "G_u": 3 * amp_u,
        "G_p": F(3, 2) * amp_p,
        "K_D": 2 * amp_grad_u + amp_u,
    }
    exterior_component_degrees = (amplitude["G_u"], amplitude["G_p"], amplitude["H_u"])
    if len(set(exterior_component_degrees)) != 1:
        raise ValueError("A_ext components do not have a common amplitude degree")
    amplitude["A_ext"] = exterior_component_degrees[0]
    payment_degrees = (amplitude["E^(3/2)"], amplitude["A_ext"])
    if len(set(payment_degrees)) != 1:
        raise ValueError("P summands do not have a common amplitude degree")
    amplitude["P"] = payment_degrees[0]
    amplitude["P^(2/3)"] = F(2, 3) * amplitude["P"]
    amplitude["(P^(2/3))^(3/2)"] = F(3, 2) * amplitude["P^(2/3)"]
    amplitude["P^(3/2)"] = F(3, 2) * amplitude["P"]

    # Exact-shear frequency ledger. Exact solvability and positive limits stay analytic.
    shear_u_n = F(0)
    shear_grad_n = shear_u_n + F(1)
    shear_heat_rate_n = 2 * (shear_grad_n - shear_u_n)
    shear_decay_time_n = -shear_heat_rate_n
    shear = {
        "endpoint_N": 2 * shear_u_n,
        "gradient_density_N": 2 * shear_grad_n,
        "heat_decay_rate_N": shear_heat_rate_n,
        "dissipation_time_N": shear_decay_time_n,
    }
    shear["D_ext_N"] = shear["gradient_density_N"] + shear["dissipation_time_N"]
    shear["cubic_payment_N"] = 3 * shear_u_n + shear_decay_time_n
    shear["H_u_N"] = F(3, 2) * (2 * shear_u_n) + shear_decay_time_n
    shear["U_amplitude"] = 2 * amp_u
    shear["D_amplitude"] = 2 * amp_grad_u
    shear["cubic_amplitude"] = 3 * amp_u
    shear["H_amplitude"] = F(3, 2) * (2 * amp_u)

    eta_margin = F(1, 6) - F(1, 8)

    def lambda_coefficient(scale: int, shell_index: int) -> Fraction:
        return F(scale) ** -3 * F(2) ** (-4 * shell_index)

    lambda_outer_ratios = [
        lambda_coefficient(1, m) / lambda_coefficient(2, m - 1)
        for m in range(2, 9)
    ]
    lambda_first_coefficient = lambda_coefficient(1, 1)
    lambda_first_r_power = F(1) - F(4)
    gauge_r_power = F(-2) + F(3)
    gauge_scaling = gauge_r_power * base["R"] + base["dt"] + F(3, 2) * base["p"]
    gauge_amplitude = F(3, 2) * amp_p
    doubled_normalization = F(1) ** -2 / (F(2) ** -2)

    nu_poly = {F(1): F(1)}
    kappa_standard = {F(0): F(1)}
    kappa_viscosity = dict(nu_poly)
    clock_standard = sparse_mul(
        sparse_add(kappa_standard, nu_poly),
        monomial_power(kappa_standard, F(-1, 3)),
    )
    clock_viscosity = sparse_mul(
        sparse_add(kappa_viscosity, nu_poly),
        monomial_power(kappa_viscosity, F(-1, 3)),
    )

    checks: list[dict[str, Any]] = []
    for index, key in enumerate(scaling, 1):
        checks.append(check(f"SC{index:02d}", f"{key} NSE scaling", scaling[key], scaling_expected[key]))
    for index, (key, value) in enumerate(shell_scaling.items(), 1):
        checks.append(check(f"SH{index:02d}", f"single-shell {key}", value, F(0)))
    for offset in (-1, 0, 1):
        row = neighbor_offsets[str(offset)]
        checks.append(check(
            f"AN{offset + 2:02d}", f"annular endpoint shift offset {offset}",
            row["R_endpoints_over_2^mR"], row["2R_endpoints_over_2^mR"],
        ))
        checks.append(check(
            f"GW{offset + 2:02d}", f"Gaussian payment exponent ratio offset {offset}",
            gaussian_exponent_ratios[str(offset)],
            {-1: F(1, 16), 0: F(1, 4), 1: F(1)}[offset],
            "beta_payment/beta_target; each exact ratio is at most one",
        ))
    checks.extend([
        check("CG01", "m=1 exact cutoff support", core_geometry["1"]["support"], ["15/8", "33/8"]),
        check("CG02", "m=2 exact cutoff support", core_geometry["2"]["support"], ["31/8", "65/8"]),
        check("CG03", "m=3 exact cutoff support", core_geometry["3"]["support"], ["63/8", "129/8"]),
        check("CO01", "m=1 support intersects B4R", core_geometry["1"]["intersects_B4R"], True),
        check("CO02", "m=2 support intersects B4R", core_geometry["2"]["intersects_B4R"], True),
        check("CO03", "m=3 is outside B4R", core_geometry["3"]["intersects_B4R"], False),
        check("CO04", "m=1 exterior support covered at 2R", core_geometry["1"]["outside_core_covered"], True),
        check("CO05", "m=2 exterior support covered at 2R", core_geometry["2"]["outside_core_covered"], True),
        check("SU01", "summability exponent at m=4", summability_delta, F(6)),
        check("SU02", "finite exp(6) lower bound exceeds 16", exp6_partial_sum > 16, True, f"partial sum={S(exp6_partial_sum)}"),
        check("PV01", "freeze manifest binds analytic source SHA256", source_sha, expected_hashes.get("analytic_source")),
        check("PV02", "independent audit embeds current source SHA256", audited_source_sha, source_sha),
        check("PV03", "freeze manifest binds independent audit SHA256", audit_sha, expected_hashes.get("independent_audit")),
        check("PV04", "freeze manifest binds literature audit SHA256", literature_sha, expected_hashes.get("literature_audit")),
        check("PV05", "freeze manifest binds certificate script SHA256", script_sha, expected_hashes.get("certificate_script")),
        check("AM01", "E amplitude degree", amplitude["E"], F(2)),
        check("AM02", "E^(3/2) amplitude degree", amplitude["E^(3/2)"], F(3)),
        check("AM03", "A_ext common amplitude degree", amplitude["A_ext"], F(3)),
        check("AM04", "P common amplitude degree", amplitude["P"], F(3)),
        check("AM05", "P^(2/3) amplitude degree", amplitude["P^(2/3)"], F(2)),
        check("AM06", "small-P K composition degree", amplitude["(P^(2/3))^(3/2)"], F(3)),
        check("AM07", "large P^(3/2) degree", amplitude["P^(3/2)"], F(9, 2)),
        check("AM08", "K_D amplitude degree", amplitude["K_D"], F(3)),
        check("AM09", "Lambda amplitude degree", amplitude["Lambda_R"], F(2)),
        check("AM10", "exterior component amplitude degrees", exterior_component_degrees, (F(3), F(3), F(3))),
        check("EX01", "shear endpoint N exponent", shear["endpoint_N"], F(0)),
        check("EX02", "shear gradient-density N exponent", shear["gradient_density_N"], F(2)),
        check("EX08", "shear heat-decay rate N exponent", shear["heat_decay_rate_N"], F(2)),
        check("EX03", "shear decay-time N exponent", shear["dissipation_time_N"], F(-2)),
        check("EX04", "shear D N exponent", shear["D_ext_N"], F(0)),
        check("EX05", "shear cubic N exponent", shear["cubic_payment_N"], F(-2)),
        check("EX06", "shear H N exponent", shear["H_u_N"], F(-2)),
        check("EX07", "shear amplitude degrees", tuple(shear[k] for k in ("U_amplitude", "D_amplitude", "cubic_amplitude", "H_amplitude")), (F(2), F(2), F(3), F(3))),
        check("ET01", "eta/gamma exponent margin", eta_margin, F(1, 24)),
        check("PR01", "Lambda outer doubled-radius coefficient", tuple(lambda_outer_ratios), tuple(F(1, 2) for _ in lambda_outer_ratios)),
        check("PR02", "Lambda first-shell coefficient and R power", (lambda_first_coefficient, lambda_first_r_power), (F(1, 16), F(-3))),
        check("PR03", "H_R scaling and amplitude degree", (scaling["H_u"], amplitude["H_u"]), (F(0), F(3))),
        check("PR04", "gauge-volume algebraic R power", gauge_r_power, F(1)),
        check("PR05", "gauge-volume NSE scaling", gauge_scaling, F(0)),
        check("PR06", "gauge-volume amplitude degree", gauge_amplitude, F(3)),
        check("PR07", "G_u/G_p doubled normalization", doubled_normalization, F(4)),
        check("PR08", "A_ext scaling and amplitude degree", (scaling["G_u"], scaling["G_p"], scaling["H_u"], amplitude["A_ext"]), (F(0), F(0), F(0), F(3))),
        check("PR09", "pressure-Q branch degrees", (amplitude["P"], amplitude["P^(3/2)"], amplitude["(P^(2/3))^(3/2)"]), (F(3), F(9, 2), F(3))),
        check("CL01", "standard clock coefficient", sparse_rows(clock_standard), [{"nu_exponent": "0", "coefficient": "1"}, {"nu_exponent": "1", "coefficient": "1"}]),
        check("CL02", "viscosity clock coefficient", sparse_rows(clock_viscosity), [{"nu_exponent": "2/3", "coefficient": "2"}]),
    ])

    provenance = {
        "source_path": str(SOURCE_PATH.relative_to(ROOT)),
        "source_sha256": source_sha,
        "audit_path": str(AUDIT_PATH.relative_to(ROOT)),
        "audit_sha256": audit_sha,
        "audit_embedded_source_sha256": audited_source_sha,
        "literature_audit_path": str(LITERATURE_PATH.relative_to(ROOT)),
        "literature_audit_sha256": literature_sha,
        "script_path": str(SCRIPT_PATH.relative_to(ROOT)),
        "script_sha256": script_sha,
        "freeze_manifest_path": str(FREEZE_MANIFEST_PATH.relative_to(ROOT)),
        "freeze_manifest_sha256": freeze_manifest_sha,
    }
    derived = {
        "NSE_scaling": encode(scaling),
        "single_shell_scaling": encode(shell_scaling),
        "annular_geometry": {
            "neighbor_offsets": neighbor_offsets,
            "gaussian_exponent_ratios": encode(gaussian_exponent_ratios),
            "core_geometry": core_geometry,
        },
        "summability_boundary": {
            "boundary_m": boundary_m,
            "delta": S(summability_delta),
            "exp6_finite_lower_bound": S(exp6_partial_sum),
            "boundary": "Finite boundary arithmetic only; uniform infinite summability remains analytic.",
        },
        "amplitude_homogeneity": encode(amplitude),
        "dissipating_shear": encode(shear),
        "eta_margin": S(eta_margin),
        "pressure_radius_ledger": {
            "Lambda_outer_ratios": encode(lambda_outer_ratios),
            "Lambda_first_shell": {"coefficient": S(lambda_first_coefficient), "R_power": S(lambda_first_r_power)},
            "gauge_volume": {"algebraic_R_power": S(gauge_r_power), "NSE_scaling": S(gauge_scaling), "amplitude_degree": S(gauge_amplitude)},
            "doubled_normalization": S(doubled_normalization),
        },
        "clock_coefficients": {
            "formula": "(kappa+nu) kappa^(-1/3)",
            "standard": sparse_rows(clock_standard),
            "viscosity": sparse_rows(clock_viscosity),
        },
    }
    analytic_boundary = [
        "periodized suitable test admissibility",
        "finite-M to infinite-shell limit",
        "uniform-theta infinite summability",
        "weighted Holder inequality",
        "Calderon-Zygmund and harmonic pressure estimates",
        "gauge transfer inequality",
        "exact NSE status and Riemann-Lebesgue positive limits for the shear",
    ]

    coverage_subject = {
        "provenance": provenance,
        "base_scaling_exponents": encode(base),
        "derived": derived,
        "analytic_boundary": analytic_boundary,
    }
    field_coverage: dict[str, dict[str, Any]] = {}

    def cover(path: str, mode: str, *check_ids: str) -> None:
        if path in field_coverage:
            raise ValueError(f"duplicate field coverage: {path}")
        field_coverage[path] = {"mode": mode, "check_ids": list(check_ids)}

    for path in ("source_path", "audit_path", "literature_audit_path", "script_path", "freeze_manifest_path"):
        cover(f"provenance.{path}", "RUNTIME_PATH_GATE")
    cover("provenance.source_sha256", "CHECK", "PV01", "PV02")
    cover("provenance.audit_sha256", "CHECK", "PV03")
    cover("provenance.audit_embedded_source_sha256", "CHECK", "PV02")
    cover("provenance.literature_audit_sha256", "CHECK", "PV04")
    cover("provenance.script_sha256", "CHECK", "PV05")
    cover("provenance.freeze_manifest_sha256", "VERSION_CONTROL_BOUNDARY")
    for key in base:
        cover(f"base_scaling_exponents.{key}", "PRIMITIVE_INPUT")
    for index, key in enumerate(scaling, 1):
        extra = ()
        if key == "H_u":
            extra = ("PR03", "PR08")
        elif key in ("G_u", "G_p"):
            extra = ("PR08",)
        cover(f"derived.NSE_scaling.{key}", "CHECK", f"SC{index:02d}", *extra)
    for index, key in enumerate(shell_scaling, 1):
        cover(f"derived.single_shell_scaling.{key}", "CHECK", f"SH{index:02d}")
    for offset in (-1, 0, 1):
        annulus_id = f"AN{offset + 2:02d}"
        cover(f"derived.annular_geometry.neighbor_offsets.{offset}.R_endpoints_over_2^mR", "CHECK", annulus_id)
        cover(f"derived.annular_geometry.neighbor_offsets.{offset}.2R_endpoints_over_2^mR", "CHECK", annulus_id)
        cover(f"derived.annular_geometry.gaussian_exponent_ratios.{offset}", "CHECK", f"GW{offset + 2:02d}")
    for m, support_id, core_id in ((1, "CG01", "CO01"), (2, "CG02", "CO02"), (3, "CG03", "CO03")):
        cover(f"derived.annular_geometry.core_geometry.{m}.support", "CHECK", support_id)
        cover(f"derived.annular_geometry.core_geometry.{m}.intersects_B4R", "CHECK", core_id)
    cover("derived.annular_geometry.core_geometry.1.outside_core_covered", "CHECK", "CO04")
    cover("derived.annular_geometry.core_geometry.2.outside_core_covered", "CHECK", "CO05")
    cover("derived.summability_boundary.boundary_m", "CHECK", "SU01")
    cover("derived.summability_boundary.delta", "CHECK", "SU01")
    cover("derived.summability_boundary.exp6_finite_lower_bound", "CHECK", "SU02")
    cover("derived.summability_boundary.boundary", "ANALYTIC_BOUNDARY")
    amplitude_coverage = {
        "E": ("AM01",), "E^(3/2)": ("AM02",), "Lambda_R": ("AM09",),
        "H_u": ("AM10", "PR03"), "G_u": ("AM10",), "G_p": ("AM10",),
        "K_D": ("AM08",), "A_ext": ("AM03", "AM10", "PR08"),
        "P": ("AM04", "PR09"), "P^(2/3)": ("AM05",),
        "(P^(2/3))^(3/2)": ("AM06", "PR09"), "P^(3/2)": ("AM07", "PR09"),
    }
    for key, ids in amplitude_coverage.items():
        cover(f"derived.amplitude_homogeneity.{key}", "CHECK", *ids)
    shear_coverage = {
        "endpoint_N": "EX01", "gradient_density_N": "EX02", "heat_decay_rate_N": "EX08",
        "dissipation_time_N": "EX03", "D_ext_N": "EX04", "cubic_payment_N": "EX05", "H_u_N": "EX06",
        "U_amplitude": "EX07", "D_amplitude": "EX07", "cubic_amplitude": "EX07", "H_amplitude": "EX07",
    }
    for key, check_id in shear_coverage.items():
        cover(f"derived.dissipating_shear.{key}", "CHECK", check_id)
    cover("derived.eta_margin", "CHECK", "ET01")
    cover("derived.pressure_radius_ledger.Lambda_outer_ratios", "CHECK", "PR01")
    cover("derived.pressure_radius_ledger.Lambda_first_shell.coefficient", "CHECK", "PR02")
    cover("derived.pressure_radius_ledger.Lambda_first_shell.R_power", "CHECK", "PR02")
    cover("derived.pressure_radius_ledger.gauge_volume.algebraic_R_power", "CHECK", "PR04")
    cover("derived.pressure_radius_ledger.gauge_volume.NSE_scaling", "CHECK", "PR05")
    cover("derived.pressure_radius_ledger.gauge_volume.amplitude_degree", "CHECK", "PR06")
    cover("derived.pressure_radius_ledger.doubled_normalization", "CHECK", "PR07")
    cover("derived.clock_coefficients.formula", "DECLARED_FORMULA")
    cover("derived.clock_coefficients.standard", "CHECK", "CL01")
    cover("derived.clock_coefficients.viscosity", "CHECK", "CL02")
    cover("analytic_boundary", "ANALYTIC_BOUNDARY")

    all_ids = [row["id"] for row in checks]
    all_names = [row["name"] for row in checks]
    if len(all_ids) != len(set(all_ids)) or len(all_names) != len(set(all_names)):
        raise ValueError("duplicate certificate check id or name")
    subject_paths = leaf_paths(coverage_subject)
    allowed_modes = {
        "CHECK", "RUNTIME_PATH_GATE", "VERSION_CONTROL_BOUNDARY",
        "PRIMITIVE_INPUT", "ANALYTIC_BOUNDARY", "DECLARED_FORMULA",
    }
    future_check_ids = set(all_ids) | {"MT01"}
    field_coverage["__coverage_meta__"] = {"mode": "CHECK", "check_ids": ["MT01"]}
    covered_check_ids = {
        check_id
        for entry in field_coverage.values()
        for check_id in entry["check_ids"]
    }
    coverage_ok = (
        set(field_coverage) - {"__coverage_meta__"} == subject_paths
        and {entry["mode"] for entry in field_coverage.values()} <= allowed_modes
        and covered_check_ids == future_check_ids
        and all(entry["check_ids"] for entry in field_coverage.values() if entry["mode"] == "CHECK")
        and all(not entry["check_ids"] for entry in field_coverage.values() if entry["mode"] != "CHECK")
    )
    checks.append(check("MT01", "field-level coverage manifest is complete", coverage_ok, True))
    if {row["id"] for row in checks} != future_check_ids:
        raise ValueError("coverage meta-check did not bind the final check set")
    coverage_manifest = {
        "field_coverage": field_coverage,
        "subject_field_count": len(subject_paths),
        "noncheck_modes_are_explicit": True,
    }

    return {
        "certificate": "R0.74B buffered-tail derived finite exact-arithmetic certificate",
        "schema_version": 3,
        "status": "PASS" if all(row["pass"] for row in checks) else "FAIL",
        "scope": "FINITE derived arithmetic only; analytic inequalities, infinite quantifiers, suitable-weak limits, pressure estimates, and Riemann-Lebesgue positivity remain in the proof; NOT CLAY",
        "convention": "Q[u_lambda]=lambda^e Q[u] on correspondingly rescaled domains",
        "provenance": provenance,
        "base_scaling_exponents": encode(base),
        "derived": derived,
        "coverage_manifest": coverage_manifest,
        "analytic_boundary": analytic_boundary,
        "checks": checks,
        "summary": {"passed": sum(row["pass"] for row in checks), "total": len(checks)},
    }


def json_text(certificate: dict[str, Any]) -> str:
    return json.dumps(certificate, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def report_text(certificate: dict[str, Any]) -> str:
    derived = certificate["derived"]
    provenance = certificate["provenance"]
    lines = [
        "# R0.74B buffered-tail derived finite certificate", "",
        f"**Status:** {certificate['status']}", "",
        "**Scope:** `FINITE_DERIVED_EXACT_ARITHMETIC_ONLY`", "",
        "Every executable actual value below is derived from primitive exponents, interval endpoints, or file bytes before comparison with its declared target. The certificate contains no literal `pass=True` annular/core rows.", "",
        "## Frozen provenance", "",
        f"- Analytic source SHA256: `{provenance['source_sha256']}`",
        f"- Independent audit SHA256: `{provenance['audit_sha256']}`",
        f"- Literature audit SHA256: `{provenance['literature_audit_sha256']}`",
        f"- Certificate script SHA256: `{provenance['script_sha256']}`",
        f"- External freeze-manifest SHA256: `{provenance['freeze_manifest_sha256']}`",
        "- The external manifest freezes the source, audit, literature-audit, and script hashes. The source SHA embedded in the independent audit must also equal the current analytic source SHA.",
        "- The manifest cannot freeze its own bytes without circularity; its immutability is a version-control and frozen-commit review boundary.", "",
        "## NSE scaling", "", "| Quantity | Derived exponent |", "|---|---:|",
    ]
    lines.extend(f"| {key} | {value} |" for key, value in derived["NSE_scaling"].items())
    lines.extend([
        "", "## Annular and core geometry", "",
        "The three relative neighbor offsets `-1,0,1` are checked by endpoint equality against the corresponding doubled-radius offsets `-2,-1,0`. Their payment-to-target Gaussian exponent ratios are exactly `1/16,1/4,1`.", "",
        "The cutoff supports are computed as `[2^m-1/8, 2^(m+1)+1/8]R`. Both `m=1` and `m=2` intersect `B_(4R)` and their exterior portions lie in `A_1(2R) union A_2(2R)`; the `m=3` boundary row is already outside the core.", "",
        "The finite summability boundary gives delta `6` at `m=4`; the exact truncated exponential lower bound is `1+6+18=25>16`, sufficient for the analytic ratio bound below `1/2`. The infinite-tail quantifier remains analytic.", "",
        "## Amplitude composition", "", "| Item | Derived degree |", "|---|---:|",
    ])
    lines.extend(f"| {key} | {value} |" for key, value in derived["amplitude_homogeneity"].items())
    lines.extend([
        "", "## Pressure, clocks, and exact-shear exponent ledger", "",
        "The Lambda first-shell coefficient and R power are derived as `(1/16,-3)`; every sampled outer Lambda ratio is derived as `1/2`; the Gaussian pressure/velocity normalization is `4`; and the gauge-volume row derives `-2+3=1` before time and pressure scaling return the NSE exponent to zero.", "",
        "Sparse exact polynomials in the viscosity exponent derive the clock factors from `(kappa+nu) kappa^(-1/3)`: `1+nu` for the standard clock and `2 nu^(2/3)` for the viscosity clock.", "",
        "The shear ledger derives endpoint, gradient-density, decay-time, dissipation, cubic, and harmonic frequency exponents from `grad u:N^1` and `integral exp(-c nu N^2 t)dt:N^-2`. Exact solvability and positive Riemann-Lebesgue limits remain analytic.", "",
        "## Result", "",
        f"All {certificate['summary']['total']} derived finite checks pass. The field-level coverage manifest accounts for {certificate['coverage_manifest']['subject_field_count']} displayed subject fields plus its own meta-check, and the external hash gates pass.", "",
        "## Analytic boundary", "",
    ])
    lines.extend(f"- {item}." for item in certificate["analytic_boundary"])
    lines.extend([
        "- Removal of the `+P` term for large `P` remains OPEN.",
        "- No absorption, epsilon regularity, or global regularity follows.",
        "- NOT CLAY.", "",
    ])
    return "\n".join(lines)


def check_only(certificate: dict[str, Any]) -> int:
    bad: list[str] = []
    if not JSON_PATH.exists() or JSON_PATH.read_text(encoding="utf-8") != json_text(certificate):
        bad.append(str(JSON_PATH))
    if not REPORT_PATH.exists() or REPORT_PATH.read_text(encoding="utf-8") != report_text(certificate):
        bad.append(str(REPORT_PATH))
    if certificate["status"] != "PASS":
        bad.append("internal status")
    if bad:
        print("R0.74B certificate check failed: " + ", ".join(bad), file=sys.stderr)
        return 1
    summary = certificate["summary"]
    print(f"R0.74B derived certificate PASS: {summary['passed']}/{summary['total']} checks; hashes and artifacts identical")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--print-json", action="store_true")
    parser.add_argument("--print-report", action="store_true")
    args = parser.parse_args()
    certificate = build()
    if args.print_json:
        sys.stdout.write(json_text(certificate))
        return 0
    if args.print_report:
        sys.stdout.write(report_text(certificate))
        return 0
    if args.check_only:
        return check_only(certificate)
    JSON_PATH.write_text(json_text(certificate), encoding="utf-8")
    REPORT_PATH.write_text(report_text(certificate), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
