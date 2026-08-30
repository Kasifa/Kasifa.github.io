# R0.73H formal figure package

This package renders one paper-ready four-panel figure from the immutable
R0.73H certificate commit.  Panel A records the exact rational/analytic
continuum subcertificate for the doubled row.  Panels B--D are finite
binary64 Galerkin diagnostics and are labelled as such in the figure and
caption.  Their response ratios use the diagnostic endpoint `d=0.01`, which is
strictly outside the theorem window `D<=1/450` (approximately `0.002222`); the
plotted endpoint is not the theorem endpoint `d=D`.  The independent numerical
check contains four formal sentinels plus one independently recomputed holdout.

The renderer refuses a changed certificate input or a changed plotting-source
blob.  The validator creates final-size, grayscale, and PDF-raster QA views,
checks the vector/raster geometry and evidence boundary, and writes a complete
SHA-256 ledger.

Run the two commands in `command.txt` from the repository root.  The final
exports are a one-page vector PDF, an editable vector SVG, and a 600 dpi PNG at
178 mm double-column width.
