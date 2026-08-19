# R0.47 exact certificate

This directory archives the formal exact-rational audit for the R0.47
charge--degree lattice endpoint theorem.

## Certified statement

For the reduced canonical edge generating system, keep the R0.46 two-block
weighted norm

\[
\|f\|_{r,\kappa}
=\kappa\|P_0f\|_{B_r}+\|P_{\ne0}f\|_{B_r},
\qquad \kappa=\frac34.
\]

For a positive input charge `s`, let `J_s` be the minimum admissible tail
degree.  Instead of replacing every degree factor by a single global
constant, the proof retains

\[
d_i(J_s)=\frac{i+J_s}{i+J_s-1}
\]

inside the complete positive sum.  The remaining common-slope expression is
convex in `x=s/j`; hence all degrees `j>=J_s` are bounded by the two exact
endpoints `x=0` and `x=s/J_s`.

For every fixed charge `2<=s<241`, the certificate evaluates these two exact
endpoints.  This finite list consists of 239 all-degree theorems; it is not a
tail-degree grid.

For `s>=241`, the charge--degree lattice has two branches:

- even `s`: `J_s=s/2` and `x=2`;
- odd `s`: `J_s=(s+3)/2` and `x=2s/(s+3)`.

With `y=1/s`, both endpoint sums are exact rational functions.  After their
positive linear denominators are cleared, every degree-318 Bernstein
coefficient of the even derivative on `0<=y<=1/242` is strictly positive,
and every degree-318 Bernstein coefficient of the negative odd derivative on
`0<=y<=1/241` is strictly positive.  One complete interval is used in each
certificate, with no subdivision.  Thus the even branch is maximized at
`s=242,j=121`, and the odd branch is bounded by its `y=0` limit.  This covers
every large integer charge continuously, without a large-charge scan.

At the target radius

\[
r=\frac{94233}{250000}=0.376932,
\]

the exact maximum is the genuine fixed-charge endpoint `s=162,j=81`:

\[
\|L_r\|_{r,3/4}
\le 0.9999973490826196656<1.
\]

The resulting fixed-point Lipschitz upper bound is
`0.99999734911089611766`, and the independent canonical-stretch operator
bound is `0.99129357597486048791`; both gates close.

At the adjacent millionth

\[
r=0.376933,
\]

the same true column `s=162,j=81` has exact value
`1.0000026584572409359>1`.  Therefore this specific induced two-block
weighted-l1 sufficient inequality fails there.  This negative control is not
a singularity theorem, does not exclude a different norm or nonlinear
construction, and says nothing by itself about three-dimensional
Navier--Stokes regularity or blow-up.

## Files

- `edge-charge-degree-lattice.json`: machine-readable GMP certificate;
- `progress.ndjson`: append-only scientific stage log;
- `resources.csv`: 0.125-second process-tree resource samples;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned inputs

- source commit: `709ecb5f20b7321079ba114a57bf20b77ca7646a`;
- R0.46 input certificate SHA-256:
  `9310267b894c32b61034ec5e8f34b7d49144028830713a5e86b59d5be00109d1`.

## Exact reproduction command

```sh
PYTHONPATH=research tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r047/resources.csv \
  --interval 0.125 -- \
  tmp/r024-venv/bin/python research/edge_charge_degree_lattice_audit.py \
  --max-total-degree 80 \
  --entry-radius 376/1000 \
  --target-radius 376932/1000000 \
  --failure-probe-radius 376933/1000000 \
  --zero-charge-weight 3/4 \
  --charge-cutoff 241 \
  --regression-charges=-1,0,1,2,162,164,240,241,242,300 \
  --regression-degree-offsets 0,3,18 \
  --ball-divisor 1000000 \
  --source-commit 709ecb5f20b7321079ba114a57bf20b77ca7646a \
  --progress \
  --progress-log research/certificates/r047/progress.ndjson \
  --check --pretty \
  --output \
  research/certificates/r047/edge-charge-degree-lattice.json
```

## Successful-run summary

- 39/39 formal checks passed;
- scientific wall time: 68.383462 seconds;
- monitored wall time: 68.516376 seconds;
- resource samples: 458;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 56.625 MiB;
- GPU: not used;
- randomness: none;
- threshold arithmetic: `gmpy2.mpq`, with no floating-point decision.

Environment:

- macOS Darwin 25.6.0 arm64;
- Apple M5 Max, 36 GiB memory;
- Python 3.12.13;
- gmpy2 2.3.1;
- GMP 6.3.0.
