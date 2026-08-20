# R0.69G signed-vorticity-kernel robustness certificate

This archive locks the source commit and the symbolic, Fourier, and spherical
checks for the direction-only magnitude-coupling barrier in
`research/signed_vorticity_kernel_robustness_note.md`.

## Reproduce

From the repository root, with the pinned research virtual environment:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069g/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python \
      research/signed_vorticity_kernel_robustness_audit.py \
      --source-commit ae328c0b02905bf48d12468ea11bbd27e3664959 \
      --output \
      research/certificates/r069g/signed-vorticity-kernel-robustness.json \
      --pretty --check

The certificate contains 14 checks, all passed.  The symbolic checks verify
the Levi-Civita contraction and the two-lobe angular kernel.  The Fourier
checks compare the periodic Green-Hessian multiplier with the direct strain
on every mode of a ten-mode real divergence-free butterfly and reproduce its
exact nonzero stretching average.  The spherical quadrature checks the
uniform cancellation, the absolute angular mean, four magnitude biases, and
the finite-selector duality identity.

The monitored reproduction completed in about 0.3 seconds and reached a peak
resident set of about 76.4 MiB.  The calculation is CPU-only because it is a
small exact and deterministic audit; a DGX run would increase overhead.

## Decision boundary

The certificate proves a robustness identity for arbitrary nonnegative
magnitude weights and validates the periodic multiplier on a finite Fourier
field.  It eliminates only direction-only signed annular estimates that seek
a uniform cancellation gain while treating magnitude as an arbitrary
positive weight.  It does not show that every selector is a divergence-free
vorticity, validate the cited 2026 preprints, prove Navier-Stokes regularity,
or solve the Millennium problem.
