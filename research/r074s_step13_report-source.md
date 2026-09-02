# R0.74S Step 13 中文发布源

## 72. Step 13：时间可积性上限与组合 Morrey 阈值

Step 12 把 short last-exit residual 写成一个共同终端窗内的绝对 physical-flux variation，并在统一 moving-tube Morrey 与 path-length 假设下证明了 selected-excess estimate。Step 13 检查普通时间可积性能够把 short gate 推到哪里，以及允许 Morrey coefficient 随 payment 增长时，excess gate 的精确标量阈值是什么。

本步得到五项结论。第一，对每个固定的周期 suitable weak solution 和固定尺度，physical shell-flux density 具有可求和的 \(\ell^1(L_t^{4/3})\) 包络；这来自 energy-class interpolation \(u\in L_t^4L_x^3\)、周期 Calderon--Zygmund pressure estimate 与固定尺度的 mollified drift bound。第二，维数化长度为 \(\delta\) 的共同终端窗因此获得 \(\delta^{1/4}\) 增益；一般的 \(L_t^p\) shell-tail estimate 获得 \(\delta^{1-1/p}\)，但整个窗口只能删除同一个 shell set。第三，这个时间增益不能修复 payment exponent：即使额外假设相关的 \(\ell^1(L_t^p)\) tail 线性依赖 \(P_R^M\)，与 positive-depth term 平衡后仍只有 \(P^{2(2p-1)/(5p-3)}\)；energy-class 值为 \(P^{10/11}\)，\(p=\infty\) 也只有 \(P^{4/5}\)，都达不到 \(P^{2/3}\)。第四，smooth \((N+1)\)-coordinate witness 证明：任意阶 scalar temporal regularity 连同 payment-linear amplitude 仍不能单独推出 fixed-window best-\(N\) gate；这是抽象向量见证，不是 Navier--Stokes solution。第五，Step 12 的 separate uniform Morrey/path assumptions 可以弱化为 combined cover coefficient 至多按 \(1+(P_R^M)^{2/3}\) 增长；\(2/3\) 对只使用 two scalar caps 的论证是精确阈值，但不声称它对其他 PDE 证明是必要条件。

Universal terminal-window gate S.280、universal ancestor gate S.288 与 combined target S.303 继续 **OPEN**。本步不证明 Q.12、Q.1、scale contraction、regularity、singularity formation 或 Millennium problem；没有使用 DNS 或 DGX。**NOT CLAY.**

## 73. 无量纲 flux density 与共同删除次序

保留 R0.74S Step 12 的全部设定。令

\[
 \vartheta={\tau-s_R\over R^2}\in(0,4),\qquad
 t(\sigma)=s_R+R^2\sigma,
\]

并把每个 derivative 在 \(\mathcal T_R\) 外延拓为零。定义

\[
 \boxed{
 h_{k,R}(\sigma):=R^2|\dot F_{k,R}(t(\sigma))|,
 \qquad 0<\sigma<4.}
\tag{S.307}
\]

则 S.273 的共同窗口 coordinate 精确为

\[
 \boxed{
 f_{k,R}(\tau,\delta)
 =\int_{(\vartheta-\delta,\vartheta)\cap(0,4)}
       h_{k,R}(\sigma)\,d\sigma.}
\tag{S.308}
\]

对 \(1\le p\le\infty\) 与整数 \(N\ge0\)，定义 common-deletion temporal tail

\[
 \boxed{
 \mathfrak H^F_{p,N,R}
 :=\inf_{\#S\le N}\sum_{k\notin S}
       \|h_{k,R}\|_{L^p(0,4)}.}
\tag{S.309}
\]

S.309 的次序不可交换：shell set 在 time norm 之外选定，因此整个窗口使用同一个删除集合。逐时移动的 minimizing shell set 不能控制这里的 common-window functional。

## 74. 固定解的 \(L_t^{4/3}\) 事实

对 frozen class 中每个固定的周期 suitable weak solution 与固定 \(R>0\)，令

\[
 E_I:=\mathop{\rm ess\,sup}_{t\in\mathcal T_R}\|v_R(t)\|_2^2,
 \qquad
 D_I:=\int_{\mathcal T_R}\|\nabla v_R(t)\|_2^2\,dt,
 \qquad
 e_R:={E_I\over R},\quad d_R:={D_I\over R}.
\]

则 Proposition 2.1 证明

\[
 \boxed{
 \mathfrak H^F_{4/3,0,R}
 \le C\left([e_R(e_R+d_R)]^{3/4}+e_R^{3/2}\right)
 \le C(e_R+d_R)^{3/2}<\infty.}
\tag{S.310}
\]

从而对每个 terminal 与 \(0<\delta<4\)，

\[
\boxed{
 \mathcal V^F_{N,R}(\tau,\delta)
 \le C\delta^{1/4}[e_R(e_R+d_R)]^{3/4}
      +C\delta e_R^{3/2}.}
\tag{S.311}
\]

S.310 的有限 coefficient 可以依赖 solution 与 \(R\)；本步没有证明它由 \(P_R^M\) 一致控制。

采用 mean-zero periodic pressure gauge。Shellwise gauge cancellation 允许在 \(F_{k,R}\) 的 signed derivative 中使用这个 gauge。Energy class 与空间插值给出

\[
 \boxed{
 v_R\in L_t^4L_x^3,\qquad
 \pi_R-\overline\pi_R(t)\in L_t^2L_x^{3/2},\qquad
 a_R\in L_t^\infty.}
\tag{S.312}
\]

其中 \(L_t^\infty L_x^2\cap L_t^2H_x^1\subset L_t^4L_x^3\)，而周期 Calderon--Zygmund 估计为

\[
 \|\pi_R-\overline\pi_R(t)\|_{L^{3/2}}
 \le C\|v_R(t)\|_{L^3}^2.
\]

固定尺度 convolution 把 \(L_x^2\) 映到 \(L_x^\infty\)，故 \(|a_R(t)|\le C_R\|v_R(t)\|_2\)。继承的 cutoff bound 与 super-Gaussian shell weights 给出 \(\sum_{k\ge1}\gamma_k(1+2^{3k}R^3)<\infty\)。在 pressure gauge 已经改变之后再取 absolute value，可由 R0.74P 的 (2.9) 得到

\[
 \boxed{
 h_{k,R}(\sigma)
 \le C\gamma_k(1+2^{3k}R^3)
 \left[
  \|v_R(t)\|_3^3
  +\|\pi_R(t)-\overline\pi_R(t)\|_{3/2}\|v_R(t)\|_3
  +|a_R(t)|\|v_R(t)\|_2^2
 \right].}
\tag{S.313}
\]

完整尺度计算使用 \(\sum_k\gamma_k|\nabla\Psi_k^R|\le CR^{-1}\) 与周期插值不等式

\[
 \|v_R(t)\|_3^4
 \le C\|v_R(t)\|_2^2
 \left(\|\nabla v_R(t)\|_2^2
       +R^{-2}\|v_R(t)\|_2^2\right).
\]

由于 \(|\mathcal T_R|=4R^2\)，cubic/pressure 部分的 \(L_t^{4/3}\) norm 至多为 \(CR^{-1/2}[e_R(e_R+d_R)]^{3/4}\)，drift 部分的 \(L_t^\infty\) norm 至多为 \(CR^{-2}e_R^{3/2}\)。在 S.307 的变量替换下，前者获得 \(R^{1/2}\)，后者获得 \(R^2\)，从而得到 S.310；在 S.308 上对固定删除集使用 Holder，得到 S.311。

令 S.313 的 bracket 在 \(t=t(\sigma)\) 处为 \(\mathcal B_R(\sigma)\)，则实际使用的是

\[
 \sum_k\|h_{k,R}\|_{4/3}
 \le C\!\left[\sum_k\gamma_k(1+2^{3k}R^3)\right]
       \|\mathcal B_R\|_{4/3}.
\]

因此这是 \(\ell^1(L^{4/3})\) estimate，不是把 \(L^{4/3}(\ell^1)\) 非法互换过来。指数 \(4/3\) 是 direct energy-class interpolation 对空间 cubic integral 给出的 endpoint；不排除加入额外 PDE 假设后获得更高时间可积性。

Energy-admissible pairs 满足

\[
 {2\over q}+{3\over r}={3\over2},
 \qquad 2<r\le6,
 \qquad q(r)={4r\over3(r-2)},
\]

而 \(r=2\) 单独理解为 \(q(2)=\infty\)。对三个空间 Holder reciprocal 和为一的 admissible factors，有

\[
 \sum_{i=1}^3{1\over q_i}
 ={9\over4}-{3\over2}\sum_{i=1}^3{1\over r_i}
 ={3\over4},
\]

故时间指数仍是 \(4/3\)。Pressure 的对称选择先把 \(v_R\otimes v_R\) 放入强型 Calderon--Zygmund 范围 \(L_x^{3/2}\)；这里不使用 \(L^1\) weak endpoint 或 \(L^\infty\)-to-BMO endpoint。

## 75. 一般时间指数与精确优化

定义

\[
 a_p:=1-{1\over p}\quad(1\le p<\infty),
 \qquad a_\infty:=1.
\tag{S.314}
\]

对 \(\ell^1(L^p(0,4))\) 中的非负 shell densities，同一证明给出

\[
 \boxed{
 \mathcal V^F_{N,R}(\tau,\delta)
 \le\delta^{a_p}\mathfrak H^F_{p,N,R}.}
\tag{S.315}
\]

只为检验此方法，额外假设某个固定 \(p\in(1,\infty]\)、\(N\)、\(\beta>0\) 与 \(C_H\) 对 solution、scale 与 terminal 一致满足

\[
 \mathfrak H^F_{p,N,R}\le C_H(P_R^M)^\beta.
\tag{S.316}
\]

S.315 与 S.275 合并为

\[
 \boxed{
 \mathcal S_N(r^{\rm sh}(\tau))
 \le C_H\delta^{a_p}P^\beta
     +C_{\rm deep}\delta^{-2/3}P^{2/3},
 \qquad P:=P_R^M.}
\tag{S.317}
\]

当 \(P\ge1\)、\(\beta>2/3\) 且 optimizer 落在 \((0,4)\) 时，平衡尺度为

\[
 \boxed{
 \delta_{p,\beta}
 \asymp P^{-(\beta-2/3)/(a_p+2/3)}.}
\tag{S.318}
\]

两项共同得到的 payment power 是

\[
 \boxed{
 E_{p,\beta}
 ={2\over3}{a_p+\beta\over a_p+2/3},
 \qquad
 E_{p,\beta}-{2\over3}
 ={2\over3}{\beta-2/3\over a_p+2/3}>0.}
\tag{S.319}
\]

因此只要 temporal coefficient 比 \(P^{2/3}\) 增长更快，任何 \(p\)，包括 \(p=\infty\)，都不能消除 exponent loss。反过来，在这个 two-term argument 内，\(\beta\le2/3\) 对 large-payment regime 已经充分；small-payment regime 由 \(P\le P^{2/3}\) 与继承的 linear ledger 控制。

乐观的 linear case \(\beta=1\) 给出

\[
 \boxed{
 \delta_p\asymp P^{-p/(5p-3)},
 \qquad
 E_p={2(2p-1)\over5p-3}.}
\tag{S.320}
\]

特别地，

\[
 \boxed{
 p={4\over3}:\quad \delta\asymp P^{-4/11},
 \quad E_p={10\over11};
 \qquad
 p=\infty:\quad \delta\asymp P^{-1/5},
 \quad E_p={4\over5}.}
\tag{S.321}
\]

\(p=1\) 没有正 window power，linear term 仍为 \(P\)。S.320 在 \(p\to\infty\) 时单调趋于 \(4/5\)，仍高于目标 \(2/3\)。

对 Proposition 2.1 实际证明的 coefficient，直接优化得到 fixed-solution estimate

\[
 \boxed{
 \mathcal S_N(r^{\rm sh}(\tau))
 \le C\left[
 A_R+(\mathfrak H^F_{4/3,N,R})^{8/11}A_R^{3/11}
 \right].}
\tag{S.322}
\]

这里 \(A_R\) 覆盖 formal optimizer 超过 allowed window length 的情况。如果再有尚未证明的 \(\mathfrak H^F_{4/3,N,R}\lesssim P\)，mixed term 才是 \(P^{10/11}\)。这是对该 upper-bound method 的 ceiling，不是每个 NSE solution 都达到的 lower bound。

## 76. Smooth all-\(p\) 抽象饱和见证

固定 \(N\ge0\)，令 \(M=N+1\)。取 \(0<\delta_0<4\) 与非负 \(\phi\in C_c^\infty((-\delta_0,0))\)，满足 \(\int\phi=1\)，并选择 terminal \(\vartheta_0\) 使 translated support 位于 \((0,4)\)。对 \(H>0\)，定义

\[
 \boxed{
 h_{k,H}(\sigma)={H\over M}\phi(\sigma-\vartheta_0)
 \quad(1\le k\le M),
 \qquad h_{k,H}=0\quad(k>M).}
\tag{S.323}
\]

每个 primitive 都 smooth 且 increasing，并且对每个 \(1\le p\le\infty\)，

\[
 \boxed{
 \sum_k\|h_{k,H}\|_{L^p}=H\|\phi\|_{L^p},
 \qquad
 \mathcal V^F_{N}(\vartheta_0,\delta_0)={H\over M}.}
\tag{S.324}
\]

若 abstract payment 归一化为 \(P_H\asymp H\)，则

\[
 \boxed{
 {\mathcal V^F_N(\vartheta_0,\delta_0)\over P_H^{2/3}}
 \asymp {H^{1/3}\over N+1}\longrightarrow\infty.}
\tag{S.325}
\]

这个 witness 有 fixed smooth time profile，属于所有 temporal \(L^p\) spaces。它只证明 logical boundary：temporal regularity 加 scalar linear-amplitude bound 不包含 S.280。它不是 velocity field、pressure、suitable weak solution 或 NSE counterexample。

还有一个饱和 adaptive \(p=4/3\) balance 的 smooth abstract witness。取 \(P\ge1\)，选择 \(0\le\rho\in C_c^\infty((-1,0))\)、\(\|\rho\|_{4/3}=1\)，并令

\[
 c_\rho:=\int_{-1}^0\rho(s)\,ds>0,
 \qquad d:=P^{-4/11}\le1.
\]

选择 \(\vartheta_0\) 使 \(\vartheta_0+d\,\operatorname{supp}\rho\subset(0,4)\)，并定义

\[
 h_{k,P}(\sigma)
 ={P\over Md^{3/4}}
 \rho\!\left({\sigma-\vartheta_0\over d}\right),
 \qquad 1\le k\le M.
\]

于是

\[
 \sum_k\|h_{k,P}\|_{4/3}=P,
 \qquad
 \sum_k\|h_{k,P}\|_1=c_\rho P^{10/11}\le c_\rho P.
\]

删除 \(N=M-1\) 个 coordinates 后精确剩下 \(c_\rho P^{10/11}/M\)。为每个 coordinate 指定 abstract depth \(d_{k,P}=d\) 与 residual \(r_{k,P}=c_\rho P^{10/11}/M\)。当 \(\delta\ge d\) 时，共同终端窗收取全部 residual；当 \(0<\delta<d\) 时，coordinate 属于 deep class，且

\[
 \sum_kr_{k,P}=c_\rho P^{10/11}
 \le c_\rho P^{2/3}\delta^{-2/3}.
\]

在 balancing depth 上，

\[
 P^{2/3}d^{-2/3}=P^{10/11},
 \qquad
 {10\over11}-{2\over3}={8\over33}.
\]

因此在固定常数 \(c_\rho\) 意义下，\(10/11\) 对 linear \(\ell^1(L^{4/3})\) rate bound、inherited linear \(L^1\) ledger、depth allowance 与 fixed deletion budget 的抽象组合是 sharp。它仍只是 method-level countermodel，不是 NSE realization。

## 77. Moving-tube 路线的精确标量阈值

允许 Step 12 的 quantities 依赖 solution、scale 与 terminal：

\[
 \begin{aligned}
 M_R(\tau)&:=\sup_{Q_R^-\ {\rm in\ the\ buffer}}
       {\widetilde{\boldsymbol\mu}(Q_R^-)\over R},\\
 L_R(\tau)&:={1\over R}\int_{s_R}^{\tau}
       |\dot{\widetilde X}_R(t)|\,dt.
 \end{aligned}
\]

定义 combined cover coefficient

\[
 \boxed{
 B_R(\tau):=C_\psi M_R(\tau)
       \bigl(\mathscr A_3+L_R(\tau)\mathscr A_2\bigr).}
\tag{S.326}
\]

只要这些 quantities 有限，Step 12 的 S.291--S.293 对每个 \((u,R,\tau)\) 点态成立，并给出

\[
 \boxed{
 \sum_kx_k^{\rm sel}(\tau)
 \le\min\{C_0P_R^M,B_R(\tau)\}.}
\tag{S.327}
\]

因此 Step 12 分别假设 \(M_R\le M\)、\(L_R\le L\) 比 algebraic closure 所需更强。

Proposition 5.1 是 conditional payment-dependent Morrey envelope：若一个 universal \(C_B\) 对所有 solution 与 scale 满足

\[
 \boxed{
 \sup_{\tau\in\mathcal G_R\cap\mathcal T_R}B_R(\tau)
 \le C_B\bigl[1+(P_R^M)^{2/3}\bigr],}
\tag{S.328}
\]

则

\[
 \boxed{
 \sup_{\tau\in\mathcal G_R\cap\mathcal T_R}
 \mathcal S_0(x^{\rm sel}(\tau))
 \le C(C_0,C_B)(P_R^M)^{2/3}.}
\tag{S.329}
\]

证明只分两个 payment regimes：\(P_R^M\le1\) 时使用 S.327 的 linear side 与 \(P_R^M\le(P_R^M)^{2/3}\)；\(P_R^M\ge1\) 时使用 S.328 与 \(1\le(P_R^M)^{2/3}\)。特别地，

\[
 \boxed{
 B_R(\tau)\le C_B[1+(P_R^M)^\theta],
 \qquad 0\le\theta\le{2\over3},}
\tag{S.330}
\]

即可闭合 selected-excess gate。\(M_R\) 与 \(L_R\) 可以分别 nonuniform，只要加权 cover cost 的组合增长不超过 quadratic payment scale。

对只知道 S.327 两个 scalar caps 的论证，指数阈值是 sharp。若 \(\theta>2/3\)，固定 \(N\)，令 \(M=N+1\)，对 large \(P\) 取 \(M\) 个等坐标，总质量 \(T_P=\min\{C_0P,C_BP^\theta\}\)，并设 \(x_k^{\rm sel}=b_k=T_P/M\)。则

\[
 \boxed{
 \sum_kb_k=T_P,
 \qquad
 \mathcal S_N(b)={T_P\over N+1},
 \qquad
 {\mathcal S_N(b)\over P^{2/3}}\longrightarrow\infty.}
\tag{S.331}
\]

这是 two-cap inference 的 abstract sequence countermodel，不是 dissipation measure 或 NSE solution。使用更多 PDE structure 的证明仍可能在 \(\theta>2/3\) 时成功。

## 78. Dynamic high frequency 不能单独攻击 flux gate

在 \(2\pi\)-periodic torus 上取 \(A>0\)、\(T>0\) 与 integer \(n\ge1\)：

\[
 \boxed{
 u^{(n)}(t,x)=Ae^{-n^2t}\sin(nx_2)e_1,
 \qquad p^{(n)}=0.}
\tag{S.332}
\]

这是 unforced smooth Navier--Stokes solution：divergence free，\((u^{(n)}\!\cdot\nabla)u^{(n)}=0\)，并满足 heat equation。Mollified path velocity 平行于 \(e_1\)，而 moving velocity 与 \(y_1\) 无关，所以对每个周期 shell cutoff，

\[
 \boxed{
 \dot F_{k,R}^{(n)}(t)
 ={\gamma_k\eta_R(t)\over2R}
 \int_{\mathbb T^3}|v_R^{(n)}|^2
       (v_{R,1}^{(n)}-a_{R,1})\,\partial_{y_1}\Psi_k^R\,dy
 =0.}
\tag{S.333}
\]

最后一个等号来自 \(y_1\) 上的周期积分。因此这个 exact family 的每个 \(f_{k,R}\) 与 \(\mathcal V^F_{N,R}\) 都为零。同时在 \([0,T]\) 上，

\[
 \boxed{
 \begin{aligned}
 \int_0^T\!\int_{\mathbb T^3}|\nabla u^{(n)}|^2
 &=2\pi^3A^2(1-e^{-2n^2T}),\\
 \int_0^T\!\int_{\mathbb T^3}|u^{(n)}|^3
 &={32\pi^2A^3\over9n^2}(1-e^{-3n^2T}).
 \end{aligned}}
\tag{S.334}
\]

其 dissipation-to-cubic ratio 按 \(n^2/A\) 增长，但 canonical physical-flux primitive 为零，completed clock 满足 \(K=Q\)。因此 high Fourier frequency 与 high Rayleigh ratio 本身不会产生 short physical-shell flux tail；这里的 \(k\) 是 physical moving annulus index，不是 Fourier shell。这个 screen 不推广为任意动态高频场的零 flux theorem。

## 79. 有限主文献边界

我进行了有界检索，没有找到能以 Step 13 所需量词直接给出 uniform temporal tail 或 S.328 的 theorem。

- Lei--Ren, *Quantitative partial regularity of the Navier--Stokes equations and applications*, [Adv. Math. 445 (2024), 109654](https://doi.org/10.1016/j.aim.2024.109654)：定量化 dissipation-energy pigeonhole 并给出 logarithmically improved partial regularity；其 annular levels 与 constants 依赖 natural local energies，不是 common-terminal fixed-physical-shell best-\(N\) flux estimate。
- Choe--Yang, *Local kinetic energy and singularities of the incompressible Navier--Stokes equations*, [JDE 264 (2018), 1171--1191](https://doi.org/10.1016/j.jde.2017.09.036)：在 uniformly bounded scaled local kinetic energy 下得到 reverse Holder improvement；这正是 bare payment ledger 没有的额外信息。
- Guevara--Phuc, *Local energy bounds and epsilon-regularity criteria for the 3D Navier--Stokes system*, [Calc. Var. PDE 56 (2017), 68](https://doi.org/10.1007/s00526-017-1151-7)：从 scale-integrated inputs 得到 pressure-sensitive local-energy 与 epsilon-regularity criteria；不产生 S.316 或 S.328 的系数。
- Koch--Tataru, *Well-posedness for the Navier--Stokes equations*, [Adv. Math. 157 (2001), 22--35](https://doi.org/10.1006/aima.2000.1937)：在 critical small-data \(BMO^{-1}\) class 中使用 Carleson-type spacetime norm；不是从 \(P_R^M\) 为每个 bare suitable weak solution 推出 Carleson estimate。

这只是 collision check，不是 novelty 或 priority claim。相邻文献的 quantitative time/Morrey gains 都带有额外 scale information、smallness 或 energy-dependent constants，不能充当 S.280、S.288 或 S.328 的证明。

## 80. Critical 八叉树抽象反例

接着检查 bounded-branching ancestor tree 连同现有 linear 与 square ledgers 是否强迫额外 packing。答案是在 critical tree exponent 上不能。

固定整数 \(m\ge1\)，令 \(L=m^3\)，取深度 \(0\le d\le L-1\) 的 complete eight-ary tree。对深度 \(d\) 的每个 node \(v\)，定义

\[
 \boxed{
 b_v={1\over m^2 8^d},\qquad
 s_v={5\over3m^2 8^d},\qquad
 c_v=2^{-d},\qquad
 p_v={1\over m^3 8^d}.}
\tag{S.335}
\]

按 \(s_v\) 缩放 Step 11 S.267 的 pure high-Rayleigh scalar row：

\[
 \boxed{
 T_v=s_v,\quad d_v^{\rm def}=0,\quad
 \int_{H_v}g_v=b_v={3\over5}s_v,
 \quad\beta_v=0,\quad
 \sigma_v={983\over12000}s_v<{T_v\over12},\quad
 x_v={2617\over6000}s_v>{T_v\over6},\quad
 r_v^x={s_v\over3}.}
\tag{S.336}
\]

每个 node 都严格处于 abstract \(\mathcal I_x\) branch，ancestor 是 pure high-Rayleigh。逐层求和得到

\[
 \boxed{
 b_v=c_vp_v^{2/3},\qquad
 \sum_vp_v=1,\qquad
 \sum_vb_v=m,\qquad
 \sum_vs_v={5m\over3}=:P_m.}
\tag{S.337}
\]

这些 scalar rows 与 inherited linear clock/variation ledgers 及 zero \(Q\)-variation 相容，并满足

\[
 \boxed{
 \sum_vs_v^2
 <{200\over63m^4},\qquad
 \sum_{w\succeq v}b_w^2\le{8\over7}b_v^2,
 \qquad
 \sum_{w\in{\rm child}(v)}c_w^3=c_v^3
 \quad(0\le d(v)\le L-2).}
\tag{S.338}
\]

其中第二项是 strong square-Carleson bound；第三项只对 nonterminal nodes 断言，并处于 exact critical equality：八个 children 各取一半系数，coefficient cube 总和守恒。

每个 coordinate 至多为 \(m^{-2}\)。删除任意固定 \(N\) 个 coordinates 后仍有

\[
 \boxed{
 \mathcal S_N(b)\ge m-{N\over m^2},\qquad
 A_m=P_m^{2/3}=\left({5m\over3}\right)^{2/3},
 \qquad
 {\mathcal S_N(b)\over A_m}\longrightarrow\infty.}
\tag{S.339}
\]

所以 linear total ledger、vanishing global square ledger、bounded branching、square-Carleson subtree estimate 与 critical child decay 仍不推出 S.288。停止一个 ancestor 不能被算成删除一个 shell exception，同时免费删除其全部 descendants；best-\(N\) functional 删除的是 individual shell coordinates。

这棵树是 strict abstract ledger model。其 nodes 没有被同时实现为一个 solution 的 physical moving annuli；它不满足一个共同 velocity field 的 coupled Navier--Stokes dynamics、pressure、diffusion、cross-cubic payment、periodic incidence 或 \(K=Q+F\)。它不是 NSE counterexample。

## 81. Conditional incidence theorem 与 cubic Dini interface

存在一个精确的充分替代条件。若对每个 terminal 都有 shell set \(E_\tau\)、\(\#E_\tau\le N_b\)，以及非负 \(q_k\)、tree payments \(p_\nu\)、coefficients \(c_\nu\) 和 incidences \(\nu\rightsquigarrow k\)，使得在 \(E_\tau\) 外

\[
 b_k\le q_k+\sum_{\nu\rightsquigarrow k}c_\nu p_\nu^{2/3},
 \qquad
 \sum_kq_k\le C_qA_R,
\]

并且

\[
 \sum_{\rm incidences}p_\nu\le B_{\rm inc}C_pP_R^M,
 \qquad
 \sum_{\substack{\rm incidences\\k\notin E_\tau}}c_\nu^3\le C_c,
\]

则在 incidence set 上使用指数 \(3\) 与 \(3/2\) 的 Holder 不等式，得到

\[
 \boxed{
 \mathcal S_{N_b}(b)
 \le\left[C_q+C_c^{1/3}(B_{\rm inc}C_p)^{2/3}\right]A_R.}
\tag{S.340}
\]

三次方是精确 dual exponent，不是方便选择。对每个有限非负 coefficient vector，

\[
 \boxed{
 \sup_{p_\nu\ge0,\ \sum p_\nu\le1}
       \sum_\nu c_\nu p_\nu^{2/3}
 =\left(\sum_\nu c_\nu^3\right)^{1/3}.}
\tag{S.341}
\]

当 denominator 非零时，\(p_\nu=c_\nu^3/\sum_\omega c_\omega^3\) 取等号。若要把 tree inequality 变成 S.340 的 incidence coefficient bound，还需要三个 uniform inputs：

- root family 满足 \(\sum_{v\in{\rm roots}}c_v^3\le C_{\rm root}\)；
- 每个固定 node 被计入的 incidence multiplicity 至多为 \(M_{\rm inc}\)；
- 非负 child factors 满足 uniform Dini product sum

\[
 0\le\theta_d,\qquad
 \sum_{w\in{\rm child}(v)}c_w^3\le\theta_d c_v^3,
 \qquad
 \sup_{d_0\ge0}\sum_{n\ge0}
       \prod_{j=0}^{n-1}\theta_{d_0+j}
 \le C_D<\infty.
\]

三项合起来给出 \(\sum_{\rm incidences}c_\nu^3\le M_{\rm inc}C_{\rm root}C_D\)，从而提供 S.340 所需的 \(C_c\)。Uniform \(\theta_d\le\theta<1\) 是简单特例。S.335 的 critical tree 有 \(\theta_d=1\)，其 finite-depth Dini constant 按 \(L=m^3\) 增长，因而不能提供 uniform coefficient bound。

## 82. Step 13 路线决定与主张账本

Step 13 排除两条无效方向。第一，提高整体 flux density 的 scalar time regularity 不够；short branch 的下一充分输入必须是 shell selective：

\[
 \boxed{
 \exists p\in(1,\infty],N_F,C:\quad
 \mathfrak H^F_{p,N_F,R}\le C(P_R^M)^{2/3}.}
\tag{S.342}
\]

S.342 的 deletion set 在时间上固定；pointwise moving exceptional set 不充分。第二，excess branch 应攻击较弱的 combined envelope S.328，而不是分别要求 \(M_R\) 与 \(L_R\) universal bounded；只要 product 保持 quadratic payment scale，较长 path 可以由较小 cylinder-density coefficient 抵消。第三，pure high-frequency heat shear 不是 physical-window gate 的反例候选；后续 exact-family search 必须制造 physical annular separation，并同时通过 \(Q\)、cubic、pressure 与 drift ledgers。

Step 13 **PROVED**：S.307--S.309 的 dimensionless/common-deletion representation；S.310--S.313 的 fixed-solution \(\ell^1(L_t^{4/3})\) finiteness 与 \(\delta^{1/4}\) common-window bound；S.314--S.315 的 general Holder bound；在明确假设 S.316 下 S.317--S.322 的 exact optimization algebra；S.323--S.325 的 smooth all-\(p\) abstract saturation witness；在 explicit geometric envelope S.328 下 S.326--S.330 的 payment-dependent Morrey implication；S.331 对 two-cap inference 的 sharpness；S.332--S.334 的 exact heat-shear identities；S.335--S.339 的 critical eight-ary abstract countermodel；以及 S.340--S.341 的 conditional incidence-charging theorem、exact cubic duality 与 Dini-subcritical criterion。

Step 13 **ABSTRACT BOUNDARY TESTS, NOT NSE COUNTEREXAMPLES**：S.323--S.325 的 synchronized temporal family；其后的 adaptive smooth rate/depth family；S.331 的 equal-coordinate two-cap family；S.335--S.339 的 eight-ary critical ancestor tree。

Step 13 **OPEN**：\(\mathfrak H^F_{4/3,N,R}\) 的 uniform payment bound；quadratic shell-selective estimate S.342；S.340 的 PDE incidence data 与 strict cubic Dini-Carleson gain；bare suitable-weak class 的 payment-dependent moving-tube estimate S.328；universal gates S.280、S.288、S.303，Step 11 S.272，Q.12 与 Q.1；以及 scale contraction、regularity、singularity formation 与 Navier--Stokes Millennium problem。

有限证书通过 31/31 exact、11/11 finite、4/4 dependency、22/22 structural 与 32/32 negative mutations；独立 Ruby verifier 通过 9/9 groups、72,027 exact cases、6/6 artifact locks、4/4 dependency locks、32/32 note checks、1/1 primary-artifact group 与 2/2 negative groups。它们检查 algebra、finite fixtures、hashes、structure 与 claim wording，不 machine-prove PDE estimates、open packing gates、Morrey hypothesis、abstract model 的 NSE realization、regularity 或 Millennium problem。

本步的 advance 是固定解的 algebraic terminal modulus、当前 two-term method 的 exact time-integrability exponent ceiling、excess branch 的较弱 combined Morrey interface，以及把 strict cubic Dini decay 指认为下一条件性 packing interface 的 critical-tree obstruction。**NOT CLAY.**
