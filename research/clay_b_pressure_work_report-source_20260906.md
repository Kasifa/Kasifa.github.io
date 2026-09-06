# 固定总能量不能给出这条 L³ 增长预算

2026-09-06。研究源说明，非网站文件。
**PROVED LOCALLY / LITERATURE / OPEN / NOT CLAY。**

## 这次检查什么

上一节的压力残差可以在不做压力功的平台上很大。因此，仅仅证明残差界
失败，还不能回答真实 NS 的 \(L^3\) 增长是否能由能量耗散控制。
我在这一节保留真实压力功，检查一条明确的候选估计。

在三维周期环面上取黏性 1、无外力的 NS。记
\[
 H(t)=\frac13\int_{\mathbb T^3}|u(t)|^3,\qquad
 E_0=\|u(0)\|_2^2.
\]
候选式为
\[
 H(t)\le H(0)\exp\left[
 C(E_0)\int_0^t\bigl(1+\|\nabla u(s)\|_2^2\bigr)\,ds\right].
\]
这里常数只依赖固定 \(E_0\)，没有前置因子或加性预算，
并且要求从任意光滑初值的初始时刻起成立。
本节证明：这个准确形式不能对所有这些解成立。

## 得到的光滑解族

对每个固定 \(E_0>0\)，可以构造零均值、光滑、无散的周期初值族
\(u_\epsilon(0)\)，满足 \(\|u_\epsilon(0)\|_2^2=E_0\)。
相应的真实 NS 解在
\[
 0\le t\le t_\epsilon,\qquad t_\epsilon=\tau_0\epsilon^{5/2}
\]
上光滑；\(\tau_0>0\) 与 \(\epsilon\) 无关。存在固定 \(\delta_0>0\)，使
\[
 \frac{H_\epsilon(t_\epsilon)}{H_\epsilon(0)}\ge1+\delta_0,
 \qquad
 \int_0^{t_\epsilon}\|\nabla u_\epsilon(t)\|_2^2\,dt
 \le C\sqrt\epsilon\longrightarrow0.
\]
因此候选式右侧除以 \(H_\epsilon(0)\) 后趋于 1，
而实际比值保持一个固定正增量。这不是数值拟合或有限采样判断。

## 为什么这次确实是压力做功

全环面恒等式为
\[
 H'+D=W,\qquad
 D=\int |u|\bigl(|\nabla u|^2+|\nabla|u||^2\bigr),\qquad
 W=\int p\,u\cdot\nabla|u|.
\]
已有 AD 周期构造给出严格正压力功。AI 用周期向量势的 curl cutoff
把它转成全空间紧支撑无散场。高频压力主项保留正号；
低频平均压力和 cutoff 修正的误差都作了积分估计。
零速处使用全局 Lipschitz 张量，不除以速度或 cutoff。

固定一个这样的紧支撑场 \(V\)，将其归一化到能量 \(E_0\)，再作单泡缩放。
AI 给出真正的初始净增长，AJ 证明它可以持续一个统一的重标时间窗。
重标后环面边长为 \(2\pi/\epsilon\)，黏性为 \(\sqrt\epsilon\)。
证明逐项控制了扩大环面上的 Sobolev 常数、局部存在区间和压力功连续性。
正时间的压力尾部使用全环面估计，不假设解继续紧支撑。

## 这个反例没有说明什么

首先，
\[
 \frac{t_\epsilon}{\epsilon^2}=\tau_0\sqrt\epsilon\longrightarrow0.
\]
它早于单泡的扩散尺度，不是成熟时间窗口。
固定能量也不等于固定全部初值范数：
\(H_\epsilon(0)\asymp\epsilon^{-3/2}\)，
\(\|\nabla u_\epsilon(0)\|_2^2\asymp\epsilon^{-2}\)。
这里是一族不同初值的解，不是一条固定解的首次奇点历史。

本节不排除允许常数依赖 \(H(0)\)、增加前置因子或加入额外预算的一般估计；
也没有排除成熟时间上的额外动力学控制。
合同 G、缩球、原移动路径、近源压力与外壳支付仍然 OPEN。

## 与已有文献的关系

压力功恒等式、压力 moderator、负阶 Besov 空间的 norm inflation
以及极端 enstrophy 增长计算，均已有相关文献。
本节的解类、固定量和结论不能与这些对象混写。
定向核对和原始链接见
research/clay_b_pressure_work_literature-boundary_20260906.md。
本节不宣称首创，也不将自己的相对增长称为 \(L^3\) 小数据 norm inflation。

## 审查与下一步

AI 和 AJ 各有 30 个编号公式，完成了根任务全文检查和独立实际文件审查。
主要修订涉及扩大环面的体积因子、直接 Leibniz 估计与高阶延拓。
内部独立审查不等于外部同行审稿；机械检查也不替代数学证明。

这是一项候选估计的排除结果，不是一般正则性定理。
我接下来回到同一解、固定半径上的成熟时间恒等式，
保留近源压力、外壳输运和有利耗散，不重复放大早时初值来代替时间估计。
本节没有新仿真、科学图或累计 recap。
