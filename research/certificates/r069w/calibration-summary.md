# R0.69W calibration history

Calibration runs were used only to tighten validated enclosures and choose the
formal grid.  A calibration that did not close the target inequality was never
reported as a mathematical result.

1. The complete P18 run at source `e383c3f` failed to certify the quadratic
   discriminant.  It produced
   `Delta=[-0.00965065009764447, 0.008180217845982413]`.  The endpoint interval
   at \(j=-2\) was already strictly negative, but the full family claim did not
   pass.
2. Monotone cutoff endpoint ranges, certified cubic-Hermite value
   interpolation, and exact dyadic distance nodes removed several artificial
   effects.  The dominant outer-transition width near right index 1588,
   however, remained essentially unchanged.
3. Raising the distance-moment power from P18 to P21 reduced the row-17 center
   width from about `8.9645e-5` to `1.12145e-5`, but left the `rr` and `ss`
   Taylor-average widths near `3.344e-6` and `1.6457e-5`.  Grid refinement alone
   therefore did not address the main derivative dependency.
4. Source `db8b319` separated certified point derivatives at a radial-box
   center from whole-cell derivative ranges used for remainders.  In a
   same-P18, same-worker, same-row comparison, the `rr` width fell by a factor
   of `3621.324887802195` and the `ss` width by `7805.038556709319`.
5. P22 was selected for the formal run because the remaining dominant
   distance-primitive center width scales down with the moment grid.  The
   resulting 20-worker certificate passed with discriminant upper endpoint
   `-0.00039732714404764783`, leaving a substantial strict margin.

The machine-readable row-17 records and improvement factors are preserved in
`calibration-comparison.json`.  Rejected raw run directories remain on the DGX
host and are not inputs to the formal merge.
