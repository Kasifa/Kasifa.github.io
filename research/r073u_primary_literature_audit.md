# R0.73U primary-literature audit: tensor correlations, heat filtering, and closure

**Audit date:** 2026-09-01

**Status:** bounded primary-source search complete for the frozen R0.73U
question; absence of a collision is not a novelty or priority certificate

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## 1. The decisive object distinction

R0.73U uses the heat-filtered local product

\[
 \Theta_{s,ij}=e^{s\Delta}(u_i u_j).
\]

The classical K\'arm\'an--Howarth--Monin (KHM) tensor instead uses a two-point
covariance such as

\[
 R_{ij}(r)=\int u_i(x)u_j(x+r)\,d\mu(x).
\]

Their Fourier data are different.  \(\widehat\Theta_{s,ij}(h)\) contains a
convolution over different velocity wave numbers, whereas
\(\widehat R_{ij}(k)\) contains the same-wave-number covariance
\(\widehat u_j(k)\overline{\widehat u_i(k)}\).  Literature statements about
one object cannot be transferred silently to the other.

## 2. Exact KHM hierarchy and its closure boundary

Von K\'arm\'an and Howarth derived the classical two-point equation for
homogeneous isotropic turbulence:

- T. von K\'arm\'an and L. Howarth, *On the Statistical Theory of Isotropic
  Turbulence*, Proceedings of the Royal Society A 164 (1938), 192--215,
  [DOI](https://doi.org/10.1098/rspa.1938.0013).

Hill later derived exact arbitrary-order structure-function equations directly
from Navier--Stokes and incompressibility:

- R. J. Hill, *Equations Relating Structure Functions of all Orders*, Journal
  of Fluid Mechanics 434 (2001), 379--388,
  [DOI](https://doi.org/10.1017/S0022112001003949).

For the scalar homogeneous trace, incompressibility and averaging can cancel
the pressure contribution, but the equation still contains a signed
third-order increment flux.  For the full second-order tensor, third-order
velocity moments and pressure--velocity correlations remain.  Continuing the
moment equation generates the next order; this is an exact hierarchy, not a
finite autonomous closure.

A current direct collision is:

- N. Zambrano and K. Duraisamy, *Two-point turbulence closures in physical
  space*, Journal of Fluid Mechanics 1034 (2026), A12,
  [DOI](https://doi.org/10.1017/jfm.2026.11485).

That paper explicitly treats the K\'arm\'an--Howarth third-order moment as
unclosed and builds a predictive closure for homogeneous isotropic turbulence
using quasi-normal, Markovian, and phenomenological eddy-damping assumptions.
It is valuable evidence about the closure landscape, but it is not a theorem
closing general deterministic three-dimensional Navier--Stokes quadratic data.

## 3. Instantaneous pressure sufficiency is not dynamic closure

For the local product tensor, the pressure Poisson equation gives

\[
 \widehat p(h)=-{h_i h_j\over|h|^2}
 \widehat{u_i u_j}(h),\qquad h\ne0.
\]

Thus \(u\otimes u\), unlike its scalar trace, is sufficient for instantaneous
pressure reconstruction.  Its time equation nevertheless contains
\(u_i u_j u_k\), \(p u_i\), and gradient products.  The pressure formula turns
the pressure--velocity terms into nonlocal third-order velocity expressions;
it does not reduce them to the quadratic tensor.

The safe classification is therefore:

```text
instantaneousPressureFromLocalProductTensor=VERIFIED_CLASSICAL
quadraticTensorOnlyDynamicClosure=NOT_ESTABLISHED
exactHigherMomentHierarchy=VERIFIED_CLASSICAL
```

## 4. Filtering and exact subgrid stress

Germano formalized filtered Navier--Stokes equations and algebraic identities
relating stresses at different filter levels:

- M. Germano, *Turbulence: the filtering approach*, Journal of Fluid
  Mechanics 238 (1992), 325--336,
  [DOI](https://doi.org/10.1017/S0022112092001733).

For a Gaussian/heat filter the semigroup property makes the two-level
identity especially direct.  Exact filtering introduces the stress
\(\tau_s=P_s(u\otimes u)-P_su\otimes P_su\); it does not supply an autonomous
constitutive relation for \(\tau_s\) in terms of the resolved field at one
scale.

Eyink derived exact subgrid stress/flux formulae and rigorous locality
estimates under stated filter and velocity hypotheses:

- G. L. Eyink, *The Multifractal Model of Turbulence and A Priori Estimates in
  Large-Eddy Simulation, I. Subgrid Flux and Locality of Energy Transfer*
  (1996), [arXiv:chao-dyn/9602018](https://arxiv.org/abs/chao-dyn/9602018).

The exact coarse-grained energy-transfer quantity is
\(-\nabla v_s:\tau_s\).  It is signed.  Neither positivity of the covariance
tensor nor exact scale composition makes this flux sign-definite or closed.

## 5. Commutators and signed third-order increments

The classical Onsager commutator route uses the filtered product difference
\((u\otimes u)_\varepsilon-u_\varepsilon\otimes u_\varepsilon\):

- P. Constantin, W. E, and E. S. Titi, *Onsager's conjecture on the energy
  conservation for solutions of Euler's equation*, Communications in
  Mathematical Physics 165 (1994), 207--209,
  [DOI](https://doi.org/10.1007/BF02099744).

Duchon--Robert express the local energy defect through a signed third-order
velocity-increment integral:

- J. Duchon and R. Robert, *Inertial energy dissipation for weak solutions of
  incompressible Euler and Navier--Stokes equations*, Nonlinearity 13 (2000),
  249--255, [DOI](https://doi.org/10.1088/0951-7715/13/1/312).

These works support the R0.73U information boundary: the transfer object is
phase/sign sensitive and cubic.  They concern energy conservation and defect
formulae, not the specific four-site tensor-tangent witness constructed here.

## 6. Collision table

| R0.73U slot | Nearest primary literature | What is established | What is not supplied |
|---|---|---|---|
| exact two-point hierarchy | von K\'arm\'an--Howarth 1938; Hill 2001 | exact second- and higher-order balance equations | finite general nonlinear closure |
| local tensor reconstructs pressure | pressure Poisson/Riesz formula | instantaneous pressure from \(u\otimes u\) | tensor-only time evolution |
| filtered stress and scale composition | Germano 1992 | exact filtered equations and inter-filter identity | exact constitutive closure from one resolved scale |
| signed SGS flux and locality | Eyink 1996 | exact stress/flux formulae and conditional locality estimates | sign-definite flux or arbitrary-data critical bound |
| third-order commutator/defect | Constantin--E--Titi 1994; Duchon--Robert 2000 | cubic increment controls energy transfer/defect | quadratic-only autonomous dynamics |
| contemporary physical-space closure | Zambrano--Duraisamy 2026 | model-based HIT closure and validation | deterministic general 3D Navier--Stokes closure theorem |
| R0.73U heat covariance PDE | direct semigroup/product proof | exact identity in the present note | novelty or priority conclusion |
| R0.73U four-site parity witness | exact local finite certificate | non-autonomy of the even quadratic heat state | failure of every signed or higher-order augmentation |

## 7. Bounded-search conclusion

The search found extensive exact hierarchy and filtering literature, and it
found modern closures that add statistical/model assumptions.  It did not
locate an existing theorem matching the exact package

```text
heat-covariance scale PDE
+ critical L2_t L3_x tensor row
+ four-site quadratic-state parity witness
+ coefficient-level parabolic s^(-1/2) separation.
```

This is only a bounded collision-search result.  It cannot support a claim of
novelty, priority, or non-existence.  The public release should describe
R0.73U as an auditable local synthesis and exact finite obstruction.  General
three-dimensional Navier--Stokes regularity remains open.
