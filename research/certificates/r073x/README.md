# R0.73X exterior-tail formal evidence archive

This directory is the hash-bound evidence archive for the two executable
R0.73X channels that were frozen before publication:

1. the deterministic Gaussian velocity-tail scalar certificate; and
2. the finite Fourier harmonic-probe harness.

`seal_package.py` runs both canonical producers in `--check-only` mode,
requires the canonical result/report bytes to remain current, verifies that
all seven canonical evidence inputs are byte-identical to their Git blobs at
one immutable source commit, copies those bytes into this archive, and seals
the archive with `manifest.json` and `SHA256SUMS`.

The Gaussian channel certifies scalar heat-kernel domination, annular
geometry, an exact scale integral, Navier--Stokes dimensional degrees,
translated-packet concentration exponents, energy-interpolation exponents,
and lifted-tail summability.  Its independent audit passes only with the
original functional claim boundary.

The Fourier channel certifies exact finite Gaussian-rational identities for a
fixed nonnegative periodic harmonic probe.  It refutes an
amplitude-independent quadratic absorption constant in that exact probe
class.  The probe is not compactly supported, and the stored absolute-value
scale slices are converged float64 diagnostics rather than interval
certificates.

## Reproduction

From the repository root, run the commands in `command.txt`.  In an installed
copy, the default repository is inferred from this directory.  In the
external staging area used to assemble the release candidate, pass
`--repository /path/to/repository` explicitly.

The seal is deterministic.  A successful `--check-only` invocation performs
no writes.  The archive is source-commit-bound and package-hash-sealed; it is
not yet package-commit-bound until the publication owner commits these files.

No PDE time stepping, DNS, random sampling, network service, GPU, or DGX was
used.  `NOT CLAY`.
