# R0.74N — independent primary-literature audit

## Binding and verdict

- Audit date: 2026-09-02.
- Audited file: `research/r074n_primary_literature_boundary.md`.
- Audited SHA-256:
  `485883f09b417a51326acc1cf94e37d86cb62cf4ff22bfaba2ef9f0f9d555054`.
- Source policy: primary pages only—official arXiv records and, for the
  weighted-energy paper, the journal's official version-of-record page.
- Verdict: **PASS**.

The eight titles, author lists, and stated research scopes agree with the
screened primary sources.  The file also states the only conclusion licensed
by this screen: no theorem in the screened set directly supplies the exact
R0.74N all-shell estimate.  It does **not** turn that bounded non-hit into a
claim of novelty, priority, exhaustiveness, or publishability.

## Item-by-item reconstruction

| No. | Primary record | Independent check | Result |
|---:|---|---|---:|
| 1 | [Fernández-Dalgo--Lemarié-Rieusset, arXiv:1906.11038](https://arxiv.org/abs/1906.11038) | The official record gives the two listed authors and the exact title.  Its abstract concerns global weak 3D Navier--Stokes solutions for initial data in polynomially weighted \(L^2\) spaces and an existence application, not a periodic signed collar observable. | PASS |
| 2 | [Fernández-Dalgo--Lemarié-Rieusset, arXiv:2010.00868](https://arxiv.org/abs/2010.00868); [Journal of Mathematical Fluid Mechanics version of record](https://link.springer.com/article/10.1007/s00021-021-00603-0) | Both official records give the two listed authors and the exact title.  The paper develops weighted energy inequalities; its displayed weighted balance contains \(\nabla\Phi\) terms.  Its main application is regular global axisymmetric flow without swirl, not the R0.74N moving family or super-Gaussian annular ledger. | PASS |
| 3 | [Bradshaw--Tsai, arXiv:2008.09204](https://arxiv.org/abs/2008.09204) | The official record gives the listed authors and title.  The paper's \(E_q^2\) and \(\mathbf{LE}_q\) norms aggregate local energies over lattice-indexed balls through an \(\ell^q\) norm.  This supports the stated local-energy precedent but not the signed collar trace. | PASS |
| 4 | [Choe--Yang, arXiv:1705.04561](https://arxiv.org/abs/1705.04561) | The official record gives Hi Jun Choe and Minsuk Yang and the listed title.  Its theorems concern local kinetic-energy control, a reverse Hölder estimate, and dimensions of the singular set. | PASS |
| 5 | [Bedrossian--Coti Zelati, arXiv:1510.08098](https://arxiv.org/abs/1510.08098) | The official paper studies semigroups for passive scalars under a fixed shear \(u=u(y)\), proving enhanced dissipation and hypoelliptic regularization.  The source file correctly separates this from a time-dependent, family-dependent signed annular trace. | PASS |
| 6 | [David Villringer, arXiv:2405.12787](https://arxiv.org/abs/2405.12787) | The author is **David Villringer**.  The paper treats a fixed smooth shear \(u(y)\) and uses Malliavin integration by parts together with bounds on the Malliavin matrix determinant.  Calling it covariance/Malliavin precedent is safe; it does not provide the endpoint-correlated R0.74N collar estimate. | PASS |
| 7 | [Gardner--Liss--Mattingly, arXiv:2410.05657](https://arxiv.org/abs/2410.05657) | The author list is exactly **Victor Gardner, Kyle L. Liss, Jonathan C. Mattingly**.  The paper uses stochastic trajectories and Girsanov control to prove enhanced-dissipation and total-variation estimates for autonomous shear flows.  These are path-method precedents, not an all-shell signed sum. | PASS |
| 8 | [Liss--Luan, arXiv:2603.09238](https://arxiv.org/abs/2603.09238) | The author list is exactly **Kyle L. Liss and Kunhui Luan**.  The March 2026 paper proves uniform-in-diffusivity mixing for parallel shear flows using stochastic representation, stochastic integration by parts, and a dynamical argument.  Its theorem has a different observable and scale from R0.74N. | PASS |

## Bounded collision check

The independent screen combined the eight exact-record reads above with
targeted arXiv searches in the following claim families:

- weighted Navier--Stokes energy plus annular, dyadic-shell, collar, and
  signed-flux terminology;
- super-Gaussian Navier--Stokes weights;
- shear/Brownian path methods plus endpoint correlation, bridge, annular,
  and collar terminology;
- passive-scalar shear mixing plus stochastic good/bad path decompositions.

Within this bounded screen, no theorem was located that simultaneously has
the calibrated periodic two-packet family, the smooth super-Gaussian annular
sum, the endpoint-correlated inward bridge, and the infinite lift-side outer
tail at the target \(\Gamma_jL_jR_j^5\) scale.  The nearby papers instead prove
weighted existence or regularity statements, local-energy estimates,
semigroup decay, total-variation contraction, or mixing estimates.

This finding is deliberately phrased as **no direct theorem in the screened
sources**.  Different terminology, an uncatalogued paper, a later version, or
a theorem outside the bounded query set could change a broader collision
assessment.  Consequently this audit provides no novelty search, no priority
claim, no publication claim, and no substitute for expert literature review.

## Logical boundary

The literature file is valid only as a black-box-import boundary.  It does
not verify any R0.74N sign, shell constant, bridge estimate, infinite-tail
summation, or PDE conclusion.  Those remain obligations of the analytic proof
and its independent mathematical reconstruction.  Conversely, R0.74N does
not inherit the cited papers' semigroup-decay, regularity, continuation, or
global-existence conclusions.  **NOT CLAY.**
