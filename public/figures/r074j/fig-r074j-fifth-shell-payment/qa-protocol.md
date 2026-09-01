# QA protocol

1. Recompute SHA-256 for the certificate, Python producer, and independent
   Ruby reconstruction.
2. Require Python stdout to be byte-identical to the frozen 38/38 JSON and
   independently execute the Ruby 38/38, 287-field, zero-mismatch audit.
3. Reconstruct every visible rational value from exact arithmetic.
4. Require exactly 24 declared package files, a 22-row manifest, and a 23-row
   `SHA256SUMS` seal.
5. Validate a one-page 178 mm x 88 mm vector PDF, embedded fonts, SVG
   structure, declared two-root palette, visible scope labels, and no raster
   image XObject in the PDF.
6. Validate the 600-dpi RGB master, full-resolution grayscale surface,
   1780-pixel final-size surface, and independent 300-dpi Poppler PDF raster.
7. Require every text-bound proxy to lie inside its declared container.
8. Inspect all four raster surfaces at actual QA size. Reject clipping,
   collision, illegible text, detached arrows, weak grayscale distinction, or
   color-only meaning.
9. Seal `validation.json`, `manifest.json`, and `SHA256SUMS`, then verify
   every digest without rewriting the seal.
