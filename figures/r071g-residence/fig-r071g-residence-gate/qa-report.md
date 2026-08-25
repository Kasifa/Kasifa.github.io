# R0.71G figure QA

Status: passed automatic validation and direct visual inspection.

- Inspected the original 600 dpi PNG at full resolution
  (4204 x 2551 px).  All four panels, panel letters, titles, axes, legends,
  mathematical labels, and twin-axis annotations remain inside the canvas.
- Inspected the 1780 x 1080 grayscale preview.  Panel A's four finite curves
  remain distinguishable by line style; Panel C retains circle, square, and
  triangle levels; Panel D retains separate line styles and axes without
  relying on color.
- Rasterized the one-page vector PDF independently at 180 dpi with
  pdftoppm and inspected the result.  It matches the PNG composition with no
  clipping, missing glyphs, or line-art failure.
- The PDF page is 178 x 108 mm to output precision.  The PNG is the required
  600 dpi archival raster; the small one-pixel rounding in its dimensions is
  due to conversion from millimetres.
- validation.json checks 5292 data rows, initial normalizations, exact weak-
  limit columns, all displayed event ordering, the exact functional partial
  sums, and the outer-mode mass.
- The maximum difference between the fixed-step sign exits and the independent
  adaptive audit is below \(4.6\times10^{-8}\).  The two adaptive truncation
  radii agree to below \(4\times10^{-14}\) on the checked sign exits.
- Panel B labels \(0.5\mu^{-1}\) as a guide.  It is not presented as a proved
  asymptotic law.  Panel D is explicitly an abstract functional construction,
  not an NSE trajectory.
- The figure contains reduced-chain checks and exact formulas.  It is not DNS,
  not 3D PDE time stepping, not fitted data, and not evidence of singularity.
