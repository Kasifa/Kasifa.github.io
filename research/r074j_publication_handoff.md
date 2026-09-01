# R0.74J publication handoff — fifth-shell matching payment

## Purpose and immutable research snapshot

This is the research-side handoff for R0.74J.  The new independent task titled
**发布任务** owns site integration and GitHub Pages deployment.  It does not
reuse an older publication task.  The research task may continue after this
handoff without absorbing publication work.

The frozen core research commit is

    3f5f9ad68d5d0e8c5998e560f0489731522a4dd5

on branch

    codex/r073z-research.

Publication may translate, summarize, typeset, and integrate the release.  It
must not edit the frozen research files, weaken an assumption, strengthen a
familywise theorem into a universal theorem, or suppress an evidence
boundary.

R0.74J proves a matching complete-payment law on the exact R0.74F--H smooth
periodic unforced family analysed in R0.74I.  It contains two independent
final-source analytic audits, a bounded four-source literature audit, a 38-row
exact certificate with an independent 38-row reconstruction, and a 24-file
journal figure package.  It does not prove a universal square-root-log
endpoint upper estimate, a matching upper bound for \(X_j\) or
\(\mathfrak C_j\), a prescribed-point smallness mechanism, global regularity,
or the Millennium problem.  **NOT CLAY.**

## Frozen files and SHA-256

| Artifact | SHA-256 |
|---|---|
| `research/r074j_problem_freeze.md` | `383e4e8e9a983e4b74050e657bd11fa234ad8dfe2c6fa3c0ec1a8800781291e0` |
| `research/r074j_matching_payment_law.md` | `d495ff3d069eceea9dd7bbf1c467f8836cb72033cde7a9d9c17e9b585478dbad` |
| `research/r074j_heat_platform_independent_audit.md` | `45214485a46271174db047c6fb6565c276d712f15c6009e15221626a0d0e9f23` |
| `research/r074j_complete_payment_ledger_independent_audit.md` | `78e18dc6daa3291bb2f7fcf2bd58d56db504560a19ae6b38e2c7b303c89b599c` |
| `research/r074j_final_source_rebind_audit.md` | `c86b1edea231663df26121a4da45d76435e6e3d3e5191022031f0559a91fa050` |
| `research/r074j_freeze_manifest.json` | `608773b688371742dffedd30938bf35fb4cfda46c72d87d9b6168d629ebe0952` |
| `research/r074j_gap_matrix.md` | `4e83680b8da9c6d651de1647b9975e2ff32c26ee291a151467b2958e873b9e89` |
| `research/r074j_report-source.md` | `e36e2529f77f81e8a6617652d641e016ece175075862500412e529907d3d4f9f` |
| `research/r074j_primary_literature_boundary.md` | `a4a60575122efde993252a9cafda2a85ea15da7f67aa34d1583dc95552f45c60` |
| `research/r074j_primary_literature_independent_audit.md` | `e72aaafb4eca9c28d0834e514866522c60155bfc3220c39857fd452a01046ae2` |
| `research/r074j_bilingual_dictionary.md` | `3ea788eeb84cd82ae24dd6c9584223b8caef5d927eea8b3a0aef348c81991a8b` |
| `scripts/r074j_matching_payment_certificate.py` | `6dcc03d283612306dc39669f5b6c8b3cf8569e40205e067c4db0c2b6929879ec` |
| `research/r074j_matching_payment_certificate.json` | `493c9cf6bc1357b36da1b0a13becbc51e62ea26aab95b6af7eaeb085b65be5d5` |
| `research/r074j_matching_payment_certificate_report.md` | `6a32098c808373a7d3cfbd30b266f20d0aa33abc2b693e51b48b0c486852fa07` |
| `scripts/r074j_matching_payment_certificate_independent.rb` | `ca3da7fafea86012c58c20801e680c9bb5ed26c712c92d32cc080426f9916197` |
| `research/r074j_certificate_independent_audit.md` | `74a68cf221efd1c30e3461012b2196d7fc38621f36c9648e24fcc4814ee755e2` |
| figure-package `SHA256SUMS` | `ea4da4d2eefcf57758c479a9cebd99cc14091ad7b42fd45f180bbb54596db366` |
| figure-package `manifest.json` | `0688dab352ac78c907b712698edd4645a4e1a6eeffb6fab5cb597dfdf05cb6cc` |
| figure-package `validation.json` | `84eb7a87482a9633aaa9d506a3b6133162cb4510f694a3705a390d1f2f1dcd81` |

The figure package is

    research/figures/r074j/fig-r074j-fifth-shell-payment/

Its publication masters are:

| Figure file | SHA-256 |
|---|---|
| `figure.svg` | `ed42960e32e7b2e4707bab933bd3ff400e2f0722ba77f7fc53f0dcaeff3d736b` |
| `figure.pdf` | `3cabf4a587ae6a7fbf145039740489d1f2ba79e9903ed560779d02e56ecab6f1` |
| `figure.png` | `5aef3c61cb0b557411599d0a1ff7dd92e8c89f750f4d7abcfbd3a1d7aaa689b2` |

## Literal mathematical result

For all sufficiently large \(j\), with

\[
 z_{0,j}=(65R_j^2,0),
 \qquad
 A_5(2R_j)=\{64R_j\le |x|<128R_j\},
 \qquad \Gamma_5=e^{-8},
\]

the selected proof box gives

\[
 \boxed{
 \mathcal G_u(z_{0,j},2R_j;1)
 \ge8e^{-8}B_j^3R_j^3.}
\]

Together with the inherited R0.74G upper bound and the exact zero-frame
identities,

\[
 \boxed{
 8e^{-8}B_j^3R_j^3
 \le P_j:=P_{R_j}^M=P_{R_j}^F
 \le CB_j^3R_j^3.}
\]

Consequently,

\[
 \boxed{
 \frac{\log P_j}{L_j^2}\longrightarrow\frac3{320},
 \qquad
 \log\frac{P_{j+1}}{P_j}
 =\frac9{320}L_j^2+O(1).}
\]

On this family,

\[
 \boxed{
 P_j^{2/3}\sqrt{1+\log_+P_j}
 \asymp B_j^2L_jR_j^2.}
\]

The last identity explains the familywise square-root-log scale.  It is not a
universal endpoint upper estimate.

## Evidence classes that must remain separate

### Analytic PROVED

- the profile-independent periodic heat-platform lower bound;
- exact placement of the selected box in the fifth payment shell;
- the nonnegative velocity-cubic lower row;
- the matching Version-M/Version-F complete-payment law on the exact family;
- the logarithmic payment rate \(3/320\); and
- the lacunarity coefficient \(9/320\).

### INHERITED

- construction and exact zero-frame identities of the R0.74F--H family;
- the amplitude calibration \(\beta_j=B_jR_j^2\to1/128\); and
- R0.74G Theorem 1.1, which supplies the matching upper bound.

### FINITE only

The Python producer returns 38/38 and is byte-identical to the frozen JSON.
The independent Ruby implementation returns 38/38, compares 287 terminal
fields, and finds zero mismatches.  These checks certify finite arithmetic
only, not the heat equation or any continuum theorem.

The figure validator returns 79/79.  The 24-file seal, SVG, vector PDF,
600-dpi PNG, final-size surface, grayscale surface, and independent PDF
raster all pass.  The figure is an exact analytic diagram, not DNS,
simulation, experimental data, or evidence of singularity.

### LITERATURE BOUNDARY only

The bounded primary-source audit covers Yang (2022), Vasseur--Yang (2021),
Lei--Ren (2024), and Wang--Wu--Zhou (2019).  Several moving-cylinder,
partial-regularity, and one-scale epsilon mechanisms are prior art.  No
matching complete-payment theorem was found in those four papers, but that
finite non-hit is not evidence of novelty or priority.

### OPEN and visibly required

1. a universal square-root-log endpoint upper estimate;
2. a matching upper bound for \(X_j\);
3. a separate matching upper bound for \(\mathfrak C_j\);
4. payment-to-admissibility or moving core-from-shell control;
5. a good-scale theorem at a prescribed possible singular point;
6. global regularity or singularity exclusion; and
7. novelty or publication priority.

## Locked Chinese publication treatment

Title:

> R0.74J｜第五支付壳给出的匹配完整支付律

Lead:

> 这一节仍然没有解决三维 Navier--Stokes 千禧年问题。我重新核对了
> R0.74F--H 构造并在 R0.74I 中再次分析的精确、光滑、周期、无外力
> 解族。在支付半径
> \(2R_j\) 的第五壳，一个固定盒中的背景剪切在整个支付时间窗内保持
> 至少 \(1/2\)，所以非负的速度三次项给出
> \(8e^{-8}B_j^3R_j^3\) 的下界。与 R0.74G 已证明的上界合并后，
> Version M 和 Version F 的共同完整支付量满足
> \(P_j\asymp B_j^3R_j^3\)，并且
> \(\log P_j/L_j^2\to3/320\)。这是一个精确解族上的匹配支付律，
> 不是普适平方根对数端点上界；它没有给出 \(X_j\) 或
> \(\mathfrak C_j\) 的匹配上界，也没有在可能奇点处制造小量条件。
> **NOT CLAY.**

Use the established concise retro style and a first-person singular voice for
research choices.  Preserve all formulas, the familywise qualifier, evidence
labels, literature boundary, and **NOT CLAY**.  Do not use “首次”, “世界首个”,
“解决千禧年问题”, “接近解决”, or any novelty or priority equivalent.
Ordinary Chinese--English translation is done locally; do not use DGX for
translation.

## Publication checklist for 发布任务

1. consume frozen core commit
   `3f5f9ad68d5d0e8c5998e560f0489731522a4dd5`; do not edit the research-side
   files or mathematical statements;
2. create the R0.74J Chinese note in the established concise retro style and
   generate a synchronized downloadable PDF from the same bound source;
3. use the frozen `figure.svg` as the primary responsive figure, retain PNG
   as fallback, and link the vector PDF, source data, caption, QA report,
   plotting source, validator, and figure manifest;
4. expose links to the main note, both analytic audits, final rebind,
   certificate report and JSON, both exact implementations, certificate
   audit, literature report/boundary/audit, gap matrix, bilingual dictionary,
   and freeze manifest;
5. display separate visible labels for **PROVED**, **INHERITED**, **FINITE**,
   **LITERATURE BOUNDARY**, **OPEN**, and **NOT CLAY**;
6. update the research index, latest-research endpoint, homepage version,
   public-note count, and release inventory from actual files;
7. publish this section but do **not** update the cumulative recap; the
   previous milestone recap remains byte-identical and explicitly labelled as
   the previous milestone;
8. run desktop/mobile layout QA, formula checks, evidence-link checks, PDF
   render QA, and the repository's publication tests;
9. publish only through the GitHub repository and GitHub Pages at
   `https://kasifa.github.io/`; do not use another hosting destination; and
10. do not report deployment as complete until the live R0.74J HTML and the
    live primary SVG are byte-checked against the release output.  A successful
    push or build alone is not deployment proof.

## Research-side reproduction

From the repository root at frozen core commit
`3f5f9ad68d5d0e8c5998e560f0489731522a4dd5`:

```text
python3 scripts/r074j_matching_payment_certificate.py \
  | diff -u research/r074j_matching_payment_certificate.json -

/usr/bin/ruby scripts/r074j_matching_payment_certificate_independent.rb

cd research/figures/r074j/fig-r074j-fifth-shell-payment
PYTHONDONTWRITEBYTECODE=1 \
  /Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  validate.py --verify-only
shasum -a 256 -c SHA256SUMS
```

Expected results:

```text
certificate: PASS 38/38 and byte-identical JSON
independent exact reconstruction: PASS 38/38, 287 fields, zero mismatches
figure validator: PASS 79/79
figure package: every SHA256SUMS entry OK; 24 files; no runtime cache
```
