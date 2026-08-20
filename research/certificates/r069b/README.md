# R0.69B critical transverse-smallness certificate

This directory archives the source-bound exact-arithmetic certificate for the
first transverse gate around the R0.69A periodic invariant-shear packet.  It
combines the R0.59 periodic heat--Carleson bound with the R0.66 dominant-root
enclosure and records the resulting geometric contraction rate.

- Source commit: `3342fb092b454df34255b82e142bfd796e5e522d`
- Audit source SHA-256:
  `12c2c64b2ec6d1f0c664005d875c4dbb2347a9891bbedc9c45ae18b05c306336`
- Arithmetic: gmpy2 2.3.1 with MPFR 4.2.2 at 256-bit precision and directed
  rounding
- Formal checks: 13, all passed
- Monitored runtime: below 0.1 seconds; peak sampled resident memory 2.141 MiB
- Critical-norm prefactor:
  `6+4sqrt(2) = 11.6568542494923801952067548968...`
- Certified geometric rate:
  `rho = 0.7975855452903291221747023131... < 1`
- The upper bound first falls below `1`, `1e-1`, `1e-2`, and `1e-3` at
  `r=11`, `22`, `32`, and `42`, respectively.

The formal command was:

```text
python3 research/run_with_monitor.py \
  --output research/certificates/r069b/resources.csv --interval 0.05 -- \
  python3 research/transverse_critical_smallness_audit.py \
  --output research/certificates/r069b/transverse-critical-smallness.json \
  --source-commit 3342fb092b454df34255b82e142bfd796e5e522d \
  --pretty --check
```

## Claim boundary

The certificate audits the packet-specific algebra, the directed numerical
intervals, and the threshold-crossing depths.  It treats the periodic
Koch--Tataru small-data theorem as an external analytical input and assigns no
numerical value to its universal threshold.  The result controls only total
data in a small critical ball.  It proves neither transverse instability nor
a singularity for order-one perturbations and is not a solution of the
Navier--Stokes Millennium problem.
