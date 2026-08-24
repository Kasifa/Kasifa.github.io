# Figure contract — fig-r070m-deformation-holonomy

## Question

Does the exact pullback by the strain-only propagator turn the covariance stretching
problem into an energy-controllable residual estimate?

## Claim encoded

Not in ordinary Euclidean normalized variables. A smooth four-pulse strain
history has zero signed matrix integral and zero covariance residual, yet its
time-ordered exponential is hyperbolic. The pulled covariance remains fixed
while the physical covariance approaches the rank-one anisotropy boundary.
Returning a general residual to the Euclidean frame costs a sharp
\(\kappa_2(G)^2\).

## Panel contract

- **A — Zero signed history.** Display the coefficients of the noncommuting
  generators \(A,C,-A,-C\) over four ordered segments. Directly state that
  both coefficient integrals vanish.
- **B — Hidden physical anisotropy.** Plot the exact rank-one gap
  \(2/3-\operatorname{tr}B_m^2\) for nine loop counts on a logarithmic axis.
  State that \(\widehat Q_m=I\) and label the exact one-loop gap.
- **C — Sharp optimized quotient.** For \(k=2,3,5\), plot
  \((\rho_G/\rho_0)/\kappa_2(G)^2\) against positive-definiteness parameter
  \(\varepsilon\). Retain the unit reference and distinguish every family
  without relying on color alone.

## Data and transformations

The loop states use exact rational matrix powers. Quotient values use the
closed exact least-squares formula after optimizing over the scalar amplitude
direction in both frames. Floating-point conversion is used only for
rendering. No random sampling, fitted curve, DNS, or PDE time integration is
allowed.

## Visual rules

- Double-column footprint, vector PDF/SVG, and 600 dpi PNG.
- Two non-neutral color roots at most.
- Line style, marker fill, direct labels, and reference lines must preserve
  the result in grayscale.
- Log scales must be explicit and contain only positive values.
- The PDE realization boundary must remain visible in the header.

## Claim boundary

The holonomy is an exact smooth matrix-history theorem. Each generator is
separately realizable as a periodic divergence-free initial strain, but the
ordered loop has not been embedded in one unforced finite-energy periodic NSE
trajectory. The rank-one affine-metric boundary is independently realized by
an exact smooth unforced periodic shear solution. The figure is not a
regularity or blow-up result.
