# R0.74U intrinsic certified-residence figure archive

This directory is the formal two-stage journal-figure archive for R0.74U
Step 20. The figure visualizes four statements from equations (U.11)--(U.45):
the symmetric centre corridor and its terminal-slab truncation, the kinematic
product that gives the `L_i R^3` time scale, the strict distinction between a
two-sided geometric-corridor estimate and a lower-only completed-clock
superlevel estimate, and the conflict between certified dwell and the
necessary exponentially short bounded-payment dwell.

The mathematical authority is core commit
`d74e7b297928147334136f4c3cb29c5226d66381`. The theorem-note blob is
`3359036a04afd87eb51123d9b9d9a321a5bfc898`, with SHA-256
`e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99`.
`plot.py` and validation fail closed if this commit/blob/content chain drifts.

## Scope

Panels A--C are exact analytic schematics. Panel D contains deterministic
values evaluated from the displayed analytic formulas on the explicit path
`d_L = log(L_1)`, `L_2 = 2L_1`, with the illustrative necessary-bound
constant `C = 1`. No panel is PDE measurement, DNS, a fitted model, or a
numerical Navier--Stokes experiment. The upper residence estimate belongs
only to the certified geometric corridor. For the full completed-clock
superlevel set the proved statement is inclusion plus an `Omega(L_i R^3)`
lower bound; there is no converse inclusion and no upper bound. NOT CLAY.

## Reproduction

Use a bundled Python 3.12.13 executable and a separate version-pinned
dependency directory whose installed metadata matches `requirements.txt`,
then follow `command.txt`. Do not assume that a generic bundled Python package
root is this pinned directory. `plot.py` verifies both the runtime versions
and the frozen note before writing all 11
raw/result files. `validate.py` independently regenerates the CSV and every
displayed value, checks exact rational identities and claim-boundary labels,
verifies SVG/PDF/600-dpi PNG properties, and compares final-size, grayscale,
and independently rasterized PDF QA assets.

## Two-stage Git seal

Stage 1 is exactly 21 files: 10 source files and 11 raw/result files. Preseal
QA writes no archive metadata. Commit those 21 files as one figure-source
boundary. Only after that commit exists may the final seal add the four
metadata files `SHA256SUMS`, `manifest.json`, `qa-report.md`, and
`validation.json`. The intended final partition is therefore 10 source + 11
raw/result + 4 metadata = 25 files.
