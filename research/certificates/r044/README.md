# R0.44 exact certificate

This directory archives the formal exact-rational audit for the R0.44
common-slope endpoint theorem.

## Certified statement

For a center monomial of degree (i) and charge (q), and a strict-tail
input of degree (j) and charge (sgeq S), write (x=s/j).  The active
support cone gives (0leq xleq2), and R0.43 gives

\[
j\geq J_S:=\max\{N+1,\lceil S/2\rceil\}.
\]

After positive degree and charge-ratio domination, the complete large-charge
column is bounded by

\[
H_r(x)=\sum_{i,q}|a_{i,q}|r^i
\frac{i+J_S}{i+J_S-1}\,\beta_q\,\frac{|ix-q|}{3},
\]

where \(\beta_{-1}=(S+1)/(S-1)\) and \(\beta_q=1\) for \(q\geq0\).
The same (x) occurs in every summand.  Since (H_r) is a positive sum of
absolute affine functions, it is convex on \([0,2]\), so its all-order
maximum is exactly reduced to \(\max\{H_r(0),H_r(2)\}\).

At (N=80) and (S=241), the preassigned R0.43 failure at (r=0.331)
becomes a strict pass.  At (r=0.370), the common-slope large-charge bound is
0.96621300575693572712, while the unchanged finite (s=-1) column is the
new maximum at 0.99701184124819861673.  The complete Banach restart and the
inherited canonical-stretch construction certify the reduced fields
\(a,\phi,U,V\) at that radius.  At the adjacent millesimal probe (r=0.371),
the large-charge sector still passes at 0.97140144220860645363, but the
finite (s=-1) column is 1.0008564924160487608 and fails the present
sufficient inequality.

This is a theorem for the reduced canonical edge generating system, not a
three-dimensional Navier--Stokes regularity or singularity theorem.  The
failure at (r=0.371) is not evidence of a singularity.

## Files

- `edge-common-slope-tail.json`: machine-readable GMP certificate;
- `progress.ndjson`: append-only scientific stage log;
- `resources.csv`: 0.125-second process-tree resource samples;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned source

- source commit: `aade631ea1a492d078f052776b443875d6a3dd73`
- R0.43 input certificate SHA-256:
  `0ebaaf6c5a9f731e5b2846f3042553bebd6748b298ce31919e8f423e41369bf8`

## Exact reproduction command

```sh
tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r044/resources.csv \
  --interval 0.125 -- \
  tmp/r024-venv/bin/python research/edge_common_slope_tail_audit.py \
  --max-total-degree 80 \
  --entry-radius 331/1000 \
  --target-radius 37/100 \
  --failure-probe-radius 371/1000 \
  --charge-cutoff 241 \
  --regression-charges 241,242,243,300,480,600,1000 \
  --regression-degree-offsets 0,3,12 \
  --ball-divisor 1000000 \
  --source-commit aade631ea1a492d078f052776b443875d6a3dd73 \
  --progress \
  --progress-log research/certificates/r044/progress.ndjson \
  --check --pretty \
  --output research/certificates/r044/edge-common-slope-tail.json
```

## Successful-run summary

- 34/34 formal checks passed;
- scientific wall time: 44.516445 seconds;
- monitored wall time: 44.618455 seconds;
- resource samples: 300;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 47.906 MiB;
- GPU: not used;
- randomness: none;
- threshold arithmetic: `gmpy2.mpq`, with no floating-point decision.

Environment:

- macOS Darwin 25.6.0 arm64;
- Apple M5 Max, 36 GiB memory;
- Python 3.12.13;
- gmpy2 2.3.1;
- GMP 6.3.0.
