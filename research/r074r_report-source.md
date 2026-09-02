# R0.74R｜窗口质量被迫收缩到第一壳层；任意终端时钟还差什么？

## 导语

这一节仍然没有解决三维 Navier--Stokes 千禧年问题。

R0.74Q 留下了一个很具体的固定尺度问题：怎样把所有壳层的有符号累计
通量，压到完整支付量的 \(2/3\) 次幂与壳层时钟平方函数之和？记

\[
 A_R:=(P_R^M)^{2/3},
 \qquad
 Z_R:=Y_{2,R}^{\rm sf},
\]

目标仍是

\[
 \boxed{
 \mathfrak C_R^M
 \stackrel{?}{\le}
 C\bigl[A_R+Z_R\bigr].}
\]

R0.74Q 已经证明，想用很多等强度光滑包同时点亮许多壳层，外部速度三次
支付会先爆掉。但那个结论仍依赖 equal-target 设计。R0.74R 做了两件更
基础的工作。

第一，我把“等强度目标”完全拿掉。只要质量确实在同一个终端时间窗口的
那些目标 lobe 中出现，任意非负质量分布都会受到一个显式凸性约束：若
支付不大，几乎全部质量必须指数级地收缩到第一目标壳层。

第二，我回到任意 defect-completed clock，精确拆出从“终端时钟很大”到
“终端窗口中有质量”的缺口。这个缺口不再是一句话，而是两个可检验的
因子：时钟必须能被端点动能近似；端点动能必须有足够的时间厚度。若这
两个因子具有正确的壳层加权可和性，固定尺度问题就闭合。

但我也证明了：只靠时钟代数、不可压条件和 Hölder 不等式，无法推出这
两个因子。大时钟可能主要是累计耗散；端点动能可以只活在极薄时间片；
固定梯度耗散也不能由速度三次量反向支付。真正剩下的是 Navier--Stokes
动力学问题，不是序列技巧。

**这一节的状态是：窗口情形 PROVED；任意时钟的充分条件 PROVED；充分
条件本身 OPEN。NOT CLAY.**

本节没有使用数值仿真或 DGX。

## 1. 先去掉 equal-target 假设

沿用 R0.74Q 的冻结参数

\[
 \lambda=\frac{63}{32},
 \qquad
 \rho=\frac1{320},
 \qquad
 c_\gamma=\frac8{3969},
\]

并令

\[
 L=\lambda2^j,
 \qquad
 R=e^{-\rho L^2},
 \qquad
 N=j,
\]

\[
 L_\ell=2^{\ell-1}L,
 \qquad
 k_\ell=j+\ell-1,
 \qquad
 \Gamma_\ell=e^{-c_\gamma L_\ell^2}.
\]

所有正 lobe 共用终端窗口

\[
 J=(65R^2-R^3,65R^2),
 \qquad |J|=R^3.
\]

我不再规定每个包的振幅，也不再假设各壳层目标相等。直接用真实总速度
\(u\) 定义第 \(\ell\) 个窗口平均质量

\[
 E_\ell
 :=\frac{\Gamma_\ell}{2R|J|}
   \int_J\int_{\Omega_{\ell,+}(t)}|u(t,x)|^2\,dx\,dt.
\]

再记

\[
 S:=\sum_{\ell=1}^NE_\ell,
 \qquad
 Q:=\left(\sum_{\ell=1}^NE_\ell^2\right)^{1/2},
 \qquad
 U:=\sum_{\ell=2}^NE_\ell=S-E_1.
\]

因为 completed clock 的其余部分非负，且各目标 lobe 位于不同壳层，

\[
 v_{k_\ell,R}\ge E_\ell,
 \qquad
 Y_{2,R}^{\rm sf}\ge Q.
\]

这里不要求各壳层在同一时刻取得最大值。每个 \(v_{k_\ell,R}\) 可以在
自己的时刻实现下界；平方函数只需要这些逐坐标下界。

## 2. 三次支付先相加，再体现凸性

R0.74Q 的 doubled-radius 权重给出

\[
 \gamma_{k_\ell-1}=\Gamma_\ell^{1/4}.
\]

把完整 Version-M 支付中的非负外部速度三次项，限制到所有互不相交的
lobe cylinder，再用时空 Hölder，得到

\[
 \boxed{
 P_R^M
 \ge2\sqrt2\,R
 \sum_{\ell=1}^N
 \Gamma_\ell^{-5/4}L_\ell^{-1/2}E_\ell^{3/2}.}
\]

关键是次序：先在每个不相交 lobe 上得到真实非负下界，再求和；我没有
假设完整非线性支付对各包可加。

令

\[
 d_\ell:=\Gamma_\ell^{-5/4}L_\ell^{-1/2}.
\]

加权 Hölder 给出

\[
 \sum_{\ell\in I}d_\ell E_\ell^{3/2}
 \ge
 \frac{(\sum_{\ell\in I}E_\ell)^{3/2}}
      {(\sum_{\ell\in I}d_\ell^{-2})^{1/2}}.
\]

其等号分布恰好是

\[
 E_\ell\propto d_\ell^{-2}
 =\Gamma_\ell^{5/2}L_\ell.
\]

这些倒数权重从第二壳层开始快速几何衰减。精确计算后，

\[
 \boxed{
 (P_R^M)^{2/3}
 \ge
 2^{2/3}(2L)^{-1/3}e^{\kappa_2L^2}U,}
\]

其中

\[
 \kappa_2
 =\frac{10}{3}c_\gamma-\frac23\rho
 =\frac{8831}{1905120}>0.
\]

因此，只要 \(S>0\) 且

\[
 (P_R^M)^{2/3}\le MS,
\]

就有

\[
 \boxed{
 \frac US
 \le
 2^{-2/3}M(2L)^{1/3}e^{-\kappa_2L^2}.}
\]

更直观地，若

\[
 \mathbf E=(E_1,\ldots,E_N),
 \qquad
 \mathbf e_1=(1,0,\ldots,0),
\]

那么

\[
 \left\|\frac{\mathbf E}{S}-\mathbf e_1\right\|_{\ell^1}
 \le
 2^{1/3}M(2L)^{1/3}e^{-\kappa_2L^2}.
\]

这比“质量只能近似 rank one”更具体：在冻结几何里，低支付不仅要求
集中到某一壳层，而且要求集中到第一目标壳层。第二层以后的总质量受到
显式指数压制。

## 3. 它怎样关闭原来的反例路线

若一个终端窗口构型想反驳固定尺度不等式，并且未来还能证明其有符号通量
与 \(S\) 可比，那么至少需要同时满足

\[
 (P_R^M)^{2/3}=o(S),
 \qquad
 Y_{2,R}^{\rm sf}=o(S).
\]

第二个关系连同 \(Y_{2,R}^{\rm sf}\ge Q\) 迫使 \(E_1=o(S)\)；第一个关系
连同上面的支付定理迫使 \(U=o(S)\)。但 \(S=E_1+U\)，矛盾。

所以，在继承的终端窗口与 lobe 几何中，无论怎样重新分配非负目标质量，
“小支付 + 小平方函数”都不能同时发生。equal-target 并不是 R0.74Q
失败的偶然原因；真正的原因是权重与三次凸性共同造成的第一壳层稳定性。

这仍然只是路线封闭，不是固定尺度不等式本身。一个任意的大 completed
clock 不一定在这个终端窗口里含有动能质量。

## 4. 任意 completed clock 的精确三分法

在 R0.74P 的 suitable-weak chart 中，每个壳层时钟都分解为

\[
 K_{k,R}=E_{k,R}+D_{k,R}=Q_{k,R}+F_{k,R}.
\]

\(E\) 是端点局部动能，\(D\) 是从起始时刻累计的非负黏性与缺陷耗散，
\(Q\) 是二次源项原函数，\(F\) 是有符号通量原函数。\(D\) 单调不减，
\(K(s_R)=0\)，且 \(K\ge0\)。继承的绝对账本给出

\[
 \sum_k\operatorname{TV}Q_{k,R}\le C(P_R^M)^{2/3},
 \qquad
 \sum_k\operatorname{TV}F_{k,R}\le CP_R^M.
\]

取任意好终端时刻 \(\tau\in(s_R,t_0)\) 和先前区间
\(J=(a,\tau)\subset(s_R,t_0)\)。把正变差明确地
取到终端值 \(K(\tau)\)，单调性立即给出

\[
 E_{k,R}(\tau)
 \le
 \fint_JE_{k,R}(t)\,dt
 +\operatorname{Var}^{+}_{J\rightsquigarrow\tau}K_{k,R}.
\]

并且

\[
 \operatorname{Var}^{+}_{J\rightsquigarrow\tau}K_{k,R}
 \le
 \operatorname{TV}_{J\rightsquigarrow\tau}Q_{k,R}
 +\operatorname{TV}_{J\rightsquigarrow\tau}F_{k,R}.
\]

令 \(T=K_{k,R}(\tau)\)。至少有一个分支成立：

\[
 \boxed{
 D_{k,R}(\tau)\ge\frac T2,}
\]

或者

\[
 \boxed{
 \fint_JE_{k,R}(t)\,dt\ge\frac T4,}
\]

或者

\[
 \boxed{
 \operatorname{TV}_{J\rightsquigarrow\tau}Q_{k,R}
 +\operatorname{TV}_{J\rightsquigarrow\tau}F_{k,R}
 \ge\frac T4.}
\]

这三个分支分别是：累计耗散、真实窗口动能、最近的正向跳升。它完整地
说明了为什么“时钟很大”不能直接替换成“终端窗口质量很大”。

## 5. 时间厚度的正确系数

为了覆盖 R0.74Q 中对全部 \(\tau<t_0\) 的上确界，不能只在平台窗口
\(I_R\) 内定义这个量。对 padded shell 定义带时间截断的端点动能

\[
 e_{k,R}^{\eta}(t)
 :=\frac{\gamma_k\eta_R(t)}{2R}
 \int_{\mathbb R^3}\psi_k^R(y)|\widetilde v_R(t,y)|^2\,dy,
\]

以及选定时间集 \(J\subset(s_R,t_0)\) 上的局部速度三次支付

\[
 p_{k,R}^{u,\eta}(J)
 :=R^{-2}\gamma_k
 \int_J\eta_R(t)^{3/2}
 \int_{\operatorname{supp}\psi_k^R}
 |\widetilde v_R|^3\,dy\,dt.
\]

把端点相对于这段时间的厚度写成无量纲比率

\[
 \Theta_{k,R}^{\eta}(\tau;J)
 :=\frac{R^{-2}\int_Je_{k,R}^{\eta}(t)^{3/2}\,dt}
         {e_{k,R}^{\eta}(\tau)^{3/2}}.
\]

这里 \(\eta_R^{3/2}\) 不是装饰项：它正好来自端点动能的
\(3/2\) 次幂，也使论证覆盖时间截断的整个过渡区。空间支撑体积是
\(O(2^{3k}R^3)\)。一次精确的空间 Hölder 与时间积分
给出

\[
 \boxed{
 e_{k,R}^{\eta}(\tau)
 \le
 C_0\,2^k\gamma_k^{1/3}
 \Theta_{k,R}^{\eta}(\tau;J)^{-2/3}
 p_{k,R}^{u,\eta}(J)^{2/3}.}
\]

这说明需要的不是一句模糊的“持续一段时间”，而是带着正确壳层系数的
\(\Theta^\eta\)。跨壳层再用 Hölder 后，必须控制的是

\[
 \sum_k
 2^{3k}\gamma_k\Lambda_k^3\Theta_k^{-2}.
\]

这正是任意时钟问题的第二个因子。

## 6. 一个足够关闭固定尺度问题的条件定理

假设存在与解、尺度和终端时刻都无关的常数
\(N_0,C_q,C_*\)。对每个好终端时刻
\(\tau\in(s_R,t_0)\)，允许删除至多 \(N_0\) 个例外壳层；在其余壳层上
能够选择误差 \(q_k\ge0\)、放大因子 \(\Lambda_k\ge0\) 与先前时间集
\(J_k\subset(s_R,\tau)\)，使

\[
 \sum q_k\le C_qA_R,
 \qquad
 K_{k,R}(\tau)\le q_k+\Lambda_ke_{k,R}^{\eta}(\tau),
\]

并满足

\[
 \boxed{
 \sum
 2^{3k}\gamma_k\Lambda_k^3
 \Theta_{k,R}^{\eta}(\tau;J_k)^{-2}
 \le C_*.}
\]

那么，壳层 Hölder 与完整支付账本直接给出

\[
 \mathcal S_{N_0,R}^{K}\le CA_R,
\]

进而由 R0.74Q 的终端 reduction 得到

\[
 \boxed{
 \mathfrak C_R^M
 \le C\left[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}\right].}
\]

这一步还有一个容易漏掉的范围问题：R0.74Q 的
\(\mathcal S_{N_0,R}^{K}\) 对全部终端时刻取上确界，而端点能量公式先在
好时刻成立。规范时钟 \(K_{k,R}\) 逐壳层连续；非负序列的最优
\(N_0\) 项尾部对逐坐标收敛下半连续。因此，把好时刻逼近任意终端时刻，
就能把同一上界传到全部 \(\tau<t_0\)。这正是采用
\(e^\eta,p^{u,\eta},\Theta^\eta\) 而不只采用平台窗口量的原因。

这个“若……则……”已经证明。没有证明的是：任意 suitable weak solution
一定能构造出这些 \(q_k,\Lambda_k,J_k\)。因此，固定尺度不等式仍然是
**OPEN**，不能把条件定理写成无条件结论。

## 7. 三个不能绕过的 no-go 检验

我用三个显式检验排除了三种过快的证明路线。

第一，纯 completed-clock 代数不能提取动能。可以令

\[
 E=0,
 \qquad
 D=K=F=Th(t),
 \qquad
 Q=0,
\]

其中 \(h\) 光滑单调。所有时钟公理都成立，终端值等于 \(T\)，但任何
动能窗口平均都为零。它准确地落在“耗散/正变差”分支。

第二，一个光滑不可压时间尖峰可以保持固定端点动能，同时让时空速度三次
量为 \(O(\varepsilon)\)，并使

\[
 \Theta=O(\varepsilon/R^2)\to0.
\]

所以任何端点到时空三次量的估计都不能删掉时间厚度因子。

第三，取

\[
 A_n(x)=n^{-2}\zeta(x)\sin(nx_1)e_3,
 \qquad
 w_n=\nabla\times A_n.
\]

则 \(w_n\) 光滑且不可压，并满足

\[
 \|\nabla w_n\|_2\ge c_\zeta>0,
 \qquad
 \|w_n\|_3^3=O(n^{-3})\to0.
\]

因此，固定梯度耗散不可能仅靠一个通用函数不等式被速度三次支付。若
Navier--Stokes 方程能排除这种分离，证明必须显式使用演化方程。

这三个对象都不是 Navier--Stokes 反例。它们只证明：代数、不可压与
Hölder 本身不够。

## 8. 与已有文献的真正边界

最接近“时间持续性”的成熟结果不是空白。Neustupa 证明：若
\((x_0,t_0)\) 已经是 suitable weak solution 的奇点，则在 \(t_0\) 左侧
某个时间邻域的每一个时刻，\(x_0\) 的任意小空间邻域中都有统一正量的
局部 \(L^3\) 集中；论文还建立了局部化解的强能量不等式
([DCDS-S, 2013](https://doi.org/10.3934/dcdss.2013.6.1391))。

Barker 与 Prange 的局部光滑化定理进一步给出：在 Type-I 局部动能控制
与首次奇点假设下，每个足够晚的时刻，在半径
\(O(\sqrt{T^*-t})\) 的奇点中心球中都有统一 \(L^3\) 下界
([ARMA, 2020](https://arxiv.org/abs/1812.09115))；他们后来的工作还发展了
定量的浓度传播与 time-slice 正则性技术
([CMP, 2021](https://doi.org/10.1007/s00220-021-04122-x))。

这些结果很强，但它们从“已知奇点 + 额外 Type-I/临界控制”出发。我们
现在缺的是更早一层：从任意 prescribed-centre、finite-scale、包含缺陷
耗散的 completed shell clock 出发，在不先假定奇点结论的情况下提取
端点动能与可打包的时间厚度。

Choe 与 Yang 的反向 Hölder 结论也以统一有界的 scaled local kinetic
energy 为输入，并作用于速度梯度
([JDE, 2018](https://arxiv.org/abs/1705.04561))；它不提供从累计耗散到
速度三次量的反向支付。

2026 年有两个特别邻近、但仍不同的预印本。Yu 在有限 coarse-grained
链上证明了 active signed-work 提取和带 leakage/backscatter 的加权
telescoping，但把从 CKN badness 到 coarse observability 的困难步骤明确
留作独立问题
([arXiv:2606.25322](https://arxiv.org/abs/2606.25322))。Huang 则在终端能量
测度已经含点原子的假设下，构造 same-state constrained/passive 比较，
得到非负累计压力功与局部压力集中
([arXiv:2608.30715](https://arxiv.org/abs/2608.30715))。二者截至本节冻结时
均为预印本，不能当作已同行评审结论；它们也都没有给出本节所需的任意
completed-clock 两因子提取。

这次有限检索没有找到同型定理，但“没有检索到”不是新颖性证明。更准确
的表述是：已有文献证明了多种在奇点、Type-I、局部能量有界、有限 resolved
test family 或端点原子假设下的集中/传播/压力功定理；本项目的任意时钟
桥接仍未由这些结果覆盖。

## 9. 这一阶段的研究价值

R0.74R 的价值不是把 OPEN 改成 PROVED，而是把一个模糊缺口压成了可攻击
的精确命题。

现在已经确定：

- 只要真实质量占据继承的终端窗口，三次支付会把它指数级压向第一壳层；
- equal-target 不是关键，任意非负目标分布都受同一约束；
- 任意时钟问题只剩 clock-to-endpoint 与 endpoint-to-window 两个主要因子，
  再加耗散与正 upcrossing 的替代支付；
- 正确的时间厚度权重必须以
  (2^{3k}\gamma_k\Lambda_k^3\Theta_k^{-2}) 的形式可和；
- 三类纯函数/代数捷径已经被显式 no-go 排除。

这使下一步不必再试探“许多壳层能否同时亮起”或重新发明序列压缩。更有
价值的路线是二选一：

1. 建立保留负功与 leakage 的 signed stopping-time 恒等式，把 recent
   upcrossing 直接送入可支付账本；
2. 建立真正的动力学耗散替代：一个耗散主导壳层要么属于统一有限例外集，
   要么在相邻抛物时间段重新产生足够厚的动能。

这是重要的结构性进展，但距离论文级主定理仍有明显缺口；当前还不能声称
创新优先权、正则性或千禧年问题突破。

## 10. 审计状态

R0.74R Step 1 的解析证明、精确有理数与指数账本、确定性重跑、负哨兵和
两轮独立审计均已通过。Step 2 修复全时段范围后，当前有限证书通过了
13/13 个有理数检查、3/3 个指数账本和 25/25 个结构检查；确定性重跑
字节一致，且把 \(2^{3k}\) 错改为 \(2^{2k}\) 的负哨兵已被拒绝。
Step 2 的独立数学审计尚未完成，因此本读者稿在独立
审计通过前不应标记为最终发布冻结版。

当前严格状态如下：

- **PROVED**：窗口 lobe 的任意质量凸性压缩与第一壳层稳定性；
- **PROVED**：任意 completed clock 的三分法；
- **PROVED**：带 \(\Theta^\eta\) 的端点到时空三次支付；
- **CONDITIONAL / PROVED IMPLICATION**：两因子条件推出固定尺度不等式；
- **FINITE**：Step 2 当前算术、指数与结构证书；
- **LITERATURE BOUNDARY**：截至 2026-09-02 的有限一手文献非同型命中；
- **OPEN**：两因子的任意 suitable-weak 构造、耗散替代、signed
  upcrossing 支付、\(Q.1\)、尺度收缩与正则性；
- **NOT CLAIMED**：奇点构造、奇点排除、Clay 问题解决。

**NOT CLAY.**
