# R0.47 figure contract

- Analytical question: does preserving the exact charge--degree lattice remove
  the apparent large-charge failure near `r=0.377`, and which real input
  column becomes limiting afterward?
- Takeaway: the lattice theorem lowers the large-charge sector below one, but
  the genuine fixed-charge endpoint `s=162,j=81` becomes active.  It passes at
  `r=0.376932` and fails at the adjacent millionth `r=0.376933` in the current
  two-block weighted-l1 norm.
- Family and variants: ordered fixed-charge line with a highlighted maximum,
  two rational parity-branch lines on `y=1/s`, focused radius line-dot
  comparison, and exhaustive sector lollipops.
- Data sufficiency: all 239 fixed positive charges are exact all-degree
  endpoint theorems.  The parity curves are exact rational presentation
  samples; the all-order conclusion comes from two continuous-interval
  degree-318 Bernstein derivative certificates, not from the samples.
- Renderer: reproducible Matplotlib static export.
- Palette policy: hard two-root cap using blue and gold plus neutral ink.
- Non-color encoding: marker shape, open versus filled marks, line style,
  direct labels, and threshold lines preserve every distinction.
- Footprint: 178 by 142 millimetres; PDF, SVG, and 600 dpi PNG.
- Final QA: color PNG, true grayscale image, and Poppler-rendered PDF at final
  aspect ratio, followed by archive validation and hash verification.
