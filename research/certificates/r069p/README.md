# R0.69P vortex-stretching sign certificate

This archive locks the sharp pointwise stretching bounds, exact local
solenoidal realization, Betchov reduction, and energy-only sextic obstruction
from `research/vorticity_stretching_sign_structure_note.md` to source commit
`1471752c76624699c0f5a40d523bdc484a49cbd3`.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069p/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python research/vorticity_stretching_sign_structure_audit.py \
      --source-commit 1471752c76624699c0f5a40d523bdc484a49cbd3 \
      --output research/certificates/r069p/vorticity-stretching-sign-structure.json

The certificate contains 20 checks, all passed. It verifies the sharp
`sqrt(2/3)` pointwise stretching constant and both signs, the quadratic vector
potential that realizes every trace-free affine velocity-gradient jet inside
a compactly supported divergence-free field, the pointwise Betchov
decomposition, the sharp middle-eigenvalue bounds, and the exact sextic Young
remainder.

The monitored run took 0.42 seconds, with 6 running samples, a maximum
observed CPU utilization of 52.6%, and a peak resident set size of
65.750 MiB. It was an exact, deterministic, CPU-only symbolic audit.

## Decision boundary

The result closes the route in which incompressibility or smoothness alone is
expected to force favorable pointwise stretching geometry. Betchov's global
identity identifies the positive middle strain eigenvalue as the signed
quantity, but energy-level information still produces a sextic remainder.
The certificate does not establish an unconditional spacetime depletion
estimate, a regularity theorem, or a singularity theorem, and it does not
solve the Millennium Problem.
