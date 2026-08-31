# R0.73R chart contract and source-data note

## Analytical question

Can two real divergence-free fields have identical Fourier support,
coefficient moduli, and quadratic Sobolev data while their critical
heat-flow sizes differ by a growing power, and how does the separation look
before and after the common amplitude scaling?

## One-sentence takeaway

The matched Dirichlet and Rudin--Shapiro tensors differ only by Fourier
signs, yet their normalized analytic heat-flow guides separate by
\(m^{2/3}\); after the common scaling, the Dirichlet heat guide stays order
one and the Rudin--Shapiro heat guide tends to zero.

## Chart map

| Panel | Family and variant | Source grain | Evidentiary role |
|---|---|---|---|
| A | paired Fourier-lattice glyph map | 128 positive-packet sign records at \(m=8\) | displays common sites and moduli, with sign carried by marker shape and fill |
| B | log--log three-series analytic guide | \(m=2^r\), \(0\le r\le12\) | displays the three unscaled exponents without fitting |
| C | log--log four-series analytic guide | the same 13 values of \(m\) | displays the four exponents after \(\alpha_m\) without fitting |

The ordered analytic grid has thirteen values and spans twelve dyadic steps.
No empirical sample, interpolation, random seed, regression, or PDE solver is
present.

## Exact source for Panel A

Let \(m=2^r\), \(N=8m\),

\[
D_m(z)=\sum_{q=0}^{m-1}z^q,
\]

and define \((P_m,Q_m)\) by

\[
P_1=Q_1=1,\qquad
P_{2m}=P_m+z^mQ_m,\qquad
Q_{2m}=P_m-z^mQ_m.
\]

If \(r_q\) is the coefficient sequence of \(D_m\) or \(P_m\), then

\[
\widehat W_{R,m}(N+q,s,0)=\frac{r_qr_s}{\sqrt2m},
\qquad 0\le q,s<m.
\]

The negative packet has coefficients at \((-N-q,-s,0)\) obtained by
complex conjugation. Since all \(r_q\in\{\pm1\}\), both families have
the same \(2m^2\) support and the same coefficient modulus. Panel A shows
only the positive packet to avoid drawing a redundant reflection.

## Analytic source for Panels B and C

The common Fourier packet lies in a fixed-ratio annulus with \(N=8m\).
Uniform heat multiplier and inverse-multiplier bounds give

\[
\|W_{R,m}\|_{\mathfrak X}\asymp
N^{-1/2}\|W_{R,m}\|_6.
\]

The exact Dirichlet sixth moment and the Rudin--Shapiro sup bound imply

\[
\|W_{D,m}\|_6\asymp m^{2/3},\qquad
1\le\|W_{P,m}\|_6\le40^{1/6}.
\]

Therefore the unscaled heat-flow exponents are \(1/6\) and \(-1/2\),
with ratio exponent \(2/3\). For

\[
\alpha_m=N^{1/2}m^{-2/3}=\sqrt8\,m^{-1/6},
\]

the common \(L^2\) exponent is \(-1/6\), the two heat-flow exponents are
\(0\) and \(-2/3\), and the common \(\dot H^{1/2}\) exponent is \(1/3\).
The source CSV records the dimensionless guides \(m^p\), each normalized at
\(m=1\). It does not claim equality to the norms whose fixed comparison
constants are suppressed by \(\asymp\).

## Surface and visual encoding

The selected surface is a reproducible static Matplotlib figure exported at
178 mm double-column width as vector SVG and PDF plus a 600-dpi PNG. The
palette policy is a hard two-root cap: blue and ochre plus neutral ink and
grey. Coefficient sign is also encoded by filled-circle versus open-square
glyphs. Every scaling series has a distinct combination of line style and
marker. Axes use honest logarithmic scales, and every displayed value is
dimensionless. Final QA must inspect the exported figure at 178 mm print
size and in grayscale.

## Claim boundary

The figure certifies the structure of one explicit formula family and
visualizes proved exponent bounds. It does not show a numerical
Navier--Stokes experiment, a fitted asymptotic law, a necessary regularity
criterion, unsafe dynamics, finite-time blow-up, arbitrary-\(L^2\) safety,
or a solution of the Clay problem. Each field has the form
\(e_3g(x_1,x_2)\), so its convection term vanishes identically.
