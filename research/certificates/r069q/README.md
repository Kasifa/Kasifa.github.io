# R0.69Q vorticity-direction diffusion certificate

This archive locks the exact polar vorticity identities, affine-core
obstruction, scaling law, and short-time interior-dissipation obstruction from
`research/vorticity_direction_diffusion_obstruction_note.md` to source commit
`c5e19140c3dc79d22eb368e63dc2014681afff18`.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069q/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python research/vorticity_direction_diffusion_obstruction_audit.py \
      --source-commit c5e19140c3dc79d22eb368e63dc2014681afff18 \
      --output research/certificates/r069q/vorticity-direction-diffusion-obstruction.json

The certificate contains 18 checks, all passed.  It verifies the exact
magnitude and projected direction equations, the radial--angular split
`|grad omega|^2=|grad rho|^2+rho^2|grad xi|^2`, the compactly supported
affine-core witness with sharp positive stretching and zero interior
direction dissipation, and the `a L^2 / nu` scaling factor that prevents a
universal positive-part absorption.

The monitored run took 0.59 seconds, with 8 running samples, a maximum
observed CPU utilization of 84.6%, and a peak resident set size of
65.578 MiB.  It was an exact, deterministic, CPU-only symbolic audit.

## Decision boundary

The result closes the route in which vorticity-direction diffusion is treated
as an additional unconditional dissipative term.  It is already one
orthogonal component of enstrophy dissipation, and an affine-core
Navier--Stokes initial datum makes both the angular and full interior
dissipation vanish at time zero while positive stretching remains sharp.  The
certificate does not exclude inequalities containing cutoff flux, an initial
trace, or nonlocal magnitude--direction coupling.  It does not establish
global regularity or finite-time blow-up and does not solve the Millennium
Problem.

