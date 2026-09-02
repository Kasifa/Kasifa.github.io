# R0.74S one-sided ball-clock certificate report

## Result

**PASS** — 5/5 exact ledger rows, 7/7 finite checks, 55/55 structural checks, and 4/4 negative mutations passed.

## Exact ledger

| Check | Left | Right | Margin |
|---|---:|---:|---:|
| frozen_geometric_tail_constant | 35/3 | 35/3 | 0/1 |
| weight_drop_decomposition | 3/35 | 3/35 | 0/1 |
| central_ball_energy_factor | 32/1 | 32/1 | 0/1 |
| ball_tower_subtraction | 1/1 | 1/1 | 0/1 |
| scalar_clock_completion | 1/1 | 1/1 | 0/1 |

## Finite checks

- The one-sided cutoff identities pass on 312 exact rational value samples and 228 transition-derivative samples.
- The support-packing proxy passes on 79 radii; its sampled maximum ratio is 73/3.
- Root, outer, and internal activation pass 82432 Boolean comparisons across 1024 stopped configurations, including tied stops.
- Exact affine fixtures reproduce all three signs and endpoint orientations in S.97--S.99.
- The finite Abel identity passes at every terminal index from 2 through 8.
- A separate tower-compatible Abel fixture checks every residual insertion and terminal boundary term.
- The abstract tower gives terminal debt equal to the square of the matched square function for every N from 1 through 24, while checking S.90--S.92 at five rational times.

## Negative sentinels

- Flipping the terminal Abel sign is rejected.
- Flipping the block-root clock sign is rejected.
- Independent numerical fixtures also reject both wrong signs.

## Boundary

This certificate checks only finite algebra, sampled cutoff bookkeeping,
stopped-family combinatorics, and statement integrity.  It does not
machine-prove the suitable local-energy calculation, the infinite
support estimate, or a PDE realization of the abstract clock witness.
It proves no unconditional stopped-work estimate or regularity theorem.

**FINITE ONLY. ABSTRACT NO-GO ONLY. NOT CLAY.**
