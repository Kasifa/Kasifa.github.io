# R0.43 exact certificate

This directory archives the formal exact-rational audit for the R0.43
charge-implied degree-floor theorem.

## Certified statement

For every strict-tail input in the large positive-charge sector,

\[
s\geq S,\qquad j>N,\qquad s\leq2j,
\]

the bivariate support cone implies

\[
j\geq\max\{N+1,\lceil S/2\rceil\}.
\]

At \(N=80\) and \(S=241\), the uniform input-degree floor is therefore 121
rather than 81.  Replacing only the corresponding decreasing degree
prefactor lowers the all-order large-charge active-tail bound at
\(r=33/100\) from 1.002872150853994023 to 0.99888144242700740673.  The
complete active Banach restart and the inherited canonical-stretch
construction then certify the reduced fields \(a,\phi,U,V\) at that radius.

This is a theorem for the reduced canonical edge generating system, not a
three-dimensional Navier--Stokes regularity or singularity theorem.  The
failure of the improved sufficient bound at \(r=331/1000\) is not a
singularity result.

## Files

- `edge-charge-degree-floor.json`: machine-readable GMP certificate;
- `progress.ndjson`: append-only scientific stage log;
- `resources.csv`: 0.125-second process-tree resource samples;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned source

- source commit: `4fe8cb308e20921fb0490aa2e76209b1d2d84221`
- R0.42 input certificate SHA-256:
  `0c426070c47afb519fc9c705cbe11ed59b82ee6b28e766696280379b15e5dfa5`

## Exact reproduction command

```sh
tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r043/resources.csv \
  --interval 0.125 -- \
  tmp/r024-venv/bin/python research/edge_charge_degree_floor_audit.py \
  --max-total-degree 80 \
  --target-radius 33/100 \
  --failure-probe-radius 331/1000 \
  --charge-cutoff 241 \
  --regression-charges 241,242,243,300,480,600,1000 \
  --regression-degree-offsets 0,3,12 \
  --ball-divisor 1000000 \
  --source-commit 4fe8cb308e20921fb0490aa2e76209b1d2d84221 \
  --progress \
  --progress-log research/certificates/r043/progress.ndjson \
  --check --pretty \
  --output research/certificates/r043/edge-charge-degree-floor.json
```

## Successful-run summary

- 22/22 formal checks passed;
- scientific wall time: 37.889746 seconds;
- monitored wall time: 38.028696 seconds;
- resource samples: 255;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 44.312 MiB;
- GPU: not used;
- randomness: none;
- threshold arithmetic: `gmpy2.mpq`, with no floating-point decision.

Environment:

- macOS Darwin 25.6.0 arm64;
- Apple M5 Max, 36 GiB memory;
- Python 3.12.13;
- gmpy2 2.3.1;
- GMP 6.3.0.
