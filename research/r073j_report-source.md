# R0.73J：周期 Rayleigh 唯一简单最右谱支的连续算子认证

- **状态：** 定理与严格计算证据已组装；正式附图、双语 HTML/PDF 与发布门禁尚待完成
- **文档角色：** R0.73J canonical report-source
- **检索与核验日期：** 2026-08-30（Asia/Shanghai）
- **用途：** 汇总连续算子定理、解析证明、严格区间证书、独立审计、失败记录与原始文献边界
- **读者：** 需要复核定理假设、重数桥接、区间计算、出处和证据边界的研究者

> 本报告认证一个指定平面周期线性化算子的连续算子谱支。它不是
> Fourier 截断外推，也不证明黏性谱支的一致持续、非自伴绝热余项、
> 横向三维闭合、有限时间奇性或 Clay 问题。

# I. 本节结果

## A. 直接结论

令

\[
W_d(x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
\qquad L=-\partial_x^2+\frac14,
\]

并在动能涡量空间 \(X\simeq H^{-1}_{\rm per}(\mathbb T)\) 上定义

\[
A_X(d)=-\frac i2\left(M_{W_d}+M_{W_d''}L^{-1}\right).
\]

解析证明与两份严格区间证书给出一条实解析函数

\[
\lambda_0:[0,1/450]\longrightarrow(0.167,0.173).
\]

对每个 \(d\in[0,1/450]\)，\(\lambda_0(d)\) 是代数简单的实特征值，
也是唯一满足 \(\operatorname{Re}\lambda>0.11\) 的谱点。其余谱点均满足

\[
\operatorname{Re}z\le0.11.
\]

因此真实的实部谱隙严格大于 \(0.057\)，可安全固定
\(g_*=1/20\)。归一化动能左右特征向量的重叠严格大于
\(0.5853>1/2\)，固定相位锚
\(\mathfrak a(h)=(L^{-1}h)(0)\) 在整条谱支上不为零。

这个结论比“有限矩阵中看见一条领先支”强：它对指定
无限维算子和完整 \(d\)-区间成立。它又比“只有一个不稳定特征值”弱：
有限诊断仍显示实部约为 \(0.04\) 的另一对不稳定根，本节没有排除它们，
也不需要排除它们。

## B. 解析闭合链

解析证明 `research/r073j_analytic_proof.md` 完成五个必要环节。

1. 单位共轭把 \(A_X(d)\) 写成虚轴乘法算子加紧扰动，从而
   \(\sigma_{\rm ess}(A_X(d))\subset i\mathbb R\)。
2. 右半平面的动能空间 Jordan 链经 Sobolev bootstrap 全部变光滑，
   与普通 \(L^2\) 实现的广义根空间一致。
3. 精确因子分解
   \[
   (\lambda-A_2(d))L=M_{\lambda+iW_d/2}T(d,\lambda)
   \]
   连同周期 BVP/IVP 的解析等价，把 Evans 零点阶数严格连接到
   \(A_X(d)\) 的代数重数。
4. 反射—共轭对称给出
   \(E(d,\bar\lambda)=\overline{E(d,\lambda)}\)。
5. Howard 恒等式给出统一外谱界
   \[
   |\lambda|\le\frac{3\sqrt3}{16}<\frac{13}{40}.
   \]

独立逐行审计 `research/r073j_analytic_audit.md` 已通过；它只审计解析
链，不替数值证书背书。

## C. 参数一致围道证书

取全局矩形

\[
\Omega=\{0.11<\operatorname{Re}\lambda<0.38,
\ |\operatorname{Im}\lambda|<0.38\}
\]

和局部圆盘 \(|\lambda-0.17|<0.003\)。主计算在 80 位十进制精度下
完成 21,632 个 Arb/Acb 单值矩阵 ODE 网格点，使用 \(d\) 次数 12、
围道次数 26/18、1024/512 个 ODE 步和 16 个进程。完整 dyadic
实盒覆盖上的区间 Clenshaw 计算证明

\[
\inf_{[0,1/450]\times\partial\Omega}|E|>5.49948,
\qquad
\inf_{[0,1/450]\times\partial B_{\rm loc}}|E|>0.164355.
\]

在 \(d=0\) 的精确有理多边形绕数均为 1。参数同伦因此保持两个
区域的零点总阶数为 1。局部圆盘包含于全局矩形；对称性迫使唯一零点
为实数；总阶数 1 和重数桥接使其成为代数简单特征值。Howard 圆盘
排除全局矩形右、上、下边以外的右半平面谱，因而完成“唯一最右”结论。

第二套围道后处理从共享原始网格重新做二维 DCT、反向轴序的区间
Clenshaw、同伦与精确绕数，得到全局和局部下界分别大于
\(5.49739\) 与 \(0.164339\)，两个绕数仍为 1。它能发现后处理、
覆盖、账本和绕数错误，但由于共享原始 ODE 网格，不能称为完整独立
ODE 证明。

## D. 左右重叠与固定相位锚

第二份正式证书在
\([0,1/450]\times[0.167,0.173]\) 的完整矩形上认证 plus/minus
全纯替身。841 个 80 位 ODE 网格点经中点 Bernstein 范围、Chebyshev
系数残差和解析插值余项后得到

\[
|M_{12}|>1.84154,
\qquad
\frac{|\langle\ell,h\rangle_X|}{\|\ell\|_X\|h\|_X}>0.585343.
\]

独立 overlap 后处理没有导入主分析代码。它重构 3364 个原始球，
用 cell-centre 加 Chebyshev 导数 Lipschitz 界覆盖全部 128 个盒，并
给出独立下界 \(0.5850094448>1/2\)。它同样明确保留“共享原始网格”
限制。

## E. 失败记录与自然参数盒复算

两种早期范围方法被拒绝并保存在
`experiments/r073j/failure_ledger.json`：完整球半径经过
Chebyshev--power--Bernstein 转换后发生 wrapping；直接区间 Clenshaw
在参数端点丢失共享变量依赖。两次失败都不是检测到 Evans 零点，原始
ODE 网格也没有被覆盖；替代分析有单独源码账本。

独立自然参数盒 ODE 复算使用 120 位、Taylor 次数 14、2048/1024
步，且不导入主 ODE 实现。初始固定宽度的 83 盒中 76 盒严格通过，
7 盒因 Evans 区间包含零而不确定；全部分母和 Picard tube margin
严格为正。随后对这 7 盒做完整两层 \(2\times2\) dyadic 细分，只有
1 个父盒被全通过叶盒覆盖，另外 6 个仍为 wrapping-inconclusive；
这个中间结果原样保留。最终自适应深细分继续完整分裂每个失败分支：
depth 3 为 64/384 通过，depth 4 为 768/1280 通过，depth 5 的
2048 盒全部通过。最后 2,896 个自适应叶盒全部通过，最小 Evans
下界大于 \(0.00714950\)，所以原 83 个选定盒现在全部由直接盒或
通过叶盒覆盖。它仍是佐证性 spot audit：选定盒不等于完整围道，
不能替代参数一致 Clenshaw 证书。

## F. 研究价值与下一门槛

R0.73J 把 R0.73I 留下的关键谱假设变成了连续算子定理：显式正窗口、
唯一简单最右支、统一实部谱隙、非退化左右重叠和固定相位锚现在都有
可复核证据。它为下一步构造黏性 rank-one 支、选定规范向量和控制
非自伴绝热余项提供了此前缺少的谱底座。

这仍不是三维 Navier--Stokes 正则性进展。下一节 R0.73K 应首先证明
该简单支在小黏性下的一致持续，并给出 Riesz 投影及 complement
resolvent 的显式一致界；只有随后闭合移动投影和绝热余项，才可能把
本节的谱底座接回非线性增长机制。

# II. 原始文献审计与方法边界

## 1. 研究问题

考虑解析周期剪切流

\[
W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin 2x,
\qquad \gamma=\frac12,
\]

以及周期 Rayleigh 方程

\[
(W_d-c)(\phi''-\gamma^2\phi)-W_d''\phi=0,
\qquad \sigma=-i\gamma c,
\qquad c=2i\sigma.
\]

R0.73J 的目标不是把不稳定特征值称为“连续谱支”。这里需要认证的是离散不稳定特征值支。目标形式是：找出显式的 $D>0$；优先检查既定候选窗口

\[
0\le d\le D,\qquad D=\frac1{450},
\]

并严格证明在包含 \([0,D]\) 的开邻域上存在关于 $d$ 解析的函数 \(\sigma_*(d)\)，满足：

1. \(\sigma_*(d)\) 是周期 Rayleigh 问题的特征值；
2. 它在指定右半平面区域内是唯一零点，按代数重数计数为一；
3. 它与其余谱之间有显式实部间隙，因此是唯一最右特征值；
4. Evans 零点的阶数确实等于原始 Rayleigh／涡量算子铅笔的代数重数。

本站先前的 R0.73C 记录只提供纯增长候选根位于

\[
\sigma_*\in(0.17035,0.17050)
\]

这一局部输入。它本身不推出全区域唯一性、代数简单性或最右性。本报告也不重新认证该区间。

一个足够而且较弱的目标是：选取 \(0<b<0.17035\) 和有限 \(R\)，令

\[
\Omega_{b,R}=\{\sigma:\operatorname{Re}\sigma>b,\ |\sigma|<R\}.
\]

若能证明每个 \(d\in[0,D]\) 时 Evans 函数在 \(\partial\Omega_{b,R}\) 上无零点、绕数为一，并另行排除 \(|\sigma|\ge R\) 的谱，那么即可得到“唯一最右支”。这不要求证明整个开右半平面内只有一个不稳定特征值。

## 2. 两轮检索方法

### 第一轮：范围检索，2026-08-30

我按四组问题检索原始论文、作者预印本与正式期刊页面：

1. 周期 Rayleigh／二维 Euler 的 Evans 函数、单值矩阵与重数；
2. argument principle、Rouché 定理和区间 Evans 计算；
3. 非自伴周期算子的 Hill／Fourier 截断收敛；
4. Rayleigh 不稳定特征值的唯一性、简单性和 Hamiltonian index theorem。

这一轮的保留标准是：来源必须给出可定位的定理、命题或明确的适用假设。综述与二手转述只用于发现关键词，不进入下文的主张账本。

### 第二轮：定点核验，2026-08-30

第二轮只回到原始来源，逐项核对：

- Dullin–Marangell 的周期 Euler Evans 零点及其重数定义；
- Zumbrun 与 Johnson–Zumbrun 的周期 Evans／Fredholm determinant／Hill 截断结论；
- Barker–Zumbrun 的区间围道与 Rouché 步骤，以及其参数覆盖边界；
- Bian–Grenier 对任意阶退化临界层的局部结论；
- Lin–Zeng index theorem 的抽象假设与二维 Euler 专门化假设；
- Xu 的第一类 Chebyshev 根节点 Lebesgue 常数和 aliasing，以及 Trefethen 的 Bernstein ellipse 系数与插值误差。

检索在以下事实收敛后停止：已有文献给出了所需方法的各个部件，但没有发现直接覆盖上述两谐波剖面、整个显式 \(d\) 窗口及“唯一、简单、最右”三项结论的现成定理。

## 3. 周期 Evans 函数与重数

### 3.1 Dullin–Marangell：周期 Euler 的 Hill–Evans 构造

**来源。** Holger R. Dullin and Robert Marangell, *An Evans function for the linearised 2D Euler equations using Hill's determinant*, Physica D 457 (2024), 133954. [期刊 DOI](https://doi.org/10.1016/j.physd.2023.133954)；[作者稿 PDF](https://www.maths.usyd.edu.au/u/marangel/publications/EulerHillEvansFinal3.pdf)。

**精确定位。**

- §2，作者稿 p. 8：用周期二阶常微分方程的单值矩阵在乘子 $1$ 处的代数重数定义 \((\lambda,k)\) 的代数重数；完整 Euler 算子的重数再按相应 lattice classes 求和。
- Theorem 5.1，作者稿 pp. 17–19：其 Evans 函数 \(E(c;\theta,d)\) 在 \(c\notin[-1,1]\) 上解析；零点对应分离后的周期问题；零点阶数等于该文周期 ODE 意义下的代数重数。这里该文的参数符号 $d$ 与本站的热时间参数 $d$ 无关。
- Theorem 6.1，作者稿 pp. 25–26：把分离问题的 Evans 函数组合成二维环面 Euler 线性化的乘积 Evans 函数。
- Introduction，作者稿 p. 2：作者说明方法可推广到一般周期剪切流；论文中的显式计算和计数则针对单模／cosine equilibrium。

**分类。**

- **直接支持：** 在该文的 cosine equilibrium 与其周期 ODE 重数定义内，Evans 零点、谱点和零点阶数的对应。
- **方法先例：** 用单值矩阵、Hill determinant 和解析 Evans 函数处理周期 Euler/Rayleigh 分离问题。
- **不适用边界：** 论文没有直接处理本站的两谐波剖面，也没有替本站证明 Evans 零点阶数等于原始涡量算子铅笔的广义特征空间维数。

因此，Theorem 5.1 不能被简写为“本站重数引理已经由文献给出”。本站仍需写出从周期 ODE 到原始算子铅笔的代数重数对应。

### 3.2 Zumbrun：周期单值 Evans 函数的零点重数

**来源。** Kevin Zumbrun, *2-Modified Characteristic Fredholm Determinants, Hill's Method, and the Periodic Evans Function of Gardner*, Zeitschrift für Analysis und ihre Anwendungen 31 (2012), 463–472；稿件提交于 2010 年。[EMS 正式 PDF](https://ems.press/content/serial-article-files/35837)；[期刊 DOI](https://doi.org/10.4171/ZAA/1469)。

**精确定位。**

- §1，p. 464：基本对象是周期二阶问题
  \[
  (\partial_x^2+\partial_xA_1+A_0-\lambda B_0)U=0,
  \]
  其中系数为 $L^2$，并对 $B_0$ 的对称部分施加正定或负定条件。
- Proposition 2.3，p. 465：2-modified Fredholm Evans 函数解析，其零点在位置和重数上与周期特征值一致。
- Definition 4.1，p. 466：Gardner 的周期 shooting Evans 函数定义为 \(E(\lambda)=\det(\Psi(X)-I)\)。
- Proposition 4.2，p. 467：在 $C^1$ 系数下，标准周期 Evans 函数的零点在位置和重数上与周期特征值一致。排印正文在该命题的一处写作 $D$，上下文定义的函数是 $E$。
- Theorem 5.1，p. 467：一阶 Fredholm Evans 函数与单值 Evans 函数相差一个处处非零的因子。

**分类。**

- **直接支持：** 对该文固定的局部周期算子类，单值 Evans 零点的阶数记录代数重数。
- **方法先例：** 本站可以仿照其 shooting/Fredholm 对照来组织重数证明。
- **不适用边界：** Rayleigh 方程在未除法前是含微分谱权的算子铅笔；除以 \(W-c\) 后又对 $c$ 呈有理依赖。必须先验证本站问题落入哪一个解析 Fredholm／operator-pencil 框架，不能直接套用 Proposition 4.2。

## 4. Hill 截断能给什么，不能给什么

### 4.1 Johnson–Zumbrun：非自伴周期算子的 Hill 收敛

**来源。** Mathew A. Johnson and Kevin Zumbrun, *Convergence of Hill's Method for Nonselfadjoint Operators*, SIAM Journal on Numerical Analysis 50 (2012), 64–78. [arXiv 作者稿](https://arxiv.org/pdf/1009.3908)；[期刊 DOI](https://doi.org/10.1137/100809349)。

**精确定位。**

- Theorem 3.4，arXiv pp. 7–8（期刊 pp. 70–71）：构造的 generalized periodic Evans function 解析，零点按位置和重数对应周期谱。
- Remark 3.5，arXiv p. 8（期刊 p. 71）：可在围道上比较截断 determinant，并通过绕数转移零点计数。
- Corollary 3.9，arXiv p. 10（期刊 p. 73）：Hill 特征值在位置和重数上收敛。
- Theorem 3.10 及紧随其后的讨论，arXiv pp. 10–11（期刊 pp. 73–74）：determinant 的收敛率本身不自动给出单个根的收敛率。

**分类。**

- **直接支持：** 对论文假设下的周期算子，Hill 谱近似在位置和重数上的收敛。
- **方法先例：** Fourier/Hill 截断可以定位候选围道、测试分辨率，并为严格围道设计提供初值。
- **不适用边界：** 一个有限矩阵的谱图、截断阶数一致性或表观 spectral gap 不是有限误差证书。R0.73J 不能从普通浮点 Hill 截断直接推出连续算子的零点数。

## 5. 区间 Evans、Rouché 与参数窗口

### 5.1 Barker–Zumbrun：围道像的区间包围

**来源。** Blake Barker and Kevin Zumbrun, *Numerical proof of stability of viscous shock profiles*, Mathematical Models and Methods in Applied Sciences 26 (2016), 2451–2469. [arXiv 作者稿](https://arxiv.org/pdf/1601.00837)；[期刊 DOI](https://doi.org/10.1142/S0218202516500585)。

**精确定位。**

- Introduction，arXiv p. 2：用区间算术包围 Evans 函数在围道上的像；若相对误差小于 $1$，Rouché 定理把近似函数的绕数转移给真实 Evans 函数，再由 argument principle 计数零点。
- Theorem 1.1，arXiv p. 3：论文实际认证的是七个离散的 $v_+$ 参数值。
- Remark 1.2，arXiv p. 3：连续性只给出每个已认证点附近某个邻域；直接携带参数区间会造成严重 overestimation，需要插值层才能得到有用的参数覆盖。
- Lemma 3.5，arXiv pp. 10–11：给出列出的离散参数值上的实际区间包围。
- §3.4，arXiv p. 11：从点态认证得到的附近稳定性是存在性的，并没有给出可用的统一显式参数宽度。

**分类。**

- **直接支持：** 论文所列 viscous-shock 实例上的区间 Evans／Rouché 认证。
- **方法先例：** R0.73J 可以沿围道包围 $E$ 或 $E/E_{\mathrm{ref}}-1$，并以 Rouché 或 argument principle 给出整数零点数。
- **不适用边界：** 七个离散参数点的认证不能推出整个 $d\in[0,D]$ 窗口。本站必须加入 $d$ 方向的导数界、Chebyshev 区间插值，或对 $d$-围道二维盒作完整细分。

这篇论文最重要的负面提醒是：参数连续性不等于显式统一窗口。

## 6. 退化临界层的适用边界

### 6.1 Bian–Grenier：任意阶临界点附近的局部 Rayleigh 解

**来源。** Dongfen Bian and Emmanuel Grenier, *Singularities of Rayleigh equation*, arXiv:2408.00977 (2024). [作者预印本 PDF](https://arxiv.org/pdf/2408.00977)。

**精确定位。**

- Definition 1.1，p. 3：定义任意阶 $n\ge1$ 的临界点。
- Theorem 1.2，p. 4：对固定 \(|\alpha|>0\) 和 $C^\infty$ 剪切流，在任意阶临界点附近构造局部解并给出控制。
- §2.1.2：给出高阶临界点局部构造的证明。
- Theorem 1.3，p. 5：是带衰减与小参数条件的半直线全局结论，不是周期单值矩阵的全局零点计数。

本站剖面在 $d=0$ 时满足

\[
W_0(x)=-2\sin^3(x/2)\cos(x/2),
\qquad -\frac{W_0''(x)}{W_0(x)}\sim-\frac6{x^2}.
\]

因此 $x=0$ 是三阶退化零点。Theorem 1.2 对理解 $c\to0$ 时的局部奇性是直接相关的，但它不计数周期特征值，也不证明 Evans 零点的唯一性或简单性。

另一方面，R0.73J 拟使用的围道位于 \(\operatorname{Re}\sigma\ge b>0\)。由于 \(c=2i\sigma\)，有

\[
\operatorname{Im}c=2\operatorname{Re}\sigma\ge2b,
\qquad |W_d(x)-c|\ge2b.
\]

所以该围道上没有实临界层。Bian–Grenier 的退化临界层理论不是这一步围道计算的必要输入；它属于靠近 $c=0$ 或虚轴边界时的局部理论。

## 7. Index theorem 为何不能直接给出本站唯一性

### 7.1 Lin–Zeng：抽象 Hamiltonian 指标与二维 Euler 专门化

**来源。** Zhiwu Lin and Chongchun Zeng, *Instability, index theorem, and exponential trichotomy for Linear Hamiltonian PDEs*, arXiv:1703.04016v4 (2021). [作者预印本 PDF](https://arxiv.org/pdf/1703.04016)。

**精确定位。**

- §2.1，pp. 17–18，假设 (H1)–(H3)：$J$ anti-self-dual；$L$ 为有界对称算子，空间分解为有限维负空间、\(\ker L\) 与一致正空间；相应 annihilator 落在 $D(J)$ 中。
- Theorem 2.3，p. 24：
  \[
  k_r+2k_c+2k_i^{\le0}+k_0^{\le0}=n^-(L).
  \]
- Corollary 2.2，pp. 24–25：若 \(n^-(L)-k_0^{\le0}=1\)，则恰有一对稳定／不稳定特征值，并且为简单特征值。
- §11.5，pp. 147–152：二维 Euler 专门化从 \(-\Delta\psi_0=g(\psi_0)\) 出发；p. 148 进入 $g'>0$ 的加权空间；p. 149 定义算子 $A$；Theorem 11.5，p. 152，在 $g'>0$ 与 \(\ker A=0\) 等条件下给出指标公式。

对本站剪切流，标准 Euler 专门化所需的权函数为

\[
g'(\psi_0)=-\frac{W_d''}{W_d}.
\]

在 $d=0$ 时它按 \(-6/x^2\) 发散并为负。对 $0<d<\log(4)/3$，在 $x=0$ 的可去极限为

\[
\lim_{x\to0}-\frac{W_d''(x)}{W_d(x)}
=\frac{e^{-d}-4e^{-4d}}{e^{-d}-e^{-4d}}<0.
\]

故本窗口不满足 §11.5 的 $g'>0$ 假设；在端点 $d=0$ 还出现 inverse-square 奇性。

**分类。**

- **直接支持：** Theorem 2.3 与 Corollary 2.2 给出抽象的“负指标为一 → 唯一简单不稳定对”判据。
- **方法先例：** 若以后能为本站构造满足 (H1)–(H3) 的奇异 Hamiltonian 空间并计算所有修正指标，该路线仍可能适用。
- **不适用边界：** 论文 §11.5 的标准二维 Euler 定理不能直接覆盖本站 cubic zero，也不能在当前假设下替代 Evans 围道认证。

因此，现阶段不能用“index theorem 已证明唯一性”作为 R0.73J 的论据。

## 8. Chebyshev 第一类根节点：常数与 off-by-one 核验

这一部分服务于后续 $d$ 参数插值或围道分片。所有公式均先按一维写出；若使用张量积插值，各方向的 Lebesgue 因子会相乘，不能把一维常数直接当成多维常数。

### 8.1 Xu：第一类根节点的 Lebesgue 常数与 aliasing

**来源。** Kuan Xu, *The Chebyshev points of the first kind*, Applied Numerical Mathematics 102 (2016), 17–30. [作者接受稿 PDF](https://kar.kent.ac.uk/58498/1/firstkind_revision2.pdf)；[期刊 DOI](https://doi.org/10.1016/j.apnum.2015.12.002)。

**精确定位。**

- Equation (1)：$N$ 个第一类根节点为
  \[
  x_k=\cos\frac{(2k+1)\pi}{2N},\qquad k=0,\ldots,N-1.
  \]
- §2.3，Theorems 1–2 与 Corollary 1，接受稿 pp. 4–5（PDF pp. 5–6）：第一类 $N$-节点网格上的精确 aliasing 关系。
- §2.10，Theorem 4(1)，接受稿 pp. 12–13（PDF p. 13）：对 $n+1$ 个第一类根节点上的次数 $n$ 插值，
  \[
  \Lambda_n\le1+\frac2\pi\log(n+1).
  \]

因此，对次数 $12,20,40$ 分别使用 $13,21,41$ 个根节点，有

| 插值次数 $n$ | 节点数 $N=n+1$ | Xu 上界 $1+\frac2\pi\log(n+1)$ |
|---:|---:|---:|
| 12 | 13 | $2.632897\ldots$ |
| 20 | 21 | $2.938203\ldots$ |
| 40 | 41 | $3.364133\ldots$ |

三者均小于 $4$。不依赖小数舍入也可统一证明：对 $n\le40$，

\[
\Lambda_n\le1+\frac2\pi\log41
<1+\frac23\,4=\frac{11}{3}<4.
\]

Xu 同时把该上界的早期来源指向 Theodore J. Rivlin, *The Lebesgue constants for polynomial interpolation*, Lecture Notes in Mathematics 399 (1974), 422–437，[DOI](https://doi.org/10.1007/BFb0063594)。本站引用具体节点约定时应优先引用 Xu，因为其 $N$ 与 $n$ 的约定在正文中明确可见。

### 8.2 Trefethen：Bernstein ellipse 系数界与插值误差

**来源。** Lloyd N. Trefethen, *Approximation Theory and Approximation Practice*, Chapter 8. [作者官方样章 PDF](https://people.maths.ox.ac.uk/trefethen/trefethen_sample.pdf)；[作者维护的 Chapter 8 源文件](https://github.com/chebfun/ATAP/blob/development/chap8.m)。

**精确定位。**

- Theorem 8.1：若 $f$ 在 Bernstein ellipse $E_\rho$ 内解析且在其上满足 \(|f|\le M\)，则 Chebyshev 系数满足
  \[
  |a_k|\le2M\rho^{-k}.
  \]
- Theorem 8.2，式 (8.3)：对该书采用的第二类／Lobatto Chebyshev 节点，次数 $n$ 插值满足
  \[
  \lVert f-p_n\rVert_\infty
  \le\frac{4M\rho^{-n}}{\rho-1}.
  \]

Trefethen 在书中把第二类节点简称为 “Chebyshev points”。所以 Theorem 8.2 不能单独作为第一类根节点误差式的来源。第一类根节点的同常数界可由 Theorem 8.1 与 Xu 的 aliasing 直接推出。

令 $I_{N-1}$ 是 $N$ 个第一类根节点上的插值算子。Xu 的 aliasing 给出，对 $k\ge N$，$I_{N-1}T_k$ 是带符号的低阶 Chebyshev 多项式，故

\[
\lVert T_k-I_{N-1}T_k\rVert_\infty\le2.
\]

由解析函数的一致收敛 Chebyshev 展开和 Theorem 8.1，

\[
\begin{aligned}
\lVert f-I_{N-1}f\rVert_\infty
&\le2\sum_{k=N}^{\infty}|a_k|\\
&\le4M\sum_{k=N}^{\infty}\rho^{-k}\\
&=\frac{4M\rho^{-N}}{1-\rho^{-1}}\\
&=\frac{4M\rho^{-(N-1)}}{\rho-1}.
\end{aligned}
\]

令 $n=N-1$，即得到第一类根节点上的

\[
\boxed{\lVert f-I_nf\rVert_\infty
\le\frac{4M\rho^{-n}}{\rho-1}}.
\]

### 8.3 off-by-one 对照表

| 说法 | 正确节点 | 多项式次数 | Lebesgue 对数项 | 椭圆误差指数 |
|---|---|---:|---:|---:|
| “degree $n$” | $n+1$ 个 $T_{n+1}$ 的根 | $n$ | \(\log(n+1)\) | \(\rho^{-n}\) |
| “$N$ nodes” | $N$ 个 $T_N$ 的根 | $N-1$ | \(\log N\) | \(\rho^{-(N-1)}\) |

所以：

- “degree 12/20/40”表示 $13/21/41$ 个节点；
- “12/20/40 nodes”表示次数 $11/19/39$；
- \(4M\rho^{-N}/(1-\rho^{-1})\) 与 \(4M\rho^{-(N-1)}/(\rho-1)\) 完全相同，不是两个不同的收敛率。

Lebesgue 常数小于 $4$ 只控制插值算子的放大。真正的区间余项还需要为每个被插值函数给出复椭圆半径 \(\rho>1\) 与边界上界 $M$。

## 9. 文献支持下的本站证明路线

在 \(\operatorname{Re}\sigma\ge b>0\) 上，\(|W_d-c|\ge2b\)。把 Rayleigh 方程写成一阶系统

\[
\frac{d}{dx}
\begin{pmatrix}\phi\\q\end{pmatrix}
=
\begin{pmatrix}
0&1\\
\gamma^2+\dfrac{W_d''}{W_d-c}&0
\end{pmatrix}
\begin{pmatrix}\phi\\q\end{pmatrix}.
\]

其系数在指定的 $(d,\sigma)$ 复邻域内联合解析。若 $M_d(\sigma)$ 是一周期单值矩阵，则系统矩阵迹为零，故 \(\det M_d=1\)，并可取

\[
E(d,\sigma)=\det(M_d(\sigma)-I)
=2-\operatorname{tr}M_d(\sigma).
\]

文献支持的认证顺序如下。

1. **外半径。** 用连续算子估计、Howard 型界或另一条可审计的解析估计给出 $R$，排除 \(\operatorname{Re}\sigma>b,|\sigma|\ge R\) 的谱。有限矩阵最大特征值不能替代这一步。
2. **基准围道。** 在 $d=0$ 的 \(\partial\Omega_{b,R}\) 上，用区间 ODE／Taylor model 包围单值矩阵和 $E$，证明边界非零并计算绕数为一。
3. **参数窗口。** 对整个 \(d\in[0,D]\) 给出统一包围。可验证充分条件
   \[
   D\sup_{[0,D]\times\partial\Omega_{b,R}}|\partial_dE|
   <\inf_{\partial\Omega_{b,R}}|E(0,\sigma)|,
   \]
   也可直接对 $d$ 与围道参数作区间细分／Chebyshev 插值。
4. **零点盒。** 对唯一零点做复区间 Newton 或 Krawczyk 检验，给出 \(\sigma_*(d)\) 的显式盒和 \(\operatorname{Re}\sigma_*\ge a_->b\)。
5. **重数桥接。** 证明 $E$ 的零点阶数等于原始 Rayleigh／涡量算子铅笔的代数重数。绕数一先给出 Evans 零点简单；该桥接再把简单性转回算子谱。
6. **最右间隙。** 由区域内唯一根、区域外排除和 \(a_->b\) 得到显式间隙至少 $a_--b$。

若第 2–3 步只得到绕数一，则已经同时得到区域内唯一性和 Evans 零点简单性；不需要再以多个浮点初值逐个“寻找”其他根。区间 Newton 的价值主要是给出根盒、导数非零与分支跟踪的独立局部核验。

一旦 \(E(d,\sigma)\) 联合解析且唯一零点满足 \(\partial_\sigma E\ne0\)，解析隐函数定理给出局部解析根支；区域内唯一性使这些局部根支在连通参数窗口上拼接为同一支。这一步仍以联合解析域和导数非零的本站证明为前提。

## 10. 主张—来源账本

| 编号 | 可引用主张 | 主来源与定位 | 归类 | 对本站的限制 |
|---|---|---|---|---|
| S1 | 周期 Euler 分离问题可构造解析 Hill–Evans 函数，零点阶数记录论文定义的 ODE 代数重数 | Dullin–Marangell 2024, §2 p. 8; Thm. 5.1 pp. 17–19 | 直接支持＋方法先例 | 显式模型为 cosine equilibrium；仍需本站 operator-pencil 重数桥接 |
| S2 | 周期 shooting Evans 的零点在位置和重数上对应周期特征值 | Zumbrun 2012, Def. 4.1 p. 466; Prop. 4.2 p. 467 | 直接支持于其算子类 | Rayleigh 的微分谱权／有理依赖需另行纳入框架 |
| S3 | Hill 特征值在位置和重数上收敛 | Johnson–Zumbrun 2012, Cor. 3.9 | 直接支持于其假设 | 普通有限截断没有给出本站所需的验证误差 |
| S4 | 区间围道像、Rouché 与 argument principle 可给出严格 Evans 零点数 | Barker–Zumbrun 2016, Intro p. 2; Lem. 3.5 pp. 10–11 | 方法先例 | 论文认证七个离散参数值，不提供本站的统一 $d$ 窗口 |
| S5 | 任意阶临界点附近可构造局部 Rayleigh 解 | Bian–Grenier 2024, Def. 1.1; Thm. 1.2 | 直接局部支持 | 不给周期单值矩阵的全局零点计数；正 $b$ 围道上无临界层 |
| S6 | Hamiltonian 负指标在附加假设下可计数不稳定谱；指标差为一时得到简单不稳定对 | Lin–Zeng 2021, Thm. 2.3; Cor. 2.2 | 直接抽象支持 | §11.5 要求 $g'>0$；本站比值为负且 $d=0$ 奇异 |
| S7 | 第一类 $n+1$ 根节点的 \(\Lambda_n\le1+(2/\pi)\log(n+1)\) | Xu 2016, Thm. 4(1) | 直接支持 | 只是一维插值算子界 |
| S8 | Bernstein ellipse 上 Chebyshev 系数按 \(2M\rho^{-k}\) 衰减 | Trefethen, Thm. 8.1 | 直接支持 | 需要实际复邻域中的 \(\rho,M\) |
| S9 | 第一类根节点误差 \(4M\rho^{-n}/(\rho-1)\) | Trefethen Thm. 8.1 ＋ Xu §2.3 aliasing 的上文推导 | 组合推论 | 不能把 Trefethen Thm. 8.2 的第二类节点约定误写成第一类 |

## 11. 文献阶段证明义务的最终状态

本轮原始文献核验得到三个结论。

第一，周期 Evans 函数、绕数计数、Hill 近似和区间 Rouché 的方法链有可靠的原始来源。它们足以指导 R0.73J 的证书设计。

第二，没有找到一条现成定理直接覆盖本站剖面

\[
-\tfrac12e^{-d}\sin x+\tfrac14e^{-4d}\sin2x
\]

在 $0\le d\le1/450$ 上的唯一、简单、最右不稳定特征值支。Dullin–Marangell 的显式计数属于 cosine equilibrium；Lin–Zeng 的标准二维 Euler 专门化在本站的符号与 cubic zero 处失效；Bian–Grenier 解决的是局部退化临界层结构，不是周期谱计数。

第三，Chebyshev 第一类根节点的常数已核对清楚：次数 $n$ 对应 $n+1$ 个节点，Lebesgue 上界含 \(\log(n+1)\)，Bernstein ellipse 误差含 \(\rho^{-n}\)。次数 $12,20,40$ 的一维 Lebesgue 常数统一小于 $4$。

文献阶段列出的六项证明义务现按下表结算。

| 证明义务 | 状态 | 最终证据 |
|---|---|---|
| 连续 Rayleigh 问题的显式外谱界 | CLOSED | 解析 Howard 界 \(|\lambda|\le3\sqrt3/16<13/40\) |
| \(d=0\) 基准围道非消失与绕数一 | CLOSED | `contour_certificate.json` 的精确有理多边形同伦与绕数 |
| 完整 \(d\in[0,1/450]\) 参数余项 | CLOSED | 两变量 Chebyshev 插值、解析椭圆余项和完整 dyadic 实盒覆盖 |
| 唯一根盒与 \(a_->b\) | CLOSED | 局部圆盘 \((0.167,0.173)\) 和全局左界 \(b=0.11\) |
| Evans 阶数到算子代数重数的桥接 | CLOSED | kinetic/L2 Jordan bootstrap、解析铅笔分解和 BVP/IVP 等价 |
| 显式最右谱隙 | CLOSED | 严格实部差 \(>0.057\)，保守常数 \(g_*=1/20\) |

此外，左右重叠与相位锚证书已经闭合。共享原始网格的两套独立后处理
通过；自然参数盒 ODE 复算的初始和 depth-two wrapping 失败被保留，
最终深细分则给出 83 个选定盒的完整通过覆盖。该抽查从一开始就不是
完整围道定理的逻辑前提。R0.73J 的数学表述因此可以写成“指定连续
算子的谱支定理已认证”，同时必须继续写明其黏性、三维、非线性、
奇性与 Clay 边界。
