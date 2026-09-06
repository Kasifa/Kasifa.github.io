# 周期自适应耗散波数的能量引理

2026-09-06。**INTERNAL / WORKING / NOT FROZEN / G OPEN / NOT CLAY。**

本稿把 Cheskidov--Shvydkoy 的耗散波数思想在当前
\(\mathbb T^3\) 规范下重新证明，只建立能量层面的周期接口。
不移植其 \(\mathbb R^3\) 正则性定理，不把已知思想称为新颖结果，
也不假定自适应波数已经支付 AK 的局部高频压力。
来源是 [作者原稿，定义 (5)--(6) 与 Lemma 4.1](https://arxiv.org/pdf/1102.1944)。
本轮定向核对这些定义和证明接口，不重新审查整篇正则性证明。

## 1. 周期 Littlewood--Paley 规范

取 \(\mathbb T^3=(-\pi,\pi]^3\)，黏性 \(\nu>0\)。
空间 \(L^p\) 范数使用非归一化积分。沿用 AK.1 的实偶光滑
\(\varphi\) 与 AK.2 的乘子，明确固定非齐次 dyadic 分解

\[
 u=u_{-1}+\sum_{q\geq0}u_q,\qquad
 u_{-1}=P_{\le1}u,\quad
 u_q=(P_{\le2^{q+1}}-P_{\le2^q})u,\quad
 \lambda_q=2^q\quad(q\geq0),
\tag{AL.1}
\]

其中 \(u_q\) 的 Fourier 支撑位于
\(\{\lambda_q\leq |k|\leq4\lambda_q\}\)，乘子绝对值不超过 1。
第一行的分解在 \(L^2\) 中由望远镜求和得到。
所有常数只依赖这一固定分解和环面规范。对 \(q\geq0\)，有

\[
 \|u_q\|_\infty\leq C_B\lambda_q^{3/2}\|u_q\|_2,
 \qquad
 \lambda_q^2\|u_q\|_2^2\leq C_{LP}\|\nabla u\|_2^2.
\tag{AL.2}
\]

第二式直接来自 multiplier 支撑远离零频，而不是 Poincaré
对整个 \(u\) 的应用。均值和最低频块留在 \(u_{-1}\)；
其中均值不能由 \(\|\nabla u\|_2\) 支付。
下面的最小化范围从 \(q=0\) 起，因此即使均值为零也保留波数基线。

## 2. 带阈值的自适应波数

固定无量纲阈值 \(a>0\)。对每个 \(q\in\mathbb N_0\) 定义可接受事件

\[
 {\cal E}_q
 :=\bigcap_{p>q}
 \left\{\,t:\lambda_p^{-1}\|u_p(t)\|_\infty<a\nu\,\right\}.
\tag{AL.3}
\]

若集合 \(\{q\in\mathbb N_0:t\in{\cal E}_q\}\) 非空，令

\[
 Q_{a,\nu}(t)
 =\min\{q\in\mathbb N_0:t\in{\cal E}_q\},\qquad
 \mathfrak d_{a,\nu}(t)=\lambda_{Q_{a,\nu}(t)}.
\tag{AL.4}
\]

若该集合为空，暂令 \(\mathfrak d_{a,\nu}(t)=\infty\)。
若 \(u(t)\in H^1\)，由 AL.2，

\[
 \lambda_p^{-1}\|u_p(t)\|_\infty
 \leq C_B\lambda_p^{1/2}\|u_p(t)\|_2
 =C_B\lambda_p^{-1/2}
       \bigl(\lambda_p\|u_p(t)\|_2\bigr)
 \longrightarrow0.
\tag{AL.5}
\]

因此 AL.4 对每个 \(H^1\) 时间都有限。能量类解属于
\(L^2_tH^1_x\)，所以至多在一个零测集上取到 \(\infty\)；
以下点态陈述均理解为几乎处处。对当前首次奇点前的光滑解，
它在每个 \(t<T_*\) 都有限。

可测性也不需要额外选择。能量类代表 \(t\mapsto u(t)\) 在
\(L^2\) 中强可测；每个 \(\Delta_q\) 在周期域只有有限个
Fourier 模式，故 \(t\mapsto\|u_q(t)\|_\infty\) 可测。
于是 \({\cal E}_q\) 是可数个可测集的交。又因
\({\cal E}_q\subset{\cal E}_{q+1}\)，

\[
 \{\mathfrak d_{a,\nu}\leq\lambda_q\}={\cal E}_q
\tag{AL.6}
\]

按上述扩展值约定恒成立，故扩展值函数
\(\mathfrak d_{a,\nu}\) 可测。

## 3. 最小性触发与周期能量引理

若 \(Q=Q_{a,\nu}(t)\geq1\)，则 \({\cal E}_Q\) 成立而
\({\cal E}_{Q-1}\) 不成立。因此存在 \(p>Q-1\) 使阈值失败。
另一方面，\({\cal E}_Q\) 已保证所有 \(p>Q\) 满足阈值，
故失败的频块只能是 \(p=Q\)。于是

\[
 \|u_Q(t)\|_\infty\geq a\nu\lambda_Q.
\tag{AL.7}
\]

把 AL.7 平方后使用 AL.2，得到

\[
 \begin{aligned}
 a^2\nu^2\mathfrak d_{a,\nu}(t)
 &\leq \mathfrak d_{a,\nu}(t)^{-1}
             \|u_Q(t)\|_\infty^2\\
 &\leq C_B^2\mathfrak d_{a,\nu}(t)^2
             \|u_Q(t)\|_2^2\\
 &\leq C\|\nabla u(t)\|_2^2 .
 \end{aligned}
\tag{AL.8}
\]

这里 \(a^2\nu^2\) 来自对触发式平方；不能把它未经说明地写成
\(a\nu\)。若 \(Q=0\)，最小化范围内没有前驱指标可触发 AL.7，
但此时 \(\mathfrak d_{a,\nu}=\lambda_0=1\)。两支合并为

\[
 \boxed{\quad
 \mathfrak d_{a,\nu}(t)
 \leq 1+C\,a^{-2}\nu^{-2}\|\nabla u(t)\|_2^2
 \quad}
\tag{AL.9}
\]

对几乎每个能量时间成立。特别地，对任意可测时间集 \(I\)，

\[
 \int_I\mathfrak d_{a,\nu}(\sigma)\,d\sigma
 \leq |I|+C\,a^{-2}\nu^{-2}
       \int_I\|\nabla u(\sigma)\|_2^2\,d\sigma .
\tag{AL.10}
\]

低频常数 \(1\) 是必要的。例如空间常速度的梯度为零，而按 AL.4
仍有 \(\mathfrak d_{a,\nu}=1\)。在边长为 \(2\pi L\) 的环面上，
同一证明把基线 \(1\) 换成最低波数 \(L^{-1}\)，并相应缩放
\(\lambda_q=2^q/L\)。

若 \(u\) 是无外力周期 Leray--Hopf 解，则

\[
 \nu\int_0^T\|\nabla u\|_2^2
 \leq \frac12\|u(0)\|_2^2,
\]

所以 AL.10 进一步给

\[
 \int_0^T\mathfrak d_{a,\nu}
 \leq T+C\,a^{-2}\nu^{-3}\|u(0)\|_2^2.
\tag{AL.11}
\]

AL.9--AL.11 是本稿的全部能量引理。它们没有推出
\(\mathfrak d_{a,\nu}\in L^{5/2}_t\)，也没有调用任何
\(\mathbb R^3\) 低模正则性结论。

## 4. 窗口 Markov 估计

令 \(J\) 是解定义域内满足 \(0<|J|<\infty\) 的时间区间，并记

\[
 A_J=\int_J\|\nabla u(\sigma)\|_2^2\,d\sigma .
\tag{AL.12}
\]

对 \(K\geq1\) 定义自适应坏时间集

\[
 {\cal B}_{K}(J)
 =\{\sigma\in J:\mathfrak d_{a,\nu}(\sigma)>K\}.
\tag{AL.13}
\]

由可测性、Markov 不等式和 AL.10，

\[
 \frac{|{\cal B}_{K}(J)|}{|J|}
 \leq \frac1K+
 \frac{C\,a^{-2}\nu^{-2}A_J}{K|J|}.
\tag{AL.14}
\]

在其补集上，\(\mathfrak d_{a,\nu}\leq K\)。若
\(\lambda_p>K\)，则 \(p>Q_{a,\nu}\)，所以定义本身给出

\[
 \lambda_p^{-1}\|u_p(\sigma)\|_\infty<a\nu .
\tag{AL.15}
\]

这是真正可供后续 paraproduct 检验的点态高频信息。
不过，只有当 \(a\) 被另行选得足够小，并且所有空间截止交换子
得到支付时，AL.15 才可能转化为黏性吸收；本稿没有证明这一步。

## 5. 代入 AK 成熟窗口

为避免符号冲突，记 AK 的终端局部 \(L^3\) 幅值为

\[
 \Lambda_A=L_r(t),\qquad
 \delta=c_0r^2\Lambda_A^{-4},\qquad
 J=(t-\delta,t).
\tag{AL.16}
\]

\(\Lambda_A\) 是振幅范数，不是波数
\(\mathfrak d_{a,\nu}\)。AL.14 变成

\[
 \frac{|{\cal B}_{K}(J)|}{\delta}
 \leq \frac1K+
 \frac{C\,a^{-2}\nu^{-2}A_J\Lambda_A^4}
      {c_0r^2K}.
\tag{AL.17}
\]

可把 \(K\) 取为 dyadic 波数；用最近的 dyadic 数替换任意 \(K\)
只改变固定常数，并与 AK 的平滑 Fourier 截断处于同一尺度。
若

\[
 K\asymp\Lambda_A^\alpha,\qquad
 0<\alpha<\frac74,
\tag{AL.18}
\]

则第一项趋零，AK.11 的低频压力相对成本
\(O(\Lambda_A^{4\alpha-7})\) 也趋零。由 AL.17 推出坏时间比例
趋零的一个充分条件仍是

\[
 A_J=o\!\left(
   a^2\nu^2c_0r^2\Lambda_A^{\alpha-4}
 \right).
\tag{AL.19}
\]

固定 \(a,\nu,c_0,r\) 时，关键指数与 AK.20 完全相同。
不预先固定 \(\alpha\) 时，这一 Markov 支付与 AK.12 的低频压力
上界要求共同留下走廊

\[
 1+\frac{a^{-2}\nu^{-2}A_J\Lambda_A^4}{c_0r^2}
 \ll K
 \ll c_0^{-1/4}M^{-1}r^{-1/2}\Lambda_A^{7/4}.
\tag{AL.20}
\]

对这两条充分估计，走廊相容的一个明确条件是

\[
 A_J=o\!\left(
 a^2\nu^2c_0^{3/4}M^{-1}r^{3/2}
 \Lambda_A^{-9/4}
 \right).
\tag{AL.21}
\]

因此自适应波数没有消除额外条件：能量绝对连续性在
\(\delta\to0\) 时只给 \(A_J=o(1)\)，不提供 AL.19 或 AL.21
所需的多项式衰减率。成熟条件
\(t-\delta\geq Cr^2\) 同样不给这一速率。

## 6. 严格边界

AL.9 是已知耗散波数思想的周期能量层复证；AL.14 是其直接
窗口 Markov 推论。它们说明在定义的好时间集上，某个自适应阈值以上
的单个速度频块满足 AL.15；好时间是否占大部分仍需上述额外速率。

它们尚未控制

\[
 -\int_J\int_{\mathbb T^3}
 \chi |u|u\cdot\nabla p_{>K}\,dx\,d\sigma,
\tag{AL.22}
\]

因为压力是 \(u\otimes u\) 的二次频率输出，且 Fourier 投影不与
\(\chi\) 交换。它们也未支付 AB 的输运、黏性截止和其他壳项。
不能把 AL.19 改名为新的“低模正则性条件”，不能从
\(\mathfrak d_{a,\nu}\in L^1_t\) 推出 \(L^{5/2}_t\)，也不能
把周期能量引理当作 \(\mathbb R^3\) 正则性定理的移植。

一般 Navier--Stokes 动力学是否能为 \(A_J\) 提供更强的局部速率
仍为 OPEN。成熟持留、首次奇点排除、移动缩球路径和合同 G
均未完成。本稿仅作内部源文件记录，不作为新 release 移交，
不含仿真或数值证书。
