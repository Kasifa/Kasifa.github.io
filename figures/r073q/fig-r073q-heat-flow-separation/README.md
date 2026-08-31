# R0.73Q heat-flow separation figure

This package is a source-complete, data-driven three-panel formula diagnostic
for R0.73Q. It is not a Navier--Stokes simulation and it is not a numerical
regularity certificate.

- Panel A evaluates the exact normalized-Haar norms of
  \(w_N=N^{-1/4}e_2\sin(Nx_1)\) for \(N=2^j\).
- Panel B displays the same exact sequence in the
  \((\|w_N\|_{\mathfrak X},|w_N|_{1/2})\)-plane. It records strict
  topological separation and does not compare the independently derived
  R0.73P and R0.73Q radii.
- Panel C evaluates the exact time-endpoint counterexample \(g_n\): its
  \(L^4\) norm stays bounded while the fractional-integral output at
  \(t=1\) diverges.

`plot.py` writes the source CSV, vector SVG and PDF, 600-dpi PNG, final-size
and grayscale QA rasters, and a PDF raster. `validate.py --preseal`
independently reconstructs every plotted formula, checks the inventory,
dimensions, labels, dependencies, claim boundaries, and hashes, but does not
bind the package to a Git commit. The resulting status is
`source-unsealed-preseal`.

Formal sealing is intentionally deferred. After the ten source files have
been committed, rerun the final validator with that immutable 40-hex commit:

```text
validate.py --final --confirm-visual-qa --source-commit FULL_40_HEX_COMMIT
validate.py --final --verify-only
```

The main release agent must then mirror the identical package under
`figures/r073q/fig-r073q-heat-flow-separation/` and commit the sealed
artifacts. Commands are recorded in `command.txt`.
