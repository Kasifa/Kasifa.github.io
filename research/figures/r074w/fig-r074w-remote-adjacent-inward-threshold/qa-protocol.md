# QA protocol

## Mathematical and provenance checks

1. Recompute every exact rational in `contract.json` with `fractions.Fraction`.
2. Recompute \(q(64)\), \(q(65)\), both original packet margins, the R0.74U
   reserve margin, and \(\chi(65)\).
3. Verify the exact SHA-256 and byte count of all three live research inputs,
   and verify that the primary audit records PASS with blocker count 0.
4. Verify source locators and the literal NOT CLAY boundary are present.
5. Regenerate `source-data.csv` independently and compare bytes.
6. Confirm the plotted Panel D curve is named a leading analytic scale and
   never a finite-\(L\) certified lower bound.
7. Confirm fixed deletion, critical transition, whole-shell occupation, DNS,
   PDE-data, and Clay claims remain false/open as specified.

## Export checks

1. SVG, PNG, and PDF must all exist and be non-empty.
2. PNG must be 4204×2740 pixels (178×116 mm at 600 dpi, rounded).
3. QA PNGs must be 2102×1370 pixels (300 dpi).
4. PDF must be one page with media box approximately 504.57×328.82 points.
5. All PDF fonts must be embedded Type 3 or embedded/subset fonts; no external
   font dependency is accepted.
6. SVG/PDF text must contain all four panel titles, the exact rate formula,
   the fixed-deletion-open boundary, and the required visible label.
7. The locked research blossom must occupy the top-right figure header.

## Visual checks

Inspect `qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png` at actual
size.  Record whether:

- panel titles and axis labels are legible;
- text, arrows, and callouts do not overlap;
- every label stays inside the canvas;
- the uniform-endpoint regions and hatched not-classified band remain
  separable in greyscale, while the exact \(q(\ell)\) curve remains visible;
- packet 1 and packet 2 remain distinguishable without colour;
- no fake trajectory-like polyline appears in Panel C;
- the footer and research blossom are clear;
- Panel D's unknown \(c\) and \(-CL\) qualification is readable.

Passing automated structure is not a substitute for visual inspection.  The
seal command requires the explicit `--confirm-visual-qa` flag after inspection.

## Determinism and seal

The validator renders twice into temporary directories and requires identical
SHA-256 hashes for the 18 deterministic source/raw files.  It then writes
`validation.json`, `qa-report.md`, `manifest.json`, and `SHA256SUMS`.  The
seal is local and precommit; the proof audit is hash-bound and passed, but the
archive must not be described as having a Git commit/blob seal.
