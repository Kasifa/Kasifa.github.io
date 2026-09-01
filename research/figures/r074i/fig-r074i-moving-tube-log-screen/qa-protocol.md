# QA protocol

1. Recompute SHA256 for the certificate and producer.
2. Require producer stdout to be byte-identical to the frozen 36/36 JSON.
3. Reconstruct the normalized cubic factors and every affine screen point
   independently from exact rational arithmetic.
4. Require exactly 24 declared package files and no undeclared file.
5. Validate a one-page 180 mm x 88 mm vector PDF, embedded fonts, SVG
   dimensions, declared two-root palette, visible scope labels, and absence of
   raster image XObjects in the PDF.
6. Validate the 600-dpi RGB master, its aspect ratio, and nonblank tonal range.
7. Validate the 1800-pixel final-size surface, full-resolution grayscale
   surface, and independently Poppler-rasterized PDF surface.
8. Require every recorded text-bound proxy to lie in its declared container.
9. Inspect master, final-size, grayscale, and PDF-raster images at their actual
   QA surfaces. Reject clipping, collision, illegible text, detached arrows or
   markers, weak grayscale separation, or color-only meaning.
10. Regenerate `validation.json`, `qa-report.md`, `results.json`,
    `manifest.json`, and `SHA256SUMS`, then verify every digest.
