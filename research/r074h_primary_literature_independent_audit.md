# R0.74H — 主文献边界独立审计

## 结论与绑定

**FINAL PASS.**

我在 2026-09-02 独立复核了下列两个固定对象：

- canonical report-source：`research/r074h_report-source.md`，SHA256
  `d72917b04e067113f419f89bc009861f264d859e80cb22dce1276c6dbfbc2c47`；
- public boundary：`research/r074h_primary_literature_boundary.md`，SHA256
  `722e338f4cdd729f3a8756b886c920f17d08e08592bbce6ed9561179d6afbadf`。

这两个哈希均在审计开始时重新计算并匹配。PASS 的含义仅是：在本次限定的四篇原始 arXiv 记录与正文内，题名、作者、研究范围和 R0.74H 比较边界表述准确；目标文本也没有把有限检索中的未命中写成新颖性或优先权结论。PASS 不表示完成了穷尽文献检索，也不证明 R0.74H 新颖。

## 本次允许使用的文献

本次外部证据只取自以下四个原始论文记录及其 arXiv 正文。未使用综述、搜索结果摘要、引文数据库或二手解读作为证据。

| arXiv | 题名与作者核对 | 正文直接支持的研究范围 | 对 R0.74H 边界的核对 | 结果 |
|---|---|---|---|---|
| [1906.11038 记录](https://arxiv.org/abs/1906.11038)；[正文](https://arxiv.org/html/1906.11038v1) | *Weak solutions for Navier--Stokes equations with initial data in weighted \(L^2\) spaces*；Pedro Gabriel Fernández-Dalgo、Pierre Gilles Lemarié-Rieusset | 三维 Navier--Stokes 方程在 \(w_\gamma(x)=(1+|x|)^{-\gamma}\)、\(0<\gamma\leq2\) 的加权 \(L^2\) 数据上存在全局弱解。正文的加权能量控制明确出现由 \(\nabla w_\gamma\) 产生的输运项和压力项，并给出 suitable weak solution 结构。 | 它直接支持“空间权重的导数承载输运与压力功”这一方法先例。它没有给出 R0.74H 的终端锚定轨迹、双局部框架、周期 dyadic collar 或双包诊断的精确组合。论文中的常规 Leray 型正则化/卷积构造不能等同于“终端锚定的 mollified trajectory”。 | PASS |
| [1907.00256 记录](https://arxiv.org/abs/1907.00256)；[正文](https://arxiv.org/html/1907.00256v1) | *Global existence, regularity, and uniqueness of infinite energy solutions to the Navier-Stokes equations*；Zachary Bradshaw、Tai-Peng Tsai | 研究 Lemarié-Rieusset 意义下的 local energy solutions；以小尺度或大尺度的 truncated Morrey-type 量为条件，处理全局存在、初始/最终正则性及临界 \(L^2\)-Morrey 类中的唯一性问题。 | 它支持“尺度相关的局部能量控制”先例。其可观测量、压力展开、几何和定理目标均不同于 R0.74H；DSS/尺度结构也不等于周期 dyadic collar 恒等式。 | PASS |
| [2008.09204 记录](https://arxiv.org/abs/2008.09204)；[正文](https://arxiv.org/html/2008.09204v1) | *Local energy solutions to the Navier-Stokes equations in Wiener amalgam spaces*；Zachary Bradshaw、Tai-Peng Tsai | 在 \(L^2\)-based Wiener amalgam 空间 \(E_q^2\) 和相应 \(\mathbf{LE}_q\) 类中建立局部能量先验界、局部构造、time-global local energy solution，以及最终正则性和局部能量长期增长估计。 | 它支持“分布在空间格点/区域上的局部能量聚合”先例。正文的固定测试函数局部能量不等式含有 cutoff 导数上的速度—压力输运项，但不是 R0.74H 的移动终端框架、周期壳层 payment 或精确正累积 collar-flux repair。 | PASS |
| [2010.00868 记录](https://arxiv.org/abs/2010.00868)；[正文](https://arxiv.org/html/2010.00868v2) | *Weighted energy estimates for the incompressible Navier-Stokes equations and applications to axisymmetric solutions without swirl*；Pedro Gabriel Fernández-Dalgo、Pierre Gilles Lemarié-Rieusset | 以满足导数、Muckenhoupt 和缩放条件的适配权重推广 Leray 程序；在三维情形得到满足局部能量不等式的全局加权弱解，并给出轴对称无旋流数据的正则全局解应用。 | 它支持更一般的加权能量与 suitable-solution 方法先例。其慢衰减适配权重、固定欧氏坐标和轴对称应用不提供 R0.74H 的双框架加速度账本、周期 super-Gaussian collar 或显式双包通量下界。 | PASS |

四篇文献的题名和作者与两个目标文件一致。目标文件对研究范围的压缩也与正文相符：1906.11038 和 2010.00868 是加权能量路线；1907.00256 是 truncated Morrey-type/local-energy 路线；2008.09204 是 Wiener-amalgam/local-energy 路线。目标文件没有把这些论文误写成 R0.74H 精确定理的来源。

## R0.74H 比较边界

我把文献所支持的内容与有限检索中的未命中分开处理：

| 比较项 | 四篇正文中的结论 | 可允许的声明强度 |
|---|---|---|
| 空间权重导数上的速度输运与压力项 | 已找到明确恒等式/不等式先例，尤其见 1906.11038 的加权能量控制和 2008.09204 的局部能量不等式 | “methodological precedent found” |
| Morrey、uniformly local、Wiener-amalgam 或慢衰减加权框架中的空间分布能量控制 | 已找到相邻方法与定理 | “close local/weighted-energy precedent” |
| 普通 mollification 或正则化构造 | 文献中存在相邻构造，但它不包含 R0.74H 的终端条件与轨迹定义 | 不得据此声称 moving-frame construction 已有，也不得把普通 mollification 当成精确碰撞 |
| 平滑周期 super-Gaussian dyadic collar、终端锚定 mollified trajectory、保留速度与减速度双框架、独立 acceleration moment、正累积 collar-flux repair、R0.74G 双包下诊断的同时组合 | 在这四篇正文的定理、主要恒等式及有界全文概念筛查中未定位到 | 只能写“not located in this four-paper bounded screen” |
| \(P^{2/3}+P\) 的 R0.74H 两区间形式或显式正 collar-flux 下界 | 未定位到与 R0.74H 同一可观测量和几何的结论 | 不能写成文献定理，也不能从未命中推出原创性 |

canonical report-source 使用了 “bounded boundary check”、`not an exhaustive novelty or priority search` 和 `not evidence of novelty`。public boundary 使用了 `BOUNDED SCREEN`、`NOVELTY NOT CLAIMED`，并明确说明 negative search observation 不是 novelty 或 priority 的证明。这些限定语覆盖了所有 non-hit 结论；文本中没有从有限语料未命中跳到“首次”“新颖”“无先例”或优先权声明。

因此，两个目标文件的逻辑层级是正确的：

1. 四篇文献证明的是相邻方法先例；
2. 精确 R0.74H 组合只是在该四篇语料中未定位到；
3. R0.74H 的公式正确性、显式通量下界及其数学后果仍须由本项目自己的证明和独立审计承担；
4. bounded non-hit 没有被写成 novelty。

## 未检索范围

以下范围不在本次 PASS 内：

- 除 arXiv:1906.11038、1907.00256、2008.09204、2010.00868 以外的任何论文、预印本、专著、学位论文或会议材料；
- 四篇论文的参考文献、引用它们的后续论文、作者其他论文及相关文献的 citation graph；
- 期刊排版版本与 arXiv 版本的逐行差异，以及 DOI 落地页的独立元数据复核；
- 其他语言、其他术语、未公开手稿，以及对所有同义表达和所有公式变体的穷尽检索；
- novelty、priority、freedom-to-operate 或投稿查重结论；
- R0.74H 推导本身的符号、常数、壳层极限、压力拆分、加速度幂次、弱解稳定性和显式双包通量下界；
- epsilon-regularity、延拓、奇点排除、三维全局正则性或 Clay 千禧年问题结论。

本次审计的停止条件就是完成用户指定的四篇原始记录/正文核对。若要作新颖性或优先权判断，必须另行扩大语料和检索策略；本文件没有作该判断。

## 最终判定

**FINAL PASS — metadata correct; scopes correctly bounded; exact R0.74H non-hit remains explicitly finite; novelty not claimed.**
