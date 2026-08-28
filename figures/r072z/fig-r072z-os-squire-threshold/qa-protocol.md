# R0.72Z formal figure QA protocol

1. Require distinct clean source and certificate commits, certificate descent
   from source, and byte-unchanged package source files.
2. Recompute Panel A signed-envelope rows as
   `4*M3*(g*alpha^2)^(-5/2)` and require the plotted crossing of `theta0` at
   `(4*M3/theta0)^(2/5)`. Recompute every high-mode row from report equation
   (7.5) and verify convergence to `sqrt(2)*exp(-d)/27`; no fitted slope.
3. Recompute Panel B low-mode derivatives from report equation (7.4), require
   strict positive and negative samples for each declared `|c|`, and retain
   the visible zero line. Recompute the tangent ratio from report equation
   (8.4), require it below one for positive alpha and tending toward one as
   alpha decreases, and retain the abstract/not-physical warning.
4. Recompute Panel C orientation rows as
   `R/sqrt(1+R^2+(rho/gamma)^2)` and require `0 < chi < 1`. Recompute the
   normalized history multipliers with the exact `min` formulas and constants
   `A=2T/(1-vartheta)`, `B=2T/(1-vartheta^2)`.
5. Confirm the visible payments `|Lambda| PAID` and `Q HISTORY REQUIRED`, and
   that the caption says these bounds are conditional and not PDE simulation.
6. Inspect 178 mm final-size, grayscale, and independent PDF previews for
   collisions, clipping, detachment, reference-line visibility, direct-label
   accuracy, and grayscale distinction.
7. Confirm a one-page vector PDF at 178 mm by 145 mm with embedded Arial fonts
   and no raster XObjects; exact SVG dimensions/view box; and 600-dpi PNG
   pixels and metadata.
8. Run package-local and repository-wide fail-closed validators. Formal
   publication requires no errors or warnings.
