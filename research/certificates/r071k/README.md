# R0.71K exact-certificate bundle

This directory archives the exact and independent audits for the fixed
matched-cell release.

## Decision recorded by the bundle

1. A single smooth translated scale-covariant partition is fixed before the
   R0.71J data.  On the selected parent \(\kappa=4K\), it has \(K^3\)
   matched cells.
2. Exact translation symmetry gives
   `B_Q=B_parent/K^3`, `d_Q=D_local/K^3`, and
   `sum q_Q=(B_parent^+)^2/D_local`.
3. Every aligned cell has zero initial work, every selected denominator stays
   positive, and there are no selected-cell denominator faces or refresh
   atoms.
4. The finite selected-cell positive creation is at least
   `A*/(64*C_part*K^2)`.
5. The same bounded-overlap full-frame local heat/support payment is at most
   `N*(1-2^(-1/9))/(2*nu*K^4)`.  Their ratio grows at least as a positive
   multiple of `nu*K^2`.
6. Cutoff-curl, denominator collar, viscous collar, tangent, and normalization
   rows are retained.  The viscous collar is leading `K^-2` after aggregate
   weighting and integration; no Leray payment for it is proved.
7. The result does not cover arbitrary or moving partitions, general faces or
   refresh atoms, an infinite frame-cell identity, a continuation criterion,
   regularity, singularity, originality, priority, or the Millennium problem.

## Files

- `result.json` — sorted exact SymPy result;
- `independent-result.json` — independent Fourier, smooth-partition,
  one-cell quadrature, and scaling audit;
- `command.txt` — reproduction commands;
- `environment.txt` — runtime and release binding;
- `SHA256SUMS` — release dependency hashes;
- `build_hashes.py` — deterministic hash-ledger generator;
- `../../r071k_exact_audit.py` — exact producer;
- `../../r071k_independent_audit.py` — independent checker;
- `../../r071k_report-source.md` — analytic report;
- `../../r071k_gap_matrix.md` — claim matrix;
- `../../r071k_literature_audit.md` — primary-source audit;
- `../../r071k_independent_audit.md` — independent mathematical audit;
- `../../../figures/r071k-matched-cells/fig-r071k-matched-cell-gap` — formal
  figure package.

## Reproduction boundary

The producer uses exact SymPy algebra.  The independent checker reconstructs
the Fourier field without importing the producer or project Fourier helpers,
then evaluates a complete one-cell cutoff-curl denominator with deterministic
360-point Gauss--Legendre quadrature.  No PDE time stepping, DNS, fitting,
random sample, GPU, or DGX system is used.

