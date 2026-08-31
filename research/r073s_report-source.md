# R0.73S | From triple convolution to autocorrelation: one computable certificate and two hard limits

**Status:** analytic proof, primary-source collision audit, independent
no-go audit, and exact finite certificate pre-seal passed; immutable source
commit seal, formal figure, and public release remain pending

**Public title (zh):** R0.73S｜把三重卷积降到自相关：一个可算证书，两条不能越过的边界

**Date:** 2026-08-31

**Audience:** researchers and technically trained readers following the
periodic three-dimensional Navier--Stokes notes

**Scope:** a lower-interaction-order sufficient proxy for the R0.73R
critical heat trace, plus exact information-theoretic obstructions; no
arbitrary-data regularity claim

**Normalization:** throughout, \(\mathbb T^d=[0,2\pi]^d\) carries Haar
probability measure \(d\mu=(2\pi)^{-d}dx\); with the displayed Fourier
coefficient convention, Parseval and the autocorrelation inequality have
constant one

## 1. 直接结论

R0.73R 留下了一个具体问题：精确计算逐壳 \(L^6\) 需要三重 Fourier
卷积。有没有保留相位、但只到二次相互作用的严格上界？

答案分成两半。

第一半是肯定的。对有限 Fourier 向量场

\[
 f(x)=\sum_{k\in S}a(k)e^{ik\cdot x},
\]

定义系数自相关

\[
 C(h)=\sum_k a(k+h)\cdot\overline{a(k)}
      =\widehat{|f|^2}(h).
\]

再记

\[
 A=\sum_h|C(h)|,
 \qquad
 Q=\sum_h|C(h)|^2=\|f\|_4^4.
\]

那么

\[
 \boxed{\|f\|_6^6\le A Q.}
 \tag{1.1}
\]

这把精确的三重卷积，换成了完整的二次自相关。它保留每个移位内部的
相位抵消，并给出严格充分上界。

第二半是否定的。只知道 \(L^2\)、\(L^4\)、频率支撑和少量预选
自相关移位，不能常数因子恢复 \(L^6\)。组合支撑因子不能无条件删掉，
低阶统计也不能代替全部高阶相位。

这正是本节的结果：我找到了一个能用的二次证书，也把它不能做到的事
用严格反例封住了。

## 2. 二次证书

令

\[
 E=\|f\|_2,
 \qquad M=|S|,
 \qquad D_C=|\operatorname{supp}C|,
 \qquad D_\Delta=|S-S|.
\]

显然 \(D_C\le D_\Delta\)。三角不等式与 Cauchy--Schwarz 给出

\[
 A\le ME^2,
 \qquad
 A\le\sqrt{D_CQ}\le\sqrt{D_\Delta Q}.
\]

因此

\[
 \boxed{
 \|f\|_6^6
 \le AQ
 \le Q\min\{ME^2,\sqrt{D_CQ}\}.}
 \tag{2.1}
\]

若写成无量纲形式

\[
 \Gamma={\|f\|_4^4\over\|f\|_2^4},
 \qquad
 \Theta={\|f\|_6^6\over\|f\|_2^6},
\]

则

\[
 \boxed{
 \Theta
 \le\Gamma\min\{M,\sqrt{D_C\Gamma}\}.}
 \tag{2.2}
\]

式 (1.1) 只是 Hölder、Parseval 与绝对 Fourier 级数估计的直接推论；
式 (2.2) 的差集分支也是把经典 Nikolskii 不等式用在 \(|f|^2\) 上。
Nessel--Wilmes 1978 的 Theorem 1 已经直接覆盖

\[
 \|f\|_6\le D_C^{1/12}\|f\|_4.
\]

所以这里没有新的调和分析定理。新增的是它在本路线中的壳层接口、
尖锐边界与可复现证书。

## 3. 临界热流入口

对 \(f_j=P_jf\)，令

\[
 Q_j=\|f_j\|_4^4,
 \qquad
 U_j=Q_j\min\{M_jE_j^2,\sqrt{D_{\Delta,j}Q_j}\}.
\]

R0.73R 的两侧热流刻画立即给出

\[
 \boxed{
 \|e^{t\Delta}f\|_{L_t^4L_x^6}
 \le C_+
 \left(\sum_j2^{-2j}U_j^{2/3}\right)^{1/4}.}
 \tag{3.1}
\]

也可以直接使用更紧的 \(U_j=A_jQ_j\)。若右端小于 R0.73Q 的固定
稳定半径，就进入同一个已知全局参考轨道周围的强解管道。

在朴素稀疏模型里，枚举 \(M\) 个活跃模态的全部有序对需要
\(O(M^2)\) 次相互作用；R0.73R 的全部有序三元组是 \(O(M^3)\)。
所以这里确实完成了代数相互作用阶数的下降。

但这不是普适运行时间定理。稠密补零网格上的二次相关和三重卷积都可
用 FFT 做到 \(O(G\log G)\)；有乘积结构的例子甚至可由递推直接求矩。
我没有证明任何复杂度下界。

## 4. 为什么差集平方根不能删

令 \(m\ge2\)，并设

\[
 d_m(x)=m^{-1/2}\sum_{q=0}^{m-1}e^{iqx},
 \qquad
 \beta_m=m^{-1/4},
 \qquad
 a_m=(1-m^{-1/2})^{1/2},
\]

并取无共振载频 \(N>2(m-1)\)：

\[
 F_m(x)=a_m+\beta_me^{iNx}d_m(x).
\]

精确计算得到

\[
 \|F_m\|_2=1,
\]

\[
 \|F_m\|_4^4
 ={5\over3}+2m^{-1/2}-3m^{-1}+{1\over3m^2}
 \longrightarrow{5\over3},
\]

而

\[
 \|F_m\|_6^6
 ={11\over20}\sqrt m+7+O(m^{-1}).
\]

同时

\[
 D_C=D_\Delta=4m-1.
\]

因此 \(L^4\) 集中度保持有界，\(L^6\) 集中度仍按
\(\sqrt{D_C}\) 增长。更强地，我可以微调 \(\beta_m\)，让
\(\Gamma\equiv5/3\) 对每个 \(m\) 精确成立，而六次集中度仍按
\(\sqrt{D_C}\) 增长。

所以式 (2.2) 中 \(D_C^{1/2}\) 的增长指数不能降低。这里没有证明最优
常数，也没有证明 \(\Gamma^{3/2}\) 的指数最优；我只封住差集指数。

这个反例可以不离开真实三维无散度场。取

\[
 N=3m,
 \qquad K=32m,
 \qquad H_m=e^{iKx_1}F_m(x_1),
\]

并定义

\[
 V_m=(0,\operatorname{Re}H_m,\operatorname{Im}H_m).
\]

那么

\[
 |V_m|=|F_m|,
 \qquad
 \nabla\cdot V_m=0,
 \qquad
 M(V_m)=2m+2.
\]

\[
 D_C(V_m)=4m-1,
 \qquad
 D_\Delta(V_m)=10m-1,
 \qquad
 32m\le|k|<36m.
\]

所有 \(L^{2p}\) 矩都原样保留。它还是一族零非线性剪切流：

\[
 (V_m\cdot\nabla)V_m=0.
\]

所以这只是证书的尖锐性反例，不是危险动力学，更不是奇性构造。

## 5. 少量自相关也不够

部分移位可以严格使用。对选定集合 \(H\)，我计算 \(C(h)\)，并对未看
移位支付系数模长相关的尾项，就得到

\[
 \|f\|_6^6\le A_HQ_H.
\]

它是有限、确定、可审计的上界。但尾信息若只给 \(\ell^2\) 质量，仍然
不够。Dirichlet 三角自相关可以做到

\[
 \|q\|_2^2\to0,
 \qquad
 \sum_{h+k+\ell=0}q_hq_kq_\ell\to\infty.
\]

即使自适应选取 \(o(m)\) 个移位，领先的三次尾贡献仍可留在未观测区。
要继续收紧，必须加入 \(\ell^1\) 尾、卷积尾范数、符号抵消或加法结构，
不能只说“剩余能量很小”。

还有一个更直接的不可辨识性对。

\[
 A(z)=1-z-z^2-z^3+z^4,
\]

\[
 B(z)=1-z-z^2-z^3-z^4.
\]

它们满足

\[
 \|A\|_2^2=\|B\|_2^2=5,
 \qquad
 \|A\|_4^4=\|B\|_4^4=37,
\]

但

\[
 \|A\|_6^6=311,
 \qquad
 \|B\|_6^6=323.
\]

用 \(q\ge14\) 的无进位 lacunary 乘积重复这两个因子，支撑、逐模幅值、
\(L^2\) 与 \(L^4\) 始终完全相同，而 \(L^6\) 比值指数增长。

这说明低阶汇总不能常数因子恢复六次相干性。但量词必须说准确：有限
Fourier 场的完整自相关本身也是有限的，并且完整决定 \(L^6\)。失败的
是预先给定的严格子集、次线性移位预算或过度压缩的低阶统计。

## 6. 回到同谱相位对

对 R0.73R 的同谱 Dirichlet/Rudin--Shapiro 场，令 \(m=2^r\)。共同有

\[
 E=1,
 \qquad
 M=2m^2,
 \qquad
 D_\Delta=3(2m-1)^2.
\]

Dirichlet 分支满足

\[
 A_D=2m^2,
 \qquad
 Q_D={(2m^2+1)^2\over6m^2},
\]

所以

\[
 A_DQ_D\asymp m^4.
\]

二次证书恢复了真实 \(L^6{}^6\asymp m^4\) 的正确次数。

Rudin--Shapiro 分支满足

\[
 Q_P={(4m-(-1)^r)^2\over6m^2}=O(1),
\]

差集界给出 \(A_P=O(m)\)。证书不是尖锐的，但已把 \(L^6\) 上界降到
\(O(m^{1/6})\)，优于只数模态时的 \(O(m^{1/3})\)。

采用 R0.73R 的共同缩放后，Dirichlet 热流代理保持常数量级；
Rudin--Shapiro 热流代理按

\[
 O(m^{-1/2})
\]

趋于零。真实衰减是 \(O(m^{-2/3})\)，但二次证书已经足以严格区分这对
同谱相位场。

## 7. 研究价值

这一节没有产生新的 Nikolskii 定理，也没有产生新的
Rudin--Shapiro 矩公式。一次严格的一手文献碰撞审计已经确认：这些基础
部分分别已有 1978、1985、2004 与 2017 年的直接来源。

本节真正完成的是三件较窄但可用的工作。

1. 我把 R0.73R 的精确三重卷积入口，降成了逐壳二次自相关的充分证书；
2. 我证明差集平方根在真实无散度固定环带内也不能删；
3. 我证明低阶统计与少量移位不能常数因子替代完整六次相位，并给出精确
   可复现的放大族。

这比“又找到一个上界”更有价值，因为它同时告诉下一步该保留什么、
不该再追什么。

但它仍不是 Clay 进展。它没有从任意 \(L^2\) 数据推出小量，没有控制
未知强解的全部时间演化，也没有把充分入口变成必要条件。

## 8. 下一步

R0.73T 不再继续寻找静态的更漂亮代理。下一步要把二次证书送入
Navier--Stokes 动力学，研究逐壳

\[
 Q_j(t)=\|P_ju(t)\|_4^4
\]

或完整 \(A_j(t)Q_j(t)\) 的演化与通量。目标是回答：黏性耗散、压力投影
和壳间能量通量，能否在某个可验证时间窗内支付这个相位预算，并强迫
轨道进入 R0.73Q 的稳定管道？

若只能得到依赖未知高阶范数的恒等式，R0.73T 就应当把它写成明确的
闭合障碍，而不是再包装成一个判据。

## 9. 证书边界

R0.73S 的有限证书使用 43 行源数据、226 项主检查、54 项独立重建和
289 项封包前结构检查。所有有限公式都用整数或有理数作通过判定；
GPU 与 DGX 均未使用。

证书不计算连续热流积分，不做 Navier--Stokes 仿真，不使用区间算术，
不认证完整 PDE 证明，也不证明运行时间下界。

本节没有证明：

- 从 \(L^2\) 单独得到临界热流小量；
- 二次自相关证书的必要性；
- 大证书意味着不稳定、爆破或奇性；
- 一个不依赖已知全局参考轨道的结论；
- 任意三维光滑性或 Clay 结论。

## 10. Primary sources

- Nessel--Wilmes 1978, finite-spectrum Nikolskii inequality:
  [DOI](https://doi.org/10.1017/S1446788700038878).
- Edwards 1972, compact-group Hausdorff--Young:
  [DOI](https://doi.org/10.1017/S0004972700044427).
- Rudin 1959, Rudin--Shapiro construction:
  [DOI](https://doi.org/10.1090/S0002-9939-1959-0116184-5).
- Høholdt--Jensen--Justesen 1985, aperiodic correlations and merit factor:
  [DOI](https://doi.org/10.1109/TIT.1985.1057071).
- Doche--Habsieger 2004, exact even moments:
  [DOI](https://doi.org/10.1007/s00041-004-3049-y).
- Rodgers 2017, limiting distribution and fixed moments:
  [DOI](https://doi.org/10.1016/j.aim.2017.09.022).
