# Visual QA protocol

Inspect all five post-render surfaces:

1. `figure.png` at 600 dpi;
2. `qa-final-size.png` at 200 dpi;
3. `qa-grayscale.png`;
4. `qa-pdf.png` rendered independently from the vector PDF at 300 dpi.
5. `qa-svg-quicklook.png` rendered by macOS Quick Look from the self-contained
   SVG master.

Pass only if there is no clipping, overlap, missing glyph, or unreadable
final-size label.  The collar, path tube, kernel tail, and good/bad ledgers
must remain distinguishable in grayscale.  The footer must state the exact
claim boundary.  The Quick Look raster must retain the embedded DejaVu Sans
regular/bold appearance, with no serif substitution or missing glyph.  This
is internal visual QA, not an independent figure-package audit; any such audit
is reported separately.

Manual status: PASS
