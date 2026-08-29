# R0.73B figure contract

- **Analytical question.** Which low-gap parameter paths and velocity weights
  remain uniformly bounded, and how do the proved kinetic envelope and its
  sharp two-dimensional shear coefficient compare with deterministic finite
  propagators?
- **Takeaway.** Physical kinetic energy is the critical diagonal weight on
  fixed-\(\Lambda\) paths: it stays bounded as \(\mu\downarrow0\), whereas
  fixed nonzero \(c\) produces \(\mu^{-1/2}\) growth and raw \(q\) remains
  singular.  The fixed-\(\Lambda\) finite propagators converge to the explicit
  triangular limit and remain below the analytic kinetic envelope.  The
  sharper OS shear-form bound approaches the exact low-gap coefficient
  \(\rho_0(0)=1/4\).
- **Surface.** Static 178 mm by 150 mm journal double-column figure; vector
  PDF/SVG and 600-dpi PNG, followed by final-size, grayscale, and independent
  PDF previews.
- **Panel A — relationship/trend.** Log--log kinetic or raw gain versus
  \(\mu\) on \([0,0.75]\), combining the 7 broad and 7 targeted grids into
  at least 13 distinct points per series.  Show fixed \(c=1\) kinetic,
  fixed \(\Lambda=1\) kinetic, and fixed \(\Lambda=1\) raw \(q\), with
  explicit asymptotic slope references.  Every point remains labelled as a
  finite \(N=10\) diagnostic.
- **Panel B — discrete comparison.** Four paired lollipop/dot comparisons at
  \(|\Lambda|=0.25,1,4,16\): finite gain at \(\mu=10^{-8}\), exact triangular
  low-gap limit, and the analytic energy envelope.  Exact values are retained
  in the underlying data and the finite/limit distinction uses filled/open
  markers as well as colour.
- **Panel C — analytic upper-envelope trend.** The elementary
  \(\|W_x\|_\infty/2\) bound, the explicit carrier/block upper bound, and the
  exact low-gap limit for \(\rho_\mu(0)\), over at least 41 logarithmic
  \(\mu\)-points.  No computed truncation is plotted as the exact infinite
  operator norm.
- **Panel D — comparison against theory.** Observed small-gap divergence
  exponents versus the diagonal weight \(a\) for fixed \(c\) (\(p=0\)) and
  fixed \(\Lambda\) (\(p=1/2\)), overlaid on the exact block predictions
  \((a/2-p)_+\).  The four tested weights are shown as discrete audited
  points; the continuous line is explicitly the analytic block prediction.
- **Data sufficiency.** 1,960 validated main norm rows, 245 targeted
  asymptotic rows, four fixed-\(\Lambda\) triangular comparisons, and an
  analytic 61-point shear-bound grid.  Missing source hashes, failed
  validation, fewer than the contracted rows, or absent formal certificate
  lineage block sealing and publication; no synthetic replacement is
  allowed.
- **Renderer.** Deterministic local Python static renderer producing native
  vector PDF/SVG and a 600-dpi PNG.  The figure source must run one-threaded
  and write a row-level `data.csv`, `results.json`, manifest, hashes, and QA
  report.
- **Palette.** Hard two-root cap: blue `#285F8F`, gold `#A6781F`, plus neutral
  ink and grey.  Solid/dashed/dotted lines, filled/open/cross markers, direct
  labels, and panel separation provide non-colour redundancy.  The research
  blossom is locked to the top-right header and carries no data.
- **Honesty constraints.** All finite propagator points say
  `FINITE N=10`; no Galerkin tail, exact maximum transient, enhanced
  dissipation, nonlinear estimate, or Clay implication is asserted.  The
  analytic kinetic envelope is an upper bound, the triangular curve is a
  low-gap finite-matrix limit, and \(0.188106\ldots\) is an integrated
  logarithmic coefficient rather than a propagator gain.

