# R0.73L figure QA protocol

1. Bind the primary diagnostic, independent validation, experiment config,
   environment, package validation, and both monitoring streams by SHA-256.
2. Derive `source-data.csv` and verify the expected row counts and epsilon
   levels.
3. Export one-page vector PDF, vector SVG, and 600-dpi PNG at 178 by 128 mm.
4. Inspect the final-size color raster, grayscale raster, and an independently
   rendered PDF raster for clipping, collisions, detached annotations, and
   loss of non-color distinctions.
5. Fail closed if source bindings, dimensions, PDF page count, SVG structure,
   validation ratios, or claim-boundary flags differ from the contract.

