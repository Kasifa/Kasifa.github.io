# R0.74T Step 19 中文读者版

## 136. 结果与精确范围：错开峰值不能消除普通驻留的付款

Step 18 把 fixed-deletion 路线归约到 completed-clock simultaneous height

\[
\mathfrak L^K_{N,R}(D):=\inf_{\#S\le N}\sup_{t\in D}\sum_{k\notin S}K_{k,R}(t).
\]

互不相交的 triangular clocks 说明，不同壳层原则上可以在不同时间达到峰值。Step 19 检查更窄的问题：只把两个 packet lobe 的目标时间错开，能否让 completed-clock witness 相对于 Version-M payment 变便宜？

答案只在明确的 lobe-floor 层面给出，而且是否定的：只要保留既有 outer-lobe 几何和不可忽略的驻留时间，外叶的正动能下界就会被非负 velocity-cubic payment 强制支付。这个结论不需要内叶与外叶同时出现。

本节证明四件事：持续 \(\theta R^3\) 的 outer lobe 产生精确 Hölder coercivity；任意甚至互不相交的两个正 K-clock floor 只产生 fixed-deletion completed-clock witness；既有相邻壳参数下，低付款要求归一化 dwell 指数坍缩；同一个 exact smooth periodic unforced common-shear Navier--Stokes 解确实能够实现两个互不相交的 \(R^3\) lobe windows，但它的 payment-to-witness ratio 发散。

这里没有 full completed-clock upper bound，没有把 \(K\) 替换成 \(\mathfrak H^{\rm fix}\)，没有任意实时间 scheduling theorem，也没有正则性或奇性结论。NOT CLAY。

## 137. 冻结的 Version-M 设置与 persistent outer-lobe floor

固定 \(R>0\)、终端时刻 \(t_0\)，以及 R0.74P Version-M 设置中的一个光滑、周期、无外力 Navier--Stokes 解。完整付款含有非负 exterior velocity row

\[
P_R^M\ge \mathcal G_u,
\qquad
\mathcal G_u=(2R)^{-2}\int_{I_{2R}}\!\int_{\mathbb T^3}W_{2R}(x)|u(t,x)|^3\,dx\,dt.
\tag{T.1}
\]

对 outer target shell \(k_2\)，记

\[
L_2=\lambda2^{k_2},\qquad \Gamma_2=\gamma_{k_2}=e^{-c_\gamma L_2^2}.
\tag{T.2}
\]

R0.74Q 的物理 lobe 位于 \(A_{k_2}(R)=A_{k_2-1}(2R)\)，因此该区域上

\[
W_{2R}\ge\gamma_{k_2-1}=\Gamma_2^{1/4}.
\tag{T.4}
\]

取可测集合 \(J_2\subset I_R\subset I_{2R}\)，令 \(|J_2|=\theta R^3\)。对几乎处处的 \(t\in J_2\)，假设 moving lobe \(\Omega_2(t)\) 联合可测，并满足

\[
\Omega_2(t)\subset A_{k_2}(R),\qquad
|\Omega_2(t)|=\frac1{16}L_2R^3,\qquad
\Psi_{k_2}^R=1\ \hbox{on }\Omega_2(t).
\tag{T.6}
\]

定义 persistent normalized lobe kinetic floor

\[
h_2:=\operatorname*{ess\,inf}_{t\in J_2}
\frac{\Gamma_2}{2R}\int_{\Omega_2(t)}|u(t,x)|^2\,dx>0.
\tag{T.7}
\]

由于 defect-completed clock 是非负端点动能项与累积耗散项之和，\(J_2\subset I_R\) 上的时间 cutoff 等于一，所以 \(K_{k_2,R}(t)\ge h_2\) 几乎处处成立。

## 138. Schedule-invariant outer-lobe Hölder coercivity

空间 Hölder 不等式给出

\[
\int_{\Omega_2(t)}|u|^3
\ge |\Omega_2(t)|^{-1/2}
\left(\int_{\Omega_2(t)}|u|^2\right)^{3/2}.
\tag{T.11}
\]

代入冻结的 lobe volume 与 kinetic normalization，得到

\[
\int_{\Omega_2(t)}|u|^3
\ge2^{7/2}h_2^{3/2}\Gamma_2^{-3/2}L_2^{-1/2}.
\tag{T.12}
\]

把 T.1 的非负积分限制到 moving lobe，再使用 weight floor 与 \(|J_2|=\theta R^3\)，得到 Step 19 的核心估计

\[
\boxed{P_R^M\ge2\sqrt2\,\theta h_2^{3/2}R
\Gamma_2^{-5/4}L_2^{-1/2}.}
\tag{T.9}
\]

等价地，令

\[
\Lambda_2:=\theta^{2/3}R^{2/3}\Gamma_2^{-5/6}L_2^{-1/3},
\]

则

\[
\boxed{(P_R^M)^{2/3}\ge2\Lambda_2h_2.}
\tag{T.10}
\]

证明中没有出现内 packet、内叶目标时间或两个目标区间的交叠。因此，只要 outer-lobe hypotheses 保持成立，估计对相对 schedule 不变。

若只知道 \(W_{2R}\ge c_W\Gamma_2^{1/4}\) 和 \(|\Omega_2(t)|\le C_\Omega L_2R^3\)，同一证明给出

\[
P_R^M\ge2^{-1/2}c_WC_\Omega^{-1/2}
\theta h_2^{3/2}R\Gamma_2^{-5/4}L_2^{-1/2}.
\tag{T.15}
\]

取 \(c_W=1\)、\(C_\Omega=1/16\) 就精确恢复 T.9。

## 139. 两枚可能不同时的 K-clock floor：只能推出 one-deletion witness

令 \(k_1\ne k_2\)，并在任意可测正测度集合 \(J_i\subset D\) 上假设

\[
K_{k_i,R}(t)\ge h_i>0\quad\hbox{a.e. on }J_i,\qquad i=1,2.
\tag{T.16}
\]

不要求 \(J_1\) 与 \(J_2\) 相交。任意 \(\#S\le1\) 的删除集合至少留下 \(k_1,k_2\) 中的一枚；在该坐标自己的目标时间集合取值并利用全部 clock 的非负性，便得到

\[
\boxed{\mathfrak L^K_{1,R}(D)\ge h_*:=\min(h_1,h_2).}
\tag{T.17}
\]

如果 outer floor 满足 \(h_2\ge h_*\)，T.10 进一步给出

\[
\boxed{(P_R^M)^{2/3}\ge2\Lambda_2h_*.}
\tag{T.18}
\]

这两式只能作单向解释。\(h_*\) 是 \(\mathfrak L^K_{1,R}\) 的一个下界 witness；其他时间、壳层或累积耗散可能让 full functional 更大。因此不能把 T.18 改写成 \((P_R^M)^{2/3}\gtrsim\mathfrak L^K_{1,R}(D)\)。

同样不能把 T.17 中的 completed clock \(K_k\) 替换成 Step 18 的 stopped forward-flux functional \(\mathfrak H^{\rm fix}\)。两者之间已证明的桥必须保留 Step 18 的 payment terms 和原方向。

## 140. 指数 dwell threshold

沿 \(L_{1,n}\to\infty\) 的序列，采用既有相邻壳参数

\[
L_2=2L_1,\qquad
\Gamma_2=e^{-c_\gamma L_2^2},\qquad
S=\log(1/R),
\]

其中

\[
c_\gamma=\frac8{3969},\qquad a_S=\frac{75}{22528}.
\tag{T.21}
\]

R0.74F 的 inherited sufficient bridge-survival window 是 \(S-a_SL_1^2\to-\infty\)。它只是该证明的充分条件，不是所有 packet 的必要条件。记

\[
d_L:=a_SL_1^2-S\to+\infty.
\tag{T.23}
\]

代入 \(\Lambda_2\) 后得到精确恒等式

\[
\boxed{\log\Lambda_2=\frac23\left[
\log\theta+(5c_\gamma-a_S)L_1^2+d_L-\frac12\log L_2\right].}
\tag{T.24}
\]

指数余量严格为正：

\[
\boxed{5c_\gamma-a_S
=\frac{603445}{89413632}>0.}
\tag{T.25}
\]

所以 \(\theta=1\) 时 \(\Lambda_2\to\infty\)。更一般地，如果要让 \((P_{R_n}^M)^{2/3}/h_{*,n}\) 保持有界，T.18 首先强迫 \(\Lambda_{2,n}=O(1)\)，进而得到必要的 dwell ceiling

\[
\boxed{\theta_n\le C L_{2,n}^{1/2}
e^{-(5c_\gamma-a_S)L_{1,n}^2-d_{L,n}}.}
\tag{T.28}
\]

等价的对数形式为

\[
\boxed{\log\theta\le-(5c_\gamma-a_S)L_1^2-d_L
+\frac12\log L_2+O(1).}
\tag{T.29}
\]

既有 R0.74F/R0.74Q lobe interval 的 \(\theta=1\)。任意移动内叶都不会进入 T.24，也不能改变结论。真正的逃逸必须让 maximal comparable-floor persistence 本身指数缩短，而不是只在分析中截取一个早已长时间存在的 lobe。

## 141. Packet-amplitude 恢复与 abstract sharpness

在 exact common-shear packet family 中，all-lobe dominance 给出 \(|u|\ge c_0\mathfrak a_2\)，因此

\[
h_2\ge c\Gamma_2\mathfrak a_2^2L_2R^2.
\tag{T.30}
\]

代入 T.9，恢复任意 normalized dwell 下的 amplitude formula

\[
P_R^M\ge c\theta\mathfrak a_2^3\Gamma_2^{1/4}L_2R^4.
\tag{T.31}
\]

\(\theta=1\) 时这正是 R0.74Q (Q.168)。关键澄清是：coercive step 只需要 outer lobe，不需要它与其他目标同时出现。

T.9 的各个幂次在纯测度论假设下是 sharp 的。取一个时空矩形，在其上令 lobe 体积、时间长度、shell weight 固定，并让向量场为常数，空间 Hölder 取等号，便精确得到

\[
\theta^1h_2^{3/2}R^1\Gamma_2^{-5/4}L_2^{-1/2}.
\tag{T.33}
\]

固定瞬时高度而令 \(\theta\downarrow0\)，cubic payment 随 \(\theta\) 线性消失，说明 peak-only estimate 不能替代 persistence input。这些矩形只是 ABSTRACT SHARPNESS TESTS：不是周期散度自由解，不实现 Version-M ledger，也不是 Navier--Stokes counterexample。

## 142. 同一个 exact common-shear 解中的 asynchronous lobe construction

沿上一节序列，另行保留中央 chart 与 common-shear platform 条件：\(L_2=2L_1\)、\(R\le1/32\)、\(L_2R\le5/144\)、\(L_1\ge9216\)，以及 \(R^{-1}e^{-a_SL_1^2}\to0\)。

在 terminal slab \(I_R=(64R^2,65R^2)\) 内任选 \(0<\theta_i\le1\) 与 terminal times \(\tau_i\)，使

\[
J_i=(\tau_i-\theta_iR^3,\tau_i)\subset I_R.
\tag{T.35}
\]

定义相应水平预移位

\[
q_{{\rm pre},i}:=-B\int_0^{\tau_i}\theta_R(s,y_i^\circ)\,ds,
\qquad
Q_i(t)=q_{{\rm pre},i}+B\int_0^t\theta_R(s,y_i^\circ)\,ds.
\tag{T.36}
\]

于是 \(Q_i(\tau_i)=0\)，并且在 \(J_i\) 上有 \(|Q_i(t)|\le R/64\)。水平平移与 common scalar advection-diffusion equation 对易，inversion partner 保持完全奇对称，因此有限和

\[
u=(\mathfrak a_1G_1+\mathfrak a_2G_2,b,0),\qquad p=0
\tag{T.39}
\]

仍是同一个 exact smooth periodic mean-zero unforced Navier--Stokes solution。这里没有把在不同 shear 下演化的两个独立解相加。

既有 shear error、heat-age reserve、inversion suppression、vertical cross-tail 与 annular margins 对两枚 admissible target times 都统一成立。特别地，每个 \(J_i\) 都携带目标 lobe，且

\[
K_{k_i,R}(t)\ge cA_*^2R^2=cT,
\qquad
\mathfrak L^K_{1,R}(I_R)\ge cT.
\tag{T.41}
\]

这个结论只允许在 stated slab 内选择相对 schedule；它不是已演化解的独立时间平移，也不是任意实目标时间定理。

## 143. 两个严格分离的 unit-dwell windows 仍然昂贵

当 \(R<1/3\) 时取

\[
\theta_1=\theta_2=1,\qquad
\tau_1=64R^2+2R^3,\qquad
\tau_2=65R^2.
\tag{T.42}
\]

则

\[
J_1=(64R^2+R^3,64R^2+2R^3),\qquad
J_2=(65R^2-R^3,65R^2)
\]

都位于 \(I_R\)，且两者间隔精确为 \(R^2-3R^3>0\)。它们是同一 common-shear solution 中两个真正互不相交的 \(R^3\)-long lobe windows。

然而 outer interval 仍有 \(\theta_2=1\)，所以 T.24-T.26 给出

\[
\frac{(P_R^M)^{2/3}}{T}\longrightarrow\infty.
\tag{T.43}
\]

这个 construction 证明 asynchronous clock floors 可以实现，却不能把这些 floors 变成 low-payment witness。它排除的只是“普通 \(R^3\) 驻留加错峰”这一条明确机制，不是所有可能的 asynchronous PDE 构造。

## 144. 一手文献的有限未命中边界

Hölder 本身与把非负积分限制到一个可测集合，都是经典测度论事实，不带 novelty claim。2D3C/passive-component reduction、parallel Kelvin waves、prescribed periodic shear 下的 scalar dispersion、forced passive-scalar mixing blocks、alternating-shear time schedules，以及 physical-shell flux locality，也都必须作为既有机制归属到相应文献。

本次两轮有界检索只核对六组一手来源：Singh-Sridhar；Biferale-Buzzicotti-Linkmann；Jiménez-Urias-Haine；Bruè-De Lellis；Bruè-Colombo-Crippa-De Lellis-Sorella；Dascaliuc-Grujić。

检索没有找到同时包含以下六项的 theorem：同一 exact common-shear/unforced solution 内的多个 passive packets；stated slab 内可独立选择的目标窗口；统一的 total-field physical lobe floor；对非负 weighted exterior \(|u|^3\) payment 的转换；互不相交时间窗口仍给 completed-clock fixed-deletion floor；由既有 shell weight 与 survival window 导出的指数 dwell threshold。

这个结论只能写成 six-source bounded non-hit。它不证明 novelty、priority、correctness、optimality 或 publishability，也没有穷尽 MathSciNet、zbMATH、完整引用图、学位论文、非英语来源和未公开材料。LITERATURE BOUNDARY。

## 145. Claim ledger、证书与下一边界

- PROVED：T.9-T.10 的 exact outer-lobe Hölder coercivity，以及在 lobe hypotheses 保持时对相对 target-time schedule 的不变性。
- PROVED：同一个 exact common-shear solution 中两个 disjoint admissible lobe windows，T.34-T.43。
- PROVED：T.17 的 two-clock completed-height witness；对象严格是 K-clock，不是 stopped flux。
- PROVED：T.24-T.29 的 logarithmic dwell identity 与必要 collapse threshold；并且 measure-theoretic class 内各幂次 sharp。
- INHERITED：Version-M payment、shell weights、exact common-shear finite-packet solution、R0.74F/R0.74Q lobe placement 与 sufficient bridge-survival proof window。
- FINITE COMPUTATION：Python 31/31 groups、18,933 cases；independent Ruby 11/11 groups、9,201 assertions；Python/Ruby 分别拒绝 26/26 与 27/27 mutations；三组 PYTHONHASHSEED 与独立 Ruby regeneration 均逐字节一致。
- FIGURE：25 文件、47 checks、18/18 deterministic-core hashes；ANALYTIC SCHEMATIC / DERIVED ANALYTIC VALUES / NOT PDE DATA / NOT DNS / NOT CLAY。
- OPEN：stated slab 外的 scheduling；指数短 maximal comparable-floor persistence 的 PDE 构造；full \(\mathfrak L^K_{1,R}(D)\) 的 payment-scale upper bound；off-target clocks 与 accumulated dissipation；无 Step 18 payment terms 的 K-to-\(\mathfrak H^{\rm fix}\) bridge；fixed-deletion、direct hybrid、Q.12、Q.1、scale contraction、regularity 与 singularity。

下一条可检验路线必须真正构造 maximal outer comparable-floor persistence 指数缩短、且更长区间上没有可比 floor 的 packet；或者放弃一个既有 shell-weight、survival 或 lobe-floor 假设。只改变两个普通 \(R^3\)-long lobes 的先后顺序，或在分析中截短它们，不再是一条可行逃逸路线。

本节是 local coercivity theorem 与 route reduction，不是 full-clock theorem，更不是 Millennium problem 的解答。NOT CLAY。
