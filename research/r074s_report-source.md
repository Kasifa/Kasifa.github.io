# R0.74S｜低 Rayleigh 耗散支的二次支付

## 0. 这一步得到什么

R0.74S Steps 1--6 已把一侧球完成、terminal Abel 恒等式、四通道 circular recombination 与未加权 genealogy 的抽象标量 no-go 分开封存。Step 7 回到 R0.74R 三分法的耗散主导支，得到一个新的正结果。

本步先把局部耗散 clock 精确拆成黏性耗散与反常缺陷，再按优先顺序分成三类：反常缺陷至少承担终端 clock 的八分之一；高 Rayleigh 黏性耗散至少承担八分之一；否则低 Rayleigh 黏性耗散承担超过四分之一。第三类由抛物归一化动能时间质量、Jensen 不等式和继承的 padded-shell 三次付款同时给出

\[
\sum_{k\in\mathcal I_{\rm lo}(\tau)}K_{k,R}(\tau)
\le C\,\mathscr L(\boldsymbol\lambda)^{1/3}(P_R^M)^{2/3}.
\]

这里不需要例外壳层，也不需要新的 signed cancellation。这个结论是全部壳层同时成立的严格二次支付，但只覆盖低 Rayleigh 耗散支；它不推出低 Rayleigh 时间集具有统一正测度。

高 Rayleigh 与反常缺陷两支仍然 **OPEN**。本步只给出它们的精确 residual ledger，以及“若未来证明剩余壳层数一致有界，则可用平方函数支付”的 **PROVED CONDITIONAL IMPLICATION**。继承的高频光滑剪切说明高 Rayleigh 时间集确实可以出现，但该剪切本身由已有 \(Q\)-ledger 支付，不是本定理的反例。

此前的 **PROVED ABSTRACT SCALAR NO-GO** 继续只排除 scalar completed-clock algebra 与未加权 genealogy；它不是 PDE/NSE 反例。无条件 stopped-work 估计、R0.74R 的普适 persistence 输入、固定尺度不等式、尺度收缩、正则性与奇点形成仍为 **OPEN / NOT CLAIMED**。**NOT CLAY.**

本节没有数值仿真、DNS 或 DGX。

## 1. 两个紧支撑一侧球 cutoff

保留 \(r_m=2^mR\)、\(\delta=R/8\) 与冻结过渡函数 \(\vartheta\)，定义

\[
\chi_{m,R}^-(y)=1-\vartheta\!\left(\frac{|y|-r_m}{\delta}\right),
\qquad
\chi_{m,R}^+(y)=\vartheta\!\left(\frac{r_m-|y|}{\delta}\right).
\]

两者都光滑、径向、紧支撑且取值于 \([0,1]\)。逐一检查 \(r_m-\delta,r_m,r_m+\delta\) 划分的四个径向区间，得到

\[
\boxed{
0\le\chi_{m,R}^-\le\chi_{m,R}^+\le1,
\qquad
\beta_m^R=\chi_{m,R}^+-\chi_{m,R}^-,
\qquad
\psi_m^R=\chi_{m+1,R}^+-\chi_{m,R}^- .}
\]

令 \(\mathsf B_{m,R}^{\pm}\) 为它们的周期化。两条径向梯度都带负号，因此对 R0.74S Step 3 的 work vector 有

\[
\boxed{
\int_{\mathbb T^3}\mathcal W_R^M\cdot\nabla\mathsf B_{m,R}^-=-J_{m,R}^-,
\qquad
\int_{\mathbb T^3}\mathcal W_R^M\cdot\nabla\mathsf B_{m,R}^+=-J_{m,R}^+.}
\]

这个符号决定了后面 root 与 outer 两行保留的是不同端点；不能在这里先取绝对值。

## 2. completed ball-clock tower

对任意非负紧支撑 lifted cutoff \(\phi\) 及其周期化 \(\Phi\)，定义端点能量、耗散、二次源项与通量四行

\[
\begin{aligned}
\mathscr E_R[\Phi](t)
&=\frac{\eta_R(t)}{2R}\int_{\mathbb T^3}\Phi|v_R|^2,\\
\mathscr D_R[\Phi](t)
&=\frac1R\int_{(s_R,t)\times\mathbb T^3}\eta_R\Phi\,d\boldsymbol\mu,\\
\mathscr Q_R[\Phi](t)
&=\frac1{2R}\int_{s_R}^{t}\!\int_{\mathbb T^3}
[\eta_R'\Phi+\eta_R\Delta\Phi]|v_R|^2,\\
\mathscr F_R[\Phi](t)
&=\frac1R\int_{s_R}^{t}\!\int_{\mathbb T^3}
\eta_R\mathcal W_R^M\cdot\nabla\Phi .
\end{aligned}
\]

写 \(\mathscr K_R=\mathscr Q_R+\mathscr F_R\)。R0.74P 的 suitable-weak 局部能量计算给出规范绝对连续代表

\[
\boxed{
\mathscr K_R[\Phi]=\mathscr E_R[\Phi]+\mathscr D_R[\Phi]\ge0,
\qquad
\mathscr K_R[\Phi](s_R)=0.}
\]

线性与上面的 cutoff 差分恒等式给出

\[
\boxed{
\begin{aligned}
\mathscr K_{m,R}^{+}-\mathscr K_{m,R}^{-}
&=\gamma_m^{-1}K_{m,R}^{\partial},\\
\mathscr K_{m+1,R}^{+}-\mathscr K_{m,R}^{-}
&=\gamma_m^{-1}K_{m,R}.
\end{aligned}}
\]

于是

\[
\boxed{
\mathscr K_{m+1,R}^{+}-\mathscr K_{m,R}^{+}
=\gamma_m^{-1}(K_{m,R}-K_{m,R}^{\partial})\ge0.}
\]

这是一条真正的单调 ball tower；但单调性本身只说明 residual 非负，并不把它从 \(\ell^1\) 变成 \(\ell^2\)。

## 3. 从 collar 到 ball 仍是二次付款

令

\[
d_m=\gamma_{m-1}-\gamma_m>0,
\qquad m\ge2.
\]

冻结权重满足 \(\sum_{k\ge j}\gamma_k\le(35/3)\gamma_j\)。把 lifted ball 分成中心球、硬边界 collar 与 padded-shell 内部后，得到点态 packing

\[
\begin{aligned}
&\sum_{k\ge1}\gamma_k\chi_{k,R}^-
+\sum_{k\ge1}\gamma_k\chi_{k+1,R}^+
+\sum_{m\ge2}d_m\chi_{m,R}^+\\
&\qquad\le C\left[
\mathbf1_{\{|y|<4R\}}+
\sum_{j\ge1}\gamma_j\mathbf1_{\operatorname{supp}\psi_j^R}(y)
\right].
\end{aligned}
\]

对应绝对 Laplacian 的和乘以 \(R^2\) 后也满足同一控制。危险的 outer collar \(C_j^+\) 上出现 \(\gamma_{j-1}\)，它由 \(\operatorname{supp}\psi_{j-1}^R\) 支付；不能错误地用 \(\gamma_j\) 代替。中心球另由

\[
R^{-3}\int_{I_{2R}}\int_{B_{4R}}|v_R|^2
\le32\,\mathcal E^{M,R}(z_0,8R)
\le32A_R
\]

支付。合并后

\[
\boxed{
\sum_{k\ge1}\gamma_k\operatorname{TV}\mathscr Q_{k,R}^-
+\sum_{k\ge1}\gamma_k\operatorname{TV}\mathscr Q_{k+1,R}^+
+\sum_{m\ge2}d_m\operatorname{TV}\mathscr Q_{m,R}^+
\le CA_R.}
\]

因此 ball completion 没有制造新的低阶损失；真正的问题是保留下来的 terminal \(\mathscr K\)-clock。

## 4. 三条 signed channel 的时间方向

固定 Step 2 的 stopped family \((\tau,I,\boldsymbol\sigma)\)。对 \(k\in I\)，令 \(\rho_k\) 为前驱 merge/终端时刻，\(\lambda_k\) 为后继 merge/终端时刻；内部边界从 \(\widehat\sigma_m=\max(\sigma_{m-1},\sigma_m)\) 开始激活。

精确积分得到：

\[
\frac1R\int_{s_R}^{\tau}\eta_R\mathcal R_R
=-\sum_{k\in I_{\rm rt}}\gamma_k
[\mathscr F_{k,R}^-(\rho_k)-\mathscr F_{k,R}^-(\sigma_k)],
\]

\[
-\frac1R\int_{s_R}^{\tau}\eta_R\mathcal L_R
=\sum_{k\in I_{\rm out}}\gamma_k
[\mathscr F_{k+1,R}^+(\lambda_k)-\mathscr F_{k+1,R}^+(\sigma_k)],
\]

\[
\frac1R\int_{s_R}^{\tau}\eta_R\mathcal G_R
=\sum_{m\in I^\partial}d_m
[\mathscr F_{m,R}^+(\tau)-\mathscr F_{m,R}^+(\widehat\sigma_m)].
\]

用 \(\mathscr F=\mathscr K-\mathscr Q\)、\(\mathscr K\ge0\) 与二次付款，只能分别留下

\[
\begin{aligned}
\left[R^{-1}\int\eta_R\mathcal R_R\right]_+
&\le\sum_{k\in I_{\rm rt}}\gamma_k\mathscr K_{k,R}^-(\sigma_k)+CA_R,\\
\left[-R^{-1}\int\eta_R\mathcal L_R\right]_+
&\le\sum_{k\in I_{\rm out}}\gamma_k\mathscr K_{k+1,R}^+(\lambda_k)+CA_R,\\
\left[R^{-1}\int\eta_R\mathcal G_R\right]_+
&\le\sum_{m\in I^\partial}d_m\mathscr K_{m,R}^+(\tau)+CA_R.
\end{aligned}
\]

不对称性是精确的：root 留在起始 stop，outer 留在 merge，weight-drop 留在终端。正性不会自动抹掉这些值。

## 5. terminal weight-drop 的 Abel 恒等式

在好时刻 \(t\) 写 \(B_m=\mathscr K_{m,R}^+(t)\)。有限求和分部给出

\[
\sum_{m=2}^{M}d_mB_m
=\gamma_1B_2+
\sum_{m=2}^{M-1}\gamma_m(B_{m+1}-B_m)
-\gamma_MB_M.
\]

由 ball tower，中间项正好等于

\[
\sum_{m=2}^{M-1}[K_{m,R}(t)-K_{m,R}^{\partial}(t)].
\]

固定 \(R,t\) 时，周期化 ball clock 至多按 \(1+2^{3M}\) 增长；而 \(\gamma_M=\exp(-4^{M-1}/32)\)，所以 \(\gamma_MB_M\to0\)。取极限并补回 \(m=1\) 得到

\[
\boxed{
\sum_{m\ge2}d_m\mathscr K_{m,R}^{+}(t)
=\gamma_1\mathscr K_{1,R}^{+}(t)
+\sum_{m\ge1}[K_{m,R}(t)-K_{m,R}^{\partial}(t)].}
\]

每一项都非负。因此对任意有限 \(H\subset\{2,3,\ldots\}\)，

\[
\sum_{m\in H}d_m\mathscr K_{m,R}^{+}(t)
\le\gamma_1\mathscr K_{1,R}^{+}(t)+Y_{1,R}^{\rm clk}.
\]

这是正确且有限的 \(\ell^1\) 估计，却没有任何平方函数压缩。把它代回 weight-drop 行，只会返回已经知道的大付款 ledger。

## 6. 抽象时钟塔严格饱和这个损失

取任意 \(N\ge1\) 与光滑单调函数 \(h\)，满足 \(h(s_R)=0\)、\(h(\tau)=1\)。规定

\[
K_{m,R}(t)=
\begin{cases}h(t),&1\le m\le N,\\0,&m>N,
\end{cases}
\qquad
K_{m,R}^{\partial}=0,
\qquad
\mathscr K_{1,R}^{+}=0,
\qquad
\mathscr K_{m,R}^{-}=\mathscr K_{m,R}^{+}.
\]

其余 ball tower 由单调差分递归定义。再在纯标量层面取 \(\mathscr E=\mathscr K\)、\(\mathscr D=\mathscr Q=0\)、\(\mathscr F=\mathscr K\)，所有 completed-clock 与线性 tower 恒等式都逐项成立。

在终端时刻，前 \(N\) 个 shell positive variations 都等于 1，于是

\[
\boxed{
Y_{2,R}^{\rm sf}=\sqrt N,
\qquad
\sum_{m\ge2}d_m\mathscr K_{m,R}^{+}(\tau)=N.}
\]

所以不存在仅由上述标量代数推出的普适常数 \(C\)，使

\[
\sum_{m\ge2}d_m\mathscr K_{m,R}^{+}(\tau)
\le C\,Y_{2,R}^{\rm sf}.
\]

这就是本节的 no-go：**positive completion + linear tower + \(\ell^1\) summation** 不能单独关闭匹配平方函数。这个见证没有空间算子或 PDE 实现，因此不排除真正利用 Navier--Stokes 方程、跨通道符号或有限 genealogy 的定理。

## 7. 四通道 signed recombination 精确返回原问题

对 \(X\in\{E,D,Q,F,K\}\)，把 root、outer、weight-drop 与 mismatch 四行按 stopped 时间方向组合成 \(\mathfrak C_X\)。有限块分解与 cutoff 线性给出

\[
\boxed{\mathfrak C_X=\sum_{k\in I}[X_{k,R}(\tau)-X_{k,R}(\sigma_k)].}
\]

特别地，\(X=F\) 时 \(\mathfrak C_F=W_R^M\)，而 \(F=K-Q\) 给出

\[
\boxed{
W_R^M=\sum_{k\in I}\Delta_{\sigma_k}^{\tau}K_{k,R}
-\sum_{k\in I}\Delta_{\sigma_k}^{\tau}Q_{k,R}.}
\]

二次 \(Q\) 行已由 \(CA_R\) 支付，但终端 upcrossing 恰好满足

\[
\mathfrak C_K=\sum_{k\in I}\Delta_{\sigma_k}^{\tau}K_{k,R}
>\frac14\sum_{k\in I}K_{k,R}(\tau).
\]

因此完整 signed recombination 没有把困难项压小，而是精确重建了要控制的对象。这是 **CIRCULAR ROUTE / PROVED**，不是 PDE 反例。

## 8. 拆出 mismatch 后的三通道正结果

令 \(\Omega_A^R\) 为由 padded shells 减去内部 boundary bumps 得到的 genealogy cutoff。精确支撑几何证明 \(\Omega_A^R\ge0\)，且插入新 shell 时 cutoff 单调增加。对三通道 stopped work \(W_{R,3}^M\)，所有起始与 merge 时钟相消，得到

\[
\boxed{[W_{R,3}^M]_+\le \Phi_I(\tau)+CA_R.}
\]

这里 \(\Phi_I=\mathscr K_R[\Omega_I^R]\)。若最终块为 \([a,b]_{\mathbb Z}\)，写 \(r_m=K_{m,R}-K_{m,R}^{\partial}\ge0\)，则终端量有精确非负分解

\[
\boxed{
\Phi_I(t)=\sum_{[a,b]\in\operatorname{Comp}(I)}
\left[K_{a,R}^{\partial}(t)+\sum_{m=a}^{b}r_m(t)\right].}
\]

这是本节保留的正结果：三通道重组消除了 temporal genealogy debt；剩余障碍被定位到每个最终块的 root-boundary clock 与完整 \(\ell^1\) residual，而不是停止时刻本身。

## 9. 单块标量族排除未加权 genealogy 压缩

取 \(I_N=\{1,\ldots,N\}\)，所有 shell 在同一时刻激活，边界 clocks 为零，令 \(K_{k,R}=F_{k,R}=h\)、\(Q=D=0\)，并用 tower identity 递归构造 ball clocks。所有标量 completed-clock 恒等式逐项成立，且

\[
\boxed{W_N^{\rm sc}=N,\qquad Y_{2,R}^{\rm sf}=\sqrt N.}
\]

同时

\[
\sup_t\#\operatorname{Comp}(I(t))=1,
\qquad \#\{\text{activation epochs}\}=1,
\qquad \#\{\text{block mergers}\}=0.
\]

因此 component、epoch 或 merger 数单独不能完成 \(\ell^1\to\ell^2\) 压缩。有限 genealogy 的精确计数为

\[
\boxed{|I_{\rm rt}|+|I_{\rm out}|+|I^\partial|=2|I|-e_{\rm tie},}
\]

仍是 \(O(|I|)\)，不是无维数损失的平方函数界。这个结论只排除 **scalar completed-clock algebra + unweighted genealogy**；PDE-weighted block length、耗散支付与跨通道动力学符号仍可能有效。

## 10. 局部耗散的精确拆分与 Rayleigh 时间集

保留 R0.74P 的 suitable-weak 总局部耗散测度

\[
\boldsymbol\mu=|\nabla u|^2\,dx\,dt+\boldsymbol D,
\qquad \boldsymbol D\ge0.
\]

对每个壳层定义动能与黏性密度

\[
e_{k,R}(t)=\frac{\gamma_k\eta_R(t)}{2R}
\int_{\mathbb T^3}\Psi_k^R|v_R|^2,
\qquad
g_{k,R}(t)=\frac{\gamma_k\eta_R(t)}{R}
\int_{\mathbb T^3}\Psi_k^R|\nabla v_R|^2.
\]

把共同零测集上的代表取为零后，两行均可测。对好终端时刻 \(\tau\)，耗散 clock 精确分解为

\[
D_{k,R}(\tau)=\int_{s_R}^{\tau}g_{k,R}(t)\,dt+m_{k,R}(\tau),
\qquad m_{k,R}(\tau)\ge0,
\]

其中 \(m_{k,R}\) 是反常缺陷部分。给定正序列 \(\boldsymbol\lambda=(\lambda_k)\)，直接定义

\[
L_{k,R}=\left\{g_{k,R}\le\frac{2\lambda_k}{R^2}e_{k,R}\right\},
\qquad H_{k,R}=(s_R,\tau)\setminus L_{k,R}.
\]

当分母与 \(\eta_R\) 为正时，这等价于 cutoff-weighted ratio

\[
\rho_{k,R}=R^2\frac{\int\Psi_k^R|\nabla v_R|^2}{\int\Psi_k^R|v_R|^2}
\le\lambda_k.
\]

原定义不做除法；分母为零时两行同时为零，因此没有 \(0/0\) 约定。

## 11. 八分之一、八分之一、四分之一三分法

对耗散主导壳层写 \(T_k=K_{k,R}(\tau)>0\) 且 \(D_{k,R}(\tau)\ge T_k/2\)。按优先顺序定义 defect、high 与 low 三类：

\[
\begin{aligned}
\mathcal I_{\rm def}&=\{m_{k,R}(\tau)\ge T_k/8\},\\
\mathcal I_{\rm hi}&=\left\{k\notin\mathcal I_{\rm def}:\int_{H_{k,R}}g_{k,R}\ge T_k/8\right\},\\
\mathcal I_{\rm lo}&=\mathcal I_D\setminus(\mathcal I_{\rm def}\cup\mathcal I_{\rm hi}).
\end{aligned}
\]

剩余的低 Rayleigh 类满足精确严格不等式

\[
\int_{L_{k,R}}g_{k,R}>\frac14T_k,
\qquad
\frac1{R^2}\int_{L_{k,R}}e_{k,R}>\frac{T_k}{8\lambda_k}.
\]

令 \(\delta_{k,R}=|L_{k,R}|/R^2\)。冻结时间窗只给 \(0<\delta_{k,R}\le4\)，但这已经足够使 Jensen 给出

\[
\frac1{R^2}\int_{L_{k,R}}e_{k,R}^{3/2}
\ge\frac12\left(\frac{T_k}{8\lambda_k}\right)^{3/2}.
\]

时间集变薄不会破坏这一步：在固定动能时间质量下，它反而增大 \(L_t^{3/2}\) 行。这里证明的是积分质量，不是统一时间厚度。

## 12. 全壳层低 Rayleigh 二次支付

把 R0.74R 的 padded-shell 三次付款限制到每个壳层自己的 \(L_{k,R}\)：

\[
p_{k,R}^{\rm lo}=R^{-2}\gamma_k\int_{L_{k,R}}\eta_R^{3/2}
\int_{\operatorname{supp}\psi_k^R}|\widetilde v_R|^3.
\]

空间 Hölder 与上一节合并，先得到逐壳层估计

\[
T_k\le C_2\lambda_k2^k\gamma_k^{1/3}
(p_{k,R}^{\rm lo})^{2/3}.
\]

定义

\[
\mathscr L(\boldsymbol\lambda)
=\sum_{k\ge1}2^{3k}\gamma_k\lambda_k^3.
\]

只要 \(\mathscr L(\boldsymbol\lambda)<\infty\)，跨壳层 Hölder 与继承的非负付款给出

\[
\boxed{
\sum_{k\in\mathcal I_{\rm lo}(\tau)}K_{k,R}(\tau)
\le C_3\mathscr L(\boldsymbol\lambda)^{1/3}(P_R^M)^{2/3}.}
\]

常数序列 \(\lambda_k=1\) 可用；\(\lambda_k=\gamma_k^{-\alpha}\) 在 \(0\le\alpha<1/3\) 时可用；近临界序列

\[
\lambda_k^{(\varepsilon)}=2^{-(1+\varepsilon)k}\gamma_k^{-1/3}
\]

给出 \(\mathscr L=2^{-3\varepsilon}/(1-2^{-3\varepsilon})\)。临界 \(\varepsilon=0\) 时每个 summand 等于 1，级数发散。这只是本论证的序列空间边界，不是任意解自动满足的 Rayleigh profile。

## 13. 未关闭 residual 与条件 finite-exception 接口

耗散主导族的完整剩余账本是

\[
\begin{aligned}
\sum_{k\in\mathcal I_D(\tau)}T_k
\le{}&C_3\mathscr L(\boldsymbol\lambda)^{1/3}A_R\\
&+8\sum_{k\in\mathcal I_{\rm def}(\tau)}m_{k,R}(\tau)
+8\sum_{k\in\mathcal I_{\rm hi}(\tau)}\int_{H_{k,R}}g_{k,R},
\qquad A_R=(P_R^M)^{2/3}.
\end{aligned}
\]

这条不等式没有隐藏新的 \(\ell^1\) clock remainder，但也没有控制最后两项。若未来 PDE 定理证明

\[
\#(\mathcal I_{\rm def}(\tau)\cup\mathcal I_{\rm hi}(\tau))\le N_D,
\]

则 Cauchy--Schwarz 立即给出剩余 clock 至多为 \(\sqrt{N_D}Y_{2,R}^{\rm sf}\)。这是 **PROVED CONDITIONAL IMPLICATION ONLY**；本步没有证明一致有限例外，更没有由此推出 (Q.1)。

## 14. 高频剪切诊断与严格边界

继承的光滑周期剪切

\[
u_N(t,x)=Ae^{-N^2(t-t_-)}\sin(Nx_2)e_1,
\qquad p_N=0,
\]

满足固定 cutoff 上 \(\rho_{k,R}^{(N)}/(R^2N^2)\to1\)。因此对固定阈值，充分高频时 high-Rayleigh 时间集可以在全部活跃时间出现；不能直接删除这一 residual。

但该剪切的 flux clock 满足 \(F_{k,R}=0\)，因而 \(K_{k,R}=Q_{k,R}\)，其 completed clocks 已由继承的 \(Q\)-variation ledger 支付。它只说明 high-Rayleigh 时间集非空，不是低 Rayleigh 定理或 completed-clock 估计的反例，也不把壳层自动放入优先类 \(\mathcal I_{\rm hi}\)。

Step 7 严格证明低 Rayleigh 耗散支的同时二次支付、精确 residual ledger 与条件 finite-exception implication。高 Rayleigh 支、反常缺陷支、stopped-work depletion、任意时钟 extraction、(Q.1)、尺度收缩与正则性仍为 **OPEN**。**NOT CLAY.**

## 15. 证书与独立审计

Step 5 最终确定性证书通过：

- 5/5 个精确 ledger 行；
- 7/7 个有限检查；
- 55/55 个结构检查；
- 4/4 个负向符号突变检查。

有限覆盖包括 312 个有理 cutoff 值、228 个导数样本、1024 个含并列 stop 的 stopped configuration、82432 个布尔激活比较、\(M=2,\ldots,8\) 的全部有限 Abel 端点，以及 \(N=1,\ldots,24\) 在五个有理时刻的抽象 tower。两个临时目录独立重算得到逐字节一致的 JSON 与 Markdown 报告。

Step 6 主证书另通过 4/4 exact、8/8 finite、58/58 structural、10/10 mutation；独立 Ruby 实现通过 9/9 independent 与 8/8 mutation，且与 producer 交叉一致。九类 forged JSON 全部被拒绝。

Step 7 主证书通过 16/16 exact、8/8 finite、52/52 structural、9/9 negative mutations。独立 Ruby 链通过 6/6 groups、31/31 structural 与 9/9 adversarial mutations，并与主 producer 交叉一致。主文 SHA-256 为 `e835a104f4a6f4d2281bef877dd6bfeb73f1c2396f6bd28203bb0812f7f8e3d3`。

这些是 **FINITE** 证书，只验证公式实现和符号哨兵；它们不机器证明 cutoff 光滑性、周期化/unfolding、suitable local-energy 计算、无限支撑估计或抽象见证的 PDE 实现。解析证明和有限证书必须继续分开。

## 16. 决定与下一门槛

本节已经 **PROVED**：

- 一侧 ball cutoff 与 flux 符号恒等式；
- completed ball-clock tower；
- 三族二次 \(\mathscr Q\) 付款；
- root、outer、weight-drop 的精确 stopped 时间方向；
- terminal weight-drop Abel 恒等式；
- 标量 positive-clock 的 \(\ell^1/\ell^2\) obstruction。
- 四通道 signed recombination 精确重建 stopped increments，证明该路线 circular；
- 三通道 genealogy cutoff 非负、插入符号有利、终端块分解精确；
- 单块标量族与有限 genealogy 计数的 abstract scalar no-go。
- 黏性/缺陷耗散的精确拆分与可测 low/high-Rayleigh 时间集；
- 八分之一、八分之一、四分之一优先三分法；
- 低 Rayleigh 动能时间质量、Jensen 转换与全壳层 \((P_R^M)^{2/3}\) 支付；
- admissible/critical Rayleigh profile 边界、精确 residual ledger 与条件 finite-exception implication。

本节关闭两条相邻的独立代数路线：分开估计所有 positive completions 只得到 \(\ell^1\)；完整保留符号再线性重组则精确返回原未知量。未加权 component/epoch/merger 计数也不能修复差距。

Step 7 已经关闭耗散主导族的 low-Rayleigh 部分。下一步应只检验 high-Rayleigh 黏性 residual 与 anomalous-defect residual 能否由 PDE 结构支付，或是否能证明一致 finite-exception theorem；不能把条件接口写成已完成定理。

root/outer/weight-drop 动力学控制、high-Rayleigh/defect residual、R0.74R persistence hypotheses、无条件固定尺度不等式 (Q.1)、尺度收缩、正则性、奇点形成和 Clay 问题全部保持 **OPEN / NOT CLAIMED**。

**LOW-RAYLEIGH BRANCH PAID. ABSTRACT SCALAR NO-GO RETAINED IN ITS ORIGINAL SCOPE. NOT CLAY.**

## 17. 继承边界

- actual collar traces 与四通道 split：继承自 R0.74S Step 3，PROVED；
- stopped-family activation：继承自 R0.74S Step 2，PROVED；
- thin boundary clock 与 \(K_m^\partial\le K_m\)：继承自 R0.74S Step 4，PROVED；
- suitable-weak completed-clock operator：继承自 R0.74P，PROVED；
- weighted \(S_2\) 与 doubled-radius support ledger：继承自 R0.74H，PROVED；
- frozen adjacent-weight tail：继承自 R0.74S Step 1，PROVED。
- suitable-weak 耗散测度与 completed shell clock：继承自 R0.74P，PROVED；
- shell-dependent cubic payment 与 padded-shell Hölder：继承自 R0.74R，PROVED；
- 高频光滑剪切诊断：继承自 R0.73Y 与 R0.74B，在其原范围内 PROVED。

不声称新颖性、优先权、正则性或千禧年问题结论。
