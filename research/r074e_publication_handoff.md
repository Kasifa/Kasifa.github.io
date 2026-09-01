# R0.74E publication handoff — local mollified frame and finite outer gate

## Purpose and immutable research snapshot

This is the research-side handoff for R0.74E. Publication may summarize and
typeset the result, but it must not strengthen any claim. The frozen research
commit is

    4d0a017f4fff08ec53ddf57d73a1d237e2bc866c

The release separates three statements:

1. the exact algebra of moving and subtracting a local mollified velocity;
2. the familywise neutralization of the old R0.74D explicit obstruction; and
3. a new odd paired-stream construction whose finite exponent gate is
   compatible, while two-packet survival and the full ledger remain open.

It is not an epsilon-regularity theorem, continuation theorem, global
regularity theorem, singularity construction, or solution of the Millennium
problem. **NOT CLAY.**

## Frozen files and SHA-256

| Artifact | SHA-256 |
|---|---|
| research/r074e_local_mollified_frame_gate.md | 3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7 |
| research/r074e_local_frame_independent_audit.md | 7be3d766010578d2c914b1261f9852534a8acdc7ce213994c0079787e430093b |
| research/r074e_finite_gate_independent_audit.md | 039f0b497f30027dfa25d67e501fb151f8fcd3e8b800f78eac16a08ab6c7f664 |
| scripts/r074e_outer_annulus_exponent_certificate.py | eece8145a024b7d6b22829f9c197f4f74e20e697b9ae74d8721325d1ee07b59b |
| research/r074e_outer_annulus_exponent_certificate.json | c6b7f0b9d11a58568c588dd3116e66fbdb9d7d5b5383493c9b492bf6cdba4372 |
| research/r074e_outer_annulus_exponent_certificate_report.md | 3bb32d68d879682199c3b7673ce6ee403ef7421faf2015744dc4a11ccc565c6e |
| figure package SHA256SUMS | 59a325208fd2eab94f27efcdc45b3915db30d001c4181b56058cfe3331692f68 |
| figure package manifest.json | bb28051f259e77f4d788b369e5be276ccff11f2d8d47dcbb7ea32ff67e4472a3 |
| figure package validation.json | 81e84a208227cf32accfa650836c0fb0b17d4a89c9a91545355c5853bdfc0a19 |

The figure package is

    research/figures/r074e/fig-r074e-outer-annulus-frame-gate/

Its publication masters are:

| Figure file | SHA-256 |
|---|---|
| figure.svg | 8d3cc697e09bce1f8aee1f98f74eeffea41e186e3120240b9a95c16f34ecef87 |
| figure.pdf | 824ba1e2e09f1473af94bb14dfa1d97ad5029800dc8eab4af24aa6ac53d5915a |
| figure.png | 2f57e053ce73c204f7831e3b69740977c5010c5e8aebc326bd7c7c67aab3cab6 |

## Literal mathematical result

### A. Two local frames are inequivalent

For the terminal trajectory

\[
 \dot X_R=u_R(t,X_R),\qquad X_R(t_0)=x_0,
\]

moving without subtracting gives

\[
 \partial_tv_R-\Delta v_R+(v_R-a_R)\cdot\nabla v_R+\nabla\pi_R=0.
\]

Moving and subtracting \(a_R=\dot X_R\) gives

\[
 \partial_tw_R-\Delta w_R+w_R\cdot\nabla w_R+\nabla\pi_R=-a_R'.
\]

The acceleration cannot be hidden in a periodic torus pressure. The matching
mollifier cancels its tested moment exactly at radius \(R\), but no
corresponding automatic cancellation exists at \(2R\), \(8R\), or for
unmatched sharp-ball and shell cutoffs.

### B. The R0.74D explicit family is neutralized

The local trajectory leaves the old packet resident at radius
\(q_m+O(R^2)\) throughout the payment interval. Its kinematic target is
then paid by the algebraic harmonic term. For every member of that explicit
family,

\[
 X_R^M\le C(P_R^M)^{2/3},
 \qquad
 X_R^F\le C(P_R^F)^{2/3}.
\]

This is a complete familywise neutralization, not a proof of either
arbitrary-solution endpoint.

### C. A new exact paired-stream gate survives the finite tests

The frozen parameters are

\[
 \lambda=\frac{63}{32},\quad
 c_h=\frac{15}{16},\quad
 \alpha=\frac{14}{15},\quad
 \beta^2=\frac{31}{256},\quad
 c_R=\frac1{320},\quad \kappa=16.
\]

They satisfy

\[
 \frac4{1323}<\frac1{320}<\frac{49}{14625},
\]

and

\[
 \frac{75}{22528}>\frac1{320}>\frac8{3969}.
\]

The first chain is the nonempty radius-exponent window. The second says the
transverse leakage exponent beats both the inverse-\(R_j\) prefactor and the
annular weight. The strict new margin is

\[
 \frac{75}{22528}-\frac1{320}
 =\frac{23}{112640}>0.
\]

The odd paired field is exact smooth periodic mean-zero unforced NSE, and
even-mollifier symmetry gives

\[
 X_{R_j}\equiv0,\qquad a_{R_j}=a_{R_j}'=0.
\]

Lemma 9.1 also proves \(B_j\asymp R_j^{-2}\) and calibrates the two reference
paths exactly. None of these finite or symmetry facts proves that the
passive packets survive.

## Mechanisms rejected only in their stated scope

- The high-frequency single cosine is rejected as a uniform scale-\(R\)
  perturbative packet mechanism; this is not a universal single-mode no-go.
- The symmetric midpoint two-bump construction has an empty window under
  its direct sufficient estimates \(c_R>1/192\) and \(c_R<1/266240\);
  this is not a universal no-go for plateau constructions.

## What remains open and must be visible on the page

1. the two-packet Feynman--Kac survival lemma;
2. buffered analytic leakage beyond the finite exponent comparison;
3. every transition, packet, mixed-pressure, and periodic-copy row in the
   complete \(E/G_u/G_p/H_u\) ledger;
4. an explicit packet amplitude closing the simultaneous Version-M/F ratio;
5. either arbitrary-solution endpoint and every regularity consequence.

The next research version is R0.74F, beginning with item 1. Publication must
not present that next step as already proved.

## Required publication treatment

Suggested Chinese title:

> R0.74E｜局部随流坐标：旧反例被支付，外环新门槛通过

Suggested lead:

> 这一节没有证明三维 Navier--Stokes 全局光滑性。它完成了两件更基础、
> 也更必要的工作：先把局部随流坐标中的加速度与周期压力严格分开，再证明
> 旧的显式反例族在这个坐标中会被谐和支付项完整吸收。随后，一个具有精确
> 奇对称消去的新双流构造通过了 13 项有限指数检查，但最关键的双包存活与
> 完整账本仍然开放。

Publication checklist:

1. create the R0.74E research-note page in the existing concise retro style;
2. use the supplied SVG as the primary responsive figure, with PNG fallback
   if the current site generator requires it;
3. link the main note, both audits, certificate report, raw JSON, producer
   script, figure caption, and figure QA report;
4. update the research index, route/current-version marker, and home-page
   latest version from R0.74D to R0.74E;
5. do not create a new cumulative recap solely for this section;
6. retain visible PROVED, OPEN, REJECTED MECHANISM, and NOT CLAY boundaries;
7. run the site build and tests, inspect desktop and mobile renderings, and
   verify deployed GitHub Pages HTML and figure bytes against the local
   release.

## Research-side reproduction

From the repository root at the frozen commit:

    python3 scripts/r074e_outer_annulus_exponent_certificate.py \
      | diff -u research/r074e_outer_annulus_exponent_certificate.json -

    python3 -m json.tool \
      research/r074e_outer_annulus_exponent_certificate.json >/dev/null

    cd research/figures/r074e/fig-r074e-outer-annulus-frame-gate
    /Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 plot.py
    /Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 validate.py
    shasum -a 256 -c SHA256SUMS

Expected results:

    certificate: PASS 13/13 and byte-identical JSON
    figure validator: PASS 42/42
    figure package: every SHA256SUMS entry OK

The research task may proceed to R0.74F without waiting for deployment. The
publication task owns site integration and GitHub Pages byte verification.
