# QA protocol

1. **Upstream gate.** Verify exact experiment row counts (1,960 and 245),
   `N=10`, `finiteDimensionalOnly=true`, passed validation checks, manifest
   hashes, certificate claims, and certificate validation.  Recompute SHA-256
   for every ingested file.
2. **Formula gate.** Recompute the heat-shear primitive, the physical energy
   envelope, all triangular gains, the `d=0` shear constants, the block upper
   bound, and `(a/2-p)_+`.  Compare the four observed exponents to the validated
   fit rows and the certificate ledger.
3. **Data gate.** Require exactly thirteen distinct `mu` values per Panel-A
   series, four finite/limit/envelope triplets in Panel B, 61 points per Panel-C
   curve, 61 prediction points per Panel-D path, and four audited markers per
   path.  No synthetic replacement is allowed.
4. **Visible-boundary gate.** The SVG and PDF must visibly state `FINITE N=10`,
   distinguish theorem curves from finite diagnostics, say whether lineage is
   draft or formal, deny a Galerkin tail bound and exact maximum transient
   claim, and keep A2/nonlinear/Clay open.
5. **Geometry gate.** Require exact 178 mm by 150 mm PDF/SVG size, one vector
   PDF page with no raster XObjects, at least two embedded fonts, exact 600-dpi
   PNG dimensions and metadata, white corners, and no clipping in the 300-dpi
   final-size preview.
6. **Visual gate.** Inspect `qa-final-size.png`, `qa-grayscale.png`, and the
   independently rasterized `qa-pdf.png`.  Confirm legibility, honest log axes,
   marker/stroke redundancy, no label collisions, and a data-free blossom
   locked to the top-right header.
7. **Inventory gate.** Require an exact manifest and `SHA256SUMS`.  In formal
   mode require clean, distinct source/certificate commits and unchanged figure
   source bytes since the source commit.  Draft outputs cannot be published.
