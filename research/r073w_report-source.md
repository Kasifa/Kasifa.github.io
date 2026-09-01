# R0.73W | Signed subfilter production: heat-plane characteristics, the energy-class boundary, and exact counterexamples

**Status:** analytic proof, independent sign/index audit, bounded
primary-literature audit, and commit-bound two-path finite certificate
complete; the figure seal and public deployment remain separate gates

**Public title (zh):** R0.73W｜带符号亚滤波 production：heat-plane 特征线、能量类边界与精确反例

**Date:** 2026-09-01

**Audience:** researchers and technically trained readers following the
periodic three-dimensional Navier--Stokes notes

**Scope:** exact Gaussian stress attribution, an exact local heat-coordinate
energy balance, an energy-class absolute estimate, a centered-increment trace
split, a critical scale-weighted identity, and finite exact sign/absorption
counterexamples; no regularity theorem

**Normalization:** \(\mathbb T^3=[0,2\pi]^3\) carries normalized Haar measure
\(d\mu=(2\pi)^{-3}dx\); viscosity is \(\nu>0\)

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

## 1. 直接结论

R0.73V 取完整 stress 方程的一半迹以后，压力--应变项严格消失，但留下
带符号的亚滤波 production

\[
 \Pi_s=-\tau_s:\nabla v_s,
 \qquad
 v_s=P_su,
 \qquad
 \tau_s=P_s(u\otimes u)-v_s\otimes v_s.
\tag{1.1}
\]

R0.73W 检查这个标量项能否由 heat 尺度或粘性耗散控制。我得到六条
边界清楚的结论。

**[经典恒等式，当前归一化已重推]** 第一，Gaussian stress 满足

\[
 \boxed{
 \tau_{ij,s}=2\int_0^sP_{s-r}
 (\partial_\ell v_{r,i}\partial_\ell v_{r,j})\,dr.}
\tag{1.2}
\]

这正是 Johnson 2020/2021 的精确 Gaussian-filter 公式在
\(s=\ell^2/2\) 下的 heat-semigroup 写法，不是新公式。虽然
\(\tau_s\) 半正定，但 incompressible strain 无迹，所以

\[
 \Pi_s=-\tau_s^\circ:S_s
\tag{1.3}
\]

仍然没有固定符号。

**[heat 坐标中的经典能量律，已独立审计]** 第二，resolved energy
\(e_s=|v_s|^2/2\) 满足

\[
 \boxed{
 (\partial_t-\nu\partial_s)e_s+
 \nabla\cdot[(e_s+p_s)v_s+\tau_sv_s]= -\Pi_s.}
\tag{1.4}
\]

沿 \(s'(t)=-\nu\) 的特征线，空间平均 production 的带符号积分恰好等于
端点 resolved energy 之差。这是精确支付，但只控制带符号空间平均，
不控制 \(|\Pi_s|\) 或逐点符号。

**[无条件能量类推论，已独立审计]** 第三，对 \(0<s\le1\)，

\[
 \boxed{
 \|\Pi_s\|_{L^1_{t,x}}
 \le Cs^{-1/4}
 \|u\|_{L_t^\infty L_x^2}
 \|\nabla u\|_{L^2_{t,x}}^2.}
\tag{1.5}
\]

因此 \(\int_0^S\|\Pi_s\|_1ds\lesssim S^{3/4}\)；绝对 production 在每个
小 heat 尺度区间可积。不过式 (1.5) 在 \(s\downarrow0\) 时不是一致界，
本节也没有证明 \(1/4\) 最优。

**[精确中心增量分解，已独立审计]** 第四，令
\(K_{j,s}=\kappa_{iij,s}/2\)，则

\[
 \boxed{
 \Pi_s=\partial_jK_{j,s}+\mathscr S_s,\qquad
 \mathscr S_s={1\over4s}\int_{\mathbb R^3}
 y\cdot a_s|a_s|^2g_s(y)\,dy,}
\tag{1.6}
\]

其中 \(a_s(x,y)=u(x-y)-v_s(x)\)，而
\(Q_{j,s}=P_s(pu_j)-p_sv_{s,j}\) 是沿用 R0.73V 的压力--速度
covariance flux。把式 (1.6) 代回 R0.73V 的 trace 方程后，\(K_s\)
完全消掉：

\[
 \boxed{
 \partial_tk_s+\nabla\cdot(v_sk_s+Q_s-\nu\nabla k_s)
 =-\nu D_{ii,s}+\mathscr S_s.}
\tag{1.7}
\]

而

\[
 D_{ii,s}=2\int_0^sP_{s-r}|\nabla^2v_r|_F^2dr\ge0.
\tag{1.8}
\]

这一步把空间 divergence、非负 carré-du-champ 与唯一带符号余项分开；
它没有把 \(\mathscr S_s\) 吸收到式 (1.8)。

**[临界尺度平均，已独立审计]** 第五，令 \(L=-\Delta\)。对均值零场，

\[
 \boxed{
 \int_0^\infty s^{-1/2}\langle\Pi_s\rangle ds
 =\sqrt{\pi/2}\,
 \langle L^{-1/2}u,(u\cdot\nabla)u\rangle.}
\tag{1.9}
\]

右侧是零阶 Riesz 三线性型，受 \(C\|u\|_3^3\) 控制。它恢复的正是经典
\(H^{1/2}\) 小数据结构，而不是任意能量的 coercive 吸收。

**[两路径精确有限计算，已 commit-bound 封存]** 第六，主见证

\[
 \begin{aligned}
 R(x,y,z)=\big(&\cos(y+z)-\sin(x+y+z)+\cos(2z),\\
 &\cos x+\sin(x+y+z),0\big)
 \end{aligned}
\tag{1.10}
\]

是光滑、均值零、无散且 Fourier 支撑秩三的场。对 \(u_A=AR\)、
\(q=e^{-s}\)，两个互不导入的精确 producer 都得到

\[
 \boxed{
 \langle\Pi_s(u_A)\rangle={A^3\over4}q^2(1-q^2),}
\tag{1.11}
\]

\[
 \boxed{
 \langle D_{ii,s}(u_A)\rangle
 ={A^2\over2}(1-q^2)(13+12q^2+10q^4+4q^6).}
\tag{1.12}
\]

把 \(A\) 换成 \(-A\) 会翻转 production，而 stress 和 \(D\) 不变；
因此不存在对所有光滑无散数据成立的单边符号律。比值

\[
 { |\langle\Pi_s\rangle|\over\nu\langle D_{ii,s}\rangle}
 ={Aq^2\over2\nu(13+12q^2+10q^4+4q^6)}
\tag{1.13}
\]

随 \(A\to\infty\) 无界，所以文中指定的同时刻、振幅无关二次吸收也
不成立。

**[开放]** 这些结果没有给出 \(s=0\) 的一致绝对控制、局部 coercivity
或 continuation criterion。任意三维初值的全局正则性与 Clay 千禧年问题
仍然开放。

## 2. Gaussian stress 与 deviatoric 障碍

heat covariance 的尺度方程是

\[
 (\partial_s-\Delta)\tau_{ij,s}
 =2\partial_\ell v_{s,i}\partial_\ell v_{s,j},
 \qquad \tau_{ij,0}=0.
\tag{2.1}
\]

式 (1.2) 是它的 Duhamel 解。heat kernel 的 variance 解释还给出

\[
 a_i\tau_{ij,s}a_j
 =P_s[(a\cdot u)^2]-[P_s(a\cdot u)]^2\ge0.
\tag{2.2}
\]

半正定性只说明 \(\tau_s\) 是正 covariance。因为
\(\operatorname{tr}S_s=0\)，其 isotropic 部分在 production 中消失：

\[
 \boxed{
 \Pi_s=-2\int_0^sP_{s-r}
 [ (\nabla v_r\nabla v_r^T)^\circ ]:S_s\,dr.}
\tag{2.3}
\]

所以真正的困难是 deviatoric covariance 与 trace-free strain 的带符号
alignment。正 stress 本身不能提供正 production。

## 3. heat-plane 特征线恒等式

过滤 Navier--Stokes 方程并与 \(v_s\) 点乘，得到经典 resolved-energy
平衡

\[
 \partial_te_s+\nabla\cdot[(e_s+p_s)v_s+\tau_sv_s]
 =\nu\Delta e_s-\nu|\nabla v_s|^2-\Pi_s.
\tag{3.1}
\]

另一方面，\(\partial_sv_s=\Delta v_s\) 给出

\[
 \partial_se_s=\Delta e_s-|\nabla v_s|^2.
\tag{3.2}
\]

式 (3.1) 减去 \(\nu\) 倍式 (3.2) 即为式 (1.4)。令
\(E_s(t)=\langle e_s(t)\rangle\)，则

\[
 \langle\Pi_s(t)\rangle
 =-(\partial_t-\nu\partial_s)E_s(t).
\tag{3.3}
\]

因此对 \(s(t)=s_0-\nu(t-t_0)>0\)，

\[
 \boxed{
 \int_{t_0}^{t_1}\langle\Pi_{s(t)}(t)\rangle dt
 =E_{s_0}(t_0)-E_{s(t_1)}(t_1).}
\tag{3.4}
\]

对光滑解，特征线可以到达 \(s=0\)。对 Leray--Hopf 解，本节只在
\(s(t)\ge\sigma>0\) 时使用该恒等式；若没有额外 energy equality，
不把零尺度端点当作等式。

## 4. 能量类绝对界

式 (1.2) 与 heat contraction 直接给出

\[
 \|\tau_s(t)\|_1
 \le2\int_0^s\|\nabla v_r(t)\|_2^2dr
 \le2s\|\nabla u(t)\|_2^2.
\tag{4.1}
\]

三维 heat kernel 的一阶导数估计是

\[
 \|\nabla P_su(t)\|_\infty
 \le Cs^{-5/4}\|u(t)\|_2,
 \qquad 0<s\le1.
\tag{4.2}
\]

式 (4.1)--(4.2) 相乘并对时间积分，得到式 (1.5)。再对 \(s\) 积分，

\[
 \boxed{
 \int_0^S\|\Pi_s\|_{L^1_{t,x}}ds
 \le {4C\over3}S^{3/4}
 \|u\|_{L_t^\infty L_x^2}
 \|\nabla u\|_{L^2_{t,x}}^2.}
\tag{4.3}
\]

这个结论不假设 Serrin 强范数。它说明绝对 production 的 small-scale
积分有限，但没有把式 (4.3) 变成尺度临界的局部正则性判据。

## 5. 中心增量与 trace 消去

把周期场延拓到 \(\mathbb R^3\)，用欧氏 heat kernel

\[
 g_s(y)=(4\pi s)^{-3/2}e^{-|y|^2/(4s)}
\tag{5.1}
\]

表示 \(P_s\)。令 \(a_s(x,y)=u(x-y)-v_s(x)\)。第三 central moment 的
收缩是

\[
 K_{j,s}={1\over2}\int g_s(y)a_{s,j}|a_s|^2dy.
\tag{5.2}
\]

对式 (5.2) 求空间散度，并在 \(y\) 上分部积分，得到式 (1.6)。这里
\(1/(4s)\) 来自 \(\nabla g_s=-yg_s/(2s)\)。若改用基本胞上的周期 kernel
坐标，不能原样套用这个 kernel derivative。

R0.73V 的完整 trace 方程是

\[
 \partial_tk_s+\nabla\cdot(v_sk_s)
 =-\nabla\cdot(K_s+Q_s-\nu\nabla k_s)
 -\nu D_{ii,s}+\Pi_s.
\tag{5.3}
\]

代入式 (1.6) 后，\(K_s\) 完全消去，得到式 (1.7)。这个等式首先是
smooth lifespan 上的物理时间恒等式。若 suitable weak solution 有局部
energy-defect measure \(\mu\ge0\)，右端还要保留 \(-P_s\mu\)；本节不把
smooth trace equality 无条件传给任意弱极限。

## 6. 临界 \(s^{-1/2}\) 尺度平均

设 \(h=(u\cdot\nabla)u\)、\(L=-\Delta\)。周期分部积分与 heat semigroup
自伴性给出

\[
 \boxed{
 \langle\Pi_s\rangle=\langle e^{-2sL}u,h\rangle.}
\tag{6.1}
\]

对一般收敛权重 \(w\)，令

\[
 m_w(\lambda)=\int_0^\infty w(s)e^{-2s\lambda}ds.
\tag{6.2}
\]

则

\[
 \int_0^\infty w(s)\langle\Pi_s\rangle ds
 =\langle m_w(L)u,h\rangle.
\tag{6.3}
\]

当 \(w(s)=s^{-1/2}\) 时，

\[
 m_w(L)=\sqrt{\pi/2}L^{-1/2},
\tag{6.4}
\]

从而得到式 (1.9)。以 \(R_j=\partial_jL^{-1/2}\) 记 Riesz transform，

\[
 \int_0^\infty s^{-1/2}\langle\Pi_s\rangle ds
 =-\sqrt{\pi/2}\int u_i u_jR_ju_i.
\tag{6.5}
\]

同时，

\[
 \int_0^\infty s^{-1/2}{d\over ds}\langle k_s\rangle ds
 =\sqrt{\pi/2}\|L^{1/4}u\|_2^2.
\tag{6.6}
\]

式 (6.5) 受 \(C\|u\|_3^3\le C\|L^{1/4}u\|_2^3\) 控制。因此 scale
smoothing 的一阶收益恰好被 nonlinear derivative 用完，只剩经典临界
三线性型。对能量解还可得

\[
 \int_0^T\left|
 \int_0^\infty s^{-1/2}\langle\Pi_s(t)\rangle ds
 \right|dt
 \le C\|u_0\|_2^3\nu^{-3/4}T^{1/4}.
\tag{6.7}
\]

式 (6.7) 先对空间与 heat 尺度做带符号积分，再取绝对值；它不是
\(\int|\Pi_s|\) 的局部或固定尺度估计。

## 7. 两路径精确 Fourier 证书

证书包含两套互不 import 的标准库实现：一套使用稀疏 complex Fourier
与 Fraction/Laurent polynomial，另一套使用 real trigonometric
product-to-sum 与独立的 dense Fraction tuple。两边都从原始场重建
\(v_s,\tau_s,\Pi_s,D_{ii,s}\)，并从实际 support 精确消元计算频率秩。

commit-bound 封存中，两条路径各通过 56/56 项检查，完整 `commonCore`
逐字节一致；manifest 绑定源提交 `b9f3b3943df1e2abf6abc2f51c1fb25d1f1e8440`。
除秩三主见证外，证书还保留：

- 一个原坐标依赖 \(x,y,z\)、但频率只张成 rank two 的 triad；
- 一个 2D3C 场，其 production 具有相反的显式多项式。

这两个对象只用于诊断交叉核验。正式公开结论绑定式 (1.10) 的秩三
主见证。证书是光滑三角多项式上的精确 Fourier 代数，不是
Navier--Stokes 时间轨道、数值仿真、奇性或 blow-up 候选。

## 8. 文献归属

R0.73W 的直接文献谱系如下。

- Johnson 2020 PRL 与 2021 JFM：Gaussian stress 的 forced diffusion、
  exact scale integral、production 和 multiscale strain/vorticity 分解。
- Eyink--Aluie 2009：一般 smooth coarse-graining 下的 filtered
  Navier--Stokes 局部能量律与 \(\Pi=-\tau:\nabla\bar u\)。
- Germano 1992：generalized central moments 与 filter composition。
- Constantin--E--Titi 1994、Eyink 1995/2006：increment commutator、local
  flux 与 exact stress expansion 的数学/湍流谱系。
- Duchon--Robert 2000：弱解的零尺度局部 energy defect；它不是固定
  \(s>0\) 的 production 恒等式。
- Fujita--Kato 1964：式 (1.9) 最终恢复的经典 \(H^{1/2}\) 临界小数据
  结构。

Johnson 2020 PRL 的 2021 erratum 影响后续 strain--rotation 分解中的一个
sign/index，不影响 forced diffusion 与 exact stress 的核心式 (8)--(10)。
本节引用完整分解时优先采用 2021 JFM。

限定式主来源检索没有找到式 (1.4)、式 (1.5) 或式 (1.9) 完全相同的公开
打包。未检出不证明新颖性、优先权、不存在或第一性。公开标签分别是
“heat-coordinate reformulation”“energy-class corollary”和
“critical scale-weighted synthesis”。

## 9. 研究价值与剩余缺口

这一节的价值不是把 Clay 问题缩成一个已经解决的 inequality，而是把
R0.73V 的最后一个标量项拆成三种不同层级：

1. 带符号空间平均可沿 heat-plane characteristic 精确支付；
2. 绝对 production 可由能量类控制，但损失 \(s^{-1/4}\)；
3. 中心增量余项在 trace 方程中保留，临界尺度权重只恢复经典
   \(H^{1/2}\) 小数据结构。

精确反例还封闭了两条不应继续投入的路线：stress positivity 不能推出
production positivity；cubic production 不能由指定的 quadratic
viscous covariance 在同一时刻、以振幅无关常数吸收。

剩余缺口集中在局部化和零尺度。若能在保持 cutoff commutator 与 energy
defect 可见的前提下，证明 scale-critical tent-space/Carleson control 或
一个非循环的 epsilon regularity criterion，才可能继续触及 regularity。
目前没有这样的证明。

## 10. 下一步：R0.73X

R0.73X 应固定一个局部 parabolic cylinder 与 cutoff，先推导式 (1.4) 的
localized heat-characteristic 版本。下一节必须逐项保留：

- spatial flux 穿过 cutoff 的边界项；
- pressure covariance；
- \(\mathscr S_s\) 的 centered increment；
- suitable weak solution 的 energy-defect measure；
- heat scale 与物理 cylinder 半径之间的 parabolic scaling。

第一道判断题不是“能否再写一个全局平均”，而是能否从 energy class
得到一个尺度无关的局部小量。若答案是否定的，应构造 exact concentration
witness 或 scaling obstruction，而不是把 \(s^{-1/4}\) 损失隐藏在常数里。

## 11. 发布边界

```text
gaussianStressDuhamel=VERIFIED_CLASSICAL_REDERIVED
deviatoricProductionIdentity=VERIFIED_CLASSICAL_REDERIVED
heatPlaneCharacteristicIdentity=INTERNAL_EXACT_AUDITED
characteristicMeanPayment=INTERNAL_EXACT_AUDITED
energyClassFixedScaleEstimate=INTERNAL_UNCONDITIONAL_AUDITED
energyClassScaleIntegral=INTERNAL_UNCONDITIONAL_AUDITED
centeredIncrementSplit=INTERNAL_EXACT_AUDITED
traceFluxCancellation=INTERNAL_EXACT_AUDITED
gradientCovarianceCarreDuChamp=INTERNAL_EXACT_AUDITED
weightedMeanMultiplierIdentity=INTERNAL_EXACT_AUDITED
criticalHalfScaleAverage=INTERNAL_CRITICAL_AUDITED
rankThreeUniversalSignCounterexample=SEALED_COMMIT_BOUND
universalProductionSign=FALSE
amplitudeIndependentQuadraticAbsorption=FALSE
formalFiniteCertificate=SEALED_COMMIT_BOUND
formalFigurePackage=PENDING
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=false
fixedScaleUniformEnergyClassControl=OPEN
localizedScaleCriticalControl=OPEN
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```
