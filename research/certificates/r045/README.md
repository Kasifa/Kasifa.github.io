# R0.45 exact certificate

This directory archives the formal exact-rational audit for the R0.45
fixed-negative-charge endpoint theorem.

## Certified statement

For a center monomial of degree (i) and charge (q), and a strict-tail
input of charge (s=-1) and degree (j), write (t=1/j).  At cutoff
(N=80), the bivariate lattice gives

\[
0\leq t\leq \frac1{82},\qquad j>80,\qquad j\equiv1\pmod 3.
\]

The exact weighted column is a finite sum of rational functions.  Terms with
(q=-1) vanish, terms with (q=0) or (q\geq2) increase with (t), and
only terms with (q=1) decrease.  On (0\leq t\leq T=1/82), the total
magnitude of those negative derivatives is bounded by

\[
\widehat Q_r(T)=\sum_i |a_{i,1}|r^i
\frac{(i-1)+2i^2T+i^2(i-1)T^2}{3}.
\]

The degree-one, charge-two seed contributes (r(3+2t)\geq3r).  Exact GMP
arithmetic at (r=0.371) gives

\[
\widehat Q_r(1/82)=0.16864755013760409118\ldots,
\qquad
3r-\widehat Q_r(1/82)=0.94435244986239590882\ldots>0.
\]

Therefore the complete column is strictly increasing in (t), and its exact
maximum over every admissible tail degree is the true lattice endpoint
(j=82).  No coefficient-sign cancellation or finite degree grid is used in
this proof.

At (r=0.371), the exact (j=82,s=-1) column is
0.99722804122918895132, while the complete large-charge sector is
0.97140144220860645363.  The complete Banach restart and inherited
canonical-stretch construction certify the reduced fields (a,\phi,U,V) at
that radius.  At the adjacent millesimal probe (r=0.372), the exact same
column is 1.0010616516434951437 and fails the present sufficient inequality,
while the large-charge sector and polynomial stretch operator still pass.

This is a theorem for the reduced canonical edge generating system, not a
three-dimensional Navier--Stokes regularity or singularity theorem.  The
failed probe is not evidence of a singularity.

## Files

- `edge-fixed-negative-charge.json`: machine-readable GMP certificate;
- `progress.ndjson`: append-only scientific stage log;
- `resources.csv`: 0.125-second process-tree resource samples;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned source

- source commit: `8f7f9ec2b90b2d249b474ec4dbba50a71c807745`;
- R0.44 input certificate SHA-256:
  `7966771f25305211907e11e1a7ab7b6d784b1a14e3db92b3cbec37b96382bb1f`.

## Exact reproduction command

```sh
tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r045/resources.csv \
  --interval 0.125 -- \
  tmp/r024-venv/bin/python research/edge_fixed_negative_charge_audit.py \
  --max-total-degree 80 \
  --entry-radius 37/100 \
  --target-radius 371/1000 \
  --failure-probe-radius 372/1000 \
  --charge-cutoff 241 \
  --regression-degree-offsets 0,3,6,18,918 \
  --ball-divisor 1000000 \
  --source-commit 8f7f9ec2b90b2d249b474ec4dbba50a71c807745 \
  --progress \
  --progress-log research/certificates/r045/progress.ndjson \
  --check --pretty \
  --output research/certificates/r045/edge-fixed-negative-charge.json
```

## Successful-run summary

- 33/33 formal checks passed;
- scientific wall time: 35.640978 seconds;
- monitored wall time: 35.747394 seconds;
- resource samples: 240;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 42.766 MiB;
- GPU: not used;
- randomness: none;
- threshold arithmetic: `gmpy2.mpq`, with no floating-point decision.

Environment:

- macOS Darwin 25.6.0 arm64;
- Apple M5 Max, 36 GiB memory;
- Python 3.12.13;
- gmpy2 2.3.1;
- GMP 6.3.0.
