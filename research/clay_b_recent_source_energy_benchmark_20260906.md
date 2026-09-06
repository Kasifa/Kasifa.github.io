# 近期源自压力的能量验收基线

2026-09-06。**INTERNAL / PENDING REVIEW / ENERGY BENCHMARK / G OPEN / NOT CLAY。**

本稿只完成 recent-source-work 计划的第一项有限检查。BB 已经把旧热
压力移入一份明确耗散和 \(o(H_t)\) 余项，剩下从窗口前时刻开始生成
的真实源积分 \(R\)。我先列出 \(R\) 只由现有能量得到的窗口预算，
再给原压力测试的一条充分验收量。结论是：\(R\) 的积分 \(H^1\)
能量确实趋于零，但直接三角估计仍留下带额外 \(L^3\) 速度权重的
四次耗散成本。这里尚未开始 dyadic 或近对角源积分分析。

## 1. 同一窗口、同一源积分

完整沿用 BB 的同一周期 NS 解、固定环带、空间截止及合法大范数序列。
并保留成熟条件 \(t-\delta\ge c_mr^2>0\)。写

\[
 \begin{gathered}
 J=(t-\delta,t),\qquad
 \delta=c_0r^2\Lambda^{-4},\qquad
 K=\Lambda^{3/4},\qquad H_t=H_\chi(t)\ge\Lambda^3/3,\\
 A_J=\int_J g(s)^2\,ds\longrightarrow0,\qquad
 g(s)=\|\nabla u(s)\|_2,\qquad
 M=\sup_{0<s<T_*}\|u(s)\|_2 .
 \end{gathered}
\tag{BC.1}
\]

取 BB.22 的充分滞后

\[
 \tau=\Lambda^{-8/3},\qquad
 a=t-\delta-\tau,\qquad
 h=P_{>K}u,\qquad
 b(s)=e^{(s-a)\Delta}h(a),\qquad R=h-b .
\tag{BC.2}
\]

原方程还给出精确的

\[
 R(s)=-\int_a^s e^{(s-v)\Delta}P_{>K}\mathbb P
              \operatorname{div}(u\otimes u)(v)\,dv .
\]

所以 \(R\) 是从 \(a\) 开始、带完整 Leray 投影和空间散度的
非线性 Duhamel 源积分。原 AQ 的 \(s_J\)、坏集、权重
\(\mu_J=w_J\mathbf1_{B_K}\) 及积分域 \([s_J,t]\) 均不改变。
充分大时 \(0<a<t-\delta<s_J<t<T_*\)，且对 \(s\in J\)，
\(s-a\ge\tau\)。

## 2. \(R\) 的能量层窗口预算

平滑高通在 \(L^2\) 上为一致有界乘子，热半群也是 \(L^2\) 收缩，
所以

\[
 \sup_{s\in J}\|R(s)\|_2
 \le \sup_{s\in J}\bigl(\|h(s)\|_2+\|b(s)\|_2\bigr)
 \le C M .
\tag{BC.3}
\]

因 \(0\le1-\varphi\le1\)，有
\(\|\nabla h(s)\|_2\le g(s)\)。另一方面，令
\(\rho=s-a\ge\tau\)，逐模热估计给

\[
 \begin{aligned}
 \|\nabla b(s)\|_2^2
 &=V_{\mathbb T}\sum_k |k|^2e^{-2\rho|k|^2}
       |1-\varphi(k/K)|^2|\widehat u(a,k)|^2\\
 &\le \left(\sup_{x\ge0}x^2e^{-2\rho x^2}\right)\|u(a)\|_2^2
 \le \frac{C M^2}{\rho}\le\frac{CM^2}{\tau}.
 \end{aligned}
\tag{BC.4}
\]

由 \(R=h-b\) 和 \([s_J,t)\subset J\)；时间积分的单个终点为
零测度，不改变积分值。因此

\[
 \begin{aligned}
 \int_J\|\nabla R(s)\|_2^2\,ds
 &\le C A_J+C\int_J\|\nabla b(s)\|_2^2\,ds\\
 &\le C\left(A_J+M^2\frac{\delta}{\tau}\right)
 =C\left(A_J+c_0r^2M^2\Lambda^{-4/3}\right)
 \longrightarrow0 .
 \end{aligned}
\tag{BC.5}
\]

BC.5 是 \(J\) 上的真实能量小量，但不是逐时上界。若后续直接使用
Duhamel 源在整个 \([a,t]\) 上的耗散，必须另记

\[
 \widetilde A_J:=\int_a^t g(s)^2\,ds
 =A_J+\int_a^{t-\delta}g(s)^2\,ds\longrightarrow0.
\tag{BC.6}
\]

最后的收敛来自 \(g^2\in L^1(0,T_*)\) 和
\(|[a,t]|=\tau+\delta\to0\)。一般没有
\(\widetilde A_J\le C A_J\)，更没有二者的多项式速率比较；后续源项
估计不能把 \(\widetilde A_J\) 偷换成 \(A_J\)。

## 3. 原压力测试给出的一个充分验收量

记

\[
 q_R(s):=\|\nabla R(s)\|_2^2,\qquad
 L_3(s):=\|u(s)\|_{L^3(\mathbb T^3)},\qquad
 p_R=T_{ij}(R_iR_j),
\tag{BC.7}
\]

其中 \(p_R\) 取零均值。\(R\) 为零均值无散场；周期 Sobolev 与
双 Riesz 的有限 \(L^3\) 有界性给出

\[
 \|p_R(s)\|_3
 \le C\|R(s)\otimes R(s)\|_3
 =C\|R(s)\|_6^2
 \le C q_R(s).
\tag{BC.8}
\]

原测试仍是 \(F_\chi=\chi|u|u\)，并令
\(D_\chi=\int\chi|u|(|\nabla u|^2+|\nabla|u||^2)\)。由 BA.8--BA.9
的同一零集正则化和加权 Hölder，

\[
 \|g_\chi(s)\|_{3/2}
 =\|\operatorname{div}(\chi|u|u)\|_{3/2}
 \le L_3(s)^{1/2}D_\chi(s)^{1/2}
       +C_\chi L_3(s)^2 .
\tag{BC.9}
\]

因此对任意固定 \(0<\eta<5/8\)，有限指数 Hölder 和 Young
不等式给

\[
 \begin{aligned}
 |{\cal K}_\chi(p_R)|
 &\le Cq_RL_3^{1/2}D_\chi^{1/2}
       +C_\chi q_RL_3^2\\
 &\le \eta D_\chi
       +C_{\eta,\chi}\bigl(L_3q_R^2+L_3^3\bigr).
 \end{aligned}
\tag{BC.10}
\]

末步还使用了
\[
 L_3^2q_R\le\frac12L_3q_R^2+\frac12L_3^3,
\]
所以没有把空间截止项删掉。定义原权重下的充分方法预算

\[
 {\cal Q}_J
 :=\frac1{H_t}\int_{s_J}^t
       \mu_J(s)L_3(s)q_R(s)^2\,ds .
\tag{BC.11}
\]

BB.6 与 BC.1 已给

\[
 \frac1{H_t}\int_JL_3^3
 \le C_{M,r,c_0}
       \left(\Lambda^{-4}A_J^{3/4}+\Lambda^{-7}\right)
 \longrightarrow0.
\tag{BC.12}
\]

BB.25 在固定旧压力耗散份额 \(1/8\) 后留下

\[
 \liminf\frac1{H_t}\int_{s_J}^t\mu_J
       \left[{\cal K}_\chi(p_R)-\frac58D_\chi\right]\,ds\ge1.
\tag{BC.13}
\]

若能从实际 NS 源积分证明 \({\cal Q}_J\to0\)，则 BC.10--BC.12
反而给

\[
 \limsup\frac1{H_t}\int_{s_J}^t\mu_J
       \left[{\cal K}_\chi(p_R)-\frac58D_\chi\right]\,ds\le0,
\tag{BC.14}
\]

因为剩余的 \((5/8-\eta)D_\chi\) 非负。BC.14 与 BC.13 矛盾，
从而排除所假定的合法大范数序列。故 \({\cal Q}_J=o(1)\) 是这条
具体绝对值路线的一个充分成功判据；它不是 NS 解必须满足的必要条件，
也尚未由 BC.5 推出。

## 4. 直接代入 \(R=h-b\) 仍回到更强的未付成本

BC.4 及 \(\|\nabla h\|_2\le g\) 给

\[
 q_R\le C\left(g^2+\frac{M^2}{\tau}\right),\qquad
 q_R^2\le C\left(g^4+\frac{M^4}{\tau^2}\right).
\tag{BC.15}
\]

所以

\[
 {\cal Q}_J
 \le \frac{C}{H_t}\int_{s_J}^t
          \mu_J L_3g^4\,ds
 +\frac{CM^4\tau^{-2}}{H_t}\int_JL_3\,ds .
\tag{BC.16}
\]

BB.6 的 \(I_1\) 估计和
\(\tau^{-2}=\Lambda^{16/3}\) 精确给出

\[
 \begin{aligned}
 \frac{\tau^{-2}}{H_t}\int_JL_3
 &\le C_{M,r,c_0}\tau^{-2}
       \left(\Lambda^{-6}A_J^{1/4}+\Lambda^{-7}\right)\\
 &\le C_{M,r,c_0}
       \left(\Lambda^{-2/3}A_J^{1/4}
             +\Lambda^{-5/3}\right)
 \longrightarrow0 .
 \end{aligned}
\tag{BC.17}
\]

因此纯热梯度在 BC.16 中产生的部分已经由现有能量支付。直接三角
估计真正留下的是

\[
 \frac1{H_t}\int_{s_J}^t\mu_J(s)L_3(s)g(s)^4\,ds .
\tag{BC.18}
\]

AW 的既有充分成本是没有 \(L_3\) 权重的
\(H_t^{-1}\int\mu_Jg^4\)。这里 \(\mu_J\) 支持于 \(B_K\)，而
\(B_K\) 上
\[
 \eta_*<\|\theta h\|_3\le\|h\|_3\le C_\varphi L_3 .
\]
所以在同一权重上，BC.18 的小量性确实蕴含 AW 的无权
\(g^4\) 成本为小量。反向则没有依据，因为现有能量不给 \(L_3\)
的窗口一致上界。因此 BC.18 是这条直接路线中更苛刻、同样未付的
充分代价，不能称为与 AW 成本等价，更不能从 BC.5 的
\(L^1_t\) 小量推出。

## 5. 当前边界与下一检查

BC.3--BC.6 完成了近期源积分的能量基线，BC.10--BC.14 固定了
一个能真正与 BB.25 冲突的充分验收量。BC.15--BC.18 同时表明，
仅用 \(R=h-b\) 的三角不等式没有获得动力学收益，反而在未付的
\(g^4\) 上增加了 \(L_3\) 权重。

下一步若检查 dyadic 近对角源积分，必须直接减少 BC.18 的实际
时间集中成本，或给 BC.11 一个由同一解能量支付的不同上界。若只
返回 \(\sup_Jq_R\)、BC.18、\(\widetilde A_J\) 的未证多项式速率，
或把测试导数转给无 BV 的 \(\mu_J\)，就应按计划停止该估计，而不
继续相邻变体。

本稿没有证明 \({\cal Q}_J\to0\)，没有给出仅由现有能量支付的
源—源压力功上界，也没有构造或排除奇点。固定球到移动缩球合同 G、
一般正则性和 Clay 问题保持 OPEN；不宣称新颖性。本稿没有仿真、
DGX、科学图、提交或发布。
