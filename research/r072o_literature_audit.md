# R0.72O literature and claim-boundary audit

**Date:** 2026-08-27
**Method:** bounded primary-source search and direct theorem-statement check.
This is not a proof of novelty or priority.

## Primary-source ledger

| Source | What it supports here | What it does not support |
|---|---|---|
| Coble and He, *A Note on Enhanced Dissipation and Taylor Dispersion of Time-dependent Shear Flows*, [arXiv:2309.15738](https://arxiv.org/html/2309.15738), published in *CMS* 22(6) (2024), [DOI](https://doi.org/10.4310/CMS.2024.v22.n6.a10) | Theorem 1.2 gives \(e^{-c\nu^{1/2}|k|^{1/2}t}\) decay for a time-dependent shear with fixed finite nondegenerate critical points, a phase-compatible slowly varying reference shear, and uniform shape constants. Constants do not depend on \(\nu\) or \(k\) once those shape parameters are fixed. | The cubic functional, Navier--Stokes cross terms, a multi-profile superposition theorem, or the physical reinsertion ledger. |
| Coti Zelati and Gallay, *Enhanced Dissipation and Taylor Dispersion in Higher-dimensional Parallel Shear Flows*, [arXiv:2108.11192](https://arxiv.org/html/2108.11192), *JLMS* 108 (2023), [DOI](https://doi.org/10.1112/jlms.12782) | In one dimension the stationary-shear decay exponent depends on critical-point degeneracy; nondegenerate/Morse critical points correspond to \(m=2\) and the \(\nu^{1/2}|k|^{1/2}\) scale. | Time-dependent multi-carrier NSE or the present trilinear row. |
| Bedrossian, Germain, and Masmoudi, *On the Stability Threshold for the 3D Couette Flow in Sobolev Regularity*, *Annals of Mathematics* 185 (2017), [journal](https://annals.math.princeton.edu/2017/185-2/p04) | A flow-specific nonlinear theory controlling nonzero-mode interactions near 3D Couette; the sufficient initial scale is \(Re^{-3/2}\) in \(H^\sigma\), \(\sigma>9/2\). | A black-box estimate for arbitrary common-band carriers or the present cubic. |
| Li, Wei, and Zhang, *Pseudospectral Bound and Transition Threshold for the 3D Kolmogorov Flow*, [arXiv:1801.05645](https://arxiv.org/abs/1801.05645), *CPAM* 73 (2020) | Another special-shear nonlinear stability precedent. | Uniform finite sums of shear profiles or a direct R0.72O theorem. |

## Exact Coble--He mapping

Their horizontal Fourier mode equation is

\[
 \partial_tf_k+ikV(t,y)f_k
 =\nu\partial_y^2f_k-\varsigma\nu|k|^2f_k,
 \qquad\varsigma\in\{0,1\}.
\]

The one-carrier generating function agrees with

\[
 k=-2,
 \qquad\varsigma=0,
 \qquad V(t,\theta)=e^{-\nu t}\sin\theta.
\]

Choosing the reference \(U=V\), the hypotheses are uniform on
\(0\le t\le\nu^{-1}\): the amplitude stays in \([e^{-1},1]\), the two
critical points are fixed and nondegenerate, the required derivatives are
uniform, and
\(\|\partial_{t\theta}U\|_\infty\le\nu\le\nu^{3/4}\).
The full interval \(t\le\nu^{-1}\) is a project-side direct verification of
the theorem hypotheses; it should not be attributed to a separate theorem
in the paper.

The theorem supplies this semigroup bound for arbitrary initial data once
\(\nu\le\nu_0\). For the complementary compact range
\(\nu_0\le\nu\le1\), the \(L^2\) contraction and a fixed enlargement of the
prefactor give the same displayed exponential form on
\(0\le t\le\nu^{-1}\). Combining the resulting all-\(\varepsilon\ge1\)
bound with bounded coordinate projections proves the project corollary

\[
 \mathcal C_\times\lesssim a^2\sqrt\varepsilon
\]

for the corrected one-carrier launch. Coble and He do not state this
cubic corollary.

## Multi-carrier boundary

Linear horizontal Fourier modes under one fixed \(x\)-independent shear can
be summed in squared \(L^2\) without a carrier-count loss. That observation
does not apply to the present nonlinear/cubic carrier expansion:

- the coefficient \(V=\sum_lV_l\) is itself the superposed profile;
- its critical points and shape constants must be checked for the whole
  sum;
- \(h=P_0VF\) and \(b=P_0V^2F\) contain signed Schur triples;
- Parseval does not delete their absolute cubic cross terms.

No checked primary source supplies the full-superposition hypothesis from
the current parameters \((R,N,B,p)\). The safe claim is the conditional
implication in the report with \(C_{\rm ED}\) and \(c_{\rm ED}\) uniform over
the compared parameter and geometry family, not an unconditional
multi-carrier theorem. If those constants vary with \(N,p,R\), the implication
is only pointwise and does not establish the plotted scaling law.

## Safe public wording

> The one-carrier enhanced-dissipation bound remains valid after the
> exact-root correction. Reintroducing the physical normalization gives
> an \(\varepsilon^{11/6}\) numerator and enlarges the paid window to
> \(\sqrt\varepsilon\lesssim R^{2/3}L_{R,\varepsilon}\). For multiple
> carriers, the same window follows from an explicit integrated estimate
> for the full superposition whose constants are uniform over the compared
> family; common-band support alone does not establish that estimate.

Unsafe wording includes:

- Coble and He proved the R0.72O cubic or physical-ledger theorem;
- one-carrier estimates tensorize over carriers;
- common-band support guarantees a uniform Morse shear;
- raw sublinearity closes arbitrary fixed-geometry coupling;
- this result advances a general 3D continuation theorem.
