# R0.74Z figure QA report

Status: **PASS**

Visual inspection confirmation: **YES**.  The explicit seal flag records that
`qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png` were inspected at
actual size after the final render.

## Scope and provenance

- Artifact: `fig-r074z-remote-persistence-gate`
- Seal: local SHA-256 precommit seal; no Git commit/blob seal is claimed.
- Mathematical input SHA-256: `bb766da4002da760c35185294081f80df97c349ea08b198a5f76db31663aaf6a`.
- Independent primary audit SHA-256:
  `6b867551bce840cb382cd13cb2ff298affbf0c0d8b1357a8163c5cedc9bace08`;
  verdict PASS, blocker count 0.
- Literature audit SHA-256:
  `8e5346ecf3c2beef4a620e0844e790703b628388ca7f0a6997aae88818caa82f`;
  bounded primary-source non-hit only.

## Automated checks

- Exact rational identities, two fourth-root shifts, strict threshold, and complexity addition: PASS.
- Source-data regeneration and 104-row semantic ledger: PASS.
- Deterministic two-render comparison: PASS (18 files).
- Publication PNG: 4204×2740 pixels at nominal 600 dpi.
- Three QA exports: 2102×1370 pixels at nominal 300 dpi.
- PDF: one page, 504.5669×328.8189 pt; all 5 font resources embedded.
- SVG: live text, no embedded raster, no external href, palette restricted to one navy root plus neutrals.
- Final-size border, quadrant occupancy, tonal range, greyscale neutrality, footer, and top-right blossom checks: PASS.
- Negative tests for source-hash drift, critical-layer closure, unconditional persistence, W-kinetic-to-full-clock promotion, accumulated-row closure, and novelty: PASS.

## Human visual checks

- Panel titles, axes, exact fractions, and endpoint qualifications are legible.
- No detected callout, footer, title, or canvas-edge collision.
- Panel A shows the exact `Gamma -> Gamma^(1/4) -> Gamma^(1/16)` ladder and the doubled-radius shell identity.
- Panel B visibly separates the strict `limsup kappa_L < kappa_*` theorem from the open critical layer.
- Panel C uses dashed/solid structure and direct labels to show that persistence is conditional on endpoint preservation, Z.22, and moving-strip all-winding uniformity; the complexity rate is visibly necessary, not sufficient.
- Panel D visibly separates PROVED, CONDITIONAL, OPEN, and NEXT Z.39.
- Full-clock Y.57, accumulated rows, the critical layer, and arbitrary exponentially ill-conditioned finite families remain visibly open.
- No novelty claim is made.
- Required scope label appears verbatim:
  `ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NO NOVELTY CLAIM | NOT CLAY`.

**ANALYTIC SCHEMATIC. DERIVED ANALYTIC VALUES. NOT PDE DATA. NOT DNS. NO NOVELTY CLAIM. NOT CLAY.**
