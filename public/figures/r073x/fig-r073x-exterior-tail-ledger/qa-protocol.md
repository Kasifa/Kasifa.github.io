# R0.73X figure QA protocol

1. Require all four frozen source files to match their contract SHA-256 values
   and immutable Git blobs at the declared source commit.
2. Parse the Gaussian denominator `32` and harmonic-pressure exponent `4`
   from the frozen proof text; reject hard-coded/source disagreement.
3. Require the Gaussian payload digest and final independent-audit verdict.
4. Reconstruct every `source-data.csv` row and require exact categorical and
   IEEE-754 coordinate equality.
5. Check Panel A against the parsed Gaussian formula for all 21 coordinates.
6. Check Panel B normalization at \(m=1\), both formula shapes, and the visible
   warning that the two analytic rows are not interchangeable.
7. Check Panel C against all five certificate rows, the stored normalizations,
   the final consecutive slopes, and the smallest-scale ratio.
8. Require the visible evidence labels `analytic formula`, `static functional
   diagnostic`, `NOT DNS`, and `NOT CLAY` in the SVG master.
9. Render SVG, one-page PDF, and 600 dpi PNG at 178 mm by 92 mm.  Verify PNG
   pixels and DPI, PDF MediaBox and embedded fonts, SVG viewBox and absence of
   remote links.
10. Reconstruct final-size and grayscale rasters exactly, independently render
    the PDF, and require byte-for-byte pixel equality with all stored QA images.
11. Inspect final-size, grayscale, and PDF rasters for clipping, collisions,
    detached annotations, unreadable ticks, and grayscale ambiguity.
12. Require the locked five-petal research blossom and center at the top-right
    header position, with no data meaning.
13. Require `navierStokesSimulation=false`, `dns=false`, `dgxUsed=false`,
    `associatedPressureCounterexample=false`, and `NOT CLAY` throughout.
14. Emit `validation.json`, `qa-report.md`, `manifest.json`, and `SHA256SUMS`.
    Until the publication owner commits the 21 source/raw files, label the seal
    `HASH_BOUND_PREPUBLICATION_ARTIFACT`, not a package-commit-bound formal seal.
15. Commit exactly the ten source files and eleven raw artifacts first.  Given
    that full 40-hex commit, require byte identity with every Git blob, record
    21 bindings, and require the exact bound scope to be clean.
16. Reseal only the four metadata files.  The final manifest must be
    `research-figure-manifest-v1` / `r073x-exterior-tail-ledger-manifest-v1`,
    `release=R0.73X`, `status=formal`, `publicationStatus=staged`, and
    `seal.state=formal-figure-source-seal`.  Independent verification rebuilds
    the 21 Git bindings and adds the three binding checks to the original 47.
