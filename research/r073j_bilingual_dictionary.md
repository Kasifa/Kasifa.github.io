# R0.73J bilingual terminology ledger

**Status:** source stage  
**Scope:** terminology used in the R0.73J proof, certificates, figure, HTML,
PDF, and cumulative recap

I use the pairs below consistently.  The word *continuum* refers to the
infinite-dimensional operator, not to continuous spectrum and not to a
continuum of eigenvalues.

| 中文 | English | Usage boundary |
|---|---|---|
| 连续算子 | continuum operator | The infinite-dimensional kinetic operator, as opposed to a Fourier truncation. |
| 唯一简单最右特征值支 | unique simple rightmost eigenvalue branch | The certified branch on (0\le d\le1/450).  Do not abbreviate it as continuous spectrum. |
| 连续体谱支证书 | continuum spectral-branch certificate | A certificate for the continuum operator; *continuum branch* is avoided when it could be misread as continuous spectrum. |
| 动能涡量空间 | kinetic vorticity space | The Hilbert space (X\simeq H^{-1}_{\rm per}) with norm (4\langle L^{-1}q,q\rangle). |
| 周期 Rayleigh 算子铅笔 | periodic Rayleigh operator pencil | The analytic Fredholm pencil (T(d,\lambda)), not a frozen finite matrix. |
| 单值矩阵 | monodromy matrix | The one-period fundamental matrix (M(d,\lambda)). |
| Evans 函数 | Evans function | (E(d,\lambda)=\det(M-I)=2-\operatorname{tr}M). |
| Evans 零点阶数 | Evans zero order | The analytic zero order, linked separately to operator algebraic multiplicity. |
| 代数重数 | algebraic multiplicity | The rank of the Riesz projection, equivalently the stabilized generalized eigenspace dimension here. |
| 全局外矩形 | global outer rectangle | The rectangle (11/100<\Re\lambda<19/50\), (|\Im\lambda|<19/50). |
| 局部根圆盘 | local root disk | The disk (|\lambda-17/100|<3/1000). |
| 参数一致边界非消失 | parameter-uniform boundary nonvanishing | A strict enclosure valid for every (d\in[0,1/450]), not sampled continuity. |
| 精确有理多边形绕数 | exact rational polygon winding | Integer winding computed by exact rational ray crossing after a certified curve-to-polygon homotopy. |
| 区间 Clenshaw 范围 | interval-Clenshaw range | An outward-rounded range enclosure of a Chebyshev polynomial on a complete real dyadic cover. |
| 中点 Bernstein 范围 | midpoint-Bernstein range | A Bernstein hull for midpoint coefficients, enlarged by a direct Chebyshev-basis coefficient-residual bound. |
| 插值解析余项 | analytic interpolation remainder | The Bernstein-ellipse error added to the ball-valued interpolant range. |
| Howard 圆盘 | Howard disk | The analytic bound (|\lambda|\le3\sqrt3/16) for right-half-plane eigenvalues. |
| 实部谱隙 | real-part spectral gap | The difference in real parts between the certified branch and every other spectral point. |
| 动能左右重叠 | kinetic left-right overlap | The normalized Hilbert-space pairing 
  ( |\langle\ell,h\rangle_X|/(\|\ell\|_X\|h\|_X) ). |
| 固定相位锚 | fixed phase anchor | The bounded functional 
  (\mathfrak a(h)=(L^{-1}h)(0)), used to choose a nonvanishing normalization. |
| 全纯正负替身 | plus/minus holomorphic substitutes | The (D_\pm,Q_\pm,M_\pm,\phi_\pm) construction replacing conjugation on complex interpolation domains. |
| 共享原始网格独立后处理 | independent post-processing from a shared raw grid | A second range and winding implementation; it is not a fully independent ODE calculation. |
| 自然参数盒抽查 | natural-parameter box spot check | Direct interval ODE recomputation on selected physical boxes; it is corroborative and not a full cover. |
| 严格证书 | validated certificate | Outward-rounded enclosures, analytic remainders, provenance, and a fail-closed decision. |
| 有限诊断 | finite diagnostic | A calculation used for contour design or comparison that carries no continuum theorem by itself. |
| 已闭合 | CLOSED | All release-contract evidence for the named claim has passed. |
| 条件成立 | CONDITIONAL | The statement follows only after the named prerequisite is supplied. |
| 开放 | OPEN | No proof or rigorous negative result has closed the named claim. |

## Fixed claim language

- **Chinese:** 在 (0\le d\le1/450) 上，动能涡量算子恰有一条位于
  ((0.167,0.173)) 的最右实特征值支；该特征值代数简单，其余谱点的
  实部不超过 (0.11)。
- **English:** On (0\le d\le1/450), the kinetic vorticity operator has a
  unique rightmost real eigenvalue branch in ((0.167,0.173)); the eigenvalue
  is algebraically simple, and every other spectral point has real part at
  most (0.11).

- **Chinese:** 归一化动能左右重叠至少为 (1/2)，固定相位锚在整条谱支上
  不为零。
- **English:** The normalized kinetic left-right overlap is at least (1/2),
  and the fixed phase anchor is nonzero along the complete branch.

## Required limitation language

- **Chinese:** 这一结果认证一个平面周期线性化算子的谱支，不证明黏性支的
  一致持续、非自伴绝热余项、横向三维闭合、有限时间奇性或 Clay 问题。
- **English:** This result certifies a spectral branch of one planar periodic
  linearized operator.  It does not prove uniform persistence of a viscous
  branch, a nonselfadjoint adiabatic remainder, transverse three-dimensional
  closure, finite-time singularity, or the Clay problem.
