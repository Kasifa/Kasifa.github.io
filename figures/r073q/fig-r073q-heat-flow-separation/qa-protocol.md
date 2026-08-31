# R0.73Q figure QA protocol

## Automated independent checks

1. Reconstruct every \(N=2^j\) and \(n=2^j\) independently from
   `config.json`.
2. Recompute \(c_6=(5/16)^{1/6}\), the three shear norms, and all recorded
   ratios without importing plotting functions.
3. Check exact monotonic direction: \(L^2\) and \(\mathfrak X\) strictly
   decrease, while \(H^{1/2}\) strictly increases.
4. Recompute \(\|g_n\|_4^4\), \(\|g_n\|_4\), and the fractional output;
   verify bounded input and strictly divergent output on the configured grid.
5. Check CSV schema, record counts, contract booleans, source inventory,
   pinned dependency versions, hashes, raster DPI/dimensions, PDF page size,
   one-page PDF structure, and required SVG labels.
6. Verify that the SVG explicitly says `NO RADIUS ORDERING` and
   `BARE ENDPOINT MAP ONLY`.

## Visual checks at delivery size

- Inspect `qa-final-size.png` at 178 mm by 90 mm and 300 dpi.
- Inspect `qa-grayscale.png` for line-style and marker redundancy.
- Inspect `qa-pdf.png`, rendered independently from the vector PDF.
- Confirm no clipped titles, legends, mathematical labels, annotations, or
  panel letters.
- Confirm the three panels use honest logarithmic axes and no hidden or
  truncated radius scale.
- Confirm arrows and labels remain attached to their data after conversion.

## Claim-boundary checks

- The figure is labelled as a closed-form formula diagnostic, not an NSE
  simulation.
- Panel B contains no numerical R0.73P or R0.73Q radius and makes no ordering
  claim.
- Panel C names only the bare \(I_{1/4}:L^4\to L^\infty\) endpoint route and
  does not claim to refute Koch--Tataru theory.
- The caption denies arbitrary \(L^2\)-small safety, nonlinear PDE
  certification, global regularity, and a Clay conclusion.

The source-unsealed preseal can pass all formula and visual checks. Formal
status additionally requires an immutable source commit and a separate
sealed-artifact commit.
