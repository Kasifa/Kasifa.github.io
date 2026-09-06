# 首次奇点的集中信息：适用范围预检

2026-09-06。**HISTORICAL PREFLIGHT / 文献接口与候选推导记录 / G OPEN。**
接续已冻结 PlateauHistory。这里不再优化 A+P 绝对账本的常数。

本预检已由 clay_b_concentration_path_limits_20260906.md 和
clay_b_local_persistence_obstruction_20260906.md 收束。
以下保留当时的候选状态和来源核查过程；当前完成范围与下一步见
clay_b_concentration_limits_work_plan_20260906.md，不把下文旧待办当作新待办。

## 1. 本轮已读取的来源及层级

以下是有界范围的来源核查，不是完整领域综述或查新。

1. [Seregin, A certain necessary condition of potential blow up for Navier--Stokes equations](https://arxiv.org/pdf/1104.3615v1)，
   arXiv:1104.3615v1，2011-04-19，Theorem 1.1。
   核对了全空间、光滑紧支撑无散初值及完整 L³ 极限发散的条件。
   不能把这个全空间表述直接当成周期定理，也没有指定缩球半径。
2. [Barker--Prange, Localized smoothing for the Navier--Stokes equations and concentration of critical norms near singularities](https://arxiv.org/pdf/1812.09115v2)，
   arXiv:1812.09115v2，2019-01-09，Theorem 1、Theorem 2 和 (14)--(15)。
   指定奇点的抛物尺度 L³ 集中含统一 Type-I 局部能量上界。
   定理 1 的数据类别还保留无穷远局部 L² 衰减。
   这些条件不能由本合同的周期能量类直接假定。
3. [Barker--Prange, Quantitative Regularity for the Navier--Stokes Equations Via Spatial Concentration](https://link.springer.com/article/10.1007/s00220-021-04122-x)，
   2021-06-14，Theorem A。
   该定理在全空间 mild 解框架中要求时间一致的弱 L³ 上界，
   再推出定量局部集中；这不是无额外假设的历史上界。
4. [Albritton--Barker, Localised necessary conditions for singularity formation in the Navier--Stokes equations with curved boundary](https://arxiv.org/pdf/1811.00507v2)，
   arXiv:1811.00507v2，2019-11-18，Theorem 1.1、Definition 2.1、
   Remark 3.4。内点结论在每个固定球中给完整 L³ 极限发散，
   不要求 Type-I 上界；下一项优先检查它的周期局部应用。

上述时间是版本/出版时间，不采用搜索引擎爬取时间当成研究发布时间。
来源检索仅使用原论文/arXiv/出版方，第三方摘要不作证明依据。
读取的定理是文献输入，不宣称已逐行独立重证其全篇证明。

## 2. 周期局部应用的候选接口

设原 suitable continuation 在 T_* 前等于光滑周期解。
现在额外是在反证中指定一个实际奇点 (x_*,T_*)，
不是断言首次奇点时间片的每个空间点都奇异。

候选应用：取嵌入环面的一个小坐标球 Omega，
x_* 为其内点，Gamma=空集。局部提升并限制原 u,p，
内部测试的分布方程和局部能量不等式保持不变，
而任意 t<T_* 前的 L∞ 有界性来自已知光滑性。
不能在人工球边界额外施加原解没有的无滑移条件。

若按 Theorem 1.1 的内点解释完成适用性核验，则对每个固定小 r 有

\[
 \lim_{t\uparrow T_*}\|u(t)\|_{L^3(B_r(x_*))}=\infty .
\tag{Z.1}
\]

这是已有定理的局部推论，不是新结果或正则性矛盾。
独立来源通道已核验内点/Gamma 空集的逻辑，但必须附带明确的源文说明。
父级按 PDF 阅读流程渲染并完整查看第 4--5 页后确认，
v2 的 Definition 2.1(1) 原页确印成
\(\overline{\Omega'}\subset\Omega\subset\Gamma\)，不只是文本提取失真。
这与非空域 Omega 及 Gamma 属于其边界不相容。
本稿显式按标准预期条件
\(\overline{\Omega'}\subset\Omega\cup\Gamma\) 理解，
内部依据是同一定义(3)的测试域、Proposition 2.2 的正确闭包条件，
以及 Remark 3.4 的内点证明。该解释是注明的排字修复约定，
不是声称作者公布过勘误。

独立通道按此约定给出 CONDITIONAL PASS；没有找到对人工球边界
另加无滑移条件的必要性。没有取得可视觉核验的出版社排版 PDF，
故不声称出版稿已修复。停止为同一排字问题重复检索，不因此阻塞主线。
Z.1 作为带上述说明的文献内点推论，仍需在正式接口稿中完整列出适用性。
它不需要强 L² 或 L³ 终点迹，因为结论只使用 t<T_* 的光滑值。

## 3. 原路径与缩球：下一项待审候选计算

Z.2/Z.3 已由 r076l_heat_chebyshev 对实际文件独立复算通过。
本稿的完整文献接口和以下应用说明尚未科学冻结。
令 M=ess sup_(t<T_*) ||u(t)||_(L²(T³))<infty。
原紧支撑核给固定合法 R 下

\[
 |a_R(s)|\le C_\varphi R^{-3/2}M,\qquad
 |X_R(t)-x_*|\le C_\varphi M R^{-3/2}(T_*-t).
\tag{Z.2}
\]

每个 R 的路径都仍锚定于同一个 x_*，没有改成一条统一路径。
固定 R 时 Z.2 给晚时间的球包含，可将 Z.1 转到该固定路径的小球。
但取 R 随 t 缩小时，归一化漂移成本是

\[
 \frac{|X_R(t)-x_*|}{R}
 \le C_\varphi M (T_*-t)R^{-5/2}.
\tag{Z.3}
\]

在本合同的归一化单位下，若 h=T_*-t、R=h^alpha 且 0<alpha<2/5，
则此粗成本趋零，且晚时间 h<64R²，路径在原定义域内。
若 R 取抛物尺度 h^(1/2)，该上界反而为 C M h^(-1/4)。
后者只说明此粗估计不给小漂移，不是证明真实漂移发散或该包含不可能。

即便 Z.1 已核验，也只具有“每个固定 r，再令 t 趋近 T_*”的量词。
不能交换为任意预定 R(t)，尤其不能未经证明取 R(t)~sqrt(h)。
一个定性对角选择可能给缓慢缩小半径，但不自带所需速率或 G 的能量小性。
下一步先审查这项量词与漂移接口，再决定是否有值得继续的定量输入。

## 4. 尚未完成的工作

1. 将已核验的 Albritton--Barker 内点适用性写入正式接口稿，
   保留上述排字说明；不继续为未取得的出版排版稿反复检索。
2. Z.2/Z.3 实际文件已通过独立代数审查；补出固定球到原路径的明确包含，
   并对完整接口稿做实际文件复核，不能使用跨尺度路径嵌套。
3. 如写对角缩球引理，保留其非定量性；不把临界范数发散本身当成
   与有限能量矛盾。
4. 只在能减少原 G-P/G-C 或跨平台/负工作缺口时继续发展。

检索记录：首次奇点局部集中/Type-I；Seregin L³ 完整极限；
再沿 Barker--Prange 的固定球对照找到 Albritton--Barker 原定理。
本预检不引用未核验的新近进展，不以这些有限检索断言全领域最佳结果。
停止当前检索扩张，优先核清已选定的内点接口。

没有新仿真、DGX 或科学图需求；没有发布本工作稿或修改论文专项。

来源页核对记录：arXiv v2 PDF SHA-256 为
fdd91e657b5cf503286b4e45cc084c12c8b202aaf24bcdad67edea46edfa4102。
只对相关 Definition 页面做原页视觉核查，不声称检查过全文排版。
本轮没有生成新读者 PDF。
