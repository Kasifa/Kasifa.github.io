# Figure contract - fig-r071d-critical-heat-defect

## Analytical question

Can a smooth material partition and a complete vertical heat ledger turn
signed parent cancellation into a subcritical refined estimate?

## Exact family

Use the normalized torus, \(\nu=A=1\), \(\rho=1/2\), and

\[
u_k=(0,k^{-1}e^{-k^2t}\sin(kx_1),0),\qquad
\omega_k=(0,0,e^{-k^2t}\cos(kx_1)).
\]

The material children are

\[
\phi_\pm=\frac12(1\pm\rho\cos(2kx_1)).
\]

At \(t=0\), normalize by the parent enstrophy \(Y=1/2\). Then

\[
\frac{\beta_+}{k^2Y}=-\frac\rho2,
\qquad
\frac{\beta_-}{k^2Y}=\frac\rho2,
\qquad
\frac{\beta_++\beta_-}{k^2Y}=0,
\]

while

\[
\frac{\delta_k}{k^2Y}=\frac{\rho^2}{2+\rho}>0.
\]

On the parabolic interval \(\tau_k=\theta/k^2\),

\[
\frac{B_-^2}{\overline D_-Y(0)}
=\frac{\rho^2}{2(2+\rho)}(1-e^{-2\theta}),
\]

independent of \(k\), and the R0.71C time-box Cauchy inequality is an
equality.

## Panel contract

- **A - Material partition.** Show \(\phi_+\), \(\phi_-\), and the normalized
  enstrophy density \(\cos^2z\) over one spatial period.
- **B - Cancellation and refinement.** Show the two signed child injections,
  their zero parent sum, and the positive normalized refined ledger.
- **C - Critical scaling.** Plot \(\delta_k/Y\) and
  \((\delta_k/Y)/k^2\) for dyadic \(k\); mark the exact slope two.
- **D - Parabolic-box cost.** Plot the scale-independent dimensionless cost
  for three values of \(\theta\), and state the exact Cauchy ratio one.

## Visual and archival rules

- Double-column static figure, 178 by 104 millimetres.
- Vector PDF and SVG plus a 600 dpi PNG.
- At most two non-neutral color roots, with line style, marker, hatching, and
  direct labels preserving every distinction in grayscale.
- Linear axes for signed quantities and logarithmic axes only for positive
  scale laws.
- Exact-formula source table, independent reconstruction, original and
  grayscale QA images, manifest, environment, and SHA-256 ledger.

## Claim boundary

The figure proves a critical viscous refinement obstruction on one exact
smooth Navier--Stokes family. It does not show that every adaptive tent norm
diverges, rule out a nonlinear Navier--Stokes compensation, prove blow-up or
global regularity, or solve the Millennium problem.
