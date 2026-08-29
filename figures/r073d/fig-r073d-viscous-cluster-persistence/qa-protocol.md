# QA protocol

1. Verify input hashes and fail-closed claim fields.
2. Require PDF, SVG, and 600 dpi PNG masters.
3. Render the PDF with Poppler at final size.
4. Inspect PDF and PNG for clipping, overlap, glyph loss, and label contrast.
5. Inspect a grayscale conversion for curve and status separation.
6. Record pixel dimensions, embedded PDF fonts, visual review, and hashes.
