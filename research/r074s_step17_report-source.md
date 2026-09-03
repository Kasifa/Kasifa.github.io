# R0.74S Step 17 中文读者稿

## 116. 路线修正：闭流线复现使绝对时间变差从 \(A^2\) 升到 \(A^3\)

Step 16 在同一 Taylor 1923 光滑精确解上选取 terminal centre \(x_*=(\pi/4,0,0)\)。该点位于非复现的 separatrix 路径：轨迹只穿过关键相位一次，因此绝对 flux variation 是 \(A^2\)。这个计算对该特殊 terminal setting 完全正确，却不能决定对所有 terminal settings 量化的 S.444。

Step 17 把终点移到同一解的一条 regular closed streamline。在固定物理时间窗中，Version-M 中心完成 \(O_R(A)\) 次闭轨道返回；每次 flux density 的瞬时尺度为 \(A^3\)。有符号增量在一圈圈之间抵消，但绝对时间变差会逐圈累加。

最终结论是：对所有 \(p\in[1,\infty]\)、所有有限删除预算 \(N\) 以及所有 \(\beta<1\)，power-only absolute temporal-tail 都失败。尤其 \(p=1,\beta=2/3\) 正是否定 S.444 的量词组合，所以 **S.444 为 FALSE**。

这不是 DNS，也不是数值 Navier--Stokes 仿真。图中轨道与曲线来自精确解公式的确定性解析可视化。例子全局光滑；S.472、direct hybrid gate、S.407、Q.12、Q.1、scale contraction 与 regularity 仍 OPEN。**NOT CLAY.**

## 117. 同一 Taylor 精确族上的 regular closed streamline

在 \(\mathbb T^3=(-\pi,\pi]^3\) 上定义

\[
 \boxed{\psi=\sin x_1\sin x_2,\qquad
 W=(\sin x_1\cos x_2,-\cos x_1\sin x_2,0).}
 \tag{S.445}
\]

令 \(p_W=(\cos2x_1+\cos2x_2)/4\)、\(b_A(t)=Ae^{-2(t-t_0)}\)、\(u_A=b_AW\)、\(p_A=b_A^2p_W\)。由 \(\nabla\!\cdot W=0\)、\(\Delta W=-2W\) 和 \((W\!\cdot\!\nabla)W=-\nabla p_W\)，它对每个 \(A>0\) 都是 smooth、periodic、mean-zero、unforced 的精确三维 NSE 解。

取 \(\Gamma=\{\sin x_1\sin x_2=1/2\}\) 在 \((0,\pi)^2\) 中的分支。它由上下两条显式图形拼成一个 compact regular oval，且 \(W\) 在其上无零点并沿切向流动。令 \(\chi'=W(\chi)\)、\(\chi(0)=(\pi/4,\pi/4,0)\)，则存在有限周期 \(T_*>0\)：

\[
 \boxed{\chi(s+T_*)=\chi(s),\qquad T_*=\int_\Gamma{d\ell\over|W|}.}
 \tag{S.447}
\]

记 \(g(s)=|W(\chi(s))|^2\)、\(q=g'\)。同一轨道上两点的 \(g\) 值分别为 \(1/2\) 与 \(3/4\)，所以 \(q\not\equiv0\)，且对所有 \(p\ge1\)，一个足够长的 phase interval 都包含线性多份完整周期：

\[
 L\ge2T_*\Longrightarrow
 \int_a^{a+L}|q(s)|^pds\ge{V_p\over2T_*}L,
 \qquad V_p=\int_0^{T_*}|q|^p>0.
 \tag{S.449}
\]

## 118. 任意 \(N+1\) 个物理 annuli 同时激活，Version-M 中心线性多次回返

先固定任意有限删除预算 \(N\)，再令 \(M=N+1\)，最后选择足够小的 admissible \(R\)。Step 16 的 Fourier multiplier 与 support/cosine 论证给出前 \(M\) 个 physical shells 的系数

\[
 c_{k,R}\ge{1\over2}m_{k,R}>0,
 \qquad 1\le k\le M.
\]

Version-M 的 terminally anchored path 恰为

\[
 \boxed{\theta_A(t)=\mu_R\int_{t_0}^tb_A(r)dr,
 \qquad \xi_A(t)=\chi(\theta_A(t)),
 \qquad \theta_A'=\mu_Rb_A.}
 \tag{S.452}
\]

在 \(I_R=(t_0-R^2,t_0)\) 上，phase length 是

\[
 \boxed{L_A={\mu_RA\over2}(e^{2R^2}-1)\asymp_RA.}
 \tag{S.453}
\]

因此随 \(A\to\infty\)，中心在固定物理时间窗里完成线性多次 closed-orbit recurrence。这一机制与 Step 16 的单次 separatrix passage 不同。

## 119. 绝对时间尾对每个 \(p\ge1\) 都是 \(A^3\)

固定框架的 kinetic 与 physical-pressure Bernoulli flux 仍精确抵消，pressure gauge 也逐壳层抵消；完整 Version-M 只留下 moving-cutoff drift：

\[
 \boxed{\dot F_{k,R}(t)=
 {\gamma_k\mu_Rc_{k,R}\over2R}\eta_R(t)b_A(t)^3q(\theta_A(t)).}
 \tag{S.454}
\]

在 \(I_R\) 上 \(\eta_R=1\)。用 \(d\theta=\mu_Rb_A\,dt\) 和周期平均后，所有有限 \(p\) 的 \(L_t^p\) norm 都获得 \(A^{3p}\) 的 \(p\) 次方下界；\(p=\infty\) 也在一个完整周期中达到 \(RA^3\) 尺度。删除至多 \(N=M-1\) 个 shell，前 \(M\) 个正坐标中至少留下一个。因此，对所有 \(p\in[1,\infty]\)，

\[
 \boxed{d_{p,N,R}A^3\le\mathfrak H^F_{p,N,R}
 \le D_{p,R}A^3,\qquad A\ge A_0(R).}
 \tag{S.459}
\]

下界是 continuum analytic statement；有限证书只核对精确恒等式、计数、删除量词和 exponent bookkeeping。

## 120. 完整 Version-M payment 仍是 \(A^3\)，所以所有 \(\beta<1\) 都失败

沿 compact orbit 平移不会改变 fixed smooth profiles 的幅值。local energy、exterior velocity/pressure、quadratic cutoff 与 harmonic rows 逐项给出至多 \(A^2\) 或 \(A^3\)；super-Gaussian all-copy sum 和 order-\(-4\) harmonic sum分别保持可和。good times 趋近 \(t_0\) 时，buffered local-energy endpoint 给出正的 \(A^2\) trace，其 \(3/2\) 次幂给出 payment 下界。于是

\[
 \boxed{c_RA^3\le P_R^M\le C_RA^3.}
 \tag{S.461}
\]

把它与 S.459 合并，若 \(\beta\ge0\) 使用 payment 上界，若 \(\beta<0\) 使用 payment 下界，得到

\[
 \boxed{{\mathfrak H^F_{p,N,R}\over(P_R^M)^\beta}
 \ge c_{p,N,R,\beta}A^{3(1-\beta)}\longrightarrow\infty,
 \qquad \beta<1.}
 \tag{S.462}
\]

量词顺序不可交换：对手先固定 \(p,N,\beta,C\)，然后取 \(M=N+1\)、选择 admissible \(R,z_0\)，最后令 \(A\) 足够大。取 \(p=1,\beta=2/3\) 就精确否定 S.444。对 absolute temporal-tail 的 power-only 形式，必要 payment exponent 至少为 \(1\)。

## 121. 有符号正向 excursion 仍只有 \(A^2\)

同一公式也说明 absolute value 丢失了什么。由于 \(d_tg(\theta_A)=\mu_Rb_Aq(\theta_A)\)，

\[
 \dot F_{k,R}={\gamma_kc_{k,R}\over2R}\eta_Rb_A^2{d\over dt}g(\theta_A).
 \tag{S.464}
\]

分部积分后，端点项与 cutoff/damping 项都只有 quadratic amplitude scale，从而

\[
 \boxed{\sum_{k\ge1}\operatorname{osc}_{[s_R,t_0)}F_{k,R}\le C_RA^2.}
 \tag{S.466}
\]

沿正确 orientation 选择同一周期内从 \(g=1/2\) 到 \(g=3/4\) 的有序两时刻，可得前 \(N+1\) 个坐标均有正向 \(c_{k,R}A^2\) excursion。于是 signed range 和 positive excursion 恰为 \(A^2\)，而 absolute variation 为 \(A^3\)。

## 122. BV/Jordan 分解精确识别 recurrent backtracking debt

在 \(p=1\) 时 dimensionless normalization 完全抵消：

\[
 \mathfrak H^F_{1,N,R}=\inf_{\#S\le N}\sum_{k\notin S}
 \operatorname{TV}_{[s_R,t_0)}F_{k,R}.
 \tag{S.467}
\]

令 \(V_{k,R}^\pm=\int[\pm\dot F_{k,R}]_+dt\)、\(B_{k,R}=\min(V^+,V^-)\)。由共同零起点和 Jordan decomposition，

\[
 \boxed{\operatorname{TV}F_{k,R}
 =|F_{k,R}(t_0^-)|+2B_{k,R}.}
 \tag{S.468}
\]

在 recurrent orbit 上，terminal endpoint 或 signed range 只有 \(A^2\)，但 backtracking debt \(B_{k,R}\) 在每个激活 shell 上达到 \(A^3\)。S.444 实际要求为每次上下往返付费；signed terminal problem 并不需要这笔重复债务。

## 123. 正确的后继目标是 fixed-deletion positive excursion / simultaneous height

定义正向有序 excursion 与 common-deletion tail

\[
 \boxed{\mathfrak O^{F,+}_{N,R}:=
 \inf_{\#S\le N}\sum_{k\notin S}
 \sup_{a<b}[F_{k,R}(b)-F_{k,R}(a)]_+.}
 \tag{S.469}
\]

每个 Step 15 hybrid coordinate 都是同一 \(F_{k,R}\) 的两时刻 increment，因此

\[
 \boxed{\mathfrak Z_{N,R}^{\boldsymbol\lambda}(\mathcal T_R)
 \le\mathfrak O^{F,+}_{N,R}\le\mathfrak H^F_{1,N,R}.}
 \tag{S.470}
\]

在当前 exact family 上，

\[
 \boxed{\mathfrak O^{F,+}_{N,R}\asymp A^2
 \asymp(P_R^M)^{2/3},\qquad
 \mathfrak H^F_{1,N,R}\asymp A^3.}
 \tag{S.471}
\]

因此 S.472--即 universal fixed-deletion positive-excursion estimate--是与 signed endpoint problem 对齐的充分输入，但目前仍 **OPEN**。它比 direct Step 15 gate 在量词上更强；更弱的 direct hybrid terminal-flux gate 也仍 OPEN，未来证明不必一定先证明 S.472。

把完成的非负 clocks 写成 \(K=F+Q\)，且 \(B_{Q,R}=\sum_k\operatorname{TV}Q_{k,R}\lesssim(P_R^M)^{2/3}\)，则 S.473--S.475 证明：S.444 对应 positive-variation packing，而正确的后继只需 maximal simultaneous height 或 positive-excursion packing。

## 124. 三份审计、双语言证书与期刊级四联图

Primary analytic audit 对 S.445--S.475 的 closed-orbit topology、periodic averaging、dimensionless \(L_t^p\) normalization、complete payment、fixed deletion、signed integration by parts 与 completed-clock inequalities 逐项复核，结论为 PASS。Independent adversarial audit 保留并关闭五项修复记录，最终也为 PASS。Literature audit 逐条检查 Taylor、Yang、Dascaliuc--Grujić、Wolf 与 Duchon--Robert 的来源、适用范围与 non-implication 边界；有限检索不构成 novelty 或 priority claim。

Python 主证书通过 12/12 finite groups、4,325 cases、11/11 structural checks 与 2/2 dependency locks。独立 Ruby 实现不调用 Python：7/7 exact groups 共 294 assertions、4/4 artifact/commit locks、20/20 semantic checks、32/32 negative mutations、3/3 artifact-path substitutions 与 14/14 reproducibility assertions 全部 PASS。

正式四联图展示 regular closed streamline、一个 orbit period 的 \(g\)、四次 return 中 signed cancellation 对 absolute debt 的分离，以及 slope 2 / slope 3 的 amplitude classes。图、caption、source-data、plot/validate scripts、manifest 与 QA 均公开；它是 analytic exact-field visualization，不是 DNS 或数值 NSE simulation。

## 125. 主张账本与严格下一接口

本节 **PROVED**：regular closed streamline 与 recurrence lemma；任意 \(N+1\) 个 physical shells 同时激活；exact Version-M recurrent path 与 flux identity；所有 \(p\ge1\) 的 \(A^3\) absolute temporal-tail；完整 \(P_R^M\asymp A^3\)；所有 \(\beta<1\) 的 power-only absolute tail 失败，尤其 **S.444 为 FALSE**；signed \(A^2\) range、BV/backtracking identity、positive-excursion implication 与 completed-clock comparison。

本节 **OPEN**：S.472 fixed-deletion positive excursion / simultaneous-height estimate。继续 **OPEN AND UNCHANGED**：direct hybrid gate、terminal-crown coercivity S.407、Q.12、Q.1、scale contraction 与 regularity。

路线决定不可回退：任何后续证明都不得再使用 S.342、S.444 或 \(\mathfrak H^F_{p,N,R}\lesssim(P_R^M)^\beta\) with \(\beta<1\)。下一 temporal task 只能研究 signed positive-excursion tail、fixed-deletion simultaneous height，或直接处理 Step 15 hybrid last-exit increments；terminal-crown 路线仍独立可用。**NOT CLAY.**
