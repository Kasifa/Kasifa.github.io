# R0.70M bounded primary-literature audit

**Audit date:** 2026-08-24

## 1. Question and stopping rule

The candidate under audit is

\[
 \dot Q=\Sigma Q+Q\Sigma+F_{\rm err},
 \qquad
 \dot G=\Sigma G,
 \qquad
 \widehat Q=G^{-1}QG^{-\mathsf T},
 \tag{1.1}
\]

which yields

\[
 \dot{\widehat Q}=G^{-1}F_{\rm err}G^{-\mathsf T}.
 \tag{1.2}
\]

The bounded search asked six questions:

1. Is (1.2) already used for a localized filtered-vorticity covariance?
2. Is \(G\) a standard physical deformation gradient?
3. Can positivity and \(\det G=1\) control congruence amplification?
4. Do known strain or vorticity criteria make the required history estimate
   circular for the regularity problem?
5. Does affine-invariant SPD geometry remove the condition number, and on
   what domain?
6. Do exact filtered/SGS papers supply a sign or coercive lower-frame bound?

The core fluid/PDE audit stopped at twelve high-signal primary sources; three
primary matrix-geometry sources were additionally checked. Together they cover
the physical flow map, viscous Eulerian--Lagrangian formulations, critical
continuation criteria, recent-fluid-deformation closures, affine SPD geometry,
and the exact filtered velocity-gradient ledger. A second targeted wave
returned refinements of the same classes but no
determinant-to-condition-number theorem or exact filtered residual pullback.
This is a bounded novelty audit, not a proof of nonexistence in the full
literature.

## 2. Direct answer

- The algebraic cancellation (1.2) is correct.
- No audited source contains the same combination of localized filtered
  covariance, strain-only continuous pullback, and normalized anisotropy.
- The auxiliary \(G\) is **not** the physical deformation gradient. A physical
  flow-map gradient solves \(\dot D=(\Sigma+W)D\), not \(\dot D=\Sigma D\).
- \(\det G=1\) gives no condition-number control.
- If the estimate ultimately assumes
  \(\int\|\Sigma\|_{\rm op}dt<\infty\), it has returned to a Ponce/BKM-level
  continuation hypothesis.
- Affine-invariant SPD geometry removes the congruence condition number only
  on \(Q\succ0\). The boundary \(\det Q=0\) lies at infinite affine distance
  and includes elementary smooth periodic NSE covariances.
- The potentially new part is therefore not “using deformation.” It is the
  sharp no-go/conditional estimate that decides whether the complete exact
  residual can be controlled before any Euclidean-frame conversion.

## 3. Claim--source--gap matrix

### 3.1 Chevillard, Meneveau, Biferale, and Toschi (2008)

- Source: [Lagrangian dynamics of velocity gradients in turbulence](https://arxiv.org/abs/0712.0900),
  [DOI 10.1063/1.3005832](https://doi.org/10.1063/1.3005832).
- Exact support: the physical flow-map gradient \(D\) satisfies
  \(\dot D=AD\), \(A=\nabla u=\Sigma+W\), and the associated tensor
  \(DD^{\mathsf T}\) obeys the full-gradient congruence equation.
- It cannot support: replacing \(A\) by \(\Sigma\), or controlling spectral
  distortion from \(\det D=1\).
- Collision/gap: it forces the naming correction. R0.70M's \(G\) is a
  strain-only propagator, not a physical deformation gradient.
- Confidence: high.

### 3.2 Constantin (2001), inviscid Eulerian--Lagrangian formulation

- Source: [arXiv:math/0004059](https://arxiv.org/abs/math/0004059),
  [DOI 10.1090/S0894-0347-00-00364-7](https://doi.org/10.1090/S0894-0347-00-00364-7).
- Exact support: the back-to-labels map is transported by the flow, its
  gradient has unit determinant, and the Cauchy formula uses the inverse
  physical flow-map gradient.
- It cannot support: the viscous NSE formula, or an energy-level bound on the
  inverse deformation gradient.
- Collision/gap: inverse-map multiplication is classical, but the generator
  is the full flow gradient rather than R0.70M's symmetric source.
- Confidence: high.

### 3.3 Constantin (2001), viscous Eulerian--Lagrangian formulation

- Source: [arXiv:math/0005116](https://arxiv.org/abs/math/0005116),
  [DOI 10.1007/s002200000349](https://doi.org/10.1007/s002200000349).
- Exact support: the viscous back-to-labels map solves a transport-diffusion
  equation and produces a nonzero Eulerian--Lagrangian commutator.
- It cannot support: treating viscosity as an ordinary deterministic
  deformation ODE with \(\det\nabla A=1\).
- Collision/gap: R0.70M is an auxiliary covariance ledger. It is not a
  viscous Cauchy formula.
- Confidence: high.

### 3.4 Constantin and Iyer (2008)

- Source: [arXiv:math/0511067](https://arxiv.org/abs/math/0511067),
  [DOI 10.1002/cpa.20192](https://doi.org/10.1002/cpa.20192).
- Exact support: the Navier--Stokes velocity admits a stochastic
  Lagrangian representation involving Brownian flow, inverse maps, Leray
  projection, and expectation.
- It cannot support: a single deterministic strain-only path, or commuting
  expectation through trace normalization.
- Collision/gap: a strict physical Lagrangian representation of viscosity
  naturally carries stochastic averaging absent from (1.1).
- Confidence: high.

### 3.5 Beale, Kato, and Majda (1984)

- Source: [DOI 10.1007/BF01212349](https://doi.org/10.1007/BF01212349).
- Exact support: an Euler solution can be continued while
  \(\int\|\omega\|_\infty dt\) stays finite; finite-time loss of smoothness
  forces divergence of that integral.
- It cannot support: an unconditional Navier--Stokes energy bound.
- Collision/gap: controlling a physical deformation gradient through maximum
  vorticity already uses continuation-level information.
- Confidence: high.

### 3.6 Ponce (1985)

- Source: [DOI 10.1007/BF01205787](https://doi.org/10.1007/BF01205787).
- Exact support: the maximum norm of the rate-of-strain tensor can replace
  vorticity in the BKM continuation mechanism.
- It cannot support: deriving the time-integrated maximum strain from the
  basic energy inequality.
- Collision/gap: the coarse estimate
  \(\kappa_2(G)\lesssim\exp(2\int\|\Sigma\|_{\rm op}dt)\) requires precisely
  the type of critical history already present in known criteria.
- Confidence: high.

### 3.7 Miller (2020)

- Source: [arXiv:1710.05569](https://arxiv.org/abs/1710.05569),
  [DOI 10.1007/s00205-019-01419-z](https://doi.org/10.1007/s00205-019-01419-z).
- Exact support: the strain equation and scale-critical criteria involving
  the positive part of the middle strain eigenvalue.
- It cannot support: an energy-level bound on that critical norm or on the
  condition number of \(G\).
- Collision/gap: a useful pullback theorem must be finer than directly
  assuming a critical strain criterion.
- Confidence: high.

### 3.8 Kozono, Ogawa, and Taniuchi (2003)

- Source: [official PDF](https://www.jstage.jst.go.jp/article/kyushujm/57/2/57_2_303/_pdf),
  [DOI 10.2206/kyushujm.57.303](https://doi.org/10.2206/kyushujm.57.303).
- Exact support: a critical Besov-vorticity time integral provides a
  continuation condition in their solution class.
- It cannot support: obtaining this integral from Leray energy or a
  strain-covariance pullback.
- Collision/gap: any successful adjacent-scale version should create a real
  Littlewood--Paley summation mechanism, not merely one determinant-one
  matrix at each scale.
- Confidence: high.

### 3.9 Phuc (2015)

- Source: [arXiv:1407.5129](https://arxiv.org/abs/1407.5129),
  [DOI 10.1007/s00021-015-0229-2](https://doi.org/10.1007/s00021-015-0229-2).
- Exact support: \(u\in L_t^\infty L_x^{3,q}\), \(q<\infty\), implies
  regularity and weak--strong uniqueness in the stated setting.
- It cannot support: the endpoint \(L^{3,\infty}\) or an implication from
  \(\widehat Q\) to this Lorentz norm.
- Collision/gap: a bridge from the pulled ledger to a known continuation
  space would itself be a major theorem; no such bridge is present.
- Confidence: high.

### 3.10 Gallagher, Koch, and Planchon (2016)

- Source: [arXiv:1407.4156](https://arxiv.org/abs/1407.4156),
  [DOI 10.1007/s00220-016-2593-z](https://doi.org/10.1007/s00220-016-2593-z).
- Exact support: finite-time singularity forces divergence of a family of
  critical Besov norms for the parameter range in the paper.
- It cannot support: endpoint cases or a Lagrangian deformation estimate.
- Collision/gap: a successful scale-coupled pullback should imply a known
  continuation quantity or establish a genuinely new one.
- Confidence: high.

### 3.11 Chevillard and Meneveau (2006)

- Source: [arXiv:cond-mat/0606267](https://arxiv.org/abs/cond-mat/0606267),
  [DOI 10.1103/PhysRevLett.97.174501](https://doi.org/10.1103/PhysRevLett.97.174501).
- Exact support: recent deformation is used to model the pressure Hessian and
  viscous terms in a stochastic velocity-gradient model.
- It cannot support: an exact PDE identity, pointwise coercivity, or a
  regularity proof. The construction includes closure assumptions.
- Collision/gap: deformation history is not itself novel. R0.70M must keep
  its exact covariance identity separate from RFD statistical regularization.
- Confidence: high.

### 3.12 Tom, Carbone, and Bragg (2021)

- Source: [arXiv:2005.04300](https://arxiv.org/abs/2005.04300),
  [DOI 10.1017/jfm.2020.960](https://doi.org/10.1017/jfm.2020.960).
- Exact support: the fixed-filter velocity-gradient equation, pressure
  Hessian, viscosity, and symmetric SGS double-gradient term.
- It cannot support: converting DNS-average SGS regularization into a
  pointwise sign, or omitting moving-cutoff terms.
- Collision/gap: R0.70M must retain the complete R0.70K cutoff,
  nonconstant-strain, diffusion, and SGS covariance residual.
- Confidence: high.

## 4. Matrix-geometry source boundary

Three primary matrix-geometry sources were additionally checked for the
affine-relative part of R0.70M:

- [Moakher (2005)](https://doi.org/10.1137/S0895479803436937),
- [Bhatia and Holbrook (2006)](https://doi.org/10.1016/j.laa.2005.08.025),
- [Pennec, Fillard, and Ayache (2006)](https://doi.org/10.1007/s11263-005-3222-z).

They support the affine-invariant metric, congruence invariance, geodesic
distance, completeness of the SPD cone, and the fact that null eigenvalues
are at infinite distance. They do not contain the localized NSE covariance
ledger or a uniform passage through rank loss. The metric is prior art; the
NSE placement and rank obstruction are the only candidate new elements.

## 5. Collision decision and remaining gap

There is no direct collision in the bounded corpus with the complete R0.70M
statement. There is strong conceptual prior art around physical deformation,
Cauchy formulas, RFD closures, and affine covariance geometry. The strongest
defensible novelty statement is therefore:

> Within the audited sources, the new part is the exact sharp
> \(\kappa_2(G)^2\) loss for the strain-only propagator covariance quotient, the
> zero-signed-integral noncommutative holonomy certificate, and the explicit
> rank obstruction to using an affine-relative inverse covariance on every
> smooth periodic NSE solution.

The unresolved mathematical gap is not the formal pullback. It is one of:

\[
 \text{direct pulled-metric control of }G^{-1}F_{\rm err}G^{-\mathsf T},
 \tag{5.1}
\]

or

\[
 \text{a coercive multi-scale frame that remains uniformly positive definite.}
 \tag{5.2}
\]

Any proof that first assumes a finite maximum-strain history returns to known
continuation criteria and does not constitute progress on global regularity.
