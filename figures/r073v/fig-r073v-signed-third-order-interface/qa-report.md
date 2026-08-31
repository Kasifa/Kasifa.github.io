# R0.73V formal-figure QA report

**Status:** PASS — EXACT CERTIFICATE / ARTIFACT SEAL

**Checks:** 147/147

The primary sparse-polynomial producer and independent dense-polynomial
producer have identical complete `commonCore` objects. Their frozen hashes,
common-core digest, complete-table digest, and immutable certificate commit
bindings passed before source-data reconstruction.

Exact compressed-lift coefficients, all displayed four-site matrices and
small-s orders, six-site zero/nonzero rows, the selected quartic coefficient,
finite-epsilon extraction, and parabolic dilation passed. All 57
certificate-derived CSV rows are string-exact. The 101 plotted-profile rows
are exact outside the renderer-only `y` field; those `y` values satisfy both
the fixed absolute and ULP portability bounds against the closed formula and
were not used as a fit.

SVG/PDF/600-dpi PNG integrity, dimensions, declared palette, final-size raster,
grayscale conversion, and independently regenerated PDF raster passed. Visual
inspection confirmed legible panel titles, equations, matrices, direct labels,
curve annotation, and claim-boundary footnotes in color, grayscale, final-size,
and PDF renderings.

The package is coefficientwise and selected-coefficient in scope. It does not
claim whole-field information non-recovery, finite-hierarchy nonclosure,
singularity, global regularity, or a Clay result.

`navierStokesSimulation=false`; `fittedScalingLaw=false`; `dgxUsed=false`;
`ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX`; `NOT CLAY`.
