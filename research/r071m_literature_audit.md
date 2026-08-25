# R0.71M bounded primary-source audit

Search date: 2026-08-26.

Question searched:

> Does an established theorem derive a fixed-physical-cell, normalized
> projected-Lamb/projective-tangent budget, including the local denominator
> and cutoff--curl, from the standard three-dimensional Leray energy
> inequality alone?

Two bounded search rounds were run over primary papers and author-hosted
copies. The search converged to three neighboring structures:

1. exact filtered/increment algebra;
2. additional critical Besov, increment, or Carleson hypotheses;
3. energy-class ultraviolet or scale gaps.

No exact collision with all parts of the question was found. This is a
bounded search result, not a theorem of nonexistence and not an originality
or priority claim.

## 1. Claim/source matrix

| Verified statement | Primary source | Scope and boundary for R0.71M |
|---|---|---|
| The quadratic filter stress can be represented by velocity increments; a weak Euler solution in \(L_t^3B_{3,\infty}^{\alpha}\cap C_tL^2\), \(\alpha>1/3\), conserves energy in the original commutator argument. | Constantin, E, and Titi, “Onsager's conjecture on the energy conservation for solutions of Euler's equation” (1994), [author PDF](https://web.math.princeton.edu/~weinan/papers/misc1.pdf), [DOI](https://doi.org/10.1007/BF02099744) | Global Euler energy balance, not a fixed-cell vorticity quotient. The Besov assumption is extra input. |
| The local inertial defect has an exact cubic velocity-increment formula. A critical \(1/3\)-type increment decay condition makes that defect vanish. | Duchon and Robert, “Inertial energy dissipation for weak solutions of incompressible Euler and Navier–Stokes equations” (2000), [DOI](https://doi.org/10.1088/0951-7715/13/1/312), [Numdam source](https://archive.numdam.org/item/SEDP_1999-2000____A13_0/) | The defect is a distributional local-energy object. It is not the normalized fixed-cell projective tangent. |
| Littlewood--Paley energy flux is controlled at the critical \(B^{1/3}_{3,c(\mathbb N)}\) endpoint. The paper also constructs a divergence-free field in \(B^{1/3}_{3,\infty}\) with nonvanishing flux and explicitly does not claim that field is an Euler solution. | Cheskidov, Constantin, Friedlander, and Shvydkoy, “Energy conservation and Onsager's conjecture for the Euler equations,” [arXiv:0704.0759](https://arxiv.org/abs/0704.0759), [author PDF](https://www.math.uic.edu/~acheskid/papers/onsager.pdf) | Exact critical endpoint and a useful claim-boundary precedent. It contains no physical cutoff denominator or projective tangent. Here \(c(\mathbb N)\) denotes the vanishing Littlewood--Paley tail condition \(2^{q/3}\|\Delta_qu\|_3\to0\). |
| For weak 3D NSE solutions, \(L_t^3V^{5/6}\) is a sufficient extra condition for energy equality. | Cheskidov, Friedlander, and Shvydkoy, “On the energy equality for weak solutions of the 3D Navier–Stokes equations,” [arXiv:0704.2089](https://arxiv.org/abs/0704.2089) | The theorem distinguishes the Leray--Hopf class from an additional regularity hypothesis. It is not a Leray-only implication. |
| Eyink writes the filtered Lamb-force commutator \(f^*=\overline{u\times\omega}-\bar u\times\bar\omega\), while his increment formula in Eq. (35) is for the stress-divergence force \(f=-\operatorname{div}\tau\). | Eyink, “The Cascade of Circulations in Fluid Turbulence,” [arXiv:physics/0606159](https://arxiv.org/abs/physics/0606159), [DOI](https://doi.org/10.1103/PhysRevE.74.066302) | These are neighboring translation-invariant structures, not the exact R0.71M commutator \(T_j(u\times\omega)-u\times T_j\omega\): the second factor/filtering differs. There is no fixed cutoff or local Hilbert denominator. |
| Resolved energy flux of Leray solutions is bounded by Constantin--E--Titi estimates under uniform Besov hypotheses; dissipation-rate assumptions exclude overly smooth uniform families. | Drivas and Eyink, “An Onsager Singularity Theorem for Leray Solutions of Incompressible Navier–Stokes,” [arXiv:1710.05205](https://arxiv.org/abs/1710.05205), [DOI](https://doi.org/10.1088/1361-6544/ab2f42) | Conditional scale obstruction for Leray families. It does not imply a fixed-viscosity cellwise tangent estimate. |
| Small \(BMO^{-1}\) initial data give a unique global solution in a scale-invariant space whose norm contains a velocity square-Carleson term. | Koch and Tataru, “Well-posedness for the Navier–Stokes equations,” [author PDF](https://math.berkeley.edu/~tataru/papers/nas.pdf), [DOI](https://doi.org/10.1006/aima.2000.1937) | A critical small-data theory on \(\mathbb R^n\). The Carleson norm is an assumption/solution norm, not a consequence of \(L^2\) energy. |
| A derivative-compatible filtered-stress estimate bounds the localized paired work \(\iint\chi_r\Omega_\ell\cdot\operatorname{curl}\operatorname{div}R_\ell\) by filtered palinstrophy, a scale-invariant quartic increment defect, and cutoff-shell residuals. | Yu, “Filtered Vortex Stretching and Subgrid Defects for the Three-Dimensional Navier–Stokes Equations,” [arXiv:2606.27560v1](https://arxiv.org/abs/2606.27560v1), Theorem 9.3 | June 2026 preprint, not treated here as peer-reviewed. The derivative is transferred in the paired work; the theorem does not control \(\operatorname{curl}\operatorname{div}R_\ell\) as a field norm. |
| Yu's Theorem 8.7 gives a reassigned-annulus \(\ell^p\)-\(\ell^q\) closure. The complete unweighted closure in Theorem 10.3 additionally assumes full far-field, \(\widetilde\Sigma_S\), and residual summability. | Yu, [arXiv:2606.27560v1](https://arxiv.org/html/2606.27560v1), Theorems 8.7 and 10.3 and Remark 8.9 | Direct evidence that scale invariance alone is not unweighted Carleson summability in that ledger. It is not an NSE counterexample. |
| Energy equality for suitable weak solutions follows under additional \(L_t^qL_x^p\) or singular-set hypotheses. | Leslie and Shvydkoy, “Conditions Implying Energy Equality for Weak Solutions of the Navier--Stokes Equations,” [arXiv:1606.02363](https://arxiv.org/abs/1606.02363) | Further evidence that critical/local energy conclusions use hypotheses beyond the bare energy class. |

## 2. Exact comparison with Yu's defect

Yu defines, for a nonnegative unit-mass filter,

\[
 d\nu_\ell=\varphi_\ell(z)\,dz,\qquad
 d\mu_\ell=
 \frac{\ell|\nabla\varphi_\ell(z)|}{\|\nabla\varphi\|_1}\,dz,
\]

\[
 \mathfrak M_{\ell,p}=M_{\varphi,p}+M_{\nabla,p},
\]

and

\[
 \widetilde{\mathcal S}_{r,\ell}^{(p)}
 =\frac r{\ell^2}\iint\chi_r\mathfrak M_{\ell,p}^4\,dx\,dt.
\]

The inner label \(p=3\) does not make the outer density cubic; the defect is
quartic. At fixed \(\ell=\sigma r\) it is NSE-scale invariant.

Lemma 9.2 of that preprint gives

\[
 |\operatorname{div}R_\ell|^2
 \lesssim\ell^{-2}\mathfrak M_{\ell,p}^4.
\]

Theorem 9.3 pairs
\(\Omega_\ell\) with
\(\operatorname{curl}\operatorname{div}R_\ell\), integrates one curl by
parts, and absorbs the resulting derivative of \(\Omega_\ell\) into filtered
palinstrophy.

R0.71M has a different consumer. Its exact pairing contains

\[
 G_j-\frac{B_Q}{d_Q}\operatorname{curl}C_Q
\]

against

\[
 G_j+\nu(\Delta+\kappa_j^2)W_j.
\]

The increment commutator is only one component of the fused \(G_j\), and the
split commutator need not be annular. Therefore Yu's theorem cannot be
substituted verbatim for the R0.71M four-row budget.

This comparison is about the objects and derivative placement. It is not a
critique of Yu's theorem.

## 3. Three critical exponents that must not be conflated

### 3.1 Onsager \(1/3\)

The \(1/3\) threshold arises from a cubic spatial energy-flux commutator.
CCFS sharpen it to the \(B^{1/3}_{3,c(\mathbb N)}\) endpoint, where the
weighted Littlewood--Paley coefficients vanish at high shells.

### 3.2 Parabolic \(L_t^3B_{3,\infty}^{2/3}\)

For a three-dimensional velocity norm with \(p_x=q_t=3\), NSE scaling gives

\[
 s_c=-1+\frac3p+\frac2q=\frac23.
\]

This is one possible critical velocity consumer for the tangent problem; it
is not asserted to be necessary or sufficient.

### 3.3 Yu's quartic derivative-compatible defect

The outer fourth power makes the global dimensional analogue an
\(L^4\)-type critical increment with spatial index \(1/4\), after the
matched parabolic normalization. It is neither of the two quantities above.

R0.71M keeps all three labels separate.

## 4. Leray interpolation boundary

From

\[
 u\in L_t^\infty L_x^2\cap L_t^2\dot H_x^1
\]

one obtains

\[
 u\in L_t^{2/\theta}\dot H_x^\theta.
\]

After spatial embedding into an \(L^p\)-based scale, the paid index is

\[
 s_E=\theta-\frac32+\frac3p,
\]

whereas NSE criticality at the same \(p,q=2/\theta\) requires

\[
 s_c=-1+\frac3p+\theta.
\]

Thus \(s_c-s_E=1/2\) for every interpolation parameter. This is an exact
function-space gap. It does not exclude an equation-specific signed
cancellation.

## 5. Search verdict

The bounded search supports the following wording:

1. translation-invariant filtered energy, Lamb, vorticity, and enstrophy
   identities are established tools;
2. small-scale decay or uniform critical control enters through additional
   increment, Besov, Carleson, or sequence-summability assumptions;
3. the standard energy class alone gives coarser quadratic controls;
4. physical cutoffs add transport/collar rows, while the R0.71M projective
   quotient also adds \(d_Q^{-1}\) and a time-dependent Hilbert direction;
5. no checked theorem pays all rows of the exact R0.71M pairing from Leray
   energy alone.

The search does not support:

- a claim that no such theorem can exist;
- an originality or priority assertion for R0.71M;
- an NSE solution counterexample;
- a conclusion about global regularity or singularity.

The second search round returned the same three structural classes as the
first, and later hits were reviews or LES modelling papers rather than a
theorem matching all fixed-cell/projective/Leray-only requirements. That was
the bounded stopping rule.
