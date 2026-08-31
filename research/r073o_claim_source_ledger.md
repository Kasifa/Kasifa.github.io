# R0.73O claim--source ledger

**Status:** bounded source reconciliation, finite validation, and final
independent analytic readback complete

| Claim ID | Claim | Source or derivation | Support class | Exact boundary |
|---|---|---|---|---|
| D1 | FPS \((X,Z)\) uses \(X\) for solution membership and \(Z\) for input smallness and observed distance | [FPS Definition 2.1](https://arxiv.org/abs/math/0508173) | external definition | fixed smooth equilibrium |
| D2 | Right-half-plane \(L^p\) spectrum implies \((L^q,L^p)\) nonlinear instability for \(q>\max\{p,n\}\) | FPS Theorem 2.2 | external theorem | autonomous forced equilibrium |
| D3 | On a finite domain the unstable initial direction may be small in smooth norms while output escape is in \(L^p\) | FPS finite-domain remark after Theorem 2.2 | external theorem detail | existence of a smooth unstable eigenfunction |
| LS1 | Strong stability of mildly decaying large global solutions is classical | [Ponce--Racke--Sideris--Titi 1994](https://doi.org/10.1007/BF02102642) | external theorem | \(H^1\)-type topology; printed domain setting differs |
| LS2 | Global-data sets are open and global critical solutions decay in the whole-space theory | [Gallagher--Iftimie--Planchon](https://doi.org/10.5802/aif.1983) | external theorem | \(\mathbb R^3\), critical spaces |
| LS3 | Strong and weak stability of global data in critical spaces are distinct | [Bahouri--Chemin--Gallagher](https://doi.org/10.5802/jep.84) | external theorem/context | \(\mathbb R^3\), not periodic \(H^3\) |
| LS4 | Large periodic global solutions under nonlinear smallness are known | [Chemin--Gallagher](https://arxiv.org/abs/math/0508374) | external theorem | special data condition; not arbitrary global orbit |
| LS4a | Smooth global decaying torus solutions have explicit \(H^n\) stability radii and exponential difference bounds | [Pizzocchero 2021](https://doi.org/10.1016/j.aml.2020.106970) | closest direct external theorem | stated for \(H^\infty\) data; \(n=3\) is allowed in \(d=3\) |
| LS4b | Every mean-zero periodic Leray--Hopf solution is eventually Gevrey regular and exponentially decaying | [Hoang--Martinez, Thm. 2.4](https://arxiv.org/abs/1511.03523) | external asymptotic theorem | potential force vanishes after Leray projection |
| LS4c | A periodic base in \(L^2_tW^{3,\infty}_x\) has an exponentially stable \(H^3\) perturbation tube | [Enciso--Lucà--Peralta-Salas, Thm. 3.1](https://arxiv.org/abs/1606.06176) | external robustness theorem | stronger base integrability hypothesis |
| LS5 | Mucha 2001 studies \(L^2\)-small perturbations of regular torus solutions | [Mucha 2001](https://doi.org/10.1006/jdeq.2000.3863) | publisher abstract / closest collision | exact threshold dependence not read from full theorem |
| LS6 | In the accessible Mucha theorem, \(L^2\) smallness is relative to a Besov trace norm | [Mucha 2008, Thm. 1.2](https://doi.org/10.4064/bc81-0-18) | external theorem | rules out interpreting the method as a uniform \(L^2\)-only threshold |
| K1 | The Kolmogorov linearized eigenproblem is (3.4), and nonnegative-real-part eigenvalues are real | [Meshalkin--Sinai](https://doi.org/10.1016/0021-8928%2862%2990149-1), [Nagatou](https://doi.org/10.1016/j.cam.2003.10.016) | external spectral theorem | two-dimensional rectangular torus |
| K2 | At \(\alpha=0.7\), \(R_c\in[3.011528364444,3.011528364446]\) | Nagatou; later exact restatement in [Watanabe et al.](https://doi.org/10.1016/j.cam.2016.01.055) | computer-assisted theorem | their nondimensionalization only |
| K3 | For \(0<\beta<1\), the zero-eigenvalue recurrence has a nonzero \(\ell^2\) solution only at the unique \(\lambda(\beta)\); for \(\beta\ge1\), none exists | [Matsuda--Miyatake 2002, Prop. 1](https://doi.org/10.2748/tmj/1113247600) | external theorem | neutral spectrum only |
| K4 | At a finite sufficiently large Reynolds parameter, the \(\alpha<1\) Kolmogorov linearization has positive real spectrum | [Ilyin 2005, Thm. 5.1](https://doi.org/10.1070/SM2005v196n01ABEH000871) | external theorem | supplies the high-parameter anchor, not the twelve-digit threshold |
| K5 | Positive spectrum propagates from the K4 anchor to every \(R>R_c\) | common-domain type-(A) family, compact resolvent, uniform right-half-plane spectral rectangle, Riesz projection rank + K1 + K3 | audited internal operator-theoretic inference from external results | continuation preserves total algebraic multiplicity; it does not prove algebraic simplicity |
| O1 | Every a priori global mean-zero unforced periodic \(H^3\) orbit eventually enters a small \(H^1\) ball | energy equality + internal ladder proof | audited internal continuum theorem | assumes global strong reference orbit |
| O2 | Every such orbit satisfies \(\int_0^\infty\|u(t)\|_{H^4}dt<\infty\) | O1 + weighted \(H^3\) energy | audited internal continuum theorem | equivalent norms; finite initial interval uses \(L^2_{loc}H^4\) |
| O3 | Every such orbit has one positive \(H^3\) radius valid for all start times, with exponential synchronization | perturbation energy, O2, bootstrap, continuation | audited internal continuum theorem | input and main output are both \(H^3\) |
| O4 | The global-data set \(\mathcal G_3\) is \(H^3\)-open | O3 at \(t_0=0\) | internal corollary | conditional openness, not all-data globality |
| O5 | O3 gives an \(H^3\)-input/\(L^2\)-output corollary | \(H^3\hookrightarrow L^2\) | internal corollary | not uniform \(L^2\)-input FPS stability |
| F1 | \(U_*=(30.12\sin10y,0,0)\), \(f_*=(3012\sin10y,0,0)\) is an exact forced steady solution with infinite accumulated strain | direct differentiation | internal exact calculation | forced equation |
| F2 | \(m=7,N=10,A=30.12,\nu=1\) maps exactly to \(\alpha=0.7,R=3.012\) in K1 | direct vorticity linearization and scaling | internal exact calculation | planar invariant subspace |
| F3 | The full 3D linearized operator has a positive smooth planar eigenfunction | K1--K5 + F2 + constant-in-\(z\) embedding | composite hybrid theorem chain | at least one positive real planar eigenvalue; not an essentially 3D mode |
| F4 | There are \(H^3\)-small perturbations with fixed \(L^2\) escape | apply D1--D3 first on the 2D invariant torus, then extend constantly in \(z\) | hybrid theorem chain | one planar sequence suffices for full-phase-space instability |
| F5 | Every witness solution in F4 is global and smooth | planar invariance + classical 2D global regularity | external classical theorem + exact invariance | does not say nearby nonplanar solutions are global |
| A1 | No checked exact theorem statement gives a uniform global threshold for arbitrary regular data small only in \(L^2\) | bounded audit + LS5--LS6 | bounded-search absence | not exhaustive; Mucha 2001 full text remains access caveat |
| X1 | Arbitrary-data 3D global regularity | none | **OPEN** | Clay problem unchanged |
| X2 | Uniform full FPS \((H^3,L^2)\) stability over arbitrarily large \(H^3\) perturbations | none in checked exact statements | **OPEN / COLLISION-SENSITIVE** | do not claim absence beyond bounded audit |
| X3 | An essentially 3D unstable eigenmode for \(U_*\) | none | OPEN / NOT NEEDED | witness eigenmode is planar |
| X4 | Blow-up, turbulence, anomalous dissipation, or nonuniqueness in the forced example | none | EXCLUDED | all witness solutions are smooth |

## Publication invariants

~~~text
unforcedGlobalOrbitH3Stability=CLOSED_CONDITIONALLY_AFTER_AUDIT
unforcedFiniteAccumulatedH4=CLOSED_CONDITIONALLY_AFTER_AUDIT
globalDataSetH3Open=STANDARD_H3_EXTENSION_OF_DIRECT_SMOOTH_PERIODIC_THEOREM
uniformL2OnlyInputThreshold=OPEN_COLLISION_SENSITIVE
forcedKolmogorovH3InputL2Escape=CLOSED_BY_COMPOSITE_PRIMARY_SOURCE_CHAIN_AFTER_AUDIT
forcedWitnessSolutionsGlobalSmooth=PLANAR_ONLY
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
~~~
