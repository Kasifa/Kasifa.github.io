# 固定能量下的频带激活：尖锐的 \(N^{-5/2}\) 时间尺度

2026-09-07（Asia/Shanghai）。解析研究源稿。
PROVED LOCAL ESTIMATE / PROVED COUNTEREXAMPLE TO A SPECIFIED UNIFORM BOUND / OPEN / NOT CLAY。
独立审查与冻结状态见配套记录；本文件本身不是发布回执。

我检查的问题很窄：完整 NS 的能量预算能否强制一个空的高频带等待至少黏性时间，才获得固定正能量？答案是否定的。下面先给出普遍的 \(N^{-5/2}\) 激活时间下界，再用同一类完整、无外力周期 NS 解证明这个频率幂次可以达到。

这里的“激活”指频带从零达到一个固定正阈值，不是激活之后停留多久。构造改变初值，不是一条固定解的无限级联。扩大环面与固定能量的短时缩放已用于本项目 AJ；此次增量是频谱为空的输出带、其非线性非退化和激活时间的尖锐性，不主张这套缩放机制的新颖性。

## 1. 固定对象与结论

固定 \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\)、\(\nu>0\)、\(E_0>0\)，研究完整无外力 NS
\[
 \partial_tu+\mathbb P\operatorname{div}(u\otimes u)=\nu\Delta u,
 \qquad \operatorname{div}u=0,\qquad
 \frac12\|u(0)\|_2^2=E_0 .
 \tag{FA.1}
\]
范数使用未归一化体积。初值实、光滑、零均值；\(\mathbb P\) 是完整 Leray 投影。最终的一般正则性目标不受此特定构造限制。

选定一次非负、实、径向 \(\chi\in C_c^\infty(\mathbb R^3)\)，满足
\(0\le\chi\le1\)，支撑在 \(2.05<|\xi|<2.2\)，且在
\(|\xi|=3/\sqrt2\) 的某个邻域内为 1。对 dyadic \(N=2^j\ge1\)，定义
\[
 Q_N=\chi(D/N),\qquad
 a_N(t)=\|Q_Nu(t)\|_2,\qquad e_N(t)=\tfrac12a_N(t)^2,
 \qquad D=\sqrt{-\Delta}.
 \tag{FA.2}
\]
因 \(\chi\) 径向，记号 \(\chi(D/N)\) 表示在 Fourier 频率 \(k\) 上乘 \(\chi(k/N)\)，不表示幂等投影。

结论有两部分。

1. 对每个光滑解及其任意存在时段 \(s<t\)，若
   \(a_N(s)\le b_0<b_1\le a_N(t)\)，则
\[
 t-s\ge\frac{b_1-b_0}{C_\chi E_0 N^{5/2}}.
 \tag{FA.3}
\]
   常数与初值、\(N,\nu,s,t\) 无关；这是到达阈值前的时间约束。
2. 对每个固定 \(\nu,E_0\)，存在 \(\eta\in(0,E_0)\)、\(c,C>0\) 和
   \(N_0\)，使每个 dyadic \(N\ge N_0\) 都有一个上述完整 NS 的光滑解
   \(u^{(N)}\)，初始频谱包含在 \(N\le|k|\le2N\)，并且
\[
 \begin{gathered}
 Q_Nu^{(N)}(0)=0,\qquad
 T_N:=\inf\{t\ge0:e_N^{(N)}(t)\ge\eta\},\\
 cN^{-5/2}\le T_N\le CN^{-5/2},\qquad
 \nu\int_0^{CN^{-5/2}}\|\nabla u^{(N)}(t)\|_2^2\,dt
 \le C'\nu N^{-1/2}\longrightarrow0 .
 \end{gathered}
 \tag{FA.4}
\]
   解在所用的整个时间窗上光滑。\(\eta,c,C,C'\) 可以依赖固定
   \(E_0,\nu,\chi\) 及下面固定的种子；不依赖 \(N\)。
   \(T_N\) 只在所构造的光滑时间窗内取首次到达，后文保证集合非空。

因此，对这个固定正阈值，不存在仅依赖这些固定量的
\(c_*>0\)，使所有此类解的激活时间都满足
\(T_N\ge c_*(\nu N^2)^{-1}\)。事实上，FA.4 给
\(\nu N^2T_N\to0\)。也不能将 FA.3 中的频率幂普遍改成任何
\(\alpha<5/2\)，而保持一个与 \(N\) 和初值的高阶范数无关的正常数。

## 2. 能量给出的普遍上升约束

乘子 \(Q_N\mathbb P\operatorname{div}\) 的周期卷积核 \(K_N\) 满足
\[
 \|K_N\|_2\le C_\chi N^{5/2},\qquad
 F_N(t):=\|Q_N\mathbb P\operatorname{div}(u\otimes u)(t)\|_2
 \le C_\chi N^{5/2}\|u(t)\|_2^2
 \le 2C_\chi E_0N^{5/2}.
 \tag{FA.5}
\]
第一式可直接用 Fourier Parseval 检查：符号在 \(|k|\asymp N\)
上为 \(O(N)\)，共有 \(O(N^3)\) 个格点。第二式用
\(L^1*L^2\to L^2\) 和 \(\|u\otimes u\|_1=\|u\|_2^2\)。
矩阵与向量分量只有固定维度常数。压力没有删去。

精确 mild 方程和目标带的最低频率给
\[
 a_N(t)\le e^{-c_\chi\nu N^2(t-s)}a_N(s)
 +\int_s^t e^{-c_\chi\nu N^2(t-r)}F_N(r)\,dr .
 \tag{FA.6}
\]
丢掉热核衰减后，\(a_N(t)-a_N(s)\le2C_\chi E_0N^{5/2}(t-s)\)，
调整常数即得 FA.3。未假设频带振幅单调，也未假设只有相邻带相互作用。
完整源项允许任意高频的 high–high 回落及同一输出频率内的相位抵消。

## 3. 从空带产生非零输出的 Euclidean 种子

采用 Fourier 约定
\(\widehat F(\xi)=\int_{\mathbb R^3}F(x)e^{-ix\cdot\xi}\,dx\)，
逆变换带 \((2\pi)^{-3}\)。
令 \(P_\xi=I-\xi\otimes\xi/|\xi|^2\)，取
\[
 p=(3/2,0,0),\quad q=(0,3/2,0),\quad
 A=(0,1,0),\quad B=(0,0,1),\quad \zeta_0=p+q .
 \tag{FA.7}
\]
固定一个非零、实、非负、偶的
\(\psi\in C_c^\infty(B_1)\)，令
\(\psi_\delta(\xi)=\delta^{-3/2}\psi(\xi/\delta)\)。定义
\[
 \widehat F(\xi)=
 \sum_{\sigma=\pm1}\big[
   \psi_\delta(\xi-\sigma p)P_\xi A+
   \psi_\delta(\xi-\sigma q)P_\xi B\big].
 \tag{FA.8}
\]
对充分小的固定 \(\delta>0\)，这是远离零频的光滑紧支撑函数。
它实且偶、横向非零，所以 \(F\) 实、Schwartz、无散、零积分。
其 Fourier 支撑包含在 \(1<|\xi|<2\)，故 \(\chi(D)F=0\)。

令 \(\Gamma_F=\chi(D)\mathbb P\operatorname{div}(F\otimes F)\)。
在 \(\zeta_0\)，卷积仅有靠近 \(p,q\) 的两个有序区域。
因为 \(q\cdot A=3/2\)、\(p\cdot B=0\)、\(P_{\zeta_0}B=B\)，
\[
 \widehat{\Gamma_F}(\zeta_0)
 =\frac{i}{(2\pi)^3}
   \big[(3/2)B+O(\delta)\big]\int_{\mathbb R^3}\psi_\delta(\alpha)^2\,d\alpha
 \ne0,\qquad
 \gamma_F:=\|\Gamma_F\|_{L^2(\mathbb R^3)}>0 .
 \tag{FA.9}
\]
这里误差向量的长度至多 \(C\delta\)，常数与 \(\delta\) 无关：
四个小球上的 \(P_\xi\) 及卷积中的线性频率因子都是一致 Lipschitz；
在 \(\zeta_0\) 两个 bump 的乘积恰为 \(\psi_\delta(\alpha)^2\)。
取 \(\delta\) 使误差小于主项的一半即可。
其它正负中心组合的和与 \(\zeta_0\) 分离，不参与该值。
\(\chi(\zeta_0)=1\)，连续的 Fourier 输出在邻域内非零，
所以最后的 \(L^2\) 范数严格为正。

## 4. 周期化及精确能量归一化

令 \(\mathbb T_N^3=\mathbb R^3/(2\pi N\mathbb Z^3)\)，以
\([-\pi N,\pi N)^3\) 为基本胞。写 \({\cal S}_NG=\sum_{\ell\in\mathbb Z^3}
G(\,\cdot+2\pi N\ell)\)，并定义
\[
 V_N={\cal S}_NF,\qquad
 d_N=\frac{\sqrt{2E_0}}{\|V_N\|_{L^2(\mathbb T_N)}},\qquad
 W_N=d_NV_N,\qquad
 d_N\longrightarrow d=\frac{\sqrt{2E_0}}{\|F\|_2}>0 .
 \tag{FA.10}
\]
所有扩大环面范数仍未归一化。对每个固定整数 \(m\)，
\(\|V_N\|_{H^m(\mathbb T_N)}\to\|F\|_{H^m(\mathbb R^3)}\)。
证明：在基本胞内，所有非零影像及其固定阶导数均为
\(O_M(N^{-M})\)，其中 \(M\) 可任意大；其 \(L^2\) 误差至多
\(O_M(N^{3/2-M})\)。再让基本胞扩大覆盖 \(\mathbb R^3\) 即得范数收敛。
于是 \(W_N\) 在每个固定 \(H^m\) 中一致有界。

扩大环面上的频率为 \(\xi=k/N\)。用 \({\cal Q}_N\) 表示符号为
\(\chi(k/N)\) 的乘子，用 \({\cal P}_N\) 表示 Leray 投影。
注意这里 \(Q_N\) 是固定环面上的物理乘子，
\({\cal Q}_N\) 是扩大环面上固定物理频率的乘子。
周期 Fourier 系数为
\(\widehat V_N(k)=(2\pi N)^{-3}\widehat F(k/N)\)，所以
\({\cal Q}_NW_N=0\) 且初始频谱仍在 \(1<|k/N|<2\)。
此外，
\[
 G_N:={\cal Q}_N{\cal P}_N\operatorname{div}(W_N\otimes W_N),
 \qquad \|G_N\|_{L^2(\mathbb T_N)}
 \longrightarrow d^2\gamma_F=:\gamma>0 .
 \tag{FA.11}
\]
完整证明不需要忽略周期影像的乘积。由前述 Schwartz 尾估计，
\(\|V_N\otimes V_N-{\cal S}_N(F\otimes F)\|_2\to0\)。
算子 \({\cal Q}_N{\cal P}_N\operatorname{div}\) 的符号光滑、紧支撑
且远离零频，在 \(L^2\) 中一致有界，并与 \({\cal S}_N\) 精确交换。
故 \(G_N-d_N^2{\cal S}_N\Gamma_F\to0\) 于 \(L^2(\mathbb T_N)\)。
\(\Gamma_F\) 也是 Schwartz，应用同一周期化范数极限即得 FA.11。

## 5. 完整非线性解上的统一余项

在扩大环面上令 \(U_N\) 解完整 NS，初值 \(W_N\)、黏性
\(\varepsilon_N=\nu N^{-1/2}\)。只取足够大的 \(N\)，使
\(0<\varepsilon_N\le1\)。

这里沿用并核对 AJ.5–AJ.15 的扩大环面方法，而非仅引用一个可能依赖
环面大小的寿命常数。对 \(N\ge1\)，
\[
 N^{-3}\sum_{k\in\mathbb Z^3}(1+|k/N|^2)^{-\sigma}\le C_\sigma
 \quad(\sigma>3/2),\qquad
 \frac12\frac d{d\tau}\|U_N\|_{H^5}^2
 +\varepsilon_N\|\nabla U_N\|_{H^5}^2
 \le C\|U_N\|_{H^5}^3 .
 \tag{FA.12}
\]
第一个式子由格点分壳给出，其体积因子保证
\(H^5\to W^{3,\infty}\) 和 \(H^2\to L^\infty\) 的常数统一；
不用随 \(N\) 变差的 Poincaré 常数。
第二式按整数 Leibniz 展开：主输运项抵消，其余两个导数阶数之和
至多 6、各自至多 5，至少一个至多 3，可放入 \(L^\infty\)。

FA.10 的初始统一界与 FA.12 给出某个固定 \(\tau_*>0\)，使
\[
 \sup_{N,\,0\le\tau\le\tau_*}\|U_N(\tau)\|_{H^5}\le M,\qquad
 \|\partial_\tau U_N(\tau)\|_{H^3}\le C_M,\qquad
 \|U_N(\tau)-W_N\|_{H^3}\le C_M\tau .
 \tag{FA.13}
\]
可用与 AJ 相同的 Fourier–Galerkin 及高阶延拓论证得到此窗上的
唯一光滑解；初值虽由紧支撑副本换成 Schwartz 周期化，但这些论证
仅使用统一 Sobolev 初值上界，FA.10 已给出该输入。

记 \({\cal B}_N(Z)={\cal Q}_N{\cal P}_N\operatorname{div}(Z\otimes Z)\)。
其在这个 \(H^5\) 有界集上满足
\(\|{\cal B}_N(Z)-{\cal B}_N(Y)\|_2\le C_M\|Z-Y\|_2\)，
因为频率截断后的导数乘子 \(L^2\to L^2\) 一致有界，
而 \(\|Z\otimes Z-Y\otimes Y\|_2
\le(\|Z\|_\infty+\|Y\|_\infty)\|Z-Y\|_2\)。
因此完整 mild 方程给
\[
 \begin{aligned}
 {\cal Q}_NU_N(\tau)
 &=-\int_0^\tau e^{\varepsilon_N(\tau-s)\Delta}{\cal B}_N(U_N(s))\,ds,\\
 \|{\cal Q}_NU_N(\tau)+\tau G_N\|_2&\le C_0\tau^2 .
 \end{aligned}
 \tag{FA.14}
\]
第二式先用 FA.13 控制非线性源差为 \(C_Ms\)。
冻结的 \(G_N\) 位于 \(|k/N|<2.2\)，故
\(\|(e^{\varepsilon_Nr\Delta}-I)G_N\|_2
\le(2.2)^2\varepsilon_Nr\|G_N\|_2\le Cr\)；
积分得到余项。所有常数与 \(N\) 无关。
这控制的是完整非线性解，不是第一 Picard 项替代真实轨道。

取 \(0<\tau_0\le\tau_*\)，使 \(C_0\tau_0\le\gamma/4\)，
并取 \(N\) 足够大使 \(\|G_N\|_2\ge\gamma/2\)。
于是
\[
 \|{\cal Q}_NU_N(\tau_0)\|_2\ge\tau_0\gamma/4=:b_*>0 .
 \tag{FA.15}
\]

## 6. 回到固定环面与首次到达

令
\[
 u^{(N)}(t,x)=N^{3/2}U_N(N^{5/2}t,Nx),\qquad
 p^{(N)}(t,x)=N^3P_N(N^{5/2}t,Nx),\qquad
 t_N=\tau_0N^{-5/2}.
 \tag{FA.16}
\]
直接代入方程，黏性恰为 \(\nu\)，不是一个受迫或删减模型。
空间积分换元给
\(\|u^{(N)}(0)\|_2^2=\|W_N\|_2^2=2E_0\)，以及
\(\|Q_Nu^{(N)}(t_N)\|_2=\|{\cal Q}_NU_N(\tau_0)\|_2\ge b_*\)。

选定 \(\eta=b_*^2/8\)。由能量及 \(0\le\chi\le1\)，
\(b_*^2\le2E_0\)，故 \(0<\eta<E_0\)。
目标带初始为零，在 \(t_N\) 的能量至少 \(b_*^2/2>\eta\)；
光滑连续性使首次到达 \(T_N\in(0,t_N]\) 存在且能量等于 \(\eta\)。
FA.3 给所需的下界，FA.16 给上界。
另外，
\[
 \nu\int_0^{t_N}\|\nabla_xu^{(N)}(t)\|_2^2\,dt
 =\nu N^{-1/2}\int_0^{\tau_0}\|\nabla_yU_N(\tau)\|_2^2\,d\tau
 \le\nu M^2\tau_0N^{-1/2}.
 \tag{FA.17}
\]
这完成 FA.4。

## 7. 这项结论没有证明什么

- 被否定的是仅由固定能量、固定黏性和频率决定的普遍抛物激活下界，
  不是“激活之后必有某段驻留”的命题；后者还未在这里检验。
- 初始高阶范数随 \(N\) 增长。结论不否定依赖完整初值、
  初始临界范数或既有成熟历史的时间估计。
- 不假设正时间内有限 Fourier 支持持续，不截断完整非线性，
  不假设相邻带闭包，也不为构造添加外力。
- 这是不同初值的有限时间光滑解族，不构造单条解的无限重复转移、
  有限时间奇点或任何长期行为。
- FA.3–4 不控制给定中心的移动壳、带符号压力功或总级联次数。
  G、R216–R217、一般终端缺口消失及一般三维正则性仍 OPEN。

同一 \(N^{-5/2}\) 固定能量缩放与统一短时工具已经出现在
research/clay_b_short_time_pressure_work_preflight_20260906.md（AJ.2–AJ.15）。
频带源的 Bernstein 幂次和 mild 方法是经典工具。此次给出的是这些工具
对一个精确频带激活问题的完整匹配，并非已证新颖性或高水平论文价值。
Luo 的局部 BKM 窗口仍需额外的低频梯度积分小量，不能与本页的
能量级激活时间混同；来源范围与本地去重另见审查记录。
