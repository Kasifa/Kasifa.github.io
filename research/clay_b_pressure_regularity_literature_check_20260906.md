# 无散压力增益：本轮定向文献核查

2026-09-06。**LITERATURE / INTERNAL / OPEN / NOT CLAY。**

本轮的任务是核对 AR--AS 中的空间压力增益是否已经有直接先例，
以及这些结果是否真的提供坏时间工作所需的时间预算。
我没有把检索结果当成完整新颖性审查，也没有重新审完所列论文。

## 实际读取的原始来源

1. Colombo--De Rosa--Forcella，
   [Regularity results for rough solutions of the incompressible Euler equations via interpolation methods](https://arxiv.org/pdf/1910.00902)。
   实际读取 Theorem 1.1、Proposition 4.1 的式 (4.3) 及其双线性证明部分，
   即作者稿第 1、8 页的相关内容。
   该空间命题就在周期域上：对两个无散输入，压力的 Besov 正则阶数
   可为两输入阶数之和；积分指数与求和指数同时改变。
   其条件是正的输入正则性，而不是仅有一个有限总能量常数。
   本轮不移植该文 Euler 时间正则性结论到黏性 NS。

2. Li--Zhang，
   [A regularity upgrade of pressure，作者稿](https://arxiv.org/pdf/2106.11852)。
   实际读取引言中的空间范围说明、Theorem 1.1、Theorem 1.2 及端点
   结论 Theorem 1.4--1.5 的陈述。原文在全空间研究给定无散速度的
   压力 Sobolev、Besov 与 Hardy 正则性，明确不研究 Cauchy 问题。
   因而不能把空间双倍正则性解释为未知范数的时间可积性。
   本轮没有重审其端点反例的全篇构造，也不将全空间命题直接当成
   当前周期域的局部正则性定理。

3. De Rosa--Latocca--Stefani，
   [On Double Hölder Regularity of the Hydrodynamic Pressure in Bounded Domains](https://arxiv.org/pdf/2205.00929)。
   实际读取 Theorem 1.4 的周期域陈述及其前后的适用说明。
   此处即使放宽无散要求，也仍需速度的正 Hölder 正则性及额外散度控制。
   我只核对这一输入边界，不调用其边界域主定理或将其作为能量类结论。

## 与本轮推导的关系

分离频带压力中，把一个导数放到较低输入上，并从输出逆 Laplacian
获得逆频率，是已知无散双线性增益的一部分。AS 在固定周期乘子下
写出所需的求和和完整局部测试，只为检查它是否支付当前缺口；
没有将这一空间增益本身命名为新机制或新正则准则。

AR.15 的精确静态双模说明：若两高输入产生低输出，不能在压力振幅上
额外保留一个普适正幂的输出/输入比。双散度源的增益会被低频逆
Laplacian 抵消。这与上述双倍正则性不矛盾：文献估计的右侧含有
速度正则性范数，它们可随输入频率增长。

AR.17--AR.19 的补充预算更直接：零均值 h 的 Sobolev 与零阶压力梯度
算子给逐时 L3/2 压力梯度，再用低输出 Bernstein。
不需要把上述任何文献中的额外速度范数当作已知。
它保留真实的 A_J，但在扩散频率处仍留下 A_J*Lambda_A，见 AR.21。

因此本轮没有从这些文献中取得尚未证明的坏时间净工作上界。
下一步若继续，必须处理时间演化、带符号配对或真正的新结构，
不能再次把一个空间条件准则重命名为总能量结论。

本记录属于内部方法筛查，不构成新的研究 release、累计 recap 或
完整发表价值判断。无仿真、科学图、读者 PDF 或发布动作。
