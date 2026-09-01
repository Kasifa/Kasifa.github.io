# QA protocol

1. Verify the SHA-256 identities of `scripts/r074g_complete_payment_certificate.py` and `research/r074g_complete_payment_certificate.json` against `contract.json`.
2. Execute the frozen script and require stdout to be byte-identical to the frozen 31/31 JSON.
3. Recompute the five-coefficient ladder, all three positive gaps, and `L_12`, `L_13` with `fractions.Fraction`; do not trust plotted decimals.
4. Recompute every Panel-B `log10` value from the exact symbolic formula and exact `L_j`; do not evaluate the exponentially small factors directly.
5. Require the exact 16-row source export, formula strings, roles, transformations, and non-simulation status boundary.
6. Verify a one-page 180 x 82 mm PDF with embedded fonts, an approximately 600 dpi RGB master, live-text SVG without raster images, grayscale derivative, final-size derivative, and PDF render.
7. Require every recorded text extent to remain within its declared panel or canvas container using the auditable font-width/ascent proxy in `layout-bounds.json`.
8. Inspect `figure.png`, `qa-pdf.png`, `qa-grayscale.png`, and `qa-final-size.png` visually for clipping, collision, exact-label legibility, line/shape distinction, and panel alignment.
9. Confirm that PROPOSED INEQUALITY REJECTED, ANALYTIC DERIVATION, NOT DNS, and NOT CLAY are visible. The rejected object must be identified as the project’s frozen proposed inequality, not the Clay problem.
