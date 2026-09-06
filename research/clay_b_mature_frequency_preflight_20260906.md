# 成熟窗口的低频压力支付与能量尾诊断

2026-09-06。**WORKING / INTERNAL / NOT FROZEN / G OPEN / NOT CLAY。**

本稿接续 AB 的固定球成熟时间恒等式，只处理一个有界的频率问题：
低频压力的**完整局部配对**可以由全局能量支付到什么程度，以及同一
频率截断下，高频速度的 \(L^3\) 尾在短窗口中能得到什么时间分布界。
两项估计都针对同一个光滑周期解；它们不构成近源压力、高频压力或
合同 G 的闭合，也不宣称新颖性。

## 1. 同一频率截断与窗口

在 \(\mathbb T^3=(-\pi,\pi]^3\) 上取实偶函数
\(\varphi\in C_c^\infty(\mathbb R^3)\)，满足

\[
 0\leq \varphi\leq1,\qquad
 \varphi(\xi)=1\quad(|\xi|\leq1),\qquad
 \varphi(\xi)=0\quad(|\xi|\geq2).
\tag{AK.1}
\]

对 \(K\geq1\) 定义

\[
 \widehat{P_{\leq K}f}(k)=\varphi(k/K)\widehat f(k),
 \qquad P_{>K}=I-P_{\leq K}.
\tag{AK.2}
\]

这不是锐投影；以下所有“低频”和“高频”均指这一固定平滑分解。
令 \(p\) 是零均值周期压力，并写

\[
 p_{\leq K}=P_{\leq K}p,\qquad
 p_{>K}=P_{>K}p,\qquad
 v_{>K}=P_{>K}u.
\tag{AK.3}
\]

固定 \(0<t<T_*\)、\(0<r<\pi/4\) 和 AB 中的空间截止
\(0\leq\chi\leq1\)，其中 \(\chi=1\) 于 \(B_r\)，
\(\operatorname{supp}\chi\subset B_{2r}\)。记

\[
 M=\sup_{0<\sigma<T_*}\|u(\sigma)\|_2,\qquad
 \Lambda=L_r(t)>0,\qquad
 \delta=c_0r^2\Lambda^{-4},\qquad
 J=(t-\delta,t).
\tag{AK.4}
\]

这里要求 \(0<\delta<t\)。若称 \(J\) 为成熟窗口，另要求
\(t-\delta\geq Cr^2\)；这一要求本身不会用于下面的频率估计。
由 \(\chi=1\) 于 \(B_r\)，AB 的终端局部能量满足

\[
 H_\chi(t)=\frac13\int\chi|u(t)|^3
 \geq \frac{\Lambda^3}{3}.
\tag{AK.5}
\]

## 2. 低频压力必须作为完整配对处理

压力方程
\(-\Delta p=\partial_i\partial_j(u_i u_j)\) 给出，对 \(k\neq0\)，

\[
 \widehat p(k)
 =-\frac{k_i k_j}{|k|^2}\widehat{u_i u_j}(k).
\tag{AK.6}
\]

采用归一化 Fourier 系数时，
\(\lvert\widehat{u_i u_j}(k)\rvert\leq C\|u\|_2^2\leq CM^2\)。
因此格点计数 \(\sum_{0<|k|\leq2K}|k|\leq CK^4\) 给出

\[
 \|\nabla p_{\leq K}(\sigma)\|_\infty
 \leq CM^2K^4.
\tag{AK.7}
\]

为保留 gauge 抵消，这里不把 AB.2 中的两个压力项分别粗估。
对每个固定时间，它们的完整配对是

\[
 \begin{aligned}
 {\cal K}_\chi(p_{\leq K})
 &:=\int_{\mathbb T^3}p_{\leq K}
       \operatorname{div}\!\bigl(\chi |u|u\bigr)\,dx\\
 &=-\int_{\mathbb T^3}\chi |u|u\cdot
       \nabla p_{\leq K}\,dx .
 \end{aligned}
\tag{AK.8}
\]

映射 \(z\mapsto |z|z\) 是 \(C^1\)，所以零速度处没有额外边界项。
任意时间 gauge \(c(\sigma)\) 与第一行的全散度配对为零。
由 AK.7 和 \(\int\chi|u|^2\leq M^2\)，

\[
 |{\cal K}_\chi(p_{\leq K})(\sigma)|
 \leq CM^4K^4.
\tag{AK.9}
\]

于是，对任意可测 \(J'\subset J\) 及 \(\vartheta\in L^1(J')\)，

\[
 \left|\int_{J'}\vartheta(\sigma)
             {\cal K}_\chi(p_{\leq K})(\sigma)\,d\sigma\right|
 \leq CM^4K^4\|\vartheta\|_{L^1(J')}.
\tag{AK.10}
\]

特别地，若 \(|\vartheta|\leq1\)，由 AK.4--AK.5，

\[
 \frac{\left|\int_{J'}\vartheta
                 {\cal K}_\chi(p_{\leq K})\right|}
      {H_\chi(t)}
 \leq Cc_0M^4r^2K^4\Lambda^{-7}.
\tag{AK.11}
\]

因此固定 \(M,r,c_0\) 时，低频完整压力功是终端能量的相对小量，只要

\[
 K=o\!\left(c_0^{-1/4}M^{-1}r^{-1/2}\Lambda^{7/4}\right).
\tag{AK.12}
\]

若另一个论证使用归一化时间权重，不能把其
\(\|\vartheta\|_{L^1}\) 免费替换成 \(\delta\)；应使用 AK.10
保留真实权重。本节也没有把 AK.8 拆成内部项与
\(\nabla\chi\) 壳项。

## 3. 高频速度尾的能量时间分布

令

\[
 g(\sigma)=\|\nabla u(\sigma)\|_2,\qquad
 A_J=\int_J g(\sigma)^2\,d\sigma .
\tag{AK.13}
\]

由于 \(1-\varphi(k/K)=0\) 于 \(|k|\leq K\)，Plancherel 给出

\[
 \|v_{>K}(\sigma)\|_2\leq CK^{-1}g(\sigma),
 \qquad
 \|\nabla v_{>K}(\sigma)\|_2\leq Cg(\sigma).
\tag{AK.14}
\]

\(v_{>K}\) 的空间均值为零。周期 Sobolev 因而给出
\(\|v_{>K}\|_6\leq C\|\nabla v_{>K}\|_2\leq Cg\)；
即使使用非齐次版本，AK.14 和 \(K\geq1\) 也给出同一结论。
插值后逐时有

\[
 \|v_{>K}\|_3^2
 \leq \|v_{>K}\|_2\|v_{>K}\|_6
 \leq CK^{-1}g^2.
\tag{AK.15}
\]

故

\[
 \int_J\|v_{>K}(\sigma)\|_3^2\,d\sigma
 \leq CK^{-1}A_J.
\tag{AK.16}
\]

对固定 \(\eta>0\)，Chebyshev 不等式和 AK.4 给出

\[
 \frac{\left|\{\sigma\in J:
        \|v_{>K}(\sigma)\|_3>\eta\}\right|}{\delta}
 \leq \frac{CA_J}{\eta^2K\delta}
 =\frac{CA_J\Lambda^4}{\eta^2c_0r^2K}.
\tag{AK.17}
\]

AK.16 是只使用一阶能量导数时自然得到的 \(K^{-1}\) 界。
一个不使用频率增益的比较估计是

\[
 \int_J\|v_{>K}\|_3^2
 \leq CM\delta^{1/2}A_J^{1/2};
\tag{AK.18}
\]

它来自
\(\|v_{>K}\|_3^2\leq CMg\) 和时间 Cauchy--Schwarz。
由 AK.18 令坏时间比例趋零需要
\(A_J=o(\delta)=o(\Lambda^{-4})\)，并没有改善下面由 AK.17
得到的可调频率条件。本稿只比较这两条已写出的估计，
不声称它们是仅用 \(M\) 与 \(A_J\) 时的最优界。

## 4. 两个充分估计的尺度走廊

先固定 \(\eta,r,M,c_0\)，并考虑 \(\Lambda\to\infty\)。
若

\[
 K\asymp\Lambda^\alpha,\qquad 0\leq\alpha<\frac74,
\tag{AK.19}
\]

则 AK.11 的低频压力相对成本为
\(O(\Lambda^{4\alpha-7})=o(1)\)。另一方面，AK.17 所给的
坏时间比例上界趋零的一个充分条件是

\[
 A_J=o\!\left(\Lambda^{\alpha-4}\right).
\tag{AK.20}
\]

这只是**该充分估计**所需的速率，不是实际坏时间比例趋零的必要条件。
全局能量只给 \(g^2\in L^1(0,T_*)\)。当 \(|J|=\delta\to0\) 时，
积分的绝对连续性给 \(A_J=o(1)\)，却不给 AK.20 所需的多项式速率。

不预先固定幂次时，要让 AK.11 与 AK.17 的两个右侧同时趋零，需要在
渐近意义下选择

\[
 \frac{A_J\Lambda^4}{\eta^2c_0r^2}\ll K
 \ll c_0^{-1/4}M^{-1}r^{-1/2}\Lambda^{7/4}.
\tag{AK.21}
\]

对这一特定的两估计法，存在这样的频率走廊的充分兼容条件是

\[
 A_J=o\!\left(
   \eta^2c_0^{3/4}M^{-1}r^{3/2}\Lambda^{-9/4}
 \right).
\tag{AK.22}
\]

在非退化情形 \(M>0\) 且 \(\Lambda\to\infty\) 下，AK.22
允许在两端之间取中间频率，并最终满足 \(K\geq1\)；
若应用还要求 \(K\gtrsim r^{-1}\)，也必须把这一固定下界与
AK.21 一并检查。AK.22 不是 Navier--Stokes 动力学的必要条件，
更不是能量等式已经提供的结论。

## 5. 这一尾界没有支付高频压力

定义

\[
 \Gamma_{K,\eta}(\sigma)
 =\mathbf 1_{\{\|v_{>K}(\sigma)\|_3>\eta\}} .
\tag{AK.23}
\]

AK.17 只把 \(\Gamma_{K,\eta}\) 当作全环面高频速度尾的时间分布诊断。
即使某时刻 \(\Gamma_{K,\eta}=0\)，也不能据此吸收局部高频压力功。
原因至少有三点：

1. Fourier 截断不与乘法截止 \(\chi\) 交换，局部化会产生交换子；
2. \(p_{>K}=P_{>K}R_iR_j(u_i u_j)\) 是二次频率输出，包含低--低
   接近截断处、低--高及高--高相互作用，并不是单个
   \(v_{>K}\) 的函数；
3. AB.2 还保留输运、黏性截止及其他壳项，单独控制压力也不足以闭合。

真正尚未支付的高频完整配对仍是

\[
 -\int_J\int_{\mathbb T^3}
       \chi |u|u\cdot\nabla p_{>K}\,dx\,d\sigma .
\tag{AK.24}
\]

成熟条件 \(t-\delta\geq Cr^2\) 只说明窗口远离初始时刻；
它不从 \(M,r\) 自动产生趋近 \(T_*\) 时统一的高阶范数或压力频率尾
速率。在固定的严格前奇点紧时间区间上，光滑性当然使频率尾趋零，
但常数依赖该解及区间与 \(T_*\) 的距离，不能代入首次奇点极限。
一般 Navier--Stokes 解是否还有可用的额外结构仍是 OPEN；本稿没有
证明高频闭合不可能。

一个准确的下一候选是保留空间截止交换子的带符号 dyadic 完整配对。
沿用同一平滑截止，明确令
\[
 \Delta_j^K=P_{\le 2^{j+1}K}-P_{\le 2^jK},\qquad j=0,1,\ldots .
\]
在每个严格前奇点的光滑紧时间区间，望远镜求和给
\(\sum_{j\ge0}\Delta_j^Kp=p_{>K}\)，故待控制的量可写成

\[
 -\sum_{j\ge0}
 \int_J\int_{\mathbb T^3}
   \chi |u|u\cdot\nabla\Delta_j^Kp\,dx\,d\sigma .
\tag{AK.25}
\]

下一步检验它能否由实际窗口量 \(A_J\) 与局部能量共同支付。
AK.25 的重写在上述光滑区间成立；尚未证明的是趋近 \(T_*\) 时
所需的统一定量支付，不能把这一目标当作免费假设。
可以检验逐块绝对值和作为更强的充分条件，但它会丢失不同频带的
符号抵消；本稿不把这种三角估计当作必须成立的条件。

## 6. 当前边界

AK.1--AK.12 给出低频压力完整配对的有界支付；
AK.13--AK.22 给出同一截断下的能量尾诊断及该方法所需的明确速率；
AK.23--AK.25 记录它们不能自动接到高频局部压力的原因。
成熟持留、首次奇点排除、缩球移动路径和合同 G 均仍 OPEN。
本稿没有仿真、科学图或数值证书，不是冻结稿，也不进入发布流程。
