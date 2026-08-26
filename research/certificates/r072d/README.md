# R0.72D certificates

This directory archives two independent machine audits for the shifted
Rudin--Shapiro dynamical root-ledger family.

- `result.json` is produced by `research/r072d_exact_audit.py` with
  90-decimal `mpmath` arithmetic and exact integer identities. It reconstructs
  the Rudin--Shapiro recursion, the shifted moment
  `Ks=M(2M-1)(7M-1)/6`, the row-aligned launch identity, the Abel heat
  envelope, and the dimensionless launch-root and rotational-charge scales.
- `independent-result.json` is produced by
  `research/r072d_independent_audit.py`. It imports neither the producer nor
  its result. It generates signs from overlapping binary `11` pairs, samples
  the multiplier by FFT, integrates its observed heat norms in scaled time,
  and solves symmetric finite Fourier ODE truncations with DOP853.
- `producer-progress.ndjson` and `independent-progress.ndjson` preserve stage
  and per-ODE-case updates. The corresponding monitor logs preserve the
  console stream.
- `producer-resource.ndjson` and `independent-resource.ndjson` record elapsed
  time, CPU time, resident-set usage, and logical CPU count.
- `config.json`, `command.txt`, `seed.txt`, and `environment.txt` record the
  declared configuration and runtime. `SHA256SUMS` is generated after the
  package is complete.

The independent ODE test evolves the row-aligned vector `G` and the target
basis vector separately. At `tau=M^-3` it sets

```text
zeta = -P0 U(tau)G / P0 U(tau)e0,
```

so the combined finite state has an exact binary64 target root at the chosen
interior time. The audit checks the predicted `|zeta|=Theta(M^-1/2)` scale,
`|h(tau)|/h0 -> 1`, the root-slope identity, contractivity, normalized atom
scaling, and stability under radius factors 4, 6, and 8.

The analytic report is primary. The high-precision calculations are not
directed-rounding interval proofs. The FFT maxima are sampled, and the ODEs
are finite truncations. The normalized atom and full-charge entries compare
the explicit model factors; they do not supply rigorous values for unknown
Navier--Stokes comparison constants. Nothing in this package proves
three-dimensional Navier--Stokes regularity or singularity.
