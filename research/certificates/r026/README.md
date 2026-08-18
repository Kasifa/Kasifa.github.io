# R0.26 edge-transfer certificate

This directory archives the reproducibility certificate for the R0.26
edge/one-defect reduction and three-leaf transfer audit.

The exact structural result is:

- b_N is a two-generator PMinus/CPlus edge coefficient;
- a_N is the sum of the PMinus-defect and CPlus-defect first variations of
  the PPlus/CMinus edge;
- each endpoint family satisfies an exact three-leaf transfer-plus-signed-
  remainder identity.

In sharp-longitudinal coordinates, the transfer matrices have limits

    T_a -> [[-24t, 0], [0, -24t]]
    T_b -> [[-24t, 0], [0,  16t]]

with t = 0.4958758920134925... and spectral radius
24t = 11.9010214083238....  The isolated transfer is therefore not
contractive.

The finite part evaluates the reduced recurrence at 160 and 224 MPFR bits
through N = 25, or 75 leaves.  It records endpoint polarizations, generated
gains, transfer matrices, signed remainders, the R0.25 regression, and
precision stability.

## Reproduce

Run from the repository root with gmpy2 available:

    PYTHONPATH=research python research/boundary_edge_transfer_audit.py \
      --max-parameter 25 \
      --precisions 160 224 \
      --check --pretty --progress \
      --output research/certificates/r026/boundary-edge-transfer.json

The archived JSON was generated from source commit f3dc5eb in a clean Git
worktree.  Its internal git.dirty field is false.

Verify the archive after checkout:

    cd research/certificates/r026
    shasum -a 256 -c SHA256SUMS

The N <= 25 endpoint window is finite numerical evidence.  It cannot by
itself prove or disprove an all-N O(1/N) sharp-coordinate bound and is not a
solution of the Navier-Stokes regularity problem.
