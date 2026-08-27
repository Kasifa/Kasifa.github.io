# R0.72N literature and claim-boundary audit

**Date:** 2026-08-27
**Method:** bounded primary-source search followed by a line-by-line check of
the theorem statement, its parameter dependence, and the relevant proof
steps.  This search is not a proof of novelty or priority.

## Primary-source ledger

| Source | What it supports here | What it does not support |
|---|---|---|
| Coble and He, *A Note on Enhanced Dissipation of Time-Dependent Shear Flows*, *Communications in Mathematical Sciences* 22(6) (2024), [arXiv:2309.15738](https://arxiv.org/abs/2309.15738), [DOI](https://doi.org/10.4310/CMS.2024.v22.n6.a10) | Theorem 1.2 gives \(L^2\) decay \(e^{-c\nu^{1/2}|k|^{1/2}t}\) for a nondegenerate time-dependent shear on \(\mathbb T^2\); Section 3 proves the zero-horizontal-diffusion mode equation; the proof records the structural parameters on which the decay constant depends.  The arXiv v2 title additionally contains “and Taylor Dispersion.” | The paper does not state the project-specific cubic functional, its \(O(\sigma^{1/2})\) corollary, or a logarithmic first-row bound. |
| Bedrossian and Coti Zelati, *Enhanced dissipation, hypoellipticity, and anomalous small noise inviscid limits in shear flows*, *Archive for Rational Mechanics and Analysis* 224 (2017), [DOI](https://doi.org/10.1007/s00205-017-1099-y) | stationary-shear hypocoercivity background and spectral inequalities used by later work | the decaying-amplitude chain or the present cubic projection |
| Coti Zelati and Gallay, *Enhanced dissipation and Taylor dispersion in higher-dimensional parallel shear flows*, *Journal of the London Mathematical Society* 108 (2023), [DOI](https://doi.org/10.1112/jlms.12782) | the \(\nu^{-1/2}\) enhanced-dissipation scale associated with Morse/nondegenerate critical points | a theorem for this exact time-dependent shear or its rowwise absolute cubic |
| Benthaus and Nobili, *Enhanced dissipation via time-modulated velocity fields*, *Evolution Equations and Control Theory* 15 (2026), [arXiv:2501.16905](https://arxiv.org/abs/2501.16905), [DOI](https://doi.org/10.3934/eect.2025051) | directly studies separable time modulation and includes \(e^{-\nu t}\) on the diffusive interval as an admissible example | its stated viscous estimate has an additional diffusivity-dependent prefactor and is not a sharper route to the present cubic |
| Albritton and Beekie, *Sharp uniform-in-diffusivity mixing rates for passive scalars in parallel shear flows* (2025), [arXiv:2511.18536](https://arxiv.org/abs/2511.18536) | optimal \(H^{-1}\) mixing for fixed nondegenerate shears suggests the missing \(t^{-1/2}\) ingredient behind a logarithmic row estimate | the theorem is for a fixed shear and does not directly cover this time-dependent amplitude |
| Liss and Luan, *Uniform-in-diffusivity mixing by shear flows: stochastic and dynamical perspectives* (2026), [arXiv:2603.09238](https://arxiv.org/abs/2603.09238) | provides another sharp fixed-shear uniform-in-diffusivity mixing route | no time-dependent-amplitude or first-row total-variation theorem |
| Coti Zelati, Delgadino, and Elgindi, *On the Relation between Enhanced Dissipation Timescales and Mixing Rates*, *Communications on Pure and Applied Mathematics* 73 (2020), [DOI](https://doi.org/10.1002/cpa.21831) | establishes an abstract direction from quantitative negative-Sobolev mixing to enhanced dissipation | does not compare the project-specific critical-log action with enstrophy |

## Exact theorem mapping

The R0.72N generating function obeys

\[
 \partial_tF=\nu\partial_\theta^2F
 +2i e^{-\nu t}\sin\theta\,F,
 \qquad \nu=\sigma^{-1}.
\]

Coble--He use

\[
 \partial_t f_k+ikV(t,\theta)f_k
 =\nu\partial_\theta^2f_k-\varsigma\nu|k|^2f_k,
 \qquad \varsigma\in\{0,1\}.
\]

The equations agree with

\[
 k=-2,\qquad \varsigma=0,\qquad
 V(t,\theta)=e^{-\nu t}\sin\theta.
\]

Their proof treats the \(\varsigma=0\) equation explicitly.  The sign of
\(k\) is immaterial by complex conjugation; the theorem is stated with
\(|k|\).

Choose the reference shear \(U=V\).  For
\(0\le t\le\nu^{-1}\):

- the critical points \(\pi/2\) and \(3\pi/2\) are fixed;
- \(e^{-\nu t}\in[e^{-1},1]\), so nondegeneracy and all shape constants
  are uniform;
- the relevant \(W^{2,\infty}\) norms are uniformly bounded;
- \(\|\partial_{t\theta}U\|_\infty\le\nu\le\nu^{3/4}\) for
  \(0<\nu\le1\).

The proof chooses its hypocoercive coefficients from the uniform
comparability constant, spectral constant, and
\(\|\partial_{\theta\theta}U\|_\infty\).  These are uniform for this
family.  The resulting estimate therefore has constants independent of
\(\nu\) on the full interval required here:

\[
 \|F(t)\|_2\le C e^{-c\nu^{1/2}t}\|F(0)\|_2,
 \qquad 0\le t\le\nu^{-1}.
\]

## Project-specific corollary

The elementary coordinate estimate

\[
 |f_1(f_0-f_2)|\le\sqrt2\sum_n|f_n|^2
\]

and Parseval turn the squared semigroup bound into

\[
\begin{aligned}
 \mathcal C_{\rm diss}
 &\le Ca^2\int_0^{\nu^{-1}}
   e^{-2c\nu^{1/2}t}\,dt \\
 &\le Ca^2\nu^{-1/2}
 =Ca^2\sigma^{1/2}.
\end{aligned}
\]

This implication is new to the project report, not quoted from the paper.
It proves the weaker direct gate
\(\mathcal C_{\rm diss}=o(\sigma a^2)\), while leaving the sharper
\(O(a^2\log\sigma)\) rate open.

## Correction to the preceding literature boundary

R0.72M correctly stated that an enhanced-dissipation semigroup estimate
does not by itself prove the **logarithmic** bounded-variation law.
Its broader wording that semigroup decay could not control the absolute
cubic variation was too strong.  For this specific product, projection by
the full \(L^2\) norm loses sharp oscillatory information but still gives
the rigorous \(O(\sigma^{1/2})\) bound above.

## Safe public wording

> Coble--He's nondegenerate time-dependent-shear theorem applies to the
> rescaled one-carrier generating function.  Combining its \(L^2\) decay
> with an elementary coordinate projection gives the project-specific
> corollary
> \(\mathcal C_{\rm diss}\lesssim a^2\sigma^{1/2}\).
> The action-poor scalar route nevertheless fails, and logarithmic,
> multi-carrier, multiscale, and general three-dimensional conclusions
> remain open.

Unsafe wording includes:

- Coble and He proved the R0.72N cubic theorem;
- the logarithmic finite-data trend has been certified;
- every time-dependent shear or every launch enjoys the same bound;
- one-carrier sublinearity closes the full strong-coupling ledger;
- the Clay Millennium problem has been solved or reduced to this theorem.
