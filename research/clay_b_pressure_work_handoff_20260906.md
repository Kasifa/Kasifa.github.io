# 科学冻结移交：ClayB-PressureWorkWindow-20260906

- 逻辑前驱：ClayB-PressureQuotient-20260906。
- 研究仓库：/Users/kasifa/Documents/Math/navier-stokes-r074m。
- 科学源码提交：fd6fa4b2bcebb702ddc2e8c03884496dca139101。
- Manifest：research/clay_b_pressure_work_release_20260906.json。
- 研究源说明：research/clay_b_pressure_work_report-source_20260906.md。
- 最终实际源审查：research/clay_b_pressure_work_freeze_audit_20260906.md。
- 证明审查历史：research/clay_b_pressure_work_internal_audit_20260906.md。
- 直接文献边界：research/clay_b_pressure_work_literature-boundary_20260906.md。

本包合并 AI 的正压力功紧支撑化与固定能量初始增长，
以及 AJ 的统一非线性短时间窗。7 个科学源、4 个依赖，
11 行源码/依赖哈希与声明提交一致，60 个公式标签通过结构检查。
最终报告和实际证明的范围审查通过；机械检查不替代证明。

请固定“发布任务”按既有 FIFO 独立处理双语 HTML、导航、资产和验收。
保持个人研究员叙述风格及 PROVED LOCALLY / LITERATURE / OPEN /
NOT CLAY 边界。本包不更新累计 recap，无新读者 PDF、仿真或科学图。
不要补入前序 PressureQuotient；这是依赖于它的新合并小节。

必须保留的结论范围：

1. 每个固定初始 \(L^2\) 能量 \(E_0>0\) 下，构造的是不同初值组成的
   三维、光滑、零均值、黏性 1、无外力周期 NS 解族。
2. 时间为 \(t_\epsilon=\tau_0\epsilon^{5/2}\)，实际 \(H\) 比值至少
   \(1+\delta_0\)，同期累计梯度平方为 \(O(\sqrt\epsilon)\)。
   不只是残差大，也不是有限仿真的拟合。
3. 只排除报告中那条常数仅依赖 \(E_0\)、前置系数为 1、
   没有加性预算、从初始时刻起要求成立的指数估计。
   不改写成所有 \(L^3\) 估计均失败。
4. \(t_\epsilon/\epsilon^2\to0\)，严格早于成熟扩散时间。
   初始 \(H\) 和梯度平方发散，不能称作固定解首次奇点反例。
5. 有限文献比对不是新颖性证明，本结果不是 \(L^3\) 小数据
   norm inflation，更不是 Clay 结论。

本 release 只投递一次 release_id + source commit。
研究侧不读取发布队列、不等待或监督发布，继续同一解成熟时间的完整配对。
独立论文 v2 的私有登记包不包含在本次移交中。
