# R0.75C Step 28 reader source

## 1. 结论先行：total-cubic packing 是背景剪切假阳性

在冻结的 exact smooth periodic saturation-shear family 中，outer collar 的 total-velocity cubic block masses 在全部 (N\asymp R^{-1}) 个短块上可比，因此 (N_{\rm eff}^{\rm sh}\asymp R^{-1})。这严格否定了 B.44 threshold 必须普适成立的命题，但不否定 B.44 作为充分条件的正确性。

\[
\textbf{UNIVERSAL B.44: DISPROVED;}\quad
\textbf{B.45: NEITHER PROVED NOR DISPROVED;}\quad
\textbf{PASSIVE DISSIPATION: OPEN.}
\]

这不是 Navier--Stokes counterexample；只是对一个 auxiliary universal packing condition 的 exact-family counterexample。完整 (K)、fixed deletion、任意 suitable-weak extension 与 regularity 仍为 OPEN。NOT CLAY。

## 2. comparable blocks 与精确 threshold gap

对 shear-only field (u^{\rm sh}=(0,b,0))，固定正 cap 在整个 (I_{2R}=(61R^2,65R^2)) 上满足 (|b|\ge B/2)。每个扩大短块的 payment 都有

\[
p_m^{\rm sh}\asymp \omega L^2R^{-2},\qquad
cR^{-1}\le N\le CR^{-1}.
\]

所以

\[
N_{\rm eff}^{\rm sh}\asymp N\asymp R^{-1},\qquad
\lim_{L\to\infty}\frac{\log N_{\rm eff}^{\rm sh}}{L^2}=\frac\rho4=\frac9{40000}.
\]

相对 B.44 sufficient threshold 的精确超额为

\[
\frac9{40000}-\frac{4279}{79380000}=\frac{27163}{158760000}>0.
\]

## 3. 被计数的 background shear dissipation 仍已支付

球面 outer collar 的固定 (x_3)-slice 面积至多为 (CLR^2)。冻结 saturation datum 的一维 BV 范数一致有界；periodic heat kernel 与 Young 不等式给出

\[
\int_{61R^2}^{65R^2}\|\partial_3\theta_R(t)\|_2^2\,dt\le CR.
\]

结合 scale-(2R) exterior velocity payment lower，得到

\[
D_{k,R}^{{\rm out},b}
\le C\omega^{1/3}L^{-1/3}(P_R^M)^{2/3}
=o\!\left((P_R^M)^{2/3}\right).
\]

这一结论在加入任意 passive component (F) 后仍成立，因为 ((F^2+b^2)^{3/2}\ge |b|^3)。large (N_{\rm eff}) 只记录低频背景在时间块上的持久性，并未记录其梯度代价。

## 4. corrected gate：只剩 passive dissipation

对一般 exact common-shear field (u=(F,b,0))，outer dissipation 精确分解为

\[
D_{k,R}^{\rm out}=D_{k,R}^{{\rm out},F}+D_{k,R}^{{\rm out},b}.
\]

shear row 已支付，最小未解命题因此是

\[
D_{k,R}^{{\rm out},F}\stackrel{?}{\le}C(P_R^M)^{2/3}.
\]

替代 observable 必须看到 passive gradient 或其 frequency scale，不能只依赖 total (|u|^3) block masses。direct outer-dissipation estimate B.45 在本节仍是 NEITHER PROVED NOR DISPROVED。

## 5. 冻结证据与主张边界

Primary analytic audit 为 PASS、0 mathematical blocker、0 release blocker。Python certificate 为 8/8，独立 Ruby 为 9/9；18/18 与 19/19 定向 mutations 均被拒绝，三个 hash seeds 字节一致，36 个 equation tags 与 references 完整解析。它们只验证 finite exact arithmetic、source binding 与 structure，不替代连续 PDE proof。

本次冻结白名单没有新增 literature-collision artifact；handoff 只允许 bounded finite non-hit 表述。它不构成 novelty、priority、nonexistence、correctness 或 publishability 判断。正式图件：NOT APPLICABLE；本节纯解析，无 simulation、DNS 或 DGX。

## 6. 停止线与下一命题

R0.75C 在 corrected passive row 停止。下一步只能证明一个 frequency-sensitive passive block estimate，或构造 accounting 完整的 exact forward passive family；二者均未完成。

\[
\boxed{\textbf{TOTAL-CUBIC PACKING REJECTED; PASSIVE DISSIPATION OPEN; NOT CLAY.}}
\]

不得把 auxiliary B.44 false positive 写成 Navier--Stokes counterexample，不得把 B.45 写成已否定，也不得把 shear-row payment 写成 passive-row closure。R0.75D/E/F/G 与其他后续工作未读取、未公开。
