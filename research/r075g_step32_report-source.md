# R0.75G Step 32 reader source

## 1. 结论先行：独立增益的精确充分阈值

R0.75F 已证明 direct modal phase substitution 只会重建同一个 localized energy ledger；R0.75G 因而把剩余问题改写成一个可证伪的定量门槛。若独立的动力学论证能够证明

\[
\mathfrak X_{\xi,R}(F,b)
\le C R^\alpha p_b^{1/3}p_F^{2/3},
\tag{G.1}
\]

则精确充分阈值为

\[
\boxed{
\alpha>\alpha_*:=1-\frac{c_\gamma}{3\rho}
=\frac{27163}{107163}
\approx0.2534736803.}
\tag{G.2}
\]

这只是一条针对 (G.1) 的 conditional sufficient threshold：本节没有证明任何正的 \(R^\alpha\) gain，也没有证明这是所有可能路线的必要条件，更没有在阈值处或阈值以下构造 counterexample。

## 2. 冻结输入、local atoms 与 background 大小

保持冻结尺度与常数

\[
R=\exp\!\left(-\frac\rho4L^2\right),\qquad
\omega=\exp\!\left(-\frac{c_\gamma}{4}L^2\right),
\qquad
\rho=\frac9{10000},\quad c_\gamma=\frac8{3969}.
\tag{G.5}
\]

在 outer collar cylinder 上定义

\[
\begin{aligned}
p_b&:=R^{-2}\omega
 \int_{I_{2R}}\!\int_{\operatorname {supp}\xi}|b|^3,\\
p_F&:=R^{-2}\omega
 \int_{I_{2R}}\!\int_{\operatorname {supp}\xi}|F|^3.
\end{aligned}
\tag{G.6}
\]

非负的 scale-\(2R\) exterior velocity row 给出

\[
p_b+p_F\le C P_R^M,
\tag{G.7}
\]

而 R0.75D 的 absolute Hölder estimate 是零增益情形

\[
\mathfrak X_{\xi,R}\le C p_b^{1/3}p_F^{2/3}.
\tag{G.8}
\]

时间窗长为 \(O(R^2)\)，collar 体积为 \(O(L^2R^3)\)，且 \(|b|\le C R^{-2}\)，所以

\[
\begin{aligned}
p_b
&\le C R^{-2}\omega(R^2)(L^2R^3)(R^{-6})\\
&\le C L^2\omega R^{-3}.
\end{aligned}
\tag{G.9}
\]

因此

\[
p_b^{1/3}\le C L^{2/3}\omega^{1/3}R^{-1}.
\tag{G.10}
\]

R0.75C 的 matching lower bound 不是这条充分蕴含所需的输入；这里只使用 (G.9) 的上界。

## 3. 阈值推导与 strictness

假设 (G.1)，由 (G.7) 与 (G.10) 得

\[
\begin{aligned}
\mathfrak X_{\xi,R}
&\le C R^\alpha p_b^{1/3}p_F^{2/3}\\
&\le C L^{2/3}\omega^{1/3}R^{\alpha-1}
(P_R^M)^{2/3}.
\end{aligned}
\tag{G.11}
\]

其系数的指数率为

\[
\lim_{L\to\infty}\frac1{L^2}
\log\!\left(L^{2/3}\omega^{1/3}R^{\alpha-1}\right)
=\frac{(1-\alpha)\rho}{4}-\frac{c_\gamma}{12}.
\tag{G.12}
\]

严格负当且仅当

\[
3(1-\alpha)\rho<c_\gamma,
\qquad
\alpha>1-\frac{c_\gamma}{3\rho}.
\tag{G.13}
\]

精确有理数计算为

\[
1-\frac{(8/3969)}{3(9/10000)}
=1-\frac{80000}{107163}
=\frac{27163}{107163}.
\tag{G.14}
\]

在等号处指数率为零，但 \(L^{2/3}\) 仍增长；因此对这个未精炼估计，(G.2) 必须保持 strict。与 R0.75E (E.22) 合并只得到条件蕴含

\[
\boxed{
\text{(G.1) for some }\alpha>\alpha_*
\quad\Longrightarrow\quad
D_{k,R}^{{\rm out},F}\le C(P_R^M)^{2/3}.}
\tag{G.15}
\]

## 4. 一组三分之一足够；四分之一不够这条路线

代入 \(\alpha=1/3\) 的严格指数 margin 是

\[
\frac{\rho}{6}-\frac{c_\gamma}{12}
=-\frac{4279}{238140000}<0.
\tag{G.3}
\]

所以 \(R^{1/3}\) gain 在条件上足够。代入 \(\alpha=1/4\) 则为

\[
\frac{3\rho}{16}-\frac{c_\gamma}{12}
=\frac{1489}{1905120000}>0.
\tag{G.4}
\]

所以 \(R^{1/4}\) 对这条 reduction 不充分；这不是反例，也不排除其他可能的证明机制。

## 5. amplitude scaling 不会创造增益

固定 shear，对任意 \(A>0\) 以 \(AF\) 替换 \(F\)，则

\[
\mathfrak X_{\xi,R}(AF,b)=A^2\mathfrak X_{\xi,R}(F,b),
\qquad
p_{AF}^{2/3}=A^2p_F^{2/3}.
\tag{G.16}
\]

因此当分母非零时，dimensionless correlation ratio

\[
\mathscr C_R(F,b)
:=\frac{\mathfrak X_{\xi,R}(F,b)}
{p_b^{1/3}p_F^{2/3}}
\tag{G.17}
\]

在 passive-field amplitude scaling 下不变；signed numerator 为零时约定 \(\mathscr C_R=0\)。缺失的小因子必须来自 sign、phase、dynamics 或 geometry，不能来自 passive amplitude 的重新归一化。R0.75E 的 horizontal zero sector 恰有 \(\mathscr C_R=0\)。

## 6. residence-time 解释与精确 exponent

若未来论证能用 nonnegative interaction atom 替代完整 background atom，并证明

\[
\mathfrak X_{\xi,R}
\le C(p_b^{\rm int})^{1/3}p_F^{2/3},
\qquad
p_b^{\rm int}\le C R^\beta p_b,
\tag{G.18}
\]

则 \(\alpha=\beta/3\)，阈值等价于

\[
\boxed{
\beta>\beta_*:=3\alpha_*
=\frac{27163}{35721}
\approx0.7604210408.}
\tag{G.19}
\]

calibrated plateau speed 与 \(R^{-2}\) 同阶。对一个 unwrapped monotone real lift，一次穿过宽度 \(O(R)\) 的区间时有纯运动学 occupation bound

\[
|\{t:q(t)\in J_R\}|
\le\frac{|J_R|}{\inf|q'|}
\le C R^3.
\tag{G.20}
\]

相对于完整 \(O(R^2)\) window，这只是 \(O(R)\) fraction，形式上对应 \(\beta=1\)、\(\alpha=1/3\)。它解释 (G.3) 的 favorable margin，却不证明 arbitrary diffusing and interfering passive field 满足 (G.18)。

## 7. pure-transport benchmark 与 diffusion obstruction

令 \(H\) 解一维 pure transport equation

\[
\partial_tH+b(t)\partial_2H=0.
\tag{G.21}
\]

对 spatially constant drift 与固定 smooth cutoff \(\xi\)，直接积分给出

\[
\frac12\frac d{dt}\int\xi|H|^2
=\frac12\int b(t)\partial_2\xi|H|^2,
\tag{G.22}
\]

从而

\[
\frac12\int_s^t\!\int b\partial_2\xi|H|^2
=\frac12\int\xi|H(t)|^2
-\frac12\int\xi|H(s)|^2.
\tag{G.23}
\]

冻结 exact fixture 给出的 positive flux 及 endpoint half-energy difference 都是 \(1/32\)。full-window absolute Hölder 丢失了这项 exact crossing cancellation；但恢复 diffusion 后，localized identity 同时包含正在估计的 dissipation，把 flux 从该 identity 解出来只会重复 R0.75F 的 circularity。因此 (G.23) 是机制 benchmark，不是 passive advection-diffusion 的证明。

## 8. 最小下一命题与五道 falsification gates

数值上有余量的目标现在可以精确写成

\[
\boxed{
\mathfrak X_{\xi,R}(F,b)
\le C R^{1/3}p_b^{1/3}p_F^{2/3}.}
\tag{G.24}
\]

- Dynamic gate：gain 必须对 total passive solution 成立，而不是只对预选 packet 或 static trigonometric family 成立。
- Diffusion gate：Brownian 或 heat recrossing 与 vertical diffusion 必须纳入，不能把 unknown dissipation 移到另一边。
- Geometry gate：spherical collar、\(x_1\) averaging、全部 periodic copies，以及 radial normal 几乎横切 drift 的区域都必须保留。
- Transition gate：\(b\) 很小或变号的 bands 必须由更小 geometry 或独立 shear estimate 支付。
- Payment gate：(G.18) 的 interaction atom 必须由 Version-M 已有 rows 支付，不能假设 E.24 或目标 dissipation bound。

允许的下一结果只有三类：证明 (G.24)，证明某个 \(\alpha>\alpha_*\) 的较弱 (G.1)，或构造 exact frozen-family sequence 使 \(R^{-\alpha_*}\mathscr C_R\) 无界。本节三者都没有建立。

## 9. 冻结证据、文献边界与停止线

Primary analytic audit 为 PASS、零 mathematical blockers、零 release blockers。Python certificate 为 16/16，独立 Ruby 为 18/18；双方拒绝全部 57/57 定向 mutations，unknown mutations fail closed，3 个 Python hash seeds 字节稳定，G.1--G.24 与 24/24 displays 完整解析。完整 frozen dependency ledger 为 12/12，并显式包含两套验证器直接读取的 fixtures 与 expected JSON。

bounded primary-source screen 只确认：邻近 shear-flow 工作会使用 resolvent 或 semigroup coercivity、pathwise trajectory information 与 local shear，physical localization 仍保留 drift flux。没有一个 inspected source 给出 (G.1)、(G.24) 或 Version-M spherical-collar theorem；有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。

本节已证明 (G.2)--(G.4)、(G.9)--(G.19) 的阈值和缩放推导，以及 (G.22)--(G.23) 的 pure-transport benchmark。每个 arbitrary-real positive gain、interaction atom (G.18)、G.24、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍 OPEN。

\[
\boxed{\textbf{EXACT SUFFICIENT THRESHOLD ONLY; POSITIVE GAIN OPEN; NOT CLAY.}}
\]

R0.75G 只量化一条 conditional route，不完成任意实场 closure。后续工作未授权、未读取、未公开。本节无正式图、simulation、numerical fit、DNS 或 DGX。
