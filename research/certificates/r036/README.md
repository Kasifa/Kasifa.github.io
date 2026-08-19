# R0.36 short-continuation certificate

This directory archives the formal R0.36 run from clean source commit
e8685f41005a3149ebff91e9f4d537b02dbacb00.

## Classification

The all-order part proves a conjugated outer-to-inner estimate for the
reduced active fixed-point map.  If a local center has componentwise modulus
|c|, local outer radius R, and local inner radius r, set

~~~text
S = R - |c|,  s = r + |c|,  lambda = max_i(s_i / S_i).
~~~

When lambda is below one,

~~~text
||Phi_c(f)-Phi_c(g)||_r
<= C(lambda)(||f||_R+||g||_R)||f-g||_R,

C(lambda) = (11/3) M1(lambda)(M2(lambda)+M1(lambda)^2),
Mj(lambda) = sup_(n>=0) n^j lambda^n.
~~~

The certified short step uses

~~~text
rho_* = 4/81
c     = (rho_*/7, -rho_*/7)
r     = rho_*/7
R     = 5 rho_*/7
lambda = 1/2
C(1/2) = 121/48.
~~~

The entire outer local disc remains inside the R0.31 polydisc, and the
affine charge orbit of the inner local disc remains inside the declared
outer disc.  The center has fixed-charge coordinate
-64/182284263, whose modulus is 1/343 of the R0.31 fixed-charge radius.

The R0.31 all-order majorant places the translated exact solution in an
inner Wiener ball of radius approximately 9.89901e-29 around the exact
translated degree-40 polynomial.  The finite exact conjugated residual norm
is approximately 2.41835e-75; an independent all-order upper bound is
approximately 5.39341e-8.

The finite regression reconstructs 40 active layers with 68,664 ordered
recurrence interactions, checks five conjugated charge projectors, and
constructs a 42-dimensional exact two-sided Jacobian-block inverse.  That
finite inverse is not an inverse for the infinite operator and does not
certify a Newton ball outside R0.31.

## Pinned inputs

~~~text
R0.31  32676dcefdf3c5285bdb18aab44bfdba385a84910d5e1d0df00f8ea9039ec395
R0.35  13d147790926f3f3d04ea8f6d93574e1c992dd2b30dc6e12c777e68868a4fede
~~~

## Formal command

Run from the repository root:

~~~text
python3 research/run_with_monitor.py \
  --output /tmp/r036-resources.csv --interval 0.2 -- \
  tmp/r024-venv/bin/python research/edge_short_continuation_audit.py \
  --max-total-degree 40 --jacobian-degree 8 \
  --source-commit e8685f41005a3149ebff91e9f4d537b02dbacb00 \
  --progress --progress-log /tmp/r036-progress.ndjson \
  --check --pretty --output /tmp/r036-edge-short-continuation.json
~~~

The local virtual environment supplies gmpy2; any environment with the same
exact GMP rational backend can reproduce the mathematical output.

## Files

- edge-short-continuation.json: pinned inputs, exact geometry, all-order
  formulas and enclosures, finite polynomial regressions, Jacobian-block
  inverse hashes, scope, and environment.
- progress.ndjson: append-only six-stage progress log.
- resources.csv: 0.2-second process-tree resource samples.
- SHA256SUMS: hashes of the archived files.

## Run summary

- Scientific wall time: 14.5704 seconds.
- Monitored wall time: 14.7 seconds.
- Resource samples: 68.
- Maximum sampled CPU: 100.0 percent.
- Maximum sampled RSS: 37.656 MiB.
- GPU: not used; the run is a small, serial exact-rational workload.
- Random seed: none.
- Exact backend: GMP rational arithmetic through gmpy2.
- All 12 formal checks passed.

The result concerns a reduced formal edge system.  It does not leave the
R0.31 analytic domain, reach the finite R0.32 Padé candidate, or prove
regularity or finite-time blow-up for the full three-dimensional
Navier--Stokes equation.
