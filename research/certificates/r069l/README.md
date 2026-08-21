# R0.69L three-zone pressure budget certificate

This archive locks the scale-invariant near--transition--far pressure budget
from `research/three_zone_pressure_budget_note.md` to source commit
`e5bcd77e238edc7cabf49d9c96e792ef92a33aba`.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069l/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python \
      research/three_zone_pressure_budget_audit.py \
      --source-commit e5bcd77e238edc7cabf49d9c96e792ef92a33aba \
      --output \
      research/certificates/r069l/three-zone-pressure-budget.json

The certificate contains 14 checks, all passed. It verifies that every term
in the normalized pressure budget is scale invariant, that the fifth-power
dyadic weights change by a factor of `1/32`, and that successive choices of
the separation index obey the exact tail-migration identity. The optimized
coefficient retains the transition-shell floor

    sum_{m>=2} 2^(-5m) e_m,

with first-shell weight `1/1024`. The amplitude audit separately records the
cross-pressure versus local-dissipation ratio `beta^2/alpha`.

The monitored run took 0.29 seconds, with 4 running samples, a maximum
observed CPU utilization of 34.0%, and a peak resident set size of
63.750 MiB. It was an exact, deterministic, CPU-only audit.

## Decision boundary

The result proves a parameter-migration obstruction: increasing the
near/far separation makes the lumped far tail small by moving fixed shells
into the transition sum. It does not show that pressure is uncontrollable
under additional local-energy, Morrey, or geometric hypotheses. It gives no
regularity or singularity conclusion and does not solve the Millennium
Problem.
