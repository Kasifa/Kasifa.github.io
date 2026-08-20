#!/usr/bin/env python3
"""Extract R0.68B-2f/g/h figure data from pinned certificates."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import resource
import time
from decimal import Decimal, localcontext
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MOMENT = ROOT / "research/certificates/r068b2f-moments/moment-enclosure.json"
HEAT = ROOT / "research/certificates/r068b2g-heat-jet/heat-jet.json"
DEFECT = ROOT / "research/certificates/r068b2h-corrected-heat/defect-sign.json"
VERIFICATION = (
    ROOT
    / "research/certificates/r068b2h-corrected-heat/independent-verification.json"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_decimal(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(), parse_float=Decimal)


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def main() -> None:
    started = time.perf_counter()
    moment = load_decimal(MOMENT)
    heat = load_decimal(HEAT)
    defect = load_decimal(DEFECT)
    verification = json.loads(VERIFICATION.read_text())

    write_rows(
        HERE / "moment-radius-by-degree.csv",
        ["degree", "channels", "maximumRadius", "centredGlobalMaximumRadius"],
        [
            {
                "degree": row["degree"],
                "channels": row["channels"],
                "maximumRadius": row["maximumRadius"],
                "centredGlobalMaximumRadius": moment["centredMaximumRadius"],
            }
            for row in moment["degrees"]
        ],
    )

    write_rows(
        HERE / "heat-partial-by-degree.csv",
        ["degree", "centre", "radius", "lower", "upper", "centreTimes1e8"],
        [
            {
                **row,
                "centreTimes1e8": row["centre"] * Decimal(10**8),
            }
            for row in heat["partialByDegree"]
        ],
    )

    heat_magnitude = -defect["heatJet"]["upper"]
    correction = defect["derivativeCorrectionUpper"]
    strict_margin = -defect["correctedDominantHeat"]["upper"]
    with localcontext() as context:
        context.prec = 50
        arithmetic_margin = heat_magnitude - correction
    write_rows(
        HERE / "sign-budget.csv",
        ["component", "value", "valueTimes1e8", "boundDirection", "evidence"],
        [
            {
                "component": "heat magnitude",
                "value": heat_magnitude,
                "valueTimes1e8": heat_magnitude * Decimal(10**8),
                "boundDirection": "lower",
                "evidence": "guarded heat jet",
            },
            {
                "component": "defect correction",
                "value": correction,
                "valueTimes1e8": correction * Decimal(10**8),
                "boundDirection": "upper",
                "evidence": "signature defect and resolvent",
            },
            {
                "component": "strict margin",
                "value": strict_margin,
                "valueTimes1e8": strict_margin * Decimal(10**8),
                "boundDirection": "lower",
                "evidence": "negative corrected upper endpoint",
            },
        ],
    )

    summary = [{
        "momentCoordinates": moment["totalCoordinates"],
        "momentMaximumDegree": moment["maximumDegree"],
        "centredMaximumRadius": moment["centredMaximumRadius"],
        "heatChannels": heat["parameters"]["channels"],
        "heatJetCentre": defect["heatJet"]["centre"],
        "signatureClasses": defect["parameters"]["signatureClasses"],
        "coveredFreeShifts": defect["parameters"]["coveredFreeShifts"],
        "correctionUpper": correction,
        "strictMargin": strict_margin,
        "arithmeticMarginFromSerializedBounds": arithmetic_margin,
        "correctedLower": defect["correctedDominantHeat"]["lower"],
        "correctedUpper": defect["correctedDominantHeat"]["upper"],
        "independentVerificationStatus": verification["status"],
    }]
    write_rows(HERE / "certified-summary.csv", list(summary[0]), summary)

    metadata = {
        "momentCertificate": str(MOMENT.relative_to(ROOT)),
        "momentSha256": digest(MOMENT),
        "momentSourceCommit": moment["provenance"]["sourceCommit"],
        "momentArchiveCommit": "e44246b5e7a16527698d7a914ca2a4435b548a72",
        "heatCertificate": str(HEAT.relative_to(ROOT)),
        "heatSha256": digest(HEAT),
        "heatSourceCommit": heat["provenance"]["sourceCommit"],
        "heatArchiveCommit": "0b4b1524eb0e9d320f574fbd154b63464ef70c90",
        "defectCertificate": str(DEFECT.relative_to(ROOT)),
        "defectSha256": digest(DEFECT),
        "defectSourceCommit": defect["provenance"]["sourceCommit"],
        "defectArchiveCommit": "04204df9ccf4a6a378cd5963d19d38f97a04526e",
        "verificationCertificate": str(VERIFICATION.relative_to(ROOT)),
        "verificationSha256": digest(VERIFICATION),
        "claimBoundary": (
            "One fixed eighth-order coefficient only; all Picard orders and "
            "general 3D Navier-Stokes regularity remain open."
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )
    write_rows(
        HERE / "figure-data-resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{
            "elapsedSeconds": f"{time.perf_counter() - started:.6f}",
            "maximumRssMiB": f"{rss_mib():.3f}",
            "status": "passed",
        }],
    )


if __name__ == "__main__":
    main()
