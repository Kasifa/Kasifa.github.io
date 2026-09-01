# QA protocol

1. Recompute SHA256 for the certificate and producer.
2. Require producer stdout to be byte-identical to the 25/25 certificate.
3. Rebuild every source-data exponent independently from certificate fields.
4. Require exactly 24 package files and no undeclared file.
5. Validate 180 mm x 82 mm PDF, one page, embedded fonts, SVG dimensions,
   declared two-root palette, and visible scope labels.
6. Validate 600-dpi PNG dimensions and RGB mode.
7. Validate grayscale, final-size, and independently rasterized PDF surfaces.
8. Require every recorded text-bound proxy to lie in its declared container.
9. Inspect the master PNG, grayscale PNG, final-size PNG, and PDF raster at
   their actual QA surfaces; reject clipping, collisions, illegible labels,
   detached markers, or color-only distinctions.
10. Regenerate `manifest.json`, `validation.json`, `qa-report.md`, and
    `SHA256SUMS`, then verify every listed digest.
