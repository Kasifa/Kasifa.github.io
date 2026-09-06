# 旧压力支付的静态比较

2026-09-06。**INTERNAL / PENDING REVIEW / CONDITIONAL COMPARISON / G OPEN / NOT CLAY。**

BA、BB 把旧热成分从原压力测试中移走。我在这里检查这一步是否
必须依赖时间顺序。结果是，同一个有界背景估计也能支付一个更高
静态截止以下的速度参与压力。这是对方法来源的比较，不把热源余量
与静态高频尾认作同一个场，也不声称得到剩余压力的上界。

## 1. 不改变原坏时间测试

沿用 AQ 的同一实际解、固定环带和合法大范数序列，记

\[
 \begin{gathered}
 J=(t-\delta,t),\quad \delta=c_0r^2\Lambda^{-4},\quad
 K=\Lambda^{3/4},\quad h=P_{>K}u,\quad H_t\ge\Lambda^3/3,\\
 M=\sup\|u\|_2,\quad g(s)=\|\nabla u(s)\|_2,\quad
 A_J=\int_Jg(s)^2\,ds\to0,\quad L(s)=\|u(s)\|_3.
 \end{gathered}
\tag{BE.1}
\]

原 \(s_J\)、坏集 \(B_K\)、\(\mu_J=w_J\mathbf1_{B_K}\) 及 \([s_J,t]\) 积分保持不变。
时间端点按零测度处理，不将含 \(t\) 的闭区间写成 \(J\) 的子集。
固定平滑低通 \(S_Q\) 的符号为 \(\varphi(k/Q)\)，满足 \(0\le\varphi\le1\)、
在单位球上为一、在半径二以外为零。平滑高通不是幂等投影。

令 \(p(v)=T_{ij}(v_i v_j)\)、\(\Pi(v,w)=T_{ij}(v_i w_j+w_i v_j)\)，
所有压力取零均值。\(T_{ij}=\partial_i\partial_j(-\Delta)^{-1}\)。
对任意实际选定的光滑背景 \(f\) 和 \(z=h-f\)，代数恒等式给

\[
 p(h)=p(z)+p_{\rm bg},\qquad
 p_{\rm bg}=\Pi(f,h)-p(f).
\tag{BE.2}
\]

只讨论实值无散零均值的 \(f,h,z\)；这足以覆盖下列两个应用。
恒等式保留全部压力输出，高高产生的低输出也没有删除。

## 2. 有界背景的通用支付

设在 \(J\) 上有有限的统一界

\[
 B=\sup_J\|f\|_\infty,\qquad
 \Gamma=\sup_J\|\nabla p(f)\|_\infty.
\tag{BE.3}
\]

高通在有限 \(L^3\) 上一致有界，所以 \(\|h\|_3\le C_\varphi L\)。双 Riesz 只在
有限 \(L^3\) 上使用，给

\[
 \|\Pi(f,h)\|_3\le C B L.
\tag{BE.4}
\]

原测试 \(g_\chi=\operatorname{div}(\chi|u|u)\) 及原 \(D_\chi\) 保留。由 BA.8–BA.9 的
加权 Hölder 和零集正则化，主项的 \(L^{3/2}\) 范数不超过
\(L^{1/2}D_\chi^{1/2}\)，截止项不超过 \(C_\chi L^2\)。因此对任意预先
固定的 \(0<\epsilon<3/4\)，

\[
 |{\cal K}_\chi(\Pi(f,h))|
 \le\epsilon D_\chi+C_{\epsilon,\chi}B^2L^3+C_\chi B L^3.
\tag{BE.5}
\]

纯背景项不作 Riesz 的 \(L^\infty\) 估计，而是直接保留压力梯度：

\[
 |{\cal K}_\chi(p(f))|
 =\left|\int\chi|u|u\cdot\nabla p(f)\right|
 \le M^2\Gamma.
\tag{BE.6}
\]

所以令 \(I_3=\int_JL^3\,ds\)，由原 \(0\le\mu_J\le1\) 得

\[
 \int_{s_J}^t\mu_J{\cal K}_\chi(p_{\rm bg})\,ds
 \le\epsilon\int_{s_J}^t\mu_J D_\chi\,ds
 +C_{\epsilon,\chi}(B^2+B)I_3+M^2\Gamma\delta.
\tag{BE.7}
\]

这是单侧上界，且 \(\epsilon\) 的耗散份额只付一次。一个充分支付条件是

\[
 \frac{(B^2+B)I_3+M^2\Gamma\delta}{H_t}\longrightarrow0.
\tag{BE.8}
\]

BE.2–BE.8 没有使用 \(f\) 的时间演化方程。它们使用原压力二次式、
原测试和实际速度的能量；不是仅凭抽象能量消去即可对任意修改方程
无条件迁移的结论。

## 3. 一个完全静态的背景

给定 \(N\ge2K\)，定义

\[
 n=S_Nh,\qquad z=(I-S_N)h.
\tag{BE.9}
\]

因为 \(1-\varphi(k/N)\) 非零时 \(|k|>N\ge2K\)，此处 \(\varphi(k/K)=0\)，
故精确有

\[
 z=P_{>N}u,\qquad n=h-P_{>N}u.
\tag{BE.10}
\]

这不是把 \(S_N\) 当成幂等投影；它来自两种不同尺度的符号支持。
\(n\) 的符号为 \(\varphi(k/N)(1-\varphi(k/K))\)，介于零和一之间且支持在
\(|k|\le2N\)，故 \(\|n\|_2\le M\)。

采用 \(V=(2\pi)^3\)、\(\widehat f(k)=V^{-1}\int f(x)e^{-ik\cdot x}\,dx\)，格点
Cauchy–Schwarz 分别给

\[
 \sum_k|\widehat n(k)|\le CM N^{3/2},\qquad
 \sum_k|k|\,|\widehat n(k)|\le CM N^{5/2}.
\tag{BE.11}
\]

压力 Fourier 乘子的模有统一界，且 \(|\xi+\eta|\le|\xi|+|\eta|\)。
卷积绝对和于是给

\[
 \|n\|_\infty\le CMN^{3/2},\qquad
 \|\nabla p(n)\|_\infty
 \le C\left(\sum|\widehat n|\right)
        \left(\sum|k|\,|\widehat n|\right)
 \le CM^2N^4.
\tag{BE.12}
\]

频率零模取零，不使用未截断 Riesz 变换的 \(L^\infty\) 有界性。
把 \(f=n\) 代入 BE.7；BB.6 的能量插值给
\(I_3\le C(M^{3/2}\delta^{1/4}A_J^{3/4}+M^3\delta)\)。
所以所有非耗散余项之和 \(E_N\) 满足

\[
 \frac{E_N}{H_t}
 \le C_{\epsilon,\chi,M,r,c_0}
 \left[
 N^3\Lambda^{-4}A_J^{3/4}+N^3\Lambda^{-7}
 +N^{3/2}\Lambda^{-4}A_J^{3/4}+N^{3/2}\Lambda^{-7}
 +N^4\Lambda^{-7}\right].
\tag{BE.13}
\]

取静态截止

\[
 N=\Lambda^{4/3}.
\tag{BE.14}
\]

沿固定数据的合法序列，最终 \(N\ge2K\)。BE.13 的五项变成

\[
 A_J^{3/4},\quad\Lambda^{-3},\quad
 \Lambda^{-2}A_J^{3/4},\quad\Lambda^{-5},\quad\Lambda^{-5/3},
\tag{BE.15}
\]

均趋零。\(N\) 可以取固定倍数或相邻 dyadic 尺度，只改变固定常数。
这一充分选择不声称是最大允许频率或必要门槛。

## 4. 必要下界和时间比较

由 \(p(h)=p(P_{>N}u)+p_{\rm bg}\) 以及 BE.7、BE.15，从 AQ.8 得

\[
 \liminf_{\Lambda\to\infty}\frac1{H_t}\int_{s_J}^t\mu_J(s)
 \left[{\cal K}_\chi(p(P_{>N}u))(s)
       -\left(\frac34-\epsilon\right)D_\chi(s)\right]ds\ge1.
\tag{BE.16}
\]

不等号方向与 BA.16 相同。仍条件于同一合法序列存在。坏集是原
\(B_K\)，不是以 \(N\) 重定义的集合；也没有把 \(p(P_{>N}u)\) 偷换成 \(P_{>N}p\)。
与 BB 的必要条件作比较时，二者分别从 AQ 消耗一份 \(\epsilon\)，
不把两次吸收在同一预算中重复使用。

另一方面，BB 的热背景 \(f=b\) 在真实滞后 \(\tau\) 后满足

\[
 B\le CM\tau^{-3/4},\qquad
 \Gamma\le CM^2\tau^{-2}.
\tag{BE.17}
\]

代入 \(\tau=N^{-2}\)，这些正好是 BE.12 的 \(N^{3/2},N^4\) 量级。
所以 BB.23 与 BE.15 的余项账本相同，其旧压力支付可由通用
有界背景机制解释。这一比较没有判定 \(R=P_{>N}u\)，也没有相互比较
它们的带符号自压力功。热历史定位与静态高输入定位是不同必要条件。

## 5. 路线判断的边界

本稿确实把一个静态高输入压力必要条件推到 \(N=\Lambda^{4/3}\)，
但没有给这个压力以能量可支付的上界，也没有重建新的好时间吸收
定理。固定球之外的移动缩球量词和 G 仍 OPEN。

因此，继续改变滞后或静态截止指数，不足以作为动态研究收益。
下一步若要说明近期非线性源有额外控制，必须实际使用源的时间结构
来减少未付成本；不能把旧背景被支付这件事再次算成该控制。
基本热分解与有限指数估计不声称新颖；这也不是任何带符号方法的
不可能性定理。无仿真、科学图、DGX、新读者 PDF、提交或发布动作。
