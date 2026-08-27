# Figure contract — R0.72F-1

## Analytical question

Which temporal weights survive both the selected-family scaling obstruction
and the Leray energy-payment screen? Do the producer and independent finite
solvers reproduce the critical-log normalization? How do the temporal,
coupling, and root-atom repair vertices differ?

## Supported takeaway

For the checked selected family, the power-log weight
`s^(-beta) [1 + log(1/s)]^gamma` first reaches the scaling boundary at
`beta = 1/3, gamma = 1`. This point lies below the Leray energy threshold
`beta = 1/2`. The two finite solvers give nearly identical values of
`Q_* delta^(2/3) / log(delta)` on `delta = 16,...,512`.

## Figure map

- **A — analytic feasibility screen:** hatched region for
  `1/3 < beta < 1/2, gamma >= 0`, plus the included ray
  `beta = 1/3, gamma >= 1`. The `beta = 1/2` Leray boundary is excluded.
- **B — critical-log finite normalization:** producer split-step and
  independent real-lattice BDF values of
  `Q_* delta^(2/3) / log(delta)`. A text-only plain-endpoint ratio records
  the missing logarithm without compressing the main scale.
- **C — augmented frontier:** barycentric schematic of the three exact
  vertices at fixed `a = 1/3`. The root-atom vertex is labelled
  `CHANGES LHS` because it modifies the sampled ledger rather than repairing
  the original right-hand-side charge.

## Data sufficiency

Panel B uses six shared dyadic coupling values from each certificate. The
series are finite diagnostics of a proved analytic exponent law; no
regression line supplies a claim. Panels A and C display exact analytic
boundaries and rational vertices rather than sampled trends.

## Surface and visual system

- Static Matplotlib journal figure, 178 x 94 mm.
- Vector PDF and SVG plus 600 dpi PNG.
- Near-white paper, charcoal text, one navy and one rust root, and neutrals.
- Hatched regions, open/filled markers, dashed/solid lines, distinct vertex
  shapes, and direct labels preserve meaning in grayscale.
- All visible figure text is English.

## Claim boundary

Panel A combines only two necessary screens for one selected-root
counterexample family. Panel B is deterministic finite binary64
corroboration. The figure does not establish a complete-root upper bound,
restart control, `R_Y` payment, Navier–Stokes regularity, singularity
formation, or a Millennium-problem solution.
