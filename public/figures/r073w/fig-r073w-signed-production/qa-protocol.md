# R0.73W figure QA protocol

1. Verify the primary and independent R0.73W certificate files against their
   frozen SHA-256 values before generating any row.
2. Require canonical complete-`commonCore` equality and its frozen digest.
   Verify the rank-three field, parity, production coefficients, gradient-defect
   factorization, absorption coefficient, and \(q\to1\) constant directly from
   `rankThreeExtension`.
3. Verify the audited analytic-source hashes and retain the periodic/boundary-
   decay and weak-solution interpretation boundaries.
4. Reconstruct `source-data.csv` in deterministic row order.  Require exact
   equality for categorical and formula fields and numeric agreement to at most
   \(5\times10^{-15}\) for closed-form renderer coordinates.
5. Check Panel A endpoints lie on one \(s+\nu t\) characteristic and that its
   displayed payment has the sign `initial minus final`.
6. Check Panel B samples are exactly the unit-scale-normalized shapes
   \(s^{-1/4}\) and \(S^{3/4}\), and that source rows plus visible panel text say
   they are upper-bound shapes rather than data.
7. Check Panel C parity, the exact extremum
   \((\tfrac12\log2,\pm1/16)\), and the zero-scale/large-scale endpoints.
8. Check Panel D formula, \((0,1/78)\), positivity, and the independently
   computed interior stationary point.  Do not impose false monotonicity.
9. Render SVG, one-page PDF, and 600 dpi PNG at 178 mm by 126 mm.  Verify PNG
   pixels/DPI, PDF MediaBox, SVG viewBox, absence of remote SVG links, and use of
   only the declared blue/orange roots plus neutrals.
10. Inspect PDF resources: require at least one referenced font and require each
    referenced embedded font descriptor to contain `FontFile`, `FontFile2`, or
    `FontFile3`.  Record page count, size, references, and embedded-font count.
11. Reconstruct the final-size raster from the master PNG, independently
    rasterize the PDF, and require exact pixel identity with the stored QA
    assets.  Require the grayscale asset to equal explicit luminance conversion.
12. Run a renderer-level artist-bounds guard, then inspect color, grayscale,
    final-size, and PDF rasters for clipped titles, equations, annotations,
    tick labels, legends, and footnotes.
13. Require the locked research-blossom SVG IDs, five petals plus one center,
    at the established top-right placement; confirm it is data-free and does not
    overlap the R0.73W header token.
14. Confirm `navierStokesSimulation=false`, `fittedScalingLaw=false`,
    `dgxUsed=false`, `ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX`, and
    `NOT CLAY` in package metadata.
15. Emit `validation.json`, `manifest.json`, `qa-report.md`, and `SHA256SUMS`.
    Because no commit is authorized, label this a hash-bound prepublication
    artifact seal rather than an immutable formal-source seal.
16. For the later final source seal, require a full lowercase 40-hex commit,
    verify that it resolves, require all 21 source/raw Git blobs to be
    byte-identical to current files, and require the exact 21-file scoped Git
    status to be clean.  Record each repository path, blob object ID, byte
    count, and SHA-256 in `manifest.json`; then set `status=formal`,
    `publicationStatus=staged`, and `seal.state=formal-figure-source-seal`.
    Final resealing may update only the four metadata files named in Step 15.
