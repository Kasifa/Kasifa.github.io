# R0.72T gap matrix

**Date:** 2026-08-28

| Item | Exact status | Evidence in R0.72T | What is still required |
|---|---|---|---|
| Collision-centered shear | **closed** | Exact formula \(W(d,x)=\frac12e^{-d}[-\sin x+\frac12e^{-3d}\sin2x]\) and \(W_d=W_{xx}\) | None for the declared path |
| Heat-polynomial jet | **closed** | Exact series and \(-H_3/4+H_5/16-H_7/160+R_9\) | Weighted global remainder norms for transfer |
| Primitive versus derivative | **closed negative result** | The fold derivative integrates to \(x^3+6dx\); a pure-time term is scalar-gauge removable; the separate quadratic model has scale \((\nu\lvert kb\rvert)^{-1/2}\) | None for this calibration |
| Four-term scaling | **closed** | Unique solution \(X=\kappa^{1/5}x\), \(S=\kappa^{2/5}d\), \(\kappa=\varepsilon_c/4\) | None at formal bounded-chart level |
| Bounded-chart model | **closed** | \(u_S=u_{XX}+i\sigma[H_3-\kappa^{-2/5}H_5/4+\kappa^{-4/5}H_7/40+O_R(\kappa^{-6/5})]u\) | Global weighted perturbation theorem |
| Real translation/scalar gauge reduction | **closed negative result** | Translation produces \(3cY^2+(3c^2+6S)Y\); scalar gauge removes only the constant | None for the declared transformation class |
| Inviscid propagator | **closed** | Exact two-parameter multiplier; symmetric block leaves \(e^{i\sigma TX^3}\) | Viscous comparison uniform in start time |
| \(H^1\to H^{-1}\) mixing | **closed** | Uniform \(C\min(1,T^{-1/3})\) via third-order van der Corput | A sharper structure-aware viscous argument |
| CDZE route | **closed method barrier** | \(p=1/3\Rightarrow q=6/7\), plus global-line compactness failure | Different quantitative mechanism |
| Weighted bracket | **closed** | Both \([X_1,[X_1,[X_1,X_0]]]\) and \([X_0,[X_1,X_0]]\) generate \(-6\partial_\theta\) at weight five | Quantitative global subelliptic Poincaré/observability |
| Drift-only calibration | **closed** | Exact norm exponent \(\nu a^2(m^2T^3/12+T^5/720)\); \(a=kA\nu\) gives \(T\asymp\lvert kA\rvert^{-2/5}\nu^{-3/5}\) | Extension to the cubic model |
| Combined fixed-\(f\) magnetic form | **closed, non-observability** | Persistent term \((ac+3bX^2)^2T^3/12+a^2T^5/720\) for one fixed function | Evolving-solution observability |
| Full model block contraction | **OPEN** | No valid proof in this release | Uniform \(L^2\) contraction for one fixed block length and all starts |
| Periodic heat-path transfer | **OPEN** | Bounded-chart asymptotics only | Localization, tails, time cutoffs, and weighted remainder absorption |
| Nonlinear Navier--Stokes consequence | **OPEN** | No nonlinear estimate is made | Coupling to pressure, stretching, mode interactions, and bootstrap closure |
| Clay regularity problem | **OPEN** | Long-range motivation only | A global regularity or finite-time blow-up theorem for arbitrary smooth data |

## Next minimal theorem

R0.72U should target one statement only: a global-\(X\), all-start
quantitative subelliptic Poincaré/time-cutoff estimate of the form

\[
 \|\chi u\|_{L^2_SL^2_X}\lesssim
 \|\partial_X(\chi u)\|_{L^2_SL^2_X}
 +\|(\partial_S-i\sigma H_3)(\chi u)\|_{L^2_SH^{-1}_X},
\]

strong enough to imply solution observability for

\[
 \partial_Su-\partial_X^2u-i\sigma(X^3+6SX)u=0,
\]

uniformly over every interval start.  It must include endpoint control,
unbounded-\(X\) tails, and a weighted remainder estimate strong enough to
control \(H_5,H_7,R_9\).  The next section should not claim a periodic
transfer until all pieces are proved.
