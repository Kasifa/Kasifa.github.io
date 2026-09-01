# R0.73X pressure and exterior-tail primary-source ledger

**Audit date:** 2026-09-01

**Status:** `PRIMARY-SOURCE DESIGN LEDGER / NO PRESSURE CLOSURE CLAIM`

**Scope:** standard local-pressure decompositions, heat off-diagonal decay,
and the boundary between those tools and the unresolved R0.73X pressure
covariance estimate

**DGX used:** false

## 1. Decision

The exterior ledger cannot be represented by one undifferentiated
"Gaussian error."  Three mechanisms have to be separated:

1. direct heat transport of velocity or \(pu\), which has Gaussian
   off-diagonal decay once the source norm is paid;
2. the nonlocal pressure/Leray contribution, which is represented on an
   interior ball by a local singular-integral part plus a spatially harmonic
   remainder and generally has only algebraic annular decay; and
3. the positive Carleson/CKN endpoint, which is not implied by cancellation
   in signed production.

This ledger licenses a design, not a theorem controlling the original

\[
 Q_s=P_s(pu)-P_sp\,P_su.
\tag{1.1}
\]

## 2. Primary-source rows

| Source | Established tool used here | Boundary for R0.73X |
|---|---|---|
| J. Wolf, *On the local pressure of the Navier--Stokes equations and related systems*, Theorem 6.4 and Corollary 6.5 ([arXiv:1611.01482](https://arxiv.org/abs/1611.01482), [DOI](https://doi.org/10.57262/ade/1489802453)) | A local pressure representation with a spatially harmonic pressure component and local projection estimates | It is a changed local representation; it is not a direct estimate for (1.1) |
| H. Kwon, *The role of the pressure in the regularity theory for the Navier--Stokes equations*, Definition 2.1 and Lemma 2.5 ([arXiv:2104.03160](https://arxiv.org/abs/2104.03160), [DOI](https://doi.org/10.1016/j.jde.2023.01.049)) | A localized Leray projection and decomposition \(u=v+h\), with \(h\) harmonic and smooth on an inner ball | A pressure-free \(v+h\) ledger would change both the equation and the production term and must be rederived |
| H. Jia and V. Šverák, *Local-in-space estimates near initial time...*, equations (3.3)--(3.6) ([arXiv:1204.0529](https://arxiv.org/abs/1204.0529), [DOI](https://doi.org/10.1007/s00222-013-0468-x)) | Near/far pressure splitting; the far kernel difference has one additional inverse power and is harmonic in the inner region | The result uses a whole-space local-Leray setting and corresponding uniform local-energy/decay hypotheses |
| Z. Bradshaw and T.-P. Tsai, *On the local pressure expansion for the Navier--Stokes equations*, equations (1.7)--(1.9) and Theorems 1.4--1.5 ([arXiv:2001.11526](https://arxiv.org/abs/2001.11526), [DOI](https://doi.org/10.1007/s00021-021-00637-4)) | A precise distributional local pressure expansion, with pressure determined modulo a time-dependent constant | The expansion is tied to the paper's mild/LPE solution class; it is not automatic for every distributional solution |
| T. Coulhon and A. Sikora, *Gaussian heat kernel upper bounds via Phragmén--Lindelöf theorem*, Davies--Gaffney estimate (3.2) and Theorems 1.1--1.2 ([arXiv:math/0609429](https://arxiv.org/abs/math/0609429), [DOI](https://doi.org/10.1112/plms/pdm050)) | Separated supports for a heat semigroup carry Gaussian off-diagonal decay | Decay of the operator does not create integrability or smallness of the remote source |
| H. Koch and D. Tataru, *Well-posedness for the Navier--Stokes equations* ([author manuscript](https://math.berkeley.edu/~tataru/papers/nas.pdf), [DOI](https://doi.org/10.1006/aima.2000.1937)) | The critical mild space contains positive caloric cylinder/Carleson control; the projected Oseen kernel has algebraic spatial decay | It is a small-data mild theory, not a signed-production-to-positive-tent theorem for arbitrary suitable weak solutions |

## 3. Frozen design skeleton

Let

\[
 A_k=B_{2^{k+1}R}(x_0)\setminus B_{2^kR}(x_0),\qquad
 E_k(t)={1\over2^kR}\int_{A_k}|u(y,t)|^2\,dy.
\tag{3.1}
\]

The direct Gaussian rows may be organized schematically as

\[
 \mathcal A^{G,u}_{\rm ext}
 \sim\sum_{k\ge1}\theta^{-3/4}2^{k/2}
 e^{-c4^k/\theta}\,E_k^{1/2},
\tag{3.2}
\]

and an analogous \(\mathcal A^{G,pu}_{\rm ext}\) must separately pay an
annular \(L^1\) or Hölder-controlled norm of \(pu\).  The exponential weight
comes from the heat operator; it is not a bound on the source.

The local-pressure far field instead has the standard algebraic skeleton

\[
 \mathcal A^{p,\mathrm{far}}_{\rm ext}
 \sim\sum_{k\ge1}2^{-3k}E_k,
\tag{3.3}
\]

after fixing the pressure gauge and the exact time norm.  Formula (3.3) is a
design row inherited from the kernel-difference mechanism; its sufficiency
for the original covariance (1.1) has not been proved here.

Accordingly the full candidate must retain at least

\[
 \boxed{
 \mathcal A_{\rm ext}
 =\mathcal A^{G,u}_{\rm ext}
 +\mathcal A^{G,pu}_{\rm ext}
 +\mathcal A^{p,\mathrm{far}}_{\rm ext}.}
\tag{3.4}
\]

Every term in (3.4) still needs an exact time norm, solution class, and
pressure convention before it can enter a theorem.

## 4. Three unresolved bridges

1. **Original covariance.**  No cited source proves a non-circular
   energy-class estimate for the exact \(Q_s\) in (1.1) from (3.4).
2. **Scale smallness.**  Standard annular estimates give a finite or bounded
   tail under additional hypotheses, not automatic smallness as
   \(R\downarrow0\) at a possible singular point.
3. **Signed to positive.**  The known Koch--Tataru and CKN-facing entry
   quantities are positive absolute norms or dissipation measures.  No cited
   theorem converts a signed heat-characteristic payment into their
   smallness.

The bounded primary-source search therefore supports the decomposition of
the problem but not a pressure closure, novelty claim, epsilon-regularity
criterion, or Clay conclusion.

NOT CLAY.
