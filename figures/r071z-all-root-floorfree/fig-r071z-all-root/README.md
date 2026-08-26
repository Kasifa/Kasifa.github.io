# Figure R0.71Z-1: all-root suppression and launch retention

This directory is the reproducible journal-figure package for the R0.71Z
complete-root BV theorem and launch-inclusive floor cancellation. Its
scientific inputs are:

- `research/certificates/r071z/result.json`;
- `research/certificates/r071z/independent-result.json`;
- `research/r071z_report-source.md`;
- `research/r071z_independent_audit.md`.

The producer refuses to run unless both certificates pass and every primary
check is true. It then extracts or independently reconstructs the exact
formulas without rerunning a PDE solver.

## Reading the panels

- **A:** exact integer-lattice payment (M/K_s) and the analytic
  (3/M^2) bound.
- **B:** bounded-η complete-root (M^{-2}) suppression against the
  neutral older selected-root (M^{-1}) payment.
- **C:** normalized upper-envelope laws for η (=1),
  η (=M^{1/2}), and η (=M^{6/7}).
- **D:** fixed-window heat retention against launch-inclusive retention one.

`data.csv`, `data.json`, `results.json`, and
`figure-data-metadata.json` retain formulas, normalizers, evidence classes,
source paths, and source hashes. Normalization is used only to compare exact
(M)-laws; every unnormalized value remains in the data files.

## Reproduce

Run `command.txt` from the repository root. The pipeline extracts and
cross-checks the certificate formulas, renders PDF/SVG/600 dpi PNG outputs,
creates final-size color/grayscale/PDF QA assets, runs an independent
validator, and builds the manifest and SHA-256 ledger.

## Claim boundary

The curves are analytic/certificate envelopes, not DNS or samples from a
constructed growing-root family. The all-root theorem controls squared slope
mass, not raw root count. It uses real shear, unit phases, distinct positive
integer carriers, a fixed target, fixed (A_0>0), and a payment interval
that includes launch while counted roots remain on the later observation
window. The η (=M^{6/7}) curve is diagnostic only. The heat-shear curve
shows loss of automatic retention but has no nonzero target-root atom. No
universal endpoint or regularity claim is made.
