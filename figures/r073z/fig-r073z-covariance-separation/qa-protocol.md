# R0.73Z figure QA protocol

The package is accepted only when all checks below pass.

1. **Source binding.** HEAD, the nine bound source hashes, certificate status,
   certificate payload, and `NOT CLAY` boundary match `config.json`.
2. **Formula reconstruction.** Every CSV row is reconstructed independently;
   binary64 discrepancy must not exceed `5e-13`.
3. **Panel A.** Energy is exactly 6 and the plotted lower-bound factor is
   exactly the integer frequency `n`; no unknown constant is fabricated.
4. **Panel B.** Every partial sum matches the exact rational
   `(1-4^-J)/3`, its limit is `1/3`, every unit term is 1, and the divergent
   partial sum is exactly `J`.
5. **Panel C.** `Pi=S=0`; `D`, `|Q|`, and `div Q` match the closed formulas
   and are strictly positive at all recorded positive scales.
6. **Export.** SVG and one-page PDF are vector, 178 mm by 74 mm; PNG is the
   same page at 600 dpi.  SVG contains no raster image and PDF contains no
   image XObject.
7. **Final-size QA.** `qa-final-size.png` is the 300 dpi downsample of the
   archival PNG.  `qa-pdf.png` is an independent 300 dpi Poppler render.
8. **Grayscale QA.** `qa-grayscale.png` is a true grayscale conversion;
   dash patterns and markers remain sufficient without color.
9. **Visual review.** Titles, axes, dual-axis labels, formulas, panel letters,
   direct labels, footer, and top-right research blossom have no collision,
   clipping, or unreadably small text.
10. **Inventory.** Exactly the 25 contract files exist, with no symlink or
    package-local temporary file.
11. **Determinism.** A second render leaves all 18 deterministic-core hashes
    unchanged.  Runtime/resource observations are excluded from that core.
12. **Claim boundary.** Caption, README, and manifest state that finite rows
    visualize normalized analytic consequences and do not prove quantifiers,
    regularity, or any Clay conclusion.
