# 固定有界环带下的局部高高压力与坏时间净工作

2026-09-06。**INTERNAL / WORKING / CONDITIONAL INTERFACE / G OPEN / NOT CLAY。**

本稿不把全域耗散换成局部耗散。假定一个明确的固定有界环带，
用全局能量导数支付该环带的梯度，再证明 AM.20 的局部小尾估计。
环带选取的文献输入与完整几何推论另见
clay_b_fixed_regular_annulus_interface_20260906.md（AP）；
在合同的同一 suitable continuation 下，该固定环带可以选到。
本稿仍将其明确写成 AO.2，避免把环带存在误作统一缩球估计。
结果仍留下坏时间的净正工作，不是首次奇点排除或新颖性主张。

## 1. 固定几何、原速度与假设

在周期域 \(\mathbb T^3=(-\pi,\pi]^3\)、黏性 1 上，固定同一解，
在 \(I=(T_*-\tau_0,T_*)\)、\(0<\tau_0<T_*<\infty\) 光滑。
假定其能量界为 \(M>0\)，并写 \(g(\sigma)=\|\nabla u(\sigma)\|_2\)，
\(g^2\in L^1(I)\)。以指定中心为原点，在一个周期坐标内选

\[
 0<\rho_0<\rho_1<\rho_2<\rho_3<\rho_4<\rho_5<\pi/4,
 \qquad \rho_2<2\rho_1.
\tag{AO.1}
\]

本稿的额外固定环带输入仅为

\[
 \operatorname*{ess\,sup}_{\sigma\in I,\;
             \rho_0<|x|<\rho_5}|u(\sigma,x)|\le B<\infty.
\tag{AO.2}
\]

不假定该环带上所有导数一致有界。选择固定光滑截止

\[
 0\le\chi,\theta\le1,\quad
 \chi=1\text{ 于 }B_{\rho_1},\quad\operatorname{supp}\chi\subset B_{\rho_2},
 \quad\theta=1\text{ 于 }B_{\rho_3},\quad
 \operatorname{supp}\theta\subset B_{\rho_4}.
\tag{AO.3}
\]

记 \({\cal S}\) 为这些固定几何、截止、B、M 和乘子规范的集合。
以下 \(C_{\cal S}\) 不依赖 K、窗口终端或与 \(T_*\) 的距离；
但它可以依赖上述固定解和固定环带，不能用于无说明的缩球极限。
使用原速度定义

\[
 q=|u|,\quad H=H_\chi=\frac13\int\chi q^3,\quad
 D=D_\chi=\int\chi q\bigl(|\nabla u|^2+|\nabla q|^2\bigr),\quad
 U=\|\theta u\|_9.
\tag{AO.4}
\]

零速度处的加权梯度项沿用 AB 的零值约定。
对 AK 的固定平滑乘子和 \(K\ge1\)，令

\[
 h=P_{>K}u,\qquad \eta_K(\sigma)=\|\theta h(\sigma)\|_3,
 \qquad p_h=T_{ab}(h_a h_b).
\tag{AO.5}
\]

小尾范数只要求 \(\theta h\) 的局部源区域，而测试权重仍是 \(|u|u\)。
本文始终沿用带符号定义
\({\cal K}_\chi(p):=-\int\chi|u|u\cdot\nabla p\)。
\(h\) 无散且 \(\|h\|_2\le M\)；\(\theta h\) 一般不无散，
以下只对其张量使用压力算子，不把它称为无外力 NS 解。

## 2. 近远压力和频率截止交换子

在零均值周期压力规范下精确分解

\[
 p_h=p_n+p_f,\quad
 p_n=T_{ab}((\theta h)_a(\theta h)_b),\quad
 p_f=T_{ab}((1-\theta^2)h_a h_b).
\tag{AO.6}
\]

\(p_f\) 的源与 \(\operatorname{supp}\chi\) 有固定正距离。
周期 Green 核的三阶导数在离对角区域有界，保留所有周期副本后，

\[
 \|\nabla p_f\|_{L^\infty(\operatorname{supp}\chi)}
 \le C_{\cal S}M^2,\qquad
 |{\cal K}_\chi(p_f)|
 =\left|\int\chi q u\cdot\nabla p_f\right|
 \le C_{\cal S}M^4.
\tag{AO.7}
\]

这里使用的是完整配对，未把压力常数或壳项另行省略。

设 \(S_K=P_{\le K}\) 的周期卷积核为 \(\Phi_K\)。其 Euclidean
原核是 Schwartz 函数的 K 缩放；周期化给出统一 L1 核界、
第一绝对矩 \(\int d_{\mathbb T}(z,0)|\Phi_K(z)|\,dz\le C/K\)，
以及每个固定离对角距离上的任意阶 K 衰减。
精确交换子为

\[
 C_K:=\theta h-P_{>K}(\theta u)
 =[S_K,\theta]u
 =\int\Phi_K(x-y)(\theta(y)-\theta(x))u(y)\,dy.
\tag{AO.8}
\]

为避免在不正则区域免费用 \(u\) 的 L9 范数，取固定截止
\(\zeta_i=1\) 于 \(B_{\rho_0}\)、支撑于 \(B_{\rho_1}\)，
\(\zeta_o=1\) 于 \(B_{(\rho_4+\rho_5)/2}\)、支撑于 \(B_{\rho_5}\)。
于是

\[
 u=\zeta_i u+(\zeta_o-\zeta_i)u+(1-\zeta_o)u.
\tag{AO.9}
\]

中间项支撑在 AO.2 的环带上，L infinity 范数至多常数乘 B。
对这一项，AO.8 中的截止差至多 \(\|\nabla\theta\|_\infty
d_{\mathbb T}(x,y)\)，故用第一矩给 \(C_{\cal S}B/K\)。
对于内项，\(\theta=1\) 于其支撑的固定邻域；只有 x 离此邻域
一个固定距离时截止差才非零。外项同理，\(\theta=0\) 于其支撑的
固定邻域。对这两项用离对角核界及 \(\|u\|_1\le CM\)。
因此每个整数 \(N\ge1\) 都有

\[
 \|C_K\|_\infty
 \le C_{\cal S}B K^{-1}+C_{{\cal S},N}M K^{-N},
 \qquad \|C_K\|_9\le E_{\cal S}<\infty.
\tag{AO.10}
\]

后一个固定常数统一于 \(K\ge1\)。Young 卷积不等式又给
\(P_{>K}\) 的统一 L9 有界性，所以

\[
 \|\theta h\|_9\le C U+E_{\cal S},\qquad
 \|p_n\|_{9/4}
 \le C\|\theta h\|_{9/2}^2
 \le C\eta_K(CU+E_{\cal S}).
\tag{AO.11}
\]

第一条没有把非局部滤波器当成局部算子；AO.8--AO.10 正是该差额。
第二条使用周期双 Riesz 的标准 L9/4 界和
\(1/(9/2)=\frac12/3+\frac12/9\)。所有高高低输出仍在 \(p_n,p_f\) 中。

## 3. 扩大球梯度用真实能量支付

对 \(f=|\theta u|^{3/2}\) 使用周期 Sobolev。
在 \(B_{\rho_1}\) 内 \(\chi=1\)，在余下支撑内 \(q\le B\)。
直接求导及 AO.2 给

\[
 \begin{aligned}
 \|\nabla f\|_2^2
 &\le C\int\theta^3q|\nabla u|^2
      +C\int\theta|\nabla\theta|^2q^3
 \le CD+CBg^2+C_{\cal S},\\
 \|f\|_2^2&=\int\theta^3q^3\le3H+C_{\cal S},\\
 U^{3/2}=\|f\|_6
 &\le C_{\cal S}\bigl(D^{1/2}+g+H^{1/2}+1\bigr).
 \end{aligned}
\tag{AO.12}
\]

周期 Sobolev 的低阶项没有删除。外层耗散也没有被吸收进 D：
它以 \(Bg^2\) 的能量成本明确留下。
这只需要环带速度有界，不需要额外假定 \(\nabla u\) 一致有界。

近压完整配对拆成内部和壳项。其内部由加权 Cauchy 和 Hölder 给

\[
 \begin{aligned}
 |I_n|&:=\left|\int\chi p_n u\cdot\nabla q\right|\\
 &\le D^{1/2}\left(\int\chi q p_n^2\right)^{1/2}
 \le D^{1/2}\|p_n\|_{9/4}U^{1/2}\\
 &\le C\eta_K D^{1/2}
          \bigl(U^{3/2}+E_{\cal S}U^{1/2}\bigr).
 \end{aligned}
\tag{AO.13}
\]

使用 \(E x^{1/3}\le x+C E^{3/2}\) 于 \(x=U^{3/2}\)，
再代 AO.12，对任意 \(\epsilon>0\) 得

\[
 |I_n|\le(C_{\cal S}\eta_K+\epsilon)D
       +C_{{\cal S},\epsilon}\eta_K^2(g^2+H+1).
\tag{AO.14}
\]

壳项的 q 有 AO.2 的固定上界；Hölder、AO.11--AO.12 给

\[
 \begin{aligned}
 |L_n|&:=\left|\int p_n q u\cdot\nabla\chi\right|
 \le C_{\cal S}\|p_n\|_{9/4}
 \le C_{\cal S}\eta_K(U+E_{\cal S})\\
 &\le \epsilon D+C_{{\cal S},\epsilon}(1+g^2+H)
 \qquad(0\le\eta_K\le1).
 \end{aligned}
\tag{AO.15}
\]

末行由 \(U\le C_{\cal S}(D^{1/3}+g^{2/3}+H^{1/3}+1)\)
及 Young 得到，未反向使用 Sobolev。
选择固定的 \(\epsilon\) 足够小，再选择
\(0<\eta_*\le1\) 使 \(C_{\cal S}\eta_*+2\epsilon\le1/4\)，
合并 AO.7、AO.14 和 AO.15，得到

\[
 \boxed{\quad
 \eta_K(\sigma)\le\eta_*
 \quad\Longrightarrow\quad
 |{\cal K}_\chi(p_h)(\sigma)|
 \le\frac14D(\sigma)+C_{\cal S}(H(\sigma)+1+g(\sigma)^2).
 \quad}
\tag{AO.16}
\]

\(\eta_*\)、\(C_{\cal S}\) 依赖已固定的环带数据，但与 K 无关。
这是逐时条件估计，不声称好时间已占多数。

## 4. 回到成熟窗口：坏时间不能删除

取 \(t<T_*\)、\(r=\rho_1\)、\(\Lambda_A=\|u(t)\|_{L^3(B_r)}\ge1\)，
并要求

\[
 \delta=c_0r^2\Lambda_A^{-4},\quad
 J=(t-\delta,t)\subset I,\quad t-\delta\ge Cr^2,\quad
 K=\Lambda_A^{3/4}.
\tag{AO.17}
\]

K 由终端选定，在整个 J 中固定。令可测好坏集合为

\[
 G_K=\{\sigma\in J:\eta_K(\sigma)\le\eta_*\},\qquad
 B_K=J\setminus G_K.
\tag{AO.18}
\]

AB 的两个非压力截止项由环带速度有界得到 \(|S_\chi|\le C_{\cal S}\)。
AM.5 和 AM.14 取吸收份额 1/4，给全部低频参与压力的逐时余项

\[
 f_K(\sigma)
 =C_{\cal S}\bigl(M^4K^4+M^3r^{3/2}K^4g^2
                         +M^3r^{-1}K^2g\bigr)\ge0,
 \qquad \frac{\int_J f_K}{H(t)}\longrightarrow0.
\tag{AO.19}
\]

极限沿固定数据的合法 \(\Lambda_A\to\infty\) 窗口，使用 AM.18。
合并原方程恒等式而非仅拼接范数，有

\[
 H'\le C_{\cal S}\mathbf1_{G_K}(H+1)
       +C_{\cal S}(1+g^2)+f_K
       -\tfrac12\mathbf1_{G_K}D
       +\mathbf1_{B_K}\bigl({\cal K}_\chi(p_h)-\tfrac34D\bigr).
\tag{AO.20}
\]

坏时间留下的是带符号压力与其可用耗散之差，不把所有压力绝对值化。
定义一个尚待由方程支付的非负量

\[
 \mathcal B_J
 :=\int_{B_K}
       \left[{\cal K}_\chi(p_h)(\sigma)-\tfrac34D(\sigma)\right]_+
       \,d\sigma.
\tag{AO.21}
\]

对 \(s\in[t-\delta,t]\)，给 \(H+1\) 使用积分因子
\(\exp(-C_{\cal S}\int_s^\sigma\mathbf1_{G_K})\in[e^{-C_{\cal S}\delta},1]\)。
AO.20 的良好耗散项可保留或舍去，坏项用其正部上界，得到

\[
 H(s)+1\ge e^{-C_{\cal S}\delta}(H(t)+1)
       -\int_J f_K-C_{\cal S}(\delta+A_J)-\mathcal B_J.
\tag{AO.22}
\]

这一步没有假定 \(\int_{G_K}H\le\delta H(t)\)；当前时间的 H
由积分因子正确处理。因而，如果另能由实际方程证明
\(\mathcal B_J=o(H(t))\)，AO.22 才给出整个窗口内一致的
\(H(s)\ge(1-o(1))H(t)\)。这一额外净工作预算现在仍 OPEN。

## 5. 结论边界

本稿在 AO.2 的明确固定环带输入下，完成局部好时间的压力吸收，
并把未付时间问题定位到 AO.21。不是证明 AO.21 自动很小。
\(\eta_K\le\|P_{>K}u\|_3\)，所以 AK 仍只给
\(|B_K|/\delta\le C A_J\Lambda_A^{13/4}/(\eta_*^2c_0r^2)\)。
即便另有小测度，压力净工作仍可能集中其上，不能省掉 AO.21。

本文没有对截断速度建立 NS 方程，因此不产生或忽略 Bogovskii
外力；若以后改走该方程，仍必须重载已有完整外力清单。
固定环带量词由 AP 单独说明；缩球常数、指定移动路径、G 和一般正则性
保持各自开放边界。
本源不直接公开，不含仿真或科学图，独立审查完成前不冻结。
