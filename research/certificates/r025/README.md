# R0.25 boundary-face polarization-channel certificate

This directory archives the reproducibility certificate for the R0.25 boundary-face computation.

The calculation studies the sharp boundary labels a_N and b_N for N = 2, 3, 4, 5. Each normalized state is decomposed as

    U / M(U) = sigma S + lambda L.

The exact estimate proved in R0.25 is

    G_N <= 44 N^2 |sigma_A sigma_B|
           + 7 N (|sigma_A lambda_B| + |lambda_A sigma_B|)
           + |lambda_A lambda_B|,

for N >= 2. The certificate records the high-precision recurrence evaluation, polarization coefficients, channel decomposition, root-split diagnostics, and the 160-bit versus 224-bit precision comparison.

## Reproduce

Run from the repository root with gmpy2 available:

    PYTHONPATH=research python research/boundary_face_channel_audit.py \
      --check --pretty --progress \
      --output research/certificates/r025/boundary-face-channels.json

The archived JSON was generated from source commit 25108b9 in a clean Git worktree. Its internal git.dirty field is false.

Verify the archive after checkout:

    cd research/certificates/r025
    shasum -a 256 -c SHA256SUMS

This finite computation is evidence for the proposed all-N polarization-decay mechanism. It is not a proof of that decay and is not a solution of the Navier-Stokes regularity problem.
