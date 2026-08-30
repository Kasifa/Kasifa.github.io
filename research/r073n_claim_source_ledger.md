# R0.73N claim--source ledger

**Status:** bounded primary-source and internal claim-boundary reconciliation,
plus independent analytic, adversarial, symmetry, and compactness audits
PASS; finite and publication gates remain separate

| Claim ID | Public or analytic claim | Primary support | Support class | Boundary |
|---|---|---|---|---|
| D1 | FPS \((X,Z)\) uses \(X\) for solution regularity and \(Z\) for both initial smallness and observed distance | [FPS Definition 2.1](https://arxiv.org/html/math/0508173v1) | external definition | stated for a fixed smooth equilibrium |
| D2 | loss of the required global \(X\)-solution is one branch of FPS instability | [FPS Definition 2.1 and following remark](https://arxiv.org/html/math/0508173v1) | external definition | fixed-distance escape is not the whole negation |
| D3 | R0.73N uses synchronized comparison with one trajectory at fixed initial time \(t_0=0\) | explicit R0.73N definition | internal definition | adaptation of the FPS quantifier pattern; not an FPS theorem |
| LS1 | right-half-plane spectrum can imply nonlinear instability of one steady Navier--Stokes equilibrium | [Friedlander--Pavlović--Shvydkoy](https://doi.org/10.1007/s00220-006-1526-7) | external theorem | fixed steady generator and fixed forcing; no non-autonomous trajectory |
| LS2 | high-order instability schemes exist for singularly parameterized approximate-solution or boundary-layer families | [Grenier 2000](https://doi.org/10.1002/1097-0312%28200009%2953%3A9%3C1067%3A%3AAID-CPA1%3E3.0.CO%3B2-Q), [Desjardins--Grenier 2003](https://doi.org/10.1016/S0294-1449%2802%2900009-4), [Grenier--Nguyen 2019](https://doi.org/10.1007/s40818-019-0074-3) | external method/theorem | parameter family, boundary, and possible forcing mismatches |
| LS3 | small-viscosity Couette dynamics can exhibit transient exponential amplification and a sharp threshold | [Li--Masmoudi--Zhao](https://doi.org/10.1002/cpa.22183) | neighboring nonlinear theorem | \(\nu\)-dependent family certificate; not fixed-\(\nu\) Lyapunov instability |
| LS4 | spectrally stable linearized shear dynamics can have large finite transient gain | [Trefethen et al.](https://doi.org/10.1126/science.261.5121.578) | terminology and linear precedent | not a nonlinear fixed-orbit theorem |
| LS5 | full-path assumptions can yield nonlinear stability of exact heat-evolving monotone shears | [Li--Zhao](https://arxiv.org/abs/2306.03555) | stable-side neighboring theorem | monotone geometry and full-path Rayleigh hypotheses differ |
| LS6 | a heat-evolving boundary-free shear can undergo a frozen Rayleigh spectral transition | [Li--Zhao](https://arxiv.org/abs/2410.23798) | neighboring spectral theorem | exact-unforced nonlinear trajectory transfer is not closed there |
| LS7 | periodic decaying Kolmogorov flows can be metastable at a viscosity-dependent perturbation scale | [Lin--Xu](https://doi.org/10.1007/s00205-018-1311-8) | stable-side conflict check | does not prove the explicit R0.73N radius |
| LS8 | fixed steady Couette and Kolmogorov flows are classical spectral/stability benchmarks | [Romanov](https://doi.org/10.1007/BF01078886), [Meshalkin--Sinai](https://doi.org/10.1016/0021-8928%2862%2990149-1) | external benchmark | moving walls, forcing, or steady geometry differ from the unforced decaying orbit |
| LS9 | classical strong-solution theory supplies a local solution and continuation framework | [Fujita--Kato](https://doi.org/10.1007/BF00276188) | external background | not support for the theorem-specific finite-strain tube |
| N1 | every coexisting perturbation satisfies the explicit relative \(L^2\) bound on its common strong lifespan | R0.73N Section 2 direct integration by parts | internal continuum theorem | does not by itself prove global three-dimensional continuation |
| N2 | every fixed \(\Lambda\) has a positive full-three-dimensional \(H^3\) stability tube | R0.73N Sections 2--4 energy, commutator, bootstrap, and continuation | internal continuum theorem | FPS-style \((H^3,H^3)\); radius is nonuniform in \(\Lambda\) |
| N3 | \(H^3\)-small full-three-dimensional input gives uniformly \(L^2\)-small synchronized output | N2 plus \(H^3\hookrightarrow L^2\) | internal corollary | custom \(H^3\)-in/\(L^2\)-out statement, not FPS \((H^3,L^2)\) notation |
| N4 | the planar subsystem is FPS-style \((H^3_{\mathrm{pl}},L^2_{\mathrm{pl}})\) stable | N1, planar invariance, and two-dimensional global regularity | internal continuum theorem | planar data only |
| N5 | R0.73M gives exponentially growing pointed amplification and family non-equicontinuity | sealed R0.73M lower theorem plus R0.73N upper bound | internal continuum theorem | varying unbounded backgrounds; one autonomous flow map evaluated at different basepoints |
| N6 | R0.73M cannot be converted by quantifier exchange into fixed-member \(H^3\)-small, \(L^2\)-fixed-distance escape | R0.73M quantifiers plus N2--N4 | internal logical consequence | route- and topology-specific |
| N7 | no registered exact symmetry, time shift, compactness limit, or smooth infinite-block shortcut identifies the family with one fixed trajectory | direct R0.73N transformation and Fourier/Sobolev audit | internal obstruction theorem | only the explicitly audited transfer candidates |
| A1 | no checked source supplies a black-box theorem for N1--N7 jointly | bounded two-wave audit recorded in r073n_literature_audit.md | bounded-search absence | not exhaustive and not an absolute novelty or priority claim |
| O1 | full-three-dimensional FPS \((H^3,L^2)\) stability | none | **OPEN** | would require global \(H^3\) control for data small only in \(L^2\) |
| O2 | optimal fixed-member stability radius | none | OPEN | the explicit bootstrap radius is sufficient, not sharp |
| O3 | sharp pointed amplification exponent | none | OPEN | current lower and upper exponential rates differ |
| O4 | fixed-trajectory instability for a different nondecaying or infinite-strain background | none | OPEN | R0.73N is family-specific |
| O5 | a different transfer mechanism outside the registered symmetry and compactness candidates | none | OPEN | N7 closes only the explicitly audited routes |
| O6 | transverse critical-norm growth, finite-time singularity, or the Clay conclusion | none | OPEN | excluded from the present theorem |

## Publication rule

Every definition sentence using FPS pair notation must resolve to D1--D2.
The trajectory adaptation must resolve to D3 and be labeled synchronized
forward stability at \(t_0=0\).  Every external positioning sentence must
resolve to LS1--LS9.  Every theorem-specific mathematical claim must resolve
to N1--N7 or be marked open.  A1 may support only a bounded non-collision
statement and must never support “first”, “new”, “unique”, exhaustive, or
priority language.

In particular:

~~~text
fullThreeDimensionalFPSH3L2Stability=OPEN
fixedMemberThreeDimensionalH3SynchronizedStability=CLOSED
fullThreeDimensionalH3InputL2Output=CLOSED_AS_COROLLARY
fixedMemberPlanarL2SynchronizedStability=CLOSED
~~~
