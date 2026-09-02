# R0.74S Step 15 中文发布源

## 95. Step 15：混合通量等价与终端 crown 强制性缺口

Step 14 把 short branch 的共同删除 flux tail S.342 与 excess branch 的 jump--corona input S.375 分成两条路线。Step 15 先证明一个此前未记录的精确归约：short last-exit residual 与 selected-excess residual 可以写进同一个非负 stopped physical-flux vector，并且在同一个 best-\(N\) 删除集合下与完整 residual 逐坐标等价。因而，若仍开放的 S.342 将来成立，同一个 \(N_F\) 会一次支付两条 residual 分支，不再需要另加 ancestor budget。

对独立的 crown 路线，本步把每个 terminal corona 压成只计一次的 disjoint crown，并证明其 cubic coefficient budget 与停止深度无关。这个组合结果没有提供缺失的 PDE coercivity：selected-crown nonlinear payment S.407 仍是 **OPEN PDE INPUT**。Periodic positive-measure tree 与 selected scalar clock 只分别通过几何和标量压力测试；它们没有被耦合成一个 completed-clock/measure fixture，更不是 Navier--Stokes 反例。

本步没有证明 S.342、S.375、S.407、Q.12、Q.1、scale contraction、regularity、singularity formation 或 Millennium problem，也不声称 novelty 或 priority。有限证书检查代数、组合、哈希、结构与边界措辞，不 machine-prove 开放的 PDE 输入。**NOT CLAY.**

## 96. Hybrid start 与同一物理通量向量

固定一个 Version-M suitable weak solution、尺度 \(R\) 与 good terminal \(\tau\)。保留

\[
 T_k=K_{k,R}(\tau),\qquad
 \ell_k=\ell_{k,2/3}^{K}(\tau),\qquad
 \mathcal I_{\rm res}(\tau)
 =\mathcal R_{\rm sh}(\tau)\mathbin{\dot\cup}\mathcal I_x(\tau).
\]

选取 frozen initial interval 中共同的 local-energy good time \(\sigma_0\)，使所有 shell 都有 \(K(\sigma_0)=Q(\sigma_0)=F(\sigma_0)=0\)。定义

\[
 \boxed{
 \sigma_k^{\rm hyb}(\tau):=
 \begin{cases}
   \ell_k(\tau),&k\in\mathcal R_{\rm sh}(\tau),\\
   \sigma_0,&k\in\mathcal I_x(\tau),\\
   \tau,&k\notin\mathcal I_{\rm res}(\tau),
 \end{cases}
 \qquad
 z_{k,R}^{\boldsymbol\lambda}(\tau)
 :=F_{k,R}(\tau)-F_{k,R}(\sigma_k^{\rm hyb}(\tau)).}
\tag{S.377}
\]

于是

\[
 \boxed{
 z_k=r_k^{\rm sh}=r_k\quad(k\in\mathcal R_{\rm sh}),\qquad
 z_k=F_{k,R}(\tau)=[F_{k,R}(\tau)]_+\quad(k\in\mathcal I_x),\qquad
 z_k=r_k=0\quad(k\notin\mathcal I_{\rm res}).}
\tag{S.378}
\]

Selected excess 因此是该 physical-flux vector 的 subcoordinate：

\[
 \boxed{0\le x_k^{\rm sel}(\tau)\le z_k(\tau)\qquad(k\ge1).}
\tag{S.379}
\]

S.377--S.379 是表示与符号结论，不是对 \(z\) 的 PDE bound。

## 97. 同一个 \(Q\)-variation diamond 与 best-\(N\) 等价

对 \(k\in\mathcal I_x(\tau)\)，令

\[
 U_k=Q_{k,R}(\ell_k),\qquad
 V_k=Q_{k,R}(\tau)-Q_{k,R}(\ell_k).
\]

两段 \(Q\)-variation 来自同一个 full-history variation measure，故不是两个可独立饱和的误差：

\[
 \boxed{|U_k|+|V_k|\le\operatorname{TV}_{J_\tau}Q_{k,R}<{T_k\over6}.}
\tag{S.380}
\]

Terminal clock 与 last-exit identity 为

\[
 \boxed{z_k=T_k-U_k-V_k,\qquad r_k={T_k\over3}-V_k.}
\tag{S.381}
\]

在 S.380 的同一个菱形约束内直接优化，得到 sharp scalar constants

\[
 \boxed{{1\over5}z_k<r_k<{3\over7}z_k\qquad(k\in\mathcal I_x(\tau)).}
\tag{S.382}
\]

与 short branch 上的 equality 合并，得到

\[
 \boxed{{1\over5}z_k(\tau)\le r_k(\tau)\le z_k(\tau),
 \qquad z(\tau)\in\ell^1_+.}
\tag{S.383}
\]

对同一个任意 shell set \(S\)、\(\#S\le N\) 先求和再优化，得到

\[
 \boxed{{1\over5}\mathcal S_N(z(\tau))
 \le\mathcal S_N(r(\tau))
 \le\mathcal S_N(z(\tau)).}
\tag{S.384}
\]

令 \(\mathfrak Z_{N,R}^{\boldsymbol\lambda}(\mathcal D)\) 为 good terminals 上 \(\mathcal S_N(z)\) 的 supremum，则

\[
 \boxed{{1\over5}\mathfrak Z_{N,R}^{\boldsymbol\lambda}(\mathcal D)
 \le\mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)
 \le\mathfrak Z_{N,R}^{\boldsymbol\lambda}(\mathcal D).}
\tag{S.385}
\]

因此完整 hybrid-flux gate 与完整 combined-residual gate 在同一个 terminal-dependent deletion budget 下按常数 \(1/5\) 与 \(1\) 等价。S.396 的 abstract scalar-ledger rows 分别把比值逼近 \(1/5\) 与 \(3/7\)，证明 S.382 的常数在已用标量约束内 sharp；它们不是 NSE counterexamples。

## 98. 一个 common-deletion temporal tail 同时支付两条分支

保留 Step 13 的 dimensionless flux density \(h_{k,R}\)。Absolute continuity 与 S.377 给出

\[
 \boxed{0\le z_k(\tau)
 \le\int_0^4h_{k,R}(\sigma)\,d\sigma
 \le4^{1-1/p}\|h_{k,R}\|_{L^p(0,4)},
 \qquad1\le p\le\infty.}
\tag{S.386}
\]

在取 terminal 或 branch 之前，整个 time norm 只删除同一个 shell set，因此

\[
 \boxed{\mathcal S_N(r(\tau))
 \le\mathcal S_N(z(\tau))
 \le4^{1-1/p}\mathfrak H^F_{p,N,R}.}
\tag{S.387}
\]

若把仍开放的 Step 13 estimate 明确作为 antecedent，

\[
 \boxed{\mathfrak H^F_{p,N_F,R}\le C_HA_R,
 \qquad A_R=(P_R^M)^{2/3},}
\tag{S.388}
\]

则同一个 \(N_F\) 给出

\[
 \boxed{\mathfrak R_{N_F,R}^{\boldsymbol\lambda}(\mathcal T_R)
 \le4^{1-1/p}C_HA_R,}
\tag{S.389}
\]

\[
 \boxed{\mathcal S_{N_F,R}^{K}(\mathcal T_R)
 \le\left[C_{\rm pay}(\boldsymbol\lambda)
 +6\,4^{1-1/p}C_H\right]A_R,}
\tag{S.390}
\]

并经 inherited terminal reduction 得到

\[
 \boxed{\mathfrak C_R^M
 \le C(\boldsymbol\lambda,p,N_F,C_H)
 \left[A_R+Y_{2,R}^{\rm sf}\right].}
\tag{S.391}
\]

S.388--S.391 证明的是 implication，不是 S.342 或 Q.1 本身。其新意义是 route-level：若 S.342 成立，它会同时关闭 short 与 selected-excess residual，不需要另加 \(N_b\) 或 ancestor coefficient。

## 99. Signed common window 的 start-clock debt

把 Step 14 的四通道 identity 积分在 hybrid active blocks 上，可写成

\[
 \boxed{
 \sum_{k\in G\cap\mathcal I_{\rm res}(\tau)}z_k(\tau)
 =\sum_{\alpha\in\{{\rm cub,loc,har,dr}\}}
 \sum_{k\in G\cap\mathcal I_{\rm res}(\tau)}
 \int_{\sigma_k^{\rm hyb}(\tau)}^\tau
 \dot F_{k,R}^{\alpha}(t)\,dt.}
\tag{S.392}
\]

这允许新的 PDE cancellation，但 algebraic regrouping 本身不产生 gain。对 common terminal window 起点 \(a=\max\{s_R,\tau-\delta R^2\}\)，若 shallow shell 满足 \(a\le\ell_k\)，则

\[
 \boxed{r_k^{\rm sh}=G_{k,\tau,\delta}
 +\left[K_{k,R}(a)-{2T_k\over3}\right]
 +\left[Q_{k,R}(\ell_k)-Q_{k,R}(a)\right].}
\tag{S.393}
\]

定义 start-clock overshoot

\[
 \omega_{k,\tau,\delta}
 :=\mathbf1_{\mathcal R_{\rm sh}^{\le\delta}(\tau)}(k)
 \left[K_{k,R}(a)-{2T_k\over3}\right]_+.
\]

同一个 deletion set 下的求和给出

\[
 \boxed{\begin{aligned}
 \sum_{k\in\mathcal R_{\rm sh}^{\le\delta}(\tau)\setminus S}r_k^{\rm sh}
 \le{}&
 \left[\sum_{k\in\mathcal R_{\rm sh}^{\le\delta}(\tau)\setminus S}
 G_{k,\tau,\delta}\right]_+
 +\sum_{k\notin S}\omega_{k,\tau,\delta}+C_QA_R.
 \end{aligned}}
\tag{S.394}
\]

于是 minimal signed common-window gate 为

\[
 \boxed{\begin{aligned}
 \mathcal S_N(r^{{\rm sh},\le\delta}(\tau))
 \le C_QA_R+\inf_{\#S\le N}\Bigg\{
 &\left[\sum_{k\in\mathcal R_{\rm sh}^{\le\delta}(\tau)\setminus S}
 G_{k,\tau,\delta}\right]_+\\
 &+\sum_{k\notin S}\omega_{k,\tau,\delta}\Bigg\}.
 \end{aligned}}
\tag{S.395}
\]

Last-exit maximality只控制 \(\ell_k<t\le\tau\)，不能控制更早的共同起点 \(a\)。S.397 的 abstract clock 取 \(K(a)=M\)、\(K(\ell)=2\)、\(K(\tau)=3\)，得到

\[
 \boxed{r=1,\qquad G=3-M,\qquad\omega=M-2,\qquad r=G+\omega.}
\tag{S.397}
\]

所以 signed synchronization 将逐坐标 absolute increment 换成了两个同删集合任务：common-window cancellation 与 start-clock overshoot control。这个 debt 是精确代数事实，但见证仍只是 abstract clock check。

## 100. Shellwise ownership 与 terminal crowns

对 selected ancestor，定义 finite positive Borel submeasure \(\alpha^{\rm anc}_{k,\tau}\)。Frozen definition 与 cutoff domination 给出

\[
 \boxed{b_k(\tau)=\alpha^{\rm anc}_{k,\tau}(\mathbb R\times\mathbb R^3),
 \qquad0\le d\alpha^{\rm anc}_{k,\tau}
 \le\gamma_k\mathbf1_{\widehat{\mathcal U}_{k,R}(\tau)}\,d\nu_R.}
\tag{S.398}
\]

对 countable locally finite half-open forest-top occurrences，分别按 shell 构造 Borel ownership：

\[
 \boxed{\widehat{\mathcal U}_{k,R}(\tau)
 =\mathop{\dot\bigcup}_{T:(T,k)\in\mathscr I_{\rm top}}\mathcal O_{Tk},
 \qquad\mathcal O_{Tk}\subset T\cap\widehat{\mathcal U}_{k,R}(\tau).}
\tag{S.399}
\]

Forest overlap 因而不重复 ancestor mass；adjacent-shell incidence、shifted-grid occurrence、periodic copy 与 repeated top occurrence 仍各自保留。定义 incidence-weighted top content

\[
 \boxed{\mathscr C_{\rm top}
 :=\sum_{(T,k)\in\mathscr I_{\rm top}}\gamma_k\rho_T<\infty.}
\tag{S.400}
\]

这里重复一个 top 会相应增加 \(\mathscr C_{\rm top}\)，不会被隐藏在几何常数中。

## 101. First roots、first jumps 与深度无关系数预算

取 canonical top level \(\lambda_T=m_T/\rho_T\)。First crossing roots 满足

\[
 \boxed{\sum_{S\in\mathscr R(T)}\rho_S\le{m_T\over\lambda_T}=\rho_T.}
\tag{S.401}
\]

从每个 root 迭代 first proper \(\kappa\)-jump descendants，则

\[
 \boxed{\sum_{S\in\mathscr J_j(T)}\rho_S\le\kappa^{-j}\rho_T,
 \qquad\sum_{j\ge0}\sum_{S\in\mathscr J_j(T)}\rho_S
 \le{\kappa\over\kappa-1}\rho_T.}
\tag{S.402}
\]

在任意 finite stopping depth \(L\)，top crown、各非终端 jump crown 与 terminal-depth crowns 构成 exact half-open partition：

\[
 \boxed{T=\Omega_T\mathbin{\dot\cup}
 \mathop{\dot\bigcup}_{0\le j\le L}
 \mathop{\dot\bigcup}_{S\in\mathscr J_j(T)}\Omega_S.}
\tag{S.403}
\]

每个 low-transition corona 只按一个 crown 计数，而不是在每一 dyadic generation 重复计数。Infinite-jump mass 保留在最后一个 finite-depth crown 中，不可在极限里丢弃。完整 crown--shell incidence multiset 因而满足

\[
 \boxed{\begin{aligned}
 \sum_{(\Omega_S,T,k)\in\mathscr C_L}\gamma_k\rho_S
 &\le C_{\kappa,L}\mathscr C_{\rm top}
 \le C_\kappa\mathscr C_{\rm top},\\
 C_\kappa&=1+{\kappa\over\kappa-1}
 ={2\kappa-1\over\kappa-1}.
 \end{aligned}}
\tag{S.404}
\]

S.404 的常数与 depth、top count 和 top levels 无关。这关闭的是 cubic coefficient side，不是 payment estimate。

## 102. Open nonlinear crown payment 与 conditional closure

先选择一个 common shell exception set \(E_\tau\)、\(\#E_\tau\le N_b\)，再对所有 tops、crowns、defect 与 high-Rayleigh channels 使用同一个集合。设 owned crown mass 分解为

\[
 \boxed{a_{Sk}=q_{Sk}+a_{Sk}^{\rm pay},
 \qquad\sum_{\mathscr C_L(E_\tau)}q_{Sk}\le C_qA_R.}
\tag{S.405}
\]

对 paid part 定义 canonical crown payment

\[
 \boxed{p_{Sk}^{\rm crown}
 ={(a_{Sk}^{\rm pay})^{3/2}\over(\gamma_k\rho_S)^{1/2}},
 \qquad{(a_{Sk}^{\rm pay})^3\over(p_{Sk}^{\rm crown})^2}
 =\gamma_k\rho_S\mathbf1_{\{a_{Sk}^{\rm pay}>0\}}.}
\tag{S.406}
\]

缺失的 PDE statement 是

\[
 \boxed{\sum_{\mathscr C_L(E_\tau)}p_{Sk}^{\rm crown}
 =\sum_{\mathscr C_L(E_\tau)}
 {(a_{Sk}^{\rm pay})^{3/2}\over(\gamma_k\rho_S)^{1/2}}
 \le C_pP_R^M.\qquad\textbf{OPEN}}
\tag{S.407}
\]

S.407 要求 constant 对 solution、\(R\)、\(\tau\)、forest、top count、levels 与 stopping depth 一致；同一份 frozen payment 若用于多个 occurrences，必须在 sum 中重复记录。它不是本步 local-energy inequality 的推论。

若 S.400、S.405、S.407 同时成立，则 Hölder 与 S.404--S.406 给出

\[
 \boxed{\mathcal S_{N_b}(b(\tau))
 \le\left[C_q+(C_\kappa\mathscr C_{\rm top})^{1/3}C_p^{2/3}\right]A_R.}
\tag{S.408}
\]

Proposition 3.1 因而是 **PROVED CONDITIONAL**：top boundary 与所有 low-transition crowns 的 bookkeeping 已闭合，但 antecedent S.407 仍开放。

## 103. Converse Hölder 与 linear-payment 方法障碍

对非负 \(a_i,p_i\)，\(A=\sum a_i\)、\(P=\sum p_i\)，Hölder 的精确 converse 为

\[
 \boxed{\sum_i{a_i^3\over p_i^2}\ge{A^3\over P^2},
 \qquad\inf_{p_i\ge0,\ \sum p_i=P}\sum_i{a_i^3\over p_i^2}
 ={A^3\over P^2}.}
\tag{S.409}
\]

Equality 恰在 \(p_i=(P/A)a_i\) 取得。固定任意 deletion budget \(N_b\)，取 \(M=N_b+1\) 个 distinct shell coordinates，并令

\[
 \boxed{b_{k_i}\ge H\quad(1\le i\le M),
 \qquad P_H=C_MH,\qquad A_H=(C_MH)^{2/3}.}
\tag{S.410}
\]

允许 forest、grids、levels、depth 与 common exception set 在看到 data 后自适应选择，完整 repeated incidence multiset 仍满足：若 \(q\)-budget 是 \(O(A_H)\)、payment 是 \(O(P_H)\)，则对 large \(H\)

\[
 \boxed{\sum_i{a_i^3\over p_i^2}
 \ge {H\over8C_p^2C_M^2}.}
\tag{S.411}
\]

等价地，若 cubic coefficient sum 被一个 fixed \(C_{\rm cor}\) 控制，则

\[
 \boxed{\sum q_k
 \ge H-C_{\rm cor}^{1/3}(C_pC_MH)^{2/3}.}
\tag{S.412}
\]

所以只有 linear payment 时，normalized \(q\)-budget 或 cubic coefficient budget 至少一项必须发散。这个 conclusion 是对 formal nonnegative incidence data 的 **ABSTRACT METHOD OBSTRUCTION**，不是 S.407 的 PDE 反例。

## 104. 两个未耦合的压力测试

Periodic positive-measure tree 取

\[
 \boxed{d\nu_H(\sigma,z)
 :=\sum_{n\in\mathbb Z^3}\sum_{i=1}^{M}{H\over\gamma_{k_i}}
 \delta_{\sigma_*}(d\sigma)
 {|Q_i^x|^{-1}\mathbf1_{Q_i^x+(2\pi/R)n}(z)\,dz}.}
\tag{S.413}
\]

在 standard grid 中，每个 retained child 满足

\[
 \boxed{\rho_v=2^{-d}\rho_0,\qquad
 m_v=8^{-d}m_0,\qquad
 \Theta(v)=4^{-d}\Theta(0).}
\tag{S.414}
\]

所以它没有 upward \(\kappa\)-jump，却保留任意深 low-transition coronas；所有 periodic copies 仍进入 finite constant \(C_M\)。独立地，把 Step 11 pure-defect scalar fixture 按 \(s=5H/3\) 缩放，得到

\[
 \boxed{T={5H\over3},\quad b=m=H,\quad r^x={5H\over9},
 \quad\sigma={959H\over7200}<{T\over12},
 \quad x={2641H\over3600}>{T\over6},\quad\beta=0.}
\tag{S.415}
\]

取 \(M=N_b+1\) 个 scalar copies 后

\[
 \boxed{{\mathcal S_{N_b}(b)\over A_H}
 \ge C_M^{-2/3}H^{1/3}\longrightarrow\infty.}
\tag{S.416}
\]

S.413--S.414 只测试 measure geometry；S.415--S.416 只测试 selected scalar-clock arithmetic。两者没有共享一个 completed-clock/measure identity，更没有共同 velocity-pressure Navier--Stokes realization。不得把它们的并列展示写成 coupled counterexample。

## 105. 路线决定、文献边界与证书

Step 15 把下一步可接受的输入压缩为两条独立路线。

1. 证明 S.342。由 S.387--S.391，这一个 common-deletion theorem 用同一个 \(N_F\) 关闭整个 combined residual，ancestor jump--corona route 随即不再需要。
2. 若保留 ancestor route，则 S.404 已给出所有 finite-depth terminal crowns 的 depth-independent coefficient budget；剩余的新 PDE burden 是 S.407 的 occurrence-level \(3/2\)-coercivity。它必须在同一个 shell deletion 后同时记录 top/stopping faces、pressure、moving drift、defect 与 infinite-jump remainder。

还有一条更直接但同样未证的接口：用 signed local-energy cancellation 证明 \(\mathfrak Z_{N,R}^{\boldsymbol\lambda}(\mathcal T_R)\lesssim A_R\)。由 S.385，它与 Step 10 residual gate 只差 literal factor \(5\)。对 shallow short intervals，S.395 说明任何 signed common-window proof 还必须控制 start-clock overshoot。

Frozen note 的 bounded collision boundary 比较了 physical-space flux locality、skewed-cylinder maximal/covering estimates、reverse Holder under extra local kinetic control、anomalous-dissipation support results、quantitative partial regularity 与 Navier--Stokes inequality flexibility。它们都没有提供 S.342 或 S.407 的 frozen quantifiers。这只是有限 collision check，不是 exhaustive review，也不是 novelty 或 priority claim。

本步 **PROVED**：S.377--S.387 的 hybrid vector、sharp coordinate comparison 与 same-deletion best-\(N\) equivalence；S.388--S.391 的 conditional implication；S.392--S.395 的 signed-window debt identity；S.396--S.397 的 abstract sharpness checks；S.398--S.404 的 ancestor submeasure、ownership、terminal crowns 与 depth-independent coefficient content；S.405--S.408 的 exact factorization 与 conditional Hölder closure；S.409--S.412 的 converse-Hölder method obstruction；S.413--S.416 的两个 separate stress tests。

本步 **OPEN PDE INPUTS**：common-deletion temporal flux tail S.342；selected-crown nonlinear payment S.407；以及 inherited S.375。继续 **OPEN**：S.288、S.303、S.272、Q.12、Q.1、scale contraction、regularity、singularity formation 与 Navier--Stokes Millennium problem。

Frozen primary certificate 通过 9/9 finite groups、3,941 finite cases、5/5 dependency、45/45 structural 与 20/20 negative checks。Independent Ruby verifier 从头重建 vectors、deletion sets、trees、crowns 与 incidence rows，并锁定两篇主文、两份实现、certificate 与 report 的哈希；它检查 finite algebra 与 combinatorics，不证明 S.342、S.407 或任何 PDE realization。Primary analytic audit 与 independent audit 均在这个边界内 PASS。**FINITE ONLY. NOT CLAY.**
