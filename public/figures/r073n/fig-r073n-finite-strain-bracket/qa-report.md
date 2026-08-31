# R0.73N figure QA report

Status: **PASS - sealed**

- The 600-dpi color master and final-size raster were inspected: panel labels,
  legends, annotations, axes, and the two-line evidence boundary are legible and
  unclipped.
- The grayscale raster was inspected: envelope/components, action interval,
  strain curve, and rational witness remain distinguishable by line style and
  fill as well as hue.
- The independently rasterized PDF was inspected and agrees with the PNG
  layout; the PDF itself contains no raster image XObjects.
- Panel B visibly marks both `T*=1/1800` and `j(infinity)=5/16`.
- Panel C states that the curves evaluate formula factors at different marked
  basepoints and does not identify them with a sharp flow-map modulus.
- The figure remains finite and illustrative.  The inherited action interval
  is an analytic input; arbitrary fixed-background instability, full 3D stability,
  singularity, and Clay claims remain open.
- The immutable theorem-source commit and all ten figure-source blobs passed verification.

Programmatic export facts:
- `pngPixels`: `[4204, 2267]`
- `pngDpi`: `[599.9988, 599.9988]`
- `qaPixels`: `{'qa-final-size.png': [2102, 1134], 'qa-grayscale.png': [2102, 1134], 'qa-pdf.png': [2103, 1134]}`
- `pdfPages`: `1`
- `pdfMillimetres`: `[178.0000000000147, 96.00000000001111]`
- `pdfRasterImageXObjects`: `0`
- `svgRasterImages`: `0`
- `svgTextPreserved`: `True`

Programmatic source-data facts:
- `strainSamples`: `241`
- `cumulativeSamples`: `243`
- `markedBasepointSamples`: `121`
- `totalRows`: `605`
- `upstreamPath`: `research/certificates/r073n/source-data.csv`
- `upstreamSha256`: `cdde9894f05a0c78ba70d272df67c2423508535bdf469c7c273a34b960418a1f`
