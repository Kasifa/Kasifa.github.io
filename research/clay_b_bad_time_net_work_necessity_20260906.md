# 大终端局部范数迫使坏时间承担净压力工作

2026-09-06。**INTERNAL / WORKING / NECESSARY CONDITION / G OPEN / NOT CLAY。**

本稿沿用 AO 的全部固定设置，以及 AP 为同一 suitable continuation
选择的固定有界环带。它不假定坏时间净工作很小；相反，检验若出现
大的终端局部范数，能量与 AO 的预算会对这一项强制提出什么要求。
这不是新的正则性定理，也不宣称新颖性。

## 1. 同一解的早时低值

取 AO.17 的合法窗口，写 \(H=H_\chi\)、\(H_t=H(t)\)，
\(L(\sigma)=\|u(\sigma)\|_{L^3(\mathbb T^3)}\)。
\(0\le\chi\le1\) 及能量插值给

\[
 H(\sigma)^{4/3}\le C L(\sigma)^4
 \le CM^2\bigl(g(\sigma)^2+M^2\bigr).
\tag{AQ.1}
\]

这正是 AN.21 的非齐次周期版本。积分后，

\[
 \int_J H(\sigma)^{4/3}\,d\sigma
 \le CM^2(A_J+M^2\delta).
\tag{AQ.2}
\]

由 \(H_t\ge\Lambda_A^3/3\)、\(\delta=c_0r^2\Lambda_A^{-4}\)，

\[
 \frac{1}{\delta}\int_J
       \left(\frac{H(\sigma)}{H_t}\right)^{4/3}d\sigma
 \le \frac{CM^2}{c_0r^2}(A_J+M^2\delta).
\tag{AQ.3}
\]

因此存在 \(s_J\in J\) 满足

\[
 \frac{H(s_J)}{H_t}\le\zeta_J,
 \qquad
 \zeta_J:=C\left[\frac{M^2}{c_0r^2}(A_J+M^2\delta)\right]^{3/4}
 \longrightarrow0.
\tag{AQ.4}
\]

例如在平均值的两倍以内选一点并把固定因子并入 C 即可。
\(s_J\) 是同一个完整窗口中的实际早时点，不要求它属于好集合。
光滑性保证可在所用时间代表上取值。极限始终针对固定 M、r、\(c_0\)
且 \(\Lambda_A\to\infty\) 的合法序列；由 \(g^2\in L^1\)
得到 \(A_J\to0\)，不需要额外多项式衰减率。

## 2. 坏时间正净工作至少为终端量级

AO.22 对 \(s=s_J\) 给

\[
 \begin{aligned}
 \frac{\mathcal B_J}{H_t}
 \ge{}&e^{-C_{\cal S}\delta}(1+H_t^{-1})
       -\zeta_J-H_t^{-1}\\
 &-\frac{\int_J f_K+C_{\cal S}(\delta+A_J)}{H_t}.
 \end{aligned}
\tag{AQ.5}
\]

AM 的余项估计与 AO.19 使最后一行趋零，\(H_t\to\infty\)、
\(\delta\to0\)。所以沿每个这样的序列，有准确的必要条件

\[
 \boxed{\qquad
 \liminf\frac{\mathcal B_J}{H_t}\ge1,\qquad
 \mathcal B_J=
 \int_{B_K}\left[{\cal K}_\chi(p_h)-\tfrac34D_\chi\right]_+\,d\sigma.
 \qquad}
\tag{AQ.6}
\]

这是一个由方程预算推出的下界，不是对 \(\mathcal B_J\) 的上界。
它说明在候选大范数序列上，不能期待仅凭已用过的能量恒等式
自动证明 \(\mathcal B_J=o(H_t)\)。若用额外的实际 NS 结构得到该上界，
才会与 AQ.6 矛盾并排除该序列。

## 3. 更精确的带权符号版本

为说明 AQ.6 不是凭空引入压力绝对值，设

\[
 w_J(\sigma)=\exp\!\left(-C_{\cal S}
          \int_{s_J}^{\sigma}\mathbf1_{G_K}(a)\,da\right),
 \qquad
 \beta_K={\cal K}_\chi(p_h)-\tfrac34D_\chi.
\tag{AQ.7}
\]

直接对 AO.20 使用该积分因子，得到

\[
 \begin{aligned}
 \int_{s_J}^{t}w_J\mathbf1_{B_K}\beta_K
 \ge{}&w_J(t)(H_t+1)-(H(s_J)+1)\\
 &-\int_{s_J}^{t}w_J\bigl[f_K+C_{\cal S}(1+g^2)\bigr]
   +\tfrac12\int_{s_J}^{t}w_J\mathbf1_{G_K}D_\chi.
 \end{aligned}
\tag{AQ.8}
\]

利用 AQ.4、\(e^{-C_{\cal S}\delta}\le w_J\le1\) 和余项支付，
AQ.8 左侧除以 \(H_t\) 的下极限也至少为 1。
因此是一个实际带符号坏时间配对迫使 AO.21 的正部预算达到该量级。
由于未控制 \(\int_{B_K}|\beta_K|\)，即便 \(w_J\to1\) 一致，
也不能将 AQ.8 中的权重免费删去。

## 4. 对下一步的限制

固定环带选择和好时间局部化已不再是缺口。
现在要寻找的是能否利用尚未使用的动力学或符号信息，限制 AQ.8
中的高高压力净工作；仅改进坏集合测度的常数不足以完成这一点。
AO.21 的 \(3/4\) 是既定吸收份额，不是被证明最佳的普适常数。

AQ.6 不断言存在任何奇点或实际大范数序列，不证明奇点不可能，
也不把固定球的条件必要机制替换成合同 G 的移动缩球结论。
若上述序列并不存在，必要条件当然不产生一个新的存在性结论。
本稿仅作内部解析记录，尚未形成发布冻结包，无仿真或科学图。
