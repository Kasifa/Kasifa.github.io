# R0.73L：非自伴绝热跟踪与匹配增长作用量

- **状态：** 解析定理 CLOSED；独立解析审计与对抗审计 PASS；有限诊断、独立重算与正式图件 PASS
- **检索与核验日期：** 2026-08-31（Asia/Shanghai）
- **作用范围：** 指定二维周期剪切行上的线性、非自治、非自伴演化
- **证据等级：** 连续算子证明 + 独立解析审计 + 有限维诊断；三者严格分账

> 这一节解决的不是 Navier--Stokes 千禧年问题，而是此前路线中的一个
> 明确中间障碍：R0.73K 已证明每一个冻结时刻都有一条一致隔离、rank-one
> 且条件良好的黏性不稳定谱支；R0.73L 进一步证明真实的慢变非自治演化
> 能在长达 \(D_*/\varepsilon\) 的快时间内跟踪它，而且总增益与谱作用量
> 之间只差一个不随 \(\varepsilon\downarrow0\) 发散的乘法常数。

## 1. 直接结论

令

\[
 B_\varepsilon(d)=\widetilde A(d)-\varepsilon L,
 \qquad D(B_\varepsilon(d))=H^2_{\rm per},
 \qquad 0\le d\le D_*:=1/450,
\]

并令 \(U_\varepsilon(d,s)\) 是

\[
 \varepsilon\partial_d u=B_\varepsilon(d)u
\]

的精确演化。R0.73K 给出实、代数简单的 selected eigenvalue
\(\lambda_\varepsilon(d)\) 及其 rank-one Riesz 投影
\(P_\varepsilon(d)\)。定义

\[
 \Phi_\varepsilon(d,s)
 :=\frac1\varepsilon\int_s^d\lambda_\varepsilon(r)\,dr.
\]

R0.73L 证明：存在 \(0<\varepsilon_L\le\varepsilon_K\) 和与
\(\varepsilon,D\) 无关的 \(0<c_L\le C_L<\infty\)，使得所有
\(0<\varepsilon\le\varepsilon_L\)、\(D\in[0,D_*]\) 以及所有单位初值
\(h_\varepsilon(0)\in P_\varepsilon(0)H\) 都满足

\[
 c_Le^{\Phi_\varepsilon(D,0)}
 \le \|U_\varepsilon(D,0)h_\varepsilon(0)\|
 \le C_Le^{\Phi_\varepsilon(D,0)}.
 \tag{R0.73L-1}
\]

而且有向量级相对跟踪

\[
 \|U_\varepsilon(D,0)h_\varepsilon(0)
 -U^{\rm a}_{\varepsilon,P}(D,0)h_\varepsilon(0)\|
 \le C_L\varepsilon e^{\Phi_\varepsilon(D,0)}.
 \tag{R0.73L-2}
\]

因此精确终点相对移动 selected line 的距离为 \(O(\varepsilon)\)，但并不
声称精确终点恰好落在该直线上。

由于 R0.73K 已证

\[
 \sup_{d\le D_*}|\lambda_\varepsilon(d)-\lambda_0(d)|
 \le C_\lambda\varepsilon,
\]

黏性作用量可以换成无黏作用量，代价只是改变常数：

\[
 c_L\exp\!\left(\frac1\varepsilon\int_0^D\lambda_0(r)\,dr\right)
 \le \|U_\varepsilon(D,0)h_\varepsilon(0)\|
 \le C_L\exp\!\left(\frac1\varepsilon\int_0^D\lambda_0(r)\,dr\right).
 \tag{R0.73L-3}
\]

同一条前向轨道还满足 action-resolved localization：

\[
 \frac{\|U_\varepsilon(s,0)h_\varepsilon(0)\|}
      {\|U_\varepsilon(D,0)h_\varepsilon(0)\|}
 \le C_L\exp\!\left[-\frac1\varepsilon
       \int_s^D\lambda_0(r)\,dr\right],
 \qquad 0\le s\le D\le D_*.
 \tag{R0.73L-4}
\]

式 \((\mathrm{R0.73L\text{-}4})\) 是同一条前向解在两个时刻的商；没有求解任何 backward
parabolic problem。

## 2. 为什么这一步不是“积分瞬时特征值”

非自伴系统的瞬时谱并不自动控制非自治传播子。Jordan nilpotent、投影
条件数、移动补空间中的 switching growth，以及快慢参数与黏性参数的
比例失配，都可能产生无界 prefactor。R0.73I 已记录了有限维 Jordan
反例，因此本节必须真正控制移动谱补空间，而不能把
\(\exp(\int\lambda/\varepsilon)\) 写下后便把余项称为“低阶”。

这里能够闭合，是因为下列性质同时成立：

1. selected branch 代数简单且 rank one；
2. \(\|P_\varepsilon(d)\|<9/5\)，并有一致 \(P_\varepsilon'\) 控制；
3. 冻结补空间相对 selected rate 有严格余隙：\(0.12<0.16\)；
4. 慢漂移在每个固定快时间块上只有 \(O(\varepsilon)\)；
5. 黏性参数与慢变参数是同一个 \(\varepsilon\)。

若把黏性 \(\nu\) 与慢变参数 \(\varepsilon\) 分开，只有
\(|\lambda_\nu-\lambda_0|=O(\nu)\) 时会出现
\(\exp[O(\nu/\varepsilon)]\)，bounded-prefactor 结论一般不能保留。

## 3. 证明的四个核心环节

### 3.1 Kato transport 的符号与纤维移动

定义

\[
 \mathcal K_\varepsilon=[P_\varepsilon',P_\varepsilon]
\]

和修正演化

\[
 \partial_dU_\varepsilon^{\rm a}
 =\left(\varepsilon^{-1}B_\varepsilon+\mathcal K_\varepsilon\right)
 U_\varepsilon^{\rm a}.
\]

由 \(P^2=P\) 得到 \([P,\mathcal K]=-P'\)，从而

\[
 P(d)U^{\rm a}(d,s)=U^{\rm a}(d,s)P(s),
 \qquad
 Q(d)U^{\rm a}(d,s)=U^{\rm a}(d,s)Q(s).
\]

这是后续能逐块串联移动补空间的精确代数事实；独立解析审计逐行核对了
commutator 符号，对抗审计则从反例结构检验这一机制的边界。

### 3.2 固定快时间块上的相对收缩

取固定 \(T\)，使

\[
 C_Ke^{-(0.16-0.12)T}\le\frac14.
\]

在一个块 \(d=s+\varepsilon\tau\)、\(0\le\tau\le T\) 内，

\[
 B_\varepsilon(s+\varepsilon\tau)-B_\varepsilon(s)
 +\varepsilon\mathcal K_\varepsilon(s+\varepsilon\tau)
 =O(\varepsilon)
\]

是 \(H\to H\) 的有界扰动。Duhamel 估计给出一个块上的误差
\(\delta_T(\varepsilon)\to0\)。选小 \(\varepsilon\) 后，每个完整块都有

\[
 \|U^{\rm a}(s+\varepsilon T,s)Q(s)\|
 \le\frac12 e^{\Phi_\varepsilon(s+\varepsilon T,s)}.
\]

精确 intertwining 让这些估计沿真正的移动 \(Q\)-纤维串联，得到

\[
 \|U_Q^{\rm a}(d,s)\|
 \le M_Qe^{\Phi_\varepsilon(d,s)}
 e^{-\gamma_Q(d-s)/\varepsilon}.
 \tag{R0.73L-5}
\]

这个环节只用统一 \(H\)-范数常数；没有调用一致图范数、
\(P_\varepsilon''\) 或全局 \(W^{-1}BW\) 共轭。

### 3.3 前向 Volterra 吸收

把精确解分成 \(p=P(d)u(d)\) 和 \(q=Q(d)u(d)\)。精确演化相对 Kato
演化的 Duhamel 公式分裂为两个 off-diagonal Volterra 方程。由
式 \((\mathrm{R0.73L\text{-}5})\) 的相对衰减核积分长度是 \(O(\varepsilon)\)，所以

\[
 \sup_{d\le D}e^{-\Phi_\varepsilon(d,0)}\|q(d)\|
 \le C\varepsilon
 \sup_{d\le D}e^{-\Phi_\varepsilon(d,0)}\|p(d)\|.
\]

再把它反馈到 rank-one selected coordinate，先得到统一上界，再通过
reverse triangle inequality 得到 selected component 的正下界。

### 3.4 非正交下界与作用量转移

证明没有把 \(p,q\) 当作正交分解。真实下界来自

\[
 \|p(d)\|=\|P(d)u(d)\|\le\|P(d)\|\,\|u(d)\|,
\]

配合 \(\|P(d)\|<9/5\)。随后利用
\(|\lambda_\varepsilon-\lambda_0|\le C_\lambda\varepsilon\)，整个慢区间
上的作用量差最多是 \(C_\lambda D_*\)，可以吸收到固定常数中。

## 4. Deep Research：已有定理与本节边界

文献检索以原始论文为准，并逐条核对假设。

- [Schmid 的共同定义域绝热定理](https://arxiv.org/html/1804.11213)在
  Kato stability、统一谱隙以及 \(P\in W_*^{2,1}\) 等条件下，给出精确演化与加入
  \([P',P]\) 的绝热演化相差 \(O(\varepsilon)\)。它是最接近的现成框架，
  但不能直接提供本节奇异双参数族所需的统一常数。
- [Abou Salem--Fröhlich 的非正规共同定义域结果](https://arxiv.org/html/math-ph/0607054)
  要求原演化一致有界；若只有 \(Me^{\gamma t}\) 的 quasi-bound，其误差会携带不适用于此处
  长时间尺度的指数因子。
- [Joye 的解析非自伴理论](https://arxiv.org/html/math-ph/0608059)说明，非平凡 nilpotent block 可产生次指数
  prefactor；rank-one 半单 selected block 正好避开这一障碍。

所以 R0.73L 没有把上述定理当黑箱。直接固定块证明只依赖 R0.73K 已封存
的统一 \(H\)-范数常数，也不要求尚未证明的一致 \(P''\) 或图范数。

## 5. 独立解析审计

独立解析审计与对抗审计均为 PASS。

第一份逐行检查：共同定义域演化、Kato 符号、一个块的 Duhamel 常数、
移动纤维串联、Volterra 吸收、非正交投影下界，以及
\(\lambda_\varepsilon\to\lambda_0\) 的作用量转移。它发现并修复了两个
会影响常数正确性的细节：一个块估计必须保留
\(\|Q\|\le1+\|P\|\)，下界吸收条件必须保留正确的 \(M_W\) 次数。

第二份以反例为目标，尝试引入 Jordan 块、竞争谱支、nonnormal
switching、投影退化、非法 backward evolution、图范数爆炸与
非正交抵消。没有一个反例能够同时保留全部封存假设和修正后的块估计。

## 6. 有限诊断与独立重算

有限 Fourier 诊断使用 \(N=32,48,64\) 三个截断、五个
\(\varepsilon\) 水平和完整慢区间 \([0,1/450]\)，共 15 条主轨迹。主求解器
为 DOP853；独立重算使用 midpoint matrix-exponential products，不调用
主求解器。

在 \(N=64\) 上：

| \(\varepsilon\) | terminal action | \(G_Ne^{-\Phi_N}\) | \(\|Q_Nu\|/\|P_Nu\|\) |
|---:|---:|---:|---:|
| \(1.0\times10^{-3}\) | 0.374611 | 0.99982849 | 0.00223605 |
| \(5.0\times10^{-4}\) | 0.752465 | 0.99970105 | 0.00184208 |
| \(2.5\times10^{-4}\) | 1.508182 | 0.99952276 | 0.00130284 |
| \(1.25\times10^{-4}\) | 3.019622 | 0.99937793 | 0.000683043 |
| \(6.25\times10^{-5}\) | 6.042504 | 0.99932905 | 0.000313255 |

关键审计量为：

- terminal action-normalized gain 范围：
  \([0.99932905,0.99982849]\)；
- forward-orbit backward-action residual 最大绝对值：
  \(6.712\times10^{-4}\)；
- 三个最小 \(\varepsilon\) 的 terminal leakage log--log slope：
  \(1.02813\)；
- \(N=48\) 与 \(N=64\) 的 terminal normalized-gain 最大差：
  \(6.995\times10^{-15}\)；
- 独立重算相对主结果的最大差：gain 为
  \(1.852\times10^{-9}\)，leakage 为 \(1.706\times10^{-9}\)。

所有冻结容差均通过。有限计算只用于复现定理预测、暴露实现错误和记录
前渐近行为；它不证明连续算子定理。

## 7. 正式图件与可复现包

正式四联图以 178 mm × 128 mm、600 dpi PNG、单页 vector PDF 和
vector SVG 保存。彩色、灰度和独立 PDF 栅格化表面均已检查；原始图数据、
输入哈希、环境、进度/资源日志、验证报告、manifest 与 SHA-256 清单均在
图件包中。

图 (a) 显示完整慢窗上的 action-normalized gain；图 (b) 显示 terminal
leakage 与锚定的 \(O(\varepsilon)\) 参考线；图 (c) 只用同一前向轨道构造
localization residual；图 (d) 显示六个数值 discrepancy-to-tolerance
比值。所有面板均明确标为 finite Fourier evidence。

## 8. 这一结果的研究价值

本节的直接价值是把“冻结谱支存在”升级为“真实长时间非自治轨道确实
取得匹配作用量增长”。这排除了路线中一个重要但常被略过的逻辑缺口：
瞬时不稳定不等于可实现的动态增长。

它仍然只是一座中间桥梁。距离更高层结论至少还有三道不同性质的门：

1. 把线性 selected-orbit 增长转成二维非线性离轨，需要精确控制
   Duhamel remainder 和可选初始振幅；
2. 把二维机制嵌入三维，需要横向频率与涡量拉伸的统一控制；
3. 即使证明三维不稳定，也与有限时间奇性和全局正则性二择一之间仍有
   本质距离。

因此它具备进一步整理为“谱动力学/绝热演化中间定理”稿件的潜力，但目前没有接近
Clay 问题闭合的百分比可诚实给出。

## 9. 精确开放边界

```text
commonDomainEvolution=CLOSED
katoIntertwining=CLOSED
movingComplementRelativeStability=CLOSED
nonselfadjointAdiabaticTracking=CLOSED
matchingSelectedGainAction=CLOSED
actionResolvedBackwardLocalization=CLOSED
finiteDiagnosticAndIndependentRecomputation=PASS
formalFigurePackage=PASS
explicitAdiabaticThreshold=OPEN
prefactorLimit=OPEN
twoTermWKB=OPEN
nonlinearNavierStokes=OPEN
threeDimensionalClosure=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
```

## 10. 下一阶段

R0.73M 应只做一件事：建立二维非线性离轨的可关闭 bootstrap。先冻结
扰动方程、线性 seed 的幅度尺度、退出时间和非线性余项范数；再证明在
selected gain 达到预定阈值之前，二次 Duhamel 项严格小于线性主项。
若这一门无法以显式不等式闭合，就停止在“线性增长定理”，不能以数值
离轨代替非线性证明。

## 11. 证据索引

- `r073l_problem_freeze.md`：冻结问题、允许机制与禁止捷径；
- `r073l_gap_matrix.md`：claim--evidence 逐项状态；
- `r073l_literature_audit.md`：一手文献和原创性边界；
- `r073l_adiabatic_tracking_proof.md`：连续算子证明；
- `r073l_independent_analytic_audit.md`：独立逐行解析审计；
- `r073l_adversarial_audit.md`：反例导向审计；
- `r073l_finite_diagnostic_audit.md`：有限计算与独立重算；
- `experiments/r073l/`：主/独立脚本、数据、日志和密封清单；
- `figures/r073l/fig-r073l-adiabatic-tracking/`：正式图、源数据与 QA。
