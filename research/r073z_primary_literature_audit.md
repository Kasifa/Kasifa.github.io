# R0.73Z primary-literature collision audit

**Audit date:** 2026-09-01

**Status:** BOUNDED COMPLETE / STRONG COMPONENT COLLISIONS

**Claim class:** PRIMARY-SOURCE COLLISION AUDIT / NO PRIORITY INFERENCE

**Search boundary:** two bounded waves over original papers, publisher
records, author-hosted manuscripts, and official arXiv records.  The search
is not bibliometrically exhaustive.  Failure to locate an identical formula
or theorem is not evidence of novelty or priority.

## 1. Executive conclusion

Every principal component used in R0.73Z has strong precedent:

1. positive heat or Gaussian covariances and their forced scale equations;
2. exact separation of signed production from nonnegative viscous covariance;
3. cubic local energy-defect quantities;
4. heat-semigroup Besov and carré-du-champ seminorms;
5. subgrid kinetic energy used as an unresolved velocity scale in LES;
6. zero SGS production for simple shear classes; and
7. the two-dimensional viscously decaying cellular witness itself.

The bounded search did not locate either of the following exact packages:

\[
 {1\over R}\int_I\int_0^{\theta R^2}\int_{B_R}
 \left(P_s|\nabla u|^2-|\nabla P_su|^2\right)^{3/2},
\tag{1.1}
\]

or

\[
 {\nu\over R^2}\int_I\int_0^{\theta R^2}\int_{B_R}
 \left(P_s|\nabla u|^2-|\nabla P_su|^2\right)
 \left\{\frac12(P_s|u|^2-|P_su|^2)\right\}^{1/2}.
\tag{1.2}
\]

Nor did it locate the exact three-way diagnostic statement

\[
 \Pi_s=0,\qquad \mathscr S_s=0,\qquad
 Q_s=P_s(pu)-P_sp\,P_su\not\equiv0
\tag{1.3}
\]

on the crossed cellular solution used in R0.73Z-B.

These are bounded non-collision findings only.  Any eventual contribution
must be phrased as a theorem about the exact combined functional or diagnostic
separation, never as discovery of its components or of the classical witness.

## 2. Claim-to-source ledger

| R0.73Z claim family | Primary source | Established content | Collision boundary |
|---|---|---|---|
| Positive covariance under a positive filter | B. Vreman, B. Geurts, and H. Kuerten, “Realizability conditions for the turbulent stress tensor in large-eddy simulation,” JFM 278 (1994), [DOI](https://doi.org/10.1017/S0022112094003745) | A nonnegative normalized filter yields a positive-semidefinite subfilter stress; Gaussian and top-hat filters satisfy realizability | Direct collision for positivity of \(k_s\) and for the variance mechanism; no mixed cubic functional |
| Gaussian width as heat time and exact stress scale evolution | P. L. Johnson, “Energy Transfer from Large to Small Scales in Turbulence by Multiscale Nonlinear Strain and Vorticity Interactions,” PRL 124 (2020), [DOI](https://doi.org/10.1103/PhysRevLett.124.104501), [arXiv](https://arxiv.org/abs/1912.00293) | Equations (7)--(10) identify Gaussian width squared as a diffusion coordinate and give the exact forced scale equation and gradient-product representation for subfilter stress | Direct formula-level collision for both covariance factors; no \(D_s^{3/2}\) or \(D_s\sqrt{k_s}\) cylinder integral |
| Multilevel central moments and filtered energy ledgers | M. Germano, “Turbulence: the filtering approach,” JFM 238 (1992), [DOI](https://doi.org/10.1017/S0022112092001733), [manuscript](https://www.ams.jhu.edu/~eyink/Turbulence/classics/Germano92.pdf) | Generalized central moments, exact multilevel identities, and large-/small-scale energy equations | Signed production and positive covariance are already distinct classical rows |
| Smooth coarse-grained cascade balance | G. L. Eyink and H. Aluie, “Localness of energy cascade in hydrodynamic turbulence. I. Smooth coarse-graining,” Physics of Fluids 21 (2009), [DOI](https://doi.org/10.1063/1.3266883), [arXiv](https://arxiv.org/abs/0909.2386) | Exact smooth-filter energy balance separates signed transfer from nonnegative viscous covariance, storage, and transport | Direct conceptual collision; no R0.73Z mixed observable |
| Cubic local defect at weak regularity | J. Duchon and R. Robert, “Inertial energy dissipation for weak solutions of incompressible Euler and Navier--Stokes equations,” Nonlinearity 13 (2000), [DOI](https://doi.org/10.1088/0951-7715/13/1/312) | Cubic velocity-increment defect in the local energy balance | Strong cubic near-neighbor; signed limiting increment defect, not either finite positive heat-covariance integral |
| Markov semigroup variance and carré du champ | M. Ledoux, “The geometry of Markov diffusion generators,” Annales de la Faculté des Sciences de Toulouse 9 (2000), [record](https://numdam.org/item/AFST_2000_6_9_2_305_0/) | Standard diffusion-generator framework for semigroup variance, gradient estimates, and Sobolev inequalities | Direct collision for the proof technology; no identified mixed \(D_s\sqrt{k_s}\) square function |
| Heat-semigroup Besov classes | P. Alonso-Ruiz et al., “Besov class via heat semigroup on Dirichlet spaces I: Sobolev type inequalities,” [arXiv:1811.04267](https://arxiv.org/abs/1811.04267) | Heat-kernel increment seminorms and Sobolev-type estimates on general Dirichlet spaces | Strong function-space neighbor; a single \(p\)-moment is not algebraically equal to a product of two quadratic variances |
| Simple shear has zero exact SGS dissipation | A. W. Vreman, “An eddy-viscosity subgrid-scale model for turbulent shear flow: Algebraic theory and applications,” Physics of Fluids 16 (2004), [DOI](https://doi.org/10.1063/1.1785131), [author PDF](https://www.vremanresearch.nl/Vreman-PF2004-subgridmodel.pdf) | Classification of zero theoretical SGS-dissipation derivative types includes simple laminar shear | Direct collision for R0.73Y and the rectangular kernel components; no crossed pressure-covariance theorem |
| SGS energy as an unresolved velocity scale | A. Yoshizawa and K. Horiuti, “A Statistically-Derived Subgrid-Scale Kinetic Energy Model for the Large-Eddy Simulation of Turbulent Flows,” JPSJ 54 (1985), [DOI](https://doi.org/10.1143/JPSJ.54.2834) | One-equation SGS kinetic-energy model; eddy viscosity is formed from filter width and the square root of SGS energy | Strong modeling-form collision for the \(\sqrt{k_s}\) motivation; it is a closure, not the exact product (1.2) |
| Dissipation conditioned on SGS kinetic energy | C. Meneveau and J. O'Neil, “Scaling laws of the dissipation rate of turbulent subgrid-scale kinetic energy,” PRE 49 (1994), [DOI](https://doi.org/10.1103/PhysRevE.49.2866) | Studies moments of SGS dissipation and its conditional relation to local SGS kinetic energy; reports mismatch with simple model prediction | Very close physical pairing, but statistical and modeled rather than the deterministic heat-covariance product |
| Classical cellular witness | G. I. Taylor and A. E. Green, “Mechanism of the Production of Small Eddies from Large Ones,” Proc. R. Soc. A 158 (1937), [DOI](https://doi.org/10.1098/rspa.1937.0036) | Classical Taylor--Green vortex lineage | Equal-amplitude, phase/reflection variants of R0.73Z-B are classical; the exact velocity-pressure solution is not a new result |

## 3. Algebraic non-equivalences that must remain explicit

### 3.1 The mixed observable is not a cubic increment moment

For a heat-kernel random displacement, write schematically

\[
 A_s=\mathbb E|\delta\nabla u|^2,
 \qquad
 2k_s=\mathbb E|\delta u|^2.
\tag{3.1}
\]

Then

\[
 A_s\sqrt{k_s}
 =2^{-1/2}
 \bigl(\mathbb E|\delta\nabla u|^2\bigr)
 \bigl(\mathbb E|\delta u|^2\bigr)^{1/2}
\tag{3.2}
\]

is generally not equal to
\(\mathbb E(|\delta\nabla u|^2|\delta u|)\), nor to
\(\mathbb E|\delta u|^3\).  Hölder inequalities may compare selected
moments in one direction, but there is no direct identity.

### 3.2 \(D_s\) is not \(\partial_sk_s\)

The exact equations are

\[
 (\partial_s-\Delta)k_s=|\nabla P_su|^2,
 \qquad
 (\partial_s-\Delta)D_s=2|\nabla^2P_su|^2.
\tag{3.3}
\]

Thus replacing \(D_s\) by a scale derivative of \(k_s\) would drop diffusion
and use the wrong forcing.

### 3.3 The positive mixed observable is not the LES energy flux

The standard transfer

\[
 \Pi_s=-\tau_s:\nabla P_su
\tag{3.4}
\]

is signed.  The R0.73Z observable \(D_s\sqrt{k_s}\) is nonnegative.  It may
be motivated by unresolved energy and dissipation scales, but it must not be
called an exact energy flux.

## 4. Attribution boundary for the crossed family

The safe mathematical description is:

> The witness is a two-mode, same-Laplacian-eigenvalue steady Euler flow with
> viscous exponential decay.  Its equal-amplitude symmetric members are
> phase-shifted or reflected representatives of the classical two-dimensional
> Taylor--Green family, and its individual components are orthogonal
> sinusoidal shear modes.

The solution, its pressure, and its viscous decay are not new.  The bounded
search did not locate (1.3) as a single Gaussian-filter theorem on this
witness.  If used as a contribution, it may only be described as a strict
separating example for the precisely defined diagnostics \(\Pi_s\),
\(\mathscr S_s\), and
\(Q_s=P_s(pu)-P_sp\,P_su\).

## 5. Stop rule and remaining searches

Two waves covered exact covariance formulas, semigroup function spaces, LES
kinetic-energy/dissipation pairings, zero-production shears, and the crossed
cellular witness.  Repeated exact-phrase variants did not change the collision
matrix.  The audit therefore stops under diminishing returns.

Before any formal novelty statement, a later paper-stage audit must still
inspect forward and backward citation chains, paid full texts not accessed
here, theses, books, and non-English sources.  R0.73Z makes no novelty or
priority claim.

**NOT CLAY.**

