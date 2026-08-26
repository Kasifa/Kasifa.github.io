# Figure R0.71Y-1: growing-root operator sampling

This directory is the reproducible journal-figure package for the R0.71Y
operator-sampling theorem. Its scientific inputs are the committed-form
certificate payloads:

- `research/certificates/r071y/result.json`;
- `research/certificates/r071y/independent-result.json`.

The source/certificate provenance commit is
`8836d45625304ce8f867283f736a1911ee3d8ada`. The package extracts those
committed files without rewriting or rerunning the theorem audits.

## Reading the panels

- **A:** the exact integer-lattice payment (NM/K_s) and its
  (3/(4N)) upper bound.
- **B:** (N=1)-normalized exact theorem envelopes at fixed
  (\delta_{\mathrm{obs}}=1/8): no separation, fixed (h=0.05), and
  quasi-uniform (h=N^{-1}).
- **C:** the certified equal-grid inverse lower bound for (r_l=l) under
  (h=N^{-3}), plotted as its base-ten logarithm.

`data.csv`, `data.json`, `results.json`, and
`figure-data-metadata.json` retain the raw formulas, normalizers, source
paths, evidence classes, and source hashes. Panel B normalizes only to compare
the exact (N)-laws; its unnormalized theorem quantities remain in
`rawValue`.

## Reproduce

Run `command.txt` from the repository root. The pipeline performs source
extraction and analytic cross-checks, renders PDF/SVG/600 dpi PNG outputs,
creates color/grayscale/PDF QA assets, runs an independent validator, and
builds the manifest and SHA-256 ledger.

## Claim boundary

The curves are analytic/certificate envelopes, not DNS or samples from a
constructed growing-root family. The (N^{-1}) theorem uses the declared
unit-phase triangular class, real shear, fixed target, and full
growing-dimensional enstrophy floors, and it controls selected exact roots.
The equal-grid inverse lower bound is a conditioning warning, not an upper
bound on the true nonlinear IFT radius. No universal endpoint or regularity
claim is made.
