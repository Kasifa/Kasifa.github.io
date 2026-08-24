# Figure contract — R0.70K normalized anisotropy evolution

## Analytical question and takeaway

The figure asks whether trace normalization turns a localized vorticity
covariance into a dissipative source-aware variable. The exact answer is no.
For the frozen axisymmetric source

\[
 \Sigma_0=\operatorname{diag}(-1/2,-1/2,1),
\]

an initially isotropic covariance follows a replicator equation toward the
rank-one extensional state. Its source correlation obeys

\[
 \dot q=(1+2q)(1-q)\ge0.
\]

Separately, an exact periodic Navier--Stokes shear with zero nonlinearity has

\[
 \frac d{dt}|B|_F^2=12\nu p(1-p)(2p-1),
\]

so normalized viscous anisotropy production has both signs.

## Chart contract

- **Panel A:** 121 closed-form evaluations on \(t\in[0,4]\), starting from
  isotropy. It plots
  \(p(t)=e^{3t}/(e^{3t}+2)\),
  \(q(t)=(e^{3t}-1)/(e^{3t}+2)\), and
  \(|B|_F^2=2q^2/3\). The sharp rank-one level \(2/3\) is shown as a
  reference.
- **Panel B:** 151 evaluations of the exact frozen-source production
  \(P(q)=(1+2q)(1-q)\) on the realizable axisymmetric interval
  \([-1/2,1]\). The nonnegative region is filled, with zeros at the
  compressive-plane and extensional-axis eigenspace states.
- **Panel C:** 201 evaluations of
  \(D(p)=12p(1-p)(2p-1)\), which equals
  \(\nu^{-1}d|B|_F^2/dt\) for the exact two-mode periodic shear. Negative and
  positive sectors are visually distinct. Certified markers record
  \(D(1/5)=-144/125\) and \(D(4/5)=144/125\).
- **Renderer and footprint:** static Matplotlib; 178 mm double-column width;
  vector PDF and SVG plus a 600 dpi PNG.
- **Palette:** hard two-root cap. Rust marks positive source alignment or
  positive production; blue marks negative or reference quantities. Stroke
  styles, marker fill, direct labels, signed fills, and zero lines preserve
  the result in grayscale.

## Source data

`data.csv` is a 483-row long-form table: 121 source-trajectory rows, 151
variance-production rows, 201 diffusion-sign rows, and 10 exact-summary rows.
Every plotted value evaluates a displayed closed formula. There is no fit,
DNS field, random seed, PDE time-stepper, or extrapolation.

## Claim boundary

This is **exact analytic data, not DNS and not a blow-up or regularity
result**. Panels A and B isolate the frozen-source subsystem of the complete
filtered covariance equation. They do not assert that a full Navier--Stokes
source remains frozen. Panel C is an exact periodic Navier--Stokes solution,
but it is not a finite-energy \(\mathbb R^3\) cascade. The figure establishes
neither global regularity nor singularity formation.
