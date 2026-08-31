# R0.73V | A pressure-aware signed third-order heat lift: exact scale generation and the 3→4 physical-time boundary

**Status:** analytic proof, independent sign/index readback, the two-path
exact-certificate final seal, and the formal-figure source seal passed;
bilingual HTML/PDF and public deployment remain separate release gates

**Public title (zh):** R0.73V｜压力感知的有符号三阶热提升：精确尺度生成律与 3→4 物理时间边界

**Date:** 2026-09-01

**Audience:** researchers and technically trained readers following the
periodic three-dimensional Navier--Stokes notes

**Scope:** an exact pressure-aware signed third-order heat lift, the complete
Germano second-stress ledger, conditional critical flux rows, an exact scalar
trace projection, bottom-scale order separation, and finite Fourier
coefficient certificates; no finite physical-time closure or arbitrary-data
global regularity claim

**Normalization:** \(\mathbb T^3=[0,2\pi]^3\) carries normalized Haar measure
\(d\mu=(2\pi)^{-3}dx\); viscosity is \(\nu>0\)

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `FALSE`

## 1. 直接结论

R0.73U 证明了：完整局部二次张量可以恢复瞬时压力，但偶二次状态不能
单值决定带符号的张量时间切向量。R0.73V 处理这个缺口的下一层。我先把
Navier--Stokes 非线性连同压力一起写成

\[
 \mathcal B(a,b)=\mathbb P\nabla\!\cdot(a\otimes b),
 \qquad N=\mathcal B(u,u)=(u\cdot\nabla)u+\nabla p.
 \tag{1.1}
\]

令

\[
 P_s=e^{s\Delta},\qquad v_s=P_su,\qquad
 \Theta_s=P_s(u\otimes u),\qquad N_s=P_sN,
 \tag{1.2}
\]

并以 \(a\odot b=a\otimes b+b\otimes a\) 记对称张量积。R0.73V 的
方程槽压缩对象是

\[
 \boxed{
 \mathcal C_s=P_s(u\odot N),\qquad
 \chi_s=\mathcal C_s-v_s\odot N_s.}
 \tag{1.3}
\]

这里“压力感知”只表示 \(N\) 已经包含 Leray/Riesz 压力贡献。“方程槽
压缩”表示 \(\chi_s\) 正好进入 R0.73U 的二次张量方程。它不表示
信息论最小、分量最小、唯一或稳定可逆。

这一节得到五条结论。

**[内部精确，已独立审计]** 第一，\(\chi_s\) 满足精确 heat 尺度生成律

\[
 \boxed{
 (\partial_s-\Delta)\chi_s
 =2\sum_\ell\partial_\ell v_s\odot\partial_\ell N_s,
 \qquad \chi_0=0.}
 \tag{1.4}
\]

它把二次张量 heat-plane 方程写成

\[
 \boxed{
 (\partial_t-\nu\partial_s)\Theta_s
 =-2\nu G_s-v_s\odot N_s-\chi_s,}
 \qquad
 G_s=P_s\sum_\ell\partial_\ell u\otimes\partial_\ell u.
 \tag{1.5}
\]

**[经典公式，当前符号已独立核对]** 第二，展开为 Germano 的透明账本后，
完整二阶 stress 方程不只含速度三阶 cumulant \(\kappa_s\)，还含
压力--速度 covariance \(Q_s\)、压力--应变 covariance \(R_s\)、
梯度 covariance 和 resolved production。只保留 \(\kappa_s\) 会漏项。

**[条件性推论，已独立审计]** 第三，若已经假设经典临界强范数
\(u\in L_t^4L_x^6\)，则 \(\kappa_s\) 与 \(Q_s\) 进入
\(L_t^{4/3}L_x^2\) 通量行。取 stress 方程的一半迹后，\(R_{ii,s}\)
严格消失，完整标量三阶通量也进入这一行。不过方程仍保留带符号的
production \(-\tau_s:\nabla v_s\)，而且临界估计仍以强范数为前提。

**[内部精确，已独立审计]** 第四，在物理时间中，原始三阶矩和
\(\mathcal C_s\) 的方程都出现四次速度项。这证明的是这些自然
三阶提升进入 \(3\to4\) 层，不是“四阶不闭合”，更不是所有有限层级
都不可能闭合。

**[精确有限证书，已封印]** 第五，两个互不导入的标准库实现通过
66 项锁定检查。在四站点场的同一 Fourier 系数上，速度三阶 cumulant
通量为 \(O(s^2)\)，完整压力源为 \(O(s)\)。因此不能用一个
\(s\)-一致的系数把该压力源吸收到该 cumulant 通量中；这个选定系数
至少付出 \(s^{-1}\) 代价。证书还给出一个非零四次 next-level
remainder，但它不证明全场信息碰撞或有限层级 no-go。

**[开放]** 这些结果没有从能量类推出 \(L_t^4L_x^6\)，也没有控制
压力--应变导数行、零 heat 尺度或 \(-\tau_s:\nabla v_s\)。任意三维
初值的全局正则性和 Clay 千禧年问题仍然开放。

## 2. 方程槽压缩提升与精确尺度生成律

heat 半群与导数及周期 Leray 投影交换，因此

\[
 \boxed{N_s=\mathbb P\nabla\!\cdot\Theta_s.}
 \tag{2.1}
\]

这一步很重要：已知完整 \(\Theta_s\) 时，不需要反演 heat flow 就能在
同一尺度求出 \(N_s\)。但 \(P_s(u\odot N)\) 不是
\(v_s\odot N_s\)，二者的差正是 \(\chi_s\)。

对固定物理时刻的两个场 \(f,g\)，定义 heat covariance

\[
 \tau_s(f,g)=P_s(fg)-P_sf\,P_sg.
 \tag{2.2}
\]

普通 Laplacian 乘积法则给出

\[
 (\partial_s-\Delta)\tau_s(f,g)
 =2\nabla P_sf\cdot\nabla P_sg,
 \qquad \tau_0(f,g)=0.
 \tag{2.3}
\]

逐分量取 \((f,g)=(u_i,N_j)\) 并对称化，就得到式 (1.4)。其 Duhamel
形式为

\[
 \boxed{
 \chi_s=2\int_0^sP_{s-r}\left[
 \sum_\ell\partial_\ell v_r\odot\partial_\ell N_r
 \right]dr.}
 \tag{2.4}
\]

因为 \(N_r=\mathbb P\nabla\cdot\Theta_r\)，式 (2.4) 使用的是
\((v_r,\Theta_r)_{0\le r\le s}\) 的较小尺度路径。它是向下三角的
尺度恒等式，不是只依赖一个正尺度的代数本构律，也不是物理时间闭合。

另一方面，\(\partial_tu=\nu\Delta u-N\) 给出

\[
 \partial_t(u\otimes u)
 =\nu\Delta(u\otimes u)
 -2\nu\sum_\ell\partial_\ell u\otimes\partial_\ell u
 -u\odot N.
 \tag{2.5}
\]

对它施加 \(P_s\)，便得到式 (1.5)。这说明 \(\chi_s\) 精确填入奇次
三阶槽，但偶次梯度矩 \(G_s\) 仍在。若保留全部 heat 尺度路径，
R0.73U 的 covariance 方程还给出

\[
 G_s={1\over2}P_s\left[
 \left.\partial_r\tau_r\right|_{r=0}\right].
 \tag{2.6}
\]

这是一个底尺度导数公式。它不能被改写成稳定的单正尺度闭合。

## 3. 透明的三阶 cumulant 与完整压力账本

为了看清 \(\chi_s\) 压缩了什么，先定义原始三阶局部矩

\[
 M_{ijk,s}=P_s(u_i u_j u_k),
 \tag{3.1}
\]

以及第三 generalized heat cumulant

\[
 \begin{aligned}
 \kappa_{ijk,s}={}&M_{ijk,s}
 -v_{s,i}\Theta_{jk,s}-v_{s,j}\Theta_{ik,s}
 -v_{s,k}\Theta_{ij,s}\\
 &+2v_{s,i}v_{s,j}v_{s,k}.
 \end{aligned}
 \tag{3.2}
\]

三因子乘积法则中，所有含一个未求导 \(v_s\) 的项恰好抵消，留下

\[
 \boxed{
 \begin{aligned}
 (\partial_s-\Delta)\kappa_{ijk,s}=2\sum_\ell\big(&
 \partial_\ell v_{s,i}\,\partial_\ell\tau_{jk,s}
 +\partial_\ell v_{s,j}\,\partial_\ell\tau_{ik,s}\\
 &+\partial_\ell v_{s,k}\,\partial_\ell\tau_{ij,s}\big),
 \qquad \kappa_{ijk,0}=0.
 \end{aligned}}
 \tag{3.3}
\]

这也是精确的 heat 尺度方程。限定式检索没有找到完全相同的公开写法，
但“未检出”不支持新颖性、优先权或第一性声明。

压力不能从完整 stress 方程中省略。记

\[
 Q_{i,s}=\tau_s(p,u_i),\qquad
 R_{ij,s}=\tau_s(p,S_{ij}),\qquad
 S_{ij}=\tfrac12(\partial_i u_j+\partial_j u_i),
 \tag{3.4}
\]

并令

\[
 D_{ij,s}=\sum_k\tau_s(\partial_k u_i,\partial_k u_j).
 \tag{3.5}
\]

它们的尺度方程是

\[
 \boxed{
 (\partial_s-\Delta)Q_{i,s}
 =2\nabla p_s\cdot\nabla v_{s,i},
 \qquad Q_{i,0}=0,}
 \tag{3.6}
\]

\[
 \boxed{
 (\partial_s-\Delta)R_{ij,s}
 =2\nabla p_s\cdot\nabla S_{ij}(v_s),
 \qquad R_{ij,0}=0.}
 \tag{3.7}
\]

Germano 1992 的 generalized-central-moment 方程在本节 heat filter 与
符号约定下成为

\[
 \boxed{
 \begin{aligned}
 \partial_t\tau_{ij,s}+\partial_k(v_{s,k}\tau_{ij,s})
 ={}&-\partial_k\!\left(
 \kappa_{ijk,s}+Q_{i,s}\delta_{jk}+Q_{j,s}\delta_{ik}
 -\nu\partial_k\tau_{ij,s}\right)\\
 &+2R_{ij,s}-2\nu D_{ij,s}
 -\tau_{ik,s}\partial_kv_{s,j}
 -\tau_{jk,s}\partial_kv_{s,i}.
 \end{aligned}}
 \tag{3.8}
\]

式 (3.8) 是这节最重要的边界之一：\(\kappa_s\) 单独不是完整的三阶
接口；删掉 \(Q_s\) 或 \(R_s\) 会把精确方程写错。但“一个展开漏项”
不等于“这些项不可能从任何其他全场状态重建”。R0.73V 没有得到后一种
信息论 no-go。

压缩表示与透明表示在固定的低阶状态上相容。具体地，

\[
 \mathcal C_{ij,s}
 =\partial_kM_{kij,s}
 +P_s(u_i\partial_jp+u_j\partial_ip)
 =v_s\odot N_s+\chi_s.
 \tag{3.9}
\]

也可以把压力梯度单独居中为

\[
 \rho_s=P_s(u\odot\nabla p)-v_s\odot\nabla p_s,
 \tag{3.10}
\]

它满足

\[
 (\partial_s-\Delta)\rho_s
 =2\sum_\ell\partial_\ell v_s\odot
 \partial_\ell\nabla p_s,
 \qquad \rho_0=0.
 \tag{3.11}
\]

\((\kappa_s,Q_s,R_s)\) 适合检查完整 stress 的每个来源，\(\chi_s\)
适合填入二次张量方程的一个对称槽。两者是不同用途的精确表示，不能据此
宣称其中任何一个唯一或全局最小。

## 4. 条件性临界行与精确 trace 投影

令平滑寿命内的区间 \(I\) 上

\[
 E(I)=L^4(I;L^6(\mathbb T^3)).
 \tag{4.1}
\]

heat contraction、H\"older 与周期 Riesz 有界性给出

\[
 \boxed{
 \sup_{s\ge0}\|\kappa_s\|_{L_t^{4/3}L_x^2(I)}
 \le C_\kappa\|u\|_{E(I)}^3,}
 \tag{4.2}
\]

\[
 \boxed{
 \sup_{s\ge0}\|Q_s\|_{L_t^{4/3}L_x^2(I)}
 \le2C_R\|u\|_{E(I)}^3.}
 \tag{4.3}
\]

这两个指数与前面的 critical Stokes interface 相容，但右端已经假设
\(u\in L_t^4L_x^6\)。所以它们对任意能量初值的全局正则性是循环的。
同一个无导数论证不能把 \(R_s\)、\(\rho_s\) 或 \(\chi_s\) 放入
式 (4.2)--(4.3)；这些对象显式带有速度或压力导数。

完整张量方程有一个精确而有用的标量投影。令

\[
 k_s={1\over2}\operatorname{tr}\tau_s,
 \qquad
 J_{k,s}={1\over2}\kappa_{iik,s}+Q_{k,s}.
 \tag{4.4}
\]

由于不可压缩性给出
\(R_{ii,s}=\tau_s(p,S_{ii})=0\)，式 (3.8) 的一半迹是

\[
 \boxed{
 \partial_t k_s+\partial_k(v_{s,k}k_s)
 =-\partial_k\big(J_{k,s}-\nu\partial_k k_s\big)
 -\nu D_{ii,s}-\tau_{ik,s}\partial_kv_{s,i}.}
 \tag{4.5}
\]

heat-kernel covariance 不等式给出

\[
 D_{ii,s}=\sum_{i,k}\left[
 P_s((\partial_ku_i)^2)-(\partial_kv_{s,i})^2\right]\ge0.
 \tag{4.6}
\]

同时，式 (4.2)--(4.3) 推出

\[
 \boxed{
 \sup_{s\ge0}\|J_s\|_{L_t^{4/3}L_x^2(I)}
 \le C_J(1+C_R)\|u\|_{E(I)}^3.}
 \tag{4.7}
\]

这个 trace 投影准确地移除了 pressure--strain，而不是把压力忽略掉；
压力--速度 covariance 已进入完整通量 \(J_s\)。但是最后一项

\[
 -\tau_{ik,s}\partial_kv_{s,i}=-\tau_s:\nabla v_s
 \tag{4.8}
\]

没有固定符号。它就是下一阶段最窄的标量障碍。式 (4.5) 不是正则性
判据，式 (4.7) 也仍然是条件性的。

## 5. 物理时间中的 3→4 边界

heat 尺度方向是向下三角的，但沿 Navier--Stokes 物理时间不是这样。
对原始三阶矩直接求导，得到

\[
 \boxed{
 \begin{aligned}
 (\partial_t-\nu\partial_s)M_{ijk,s}
 ={}&-2\nu P_s\sum_\ell\Big[
 u_k\partial_\ell u_i\partial_\ell u_j
 +u_j\partial_\ell u_i\partial_\ell u_k\\
 &\hspace{40mm}
 +u_i\partial_\ell u_j\partial_\ell u_k\Big]\\
 &-P_s\Big[N_i u_j u_k+u_iN_j u_k+u_i u_jN_k\Big].
 \end{aligned}}
 \tag{5.1}
\]

因为 \(N=\mathcal B(u,u)\) 是二次的，最后一行是四次速度项。

对压缩对象，定义

\[
 \mathcal R_4=\mathcal B(N,u)+\mathcal B(u,N),
 \qquad
 \mathcal S_3=\sum_\ell\mathcal B(\partial_\ell u,\partial_\ell u).
 \tag{5.2}
\]

这里 \(\mathcal R_4\) 自身是三次，标签表示它与 \(u\) 的乘积进入四次
行；\(\mathcal S_3\) 自身是二次。双线性直接计算给出

\[
 \partial_tN=\nu\Delta N-2\nu\mathcal S_3-\mathcal R_4,
 \tag{5.3}
\]

从而

\[
 \boxed{
 \begin{aligned}
 (\partial_t-\nu\partial_s)\mathcal C_s
 =-P_s\Big\{&N\odot N+u\odot\mathcal R_4\\
 &+2\nu\big[
 \sum_\ell\partial_\ell u\odot\partial_\ell N
 +u\odot\mathcal S_3\big]\Big\}.
 \end{aligned}}
 \tag{5.4}
\]

式 (5.4) 第一行是明确的四次层。居中后的 \(\chi_s\) 只是重新组织
这些项：

\[
 \begin{aligned}
 (\partial_t-\nu\partial_s)\chi_s
 ={}&(\partial_t-\nu\partial_s)\mathcal C_s
 +N_s\odot N_s\\
 &+v_s\odot\mathbb P\nabla\!\cdot(2\nu G_s+\mathcal C_s).
 \end{aligned}
 \tag{5.5}
\]

所以 R0.73V 的自足结论只针对式 (5.1) 的原始 \(M_s\) 和式 (5.4)
的 \(\mathcal C_s\)：这些自然三阶观测量的时间方程进入四次层。我没有
写出一般 centered \(\kappa_s\) 的完整四阶索引账本；有限证书只检查
一个选定 \(\kappa\) 系数。这里不允许写成“四阶不闭合”、
“任何三阶状态都失败”或“有限矩层级 no-go”。

## 6. 底 heat 尺度的阶数分离

对光滑周期场，式 (2.3) 在 \(s\downarrow0\) 给出

\[
 \tau_s(f,g)
 =2s\sum_\ell\partial_\ell f\,\partial_\ell g+O(s^2).
 \tag{6.1}
\]

因此

\[
 Q_{i,s}=2s\sum_\ell\partial_\ell p\,\partial_\ell u_i+O(s^2),
 \qquad
 R_{ij,s}=2s\sum_\ell\partial_\ell p\,\partial_\ell S_{ij}+O(s^2).
 \tag{6.2}
\]

由式 (3.3)，\(\partial_s\kappa_{ijk,0}=0\)。再求一次导数得到

\[
 \boxed{
 \begin{aligned}
 \kappa_{ijk,s}=2s^2\sum_{\ell,m}\big[&
 \partial_\ell u_i\,\partial_\ell(
     \partial_m u_j\,\partial_m u_k)\\
 &+\partial_\ell u_j\,\partial_\ell(
     \partial_m u_i\,\partial_m u_k)\\
 &+\partial_\ell u_k\,\partial_\ell(
     \partial_m u_i\,\partial_m u_j)\big]+O(s^3).
 \end{aligned}}
 \tag{6.3}
\]

把 stress 方程中的完整 centered pressure source 记为

\[
 \mathfrak P_{ij,s}
 =-\partial_iQ_{j,s}-\partial_jQ_{i,s}+2R_{ij,s}.
 \tag{6.4}
\]

式 (6.2) 中的速度二阶导数恰好抵消，留下

\[
 \boxed{
 \mathfrak P_{ij,s}
 =-2s\sum_\ell\left[
 (\partial_i\partial_\ell p)(\partial_\ell u_j)
 +(\partial_j\partial_\ell p)(\partial_\ell u_i)
 \right]+O(s^2).}
 \tag{6.5}
\]

所以局部速度 cumulant 通量从 \(O(s^2)\) 开始，而 centered pressure
source 通常从 \(O(s)\) 开始。这里“通常”不是一个对每个场都非零的
定理；要得到比值结论，必须给出两个领先系数都不退化的具体见证。

压缩提升本身也从一阶开始：

\[
 \boxed{
 \chi_s=2s\sum_\ell
 \partial_\ell u\odot\partial_\ell N+O(s^2).}
 \tag{6.6}
\]

这个展开解释了为什么压力感知 cross-covariance 会自然出现在底尺度，
但它没有给出能量类导数估计。

## 7. 两路径精确证书说明了什么

有限包使用 Python 标准库和精确 Gaussian rational 多项式。主实现采用
稀疏指数字典，独立实现采用稠密截断多项式；二者不互相导入，并对完整
\(\kappa,Q,\Xi=2R\) 非零表的公共核心逐字节一致。最终封印通过
66/66 项检查。这里没有浮点数、GPU、DGX、PDE 时间积分或 Navier--Stokes
仿真。

### 7.1 四站点的 \(O(s^2)\) 对 \(O(s)\) 分离

取

\[
 u=(2\sin(x+y),\;2\sin x-2\sin(x+y),\;0),
 \qquad h_*=(1,2,0),\qquad q=e^{-s}.
 \tag{7.1}
\]

精确证书给出

\[
 -\widehat{\partial_k\kappa_{kij}}(h_*)
 =q^3(1-q^2)^2(q^2+2)
 \begin{pmatrix}2&-3&0\\-3&4&0\\0&0&0\end{pmatrix},
 \tag{7.2}
\]

\[
 -\widehat{\partial_iQ_j+\partial_jQ_i}(h_*)
 =q^3(1-q^2)
 \begin{pmatrix}4&2&0\\2&-8&0\\0&0&0\end{pmatrix},
 \tag{7.3}
\]

\[
 \widehat{\Xi}(h_*)
 =q^3(1-q^2)
 \begin{pmatrix}-4&0&0\\0&4&0\\0&0&0\end{pmatrix}.
 \tag{7.4}
\]

因此完整 pressure source 在该系数上是

\[
 q^3(1-q^2)
 \begin{pmatrix}0&2&0\\2&-4&0\\0&0&0\end{pmatrix},
 \tag{7.5}
\]

它为 \(O(s)\)，而式 (7.2) 为 \(O(s^2)\)。这严格排除了在这一
见证、这一输出系数上用 \(s\)-一致常数把 pressure source 吸收到
cumulant flux；至少需要 \(s^{-1}\) 系数代价。它不是整个场上的范数
下界，也没有比较两个完整 \(\kappa_s\) 状态。

### 7.2 压缩提升的精确系数

令

\[
 K=\begin{pmatrix}-2&1&0\\1&0&0\\0&0&0\end{pmatrix}.
 \tag{7.6}
\]

同一四站点场满足

\[
 \widehat{\mathcal C_s}(h_*)=-q^5K,
 \qquad
 \widehat{v_s\odot N_s}(h_*)=-q^3K,
 \qquad
 \widehat\chi_s(h_*)=(q^3-q^5)K.
 \tag{7.7}
\]

\(u\) 与 \(-u\) 的 \(\chi_s\) 差为 \(2(q^3-q^5)K\)。对整数覆盖
伸缩 \(u_L(x)=u(Lx)\)，在 \(s=\theta L^{-2}\) 上，其 Frobenius
大小为

\[
 2\sqrt6\,L(e^{-3\theta}-e^{-5\theta}).
 \tag{7.8}
\]

这是选定提升系数的一阶导数代价，不是普适闭合下界。

### 7.3 六站点的同输出压力见证

再取 R0.73T 的六站点场

\[
 u=(6\sin y-4\sin(x+y),\;4\sin x+4\sin(x+y),\;0).
 \tag{7.9}
\]

在输出 mode \(0\)，contracted \(\kappa\)-flux 与 \(Q\)-divergence
都为零，但

\[
 \widehat\Xi(0)
 =(1-q^4)\operatorname{diag}(-48,48,0).
 \tag{7.10}
\]

这证明的只是：同一个输出系数上的局部速度 cumulant flux 不能代替完整
压力 forcing。它不是两个全场状态的 collision，也不排除使用全场信息或
不稳定 inverse heat reconstruction。

### 7.4 一个非零四次 next-level remainder

在四站点场上，选定系数满足

\[
 \left.\partial_t\widehat\kappa_{112,s}(0,2,0)
 \right|_{\rm nonlinear}
 =2iq^2(1-q^2)^2.
 \tag{7.11}
\]

它在每个 \(0<s<\infty\) 上非零。独立有限 \(\varepsilon\) 插值在
\(q=1/2\) 提取出 \(9i/32\)，与形式多项式一致。这个结果只认证
所选三阶量的时间方程含一个非零四次 remainder；它不认证四阶不闭合，
也不认证所有有限矩层级都失败。

## 8. 文献归属与限定式检索

Germano 1992 是最直接的经典碰撞来源。其 generalized-central-moment
方程已经包含第三速度 cumulant、pressure--velocity、pressure--strain、
gradient covariance 与 production；本节的式 (3.8) 是 heat filter 下的
专门化与符号核对：
[DOI](https://doi.org/10.1017/S0022112092001733)。

经典二点与 structure-function 层级从 von K\'arm\'an--Howarth 1938
推进到 Hill 2001 的任意阶 exact equations：
[1938 DOI](https://doi.org/10.1098/rspa.1938.0013)，
[2001 DOI](https://doi.org/10.1017/S0022112001003949)。这些是二点增量
对象，不是本节的确定性局部 heat cumulant。

Eyink 1996/2006 研究 exact subgrid flux、locality 与 multiscale-gradient
expansion；Duchon--Robert 2000 以有符号三阶速度增量表达局部能量
defect：
[Eyink 1996](https://arxiv.org/abs/chao-dyn/9602018)，
[Eyink 2006 DOI](https://doi.org/10.1017/S0022112005007895)，
[DR DOI](https://doi.org/10.1088/0951-7715/13/1/312)。这些结果解释了
三阶有符号传递为何自然，但不提供完整 stress 的有限确定性闭合。

Zambrano--Duraisamy 2026 在 homogeneous isotropic turbulence 下，以
quasi-normal、Markovian 与 eddy-damping 假设建立二点闭合模型：
[DOI](https://doi.org/10.1017/jfm.2026.11485)。模型假设不能改写成一般
三维 Navier--Stokes 的确定性闭合定理。LMN 与 Fursikov moment chain
同样提供逐阶耦合背景，但它们是 ensemble/moment 理论，不是这里的有限
局部 heat 状态。

两轮限定式检索没有找到与式 (3.3) 完全相同的 third heat-cumulant
\(s\)-PDE，也没有找到有限局部 heat-moment state 的普适最小性或 no-go
定理。这只是有边界的 negative finding，不能写成不存在、首次、新颖性或
优先权证明。

## 9. 结果价值与下一步

我对 R0.73V 的判断是：它是一项严肃、可复核的结构性推进，但现在还不是
一条解决三维全局正则性的核心先验估计，也不足以单独支撑高水平纯数学期刊
所要求的主定理。

它的实际价值有三层。

1. **方程价值。** R0.73U 的“缺少奇次信息”现在被替换成一个精确对象
   \(\chi_s\)，并有完整 heat 尺度生成律和 tensor heat-plane 接口。
2. **排错价值。** Germano 账本和两个有限见证排除了“只加速度
   \(\kappa_s\) 就能写对完整 stress 方程”以及“压力行可被同阶、
   \(s\)-一致地吞进选定 cumulant 系数”这两条具体捷径。
3. **路线价值。** trace 投影严格消掉 \(R_{ii}\)，把下一步压缩为一个
   更具体的问题：能否在不预先假设 \(L_t^4L_x^6\) 的条件下，用 heat
   carré-du-champ、尺度积分或物理时间抵消支付
   \(-\tau_s:\nabla v_s\)。

下一阶段我会先沿 trace 方程工作，而不是继续机械地添加张量分量：

1. 为 \(-\tau_s:\nabla v_s\) 推导带尺度权重的精确积分表示，分离散度项、
   carré-du-champ 项与真正的 signed remainder，再检查它能否与
   \(-\nu D_{ii,s}\)、\(\nu\partial_s\tau_s\) 或 Stokes smoothing 在
   \((t,s)\) 积分后形成可支付的组合；
2. 只接受不以 \(L_t^4L_x^6\) 为前提的能量类估计作为实质推进，并检查
   \(s\downarrow0\) 的一致性与光滑近似传递；若候选不等式失败，就构造
   精确 Fourier 反例并记录失败边界。

这条路线的真正门槛不是再写一个高阶恒等式，而是从能量类获得新的、
非循环的符号控制。这个门槛目前仍未跨过。

现阶段准确的 release ledger 是：

```text
problemFreeze=COMPLETE
parentAnalyticDerivation=COMPLETE
independentAnalyticAudit=PASS
primaryLiteratureAudit=BOUNDED_COMPLETE
pressureAwareSignedHeatLift=INTERNAL_EXACT_AUDITED
signedCrossCovarianceScalePDE=INTERNAL_EXACT_AUDITED
tensorHeatPlaneOddSlot=INTERNAL_EXACT_AUDITED
germanoStressEquation=VERIFIED_CLASSICAL_INDEX_AUDITED
conditionalKappaCriticalRow=INTERNAL_CONDITIONAL_AUDITED
conditionalPressureVelocityCriticalRow=INTERNAL_CONDITIONAL_AUDITED
scalarTraceEquation=INTERNAL_EXACT_AUDITED
conditionalScalarFluxRow=INTERNAL_CONDITIONAL_AUDITED
pressureStrainCriticalRow=OPEN
signedProductionEnergyControl=OPEN
rawAndCompressedThreeToFour=INTERNAL_EXACT_AUDITED
bottomScaleOrderSeparation=INTERNAL_EXACT_AUDITED
fourSiteCoefficientOrderSeparation=INTERNAL_EXACT_FINITE_SEALED
sixSiteSameOutputPressureWitness=INTERNAL_EXACT_FINITE_SEALED
selectedQuarticNextLevelRemainder=INTERNAL_EXACT_FINITE_SEALED
formalFiniteCertificate=PASS
formalFiniteCertificateChecks=66
analyticSourceCommit=25636c886f1ee2449418b5548b42f9f0fa269b47
certificateSourceCommit=7c445c522a241bdc8b867b6fce0f0fed9b82e97d
finitePackageCommit=b34d91ea96c257b943f11d134e8024138e5f3cb0
finalSeal=TRUE
formalFigurePackage=PASS
formalFigureChecks=147
formalFigureRows=158
figureSourceCommit=f94915332ff405ae723711e8041acc2af07e896b
figurePackageCommit=ae679d5afa5f3cfacfe79c4d7b8a462baca2c195
publicReleaseTransaction=PENDING
signedLiftInformationTheoreticMinimality=NOT_ESTABLISHED
signedLiftComponentwiseMinimality=NOT_ESTABLISHED
signedLiftUniqueness=NOT_ESTABLISHED
fullThirdCumulantStateNonAutonomy=NOT_ESTABLISHED
fourthOrderNonClosure=NOT_ESTABLISHED
finiteMomentHierarchyNoGo=NOT_ESTABLISHED
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=FALSE
navierStokesSimulation=NOT_RUN
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```
