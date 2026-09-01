# QA protocol

1. Verify the certificate SHA-256, schema, 30/30 PASS status, and all thirty Boolean checks.
2. Recompute every displayed exponent and exact gap independently with `Fraction`, including the close-range ordering around `c_leak`, `alpha^2/260`, and `c_surv`.
3. Recompute the buffer threshold, `L_12`, `L_13`, the conditional inner-radius margin, and the conditional outer squared-radius margin.
4. Require the exact source-data export and 24-file inventory.
5. Check a one-page 180 x 82 mm PDF with embedded fonts, an approximately 600 dpi RGB PNG, live SVG text with no raster image, and all three QA derivatives.
6. Check every recorded text bound against its declared panel or canvas container using the font-width/ascent proxy in `layout-bounds.json`.
7. Inspect `figure.png`, `qa-pdf.png`, `qa-grayscale.png`, and `qa-final-size.png` visually for clipping, collisions, grayscale distinction, and readable exact fractions.
8. Confirm that FINITE COMPATIBILITY ONLY, CONDITIONAL, ANALYTIC BRIDGE NOT CERTIFIED, and NOT CLAY are visible. Packet survival must not be presented as proved by the figure.
