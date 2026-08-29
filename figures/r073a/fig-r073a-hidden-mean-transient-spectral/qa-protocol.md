# R0.73A formal figure QA protocol

1. Recompute every Panel A hidden-mean and singular-limit row. Require the
   nonzero `mu -> 0` normalized-bracket limit, `c_mu -> c0 != 0` path condition,
   and visible statements that the abstract tangent has no hidden coordinate
   and fixed `Lambda` remains undecided.
2. Recompute every Panel B `J(s,d)` and analytic envelope row. Confirm the
   envelope is an upper bound from the analytic proof, not observed gain.
3. At source/draft stage require `CERTIFIED X_mu GAIN: PENDING - NOT PLOTTED`
   and zero certificate rows. Formal mode must refuse this state.
4. Before formal mode, require the external certificate CSV schema
   `certificateId,s,d,mu,c,gain,bound,sourceCommit,certificateCommit`, validate
   `0 < gain <= bound + 2e-8`, where `2e-8` is a fixed numerical crosscheck
   tolerance, and bind its SHA-256 in the generated manifest. Preserve the raw
   gain; do not clip it to the bound.
5. Recompute Panel C transformed display values from the raw spectral edge and
   numerical abscissa. Require exactly 30 `N=40` source rows / 60 plotted metric
   rows and byte-bind the audited target CSV and its validation ledger.
6. Confirm visible `FINITE GALERKIN N=40 - NOT INFINITE-DIMENSIONAL` and the
   absence of language claiming a spectral theorem, continuous-time maximum,
   nonautonomous concatenation, nonlinear closure, or Clay solution.
7. Inspect final-size, grayscale, and independent PDF previews for clipping,
   detached labels, marker/dash distinction, transformed-axis honesty, and
   readability at 178 mm.
8. Confirm one-page vector PDF with embedded fonts and no raster XObjects,
   exact SVG dimensions/view box, and PNG size/metadata at 600 dpi.
9. Require both Panel C signed-log domains to contain every plotted `N=40`
   value with at least `0.2` transformed-unit padding and retain a visible zero
   tick/reference. Reject any mark outside its axes.
10. Require Panel A/B formulas outside their data rectangles and require compact
    `J start` and envelope `mu/|c|/s` legends with matching dash/marker encodings.
