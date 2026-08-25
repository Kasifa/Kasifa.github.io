#!/usr/bin/env python3
"""Generate deterministic source data for the R0.71N journal figure."""

from __future__ import annotations

import argparse
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
    "witness",
    "stage",
    "component",
    "x",
    "value",
    "unit",
    "formula",
    "evidenceClass",
    "note",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(
    rows,
    panel,
    series,
    *,
    witness="",
    stage="",
    component="",
    x=0.0,
    value=0.0,
    unit="",
    formula="",
    evidence="",
    note="",
):
    rows.append(
        {
            "panel": panel,
            "series": series,
            "witness": witness,
            "stage": stage,
            "component": component,
            "x": f"{float(x):.17g}",
            "value": f"{float(value):.17g}",
            "unit": unit,
            "formula": formula,
            "evidenceClass": evidence,
            "note": note,
        }
    )


def order_result(independent, label, order=64):
    selected = [
        row for row in independent["witnesses"][label]
        if int(row["order"]) == order
    ]
    if len(selected) != 1:
        raise RuntimeError(f"expected one order-{order} result for {label}")
    return selected[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exact-certificate", type=Path, required=True)
    parser.add_argument("--independent-certificate", type=Path, required=True)
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
    if exact["release"] != "R0.71N" or exact["status"] != "passed":
        raise RuntimeError("exact R0.71N certificate must pass")
    if independent["release"] != "R0.71N" or independent["status"] != "passed":
        raise RuntimeError("independent R0.71N certificate must pass")

    rows = []
    exact_evidence = "exact fixed-cell theorem"
    diagnostic = "finite-Fourier diagnostic; not interval theorem"
    scaling_evidence = "exact NSE co-scaling ledger"

    stages = (
        (
            "complete derivative",
            "J=(B_t+lambda*B-0.5*B*(Y_t/Y+d_t/d))/sqrt(Y*d)",
            "retain B_t, d_t, and Y_t together",
        ),
        (
            "square plus residual",
            "J=(P_square+R)/sqrt(Y*d)",
            "P_square is nonnegative; R is signed",
        ),
        (
            "local enstrophy substitution",
            "B=e_t+nu*D_chi; R=-P_square+K",
            "the same positive square cancels exactly",
        ),
        (
            "signed second jet",
            "J=K/sqrt(Y*d)",
            "K has no sign or Leray-energy bound here",
        ),
    )
    for index, (stage, formula, note) in enumerate(stages):
        add(
            rows,
            "A",
            "structureFlow",
            stage=stage,
            x=index,
            value=index,
            formula=formula,
            evidence=exact_evidence,
            note=note,
        )

    witness_map = (
        ("positiveJ_seed49", "seed 49"),
        ("negativeJ_seed5", "seed 5"),
    )
    witness_metadata = {}
    for label, display in witness_map:
        result = order_result(independent, label)
        cell = result["cell"]
        fusion = result["signedFusion"]
        j_value = float(result["J"]["direct"])
        p_square = float(fusion["positiveSquare"])
        residual = float(fusion["signedResidual"])
        total = p_square + residual
        root = math.sqrt(float(cell["Y"]) * float(cell["d"]))
        add(
            rows,
            "B",
            "positiveSquare",
            witness=display,
            component="P_square",
            x=0,
            value=p_square,
            unit="raw numerator",
            formula="integral chi*|G+(nu/2)H|^2",
            evidence=diagnostic,
            note="nonnegative exact component evaluated in binary64",
        )
        add(
            rows,
            "B",
            "signedResidual",
            witness=display,
            component="R",
            x=1,
            value=residual,
            unit="raw numerator",
            formula="<G_t,chi W>-(nu^2/4)int chi|H|^2-(B/2)(Y_t/Y+d_t/d)",
            evidence=diagnostic,
            note="signed component",
        )
        add(
            rows,
            "B",
            "numeratorTotal",
            witness=display,
            component="P_square+R",
            x=2,
            value=total,
            unit="raw numerator",
            formula="P_square+R",
            evidence=diagnostic,
            note="diamond marker in Panel B",
        )
        add(
            rows,
            "B",
            "normalizerRoot",
            witness=display,
            component="sqrt(Y*d)",
            x=3,
            value=root,
            unit="normalizer",
            formula="sqrt(Y*d)",
            evidence=diagnostic,
            note="not plotted; retained for audit",
        )
        add(
            rows,
            "C",
            "z",
            witness=display,
            component="z",
            x=0,
            value=float(cell["z"]),
            unit="normalized pairing",
            formula="B/sqrt(Y*d)",
            evidence=diagnostic,
            note="strictly positive in both witnesses",
        )
        add(
            rows,
            "C",
            "J",
            witness=display,
            component="J",
            x=1,
            value=j_value,
            unit="complete scalar source",
            formula="z_t+nu*kappa^2*z",
            evidence=diagnostic,
            note="opposite signs across the two witnesses",
        )
        witness_metadata[display] = {
            "certificateLabel": label,
            "gridOrder": int(result["order"]),
            "z": float(cell["z"]),
            "positiveSquare": p_square,
            "signedResidual": residual,
            "numeratorTotal": total,
            "rootYd": root,
            "J": j_value,
            "maxJRepresentationRelativeResidual": float(
                result["checks"]["maxJRepresentationRelativeResidual"]
            ),
            "squareCancellationRelativeResidual": float(
                result["checks"]["squareCancellationRelativeResidual"]
            ),
        }

    scaling = exact["checks"]["scalingLedger"]
    scaling_rows = (
        ("numerator", float(scaling["numeratorExponents"]["acceleration"]), "P_square and R"),
        ("root", float(scaling["rootExponent"]), "sqrt(Y*d)"),
        ("J", float(scaling["JExponent"]), "numerator/root"),
        (
            "weighted creation",
            float(scaling["kappaMinus2_z_J_dt_Exponent"]),
            "kappa^-2*z*J*dt",
        ),
    )
    for index, (component, exponent, formula) in enumerate(scaling_rows):
        add(
            rows,
            "D",
            "scalingExponent",
            stage=component,
            component=component,
            x=index,
            value=exponent,
            unit="NSE scaling exponent",
            formula=formula,
            evidence=scaling_evidence,
            note="local co-scaling; not a continuous fixed-torus symmetry",
        )
    add(
        rows,
        "D",
        "nextGate",
        stage="R0.71O face gate",
        component="hard/soft denominator face",
        x=4,
        value=0,
        unit="route marker",
        formula="d_Q downarrow 0: compare hard components with soft regularization",
        evidence="declared next finite gate",
        note="no face estimate is asserted in R0.71N",
    )

    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    resolution_maximum = max(
        float(value["maximumRelativeResidual"])
        for value in independent["resolutionAgreement"].values()
    )
    metadata = {
        "release": "R0.71N",
        "rows": len(rows),
        "exactCertificate": str(args.exact_certificate),
        "exactCertificateSha256": digest(args.exact_certificate),
        "independentCertificate": str(args.independent_certificate),
        "independentCertificateSha256": digest(args.independent_certificate),
        "gridOrders": independent["configuration"]["gridOrders"],
        "selectedGridOrder": 64,
        "kappa": independent["configuration"]["kappa"],
        "viscosity": independent["configuration"]["viscosity"],
        "witnesses": witness_metadata,
        "resolutionMaximumRelativeResidual": resolution_maximum,
        "precision": "exact symbolic algebra plus deterministic IEEE binary64 finite Fourier initial jets",
        "python": platform.python_version(),
        "randomSeed": None,
        "labelsRetainExploratorySeedIdentifiers": True,
        "dns": False,
        "pdeTimeStepping": False,
        "fittedData": False,
        "intervalCertified": False,
        "wallTimeSeconds": time.perf_counter() - started,
        "panelEvidence": {
            "A": exact_evidence,
            "B": diagnostic,
            "C": diagnostic,
            "D": "exact scaling ledger plus declared next finite gate",
        },
        "claimBoundary": (
            "Panels B-C are deterministic alias-safe finite-Fourier initial-jet "
            "diagnostics, not interval theorems. Panel A is exact fixed-cell "
            "algebra and Panel D is an exact local co-scaling ledger plus a "
            "declared next gate. No no-go, continuation, regularity, singularity, "
            "originality, or Millennium-problem conclusion is represented."
        ),
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
