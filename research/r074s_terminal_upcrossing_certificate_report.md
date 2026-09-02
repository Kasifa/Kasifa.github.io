# R0.74S terminal-upcrossing certificate report

## Result

**PASS** — 5/5 exact rational checks, 1/1 finite balance fixtures, and 19/19 structural checks passed.

## Exact rational ledger

| Check | Left | Right | Margin |
|---|---:|---:|---:|
| terminal_energy_floor | 1/2 | 1/2 | 0/1 |
| net_upcrossing_floor | 1/4 | 1/4 | 0/1 |
| reduction_multiplier | 4/1 | 4/1 | 0/1 |
| small_payment_order | 1/3 | 1/3 | 0/1 |
| two_quarter_reserve | 1/2 | 1/2 | 0/1 |

## Finite fixture

The JSON verifies an exact four-shell rational stopped balance,
the strict one-quarter upcrossing hypotheses, and the resulting
factor-four terminal reduction.

## Boundary

This certificate does not prove good-time selection, the local
energy identity, the inherited Q-variation or absolute-flux
bounds, or the open signed stopped-work estimate.  It checks
fractions, one exact finite fixture, tags, and claim sentinels.

**FINITE ONLY. NOT CLAY.**
