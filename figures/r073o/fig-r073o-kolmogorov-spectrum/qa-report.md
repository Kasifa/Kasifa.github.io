# R0.73O figure QA report

Status: **PASS - source sealed**

- The corrected final-size color raster is legible and unclipped.
- The grayscale raster preserves line-style and marker distinctions.
- The independently rasterized PDF agrees with the PNG layout.
- The PDF and SVG contain no raster image objects; SVG text is preserved.
- Panel A separates the finite crossing, critical marker, and target legend.
- Panel B retains the finite value, physical scaling, and residual.
- The finite/illustrative footer and all exclusion claims remain visible.

Programmatic facts:

```json
{
  "pdfMillimetres": [
    178.0000000000147,
    82.00000000000361
  ],
  "pdfRasterImageXObjects": 0,
  "pngDpi": [
    599.9988,
    599.9988
  ],
  "pngPixels": [
    4204,
    1937
  ],
  "qaPixels": {
    "qa-final-size.png": [
      2102,
      969
    ],
    "qa-grayscale.png": [
      2102,
      969
    ],
    "qa-pdf.png": [
      2103,
      969
    ]
  },
  "sourceCommit": "f139c5e707ffdfe855ca114faac669d12e431e59",
  "sourceRows": {
    "convergence": 10,
    "sweep": 121,
    "total": 131
  },
  "svgRasterImages": 0
}
```
