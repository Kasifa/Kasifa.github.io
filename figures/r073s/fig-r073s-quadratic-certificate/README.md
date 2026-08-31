# R0.73S formal figure package

This directory contains the journal-width source data, vector/raster figure,
independent validator, visual-QA derivatives, provenance manifest, and
cryptographic inventory for `fig-r073s-quadratic-certificate`.

The source table is derived from the already sealed R0.73S certificate plus
one explicitly marked analytic identity in Panel C. The validator reads the
sealed source independently, reconstructs every plotted quantity without
importing `plot.py`, checks vector/physical-size properties, and fails closed
on inventory drift.

Run the exact commands in `command.txt`. A preseal is diagnostic only. Formal
status requires manual confirmation of the final-size, grayscale, and PDF
raster views followed by the final validator/sealer pass.

No GPU or DGX resource is used.
