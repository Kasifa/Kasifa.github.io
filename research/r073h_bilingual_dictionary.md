# R0.73H bilingual dictionary

**Version:** R0.73H  
**Purpose:** keep the Chinese HTML/PDF, the English in-page translation,
and the analytic sources aligned

| English | 中文 | Fixed meaning in R0.73H |
|---|---|---|
| gain-normalized seed | 按实际增益归一化的种子 | \(u(0)=\delta\phi_\Lambda/G_\Lambda\), where \(G_\Lambda\) is the actual selected endpoint gain |
| prescribed lower-law seed | 按下界指数预设的种子 | \(\delta e^{-r\Lambda D}\phi_\Lambda\); R0.73H does not prove fixed-distance departure for this scale |
| family-level nonlinear departure | 背景族层面的非线性固定距离偏离 | backgrounds and initial perturbations both depend on \(\Lambda\) |
| fixed-distance endpoint | 固定距离端点 | target-row norm at least \(\delta/2\), independent of sufficiently large \(\Lambda\) |
| moving unstable bundle | 移动不稳定丛 | the finite-dimensional nonautonomous bundle supplied by R0.73F |
| backward localization | 反向局部化 | the endpoint-normalized unstable orbit decays exponentially when followed backward from \(D\) |
| harmonic selection rule | 谐波选择律 | order \(j\) contains only \(K_z=-j,-j+2,\ldots,j\) |
| quadratic leakage | 二次谐波泄漏 | the carrier \(K_z=\pm1\) creates \(K_z=0,\pm2\) |
| cubic target return | 三次目标回馈 | the mean and doubled rows return to \(K_z=\pm1\) and also create \(K_z=\pm3\) |
| mean-return path | 零频回馈路径 | ordered paths \((1,0)\) and \((0,1)\) |
| double-return path | 倍频回馈路径 | ordered paths \((-1,2)\) and \((2,-1)\) |
| numerical abscissa | 数值横坐标 | the largest real part of the kinetic quadratic form, not a spectral eigenvalue |
| doubled-row bound | 倍频行上界 | the continuum estimate \(\omega_1(d)\le1/3\) for \(K_z=\pm2\) |
| gauge completion | 规范变换配方 | the unitary reduction to \(-\partial_x^2+1-\frac94W_x^2\) |
| exact rational subcertificate | 精确有理数子证书 | the finite \(|m|\le4\) LDL or determinant calculation inside an analytic infinite-tail proof |
| Stieltjes localization lemma | Stieltjes 局部化引理 | converts cumulative dissipation envelopes into harmonic Duhamel envelopes |
| cumulative dissipation | 累计耗散 | \(M_h(s)=\frac14\int_0^s\|\nabla h\|_2^2\,d\tau\) |
| fourth-order remainder | 四阶余项 | the exact error after retaining the linear, quadratic, and cubic Taylor coefficients |
| unit-real launch | 单位实值共轭初态 | a real \(K_z=\pm1\) pair with total physical \(L^2\) norm one |
| finite Galerkin diagnostic | 有限 Galerkin 诊断 | binary64 evidence at stated cutoffs; not a continuum PDE proof |
| compensated ratio | 补偿比率 | a finite coefficient divided by its predicted power of \(\varepsilon_\nu\) and the linear endpoint gain |
| signed parallel feedback | 有符号平行回馈 | cubic target projection onto the linear endpoint direction; negative means opposing that direction |
| planar invariant subspace | 平面不变子空间 | \(u_1=0\), no \(x\)-dependence, equivalent to periodic 2D Navier--Stokes |
| transverse three-dimensional coupling | 横向三维耦合 | a mode with \(K_x\ne0\) or a nonzero first velocity component |
| CLOSED | 已闭合 | supported by the stated continuum proof or exact certificate |
| FINITE | 有限证据 | reproducible finite-dimensional computation only |
| OPEN | 未闭合 | not proved by the present release |
| FALSE AS INFERENCE | 推断无效 | the stated conclusion does not follow from the available premise |

## Required wording boundary

Use “gain-normalized” for \(\delta/G_\Lambda\).  Do not translate it as
“sharp natural scale” or state that
\(G_\Lambda\asymp e^{r\Lambda D}\).  The available theorem supplies only
the lower bound

\[
 G_\Lambda\ge K_{\rm F}^{-1}e^{r\Lambda D}.
\]

Use “planar” for the selected nonlinear orbit.  Do not translate the
family-level fixed-distance departure into a three-dimensional singularity,
vortex-stretching, or Clay conclusion.
