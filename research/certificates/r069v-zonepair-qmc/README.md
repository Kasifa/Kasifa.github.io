# R0.69V fixed-candidate zone-pair QMC cross-check

This archive independently evaluates the candidate `epsilon = 1/4`,
`a = 0.1595` by sampling all ten unordered radial zone pairs directly.  It is
designed to resolve the coarse annuli, especially the outer-transition
self-pair, rather than the near-distance singular kernel.

The source is locked to commit
`2895a99b2448f8102663e238e68d3c4a5a3504c6`.

## Reproduce

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069v-zonepair-qmc/resources.csv \
      --interval 1 -- \
      tmp/r068b-venv/bin/python research/two_scale_full_annular_qmc.py \
      --output-root research/certificates/r069v-zonepair-qmc \
      --replicates 16 --power 19 --separations 2 \
      --amplitude-laws fixed:0.1595 --j-padding 6 \
      --source-commit 2895a99b2448f8102663e238e68d3c4a5a3504c6

The run evaluated 83,886,080 zone-pair samples, exited with code zero after
243.058 seconds, and retained all transition--transition pairs.  The exact
sample partition residual was zero.  Peak monitored CPU and resident memory
are recorded in `resources.csv`.

## Main cross-check

For the coarse annuli the direct estimator gives

- `j = -1`: `-6.371850480254573e-5 +/- 7.229479685274118e-5`;
- `j = 0`: `-6.29186090035789e-4 +/- 1.034313670418529e-5`;
- `j = 1`: `8.161292323402724e-5 +/- 1.6093360534896416e-6`.

Here `+/-` denotes one independent-scramble standard error.  The `j = 0`
negative sign is about 61 reported standard errors from zero and confirms that
the near-saturation candidate is not all one sign.

## Claim boundary

Direct zone-pair sampling is noisy for fine annuli and the complete singular
kernel; those outputs are retained as a negative estimator comparison.  The
coarse-annulus errors are randomized diagnostics, not rigorous intervals.
