# R0.51 figure contract

- Analytical question: how does the affine factor `1+lambda|s|` create a
  strict threshold improvement beyond R0.50, which sector stops further
  movement in `lambda`, and how large are all remaining exact gaps?
- Takeaway: the simple rational choice `c=0.79756`, `lambda=0.7653` gives the
  exact threshold interval
  `0.382624471846022<r_*<0.382624471846023`.  It improves the R0.50 radius by
  more than 12.174 ppm.  The active `s=162,j=81` column remains limiting, but
  the `s=0` column is now the nearest competitor and would take over after a
  small increase in `lambda`.
- Family and variants: focused constraint-switch line; logarithmic incremental
  gain lollipops; ranked logarithmic competitor-gap curve.
- Data sufficiency: 126 exact-rational presentation samples resolve one sign
  change of the conservative active-minus-zero root-box gap on
  `0.76520<=lambda<=0.76545`.  Three exact inter-stage lower gain factors and
  every one of the 243 formal competitor gaps are retained.  The samples
  illustrate the constraint switch; the root, sharpness, restart, and
  all-order dominance claims come from the pinned GMP certificate.
- Renderer: reproducible Matplotlib static export.
- Palette policy: hard two-root cap using blue and gold plus neutral ink.
- Non-color encoding: solid line, zero reference, open and filled markers,
  direct labels, ordering, and logarithmic position preserve distinctions in
  grayscale.
- Output footprint: 178 by 112 millimetres; PDF, SVG, and 600 dpi PNG.
- Final QA: color PNG, true grayscale conversion, and Poppler-rendered PDF at
  final size, followed by independent data and archive validation.
