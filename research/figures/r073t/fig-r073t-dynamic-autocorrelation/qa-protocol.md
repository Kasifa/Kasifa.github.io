# R0.73T figure QA protocol

1. Run the exact certificate in check-only mode.
2. Reconstruct all 28 source rows from the frozen formulas.
3. Render SVG, one-page PDF, and 600 dpi PNG at 178 mm by 100 mm.
4. Verify the source-file inventory and immutable source commit.
5. Verify row schema, row count, exact formulas, finite values, and panel
   normalization.
6. Verify the PNG pixel dimensions, PDF page count/media box, and SVG viewBox.
7. Rasterize the PDF independently and save the final-size, grayscale, and
   PDF QA images; at sealing time reconstruct the final-size raster from the
   master PNG, regenerate the PDF raster, and require exact pixel identity;
   require the grayscale image to equal the explicit luminance conversion of
   the final-size raster.
8. Confirm that titles, direct labels, axes, zero line, equation boxes, and
   footnotes do not collide or clip in color or grayscale.
9. Confirm that Panels B and C explicitly say \(t=0\), and that Panel C is
   labelled as the viscous-centered derivative and
   cannot be mistaken for the full \(Q'\).
10. Record `navierStokesSimulation=false`, `dgxUsed=false`, and
    `clayProblemSolved=false` in the contract and manifest.
