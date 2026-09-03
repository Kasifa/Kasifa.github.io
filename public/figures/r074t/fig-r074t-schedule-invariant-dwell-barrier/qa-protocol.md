# R0.74T figure QA protocol

## Mathematical and data checks

1. Recompute the exact rational margin
   \(5(8/3969)-75/22528=603445/89413632>0\).
2. Verify the exact schedule endpoints, unit \(R^3\) lengths, terminal-slab
   containment, and gap \(R^2-3R^3>0\).
3. Recompute the atomic coefficient
   \(2^{-2}\cdot4\cdot2^{3/2}=2\sqrt2\) and the exponents
   \((1,3/2,1,-5/4,-1/2)\).
4. Regenerate all 121 Panel C and 121 Panel D values from the formulas in
   `config.json`; do not read plotted pixels as data.
5. Check the exact identity
   \(\log\Lambda_2=(2/3)[\log\theta+mL_1^2+d_L-\tfrac12\log L_2]\)
   for \(m=5c_\gamma-a_S\), and the corresponding \(C=1\) dwell ceiling.

## Rendering checks

1. Confirm the 178 mm by 116 mm canvas, 4204 by 2740 600-dpi PNG, vector SVG,
   and one-page PDF with embedded fonts.
2. Inspect `qa-final-size.png` at 300 dpi for legibility, clipped text, and
   detached annotations.
3. Inspect `qa-grayscale.png`; no comparison may depend on hue alone.
4. Inspect `qa-pdf.png`, an independent PDF rasterization, and compare it
   against the final-size PNG.
5. Confirm the header blossom is fixed at top right and the scope language is
   present in both SVG and extracted PDF text.

## Required scope labels

`ANALYTIC SCHEMATIC`, `DERIVED ANALYTIC VALUES`, `NOT PDE DATA`, `NOT DNS`,
and `NOT CLAY` must be embedded in the rendered outputs. Panel A must also
say `GAP COMPRESSED / NOT TO SCALE`.

## Preseal and final-seal policy

The mathematical core and certificate are frozen at commit
`b120598d36140385676bb4a9922d46abcdff0ba4`. The current archive carries only
`PENDING_FIGURE_SOURCE_COMMIT`. Final release is forbidden until the actual
21-file figure-source commit is bound. Deterministic-core hashes must survive
a complete second render unchanged.
