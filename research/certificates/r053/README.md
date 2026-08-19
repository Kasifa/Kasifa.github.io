# R0.53 exact certificate

This directory archives the formal exact-rational audit of one fixed
product-affine charge weight

\[
\omega_s=c^s(1+\lambda|s|)(1+\mu|s|)
\]

for the exact degree-80 center of the reduced canonical edge generating
system.  The pinned rational parameters are

\[
c=\frac{396403}{500000},\qquad
\lambda=\mu=\frac{153931}{500000}.
\]

## Certified statement

The zero-charge column at minimum tail degree `j=81` has a globally unique
positive threshold root in

\[
0.382628602237879637
<r_*<
0.382628602237879638.
\]

The interval width is exactly `1e-18`.  The lower endpoint exceeds the R0.52
global upper bound for the complete single-affine family by a factor greater
than `1.0000107948905119688`.

The product weight retains algebra constant one because each affine factor is
submultiplicative.  Every non-active charge and degree is strictly below the
zero-charge equality on the root box.  The audit covers 278 fixed positive
charges `2<=s<280`, the all-degree `s=1` and `s=-1` sectors, and one exact
even/odd large-charge theorem for every `s>=280`.  There are 281 inactive
records.  The nearest competitor is the former active column
`(j,s)=(81,162)`, with gap greater than
`1.4883451915609408904e-6`.

For `s>=280`, the squared-affine coefficientwise envelope is followed by
exact rational even and odd minimum-degree endpoint functions.  Complete
Bernstein derivative signs prove the even maximum occurs at `s=280` and the
odd branch is bounded by its infinite-charge limit.  The uniform tail bound
at the root-box right endpoint is

\[
0.99856429173292745732<1.
\]

At the simpler rational restart radius

\[
r_0=\frac{95657}{250000}=0.382628,
\]

the exact linearization bound is below `0.99999769297234707665`, leaving
margin greater than `2.3070276529233482826e-6`.  The product-affine weighted
residual norm is below `7.5271302784558830723e-31`; the exact self-map and
Lipschitz inequalities pass with quadratic constant three.  This restart
radius exceeds the R0.52 complete-family upper bound by a factor greater than
`1.000009220924589906`.

This is a strict rational counterexample to degeneration of the
product-affine family to the complete single-affine boundary.  It does not
prove global optimality inside the complete product-affine family, optimize
every Banach norm, provide a critical-space bridge for arbitrary
three-dimensional divergence-free fields, or prove or disprove
three-dimensional Navier--Stokes regularity.

## Files

- `edge-product-affine-charge-weight.json`: machine-readable GMP certificate;
- `progress.ndjson`: append-only scientific stage log;
- `resources.csv`: two-second process-tree resource samples;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned inputs and proof digests

- source commit: `96d7d8c7d0a59e1b0b75d2580403cb5969d6ea6e`;
- formal audit source SHA-256:
  `e4e9e71f3663e23dd33aaf11bcdd3f0cb2e5db5ca27ecdff98ca06dbe232828b`;
- mathematical note SHA-256:
  `f108bd70071932b3366bd11198d4fdb2bf72db4dbcda5b55aa0806d10ea91a92`;
- R0.52 input certificate SHA-256:
  `b79e59ec327bc02b64e23ad3f903b6d61860a075d59ff75a43d82f5684590def`;
- degree-80 polynomial SHA-256:
  `056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7`.

## Exact reproduction command

```sh
PYTHONPATH=research tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r053/resources.csv \
  --interval 2 -- \
  tmp/r024-venv/bin/python \
  research/edge_product_affine_charge_weight_audit.py \
  --max-total-degree 80 \
  --charge-cutoff 280 \
  --character 396403/500000 \
  --lambda 153931/500000 \
  --mu 153931/500000 \
  --radius-lower 382628602237879637/1000000000000000000 \
  --radius-upper 382628602237879638/1000000000000000000 \
  --restart-radius 95657/250000 \
  --ball-divisor 1000000 \
  --source-commit 96d7d8c7d0a59e1b0b75d2580403cb5969d6ea6e \
  --progress \
  --progress-log research/certificates/r053/progress.ndjson \
  --check --pretty \
  --output research/certificates/r053/edge-product-affine-charge-weight.json
```

## Successful-run summary

- 28/28 exact checks passed;
- inactive records: 281;
- finite exact center terms: 2,161;
- recurrence ordered interactions: 1,113,168;
- scientific wall time: 143.264860 seconds;
- monitored wall time: 143.399436 seconds;
- resource samples: 72;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 222.453 MiB;
- GPU: not used;
- randomness: none;
- sign arithmetic: `gmpy2.mpq` over GMP 6.3.0, with no floating-point
  decision.

Environment:

- macOS 26.6.1 arm64;
- Apple M5 Max, 36 GiB memory;
- Python 3.12.13;
- gmpy2 2.3.1;
- GMP 6.3.0.

