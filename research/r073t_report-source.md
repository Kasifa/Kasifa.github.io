# R0.73T | Dynamic autocorrelation and the pressure-tensor barrier

**Status:** primary-source audit, exact-certificate final seal, and formal-
figure QA passed; only the public HTML/PDF/deployment transaction remains

**Public title (zh):** R0.73T｜自相关进入动力学：一个临界一侧估计与压力张量障碍

**Date:** 2026-08-31

**Audience:** researchers and technically trained readers following the
periodic three-dimensional Navier--Stokes notes

**Scope:** exact evolution of the scalar energy-density autocorrelation, a
one-sided dynamic consequence of R0.73S, two exact non-autonomy witnesses,
and a shell/heat closure ledger; no arbitrary-data regularity claim

**Normalization:** throughout, \(\mathbb T^3=[0,2\pi]^3\) carries Haar
probability measure \(d\mu=(2\pi)^{-3}dx\); viscosity is \(\nu>0\)

## 1. 直接结论

R0.73S 得到静态证书

\[
 \|u\|_6^6\le A Q,
 \qquad
 Q=\|u\|_4^4,
 \qquad
 A=\sum_h\left|\widehat{|u|^2}(h)\right|.
 \tag{1.1}
\]

R0.73T 问的是：它能不能进入 Navier--Stokes 动力学？答案仍然分成
一条正结果和两条边界。

正结果是

\[
 \boxed{
 Q'+4\nu\int |u|^2|\nabla u|^2
 +\nu\|\nabla |u|^2\|_2^2
 \le {4C_R^2\over\nu}A Q.}
 \tag{1.2}
\]

这是真正的动态化：R0.73S 的二次自相关证书已经出现在一个正确的
\(L^4\) 微分不等式里。

第一条边界是，式 (1.2) 仍需要 \(\int A(t)dt\)。这个积分在
Navier--Stokes 缩放下临界，而且

\[
 \|u(t)\|_\infty^2\le A(t).
 \tag{1.3}
\]

所以 \(A\in L_t^1\) 至少具有经典端点条件
\(u\in L_t^2L_x^\infty\) 的强度，并且直接蕴含该条件。它没有绕开
Serrin 门槛。

第二条边界是，完整的标量自相关也不是自治变量。式 (2.2) 仍需要
带符号向量通量 \(u(w+2p)\)，而标量 \(C\) 不保留其中的速度相位；
另一方面，一般的压力重建还需要完整张量
\(\widehat{u_i u_j}\)，而 \(C\) 只给出它的迹。这是两个不同的信息
缺口。

## 2. 精确自相关演化

令

\[
 w=|u|^2,
 \qquad C(h)=\widehat w(h).
\]

由

\[
 \partial_tu+(u\cdot\nabla)u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0,
\]

得到能量密度方程

\[
 \partial_tw
 =\nu\Delta w-2\nu|\nabla u|^2
 -\nabla\cdot\bigl(u(w+2p)\bigr).
 \tag{2.1}
\]

逐 Fourier 系数因此满足

\[
 \boxed{
 \dot C(h)
 =-\nu|h|^2C(h)
 -2\nu\widehat{|\nabla u|^2}(h)
 -ih\cdot\widehat{u(w+2p)}(h).}
 \tag{2.2}
\]

这条式子已经说明标量 \(C\) 为什么不闭合。粘性部分除了
\(-\nu|h|^2C(h)\)，还需要带绝对频率权重的梯度相关；非线性部分还
需要 \(u(w+2p)\)。即使给定 \(p\)，\(C\) 也不能恢复其中带符号的
速度因子；同时 \(p=R_iR_j(u_i u_j)\) 的一般重建另需完整张量，而
\(C=\widehat{|u|^2}\) 只记录其迹。

把 (2.1) 乘以 \(2w\) 并积分。输运项因无散度而严格抵消，得到

\[
 \boxed{
 Q'+4\nu Y+2\nu X^2
 =4\int p\,u\cdot\nabla w,}
 \tag{2.3}
\]

其中

\[
 X^2=\|\nabla w\|_2^2,
 \qquad
 Y=\int w|\nabla u|^2.
\]

这是经典 \(L^4\) 平衡的自相关重建，不是新的 \(L^p\) 能量定理。

## 3. 一侧动态估计

周期压力满足

\[
 p=R_iR_j(u_i u_j),
 \qquad
 \|p\|_3\le C_R\|u\|_6^2.
 \tag{3.1}
\]

因此

\[
\begin{aligned}
 4\left|\int p\,u\cdot\nabla w\right|
 &\le4C_R\|u\|_6^3X\\
 &\le\nu X^2+{4C_R^2\over\nu}\|u\|_6^6.
\end{aligned}
 \tag{3.2}
\]

再代入 R0.73S 的 \(\|u\|_6^6\le A Q\)，就得到式 (1.2)。若
\(A\in L^1(0,T)\)，Gronwall 给出

\[
 Q(t)\le Q(0)
 \exp\!\left({4C_R^2\over\nu}\int_0^tA(s)\,ds\right).
 \tag{3.3}
\]

但控制 \(A\) 的导数不会关闭问题。其上 Dini 导数引入
\(|\nabla u|^2\) 的 Wiener 范数和带一阶导数的三次压力通量，严格强于
\((A,Q,\|u\|_2)\) 所含信息。

不用 Fourier 支撑可以退回一个分辨率一致的局部估计

\[
 Q'\le C\left(\nu^{-7}Q^3+\nu^{-1}Q^{3/2}\right).
 \tag{3.4}
\]

它的比较 ODE 本身可以有限时爆破，所以只给局部控制，不给全局正则性。

## 4. 为什么这还不是新的正则性门槛

在标准缩放

\[
 u^{[\lambda]}(x,t)=\lambda u(\lambda x,\lambda^2t)
\]

下，

\[
 A^{[\lambda]}(t)=\lambda^2A(\lambda^2t),
 \qquad
 \int_0^{T/\lambda^2}A^{[\lambda]}(t)\,dt
 =\int_0^TA(s)\,ds.
 \tag{4.1}
\]

所以缺失的 \(\int A\) 不是低阶余量，而是临界预算。又因为
\(\||u|^2\|_\infty\le\sum_h|C(h)|\)，

\[
 A\in L_t^1
 \Longrightarrow
 u\in L_t^2L_x^\infty.
 \tag{4.2}
\]

后者正是经典 Prodi--Serrin 缩放线上“时间指数 \(2\)、空间指数
\(\infty\)”的端点，而不是较微妙的
\(L_t^\infty L_x^3\) 端点。因此本节的正结果应这样评价：它把静态
证书接到了动力学，但把真正的难点原样暴露为一个经典强度的临界积分。

The dynamic \(AQ\) inequality is a local synthesis of classical pressure,
\(L^4\)-energy, and autocorrelation estimates; it is not asserted as a new
regularity criterion or a priority theorem.

## 5. 两个精确非自治见证

第一族已经在线性热流中出现：

\[
 v_N=(0,\cos Nx_1,\sin Nx_1).
\]

它们全部满足

\[
 |v_N|^2\equiv1,
 \qquad C(h)=\mathbf1_{h=0},
 \qquad A=Q=1,
\]

而精确解 \(e^{-\nu N^2t}v_N\) 给出

\[
 \dot C(0,0)=-2\nu N^2,
 \qquad Q'(0)=-4\nu N^2.
 \tag{5.1}
\]

所以完整无权自相关丢失载频。

第二个见证针对进入压力配对的带符号速度相位。取

\[
 u(x,y)=
 \bigl(6\sin y-4\sin(x+y),\;4\sin x+4\sin(x+y),\;0\bigr).
 \tag{5.2}
\]

精确有理数卷积得到

\[
 \|u\|_2^2=42,
 \quad Q=2918,
 \quad A=164,
 \quad D_C=15,
 \tag{5.3}
\]

以及

\[
 \mathcal N_4(u)=4\int p\,u\cdot\nabla|u|^2=-384.
 \tag{5.4}
\]

令 \(u_L(x)=u(Lx)\)。式 (5.3) 四个量保持不变，所有速度模态仍在
\([L,\sqrt2L]\) 固定宽比环带中，而

\[
 \mathcal N_4(u_L)=-384L,
 \qquad
 \mathcal N_4(-u_L)=+384L.
 \tag{5.5}
\]

\(u_L\) 与 \(-u_L\) 有完全相同的标量 \(C\)，并且

\[
 (-u_L)\otimes(-u_L)=u_L\otimes u_L,
 \qquad p[-u_L]=p[u_L].
 \tag{5.6}
\]

因此式 (5.5) 的变号只来自 \(p\,u\cdot\nabla|u|^2\) 中带符号的
速度因子。这个证书隔离的是标量 \(C\) 丢失的速度相位；由于这对场的
张量和压力完全相同，它本身不构成“压力张量极化不可辨识”的证明。
一般压力重建需要 \(\widehat{u_i u_j}\) 的事实来自
\(p=R_iR_j(u_i u_j)\)，必须与该符号对证书分开陈述。它们的共同粘性
项按 \(-16536\nu L^2\) 衰减，因此绝不与一侧上界矛盾。

这两个见证都是光滑三角多项式。它们不是奇性、近奇性或爆破解。

## 6. 逐壳输运与 heat 版本

令 \(m_j\) 是固定实自伴 Littlewood--Paley 投影 \(P_j\) 的 Fourier
符号，并定义

\[
 v_j=P_ju,\qquad
 \mathcal F_j=P_j\mathbb P\nabla\cdot(u\otimes u),\qquad
 F_j=\|\mathcal F_j\|_2,
\]

\[
 Q_j=\|v_j\|_4^4,\qquad
 A_j=\sum_h\left|\widehat{|v_j|^2}(h)\right|,
\]

\[
 \mathcal D_j=\int|v_j|^2|\nabla v_j|^2
 +{1\over2}\|\nabla|v_j|^2\|_2^2.
\]

投影的固定环境支撑及其差集记为

\[
 \Sigma_j=\{k\in\mathbb Z^3:m_j(k)\ne0\},
 \qquad
 \overline D_j=|\Sigma_j-\Sigma_j|.
\]

精确逐壳平衡是

\[
 {1\over4}Q_j'+\nu\mathcal D_j
 =-\int |v_j|^2v_j\cdot\mathcal F_j.
 \tag{6.1}
\]

周期频率局部化 nonlinear Bernstein 不等式在 \(p=4\) 给出

\[
 \mathcal D_j\ge c_B2^{2j}Q_j.
 \tag{6.2}
\]

标量定理逐分量应用即可得到这里的向量结论。结合 R0.73S，得到

\[
 D^+(Q_j^{1/2})+2\nu c_B2^{2j}Q_j^{1/2}
 \le2A_j^{1/2}F_j,
 \tag{6.3}
\]

以及固定环境差集分支

\[
 D^+(Q_j^{1/4})+\nu c_B2^{2j}Q_j^{1/4}
 \le \overline D_j^{1/4}F_j.
 \tag{6.4}
\]

这里
\(A_j\le\overline D_j^{1/2}Q_j^{1/2}\)。固定的
\(\overline D_j\) 很重要：若 \(v_j=0\)，则瞬时自相关支撑为空，但
\(D^+\|v_j\|_4\) 仍可能由壳外强迫产生；此时
\(\|\mathcal F_j\|_4\le\overline D_j^{1/4}F_j\) 使式 (6.4) 仍然成立。
这两条都有显式 Duhamel 形式，且固定因子
\(\overline D_j^{1/4}\) 可以安全地放在时间积分外。

剩余强迫只有两个朴素选择：

\[
 F_j\lesssim2^j\|u\|_4^2,
 \qquad
 F_j\lesssim2^{5j/2}\|u\|_2^2.
 \tag{6.5}
\]

第一条重新引入正在输运的全场 \(L_x^4\) 强量；它对应的 Serrin
临界时空预算是 \(u\in L_t^8L_x^4\)，等价于
\(\|u\|_4^2\in L_t^4\)。第二条虽然只用能量，却在高频超临界。这就是
逐壳入口目前尚未闭合的精确位置。

对 \(v_s=e^{s\Delta}u\)，还有二维 heat-plane 恒等式

\[
 (\partial_t-\nu\partial_s)\|v_s\|_4^4
 =-4\int|v_s|^2v_s\cdot
 e^{s\Delta}\mathbb P\nabla\cdot(u\otimes u).
 \tag{6.6}
\]

heat 方向的耗散有正确符号，但
\(e^{s\Delta}(u\otimes u)\ne v_s\otimes v_s\)。剩余对象是一个带符号
双线性 heat commutator。

## 7. 文献归属、精确证书与声明边界

本节保留四层证据。

1. 经典输入：Serrin 的时空正则性门槛、Kato 的 \(L^p\) 耗散结构、
   周期 Riesz 估计，以及 Li、Li--Sire 的频率局部化 Bernstein 理论。
2. 本地解析综合：式 (2.2)、(1.2)、逐壳 Duhamel 形式和 heat-plane
   恒等式的同一归一化重建。
3. 精确有限证书：六模态压力、15 个自相关系数、剪切族、缩放和
   heat 权重全部用 `Fraction` 稀疏卷积复算；最终封印通过 `55/55`
   项检查。配套正式附图通过 `106/106` 项检查，数据账本共有 28 行。
4. 开放结论：\(\int A\) 的任意能量数据控制、可吸收的带符号壳通量、
   临界 heat commutator、任意三维数据全局正则性。

限定式碰撞检索没有发现与“标量能量密度自相关 \(A Q\) + 两个精确
非自治见证”完全相同的打包，但有限检索不是新颖性或优先权证明。本站
只把它称为可审计的本地综合。

精确证书与正式附图都绑定到源码提交
`05c55d21f060a17a0a4db04c12e89e7271b03d30`；科学产物提交为
`29d01625731d1c611f927c2852dbddf05967c6cb`。图件另有一个仅限元数据的
重封提交 `b17c45013cc9a3f6f09efa146bcbc2ef8ab043f9`：它补录由原始日志确定的
运行耗时，以及同机前后夹证的系统、处理器和内存字段；精确数据、验证
结果、PDF、SVG 与 PNG 字节均未改变。这些通过项验证的是有限代数、清单、
哈希与图形交付链，不是对连续方程推导或任意三维数据的数值证明。本节
没有运行 Navier--Stokes 仿真，也没有使用 DGX；普通双语翻译固定在本地
直接完成。

Machine-readable boundary:

```text
exactAutocorrelationEvolution=VERIFIED_CLASSICAL_RECONSTRUCTION
quarticBalance=VERIFIED_CLASSICAL_RECONSTRUCTION
dynamicAQUpperInequality=INTERNAL_COROLLARY
criticalAIntegral=INTERNAL_EXACT_SCALING
criticalAIntegralControl=OPEN
carrierScaleNonAutonomy=CLOSED_EXACT
signedVelocityPhaseInPressurePairing=CLOSED_EXACT
pressureTensorNeededForGeneralReconstruction=VERIFIED_CLASSICAL
shellDuhamelTransport=INTERNAL_CONDITIONAL
finiteFormulaCertificateOnly=TRUE
finiteFormulaDiagnosticValidation=PASS
finiteFormulaDiagnosticChecks=55
formalFigurePackage=PASS
formalFigureChecks=106
formalFigureRows=28
sourceCommitAssigned=TRUE
sourceCommit=05c55d21f060a17a0a4db04c12e89e7271b03d30
scientificArtifactCommit=29d01625731d1c611f927c2852dbddf05967c6cb
figureMetadataResealCommit=b17c45013cc9a3f6f09efa146bcbc2ef8ab043f9
figureMetadataResealScope=ENVIRONMENT_MANIFEST_SUMS_ONLY
figureMetadataBackfill=SAME_HOST_BRACKETED_NOT_ORIGINAL_RUN_EMISSION
finalSeal=TRUE
navierStokesSimulation=NOT_RUN
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=FALSE
publicHtmlRendered=FALSE
publicPdfRendered=FALSE
publicDeploymentCompleted=FALSE
tensorHeatClosure=OPEN
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```

## 8. 研究价值与下一步

这一节的价值不在于把 Clay 问题向“已解决”推进了多少百分比，而在于
把一条看似可闭合的路线分解得足够精确。

- 保留下来的正结果是式 (1.2)：二次自相关确实能支付压力估计中的
  六次矩。
- 被排除的幻想是“只跟踪标量 \(C\) 就能自治”。载频与进入压力配对的
  带符号速度相位都有精确反例；一般压力重建另需完整张量，则由
  \(p=R_iR_j(u_i u_j)\) 直接给出，不能归功于符号对本身。
- 真正的下一对象不再是更多标量摘要，而是带尺度的张量相关
  \(T_{ij}(h)=\widehat{u_i u_j}(h)\)，再配合能被耗散吸收的带符号
  heat commutator 或壳通量估计。

因此 R0.73U 的冻结问题是：能否构造一个保留完整张量信息、
parabolic-scale aware 的 heat hierarchy，使压力项的符号信息保留下来，
同时其代价仍处在 R0.73Q/R0.73R 的临界指数内？

在这条新引理出现之前，任意三维初值的全局光滑性与 Clay 千禧年问题
保持 OPEN。
