# R0.72O physical-reinsertion exact-audit bundle

This directory is the formal machine-audit bundle for R0.72O. The analytic
proof is `research/r072o_report-source.md`; the programs here audit the
exponent bookkeeping and a deterministic finite screen. They do not replace
the semigroup theorem, the local action-floor proof, or the analytic
inequalities in the report.

The bundle has four narrow jobs:

1. verify the physical lift from the raw enhanced-dissipation cubic to the
   normalized exponent `epsilon^(11/6)`;
2. verify the general exponent-transfer ledger, derive the conditional
   full-superposition `a^2 N^2 epsilon^(1/2)` scale from its five monomial
   factors, and recover the `p^(4/3)` bookkeeping;
3. verify the exact two-carrier degenerate-critical-point identity; and
4. compare old and enhanced-dissipation scalar screens around the declared
   one-carrier and worst-common-band windows.

## Independent routes

The producer source is `research/r072o_exact_audit.py`. It uses Python
`fractions.Fraction` monomial dictionaries and writes the files prefixed
`producer-`.

The independent source is `research/r072o_independent_audit.mjs`. It uses a
separately written JavaScript `BigInt` numerator/denominator implementation
and writes the files prefixed `independent-`. It does not import, execute, or
read the producer.

Both routes use exact rational exponents. Their floating-point window tables
use the same declared binary64 grid only so that
`research/r072o_compare_audits.py` can check independently evaluated screen
values. Equality of the old and new direct terms at `epsilon=1` is expected;
the strict improvement begins for `epsilon>1`.

`crosscheck.json` requires:

- structurally identical exact exponent ledgers after JSON parsing;
- identical exact degeneracy identities;
- at most `2e-12` relative difference on every shared finite-screen field;
- both routes to keep the general-`p` conclusion explicitly conditional on
  full-superposition integrated ED with constants uniform over the compared
  parameter and geometry family.

## Reproduction commands

Run from the repository root:

```text
python3 research/r072o_exact_audit.py --output-dir research/certificates/r072o
node research/r072o_independent_audit.mjs --output-dir research/certificates/r072o
python3 research/r072o_compare_audits.py --certificate-dir research/certificates/r072o
python3 research/certificates/r072o/write_environment.py
python3 research/certificates/r072o/build_hashes.py
```

The exact commands are archived in `command.txt`. Build `SHA256SUMS` only
after every other formal artifact is final. The hash ledger is sorted by
file name, hashes exact bytes, and deliberately excludes itself.

## Frozen lineage

- Source commit: `8fc31ff1a15e9754d1e02977707b50464c391778`
- Certificate commit: `af02960b39e05a921f1981468a6e0a04cb3247d2`

The source id equals the `gitCommit` recorded by both audit routes. The
certificate id is the immutable commit that first archived all dual-route
payloads. This final lineage update deliberately does not try to make a
commit recursively encode its own id.

## Claim boundary

The bundle audits algebra and deterministic finite values. It does not prove
enhanced dissipation, the critical-log action floor, an unconditional
multi-carrier theorem, a fixed-geometry arbitrary-coupling closure,
multiscale absorption, or a continuation theorem for arbitrary
three-dimensional Navier--Stokes solutions. The Clay Millennium problem
remains open.
