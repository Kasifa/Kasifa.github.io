# Visual QA protocol

1. Recompute `source-data.csv` from the exact Step 13 formulas.
2. Render vector PDF and SVG masters at 178 mm width.
3. Render the PDF at 600 dpi and compare pixels with `figure.png`.
4. Inspect the 300 dpi final-size derivative and the 600 dpi grayscale copy.
5. Confirm that titles, axes, formula labels, status boxes, and the explicit
   `ANALYTIC SCHEMATIC | NOT SIMULATION OR DNS` boundary are legible.
6. Confirm that no panel visually represents an abstract sequence or tree as a
   Navier--Stokes simulation.
7. Validate every packaged hash and all frozen-source bindings.
