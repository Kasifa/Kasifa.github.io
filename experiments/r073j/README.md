# R0.73J continuum spectral-branch computation package

This package is the formal continuous-operator contour calculation for the
periodic planar row

\[
(\beta,\xi,\gamma)=(0,0,1/2),\qquad 0\le d\le1/450.
\]

The primary program evaluates the monodromy with Arb ball arithmetic on a
two-variable Chebyshev grid.  The accepted analysis uses outward-rounded
interval Clenshaw evaluation plus analytic Bernstein-ellipse remainders on a
complete dyadic real-box cover.  It covers every point of the outer rectangle
and the local circle for every real `d` in the frozen interval.

The outer rectangle is

\[
11/100\le\operatorname{Re}\lambda\le19/50,
\qquad |\operatorname{Im}\lambda|\le19/50,
\]

and the local circle is

\[
|\lambda-17/100|=3/1000.
\]

The analysis also restricts the validated tensor polynomial to `d=0`, builds
a rational polygon, verifies a convex half-plane homotopy cell by cell, and
computes the polygon winding with exact rational ray crossing.  A binary64
phase sum is not used for the primary decision.

The companion overlap certificate covers the full rectangle

\[
0\le d\le1/450,\qquad 167/1000\le\lambda\le173/1000,
\]

and proves normalized kinetic left-right overlap greater than `0.585343`
and a nonzero fixed phase anchor.  An independent centre-Lipschitz analysis
from the shared raw grid gives the lower bound `0.585009`.

## Independent audits

`independent_validate.py` and `independent_validate_overlap.py` reimplement
the post-processing without importing the primary analyzers.  They share the
frozen raw ODE grids and are classified as independent post-processing, not
fully independent ODE proofs.

The natural-parameter-box audit uses a separate 120-digit, Taylor-order-14
interval ODE implementation with 2048/1024 steps.  Its history is deliberately
append-only:

- the initial fixed-width run passed 76 of 83 selected boxes and left seven
  wrapping-inconclusive;
- the complete depth-two refinement resolved one of those seven parents and
  left 96 inconclusive leaves;
- the final adaptive refinement passed all 2,896 final leaves by depth five,
  with minimum Evans lower bound greater than `0.00714950`.

The 83 boxes are corroborative spot checks.  They do not replace the complete
parameter-uniform contour certificate.

## Proof boundary

The computation closes the contour, winding, overlap, and phase-anchor inputs.
Algebraic multiplicity still comes from the separately audited analytic
kinetic-operator/periodic-pencil bridge.  The assembled result certifies one
planar periodic continuum-operator spectral branch.  It does not certify a
viscous branch, a nonselfadjoint adiabatic remainder, transverse 3D closure,
finite-time singularity, or the Clay problem.

## Reproduction

The exact commands are in `command.txt`.  A primary run checkpoints every
complete panel atomically in `contour_grid_checkpoint.json`, appends progress
to `progress.ndjson`, and appends machine resource observations to
`resources.ndjson`.  A checkpoint resumes only when its configuration and
source digest match exactly.  Overlap and all three natural-box stages keep
separate progress and resource logs.

The pinned arithmetic dependency is `python-flint==0.6.0`.  The formal
configuration uses 80 decimal digits, Taylor order 12, 16 worker processes,
1024 ODE steps for the outer contour, and 512 ODE steps for the local circle.
`seal_package.py` binds the sources and evidence to an immutable source
commit; `validate_package.py --require-commit` verifies that binding and the
flat SHA-256 inventory.
