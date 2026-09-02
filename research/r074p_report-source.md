# R0.74P｜哪些时间可观测量真正看见了缺失的尺度？

## 导语

这一节仍然没有解决三维 Navier--Stokes 千禧年问题。

R0.74O 已经说明：只看原来的完整标量支付量，不可能给出我曾希望
得到的普适次线性端点上界。在那列光滑、周期、无外力的精确解上，
记

\[
 T_*:=\varkappa^2B^2LR^2,
 \qquad
 K_*:=\frac{T_*}{B^2R^2}=\varkappa^2L\longrightarrow\infty,
\]

则

\[
 X_*^\alpha\asymp\mathfrak C_*^\alpha\asymp T_*,
 \qquad
 (P_*^\alpha)^{2/3}\asymp\frac{T_*}{K_*}.
\]

这里带 \(\alpha\) 的结论只用于光滑精确解族，
\(\alpha\in\{M,F\}\)，其中 \(z_M=v_R\)，
\(z_F=v_R-a_R\)。下文关于一般周期适合弱解的定理及全部紧性结论
都只在 Version M 中陈述，并固定半径 \(R\) 与终点。

所以真正缺失的是一个能区分“平均尺度”与“短时集中尺度”的结构
量。R0.74P 没有直接猜一个答案，而是逐一筛选三个候选：正阶时间
窗口质量、能量振荡、以及缺陷补全壳层时钟。

结论很清楚。

1. 每个固定正阶的窗口质量都漏掉目标尺度。
2. 能量振荡能看见目标尺度，但它基本上把原端点重新写了一遍。
3. 缺陷补全时钟在固定 \(R\)、固定终点的适合弱解极限下稳定；其
   匹配平方函数的目标壳分量恰好达到 \(T_*\)，但完整平方函数的上
   界仍未证明。

这把下一步从一片模糊的“寻找时间信息”，缩成了一条明确的 PDE
问题：怎样把逐壳层的 \(\ell^1\) 通量账本压缩成匹配的
\(\ell^2\) 时钟？

**NOT CLAY.**

## 1. 第一条路线：正阶窗口质量为什么必然漏检

令加权能量为

\[
 E_R^\alpha(t)
 :=\frac1R\int_{\mathbb T^3}\Theta_R|z_\alpha(t)|^2\,dx,
\]

对固定 \(\sigma>0\) 定义

\[
 \mathcal C_{\sigma,R}(E)
 :=\sup_{J\Subset I_R,\ |J|>0}
 \left(\frac{|J|}{R^2}\right)^\sigma
 \fint_JE(t)\,dt.
\]

这个量试图奖励短时间窗口中的高能量，同时用
\((|J|/R^2)^\sigma\) 惩罚过短窗口。问题在于，精确解族同时给出

\[
 \operatorname*{ess\,sup}_{I_R}E_*\le CT_*,
 \qquad
 \fint_{I_R}E_*\le C\frac{T_*}{K_*}.
\]

若令 \(x=|J|/R^2\in(0,1)\)，任何窗口都满足

\[
 x^\sigma\fint_JE_*
 \le CT_*\min\{x^\sigma,K_*^{-1}x^{\sigma-1}\}.
\]

分别取三个区间 \(0<\sigma<1\)、\(\sigma=1\) 与
\(\sigma>1\) 的上确界，得到

\[
 \boxed{
 \mathcal C_{\sigma,R}(E_*)
 \le CT_*K_*^{-\min\{\sigma,1\}}
 =o(T_*).}
\]

当 \(\sigma>1\) 时，第二个分支随 \(x\) 增长；因为 \(x<1\)，
\(K_*^{-1}\) 只在 \(x\uparrow1\) 时逼近，并不在允许窗口上取到。

这里的量词非常重要：对每个固定 \(\sigma>0\)，对所有充分大的
\(j\) 成立，常数对 \(j\) 一致；但当
\(\sigma\downarrow0\) 时并不一致。恰在 \(\sigma=0\) 时，窗口上
确界退化为

\[
 \sup_{J\Subset I_R,\ |J|>0}\fint_JE
 =\operatorname*{ess\,sup}_{I_R}E,
\]

也就是原来的端点量。

因此，不存在一个“稍微正阶”的窗口质量，既保持弱于端点，又能在
这个精确解族上看见 \(T_*\)。这是一条严格的 no-go，而不是数值
现象。

正式附图中的三条直线只画
\(-\min\{\sigma,1\}\log_{10}K_*\) 这一衰减率项。真实上界还有一
个未知的加法截距 \(\log_{10}C\)，图和源数据都明确把它省略；因
此曲线表达斜率与渐近速率，不表达绝对纵向数值。

## 2. 第二条路线：能量振荡能检出，但没有真正变弱

定义所有时间窗口平均之间的最大振荡

\[
 \Omega_R^\alpha
 :=\sup_{\substack{J,K\Subset I_R\\ |J|,|K|>0}}
 \left|\fint_JE_R^\alpha-\fint_KE_R^\alpha\right|.
\]

Lebesgue 微分定理给出精确恒等式

\[
 \Omega_R^\alpha
 =\operatorname*{ess\,sup}_{I_R}E_R^\alpha
 -\operatorname*{ess\,inf}_{I_R}E_R^\alpha.
\]

于是

\[
 \mathcal U_{\rm ext}^{\infty,\alpha,R}
 \le C\left[(P_R^\alpha)^{2/3}+\Omega_R^\alpha\right].
\]

若再把完整外部耗散加回来，当然可以控制 \(X_R^\alpha\)。在精确
解族上，对所有充分大的 \(j\)，且常数对 \(j\) 一致，也确实有

\[
 \Omega_R^{\alpha,*}\asymp T_*.
\]

但这不是我想寻找的更弱机制。它用“最高能量减最低能量”重建了
端点，并显式把全部外部耗散重新放入右端。它是一个稳定、正确、但
已经解决的基线。

## 3. 第三条路线：用总局部耗散补全壳层时钟

适合弱解的局部能量不一定满足等式。定义总局部耗散分布

\[
 \boldsymbol\mu[u,p]
 :=-\partial_t\frac{|u|^2}{2}
 -\nabla\!\cdot\!\left[\left(\frac{|u|^2}{2}+p\right)u\right]
 +\Delta\frac{|u|^2}{2}.
\]

局部能量不等式给出

\[
 \boldsymbol\mu\ge|\nabla u|^2\,dx\,dt.
\]

对每个空间壳层，我先在局部能量良时间 \(\tau<t_0\) 定义

\[
 \widetilde K_{k,R}(\tau)
 :=
 \frac{\eta_R(\tau)}{2R}
 \int_{\mathbb T^3}\Psi_k^R(y)|v_R(\tau,y)|^2\,dy
 +\frac1R
 \int_{(s_R,\tau)\times\mathbb T^3}
 \eta_R(t)\Psi_k^R(x-X_R(t))\,d\boldsymbol\mu(t,x).
\]

壳层权重放在时钟内部，即良时间上
\(K_{k,R}=\gamma_k\widetilde K_{k,R}\)。但在所有时间上，我不把
这个测度公式当作定义，而是用精确累计平衡

\[
 K_{k,R}=Q_{k,R}+F_{k,R},
\]

其中 \(Q\) 是二次截断原函数，\(F\) 是物理通量原函数，并把
\(Q+F\) 选为 \(K\) 在 \([s_R,t_0]\) 上的规范绝对连续代表。它在
每个良时间与上式一致。这样做的关键不是多加一个符号，而是避免在
某个固定时刻切取耗散测度；弱星收敛时也不需要穿过可能的时间原子。

## 4. 已闭合的 \(\ell^1\) 时钟

取时钟的正变差

\[
 v_{k,R}:=\operatorname{Var}^+_{[s_R,t_0)}K_{k,R},
 \qquad
 Y_{1,R}^{\rm clk}:=\sum_{k\ge1}v_{k,R}.
\]

完整绝对值账本给出

\[
 \sum_k\operatorname{TV}_{[s_R,t_0)}Q_{k,R}\le C(P_R^M)^{2/3},
 \qquad
 \sum_k\operatorname{TV}_{[s_R,t_0)}F_{k,R}\le CP_R^M.
\]

因此

\[
 \boxed{
 Y_{1,R}^{\rm clk}
 \le C\left[(P_R^M)^{2/3}+P_R^M\right],}
\]

而且

\[
 \boxed{
 \mathfrak C_R^M
 \le Y_{1,R}^{\rm clk}+C(P_R^M)^{2/3}.}
\]

这是一个 Version M 中、在冻结局部设置下对周期适合弱解成立的定
理，但它没有完成压缩：右端仍然保留线性的逐壳层绝对通量成本。

## 5. 匹配平方函数：目标壳检出，完整上界未闭合

自然的弱化是

\[
 Y_{2,R}^{\rm sf}
 :=\left(\sum_{k\ge1}v_{k,R}^2\right)^{1/2}.
\]

在 R0.74O 精确解族的目标壳 \(j\) 上，对所有充分大的 \(j\)，并
且常数对 \(j\) 一致，我证明

\[
 \boxed{cT_*\le v_{j,R}\le CT_*.}
\]

因此

\[
 Y_{2,R}^{\rm sf}\ge cT_*.
\]

这只是一条“下方检出”结论：目标壳没有被平方求和抹掉。它绝不表
示完整 \(Y_{2,R}^{\rm sf}\) 也有 \(CT_*\) 上界，因为其他壳层仍然
存在。

若改用能通过 Cauchy--Schwarz 自动闭合的强加权量

\[
 Y_{2,R}^{\rm strong}
 :=\left(\sum_k\frac{v_{k,R}^2}{\gamma_k}\right)^{1/2},
\]

目标壳却至少支付

\[
 Y_{2,R}^{\rm strong}
 \ge cT_*\Gamma^{-1/2}.
\]

它比目标尺度多出指数因子。有限证书把这个额外指数相对
\(a=2m/3\) 的精确比值复算为

\[
 \frac{(c_\gamma/2)}{a}=\frac{640}{43}.
\]

所以现在已经知道两端：\(\ell^1\) 账本太贵；带
\(\gamma_k^{-1/2}\) 的 \(\ell^2\) 也太贵。匹配的无附加权
\(\ell^2\) 正好处在需要 PDE 结构填补的中间位置。

## 6. 固定尺度弱稳定性已经闭合

在固定半径 \(R\)、固定终点、每个紧子柱上的 Lin 紧性拓扑下，若

\[
 u_n\to u\ \hbox{strongly in }L^3,
 \qquad
 \nabla u_n\rightharpoonup\nabla u\ \hbox{weakly in }L^2,
 \qquad
 p_n\rightharpoonup p\ \hbox{weakly in }L^{3/2},
\]

则平滑轨迹一致收敛，移动场按相应强弱拓扑收敛，总耗散测度局部弱
星收敛。每个固定壳层的 \(Q,F,K\) 累计原函数都在闭时间区间上一致
收敛。

正变差因此满足

\[
 v_{k,R}[u,p]
 \le\liminf_n v_{k,R}[u_n,p_n],
\]

并进一步得到

\[
 \boxed{
 Y_{2,R}^{\rm sf}[u,p]
 \le\liminf_nY_{2,R}^{\rm sf}[u_n,p_n].}
\]

窗口质量、能量振荡与外部耗散也具有相应下半连续性。

这一步说明匹配时钟可以穿过标准适合弱解极限。它没有说明该时钟在
半径 \(R\downarrow0\) 时小，也没有给出跨尺度紧性。

## 7. 真正剩下的一条不等式

当前核心缺口可以写成

\[
 \boxed{
 \mathfrak C_R^M
 \stackrel{?}{\le}
 C\left[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}\right].}
\]

不能用纯序列不等式证明它。若 \(v_1=\cdots=v_N=1\)，则

\[
 \sum_kv_k=N,
 \qquad
 \left(\sum_kv_k^2\right)^{1/2}=\sqrt N.
\]

所以必须使用 Navier--Stokes 方程本身限制“同时有效的壳层”数量、
持续时间或相互作用。这可能采取有效壳层定理、尺度装箱估计，或另
一种能把正变差关联起来的 PDE 机制。

即使这条不等式成立，也还没有解决正则性。下一层接口还需要一个真
正的尺度收缩，例如

\[
 \mathcal E_{\theta R}
 \le\lambda\mathcal E_R
 +C\left[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}\right],
 \qquad 0<\theta<1,\quad 0<\lambda<1,
\]

并证明右端新增项沿一个预定中心的嵌套尺度序列足够小或可求和。
Lei--Ren 在看过解以后选择的空间正则区间和 quantitative regularity
epochs，都不能自动强迫一个穿过预定时空中心的收缩尺度列。Yu 2026
研究了相邻的移动抛物窗口链、局部能量 supply--tax 账本与尺度缺陷
包，但没有陈述本文的 \(K=Q+F\) 壳层时钟、时间正变差 BV 或匹配壳
层 \(\ell^2\) 下半连续性定理。

## 8. 这一节的研究价值

R0.74P 的价值不是向 Clay 终点迈出一个可量化百分比，而是把三条容
易混淆的路线严格分开。

- 正阶窗口路线在精确解族上被排除。
- 能量振荡路线被识别为端点的重包装。
- 缺陷补全匹配时钟同时通过了目标壳检出与固定尺度弱稳定两道必要
  门槛。

它还把失败原因从“估计技巧不够”变成了一个可检验的结构问题：能
否证明 PDE 只允许有限或可装箱的有效壳层？这个问题既可以被证明，
也可以被新的精确解族否定，因此适合作为下一阶段的严肃研究目标。

## 9. 证据与边界

- **PROVED：**正阶窗口 no-go、能量振荡恒等式、缺陷补全平衡、
  \(\ell^1\) 闭合、目标壳双边尺度、固定尺度弱下半连续性。
- **INHERITED：**R0.74O 的光滑精确解族及其
  \(P_*,X_*,\mathfrak C_*\)
  尺度。
- **FINITE：**52 项精确有理数与有限序列检查；图件中的 147 个包络
  点和 5 个速率行。
- **LITERATURE BOUNDARY：**相关文献提供适合弱解、局部耗散、移动
  圆柱、固定物理壳层通量、空间正则区间与 quantitative regularity
  epochs 等工具；Yu 2026 是移动窗口与尺度缺陷账本的相邻预印本。
  没有任何一篇被用来替代本文的壳层时钟证明。有限未命中不证明创
  新性或优先权。
- **OPEN：**完整匹配平方函数上界、\(\ell^1\) 到匹配 \(\ell^2\)
  的 PDE 压缩、预定中心尺度装箱、收缩迭代与全局正则性。

本节没有数值 Navier--Stokes 仿真，没有构造奇点，没有排除奇点，
也没有证明任意光滑有限能量初值的全局正则性。

**NOT CLAY.**
