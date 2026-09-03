# R0.74W｜远端相邻内壳 common-shear 阈值与加权端点阻断

## 1. 结论先行：严格阈值，而不是近叶估计的直接复用

本节在冻结的 two-packet exact smooth common-shear family 内，完成 R0.74V 的第一个 remote endpoint comparison。结论是相对于 free derivative-heat comparator 的 survival/sweeping 尺度二分；它不是绝对 (o(1)) 代换，也不是任意 suitable weak solution 的结论。

\[
p=\frac1\lambda=\frac{32}{63},\qquad q(\ell)=\frac{p^2}{4\ell},\qquad q_{64}=\frac4{3969},\qquad q_{65}=\frac{256}{257985}<q_{64}.
\]

在 central conditional bridge 概率下，若 (t=\tau_m=\ell R^2)、(64\le\ell\le65)，则

\[
\mathbb P_{0,y}^{\rm br}\!\left\{e^{-(q(\ell)+\eta)L^2}\le\mathfrak S_t\le e^{-(q(\ell)-\eta)L^2}\right\}\longrightarrow1\qquad(\eta>0).
\]

这是概率意义的 logarithmic asymptotic，不是 deterministic prefactor asymptotic。位移 deficit 使用 age (t=\ell R^2)；free heat comparator 的总 age 是 (T=(\ell+1)R^2)，两者不得混同。

## 2. 冻结 family 与显式 remote strip

沿用

\[
\lambda=\frac{63}{32},\quad c_h=\frac{15}{16},\quad d=c_h-p=\frac{433}{1008},\quad L_2=2L_1,\quad h_m=c_hL_mR,
\]

以及 (L_1\ge9216)、(L_2R\le5/144) 和 (R^{-1}e^{-a_SL_1^2}\to0)，其中 (a_S=75/22528)。在 (t=\tau_m) 时定义

\[
\mathcal S_m=\left\{x:\ |x_1|<\frac14\sqrt{pL_m}R,\ \frac54R<x_2<\frac32R,\ pL_mR-R<x_3<pL_mR-\frac12R\right\}.
\]

直接几何计算给出

\[
\mathcal S_m\subset A_{k_m-1}(R),\qquad \Psi_{k_m-1}^R=1\ \text{on }\mathcal S_m,\qquad |\mathcal S_m|=\frac1{16}\sqrt{pL_m}\,R^3.
\]

令 (z=x_2)、(y=x_3-h_m=-(dL+\delta)R) 且 (1/2<\delta<1)。free comparator 为

\[
H_m(t,z,y)=R^3\partial_zK_{R^2+t}^{\rm per}(z)K_{R^2+t}^{\rm per}(y),\qquad |H_m|\asymp e^{-(dL+\delta)^2/[4(1+\ell)]}.
\]

## 3. 精确 all-winding 条件桥表示

对 direct positive packet，时间反向 Feynman--Kac 表示保留每一个 vertical winding：

\[
G_m^+(t,Q_m(t)+z,h_m+y)=R^3\sum_{n\in\mathbb Z}w_n\,\mathbb E_{n,y}^{\rm br}\!\left[\partial_zK_T^{\rm per}(z+\mathfrak S_t)\right],
\]

\[
w_n=k_T(2\pi n-y),\qquad T=t+R^2,\qquad \mathfrak S_t=B\int_0^t\!\left[\theta_R(t-s,h_m)-\theta_R(t-s,h_m+Y_s)\right]ds.
\]

相应 free comparator 是

\[
H_m=R^3\partial_zK_T^{\rm per}(z)\sum_{n\in\mathbb Z}w_n.
\]

因此比较必须除以完整 winding sum。非中心质量没有被删除，而是满足

\[
\omega_{\rm per}:=\frac{\sum_{n\ne0}w_n}{w_0}\le C\exp\!\left[-\frac1{11R^2}\right]\le Ce^{-75L^2}=o(1).
\]

## 4. remote saturation deficit 与短时层

令 (A(r,x)=1-\theta_R(r,x)\ge0)。上、下周期 Gaussian 界在 (x=pLR+O(R))、(r=\ell R^2) 给出同一指数：

\[
-\frac1{L^2}\log A(\ell R^2,pLR+O(R))\longrightarrow q(\ell)=\frac{p^2}{4\ell}.
\]

central bridge 的半群恒等式为

\[
\mathbb E_{0,y}^{\rm br}A(t-s,h_m+Y_s)=A(t-s+v_s,h_m+\mu_s),\quad \mu_s=\frac{T-s}{T}y,\quad v_s=\frac{s(T-s)}T.
\]

指数差把积分局部化到 (s\asymp R^2/L^2) 的短时层，因而

\[
\mathbb E_{0,y}^{\rm br}|\mathfrak S_t|\le CL^{-2}e^{-q(\ell)L^2+CL}+Ce^{-c_h^2L^2/260+CL}.
\]

反向的高概率下界来自同一短时层；对足够小的固定 (epsilon>0)，

\[
\mathfrak S_t\ge cL^{-2}\exp\!\left[-\frac{(p+\epsilon)^2}{4\ell}L^2-CL\right]>0
\]

以 (1-Ce^{-c\epsilon^2L^4}) 的 central-bridge 概率成立。这里没有假设冻结 saturation profile 单调。

## 5. relative survival、uniform slab 与 sweeping

若

\[
\frac1{RL^2}e^{-q(\ell)L^2+C_0L}\longrightarrow0,
\]

则在 remote strip 上

\[
\sup_{x\in\mathcal S_m}\left|\frac{G_m^+(t,x_2,x_3)}{H_m(t,x_2,x_3-h_m)}-1\right|\longrightarrow0.
\]

特别地，uniform slab survival 的充分条件是

\[
\limsup\frac{\log(1/R)}{L^2}<q_{65}.
\]

反之，若 (\ell_j\to\ell_\infty\) 且

\[
\liminf\frac{\log(1/R_j)}{L_j^2}>q(\ell_\infty),
\]

则 (G_m^+/H_m\to0)；在全 slab 上统一成立的充分条件是

\[
\liminf\frac{\log(1/R)}{L^2}>q_{64}.
\]

窄带 (q_{65}\le\log(1/R)/L^2\le q_{64}) 不能整体称作“未分类”：固定极限 (\ell) 时，与 (q(\ell)) 的严格比较仍决定一侧；只有 equality 及其 critical law 保持 OPEN。

## 6. inversion、另一 packet 与 amplitudes 之后的非抵消

物理第一分量是

\[
U=\mathfrak a_1(G_1^++G_1^-)+\mathfrak a_2(G_2^++G_2^-),\qquad \frac{\mathfrak a_2}{\mathfrak a_1}=2^{-1/2}e^{3q_{64}L_1^2}.
\]

inversion partner 与 cross-packet 项必须在插入实际 amplitudes 后比较。冻结精确 margins 为

\[
\frac5{693}>0,\qquad \delta_{1\leftarrow2}=\frac{100043}{29804544}>0,\qquad \delta_{2\leftarrow1}=\frac{3667}{17611776}>0.
\]

连同 periodic-copy reserve，它们给出

\[
\frac{\mathfrak a_{3-m}|G_{3-m}|+\mathfrak a_m|G_m^-|}{\mathfrak a_m|H_m|}\longrightarrow0.
\]

这是一条 amplitude-weighted relative noncancellation statement，不是未加权的 absolute (o(1))。

## 7. 冻结尺度上两 packet 的相反结果

对 outer packet (m=2)，

\[
4q_{65}-a_S=\frac{3719797}{5811886080}>0
\]

把 R0.74U reserve 转成全 slab survival，故

\[
\sup_{x\in\mathcal S_2}\left|\frac{U(t,x)}{\mathfrak a_2H_2(t,x_2,x_3-h_2)}-1\right|\longrightarrow0.
\]

inner packet 在一般冻结假设下没有统一结果。对原始尺度 (R=e^{-L_1^2/320})，精确 margins

\[
\frac1{320}-q_{64}=\frac{2689}{1270080}>0,\qquad q_{65}-\frac1{1280}=\frac{13939}{66044160}>0
\]

给出 packet 1 swept、packet 2 survives：

\[
\frac{U}{\mathfrak a_1H_1}\longrightarrow0\ \text{on }\mathcal S_1,\qquad \frac{U}{\mathfrak a_2H_2}\longrightarrow1\ \text{on }\mathcal S_2.
\]

## 8. 加权端点发散与 fixed-deletion 边界

相邻内壳权重满足

\[
\frac{\gamma_{k_m-1}}{\Gamma_m}=e^{(3/4)c_\gamma L_m^2}.
\]

packet 2 的 relative survival、remote strip 体积和 completed-clock 非负 endpoint row 合并为

\[
\boxed{\frac{K_{k_2-1,R}(\tau_2)}{T_*}\ge cL_2^{-1/2}e^{\chi(65)L_2^2-CL_2}\longrightarrow\infty,\qquad \chi(65)=\frac{12191}{132088320}>0.}
\]

因此 matching all-shell (O(T_*)) upper bound 对这个 frozen placement 为 FALSE。但唯一发散坐标是 (k_2-1=k_1)，one-shell fixed deletion 可以恰好删去它；所以 fixed-deletion obstruction、whole-shell upper、time occupation、accumulated viscosity 与 target-coordinate duration 都没有被证明。

## 9. 四联图、证书与文献边界

冻结四联图只展示 derived analytic values：Panel A 是 physical-shell schematic；Panel B 是 (q(\ell)) 阈值；Panel C 是 exact all-winding bridge proof map；Panel D 是 leading analytic endpoint factor。它没有 sampled path、PDE data、DNS 或 finite-(L_2) numerical lower certificate。

- primary analytic audit：PASS，0 blockers；
- Python certificate：33/33 checks，33 exact cases；
- independent Ruby：6/6 groups，56 assertions；
- negative mutations：Python 23/23、Ruby 24/24 rejected；
- seeds 0、1、42 与 independent regeneration：byte-identical；
- literature：截至 2026-09-03 的 bounded primary-source screen 仅给 finite non-hit，不证明 novelty、priority、correctness、nonexistence 或 publishability。

## 10. 停止线与开放问题

本节只对一个 frozen exact smooth common-shear family 建立 remote adjacent-inward relative comparison，并由 packet 2 导出一个 frozen-placement all-shell upper obstruction。

- PROVED：exact all-winding disintegration；central-bridge logarithmic rate；严格阈值两侧的 relative survival/sweeping；amplitude 后的 inversion/cross-packet noncancellation；packet-2 加权 endpoint divergence。
- OPEN：critical equality law；fixed deletion；whole-shell (H^1) occupation；time occupation；positive-variation upper；accumulated viscosity；payment normalization；arbitrary-clock extraction；scale contraction；一般 suitable weak solutions；regularity 与 singularity。
- PUBLICATION BOUNDARY：ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | LOCAL DIRECT TRANSLATION | NO DGX | NOT CLAY。

这不是 Navier--Stokes Millennium problem 的解决，也不声称构造了一般解的反例。**NOT CLAY.**
