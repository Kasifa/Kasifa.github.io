# R0.73K：参数一致黏性 rank-one 谱支与补空间控制

- **状态：** 连续算子定理、两份独立解析审计与有限诊断包已闭合；正式附图、双语 HTML/PDF 和发布门仍待封存
- **文档角色：** R0.73K canonical report-source
- **检索与核验日期：** 2026-08-31（Asia/Shanghai）
- **用途：** 汇总定理、奇异极限证明、Deep Research 文献边界、独立审计、有限诊断与开放问题

> 本节处理一个指定平面周期线性化算子的黏性谱支。它不把
> \(-\varepsilon L\) 当作有界扰动，也不依赖 Fourier 截断证明连续定理。
> 黏度阈值是存在性的；非自伴绝热跟踪、非线性与三维闭合、有限时间
> 奇性和 Clay 问题均未由此解决。

# I. 直接结果

## A. 算子与共同参数区间

令

\[
 W_d(x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad L=-\partial_x^2+\frac14,
\]

并在动能涡量空间 \(X\simeq H^{-1}_{\rm per}\) 上考虑

\[
 A_X(d)=-\frac i2\left(M_{W_d}+M_{W_d''}L^{-1}\right).
\]

固定酉变换 \(U=2L^{-1/2}:X\to L^2\) 后，生成元写成

\[
 \widetilde A(d)=M_d+K_d,
 \qquad M_d=-\frac i2M_{W_d},
\]

其中 \(M_d\) 斜自伴，\(K_d\) 紧。黏性生成元为

\[
 B_\varepsilon(d)=M_d+K_d-\varepsilon L,
 \qquad D(B_\varepsilon(d))=H^2_{\rm per}\quad(\varepsilon>0).
\]

在 \(\varepsilon=0\) 时，\(B_0(d)\) 是定义在全部 \(L^2\) 上的有界算子。
这个定义域跳变是证明的中心困难，不可省略。

R0.73J 已在完整区间 \(0\le d\le D_*:=1/450\) 认证一条代数简单的实无黏谱支

\[
 0.167<\lambda_0(d)<0.173,
\]

且其他谱点实部不超过 \(0.11\)。归一化动能左右重叠大于
\(0.5853\)，固定相位锚在整条支上不为零。

## B. R0.73K 定理

取共同圆

\[
 \Gamma_*:=\{|z-0.17|=0.003\}
\]

和固定半平面界 \(b_K=0.12\)。存在一个共同阈值
\(\varepsilon_K>0\)，使得对每个
\(0<\varepsilon\le\varepsilon_K\) 与每个
\(d\in[0,1/450]\)：

1. \(\Gamma_*\subset\rho(B_\varepsilon(d))\)，相应 Riesz 投影
   \(P_\varepsilon(d)\) 的秩为一；
2. 圆内唯一特征值 \(\lambda_\varepsilon(d)\) 代数简单、为实数，且关于
   \(d\) 实解析；
3. 投影在算子范数中一致收敛：
   \[
    \sup_{0\le d\le1/450}
    \|P_\varepsilon(d)-P_0(d)\|\longrightarrow0;
   \]
4. 特征值具有后续绝热分析所需的一阶误差率：
   \[
    \sup_{0\le d\le1/450}
    |\lambda_\varepsilon(d)-\lambda_0(d)|
    \le C_\lambda\varepsilon;
   \]
5. 充分减小共同阈值后，
   \[
    \sup_{\varepsilon,d}\|P_\varepsilon(d)\|<\frac95,
    \qquad
    \sup_{\varepsilon,d}\|\partial_dP_\varepsilon(d)\|<\infty;
   \]
   因而归一化黏性左右重叠大于 \(5/9\)，固定相位锚持续非零；
6. 固定半平面内没有其他黏性谱：
   \[
    \sigma(B_\varepsilon(d))\cap\{\operatorname{Re}z\ge0.12\}
    =\{\lambda_\varepsilon(d)\};
   \]
7. 移除该 rank-one 支后，缩减 resolvent 在整个固定半平面一致有界，并且
   \[
    \|e^{tB_\varepsilon(d)}Q_\varepsilon(d)\|
    \le C e^{0.12t},
    \qquad Q_\varepsilon=I-P_\varepsilon,
   \]
   而 rank-one 块上的逆向群满足
   \[
    \|e^{-tB_\varepsilon(d)}P_\varepsilon(d)\|
    \le C e^{-0.16t}.
   \]

选定支大于 \(0.167\)，补谱严格位于 \(0.12\) 左侧；本节采用保守的
统一实部安全间隔 \(1/25=0.04\)，没有声称达到端点 \(0.047\)。

# II. 为什么常规 Kato 黑箱不适用

对每个正黏性，椭圆项使 \(B_\varepsilon(d)\) 具有紧 resolvent。
无黏极限 \(B_0(d)=M_d+K_d\) 保留乘法本质谱，其 resolvent 非紧。
如果全算子 resolvent 在算子范数中收敛，那么非紧的极限 resolvent
会成为紧算子的范数极限，产生矛盾。

因此，本节明确记录：

- fullNormResolventConvergence=FALSE
- katoGeneralizedConvergenceAtEpsilonZero=FALSE

Kato 的 type-A 解析族理论只用于固定正黏性时的 \(d\)-参数，此时定义域
始终为 \(H^2_{\rm per}\)。它不用于把 \(\varepsilon\) 解析延拓穿过零点。

# III. 证明链

## 1. 联合强收敛

先移除紧项，定义耗散基算子

\[
 H_{\varepsilon,d}=M_d-\varepsilon L,
 \qquad R_{\varepsilon,d}(z)=(z-H_{\varepsilon,d})^{-1}.
\]

在任意紧集 \(\mathcal Z\Subset\{\operatorname{Re}z>0\}\) 上，
\(\|R_{\varepsilon,d}(z)\|\le(\operatorname{Re}z)^{-1}\)。对共同稠密核
\(H^2_{\rm per}\) 上的 \(f\)，有精确恒等式

\[
 R_{\varepsilon,d}(z)f-R_{0,d}(z)f
 =-\varepsilon R_{\varepsilon,d}(z)L R_{0,d}(z)f.
\]

乘法 resolvent \((z+iW_d/2)^{-1}\) 的前两阶导数在
\([0,D_*]\times\mathcal Z\) 上一致有界。由此得到基 resolvent 及其伴随
在 \((d,z)\) 上联合一致强收敛。

## 2. 两侧紧夹逼

\(d\mapsto K_d\) 在算子范数中实解析，每个 \(K_d\) 紧，所以
\(\{K_d\}\) 与 \(\{K_d^*\}\) 都 collectively compact。联合强收敛因而升级为

\[
 \sup_{d,z}\|(R_{\varepsilon,d}-R_{0,d})K_d\|\to0,
 \qquad
 \sup_{d,z}\|K_d(R_{\varepsilon,d}-R_{0,d})\|\to0.
\]

这个结论只作用在紧项的左右两侧，没有偷渡完整 norm-resolvent 收敛。

## 3. Fredholm 因子与投影范数

在右半平面分解

\[
 z-B_\varepsilon(d)
 =(z-H_{\varepsilon,d})
 [I-R_{\varepsilon,d}(z)K_d].
\]

R0.73J 保证无黏 Fredholm 因子在共同围道上可逆。两侧紧夹逼使黏性
Fredholm 因子在该围道上按算子范数一致收敛并保持可逆。完整 resolvent
与基 resolvent 之差满足

\[
 G_{\varepsilon,d}-R_{\varepsilon,d}
 =G_{\varepsilon,d}K_dR_{\varepsilon,d}.
\]

围道内部没有基算子的谱，因此
\(\int_{\Gamma_*}R_{\varepsilon,d}(z)\,dz=0\)。只积分按范数收敛的紧修正，
即可得到 \(P_\varepsilon\to P_0\) 的算子范数结论。投影差小于一时秩保持，
于是黏性谱块的总代数重数仍为一。

## 4. 为什么特征值误差真的是 \(O(\varepsilon)\)

仅有投影收敛只能给出 \(o(1)\)，不能给出速率。R0.73J 的显式左势为

\[
 p_d={\overline{\phi_d}\over W_d+2i\lambda_0(d)},
 \qquad \ell_0(d)\parallel2L^{1/2}p_d.
\]

因为 \(|W_d+2i\lambda_0(d)|\ge2\lambda_0(d)>0.334\)，参数 ODE 正则性给出
\(\ell_0(d)\in D(L)\) 和
\(\sup_d\|L\ell_0(d)\|<\infty\)。另一方面，Riesz 函数演算给出
\(P_\varepsilon H\subset D(B_\varepsilon)=D(L)\)。令
\(h_\varepsilon=P_\varepsilon h_0\)，则

\[
 (\lambda_\varepsilon-\lambda_0)
 \langle\ell_0,h_\varepsilon\rangle
 =-\varepsilon\langle L\ell_0,h_\varepsilon\rangle.
\]

投影收敛与无黏 overlap 下界使分母统一远离零，右侧则由平滑左向量
控制。这一步把无界 \(L\) 移到已知平滑的对象上，不估计
\(L(h_\varepsilon-h_0)\)。

## 5. 实性、解析性与条件数

反射与复共轭组成的 antiunitary 对称保持 \(H^2_{\rm per}\) 并与
\(B_\varepsilon(d)\) 交换。共同圆盘关于实轴对称，内部总代数重数为一；
若唯一特征值非实，其共轭会成为第二个谱点，产生矛盾。

固定正黏性时，\(d\mapsto B_\varepsilon(d)\) 是共同定义域上的 type-A
解析族。Riesz 公式给出

\[
 \partial_dP_\varepsilon(d)=\frac1{2\pi i}
 \int_{\Gamma_*}G_{\varepsilon,d}(z)
 \partial_d\widetilde A(d)G_{\varepsilon,d}(z)\,dz,
\]

从共同围道界得到统一 \(P_\varepsilon'\) 界。rank-one 投影范数等于
归一化左右重叠的倒数。由
\(\|P_0(d)\|<1/0.5853<1.709\) 和充分小黏性下的投影差 \(<0.08\)，得到
\(\|P_\varepsilon(d)\|<1.789<9/5\)，即黏性 overlap 大于 \(5/9\)。

## 6. 完整固定半平面与 Bromwich 界

局部 Riesz 圆不能控制不正规补空间。证明另外处理：

1. 高虚部区域，由两次 Neumann 分解得到
   \(\|G_{\varepsilon,d}(x+i\tau)\|=O(|\tau|^{-1})\)；
2. 高实部区域，由耗散基 resolvent 与 \(K_d\) 的一致范数排除谱；
3. 剩余显式紧矩形，用 R0.73J 的无黏谱隙和参数一致 Fredholm 收敛；
4. 选定圆盘内部，对移除 rank-one 块后的缩减 resolvent 应用标量最大模
   原理。

从公共增长线开始，先对截断 Bromwich 积分分部，得到平方 resolvent
的绝对收敛积分。再在已经移除唯一极点的缩减空间中，把积分线移动到
\(\operatorname{Re}z=0.12\)。水平边由统一
\(O(|\tau|^{-2})\) 控制而消失。最终得到

\[
 e^{tB_\varepsilon(d)}Q_\varepsilon(d)
 ={e^{0.12t}\over2\pi t}\int_{\mathbb R}e^{i\tau t}
 (0.12+i\tau-C_{\varepsilon,d})^{-2}Q_\varepsilon(d)\,d\tau.
\]

这不是由谱隙直接推得，也不需要随 \(\varepsilon\to0\) 保持一个统一
解析半群角。

# IV. 独立解析审计

独立逐节审计第一次检查没有发现结构性 blocker，但要求补齐三处：

- 显式拆开 \(G_\varepsilon KR_\varepsilon-G_0KR_0\) 的两项紧夹逼；
- 证明左右向量都在 \(D(L)\)，使 \(O(\varepsilon)\) 配对域合法；
- 写出 Riesz domain decomposition 和 square-resolvent Bromwich 桥接。

补丁完成后的复审结论为 ANALYTIC PASS。第二份反例式审计分别尝试
破坏全 \(d\) 一致性、rank-one 实性、条件数、无界配对和不正规半群；
最终结论为 PASS。两份审计都没有使用有限 Fourier 数据替解析证明背书。

# V. Deep Research 文献边界

## 1. 已知的一般现象

Shvydkoy 与 Friedlander 已证明环面 Navier--Stokes 算子在黏性消失时，
位于 Euler 本质谱阈值右侧的孤立不稳定特征值持续，总代数重数保持：

- Roman Shvydkoy and Susan Friedlander,
  [The unstable spectrum of the Navier--Stokes operator in the limit of
  vanishing viscosity](https://www.numdam.org/articles/10.1016/j.anihpc.2007.05.004/),
  Ann. IHP C 25 (2008), 713--724.

所以 R0.73K 不能称为“首个黏性消失谱持续定理”。该文没有给出本站
所需的紧剖面参数一致共同围道、目标空间中的算子范数投影收敛、
\(O(\varepsilon)\) 速率或完整补空间界。

## 2. 本节的窄贡献

在已核验的一手来源中，未发现一条定理同时覆盖：固定
\(\gamma=1/2\)、完整 \(d\in[0,1/450]\)、共同 rank-one 黏性支、
投影算子范数一致收敛、特征值 \(O(\varepsilon)\) 率和固定半平面补空间
控制。

最稳妥的原创性表述是：

> 对已认证的两谐波周期剪切流族，给出一个紧参数一致、可独立审计的
> vanishing-viscosity spectral-persistence specialization；新增的项目
> 特定内容是算子范数 Riesz 投影、rank-one 条件数、
> \(O(\varepsilon)\) 位移率和完整固定半平面补空间控制。

这个表述只针对已核验来源，不声称穷尽全部文献。

## 3. 相邻但不同的尺度

Li、Li--Lin 及 Grenier--Nguyen 的工作提供了周期 Kolmogorov 流或带壁
Orr--Sommerfeld 延拓先例；壁面快速模态自然产生分数黏性尺度，不能
直接决定本周期无壁问题的 \(O(\varepsilon)\) 率。

2025 年 Colombo--Dolce--Montalto--Ventura 的周期长波定理给出唯一简单
不稳定模与稳定余谱，但假设流向波数随黏性满足
\(\alpha|k|=O(\nu)\)。本站固定 \(\gamma=1/2\)，所以该假设在
\(\nu\to0\) 时失效。

Prüss 的 Hilbert 空间判据还强调：谱隙或局部围道不足以控制不正规
半群，必须保留整条竖线 resolvent。

# VI. 有限诊断合同

正式有限计算在精确动能酉变换后的 Fourier 压缩中进行。设
\(\ell_n=n^2+1/4\)、\(a=e^{-d}\)、\(b=e^{-4d}\)。raw vorticity 矩阵只有
四条副对角线：

\[
 A_{n+1,n}=\frac a8\left(1-\frac1{\ell_n}\right),
 \qquad A_{n-1,n}=-A_{n+1,n},
\]

\[
 A_{n+2,n}=b\left(-\frac1{16}+\frac1{4\ell_n}\right),
 \qquad A_{n-2,n}=-A_{n+2,n}.
\]

动能 \(L^2\) 矩阵为

\[
 B^{(N)}_{\varepsilon,d}(m,n)
 =\sqrt{\frac{\ell_n}{\ell_m}}A_{mn}(d)
  -\varepsilon\ell_n\delta_{mn}.
\]

有限计算应保存：固定圆盘内计数、左右 overlap、投影范数、
\(P_\varepsilon-P_0\)、特征值差商、解析一阶配对公式、左右 embedded
residual、幂等与 intertwining residual，以及跨 cutoff 的嵌入投影差。

第二实现不得导入主 recurrence，而应从
\(\widehat W_d(k)\) 和 \(\widehat{W_d''}(k)=-k^2\widehat W_d(k)\) 直接重建
Toeplitz 矩阵。它仍然只认证两个有限计算实现彼此一致。

正式网格取

\[
 N\in\{24,48,96,128,160\},\qquad
 d_j={j\over7200}\quad(0\le j\le16),
\]

核心黏度为
\(0,10^{-8},3\cdot10^{-8},\ldots,10^{-3}\)，另以
\(3\cdot10^{-3}\) 和 \(10^{-2}\) 作圆外 continuation 压力测试。主实现共
保存 1,190 个谱状态与 952 个相邻 cutoff 比较；所有 fail-closed 检查
通过。独立实现没有导入主 recurrence，而由 \(W_d,W_d''\) 的显式 Fourier
系数重建矩阵；其全部检查同样通过，与主实现的最大绝对字段差为
\(3.664\times10^{-7}\)。该最大值出现在除以极小黏度后的差商，不是
特征值本身；特征值实部的最大实现间差为
\(1.008\times10^{-14}\)。

在最大 cutoff \(N=160\) 的核心区间内，有限支满足

\[
 0.168207092942025\le\operatorname{Re}\lambda_\varepsilon^{(160)}(d)
 \le0.170407976920434,
\]

最小左右 overlap 为 \(0.5939991104\)，最大投影范数为
\(1.683504205\)，而 \(\varepsilon\le10^{-3}\) 时最大的
\(\|P_\varepsilon^{(160)}-P_0^{(160)}\|\) 为 \(0.1806379812\)。
\(N=128\) 与 \(N=160\) 在核心网格上的最大特征值差为
\(7.586\times10^{-15}\)，最大嵌入投影差为
\(5.662\times10^{-14}\)。最大左右 algebraic residual、rank-one
intertwining residual 与稳定低秩幂等 residual 分别不超过
\(1.599\times10^{-14}\)、\(2.374\times10^{-14}\) 与
\(9.336\times10^{-16}\)。

manifest、16 条 SHA256 记录、运行环境、命令、主/独立进度日志及资源日志
均已封存；独立整包审计的九项检查全部通过。其 claim boundary 明确记录：
这是有限维 Fourier 诊断，不认证连续谱秩、共同黏度阈值、补空间半群、
非线性 Navier--Stokes 或 Clay 问题。它为 K1--K7 提供可复现的错误探测，
但不进入连续证明逻辑。

# VII. 价值、限制与下一步

R0.73K 关闭了 R0.73I 合同 I2 的核心部分：在完整固定窗口上，现在有
一个规范可选、条件数受控、随黏性以 \(O(\varepsilon)\) 靠近无黏支的
rank-one 谱块，并且补空间具有统一 resolvent/半群控制。这是进入移动
生成元和非自伴绝热余项前缺少的最后一个静态谱输入。

它仍不证明长达 \(D_*/\varepsilon\) 的时间内解会跟随瞬时谱支。
\(P_\varepsilon'\) 有界只是绝热证明的输入，不是绝热定理本身。下一节
应在共同定义域和不正规二分性下控制移动投影耦合，证明或否定匹配
作用量的有界前因子。

- uniformRankOneViscousBranch=CLOSED
- uniformProjectionNormConvergence=CLOSED
- uniformEigenvalueOepsilon=CLOSED
- uniformProjectionConditioning=CLOSED
- fixedHalfPlaneNoPollution=CLOSED
- uniformReducedResolvent=CLOSED
- uniformComplementSemigroup=CLOSED
- explicitViscosityThreshold=OPEN
- finiteDiagnosticPackage=CLOSED
- nonselfadjointAdiabaticTracking=OPEN
- matchingSelectedGainAction=OPEN
- nonlinearNavierStokes=OPEN
- transverseThreeDimensionalClosure=OPEN
- finiteTimeSingularity=OPEN
- Clay=OPEN
