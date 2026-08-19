# R0.46 figure contract

- Analytical question: does weighting the charge-zero output block preserve
  same-column correlations strongly enough to replace the failed unweighted
  `s=-1` control, and which sector becomes limiting afterward?
- Takeaway: with `kappa=3/4`, the exact correlated column theorem certifies
  `r=0.376`; the large positive-charge sector is then limiting, while the
  separately maximized `2x2` block matrix is demonstrably too coarse.
- Family and variants: weight-envelope line chart, ordered radius line-dot
  comparison, target-sector lollipops, and focused proof-gate lollipops.
- Data sufficiency: all plotted decisions come from the 31-check GMP
  certificate.  The 101 weight-envelope points are presentation samples of
  explicit rational formulas; they are not the all-order proof.
- Renderer: reproducible Matplotlib static export.
- Palette policy: hard two-root cap using blue and gold plus neutral ink.
- Non-color encoding: marker shape, open versus filled marks, line style,
  direct labels, and threshold lines preserve every distinction.
- Footprint: 178 by 140 millimetres; PDF, SVG, and 600 dpi PNG.
- Final QA: color PNG, true grayscale image, and Poppler-rendered PDF at final
  aspect ratio, followed by archive validation and hash verification.
