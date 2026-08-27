# R0.72J bounded primary-source audit

**Search cutoff:** 2026-08-27

**Audit target:** literature collision with the gcd-reduced Cayley-graph
classification, the signed-Schur interpretation of the target rows, and the
common-band joint-exposure estimate for the true cubic contribution.

## 0. Direct decision

The graph-theoretic part has a standard source: Proposition 9.1 of
Árnadóttir et al. characterizes bipartite Cayley graphs by a homomorphism to
\(\mathbb Z_2\). Specializing that proposition to \(g_0\mathbb Z\) gives the
odd-reduced-carrier criterion in R0.72J.

Green--Ruzsa supply the standard definition and structural setting for
sum-free sets in abelian groups. Their theorem concerns extremal sizes and
counts in finite abelian groups, not the weighted signed convolution in the
Navier--Stokes row.

The checked bilinear, trilinear, and semigroup Carleson sources establish
strong dimension-free or abstract heat-flow embeddings for their stated
operators and function spaces. None of them directly gives the
solution-dependent minimum in R0.72J (4.5), the exact target-root correction,
or the physical conversion exponent. The R0.72J analytic estimates are
therefore proved directly for the finite triangular model.

This is a bounded comparison, not a proof of priority or an exhaustive claim
that no equivalent result exists.

## 1. Claim--source ledger

| ID | Primary source | What the source supports | What it does not imply here |
|---|---|---|---|
| J-L1 | A. S. Árnadóttir, A. Gordeev, S. Lato, T. Randrianarisoa, and J. Vermant, [*Cayley Incidence Graphs*](https://arxiv.org/abs/2411.19428), Proposition 9.1. | A Cayley graph \(\operatorname{Cay}(G,S)\) is bipartite iff there is a homomorphism \(G\to\mathbb Z_2\) sending every generator in \(S\) to \(1\). For \(G=g_0\mathbb Z\), this gives exactly “every \(r_l/g_0\) is odd.” | It does not identify the one-step and two-step operator rows, distinguish a triangle from a longer odd cycle, or estimate any Navier--Stokes quantity. |
| J-L2 | B. Green and I. Z. Ruzsa, [*Sum-free sets in abelian groups*](https://arxiv.org/abs/math/0307142). | Defines sum-free sets by absence of \(x+y=z\) and determines extremal size, with counting results, for finite abelian groups. It supplies the standard additive-combinatorial language behind the signed Schur-triple test. | The report uses a signed symmetric carrier set in \(\mathbb Z\), coefficient phases, heat weights, and a cubic operator row. The finite-group extremal theorem neither bounds that row nor supplies the physical normalization. |
| J-L3 | A. Carbonaro and O. Dragičević, [*Bilinear embedding for divergence-form operators with complex coefficients on irregular domains*](https://arxiv.org/abs/1905.01374). | Proves a bilinear inequality for divergence-form operators with complex coefficients and mixed boundary conditions, with maximal-regularity consequences. | Its observation is not the endogenous pair \(h=P_0VF\), \(b=P_0V^2F\), and it does not yield the exact joint multiplier exposure \(E\int\rho^2\|V\|\) or the root correction used here. |
| J-L4 | A. Carbonaro, O. Dragičević, V. Kovač, and K. Škreb, [*Trilinear embedding for divergence-form operators with complex coefficients*](https://arxiv.org/abs/2101.11694). | Proves a dimension-free trilinear heat-flow embedding for three divergence-form operators under \(p\)-ellipticity assumptions, with paraproduct, square-function, and Kato--Ponce consequences. | Dimension-free trilinearity alone does not identify the carrier heat window, the coefficient \(B\), the signed additive relations, or the physical factor \(\Theta\). It does not prove R0.72J (5.21) or sample target roots. |
| J-L5 | T. Mei, [*An \(H^1\)--BMO duality theory for semigroups of operators*](https://arxiv.org/abs/1204.5082). | Establishes semigroup \(H^1\)--BMO duality and a Carleson embedding under abstract positivity assumptions, without requiring a metric kernel. | The R0.72J weight is a critical-log action along a solution-dependent multiplication row. The source does not convert that action into the exact cubic minimum, eliminate the common-band hypothesis, or control zeros of a complex target coordinate. |

## 2. Three distinctions used in the report

### 2.1 Bipartite is not the same as triangle-free

The homomorphism criterion detects every odd closed walk. The cubic launch
overlap detects only length three. The set \(\{1,4\}\) is the smallest
useful warning in this report: its Cayley graph has a length-five odd walk,
while \(\Sigma\cap(\Sigma+\Sigma)=\varnothing\).

### 2.2 Sum-free language does not estimate weighted convolution

The relation \(s+t=u\) decides whether a coefficient can occur. Its size is
then determined by multiplicity, phases, heat factors, the evolving launch,
and the physical amplitude balance. An extremal theorem for sum-free subsets
does not supply those analytic estimates.

### 2.3 Abstract heat-flow embeddings do not close endogenous roots

The bilinear/trilinear and Carleson sources control integrals in specified
function spaces. R0.72J has a row generated by the same shear that drives the
solution and a root set generated by the observed coordinate. Even a
dimension-free embedding would not by itself justify real Rolle sampling for
a complex target trajectory.

## 3. Allowed literature statement

The following wording is supported:

> The gcd-reduced bipartite criterion is a specialization of the standard
> Cayley-graph homomorphism criterion. The checked additive-combinatorial and
> heat-semigroup embedding sources provide language and comparison, but do
> not directly prove the signed target-row identities, common-band cubic
> estimate, exact root correction, or physical decay exponent used here.

The stronger statements “the whole R0.72J result is new” and “no related
theorem exists” are not supported.
