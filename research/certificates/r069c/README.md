# R0.69C transverse sideband and linearized-stability certificate

This directory archives the source-locked symbolic certificate for the first
genuinely three-dimensional Fourier sideband of the R0.69A periodic packet
and for the complete critical-space linearized propagator estimate.

- Source commit: `55b89d43ca854e33c10e63f64974fc479f56ceaa`
- Audit source SHA-256:
  `3a1acb517642f595f0db40038ae6d1c68cc3b00d20210d326ac203f40ead1135`
- Arithmetic: SymPy 1.14.0 exact symbolic algebra; gmpy2 2.3.1 provenance
- Formal checks: 18, all passed
- Monitored runtime: 0.274 seconds; peak sampled resident memory 65.031 MiB
- Sideband: `p=(R,0,0)`, `q=(-R,m,s)`, `k=(0,m,s)`, with `s != 0`
- Exact heat denominator: `2R^2`
- Sharp symbol bound: `||T_{R,m,s}|| <= sqrt(m^2+s^2)`
- Full propagator difference: `O(rho^r)` in the periodic Koch--Tataru
  data-to-path operator norm, with the R0.69B certified `rho < 0.797586`

The formal command was:

```text
python3 research/run_with_monitor.py \
  --output research/certificates/r069c/resources.csv --interval 0.05 -- \
  python3 research/transverse_sideband_linear_audit.py \
  --output research/certificates/r069c/transverse-sideband-linear.json \
  --source-commit 55b89d43ca854e33c10e63f64974fc479f56ceaa \
  --pretty --check
```

## Claim boundary

The certificate checks the exact Fourier--Leray geometry, the non-normal
two-polarization matrix, its positive-semidefinite contraction identity, the
heat denominator, and the Neumann-series reduction.  The periodic
Koch--Tataru heat and bilinear bounds remain external analytical inputs, with
their universal constants left symbolic.  The result omits the perturbation
self-interaction, proves no global theorem for order-one transverse data, and
is not a solution of the Navier--Stokes Millennium problem.
