# R0.64 certificate

This directory archives the exact audit for the zero-time lifted-transfer
cycle in R0.64.

- Source commit: `245e53c18100ac05b4143571d1160d4bf6339c20`
- Command:

  `python3 research/quartic_supercritical_cycle_audit.py --output research/certificates/r064/supercritical-cycle-audit.json --max-direct-level 10`

- Arithmetic: integer and rational arithmetic for the transfer, ranks,
  image restriction, characteristic polynomial, convolution regressions,
  recurrence, and polynomial gcd. Floating-point roots are display-only.
- Randomness: none.
- Boundary: this certificate rules out a factor-two common pointwise norm
  for the zero-time full state space. It does not prove or disprove the
  heat-integrated quartic estimate.

`SHA256SUMS` hashes the machine-readable certificate. The README is excluded
so that explanatory edits do not change the mathematical payload hash.

