# 单侧局部压力势的能量类筛查

2026-09-06。**INTERNAL / PENDING REVIEW / ENERGY-CLASS SCREEN / G OPEN / NOT CLAY。**

我在这里检查一个很窄的问题：基本能量类是否已经自动给出
Seregin--Šverák 单侧压力机制所需的时间一致局部压力势控制。
答案是否定的。能量确实给出一个尺度一致的 \(L^1_t\) 上界；但它
不给 \(L^\infty_t\) 或候选终点的有限左连续迹。下面的反检查始终
使用由速度张量产生的真实周期压力负部，不把任意标量函数冒充压力。

这只是条件适用性的基线，不复述或导入全空间定理，也不构造
Navier--Stokes 奇点。

## 1. 能量给出的空间与时间界

空间取 \(\mathbb T^3=(-\pi,\pi]^3\)。固定一个时刻，设 \(u\) 为
零均值、无散的光滑实向量场，并采用零均值压力规范

\[
 p=\partial_i\partial_j(-\Delta)^{-1}(u_i u_j),
 \qquad \int_{\mathbb T^3}p=0 .
\tag{BG.1}
\]

记

\[
 M=\|u\|_2,\qquad g=\|\nabla u\|_2,\qquad
 p_-:=\max\{-p,0\},
\]

并对 \(0<R<\pi/4\) 定义提升坐标中的局部压力势

\[
 \mathcal P_R^-(x)
 :=\int_{B_R(x)}\frac{p_-(y)}{|y-x|}\,dy .
\tag{BG.2}
\]

因为 \(R<\pi/4\)，球和距离可以在唯一的小坐标提升中理解。
周期 Riesz 变换的有限 \(L^q\) 有界性及零均值
Poincaré–Sobolev 不等式给

\[
 \|p\|_3\le C\|u\otimes u\|_3
 \le C\|u\|_6^2\le Cg^2,
 \qquad
 \|p\|_2\le C\|u\|_4^2
 \le C M^{1/2}g^{3/2}.
\tag{BG.3}
\]

令 \(K_R(z)=\mathbf 1_{|z|<R}|z|^{-1}\)。三维直接积分得到

\[
 \|K_R\|_{3/2}
 =\left(4\pi\int_0^R r^{1/2}\,dr\right)^{2/3}
 =C R,
 \qquad
 \|K_R\|_2
 =\left(4\pi\int_0^R1\,dr\right)^{1/2}
 =C R^{1/2}.
\tag{BG.4}
\]

因此 Hölder 给出两套逐时估计

\[
 \boxed{
 \sup_x\mathcal P_R^-(x)\le C Rg^2,\qquad
 \sup_x\mathcal P_R^-(x)
 \le C R^{1/2}M^{1/2}g^{3/2}.}
\tag{BG.5}
\]

现在令 \(u\in L_t^\infty L_x^2\cap L_t^2H_x^1\)，并在几乎每个
时间由 BG.1 定义压力。第一条界的常数与 \(R\) 无关，所以

\[
 \int_I\sup_{0<R<\pi/4}\sup_x
       \frac{\mathcal P_R^-(t,x)}R\,dt
 \le C\int_I\|\nabla u(t)\|_2^2\,dt<\infty .
\tag{BG.6}
\]

对几乎每个时间，\(p(t)\in L^3\)。\(K_R\) 的空间平移在
\(L^{3/2}\) 中连续，改变 \(R>0\) 也在该范数中连续；因此
\((R,x)\mapsto\mathcal P_R^-(t,x)\) 连续。时间可测性来自
\(p\) 的强可测 \(L^3\) 代表。BG.6 中的半径和中心上确界可等价地
先取有理 \(R\) 与环面的可数稠密点，故没有隐藏的不可测上确界。

对每个固定 \(R\)，第二条界还给

\[
 \int_I\left(R^{-1/2}\sup_x\mathcal P_R^-(t,x)\right)^{4/3}dt
 \le C\left(\sup_I\|u(t)\|_2\right)^{2/3}
       \int_I\|\nabla u(t)\|_2^2dt .
\tag{BG.7}
\]

所以现有能量给的是尺度一致的 \(L^1_t\)，或固定尺度的
\(L_t^{4/3}\)，而不是 \(L_t^\infty\)。它也没有赋予候选终点处
有限的左极限。严格早于最大光滑时间的真实光滑 NS 解当然逐时
连续；BG.6--BG.7 没有把这种局部光滑性统一延伸到候选终点。

## 2. 固定能量的真实负压力势可以任意大

取非负 \(\varphi\in C_c^\infty([0,\infty))\)，令它在零点附近
恒等于一且不恒为零，定义 Euclidean 紧支撑种子

\[
 V(y)=\varphi(|y|^2)(-y_2,y_1,0),
 \qquad C_2=\|V\|_2^2>0,
 \qquad C_1=\|\nabla V\|_2^2>0.
\tag{BG.8}
\]

径向性直接给 \(\operatorname{div}V=0\)，奇偶性给
\(\int_{\mathbb R^3}V=0\)，并且 \(y\cdot V(y)=0\)、\(V(0)=0\)。
令 \(\Gamma(y)=(4\pi|y|)^{-1}\)，以及取衰减规范的 Euclidean
压力

\[
 p_V=\partial_i\partial_j\Gamma*(V_iV_j).
\]

分布 Hessian 为

\[
 \partial_i\partial_j\Gamma
 =\operatorname{p.v.}\frac{3y_i y_j-|y|^2\delta_{ij}}
                         {4\pi|y|^5}
   -\frac13\delta_{ij}\delta_0 .
\tag{BG.9}
\]

对 \(p_V(0)\) 而言，delta 项因 \(V(0)=0\) 消失；其余积分在
原点可积。利用 \(y\cdot V=0\) 得到严格符号

\[
 p_V(0)
 =-\frac1{4\pi}\int_{\mathbb R^3}
       \frac{|V(y)|^2}{|y|^3}\,dy<0.
\tag{BG.10}
\]

由于 \(p_V\) 光滑，存在 \(\rho,c_V^->0\)，使
\(p_V(z)\le-c_V^-\) 于 \(B_\rho\)。固定 \(M_0>0\) 和
\(x_*\in\mathbb T^3\)。当 \(\epsilon\) 足够小，使一只泡完全
落在同一坐标球内时，令

\[
 u_\epsilon(x)=\frac{M_0}{\sqrt{C_2}}\epsilon^{-3/2}
 \sum_{k\in\mathbb Z^3}
 V\!\left(\frac{\widetilde x-\widetilde x_*+2\pi k}{\epsilon}\right).
\tag{BG.11}
\]

小支撑保证每点至多一个非零副本。于是 \(u_\epsilon\) 光滑、周期、
无散、零均值，并且

\[
 \|u_\epsilon\|_2=M_0,
 \qquad
 \|\nabla u_\epsilon\|_2^2
 =\frac{M_0^2C_1}{C_2}\epsilon^{-2}.
\tag{BG.12}
\]

令 \(\mathcal G_{\mathbb T}\) 为 \(-\Delta\) 的周期零均值 Green
函数。在当前差坐标邻域，分布意义下
\(\partial_i\partial_j\mathcal G_{\mathbb T}
=\partial_i\partial_j\Gamma+S_{ij}\)，其中 \(S_{ij}\) 光滑。
由 BG.1 的零均值规范和一次换元，周期压力满足

\[
 p_\epsilon(x_*+\epsilon z)
 =\frac{M_0^2}{C_2}\epsilon^{-3}p_V(z)+r_\epsilon(z),
 \qquad
 \|r_\epsilon\|_{L^\infty(B_\rho)}\le C_V M_0^2.
\tag{BG.13}
\]

这里 Euclidean 奇异部分精确产生 \(\epsilon^{-3}p_V\)；光滑
周期修正含振幅平方乘源体积，故只是 \(O(M_0^2)\)。对
\(\partial_i\partial_j\mathcal G_{\mathbb T}\) 作卷积已经固定了
零均值，未另加随 \(\epsilon\) 增长的压力常数。

因此，固定任意 \(R\in(0,\pi/4)\)，当
\(\epsilon\rho<R\) 且 \(\epsilon\) 足够小时，BG.10--BG.13 给

\[
 \mathcal P_R^-(x_*)
 \ge c M_0^2\epsilon^{-3}
       \int_{B_{\epsilon\rho}(x_*)}\frac{dy}{|y-x_*|}
 =c' M_0^2\epsilon^{-1}\longrightarrow\infty .
\tag{BG.14}
\]

每个固定的 \(u_\epsilon\) 与 \(p_\epsilon\) 都是光滑的，因而其
压力势在紧时间区间取为常值时有有限上界和左连续性；换言之，单个
静态场本身仍满足正在比较的条件 C 类型要求。BG.14 只否定一个
仅依赖固定 \(M_0\) 且对所有场一致的逐时常数。它不是一条 NS
轨道上的条件 C 反例。

## 3. 能量关系型时间族仍不产生端点控制

上一节的静态族还没有使用 \(\int g^2dt<\infty\)。下面构造一个
抽象时间族，把这个预算也完整保留。全局标量能量关系在本节按
黏性 \(\nu=1\) 归一化。固定 \(0<\alpha<1/2\)，并令

\[
 \epsilon(t)=\epsilon_0(T-t)^\alpha,
 \qquad c_V=\frac{C_1}{C_2},
 \qquad
 E'(t)=-2c_VE(t)\epsilon(t)^{-2},
 \qquad E(t_0)=E_0>0 .
\tag{BG.15}
\]

对任意固定 \(\nu>0\)，只需把 BG.15 中的 \(c_V\) 替换为
\(\nu c_V\)，后面的标量能量关系相应带 \(2\nu\)；核心非 NS
验证中的第一项也变为 \(-\nu c_V\epsilon^{-2}\)，结论不变。

取 \(t_0<T\) 与 \(\epsilon_0\) 使全部泡位于同一小坐标球。
因为 \(2\alpha<1\)，\(\int_{t_0}^T\epsilon(t)^{-2}dt<\infty\)，
所以 \(E(t)\) 下降到严格正的极限 \(E_*>0\)。用 BG.11 的同一
周期化约定定义

\[
 U(t,x)=\sqrt{\frac{E(t)}{C_2}}\,\epsilon(t)^{-3/2}
 \sum_{k\in\mathbb Z^3}
 V\!\left(\frac{\widetilde x-\widetilde x_*+2\pi k}{\epsilon(t)}\right),
 \quad t<T,
 \qquad U(T)=0 .
\tag{BG.16}
\]

逐时仍有零均值和无散性，并且

\[
 \|U(t)\|_2^2=E(t),
 \qquad
 \|\nabla U(t)\|_2^2=c_VE(t)\epsilon(t)^{-2},
\]

从而对 \(t_0\le s<t<T\) 有精确全局标量能量关系

\[
 \|U(t)\|_2^2+2\int_s^t\|\nabla U(\sigma)\|_2^2d\sigma
 =\|U(s)\|_2^2.
\tag{BG.17}
\]

跨到终点时则有

\[
 \|U(T)\|_2^2+2\int_s^T\|\nabla U(\sigma)\|_2^2d\sigma
 =E(s)-E_*\le E(s).
\tag{BG.18}
\]

因此 \(U\in L_t^\infty L_x^2\cap L_t^2H_x^1\)，并满足相应的
全局标量能量不等式。对任意 \(\zeta\in L^2(\mathbb T^3)\)，

\[
 |\langle U(t),\zeta\rangle|
 \le \sqrt{E(t)}\,
       \|\zeta\|_{L^2(B_{C\epsilon(t)}(x_*))}
 \longrightarrow0 .
\tag{BG.19}
\]

故 BG.16 在 \(T\) 取零以后属于
\(C_w([t_0,T];L^2)\)；在每个 \(t<T\) 处则强连续。按 BG.1
逐时定义它的真实周期零均值压力，BG.13--BG.14 同样给

\[
 \mathcal P_R^-(t,x_*)
 \ge c\frac{E(t)}{\epsilon(t)}\longrightarrow\infty,
 \qquad
 \mathcal P_R^-(T,x_*)=0 .
\tag{BG.20}
\]

所以基本能量空间、弱连续代表、全局标量能量不等式与瞬时压力
Poisson 关系合在一起，仍不推出时间一致压力势或候选终点的有限
左连续迹。

这个时间族不是 NS 解。事实上，由 \(\varphi=1\) 于零点附近，
在泡核心有

\[
 U(t,x)=A(t)(-(x_2-x_{*,2}),x_1-x_{*,1},0),
 \qquad
 A(t)=\sqrt{\frac{E(t)}{C_2}}\,\epsilon(t)^{-5/2}.
\tag{BG.21}
\]

相应涡量为 \(\omega=2A(t)e_3\)，并在核心逐点满足

\[
 \Delta\omega=0,\qquad
 (U\cdot\nabla)\omega=0,\qquad
 (\omega\cdot\nabla)U=0,
 \qquad
 \frac{A'}A=-c_V\epsilon^{-2}
                +\frac{5\alpha}{2(T-t)}.
\tag{BG.22}
\]

因 \(2\alpha<1\)，最后一式在充分接近 \(T\) 时严格为正。
NS 涡量方程在该核心会要求 \(\partial_t\omega=0\)，所以 BG.16
明确不满足 NS；压力无法修复取 curl 后的这个矛盾。本稿也没有
声称 BG.16 满足局部能量不等式、suitable 条件或任何弱 NS 方程。

## 4. 结论边界

BG.5--BG.7 是正面的能量类结论：归一化局部负压力势在时间上
可积，并在几乎每个时间有限。BG.14 与 BG.20 则严格说明，不能只
从这些能量数据推到条件 C 类型的 \(\sup_t\sup_x\) 控制和终点
左连续性。

单泡压缩与周期 Green 光滑修正复用 AH 的技术，不作新颖性声明。
这里新增的窄信息只是：一个显式旋转种子给出真实 \(p_-\) 的局部
压力势下界；AH 检查的是 moderator residual，并没有给出这个符号
结论。静态族只排除 \(M\)-only 的统一常数，真正破坏端点条件的
时间族不满足 NS。因此，真实 NS 动力学是否额外强制文献条件仍然
OPEN，移动缩球合同 G 也没有减少未证输入。

这项 energy-only candidate 到此停止；不自动续写相邻压力范数或
截止变体。无仿真、科学图、DGX 或 Clay 结论。
