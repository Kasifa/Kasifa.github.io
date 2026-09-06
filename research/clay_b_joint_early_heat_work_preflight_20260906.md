# 联合早时点与纯热压力功的窗口检查

2026-09-06。**INTERNAL / PENDING REVIEW / METHOD CHECK / G OPEN / NOT CLAY。**

本稿只检查 time-ordered-pressure-work 路线的两个有限步骤。第一步在
AQ 的同一窗口前半部选出一个同时控制局部立方能量和瞬时梯度的实际
时刻，并从该新起点重新推导 AQ.8 的积分因子。第二步只估计从这个
时刻自由热演化出的纯热—纯热压力项。结论仍留下
\(A_J^2\Lambda_A\) 的未付速率，也没有处理 Duhamel 交叉项或源—源项。

本稿完整使用 AQ 当前源的 AQ.1--AQ.8 与 AW 当前源的
AW.35--AW.44。它不把新时刻冒充 AQ 原来的 \(s_J\)，不增加早时小梯度、
临界范数、时间 BV 或方向持续假设。

## 1. 在前半窗口联合选择一个实际时刻

沿用 AO--AQ 的固定数据与合法大范数窗口。写

\[
 \begin{gathered}
 H=H_\chi,\qquad H_t=H(t),\qquad
 g(\sigma)=\|\nabla u(\sigma)\|_2,\qquad
 M=\sup_{0<\sigma<T_*}\|u(\sigma)\|_2,\\
 \delta=c_0r^2\Lambda_A^{-4},\qquad
 J=(t-\delta,t),\qquad
 A_J=\int_Jg(\sigma)^2\,d\sigma,\qquad
 S_J=A_J+M^2\delta .
 \end{gathered}
\tag{AZ.1}
\]

这里 \(H_t\ge\Lambda_A^3/3\)，且沿所考虑的合法序列
\(\Lambda_A\to\infty\)、\(\delta\to0\)、\(A_J\to0\)。AQ.3 可写成

\[
 X(\sigma):=\left(\frac{H(\sigma)}{H_t}\right)^{4/3},
 \qquad
 \int_JX(\sigma)\,d\sigma\le\delta C_0S_J,
 \qquad
 C_0=\frac{C_{\rm AQ}M^2}{c_0r^2}.
\tag{AZ.2}
\]

\(C_0\) 只依赖已经固定的数据。取窗口前半

\[
 E_J=(t-\delta,t-\delta/2),\qquad |E_J|=\delta/2,
\tag{AZ.3}
\]

并定义两个坏点集

\[
 N_H=\{\sigma\in E_J:X(\sigma)>8C_0S_J\},
 \qquad
 N_g=\{\sigma\in E_J:g(\sigma)^2>8A_J/\delta\}.
\tag{AZ.4}
\]

由 AZ.2、\(\int_{E_J}g^2\le A_J\) 和 Markov 不等式，

\[
 |N_H|\le\frac{\delta}{8},\qquad
 |N_g|\le\frac{\delta}{8},\qquad
 |E_J\setminus(N_H\cup N_g)|\ge\frac{\delta}{4}>0.
\tag{AZ.5}
\]

若某个积分为零，相应坏点集直接按零测集处理。所有时刻都位于严格
前奇点光滑区间；因此可从 AZ.5 的正测度集合中取一个实际点
\(a=a_J\in E_J\)，使

\[
 \boxed{\qquad
 \frac{H(a)}{H_t}\le
       [8C_0(A_J+M^2\delta)]^{3/4}=:\zeta_{J,a}\longrightarrow0,
 \qquad
 g(a)^2\le\frac{8A_J}{\delta}.
 \qquad}
\tag{AZ.6}
\]

第一条正是所需的联合早时低值；其中常数可记为
\(C_{M,r,c_0}(A_J+M^2\delta)^{3/4}\)。第二条只是平均尺度上界。
能量绝对连续性不推出 \(A_J/\delta\to0\)，所以 AZ.6 不能改写成
“\(g(a)\) 小”，也不说明 \(a\in G_K\)。

## 2. 必须从新时刻重建 AQ 的积分因子

保留 AO.18 的同一 \(G_K,B_K\)、同一个固定 \(K\)，以及

\[
 \beta_K={\cal K}_\chi(p_h)-\frac34D_\chi .
\tag{AZ.7}
\]

旧的 \(w_J\) 从 \(s_J\) 起算，不能原封不动用于以新 \(a\) 为
归一化起点的公式。在
\([a,t]\) 上重新定义

\[
 w_{J,a}(\sigma)
 =\exp\!\left(-C_{\cal S}
       \int_a^\sigma\mathbf1_{G_K}(\tau)\,d\tau\right),
 \qquad
 \mu_{J,a}=w_{J,a}\mathbf1_{B_K},
 \qquad e^{-C_{\cal S}\delta}\le w_{J,a}\le1.
\tag{AZ.8}
\]

若要把权重视为整个 \(J\) 上的函数，另约定
\(\mu_{J,a}=0\) 于 \(J\setminus[a,t]\)。将 AO.20 乘以
\(w_{J,a}\)，从 \(a\) 到 \(t\) 积分，得到

\[
 \begin{aligned}
 \int_a^t\mu_{J,a}\beta_K\,d\sigma
 \ge{}&w_{J,a}(t)(H_t+1)-(H(a)+1)\\
 &-\int_a^tw_{J,a}
       [f_K+C_{\cal S}(1+g^2)]\,d\sigma
 +\frac12\int_a^tw_{J,a}\mathbf1_{G_K}D_\chi\,d\sigma .
 \end{aligned}
\tag{AZ.9}
\]

AZ.9 是 AQ.8 从新起点的重新推导，不是对旧公式作符号替换。
由 \([a,t]\subset J\)、AZ.6、AO.19 的余项支付以及
\(e^{-C_{\cal S}\delta}\le w_{J,a}\le1\)，沿同一合法序列有

\[
 \boxed{\qquad
 \liminf_{\Lambda_A\to\infty}
 \frac1{H_t}\int_a^t\mu_{J,a}\beta_K\,d\sigma\ge1 .
 \qquad}
\tag{AZ.10}
\]

AQ.1--AQ.3、AO.20 和全窗 \(f_K,A_J\) 的支付没有改变；改变的是
早时点、积分下限、权重及其端点项。AZ.10 仍是条件于合法大范数序列
存在的必要下界，不是上界，也不产生这样的序列。

## 3. 从联合早时点作真实 Duhamel 分解

令 \(\mathbb P\) 是周期 Leray 投影，并写 \(h=P_{>K}u\)。在
\(a\le s\le t<T_*\) 上，真实 NS 方程给

\[
 \begin{aligned}
 h(s)&=b(s)+R(s),\\
 b(s)&=e^{(s-a)\Delta}h(a),\\
 R(s)&=-\int_a^s e^{(s-\tau)\Delta}
       P_{>K}\mathbb P\operatorname{div}(u\otimes u)(\tau)\,d\tau .
 \end{aligned}
\tag{AZ.11}
\]

所有乘子与热半群交换，且 \(b,R\) 都保持零均值和无散。高高压力的
二次性给出精确分组

\[
 p_h=T_{ij}(h_i h_j)
 =p_{bb}+p_{bR}+p_{RR},
 \quad
 \begin{cases}
 p_{bb}=T_{ij}(b_i b_j),\\
 p_{bR}=T_{ij}(b_iR_j+R_i b_j),\\
 p_{RR}=T_{ij}(R_iR_j).
 \end{cases}
\tag{AZ.12}
\]

下面只估计第一项。AZ.12 的后两项不能因 \(R(a)=0\) 被删除；它们是
下一步 time-ordered 检查中仍需处理的真实源项。

## 4. 原测试对纯热压力的半阶估计

固定一个 \(s\in[a,t]\)。仿照 AW.35，定义标量 Fourier 场

\[
 {\mathfrak a}_b(x,s)
 =\sum_{k\in\mathbb Z^3}|\widehat b(k,s)|e^{ik\cdot x}.
\tag{AZ.13}
\]

因为 \(b\) 实值且零均值，其系数实、偶、非负，并且
\(\widehat{\mathfrak a_b}(0)=0\)。Plancherel 与周期 Poincaré 给

\[
 \|{\mathfrak a}_b(s)\|_{H^1}
 =\|b(s)\|_{H^1}
 \le C\|\nabla b(s)\|_2.
\tag{AZ.14}
\]

令 \(\Gamma\) 是 AW.16 的无散方向因子，并在零输入或零输出处按
AW.16 后的约定取零。收集同一压力输出的绝对系数，

\[
 Z_b(\kappa,s)
 =\sum_{\xi+\eta=\kappa}
   \Gamma(\xi,\eta)
   |\widehat b(\xi,s)|\,|\widehat b(\eta,s)|,
 \quad \kappa\ne0,\qquad Z_b(0,s)=0.
\tag{AZ.15}
\]

由于 \(0\le\Gamma\le1\) 且
\(\widehat{{\mathfrak a}_b^2}(\kappa)\ge0\)，AW.38--AW.41 的
逐系数比较和周期
\(W^{1,3/2}\hookrightarrow H^{1/2}\) 给

\[
 \|{\cal Z}_b(s)\|_{\dot H^{1/2}}
 \le\|{\mathfrak a}_b(s)^2\|_{\dot H^{1/2}}
 \le C\|\nabla b(s)\|_2^2,
 \quad
 {\cal Z}_b=\sum_\kappa Z_b(\kappa)e^{i\kappa\cdot x}.
\tag{AZ.16}
\]

最终测试仍是同一时刻的真实
\(F_\chi(s)=\chi|u(s)|u(s)\)，不是由 \(b\) 替换的测试。AW.42 给

\[
 \|F_\chi(s)\|_{\dot H^{1/2}}
 \le C_\chi(M+g(s))^2.
\tag{AZ.17}
\]

将 AZ.16--AZ.17 放入 AW.43 的加权 Fourier
Cauchy--Schwarz，得到

\[
 \boxed{\qquad
 |{\cal K}_\chi(p_{bb})(s)|
 \le C_\chi\|\nabla b(s)\|_2^2(M+g(s))^2
 \le C_\chi\|\nabla b(s)\|_2^2(M^2+g(s)^2).
 \qquad}
\tag{AZ.18}
\]

这里保留了原来的非线性测试；AZ.18 不是把 \(F_\chi\) 换成
\(\chi|b|b\) 后得到的另一条能量恒等式。

## 5. 热能量积分与剩余速率

自由热流满足

\[
 \frac12\frac{d}{ds}\|b(s)\|_2^2+\|\nabla b(s)\|_2^2=0,
 \qquad
 \int_a^t\|\nabla b(s)\|_2^2\,ds
 \le\frac12\|h(a)\|_2^2\le\frac12M^2.
\tag{AZ.19}
\]

热半群的梯度收缩、\(0\le1-\varphi\le1\) 及 AZ.6 又给

\[
 \sup_{a\le s\le t}\|\nabla b(s)\|_2^2
 \le\|\nabla h(a)\|_2^2
 \le g(a)^2
 \le\frac{8A_J}{\delta}.
\tag{AZ.20}
\]

由 \(0\le\mu_{J,a}\le1\)、\(\int_a^tg^2\le A_J\)，
AZ.18--AZ.20 合并为

\[
 \begin{aligned}
 \int_a^t\mu_{J,a}|{\cal K}_\chi(p_{bb})|\,ds
 &\le C_\chi\left[
 M^2\int_a^t\|\nabla b\|_2^2
 +\left(\sup_{[a,t]}\|\nabla b\|_2^2\right)
     \int_a^tg^2\right]\\
 &\le C_\chi\left(M^4+\frac{A_J^2}{\delta}\right).
 \end{aligned}
\tag{AZ.21}
\]

若把一份尚未另处分配的耗散份额 \(0\le\vartheta\le3/4\) 留在该项，
则同样有

\[
 \int_a^t\mu_{J,a}
       [{\cal K}_\chi(p_{bb})-\vartheta D_\chi]\,ds
 \le-\vartheta\int_a^t\mu_{J,a}D_\chi\,ds
    +C_\chi\left(M^4+\frac{A_J^2}{\delta}\right).
\tag{AZ.22}
\]

这不允许在 \(p_{bR}\) 或 \(p_{RR}\) 中再次使用同一份耗散。
它只是对纯热压力项的一条充分绝对估计，不是 AZ.10 左侧总净工作的
必要结构。

最后除以 \(H_t\)，并用
\(\delta=c_0r^2\Lambda_A^{-4}\)、\(H_t\ge\Lambda_A^3/3\)，得到

\[
 \boxed{\qquad
 \frac1{H_t}\int_a^t\mu_{J,a}
       |{\cal K}_\chi(p_{bb})|\,ds
 \le C_\chi\left(\frac{M^4}{H_t}
                 +\frac{A_J^2}{\delta H_t}\right)
 \le C_{\chi,c_0,r}
       \left(M^4\Lambda_A^{-3}+A_J^2\Lambda_A\right).
 \qquad}
\tag{AZ.23}
\]

第一项趋零。现有能量绝对连续性只有 \(A_J=o(1)\)，并不推出
\(A_J^2\Lambda_A=o(1)\)。因此联合选择确实把 AW.44 的纯热部分
变成一个明确速率缺口，但尚未支付它。

## 6. 方法结论与停止边界

AZ.5--AZ.10 证明：不增加假设也能在同一窗口前半选到一个兼具
早时局部能量低值与平均尺度梯度上界的实际起点，并合法重建 AQ 的
带权必要下界。这个改进不提供 \(g(a)\) 的绝对小性。

AZ.18--AZ.23 证明：纯热—纯热压力项不再需要整个窗口的
\(\int g^4\)，但直接估计留下 \(A_J^2\Lambda_A\)。这只是当前
半阶配对加热能量收缩给出的充分成本，不宣称该速率必要或最优。
负耗散、未取绝对值的相位和频率抵消仍可能改善总账。

本稿没有支付 AZ.12 的初始—源或源—源压力，没有形成 AZ.10 的上界，
也没有把自由热分量当成一条独立 NS 解。若后续两类 Duhamel 配对仍
返回同一速率、AW 的 \(g^4\) 或 AV 的原能量恒等式，应记录具体等价
并停止这一估计，而不能升级为所有动态机制的不可能性结论。

所有结论只在同一固定环带、严格前奇点光滑窗口及原 \(F_\chi\) 下成立。
本稿不构造 NS 轨道或奇点反例，不改变合同 G，不宣称新颖性，也不需要
仿真、DGX、科学图、提交或发布。
