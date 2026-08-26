# R0.71P 一手文献核查：正进入变差、时间零点与定量计数边界

**核查日期：2026-08-26**  
**性质：两轮 bounded primary-source audit，不是原创性、优先权或不存在性证明。**

## 1. 需要区分的三个对象

对一个内部有限阶 denominator zero，R0.71O 给出左右迹 \(A_-\)、
\(A_+\)。R0.71P 必须区分

\[
 \text{ordinary hard BV 正原子}=(A_+-A_-)^+,
\]

\[
 \text{逐分量 soft/分段正进入原子}=A_+,
\]

以及更强的 total-Jordan cost \(A_-+A_+\)。前两者相差

\[
 A_+-(A_+-A_-)^+=\min(A_+,A_-).
\]

偶阶 touch 可以让 ordinary hard BV 正原子为零，同时保留完整 \(A_+\)。
因此不能直接把本站的正进入和称为 ordinary positive variation，也不能
把逐 shell--cell 先取 soft 正部再求和的 relaxed measure，称为 signed
aggregate 的正 Jordan 部。

在半开窗口 \(K=[a,b)\) 上，若窗口从正分母分支内部开始，zero padding
产生的左端上升是单独的 initial trace；从 segmented positive variation
扣除 branch-interior variation 与该 initial trace 后，才精确得到内部
entries 与左端零 entry 的总和。

对非负权重 \(w_{j,Q}=\kappa_j^{-2}\)，Tonelli 给出精确层析式

\[
 \sum_{j,Q}w_{j,Q}\sum_{t_0\in\mathcal Z^+_{j,Q}(K)}A_{j,Q,+}(t_0)
 =\int_0^\infty
 \sum_{j,Q}w_{j,Q}
 \#\{t_0\in\mathcal Z^+_{j,Q}(K):A_{j,Q,+}(t_0)>s\}\,ds.
\]

这里数的是 zero-padded/soft amplitude 对正幅值层 \(s\) 的向上进入，
不是 \(d_Q\ge0\) 对零层的符号穿越。

## 2. Claim-to-source ledger

| 一手来源 | 直接支持 | 不能支持 |
|---|---|---|
| Fleming--Rishel, *An integral formula for total gradient variation* (1960), [Springer 原文页](https://link.springer.com/article/10.1007/BF01236935) | coarea 将已经受控的 \(\lvert Du\rvert\) 写成 level-set perimeter 的积分；一维化后连接 variation 与 crossing count | 不区分坍缩在同一点的 \(A_+\)、\(A_-\)；不从 Leray energy 生成 BV |
| Rafał M. Łochowski, *On a generalisation of the Banach indicatrix theorem* (2015/2016), [arXiv v4](https://arxiv.org/abs/1503.01746v4) | Theorem 1 与式 (6)--(8) 把 upward/downward/truncated variation 写成 level crossings 的积分 | 作用于 ordinary hard representative 时只看到 \((A_+-A_-)^+\)；恢复 \(A_+\) 必须先采用 soft 或分段补零代表；表示已有 variation，不提供 NSE payment |
| Vol'pert, *The spaces \(BV\) and quasilinear equations* (1967), [MathNet 原文](https://www.mathnet.ru/eng/sm4127) | 固定光滑复合映射的 BV chain-rule 背景 | soft map 的导数随 \(\varepsilon\downarrow0\) 退化；不给 uniform face sum |
| Roger Temam, *Navier--Stokes Equations and Nonlinear Functional Analysis*, 2nd ed., [SIAM Chapter 7](https://epubs.siam.org/doi/10.1137/1.9781611970050.ch7) | Theorem 7.1 与 Remark 7.1 将三维时间解析性限制在 classical \(H^1\)-regular interval 内；固定 bounded observable 因而为 Hilbert 值解析函数 | 不穿过潜在奇性端点；不给跨解、壳、小区的统一零点数、阶数、间距或 transversality |
| Kyuya Masuda, *On the Analyticity and the Unique Continuation Theorem for Solutions of the Navier--Stokes Equation* (1967), [J-STAGE PDF](https://www.jstage.jst.go.jp/article/pjab1945/43/9/43_9_827/_pdf/-char/en), [DOI](https://doi.org/10.3792/pja/1195521421) | Theorem 1 给解析性；Theorem 2 给完整速度场在一个时刻于空间开集消失时的唯一延拓 | \(C_{j,Q}(t_0)=0\) 只是 filter/cutoff observable 落入算子核，不等于完整速度在空间开集消失，不能计数 projection zeros |
| Foias--Temam, *Gevrey class regularity for the solutions of the Navier--Stokes equations* (1989), [DOI](https://doi.org/10.1016/0022-1236(89)90015-3) | 周期正则解的空间 Gevrey 正则性与 Fourier 衰减 | per-time 空间幅值衰减不控制时间零点重复次数，也不给 projection lower anchor |
| Giga--Jo--Mahalov--Yoneda, *On time analyticity ... with spatially almost periodic data* (2008), [DOI](https://doi.org/10.1016/j.physd.2008.03.007) | Theorems 1.1、1.2 给时间解析性；Theorem 1.4 给 Fourier mode 的 no-sudden-creation | 不能排除孤立重复过零；物理 cutoff observable 也不是单个 Fourier mode |
| Jean Leray, *Sur le mouvement d'un liquide visqueux emplissant l'espace* (1934), [Springer 原文页](https://link.springer.com/article/10.1007/BF02547354) | 弱解与基本能量不等式的原始框架，提供 Lebesgue-time 积分预算 | 时间积分不能控制零测集合上的反复取样，也不控制 \(C/\lVert C\rVert\) 在 \(C=0\) 附近的方向变差 |

## 3. 时间解析性的准确正结果

若 \(K=[a,b)\) 且 \(\overline K=[a,b]\Subset I_{\mathrm{strong}}\)，固定
\(C_{j,Q}\) 不恒为零，则其 Hilbert 值 Taylor 级数有首个非零系数。
每个零点因此孤立且有限阶，\(\overline K\) 上零点有限。对固定有限个
\((j,Q)\)，正进入和有限。

该结论没有统一常数。它不能升级为：

- 全壳、全小区统一零点数；
- 接近潜在奇性端点的 packing bound；
- 从 spatial Gevrey decay 推出 temporal crossings；
- 用 Masuda 唯一延拓删除 filtered-observable zeros；
- 从 Leray energy 支付正进入和。

## 4. 定量解析路线需要的额外输入

若一个 Hilbert 值 observable 在复圆盘 \(D(t_*,R)\) 解析，满足

\[
 \sup_{D(t_*,R)}\lVert C(z)\rVert\le M,
 \qquad C(t_*)\ne0,
\]

则在 Hilbert 空间复化后，选取在 \(C(t_*)\) 上取范数的单位复线性泛函，
再用 Jensen 公式可得 distinct vector-zero count

\[
 N_C(D(t_*,r))
 \le\frac{\log(M/\lVert C(t_*)\rVert)}{\log(R/r)},
 \qquad0<r<R.
\]

标量 Jensen count 按重数计，只会更大。这条条件路线显式要求
complex-time radius、整盘上界 \(M\)、非退化 anchor
\(\lVert C(t_*)\rVert\) 与窗口覆盖。当前 Leray 预算没有给出这些量的
统一版本。

## 5. Bounded negative finding 与停止理由

截至 2026-08-26 的两轮限定检索，没有定位到从三维 NSE/Leray energy、
时间解析性、唯一延拓或空间频率衰减直接控制

\[
 \sum_{j,Q}\kappa_j^{-2}\sum_{t_0}A_{j,Q,+}(t_0)
\]

的定理。现有工具只能在已经拥有 segmented-BV、level-upcrossing、统一
zero count、transversality/inverse-denominator、componentwise
positive-source bound 或定量 complex-time anchor 的条件下使用。

停止检索的原因是：正变差与 crossing 的精确对应、三维时间解析性的有效
区间、唯一延拓的对象错配、以及 spatial Gevrey decay 的能力边界都已由
原始来源确定；继续宽泛检索不太可能改变本节判断。该负面结论不是“不存在
此类定理”的证明，也不支持原创性或优先权表述。
