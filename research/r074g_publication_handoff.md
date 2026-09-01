# R0.74G publication handoff — complete-payment counterexample

## Purpose and immutable research snapshot

This is the research-side handoff for R0.74G.  The separate task titled
**发布任务** owns site integration and GitHub Pages deployment.  Publication
may translate, summarize, and typeset the result, but it must not strengthen,
recompute, or silently simplify any mathematical claim.

The frozen core research commit is

    88b599633d4de0b3754a37380eb91104be92da81

on branch

    codex/r073z-research.

The release contains one proved analytic counterexample theorem, three
independent same-source analytic audits, one 31-row exact certificate plus an
independent exact-arithmetic audit, one evidence-and-gap matrix, and one
24-file journal figure package.  It rejects two internally proposed frozen
local-frame inequalities.  It is not a singular solution, a blow-up theorem,
a regularity criterion, or a solution of the Millennium problem.
**NOT CLAY.**

## Frozen files and SHA-256

| Artifact | SHA-256 |
|---|---|
| `research/r074g_complete_payment_counterexample.md` | `95548d6225389b9cfd1822a8abaf89e495e7f15ca5ff30c6b92aaa8ac5f2d6be` |
| `research/r074g_energy_pressure_independent_audit.md` | `305d73a8d45b7292baa7f3535b9347d3822f366087a6600e936915ad20cd1d0e` |
| `research/r074g_occupation_independent_audit.md` | `aa958b3ab703e0078b4e3e1e9d028b7304889d6038be58dd3c4333f2ae6843ab` |
| `research/r074g_complete_ledger_adversarial_audit.md` | `60fff91179a49f2f71a4a68aa5d0e77304b58c6310791e2293ad50d9a95f2cb6` |
| `scripts/r074g_complete_payment_certificate.py` | `315f4cc7f0a397287cc2eb14ec1ad65bcacb797692e2a6ce5a1459985a4853ca` |
| `research/r074g_complete_payment_certificate.json` | `2a411007989e63e51ab7f1644724f654f26794b80507681aaf62e00adbeefd53` |
| `research/r074g_complete_payment_certificate_report.md` | `aee995c26795c460fa76cd004f227f56a102ca2daf1040b428c313d48f3ab3bc` |
| `research/r074g_certificate_independent_audit.md` | `598a92ef5c3cb061142ede1bb1c5dff0680848c386c0847f45d97f246b93fade` |
| `research/r074g_gap_matrix.md` | `e9001e32b993ac565eaf9d3efc70cbec55e4045cc03d3e9c1e736653bea97bf3` |
| `research/r074g_freeze_manifest.json` | `9e6df815df139212ddaa6c54e473bb7fd6e516264287784e20ee96010afe2abe` |
| figure-package `SHA256SUMS` | `5a2143c2c423462aed4adfcc67666dee1c09d89fcb4c28bd20dc738394177977` |
| figure-package `manifest.json` | `f2846fea031d17dd23770b43ef63d66aeaa34055e5881737b49a69b6b66529cd` |
| figure-package `validation.json` | `efc1e674ebcc655e996c2799ef13e46b9094e7e6afd7829e92054a700377d673` |
| figure-package `source-data.csv` | `9cad2386d56dac94a2ea3b471fa0ed5bcc87b24e01699547e0603322296ccc6b` |

The 24-file figure package is

    research/figures/r074g/fig-r074g-complete-payment-ledger/

Its publication masters are:

| Figure file | SHA-256 |
|---|---|
| `figure.svg` | `254aa5c7482d3665ab0873690bd2a3a14dfa0a0555beb3182b001636b8518785` |
| `figure.pdf` | `62fdeeca29227ce508631386d8406815440fd8d06ee9110cb3fb2b707f0f8134` |
| `figure.png` | `57e83342f003217eaa915a7a68122c6015aef3da5d8a8d7f3e6322667306ba7d` |

## Literal mathematical result

Retain the exact parameters

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \alpha=\frac{14}{15},\qquad
 \beta=\frac{\sqrt{31}}{16},\qquad
 c_R=\frac1{320},\qquad
 \kappa=16,
\]

and

\[
 L_j=\lambda2^j,\qquad
 R_j=e^{-c_RL_j^2},\qquad
 r_j=L_jR_j,\qquad
 \gamma_j=e^{-c_\gamma L_j^2},\quad c_\gamma=\frac8{3969}.
\]

For the exact smooth periodic mean-zero unforced 2D3C Navier--Stokes
family inherited from R0.74F, choose

\[
 \mathfrak a_j=B_j\gamma_j^{-1/2}.
\]

Then, for all sufficiently large \(j\), R0.74G proves

\[
 \boxed{P_{R_j}^M=P_{R_j}^F\le C B_j^3R_j^3,}
\]

while the R0.74F survival theorem gives

\[
 \boxed{X_{R_j}^M=X_{R_j}^F\ge cB_j^2L_jR_j^2.}
\]

Consequently,

\[
 \boxed{
 \frac{X_{R_j}^M}{(P_{R_j}^M)^{2/3}}
 =
 \frac{X_{R_j}^F}{(P_{R_j}^F)^{2/3}}
 \ge cL_j\longrightarrow\infty.}
\]

Therefore no solution- and scale-independent constant can make either
proposed inequality R0.74E (3.11) or (4.17) true.

## Evidence classes that must remain separate

### Analytic PROVED

- the buffered local energy estimate, including packet-gradient exclusion;
- the gauge-fixed pressure estimate despite physical pressure \(p=0\);
- the full-time, all-annulus, all-periodic-copy \(p=2,3\) occupation lemma;
- the complete velocity-cubic and algebraic-harmonic packet payments;
- the uniform denominator upper bound at the selected amplitude; and
- divergence of both frozen Version-M and Version-F ratios.

The energy--pressure audit includes a final-source rebind of Sections 2--3
against full-note SHA-256

    95548d6225389b9cfd1822a8abaf89e495e7f15ca5ff30c6b92aaa8ac5f2d6be.

The occupation and complete-ledger audits bind the pre-promotion main-note
SHA-256

    7282ccbe693c7277e111117d5105032d8fed6e55756ad26f2b6b2cd597ddd756.

Only the status block and freeze record were changed afterward.  Sections
1--8 are byte-identical with SHA-256

    ba1d75c6728aaa95d1360f2ff3d9d0c4923aa14c011c2876f41dd7783c3963f9.

### FINITE only

The certificate returns **PASS: 31/31**.  Its Python output is byte-identical
to the frozen JSON, and an independent exact-rational implementation matched
all 31 rows.  It checks finite rational identities, exponent margins, and
geometry gates.  It does not prove the heat-kernel, Brownian-bridge,
Riesz/Newton, Peetre, asymptotic, or counterexample arguments.

The figure validator returns **PASS: 70/70**.  SVG, PDF, 600 dpi PNG,
grayscale, final-size, and PDF-rendered surfaces passed visual QA.  The
figure evaluates exact formulas; it is not DNS, a stochastic simulation, or
measured data.

### Route conclusion only

The frozen R0.74E right side is retired: it does not pay the explicit
travelling two-packet mechanism.  This is a rigorous route-elimination
result.  It does not show that every local-frame estimate fails and does not
identify a sufficient replacement.

### OPEN and visibly required

1. a new scale-invariant denominator that pays the exact two-packet family
   without becoming tautological;
2. an arbitrary-solution theorem for any corrected denominator;
3. every epsilon-regularity, continuation, or singularity-exclusion
   consequence;
4. every global regularity, blow-up, or Clay consequence; and
5. novelty or publication priority, which was not exhaustively audited and
   is not claimed.

## Required Chinese publication treatment

Suggested title:

> R0.74G｜完整支付闭合：一个显式光滑解族否定冻结局部坐标不等式

Suggested lead:

> 这一节没有解决三维 Navier--Stokes 千禧年问题。它完成了上一节留下的
> 完整支付账本：对同一个精确、光滑、周期、零均值的 2D3C 解族，缓冲
> 局部能量的 \(3/2\) 次幂、规范压力项、速度三次项与代数调和项全部可被
> 同一背景尺度控制；
> 与已经证明的双包存活下界合并后，两条冻结局部坐标不等式的比值至少按
> \(L_j\) 发散。因此这两条内部候选估计被严格否定。它的价值是淘汰一条
> 已经走通到完整分母的错误路线，并为下一版分母留下精确压力测试；它不
> 构造奇性，也不推出正则性，更不是 Clay 问题的解答。

The page must use the established concise retro style and complete Chinese
prose.  Preserve the formulas, equation references, evidence labels, and
the phrase **NOT CLAY** exactly.  Do not use “首次”, “世界首个”, “证明千禧年
问题”, or any novelty/priority equivalent.

## Publication checklist for 发布任务

1. consume frozen core commit `88b599633d4de0b3754a37380eb91104be92da81`;
   do not edit research-side files;
2. create the R0.74G Chinese research-note page in the established concise
   retro style;
3. use `figure.svg` as the primary responsive figure, retain PNG as fallback,
   and link PDF and exact `source-data.csv`;
4. link the main note, all three analytic audits, certificate report, raw
   JSON, producer script, certificate audit, gap matrix, freeze manifest,
   figure caption, and QA report;
5. show separate visible labels for **PROVED**, **FINITE**, **OPEN**,
   **ROUTE REJECTED**, and **NOT CLAY**;
6. update the research index, current-version route, and homepage latest
   version to R0.74G after all earlier queued versions are present;
7. include the route decision in this section page, but do not create a
   separate cumulative recap solely for this section;
8. build and inspect desktop and mobile layouts, verify formulas and figure
   readability, then byte-check deployed GitHub Pages HTML and the primary
   figure against the release output; and
9. publish only to GitHub Pages.  Do not use another hosting destination.

## Research-side reproduction

From the repository root at the frozen core commit:

```text
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/r074g_complete_payment_certificate.py \
  | diff -u research/r074g_complete_payment_certificate.json -

python3 -m json.tool research/r074g_freeze_manifest.json >/dev/null

cd research/figures/r074g/fig-r074g-complete-payment-ledger
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 plot.py
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 validate.py
shasum -a 256 -c SHA256SUMS
```

Expected results:

```text
certificate: PASS 31/31 and byte-identical JSON
figure validator: PASS 70/70
figure package: every SHA256SUMS entry OK
```
