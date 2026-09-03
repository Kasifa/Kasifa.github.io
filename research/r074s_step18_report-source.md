# R0.74S Step 18 中文读者稿

## 126. 结论与修正：真正缺失的是时间量词的中间层

Step 17 已证明 absolute temporal-variation tail 的所有次线性幂估计都为 FALSE，并保留逐坐标 positive excursion \(\mathfrak O^{F,+}_{N,R}\) 作为一个充分的 signed 后继。但它对每个 shell 分别取时间上确界，再对 shell 求和；Step 15 的实际 residual gate 则先固定一个 terminal time。Step 18 补上两者之间缺失的 fixed-deletion functional，并把三种量词次序精确分开。

直接 Step 15 gate 是 \(\sup_\tau\inf_{\#S\le N}\sum_{k\notin S}z_k(\tau)\)。若要求一个异常 shell 集合对所有 common good terminal times 同时有效，就得到更强但仍非 separable 的 \(\inf_{\#S\le N}\sup_\tau\sum_{k\notin S}z_k(\tau)\)。它仍弱于逐坐标 positive excursion。

completed-clock simultaneous height 在一次支付已控制的 \(Q\)-variation 后控制 fixed-set hybrid tail；反向上，Step 10 paid-branch inequality 用 fixed hybrid tail 加已知 \(A_R\)-scale payments 控制 simultaneous height。因此两者只在目标尺度上等价，不是字面相等，也不等同于更弱的 moving-deletion gate。

互不相交的 triangular clocks 证明前两条层级不等式都可严格，并且逐坐标 maxima 可以任意倍数高估 simultaneous height。正确的严格例子需要 \(M\ge N+2\)，不是 \(M=N+1\)。同一抽象族还证明 inherited nonnegativity、\(Q\)-variation 与 linear absolute-flux ledger 不能纯代数推出所需 \(2/3\)-power estimate。这是 ABSTRACT information-theoretic obstruction，不是 Navier--Stokes 反例。

Step 17 的 recurrent Taylor smooth family 不否定任何仍存活的 gate：固定 \(N\) 后按 S.451 固定 \(R\)，它只把 positive excursion 饱和在 quadratic scale，同时继续否定已经弃用的 absolute-variation route。本节是严格 route reduction 与 correction；不证明 fixed-deletion gate、direct hybrid gate、Q.12、Q.1、scale contraction 或 regularity。**NOT CLAY.**

## 127. 冻结设定与三种 deletion order

固定一个 Version-M suitable weak solution、一个 admissible scale \(R\)、一个 admissible profile \(\boldsymbol\lambda\)、一个 terminal domain \(\mathcal D\in\{I_R,\mathcal T_R\}\) 以及一个 \(N\in\mathbb N_0\)。令 \(I=[s_R,t_0)\)、\(\mathcal D_g=\mathcal D\cap\mathcal G_R\)。继承对象满足

\[
 \boxed{K_{k,R}=F_{k,R}+Q_{k,R}\ge0,\qquad F_{k,R}(s_R)=Q_{k,R}(s_R)=K_{k,R}(s_R)=0.}
 \tag{S.476}
\]

并且

\[
 B_{F,R}:=\sum_{k\ge1}\operatorname{TV}_{I}F_{k,R}\le C_FP_R^M,
 \qquad B_{Q,R}:=\sum_{k\ge1}\operatorname{TV}_{I}Q_{k,R}\le C_QA_R,
 \qquad A_R=(P_R^M)^{2/3}.
\]

保留 Step 15 的 nonnegative stopped-flux vector

\[
 z_k(\tau)=F_{k,R}(\tau)-F_{k,R}(\sigma_k^{\rm hyb}(\tau)),
 \qquad \tau\in\mathcal D_g,
\]

其中 active coordinate 上 \(\sigma_k^{\rm hyb}(\tau)\in[s_R,\tau]\)，否则 \(z_k(\tau)=0\)；Step 15 已证明 \(z(\tau)\in\ell^1_+\)。设 \(\mathscr S_N=\{S\subset\mathbb N:\#S\le N\}\)，定义

\[
 \boxed{\begin{aligned}
 \mathfrak H^{\rm hyb}_{N,R}(\mathcal D)
 &:=\sup_{\tau\in\mathcal D_g}\inf_{S\in\mathscr S_N}\sum_{k\notin S}z_k(\tau)
 =\mathfrak Z_{N,R}^{\boldsymbol\lambda}(\mathcal D),\\
 \mathfrak H^{\rm fix}_{N,R}(\mathcal D)
 &:=\inf_{S\in\mathscr S_N}\sup_{\tau\in\mathcal D_g}\sum_{k\notin S}z_k(\tau).
 \end{aligned}}
 \tag{S.477}
\]

这里的 fix 只表示：对每个已经固定的 solution、scale、centre 与 terminal domain，同一个 shell set 要用于全部 common good terminal times；该集合仍可依赖这些固定数据。它不冻结 hybrid starts，后者仍依赖 terminal time。

为比较，定义

\[
 \boxed{o_{k,R}^F:=\sup_{s_R\le a<b<t_0}[F_{k,R}(b)-F_{k,R}(a)]_+,
 \qquad \mathfrak O^{F,+}_{N,R}:=\inf_{S\in\mathscr S_N}\sum_{k\notin S}o_{k,R}^F.}
 \tag{S.478}
\]

因为 \(o_{k,R}^F\le\operatorname{TV}_I F_{k,R}\)，序列 \((o_{k,R}^F)_k\in\ell^1_+\)，且对每个 \(k,\tau\) 都有 \(0\le z_k(\tau)\le o_{k,R}^F\)。以下所有级数都由同一可和序列控制，不交换任何无限 signed sum。

## 128. 精确层级与 layer-cake incidence

minimax inequality 与逐坐标支配直接给出

\[
 \boxed{\mathfrak H^{\rm hyb}_{N,R}(\mathcal D)
 \le\mathfrak H^{\rm fix}_{N,R}(\mathcal D)
 \le\mathfrak O^{F,+}_{N,R}
 \le\mathfrak H^F_{1,N,R}.}
 \tag{S.479}
\]

第一条只用 \(\sup\inf\le\inf\sup\)，不假设 minimax equality 或 attainment。第二条来自 \(z_k(\tau)\le o_{k,R}^F\)，第三条来自 \(o_{k,R}^F\le\operatorname{TV}F_{k,R}\)；若 infimum 不取到，就用 \(\varepsilon\)-minimizer 再令 \(\varepsilon\downarrow0\)。

对 \(\lambda>0\)，令 \(A_\tau(\lambda)=\{k:z_k(\tau)>\lambda\}\)、\(A_o(\lambda)=\{k:o_{k,R}^F>\lambda\}\)。layer-cake 与 best-\(N\) rearrangement 给出

\[
 \boxed{\begin{aligned}
 \mathfrak H^{\rm hyb}_{N,R}(\mathcal D)
 &=\sup_{\tau\in\mathcal D_g}\int_0^\infty(\#A_\tau(\lambda)-N)_+\,d\lambda,\\
 \mathfrak H^{\rm fix}_{N,R}(\mathcal D)
 &=\inf_{S\in\mathscr S_N}\sup_{\tau\in\mathcal D_g}
 \int_0^\infty\#(A_\tau(\lambda)\setminus S)\,d\lambda,\\
 \mathfrak O^{F,+}_{N,R}
 &=\int_0^\infty(\#A_o(\lambda)-N)_+\,d\lambda.
 \end{aligned}}
 \tag{S.480}
\]

对非负 \(\ell^1\) 序列 \(x\)，所用恒等式为

\[
 \inf_{\#S\le N}\sum_{k\notin S}x_k
 =\int_0^\infty(\#\{k:x_k>\lambda\}-N)_+\,d\lambda.
\]

先对有限截断排序，再用 monotone convergence 即得无限序列版本。S.480 中间一行仅在固定 \(S,\tau\) 后使用 Tonelli；两个 optimization 都没有穿过积分号。

这正定位量词缺口：direct gate 可在知道每个 terminal time 后改变删除集；fixed gate 要求一个集合击中全部 common good terminal times；separable excursion gate 又把 \(A_\tau(\lambda)\) 换成更大的 coordinatewise envelope \(A_o(\lambda)\)，因而忘记不同 shell peaks 是否只在互斥时刻出现。这里只断言 \(\bigcup_\tau A_\tau(\lambda)\subseteq A_o(\lambda)\)，不断言相等。

## 129. Completed-clock simultaneous height 与目标尺度等价

定义 terminal domain 上的 fixed-deletion simultaneous height

\[
 \boxed{\mathfrak L^K_{N,R}(\mathcal D):=
 \inf_{S\in\mathscr S_N}\sup_{t\in\mathcal D}\sum_{k\notin S}K_{k,R}(t).}
 \tag{S.481}
\]

它不同于 Step 17 的 separable maximum \(\mathfrak M^K_{N,R}=\inf_S\sum_{k\notin S}\sup_{t\in I}K_{k,R}(t)\)：\(\mathfrak L^K\) 的时间上确界位于 shell sum 外，但仍保留一个 deletion set。

对 active hybrid coordinate，\(K=F+Q\)、\(K\ge0\) 与 \(\sigma_k^{\rm hyb}(\tau)\le\tau\) 给出

\[
 \boxed{\begin{aligned}
 z_k(\tau)&=K_k(\tau)-K_k(\sigma_k^{\rm hyb}(\tau))-Q_k(\tau)+Q_k(\sigma_k^{\rm hyb}(\tau))\\
 &\le K_k(\tau)+\operatorname{TV}_I Q_k.
 \end{aligned}}
 \tag{S.482}
\]

在同一个固定 \(S\) 外求和，先取 terminal supremum，再优化，得到

\[
 \boxed{\mathfrak H^{\rm fix}_{N,R}(\mathcal D)
 \le\mathfrak L^K_{N,R}(\mathcal D)+B_{Q,R}
 \le\mathfrak L^K_{N,R}(\mathcal D)+C_QA_R.}
 \tag{S.483}
\]

所有 clock sums 都有限，因为共同零起点给出 \(K_k(t)\le o_{k,R}^F+\operatorname{TV}_I Q_{k,R}\)，故 \(\sum_k\sup_tK_k(t)\le B_{F,R}+B_{Q,R}<\infty\)。

令 \(\Pi_R^{\boldsymbol\lambda}=6B_{Q,R}+C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R\le C_{\rm pay}(\boldsymbol\lambda)A_R\)。Step 10 S.235 对同一个固定 \(S\) 与每个 good terminal time 给出 \(\sum_{k\notin S}K_{k,R}(\tau)\le\Pi_R^{\boldsymbol\lambda}+6\sum_{k\notin S}z_k(\tau)\)。利用 \(t\mapsto(K_{k,R}(t))_k\) 在 \(\ell^1\) 中连续、common good-time set 稠密，得到反向估计

\[
 \boxed{\mathfrak L^K_{N,R}(\mathcal D)
 \le\Pi_R^{\boldsymbol\lambda}+6\mathfrak H^{\rm fix}_{N,R}(\mathcal D).}
 \tag{S.484}
\]

所以对固定 admissible profile 和固定 universal \(N\)，\(\mathfrak H^{\rm fix}\lesssim A_R\) 当且仅当 \(\mathfrak L^K\lesssim A_R\)。这是支付已知项后的 target-scale equivalence，不是 literal equality，也不把任一 functional 等同于更弱的 moving-deletion tail。

最后，固定删除集后，sum 的 supremum 不超过 coordinatewise suprema 之和；结合 Step 17 S.475，

\[
 \boxed{\mathfrak L^K_{N,R}(\mathcal D)
 \le\mathfrak M^K_{N,R}
 \le\mathfrak O^{F,+}_{N,R}+B_{Q,R}.}
 \tag{S.485}
\]

不存在从 \(\mathfrak L^K\) 到 \(\mathfrak M^K\) 的 universal reverse comparison；后面的 abstract clocks 给出无界分离。

## 130. 修正后的 OPEN targets 与无条件线性 fallback

最弱且精确匹配 Step 15 route 的 direct target 仍是某个 universal finite \(N_0,C\) 下 \(\mathfrak H^{\rm hyb}_{N_0,R}(\mathcal T_R)\le CA_R\)；它与 full residual gate 相差 Step 15 S.385 的字面因子 \(5\)。

若坚持一个 exceptional shell set 对全部 common good terminal times 同时有效，route-minimal successor 是

\[
 \boxed{\begin{gathered}
 \exists N_{\rm fix}\in\mathbb N_0,\ C_{\rm fix}<\infty
 \text{ for the fixed universal admissible profile, such that}\\
 \mathfrak H^{\rm fix}_{N_{\rm fix},R}(\mathcal T_R)
 \le C_{\rm fix}(P_R^M)^{2/3}
 \quad\text{uniformly in the solution and admissible }R,z_0.
 \end{gathered}}
 \tag{S.486}
\]

S.486 为 **OPEN**。由 S.479，它蕴含 direct hybrid gate，进而通过既证 reductions 蕴含 Step 10 S.243、Q.12 与 Q.1；它比 direct gate 更强，因为 direct exceptional set 可依赖 \(\tau\)。

目标尺度等价的 completed-clock 表述是

\[
 \boxed{\begin{gathered}
 \exists N_L\in\mathbb N_0,\ C_L<\infty
 \text{ for the fixed universal admissible profile, such that}\\
 \bigl(\mathfrak L^K_{N_L,R}(\mathcal T_R)\bigr)^{3/2}
 \le C_LP_R^M
 \quad\text{uniformly in the solution and admissible }R,z_0.
 \end{gathered}}
 \tag{S.487}
\]

S.487 同样为 **OPEN**。S.483--S.484 只证明它与 S.486 在目标尺度等价，常数仅依赖同一冻结 profile；二者都强于 direct moving-deletion gate。

继承的无条件信息只有

\[
 \boxed{\mathfrak H^{\rm fix}_{N,R}(\mathcal D)\le B_{F,R}\le C_FP_R^M,
 \qquad \mathfrak L^K_{N,R}(\mathcal D)\le B_{F,R}+B_{Q,R}
 \le C_FP_R^M+C_QA_R.}
 \tag{S.488}
\]

当 \(P_R^M\le1\) 时第一式已不超过 \(C_FA_R\)；当 \(P_R^M>1\) 时，它还差因子 \((P_R^M)^{1/3}\)。只重排 displayed linear ledger 无法消掉这一因子。

## 131. Disjoint triangular clocks 的精确 ABSTRACT separation

固定整数 \(M>N\)、高度 \(H>0\) 与 \(I=[0,1]\)。对 \(1\le j\le M\)，令

\[
 \boxed{\phi_j(t)=\left(1-2M\left|t-\frac{2j-1}{2M}\right|\right)_+,
 \qquad K_j(t)=F_j(t)=H\phi_j(t),\qquad Q_j(t)=0,}
 \tag{S.489}
\]

其 support interiors 两两不交，后续坐标为零，并取 common-zero-start increment \(z_j(\tau)=H\phi_j(\tau)\)。每个时刻至多一个坐标为正；任一至多删除 \(N<M\) 项的固定集合都遗漏某个 peak。于是

\[
 \boxed{\begin{aligned}
 \mathfrak H^{\rm hyb}_N&=\begin{cases}H,&N=0,\\0,&N\ge1,\end{cases}
 &\mathfrak H^{\rm fix}_N&=H,&\mathfrak L^K_N&=H,\\
 \mathfrak O_N^{F,+}&=\mathfrak M_N^K=\mathfrak V_N^K=(M-N)H,
 &\mathfrak H^F_{1,N}&=2(M-N)H,
 &\sum_j\operatorname{TV}F_j&=2MH.
 \end{aligned}}
 \tag{S.490}
\]

特别地，当 \(N\ge1\) 且 \(M\ge N+2\) 时，

\[
 \boxed{0=\mathfrak H^{\rm hyb}_N
 <\mathfrak H^{\rm fix}_N=\mathfrak L^K_N
 <\mathfrak O_N^{F,+}=\mathfrak M_N^K.}
 \tag{S.491}
\]

比值 \(\mathfrak O_N^{F,+}/\mathfrak H_N^{\rm fix}=M-N\) 在固定 \(N\)、\(M\to\infty\) 时无界。因此 abstract clock class 中不存在从 simultaneous functional 到 separable coordinatewise maximum 的 universal reverse comparison。先前诱人的 \(M=N+1\) 只分开 moving 与 fixed deletion，不能使第二条不等式严格。

以 full absolute-flux ledger \(\mathcal P=\sum_j\operatorname{TV}F_j=2MH\) 归一化。固定 \(N\) 与任意 \(M>N\)，令 \(H\to\infty\)，则

\[
 \boxed{\frac{\mathfrak H_N^{\rm fix}}{\mathcal P^{2/3}}
 =\frac{\mathfrak L_N^K}{\mathcal P^{2/3}}
 =\frac{H^{1/3}}{(2M)^{2/3}}\longrightarrow\infty.}
 \tag{S.492}
\]

所以 \(K\ge0\)、\(K=F+Q\)、\(B_Q\lesssim\mathcal P^{2/3}\) 与 \(\sum_k\operatorname{TV}F_k\lesssim\mathcal P\) 这些 abstract assumptions，不能对任何预先指定的有限 \(N\) 推出 fixed-deletion quadratic bound。高度 \(H\) 是独立参数；只令 \(M=N+1\)、\(H=M^3\) 改变的是对 \(N\) 的 uniformity，不能否定 fixed-\(N\) statement。

S.489--S.492 全部是 **ABSTRACT CLOCK STRESS TESTS**：它们不是 spatial fields，不实现 Version-M payment，也不是 Navier--Stokes solutions 或 counterexamples。

## 132. Recurrent Taylor family 通过所有仍存活的 gates

对 Step 17 的 exact smooth family，先固定有限 \(N\)，再按 S.451 选择并固定 \(R\)。对该量词次序以及 \(A\ge A_0(N,R)\)，

\[
 \mathfrak O^{F,+}_{N,R}\asymp_{N,R}A^2,
 \qquad B_{Q,R}=O_R(A^2),
 \qquad P_R^M\asymp_RA^3.
\]

因此 S.479 与 S.485 给出

\[
 \boxed{\mathfrak H^{\rm hyb}_{N,R}
 \le\mathfrak H^{\rm fix}_{N,R}
 \lesssim_{N,R}A^2
 \asymp_{N,R}(P_R^M)^{2/3},
 \qquad \mathfrak L^K_{N,R}(\mathcal T_R)\lesssim_{N,R}A^2.}
 \tag{S.493}
\]

这是 fixed-\(R\) screen，不是 universal S.486 或 S.487 的证明。它只说明摧毁 absolute temporal variation 的 smooth recurrent family 与全部存活的 quadratic gates 相容：recurrence 产生 \(O(A)\) 次重复绕行，但 peaks 处于同一 phase geometry，signed excursion 仍为 \(O(A^2)\)。

## 133. 成功的 PDE theorem 必须补入什么

精确 reductions 留下三个嵌套研究目标：最弱的 direct hybrid target 是 \(\mathfrak H^{\rm hyb}\lesssim A_R\)，完全匹配 Step 15；fixed-deletion target 是 S.486，要求一个共同有限 shell set，但保留 simultaneous terminal incidence；completed-clock target 是 S.487，或更强的 Step 17 positive-excursion bound。simultaneous-height form 在已知 payment 后与 fixed hybrid gate 等价，而 separable positive excursion 仍要求额外 cross-time information。

triangular clocks 已证明新输入不能只有 nonnegativity 与 inherited linear ledgers。可行 theorem 至少要加入一个真正 PDE-specific mechanism，例如：

- simultaneous height-to-cubic-payment estimate；
- persistence 或 dwell-time，使高 clock aggregate 占据足够 parabolic time 并由 cubic payment 支付；
- deterministic stopping-time / Carleson charge，控制 S.480 的 time--shell incidence sets；
- 与 hybrid first-passage intervals 绑定的 signed entrance 或 collar-flux payment。

这些只是 mechanism classes，不是已证明 lemmas。

## 134. 一手来源 collision boundary

有界两轮一手来源检索没有找到同时具有 S.486 全部量词的 theorem：deterministic suitable weak solutions；对每个固定 solution、scale、centre 与 terminal domain，保留一个 finite shell deletion 覆盖全部 common good terminal times；对 forward stopped increments 作 infinite-shell \(\ell^1\) sum；删除预算 universal；并由 \((P_R^M)^{2/3}\) 支付。

- Dascaliuc--Grujić 的 physical-scale energy cascade / flux locality 证明 inertial-range 条件下的 signed time/ensemble-averaged flux estimates，不是带一个 shell deletion 的 terminal-time maximum。
- Yang 的 flow-generated skewed cylinders maximal functions 给出 space-time averages 的 weak-\((1,1)\) 与 strong-\((p,p)\) bounds，不控制 simultaneous clock height 或 fixed best-\(N\) terminal functional。
- Yu 的 finite-chain CKN bad-scale counting 在预先指定的有限 scale chain 上用 nonnegative channel costs 得到至少一个 CKN-small scale，不给 infinite-shell、all-good-terminal 的 S.486。
- Yu 的 coarse-grained pressure-flux work depletion 给出 exact fixed-chain signed-work depletion，并明确保留 negative work / backscatter；它不声称 negative set smallness、uniform moving-window constants 或 chain length 趋于无穷时的 summability。

这些是相邻工具与可能 ingredients，不是 open gate 的证明。检索有界；未命中不构成 novelty、priority 或 exhaustiveness claim。

## 135. 主张账本、证书与严格后续边界

本节 **PROVED**：S.476--S.479 的 hierarchy 与 infinite-shell justification；S.480 的 exact layer-cake incidence formulas；S.481--S.485 的 completed-clock 双向 target-scale reduction；S.488 的 unconditional linear fallback；S.489--S.492 的 abstract triangular-clock exact values；S.493 的 fixed-\(R\) Taylor compatibility screen。

本节 **ABSTRACT ONLY**：S.491 的 strictness 与 unbounded reverse ratio；S.492 中 listed ledger assumptions 不能推出 \(2/3\)-power bound。二者都不是 NSE counterexample。

继续 **OPEN**：direct moving-deletion hybrid gate；route-minimal fixed-deletion gate S.486；target-scale-equivalent simultaneous-height gate S.487；Step 17 positive-excursion gate S.472；terminal-crown coercivity S.407；Q.12、Q.1、scale contraction 与 regularity。**NOT CLAY.**

Python 主证书通过 5/5 exact finite groups、283,157 rational cases、5/5 structural groups 与 5/5 hash locks。独立 Ruby verifier 通过 8/8 groups、72,144 assertions；Python/Ruby 分别拒绝 12/12 与 13/13 intentional mutations；三组 Python hash seed 和一次跨工作目录 Ruby 重放均 byte-identical。

正式四联图的 25 文件档案通过 39 checks 与 verify-only。Panel A 是 proved inequalities 与 known-payment links 的精确 schematic；Panels B--D 是 exact abstract clocks。彩色、灰度与独立 PDF render 均完成视觉 QA。它不是 PDE data，不是 DNS，不是 NSE simulation，也不证明 OPEN S.486--S.487 或 Clay 问题。

route decision 已精确固定：后续 fixed-deletion 工作应直接研究 \(\mathfrak H^{\rm fix}\)，不应自动升级到更强的 \(\mathfrak O^{F,+}\)；completed-clock 工作可研究在已支付项后等价的 \(\mathfrak L^K\)；最弱有效路线仍是 terminal-dependent deletion set 的 direct Step 15 hybrid gate。本站在此停于冻结 Step 18，等待下一份明确冻结包。
