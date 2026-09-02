# QA protocol

1. Recompute every exact rational input and every Panel A row.
2. Require 147 Panel A rows and 5 Panel B rows with stable identifiers.
3. Require PDF and SVG vector masters plus a 178 mm by 100 mm, 600 dpi PNG;
   the SVG root must declare `178mm` by `100mm` rather than unitless pixels.
4. Render the PDF independently and compare its raster dimensions.
5. Inspect the full-color figure at final print size.
6. Inspect a grayscale derivative; line styles and direct labels must retain
   the three Panel A series, and Panel B must remain readable without color.
   Essential final-size SVG text must be at least 5 pt and both font faces
   must be embedded.
7. Check that the caption says the plotted quantity is a decay-rate term
   with additive `log10 C` suppressed, says target component, and explicitly
   excludes a full square-function upper bound.
8. Freeze hashes in manifest.json and SHA256SUMS.
