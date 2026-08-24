# Figure contract — R0.70I temporal Hardy envelope

## Analytical question and takeaway

The figure asks what the direct source--core Cauchy route actually produces
after the nested time slabs are summed.  On a finite geometric chain, the
normalized temporal envelope is

\[
 G_K(s)=\min\{r_K^{-1},s^{-1/2}\},\qquad 0<s\leq r_0^2,
\]

so the continuum Hardy singularity is cut off only below the finest parabolic
time $r_K^2$.  If $f(s)=s^{-\alpha}$, the resulting scalar model has
integrand $s^{-1/2-2\alpha}$: its endpoint is
$\alpha=1/4$, with logarithmic growth there.  A separate fixed-amplitude
initial-boundary scale ledger shows that the energy and integrated
dissipation scale like $r$, while both the target-functional scale factor and
the dual expression $r^{-3}E^2$ scale like $r^{-1}$.  This diagnoses the
critical obstruction but does not construct a common-positive-top solution.

## Chart contract

- **Panel A:** base-two log--log plot of the normalized finite-chain envelope
  $G_K$, the reference $s^{-1/2}$, and the cap $r_K^{-1}$, with
  $r_0=1$, $\rho=1/4$, and $K=6$.  The breakpoint
  $s=r_K^2=2^{-24}$ is explicitly marked.
- **Panel B:** exact truncated integrals

  \[
   H_\alpha(\varepsilon)=\int_\varepsilon^1
   s^{-1/2-2\alpha}\,ds
  \]

  for $\alpha=3/20,1/4,7/20$ and
  $\varepsilon=2^{-J}$, $J=2,\ldots,32$.  The three curves exhibit a
  bounded subcritical limit, logarithmic endpoint growth, and power growth.
- **Panel C:** normalized NSE scaling ledger for a fixed small amplitude
  $a=1/8$, radii $r=2^{-k}$, and unit reference-profile constants:
  $E=D=a^2r$, the normalized target scale factor
  $\mathcal T_n=a^4r^{-1}$, and $Q=r^{-3}E^2=a^4r^{-1}$.  The two
  inverse-scale curves coincide only because the displayed reference-profile
  constants are normalized to one; the two mathematical quantities are not
  identified.
- **Renderer and footprint:** static Matplotlib; 178 mm double-column width;
  vector PDF and SVG plus a 600 dpi PNG.
- **Palette:** hard two-root cap. Blue denotes the Hardy reference,
  subcritical behavior, and energy-class quantities; rust denotes the
  finite-chain cap, supercritical growth, and the focal $r^{-1}$ quantities.
  Stroke pattern, marker fill, neutral ink, labels, and panel separation keep
  every comparison readable without color.

## Source data

`data.csv` is a 138-row long-form table: 33 finite-chain kernel rows, 93
Hardy-integral rows, and 12 initial-boundary scaling rows.  Every value is an
evaluation of a displayed closed formula.  The table contains no fit, PDE
trajectory, discretized PDE state, or extrapolation from a simulation.

## Claim boundary

This is **closed-form analytic scaling, not a simulated NSE trajectory and
not a fixed-positive-top counterexample**.  Panel A is a normalized envelope
for the crude direct estimate, not an equality for the full filtered
source--core term.  Panel C records scale covariance for a fixed-amplitude
initial-boundary family; it does not show nonlinear persistence to one common
positive terminal time.  The figure is not simulation evidence or a
numerical PDE proof and establishes no regularity, blow-up, or Millennium
problem result.
