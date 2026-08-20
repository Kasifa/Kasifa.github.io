# R0.69E positive-time critical-resolvent certificate

This archive locks the source commit and the formal/numerical checks for the
finite-interval Volterra gluing theorem in
research/critical_resolvent_restart_note.md.

## Reproduce

From the repository root, with the pinned R0.68B virtual environment:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069e/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python research/critical_resolvent_restart_audit.py \
      --source-commit 2d49cf91a29c2a2ecd19edbe97356a924b958917 \
      --output research/certificates/r069e/critical-resolvent-restart.json \
      --pretty --check

The certificate contains 18 checks, all passed.  The exact two-block inverse,
Gamma half-integral, and equal-slab telescoping identity are checked
symbolically.  Sixteen finite slab systems use 80-digit arithmetic to compare
direct matrix inversion with forward substitution through 32 time slabs.

## Boundary

The certificate uses the periodic Koch--Tataru bilinear estimate and the
periodic Oseen-gradient kernel estimate as analytical inputs.  It does not
assign sharp numerical values to those constants, control a reference path at
a hypothetical singular time, continue a solution through such a time, or
solve the Navier--Stokes Millennium problem.
