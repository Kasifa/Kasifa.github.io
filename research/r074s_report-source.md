# R0.74S｜共享 best-N budget 与终端 trace 障碍

## 0. 这一步得到什么

R0.74S Steps 1--10 已把一侧球完成、terminal Abel 恒等式、四通道 circular recombination、未加权 genealogy 的抽象标量 no-go、低 Rayleigh 支付、no-exception exact-family no-go、canonical last exit 以及 paid/residual 六类分区逐项封存。Step 11 不再重复分区，而是精确回答两个 residual mechanisms 怎样共享一个 best-\(N\) budget，并分别把 short branch 与 scalar-excess branch 推到各自第一个仍缺失的 PDE 门槛。

本步先把局部耗散 clock 精确拆成黏性耗散与反常缺陷，再按优先顺序分成三类：反常缺陷至少承担终端 clock 的八分之一；高 Rayleigh 黏性耗散至少承担八分之一；否则低 Rayleigh 黏性耗散承担超过四分之一。第三类由抛物归一化动能时间质量、Jensen 不等式和继承的 padded-shell 三次付款同时给出

\[
\sum_{k\in\mathcal I_{\rm lo}(\tau)}K_{k,R}(\tau)
\le C\,\mathscr L(\boldsymbol\lambda)^{1/3}(P_R^M)^{2/3}.
\]

这里不需要例外壳层，也不需要新的 signed cancellation。这个结论是全部壳层同时成立的严格二次支付，但只覆盖低 Rayleigh 耗散支；它不推出低 Rayleigh 时间集具有统一正测度。

Step 8 引入标量 excess \(x\) 与 Jordan envelope \(X\)，证明 selected defect/high-Rayleigh residual 是既有 stopped-work ledger 的子账本。更关键的是，S.197--S.198 证明 no-exception stopped-work supremum \(\mathfrak W_{\rm up}\) 与 full terminal clock、full positive cumulative flux 只差已由二次 ledger 支付的 \(B_Q\)。R0.74O/P 的平滑精确族随后给出

\[
\frac{\mathfrak W_{{\rm up},R_j}^{M,*}}
{(P_{R_j}^{M,*})^{2/3}}\longrightarrow\infty,
\]

从而严格否定普适 no-exception 二次界。S.38 仍是正确的条件蕴含；被反证的是它若要作为无条件定理所需的 antecedent。下一条可行路线必须回到固定 best-\(N\)、随终端变化的例外集合，并用 \(\sqrt N,Y_{2,R}^{\rm sf}\) 支付尾部。

此前的 **PROVED ABSTRACT SCALAR NO-GO** 继续只排除 scalar completed-clock algebra 与未加权 genealogy；Step 8 的 no-go 由继承的真实平滑 NSE exact family 给出；Step 9 的 no-gain 说明 canonical stops 本身没有压缩。Step 10 证明四个 paid classes 合计只使用一个 \(6B_Q\) ledger 和一个 \(C_5\) cubic ledger，余项正好是 \(\mathcal R_{\rm sh}\cup\mathcal R_x\) 上的共享 best-\(N\) residual gate。Step 11 进一步证明共享 budget 的离散 infimal convolution；short branch 得到 inverse-duration 与 nested-tent 控制，却仍缺 depth zero 的 terminal trace；scalar-excess branch 与 residual best-\(N\) 以字面常数 \(1/5\) 与 \(3\) 等价。固定解的 tail tightness 不能替代与解和尺度无关的固定 \(N_0\)。现有 multi-packet exact families 也没有否定任意固定正 \(N\)。S.261、S.269、S.272、S.243、Q.12、Q.1、尺度收缩、正则性与奇点形成仍为 **OPEN / NOT CLAIMED**。**NOT CLAY.**

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

## 18. 三个时间测度与开放终端约定

固定 R0.74P--R0.74R 的 periodic suitable-weak Version-M 几何：黏性系数一、尺度 \(R\)、终端锚定路径 \(X_R\)、非降时间 cutoff \(\eta_R\)、padded shell cutoff \(\Psi_k^R\) 与权重 \(\gamma_k\)。写

\[
\mathcal T_R=(s_R,t_0),\qquad J_\tau=(s_R,\tau),\qquad s_R=t_0-4R^2.
\]

对 Borel 集 \(A\subset\mathcal T_R\) 定义

\[
\boxed{
\begin{aligned}
\sigma_{k,R}(A)&=R^{-2}\int_Ae_{k,R}(t)\,dt,\\
\nu_{k,R}(A)&=\gamma_kR^{-1}\int_{A\times\mathbb T^3}
\eta_R(t)\Psi_k^R(x-X_R(t))\,d\boldsymbol\mu(t,x),\\
\beta_{k,R}(A)&=\int_A|\dot Q_{k,R}(t)|\,dt.
\end{aligned}}
\]

\(\sigma\) 是抛物归一化动能测度，\(\nu\) 是黏性加反常缺陷的总耗散测度，\(\beta\) 是 canonical \(Q\)-primitive 的 total-variation measure。区间 \(J_\tau\) 在终端开口，与 inherited completed-clock 的 \((s_R,\tau)\) 约定一致，因此不会额外计入 \(t=\tau\) 的耗散原子。冻结 cutoff 与其导数在 \(s_R\) 的公共邻域内为零，左端也没有质量逃逸。

若 \(\boldsymbol\delta_{k,R}\) 是反常耗散的加权时间推前，则

\[
d\nu_{k,R}=g_{k,R}\,dt+d\boldsymbol\delta_{k,R},
\qquad \boldsymbol\delta_{k,R}(J_\tau)=m_{k,R}(\tau).
\]

在 inherited local-energy good terminal time 上，\(\nu_{k,R}(J_\tau)=D_{k,R}(\tau)\)，而 \(\beta_{k,R}(J_\tau)=\operatorname{TV}_{J_\tau}Q_{k,R}\)。这些是 S.163--S.166 的精确测度身份。

## 19. 标量 excess 与 Jordan envelope

固定正的确定性 profile \(\boldsymbol\lambda=(\lambda_k)\)，令

\[
\alpha_{k,R}^{\boldsymbol\lambda}
=\nu_{k,R}-\beta_{k,R}-2\lambda_k\sigma_{k,R}.
\]

两个 excess 层级分别是

\[
\boxed{
x_{k,R}^{\boldsymbol\lambda}(\tau)
=\bigl[\alpha_{k,R}^{\boldsymbol\lambda}(J_\tau)\bigr]_+,
\qquad
X_{k,R}^{\boldsymbol\lambda}(\tau)
=(\alpha_{k,R}^{\boldsymbol\lambda})^+(J_\tau).}
\]

\(x\) 先计算整个终端区间的 signed mass，再取标量正部；\(X\) 是 Jordan decomposition 的正测度质量，会保留不同时间区间之间被净额相消的局部正 excess。Hahn decomposition、Radon measure 正则性与 Urysohn 逼近给出

\[
0\le[\alpha(J_\tau)]_+\le\alpha^+(J_\tau)
=\sup_{A\in\mathcal B(J_\tau)}\alpha(A)
=\sup_{\substack{\phi\in C_c(J_\tau)\\0\le\phi\le1}}
\int_{J_\tau}\phi\,d\alpha.
\]

因此 \(0\le x\le X\)，并且

\[
\nu(J_\tau)\le\beta(J_\tau)+2\lambda\sigma(J_\tau)+x
\le\beta(J_\tau)+2\lambda\sigma(J_\tau)+X.
\]

终端三分法使用较小的 \(x\)；\(X\) 用于局部化与弱极限稳定性，不是更小的终端上界。

## 20. 六分之一优先三分法与两个已付分支

对 dissipation-dominated shell 写 \(T_k=K_{k,R}(\tau)>0\)、\(D_{k,R}(\tau)\ge T_k/2\)。按优先顺序检查

\[
\beta_{k,R}(J_\tau)\ge\frac16T_k,
\qquad
\sigma_{k,R}(J_\tau)>\frac{T_k}{12\lambda_k}.
\]

若两项都失败，则

\[
\alpha(J_\tau)>\frac12T_k-\frac16T_k-\frac16T_k
=\frac16T_k,
\]

所以 \(x_k>T_k/6\)。这给出 S.170--S.171 的 literal trichotomy：每个耗散主导正 clock 要么由 \(\beta\) 支付至少六分之一，要么有足够 kinetic time mass，要么进入 selected excess 类。

\(\beta\)-branch 由 inherited quadratic \(Q\)-variation ledger 支付。对 kinetic branch，令 \(\delta_\tau=|J_\tau|/R^2<4\)，Jensen 给出

\[
R^{-2}\int_{J_\tau}e_{k,R}^{3/2}
\ge\delta_\tau^{-1/2}\sigma_{k,R}(J_\tau)^{3/2}
>\frac12\left(\frac{T_k}{12\lambda_k}\right)^{3/2}.
\]

与 inherited padded-shell cubic estimate 合并可得

\[
T_k\le C_4\lambda_k2^k\gamma_k^{1/3}(p_{k,R}^\tau)^{2/3}.
\]

定义 \(\mathscr L(\boldsymbol\lambda)=\sum_k2^{3k}\gamma_k\lambda_k^3\)。若 \(\mathscr L<\infty\)，有限壳层 Hölder 与 monotone convergence 给出

\[
\boxed{
\sum_{k\in\mathcal I_\sigma(\tau)}T_k
\le C_5\mathscr L(\boldsymbol\lambda)^{1/3}(P_R^M)^{2/3}.}
\]

## 21. selected/global excess ledger 与 Step 7 比较

\(\beta\)-branch 满足 \(\sum_{\mathcal I_\beta}T_k\le C_\beta(P_R^M)^{2/3}\)，selected excess branch 满足 \(T_k\le6x_k\)。因此

\[
\boxed{
\sum_{k\in\mathcal I_D(\tau)}K_{k,R}(\tau)
\le C_6(1+\mathscr L^{1/3})(P_R^M)^{2/3}
+6\sum_{k\in\mathcal I_x(\tau)}x_{k,R}^{\boldsymbol\lambda}(\tau).}
\]

定义全壳层接口

\[
\mathfrak x_{1,R}^{\boldsymbol\lambda}=\sum_kx_{k,R}^{\boldsymbol\lambda},
\qquad
\mathcal X_{1,R}^{\boldsymbol\lambda}=\sum_kX_{k,R}^{\boldsymbol\lambda},
\qquad
\mathfrak x_{1,R}\le\mathcal X_{1,R}.
\]

selected inequality 因而可放宽为加上 \(6\mathfrak x_{1,R}\)，再放宽为加上 \(6\mathcal X_{1,R}\)。global sums 会覆盖已由 \(\beta\) 支付的壳层；\(X\) 还会保留被终端 signed mass 抵消的局部正 excess。

对 Step 7 同一个 high/low-Rayleigh 分割，逐壳层有

\[
\boxed{x_{k,R}\le X_{k,R}
\le m_{k,R}(\tau)+\int_{H_{k,R}}g_{k,R}(t)\,dt.}
\]

这是对 old raw residual 的逐壳层支配，但由于两步 priority partition 不同，不能说 Step 8 的 global sum 数值上严格小于 Step 7 的 prioritized residual。

## 22. exact shear、lower semicontinuity 与光滑公式边界

对 inherited heat shear，Step 7 已证明 \(F_k=0\)，故 \(K_k=Q_k\)。若 \(T_k=K_k(\tau)>0\)，则

\[
T_k=Q_k(\tau)\le\operatorname{TV}_{J_\tau}Q_k=\beta_k(J_\tau),
\qquad x_k(\tau)=0.
\]

所以它进入 \(\beta\)-priority branch，不是 excess theorem 的反例；这里不声称 Jordan envelope \(X_k\) 为零。

在 R0.74P 的 fixed-scale Version-M topology 下，若 \(u_n\to u\) strongly in \(L^3\)、\(\nabla u_n\rightharpoonup\nabla u\) in \(L^2\)、\(p_n\rightharpoonup p\) in \(L^{3/2}\)，则每个 fixed shell 上 \(\nu_n\rightharpoonup^*\nu\) locally，\(\sigma_n\to\sigma\) 与 \(\beta_n\to\beta\) in total variation。开放集 Portmanteau 与 Jordan continuous-test formula 分别给出

\[
x_k[u,p](\tau)\le\liminf_nx_k[u_n,p_n](\tau),
\qquad
X_k[u,p](\tau)\le\liminf_nX_k[u_n,p_n](\tau).
\]

finite-shell Fatou 再接 monotone convergence，得到 \(\mathfrak x_{1,R}\) 与 \(\mathcal X_{1,R}\) 的全壳层 lower semicontinuity。这个结论只在固定 \(R\) 的 inherited topology 中成立，不提供 cross-scale compactness。

若解本身光滑，则 defect measure 为零，且

\[
x_k=\left[\int_{s_R}^{\tau}
\left(g_k-|\dot Q_k|-2\lambda_kR^{-2}e_k\right)dt\right]_+,
\qquad
X_k=\int_{s_R}^{\tau}
\left[g_k-|\dot Q_k|-2\lambda_kR^{-2}e_k\right]_+dt.
\]

只有在另行提供满足上述 topology 的 smooth periodic NSE sequence 时，才能对这些光滑公式取 \(\liminf\)。本节不声称任意 suitable weak solution 都存在这样的 smooth approximants。

## 23. fixed-scale finiteness 与 terminal flux domination

由 signed-measure order \(\alpha\le\nu\) 得 \(\alpha^+\le\nu\)。Tonelli、\(\Theta_R=\sum_k\gamma_k\Psi_k^R\) 的 inherited \(C^2\)-convergence 与 local finiteness 给出

\[
\boxed{
0\le x_k\le X_k\le\nu_k(J_\tau),
\qquad
\mathcal X_{1,R}(\tau)
\le\sum_k\nu_k(J_\tau)<\infty.}
\]

这是 fixed-scale total-dissipation finiteness，不是关于 \(R\) 的一致二次界。

canonical primitives 在 \(s_R\) 为零，故 \(\beta_k(J_\tau)\ge|Q_k(\tau)|\)。completed-clock identity 给出

\[
\alpha_k(J_\tau)
=Q_k(\tau)+F_k(\tau)-E_k(\tau)-\beta_k(J_\tau)-2\lambda_k\sigma_k(J_\tau)
\le F_k(\tau).
\]

所以

\[
\boxed{x_k(\tau)\le[F_k(\tau)]_+,
\qquad
\mathfrak x_{1,R}(\tau)
\le\mathfrak L_{{\rm abs},R}^M\le CP_R^M.}
\]

线性 \(CP_R^M\) bound 在 \(P_R^M>1\) 时不是二次 \((P_R^M)^{2/3}\) bound。

## 24. selected excess 归入 Step 2 gate

在 \(\eta_R=\eta_R'=0\) 的共同初始区间内取 common good time \(\sigma_0\)。每个壳层都满足 \(K_k(\sigma_0)=Q_k(\sigma_0)=F_k(\sigma_0)=0\)。若 \(x_k(\tau)>0\)，则 \(K_k(\tau)>0\)，所以这个共同零起点满足 Step 2 的 strict upcrossing condition。对任意有限非空 \(G\subset\{k:x_k(\tau)>0\}\)，

\[
W_R^M(\tau;G,(\sigma_0)_{k\in G})
=\sum_{k\in G}F_k(\tau)
\ge\sum_{k\in G}x_k(\tau)>0.
\]

取 finite-family supremum 得

\[
\boxed{
\mathfrak x_{1,R}(\tau)
\le\mathfrak W_{{\rm up},R}^M
\le\mathfrak L_{{\rm abs},R}^M\le CP_R^M.}
\]

在 priority-selected excess class 上，\(\beta_k<T_k/6\) 且 \(|Q_k(\tau)|\le\beta_k\)，故

\[
F_k(\tau)=T_k-Q_k(\tau)
\ge T_k-|Q_k(\tau)|>\frac56T_k,
\qquad T_k<\frac65F_k(\tau).
\]

结合 \(\beta\) 与 kinetic 两个已付分支，S.196 给出

\[
\boxed{
\sum_{k\in\mathcal I_D(\tau)}K_{k,R}(\tau)
\le C_6(1+\mathscr L(\boldsymbol\lambda)^{1/3})(P_R^M)^{2/3}
+\frac65\mathfrak W_{{\rm up},R}^M.}
\]

这一步证明 selected defect/high-Rayleigh scalar residual 不是新的独立 obstruction，而是既有 stopped-work ledger 的子账本；但 Step 2 的 gate 本来就允许共同 zero start，所以它没有缩窄 no-exception supremum。

## 25. no-exception stopped work 与 full terminal flux 的等价

定义已付的 \(Q\)-variation、full terminal clock supremum 与 full positive cumulative flux：

\[
\boxed{
B_{Q,R}^M=\sum_k\operatorname{TV}_{[s_R,t_0)}Q_{k,R}
\le C_Q(P_R^M)^{2/3},
\quad
\mathcal K_R^M=\sup_{\tau\in\mathcal G_R}\sum_kK_{k,R}(\tau),
\quad
\mathfrak C_{{\rm full},R}^M
=\sup_{s_R<\tau<t_0}\left[\sum_kF_{k,R}(\tau)\right]_+.}
\]

对 S.37 任意 admissible stopped family，把 work 与同一终端的 full flux 直接相减；start 与 omitted-shell 两部分中的 \(K_k\) 都非负，余下的 \(Q\)-差总计至多 \(B_Q\)。反向则在 common good terminal time 上，对 \(K_k(\tau)>0\) 且 \(F_k(\tau)>0\) 的有限壳层集合使用共同 zero stop，再取 monotone limit；若某个 omitted shell 满足 \(K_k=0<F_k\)，则 \(F_k=-Q_k\)，总量仍至多 \(B_Q\)。因此 S.197--S.198 得到

\[
\boxed{
\mathcal K_R^M-B_{Q,R}^M
\le\mathfrak W_{{\rm up},R}^M
\le\mathcal K_R^M+B_{Q,R}^M,
\qquad
\bigl|\mathfrak W_{{\rm up},R}^M-
\mathfrak C_{{\rm full},R}^M\bigr|
\le B_{Q,R}^M.}
\]

第二条的系数一已经被 single-shell scalar stress \(K=0,Q=-B,F=B\) 证明 sharp。故 Step 2 no-exception observable 只是在已付二次误差 \(B_Q\) 内等价于 full-cutoff positive cumulative flux；它不是一个更小的 signed-depletion quantity。

## 26. smooth exact-family no-go

使用 inherited R0.74O/P smooth periodic exact family，已有

\[
\mathfrak C_{R_j}^{M,*}\asymp T_*,
\qquad
\mathfrak C_{{\rm full},R_j}^{M,*}\ge\mathfrak C_{R_j}^{M,*},
\qquad
(P_{R_j}^{M,*})^{2/3}\asymp\frac{T_*}{K_*},
\qquad K_*\to\infty.
\]

由于 S.198 的 additive \(Q\)-error 仅为 \(O((P_{R_j}^{M,*})^{2/3})\)，S.199 推出

\[
\boxed{
\frac{\mathfrak W_{{\rm up},R_j}^{M,*}}
{(P_{R_j}^{M,*})^{2/3}}\longrightarrow\infty.}
\]

也可只选 exact-family target shell：其 terminal clock 为 \(\gtrsim T_*\)，full \(Q\)-variation 为 \(O(T_*/K_*)\)，共同 zero stop 给 stopped work \(\gtrsim T_*\)。这个 witness 是 smooth、periodic、mean-zero、unforced、pressure-free 的真实 NSE solution family。

因此普适 antecedent

\[
\mathfrak W_{{\rm up},R}^M\lesssim(P_R^M)^{2/3}
\]

被严格 **REFUTED / no-go**。这不反驳 S.38 的条件代数、S.196、带 terminal exceptions 且由 \(Y_{2,R}^{\rm sf}\) 支付的估计，也不反驳 (Q.1)。

## 27. 压力测试、证书与下一门槛

本步还保留六类 stress tests：interior atom 被 Jordan formula 完整检测；\(\nu=\beta\) 的 already-paid dissipation 被 excess 扣除；高频 divergence-free functional family 排除仅靠 incompressibility/cutoff/Hölder 得到 \(x\) 或 \(X\) 的 cubic bound；符号密度的时间相消证明 \(X\) 可严格大于 \(x\)；质量向硬终端逃逸说明只能主张 lower semicontinuity；\(Q_n=n^{-1}\sin(nt)\) 说明 primitive uniform convergence 不能替代 \(\dot Q_n\) 的 strong \(L^1\) convergence。这些 stress tests 的 PDE 身份边界逐项保留。

最终 Step 8 主证书通过 16/16 exact、19/19 finite、75/75 structural、20/20 negative mutations。独立 Ruby 审计通过 14/14 groups、22/22 exact rows、61/61 structural、14/14 source mutations、10/10 artifact mutations 与 6/6 report checks。主文 SHA-256 为 `0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab`。有限证书支持实现可复现性，不替代 measure/PDE 解析证明。

Step 8 **PROVED**：S.163--S.196 的 three-measure excess interface、one-sixth trichotomy、两个已付分支、lower semicontinuity、fixed-scale finiteness、terminal flux domination 与 stopped-work bridge；S.197--S.198 的 no-exception two-sided equivalence；以及 S.199 的 smooth exact-family refutation。

继续 **OPEN**：固定 best-\(N_0\)、terminal-dependent exception estimate，并以 \(\sqrt{N_0}Y_{2,R}^{\rm sf}\) 支付例外尾；Jordan envelope 的二次/平方函数/finite-exception bound；smooth NSE approximation existence；R0.74R extraction hypotheses；unconditional fixed-scale (Q.1)、scale contraction、prescribed-centre packing 与 regularity。

明确 **NOT CLAIMED**：exact shear 的 \(X=0\)；selected excess sum lower semicontinuity；\(X\le\mathfrak W_{\rm up}\)；Step 8 缩窄 Step 2 gate；硬终端 mass convergence；新颖性、优先权、奇点或 Clay 结论。

下一步不再尝试 no-exception supremum。唯一冻结方向是回到 R0.74Q (Q.7)--(Q.12) 的 fixed best-\(N\)、terminal-dependent exceptions，并保留 \(\sqrt N,Y_{2,R}^{\rm sf}\) 付款。

**UNIVERSAL NO-EXCEPTION STOPPED-WORK QUADRATIC BOUND: REFUTED. CONDITIONAL S.38: RETAINED. NOT CLAY.**

## 28. Step 9 的结果与终端域

Step 9 不再修补已被 Step 8 反驳的 no-exception gate，而是回到 R0.74Q 的 fixed best-\(N\) terminal tail。必须区分 plateau 终端域 \(I_R\) 与 full clock interval \(\mathcal T_R=(s_R,t_0)\)：

\[
\mathfrak C_R^M(\mathcal D)
:=\sup_{\tau\in\mathcal D}\left[\sum_{k\ge1}F_{k,R}(\tau)\right]_+,
\qquad
\mathfrak C_R^M(I_R)\le \mathfrak C_R^M(\mathcal T_R).
\tag{S.200}
\]

只保留这个不等式，不声称两个终端域相等。记

\[
A_R=(P_R^M)^{2/3},\qquad Z_R=Y_{2,R}^{\rm sf},\qquad
B_{Q,R}^M=\sum_k\operatorname{TV}Q_{k,R}\le C_QA_R.
\tag{S.201}
\]

\(Q,F,K\) 连续、从零起步，\(K\ge0\)；继承的 variation 与 Step 8 有限性保证下文所有无穷和绝对收敛。

## 29. signed best-N tail 与正确量词

对 \(x\in\ell^1(\mathbb N;\mathbb R)\) 及固定整数 \(N\ge0\)，定义

\[
\mathcal S_N(x)
:=\inf_{S\subset\mathbb N,\,\#S\le N}
\left[\sum_{k\notin S}x_k\right]_+.
\tag{S.202}
\]

对 \(F\) 与 \(K\) 分别在终端域上取 \(\sup_\tau\)，得到 \(\mathcal S_{N,R}^{F}(\mathcal D)\) 与 \(\mathcal S_{N,R}^{K}(\mathcal D)\)，即 (S.203)。删除的只能是最大的 \(N\) 个正坐标，因而

\[
\mathcal S_N(x)
=\left[\sum_kx_k-\sum_{m=1}^{N}x_m^{+*}\right]_+,
\qquad
|\mathcal S_N(x)-\mathcal S_N(y)|\le\|x-y\|_{\ell^1}.
\]

这是 forced full signed tail：负坐标的 cancellation 不能被任意 finite-subset supremum 取代。正确量词是

\[
\boxed{\sup_{\tau}\inf_{\#S_\tau\le N}},
\]

其中 \(N\) 与终端、尺度、解无关，但最优例外集 \(S_\tau\) 可随 \(\tau\) 变化。它不是更强的 \(\inf_S\sup_\tau\)。

## 30. F-half-exit：精确二分之一

固定终端 \(\tau\)，令 \(f_k=F_{k,R}(\tau)\)。当 \(f_k\ne0\) 时，取最后一个满足

\[
\operatorname{sgn}(f_k)F_{k,R}(t)\le |f_k|/2
\]

的时刻 \(\ell_k^F(\tau)\)；当 \(f_k=0\) 时定义 \(\ell_k^F(\tau)=\tau\)，即 (S.204)。连续性立即给出

\[
F_{k,R}(\ell_k^F(\tau))={1\over2}F_{k,R}(\tau),
\qquad
F_{k,R}(\tau)-F_{k,R}(\ell_k^F(\tau))={1\over2}F_{k,R}(\tau).
\tag{S.205}
\]

在完整非例外 signed tail 上先求和，再取正部、\(\inf_S\) 与 \(\sup_\tau\)，得到

\[
\boxed{
\mathfrak W_{1/2,N,R}^{F}(\mathcal D)
={1\over2}\mathcal S_{N,R}^{F}(\mathcal D).}
\tag{S.207}
\]

对 plateau 域，这给出

\[
\mathfrak C_R^M
\le B_{Q,R}^M+\sqrt N\,Z_R
+2\mathfrak W_{1/2,N,R}^{F}(I_R).
\tag{S.208}
\]

但 F-half-exit 一般不满足 Step 2 的严格 S.25 upcrossing。精确反例 \(F(t)=t\)、\(K(t)=\min\{2t,1\}\)、\(\tau=1\) 中，\(\ell^F=1/2\)，但 \(K(1)-K(1/2)=0\)。因此 (S.209) 排除了“canonical half-exit 自动是 S.25 admissible stop”的推断。

## 31. K-theta last exit 与尖锐一个 B_Q

对 \(0<\theta<1\) 及 \(T_k=K_{k,R}(\tau)>0\)，令 \(\ell_{k,\theta}^{K}(\tau)\) 为最后一个满足 \(K_{k,R}(t)\le\theta T_k\) 的时刻；\(T_k=0\) 时取 \(\ell=\tau\)。由 \(F=K-Q\)，

\[
L_{k,\theta}(\tau)
:=F_k(\tau)-F_k(\ell_{k,\theta}^{K})
=(1-\theta)T_k-\Delta Q_{k,\theta}(\tau).
\tag{S.211}
\]

完整非例外 tail 的 last-exit observable 与 best-\(N\) clock tail 满足

\[
\boxed{
(1-\theta)\mathcal S_{N,R}^{K}(\mathcal D)-B_{Q,R}^M
\le\mathfrak W_{\theta,N,R}^{K}(\mathcal D)
\le(1-\theta)\mathcal S_{N,R}^{K}(\mathcal D)+B_{Q,R}^M.}
\tag{S.214}
\]

误差只是一个 \(B_Q\)，不是两个；系数 \(1\) 在单标量连续 clock 上可达，所以是尖锐的。对 \(0<\theta<3/4\)，正终端壳层有

\[
K_k(\tau)-K_k(\ell_{k,\theta}^{K})=(1-\theta)T_k>{1\over4}T_k.
\tag{S.215}
\]

因此在 good terminal 上，任意有限正终端壳层族可用共同稠密 good-time set 逼近，落入 S.37 的闭包。这只是有限族、正终端、good terminal 的 closure statement；它不说 last-exit selector 连续，也不允许把一个无穷且时间不连续的 cutoff 直接插入 local energy inequality。\(\theta=3/4\) 时严格余量消失，故不包含端点。

## 32. 与 R0.74Q 既有 gate 等价：no-gain

signed \(F\)-tail 与非负 \(K\)-tail 之差由一个 \(B_Q\) 控制：

\[
\left|\mathcal S_{N,R}^{F}(\mathcal D)
-\mathcal S_{N,R}^{K}(\mathcal D)\right|
\le B_{Q,R}^M.
\tag{S.217}
\]

因此，对与 \(R\) 及解都无关的固定 \(N_0\)，

\[
\mathcal S_{N_0,R}^{F}(\mathcal D)\lesssim A_R
\Longleftrightarrow
\mathfrak W_{1/2,N_0,R}^{F}(\mathcal D)\lesssim A_R,
\]

\[
\mathcal S_{N_0,R}^{K}(\mathcal D)\lesssim A_R
\Longleftrightarrow
\mathfrak W_{\theta,N_0,R}^{K}(\mathcal D)\lesssim A_R.
\tag{S.218}
\]

这是 Step 9 的精确 no-gain/no-go：证明 last-exit 二次界，就等价于证明已经开放的 best-\(N\) terminal-tail bound，canonical stop 本身没有提供更弱的过渡定理。当 \(\mathcal D=\mathcal T_R\) 时正好是 Q.12；当 \(\mathcal D=I_R\) 时只是更弱的 plateau restriction。

## 33. 量词、相消与 full-history 压力测试

(S.219) 用两个终端状态 \(x(\tau_1)=(1,0)\)、\(x(\tau_2)=(0,1)\) 证明

\[
\sup_\tau\inf_{\#S_\tau\le1}\sum_{k\notin S_\tau}x_k=0,
\qquad
\inf_{\#S\le1}\sup_\tau\sum_{k\notin S}x_k=1.
\]

(S.220) 用 \(F(\tau)=(1,-1)\)、\(N=0\) 证明 forced signed tail 为零，而任意 subset supremum 会挑出正坐标并得到 \(1/2\)；后者破坏了需要保留的 cancellation。

(S.221) 取 \(M>N\) 个同步 completed clocks，\(K_k=F_k=h\)、\(Q_k=0\)。平台终端上

\[
\mathcal S_N(F)=\mathcal S_N(K)=(M-N)H,
\quad
\mathfrak W_{1/2,N}^F={M-N\over2}H,
\quad
\mathfrak W_{\theta,N}^K=(1-\theta)(M-N)H.
\]

这是抽象连续-clock stress test，不是 NSE solution；它严格显示 last exit 不会自动把 \(\ell^1\) tail 变成 \(\ell^2\) payment。另外，若所有 level exit 都发生在某个“recent window”之前，该窗口内根本没有可用 exit；因此 (S.210) 必须保留从 \(s_R\) 到 \(\tau\) 的 full history，除非另有 PDE 定理支付早期段。

## 34. theta=2/3 的兼容性与下一 PDE residual

\(\theta=2/3\) 与 Step 8 的 one-sixth rows 兼容：

\[
\Delta K_{k,2/3}={1\over3}T_k,
\qquad
|\Delta Q_{k,2/3}|<{1\over6}T_k
\Longrightarrow
\Delta F_{k,2/3}>{1\over6}T_k.
\tag{S.222}
\]

这是为下一 PDE 分解选择的兼容参数，不是全局最优化定理。下一真正新的目标是：在删去 Step 7 low-Rayleigh 支、Step 8 \(\mathcal I_\beta\) 与 \(\mathcal I_\sigma\) 两个已付分支后，定义并审计 forced full PDE residual tail；只允许至多 \(N_0\) 个随终端变化的例外，且以 \(\sqrt{N_0}Z_R\) 支付。该 residual 可能仍包含 anomalous defect 或 high-Rayleigh dissipation，本步没有预先定义成有利对象。

## 35. Step 9 主张边界与双路审计

Step 9 **PROVED**：(S.200)--(S.203) 的终端域分离与 best-\(N\) tails；(S.204)--(S.207) 的 signed half-exit 精确表示；(S.208) 的 plateau reduction；(S.209) 的 S.25 失败反例；(S.210)--(S.215) 的 \(K\)-last-exit、尖锐一个 \(B_Q\) 误差与 \(\theta<3/4\) 有限 good-stop closure；(S.216)--(S.218) 的 plateau reduction、\(F/K\) tail comparison 与 no-gain 等价；以及 (S.219)--(S.222) 的量词、相消、平台和 \(\theta=2/3\) 压力测试。

继承的 Step 8 no-exception gate 仍是 **REFUTED**，S.38 条件蕴含仍然 **RETAINED**。canonical last exits 不产生新二次压缩，是 completed-clock algebra 层面的严格 **no-gain/no-go**。

继续 **OPEN**：存在与解和尺度无关的固定 \(N_0\)，使 (S.218) 的任一 best-\(N_0\) PDE tail 获得二次界；删去已付分支后的 residual full tail；(Q.1)、R0.74R extraction hypotheses、scale contraction、prescribed-centre packing 与 regularity。

明确 **NOT CLAIMED**：F-half-exit 满足 S.25；canonical selector 对终端连续；一个无穷 stopped cutoff 可直接作 local-energy test；arbitrary subset supremum 可取代 forced full tail；\(\sup\inf\) 可换成 \(\inf\sup\)；plateau 与 full domain 相等；单个 dominant packet 证明 \(N_0=1\)；标量 stress tests 是 PDE solutions；以及新颖性、优先权、奇点形成或 Clay 结论。

主证书通过 9/9 exact、8/8 finite、57/57 structural 与 18/18 mutations。独立 Ruby 审计通过 12/12 groups、91,396/91,396 finite cases、49/49 structural、21/21 source mutations、15/15 artifact mutations与 6/6 report checks。主文 SHA-256 为 `85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd`。有限证书只支持实现可复现性，不替代 PDE 解析证明。

**CANONICAL BEST-N LAST EXITS: EXACT REPRESENTATIONS, NO NEW QUADRATIC COMPRESSION. NEXT: PDE RESIDUAL TAIL AFTER PAID BRANCHES. NOT CLAY.**

## 36. Step 10 的问题与结论

Step 9 已说明 canonical last exit 只表示 R0.74Q 的 best-\(N\) terminal tail，并不自行压缩它。Step 10 的问题更窄：先删除所有已经被二次 \(Q\)-variation ledger 或 velocity-cubic ledger 支付的壳层，canonical \(2/3\)-last-exit tail 还剩什么？

答案是一个精确六分区。四个 paid classes 合计只需

\[
6B_{Q,R}^M+C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R,
\qquad A_R=(P_R^M)^{2/3},
\]

其中 \(Q\) 行只记一次 \(6B_Q\)，\(\mathcal P_\sigma\) 与 \(\mathcal P_{\rm LE}\) 先合并再做 Hölder，只记一次 \(C_5\) cubic ledger。余下两个 residual mechanisms 是：short non-\(D\)、\(Q\)-small 的 \(\mathcal R_{\rm sh}\)，以及 Step 8 scalar-excess class \(\mathcal R_x=\mathcal I_x\)。二者共享同一个 best-\(N\) exception budget，不能各自删除 \(N\) 个坐标。

本步证明的是 exact reduction。它没有证明存在与解、尺度无关的固定 \(N_0\)，使 residual tail 获得二次界；没有证明 Q.12、Q.1、正则性或 Clay 结论。**NOT CLAY.**

## 37. canonical 2/3-last exit 与固定 profile

保留 periodic suitable-weak Version-M、full clock interval \(\mathcal T_R=(s_R,t_0)\)、plateau interval \(I_R\)、good-time set \(\mathcal G_R\)，以及

\[
A_R=(P_R^M)^{2/3},\qquad
B_{Q,R}^M=\sum_{k\ge1}\operatorname{TV}_{[s_R,t_0)}Q_{k,R}\le C_QA_R,
\qquad
Z_R=\left(\sum_{k\ge1}v_{k,R}^2\right)^{1/2}.
\]

固定 \(\tau\in\mathcal G_R\cap\mathcal T_R\)。若 \(T_k=K_{k,R}(\tau)>0\)，取最后一个 \(K\le2T_k/3\) 的时刻 \(\ell_k\)，并写

\[
\boxed{
\begin{gathered}
\ell_k=\max\{t\in[s_R,\tau]:K_{k,R}(t)\le2T_k/3\},
\quad J_k^{\rm LE}=(\ell_k,\tau),
\quad d_k={\tau-\ell_k\over R^2},\\
0<d_k<4,\quad K_{k,R}(\ell_k)={2T_k\over3},
\quad K_{k,R}(t)>{2T_k\over3}\ (t\in J_k^{\rm LE}),\\
\Delta Q_k=Q_k(\tau)-Q_k(\ell_k),\quad
\Delta F_k=F_k(\tau)-F_k(\ell_k),\\
\Delta K_k={T_k\over3},\qquad
\Delta F_k={T_k\over3}-\Delta Q_k.
\end{gathered}}
\tag{S.223}
\]

若 \(T_k=0\)，令 \(\ell_k=\tau\)、\(d_k=0\)、residual coordinate 为零。\(\ell_k\) 不必是 good time；这里只用 \(K_k\) 连续。

固定正的 deterministic profile \(\boldsymbol\lambda\)，它与 \(R,\tau\) 和解无关，并满足

\[
\boxed{\mathscr L(\boldsymbol\lambda)
=\sum_{k\ge1}2^{3k}\gamma_k\lambda_k^3<\infty.}
\tag{S.224}
\]

在正终端壳层中，按 \(d_k\gtreqless\lambda_k^{-3/2}\)、\(|\Delta Q_k|\gtreqless T_k/6\)、\(D_{k,R}(\tau)\gtreqless T_k/2\) 分出 long/short、\(Q+\)/\(Q-\)、\(D\)/non-\(D\)。等号分别放入 long、absolute-\(Q\)-large 与 \(D\)-dominated 一侧。

## 38. D-first 六分区与 genealogy

Step 8 的 full-history priority partition 保持不变：

\[
\mathcal I_D
=\mathcal I_\beta\mathbin{\dot\cup}\mathcal I_\sigma
\mathbin{\dot\cup}\mathcal I_x.
\]

这里 \(\mathcal I_\beta,\mathcal I_\sigma,\mathcal I_x\) 仍在完整 \(J_\tau=(s_R,\tau)\) 上定义，不能改写成 last-exit interval。按 D-first 优先顺序定义

\[
\boxed{
\begin{aligned}
\mathcal P_\beta&=\mathcal I_\beta,
&\mathcal P_\sigma&=\mathcal I_\sigma,\\
\mathcal P_{\rm LE}&=\mathcal I_{\neg D}\cap\mathcal I_{\rm long},
&\mathcal P_Q&=\mathcal I_{\neg D}\cap\mathcal I_{\rm short}\cap\mathcal I_{Q+},\\
\mathcal R_{\rm sh}&=\mathcal I_{\neg D}\cap\mathcal I_{\rm short}\cap\mathcal I_{Q-},
&\mathcal R_x&=\mathcal I_x,\\
\{k:T_k>0\}
&=\mathcal P_\beta\mathbin{\dot\cup}\mathcal P_\sigma
\mathbin{\dot\cup}\mathcal P_{\rm LE}\mathbin{\dot\cup}\mathcal P_Q
\mathbin{\dot\cup}\mathcal R_{\rm sh}\mathbin{\dot\cup}\mathcal R_x.
\end{aligned}}
\tag{S.225}
\]

\(\mathcal P_Q\) 表示 absolute-\(Q\)-large，不是 \(Q\) 符号为正。Step 7 low-Rayleigh 支不会再生成第七类：

\[
\boxed{
\mathcal I_{\rm lo}\subset\mathcal I_\beta\cup\mathcal I_\sigma,
\qquad
\mathcal I_{\rm lo}\setminus(\mathcal I_\beta\cup\mathcal I_\sigma)=\varnothing,
\qquad
\mathcal I_x=\mathcal I_x\cap(\mathcal I_{\rm def}\cup\mathcal I_{\rm hi}).}
\tag{S.226}
\]

这是 genealogy 与 no-double-charge 结论，不是对 \(\mathcal I_x\) 的新支付；它仍可能来自 anomalous-defect 或 high-Rayleigh 支。

## 39. 一个 Q ledger 与一个 cubic ledger

对 \(\mathcal P_\beta\)，Step 8 给出 \(T_k\le6\beta_k(J_\tau)\)；对 \(\mathcal P_Q\)，定义给出 \(T_k\le6|\Delta Q_k|\)。两类位于互不相交的 \(D\) 与 non-\(D\) shell sets，因此先求和再扩大到完整 variation ledger：

\[
\boxed{
\sum_{k\in\mathcal P_\beta\cup\mathcal P_Q}T_k
\le6\left(\sum_{k\in\mathcal P_\beta}\beta_k(J_\tau)
+\sum_{k\in\mathcal P_Q}|\Delta Q_k|\right)
\le6B_{Q,R}^M\le6C_QA_R.}
\tag{S.227}
\]

正确系数是一个 \(6B_Q\)，不是两个 \(6B_Q\)。

若 \(k\in\mathcal P_{\rm LE}\)，由 \(D_k(t)\le D_k(\tau)<T_k/2\) 与 \(K_k(t)>2T_k/3\)，对 last-exit interval 上几乎处处 good times 有

\[
\boxed{
e_{k,R}(t)>{T_k\over6},\qquad
{1\over R^2}\int_{J_k^{\rm LE}}e_{k,R}(t)^{3/2}\,dt
>d_k\left({T_k\over6}\right)^{3/2}
\ge\lambda_k^{-3/2}\left({T_k\over6}\right)^{3/2}.}
\tag{S.228}
\]

这里没有在可能非 good 的 \(\ell_k\) 取 \(E_k,D_k\) 的值。接上 inherited padded-shell estimate 得到

\[
\boxed{
T_k\le C_{\rm LE}\lambda_k2^k\gamma_k^{1/3}
\bigl(p_{k,R}^{u,\eta}(J_k^{\rm LE})\bigr)^{2/3},
\quad C_{\rm LE}=6C_1^{2/3}<C_4,
\quad C_4=12(2C_1)^{2/3}.}
\tag{S.229}
\]

对 \(\mathcal P_\sigma\) 使用 \(J_\tau\)，对 \(\mathcal P_{\rm LE}\) 使用各自的 \(J_k^{\rm LE}\)，在并集上先做 finite-shell Hölder，再只调用一次允许 shell-dependent time sets 的 (R.211)，得到

\[
\boxed{
\sum_{k\in\mathcal P_\sigma\cup\mathcal P_{\rm LE}}T_k
\le C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R,
\qquad C_5=C_4C_P^{2/3}.}
\tag{S.230}
\]

把两支各自估成完整全局 ledger 会多收一次 \(C_5\)，本步不这样做。

## 40. residual vector 与尖锐比较

记四个 paid classes 的并为 \(\mathcal I_{\rm pay}\)，两个 residual classes 的并为 \(\mathcal I_{\rm res}=\mathcal R_{\rm sh}\cup\mathcal R_x\)。已有

\[
\boxed{
\sum_{k\in\mathcal I_{\rm pay}(\tau)}T_k
\le6B_{Q,R}^M+C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
\le C_{\rm pay}(\boldsymbol\lambda)A_R,
\quad C_{\rm pay}=6C_Q+C_5\mathscr L(\boldsymbol\lambda)^{1/3}.}
\tag{S.231}
\]

定义 residual stopped-flux vector

\[
\boxed{
r_{k,R}^{\boldsymbol\lambda}(\tau)
=1_{\mathcal I_{\rm res}(\tau)}(k)
\bigl[F_{k,R}(\tau)-F_{k,R}(\ell_k)\bigr],
\qquad r_k=0\ \text{if }T_k=0.}
\tag{S.232}
\]

在 \(\mathcal R_{\rm sh}\) 上，\(|\Delta Q_k|<T_k/6\) 来自定义；在 \(\mathcal R_x=\mathcal I_x\) 上，失败的 Step 8 \(\beta\)-test 给出同样严格界。配合 \(\Delta F=T/3-\Delta Q\)，两个 residual classes 都满足

\[
\boxed{
{T_k\over6}<r_{k,R}^{\boldsymbol\lambda}(\tau)<{T_k\over2},
\qquad
2r_{k,R}^{\boldsymbol\lambda}(\tau)<T_k<6r_{k,R}^{\boldsymbol\lambda}(\tau).}
\tag{S.233}
\]

全局补零后，

\[
\boxed{
0\le r_{k,R}^{\boldsymbol\lambda}(\tau)\le{T_k\over2}\le{v_{k,R}\over2},
\quad
\|r_R^{\boldsymbol\lambda}(\tau)\|_{\ell^2}\le{Z_R\over2},
\quad
\sum_kr_{k,R}^{\boldsymbol\lambda}(\tau)\le C_FP_R^M.}
\tag{S.234}
\]

\(\ell^2\) 上界本身不能推出 fixed-\(N\) 的 \(\ell^1\) tail bound；最后一项在大 \(P_R^M\) 区域也只有线性尺度。

## 41. paid-branch deletion 的 best-N reduction

对非负 \(\ell^1\) vector 定义

\[
\mathcal S_N(x)=\inf_{S\subset\mathbb N,\#S\le N}\sum_{k\notin S}x_k.
\]

对每一个同样的 exceptional set \(S\)，四个 paid classes 与 residual comparison 给出

\[
\boxed{
\sum_{k\notin S}T_k
\le6B_{Q,R}^M+C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
+6\sum_{k\notin S}r_{k,R}^{\boldsymbol\lambda}(\tau).}
\tag{S.235}
\]

用逼近 residual infimum 的同一批集合取极限，得到 fixed-good-terminal theorem

\[
\boxed{
\mathcal S_N((K_{k,R}(\tau))_k)
\le6B_{Q,R}^M+C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
+6\mathcal S_N((r_{k,R}^{\boldsymbol\lambda}(\tau))_k).}
\tag{S.236}
\]

\(\mathcal R_x\) 与 \(\mathcal R_{\rm sh}\) 必须先合并再只做一次 best-\(N\) infimum；分别允许 \(N\) 个例外会悄悄把总预算增至 \(2N\)。

对 \(\mathcal D\in\{I_R,\mathcal T_R\}\) 定义 good-terminal residual gate

\[
\boxed{
\mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)
=\sup_{\tau\in\mathcal D\cap\mathcal G_R}
\mathcal S_N((r_{k,R}^{\boldsymbol\lambda}(\tau))_k).}
\tag{S.237}
\]

只用 terminal \(K\)-vector 的 inherited \(\ell^1\)-continuity，把左侧从 dense good times 延伸到所有 terminal times；不使用 residual path、selector 或 masks 的连续性：

\[
\boxed{
\mathcal S_{N,R}^{K}(\mathcal D)
\le C_{\rm pay}(\boldsymbol\lambda)A_R
+6\mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D).}
\tag{S.238}
\]

反向由 coordinatewise \(r\le K/2\) 与同一 exceptional set 得到

\[
\boxed{
\mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)
\le{1\over2}\mathcal S_{N,R}^{K}(\mathcal D).}
\tag{S.239}
\]

因此对固定、与尺度和解无关的 \(N_0\)，

\[
\boxed{
\mathfrak R_{N_0,R}^{\boldsymbol\lambda}(\mathcal D)\lesssim A_R
\quad\Longleftrightarrow\quad
\mathcal S_{N_0,R}^{K}(\mathcal D)\lesssim A_R.}
\tag{S.240}
\]

这个等价移除了已知付款，但没有把 residual gate 变成定理；它准确标出还需要新 PDE 信息的位置。

## 42. plateau corollary、full gate 与 fallback

把 inherited plateau reduction 与 (S.238) 合并：

\[
\boxed{
\mathfrak C_R^M
\le\sqrt N\,Z_R+7B_{Q,R}^M
+C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
+6\mathfrak R_{N,R}^{\boldsymbol\lambda}(I_R).}
\tag{S.241}
\]

七个 \(B_Q\) units 中，六个来自 paid partition，一个来自 terminal \(K\)-to-flux reduction。该式只在 plateau 域，不是 full-terminal Q.12。

绝对 \(F\)-variation 给出线性 fallback：

\[
\boxed{
\mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)\le C_FP_R^M,
\qquad
P_R^M\le1\Longrightarrow
\mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)\le C_FA_R.}
\tag{S.242}
\]

因此 small-payment regime 已经闭合；当 \(P_R^M>1\) 时，线性 fallback 与目标之间仍差 \((P_R^M)^{1/3}\)。真正开放的 full-domain statement 是

\[
\boxed{
\text{OPEN: 存在固定 }N_0<\infty,C_{\rm res}<\infty,
\text{ 使 }
\mathfrak R_{N_0,R}^{\boldsymbol\lambda}(\mathcal T_R)
\le C_{\rm res}A_R
\text{ 对所有 }R\text{ 与解一致成立}.}
\tag{S.243}
\]

若 (S.243) 成立，则 (S.238) 推出 full Q.12，再由 inherited Q.9 推出 Q.1。只在 \(I_R\) 证明 residual bound 能直接给 plateau Q.1，但不能升级成 full Q.12。

## 43. sharpness、exception budget 与 D-persistence no-go

在 abstract continuous-clock 层面，取 \(T=1\)、\(0<\varepsilon<1/6\)，并令

\[
\boxed{
\Delta Q={1\over6}-\varepsilon
\Longrightarrow r={1\over6}+\varepsilon,
\qquad
\Delta Q=-{1\over6}+\varepsilon
\Longrightarrow r={1\over2}-\varepsilon.}
\tag{S.244}
\]

因此仅凭 \(|\Delta Q|<T/6\)，系数六与上界二分之一都是 limiting-sharp；等号 \(|\Delta Q|=T/6\) 已归入 paid \(\mathcal P_Q\)。这些是 clock-algebra tests，不是 NSE solutions。

一份共享 exception budget 的必要性由 \(T_1=T_2=3\)、\(r_1=r_2=1\) 给出：

\[
\boxed{
\mathcal S_1((r_1,r_2))=1,
\qquad
\mathcal S_1((r_1,0))+\mathcal S_1((0,r_2))=0.}
\tag{S.245}
\]

右式违法之处是给两个 residual labels 各花一个例外。固定 \(N\) 也不能被 truncation-dependent budget 替代：

\[
\boxed{
T_k=2^{-k}:\quad
\mathcal S_1((T_k)_{k\ge1})={1\over2},
\quad
\mathcal S_1((T_k)_{1\le k\le M})={1\over2}-2^{-M},
\quad
\mathcal S_M((T_k)_{1\le k\le M})=0.}
\tag{S.246}
\]

最后，terminal \(D\)-dominance 不能免费局部化成 last-exit persistence。显式 rational piecewise-linear clock 取 \(R^2=1,s_R=0,\tau=2,T=1\)，last exit \(\ell=1/4\)，并安排 \(D(t)=3/5\) 在后段保持不变；则

\[
\boxed{
D(\tau)={3T\over5}\ge{T\over2},
\qquad
\Delta D|_{(\ell,\tau)}=0,
\qquad
E(1)={7T\over100}<{T\over6}.}
\tag{S.247}
\]

这严格排除把 \(\mathcal I_D\) 直接塞入 long non-\(D\) persistence proof；Step 8 full-history trichotomy 必须保留。该 witness 仍只是 continuous clock stress test。

## 44. 路线决定

paid-branch deletion 已达到它的自然终点。下一 PDE 阶段应分别研究两类 residual mechanism，但最终必须用一个共享 exception budget 重组：

- **short non-D、Q-small packing**：正 stopped flux 与 \(T_k\) 可比，却生成在短于 \(R^2\lambda_k^{-3/2}\) 的 terminal interval。新定理必须使用 spatial crowding、overlap 或 Carleson-type constraint 等跨壳层 PDE 信息；普通 \(\ell^2\) sequence inequality 不足以闭合。
- **scalar-excess ancestry**：\(\mathcal I_x\) 只可能来自 anomalous-defect 或 high-Rayleigh shells，且 full-history \(Q\)-variation 与 kinetic mass 都低于 Step 8 thresholds。需要真正打包剩余 defect/high-Rayleigh mass；terminal \(D\)-dominance 不能免费变成 last-exit interval 内的支付。

任何候选估计都必须通过 (S.245)--(S.247)，并保留 inherited R0.74O/P exact family 的边界：该精确族只 refute no-exception gate，不证明 \(N_0=1\) 足够。

## 45. Step 10 主张边界与双路审计

Step 10 **PROVED**：(S.223)--(S.224) 的 canonical \(2/3\)-last-exit 与固定 profile；(S.225) 的 exact six-class partition；(S.226) 的 Step 7/8 compatibility；(S.227)--(S.231) 的 single \(6B_Q\) 与 single \(C_5\) payments；(S.232)--(S.234) 的 positive residual 与 \(T/6<r<T/2\)；(S.235)--(S.240) 的 fixed-good-terminal/domain-safe best-\(N\) reductions；以及 (S.241)--(S.242) 的 plateau corollary 与 small-payment fallback。

Step 10 **INHERITED**：R0.74P canonical clocks、variation ledgers 与 \(\ell^1\)-terminal continuity；R0.74Q fixed-\(N\) reduction；R0.74R shell-dependent cubic payment；Step 7 Rayleigh trichotomy；Step 8 full-history \(\beta/\sigma/x\) partition；Step 9 last-exit identity 与 finite good-stop closure。

Step 10 **REFUTED / RULED OUT**：额外 low-Rayleigh residual class；必须重复收取完整 \(Q\) 或 cubic ledger；两个 residual mechanisms 分别拥有 \(N\) 个 exceptions；terminal \(D\)-dominance 自动局部化到 last-exit interval；以及 last-exit algebra 单独产生 fixed-\(N\) shell compression。

继续 **OPEN**：固定、与解和尺度无关的 \(N_0\) residual estimate (S.243)；\(\mathcal R_{\rm sh}\) 与 \(\mathcal R_x\) 的 PDE packing；full Q.12、Q.1、R0.74R extraction hypotheses、scale contraction、prescribed-centre packing 与 regularity。

明确 **NOT CLAIMED**：last-exit selector、branch masks 或 residual path 对终端连续/可测/lower semicontinuous；\(\ell_k\) 是 good time；无穷 last-exit family 是一个 admissible local-energy test；Step 8 classes 可在 \(J_k^{\rm LE}\) 重定义；plateau 与 full domain 相等；\(\boldsymbol\lambda\) 已优化；scalar fixtures 是 NSE solutions；以及新颖性、优先权、奇点形成、正则性或 Clay 结论。

主证书通过 12/12 exact、10/10 finite、79/79 structural 与 47/47 negative mutations。独立 Ruby 通过 9/9 groups、65,681 cases、21/21 contract mutations、13/13 report checks 与 15/15 audit bindings；deterministic stdout SHA-256 为 `4877dc3a0de2c2f605641736c7355672f0a7a68cb97a37849d4a7c28495e8bbd`。主文 SHA-256 为 `9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c`。有限证书不替代 inherited local-energy/PDE analysis。

**PAID BRANCHES: DELETED WITH ONE Q LEDGER AND ONE CUBIC LEDGER. TWO RESIDUAL MECHANISMS SHARE ONE BEST-N GATE. S.243 OPEN. NOT CLAY.**

## 46. Step 11 的问题与四项结论

Step 10 已把 full-terminal clock estimate 归约为两个不交 residual mechanisms 上的一个 combined best-\(N\) tail。Step 11 不证明这个 tail estimate，而是确定两支怎样精确重组、各自现有估计能走到哪里，以及哪一条新的 PDE 陈述足以闭合 short branch。

- combined residual 是两支 best-\(N\) tails 的精确离散 infimal convolution。两支可以分别研究，但 exception counts 必须相加；两个固定有限 count 仍足以满足最终“存在某个固定 \(N_0\)”的目标。
- short non-\(D\) branch 得到尖锐 inverse-duration coefficient、nested-tent integral 与任意正 backward depth 的控制；depth zero 的 terminal trace 仍缺失，critical \(s^2\) Carleson endpoint 有 logarithmic divergence。
- scalar-excess branch 上，stopped residual 与 Step 8 priority-selected excess 在 best-\(N\) 意义下以字面常数 \(1/5\) 与 \(3\) 等价。现有理论只有 linear summability 与 fixed-solution tightness，没有 solution- and scale-independent count。
- 现有 smooth exact families 只 refute zero-exception route。当前 multi-packet designs 的 cubic cost 过大，不能 refute 任意固定正 exception count。

因此 short branch 的缺口是 terminal anti-concentration，不是 interval overlap；excess branch 的缺口是 uniform weighted packing，不是 ancestry classification。两条都 **OPEN**。无新颖性、优先权、奇点、正则性或千禧年问题结论。**NOT CLAY.**

## 47. 两个 residual vectors 与共享 budget 恒等式

保留 Step 10 的全部定义。固定 good terminal \(\tau\)，令 \(T_k=K_{k,R}(\tau)\)、\(\ell_k=\ell^K_{k,2/3}(\tau)\)、\(d_k=(\tau-\ell_k)/R^2\)，并把 residual 拆成不交支撑的两向量

\[
\boxed{
r_k^{\rm sh}(\tau):=\mathbf1_{\mathcal R_{\rm sh}(\tau)}r_k(\tau),
\qquad
r_k^x(\tau):=\mathbf1_{\mathcal R_x(\tau)}r_k(\tau),
\qquad r=r^{\rm sh}+r^x.}
\tag{S.248}
\]

两支上都有 \(T_k/6<r_k<T_k/2\le v_{k,R}/2\)。对 \(z\in\ell^1_+\) 写
\(\mathcal S_N(z)=\inf_{\#S\le N}\sum_{k\notin S}z_k\)。若 \(a,b\) 支撑不交，则

\[
\boxed{
\mathcal S_N(a+b)=\min_{0\le n\le N}
\left[\mathcal S_n(a)+\mathcal S_{N-n}(b)\right].}
\tag{S.249}
\]

这是 pointwise equality。取 terminal supremum 后只有 domain-safe inequality：

\[
\boxed{
\mathfrak R_{N,R}^{\boldsymbol\lambda}(\mathcal D)
\le\min_{0\le n\le N}
\left[\mathfrak R^{\rm sh}_{n,R}(\mathcal D)
+\mathfrak R^x_{N-n,R}(\mathcal D)\right].}
\tag{S.250}
\]

这里通常不能写等号，因为 supremum 与 finite minimum 不交换；最优 budget split 与 top-\(N\) shells 可以依赖 \(\tau\)。若两支分别以固定 \(N_{\rm sh},N_x\) 闭合，令 \(N_0=N_{\rm sh}+N_x\)，则

\[
\boxed{
\begin{gathered}
\mathfrak R_{N_0,R}^{\boldsymbol\lambda}\le(C_{\rm sh}+C_x)A_R,\\
\mathcal S^K_{N_0,R}\le
\left[6C_Q+C_5\mathscr L(\boldsymbol\lambda)^{1/3}
+6C_{\rm sh}+6C_x\right]A_R.
\end{gathered}}
\tag{S.251}
\]

两个 best-\(N\) branch theorems 给出 combined best-\(2N\)，不是 best-\(N\)。fixture \(a=(M,0),b=(0,M)\) 给出

\[
\boxed{
\mathcal S_1(a)=\mathcal S_1(b)=0,
\qquad \mathcal S_1(a+b)=M,
\qquad \mathcal S_2(a+b)=0.}
\tag{S.252}
\]

它精确说明 duplicate \(N\)-budgets 会偷偷把总预算加倍。

## 48. Short branch 的 inverse-duration ledger

令 \(\mathcal H_\tau=\mathcal R_{\rm sh}(\tau)\)、\(a_k=2^{3k}\gamma_k\)、\(p_k=p_{k,R}^{u,\eta}(J_k^{\rm LE})\)。non-\(D\) persistence 与继承的 cubic estimate 给出

\[
\boxed{
d_k\left({T_k\over6}\right)^{3/2}<C_1a_k^{1/2}p_k,
\qquad
r_k^{\rm sh}<3C_1^{2/3}(a_kd_k^{-2})^{1/3}p_k^{2/3}.}
\tag{S.253}
\]

对同一个 exceptional set 做 finite-shell Hölder，再只调用一次 shell-dependent-time-set estimate，得到

\[
\boxed{
\mathcal S_N(r^{\rm sh}(\tau))
\le3C_1^{2/3}C_P^{2/3}
\bigl(\mathfrak D_N^{\rm sh}(\tau)\bigr)^{1/3}A_R,
\quad
\mathfrak D_N^{\rm sh}:=
\inf_{\#S\le N}\sum_{k\in\mathcal H_\tau\setminus S}a_kd_k^{-2}.}
\tag{S.254}
\]

这只是 sufficient interface，不是对 \(\mathfrak D_N^{\rm sh}\) 的新估计；它把遗留债务精确定位为 inverse-square duration。

## 49. Normalized depth 与 critical Carleson log gap

在 short branch 定义 \(h_k=d_k\lambda_k^{3/2}\in(0,1)\)、\(w_k=a_k\lambda_k^3\)。令 \(\mathcal H_j=\{2^{-j-1}\le h_k<2^{-j}\}\)、\(W_j=\sum_{k\in\mathcal H_j}w_k\)，则

\[
\boxed{
w_kh_k^{-2}=a_kd_k^{-2},
\qquad
\sum_j4^jW_j\le\sum_kw_kh_k^{-2}\le4\sum_j4^jW_j.}
\tag{S.255}
\]

对原子测度 \(\mu_\tau=\sum_{k\in\mathcal H_\tau}w_k\delta_{h_k}\)，Tonelli 给出精确 layer-cake：

\[
\boxed{
\sum_kw_kh_k^{-2}
=\mu_\tau((0,1))+2\int_0^1s^{-3}\mu_\tau((0,s])\,ds.}
\tag{S.256}
\]

因此 \(\mu_\tau((0,s])\lesssim s^{2+\varepsilon}\) 足够，但 critical exponent two 不足。取固定 profile \(\lambda_k=1\)、\(w_k=2^{3k}\gamma_k\)、\(h_k=w_k^{1/2}\)，可有 \(\mu((0,s])\le2s^2\)，同时

\[
\boxed{
\sum_{k\ge k_0}w_kh_k^{-2}=\sum_{k\ge k_0}1=\infty.}
\tag{S.257}
\]

这就是 critical \(s^2\) Carleson endpoint 的 logarithmic obstruction。它是 coefficient/clock stress test，**不是 NSE solution**。

## 50. Nested tent 能控制什么、不能控制什么

以 backward time \(s=(\tau-t)/R^2\) 定义
\(M_I(s)=\sum_{k\in I,d_k>s}r_k^{\rm sh}\)、
\(V_I(s)=\sum_{k\in I,d_k>s}a_k\)。所有 last-exit intervals 共用 terminal endpoint，故其 indicator 精确为 \(\mathbf1_{\{s<d_k\}}\)。weighted Hölder、(R.214) 与 (R.211) 给出

\[
\boxed{
\int_0^4{M_I(s)^{3/2}\over V_I(s)^{1/2}}\,ds
\le3^{3/2}C_1C_PP_R^M.}
\tag{S.258}
\]

令 \(\mathscr A_0=\sum_k2^{3k}\gamma_k<\infty\)。对任意 \(0<\delta<4\)，

\[
\boxed{
\sum_{k\in I,\ d_k>\delta}r_k^{\rm sh}
\le3C_1^{2/3}C_P^{2/3}\mathscr A_0^{1/3}
\delta^{-2/3}A_R.}
\tag{S.259}
\]

所以任何持续到固定正 backward depth 的 residual 已经得到 quadratic control；未解决的全部质量可以集中到 \(d_k\downarrow0\)。一个 \(L^{3/2}\)-in-time tent bound 没有 depth-zero terminal trace。

严格嵌套本身也无能为力：连续 clock/payment tower 可同时满足 nested intervals 与很小 cubic integral，却有

\[
\boxed{
\mathcal S_N(r)=M-N,
\qquad A_M\asymp M^{2/3},
\qquad Z_M=3\sqrt M.}
\tag{S.260}
\]

这是 abstract continuous clock/payment witness，**不是 NSE counterexample**。

## 51. Short branch 的第一个新 PDE 门槛

比 raw inverse-duration moment 更自然的目标是 amplitude-sensitive terminal anti-concentration：寻找与解和尺度无关的固定 \(N_{\rm sh}\)、\(0<\delta_*<4\)、\(0\le\theta_*<1\)、\(C_{\rm nc}<\infty\)，使每个 good terminal 都存在同一个 \(S_\tau\)、\(\#S_\tau\le N_{\rm sh}\)，满足

\[
\boxed{
\sum_{k\in\mathcal H_\tau\setminus S_\tau,\ d_k\le\delta_*}
r_k^{\rm sh}
\le\theta_*
\sum_{k\in\mathcal H_\tau\setminus S_\tau}r_k^{\rm sh}
+C_{\rm nc}A_R.
\quad\textbf{OPEN}}
\tag{S.261}
\]

(S.261) 与 (S.259) 的 implication 已证明：它将闭合 short branch。boxed hypothesis 本身没有证明；它要求 PDE 排除一个非二次比例的 tail 完全在最后 \(\delta_*R^2\) 时间内生成。

## 52. Scalar excess 与 residual 的精确 best-N 等价

保留 Step 8 scalar excess
\(x_k=[D_{k,R}(\tau)-\beta_{k,R}(J_\tau)-2\lambda_k\sigma_{k,R}(J_\tau)]_+\)，并令 \(x_k^{\rm sel}=\mathbf1_{\mathcal I_x}x_k\)。priority failures 与 terminal clock identity 给出字面坐标比较

\[
\boxed{
{1\over5}x_k^{\rm sel}<r_k^x<3x_k^{\rm sel}
\qquad(k\in\mathcal I_x).}
\tag{S.262}
\]

常数在 scalar constraints 层面尖锐。优化同一个 exceptional set 后，

\[
\boxed{
{1\over5}\mathcal S_N(x^{\rm sel}(\tau))
\le\mathcal S_N(r^x(\tau))
\le3\mathcal S_N(x^{\rm sel}(\tau)).}
\tag{S.263}
\]

因此 \(\mathcal R_x\) gate 已精确归约，但没有闭合。

## 53. Fixed-solution tightness 不等于 uniform \(N\)

Step 8 ancestor vector \(b_k=\mathbf1_{\mathcal I_x}[m_{k,R}+\int_{H_{k,R}}g_{k,R}]\) 满足

\[
\boxed{
r_k^x\le3x_k^{\rm sel}\le3b_k,
\qquad
\sum_kx_k^{\rm sel}\le CP_R^M,
\qquad
\sum_kb_k\le C(A_R+P_R^M).}
\tag{S.264}
\]

这些在 \(P_R^M>1\) 时只是 linear ledger，Markov counting 不能产生 universal quadratic best-\(N\) tail。另一方面，因 \(r_k^x\le v_{k,R}/2\) 且 \(v_R\in\ell^1\)，对每个固定 solution、固定 \(R\) 和 \(\varepsilon>0\)，可以选取依赖于它们的 \(N=N(u,R,\varepsilon)\)，使

\[
\boxed{
\sup_{\tau\in\mathcal G_R\cap\mathcal D}
\mathcal S_N(r^x(\tau))
\le{1\over2}\sum_{k>N}v_{k,R}<\varepsilon.}
\tag{S.265}
\]

这是真实的 nonuniform compactness，但缺失的恰恰是与 solution、scale 无关的 uniform \(N\) 与 \(O(A_R)\) rate；两者不能混同。

## 54. Ancestry 不能倒推到 last-exit interval

两个 exact rational scalar clocks 表明禁止的 shortcut。pure-defect row 满足

\[
\boxed{
\ell=1,
\quad r^x={1\over3},
\quad \sigma={959\over12000}<{1\over12},
\quad x={2641\over6000}>{1\over6},
\quad D(2)-D(\ell)=0.}
\tag{S.266}
\]

pure high-Rayleigh row 满足

\[
\boxed{
\ell=1,
\quad r^x={1\over3},
\quad \sigma={983\over12000}<{1\over12},
\quad x={2617\over6000}>{1\over6},
\quad \int_{H\cap J^{\rm LE}}g=0.}
\tag{S.267}
\]

两者都说明 full-history ancestry 不能 retrospectively restricted to \(J^{\rm LE}\)。重复 pure-defect row 得到

\[
\boxed{
\mathcal S_N(r^x)={(M-N)_+\over3},
\qquad A_M\asymp M^{2/3},
\qquad Z_M=\sqrt M.}
\tag{S.268}
\]

(S.266)--(S.268) 都是 **ABSTRACT STRESS TESTS, NOT NSE COUNTEREXAMPLES**；它们排除只靠 scalar \(\ell^1/\ell^2\) ledgers 的推导，不否定 (S.243)。exact minimal target 是

\[
\boxed{
\textbf{OPEN:}\quad
\exists N_x,C_x<\infty\ \text{uniformly such that}
\mathcal S_{N_x}(x^{\rm sel}(\tau))\le C_xA_R.}
\tag{S.269}
\]

由 (S.263)，这与 \(\mathcal R_x\) residual gate 在字面常数范围内等价。

## 55. Exact-family falsification criterion

若要 refute 某个固定 \(N\)，新的 smooth exact family 必须提供 \(N+1\) 个不同 target shells，且

\[
\boxed{
\min_{1\le i\le N+1}{K_{k_i,R}(\tau)\over A_R}
\longrightarrow\infty.}
\tag{S.270}
\]

Step 10 将迫使这些 target shells 最终全部落入 combined residual，于是 \(\mathcal S_N(r)/A_R\to\infty\)。现有 R0.74O/P single-packet family 只对 \(N=0\) 通过此检验：一个正 exception 可以删除唯一大坐标。

现有 common-shear multi-packet construction 虽能制造 distinct terminal lobes，却同时证明 exterior cubic lower bound

\[
\boxed{
{A_R^{(N)}\over NT}
\ge {c\over N}R^{2/3}L_N^{-1/3}
\exp\left({5\over6}c_\gamma L_N^2\right)
\longrightarrow\infty.}
\tag{S.271}
\]

所以其 clock lower scale 被 nonnegative cubic payment 压倒；它没有建立 (S.270)，也没有 refute fixed positive exception count。这是对现有设计的 quantitative obstruction，不是对全部 multi-packet architectures 的 no-go。

## 56. 合并后的开放定理

下一 PDE 阶段保留两个工作包：short terminal trace 检验 (S.261)；selected-excess packing 检验 (S.269)，并分开 anomalous measure 与 high-Rayleigh viscous mass。任何 adversarial exact family 先通过 (S.270)，不能只展示多个 terminal lobes。

最终 combined theorem 写成

\[
\boxed{
\begin{gathered}
\textbf{OPEN: find fixed }N_{\rm sh},N_x\in\mathbb N_0
\textbf{ and }C_{\rm sh},C_x<\infty\textbf{ such that}\\
\sup_{\tau\in\mathcal T_R\cap\mathcal G_R}
\mathcal S_{N_{\rm sh}}(r^{\rm sh}(\tau))\le C_{\rm sh}A_R,\\
\sup_{\tau\in\mathcal T_R\cap\mathcal G_R}
\mathcal S_{N_x}(r^x(\tau))\le C_xA_R.
\end{gathered}}
\tag{S.272}
\]

若 (S.272) 成立，(S.251) 以 \(N_0=N_{\rm sh}+N_x\) 推出 Step 10 (S.243)，继而条件性推出 R0.74Q (Q.12) 与 fixed-scale (Q.1)。implication 已证明，antecedent 仍 **OPEN**。

## 57. Step 11 主张边界与双路审计

Step 11 **PROVED**：(S.249)--(S.251) shared-budget identity 与 domain consequence；(S.253)--(S.254) inverse-duration estimate；(S.255)--(S.256) normalized-depth/dyadic/layer-cake identities；(S.257) coefficient-level critical Carleson failure；(S.258)--(S.259) nested-tent 与 positive-depth estimates；(S.262)--(S.263) scalar-excess/residual equivalence；(S.264)--(S.265) ancestry、linear ledger 与 fixed-solution compactness；以及从 (S.261)、(S.269)、(S.270)、(S.272) 出发的 conditional implications。

Step 11 **ABSTRACT STRESS TESTS, NOT NSE COUNTEREXAMPLES**：(S.252) duplicate-budget fixture；(S.257)、(S.260) critical Carleson sequence 与 nested tower；(S.266)--(S.267) ancestry-localization witnesses；(S.268) flat selected-excess tower。

Step 11 **OPEN**：terminal anti-concentration (S.261)；uniform selected-excess packing (S.269)；(S.272) 的两支估计；固定 universal \(N_0\)；Step 10 (S.243)、Q.12、Q.1、scale contraction、prescribed-centre packing 与 regularity；以及能通过 (S.270) 且没有 prohibitive full payment 的新 exact multi-packet family。

明确 **NOT CLAIMED**：moving masks、last-exit selectors、top-\(N\) sets 或 adaptive budget split 的连续性/可测性；terminal supremum 与 branch-budget minimum 交换；CKN-type singular-set estimates 对当前 shell residuals 计数；terminal ancestry 在 last-exit interval 持续；bounded literature search 穷尽；新颖性、优先权；或 Navier--Stokes Millennium problem 的解。

主证书通过 14/14 exact、7/7 finite、34/34 structural 与 7/7 negative mutations。独立 Ruby audit 通过 7/7 groups、206,891 cases、6/6 artifact locks、7/7 dependency locks 与 59/59 note checks；canonical stdout SHA-256 为 `506440647a0a9b5be9d65ded24762b6eb6f6ce8cf054473a0ac04bf8835a1ffb`。这些有限证书只支持实现可复现性，不替代 inherited local-energy/PDE analysis。

**SHARED BUDGET: EXACT. SHORT TERMINAL TRACE: OPEN. SELECTED-EXCESS PACKING: OPEN. EXISTING MULTI-PACKET FAMILIES DO NOT REFUTE FIXED POSITIVE N. NOT CLAY.**

## 58. Step 12：终端公共窗口与 conditional Morrey packing

Step 11 把 full-terminal clock estimate 归约为两个 best-\(N\) tail：short non-dissipation residual \(r^{\rm sh}\) 与 selected dissipation excess \(x^{\rm sel}\)（等价地 \(r^x\)）。Step 12 没有证明这两个 universal tail estimate，而是把它们改写成更清晰的 PDE 接口，并证明一个带附加统一假设的 conditional packing theorem。

本步得到六项结论：short residual 可由一个共同终端窗内的 absolute shell-flux variation 与已证明的 positive-depth cubic term 控制；该新窗口泛函对 terminal 连续，但固定解的模量不对解与尺度统一；best-\(N\) 的 exact layer-cake identity 把问题变成所有阈值上的 shell counting；selected excess 的 anomalous-defect 与 high-Rayleigh ancestors 必须诚实相加 exception budgets；若 total local dissipation 具有统一 critical Morrey coefficient，且 lifted mollified path 的长度以 \(R\) 为单位一致有界，则 moving-tube covering 给出 conditional Morrey packing；最后，单个 inherited passive packet 的统一加速受到 kinematic screen，并不能绕过 cubic obstruction。

**OPEN**：S.280、S.288、S.303、Step 11 的 S.272、Q.12、Q.1、scale contraction、regularity 与 singularity。conditional Morrey 与 mixed-norm 结论的常数依赖其额外统一上界；不声称 novelty 或 priority。无 DNS、无 floating-point asymptotics、无 DGX。**NOT CLAY.**

## 59. 冻结设置与公共终端窗

保留 R0.74S Steps 10--11 的全部定义：

\[
 \mathcal T_R=(s_R,t_0),\qquad |\mathcal T_R|=4R^2,
 \qquad A_R=(P_R^M)^{2/3},
\]

并对每个 \(\tau\in\mathcal G_R\cap\mathcal T_R\) 保留 \(r_k^{\rm sh}\)、\(d_k=(\tau-\ell_k)/R^2\) 以及 inherited absolute flux ledger

\[
 \sum_{k\ge1}\int_{\mathcal T_R}|\dot F_{k,R}(t)|\,dt
 \le \mathfrak L_{{\rm abs},R}^M\le C_FP_R^M.
\]

把 \(|\dot F_{k,R}|\) 在 \(\mathcal T_R\) 外延为零。对 \(0<\delta<4\)，定义

\[
 \boxed{
 \begin{aligned}
 J_{\tau,\delta}&=(\max\{s_R,\tau-\delta R^2\},\tau),\\
 f_{k,R}(\tau,\delta)&=\int_{J_{\tau,\delta}}|\dot F_{k,R}(t)|\,dt,\\
 \mathcal V^F_{N,R}(\tau,\delta)&=\mathcal S_N((f_{k,R}(\tau,\delta))_{k\ge1}).
 \end{aligned}}
\tag{S.273}
\]

这里用一个共同 shell deletion set 处理整段 window；不能在积分内部随时间改变。

## 60. Exact terminal variation-window reduction

若 \(k\in\mathcal R_{\rm sh}(\tau)\) 且 \(d_k\le\delta\)，则 \(J_k^{\rm LE}\subset J_{\tau,\delta}\)。因此对每个 \(S\subset\mathbb N\)，

\[
 \boxed{
 \sum_{\substack{k\in\mathcal R_{\rm sh}(\tau)\setminus S\\d_k\le\delta}}
 r_k^{\rm sh}(\tau)
 \le\sum_{k\notin S}f_{k,R}(\tau,\delta).}
\tag{S.274}
\]

其余 \(d_k>\delta\) 的坐标由 Step 11 (S.259) 以同一个 \(S\) 控制，故

\[
 \boxed{
 \mathcal S_N(r^{\rm sh}(\tau))
 \le \mathcal V^F_{N,R}(\tau,\delta)
 +C_{\rm deep}\delta^{-2/3}A_R,
 \quad C_{\rm deep}=3C_1^{2/3}C_P^{2/3}\mathscr A_0^{1/3}.}
\tag{S.275}
\]

这个结构性增益把 last-exit selectors 与 branch masks 从新项中移除，改为固定窗口上的连续泛函。

## 61. 终端连续性与缺失的 uniform modulus

令 \(g_R(t)=\sum_k|\dot F_{k,R}(t)|\in L^1(\mathcal T_R)\)。当 \(\tau_n\to\tau\) 时，

\[
 \begin{aligned}
 \|f_R(\tau_n,\delta)-f_R(\tau,\delta)\|_{\ell^1}
 &\le\int_{J_{\tau_n,\delta}\triangle J_{\tau,\delta}}g_R(t)\,dt\to0,\\
 |\mathcal S_N(a)-\mathcal S_N(b)|&\le\|a-b\|_{\ell^1}.
 \end{aligned}
\tag{S.276}
\]

所以 \(\tau\mapsto\mathcal V^F_{N,R}(\tau,\delta)\) 连续，good terminals 上的 supremum 等于全 \(\mathcal T_R\) 上的 supremum。对每个固定 \((u,R)\)，Lebesgue integral 的 absolute continuity 还给出

\[
 \boxed{
 \Omega_{u,R}(\delta):=
 \sup_{\tau\in\mathcal T_R}\sum_kf_{k,R}(\tau,\delta)
 \longrightarrow0\qquad(\delta\downarrow0).}
\tag{S.277}
\]

但这个 modulus 依赖 solution 与 scale，且 S.275 的 positive-depth term 同时按 \(\delta^{-2/3}A_R\) 增长，因此不能据此得到 universal estimate。

## 62. Layer cake：精确的 all-threshold counting problem

对 \(z\in\ell^1_+\) 定义 \(n_z(t)=\#\{k:z_k>t\}\)。删除最大的 \(N\) 个坐标并用 Tonelli，得到

\[
 \boxed{
 \mathcal S_N(z)=\int_0^\infty(n_z(t)-N)_+\,dt.}
\tag{S.278}
\]

因此一个充分的 distributional theorem 是找到 fixed \(N_F\) 与一个对解、尺度、terminal 均统一的 \(\Phi\in L^1(0,\infty)\)，使

\[
 \boxed{
 \#\{k:f_{k,R}(\tau,\delta_*)>sA_R\}
 \le N_F+\Phi(s)
 \Longrightarrow
 \mathcal V^F_{N_F,R}(\tau,\delta_*)\le A_R\|\Phi\|_{L^1}.}
\tag{S.279}
\]

只在一个 threshold 上计数不够；critical \(A_R/t\) count 在 layer-cake endpoint 仍产生 logarithmic divergence。clean short-branch target 为

\[
 \boxed{
 \begin{gathered}
 \textbf{OPEN: find fixed }N_F,\ 0<\delta_*<4,\ C_F^*<\infty\textbf{ such that}\\
 \sup_{\tau\in\mathcal T_R}\mathcal V^F_{N_F,R}(\tau,\delta_*)
 \le C_F^*A_R.\\
 \text{Then (S.275) proves the short gate with }N_{\rm sh}=N_F.
 \end{gathered}}
\tag{S.280}
\]

S.280 是 S.261 的 sufficient replacement，不是 equivalent reformulation；它更强，但目标连续、窗口固定且无 moving selector。

## 63. Inherited \(L_t^1\) ledger 的 method boundary

固定 \(N\)，令 \(M=N+1\)。在同一 terminal window 内放置 \(M\) 个同步 AC spikes，可得

\[
 \boxed{
 \sum_k\int_{\mathcal T_R}|\dot F_{k,H}|=MH,
 \quad \mathcal S_N\left(\left(\int_{J_{\tau_0,\delta}}|\dot F_{k,H}|\right)_k\right)=H,
 \quad {H\over(MH)^{2/3}}={H^{1/3}\over M^{2/3}}\to\infty.}
\tag{S.281}
\]

这是 vector-valued translated-spike witness，**不是 Navier--Stokes solution**。它只证明 AC 加 linear total-mass ledger 不能推出 uniform fixed-\(N\)、\(P^{2/3}\)-scaled window estimate；这是一个明确的 abstract no-go。

Fubini 仍给出 averaged terminal statement：

\[
 \boxed{
 \int_{\mathcal T_R}\sum_kf_{k,R}(\tau,\delta)\,d\tau
 \le\delta R^2\int_{\mathcal T_R}g_R(t)\,dt
 \le C_F\delta R^2P_R^M.}
\tag{S.282}
\]

除去至多 \(\eta R^2\) 的 terminal times 后，

\[
 \sum_kr_k^{\rm sh}(\tau)
 \le C\left(\eta^{-1}\delta P_R^M+\delta^{-2/3}A_R\right).
\tag{S.283}
\]

若内点 optimizer 落在 \((0,4)\)，平衡两项只得到

\[
 \boxed{
 \sum_kr_k^{\rm sh}(\tau)
 \le C\eta^{-2/5}A_R^{3/5}(P_R^M)^{2/5}
 =C\eta^{-2/5}(P_R^M)^{4/5}.}
\tag{S.284}
\]

这弱于所需 \(P^{2/3}\)，且不控制 supremum terminal；它是该方法的精确 exponent boundary，不声称对 NSE sharp。

## 64. Excess branch 与 honest exception accounting

在 Step 8 的 priority-selected set \(\mathcal I_x(\tau)\) 上定义

\[
 \boxed{
 \begin{aligned}
 d_k^{\rm def}(\tau)&=\mathbf1_{\mathcal I_x(\tau)}m_{k,R}(\tau),\\
 h_k(\tau)&=\mathbf1_{\mathcal I_x(\tau)}\int_{H_{k,R}}g_{k,R}(t)\,dt,\\
 b_k(\tau)&=d_k^{\rm def}(\tau)+h_k(\tau),
 \qquad0\le x_k^{\rm sel}(\tau)\le b_k(\tau).
 \end{aligned}}
\tag{S.285}
\]

两个 ancestor vectors 可重叠，但 deletion sets 的 union 给出

\[
 \boxed{
 \mathcal S_{N_D+N_H}(x^{\rm sel})
 \le\mathcal S_{N_D}(d^{\rm def})+\mathcal S_{N_H}(h).}
\tag{S.286}
\]

若存在一个共享 exceptional set \(E_\tau\)、\(\#E_\tau\le N_b\)，且在其外
\(b_k\le q_k+c_kp_k^{2/3}\)、\(\sum q_k\le C_qA_R\)、\(\sum p_k\le C_pP_R^M\)、\(\sum c_k^3\le C_c\)，则 shellwise Hölder 得到

\[
 \boxed{
 \mathcal S_{N_b}(b)
 \le(C_q+C_c^{1/3}C_p^{2/3})A_R.}
\tag{S.287}
\]

PDE 必须构造这些对象并保留 full-history ancestry。bare minimal statement 仍为

\[
 \boxed{
 \textbf{OPEN:}\quad
 \exists N_b,C_b\text{ fixed such that }
 \mathcal S_{N_b}(b(\tau))\le C_bA_R.}
\tag{S.288}
\]

## 65. Conditional moving-tube Morrey theorem

令 \(\widetilde{\boldsymbol\mu}\) 为 total local dissipation measure 的 periodic lift，\(\widetilde X_R\) 为 mollified path 的 continuous lift，并定义 full-history tube

\[
 \boxed{
 \mathcal U_{k,R}(\tau)
 =\{(t,y):s_R<t<\tau,\ y-\widetilde X_R(t)\in\operatorname{supp}\psi_k^R\}.}
\tag{S.289}
\]

假设在所限制的整个 solution class、所有尺度与 terminals 上存在共同常数 \(M,L<\infty\)：

\[
 \boxed{
 \sup_{Q_R^-(z,s)}{\widetilde{\boldsymbol\mu}(Q_R^-(z,s))\over R}\le M,
 \qquad
 \mathcal L_R(\tau)={1\over R}\int_{s_R}^{\tau}|\dot{\widetilde X}_R(t)|\,dt\le L.}
\tag{S.290}
\]

按 elapsed time \(O(R^2)\) 或 accumulated path variation \(O(2^kR)\) 贪心停时，可用至多

\[
 \boxed{C_\psi(2^{3k}+L2^{2k})}
\tag{S.291}
\]

个 backward \(R\)-cylinders 覆盖 \(\mathcal U_{k,R}(\tau)\)。arc-length stopping 不可用 endpoint displacement 代替。又因 \(\boldsymbol\mu=|\nabla u|^2dxdt+\boldsymbol D\) 正好一次分解，defect 与 restricted high-Rayleigh viscous parts 相加后只需支付 tube total mass 一次：

\[
 \boxed{
 b_k(\tau)
 \le {\gamma_k\over R}\widetilde{\boldsymbol\mu}(\mathcal U_{k,R}(\tau))
 \le C_\psi M\gamma_k(2^{3k}+L2^{2k}).}
\tag{S.292}
\]

令 \(\mathscr A_m=\sum_{k\ge1}2^{mk}\gamma_k<\infty\)（\(m=2,3\)），则

\[
 \boxed{
 \sum_kx_k^{\rm sel}(\tau)\le\sum_kb_k(\tau)
 \le B(M,L):=C_\psi M(\mathscr A_3+L\mathscr A_2).}
\tag{S.293}
\]

与 inherited linear cap \(\sum x_k^{\rm sel}\le C_0P_R^M\) 合并，在 \(P_R^M\le1\) 与 \(P_R^M\ge1\) 两区分别选择较强上界，得到

\[
 \boxed{
 \mathcal S_0(x^{\rm sel}(\tau))
 \le\max\{C_0,B(M,L)\}A_R.}
\tag{S.294}
\]

这是真正证明的 **conditional theorem**。允许 \(M=M(u,R)\) 或 \(L=L(u,R)\) 只会恢复 nonuniform fixed-solution finiteness，不能冒充 bare suitable-weak class 的 uniform packing。

## 66. Scale-critical mixed-norm benchmark

令 \(q\in[3,\infty]\)、\(r\in[3,\infty)\)，\(\theta=3/r+2/q\)，并在 restricted class 的所有 target scales 上假设

\[
 \boxed{
 \mathcal U_{q,r}(R)=R^{1-\theta}
 \|u\|_{L_t^q(I_{8R};L_x^r(\mathbb T^3))}\le M_*.}
\tag{S.295}
\]

mean-zero periodic pressure gauge 与 Calderón--Zygmund 给出

\[
 \boxed{
 \|p-\bar p(t)\|_{L_t^{q/2}L_x^{r/2}}
 \le C_rM_*^2R^{2\theta-2}.}
\tag{S.296}
\]

把等于一的 smooth spacetime test 插入 \(\boldsymbol\mu\) 的 distribution definition，得到

\[
 \begin{aligned}
 \boldsymbol\mu(Q_R^-)
 \le C\bigg[&R^{-2}\int_{Q_{2R}^-}|u|^2
 +R^{-1}\int_{Q_{2R}^-}|u|^3\\
 &+R^{-1}\int_{Q_{2R}^-}|p-\bar p(t)|\,|u|\bigg].
 \end{aligned}
\tag{S.297}
\]

mixed Hölder 后所有 \(R\) powers 精确抵消为一次 \(R\)：

\[
 \boxed{
 \sup_{Q_R^-}{\boldsymbol\mu(Q_R^-)\over R}
 \le C_{q,r}(M_*^2+M_*^3)=:M_\mu.}
\tag{S.298}
\]

同时 \(|\dot X_R(t)|\le CR^{-3/r}\|u(t)\|_{L^r}\)，故

\[
 \boxed{
 {1\over R}\int_{s_R}^{\tau}|\dot X_R(t)|\,dt
 \le CM_*R^{-1-3/r+2-2/q+\theta-1}=CM_*.}
\tag{S.299}
\]

代入 S.294 得

\[
 \boxed{
 \mathcal S_0(x^{\rm sel}(\tau))\le C_{q,r,M_*}A_R.}
\tag{S.300}
\]

这只是 conditional sanity check：critical strong norm ball 已有更强 regularity theory；当 \(\theta>1\) 时，单个解的 global mixed norm finiteness 不推出 S.295 所需的 scale-Morrey decay。这里也不把 weak \(L^3\) 未经 Lorentz endpoint argument 直接代入 cubic row。

## 67. Partial regularity 为什么没有闭合 excess gate

CKN 给出 singular set 的 parabolic \(\mathcal H^1\)-measure 为零，这是 support-size conclusion，不是 \(\boldsymbol D\) 的 mass-density upper bound。抽象测度

\[
 \boxed{
 \boldsymbol D_M=\sum_{k=1}^Ma_k\delta_{z_k},\qquad a_k>0}
\tag{S.301}
\]

可支撑在有限点集上，却在 \(M\) 个 moving annular tubes 中各有非零 weighted mass。它只是反驳“dimension 自动推出 packing”的 measure countermodel，**不是 NSE defect measure**。

high-Rayleigh ancestor 属于 \(|\nabla u|^2dxdt\)，可完全位于 regular set。于是

\[
 \boxed{
 \text{large high-Rayleigh mass}\ \not\Longrightarrow\
 \text{a singular point detected by epsilon regularity}.}
\tag{S.302}
\]

epsilon regularity 的 converse 不把每个大的 regular viscous mass 变成 singular point。即使有一个 threshold 的 singular-cylinder count，也仍需提升为 all-threshold integrable mass distribution 才能推出 S.288。

## 68. Bounded primary-source collision audit

有限文献检索覆盖 Caffarelli--Kohn--Nirenberg 的 partial regularity、De Rosa--Drivas--Inversi 的 anomalous dissipation support、Seregin 的 critical Morrey estimates、Barker 在附加 weak-\(L^3\) bound 下的 singular-point count，以及 Neustupa 的 singular-point \(L^3\) concentration。没有找到与 S.280 或 S.288 量词完全相同的 theorem。

这些来源分别控制 singular-set size、附加 integrability 下的 density、假设性的 critical coefficient 或依赖额外 norm 的 singular-point count；都没有从 bare inherited ledger 推出 full-history high-Rayleigh annular best-\(N\) packing。检索只用于标记 literature boundary，不构成 novelty 或 priority proof。

## 69. Route decision 与 combined target

short branch 应直接攻连续公共窗口 gate S.280，最好通过 all-threshold count S.279；scalar temporal \(L^1\)、terminal averaging 或没有 endpoint gain 的 critical one-threshold count 已被证明不足。excess branch 应攻 shared ancestor charging S.287 或足以触发 S.294 的 uniform moving-tube coefficient；defect 与 high-Rayleigh budgets 必须按 S.286 相加。

combined Step 12 target 是

\[
 \boxed{
 \begin{gathered}
 \textbf{OPEN: find fixed }N_F,N_b\textbf{ and constants such that}\\
 \sup_{\tau\in\mathcal T_R}\mathcal V^F_{N_F,R}(\tau,\delta_*)\lesssim A_R,
 \qquad
 \sup_{\tau\in\mathcal G_R\cap\mathcal T_R}\mathcal S_{N_b}(b(\tau))\lesssim A_R.\\
 \text{Then Step 11 closes with }N_{\rm sh}=N_F,\ N_x=N_b,
 \text{ and total budget }N_F+N_b.
 \end{gathered}}
\tag{S.303}
\]

两个 antecedents 在 bare suitable-weak class 中都 **OPEN**；第二项目前只在 Section 65/66 的附加统一假设下证明。

## 70. 单包加速的 kinematic screen

inherited R0.74F packet centre 满足 \(Q(t)=q_{\rm pre}+B\int_0^t\theta(s,h)ds\)、\(|\theta|\le1\)、\(0<B\le(32R^2)^{-1}\)，故

\[
 \boxed{
 \operatorname{Var}_{[0,65R^2]}Q\le{65\over32}<2\pi,
 \qquad \operatorname{Var}_{I_{2R}}Q\le{1\over8}.}
\tag{S.304}
\]

冻结 exact family 的 packet centre 不发生一次完整 torus winding；R0.74F 的 all-winding estimates 是 Brownian-bridge heat kernel 的 periodic copies，不是 packet-centre orbits。

若 hypothetical monotone extension 满足 \(0<\beta B\le q'(t)\le B\)，对 torus measurable set \(J\)，令 \(D=q(T)-q(0)\)、\(m=\lfloor D/(2\pi)\rfloor\)，则 change of variables 给出 exact occupation bound

\[
 \boxed{
 {m|J|\over B}\le\tau_J\le{(m+1)|J|\over\beta B}.}
\tag{S.305}
\]

many-winding regime 中 \(m\asymp BT\)，访问次数与每次 residence time 的 \(B\) 因子抵消，不能产生 outer dyadic shells 的 exponential preference。若 \(z_\ell\le H2^{p\ell}\Gamma^{4^\ell}\)，且 \(q_N=2^p\Gamma^{3\cdot4^N}<1\)，则

\[
 \boxed{
 \mathcal S_N(z)
 \le\sum_{\ell\ge N}z_\ell
 \le{H2^{pN}\Gamma^{4^N}\over1-q_N}.}
\tag{S.306}
\]

所以 uniform speed-up 只改变共同 prefactor，不改变 super-Gaussian shell ratio。这是 kinematic screen，**不是 universal PDE no-go**，也没有把 earlier packet deposit 识别成 complete ancestor vector \(b\)。

## 71. Step 12 主张边界与双路审计

Step 12 **PROVED**：S.274--S.275 terminal variation-window reduction；S.276--S.277 continuity 与 fixed-solution modulus；S.278--S.279 best-\(N\) layer cake 与 all-threshold implication；S.281--S.284 \(L_t^1\)-only abstract no-go 与 averaged \(P^{4/5}\) boundary；S.285--S.287 exception-budget recombination 与 conditional charging；S.289--S.294 moving-tube cover 与 conditional critical-Morrey theorem；S.295--S.300 mixed-norm sufficient benchmark；S.304--S.305 literal no-winding 与 occupation lemma；S.306 abstract super-Gaussian filter。

Step 12 **ABSTRACT BOUNDARY TESTS, NOT NSE COUNTEREXAMPLES**：S.281 synchronized temporal spikes；S.301 finite atomic defect-support model。

Step 12 **OPEN**：universal terminal-window gate S.280；universal ancestor gate S.288；combined S.303；Step 11 S.272；Q.12、Q.1；从 frozen payment alone 推出 uniform critical Morrey/path estimate；把 earlier moving-packet deposit 与完整 \(b\) 识别；bare suitable weak class 的 universal shell count；scale contraction、regularity、singularity 与 Clay。

主证书通过 16/16 exact、12/12 finite、51/51 structural 与 11/11 mutations。独立 Ruby audit 通过 12/12 groups、153,237 exact cases、6/6 artifact locks、6/6 dependency locks、39/39 note checks；两条实现相互独立地封存 source 与证书边界。有限检查只支持公式实现与防篡改，不替代 analytic proof。

**TERMINAL WINDOW: EXACT REDUCTION. MORREY PACKING: CONDITIONAL. UNIVERSAL WINDOW / ANCESTOR GATES: OPEN. SPEED-ONLY ROUTE: KINEMATICALLY SCREENED, NOT A UNIVERSAL NO-GO. NOT CLAY.**
