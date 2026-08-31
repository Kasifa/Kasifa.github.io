# R0.73U | Full tensors in the heat hierarchy: pressure is recoverable, but the even quadratic state is not dynamically closed

**Status:** analytic proof, independent readback, exact-certificate final seal,
and formal-figure QA passed; the remaining release transaction is bilingual
HTML/PDF rendering and deployment

**Public title (zh):** R0.73U｜完整张量进入热层级：压力可以恢复，但偶二次状态的动力学并不闭合

**Date:** 2026-09-01

**Audience:** researchers and technically trained readers following the
periodic three-dimensional Navier--Stokes notes

**Scope:** an exact heat-covariance hierarchy, same-scale pressure
reconstruction, two critical stress bounds, a centered pressure-variance
refinement, and a four-site quadratic-state non-autonomy witness; no
arbitrary-data global regularity claim

**Normalization:** \(\mathbb T^3=[0,2\pi]^3\) carries normalized Haar measure
\(d\mu=(2\pi)^{-3}dx\); viscosity is \(\nu>0\)

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## 1. 直接结论

R0.73T 留下的问题是：标量 \(\widehat{|u|^2}\) 不足以恢复压力所需的
张量极化。R0.73U 把状态扩大为每一个 heat 尺度上的完整局部乘积张量。
令

\[
 P_s=e^{s\Delta},\qquad
 v_s=P_su,\qquad
 \Theta_s=P_s(u\otimes u),\qquad
 \tau_s=\Theta_s-v_s\otimes v_s.
 \tag{1.1}
\]

这里得到四条正结果。

第一，\(\Theta_s\) 和 \(\tau_s\) 都逐点半正定，而且 \(\tau_s\) 是严格的
heat covariance。它满足

\[
 \boxed{
 (\partial_s-\Delta)\tau_s
 =2\sum_\ell\partial_\ell v_s\otimes\partial_\ell v_s,
 \qquad \tau_0=0.}
 \tag{1.2}
\]

第二，完整张量确实恢复了压力：

\[
 \boxed{
 p_s=P_sp=R_iR_j\Theta_{s,ij}
 =R_iR_j(v_{s,i}v_{s,j}+\tau_{s,ij}).}
 \tag{1.3}
\]

第三，stress 没有超出 R0.73Q/R 的临界指数。若
\(E=L_t^4L_x^6\)，则

\[
 \boxed{
 \sup_{s\ge0}\|\tau_s\|_{L_t^2L_x^3}
 \le\|u\|_E^2.}
 \tag{1.4}
\]

而仅用能量时，每一个固定 \(s>0\) 仍有

\[
 \boxed{
 \|\tau_s\|_{L_t^2(0,T;L_x^3)}
 \lesssim {\|u(0)\|_2^2\over\sqrt{\nu s}}.}
 \tag{1.5}
\]

式 (1.4) 是临界强范数的重新包装；式 (1.5) 是能量类的正尺度估计，
但在 \(s\downarrow0\) 时损失 \(s^{-1/2}\)。两条式子必须同时读。

第四，把压力按 \(|u|^2\) 加权居中后，可以严格收紧 R0.73T 的一侧
\(AQ\) 估计。这条改进与已有的 velocity--pressure correlation 文献有
直接公式碰撞，因此不承担新颖性声明。

负结果也变得更准确。完整二次张量可以恢复压力，却不能恢复其时间方程中
的三次带符号通量。一个四 Fourier 站点的精确见证给出

\[
 \Theta_s(-u)=\Theta_s(u),\qquad
 \tau_s(-u)=\tau_s(u),\qquad
 p_s(-u)=p_s(u),
 \tag{1.6}
\]

但二者的 tensor time tangent 不同。这排除的是“只由偶次二次张量组成的
自治等式”。它不排除一侧上界，也不排除加入 \(v_s\) 或三阶有符号对象。

## 2. 先区分两种完全不同的“张量相关”

这一节最容易发生的错误，是把局部乘积张量写成经典 KHM 两点相关。
R0.73U 使用

\[
 T^{\rm loc}_{ij}(h)
 =\widehat{u_i u_j}(h)
 =\sum_k\widehat u_i(k)\widehat u_j(h-k).
 \tag{2.1}
\]

经典 K\'arm\'an--Howarth--Monin 对象则是

\[
 R_{ij}(r)=\int u_i(x)u_j(x+r)d\mu(x),
 \qquad
 \widehat R_{ij}(k)=\widehat u_j(k)\overline{\widehat u_i(k)}.
 \tag{2.2}
\]

式 (2.1) 保存不同波数之间的卷积相位，所以可由

\[
 \widehat p(h)=-{h_i h_j\over|h|^2}T^{\rm loc}_{ij}(h),\quad h\ne0,
 \qquad \widehat p(0)=0
 \tag{2.3}
\]

重建瞬时压力。式 (2.2) 只保存同一波数的协方差，不能做这个一般重建。

反过来，经典 scalar KHM 方程在周期或齐次平均后可以让 pressure trace
抵消，但它仍含三阶速度增量。压力从一条方程里消失，并不等于二阶统计
已经自治。R0.73U 的正负结果都针对式 (2.1)，不应被改写成对式 (2.2)
的优先权主张。

## 3. heat covariance 的精确正结构

周期 heat kernel 非负且质量为一。对任意固定向量 \(a\)，

\[
 a^T\Theta_sa=P_s((a\cdot u)^2)\ge0,
 \tag{3.1}
\]

并且 Jensen 不等式给出

\[
 a^T\tau_sa
 =P_s((a\cdot u)^2)-(P_s(a\cdot u))^2\ge0.
 \tag{3.2}
\]

所以这两个张量都半正定。更直接地，\(\tau_s\) 是

\[
 \tau_s(x)
 =P_s[(u-v_s(x))\otimes(u-v_s(x))](x).
 \tag{3.3}
\]

把 \(\tau_s=\Theta_s-v_s\otimes v_s\) 对 \(s\) 求导，并使用乘积法则，
就得到式 (1.2)。Duhamel 形式是

\[
 \boxed{
 \tau_s
 =2\int_0^sP_{s-r}\left[
  \sum_\ell\partial_\ell v_r\otimes\partial_\ell v_r
 \right]dr.}
 \tag{3.4}
\]

不同 heat 层之间还有

\[
 \boxed{
 \tau_{s+r}(u)=P_r\tau_s(u)+\tau_r(P_su).}
 \tag{3.5}
\]

这是 Germano filtering identity 在 heat 半群下的直接形式。它给尺度
组织，不给物理时间闭合。式 (1.2) 的自变量是 filter parameter \(s\)，
不是 Navier--Stokes 时间 \(t\)。

## 4. 同尺度压力、filtered NSE 与有符号能量通量

heat 半群与导数、Leray 投影和 Riesz 变换交换。因此

\[
 \boxed{
 \partial_tv_s
 +\mathbb P\nabla\cdot(v_s\otimes v_s+\tau_s)
 =\nu\Delta v_s.}
 \tag{4.1}
\]

在 primitive variables 中，它是

\[
 \partial_tv_s+(v_s\cdot\nabla)v_s+\nabla\cdot\tau_s+\nabla p_s
 =\nu\Delta v_s.
 \tag{4.2}
\]

相应的 resolved local energy law 为

\[
\begin{aligned}
 \partial_t{|v_s|^2\over2}
 +\nabla\cdot\left[
 \left({|v_s|^2\over2}+p_s\right)v_s+\tau_sv_s\right]
 ={}&\nu\Delta{|v_s|^2\over2}-\nu|\nabla v_s|^2\\
 &+\tau_s:\nabla v_s.
\end{aligned}
 \tag{4.3}
\]

通常把 \(\Pi_s=-\tau_s:\nabla v_s\) 称为 subgrid energy flux。即使
\(\tau_s\succeq0\)，\(\Pi_s\) 也没有固定符号，因为不可压应变是
trace-free，通常同时有正负特征方向。

这条界限很重要：covariance 的半正定性不等于 eddy viscosity，也不等于
耗散已经控制。

## 5. 两条临界 stress 估计

对半正定矩阵 \(A\)，\(|A|_F\le\operatorname{tr}A\)。因此

\[
 |\Theta_s|_F\le P_s|u|^2,
 \qquad
 |\tau_s|_F\le\operatorname{tr}\tau_s\le P_s|u|^2.
 \tag{5.1}
\]

heat contraction 和 H\"older 直接给

\[
 \sup_{s\ge0}\bigl(
 \|\Theta_s\|_{L_t^2L_x^3}
 +\|\tau_s\|_{L_t^2L_x^3}\bigr)
 \le2\|u\|_{L_t^4L_x^6}^2.
 \tag{5.2}
\]

R0.73Q 的周期 Stokes--HLS 映射是

\[
 \left\|
 \int_{t_0}^te^{\nu(t-r)\Delta}
 \mathbb P\nabla\cdot F(r)dr
 \right\|_{L_t^4L_x^6}
 \le C_{B,\nu}\|F\|_{L_t^2L_x^3}.
 \tag{5.3}
\]

故 \(\tau_s\) 的 Duhamel 输出仍回到同一个 \(L_t^4L_x^6\) 空间。这个
指数匹配是正确的，但式 (5.2) 已经假设 \(u\in L_t^4L_x^6\)，所以不能
把它写成任意初值的先验收益。

不假设这个强范数时，能量仍给每个固定正尺度的估计。固定光滑寿命内的
\(0<T<T_*\)，并记

\[
 E_0=\|u(0)\|_2^2,
 \qquad H_3(s)=\|P_s\|_{L^1\to L^3}.
\]

这里 \(C_S\) 表示归一化周期环面上的 mean-zero Sobolev 常数。

一方面，周期 Sobolev 与能量不等式给

\[
 \|\tau_s\|_{L_t^1(0,T;L_x^3)}
 \le {C_S^2E_0\over2\nu}.
 \tag{5.4}
\]

另一方面，heat smoothing 给

\[
 \|\tau_s\|_{L_t^\infty(0,T;L_x^3)}\le H_3(s)E_0.
 \tag{5.5}
\]

时间插值得到

\[
 \boxed{
 \|\tau_s\|_{L_t^2(0,T;L_x^3)}^2
 \le {C_S^2H_3(s)\over2\nu}E_0^2.}
 \tag{5.6}
\]

该常数与 \(T<T_*\) 无关。在三维短 heat 尺度，
\(H_3(s)\lesssim s^{-1}\)，所以得到式 (1.5)。
这条式子把下一步的难点定位得很具体：正尺度 stress 已有能量控制，缺的是
把 \(s^{-1/2}\) 损失消掉，或在物理时间积分中证明足够的抵消。

这里的“临界”指 Euclidean/local parabolic exponent relation。固定归一化
环面的整数 covering dilation 不应被写成字面 norm invariance。

## 6. 加权中心压力方差收紧 R0.73T

令

\[
 w=|u|^2,\quad Q=\int w^2,\quad
 X^2=\int|\nabla w|^2,\quad
 Y=\int w|\nabla u|^2.
\]

R0.73T 的精确四次平衡是

\[
 Q'+4\nu Y+2\nu X^2=4\int p\,u\cdot\nabla w.
 \tag{6.1}
\]

右端对 \(p\mapsto p-c(t)\) 不变。当 \(u\not\equiv0\) 时，我选择使
加权方差最小的常数

\[
 \bar p_w={\int wp\over\int w},
 \qquad
 \mathcal P_*=\int w(p-\bar p_w)^2.
 \tag{6.2}
\]

若 \(u\equiv0\)，则本节不等式平凡并单独处理。

weighted Cauchy 给

\[
 \left|\int(p-\bar p_w)u\cdot\nabla w\right|
 \le\mathcal P_*^{1/2}X.
 \tag{6.3}
\]

于是对任意 \(0<\vartheta\le2\)，

\[
 \boxed{
 Q'+4\nu Y+(2-\vartheta)\nu X^2
 \le {4\over\vartheta\nu}\mathcal P_*.}
 \tag{6.4}
\]

令 \(\beta_*=\mathcal P_*/Q\)。取 \(\vartheta=1\)，得到

\[
 \boxed{
 Q'+4\nu Y+\nu X^2\le {4\over\nu}\beta_*Q.}
 \tag{6.5}
\]

记 R0.73T 的 Wiener 量
\(A=\sum_h|\widehat{|u|^2}(h)|\)，并令 \(C_R\) 表示周期
double-Riesz 算子在这里所用空间上的有界性常数。同时

\[
 \mathcal P_*
 \le\int wp^2
 \le\|p\|_3^2\|w\|_3
 \le C_R^2\|u\|_6^6
 \le C_R^2AQ.
 \tag{6.6}
\]

所以 \(\beta_*\le C_R^2A\)。式 (6.5) 的右端逐点不大于 R0.73T，
对 pressure-free shear 则严格更小。取 \(\vartheta=2\) 还得到

\[
 Q'+4\nu Y\le {2\over\nu}\beta_*Q.
 \tag{6.7}
\]

若 \(\int\beta_*dt<\infty\)，Gronwall 控制 \(Q\)，随后进入经典
\(L_t^\infty L_x^4\) continuation 路径。这个预算在 local parabolic
scaling 下临界，尚无能量类先验控制。

这条推论不是从空白开始。Tran、Yu 与 Dritschel 在 2021 年的 JFM
论文中直接研究了 \(\int p^2|u|^{q-2}\) 和 velocity--pressure
correlation coefficient：
[DOI](https://doi.org/10.1017/jfm.2020.1033)。所以我把式 (6.4)--(6.7)
标为 `INTERNAL_COROLLARY_WITH_CLASSICAL_COLLISION`，不写成新的正则性
判据或优先权结果。

## 7. 物理时间方程为何仍不闭合

令 \(T_{ij}=u_i u_j\)。直接对乘积求导得到

\[
\begin{aligned}
 \partial_tT_{ij}
 ={}&\nu\Delta T_{ij}
 -2\nu\partial_\ell u_i\partial_\ell u_j\\
 &-\partial_k(u_ku_iu_j)
 -(u_j\partial_ip+u_i\partial_jp).
\end{aligned}
 \tag{7.1}
\]

因此

\[
\boxed{
 (\partial_t-\nu\partial_s)\Theta_{s,ij}
 =-2\nu P_s(\partial_\ell u_i\partial_\ell u_j)
 -\partial_kP_s(u_ku_iu_j)
 -P_s(u_j\partial_ip+u_i\partial_jp).}
 \tag{7.2}
\]

完整 \(\Theta_s\) 解决了“如何重建 \(p_s\)”的问题，但式 (7.2) 仍需要
\(u_ku_iu_j\) 和 \(pu\)。这两个都是对 \(u\mapsto-u\) 变号的奇次对象。

我把这里的主状态写成 \((v_s,\tau_s)\)，并把
\(\Theta_s=v_s\otimes v_s+\tau_s\) 保留为 pressure/nonlinearity ledger。
单独的 \(\Theta_s\) 或 \(\tau_s\) 都是偶对象，不能携带这部分方向信息。

## 8. 四站点精确见证与 parabolic loss

取

\[
 u(x,y,z)=
 \bigl(2\sin(x+y),\;2\sin x-2\sin(x+y),\;0\bigr).
 \tag{8.1}
\]

它只有四个非零 Fourier 站点，实、零均值、无散度。正频率系数是

\[
 \widehat u(1,0,0)=(0,-i,0),
 \qquad
 \widehat u(1,1,0)=(-i,i,0).
 \tag{8.2}
\]

把
\(V=\Delta T-2\partial_\ell u\otimes\partial_\ell u\)
记为不含 \(\nu\) 的黏性张量系数。在 \(h_*=(1,2,0)\)，精确有理数
卷积给出

\[
 \widehat T(h_*)=0,
 \qquad
 \widehat V(h_*)=0,
 \tag{8.3}
\]

而非线性 tensor tangent 为

\[
 K(h_*)=
 \begin{pmatrix}
 -2&1&0\\1&0&0\\0&0&0
 \end{pmatrix}.
 \tag{8.4}
\]

对 \(-u\)，\(T,p,V\) 完全相同，\(K\) 反号。以下
\(\partial_t\) 都指相应光滑初值在 \(t=0\) 的 Navier--Stokes 切向量。
因此

\[
 \partial_t\widehat T(h_*;u)
 -\partial_t\widehat T(h_*;-u)=2K(h_*)\ne0.
 \tag{8.5}
\]

heat 只乘 \(e^{-5s}\)，不能恢复方向。对
\(u_L(x)=u(Lx)\)、\(h_{*,L}=Lh_*\)，差值为

\[
 2Le^{-5sL^2}K(h_*).
 \tag{8.6}
\]

在 \(s=\theta L^{-2}\) 时，其 Frobenius size 是

\[
 \boxed{
 2\sqrt6Le^{-5\theta}
 =2\sqrt{6\theta}e^{-5\theta}s^{-1/2}.}
 \tag{8.7}
\]

归一化 profile 在 \(\theta=1/10\) 取峰值。这与式 (1.5) 的
\(s^{-1/2}\) loss 在指数上对齐：heat 能选择尺度，却不能凭偶次张量
恢复方向。这个指数匹配不证明能量唯一估计已经达到 sharp 常数或普适
最优阶。

这个见证的最小性也有严格边界。一个单独的共轭频率对因
\(k\cdot\widehat u(k)=0\) 而 self-advection 为零，所以在实、零均值、
无 mean mode 的有限 Fourier 类中至少需要四站点；式 (8.1) 达到这个
下界。但它的全局 quartic nonlinear derivative 为零，不能取代 R0.73T
的六模 pressure-work 见证。

更不能从式 (8.5) 推出“tensor-only 上界都不可能”。例如

\[
 |u\otimes a+a\otimes u|_F^2
 =2\operatorname{tr}(u\otimes u)|a|^2
 +2a^T(u\otimes u)a.
 \tag{8.8}
\]

二次张量可能控制某些无符号大小，只是不能决定这个 signed tangent。

## 9. 文献归属、结果价值与下一步

经典 KHM 层级来自 von K\'arm\'an--Howarth 1938，Hill 2001 给出了任意
阶 exact structure-function equations：
[1938 DOI](https://doi.org/10.1098/rspa.1938.0013)，
[2001 DOI](https://doi.org/10.1017/S0022112001003949)。

Germano 1992 给出 filtering framework 和层间 stress identity：
[DOI](https://doi.org/10.1017/S0022112092001733)。Eyink 1996 研究 exact
subgrid stress/flux 与 locality：
[arXiv](https://arxiv.org/abs/chao-dyn/9602018)。
Constantin--E--Titi 1994 与 Duchon--Robert 2000 的 commutator/defect
公式同样指出，能量传递的精确对象是有符号三阶增量：
[CET DOI](https://doi.org/10.1007/BF02099744)，
[DR DOI](https://doi.org/10.1088/0951-7715/13/1/312)。

最新直接碰撞之一是 Zambrano--Duraisamy 2026 的 physical-space
two-point closure。该文明确把 K\'arm\'an--Howarth 的三阶矩作为
unclosed moment，并在 homogeneous isotropic turbulence 下加入
quasi-normal、Markovian 与 eddy-damping 假设：
[DOI](https://doi.org/10.1017/jfm.2026.11485)。模型闭合不能改写成一般
确定性三维 Navier--Stokes 的有限阶闭合定理。

我对 R0.73U 的价值判断是：它没有解决全局正则性，但把 R0.73T 的两个
信息缺口分开了。

- pressure polarization 已由 full local-product tensor 修复；
- signed cubic orientation 仍缺失，而且有四站点精确 no-go；
- stress 在每个正尺度由能量控制，但带 \(s^{-1/2}\) 损失；
- centered pressure variance 比 \(AQ\) 更精确，但它仍是临界预算，并与
  已有 pressure-correlation 方法直接相邻。

因此下一步不应继续增加更多偶次二阶统计。我会检查两个更窄的方向：

1. 加入最小的 signed third-order lift，寻找其 physical-time 方程中可被
   \(\nu\partial_s\) 或 Stokes smoothing 吸收的组合；
2. 保留 tensor-only 无符号 envelope，检验式 (8.8) 能否与式 (1.2) 的
   carré-du-champ 正项配对，并把 \(s^{-1/2}\) 损失放进可积的时间结构。

现阶段准确的 release ledger 是：

```text
heatCovariancePSD=INTERNAL_EXACT
heatCovarianceScalePDE=INTERNAL_EXACT
sameScalePressureReconstruction=VERIFIED_CLASSICAL
filteredNSEAndSGSFlux=VERIFIED_CLASSICAL_RECONSTRUCTION
conditionalCriticalStressRow=INTERNAL_COROLLARY
fixedPositiveScaleEnergyStressBound=INTERNAL_COROLLARY
centeredPressureVarianceRefinement=INTERNAL_COROLLARY_WITH_CLASSICAL_COLLISION
fourSiteQuadraticStateNonAutonomy=CLOSED_EXACT
parabolicCoefficientLoss=CLOSED_EXACT
formalFiniteCertificate=PASS
formalFiniteCertificateChecks=75
formalFigurePackage=PASS
formalFigureChecks=325
sourceCommitAssigned=TRUE
sourceCommit=84e808dae473f6381cbf9df55a71f5fe81a1cfce
certificateSourceCommit=6c79f23152116f5d420be6ff03653500ab02ef0e
finitePackageCommit=044bfb3f7e5af98e2615f60747c9e5109ef12d7c
figurePackageCommit=6c20af03a21488fea3f060738084fa9048437984
finalSeal=TRUE
finiteGeneralTensorClosure=OPEN
zeroScaleEnergyCriticalStressControl=OPEN
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=FALSE
navierStokesSimulation=NOT_RUN
NOT CLAY
```
