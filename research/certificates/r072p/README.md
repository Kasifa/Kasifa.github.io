# R0.72P two-carrier exact-audit bundle

This directory is the scaffold for the formal R0.72P machine-audit bundle.
The analytic proof is `research/r072p_report-source.md`. The programs audit
finite exact algebra used by that proof; they do not replace the
full-superposition semigroup theorem or its proof-level uniformity argument.

The two routes have seven narrow jobs:

1. verify the factor `epsilon = 2 |delta| a / R^2` on the affine invariant
   row `{(nR,q_*):n∈Z}` (isomorphic to `R Z`) and retain both cell shifts `1`
   and `2`;
2. recover the exact factor bounds `1/2` and `3/2`, the two fixed critical
   points, the displayed shape constants, and all derivative bounds;
3. check the exact slow-time wall `eta <= 1/16`;
4. verify the fourth-order jets at `lambda = +/-1/4` while keeping the result
   at the level of a Morse/applicability wall;
5. require both the integrated and terminal clauses in the propagation claim
   contract;
6. keep arbitrary common-band patterns and growing carrier count explicitly
   open; and
7. recover `N=2`, `B=2`, `p^2=1/2`, the `epsilon^(11/6)` numerator, and the
   fixed-pattern powers of `2` in the physical ledger.

The enhanced-dissipation constants are uniform in `lambda_minus` and may
depend only on the fixed upper shape class / `lambda_max`. The separate
physical-amplitude balance may depend on `lambda_minus`; the audit contract
does not conflate these dependencies.

## Independent routes

The producer source is `research/r072p_exact_audit.py`. It uses Python
`fractions.Fraction` arithmetic and writes files prefixed `producer-`.

The independent source is `research/r072p_independent_audit.mjs`. It uses a
separate JavaScript `BigInt` rational implementation and writes files prefixed
`independent-`. It does not import or read the Python route.

The exact payload consists of:

- `*-exponents.json`: cell, shape, slow-threshold, claim-contract, Morse-wall,
  and exponent ledgers;
- `*-shape.csv`: independently derived rational shape constants;
- `*-wall.csv`: the two exact fourth-order wall jets;
- `*-result.json`, `*-config.json`, progress/resource NDJSON, and monitor logs;
- `crosscheck.json`: structural equality and formal source-lineage gate.

The scripts record whether the audit sources are tracked and whether tracked
files differ from `HEAD`. A temporary pre-commit run may pass the comparator
only with `--allow-unsealed-source`. Such a crosscheck is explicitly barred
from `SHA256SUMS`; the formal commands in `command.txt` do not use that flag.

## Reproduction commands

Run the exact commands archived in `command.txt` from the repository root,
after the analytic report and all three audit sources have been committed and
the tracked worktree is clean. `build_hashes.py` is deliberately last: it
rejects temporary/unsealed crosschecks, incomplete payloads, inconsistent
source commits, symlinks, and stale files.

## Frozen lineage

Source and certificate commits are intentionally pending. Do not replace this
paragraph with a source id until the report and audit programs are frozen, and
do not claim a certificate commit before the generated bundle has been
archived in an immutable commit.

## Claim boundary

The certificate audits finite exact identities and claim wiring. In
particular, it does not prove the Coble--He semigroup estimate, the continuum
shape lemma, family-uniform theorem constants, enhanced dissipation beyond the
Morse wall, a result for arbitrary carrier patterns or growing `N`,
fixed-geometry arbitrary-coupling closure, multiscale absorption, or a
continuation theorem for general three-dimensional Navier--Stokes solutions.
The Clay Millennium problem remains open.
