# R0.69S signed output-shell certificate

This archive locks the exact six-mode, single-dyadic-shell stretching witness
from 'research/signed_output_shell_no_cancellation_note.md' to source commit
'3bbbb660949181380420ebba9f103e901e560043'.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069s/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python research/signed_output_shell_no_cancellation_audit.py \
      --source-commit 3bbbb660949181380420ebba9f103e901e560043 \
      --output research/certificates/r069s/signed-output-shell-no-cancellation.json

The certificate contains 17 checks, all passed. It verifies triad closure,
divergence freedom, reality through conjugate modes, one-shell support, exact
modal transfers (2,-3,1), zero kinetic-energy transfer, positive enstrophy
transfer, direct vortex stretching equal to two, and shell-cancellation ratio
equal to one.

The monitored run took 0.26 seconds, with 4 running samples, a maximum observed
CPU utilization of 43.8%, and a peak resident set size of 64.812 MiB. It was
an exact, deterministic, CPU-only symbolic audit.

## Decision boundary

The result excludes a universal signed depletion factor below one arising
solely from sharp dyadic output-shell grouping. It does not exclude
smooth-projector commutators, cancellation within the active shell,
physical-space annular cancellation, or dynamical decorrelation. It proves
neither global regularity nor finite-time blow-up and does not solve the
Millennium Problem.
