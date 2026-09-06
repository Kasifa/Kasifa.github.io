# 压力功中的速度方向：精确结构与临界缺口

2026-09-06。**LOCAL DERIVATION / LITERATURE / CONDITIONAL / G OPEN / NOT CLAY。**
本稿已完成内部实际文件独立复核，范围见本包审计记录。
沿用黏性 1、无外力周期 NS 及原速度，
不改变合同 G 的初值类别或尺度依赖路径。
我在这里核查方向结构能提供什么，不把附加的方向条件当成已有能量界。

## 1. 非零集上的方向与加权零集约定

对一个光滑时间，记 \(q=|u|\)，\(\Omega_+=\{q>0\}\)，
仅在该开集上定义 \(e=u/q\)。令
\[
 D_r=\int q|\nabla q|^2,\qquad
 D_\theta=\int_{\Omega_+}q^3|\nabla e|^2,\qquad
 Z_e=\int_{\Omega_+}q^3(\operatorname{div}e)^2.
\tag{AC.1}
\]
这些是整个环面的积分。逐列微分给
\(\partial_j u=e\,\partial_jq+q\,\partial_j e\)，
且 \(e\cdot\partial_j e=0\)，所以
\[
 q^3|\nabla e|^2
 =q|\nabla u|^2-q|\nabla q|^2\ge0,\qquad
 D:=\int q\bigl(|\nabla u|^2+|\nabla q|^2\bigr)=2D_r+D_\theta.
\tag{AC.2}
\]
右侧密度在 \(q=0\) 上取零，受 \(q|\nabla u|^2\) 支配。
这给出合法加权延拓，不表示 e 是跨零集的普通 Sobolev 场。
同理 \(q|\nabla q|^2=\sum_j(u\cdot\partial_j u)^2/q\)
在非零集成立，零集上取零。

由无散性，在 \(\Omega_+\) 上有
\[
 q\operatorname{div}e=-e\cdot\nabla q=:F,\qquad
 W:=\int p\,u\cdot\nabla q
 =-\int_{\Omega_+}p q^2\operatorname{div}e
 =-\int p q F.
\tag{AC.3}
\]
F 在零速度集上定义为零。这里使用加权点态恒等式，
不对可能奇异的 \(\operatorname{div}e\) 作跨零集分部积分。
如需全域极限，取 \(q_\epsilon=(q^2+\epsilon^2)^{1/2}\)、
\(e_\epsilon=u/q_\epsilon\)，则
\(-q_\epsilon^2\operatorname{div}e_\epsilon=u\cdot\nabla q_\epsilon\)。
由 \(|u\cdot\nabla q_\epsilon|\le q|\nabla u|\) 支配收敛恢复 AC.3。
并且 \(|F|\le|\nabla u|\)，所以 F 的这个可测代表没有方向除零的问题。

## 2. 径向与角向耗散究竟提供多少控制

设矩阵 \(A_{ij}=\partial_j e_i\)。由 \(e^TA=0\)，
\[
 \operatorname{div}e=(I-e\otimes e):A,\qquad
 |\operatorname{div}e|^2\le2|\nabla e|^2.
\tag{AC.4}
\]
常数 2 来自三维正交投影 \(I-e\otimes e\) 的 Frobenius 范数平方；
这是点态线性代数，不是 NS 的新耗散机制。
另一方面，AC.3 给
\(q^2(\operatorname{div}e)^2\le|\nabla q|^2\)。因此
\[
 Z_e\le \min\{D_r,2D_\theta\},\qquad
 Z_e\le\frac25D,\qquad
 |W|\le\left(\int p^2q\right)^{1/2} Z_e^{1/2}.
\tag{AC.5}
\]
最后一个不等式是对 AC.3 作加权 Cauchy--Schwarz。
\(2/5\) 只改善常数，不解决大临界范数。

令 \(L=\|u\|_3\)。沿 AB.6 的压力估计与
\(|u|^{3/2}\) 的周期 Sobolev 界，
\[
 |W|\le CL(D_r^{1/2}+L^{3/2})
             \min\{D_r^{1/2},\sqrt2D_\theta^{1/2}\}.
\tag{AC.6}
\]
这保留了径向或角向部分很小时的额外信息。
但最坏情形仍有 \(CLD_r\) 或 \(CL\sqrt{D_rD_\theta}\)；
没有由原方程推出比例小性，就不能吸收。
下一份压力符号源还构造了 \(W>0\) 和 \(W<0\) 的光滑无散初值，
所以也不能直接假定 W 具有有利符号。

## 3. 已有方向准则不是无条件结论

这里仅核对一篇直接相关原稿：
[Vasseur, Regularity criterion for 3D Navier-Stokes equations in terms of the direction of the velocity](https://web.ma.utexas.edu/users/vasseur/documents/preprints/NSdirection2.pdf)，
作者稿日期 2007-04-25，Theorem 1（第2页）、式(3)及第3--5页证明。
arXiv 编号为 0705.2446。主级读取了该作者稿全部6页。

原定理在 \(\mathbb R^3\) 的 Leray--Hopf 类中，要求
\[
 \operatorname{div}(u/|u|)\in L^a_tL^b_x,\qquad
 \frac2a+\frac3b\le\frac12,\quad a\ge4,\quad b\ge6.
\tag{AC.7}
\]
它不是周期定理的字面表述。该未加权方向量的尺度临界线是
\(2/a+3/b=1\)，故 AC.7 是更强的次临界条件。
原稿未单独规定速度零集上的方向定义；本稿不直接导入其未加权分布量，
而使用 AC.3 明确定义的 F。
原证明的中间量就是这种加权流线变化，并要求它有适当的临界可积性。
因此下面的周期估计是该证明思路的一个本地特例，不作新颖性声明。

## 4. 能量只给 F 的较弱可积性

对同一个有限能量解，
\[
 \int_0^{T_*}\|F(t)\|_2^2\,dt
 \le\int_0^{T_*}\|\nabla u(t)\|_2^2\,dt<\infty.
\tag{AC.8}
\]
F 的尺度为长度的负二次方；相应临界线为
\(2/a+3/b=2\)。AC.8 的指数和是 \(5/2\)，不是 2。
下面将 \(\|F\|_{L_t^2L_x^3}\) 作为明确的附加条件核查；
没有从 AC.8 得到这个条件。

**条件接口。** 设一个光滑周期解存在于 \([0,T)\)，\(T<\infty\)。
固定 \(0<t_0<T\)。若
\[
 \int_{t_0}^T \|F(t)\|_3^2\,dt<\infty,
\tag{AC.9}
\]
则该解可光滑延拓越过 T。结论只在附加条件 AC.9 下成立。

证明：令 \(\beta(t)=\|F(t)\|_3\)，\(H=L^3/3\)。
周期压力取零均值；Hölder 指数 \(9/4,9/2,3\) 和双 Riesz 界给
\[
 \begin{aligned}
 |W|
 &\le \|p\|_{9/4}\|u\|_{9/2}\beta
 \le C\beta\|u\|_{9/2}^3\\
 &\le C\beta L^{3/2}\|u\|_9^{3/2}
 \le C\beta L^{3/2}(D_r^{1/2}+L^{3/2})\\
 &\le \eta D_r+C_\eta(\beta+\beta^2)H .
 \end{aligned}
\tag{AC.10}
\]
保留低阶项是周期域上的必要步骤。
取 \(0<\eta<2\)，由 \(H'+2D_r+D_\theta=W\)，Gronwall 得
\[
 \sup_{t_0<t<T}H(t)<\infty,\qquad
 \int_{t_0}^T(D_r+D_\theta)\,dt<\infty,\qquad
 \int_{t_0}^T\|u(t)\|_9^3\,dt<\infty .
\tag{AC.11}
\]
有限时间上 \(\beta+\beta^2\) 可积；最后一式用
\(\|u\|_9^3\le C(D_r+L^3)\)。

为明确周期延拓接口，对原方程与 \(-\Delta u\) 配对。
记 \(Y=\|\nabla u\|_2^2\)。压力消失，且
\[
 \left|\int (u\cdot\nabla)u\cdot\Delta u\right|
 \le \|u\|_9\|\nabla u\|_{18/7}\|\Delta u\|_2
 \le C\|u\|_9Y^{1/3}\|\Delta u\|_2^{4/3}
 \le\frac12\|\Delta u\|_2^2+C\|u\|_9^3Y .
\tag{AC.12}
\]
这里 \(\nabla u\) 均值为零，周期 Sobolev 和椭圆界给
\(\|\nabla u\|_6\le C\|\Delta u\|_2\)，
再与 L² 插值得到中间指数 \(18/7\)。
故 \(Y'/2+\|\Delta u\|_2^2/2\le C\|u\|_9^3Y\)，
AC.11 给一致 H¹ 上界。
最后调用标准周期次临界 H¹ 局部存在与延拓，
其共同寿命依赖该 H¹ 上界和固定黏性，不依赖接近 T 的重启时刻。
这排除有限终点 T。该局部理论是文献背景，不是这里重证的结果；
参见 [Tao, Notes 1, Remark 46 的次临界范围说明](https://terrytao.wordpress.com/2018/09/16/254a-notes-1-local-well-posedness-of-the-navier-stokes-equations/)。
不能把同页只陈述 \(s>3/2\) 的 Theorem 38 直接当作 H¹ 定理。

## 5. 光滑解也可能有不可积的未加权方向散度

一个无需仿真的精确检查是
\[
 u(t,x,y,z)=e^{-2t}(\sin x\cos y,-\cos x\sin y,0),\qquad
 p(t,x,y,z)=\frac{e^{-4t}}4(\cos2x+\cos2y).
\tag{AC.13}
\]
直接求导得 \(\operatorname{div}u=0\)、\(\partial_tu=\Delta u\)，
\((u\cdot\nabla)u=(e^{-4t}/2)(\sin2x,\sin2y,0)=-\nabla p\)。
因此它是全时光滑、零均值的周期 NS 解。

在零线 \((0,0,z)\) 附近，令 \(r=(x^2+y^2)^{1/2}\)，则对固定 t，
\[
 q=e^{-2t}r(1+O(r^2)),\quad
 e=(x,-y,0)/r+O(r^2),\quad
 \operatorname{div}e=(y^2-x^2)/r^3+O(r).
\tag{AC.14}
\]
这些余项来自解析三角函数的 Taylor 展开，方向误差的一阶导数为 O(r)。
在 \(|y^2-x^2|\ge r^2/2\) 的固定角锥内，
\(|\operatorname{div}e|\ge c/r\)。
沿零线有正长度的 z 区间，因此其空间 \(L^b\) 积分含
\(\int_0^\epsilon r^{1-b}dr\)，对所有 \(b\ge2\) 发散。
零集上的任意赋值不能改变零集外的这个发散。

这说明同型的未加权方向条件不是周期光滑性的必要条件，
周期光滑性甚至不推出方向散度的局部 \(L^b\) 可积性（\(b\ge2\)）。
由于定义域不同，此例不判定 Vasseur 的全空间条件在其原类中是否必要。
它不是对该充分准则的反例，更不是 NS 奇点。
加权 F 满足 \(|F|\le|\nabla u|\)，在这个解中则有界。
不能因为未加权方向量在零点很差，就认定速度本身不光滑。

## 6. 对当前问题的含义

压力功的方向重写是已有结构；它既不自动有利，也不自动带来临界控制。
已得到的条件接口将缺口准确落到 F 的额外时空可积性，
并避免未加权方向量在低速零点的伪障碍。
但 AC.9 仍未由一般 NS 初值与能量推出，合同 G 仍未完成。
这些全环面恒等式也没有支付固定 cutoff 的外壳或原移动路径的几何误差。

本节无有限计算、数值证书、DGX 或科学图需求；没有新读者 PDF。
解析恒等式、显式例子及条件接口均不包含发表等级或新颖性承诺。
