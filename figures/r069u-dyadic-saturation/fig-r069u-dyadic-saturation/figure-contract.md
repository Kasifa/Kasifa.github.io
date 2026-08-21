# Figure contract — R0.69U dyadic core saturation

- Analytical question: does pushing a smooth affine cutoff to dyadic radius
  \(R\) force the core-restricted boundary carrier into a one-sign regime, and
  how do the surviving annuli approach their analytic limits?
- Supported takeaway: the exact theorem gives eventual
  `Gamma_core=1`; monitored QMC resolves the finite-radius transition and the
  two positive limiting annuli.  Pure dilation leaves the full-space ratio
  unchanged.
- Family and variants: unconnected logarithmic point observations with
  explicitly floored zeros; point-interval principal shares with analytic
  benchmarks; standardized exact-value reconstruction residuals.
- Data sufficiency: seven dyadic radii, sixteen independent scrambles and
  `2^18` pairs per radius.  No time-series or fitted-rate inference.
- Renderer and footprint: reproducible Matplotlib, 178 mm by 82 mm; PDF, SVG,
  and 600 dpi PNG.
- Palette: hard two-root cap (blue and rust) plus neutral analytic benchmark;
  markers, open fills, shading and line style duplicate the color encoding.
- Boundary: core-restricted saturation and the rational limiting sign margin
  are exact.  The plotted finite-radius values are randomized QMC, not
  interval enclosures.  The family does not prove full-space annular
  saturation, global regularity, finite-time singularity, or the Millennium
  Problem.
