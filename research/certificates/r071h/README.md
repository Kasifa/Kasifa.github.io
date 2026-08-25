# R0.71H exact-certificate bundle

This directory archives the exact 2D3C witness audit and an independent
standard-library audit of the projective-curvature identity used in R0.71H.

## Decision recorded by the bundle

1. On every connected component of `d > 0`, the unit direction satisfies the
   exact projective heat identity stated in the report.  The independent
   checker verifies forced finite-dimensional and pure Fourier-heat cases,
   both pointwise and after time integration.
2. Replacing `d` by `d + epsilon` does not preserve the unit-sphere identity.
   The corrected soft identity contains its radial defect, and the linear
   zero crossing has the exact isolated-source integral
   `3*pi/(8*sqrt(epsilon))`.
3. The exact global-smooth 2D3C family has fixed initial energy and positive
   denominator while its initial angular speed grows linearly with shell
   frequency.  This rejects only a uniform unweighted pointwise angular-speed
   bound.
4. The same family has vanishing critical weighted variation on fixed viscous
   windows, so it is not a counterexample to the desired time-integrated
   weighted-BV estimate.
5. For the fixed nonconstant cutoff `(1 + delta*cos(z))/2`, the denominator,
   Rayleigh quotient, and projective source ratio are exact finite-Fourier
   rational functions.  Their saturation records a leading
   viscous-source cancellation, not a general denominator theorem.

These statements prove no Leray-level weighted-BV estimate, continuation
criterion, singularity, priority, originality, or Millennium-problem claim.

## Files

- `result.json` — canonical sorted JSON emitted by the exact SymPy producer;
- `independent-result.json` — independent finite-dimensional, Fourier-heat,
  epsilon-defect, and scaling checker;
- `command.txt` — exact reproduction commands;
- `environment.txt` — runtime, hardware, and compute-boundary record;
- `SHA256SUMS` — hashes for the archived payloads and source dependencies;
- `build_hashes.py` — deterministic generator for `SHA256SUMS`;
- `../../r071h_exact_audit.py` — exact symbolic producer;
- `../../r071h_independent_audit.py` — independent checker;
- `../../r071h_report-source.md` — analytic report;
- `../../r071h_gap_matrix.md` — claim and obstruction matrix;
- `../../r071h_literature_audit.md` — bounded primary-source audit;
- `../../r071h_independent_audit.md` — independent mathematical audit.

## Reproduction boundary

The producer uses exact finite Fourier convolution and symbolic identities.
The independent checker uses only the Python standard library and starts from
finite-dimensional paths rather than importing the producer.  Neither
program performs DNS or time-evolves a three-dimensional PDE.  The local Mac
workstation alone was used, with one process and no GPU or DGX resource.
