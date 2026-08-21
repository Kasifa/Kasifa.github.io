# R0.69V common-sample annular polynomial QMC

This archive records the primary full-annulus amplitude scan at separation
`epsilon = 1/4`.  Every annular carrier is reconstructed as a cubic in the
outer amplitude from the four common nodes `0, 1/3, 2/3, 1`.  The exact local
production polynomial supplies the signed numerator; randomized QMC supplies
the individual annular means and their absolute-value sum.

The source is locked to commit
`2895a99b2448f8102663e238e68d3c4a5a3504c6`.

## Reproduce

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069v-polynomial-qmc/resources.csv \
      --interval 1 -- \
      tmp/r068b-venv/bin/python research/two_scale_annular_polynomial_qmc.py \
      --output-root research/certificates/r069v-polynomial-qmc \
      --replicates 16 --power 18 --separation 2 --j-padding 6 \
      --amplitude-grid 4001 \
      --source-commit 2895a99b2448f8102663e238e68d3c4a5a3504c6

The run evaluated 167,772,160 stratified point pairs, exited with code zero
after 334.399 seconds, reached 100.0% CPU and 1012.375 MiB resident memory, and
used no NVIDIA GPU.  Sample-level cubic reconstruction residual was
`1.3322676295501878e-15`; all four sampled total coefficients were within
`0.64` reported standard errors of their deterministic values.

## Main observation

The dense scan selected `a = 0.1595`.  Its exact signed total is
`0.021157876459851562`; the QMC annular `ell^1` sum of means is
`0.021958170413693592`, giving the screening ratio `0.9635537051236769`.
One mean annulus remained negative.  The candidate's sampled total agreed with
the exact total to `0.0223` reported standard errors.

The importance parameterization has relatively high variance on the coarse
outer-transition self-pairs.  The independent zone-pair archives therefore
control the coarse-annulus interpretation used in the research note.

## Claim boundary

The ratio is an exploratory estimator using means, not an interval enclosure.
The scan is data-selected and its pointwise scramble intervals are not
simultaneous.  This archive does not prove sign saturation, a uniform gap,
Navier--Stokes regularity, or singularity.
