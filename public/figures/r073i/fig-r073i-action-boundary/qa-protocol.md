# R0.73I figure QA protocol

1. Render PDF and SVG vectors plus the 600 dpi PNG at exactly 178 x 96 mm.
2. Rasterize the PDF independently with Poppler at 180 dpi.
3. Downsample the PNG to the same physical 180 dpi inspection surface.
4. Inspect the final-size color, grayscale, and PDF-raster surfaces.
5. Check panel titles, broken-axis marks, endpoint qualifiers, legend entries,
   reference-line labels, footer, and blossom for clipping or collision.
6. Confirm that marker shapes, fill states, and line styles remain distinct in
   grayscale and that the two panels use honest log/broken scales.
7. Recompute every plotted row from the bound R0.73I experiment files, then
   verify the complete flat-file SHA256 ledger.
8. Reject the package if any finite curve is presented as continuum evidence,
   if `D_ub` is called `d0`, or if `1/450` is called the theorem endpoint.
