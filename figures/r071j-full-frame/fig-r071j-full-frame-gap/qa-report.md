# R0.71J figure QA

Status: passed producer validation, independent validation, and direct visual
inspection.

- Inspected the original 600 dpi PNG at full resolution
  (4204 x 2645 px). The header, blossom, four panel letters, five plotting
  axes, titles, legends, formula labels, markers, and footer remain inside
  the canvas. Panel D's negative ledger annotation stays inside its bar;
  the lower support-strip label and the footer do not overlap.
- Inspected the 1780 x 1120 grayscale preview. Panel A preserves opposed
  hatches and the zero-defect cross. Panel B preserves four line styles and
  marker shapes. Panel C preserves solid-circle and dashed-square series.
  Panel D preserves signed hatches plus circle/square channel markers. No
  conclusion depends on color.
- Rasterized the one-page vector PDF independently at 180 dpi
  (1262 x 794 px) and inspected the result. It matches the PNG composition
  with no clipping, missing glyphs, overlap, or line-art failure.
- The PDF page is 178.0000 x 111.9999 mm to `pdfinfo` precision. The PNG is
  the required 600 dpi archival raster; one-pixel rounding follows from the
  millimetre-to-pixel conversion.
- `validation.json` passes 48 producer checks across all 856 closed-form
  rows. Its direct binary64 formula disagreement and positive-identity
  residual are both zero because the generator and producer validator
  evaluate the same explicit formulas independently in separate passes.
- `independent-validation.json` passes 35 checks. Its separate 80-digit
  standard-library Decimal path has maximum absolute CSV disagreement
  \(2.16\times10^{-15}\), maximum relative disagreement
  \(3.42\times10^{-15}\), maximum exact-balance error
  \(1.56\times10^{-21}\), and maximum recorded grid roundoff
  \(7\times10^{-17}\). It imports neither the producer nor NumPy,
  Matplotlib, SymPy, or Pillow.
- Panel A shows an exact pointwise instance of the positive-defect identity;
  it does not present a fitted decomposition.
- Panel B labels normalized closed-form fixed-window profiles; it is not a
  finite-\(K\) NSE trajectory.
- Panel C explicitly labels its dyadic abscissae as a reference grid and
  states that the large-\(K\) threshold is not quantified. The \(-2\) and
  \(-4\) exponents are exact algebra, not regression estimates.
- Panel D retains the exact signed Fourier ledger and plots all six mode
  radii inside the parent flat top; no selected two-ring replacement is used.

Claim boundary: the package concerns the R0.71E section 10.1 parent-only
broad frame, global cell \(\chi=1\), and heat height zero. It does not cover
the later child refinement, matched spatial cells, denominator or refresh
faces, another Navier--Stokes budget, or full face-paid weighted BV. It is
not DNS and proves no continuation, regularity, singularity, originality, or
Millennium-problem conclusion.
