# R0.72W visual and numerical QA protocol

The source stage performs structural checks only and records no visual or
numerical approval. Before a later formal build passes
`--visual-inspected`, inspect all of the following.

1. View the PDF at 178 mm width. Confirm every panel letter, formula, direct
   label, status box, tick, and diagnostic value is legible and unclipped.
2. Compare the PDF, SVG, and 600 dpi PNG masters. Confirm identical panel
   order, dimensions, analytic curves, diagnostic lines, and claim statuses.
3. Inspect the grayscale preview. Coarse, medium, and fine diagnostic curves
   must remain distinguishable by dotted, dashed, and solid strokes, direct
   resolution labels, and open/filled markers; hue alone is insufficient.
4. Confirm Panel A uses the exact pair
   `(2(cos z-cos 2z), 2(-cos z+4cos 2z))`, marks the collision, extrema, and
   antipode, and states that the origin is excluded.
5. Recalculate all four centered no-go ratios from the formulas in
   `config.json`; confirm that the plotted axis starts at zero and values are
   not clipped.
6. Confirm Panel B visually separates compact Taylor absorption from the
   escaping/torus obstruction. It must say `global termwise absorption:
   FALSE` before displaying the exact nonperturbative transfer.
7. Confirm Panel C starts its norm axis at zero and labels the calculation
   `NUMERICAL DIAGNOSTIC ONLY — NOT PROOF`. It must not call a discrete norm
   the analytic constant or an optimal continuum propagator norm.
8. Inspect `data.csv`, `results.json`, `validation.json`, and
   `progress.ndjson`. Confirm 5 alpha values, all 3 `(N,N_S)` levels, 32 fixed
   power iterations, finite power residuals, finite forward--adjoint defects,
   and an explicit relative-to-finest audit.
9. Confirm the PDE diagnostic uses the full exact potential on `[-1,1]`,
   NumPy float64/complex128, deterministic fixed vectors, and no random seed.
10. Confirm the visible boundaries are exactly: exact periodic scalar-row
    block contraction CLOSED; outer concatenation, nonlinear closure, and
    Clay OPEN; the diagnostic does not evaluate `C_T`.
11. Confirm the only chromatic roots are blue `#285f8f` and gold `#a6781f`;
    neutral ink, muted gray, grid gray, white, and pale gold are allowed.
12. Confirm the five-petal research blossom remains at the top-right header,
    overlaps no title or evidence, and carries no data.
13. Confirm formal public PDF/SVG/PNG copies are byte-identical to package
    masters and the strict validator passes.
