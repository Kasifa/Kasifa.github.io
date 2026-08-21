# R0.69U finite-radius dyadic QMC certificate

This archive records the finite-radius randomized quasi-Monte Carlo companion
to the exact R0.69U core-saturation theorem.  The executable source is locked
to commit `29ca62f2667816cb26564b2791251a9d2e68197c` and SHA-256
`3516720be82e4c7c97e42295c5e86ad6c6199b6a0c8cfe74b33d738dd6cc7828`.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069u-dyadic-qmc/resources.csv \
      --interval 0.10 -- \
      tmp/r068b-venv/bin/python research/affine_core_dyadic_qmc.py \
      --output-root research/certificates/r069u-dyadic-qmc \
      --replicates 16 --power 18 \
      --radius-powers 0,1,2,3,4,5,6 \
      --source-commit 29ca62f2667816cb26564b2791251a9d2e68197c

The run used 16 independent scrambled Sobol replicates and `2^18` pairs per
replicate at each of the seven radii `R=1,2,4,8,16,32,64`: 4,194,304 pairs
per radius and 29,360,128 evaluated pairs in total.  Axial covariance reduced
the point-pair integral from six dimensions to five.

The monitored process exited with code zero after 79.594495 seconds.  Its
maximum observed CPU utilization was 100.0%, peak resident set size was
669.969 MiB, and no NVIDIA GPU was present.  The exact samplewise annular
partition residual was zero; the maximum reconstruction residual was
`8.881784197001252e-16`.

## Main finite-radius observations

The analytic core production is `3.4201328804316375`.  At `R=64`, the QMC
mean was `3.4201322121361635` with scramble standard error
`8.598056704213007e-7`.  The two surviving reported annuli were
`3.336162372184349` and `0.08396983995181467`; the theoretical mollified-profile
limits are `3.336321860269419` and `0.08381102016221852`.

The reported core cancellation ratios were:

- `R=1`: `0.9959200564387795`;
- `R=2`: `0.9998334458652298`;
- `R=4`: `0.9999995744984411`;
- `R=8`: `0.9999999999984578`;
- `R=16,32,64`: `1.0` at binary64 output precision.

Only the exact theorem proves eventual saturation.  In particular, the
analytic carrier support gives a deterministic two-annulus regime once the
dyadic radius is sufficiently large; the displayed floating-point ratios do
not replace that argument.

## Decision boundary

This archive is exploratory randomized quadrature for finite radii.  It is
not an interval enclosure and does not prove full-space annular saturation.
The full-space ratio is invariant under this self-similar dilation, so the
next nonredundant experiment must change the radial shape and include all
transition-transition pairs.  Nothing here proves global regularity,
finite-time singularity, or the Millennium Problem.
