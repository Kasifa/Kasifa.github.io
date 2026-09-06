# 坏时间净压力工作：从频率支付到必要下界

2026-09-06。ClayB-BadTimeNetWork-20260906。
前置小节为 ClayB-PressureWorkWindow-20260906。
**PROVED LOCALLY / LITERATURE INPUT / NECESSARY CONDITION / G OPEN / NOT CLAY。**

本包冻结 AK--AQ 的推导期原文；原稿中的内部状态和下一步描述是
写作时记录，当前科学状态由本报告及 release manifest 统一说明。
原稿不直接充当读者页面。

这不是累计 recap。我只整理本小节新完成的频率分解、固定环带局部化
和坏时间必要机制，不重复前面已经冻结的压力符号与短时解族。

## 这一步最终得到什么

我从同一个周期 Navier--Stokes 解出发，固定指定中心、一个小半径、
空间截止和成熟窗口。低频压力与真正分离的低高压力可以由能量支付；
高高压力在局部高频尾足够小时也可以吸收。剩余项不是“高频压力很大”
这一模糊说法，而是坏时间上的正净工作

\[
 H_\chi=\frac13\int\chi|u|^3,\qquad
 D_\chi=\int\chi|u|
       \bigl(|\nabla u|^2+|\nabla|u||^2\bigr),
\]

\[
 h=P_{>K}u,\qquad p_h=T_{ij}(h_i h_j),\qquad
 \eta_K(\sigma)=\|\theta h(\sigma)\|_3,
\]

\[
 G_K=\{\sigma\in J:\eta_K(\sigma)\le\eta_*\},\qquad
 B_K=J\setminus G_K,
\]

\[
 \mathcal B_J=
 \int_{B_K}
 \left[\mathcal K_\chi(p_h)-\frac34D_\chi\right]_+\,d\sigma,
 \qquad
 \mathcal K_\chi(p)=-\int\chi|u|u\cdot\nabla p .
\]

若同一解确有一列合法的固定半径终端局部 \(L^3\) 大范数窗口，
那么本节证明的必要条件是

\[
 \liminf\frac{\mathcal B_J}{H_\chi(t)}\ge1.
\]

这不是 \(\mathcal B_J\) 的上界。现有能量估计尚未把该项控制为
终端能量的低阶误差，不能把所需上界当作已知。下一步必须从尚未使用的
Navier--Stokes 动力学或带符号结构中寻找真正的新控制。

## 能量波数接口为什么没有闭合

AK 先把压力的平滑低频部分作为完整局部配对处理，没有拆散压力内项
与 \(\nabla\chi\) 壳项。若终端固定球范数为 \(\Lambda_A\)，窗口长度为

\[
 \delta=c_0r^2\Lambda_A^{-4},
\]

则频率 \(K=o(\Lambda_A^{7/4})\) 时，低频压力成本相对
\(H_\chi(t)\) 趋于零。另一方面，能量只给

\[
 \int_J\|P_{>K}u\|_3^2\,d\sigma
 \le C K^{-1}A_J,
 \qquad
 A_J=\int_J\|\nabla u\|_2^2\,d\sigma .
\]

若取 \(K\asymp\Lambda_A^\alpha\)，使高频尾坏时间比例趋零的这个
充分估计仍要求

\[
 A_J=o(\Lambda_A^{\alpha-4}).
\]

有限总耗散只给 \(A_J=o(1)\)，不给这里的多项式速率。

AL 又在当前周期规范下复证了自适应耗散波数的能量层接口。带阈值
\(a\) 和黏性 \(\nu\) 时，其结论只有

\[
 \mathfrak d_{a,\nu}(t)
 \le1+C a^{-2}\nu^{-2}\|\nabla u(t)\|_2^2.
\]

因此能量给 \(\mathfrak d_{a,\nu}\in L_t^1\)，不能升级成相关正则性
准则所需的 \(L_t^{5/2}\)。窗口 Markov 估计回到与 AK 相同的耗散
速率缺口；它还没有控制压力的二次频率输出，也没有解决 Fourier
投影与空间截止不交换的问题。成熟条件本身不提供缺失的衰减率。

所以 AK--AL 的结果是一次有用的失败定位：低频可以付，高频速度尾的
能量时间分布也可量化，但这两者不能自动变成局部高频压力功的支付。

## 真正付掉的低高压力

AM 不再把压力输出简单分成低频和高频，而是先写

\[
 u=l+h,\qquad h=b+w,
\]

其中 \(l\) 是低频，\(b\) 是相邻过渡带，\(w\) 与 \(l\) 具有真正的
频率分离。压力精确分成 \(p_0+p_{lh}+p(h)\)；\(b\) 与 \(w\) 的
交互没有丢失，而是完整留在 \(p(h)\) 中。

无散条件使 \(\Pi(l,w)\) 获得一个逆频率梯度增益。逐带求和后得到

\[
 \|p_{lh}\|_\infty\le C M K^2\|\nabla u\|_2.
\]

把它放回原速度 \(|u|u\) 的完整局部压力配对，任意固定小份额的
\(D_\chi\) 可以吸收其梯度部分，其余由 \(M,r,K,A_J\) 支付。
选择

\[
 K=\Lambda_A^{3/4}
\]

后，两者的全部相对余项均趋零：\(p_0\) 的成本自行衰减，
\(p_{lh}\) 的余项只需能量给出的 \(A_J\to0\)。
这里没有遗漏 \(h=b+w\) 内部的交互；尚未付掉的正是
\(p_h=p(h)\)，即高频速度自相互作用产生的完整压力，包括其所有
低频输出。

## 从全环面原型到固定环带局部化

AN 先保留完整原速度测试，在全环面证明：若
\(h=P_{>K}u\)、\(p_h=T_{ij}(h_i h_j)\)、
\(\eta_K=\|h\|_3\)，则

\[
 |W_h|
 \le C\eta_KD+C\eta_KD^{1/2}\|u\|_3^{3/2}.
\]

周期 Sobolev 的非零均值低阶项保留在证明中。小 \(\eta_K\) 确能
吸收一部分耗散，但坏时间测度小并不控制坏时间上的压力功；当前时间
的 \(H\) 积分也不能未经证明换成终端 \(H(t)\)。AN 因而只是正确的
全域基准，不是局部闭合。

AP 使用已知 CKN 部分正则性为 AO 选择固定环带。对合同中的同一
suitable Leray continuation，候选首次奇点时间位于开放时空域内部。
CKN 给出奇异集的一维抛物 Hausdorff 测度为零；切到终端时间后，
空间奇异切片的 \(\mathcal H^1\) 测度为零。到指定中心的距离函数是
1-Lipschitz，因此几乎每个足够小的半径球面都避开该切片。
正则点邻域的有限覆盖再给出一个固定左时间管，在其中速度于球面附近
的固定环带本质有界。

这个环带可依赖解、continuation、首次奇点时间、中心与所选半径。
AP 没有给缩球时统一的厚度或常数，也没有推出压力或高阶导数界。

AO 在这个固定环带内取更大的源截止 \(\theta\)，使用局部尾

\[
 \eta_K(\sigma)=\|\theta P_{>K}u(\sigma)\|_3.
\]

近源高高压力由局部 \(L^3\)--\(L^9\) 估计处理；远源与测试区保持
固定距离。频率截止交换子分成内区、正则环带和外区：环带只使用
速度上界，内外区使用周期核的离对角衰减。扩大球上的梯度没有被
偷换成局部 \(D_\chi\)，而是以全局能量成本
\(B\|\nabla u\|_2^2\) 明确保留。

由此得到一个与 \(K\) 无关的固定阈值 \(\eta_*\)：在好时间
\(\eta_K\le\eta_*\) 上，

\[
 |\mathcal K_\chi(p_h)|
 \le\frac14D_\chi+C_{\mathcal S}
       \bigl(H_\chi+1+\|\nabla u\|_2^2\bigr).
\]

合并 AM 已付的低频参与压力后，局部恒等式保留为

\[
 H_\chi'
 \le C_{\mathcal S}\mathbf1_{G_K}(H_\chi+1)
    +C_{\mathcal S}(1+\|\nabla u\|_2^2)+f_K
    -\frac12\mathbf1_{G_K}D_\chi
    +\mathbf1_{B_K}\left(\mathcal K_\chi(p_h)-\frac34D_\chi\right).
\]

最后一项没有取压力绝对值，也没有因为坏集合可能很小而被删除。

## 为什么坏时间下界是必要的

令 \(H_t=H_\chi(t)\)。同一解的能量插值给

\[
 \int_J H_\chi(\sigma)^{4/3}\,d\sigma
 \le C M^2(A_J+M^2\delta).
\]

而 \(H_t\ge\Lambda_A^3/3\) 与
\(\delta=c_0r^2\Lambda_A^{-4}\) 保证
\(\delta H_t^{4/3}\ge c c_0r^2\)。因此每个这样的窗口内都能选到
一个真实时刻 \(s_J\)，使

\[
 \frac{H_\chi(s_J)}{H_t}\longrightarrow0.
\]

另一方面，AO 的微分不等式用积分因子反向积分后说：如果坏时间正净
工作很小，那么整个窗口内的早时 \(H_\chi\) 必须接近终端值。把上面的
\(s_J\) 代入，两者只能由坏时间项补偿，于是得到

\[
 \liminf\frac{\mathcal B_J}{H_t}\ge1.
\]

还有一个更精确的带权、带符号版本。写

\[
 \beta_K=\mathcal K_\chi(p_h)-\frac34D_\chi,
 \qquad
 w_J(\sigma)=\exp\left(-C_{\mathcal S}
       \int_{s_J}^{\sigma}\mathbf1_{G_K}(a)\,da\right).
\]

则

\[
 \liminf\frac1{H_t}
 \int_{s_J}^{t}w_J\mathbf1_{B_K}\beta_K\,d\sigma\ge1.
\]

这里 \(w_J\to1\) 一致，但没有
\(\int_{B_K}|\beta_K|\) 的控制时，仍不能免费删除权重。这条式子说明
大正贡献来自实际带符号配对，不是人为把压力全部绝对值化后的产物。

## 必要结论的准确量词

先固定同一个 suitable continuation、指定中心、由 AP 选出的环带、
半径 \(r\)、截止、能量界 \(M\) 与 \(c_0\)。若存在一列
\(t_n<T_*\)，满足

- \(\Lambda_{A,n}=\|u(t_n)\|_{L^3(B_r)}\to\infty\)；
- \(\delta_n=c_0r^2\Lambda_{A,n}^{-4}\)，且
  \(J_n=(t_n-\delta_n,t_n)\) 位于固定正则左时间带内；
- \(t_n-\delta_n\ge Cr^2\)，并在整个窗口固定
  \(K_n=\Lambda_{A,n}^{3/4}\)；

那么上述两个下极限结论成立。这里所有范数、压力和耗散都来自这一个
解，不是改变初值得到的解族。

本节不证明这列时间存在。在首次奇点接口中，固定半径 \(L^3\) 发散
需要其相应文献输入和量词；本节只说明一旦有合法序列，坏时间必须承担
什么净工作。若序列不存在，必要条件不会反向制造奇点或大范数。

固定半径结论也不是原合同 G。合同 G 还涉及随尺度改变的移动中心、
缩小半径、路径包含和尺度一致常数。AP 的环带常数依赖固定半径，
AO 的截止不随尺度移动；这里的 \(s_J\) 也只是各固定窗口内选出的时刻。
这些对象不能直接替换原移动缩球时钟。

## 已验证部分、文献边界与剩余缺口

AK--AQ 的代数、尺度、周期核估计、局部压力配对和积分因子均已完成
根任务逐式检查与独立实际文件审查。这里的“已验证”是内部数学审查，
不是外部同行评审；文件存在、哈希或机械检查也不替代证明。

AP 的外部输入没有被写成本地新定理。CKN 的 DOI 入口本轮只提供
书目信息；根任务实际读取的是公开原文转录中的相关定理、正则点定义
与覆盖位置，转录 OCR 存在符号损坏，因此没有声称重审全篇证明。
Albritton--Barker 作者稿的 Lemma 2.6 与脚注 5 已定向读取，
Barker--Popkin 的同类固定环带陈述只作接口交叉核对；没有移植它们的
全空间或边界主定理。

当前最具体的缺口是：能否从尚未使用的真实 NS 结构推出
\(\mathcal B_J\) 的上界，并与必要下界冲突。只改善坏集合测度、
重新命名耗散波数或再次使用总能量绝对连续性都不够。
此外，固定尺度结果到原移动缩球路径及合同 G 的一致延拓仍未完成。

本小节不宣称新颖性，不证明正则性、首次奇点排除或 Clay 问题，
也不提供 \(\mathcal B_J\) 上界。没有新增仿真、科学图或读者 PDF；
这是一份非累计研究报告。

## 完整推导源

- `research/clay_b_mature_frequency_preflight_20260906.md`（AK）：
  低频完整压力配对与高频尾能量时间分布。
- `research/clay_b_periodic_dissipation_wavenumber_preflight_20260906.md`（AL）：
  周期耗散波数的能量层复证与窗口 Markov 边界。
- `research/clay_b_separated_pressure_pair_preflight_20260906.md`（AM）：
  分离低高压力的无散增益和完整局部支付。
- `research/clay_b_global_high_high_pressure_preflight_20260906.md`（AN）：
  保留全部压力输出的全环面高高小尾原型。
- `research/clay_b_fixed_regular_annulus_interface_20260906.md`（AP）：
  CKN 输入、终端切片和固定正则环带的几何推论。
- `research/clay_b_local_high_high_pressure_preflight_20260906.md`（AO）：
  固定环带上的局部好时间吸收与坏时间净工作。
- `research/clay_b_bad_time_net_work_necessity_20260906.md`（AQ）：
  正净工作相对终端能量的必要下界及带权符号版本。
