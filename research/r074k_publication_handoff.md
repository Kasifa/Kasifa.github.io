# R0.74K publication handoff — single inward-collar reduction

## Purpose and immutable research snapshot

This is the research-side handoff for R0.74K.  The new independent task titled
**发布任务** owns site integration and GitHub Pages deployment.  Its task id is

    01a05bea-7f45-7410-8792-4e1f840b83f8.

It does not reuse an older publication task.  The research task freezes the
mathematics and transfers an auditable release packet; the publication task
alone owns web copy, integration, deployment, and live verification.

The frozen core research commit is

    a817fb1169b34d6e92911c448cad9c8c59fae138

on branch

    codex/r073z-research.

R0.74K must be published only after R0.74J.  At handoff time the verified live
baseline remains R0.74I at `origin/main`
`5facce779682488b5223b3fc75f6dec1d83dce00`; therefore a completed task or a
successful push is not evidence that either later section is live.

Publication may translate, summarize, typeset, and integrate the release.  It
must not edit the frozen research files, promote the sufficient hypothesis
(4.3) to a theorem, turn a route obstruction into a counterexample, or
suppress an evidence boundary.

R0.74K proves a single-adverse-inward-collar route reduction, a
positive-volume obstruction to a free-heat replacement, the correct
constant-shear reference scale, and a conditional implication on the exact
R0.74F--H smooth periodic unforced family.  It does not prove the true-packet
bridge--BV estimate, either matching observable upper bound, a universal
endpoint theorem, regularity, singularity formation, or the Millennium
problem.  **NOT CLAY.**

## Frozen files and SHA-256

| Artifact | SHA-256 |
|---|---|
| `research/r074k_problem_freeze.md` | `ddb9467b2a68faae8f85bfc208393cd00fd90bc51ef02d723dfab24216bde2e4` |
| `research/r074k_single_collar_shear_lag_reduction.md` | `8f21248603551c39f34864dd921847dc8b9c6f70962209864901d476fe6722e3` |
| `research/r074k_inward_tail_independent_audit.md` | `df71c930f35bccf096c73261acf8a721c439eb15b932323fc8a1219379941656` |
| `research/r074k_collar_reduction_independent_audit.md` | `120856123269679c25de3d86b675cf948e6409cdb7a131cfd3ad06460c176285` |
| `research/r074k_certificate_independent_audit.md` | `89055883887b8a52003dd0f11224320855a6914d3e79213ac6d11e0e5602c6a1` |
| `research/r074k_figure_independent_audit.md` | `5a1ff2af46ef5ea8ddbac1f4056d7e9f0120d13336b33c2e043289a29fa33b0a` |
| `research/r074k_final_source_rebind_audit.md` | `45904c4307fc0b1745d44f903a62f6b06f2ed639ac7d49af4ebffb41d706a7e5` |
| `research/r074k_freeze_manifest.json` | `82e5750ab3153401ebab37f36d53c1d593ab4c6cbf4ec16a633330a88aa68769` |
| `research/r074k_gap_matrix.md` | `61382ecdd6ada4ef91883390ab03afbbc832c5ecd066fb7f26e22f11d916a4dc` |
| `research/r074k_report-source.md` | `457a0a72aa36fb35d8924b9d4af5cfc826c363e6b01852c8b3fc87be8fb7288b` |
| `research/r074k_primary_literature_boundary.md` | `a0b7d1204c9d54ee642ea7547c961ddfdb45ad1e76df88e30c3773e5a576cdd9` |
| `research/r074k_primary_literature_independent_audit.md` | `b14b219efcc2238c3067f627101bb3070769251b84876f268df55c718d9f1331` |
| `research/r074k_bilingual_dictionary.md` | `c83ded2c62979c42b27e3102907edada0248a70d02c870d9177e675ab5966f66` |
| `scripts/r074k_single_collar_exponent_certificate.py` | `c1de693bdae761826608ece64d518035e2d732578b191ce01158f30adedf0b5b` |
| `research/r074k_single_collar_exponent_certificate.json` | `67e4ab156d7d5a73fd07e584f3f87f7c9287591856b285bd9a747d00f85de41f` |
| `research/r074k_single_collar_exponent_certificate_report.md` | `86ee3ec729a087214a06c6520306bc6f8b8487d9f9df9aabe611276150b68958` |
| `scripts/r074k_single_collar_exponent_certificate_independent.rb` | `b37394432f673a9084acad963eafe32f9ab995243e1cff85fe3f819de184cc79` |
| figure-package `SHA256SUMS` | `59ad9518f0525e6fb9234aa4660511ab78bbda14eccf94c1bd5ed680f070753c` |
| figure-package `manifest.json` | `758e9335265928deaa7874b3fed1689dcacc66b1a82a673f0231ca9ba3faddbd` |
| figure-package `validation.json` | `cd5919984d6b4e5b1c93b7ac58e9e45d7c762f00abba4c6098f9a7635cdf1092` |

The figure package is

    research/figures/r074k/fig-r074k-single-inward-collar/

Its publication masters are:

| Figure file | SHA-256 |
|---|---|
| `figure.svg` | `599c269979c368473fbcb57f6691025ec06ee909ca19efbae35e078b79f0745e` |
| `figure.pdf` | `826fb9441fbdfa699f39bd528314529a734bf9f371e009aa60d86c6e9046c3bc` |
| `figure.png` | `d0644e4d3b98c73ed53151e9816f7d3ce68028150ede9d939c13eab173a624b5` |
| `source-data.csv` | `defae44140159e2d3d97271da559fb9f49520e1e50c17191529af0bbad429d32` |

## Literal mathematical result

For the inward shell (A_{j-m}(R_j)), define

\[
 d_m=c_h-\frac{2^{1-m}}{\lambda},
 \qquad
 G_m=c_\gamma(1-4^{-m}),
\]

with

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 c_\gamma=\frac{8}{3969}.
\]

For every physical deeper shell (2\le m\le j-1),

\[
 \boxed{
 \frac{d_m^2}{132}-G_m
 \ge\frac{204385}{134120448}>0.}
\]

At the nearest inner shell, the positive-volume box

\[
 \frac{4033}{8064}r_j\le x_3
 \le\left(\frac{4033}{8064}+\frac1{256}\right)r_j,
 \qquad |x_1|,|x_2|<\frac1{64}r_j
\]

has normalized volume (1/262144), lies inside the audited region, and keeps
the wrong-sign margin

\[
 \boxed{
 G_1-\frac{d_{1,\varepsilon}^2}{132}
 =\frac{536399}{8583708672}>0.}
\]

This proves that replacing the true packet by a free heat packet cannot close
the selected route.  It does not prove that the desired observable upper
bound is false.

For the constant-shear reference packet, R0.74K proves

\[
 \sup_{x_3}\int M_j(x_2,x_3)\,dx_2\le C L_jR_j
\]

and, for every \(\tau\in I_{R_j}\),

\[
 \Gamma_j\int_{I_{2R_j}\cap(-\infty,\tau]}
 |F_{\rm fr}|^2|\partial_2\psi_j^{R_j}|
 \le C\Gamma_jL_jR_j^5.
\]

The precise sufficient hypothesis is

\[
 \boxed{
 \sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+
 \le C\Gamma_jL_jR_j^5.}
\]

If this OPEN true-packet hypothesis is proved, then

\[
 \boxed{\mathfrak C_j\lesssim B_j^2L_jR_j^2.}
\]

Together with the inherited lower bound and R0.74J, it would yield the
familywise identity

\[
 \mathfrak C_j
 \asymp B_j^2L_jR_j^2
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.
\]

The hypothesis and the matching upper remain **OPEN**.

## Evidence classes that must remain separate

### Analytic PROVED

- only the nearest inward shell obstructs the free squared-heat exponent;
- the obstruction holds on an explicit positive-volume box;
- the physical deeper-shell margin is uniform for (2\le m\le j-1);
- the slice-BV reference-packet collar scale is
  (C\Gamma_jL_jR_j^5); and
- hypothesis (4.3) implies the stated familywise matching collar upper.

### INHERITED

- the exact R0.74F--H smooth periodic unforced family;
- R0.74J's complete-payment law
  (P_j\asymp B_j^3R_j^3); and
- the previously proved familywise lower bound for \(\mathfrak C_j\).

### FINITE only

The Python producer returns 41/41 and is byte-identical to the frozen JSON.
The independent Ruby implementation returns 41/41 with zero mismatches.
These checks certify rational arithmetic and the conditional exponent ledger,
not the Brownian bridge or a PDE estimate.

The formal figure validator returns 41/41.  The 25-file package, vector SVG
and PDF, 600-dpi PNG, final-size surface, grayscale surface, independent PDF
raster, and checksums pass.  The figure is a mathematical dependency diagram,
not DNS, simulation, experimental data, or singularity evidence.

### LITERATURE BOUNDARY only

The bounded primary-source screen covers Bedrossian--Coti Zelati,
Albritton--Beekie--Novack, Villringer, Gardner--Liss--Mattingly, and
Liss--Luan.  Albritton--Beekie--Novack Remark 1.4 discusses a possible
time-varying generalization, but none of the screened theorems supplies the
required scale-dependent finite-window signed collar estimate.  This finite
non-hit is not an exhaustive search and is not a novelty or priority claim.

### OPEN and visibly required

1. the time-coupled normalized-bridge--BV estimate on the main collar;
2. positive shear expulsion at the nearest inner shell;
3. hypothesis (4.3) itself;
4. the matching upper for \(\mathfrak C_j\);
5. the stronger matching upper for \(X_j\);
6. a universal square-root-log endpoint theorem;
7. payment-to-admissibility or prescribed-point good-scale control; and
8. global regularity, singularity exclusion, novelty, or priority.

## Locked Chinese publication treatment

Title:

> R0.74K｜自由热指数为何只卡在最近内领圈

Lead:

> 这一节仍然没有解决三维 Navier--Stokes 千禧年问题。我审计了
> R0.74J 留下的两个匹配上界方向。精确指数核算表明：如果把真实
> 被动包替换为自由热包，所有更深内壳都有严格指数余量，只有最近的
> \(j-1\) 壳在一个正体积薄片上仍以
> \(536399/8583708672\) 的系数向错误方向增长。因此，所选的归一化
> 周期桥路线必须保留内向 Brownian bridge 与正剪切滞后之间的相关性。
> 本文还给出一个精确充分条件：若对应的有符号包领圈积分不超过
> \(\Gamma_jL_jR_j^5\)，则该精确解族的领圈通量恰好饱和
> \(P_j^{2/3}\sqrt{1+\log P_j}\) 尺度。这个随机路径估计尚未证明；
> 匹配上界仍为 OPEN。NOT CLAY。

Use the established concise retro style and first-person singular voice for
research choices.  Preserve the exact formulas, the familywise qualifier,
all evidence labels, and **NOT CLAY**.  Do not use “首次”, “世界首个”,
“解决千禧年问题”, “接近解决”, or any novelty or priority equivalent.
Ordinary translation remains local; do not use DGX for translation.

## Publication checklist for 发布任务

1. publish R0.74J first from core commit
   `3f5f9ad68d5d0e8c5998e560f0489731522a4dd5` and its handoff commit
   `18d5e1dfe4c6516abe3b7400cad1c659f0790e03`;
2. complete R0.74J's live HTML and primary-SVG byte gates before integrating
   R0.74K from core commit
   `a817fb1169b34d6e92911c448cad9c8c59fae138`;
3. create the R0.74K Chinese note in the established concise retro style and
   generate a synchronized downloadable PDF from the same bound source;
4. use the frozen `figure.svg` as the primary responsive figure, retain PNG
   as fallback, and link the vector PDF, source data, caption, QA report,
   plotting source, validator, and figure manifest;
5. expose the main note, both analytic audits, final rebind, exact certificate
   and report, both implementations, certificate audit, literature boundary
   and audit, gap matrix, bilingual dictionary, and freeze manifest;
6. display separate visible labels for **PROVED**, **INHERITED**, **FINITE**,
   **LITERATURE BOUNDARY**, **OPEN**, and **NOT CLAY**;
7. update the research index, latest-research endpoint, homepage version,
   public-note count, and release inventory from actual files after each
   ordered release;
8. publish both sections but do **not** update the cumulative recap; the last
   milestone recap remains labelled as the previous milestone;
9. run desktop/mobile layout QA, formula checks, evidence-link checks, PDF
   render QA, and the repository's publication tests;
10. publish only through the GitHub repository and GitHub Pages at
    `https://kasifa.github.io/`; and
11. do not report either release complete until its live HTML and live primary
    SVG are byte-identical to the corresponding built output.

## Research-side reproduction

From the repository root at frozen core commit
`a817fb1169b34d6e92911c448cad9c8c59fae138`:

```text
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/r074k_single_collar_exponent_certificate.py \
  | diff -u research/r074k_single_collar_exponent_certificate.json -

/usr/bin/ruby \
  scripts/r074k_single_collar_exponent_certificate_independent.rb

/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  research/figures/r074k/fig-r074k-single-inward-collar/validate.py \
  --verify-only

cd research/figures/r074k/fig-r074k-single-inward-collar
shasum -a 256 -c SHA256SUMS
```

Expected results:

```text
certificate: PASS 41/41 and byte-identical JSON
independent exact reconstruction: PASS 41/41, zero mismatches
figure validator: verify-only PASS 41/41; 25 files; seals PASS
figure package: every SHA256SUMS entry OK; no runtime cache
```
