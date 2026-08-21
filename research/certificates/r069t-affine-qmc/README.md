# R0.69T affine-core annular QMC certificate

This archive records the exploratory signed Biot--Savart boundary-carrier
quadrature for the compact affine-core field in R0.69T.

- Exact core production: `8*pi/(3*sqrt(6)) = 3.4201328804316375`.
- Quadrature: 16 independently scrambled five-dimensional Sobol replicates.
- Finest resolution: `2^22` pairs per replicate, 67,108,864 pairs total.
- Finest mean: `3.419001359623872`.
- Scramble standard error: `0.000530335805987068`.
- Difference from the exact value: `-0.0011315208077653516`, or `-2.1336`
  reported scramble standard errors.
- Annular cancellation ratio for the core boundary carrier, excluding the
  numerically zero near remainder: `0.9964780845826579`.
- Only the outermost displayed annulus, `j=1`, has a statistically resolved
  negative mean: `-0.006041996199753805`.
- Samplewise annular reconstruction residual: below `1e-12`.

The scientific process log is `progress.ndjson`; independent process-tree
monitoring is in `resources.csv`. The run used one CPU process, reached 100%
observed CPU, peaked at 2045.141 MiB RSS, used no NVIDIA GPU, and exited zero.

Run command:

```text
python research/run_with_monitor.py \
  --output research/certificates/r069t-affine-qmc/resources.csv \
  --interval 1 -- \
  python research/affine_core_annular_qmc.py \
  --output-root research/certificates/r069t-affine-qmc \
  --replicates 16 --power 22 --refinement-powers 18,20,22
```

This is randomized quasi-Monte Carlo evidence, not an interval enclosure.
It proves no universal annular depletion theorem, no Navier--Stokes regularity
criterion, and no solution of the Millennium Problem.
