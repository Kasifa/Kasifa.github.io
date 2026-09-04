# R0.75Z exact finite certificate report

- Verdict: **PASS**
- Assertions: 15/15
- Negative mutation classes: 72
- Fixture: q=2, ell=1; strict X case, equality Y case, and clustered Z case
- Exact point test: Z=2-exp(iy) at y=0

## Computed ledgers

```json
{
  "clusterLedger": {
    "carrier": 16,
    "offsets": [
      0,
      1
    ],
    "scaledWidth": 1,
    "strictWidthBound": 16,
    "widthBelowCarrier": true,
    "widthBoundHolds": true
  },
  "globalLedger": {
    "currentOver2Pi": 1,
    "fullGradientOver2Pi": 1313,
    "modulatedDissipationOver2Pi": 33,
    "offsetGradientOver2Pi": 1
  },
  "identityLedger": {
    "pdeResidual": [
      0,
      0
    ],
    "squareLeft": 1,
    "squareRight": 1
  },
  "partition": {
    "x": {
      "dyadicBand": true,
      "sector": "X"
    },
    "yEquality": {
      "clusters": [
        [
          16
        ],
        [
          32
        ]
      ],
      "dyadicBand": true,
      "sector": "Y",
      "separationProduct": 16,
      "signedMinimumGap": 16
    },
    "zCluster": {
      "clusters": [
        [
          16,
          17
        ]
      ],
      "dyadicBand": true,
      "sector": "Z",
      "separationProduct": 1,
      "signedMinimumGap": 1
    }
  },
  "pointLedger": {
    "J": -1,
    "Q": 1,
    "Z": [
      1,
      0
    ],
    "Zy": [
      0,
      -1
    ],
    "modulatedDissipationDensity": -31,
    "unweightedAbsorber": 2,
    "weightedCurrent": 32
  },
  "threshold": 16
}
```

The finite fixture checks branch inequalities, the equality cut, algebraic signs,
and exact integer ledgers.  It is not proof of the continuum identities.
The full clustered-sector flux payment and all regularity claims remain OPEN.
**NOT CLAY.**
