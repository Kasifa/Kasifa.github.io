# R0.73M figure QA protocol

1. Require the sealed R0.73M certificate, validation, and manifest to pass;
   bind those files and all plotted JSON inputs by SHA-256.
2. Deterministically derive `source-data.csv`; verify the complete 15-case
   grid, the 12 gate components, their provenance, and each family maximum.
3. Recompute every plotted normalization and discrepancy-to-tolerance ratio
   from the upstream scalar and its frozen tolerance.
4. Export one-page vector PDF, vector SVG, and 600-dpi PNG at 178 by 128 mm.
5. Inspect the final-size color raster, grayscale raster, and an independently
   rendered PDF raster for clipping, collisions, detached labels, sign loss,
   scale ambiguity, and loss of non-color distinctions.
6. Fail closed if input bindings, row counts, formulas, dimensions, PDF page
   count, SVG structure, gate ratios, or claim-boundary flags differ from the
   contract.

