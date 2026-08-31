# R0.73O finite Kolmogorov-spectrum figure

Formal two-panel source package for the R0.73O finite Fourier diagnostic.  It
binds the exact `research/certificates/r073o` source rows, exports vector
PDF/SVG and a 600-dpi PNG, and keeps final-size, grayscale, and PDF-raster QA
surfaces.

Panel A shows the finite spectral abscissa through the published rigorous
critical interval.  Panel B checks truncation stability and the eigen-residual
at the physical target.  The published interval remains an external
computer-assisted theorem input.  Neither panel proves the infinite-
dimensional spectrum or the nonlinear escape theorem.

Run `command.txt` from the repository root.  The validator fails closed on
upstream diagnostic or independent-recomputation failure, source-data drift,
format or dimension drift, escaped claim boundaries, and missing visual QA.
