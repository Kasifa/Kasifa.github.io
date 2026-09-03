# QA protocol

## Mathematics and provenance

1. Recompute every fraction in `contract.json` with `fractions.Fraction`.
2. Check in particular
   \(r_{\rm pay}-16\chi(66)=3062597/134120448>0\).
3. Verify all three live-source SHA-256 hashes and byte counts.
4. Verify the primary audit records PASS with zero blockers and the literature
   audit describes only a bounded non-hit.
5. Verify `source-data.csv` row counts, exact rates, quantifier branch order,
   and byte-identical deterministic regeneration.
6. Reject any encoding that requires \(\tau_2=\tau_3\), promotes the strip
   upper comparison to a whole-shell upper bound, closes the actual payment
   gate, or asserts novelty.

## Exports

1. Require SVG, PNG, and single-page PDF.
2. Require the 600-dpi PNG to be 4204×2740 pixels.
3. Require final-size, greyscale, and PDF QA PNGs to be 2102×1370 pixels.
4. Require PDF media box approximately 504.57×328.82 points and all fonts
   embedded.
5. Require live SVG text, no embedded raster, no external href, one navy root
   plus neutrals, and the locked top-right research blossom.
6. Require the visible scope label verbatim in vector and PDF text.

## Human visual inspection

Inspect the three QA PNGs at actual size and confirm:

- all titles, fractions, axes, and branch labels are legible and unclipped;
- packet identities survive greyscale through marker shape/fill;
- Panel B clearly says the time is chosen after the fixed deletion set and
  that witness times may differ;
- Panel C identifies rates in \(L_1^2\)-units and confines its upper comparison
  to the two strip integrals;
- Panel D visibly separates PROVED, NOT PROVED, NO-GO, and NEXT X.52;
- no title, label, arrow, footer, or blossom collision is present.

## Determinism and seal

The seal command renders twice into independent temporary directories and
requires identical SHA-256 hashes for the 18 deterministic source/raw files.
It then writes `validation.json`, `qa-report.md`, `manifest.json`, and
`SHA256SUMS`. The result remains a local precommit seal, not a Git seal.
