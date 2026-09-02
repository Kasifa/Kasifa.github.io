# Visual QA protocol

Inspect all five post-render surfaces:

1. `figure.png` at 600 dpi;
2. `qa-final-size.png` at 200 dpi;
3. `qa-grayscale.png`;
4. `qa-pdf.png` rendered independently from the vector PDF at 300 dpi; and
5. `qa-svg-quicklook.png` rendered by macOS Quick Look from the self-contained
   SVG master.

Pass only if there is no clipping, overlap, missing glyph, detached label, or
unreadable final-size text.  Panels A--D, the free `varkappa` multiplier,
complete E/G/H/J payment ledger, quadratic `X_*` and positive collar-flux
growth, exact `q_*` conversion, and endpoint-divergence law must remain
distinguishable in grayscale without relying on color.  The phrase
`scalar-payment-only no-go` and the boundary `smooth exact family • NOT CLAY`
must be prominent.  The footer must also state analytic schematic, not to
scale, and no DNS/simulation/fitted data.  Quick Look must retain embedded
DejaVu Sans regular/bold without serif substitution or missing glyph.

This is internal visual QA, not the separate independent figure-package audit.

Manual status: PASS
