# R0.35 continuation-geometry certificate

This directory archives the formal R0.35 run from clean source commit
`c95c74eb19c36962b55de887ee75654a12e3a833`.

## Classification

The principal results are all-order statements for the reduced edge
generating equation:

- charge projection is Fourier projection under
  `(Z,W) -> (exp(-i theta)Z, exp(2i theta)W)`;
- a fixed-charge contour extracted from a polydisc exists exactly when
  `|R| < rho_Z^2 rho_W`;
- the origin charge projector and Euler fields do not retain their form under
  translation to a nonzero Taylor center;
- the raw nonlinear fixed-point map is unbounded on the unit ball of a
  same-radius weighted Wiener algebra;
- its bilinear polarization satisfies the outer-to-half-radius estimate
  `||B(f,g)||_(rho/2) <= (121/48)||f||_rho||g||_rho`.

The comparison with the high-cut R0.32 candidate hull is a finite exact
geometry diagnostic.  The candidate requires a balanced bivariate radius
between `0.908331313675102447...` and `0.908358242708991237...`, more than
18.3937 times the R0.31 radius `4/81`.  This does not prove that the candidate
is an original-function singularity or that a singularity-free continuation
path reaches it.

## Pinned inputs

```text
R0.31  32676dcefdf3c5285bdb18aab44bfdba385a84910d5e1d0df00f8ea9039ec395
R0.32  bd70ed05779631b729e89c269f82d287da361fdcea34e3c42703a712222f5575
```

## Formal command

Run from the repository root:

```text
python3 research/run_with_monitor.py \
  --output /tmp/r035-resources.csv --interval 0.02 -- \
  python3 research/edge_continuation_geometry_audit.py \
  --source-commit c95c74eb19c36962b55de887ee75654a12e3a833 \
  --progress --progress-log /tmp/r035-progress.ndjson \
  --check --pretty --output /tmp/r035-continuation-geometry.json
```

## Files

- `edge-continuation-geometry.json`: pinned inputs, exact projection and
  translation checks, same-radius witnesses, half-radius constants, rational
  cube-root enclosures, scope boundaries, and clean source state.
- `progress.ndjson`: append-only stage log.
- `resources.csv`: 0.02-second process-tree resource samples.
- `SHA256SUMS`: hashes of the archived files.

## Run summary

- Scientific wall time: 0.00625 seconds.
- Monitored wall time: 0.1 seconds.
- Resource samples: 3.
- Maximum sampled RSS: 23.969 MiB.
- GPU: not used; exact integer and rational arithmetic is too small to
  benefit from a remote accelerator.
- Random seed: none.
- Exact backend: Python integers and `Fraction`.
- All 9 formal checks passed.
- Certificate SHA-256:
  `13d147790926f3f3d04ea8f6d93574e1c992dd2b30dc6e12c777e68868a4fede`.

The result concerns a reduced formal edge system.  It contains no conclusion
about regularity or finite-time blow-up for the full three-dimensional
Navier--Stokes equation.
