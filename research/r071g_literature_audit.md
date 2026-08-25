# R0.71G 一手文献审计：时频占据、坏区间与正号伸长

日期：2026-08-25

状态：bounded primary-source audit

## 直接结论

我围绕“固定高频 signed projected-Lamb 迹能否由标准 NSE 预算推出
\(K^{-2}\) 物理时间驻留”做了两轮定向核对。最接近的既有结果分为四类：

1. 动态耗散波数和带指标函数的时频正则判据；
2. 高阶导数比的 good/bad intervals 及坏区间宽度；
3. 只保留正号应变的临界正则判据；
4. 带 commutator、远场和其余 shell 可和性假设的 filtered stretching
   闭合。

这些结果没有给出下列单向推导：

\[
 \text{standard Leray--Hopf budgets}
 \Longrightarrow
 \bigl|\{t:B^{L,+}_{K,Q}(t)>\lambda\}\bigr|
 \lesssim K^{-2}\Phi(\lambda,E_0,\nu),
 \tag{1.1}
\]

其中左侧同时固定 LP 输出壳、signed projected-Lamb 配对和移动局部柱。
这是本次限定检索的结果，不是文献不存在证明，也不是原创性或优先权
结论。

## Claim-to-source ledger

| 一手来源与条目 | 已证明的逻辑 | 与 R0.71G 的交集 | 不能推出的部分 |
|---|---|---|---|
| [Cheskidov--Shvydkoy, arXiv:1102.1944v2](https://arxiv.org/abs/1102.1944v2), Thm. 3.1, Cor. 3.3, Lem. 4.1 | 动态耗散波数 \(\Lambda(t)\) 分开高模黏性区和低模 Euler 区；低模涡量的时间可积性推出正则；每个 Leray--Hopf 解只有无条件 \(\Lambda\in L_t^1\)，而 \(\Lambda\in L_t^{5/2}\) 足以正则。 | 真正的动态频率阈值和物理时间基线。 | 由 \(L^1\) 与 Chebyshev 只得 \(|\{\Lambda>K\}|\lesssim K^{-1}\|\Lambda\|_{L^1}\)，不是逐壳 \(K^{-2}\) 驻留；对象不含符号和局部中心。 |
| [Cheskidov--Dai, arXiv:1507.06611v6](https://arxiv.org/abs/1507.06611v6), Thm. 1.1, 1.3 | 若活跃耗散频率区中 \(\mathbf1_{\{q\le Q_r(t)\}}\|\Delta_q\omega\|_\infty\) 的时间积分在高频足够小，则解可延拓；也给出从 \(\mathcal T_q\) 到候选奇性时刻的壳涡量条件。 | 这是本次找到的最接近“壳处于活跃区时的加权 occupation”公式。 | 该积分小量是正则性假设，不是标准能量推出的估计；没有 signed work、移动 cutoff 或未加权 \(K^{-2}\) 时长。 |
| [Bradshaw--Grujić, arXiv:1501.01043v2](https://arxiv.org/abs/1501.01043v2), Thm. 2 | 用动态 Besov 端点定义有限频率窗，并以局部存在时间和 escape times 选择采样时刻。 | 频率窗和抛物时间尺度的严格先例。 | 时间尺度依赖整体 Besov 振幅，不是固定 signed 壳迹的驻留定理。 |
| [Gibbon--Doering, arXiv:math/0406146](https://arxiv.org/abs/math/0406146), bad-interval width theorem | 用高阶导数能量比 \(\kappa_n\) 分割 good/bad intervals，并以 Reynolds 数给出所选坏区间宽度上界。 | 已发表的 active-event residence-time 型结果。 | 对象是全局高阶 Sobolev 比，不是 LP 壳的 Lamb 商；尺度写成 \(Re\) 和 \(\omega_0\)，不是逐壳 \(K^{-2}\)。 |
| [Miller, arXiv:1710.05569v4](https://arxiv.org/abs/1710.05569v4), Thm. 1.1 | 应变矩阵中间特征值正部 \(\lambda_2^+\) 的临界时空范数控制 enstrophy；有限时爆破迫使相应积分发散。 | 一个真正 sign-sensitive 的正号生产判据。 | 它假定临界积分，不提供 occupation 的生成机制；物理空间特征值不等于过滤 Lamb 配对。 |
| [Lerner--Vigneron, arXiv:2203.07950v1](https://arxiv.org/abs/2203.07950v1), eqs. (28)--(32) | 严格使用 \(\mathbb P((u\cdot\nabla)u)=\mathbb P((\nabla\times u)\times u)\)，并把弱非线性写成有符号行列式。 | projected-Lamb 代数已有明确先例。 | 没有 LP 驻留、occupation measure 或 moving-partition 时间账本。 |
| [Yu, arXiv:2606.27560v1](https://arxiv.org/abs/2606.27560v1), Thm. 9.3, 10.3 | 在远场、commutator increment 和其余 localization/shell budgets 可和等额外假设下，filtered vortex-stretching surplus 可和并趋零。 | 对象层面最接近 filtered positive stretching 与跨壳 defect。 | 结论沿尺度方向且是条件性的；关键可和性没有由 Leray energy 推出，也没有物理时间驻留。 |
| [Cheskidov--Dai, arXiv:1510.00379v3](https://arxiv.org/abs/1510.00379v3) | 用 intermittency dimension 控制完整有界轨道的平均耗散波数和确定模数量。 | 可比较 active volume 和动态波数的长期统计。 | 受迫周期系统的完整有界轨道不是首次候选奇性前的 fixed-shell signed residence。 |

## 无条件基线少一个频率幂

Cheskidov--Shvydkoy 的 Lemma 4.1 给出

\[
 \Lambda\in L^1(0,T)
 \tag{3.1}
\]

而不是 \(L^2\) 或更强。于是标准 Chebyshev 步骤只有

\[
 |\{t:\Lambda(t)>K\}|
 \le K^{-1}\int_0^T\Lambda(t)\,dt.
 \tag{3.2}
\]

R0.71G 想要的黏性驻留尺度是 \(K^{-2}\)。两者相差一个频率幂。
这只是逻辑比较：\(\Lambda(t)\) 与 signed Lamb 商不是同一个量，不能把
(3.2) 当成后者的下界或反例。

同文还给出在 \(\Lambda>1\) 时的比较

\[
 \Lambda^2\lesssim
 \|\omega_{\le Q(t)}\|_{B^0_{\infty,\infty}}
 \lesssim\Lambda^{5/2},
 \tag{3.3}
\]

并由更强的低模涡量条件得到正则。该结构说明：把 \(K^{-1}\) 尾界升级为
\(K^{-2}\) 不能只靠重命名耗散波数；必须增加可传播的动力学预算。

## 最接近的时频 occupation 判据仍是条件

Cheskidov--Dai 定义 \(\Lambda_r(t)=\lambda_{Q_r(t)}\)，并在 NSE 情形
给出如下类型的条件：

\[
 \limsup_{q\to\infty}
 \int_{T/2}^{T}
 \mathbf1_{\{q\le Q_r(t)\}}
 \|\Delta_q\omega(t)\|_\infty,dt
 \le c_r.
 \tag{4.1}
\]

该式确实同时保留频率指标和物理时间，是 R0.71G 必须比较的近邻。
不过它的逻辑方向是“小量条件推出延拓”。论文没有从 Leray energy 推导
(4.1)。若 R0.71G 直接假定同类壳积分，只会把目标改写成另一项正则性
假设。

## 坏区间宽度不是固定壳驻留

Gibbon--Doering 的 bad intervals 来自高阶导数能量比，论文摘要也明确
说明坏区间宽度随 Reynolds 数增长而缩小。这是一条真正的区间宽度
结果，不能忽略。

但其区间判据含 \(\kappa_{n+1}/\kappa_n\)、\(Re\) 和阶数参数；它不固定
Littlewood--Paley 输出壳，也不保留 signed Lamb/vortex-stretching 配对。
因此它提供概念近邻和证明模板，不直接填补 R0.71G 的账本。

## 正号判据与 filtered stretching 的边界

Miller 的 \(\lambda_2^+\) 判据证明“只保留正号生产”可以形成临界正则
条件。R0.71G 若最终只把 signed Lamb 量上界到该已知范数，将只是既有
判据的推论；它还必须说明新的 occupation 预算来自哪里。

Yu 的近期预印本更接近过滤伸长对象，但其闭合依赖 far-field、commutator
和其余 shell budgets 的额外可和性。它的结论是尺度方向的 surplus
可和与消失，不是物理时间的逐壳驻留。R0.71G 不能把这些条件性输入写成
标准能量的自动后果。

## 检索边界后的表述

最安全的文献结论是：已有研究分别建立了动态耗散波数、时频正则判据、
高阶坏区间宽度、正号应变判据和条件性 filtered stretching 闭合；在本次
限定检索中，尚未找到由标准 NSE 预算导出的、固定高频 signed
projected-Lamb 迹的 \(K^{-2}\) 物理时间驻留估计。

这句话只描述八组已核对主源的重叠边界。它不能支持“首次”“唯一”或
全局文献不存在等表述。
