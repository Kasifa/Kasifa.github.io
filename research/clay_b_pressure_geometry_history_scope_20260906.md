# 本次 Fourier 压力检查与旧结果的边界

2026-09-06。**INTERNAL SCOPE RECORD / NO NOVELTY CLAIM / G OPEN。**

## 实际重读的历史来源

本轮完整重读 AB、AM、AO、AQ、AR、AS、AV 的当前源文件，作为本次
原压力配对的依赖。另完整重读以下历史来源，以免把已有改写重复列为
新进展：

- AC：`research/clay_b_pressure_geometry_20260906.md`，SHA256
  `a608bdf61adcdf3b080e8be3efed495dd2d1b5c289551a7774bfaf5ea3732db5`。
  这里处理物理空间速度方向及加权流线变化，不是 Fourier 模态夹角。
  它的临界可积性接口仍有附加条件。本轮重读不等于重审其所引论文。
- AD：`research/clay_b_pressure_sign_20260906.md`，SHA256
  `c02090cf86979b1b8a6edb9fc6380d4bc254ee81d3e7bc688876442b80d5655f`。
  已有全域压力功双符号构造和大幅值初值的短时增长。不能把本轮
  压力 Fourier 绝对和的例子再次写成首次发现压力功无固定符号。
- R0.75F：`research/r075f_modal_phase_integration_identity.md`，SHA256
  `f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440`。
  该文的相位积分针对已指定的被动剪切模态方程及局部能量配对。
  它不是当前完整非线性压力工作所有时间估计的不可能性定理。

还完整读回压力投影小节的报告与后续计划，而**没有**把这个动作记成
对 AF–AH 全部原始证明的重新独立审稿：

- `research/clay_b_pressure_quotient_report-source_20260906.md`，SHA256
  `747ab9941833a8c6974017b7e9a408873959873add49092fa260b43c1c9021da`；
- `research/clay_b_pressure_quotient_work_plan_20260906.md`，SHA256
  `9bbd3fb4a0d8f3923b05c144d1c73bf87d85e28c81eec69159d1296fecff5400`。

这两份记录已经明确覆盖 speed-only moderator、条件期望式压力投影、
局部截止成本及一个特定瞬时残差估计的失效。本轮不再重做这些操作。

## 本轮有限文献读取

检索方向是原压力的 Fourier 角度结构及几何正则性条件。搜索结果本身
不作数学依据，也不据没有找到同题论文宣称新颖性。

实际打开 C. V. Tran 与 X. Yu 的
[A geometrical regularity criterion in terms of velocity profiles for the 3D Navier–Stokes equations](https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/20720/qjmam_20190430_R1_20190813.pdf?isAllowed=y&sequence=1)，
作者稿 2019，18 页。定向读取作者页 3 的 Lemma 2.1 完整陈述及证明、
页 4 的 moderator 定义、页 5–6 的相关能量展开；也看到了 Theorem 3.5
陈述，但没有核查其全部前提推导与证明，因此不调用该定理。

Lemma 2.1 concerns a whole-space divergence-free velocity, a bounded
speed-dependent factor, and a W1,infinity spatial factor constant along
streamlines, with stated velocity integrability assumptions. Its integral
cancellation is proved by a scalar primitive and integration by parts.
This is pressure moderation, not a theorem that actual Fourier phases
or the AQ bad-time pressure work are automatically small.

本轮读取与既存
`research/clay_b_pressure_work_literature-boundary_20260906.md`
（SHA256 `833b109c22957466fd77383a24d73df6e08e2c6d142a18c0c50eb39516a00b50`）
一致：不能把 moderator 作为新机制。当前 Fourier 推导不依赖这篇
论文的正则性定理，全部恒等式与反检查另给本地证明。

## 半阶嵌入的标准工具与周期适配

AW.40 的半阶嵌入使用标准 Sobolev/HLS 工具，不是新正则性定理。
本轮实际读取 Tao 的
[245C Notes 1: Interpolation of Lp spaces](https://terrytao.wordpress.com/2009/03/30/245c-notes-1-interpolation-of-lp-spaces/)
当前编号 Corollary 46 的完整 HLS 陈述。该页把核写成
\(|x-y|^{-\alpha}\)；三维取核指数 \(\alpha=5/2\)、输入指数
\(3/2\)、输出指数 \(2\)。这对应阶数为 \(1/2\) 的势算子，
不是把核指数误作势阶数，也不涉及失效的 L1 或 L infinity 端点。
相关旧文章的 Corollary 7 链接编号已经过时，本记录不用该编号。

该网页直接陈述全空间版本；AW 使用的周期版本另需说明。对零均值
周期函数，\(I_{1/2}=(-\Delta)^{-1/4}\) 的核可由热核积分表示：
\(\Gamma(1/4)^{-1}\int_0^\infty
s^{-3/4}(H_s-V_{\mathbb T}^{-1})\,ds\)。大时间部分光滑有界；
小时间周期热核展开给出的奇性至多为周期距离的 \(-5/2\) 次方。
在基本立方体及有限相邻副本上应用上述全空间 HLS，再加上有界余项，
得到周期 \(I_{1/2}:L^{3/2}\to L^2\)。周期 Riesz 变换在
\(L^{3/2}\) 有界，并且非零模上
\(D^{1/2}f=-\sum_jR_j I_{1/2}\partial_jf\)。平均值单独由
\(\|f\|_{3/2}\) 控制，即得 AW.40。这里记录标准工具的具体适配，
不声称网页本身证明了本项目的周期压力配对或 NS 时间预算。

## 本次究竟检查什么

本次区分三个对象：精确带相位的原压力工作；保留速度极化但先对输入
取绝对值的压力成本；只保留频率夹角的更粗成本。后两者的静态失控
不能直接传递给第一个对象。

尤其，静态例中的固定 K、固定能量、统一 H1 不是 AQ 的同一解大范数
终端序列。它没有产生该序列，不能否定保留原测试、负耗散和真实时间
演化的估计。只有实际支付了这样的动态成本，才可能接回未完成的 G。
本记录不作外部同行评审、完整新颖性审查或任何 Clay 结论。
