# R0.65 weighted-cycle certificate

This directory archives the publication-profile output for the exact moment
and rational Taylor enclosure of the heat-weighted periodic target

\[
L=1,\qquad M=16^r,\qquad q=2(16^r-1)/15,\qquad 1\le r\le24.
\]

The scientific source is commit
`22044d1d0fd530f2d50f4a541978aa7ae118da56`.

Reproduction command:

```text
python3 research/run_with_monitor.py \
  --output research/certificates/r065/audit-resources.csv \
  --interval 5 -- \
  python3 research/quartic_weighted_cycle_audit.py \
  --profile publication --max-r 24 --order 48 \
  --time-series-terms 120 \
  --probe research/certificates/r065/probes/r1.json \
  --probe research/certificates/r065/probes/r2.json \
  --probe research/certificates/r065/probes/r3.json \
  --probe research/certificates/r065/probes/r4.json \
  --output research/certificates/r065/weighted-cycle-audit.json \
  --progress
```

`weighted-cycle-audit.json` was produced with exact integer carrier moments
through total degree 96 and exact `Fraction` endpoints for the order-48
simplex expansion.  The four files under `probes/` are independent
long-double path enumerations at the first four cycle lengths.  They are
cross-checks, not the source of the certified inequalities.

The certificate proves facts only at the 24 explicitly listed finite scales.
It does not prove that the normalized sequence is unbounded, does not disprove
a uniform quartic estimate, and is not a Navier--Stokes regularity result.
