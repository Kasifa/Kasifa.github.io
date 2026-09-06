# 算子预算强度审计：它已经包含原解的正则延拓

2026-09-06。**INTERNAL LOGICAL AUDIT / CONDITIONAL / NON-AUTHOR REVIEW PASS / G OPEN / NOT CLAY。**

我先检查 BQ 的出口究竟有多强，再决定是否求它的上界。
结论分两层：共同伴随给具体后继解一个连续时间的障碍；
而取遍所有初态的延迟二阶算子预算，已经与固定周期原解在
指定终点的光滑延拓等价。这个观察不支付该预算，也不宣称新颖性。

## 1. 共同伴随给所有固定起点一个具体障碍

先假设 BP 的正原子条件及已构造的同一个 \(A\)。
对任意固定 \(t_b\le s<T\)，定义
\[
 \alpha_s=\|A(s)\|_2^2>0,\qquad F_s(t)=U(t,s)A(s),\quad t\ge s.
 \tag{BR.1}
\]
BP 的 \(\langle u(s),A(s)\rangle=\sqrt m\) 保证 \(\alpha_s>0\)，
并有 \(\alpha_s\uparrow1\) 当 \(s\uparrow T\)。不限制 \(s\) 是离散节点。

前向与伴随的对偶给
\[
 \langle F_s(t),A(t)\rangle=\alpha_s,\quad
 \|F_s(t)\|_2^2\le\alpha_s,\quad
 \|F_s(t)-A(t)\|_2^2\le1-\alpha_s\quad(s\le t<T).
 \tag{BR.2}
\]
最后式是精确平方展开、\(\|A(t)\|_2^2\le1\) 的结果。
这是对特定 \(F_s,A\) 的连续时间比较，不把 BP 原来的
离散 \(q_j\) 三角结论改称任意连续时间传播结论。

两条能量等式还给
\[
 \|F_s(t)-A(t)\|_2^2
 =2\nu\int_s^t(\|\nabla A\|_2^2-\|\nabla F_s\|_2^2),\qquad
 \int_s^t\|\nabla F_s\|_2^2\le\int_s^t\|\nabla A\|_2^2 .
 \tag{BR.3}
\]
仅比较积分，不声称被积差逐点非负。这些上界仍是一阶能量上界。

若 \(F_s(t)\) 在 \(t\uparrow T\) 有强 \(L^2\) 极限 \(F_*\)，
BP 的 \(A(t)\rightharpoonup0\)、统一范数界会给
\[
 \langle F_s(t),A(t)\rangle
 =\langle F_s(t)-F_*,A(t)\rangle+\langle F_*,A(t)\rangle
 \longrightarrow0,
 \tag{BR.4}
\]
与 BR.2 的严格正数矛盾。因此每一个这样的固定后继解都无强终端迹。

若另假设某个 \(s<r<T\) 上
\(\int_r^T\|\Delta F_s\|_2^2<\infty\)，则对 \(r\le a<b<T\)，
BQ 的积分方程与同一 Hölder 估计给
\[
 \|F_s(b)-F_s(a)\|_2
 \le C\left(\int_a^b(\|\nabla u\|_2^2+E_*^2)\right)^{1/2}
       \left(\int_a^b\|\nabla F_s\|_2^2\right)^{1/4}
       \left(\int_a^b\|\Delta F_s\|_2^2\right)^{1/4}
       +\nu(b-a)^{1/2}
          \left(\int_a^b\|\Delta F_s\|_2^2\right)^{1/2}
 \longrightarrow0 .
 \tag{BR.5}
\]
由 \(L^2\) 完备性即有强终端迹，产生矛盾。所以
\[
 \int_r^T\|\Delta U(t,s)A(s)\|_2^2dt=+\infty
 \quad\text{每一对 }t_b\le s<r<T,\qquad
 \mathcal R_u(s,r)=+\infty\quad\text{每一对 }s<r.
 \tag{BR.6}
\]
最后用单位初态 \(A(s)/\sqrt{\alpha_s}\)。
这是独立的量词加强推导，不是直接篡改 Huang Corollary 2.6
原来针对充分晚离散根的陈述；没有证明原子条件可以实现。

## 2. 先把原解自己的初态代入算子预算

下面完全不需要原子或共同伴随，只保留固定光滑周期 NS 原解。
若某一对 \(t_b\le s<r<T\) 有 \(\mathcal R_u(s,r)<\infty\)，
且 \(u(s)\ne0\)，将 \(f=u(s)/\|u(s)\|_2\) 代入。
因为原解本身满足 \(u(t)=U(t,s)u(s)\)，
\[
 \int_r^T\|\Delta u(t)\|_2^2dt
 \le \|u(s)\|_2^2\,\mathcal R_u(s,r)<\infty .
 \tag{BR.7}
\]
若 \(u(s)=0\)，无外力光滑 NS 的前向唯一性使以后恒为零，
光滑延拓已是平凡情形，无需除以零。

周期 Fourier Cauchy--Schwarz、\(\sum_{k\in\mathbb Z^3}(1+|k|^2)^{-2}<\infty\)
给 \(\|v\|_\infty^2\le C(\|v\|_2^2+\|\Delta v\|_2^2)\)。
于是
\[
 \int_r^T\|u(t)\|_\infty^2dt
 \le C E_*^2(T-r)+C\int_r^T\|\Delta u(t)\|_2^2dt<\infty .
 \tag{BR.8}
\]
此处已得到非端点 Serrin 的 \(L^2_tL^\infty_x\) 条件，
不是由基本能量自动推出；关键额外输入正是 BR.7。

将原 NS 与 \(-\Delta u\) 配对并吸收一半黏性项，令
\(G(t)=\|\nabla u(t)\|_2^2\)，有
\[
 G'(t)+\nu\|\Delta u(t)\|_2^2
 \le\nu^{-1}\|u(t)\|_\infty^2 G(t),\qquad
 \sup_{r\le t<T}G(t)
 \le G(r)\exp\left(\nu^{-1}\int_r^T\|u\|_\infty^2dt\right)<\infty .
 \tag{BR.9}
\]
所以原解在整个晚期有统一非齐次 \(H^1\) 界。

## 3. 局部延拓接口及反向蕴含

这里使用已知周期 \(H^1\) 局部理论，不当作新结论。
Tao [1108.1165v4](https://arxiv.org/abs/1108.1165v4)
Theorem 5.1(ii)--(iv) 给依赖初态 \(H^1\) 范数的正寿命、唯一性与
光滑数据的光滑性，Corollary 5.2 给相应延拓判据。
本轮读取了实际定理与证明及其局部工具，范围见文献记录。

原文先归一化周期、黏性与均值。这里 \(\nu,\Omega\) 固定；
时间/速度归一化和空间缩放只改变常数。
原无外力周期解的均值 \(c\) 恒定，用
\(v(x,t)=u(x+ct,t)-c\) 得零均值的同型方程，且范数受原 \(H^1\) 界控制。
没有给原解擅自添加零均值假设。

因此 BR.9 使任意晚时刻 \(t_n\uparrow T\) 重新启动的局部解都有
同一个正寿命 \(\tau_0>0\)。取 \(T-t_n<\tau_0/2\)，
初态 \(u(t_n)\) 光滑；局部理论给光滑解越过 \(T\)，
并由唯一性在 \([t_n,T)\) 与原解一致。故
\[
 \mathcal R_u(s,r)<\infty\text{ 对某一对 }s<r
 \quad\Longrightarrow\quad
 u\text{ 在 }T\text{ 有光滑周期 NS 延拓}.
 \tag{BR.10}
\]
这里没有声称重新证明所有 Kato/Prodi/Serrin 原论文及局部理论的全部基础。

反过来，若 \(u\) 光滑延拓过 \(T\)，则每个固定 \([s,T]\) 上
\(\|u\|_\infty\) 有界。BQ.11 的正延迟平滑和 BQ.12--13 的
\(q=\infty,p=2\) 情形给
\[
 \mathcal R_u(s,r)<\infty
 \quad\text{对每一对 }t_b\le s<r<T .
 \tag{BR.11}
\]
常数可以依赖 \(s,r\)，不要求在 \(r-s\downarrow0\) 时一致。

综上，在本稿固定周期光滑终点前原解的设定中，
\[
 \boxed{
 \text{在 }T\text{ 光滑延拓}
 \ \Longleftrightarrow\
 \exists\,s<r<T:\mathcal R_u(s,r)<\infty
 \ \Longleftrightarrow\
 \forall\,s<r<T:\mathcal R_u(s,r)<\infty .}
 \tag{BR.12}
\]
这不是所有空间、外力及弱解设定的等价声明。
也不等于已证明以上任何一个条件对任意 NS 初值自动成立。

## 4. 对路线的实际影响

原子迫使 BQ 的二阶作用发散这一条件结构可以保留。
但若接下来试图直接证明“整个 \(\mathcal R_u\) 有限”来解决问题，
就已经在要求固定原解的光滑延拓；不能把它报告为更弱且已经接近支付的
能量预算。这是一次逻辑强度核查，不是否定所有算子方法，也不是新颖性声明。

BR.2--BR.6 则留下一个更有针对性的对象：正原子所生的非零共同伴随
\(A\)，具有弱零终端迹；相应固定 \(F_s\) 与 \(A\) 保持严格正配对。
下一项先核查这个带压力、由真实 NS 原解驱动的伴随是否已有适用的
终端唯一性结果，以及其确切条件能否由原解保证。
不得把标量被动扩散、任意给定漂移或有临界范数假设的定理直接移植。
这只规定下一项的有界问题，不承诺能排除该伴随或解决 Clay。
