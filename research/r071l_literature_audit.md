# R0.71L primary-source audit — fixed-cell viscous collars, cutoff commutators, and fused projective tangents

Search date: 2026-08-26.

## 1. Exact collision object

This audit asks a narrower question than whether localized energy,
localized enstrophy, commutator estimates, or vorticity-direction equations
exist in the literature.

For a fixed spatial cutoff \(\chi_{j,Q}\) at the matched radius
\(r_j\asymp\kappa_j^{-1}\), R0.71K uses

\[
 C_{j,Q}=\nabla\times(\chi_{j,Q}W_j),
 \qquad
 \rho_{j,Q}=\|C_{j,Q}\|_2,
 \qquad
 E_{j,Q}=\frac{C_{j,Q}}{\rho_{j,Q}},
\]

and

\[
 P_{j,Q}=I-E_{j,Q}\otimes E_{j,Q}.
\]

The cutoff--curl is part of the state:

\[
 C_{j,Q}
 =\chi_{j,Q}\nabla\times W_j
  +\nabla\chi_{j,Q}\times W_j.
 \tag{1.1}
\]

For a fixed cutoff, the localized curl equation contains the full viscous
commutator

\[
 \mathcal K_{\chi}W
 =2\sum_m(\partial_m\chi)\partial_mW+(\Delta\chi)W,
\]

\[
 C_{j,Q,t}
 =\nu\Delta C_{j,Q}
  +\nabla\times(\chi_{j,Q}\mathcal G_j)
  -\nu\nabla\times(\mathcal K_{\chi_{j,Q}}W_j),
 \tag{1.2}
\]

where \(\mathcal G_j\) denotes the relevant nonlinear frequency source.  With

\[
 M_{j,Q}=C_{j,Q,t}+\nu\kappa_j^2C_{j,Q},
\]

the tangent row in the complete normalized source is

\[
 \mathfrak T_{j,Q}
 =\frac{
 \langle P_{j,Q}F_j,P_{j,Q}M_{j,Q}\rangle}
 {\rho_{j,Q}}.
 \tag{1.3}
\]

Equivalently,

\[
 \partial_t E_{j,Q}
 =\frac{P_{j,Q}C_{j,Q,t}}{\rho_{j,Q}}.
 \tag{1.4}
\]

A source collides with the R0.71L fixed-cell fused-tangent question only if
it supplies all of the following:

1. a theorem for Leray--Hopf or suitable weak solutions, rather than only a
   smooth or Gevrey solution;
2. a fixed, preassigned spatial cutoff or matched finite-overlap cell family,
   rather than a solution-adapted, transported, or selected favorable cutoff;
3. the complete cutoff--curl and viscous-collar source in (1.1)--(1.2);
4. the normalized projective tangent in (1.3), including the
   \(\rho_{j,Q}^{-1}\) factor;
5. an absolute or positive fused source budget after the cell and scale
   operations used by the consumer; and
6. a non-circular bound from the Leray energy and dissipation alone, with no
   assumed local palinstrophy, denominator lower bound, coherence, Morrey or
   Serrin norm, Besov increment defect, Carleson closure, adjoint cutoff, or
   summable shell budget.

Using a cutoff, a physical-space cover, a vorticity direction, or a Rayleigh
quotient separately is therefore not a collision.

## 2. Direct decision

The bounded primary-source search did not locate a theorem satisfying the six
collision conditions above.  It also did not locate a published
Navier--Stokes counterexample isomorphic to the full fixed-cell fused tangent.

The literature does contain three narrower positive mechanisms:

1. scalar local kinetic-energy cutoff rows for suitable weak solutions;
2. scalar local enstrophy rows under local smallness, favorable localization,
   or additional geometric and scale hypotheses; and
3. single-cutoff or single-operator \(L^2\) commutator bounds.

None of these statements by itself controls the fused quotient (1.3).

## 3. Primary-source matrix

| Primary source and status | Object actually controlled | Additional input or mechanism | Difference from the fixed-cell fused tangent |
|---|---|---|---|
| Caffarelli--Kohn--Nirenberg, *Partial regularity of suitable weak solutions of the Navier--Stokes equations* (1982, published), [DOI](https://doi.org/10.1002/cpa.3160350604) | The local kinetic-energy inequality for suitable weak solutions, including the classical scalar cutoff, pressure, transport, and viscous rows. | Suitability supplies a one-sided local energy inequality at velocity level. | No test of the vorticity equation by localized vorticity, no frequency parent, no cutoff--curl state, no viscous curl collar, and no normalized tangent. |
| Dascaliuc--Grujić, *Energy cascades and flux locality in physical scales of the 3D Navier--Stokes equations* (2011, published), [arXiv:1101.2193](https://arxiv.org/abs/1101.2193), [DOI](https://doi.org/10.1007/s00220-011-1219-8) | Refined physical-space cutoffs, bounded-multiplicity covers, and ensemble-averaged local kinetic-energy and pressure flux for suitable weak solutions. | A Taylor-microscale condition relative to the integral scale identifies the inertial range. | The controlled object is a signed scalar energy flux.  There is no local curl denominator, positive-part square, projective direction, or absolute tangent budget. |
| Tao, *Localisation and compactness properties of the Navier--Stokes global regularity problem* (2013, published), [arXiv:1108.1165](https://arxiv.org/abs/1108.1165), [DOI](https://doi.org/10.2140/apde.2013.6.25) | Theorem 10.1 gives localized \(L_t^\infty L_x^2\) vorticity and \(L_t^2L_x^2\) vorticity-gradient control inside a smaller ball. | Local initial vorticity and curl-forcing smallness; \(\delta^4T+\delta^5E^{1/2}T\) small; a sufficiently wide collar; and a shrinking cutoff with a favorable radius selected by averaging. | This is a scalar local-enstrophy theorem for finite-energy almost-smooth solutions.  It does not cover every preassigned matched cell and does not contain a normalized projective tangent. |
| Dascaliuc--Grujić, *Coherent vortex structures and 3D enstrophy cascade* (2013, published), [arXiv:1107.0058](https://arxiv.org/abs/1107.0058), [DOI](https://doi.org/10.1007/s00220-012-1595-8) | A localized physical-scale enstrophy balance and an ensemble enstrophy cascade. | One-half-Hölder coherence of the vorticity direction, a modified Kraichnan-scale condition, and an endpoint modulation hypothesis. | The conclusion compares a conditional signed flux with modified palinstrophy.  It is not a Leray-only payment for an absolute collar or the quotient (1.3). |
| Leitmeyer, *Enstrophy Cascade in Physical Scales for the Three-Dimensional Navier--Stokes Equations* (2016, published), [arXiv:1502.01258](https://arxiv.org/abs/1502.01258), [DOI](https://doi.org/10.1137/140997154) | Refined test functions, exact finer partitions, bounded-overlap ensembles, and an enstrophy-cascade theorem. | Vorticity-direction coherence, a modified Kraichnan condition, endpoint modulation, an \(L^1\)-type vorticity bound, and \(L_t^2M_x^{2,q}\) Morrey control.  The paper explicitly notes that the Morrey input is stronger than the \(L_t^2L_x^2\) information available for all Leray solutions. | This is geometrically close to matched physical cells, but the theorem is a conditional linear-flux statement without a frequency parent, a local normalization, or a tangent denominator. |
| Yu, *Filtered Vortex Stretching and Subgrid Defects for the Three-Dimensional Navier--Stokes Equations* (2026, arXiv preprint v1; not a peer-reviewed theorem at the search date), [arXiv:2606.27560v1](https://arxiv.org/abs/2606.27560v1), [arXiv DOI](https://doi.org/10.48550/arXiv.2606.27560) | Proposition 6.1 gives an exact localized filtered-enstrophy identity.  Proposition 6.4 cancels the principal localization residual with a backward adjoint drift--diffusion cutoff.  Theorem 9.3 controls differentiated commutator forcing by diffusion, a derivative-compatible scale-invariant increment defect, and shell terms. | A solution-adapted adjoint cutoff is needed for exact principal cutoff cancellation.  The unweighted closure in Corollary 10.2 and Theorem 10.3 additionally assumes far-field Carleson closure, increment-defect summability, and summable localization/shell budgets. | This is the closest current filtered-vorticity comparison.  Its residuals are additive scalar enstrophy rows, not \(\langle P F,P M\rangle/\rho\); its unweighted closure is conditional and its cutoff is not the fixed preassigned R0.71L cell. |
| Constantin--Fefferman, *Direction of vorticity and the problem of global regularity for the Navier--Stokes equations* (1993, published), [journal page](https://iumj.org/article/3627/), together with Beirão da Veiga--Berselli, *On the regularizing effect of the vorticity direction in incompressible viscous flows* (2002, published), [author PDF](https://people.dm.unipi.it/beiraodaveiga/pdf/hbv-79.pdf), [DOI](https://doi.org/10.57262/die/1356060864) | Geometric depletion criteria based on spatial vorticity-direction coherence.  The Constantin--Fefferman estimate recalled as equation (3.2) by Beirão da Veiga--Berselli controls \(\int|\omega||\nabla\xi|^2\) when \(\omega_0\in L^1\). | Spatial direction coherence or Sobolev control is a regularity hypothesis; the unconditional weighted spatial-direction estimate additionally assumes \(L^1\) initial vorticity. | The object is the physical pointwise spatial direction \(\xi=\omega/|\omega|\), not the temporal Hilbert-space direction \(E_{j,Q}=C_{j,Q}/\|C_{j,Q}\|_2\).  It does not supply a cellwise denominator lower bound or a fused time-tangent budget. |
| Calderón, *Commutators of singular integral operators* (1965, published), [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC301378/), and Coifman--Meyer, *Commutateurs d'intégrales singulières et opérateurs multilinéaires* (1978, published), [journal page](https://numdam.org/articles/10.5802/aif.708/) | Classical \(L^2\) boundedness for commutators of singular or first-order pseudodifferential operators with a sufficiently regular, in particular Lipschitz or \(C_c^1\), coefficient. | The coefficient regularity pays for the commutator at a fixed operator level. | These results justify single-cutoff estimates but do not state a scale-weighted matched-cell absolute budget for \(\nabla\times[\Delta,\chi]W\), and they do not address normalization by \(\rho_{j,Q}\). |
| Gibbon--Holm--Kerr--Roulstone, *Quaternions and particle dynamics in the Euler fluid equations* (2006, published), [arXiv:nlin/0512034](https://arxiv.org/abs/nlin/0512034), [DOI](https://doi.org/10.1088/0951-7715/19/8/011) | Exact Lagrangian equations for Euler vorticity growth and rotation, with the direction/frame dynamics driven by a pressure-Hessian tetrad. | Smooth Euler dynamics and pressure-Hessian information. | This confirms that a direction tangent carries its own source.  It has no viscosity, fixed cutoff, local \(L^2\) normalization, or Leray-level estimate. |
| Ignatova--Kukavica, *Strong Unique Continuation for the Navier--Stokes Equation with Non-Analytic Forcing* (2013, published), [author PDF](https://web.math.princeton.edu/~ignatova/IK_NSE.pdf), [DOI](https://doi.org/10.1007/s10884-012-9282-1) | Remark 2.5 derives a Dirichlet/Rayleigh quotient inequality for a linear periodic parabolic equation \(v_t-\Delta v+b\cdot\nabla v+cv=0\). | The bound depends on \(L^\infty\) norms of \(b,c\) and on the initial quotient.  The Navier--Stokes unique-continuation theorem uses Gevrey and doubling hypotheses. | This is a strong-solution, coefficient-controlled quotient estimate, not a fixed-cell projective tangent for an energy-class solution. |

## 4. What the established estimates safely provide

### 4.1 Scalar viscous cutoff pairing

For a scalar localized enstrophy identity, integration by parts produces a
row of the form

\[
 \iint(\Delta\chi)|\omega|^2.
\]

For a matched cutoff,

\[
 \left|
 \iint(\Delta\chi)|\omega|^2
 \right|
 \lesssim
 \kappa^2\iint_{\operatorname{collar}(\chi)}|\omega|^2.
 \tag{4.1}
\]

On \(\mathbb R^3\) or the torus, the time integral of
\(\|\omega\|_2^2\) is controlled at Leray level.  Thus (4.1) is a legitimate
fixed-scale scalar payment, with its explicit \(\kappa^2\) loss retained.
It is not an estimate of the \(L^2\) norm of the vector collar source and it
does not survive division by a possibly small \(\rho_{j,Q}\).

### 4.2 Cutoff--curl

The exact identity

\[
 [\nabla\times,\chi]W=\nabla\chi\times W
\]

gives

\[
 \|[\nabla\times,\chi]W\|_2
 \le
 \|\nabla\chi\|_\infty\|W\|_2.
 \tag{4.2}
\]

This is an energy-level estimate for one cutoff.  It does not make the term
small relative to the interior curl at the matched scale, and it does not
control the derivative of the normalized cell direction.

### 4.3 Classical operator commutators

Calderón and Coifman--Meyer provide the correct background for fixed
Lipschitz-coefficient commutators.  A vector-valued dyadic aggregation,
arbitrary cell weights, the second-order viscous commutator, and the
projective denominator require separate estimates.  None of those extensions
is asserted here as an automatic corollary of the classical theorem.

## 5. Scale and denominator obstacles

The observations in this section are direct order counts or elementary
Hilbert-space facts.  They are not cited as published Navier--Stokes
counterexamples.

### 5.1 The matched viscous collar is principal order

At frequency \(\kappa\), with

\[
 |\nabla\chi|\asymp\kappa,
 \qquad
 |\Delta\chi|\asymp\kappa^2,
\]

one has schematically

\[
 C=\nabla\times(\chi W)\asymp\kappa W,
\]

\[
 \Delta C\asymp\kappa^3W,
 \qquad
 \nabla\times(\mathcal K_\chi W)\asymp\kappa^3W.
 \tag{5.1}
\]

Thus the viscous collar and the localized principal diffusion are the same
parabolic order.  Fixedness of the cutoff removes cutoff motion and refresh
rows; it does not turn the viscous collar into a lower-order error.

### 5.2 The cutoff--curl is not a small denominator perturbation

At the same matched scale,

\[
 \chi\nabla\times W\asymp\kappa W,
 \qquad
 \nabla\chi\times W\asymp\kappa W.
 \tag{5.2}
\]

Although (4.2) controls the second term for a fixed cell, it can be as large
as the interior curl that defines the denominator.  A proof cannot replace
\(\rho=\|\nabla\times(\chi W)\|_2\) by an interior-only norm without a
separate comparison theorem.

### 5.3 Leray energy gives no local denominator floor

The map

\[
 C\longmapsto \frac{C}{\|C\|_2}
\]

is singular at \(C=0\), and (1.4) contains exactly this singularity.  The
global Leray inequality gives no positive lower bound for every
\(\rho_{j,Q}\).  Therefore an estimate of \(M_{j,Q}\) in a negative or
unprojected norm does not by itself bound

\[
 \frac{\|P_{j,Q}M_{j,Q}\|_2}{\rho_{j,Q}}
\]

or its pairing with \(P_{j,Q}F_j\).

An elementary abstract example makes the logical gap explicit.  For
orthonormal vectors \(e_1,e_2\), put

\[
 C_n(t)=n^{-1}(\cos(nt)e_1+\sin(nt)e_2).
\]

Its amplitude tends to zero, while

\[
 \left\|
 \partial_t\frac{C_n}{\|C_n\|}
 \right\|=n.
\]

This is not a Navier--Stokes solution.  It shows only that amplitude and
dissipation-size information cannot abstractly control a projective time
tangent without additional evolution structure or a denominator floor.

## 6. Conflict and gap ledger

### Established and available

- suitable-weak local kinetic-energy inequalities;
- refined bounded-overlap physical-space covers;
- scalar localized enstrophy identities in regimes where they are justified;
- conditional enstrophy cascade and palinstrophy comparisons;
- fixed Lipschitz-cutoff and pseudodifferential commutator estimates;
- spatial vorticity-direction depletion and conditional regularity criteria;
- strong-solution Dirichlet-quotient inequalities.

### Not supplied by the checked sources

- an absolute fixed-cell bound for the full viscous curl collar at every
  matched scale using only the Leray budget;
- a cellwise lower bound for
  \(\|\nabla\times(\chi_{j,Q}W_j)\|_2\);
- a Leray-level bounded-variation estimate for the normalized local direction
  \(E_{j,Q}\);
- a non-circular estimate for the fused term
  \(\langle P_{j,Q}F_j,P_{j,Q}M_{j,Q}\rangle/\rho_{j,Q}\);
- a scale-uniform positive or absolute cell sum with the R0.71K consumer
  weights.

### Extra hypotheses that change the claim

Any positive theorem obtained by assuming one of the following must be
reported as conditional rather than as a Leray-only closure:

- local initial enstrophy smallness or a favorable selected collar;
- vorticity-direction coherence;
- a small modified Kraichnan scale or endpoint modulation;
- Morrey, Serrin, Besov, or increment-defect control;
- a solution-adapted backward adjoint cutoff;
- unweighted Carleson closure or summable shell/localization budgets;
- a positive lower bound on every active cell denominator; or
- bounded strong-solution coefficients and an initial Rayleigh quotient.

## 7. Bounded negative finding

The primary-source search covered:

- suitable-weak local energy and partial regularity;
- physical-space energy and enstrophy cascades;
- Tao's local energy/enstrophy localization;
- filtered-vorticity commutator and localization defects;
- spatial vorticity-direction regularity;
- singular-integral and pseudodifferential commutators;
- Euler vorticity-direction dynamics; and
- parabolic Dirichlet/Rayleigh quotient estimates.

The search also used direct combinations of fixed cutoff, localized
vorticity, viscous commutator, normalized local enstrophy, projective tangent,
Rayleigh quotient, and Leray--Hopf terminology.  Those direct searches did
not identify a theorem or a published counterexample satisfying the collision
conditions in Section 1.

This is a bounded negative finding only.  It does not establish novelty,
priority, or nonexistence in the full literature.  A publication-level
originality statement would require a broader MathSciNet/zbMATH citation
review and expert checking, including later versions or responses to the 2026
Yu preprint.

## 8. Safe claim boundary for R0.71L

R0.71L may safely state:

1. scalar cutoff-collar and single-cutoff commutator controls have established
   precedents;
2. the matched viscous collar is principal order and the local normalization
   introduces a denominator singularity;
3. the checked local-enstrophy theorems use additional smallness, geometry,
   scale, localization, or summability inputs; and
4. this bounded primary-source search did not find a Leray-only theorem
   isomorphic to the fixed-cell fused tangent.

R0.71L must not state that the object is new, that no such theorem exists, or
that the scale and denominator observations constitute a published
Navier--Stokes counterexample.
