# R0.73D finite kinetic-space diagnostics

This directory contains reproducible finite Fourier computations for the
static viscous spectral cluster.  The primary computation is performed after
the exact isometry

\[
 U_\mu=\mu^{-1/2}L_\mu^{-1/2}:X_\mu\to L^2,
 \qquad \mu=1/4.
\]

Consequently, the reported Euclidean projector norms are finite-compression
diagnostics for the physical kinetic-space norm, not raw-vorticity
\(L^2\) norms.

## Files

- `viscous_cluster_diagnostic.json`: 48 primary rows over four cutoffs and
  twelve viscosities;
- `progress.ndjson`: deterministic phase and row-level monitor events;
- `independent_validate.py`: independent matrix construction from the
  explicit Fourier coefficients of \(W_0\) and \(W_0''\);
- `independent_validation.json`: comparison of every primary row;
- `command.txt`: exact reproduction commands;
- `requirements.txt`: package versions used by the finite computation.

## Result boundary

At the largest cutoff \(N=128\), the leading finite eigenvalue moves from

\[
 0.156316407014908\quad(\varepsilon=10^{-2})
\]

to

\[
 0.170407962217171\quad(\varepsilon=10^{-8}),
\]

while the finite projector difference from \(\varepsilon=0\) decreases from
approximately \(5.62\times10^{-1}\) to \(3.09\times10^{-6}\).  The
\(N=96\) and \(N=128\) leading eigenvalues agree to less than
\(3\times10^{-15}\) on the frozen grid.

These values are diagnostics only.  They do not prove a continuum contour,
Riesz projection convergence, algebraic simplicity, a complementary
dichotomy, or nonautonomous transfer.  The continuum theorem is analytic and
is proved in `research/r073d_viscous_persistence_proof.md`.
