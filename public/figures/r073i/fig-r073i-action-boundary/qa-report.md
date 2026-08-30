# R0.73I figure QA report

Status: **PASS** — final-size color, grayscale, and independent PDF-raster
surfaces inspected.

- Final journal size: 178 x 96 mm.
- Master PNG: 4204 x 2267 pixels at 600 dpi.
- Final-size QA surface: 1261 x 680 pixels at 180 dpi.
- Independent Poppler PDF raster: 1262 x 681 pixels at 180 dpi; the one-pixel
  ceiling difference is the expected PDF raster quantization.
- Grayscale standard deviation: approximately 33.8.
- Panel titles, axis labels, endpoint qualifiers, legends, footer, broken-axis
  marks, reference labels, and the top-right research blossom are legible and
  do not collide or clip.
- The nested triangle, square, and circle cutoff markers remain distinguishable
  in grayscale without implying a visible cutoff separation that is absent in
  the data.
- Panel B's three finite curves remain separable by marker, fill, and line
  style; the detached dash-dot `Lambda^-1` guide is visibly not a fitted curve.

This QA covers presentation integrity only.  It does not certify a Fourier
tail, a continuum selected action, a WKB asymptotic theorem, or either
non-theorem endpoint.
