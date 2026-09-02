# R0.74S Step 16 中文读者稿

## 106. Step 16：光滑精确解否定所有 \(p>1\) 的二次时间尾估计

Step 15 说明，只要一个 common-deletion temporal flux tail 成立，同一个删除集就能支付 combined terminal residual 的两条分支。Step 16 检查 Step 13 候选 S.342 额外要求的 \(p>1\) 时间可积性。检验对象不是数值近似，也不是奇异解，而是 Taylor 1923 bi-periodic decaying vortex 的平移与振幅族。

结论是严格的：对每个 \(p>1\)、每个有限删除预算 \(N\) 和每个拟议常数 \(C\)，都能选择 admissible \(R,z_0\) 与足够大的振幅 \(A\)，使 S.342 失败。因此 S.342 必须标记为 **FALSE**，不能继续列为 open candidate。

这个否定结果只针对 supercritical temporal-tail statement S.342。它不否定 direct hybrid terminal-flux gate，不否定临界 \(p=1\) 候选 S.444，也不证明或否定 S.407、S.375、Q.12、Q.1、scale contraction、regularity、singularity formation 或 Navier--Stokes Millennium problem。这里没有 singular solution。**NOT CLAY.**

## 107. Taylor 1923 二周期衰减涡是三维周期类中的光滑精确解

在 \(\mathbb T^3=(-\pi,\pi]^3\) 上定义

\[
 \boxed{
 W(x)=\bigl(\sin x_1\cos x_2,-\cos x_1\sin x_2,0\bigr),
 \qquad
 p_W(x)={\cos 2x_1+\cos 2x_2\over4}.}
 \tag{S.417}
\]

直接微分得到

\[
 \boxed{
 \nabla\!\cdot W=0,
 \qquad \Delta W=-2W,
 \qquad (W\!\cdot\!\nabla)W=-\nabla p_W.}
 \tag{S.418}
\]

固定 \(t_0>0\)，令

\[
 b_A(t):=Ae^{-2(t-t_0)},
 \qquad
 u_A(t,x):=b_A(t)W(x),
 \qquad
 p_A(t,x):=b_A(t)^2p_W(x).
 \tag{S.419}
\]

于是

\[
 \partial_tu_A-\Delta u_A+(u_A\!\cdot\!\nabla)u_A+\nabla p_A=0.
 \tag{S.420}
\]

对每个 \(A>0\)，这都是光滑、精确、周期、mean-zero、无外力的三维不可压 NSE 解。它独立于 \(x_3\)，所以是嵌入三维解类的二维光滑 screen。这里能自由改变振幅，是因为这个特定 \(W\) 同时是 steady Euler field 与 Laplace eigenfield；这不是一般 NSE 解的振幅对称性。

## 108. 固定坐标 Bernoulli 通量精确抵消，Version-M 只留下移动漂移

冻结的 even radial mollifier 对 \(W\) 的所有 \(\sqrt2\)-频率模式给出同一个实乘子

\[
 \varphi_R^{\rm per}*W=\mu_R W,
 \qquad
 \mu_R:=\int_{\mathbb R^3}\varphi(z)
            \cos\!\bigl(R(1,1,0)\!\cdot z\bigr)\,dz.
 \tag{S.421}
\]

当 \(R\downarrow0\) 时 \(\mu_R\to1\)。取 \(R\) 足够小，可令 \(1/2\le\mu_R\le1\)。以 \(x_*=(\pi/4,0,0)\) 为终点，Version-M 轨迹和移动场满足

\[
 \boxed{
 \dot\xi=\mu_Rb_AW(\xi),
 \quad
 v_R(t,y)=b_A(t)W(y+\xi(t)),
 \quad
 \pi_R(t,y)=b_A(t)^2p_W(y+\xi(t)).}
 \tag{S.422}
\]

唯一性给出 \(\xi_2=\xi_3=0\)，并且

\[
 \dot\xi_1=\mu_Rb_A\sin\xi_1,
 \qquad
 \boxed{
 \tan{\xi_1(t)\over2}
 =\tan{\pi\over8}
 \exp\!\left(-\mu_R\int_t^{t_0}b_A(s)\,ds\right).}
 \tag{S.423}
\]

对 shell cutoff \(\Psi_k^R\)，记

\[
 m_{k,R}:=\int_{\mathbb R^3}\psi_k^R(y)\,dy,
 \qquad
 J_{k,R}(\xi):=\int_{\mathbb T^3}\Psi_k^R(y)
          |W(y+\xi)|^2\,dy.
 \tag{S.424}
\]

Bernoulli 函数 \(B_W=|W|^2/2+p_W\) 满足 \(\nabla\cdot(B_WW)=0\)。因此固定坐标中的 kinetic 与 physical-pressure shell flux 经过周期分部积分后精确抵消；time-dependent pressure gauge 也因不可压而积分为零。Version-M 的完整公式只剩 moving-cutoff drift：

\[
 \boxed{
 \dot F_{k,R}(t)
 ={\gamma_k\mu_R\eta_R(t)b_A(t)^3\over2R}
       W(\xi(t))\!\cdot\!\nabla_\xi J_{k,R}(\xi(t)).}
 \tag{S.425}
\]

这是本步的关键区分。固定坐标 Bernoulli 通量为零，不代表冻结的移动观测量没有通量；沿非恒定局部速度移动的 cutoff 产生可计算漂移，而且这项不能从 Version-M flux 中删除。

## 109. 一个径向 Fourier 乘子同时激活任意 \(N+1\) 个物理 annuli

Taylor 平面场满足

\[
 |W(x)|^2={1-\cos2x_1\cos2x_2\over2}.
 \tag{S.426}
\]

令 \(q_+=(2,2,0)\)，并定义

\[
 c_{k,R}:=\int_{\mathbb R^3}\psi_k^R(y)
                  \cos(q_+\!\cdot y)\,dy.
 \tag{S.427}
\]

径向对称和积化和差公式给出

\[
 \boxed{
 J_{k,R}(\xi)={m_{k,R}\over2}
       +c_{k,R}\left(|W(\xi)|^2-{1\over2}\right),
 \qquad
 \nabla J_{k,R}=c_{k,R}\nabla|W|^2.}
 \tag{S.428}
\]

先固定任意有限删除预算 \(N\ge0\)，令 \(M=N+1\)。再选择 \(R\) 使

\[
 \boxed{
 0<R<\min\left\{{\pi\over16},
 {\pi\over6\sqrt2(2^{M+1}+1/8)}\right\},
 \qquad \mu_R\ge{1\over2},
 \qquad \overline I_{8R}\Subset(0,T).}
 \tag{S.429}
\]

这样，对前 \(M\) 个物理 shell cutoff 的整个支撑都有 \(|q_+\cdot y|\le\pi/3\)，从而

\[
 \boxed{
 c_{k,R}\ge{1\over2}m_{k,R}>0,
 \qquad 1\le k\le M.}
 \tag{S.430}
\]

这些是移动空间坐标中的 \(N+1\) 个不同物理 annuli，不是 Fourier-shell index。沿 \(\xi_2=0\) 有

\[
 W(\xi)\!\cdot\!\nabla|W(\xi)|^2
 =\sin\xi_1\sin2\xi_1.
 \tag{S.431}
\]

选一个固定小 \(\delta>0\)。当 \(A\) 足够大时，终端物理时间块 \([t_0-\delta/A,t_0)\) 位于 \(I_R\)，且 \(\pi/8\le\xi_1(t)\le\pi/4\)。于是前 \(N+1\) 个 shell 同时满足

\[
 \boxed{
 |\dot F_{k,R}(t)|=\dot F_{k,R}(t)
 \ge {\gamma_k\mu_Rc_{k,R}g_0\over2R}A^3,
 \quad
 1\le k\le M,
 \quad t_0-\delta/A\le t<t_0,}
 \tag{S.432}
\]

其中 \(g_0=\sin(\pi/8)\sin(\pi/4)>0\)。

## 110. \(p>1\) 的 common-deletion temporal tail 逐量词失败

沿用 Step 13 的无量纲 density

\[
 h_{k,R}(\sigma)=R^2
 |\dot F_{k,R}(s_R+R^2\sigma)|,
 \qquad 0<\sigma<4.
\]

S.432 的无量纲时间长度是 \(\delta/(AR^2)\)。因此，对 \(1<p<\infty\)，

\[
 \boxed{
 \|h_{k,R}\|_{L^p(0,4)}
 \ge {\gamma_k\mu_Rc_{k,R}g_0\over2}
       \delta^{1/p}R^{\,1-2/p}A^{\,3-1/p},
 \qquad 1\le k\le M.}
 \tag{S.433}
\]

对 \(p=\infty\)，

\[
 \boxed{
 \|h_{k,R}\|_{L^\infty(0,4)}
 \ge {\gamma_k\mu_Rc_{k,R}g_0R\over2}A^3.}
 \tag{S.434}
\]

删除至多 \(N=M-1\) 个 index，前 \(M\) 个正坐标中至少留下一个。所以

\[
 \boxed{
 \mathfrak H^F_{p,N,R}
 \ge c_{p,N,R}A^{\,3-1/p},
 \qquad p\in(1,\infty],}
 \tag{S.435}
\]

其中 \(c_{p,N,R}>0\) 与 \(A\) 无关。另一方面，完整 payment 的每个非负 row 都必须纳入比较。固定 \(R\) 后，平移不改变 pointwise amplitude；local energy、exterior velocity/pressure、fixed gauge 与 algebraic harmonic row 分别至多是 \(O_R(A^2)\) 或 \(O_R(A^3)\)。因此

\[
 \boxed{P_R^M\le C_RA^3.}
 \tag{S.436}
\]

这里 exterior \(\mathcal G\) 的 all-copy sum 由 super-Gaussian shell weights 收敛；harmonic \(\mathcal H\) row 则使用冻结的 order-\(-4\) algebraic kernel。两种收敛机制不能混写。

结合 S.435--S.436，

\[
 {\mathfrak H^F_{p,N,R}\over(P_R^M)^{2/3}}
 \ge c'_{p,N,R}A^{\,1-1/p}\longrightarrow\infty
 \qquad(A\to\infty).
 \tag{S.437}
\]

因此 S.342 的精确量词否定是

\[
 \boxed{
 \begin{gathered}
 \text{对每个 }p\in(1,\infty],\ N\in\mathbb N_0,\ C>0,\\
 \text{都存在 admissible }R,z_0\text{ 和一个光滑、周期、无外力解，使得}\\
 \mathfrak H^F_{p,N,R}>C(P_R^M)^{2/3}.
 \end{gathered}}
 \tag{S.438}
\]

顺序不能交换：先由对手给定 \(p,N,C\)，再取 \(M=N+1\)，选择一个 admissible \(R\)，最后令 \(A\to\infty\)。\(R\) 可以依赖 \(N\)，因为 S.342 要求同一个有限 \(N\) 对所有 admissible scales 一致成立。

## 111. 更一般的付款幂与时间反集中指数也受到限制

同一族还给出更尖锐的指数边界。若某个固定 \(p\in[1,\infty]\) 存在

\[
 \mathfrak H^F_{p,N,R}\le C(P_R^M)^\beta,
\]

则必须有

\[
 \boxed{\beta\ge1-{1\over3p}.}
 \tag{S.438a}
\]

这里 \(1/\infty=0\)。所以 \(2/3\) 只在 \(p=1\) 与振幅标度相容；每个 \(p>1\) 都要求严格更大的 payment power，除非加入额外因子。

更一般地，在同一个无量纲终端块上，若

\[
 \int_I h_{k,R}\le C(P_R^M)^\beta |I|^\alpha,
\]

则 \(|I|\asymp_RA^{-1}\)、\(\int_Ih_{k,R}\asymp_RA^2\) 强制

\[
 \boxed{3\beta-\alpha\ge2.}
 \tag{S.438b}
\]

特别地，在 bare class 中，二次 payment power \(\beta=2/3\) 不允许任何正的 time anti-concentration exponent \(\alpha>0\)。

## 112. 临界 \(p=1\) 只达到振幅饱和，新的 S.444 仍然 OPEN

对所有 \(k\)，S.428 仍成立且 \(|c_{k,R}|\le m_{k,R}\)。沿特征线使用

\[
 d\xi_1=\mu_Rb_A\sin\xi_1\,dt
\]

作变量替换，\(\mu_R\) 精确抵消，同时少掉一个振幅因子。于是

\[
 \int_{s_R}^{t_0}|\dot F_{k,R}(t)|\,dt
 \le C_R\gamma_km_{k,R}A^2.
 \tag{S.439}
\]

由 \(m_{k,R}\le C2^{3k}R^3\) 与 \(\sum_k2^{3k}\gamma_k<\infty\)，

\[
 \mathfrak H^F_{1,N,R}\le C_RA^2.
 \tag{S.440}
\]

把 S.432 在长度 \(\delta/A\) 的终端块上积分，并再次使用 \(N+1\) 个 shell 的 pigeonhole，得到反向振幅下界

\[
 \mathfrak H^F_{1,N,R}\ge c_{N,R}A^2.
 \tag{S.441}
\]

取趋向 \(t_0\) 的 local-energy good times，buffered local energy 的 endpoint 项还给出

\[
 P_R^M\ge c_RA^3.
 \tag{S.442}
\]

所以在固定 \((N,R)\) 下，

\[
 \boxed{
 \mathfrak H^F_{1,N,R}\asymp_{N,R}A^2,
 \qquad
 P_R^M\asymp_RA^3,
 \qquad
 \mathfrak H^F_{1,N,R}\asymp_{N,R}(P_R^M)^{2/3}.}
 \tag{S.443}
\]

这只是振幅 exponent 的饱和。它既没有给出 universal \(N_1,C\)，也没有证明下面的新候选：

\[
 \boxed{
 \begin{gathered}
 \exists\,N_1\in\mathbb N_0,\ C>0\ \text{universal，使得}\\
 \forall\text{ admissible Version-M solutions, }R,z_0
 \text{ and terminal settings},\\
 \mathfrak H^F_{1,N_1,R}\le C(P_R^M)^{2/3}.
 \end{gathered}}
 \tag{S.444}
\]

S.444 仍是 **OPEN**。Step 15 的 S.386--S.387 包含 \(p=1\)；若将 S.444 作为 antecedent，S.389--S.391 的同一推理仍能支付完整 hybrid residual。Step 13 的 \(p>1\) 时间窗增益不得继续使用。

## 113. ABC 精确族提供独立代数 screen，但不是第二个所需定理

等参数 ABC field

\[
 U=(\sin x_3+\cos x_2,\ \sin x_1+\cos x_3,
       \ \sin x_2+\cos x_1)
\]

满足 \(\nabla\times U=U\) 与 \(\Delta U=-U\)。因此 \(u=Ae^{-(t-t_0)}U\)，连同 mean-zero pressure \(-A^2e^{-2(t-t_0)}(|U|^2-3)/2\)，也是一个光滑周期精确解。在 \(\xi_*=0\) 有

\[
 U(0)\!\cdot\!\nabla|U|^2(0)=6.
\]

速度模式的频率长度为 \(1\)，\(|U|^2\) 的非恒定模式长度为 \(\sqrt2\)。径向乘子、small-\(R\) shell positivity 与 \(O(A^{-1})\) trajectory residence 再次产生 \(A^{3-1/p}\) obstruction。

这只是对机制的独立 exact-family screen。Taylor 族的主证明不依赖它，也不需要把它提升为第二个 theorem。ABC 的历史语境见 Dombre et al., [*Chaotic streamlines in the ABC flows*](https://doi.org/10.1017/S0022112086002859) (1986)。

## 114. 原始来源只支持经典背景，不承担本项目的否定结论

S.417 的精确场采用 Taylor 1923 的 bi-periodic decaying vortex。现代数值文献有时把它称为 two-dimensional Taylor--Green vortex，但这里不把它与 Taylor--Green 1937 的 fully three-dimensional datum 混为一谈。

历史来源是 G. I. Taylor, [*On the decay of vortices in a viscous fluid*](https://doi.org/10.1080/14786442308634295) (1923)。Taylor--Green 1937 只作为历史语境，见 [*Mechanism of the production of small eddies from large ones*](https://doi.org/10.1098/rspa.1937.0036)。现代 exact-flow 背景包括 Chai--Wu--Fang 的 [*Single-scale two-dimensional-three-component generalized-Beltrami-flow solutions of incompressible Navier--Stokes equations*](https://doi.org/10.1016/j.physleta.2020.126857) (2020) 与 Antuono 的 [*Tri-periodic fully three-dimensional analytic solutions for the Navier--Stokes equations*](https://doi.org/10.1017/jfm.2020.126) (2020)。这些 classical fields、generalized-Beltrami mechanism 与 exponential decay 都不是 novelty claims。

附近的分析背景还包括 Caffarelli--Kohn--Nirenberg 的 suitable-weak partial regularity [DOI](https://doi.org/10.1002/cpa.3160350604)，Wolf 的 local pressure decomposition，Dascaliuc--Grujić 的 physical-scale flux locality，Koch--Tataru 的 critical Carleson-type norm，以及 Yang 的 skewed-cylinder maximal estimates [DOI](https://doi.org/10.4171/AIHPC/20)。它们不提供本项目特定的 terminal mollified trajectory、periodized physical annuli、time norm 之前的 fixed shell deletion 与 \(P_R^M\) payment 的组合定理。

冻结审计只做了 bounded collision search。没有找到相同量词的 theorem 或 counterexample，不等于 exhaustiveness，也不构成 novelty 或 priority claim。S.438 的证明依赖页面展示的直接 substitution 与 payment comparison，不依赖文献搜索没有命中。

## 115. 主张账本、有限证书与下一条允许路线

在冻结的 Version-M setting 中，本步 **PROVED**：S.417--S.420 的精确光滑 NSE identities；S.421--S.423 的径向 mollifier 与 terminal path；S.424--S.425 的 fixed-frame Bernoulli cancellation 与 moving-drift identity；S.426--S.432 对任意 \(N+1\) 个 physical shells 的 simultaneous positivity；S.433--S.437 的 temporal-tail lower bounds 与 complete-payment upper bound；S.438 对 S.342 的量词级否定；以及 S.439--S.443 在固定 \((N,R)\) 下的临界 \(L_t^1\) 振幅饱和。

本步新写出的 S.444 仍 **OPEN**。继续 **OPEN AND UNCHANGED**：direct hybrid terminal-flux gate、selected-crown estimate S.407、S.375、S.288、S.303、S.272、Step 10 S.243、Q.12、Q.1、scale contraction、regularity、singularity formation 与 Millennium problem。

路线校正是明确的：以后不能再把 S.342 当作 proof antecedent，因为它在光滑周期精确解上已经为 false。short-flux 路线下一步只能分析临界 \(L_t^1\) tail S.444，并保留 signed moving-drift cancellation 与 common deletion set。terminal-crown 路线仍可通过另外开放的 coercivity estimate S.407 继续。

主证书通过 7/7 finite groups、2,207 cases、7/7 structural groups 与 3/3 dependency locks。Independent Ruby verifier 通过 9/9 groups、2,839 independent cases，并锁定主文、两份审计、Python/Ruby 实现、主证书 JSON 与证书报告。另有 11 个外部负探针，全部按预期失败关闭。两套有限程序核对 exact Fourier identities、pigeonhole、representative support/path inequalities、amplitude exponents、hashes、structure 与 claim labels；它们不 machine-prove arbitrary-mollifier continuity、continuous payment estimate、S.444、S.407、regularity 或 Clay problem。**FINITE ONLY. NOT CLAY.**
