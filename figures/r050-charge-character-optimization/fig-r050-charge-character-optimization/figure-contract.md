# R0.50 figure contract

- Analytical question: what is the global shape of the active-column
  threshold across the multiplicative charge-character family, how much does
  exact optimization improve on `c=4/5`, and does the true column remain
  uniformly dominant near the optimum?
- Takeaway: the threshold has one certified global maximum in
  `0.8024563827<c_*<0.8024563828`, with
  `0.382619813709565<r_*(c_*)<0.382619813709566`.  The gain over `c=4/5` is
  strict but only about 3.061 ppm in threshold radius.  All 243 competing
  columns remain strictly below the true `s=162,j=81` column throughout the
  exact isolating rectangle.
- Family and variants: global threshold-profile line; focused local-gain line;
  ranked logarithmic competitor-gap curve.
- Data sufficiency: 191 global and 151 local 90-digit presentation samples are
  evaluated from the reconstructed exact degree-80 Laurent polynomial.  They
  show shape only.  The optimum, four-face signs, uniqueness, and all 243
  competitor gaps come from the pinned GMP certificate.
- Renderer: reproducible Matplotlib static export.
- Palette policy: hard two-root cap using blue and gold plus neutral ink.
- Non-color encoding: solid and dashed lines, open circle and filled diamond
  markers, direct labels, ordering, and logarithmic position preserve the
  distinctions in grayscale.
- Output footprint: 178 by 112 millimetres; PDF, SVG, and 600 dpi PNG.
- Final QA: color PNG, true grayscale conversion, and Poppler-rendered PDF at
  final size, followed by archive validation and hash verification.
