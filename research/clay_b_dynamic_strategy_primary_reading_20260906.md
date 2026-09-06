# 动力学路线复查：原始来源和阅读范围

2026-09-06。**PRIMARY SOURCE RECORD / BOUNDED SCOPE / NOT CLAY。**

我核验以下两条候选路线。这里记录实际阅读，不把部分论文阅读称为
完整文献审计，也不声称完成新颖性检索或 Deep Research。

## 1. 古老解与峰值提取

Koch、Nadirashvili、Seregin、Šverák，*Liouville theorems for the
Navier–Stokes equations and applications*。
[作者原文 PDF](https://www-users.cse.umn.edu/~sverak/publications/liouville.pdf)，
[arXiv:0709.3599](https://arxiv.org/abs/0709.3599)。期刊信息为 Acta
Mathematica 203 (2009), 83–105；本次实际读取的是标注 2007-09-22
的 26 页作者预印本，不是期刊版 PDF。

- 实际临时文件：`/tmp/ns-strategy-primary.TEj0ZX/knss-2007.pdf`。
- 大小 231150 bytes；SHA-256
  `5d86444c4c34bcad3642b2087a69b98d265f6da0e366bd50621d4ce792abc9f2`。
- 主审完整读取第 3–6 节（PDF 页 6–24），另读引言；第 2 节没有
  完整重读，所引用外部局部正则性理论也未全部重新审计。
- PDF 页 18–20 已渲染并检查公式。关注 Lemma 6.1、Proposition
  6.1、端点归一化，以及 Proposition 后的常向量限制。

本次使用的范围是：mild 与一般有界弱解的区别、有限窗口紧性接口、
有对称／衰减条件的古老解结论，以及非零极限不自动产生矛盾。
“无环向速度”不译为“无旋”。峰值提取必须保留终点控制；仅有
爆破下界给出的时间长度，不能代替延伸区间内的统一速度界。
本文的全空间叙述不当作已经在本次完整证明了周期极限的所有接口。

## 2. 中间应变特征值

Evan Miller，*A regularity criterion for the Navier–Stokes equation
involving only the middle eigenvalue of the strain tensor*，
[arXiv:1710.05569](https://arxiv.org/abs/1710.05569)，本次为 v4
（2019-08-17）。期刊 DOI 为
[10.1007/s00205-019-01419-z](https://doi.org/10.1007/s00205-019-01419-z)。

- 实际临时文件：`/tmp/ns-strategy-primary.TEj0ZX/miller-strain-v4.pdf`。
- 36 页、377811 bytes；SHA-256
  `6762db9fe7b947b4902c6917b81d894faa2f0764f2049f6bd14f1be6acc65c4e`。
- 主审完整读 PDF 页 2–6、14–17、21–24。实际覆盖第 4 节所用
  enstrophy 恒等式论证及第 5 节 Lemma 5.1、Theorem 5.2 和
  Theorem 5.3 的证明。Proposition 4.8 只读开头，不记完整阅读。
- PDF 页 21–23 已渲染检查。未完整重读第 2–3 节、toy ODE
  部分或全部外部依赖。

本次只用来识别已知的条件正则性目标，以及应变代数界与真正动力学
控制之间的区别。原文使用全空间条件；不把中间特征值的全局积分
恒等式误作逐点涡量对齐。第 5 节临界端点结论不能扩写为所有后续
端点情形的完整分类。

## 3. 有限的时效核验

为避免用旧论文年代推断当前全部进展，另检查两条出版方来源。
这不是新增候选路线。

- Chae，2026 年 CMP 407, article 53，
  [出版方原文](https://link.springer.com/article/10.1007/s00220-026-05555-y)。
  已读摘要、第 1 节及返回的第 2 节开头至式 (2.17)，未读完整证明。
  文中研究带额外条件的定常全空间 Liouville 问题；它不能提供本次
  所需的一般三维有界古老 mild 解分类。
- Guo / O，Applied Mathematics Letters 160 (2025), 109354，
  [出版方条目](https://www.sciencedirect.com/science/article/abs/pii/S0893965924003744)，
  DOI 10.1016/j.aml.2024.109354。仅检索结果中的出版方摘要可读；
  直接打开失败。没有读取正文、验证证明或引入该文的 Besov 条件。

因此，本次可以说的是“所核验的来源没有支付当前一般性输入”，
而不是“穷尽文献后证明没人解决过相邻问题”。后续若采用任一新的
文献接口，应重新读其准确版本和证明。

两份 PDF 与渲染图只作本地阅读证据，不放进公开发布资产。
本记录不授权第三方论文再分发；原文链接、版本和哈希可随研究记录
保留。不产生新读者 PDF、图表或仿真。
