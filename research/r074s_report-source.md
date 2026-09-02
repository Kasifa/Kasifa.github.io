# R0.74S｜一侧球时钟为何仍留下 ℓ¹ 债务

## 0. 这一步得到什么

R0.74R 把任意 completed clock 的困难分成累计耗散、真实动能窗口和近期正变差三支。R0.74S 继续检验其中最自然的修复：在最后一次 upcrossing 处停止每个活跃壳层，用一侧球 cutoff 完成剩余的 root、outer 与 weight-drop 三条有符号通道，再利用正性和相邻壳层消去边界。

本节证明了三件事：

- 三条有符号通道都有精确的 stopped ball-clock 表示，但时间方向不同；
- 从 collar 换成 ball 不会增加低阶损失，所有二次 cutoff 行仍由 \(A_R=(P_R^M)^{2/3}\) 支付；
- terminal weight-drop ball clocks 满足精确 Abel 恒等式，但右端是完整的 \(\ell^1\) shell residual，而不是匹配平方函数。

最后，一个光滑抽象时钟塔使 ball-clock 债务等于 \(N\)，而平方函数只等于 \(\sqrt N\)。因此，单靠 completed-clock 正性、cutoff 线性与 tower 恒等式，不能推出所需的 \(\ell^2\) 压缩。这是一个 **PROVED ABSTRACT NO-GO**；见证不是速度场、压力场、耗散测度或 Navier--Stokes 解，不能写成 PDE/NSE 反例。

无条件 stopped-work 估计、跨通道动力学符号定理、R0.74R 的普适 persistence 输入、固定尺度不等式、尺度收缩、正则性与奇点形成仍为 **OPEN / NOT CLAIMED**。**NOT CLAY.**

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

## 7. 证书与独立审计

最终确定性证书通过：

- 5/5 个精确 ledger 行；
- 7/7 个有限检查；
- 55/55 个结构检查；
- 4/4 个负向符号突变检查。

有限覆盖包括 312 个有理 cutoff 值、228 个导数样本、1024 个含并列 stop 的 stopped configuration、82432 个布尔激活比较、\(M=2,\ldots,8\) 的全部有限 Abel 端点，以及 \(N=1,\ldots,24\) 在五个有理时刻的抽象 tower。两个临时目录独立重算得到逐字节一致的 JSON 与 Markdown 报告。

这些是 **FINITE** 证书，只验证公式实现和符号哨兵；它们不机器证明 cutoff 光滑性、周期化/unfolding、suitable local-energy 计算、无限支撑估计或抽象见证的 PDE 实现。解析证明和有限证书必须继续分开。

## 8. 决定与下一门槛

本节已经 **PROVED**：

- 一侧 ball cutoff 与 flux 符号恒等式；
- completed ball-clock tower；
- 三族二次 \(\mathscr Q\) 付款；
- root、outer、weight-drop 的精确 stopped 时间方向；
- terminal weight-drop Abel 恒等式；
- 标量 positive-clock 的 \(\ell^1/\ell^2\) obstruction。

本节只关闭一条独立代数路线：把所有剩余 signed face 分别完成成正 ball clock，再逐项取绝对值或终端值，不能从正性、线性与 tower identity 得到 matched square-function estimate。

仍可能有效的下一步必须保留跨通道动力学关系，例如 root supply 与 inactive inner shell、outer leakage 与 later merge、weight-drop 与取正之前的 negative work/backscatter 之间的符号耦合；另一种可能是证明 stopped block genealogy 具有统一有限复杂度。

root/outer/weight-drop 动力学控制、耗散主导分支、R0.74R persistence hypotheses、无条件固定尺度不等式 (Q.1)、尺度收缩、正则性、奇点形成和 Clay 问题全部保持 **OPEN / NOT CLAIMED**。

**PROVED ABSTRACT NO-GO ONLY. NOT PDE/NSE. NOT CLAY.**

## 9. 继承边界

- actual collar traces 与四通道 split：继承自 R0.74S Step 3，PROVED；
- stopped-family activation：继承自 R0.74S Step 2，PROVED；
- thin boundary clock 与 \(K_m^\partial\le K_m\)：继承自 R0.74S Step 4，PROVED；
- suitable-weak completed-clock operator：继承自 R0.74P，PROVED；
- weighted \(S_2\) 与 doubled-radius support ledger：继承自 R0.74H，PROVED；
- frozen adjacent-weight tail：继承自 R0.74S Step 1，PROVED。

不声称新颖性、优先权、正则性或千禧年问题结论。
