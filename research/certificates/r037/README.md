# R0.37 weighted-restart certificate

This directory archives the formal R0.37 run from clean source commit
04e62468f383d5e07c572ffd89561ee46dc249b8.

## Classification

The all-order theorem works on the active support cone `q=2k-n>=-1` with
the one-degree weighted Wiener norm

~~~text
||f||_(B_r) = sum_(n,k) (n+k) |f_(n,k)| r^(n+k).
~~~

Charge symmetrization and `(i+j) min(i,j) <= 2ij` give

~~~text
||Phi(f)||_(B_r)       <= 3 ||f||_(B_r)^2,
||D Phi(f) h||_(B_r)  <= 6 ||f||_(B_r) ||h||_(B_r).
~~~

Together with the R0.31 all-order majorant, this proves that the infinite
Jacobian `I-D Phi(a)` is invertible throughout the old radius.  The universal
Neumann inverse bound is 81.  Replacing the first 40 majorant layers by their
exact values improves the boundary inverse bound to approximately
3.306364997.

The exact degree-40 restart uses

~~~text
old radius       = 4/81
new radius       = 16/243
radius gain      = 4/3
fixed-charge gain= 64/27
~~~

At the new radius, the degree-40 polynomial norm is approximately
0.15865694927073254, the derivative bound is approximately
0.95194169562439524, and the complete degree-41-through-80 residual norm is
approximately 2.99904918794896e-46.  The rational contraction ball has radius
approximately 0.004004858697967064 and Lipschitz upper bound approximately
0.9759708478121976.  The exact residual occupies about 2.08e-42 of the
available allowance.

The same fixed point satisfies an active-field norm bound of approximately
0.16266180796869960.  The normalized transport operator then has norm at
most approximately 0.32532361593739921, so the canonical normalized U and V
fields are constructed on the same new radius.

## Pinned inputs

~~~text
R0.31  32676dcefdf3c5285bdb18aab44bfdba385a84910d5e1d0df00f8ea9039ec395
R0.36  dfe0395df8b9654f235207c71dda5a0de8a70a54908b76b92dca00ad83c38e48
~~~

## Formal command

Run from the repository root:

~~~text
tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output /tmp/r037-resources.csv --interval 0.05 -- \
  tmp/r024-venv/bin/python research/edge_weighted_restart_audit.py \
  --max-total-degree 40 --pair-audit-degree 12 --jacobian-degree 12 \
  --source-commit 04e62468f383d5e07c572ffd89561ee46dc249b8 \
  --progress --progress-log /tmp/r037-progress.ndjson \
  --check --pretty --output /tmp/r037-edge-weighted-restart.json
~~~

The local virtual environment supplies gmpy2.  Any environment with the same
exact GMP rational backend can reproduce the mathematical output.

## Files

- `edge-weighted-restart.json`: pinned inputs, all-order formulas, exact
  contraction inequalities, support-pair regression, negative scope witness,
  finite Jacobian hashes, checks, and environment.
- `progress.ndjson`: append-only six-stage progress log.
- `resources.csv`: 0.05-second process-tree resource samples.
- `SHA256SUMS`: hashes of the archived files.

## Run summary

- Scientific wall time: 0.765986 seconds.
- Monitored wall time: 0.859766 seconds.
- Resource samples: 14.
- Maximum sampled CPU: 94.2 percent.
- Maximum sampled RSS: 36.797 MiB.
- Exact recurrence interactions: 68,664.
- Exact admissible ordered support pairs: 4,096.
- Exact finite Jacobian dimension: 62.
- GPU: not used; this is a short serial exact-rational workload.
- Random seed: none.
- Exact backend: GMP rational arithmetic through gmpy2.
- All 13 formal checks passed.

## Boundary

The support restriction is essential.  Outside `q>=-1`, the exact pair
`W^2,Z^3` violates the mixed constant-three estimate by the factor `7/4`.
The result concerns a reduced edge generating system.  It does not reach the
finite R0.32 Pade candidate, identify a singularity, or prove regularity or
finite-time blow-up for the full three-dimensional Navier--Stokes equation.
