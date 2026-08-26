# Visual QA report

Status: passed

The regenerated nominal 178 mm by 118 mm figure was inspected at its
1780-by-1180 final-size color preview, in true grayscale, and after rendering
the vector PDF at 180 dpi. Matplotlib 3.11 stores figure sizes to the nearest
0.01 inch; the archived PDF and SVG are therefore 178.05 mm by 118.11 mm,
within 0.2 mm of the declared journal size. The 600 dpi PNG is 4206 by 2790
pixels and carries 600 dpi metadata.

All four panel titles, axes, legends, formulas, direct values, Fourier-mode
labels, evidence boundaries, and the finite-result footer remain inside the
canvas. Panel A keeps the even-touch annotation in the whitespace between the
two bar groups and its arrow terminates at the exact hard zero. Panel B leaves
the overlap inequality and all three paired cell ledgers unobstructed. Panel C
places the half-open window `[0,2*pi)` and the abstract-path boundary in the
legend, so no data mark is hidden. The left endpoint is included, the right
endpoint is excluded, and the plotted family has exactly `N` positive atoms.
Panel D leaves clear separation between the Fourier map, exact scalar ledger,
sharp equality, and the two-line claim-boundary box.

The figure does not rely on color alone. Panels A and B use solid versus open
hatched bars and direct values. Panel C uses solid, dashed, dotted, and
dash-dot lines together with filled circles, open squares, open triangles, and
open diamonds. Panel D uses filled circles and open squares. These encodings
remain distinct in true grayscale. The logarithmic scales in Panel C retain
all seven frequencies and every positive value without truncation.

The rendered PDF has one vector page and no raster image XObjects. Its text is
embedded and searchable. The visible wording identifies Panel C as an
abstract Hilbert path, not NSE, and Panel D as one one-sided initial jet only,
with no internal or repeated NSE face theorem. The figure asserts no uniform
all-shell/all-cell estimate, infinite-frame or Leray passage, continuation,
singularity, or regularity result.
The measure convention was reviewed explicitly: soft positive parts are taken
component by component before summing, producing the componentwise relaxed
positive-entry measure. This is generally not the positive Jordan part of a
signed shell-cell aggregate.
