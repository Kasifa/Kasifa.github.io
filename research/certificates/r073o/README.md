# R0.73O finite Kolmogorov-spectrum diagnostic

This package checks one finite-dimensional numerical consequence of the
R0.73O forced Kolmogorov-flow contrast.  It is a reproducibility and
error-detection package, not a proof substitute.

For the normalized two-dimensional eigenproblem

\[
\sigma\Delta\phi-R^{-1}\Delta^2\phi
 +\sin Y\,(\Delta+I)\partial_X\phi=0,
\]

the package uses

\[
\alpha=0.7,\qquad R=3.012,
\]

which is the planar invariant slice of the three-dimensional equilibrium

\[
U_*=(30.12\sin(10y),0,0),\qquad
f_*=(3012\sin(10y),0,0).
\]

The producer forms a row-normalized tridiagonal Fourier matrix.  The
independent validator instead assembles the generalized pencil
\(Ac=\sigma Bc\) directly by source Fourier column and does not import the
producer.  Both paths check truncation convergence, the sign of the finite
spectral abscissa, the finite critical crossing, residuals, and the physical
scaling \(\lambda=AN\sigma\).

## Evidence boundary

The rigorous interval

\[
R_c\in[3.011528364444,3.011528364446]
\]

is an external computer-assisted theorem input.  This package does not
recompute or strengthen it.  A finite Fourier eigenvalue does not prove the
infinite-dimensional positive spectrum, nonlinear instability, an
essentially three-dimensional mechanism, finite-time singularity, or the
Clay problem.  The R0.73O analytic report carries the separate primary-source
argument for the infinite-dimensional spectral sign and the separate
Friedlander--Pavlovic--Shvydkoy nonlinear implication on the invariant
two-dimensional subspace.

Run the commands in `command.txt` from the repository root.  `--verify-only`
is fail-closed and performs no writes.  The dependency lock is exact; the
calculation is local and does not use a GPU or DGX.

## Two-stage provenance seal

Running `seal_package.py` without `--source-commit` produces the pre-seal
`hash-bound-uncommitted` state.  After the nine package source files have
been committed, run `seal_package.py --source-commit <40-hex>` and then its
`--verify-only` form.  Final sealing succeeds only if that commit exists and
contains byte-identical regular blobs for all nine source bindings.  The
sealer never substitutes the current `HEAD` for an explicit commit.
