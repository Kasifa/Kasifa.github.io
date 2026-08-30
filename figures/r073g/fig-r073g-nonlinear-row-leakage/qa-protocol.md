# Visual QA protocol

1. Render `figure.pdf` to a lossless PNG and compare it with `figure.png`.
2. Inspect the 178 mm double-column figure at final print size.
3. Verify every axis title, unit, legend, marker, line style, and panel label.
4. Convert the PNG to grayscale and verify that line styles and markers remain
   distinguishable without color.
5. Confirm there is no clipping, overlap, rasterized text, misleading scale,
   or implication that finite cutoff agreement is a continuum proof.
6. Record page size, PDF page count, PNG dimensions and density, SVG parse
   status, and the visual verdict in `qa-report.md`.
