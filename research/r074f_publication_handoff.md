# R0.74F publication handoff — two-packet survival in the odd local frame

## Purpose and immutable research snapshot

This is the research-side handoff for R0.74F.  The separate task titled
**发布任务** owns site integration and GitHub Pages deployment.  Publication
may translate, summarize, and typeset the result, but it must not strengthen
or recompute any mathematical claim.

The frozen core research commit is

    56f53d4e8b905203589e1129fd15a61863cd8cc1

on branch

    codex/r073z-research.

The release has one proved analytic theorem, two same-source independent
analytic audits, one finite exact certificate, one journal figure package,
and one bounded primary-literature audit.  It is not a denominator closure,
regularity theorem, singularity construction, or solution of the Millennium
problem.  **NOT CLAY.**

## Frozen files and SHA-256

| Artifact | SHA-256 |
|---|---|
| `research/r074f_two_packet_survival.md` | `0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb` |
| `research/r074f_periodic_bridge_independent_audit.md` | `0a56b354ffb6c121f49b9c1470db21ed74dd193074d0ce0ebff3dd3dac0dbafb` |
| `research/r074f_two_packet_survival_independent_audit.md` | `2867f26a4076b784396d7b28a5e9eba85f62129908ab623369875eeb930309c5` |
| `scripts/r074f_two_packet_survival_certificate.py` | `578879ad456b80a8a919e3b9a7f84da9347ad4d51f120cc53185ac61e27b0e19` |
| `research/r074f_two_packet_survival_certificate.json` | `44bd3208d10134ae84cf8b001e9569b6c480af6ac7d85efc25759dc4e725e981` |
| `research/r074f_two_packet_survival_certificate_report.md` | `c8aa8a832cfc74722df463e660b362a27cb778280b643f4e304491a5144ead76` |
| `research/r074f_primary_literature_boundary.md` | `03a06f2e2ee4b2e860a1deb2aa31649f73b00b18ec0e202b0a75daffe4cfda5d` |
| `research/r074f_freeze_manifest.json` | `00eaf3562bad18c81455b6dd23fd57a7529862d4e7565a41857e18079413b3e4` |
| figure-package `SHA256SUMS` | `0b6de302cac7f4a2659edd58d775ff62aa18025f7d1afe3364a43b4bb82aa5ce` |
| figure-package `manifest.json` | `c31833aa03911b14ec6b93064f03f1aad6469d84693c0743645efb01b7c82bbf` |
| figure-package `validation.json` | `7f6b7ea4be4b44ee52cffa37fb51cd0cc5f2c6e66608b0b29493036e9f476fc1` |

The 24-file figure package is

    research/figures/r074f/fig-r074f-two-packet-survival-gates/

Its publication masters are:

| Figure file | SHA-256 |
|---|---|
| `figure.svg` | `b30c2972ed0b60052ad6484ebe33f2fd1f85fd34cc7705c4eab02557b4495a51` |
| `figure.pdf` | `01366deccdcc9fa7d7d9dea7cda351777b8ac5143ea76d23b402d2b830f17bcb` |
| `figure.png` | `0d366d31815d261424f0fc5f94e6dfb5bc5ec6c5444b9fbf0d8ffda681945722` |

## Literal mathematical result

Retain the exact parameters

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \alpha=\frac{14}{15},\qquad
 \beta=\frac{\sqrt{31}}{16},\qquad
 c_R=\frac1{320},\qquad
 \kappa=16.
\]

For

\[
 L_j=\lambda2^j,\qquad
 R_j=e^{-c_RL_j^2},\qquad
 r_j=L_jR_j,
\]

the note constructs an exact smooth periodic mean-zero unforced 2D3C
Navier--Stokes family

\[
 u_j=(\mathfrak a_jF_j,b_j,0),\qquad p_j=0.
\]

Full inversion oddness and the even matching mollifier give

\[
 X_{R_j}(t)\equiv0,\qquad
 a_{R_j}(t)=a_{R_j}'(t)=0.
\]

The periodic all-winding Brownian-bridge estimate, drift-shift control,
opposite-packet suppression, and terminal annular-lobe geometry then prove:

\[
 \boxed{
 X_{R_j}^M=X_{R_j}^F
 \ge c\,\mathfrak a_j^2L_jR_j^2
 e^{-c_\gamma L_j^2},
 \qquad c_\gamma=\frac8{3969}.}
\]

This holds for every \(\mathfrak a_j>0\) and all sufficiently large
\(j\).  The finite arithmetic gate begins at \(j=13\), but the analytic
theorem deliberately retains “sufficiently large”; it does not assert that
\(j=13\) alone is sufficient for every asymptotic estimate.

## Evidence classes that must remain separate

### Analytic PROVED

- the exact 2D3C Navier--Stokes family;
- zero mollified trajectory and acceleration by symmetry;
- the positive-packet time-reversed Feynman--Kac formula;
- the exact periodic bridge identity retaining every winding;
- the weighted leakage and accumulated-shift estimates;
- inverted-packet suppression;
- the positive-measure terminal lobe inside the frozen dyadic annulus; and
- the displayed lower bound for \(X_{R_j}^M=X_{R_j}^F\).

Both independent audits bind the exact final main-note SHA.  During the
administrative status promotion, Sections 1--6 were verified byte-identical
with shared SHA-256

    43075ecd48169a2148f587d43f0c7ac17fff122c38f4f5986ab9b78046b0e981.

### FINITE only

The exact certificate returns **PASS: 30/30**.  It checks rational
identities, exponent margins, the discrete threshold, and conditional
annular geometry.  It does not prove any stochastic, PDE, sign, or packet
survival statement.

The figure validator returns **PASS: 50/50**.  The SVG, PDF, 600 dpi PNG,
grayscale derivative, PDF rendering, and final-size derivative passed visual
inspection.  The figure is analytic bookkeeping, not DNS or simulation.
Its visible boundary must remain:

> FINITE COMPATIBILITY ONLY — ANALYTIC BRIDGE / PACKET SURVIVAL NOT
> CERTIFIED BY FIGURE — NOT CLAY.

### Bounded literature audit only

The primary-literature file places the proof against classical
Feynman--Kac, Brownian-bridge, 2D3C passive-scalar, shear-dispersion, and
mollified-trajectory results.  The targeted search found no direct statement
of the same combined theorem, but this is not a priority or novelty proof.
Do not use “first”, “new”, “unprecedented”, or any equivalent wording.

## What remains OPEN and must be visible

1. the buffered \(8R_j\) local-energy upper bound for all relevant velocity
   and gradient components;
2. the complete transition, background, packet, and mixed \(G_u\) rows;
3. the gauge-fixed pressure row and all-copy algebraic \(H_u\) row;
4. one amplitude \(\mathfrak a_j\) closing the full denominator and deciding
   whether this explicit family is paid or yields a diverging ratio;
5. the corresponding endpoint statement for arbitrary Navier--Stokes
   solutions; and
6. every global regularity, blow-up, or Clay consequence.

## Required Chinese publication treatment

Suggested title:

> R0.74F｜奇对称局部坐标中的双包存活：周期桥估计闭合

Suggested lead:

> 这一节没有解决三维 Navier--Stokes 千禧年问题。它证明了一个更窄、
> 但此前尚未闭合的解析门槛：在一个精确光滑、周期、零均值的 2D3C
> 解族中，奇对称性把选定的局部随流轨迹严格钉在原点；保留所有周期
> winding 的 Brownian bridge 估计随后证明，成对热核包在终端时间片仍有
> 一个正测度瓣落入指定外环带，从而给出冻结端点的显式下界。完整支付
> 账本、振幅闭合和任意解问题仍然开放。

The page must use the existing concise retro style and complete Chinese
prose.  Preserve mathematical formulas exactly; do not translate symbols or
silently sharpen the safe constants \(65/32\) and \(97/32\).

## Publication checklist for 发布任务

1. consume the frozen core commit above; do not edit research-side files;
2. create the R0.74F Chinese research-note page in the established retro
   style;
3. use `figure.svg` as the primary responsive figure, retaining PNG as a
   fallback and links to PDF/source data;
4. link the main note, both independent audits, certificate report, raw
   JSON, producer script, freeze manifest, literature boundary, figure
   caption, and QA report;
5. show separate visible labels for **PROVED**, **FINITE**, **OPEN**,
   **BOUNDED LITERATURE AUDIT**, and **NOT CLAY**;
6. update the research index, current-version route, and home-page latest
   version to R0.74F after any earlier queued section is present;
7. do not create a cumulative recap solely for this section;
8. build and test the site, inspect desktop and mobile rendering, verify
   formulas and figure readability, then byte-check deployed GitHub Pages
   HTML and primary figure against the release output; and
9. publish only to GitHub Pages.  Do not use another hosting destination.

## Research-side reproduction

From the repository root at the frozen core commit:

```text
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/r074f_two_packet_survival_certificate.py \
  | diff -u research/r074f_two_packet_survival_certificate.json -

/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  -m json.tool research/r074f_freeze_manifest.json >/dev/null

cd research/figures/r074f/fig-r074f-two-packet-survival-gates
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 plot.py
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 validate.py
shasum -a 256 -c SHA256SUMS
```

Expected results:

```text
certificate: PASS 30/30 and byte-identical JSON
figure validator: PASS 50/50
figure package: every SHA256SUMS entry OK
```

The research task proceeds independently after this handoff.  It does not
wait for site integration or deployment verification.
