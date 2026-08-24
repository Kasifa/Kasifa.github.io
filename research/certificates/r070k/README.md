# R0.70K exact normalized-anisotropy audit

This archive records exact symbolic regressions for the R0.70K
trace-normalized vorticity-covariance gate.

The producer checks six groups:

1. symmetry, trace normalization, and cancellation of a pure covariance
   amplitude change;
2. the constant-source shape equation and its nonnegative variance identity;
3. the axisymmetric replicator model, its exact isotropic solution, and both
   source-eigenspace endpoints;
4. sharp trace-one covariance realizability examples;
5. the scalar Burgers-vortex vorticity balance, the curl of its swirl
   velocity, and its rank-one shape geometry;
6. the exact periodic two-mode Navier--Stokes shear, including both signs of
   normalized viscous anisotropy production.

The exact values include

- `dB/dt=(dev(F)-B*tr(F))/E` for `F=dQ/dt`;
- `dq/dt=2*(tr(R*Sigma**2)-q**2)` for a frozen STF source;
- `q(t)=(exp(3*t)-1)/(exp(3*t)+2)` from isotropic covariance under the
  axisymmetric source;
- the sharp realizability value `tr(B**2)=2/3` for a rank-one shape;
- Burgers-vortex correlation `q=gamma>0` with stationary maximal shape;
- diffusion-only witnesses `+144*nu/125` and `-144*nu/125` in an exact
  periodic Navier--Stokes solution.

The finite symbolic checks do not computer-prove positivity for every
positive-semidefinite covariance, the full filtered tensor identity obtained
by integration by parts, the complete three-dimensional Burgers
velocity-pressure solution, small-data Navier--Stokes theory, a weak-solution
endpoint passage, or completeness of the literature search.

## Reproduction

From the repository root, run the exact command in `command.txt`. The expected
interpreter, SymPy version, platform, and Git baseline are recorded in
`environment.txt`. Standard output must match `result.json` exactly.

## Payloads

- `result.json`: deterministic exact symbolic output and claim boundaries;
- `command.txt`: reproduction command;
- `environment.txt`: platform, interpreter, arithmetic, and baseline;
- `../../r070k_anisotropy_evolution_audit.py`: exact producer;
- `../../r070k_report-source.md`: canonical mathematical report;
- `../../r070k_literature_audit.md`: bounded primary-source audit;
- `../../r070k_independent_audit.md`: independent internal derivation check;
- `README.md`: archive scope and reproduction boundary.

`SHA256SUMS` seals the eight payloads above after the report bundle is frozen.
