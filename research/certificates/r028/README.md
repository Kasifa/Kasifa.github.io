# R0.28 exact rational edge certificate

This directory archives the formal GMP rational computation used in R0.28.
The negative-edge scalar recurrence is evaluated through \(N=40\), or 119
leaves, after an all-order change of variables that removes the radical
generator from the coefficient arrays.

The certificate records:

- every exact fraction \(a_N,u_N,v_N,d_N\) for \(1\leq N\leq40\);
- exact interval images of \(d_N(p,q)\) on the certified radius-\(10^{-6}\)
  R0.20 root box;
- parity-sign certificates for \(8\leq N\leq40\);
- exact consecutive coefficient-ratio intervals for \(18\leq N\leq40\);
- regression against the R0.27 MPFR certificate through \(N=25\);
- the software environment and clean source commit.

This is a finite exact certificate.  It does not prove eventual sign
persistence, coefficient-ratio convergence, a dominant-singularity theorem,
or any Navier--Stokes regularity statement.

## Source state

- repository: Kasifa/Kasifa.github.io
- source commit: 99d95354c367bd520a0bc4846bcb93459dd88338
- source working tree at audit start: clean
- arithmetic: gmpy2 2.3.1 with GMP 6.3.0 rational numbers
- maximum parameter: \(N=40\)
- maximum leaf count: 119
- ordered scalar interactions: 5,484,501

## Reproduction

Install the pinned research environment, then run from the repository root
with fresh temporary output paths:

    python research/run_with_monitor.py \
      --output /tmp/r028-resources.csv \
      --interval 5 -- \
      python research/edge_rational_asymptotic_audit.py \
        --max-parameter 40 \
        --tail-count 12 \
        --progress \
        --progress-log /tmp/r028-progress.ndjson \
        --check \
        --pretty \
        --output /tmp/r028-edge-rational-asymptotic.json

The archived run took 28.93 seconds on an Apple M5 Max.  Its SHA-256 digest
is listed in `SHA256SUMS`.
