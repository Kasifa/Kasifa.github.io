# R0.72Y formal figure QA protocol

1. Require distinct clean source and certificate commits.  Require the
   certificate commit to descend from the source commit and the package source
   files to be unchanged between them.
2. Recompute every Panel B sample from
   `exp(-2*xi^2*d)*(1+Lambda^2*d^2*(exp(-2*d)+exp(-8*d))/8)`.
   Require all three representative curves to exceed the no-growth reference
   at some positive time, and require both positive-xi series to be present.
3. Recompute every Panel C sample as `alpha^power`.  Require the exact powers
   1, 2, and 0; no regression or fitted exponent is permitted.
4. Confirm Panel A states the `mu > 0` restriction on Orr-Sommerfeld/Squire
   reconstruction, the closed scalar embedding, the false uniform-contraction
   claim, and the open strong full-row A2 estimate.
5. Inspect the 178 mm final-size preview, grayscale preview, and independent PDF
   render.  Check all labels, formulas, direct annotations, markers, dashes,
   panel borders, and axis limits.  Confirm there is no clipping or overlap.
6. Confirm the PDF is one vector page at 178 mm by 145 mm, contains no raster
   image XObjects, and embeds the declared Arial fonts.  Confirm the SVG uses a
   matching view box and the PNG carries 600-dpi metadata at the expected pixel
   dimensions.
7. Confirm the visible boundaries `EXACT COUNTEREXAMPLE - NOT A STABILITY
   PROOF`, `EXACT RATE GUIDE - ANALYTIC PROOF ELSEWHERE`, `OPEN`, and `FALSE`.
8. Run the package-local fail-closed validator and the repository-wide figure
   schema validator.  A formal release requires no errors or warnings.
