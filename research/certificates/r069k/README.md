# R0.69K velocity-generated shell quadrupole certificate

This archive locks the exact double-divergence and fourth-derivative audit
from `research/velocity_generated_shell_quadrupole_note.md` to source commit
`b2c7ad329eba2df516dd251a1f74af42ad153e74`.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069k/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python \
      research/velocity_generated_shell_quadrupole_audit.py \
      --source-commit b2c7ad329eba2df516dd251a1f74af42ad153e74 \
      --output \
      research/certificates/r069k/velocity-generated-shell-quadrupole.json

The certificate contains 14 checks, all passed. It verifies the two exact
fourth-derivative channels, the zero mass and dipole moments of a
double-divergence shell source, the second-moment identity, and the
positive-semidefinite energy tensor `diag(1,2,0)`. The resulting normalized
quadrupole is

    4*pi*Q_R = R^(-5) diag(0,6,-6),

whose pairing with `diag(1,-1,0)` is `-6/R^5`, or
`-3/(2*pi*R^5)` in the physical normalization.

The monitored run took 0.35 seconds, with 5 running samples, a maximum
observed CPU utilization of 48.7%, and a peak resident set size of
65.781 MiB. It was an exact, deterministic, CPU-only audit.

## Decision boundary

The result proves a shell-separation gain for the velocity-generated pressure
source, but the bound is still Navier--Stokes scaling-consistent and the
leading coefficient can be nonzero. The near shells and cutoff-transition
region remain uncontrolled. It gives no regularity or singularity conclusion
and does not solve the Millennium Problem.
