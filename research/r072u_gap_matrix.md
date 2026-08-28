# R0.72U gap matrix

**Date:** 2026-08-28

| Item | Exact status | Evidence in R0.72U | What is still required |
|---|---|---|---|
| Literal spatial-cutoff audit | **closed negative audit** | If \(v\in H_0^1((-R,R))\), ordinary Poincare proves the proposed inequality without using \(P_c\); \(v=\eta u\) also inserts the zero-order term \(\eta'u\) into \(v_X\) | Do not use this trace-restricted statement as \(A_2\) observability |
| Function space | **closed** | Time interval \(I=(-T,T)\), spatial chart \(J=(-R,R)\), \(H_D^{-1}(J)=(H_0^1(J))^*\), \(v\in L^2_IH^1_J\), \(P_cv\in L^2_IH_D^{-1}\), no temporal or spatial trace conditions | Whole-line weighted graph space remains separate |
| Graph-space traces | **closed boundary audit** | The full function is used only as \(v\in C(\overline I;H_D^{-1}(J))\); no \(L^2(J)\) endpoint trace is claimed.  The scalar moments \(A,B\in H^1(I)\) have the endpoint traces used in the proof | None for the scalar endpoint argument |
| Weighted Poincare lemma | **closed** | Even normalized \(q_0\in C_c^\infty(J)\) and \(A=\int vq_0\) give \(\|v-A\|_2\le C_P\|v_X\|_2\) without boundary values | None on the fixed chart |
| Exact rational-probe ledger | **closed algebraic calibration** | On a chart containing \([-1,1]\), \(\rho=(315/256)(1-X^2)^4\mathbf1_{[-1,1]}\) lies in \(H_0^1\), as does \(X\rho\); \(\mu_2=1/11\), \(\mu_4=3/143\), and \(T=1\) gives the sufficient threshold \(\lvert c\rvert\ge27/13\) | The finite ledger does not machine-check compactness, graph-space traces, or the functional-analytic limit |
| Scalar moment system | **closed** | \(q_1=Xq_0\), \(A'=i\sigma\langle V_cr,q_0\rangle+G_0\), and \(B'=i\sigma[m_4+6(c+t)m_2]A+E\) | None for the declared graph space |
| Bounded-center coercivity | **closed** | \(A_n'\to0\), \(B_n\to0\), and the affine second-moment coefficient force the only normalized compactness limit to vanish | None on a fixed \(R,T\) chart |
| Escaping-center coercivity | **closed** | For \(|c|\to\infty\), the second moment has fixed sign and size \(3m_2|c|\); scalar endpoint traces are bounded explicitly and all divided endpoint terms vanish without assuming \(|c|\|v_X\|\to0\) | None on a fixed \(R,T\) chart |
| Endpoint conditions | **closed absence result** | The integration by parts retains \([B\overline A]_{-T}^{T}\); the scalar \(H^1\) trace inequality controls it | No endpoint vanishing is required |
| Exact inviscid gauge calibration | **closed** | Every \(P_cv=0\) solution satisfies \(\|v_X\|_2^2\ge(4/5)T^4\|v\|_2^2\); the optimized phase is explicit | This does not produce viscous norm loss by itself |
| Time-length uniformity | **closed negative result** | The exact family \(e^{i\sigma(tX^3+3t^2X-T^2X)}\) has derivative ratio \((3/5)T^2R^4+(4/5)T^4\) | Keep \(T>0\) fixed; no claim as \(T\downarrow0\) |
| `centerUniformLocalGraphCoercivity` | **CLOSED** | Theorem 2.1 proves the graph estimate with a finite constant independent of interval center \(c\) | No explicit numerical value for the constant is claimed |
| `localSolutionObservability` | **CLOSED** | For \(P_cu=u_{XX}\), \(\|u\|_{L^2(I\times J)}\le2C_{R,T}\|u_X\|_{L^2(I\times J)}\) without a time cutoff | A global lower bound requires tail control |
| Bounded-chart dissipative contraction | **closed conditional consequence** | With a valid chart energy identity, \(E(T)\le C_{R,T}(T+C_{R,T}^2)^{-1/2}E(-T)\) | Quantitative rate is non-explicit because \(C_{R,T}\) is non-explicit |
| `wholeLineBlockContraction` | **OPEN** | The local theorem controls only \(I\times(-R,R)\); global mass may remain outside the chart | Uniform tails, annular flux, cutoff commutators, and all-start iteration |
| `periodicTransfer` | **OPEN** | No \(H_5,H_7,R_9\) absorption or periodic localization is proved here | Weighted remainders, localization, tails, and rescaling back to the heat path |
| Nonlinear Navier--Stokes consequence | **OPEN** | No pressure, stretching, mode-coupling, or bootstrap estimate is made | A separate nonlinear closure |
| `Clay` | **OPEN** | The result is a linear bounded-chart coercivity theorem | A global regularity or finite-time blow-up theorem for arbitrary smooth three-dimensional data |

## Next minimal theorem

The next section should prove a center-uniform whole-line tail estimate strong
enough to replace local spacetime mass by a fixed fraction of global mass and
to absorb

\[
 2\eta'u_X+\eta''u
\]

from spatial localization.  Only after that step can the bounded-chart
contraction be promoted to `wholeLineBlockContraction=CLOSED`.
