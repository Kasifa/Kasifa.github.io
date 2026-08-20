# R0.60 invariant-shear Picard certificate

This directory archives the deterministic exact regression for
research/invariant_shear_picard_note.md.

## Source lock

- theorem and audit source:
  db3e7eb9071f67c041a96863f9afc43bbca50aec
- formal command:

      python3 research/run_with_monitor.py --output research/certificates/r060/resources.csv --interval 0.10 -- python3 research/invariant_shear_picard_audit.py --maximum-level 12 --maximum-exhaustive-level 3 --maximum-order 11 --maximum-energy-level 3 --source-commit db3e7eb9071f67c041a96863f9afc43bbca50aec --progress --progress-log research/certificates/r060/progress.ndjson --check --pretty --output research/certificates/r060/invariant-shear-picard.json

## Result

- 24 of 24 declared checks passed.
- 169 dyadic parameter pairs were covered by the all-index interval formulas.
- Those formulas cover 67,092,481 carrier positions without materializing the
  largest arrays.
- The finite support regression checked 32,771,750 exact state transitions
  through Picard order eleven.
- The fourth-order energy regression checked 323,216 exact Gaussian-integer
  convolution pairs.
- Scientific audit wall time: 0.737199 seconds.
- Monitor wall time: 0.795783 seconds over 8 samples.
- Peak process-tree CPU: 90.7 percent.
- Peak process-tree resident memory: 18.891 MiB.
- No GPU, random input, or floating-point mathematical decision was used.

## Interpretation

The analytic proof is the invariant-subspace calculation and the all-index
carrier-interval argument in the note.  The certificate is an implementation
regression, not the source of the theorem.

The result proves that the R0.59 packet evolves inside a globally regular
plane-parallel shear class, that its cubic Picard term cannot return to the
target low-frequency plane, and that the odd terms through order nine share
that exclusion.  It does not bound the quartic term or the complete nonlinear
remainder, and it does not prove arbitrary-data three-dimensional
Navier--Stokes regularity.
