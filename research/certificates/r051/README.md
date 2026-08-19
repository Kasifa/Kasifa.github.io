# R0.51 exact certificate

This directory archives the formal exact-rational audit for one affine
charge weight beyond the optimized multiplicative-character family of R0.50.

## Certified statement

Fix

\[
\omega_s(c,\lambda)=c^s(1+\lambda|s|),\qquad
c=\frac{19939}{25000},\quad
\lambda=\frac{7653}{10000}.
\]

The inequality

\[
1+\lambda|a+b|
\le 1+\lambda|a|+\lambda|b|
\le (1+\lambda|a|)(1+\lambda|b|)
\]

proves submultiplicativity with algebra constant one.  For the exact
degree-80 center, the true `(j,s)=(81,162)` column is a degree-80 polynomial
with positive nonconstant coefficients.  Its unique positive threshold root
satisfies

\[
0.382624471846022<r_*<0.382624471846023.
\]

An exact Sturm sequence counts one root in this interval.  The five
exhaustive charge sectors are also covered without a tail-degree or infinite
charge grid:

- `s=0`, `s=-1`, and `s=1` use exact special-sector theorems;
- every `2<=s<241` uses the two exact convex endpoints in tail degree;
- every `s>=241` uses a coefficientwise affine envelope followed by the
  parity/Bernstein theorem.

There are 243 non-active competitors.  The nearest is `s=0`; its exact upper
bound at the right side of the root box is approximately
`0.99998219180517380589`.  The exact gap below the active column at the left
side is approximately `1.7808194822375234792e-05`.

Relative to the R0.50 globally optimized multiplicative-character upper
root, the R0.51 lower root improves the threshold radius by a factor greater
than `1.0000121743210599539`.  The corresponding `r^3` factor is greater than
`1.0000365234078239459`.  This is a strict but small improvement.

At the simple rational restart radius `r=0.382624`, the exact affine weighted
linearization bound is approximately `0.99999773673918514317`, its margin is
approximately `2.2632608148568333017e-06`, and the affine weighted residual is
approximately `2.7403915410748708982e-31`.  The coefficient-algebra
fixed-point inequalities close.

The theorem is for one fixed norm on the reduced canonical edge generating
system and a finite exact degree-80 center.  It does not prove that this
choice is globally optimal in `(c,lambda)`, does not provide a critical-space
bridge for arbitrary three-dimensional velocity fields, and does not prove
or disprove three-dimensional Navier--Stokes regularity.

## Files

- `edge-affine-charge-weight.json`: machine-readable GMP certificate;
- `progress.ndjson`: append-only scientific stage log;
- `resources.csv`: two-second process-tree resource samples;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned inputs

- source commit: `a53fdea63631977e4bb18f56da91e4e32e1a70c3`;
- formal audit source SHA-256:
  `fc1d0d880e3ac1a64380619e54979969b0cfc50480e5adbcb116d200a7ab3b1a`;
- exploratory source SHA-256:
  `7b4f87cc459e42d5937ba9071327ed9b0626ac850e00abc5c1d6a373f5b96a32`;
- R0.50 input certificate SHA-256:
  `fc173a2108ef881d21d9d54046085f0d5daf5cc33ed50e024ca32ec867f7b79a`;
- degree-80 polynomial SHA-256:
  `056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7`;
- competitor-bound digest SHA-256:
  `1e740cb7e4fdc82567872e86dd5d8dad0326b46eb8b07aabfb778f8e7c3e9ea1`;
- active polynomial coefficient digest SHA-256:
  `04f270d1ecfebe8c292bb09a3bb2c69bf6dd9e2511a103dfbb2fedd974f75744`;
- primitive threshold polynomial coefficient digest SHA-256:
  `efbfc1e247a4c74ab86e750e6800aa3c4e5fbc39860f0a9d77e80bdeb0d85f3f`.

## Exact reproduction command

```sh
PYTHONPATH=research tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r051/resources.csv \
  --interval 2 -- \
  tmp/r024-venv/bin/python \
  research/edge_affine_charge_weight_audit.py \
  --max-total-degree 80 \
  --character 19939/25000 \
  --lambda 7653/10000 \
  --radius-lower 382624471846022/1000000000000000 \
  --radius-upper 382624471846023/1000000000000000 \
  --restart-radius 382624/1000000 \
  --charge-cutoff 241 \
  --ball-divisor 1000000 \
  --source-commit a53fdea63631977e4bb18f56da91e4e32e1a70c3 \
  --progress \
  --progress-log research/certificates/r051/progress.ndjson \
  --check --pretty \
  --output research/certificates/r051/edge-affine-charge-weight.json
```

## Successful-run summary

- 26/26 exact checks passed;
- competitors covered: 243;
- finite exact center terms: 2161;
- recurrence ordered interactions: 1,113,168;
- scientific wall time: 127.065471 seconds;
- monitored wall time: 127.2 seconds;
- resource samples: 64;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 201.453 MiB;
- GPU: not used;
- randomness: none;
- sign arithmetic: `gmpy2.mpq` over GMP 6.3.0, with no floating-point
  decision.

Environment:

- macOS Darwin 25.6.0 arm64;
- Apple M5 Max, 36 GiB memory;
- Python 3.12.13;
- gmpy2 2.3.1;
- GMP 6.3.0.
