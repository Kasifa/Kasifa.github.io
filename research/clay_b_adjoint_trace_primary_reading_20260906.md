# 弱初迹伴随：四个原始文献接口

2026-09-06。**LITERATURE / BOUNDED APPLICABILITY AUDIT / G OPEN / NOT CLAY。**

我按 BS 的实际问题筛选定理，不把标题中的“唯一性”视为可直接使用的结论。
本次是有界原始文献核读，不是穷尽检索或已完成的 Deep Research 报告。
下述文献均不证明当前正原子假设能够发生或必须排除。

## 1. 要匹配的对象

BS.1--6 已确定：在三维固定环面上，
\(w_\rho+P\operatorname{div}(w\otimes b)=\nu\Delta w\)，
\(b=-u(T-\rho)\) 来自同一个无外力 NS 原解。
\(b,w\in L^\infty L^2\cap L^2H^1\)，\(w\in C_wL^2\)，
初迹弱零，但能量右极限为一。
\(b\) 在这个方向满足负黏性方程，不另当成正黏性 NS 解。

这需要的是带非局部压力的向量方程之弱初值接口。
BS.4 的从零初值能量不等式尚不成立。
BS.15 的强时间导数条件也没有从基本能量支付。
以下分别比较扩散符号、零迹端点、压力、定义中的能量条件及漂移范数。

## 2. Escauriaza--Seregin--Šverák：后向抛物唯一性

原文：*Backward Uniqueness for Parabolic Equations* (2003)，
DOI [10.1007/s00205-003-0263-8](https://doi.org/10.1007/s00205-003-0263-8)。
核读的是作者托管的 [11 页 PDF](https://www.pdmi.ras.ru/~seregin/Recent%20Publications/complementtoball.pdf)。

PDF 第 3 页 Theorem 1 的实际主部是 \(\partial_s+\Delta\)，
零迹放在 \(s=0\)。它还要求闭合的点态微分不等式、
规定的空间增长和局部导数可积性。
同页明确允许向量函数，故不能用“仅标量定理”来否定它。

当前 \(w\) 在 \(\rho=0\) 弱零，但主部是
\(\partial_\rho-\nu\Delta\)；当前 \(A\) 的主部虽为反向扩散，
弱零迹却在右端 \(T\)。单纯反时同时改变主部与端点，
没有把对象变成 Theorem 1 的输入。
这里首先就有方向及迹意义的错配，不能仅改变量名套用。

压力还要求另一层核对。若尝试对 \(w\) 取旋度，
输运项的交换子含 \(\nabla b\,\nabla w\)；
它不是已经付清的、只由旋度及其一阶导数构成的点态下阶项。
没有建立所需系数界，也不能用非局部 Riesz 控制替代点态闭合。
这只记录当前缺少的输入，不断言所有未来旋度方法都不可能。

核读范围：主任务完整读取并可视检查 PDF 1--3 页。
未重做 4--11 页的 Carleman 证明；本次不靠那部分新推导，
只作定理输入的排除性比较。

## 3. Lei--Yang--Yuan：压力并未消失，但解类更强

原文：*Backward uniqueness for 3D Navier-Stokes equations with non-trivial final data and applications*，
[arXiv:2311.02429v1](https://arxiv.org/abs/2311.02429v1)，提交日 2023-11-04。
PDF 内署日 2023-11-07，与版本提交日分别记录。

Theorem 1.1 在全空间讨论两个有界 mild NS 解及有界涡量，
并匹配终值。其加权论证确实处理非局部压力，
所以本次不采用“压力一出现就无文献可用”的说法。
Remark 1.1 在相应有界 mild 条件下讨论涡量假设，
没有把有界 mild 条件一并取消。

当前 \(w\) 是周期线性压力耦合伴随，不是上述两个有界 mild NS 解之差；
仅有能量漂移，零迹还处于前向初端。
Corollary 1.3 涉及的临界空间也不是基本能量自动提供的条件。
PDF 第 9 页 Corollary 3.3 的测试空间与第 4 节方程 (4.1)
进一步显示，不能只抽取“后向唯一性”四个字而省略函数空间和扩散方向。

核读范围：主任务完整读取 PDF 1--3、9--10 页，可视检查 3、9 页。
这是定理及使用接口核读；没有宣称复核全篇权重与 Carleman 证明。
同文反例的全空间压力设置也不拿来当作本周期问题的反例。

## 4. Cheskidov--Luo：最近的压力线性对偶接口

原文：*Sharp nonuniqueness for the Navier-Stokes equations*，
[arXiv:2009.06596v2](https://arxiv.org/abs/2009.06596v2)，版本日 2022-04-13，
PDF 内署日 2022-04-14。只使用其定义和 Appendix A 的唯一性接口，
不把主文非唯一性构造当成当前解类的反例。

Appendix A 在周期域引入压力耦合线性方程及反向测试方程。
它的确与当前问题有结构上的交集。
但 Theorems A.1--A.3 的输入包含临界
Ladyzhenskaya--Prodi--Serrin 范数，不是只有能量类漂移。
其 \(X^{p,q}\) 在 \(p=\infty\) 时定义为 \(C_tL^q_x\)；
三维 \(q=3\) 端点不能误写成任意 \(L^\infty_tL^3_x\)。

主任务完整核读 Appendix A（PDF 32--34 页）。
关键付费点是使反向测试的时间导数、二阶空间导数、
输运及压力梯度在 \(L^2\) 中成立：
\(q>3\) 情形用临界时间可积性进入估计，
\(q=3\) 端点的分解还使用时间连续性。
原文引用的热方程最大正则性定理没有在本次重证。

Theorem A.2 构造的能量解具有从初始时刻出发的能量不等式。
不能先宣布当前 \(w\) 就属于这个更窄解类，
再把 BS.3 的初端能量跳跃排除。
此外原文这一接口以正向 NS 速度为输入；
\(b=-u(T-\rho)\) 不字面满足那个方程假设。
即使抽取只依赖漂移范数的线性估计，也需说明改写，
且临界范数仍然未付。

本次比较与 BS.18 相容：额外 Serrin 条件足以给张量 \(L^2\)，
但对同一 NS 原解，它仍是额外正则性输入，不是新的能量闭合。
核读范围：PDF 1--3、32--34 页完整提取，32--34 页可视。
主文构造及 Appendix B 未作为论据导入。

## 5. Bonicatto--Ciampa--Crippa：标量弱初迹定理确实更强

原文：*Weak and parabolic solutions of advection-diffusion equations
with rough velocity field*，
[arXiv:2306.15529v1](https://arxiv.org/abs/2306.15529v1)，版本日 2023-06-27。
后续期刊版本 DOI
[10.1007/s00028-023-00919-6](https://doi.org/10.1007/s00028-023-00919-6)
仅作元数据，不把 v1 核读自动等同于期刊逐字复核。

Definition 2.3 的标量 parabolic solution 是能量空间内的分布解，
没有先把从初始时刻的能量不等式放进定义。
Theorem 2.7 对无散 \(b\in L^2_{t,x}\) 给唯一性。
所以“能量空间加弱零初迹总不足以给唯一性”是过宽的说法：
在这个标量方程中，原文给出了正面的定理。

Lemma 2.6 的关键是漂移平移与解梯度产生 \(L^1\) 交换子收敛；
Theorem 2.7 使用有界导数的凸函数完成重整化测试。
主任务完整读了这两个证明，不只读取摘要。

当前方程的差别不在漂移是否无散，而在向量压力。
对光滑向量方程的凸函数 \(\beta(w)\) 测试，压力在等式右侧给
\[
 \int_\Omega \pi\,\operatorname{div}(D\beta(w)).
\]
一般没有消失或确定符号。
取二次 \(\beta=|w|^2/2\) 会利用 \(\operatorname{div}w=0\) 消去压力，
但 \(D\beta=w\) 无界，不能据上述 \(L^1\) 交换子收敛直接完成极限。
这是一项具体的证明接口障碍，不是声称压力问题不存在唯一性定理。

核读范围：PDF 1、5--9 页完整提取，可视 6--8 页；
Definition 2.1、2.3，Lemma 2.6 与 Theorem 2.7 的证明均覆盖。
第 9 页后续极限议题没有作为本节结论导入。

## 6. 可复核来源身份与历史去重

以下文件只作本地来源证据；不纳入公开发布包，不再分发第三方 PDF。

- ESS：本地 /tmp/ns-adjoint-trace.x6ZtIb/ess-backward-2003.pdf；
  11 页，156012 B；
  SHA256 8ab537af5ff5b23d9c6756617476bc9c366905aaf8338a1d4f82e62136325c7c。
- Lei--Yang--Yuan：
  /tmp/ns-terminal-uniqueness.3jqp9E/pressure-coupled-bu-2311.02429.pdf；
  16 页，188409 B；
  SHA256 bb9496ccf3b3f2c962b97a2cd1ffaa4e239ace8fbd174b154baa100ad08a9a81。
- Cheskidov--Luo：/tmp/cheskidov-luo-2009.06596.pdf；
  38 页，554602 B；
  SHA256 8921976e8c7b0a81668534c2014bfbe610feeab40efb3673ad56ed33227180dd。
- Bonicatto--Ciampa--Crippa：/tmp/bonicatto-ciampa-crippa-2306.15529.pdf；
  12 页，438696 B；
  SHA256 f5a5699472f40a48997a37c9772176770154a36724ad1f1a999b66377dfe300e。

历史对照：
旧物理伴随稿 B.3--5 已警告强迹与 suitable 缺陷测度的识别边界。
R0.71R、R0.71S 已记录 ESS 及 Lions--Magenes 的适用性问题。
本节没有把这些基础警告再宣称为新发现；
新工作是对 BP 的具体伴随推得 BS.8--17 的精确端点通量及必要障碍。

主任务本次完整读旧物理伴随稿、R0.71R 与 2026-09-05 来源账本；
R0.71S 读取完整相关 §§2.1--2.2、4.4、4.6，
没有声称重读整份历史文献综述。
团队额外定向检索的候选仅作内部范围记录，不代替上述四份原文的核读。

## 7. 这次筛选实际说明什么

在已核读的四个接口中，没有一个可在不增加假设的情况下直接排除当前 \(w\)：
ESS 的方向和迹不匹配；Lei--Yang--Yuan 使用更强 NS 解类；
Cheskidov--Luo 的压力对偶需要额外临界输入；
Bonicatto--Ciampa--Crippa 的标量凸测试不能直接跨过向量压力。

这不是“文献中绝无适用定理”的证明，不据此宣布一个公认开放问题，
也不作新颖性认证。当前能精确主张的是：
BS 给出了待付初端通量，已有基本能量没有付清它，
而本次四个已读接口不能被无条件导入。
下一步应检查具体的压力测试和同一原解结构，
不是继续按相似标题无界检索。
