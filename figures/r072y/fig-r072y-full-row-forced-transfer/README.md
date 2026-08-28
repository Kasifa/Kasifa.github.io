# R0.72Y full-row and forced-transfer figure

This package is the reproducible, double-column three-panel figure source for
R0.72Y.  It separates three different statements that must not be conflated:

1. the exact Fourier-row and Orr-Sommerfeld/Squire algebra;
2. an exact zero-streamwise-coupling lift-up counterexample to uniform strict
   contraction; and
3. the proved scalar forced-transfer powers in standard and semiclassical
   negative norms.

Panels B and C sample closed formulas only.  No PDE solver, regression, random
seed, or fitted exponent is used.  The sampled rows exist so that every plotted
mark can be recomputed and checked; the analytic proofs live in the bound
R0.72Y report and independent audits.

The current generated manifest is deliberately `draft` until the R0.72Y source
and certificate commits exist.  A formal render requires two distinct clean
commits, with the certificate commit descending from the source commit.  The
formal command also requires an explicit visual-inspection flag.  The plotting
script refuses to overwrite an already formal package.

The chart uses two chromatic roots plus neutrals.  Dash pattern, marker shape,
open fill, direct labels, and panel structure make every distinction survive
grayscale printing.
