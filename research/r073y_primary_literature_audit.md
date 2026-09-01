# R0.73Y primary-literature collision audit

**Audit date:** 2026-09-01

**Status:** `BOUNDED_COMPLETE / DIRECT_COLLISION_FOUND`

**Claim class:** `PRIMARY_SOURCE_COLLISION_AUDIT / NO_PRIORITY_INFERENCE`

**Search boundary:** original papers, official publisher records, author-hosted
manuscripts, and official arXiv records.  The search is bounded, not
bibliometrically exhaustive.  Failure to find an identical theorem is not a
novelty or priority proof.

## 1. Executive conclusion

The exact shear trajectory and the identity \(\Pi_s=0\) are classical or
direct specializations of established results.  In particular, Vreman (2004)
classified simple laminar shears with one nonzero off-diagonal velocity
derivative among the exact zero-subgrid-dissipation flow types.  Germano
(1992) and Eyink--Aluie (2009) already separate signed subgrid production from
the nonnegative viscous gradient covariance in exact small-scale energy
budgets.  Jeong--Yoneda (2022) explicitly use on \(\mathbb T^3\) the shear
component \(u^L(t,x_2)e_1\), whose equation is the one-dimensional heat
equation.

Therefore R0.73Y must not claim discovery of an exact shear, zero SGS
production, positive covariance, or the general principle that a signed flux
need not be coercive.  Its narrower local increment is the following packaged
statement tied to the frozen R0.73X definitions:

1. an entire orthogonal periodic shear class consists of smooth exact NSE
   trajectories;
2. both \(\Pi_s\) and the centered heat production \(\mathscr S_s\) vanish
   pointwise for every positive heat scale;
3. the heat gradient covariance is pointwise strictly positive for every
   nonzero member;
4. the precise positive size
   \(\mathcal E^{3/2}+\mathcal A_{\rm ext}\) scales like \(|A|^3\) and is
   unbounded while every zero-preserving production-only input is zero; and
5. hence the particular production-only amplitude-independent modulus needed
   after R0.73X is false.

The bounded search found no source containing this full package verbatim.
That is a bounded negative finding, not a claim of novelty.  The result should
be described as a **literature-calibrated exact obstruction** or
**sanity-check counterexample**, not as a high-level regularity theorem.

## 2. Collision and gap matrix

| R0.73Y row | Primary source | Established content | R0.73Y boundary |
|---|---|---|---|
| Periodic 3D shear solves a 1D heat equation | I.-J. Jeong and T. Yoneda, “Quasi-streamwise vortices and enhanced dissipation for the incompressible 3D Navier--Stokes equations,” *Proc. Amer. Math. Soc.* **150** (2022), [DOI](https://doi.org/10.1090/proc/15754), [arXiv](https://arxiv.org/abs/2012.14621) | On \(\mathbb T^3\), the component \(u^L(t,x_2)e_1\) satisfies \(\partial_tu^L=\nu\partial_2^2u^L\) exactly | Direct collision for the exact-family mechanism; no coarse-grained no-go |
| Classical plane-parallel reduction | A. L. Mazzucato and M. E. Taylor, “Vanishing viscosity plane parallel channel flow and related singular perturbation problems,” *Anal. PDE* **1** (2008), 35--93, [DOI](https://doi.org/10.2140/apde.2008.1.35) | Gives an exact pressureless plane-parallel NS reduction to heat plus linear advection--diffusion | Establishes classical lineage; different boundary geometry and broader two-component class |
| Simple shear has zero exact SGS dissipation | A. W. Vreman, “An eddy-viscosity subgrid-scale model for turbulent shear flow: Algebraic theory and applications,” *Phys. Fluids* **16** (2004), 3670--3681, [DOI](https://doi.org/10.1063/1.1785131), [author PDF](https://www.vremanresearch.nl/Vreman-PF2004-subgridmodel.pdf) | Defines \(D_\tau=-\tau_{ij}\partial_j\bar u_i\) and proves zero exact SGS dissipation for 13 laminar derivative classes, including a simple shear with one nonzero off-diagonal derivative | Strongest direct collision.  Its local filter hypotheses are not stated as the noncompact heat semigroup; the same sparse tensor contraction proves the heat case directly |
| Signed production and positive covariance are distinct ledger rows | M. Germano, “Turbulence: the filtering approach,” *J. Fluid Mech.* **238** (1992), 325--336, [DOI](https://doi.org/10.1017/S0022112092001733) | Generalized central moments and exact large-/small-scale energy equations separate production from viscous gradient covariance | Direct mechanism collision; no R0.73X exterior functional or modulus theorem |
| Exact smooth-coarse-grained energy budget | G. L. Eyink and H. Aluie, “Localness of energy cascade in hydrodynamic turbulence. I. Smooth coarse-graining,” *Phys. Fluids* **21** (2009), 115107, [DOI](https://doi.org/10.1063/1.3266883), [arXiv](https://arxiv.org/abs/0909.2386) | Exact small-scale energy equation contains signed \(\Pi\) and nonnegative viscous covariance as separate terms; storage and transport remain | Explains why \(\Pi=0\) does not force covariance zero |
| Positive-filter realizability | B. Vreman, B. Geurts, and H. Kuerten, “Realizability conditions for the turbulent stress tensor in large-eddy simulation,” *J. Fluid Mech.* **278** (1994), 351--362, [DOI](https://doi.org/10.1017/S0022112094003745) | A nonnegative filter yields a positive-semidefinite SGS covariance | Positivity is established background; the explicit strictly positive heat formula is a specialization |
| Gaussian scale is heat time and stress has an exact scale integral | P. L. Johnson, “Energy Transfer from Large to Small Scales in Turbulence by Multiscale Nonlinear Strain and Vorticity Interactions,” *Phys. Rev. Lett.* **124** (2020), 104501, [DOI](https://doi.org/10.1103/PhysRevLett.124.104501), [arXiv](https://arxiv.org/abs/1912.00293) | The Gaussian width squared is a diffusion-time coordinate; the exact subfilter stress solves a forced diffusion equation | Formula-level collision for the heat stress; no shear no-go |
| Cubic increment energy defect | J. Duchon and R. Robert, “Inertial energy dissipation for weak solutions of incompressible Euler and Navier--Stokes equations,” *Nonlinearity* **13** (2000), 249--255, [DOI](https://doi.org/10.1088/0951-7715/13/1/312) | Introduces the cubic velocity-increment defect in the local energy balance | Closest classical background for \(\mathscr S_s\); no explicit orthogonal-shear parity theorem located |
| Positive CKN size is not a signed-work quantity | L. Caffarelli, R. Kohn, and L. Nirenberg, “Partial regularity of suitable weak solutions of the Navier--Stokes equations,” *Comm. Pure Appl. Math.* **35** (1982), 771--831, [DOI](https://doi.org/10.1002/cpa.3160350604) | Suitable local energy inequality and positive scale-critical partial-regularity mechanism | The smooth R0.73Y family does not challenge CKN or epsilon regularity |
| Current coarse-work observability boundary | R. Yu, “Coarse-Grained Resolution and Pressure--Flux Work Depletion for Navier--Stokes CKN Badness,” arXiv:2606.25322v1 (2026), [record](https://arxiv.org/abs/2606.25322), [DOI](https://doi.org/10.48550/arXiv.2606.25322) | Defines signed coarse pressure--flux work and leaves the badness-to-work observability implication conditional; coherent cancellation is an explicit obstruction | Closest conceptual collision; no exact shear witness; preprint not represented as peer reviewed |
| Positive anti-kernel repair direction | R. Yu, “Invisible Defect Cascades for Navier--Stokes Regularity,” arXiv:2606.12756v1 (2026), [record](https://arxiv.org/abs/2606.12756), [DOI](https://doi.org/10.48550/arXiv.2606.12756) | Uses positive resolved-energy/covariance channels to detect pressure--flux invisible directions | Highly adjacent repair principle; no R0.73Y heat-shear package; preprint not represented as peer reviewed |

## 3. Exact attribution rule for public text

The public note may say:

> Vreman already proved that simple shear can have zero exact SGS production,
> while Germano and Eyink--Aluie separate signed production from nonnegative
> gradient covariance in exact coarse-grained energy budgets.  R0.73Y turns
> that established mechanism into an explicit all-heat-scale NSE witness for
> the particular production-only modulus left open by R0.73X.

It must not say “first,” “new exact shear,” “new zero-flux principle,” or
“regularity criterion.”

## 4. Research value and next high-value target

As a standalone result, R0.73Y-A is too elementary and too close to known LES
structure to support a high-level paper.  It is nevertheless valuable as a
fail-fast theorem: it removes a false bridge and specifies which positive rows
cannot be discarded.

The next potentially publishable target is a quotient coercivity theorem:
factor out the Vreman/orthogonal-shear production kernel, add the minimal
positive covariance or endpoint/cutoff debt, and prove a uniform lower bound
on a precisely declared NS-realizable class.  A second high-value alternative
is a genuinely three-dimensional, pressure-active production-invisible family.

**NOT CLAY.**
