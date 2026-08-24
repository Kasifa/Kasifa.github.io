# R0.70J exact deviatoric-helical audit

This archive records exact symbolic regressions for the R0.70J deviatoric
diagonal correlation gate.

The producer checks five groups:

1. the identity
   `S:dev(w tensor w)=w^T S w` for a general symmetric trace-free matrix;
2. both helical eigenvectors, their Hermitian projectors, spin-two terms, and
   the full real conjugate-pair formula;
3. the pointwise-positive Beltrami witness for both helicities, including its
   zero self-stretching against the wave's own strain;
4. the signed sphere, sphere positive part, great-circle, same-shell two-mode,
   and three-axis second-order-isotropy ledgers;
5. the harmonic quadratic, compact-core homotopy identities, one exact
   periodic NSE Beltrami solution, and the degree-zero critical scale ledger.

The exact values include

- `K_S(xi)=-xi^T*S*xi` for the phase-averaged pure-helicity symbol;
- pointwise coupling `1` for
  `S0=diag(1/2,1/2,-1)` and either helicity;
- complete-sphere signed mean `0` but positive-part mean `sqrt(3)/9`;
- same-shell two-direction pairing `73/50`;
- for common amplitude `a`, source square norm scale
  `a^2*r/Lambda^4`, core dual square norm scale `a^4/r`, and normalized
  spacetime pairing `a^3/Lambda^2`;
- at `a=r^(-1/2)`, the exact scales
  `Lambda^(-4)`, `r^(-3)`, and `r^(-3/2)/Lambda^2`, with unit energy and
  unit window dissipation scales.

The finite exact checks do not computer-prove smooth cutoff support buffers,
strict annular Littlewood--Paley localization of a compact packet, the
pressure-orbit convexity argument, literature completeness, small-data
theory, nonlinear persistence at one fixed positive terminal time, or any
regularity or singularity theorem.

## Reproduction

From the repository root, run the exact command in `command.txt`. The expected
interpreter, SymPy version, and baseline are recorded in `environment.txt`.
The command writes the deterministic JSON payload to standard output; it must
match `result.json` exactly.

## Payloads

- `result.json`: deterministic exact symbolic output and claim boundaries;
- `command.txt`: reproduction command;
- `environment.txt`: platform, interpreter, arithmetic, and baseline;
- `../../r070j_deviatoric_helical_audit.py`: exact producer;
- `../../r070j_report-source.md`: canonical mathematical report;
- `../../r070j_literature_audit.md`: bounded primary-source audit;
- `README.md`: archive scope and reproduction boundary.

`SHA256SUMS` seals the seven payloads above after the report bundle is frozen.
