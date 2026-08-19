# R0.48 figure contract

- Analytical question: where exactly does the active induced column cross one,
  is that root unique, and do all other charge sectors stay strictly below it
  throughout the adjacent millionth window?
- Takeaway: the degree-80 active-column polynomial has one positive root in a
  width-`10^-18` rational interval.  An exact monotone sandwich keeps all 243
  competitors below the active column on `[0.376932,0.376933]`.
- Family and variants: focused threshold-crossing line, two-endpoint signed
  lollipops with Sturm variation labels, ranked logarithmic dominance-gap
  curve, and focused horizontal lollipops for the active left endpoint and the
  seven nearest right-end competitors.
- Data sufficiency: 101 curve points are exact rational presentation samples
  of the explicit degree-80 polynomial.  Root existence and uniqueness come
  from coefficient positivity and an 81-polynomial exact Sturm sequence, not
  from the samples.  The gap curve contains all 243 exact competitor bounds.
- Renderer: reproducible Matplotlib static export.
- Palette policy: hard two-root cap using blue and gold plus neutral ink.
- Non-color encoding: marker shape, open versus filled marks, line style,
  direct labels, ordering, and threshold lines preserve every distinction.
- Output footprint: 178 by 142 millimetres; PDF, SVG, and 600 dpi PNG.
- Final QA: color PNG, true grayscale image, and Poppler-rendered PDF at final
  aspect ratio, followed by archive validation and hash verification.
