# QA protocol

1. Verify the certificate SHA-256, schema, 13/13 PASS status, and all thirteen Boolean checks.
2. Recompute every displayed fraction independently with `Fraction`, including both window margins, the leakage margin, normalized annular radii, outer-edge gap, and finite transition reserve.
3. Require the exact 23-row source-data export and 24-file inventory.
4. Check a one-page 180 × 82 mm PDF with embedded fonts, an approximately 600 dpi RGB PNG, live SVG text with no raster image, and the three QA derivatives.
5. Check every recorded text bound against its declared panel/canvas container using the font-width/ascent proxy in `layout-bounds.json`.
6. Inspect `figure.png`, `qa-pdf.png`, `qa-grayscale.png`, and `qa-final-size.png` visually for clipping, collisions, contrast, grayscale distinction, and readable exact fractions.
7. Confirm that FINITE GATE ONLY, OPEN analytic work, and NOT CLAY are visible. Packet survival must not be implied.
