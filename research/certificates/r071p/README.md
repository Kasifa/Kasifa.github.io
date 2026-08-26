# R0.71P certificate bundle

This bundle certifies the half-open positive-entry ledger, the distinction
between componentwise relaxed soft positive parts and the positive Jordan
part of a signed aggregate, the simultaneous frame--cell batching theorem,
the distinct entry-time counting-measure reduction, one abstract temporal
packing separation, and one sharp smooth Navier--Stokes initial jet.

The exact producer checks:

- the sharp Cauchy projection identity and a rational bounded-overlap ledger;
- the positive atomic layer-cake identity and even-touch hard/soft defect;
- subtraction of the declared initial trace on a constant positive branch;
- the half-open \([0,2\pi)\) endpoint convention and its exact \(N\)-entry
  count;
- exact denominator, first-time, and soft-entry budgets for the oscillatory
  Hilbert family;
- exact finite Fourier convolution for the NSE initial jet, including the
  vanishing filtered vorticity and filtered viscous jet; and
- the qualitative finite-truncation statement on a classical analytic
  interval.

The standalone checker imports neither producer nor prior release code.  It
uses 64 seeded finite-overlap trials, sampled-sign/Brent root detection on
half-open windows, adaptive SciPy quadrature, and a separate \(32^3\) NumPy
FFT reconstruction of the NSE initial jet.

Claim boundary: the componentwise relaxed positive-entry measure need not be
the positive Jordan part of a signed aggregate.  The oscillatory family is an
abstract Hilbert path, not a coupled NSE observable.  The NSE calculation is
one one-sided initial jet, not an internal face or an unbounded NSE face
count.  The bundle proves no uniform temporal packing, infinite-frame or
Leray passage, continuation criterion, singularity, global regularity,
originality, or Millennium-problem result.

## Files

- `result.json` - exact symbolic result;
- `independent-result.json` - standalone overlap, root, quadrature, and FFT
  audit;
- `command.txt` - reproduction commands;
- `environment.txt` - execution environment;
- `build_hashes.py` and `SHA256SUMS` - archive integrity;
- `../../r071p_exact_audit.py` and `../../r071p_independent_audit.py` -
  producers;
- `../../r071p_report-source.md`, `../../r071p_gap_matrix.md`,
  `../../r071p_literature_audit.md`, and
  `../../r071p_independent_audit.md` - analytic evidence;
- `../../../figures/r071p-positive-entry-batching/fig-r071p-positive-entry-batching`
  - journal figure package; and
- the synchronized public note, cumulative recap, PDFs, and public figure
  mirrors listed in `SHA256SUMS`.
