# R0.69N energy-stress-commutator certificate

This archive locks the energy-level replacement for the near pressure source,
the Hardy--BMO duality wall, and the remaining temporal exponent gap from
`research/energy_stress_commutator_note.md` to source commit
`eb80615c8efe45dd26cdbb6ecb1c6e78ab264b4e`.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069n/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python research/energy_stress_commutator_audit.py \
      --source-commit eb80615c8efe45dd26cdbb6ecb1c6e78ab264b4e \
      --output research/certificates/r069n/energy-stress-commutator.json

The certificate contains 17 checks, all passed. It verifies the exact
Holder and interpolation exponents across `4 <= q <= 6`, the dimensionless
normalizations, the `q=4` Young cost `mu sigma^3`, and the `q=6` cost
`sigma^4`. It also checks that the Hardy dual frontier has derivative-integrability
product `3`, whereas the energy dissipation point has product `2`, and that a
time spike can keep its quadratic mass fixed while its cubic mass diverges.

The monitored run took 0.24 seconds, with 3 running samples, a maximum
observed CPU utilization of 11.8%, and a peak resident set size of
63.750 MiB. It was an exact, deterministic, CPU-only audit.

## Decision boundary

The result replaces the unavailable near `L2` pressure-source norm by an exact
stress commutator controlled by localized energy, enstrophy, and an absorbable
second-derivative term. It does not close the time integral: the best endpoint
still costs `mu sigma^3`, while CKN controls only quadratic enstrophy. The time
spike is a functional exponent witness, not a Navier--Stokes solution. This
certificate gives no regularity or singularity conclusion and does not solve
the Millennium Problem.
