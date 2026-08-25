# Figure contract - fig-r071b-common-packing

## Analytical question

Which scale-packing shortcuts fail for the common-response channel, and what
exact sign-sensitive output survives the R0.71A same-covariance sign pair?

## Exact quantities

For the two-shell HHL triad, define

\[
\mathcal U_M=
\frac{\sqrt2\,M(M+1)(2M+1)}{(2M^2+2M+1)^{3/2}},
\qquad
\mathcal C_M=
-\frac{\sqrt2(2M+1)}{2(2M^2+2M+1)^{3/2}}.
\]

Then

\[
\mathcal U_M\to1,
\qquad
M^2\mathcal C_M\to-\frac12.
\]

For the same-low fan with \(M_j=8^j\), the plotted quantities are

\[
W_N=\frac1{4N}\sum_{j=1}^N\mathcal U_{M_j},
\qquad
L_N=\frac1{4N}
\left(\sum_{j=1}^N\mathcal U_{M_j}^2\right)^{1/2}.
\]

They satisfy \(W_N\to1/4\) and \(L_N\sim1/(4\sqrt N)\).

For the shared-high equal-radius fan with \(M_j=16^j\), the normalized
polarized operator ratio is

\[
\rho_N=
\frac1{4\sqrt N}\sum_{j=1}^N
\frac{M_j}{\sqrt{1+M_j^2}},
\]

while the exact root-tent norm is \(\sqrt{N/2}\) and the frame shell
supremum is at most one.

For the R0.71A sign pair, the sole output at \(k=(1,0,1)\) is
\(\pm3\sqrt2/40\). The sign-sensitive coefficient has

\[
\mathcal T_+^2=\frac9{800},\quad
a_+=\frac3{39940400}
\]

for the positive field, and both values are zero for the negative field.

## Panel contract

- **A - Two-shell response channels.** Plot \(\mathcal U_M\) and
  \(M^2|\mathcal C_M|\) for powers of two from \(4\) through \(65536\).
  The chord scaling is explicit in the axis label and legend; reference lines
  mark the exact limits \(1\) and \(1/2\).
- **B - Same-low packing.** Plot \(W_N\), \(L_N\), and the two exact
  asymptotic references for \(N=1,2,4,8,16,32,64\).
- **C - Shared-high packing.** Plot \(\rho_N\), \(\sqrt{N/2}\), and the
  shell-supremum upper bound one on logarithmic axes.
- **D - Signed output.** Use a diverging bar comparison for the two sole
  signed outputs. Carry \(\mathcal T_+^2\) and \(a_+\) as direct exact
  annotations rather than forcing unlike units onto a second axis.

## Data sufficiency and provenance

The 15 values in panel A resolve both monotone approaches to their exact
limits. The seven dyadic sizes in panels B and C span six doublings and expose
the proved constant versus square-root scaling. Panel D contains the complete
two-state sign pair. Every row is generated from the displayed closed formula
and cross-checked against `research/certificates/r071b/result.json` wherever
that producer contains the corresponding finite value. No random seed,
fitting, DNS, or PDE time integration is used.

## Visual rules

- Static Matplotlib at double-column width, 178 by 136 mm.
- Vector PDF and SVG plus a 600 dpi PNG.
- Hard cap of two non-neutral color roots.
- Solid/dashed/dotted strokes, open/filled markers, hatching, direct labels,
  and the zero line preserve distinctions in grayscale.
- Panel A uses a focused dimensionless scale because its question concerns
  two nonzero limits; both exact limits are visible.
- Original-resolution and grayscale QA images are archived and inspected.

## Claim boundary

The figure certifies two direct scale-packing obstructions and visualizes one
exact Cauchy--Young consumer coefficient. It does not derive time integrability
or any Navier--Stokes evolution estimate for \(a_+\). It is not a new
continuation theorem, a finite-time singularity result, a global-regularity
result, or a solution of the Millennium problem.
