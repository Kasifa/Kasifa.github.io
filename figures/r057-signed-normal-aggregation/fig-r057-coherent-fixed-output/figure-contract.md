# Figure contract — R0.57 coherent fixed-output packet

## Analytical question

Can scale separation, antipodal angular localization, exchange
symmetrization, or instantaneous heat evolution reduce the sharp
fixed-output normal-channel constant below one?

## Takeaway

No.  A real divergence-free one-shell packet sends arbitrarily many
high-frequency pairs coherently into the same low normal mode.  Its shell
ratio and cap aperture tend to zero, while the fixed-output
\(\ell^2\times\ell^2\) norm ratio remains exactly one.  The equality also
persists after applying the heat semigroup to both input blocks at the same
time.

## Chart family and variants

- panel (a): exact frequency-lattice geometry and polarization schematic for
  one presentation packet with \(L=8\);
- panel (b): log--log ordered comparison of the exact norm ratio, shell ratio,
  and angular-cap aperture for \(L=2^j\), \(0\leq j\leq18\);
- panel (c): semilog instantaneous heat response for \(L=64\), showing the
  exact overlap of the normalized output and the two block-norm product.

## Data sufficiency

The geometric and localization claims are all-index analytic identities.
Nineteen dyadic localization rows and eighty-one heat-response rows are
presentation samples, not numerical evidence for the theorem.  The formal
certificate checks a 200,000-pair packet and 1,000,000 all-index instances
using exact integer arithmetic.

## Renderer and output

Reproducible Matplotlib static rendering.  Export at 178 by 105 millimetres as
vector PDF and SVG plus a 600 dpi PNG.  The final QA surfaces are the color
PNG, a true grayscale conversion, and a Poppler rendering of the PDF.

## Palette and non-color encoding

Use a hard two-root cap: blue for the surviving equality channel, gold for
shrinking geometric parameters, and neutral ink/grid.  Solid, dashed, and
dotted lines, open markers, direct labels, separate panels, and a diamond
output marker preserve meaning in grayscale.

