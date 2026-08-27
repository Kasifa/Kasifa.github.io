# R0.72F 有界一手文献非碰撞审计

**检索截止日：** 2026-08-27
**审计对象：** 临界对数初始层作用量

\[
 w_*(s)=s^{-1/3}\log(e/s),
 \qquad
 \mathscr A_*(I;u)
 =\frac1T\int_I
 w_*\!\left(\frac{t-a}{T}\right)
 \frac{\|\mathbb P(u\times\omega)(t)\|_{\dot H^{-1}}^2}
 {\|\omega(t)\|_2^2}\,dt,
\]

以及尚未证明的完整根候选不等式

\[
 \mathcal J_{\rm all}(I)
 \stackrel{?}{\le}
 C D^{1/3}\mathcal R_Y(I)[1+\mathscr A_*(I;u)].
 \tag{0.1}
\]

## 0. 直接结论

我对十组最接近的原始论文或原始专著做了有界核验。没有一项已核验结果同时满足下面四个条件：

1. 适用于任意大数据或 Leray--Hopf 层级；
2. 右端能够只用能量不等式支付；
3. 能识别 R0.72E 中“固定初始频率支撑、增长耦合振幅”这一机制；
4. 能控制一个指定时间观测量全部零点处的平方斜率总账
   \(\mathcal J_{\rm all}\)。

Koch--Tataru、Tao 和 Temam 给出临界小数据、定量局部理论及 Leray
能量框架；Chemin--Planchon 给出真正带初始时刻奇异权的非线性能量估计；
Yang、Cheskidov--Dai、Yu 以及 Lerner--Vigneron 分别控制空间迹、动态频率、
滤波涡量拉伸和旋度几何；Foias--Guillopé--Temam 控制高阶空间导数的
时间平均；Kusuoka--Stroock 则为 R0.72E 的随机相位密度估计提供了外部工具。
这些结果都不能直接推出 (0.1)。

因此，文献能确认的是候选设计所处的数学邻域，而不是候选不等式本身。
我不把 (0.1) 称为新定理，也不把这次有界搜索写成原创性、优先权或全局
不存在性证明。

## 1. 逐项来源账本

| ID | 一手来源与已核验位置 | 该来源支持什么 | 该来源不支持什么 |
|---|---|---|---|
| F-L1 | H. Koch and D. Tataru, *Well-posedness for the Navier--Stokes equations* (2001), Theorems 2--3；[作者 PDF](https://math.berkeley.edu/~tataru/papers/nas.pdf)，[DOI](https://doi.org/10.1006/aima.2000.1937) | 以热流定义的 \(BMO^{-1}\) 数据范数、含 \(\sqrt t\,L^\infty\) 与 Carleson/tent 平方项的解空间，以及小 \(BMO^{-1}\) 数据的全局适定性和局部版本。它说明临界尺度的“初始层 + 时空帐篷”结构是严格分析工具。 | 结论要求临界范数小；它没有给出任意大 Leray 数据的能量支付，也没有出现 \(\mathbb P(u\times\omega)\) 的归一化 \(\dot H^{-1}\) 作用量、时间零点或平方斜率总账。其 tent 项不能直接替换 \(\mathscr A_*\)。 |
| F-L2 | T. Tao, *A quantitative formulation of the global regularity problem for the periodic Navier--Stokes equation* (2009), Theorem 1.4 and Proposition 2.2；[arXiv:0710.1604](https://arxiv.org/html/0710.1604) | 将周期 NSE 的定性全局正则性与统一的定量 \(H^1\) 先验界等价起来；对 \(\|u_0\|_{H^1}\le A\) 给出 \(T=cA^{-4}\) 的标准局部强解时间。它准确说明任何成功路线最终都必须产生统一定量估计。 | 在 R0.72E 家族中 \(A\asymp\delta\)，通用保证时间只有 \(O(\delta^{-4})\)，短于首批 Bessel 根的 \(O(\delta^{-1})\) 时间尺度。该局部理论既不支付 \(\mathscr A_*\)，也不控制完整时间根总账。 |
| F-L3 | J.-Y. Chemin and F. Planchon, *Self-improving bounds for the Navier--Stokes equations* (2012), Proposition 3.1；[arXiv:1111.1356v2](https://arxiv.org/html/1111.1356v2) | 对非线性余项 \(w=u-e^{t\Delta}u_0\) 建立含 \(t^{-1/2}\) 与 \(t^{-3/2}\) 的缩放能量估计，右端由临界 Besov 数据控制。它是与 R0.72F 最近的“初始时刻奇异权可以进入 NSE 能量法”实例。 | 权重作用在 Duhamel 余项能量上，右端使用临界 Besov 范数；它不是任意 Leray 解上由动能单独支付的 Lamb 向量比值，也没有 \(s^{-1/3}\log(e/s)\) 的最小性、耦合振幅探测或时间根采样结论。 |
| F-L4 | R. Temam, *Navier--Stokes Equations and Nonlinear Functional Analysis*, 2nd ed.；[原始专著 PDF](https://ftp.mi.fu-berlin.de/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf) | Leray--Hopf 弱解、能量不等式、Galerkin 构造以及相关函数空间框架。R0.72F 的“可支付”部分只调用这一层级的能量信息，再加上显式 Sobolev 对偶与插值。 | 该框架不给出带 \(w_*\) 的投影 Lamb 向量估计，不识别固定频率支撑上的增长耦合尺度，也没有从能量不等式推出时间零点斜率总和。经典框架本身不能填补 (0.1) 的迹打包步骤。 |
| F-L5 | R. Yang, *Vorticity interior trace estimates and higher derivative estimates via blow-up method*；Theorem 1.1，[arXiv:2308.09350](https://arxiv.org/html/2308.09350)，[期刊 DOI](https://doi.org/10.1016/j.jde.2025.113486) | 对经典 NSE 解在随时间变化的 Lipschitz 空间子流形 \(\Gamma_t\) 上建立涡量及高阶导数的内部迹估计，并把界归结为耗散尺度函数与 \(\|\nabla u\|_{L^2_{t,x}}\)。它表明能量控制可以支付某些真正的空间迹。 | 这里的“迹”取在空间或时空图上，不是一个傅里叶坐标的离散时间零集；定理不估计 \(\sum_{F_0(t_k)=0}|F_0'(t_k)|^2\)，也不产生 (0.1) 的 \(D^{1/3}\) 归一化。 |
| F-L6 | A. Cheskidov and M. Dai, *Regularity criteria for the 3D Navier--Stokes and MHD equations* (2016), Theorem 1.1；[arXiv:1507.06611v6](https://arxiv.org/html/1507.06611v6) | 用随解变化的耗散波数 \(Q_r(t)\) 和高于该波数的 Littlewood--Paley 涡量占用量给出继续性判据。它是能够动态识别“振幅--频率活跃区”的近邻路线。 | 判据是附加的小量/可积条件，不是由 Leray 动能自动支付的先验界；观测量是空间频带中的 \(L^\infty\) 涡量，不是投影 Lamb 向量的负 Sobolev 作用，也不计数指定坐标的时间根。 |
| F-L7 | R. Yu, *Filtered Vortex Stretching and Subgrid Defects for the Three-Dimensional Navier--Stokes Equations* (2026), Theorems 2.1--2.2；[arXiv:2606.27560v1](https://arxiv.org/html/2606.27560v1) | 在滤波尺度上把近场正涡量拉伸压到成对角度缺陷，再由局部 palinstrophy、重叠量和尺度比支付。它给出当前的一手“几何耗尽 + 尺度局部化”比较。 | 估计依赖滤波尺度、几何缺陷和局部强度；它既不是全局能量支付的 \(\mathscr A_*\)，也没有初始层临界对数、固定支撑耦合参数或时间零点平方斜率账本。 |
| F-L8 | N. Lerner and F. Vigneron, *On some properties of the curl operator and their consequences for the Navier--Stokes system*；[arXiv:2203.07950](https://arxiv.org/html/2203.07950)，[DOI](https://doi.org/10.4208/cmr.2021-0106) | 对 divergence-free 场对角化 curl，分解正负 spin 分量，并把 NSE 非线性写成叉积/行列式结构；文中讨论能量、helicity 和临界 determinant 的正则性意义。这为选择 \(u\times\omega\) 作为几何观测量提供直接邻域。 | 其 determinant 与 spin 判据不等同于 \(\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2/Y\)；论文没有给出初始层加权支付，也没有完整时间根的离散迹不等式。 |
| F-L9 | C. Foias, C. Guillopé, and R. Temam, *New a priori estimates for Navier--Stokes equations in dimension 3* (1981)；[DOI](https://doi.org/10.1080/03605308108820180) | 建立三维 NSE 高阶空间导数的先验时间平均估计，是从基本能量层向正时间高阶正则量推进的经典来源。它说明耗散可以控制一族空间导数积分，但控制形式和指数必须逐项核对。 | 论文不处理左端点奇异的 Lamb 向量比值，不给出 R0.72E 的固定载波振幅响应，也没有把高阶空间平均转化为零点处的平方斜率和。它不能被概括成 (0.1) 的现成证明。 |
| F-L10 | S. Kusuoka and D. Stroock, *Applications of the Malliavin calculus, Part II* (1985), Corollary (3.25) and inequality (3.27), pp. 22--23；[原始仓储记录](https://repository.dl.itc.u-tokyo.ac.jp/records/39529)，[DOI](https://doi.org/10.15083/00039520) | 在包含由漂移括号生成缺失方向的统一条件下，给出转移密度及其导数的定量估计。R0.72E 用它支付随机相位扩散的多项式密度界，进而控制未加权 \(A_q^{-1}\) 作用量。 | 它不是 NSE 正则性定理，不包含 \(w_*\)、Leray 能量、时间根或 \(D^{1/3}\) 账本。它只支撑被 R0.72F 继承的精确反例族作用量估计，不能证明候选修复。 |

## 2. 三条最接近的路线为何仍未碰撞

### 2.1 临界初始层范数不是当前作用量

Koch--Tataru 的 tent 平方项和 Chemin--Planchon 的时间加权余项能量都
证明：初始层权重并非人为装饰，热尺度与非线性确实会自然地产生这类量。
但二者都绑定于 mild/强解结构和临界数据空间。R0.72F 所需的第一步更弱也
更特殊：只从

\[
 u\in L_t^\infty L_x^2\cap L_t^2\dot H_x^1
\]

支付一个归一化的投影 Lamb 向量作用量。已核验来源没有给出从前两种
临界框架到这一量的等价或支配关系。

### 2.2 动态频率或空间迹不是时间零点迹

Cheskidov--Dai 会追踪活跃耗散波数，Yang 会把能量耗散压到空间子流形，
Yu 会在滤波尺度上分解涡量拉伸。这三类结果都比静态初值频率矩更能看见
解的动态结构；但它们的观测集合分别是频带、空间图和尺度局部相互作用。
R0.72F 的缺口是离散时间集合

\[
 \{t:F_0(t)=0\}
\]

上的平方斜率总量。把空间/频率控制转成这一离散时间迹，需要新的采样或
变差机制，不能只改写已有定理的符号。

### 2.3 几何非线性描述不是能量支付

Lerner--Vigneron 解释了 curl、spin 与叉积非线性的几何结构，
Foias--Guillopé--Temam 则给出高阶耗散平均。二者都能帮助判断应该观察
什么，但都不自动把

\[
 \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}
 {\|\omega\|_2^2}
\]

变成一个只由初始动能和区间长度控制、同时还能支付完整根账本的量。
R0.72F 中 \(\beta<1/2\) 的支付估计必须直接从 Sobolev 对偶、插值和
Leray 能量不等式证明；它不是上述文献中某个结论的重新命名。

## 3. 本次审计允许写入报告的边界

我只允许据此写出下面四点。

1. 奇异初始层权、动态频率、空间迹、滤波涡量拉伸和 curl 几何都有严格
   的一手先例，但它们控制的是不同量。
2. R0.72F 已证明的 \(\beta<1/2\) 能量支付和 R0.72E 选定根上的
   \((\beta,\gamma)=(1/3,1)\) 饱和，是本项目内部的解析筛选；不能把它们
   扩写成完整根控制。
3. 候选式 (0.1) 仍是问号。当前没有完整根上界、重启/二进覆盖定理，也
   没有从该候选推出延拓或正则性的证明。
4. 固定频率支撑上的有限个归一化初值矩在 R0.72E 家族中保持有界；
   已核验来源没有提供一个现成定理，把这种静态信息升级为所需的耦合尺度
   或时间根总账。

## 4. 检索边界与非碰撞声明

这次审计以截至 2026-08-27 可核验的一手论文、作者稿、出版社 DOI 和
原始专著为限，集中检查以下交叉点：临界初始层空间、时间加权能量、
Leray 支付、动态耗散频率、空间迹、涡量拉伸、curl 几何、高阶导数平均、
弱 Hörmander 密度，以及时间零点斜率采样。

“未发现同时满足四项条件的定理”只描述这组有界核验。它不表示我穷尽了
Navier--Stokes 文献，也不证明不存在另一种等价表述。后续若要声称
原创性或优先权，仍需独立的系统检索、专家核查和正式同行评议。
