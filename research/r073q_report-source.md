# R0.73Q | A critical heat-flow tube beyond the \(H^{1/2}\) entrance

**Status:** continuum proof, primary-source audit, independent formula
certificate, and formal figure package passed; public rendering is
release-ready

**Public title (zh):** R0.73Q｜越过 \(H^{1/2}\) 入口的临界热流稳定管

## 1. 直接结论

R0.73Q 在固定的三维周期 Navier--Stokes 方程上，给一条先验全局
\(H^3\) 强参考轨道增加了一条比 \(H^{1/2}\) 更弱的强稳定入口。

对平均零扰动 \(f\)，定义具体的热流迹范数

\[
 \|f\|_{\mathfrak X}
 :=\left(\int_0^\infty
 \|e^{t\Delta}f\|_6^4\,dt\right)^{1/4}.
 \tag{1.1}
\]

它等价于周期临界 Besov 范数
\(\dot B^{-1/2}_{6,4}\)，但 (1.1) 不含未说明的 Littlewood--Paley
截断，因此可以直接复算。

若

\[
 u\in C([0,\infty);H^3_{\sigma,0})
 \cap L^2_{\rm loc}([0,\infty);H^4_{\sigma,0})
\]

是固定的先验全局强解，则存在一个正半径
\(\rho_{\mathfrak X}[u]>0\)，使对每个起始时刻 \(t_0\ge0\) 和每个
\(H^3\) 初值 \(v_0\)，只要

\[
 \|v_0-u(t_0)\|_{\mathfrak X}<\rho_{\mathfrak X}[u],
 \tag{1.2}
\]

从 \(v_0\) 出发的解就全局保持 \(H^3\)，并且差值属于
\(L^4((t_0,\infty);L^6)\)。同一个半径适用于所有重启时刻。

这个结论确实增加了旧 \(H^{1/2}\) 稳定域所不包含的光滑数据。令

\[
 w_N(x)=N^{-1/4}e_2\sin(Nx_1).
 \tag{1.3}
\]

则

\[
 \|w_N\|_2\to0,
 \qquad
 \|w_N\|_{\mathfrak X}\to0,
 \qquad
 |w_N|_{1/2}\to\infty.
 \tag{1.4}
\]

所以充分大的 \(N\) 会进入新热流管，却离开任意固定半径的
\(H^{1/2}\) 球。严格的发布集合是旧管与新管的并集，而不是把两个
来源不同的半径强行排序。

这一步关闭的是一类有热扩散结构的高频入口，不是任意
\(L^2\)-小初值。一般的早期 \(L^2\)-only 强正则问题仍然开放，Clay
问题的状态没有改变。

## 2. 为什么选择 \(L^4_tL^6_x\)

在三维中，Serrin 临界关系为

\[
 {2\over r}+{3\over p}=1.
 \tag{2.1}
\]

取 \((r,p)=(4,6)\)，正好得到

\[
 E:=L^4_tL^6_x.
 \tag{2.2}
\]

这个选择同时完成三件事。

第一，初始热流的 \(E\) 范数就是 (1.1)，即
\(\dot B^{-1/2}_{6,4}\) 的热半群刻画。

第二，两个 \(E\) 场的乘积属于 \(L^2_tL^3_x\)，周期 Stokes 热核把
这个空间送回 \(E\)。因此非线性 Duhamel 映射在同一个空间闭合。

第三，一旦构造出全局 \(E\) mild 解，(2.1) 的 Serrin 继续性就能把
\(H^3\) 初值的局部强解延伸到所有时间。

这条路线位于有限指标临界 Besov 范围内，没有进入
\(BMO^{-1}\) 的 Carleson 端点。

## 3. 固定参考轨道只需要一个有限作用量

R0.73P 已证明

\[
 \mathcal A_{1/2}[u]
 :=\int_0^\infty |u(t)|_1^4\,dt<\infty.
 \tag{3.1}
\]

周期 Sobolev 嵌入给出

\[
 M[u]
 :=\|u\|_{L^4((0,\infty);L^6)}
 \le C_S\mathcal A_{1/2}[u]^{1/4}<\infty.
 \tag{3.2}
\]

对任意 \(t_0\ge0\)，参考轨道的尾部满足

\[
 \|u\|_{L^4((t_0,\infty);L^6)}\le M[u].
 \tag{3.3}
\]

因此所有重启后的常数都能用同一个全轨道作用量控制。这里不需要
把 \(\mathbb R^3\) 的连续缩放原样移植到固定环面，也不需要假设轨道
在每个短区间天然很小。

## 4. 周期双线性估计

定义

\[
 \mathcal B(a,b)(t)
 :=\int_0^t e^{(t-s)\Delta}P\nabla\!\cdot(a\otimes b)(s)\,ds.
 \tag{4.1}
\]

周期 Stokes 热核满足

\[
 \|e^{\tau\Delta}P\nabla\!\cdot F\|_6
 \le C_O k(\tau)\|F\|_3,
 \tag{4.2}
\]

其中

\[
 k(\tau)\lesssim
 \begin{cases}
 \tau^{-3/4},&0<\tau\le1,\\
 e^{-c\tau},&\tau>1.
 \end{cases}
 \tag{4.3}
\]

短时间的 \(3/4\) 由一个空间导数的 \(1/2\) 和
\(L^3\to L^6\) 热平滑的 \(1/4\) 相加得到。长时间则使用平均零输出
和第一 Stokes 特征值。

令

\[
 g(s)=\|a(s)\|_6\|b(s)\|_6.
\]

则

\[
 \|g\|_2\le\|a\|_E\|b\|_E.
\]

一维 Hardy--Littlewood--Sobolev 映射

\[
 I_{1/4}:L^2_t\to L^4_t
\]

控制短时间核，长时间指数核由 Young 不等式控制，最终得到

\[
 \boxed{
 \|\mathcal B(a,b)\|_E
 \le C_B\|a\|_E\|b\|_E.}
 \tag{4.4}
\]

普通 Young 卷积不能替代短时间 HLS：
\(\tau^{-3/4}\notin L^{4/3}(0,1)\)。这一个对数端点是后面区分有限
指标 Besov 与裸 Kato 上确界的关键。

## 5. 大参考轨道的线性化逆

把起始时刻移到零，记 \(U(s)=u(t_0+s)\)，并定义交叉算子

\[
 \mathcal L_Uz=\mathcal B(U,z)+\mathcal B(z,U).
 \tag{5.1}
\]

当参考轨道很大时，不能要求 \(2C_B\|U\|_E<1\)。取

\[
 \varepsilon_B={1\over4C_B}
\]

并按可加作用量 \(\int\|U(t)\|_6^4dt\) 切分时间轴，使每段满足

\[
 \|U\|_{E(I_j)}\le\varepsilon_B.
\]

所需段数至多

\[
 N[u]\le1+\left({M[u]\over\varepsilon_B}\right)^4.
 \tag{5.2}
\]

在第 \(j\) 段，局部交叉算子范数不超过 \(1/2\)，局部逆范数不超过
2。Duhamel 因果性保证历史项只包含此前区间上同一积分时刻的
\(U_{<j}z_{<j}\) 与 \(z_{<j}U_{<j}\)，不会产生跨时刻乘积。若

\[
 Z_j=\|z\|_{E(0,\tau_j)},
\]

则可逐段得到

\[
 Z_j
 \le(1+4C_BM[u])Z_{j-1}+2\|f\|_{E(I_j)}.
 \tag{5.3}
\]

因此 \(I+\mathcal L_U\) 可逆，并有一个故意保守但完全显式的上界

\[
 \boxed{
 K[u]
 =2\widehat N[u]^{3/4}
 (1+4C_BM[u])^{\widehat N[u]-1},}
 \tag{5.4}
\]

其中 \(\widehat N[u]\) 是 (5.2) 右侧的安全整数上界。由于所有尾部
作用量都不超过 \(M[u]\)，(5.4) 对每个 \(t_0\) 同时有效。

这个常数很差，不代表最优稳定半径；它的作用是把“可以分段”变成
一条可核查的有限递推。

## 6. 二次固定点与全局 H3 延拓

令

\[
 R_U=(I+\mathcal L_U)^{-1},
 \qquad
 \delta=\|e^{t\Delta}w_0\|_E.
\]

差分方程等价于

\[
 w=R_Ue^{t\Delta}w_0-R_U\mathcal B(w,w).
 \tag{6.1}
\]

在半径 \(2K[u]\delta\) 的 \(E\) 球上，只要

\[
 \delta<\rho_{\mathfrak X}[u]
 :={1\over8C_BK[u]^2},
 \tag{6.2}
\]

右侧就把球送回自身，并且压缩常数小于 \(1/2\)。所以存在唯一的
全局 \(E\) mild 差值，并满足

\[
 \|w\|_{L^4((t_0,\infty);L^6)}
 \le2K[u]\|w_0\|_{\mathfrak X}.
 \tag{6.3}
\]

若初值属于 \(H^3\)，局部强解在其最大存在区间内与这个 mild 解
一致。若最大时刻 \(T_*<\infty\)，则

\[
 \|v\|_{L^4((t_0,T_*);L^6)}
 \le M[u]+2K[u]\delta<\infty.
 \tag{6.4}
\]

临界 Serrin 继续性把解延伸过 \(T_*\)，产生矛盾。因此解全局保持
\(H^3\)。R0.73P 的相对能量结论还给出

\[
 \|w(t)\|_2
 \le e^{\mathcal L[u]}e^{-(t-t_0)}\|w_0\|_2,
 \tag{6.5}
\]

所以新入口进入全局强解后仍在 \(L^2\) 中指数同步。

## 7. 新域为何真地越过 H1/2

周期 Bernstein 与 \(\ell^2\hookrightarrow\ell^4\) 给出

\[
 H^{1/2}=B^{1/2}_{2,2}
 \hookrightarrow B^{-1/2}_{6,2}
 \hookrightarrow B^{-1/2}_{6,4}\simeq\mathfrak X.
 \tag{7.1}
\]

因此一个匹配半径的小 \(H^{1/2}\) 球包含在热流球中。为了与
R0.73P 已发表的完整半径比较，必须保留两个证明各自的常数，定义

\[
 \mathcal D_P[u]
 =\{w_0:|w_0|_{1/2}<R_{1/2}[u]\},
\]

\[
 \mathcal D_Q[u]
 =\mathcal D_P[u]
 \cup\{w_0:\|w_0\|_{\mathfrak X}<\rho_{\mathfrak X}[u]\}.
 \tag{7.2}
\]

现在计算 (1.3)。归一化 Haar 测度下

\[
 \|\sin(Nx_1)\|_2={1\over\sqrt2},
 \qquad
 \|\sin(Nx_1)\|_6=\left({5\over16}\right)^{1/6}=:c_6.
\]

因为 \(e^{t\Delta}w_N=e^{-N^2t}w_N\)，

\[
 \|w_N\|_{\mathfrak X}
 ={c_6\over4^{1/4}}N^{-3/4},
 \tag{7.3}
\]

而

\[
 \|w_N\|_2={1\over\sqrt2}N^{-1/4},
 \qquad
 |w_N|_{1/2}={1\over\sqrt2}N^{1/4}.
 \tag{7.4}
\]

所以对充分大的 \(N\)，

\[
 \|w_N\|_{\mathfrak X}<\rho_{\mathfrak X}[u],
 \qquad
 |w_N|_{1/2}>R_{1/2}[u].
\]

这严格证明

\[
 \boxed{\mathcal D_P[u]\subsetneq\mathcal D_Q[u].}
 \tag{7.5}
\]

该剪切模自身满足 \((w_N\cdot\nabla)w_N=0\)，但定理的证明没有使用
这一自相互作用消失；交叉作用 \(u\cdot\nabla w_N+w_N\cdot\nabla u\)
仍由线性化逆统一控制。

## 8. 裸 Kato 上确界的精确 no-go

若只使用

\[
 \|w\|_{\mathcal K_6}
 =\sup_{t>0}t^{1/4}\|w(t)\|_6,
\]

并试图仅靠 \(u\in L^4_tL^6_x\) 控制交叉项，就会需要假映射

\[
 I_{1/4}:L^4_t\to L^\infty_t.
 \tag{8.1}
\]

取

\[
 g_n(s)=n^{-1/4}(1-s)^{-1/4}
 {\bf1}_{\{e^{-n}<1-s<1/2\}},
\]

则

\[
 \|g_n\|_4^4=1-\frac{\log2}{n}\to1,
\]

但在 \(t=1\)，

\[
 \int_0^1(1-s)^{-3/4}g_n(s)\,ds
 =n^{3/4}-n^{-1/4}\log2\to\infty.
 \tag{8.2}
\]

这关闭的是一条证明路线，不是否定 Kato 或完整
\(BMO^{-1}\) 稳定。Koch--Tataru 空间还包含局部 Carleson 能量项，
不能被一个裸上确界替代。

## 9. 一手文献碰撞与 2025/2026 端点边界

[Kato 1984](https://doi.org/10.1007/BF01174182) 给出
\(\mathbb R^3\) 临界 \(L^3\) 局部理论和小数据全局理论；
[Koch--Tataru 2001](https://doi.org/10.1006/aima.2000.1937) 给出完整
\(BMO^{-1}\) Carleson 空间中的唯一小全局解。两者都不是周期
\(L^2\)-only 定理。

[Iftimie 1999](https://doi.org/10.24033/bsmf.2358) 已在环面上构造了
围绕二维分量的各向异性稳定域；其定理再结合一个初等 Fourier 权重比较，
可见当 \(0<\delta<1/2\) 时该域严格宽于各向同性 \(H^{1/2}\)。因此
“周期稳定域可以大于 \(H^{1/2}\)”本身不是新发现；严格性不冒充论文原句。

最直接的碰撞是
[Gallagher--Iftimie--Planchon 2003 Theorem 3.1](https://doi.org/10.5802/aif.1983)：
在 \(\mathbb R^3\) 的有限指标临界 Besov 空间
\(\dot B^{3/p-1}_{p,q}\) 中，一条先验全局规范解周围的全局数据集合
是开集，并有全时 Lipschitz 差值估计。取 \(p=6,q=4\) 就得到新热流
拓扑的 whole-space 对应物。R0.73Q 因此只把固定环面、全重启统一和
显式逆常数组合成可审计推论，不作新理论或优先权声明。

[Auscher--Dubois--Tchamitchian 2004](https://doi.org/10.1016/j.matpur.2004.01.003)
的出版社摘要报告：在 \(\mathbb R^3\) 中，相应全局解所对应的 Cauchy
数据集合在 \(BMO^{-1}\) 拓扑中开放，解衰减并解析依赖于数据。本次未取得
全文定理公式，因此不从摘要重建半径、完整扰动量词或唯一性类。

端点的当前边界已经发生变化。
[Coiculescu--Palasek Theorem 1.2](https://doi.org/10.1007/s00222-025-01396-z)
在同一个标准三维环面上构造了一个 \(BMO^{-1}\) 初值及两条不同的
全局有限 \(X_{KT}\) 范数解，两者属于
\(C^\infty((0,\infty)\times\mathbb T^3)\cap
L^\infty_tBMO^{-1}\cap C_t^0\dot W^{-1,p}\)（每个 \(p<\infty\)）。
该初值不在 \(L^2\)，所以这不是 Leray--Hopf 非唯一性；Remark 1.3
称其为“不是零解附近的扰动”，但没有给出一个定量的大范数下界。该定理
已经否定其定理所列有限 \(X_{KT}\) 解类中的无条件唯一性。

[Mucha 2008](https://doi.org/10.4064/bc81-0-18) 的可核实定理仍把
\(L^2\) 小量阈值绑定到更高 Besov 迹范数。Mucha 2001 的出版摘要
高度相关，明确涉及三维环面、非平凡参考解和 \(L^2\)-小扰动，但本次
有界检索仍未取得完整定理公式，因此不从摘要重建其阈值依赖。

## 10. 研究价值判断

本节得到一个严格、正值、对所有起始时刻统一的临界热流稳定半径，
并给出一族同时满足

\[
 L^2\to0,
 \qquad
 \dot B^{-1/2}_{6,4}\to0,
 \qquad
 H^{1/2}\to\infty
\]

的光滑全局安全扰动。它比 R0.73P 的单纯带限
\(N^{-1/2}\) 范数转移更进一步：这里不是先用
\(H^{1/2}\) 小量进入，而是直接在更弱的热流拓扑中闭合非线性。

但整个机制仍属于临界 Besov/Serrin 扰动理论的周期轨道化推论。
whole-space 原理已有直接文献，周期二维核附近也有更早先例。因此
价值主要在四点：固定域量词明确、重启半径统一、线性化逆可审计、
严格扩域有精确证书。它不是一条可单独声称高原创性的主定理。

对千禧年问题，真正未跨越的障碍仍是：怎样在不预先假设临界热流、
频率包络或高阶范数小量的情况下，把任意光滑有限能量初值的早期
演化送入这类稳定域。R0.73Q 没有完成这一步。

## 11. 附图、证书与证据层级

正式附图只绘制两类可独立复算的解析量。

1. 对 \(w_N=N^{-1/4}e_2\sin(Nx_1)\)，绘制
   \(L^2\sim N^{-1/4}\)、热流迹 \(\sim N^{-3/4}\) 与
   \(H^{1/2}\sim N^{1/4}\) 的精确值。
2. 对 (8.2) 的端点反例，绘制保持有界的 \(\|g_n\|_4\) 与发散的
   分数积分输出。

这些是公式诊断，不是 Navier--Stokes 数值仿真。它们核对常数、
幂次和 no-go 边界，不能代替连续体双线性证明，也不能证明一般
数据全局正则。本节不需要 DGX；普通翻译也直接在本机完成。

| 证据层级 | 本节内容 | 可以支持 | 不能支持 |
| --- | --- | --- | --- |
| 已核对全文定理 | Kato、Koch--Tataru、Iftimie、GIP、Mucha 2008、Coiculescu--Palasek | 各自原域、原拓扑和原定理解类 | 固定环面的未写出量词或 \(L^2\)-only 结论 |
| 出版社摘要来源 | ADT 2004、Mucha 2001 | 摘要明确报告的域和定性结论 | 半径、完整扰动量词、精确阈值依赖或唯一性类 |
| 内部解析证明 | 周期 HLS 双线性、有限 Volterra 逆、二次固定点、Serrin 延拓 | 固定全局轨道周围的统一热流管 | 任意初值或非扰动型 \(BMO^{-1}\) 唯一性 |
| 独立解析审计 | 指数、历史项、固定点、端点延拓、集合严格性 | 证明内部一致性和量词边界 | 新颖性或最优常数 |
| 有限公式证书 | 单模三范数与时间端点反例 | 图表实现、常数和幂次复算 | 非线性 PDE 必要性、爆破或奇性 |
| 开放项 | 一般早期 \(L^2\)-only 入口 | 下一步问题定义 | 已解决的 Clay 结论 |

19 文件公式证书与 25 文件正式附图都已封印到不可变解析源提交
`cb9511c3af08a4beb0b31284e96e2a9c47a23d04`。该哈希只绑定证据来源和
声明范围，不扩大连续体定理。附图的矢量 PDF、SVG、600 dpi PNG、终尺寸、
灰度和 PDF 栅格检查均通过。

## 12. 下一步：把“频率”升级为“热扩散集中度”

R0.73R 将研究怎样从可计算的频谱和空间集中度上界推出
\(\mathfrak X\)-小量。单一 Fourier 模的 \(L^6/L^2\) 比值与最坏
Bernstein 饱和值相差一个频率幂，说明“最高频率 \(N\)”不足以描述
新入口；真正控制热流迹的是每个壳层的模态数、相位相干和空间集中。

下一门需要区分三层。

1. 给出逐壳层 \(L^6\) 集中系数和热衰减的严格充分条件。
2. 构造同一 \(L^2\) 与频率尺度、但热流迹截然不同的可复算数据族。
3. 判断是否存在比 \(B^{-1/2}_{6,4}\) 更宽、仍保留唯一 mild 分支的
   周期频率包络空间，同时避开非扰动型 \(BMO^{-1}\) 非唯一性端点。

这条路线仍然只会产生结构化充分条件。若无法去掉集中度条件，失败
本身会精确说明 \(L^2\)-only 入口缺少哪一个量。

## 13. 可直接发布的中文短文

### Lead

固定一条先验全局强轨道后，初始差不必在 \(H^{1/2}\) 中很小；只要
它的线性热流属于一个足够小的 \(L^4_tL^6_x\) 球，非线性交叉项就能
通过有限时间分段闭合，并得到对所有重启时刻统一的全局 \(H^3\)
稳定半径。

### Home

R0.73Q 增加了一个周期 \(\dot B^{-1/2}_{6,4}\) 热流入口。显式剪切
模可以同时满足 \(L^2\to0\)、热流迹 \(\to0\)，却有
\(H^{1/2}\to\infty\)；因此新旧稳定管的并集严格扩大。任意
\(L^2\)-小数据仍未覆盖。

### Recap

这一节用周期 Stokes--HLS 双线性估计和有限 Volterra 递推，构造了
一个全起点统一的临界热流稳定管。精确 Fourier 族证明它加入了旧
\(H^{1/2}\) 管之外的光滑安全数据；裸 Kato 上确界则被一个时间端点
反例阻断。whole-space Besov 开放性属于已知文献，Clay 结论仍开放。

### Literature

Gallagher--Iftimie--Planchon 已证明 \(\mathbb R^3\) 临界 Besov 全局
解集合的开放性，Iftimie 的定理结合初等 Fourier 权重比较给出周期各向
异性扩域；Auscher--Dubois--Tchamitchian 的出版社摘要报告了 whole-space
\(BMO^{-1}\) 邻域开放性。Coiculescu--Palasek 的最新定理同时表明：
非扰动型周期 \(BMO^{-1}\) 数据在定理所列有限 \(X_{KT}\) 解类中可以不唯一。

### Next

R0.73R 将把单一频率上界升级为热扩散集中度证书：逐壳层追踪模态
数量、相位相干和 \(L^6/L^2\) 集中，寻找可计算的
\(\mathfrak X\)-入口，并明确它与一般 \(L^2\)-only 问题之间还差什么。

## 14. 精确排除

- 不证明任意 \(L^2\)-小初值从初时刻全局强正则。
- 不证明热流球包含 R0.73P 的整个数值 \(H^{1/2}\) 球；严格比较使用
  两管并集。
- 不把 \(K[u]\) 或 \(\rho_{\mathfrak X}[u]\) 写成最优常数。
- 不把单 Fourier 剪切模写成一般动力学的必要阈值。
- 不把裸 Kato 上确界的失败写成 Koch--Tataru 理论失败。
- 不证明非扰动型 \(BMO^{-1}\) 数据唯一；该命题在一般情形已经为假。
- 不把 Mucha 2001 的摘要重建成未取得的定理公式。
- 不把解析公式图写成 Navier--Stokes 仿真。
- 不作新颖性或优先权声明。
- 不证明任意三维光滑数据全局，不证明 Clay 问题。

精确公开标签是 **NOT CLAY**。

## 15. 机器账本

~~~text
periodicHeatFlowTraceB64MinusHalf=KNOWN
periodicStokesHLSBilinearEstimate=CLOSED_AFTER_AUDIT
uniformAllRestartLinearizedInverse=CLOSED_AFTER_AUDIT
uniformCriticalHeatFlowOrbitTube=CLOSED_AFTER_AUDIT
criticalHeatToGlobalH3Propagation=CLOSED_AFTER_AUDIT
strictExtensionOfR073PDomainByUnion=CLOSED
singleModeL2SmallHeatSmallH12Large=CLOSED_EXACT
bareKatoSupFromL4L6Action=BLOCKED_BY_ENDPOINT
fullKochTataruTheory=NOT_REFUTED
wholeSpaceBesovOrbitOpenness=KNOWN_DIRECT_COLLISION
wholeSpaceBMOInverseOrbitOpenness=KNOWN_ABSTRACT_COLLISION
nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL
uniformL2OnlyStrongThreshold=OPEN_COLLISION_SENSITIVE
earlyWeakIntervalRegularity=OPEN
arbitraryThreeDimensionalGlobalRegularity=OPEN
formulaDiagnosticValidation=PASS
formulaDiagnosticPackage=CLOSED
sourceCommitAssigned=TRUE
finalSeal=TRUE
formalFigurePackage=PASS
publicReleaseContent=READY
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
~~~
