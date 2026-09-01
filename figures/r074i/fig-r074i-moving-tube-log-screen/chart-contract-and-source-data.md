# Chart contract and source data

## Analytical question

What does the R0.74I proof chain actually establish from a small moving-tube
energy, and which logarithmic powers remain compatible with the explicit
packet family?

## Takeaway

Panel A records a strict implication chain: sufficiently small moving-tube
energy confines the mollified trajectory, embeds a fixed half-radius cylinder,
controls its normalized cubic velocity integral, and then reaches a regular
point through a published velocity-only one-scale criterion. Panel B records
the exact exponent screen

\[
y(\gamma)=1-2\gamma.
\]

Thus every fixed \(\gamma<1/2\) is rejected by the explicit family,
\(\gamma=1/2\) is the open endpoint, and \(\gamma>1/2\) is only not rejected;
it is not proved.

## Figure family and surface

- Panel A: exact moving-tube geometry plus a four-stage implication diagram.
- Panel B: exact affine exponent screen, with a signed vertical residual axis.
- Surface: static 180 mm x 88 mm double-column journal figure.
- Exports: SVG, vector PDF, and 600-dpi PNG.
- QA: 1800-pixel final-size raster, grayscale raster, and an independently
  rasterized PDF surface.

## Source contract

Every quantitative label and the exact affine screen are bound to
`research/r074i_tube_log_certificate.json`, SHA256
`d4d0f32f6772bdae8a9ec0e8fd6f5f5f9248877df3c19bf544c3577055ab7bf5`.
The sole finite producer is `scripts/r074i_tube_log_certificate.py`, SHA256
`5411134949eedbb1c285607c33a4f8feb9f8d358f5fc7cee91ec3601dfe3932f`.
The renderer refuses either source if its hash drifts or if producer stdout
is not byte-identical to the certificate JSON.

`source-data.csv` stores the exact rational exponents, implication direction,
status, and note for every visible quantitative record. Panel A is an exact
diagram of proved analytic implications; it does not plot unknown constants,
sampled paths, or numerical flow data. Panel B plots only the certified affine
exponent relation and exact rational reference points.

## Visual policy

- Palette: a hard two-root cap, blue and gold plus neutrals.
- Non-color distinction: numbered solid-outline stages, solid versus dashed
  arrows, hatch versus stipple texture, distinct markers, direct region labels,
  and positive/zero/negative residual signs.
- No unknown epsilon, interpolation, or theorem constants are assigned numeric
  values. The moving path is a schematic geometric carrier, not a measured
  trajectory.
- The research blossom is fixed at the top-right of the header.
- The final figure visibly states `EXACT DIAGRAM`, `NOT DNS`,
  `NOT SIMULATION`, and `NOT CLAY`.

## Interpretation boundary

The figure does not show that the smallness hypothesis holds at arbitrary
points or scales. It does not prove the endpoint logarithmic upper estimate,
and the region \(\gamma>1/2\) means only “not rejected by this family.” It is
not evidence of global regularity or a solution of the Clay problem.
