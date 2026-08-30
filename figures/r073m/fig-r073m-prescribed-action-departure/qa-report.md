# R0.73M figure QA report

Status: **PASS**

- Color final-size raster inspected: no clipping, detached labels, or collisions.
- Grayscale raster inspected: cutoff nesting, coefficient paths, cubic paths,
  and four gate-family markers remain distinguishable without color.
- Independently rasterized PDF inspected: layout agrees with the PNG export.
- Panel (a) declares its focused vertical scale, retains the benchmark one,
  and labels the finite action proxy rather than a continuum action.
- Panel (b) displays the registered epsilon powers explicitly and does not fit
  or claim a limiting coefficient.
- Panel (c) retains the signed values and an explicit zero line.
- Panel (d) plots the maximum component ratio within each requested family,
  labels the fail threshold, and uses stems only as distance guides.
- The figure remains a finite binary64 diagnostic and does not certify a
  continuum limit, nonlinear trajectory, singularity, or the Clay problem.

Programmatic export facts:
- `pngPixels`: `[4204, 3023]`
- `qaPixels`: `{'qa-final-size.png': [2102, 1512], 'qa-grayscale.png': [2102, 1512], 'qa-pdf.png': [2103, 1512]}`
- `pdfPages`: `1`
- `pdfMillimetres`: `[178.0000000000147, 128.00000000000307]`
- `svgRasterImages`: `0`

Programmatic source-data facts:
- `finiteCaseRows`: `15`
- `gateComponentRows`: `12`
- `totalRows`: `27`
- `gateFamilyMaximums`: `{'cutoff': 5.421010862427522e-08, 'step': 0.11582529656770109, 'physical-kinetic': 0.0013032639323169652, 'independent': 0.041599078041835616}`
