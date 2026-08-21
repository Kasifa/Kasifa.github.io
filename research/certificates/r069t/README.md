# R0.69T physical-space annular increment certificate

This archive locks the exact direction-free, pair-symmetrized annular
vortex-stretching identities from
'research/physical_space_annular_increment_note.md' to source commit
'bf437d5ec74532006c19fa09a8b486129503718d'.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069t/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python research/physical_space_annular_increment_audit.py \
      --source-commit bf437d5ec74532006c19fa09a8b486129503718d \
      --output research/certificates/r069t/physical-space-annular-increment.json

The certificate contains 12 checks, all passed. It verifies exact removal of
the vorticity-direction denominators, the two-increment identity created by
pair exchange, vanishing of constant-vorticity interior pairs, cubic amplitude
homogeneity, the telescoping finite annular window, explicit near and far
boundary remainders, Navier--Stokes scaling exponent three, and the direction
of the dyadic physical-shell shift.

The monitored run took 0.272000 seconds, with 4 running samples, a maximum
observed CPU utilization of 29.1%, and a peak resident set size of 64.859 MiB.
It was an exact, deterministic, CPU-only symbolic audit.

## Decision boundary

The result proves an exact signed physical-space annular reconstruction and
shows that positive affine-core stretching is carried entirely by pairs that
cross the cutoff boundary. It does not prove a universal annular depletion
factor or a new regularity criterion. It proves neither global regularity nor
finite-time blow-up and does not solve the Millennium Problem.
