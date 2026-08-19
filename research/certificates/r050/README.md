# R0.50 exact certificate

This directory archives the formal exact-rational audit for the R0.50 global
optimization theorem in the multiplicative charge-character family.

## Certified statement

For the exact degree-80 center and the true input column `(j,s)=(81,162)`,
write

\[
A(r,c)=\sum_{i,q}b_{iq}r^ic^q,\qquad b_{iq}>0.
\]

The active charge support is `-1 <= q <= 157`, with both negative and
positive charges.  Every active degree is positive.  Therefore, for fixed
`r>0`, `A(r,e^t)` is strictly convex and coercive in `t=log(c)`; for fixed
`c>0`, it is strictly increasing in `r`.

The exact face polynomials

\[
P(r,c)=c(A(r,c)-1),\qquad
Q(r,c)=c\,\partial_tA(r,e^t)
\]

have the required opposite signs on all four complete faces of the rational
rectangle

\[
0.382619813709565\le r\le0.382619813709566,
\]

\[
0.8024563827\le c\le0.8024563828.
\]

All face signs are proved from exact Bernstein coefficients.  The
Poincare--Miranda theorem gives a simultaneous zero of `P` and `Q` inside the
rectangle.  Strict convexity, coercivity, and radius monotonicity imply that
this zero is unique and is the unique global maximizer of the active-column
threshold over every `c>0`.

Coefficientwise lower and upper charge envelopes make the comparison uniform
on the complete rectangle.  The all-order charge-degree theorem then covers
all 243 non-active competitors.  The nearest competitor remains the fixed
charge `s=164` sector, with exact positive dominance gap approximately
`0.00014580280493538903081`.

Relative to the R0.49 upper root at `c=4/5`, the new exact lower bound improves
the threshold radius by a factor greater than
`1.0000030613272706956`.  The corresponding fixed-charge radius `r^3`
improves by a factor greater than `1.0000091840099272895`.  This gain is
strict but small.

At the simple rational point

\[
r=0.382619,\qquad c=0.8024563827,
\]

the degree-weighted residual is approximately
`1.7828790986376003423e-30`, the tail linearization bound is
`0.99999609693061278829`, and the exact anisotropic fixed-point and canonical
field checks close.

The theorem is for the reduced canonical edge generating system and the
finite exact degree-80 center.  It is not an optimization over every Banach
norm, not a critical-norm bridge for arbitrary three-dimensional velocity
fields, and not a proof or disproof of three-dimensional Navier--Stokes
regularity.

## Files

- `edge-charge-character-optimization.json`: machine-readable GMP
  certificate;
- `progress.ndjson`: append-only scientific stage log;
- `resources.csv`: two-second process-tree resource samples;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned inputs

- source commit: `a9c469a96462e60655b0fea435177ececb8aef20`;
- formal audit source SHA-256:
  `499cbbc1e29cb3d8276efa7aa35a67abe2afcfcce579d251b7b6073cc3ecb437`;
- exploratory source SHA-256:
  `5c20ffe676d2ad93440fcb3a207d4e3243a24a9253a07ca6a45d1141eab76c9b`;
- R0.49 input certificate SHA-256:
  `e36fce33f8a5edeb144cdbeda00a568b972d9a3a8ac0e96c04d7651e71a64578`;
- degree-80 polynomial SHA-256:
  `056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7`;
- rectangle competitor-bound digest SHA-256:
  `aa1aa7d75a4ec7f3ec4571603df587722bb863e3892830197b4eab4e48272400`.

## Exact reproduction command

```sh
PYTHONPATH=research tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r050/resources.csv \
  --interval 2 -- \
  tmp/r024-venv/bin/python \
  research/edge_charge_character_optimization_audit.py \
  --max-total-degree 80 \
  --radius-lower 382619813709565/1000000000000000 \
  --radius-upper 382619813709566/1000000000000000 \
  --character-lower 8024563827/10000000000 \
  --character-upper 8024563828/10000000000 \
  --restart-radius 382619/1000000 \
  --ball-divisor 1000000 \
  --charge-cutoff 241 \
  --source-commit a9c469a96462e60655b0fea435177ececb8aef20 \
  --progress \
  --progress-log research/certificates/r050/progress.ndjson \
  --check --pretty \
  --output \
  research/certificates/r050/edge-charge-character-optimization.json
```

## Successful-run summary

- 33/33 exact checks passed;
- complete-face Bernstein degrees: 158 for `P`, 80 for `Q`;
- competitors covered: 243;
- finite exact center terms: 2161;
- active Laurent terms: 2160;
- recurrence ordered interactions: 1,113,168;
- scientific wall time: 137.928040 seconds;
- monitored wall time: 138.1 seconds;
- resource samples: 70;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 104.234 MiB;
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
