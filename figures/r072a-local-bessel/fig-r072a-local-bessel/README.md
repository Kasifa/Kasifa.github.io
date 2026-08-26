# Figure R0.72A-1

Formal double-column figure for the R0.72A local-exposure theorem and exact
Bessel strong-coupling family.

The package is deterministic. `build_figure.py` reads the two certified JSON
files, reconstructs the analytic phase boundary and Bessel comparison rows,
writes `data.csv`, `data.json`, and `results.json`, then exports SVG, PDF, and
600 dpi PNG. `qa_images.py` creates final-size, grayscale, and PDF-render QA
images. `validate.py` independently checks formulas, source hashes, cross-
auditor agreement, physical dimensions, palette, labels, and QA assets.
`build_manifest.py` records hashes after validation.

The plot is evidence, not the proof. The infinite-lattice argument is in
`research/r072a_report-source.md`; finite simulations corroborate it. No
random input, GPU, DGX, DNS, or three-dimensional PDE time stepping is used.
