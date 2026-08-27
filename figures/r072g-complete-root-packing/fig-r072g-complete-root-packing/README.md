# R0.72G-1 formal figure package

This directory is the paper-ready archive for the complete-root packing
figure.  `build_figure.py` reads the two passing R0.72G certificates,
reconstructs `data.csv`, and exports PDF, SVG, and 600 dpi PNG.  The figure
does not read the failed-attempt files.

The chart contract is in `figure-contract.md` and `contract.json`.  It
separates the analytic logarithmic-order theorem from the finite diagnostic
leading coefficient, root count, and dyadic tail.

Run the commands in `command.txt` from the repository root.  The final-size,
grayscale, PDF-raster, data-lineage, and byte-identical public-copy checks
must all pass before publication.
