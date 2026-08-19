# R0.40 formal certificate package

This directory archives the formal exact run for the R0.40 two-endpoint
transport theorem and degree-80 restart.

## Claim boundary

The certificate proves an all-order theorem for the normalized transport
operator of the reduced edge generating system. Convexity reduces every
input slope to the actual endpoints x=-1 and x=2; monotonicity reduces
every input degree to j=1. Together with the R0.39 active-tail theorem,
this gives the common isotropic radius

    32/125 = 0.256

This does not prove global regularity or finite-time blow-up for the full
three-dimensional Navier--Stokes equation. The finite Padé candidate from
R0.32 remains a diagnostic only.

## Pinned source

    413f1cbcb12a961129eacf2482eb9b705c9a2feb

The R0.39 input certificate is pinned in the JSON by path and SHA-256.

## Formal command

Run from the repository root:

    tmp/r024-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r040/resources.csv \
      --interval 0.125 \
      -- \
      tmp/r024-venv/bin/python research/edge_slope_resolved_transport_audit.py \
      --max-total-degree 80 \
      --target-radius 32/125 \
      --failure-probe-radius 257/1000 \
      --charge-cutoff 241 \
      --finite-column-degrees 1,2,5,20,81 \
      --formula-regression-degree 10 \
      --ball-divisor 1000000 \
      --source-commit 413f1cbcb12a961129eacf2482eb9b705c9a2feb \
      --progress \
      --progress-log research/certificates/r040/progress.ndjson \
      --check \
      --pretty \
      --output research/certificates/r040/edge-slope-resolved-transport.json

## Formal result

- all 20 exact checks passed;
- the R0.39 all-order active-tail bound is approximately 0.994409311;
- the exact two-endpoint transport bound, including the unknown correction,
  is approximately 0.862199211;
- the R0.39 termwise transport bound is approximately 1.385989838 at the
  same radius, so the new radius does not follow from the previous estimate;
- the nearby exact probe at 257/1000 still has polynomial transport bound
  approximately 0.867286688, but its active-tail bound is approximately
  1.000256152;
- the complete residual has 6345 nonzero terms in degrees 81 through 160;
- 3055 ordered monomial pairs agree with the original bracket implementation;
- no floating-point value decides a sign or inequality in the certificate.

## Monitoring

- exact audit wall time recorded in the JSON: 31.9825 s;
- monitored process wall time: 32.1406 s;
- resource samples: 221 at a requested interval of 0.125 s;
- peak process-tree CPU: 100.0%;
- peak process-tree RSS: 40.531 MiB;
- GPU count: 0;
- random seed: none.

The computation is dominated by single-process exact GMP rational arithmetic.
The append-only progress and process-tree resource logs are preserved beside
the JSON certificate.
