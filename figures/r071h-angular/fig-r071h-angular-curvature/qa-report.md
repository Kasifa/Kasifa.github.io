# R0.71H figure QA

Status: passed automatic validation, independent validation, and direct
visual inspection.

- Inspected the original 600 dpi PNG at full resolution
  (4204 x 2551 px), including separate crops of all four panels. Titles,
  panel letters, axes, legends, mathematical labels, markers, and annotations
  remain inside the canvas. No curve is hidden by an annotation.
- Inspected the 1780 x 1080 grayscale preview. Panel A retains distinct
  circle, cross, and open-square markers on coincident exact curves. Panels B
  and C retain solid/dashed and filled/open distinctions. Panel D preserves
  both boundary curves and the shaded two-power gap without relying on color.
- Rasterized the one-page vector PDF independently at 180 dpi
  (1262 x 766 px) and inspected the result. It matches the PNG composition
  with no clipping, missing glyphs, overlap, or line-art failure.
- The PDF page is 178.0000 x 108.0001 mm to pdfinfo precision. The PNG is the
  required 600 dpi archival raster; the one-pixel width rounding follows from
  converting 178 mm to pixels.
- validation.json passes 28 checks across all 391 closed-form rows. The
  producer formula and exact-balance residuals are zero in binary64.
- independent-validation.json passes 35 checks. Its separate 60-digit Decimal
  path has maximum formula disagreement below \(4.0\times10^{-16}\), maximum
  identity imbalance \(4.0\times10^{-17}\), and maximum recorded sampling-grid
  roundoff \(1.0\times10^{-16}\).
- Panel B states \(t=0\) in its title and displays the fixed values
  \(\nu=1\), \(\|u_0\|_2^2=6\), and \(a_K=K^{-1}\). It is not presented as a
  time-integrated counterexample.
- Panel D labels the \(K^2\) separation as a scaling comparison. No exponent
  was fitted.

Claim boundary: the package contains closed-form formula evaluation and exact
initial-time Fourier algebra only. It is not DNS or a time-evolved 3D
simulation. It proves no general integrated angular no-go, regularity theorem,
singularity statement, originality claim, or Millennium-problem conclusion.
