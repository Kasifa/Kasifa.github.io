# R0.73J figure QA protocol

1. Recompute all plotted rows from the two certificate JSON files and verify
   their SHA-256 bindings.
2. Check that the 64 contour rows and 128 overlap cells are complete and that
   their minima equal the certificate decisions.
3. Verify the PDF and SVG remain vector outputs and that the PNG metadata and
   dimensions correspond to 178 mm by 104 mm at 600 dpi.
4. Inspect the final-size, grayscale, and independently rasterized PDF
   surfaces for clipping, label collisions, detached annotations, and loss of
   global/local distinctions.
5. Fail closed if any contour bound is nonpositive, either winding differs
   from one, any overlap bound is at most (1/2), or a public claim exceeds
   `contract.json`.
