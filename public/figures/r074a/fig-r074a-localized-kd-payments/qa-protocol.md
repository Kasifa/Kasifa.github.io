# R0.74A figure QA protocol

The package is accepted only when all checks below pass.

1. **Source binding.** HEAD, six frozen source hashes, certificate status and
   21/21 summary, and every `OPEN`/`NOT CLAY` boundary match `config.json`.
2. **Formula reconstruction.** Every CSV row is reconstructed independently;
   binary64 discrepancy must not exceed `5e-13`.
3. **Panel A.** The two displayed weights are exactly `theta^(1/4)` and
   `theta` under the declared unit normalization; unknown `C` is suppressed.
4. **Panel B.** `N=2^j`, `epsilon=N^(-2/3)`, and all three factors exactly
   match `N^0`, `N^(-2)`, and `N^(2/3)`; unknown `c` is suppressed.
5. **Panel C.** The two displayed factors exactly match `delta^0` and
   `delta^(-2/3)`; every row retains the separate-field and no-uniform-energy
   qualifier.
6. **Export.** SVG and one-page PDF are vector, 178 mm by 74 mm; PNG is the
   same page at 600 dpi. SVG contains no raster image and PDF contains no
   image XObject.
7. **Final-size QA.** `qa-final-size.png` is the 300 dpi downsample of the
   archival PNG. `qa-pdf.png` is an independent 300 dpi Poppler render.
8. **Grayscale QA.** `qa-grayscale.png` is a true grayscale conversion;
   dash patterns and markers remain sufficient without color.
9. **Visual review.** Titles, axes, direct labels, qualifiers, footer, and
   top-right research blossom have no collision, clipping, or unreadable text.
10. **Inventory.** Exactly the 25 contract files exist, with no symlink or
    package-local temporary file.
11. **Determinism.** A second render leaves all 18 deterministic-core hashes
    unchanged. Runtime/resource observations are excluded from that core.
12. **Claim boundary.** Figure, caption, README, and manifest say the packets
    are not unforced NSE trajectories; no simulation/DNS is used; finite rows
    do not prove quantifiers; and the result is `NOT CLAY`.
