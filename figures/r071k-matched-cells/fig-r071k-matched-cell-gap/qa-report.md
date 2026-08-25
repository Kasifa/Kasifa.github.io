# R0.71K figure QA

Status: passed producer validation, independent validation, and direct visual
inspection.

- Inspected the original 600 dpi PNG at full resolution
  (4204 x 2645 px).  The title, subtitle, four panel letters, axes, legends,
  endpoint markers, exponent labels, and scope footer remain inside the
  canvas.  The footer is separated from both lower x-axis labels.
- Inspected the 1780-pixel-wide grayscale preview.  Panel A preserves four
  line styles; panel B preserves filled/open endpoint markers; panel C
  preserves solid-circle and dashed-open-square series; panel D preserves
  the dotted heat and hatched collar bars.  No conclusion depends on color.
- Rasterized the one-page vector PDF independently at 180 dpi and inspected
  the result.  It matches the PNG composition without clipping, missing
  glyphs, overlap, or line-art failure.
- `pdfinfo` reports a 504.567 x 317.48 pt page, equal to 178 x 112 mm to the
  displayed precision.  The archival PNG records 600 dpi.
- `validation.json` passes 40 producer checks over 1477 deterministic rows.
  The maximum partition-of-unity residual is
  \(2.22\times10^{-16}\), and the power-law formula residual is zero.
- `independent-validation.json` passes 15 checks through a separate
  standard-library/80-digit Decimal path and archive signature checks.  Its
  maximum Decimal power disagreement is \(2.5\times10^{-25}\).
- Panel B labels the open local-template marker as an independent diagnostic;
  the theorem uses the analytic denominator bound instead.
- Panel C labels its dyadic frequencies as a reference grid and states that
  \(K_0\) is not quantified.  The \(-2\) and \(-4\) powers are exact, not
  fitted slopes.
- Panel D shows the collar and positive creation at the same aggregate
  \(K^{-2}\) scale.  It does not depict the collar as a controlled or
  coercive term.

Claim boundary: one fixed aligned matched partition is shown.  The figure
does not claim an explicit finite-\(K\) threshold, a collar-paid estimate,
general moving partitions, continuation, regularity, singularity,
originality, or a Millennium-problem conclusion.
