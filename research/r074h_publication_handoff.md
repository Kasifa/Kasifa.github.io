# R0.74H publication handoff — collar-flux repair and two-regime closure

## Purpose and immutable research snapshot

This is the research-side handoff for R0.74H.  The new, independent task
titled **发布任务** owns site integration and GitHub Pages deployment.  It
must not reuse an older publication task.  Research continues without
waiting for publication.

The frozen core research commit is

    5cd31fd8cde1574f02d9e9af3417686d2a8f8d9c

on branch

    codex/r073z-research.

Publication may translate, summarize, and typeset the result.  It must not
change the research files, recompute definitions, strengthen a theorem,
turn a one-sided bound into an equivalence, or remove an evidence boundary.

The release contains a smooth-solution one-scale theorem, three independent
analytic audit tracks, a full-note adversarial audit, a final-source rebind,
a 25-row exact certificate plus independent exact reconstruction, a bounded
four-paper primary-literature screen, a gap matrix, and a 24-file journal
figure package.  It is not an epsilon-regularity theorem, continuation
criterion, singularity-exclusion theorem, or solution of the Millennium
problem.  **NOT CLAY.**

## Frozen files and SHA-256

| Artifact | SHA-256 |
|---|---|
| `research/r074h_collar_flux_two_regime_closure.md` | `8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1` |
| `research/r074h_energy_identity_independent_audit.md` | `a63377c01ddaf8aaa07f99befc05696abff86e69854ca9d8ac76c748afd4d104` |
| `research/r074h_packet_flux_independent_audit.md` | `9330181d9288ca50ab806f31d96ca76223d3248026561950f4e21535f0374649` |
| `research/r074h_scaling_and_claim_audit.md` | `a6dd7f5e1efae508ed332acfb7b3af3170668a9b12e95a1eec167ee90cad3be2` |
| `research/r074h_full_note_adversarial_audit.md` | `e42e2a6a64b689c4477a7814d58cfd273e25a881724a76afbb2c6bcf139dab32` |
| `research/r074h_final_source_rebind_audit.md` | `f0aef5522c7201250f625418275e57512f85309f50ec1e24e1ccb9b6ef93f1d7` |
| `scripts/r074h_collar_flux_certificate.py` | `acce024b8dd78ba727e3ec8176a308dc53ecc34b7bdaf57b6c48e5d1e1a5c6e4` |
| `research/r074h_collar_flux_certificate.json` | `783591f3da880ec9182be89c585eb732e35d5842b7d196dc2ae4e35b6c0d2ba4` |
| `research/r074h_collar_flux_certificate_report.md` | `c675d4efea3edfdd3e77844b54ae34a7721902a5f03d6ace72e3dc09ce85bc27` |
| `scripts/r074h_collar_flux_certificate_independent.rb` | `9004240b7a041001fb853eb9963ed10cc768f2e2a3c4b675d1187167c051a39f` |
| `research/r074h_certificate_independent_audit.md` | `3760692601b27e40fcd219aabe9ed612c10e8e1063100b58b6208055ba969545` |
| `research/r074h_report-source.md` | `d72917b04e067113f419f89bc009861f264d859e80cb22dce1276c6dbfbc2c47` |
| `research/r074h_primary_literature_boundary.md` | `722e338f4cdd729f3a8756b886c920f17d08e08592bbce6ed9561179d6afbadf` |
| `research/r074h_primary_literature_independent_audit.md` | `f5c0572c16f26e5066edbf07db8347d591815fe461ffeb81b8c95e2a4ac39f81` |
| `research/r074h_gap_matrix.md` | `3cc23977e865596eb679cceef6260ce7909204da785168efd42663fef9841251` |
| `research/r074h_freeze_manifest.json` | `94911632e1763e308c58a3f01cd90b532e2087be9b5c24264bed90fb53d019d7` |
| figure-package `SHA256SUMS` | `6c1e02e2f2322a25bded0b948f7383a067de4bd247486bd133d68e77e77bf2ca` |
| figure-package `manifest.json` | `0bb323ce916e406c13c17559920699a2dee33bce3041f6dfd3432ad6b6296571` |
| figure-package `validation.json` | `66bc780f94342277a9efb47ad9c33b88f455218e5b64367f3237a2ffc977b655` |
| figure-package `source-data.csv` | `6106a477847cb60765fa48b929aaabe76be14c4c3b9cc1245b19aaa115aa7217` |

The 24-file figure package is

    research/figures/r074h/fig-r074h-collar-flux-repair/

Its publication masters are:

| Figure file | SHA-256 |
|---|---|
| `figure.svg` | `9989d22ac20c619f0f5da285108676318584e53b194fd13abe4a9456c97b09c3` |
| `figure.pdf` | `80441f23ea0a056fdc7a22ee39bc3a452ce39ff11725867b4304b025791d55a0` |
| `figure.png` | `876b88609a12dcda7a88fbffd1f97fcbaf2749251060fbe148ac2b221e8b6c9a` |

## Literal mathematical result

For every smooth periodic unforced solution in the two local frames frozen
in R0.74E, and for each admissible scale and cylinder in the scope of
Section 1, R0.74H proves

\[
 \boxed{
 X_R^M\le C\bigl[(P_R^M)^{2/3}+P_R^M\bigr],}
\]

and, with \(P_{0,R}^F\) denoting the Version-F payment before the
acceleration row,

\[
 \boxed{
 X_R^F\le C\bigl[(P_R^F)^{2/3}+P_{0,R}^F\bigr]
 \le C\bigl[(P_R^F)^{2/3}+P_R^F\bigr].}
\]

Consequently,

\[
 \boxed{
 P_R^\alpha\le1
 \quad\Longrightarrow\quad
 X_R^\alpha\le C(P_R^\alpha)^{2/3},
 \qquad \alpha\in\{M,F\}.}
\]

The exact signed-flux repair is

\[
 \boxed{
 X_R^\alpha
 \le C\left[(P_R^\alpha)^{2/3}+\mathfrak C_R^\alpha\right],}
\]

and, for

\[
 \boxed{
 \widehat P_R^\alpha
 =P_R^\alpha+(\mathfrak C_R^\alpha)^{3/2},}
\]

one has

\[
 \boxed{X_R^\alpha\le C(\widehat P_R^\alpha)^{2/3}.}
\]

On the exact R0.74F--G two-packet family, for all sufficiently large \(j\),

\[
 \boxed{
 P_{R_j}^M=P_{R_j}^F
 \ge cB_j^2L_jR_j^2\longrightarrow\infty,}
\]

\[
 \boxed{
 \mathfrak C_{R_j}^M=\mathfrak C_{R_j}^F
 \ge cB_j^2L_jR_j^2,}
\]

and

\[
 \boxed{
 (\mathfrak C_{R_j}^{\alpha})^{3/2}
 \ge cB_j^3L_j^{3/2}R_j^3,
 \qquad \alpha\in\{M,F\}.}
\]

This identifies positive collar flux as the necessary missing lower scale
for that explicit family.  No reverse comparison, asymptotic equivalence,
matching \(B_j^3R_j^3\) lower bound, or logarithmic-frontier theorem is
claimed.

## Evidence classes that must remain separate

### Analytic PROVED

- the exact weighted local energy identities in both frozen frames;
- the finite-shell limit and pressure-gauge transfer;
- the quadratic cutoff row with exponent \(2/3\);
- the exact positive collar-flux repair;
- the two-regime closure using the frozen nonnegative ledger;
- survival of the small-payment size endpoint; and
- the one-sided collar-flux lower bound on the R0.74G family.

The final source has SHA-256

    8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1.

The byte slice from Sections 1--9 is unchanged across status promotion and
has SHA-256

    56d5e8487224348e9ce0282c4784a57921f70e0d277f261b705993e4e4b3b3ee.

The old pre-promotion full-file digest is retained, but its old byte copy is
not present in the current worktree; the final-source audit states this
boundary explicitly and does not claim an unavailable full-byte diff.

### FINITE only

The certificate returns **PASS: 25/25**.  Python output is byte-identical to
the frozen JSON.  An independent Ruby `Rational` implementation matched all
25 rows and 150 exact fields with zero mismatches.  These checks cover
rational powers and elementary algebra only; they do not prove the analytic
theorem.

The figure validator returns **PASS: 69/69** on two consecutive post-seal
runs.  `SHA256SUMS` verifies all 23 listed package entries, and the physical
package contains exactly 24 files with no runtime cache.  SVG, embedded-font
PDF, 600 dpi PNG, grayscale, final-size, and PDF-rendered surfaces passed QA.
The figure is an exact exponent diagram, not DNS, simulation, or measured
data.

### LITERATURE BOUNDARY only

Four primary papers were checked for neighboring weighted-energy and local-
energy methods.  The exact R0.74H combination was not located in this bounded
screen.  This is a non-hit in a limited corpus, not a novelty or priority
conclusion.

### OPEN and visibly required

1. stability of the theorem under suitable weak-solution approximation;
2. an independently controllable replacement for the identity-level collar
   flux payment;
3. scale iteration or an absorption mechanism;
4. every epsilon-regularity, continuation, or singularity-exclusion result;
5. every global regularity, blow-up, or Clay consequence; and
6. novelty or publication priority.

## Required Chinese publication treatment

Suggested title:

> R0.74H｜环带通量修复：冻结局部坐标中的双区间闭合

Suggested lead:

> 这一节仍然没有解决三维 Navier--Stokes 千禧年问题。上一节证明，原先
> 试图把任意大支付量统一压成 \(P^{2/3}\) 的估计会被一个精确光滑双包解族
> 否定。本节回到局部能量恒等式，找出被遗漏的正环带通量：它给出一个
> 精确的通量修复，并进一步利用已有非负支付账本，证明对任意光滑周期无
> 外力解都成立的双区间估计 \(X\lesssim P^{2/3}+P\)。因此，小支付端的
> \(P^{2/3}\) 尺度结论被保留下来，而大支付端必须支付线性项。双包家族上，
> 正环带通量确实承担了缺失的 \(L_j\) 尺度。这是一项严格的一尺度能量估计，
> 不是 epsilon 正则性、延拓判据或 Clay 问题解答。

The page must use the established concise retro style and complete Chinese
prose.  Preserve the formulas, evidence labels, one-sided qualifiers, and
the phrase **NOT CLAY**.  Do not use “首次”, “世界首个”, “解决千禧年
问题”, or any novelty/priority equivalent.

## Publication checklist for 发布任务

1. consume frozen core commit `5cd31fd8cde1574f02d9e9af3417686d2a8f8d9c`;
   do not edit research-side files or mathematical statements;
2. create the R0.74H Chinese research-note page in the established concise
   retro style;
3. use `figure.svg` as the primary responsive figure, retain PNG as fallback,
   and link the PDF, exact `source-data.csv`, caption, and QA report;
4. link the main note, analytic audits, certificate report, raw JSON, both
   implementations, certificate audit, literature boundary, gap matrix,
   freeze manifest, and figure package evidence;
5. show separate visible labels for **PROVED**, **FINITE**, **OPEN**,
   **LITERATURE BOUNDARY**, and **NOT CLAY**;
6. update the research index, current-version route, and homepage latest
   version to R0.74H only after all earlier queued releases are present;
7. publish this section page and index changes, but do **not** update the
   cumulative recap for this section alone; recap updates remain reserved for
   larger milestones;
8. build and inspect desktop and mobile layouts, verify formula and figure
   readability, and confirm the generated site contains the exact theorem and
   evidence boundaries;
9. publish only to GitHub Pages at `https://kasifa.github.io/`; do not use
   another hosting destination; and
10. do not report deployment as complete until the live GitHub Pages HTML is
    byte-checked against the release output and the live primary figure is
    byte-checked against the frozen `figure.svg`.  A successful push or build
    alone is not deployment proof.

## Research-side reproduction

From the repository root at frozen core commit
`5cd31fd8cde1574f02d9e9af3417686d2a8f8d9c`:

```text
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/r074h_collar_flux_certificate.py \
  | diff -u research/r074h_collar_flux_certificate.json -

/usr/bin/ruby scripts/r074h_collar_flux_certificate_independent.rb

cd research/figures/r074h/fig-r074h-collar-flux-repair
PYTHONDONTWRITEBYTECODE=1 \
  /Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  validate.py
shasum -a 256 -c SHA256SUMS
```

Expected results:

```text
certificate: PASS 25/25 and byte-identical JSON
independent exact reconstruction: PASS 25/25, 150 fields, zero mismatches
figure validator: PASS 69/69
figure package: every SHA256SUMS entry OK; 24 files; no runtime cache
```
