# R0.71H 主源文献台账：时间角变差、占用与穿越

状态：正式文献边界审计
检索日期：2026-08-25
用途：为 R0.71H 的非循环性审计提供可追溯的主源先例，不进入正式报告。

## 限定检索与非原创性声明

本台账是一次限定检索，不是系统综述。检索仅覆盖与下列接口直接相关的 11 个高信号主源：归一化涡量方向的时间演化、压力 Hessian/源曲率、空间涡量方向相干、动态耗散波数、时间—频率 occupation、频率窗、间歇事件宽度，以及 BV—穿越次数恒等式。来源限于作者论文、官方 arXiv 或期刊 DOI 页面；未把二手综述当作定理依据。

“未发现现成定理”只表示在上述限定检索范围内未发现直接覆盖 R0.71H 目标的结果，不构成完备的全球文献排除，也不构成原创性、新颖性、优先权或可发表性的证明。任何原创性声明仍须经过更广的主题词、引文网络、MathSciNet/zbMATH 和专家审阅核验。

本台账审计的目标预算为

\[
\sum_{j,Q}K_j^{-2}\operatorname{Var}_t(a_{j,Q,\varepsilon}),
\]

其中关键对象是归一化、局域化、投影后的 Lamb/涡量方向；还要求对壳、空间块、移动截断、\(\varepsilon\) 和零分母缺陷面一致。

## Claim-to-source ledger

### 1. Gibbon–Holm–Kerr–Roulstone：物质涡量方向与压力源曲率

主源：[arXiv:nlin/0512034](https://arxiv.org/abs/nlin/0512034)；[DOI:10.1088/0951-7715/19/8/011](https://doi.org/10.1088/0951-7715/19/8/011)。

- 精确定义：
  \[
  \alpha=\widehat\omega\cdot S\widehat\omega,
  \qquad
  \chi=\widehat\omega\times S\widehat\omega,
  \qquad
  \frac{D\widehat\omega}{Dt}=\chi\times\widehat\omega.
  \]
  对压力 Hessian \(P=\nabla^2p\)，定义
  \(\alpha_p=\widehat\omega\cdot P\widehat\omega\)、
  \(\chi_p=\widehat\omega\times P\widehat\omega\)。
- 定理：Theorem 1 给出相应四元数 Riccati 方程；Theorem 2 以
  \(\int_0^{t_*}\|\chi_p(t)\|_\infty\,dt<\infty\)
  为 Euler 延拓条件，并有涡量方向与压力 Hessian 特征向量共线的退化例外。
- 尺度：\(\chi\) 是物质角速度；按 NSE 抛物标度，\(\chi\sim K^2\)、\(\chi_p\sim K^4\)。
- BV/穿越：不控制总变差或穿越次数，只提供精确角速度恒等式和条件正则性。
- 与 R0.71H 的错位：对象是 Euler 物质涡量，无黏性、Littlewood–Paley 壳、局域投影 Lamb 向量、移动 cutoff/collar、\(Y\) 归一化和零分母面；\(L_t^1L_x^\infty\) 源曲率本身也是强正则性输入。

### 2. Beirão da Veiga–Berselli：涡量方向相干的正则化效应

主源：[作者 PDF](https://people.dm.unipi.it/beiraodaveiga/pdf/hbv-79.pdf)；[DOI:10.57262/die/1356060864](https://doi.org/10.57262/die/1356060864)。

- 精确假设：在两点涡量均高于阈值的区域，\(\alpha\in[1/2,1]\)，
  \[
  |\sin\theta(\xi(x),\xi(x+y))|
  \le g(t,x)|y|^\alpha,
  \qquad
  g\in L_t^aL_x^b,
  \qquad
  \frac2a+\frac3b=\alpha-\frac12,
  \]
  且 \(a\in[4/(2\alpha-1),\infty]\)。Theorem 1.2 对 \(u_0\in H^1\) 的弱解推出强正则性。
- 相关无条件估计：若 \(\omega_0\in L^1\)，文中的估计 (3.2) 为
  \[
  \|\omega(t)\|_1
  +\nu\int_0^t\!\int |\omega|\,|\nabla\xi|^2
  \le \|\omega_0\|_1+2\nu^{-1}\|u_0\|_2^2.
  \]
- 尺度：方向相干条件位于临界指数族；后一项是加权空间方向 Fisher 信息。
- BV/穿越：只控制空间方向梯度的加权积分，不控制时间 BV 或穿越。
- 错位：没有从 \(\nabla_x\xi\) 到归一化局域 projected-Lamb 方向 \(\partial_t\) 的传递定理。

### 3. Vasseur：速度方向散度判据

主源：[arXiv:0705.2446](https://arxiv.org/abs/0705.2446)；[作者 PDF](https://web.ma.utexas.edu/users/vasseur/documents/preprints/NSdirection2.pdf)。

- 定理：Theorem 1 假设
  \[
  \operatorname{div}(u/|u|)\in L_t^pL_x^q,
  \qquad
  \frac2p+\frac3q\le\frac12,
  \qquad q\ge6, p\ge4,
  \]
  则解光滑。恒等式
  \(|u|\operatorname{div}(u/|u|)=-(u/|u|)\cdot\nabla|u|\)
  是其方向机制接口。
- 尺度：空间速度方向的临界/次临界混合范数条件。
- BV/穿越：否。
- 错位：控制的是速度方向散度，不是时间角变差；无壳分解、局域化、源曲率和零分母审计。

### 4. Dascaliuc–Grujić：临界涡量方向相干与局域烯量级联

主源：[arXiv:1107.0058](https://arxiv.org/abs/1107.0058)；[DOI:10.1007/s00220-012-1595-8](https://doi.org/10.1007/s00220-012-1595-8)。

- 精确假设：A1 在指定高梯度局域区假设
  \[
  |\sin\varphi(\xi(x,t),\xi(y,t))|\le C_1|x-y|^{1/2}.
  \]
  A2 要求修改后的 Kraichnan 尺度
  \(\sigma_0=(E_0/P_0)^{1/2}<\beta R_0\)；A3 包含局域化小量和终端烯量调制条件。
- 定理：Theorem 4.1 对相应 Leray 解给出
  \[
  \frac{1}{4K_*}P_0\le\langle\Phi\rangle_R\le4K_*P_0,
  \qquad \sigma_0/\beta\le R\le R_0.
  \]
- 尺度：\(1/2\)-Hölder 是三维涡量方向相干削弱 vortex stretching 的临界空间阈值。
- BV/穿越：不控制；终端时间调制是额外假设。
- 错位：结论是物理尺度级联，不是时间旋转；时间调制没有从 Leray 预算推出，也没有局域有符号 projected-Lamb 商。

### 5. Cheskidov–Shvydkoy：动态耗散波数

主源：[arXiv:1102.1944](https://arxiv.org/abs/1102.1944)；[DOI:10.1007/s00021-014-0167-4](https://doi.org/10.1007/s00021-014-0167-4)。

- 定义：\(\Lambda(t)=\lambda_{Q(t)}\)，其中高模满足
  \(\lambda_p^{-1}\|u_p(t)\|_\infty<c_0\nu\) 对所有 \(p>Q(t)\)。
- 定理：Theorem 3.1/Corollary 3.3 以
  \[
  f(t)\simeq\|\omega_{\le Q(t)}(t)\|_{B^0_{\infty,\infty}}
  \in L_t^1
  \]
  推出正则性。Lemma 4.1 对每个 Leray–Hopf 解给出 \(\Lambda\in L_t^1\)，而 \(\Lambda\in L_t^{5/2}\) 足以正则。
- 尺度：\(\Lambda\in L_t^2\) 才是 NSE 临界；无条件 \(L^1\) 经 Chebyshev 只给 \(K^{-1}\) 占用尾。
- BV/穿越：否。
- 错位：无条件结果比所需 \(K^{-2}\) 少一阶，也完全没有方向变差；更强可积性已是正则性输入。

### 6. Cheskidov–Dai：临界振幅加权时间—频率 occupation

主源：[arXiv:1507.06611](https://arxiv.org/abs/1507.06611)。

- 定义：
  \[
  \Lambda_r(t)=\lambda_{Q_r(t)},
  \quad
  \lambda_p^{-1+3/r}\|u_p(t)\|_r
  <c_r\min(\nu,\mu),\quad p>Q_r(t).
  \]
- 定理：Theorem 1.1 假设
  \[
  \limsup_{q\to\infty}
  \int_{T/2}^{T}
  \mathbf1_{\{q\le Q_r(t)\}}
  \|\Delta_q\omega(t)\|_\infty\,dt
  \le c_r,
  \]
  则可延拓过 \(T\)。Theorem 1.3 给出若干单壳终端积分、低模 Besov 条件和临界壳振幅条件的充分版本。
- 尺度：\(\|\Delta_q\omega\|_\infty dt\) 在 NSE 标度下不变，是临界的振幅加权 occupation。
- BV/穿越：不控制方向 BV 或穿越；也不控制无权 episode 长度。
- 错位：这是最接近的 occupation 先例，但它是假设的小量正则性判据，不是 Leray 推论；没有局域移动中心、方向、signed work 或分母退化。

### 7. Cheskidov–Shvydkoy：\(B^{-1}_{\infty,\infty}\) 跳跃与壳振幅

主源：[arXiv:0708.3067](https://arxiv.org/abs/0708.3067)；[DOI:10.1007/s00205-009-0265-2](https://doi.org/10.1007/s00205-009-0265-2)。

- 定理：Theorem 3.1 假设
  \[
  \sup_{t\in(0,T]}
  \limsup_{t_0\to t^-}
  \|u(t)-u(t_0)\|_{B^{-1}_{\infty,\infty}}<c\nu,
  \]
  则正则。Lemma 4.1/Theorem 4.2 使用
  \[
  \int
  \bigl(\lambda_q^{2/r-1}\|u_q\|_\infty\bigr)^r,dt,
  \qquad r>2.
  \]
- 尺度：均为 NSE 临界的 Besov 跳跃或壳振幅条件。
- BV/穿越：只限制单次左跳或振幅积分，不求和所有跳跃，因而不控制总变差或穿越数。
- 错位：小跳允许无限振荡；对象不是角变量，且没有局域中心、投影 Lamb 结构和零分母面。

### 8. Bradshaw–Grujić：动态频率窗与 frequency envelope

主源：[arXiv:1501.01043](https://arxiv.org/abs/1501.01043)；[DOI:10.1007/s00205-016-1069-9](https://doi.org/10.1007/s00205-016-1069-9)。

- 定义：对 \(\varepsilon\in(0,1)\)，以 \(\dot B^{-\varepsilon}_{\infty,\infty}\) 范数定义动态窗口 \(J_{\rm low}(t)\le j\le J_{\rm high}(t)\)。
- 定理：Theorem 2 假设
  \[
  \int_0^T
  \left(
  \sup_{J_{\rm low}(t)\le j\le J_{\rm high}(t)}
  \lambda_j^{-\varepsilon}\|\Delta_j u(t)\|_\infty
  \right)^{2/(1-\varepsilon)}dt<\infty,
  \]
  则正则。Theorem 1 给出按局部 lifespan 分隔的有限时间采样判据。
- 尺度：时间指数 \(2/(1-\varepsilon)\) 与 Besov 阶数构成 NSE 临界组合。
- BV/穿越：否，只控制动态频率窗内的振幅。
- 错位：可作为 frequency-envelope 先例，但局部 lifespan 依赖强范数，不产生纯 \(K^{-2}\) 的角向 residence/crossing 预算。

### 9. Gibbon–Doering：bad/dangerous interval 的宽度

主源：[arXiv:math/0406146](https://arxiv.org/abs/math/0406146)；[DOI:10.1007/s00205-005-0382-5](https://doi.org/10.1007/s00205-005-0382-5)。

- 定义：周期强迫 NSE 中
  \[
  F_n=\|\nabla^nu\|_2^2+\tau^2\|\nabla^nf\|_2^2,
  \qquad
  \kappa_n=(F_n/F_0)^{1/(2n)}.
  \]
- 定理：Theorem 5 对 bad intervals 给出 Reynolds 数负幂或 \(Re^{-1}\log Re\) 的宽度上界；Theorem 7 对 dangerous subintervals 给出
  \(\omega_0\Delta t_+\le c_nRe^{-b_n}\)，\(b_n>1\)。
- 尺度：事件由全局导数比和 Reynolds 数刻画，不是固定频率壳事件。
- BV/穿越：给出事件宽度，但不控制事件数量、交叠、角方向 BV 或 crossing count。
- 错位：不能转化为局域壳上的 \(K^{-2}\) 角向驻留律；强迫周期背景与候选终端奇异区间也不同。

### 10. Łochowski：BV 与穿越次数的精确接口

主源：[arXiv:1503.01746](https://arxiv.org/abs/1503.01746)；[DOI:10.4064/cm6583-3-2017](https://doi.org/10.4064/cm6583-3-2017)。

- 定理：连续函数的 Banach indicatrix 公式为
  \[
  TV(f,[a,b])=\int_{\mathbb R}N_y(f)\,dy.
  \]
  Theorem 1 对 regulated 函数给出截断变差
  \[
  TV^c(f)=\int_{\mathbb R}n_c^y(f)\,dy,
  \]
  并有相应上、下穿越公式。
- 尺度：纯一维几何测度恒等式；乘以 \(K_j^{-2}\) 后两端保持相等。
- BV/穿越：是；这是 BV 与积分穿越次数的精确等价，而非估计损失。
- 错位：不提供任何 NSE 预算。它只能证明“已有 BV 即可换成平均 crossing 控制”，不能产生 BV。

### 11. Cheskidov–Dai：determining wavenumber 的长时间平均

主源：[arXiv:1510.00379](https://arxiv.org/abs/1510.00379)；[DOI:10.1017/PRM.2018.33](https://doi.org/10.1017/PRM.2018.33)。

- 定理背景：对周期强迫、完整有界 Leray–Hopf 轨道定义 determining wavenumber \(\Lambda_u(t)\)。Theorem 1.1 说明若两条轨道在其 determining wavenumber 以下对全部过去时间一致，则轨道相同。
- 平均估计：
  \[
  \langle\Lambda_u\rangle-\lambda_0
  \le C_{\delta,d}\kappa_d,
  \qquad d\in[\delta,3),
  \]
  \(d=3\) 时带对数修正。
- 尺度：长时间统计、间歇维数和 Kolmogorov 耗散尺度；由一阶均值通过 Markov 至多得到 \(K^{-1}\) 型 occupation 尾。
- BV/穿越：否。
- 错位：不能用于有限终端候选奇异区间；无方向、局域 signed quotient 或时间总变差。

## 明确剩余缺口

1. **完整局域方向方程。** 需写出归一化方向的精确 NSE 演化，包括 \(\partial_tL\)、全部 inter-shell pairs、压力/投影、黏性与 LP/截断交换子、移动 cutoff/collar、\(Y\) 归一化，以及 \(\varepsilon\) 和零分母缺陷面。

2. **非循环角向预算。** 核心仍是从 Leray 级数据控制
   \[
   \int_I
   \frac{|P_{C^\perp}\partial_tC|}{|C|+\varepsilon}\,dt
   \]
   或相应 projected-Lamb 源曲率项。若右端要求
   \(\|\chi_p\|_{L_t^1L_x^\infty}\)、Serrin/Besov 条件、Cheskidov–Dai occupation，或直接假设目标 BV/crossing，则属于已知正则性输入或循环。

3. **壳—空间块—正则化一致可和性。** 单个 \((j,Q)\) 的条件 BV 不足；需证明 \(K_j^{-2}\) 加权后对 \(j,Q\) 可和，并能一致通过 \(\varepsilon\downarrow0\)，同时保留端点跳跃和零分母缺陷测度。

4. **从振幅加权 occupation 到无权事件。** \(\|\Delta_q\omega\|_\infty dt\) 型控制不能自动给 episode 长度或 crossing count；还缺事件上的振幅下界、横截性或其他非退化机制。

5. **空间方向到时间方向的传递。** 现有 \(\int|\omega||\nabla\xi|^2\) 或 Hölder coherence 结果没有导出归一化局域 projected-Lamb 方向的时间变差。

6. **长时间统计与终端区间的断层。** determining-wavenumber 的吸引子时间平均不能替代候选奇异时间附近的局部预算。

## 文献通道判定

限定检索的结论是：**未发现与目标预算直接重合的先例，但也没有现成闭合工具。** 最接近的三个独立部件分别是：Gibbon 等的精确角速度/压力源曲率恒等式、Cheskidov–Dai 的临界振幅加权 occupation，以及 Łochowski 的 BV—crossing 等价。现有主源没有把三者在 Leray 级、局域壳化、零分母可控的框架内连接起来。

因此 R0.71H 的下一道非循环门应是：先建立带完整源项台账的条件性归一化方向 BV 恒等式/不等式，再逐项审计右端能否由 Leray 预算控制。若最终只复述已知正则性条件或假设目标变差，则 temporal-residence 分支应停止。
