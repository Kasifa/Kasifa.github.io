# R0.75S exact finite certificate report

- Verdict: **PASS**
- Assertions: 21/21
- Blocker count: 0
- Mutation: `none`

## Exact computed rows

- Complete clock at `R=1/16`: `T=1/64`.
- Regime fixtures: `[{"epsilon": "1", "lambda": "1/64", "name": "low-node", "q": "1/16", "regime": "low"}, {"epsilon": "8", "lambda": "1", "name": "spread-q-below-one", "q": "1/2", "regime": "high-q-below-one"}, {"epsilon": "32", "lambda": "16", "name": "spread-q-above-one", "q": "2", "regime": "high-q-above-one"}]`.
- BV total: `2`.
- Frozen logarithmic rate: `-2/11907`.
- Low target ledger: `{"amplitudeCancels": true, "lowTarget": {"A": 2, "J": "2/3", "R": 3, "a": 2}, "normalizedOmegaExponent": "1/3", "normalizedRExponent": 0}`.

## Boundary

The certificate checks the full-frequency complete-clock payment only for one real constant-drift harmonic and the canonical radial collar. Multimode interference, nonconstant shear, E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. NOT CLAY.
