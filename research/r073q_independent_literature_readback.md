# R0.73Q independent primary-literature readback

**Audit date:** 2026-08-31

**Audited files:** `r073q_primary_literature_audit.md`,
`r073q_gap_matrix.md`, and `r073q_claim_source_ledger.md`

**Mode:** bounded, source-level readback of domains, indices, time exponents,
solution classes, and theorem-versus-abstract labels; no novelty search and no
inference from an unavailable theorem

**Final verdict:** `PASS_AFTER_TWO_TARGETED_CORRECTION_ROUNDS`

## 1. Exact items independently checked

| Source | Readback result | Boundary retained in R0.73Q |
| --- | --- | --- |
| Kato 1984 | `PASS_WITH_PRECISION` | Domain \(\mathbb R^m\); in three dimensions the critical datum is \(L^3\).  The uniqueness statement remains in Theorem 1's weighted smoothing class and is not promoted to unconditional bare \(C_tL^3_x\) uniqueness. |
| Koch--Tataru 2001 | `PASS` | Domain \(\mathbb R^n\); Theorem 2 is the unique **small** global \(X\) solution and Theorem 3 the unique **small** local \(X_R\) solution.  The Carleson component is not replaced by a bare Kato supremum. |
| Iftimie 1999 | `PASS_AFTER_ATTRIBUTION_FIX` | Theorem 2.1 uses the vertical average \(v_0=Mu_0\); Theorem 2.2 permits a separately prescribed two-dimensional component.  Strict enlargement beyond isotropic \(H^{1/2}\) for \(0<\delta<1/2\) is labeled theorem plus elementary Fourier-weight comparison, not a verbatim theorem sentence. |
| Mucha 2001 | `ABSTRACT_ONLY_PASS` | The three-torus, nontrivial reference solution, and abstract-level \(L^2\)-small perturbation statement are retained.  The unavailable \(r\), trace space, threshold dependence, and uniqueness class are not reconstructed. |
| Mucha 2008 | `PASS_AFTER_INDEX_FIX` | The exact range \(1<p,q<\infty\), \(3/p+2/q<3\), the trace space \(B^{2-2/q}_{p,q}\cap L^2\), and higher-trace-dependent \(L^2\) smallness are explicit. |
| Gallagher--Iftimie--Planchon 2003 | `PASS_AFTER_ENDPOINT_FIX` | Domain \(\mathbb R^3\), \(1\le p,q<\infty\), and \((p,q)=(6,4)\) giving \(\dot B^{-1/2}_{6,4}\) are correct.  The reference control uses an auxiliary \(2<r_0<2/(1-3/p)\), hence \(2<r_0<4\) at \(p=6\); the difference estimate separately covers the theorem's displayed \(1\le r\le\infty\) range. |
| Auscher--Dubois--Tchamitchian 2004 | `ABSTRACT_ONLY_PASS_AFTER_DOWNGRADE` | Author name is Sandrine Dubois.  Only the publisher abstract's decay, analytic dependence, and openness of the corresponding Cauchy-data set in \(BMO^{-1}\) are used.  No radius, full perturbation quantifier, uniqueness class, or missing title typography is reconstructed. |
| Coiculescu--Palasek 2025/2026 | `PASS_AFTER_CLASS_FIX` | Theorem 1.2 gives two distinct solutions in the displayed smooth, \(L^\infty_tBMO^{-1}\), continuous negative-Sobolev class; Remark 1.3 gives finite \(X_{KT}\) norm and says the construction is not perturbative around zero.  `Nonperturbative` is not converted into a quantitative large-norm lower bound.  Remark 1.5 keeps the initial datum outside \(L^2\). |

## 2. Corrections required before the final pass

The first readback rejected an incorrect ADT author name, theorem-level use
of publisher-abstract evidence, omission of Mucha's \(1<p,q<\infty\) range,
failure to separate GIP's auxiliary \(r_0\) from the difference exponent,
and attribution of Iftimie's elementary strictness comparison as a paper
theorem.  It also rejected the token `large BMO^{-1}` because the verified
source supplies `not perturbative around zero`, not a numerical lower bound
on the datum norm.

The second readback found residual copies of those labels in the report,
dictionary, and gap matrix.  They were removed, the public evidence table
was split into full-theorem and publisher-abstract rows, and the
Coiculescu--Palasek conclusion was restricted to the theorem's finite-
\(X_{KT}\) solution class.

The third, read-only pass returned `PASS` with no remaining source-level
upgrade.

## 3. Authorized literature ledger

```text
KatoCriticalL3=VERIFIED_THEOREM_WITH_WEIGHTED_CLASS
KochTataruSmallBMOInverse=VERIFIED_THEOREM
IftimiePeriodicAnisotropic=VERIFIED_THEOREM_PLUS_ELEMENTARY_COMPARISON
Mucha2001PeriodicPerturbation=ABSTRACT_ONLY
Mucha2008HighTraceDependentL2=VERIFIED_THEOREM
GIPWholeSpaceBesovOrbitOpenness=VERIFIED_THEOREM_DIRECT_COLLISION
ADTBMOInverseCauchyDataOpenness=ABSTRACT_ONLY_COLLISION
nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL
periodicR073QNoveltyOrPriority=NOT_CLAIMED
uniformL2OnlyStrongRadius=OPEN
clayConclusion=OPEN
```

The readback audits fidelity to the located primary material.  It is not a
priority search and does not authorize a novelty claim.
