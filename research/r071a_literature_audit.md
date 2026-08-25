# R0.71A literature audit — projector coherence and common-response compensation

**Date:** 2026-08-25

**Scope:** a bounded primary-source audit for two questions:

1. whether a published Navier--Stokes criterion already controls the
   principal projector of an analysis-frame covariance on
   \(2/q_t+3/p_x=1\);
2. whether an established Hardy/BMO or Carleson theorem automatically closes
   the exact R0.70Z common-response trace from Leray energy.

This is not a systematic review and makes no priority claim.

## 1. Result matrix

| Published result | Exact object and hypothesis | Relation to R0.71A | Decision |
|---|---|---|---|
| [Chae--Choe 1999](https://www.kurims.kyoto-u.ac.jp/EMIS/journals/EJDE/Volumes/1999/05/chae.pdf) | A fixed plane; two vorticity components in \(L_t^{q_t}L_x^{p_x}\) with \(2/q_t+3/p_x=2\), \(3/2<p_x<\infty\) | No variable projector and no frame covariance | Established neighbor, not the target |
| [Miller 2021, Theorem 1.6](https://arxiv.org/pdf/2002.02152) | A variable unit normal \(v\); \(\nabla v\in L_{\mathrm{loc},t}^\infty L_x^\infty\) and \(v\times\omega\in L_t^4L_x^2\) | This is the oriented whole-space source of the R0.70P consumer | R0.70P is a projector rewrite, not a new mixed-norm family |
| [Miller 2021, Remark 3.3](https://arxiv.org/pdf/2002.02152v1) | Proposes \(\nabla v\in L_t^4L_x^\infty\), but states that the integration-by-parts/middle-eigenvalue proof cannot provide it because of the transpose asymmetry | Even this proposed \(L_t^4L_x^\infty\) relaxation is open in that proof; R0.71A's critical endpoint is the weaker \(L_t^2L_x^\infty\) condition | Direct evidence for a method boundary, not evidence that the desired theorem is false |
| [Beir\~ao da Veiga--Berselli 2002, Corollary 4.2](https://people.dm.unipi.it/beiraodaveiga/pdf/hbv-79.pdf) | The physical vorticity direction \(\xi=\omega/|\omega|\); \(\nabla\xi\in L_t^{q_t}L_x^{p_x}\) with \(2/q_t+3/p_x=1/2\) | Uses physical-direction depletion in the Biot--Savart kernel; does not treat \(P_1(Q)\) | The \(1/2\) line for physical \(\xi\) is known and must not be relabeled as the covariance-projector target |
| [Beir\~ao da Veiga--Berselli 2002, Corollary 4.3](https://people.dm.unipi.it/beiraodaveiga/pdf/hbv-79.pdf) | Physical direction in Nikol'skij/Besov classes with \(2/q_t+3/p_x=\alpha-1/2\), \(1/2\le\alpha\le1\) | A fractional physical-direction family | Established; different geometric object and mechanism |
| [Chae 2006, Theorem 2](https://www.impan.pl/shop/en/publication/transaction/download/product/86213) | Physical direction in a Triebel--Lizorkin space coupled to a separate vorticity-amplitude norm | With only Leray's \(\omega\in L_t^2L_x^2\), the condition becomes \(3/p_1+2/r_1\le s-1/2\) | Shows that direction regularity and amplitude can trade, but does not give the R0.71A pure critical projector condition |
| [Constantin--Fefferman 1993](https://iumj.org/article/3627/) | Coherence of the physical vorticity direction in the high-vorticity region depletes the Biot--Savart stretching kernel | The physical direction is not the principal direction of the analysis covariance | Conceptual neighbor only |
| [CLMS 1993](https://zbmath.org/0864.42009) | If \(E,B\in L^2\), \(\operatorname{div}E=0\), and \(\operatorname{curl}B=0\), then \(E\cdot B\in\mathcal H^1\) with the div--curl bound | Taking \(E=\omega\), \(B=\nabla u_j\) yields the established Hardy endpoint for the full common channel | Supplies compensation only after a BMO-side coefficient is controlled |
| [Kozono--Taniuchi 2000](https://doi.org/10.1007/s002090000130) | Bilinear BMO estimates and a Navier--Stokes BMO regularity criterion | A known sufficient common-channel endpoint | Does not produce BMO from \(Q\), its gap, or \(P_1\) |
| [Bradshaw--Gruji\'c 2013/2015](https://arxiv.org/pdf/1309.2519) | Local Hardy--bmo duality, a logarithmically weighted direction coefficient, and an \(L\log L\) vorticity conclusion | Shows that direction-weighted common-channel compensation is established beyond direct BMO | Does not imply the R0.70P residual/commutator hypotheses or continuation |

## 2. Exact distinctions that matter

### 2.1 The two critical lines are not interchangeable

For a dimensionless projector or unit direction transported by the
Navier--Stokes scaling,

\[
 \|\nabla L\|_{L_t^qL_x^p}
 \quad\hbox{is invariant when}\quad
 \frac2q+\frac3p=1.
 \tag{2.1}
\]

Beir\~ao da Veiga--Berselli's gradient theorem assumes instead

\[
 \frac2q+\frac3p=\frac12.
 \tag{2.2}
\]

Condition (2.2) is stronger.  More importantly, it concerns
\(\xi=\omega/|\omega|\), for which the Biot--Savart kernel exposes a
two-point angular cancellation.  A covariance projector has no automatic
access to that cancellation.

### 2.2 A variable plane needs both geometry and transverse amplitude

Miller's theorem assumes

\[
 \nabla v\in L_{\mathrm{loc},t}^\infty L_x^\infty,
 \qquad
 v\times\omega\in L_t^4L_x^2.
 \tag{2.3}
\]

The first factor controls variation of the plane; the second measures the
vorticity actually lying in that plane.  R0.71A's constant-projector family
has perfect control of the first factor but a nonzero lower-plane residual.
It therefore fits, rather than contradicts, the structure of (2.3).

### 2.3 CLMS does not manufacture its BMO partner

The CLMS div--curl lemma gives

\[
 \|\omega\cdot\nabla u_j\|_{\mathcal H^1}
 \lesssim\|\omega\|_2\|\nabla u_j\|_2.
 \tag{2.4}
\]

Hardy--BMO duality controls a pairing only when the other coefficient has a
BMO bound.  Neither a principal eigengap nor \(\nabla P_1=0\) supplies that
bound for the exact response trace.  Assuming an unweighted Carleson norm
for the trace would restate the missing gate.

## 3. Bounded search record

The checked concepts included:

- variable vorticity plane regularity;
- gradient of vorticity direction in mixed Lebesgue spaces;
- spectral or covariance projector regularity for Navier--Stokes;
- direction Triebel--Lizorkin and Nikol'skij criteria;
- div--curl Hardy space and BMO endpoints;
- direction-weighted local bmo and Carleson compensation;
- exact response or analysis-frame covariance stretching.

No checked primary source contained a theorem whose hypotheses and object
match

\[
 \nabla P_1(Q)\in L_t^{q_t}L_x^{p_x},
 \qquad
 \frac2{q_t}+\frac3{p_x}=1,
 \tag{3.1}
\]

for the principal projector of an analysis-frame covariance.  No checked
source derived an unconditional R0.70Z common-response Carleson closure from
Leray energy.  These are bounded negative-search statements, not proof of
novelty.

## 4. Safe claim matrix

### Established and therefore not new

- fixed-plane two-vorticity-component criteria;
- Miller's Lipschitz variable-plane criterion;
- the physical-vorticity-direction gradient line
  \(2/q_t+3/p_x=1/2\);
- fractional physical-direction criteria coupled to vorticity amplitude;
- CLMS followed by an assumed BMO or local-bmo coefficient.

### Narrow R0.71A contribution

- an exact same-covariance sign pair whose principal projector is constant,
  whose eigengap is strong, and whose scalar-frame commutator is zero;
- a theorem-grade \(L_t^1\) estimate on the critical covariance-projector
  line;
- a compact-seed scaling obstruction to the corresponding direct
  energy-level \(L_t^2\) estimate;
- a finite-\(p\) weighted continuation family, explicitly classified as a
  conditional interpolation extension.

### Still open in this route

- a continuation theorem from the pure critical condition (3.1) plus a
  non-tautological covariance-to-vorticity coupling;
- propagation of the residual and exact frame commutator at the needed
  time exponent;
- a signed or Carleson estimate for the exact common-response trace that is
  derived rather than assumed.
