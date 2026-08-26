# R0.71Z bounded primary-source literature audit

**Date:** 2026-08-27  
**Scope:** zero sampling, analytic/non-autonomous evolution, finite ECT
zero counts, Dyson--Phillips expansions, and NSE time analyticity.

## 1. Direct literature decision

The R0.71Z theorem is proved from the exact triangular equations. The
literature supplies neighboring frameworks, not the theorem itself.

1. Scattered-zero Sobolev inequalities use fill distance and do not give the
   discrete zero-count-independent derivative mass used here.
2. Analytic-semigroup and non-autonomous maximal-regularity theory does not
   turn a merely bounded time-dependent perturbation into an automatic
   \(H_t^2\) estimate. R0.71Z avoids that promotion by differentiating one
   explicit target row and paying it with exact dissipation.
3. ECT theory controls a fixed finite-dimensional exponential space.
   Dyson--Phillips is an infinite iterated-integral expansion. The first
   cannot be applied to the second without finite closure or a separate
   complex-tail zero-stability theorem.
4. NSE time analyticity isolates zeros of a nontrivial fixed observable, but
   does not bound their count or total squared slope from the launch data.

No checked source states the R0.71Z all-root BV estimate, the combined
dissipation row, or the launch-inclusive \(\mathcal R_Y\) cancellation. This
is a bounded non-collision finding, not a claim of originality, priority, or
nonexistence.

## 2. Claim--source--gap ledger

| ID | primary or authoritative source | what it supports | what it does not support here |
|---|---|---|---|
| ZL1 | Francis J. Narcowich, Joseph D. Ward, and Holger Wendland, “Sobolev bounds on functions with scattered zeros, with applications to radial basis function surface fitting,” *Mathematics of Computation* 74 (2005), [DOI](https://doi.org/10.1090/S0025-5718-04-01708-9) | Lower Sobolev seminorms of scalar functions vanishing on a scattered set can be controlled by higher seminorms with an explicit fill-distance power. | No discrete \(\sum|u'(t_k)|^2\), no zero-count/separation-free constant, no Hilbert-valued curve theorem, and no R0.71Z BV identity. |
| ZL2 | A. Pazy, *Semigroups of Linear Operators and Applications to Partial Differential Equations* (Springer, 1983), [publisher/DOI](https://doi.org/10.1007/978-1-4612-5561-1) | Analytic-semigroup smoothing and bounded autonomous perturbation theory. | No automatic \(u''\in L^2_t\) for an arbitrary time-varying bounded perturbation and no constants uniform in the present carrier geometry. |
| ZL3 | Tosio Kato, “Integration of the equation of evolution in a Banach space,” *Journal of the Mathematical Society of Japan* 5 (1953), [DOI](https://doi.org/10.2969/jmsj/00520208) | Construction of non-autonomous evolution operators under explicit stability and domain assumptions. | No project-specific second-time estimate, target-row cancellation, or all-root slope mass. |
| ZL4 | Paolo Acquistapace and Brunello Terreni, “Maximal space regularity for abstract linear non-autonomous parabolic equations,” *Journal of Functional Analysis* 60 (1985), [DOI](https://doi.org/10.1016/0022-1236(85)90050-3) | Maximal regularity for non-autonomous parabolic equations under quantitative generator/domain continuity hypotheses. | A uniformly bounded \(V(t)\) alone does not imply \(u''\in L^2\); the AT constants and hypotheses cannot be imported without verification. |
| ZL5 | Paolo Acquistapace and Brunello Terreni, “A unified approach to abstract linear nonautonomous parabolic equations,” *Rendiconti del Seminario Matematico della Università di Padova* 78 (1987), [NUMDAM full text](https://www.numdam.org/item/RSMUP_1987__78__47_0/) | Existence, uniqueness, strict/classical solutions, and maximal-regularity framework with changing domains. | No carrier-uniform R0.71Z \(Q\)-row estimate and no zero-sampling result. |
| ZL6 | Paolo Acquistapace and Brunello Terreni, “Regularity properties of the evolution operator for abstract linear parabolic equations,” *Differential and Integral Equations* 5 (1992), [DOI](https://doi.org/10.57262/die/1370870947) | Refined time-space regularity of evolution operators under AT conditions. | No license to claim dimension- and \(q\)-uniform second derivatives before checking all constants and domains. |
| ZL7 | R. S. Phillips, “Perturbation theory for semi-groups of linear operators,” *Transactions of the AMS* 74 (1953), [DOI](https://doi.org/10.1090/S0002-9947-1953-0054167-3) | Dyson--Phillips series for bounded perturbations; the paper also treats strongly differentiable time-varying bounded perturbations. | Absolute series convergence does not place the sum in a fixed finite ECT space and gives no uniform real-zero count. |
| ZL8 | J. M. Aldaz, O. Kounchev, and H. Render, “Bernstein operators for exponential polynomials,” *Constructive Approximation* 29 (2009), [DOI](https://doi.org/10.1007/s00365-008-9010-6) | ECT structure for the finite-dimensional kernel of a fixed finite-order constant-coefficient differential operator, with interval restrictions for complex exponents. | No zero count for an infinite Dyson expansion, a time-dependent generator, or dimension tending to infinity. |
| ZL9 | Samuel Karlin and William J. Studden, *Tchebycheff Systems: With Applications in Analysis and Statistics* (1966), [catalogue](https://books.google.com/books/about/Tchebycheff_Systems.html?id=P7Y-AAAAIAAJ) | Classical T/ET/ECT definitions, interpolation nondegeneracy, and finite-dimensional zero counting. | No growing-dimensional conditioning or exact nonlinear all-root theorem. |
| ZL10 | Kyuya Masuda, “On the Analyticity and the Unique Continuation Theorem for Solutions of the Navier--Stokes Equation” (1967), [DOI](https://doi.org/10.3792/pja/1195521421) | Time analyticity and unique continuation for classical NSE solutions. | Analyticity does not give a data-uniform root count, root separation, or squared-slope mass. |
| ZL11 | Giga, Jo, Mahalov, and Yoneda, “On time analyticity of the Navier--Stokes equations with spatially almost periodic data,” *Physica D* 237 (2008), [DOI](https://doi.org/10.1016/j.physd.2008.03.007) | Holomorphic time sectors for a Fourier class and a no-sudden-creation consequence. | No \(M^{-2}\) payment, no all-root slope sum, and no launch-inclusive enstrophy cancellation. |

## 3. Why bounded time dependence is insufficient

A scalar example prevents an unjustified regularity shortcut. Let

\[
 A(t)=b(t)I,\qquad
 b(t)=|t-t_0|^\alpha,\qquad0<\alpha\le\frac12.
\]

This is a bounded Hölder time-dependent perturbation of the zero analytic
generator. The solution

\[
 u(t)=\exp\left(\int_{t_0}^tb(s)\,ds\right)
\]

satisfies \(u'=bu\), but

\[
 u''=(b'+b^2)u,\qquad
 |b'(t)|\asymp|t-t_0|^{\alpha-1}\notin L^2_{\rm loc}.
\]

Thus bounded, or low-order Hölder, time dependence alone cannot supply the
second-time row. In the exact R0.71Z class, \(V_z\) is an explicit finite
heat-mode sum. The proof differentiates only

\[
 P_0V_zF
\]

and combines \(V_z'\) with \(V_z(D_q+\lambda_0)\). Its \(L_x^1\) norm is
paid by one shear heat derivative and one factor of the exact scalar
dissipation. This project-specific step is not delegated to abstract maximal
regularity.

## 4. Why finite ECT does not count the complete Dyson zeros

The finite-dimensional limitation is sharp. Given distinct real points
\(t_1,\ldots,t_N\),

\[
 p_N(t)=\prod_{k=1}^N(e^t-e^{t_k})
 =\sum_{j=0}^Nc_je^{jt}
\]

belongs to an \(N+1\)-dimensional real exponential ECT space and has exactly
\(N\) distinct zeros. Therefore the statement “every finite truncation is
ECT” cannot yield a truncation-independent root count.

Phillips' Dyson--Phillips expansion has the form

\[
 S(t)=\sum_{m=0}^\infty S_m(t),\qquad
 S_{m+1}(t)=\int_0^tT(t-s)BS_m(s)\,ds.
\]

Uniform convergence on a real interval is insufficient to stabilize all
zeros. An all-root count would additionally require one of:

1. an exact invariant subspace of uniformly bounded finite dimension;
2. a scalar annihilating ODE of uniformly bounded order;
3. complex-neighborhood tail control relative to a nonzero boundary minimum,
   permitting Rouché or Jensen;
4. another zero-number or variation-diminishing theorem whose hypotheses are
   verified for the nonlinear target coordinate.

R0.71Z needs none of these because it controls the total slope mass without
counting the zeros.

## 5. Wording constraints carried into the release

- The BV sampling lemma is proved directly and is not attributed to the
  scattered-zero theorem.
- ECT is described as a finite-dimensional neighboring theory, not an
  all-Dyson root theorem.
- Abstract maximal regularity is not cited as the proof of the \(Q\)-row
  estimate.
- Time analyticity supports qualitative isolation only.
- The fixed-window heat-shear example disproves automatic retention, not the
  entire fixed-window floor-free atom estimate.
- No statement of novelty, priority, universal regularity, or singularity is
  inferred from the bounded search.
