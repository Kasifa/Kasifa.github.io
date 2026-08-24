# Figure contract — R0.70G critical transport

## Analytical question and takeaway

The figure asks what adjacent-source differencing retains after every affine
jet is transported to its unit shell. It shows three exact facts: the
critical transport coefficient for a degree-(n) jet is
\(2^{-(n+2)}\); an ordinary signed difference can replace linear raw
accumulation by a bounded endpoint; and the source-side coefficient square
function does not supply the dual core-moment square function needed for an
absolute or positive-part estimate.

## Chart contract

- **Panel A:** comparison / lollipop chart for the exhaustive jet orders
  \(n=0,1,2\), with direct fraction labels and the reciprocal dual-dilation
  factors.
- **Panel B:** ordered analytic line comparison for \(N=1,\ldots,40\), with a
  semilog inset for the geometric increments.
- **Panel C:** ordered analytic line comparison for the two Cauchy factors over
  \(N=1,\ldots,32\).
- **Renderer and footprint:** static Matplotlib; 178 mm double-column width;
  vector PDF and SVG plus a 600 dpi PNG.
- **Palette:** hard two-root cap. Blue denotes transported differences or the
  controlled source factor; rust denotes raw accumulation or the missing dual
  factor. Solid/dashed strokes, filled/open markers, and direct labels retain
  the distinction without color.

## Source data

- `critical-transport-data.csv` evaluates
  \(\lambda_n=2^{-(n+2)}\), its reciprocal dual-dilation factor, and the
  unmatched defect \(1-\lambda_n\).
- `constant-recurrence-data.csv` evaluates the exact comparator
  \(p_j=1-2^{-j}\),
  \(\sum_{j=1}^N p_j=N-1+2^{-N}\), and
  \(\sum_{j=1}^N\Delta p_j=p_N\).
- `square-function-data.csv` evaluates the explicit comparison
  \(\sum_{j=1}^N2^{-j}=1-2^{-N}\) and
  \(\sum_{j=1}^N1=N\), together with their square roots.

All rows are evaluations of closed formulas. No fitted parameter, sampled
trajectory, or simulation output is used.

## Claim boundary

The figure is an algebraic illustration of critical dilation, signed
telescoping, and a conditional square-function pairing. It does not prove a
positive-part estimate, a Carleson bound for the physical core moments, a
common-terminal-time packing theorem, regularity, or singularity formation.
