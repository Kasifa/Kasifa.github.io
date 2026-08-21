# Figure contract — R0.69T affine-core physical annuli

- Analytical question: which physical separation scales carry the positive
  vortex stretching inside the compact affine core, and does the annular sum
  reconstruct its exact boundary-carrier value?
- Supported takeaway: at 67,108,864 scrambled-Sobol pairs, the production is
  concentrated in the overlapping annuli `j=-2` and `j=-1`; the only resolved
  negative mean is the outer `j=1` annulus, and the exploratory signed ratio is
  `0.996478`. The refinement estimates remain compatible with the exact core
  benchmark at the declared scramble-error scale.
- Family and variants: signed categorical bars with uncertainty; small-tail
  interval bars; refinement dot-and-interval benchmark.
- Data sufficiency: ten annular rows, three refinement resolutions, sixteen
  independent scrambles at each nested resolution; no time-series inference.
- Renderer and footprint: reproducible Matplotlib, 178 mm by 82 mm; PDF, SVG,
  and 600 dpi PNG.
- Palette: hard two-root cap (blue positive, rust negative) plus neutral exact
  benchmark; sign is also encoded by fill, hatching, zero line, and labels.
- Boundary: randomized quasi-Monte Carlo evidence for one explicit cutoff and
  the core-restricted boundary carrier. It is not an interval proof, a global
  annular ratio, a universal depletion theorem, or a regularity result.
