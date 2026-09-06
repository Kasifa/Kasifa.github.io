# 从正变差得到持留窗口：下一项工作稿

2026-09-06。**WORKING / 内部工作稿 / 不属于 PhysicalAdjoint 冻结包。**
U.1--U.9 已完成实际文件独立解析审查；本工作线尚未形成新科学冻结。
只清理原 R 条件，不声称新的 NS 动力学闭合。G 仍 OPEN。

## 1. 沿用原时钟，不另造能量

完整重读 R0.74P 的 (2.6)--(3.6) 与 R0.74R 的 (R.200)--(R.217)。
固定 R、一个 local-energy good 终点 \(\tau\) 和壳 k，省略 k,R 下标。
原量为 \(K=E+D=Q+F\)，K、Q、F 取绝对连续代表；
D 是非减的累积**总耗散**，包括黏性耗散和局部能量缺陷。
这与上一节 B.5 单独记为 mu 的 defect 不同，不得混用。
\(K(s_R)=Q(s_R)=F(s_R)=0\)，E 和 D 在好时间与原能量定义一致。

在同一原移动坐标 \(v(t,y)=u(t,y+X_R(t))\) 中，记
\(a_R(t)=b_R(t,X_R(t))\)、\(e=|v|^2/2\)。
原有符号速率准确为

\[
\begin{split}
 Q'_k(t)&=\frac{\gamma_k}{R}\int
       [\eta'_R\Psi_k^R+\eta_R\Delta\Psi_k^R]e\,dy,\\
 F'_k(t)&=\frac{\gamma_k}{R}\int\eta_R
       [e(v-a_R)+(\pi-c_R)v]\cdot\nabla\Psi_k^R\,dy .
\end{split}
\tag{U.1}
\]

这里 a_R 是单个中心的速度，不是上一节伴随 PDE 中随 x 变化的 b_R。
压力 gauge 的空间积分可消去，但压力功整体不能删掉。
下文 \((F'_k)_+\) 是**整个有符号空间积分之后**的正部，
不是预先把每个空间项、压力或输运换成绝对值。

## 2. 任意单壳的正变差窗口

设 \(E(\tau)>0\)、\(h=K'\)。对几乎处处的好 \(t<\tau\)，

\[
 E(\tau)-E(t)
 =K(\tau)-K(t)-[D(\tau)-D(t)]
 \le\int_t^\tau h_+(r)\,dr .
\tag{U.2}
\]

定义
\[
 H_\tau(d)=\int_{\tau-d}^{\tau}h_+(r)\,dr,\qquad
 \delta_\tau=\max\{d\in[0,\tau-s_R]:H_\tau(d)\le E(\tau)/2\}.
\tag{U.3}
\]

L¹ 可积性给 H 连续、非减且 H(0)=0。
因为完整区间的正变差至少为 \(K(\tau)\ge E(\tau)\)，
\(0<\delta_\tau<\tau-s_R\)，并且 \(H_\tau(\delta_\tau)=E(\tau)/2\)。
允许 H 有平台，取满足条件的最大 d。
于是 \(J=(\tau-\delta_\tau,\tau)\) 满足

\[
 E(t)\ge E(\tau)/2\quad\hbox{a.e. }t\in J,\qquad
 \Theta(\tau;J)\ge\frac{\delta_\tau}{2^{3/2}R^2}.
\tag{U.4}
\]

该窗口不能覆盖一段 E=0 的初始 cutoff 区间。
若 \(E(\tau)=0\)，仍用原合同 \(\Theta=+\infty\)，不定义正阈值宽度。
这是原 R.204--R.206 的点态版本，逐壳 \(\delta_\tau>0\)
不意味着任何统一时间厚度或加权可求和性。

## 3. 先把已可支付的 Q 部分单独收费

设 \(VQ_k=\operatorname{TV}_{[s_R,\tau]}Q_k\)。
按原合同 \(\sum_k VQ_k\le C A_R\)，\(A_R=(P_R^M)^{2/3}\)。
所有非零终点时钟可分成下面三支：

1. \(D_k(\tau)\ge K_k(\tau)/2\)：耗散主导，原缺口仍在。
2. \(D_k(\tau)<K_k(\tau)/2\) 且 \(E_k(\tau)\le4VQ_k\)：
   此时 \(K_k(\tau)<2E_k(\tau)\le8VQ_k\)，
   可由 \(q_k=8VQ_k\) 支付，总误差仍为 \(C A_R\)。
3. \(D_k(\tau)<K_k(\tau)/2\) 且 \(E_k(\tau)>4VQ_k\)：
   需要真正的非线性持留控制，记这些壳为 \(\mathcal I_\tau\)。

零时钟可免费置 q=Lambda=0。
第二支如需完整代入 R.216，可取 Lambda=0；
E 终点为正时 (U.3)--(U.4) 保证能选到正 Theta 的区间，
避免写未约定的 \(0\cdot\infty\)。

对第三支，有

\[
 F_k(\tau)=K_k(\tau)-Q_k(\tau)
 \ge E_k(\tau)-VQ_k>\tfrac34E_k(\tau).
\tag{U.5}
\]

因此可以定义严格正的反向非线性阈值宽度

\[
 \delta^F_k=\max\left\{d\in[0,\tau-s_R]:
       \int_{\tau-d}^\tau(F'_k)_+(r)\,dr\le E_k(\tau)/4\right\}.
\tag{U.6}
\]

其严格短于全窗，积分在 d=delta 时等于阈值。
对 \(J_k=(\tau-\delta^F_k,\tau)\) 和几乎处处好 t，

\[
 E_k(\tau)-E_k(t)
 \le VQ_k+\int_t^\tau(F'_k)_+
 <E_k(\tau)/2 .
\tag{U.7}
\]

所以第三支可取 \(\Lambda_k=2,q_k=0\)，并有

\[
 \Theta_k(\tau;J_k)\ge 2^{-3/2}\delta^F_k/R^2.
\tag{U.8}
\]

若要凭这个下界闭合 R.217，一个**充分但尚未证明**的宽度条件是

\[
 \sum_{k\in\mathcal I_\tau}
     2^{3k}\gamma_k\left(\frac{R^2}{\delta^F_k}\right)^2\le C .
\tag{U.9}
\]

这会把第三支的 R.217 和控制在 64C；
不声称 (U.9) 对所有可能的持留集合 J 都是必要条件。
第一支还需另行支付或落入统一有限的例外集，
否则即便 (U.9) 成立也不能完成全部 R.216--R.217。

## 4. 下一项的准确边界

原先继承的正变差质量预算为
\(\sum_k\int(F'_k)_+\le\sum_k\operatorname{TV}F_k\le CP_R^M\)。
它不限制这些质量在时间上有多窄，不能单凭积分范数推出 (U.9)。
对真实 NS 能否有额外约束，本稿没有给否定例子。
这也是为何只把 (U.1) 取绝对值、套既有压力/三次估计不会补上缺口。

下一轮先检验一个具体问题：
在真实 NS 的 (U.1) 中，能否把过窄窗口的正工作与同尺度可观测的
耗散、回流或原匹配平方函数相连，同时保留压力和中心速度差？
需要的是控制过窄窗口**在所有壳上的联合权重**，
而不只是再次证明单个窗口存在。

冻结出口：若得到完整的新有符号不等式或明确的真实 NS 检验，
完成实际文件审查后再形成下一科学包。
本稿是继续研究的起点，不额外投递发布，不启动仿真或 DGX。
后续能量类时间可积性检验见
clay_b_signed_upcrossing_time_integrability_20260906.md；
它补充固定尺度定量宽度，不把 U.9 升级为已证。
