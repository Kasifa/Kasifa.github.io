# Visual QA protocol

1. Verify that all source blobs match the recorded renderer-source commit and
   every certificate input matches commit
   `a2414fbf40908381acff0aa6f6ebf088e392a9b8`.
2. Render `figure.pdf` to a lossless PNG and compare it with the direct PNG.
3. Inspect the 178 mm double-column view at 254 dpi (10 pixels/mm).
4. Inspect a grayscale conversion and verify that markers, line styles, direct
   labels, the zero line, and the normalized gate remain distinguishable.
5. Verify all panel titles, variables, units, log scales, exact fraction labels,
   holdout marker, and decomposition annotation.
6. Confirm a one-page 178 mm by 132 mm vector PDF, editable SVG text without a
   raster image element, and a 600 dpi archival PNG.
7. Confirm the footer and caption separate the exact continuum subcertificate
   from finite diagnostics and reject continuum-saturation, tail-proof,
   three-dimensional-regularity, and Clay-problem interpretations.
8. Confirm that the finite response endpoint is labelled
   `d=0.01>1/450`, hence outside the theorem window, and that the independent
   inventory is stated as four formal sentinels plus one recomputed holdout.
