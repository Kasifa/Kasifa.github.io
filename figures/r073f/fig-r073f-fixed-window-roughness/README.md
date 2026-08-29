# R0.73F fixed-window finite diagnostic figure

This package turns the archived R0.73F binary64 data into a 178 mm by
132 mm, four-panel journal figure.  It does not rerun the scientific
propagation.  `plot.py` binds every input by SHA-256 and writes PDF, SVG, and
600 dpi PNG masters; `validate.py` checks dimensions, vector text, input
bindings, the numerical sentinels, and the claim boundary, then produces
final-size, grayscale, and PDF-raster QA views.

The endpoint `d_diag = 0.01` is a diagnostic choice, not a certified analytic
`d0`.  The Fourier cutoffs, sampled times, binary64 gains, and agreement checks
are finite diagnostics only.  They do not prove a continuum dichotomy,
continuum spectral statement, nonlinear Navier--Stokes assertion, or any Clay
Millennium statement.  Panels C and D are exact abstract counterexamples, not
claims about the exact Fourier row.

Run the two commands in `command.txt` from the repository root.  The package
uses the shared `figures/journal.mplstyle`.  A `validated` manifest is
content-addressed but intentionally unsealed at the Git level; conversion to a
repository-level `formal` package requires a later clean source/certificate
commit.
