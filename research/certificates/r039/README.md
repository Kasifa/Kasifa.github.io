# R0.39 formal certificate package

This directory archives the formal exact run for the R0.39 charge-resolved
tail and transport theorem.

## Claim boundary

The certificate proves an all-order contraction theorem for the reduced edge
generating system.  It uses a degree-80 exact center, 242 fixed input-charge
bounds, and one analytic sector covering every input charge at least 241.
It also proves a charge-resolved Neumann bound for the normalized transport
fields.  The resulting common isotropic radius is

```text
397/2000 = 0.1985
```

This does not prove global regularity or finite-time blow-up for the full
three-dimensional Navier--Stokes equation.  The finite Padé candidate from
R0.32 remains a diagnostic only.

## Pinned source

```text
ed08ad45b3440a679d8132d7b3464dc21dd07fa5
```

The R0.38 input certificate is pinned in the JSON by path and SHA-256.

## Formal command

Run from the repository root:

```text
tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r039/resources.csv \
  --interval 0.125 \
  -- \
  tmp/r024-venv/bin/python research/edge_charge_resolved_audit.py \
  --max-total-degree 80 \
  --target-radius 397/2000 \
  --charge-cutoff 241 \
  --failure-probe-radius 199/1000 \
  --finite-column-degrees 81,82,160,241 \
  --formula-regression-degree 10 \
  --ball-divisor 1000000 \
  --source-commit ed08ad45b3440a679d8132d7b3464dc21dd07fa5 \
  --progress \
  --progress-log research/certificates/r039/progress.ndjson \
  --check \
  --pretty \
  --output research/certificates/r039/edge-charge-resolved.json
```

## Formal result

- all 18 exact checks passed;
- the R0.38 scalar tail bound is approximately `2.03876648`, so it fails;
- the new all-order charge-resolved tail bound is approximately
  `0.689601119`;
- the refined transport bound, including the unknown tail correction, is
  approximately `0.999410431`;
- the nearby exact probe at `199/1000` fails the present transport condition
  with bound approximately `1.002542865`;
- the complete residual has 6345 nonzero terms in degrees 81 through 160;
- no floating-point value decides a sign or inequality in the certificate.

## Monitoring

- exact audit wall time recorded in the JSON: 33.7555 s;
- monitored process wall time: 33.8 s;
- resource samples: 228 at a requested interval of 0.125 s;
- peak process-tree CPU: 100.0%;
- peak process-tree RSS: 41.656 MiB;
- GPU count: 0;
- random seed: none.

The computation is dominated by single-process exact GMP rational arithmetic.
The append-only progress and process-tree resource logs are preserved beside
the JSON certificate.
