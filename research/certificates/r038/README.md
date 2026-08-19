# R0.38 tail-aware Newton certificate

This directory archives the formal R0.38 run from clean source commit
bc230622aeac611966c091c4beca734c783f65ac.

## Classification

The all-order theorem works on the active support cone q>=-1 in the
one-degree weighted Wiener space from R0.37.  If p_N has degrees at most N
and h has degrees strictly above N, the disjoint supports sharpen the
derivative estimate to

~~~text
||D Phi(p_N) h||_(B_r)
  <= 3 (M_N(r) + S_N(r)/(N+1)) ||h||_(B_r),

M_N(r) = sum_i i   ||(p_N)_i||_1 r^i,
S_N(r) = sum_i i^2 ||(p_N)_i||_1 r^i.
~~~

The proof covers every uncomputed tail degree.  It uses the R0.37
mixed-layer theorem and total-degree separation, not a finite matrix or
tail-column extrapolation.

The exact degree-80 restart uses

~~~text
R0.37 radius          = 16/243
R0.38 radius          = 59/500
bivariate gain        = 14337/8000 = 1.792125
fixed-charge gain     = 5.755789396001953125
~~~

At the new radius, the degree-80 polynomial norm is approximately
0.32561381732092066.  The old full-space derivative bound is approximately
1.953682903925524 and therefore fails.  The tail-aware all-order bound is
approximately 0.9924959984799435, leaving the exact positive margin
0.007504001520056506.

The complete 6345-term residual occupies degrees 81 through 160 and has norm
approximately 7.463302564998892e-70.  It uses approximately 2.12e-64 of the
available contraction allowance.  The ball Lipschitz upper bound is
approximately 0.9962479992399717.

The same fixed point gives a transport-operator upper bound of approximately
0.6524783015618507, so the canonical normalized U and V fields are
constructed at the same radius.

## Low-block preconditioner audit

The pinned degree-12 support-cone Jacobian is the same 62-dimensional exact
block as in R0.37.  Its inverse passes on both sides and both matrix hashes
match.

For a correction supported above degree 80, however, both J h and
D Phi(p_80) h remain above degree 80.  The natural preconditioner

~~~text
A = P_12 (P_12 J P_12)^(-1) P_12 + (I-P_12)
~~~

therefore acts as the identity on the certified correction space.  It does
not reduce the tail defect.  The radius gain comes from the all-order
tail-aware inequality.

## Negative and finite controls

- At the nearby radius 19/160, the same sufficient tail bound is
  approximately 1.0007181485912454 and does not close.  This is a failure of
  the sufficient inequality, not proof of nonanalyticity.
- The 55 exact degree-81 tail columns have maximum weighted ratio
  approximately 0.16577696827316245.  This is a finite regression only.
- The maximum finite column is W^81.
- The finite R0.32 transport-candidate cluster remains more than
  approximately 456.128 times outside the proved fixed-charge disk.  It is
  not certified as a singularity.

## Pinned inputs

~~~text
R0.32  bd70ed05779631b729e89c269f82d287da361fdcea34e3c42703a712222f5575
R0.37  a4fe36192b80112c282b9388da65ffca625f7a84d0b64f294b24352f92870eda
~~~

## Formal command

Run from the repository root:

~~~text
tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output /tmp/r038-resources.csv --interval 0.1 -- \
  tmp/r024-venv/bin/python research/edge_tail_newton_audit.py \
  --max-total-degree 80 --target-radius 59/500 \
  --low-block-degree 12 --tail-column-degree 81 \
  --source-commit bc230622aeac611966c091c4beca734c783f65ac \
  --progress --progress-log /tmp/r038-progress.ndjson \
  --check --pretty --output /tmp/r038-edge-tail-newton.json
~~~

The local virtual environment supplies gmpy2.  Any environment with the same
exact GMP rational backend can reproduce the mathematical decisions.

## Files

- edge-tail-newton.json: pinned inputs, all-order formulas, exact contraction
  inequalities, low-block audit, finite tail regression, candidate scale
  comparison, checks, digests, and environment.
- progress.ndjson: append-only seven-stage scientific progress log.
- resources.csv: 0.1-second process-tree resource samples.
- SHA256SUMS: hashes of every archived file.

## Run summary

- Scientific wall time: 30.290959 seconds.
- Monitored wall time: 30.388580 seconds.
- Resource samples: 253.
- Maximum sampled CPU: 100.0 percent.
- Maximum sampled RSS: 45.281 MiB.
- Exact recurrence interactions: 1113168.
- Degree-80 polynomial terms: 2161.
- Complete residual terms: 6345.
- Exact finite tail columns: 55.
- Exact low-block dimension: 62.
- GPU: not used; this is a short serial exact-rational workload.
- Random seed: none.
- Exact backend: GMP rational arithmetic through gmpy2.
- All 17 formal checks passed.

## Boundary

The theorem concerns a reduced edge generating equation on the active
support cone.  It does not reach the finite R0.32 candidate, identify a
singularity, or prove regularity or finite-time blow-up for the full
three-dimensional Navier--Stokes equation.
