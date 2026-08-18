# R0.24 minimal-face sharpness certificate

This directory archives the exact boundary-face recurrence audit for the
R0.22 sharp-label family at parameters \(N=2\) and \(N=3\).

## Contents

- `boundary-face-sharpness.json`: exact quadratic-field coordinates, graded
  support counts through time order sixteen, the exact R0.23 regression,
  sharpness comparisons, and finite-shell convergence checks.
- `SHA256SUMS`: checksums for this README and the JSON certificate.

## Main certified statements

At the rational center of the R0.20 root certificate:

1. At leaf count \(L\), the extremal face \(m_2=-L\) is closed under the
   graded recurrence: equality forces every input leaf and every child of a
   root split to attain the same lower bound.
2. The face restriction reduces the ambient support capacity from
   \((L+1)^3\) to \((L+1)^2\).  At time order sixteen it contains 320
   nonzero modes out of 324 possible face labels.
3. The restricted recurrence reproduces the three archived R0.23 \(N=2\)
   coefficients exactly.
4. For \(N=3\), the generated input coefficients have exactly nonzero sharp
   projections and the symmetrized root interaction is exactly nonzero.
5. The generated symmetrized gain is \(0.3615555663\ldots\), while the sharp
   benchmark is \(184.7738320\ldots\); their ratio is
   \(0.0019567466\ldots\).
6. The selected root split contributes about \(7.72\times10^{-7}\) of the
   complete order-sixteen output mode norm.

The comparison from \(N=2\) to \(N=3\) is evidence for generated-direction
suppression, not an all-\(N\) estimate.  The certificate does not establish
root-box uniformity, one-radius analytic closure, or a Navier--Stokes
regularity or singularity result.

## Reproduction

The JSON was generated from clean source commit `22bfd58` with Python 3.12,
`gmpy2` 2.3.1, and GMP 6.3.0:

    PYTHONPATH=research python3.12 \
      research/boundary_face_sharpness_audit.py \
      --check --pretty --progress \
      --checkpoint-dir tmp/r024-checkpoints \
      --output research/certificates/r024/boundary-face-sharpness.json

Verify the archive with:

    cd research/certificates/r024
    shasum -a 256 -c SHA256SUMS
