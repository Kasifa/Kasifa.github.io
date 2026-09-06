# Euler 缩放预检：预算与非平凡性不能分开选择

2026-09-06。**INTERNAL / PROVED BOOKKEEPING / CONDITIONAL COMPARISON / NON-AUTHOR REVIEW PASS / G OPEN / NOT CLAY。**

本稿检查 Seregin 的 2026 年 Type II 预印本提出的缩放接口。
不调用该文的 Euler 紧性或刚性定理来证明以下计算，也不把其
局部 Type II 定义替换成上一节的速度 Type I 或 record 间隔。
我只问：固定周期初值的能量，能同时支付哪些预算并保留什么？

## 1. 同一原解与加权量

沿用 G 的任意光滑周期初值、黏性一、无外力和 suitable continuation。
把一个有限候选终点平移为 \((0,0)\)，选择固定内点坐标球及
\((-T_0,0)\)；以下 \(0<r<r_0\le1\) 均处在该坐标球和时间段内。
压力始终取原周期零均值代表，不使用截断后重命名的无外力方程。

记

\[
 M=\mathop{\rm ess\,sup}_{-T_0<t<0}\|u(t)\|_2<\infty,
 \quad G(r)=\int_{-r^2}^0\|\nabla u(t)\|_2^2dt,
 \quad P(r)=\int_{-r^2}^0\!\int_{\mathbb T^3}|p|^{3/2}.
\tag{BK.1}
\]

有限耗散和规范压力的局部时间可积性给 \(G(r),P(r)\to0\)。
这里压力可积也可由周期有限指数 Riesz 估计
\(\|p(t)\|_{3/2}\le C\|u(t)\|_3^2\) 和能量插值得到。
绝对连续性本身不给指定幂率。

对 \(f(r)=r^\beta\)、\(0<\beta\le1\)，令

\[
 \begin{aligned}
 A_f(r)&=\frac{f(r)^2}{r}\mathop{\rm ess\,sup}_{-r^2<t<0}
                  \int_{B_r}|u|^2,\\
 E_f(r)&=\frac{f(r)}r\int_{Q_r}|\nabla u|^2,\qquad
 D_f(r)=\frac{f(r)^2}{r^2}\int_{Q_r}|p|^{3/2},
 \quad Q_r=B_r\times(-r^2,0).
 \end{aligned}
\tag{BK.2}
\]

直接扩大积分区域，有

\[
 A_f(r)\le M^2r^{2\beta-1},\quad
 E_f(r)\le r^{\beta-1}G(r),\quad
 D_f(r)\le r^{2\beta-2}P(r).
\tag{BK.3}
\]

因此 \(\beta=1\) 时三项均自动有界且趋零；\(\beta\ge1/2\)
时 kinetic 项有界。但当 \(\beta<1\) 时，仅把 \(G,P\to0\)
代入后两式并未给出统一界。通过这些全域粗界支付它们的一种
充分办法是 \(G(r)=O(r^{1-\beta})\)、\(P(r)=O(r^{2-2\beta})\)。
这不是说局部 \(E_f,D_f\) 有界必须要求全域尾量有这些速率，
也不是证明真实 NS 不能给出更好的局部估计。

## 2. 精确缩放

在逐渐扩张的周期胞上定义

\[
 w_\lambda(y,\tau)=\lambda^{1+\beta}
 u(\lambda y,\lambda^{2+\beta}\tau),\qquad
 \pi_\lambda(y,\tau)=\lambda^{2+2\beta}
 p(\lambda y,\lambda^{2+\beta}\tau).
\tag{BK.4}
\]

直接换元得到完整方程

\[
 \partial_\tau w_\lambda+w_\lambda\cdot\nabla w_\lambda
 +\nabla\pi_\lambda=\lambda^\beta\Delta w_\lambda,
 \qquad\operatorname{div}w_\lambda=0.
\tag{BK.5}
\]

没有把它称为黏性仍为一的 NS 缩放；欲取 Euler 极限还须另证
足够紧性。对每个固定 \(a>0\)，\(\lambda\) 足够小时有

\[
 \mathop{\rm ess\,sup}_{-a^2<\tau<0}
 \int_{B_a}|w_\lambda|^2\le M^2\lambda^{2\beta-1},
\tag{BK.6}
\]

\[
 \begin{aligned}
 \int_{Q_a}|\nabla w_\lambda|^2
 &=\lambda^{\beta-1}\int_{-a^2\lambda^{2+\beta}}^0
                         \int_{B_{a\lambda}}|\nabla u|^2,\\
 \int_{Q_a}|\pi_\lambda|^{3/2}
 &=\lambda^{2\beta-2}\int_{-a^2\lambda^{2+\beta}}^0
                         \int_{B_{a\lambda}}|p|^{3/2}.
 \end{aligned}
\tag{BK.7}
\]

特别当 \(\beta=1\)，(BK.6) 趋零，(BK.7) 也由绝对连续性趋零。
所以 \(w_\lambda\to0\) 于每个固定柱体的
\(L^\infty_\tau L^2_y\cap L^2_\tau H^1_y\)。不需要 Euler
Liouville 定理便已知道这个缩放不保留非零极限。

## 3. 短窗非平凡性的直接检查

只检查原文允许的一个明确指标 \(s=l=3\)。此时
\(\kappa=l(3/s+2/l-1)=2\)，\(\eta=0\) 给
\(p(0)=q(0)=10/3>3\)。定义

\[
 \overline{\mathcal M}_2^{3,3}(u,r)
 =r^{-2}\int_{-r^{2+\beta}}^0\int_{B_r}|u|^3,
 \qquad g(r)=f(r)^{l-1}=r^{2\beta}.
\tag{BK.8}
\]

准确的非平凡性匹配是

\[
 g(r)\overline{\mathcal M}_2^{3,3}(u,r)
 =\int_{Q_1}|w_r|^3.
\tag{BK.9}
\]

原文的正下界必须约束这个缩短的时间窗，不能用整个 \(Q_r\)
中的积分大来替换。设
\(G_{\rm sh}(r)=\int_{-r^{2+\beta}}^0\|\nabla u(t)\|_2^2dt\to0\)。
周期非齐次 Gagliardo--Nirenberg 和时间 Hölder 给

\[
 \int_{Q_1}|w_r|^3
 \le CM^{3/2}r^{-3/2+9\beta/4}G_{\rm sh}(r)^{3/4}
       +CM^3r^{3\beta}.
\tag{BK.10}
\]

证明中使用
\(\|u(t)\|_3^3\le CM^{3/2}\|\nabla u(t)\|_2^{3/2}+CM^3\)，
长度为 \(r^{2+\beta}\) 的时间 Hölder 因子为
\(r^{(2+\beta)/4}\)，最后乘缩放 Jacobian 因子 \(r^{2\beta-2}\)。
因此仅能量已给 \(\beta\ge2/3\) 时 (BK.9) 趋零；端点
\(\beta=2/3\) 使用 \(G_{\rm sh}\to0\)，不是只使用有界性。

若额外有 \(\sup_{r<r_0}E_f(r)\le C_E\)，则对 \(a=1\)
在 (BK.7) 中只扩大时间窗，得到
\(\int_{Q_1}|\nabla w_r|^2\le E_f(r)\le C_E\)。
令 \(e_r=M^2r^{2\beta-1}\)，在固定球上使用非齐次局部插值：

\[
 \int_{Q_1}|w_r|^3\le C e_r^{3/4}(C_E+e_r)^{3/4}
 \longrightarrow0\qquad(\beta>1/2).
\tag{BK.11}
\]

这一步没有从局部 \(E_f\) 反推全域 \(G_{\rm sh}\) 的上界。
结论仅为：本项目有限总能量来源若同时满足该局部加权耗散界，
则所有 \(\beta>1/2\) 的这个短窗非平凡性都消失。可能保留非零
极限的 \(\beta\le1/2\) 区域仍需尚未支付的局部预算和非平凡性。

## 4. 原文附加条件不能漏掉

同一 \(s=l=3,\eta=0\) 下，原文 (3.3) 的比值为

\[
 \frac{f(\lambda)^{57/20}}
        {f(\lambda\sqrt{f(\lambda)})^2}
 =\lambda^{\beta(17/20-\beta)}.
\tag{BK.12}
\]

\(\beta=1\) 时该比值发散，因而它并非满足原文 Theorem 3.1
其余全部条件的实例；其预算有界与零极限是本稿直接计算。
\(\beta=1/2\) 时指数为 \(7/40\)，该条件通过，却仍未得到
局部耗散界、短窗非平凡性或一般 Euler 刚性。

原文用 \(g_0=\min\{\liminf A,\liminf E,\liminf C\}\) 的有限或
无穷定义局部 Type I/II；本节不把它与速度的
\(\sup\sqrt{-t}\|u(t)\|_\infty\)、BJ 的 \(D_j\) 等同。
一般局部 Type II 不蕴含任意选定 \(f\) 的短窗条件。

以上是适用边界和独立缩放计算，不是对原稿全部证明的接受、一般
Type II 排除、NS 奇点构造、新颖性声明或 Clay 结果。
本稿尚未形成新的研究发布包。下一项具体候选见阶段策略记录。
