# 近期源筛查与单侧压力：本轮文献读取范围

2026-09-06。**LITERATURE SCOPE / BOUNDED PRIMARY CHECK / NOT NOVELTY REVIEW / NOT CLAY。**

## 热核背景

[Tao，Quantitative bounds for critically bounded solutions to the Navier-Stokes equations，arXiv:1908.04958v2](https://arxiv.org/pdf/1908.04958)。
本轮读其紧支撑乘子核论证及 (2.3)–(2.5)；此前完整读取的设置、
Theorem 1.2、Proposition 3.1 陈述与 (3.7)–(3.15) 范围仍以
`clay_b_lagged_pressure_literature_scope_20260906.md` 为准。
这些是全空间频率局部化工具；BD 的周期乘子一致性另作论证。
不能导入该文预先假定的统一临界范数控制，也不把基本热分解称为新方法。

## 一项单侧压力判据的准确入口

[Seregin、Šverák，MiS Preprint 92/2001](https://www.mis.mpg.de/de/publications/preprint-repository/article/2001/issue-92)，
[机构原始 PDF](https://files-www.mis.mpg.de/mpi-typo3/preprints/2001/preprint2001_92.pdf)。
期刊元数据为 ARMA 163 (2002), 65–86，DOI 10.1007/s002050200199；
本轮实际读取的是 2001 预印本，不声称两个版本逐字相同。

读取摘要、引言及 §2 的完整问题设置和主要陈述（纸面页 1–7）；
PDF 第 6–10 页另渲染检查，涵盖压力规范、Definition 2.1、
Theorem 2.2 和 §3 起始 suitable 定义。§3 后续、§4 和主定理证明
尚未完整读，不宣称全证明复核。

该定理针对全空间 \(H^1\) 无散初值的 Leray–Hopf 解，压力用
Newton 势规范化。存在非负控制函数 \(f\)，满足下述 (C)，且
\(|u|^2+2p\le f\) 或 \(p\ge-f\)，便得到正时光滑性。
此处改名 \(f\)，以免与当前稿件的梯度范数 \(g(t)\) 混淆。

条件 (C)：每个 \(t_0>0\) 存在 \(R_0>0\)，使
\[
 \sup_{x_0\in\mathbb R^3}\sup_{t_0-R_0^2\le t\le t_0}
 \int_{B(x_0,R_0)}\frac{f(x,t)}{|x-x_0|}\,dx<\infty;
\]
且每个固定 \(x_0\) 与 \(0<R\le R_0\) 的上述半径 \(R\) 势积分，
在 \(t_0\) 左连续。不能删去中心一致上确界或左连续性。
常数控制函数满足 (C)，只是一个充分特例。

这不是从当前周期能量推出的性质，亦未证明该全空间定理直接适用于
周期情形。单侧压力规范不能任意加时间函数。AG 的 Bernoulli
重写早已完成；此处只为下一轮定位原证明中的真正强制估计，而非
把已有恒等式重新计作成果。全文证明与周期余项是下一项未完成检查。

## 检索与获取证据

使用作者姓名、lower bounds on pressure、Bernoulli regularity 等
组合做有限检索；机构页、作者原文入口为主要来源。未以 ResearchGate
或二手摘要证明定理，未做穷尽新颖性检索，未调用 Deep Research。
机构 PDF 在网页读取工具中因 application/octet-stream 失败；
作者目录返回 502，作者 PDF 超时。随后从同一机构下载原文件成功。

原文件 341792 bytes、27 页，SHA256
`d5f253e96a6518cae26c7a98026977979c138403b76f5d707cc4382606b3091f`。
临时读取文件在 `/tmp/ns-pressure-primary.5uEzyi/ss-pressure-2001.pdf`；
不把第三方整篇 PDF 纳入发布资产。文本提取有旧字体编码噪声，
主要定理假设以渲染页面复核。没有修改、重导出或创作读者 PDF。
