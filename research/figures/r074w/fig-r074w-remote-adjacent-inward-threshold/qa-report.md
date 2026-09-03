# R0.74W figure QA report

Status: **PASS**

Visual inspection confirmation: **YES**.  The explicit seal flag records that
`qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png` were inspected at
actual size after the final render.

## Scope and provenance

- Artifact: `fig-r074w-remote-adjacent-inward-threshold`
- Seal: local SHA-256 precommit seal; no Git commit/blob seal is claimed.
- Mathematical input SHA-256: `d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10`.
- Independent primary audit SHA-256:
  `66ec78f67bba64c555a92e9a616c477d702ebb200b48bbfc08a353bdfde5bb73`;
  verdict PASS, blocker count 0.
- Literature audit SHA-256:
  `ec6259d95990fd6a8357d9685cc3f17e300e672c1add911a5eb64c6291f3bb99`;
  bounded primary-source non-hit only.

## Automated checks

- Exact rational identities and strict packet-rate comparisons: PASS.
- Source-data regeneration and 210-row semantic ledger: PASS.
- Deterministic two-render comparison: PASS (18 files).
- Publication PNG: 4204×2740 pixels at nominal 600 dpi.
- Three QA exports: 2102×1370 pixels at nominal 300 dpi.
- PDF: one page, 504.5669×328.8189 pt; all 8 font resources embedded.
- SVG: live text, no embedded raster, no external href, palette restricted to one navy root plus neutrals.
- Final-size border, quadrant occupancy, tonal range, greyscale neutrality, footer, and top-right blossom checks: PASS.
- Negative tests for source-hash drift, false fixed-deletion closure, and packet-1/packet-2 scale confusion: PASS.

## Human visual checks

- Panel titles, axes, exact fractions, and endpoint qualifications are legible.
- No detected callout, footer, title, or canvas-edge collision.
- Survival, the band not classified by the uniform slab test, and sweeping remain distinguishable in greyscale by fill/hatch/weight; the exact `q(ell)` curve stays visible.
- Packet 1 and packet 2 remain distinguishable by circle/square and dashed/dash-dot encodings.
- Panel C is a dependency map and contains no synthetic trajectory.
- Panel D states that its curve is a leading analytic scale and that unknown
  `c` and `-CL_2` are omitted; it is not a finite-`L_2` lower certificate.
- The all-shell frozen-placement failure and the fixed-deletion-open boundary are both visible.
- Required scope label appears verbatim:
  `ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY`.

**ANALYTIC SCHEMATIC. DERIVED ANALYTIC VALUES. NOT PDE DATA. NOT DNS. NOT CLAY.**
