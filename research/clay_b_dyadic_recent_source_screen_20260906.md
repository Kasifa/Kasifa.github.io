# 近期源积分的 dyadic 近对角筛查

2026-09-06。**INTERNAL / PENDING REVIEW / NORM-ROUTE SCREEN / G OPEN / NOT CLAY。**

本稿只执行 recent-source-work 计划的一次有限筛查。BC 已把真正能与
BB 必要下界冲突的充分量定位为
\(H_t^{-1}\int\mu_JL_3\|\nabla R\|_2^4\)。这里对真实 Duhamel 源
逐个平滑环带保留 Leray 投影、空间散度与时间顺序，检查普通热核
平均和现有能量是否足以支付该量。

结论是：每个频带都能得到严格的近对角和时间卷积估计，但提高时间
可积性会留下正的频率权重。现有能量没有支付相应的 dyadic 源范数；
若退回 \(R=h-b\)，又正是 BC 已记录的更强 \(L_3g^4\) 成本。因此
这条绝对值/时间核路线在此停止。该结论不排除原带符号压力、相位或
负耗散之间尚未发现的抵消。

## 1. 固定对象和不能混用的时间能量

沿用 BC 的同一周期 NS 解、固定空间截止、坏集、权重与合法序列：

\[
 \begin{gathered}
 J=(t-\delta,t),\qquad
 \delta=c_0r^2\Lambda^{-4},\qquad
 K=\Lambda^{3/4},\qquad H_t=H_\chi(t)\ge\Lambda^3/3,\\
 \tau=\Lambda^{-8/3},\qquad a=t-\delta-\tau,\qquad
 \mu_J=w_J\mathbf1_{B_K}\quad\hbox{于 }[s_J,t],\\
 A_J=\int_Jg(s)^2\,ds,\qquad
 \widetilde A_J=\int_a^tg(s)^2\,ds,\qquad
 g(s)=\|\nabla u(s)\|_2 .
 \end{gathered}
\tag{BD.1}
\]

这里 \(0\le\mu_J\le1\)，\(A_J\to0\) 且
\(\widetilde A_J\to0\)，但没有
\(\widetilde A_J\le C A_J\) 或任何多项式速率。为缩短后面的式子，
记

\[
 {\cal E}_J:=M^2(\tau+\delta)+\widetilde A_J\longrightarrow0,
 \qquad M=\sup_{0<s<T_*}\|u(s)\|_2 .
\tag{BD.2}
\]

原必要下界仍是
\[
 \liminf\frac1{H_t}\int_{s_J}^t\mu_J
 \left[{\cal K}_\chi(p(R))-\frac58D_\chi\right]\,ds\ge1.
\]
BC 的这条绝对值路线只有在
\[
 {\cal Q}_J:=\frac1{H_t}\int_{s_J}^t
       \mu_JL_3\|\nabla R\|_2^4\,ds\longrightarrow0
\]
时才给出矛盾上界。本稿不改变这两个积分的下限、权重或剩余耗散。

令 \(F=u\otimes u\)。BC 的真实近期源积分是

\[
 R(s)=-\int_a^s e^{(s-v)\Delta}P_{>K}\mathbb P
                    \operatorname{div}F(v)\,dv,\qquad R(a)=0.
\tag{BD.3}
\]

BD.3 的 \(F\) 是完整原速度张量。若写
\(u=S_Ku+P_{>K}u\)，则低低、低高、高低和高高四类全部仍在 \(F\)
中；本稿不删除其中任何一类，也不把 \(R\) 当成独立 NS 解。

## 2. 非零平滑环带上的精确公式

取实偶 \(\psi\in C_c^\infty(\mathbb R^3\setminus\{0\})\)，支撑于
\(\{1/2\le|\xi|\le2\}\)，使相应 dyadic 分解具有有限重叠，并在
非零频率上构成单位分解。
对 \(N=2^j\ge1\)，记

\[
 \widehat{\Delta_Nf}(k)=\psi(k/N)\widehat f(k),\qquad
 R_N=\Delta_NR .
\tag{BD.4}
\]

另取稍宽的 \(\widetilde\Delta_N\)，其符号在
\(\operatorname{supp}\psi(k/N)\) 上等于一，并记
\(F_N=\widetilde\Delta_NF\)。因 \(R\) 带 \(P_{>K}\)，只有
\(N\gtrsim K\) 的环带可能非零。对 \(k\ne0\)，有精确公式

\[
 \begin{aligned}
 \widehat{R_{N,i}}(k,s)
 ={}&-\psi(k/N)m_K(k)
 \left(\delta_{i\ell}-\frac{k_i k_\ell}{|k|^2}\right)ik_j\\
 &\times\int_a^s e^{-|k|^2(s-v)}
              \widehat{F_{\ell j}}(k,v)\,dv,
 \qquad \widehat R_N(0,s)=0 .
 \end{aligned}
\tag{BD.5}
\]

这里 \(m_K=1-\varphi(k/K)\)。零模由环带、高通和散度共同删除；
BD.5 没有在 Leray 原点写未定义符号。严格前奇点光滑闭区间上，
可先截成有限模态再交换 \(v\) 积分与 Fourier 和，最后由一致快速
衰减取极限。

## 3. 两个可用的 block 算子范数

定义

\[
 {\cal T}_{N,\rho}A
 :=\nabla e^{\rho\Delta}\Delta_NP_{>K}\mathbb P
                    \operatorname{div}A,\qquad \rho>0 .
\tag{BD.6}
\]

环带上两次空间导数给 \(N^2\)，热因子给
\(e^{-cN^2\rho}\)。再用 \(L^{3/2}\to L^2\) Bernstein 的
\(N^{1/2}\) 因子，或直接留在 \(L^2\)，分别得到

\[
 \begin{aligned}
 \|{\cal T}_{N,\rho}A\|_2
 &\le C N^{5/2}e^{-cN^2\rho}\|A\|_{3/2},\\
 \|{\cal T}_{N,\rho}A\|_2
 &\le C N^2e^{-cN^2\rho}\|A\|_2 .
 \end{aligned}
\tag{BD.7}
\]

常数与 \(N,K,\rho\) 无关。证明可在稍宽环带先插入
\(\widetilde\Delta_N\)：缩放后的紧支撑光滑乘子核有一致 \(L^1\)
范数；Leray 符号因远离零模而光滑。即使 \(N\simeq K\) 穿过
\(m_K\) 的过渡带，Mikhlin 常数仍一致。故 BD.7 不是使用
Riesz 的 \(L^\infty\) 端点。

能量层对完整张量只给

\[
 \begin{aligned}
 \|F(s)\|_{3/2}
 &=\|u(s)\|_3^2\le CM(M+g(s)),\\
 \|F(s)\|_2
 &=\|u(s)\|_4^2\le CM^{1/2}(M+g(s))^{3/2}.
 \end{aligned}
\tag{BD.8}
\]

因此在 \(I_*=(a,t)\) 上，

\[
 \begin{aligned}
 \|F_N\|_{L^2(I_*;L^{3/2})}^2
 &\le CM^2{\cal E}_J,\\
 \|F_N\|_{L^{4/3}(I_*;L^2)}^{4/3}
 &\le CM^{2/3}{\cal E}_J .
 \end{aligned}
\tag{BD.9}
\]

每个 \(F_N\) 都可由完整 \(F\) 的右侧控制，但 BD.9 不提供带正
\(N\) 权重的可求和估计。

## 4. 扩散时间前后的完整近对角账本

固定常数 \(c_*>0\)，令

\[
 \ell_N=c_*N^{-2},\qquad
 v_N(s)=\max\{a,s-\ell_N\},
\tag{BD.10}
\]

并把 BD.3 分成

\[
 \begin{aligned}
 R_N^{\rm near}(s)
 &=-\int_{v_N(s)}^s e^{(s-v)\Delta}\Delta_NP_{>K}\mathbb P
                       \operatorname{div}F_N(v)\,dv,\\
 R_N^{\rm old}(s)
 &=-\int_a^{v_N(s)} e^{(s-v)\Delta}\Delta_NP_{>K}\mathbb P
                       \operatorname{div}F_N(v)\,dv .
 \end{aligned}
\tag{BD.11}
\]

第二个积分在 \(v_N(s)=a\) 时取零。对 BD.7 第一条的时间核作
Cauchy--Schwarz，使用
\(\int_0^{\ell_N}e^{-2cN^2\rho}d\rho\le CN^{-2}\)，得到

\[
 \begin{aligned}
 \|\nabla R_N^{\rm near}(s)\|_2
 &\le CN^{3/2}
 \left(\int_{(s-\ell_N,s)\cap I_*}
       \|F_N(v)\|_{3/2}^2\,dv\right)^{1/2},\\
 \|\nabla R_N^{\rm old}(s)\|_2
 &\le CN^{3/2}e^{-c'c_*}
       \|F_N\|_{L^2((a,s-\ell_N);L^{3/2})}.
 \end{aligned}
\tag{BD.12}
\]

对 BD.7 第二条改用时间 Hölder \(4\) 与 \(4/3\)，同样有

\[
 \begin{aligned}
 \|\nabla R_N^{\rm near}(s)\|_2
 &\le CN^{3/2}
 \left(\int_{(s-\ell_N,s)\cap I_*}
       \|F_N(v)\|_2^{4/3}\,dv\right)^{3/4},\\
 \|\nabla R_N^{\rm old}(s)\|_2
 &\le CN^{3/2}e^{-c'c_*}
       \|F_N\|_{L^{4/3}((a,s-\ell_N);L^2)}.
 \end{aligned}
\tag{BD.13}
\]

若 \(\ell_N\ge s-a\)，旧项为空，全部源都属于近对角项；否则
BD.12--BD.13 给出旧项。固定 \(c_*\) 只把旧项乘以一个固定小因子，
没有改善 \(N^{3/2}\) 的频率幂次。把 \(c_*\) 随 N 增长会变成另一
条频率依赖的对数切分，需重新核对全部时间成本，不属于本次检查。

对近项平方后再作时间 Fubini，BD.12 还给出

\[
 \int_J\|\nabla R_N^{\rm near}(s)\|_2^2\,ds
 \le C N^3\min\{\delta,\ell_N\}
       \|F_N\|_{L^2(I_*;L^{3/2})}^2 .
\tag{BD.14}
\]

这至多是
\(CN\|F_N\|_{L^2L^{3/2}}^2\)，仍损失一个正的 N。BD.13
也只给相同频率级别、但含
\(\|F_N\|_{L^{4/3}L^2}^2\) 的时间卷积界；它没有由
\({\cal E}_J=o(1)\) 自动产生可求和的小量。

## 5. 时间卷积提高可积性时的精确频率成本

把 \(F_N\) 延为 \(I_*\) 外的零。BD.7 第一条的时间核
\(N^{5/2}e^{-cN^2\rho}\mathbf1_{\rho>0}\) 的 \(L^1_\rho\)
范数为 \(CN^{1/2}\)。第二条时间核
\(N^2e^{-cN^2\rho}\mathbf1_{\rho>0}\) 的
\(L^{4/3}_\rho\) 范数也为 \(CN^{1/2}\)。Young 卷积不等式因此给

\[
 \begin{aligned}
 \|\nabla R_N\|_{L^2(I_*;L^2)}
 &\le CN^{1/2}
       \|F_N\|_{L^2(I_*;L^{3/2})},\\
 \|\nabla R_N\|_{L^2(I_*;L^2)}
 &\le CN^{1/2}
       \|F_N\|_{L^{4/3}(I_*;L^2)} .
 \end{aligned}
\tag{BD.15}
\]

所以逐块热平均只重获 \(L^2_tH^1_x\)，仍带 \(N^{1/2}\)。
BC.5 的无权全频结论反而来自精确恒等式 \(R=h-b\)，不能由
BD.15 对全体 N 作绝对求和重证。

BC 的充分量含 \(\|\nabla R\|_2^4\)。能量还给

\[
 \int_{I_*}L_3(s)^4\,ds\le CM^2{\cal E}_J.
\tag{BD.16}
\]

由时间 Hölder，

\[
 \int_{s_J}^t\mu_JL_3\|\nabla R\|_2^4
 \le \|L_3\|_{L^4(I_*)}
       \|\nabla R\|_{L^{16/3}(I_*;L^2)}^4 .
\tag{BD.17}
\]

要把 BD.7 第一条从 \(L^2_t\) 推到 \(L^{16/3}_t\)，Young 指数是
\(16/11\)，而

\[
 \|N^{5/2}e^{-cN^2\rho}\|_{L^{16/11}_\rho}
 =CN^{9/8}.
\]

第二条从 \(L^{4/3}_t\) 推到 \(L^{16/3}_t\) 时，Young 指数是
\(16/7\)，并且

\[
 \|N^2e^{-cN^2\rho}\|_{L^{16/7}_\rho}
 =CN^{9/8}.
\]

故两条严格的逐块估计是

\[
 \begin{aligned}
 \|\nabla R_N\|_{L^{16/3}(I_*;L^2)}
 &\le CN^{9/8}
       \|F_N\|_{L^2(I_*;L^{3/2})},\\
 \|\nabla R_N\|_{L^{16/3}(I_*;L^2)}
 &\le CN^{9/8}
       \|F_N\|_{L^{4/3}(I_*;L^2)} .
 \end{aligned}
\tag{BD.18}
\]

环带有限重叠及 \(16/3\ge2\) 表明，分别支付下列任一 Besov 型量
会充分控制 BD.17：

\[
 \begin{aligned}
 {\mathfrak X}_{3/2}^2
 &:=\sum_{N\gtrsim K}N^{9/4}
       \|F_N\|_{L^2(I_*;L^{3/2})}^2,\\
 {\mathfrak X}_{2}^2
 &:=\sum_{N\gtrsim K}N^{9/4}
       \|F_N\|_{L^{4/3}(I_*;L^2)}^2 .
 \end{aligned}
\tag{BD.19}
\]

但 BD.9 只有每块的无权能量上界；它不控制 BD.19 的正
\(9/8\) 阶频率矩。BD.19 若直接作为假设，只是给问题改名，并非
从现有能量得到的动力学收益。

即使只看单个环带并用 BD.9，BD.16--BD.18 至多给

\[
 \frac1{H_t}\int_JL_3\|\nabla R_N\|_2^4
 \le \frac{CN^{9/2}}{H_t}
 \min\left\{
 M^{9/2}{\cal E}_J^{9/4},
 M^{5/2}{\cal E}_J^{13/4}\right\}.
\tag{BD.20}
\]

在最低相关频率 \(N\simeq K=\Lambda^{3/4}\) 上，
\(N^{9/2}/H_t\lesssim\Lambda^{3/8}\)。虽然
\({\cal E}_J\to0\)，能量绝对连续性不给它抵消该正幂所需的速率；
更高环带还更差。因此 BD.20 也不是 BC.11 的已付上界。

## 6. 时间集中本身不能从 \(L^1\) 小量删除

BC.5 只给
\(\int_Jq_R=o(1)\)，其中 \(q_R=\|\nabla R\|_2^2\)。这个事实
在纯测度论层面不能推出
\(H_t^{-1}\int\mu_JL_3q_R^2=o(1)\)。例如令
\(H_n\to\infty\)、\(|J_n|=H_n^{-4/3}\)，在
\(J_n\) 内取集合 \(|E_n|=H_n^{-3}\)，并设

\[
 L_n=1,\qquad \mu_n=1,\qquad
 q_n=H_n^2\mathbf1_{E_n}.
\tag{BD.21}
\]

则

\[
 \int_{J_n}q_n=H_n^{-1}\longrightarrow0,\qquad
 \frac1{H_n}\int_{J_n}\mu_nL_nq_n^2=1.
\tag{BD.22}
\]

BD.21 只是非负标量时间函数，目的仅是反驳“\(L^1\) 小量自动给
归一化平方小量”这一推断。它不是无散速度、不是 NS 轨道，也不
否定真实源积分可能拥有额外带符号结构。

## 7. 本次筛查的停止结论

BD.5 保留了完整非线性源、Leray 投影、散度、零模和真实时间顺序。
BD.12--BD.18 说明固定扩散时间分拆与普通 Young 卷积确能提高每块
时间可积性，但代价是 \(N^{1/2}\) 或 \(N^{9/8}\) 的正频率权重。
现有能量不支付 BD.19；仅用每块全局上界也留下 BD.20 的未证速率。

所以这次 dyadic 绝对值/时间核检查没有控制 BC.11，也没有减少
AW、BC 已记录的开放假设。若下一步仍只提出 BD.19、时间上
\(\sup q_R\)、\(\int\mu_JL_3g^4\) 或
\(\widetilde A_J\) 的多项式速率，就应结束这一估计并复评问题选择，
不继续缩短滞后或细分同一账本。

本稿不排除 Fourier 相位、压力符号、无散收缩与剩余 \(5/8\)
耗散的联合抵消；它只排除上述具体的逐块绝对值推断。没有证明
源—源压力的能量上界，没有构造或排除奇点，也没有推进移动缩球
合同 G、一般正则性或 Clay 问题。不宣称新颖性；无仿真、DGX、
科学图、提交或发布。
