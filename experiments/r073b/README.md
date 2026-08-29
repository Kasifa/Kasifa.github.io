# R0.73B finite weighted-propagator screen

This directory contains a deterministic, one-thread Fourier--Galerkin screen
for the special `beta=xi=0` Orr--Sommerfeld row in the R0.73A hidden-mean
coordinates. The producer measures 280 propagators in seven norms. The
validator is independent code: it does not import the producer, rebuilds the
raw-q and `(h,r)` matrices, reruns selected integrations, extends the small-gap
grid, and checks the physical kinetic bound on both generator and propagator.
`contract.json` fixes row counts, norm weights, numerical policy, field groups,
and the fail-closed claim boundary consumed by the validator.

The essential finite findings are:

- for `c=mu^p`, raw q displays the sampled exponent `(1-p)_+`;
- in the diagonal family `|h|^2+mu^-a ||L^-b/2 r||^2`, the sampled exponent is
  `(a/2-p)_+`;
- the physical kinetic weight `(a,b)=(1,1)` is bounded on fixed-Lambda paths
  (`p=1/2`) and grows like `mu^-1/2` on fixed nonzero-c paths (`p=0`);
- fixed-Lambda gains converge to the explicit triangular finite-matrix limit;
- every sampled kinetic row obeys the analytic energy majorant.

The CSV and JSON files do not establish an infinite-dimensional theorem. They
contain no Galerkin tail enclosure, interval arithmetic, Squire row, Bloch
direct sum, nonlinear estimate, or Navier--Stokes regularity result.
