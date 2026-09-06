# 压力对速度模长投影的残差：一个固定能量瞬时反检查

2026-09-06。**PROVED LOCALLY / INTERNAL ACTUAL-FILE AUDIT PASS / G OPEN / NOT CLAY。**

本稿只检验一条可能用于全环面 \(L^3\) 压力功的瞬时范数预算。
它不估计同一条 Navier--Stokes 轨道上的时间积分，也不改变原合同 G。

## 1. 要检验的投影残差

空间为 \(\mathbb T^3=(-\pi,\pi]^3\)，积分不作体积归一化。
对一个光滑、周期、零均值、无散场 \(u\)，令

\[
 q=|u|,\qquad H(u)=\frac13\int_{\mathbb T^3}q^3,
 \qquad -\Delta p=\partial_i\partial_j(u_i u_j),
 \qquad \int_{\mathbb T^3}p=0 .
\tag{AH.1}
\]

在带权空间 \(L^2(q\,dx)\) 中，考虑压力到只依赖 \(q\) 的函数的距离

\[
 {\mathscr R}^2(u)
 :=\inf_{\Phi}
   \int_{\mathbb T^3}q(x)\,|p(x)-\Phi(q(x))|^2\,dx .
\tag{AH.2}
\]

这里下确界取遍使积分有意义的 Borel 函数
\(\Phi:[0,\infty)\to\mathbb R\)。改变压力的时间常数只会相应平移
\(\Phi\)，所以 \({\mathscr R}\) 与压力 gauge 无关。

下面证明：给定任意 \(E_0>0\)，存在一族这样的场 \(u_\epsilon\)，使

\[
 \|u_\epsilon\|_2^2=E_0,\qquad
 \frac{{\mathscr R}^2(u_\epsilon)/H(u_\epsilon)}
      {1+\|\nabla u_\epsilon\|_2^2}
 \longrightarrow\infty .
\tag{AH.3}
\]

因此即使把全局 \(L^2\) 能量固定，也不存在只依赖 \(E_0\) 的常数
\(C(E_0)\)，使所有光滑无散场都满足

\[
 {\mathscr R}^2(u)
 \le C(E_0)H(u)\bigl(1+\|\nabla u\|_2^2\bigr).
\tag{AH.4}
\]

## 2. Euclidean 常速平台与远源压力

先在 \(\mathbb R^3\) 构造一个固定紧支撑种子。取球
\(K=B_1(0)\)、非零常向量 \(c\)，以及
\(\chi_0\in C_c^\infty(B_2(0))\)，使 \(\chi_0=1\) 于 \(K\)。令

\[
 A_0(x)=\frac12c\times x,\qquad
 V_0=\nabla\times(\chi_0 A_0).
\tag{AH.5}
\]

因为 \(\nabla\times(c\times x)=2c\)，所以 \(V_0=c\) 于 \(K\)；
同时 \(V_0\) 光滑、紧支撑且无散。

还需要一只支撑分离的远源涡。取非零、径向
\(\psi\in C_c^\infty(B_1(0))\)，并令

\[
 W=(\partial_2\psi,-\partial_1\psi,0),\qquad
 M_{ij}:=\int_{\mathbb R^3}W_iW_j
   =m\,\operatorname{diag}(1,1,0)_{ij},\quad m>0.
\tag{AH.6}
\]

固定 \(y_0=Le_3\)，其中 \(L>4\)。对小的 \(\eta>0\)，置

\[
 w_\eta(x)=\eta^{-3/2}
        W\!\left(\frac{x-y_0}{\eta}\right),\qquad
 P_\eta=\partial_i\partial_j\Gamma*(w_{\eta,i}w_{\eta,j}),
 \qquad -\Delta\Gamma=\delta_0 .
\tag{AH.7}
\]

这里 \(w_\eta\) 光滑、紧支撑、无散，并在 \(\eta\) 足够小时与
\(V_0\) 支撑分离。由于 Newtonian 核在 \(K-y_0\) 上光滑，直接对核作
Taylor 展开给出，一致地对 \(x\in K\)，

\[
 \nabla P_\eta(x)
 =M_{ij}\nabla\partial_i\partial_j\Gamma(x-y_0)+O_K(\eta).
\tag{AH.8}
\]

在源点之外 \(\Delta\Gamma=0\)，故

\[
 M_{ij}\partial_i\partial_j\Gamma
 =m(\partial_{11}+\partial_{22})\Gamma
 =-m\partial_{33}\Gamma .
\tag{AH.9}
\]

沿 \(e_3\) 轴，\(\nabla\partial_{33}\Gamma\ne0\)。因此固定足够小的
\(\eta\)，并记 \(w=w_\eta\)、\(P_w=P_\eta\)，便有

\[
 g:=\nabla P_w(0)\ne0 .
\tag{AH.10}
\]

这一步完全在 \(\mathbb R^3\) 上；这里没有周期 Green 函数，也没有
周期光滑余项。

令 \(P_0\) 是 \(V_0\) 的 Euclidean 衰减压力，并取有限但充分大的
常数 \(b>0\)，使

\[
 V=V_0+bw,\qquad
 P=P_0+b^2P_w,\qquad
 |b^2g|>|\nabla P_0(0)| .
\tag{AH.11}
\]

支撑分离使 \(V_0\otimes w=w\otimes V_0=0\) 逐点成立，所以 AH.11
中的压力分解是精确的。特别地，\(\nabla P(0)\ne0\)，从而 \(P\) 在
\(K\) 上不是常数。另一方面 \(V=c\) 于 \(K\)，故
\(Q:=|V|=q_0:=|c|>0\) 在整个平台上为常数。于是

\[
 \begin{aligned}
 {\mathscr R}_{\mathbb R^3}^2(V)
 &:=\inf_\Phi\int_{\mathbb R^3}
      Q\,|P-\Phi(Q)|^2\\
 &\ge q_0\inf_{a\in\mathbb R}\int_K|P-a|^2
 =:\rho_0^2>0 .
 \end{aligned}
\tag{AH.12}
\]

任意紧支撑无散场都满足
\(\int V_i=\int\partial_j(x_iV_j)=0\)。最后把整个 \(V\) 乘一个固定
正常数，使 \(\|V\|_2^2=E_0\)。把缩放后的场、压力、平台常值和
正方差仍记为 \(V,P,q_0,\rho_0^2\)。这一固定幅值变换把 \(P\)
乘幅值平方，不会破坏 AH.12 的严格正性。

## 3. 单个紧支撑泡嵌入环面

取 \(R_0<\infty\)，使 \(\operatorname{supp}V\subset B_{R_0}(0)\)。
固定 \(x_0\in\mathbb T^3\)。当 \(\epsilon R_0<\pi/4\) 时，定义

\[
 u_\epsilon(x)=\epsilon^{-3/2}
 \sum_{k\in\mathbb Z^3}
 V\!\left(\frac{\widetilde x-\widetilde x_0+2\pi k}{\epsilon}\right).
\tag{AH.13}
\]

相容提升的改变只重排求和；小支撑保证每点至多有一个非零副本。
所以 \(u_\epsilon\) 是光滑周期无散场。由上一节的零积分，它仍为
零均值。直接换元得到全部精确尺度

\[
 \begin{aligned}
 \|u_\epsilon\|_2^2&=\|V\|_2^2=E_0,\\
 H(u_\epsilon)&=\epsilon^{-3/2}H(V),\\
 \|\nabla u_\epsilon\|_2^2
   &=\epsilon^{-2}\|\nabla V\|_2^2.
 \end{aligned}
\tag{AH.14}
\]

这是一只泡的空间集中，不是把一个周期胞元复制 \(\epsilon^{-3}\) 次。

## 4. 周期压力的分布核与平台方差

令 \({\cal G}_{\mathbb T}\) 是 \(-\Delta\) 的周期零均值 Green 函数。
在原点的一个固定坐标邻域内，分布意义下有

\[
 \partial_i\partial_j{\cal G}_{\mathbb T}
 =\partial_i\partial_j\Gamma+S_{ij},
 \qquad S_{ij}\in C^\infty .
\tag{AH.15}
\]

这里两边的 Hessian 都按分布理解；奇异核的对角 delta 部分包含在
\(\partial_i\partial_j\Gamma\) 中，没有被删去。令 \(p_\epsilon\) 是
AH.1 的周期零均值压力。对 \(y\in K\)，把
\(x=x_0+\epsilon y\) 代入卷积，并对源变量作同一换元，AH.15 给出

\[
 p_\epsilon(x_0+\epsilon y)
 =\epsilon^{-3}P(y)+r_\epsilon(y),\qquad
 \|r_\epsilon\|_{L^\infty(K)}\le C(V,{\cal G}_{\mathbb T}).
\tag{AH.16}
\]

其中 Euclidean 奇异部分精确产生 \(\epsilon^{-3}P\)；光滑部分为

\[
 r_\epsilon(y)
 =\int S_{ij}\bigl(\epsilon(y-z)\bigr)V_i(z)V_j(z)\,dz,
\tag{AH.17}
\]

所以只是 \(O(1)\)，而不是 Euclidean 种子中的一项。任何另选的压力
常数都只改变 \(r_\epsilon\) 的常数部分，不影响下面的方差。

缩放平台为 \(K_\epsilon=x_0+\epsilon K\)。在这里
\(q_\epsilon=|u_\epsilon|=\epsilon^{-3/2}q_0\)。对任意 \(\Phi\)，令

\[
 a_\epsilon=\epsilon^3
    \Phi(\epsilon^{-3/2}q_0).
\]

只把 AH.2 的积分限制到 \(K_\epsilon\)，便有

\[
 \begin{aligned}
 \int_{K_\epsilon}q_\epsilon
       |p_\epsilon-\Phi(q_\epsilon)|^2\,dx
 &=\epsilon^{-9/2}q_0
   \int_K|P+\epsilon^3r_\epsilon-a_\epsilon|^2\,dy\\
 &\ge\epsilon^{-9/2}q_0
   \inf_{a\in\mathbb R}
   \int_K|P+\epsilon^3r_\epsilon-a|^2\,dy .
 \end{aligned}
\tag{AH.18}
\]

到常数子空间的 \(L^2(K)\) 距离是 1-Lipschitz 的。由 AH.12、AH.16，
当 \(\epsilon\) 足够小时，

\[
 q_0\inf_{a\in\mathbb R}
 \int_K|P+\epsilon^3r_\epsilon-a|^2\,dy
 \ge\frac14\rho_0^2.
\tag{AH.19}
\]

因此

\[
 {\mathscr R}^2(u_\epsilon)
 \ge\frac14\rho_0^2\epsilon^{-9/2}.
\tag{AH.20}
\]

结合 AH.14，并令 \(G_0=\|\nabla V\|_2^2>0\)，对
\(0<\epsilon\le1\) 有

\[
 \begin{aligned}
 \frac{{\mathscr R}^2(u_\epsilon)/H(u_\epsilon)}
      {1+\|\nabla u_\epsilon\|_2^2}
 &\ge
 \frac{\rho_0^2}{4H(V)}
 \frac{\epsilon^{-3}}{1+G_0\epsilon^{-2}}\\
 &\ge
 \frac{\rho_0^2}{4H(V)(1+G_0)}\epsilon^{-1}
 \longrightarrow\infty .
 \end{aligned}
\tag{AH.21}
\]

这证明了 AH.3--AH.4。

## 5. 为什么周期复制不能代替单泡

若从固定周期场 \(U\) 出发，对整数 \(N\) 只令
\(U_N(x)=A\,U(Nx)\)，那么映射
\(x\mapsto Nx\) 保持归一化后的空间分布，却产生 \(N^3\) 个副本。
固定 \(L^2\) 能量时 \(A\) 不随 \(N\) 增长；此时
\({\mathscr R}^2/H\) 不随 \(N\) 增长，而
\(\|\nabla U_N\|_2^2\) 按 \(N^2\) 增长，目标比值反而趋于零。
AH.13 的单个紧支撑泡和 \(\epsilon^{-3/2}\) 幅值缺一不可。

## 6. 结论边界：大残差不等于大压力功

在产生 AH.20 下界的平台 \(K_\epsilon\) 上，速度和模长都是常数，故

\[
 F=-\frac{u_\epsilon}{|u_\epsilon|}\cdot\nabla q_\epsilon=0,
 \qquad
 p_\epsilon u_\epsilon\cdot\nabla q_\epsilon=0.
\tag{AH.22}
\]

所以这个例子揭示的是：\({\mathscr R}\) 会把常速平台上并不做功的
远源压力变化也全部计入。AH.20 不能推出压力功 \(W\) 很大，更不能替代
PressureGeometry 中带 \(F\) 或 \(Z_e\) 的方向控制。

每个 \(u_\epsilon\) 都可以作为黏性 1、无外力周期 NS 的光滑初值，
但 AH.14 显示其 \(H^1\) 大小发散，由标准 \(H^1\) 局部理论得到的
保证寿命没有统一正下界；本构造不判断实际最大寿命是否可能更长。本稿
只排除包含初始时刻的普适瞬时预算 AH.4；它不排除正成熟时间后的平滑估计，
不证明同一固定解上的时间积分失败，也不是 NS 轨道、首次奇点、反向持留
或合同 G 的反例。

本节是纯解析工作，没有仿真、DGX 或科学图。实际文件独立复核范围
见本包 audit，不作新颖性或发表等级声明。**G OPEN / NOT CLAY。**
