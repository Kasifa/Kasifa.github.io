# R0.74T schedule-invariant dwell-barrier figure archive

This directory is the formal 25-file **preseal** archive for the Step 19
schedule-invariant outer-lobe coercivity result. It visualizes four exact or
derived-analytic statements from equations (T.9)--(T.43): an admissible pair
of disjoint lobe windows inside one terminal slab, the atomic factors yielding
the exact constant `2 sqrt(2)`, the positive logarithmic reserve for unit
dwell, and the corresponding exponentially small necessary dwell ceiling.

The mathematical sources, certificate, and audits are frozen at core commit
`b120598d36140385676bb4a9922d46abcdff0ba4`. Their Git blob object IDs and
SHA-256 digests are locked in `config.json`.

## Scope

Panel A is an exact scheduling schematic with a compressed gap, not a plot to
physical time scale. Panel B is exact algebra. Panels C--D contain
deterministic values evaluated from displayed analytic formulas for an
explicit parameter path. None of the panels is DNS, measured PDE data, a
numerical Navier--Stokes experiment, or a Clay-problem claim.

## Reproduction

Use Python 3.12.13 and the exact packages in `requirements.txt`, then follow
`command.txt`. `plot.py` verifies the live preseal source hashes before
writing all 11 raw/result files. `validate.py` independently regenerates the
CSV, checks the exact rational constant and schedule inequalities, verifies
SVG/PDF/600-dpi PNG properties, and checks the final-size, grayscale, and
independently rasterized PDF QA assets.

## Two-stage Git seal

The preseal records `PENDING_FIGURE_SOURCE_COMMIT`; it never guesses a future
figure commit. After the 21 source/raw figure files are committed, run the
final reseal with that actual figure-source commit. Only
`SHA256SUMS`, `manifest.json`, `qa-report.md`, and `validation.json` are
rewritten by the final figure seal.

The archive partition is exactly 10 source files, 11 raw/result files, and
4 metadata files. The mathematical core is already fully bound.
