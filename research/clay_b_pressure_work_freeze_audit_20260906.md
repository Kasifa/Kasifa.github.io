# PressureWorkWindow：冻结前实际源核验

2026-09-06。**FINAL ACTUAL-SOURCE AUDIT / PASS / INTERNAL / NOT PEER REVIEW / NOT CLAY。**

本轮只核验 PressureWorkWindow 合并研究包的最终数学源和研究报告，
不执行提交、发布、网页制作或线上检查。独立实际文件核验由
`r076l_figure_audit` 完成。

## 1. 绑定的最终文件

根任务确认下列三份文件已经停止修改后，本轮完整读取实际文件，并在读取前后
重复计算 SHA-256；两次结果一致：

| 文件 | SHA-256 |
|---|---|
| `research/clay_b_compact_pressure_work_preflight_20260906.md` | `0fc2b08c38b9e9dc0ace462c8be39df1c40338ffb4daf5967e2d9eedeb39a588` |
| `research/clay_b_short_time_pressure_work_preflight_20260906.md` | `a8061f7c4fbc8e274414e97561cee4d7d9da7fc52120778e82ee5ab8ab8d14ea` |
| `research/clay_b_pressure_work_report-source_20260906.md` | `4516d108b7c9c2123ca6cfe7253f79b4267f2e75145587942b5f30ea0a057598` |

这三个哈希是本审计的源绑定。release manifest、冻结提交及其余依赖由整包
清单另行绑定；本文件不把辅助状态文件的当前哈希并入上述源绑定。

## 2. 相对检查点的数学不变性

对检查点 `9771fa5b79b25824ce015c2e9174ae9bc9de6ae7` 的实际
`git diff --unified=0` 显示：

- AI 只改了预检状态、manifest 与文献指针、历史审查说明和后续指针；
- AJ 只改了预检状态、manifest 与文献指针及结论边界中的文献说明；
- AI.1--AI.30 和 AJ.1--AJ.30 的公式、推导段落及结论量词没有改动。

检查点的完整文件哈希分别为
`efb38512be70c7c6dbfbadcd225b274aba72048f78f5a966cf23fe136b941e2f`
和
`ac9576a17189d93648d5a79d0c1b497f9f440a36b48ecd077ddd1b479d6ca32e`。
最终文件哈希变化来自上述状态与引用文字，不是未经复核的数学改写。

## 3. 报告的精确量词

完整读取 `clay_b_pressure_work_report-source_20260906.md` 后，逐项结论如下：

1. **固定能量。** 报告量词是每个固定 \(E_0>0\)，且
   \(\|u_\epsilon(0)\|_2^2=E_0\)；不是让估计常数暗中依赖整族的
   \(H(0)\) 或 \(H^1\) 范数。
2. **真实光滑 NS。** 解族是三维周期、零均值、光滑、无散、黏性 \(1\)、
   无外力的 Navier--Stokes 解，不是 Euler 解、辅助调制场或有限计算。
3. **明确短窗。** 时间为
   \(t_\epsilon=\tau_0\epsilon^{5/2}\)，其中 \(\tau_0>0\) 与
   \(\epsilon\) 无关；报告同时写明
   \(t_\epsilon/\epsilon^2\to0\)，所以没有冒称成熟扩散时间。
4. **固定相对增长与消失作用量。** 存在与 \(\epsilon\) 无关的
   \(\delta_0>0\)，使

   \[
   \frac{H_\epsilon(t_\epsilon)}{H_\epsilon(0)}\ge1+\delta_0,
   \qquad
   \int_0^{t_\epsilon}\|\nabla u_\epsilon(t)\|_2^2\,dt
   =O(\sqrt\epsilon)\to0.
   \]

   再结合 \(t_\epsilon\to0\)，得到
   \(\int_0^{t_\epsilon}(1+\|\nabla u_\epsilon\|_2^2)\,dt\to0\)。
5. **只排除一个精确形式。** 被排除的是对所有相应光滑解从初始时刻成立、
   常数仅依赖 \(E_0\)、前置系数严格为 \(1\)、没有加性预算的估计

   \[
   H(t)\le H(0)\exp\!\left[
   C(E_0)\int_0^t(1+\|\nabla u(s)\|_2^2)\,ds\right].
   \]

   报告没有把这个反例扩大成一般 \(L^3\) 上界或正则性反例。

## 4. 证明接口与范围边界

- AI 把已有周期正压力功场通过 curl cutoff 和高频压力比较转成光滑紧支撑
  Euclidean 无散场，并在固定 \(L^2\) 能量的单泡缩放上得到真实初始净增长。
- AJ 在扩张环面上给出与 \(L\) 和有效黏性无关的 \(H^5\) 短时控制，
  处理压力功的正时间连续性、零速集合和黏性耗散，再精确回缩到黏性 \(1\)
  的物理解。报告对这两个接口的叙述与源文件一致。
- 允许前置因子 \(K>1\)、加性预算、常数依赖 \(H(0)\) 或其他初值范数的
  估计没有被排除。
- 成熟时间、同一固定解的历史、首次奇点、缩球、原移动路径、近源压力、
  外壳支付及合同 G 均仍为 OPEN。
- 本结果不是 \(L^3\) 小数据 norm inflation，不是临界空间不适定性，
  也没有新颖性、优先权、论文等级或接近 Clay 的结论。

## 5. 文献和辅助记录

实际读取的 literature-boundary 明确限定为三篇原始来源的有界核查：
Tran--Yu 的压力 moderator、Bourgain--Pavlović 的负阶 Besov norm
inflation，以及 Kang--Yun--Protas 的固定初始 enstrophy 数值优化。
该记录只说明已核对陈述没有直接等同于 AJ.27--AJ.30，不以检索未命中证明
新颖性。

实际读取的 internal audit 已把旧的“尚无 report/manifest”限定为检查点
`9771fa5b` 的历史状态，并把最终冻结状态交给整包 manifest。工作计划也明确
自身不是冻结清单或发布状态。这些辅助记录没有虚构发布、外部同行审稿或
成熟时间完成。

## 6. 机械与最终判断

- AI.1--AI.30 共 30 个标签，AJ.1--AJ.30 共 30 个标签，末项均为 `.30`；
- 三份绑定源未发现异常 form-feed、vertical-tab 或 carriage-return 字节；
- 对三份绑定源执行的 `git diff --check` 通过；
- 本节是纯解析结果，没有仿真或科学图，不需要补造数值或图表证据。

**最终判断：PASS。** 三份绑定源在数学结论、报告量词和声明边界上相互一致，
可以进入整包 manifest 与冻结提交；此判断不等于外部同行审稿、网页发布或
Navier--Stokes 千禧年问题的解决。
