# R0.71F 一手文献审计：skewed cylinders、caloric trace 与无权求和边界

日期：2026-08-25

状态：bounded primary-source audit

## 直接结论

我围绕 R0.71F 的准确缺口核对了四组一手来源：Yang 的流适应极大
算子、Vasseur--Yang 的局部涡量方法、Chen--Liang--Tsai 的 caloric
trace theorem，以及 Yu 的 filtered-vortex-stretching closure。

这些来源给出的工具可以清楚分成三层。

1. skewed-cylinder 理论提供轨道、admissibility、覆盖、极大估计和几乎
   处处微分；
2. 逆热迹定理以内部法向高阶导数控制边界
   Besov/Triebel--Lizorkin 正则，而不是从零阶 bulk mass 出发；
3. filtered-vortex-stretching 的无权闭合需要远场、commutator 和其余
   shell budgets 的额外可和性。

指定主源中没有一条定理给出

\[
 \text{standard Leray--Hopf budgets + skewed geometry}
 \Longrightarrow
 \text{projected-Lamb bottom-trace summability}.
 \tag{1.1}
\]

这是四组主源内的限定范围结论，不是全局文献不存在证明，也不是新颖性
或优先权结论。

## Claim-to-source ledger

| 一手来源与条目 | 定理的单向逻辑 | R0.71F 可以使用的部分 | 不能推出的部分 |
|---|---|---|---|
| [Yang, arXiv:2008.05588v2](https://arxiv.org/abs/2008.05588v2), Def. 1 | 以 \(u_\varepsilon=u*\varphi_\varepsilon\) 的轨道生成时间尺度 \(\varepsilon^2\)、空间尺度 \(\varepsilon\) 的 skewed cylinders。 | 流适应柱的定义与尺度。 | 没有 NSE 底迹、耗散或跨尺度可和性。 |
| 同文 Def. 2, Assumption 13, Prop. 14 | admissibility 要求 \(\varepsilon^2\fint_{Q_\varepsilon}\mathcal M(|\nabla u|)<\eta\)；若 \(\operatorname{div}u=0\) 且 \(\mathcal M(\nabla u)\in L^p((S,T)\times\mathbb R^d)\)，\(1\le p\le\infty\)，则对任意 \(\eta>0\)，几乎处处最终存在充分小的 admissible 半径。 | 检查哪些柱可进入覆盖族。 | 不保证预定的完整 dyadic chain 逐层 admissible。 |
| 同文 Prop. 12, Thm. 3, Thm. 19 | 当固定 \(\eta<\eta_0\) 时，covering lemma 选出两两不交的子族并以其总体积控制原柱族并集的测度；流适应极大算子为 weak \((1,1)\) 和 strong \((q,q)\), \(q>1\)，并给出微分定理。 | Vitali 型选择、local-to-global 与几乎处处恢复。 | 不提供 R0.71F 所用的逐点 bounded-overlap partition；weak \((1,1)\) 也不等于无权 \(\ell^1\) shell packing。 |
| [Vasseur--Yang, arXiv:2009.14291v1](https://arxiv.org/html/2009.14291v1), Thm. 2.1--2.2 | 在沿 \(u_\varepsilon\) 的后向 skewed cylinders 上引用上述极大估计与微分定理。 | 确认这一几何能用于严格 NSE 局部到整体论证。 | geometry 本身没有解析 trace gain。 |
| 同文 Thm. 1.3 | 在局部均值归零和混合范数小量条件下，推出更小柱内全部 \(\nabla^n\omega\) 的 \(L^\infty\) 控制。 | 一个真正的“局部小量 \(\Rightarrow\) 正则”模板。 | 所需小量不是标准 Leray--Hopf 预算的自动结论。 |
| 同文 Lem. 3.1, Cor. 3.2, Thm. 1.1 | 次二次 \(\nabla u\) 枢轴加小 \(L^2\) 项，经过 skewed maximal function 得到 Lorentz 导数估计。 | 说明怎样把局部估计全局化。 | 纯能量级 \(L^1\) 枢轴通常只进入 weak \(L^1\)，不能据此宣称目标无权求和。 |
| [Chen--Liang--Tsai, arXiv:2606.16438v1](https://arxiv.org/html/2606.16438v1), Thm. 1.2 | 对公式 (1.3) 定义的半空间抛物 Poisson 延拓，边界的时间 Triebel--Lizorkin 与切向 Besov 范数控制内部导数的混合范数。 | 提供“有边界正则 \(\Rightarrow\) bulk derivatives”的精确定理。 | 不是零阶 bulk mass 恢复底迹。 |
| 同文 Thm. 1.3 | 当整数 \(n>1/q\) 时，内部法向高阶导数反向控制上述边界正则范数。 | 在该半空间 Poisson 延拓框架内，严格说明已证明的逆向估计使用法向导数输入。 | 边界正则范数是被控制的结论；其高度变量是物理半空间法向，延拓也不是 R0.71F 的 \(e^{s\Delta_x}\)，不能直接搬成 signed Lamb heat trace。 |
| [Yu, arXiv:2606.27560v1](https://arxiv.org/html/2606.27560v1), Thm. 8.2 | 对 \(\mathbb R^3\) 上的 Leray--Hopf 解，Leray energy 对 far-field 只给带 \(2^{3k/2}\) 损失的估计，因此只能对相应权类求和。 | 提供该全空间设定下标准能量预算能做到的基线。 | 不能自动去权，也不能不经论证直接移植为周期域定理。 |
| 同文 Def. 8.5, Prop. 8.6, Thm. 8.7, Cor. 8.8 | 若 reassigned annular reservoirs \(\mathfrak A\in\ell^p\)、profiles \(\mathcal Q\in\ell^q\)，\(1/p+1/q=1\)，则 annular far field 无权可和。 | 条件性离散 Carleson 闭合的精确形式。 | 序列可和性是额外假设；exterior tail 仍需另行控制。 |
| 同文 Thm. 9.3, Cor. 10.2, Thm. 10.3 | 在 exact whole-space setting 中，若 principal cutoff residual 被 adjoint cutoff 消除或纳入可和的非负 shell budget，full far field（含另行控制的 exterior tail）、commutator increment defects 及其余 localization/shell budgets 均可和，则 positive surplus 可和并趋零。 | 与目标最近的已写明 closure ledger。 | 结论依赖的正是 R0.71F 不能偷设的可和性。 |

## 对 skewed-cylinder 几何的准确使用

Yang 的 admissibility 是一个积分小量条件：

\[
 \varepsilon^2\fint_{Q_\varepsilon(t,x)}
 \mathcal M(|\nabla u|)<\eta.
 \tag{3.1}
\]

Assumption 13 要求 \(\operatorname{div}u=0\) 且
\(\mathcal M(\nabla u)\in L^p((S,T)\times\mathbb R^d)\)，
\(1\le p\le\infty\)。Proposition 14 对任意 \(\eta>0\) 给出几乎处处的
最终小尺度 admissibility；Proposition 12 和 Theorem 3 另要求固定
\(\eta<\eta_0\)。Proposition 12 选出两两不交的子族，并用其总体积控制
原柱族并集的测度；它不提供逐点 bounded-overlap partition。

该理论不控制 R0.71F 的独立 heat-height 变量 \(s\)，也不把 \(s>0\) 的
面积积分变成 \(s=0\) 的边界值。因此我只把它用于下列两点：

1. 给移动空间--时间截断一个合法几何来源；
2. 使用 admissible covering/maximal machinery 做 local-to-global。

R0.71F 在每个固定 \((t,s,j)\) 上使用的 bounded-overlap partition 是本报告
另行假定或构造的几何输入，不是 Yang 定理的结论。

任何额外的底迹增益必须来自新的解析估计，而不能记在 covering lemma
名下。

## 对 caloric trace 的准确使用

Chen--Liang--Tsai 的 Theorem 1.3 确实是逆向 trace estimate，但对象是其
公式 (1.3) 定义的半空间抛物 Poisson 延拓；右侧是
\(\partial_{x_d}^n v\) 的内部混合范数，且 \(n>1/q\)。它控制的是边界
Besov/Triebel--Lizorkin 正则范数，后者是结论而不是另一个输入。该定理
只支持以下限定判断：在这套半空间 Poisson 延拓框架内，已证明的反向
估计使用法向高阶导数；它不证明所有逆迹都必须具有同类输入，也不从
有限的零阶 bulk mass 恢复边界迹。

它不能直接证明 R0.71F 的 no-go。R0.71F 的严格障碍来自六模态初值所
生成的真实全局光滑 2D3C NSE 解在初始迹上的精确局部公式；该文只用于
说明这项结论与成熟 trace 理论的结构一致。

## 对近期 filtered-vortex-stretching 预印本的边界

Yu 的 Theorem 10.3 不能被概括成“已经证明小尺度 defect 自动消失”。
在它的 exact whole-space setting 中，principal cutoff residual 还必须由
adjoint cutoff 消除，或纳入一个可和的非负 shell budget。其余逻辑是

\[
 \begin{gathered}
  \text{far field summable},\quad
  \sum_k\widetilde{\mathcal S}_k^{(p)}<\infty,\quad
  \sum_k(L_k+L_{k,\mathrm{inc}}^{\mathrm{com}})<\infty
  \\
  \Longrightarrow\quad
  \sum_k\mathfrak S_k<\infty,\qquad \mathfrak S_k\to0.
 \end{gathered}
 \tag{5.1}
\]

其中 full far field 包括必须另行控制的 exterior tail。这是有价值的条件性
结构，但三组可和性没有由标准能量预算推出。R0.71F 若重新假定同类
Carleson closure，只会移动缺口，不会闭合缺口。

## 文献门槛后的研究决定

文献审计允许 R0.71F 安全地做两件事：

1. 证明 bounded-overlap moving cutoffs 下的 projected-Lamb heat-area
   packing；
2. 检查局部底迹是否仍被精确高频族饱和。

它不允许把 skewed maximal theorem、caloric trace theorem 或条件性
filtered closure 表述成无条件 regularity input。任何新的条件性判据还
必须与 Serrin、Koch--Tataru、临界 Besov 和 dissipation-wavenumber
判据逐项比较，不能只因观测量不同就声称更弱。
