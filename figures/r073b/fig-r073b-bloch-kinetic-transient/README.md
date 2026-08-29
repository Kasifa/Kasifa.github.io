# R0.73B Bloch kinetic transient figure package

This package renders the four-panel journal figure contracted in
`figure-contract.md`.  It ingests the validated R0.73B finite
Fourier--Galerkin screen and the R0.73B certificate, records every plotted
row in `data.csv`, and recomputes all displayed analytic curves.

The package is deliberately fail-closed.  It refuses missing or failed
experiment validation, incomplete row counts, changed upstream hashes,
non-finite values, absent certificate claims, or an attempt to seal a formal
figure before the certificate has a distinct committed lineage.  Draft mode
is allowed while the certificate is still `source-stage`; its manifest and
visible figure both say that formal lineage is pending.

## Reproduction

Use the bundled Python runtime recorded in `command.txt`.

1. Run `plot.py --self-test` for a zero-write source and formula check.
2. Run `plot.py --draft --visual-inspected` to create the source-stage draft.
3. Run `validate.py` independently.
4. After the certificate commit exists, rerun in formal mode with full source
   and certificate commit hashes.  Formal mode also requires a clean worktree
   at the certificate commit and refuses to overwrite a prior formal result.

The renderer is deterministic, single-process, one-threaded, and uses no
randomness.  PDF and SVG are native vector output.  The PNG is exactly 600
dpi; the PDF QA preview is independently rasterized by `pdftoppm`.

## Claim boundary

The propagator markers are finite `N=10` diagnostics.  They do not provide a
Galerkin tail enclosure or an infinite-dimensional maximum transient theorem.
The energy envelope and the two analytic shear-coefficient bounds are theorem
curves imported from the analytic work.  The integrated coefficient
`0.188106...` is not plotted as a propagator gain.  Complete A2 direct-sum,
nonlinear Navier--Stokes, and Clay implications remain open.
