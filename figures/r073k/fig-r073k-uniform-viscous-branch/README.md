# R0.73K uniform viscous-branch diagnostic figure

This package renders a 178 mm four-panel journal figure from the sealed
R0.73K finite Fourier diagnostic and its independent recomputation.

- Panel A plots the real selected eigenvalue across all 17 frozen parameter
  nodes at cutoff `N=160` for four core viscosity levels.
- Panel B compares the d-uniform finite-difference drift rate with the
  inviscid-adjoint first-order formula on all 11 positive core viscosity
  levels.
- Panel C shows the finite projector difference and its conditioning over the
  same complete core grid.
- Panel D records adjacent-cutoff projector discrepancies together with right
  and left embedded residuals.

The analytical question is whether the complete frozen grid displays a
coherent discrete rank-one viscous branch and whether its first-order and
cutoff diagnostics close. The supported takeaway is deliberately limited to
the finite Fourier matrices: the primary 1,190-row computation passes, the
952 cross-cutoff rows are complete, and an implementation that reconstructs
the matrices from explicit Fourier coefficients agrees within the frozen
tolerances.

The renderer uses a hard two-root palette cap (blue and orange) plus
neutrals. Stroke patterns, marker shapes, open fills, uncertainty bands, and
panel position retain the distinctions without color. `source-data.csv`
contains the 204 largest-cutoff core rows and nine independently derived
cutoff summaries used by the figure, with upstream paths and SHA-256 digests.

Run `command.txt` from the repository root. The archival outputs are vector
PDF, vector SVG, and a 600 dpi PNG. The QA surfaces are a final-size raster, a
grayscale raster, and an independently rasterized PDF.

This is a finite-dimensional diagnostic, not a continuum proof. It does not
certify an explicit continuum viscosity threshold, an adiabatic estimate,
nonlinear or three-dimensional Navier–Stokes control, finite-time
singularity, or the Clay problem.
