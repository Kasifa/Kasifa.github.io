# R0.74F — bounded primary-literature boundary and collision audit

## Status

**BOUNDED PRIMARY-LITERATURE AUDIT / NOT A NOVELTY PROOF.**

This note records a targeted search completed on 2026-09-01 for the
mathematical ingredients and the closest visible collision classes of
R0.74F.  It distinguishes established tools from the particular explicit
construction proved in `r074f_two_packet_survival.md`.  Absence from the
search results is not evidence of absolute priority, and no novelty or
priority claim is made here.

R0.74F is also **NOT CLAY**.  Its theorem is a lower bound for one frozen
endpoint on an explicit smooth solution family.  It does not prove the
open denominator estimate, endpoint divergence, singularity formation,
or global regularity.

---

## 1. Claim under comparison

The local R0.74F result combines the following specific ingredients:

1. an exact smooth, periodic, mean-zero 2D3C Navier--Stokes family with
   pressure zero;
2. a heat-evolved odd saturated shear and a pair of opposite derivative
   heat-kernel packets;
3. exact cancellation of the selected mollified trajectory and local
   acceleration;
4. a time-reversed Feynman--Kac formula in the moving positive-packet
   frame;
5. an all-winding periodic Brownian-bridge identity and an explicit
   weighted leakage estimate;
6. suppression of the inverted packet and a positive-measure terminal
   lobe contained in one frozen dyadic annulus; and
7. the conditional endpoint lower bound

   \[
   X_{R_j}^M=X_{R_j}^F
   \ge c\,\mathfrak a_j^2L_jR_j^2e^{-c_\gamma L_j^2}.
   \]

The comparison question is narrow: whether a primary source located by
the bounded search already states this combination or a theorem that
immediately implies it with the same geometry, weights, and endpoint.

---

## 2. Established ingredients

### 2.1 Feynman--Kac and pinned Wiener paths

Kac's classical paper relates distributions of Wiener functionals to
parabolic equations.  It establishes the historical probabilistic-PDE
boundary behind the Feynman--Kac step; it does not contain the R0.74F
periodic packet construction.

- Mark Kac, [On Distributions of Certain Wiener Functionals](https://www.jstor.org/stable/1990512),
  *Transactions of the American Mathematical Society* 65 (1949), 1--13,
  DOI [10.2307/1990512](https://doi.org/10.2307/1990512).

Güneysu proves the semimartingale property, including terminal time, for
adapted Brownian bridges on complete manifolds.  This confirms that
heat-kernel-defined pinned paths are standard objects in a substantially
broader geometric setting.  R0.74F instead needs and derives an elementary
one-dimensional torus identity retaining every winding copy and explicit
small-scale constants.

- Batu Güneysu,
  [On the semimartingale property of Brownian bridges on complete manifolds](https://alea.math.cnrs.fr/articles/v16/16-02.pdf),
  *ALEA* 16 (2019), 15--31,
  DOI [10.30757/ALEA.v16-02](https://doi.org/10.30757/ALEA.v16-02).

### 2.2 The 2D3C passive-scalar reduction

For two-dimensional three-component flows, the planar velocity obeys the
two-dimensional Navier--Stokes dynamics while the third component is
passively advected when the forcing does not couple it back.  That
structural reduction is established background, not an R0.74F novelty.

- Luca Biferale, Michele Buzzicotti, and Moritz Linkmann,
  [From two-dimensional to three-dimensional turbulence through two-dimensional three-component flows](https://www.pure.ed.ac.uk/ws/files/148081708/1706.02371.pdf),
  *Physics of Fluids* 29 (2017), 111101,
  DOI [10.1063/1.4990082](https://doi.org/10.1063/1.4990082).

### 2.3 Mixing and dispersion by incompressible and parallel shear flows

Constantin--Kiselev--Ryzhik--Zlatoš characterize relaxation-enhancing
flows on compact manifolds by spectral properties.  Wei develops a
resolvent route and includes quantitative dissipation results for shear
flows.  Coti Zelati--Gallay analyze enhanced dissipation and Taylor
dispersion for higher-dimensional parallel shears.  These sources place
R0.74F inside an established passive-scalar/shear-dispersion subject, but
their principal conclusions concern decay or dispersion rather than a
terminal lower lobe for the frozen endpoint used here.

- Peter Constantin, Alexander Kiselev, Lenya Ryzhik, and Andrej Zlatoš,
  [Diffusion and mixing in fluid flow](https://annals.math.princeton.edu/2008/168-2/p06),
  *Annals of Mathematics* 168 (2008), 643--674,
  DOI [10.4007/annals.2008.168.643](https://doi.org/10.4007/annals.2008.168.643).
- Dongyi Wei,
  [Diffusion and mixing in fluid flow via the resolvent estimate](https://arxiv.org/abs/1811.11904),
  arXiv:1811.11904; later published in *Science China Mathematics*,
  DOI [10.1007/s11425-018-9461-8](https://doi.org/10.1007/s11425-018-9461-8).
- Michele Coti Zelati and Thierry Gallay,
  [Enhanced dissipation and Taylor dispersion in higher-dimensional parallel shear flows](https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/jlms.12782),
  *Journal of the London Mathematical Society* 108 (2023), 1358--1392,
  DOI [10.1112/jlms.12782](https://doi.org/10.1112/jlms.12782).

Jiménez-Urias--Haine give analytical eigenfunction solutions for passive
scalar advection--diffusion under plane parallel shear, including
localized tracer dispersion.  This is the closest located source at the
level of exact laminar-shear solution analysis.  Its spectral/Mathieu
framework does not state the paired derivative-heat-packet construction,
the matched mollified-frame cancellation, or the R0.74F all-copy terminal
annulus estimate.

- Miguel A. Jiménez-Urias and Thomas W. N. Haine,
  [On the non-self-adjoint and multiscale character of passive scalar mixing under laminar advection](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/on-the-nonselfadjoint-and-multiscale-character-of-passive-scalar-mixing-under-laminar-advection/A12F2A99D516A4FAFA9BFF94334C056A),
  *Journal of Fluid Mechanics* 973 (2023), A44,
  DOI [10.1017/jfm.2023.748](https://doi.org/10.1017/jfm.2023.748).

### 2.4 Mollified trajectories and skewed cylinders

Yang constructs maximal functions on cylinders following trajectories of
a mollified incompressible flow and applies them to Navier--Stokes
estimates.  Thus mollified-flow trajectories and their moving geometry
are established.  The source does not contain the particular odd-symmetry
cancellation, packet bridge estimate, or frozen endpoint lower bound of
R0.74F.

- Jincheng Yang,
  [Construction of maximal functions associated with skewed cylinders generated by incompressible flows and applications](https://ems.press/journals/aihpc/articles/4938796),
  *Annales de l'Institut Henri Poincaré C, Analyse non linéaire* 39
  (2022), 793--818,
  DOI [10.4171/AIHPC/20](https://doi.org/10.4171/AIHPC/20).

---

## 3. Collision matrix

| Source class | Established overlap | Material difference from R0.74F | Classification |
|---|---|---|---|
| Kac; Güneysu | stochastic representations, pinned paths, heat kernels | no paired torus packet, explicit winding sum, or annular endpoint | background tool |
| 2D3C literature | third component as a passive scalar | no zero-mollified-frame paired-packet theorem | structural prior art |
| compact-flow mixing | incompressible advection can enhance diffusion | decay/spectral criteria, not the terminal survival lower bound | neighboring theory |
| parallel-shear dispersion | quantitative shear decay and Taylor dispersion | different observables and asymptotic target | close neighboring theory |
| exact laminar-shear scalar solutions | analytical treatment of localized tracers | spectral solution method, not the R0.74F packet/bridge construction | closest located construction class |
| mollified skewed cylinders | trajectories generated by mollified flows | maximal-function geometry, not matched cancellation or packet survival | geometric prior art |

No source in this matrix was found to state the seven-part combination in
Section 1 or to imply the precise R0.74F endpoint lower bound without new
arguments.  This sentence reports the bounded search outcome only; it is
not a universal nonexistence or priority statement.

---

## 4. Search protocol and stopping rule

The search used primary-source pages, journal repositories, DOI records,
and arXiv for query families built from:

- `2D3C Navier--Stokes passive scalar exact solution shear`;
- `mollified trajectory local frame Navier--Stokes`;
- `Brownian bridge periodic heat kernel torus winding`;
- `derivative heat kernel packet passive scalar shear`;
- `paired heat-kernel packets Navier--Stokes shear flow`;
- `outer annulus mollified flow Navier--Stokes`;
- `odd passive scalar periodic shear Brownian bridge`; and
- combinations of `terminal lobe`, `all winding`, and `moving packet`.

The search stopped when the results repeatedly returned the same five
neighboring classes in Section 3, and additional exact-phrase variations
produced no source addressing the combined claim.  Eight primary sources
were retained because together they cover every inherited primitive and
the closest exact-shear comparison located.  Citation-chain exhaustion,
MathSciNet/zbMATH classification searches, author correspondence, and a
referee-level priority audit remain outside this bounded pass.

One 2026 repository preprint was also surfaced by broad packet/closure
queries: Jeremy Rodgers,
[Closure and Regularity in Partial Differential Equations I](https://doi.org/10.5281/zenodo.18371918).
It assumes a strict high-frequency margin and derives a conditional
frequency-shell contraction with Fejér packets.  It was not used as
support: it is not peer reviewed in the located record, does not establish
its margin, and does not match the physical-space Brownian-bridge
construction here.

---

## 5. Publication boundary

The safe literature statement for R0.74F is:

> The proof uses classical 2D3C passive-scalar structure,
> Feynman--Kac/Brownian-bridge methods, periodic heat kernels, shear-flow
> dispersion, and mollified-flow trajectories.  In a bounded targeted
> search, no primary source was located that states the same explicit
> paired-packet, zero-mollified-frame, all-winding annular-survival lower
> bound.  No priority claim is made.

Any stronger wording such as “first”, “new”, “unprecedented”, or “solves a
known open problem” is unsupported by this audit and must not appear in the
research note or public release.
