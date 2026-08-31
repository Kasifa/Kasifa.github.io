# R0.73U figure QA protocol

1. Reconstruct every schematic, matrix, zero coefficient, separation, curve,
   and exact peak record from frozen formulas.
2. Verify \(A+B=K\), \(\|K\|_F=\sqrt6\), and
   \(f'(z)=e^{-5z^2}(1-10z^2)\), hence
   \(z_*=1/\sqrt{10}\).
3. Render SVG, one-page PDF, and 600 dpi PNG at 178 mm by 100 mm.
4. Verify source and generated-file inventories, regular-file status, CSV
   schema, row order, formula labels, finite values, and exact matrix entries.
5. Verify PNG pixel dimensions, PDF page count and media box, SVG viewBox,
   absence of remote SVG links, and use of only the declared two-root palette
   plus neutrals.
6. Reconstruct the final-size raster from the master PNG, regenerate the PDF
   raster independently, and require exact pixel identity with the stored QA
   assets.  Require the grayscale image to equal the explicit luminance
   conversion of the final-size raster.
7. Inspect color, grayscale, and PDF rasters for clipped titles, equations,
   matrix entries, arrows, peak annotation, and footnotes.
8. Confirm that all three panels say or imply exact analytic/finite evidence,
   Panel C is an analytic formula rather than a fit, and the boundary is
   explicitly coefficient-level and parabolic-scale.
9. Confirm `navierStokesSimulation=false`, `fittedScalingLaw=false`,
   `dgxUsed=false`, and `ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX` in the
   sealed metadata.
10. Before publication, rerun validation with authoritative analytic commit
    `84e808dae473f6381cbf9df55a71f5fe81a1cfce`; the validator rejects the
    superseded `7249375...` commit.  A local preseal passes artifact QA but is
    not the publication seal.
