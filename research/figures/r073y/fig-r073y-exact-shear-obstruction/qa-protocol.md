# R0.73Y figure QA protocol

The archive is accepted only when all of the following checks pass.

1. **Runtime gate.** `plot.py` must verify Python 3.12.13, NumPy 2.5.2, and Matplotlib 3.10.6 before writing output.
2. **Source gate.** The checkout commit, three theorem/certificate file hashes, certificate status, `not_clay` flag, and certificate payload must match `config.json` before writing output.
3. **Formula gate.** Every CSV row must be independently reconstructed. The expanded heat-semigroup identity, sampled exact statistics, and amplitude homogeneity must agree within `5e-13`; every audited $D_{ii,s}$ minimum must be positive.
4. **Export gate.** PDF must be one page at 178 mm by 62 mm with embedded fonts. SVG must declare the same physical dimensions. PNG must have the corresponding pixel dimensions and 600 dpi metadata.
5. **Final-size QA.** `qa-final-size.png` must be the 300 dpi, 178 mm by 62 mm downsample of the archival PNG.
6. **Grayscale QA.** `qa-grayscale.png` must be the exact grayscale conversion of the final-size QA image; line styles and labels must remain distinguishable.
7. **PDF QA.** `qa-pdf.png` must be a 300 dpi rendering of the one-page PDF at the final physical size. Its mean absolute RGB difference from the final-size PNG must remain below the recorded threshold.
8. **Visual review.** Titles, axes, legends, formula, non-DNS label, panel markers, footer, and top-right research blossom must be legible with no clipping or collisions in all three QA assets.
9. **Inventory gate.** The archive must contain exactly the 25 contract filenames, no symlinks, no package-local temporary files, and no additional files.
10. **Portability gate.** No archive file may contain machine-specific hard-coded source or home-directory paths. Runtime provenance records versions and policy without absolute interpreter or package paths.
11. **Determinism gate.** A second rendering with the same frozen source and pinned runtime must leave all 18 deterministic-core hashes unchanged.
12. **Negative tests.** Simulated runtime drift, theorem-source byte drift, and inventory drift must each fail closed.
13. **Standard manifest gate.** `manifest.json` must use `research-figure-manifest-v1`, the R0.73Y figure schema, `status=formal`, and `publicationStatus=staged`; the project-wide figure validator must return `errors=[]`.
14. **Two-stage Git seal.** Preseal retains an explicit pending figure-source sentinel. Final reseal accepts only a real full 40-hex commit, verifies all 21 committed Git blobs are byte-identical and scoped-clean, then rewrites only the four metadata files. `--verify-only` reconstructs those bindings.

UTC timestamps, process IDs, wall/CPU timing, resource observations, environment observations, sealing metadata, and checksums depending on them are nondeterministic observability and are excluded from the deterministic core.
