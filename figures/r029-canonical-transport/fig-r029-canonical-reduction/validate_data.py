#!/usr/bin/env python3
"""Cross-check the R0.29 figure contract against the exact certificate."""

from __future__ import annotations

import csv
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = (
    REPOSITORY / "research/certificates/r029/edge-canonical-transport.json"
)

EXPECTED_IDENTITIES = {
    "canonical": "{U,V}=UV",
    "ratio": "U/V=(Z/W) exp(-a)",
    "factor": "d=-exp(phi)[p Z exp(-a/2)/12+q W exp(a/2)/3]",
    "ladder": "(3k-q-1)f_(k,q)=k f_(k,q+1)+lower-degree terms",
}


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    with (PACKAGE / "identities.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    assert len(rows) == 4
    assert {row["id"]: row["statement"] for row in rows} == EXPECTED_IDENTITIES
    assert all(row["status"] == "all-order identity" for row in rows)

    theorem = payload["formalTheorem"]
    assert theorem["identities"]["logCanonical"] == EXPECTED_IDENTITIES["canonical"]
    assert theorem["identities"]["ratio"] == EXPECTED_IDENTITIES["ratio"]
    obstruction = theorem["finiteChargeClosureObstruction"]
    assert obstruction["aSupport"] == "a_(k,q)=0 for q<-1 and a_(0,-1)=1"
    assert obstruction["transportRecurrence"] == EXPECTED_IDENTITIES["ladder"].replace(
        "+lower-degree terms", "+lower-degree convolution terms"
    )

    identities = payload["checks"]["canonicalIdentities"]
    support = payload["checks"]["aChargeSupport"]
    assert payload["scope"]["maximumCheckedTotalDegree"] == 119
    assert identities["maximumTotalDegree"] == 119
    assert identities["coefficientChecks"] == 14514
    assert identities["exactConvolutionInteractions"] > 0
    assert identities["passed"] is True
    assert identities["firstFailure"] is None
    assert support["passed"] is True
    assert support["minimumAllowedCharge"] == -1
    assert support["violations"] == []
    assert payload["computation"]["backend"].startswith("gmpy2.mpq (GMP")
    assert payload["git"]["dirty"] is False
    print("validated the four R0.29 theorem statements and degree-119 exact audit")


if __name__ == "__main__":
    main()
