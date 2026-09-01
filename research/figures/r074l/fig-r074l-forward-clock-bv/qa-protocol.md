# Visual QA protocol

Inspect all four post-render surfaces:

1. figure.png at 600 dpi;
2. qa-final-size.png at 200 dpi;
3. qa-grayscale.png;
4. qa-pdf.png rendered independently from the vector PDF at 300 dpi.

Pass only if there is no clipping, overlap, missing glyph, or unreadable
final-size label; arrows and row totals remain distinguishable in
grayscale; and the footer states the exact claim boundary.

Manual status: PASS
