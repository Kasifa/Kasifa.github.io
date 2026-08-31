# R0.73R | A shellwise phase certificate for the critical heat trace

**Status:** analytic proof and literature collision audit passed; finite
certificate, formal figure, and public seal are pending

**Public title (zh):** R0.73R｜能谱看不见的相位：临界热流迹的壳层证书

**Date:** 2026-08-31

**Audience:** researchers and technically trained readers following the
periodic three-dimensional Navier--Stokes notes

**Scope:** one deterministic Fourier interface for the R0.73Q sufficient
heat-flow entrance; no arbitrary-data regularity claim

## 1. 直接结论

R0.73R 把 R0.73Q 的抽象热流入口写成逐壳可核查的量，并准确说明
能谱数据为什么还不够。

对平均零扰动 \(f\)，固定一个光滑周期 Littlewood--Paley 分解，记

\[
 f_j=P_jf,\qquad E_j=\|f_j\|_2,\qquad
 \Theta_j={\|f_j\|_6^6\over E_j^6}.
\]

则

\[
 \boxed{
 \|e^{t\Delta}f\|_{L^4_tL^6_x}
 \asymp
 \left(\sum_{j\ge0}
 2^{-2j}\Theta_j^{2/3}E_j^4\right)^{1/4}
 =
 \left(\sum_{j\ge0}2^{-2j}\|P_jf\|_6^4\right)^{1/4}.}
 \tag{1.1}
\]

这里的 \(\ell^4\) 不是随意选择。上界必须保留热衰减产生的双壳核，
下界则由短时间逆热乘子逐壳恢复。它正是
\(L^4_tL^6_x\) 热流迹对应的临界序列指数。

式 (1.1) 的函数空间内容是经典的周期负指标 Besov 热半群刻画，不是
新定理。R0.73R 的新增工作是把它拆成三种不同成本的有限 Fourier
接口，并给出一个完全同谱、只改相位的严格分离族。

## 2. 三层证书

第一层保留完整相位。若 \(A_{j,m}(k)\) 是第 \(m\) 个分量的 Fourier
系数，令

\[
 T_{j,m}=\sum_{r=1}^3
 A_{j,r}*\widetilde A_{j,r}*A_{j,m},
 \qquad
 \widetilde A_{j,r}(k)=\overline{A_{j,r}(-k)}.
\]

Parseval 给出精确恒等式

\[
 \boxed{\|f_j\|_6^6=\sum_{m=1}^3\|T_{j,m}\|_{\ell^2}^2.}
 \tag{2.1}
\]

这是从有限 Fourier 数据精确求值 \(L^6\) 的办法。它保留相位和极化，
但并不是比 \(L^6\) 更便宜的新先验估计。实现时必须做线性三重卷积；
循环 FFT 若没有充分补零，会把混叠误当成相干性。

第二层只保留支撑的加法几何。设

\[
 R_j=\max_n\#\{(k_1,k_2,k_3)\in S_j^3:
                    k_1+k_2+k_3=n\}.
\]

逐输出频率使用 Cauchy--Schwarz 可得

\[
 \|f_j\|_6\le R_j^{1/6}E_j,
\]

于是

\[
 \|f\|_{\mathfrak X}
 \lesssim
 \left(\sum_j2^{-2j}R_j^{2/3}E_j^4\right)^{1/4}.
 \tag{2.2}
\]

第三层只数活跃 Fourier 位点。若 \(M_j=|S_j|\)，则

\[
 \|f_j\|_6\le M_j^{1/3}E_j,
\]

\[
 \|f\|_{\mathfrak X}
 \lesssim
 \left(\sum_j2^{-2j}M_j^{4/3}E_j^4\right)^{1/4}.
 \tag{2.3}
\]

式 (2.2) 与 (2.3) 是非循环、确定性、可计算的充分上界，但会丢失
相位。任何一个无量纲的 \(R_j\) 或 \(M_j\) 都不能单独给出小量；还需
逐壳加权能量 \(E_j\)。

## 3. 为什么壳指数是四

写 \(b_j=\|P_jf\|_6\) 和 \(a_j=2^{-j/2}b_j\)。LP 平方函数与环带
热衰减给出

\[
 \|e^{t\Delta}f\|_{L_t^4L_x^6}^4
 \lesssim
 \sum_{j,k}{b_j^2b_k^2\over4^j+4^k}.
\]

关键核满足

\[
 {2^{j+k}\over4^j+4^k}\lesssim2^{-|j-k|}.
\]

对 \(a_j^2\) 使用 \(\ell^2\) Young 不等式，正好得到
\(\sum_ja_j^4\)。若一开始逐块使用 Minkowski，会得到过强的
\(\ell^1\)；若过早对平方函数作三角不等式，会得到过强的
\(\ell^2\)。

反方向，在时间窗

\[
 I_j=[A4^{-j},B4^{-j}]
\]

内，逆热乘子的 \(L^6\) 范数一致有界。因此

\[
 2^{-2j}b_j^4
 \lesssim\int_{I_j}\|e^{t\Delta}f\|_6^4dt.
\]

这些时间窗只有有限重叠，求和就得到 (1.1) 的下界。若有 \(n\) 个
壳满足 \(a_j=1\)，热流迹至少按 \(n^{1/4}\) 增长；单独的
\(\ell^\infty\) 壳界不够。

## 4. 同一能谱，不同临界热流迹

令 \(m=2^r\)、\(N=8m\)，并定义 Dirichlet 多项式

\[
 D_m(z)=\sum_{q=0}^{m-1}z^q.
\]

Rudin--Shapiro 多项式由

\[
 P_1=Q_1=1,
 \quad
 P_{2m}=P_m+z^mQ_m,
 \quad
 Q_{2m}=P_m-z^mQ_m
\]

递归生成。它的系数是 \(\pm1\)，并满足

\[
 |P_m|^2+|Q_m|^2=2m,
 \qquad \|P_m\|_\infty\le\sqrt{2m}.
\]

对 \(R_m=D_m\) 或 \(P_m\)，取三维实向量场

\[
 W_{R,m}(x)
 ={\sqrt2\over m}e_3
 \operatorname{Re}\!\left[
 e^{iNx_1}R_m(e^{ix_1})R_m(e^{ix_2})
 \right].
 \tag{4.1}
\]

两族有完全相同的 \(2m^2\) 个 Fourier 位点；每个活跃系数的模都是
\(1/(\sqrt2m)\)。所以它们不仅 \(L^2=1\)，而且所有只依赖
\(|\widehat f(k)|^2\) 的二次 Fourier/Sobolev 范数都逐项相同。

相位却改变了六次相干性。载频消去给出

\[
 \|W_{R,m}\|_6^6
 ={5\over2m^6}\|R_m\|_6^{12}.
 \tag{4.2}
\]

Dirichlet 六次矩可以精确求和：

\[
 \|D_m\|_6^6
 ={11m^5+5m^3+4m\over20}.
 \tag{4.3}
\]

因而

\[
 \|W_{D,m}\|_6\asymp m^{2/3},
 \qquad
 (5/2)^{1/6}\le\|W_{P,m}\|_6\le40^{1/6}.
\]

所有频率都在同一固定比例环带

\[
 N\le|k|\le{\sqrt{82}\over8}N.
\]

环带热乘子与短时间逆乘子于是给出

\[
 \|W_{R,m}\|_{\mathfrak X}
 \asymp N^{-1/2}\|W_{R,m}\|_6.
\]

最终得到

\[
 {\|W_{D,m}\|_{\mathfrak X}
  \over\|W_{P,m}\|_{\mathfrak X}}
 \asymp m^{2/3}.
 \tag{4.4}
\]

这说明：频率支撑、活跃模态数、逐模幅值、能谱、\(L^2\) 和全部
二次 Sobolev 范数都不能决定临界热流入口。必须保留某种高阶相位
信息。

## 5. 同时让 L2 消失

再乘共同振幅

\[
 \alpha_m=N^{1/2}m^{-2/3}=\sqrt8\,m^{-1/6}.
\]

两族同时满足

\[
 \|\alpha_mW_{R,m}\|_2=\alpha_m\to0,
\]

但

\[
 \|\alpha_mW_{D,m}\|_{\mathfrak X}\asymp1,
 \qquad
 \|\alpha_mW_{P,m}\|_{\mathfrak X}\asymp m^{-2/3}\to0.
 \tag{5.1}
\]

它们的半阶 Sobolev 范数仍完全相同，并共同满足

\[
 \|\alpha_mW_{R,m}\|_{\dot H^{1/2}}\asymp m^{1/3}\to\infty.
\]

若要与一个已给定的正热流半径作“进入/不进入”的严格比较，可以再
给两族乘同一个固定常数，并用解析上下界选择该常数。仅凭
\(\asymp1\) 不能擅自排序一个未知半径。

## 6. 这不是危险数据的例子

式 (4.1) 的每个场都形如 \(e_3g(x_1,x_2)\)，所以

\[
 (W_{R,m}\cdot\nabla)W_{R,m}
 =g\,\partial_3(e_3g)=0.
\]

它们的无强迫 Navier--Stokes 演化就是线性热流，始终全局光滑。
Dirichlet 族不进入一个小热流球，并不表示它不安全；只表示 R0.73Q
给出的充分入口不是必要条件。

这个例子也不能推出小 \(L^2\) 数据会奇性。它证明的准确否定命题是：
单靠 \(L^2\) 大小和任意二次能谱信息，无法判断这一临界热流入口。

## 7. 文献边界

一手文献核验关闭了几个潜在的新颖性误区。

- Chemin--Gallagher 2006 已在三维周期域同时给出负指标 thermic
  Besov 定义和 LP 定义；(1.1) 的函数空间等价是经典内容。
- Rudin--Shapiro 平坦性、稀疏频集的 \(\Lambda(p)\) 控制，以及
  Khintchine 随机相位增益都是成熟的调和分析机制。
- Nahmod--Pavlović--Staffilani 2013 已把随机化热流估计用于周期
  超临界 Navier--Stokes 弱解；R0.73R 的区别只在固定、确定性、有限
  可审计的输入。
- 一般谱簇、改进 Sobolev 和三维环面薄谱窗已有深入结果。2025 年的
  三维环面谱投影预印本仍研究窄径向窗，不能直接替代完整 dyadic
  壳的证书。
- 高频振荡大数据导致全局光滑解已有明确先例，不能把 (4.1) 包装成
  “首次利用相位或高频得到大而安全的数据”。

在限定检索中没有找到完全相同的三维散度零 matched pair，但这只
支持“本地精确构造”标签，不构成优先权证明。

## 8. 研究价值与下一道门

我把 R0.73R 的当前价值评为“可靠的桥接引理与反例工具”，而不是
高水平正则性主定理。它有三项可保留价值：

1. 把 R0.73Q 的热流入口拆成能量、加法几何和高阶相位三个清楚层次；
2. 给出可以由有限 Fourier 数据复算的严格证书；
3. 用完全同谱的确定性族证明二次能谱为何不足。

它离高水平主结果还差至少一项实质增量：一个真正低成本的相位敏感
上界、一个带锐常数或极值结构的定理、跨壳热权重的新增益，或者一条
超出现有振荡大数据理论的新 Navier--Stokes 后果。

下一发布门 R0.73S 将优先检查：能否用部分自相关、低阶加法能量或
可分块相位图，构造复杂度明显低于精确三重卷积、同时严格支配
\(\Theta_j\) 的确定性代理量。若做不到，结果应以 no-go 或复杂度
下界形式发布。

## 9. 可复核范围

连续体证明负责 (1.1)、(2.2)、(2.3) 和 matched-family 的渐近界。
有限证书只复算离散支撑、逐模幅值、精确 \(L^2\)、Dirichlet 六次矩、
Rudin--Shapiro 递归和所列有限 \(m\) 的公式行。有限计算不能替代
渐近证明，也不是 Navier--Stokes 仿真。

普通翻译直接在本机完成。R0.73R 的证明、证书和附图也只需本地 CPU；
DGX 未使用。

解析源文件固定在提交
`25b20d225202359de2fd2d95ed86dd4b372d23a5`。19 文件公式证书在提交
`6809fc92a2d1338fb77fb3bf5a72d16ed158d807` 终封；25 文件正式图包在提交
`f3d8ac3b04aa122a44f112d554c4991ecfb6f36e` 终封。两套终封都逐字节绑定
同一解析源提交；该来源链只证明有限公式、数据和制图可复现，不扩大
连续体结论。

## 10. 碰撞边界使用的一手来源

- J.-Y. Chemin and I. Gallagher,
  [*On the global wellposedness of the 3-D Navier--Stokes equations with
  large initial data*](https://www.numdam.org/articles/10.1016/j.ansens.2006.07.002/),
  2006.  Definition 1.1 给 thermic negative Besov 范数；Definition 2.2
  给周期 LP 范数；Theorem 2 构造高频振荡大数据。
- W. Rudin,
  [*Some theorems on Fourier coefficients*](https://doi.org/10.1090/S0002-9939-1959-0116184-5),
  1959，以及
  [*Trigonometric Series with Gaps*](https://iumj.org/article/1263/),
  1960。前者是 Rudin--Shapiro 历史来源之一，后者属于稀疏频集
  \(\Lambda(p)\) 理论背景。
- A. R. Nahmod, N. Pavlović, and G. Staffilani,
  [*Almost Sure Existence of Global Weak Solutions for Supercritical
  Navier--Stokes Equations*](https://epubs.siam.org/doi/10.1137/120882184),
  2013。它给出周期随机化热流估计与几乎处处的超临界弱解。
- P. Gérard, Y. Meyer, and F. Oru,
  [*Inégalités de Sobolev précisées*](https://www.numdam.org/item/SEDP_1996-1997____A4_0/),
  1996--97。Theorem 1 是空间集中度改进 Sobolev 的经典来源。
- P. Germain and S. L. Rydin Myerson,
  [*Bounds for spectral projectors on tori*](https://arxiv.org/abs/2104.13274),
  2022；P. Germain, S. L. Rydin Myerson, and D. Pezzi,
  [*Bounds for spectral projectors on the three-dimensional
  torus*](https://arxiv.org/abs/2508.05573), 2025。这两项是最接近的
  三维环面薄谱窗前沿，但不自动给完整 dyadic 壳的入口证书。

## 11. 发布账本

```text
periodicHeatBesovEquivalence=VERIFIED_CLASSICAL
ell4ShellExponent=CLOSED_AFTER_AUDIT
exactVectorTripleConvolution=CLOSED_EXACT_EVALUATION
additiveMultiplicityCertificate=CLOSED
supportCardinalityCertificate=CLOSED_SHARP_FROM_SUPPORT_ONLY
matchedSupportMagnitudeQuadraticData=CLOSED_EXACT
matchedPhaseHeatTraceSeparation=CLOSED_AFTER_AUDIT
zeroNonlinearityBoundary=CLOSED
exactConvolutionIsCheapAPrioriProxy=FALSE
failureOfEntranceImpliesUnsafeDynamics=FALSE
uniformL2OnlyStrongRadius=OPEN
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
```

```text
formulaCertificateValidation=PASS
formulaCertificatePackage=CLOSED
sourceCommitAssigned=TRUE
finalSeal=TRUE
formalFigurePackage=PASS
publicReleaseContent=READY
translationPath=LOCAL_DIRECT_NO_DGX
```
