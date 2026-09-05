# 真实物理时间的反向测试：下一回合工作稿

2026-09-05。由 f8534cf7 的 S/T 结果继续。
状态：**WORKING / 未独立审查 / 不构成新 release / G OPEN**。
本稿只在光滑时段先作推导，不把弱端点或尺度一致性视为已证。

## 1. 不再沿辅助滤波尺度扩散检验

固定原 phi 核产生的 b_R=S_Ru。对实际窗口 [s,T]，T-s<=64R^2，
考虑周期非负终端测试 psi_R(x)=psi((x-x_*)/R)，
其中 0<=psi<=1、psi=1 于 B_1、支撑于 B_2，R<pi/16。
令

\[
 \partial_t\chi+\Delta\chi+b_R\cdot\nabla\chi=0,\qquad
 \chi(T)=\psi_R.
\tag{A.1}
\]

反向时间 sigma=T-t 后，这是正向抛物方程，最大值原理给
0<=chi<=1；div b_R=0 给空间质量 int chi=int psi_R。
不同 R 的终端质量本来就不同，因此不受 T.2 那种沿尺度
保持同一个固定质量的矛盾约束。
这并不自动意味着 chi 与原移动球上的指示函数可互相比较。

对原 NS 局部能量等式，以 e=|u|^2/2 记，测试得到

\[
\begin{aligned}
 [\int\chi e]_s^T+\int_s^T\int\chi|\nabla u|^2
 =\int_s^T\int
 \left[e(u-b_R)\cdot\nabla\chi+(p-c(t))u\cdot\nabla\chi\right].
\end{aligned}
\tag{A.2}
\]

这里使用 (A.1) 消去 e(chi_t+Delta chi+b_R dot grad chi)；
没有消除残余速度、压力功或左端的初始加权能量。
压力 gauge 项为零由 div u=0 和周期分部积分给出。
不能在另乘时间 cutoff 后仍假装没有时间导数支付。

## 2. 一个初步的形状控制及其代价

为跟踪周期核的空间尾部，可先在 R^3 上取 psi_R 的单个紧支撑
提升、周期延拓系数 b_R，再将所得密度周期化。
在反向时间令 rho(sigma,x)=chi_lift(T-sigma,x)；
它满足 Fokker--Planck 方程

\[
 \partial_\sigma\rho=\Delta\rho+
 \nabla\cdot\bigl(b_R(T-\sigma)\rho\bigr),
\tag{A.3}
\]

即漂移为 -b_R。相应确定性中心 Y 满足
Y'=-b_R(T-sigma,Y)、Y(0)=x_*，故 Y(sigma)=X_R(T-sigma)。
令 M=int rho、Q(sigma)=int|x-Y(sigma)|^2rho，
L(sigma)=||grad b_R(T-sigma)||_infty。光滑有界系数和有限二阶矩下，
分部积分给

\[
 Q'=-2\int(x-Y)\cdot(b_R(T-\sigma,x)-b_R(T-\sigma,Y))\rho+6M
 \le2LQ+6M.
\tag{A.4}
\]

因此若 sigma<=64R^2，

\[
 \frac{Q(\sigma)}M
 \le e^{2\mathcal L_R}\left(\frac{Q(0)}M+6\sigma\right)
 \le C_\psi R^2e^{2\mathcal L_R},\qquad
 \mathcal L_R=\int_s^T\|\nabla b_R(t)\|_\infty\,dt.
\tag{A.5}
\]

这控制尾部二阶矩，不是球内点态下界或原 E_R 的支配估计。
由原平滑核的 L^2 界，

\[
 \mathcal L_R
 \le C_\varphi R^{-3/2}(T-s)^{1/2}
        \left(\int_s^T\|\nabla u\|_2^2dt\right)^{1/2}
 \le C_\varphi
        \left(R^{-1}\int_s^T\|\nabla u\|_2^2dt\right)^{1/2}.
\tag{A.6}
\]

所以这个直接估计再次遇到路径预检中的归一化耗散 D_J/R。
有限总耗散不保证该量有界或趋零；本稿不声称已经改进这一点。
也不能因为此粗上界无效，就断定真实核必然失去定位。

## 3. 下一回合须完成的检验

- 独立核对 A.1--A.6 的反向时间符号、提升/周期化与二阶矩论证；
- 给出允许使用的弱解时间正则性，不偷用原始解的强端点；
- 检查是否存在优于全局 Lipschitz 指数的局部漂移控制，
  并明确它是否真的由现有能量类推出；
- 精确估计 A.2 的压力和残余项，保留早期端点；
- 若仅重得既有临界量假设或 E.10 的三次支付，记录没有改善 G，
  不继续以换一种测试记号代替新的原方程输入。

无仿真、无图表、无新正则性结论。本稿不属于刚移交的冻结小节。
