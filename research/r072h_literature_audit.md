# R0.72H literature audit -- non-autonomous mixed rows and temporal zero sampling

**Search cutoff:** 2026-08-27

**Scope:** primary papers, publisher records, DOI pages, and arXiv records
covering non-autonomous maximal regularity, observation admissibility,
bilinear heat-flow embeddings, vector-valued square functions,
operator-valued Carleson embedding, Navier--Stokes tent spaces, commutators,
BV indicatrix results, and scattered-zero sampling.

## Direct decision

The bounded search found no published theorem or identified preprint that
directly implies

\[
 \int_0^X
 \left|P_0V(x)F(x)\right|
 \left|P_0[V'(x)+V(x)(D+\lambda_0)]F(x)\right|\,dx
\]

from the inherited negative-Sobolev critical-log action with a constant
simultaneously uniform in the number and locations of Fourier carriers.

This is a bounded non-collision conclusion, not a proof that no related result
exists anywhere in the literature and not a claim of priority.

## Primary-source matrix

| Source | What it proves | Why it does not close R0.72H |
|---|---|---|
| T. Kato and G. Ponce, [*Commutator estimates and the Euler and Navier--Stokes equations*](https://doi.org/10.1002/cpa.3160410704), 1988 | Sobolev commutator estimates for fractional derivatives and multiplication, with applications to Euler and Navier--Stokes energy estimates. | \(V'\) is a time-coefficient derivative, not the Kato--Ponce spatial commutator. Direct carrierwise use also pays higher Sobolev or \(\ell^1\) coefficient norms. |
| B. Haak and E.-M. Ouhabaz, [*Maximal regularity for non-autonomous evolution equations*](https://doi.org/10.1007/s00208-015-1199-7), 2015; [arXiv:1402.1136](https://arxiv.org/abs/1402.1136) | Maximal \(L^p\) regularity for non-autonomous coercive forms under Dini/Hölder time regularity. | It controls the full \(u'\) and \(A(t)u\), not the two specified time-dependent target rows or their product from the internal action. |
| S. Trostorff and M. Waurick, [*Maximal Regularity for Non-Autonomous Evolutionary Equations*](https://doi.org/10.1007/s00020-021-02645-5), 2021; [arXiv:2006.16696](https://arxiv.org/abs/2006.16696) | Weighted Hilbert-time maximal regularity under commutator hypotheses involving fractional time derivatives. | The needed commutator bound is an assumption in that framework and does not identify \(P_0[V'+V(D+\lambda_0)]\). |
| Y. Kharou, [*On the admissibility of observation operators for evolution families*](https://doi.org/10.1007/s00233-022-10281-7), 2022; [arXiv:2109.10069](https://arxiv.org/abs/2109.10069) | Admissibility of fixed observation operators for non-autonomous evolution families under maximal-regularity and relative Dini conditions. | Both observations in R0.72H vary with time, the second contains \(V'\), and no carrier-uniform frozen observation constant is supplied. |
| B. Haak and E.-M. Ouhabaz, [*Exact observability, square functions and spectral theory*](https://doi.org/10.1016/j.jfa.2012.01.007), 2012; [arXiv:1102.3268](https://arxiv.org/abs/1102.3268) | \(L^2\)-admissibility, exact observability, and square-function criteria for fixed observations of autonomous semigroups. | The current rows are non-autonomous and the right side is an internal negative-Sobolev action, not just the initial norm. |
| A. Carbonaro and O. Dragičević, [*Bilinear embedding for divergence-form operators with complex coefficients on irregular domains*](https://doi.org/10.1007/s00526-020-01751-3), 2020; [arXiv:1905.01374](https://arxiv.org/abs/1905.01374) | Dimension-free bilinear gradient embeddings for two autonomous divergence-form semigroups under \(p\)-ellipticity. | “Dimension-free” refers to ambient spatial dimension. The factors are spatial gradients, not the time-varying \(h\) and \(QF\) rows. |
| L. L. Morelato and A. Poggio, [*Bilinear embedding for divergence-form operators with first-order terms and negative potentials*](https://arxiv.org/abs/2605.14699), 2026 preprint | Bilinear embedding for autonomous divergence-form semigroups including first-order terms and negative potentials, with dimension-independent regimes. | It remains an autonomous spatial heat-flow result and does not include a differentiated observation row \(V'\). The item is a preprint, not a published theorem. |
| Q. Xu, [*Holomorphic functional calculus and vector-valued Littlewood--Paley--Stein theory for semigroups*](https://doi.org/10.4171/JEMS/1430), JEMS 2025; [arXiv:2105.12175](https://arxiv.org/abs/2105.12175) | Vector-valued semigroup square functions with constants governed by martingale cotype; Hilbert targets can avoid finite-dimensional growth. | It requires a fixed regular contraction/analytic semigroup. The current Fourier evolution is coupled and non-autonomous, and \(QF\) is not \(t\partial_tT_tf\). |
| F. Nazarov, G. Pisier, S. Treil, and A. Volberg, [*Sharp estimates in vector Carleson imbedding theorem and for vector paraproducts*](https://doi.org/10.1515/crll.2002.004), 2002 | Sharp finite-dimensional growth for vector/operator Carleson embeddings and paraproducts; general testing can incur logarithmic dimension loss. | It is an obstruction to an unrestricted matrix-Carleson reduction, not a negative result for the scalar rank-one heat structure used here. |
| H. Koch and D. Tataru, [*Well-posedness for the Navier--Stokes equations*](https://doi.org/10.1006/aima.2000.1937), 2001; [author manuscript](https://math.berkeley.edu/~tataru/papers/nas.pdf) | Small-data global well-posedness in \(BMO^{-1}\), using parabolic tent/Carleson norms of the heat extension. | It shows that scalar positive heat budgets can be dimension-stable in Navier--Stokes, but it does not control an internal retrospective mixed row or temporal root sampling. |
| W. Stadje, [*On functions with derivative of bounded variation: An analogue of Banach's indicatrix theorem*](https://doi.org/10.1017/S0013091500017417), 1986 | Indicatrix-type characterization for primitives of BV functions through crossing counts averaged over levels/scales. | The result does not control a squared derivative sum at the single endogenous level \(F_0=0\), and it does not identify \(QF\). |
| F. J. Narcowich, J. D. Ward, and H. Wendland, [*Sobolev bounds on functions with scattered zeros, with applications to radial basis function surface fitting*](https://doi.org/10.1090/S0025-5718-04-01708-9), 2005 | Sobolev sampling inequalities for functions vanishing on an externally specified set with controlled fill distance. | R0.72H has endogenous roots with no separation or fill-distance assumption and seeks derivatives at the roots rather than a lower Sobolev norm. |

## Three consequential distinctions

### 1. Maximal regularity is not the mixed-row estimate

Non-autonomous maximal regularity places \(F'\) and \(A(x)F\) in a time
space. To infer the R0.72H product, one would still have to prove uniform
admissibility of two particular time-dependent observations and then identify
the resulting norm with the inherited action. That missing step is the main
problem, not a corollary of the cited theorems.

### 2. Two meanings of “dimension-free”

The bilinear embedding papers remove dependence on ambient Euclidean
dimension. Xu's Hilbert-valued square-function theorem is closer to avoiding
growth in a finite \(\ell^2_M\) target. Neither applies directly to the
non-autonomous target row. Conversely, the Nazarov--Pisier--Treil--Volberg
result warns that a generic operator-valued Carleson reformulation can carry a
\(\log M\) loss.

### 3. Fixed-level temporal sampling is special

BV indicatrix theorems average over levels, while scattered-zero inequalities
assume an external geometry. Neither provides a no-separation estimate for
\(\sum_{F_0(\tau)=0}|F_0'(\tau)|^2\). The exact target-row identities and the
real/complex scalar BV or Rolle reductions in this project therefore remain
essential.

## How R0.72H avoids the missing abstraction

The proof does not assert a general non-autonomous bilinear embedding. It uses
four special facts:

1. \(P_0V_wF\) is one scalar coordinate of the already observed vector
   \(V_wF\);
2. the target eigenvalue gives
   \(|P_0V_wF|^2\le\lambda_0\|V_wF\|_{A_q^{-1}}^2\);
3. the differentiated row shares the same scalar shear heat factors as
   \(V_w\);
4. one carrier derivative pairs with the diagonal dissipation, leaving the
   reciprocal-weight moment \(m_*\).

These identities produce the carrier-free estimate directly. The
Rudin--Shapiro family then shows why a theorem using the action alone would be
too strong.

## Search boundary

Queries and citation chaining covered:

- non-autonomous maximal regularity and time-dependent forms;
- observation admissibility for evolution families;
- bilinear embedding and Bellman heat-flow estimates;
- vector-valued Littlewood--Paley square functions;
- operator-valued Carleson embedding and vector paraproducts;
- \(BMO^{-1}\) and Navier--Stokes tent spaces;
- Sobolev commutator estimates;
- BV indicatrix and temporal/scattered zero sampling.

Further returned sources were repetitions, surveys, or results weaker than
the primary items above. Search stopped at that saturation point.
