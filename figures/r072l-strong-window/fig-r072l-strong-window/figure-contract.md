# Figure contract

- Analytical question: how far can the common-band complete-root ledger move
  beyond its perturbative exposure scale, and why can a divergent three-mode projection
  not decide the full-lattice extreme regime?
- Takeaway: an exact local action floor closes a growing moderate
  strong-coupling window; beyond it the Galerkin warning is non-portable
  because the first omitted shell is excited at order one.
- Family: four-panel research figure with two phase/bound panels, one ordered
  finite projected-ODE comparison, and one full-lattice support schematic.
- Data sufficiency: 181 carrier scales for each analytic window boundary, 161
  normalized-coupling points for each bound component, seven deterministic
  projected-ODE cases, and one exact leakage identity.
- Static renderer: Matplotlib with deterministic NumPy/binary64 arithmetic.
- Palette policy: hard two-root cap using muted blue and ochre plus paper,
  charcoal, and gray neutrals.
- Non-color distinctions: solid/dashed/dotted lines, filled/open markers,
  direct labels, and hatching.
- Final width: 177.8 mm; final height: 124.0 mm.
- Vector masters: PDF and SVG; raster master: 600 dpi PNG.
- QA surfaces: 180 dpi final-size, grayscale, and PDF rasterization.
- Public copies: byte-identical PDF, SVG, and PNG under
  `public/assets/r072l/`.
- Panel A: the analytic upper window for \(p=1\) and \(p=R^{-1/2}\), with the
  unresolved region explicitly hatched.
- Panel B: the first-root, mixed-row, and cubic components of equation (0.8)
  versus \(q=\varepsilon/\varepsilon_{\max}\), using normalized constants.
- Panel C: finite exact-projected-ODE diagnostics for equations (6.3)--(6.6),
  explicitly separated from the full lattice.
- Panel D: support propagation under \(W_R\), the exact \(1/\sqrt2\) leakage
  ratio, and the unresolved extreme-coupling tag.
- Claim boundary: finite panels are diagnostics.  The figure does not display
  a DNS, a full-PDE counterexample, a continuation theorem, or a proof of
  general Navier--Stokes regularity.
