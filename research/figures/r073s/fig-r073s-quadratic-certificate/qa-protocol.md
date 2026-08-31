# R0.73S figure QA protocol

1. Reconstruct all plotted values independently from the sealed R0.73S
   source CSV and the stated exact identities.
2. Verify that every exact Panel B curve lies below its corresponding
   certificate curve.
3. Verify physical PDF size, vector-only PDF/SVG output, 600-dpi PNG size,
   schema, row counts, formula monotonicity, and claim-boundary metadata.
4. Inspect `qa-final-size.png` at 178 mm equivalent size for labels, legends,
   collisions, clipping, and hierarchy.
5. Inspect `qa-grayscale.png` to confirm line/marker redundancy independent
   of colour.
6. Inspect `qa-pdf.png` to catch vector-export and font-rendering defects.
7. Run the final fail-closed validator with `--confirm-visual-qa`, then verify
   the resulting manifest and `SHA256SUMS` in `--verify-only` mode.

No visual confirmation may be inferred from structural checks alone.
