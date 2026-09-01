# Chart contract and source data

## Analytical question

Why does the frozen (P^{2/3}) payment miss one power of (L) on the
explicit two-packet family, and how does the positive collar flux restore
that scale without inventing numerical constants?

## Takeaway

The old normalized payment carries (L^0), while both the endpoint and the
positive cumulative collar flux carry the rigorously derived lower scale
(L^1). Inserting \(\mathfrak C_R^{3/2}\) inside the repaired payment turns
that row back into (L^1) after the outer (2/3) power.

## Figure family and surface

- Panel A: exact implication/ledger diagram.
- Panel B: horizontal exact-exponent dot diagram.
- Surface: static 180 mm x 82 mm journal figure.
- Exports: SVG, PDF, and 600-dpi PNG.
- QA: grayscale, 1800-pixel final-size raster, and independent PDF raster.

## Source contract

All plotted powers are parsed from the frozen R0.74H certificate
`research/r074h_collar_flux_certificate.json`, SHA256
`783591f3da880ec9182be89c585eb732e35d5842b7d196dc2ae4e35b6c0d2ba4`.
The only finite producer is `scripts/r074h_collar_flux_certificate.py`,
SHA256
`acce024b8dd78ba727e3ec8176a308dc53ecc34b7bdaf57b6c48e5d1e1a5c6e4`.
The renderer refuses either source if its hash drifts or if producer stdout
is not byte-identical to the certificate.

`source-data.csv` retains the exact rational exponent, formula, direction,
status, and note for every visible quantitative row. Endpoint and flux rows
are labeled analytic lower scales because the finite certificate checks
compatibility but does not prove their analytic lower bounds.

## Visual policy

- Palette: hard two-root cap, blue and gold plus neutrals.
- Non-color distinction: open circle, filled square, filled diamond;
  solid versus dashed strokes; separate rows; direct (L^0/L^1) labels.
- Absolute magnitudes are not plotted because the theorems contain unknown
  constants. No proxy numbers, sampled trajectories, or simulated values are
  introduced.
- Research blossom: locked at the top-right of the header.
- Scope labels: `EXACT EXPONENT DIAGRAM`, `NOT DNS`, `NOT SIMULATION`, and
  `NOT CLAY` are visible on the final figure.
