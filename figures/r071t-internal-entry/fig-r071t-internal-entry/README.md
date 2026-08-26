# fig-r071t-internal-entry

Paper-ready four-panel figure package for R0.71T. It contains the primary
pseudo-spectral finite Fourier--Galerkin shooting run, an independent direct-
convolution reconstruction, raw results, progress and resource logs, a
reviewed plotting table, vector PDF/SVG, a 600 dpi PNG, checksums, and
color/grayscale/PDF-render QA previews.

Run the commands in `command.txt` from the repository root. The numerical
model is the (x_3)-independent, three-component invariant sector of periodic
three-dimensional NSE. The primary run uses (N=10, K_{\rm cut}=2); the
independent refined check uses (N=12, K_{\rm cut}=3) at (	au=0.04).

This package records finite Galerkin PDE time stepping. It is not DNS and has
no continuum truncation-error certificate. Its role is to corroborate the
analytic local-flow implicit-function construction, not replace it.
