# Figure QA protocol

1. Confirm the package is exactly 25 files: 10 source, 11 raw/result, and 4 metadata.
2. Verify the frozen core commit exists, is an ancestor of the active checkout, and yields the three configured Git blobs and SHA-256 digests.
3. Regenerate every CSV row and require exact equality.
4. Require the period quadrature, RK4 closure, streamline invariant, endpoint return, \(g\)-range, \(q=g'\), one-cycle variation, signed drift, cumulative monotonicity, and amplitude-slope audits to pass.
5. Check the master PNG pixel dimensions and 600-dpi metadata at 178 mm by 116 mm.
6. Check the SVG and one-page PDF physical dimensions; require embedded PDF fonts and explicit non-DNS/non-Clay text.
7. Independently rasterize the PDF and compare it with the final-size PNG.
8. Inspect `qa-final-size.png` at 178 mm equivalent, `qa-grayscale.png`, and `qa-pdf.png`.  Reject clipping, overflow, detached labels, illegible markers, or ambiguous grayscale series.
9. Capture the deterministic core, rerender, and require all 18 hashes to remain unchanged.
10. Preseal with `PENDING_FIGURE_SOURCE_COMMIT`.  After committing exactly 21 source/raw files, final-reseal with the actual commit and verify each Git blob byte-for-byte.

Passing this protocol certifies figure reproducibility and presentation only.  It does not certify the open positive-excursion estimate or Navier--Stokes regularity.
