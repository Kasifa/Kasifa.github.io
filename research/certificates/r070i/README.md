# R0.70I exact temporal-Hardy and scaling audit

This archive records exact finite symbolic regressions for the R0.70I
temporal-Hardy obstruction lane.

The producer checks:

- finite constant-ratio kernels `G_K(s)` for `rho=1/2,1/3,2/5`, including
  the interior overlap increments `k=0,...,K-1`, every unique discarded
  slab, and the separate fine Abel endpoint
  `r_K^(-1)1_{s<r_K^2}`;
- the finite bound
  `G_K(s) <= C_rho*min(r_K^(-1),s^(-1/2))` with
  `C_rho=1/(1-rho)`;
- the weighted exponent `1/2+2*alpha` and the exact threshold
  `alpha=1/4`;
- heat/Stokes scaling of velocity energy, integrated enstrophy, zeroth and
  first moments, critical moments, and the core target;
- Navier--Stokes invariant scaling
  `T~r^(-1)a^4`, `E,D~r*a^2`, and
  `r_0^(-3)E^2~r^(-1)a^4`;
- the general homogeneous constraint `gamma=p+q+1` for a candidate
  `r_0^(-gamma)E^pD^q`;
- the frozen-low/annular same-index exponent
  `r_k^(-1)*r_k^(3/2)*r_k^(-1)=r_k^(-1/2)`, the frozen low--low
  outer ledger `r_0^(5/2-5+1)=r_0^(-3/2)`, and the vanishing contraction
  of an isotropic moment tensor with a trace-free strain.

The frozen-low machine ledger covers only the same-index exponent with
`L_0=P_(<=c/r_0)omega`. The report separately proves the complete
lower-triangular frozen-low array by the analytic geometric convolution
`r_k/r_j <= rho_+^(k-j)`. The producer does not computer-prove that Young
inequality step. It retains the physical cutoff, and time-window indicators
only decrease its absolute estimate. It does not cover the moving-low sum
between the outer and current frequency scales.

The kernel cases are finite exact regressions for `K=0,...,8`; the analytic
geometric-series proof for arbitrary `K` remains a mathematical proof, not a
consequence of the loop. The scalar `s^(-alpha)` profile is a norm test and is
not realized here as a Navier--Stokes trajectory.

The fixed-energy amplitude `A=r^(-3/2)` belongs to the linear heat/Stokes
equation. The actual Navier--Stokes scaling audit uses `A=a/r`, outer radius
`r_0=r`, and terminal time `t_0=r^2`. It is therefore an initial-boundary
scaling ledger. All family members start at `t=0`, but they have different
rescaled initial data and are different solutions, with `t_0=r^2` tending to
zero. The ledger does not construct concentration along one solution history
at a fixed positive terminal time uniformly separated from the initial face.
No singularity, regularity, theorem-nonexistence, or Millennium claim is made.

## Reproduction

From the repository root, run the exact command in `command.txt`. The expected
interpreter and arithmetic environment are recorded in `environment.txt`.

## Payloads

- `result.json`: deterministic exact symbolic output and claim boundaries;
- `command.txt`: reproduction command;
- `environment.txt`: platform, interpreter, SymPy, and baseline information.
- `../../r070i_temporal_hardy_audit.py`: exact producer;
- `../../r070i_report-source.md`: canonical mathematical report;
- `../../r070i_literature_audit.md`: bounded primary-source audit.

`SHA256SUMS` seals the seven payloads above after the report bundle is
frozen.
