# R0.70L bounded primary-literature audit

**Question.** Does the primary literature already provide either (i) the
exact evolution of a filtered strain source that can be coupled to the
R0.70K normalized vorticity covariance, or (ii) a deterministic compensator
whose evolution absorbs the positive source--shape variance?

**Protocol.** The search used three bounded passes: exact filtered
velocity-gradient equations; pressure-Hessian and restricted-Euler
closures; and exact adjacent-scale/filter identities. It stopped after
eleven high-signal primary sources because later results repeated the same
three categories. This is a bounded-search saturation statement, not a proof
that no further relevant paper exists.

**Finding.** The first item is known: the filtered strain equation contains
the local quadratic term, filtered vorticity dyad, deviatoric pressure
Hessian, viscosity, and a symmetric Hessian of the SGS stress. The second
item was not found. Existing pressure and recent-deformation closures are
statistical or modeled; exact filter identities do not supply a time sign.

---

## 1. Tom--Carbone--Bragg: filtered velocity-gradient dynamics

**Primary source:** J. Tom, M. Carbone, and A. D. Bragg, *Exploring the
turbulent velocity gradients at different scales from the perspective of the
strain-rate eigenframe*, Journal of Fluid Mechanics 910 (2021),
[arXiv](https://arxiv.org/abs/2005.04300),
[DOI](https://doi.org/10.1017/jfm.2020.960).

For a derivative-commuting filter, resolved velocity (U), and

\[
 \tau=\overline{u\otimes u}-U\otimes U,
 \qquad A=\nabla U,
\]

the exact resolved-gradient equation has the form

\[
 D_t^U A=-A^2-\nabla^2P+\nu\Delta A
          -\nabla(\nabla\!\cdot\tau).
 \tag{A.1}
\]

Its symmetric trace-free part is the exact source equation used in R0.70L.
The paper's statements that the anisotropic pressure Hessian controls much of
the eigenframe rotation and that the SGS term regularizes the dynamics are
DNS/statistical findings.

**Does not provide.** A pointwise sign for pressure or SGS contraction with
an arbitrary normalized covariance (B), or a Lyapunov inequality.

## 2. Wilczek--Meneveau: exact pressure nonlocality and Gaussian closure

**Primary source:** M. Wilczek and C. Meneveau, *Pressure Hessian and viscous
contributions to velocity gradient statistics based on Gaussian random
fields*, Journal of Fluid Mechanics 756 (2014),
[arXiv](https://arxiv.org/abs/1401.3351),
[DOI](https://doi.org/10.1017/jfm.2014.367).

The paper starts from the exact unfiltered strain equation and a singular
integral representation of the deviatoric pressure Hessian. Under a Gaussian
velocity-field assumption it derives a conditional mean closure built from
((S^2)^circ), ((W^2)^circ), and (SW-WS).

**Use.** It cleanly separates exact nonlocal pressure structure from a model
for its conditional average.

**Does not provide.** A trajectorywise identity for the conditional closure,
or a universal sign for (B:(\nabla^2p)^circ).

## 3. Germano: exact nested-filter identity

**Primary source:** M. Germano, *Turbulence: the filtering approach*, Journal
of Fluid Mechanics 238 (1992),
[DOI](https://doi.org/10.1017/S0022112092001733).

For compatible nested filters (F,G), the exact central-moment identity
decomposes the stress at the composite scale into a filtered fine-scale
stress plus the stress of the filtered field. It is the correct algebraic
ledger for adjacent-scale SGS terms.

**Does not provide.** A time-direction sign, a physical-cutoff estimate, or a
compensator for (q=\Sigma:B).

## 4. Johnson: exact Gaussian scale calculus

**Primary source:** P. L. Johnson, *Energy Transfer from Large to Small
Scales in Turbulence by Multiscale Nonlinear Strain and Vorticity
Interactions*, Physical Review Letters 124 (2020),
[arXiv](https://arxiv.org/abs/1912.00293),
[DOI](https://doi.org/10.1103/PhysRevLett.124.104501), and
[erratum](https://doi.org/10.1103/PhysRevLett.126.029901).

For the Gaussian semigroup,

\[
 \partial_{\ell^2}\bar u^\ell=\frac12\Delta\bar u^\ell,
 \qquad
 \partial_{\ell^2}\tau_{ij}^\ell
 =\frac12\Delta\tau_{ij}^\ell
  +A_{ik}^\ell A_{jk}^\ell.
 \tag{A.2}
\]

Integrating (A.2) gives an exact scale integral for the SGS stress and an
exact split of energy transfer into strain, vorticity, and cross-scale
interactions.

**Does not provide.** An evolution equation for the R0.70K correlation, a
pointwise compensator, or an energy-only bound for its positive part.

## 5. Cantwell: restricted Euler as a baseline

**Primary source:** B. J. Cantwell, *Exact solution of a restricted Euler
equation for the velocity gradient tensor*, Physics of Fluids A 4 (1992),
[DOI](https://doi.org/10.1063/1.858295).

Deleting the deviatoric pressure Hessian and viscosity gives

\[
 \dot A=-A^2+\frac13\operatorname{tr}(A^2)I.
 \tag{A.3}
\]

The resulting invariant system has exact finite-time singular branches.

**Use.** It is a baseline showing why the omitted pressure and viscous terms
cannot be treated as optional details in a regularity mechanism.

**Does not provide.** A singularity theorem for NSE or a valid pressure
compensator.

## 6. Chevillard--Meneveau: recent fluid deformation

**Primary source:** L. Chevillard and C. Meneveau, *Lagrangian Dynamics and
Statistical Geometric Structure of Turbulence*, Physical Review Letters 97
(2006), [arXiv](https://arxiv.org/abs/cond-mat/0606267),
[DOI](https://doi.org/10.1103/PhysRevLett.97.174501).

The recent-fluid-deformation model uses
(C_\tau=e^{\tau A}e^{\tau A^{\mathsf T}}) to close pressure and viscosity
in a stochastic Lagrangian model. It avoids the restricted-Euler blow-up and
reproduces several gradient statistics.

**Does not provide.** An exact NSE identity, deterministic sign, or
high-Reynolds-number a priori bound.

## 7. Chevillard--Meneveau--Biferale--Toschi: closure assumptions audited

**Primary source:** L. Chevillard, C. Meneveau, L. Biferale, and F. Toschi,
*Modeling the pressure Hessian and viscous Laplacian in turbulence: comparisons
with direct numerical simulation and implications on velocity gradient
dynamics*, Physics of Fluids 20 (2008),
[arXiv](https://arxiv.org/abs/0712.0900),
[DOI](https://doi.org/10.1063/1.3005832).

The paper begins with the exact velocity-gradient equation and makes explicit
the assumptions behind recent-deformation pressure and viscous closures:
Lagrangian isotropy of an earlier pressure Hessian, frozen recent gradients,
neglected spatial variation of the inverse deformation, and a linear viscous
model.

**Does not provide.** A theorem transferring the modeled stabilization to
the deterministic NSE.

## 8. Hamlington--Schumacher--Dahm: local/background strain split

**Primary source:** P. E. Hamlington, J. Schumacher, and W. J. A. Dahm,
*Direct assessment of vorticity alignment with local and nonlocal strain
rates in turbulent flows*, Physical Review E 77 (2008),
[arXiv](https://arxiv.org/abs/0801.1248),
[DOI](https://doi.org/10.1103/PhysRevE.77.026303).

The Biot--Savart strain is split into a ball contribution and a background
contribution. Under its convergence hypotheses the background admits a local
Laplacian expansion.

**Use.** This gives a precise kinematic meaning to local versus exterior
strain.

**Does not provide.** A closed material evolution for the exterior part; a
moving ball introduces transport and boundary commutators.

## 9. Hamlington--Schumacher--Dahm: alignment evidence

**Primary source:** P. E. Hamlington, J. Schumacher, and W. J. A. Dahm,
*Local and nonlocal strain rate fields and vorticity alignment in turbulent
flows*, Physics of Fluids 20 (2008),
[arXiv](https://arxiv.org/abs/0810.3439),
[DOI](https://doi.org/10.1063/1.3021055).

DNS shows preferential alignment with the intermediate eigenvector of the
total strain and stronger alignment with the most extensional eigenvector of
the background strain.

**Does not provide.** Pointwise alignment, a uniform angular bound, or a
signed deterministic evolution for (q).

## 10. Carbone--Bragg: averaged strain and vorticity production

**Primary source:** M. Carbone and A. D. Bragg, *Is vortex stretching the
main cause of the turbulent energy cascade?*, Journal of Fluid Mechanics 883
(2020), [arXiv](https://arxiv.org/abs/1906.07144),
[DOI](https://doi.org/10.1017/jfm.2019.923).

The paper derives an exact filtered energy-transfer decomposition and uses
the homogeneous Betchov identity to compare mean strain self-amplification
and vortex stretching.

**Does not provide.** A pointwise causal statement or a Lyapunov sign.
Homogeneous averaging removes divergences that a physical cutoff retains.

## 11. Yang--Xu--Pumir--He: strong-vorticity pressure asymptotics

**Primary source:** Y. Yang, H. Xu, A. Pumir, and G. He, *Structure and role
of the pressure Hessian in regions of strong vorticity in turbulence*,
Journal of Fluid Mechanics 985 (2024),
[DOI](https://doi.org/10.1017/jfm.2024.143).

In strong-vorticity regions the paper proposes and tests the leading-order
approximation

\[
 H^p_{ij}\approx
 -\frac13\operatorname{tr}(A^2)\delta_{ij}
 -\frac14\left(\omega_i\omega_j
 -\frac13|\omega|^2\delta_{ij}\right).
 \tag{A.4}
\]

The deviatoric part can approximately cancel the vorticity dyad in the
strain equation in the studied regime.

**Does not provide.** A global error bound, an all-scale identity, or a
deterministic sign outside the strong-vorticity asymptotic regime.

---

## 12. Collision with R0.70L

Let (\Sigma_\ell=S(U_\ell)(X_\ell(t),t)), with
(\dot X_\ell=U_\ell(X_\ell,t)). Coupling the exact filtered source equation
to R0.70K gives

\[
\begin{aligned}
 \dot q_\ell={}&
 2\operatorname{tr}[R_\ell(\Sigma_\ell-q_\ell I)^2]\\
 &+B_\ell:\left[
 -(\Sigma_\ell^2)^\circ
 -\frac14(\Omega_\ell\otimes\Omega_\ell)^\circ
 -(\nabla^2P_\ell)^\circ
 +\nu\Delta S(U_\ell)
 -K_{\tau_\ell}^\circ\right]_{X_\ell}\\
 &+\Sigma_\ell:\mathcal T_{B_\ell}(F_{\rm err}).
 \tag{A.5}
\end{aligned}
\]

The first source-evolution test is already indefinite:

\[
 2\operatorname{tr}[R(\Sigma-qI)^2]-B:\Sigma^2
 =B:\Sigma^2+\frac23|\Sigma|_F^2-2q^2.
 \tag{A.6}
\]

For (\Sigma=\operatorname{diag}(2,-1,-1)), (A.6) equals (-2) at
(R=e_1\otimes e_1), but (+1) at (R=e_2\otimes e_2).

No audited source provides a deterministic estimate that controls all of the
pressure, SGS, cutoff, denominator, and neighboring-scale terms in (A.5).
The literature therefore fixes the exact ledger but leaves the compensator
problem open.

## 13. Research boundary

The R0.70L novelty claim must remain narrow:

- the filtered strain equation and pressure nonlocality are established;
- restricted-Euler and recent-deformation closures are models, not proofs;
- Gaussian scale calculus and Germano identities are exact but unsigned;
- the new task is to prove or exclude a compensator for this particular
  normalized covariance correlation.

Finding such a compensator with an energy-controlled scale sum would be a
substantive analytical result. A bounded literature gap is not evidence that
the Millennium problem has been advanced.
