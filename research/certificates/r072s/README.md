# R0.72S exact singular-strata audit bundle

This directory starts as the source-stage scaffold for the formal R0.72S
machine audit.  The analytic proof is
`research/r072s_report-source.md`.  The two programs machine-check finite
rational identities, crossing-power identities, nonzero jets, representative
endpoint evaluations, and sign/monotonicity guards.  The continuous argument
in the report—not this finite computation—deduces event uniqueness, global
critical-point counts, simplicity away from collision, and transversality.

The formal result has three pieces:

1. the marked incidence preimages split exactly into local
   `A2/A3/A4/A5` types;
2. the four coefficient directions have jet determinant `5400`, giving local
   codimensions one through four;
3. exact finite inputs for the two heat paths crossing at `y=log(2)`; the
   report's continuous proof turns those inputs into counts `4/3/2` for the
   generic A2 path and `4/2/2` for the real-even A3 path.

The Python producer uses `Fraction` arithmetic and a permutation determinant.
The JavaScript route has its own BigInt rational implementation and a Bareiss
determinant.  Neither route reads the other source or output.  The comparator
is the only program that reads both payloads.

Run `command.txt` from the repository root after the report, both audit
programs, the comparator, and this scaffold are committed and the tracked
worktree is clean.  The formal command does not use
`--allow-unsealed-source`.  `build_hashes.py` rejects temporary lineage,
failed checks, dirty or untracked sources, unexpected files, and symlinks.

The bundle does not certify a global embedded caustic stratification, all
incidence self-intersections, enhanced dissipation through a collision,
general three-dimensional Navier--Stokes regularity, or the Clay problem.
