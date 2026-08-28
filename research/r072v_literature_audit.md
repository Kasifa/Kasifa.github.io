# R0.72V 文献审计：非自治三次碰撞的全直线图范数边界

**检索日期：** 2026-08-28
**审计性质：** 有界的一手文献检索；不是新颖性、首创性或优先权证明。

---

## 1. 本节究竟证明了什么

R0.72V 研究固定正时间块

\[
I=(-T,T),\qquad T>0,
\]

上的非自治算子

\[
P_{c,\sigma}
=\partial_t-i\sigma\bigl[x^3+6(c+t)x\bigr],
\qquad c\in\mathbb R,\quad \sigma\in\{-1,1\}.
\tag{1.1}
\]

其核心结论是中心一致的全直线图范数估计

\[
\|v\|_{L^2(I\times\mathbb R)}
\le C_T\left(
\|v_x\|_{L^2(I\times\mathbb R)}
+\|P_{c,\sigma}v\|_{L^2(I;H^{-1}(\mathbb R))}
\right),
\tag{1.2}
\]

其中 \(C_T\) 与 \(c\) 和 \(\sigma\) 无关。它不是由每个时刻的冻结算子
semigroup 估计拼接而来；证明链是：

1. 在单位区间 \(J=(-1/2,1/2)\) 上，对

   \[
   Q_{a,b,\sigma}
   =\partial_t-i\sigma\bigl[y^3+ay^2+(b+6t)y\bigr]
   \tag{1.3}
   \]

   直接证明对全部 \((a,b)\in\mathbb R^2\) 一致的图范数估计；
2. 将全直线分成互不相交的单位区间 \(J_k\)。平移 \(x=k+y\) 后，
   二次、一次系数正好是 \(a_k=3k\)、\(b_{k,c}=3k^2+6c\)，而纯时间项由
   标量酉规范消去；
3. 使用精确负 Sobolev 直和不等式

   \[
   \sum_{k\in\mathbb Z}
   \|g|_{J_k}\|_{H_D^{-1}(J_k)}^2
   \le \|g\|_{H^{-1}(\mathbb R)}^2
   \tag{1.4}
   \]

   对单位坐标片估计平方求和，直接得到 (1.2)。

因此，本文献审计的判断标准不是“某篇论文是否证明过三次势的衰减”，而是更严格的：
它是否已经给出 **非自治、全直线、对碰撞中心一致、允许 \(H^{-1}\) 非齐次残差的图范数定理**。
下列近邻结果均不满足这四项的完整组合。

### 1.1 Maximal graph space 与 all-\(L^2\) 能量演化不是同一结论

估计 (1.2) 的适用域是 maximal distributional graph space

\[
\mathcal G_{c,\sigma}(I)
=\left\{
v\in L^2(I;H^1(\mathbb R)):
P_{c,\sigma}v\in L^2(I;H^{-1}(\mathbb R))
\text{ in }\mathcal D'(I\times\mathbb R)
\right\}.
\]

这里 \(v_t\) 与无界虚势项只要求作为整体 \(P_{c,\sigma}v\) 落在负空间；不要求两项
分别属于 \(L^2H^{-1}\)。Maximal graph membership 本身不提供
\(C(\overline I;L^2)\) 时间迹，也不提供全局能量恒等式。

R0.72V 的 all-\(L^2\) 结论来自另一条独立的解析步骤：对每个
\(u_-\in L^2(\mathbb R)\)，先截断实值多项式势，利用一致能量界和局部
Aubin--Lions 紧性取极限，再以空间 cutoff 恢复全局能量恒等式和唯一性。由此得到唯一

\[
u\in C(\overline I;L^2(\mathbb R))
\cap L^2(I;H^1(\mathbb R)),
\qquad
P_{c,\sigma}u=u_{xx},
\]

并且

\[
\|u(t_2)\|_2^2
+2\int_{t_1}^{t_2}\|u_x(t)\|_2^2\,dt
=\|u(t_1)\|_2^2.
\]

该已构造的能量解属于 graph space，因此可代入 (1.2) 得到 observability，继而得到严格
固定块收缩。准确边界是：

- all-\(L^2\) energy evolution 与 block contraction 对精确三次标量模型成立；
- observability 是 graph theorem 对满足方程之 graph-class 解的先验结论；
- 时间迹、能量律和 block contraction 不能从任意 maximal graph element 自动推出。

### 1.2 Fourier 归一化说明

按

\[
\widehat u(\xi)=\int_{\mathbb R}e^{-ix\xi}u(x)\,dx
\]

的约定，若 \(\sigma=1\) 且耗散方程写成

\[
\left[\partial_t-i\bigl(x^3+6a(t)x\bigr)\right]u=u_{xx},
\tag{1.5}
\]

则其 Fourier 对偶是

\[
\partial_t\widehat u
=\partial_\xi^3\widehat u
-6a(t)\partial_\xi\widehat u
-\xi^2\widehat u.
\tag{1.6}
\]

若原势写成 \(x^3+a(t)x\) 而没有系数 6，则 (1.6) 中的平移漂移应相应写成
\(-a(t)\partial_\xi\)。这一系数归一化不能混用。R0.72V 对应
\(a(t)=c+t\)。

### 1.3 短时间结论只有下界

R0.72V 的精确核测试族只证明

\[
C_T\ge c_fT^{-1/3},
\qquad 0<T\le1.
\]

这是每一个可行 graph constant 的 **下界**，只说明 \(C_T\) 不可能在
\(T\downarrow0\) 时保持有界。当前单位坐标片证明没有给出
\(C_T\lesssim T^{-1/3}\)，也没有证明 sharp asymptotic 或相应收缩间隙的精确阶。

---

## 2. 最接近的 enhanced-dissipation 与虚势结果

### 2.1 Li--Zhang：非有界横截面的自治有限型剪切

T. Li and L. Zhang, “Enhanced dissipation and Taylor dispersion by a parallel
shear flow in an infinite cylinder with unbounded cross section,” preprint
(2025).

- 一手来源：[arXiv:2510.13097](https://arxiv.org/abs/2510.13097)
- arXiv DOI：[10.48550/arXiv.2510.13097](https://doi.org/10.48550/arXiv.2510.13097)
- 可使用的准确内容：Theorem 1.1 处理一维无界横截面上的固定算子

  \[
  H_{\nu,k}=-\nu\partial_y^2+ikv(y).
  \]

  若 \(v\in C^m\)，其一至 \(m\) 阶导数不同时为零，并且
  \(\liminf_{|y|\to\infty}|v'(y)|>0\)，则得到

  \[
  \|e^{-tH_{\nu,k}}\|
  \lesssim e^{-c\lambda_{\nu,k}t},\qquad
  \lambda_{\nu,k}=
  \begin{cases}
  \nu^{m/(m+2)}|k|^{2/(m+2)},&\nu\le |k|,\\
  k^2/\nu,&|k|\le\nu.
  \end{cases}
  \]

  对每个固定 \(a\)，剖面 \(v_a(y)=y^3+6ay\) 可取 \(m=3\)，因而给出
  \(\nu^{3/5}|k|^{2/5}\) 的自治基准。
- **Why not a substitute：** 该定理固定一个 \(v\)，其常数在陈述中允许依赖该剖面；它没有断言
  对全部 \(a\in\mathbb R\) 一致，更没有处理 \(a=a(t)\)。结论是齐次自治 semigroup
  衰减，而不是带 \(L_t^2H_x^{-1}\) 残差的非自治图范数估计。逐时应用于
  \(v_{c+t}\) 只得到冻结信息，不能控制时间有序传播子，也不能替代 R0.72V 的
  coefficient-uniform unit charts 与 (1.4)。

### 2.2 Arnaiz--Bony--Michel：纯虚半经典势的谱与演化

V. Arnaiz, J.-F. Bony, and L. Michel, “Semiclassical Schrödinger operators
with purely imaginary potential,” preprint (2026).

- 一手来源：[arXiv:2607.07301](https://arxiv.org/abs/2607.07301)
- arXiv DOI：[10.48550/arXiv.2607.07301](https://doi.org/10.48550/arXiv.2607.07301)
- 可使用的准确内容：论文研究

  \[
  P_h=-h^2\Delta+iV(x),
  \]

  在有界域上的低端谱、resolvent 与 eigenmode expansion；临界点附近由次数
  \(\alpha_c>1\) 的齐次多项式模型控制。相应半经典指数为
  \(\sigma_c=2\alpha_c/(\alpha_c+2)\)。三次模型
  \(\alpha_c=3\) 给出 \(h^{6/5}\)，与剪切重标度后的
  \(\nu^{3/5}|k|^{2/5}\) 一致。论文也独立分析全空间单项式模型的最大增生性、
  谱和 resolvent。
- **Why not a substitute：** 主演化定理针对固定 \(V\) 的自治算子；全空间三次算子在其中是
  局部/模型算子，而不是随 \(t\) 穿过临界点碰撞的全直线图问题。该文没有
  \(L_t^2H_x^{-1}\) 非齐次估计，也没有 R0.72V 所需的 \((a,b)\)-一致单位坐标片定理或
  负 Sobolev 直和全球化。它严格校准 \(3/5\) 标度，但不直接推出 (1.2)。

### 2.3 Coti Zelati--Gallay：有界横截面的自治 resolvent/hypocoercivity

M. Coti Zelati and T. Gallay, “Enhanced dissipation and Taylor dispersion in
higher-dimensional parallel shear flows,” *Journal of the London
Mathematical Society* 108 (2023), 1358--1392.

- 一手来源：[arXiv:2108.11192](https://arxiv.org/abs/2108.11192)
- 期刊 DOI：[10.1112/jlms.12782](https://doi.org/10.1112/jlms.12782)
- 可使用的准确内容：固定平行剪切、无限长圆柱但有界横截面；通过薄层集
  resolvent estimate 与定量 Gearhart--Prüss，或直接通过 hypocoercivity，统一描述
  enhanced-dissipation 与 Taylor-dispersion 两个频率区间。
- **Why not a substitute：** 横截面是有界的，剪切剖面不随时间改变。其薄层集常数和
  resolvent 都属于单个自治生成元；它没有穿过临界点出生--合并--消失的参数族，也没有
  全直线 \(H^{-1}\) 直和图范数结论。它是 Li--Zhang 的有界域方法先例，不是 (1.2)
  的现成证明。

---

## 3. 最接近的非自治剪切结果

### 3.1 Coble--He：缓慢运动且保持非退化的临界点

D. Coble and S. He, “A Note on Enhanced Dissipation and Taylor Dispersion of
Time-dependent Shear Flows,” *Communications in Mathematical Sciences* 22
(2024), no. 6, 1685--1700.

- 一手来源：[arXiv:2309.15738](https://arxiv.org/abs/2309.15738)
- 期刊 DOI：[10.4310/CMS.2024.v22.n6.a10](https://doi.org/10.4310/CMS.2024.v22.n6.a10)
- 可使用的准确内容：
  - Theorem 1.1 在 \(\mathbb T\times\mathbb R\) 的单调情形要求
    \(\inf_{t,y}|\partial_yV|>0\) 及 \(V\in L_t^\infty W_y^{3,\infty}\)，给出
    \(\nu^{1/3}|k|^{2/3}\) 衰减；
  - Theorem 1.2 在二维环面上要求 \(V\) 与参考剪切 \(U\) 共享固定有限数目 \(N\)
    的非退化临界点，临界点有固定半径、两两不交的邻域，并要求
    \(\|\partial_{ty}U\|_\infty\le\nu^{3/4}\)；
  - Theorem 1.3 在有界横截面长通道的低频
    \(0<|k|\le\nu\) 中允许每个时刻有限多个临界点，但要求
    \(\|\partial_{ty}V\|_\infty\lesssim\nu\)，结论是 Taylor dispersion。
- **Why not a substitute：** 对 \(V(t,x)=x^3+6(c+t)x\)，当 \(c+t<0\) 时有两个简单
  临界点，\(c+t=0\) 时合并成退化临界点，\(c+t>0\) 时无临界点。因而单调定理、固定
  \(N\)、非退化、固定分离邻域均在碰撞处失效；此外三次剖面不属于
  \(W^{3,\infty}(\mathbb R)\)。有界通道的低频 Taylor-dispersion 定理既不是全直线
  enhanced dissipation，也要求黏性尺度的缓慢时间变化。Coble--He 证明“非自治可以做”，
  但其假设刻意避开 R0.72V 的临界点碰撞。

### 3.2 Benthaus--Coclite--Nobili：刚性平移的临界点

J. Benthaus, G. M. Coclite, and C. Nobili, “Mixing and enhanced dissipation in
a time-translating shear flow,” preprint (2026).

- 一手来源：[arXiv:2603.14624](https://arxiv.org/abs/2603.14624)
- arXiv DOI：[10.48550/arXiv.2603.14624](https://doi.org/10.48550/arXiv.2603.14624)
- 可使用的准确内容：论文在环面上研究
  \(v(y,t)=\alpha\sin(y-ct)\)。Theorem 1 是有限 pre-unmixing 时间窗内“时间平均解”的
  \(H_y^{-1}\) mixing estimate；Theorem 2 在
  \(c=c_0\nu^\ell\)、\(\ell\in(1/3,3/4)\) 时，通过扩展的非自治 hypocoercive
  functional 得到 \(\nu^{(1+2\ell)/5}\) 衰减；快速平移时，Theorem 3 反而证明固定时间内
  接近热方程。
- **Why not a substitute：** 正弦剖面的临界点始终保持简单、数目不变，并只作刚性平移；
  不发生临界点合并、退化或消失。速度还受特殊黏性幂律约束。该文的 \(H^{-1}\) 对象是
  时间平均后的解，不是 R0.72V 中的 \(H^{-1}\) 图残差。它尤其说明时间运动可能改变衰减率，
  因而反对“冻结谱隙自动拼接”的推理；但它不提供 (1.2)。

---

## 4. 为什么自治 resolvent-to-semigroup 定理不能完成时间拼接

### 4.1 Wei 2020

D. Wei, “Diffusion and mixing in fluid flow via the resolvent estimate,”
*Science China Mathematics* 63 (2020).

- 一手来源：[arXiv:1811.11904](https://arxiv.org/abs/1811.11904)
- 期刊 DOI：[10.1007/s11425-018-9461-8](https://doi.org/10.1007/s11425-018-9461-8)
- 可使用的准确内容：Theorem 1.3 对单个 \(m\)-accretive 算子 \(H\) 给出锋利的
  Gearhart--Prüss 型估计

  \[
  \|e^{-tH}\|\le
  \exp\{-t\Psi(H)+\pi/2\},
  \qquad
  \Psi(H)=\left(\sup_{\lambda\in\mathbb R}
  \|(H-i\lambda)^{-1}\|\right)^{-1}.
  \]

- **Why not a substitute：** 该定理的对象是一个固定生成元 \(H\) 及其自治 semigroup。
  对 \(H(t)\) 逐时控制 \(\Psi(H(t))\)，并不能控制时间有序传播子
  \(U(t,s)\)：不同时间的生成元一般不交换，冻结基底或 resolvent 的时间变化会产生额外项。
  Wei 的定理没有非自治误差项，也没有给出 (1.2) 的空间--时间图范数。R0.72V 因而没有把
  Wei 定理作“冻结后逐块调用”。

### 4.2 Helffer--Sjöstrand 2021

B. Helffer and J. Sjöstrand, “Improving semi-groups bounds with resolvent
estimates,” *Integral Equations and Operator Theory* 93 (2021), Paper 36.

- 一手来源：[arXiv:2103.06792](https://arxiv.org/abs/2103.06792)
- 期刊 DOI：[10.1007/s00020-021-02652-6](https://doi.org/10.1007/s00020-021-02652-6)
- 可使用的准确内容：重新推导并改进 Gearhart--Prüss--Hwang--Greiner 型结论，给出
  semigroup norm 关于生成元 resolvent bounds 的显式估计，并讨论常数优化。
- **Why not a substitute：** 与 Wei 一样，定理以固定生成元及其 semigroup 为对象。
  它不把一族冻结 resolvent bounds 自动提升为非自治传播子估计，也不处理临界点拓扑变化、
  \(H^{-1}\) 非齐次残差或单位坐标片直和。它可用于自治比较，但不是 R0.72V 的时间拼接定理。

### 4.3 方法学结论

Li--Zhang、Coti Zelati--Gallay、Wei 与 Helffer--Sjöstrand 可以组成一条严谨的
**自治**路线：有限型/薄层集 coercivity \(\Rightarrow\) resolvent bound
\(\Rightarrow\) semigroup decay。缺失的箭头恰好是

\[
\left\{\text{对每个 }t\text{ 的冻结估计}\right\}
\centernot\Longrightarrow
\left\{\text{非自治 }U(t,s)\text{ 的一致收缩}\right\}.
\tag{4.1}
\]

R0.72V 绕开 (4.1)，直接在整个时间块上证明图范数 coercivity，再把它代入另行构造的
实际能量解；graph theorem 本身不负责产生该能量演化。这是与上述自治工具最重要的逻辑
区别。

---

## 5. Imaginary cubic 与 complex Airy 的一手模型文献

### 5.1 Henry：恰好包含三次加一次虚势

R. Henry, “Spectral Projections of the Complex Cubic Oscillator,”
*Annales Henri Poincaré* 15 (2014).

- 一手来源：[arXiv:1310.4629](https://arxiv.org/abs/1310.4629)
- 期刊 DOI：[10.1007/s00023-013-0292-2](https://doi.org/10.1007/s00023-013-0292-2)
- 可使用的准确内容：研究固定参数 \(\alpha\ge0\) 的精确模型

  \[
  -\frac{d^2}{dx^2}+ix^3+i\alpha x,
  \]

  并证明第 \(n\) 个谱投影满足
  \(\lim_{n\to\infty}n^{-1}\log\|\Pi_n(\alpha)\|=\pi/\sqrt3\)。这是该三次族强非正规性与
  谱不稳定性的直接证据。
- **Why not a substitute：** 结论是固定 \(\alpha\) 的高能谱投影渐近，不是 semigroup decay，
  更不是 \(\alpha=\alpha(t)\) 穿过零时的非自治图范数。参数范围和结论类型均不足以给出
  \(c\)-一致的 (1.2)。它的主要作用是警告：只看本征值或瞬时谱隙不能可靠控制传播子。

### 5.2 Delabaere--Trinh：复三次振子的全局谱解析结构

E. Delabaere and D. T. Trinh, “Spectral analysis of the complex cubic
oscillator,” *Journal of Physics A: Mathematical and General* 33 (2000),
8771--8796.

- 期刊 DOI：[10.1088/0305-4470/33/48/314](https://doi.org/10.1088/0305-4470/33/48/314)
- 可使用的准确内容：用 exact semiclassical/WKB analysis 研究一参数复三次振子的谱、
  \(PT\) 对称、关于参数的解析延拓与分支点结构。
- **Why not a substitute：** 这是固定参数的谱解析与精确 WKB 结果，不给出全参数一致的
  \(L_t^2H_x^{-1}\) coercivity、非自治传播子或临界点碰撞估计。参数谱的分支结构反而说明
  逐时谱分解可能具有非平凡参数奇性。

### 5.3 Dondl--Dorey--Rösler：非正规 Schrödinger 算子的 pseudospectrum

P. W. Dondl, P. Dorey, and F. Rösler, “A Bound on the Pseudospectrum for a
Class of Non-normal Schrödinger Operators,” *Applied Mathematics Research
eXpress* 2017, no. 2, 271--296. 该预印本早期题名是 “A Bound on the
Pseudospectrum of the Harmonic Oscillator with Imaginary Cubic Potential.”

- 一手来源：[arXiv:1505.05719](https://arxiv.org/abs/1505.05719)
- 期刊 DOI：[10.1093/amrx/abw011](https://doi.org/10.1093/amrx/abw011)
- 可使用的准确内容：对具有增长实部的非正规 Schrödinger 势证明立即紧 semigroup 与
  pseudospectrum 包含关系，并以带 imaginary cubic term 的 harmonic oscillator 为核心例子；
  文中也比较纯 imaginary cubic/complex Airy 等边界模型。
- **Why not a substitute：** 主要类别依赖增长的实部产生束缚，而 R0.72V 的三次项纯虚、
  空间全直线且没有该束缚结构；其结论是固定算子的 pseudospectral 包含，不是非自治
  \(H^{-1}\) 图范数。它支持“非正规性必须被认真处理”，但不能完成 (1.2)。

### 5.4 Grebenkov--Helffer--Henry：全直线 complex Airy 与界面

D. S. Grebenkov, B. Helffer, and R. Henry, “The complex Airy operator with a
semi-permeable barrier,” *SIAM Journal on Mathematical Analysis* 49 (2017),
1844--1894.

- 一手来源：[arXiv:1603.06992](https://arxiv.org/abs/1603.06992)
- 期刊 DOI：[10.1137/16M1067408](https://doi.org/10.1137/16M1067408)
- 可使用的准确内容：严格定义全直线上的
  \(-d^2/dx^2+ix\) 及原点半渗透传输条件，证明离散谱/广义本征函数完备性，给出 Airy
  函数 resolvent kernel、resolvent estimate 与关联 semigroup 衰减。无界面全直线 Airy
  模型在 Fourier 空间化为一阶平移加乘子，并有显式的超指数型短时/长时范数结构。
- **Why not a substitute：** Airy 势是线性的、固定的，且该论文的主要模型带界面传输条件；
  三次转折点、参数碰撞以及 \((a,b)\)-一致图范数均不存在。显式 Fourier 平移只在这一特殊
  线性势下闭合，不能直接推广为
  \(\partial_\xi^3-6a(t)\partial_\xi-\xi^2\) 的非自治估计。

### 5.5 这一组文献能支持与不能支持的结论

这些模型论文支持三点：

1. 三次纯虚势的自然半经典标度确为五次根结构；
2. complex cubic 的非正规性很强，谱位置本身不足以控制动力学；
3. complex Airy 在线性势下可显式解，但这种可解性不能外推到三次碰撞。

它们均未给出 R0.72V 的 coefficient-uniform unit-chart theorem，也未给出 (1.4) 所需的
负 Sobolev 直和全球化，因此都不是 R0.72V 证明的替代品。

---

## 6. 逐项替代性判定

| 来源 | 自治/非自治 | 空间几何 | 临界点机制 | 结论类型 | 可否替代 R0.72V |
|---|---|---|---|---|---|
| Li--Zhang (2025) | 自治 | 无界横截面 | 固定有限型 | resolvent/semigroup decay | 否：无 \(a(t)\)、无参数一致性、无 \(H^{-1}\) 图残差 |
| Arnaiz--Bony--Michel (2026) | 自治 | 主定理有界域；全空间模型 | 固定齐次退化 | 谱、resolvent、eigenmode expansion | 否：无碰撞时间、无全直线非自治图定理 |
| Coble--He (2024) | 非自治 | 全线/环面/有界通道分情形 | 单调或固定数目、分离、非退化临界点 | hypocoercive decay | 否：碰撞恰好破坏核心假设 |
| Benthaus--Coclite--Nobili (2026) | 非自治 | 环面 | 简单临界点刚性平移 | mixing 与 enhanced dissipation | 否：无合并退化；\(H^{-1}\) 对象不同 |
| Coti Zelati--Gallay (2023) | 自治 | 有界横截面 | 固定薄层集/有限型 | resolvent 与 hypocoercivity | 否：无全直线、无时间变化、无图残差 |
| Wei (2020) | 自治抽象定理 | Hilbert 空间 | 不编码碰撞 | resolvent \(\Rightarrow\) semigroup | 否：不能从 frozen \(H(t)\) 推出 \(U(t,s)\) |
| Helffer--Sjöstrand (2021) | 自治抽象定理 | Hilbert 空间 | 不编码碰撞 | 显式 semigroup bounds | 否：同样缺少非自治传递 |
| Henry (2014) | 自治 | 全直线 | 固定 complex cubic 参数 | 谱投影渐近 | 否：不是 coercivity 或传播子估计 |
| Delabaere--Trinh (2000) | 自治参数族 | 一维复三次振子 | 参数谱分支 | exact WKB/谱解析 | 否：没有动力学图范数 |
| Dondl--Dorey--Rösler (2017) | 自治 | 全空间 | imaginary cubic 非正规性 | pseudospectrum | 否：主要类有束缚实部，且无非自治残差 |
| Grebenkov--Helffer--Henry (2017) | 自治 | 全直线加界面 | 固定线性 Airy | resolvent/semigroup | 否：线性势可解性不覆盖三次碰撞 |

没有一行同时满足：

\[
\boxed{
\text{nonautonomous}
+\text{whole line}
+\text{collision-uniform}
+L_t^2H_x^{-1}\text{ graph forcing}.}
\tag{6.1}
\]

---

## 7. 有界检索说明

本轮只检索并核对了一手来源：作者/arXiv 原文、期刊页面和 DOI 元数据。检索入口包括：

- exact imaginary cubic \(x^3+\alpha x\) 与 complex Airy operators；
- purely imaginary/complex Schrödinger and heat operators；
- subelliptic、hypocoercive、resolvent-to-semigroup estimates；
- time-dependent shear、moving critical points、critical-point collision；
- unbounded cross-section、turning-point 与 global coercivity；
- 物理空间算子 (1.5) 及 Fourier 对偶 (1.6)。

在这个有界范围内，没有找到可直接套用并替代 R0.72V 证明链的定理。最接近的来源分别覆盖
“自治全直线有限型”“固定纯虚势的半经典谱”“缓慢移动的非退化临界点”“刚性平移临界点”
和“自治 resolvent-to-semigroup”，但没有覆盖 (6.1) 的交集。

这句话严格只表示 **bounded search did not locate a direct substitute**。它不是：

- 对全部数学文献的穷尽性检索；
- 对未检索语言、旧专著、未公开稿件或不同术语文献的不存在性证明；
- R0.72V 的 novelty、priority、first-proof 或独创性主张；
- 可以写入论文摘要的首创声明。

若未来需要投稿层面的新颖性判断，仍应由作者继续做 MathSciNet、zbMATH、Web of Science、
Google Scholar 引文链、相关作者主页及审稿人建议下的扩展检索。

---

## 8. 可被文献支持的准确定位

可使用以下表述：

> 自治有限型剪切、纯虚半经典 Schrödinger 算子以及若干保持临界点类型的时变剪切，已有
> 严格的 resolvent、hypocoercive 或 semigroup 理论。它们校准了三次退化的五次根标度，
> 也表明临界点运动与非正规性不能由瞬时谱信息忽略。R0.72V 不通过 frozen semigroup
> 拼接调用这些结果，而是先直接证明对两个低阶多项式系数一致的单位坐标片图范数估计，
> 再用精确 \(H^{-1}\) 直和不等式全球化，从而得到固定正时间块上的非自治全直线图范数定理。
> 对每个 \(L^2\) 初值的能量演化、时间迹与能量恒等式由独立的截断--紧性--cutoff
> 论证构造，不能从 maximal graph membership 单独推得。短时间测试只给出
> \(C_T\gtrsim T^{-1/3}\) 的下界，没有 matching upper bound。
> 本次有界一手文献检索未找到可直接替代这条证明链的定理；该检索结论本身不构成新颖性或
> 优先权主张。

仍必须同时保留 R0.72V 报告中的限制：常数不对 \(T\downarrow0\) 一致；周期 heat-path
传递、高阶余项稳定性、非线性 Navier--Stokes 闭合以及任何 Clay-level 后果均未由这些文献
或本节结果解决。
