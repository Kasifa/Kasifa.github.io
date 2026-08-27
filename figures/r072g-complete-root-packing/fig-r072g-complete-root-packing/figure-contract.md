# Figure contract — R0.72G-1

## Analytical question

Do all roots of the exact one-carrier target change the logarithmic
root-slope order found from the selected Bessel roots?  How can a polynomial
number of roots coexist with only logarithmic slope mass?

## Supported takeaway

The R0.72G theorem proves

\[
G_{\rm all}(\delta_R;X)=\Theta(\log\delta_R)
\]

for the exact fixed-\(q_0\), real one-carrier Bessel sequence.  Two
independent finite solvers agree on every common root count and on complete
mass within \(9.18\times10^{-7}\) relative.  The finite count grows roughly
like \(\sqrt\delta\), but most late roots have very small slopes.

## Figure map

- **A — slope-weighted mass:** producer and independent complete masses,
  producer selected mass, and a neutral \(4/\pi^2\) finite diagnostic guide
  against \(\log\delta\).
- **B — resolved root count:** producer counts against \(\sqrt\delta\) on
  log axes with a neutral \(24/\pi\) guide.  This is a finite count, not part
  of the theorem.
- **C — dyadic mass packets:** producer slope mass for \(R=64\) grouped by
  scaled-time intervals \([2^m,2^{m+1})\).  A log ordinate keeps the
  enhanced-dissipation tail visible without inflating it.

## Data sufficiency

Panel A has seven producer and five independent coupling scales.  Panel B
has seven ordered scales.  Panel C uses every positive dyadic packet in the
largest producer run.  Exact values remain in `data.csv` and the source
certificates.

## Visual system

- Static Matplotlib export, 177.8 x 97.79 mm (nominal 178 mm double column).
- Vector PDF and SVG plus 600 dpi PNG.
- Near-white paper, charcoal ink, navy producer marks, rust independent
  marks, and neutral guides.
- Marker fill, line style, and keylines preserve series identity in
  grayscale.
- All visible figure text is English.

## Claim boundary

The \(\Theta(\log\delta)\) order is analytic only in the exact one-carrier
family.  The apparent \(4/\pi^2\) leading coefficient, root-count guide,
selected fraction, and dyadic tail are finite binary64 diagnostics.  No
panel proves the bound for growing carrier count, general triangular flow,
or arbitrary three-dimensional Navier--Stokes solutions.
