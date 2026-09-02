# Visual QA protocol

Inspect all five post-render surfaces:

1. `figure.png` at 600 dpi;
2. `qa-final-size.png` at 200 dpi;
3. `qa-grayscale.png`;
4. `qa-pdf.png` rendered independently from the vector PDF at 300 dpi; and
5. `qa-svg-quicklook.png` rendered by macOS Quick Look from the self-contained
   SVG master.

Pass only if there is no clipping, overlap, missing glyph, detached label, or
unreadable final-size text.  The three exact index ranges, combined inward
chord/tube, target-shell absolute estimate, outer super-Gaussian tail, and
common target must remain distinguishable in grayscale without relying on
color.  The footer must say schematic, not to scale, no simulation, familywise,
and NOT CLAY.  Quick Look must retain embedded DejaVu Sans regular/bold, with
no serif substitution or missing glyph.  This is internal visual QA, not the
separate independent figure-package audit.

Manual status: PASS
