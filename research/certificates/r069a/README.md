# R0.69A complete target Picard-series certificate

This directory archives the source-bound assembly certificate for the full
target Fourier coefficient on the periodic invariant-shear family.  It joins
the R0.66 quartic asymptotic, the R0.67C-2 sixth-order heat projection, the
R0.68B-2h eighth-order heat projection, and the R0.68A all-order tail.

- Source commit: `9ca36bcadb43a5e43e84fdd779cd22959cfc6518`
- Audit source SHA-256:
  `acee1c943e9f947bfb22c670ce30825bd4484b4cc5833627398f4f3aa93b139b`
- Arithmetic: gmpy2 2.3.1 with MPFR 4.2.2 at 256-bit precision and directed
  rounding for the transcendental quadratic limit
- Formal checks: 18, all passed
- Monitored runtime: below 0.1 seconds; peak sampled resident memory 2.266 MiB
- Positive quartic correction:
  `[2.5937453534608412212e-8, 2.6140836268319572193e-8]`
- Complete normalized target limit:
  `[1.0000000259374535346, 1.0000000261408362683]`
- Sixth-order decay-rate upper bound: `0.6361427020560715961`
- Eighth-order decay-rate upper bound: `0.4046775373791999253`
- Orders-at-least-ten decay-rate upper bound: `43/64 = 0.671875`

The formal command was:

```text
python3 research/run_with_monitor.py \
  --output research/certificates/r069a/resources.csv --interval 0.1 -- \
  python3 research/full_picard_target_closure_audit.py \
  --output research/certificates/r069a/full-picard-target-closure.json \
  --source-commit 9ca36bcadb43a5e43e84fdd779cd22959cfc6518 --pretty
```

## Claim boundary

The theorem closes every Picard order for one target Fourier coefficient in
an exactly invariant parallel-shear class.  Every fixed solution in this
class is globally smooth because the system reduces to a heat equation and a
linear advection--diffusion equation.  The certificate does not control a
critical norm for arbitrary three-dimensional solutions, construct a
finite-time singularity, or prove global regularity.  It is not a solution of
the Navier--Stokes Millennium problem.
