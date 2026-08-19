# R0.52 figure contract

- Analytical question: how does the exact local active/zero balance become a
  complete parameter-domain bound for `c>0, lambda>=0`, how strong is the
  interval contraction, and how far below one are all inactive sectors?
- Takeaway: the affine-family optimum is enclosed in a rational interval of
  width `1e-40`.  Exact Krawczyk, KKT, inactive-sector, Descartes, and
  Bernstein certificates connect the local root to a complete global upper
  bound.
- Family and variants: two-sided log-log eliminated-margin profile; logarithmic
  Krawczyk contraction lollipops; ranked logarithmic inactive-sector gaps.
- Data sufficiency: 80 exact-rational presentation samples cover distances
  `1e-1` through `1e-40` on both sides of the relevant derivative root; three
  root-box widths and exact Krawczyk image-radius renderings show strict
  inclusion; all 242 inactive records are retained.  The global theorem comes
  from the pinned machine certificate, not interpolation of the plotted
  samples.
- Renderer: reproducible Matplotlib static export.
- Palette policy: hard two-root cap using blue and gold plus neutral ink.
- Non-color encoding: two marker shapes, solid lines, a dashed proof margin,
  filled diamonds, direct labels, ordering, and logarithmic position preserve
  distinctions in grayscale.
- Output footprint: 178 by 112 millimetres; PDF, SVG, and 600 dpi PNG.
- Final QA: color PNG, true grayscale conversion, and Poppler-rendered PDF at
  final size, followed by independent data and archive validation.
