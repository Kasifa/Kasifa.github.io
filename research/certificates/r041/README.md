# R0.41 formal certificate package

This directory archives the formal exact run for the R0.41
degree-resolved common-endpoint active-tail theorem and the degree-80 restart.

## Claim boundary

For each fixed input charge from 2 through 240, the complete center column
is kept as a convex function of the common slope `x=s/j`. Its maximum is
therefore reduced to `x=0` and `x=s/J_s` before the uniform degree prefactor
is applied. The exceptional charges `-1,0,1` and the infinite sector
`s>=241` retain the proved R0.39 bounds. This covers every input degree above
80 and gives the common isotropic radius

    9/32 = 0.28125

This does not prove global regularity or finite-time blow-up for the full
three-dimensional Navier--Stokes equation. The finite column regressions and
the R0.32 Padé candidates remain diagnostics only.

## Pinned source

    c851762902bb97dd3f3f2510b7321771e0a1ff03

The R0.40 input certificate is pinned in the JSON by path and SHA-256.

## Formal command

Run from the repository root:

    tmp/r024-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r041/resources.csv \
      --interval 0.125 \
      -- \
      tmp/r024-venv/bin/python research/edge_degree_resolved_tail_audit.py \
      --max-total-degree 80 \
      --target-radius 9/32 \
      --acceptance-radius 257/1000 \
      --failure-probe-radius 141/500 \
      --charge-cutoff 241 \
      --finite-degrees 81,84,87,90,99,120,162,243,324,486,810,1620 \
      --formula-regression-degree 10 \
      --ball-divisor 1000000 \
      --source-commit c851762902bb97dd3f3f2510b7321771e0a1ff03 \
      --progress \
      --progress-log research/certificates/r041/progress.ndjson \
      --check \
      --pretty \
      --output research/certificates/r041/edge-degree-resolved-tail.json

## Formal result

- all 30 exact checks passed;
- the preassigned R0.40 failure probe `257/1000` is now certified, with
  degree-resolved active-tail bound approximately `0.6804858814` and total
  transport bound approximately `0.8672869049`;
- at `9/32`, the all-order active-tail bound is approximately
  `0.7785423316`, and its worst sector is the inherited analytic sector
  `s>=241`;
- at the same radius, the exact two-endpoint transport bound including the
  unknown correction is approximately `0.9962112032`;
- the complete residual has 6345 nonzero terms in degrees 81 through 160 and
  norm approximately `3.8850013583e-39`;
- the ball radius is approximately `2.2145766838e-7`, the mapping upper bound
  is approximately `1.7241431663e-7`, and the Lipschitz upper bound is
  approximately `0.7785436604`;
- the common radius gain from R0.40 is exactly `1125/1024`, and the cubic
  fixed-charge gain is exactly `1423828125/1073741824`;
- the adjacent probe `141/500=0.282` still passes the new active fixed-point
  gate, but its transport bound is approximately `1.0003750452`, so the
  present sufficient proof fails only at the transport gate;
- 2209 active-derivative monomial pairs agree with the original bracket
  implementation;
- 1195 exact multicharge columns and 12 additional charge-162 columns lie
  below their all-order sector bounds;
- no floating-point value decides a sign or inequality in the certificate.

## Monitoring

- exact audit wall time recorded in the JSON: `40.6692 s`;
- monitored process wall time: `40.7794 s`;
- resource samples: `274` at a requested interval of `0.125 s`;
- peak process-tree CPU: `100.0%`;
- peak process-tree RSS: `53.938 MiB`;
- GPU count: `0`;
- random seed: none.

The computation is dominated by single-process exact GMP rational arithmetic.
The append-only progress and process-tree resource logs are preserved beside
the JSON certificate.

## Files

- `edge-degree-resolved-tail.json`: exact theorem, restart, probe, and finite
  regression records;
- `progress.ndjson`: append-only scientific progress stages;
- `resources.csv`: independent process-tree resource samples;
- `SHA256SUMS`: package integrity manifest.
