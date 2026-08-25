# R0.71O certificate bundle

This bundle certifies the fixed-cell soft-denominator identities, the
finite-order face-layer theorem, the logarithmic cancellation in the raw
source split, an abstract ordinary-budget separation, and one smooth
Navier--Stokes initial entry face.

The exact producer checks:

- the two soft-source conventions and positive-branch balances;
- the factorization \(z_\varepsilon=\sqrt{\sigma_\varepsilon}z\) and
  \(a_\varepsilon=\sigma_\varepsilon a\);
- finite-order inner profiles for orders one through eight;
- signed, positive, negative, and total-variation face atoms;
- the opposite logarithmic divergence of the raw source and radial pieces;
- exact oscillatory-path budgets and measure limits; and
- exact finite Fourier convolution for the NSE initial jet.

The standalone checker imports neither producer nor earlier release code. It
uses adaptive SciPy quadrature for the profiles, raw cancellation, and seven
oscillation frequencies, plus a separate \(32^3\) NumPy FFT reconstruction of
the four-mode NSE initial face.

Claim boundary: the oscillatory family is an abstract Hilbert path, not a
coupled NSE observable. The NSE calculation is one one-sided initial jet, not
an internal face or an unbounded NSE face count. The bundle proves no uniform
frame--cell face sum, continuation criterion, singularity, global regularity,
originality, or Millennium-problem result.

## Files

- result.json - exact symbolic result;
- independent-result.json - standalone quadrature and FFT audit;
- command.txt - reproduction commands;
- environment.txt - execution environment;
- build_hashes.py and SHA256SUMS - archive integrity;
- ../../r071o_exact_audit.py and ../../r071o_independent_audit.py - producers;
- ../../r071o_report-source.md, ../../r071o_gap_matrix.md,
  ../../r071o_literature_audit.md, and ../../r071o_independent_audit.md -
  analytic evidence;
- ../../../figures/r071o-soft-denominator-faces/fig-r071o-soft-denominator-faces -
  journal figure package.
