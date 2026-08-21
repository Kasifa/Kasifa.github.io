# R0.69M criterion-comparison certificate

This archive locks the Morrey comparison, high-frequency functional witness,
and lower-exponent near-field audit from
`research/criterion_comparison_pressure_budget_note.md` to source commit
`dd6411d1386328a3b873c410dfe5d52e89596591`.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069m/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python \
      research/criterion_comparison_pressure_budget_audit.py \
      --source-commit dd6411d1386328a3b873c410dfe5d52e89596591 \
      --output \
      research/certificates/r069m/criterion-comparison-pressure-budget.json

The certificate contains 14 checks, all passed. It verifies the exact
geometric-series constant

    B_infinity <= M_2 / 120,

the unbounded single-shell reverse ratio `2^(4k-1)`, and the high-frequency
amplitude exponents for `a_N=N^(-1/2)`: velocity `-1/2`, kinetic Morrey `-1`,
near `L2` source `+1`, and absolute annular `u q` cost `+1/2`. It also checks
that the `L3`--`L3/2` repair is scale invariant and has mixed gradient
exponent sum `5/3`, below the established critical line `2`.

The monitored run took 0.26 seconds, with 4 running samples, a maximum
observed CPU utilization of 49.2%, and a peak resident set size of
64.938 MiB. It was an exact, deterministic, CPU-only audit.

## Decision boundary

The result proves that the far-shell term is controlled by, but does not
control, the centered critical kinetic Morrey envelope. The high-frequency
family rules out a purely spatial functional bound of the near quantities by
velocity smallness. It is not a Navier--Stokes solution counterexample. The
current three-zone estimate is not a new epsilon-regularity criterion, gives
no regularity or singularity conclusion, and does not solve the Millennium
Problem.
