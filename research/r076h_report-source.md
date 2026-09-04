# R0.76H bounded source and dependency report

## Report frame

- Date: 2026-09-04.
- Question: which claims in R0.76H are imported, which are proved locally,
  and what established literature bounds the interpretation?
- Scope: the explicit R0.76G packet, the frozen physical plateau geometry,
  and the complete-clock signed collar flux.
- Exclusions: exhaustive priority research, arbitrary packets, nonlinear
  non-shear dynamics, Version-M extraction, and the Clay problem.

## Direct answer

R0.76H imports no external observability, Remez, or control theorem.  The
new implication is local to the frozen packet and follows from the exact
Gaussian representation, the elementary even-moment expansion, Hölder,
Jensen, and the exact shell cross-section.  The finite certificate can
audit constants, powers, tags, hashes, and boundary statements; it cannot
replace the limiting moment argument.

The bounded literature search already frozen for R0.76G remains the
appropriate context.  General heat observability and exponential-polynomial
propagation results explain why exponential costs can occur, but they do not
state either H.5 or the exact normalized rate H.7.  Reusing those sources
does not turn this packet-specific proof into a general theorem.

## Frozen local dependencies

| dependency | SHA-256 | role |
|---|---|---|
| R0.76G complete-clock central-fibre lower bound | 20f32790b53f2b0f5cb39b7071bd2cda96ddb4e15f75211e1682f4ba37dd0bb2 | Exact packet, drift, clock, cap sign, Gaussian representation, and adverse-cap estimate. |
| R0.75P buffered collar entrance concentration | 8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6 | Frozen physical plateau and shell geometry. |
| R0.75R outer-cap spectral concentration obstruction | e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3 | Positive transition subcap constants. |
| R0.76E linear modal entropy window | 1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4 | Uniform arbitrary-packet upper boundary that H does not improve. |

These hashes bind the exact local objects used by the proof.  R0.76H does
not alter their claims.

## Established external context retained from R0.76G

- G. Wang, M. Wang, C. Zhang, and Y. Zhang, *Observable set,
  observability, interpolation inequality and spectral inequality for the
  heat equation in R^n*, arXiv:1711.04279.
- M. Egidi and I. Veselic, *Sharp geometric condition for
  null-controllability of the heat equation in R^d and consistent estimates
  on the control cost*, arXiv:1711.06088.
- L. Miller, *Geometric bounds on the growth rate of
  null-controllability cost for the heat equation in small time*,
  arXiv:math/0307158, DOI 10.1016/j.jde.2004.05.007.
- C. Laurent and M. Leautaud, *Observability of the heat equation,
  geometric constants in control theory, and a conjecture of Luc Miller*,
  arXiv:1806.00969, DOI 10.2140/apde.2021.14.355.
- F. L. Nazarov, *Local estimates for exponential polynomials and their
  applications to inequalities of the uncertainty principle type*,
  Algebra i Analiz 5:4 (1993), official record at mathnet.ru/eng/aa397.
- S. Tikhonov and P. Yuditskii, *Sharp Remez Inequality*,
  arXiv:1809.09726, DOI 10.1007/s00365-019-09473-2.

These papers are context only.  No theorem from them is invoked in
H.11--H.39.

## Claim-to-evidence ledger

| claim | evidence class | status |
|---|---|---|
| The shell cross-section and \(aR^5\) conversion are exact. | Local geometry calculation H.11--H.12. | **PROVED** |
| The cap is paid by an adjacent plateau strip for the explicit packet at cost \(\exp(O(m/a))\). | Local Gaussian-moment comparison H.13--H.27. | **PROVED** |
| The complete signed flux is eventually positive. | Terminal positive box plus full adverse-cap absorption H.35--H.37. | **PROVED** |
| The raw full-plateau quotient has exact rate \(3/40000\). | Two-sided analytic bounds H.34--H.39. | **PROVED** |
| The normalized full-plateau quotient has exact rate \(-2/11907\). | Exact scaling and the same two-sided bounds. | **PROVED** |
| The same subquadratic loss holds for arbitrary real dyadic packets. | No proof in H or in the cited sources. | **OPEN** |
| The uniform \(\exp(Cq)\) loss in R0.76E is removable. | No proof. | **OPEN** |
| Version-M extraction, regularity, or singularity follows. | No proof. | **OPEN** |

## Search and interpretation boundary

No fresh broad search was needed for H because its proof imports no new
external theorem and its contextual literature was already verified and
frozen in G.  The absence of an exact collision in that bounded search is
not evidence of novelty or priority.  The result is a rigorous
candidate-killing lemma for one explicit packet, not a general
Navier--Stokes regularity theorem.  **NOT CLAY.**
