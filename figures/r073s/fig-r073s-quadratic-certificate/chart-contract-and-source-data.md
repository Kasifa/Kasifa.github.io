# R0.73S chart contract and source-data note

## Analytical question

How much of the phase-sensitive sixth moment is already controlled by the
quadratic autocorrelation certificate, and which two losses remain genuinely
unavoidable?

## One-sentence takeaway

The quadratic autocorrelation proxy separates the matched phase pair, but its
square-root dependence on autocorrelation support is sharp and identical
support, coefficient moduli, (L^2), and (L^4) data can still hide an
unbounded (L^6) ratio.

## Chart map

| Panel | Family and quantity | Source grain | Evidentiary role |
|---|---|---|---|
| A | asymptotically fixed-quartic Dirichlet spike: exact \(\Theta\), autocorrelation-support certificate, and sharp asymptotic guide | six sealed dyadic records, \(m=4,\ldots,4096\) | shows that the \(D_C^{1/2}\) exponent cannot be reduced |
| B | R0.73R matched Dirichlet/Rudin--Shapiro pair after the common scaling | sixteen sealed records, \(m=1,\ldots,128\) | compares exact sixth-moment guides with the computable \(AQ\) certificate |
| C | lacunary-product pair with identical low-order summaries | exact identity at every integer depth \(0\le r\le128\); sealed finite checks mark \(1\le r\le8\) | shows low-summary non-identifiability without claiming a computational lower bound |

There is no random sample, fitted exponent, PDE solver, or Navier--Stokes
time integration in this figure. Panel C connects every displayed integer
depth as a visual guide to one exact closed-form identity; it does not
interpolate uncomputed sample data.

## Panel A formulas

For the complex bounded, asymptotically fixed-quartic spike with \(E=1\),

\[
D_C=4m-1,
\qquad
\Gamma_m=\frac53+2m^{-1/2}-3m^{-1}+\frac1{3m^2},
\]

\[
\Theta_m=\frac{11}{20}m^{1/2}+7-\frac{15}{m}
+\frac{33}{4}m^{-3/2}+3m^{-2}-3m^{-5/2}
+\frac15m^{-7/2}.
\]

The plotted autocorrelation-support branch is

\[
B_{C,m}=\Gamma_m^{3/2}\sqrt{D_C},
\]

and the sharp exponent guide is

\[
\frac{11}{40}\sqrt{D_C}.
\]

The guide is an asymptotic comparison, not an equality. The sealed source
records are the `asymptotically_fixed_quartic_spike` rows in
`research/certificates/r073s/source-data.csv`.

## Panel B formulas

For the R0.73R matched pair, let

\[
A=\|\widehat{|W|^2}\|_{\ell^1},
\quad Q=\|W\|_4^4,
\quad \Theta=\|W\|_6^6,
\quad m=2^r.
\]

After the common R0.73R amplitude scaling, the two dimensionless plotted
guides are

\[
H_{AQ}=m^{-2/3}(AQ)^{1/6},
\qquad
H_6=m^{-2/3}\Theta^{1/6}.
\]

Thus \(H_6\le H_{AQ}\). Dirichlet remains order one; the computed
Rudin--Shapiro certificate tends to zero and has the proved envelope
\(O(m^{-1/2})\), while its exact guide is \(O(m^{-2/3})\). The plot shows
finite exact values only and does not fit either exponent. Its sixteen rows
are the sealed `matched_r073r` records.

## Panel C formulas

Let

\[
A(z)=1-z-z^2-z^3+z^4,
\qquad
B(z)=1-z-z^2-z^3-z^4,
\]

and use no-carry products for every integer radix \(q\ge14\). At each
integer depth \(r\in\mathbb N_0\), both
families have the same support, coefficient moduli, \(L^2\), and \(L^4\),
while

\[
\frac{\|G_r\|_6}{\|F_r\|_6}
=\left(\frac{323}{311}\right)^{r/6}.
\]

The plotted line connects this exact analytic identity at every integer depth
through 128. Depths \(1,\ldots,8\) are separately present in the sealed
certificate; depth zero is the empty-product identity and is not called a
sealed row. Values beyond \(r=8\) are independently re-evaluated closed-form
values, not additional enumerated certificate rows. Unboundedness follows
from \(323/311>1\) and the identity as \(r\to\infty\), not from the finite
display window.

## Surface and visual encoding

The selected surface is a reproducible static Matplotlib figure exported at
178 mm double-column width as vector SVG and PDF plus a 600-dpi PNG. The
palette has two chromatic roots (blue and ochre) plus neutral ink and grey.
Families use colour; exact quantities, certificates, and asymptotic guides
also use distinct line styles and markers so the figure remains legible in
grayscale. Axes carrying power laws use honest logarithmic scales. Final QA
must inspect the PDF raster, the 178 mm print-size raster, and grayscale.

## Claim boundary

The figure visualizes exact formulas and rigorous sufficient upper bounds for
explicit finite Fourier families. It does not show a Navier--Stokes
simulation, a complexity lower bound, a necessary regularity criterion,
unsafe dynamics, finite-time blow-up, arbitrary-
\(L^2\) safety, or a solution of the Clay problem. The annular lifts used for
the sharpness statement have zero convection and are globally smooth shear
flows.
