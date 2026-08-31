# R0.73O | Global-orbit stability and a forced Kolmogorov contrast

**Status:** continuum mathematics passed independent analytic readback; the finite diagnostic and formal figure packages are source-commit sealed; canonical public content is ready for transactional rendering

**Public title (zh):** R0.73O｜先验全局轨道稳定性与强迫 Kolmogorov 对照

## 1. 直接结论

R0.73O 得到两个边界不同、方向相反的结论。

无强迫方程一侧，每条已经先验全局存在的周期三维 \(H^3\) 强轨道都有有限的累积 \(H^4\) 作用量，并有一个正的 \(H^3\) 同步稳定半径。这个半径依赖固定参考轨道，却对所有起始时刻有效。该结论关闭的是已知全局背景上的 \(H^3\)-小扰动路线，不证明任意三维初值全局。

强迫方程一侧，显式 Kolmogorov 平衡态

\[
 U_*=(30.12\sin 10y,0,0),\qquad
 f_*=(3012\sin 10y,0,0)
\]

在 \(R=3.012\) 时至少有一个正实平面特征值。Friedlander--Pavlović--Shvydkoy 定理先在二维不变子空间中应用，再沿 \(z\) 常数延拓，得到全局光滑、初始 \(H^3\) 范数趋于零、但在某些时刻逃离固定 \(L^2\) 球的三维见证解。

这不是代数简单性结论，不是本质三维不稳定模态，也不能转移到无强迫方程。所有见证解都全局光滑，因此这里没有奇性结论，也没有 Clay 问题的进展声明。

## 2. 无强迫全局轨道的有限作用量

在标准三维环面、黏性系数一、零均值无散度相空间中，考虑

\[
 \partial_tu-\Delta u+P(u\cdot\nabla u)=0
\]

的一条先验全局强解

\[
 u\in C([0,\infty);H^3_{\sigma,0})
 \cap L^2_{\rm loc}([0,\infty);H^4_{\sigma,0}).
\]

能量等式先给出有限的 \(L^2_tH^1_x\) 耗散。轨道随后进入一个通用的小 \(H^1\) 球；\(H^1\to H^2\to H^3\) 的能量阶梯给出高阶指数衰减。带权 \(H^3\) 能量估计进一步推出

\[
 \mathcal A_4[u]
 :=\int_0^\infty |u(t)|_4\,dt<\infty.
\]

有限初始区间使用假设中的 \(L^2_{\rm loc}H^4\)，无限尾部使用指数权重。这个论证依赖参考轨道已经全局存在，不能反过来作为任意局部轨道的全局延拓证明。

## 3. 对全部起始时刻有效的稳定管

令 \(w=v-u\)、\(X=|w|_3^2\)、\(Y=|w|_4^2\)。周期交换子和 Moser 估计给出

\[
 {1\over2}X'+Y
 \le C_*|u|_4X+C_*X^{1/2}Y.
\]

Stokes \(H^3\) 范数中的半径可取为

\[
 R_A[u]
 ={1\over4C_*}\exp\!\bigl(-C_*\mathcal A_4[u]\bigr)>0.
\]

对任意 \(t_0\ge0\)，只要

\[
 |v(t_0)-u(t_0)|_3<R_A[u],
\]

比较解就全局存在，并满足

\[
 |v(t)-u(t)|_3
 \le e^{C_*\mathcal A_4[u]}
 e^{-(t-t_0)/2}|v(t_0)-u(t_0)|_3,
 \qquad t\ge t_0.
\]

通常的非齐次 \(H^3\) 范数与 Stokes 范数等价，因此也得到正的通常 \(H^3\) 半径；固定等价常数会改变数值半径，不能把两个半径写成同一个数。

## 4. 拓扑结论与仍未关闭的输入接口

上述定理给出全三维同步 \((H^3,H^3)\) 稳定，也通过 \(H^3\hookrightarrow L^2\) 给出 \(H^3\)-输入、\(L^2\)-输出的直接推论。初始扰动仍须在 \(H^3\) 中小。

全局强解初值集

\[
 \mathcal G_3
 =\{u_0\in H^3_{\sigma,0}:u_0\text{ 生成全局强解}\}
\]

因此在 \(H^3\) 中是开集。其补集若非空则为闭集。这不证明补集非空，也不证明所有光滑初值都属于 \(\mathcal G_3\)。

尚未关闭的接口是：初值只在 \(L^2\) 中小，而 \(H^3\) 可以任意大时，能否仍得到全局 \(H^3\) 延拓和固定的 \(L^2\) 控制。现有稳定半径不能排除高频、大高阶范数的扰动。

## 5. 强迫 Kolmogorov 平衡态与精确缩放

在同一标准三维环面上考虑带固定外力的方程

\[
 \partial_tu-\Delta u+P(u\cdot\nabla u)=Pf_*.
\]

由于 \(U_*\) 只有依赖 \(y\) 的第一分量，

\[
 (U_*\cdot\nabla)U_*=0,\qquad
 -\Delta U_*=100U_*=f_*.
\]

所以 \(U_*\) 是精确的非衰减平衡态。它还有

\[
 \int_0^\infty\|\nabla U_*\|_{L^\infty}\,dt=\infty.
\]

这只是非恒定稳态不衰减的直接结果，不是湍流或奇性的证据。

取物理纵向波数 \(m=7\)、基流波数 \(N=10\)、振幅 \(A=30.12\) 和黏性系数 \(\nu=1\)。归一化变量给出

\[
 \alpha={m\over N}=0.7,\qquad
 R={A\over\nu N}=3.012,\qquad
 \lambda=AN\sigma=301.2\sigma.
\]

因此文献中的矩形二维环面问题被精确嵌入标准三维立方环面的平面不变子空间，而不是从不同几何或不同参数定义中直接搬用临界值。

## 6. 无限维正实谱的组合证明链

Nagatou 的计算机辅助定理给出

\[
 R_c\in[3.011528364444,\;3.011528364446].
\]

仅有这个临界区间不能决定穿越后的谱方向。R0.73O 使用以下分工明确的组合链。

1. [Nagatou](https://doi.org/10.1016/j.cam.2003.10.016) 证明非负实部特征值都是实数，从而排除非零虚轴穿越。
2. [Matsuda--Miyatake Proposition 1](https://doi.org/10.2748/tmj/1113247600) 给出零特征值递推的唯一中性参数。余弦扇区、平移所得的正弦扇区、负纵向模和 \(m=0\) 规范模分别处理后，这一排除覆盖完整的零均值平面 Fourier 空间。
3. [Ilyin Theorem 5.1](https://doi.org/10.1070/SM2005v196n01ABEH000871) 在 \(L=2\pi\) 的同一归一化下，于某个有限的大 Reynolds 参数提供非空正实谱锚点。
4. 固定零均值无散度 Hilbert 空间上的速度算子构成公共 \(H^2\) 定义域的 type-(A) 解析族，并有紧预解式。能量估计把闭右半平面谱统一限制在一个固定矩形中。虚轴无谱和 Riesz 投影秩的连续性使右半平面总代数重数从高参数锚点保持到 \(R=3.012\)。

由于

\[
 3.012>3.011528364446,
\]

二维无限维线性化算子在目标参数处至少有一个正实特征值。沿 \(z\) 常数延拓后，同一平面特征函数属于完整三维线性化相空间。

被保持的是右半平面 Riesz 投影的秩，即正实部谱的总代数重数。这个论证不证明该特征值代数简单，也不产生本质三维特征模。

## 7. 从正实谱到全局光滑的固定逃逸

[Friedlander--Pavlović--Shvydkoy](https://doi.org/10.1007/s00220-006-1526-7) 的非线性不稳定定理先应用在二维不变相空间，参数取

\[
 n=2,p=2,q=4.
\]

光滑不稳定方向给出二维初始扰动序列 \(w_{0,j}\)，使其在 \(H^3\) 中趋于零，而相应解在某些时刻与平衡态的 \(L^2\) 距离至少为一个固定正数。

再把二维速度场沿 \(z\) 常数延拓。二维平面子空间对非线性方程严格不变，二维周期 Navier--Stokes 的经典全局正则性保证每个见证解全局光滑。固定延拓因子同时作用于 \(H^3\) 和 \(L^2\) 范数，所以三维相空间中存在

\[
 \|w_{0,j}\|_{H^3(\mathbb T^3)}\longrightarrow0,
 \qquad
 \|u_j(t_j)-U_*\|_{L^2(\mathbb T^3)}\ge\rho_*>0.
\]

一个平面序列足以证明完整相空间中的不稳定。这个存在性结论不说明任意非平面扰动全局，也不说明不稳定机制本质上是三维的。

## 8. 有限 Fourier 诊断及其证据边界

截断阶数 \(K=120\) 的主计算在 \(R=3.012\) 得到

\[
 \sigma_{\max}^{(120)}
 =3.7327236415731776\times10^{-5},
 \qquad
 \lambda^{(120)}
 =0.011242963608418411.
\]

等价的机器可读数值是：

~~~text
sigma=3.7327236415731776e-05
lambda=0.011242963608418411
~~~

独立装配的广义特征值铅笔复现了符号、尺度和临界穿越；有限验证器检查了源数据、残差、配置和哈希关系。正式附图以 SVG、矢量 PDF 和 600 dpi PNG 保存，并完成尺寸、灰度与标签检查。

这些结果只用于检查缩放、符号、实现和截断收敛表现。有限矩阵的正特征值不证明无限维算子的正谱，不代替 Nagatou 的严格临界区间，也不单独推出非线性不稳定。无限维结论来自上一节的组合证明链。

## 9. 证据层级与结论账目

| 层级 | 本节内容 | 可以支持的陈述 | 不能支持的陈述 |
| --- | --- | --- | --- |
| 已发表文献 | Pizzocchero、Nagatou、Matsuda--Miyatake、Ilyin、FPS 等定理 | 各自原文量词和本文明确完成的参数对应 | 未核对量词、不同方程或不同拓扑的转移 |
| 内部解析证明 | 无强迫能量阶梯、有限作用量、稳定管；紧预解式与 Riesz 投影延拓 | 在写明假设下的连续体结论 | 任意三维初值全局、代数简单性 |
| 有限诊断 | \(K=120\) 谱值、独立重算、残差与正式附图 | 数值尺度、符号和实现检查 | 无限维谱、非线性逃逸或奇性证明 |
| 开放项 | \(L^2\)-only 高频接口、任意三维初值全局、本质三维模 | 下一步问题的精确定义 | 已完成的数学结论 |

数学结论已经通过独立解析复核。有限诊断的 19 文件证书包和正式附图的 25 文件包均已绑定到不可变源提交 `f139c5e707ffdfe855ca114faac669d12e431e59`，其内部验证与哈希账本同时通过。canonical 公开内容已经就绪；网页仍须按事务顺序生成、翻译、同步 PDF 并做线上字节核对。

## 10. 文献边界

[Pizzocchero 2021](https://doi.org/10.1016/j.aml.2020.106970) 已直接给出周期光滑全局解的稳定半径；Ponce--Racke--Sideris--Titi、Gallagher--Iftimie--Planchon、Hoang--Martinez 等工作也给出相关的稳定、开放性或最终衰减结论。因此无强迫部分定位为当前 \(H^3\) 拓扑下的自包含经典路线闭合，不作 novelty 或 priority 声明。

[Mucha 2001](https://doi.org/10.1006/jdeq.2000.3863) 是周期 \(L^2\)-小扰动问题最接近的碰撞来源，但本次 bounded audit 没有获得其完整定理量词。[Mucha 2008](https://doi.org/10.4064/bc81-0-18) 的可读定理显示其自身的小 \(L^2\) 条件仍依赖高阶迹范数。这不能证明全部文献都不存在统一的 \(L^2\)-only 阈值。

强迫侧没有把十二位临界区间和超临界谱方向归于同一篇文献。临界区间来自 Nagatou；零谱唯一性来自 Matsuda--Miyatake；高参数正谱锚点来自 Ilyin；连续体方向由公共定义域、紧预解式、统一谱界和 Riesz 投影秩完成；非线性逃逸使用 FPS。

## 11. 可直接发布的中文短文

### Lead

无强迫一侧，每条先验全局的周期 \(H^3\) 强轨道都有正的同步稳定管；强迫一侧，一个非衰减 Kolmogorov 平衡态沿平面方向发生全局光滑的固定 \(L^2\) 逃逸。前者是经典路线在当前拓扑下的闭合，后者的无限维正实谱来自组合文献与算子论证明链；有限谱图只作诊断。

### Home

我把固定背景的有限作用量稳定机制推广到任意一条先验全局的无强迫周期 \(H^3\) 轨道，并登记了一个拓扑匹配的强迫 Kolmogorov 对照。两个结论都不改变任意三维初值的全局正则性问题。

### Recap

R0.73O 关闭了已知全局无强迫背景上的 \(H^3\)-小扰动不稳定路线：每条轨道最终衰减，累积 \(H^4\) 作用量有限，并有一个对所有起始时刻有效的正稳定半径。强迫对照保留无限累积应变，并由平面方向给出全局光滑、初始 \(H^3\) 趋零而输出固定 \(L^2\) 逃逸的见证。

### Literature

Pizzocchero 已给出直接的周期稳定定理；Mucha 2001 仍是 \(L^2\)-only 阈值最接近、但完整量词尚未核对的碰撞来源。Kolmogorov 正实谱使用 Nagatou、Matsuda--Miyatake、Ilyin 与标准算子延拓的组合链，非线性逃逸使用 Friedlander--Pavlović--Shvydkoy。

### Next

数学上的下一发布门是 R0.73P：直接检查 \(L^2\)-only / 高频输入接口，确定初始 \(L^2\) 很小而 \(H^3\) 很大时现有稳定管在哪一步失效，并测试哪些可审计的频率局部化条件能够恢复严格控制。

## 12. 精确排除

- 不证明任意三维光滑初值全局。
- 不证明全三维 \(L^2\)-only 输入稳定。
- 不证明目标正特征值代数简单。
- 不证明本质三维不稳定模态。
- 不证明爆破、湍流、异常耗散或非唯一性。
- 不把有限 Fourier 矩阵当作无限维谱证书。
- 不把带外力的对照转移到无强迫 Clay 方程。
- 不作新颖性或优先权声明。

精确公开标签是 **NOT CLAY**。

## 13. 机器账本

~~~text
unforcedGlobalOrbitH3Stability=CLOSED_CONDITIONALLY_AFTER_AUDIT
unforcedFiniteAccumulatedH4=CLOSED_CONDITIONALLY_AFTER_AUDIT
globalDataSetH3Open=CLOSED_AS_COROLLARY
unforcedH3InputL2Output=CLOSED_AS_COROLLARY
uniformL2OnlyInputThreshold=OPEN_COLLISION_SENSITIVE
arbitraryThreeDimensionalGlobalRegularity=OPEN
forcedKolmogorovPositivePlanarSpectrum=CLOSED_BY_COMPOSITE_PRIMARY_SOURCE_CHAIN_AFTER_AUDIT
forcedKolmogorovH3InputL2Escape=CLOSED_BY_COMPOSITE_PRIMARY_SOURCE_CHAIN_AFTER_AUDIT
forcedWitnessSolutionsGlobalSmooth=PLANAR_ONLY
positiveEigenvalueAlgebraicallySimple=OPEN_NOT_CLAIMED
essentiallyThreeDimensionalUnstableMode=OPEN_NOT_NEEDED
forcedConclusionTransfersToClay=FALSE
finiteFourierDiagnostic=PASS
finiteComputationProvesInfiniteDimensionalSpectrum=FALSE
finiteComputationProvesNonlinearInstability=FALSE
finiteComputationReplacesNagatouCertificate=FALSE
finiteDiagnosticValidation=PASS
finiteDiagnosticPackage=CLOSED
sourceCommitAssigned=TRUE
finalSeal=TRUE
formalFigurePackage=PASS
publicReleaseContent=READY
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
~~~
