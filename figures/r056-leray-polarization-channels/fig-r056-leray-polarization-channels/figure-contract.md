# Figure contract — R0.56 Leray polarization channels

- **Analytical question.** After resolving one Fourier--Leray triad into its
  two transverse output polarizations, which channel retains the critical
  high--high-to-low constant and which channel has a strict gap?
- **Takeaway.** The normal channel has exact gain
  \(g_N=\sqrt{1-\mu^2}\), independent of the shell ratio and capable of
  attaining one. The in-plane channel satisfies
  \(g_T\le(1+\rho)/2<1\) when \(|k|/|p|\le\rho<1\), with sharp separated
  limit \(1/2\). Positive angular averaging does not create shell decay for
  the normal channel.
- **Figure family.** Three coordinated line comparisons: a fixed-shell-ratio
  channel profile, two exact integer-family asymptotics, and the exact
  near-saturation solid-angle law.
- **Data sufficiency.** Panel (a) uses 801 exact-rational squared-gain rows at
  \(\varepsilon=1/8\). Panel (b) uses 512 exact rows from each of two
  all-index families. Panel (c) uses 401 exact-rational squared-measure rows.
  The analytic note proves the formulas; the plotted rows are presentation
  data backed by a certificate containing 1,764,912 exhaustive integer
  triads and 400,000 family instances.
- **Renderer.** Reproducible Matplotlib static export.
- **Palette.** Hard two-root cap: blue for the unresolved normal channel,
  gold for the improved planar channel, with neutral ink/grid and a restrained
  red theorem-bound line.
- **Non-color distinctions.** Solid, dashed, and dotted lines; open versus
  filled markers; direct annotations; and panel-specific axes preserve the
  comparison in grayscale.
- **Footprint.** One double-column figure, 178 mm by 105 mm, exported as PDF,
  SVG, and 600 dpi PNG.
- **Final QA.** Inspect the color PNG, a true grayscale conversion, and a
  rasterization of the PDF at final physical size. Validate every data row,
  embedded fonts, dimensions, hashes, and monitored provenance.

