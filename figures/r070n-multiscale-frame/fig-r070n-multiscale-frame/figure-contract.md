# Figure contract — fig-r070n-multiscale-frame

## Question

Can nonnegative summation of scalar-filtered vorticity covariances across
scales, centers, or times create a universal positive three-dimensional
frame?

## Claim encoded

No.  A componentwise scalar filter preserves every fixed target-space
subspace.  Exact periodic shear remains rank one, and a one-axis real helical
wave remains rank two, under every nonnegative aggregation.  Positive
definiteness requires genuinely nonparallel observed directions and a
quantitative balance; it is not forced by trace, smoothness, sample count, or
full rank at one datum.

## Panel contract

- **A — Exact normalized spectra.** Compare the rank-one shear spectrum, the
  rank-two one-axis helical spectrum, and a balanced two-axis helical positive
  control.  State each optimal frame constant.
- **B — Minimal helical escape.** Plot the exact two-axis formula
  \[
  c_*(r,\theta)
  =\frac{1-\sqrt{1-4r(1-r)\sin^2\theta}}4
  \]
  for four fixed nonzero axis angles.  Preserve the energy-balance symmetry
  \(r\leftrightarrow1-r\).
- **C — Full rank without a uniform constant.** Plot the exact whole-space
  Schwartz-family quotient \(1/(8L^2+2)\) for \(1\le L\le100\), with its
  \(1/(8L^2)\) asymptotic reference.
- **D — Count is not direction.** Show that repeated positive scales or time
  samples keep \(c_*=0\) for shear and one-axis helical witnesses, while the
  balanced two-axis control keeps \(c_*=1/4\).

## Data and transformations

All spectra and quotients are closed exact formulas.  The shear, one-axis
helical wave, two-axis Beltrami control, and whole-space Gaussian covariance
are checked by the R0.70N symbolic producer.  Floating-point conversion is
used only for rendering.  No random sampling, fitted curve, DNS, or PDE time
integration is allowed.

## Visual rules

- Double-column footprint, vector PDF/SVG, and 600 dpi PNG.
- Two non-neutral color roots at most.
- Hatching, line style, marker shape/fill, and direct labels must preserve the
  result in grayscale.
- Log axes must be explicit and contain only positive values.
- The route and claim boundary must remain visible in the header.

## Claim boundary

The figure closes only the universal nonnegative scalar/componentwise
multi-scale covariance-frame route.  It does not exclude a conditional
genuinely three-dimensional frame, component-mixing or augmented observables,
or a fixed-rank geometric analysis.  Low rank is not asserted to imply
regularity.  The figure is not a blow-up, global-regularity, or
Millennium-problem result.
