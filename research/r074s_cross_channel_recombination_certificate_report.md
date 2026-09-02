# R0.74S cross-channel recombination certificate report

## Result

**PASS** — 4/4 exact ledger rows, 8/8 finite checks, 58/58 structural checks, and 10/10 negative mutations passed.

## Exact ledger

| Check | Left | Right | Margin |
|---|---:|---:|---:|
| weight_drop_coefficient_recombination | 1/1 | 1/1 | 0/1 |
| singleton_genealogy_row_count | 2/1 | 2/1 | 0/1 |
| one_block_internal_edge_count | 63/1 | 63/1 | 0/1 |
| witness_matched_square_scaling | 64/1 | 64/1 | 0/1 |

## Finite checks

- Full stopped-row recombination passes 1024 exact rational configurations through five shells, including tied stops.
- The genealogy-cutoff grid passes 3276 pair comparisons and 34944 insertion comparisons on 182 rational radii.
- The three-channel event-jump identity passes 1024 stopped configurations and 2343 grouped activation epochs.
- The dissipation-corrected S.137 check passes 768 exact rational density configurations (549 with tied stops), verifying the delta-Omega partition, nonnegative insertion energy, the exact D_post split and bounds, and both E+D-Q one-sided inequalities.
- The residual Abel decomposition passes all 78 blocks in the first twelve shells.
- The exact genealogy counts pass 65536 eight-shell configurations, with tied stops included.
- The one-block scalar witness passes every N from 1 through 64; its matched square is computed from the unit positive variations, while its one-block, one-epoch, and zero-merger statistics are derived from the stopped active sets.  No PDE realization is asserted.
- The super-Gaussian epsilon exponent gap passes 2016 exact comparisons for N=2 through 64.

## Negative mutations

- Removing the outer k+1 shift is rejected.
- Reversing the weight-drop coefficient sign is rejected.
- Reversing the root completed-clock sign is rejected.
- Replacing the internal max-stop by the min-stop is rejected.
- Reversing the post-dissipation increments is rejected by a nonempty exact rational cutoff/density fixture: correct D_post is 771/88, mutated D_post is -771/88, and the mutated reconstruction differs from the directly computed W3.  The target inequality is not used as an input.
- Structural sentinels reject the wrong event-jump and residual signs.
- Structural sentinels reject reversal of the D_post upper bound.
- Structural sentinels reject promotion of W_N^sc to PDE work.
- Structural sentinels reject enlargement of the epsilon exponent gap.

## Boundary

This certificate checks finite exact algebra, sampled lifted-cutoff
monotonicity, stopped genealogy, statement integrity, and explicit
counterexamples to dangerous mutations.  The periodized cutoff
inequality and local-energy clock positivity are analytic arguments,
not machine proofs.  D_post is checked only on finite rational
density fixtures.  The saturation symbol W_N^sc is scalar, not a
Navier--Stokes velocity, pressure, work, or dissipation measure.

**FINITE ONLY. ABSTRACT NO-GO ONLY. NOT CLAY.**
