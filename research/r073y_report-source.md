# R0.73Y｜Exact shear 类否定 production-only coercivity

**副标题：** 全尺度零生产、严格正 heat covariance 与最小修复边界

**日期：** 2026-09-01

**状态：** `EXACT_ANALYTIC_THEOREM + SINGLE_MODE_DETERMINISTIC_CERTIFICATE + BOUNDED_PRIMARY_SOURCE_AUDIT`

**普通翻译路径：** `LOCAL_DIRECT_NO_DGX`

**DGX used：** `false`

## 1. 本节结论

R0.73X 留下的 signed-to-positive coercivity 桥，至少在
production-only 形式下是假的。存在一整个光滑、零均值、任意振幅的
周期 Navier--Stokes exact shear 类，使

\[
 \Pi_s=\mathscr S_s=Q_s=0
 \qquad\text{for every }t>0, x\in\mathbb T^3, s>0,
\tag{1.1}
\]

同时

\[
 D_{ii,s}>0
\tag{1.2}
\]

逐点严格成立，而且 R0.73X 的正尺度大小满足

\[
 \mathcal Z_A
 :=\mathcal E^\square[u^A](z_0,4R)^{3/2}
 +\mathcal A_{\rm ext}^\square[u^A,p^A](z_0,R;\theta)
 =|A|^3C,qquad C>0.
\tag{1.3}
\]

所以，凡是只由 \(\Pi_s\) 和 \(\mathscr S_s\) 经过 scalar weight、
cutoff、绝对值、有限求和或积分构成、且在零输入处取零的 functional
\(\mathfrak P\)，都不能给出振幅无关的有限模量

\[
 \mathcal Z_A\le\omega(\mathfrak P_A),
 \qquad \omega(0)<\infty.
\tag{1.4}
\]

这是一条 exact no-go theorem，不是正则性判据。反例族本身全部光滑，
没有产生奇性，也没有否定 CKN epsilon regularity。

## 2. 更强的 exact shear 类

取

\[
 k\in\mathbb Z^3\setminus\{0\},\qquad
 a\in\mathbb R^3\setminus\{0\},\qquad a\cdot k=0,
\tag{2.1}
\]

令 \(f_0\in C^\infty(\mathbb T)\) 非常数且零均值，并定义

\[
 F(t,\vartheta)=e^{\nu|k|^2t\partial_\vartheta^2}f_0(\vartheta),
 \qquad
 u^A(t,x)=AaF(t,k\cdot x),qquad p^A=0.
\tag{2.2}
\]

正交条件同时消掉 divergence 和 convection：

\[
 \nabla\cdot u^A=A(a\cdot k)F'=0,
 \qquad
 (u^A\cdot\nabla)u^A=A^2aF(a\cdot k)F'=0.
\tag{2.3}
\]

而 \(F\) 的时间演化恰好支付 \(\nu\Delta u^A\)。这不是静态测试场、
线性化解或数值轨迹，而是真实 NSE 解。

对 \(H_\sigma=e^{\sigma\partial_\vartheta^2}\)，三维 heat filter 精确化为

\[
 P_su^A=AaH_{s|k|^2}F.
\tag{2.4}
\]

其 stress 与 filtered gradient 分别沿
\(a\otimes a\) 和 \(a\otimes k\)：

\[
 \tau_s=A^2(a\otimes a)
 \bigl[H_{s|k|^2}(F^2)-(H_{s|k|^2}F)^2\bigr],
\tag{2.5}
\]

\[
 \nabla P_su^A=A(a\otimes k)\partial_\vartheta H_{s|k|^2}F.
\tag{2.6}
\]

因为

\[
 (a\otimes a):(a\otimes k)=|a|^2(a\cdot k)=0,
\tag{2.7}
\]

故 \(\Pi_s=-\tau_s:\nabla P_su^A=0\)。centered increment 平行于
\(a\)，但只依赖 \(k\cdot y\)；Euclidean-lift Gaussian 在正交的
\(a\)-方向给出奇积分，因此 \(\mathscr S_s=0\)。

相反，gradient covariance 是严格正的 heat variance：

\[
 \boxed{
 D_{ii,s}=A^2|a|^2|k|^2
 \left\{H_{s|k|^2}\![(F')^2]
 -(H_{s|k|^2}F')^2\right\}>0.}
\tag{2.8}
\]

周期 heat kernel 处处为正。若方差在某点为零，则 \(F'\) 在整个圆周
几乎处处为常数；周期性迫使它为零，与 \(f_0\) 非常数及有限时间 heat
半群在非零 Fourier 模上的单射性矛盾。

## 3. 单一 Fourier 见证与可复现证书

证书固定

\[
 u^A(t,x)=Ae^{-\nu n^2t}\sin(nx_2)e_1,qquad n\ge1.
\tag{3.1}
\]

令 \(\rho=e^{-n^2s}\)。可逐项得到

\[
 \tau_{11,s}={b_A(t)^2\over2}
 \bigl[(1-\rho^2)+(\rho^2-\rho^4)\cos(2nx_2)\bigr],
\tag{3.2}
\]

\[
 D_{ii,s}={b_A(t)^2n^2\over2}
 (1-\rho^2)(1-\rho^2\cos(2nx_2))
 \ge {b_A(t)^2n^2\over2}(1-\rho^2)^2>0.
\tag{3.3}
\]

deterministic certificate 在 \(\mathbb Q[\rho][\mathbb Z]\) 中精确核验
NSE residual、heat multiplier、stress、tensor-support contraction、
centered parity、\(D\) 与 fixed-scale trace ledger；另用五组直接 Gaussian
积分作交叉验证。数值最大 scaled discrepancy 为
\(1.286\times10^{-13}\)，但任何普遍量词和严格正性都来自解析证明，
不依赖该有限数值。

跨平台 gate 对解析、代数、结构、量词和 claim ledger 逐字段严格比较；
只有明确位于 numerical cross-check 下的 binary64 字段允许
\(5\times10^{-12}\) 相对、\(5\times10^{-13}\) 绝对容差。stored payload
hash、误差阈值和 Markdown report 绑定仍为严格校验。

## 4. 正 covariance 由什么支付

对单模见证，subfilter energy 的 torus 平均满足

\[
 {d\over dt}\int_{\mathbb T^3}k_s\,dx
 +\nu\int_{\mathbb T^3}D_{ii,s}\,dx=0.
\tag{4.1}
\]

所以 \(\Pi_s=\mathscr S_s=0\) 并不迫使 \(D_{ii,s}=0\)。正 covariance
由 subfilter storage 的下降支付；局部化后，还要保留 endpoint、
time-cutoff、spatial-cutoff 和 viscous-boundary 等 nonproduction debt。
这些项的 signed sum 由 exact ledger 固定，但它们的绝对值不受零 production
控制。

这给出了修复方向：任何可能成立的正向定理，都必须保留至少一个能检测
shear kernel 的正量，例如 scale-critical covariance、endpoint/cutoff
debt，或独立的正 tent norm。

## 5. 文献校准

本节最重要的文献事实不是“未发现重合”，而是发现了直接重合：

- Jeong--Yoneda（2022）在 \(\mathbb T^3\) 上明确使用
  \(u^L(t,x_2)e_1\)，其演化就是一维 heat equation；
- Vreman（2004）已经把 simple shear 列入 exact SGS dissipation 为零的
  laminar flow classes；
- Germano（1992）和 Eyink--Aluie（2009）的 exact small-scale energy
  ledger 已把 signed production 与 nonnegative gradient covariance 分成
  不同账目；
- Johnson（2020）把 Gaussian filter width squared 写成 diffusion-scale
  coordinate，并给出 exact stress evolution；
- Duchon--Robert（2000）建立 cubic increment defect 的局部能量背景；
- Yu（2026，预印本）已明确指出 coarse pressure--flux work 的 observability
  可能因 cancellation/coherent profiles 失败，并把 positive covariance
  作为 anti-kernel 方向之一。

因此，exact shear、\(\Pi_s=0\)、正 covariance 以及一般性的“signed flux
不自动 coercive”都不能申报为新发现。可保留的成果只是：把这些已知机制
放进 R0.73X 的精确定义中，得到一个全 heat scale、全 cutoff/path、真实
NSE、振幅无界的 production-only no-go package。限定检索未发现逐字相同
的打包命题，但这不是 novelty 或 priority 证明。

## 6. 价值评估

本节对整个 Clay 问题的直接推进很小；它不提供任意三维解的新正估计。
它的研究价值是“及时关闭错误路线”：若继续尝试仅从 \(\Pi_s\) 或
\(\mathscr S_s\) 的小ness 推出正尺度 smallness，必然撞上 exact shear
kernel。这个否证节省后续证明成本，并把下一步所需信息写得更精确。

作为独立论文主定理，当前结果过于初等，且与 LES/coarse-graining 文献
高度邻近。若要形成更高水平成果，必须继续完成正向部分：在 quotient 掉
Vreman/orthogonal-shear kernel 后，加入最小 positive observable，并证明
统一 coercivity；或者构造真正三维、pressure-active 的 production-invisible
exact family。

## 7. R0.73Z 的冻结任务

下一节不再尝试 production-only bridge，而先冻结一个同次齐次的正观测：

\[
 \mathcal D_{3/2}^{\square}(z_0,R;\theta)
 ={1\over R}\int_{I_R^\square}\int_0^{\theta R^2}
 \int_{B_R}D_{ii,s}^{3/2}\,dx\,ds\,dt.
\tag{7.1}
\]

它在 Navier--Stokes scaling 下无量纲、对振幅为三次，并能检测本节 shear
kernel。R0.73Z 依次完成：

1. 精确核验 (7.1) 的 scaling、finiteness 和 suitable-weak 正尺度定义；
2. 分类 rank-one orthogonal shear 类上的零 production kernel；
3. 对两模、pressure-active 和 local-cutoff probes 做反例压力测试；
4. 只有通过前三关后，才提出 quotient coercivity 的精确定理；
5. 任何失败都以 exact counterexample 记录，不把 conjecture 写成 theorem。

开放项仍包括 compact quotient coercivity、endpoint debt 的最小性、
suitable-weak \(s=0\) endpoint、epsilon regularity、任意三维 global
regularity 与 Clay conclusion。

**NOT CLAY.**

## 参考文献

1. I.-J. Jeong and T. Yoneda, *Proc. Amer. Math. Soc.* **150** (2022),
   [DOI](https://doi.org/10.1090/proc/15754),
   [arXiv](https://arxiv.org/abs/2012.14621).
2. A. W. Vreman, *Phys. Fluids* **16** (2004),
   [DOI](https://doi.org/10.1063/1.1785131),
   [author PDF](https://www.vremanresearch.nl/Vreman-PF2004-subgridmodel.pdf).
3. M. Germano, *J. Fluid Mech.* **238** (1992),
   [DOI](https://doi.org/10.1017/S0022112092001733).
4. G. L. Eyink and H. Aluie, *Phys. Fluids* **21** (2009),
   [DOI](https://doi.org/10.1063/1.3266883),
   [arXiv](https://arxiv.org/abs/0909.2386).
5. P. L. Johnson, *Phys. Rev. Lett.* **124** (2020),
   [DOI](https://doi.org/10.1103/PhysRevLett.124.104501),
   [arXiv](https://arxiv.org/abs/1912.00293).
6. J. Duchon and R. Robert, *Nonlinearity* **13** (2000),
   [DOI](https://doi.org/10.1088/0951-7715/13/1/312).
7. L. Caffarelli, R. Kohn, and L. Nirenberg,
   *Comm. Pure Appl. Math.* **35** (1982),
   [DOI](https://doi.org/10.1002/cpa.3160350604).
8. R. Yu, arXiv:2606.25322v1 (2026),
   [record](https://arxiv.org/abs/2606.25322),
   [DOI](https://doi.org/10.48550/arXiv.2606.25322).
