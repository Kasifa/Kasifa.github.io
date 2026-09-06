# 高高压力的 dyadic 输入—输出账本

2026-09-06。**INTERNAL / WORKING / NOT FROZEN / G OPEN / NOT CLAY。**

本稿继续 AR 的独立压力输出截断，检查剩余 \(p_h^{>L}\) 的可比输入与
分离输入。所有重排先在同一解的严格前奇点光滑紧时间区间进行；
不把静态频率矩写成已付的动态条件，也不提出新正则性准则或新颖性主张。

## 1. 固定分解与只可单向使用的能量账

沿用 AK 的平滑低通 \(S_Q=P_{\le Q}\)。固定速度输入阈值 \(K\ge1\)，令

\[
 Q_j=2^jK,\qquad
 v_j=(S_{2Q_j}-S_{Q_j})u,\qquad
 h=P_{>K}u=\sum_{j\ge0}v_j,
\tag{AS.1}
\]

其中

\[
 \operatorname{supp}\widehat v_j
 \subset\{k\in\mathbb Z^3:Q_j\le |k|\le4Q_j\}.
\tag{AS.2}
\]

记

\[
 m_j=\|v_j\|_2,\qquad g_j=\|\nabla v_j\|_2,\qquad
 b_j=Q_j^{3/2}m_j,\qquad g=\|\nabla u\|_2.
\tag{AS.3}
\]

固定乘子的有限重叠与 Plancherel 给

\[
 cQ_jm_j\le g_j\le CQ_jm_j,\qquad
 \sum_{j\ge0}m_j^2\le CM^2,\qquad
 \sum_{j\ge0}Q_j^2m_j^2\le Cg^2.
\tag{AS.4}
\]

最后一式只作这个方向使用；一般不能把它写成与全速度 \(g^2\) 双向等价。
下面出现的额外半阶矩为

\[
 \mathfrak C_K
 :=\sum_{j\ge0}b_j^2
 =\sum_{j\ge0}Q_j^3m_j^2.
\tag{AS.5}
\]

它在每个严格光滑紧时间区间内有限，但 AS.4 的能量账不控制它。

## 2. 原局部测试、坏时间与精确输入分组

仍用 AO--AQ 的原速度测试。写 \(q=|u|\)，

\[
 F_\chi=\chi q u,\qquad
 {\cal K}_\chi(p)=\int p\,\operatorname{div}F_\chi
 =-\int F_\chi\cdot\nabla p,
\tag{AS.6}
\]

并在 AQ 的实际窗口内记

\[
 \mu_J(\sigma)=
 \begin{cases}
  w_J(\sigma)\mathbf1_{B_K}(\sigma),&\sigma\in[s_J,t],\\
  0,&\sigma\in J\setminus[s_J,t],
 \end{cases}
 \qquad
 0\le\mu_J\le1.
\tag{AS.7}
\]

时间权重与坏集合指标只是空间常数；它们不改变下列 Fourier 支撑。
下列所有双和的指标 \(i,j\) 都属于 \(\mathbb Z_{\ge0}\)。在光滑闭区间上，
\(u\in C^\infty\) 使速度频率和及相应压力和在时间上一致快速收敛；
因此可先截断 \(i,j\le N\)，重排后令 \(N\to\infty\)，也可与有界时间权重
的积分交换。测试场 \(F_\chi=\chi|u|u\) 在这里仅需 \(C^1\)，不把它
误称为 \(C^\infty\)。由此得到精确分解

\[
 \begin{aligned}
 p(h)&=p_{\rm cmp}+p_{\rm sep},\\
 p_{\rm cmp}
 &=\sum_{|i-j|\le2}T_{ab}(v_{i,a}v_{j,b}),\\
 p_{\rm sep}
 &=\sum_{i<j-2}\Pi(v_i,v_j),
 \end{aligned}
\tag{AS.8}
\]

其中

\[
 T_{ab}=\partial_a\partial_b(-\Delta)^{-1},\qquad
 \Pi(a,b)=T_{ij}(a_i b_j+b_i a_j),\qquad \widehat T_{ab}(0)=0.
\tag{AS.9}
\]

AS.8 没有删除过渡带交互：有序可比对由第一重和覆盖，严格分离的两种
次序由对称的 \(\Pi\) 合并。

## 3. 输入频差决定哪些压力输出可能出现

若 \(i<j-2\)，则 \(Q_j\ge8Q_i\)。因此分离输入满足

\[
 \operatorname{supp}\widehat{\Pi(v_i,v_j)}
 \subset\left\{k:\frac12Q_j\le |k|\le\frac92Q_j\right\}.
\tag{AS.10}
\]

分离输入没有远低于较高输入的压力输出。相反，若 \(|i-j|\le2\)，
令 \(n=\max\{i,j\}\)，则只有上界

\[
 \operatorname{supp}\widehat{T_{ab}(v_{i,a}v_{j,b})}
 \subset\{k:|k|\le8Q_n\};
\tag{AS.11}
\]

输出可以是任意非零低频。高高到低输出只出现在这一可比分组中。

现在引入 AR 的独立压力输出阈值 \(L\ge1\)，它在每个窗口中固定，
但不要求 \(L=K\)。令

\[
 p_h^{\le L}=P_{\le L}p(h),\qquad
 p_h^{>L}=P_{>L}p(h).
\tag{AS.12}
\]

AR.6、AR.18--AR.19 已经证明，在同一坏集合和支撑化权重下

\[
 \frac1{H_t}\int_J
 \mu_J\left|{\cal K}_\chi(p_h^{\le L})\right|\,d\sigma
 \le e_J(L).
\tag{AS.13}
\]

因此只要 \(e_J(L)\to0\)，低输出压力功就是 \(o(1)\)；旧条件
\(L=o(\Lambda_A^{7/4})\) 仍是第一项预算给出的充分条件，而不是全部允许范围。
并且 AQ.8 的必要下界可原样转移到

\[
 \beta_K^{>L}={\cal K}_\chi(p_h^{>L})-\frac34D_\chi,\qquad
 \liminf\frac1{H_t}\int_{s_J}^t\mu_J\beta_K^{>L}\,d\sigma\ge1.
\tag{AS.14}
\]

由 AS.10--AS.11，若 \((9/2)Q_j\le L\)，则相应分离对被
\(P_{>L}\) 完全杀掉；若 \(8Q_n\le L\)，则相应可比对也被完全杀掉。
所以 AS.14 的压力部分精确列为

\[
 P_{>L}p(h)=P_{>L}p_{\rm cmp}+P_{>L}p_{\rm sep},
\tag{AS.15}
\]

其中第一项只需保留 \(Q_{\max(i,j)}>L/8\)，第二项只需保留
\(Q_j>2L/9\)。投影从未穿过空间截止 \(\chi\)。

## 4. 分离高高输入：有逆频率增益，但仍多半阶

因每个 \(v_i\) 无散，直接展开双散度得到

\[
 \begin{aligned}
 -\Delta\Pi(v_i,v_j)
 &=2(\partial_a v_{i,b})(\partial_bv_{j,a})\\
 &=2\partial_b\big((\partial_av_{i,b})v_{j,a}\big),
 \qquad i<j-2.
 \end{aligned}
\tag{AS.16}
\]

AS.10 允许在 \((-\Delta)^{-1}\partial_b\) 前插入一个固定的
\(Q_j\)-缩放光滑环带。其周期化核的 \(L^1\) 范数至多 \(CQ_j^{-1}\)，
故

\[
 \begin{aligned}
 \|\Pi(v_i,v_j)\|_\infty
 &\le CQ_j^{-1}\|\nabla v_i\|_\infty\|v_j\|_\infty,\\
 \|\nabla\Pi(v_i,v_j)\|_\infty
 &\le C\|\nabla v_i\|_\infty\|v_j\|_\infty.
 \end{aligned}
\tag{AS.17}
\]

第二行说明对压力再取一个输出导数后，\(Q_j^{-1}\) 增益恰好耗尽；
本稿后续使用保留该增益的第一行与完整散度配对。

Bernstein 给

\[
 \|\nabla v_i\|_\infty\le CQ_i^{5/2}m_i,\qquad
 \|v_j\|_\infty\le CQ_j^{3/2}m_j.
\tag{AS.18}
\]

结合 AS.17，得到准确的分离对成本

\[
 \|\Pi(v_i,v_j)\|_\infty
 \le C\frac{Q_i}{Q_j}b_i b_j.
\tag{AS.19}
\]

令

\[
 j_L=\min\{j\ge0:Q_j>2L/9\},\qquad
 \mathfrak S_{K,L}
 =\sum_{j\ge j_L}\sum_{i\le j-3}\frac{Q_i}{Q_j}b_i b_j.
\tag{AS.20}
\]

若内层为空则取零。因 \(Q_i/Q_j=2^{i-j}\)，序列 Young 或
\(2b_i b_j\le b_i^2+b_j^2\) 给

\[
 \begin{aligned}
 \mathfrak S_{K,L}
 &\le C\sum_{j\ge j_L}b_j^2
   +C\sum_{i<j_L}2^{\,i-j_L}b_i^2\\
 &\le C\mathfrak C_K.
 \end{aligned}
\tag{AS.21}
\]

这里第二和明确记录了低于 L、但与更高输入形成分离对的加权成本；
不能把它无条件删成纯高频尾。由于 \(P_{>L}=I-P_{\le L}\) 的平滑
低通核有统一 \(L^1\) 界，\(P_{>L}\) 在 \(L^\infty\) 上一致有界。
因此

\[
 \|P_{>L}p_{\rm sep}\|_\infty
 \le C\mathfrak S_{K,L}\le C\mathfrak C_K.
\tag{AS.22}
\]

AS.22 的最后一步来自平滑低通核，不是 \(L^\infty\) Riesz 有界性。

## 5. 可比高高输入：用 Fourier 系数，而非 \(L^\infty\) Riesz

取 \(|i-j|\le2\)、\(n=\max\{i,j\}\)。对每个 Fourier 系数，
空间 Cauchy--Schwarz 给

\[
 \left|\widehat{v_{i,a}v_{j,b}}(k)\right|
 \le C m_i m_j.
\tag{AS.23}
\]

压力乘子在 \(k\ne0\) 上绝对值至多 1。由 AS.11 的支撑球及格点计数，

\[
 \begin{aligned}
 \|T_{ab}(v_{i,a}v_{j,b})\|_\infty
 &\le C\sum_{0<|k|\le8Q_n}m_i m_j\\
 &\le CQ_n^3m_i m_j
 \le Cb_i b_j.
 \end{aligned}
\tag{AS.24}
\]

最后一步只用 \(Q_i,Q_j,Q_n\) 可比。这里没有调用错误的
\(L^\infty\) Riesz 有界性。再次使用平滑 \(P_{>L}\) 的统一
\(L^\infty\) 算子界，并由 AS.15 去掉不可能产生高输出的输入对，得到

\[
 \begin{aligned}
 \|P_{>L}p_{\rm cmp}\|_\infty
 &\le C\!\sum_{\substack{|i-j|\le2\\Q_{\max(i,j)}>L/8}}b_i b_j\\
 &\le C\sum_{Q_j>L/32}b_j^2.
 \end{aligned}
\tag{AS.25}
\]

定义完整剩余输入成本

\[
 \mathfrak R_{K,L}
 :=\mathfrak S_{K,L}+\sum_{Q_j>L/32}b_j^2.
\tag{AS.26}
\]

AS.22 与 AS.25 合并为

\[
 \|p_h^{>L}\|_\infty
 \le C\mathfrak R_{K,L}\le C\mathfrak C_K.
\tag{AS.27}
\]

独立的 L 已真实进入 AS.20、AS.25--AS.26；最后用
\(\mathfrak C_K\) 只是一个较粗的诊断上界。

## 6. 放回原测试和 AQ.8 的带符号账本

由无散性，

\[
 \operatorname{div}F_\chi
 =\chi u\cdot\nabla q+q u\cdot\nabla\chi.
\tag{AS.28}
\]

记 \(B_\chi=\int\chi q\)。空间 Cauchy--Schwarz、
\(B_\chi\le Cr^{3/2}M\) 及 \(\|\nabla\chi\|_\infty\le C/r\) 给

\[
 \|\operatorname{div}F_\chi\|_1
 \le Cr^{3/4}M^{1/2}D_\chi^{1/2}+Cr^{-1}M^2.
\tag{AS.29}
\]

所以 AS.27 对任意 \(\varepsilon>0\) 给出逐时估计

\[
 \begin{aligned}
 |{\cal K}_\chi(p_h^{>L})|
 &\le C\mathfrak R_{K,L}
       \big(r^{3/4}M^{1/2}D_\chi^{1/2}+r^{-1}M^2\big)\\
 &\le\varepsilon D_\chi
   +C_\varepsilon r^{3/2}M\mathfrak R_{K,L}^2
   +Cr^{-1}M^2\mathfrak R_{K,L}.
 \end{aligned}
\tag{AS.30}
\]

乘以 AS.7 的支撑化原权重并积分，得到

\[
 \begin{aligned}
 \int_{s_J}^t\mu_J|{\cal K}_\chi(p_h^{>L})|
 \le{}&\varepsilon\int_{s_J}^t\mu_JD_\chi\\
 &+C_\varepsilon r^{3/2}M
       \int_{s_J}^t\mu_J\mathfrak R_{K,L}^2\\
 &+Cr^{-1}M^2
       \int_{s_J}^t\mu_J\mathfrak R_{K,L}.
 \end{aligned}
\tag{AS.31}
\]

特别地，取 \(\varepsilon=1/4\)，保留坏时间耗散的真实符号，

\[
 \begin{aligned}
 \int_{s_J}^t\mu_J\beta_K^{>L}
 \le{}&-\frac12\int_{s_J}^t\mu_JD_\chi\\
 &+Cr^{3/2}M\int_{s_J}^t\mu_J\mathfrak R_{K,L}^2
 +Cr^{-1}M^2\int_{s_J}^t\mu_J\mathfrak R_{K,L}.
 \end{aligned}
\tag{AS.32}
\]

AR--AQ 给 AS.32 左侧除以 \(H_t\) 的下极限至少为 1。若不进一步利用
负耗散与右侧各项的关联，也不退回 AS.30 前保留带符号抵消，则从
AS.32 直接闭合的一组充分任务，是控制下列两项相对 \(H_t\) 的成本：

\[
 \int_{s_J}^t\mu_J\mathfrak R_{K,L}\,d\sigma,\qquad
 \int_{s_J}^t\mu_J\mathfrak R_{K,L}^2\,d\sigma.
\tag{AS.33}
\]

两项分别为小量不是实际 NS 的必要条件；它们的组合也可能由
AS.32 的负耗散吸收。现有能量只给 \(\int_Jg^2=A_J\)，没有直接
给出上述充分控制，不能把
\(\mathfrak R_{K,L}\) 或较粗的 \(\mathfrak C_K\) 当成已经获得的临界量。
输出高频本身也不再免费产生一个逆频率：把输出投影移到
\(\operatorname{div}F_\chi\) 只保留同一 \(L^1\) 界；若改为投到
\(F_\chi\)，压力梯度的输出频率会抵消所得的逆频率。

## 7. 为什么 AM 的成功不能在高高层重复

AM 的低输入 \(l=P_{\le K}u\) 有固定上限，故

\[
 \|\nabla l\|_\infty\le CMK^{5/2},\qquad
 \sum_jQ_j^{-1}\|w_j\|_\infty\le CK^{-1/2}g,\qquad
 \|p_{lh}\|_\infty\le CMK^2g.
\tag{AS.34}
\]

最后一项只含能量可积的 g。当前分离高高项中，“较低输入” \(v_i\)
仍可处在任意高频；同一个无散增益求和后成为 AS.20--AS.21，
而不是 \(MK^2g\)。这正是额外半阶的来源。

## 8. 静态能量层不能支付该频率矩

取固定整数 \(K\ge1\) 及 \(N\gg K\)，考虑零均值无散剪切

\[
 u_N(x)=\bigl(0,\sin x_1,N^{-1}\sin(Nx_1)\bigr).
\tag{AS.35}
\]

若 \(c_{\mathbb T}=\int_{\mathbb T^3}\sin^2x_1\,dx\)，则

\[
 \|u_N\|_2^2=c_{\mathbb T}(1+N^{-2}),\qquad
 \|\nabla u_N\|_2^2=2c_{\mathbb T},\qquad
 p(u_N)=0.
\tag{AS.36}
\]

频率 N 的分量至少落入有限个 \(Q_j\simeq N\) 的块中，而这些块的
乘子和为 1。有限重叠与 Cauchy--Schwarz 因而给

\[
 \mathfrak C_K(u_N)\ge cN\longrightarrow\infty.
\tag{AS.37}
\]

所以没有仅从瞬时统一的 \(L^2\) 与 \(H^1\) 上界控制
\(\mathfrak C_K\) 的估计。这个例子的压力恰为零；它不是 NS 压力功、
坏时间、成熟窗口或奇点反例，也不排除真实 NS 演化可能产生额外动态
控制。它只证明不能把 AS.5 的静态频率矩冒充现有能量预算。

## 9. 当前边界

AS.8--AS.15 是精确输入—输出清单；AS.16--AS.22 是分离高高的
真实无散增益；AS.23--AS.25 以 Fourier 系数和格点求和处理可比输入，
没有使用 \(L^\infty\) Riesz 有界性；AS.30--AS.33 保留了原
\(\chi|u|u\)、\(w_J\mathbf1_{B_K}\) 和 \(3D_\chi/4\) 的带符号账本。

结果没有给出 AQ.8 所需上界。沿当前绝对值账本，剩余问题是控制或
吸收 AS.33；另一条开放路线是在 AS.30 前利用动力学与带符号抵消。
不能把新增半阶量改名后作为已知假设。
固定半径到移动缩球合同 G、首次奇点排除和一般正则性均保持 OPEN。
本稿不含仿真、科学图、提交或发布动作。
