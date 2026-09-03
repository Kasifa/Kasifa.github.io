# R0.74T schedule-invariant dwell formal figure QA report

Status: **PASS**

- generated at UTC: `2026-09-03T01:37:47.026607+00:00`
- frozen mathematical core: `b120598d36140385676bb4a9922d46abcdff0ba4`
- bound frozen evidence blobs: `7`
- figure-source seal: `0433c129868ddf349c7b64d427747f590fa06898`
- exact inventory: 25 files = 10 source + 11 raw/result + 4 metadata
- deterministic-core regeneration: PASS, `18` hashes unchanged
- validation checks: `47` passed
- Panel A exact schedule records: `6`
- exact gap in window units: `1179645` times `R^3`
- exact Hölder coefficient: `2.828427124746190` = `2 sqrt(2)`
- exact positive margin: `603445/89413632`
- Panel C/D derived values: `121` each
- Panel C log-Lambda endpoints: `382147.326383`, `1799713.730191`
- Panel D log10-dwell-ceiling endpoints: `-248946.712683`, `-1172408.613041`
- Lambda/dwell identity maximum residual: `0.000e+00`
- PDF-versus-PNG mean absolute RGB difference: `5.887729`
- render wall time: `7.610222` seconds
- render CPU time: `1.059174` seconds

## Frozen-blob mapping correction

The source map was verified directly with `git ls-tree` at the frozen core.
The theorem-note blob is `b75cdf0ef33e014ab9b9511c84c54f4536db2b09`;
`ddadc9a39a65fd83a6465cc02200753985f23699` belongs to the certificate JSON.
An earlier transposed handoff label was corrected before preseal. No incorrect
mapping is present in `config.json`, this report, or the manifest.

## Visual QA

The 178 mm by 116 mm final-size image, grayscale conversion, and independent
PDF render were inspected.  The four panel titles, direct labels, markers,
axes, legends, scope badges, footer, and top-right research blossom are
legible.  No clipping or collision was accepted.  Line styles, marker shapes,
and tones preserve every comparison in grayscale.

## Scope

ANALYTIC SCHEMATIC · DERIVED ANALYTIC VALUES · NOT PDE DATA · NOT DNS · NOT CLAY.
The package does not upper-bound the full completed clock, prove the
fixed-deletion gate, prove global regularity, or solve the Navier--Stokes
Millennium problem.
