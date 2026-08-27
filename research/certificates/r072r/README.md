# R0.72R quantitative 1:2:3 core exact-audit bundle

This directory is the source-stage scaffold for the formal R0.72R machine
audit.  The analytic proof is `research/r072r_report-source.md`.  The two
programs audit only its finite exact ledger; they do not replace the
continuum root-localization argument, Coble--He's enhanced-dissipation
theorem, or a global four-dimensional caustic decomposition.

The declared coefficient class is

```text
|z2-3/20| <= 1/100,    |z3| <= 1/1000.
```

It has nonempty interior in four real dimensions and starts strictly outside
the old sufficient cone: `Q2(0)>=14/25>1/2`.  Every heat path crosses the old
`Q2=1/2` boundary exactly once while retaining two nondegenerate critical
points.  On `0<=y<=1`, the physical shape contract is

```text
(r,C0,C1)=(pi/48,144,240).
```

## Independent routes

The producer `research/r072r_exact_audit.py` uses Python `Fraction` arithmetic
and an exact integer Bareiss resultant.  The independent route
`research/r072r_independent_audit.mjs` implements its own JavaScript `BigInt`
rationals and determinant.  Neither route reads the other source or output.
The comparator is the only program that reads both canonical payloads.

Both routes check the cone-exit and heat-crossing ledgers, all rational shape
margins, the spatial and slow-time derivative budgets, the complex incidence
jet identities, and the exact real-slice discriminant factorization.  The
factorization is verified on an exact 11 by 11 tensor grid after an explicit
degree-at-most-ten bound in each coefficient.

## Reproduction and sealing

Run `command.txt` from the repository root only after the report, audit
programs, and comparator have been committed and the tracked worktree is
clean.  The formal comparator deliberately omits `--allow-unsealed-source`.
A temporary pre-commit comparison may use that flag, but `build_hashes.py`
rejects the temporary result.

`build_hashes.py` runs last.  It rejects failed checks, temporary lineage,
dirty or untracked sources, mismatched commits, incomplete or unexpected
artifacts, symlinks, and stale files before atomically replacing the sorted
SHA-256 ledger.

## Claim boundary

The certificate does not prove the continuum trigonometric theorem, a full
chamber classification, optimality of the polydisc, enhanced dissipation
through a caustic, arbitrary time-dependent phases, a uniform third-carrier
amplitude floor, general three-dimensional continuation, or the Clay
Millennium problem.

