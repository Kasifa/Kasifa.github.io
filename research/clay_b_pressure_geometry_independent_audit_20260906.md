# 压力预算、方向结构与符号构造：独立审查记录

2026-09-06。内部实际文件解析复核，不是外部同行评审、形式化证明或新颖性审查。

## 对象与作者隔离

| 实际源与范围 | 作者 | 独立实际文件审查 | 结果 |
|---|---|---|---|
| mature_l3_budget_preflight，AB.1–AB.5 | 父级 | r076l_figure_audit；r076l_heat_chebyshev 复算 AB.4–5 | PASS |
| mature_l3_budget_preflight，AB.6–AB.8 | 父级及 r076l_proof_audit 推导 | r076l_figure_audit 全部增量；父级复算 | PASS |
| pressure_geometry，AC.1–AC.14 | 父级 | r076l_figure_audit、r076l_heat_chebyshev | 修订域边界后 PASS |
| pressure_sign，AD.1–AD.23 | r076l_proof_audit | 父级、r076l_figure_audit、r076l_heat_chebyshev | PASS |

作者不计入自己所写源文件的独立审查。父级读完三份源并逐式检查；
审查不是只看聊天候选公式。AB 的实际文件复核先于本包整理完成，
本次合并只更新其工作稿/冻结状态，没有改动 AB.1–AB.8 的数学。
AC、AD 的最终元状态调整也没有改变已审公式。

## AB：带符号预算和固定球远源项

q_epsilon 正则化给耗散与 cutoff 的准确系数，压力内项有支配收敛；
零集的加权乘积取零。压力 gauge 加上 c(t) 后合并压力功不变。
反向恒等式为 H(s)=H(t)+integral D−integral W，符号已复算。

固定球远源梯度的 L∞ 界 CM²r^(−4)，乘速度平方能量 M²，
再积分 delta=c0r²L^(−4)、除 H_chi(t)≥L³/3，得到
Cc0M⁴r^(−2)L^(−7)。没有误用 AA 的裸压力冲量。
固定 M/r、缩球、成熟时间条件与原移动路径的不同范围均保留。

AB.6 的 Hölder、插值与周期 Sobolev 低模项正确，
最后留下 (CL+eta−1)D，不能对大 L 吸收。
高频剪切只排除从 L 单独推出 D 上界，没有冒充动力学反例。

## AC：方向、临界缺口与适用域修复

非零集的正交分解给 D=2D_r+D_theta；加权密度合法延零，
没有声称 e 跨零集属于普通 H¹。
F=q div e=−e·grad q、W=−integral pqF 的符号正确。
q_epsilon/e_epsilon 的精确恒等式和支配量支持全域极限。

三维投影 Frobenius 范数平方为 2，故
Z_e≤min(D_r,2D_theta)≤2D/5。这个常数不消除大 L 系数。
F 的临界指数和为 2，能量 L²_tL²_x 的指数和为 5/2。

AC.10 的 Hölder 指数 9/4、9/2、3，插值、周期低模项与 Young
全部一致；beta∈L²_t 在有限时间给 beta+beta²∈L¹_t。
Gronwall、L³_tL⁹_x 与 AC.12 的 18/7 插值准确。
grad u 的均值为零，椭圆/Sobolev 无遗漏常模；
全局能量补足 full H¹，再调用标准次临界局部存在共同寿命。

父级与 r076l_heat_chebyshev 实际核对 Vasseur 全6页作者稿：
日期 2007-04-25、全空间 Leray–Hopf 量词、Theorem 1 的
2/a+3/b≤1/2、a≥4、b≥6，以及式(3)和中间加权量。
未加权方向散度的临界线为 1；原文条件并非该量的尺度临界条件。
父级与该审查通道也核对 Tao Notes 1 Remark 46 的次临界范围，
没有把只陈述较高 Sobolev 阶数的 Theorem 38 直接当作 H¹ 定理。
这些是原来源核验，不代表在本包重证全部背景理论。

Taylor–Green 的压力、热因子和 NS 方程逐项满足。
其方向散度主项 (y²−x²)/r³ 在固定角锥有 1/r 下界，
管状积分 integral r^(1−b)dr 在 b≥2 发散；F 仍有界。

r076l_heat_chebyshev 指出一处必须修复的域边界：
周期例不能判定 Vasseur 全空间原类中条件的必要性。
父级已改为“同型条件不是周期光滑性的必要条件”，并明确不判定原全空间类。
同一审查通道实际重读修订行及 D 首次显式定义，确认 PASS。
这项修复保留原公式，不把周期反例扩大到全空间。

## AD：压力功严格正负号

六个 Fourier 源系数均为 −1；压力对应 −1/2、−1/5、−1 的分母
是模式 Laplace 特征值。唯一配对给 I=pi²，积分未作体积归一化。
背景和两个交叉张量双散度精确为零，所以 p_epsilon=epsilon²p_v。

非消失性 |V_epsilon|≥1/2 保证 Taylor 余项一致，
不是形式渐近。K 的非对角项因奇性为零；
辅助 mathcal J(1)=0 且 J'(r)>0 给所有 a>1 的 kappa(a)>0。
余项中 2pi 是第三维积分长度，已经显式写入。
两条独立通道均审查了补上 2pi 后的实际源文件。

p(−u)=p(u) 与 W(−u)=−W(u) 是初值恒等式，不是正向轨道对称。
幅值齐次 H、D、W 分别为 A³、A³、A⁴；
先固定 U，再选有限 A，每个初值各自有局部光滑寿命。
严格增长能延续一段正时间，但该寿命不要求在 A 中一致。
能量增长、非成熟时间、非首次奇点、非固定能量等边界均准确。

## 冻结门禁

报告与计划另经 r076l_figure_audit 实际文件语义核查。
其指出报告中 div e 与 1/r 的简写可能被误读成全方向双边可比，
父级已改为次齐性主项及固定角锥中的下界，保留严格适用范围。
最终修订复查结果记录在 manifest。
结构、控制字符、定界符、唯一标签、文件哈希和提交一致性也由 manifest
记录实际检查结果；这些机械门禁不代替上述解析审查。
三份数学源共 45 个编号公式，没有数值计算或数值证书的声明。
无仿真、DGX 或科学图需求；不生成新读者 PDF，不更新累计 recap。
合同 G 与一般三维正则性继续 OPEN / NOT CLAY。
