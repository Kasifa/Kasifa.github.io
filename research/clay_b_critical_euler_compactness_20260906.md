# 临界 Euler 缩放：条件压力控制与完整短窗紧性

2026-09-06。**INTERNAL / CONDITIONAL PROPOSITION / NON-AUTHOR REVIEW PASS / G OPEN / NOT CLAY。**

我检查上一阶段指定的一个问题：在能量保持的扩张周期胞上，
是否还须独立假设压力有界？答案在下面明确的速度假设下是否定的。
这是标准局部化与紧性工具的重组，不宣称新颖性或一般 NS 正则性。

## 1. 原解、条件和结论

原周期胞为 \(\mathbb T^3=(-\pi,\pi]^3\)。固定任意一个无外力、
黏性一的光滑周期 NS 解 \(u,p\)，考察它的首次可能奇点时间
\(T_*<\infty\)，在 \(0<t<T_*\) 光滑。压力取原胞零均值。
记 \(E=\sup_{0<t<T_*}\int_{\mathbb T^3}|u(t)|^2<\infty\)。

选 \(\lambda_k\downarrow0\)、中心 \(x_k\)，设置
\[
 L_k=\lambda_k^{-1},\quad \nu_k=\lambda_k^{1/2},\qquad
 w_k(y,\tau)=\lambda_k^{3/2}
 u(x_k+\lambda_ky,T_*+\lambda_k^{5/2}\tau),\quad
 \pi_k(y,\tau)=\lambda_k^3p(x_k+\lambda_ky,T_*+\lambda_k^{5/2}\tau).
\tag{BL.1}
\]
这是 \(\mathbb T^3_{L_k}=(-\pi L_k,\pi L_k]^3\) 上的完整方程：
\[
 \partial_\tau w_k+\operatorname{div}(w_k\otimes w_k)+\nabla\pi_k
 =\nu_k\Delta w_k,\quad \operatorname{div}w_k=0,\quad
 \int_{\mathbb T^3_{L_k}}\pi_k=0,\quad
 \sup_\tau\int_{\mathbb T^3_{L_k}}|w_k|^2\le E.
\tag{BL.2}
\]
每个固定 \(Q_{R,S}=B_R\times(-S,0)\) 对充分大的 \(k\) 都在定义域内。
另假设，对每个 \(R,S>0\)，有与 \(k\) 无关的有限 \(C_{R,S}\)，
以及一个固定 \(\varepsilon_*>0\)，使
\[
 \int_{Q_{R,S}}|\nabla w_k|^2
 =\lambda_k^{-1/2}
 \int_{T_*-S\lambda_k^{5/2}}^{T_*}
 \int_{B_{R\lambda_k}(x_k)}|\nabla u|^2
 \le C_{R,S},\qquad
 \int_{Q_{1,1}}|w_k|^3\ge\varepsilon_*.
\tag{BL.3}
\]
两项都是额外条件，没有由基本能量、有限总耗散或候选奇点推出。
不同 \(R,S\) 的常数可不同，不能擅自给它们增长率。

**条件命题。** 在 BL.1--BL.3 下，有一个子列及 \(w,\pi\)，在每个
固定 \(Q_{R,S}\) 上
\[
 \begin{gathered}
 w_k\longrightarrow w\ \hbox{强 }L^q,\quad 1\le q<10/3,\qquad
 \pi_k\longrightarrow\pi\ \hbox{强 }L^{3/2},\\
 w\in L^\infty((-\infty,0);L^2(\mathbb R^3)),\quad
 \mathop{\rm ess\,sup}_{\tau<0}\|w(\tau)\|_2^2\le E,\quad
 \int_{Q_{1,1}}|w|^3\ge\varepsilon_*.
 \end{gathered}
\tag{BL.4}
\]
极限为古老 Euler 解，局部 \(L^2_\tau H^1_y\)，具有全空间规范
Riesz 压力与开域内局部能量等式。没有任意时间压力常数残留。
命题不声称全空间能量守恒、Euler 刚性或原解正则。

## 2. 局部速度与规范周期核

取截止 \(\eta_R=1\) 于 \(B_{3R}\)，支撑在 \(B_{4R}\)，
\(|\nabla\eta_R|\le C/R\)。全空间 Sobolev 与插值给
\[
 \int_{Q_{3R,S}}|w_k|^{10/3}
 \le C E^{2/3}\big(C_{4R,S}+SE/R^2\big)=:V_{R,S}.
\tag{BL.5}
\]
这里先对 \(\eta_Rw_k\) 使用
\(\|v\|_{10/3}^{10/3}\le\|v\|_2^{4/3}\|v\|_6^2\)，
再用 \(\|v\|_6\le C\|\nabla v\|_2\)。常数不依赖 \(L_k\)。

为明确这一基础空间工具，可从紧支撑标量 \(h\) 的三个坐标
基本定理界 \(|h(x)|\le A_i(\widehat x_i):=\int|\partial_i h|dx_i\)
出发。对 \((A_1A_2A_3)^{1/2}\) 依次使用 Cauchy--Schwarz，
得 \(\int|h|^{3/2}\le\prod_i\|\partial_i h\|_1^{1/2}\)。
以 \(h=|v|^4\) 代入，再用 Hölder，得
\(\|v\|_6^4\le C\|v\|_6^3\|\nabla v\|_2\)；零值情形直接成立，
非零时约去公共因子。光滑逼近给所需 \(H^1\) 版本。

令 \(G_L\) 为 \(-\Delta_{\mathbb T_L^3}\) 的零均值 Green 函数。
它满足
\[
 -\Delta G_L=\delta_0-(2\pi L)^{-3},\qquad
 G_L(z)=L^{-1}G_1(z/L),\qquad
 K_{ij,L}:=\partial_i\partial_jG_L.
\tag{BL.6}
\]
构造上可在单位胞内用一个等于一的局部截止乘
\(\Gamma(z)=(4\pi|z|)^{-1}\)，再解具有光滑零均值右端的周期
Poisson 方程。后者的 Fourier 系数除以非零 \(|n|^2\)，仍快速衰减，
所以修正光滑。由缩放，在原点的固定比例邻域内，
\[
 K_{ij,L}
 =\operatorname{p.v.}\frac{3z_i z_j-|z|^2\delta_{ij}}{4\pi|z|^5}
   -\frac{\delta_{ij}}3\delta_0+\partial_i\partial_jH_L,\qquad
 |D^2H_L|\le CL^{-3}.
\tag{BL.7}
\]
原点 delta 系数可由去掉小球后两次积分分部及球面平均
\(\int_{\mathbb S^2}n_i n_j=4\pi\delta_{ij}/3\) 验证。
因此近场压力含 \(-|w_k|^2/3\)，不能只保留点态核。
单位胞去掉原点后光滑紧致，BL.7 与缩放进一步给
\[
 |K_{ij,L}(z)|\le C\,d_L(z,0)^{-3}\quad(z\ne0),
\tag{BL.8}
\]
其中 \(d_L\) 是周期距离。完整周期像和零模已包含在 \(G_L\)；
没有把不绝对收敛的三次幂周期像级数逐项取绝对值。

## 3. 压力不需独立输入

记 \(\mathcal T_{ij}=\partial_i\partial_j(-\Delta_{\mathbb R^3})^{-1}\)。
其 Fourier 乘子为 \(-\xi_i\xi_j/|\xi|^2\)，故在 \(L^2\) 有界；
离对角核就是 BL.7 的 Euclidean 部分，满足三次幂大小及四次幂
梯度界。因此经典 Calderón--Zygmund 定理在 \(p=5/3,3/2\) 给
\[
 \|\mathcal T_{ij}F\|_p\le C_p\|F\|_p,\qquad 1<p<\infty.
\tag{BL.9}
\]
只在 Euclidean 空间调用此已知定理。原文定义、弱型证明与有限
\(p\) 推论的读取范围见本节文献记录；不把周期范数一致性当作未证黑箱。

取 \(0\le\chi_R\le1\)，等于一于 \(B_{2R}\)，支撑于 \(B_{3R}\)。
对 \(y\in B_R\)，当 \(L_k\) 足够大时，完整规范压力精确写为
\[
 \begin{split}
 \pi_k(y,\tau)
 ={}&\mathcal T_{ij}(\chi_R w_{k,i}w_{k,j})(y,\tau)
       +h_{k,R}(y,\tau)+f_{k,R}(y,\tau),\\
 h_{k,R}&=\int D_{ij}H_{L_k}(y-z)\chi_R(z)w_{k,i}w_{k,j}(z)\,dz,\\
 f_{k,R}&=\int_{\mathbb T^3_{L_k}}
       K_{ij,L_k}(y-z)(1-\chi_R(z))w_{k,i}w_{k,j}(z)\,dz .
 \end{split}
\tag{BL.10}
\]
重复指标求和。第一项的源作零延拓；后两项无奇异积分，
因为前者只有光滑修正，后者源与 \(B_R\) 的周期距离至少为 \(R\)。
于是逐时
\[
 |h_{k,R}|\le CL_k^{-3}E,\qquad |f_{k,R}|\le CR^{-3}E,
\tag{BL.11}
\]
不作任意 gauge 扣除。由 BL.5、BL.9--BL.11 得
\[
 \int_{Q_{R,S}}|\pi_k|^{5/3}
 \le C\big[E^{2/3}C_{4R,S}+SE^{5/3}R^{-2}\big]=:P_{R,S}.
\tag{BL.12}
\]
例如
\(\int_{Q_{R,S}}|\pi_k|^{3/2}
 \le |Q_{R,S}|^{1/10}P_{R,S}^{9/10}\)。
这是每个固定柱体的控制，不是 Seregin 原稿的全尺度一致加权预算。

## 4. 时间紧性覆盖整个短窗

以下给出紧性的直接证明，不将只在远离零时成立的收敛延伸到零。
取固定空间截止 \(\eta\)，等于一于 \(B_R\)，支撑在 \(B_{2R}\)，
置 \(v_k=\eta w_k\) 后零延拓。在 \((-S,0)\) 上，
\[
 v_k\ \hbox{有界于 }L^\infty_\tau L^2_y\cap L^2_\tau H^1_y,\qquad
 \partial_\tau v_k\ \hbox{有界于 }L^{5/3}_\tau W^{-1,5/3}_y.
\tag{BL.13}
\]
第二项来自 BL.2：\(\eta\operatorname{div}(w_k\otimes w_k+\pi_kI)\)
配对时保留 \(\nabla\eta\) 项，由 BL.5、BL.12 控制；
\(\nu_k\eta\Delta w_k\) 一次分部后由局部 \(L^2\) 梯度控制，
有限空间时间域上的 \(L^2\subset L^{5/3}\) 即够用。
这里 \(W^{-1,5/3}\) 是 \(W^{1,5/2}\) 的对偶，所有截止项均紧支撑。

令 \(\rho_\delta\) 为光滑空间近似恒等核。空间平移估计给
\[
 \|v_k-\rho_\delta*v_k\|_{L^2(\mathbb R^3\times(-S,0))}
 \le C\delta\|\nabla v_k\|_{L^2(\mathbb R^3\times(-S,0))}.
\tag{BL.14}
\]
对固定 \(\delta>0\)，BL.13 与时间 Hölder 给
\[
 \|(\rho_\delta*v_k)(t)-(\rho_\delta*v_k)(s)\|_\infty
 \le C_{\delta,R,S}|t-s|^{2/5},\qquad -S<s,t<0.
\tag{BL.15}
\]
空间各阶导数的一致界来自 \(L^\infty_\tau L^2_y\)。
因此每个平滑序列可连续延至闭区间 \([-S,0]\)，且在固定紧空间集
与此闭区间上一致有界、等度连续。有限网格选子列再用等度连续性，
得到一致收敛子列。按 \(\delta\downarrow0\) 对角选取，结合 BL.14
得到整个 \(Q_{R,S}\) 上强 \(L^2\)。随后插值
\[
 \|w_k-w\|_{L^3(Q_{R,S})}
 \le \|w_k-w\|_{L^2(Q_{R,S})}^{1/6}
      \|w_k-w\|_{L^{10/3}(Q_{R,S})}^{5/6}\longrightarrow0.
\tag{BL.16}
\]
弱紧性和下半连续给极限局部梯度与 \(L^{10/3}\) 界；对整数
\(R,S\) 再对角选取，处理全部有限柱体。相同插值给 \(q<10/3\)。

另有显式终点薄层核验：
\(\int_{B_R\times(-a,0)}|w_k|^3
 \le |B_R|^{1/10}a^{1/10}
       (\int_{Q_{R,S}}|w_k|^{10/3})^{9/10}\)，
故对 \(0<a<S\) 一致趋零。BL.3 的下界不会只留在逃逸终点薄层。

## 5. 全空间能量与强规范压力

固定球上的 \(L^2\) 强收敛，可再选子列使几乎处处时间的局部
\(L^2\) 收敛同时在所有整数球成立。BL.2、单调收敛与可数对角法给
\(\int_{\mathbb R^3}|w(\tau)|^2\le E\) 几乎处处成立。
这保留的是非归一化全胞能量，不是每单位体积的平均。

因 \(w\otimes w\) 逐时全空间 \(L^1\)、局部时空 \(L^{5/3}\)，
定义其规范压力 \(\pi=\mathcal T_{ij}(w_iw_j)\)：
近源用 BL.9，远源用绝对收敛的 Euclidean 核积分。
不同截止半径给相同分布。对固定 \(A>2R\)，截断源于 \(B_A\)
并在 \(B_{2A}\) 外为零，BL.10--BL.11 同样成立。
源的强 \(L^{3/2}(Q_{2A,S})\) 收敛及 BL.9 给
\[
 \limsup_{k\to\infty}\|\pi_k-\pi\|_{L^{3/2}(Q_{R,S})}
 \le C E\,|Q_{R,S}|^{2/3}(A-R)^{-3}.
\tag{BL.17}
\]
这里先固定 \(A\) 令 \(k\to\infty\)：周期近源修正
\(CL_k^{-3}E\) 消失；两边远源均由全域 \(L^1\) 能量和分离距离控制。
再令 \(A\to\infty\) 得强压力收敛。既没有未定调和项，也没有
随时间变化的常数被隐含加入。BL.12 的弱下半连续还给极限局部
\(L^{5/3}\) 控制。

## 6. 方程、非零性与局部能量

在紧支撑测试下，速度强 \(L^2\)、压力强 \(L^{3/2}\) 传递
动量与无散方程。黏性项至多
\(\nu_k\|\nabla w_k\|_{L^2}\|\nabla\varphi\|_{L^2}\to0\)。
故
\[
 \partial_\tau w+\operatorname{div}(w\otimes w)+\nabla\pi=0,\quad
 \operatorname{div}w=0,\qquad
 \int_{Q_{1,1}}|w|^3=\lim_k\int_{Q_{1,1}}|w_k|^3\ge\varepsilon_*.
\tag{BL.18}
\]
原解在 \(T_*\) 前光滑，所以每个 \(w_k\) 具有局部能量等式。
对任意 \(\varphi\in C_c^\infty(\mathbb R^3\times(-\infty,0))\)，
\[
 \int\frac{|w_k|^2}{2}(\partial_\tau\varphi+\nu_k\Delta\varphi)
 +\int\left(\frac{|w_k|^2}{2}+\pi_k\right)w_k\cdot\nabla\varphi
 =\nu_k\int|\nabla w_k|^2\varphi .
\tag{BL.19}
\]
右侧绝对值至多 \(\nu_k C_{R,S}\|\varphi\|_\infty\to0\)，
左侧黏性截止项也趋零。由 BL.16--BL.17，三次通量及压力乘速度
在局部 \(L^1\) 强收敛，得到
\[
 \int\frac{|w|^2}{2}\partial_\tau\varphi
 +\int\left(\frac{|w|^2}{2}+\pi\right)w\cdot\nabla\varphi=0.
\tag{BL.20}
\]
这只是开古老域上的局部等式；没有把空间截止放至无穷远，
也未证明整条古老时间轴上的全空间能量守恒。若改成只有 suitable
弱原解的设定，不能沿用这里的原光滑局部等式假设而不另行核对。

## 7. 得到什么、未得到什么

本命题在 BL.3 的两个未付条件下消除了独立的压力界假设，
并保留完整短窗非零性及压力规范。它不支付 BL.3，不选择实际
奇点序列，不给所有 \(R,S\) 的增长率，不证明任何 Euler 刚性。
宽 Euler 类的全零刚性另受已知定常解反例限制，见 BM。
原 G、带符号压力功上界与一般三维正则性仍 OPEN，NOT CLAY。
