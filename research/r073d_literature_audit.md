# R0.73D literature audit: inviscid unstable spectrum under vanishing viscosity

**Date:** 2026-08-30  
**Question:** Is static persistence of the R0.73C periodic Rayleigh eigenvalue
already known in a general form, and what remains specific to the present
double-harmonic operator?

## 1. Direct decision

The existence and algebraic-multiplicity part of the R0.73D target has a
clear prior general theorem.  Shvydkoy and Friedlander prove that unstable
Navier--Stokes eigenvalues converge to isolated Euler eigenvalues lying
beyond the inviscid essential spectral threshold, and that the corresponding
fixed-cluster spectral subspaces converge.  Their theorem includes periodic
incompressible flows.

Accordingly, this release must not describe vanishing-viscosity spectral
persistence as a new general theorem.  The project-specific contribution is
instead:

1. R0.73C supplies a certified positive inviscid eigenvalue for the explicit
   double-harmonic profile \(W_0\);
2. R0.73D gives a short self-contained proof in the exact kinetic space
   \(X_{1/4}\), including all domain and Fourier-commutator checks;
3. the special single-row structure gives an explicit operator-norm
   convergence proof for the fixed-cluster Riesz projections.
   Shvydkoy--Friedlander Theorem 2.1(iii) states convergence of the
   corresponding Riesz projections without explicitly naming the topology,
   while its preceding resolvent convergence is explicitly strong.  The
   present argument is therefore recorded as a self-contained fixed-row norm
   proof, not as a first or a strict strengthening of their general theorem;
4. none of these static results supplies the nonautonomous complementary
   dichotomy or nonlinear estimate required later.

## 2. Primary-source comparison

| Primary source | Exact result used or excluded | Relation to the present row | Boundary |
|---|---|---|---|
| R. Shvydkoy and S. Friedlander, *The unstable spectrum of the Navier--Stokes operator in the limit of vanishing viscosity*, Ann. Inst. H. Poincare C 25 (2008), 713--724. [DOI](https://doi.org/10.1016/j.anihpc.2007.05.004), [journal record and full text](https://www.numdam.org/articles/10.1016/j.anihpc.2007.05.004/), [arXiv](https://arxiv.org/abs/math/0509538) | Theorem 2.1(ii)--(iii) proves total algebraic multiplicity and convergence of the fixed-cluster Riesz spectral subspace for inviscid eigenvalues beyond the essential spectral threshold. The end of Section 4 obtains uniformly bounded resolvents on a surrounding circle and explicitly strong resolvent convergence there. | This is the decisive general precedent for periodic Euler/Navier--Stokes spectral persistence. It confirms that the existence part of R0.73D is not a new abstract phenomenon. | Its general proof is formulated for the full advective PDE and a geometric-optics essential-spectrum threshold. It does not explicitly label the topology of the projection limit or display the present compact-Fredholm norm estimate. The paper's \(\mu_m\) is an essential spectral growth threshold, not \(\mu=\gamma^2\) in \(L_\mu\). |
| Y. Charles Li, *Invariant Manifolds and Their Zero-Viscosity Limits for Navier--Stokes Equations*, Dynamics of PDE 2 (2005), 159--186. [DOI](https://doi.org/10.4310/DPDE.2005.v2.n2.a4), [arXiv](https://arxiv.org/abs/math/0505390) | For a rectangular periodic Kolmogorov-flow example, the paper gives a unique positive viscous eigenvalue in a stated aspect-ratio and viscosity regime and studies its zero-viscosity limit. | It is an explicit periodic-flow precedent showing that Rayleigh-to-viscous spectral persistence can be proved without wall boundary layers. | The proof uses the single-harmonic recurrence of that model. It cannot be substituted for the double-harmonic \(W_0\), and it does not provide the present compact-Fredholm proof. |
| Y. Charles Li and Z. Lin, *A Resolution of the Sommerfeld Paradox*, SIAM J. Math. Anal. 43 (2011), 1923--1954. [DOI](https://doi.org/10.1137/100794912), [arXiv](https://arxiv.org/abs/0904.4676) | Theorem 4.1 proves that an unstable Rayleigh eigenmode of their oscillatory channel shear has a nearby unstable Orr--Sommerfeld eigenmode for sufficiently small viscosity, with phase speed convergence. The proof uses Wasow asymptotics and Rouche's theorem. | It is a direct inviscid-to-viscous unstable-eigenvalue precedent. | The cross-stream domain is a channel and the viscous problem has no-slip conditions \(\phi=\phi'=0\). The boundary-layer matching and fourth-order determinant are absent from the present periodic row, so the theorem is not a plug-in proof here. |
| E. Grenier, Y. Guo and T. T. Nguyen, *Spectral instability of characteristic boundary layer flows*, Duke Math. J. 165 (2016), 3085--3146. [DOI](https://doi.org/10.1215/00127094-3645437), [arXiv](https://arxiv.org/abs/1406.3862) | Constructs exact viscous growing modes for boundary-layer profiles at high Reynolds number using Rayleigh/Airy Green functions and critical-layer analysis. | Shows the depth of the singular Orr--Sommerfeld problem when a wall is present. | It treats a different Tollmien--Schlichting mechanism and no-slip half-space geometry. It neither supplies nor is needed for the periodic compact-Fredholm argument. |
| R. Beekie, S. Chen and H. Jia, *Uniform vorticity depletion and inviscid damping for periodic shear flows in the high Reynolds number regime* (2024). [arXiv](https://arxiv.org/abs/2403.13104) | Proves uniform high-Reynolds resolvent, damping, and enhanced-dissipation estimates for periodic shears under an assumption excluding inviscid discrete and generalized embedded eigenvalues. | It is the closest recent periodic resolvent comparison on the spectrally stable side. | Its no-discrete-eigenvalue hypothesis conflicts with R0.73C. Its nondegenerate-critical-point assumptions also do not match the cubic degeneracy of \(W_0\). It cannot supply the complementary dichotomy needed here. |
| M. Colombo, M. Dolce, R. Montalto and P. Ventura, *Long-wave instability of periodic shear flows for the 2D Navier--Stokes equations* (2025). [arXiv](https://arxiv.org/abs/2509.18070) | Constructs periodic long-wave viscous instability using Kato isomorphisms and normal forms in a regime where the horizontal wave number scales with viscosity. | Relevant as a modern Riesz/Kato technique for periodic shear flows. | The present row has fixed \(\gamma=1/2\), not a wave number tending to zero with viscosity. The theorem addresses a different scaling and does not replace static persistence of the certified R0.73C mode. |

## 3. Applicability to the exact R0.73C eigenvalue

The certified phase speed is \(c=i\eta_*\), \(\eta_*>0\).  Since \(W_0\)
is real,

\[
 |W_0(x)-c|\ge\eta_*>0.
\]

There is therefore no real critical layer for this eigenmode.  The periodic
cross-stream coordinate also creates no wall boundary layer.  These two facts
explain why the present vorticity-space factorization is substantially
simpler than the channel Orr--Sommerfeld constructions.

After fixing the nonzero streamwise Fourier row \(\gamma=1/2\), the
Biot--Savart map and the kinetic-space unitary map reduce the operator to

\[
 M+K-\varepsilon L_{1/4},
\]

where \(M\) is skew-adjoint multiplication and \(K\) is compact.  The exact
proof is given in `research/r073d_viscous_persistence_proof.md`; it does not
invoke the general geometric-optics machinery of Shvydkoy--Friedlander.

## 4. Claim boundary after the literature audit

The following wording is supported:

```text
certifiedProfileSpecificInviscidInput=R0.73C
generalVanishingViscosityPrecedent=KNOWN
staticProfileSpecificPersistence=CLOSED_BY_SELF_CONTAINED_PROOF
fixedClusterRieszProjectionNormConvergence=VERIFIED_FOR_FIXED_ROW
noveltyOfNormConvergence=NOT_CLAIMED
relationToShvydkoyFriedlander=SELF_CONTAINED_SPECIALIZATION_WITH_EXPLICIT_NORM_PROOF
movingProfileContinuation=OPEN
uniformComplementaryDichotomy=OPEN
logFastTimeTransfer=OPEN
nonlinearNavierStokes=OPEN
Clay=OPEN
```

The release should not claim a first general proof of inviscid-to-viscous
spectral persistence.  If the operator-norm projection argument survives the
independent audit, it may be stated only as a strengthening for this special
compact single-row representation, not as a new general Navier--Stokes
theorem.
