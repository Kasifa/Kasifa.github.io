# QA protocol

1. Validate input hashes and claim-boundary fields.
2. Check PDF page count, MediaBox dimensions, and embedded text.
3. Render the PDF at final-size and grayscale resolutions.
4. Inspect the final-size, grayscale, and high-resolution raster for clipped
   labels, collisions, illegible residuals, and ambiguous status colors.
5. Require the public PDF/SVG/PNG copies to be byte-identical to the archival
   masters before release.

