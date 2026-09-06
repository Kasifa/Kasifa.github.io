# Clay B：固定球集中与卷积路径能说明什么

2026-09-06。**LITERATURE CONDITIONAL / PROVED LOCALLY / NEGATIVE LOGICAL MODEL /
G OPEN / NOT CLAY。**

这份笔记固定三个不同层级。Albritton--Barker 的固定球结论是文献输入，
并保留原定义的排字解释条件。固定尺度球包含和缓慢缩球对角引理在这里
直接证明。最后的场只是一项非 Navier--Stokes 反模型，用来检查哪些
聚合信息不足以推出合同 G。

## 1. 文献接口：周期内点的固定球集中

沿用 `clay_b_prescribed_centre_contract_20260905.md` 的归一化。
空间是 \(\mathbb T^3=(-\pi,\pi]^3\)，黏性为一。设 \(u\) 是光滑初值
的最大光滑解，最大区间为 \([0,T_*)\)。若 \(T_*<\infty\)，固定一个
suitable Leray--Hopf continuation；它在 \([0,T_*)\) 上由弱强唯一性
与光滑解一致。以下另固定一个实际奇点 \((x_*,T_*)\)。这不是说
时间片 \(T_*\) 上每一点都奇异。

Albritton--Barker, [Theorem 1.1](https://arxiv.org/pdf/1811.00507v2)，
对有界 \(C^2\) 域 \(\Omega\)、相对开边界部分
\(\Gamma\subset\partial\Omega\) 和 \(x_*\in\Omega\cup\Gamma\)
给出：若 \(v\) 是相应的 boundary suitable weak solution，且每个
\(t<T_*\) 前在 \(\Omega\times(0,t)\) 有界，那么终点奇异蕴含

\[
 \lim_{t\uparrow T_*}
 \|v(t)\|_{L^3(\Omega\cap B_r(x_*))}=\infty
 \qquad\text{对每个固定 }r>0.
\tag{L.1}
\]

这里有一项必须公开保留的来源缺陷。arXiv v2 的 Definition 2.1(1)
原页印成

\[
 \overline{\Omega'}\subset\Omega\subset\Gamma,
\tag{L.2}
\]

它与非空三维域 \(\Omega\) 及 \(\Gamma\subset\partial\Omega\) 不相容。
本地只对 arXiv v2 的这一页作过视觉核验；我没有取得可视觉核验的
出版社排版 PDF，因而不声称其他版本已修正或仍保留这行。这里按
标准预期条件

\[
 \overline{\Omega'}\subset\Omega\cup\Gamma
\tag{L.3}
\]

理解 Definition 2.1(1)。同一定义第 (3) 项的测试域、Proposition 2.2
的闭包条件、Lemma 3.3 中 \((\mathbb R^3,\varnothing)\) 的选择，以及
Remark 3.4 的内点论证都与 (L.3) 一致。因此下面的调用标为
**LITERATURE CONDITIONAL**，不是作者勘误声明，也不是本地重证原定理。

取小于环面注入半径的坐标球 \(\Omega=B_{r_0}(x_*)\)，并令
\(\Gamma=\varnothing\)。空集是 \(\partial\Omega\) 的相对开子集，
且人工球面上没有无滑移条件。周期 \(u,p\) 的欧氏提升限制到
\(\Omega\) 后保持分布方程、局部能量空间、局部
\(p\in L^{3/2}\) 和内部测试的局部能量不等式。全局弱
\(L^2\) 连续性限制后仍是 \(C_wL^2(\Omega)\)。定理的结论只取
\(t<T_*\) 的光滑值，不需要在 \(T_*\) 有强 \(L^2\) 或 \(L^3\) 迹。
由 (L.1)，

\[
 \boxed{\displaystyle
 \lim_{t\uparrow T_*}\|u(t)\|_{L^3(B_r(x_*))}=\infty
 \quad\text{对每个固定 }0<r<r_0.}
\tag{L.4}
\]

这是已有定理的周期内点推论。它没有给出随时间预定缩小的半径。

## 2. 固定尺度路径的球包含

对合法尺度

\[
 0<R<\min\{\pi/16,\sqrt{T_*}/8\},
\tag{P.1}
\]

沿用偶、径向、非负、质量一的紧支撑核，定义

\[
 u_R=\varphi_R^{\rm per}*u,\qquad
 \dot X_R(t)=u_R(t,X_R(t)),\qquad X_R(T_*)=x_*.
\tag{P.2}
\]

每个 \(R\) 都重新定义一条由同一终点锚定的路径。令

\[
 M=\mathop{\rm ess\,sup}_{t<T_*}\|u(t)\|_{L^2(\mathbb T^3)}<\infty.
\]

原卷积估计给出

\[
 |\dot X_R(s)|\le C_\varphi R^{-3/2}M,
 \qquad
 |X_R(T_*-h)-x_*|\le C_\varphi M R^{-3/2}h.
\tag{P.3}
\]

固定 \(R\) 后，右侧除以 \(R\) 趋于零。因此存在
\(h_R>0\)，使 \(0<h<h_R\) 时

\[
 |X_R(T_*-h)-x_*|<R/2,
 \qquad
 B_{R/2}(x_*)\subset B_R(X_R(T_*-h)).
\tag{P.4}
\]

结合 (L.4)，每个固定合法 \(R<2r_0\) 都有

\[
 \|u(T_*-h)\|_{L^3(B_R(X_R(T_*-h)))}\longrightarrow\infty.
\tag{P.5}
\]

这里没有比较两个不同尺度的路径，也没有把固定 \(R\) 的 ODE
换成变尺度 ODE。

## 3. 缓慢缩球的定性对角引理

下面的半径可以依赖这一个解。它不是预先给定的幂率。

**引理（PROVED LOCALLY）。** 假设 (L.4) 和 (P.3)。对每个预先选定的
\(0<\alpha<2/5\)，存在 \(h_1>0\) 和
\(\rho:(0,h_1]\to(0,\infty)\)，使得

\[
 \begin{gathered}
 \rho(h)\to0\quad(h\downarrow0),\qquad \rho(h)\ge h^\alpha,\\
 \|u(T_*-h)\|_{L^3(B_{\rho(h)/2}(x_*))}\to\infty,\\
 \frac{|X_{\rho(h)}(T_*-h)-x_*|}{\rho(h)}\to0.
 \end{gathered}
\tag{D.1}
\]

若 \(0<h'<h\le h_1\)，则 \(\rho(h')\le\rho(h)\)。所以
\(h\mapsto\rho(h)\) 按通常次序是非降的；等价地，实际时间中的
\(t\mapsto\rho(T_*-t)\) 随 \(t\uparrow T_*\) 非增。

**证明。** 取合法 \(R_*<\min\{r_0,\pi/16,\sqrt{T_*}/8,1\}\)，
并令 \(r_n=2^{-n}R_*\)。由 (L.4)，对每个 \(n\ge1\) 可取
\(\delta_n>0\)，使

\[
 0<h\le\delta_n
 \quad\Longrightarrow\quad
 \|u(T_*-h)\|_{L^3(B_{r_n/2}(x_*))}\ge n.
\tag{D.2}
\]

令 \(h_0=T_*\)，再递归选择

\[
 0<h_n<\min\{\delta_n,2^{-n},h_{n-1}/2,
                    r_n^{1/\alpha},64r_n^2\}.
\tag{D.3}
\]

对唯一满足 \(h_{n+1}<h\le h_n\) 的 \(n\)，定义

\[
 \rho(h)=r_n.
\tag{D.4}
\]

这覆盖 \((0,h_1]\)，并立即给出所述单调方向和
\(\rho(h)\to0\)。在第 \(n\) 个阶梯上，\(h\le h_n\le\delta_n\)，
故 (D.2) 给出范数至少为 \(n\)。又因
\(h\le h_n\le r_n^{1/\alpha}\)，有
\(h^\alpha\le r_n=\rho(h)\)。于是前两项极限成立。

在每一个时刻只调用对应固定尺度的 (P.3)，得到

\[
 \frac{|X_{\rho(h)}(T_*-h)-x_*|}{\rho(h)}
 \le C_\varphi M h\rho(h)^{-5/2}
 \le C_\varphi M h^{1-5\alpha/2}\longrightarrow0.
\tag{D.5}
\]

指数为正恰好使用 \(\alpha<2/5\)。此外

\[
 \frac{h}{\rho(h)^2}\le h^{1-2\alpha}\to0,
\tag{D.6}
\]

所以晚时间确在固定尺度路径的 \(64\rho(h)^2\) 定义窗内。
当 (D.5) 小于 \(1/2\) 时，

\[
 B_{\rho(h)/2}(x_*)
 \subset B_{\rho(h)}(X_{\rho(h)}(T_*-h)).
\tag{D.7}
\]

因此还得到

\[
 \|u(T_*-h)\|_{L^3(B_{\rho(h)}
       (X_{\rho(h)}(T_*-h)))}\longrightarrow\infty.
\tag{D.8}
\]

证毕。

函数 \(\rho\) 使用了未知的 \(\delta_n\)，所以 (D.1) 不允许把
\(\rho\) 换成预定的 \(h^\alpha\)，也不给
\(c h^\beta\le\rho(h)\le C h^\beta\)。固定球极限的量词本身允许
收敛阈值随半径任意恶化。

还要注意，\(X_{\rho(h)}(T_*-h)\) 是从一族固定尺度路径中逐时取值。
跨越阶梯时尺度和路径都会改变。它不必连续，更不满足一条变尺度
ODE，不能作为移动截止的可微路径代入完整时间柱体预算。

(D.8) 只给每个时刻的一只缩球。合同 (C.3) 的 \(E_R\) 还包含
整个 \([T_*-64R^2,T_*]\) 上的局部 \(L^2\) 本质上确界与积分耗散。
两者不能替换；在实际奇点处，已证 (C.4) 的逆否命题反而给出每个
固定合法 \(R\) 都有 \(E_R>\varepsilon_{\rm tube}\)。对角选择不产生 G
所需的完整 \(E_R\) 小性。

## 4. 终点发散与 \(L^4_tL^3_x\) 没有矛盾

周期能量类本来就包含这一有限时间可积性。由周期 Sobolev 插值，

\[
 \|u(t)\|_3^4
 \le C\|u(t)\|_2^2\|u(t)\|_6^2
 \le C\|u(t)\|_2^2
       \bigl(\|\nabla u(t)\|_2^2+\|u(t)\|_2^2\bigr).
\tag{I.1}
\]

因此在任意有限时间区间 \((0,T)\) 上，

\[
 \int_0^T\|u(t)\|_3^4\,dt
 \le C\|u\|_{L_t^\infty L_x^2}^2
 \left(\|\nabla u\|_{L_{t,x}^2}^2
       +T\|u\|_{L_t^\infty L_x^2}^2\right)<\infty.
\tag{I.2}
\]

这个积分结论不控制单个终点附近的逐时上界。点态时间极限发散仍可
与它并存。最简单的标量速度是 \(h^{-1/6}\)：

\[
 \int_0^T (h^{-1/6})^4\,dh
 =\int_0^T h^{-2/3}\,dh=3T^{1/3}<\infty.
\tag{I.3}
\]

因此 (L.4) 本身不与能量类已有的 \(L^4_tL^3_x\) 相冲突。下一节
给出同时实现这种增长、精确全局能量等式和有限耗散的显式场；
它不是 NS 解。

## 5. 精确能量等式的非 NS 反模型

取非零、非负、径向函数 \(\psi\in C_c^\infty(B_1(0))\)，并定义

\[
 \Phi=\nabla\times(0,0,\psi)
      =(\partial_2\psi,-\partial_1\psi,0),
\qquad
 C_2=\int_{\mathbb R^3}|\Phi|^2,
\qquad
 C_1=\int_{\mathbb R^3}|\nabla\Phi|^2.
\tag{M.1}
\]

则 \(\Phi\) 光滑、紧支撑、散度为零且为奇函数；\(C_1,C_2>0\)。令

\[
 \ell^2=\frac{12C_1}{C_2},\qquad A>0.
\tag{M.2}
\]

取小的终点 \(T>0\)，使 \(\ell\sqrt T<\pi/4\)。令
\(h=T-t\)，并在环面上周期化

\[
 u(t,x)=A h^{-2/3}
 \sum_{k\in\mathbb Z^3}
 \Phi\!\left(\frac{\widetilde x-\widetilde x_*+2\pi k}
                    {\ell\sqrt h}\right),
 \qquad 0\le t<T.
\tag{M.3}
\]

这里 \(\widetilde x,\widetilde x_*\) 是任意相容提升。小支撑保证每个
基本胞元只有一个局部副本。该场在每个 \(t<T\) 光滑且散度为零。
直接换元得到

\[
 \begin{aligned}
 \|u(t)\|_2^2
    &=A^2\ell^3C_2h^{1/6},\\
 \|\nabla u(t)\|_2^2
    &=A^2\ell C_1h^{-5/6},\\
 \|u(t)\|_3
    &=A\ell\|\Phi\|_3h^{-1/6}.
 \end{aligned}
\tag{M.4}
\]

由 (M.2)，

\[
 \frac12\frac{d}{dt}\|u(t)\|_2^2+\|\nabla u(t)\|_2^2
 =A^2\ell h^{-5/6}
   \left(C_1-\frac{\ell^2C_2}{12}\right)=0.
\tag{M.5}
\]

所以任意 \(0\le t_1<t_2<T\) 都满足精确全局能量等式

\[
 \frac12\|u(t_2)\|_2^2
 +\int_{t_1}^{t_2}\|\nabla u(t)\|_2^2\,dt
 =\frac12\|u(t_1)\|_2^2.
\tag{M.6}
\]

令 \(u(T)=0\)，(M.6) 也可取 \(t_2=T\)，并且

\[
 \int_0^T\|\nabla u(t)\|_2^2\,dt
 =6A^2\ell C_1T^{1/6}<\infty.
\tag{M.7}
\]

另一方面，

\[
 \int_0^T\|u(t)\|_3^4\,dt
 =3A^4\ell^4\|\Phi\|_3^4T^{1/3}<\infty.
\tag{M.8}
\]

对每个固定 \(r>0\)，当 \(h<(r/\ell)^2\) 时全部支撑落在
\(B_r(x_*)\)，故局部 \(L^3\) 范数仍按 \(h^{-1/6}\) 趋于无穷。
这验证了 (I.3) 所述兼容性。

## 6. 原卷积路径恒定，完整能量仍可在每个尺度很大

由于 \(u(t,x_*+z)=-u(t,x_*-z)\)，原合同的偶径向核满足

\[
 (\varphi_R^{\rm per}*u)(t,x_*)=0.
\tag{M.9}
\]

固定尺度路径的唯一性于是给出

\[
 X_R(t)\equiv x_*
\tag{M.10}
\]

对每个合法 \(R\) 成立。这里“合法”使用终点 \(T\)：

\[
 0<R<\min\{\pi/16,\sqrt T/8\}.
\tag{M.11}
\]

令

\[
 c_0=\min\{1,16/\ell^2\},\qquad h_R=c_0R^2.
\tag{M.12}
\]

则 \(0<h_R<64R^2<T\)，且
\(\operatorname{supp}u(T-h_R)\subset B_{4R}(x_*)\)。在合同 (C.3)
的完整移动核心能量中，仅取这个时刻的 kinetic 项便有

\[
 \begin{aligned}
 E_R(T,x_*)
 &\ge \frac1{8R}
       \int_{B_{8R}(x_*)}|u(T-h_R,x)|^2\,dx\\
 &=\frac{A^2\ell^3C_2c_0^{1/6}}8R^{-2/3}.
 \end{aligned}
\tag{M.13}
\]

上述局部 \(L^2\) 量随 \(t<T\) 连续，所以单个时刻的值确实不超过
相应的本质上确界；这里没有用零测时间截面替换 essential supremum。

这对每个合法 \(R\) 成立。若再取

\[
 T<\min\left\{\frac{\pi^2}{4},
                 \frac{\pi^2}{16\ell^2}\right\},
\tag{M.14}
\]

则 (M.11) 的有效上限是 \(\sqrt T/8\)，从而

\[
 E_R(T,x_*)>
 \frac{A^2\ell^3C_2c_0^{1/6}}{2T^{1/3}}
 \qquad\text{对所有合法 }R.
\tag{M.15}
\]

给定合同门槛 \(\varepsilon_{\rm tube}>0\)，还可要求

\[
 T<\left(
 \frac{A^2\ell^3C_2c_0^{1/6}}
      {2\varepsilon_{\rm tube}}
 \right)^3.
\tag{M.16}
\]

于是这个场在所有合法尺度上都有
\(E_R(T,x_*)>\varepsilon_{\rm tube}\)。这不是对 NS 合同 G 的反例；
它只表明精确总能量等式、有限耗散、固定球集中和路径稳定本身
不会迫使出现小的完整 \(E_R\)。

## 7. curl 与矩检验：这个场不可能满足 NS

这一点不能只用标签说明。记

\[
 y=\frac{x-x_*}{\ell\sqrt h},\qquad
 V=\frac23\Phi+\frac12(y\cdot\nabla)\Phi-\ell^{-2}\Delta\Phi,
 \qquad
 N=(\Phi\cdot\nabla)\Phi.
\tag{N.1}
\]

在支撑所在的欧氏坐标球内，

\[
 \partial_tu-\Delta u=A h^{-5/3}V,
 \qquad
 (u\cdot\nabla)u=A^2\ell^{-1}h^{-11/6}N.
\tag{N.2}
\]

若存在压力使 (M.3) 在整个 \((0,T)\) 满足无外力 NS，取空间 curl
并约去 \(A\ell^{-1}h^{-13/6}\) 后必须有

\[
 \operatorname{curl}V+\frac{A}{\ell}h^{-1/6}
       \operatorname{curl}N=0
 \qquad\text{对所有 }h\in(0,T).
\tag{N.3}
\]

这里固定同一个 \(y\)，分别在物理点 \(x_h=x_*+\ell\sqrt h\,y\)
处评价不同 \(h\) 的恒等式；对支撑内的 \(y\) 均在合法欧氏副本中，
支撑外 \(V,N\) 为零。因此在两个不同的 \(h\) 上相减，先得
\(\operatorname{curl}N=0\)，再得 \(\operatorname{curl}V=0\)。
同时 \(\operatorname{div}V=0\)，且 \(V\) 光滑紧支撑。因此向量恒等式
或分部积分给出 \(\nabla V=0\)，从而 \(V=0\)。

但 \(\Phi_1=\partial_2\psi\)，所以

\[
 \int_{\mathbb R^3}y_2\Phi_1\,dy=-\int_{\mathbb R^3}\psi\,dy.
\tag{N.4}
\]

对紧支撑函数 \(f\)，分部积分给出

\[
 \int y_2(y\cdot\nabla f)\,dy=-4\int y_2f\,dy,
 \qquad
 \int y_2\Delta f\,dy=0.
\tag{N.5}
\]

代入 \(V_1\) 得到

\[
 \int_{\mathbb R^3}y_2V_1\,dy
 =\left(\frac23-2\right)\int y_2\Phi_1\,dy
 =\frac43\int_{\mathbb R^3}\psi\,dy>0.
\tag{N.6}
\]

这与 \(V=0\) 矛盾。因此不存在任何压力把 (M.3) 变成 NS 解。

## 8. 结论边界

1. (L.4) 是带 Definition 2.1 显式排字解释的
   **LITERATURE CONDITIONAL** 输入。
2. 固定尺度球包含和 (D.1)--(D.8) 是本地证明的定性结论。
   对角半径依赖解，不是预定幂率；其中心不是一条变尺度路径。
3. \(L^4_tL^3_x\) 有限与固定球 \(L^3\) 终点发散可以同时成立。
4. (M.3) 只是否定一条逻辑推断：全局能量等式、有限耗散、
   固定球集中、原卷积路径控制等聚合信息，单独不足以推出 G。
5. curl 检验只排除了 NS 方程，所以该模型不是 suitable NS 解。
   我没有另行构造压力或核查脱离 NS 方程单独书写的标量局部能量
   不等式。它不是 NS 奇点、LEI 或 Clay 反例。真实 NS 的带符号
   非线性、压力和 defect-completed 局部预算仍可能提供模型刻意
   缺少的信息。

所以合同 G 仍为 **OPEN / NOT CLAY**。这里没有新颖性声明，也没有
把文献定理、本地证明和反模型放在同一个证明层级。
