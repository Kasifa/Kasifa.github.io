# R0.74H — final-source rebind audit

**Audit date:** 2026-09-02
**Verdict:** `R074H_FINAL_SOURCE_REBIND_PASS`
**Method:** local byte-level inspection only; no network search

## 1. Final source and analytic-slice binding

The final source exists at

    research/r074h_collar_flux_two_regime_closure.md

and its current SHA-256 is

    8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1.

This exactly matches the designated final-main digest.

The Sections 1--9 slice was recomputed directly from the current source
bytes.  The slice begins with the byte sequence

    ## 1. Frozen frames, payments, and the pre-acceleration ledger

and ends immediately before

    ## 10. Verification and freeze record

with no whitespace normalization or Markdown parsing.  Its half-open byte
range is `[2181, 20204)`, its length is 18,023 bytes, and its SHA-256 is

    56d5e8487224348e9ce0282c4784a57921f70e0d277f261b705993e4e4b3b3ee.

This exactly matches the frozen Sections 1--9 digest.  Hence the analytic
body bound by that digest is byte-identical across the final status/Section
10 promotion.

## 2. Section 10 existence and current identity

Section 10 is not a separate source file in this freeze.  It is the unique
final section of the main source above.  The heading occurs exactly once,
at byte offset 20,204.  The containing file exists and has the final-main
SHA-256 recorded in Section 1 of this audit.

For additional localization, the raw byte slice from the Section 10 heading
through end of file is 3,391 bytes and has SHA-256

    e97a560e12f0f0ea9eeaf7aa5660fd7be24312f1cee874f2af545655a21cf06f.

This Section-10 slice digest is an audit locator, not a replacement for the
full-source digest.

## 3. Pre-promotion source and old-copy evidence boundary

The retained pre-promotion full-source identifier is

    4140879118b501e0891646632aedb35e796434eb294454c28d35f4f7843c5aea.

No byte-identical old full-source copy with that digest is present in the
current worktree.  The digest is recorded in the final source, but the old
byte sequence itself is not available here for an independent full-file
recomputation.  Accordingly, this audit does **not** claim:

1. a byte-for-byte comparison of the two complete full-source files;
2. independent recovery of the old status block; or
3. independent recomputation of the retained pre-promotion full-file hash.

The affirmative rebind is narrower and exact: the currently recomputed
Sections 1--9 digest equals the designated frozen analytic-slice digest,
while the current complete file equals the designated final-main digest.
Continuity with the unavailable old copy relies on the retained digest as
the supplied freeze identifier.

## 4. Section-10 artifact inventory

Every non-figure artifact named by the Section 10 verification record, plus
the frozen gap matrix, was tested as a regular file and hashed from its
current bytes.  No digest below was copied from an earlier audit.

| Role | Current path | Exists | Current SHA-256 |
|---|---|---:|---|
| energy-identity audit | `research/r074h_energy_identity_independent_audit.md` | PASS | `a63377c01ddaf8aaa07f99befc05696abff86e69854ca9d8ac76c748afd4d104` |
| packet-flux audit | `research/r074h_packet_flux_independent_audit.md` | PASS | `9330181d9288ca50ab806f31d96ca76223d3248026561950f4e21535f0374649` |
| scaling-and-claim audit | `research/r074h_scaling_and_claim_audit.md` | PASS | `a6dd7f5e1efae508ed332acfb7b3af3170668a9b12e95a1eec167ee90cad3be2` |
| full-note adversarial audit | `research/r074h_full_note_adversarial_audit.md` | PASS | `e42e2a6a64b689c4477a7814d58cfd273e25a881724a76afbb2c6bcf139dab32` |
| certificate producer | `scripts/r074h_collar_flux_certificate.py` | PASS | `acce024b8dd78ba727e3ec8176a308dc53ecc34b7bdaf57b6c48e5d1e1a5c6e4` |
| certificate JSON | `research/r074h_collar_flux_certificate.json` | PASS | `783591f3da880ec9182be89c585eb732e35d5842b7d196dc2ae4e35b6c0d2ba4` |
| certificate report | `research/r074h_collar_flux_certificate_report.md` | PASS | `c675d4efea3edfdd3e77844b54ae34a7721902a5f03d6ace72e3dc09ce85bc27` |
| independent Ruby implementation | `scripts/r074h_collar_flux_certificate_independent.rb` | PASS | `9004240b7a041001fb853eb9963ed10cc768f2e2a3c4b675d1187167c051a39f` |
| independent certificate audit | `research/r074h_certificate_independent_audit.md` | PASS | `3760692601b27e40fcd219aabe9ed612c10e8e1063100b58b6208055ba969545` |
| primary-source report | `research/r074h_report-source.md` | PASS | `d72917b04e067113f419f89bc009861f264d859e80cb22dce1276c6dbfbc2c47` |
| primary-literature boundary | `research/r074h_primary_literature_boundary.md` | PASS | `722e338f4cdd729f3a8756b886c920f17d08e08592bbce6ed9561179d6afbadf` |
| independent literature audit | `research/r074h_primary_literature_independent_audit.md` | PASS | `f5c0572c16f26e5066edbf07db8347d591815fe461ffeb81b8c95e2a4ac39f81` |
| gap matrix | `research/r074h_gap_matrix.md` | PASS | `3cc23977e865596eb679cceef6260ce7909204da785168efd42663fef9841251` |

The requested current hashes for the figure package's binding and primary
publication outputs are:

| Artifact | Current path | Exists | Current SHA-256 |
|---|---|---:|---|
| checksum ledger | `research/figures/r074h/fig-r074h-collar-flux-repair/SHA256SUMS` | PASS | `6c1e02e2f2322a25bded0b948f7383a067de4bd247486bd133d68e77e77bf2ca` |
| manifest | `research/figures/r074h/fig-r074h-collar-flux-repair/manifest.json` | PASS | `0bb323ce916e406c13c17559920699a2dee33bce3041f6dfd3432ad6b6296571` |
| validation record | `research/figures/r074h/fig-r074h-collar-flux-repair/validation.json` | PASS | `66bc780f94342277a9efb47ad9c33b88f455218e5b64367f3237a2ffc977b655` |
| exact source data | `research/figures/r074h/fig-r074h-collar-flux-repair/source-data.csv` | PASS | `6106a477847cb60765fa48b929aaabe76be14c4c3b9cc1245b19aaa115aa7217` |
| editable SVG | `research/figures/r074h/fig-r074h-collar-flux-repair/figure.svg` | PASS | `9989d22ac20c619f0f5da285108676318584e53b194fd13abe4a9456c97b09c3` |
| journal PDF | `research/figures/r074h/fig-r074h-collar-flux-repair/figure.pdf` | PASS | `80441f23ea0a056fdc7a22ee39bc3a452ce39ff11725867b4304b025791d55a0` |
| 600 dpi PNG | `research/figures/r074h/fig-r074h-collar-flux-repair/figure.png` | PASS | `876b88609a12dcda7a88fbffd1f97fcbaf2749251060fbe148ac2b221e8b6c9a` |

All twenty listed artifacts exist at the displayed paths.  The figure
checksum ledger was also executed from its package directory; all 23 listed
entries verified.

## 5. Journal-figure package

The package

    research/figures/r074h/fig-r074h-collar-flux-repair/

contains exactly 24 regular files recursively.  It contains no
`__pycache__` directory and no `.pyc` or `.pyo` artifact.  Its independent
validation record is `PASS 69/69`, and every listed entry in its
`SHA256SUMS` verifies against the current package bytes.

## 6. Claim-boundary audit of the promotion

The promoted status block reports proof/audit/certificate/literature/figure
verification states.  Section 10 records hashes, audit locations,
certificate scope, literature-search limits, figure QA, and the freeze
boundary.  These additions do not alter the equations, hypotheses,
theorems, corollary, explicit-family diagnostic, or open-problem inventory
in Sections 1--9; their unchanged byte digest independently confirms that
fact.

The final source continues to restrict the mathematical result to a
smooth-periodic, unforced, one-scale positive-size estimate.  It explicitly
leaves weak-solution stability, independent flux payment, scale iteration,
epsilon regularity, continuation, singularity exclusion, global
regularity, novelty, and priority open or unclaimed.  The phrases
`FROZEN`, `PASS`, and `PROVED` describe the verified status of the stated
R0.74H result; they do not promote it to any stronger theorem.

No strengthened mathematical claim was introduced by the status or Section
10 promotion.  In particular, there is no Millennium-problem claim.

## Final verdict

**FINAL SOURCE REBIND PASS**, subject to the explicit old-copy evidence
boundary in Section 3.  The final full-source hash, the raw Sections 1--9
hash, Section 10 existence, the 24-file clean figure inventory, and the
non-strengthening claim boundary all pass.

**NOT CLAY.**
