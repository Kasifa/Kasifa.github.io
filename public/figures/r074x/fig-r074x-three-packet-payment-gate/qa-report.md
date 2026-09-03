# R0.74X figure QA report

Status: **PASS**

Visual inspection confirmation: **YES**.  The explicit seal flag records that
`qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png` were inspected at
actual size after the final render.

## Scope and provenance

- Artifact: `fig-r074x-three-packet-payment-gate`
- Seal: local SHA-256 precommit seal; no Git commit/blob seal is claimed.
- Mathematical input SHA-256: `4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3`.
- Independent primary audit SHA-256:
  `834ec846c3f8629f9e7462caf4503bfa99ba6b88288da2dd525793206de9357e`;
  verdict PASS, blocker count 0.
- Literature audit SHA-256:
  `f58f7a1d095ba6bd8b27c41872301fd367fe784597160fe060f9cd332c64c422`;
  bounded primary-source non-hit only.

## Automated checks

- Exact rational identities and strict payment-versus-strip rate comparison: PASS.
- Source-data regeneration and 30-row semantic ledger: PASS.
- Deterministic two-render comparison: PASS (18 files).
- Publication PNG: 4204×2740 pixels at nominal 600 dpi.
- Three QA exports: 2102×1370 pixels at nominal 300 dpi.
- PDF: one page, 504.5669×328.8189 pt; all 7 font resources embedded.
- SVG: live text, no embedded raster, no external href, palette restricted to one navy root plus neutrals.
- Final-size border, quadrant occupancy, tonal range, greyscale neutrality, footer, and top-right blossom checks: PASS.
- Negative tests for source-hash drift, false payment-gate closure, simultaneous-time requirement, and strip-to-whole-shell promotion: PASS.

## Human visual checks

- Panel titles, axes, exact fractions, and endpoint qualifications are legible.
- No detected callout, footer, title, or canvas-edge collision.
- Packets 1, 2, and 3 remain distinguishable by circle/square/diamond and fill encodings.
- Panel B places `inf` before `sup`, says that the deletion set is fixed before time selection, and visibly permits different witness times.
- Panel C displays the exact payment rate, maximum two-strip rate, and their strict positive gap; its upper comparison is explicitly restricted to the two strip integrals.
- Panel D visibly separates PROVED, NOT PROVED, NO-GO, and NEXT X.52.
- The two-coordinate `T_*` result, open payment-normalized gate, and absence of a whole-shell upper bound are all visible.
- No novelty claim is made.
- Required scope label appears verbatim:
  `ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY`.

**ANALYTIC SCHEMATIC. DERIVED ANALYTIC VALUES. NOT PDE DATA. NOT DNS. NOT CLAY.**
