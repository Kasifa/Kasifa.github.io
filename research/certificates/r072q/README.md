# R0.72Q arbitrary-phase exact-audit bundle

This directory is the source-stage scaffold for the formal R0.72Q machine
audit.  The analytic proof is `research/r072q_report-source.md`.  The two
programs audit only the finite exact ledger used by that proof; they do not
replace the continuum root-isolation argument, the fixed-`M` Morse proof, or
the enhanced-dissipation theorem.

The declared positive class fixes a finite carrier ceiling `M`, allows
arbitrary relative phases, and assumes

```text
Q_2 = sup_y sum_{m=2}^M m^2 |beta_m(y)| <= 1/2.
```

The exact routes independently recover `Q_1 <= 1/4`, `Q_0 <= 1/8`, exactly
two critical points, and the physical Coble-shear contract
`(r,C_0,C_1)=(pi/12,81,36)` on `0 <= y <= 1`.  They separately retain the
sharper normalized-profile away constant `C_1=12`, the fixed-`M`
third-derivative and slow-time ledgers, and the exact 1:2 caustic

```text
z(phi) = (1/8) exp(-3 i phi) - (3/8) exp(-i phi).
```

In particular, the caustic has radial range `[1/4, 1/2]`, so the open disk
`|z| < 1/4` is a sharp phase-uniform nondegeneracy disk for the 1:2 family.
The wall is a Morse-applicability boundary, not evidence that enhanced
dissipation fails there.

## Independent routes

The producer source is `research/r072q_exact_audit.py`.  It uses Python
`fractions.Fraction` arithmetic and writes exactly:

- `producer-config.json`, `producer-payload.json`, and
  `producer-result.json`;
- `producer-progress.ndjson` and `producer-resource.ndjson`; and
- `producer-monitor.log`.

The independent source is `research/r072q_independent_audit.mjs`.  It uses a
separate JavaScript `BigInt` rational implementation, does not import or read
the Python route, and writes the corresponding six `independent-*` files.
The comparator is the only program that reads both payloads.  It requires
exact JSON equality and writes `crosscheck.json`.

The formal archived command uses `M=2` as the exact reference instance for
the 1:2 caustic.  This finite instance is not a proof for every fixed `M`;
the general fixed-`M` result remains the analytic theorem in the report.  The
programs accept any common integer `M >= 2` for additional audit runs.

## Reproduction and sealing

Run the exact commands in `command.txt` from the repository root only after
the report and all three audit programs have been committed and the tracked
worktree is clean.  The formal comparator command deliberately omits
`--allow-unsealed-source`.  A temporary pre-commit comparison may use that
flag, but `build_hashes.py` rejects its output.

`build_hashes.py` runs last.  It rejects a failed or temporary crosscheck,
dirty or untracked source lineage, mismatched commits or carrier ceilings,
incomplete or unexpected artifacts, symlinks, subdirectories, and stale
files before atomically replacing `SHA256SUMS`.

## Frozen lineage

Source and certificate commits are intentionally pending at this source
stage.  Do not add a source id until the report, both independent routes, and
the comparator are frozen.  Do not claim a certificate commit until all
generated artifacts and the flat SHA-256 ledger are archived in an immutable
commit.

## Claim boundary

The certificate verifies finite exact identities and claim wiring.  It does
not prove the continuum trigonometric argument, uniformity as `M` grows, a
result without the `Q_2 <= 1/2` jet-dominance condition, arbitrary common-band
carrier sets, fixed-geometry arbitrary-coupling closure, passage through the
caustic, general three-dimensional continuation, or the Clay Millennium
problem.  Those claims remain open.
