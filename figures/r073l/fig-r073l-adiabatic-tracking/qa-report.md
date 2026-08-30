# R0.73L figure QA report

Status: **PASS**

- Color final-size raster inspected: no clipping, detached labels, or collisions.
- Grayscale raster inspected: epsilon series remain separable by line style and marker; cutoff curves remain separable by dashed-square versus solid-circle encoding.
- Independently rasterized PDF inspected: layout agrees with the PNG export.
- Panel (a) explicitly declares its focused vertical scale.
- Panel (b) distinguishes the nearly coincident cutoff curves and labels the tail-three slope; the caption states that the slope-one line is anchored, not fitted.
- Panel (c) states that the residual comes from one forward orbit; no backward parabolic solve is implied.
- Panel (d) labels the fail threshold; the caption states that stems are distance guides, not uncertainty intervals.
- The figure remains a finite Fourier diagnostic and does not certify the continuum theorem.

Programmatic export facts:
- `pngPixels`: `[4204, 3023]`
- `qaPixels`: `{'qa-final-size.png': [2102, 1512], 'qa-grayscale.png': [2102, 1512], 'qa-pdf.png': [2103, 1512]}`
- `pdfPages`: `1`
- `pdfMillimetres`: `[178.0000000000147, 128.00000000000307]`
- `svgRasterImages`: `0`
