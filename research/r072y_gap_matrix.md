# R0.72Y gap matrix

**Date:** 2026-08-28

The statuses below concern the complete linearization about the exact
two-harmonic heat shear and the scalar invariant rows inherited from R0.72X.
“CLOSED” means the stated analytic result is proved in the bound report.
“FALSE” means an explicit counterexample or scaling witness rules out the
stated extension.  A deterministic certificate checks finite algebra only;
it does not replace the functional-analytic arguments.

| Item | Exact status | Evidence in R0.72Y | Boundary / what remains |
|---|---|---|---|
| Three-dimensional physical linearization | **CLOSED** | Direct differentiation about \(U^b=(0,0,V(t,y))\) gives transport, shear-gradient, pressure, diffusion, and divergence equations | Linear only; no nonlinear perturbation estimate |
| Pressure Poisson factor two | **CLOSED** | Both \(\nabla\cdot(V\partial_{x_3}u)\) and \(\nabla\cdot(u_2V_ye_3)\) equal \(iK_zV_yu_2\) | Sign convention is frozen with \(+\nabla p\) on the left |
| Bloch normalization and row Leray projection | **CLOSED** | \(A_\beta,\mathcal L,\nabla_j,\operatorname{div}_j\) give \(\operatorname{div}_j\nabla_j=-\mathcal L\) and \(\mathbb P_j=I+\nabla_j\mathcal L^{-1}\operatorname{div}_j\) | \(\mathcal L^{-1}\) requires a positive row gap |
| Exact orthogonal row decomposition | **CLOSED structural identity** | Shear multiplication preserves \(m\bmod R\), while Leray is diagonal in complete Fourier frequency | Orthogonality gives no uniform row estimate by itself |
| Orr--Sommerfeld row | **CLOSED identity** | \(q=\mathcal Lu_2\) satisfies \(q_d=(-\mathcal L-icW)q-icW_{xx}\mathcal L^{-1}q\) | Scale-sharp absorption of the pressure feedback is **OPEN** |
| Squire row | **CLOSED identity** | \(\eta=i\gamma u_1-i\xi u_3\) satisfies \(\eta_d=(-\mathcal L-icW)\eta+i\xi\Lambda W_x\mathcal L^{-1}q\) | \(|c|=|\gamma\Lambda|\) does not control \(|\xi\Lambda|\) uniformly |
| Velocity recovery and kinetic energy | **CLOSED for \(\mu>0\)** | Exact \(2\times2\) inverse gives \(u_1,u_3\) and the \(\mu^{-1}\) energy identity | Must not be continued to \(\mu=0\) |
| Exceptional \(\mu=0\) rows | **CLOSED structural split** | Nonzero Bloch residue forces \(u_2=0\); zero residue retains component lift-up | Requires component variables, not OS--Squire inverses |
| Scalar \(A_2\) invariant embedding | **CLOSED** | \(u=g(\gamma,0,-\xi)/\sqrt\mu\) reduces exactly to the R0.72X scalar row | It is a proper subspace |
| Scalar \(A_2\) equals complete row | **FALSE** | General data activate pressure feedback and Squire transfer | Complete strong row remains **OPEN** |
| Full-row energy identity | **CLOSED** | Exact shear-production balance \(-\Lambda\operatorname{Re}\langle W_xu_2,u_3\rangle\) | Production has no fixed sign |
| Damping-dominated full rows | **CLOSED** | If \(g_j>|\Lambda|M_K/2\), the full velocity decays with explicit exponent | Low-gap rows remain **OPEN** |
| Exact zero-coupling lift-up | **CLOSED** | For \(\gamma=\beta=0\), \(u_3=-\Lambda\tau e^{-\xi^2\tau}W_x(d_2)u_2(d_1)\) | The formula allows transient growth |
| Mean-zero full-row contraction based only on \(\varepsilon_j\) | **FALSE** | \(\xi>0,\gamma=0\) gives a physical mean-zero perturbation with \(\varepsilon_j=0\) and amplification for large \(|\Lambda|\) | A bound with orientation payment or transient prefactor is not refuted |
| Strong scalar \(L_d^2L_x^2\) forcing | **CLOSED at \(\alpha^2\)** | Exact causal-kernel \(L^1\) norm and Young convolution | Scalar invariant rows only |
| Strong scalar standard \(L_d^2H^{-1}_\beta\) forcing | **CLOSED at \(\alpha\)** | Backward adjoint energy plus transposition | \(\alpha^2\) is **FALSE** |
| Strong scalar semiclassical \(L_d^2\mathcal H^{-1}_{\alpha,\beta}\) forcing | **CLOSED at \(\alpha^2\)** | Semiclassical adjoint \(H^1\) norm retains the extra power | Norm depends explicitly on \(\alpha\) |
| Standard \(H^{-1}\) endpoint gain | **FALSE** | A terminal high-frequency pulse has unit input norm and order-one endpoint response | Safe endpoint coefficient is \(O(1)\) |
| Semiclassical endpoint | **CLOSED at \(\alpha\)** | Prefix energy estimate and spacetime transfer | No \(\alpha^2\) endpoint claim |
| Standard and semiclassical spacetime powers | **CLOSED and sharp** | Localized mean-zero collision-chart witness gives ratios \(\alpha\) and \(\alpha^2\) | Scaling limit is analytic, not finite-certified |
| Strong scalar direct sum | **CLOSED without row-count loss** | Square, sum, and use Parseval with row weights \(\alpha_j\) or \(\alpha_j^2\) | Only decoupled invariant rows |
| Weak/zero scalar finite-history ledger | **CLOSED** | Energy and Gronwall give \(O_K(1)\) bounds | No common strong-row power |
| Time-global gap estimate | **CLOSED when \(\rho^2+\mu>0\)** | Covariant Poincare gives \(\gamma_{\rho,\mu}^{-1}\) | Gapless constant row grows linearly under forcing |
| Mean-zero weak-row restriction | **NOT AUTOMATIC** | Multiplication by \(W\) can create a mean at \(\beta=0\) | Requires an explicit projection or pure heat |
| Complete strong-row \(A_2\) estimate | **OPEN** | Scalar estimates do not absorb OS pressure and Squire transfer | Next target |
| Complete linearized shear subsystem | **OPEN** | High-gap class and scalar polarization are closed, low-gap vector class is not | No global vector direct sum |
| Nonlinear Navier--Stokes / Clay | **OPEN** | No nonlinear convolution, vortex-stretching bootstrap, or continuation criterion | No global regularity or blow-up result |

## Next minimal theorem

Work directly with

\[
 q_d=(-\mathcal L-icW)q-icW_{xx}\mathcal L^{-1}q,
\]

\[
 \eta_d=(-\mathcal L-icW)\eta
 +i\xi\Lambda W_x\mathcal L^{-1}q.
\]

The next gate should:

1. seek a collision-scale resolvent or forced estimate that absorbs the
   Orr--Sommerfeld feedback;
2. split rows by the orientation ratio \(|\xi/\gamma|\) and the damping gap;
3. retain an explicit lift-up transient prefactor;
4. keep \(\mu=0\) in component variables;
5. postpone nonlinear convolution until a uniform weighted full-row bound
   is actually proved.
