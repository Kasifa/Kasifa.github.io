# Figure contract - fig-r071e-projected-lamb-trace

## Analytical question

What part of the R0.71C signed shell coefficient is controlled by the
projected-Lamb heat bulk, and what exact frequency cost remains when that
bulk is returned to the bottom face (s=0)?

## Exact family and normalization

Use the support-minimal smooth 2D3C Navier--Stokes datum from R0.71E with
(a=1), dyadic (K\in\{1,2,4,8,16,32,64,128\}), and dimensionless heat
height

\[
 \tau=K^2s.
\]

For the unsplit parent, set the two radial multiplier values to
\(\alpha=\beta=1\) and use the positive phase \(\sigma=+1\).  The exact
normalized works are

\[
 \frac{b^{\rm stretch}(\tau)}{a^3K^6}=2e^{-4\tau},
 \qquad
 \frac{b^{\rm comm}(\tau)}{a^3K^6}
 =2(e^{-4\tau}-e^{-2\tau}),
\]

\[
 \frac{b(\tau)}{a^3K^6}
 =2(2e^{-4\tau}-e^{-2\tau}).
\]

For the fixed tight radial refinement and the negative phase \(\sigma=-1\),
only the low-radius child has positive injection:

\[
 q_{\rm lo}(s)
 =\frac{(b_{\rm lo}(s)^+)^2}{D_{\rm lo}(s)}
 =a^4K^6e^{-2K^2s}.
\]

Consequently,

\[
 q_{\rm lo}(0)=2K^2\int_0^\infty q_{\rm lo}(s)\,ds,
\]

\[
 A_{\rm bottom}=\frac{a^2K^2}{8},
 \qquad
 \mathcal V_{\rm bulk}=\frac{a^2}{16},
 \qquad
 \frac{A_{\rm bottom}}{\mathcal V_{\rm bulk}}=2K^2,
\]

and on \(0<s<\theta/K^2\),

\[
 \mathcal V_\theta
 =\frac1Y\int_0^{\theta/K^2}q_{\rm lo}(s)\,ds
 =\frac{a^2}{16}(1-e^{-2\theta}).
\]

## Panel contract

- **A - Compression before positivity.** Plot the stretching,
  transport--filter commutator, and their combined projected-Lamb work
  against \(\tau\).  Keep the zero line and mark the exact combined-work
  zero \(\tau=(\log2)/2\).  The panel must make clear that neither component
  alone is the shell injection.
- **B - Vertical heat bulk.** Plot
  \(q_{\rm lo}/(a^4K^6)=e^{-2\tau}\), mark its bottom value one, and shade
  the exact dimensionless vertical area \(\int_0^\infty e^{-2\tau}d\tau=1/2\).
- **C - Bottom trace cost.** For dyadic \(K\), plot
  \(A_{\rm bottom}/\mathcal V_{\rm bulk}=2K^2\) and its scale-normalized
  quotient \(A_{\rm bottom}/(K^2\mathcal V_{\rm bulk})=2\).  Mark the exact
  slope two.
- **D - Finite heat boxes.** Plot \(\mathcal V_\theta\) against \(K\) for
  \(\theta\in\{1/4,1/2,1\}\), together with the infinite-height limit
  \(a^2/16\).  Every curve must be horizontal, displaying exact scale
  independence.

## Data sufficiency and grain

- Panel A: 241 deterministic samples on \(0\le\tau\le1.5\).
- Panel B: 241 deterministic samples on \(0\le\tau\le3\); the omitted tail
  is stated analytically rather than estimated from the plotted window.
- Panel C: eight dyadic wavenumbers.
- Panel D: eight wavenumbers for each of three finite heights, plus the exact
  infinite-height benchmark.
- All rows are closed-form evaluations in binary64 for display.  There is no
  random seed, fitted model, DNS, or PDE time stepping.

## Visual and archival rules

- Double-column static research figure, 178 by 104 millimetres.
- Vector PDF and SVG plus a 600 dpi PNG.
- Near-white background, dark ink, and a hard two-root palette cap; line
  style, markers, direct labels, and hatching must preserve every distinction
  in grayscale.
- Linear axes for signed work and heat height; logarithmic axes only for
  strictly positive dyadic scale laws.
- Archive the exact-formula CSV, metadata, independent reconstruction,
  original and grayscale QA images, manifest, environment, commands, and
  SHA-256 ledger.
- Final QA is performed on the 600 dpi PNG, its grayscale conversion, and a
  rasterized rendering of the PDF.

## Supported takeaway

Projected-Lamb compression and Leray energy control the normalized vertical
heat bulk, but this exact smooth NSE family pays the full two-derivative
factor (2K^2) when that bulk is returned to the bottom trace.

## Claim boundary

The figure is an exact-formula visualization of one smooth global 2D3C NSE
family and one fixed tight radial refinement.  It does not prove bottom-trace
integrability or divergence for arbitrary solutions, exclude nonlinear
depletion or a different adaptive trace theorem, prove singularity or global
regularity, or solve the Millennium problem.
