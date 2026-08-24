# Figure contract — fig-r070l-source-compensator

## Question

Can the actual strain-source equation produce a universal sign for
\(q=\Sigma:B\) once the source and normalized covariance are matched?

## Claim encoded

No. The two exact smooth periodic initial data have the same
\(\Sigma,B,q\), kinetic energy, source quadratic, source viscosity, and
normalized covariance derivative. Their center pressure Hessians differ and
give

\[
\dot q_-=\frac{3901}{2040}>0,\qquad
\dot q_+=-\frac{1283}{2040}<0.
\]

## Panel contract

- **A — Matched state, different pressure orientation.** Plot the three
  diagonal pressure-Hessian entries for both witnesses and the common
  diagonal entries of \(B\) in a separate inset scale. Show the shared
  off-diagonal entry \(H_{12}=-152/65\) as a direct note.
- **B — Exact derivative ledger.** Group the four contributions
  \(1/6,-1,197/120,-H:B\), retain the zero line, and display each total as a
  distinct marker. The three nonpressure bars must coincide exactly.

## Data and transformations

Every plotted value is an exact rational number generated from the finite
Fourier witness. Floating-point conversion is only for rendering. No
statistical aggregation, fit, PDE time integration, or random sampling is
allowed.

## Visual rules

- Double-column footprint, vector PDF/SVG, and 600 dpi PNG.
- Two color roots at most.
- Line style, marker shape/fill, hatching, direct values, and the zero line
  must preserve the result in grayscale.
- The claim boundary must remain visible in the figure header.

## Claim boundary

This is an exact initial-face sign witness and a structural local-compensator
obstruction. It is not DNS, a long-time trajectory, a regularity criterion,
or a solution of the Millennium problem.
