# R0.73Q primary-literature audit: critical neighborhoods and endpoint limits

**Status:** bounded primary-source pass complete; direct collision found;
Mucha 2001 full-theorem quantifiers remain unavailable

**Audit rule:** a statement is promoted to `VERIFIED_THEOREM` only when the
primary text or a legible theorem page was inspected.  Publisher abstracts
are labeled `ABSTRACT_ONLY`.  Whole-space theorems are not silently imported
to the fixed torus.

## 1. Corpus and release question

The audited question is not whether any critical stable neighborhood exists.
It is whether R0.73Q may defensibly publish the following fixed-domain
combination:

1. a given arbitrary three-dimensional global \(H^3\) reference orbit on
   \(\mathbb T^3\);
2. a finite-index critical heat-flow topology strictly weaker than
   \(H^{1/2}\);
3. one positive radius valid at every restart time;
4. a displayed periodic linearized inverse bound and an exact smooth
   strictness witness.

The primary corpus comprises Kato 1984, Iftimie 1999, Mucha 2001 and 2008,
Koch--Tataru 2001, Gallagher--Iftimie--Planchon 2003,
Auscher--Dubois--Tchamitchian 2004, and Coiculescu--Palasek 2025/2026.

## 2. Kato 1984: critical \(L^3\), not an \(L^2\)-only theorem

**Source.** Tosio Kato, *Strong \(L^p\)-Solutions of the Navier--Stokes
Equation in \(\mathbb R^m\), with Applications to Weak Solutions*,
Mathematische Zeitschrift 187 (1984), 471--480,
[DOI 10.1007/BF01174182](https://doi.org/10.1007/BF01174182),
[GDZ scan](https://gdz.sub.uni-goettingen.de/id/PPN266833020_0187).

**Verified theorem boundary.** The domain is \(\mathbb R^m\).  In dimension
three the scale-invariant datum is \(L^3\).  Kato constructs the local mild
solution for divergence-free \(L^3\) data and obtains a global solution under
a sufficiently small \(L^3\) norm.  The uniqueness assertion is in the
weighted smoothing class stated in Theorem 1; this audit does not promote it
to unconditional uniqueness in bare \(C_tL^3_x\).

**R0.73Q use.** `BACKGROUND_ONLY`.  It confirms that a critical heat norm can
be small while an energy or high Sobolev norm behaves differently.  It does
not provide the fixed-torus relative-orbit radius and cannot be weakened to
an unrestricted \(L^2\) threshold.

## 3. Koch--Tataru 2001: the full Carleson endpoint

**Source.** Herbert Koch and Daniel Tataru, *Well-posedness for the
Navier--Stokes Equations*, Advances in Mathematics 157 (2001), 22--35,
[author PDF](https://math.berkeley.edu/~tataru/papers/nas.pdf),
[DOI 10.1006/aima.2000.1937](https://doi.org/10.1006/aima.2000.1937).

**Verified definitions.** The domain is \(\mathbb R^n\).  Their datum norm is
the heat-extension Carleson norm

\[
 \|a\|_{BMO^{-1}}
 =\sup_{x,R>0}
 \left(|B(x,R)|^{-1}
 \int_0^{R^2}\!\int_{B(x,R)}|e^{t\Delta}a|^2\,dy\,dt
 \right)^{1/2}.
 \tag{3.1}
\]

The solution norm \(X\) contains both

\[
 \sup_{t>0}\sqrt t\|u(t)\|_\infty
 \tag{3.2}
\]

and the corresponding local parabolic-cylinder \(L^2\) Carleson term.

**Verified theorems.** Theorem 2 gives a unique **small** global solution in
\(X\) when the divergence-free \(BMO^{-1}\) datum is sufficiently small.
Theorem 3 gives the local \(BMO^{-1}_R\) version up to time \(R^2\), hence
local theory for the stated \(VMO^{-1}\) class.

**R0.73Q use.** `ENDPOINT_BOUNDARY`.  A bare Kato supremum is not the
Koch--Tataru norm.  R0.73Q therefore cannot infer a periodic
\(BMO^{-1}\) theorem from the single finite action
\(u\in L^4_tL^6_x\).

## 4. Iftimie 1999: a periodic domain already larger than \(H^{1/2}\)

**Source.** Drago\c{s} Iftimie, *The 3D Navier--Stokes equations seen as a
perturbation of the 2D Navier--Stokes equations*, Bulletin de la Soci\'et\'e
Math\'ematique de France 127 (1999),
[primary PDF](https://www.numdam.org/item/10.24033/bsmf.2358.pdf),
[DOI 10.24033/bsmf.2358](https://doi.org/10.24033/bsmf.2358).

**Verified theorem boundary.** The domain is \(\mathbb T^3\).  Theorem 2.1
takes the two-dimensional/three-component reference part to be the vertical
average \(v_0=Mu_0\); Theorem 2.2 permits a separately prescribed
two-dimensional component \(v_0\), which need not equal that average.  For
\(0<\delta<1\), the three-dimensional remainder is controlled in
\(H^{\delta,1/2-\delta}\) under the paper's explicit smallness condition
relative to the two-dimensional energy.  The conclusion is a unique global
solution with all-time anisotropic bounds.

For \(0<\delta<1/2\), strict enlargement beyond isotropic \(H^{1/2}\) is an
elementary Fourier-weight consequence of those anisotropic spaces.  It is
recorded here as `PRIMARY_THEOREM_PLUS_ELEMENTARY_COMPARISON`, not as a
verbatim theorem sentence from the paper.

**R0.73Q use.** `DIRECT_GEOMETRIC_COLLISION`.  The phrase "a periodic stable
domain larger than \(H^{1/2}\)" is not new.  Iftimie's domain is organized
around the two-dimensional invariant subspace, while R0.73Q fixes an
arbitrary already-global three-dimensional orbit and uses an isotropic
heat-flow trace.

## 5. Mucha: what the \(L^2\)-small statements do and do not say

### 5.1 Mucha 2001 on the three-torus

**Source.** Piotr B. Mucha, *Stability of Nontrivial Solutions of the
Navier--Stokes System on the Three Dimensional Torus*, Journal of
Differential Equations 172 (2001), 359--375,
[publisher page](https://www.sciencedirect.com/science/article/pii/S0022039600938634),
[DOI 10.1006/jdeq.2000.3863](https://doi.org/10.1006/jdeq.2000.3863).

**Accessible evidence.** `ABSTRACT_ONLY`.  The publisher abstract states that
the domain is the three-dimensional torus and that a perturbation's
\(W^{2,1}_r\) norm can be controlled when its initial datum is sufficiently
small in \(L^2\); unforced two-dimensional flows are included.

**Unverified quantifiers.** This bounded pass did not obtain the full theorem
text.  The admissible \(r\), trace regularity, dependence of the \(L^2\)
threshold on the reference orbit or higher norms, and the exact uniqueness
class therefore remain `UNRESOLVED_SOURCE_DETAIL`.

**R0.73Q rule.** No claim relies on reconstructing those missing details.
The paper is retained as the closest periodic collision.

### 5.2 Mucha 2008 on high-trace-dependent \(L^2\) smallness

**Source.** Piotr B. Mucha, *Global solutions, structure of initial data and
the Navier--Stokes equations*, Banach Center Publications 81 (2008),
[official full text](https://www.impan.pl/shop/en/publication/transaction/download/product/86758),
[DOI 10.4064/bc81-0-18](https://doi.org/10.4064/bc81-0-18).

**Verified Theorem 1.2 boundary.** The indices satisfy

\[
 1<p,q<\infty,
 \qquad {3\over p}+{2\over q}<3.
\]

The datum belongs to \(B^{2-2/q}_{p,q}(\Omega)\cap L^2(\Omega)\), and the
required \(L^2\) smallness is relative to the higher Besov trace norm.  The
conclusion is a unique global regular solution with uniform unit-time-slab
\(W^{2,1}_{p,q}\) control on the stated class of domains.

**R0.73Q use.** `EXCLUSION_SOURCE`.  It does not yield a higher-norm-
independent \(L^2\) ball.

## 6. Gallagher--Iftimie--Planchon 2003: the strongest direct collision

**Source.** Isabelle Gallagher, Drago\c{s} Iftimie, and Fabrice Planchon,
*Asymptotics and Stability for Global Solutions to the Navier--Stokes
Equations*, Annales de l'Institut Fourier 53 (2003), 1387--1424,
[primary PDF](https://www.numdam.org/item/10.5802/aif.1983.pdf),
[DOI 10.5802/aif.1983](https://doi.org/10.5802/aif.1983).

**Verified domain and index range.** The equation is posed on \(\mathbb R^3\).
The paper works in homogeneous critical Besov spaces

\[
 \dot B^{3/p-1}_{p,q}(\mathbb R^3),
 \qquad 1\le p,q<\infty,
 \tag{6.1}
\]

with the proof reduced to the displayed \(p\ge3\) regime when convenient.
The finite \(q\) hypothesis is used in the time decomposition; Remark 3.2
records an additional closure condition at \(q=\infty\).

**Verified Theorem 3.1.** Let a divergence-free datum \(u_0\) in (6.1)
generate an a priori global solution continuous in that critical space,
belonging to the canonical fixed-point/uniqueness branch stated in the
theorem.  The reference trajectory is controlled with an auxiliary time
index \(r_0\) satisfying

\[
 2<r_0<{2\over1-3/p}.
 \tag{6.2a}
\]

Thus, at \(p=6\), one chooses \(2<r_0<4\); the proof does not place the
reference trajectory at the endpoint \(r_0=4\).  There is then
\(\eta_0>0\), depending on \(p,q\) and the stated finite global
Chemin--Lerner norm of the reference solution, such that every divergence-
free \(v_0\) with

\[
 \|v_0-u_0\|_{\dot B^{3/p-1}_{p,q}}\le\eta_0
 \tag{6.2}
\]

generates a global solution.  Distinct from the auxiliary \(r_0\), the
theorem's difference estimate covers every displayed \(1\le r\le\infty\):
it is uniform in time in the critical Besov norm and holds in the stated
\(\widetilde L^r_t\dot B^{3/p+2/r-1}_{p,q}\) norms.  The proof explicitly
partitions time so the reference norm is small on each piece.

For \(p=6,q=4\), (6.1) is precisely
\(\dot B^{-1/2}_{6,4}\), the whole-space counterpart of the R0.73Q heat
trace.

**R0.73Q use.** `DIRECT_COLLISION`.  Openness around a large global orbit in
this critical topology is classical.  The release may claim only its
self-contained periodic all-restart corollary and explicit certificate, not
a new Besov stability principle.

## 7. Auscher--Dubois--Tchamitchian 2004: whole-space endpoint openness

**Source.** Pascal Auscher, Sandrine Dubois, and Philippe Tchamitchian,
article identified by DOI 10.1016/j.matpur.2004.01.003, Journal de
Math\'ematiques Pures et Appliqu\'ees 83 (2004), 673--697.  The accessible
publisher metadata truncates the title after “in the space”, so this audit
does not reconstruct the omitted mathematical typography from that record.
[publisher record](https://www.sciencedirect.com/science/article/pii/S0021782404000042),
[DOI 10.1016/j.matpur.2004.01.003](https://doi.org/10.1016/j.matpur.2004.01.003).

**Abstract-level claim boundary.** On \(\mathbb R^3\), global
solutions in the Koch--Tataru class arising from \(VMO^{-1}\) data decay at
infinity and depend analytically on their data.  The publisher abstract
reports that the corresponding set of Cauchy data generating such global
solutions is open in the \(BMO^{-1}\) topology.  It does not expose a radius,
the full perturbation quantifiers, or a theorem-level uniqueness statement.

**Access label.** `ABSTRACT_ONLY (publisher abstract inspected)`; no explicit
radius, full uniqueness class, or linearized inverse constant is imported
because the full theorem formulas were not accessible in this pass.

**R0.73Q use.** `ABSTRACT_ONLY_COLLISION`.  It reports qualitative endpoint
openness on the whole space at abstract level.  It does not supply the
periodic quantitative statement from the sole R0.73P action.

## 8. Coiculescu--Palasek 2025/2026: unrestricted nonperturbative \(BMO^{-1}\) uniqueness is false

**Source.** Matei P. Coiculescu and Stan Palasek, *Non-Uniqueness of Smooth
Solutions of the Navier--Stokes Equations from Critical Data*, Inventiones
Mathematicae 244 (2026), 165--219,
[arXiv v2 primary PDF](https://arxiv.org/pdf/2503.14699),
[DOI 10.1007/s00222-025-01396-z](https://doi.org/10.1007/s00222-025-01396-z).

**Verified Theorem 1.2.** On the standard three-torus there exists
divergence-free \(U^0\in BMO^{-1}\) for which the Cauchy problem has two
distinct global solutions.  For \(j=1,2\),

\[
 u^{(j)}\in C^\infty((0,\infty)\times\mathbb T^3)
 \cap L^\infty([0,\infty);BMO^{-1})
 \cap C^0([0,\infty);\dot W^{-1,p})
 \quad\hbox{for every }p<\infty.
\]

**Verified remarks.** Remark 1.3 states that both solutions have finite norm
in the natural Koch--Tataru path space and are not perturbative around zero.
This wording supplies no numerical lower bound for their \(BMO^{-1}\) norm.
Remark 1.5 states that the constructed solutions are not Leray--Hopf because
the initial datum is not in \(L^2\).

**R0.73Q use.** `HARD_ENDPOINT_BOUNDARY`.  The release must not say that
arbitrary nonperturbative periodic \(BMO^{-1}\) data have a unique global
mild branch.  This result does not contradict Koch--Tataru small-data
uniqueness and does not affect the finite-index \(L^4_tL^6_x\) fixed point
proved in R0.73Q.

## 9. Collision verdict and safe contribution

The audit verdict is:

```text
criticalSmallDataMechanism=CLASSICAL
wholeSpaceLargeOrbitBesovOpenness=VERIFIED_DIRECT_COLLISION
wholeSpaceVMOInverseOrbitBMOOpenness=VERIFIED_ABSTRACT_COLLISION
periodicAnisotropicDomainBeyondH12=VERIFIED_DIRECT_COLLISION
periodicArbitrary3DOrbitExplicitB64AllRestartRadius=NOT_FOUND_AS_SOURCE_THEOREM
nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL
uniformL2OnlyStrongRadius=OPEN
clayConclusion=OPEN
noveltyOrPriority=NOT_CLAIMED
```

The safe R0.73Q contribution is consequently narrow and auditable:

- prove the periodic \(L^4_tL^6_x\) bilinear estimate directly;
- turn the finite R0.73P orbit action into one explicit inverse bound valid
  at every restart time;
- adjoin the resulting heat-flow tube to the older \(H^{1/2}\) tube;
- certify by exact smooth Fourier modes that the union is a strict set
  enlargement;
- retain the unrestricted early \(L^2\)-only interface as open.

That package is a useful fixed-domain synthesis and a reproducible theorem
corollary.  It is not a new critical-space stability theory and it does not
advance the arbitrary-data alternative in the Millennium problem.
