# R0.69V zone-pair polynomial root-gap audit

This archive reconstructs the `j = -2` and `j = 0` coarse-annulus carriers as
cubic polynomials in the outer amplitude.  It uses all ten unordered radial
zone pairs and four common amplitude nodes, independently of the primary
displacement-importance scan.

The source is locked to commit
`ba569f3832d93a6f286bb90d92d2d7b15478bf23`.

## Reproduce

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069v-zonepair-polynomial-qmc/resources.csv \
      --interval 1 -- \
      tmp/r068b-venv/bin/python research/two_scale_zonepair_polynomial_qmc.py \
      --output-root research/certificates/r069v-zonepair-polynomial-qmc \
      --replicates 16 --power 18 --separation 2 --indices=-2,0 \
      --amplitude-grid 4001 \
      --source-commit ba569f3832d93a6f286bb90d92d2d7b15478bf23

The run evaluated 41,943,040 common-sample point pairs, exited with code zero
after 83.633 seconds, reached 100.0% CPU and 937.688 MiB resident memory, and
used no NVIDIA GPU.  Sample-level cubic reconstruction residual was
`1.5543122344752192e-15`.

## Root-gap diagnostic

The `j = 0` mean polynomial is

    a(-0.0016401859039318904
      + 0.004131459799856901 a
      - 0.13605131640559034 a^2).

Its quadratic factor has negative mean discriminant and negative leading
coefficient, so the mean polynomial is negative for every `a > 0`.  At
`a = 0`, the `j = -2` mean is
`-0.001946783996464467 +/- 8.677972585209608e-5`.

On the 4001-point grid, no amplitude makes both mean carriers nonnegative.
The best minimum mean is still `-0.00029486752127560415` at `a = 0.107`, and
at every grid point at least one pointwise 95% upper scramble band is below
zero.

## Claim boundary

This is a strong randomized root-gap diagnostic, not a simultaneous interval
certificate.  Turning it into a theorem requires rigorous enclosures for the
three nonzero `j = 0` coefficients and the negative `j = -2` constant term.
It does not prove a dynamical Navier--Stokes estimate or solve the Millennium
Problem.
