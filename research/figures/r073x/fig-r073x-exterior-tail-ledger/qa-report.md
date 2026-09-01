# R0.73X figure QA report

**Status:** PASS — FORMAL FIGURE-SOURCE SEAL

**Checks:** 50/50

All four frozen sources matched their SHA-256 values and immutable blobs at
source commit `958b6b4216f6914a5d42f7712b6bc9b218caf801`.  The renderer parsed the
Gaussian denominator `32` and harmonic-pressure exponent `4` from the proof,
then reconstructed all 46 source-data rows.

SVG, PDF, and 600 dpi PNG integrity passed at
178 mm by 92 mm.
The PDF has one page, MediaBox 504.566929 by 260.787402 pt,
3 referenced font resource(s), and
3 embedded font resource(s).  The independently
regenerated PDF raster is 1800 by
931 pixels and exactly matches `qa-pdf.png`.

Final-size, grayscale, and PDF rasters were inspected for clipped or colliding
titles, formulas, labels, ticks, legends, annotations, and footer text.  No
clipping was observed.  Solid/dashed lines, filled/open markers, and distinct
circle/square/triangle shapes preserve every comparison in grayscale.  The
locked five-petal research blossom is present at the top-right data-free token.

After the log-axis repair, the Site owner independently reviewed the final-size
asset and returned `PASS`: Panels A and B both display the $10^0$ major tick;
Panel A keeps `yMaximum=40`, above the $\theta^{-2}$ prefactor's largest
plotted value; Panel B remains normalized at $m=1$.  The owner also confirmed
no clipping or collisions, grayscale-distinguishable line/marker encodings,
PDF/PNG visual consistency, and clear `NOT DNS` / `NOT CLAY` boundaries.

Panels A--B are visibly labelled `analytic formula`.  Panel C is visibly
labelled `static functional diagnostic · NOT DNS`.  The pressure and Gaussian
rows are marked as non-interchangeable.  The static packet is not an NSE
trajectory or associated-pressure counterexample.  No DNS, fit, compact-cutoff
closure, epsilon regularity, global regularity, or Clay claim is made.

The 21 figure source/raw artifacts are byte-identical to immutable commit `161fd9d5ca3ebea55e34567188a0e152ee39ecfb` and their exact scoped Git status is clean.  This is the formal figure-source seal; only the four metadata files are left for the separate reseal commit.  `dgxUsed=false`; `NOT CLAY`.
