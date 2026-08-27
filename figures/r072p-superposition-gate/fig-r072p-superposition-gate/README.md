# R0.72P formal figure source scaffold

This directory contains source code only for the proposed 2 x 2 journal
figure accompanying the R0.72P two-carrier superposition theorem. Formal
outputs are intentionally absent until the analytic report and both audit
routes are frozen.

The figure separates four statements:

- Panel A records the exact reduction of the carriers `(R, 2R)` on one
  affine residue row to the full shear
  `W(y, phi) = exp(-y) cos(phi) + lambda exp(-4y) cos(2 phi)`. Each pair of
  signed shifts contributes the factor `2 cos(m phi)`; the declared
  definition of `epsilon` absorbs that factor. `B=2` does not cancel it.
- Panel B displays the positive shape bracket for `|lambda| <= 1/8` and the
  resulting fixed critical set `{0, pi}`. These are analytic inequalities,
  not sampled evidence for the theorem.
- Panel C displays the exact time-slice Morse wall
  `|lambda| = exp(3y) / 4` and the strictly separated safe cone. The wall is
  a theorem-applicability boundary, not a counterexample to enhanced
  dissipation.
- Panel D shows that the R0.72O conditional physical ledger becomes proved
  only in the declared R0.72P class: `N=2`, `B=2`,
  `p=1/sqrt(2)`, a fixed nonzero lambda cone, and one affine invariant row.
  Its curve is the fixed-polynomial-coupling asymptotic representative
  `L_(R,epsilon) asymp 1+log R`; the exact ledger retains
  `L_(R,epsilon)`, so the curve is not an exact window for every epsilon.

All dense curves are direct formula evaluations. The package runs no PDE
simulation, regression, exponent fit, or interpolation. Producer,
independent, and crosscheck certificates enter only through required runtime
lineage parameters, including both route configurations; the source scaffold
does not guess their final paths. A passed temporary/unsealed crosscheck is
rejected.

The six explicit lineage paths induce a seventh, mandatory lineage object:
`research/certificates/r072p/SHA256SUMS`. The figure independently verifies
that all five runtime certificate JSON files come from that canonical flat
directory; ledger rows are valid, unique, byte-sorted, and digest-correct;
the ledger exactly covers every directory file except itself and a regular
`.DS_Store`; and no symlink or subdirectory is present.

The intended archival masters are an editable-text SVG, a one-page PDF, and
a 600 dpi PNG at 177.8 x 132.08 mm. Final-size, grayscale, and PDF-raster QA,
validation, byte-identical publication, and manifest sealing follow the
R0.72O journal package structure.

The formal workflow first runs `validate.py --automatic-only`, then stops for
explicit `view_image` inspection of all three QA surfaces. The visual
environment flag may be set only after that inspection. The manifest builder
reruns final custom validation, rejects any extra package entry, verifies that
validated assets did not change, and is followed by the repository-generic
figure validator and flat `SHA256SUMS` check.

See `command.txt` for the formal runtime placeholders. A formal build must
use a frozen report, passed producer and independent certificates, and a
passed non-temporary crosscheck. The formal manifest verifies Git blob
identity for the report/audit programs at the source commit and the five
runtime certificate JSON files plus `SHA256SUMS` at the certificate commit;
the figure build commit must equal that certificate commit. Do not treat a
source-only syntax check as visual QA.

Formal plotting and formal manifest sealing both execute `git diff --quiet`
and `git diff --cached --quiet`; tracked or staged drift is fatal while
untracked generated outputs are allowed. The plot additionally binds every
figure-package source to its HEAD Git blob and records
`verifiedTrackedTreeClean=true`; the manifest rebinds those sources to the
certificate commit.
