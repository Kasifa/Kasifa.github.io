# R0.74X｜三 packet fixed-deletion endpoint obstruction 与 cubic-payment gate

## 1. 结论先行：两坐标 endpoint obstruction 已证，actual gate 反例未证

本节只讨论一个 frozen three-packet exact smooth periodic common-shear family。它把 R0.74W 的一个发散坐标扩展为两个不同的发散坐标，但随后证明这两个 audited W-strip witnesses 仍不足以击败 actual cubic-payment normalization。

\[
\boxed{\begin{gathered}\textbf{TWO-COORDINATE ENDPOINT OBSTRUCTION RELATIVE TO }T_*\textbf{: PROVED,}\\[2pt]\textbf{ACTUAL }(P_R^M)^{2/3}\textbf{-NORMALIZED COUNTEREXAMPLE: NOT PROVED,}\\[2pt]\textbf{EQUAL-TARGET W-STRIP ROUTE: NO-GO BY CUBIC PAYMENT.}\end{gathered}}
\]

这不是 whole-shell clock upper/lower theorem，不控制 accumulated dissipation，也不是任意 suitable weak solution、regularity 或 singularity 结论。**NOT CLAY.**

## 2. 三 packet 精确 family 与共同归一化

取

\[
k_2=k_1+1,\qquad k_3=k_1+2,\qquad L_2=2L_1,\qquad L_3=4L_1,
\]

并在同一 heat-evolved shear (b) 下重演化三个 inversion-paired derivative-heat packets：

\[
U_3=\sum_{m=1}^3\mathfrak a_mG_m,\qquad u^{(3)}=(U_3,b,0),\qquad p^{(3)}=0,
\]

\[
\Gamma_m=e^{-c_\gamma L_m^2},\qquad \mathfrak a_m=A_*(\Gamma_mL_m)^{-1/2},\qquad \Gamma_m\mathfrak a_m^2L_mR^2=A_*^2R^2=:T_*.
\]

这是 exact smooth periodic unforced Navier--Stokes solution。equal target-clock normalization 不等于 equal raw-energy normalization；改变共同振幅 (A_*) 不能修复后文的 payment ratio。

## 3. remote strips、relative survival 与完整 cross audit

对 (m=2,3)，使用 R0.74W 的 adjacent-inward strip

\[
\mathcal S_m=\left\{x:\ |x_1|<\frac14\sqrt{pL_m}R,\ \frac54R<x_2<\frac32R,\ pL_mR-R<x_3<pL_mR-\frac12R\right\}.
\]

outermost chart 条件 (L_3R\le5/144) 与 inherited U-reserve 给出

\[
4q_{65}-a_S=\frac{3719797}{5811886080}>0,\qquad 16q_{65}-a_S=\frac{72925813}{5811886080}>0.
\]

因此 packets 2、3 都在 full closed slab 上 relatively survive。插入真实 amplitudes 后，四个正 cross margins 为

\[
\delta_{2\leftarrow1}=\frac{3667}{70447104},\quad \delta_{2\leftarrow3}=\frac{100043}{29804544},\quad \delta_{3\leftarrow2}=\frac{3667}{70447104},\quad \delta_{3\leftarrow1}=\frac{147359}{281788416}>0.
\]

inversion margin (5/693>0)，noncentral winding reserve (123450676/1091475>0)。所以 inversion partners、相邻与非相邻 cross packets、全部 periodic windings 都已按 amplitude-weighted 比较控制；这里没有 diagonal-only 假设。

## 4. 两个不同坐标的 T-star endpoint 发散

adjacent-shell weight、strip volume、free kernel 与共同 (T_*) 归一化给出

\[
K_{k_m-1,R}(\tau_m)\ge cT_*L_m^{-1/2}e^{\chi(65)L_m^2-CL_m},\qquad m=2,3,
\]

\[
\chi(65)=\frac{12191}{132088320}>0.
\]

因为 (k_2-1=k_1)、(k_3-1=k_2)，得到两个 distinct coordinates：

\[
\frac{K_{k_1,R}(\tau_2)}{T_*}\longrightarrow\infty,\qquad \frac{K_{k_2,R}(\tau_3)}{T_*}\longrightarrow\infty.
\]

这些是 explicit strip lower witnesses。它们不提供任一 whole-shell upper bound。

## 5. fixed deletion 的量词次序：时间可以不同

实际 budget-one deletion functional 是

\[
\boxed{\mathfrak L^K_{1,R}(\mathcal D)=\inf_{\substack{S\subset\mathbb N\\ \#S\le1}}\sup_{t\in\mathcal D}\sum_{k\notin S}K_{k,R}(t).}
\]

删除集 (S) 必须先固定，之后才取时间上确界。于是无论删除哪个坐标，另一个 witness 都可在自己的时间被选中：

\[
\mathfrak L^K_{1,R}(\mathcal D)\ge\min\{K_{k_1,R}(\tau_2),K_{k_2,R}(\tau_3)\}.
\]

令 (\mathcal D=\mathcal T_R)，便有

\[
\boxed{\frac{\mathfrak L^K_{1,R}(\mathcal T_R)}{T_*}\longrightarrow\infty.}
\]

(\tau_2) 与 (\tau_3) 可以不同；simultaneity 不是证明所需。可选地令二者相等，也可得到同一 smooth time 的 simultaneous vector-height statement。若 deletion set 被错误地允许依赖时间，上述 pigeonhole 会失效。

## 6. actual gate 使用 cubic-payment normalization

真正待检验的不等式不是 (O(T_*))，而是

\[
\mathfrak L^K_{1,R}(\mathcal T_R)\le C_L^{2/3}(P_R^M)^{2/3}.
\]

packet 3 的 target lobe 在 payment radius (2R) 上满足

\[
A_{k_3}(R)=A_{k_3-1}(2R),\qquad \gamma_{k_3-1}=\Gamma_3^{1/4}.
\]

三 packet amplitude-weighted target-lobe dominance 与 nonnegative exterior velocity-cubic row 强制

\[
P_R^M\ge c\mathfrak a_3^3\Gamma_3^{1/4}L_3R^4=cA_*^3R^4\Gamma_3^{-5/4}L_3^{-1/2},
\]

所以

\[
\boxed{\frac{(P_R^M)^{2/3}}{T_*}\ge cR^{2/3}L_3^{-1/3}e^{(5/6)c_\gamma L_3^2}.}
\]

该比值中的 (A_*) 精确抵消，不能通过共同振幅调节消除。

## 7. payment rate 严格压过两个 audited W-strip rates

写 (\rho_R=\log(1/R)/L_1^2)。U-reserve 给出 (\rho_R\le a_S+o(1))，从而 payment lower rate 是

\[
\frac{40}{3}c_\gamma-\frac23a_S=\frac{3306805}{134120448}>0.
\]

最大的 audited W-strip exponent 是

\[
16\chi(66)=\frac{244208}{134120448},\qquad \chi(66)=\frac{15263}{134120448}.
\]

二者严格 gap 为

\[
\boxed{\frac{3306805-244208}{134120448}=\frac{3062597}{134120448}>0.}
\]

因此对两个实际 strip integrals，

\[
\boxed{\frac{E_2^{\rm strip}+E_3^{\rm strip}}{(P_R^M)^{2/3}}\longrightarrow0.}
\]

这只是 two-strip upper comparison，不是 whole-shell clock upper bound，也不排除尚未证明的 whole-shell 或 accumulated-dissipation effect。

## 8. precise no-go 与 next proposition X.52

本节精确排除的是 equal-target three-packet W-strip architecture：两个 endpoints 相对 (T_*) 发散，但外 packet 的 cubic payment 具有更大指数，因此这两个 witnesses 不可能反驳 actual normalized gate。

下一构造目标必须直接满足

\[
\boxed{\frac{\min\{K_{r,R}(t_r),K_{s,R}(t_s)\}}{(P_R^M)^{2/3}}\longrightarrow\infty,\qquad r\ne s,\quad t_r,t_s\in\mathcal T_R.}
\]

这就是 X.52。它不要求 (t_r=t_s)，但必须把两个 undeletable clock heights 与 outer exterior cubic payment 解耦。改变 amplitude law、shell placement、weight interaction 或 packet geometry 都需要新的 exact normalization、survival proof 与 all-cross-packet audit。

## 9. 冻结四联图、证书与 bounded literature screen

四联图只编码 analytic scale index、different-time fixed-deletion pigeonhole、exact exponent comparison 与 claim hierarchy；没有 sampled trajectories、PDE data、DNS 或 simulation。

- primary analytic audit：PASS，0 blockers；
- Python certificate：31/31 checks，231 exact cases/assertions；
- independent Ruby：5/5 groups，36 assertions；
- negative mutations：Python 24/24、Ruby 25/25 rejected；
- seeds 0、1、42 与 independent regeneration：byte-identical；
- figure archive：25 files、3,096,940 bytes，deterministic 18/18，visual QA PASS；
- literature：截至 2026-09-03 的 bounded primary-source screen 仅给 finite non-hit，不证明 novelty、priority、correctness、nonexistence 或 publishability。

项目术语 fixed deletion、common-shear packet、simultaneous height、remote adjacent-inward 不能作为标准文献术语呈现。

## 10. 停止线与开放边界

- PROVED：frozen exact three-packet smooth NSE family；packets 2、3 的 relative survival；两个 distinct (T_*)-normalized endpoint divergences；fixed-set/different-time pigeonhole；(\mathfrak L^K_{1,R}/T_*\to\infty)；两个 audited strip integrals 相对 actual cubic payment 可忽略。
- NOT PROVED：actual ((P_R^M)^{2/3})-normalized fixed-deletion counterexample；whole-shell clock upper/lower；accumulated-dissipation enhancement。
- NO-GO：equal-target W-strip route 被 outer exterior velocity-cubic payment 阻断。
- OPEN：payment-compatible two-coordinate construction X.52；positive-variation upper；accumulated viscosity；arbitrary-clock extraction；scale contraction；一般 suitable weak solutions；regularity 与 singularity。
- PUBLICATION BOUNDARY：ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | LOCAL DIRECT TRANSLATION | NO DGX | NOT CLAY。

这不是 Navier--Stokes Millennium problem 的解决，也不声称构造了一般解的反例。**NOT CLAY.**
