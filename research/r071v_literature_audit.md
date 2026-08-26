# R0.71V bounded primary-source audit: level integration, 2D3C reduction, and Leray--rotational identities

**Search date:** 2026-08-26

**Question:** which established results justify the one-dimensional
level formulas, exact 2D3C invariant reduction, and Leray energy/rotational
identities used around R0.71V; and does any checked source promote a
level-integrated crossing estimate to the prescribed boundary level \(z=0\)?

## 1. Bounded answer

The checked literature supports the surrounding interfaces, not the complete
R0.71V theorem.

Federer's area formula, Banach's indicatrix theorem, deterministic
finite-variation occupation densities, and truncated-variation identities all
integrate multiplicity or crossing information over the level variable. They
do not bound the value of the resulting density at a preassigned level.
This remains true when the crossing density has a distinguished representative
defined at every level: changing or concentrating a density at one level is
invisible to its \(L^1(dz)\) norm.

The 2D3C invariant manifold is standard: three-dimensional NSE restricted to
fields depending on two coordinates splits into two-dimensional NSE for the
in-plane velocity and an advection--diffusion equation for the out-of-plane
component. The narrower triangular ansatz used in R0.71V follows by direct
substitution. The checked 2D3C sources do not state the prescribed-root or
high-frequency boundary-layer constructions proved in the report.

Leray and modern monographs supply the energy equality/inequality and the
energy-class spaces. The rotational form and classical enstrophy identity are
also standard. They do not give Leray-level control of \(\omega_t\), \(L_t\),
or the second time jet. The bounded review found no theorem that supplies the
R0.71V reverse average, excursion-to-atom noncollapse factor, or
first-row-only obstruction. This is a scoped source review, not a novelty,
originality, priority, or nonexistence statement.

## 2. Claim--source--gap matrix

| Claim or interface | Primary or authoritative source and exact location | What the source licenses | Remaining R0.71V gap |
|---|---|---|---|
| Weighted one-dimensional area formula | Herbert Federer, *Geometric Measure Theory*, [Springer DOI](https://doi.org/10.1007/978-3-642-62010-2), §3.2.3, p.243 | For Lipschitz \(f:\mathbb R^m\to\mathbb R^n\), the weighted area formula integrates the sum over preimages against Hausdorff measure. With \(m=n=1\), it gives \(\int g(t)|r'(t)|dt=\int\sum_{r(t)=z}g(t)dz\). | The result is integrated in \(z\). It gives no evaluation functional at \(z=0\). The report's \(r\in W^{1,1}(I)\) version uses the one-dimensional fact \(W^{1,1}=AC\), followed by the standard absolutely-continuous/finite-variation extension; it is not §3.2.3 applied verbatim beyond its Lipschitz hypotheses. |
| Banach indicatrix | Stefan Banach, *Sur les lignes rectifiables et les surfaces dont l'aire est finie* (1925), [DOI](https://doi.org/10.4064/fm-7-1-225-236), [EuDML scan](https://eudml.org/doc/214571), p.228, Théorème 2 | For continuous real \(f\), bounded variation is equivalent to integrability of the indicatrix, and \(\operatorname{TV}(f)=\int_{-\infty}^{\infty}N(z,f)dz\). | It controls the level integral of multiplicity, not one exceptional level or a slope-weighted zero trace. |
| Finite-variation occupation density | Jean Bertoin and Marc Yor, *Local times for functions with finite variation* (2014), [DOI](https://doi.org/10.1112/blms/bdu014), [arXiv](https://arxiv.org/abs/1307.1288), Theorem 1, journal p.555; proof on pp.559--560 | The signed and absolute occupation measures of a càdlàg finite-variation path are absolutely continuous, with crossing-number densities \(\ell^z(t)\) and \(\lambda^z(t)\). The theorem explicitly treats these densities as \(L^1(dz)\) objects defined for almost every \(z\). | Absolute continuity of the occupation measure does not provide an endpoint trace at a prescribed \(z=0\). |
| Positive-height band crossings and truncated variation | Rafał M. Łochowski, *On a generalisation of the Banach indicatrix theorem* (2017), [DOI](https://doi.org/10.4064/cm6583-3-2017), [arXiv](https://arxiv.org/abs/1503.01746), Theorem 1, journal pp.304--305 | For regulated \(f\) and \(c>0\), \(\mathrm{UTV}^c=\int u_c^z dz\), \(\mathrm{DTV}^c=\int d_c^z dz\), and \(\mathrm{TV}^c=\int n_c^z dz\). | A positive band pays excursions that persist through height \(c\); excursions whose heights collapse with the data can disappear as \(c\downarrow0\). |
| Recent deterministic local-time formulation | Hove--Mhlanga--Łochowski--Zondi, *Local times of deterministic paths with finite variation*, [DOI](https://doi.org/10.4064/cm9372-11-2025), [arXiv](https://arxiv.org/abs/2405.13174), Theorem 2.8 and Remark 2.9, manuscript pp.5--6 | Defines crossing counts for càdlàg finite-variation paths and proves weighted identities after integration over \(z\); its pointwise change-of-variable formula (16), manuscript p.8, is stated at simple levels. | Even an everywhere-defined chosen representative is not pointwise bounded by its level integral. The source does not give a uniform trace or reverse average at a distinguished zero level. |
| Exact 2D3C invariant reduction | Biferale--Buzzicotti--Linkmann, *From two-dimensional to three-dimensional turbulence through two-dimensional three-component flows* (2017), [DOI](https://doi.org/10.1063/1.4990082), [arXiv](https://arxiv.org/abs/1706.02371), §II, equations (1)--(2), article/manuscript p.2 | For \(u=(u_x(x,y),u_y(x,y),u_z(x,y))\), 3D NSE splits exactly into 2D NSE for \(u_{2D}\) and passive advection--diffusion for \(u_z\). | It supplies the invariant class only. The triangular shear, finite interpolation, implicit curve, and prescribed root times in R0.71V are direct internal arguments, not statements attributed to this paper. |
| Global smoothness in the selected triangular subclass | Roger Temam, *Navier--Stokes Equations and Nonlinear Functional Analysis*, 2nd ed., [DOI](https://doi.org/10.1137/1.9781611970050), Theorem 3.2 and Remark 3.2, pp.21--22, together with the preceding 2D3C reduction | Standard two-dimensional strong-solution theory is global; in the still narrower R0.71V ansatz the in-plane field solves a heat equation and the passive component a linear advection--diffusion equation. | Neither source gives the prescribed Fourier zero map or its \(q\to\infty\) asymptotics. |
| Leray energy inequality and energy-class regularity | Jean Leray, *Sur le mouvement d'un liquide visqueux emplissant l'espace* (1934), [DOI](https://doi.org/10.1007/BF02547354), [original scan](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/5537-11511_2006_Article_BF02547354.pdf), p.235, equation (5.9), and p.241; Temam, equation (3.2), p.17, Theorem 3.1, p.21, and Remark 3.2, p.22 | Smooth solutions satisfy the energy identity; a three-dimensional weak solution can be selected to satisfy the energy inequality and \(u\in L^\infty_tL^2_x\cap L^2_tH^1_x\). | These statements control \(u\) and one spatial derivative in the energy sense, not \(\omega_t\), \(L_t\), \(C_{tt}\), or pointwise jets at adaptively chosen weak zero times. |
| Finiteness of the projected rotational row | Temam, §2.3, pp.11--13, especially the Sobolev interpolation and trilinear estimates (2.25)--(2.32), combined with the preceding energy inequality | The standard three-dimensional estimate gives \(\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}\lesssim\|u\|_4^2\lesssim\|u\|_2^{1/2}\|\omega\|_2^{3/2}\). Hence \(\|L\|_{\dot H^{-1}}^2/Y\lesssim\|u\|_2Y^{1/2}\), which is integrable on finite intervals by the energy inequality. | This pays the time-integrated first row only. It is not a fixed-zero trace estimate. |
| Rotational form, energy orthogonality, and enstrophy identity | Doering--Gibbon, *Applied Analysis of the Navier--Stokes Equations*, [Cambridge DOI](https://doi.org/10.1017/CBO9780511608803), p.129, equations (6.5.1)--(6.5.3), and p.131, equation (6.5.13); Gibbon--Holm, [Cambridge DOI](https://doi.org/10.1017/CBO9781139235792.010), [arXiv](https://arxiv.org/abs/1012.3597), arXiv p.3, equation (1.3) | The rotational identity is \(u_t+\omega\times u=\nu\Delta u-\nabla(p+|u|^2/2)\) in the unforced case. The classical enstrophy equation contains the three-dimensional vortex-stretching term. | The enstrophy equality is a strong-solution identity, not a Leray a priori estimate for time derivatives. It also fixes the sign convention described below. |
| Chebyshev-system interpolation | Karlin--Studden, *Tchebycheff Systems: With Applications in Analysis and Statistics* (1966), [catalogue record](https://books.google.com/books?id=P7Y-AAAAIAAJ), Chapters I and XI, especially Chapter XI, Theorem 1.1 for the Wronskian criterion for ECT systems | Supplies the standard determinant, zero-count, and interpolation machinery for a verified T-system. | It does not verify the particular response family automatically and contains no NSE recurrence theorem. R0.71V must, and does, identify the exponential response system and derive its scaling separately. |
| Absolute continuity of compact-shell coefficients | Temam, Theorem 3.1, p.21, supplies the weak energy spaces; the remaining step is direct testing of the weak equation against each smooth Fourier basis vector | A compact torus annulus contains finitely many modes. Viscous and quadratic terms paired with a fixed smooth mode are in \(L^1_t\), so each coefficient has a \(W^{1,1}\) representative. | This is an elementary deduction in R0.71V, not a theorem quoted verbatim from Temam. It does not define the normalized derivative atom at every weak zero time. |

## 3. The fixed distinguished level is an additional theorem, not a corollary

Write \(\Phi(z)\) for any of the crossing densities produced by the area or
occupation formulas. An \(L^1(dz)\) estimate cannot control \(\Phi(0)\).
Even continuity of each individual density is insufficient uniformly:

\[
 \Phi_n(z)=n(1-nz)_+,\qquad
 \int_0^\infty\Phi_n(z)\,dz=\frac12,\qquad
 \Phi_n(0)=n.
\]

Thus an endpoint trace must carry additional quantitative information. A
sufficient hypothesis would be one of the following equivalent types:

1. a uniform one-sided trace or reverse-average inequality,
   \[
    \Phi(0+)\le \frac{C}{h_0}\int_0^{h_0}\Phi(z)\,dz;
   \]
2. a uniform \(W^{1,p}\), BV, or modulus-of-continuity bound in the level
   variable, with a trace constant independent of the trajectory;
3. rootwise persistence: every zero branch reaches a uniform positive level
   width and its crossing weight remains comparable along that branch.

For one fixed smooth trajectory, a simple scalar root gives a local branch
and a path-dependent trace. The available height depends on the slope,
curvature, neighboring critical values, and excursion height. That local
fact does not provide a constant uniform over the Leray class. Moreover,
for \(r=\|C\|\ge0\), zero is a one-sided boundary level and \(r\) has a cusp
at a first-order vector zero; the ordinary scalar regular-value theorem is
not the missing estimate.

## 4. Projected rotational nonlinearity: sign convention

With \(\omega=\operatorname{curl}u\), the standard vector identity gives

\[
 (u\cdot\nabla)u=\omega\times u+
 \nabla\frac{|u|^2}{2}.
\]

Many fluid-mechanics sources call
\(D_{\mathrm{Lamb}}=\omega\times u\) the Lamb vector. After applying the
Leray projector to unforced NSE,

\[
 u_t=\nu\Delta u+\mathbb P(u\times\omega).
\]

Accordingly, R0.71V's convention

\[
 L=\mathbb P(u\times\omega)=-\mathbb P D_{\mathrm{Lamb}}
\]

is algebraically correct but has the opposite sign from the commonly named
Lamb vector. “Projected rotational nonlinearity” is therefore the
unambiguous term for \(L\) in this report.

## 5. Attribution boundary for the report

- Sections 2--4 are real-variable deductions from weak Fourier testing,
  absolute continuity, Cauchy--Schwarz, and the report's definitions. They
  are not attributed as external theorems.
- Section 5 uses the established area/occupation interface above. The
  prescribed zero-level reverse average is explicitly left as an extra
  hypothesis.
- The sine test in Section 6 is an internal scalar example, not an NSE
  trajectory and not a literature claim.
- The particular triangular 2D3C response, Chebyshev interpolation,
  implicit-function construction, tangent ledger, high-frequency limits,
  and noncommuting limits in Sections 7--11 are the report's proofs and
  calculations. The cited 2D3C and T-system sources provide only the
  ambient framework.
- The numerical figure is corroboration of finite formulas; it is not
  evidence for global regularity, uniform nonlinear remainders, or a
  literature-priority claim.

## 6. Search and wording boundary

The focused review covered one-dimensional area/coarea formulas, Banach
indicatrix, deterministic finite-variation local time, truncated variation,
2D3C invariant NSE, Leray energy theory, rotational/Lamb identities,
enstrophy, and Chebyshev-system interpolation. Targeted reverse searches
for a fixed-level trace returned the same level-integrated or almost-everywhere
interfaces.

No checked source states the complete R0.71V excursion packing theorem,
the fixed-target repeated-root sequence, or the first-row-only obstruction.
That sentence records only the stopping boundary of this review. It must
not be converted into a claim of novelty, originality, priority, or
nonexistence in the literature.

The release-source scan is clear of all four disabled narration terms in the
project wording policy.
