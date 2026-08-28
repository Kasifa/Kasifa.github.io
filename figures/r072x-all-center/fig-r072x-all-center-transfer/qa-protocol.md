# R0.72X formal figure QA protocol

1. Require a clean, source-bound formal certificate and distinct source and
   certificate commits before rendering.
2. Confirm the scan uses the full exact shifted potential, ten physical
   centers spanning both endpoints of the heat history, five alpha values,
   and simultaneous spatial/time refinement.
3. Require the exact Lanczos-Ritz policy in `config.json`: dimensions 8 through
   32, checks every 4 dimensions, two full reorthogonalization passes, and
   actual-space relative residual tolerance `1e-10`.  Check every raw-row
   dimension against that range and stride.  Cross-check the relative-to-finest
   audit, discrete adjoint defect, actual Ritz residual, and direct-versus-
   Rayleigh norm defect against the global numerical-QA thresholds `5e-4`,
   `1e-10`, `1e-8`, and `1e-10`.  Require every numerical scalar to be finite
   and every fine-grid relative-to-fine value to be exactly zero.  These are
   reproducibility gates, not theorem hypotheses or continuum-error bounds.
4. Cross-check the exact finite-alpha interface rows and exact block counts
   against independent formulas.
5. Inspect the 178 mm final-size preview, the grayscale preview, and the PDF
   render.  Check labels, direct annotations, axes, log units, and every panel
   boundary.  Hue alone is insufficient; dash, fill, and marker shape carry
   redundant distinctions.
6. Confirm the visible label `NUMERICAL DIAGNOSTIC ONLY - NOT PROOF`, the
   symbolic unevaluated q statement, the CLOSED analytic-report statement,
   and all OPEN boundaries.
7. Run the package-local fail-closed validator and the repository-wide figure
   schema validator.  Both must return no errors before publication.
