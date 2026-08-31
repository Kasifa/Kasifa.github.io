# R0.73P figure QA protocol

## Current non-PDF preflight

1. Run `plot.py --data-only` and confirm that only formula data, environment,
   results, and monitoring logs are written.
2. Run `plot.py --render-nonpdf` and confirm that the only figure formats
   written are SVG and PNG.
3. Run `validate.py --preflight` before visual confirmation. The validator must
   fail on a present PDF, unexpected inventory item, formula drift, an
   incomplete lattice enclosure, a discrete value above the continuous bound,
   a wrong raster size, or an empty SVG.
4. Inspect `qa-final-size.png` at its encoded 178 mm by 86 mm print size.
   Confirm readable labels, non-overlapping annotations, correct log axes, and
   the exact warning in Panel C.
5. Inspect `qa-grayscale.png`. Confirm that the two threshold curves, three
   exponent curves, open-strip hatch, and two heat curves remain separable.
6. Re-run `validate.py --preflight --confirm-nonpdf-visual-qa`, then run
   `validate.py --preflight --verify-only`.

## Deferred formal sealing

The current round forbids PDF generation. A later formal run must additionally
create vector `figure.pdf`, rasterize it independently as `qa-pdf.png`, inspect
that raster at final size, bind all source files to an immutable Git commit,
and run `validate.py --final --confirm-visual-qa --source-commit COMMIT`.
Until those steps pass, `manifest.json` must remain a draft and
`allPrerequisiteChecksPass` must remain false.

## Mathematical cross-checks

- Verify \(N^3\varepsilon_{H^3}=1\) and
  \(N^{1/2}\varepsilon_{\dot H^{1/2}}=1\) on every Panel A row.
- Verify the three Panel B powers exactly equal
  \(-\gamma\), \(1/2-\gamma\), and \(3-\gamma\).
- Verify the open interval is represented as open: the lines
  \(\gamma=1/2\) and \(\gamma=3\) are boundaries, not interior points.
- Verify the endpoint statement: \(\gamma=1/2\) needs a strict prefactor
  inequality.
- Reconstruct the complete set of three-square radii through \(64^2\), recompute
  every Panel C maximum, and verify the tail monotonicity inequality
  \(64^2>3/(2\tau_{\min})\).
- Verify the continuous envelope formula and
  \(H_{\rm disc}(\tau)\leq(3/(2e\tau))^{3/2}\) at every sampled \(\tau\).

## Claim-language check

Search the package for any statement that calls Panel C a nonlinear smoothing
or entry theorem. The exact sentence `LINEAR ONLY — NOT A NONLINEAR ENTRY
CERTIFICATE` must be visible inside Panel C. The caption must state that this
is not evidence for a solution of the Navier--Stokes millennium problem.
