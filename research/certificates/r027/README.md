# R0.27 scalar edge generating-equation certificate

This directory archives the formal dual-precision computation used in R0.27.
The exact negative-edge scalar recurrence is evaluated through \(N=75\), or
225 leaves, at 160 and 224 MPFR bits.

The certificate records:

- the exact scalar and generating-equation conventions;
- every charge-one endpoint for \(2\leq N\leq75\);
- the charge-zero ray through \(N=75\);
- regression against all R0.26 negative-edge endpoints through \(N=25\);
- the relative discrepancy between the two precision levels;
- descriptive finite-tail fits and threshold indices;
- the software environment and clean source commit.

The computation is finite.  It does not prove
\(|\sigma_{B,N}|\to1\), a dominant-singularity theorem, or any
Navier--Stokes regularity statement.

## Source state

- repository: Kasifa/Kasifa.github.io
- source commit: 4d6cc6e0dff8da28998ff9cc9e777af795feafae
- source working tree at audit start: clean
- arithmetic: gmpy2 2.3.1, MPFR 4.2.2
- precisions: 160 and 224 bits
- internal scale: \(4^{-L}\), which leaves the reported normalized quantities
  invariant

## Reproduction

Install the pinned research environment, then run from the repository root
with fresh temporary output paths:

    python research/run_with_monitor.py \
      --output /tmp/r027-resources.csv \
      --interval 5 -- \
      python research/edge_generating_function_audit.py \
        --max-parameter 75 \
        --precisions 160 224 \
        --progress \
        --progress-log /tmp/r027-progress.ndjson \
        --check \
        --pretty \
        --output /tmp/r027-edge-generating-function.json

The archived run took 63.46 seconds on an Apple M5 Max and reached a maximum
relative discrepancy of \(3.21\times10^{-43}\).  The SHA-256 digest of the
certificate is listed in SHA256SUMS.
