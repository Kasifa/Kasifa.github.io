# R0.49 figure contract

- Analytical question: does the exact multiplicative charge character
  `omega_s=(4/5)^s` move the true reduced-system threshold, which center
  charges create that threshold, and what geometric trade-off does the new
  anisotropic norm make?
- Takeaway: the same true `s=162,j=81` column crosses one at a globally unique
  positive root in a width-`10^-18` interval near `0.3826186424`.  All 243
  competitors remain strictly below it on the full adjacent-millionth window.
  Charges `q=-1` and `q=+1` supply about 88.8% of the active column.  Relative
  to the R0.48 certified threshold, the new polydisc stretches the `Z` radius,
  contracts the `W` radius, and increases the fixed-charge `R=Z^2W` disk
  radius by a strict lower factor about `1.04594`; the polydiscs are not nested.
- Family and variants: focused threshold-crossing line; compact horizontal
  contribution bars; ranked logarithmic dominance-gap curve; signed
  horizontal lollipops for normalized polyradius and fixed-charge-radius
  changes.
- Data sufficiency: 101 threshold-curve points are exact rational presentation
  samples of the explicit degree-80 polynomial.  Root uniqueness comes from
  coefficient positivity and an 81-polynomial exact Sturm sequence.  The
  contribution table contains all 158 center charges, with only the display
  tail aggregated.  The gap curve contains all 243 formal competitor records.
  The geometry uses exact ratios to the upper endpoint of the pinned R0.48
  root bracket.
- Renderer: reproducible Matplotlib static export.
- Palette policy: hard two-root cap using blue and gold plus neutral ink.
- Non-color encoding: marker shape, open versus filled marks, sign position,
  line style, direct labels, and ordering preserve every distinction.
- Output footprint: 178 by 142 millimetres; PDF, SVG, and 600 dpi PNG.
- Final QA: color PNG, true grayscale image, and Poppler-rendered PDF at final
  aspect ratio, followed by archive validation and hash verification.
