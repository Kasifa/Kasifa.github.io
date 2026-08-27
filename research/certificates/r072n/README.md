# R0.72N dissipative one-carrier finite-audit bundle

This directory is the formal finite certificate bundle for R0.72N.  The
analytic proof remains in `research/r072n_report-source.md`; no numerical
artifact in this directory replaces the full-chain moment argument or the
published enhanced-dissipation theorem used there.

The finite bundle has four narrower jobs:

1. check declared instances of the moment barrier
   `max D <= max(1,(2 sigma)^(2/3))`;
2. sample the critical-log action, its physical lift, and the failure of the
   proposed action-poor ratio;
3. compare the scalar danger-screen proxy with the true first-row cubic; and
4. corroborate common observables through two independently implemented
   finite evolutions.

## Formal routes and artifacts

### Producer route

Source: `research/r072n_exact_audit.py`.

The producer evolves the angular generating function with an FFT
exact-mixing/diagonal-heat Strang split on the uniform coordinate
`r=y^(2/3)`.  Its formal outputs are:

- `config.json` and `environment.txt`;
- `producer-dissipative.csv`;
- `producer-progress.ndjson` and `producer-resource.ndjson`;
- `producer-monitor.log`; and
- `result.json`.

### Independent route

Source: `research/r072n_independent_audit.py`.

The independent route evolves a finite real Fourier chain with a separately
written diagonal-heat/fourth-order exponential Strang split.  It must not
import the producer or read producer artifacts.  Its formal outputs are:

- `independent-config.json` and `independent-environment.txt`;
- `independent-dissipative.csv`;
- `independent-progress.ndjson` and `independent-resource.ndjson`;
- `independent-monitor.log`; and
- `independent-result.json`.

Both routes use the same ten declared coupling values from `16` through
`32768`, but have different state representations, spatial truncations, and
time-step refinements.  Neither route uses randomness, so no seed artifact is
required.

### Crosscheck

Source: `research/r072n_compare_audits.py`.

`crosscheck.json` compares the common fields

- `maxMoment`;
- `action`;
- `liftedAction`;
- `actionPoorRatio`;
- `tOverV`; and
- `cubic`.

Every producer-independent relative difference must be at most `0.005`.
The finite moment check permits only the declared `0.002` relative numerical
slack above the analytic barrier.  Each route must also keep its spatial
boundary/tail diagnostic below `1e-18`, and the last sampled
`cubic/sqrt(sigma)` value below `0.2`.  These are certificate acceptance
thresholds for the declared binary64 grids, not constants in the analytic
theorem.

## Reproduction commands

Run from the repository root, using the scientific Python environment that
provides NumPy:

```text
python3 research/r072n_exact_audit.py --output-dir research/certificates/r072n
python3 research/r072n_independent_audit.py --output-dir research/certificates/r072n
python3 research/r072n_compare_audits.py --certificate-dir research/certificates/r072n
python3 research/certificates/r072n/build_hashes.py
node --test tests/r072n-dissipative-carrier-gate.test.mjs
```

Archive the first four commands verbatim in `command.txt`.  Build
`SHA256SUMS` only after every other formal file is final.  The ledger is
sorted by file name, uses SHA-256 over exact bytes, and deliberately does not
hash itself.

## Lineage placeholders

- Source commit: `5e57e5473ef95f533bdb71e2fca47aff67d3c6d3`
- Certificate commit: `1da2a29ff8b95ba82a09244715d706a088f80807`

At the formal freeze, the source commit must be the clean commit from which
both audit routes were run and must agree with every archived `gitCommit`
field.  The certificate commit is the immutable commit that first archives
the completed producer, independent, and crosscheck payloads.  A subsequent
lineage/freeze commit may replace this placeholder and rebuild `SHA256SUMS`;
the bundle must not try to encode its own current commit recursively.
Replace the placeholders only with full 40-hex commit identifiers; do not
infer either value from an uncommitted worktree.

## Finite-diagnostic boundary

The moment barrier, the critical-log action lower bound, the scalar-screen
asymptotic order, and the `O(a^2 sqrt(sigma))` true-cubic bound are analytic
claims proved or derived in the report.  In particular, the cubic upper bound
comes from applying Coble--He Theorem 1.2 to the rescaled generating
function and then using exact Parseval and `sigma dy=dt`; decreasing finite
curves do not prove that exponent.

The CSV and JSON files are finite binary64 corroboration, not interval
certificates, continuum asymptotic proofs, or DNS.  They do not prove the
numerically suggested logarithmic cubic law, a matching action or moment
asymptotic, a multi-carrier estimate, completion of the R0.72L physical
absorption ledger, a continuation criterion for arbitrary three-dimensional
solutions, or resolution of the Clay Millennium Problem.
