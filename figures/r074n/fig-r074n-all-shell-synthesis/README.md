# R0.74N formal figure package

This deterministic package visualizes the exact all-shell synthesis of the
signed annular collar flux.  It separates the complete index set into
`k <= j-1`, `k = j`, and `k >= j+1`, then records the distinct analytic
payment used in each range.

Run with the pinned local runtime:

    python3 plot.py
    python3 validate.py

Publication masters are `figure.svg`, `figure.pdf`, and the 600-dpi
`figure.png`.  QA derivatives are the 200-dpi final-size raster and grayscale
copy, an independent 300-dpi raster of the vector PDF, and a macOS Quick Look
raster of the self-contained SVG.

The source theorem has an independent analytic audit with result PASS.  The
figure is a schematic proof ledger, not to scale, not DNS, and not a sampled
stochastic path.  Its theorem is familywise for one exact smooth construction.
It is not a universal endpoint inequality or a Navier--Stokes regularity
result.  **NOT CLAY.**  Package validation and the separate independent
figure-package audit do not enlarge that boundary.
