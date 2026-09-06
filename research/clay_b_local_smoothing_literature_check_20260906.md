# 局部尾持留与已有局部平滑结果的边界

2026-09-06。**LITERATURE / INTERNAL / NOT A NOVELTY AUDIT / NOT CLAY。**

本轮只核对局部短时持留的先例和可调用范围，不声称审完以下论文的证明。

## 实际读取

- Jia--Šverák，
  [Local-in-space estimates near initial time for weak solutions of the Navier-Stokes equations and forward self-similar solutions](https://arxiv.org/pdf/1204.0529)。
  实际读取作者稿第 15--16 页 Theorem 3.1 的完整陈述与其分解脚注。
  它在全空间的均匀局部能量框架下，还要求局部初值属于 m>3 的 Lm；
  从无散局部扩展构造 mild 解后，结论控制二者之差的局部 Hölder 正则性。
  本轮不重审其余证明，也不调用自相似解主定理。
- Barker--Prange，
  [Localized smoothing for the Navier-Stokes equations and concentration of critical norms near singularities](https://arxiv.org/pdf/1812.09115)。
  实际读取作者稿第 2 页 Theorem 1、第 5--6 页 Type I 假设 (14)、
  Theorem 2 与 §1.5 的固定球讨论。Theorem 1 需要局部 L3 初值小，
  并保留其全空间局部能量解与远处衰减条件。Theorem 2 的缩球集中结论
  另有 Type I 控制，不是只从有限总能量得到。未重审其完整证明或附录。

## 本轮不作的移植

AT 的 h 是平滑高通后的真实强迫场；theta*h 又一般不无散。
因此不能将它们直接代入上述无外力初值定理。
从全空间到周期域、从原速度到受迫高频尾的任何转换都须另证。
AU 的用途是直接核对当前周期方程和固定截止下的全部成本，
而不是将局部平滑重新命名为新机制。

即使在候选大范数窗口排除了局部小尾时刻，这仍是必要条件。
它既不产生缺失的小尾时刻，也不把 AQ 的带符号压力净工作变成小量。
上述文献不在本轮被当成未知时间预算、Type I 先验界、首次奇点排除
或移动缩球合同 G 的证明。

本记录仅作方法筛查；无发布、仿真、科学图或新读者 PDF。
