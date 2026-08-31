# R0.73V figure QA protocol

1. Verify that the current `results.json` and `independent-results.json` match
   their frozen hashes and their blobs in certificate package commit
   `b34d91e...`.
2. Require complete `commonCore` equality, the frozen common-core SHA-256, and
   the complete-table digest before generating any source row.
3. Reconstruct every Panel A coefficient, all Panel B matrix entries and
   small-s orders, every Panel C zero/nonzero entry, and the selected
   Panel D quartic coefficient from the common core.
4. Verify the exact identities
   \(\widehat\chi_s=\widehat{\mathcal C_s}-\widehat{v_s\odot N_s}\),
   pressure diffusion plus pressure strain equals the displayed combined
   pressure matrix, and the finite-\(\varepsilon\) extraction equals
   \(9i/32\).
5. Verify that the small-s order verdict is read from exact certificate
   metadata rather than estimated from plotted samples.
6. Render SVG, one-page PDF, and 600 dpi PNG at 178 mm by 118 mm.
7. Verify source and generated-file inventories, regular-file status, CSV
   schema, row order, JSON paths, finite renderer samples, and exact formulas.
8. Verify PNG dimensions and DPI, PDF page count and media box, SVG viewBox,
   absence of remote SVG links, and use of only the declared two-root palette
   plus neutrals.
9. Reconstruct the final-size raster from the master PNG, independently
   regenerate the PDF raster, and require exact pixel identity with the stored
   QA assets. Require grayscale to equal explicit luminance conversion.
10. Inspect color, grayscale, final-size, and PDF rasters for clipped titles,
    equations, matrices, arrows, direct labels, and footnotes.
11. Confirm that Panel B and Panel C say `coefficientwise`, Panel D says
    `selected coefficient`, and the footer says `NOT CLAY`.
12. Confirm `navierStokesSimulation=false`, `fittedScalingLaw=false`,
    `dgxUsed=false`, and
    `ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX` in sealed metadata.
