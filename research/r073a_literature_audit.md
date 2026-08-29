# R0.73A primary-literature audit: long waves, slow projections, and transient OS growth

**Search cutoff:** 2026-08-29

**Status:** source-stage.  This is a bounded primary-source search, not a
novelty or priority proof.

## 1. Search question

The search asked whether an existing theorem supplies all of the following
for the R0.72 heat path:

1. the active Orr--Sommerfeld inverse-Laplacian term;
2. the physical long-wave singularity \(\mu=\gamma^2\downarrow0\);
3. a time-dependent shear with changing critical-point type;
4. an explicit finite transient prefactor after a slow-mode projection;
5. all-start propagation and forcing;
6. three-dimensional Squire/lift-up transfer and a Bloch-uniform kinetic
   direct sum.

No checked source supplies that complete combination.  Several sources do,
however, determine the safe structure of R0.73A.

## 2. Consequential primary sources

### 2.1 Colombo--Dolce--Montalto--Ventura: the physical long-wave mode

**Source:** Maria Colombo, Michele Dolce, Riccardo Montalto, and Paolo
Ventura, [*Long-wave instability of periodic shear flows for the 2D
Navier--Stokes equations*](https://arxiv.org/html/2509.18070v2),
arXiv:2509.18070v2 (2025).

**Checked content:** Theorem 1.1 and Theorem 2.1 isolate a simple long-wave
eigenvalue.  In their normalized \(L^2(\mathbb T)\) convention,

\[
 \lambda_{\nu,\varepsilon}^{(0)}
 =\frac{\varepsilon^2}{\nu}
 \left(\|\partial_y^{-1}U\|_2^2-\nu^2
 +O\big(\varepsilon(\nu+\nu^{-1})\big)\right),
\]

and the eigenvector is close to \(U-i\nu\varepsilon\).  Lemma 2.2 proves
the exact zero-mode cancellation
\(\Pi_0\mathcal R_\varepsilon=O(\varepsilon^2)\).  The Kato and normal-form
constructions isolate the simple direction and a stable complementary
hyperplane, but the conjugating map can be far from the identity.

**Supports:** the singular physical slow coordinate contains a small
constant component; the correct cancellation is a zero-mode identity, not
an orthogonal projection onto the abstract tangent \(W_{xx}\); frozen weak
streamwise rows can be unstable.

**Does not support:** the profile is stationary and externally maintained.
The result is spectral; it does not give the nonautonomous R0.73A
propagator or a three-dimensional Squire estimate.

### 2.2 Chen--Dai--Wang--Wang: parameter-uniform Riesz projections

**Source:** Robin Ming Chen, Tian Dai, Dehua Wang, and Weiqiang Wang,
[*Long-Wave Stability And Instability Of Periodic Shear Flows For The 2D
Navier--Stokes Equations On The beta-Plane*](https://arxiv.org/html/2608.06899v1),
arXiv:2608.06899v1 (2026).

**Checked content:** the paper extends the long-wave Kato reduction to a
rotation parameter.  It tracks parameter-dependent resolvent contours and
Riesz projections uniformly and derives a second-order principal-eigenvalue
expansion.  The symbol \(\beta\) in this paper is a Coriolis parameter; it is
not the Bloch residue \(\beta\) used in R0.72Y--Z.

**Supports:** slow-mode projection must be built with a parameter-uniform
resolvent or an exact algebraic substitute; pointwise closeness of
projections is not automatic in a singular long-wave problem.

**Does not support:** the flow is stationary, two-dimensional, forced, and
on the beta-plane.  Its stabilizing rotation mechanism is absent from the
present equation.

### 2.3 Li--Zhao: all-start nonautonomous propagator under spectral stability

**Source:** Hui Li and Weiren Zhao, [*Asymptotic stability in the critical
space of 2D monotone shear flow in the viscous
fluid*](https://arxiv.org/html/2306.03555v1), arXiv:2306.03555 (2023),
Communications in Mathematical Physics 405 (2024), 267.

**Checked content:** Assumption 1.1 requires strict monotonicity and absence
of Rayleigh eigenvalues or embedded eigenvalues at every time.  Proposition
3.1 gives an all-start solution operator \(S(t,s)\) with an explicit
enhanced-dissipation exponential and spacetime estimates.  A time-dependent
wave operator absorbs the nonlocal Rayleigh term.

**Supports:** an all-start two-parameter propagator, rather than a single
initial-time estimate, is the correct nonautonomous object.

**Does not support:** the domain is \(\mathbb T\times\mathbb R\), the shear
is strictly monotone for all time, and the theorem assumes spectral
stability.  The two-harmonic periodic collision path satisfies none of those
geometric hypotheses.

### 2.4 Li--Zhao: heat evolution can cross a spectral boundary

**Source:** Hui Li and Weiren Zhao, [*Viscosity driven instability of shear
flows without boundaries*](https://arxiv.org/abs/2410.23798),
arXiv:2410.23798 (2024).

**Checked content:** the authors construct a shear that is spectrally stable
initially but becomes spectrally unstable under heat evolution.

**Supports:** initial-time spectral stability cannot be silently propagated
along a heat path.

**Does not support:** it does not decide the exact R0.72 two-harmonic path or
provide its transient prefactor.

### 2.5 Li--Ren--Wang--Zhang: neutral modes and nonnormal growth

**Source:** Hui Li, Siqi Ren, Yuxi Wang, and Guoqing Zhang,
[*Instability of shear flows with neutral embedded
eigenvalues*](https://arxiv.org/abs/2602.07807), arXiv:2602.07807 (2026).

**Checked content:** neutral embedded eigenvalues can generate arbitrarily
large \(L^2\) and \(L^\infty\) growth; multiple embedded eigenvalues can
produce linear-in-time growth through nonnormality.

**Supports:** a frozen spectrum in the closed left half-plane is not enough
to infer a small transient prefactor.

**Does not support:** the result concerns an inviscid monotone class and
does not identify the hidden physical mean coordinate in R0.73A.

### 2.6 Li--Wei--Zhang: pseudospectrum-to-semigroup payment

**Source:** Te Li, Dongyi Wei, and Zhifei Zhang,
[*Pseudospectral bound and transition threshold for the 3D Kolmogorov
flow*](https://arxiv.org/html/1801.05645v1), arXiv:1801.05645 (2018),
Communications on Pure and Applied Mathematics 73 (2020).

**Checked content:** Section 4 converts a pseudospectral bound into a
semigroup estimate through a Gearhart--Pruss type lemma with an explicit
prefactor.  The paper treats the full three-dimensional Kolmogorov
linearization and structured nonlocal terms.

**Supports:** resolvent control can legitimately produce a transient
prefactor; three-dimensional OS--Squire payments are structural.

**Does not support:** the base flow is stationary and single-harmonic, and
the streamwise mode is discrete and nonzero.  There is no heat collision or
continuous Bloch residue.

### 2.7 Reddy--Schmid--Henningson: spectrum alone misses transient growth

**Source:** Satish C. Reddy, Peter J. Schmid, and Dan S. Henningson,
[*Pseudospectra of the Orr--Sommerfeld
Operator*](https://doi.org/10.1137/0153002), SIAM Journal on Applied
Mathematics 53 (1993), 15--47.

**Checked content:** the paper computes the OS pseudospectrum and numerical
range for plane Poiseuille flow and relates near-linear dependence of
eigenfunctions to transient amplification even when every eigenmode decays.

**Supports:** the R0.73A numerical audit must record singular values or
propagator norms, not only eigenvalues.

**Does not support:** the geometry, boundary conditions, norm, and
stationarity differ; numerical pseudospectra are not an infinite-dimensional
proof for the present operator.

### 2.8 Beekie--Chen--Jia: rigorous periodic nonmonotone OS control

**Source:** Rajendra Beekie, Shan Chen, and Hao Jia,
[*Uniform vorticity depletion and inviscid damping for periodic shear flows
in the high Reynolds number regime*](https://arxiv.org/abs/2403.13104),
arXiv:2403.13104v2 (2024), Archive for Rational Mechanics and Analysis 250
(2026), Article 7.

**Checked content:** the full periodic Orr--Sommerfeld problem is controlled
under exactly two fixed nondegenerate critical points and a no-discrete-
spectrum hypothesis, with separate critical-layer regimes.

**Supports:** active pressure feedback can be handled rigorously in periodic
nonmonotone geometry.

**Does not support:** the critical points remain fixed in number and type;
the theorem is not uniform through the R0.72 collision.

### 2.9 Wei--Zhang--Zhao: active heat-decaying Kolmogorov geometry

**Source:** Dongyi Wei, Zhifei Zhang, and Weiren Zhao,
[*Linear inviscid damping and enhanced dissipation for the Kolmogorov
flow*](https://arxiv.org/abs/1711.01822), arXiv:1711.01822 (2017),
Advances in Mathematics 362 (2020), 106963.

**Checked content:** a wave-operator method controls the active nonlocal term
for the Kolmogorov flow, including its heat-decaying amplitude.

**Supports:** nonautonomous active OS structure is tractable in special
geometry.

**Does not support:** a single sine has fixed critical-point type and no
long-wave zero-mode collision of the present two-harmonic path.

### 2.10 Coble--He: time-dependent scalar estimates require critical geometry

**Source:** Daniel Coble and Siming He, [*A Note on Enhanced Dissipation and
Taylor Dispersion of Time-dependent Shear
Flows*](https://arxiv.org/html/2309.15738v2), arXiv:2309.15738v2 (2023).

**Checked content:** the sharp passive-scalar theorem assumes a fixed finite
set of nondegenerate critical points shared with a reference shear and
controls their time variation.  The authors explicitly note that rapid
critical-point motion can mix and unmix.

**Supports:** changing critical geometry is a real nonautonomous boundary,
even before OS pressure feedback is added.

**Does not support:** the equation is passive scalar; it has no
inverse-Laplacian pressure term or physical long-wave mean variable.

### 2.11 Ibrahim--Maekawa--Masmoudi: projected Kolmogorov semigroup

**Source:** Slim Ibrahim, Yasunori Maekawa, and Nader Masmoudi,
[*On pseudospectral bound for non-selfadjoint operators and its application
to stability of Kolmogorov flows*](https://arxiv.org/abs/1710.05132),
arXiv:1710.05132v2 (2019), Annals of PDE 5 (2019), Article 14.

**Checked content:** the paper proves resolvent and semigroup bounds for a
stationary Kolmogorov linearization after separating exceptional finite
dimensional modes.  The estimates explicitly distinguish fast projected
decay from slower leakage toward the exceptional subspace.

**Supports:** a valid projected theorem must ledger both the complement
semigroup and slow-mode leakage; “remove one mode, then contract” is not an
automatic consequence of spectral stability.

**Does not support:** the operator is stationary, single-sine,
two-dimensional, and indexed by nonzero discrete Fourier modes.

### 2.12 Ren--Zhang: an eigenprojection may leave a rank-one slow term

**Source:** Siqi Ren and Zhifei Zhang, [*Linear inviscid damping in the
presence of an embedding eigenvalue*](https://arxiv.org/abs/2402.18229),
arXiv:2402.18229 (2024), Communications in Mathematical Physics 406 (2025),
Paper 39.

**Checked content:** for the first mode of the hyperbolic-tangent Rayleigh
operator, the evolution separates into a nondecaying eigenspace, a slow
rank-one term caused by a resolvent singularity, and a faster inviscid-
damping remainder.

**Supports:** R0.73A must allow a transported finite-rank corrector in
addition to the obvious tangent projection if the low-gap resolvent has a
threshold singularity.

**Does not support:** the problem is inviscid, stationary, monotone, and on
the whole line; it gives no viscous nonautonomous OS propagator here.

### 2.13 Wei: a sharp abstract resolvent-to-semigroup prefactor

**Source:** Dongyi Wei, [*Diffusion and mixing in fluid flow via the
resolvent estimate*](https://arxiv.org/abs/1811.11904), arXiv:1811.11904
(2018), Science China Mathematics 63 (2020).

**Checked content:** the paper proves a Gearhart--Pruss type estimate with a
sharp explicit prefactor for m-accretive operators and applies it to mixing
and diffusion.

**Supports:** once a projected frozen operator is proved m-accretive with a
quantitative pseudospectral floor, an explicit prefactor is legitimate.

**Does not support:** the theorem is autonomous and does not control
time-dependent projections, their derivatives, or a long-wave Jordan block.

### 2.14 Beck--Wayne: nonautonomous invariant subspaces, with a warning

**Source:** Margaret Beck and C. Eugene Wayne, [*Metastability and rapid
convergence to quasi-stationary bar states for the 2D Navier--Stokes
Equations*](https://arxiv.org/abs/1108.3416), arXiv:1108.3416v3 (2012),
Proceedings of the Royal Society of Edinburgh A 143 (2013).

**Checked content:** linearization around heat-decaying bar states produces
a nonautonomous operator.  The analytic rapid-decay theorem is proved for a
model obtained by dropping a higher-order nonlocal term; the full operator
is supported numerically.

**Supports:** an invariant or transported slow subspace is more natural than
independent frozen projections in a nonautonomous problem.

**Does not support:** the primary positive theorem omits precisely the
nonlocal term that is active in the present OS equation, so it cannot be
quoted as a complete-OS precedent.

## 3. Claim-to-source ledger

| R0.73A statement | Supporting primary source | Exact limit of support |
|---|---|---|
| zero-mode cancellation is the relevant long-wave structure | Colombo et al., Lemma 2.2 | stationary 2D operator |
| frozen low waves may be unstable | Colombo et al., Theorem 1.1 | stationary forced shear |
| Riesz contours need uniform parameter control | Chen et al., Secs. 3--4 | rotation parameter, not Bloch residue |
| all-start propagation is possible under strong hypotheses | Li--Zhao, Proposition 3.1 | monotone and spectrally stable at every time |
| heat evolution need not preserve stability | Li--Zhao 2024 | constructed profile, not this exact path |
| spectrum alone does not bound transient growth | Reddy et al.; Li et al. 2026 | different geometries |
| pseudospectrum can yield an explicit semigroup prefactor | Li--Wei--Zhang, Sec. 4 | stationary Kolmogorov geometry |
| active periodic OS estimates exist | Beekie--Chen--Jia | fixed critical type and spectral assumptions |
| time-dependent active special geometry exists | Wei--Zhang--Zhao | single harmonic |
| scalar time dependence is geometry-sensitive | Coble--He | passive scalar only |
| projected fast decay needs a slow-leakage ledger | Ibrahim--Maekawa--Masmoudi | stationary single-sine flow |
| one eigenprojection may leave a finite-rank slow term | Ren--Zhang | inviscid embedded-eigenvalue setting |
| resolvent floors can yield explicit autonomous prefactors | Wei | no time-dependent projection |
| transported invariant subspaces are natural in heat-decaying flows | Beck--Wayne | rigorous theorem drops the nonlocal term |

## 4. Search decision

- `existingPhysicalLongWaveZeroModeCancellation`: **SUPPORTED**.
- `existingStationaryLongWaveSpectralProjection`: **SUPPORTED**.
- `existingAllStartNonautonomousActiveOSPropagatorUnderStableMonotoneGeometry`:
  **SUPPORTED**.
- `existingNonautonomousTwoHarmonicCollisionProjectionWithExplicitTransientPrefactor`:
  **NOT FOUND IN THIS SEARCH**.
- `existingThreeDimensionalBlochUniformKineticDirectSumThroughTheCollision`:
  **NOT FOUND IN THIS SEARCH**.
- `frozenLowWaveRowsAutomaticallyStable`: **CONTRADICTED AS A GENERAL
  PRINCIPLE**.

The safe R0.73A route is therefore to prove the exact physical mean
cancellation and a scoped nonautonomous transient bound, while keeping the
frozen long-wave instability and the full kinetic/Squire gaps visible.
