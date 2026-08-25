# R0.71M certificate bundle

This bundle certifies the exact annular-filter Lamb increment identity, the
fixed-cell projective-pairing formulas, the displayed direct four-row
envelope, and a standalone deterministic Fourier diagnostic.

The exact producer checks:

- the signed quadratic velocity-increment formula;
- the fixed-cell rank-one projective pairing and radial form;
- the constants in the direct four-row Cauchy envelope;
- formal local Euclidean NSE scaling with co-scaled filter and cutoff; and
- the heat-packet exponents and half-derivative interpolation gap.

The independent checker reconstructs a divergence-free finite Fourier field,
annular multiplier, and positive cutoff without importing the exact producer.
It verifies the increment identity, fused source, projective and radial
pairings, positive high off-band commutator energy for the witness, and the
four-row upper bound at order 64.

Claim boundary: the four-row ledger is sufficient only for the displayed
direct absolute route and is not claimed necessary. The heat packets are
linear heat flows, not nonlinear NSE solutions. This bundle proves no logical
defect-to-tangent non-implication, continuation criterion, singularity,
global regularity, originality, or Millennium-problem result.

## Files

- `result.json` — exact symbolic result;
- `independent-result.json` — standalone order-64 Fourier diagnostic;
- `command.txt` — reproduction commands;
- `environment.txt` — execution environment;
- `build_hashes.py` and `SHA256SUMS` — archive integrity;
- `../../r071m_exact_audit.py` and `../../r071m_independent_audit.py` — producers;
- `../../r071m_report-source.md`, `../../r071m_gap_matrix.md`,
  `../../r071m_literature_audit.md`, and `../../r071m_independent_audit.md` —
  analytic evidence;
- `../../../figures/r071m-increment-commutator/fig-r071m-increment-commutator-boundary` —
  journal figure package.
