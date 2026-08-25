# R0.71N 一手文献核查：固定单元归一化 Lamb–涡量配对

**核查日期：2026-08-26**
**性质：bounded literature audit，不是原创性或优先权证明。**

## 1. 核查对象与代数边界

本次核查针对

\[
L=P(u\times\omega),\qquad F_j=T_jL,\qquad
C_Q=\nabla\times(\chi_QT_j\omega),
\]
\[
Y=\|\omega\|_2^2,\qquad d_Q=\|C_Q\|_2^2,\qquad
B_Q=\langle F_j,C_Q\rangle,
\]
\[
z_Q=\frac{B_Q}{\sqrt{Yd_Q}}
\]

在固定物理单元 \(Q\) 上的时间演化。只比较论文原文、arXiv 原文、作者页面或期刊原文。

先区分通用微积分与可能含有 NSE 内容的部分。若暂略下标，令

\[
B=\langle F,C\rangle,\qquad d=\|C\|_2^2,
\]

则在 \(Y,d>0\) 时恒有

\[
z_t=\frac{B_t}{\sqrt{Yd}}
-\frac z2\left(\frac{Y_t}{Y}+\frac{d_t}{d}\right),
\]
\[
B_t=\langle F_t,C\rangle+\langle F,C_t\rangle,
\qquad d_t=2\langle C,C_t\rangle.
\]

令 \(x=F/\sqrt Y\)、\(E=C/\|C\|_2\)、\(P_E=I-E\otimes E\)，则

\[
E_t=\frac{P_EC_t}{\|C\|_2},\qquad
z_t=\langle x_t,E\rangle+\langle P_Ex,E_t\rangle.
\]

这是 Hilbert 单位球上归一化映射的通用切空间微分，亦可视为连续 Gram–Schmidt 投影；乘积法则本身不能作为研究原创点。需要核查的是选取 \(F_j,C_Q,Y,d_Q\) 后，NSE 展开是否产生新的、可用于闭合估计的结构。

### 两项必须保留的限制

1. **\(z_Q\) 不是通常意义的相关系数或夹角余弦。** 标准余弦的分母应为 \(\|F_j\|_2\|C_Q\|_2\)，而这里为 \(\sqrt Y\|C_Q\|_2\)。一般只能推出
   \[
   |z_Q|\leq \frac{\|F_j\|_2}{\sqrt Y},
   \]
   不能无条件写成 \(|z_Q|\leq1\)。下文称其为“归一化配对”或 “projective scalar”。

2. **三维总 enstrophy 导数含涡量拉伸。** 按
   \[
   u_t=\nu\Delta u+P(u\times\omega)
   \]
   的符号约定，
   \[
   Y_t=2\langle\omega,\nabla\times P(u\times\omega)\rangle
   -2\nu\|\nabla\omega\|_2^2.
   \]
   因而不能使用二维式 \(Y_t/2=-\nu\|\nabla\omega\|_2^2\)。

## 2. 一手来源的直接重叠与缺口

| 一手来源 | 直接相关定理或公式 | 与 R0.71N 的直接重叠 | 尚缺的对象 |
|---|---|---|---|
| Eyink, *The Cascade of Circulations in Fluid Turbulence*, [arXiv:physics/0606159](https://arxiv.org/abs/physics/0606159) | 式 (7)–(9) 给出局部 enstrophy 方程；式 (15) 定义 \(f_\ell^*=\overline{u\times\omega}_\ell-\bar u_\ell\times\bar\omega_\ell\)；式 (28)–(31) 给出 filtered vorticity/enstrophy 方程。 | 粗粒化 Lamb 向量、subgrid vortex force、过滤涡量及 enstrophy 配对已有明确先例。 | 使用平移不变低通滤波；没有固定 \(\chi_Q\)、\(C_Q=\nabla\times(\chi_QT_j\omega)\)、\(d_Q^{-1/2}\)、Hilbert 切投影或 \(B_Q/\sqrt{Yd_Q}\) 演化。 |
| Yu, *Filtered Vortex Stretching and Subgrid Defects for the Three-Dimensional Navier–Stokes Equations*, [arXiv:2606.27560v1](https://arxiv.org/abs/2606.27560v1) | 式 (6.1)–(6.3) 给出 \(R_\ell\)、filtered vorticity 及 \(F_\ell=-\nabla\times\nabla\cdot R_\ell\)；Proposition 6.1、式 (6.5)–(6.11) 给出局部 filtered-enstrophy 恒等式；Proposition 6.4 以伴随漂移扩散 cutoff 消去 localization row。 | 截至核查日，这是最接近“过滤涡量 + 局部 cutoff + 完整误差 ledger”的精确恒等式。 | cutoff 可随解选择；没有固定预指定单元上的 cutoff-curl 方向、Lamb 配对、projective 分母或其时间导数。2026 年预印本，不能按已同行评审结果表述。 |
| Dascaliuc–Grujić, *Coherent Vortex Structures and 3D Enstrophy Cascade*, [arXiv:1107.0058](https://arxiv.org/abs/1107.0058) | 式 (3.1) 将局部 enstrophy 分解为耗散、\(\phi_t+\Delta\phi\)、输运 cutoff 和 vortex-stretching 项。 | 固定物理单元、光滑 cutoff、collar/输运项的分部积分结构是已有标准机制。 | 未作 LP 过滤；没有 filtered Lamb 配对、cutoff-curl 状态、归一化或切空间动力学。 |
| Tao, *Localisation and Compactness Properties of the Navier–Stokes Global Regularity Problem*, [arXiv:1108.1165](https://arxiv.org/abs/1108.1165) | Theorem 10.1 是含局部初始涡量、curl forcing 和尺度小量条件的 enstrophy localisation 定理；证明中的式 (84)–(85) 分列耗散、cutoff、热通量、输运、外力和非线性项。 | 给出严谨局部 enstrophy ledger 及边界项控制框架。 | 依赖额外小量条件及移动/有利 cutoff；不是 LP–Lamb–projective 恒等式。 |
| Galanti–Gibbon–Heritage, *Vorticity Alignment Results for the Three-Dimensional Euler and Navier–Stokes Equations*, [arXiv:chao-dyn/9709003](https://arxiv.org/abs/chao-dyn/9709003) | 定义 \(\xi=\omega/|\omega|\)、\(\alpha=\xi\cdot S\xi\)、\(\chi=\xi\times S\xi\)、\(\tan\phi=\chi/\alpha\)；式 (34)–(39) 等价地包含 \((I-\xi\otimes\xi)\) 切投影。 | 是 \(E_t=(I-E\otimes E)C_t/\|C\|\) 最直接的流体力学类比，并给出动态夹角语言。 | 点态三维方向在 \(|\omega|=0\) 处奇异；不是固定单元的 Hilbert 方向，没有 Lamb 配对或 \(B_Q/\sqrt{Yd_Q}\)。 |
| Milanese–Loureiro–Boldyrev, *Dynamic Phase Alignment in Navier–Stokes Turbulence*, [arXiv:2104.13518](https://arxiv.org/abs/2104.13518) | 式 (6) 定义尺度依赖的归一化速度–涡量相位夹角 \(\cos\alpha_k\)。 | 表明频率尺度上的 normalized alignment 是已有诊断量。 | 这是 DNS 壳层统计量；分母不是 \(\sqrt{Yd_Q}\)，且没有精确时间演化。 |
| Bradshaw–Grujić, *Frequency Localized Regularity Criteria for the 3D Navier–Stokes Equations*, [arXiv:1501.01043](https://arxiv.org/abs/1501.01043) | 采用标准 Littlewood–Paley 分解并给出频率窗口/Besov 型正则性判据。 | LP 局部化和关键频率窗口属于既有 NSE 正则性方法。 | 控制的是 \(\|\Delta_ju\|_\infty\) 等范数；没有 filtered Lamb、物理单元或 projective pairing。 |
| Grujić, *Logarithmic Depletion of Vortex Stretching and Singularity Evasion in the 3D Navier–Stokes Equations*, [arXiv:2607.08866](https://arxiv.org/abs/2607.08866) | 式 (7) 将拉伸标量写成 \(\alpha(x)=\xi(x)\cdot[T,\xi](\omega)(x)\cdot\xi(x)\)，并以方向场的对数空间正则性估计拉伸。 | 与最新的涡量方向几何耗减路线相邻。 | 研究空间方向正则性和奇异积分交换子，含条件假设；没有固定单元时间归一化配对。2026 年预印本。 |

Eyink 的未过滤局部 enstrophy 方程明确包含

\[
\partial_t\frac{|\omega|^2}{2}
+\nabla\cdot\left(
\frac{|\omega|^2}{2}u-\nu\nabla\frac{|\omega|^2}{2}
\right)
=\omega^\top S\omega-\nu|\nabla\omega|^2,
\]

这也独立确认了上一节关于 \(Y_t\) 中拉伸项的限制。

## 3. 检索范围与 bounded negative finding

截至 **2026-08-26**，核查包括 arXiv 元数据检索、原文关键词检索以及上述论文 PDF/HTML 的公式复核。重点组合词包括：

- “B_Q” + “d_Q” + “vorticity”；
- “z_Q” + “d_Q” + “Navier-Stokes”；
- “projective” + “Lamb vector” + “Navier-Stokes”；
- “fixed-cell” + “Lamb” + “vorticity”；
- “normalized correlation” + “Navier-Stokes”；
- “filtered Lamb” + “vorticity”；
- “Lamb vector” + “Littlewood-Paley”；
- “vorticity direction” + “time derivative”。

在这一限定检索范围内，**未找到**一手来源陈述下列完整对象的演化律：

\[
\frac{B_Q}{\sqrt{Yd_Q}},\qquad
B_Q=\langle T_jP(u\times\omega),
\nabla\times(\chi_QT_j\omega)\rangle,
\]

同时保留固定物理单元上的 \(B_{Q,t}\)、\(Y_t\)、\(d_{Q,t}\) 及相应 cutoff/commutator 行。

这是 **bounded negative finding**，不是“不存在相同结果”的证明。检索不能排除不同术语、不同符号、非 arXiv 期刊文献、专著、会议论文或未公开稿中的重合。正式主张新颖性前，仍需 MathSciNet、zbMATH、引文网络和领域专家核查。

## 4. 可使用的表述边界

可审计的表述是：

> 已核查的一手来源分别覆盖局部 enstrophy cutoff 恒等式、过滤 Lamb/vortex force、单位方向切投影及频率尺度 alignment；在本次限定检索中，尚未发现把这些部件合并为上述固定单元 \(B_Q/\sqrt{Yd_Q}\) 时间演化恒等式的直接来源。

不得据此写“首次”“原创”“优先结果”，也不得把该恒等式本身描述为对三维 Navier–Stokes 正则性或千禧年问题的实质推进。R0.71N 已用独立 Fourier 实现复核 \(F_{j,t}\)、\(C_{Q,t}\)、\(Y_t\) 与五种完整标量表示；尚未完成的是 outward-rounded 符号证书，以及由该恒等式导出的统一估计。下一节先处理 \(d_Q\downarrow0\) 时 hard/soft denominator 的极限与一侧 face measure，不进入 refresh 或 moving cutoff。
