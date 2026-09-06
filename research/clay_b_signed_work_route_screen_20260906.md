# 原测试与高尾测试之间的带符号接口

2026-09-06。**INTERNAL / ROUTE SCREEN / PROVED IDENTITIES / TEST-CHANGE ROUTE CLOSED / NOT FROZEN / G OPEN / NOT CLAY。**

本稿只筛查 AQ.8 之后的一条路线：即使在同一固定环带和窗口内证明
局部高尾始终不小，当前估计是否给出坏时间净压力功的上界。以下推导
没有得到这样的上界；测试更换最终还原原身份的准确范围单独记录。

## 1. 局部尾下界只改变好坏集合（PROVED）

沿用 AO 的
\(\eta_K=\|\theta P_{>K}u\|_3\)、
\(G_K=\{\eta_K\le\eta_*\}\)、\(B_K=J\setminus G_K\)。若用的正是
AO 已认证的同一阈值，且

\[
 \eta_K(\sigma)>\eta_*\quad\hbox{对每个 }\sigma\in J,
 \qquad\Longrightarrow\qquad
 G_K=\varnothing,\quad B_K=J,\quad w_J\equiv1.
\tag{AV.1}
\]

若只有 \(\eta_K>c\) 且 \(c<\eta_*\)，则不能据此改写原来的 \(B_K\)；
至多可显式选取更小的已认证阈值并重跑 AO--AQ。AV.1 的
\(w_J=1\) 仅指其 \([s_J,t]\) 定义域。即便 AV.1 成立，AQ.8
也只是去掉坏集筛选，仍在 \([s_J,t]\) 上给必要的带符号下界；
没有扩成整个 J，更未产生上界。
尾的下界不控制压力梯度、压力功符号或相应时间乘积。

## 2. 原速度测试不能静默换成高尾测试（PROVED）

写 \(u=l+h\)，\(l=S_Ku\)，\(h=P_{>K}u\)，并令 \(F(v)=|v|v\)。定义
\({\cal K}_\chi^v(p_h)=-\int\chi F(v)\cdot\nabla p_h\)。则精确地

\[
 \begin{aligned}
 {\cal K}_\chi^u(p_h)&={\cal K}_\chi^h(p_h)+{\cal E}_\chi,\\
 {\cal E}_\chi
 &:=-\int\chi\,[F(u)-F(h)]\cdot\nabla p_h,\\
 F(u)-F(h)&=(|u|-|h|)h+|u|l.
 \end{aligned}
\tag{AV.2}
\]

本稿尚未给该缺陷确定的符号界。由
\(|F(u)-F(h)|\le C(|l||h|+|l|^2)\)、
\(\theta=1\) 于 \(\operatorname{supp}\chi\) 以及 Bernstein，

\[
 |{\cal E}_\chi|
 \le C\bigl(MK^{3/2}\eta_K+M^2K^2\bigr)
 \|\nabla p_h\|_{L^{3/2}(\operatorname{supp}\chi)}.
\tag{AV.3}
\]

AR.17 给 \(\|\nabla p_h\|_{3/2}\le Cg^2\)。因此纯 \(l^2\) 项在
\(K=\Lambda_A^{3/4}\)、\(H_t\ge\Lambda_A^3/3\) 下满足

\[
 \frac{M^2K^2}{H_t}\int_J g^2
 \le CM^2A_J\Lambda_A^{-3/2}\longrightarrow0.
\tag{AV.4}
\]

以下 \(\mu_J\) 沿用 AS.7，并且只在 \([s_J,t]\) 上使用。当前直接
范数估计留下的任务是

\[
 X_J:=\frac{MK^{3/2}}{H_t}
 \int_{s_J}^t\mu_J\eta_K
 \|\nabla p_h\|_{L^{3/2}(\operatorname{supp}\chi)}\,d\sigma.
\tag{AV.5}
\]

现有粗界 \(\eta_K\le\|h\|_3\le CK^{-1/2}g\) 只给

\[
 X_J\le \frac{CMK}{H_t}\int_{s_J}^t\mu_Jg^3\,d\sigma,
\tag{AV.6}
\]

而能量只控制 \(\int_Jg^2\)。局部尾下界不仅不能支付 AV.5，反而
出现在这个未付乘积中。未取绝对值的原对象应保留为带符号的
\(\int\mu_J{\cal E}_\chi\)，AV.5 仅是一条充分的范数控制路线。

## 3. 小能量差不能穿过任意坏集权重（PROVED BARRIER）

令
\(H_\chi(v)=\frac13\int\chi|v|^3\)。逐时有

\[
 |H_\chi(u)-H_\chi(h)|
 \le CM^3K^{3/2},\qquad
 \frac{|H_\chi(u)-H_\chi(h)|}{H_t}
 \le C\Lambda_A^{-15/8}.
\tag{AV.7}
\]

耗散差本身可由矩阵
\(A(v)=|v|I+v\otimes v/|v|\)（在零点取零）的 Lipschitz 性控制。
矩阵项 \(v\otimes v/|v|\) 本身可在零点连续补零；其在
\(v\ne0\) 的一阶导数一致有界，但一般不能在零点连续延拓。
沿线段积分，在线段穿过零点时分段，得到 \(A\) 全局 Lipschitz。
逐个空间方向写
\(D_\chi(v)=\sum_j\int\chi\,\partial_jv\cdot A(v)\partial_jv\)，则

\[
 \begin{aligned}
 D_\chi(u)-D_\chi(h)
 =\sum_j\int\chi\bigl\{&
 \partial_ju\cdot[A(u)-A(h)]\partial_ju\\
 &+2\partial_jh\cdot A(h)\partial_jl
 +\partial_jl\cdot A(h)\partial_jl\bigr\}.
 \end{aligned}
\]

第一项至多 \(C\|l\|_\infty g^2\)。后两项用
\(\|A(h)\|\le C|h|\)、Young、
\(\|\nabla l\|_\infty^2\|h\|_1\le CM^3K^5\)，得到

\[
 |D_\chi(u)-D_\chi(h)|
 \le \varepsilon D_\chi(h)
 +C_\varepsilon\bigl(MK^{3/2}g^2+M^3K^5\bigr).
\tag{AV.8}
\]

AV.8 的后两项在窗口积分并除以 \(H_t\) 后分别为
\(O(A_J\Lambda_A^{-15/8})\) 与 \(O(\Lambda_A^{-13/4})\)。
然而 AQ 使用 \(\mu_J=w_J\mathbf1_{B_K}\)。现有理论不给
\(\mathbf1_{B_K}\) 有界变差，故 AV.7 不能推出
\(\int\mu_J(H_\chi(u)-H_\chi(h))'\) 很小。

具体的纯静态警示是：取 \(a,T>0\)、正整数 N，在区间
\([s_0,s_0+T]\) 上令
\(E_N(s)=a\sin(2\pi N(s-s_0)/T)\)、
\(\mu_N=\mathbf1_{\{E_N'>0\}}\)。则端点均为零且
\(\|E_N\|_\infty=a\)，但

\[
 \int\mu_NE_N'=2aN.
\tag{AV.9}
\]

若另有 \(0\le\mu\le1\) 且 \(\mu\in BV\)，积分分部至多给
\(|\int\mu E'|\le\|E\|_\infty(2+\operatorname{TV}\mu)\)；
\(w_J\) 的绝对连续性不能供应 \(\mathbf1_{B_K}\) 的变差。
AV.9 不是 NS 或实际坏集反例，只排除“原函数一致小即可穿过任意
可测时间筛选”的错误步骤。若显式得到 AV.1，这一时间筛选障碍消失，
但仍不会自动得到压力功上界。

## 4. 测试更换仍还原原能量身份（PROVED）

在一个**显式证明为全坏**的窗口上，先不取绝对值，用
\(\chi|h|h\) 测试 AT.5 的精确高尾方程。若把全部低频、截止和投影
强迫记为保持符号的 \({\cal R}_h\)，则

\[
 (H_\chi(h))'+D_\chi(h)
 ={\cal K}_\chi^h(p_h)+{\cal R}_h,
\quad
 \beta_K=(H_\chi(h))'+\frac14D_\chi(h)
 +\left[{\cal E}_\chi-{\cal R}_h
 -\frac34\bigl(D_\chi(u)-D_\chi(h)\bigr)\right].
\tag{AV.10}
\]

这个方括号其实不再是新的开放项。令 \(S_\chi(u)\) 为 AB.2 中两个
非压力截止项，令 \(p_0,p_{lh}\) 沿用 AM.4，并定义
\({\cal R}_u=S_\chi(u)+{\cal K}_\chi^u(p_0+p_{lh})\)。原速度与高尾的
两条精确恒等式及其差为

\[
 \begin{gathered}
 H_\chi(u)'+D_\chi(u)={\cal K}_\chi^u(p_h)+{\cal R}_u,
 \qquad
 H_\chi(h)'+D_\chi(h)={\cal K}_\chi^h(p_h)+{\cal R}_h,\\
 E:=H_\chi(u)-H_\chi(h),\qquad
 E'={\cal E}_\chi+{\cal R}_u-{\cal R}_h
              -\bigl(D_\chi(u)-D_\chi(h)\bigr),\\
 {\cal E}_\chi-{\cal R}_h
 -\frac34\bigl(D_\chi(u)-D_\chi(h)\bigr)
 =E'+\frac14\bigl(D_\chi(u)-D_\chi(h)\bigr)-{\cal R}_u,\\
 \boxed{\quad
 \beta_K=H_\chi(u)'+\frac14D_\chi(u)-{\cal R}_u.
 \quad}
 \end{gathered}
\tag{AV.11}
\]

所以 AV.10 的测试更换经过精确消元后，只还原原来的局部三次能量
恒等式。若窗口已显式证明为全坏，则仅在 \([s_J,t]\) 上
\(\mu_J=1\)，它在此前仍为零。AV.7 使
\(\int_{s_J}^t E'=E(t)-E(s_J)\) 成为相对 \(H_t\) 可忽略的端点差；
AV.8 允许用任意小
耗散份额加 \(o(H_t)\) 支付耗散差。AM--AO 对 \({\cal R}_u\) 同样只给
任意小耗散份额及窗口积分为 \(o(H_t)\) 的固定截止/低频余项。
代回后留下的是高尾三次能量增长和正耗散，而不是 AQ 所需的上界。

这只关闭“把原测试换成高尾测试”这一操作，不是一般 NS 带符号方法的
不可能性结论。真正未付的仍是高尾自压力或三次能量增长的实际动态
上界/有利抵消；本文没有提供它。也不得把 AV.5 的充分范数条件称为
NS 必要条件。

本筛查不证明坏时间上界、成熟窗口闭合、合同 G、首次奇点排除或
Clay 正则性；不含仿真、图、提交或发布动作。
