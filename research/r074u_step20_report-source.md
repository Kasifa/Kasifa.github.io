# R0.74U｜内禀运动认证驻留尺度，并关闭指数短驻留逃逸

## 146. 本节结论：先分清两个时间集合

Step 20 对冻结的 canonical common-shear packet architecture 证明一个明确的运动学事实：包中心以 `R^-2` 量级穿过水平空间，而物理 annulus 给它 `L_i R` 量级的中心余量，因此显式认证几何走廊 `R_i^cert` 的时间尺度是 `L_i R^3`。这是对几何走廊的双边结论。completed-clock 的 `K_{k_i,R}` 超水平集可能更大，本节对它仅证明包含关系与下测度界；没有 converse，也没有上测度界。

## 147. 冻结架构与完整终端时间片

对象仍是同一个 exact smooth periodic、mean-zero、unforced common-shear Navier–Stokes 解，压力为零；两个 inversion-paired derivative-heat packets 共用一个 shear coefficient。对 `i=1,2`，令 `L_2=2L_1`、`L_1>=9216`，并在终端片 `I_R=(64R^2,65R^2)` 上追踪包中心 `Q_i(t)`。平台校准给出严格单调速度区间

\[
\frac{1-\varepsilon_i}{128R^2}\le Q_i'(t)\le\frac{1}{128(1-\varepsilon_1)R^2},\qquad \varepsilon_i=4e^{-a_D L_i^2}<\frac14.
\]

这里没有把先前较短的 `R^3` 窗口悄然放大；完整时间片上的 packet survival、inversion suppression、cross-packet tail 与 periodic remainder 分别由冻结主文列出的全时间输入重新核对。

## 148. 物理 annulus 的精确中心余量

选定移动 lobe box `Omega_i(t)`，其体积恰为 `L_iR^3/16`。显式中心余量

\[
A(L)=\sqrt{\left(\frac2\lambda\right)^2-\frac1{256}-\left(c_h+\frac1L\right)^2}-\frac{b_2}{L}
\]

在 `L>=9216` 时满足 `3/8<A(L)<1`。因此，只要 `|Q_i(t)|<A(L_i)L_iR`，整个 lobe 都位于选定的物理空间 annulus `A_{k_i}(R)` 内，并且 cutoff `Psi_{k_i}^R` 在 lobe 上恒为一。这是 physical-space shell 陈述，不是 Fourier frequency shell，也不是对所有可能中心位置的最优刻画。

## 149. 认证几何走廊的双边尺度

定义完整的显式充分条件预像

\[
\mathscr R_i^{\rm cert}=\{t\in I_R:\ |Q_i(t)|<A(L_i)L_iR\}.
\]

中心余量除以速度给出 `A(L_i)L_iR^3` 量级；即使零点落在时间片端点，至少一侧仍保留足够时间。精确的 slab truncation 与单调预像估计得到

\[
\frac{72}{5}L_iR^3\le |\mathscr R_i^{\rm cert}|\le\min\!\left\{R^2,\frac{256A(L_i)}{1-\varepsilon_i}L_iR^3\right\}<\frac{1024}{3}L_iR^3.
\]

所以 `|R_i^cert|=Theta(L_iR^3)`。上式右端只约束这个认证几何走廊；它不是 maximal physical residence，更不是完整 `K`-超水平集的上界。

## 150. 从总场 lobe floor 到 completed-clock：只有下包含

在认证走廊内，direct packet、inversion partner、另一 packet 与 periodic copies 的比较都在总场中完成，得到 `|u(t,x)|>=c a_i` 的 lobe floor。时间 cutoff 与空间 cutoff 在 lobe 上等于一，而 completed clock 的其余项非负，故

\[
\mathscr R_i^{\rm cert}\subset\{t\in I_R:K_{k_i,R}(t)\ge c_KT\},\qquad
\big|\{K_{k_i,R}\ge c_KT\}\cap I_R\big|\ge\frac{72}{5}L_iR^3.
\]

这是本页最重要的量词边界：只证明 `corridor subset K-superlevel` 和 full `K`-superlevel 的 lower measure bound。accumulated dissipation、off-target endpoint rows、另一 packet 或 common shear 都可能让 `K` 在 lobe 离开后继续保持高值，因而不能反向包含，也不能把上一节的 `1024/3` 上界转移给 `K`。

## 151. 认证驻留进入 cubic payment

令外包的 normalized certified dwell 为 `theta_cert,2=|R_2^cert|/R^3`，则

\[
\theta_{{\rm cert},2}\ge\frac{72}{5}L_2.
\]

R0.74T 的 measurable-lobe Hölder coercivity 可用于整个认证走廊。把 lobe floor `h_2>=cT` 与上述驻留下界代入，得到

\[
\frac{(P_R^M)^{2/3}}{T}\ge cR^{2/3}\Gamma_2^{-5/6}L_2^{1/3}.
\]

这里使用的是空间 Hölder 与非负积分对可测时间集的限制，二者都是经典工具；本节的新工作边界在冻结 PDE 架构、物理 lobe、总场比较、completed-clock 与 payment 量词的组合，而不是 Hölder 本身。

## 152. 指数短驻留逃逸为何冲突

沿冻结尺度关系写 `S=log(1/R)`、`d_L=a_SL_1^2-S -> +infinity`。若反设 normalized payment 保持有界，R0.74T 的必要条件会强迫

\[
\theta_{{\rm cert},2}\le C L_2^{1/2}\exp\!\left[-(5c_\gamma-a_S)L_1^2-d_L\right],\qquad
5c_\gamma-a_S=\frac{603445}{89413632}>0.
\]

这不是对真实走廊的无条件上界，而是“付款若有界”推出的必要上界。它与已证明的 `theta_cert,2>=(72/5)L_2` 指数级不相容。因此，frozen canonical common-shear architecture 中的 exponentially short-dwell escape 被关闭；结论没有推广到任意 shear、任意 packet 或任意 clock。

## 153. 显式相位还可改善常数

对冻结显式相位 `tau_1=64R^2+2R^3`、`tau_2=65R^2`，一侧 slab room 可以直接加强：inner forward corridor 至少为 `(96/5)L_1R^3`，outer one-sided corridor 至少为 `(144/5)L_2R^3`。这些是认证几何走廊的改进 lower constants，不改变完整 `K`-超水平集仍然只有下界的结论。

## 154. 有限证书、图包与可复现边界

冻结 Python certificate 为 PASS：31/31 checks、869 个 exact finite cases；独立 Ruby audit 为 PASS：9/9 groups、1,651 个 Rational assertions。Python/Ruby mutation suites 分别拒绝 23/23 与 24/24 个故意错误，Python hash seeds 0、1、42 输出 byte-identical。期刊图包通过 47/47 validation checks，deterministic core 为 18/18，SVG、one-page PDF 与 600 dpi PNG 均绑定到冻结来源。

这些结果是 exact arithmetic、kinematic、structural、dependency 与 hash QA；图是 analytic schematic / derived analytic values，不是 PDE data，也不是 DNS。有限计算不替代 continuum PDE proof，图包 seal 也不认证数学正确性。

## 155. 文献近碰撞与停止线

有限一手来源筛查没有找到同时陈述六部分冻结组合的来源；这只是 bounded-search non-hit，不是 novelty、priority、correctness、nonexistence 或 publishability 证明。最接近的名称碰撞是 Inage（2026）的 coherent same-scale Fourier–helical triads “residence-time compression”：它对 low phase-drift set 给出 scale-decaying upper temporal estimate；这里则对 physical-space annulus 中的 canonical packet lobe 证明 lower residence，并只向 completed-clock 超水平集传递下界。对象、shell、假设与不等式方向都不同。

仍 OPEN：完整 `K`-超水平集上测度界；包含 off-target endpoint rows、viscous accumulation、cross terms 与 shear baseline 的 full completed-clock upper ledger；arbitrary-clock lobe extraction；high-Rayleigh / anomalous-defect；fixed deletion；direct hybrid；Q.12；Q.1；scale contraction；regularity 与 singularity formation。本节不是 suitable-weak 任意解定理，不是 Navier–Stokes counterexample，**NOT CLAY**。
