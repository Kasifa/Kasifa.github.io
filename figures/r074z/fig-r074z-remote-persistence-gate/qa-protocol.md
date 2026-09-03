# QA protocol

## Mathematics and provenance

1. Recompute every rational in `contract.json` with `fractions.Fraction`.
2. Verify the two fourth-root shifts and recompute
   \(\Delta_{\rm rem}=64279/238140000\),
   \(\kappa_*=64279/158760000\), and the complexity coefficient
   \(476239/1064835072\).
3. Verify all three live-source SHA-256 hashes and byte counts.
4. Verify primary-audit PASS with zero blockers and literature-audit bounded
   non-hit/no-novelty boundaries.
5. Regenerate `source-data.csv` byte-for-byte and check the exact affine rate
   curve crosses zero at \(\kappa_*\).
6. Reject any critical-layer closure, unconditional endpoint-to-tube claim,
   strip-kinetic-to-full-clock promotion, accumulated-row closure, or novelty
   claim.

## Exports

1. Require SVG, 600-dpi PNG, and single-page vector PDF.
2. Require the publication PNG to be 4204×2740 pixels.
3. Require final-size, greyscale, and PDF QA PNGs to be 2102×1370 pixels.
4. Require PDF media box approximately 504.57×328.82 points and all fonts
   embedded.
5. Require live SVG text, no embedded raster, no external href, one navy root
   plus neutrals, and the locked top-right research blossom.
6. Require the scope label verbatim in vector and PDF text.

## Human visual inspection

Inspect all three QA PNGs at actual size and confirm:

- all panel titles, exact fractions, equations, and status labels are legible;
- the two weight shifts and physical-shell identity are unambiguous;
- Panel B distinguishes the strict proved side from the open equality layer
  using line/open mark/hatch as well as tone;
- Panel C says `CONDITIONAL ON Z.22 + MOVING-STRIP ALL-WINDING` and
  `NECESSARY, NOT SUFFICIENT`;
- Panel D visibly keeps full-clock Y.57 and accumulated rows OPEN;
- no title, label, callout, footer, arrow, or blossom collision is present.

## Determinism and seal

The seal command renders twice into independent temporary directories and
requires byte-identical hashes for the 18 deterministic source/raw files. It
then writes `validation.json`, `qa-report.md`, `manifest.json`, and
`SHA256SUMS`. The result is a local precommit seal, not a Git seal.
