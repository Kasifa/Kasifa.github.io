# R0.71I figure QA

Status: passed automatic validation, independent validation, and direct
visual inspection.

- Inspected the original 600 dpi PNG at full resolution
  (4204 x 2551 px).  All four titles, panel letters, axes, legends,
  mathematical labels, markers, and annotations remain inside the canvas.
  The zero-entry squares in panels A and D have explicit left margins and are
  not clipped by their axes.  No curve is hidden by an annotation.
- Inspected the 1780 x 1080 grayscale preview.  Panel A preserves the open
  exact-maximum circle and zero-entry square.  Panel B preserves its open
  dyadic squares.  Panel C retains solid/dashed line styles, an open test
  point, and separate left/right axes.  Panel D retains open endpoint squares
  and a bidirectional refresh bracket.  No conclusion depends on color.
- Rasterized the one-page vector PDF independently at 180 dpi
  (1262 x 766 px) and inspected the result.  It matches the PNG composition
  with no clipping, missing glyphs, overlap, or line-art failure.
- The PDF page is 178.0000 x 108.0001 mm to pdfinfo precision.  The PNG is the
  required 600 dpi archival raster; the one-pixel rounding follows from
  converting millimetres to pixels.
- validation.json passes 35 checks across all 567 closed-form rows.  Its
  maximum binary64 formula disagreement is approximately
  \(1.39\times10^{-17}\).
- independent-validation.json passes 28 checks.  Its separate 70-digit
  Decimal path has maximum absolute CSV disagreement
  \(1.18\times10^{-12}\) at the largest \(K^2\)-scaled ordinate, maximum
  relative disagreement there \(8.26\times10^{-17}\), maximum exact-balance
  error \(2.50\times10^{-17}\), and maximum recorded sampling-grid roundoff
  \(2.0\times10^{-16}\).
- Panels A and B are explicitly labelled as common-heat calculations; they
  are not presented as NSE solutions or as fitted data.  Panel B fixes
  \(\nu=1\) and labels the exact algebraic \(K^2\) law.
- Panel C is explicitly labelled as the fixed-window \(K\to\infty\) profile
  of an exact global-smooth 2D3C NSE family.  It is not presented as a finite-
  \(K\) numerical trajectory, and the selected smooth radial two-ring
  multiplier is not conflated with the preselected broad dyadic frame.
- Panel D labels \(\delta\) as cutoff modulation and the exact refresh gap as
  \(3/28\); \(\delta\) is not presented as natural time.

Claim boundary: the package contains closed-form formula evaluation, a
rigorous fixed-window 2D3C limit, and exact initial-time cutoff algebra.  It
is not DNS, a finite-\(K\) PDE trajectory, or a fitted scaling law.  The
volume-only obstruction is not a no-go theorem for every face-paid weighted-
BV target.  The package proves no broad-frame theorem, continuation result,
regularity theorem, singularity statement, originality claim, or
Millennium-problem conclusion.
