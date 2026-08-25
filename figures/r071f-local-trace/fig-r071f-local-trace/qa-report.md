# R0.71F figure QA

Status: passed automatic validation and direct visual inspection.

- Inspected the original 600 dpi PNG at full resolution (4204 x 2456 px): all four panels, titles, axis labels, legends, annotations, and panel letters remain inside the canvas. The shortened Panel B title is complete and unclipped.
- Inspected the grayscale conversion at full resolution: exact curves, all four independent FFT marker shapes, dashed/dotted asymptotes, open/filled envelope markers, and the two geometry families remain distinguishable without color.
- Rendered the PDF independently at 300 dpi with `pdftoppm` and inspected the raster result. It matches the PNG composition, with no clipping, missing text, or line-art failure.
- `pdfinfo` reports one unencrypted page of 504.567 x 294.803 pt, equal to 178 x 104 mm to output precision.
- Panel A discloses the display-only horizontal marker offsets (at most 0.018 in tau); the CSV retains the true tau values. Its largest independent FFT relative residual is 7.1e-16.
- Panel B separates the exact finite-height multiplier from its short-box and long-box limits. Panel C states that unknown prefactors are divided out and does not present full-frame measurements. Panel D states that the curves are different smooth solutions, not a blow-up trajectory.
- The figure contains exact formulas, independent FFT checks, normalized analytic envelopes, and scaling families. It is not DNS, fitted data, or PDE time stepping.
