# Figure contract - fig-r071f-local-trace

## Analytical question

After localization by a genuine spatial cutoff or a matched partition, which
parts of the projected-Lamb heat quotient still pack unconditionally, and what
sharp scale is lost when its heat bulk is returned to the bottom face
\(s=0\)?

## Supported takeaway

The localized quotient has an exact heat-profile collapse and valid
bounded-overlap envelopes, but the bottom-from-bulk multiplier remains
critical: it is exactly

\[
 \frac{2K^2}{1-e^{-2K^2h}}
\]

for the localized 2D3C witness and scales like \(r^{-2}\) in the covariant
interior-cylinder family.  Localization preserves bulk packing; it does not
produce a subcritical trace gain.

## Evidence classes

The figure must distinguish three evidence classes without relying on color:

1. **Exact analytic curves** from the formulas in R0.71F.
2. **Independent FFT points** reconstructed from the full trigonometric
   velocity for \(K\in\{1,2,4,8\}\); these are numerical checks of the exact
   initial-trace formula, not simulations.
3. **Normalized analytic envelopes/scaling families**; these show theorem
   scaling only and are not measured values from a full frame or an NSE
   trajectory.

There is no DNS, time stepping, fitted model, random sample, or blow-up
trajectory in any panel.

## Exact formulas and normalizations

For every nonzero smooth \(\phi\ge0\) in the localized 2D3C low block,

\[
 q_\phi(s)=q_\phi(0)e^{-2K^2s},
 \qquad \tau=K^2s.
\]

For a finite height \(h=\theta/K^2\), define the trace multiplier normalized
by \(K^2\):

\[
 m(\theta)
 =\frac1{K^2}\frac{q_\phi(0)}{\int_0^{\theta/K^2}q_\phi(s)\,ds}
 =\frac{2}{1-e^{-2\theta}}.
\]

It obeys \(m(\theta)\sim\theta^{-1}\) as \(\theta\downarrow0\) and
\(m(\theta)\to2\) as \(\theta\to\infty\).

For the matched-partition bounds with fixed energy amplitude \(a=K^{-1}\),
write \(C_*=C_0+C_1/\rho^2\), and define only for the positive low-radius
subblock

\[
 A_{\rm lo,part}
 =\frac1Y\sum_Qq_Q(0),
 \qquad
 \mathcal V_{\rm lo,part}
 =\frac1Y\int_0^\infty\sum_Qq_Q(s)\,ds.
\]

The exact analytic envelopes are

\[
 \frac1{16C_*}\le A_{\rm lo,part}\le\frac N4,
 \qquad
 \frac1{32C_*K^2}\le\mathcal V_{\rm lo,part}
 \le\frac N{8K^2}.
\]

Panel C divides each lower or upper envelope by its own bottom prefactor.  In
this normalization both bottom envelopes equal one and both heat-bulk
envelopes equal \(1/(2K^2)\).  This displays only the certified scale law;
it does not assign numerical values to \(N,C_0,C_1\), or \(\rho\), and it
does not assert a two-sided bound for the full-frame \(A_{\rm loc,+}\).

For the scale-covariant interior-cylinder family, normalize one base cylinder
by \(r_0=c_*=1\):

\[
 \frac{A_{Q_r}}{\mathcal V_{Q_r,\theta r^2}}=r^{-2}.
\]

The comparison \(r^{-3/2}\) in Panel D is an illustrative subcritical power,
not a competing theorem.

## Panel contract

- **A - Exact heat-profile collapse.** Plot the analytic curve
  \(e^{-2\tau}\) on \(0\le\tau\le3\).  Overlay independent FFT points for
  \(K=1,2,4,8\) at
  \(\tau\in\{0,1/8,1/2,1,2\}\).  Marker shape distinguishes \(K\); the
  analytic curve is a solid dark line.  Because the four checks agree to
  machine precision, their plotted symbols may be staggered horizontally by
  at most \(0.018\) in \(\tau\) solely for visibility; `data.csv` retains the
  true heat height and the panel must disclose the display offset.  State
  visibly: `exact curve + independent FFT points; not DNS`.
- **B - Finite-height trace multiplier.** Plot
  \(m(\theta)=2/(1-e^{-2\theta})\) for
  \(10^{-2}\le\theta\le10\), together with the small-height reference
  \(\theta^{-1}\) and the large-height limit \(2\).  Both axes are logarithmic.
- **C - Matched-partition fixed-energy envelopes.** For dyadic
  \(K=1,\ldots,128\), plot the prefactor-normalized bottom envelope \(1\)
  and heat-bulk envelope \(1/(2K^2)\).  Use paired open/filled markers to
  indicate that lower and upper analytic envelopes have the same normalized
  law.  Label the panel `analytic envelope shape; constants divided out`.
- **D - Geometry-only scaling boundary.** Plot the normalized critical family
  \(r^{-2}\) and the illustrative subcritical comparator \(r^{-3/2}\) for
  \(r=2^{-k}\), \(0\le k\le7\).  The radius axis decreases to the right.
  Annotate that the ratio to the subcritical comparator diverges and that the
  critical power is saturated, not disproved.

## Data sufficiency and grain

- Panel A analytic curve: 241 deterministic samples; FFT overlay: 20 points
  from four independently reconstructed frequencies and five heat heights.
- Panel B: 241 deterministic log-spaced samples.
- Panel C: eight dyadic frequencies for each of two symbolic envelopes.
- Panel D: eight dyadic radii.
- `data.csv` retains evidence class, formula identifier, normalization, and
  source fields so analytic curves are never confused with FFT checks or
  schematic envelope laws.

## Visual and archival rules

- Static double-column research figure, exactly 178 by 104 millimetres.
- Vector PDF and SVG plus a 600 dpi PNG.
- Near-white background, dark ink, one navy root and one rust root plus
  neutrals.  Marker fill, line style, hatching, and direct labels must retain
  all distinctions in grayscale.
- No decorative gradients, pseudo-measurement bands, or simulation language.
- Archive the exact/FFT CSV, metadata, independent reconstruction,
  original/grayscale QA images, manifest, environment, commands, and SHA-256
  ledger.
- Final QA is performed on the 600 dpi PNG, its grayscale conversion, and a
  rasterized rendering of the PDF.

## Claim boundary

The figure proves and checks only the formulas and scaling statements above.
It does not prove persistence of a large bottom trace in physical time, reject
a critical \(Cr^{-2}\) estimate, compare arbitrary prescribed frames, produce
a singular solution, prove global regularity, or solve the Millennium problem.
