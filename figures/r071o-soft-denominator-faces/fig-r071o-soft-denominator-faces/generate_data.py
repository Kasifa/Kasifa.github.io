#!/usr/bin/env python3
"""Generate deterministic source data for the R0.71O journal figure."""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import math
import platform
import time
from pathlib import Path


FIELDS = (
    "panel",
    "series",
    "case",
    "component",
    "order",
    "N",
    "x",
    "y",
    "value",
    "unit",
    "formula",
    "evidenceClass",
    "note",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(left: float, right: float, tolerance: float = 2.0e-11) -> bool:
    return abs(left - right) <= tolerance * max(1.0, abs(left), abs(right))


def add(
    rows: list[dict[str, str]],
    panel: str,
    series: str,
    *,
    case: str = "",
    component: str = "",
    order: int | str = "",
    frequency: int | str = "",
    x: float = 0.0,
    y: float = 0.0,
    value: float = 0.0,
    unit: str = "",
    formula: str = "",
    evidence: str = "",
    note: str = "",
) -> None:
    rows.append(
        {
            "panel": panel,
            "series": series,
            "case": case,
            "component": component,
            "order": str(order),
            "N": str(frequency),
            "x": f"{float(x):.17g}",
            "y": f"{float(y):.17g}",
            "value": f"{float(value):.17g}",
            "unit": unit,
            "formula": formula,
            "evidenceClass": evidence,
            "note": note,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--exact-certificate", type=Path, default=Path("exact-certificate.json")
    )
    parser.add_argument(
        "--independent-certificate",
        type=Path,
        default=Path("independent-certificate.json"),
    )
    parser.add_argument("--output", type=Path, default=Path("data.csv"))
    parser.add_argument(
        "--metadata", type=Path, default=Path("figure-data-metadata.json")
    )
    args = parser.parse_args()
    started = time.perf_counter()
    exact = json.loads(args.exact_certificate.read_text(encoding="utf-8"))
    independent = json.loads(
        args.independent_certificate.read_text(encoding="utf-8")
    )
    if exact.get("release") != "R0.71O" or exact.get("status") != "passed":
        raise RuntimeError("exact R0.71O certificate must pass")
    if (
        independent.get("release") != "R0.71O"
        or independent.get("status") != "passed"
    ):
        raise RuntimeError("independent R0.71O certificate must pass")

    rows: list[dict[str, str]] = []
    exact_face = "exact finite-order theorem"
    abstract = "exact abstract Hilbert-path separation; not NSE"
    nse_jet = "exact NSE initial jet; standalone FFT cross-check"

    # Panel A: normalized finite-order profiles.  The independent certificate
    # verifies the half-line derivative mass for orders 1 through 8; the plot
    # uses the first odd and second even cases.
    sample_count = 241
    for case, order in (("odd m=1, b>0", 1), ("even m=2, b>0", 2)):
        for index in range(sample_count):
            tau = -4.0 + 8.0 * index / (sample_count - 1)
            magnitude = abs(tau) ** (2 * order)
            profile = magnitude / (1.0 + magnitude)
            if order % 2 == 1 and tau < 0.0:
                profile = 0.0
            add(
                rows,
                "A",
                "softProfile",
                case=case,
                component="a_epsilon/A",
                order=order,
                x=tau,
                y=profile,
                value=profile,
                unit="normalized amplitude",
                formula="1_active_side*s^(2m)/(1+s^(2m))",
                evidence=exact_face,
                note="s=(t-t0)/delta_epsilon; A normalized to one",
            )
    for case, order, positive, negative in (
        ("odd m=1, b>0", 1, 1.0, 0.0),
        ("even m=2, b>0", 2, 1.0, 1.0),
    ):
        for component, value in (
            ("positiveAtom", positive),
            ("negativeAtom", negative),
        ):
            add(
                rows,
                "A",
                "faceAtom",
                case=case,
                component=component,
                order=order,
                value=value,
                unit="normalized atom mass",
                formula="A_plus or A_minus",
                evidence=exact_face,
                note="one-sided Jordan atom at t0",
            )

    # Panel B: the signed measure and the relaxed/Jordan ledger are different
    # when opposite layers collapse at the same even-order zero.
    for case, order, a_plus, a_minus in (
        ("odd m=1", 1, 1.0, 0.0),
        ("even m=2", 2, 1.0, 1.0),
    ):
        signed = a_plus - a_minus
        hard_jump = abs(signed)
        jordan = a_plus + a_minus
        defect = jordan - hard_jump
        metrics = (
            ("Aplus", a_plus, "A_plus"),
            ("Aminus", a_minus, "A_minus"),
            ("signedAtom", signed, "A_plus-A_minus"),
            ("hardBVJump", hard_jump, "abs(A_plus-A_minus)"),
            ("relaxedJordan", jordan, "A_plus+A_minus"),
            ("relaxationDefect", defect, "2*min(A_plus,A_minus)"),
        )
        for component, value, formula in metrics:
            add(
                rows,
                "B",
                "faceLedger",
                case=case,
                component=component,
                order=order,
                value=value,
                unit="normalized face mass",
                formula=formula,
                evidence=exact_face,
                note="standard hard BV and segmented soft relaxation are distinct",
            )

    # Panel C: exact oscillatory separation, cross-checked against the
    # independent quadrature rows.
    exact_samples = exact["checks"]["oscillatorySeparation"]["samples"]
    independent_rows = {
        int(row["N"]): row
        for row in independent["checks"]["oscillatoryPaths"]["rows"]
    }
    frequencies: list[int] = []
    for sample in exact_samples:
        frequency = int(sample["N"])
        frequencies.append(frequency)
        epsilon = frequency ** -4
        face_tv = 2.0 * frequency**3 / (frequency**2 + 1.0)
        denominator_mass = math.pi / frequency**2
        derivative_mass = math.pi
        check = independent_rows[frequency]
        if not close(0.5 * face_tv, float(check["positiveVariation"])):
            raise RuntimeError(f"independent variation mismatch at N={frequency}")
        if not close(denominator_mass, float(check["denominatorMass"])):
            raise RuntimeError(f"independent denominator mismatch at N={frequency}")
        if not close(derivative_mass, float(check["C_tSquareMass"])):
            raise RuntimeError(f"independent derivative mismatch at N={frequency}")
        for series, value, unit, formula, note in (
            (
                "softFaceTV",
                face_tv,
                "total variation",
                "2*N^3/(N^2+1)",
                "epsilon_N=N^(-4); asymptotic to 2*N",
            ),
            (
                "denominatorMass",
                denominator_mass,
                "time integral",
                "pi/N^2",
                "integral_0^(2*pi) d_N dt",
            ),
            (
                "CtSquareMass",
                derivative_mass,
                "time integral",
                "pi",
                "integral_0^(2*pi) ||C_(N,t)||^2 dt",
            ),
        ):
            add(
                rows,
                "C",
                series,
                case="C_N=N^(-1) sin(Nt)e",
                frequency=frequency,
                x=frequency,
                y=value,
                value=value,
                unit=unit,
                formula=formula,
                evidence=abstract,
                note=note,
            )

    # Panel D: exact Fourier modes and scalar initial-jet ledger.
    exact_nse = exact["checks"]["nseInitialFace"]
    independent_nse = independent["checks"]["nseInitialFace"]
    modes = exact_nse["initialFacts"]["F_modes"]
    for mode_text in sorted(modes):
        mode = ast.literal_eval(mode_text)
        if len(mode) != 3 or mode[2] != 0:
            raise RuntimeError(f"unexpected target mode {mode_text}")
        coefficient = modes[mode_text]
        add(
            rows,
            "D",
            "targetMode",
            case="filtered Lamb field",
            component=",".join(coefficient),
            x=float(mode[0]),
            y=float(mode[1]),
            value=0.25,
            unit="Fourier coefficient magnitude",
            formula="F_hat(k)=(0,0,+/- i/4)",
            evidence=nse_jet,
            note=f"k=({mode[0]},{mode[1]},0)",
        )
    metric_values = (
        ("targetModeCount", float(independent_nse["targetModeCount"]), "count"),
        ("Y0", float(independent_nse["Y0"]), "normalized enstrophy"),
        ("F2", float(independent_nse["F2"]), "squared L2 norm"),
        ("G2", float(independent_nse["G2"]), "squared L2 norm"),
        ("Ct2", float(independent_nse["CFirst2"]), "squared L2 norm"),
        ("Bt", float(independent_nse["BFirst"]), "initial derivative"),
        ("rightTrace", float(independent_nse["rightEntryTrace"]), "a(0+)"),
    )
    for index, (component, value, unit) in enumerate(metric_values):
        add(
            rows,
            "D",
            "nseMetric",
            case="one-sided initial jet",
            component=component,
            x=index,
            value=value,
            unit=unit,
            formula={
                "targetModeCount": "number of nonzero filtered Lamb modes",
                "Y0": "||omega_0||_2^2",
                "F2": "||F_j(0)||_2^2",
                "G2": "||curl F_j(0)||_2^2",
                "Ct2": "||C_(Q,t)(0)||_2^2",
                "Bt": "<F_j(0),C_(Q,t)(0)>",
                "rightTrace": "B_t(0)^2/(Y(0)*||C_(Q,t)(0)||_2^2)",
            }[component],
            evidence=nse_jet,
            note="exact symbolic result and zero-residual order-32 FFT cross-check",
        )
    add(
        rows,
        "D",
        "claimBoundary",
        case="one-sided initial jet",
        component="scope",
        evidence=nse_jet,
        note=exact_nse["claimBoundary"],
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "release": "R0.71O",
        "rows": len(rows),
        "profileSampleCountPerCase": sample_count,
        "frequencies": frequencies,
        "softDiagonal": "epsilon_N=N^(-4)",
        "exactCertificate": args.exact_certificate.name,
        "exactCertificateSha256": digest(args.exact_certificate),
        "independentCertificate": args.independent_certificate.name,
        "independentCertificateSha256": digest(args.independent_certificate),
        "independentImplementation": independent["implementation"],
        "independentAuditWallTimeSeconds": independent["wallSeconds"],
        "independentMaximumProfileMassError": independent["checks"][
            "innerProfiles"
        ]["maximumDerivativeMassError"],
        "independentMaximumVariationRelativeError": independent["checks"][
            "oscillatoryPaths"
        ]["maximumVariationRelativeError"],
        "independentNseMaximumResidual": independent_nse["maximumResidual"],
        "nseTargetModes": sorted(modes),
        "nseGridOrder": independent_nse["gridOrder"],
        "nseRightEntryTrace": independent_nse["rightEntryTrace"],
        "panelEvidence": {
            "A": exact_face,
            "B": exact_face,
            "C": abstract,
            "D": nse_jet,
        },
        "precision": (
            "exact SymPy algebra plus deterministic IEEE binary64 SciPy "
            "quadrature and order-32 NumPy FFT"
        ),
        "randomSeed": None,
        "dns": False,
        "pdeTimeStepping": False,
        "fittedData": False,
        "intervalCertified": False,
        "claimBoundary": (
            "Panel C is an abstract smooth Hilbert path, not a coupled NSE "
            "observable. Panel D is one one-sided smooth NSE initial jet, not "
            "a time step, internal or unbounded NSE face-count theorem, or "
            "failure of an NSE face estimate. No continuation, singularity, "
            "regularity, originality, or Millennium-problem claim is represented."
        ),
        "python": platform.python_version(),
        "dataGenerationWallTimeSeconds": time.perf_counter() - started,
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
