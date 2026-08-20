# R0.69D conditional nonlinear-decoupling certificate

This directory archives the source-locked symbolic certificate for the exact
nonlinear comparison between a resolvent-stable reference solution and the
solution obtained by adding the R0.69A deep packet.

- Source commit: `d6e085404bb78e23ec2ea14d541e2841a01ed7bb`
- Audit source SHA-256:
  `bb658514e69dc3cde4bdeaf81fdf596be1cb6e0dfed7423ae287ff07cf82e171`
- Certificate SHA-256:
  `1bb0e9af3f9cb81da5ece68fc50a2b7d4782bc8f66187bb30693616d5f755932`
- Arithmetic: SymPy 1.14.0 exact symbolic algebra; gmpy2 2.3.1 provenance
- Formal checks: 18, all passed
- Monitored runtime: 0.226 seconds; peak sampled resident memory 63.953 MiB
- Nonlinear parameter: `chi_r=4 C_B M_T^2 C_H delta_r`
- Exact branch radius:
  `R_-=(1-sqrt(1-chi_r))/(2 C_B M_T)`
- Certified envelope: `R_- <= 2 M_T C_H C_0 rho^r`

The formal command was:

```text
python3 research/run_with_monitor.py \
  --output research/certificates/r069d/resources.csv --interval 0.05 -- \
  python3 research/transverse_nonlinear_decoupling_audit.py \
  --output research/certificates/r069d/transverse-nonlinear-decoupling.json \
  --source-commit d6e085404bb78e23ec2ea14d541e2841a01ed7bb \
  --pretty --check
```

## Claim boundary

The certificate checks the scalar majorant, quadratic-root identities,
self-map equality, strict contraction factor, and inheritance of the
R0.69B geometric packet rate.  The Koch--Tataru heat and bilinear estimates
and bounded invertibility of the reference linearization are analytical
inputs.  The result is unique only in the explicit local ball around the
reference path.  It does not prove that every finite critical path norm
implies the resolvent hypothesis, does not continue an arbitrary large
solution through a possible singular time, and is not a solution of the
Navier--Stokes Millennium problem.

