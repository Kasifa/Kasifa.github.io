# R0.71O 一手文献核查：soft denominator、零分母 faces 与 BV 极限

**核查日期：2026-08-26**

**性质：bounded primary-source audit。本文献核查不是原创性、优先权或不存在性证明。**

## 1. 核查对象与项目边界

R0.71O 考察一个固定 shell、固定物理单元和固定 cutoff 上的软分母

\[
 R_\varepsilon=\sqrt{d+\varepsilon},\qquad
 z_\varepsilon=\frac{B}{\sqrt YR_\varepsilon},\qquad
 a_\varepsilon=(z_\varepsilon^+)^2
 =\frac{(B^+)^2}{Y(d+\varepsilon)},
 \tag{1.1}
\]

其中

\[
 B=\langle F,C\rangle,\qquad d=\|C\|_2^2,
 \qquad Y=\|\omega\|_2^2>0.
 \tag{1.2}
\]

检索只问四件事：

1. BV 弱星、strict 与 area-strict 收敛分别能保留什么；
2. \(C/|C|\) 在零点附近的光滑正则化、coarea 与 crossing 公式能否识别一侧 face；
3. 周期 Navier--Stokes 经典强解的时间解析性能否保证固定投影零点为有限阶；
4. 是否已有定理直接处理 (1.1) 的正负一侧 face measures，并从 NSE 能量与 denominator mass 支付其总和。

R0.71O 自身在孤立经典有限阶零点

\[
 C(t_0+\tau)=c\tau^m+O(|\tau|^{m+1}),\qquad
 C_t(t_0+\tau)=mc\tau^{m-1}+O(|\tau|^m),\qquad c\ne0,
 \tag{1.3}
\]

下得到一侧 trace 与软层测度。这些公式是本项目的代数和一维渐近结论，不是下列文献中的定理。文献核查的作用是确定它们与既有 BV、crossing 和时间解析性工具的精确重叠范围。

## 2. 一手来源、直接重叠与缺口

| 一手来源 | 已核对的定理、页码或公式 | 与 R0.71O 的直接重叠 | 不能从该来源推出的结论 |
|---|---|---|---|
| Reshetnyak, *The weak convergence of completely additive vector-valued set functions*, [MathNet 原文与英译信息](https://www.mathnet.ru/eng/smj5605), [DOI](https://doi.org/10.1007/BF02196453), Siberian Math. J. 9 (1968), 1039--1045；Spector, *Simple proofs of some results of Reshetnyak*, [作者库 PDF](https://cvgmt.sns.it/media/doc/paper/505/reshetnyakcontinuityrevised.pdf) | Spector Theorem 1.3，printed p.3：\(\mu_n\stackrel*\rightharpoonup\mu\) 且 \(|\mu_n|(\Omega)\to|\mu|(\Omega)\) 时，连续有界的 polar integrand 积分收敛。Theorem 1.6，p.5，及 Theorem 1.7，p.7：对下半连续、凸、正一齐次 integrand 给出 liminf 结论。 | 明确区分弱星下半连续与 strict convergence 下的一齐次连续性。它解释了为什么 signed derivative 的弱极限可以小于近似序列的总变差。 | strict convergence 本身不识别 \(a_\varepsilon\) 在同一点坍缩的正、负两颗原子，也不自动控制非一齐次 area energy。 |
| Kristensen--Rindler, *Relaxation of signed integral functionals in BV*, [期刊原文页](https://link.springer.com/article/10.1007/s00526-009-0250-5), Calc. Var. PDE 37 (2010), 29--62 | Theorem 4 是 generalized Reshetnyak continuity theorem。对 \(\mu=(d\mu/dx)\mathcal L^n+\mu^s\)，area functional 为 \(\langle\mu\rangle(\Omega)=\int_\Omega\sqrt{1+|d\mu/dx|^2}\,dx+|\mu^s|(\Omega)\)；area-strict 是弱星收敛加该量收敛。 | area-strict 对有连续 strong recession function 的线性增长 integrand 提供连续性；这是保留非一齐次软能量信息的相邻正确拓扑。 | R0.71O 没有证明 \(Da_\varepsilon\) 的 area-strict 紧性。area-strict 也不把一个一般 concentration measure 自动识别为 denominator-zero face measure。 |
| Alibert--Bouchitté, *Non-Uniform Integrability and Generalized Young Measures*, [期刊原文 PDF](https://www.heldermann-verlag.de/jca/jca04/jca04006.pdf), J. Convex Anal. 4 (1997), 129--147 | Theorem 2.5，printed pp.132--133：有界 \(L^1\) 序列经子列产生 oscillation law \(\nu_x\)、concentration measure \(m\) 与 concentration-direction law \(\nu_x^\infty\)。式 (3.3)，p.134，给出带 \(|u_n|\phi(u_n/|u_n|)\) 的方向浓缩表示。Theorem 2.9(ii)，pp.133--134，将弱局部 \(L^1\) 收敛与 concentration term 的消失对应起来；式 (4.13)，p.140，识别 non-uniform-integrability mass；Theorem 5.1，pp.140--141，给出带 recession/concentration 项的 liminf 结构。 | 为“signed weak limit 发生抵消而 Jordan mass 留下 defect”提供标准 measure-valued 语言，并清楚分开 oscillation 与 concentration。 | \(m\) 依赖子列和所选生成序列；文献没有证明它等于 R0.71O 的 \(A_\pm\delta_{t_0}\)，也没有 NSE shell--cell 支付。 |
| Vol'pert, *The spaces BV and quasilinear equations*, [MathNet 原文](https://www.mathnet.ru/eng/sm4127), Math. USSR-Sb. 2 (1967), 225--267；Ambrosio--De Lellis--Malý, *On the chain rule for the divergence of BV-like vector fields*, [作者 PDF](https://www.math.ias.edu/delellis/sites/math.ias.edu.delellis/files/chain100.pdf) | Ambrosio--De Lellis--Malý Theorem 1，printed p.10，重述 Vol'pert chain rule：对有限维 \(v\in BV_{\rm loc}\) 与 \(C^1\) 且梯度有界的 \(\Phi\)，\(D(\Phi\circ v)\) 分成 absolutely continuous、Cantor 与 jump 三部分。 | 对每个固定 \(\varepsilon>0\)，\(\Phi_\varepsilon(C)=C/\sqrt{|C|^2+\varepsilon}\) 光滑，且 \(D\Phi_\varepsilon(C)[H]=H/R_\varepsilon-C(C\cdot H)/R_\varepsilon^3\)。有限维 BV 截断可直接套用；经典 Hilbert-valued 时间路径则可直接微分。 | \(\|D\Phi_\varepsilon\|\le\varepsilon^{-1/2}\)，常数随 \(\varepsilon\downarrow0\) 爆炸。该定理不给 uniform BV、face atom 或无限维 BV 链式法则的无条件版本。并且 \(E_\varepsilon=C/R_\varepsilon\) 不是单位向量，\(I-E_\varepsilon\otimes E_\varepsilon\) 不是正交投影。 |
| Fleming--Rishel, *An integral formula for total gradient variation*, [期刊原文](https://link.springer.com/article/10.1007/BF01236935), Arch. Math. 11 (1960), 218--222 | 论文的核心 coarea 公式为 \(|Du|(\Omega)=\int_{\mathbb R}{\rm Per}(\{u>y\},\Omega)\,dy\)。 | 可把一个已经控制的总变差转换为几乎处处 level 的积分周长；一维时对应 level crossing 的积分计数。 | 它积分所有 level，不从 Leray energy 单独产生指定 level \(d=0\) 的界。又因 \(d=\|C\|^2\ge0\)，\(d=0\) 不是通常的符号横截 level。 |
| Łochowski, *On a generalisation of the Banach indicatrix theorem*, [arXiv:1503.01746v4](https://arxiv.org/abs/1503.01746v4), [PDF](https://arxiv.org/pdf/1503.01746v4) | Theorem 1，printed pp.4--5，式 (6)--(8)：对 regulated \(f\) 和 \(c>0\)，\({\rm UTV}^c=\int u_c^y\,dy\)、\({\rm DTV}^c=\int d_c^y\,dy\)、\({\rm TV}^c=\int n_c^y\,dy\)。Remark 1.5，p.4，给出 truncated variation 的一致逼近变分表征。 | 分开 upcrossing、downcrossing 与 total crossing，和 R0.71O 必须分开正、负一侧 faces 的 bookkeeping 相邻。 | 它需要先有 truncated variation 控制，并仍对 level 积分；不提供零 level 的 NSE 计数、横截性或能量支付。 |
| Temam, *Navier--Stokes Equations and Nonlinear Functional Analysis*, 2nd ed., [SIAM Chapter 7](https://epubs.siam.org/doi/10.1137/1.9781611970050.ch7) | Theorem 7.1，p.51：在书中周期盒/有界域框架内，\(u_0\in V\)、时间无关 \(f\in H\) 的强解在正时间是 \(D(A)\)-值解析函数。二维覆盖全部正时间；三维只覆盖局部强解存在区间 \((0,T^\#)\)。Remarks 7.1--7.2，p.56，分别限制三维弱解到其 \(H^1\)-regularity 最大区间，并允许解析的时间依赖力。 | 固定有界线性投影 \(C_Q(t)\) 在经典区间内解析。若它不恒等为零，则内部零点孤立且有限阶；在紧含于该区间的闭子区间上零点有限。 | 不跨潜在奇性时刻；不排除某个投影因对称性恒等为零；不给不同解、shell、cell 间统一的零点数、零阶、间距或横截性。 |
| Giga--Jo--Mahalov--Yoneda, *On time analyticity of the Navier--Stokes equations in a rotating frame with spatially almost periodic data*, [期刊原文页](https://www.sciencedirect.com/science/article/abs/pii/S0167278908000985), Physica D 237 (2008), 1422--1428 | Theorem 1.1 给出 \(FM_0\)-值局部 mild solution 的时间全纯性；Theorem 1.2 在无旋转时给出 \(BUC\)-值解析性；Theorem 1.4 由前两者推出 almost-periodic Fourier amplitude 的解析性和 no sudden creation of a mode。 | 独立确认固定 Fourier amplitude 在其解析区间的零点结构，并覆盖 periodic data 作为 almost-periodic data 的特例。 | “no sudden creation”只排除一个 mode 在整个开时间段恒零后突然出现；不排除孤立过零。物理 cutoff 后的 \(C_Q\) 也不是单个 Fourier amplitude。 |

## 3. strict、area-strict 与 face defect 不能混同

ordinary strict convergence 不推出 area-strict convergence。一个直接例子是在 \((0,1)\) 上令非负密度 \(f_n\) 在每个快速小周期的两半分别取 \(0\) 和 \(2\)。则

\[
 f_n\,dx\stackrel*\rightharpoonup dx,
 \qquad \int_0^1f_n\,dx=1,
\]

所以它 strict 收敛；但

\[
 \int_0^1\sqrt{1+f_n^2}\,dx
 \longrightarrow\frac{1+\sqrt5}{2}
 \ne\sqrt2.
\]

因此它不 area-strict 收敛。这个例子只说明拓扑的严格区分，不是 R0.71O 的 NSE 反例。

在 R0.71O 的有限阶零点，设

\[
 b=\langle F(t_0),c\rangle,\qquad q=\|c\|^2,
\]

则项目内计算得到

\[
 A_+=\frac{(b^+)^2}{Y_0q},
 \qquad
 A_-=\frac{(((-1)^mb)^+)^2}{Y_0q}.
 \tag{3.1}
\]

signed derivative 的面原子为 \((A_+-A_-)\delta_{t_0}\)，而正、负 Jordan atoms 分别为 \(A_+\delta_{t_0}\) 与 \(A_-\delta_{t_0}\)。当两侧都活跃时，普通 hard-limit BV 只看到 \(|A_+-A_-|\)，soft relaxed layer 保留 \(A_++A_-\)，差为

\[
 2\min(A_+,A_-).
 \tag{3.2}
\]

Reshetnyak、area-strict 和 generalized Young-measure 理论说明这种 defect 应如何分类；它们没有给出 (3.1)--(3.2) 或其 NSE 总和估计。

## 4. raw split 的文献边界

在一个 active half-face 上，R0.71O 的直接 source/radial 拆分有

\[
 \int\mathsf S_\varepsilon\,dt
 =\gamma^2\log\!\left(1+\frac X\varepsilon\right)+O(1),
 \tag{4.1}
\]

\[
 \int\mathsf R_\varepsilon\,dt
 =-\gamma^2\left[
 \log\!\left(1+\frac X\varepsilon\right)
 -\frac X{X+\varepsilon}\right]+O(1).
 \tag{4.2}
\]

两项的 total masses 分别按相反符号对数发散。只有保留 joint form 后，主部才是

\[
 \gamma^2\frac X{X+\varepsilon}\longrightarrow\gamma^2.
 \tag{4.3}
\]

这不是 Vol'pert、coarea 或 crossing 公式的直接实例。它首先是本项目的 exact cancellation statement；已有 BV 文献只说明为什么不能先逐项取绝对值再期待稳定的测度极限。

## 5. 检索范围与 bounded negative finding

截至 **2026-08-26**，限定检索只使用论文原文、arXiv/作者预印本、作者页面、期刊原文和出版社专著页面。关键词与反向公式检索包括：

- `C/sqrt(|C|^2+epsilon)`、`normalized vector field`、`zero set measure`；
- `soft denominator`、`defect measure`、`source measure`、`one-sided face`；
- `sqrt(d+epsilon)`、`(B^+)^2/(Y(d+epsilon))`；
- `coarea`、`level crossing`、`upcrossing`、`downcrossing`；
- `Navier-Stokes time analytic`、`finite projection zero`、`mode creation`。

在这一有界检索中，**未定位到**同时完成下列两件事的一手定理：

1. 对 \((B^+)^2/[Y(d+\varepsilon)]\) 的 \(\varepsilon\downarrow0\) 极限识别 \(A_\pm\) 两个一侧 Jordan face atoms；
2. 从三维 NSE 的 Leray energy 加现有 denominator-mass budget，统一支付所有 shell--cell faces。

这只能写成 **bounded negative finding**。它不能写成“没有相关定理”“首次”“原创”“优先结果”或一般 no-go。它也不排除不同术语、非公开稿、未索引文献或一个尚未识别的 NSE 特定全和抵消。

## 6. 可使用的表述边界

可审计的表述是：

> 既有一手来源分别覆盖 fixed-\(\varepsilon\) BV chain rule、strict/area-strict 连续性、generalized Young-measure concentration、coarea/crossing 表示和经典强解的时间解析性。在截至 2026-08-26 的限定检索中，未定位到把这些工具合并为 R0.71O 精确 soft-denominator 一侧 face-measure 公式并支付其 NSE frame--cell 总和的直接定理。

R0.71O 证明的是固定单元的软硬恒等式、有限阶一维 face 渐近、一个抽象 Hilbert-path 功能空间分离和一个一侧 NSE 初始 jet。它不证明内部 NSE face-count 定理、统一 face sum、continuation criterion、有限时奇性或全局正则性。
