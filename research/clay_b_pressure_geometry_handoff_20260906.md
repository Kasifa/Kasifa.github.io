# 科学冻结移交：ClayB-PressureGeometry-20260906

- 逻辑前驱：ClayB-ConcentrationLimits-20260906。
- 研究仓库：/Users/kasifa/Documents/Math/navier-stokes-r074m。
- 科学源码提交：40b18a9c29499f4956d72e197f8d285bd3f6b453。
- Manifest：research/clay_b_pressure_geometry_release_20260906.json。
- 研究源说明：research/clay_b_pressure_geometry_report-source_20260906.md。
- 证明：mature_l3_budget_preflight、pressure_geometry、pressure_sign，均在 research/ 且日期后缀为 20260906.md。
- 实际文件独立审查：research/clay_b_pressure_geometry_independent_audit_20260906.md。

本包把 AB、AC、AD 合并为一个研究小节：6 个科学源文件、3 个依赖，
9 行提交/工作树/hash 一致，45 个公式标签与字节结构检查通过。
这些机械检查不是证明；独立解析审查及修复范围见审计源。

请固定“发布任务”按既有 FIFO 独立处理双语 HTML、导航、资产与验收。
保持个人研究员叙述风格和 LITERATURE / CONDITIONAL / PROVED LOCALLY /
OPEN / NOT CLAY 的区分。本节没有累计 recap、新读者 PDF、仿真或科学图。

必须保留的边界：

1. 远源带权压力功小量只在同一固定 M、r 下成立，不支付近源和外壳。
2. F 的临界条件没有由能量推出；周期条件接口沿已有方向准则思路，
   没有无条件正则性、新颖性或发表等级声明。
3. 显式压力功符号例子只给改变初值后的瞬时/短时行为，放大幅值同时
   放大能量；不否定成熟时间或固定解首次奇点附近的估计。
4. 周期 Taylor–Green 的零线不是 NS 奇点，也不判定 Vasseur 全空间
   原类中的条件必要性；方向散度的 1/r 下界只在固定角锥内使用。

只投递一次 release_id + source commit。研究任务不读取发布队列，
不等待、重试、监督、部署或报告发布执行，随后继续 F 的真实演化检查。
独立论文 v2 私有登记包不包含在本次移交中。
