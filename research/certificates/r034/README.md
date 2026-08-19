# R0.34 polynomial-background obstruction certificate

This directory archives the formal R0.34 run from clean source commit
`11cb3c386814a4d725944251a2d46faef0f5c53c`.

## Classification

The principal result is an **exact universal non-representation theorem for
four finite-dimensional background classes**.  The degree thresholds are
finite coefficient-window results.

For

```text
C(x) = P_d(x) + integral_[0,infinity) dmu(t)/(1-x*t),  mu >= 0,
```

where `P_d` is any real polynomial, the following classes are excluded:

```text
B_U: every degree d <= 43   witness shift 44, order 3
B_V: every degree d <= 44   witness shift 45, order 3
H_U: every degree d <= 46   witness shift 47, order 1
H_V: every degree d <= 45   witness shift 46, order 2
```

The coefficients of `P_d` are not fitted or restricted.  At every tail shift
`s>d`, the polynomial leaves the matrix
`(c_(s+i_alpha+i_beta))` unchanged.  A nonnegative measure would make this a
positive-semidefinite Gram matrix, but the archived exact determinant is
negative in each case.

The theorem excludes all polynomial coefficient choices through the stated
degrees.  The statement that these are the largest witnessed degrees is only
an exhaustive fact inside the 50/49-coefficient window searched from tail
shift 40.  The result does not prove that any higher-degree background works,
does not exclude a genuinely infinite analytic background, and has no direct
three-dimensional Navier--Stokes regularity consequence.

## Pinned inputs

The audit requires these upstream certificate hashes:

```text
R0.32  bd70ed05779631b729e89c269f82d287da361fdcea34e3c42703a712222f5575
R0.33  ccbf8ab05615378f6d4b9824e86b679b6d0df2882cbc6e563b063b8769292367
```

## Formal command

Run from the repository root inside the research Python environment:

```text
python research/run_with_monitor.py \
  --output /tmp/r034-resources.csv --interval 0.02 -- \
  python research/edge_polynomial_background_audit.py \
  --minimum-tail-start 40 \
  --progress --progress-log /tmp/r034-progress.ndjson \
  --check --pretty --output /tmp/r034-polynomial-background.json
```

## Files

- `edge-polynomial-background.json`: provenance, exact theorem statements,
  full rational witness matrices and determinants, every tested tail
  principal minor, finite-window maximality diagnostics, checks, environment,
  and clean source state.
- `progress.ndjson`: append-only stage log.
- `resources.csv`: 0.02-second process-tree resource samples.
- `SHA256SUMS`: hashes of the archived files.

## Run summary

- Scientific wall time: 0.0722 seconds.
- Monitored wall time: 0.3 seconds.
- Maximum sampled CPU: 47.7%.
- Maximum sampled RSS: 77.812 MiB.
- GPU: not used; this small exact rational audit would not benefit from a
  remote accelerator.
- Random seed: none.
- Exact backend: Python `Fraction`, SymPy domain determinants, and independent
  `Fraction` Leibniz determinants for all four theorem witnesses.
- All 8 formal checks passed.

