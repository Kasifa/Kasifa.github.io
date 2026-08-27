# R0.72N formal figure package

This source package builds the 2 x 2 journal figure for the dissipative
one-carrier theorem in `research/r072n_report-source.md`.

The plotted finite data are read only from
`research/certificates/r072n/producer-dissipative.csv` and
`research/certificates/r072n/independent-dissipative.csv`. The producer uses
the angular FFT exact-mixing route and the independent audit uses a finite
real chain with a fourth-order Taylor exponential mixing step. Their
agreement is checked by
`research/certificates/r072n/crosscheck.json` before the figure is built.

- Panel A compares the finite maximum modal moment with the rigorous barrier
  `max(1, (2 sigma)^(2/3))`.
- Panel B shows the finite scaled critical-log action and the normalized
  action-poor proxy.
- Panel C shows the finite normalized scalar proxy `T_proxy/V_proxy` against
  the exact algebraic ceiling one.
- Panel D shows the two finite cubic normalizations. The project corollary
  derived from Coble–He Theorem 1.2 controls the square-root normalization;
  the apparently logarithmic normalization is diagnostic only.

Every finite proxy uses the audit normalization
`mu=a=1`, `x_proxy=sigma^2 A_sigma`, `K_proxy=1+D_max`,
`U_proxy=sigma^(7/3)`, and `V_proxy=sigma^(1/3)`. Fixed geometric constants
are suppressed. These plotted proxies are not labelled as the actual physical
enstrophy contrast or actual scalar ratio.

Theorem curves are dark, marker-free lines. Finite producer and independent
curves use different colors, markers, fills, and line styles. Unknown theorem
constants are never converted into arbitrary plotted constants.

After the commands in `command.txt` are run, the archival masters are
`figure.pdf`, `figure.svg`, and a 600 dpi `figure.png`, all at
177.8 x 124.0 mm. `data.csv` records every plotted datum and its source
pointer. Public copies under `public/assets/r072n/` must be byte-identical to
the masters.

`manifest.json`, `SHA256SUMS`, `validation.json`, and the three QA surfaces
complete the formal archive only after explicit visual inspection and a clean
two-commit certificate seal.
