# R0.74O formal figure package

This deterministic package visualizes the passive-amplitude obstruction to a
scalar-payment-only Navier--Stokes endpoint estimate.  The four directly
labelled panels record (A) the free multiplier \(\varkappa\) in the exact
smooth 2D3C family, (B) closure of every row in the complete scalar payment,
(C) the quadratic growth of the endpoint quantity and positive cumulative
collar flux, and (D) conversion to the realized scalar frontier.

Run with the pinned local runtime:

    python3 plot.py
    python3 validate.py

Publication masters are `figure.svg`, `figure.pdf`, and the 600-dpi RGB
`figure.png`.  QA derivatives are the 200-dpi final-size raster and grayscale
copy, an independent 300-dpi raster of the vector PDF, and a macOS Quick Look
raster of the self-contained SVG.

The figure is an analytic proof ledger, not a simulation, DNS result,
finite-precision asymptotic fit, or sampled trajectory.  It refutes only
universal bounds whose right side is a function of the frozen scalar payment
alone.  It constructs no singularity and proves no global regularity theorem.
**NOT CLAY.**  Package validation does not claim the separate independent
figure-package audit.
