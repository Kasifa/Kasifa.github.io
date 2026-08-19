# R0.42 exact certificate

This directory archives the formal exact-rational audit for the R0.42
canonical-stretch transport theorem.

## Certified statement

For the reduced canonical edge generating system, the R0.41 all-order active
restart and the R0.29 canonical factorization combine to construct the active
field (a), the zero-initial stretch (\phi), and the normalized fields
(U,V) on the common isotropic polydisc of radius

\[
r=329/1000.
\]

The stretch operator is (S_a=\mathcal L^{-1}\{a,\cdot\}).  Its complete
weighted column is convex in the common input slope and has no input-degree
prefactor.  The two exact endpoint columns therefore cover every input degree
and charge.  This is a theorem for the reduced generating system, not a
three-dimensional Navier--Stokes regularity or singularity theorem.

## Files

- `edge-stretch-transport.json`: machine-readable GMP certificate;
- `progress.ndjson`: append-only scientific stage log for the successful run;
- `resources.csv`: 0.125-second process-tree resource samples for the
  successful run;
- `attempt-1-progress.ndjson`, `attempt-1-resources.csv`: preserved interrupted
  provenance attempt described below;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned source

- source commit: `5ff24eae1cb9f73a1aac6965b07f0c1f12c62477`
- R0.41 input certificate SHA-256:
  `1eb4bbe5f7e53e9eacf7f445b716194ab492603a7de35884549e9c7def640653`

## Exact reproduction command

```sh
tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r042/resources.csv \
  --interval 0.125 -- \
  tmp/r024-venv/bin/python research/edge_stretch_transport_audit.py \
  --max-total-degree 80 \
  --target-radius 329/1000 \
  --acceptance-radius 141/500 \
  --failure-probe-radius 33/100 \
  --charge-cutoff 241 \
  --finite-column-degrees 1,2,5,20,81 \
  --formula-regression-degree 10 \
  --factorization-degree 30 \
  --ball-divisor 1000000 \
  --source-commit 5ff24eae1cb9f73a1aac6965b07f0c1f12c62477 \
  --progress \
  --progress-log research/certificates/r042/progress.ndjson \
  --check --pretty \
  --output research/certificates/r042/edge-stretch-transport.json
```

## Successful-run summary

- 26/26 formal checks passed;
- scientific wall time: 36.271151 seconds;
- monitored wall time: 36.405242 seconds;
- resource samples: 244;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 45.641 MiB;
- GPU: not used;
- randomness: none;
- threshold arithmetic: `gmpy2.mpq`, with no floating-point decision.

Environment:

- macOS Darwin 25.6.0 arm64;
- Apple M5 Max, 36 GiB memory;
- Python 3.12.13;
- gmpy2 2.3.1;
- GMP 6.3.0.

## Preserved interrupted attempt

The first formal launch was stopped after 13.98 seconds, during construction
of the complete residual.  The short source commit had been manually expanded
to an incorrect full hash in the command.  No certificate JSON was produced,
and no mathematical threshold was reached.  Its progress and resource logs
are retained rather than overwritten.  The successful run used the full hash
returned directly by Git and is the only run cited by the certificate.
