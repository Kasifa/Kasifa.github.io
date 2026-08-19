# R0.48 exact certificate

This directory archives the formal exact-rational audit for the R0.48
charge-threshold root theorem.

## Certified statement

For the reduced canonical edge generating system, keep the two-block
weighted norm

\[
\|f\|_{r,\kappa}
=\kappa\|P_0f\|_{B_r}+\|P_{\ne0}f\|_{B_r},
\qquad \kappa=\frac34.
\]

The R0.47 endpoint theorem isolates the true minimum-degree input column
with charge `s=162` and degree `j=81` at both ends of
`[0.376932,0.376933]`.  Its exact value is a degree-80 polynomial

\[
A(r)=C_r(81,162)=\sum_{i=1}^{80}\alpha_i r^i,
\qquad \alpha_i>0.
\]

Consequently `P(r)=A(r)-1` has constant coefficient `-1`, all 80
nonconstant coefficients are strictly positive, and `P'(r)>0` for every
positive `r`.  Thus `P` has at most one positive root.  Exact GMP rational
bisection and an independent exact Sturm sequence isolate and count one root:

\[
0.376932499290527340<r_*<0.376932499290527341.
\]

The lower-end Sturm variation is 40 and the upper-end variation is 39; none
of the 81 sequence values vanishes at either endpoint.

Full-window dominance follows from an exact monotone sandwich.  Every column
is a nonnegative sum of powers of `r`.  Each competitor in the window is
therefore at most its pinned R0.47 all-order value at the right endpoint,
while the active column is at least its exact left-endpoint value.  The audit
covers all 243 competitors: 238 other fixed positive charges, the inactive
endpoint of charge 162, and four other exhaustive charge sectors.  The
nearest competitor is `s=164`, and the exact dominance gap is approximately
`9.9933786489298977945e-05`.

It follows that the full induced norm equals `A(r)` throughout the adjacent
millionth window.  It is below one for `r<r_*`, exactly one at `r_*`, and
above one for `r>r_*` within that window.

This is a sharp local threshold theorem for the current reduced induced
two-block weighted-l1 norm.  It is not a PDE singularity theorem, does not
establish or refute three-dimensional Navier--Stokes regularity, and does not
exclude a different norm or nonlinear construction beyond the threshold.

## Files

- `edge-charge-threshold-root.json`: machine-readable GMP certificate;
- `progress.ndjson`: append-only scientific stage log;
- `resources.csv`: 0.125-second process-tree resource samples;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned inputs

- source commit: `fe65dcb365eca9d934c3ec6055c06d7a7c1a515c`;
- R0.47 input certificate SHA-256:
  `e45bc20ddeab9efde83dafefc84514df0260f8831c102c4621f0fdcd43dea6c9`;
- rational threshold-polynomial SHA-256:
  `37653ae3a9fe744036643d9480250aa2ccbede6e6a8091050827254617d675cf`;
- primitive integer threshold-polynomial SHA-256:
  `d30024f19b2538961103ade17ac0df50947518fa698e43b28a8fcd1e5e33e87f`.

## Exact reproduction command

```sh
PYTHONPATH=research tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r048/resources.csv \
  --interval 0.125 -- \
  tmp/r024-venv/bin/python research/edge_charge_threshold_root_audit.py \
  --max-total-degree 80 \
  --window-lower 376932/1000000 \
  --window-upper 376933/1000000 \
  --root-decimal-digits 18 \
  --zero-charge-weight 3/4 \
  --charge-cutoff 241 \
  --source-commit fe65dcb365eca9d934c3ec6055c06d7a7c1a515c \
  --progress \
  --progress-log research/certificates/r048/progress.ndjson \
  --check --pretty \
  --output \
  research/certificates/r048/edge-charge-threshold-root.json
```

## Successful-run summary

- 22/22 formal checks passed;
- exact Sturm sequence length: 81;
- exact root count in the isolated interval: 1;
- exact bisection decisions: 40;
- competitors covered: 243;
- scientific wall time: 21.172433 seconds;
- monitored wall time: 21.287027 seconds;
- resource samples: 144;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 109.875 MiB;
- GPU: not used;
- randomness: none;
- threshold arithmetic: `gmpy2.mpq/mpz`, with no floating-point decision.

Environment:

- macOS Darwin 25.6.0 arm64;
- Apple M5 Max, 36 GiB memory;
- Python 3.12.13;
- gmpy2 2.3.1;
- GMP 6.3.0.
