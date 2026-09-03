# R0.74Z｜远端持续性门：kinetic coercivity、time-tame 条件与 full-clock 开放边界

## 1. 结论先行：持续 tube 会支付，endpoint-only 尚未关闭

R0.74Y 留下的目标是在 outer target spacetime box 上以指数精度消去 field，同时保留同一 packet 的 adjacent-inward remote tail 作为第二 clock coordinate。R0.74Z 对这个 cancellation-cell continuation 给出两级结论。

若 remote weighted kinetic floor (h) 在长度 (|J|=\theta_LR^3) 的 spacetime tube 上持续，则它自己强制 exterior cubic payment；严格低于临界 rate 的 persistence sequence 不能形成 W-kinetic payment escape。若只在 endpoint 保留 remote field，则 smoothness 只给某个 persistence interval，不能自动给 uniform (R^3) residence，critical 和更短时间集中仍开放。

\[
\boxed{\begin{gathered}
\textbf{PERSISTENT-TUBE KINETIC COERCIVITY: PROVED,}\\
\textbf{TIME-TAME ENDPOINT ROUTE: CONDITIONALLY BLOCKED,}\\
\textbf{FULL-CLOCK Y.57 CANCELLATION CELL: OPEN.}
\end{gathered}}
\]

没有 payment-compatible cell 被构造，也没有 whole-shell、regularity 或 singularity 结论。**NOT CLAY.**

## 2. exact common-shear algebra 与禁止的平移

令

\[
\mathcal L_bF=(\partial_t+b(t,x_3)\partial_2-\Delta_{23})F.
\]

同一 odd shear (b) 下任意有限个 smooth periodic solutions (C_j^+) 与 inversion partners

\[
C_j^-(t,x_2,x_3)=-C_j^+(t,-x_2,-x_3)
\]

的实系数线性组合仍解同一 passive equation。与 primary field 合并后，(u=(U_{\rm primary}+C,b,0)) 是 exact smooth periodic mean-zero unforced Navier--Stokes solution，pressure 可取零，negative coefficients 允许。

但 exact algebra 不允许把已演化 packet 任意垂直或时间平移：

\[
[\partial_2,\mathcal L_b]=0,
\qquad
[\partial_3,\mathcal L_b]=(\partial_3b)\partial_2,
\]

\[
\mathcal L_b[C_0(t-\tau)]
=[b(t,x_3)-b(t-\tau,x_3)]\partial_2C_0(t-\tau,x).
\]

因此 vertical centers、time offsets 或 Hermite cells 必须从 initial data 在实际 (b(t,x_3)) 下重新演化；不能静默删去 periodic windings。

## 3. 两次 fourth-root weight shift 与 tube coercivity

outer packet 的 adjacent-inward shell 是 (k=k_2-1)。写

\[
\omega=\gamma_{k_2-1}=\Gamma^{1/4}.
\]

同一物理 annulus 在 doubled radius 上满足

\[
A_{k_2-1}(R)=A_{k_2-2}(2R),
\qquad
\gamma_{k_2-2}=\omega^{1/4}=\Gamma^{1/16}.
\]

这是第二次 fourth-root shift；不能再次使用 (\Gamma^{1/4}) 作为 doubled-radius payment weight。

若 (\Omega(t)\subset A_{k_2-1}(R))、(|\Omega(t)|\le C_\Omega L^\nu R^3)，且对 (t\in J)、(|J|=\theta_LR^3) 有

\[
\frac{\omega}{2R}\int_{\Omega(t)}|u(t,x)|^2\,dx\ge h,
\]

则 spatial Hölder 和 nonnegative exterior velocity row 给出 exact deterministic coercivity：

\[
P_R^M\ge cC_\Omega^{-1/2}\theta_Lh^{3/2}R\omega^{-5/4}L^{-\nu/2},
\]

\[
\boxed{(P_R^M)^{2/3}
\ge cC_\Omega^{-1/3}\theta_L^{2/3}hR^{2/3}
\omega^{-5/6}L^{-\nu/3}.}
\]

该下界使用 total field，而不是某个 summand，所以已包含 primaries、correctors、inversion partners 与全部 periodic copies 的 interference。

## 4. strict persistence threshold 与临界层

令

\[
\theta_L=e^{-\kappa L^2+o(L^2)}.
\]

R0.74Y 的 frozen rational parameters 给出

\[
\Delta_{\rm rem}
=\frac5{24}c_\gamma-\frac\rho6
=\frac{64279}{238140000}>0,
\qquad
\kappa_*=\frac32\Delta_{\rm rem}
=\frac{64279}{158760000}.
\]

于是

\[
\liminf_{L\to\infty}\frac1{L^2}
\log\frac{(P_R^M)^{2/3}}h
\ge \Delta_{\rm rem}-\frac23\kappa.
\]

因此每个满足

\[
\boxed{\limsup_{L\to\infty}
\frac{-\log\theta_L}{L^2}<\kappa_*}
\]

的 persistence sequence 都被严格排除为 W-kinetic payment escape。等号层 (-L^{-2}\log\theta_L=\kappa_*+o(1)) 仍是 **OPEN**：poly(L) 和 (o(L^2)) 因子可能决定符号。

## 5. time-tame endpoint-to-tube 只是一条条件路线

remote free comparator 的 field scale 为

\[
\mathcal A_{\rm rem}=|\mathfrak a_2|e^{-\beta L^2+O(L)},
\qquad
\beta=\frac{49}{268288},
\]

并有 exact reserve

\[
\frac\rho4-\beta=\frac{7103}{167680000}>0.
\]

定义 moving derivative

\[
\mathscr D_2=\partial_t+Q_2'(t)\partial_2.
\]

如果 total corrector 在固定 normalized remote neighborhood 上满足 time-tame envelope

\[
R^2|\mathscr D_2C|\le|\mathfrak a_2|e^{o(L^2)},
\]

endpoint preservation 又在略放大的 remote strip 上成立，并且 W comparison 在移动 strip、全部 windings 与 (O(R)) center/heat-age perturbation 下 uniform，则 endpoint field 可在 (R^3) 时间 tube 上持续。结合上一节的 exact coercivity，W-kinetic route 被阻断。

第一步依赖 displayed envelope、endpoint condition 和 moving-strip all-winding uniformity，是 **CONDITIONAL LEMMA**；第二步才是 exact payment theorem。不得把 (Z.22) 单独写成 unconditional persistence theorem。

## 6. Gaussian、multi-center 与 Hermite cells 的边界

加入 identical negative copy 会在 target 与 remote strip 上同时把 primary 完全消去，因而也毁掉所需第二 coordinate。一个 displaced restoring Gaussian 可以在两个选定 points 做插值，其 target suppression rate 为

\[
\zeta_{\rm 2c}=\frac{49}{134144},
\qquad
\zeta_{\rm 2c}-\frac1{5000}
=\frac{13857}{83840000}>0.
\]

但其 remote ratio 的 logarithmic slope 是 (-\Theta(L))，跨固定宽度 strip 会变化 (e^{\Theta(L)})，不能给 uniform (1+o(1)) restoration。即使只恢复一点，普通 (R)-width packet 的 remote field 也会在 (R^3) interval 上持续并触发 tube coercivity。

更多 centers 或高阶 finite differences 可以 flatten 更多 derivatives，却不能在 family size、coefficient condition number 和 separations 任意依赖 (R) 时推出 uniform no-go。fixed 或 coefficient-tame subexponential families 若满足 time-tame envelope，则落入条件阻断；arbitrary exponentially ill-conditioned finite network 仍开放。qualitative analyticity 也不能在没有 frequency/global-norm bound 时传播 (e^{-\zeta L^2}) smallness。

## 7. endpoint-focused escape 的必要复杂度

令 (\mathcal N_L) 表示 (Z.22) 中 normalized time derivative 与 conditioning factor。endpoint preservation 所保证的 residence rate 形式上满足

\[
\theta_L\gtrsim
\min\left\{1,
\frac{\exp[(\rho/4-\beta)L^2+o(L^2)]}{\mathcal N_L}
\right\}.
\]

在该 derivative/conditioning model 内，想避开 strict subcritical persistence no-go，必须至少有

\[
\boxed{
\log\mathcal N_L\ge
\left(\frac{476239}{1064835072}+o(1)\right)L^2.}
\]

这是 **necessary leading rate**，不是 sufficient construction；等号仍开放。fixed (M)、polynomial (M) 与 polynomial Hermite order 只有在 total conditioning 和 derivative envelope 也 subexponential 时才被排除。极窄 packet 的 backward heat amplification 对 isolated modes 给出强烈代价，但推广到 arbitrary cancelling finite sums 仍需要 spectral/observability estimate。

## 8. W-kinetic 结论不能提升为 full-clock Y.57

tube coercivity 比较的是 payment 与 chosen region 上的 kinetic floor (h)。endpoint clock 只知 (K_{k_2-1,R}(t_2)\ge h)，而没有证明 (K\le e^{o(L^2)}h)。accumulated ordinary-viscosity row 可能比 (h) 大；若要关闭它，必须证明该 row 自身也强制 comparable central-energy 或 exterior payment。

因此已证的是：strict subcritical residence 下，time-tame corrector 不能把 persistent W-type remote kinetic strip witness 单独变成 clock-over-payment counterexample。未证的是：任何 time-tame cell 都不可能满足完整 Y.57 ratio。

下一 proposition (Z.39) 是 cancellation-robust remote endpoint persistence/payment dichotomy：要么 field 在 rate 严格低于 (\kappa_*) 的 tube 上持续并由本节关闭，要么 critical/shorter concentration 必须在 complete Version-M ledger 中支付。第二分支、critical layer、full completed clock 与 arbitrary ill-conditioned finite family 均保持开放。

## 9. certificate、literature 与冻结四联图

- independent primary analytic audit：PASS，0 blockers；
- Python certificate：10/10 checks；
- independent Ruby audit：11/11 assertions；
- negative mutations：Python 22/22、Ruby 23/23 rejected；
- (PYTHONHASHSEED=0,1,42)：byte-identical；
- figure archive：25 files、3,032,354 bytes，18/18 deterministic rerender，SVG/PNG/PDF 与 greyscale QA PASS；
- certificate scope：finite exact arithmetic、source structure、hashes 与 claim boundaries，不是 continuous PDE proof；
- literature：截至 2026-09-03 的 bounded primary-source screen 仅为 finite non-hit，不证明 novelty、priority、nonexistence、correctness 或 publishability。

四联图编码 exact weight ladder、strict persistence threshold、conditional time-tame route 与 full-clock claim hierarchy。它是 analytic schematic 和 derived analytic values，不是 PDE simulation、DNS、sampled trajectory 或 empirical fit。

## 10. 发布停止线

- **PROVED**：finite same-(b) inversion-paired superposition 的 exact NSE closure；two fourth-root weight shifts；persistent remote tube 的 Hölder coercivity；strict (\limsup(-L^{-2}\log\theta_L)<\kappa_*) W-kinetic no-go。
- **CONDITIONAL**：endpoint preservation 加 (Z.22) 与 moving-strip all-winding uniformity 推出 (R^3) persistence；在该 model 内的 complexity lower rate。
- **OPEN / NOT CERTIFIED**：critical layer、endpoint-only branch、arbitrary exponentially ill-conditioned finite family、accumulated clock rows、full-clock Y.57、complete payment upper、whole-shell estimates、fixed deletion、general suitable weak solutions、regularity 与 singularity。
- **PUBLICATION BOUNDARY**：没有构造 payment-compatible cancellation cell；finite literature non-hit 不是 novelty evidence。ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NO NOVELTY CLAIM | LOCAL DIRECT TRANSLATION | NO DGX | NOT CLAY。

本节不解决 Navier--Stokes Millennium problem，也不提出一般解反例。**NOT CLAY.**
