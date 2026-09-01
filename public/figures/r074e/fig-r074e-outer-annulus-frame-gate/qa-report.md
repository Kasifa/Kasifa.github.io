# QA report

**Status:** PASS (42/42 independent checks).

The validator recomputed every displayed fraction from the frozen 13/13 exact certificate, checked the 23-row source export, verified the 180 x 82 mm one-page PDF and embedded fonts, checked the approximately 600 dpi RGB PNG, confirmed live SVG text with no raster image, and required every recorded text extent to stay inside its declared canvas or panel container. The latter is an auditable string-width/ascent proxy, not a substitute for visual inspection. Final-size, grayscale, and PDF-render derivatives are present. The figure states FINITE GATE ONLY, OPEN packet-survival/full-ledger work, and NOT CLAY.

## Manual visual QA

**PASS (2026-09-01).** The 600 dpi master, grayscale derivative, 300 dpi PDF render, and 1800-pixel final-size derivative were inspected locally at original detail. Exact fractions remain readable; the c_R marker and both leakage margins are unobscured; paired annular labels, the alpha-separation arrow, and the odd/even implication chain do not clip; the OPEN/NOT CLAY footer is intact. In grayscale, open/filled circle, diamond, square, dashed guide, and outlined interval encodings remain distinguishable. The PDF render matches the master composition.
