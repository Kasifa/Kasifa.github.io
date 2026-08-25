# R0.71K primary-source audit — matched spatial localization, collars, and normalized positive work

Search date: 2026-08-26.

## 1. Object being compared

The comparison is not against local energy or enstrophy localization in the
abstract.  R0.71K studies the specific cellwise quantity

\[
 q_{j,Q}
 =\frac{((B^L_{j,Q})^+)^2}{d_{j,Q}},
 \qquad
 B^L_{j,Q}
 =\left\langle A_j\mathbb P(u\times\omega),
 \nabla\times(\chi_QA_j\omega)\right\rangle,
\]

\[
 d_{j,Q}=\|\nabla\times(\chi_QA_j\omega)\|_2^2,
 \qquad
 A_{\mathrm{loc},+}=\|\omega\|_2^{-2}\sum_{j,Q}q_{j,Q},
\]

with matched radii \(r_j\asymp K_j^{-1}\), bounded spatial overlap, and the
complete cutoff--curl, viscous-collar, tangent, denominator-face, and refresh
ledger.  A source collides with R0.71K only if it controls this nonlinear,
normalized positive quotient, not merely because it uses a cutoff or a cover.

## 2. Primary-source matrix

| Primary source | Object actually covered | Difference from R0.71K | Boundary imposed on the claim |
|---|---|---|---|
| Caffarelli--Kohn--Nirenberg, *Partial regularity of suitable weak solutions of the Navier--Stokes equations* (1982), [DOI](https://doi.org/10.1002/cpa.3160350604) | Local kinetic-energy inequality for suitable weak solutions, with the classical cutoff, pressure, and transport rows. | No frequency parent, projected-Lamb/cutoff--curl pairing, positive-part square, local curl denominator, or global-enstrophy normalization. | Local cutoff budgets and partial-regularity localization are classical; R0.71K does not claim them. |
| Duchon--Robert, *Inertial energy dissipation for weak solutions of incompressible Euler and Navier--Stokes equations* (2000), [DOI](https://doi.org/10.1088/0951-7715/13/1/312) | A local energy-defect distribution defined through velocity increments. | Scalar energy defect in a coarse-graining limit, rather than the cellwise vorticity/Lamb Rayleigh quotient above. | A weak all-scale limit may retain a defect; no defect-free infinite frame--cell passage is assumed here. |
| Constantin--E--Titi, *Onsager's conjecture on the energy conservation for solutions of Euler's equation* (1994), [DOI](https://doi.org/10.1007/BF02099744) | Spatial mollification and nonlinear commutator estimates at the Onsager threshold. | Euler energy commutator; no viscosity, matched physical partition, quotient denominator, or time-face ledger. | Filter commutators are established tools, not an R0.71K novelty claim. |
| Cheskidov--Constantin--Friedlander--Shvydkoy, *Energy conservation and Onsager's conjecture for the Euler equations* (2008), [arXiv:0704.0759](https://arxiv.org/abs/0704.0759), [DOI](https://doi.org/10.1088/0951-7715/21/6/005) | Littlewood--Paley flux representations, shell interactions, and critical Besov closure. | Signed global spectral energy flux, not a physical-space collar ledger or \(((B_Q^L)^+)^2/d_Q\). | Ordinary LP telescoping cannot be presented as new, and its conditional Besov estimates are not an unconditional Leray payment. |
| Eyink--Aluie, *Localness of energy cascade in hydrodynamic turbulence, I. Smooth coarse-graining* (2009), [arXiv:0909.2386](https://arxiv.org/abs/0909.2386), [DOI](https://doi.org/10.1063/1.3266883) | Smooth graded filters, Germano multiscale decomposition, and space/scale locality of kinetic-energy transfer under inertial-range scaling assumptions. | Filter footprints and SGS flux, not a compact matched partition with local curl denominators, faces, or refresh atoms. | Space--scale filtered budgets and signed flux telescopes are classical; the present object is different. |
| Dascaliuc--Grujić, *Energy cascades and flux locality in physical scales of the 3D Navier--Stokes equations* (2011), [arXiv:1101.2193](https://arxiv.org/abs/1101.2193), [DOI](https://doi.org/10.1007/s00220-011-1219-8) | Refined ball/shell cutoffs, bounded-multiplicity covers, and ensemble-averaged local energy/pressure flux for suitable weak solutions under a Taylor-scale condition. | A linear signed flux is ensemble averaged; there is no LP parent and no positive-part-square/local-denominator quotient. | This is the closest physical-space energy precedent.  Refined covers and bounded overlap are not claimed as new. |
| Dascaliuc--Grujić, *Coherent vortex structures and 3D enstrophy cascade* (2013), [arXiv:1107.0058](https://arxiv.org/abs/1107.0058), [DOI](https://doi.org/10.1007/s00220-012-1595-8) | Local enstrophy balance and an ensemble cascade under vorticity-direction coherence, Kraichnan-scale, and modulation hypotheses. | Conditional transport-enstrophy flux and palinstrophy comparison, not the filtered projected-Lamb quotient. | Conditional local palinstrophy coercivity cannot be imported as a Leray-level consequence. |
| Leitmeyer, *Enstrophy Cascade in Physical Scales for the Three-Dimensional Navier--Stokes Equations* (2016), [arXiv:1502.01258](https://arxiv.org/abs/1502.01258), [DOI](https://doi.org/10.1137/140997154) | Refined test functions, bounded-overlap ensembles, and an exact finer partition of a physical-scale cutoff; cascade conclusions require coherence/Morrey/Kraichnan hypotheses. | Geometrically close, but still a linear flux ensemble without matched frequency parents, \(q_{j,Q}\), or \(Y^{-1}\) normalization. | Matched/refined partitions and finite multiplicity are known components.  The theorem is not isomorphic to R0.71K. |
| Tao, *Localisation and compactness properties of the Navier--Stokes global regularity problem* (2013), [arXiv:1108.1165](https://arxiv.org/abs/1108.1165), [DOI](https://doi.org/10.2140/apde.2013.6.25) | Local energy/enstrophy estimates with time-dependent cutoffs whose motion suppresses transport leakage, together with collar and nonlocal leakage control. | A moving localized region rather than a fixed finite-overlap matched partition; no frequency parent or normalized local quotient. | Transported cutoffs and explicit collar accounting have direct precedent. |
| Runlong Yu, *Filtered Vortex Stretching and Subgrid Defects for the Three-Dimensional Navier--Stokes Equations* (2026 preprint), [arXiv:2606.27560v1](https://arxiv.org/abs/2606.27560v1), [arXiv DOI](https://doi.org/10.48550/arXiv.2606.27560) | Positive filtered strain--vorticity stretching, near-/far-field splitting, filtered palinstrophy absorption, commutator defects, and localization residuals. | Additive filtered-enstrophy residuals, not the projected-Lamb/cutoff--curl quotient; no matched \(Q\)-sum, local denominator faces, or refresh atoms. | The closest current analytic comparison, but not an isomorphic theorem. |

## 3. Three routes that must remain distinct

### 3.1 Refined-cover ensemble flux

Dascaliuc--Grujić and Leitmeyer average a signed physical-space energy or
enstrophy flux over a refined cover.  Under additional scale, modulation, or
geometric assumptions, the ensemble average is comparable to dissipation or
modified palinstrophy.  Positivity of such an ensemble average is not the
same operation as taking the positive part in every cell, squaring, dividing
by a local curl denominator, and then summing.

### 3.2 Yu's filtered localization residual

Yu's Section 7 treats \(L_k\) as nonnegative localization budgets and states
that they have no coercive contribution.  Proposition 6.4 removes the main
cutoff residual only for a cutoff satisfying a backward adjoint
drift--diffusion equation.  The unweighted closure in Theorem 10.3 also assumes
summability of the far-field, increment-defect, and remaining shell budgets.
Thus the preprint does not prove that a localization residual automatically
becomes a coercive payment available from the Leray energy inequality.

### 3.3 The R0.71K quotient

R0.71K retains the nonlinear combination

\[
 \frac{((B^L_{j,Q})^+)^2}{d_{j,Q}\,Y}
\]

and the complete time derivative of its projective direction.  Its possible
difference lies only in this combined consumer and its proposed payment.  It
does not lie in cutoffs, partitions, local fluxes, commutators, or
space--scale filtering separately.

## 4. Search finding and claim boundary

This bounded ten-source primary search did not locate a theorem isomorphic to
the full normalized quotient and ledger above.  That negative search finding
is not an originality, priority, or publication-level determination.  A
formal novelty claim would require broader bibliographic databases and expert
citation review.

The literature imposes four immediate restrictions on R0.71K:

1. a localization residual cannot be called a coercive gain merely because it
   is written as a nonnegative budget;
2. a result requiring coherence, a small Kraichnan scale, Carleson
   summability, or an adjoint cutoff is conditional and must be labeled so;
3. the fixed-partition collar must be retained at its actual scale rather than
   absorbed into a generic lower-order term; and
4. no local smooth calculation may be conflated with the CKN suitable-weak
   local energy inequality or with a Leray-limit theorem.
