# R0.74M formal figure package

This deterministic package visualizes the final-segment expulsion mechanism
for the complete nearest inward (j-1) collar.  The curve in panel A is a
schematic of the analytic modulus event; it is not a simulated or sampled
Brownian path.

Run with the pinned local runtime:

    python3 plot.py
    python3 validate.py

Publication masters are `figure.svg`, `figure.pdf`, and the 600-dpi
`figure.png`.  QA derivatives are the 200-dpi final-size raster, its
grayscale copy, and an independent 300-dpi raster of the vector PDF.

Claim boundary: nearest inward estimate proved in the current source note;
independent analytic audit PASS; full collar synthesis open; not Clay.  This
package records its own deterministic validation and visual QA.  Any
independent figure-package audit is reported separately and is not claimed by
this package.
