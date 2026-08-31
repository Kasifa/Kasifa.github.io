# R0.73O chart contract and source-data note

## Analytical question

Does an independently assembled Fourier truncation place the explicitly
embedded standard-cube Kolmogorov equilibrium on the unstable side of the
published computer-assisted critical interval, and is the computed leading
eigenvalue stable under increasing truncation?

## One-sentence takeaway

At \(\alpha=0.7\) and \(R=3.012\), the finite spectral abscissa is positive and
converges to approximately \(3.73272364\times10^{-5}\), while the independently
computed finite crossing agrees with the rigorous published critical interval;
the plot is a consistency diagnostic and not an infinite-dimensional proof.

## Chart map

| Panel | Chart family and variant | Source grain | Evidentiary role |
|---|---|---|---|
| A | highlighted line with uncertainty/reference band | 121 ordered Reynolds samples | shows the finite spectral crossing, rigorous critical interval, and target \(R\) |
| B | convergence dot/line with residual inset | 10 truncation levels | shows truncation stability at \(R=3.012\) and numerical residual scale |

## Data sufficiency

Panel A has 121 ordered samples on \(R\in[2.98,3.04]\), enough to resolve the
local sign change. Panel B has ten deliberate truncation levels from 8 to 120;
each point is meaningful and exact lookup is retained in source-data.csv.
If the abscissa is not monotone on the selected local interval or the
truncation spread fails the configured tolerance, figure generation must fail
instead of smoothing or hiding the discrepancy.

## Static delivery contract

- Renderer: reproducible local Matplotlib.
- Final size: 178 mm by 82 mm.
- Formats: vector PDF and SVG plus 600 dpi PNG.
- Palette: single blue root plus gold for the rigorous interval/target; line
  style, markers, direct labels, and a zero line carry meaning without color.
- QA: final-size raster, grayscale raster, PDF raster, exact dimension and
  label checks, and visual inspection.

## Source-data derivation

For

\[
 \phi(X,Y)=e^{i\alpha X}\sum_{k=-M}^M c_ke^{ikY},
 \qquad d_k=\alpha^2+k^2,
\]

the truncated matrix for

\[
 \sigma\Delta\phi-\frac1R\Delta^2\phi
 +\sin Y(\Delta+I)\partial_X\phi=0
\]

has entries

\[
\begin{aligned}
 A_{k,k}&=-d_k/R,\\
 A_{k,k-1}&=\frac{\alpha(1-d_{k-1})}{2d_k},\\
 A_{k,k+1}&=-\frac{\alpha(1-d_{k+1})}{2d_k}.
\end{aligned}
\]

source-data.csv records the leading finite eigenvalue, normalized residual,
and all parameter identities used to convert back to the physical cube. No
row is experimental or fitted.

## Claim boundary

The rigorous interval

\[
R_c\in[3.011528364444,3.011528364446]
\]

is an external computer-assisted theorem input from Nagatou and its later
restatement. The local eigensolver is an independent finite consistency check.
It does not prove the infinite-dimensional spectral theorem, replace interval
arithmetic, compute nonlinear escape, establish an essentially
three-dimensional mode, show singularity, or affect the Clay status.
