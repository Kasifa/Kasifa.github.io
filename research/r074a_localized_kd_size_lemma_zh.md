# R0.74A | 混合 heat covariance 的局部 size 引理

**整理日期：** 2026-09-01

**状态：** `PROVED_SIZE_LEMMA + FINITE_DECLARED_TAILS + OPEN_ABSORPTION`

**主张类型：** 正尺度解析估计；不是正则性判据

**区域：** 归一化环面
\(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\)，并使用其欧氏提升

**依赖：** `r073x_problem_freeze.md`、
`r073x_exterior_tail_freeze.md` 和
`r073z_finiteness_obstruction_and_repair.md`

本笔记证明下列量的一个局部上界：

\[
 \mathcal K_D^\square(z_0,R;\theta)
 =\frac{\nu}{R^2}\int_{I_R^\square}\int_0^{\theta R^2}
   \int_{B_R}D_s\sqrt{k_s}\,dx\,ds\,dt.
\tag{0.1}
\]

该估计把 Gaussian 滤波器的输入分为局部核心与提升后的外部环带。core--core 项由已冻结、与时间钟匹配的局部能量控制。其余三项需要一个新的二次 Gaussian 尾项，即带有本质时间上确界的环带速度能量；同时还需要 R0.73X 已冻结的有利环带梯度能量尾
\(\mathcal D_{\rm ext}^{\square}\)。

R0.73X 的旧 exterior functional 包含 \(|u|^3\)、
\(|p|^{3/2}\)，以及用于 pressure tail 的代数加权 \(|u|^2\) 项，但不包含外部梯度能量。因此，它本身不能作为本笔记所证估计的右端。

这只是一个 size 引理。它没有证明任何尾项是小的、可吸收的、紧的，或由更小柱上的数据决定。

---

## 1. 冻结定义与时间钟说明

R0.73X 冻结的标准时间区间和黏度适配时间区间为

\[
 I_R^{\rm std}=(t_0-R^2,t_0),
 \qquad
 I_R^\nu=(t_0-R^2/\nu,t_0).
\tag{1.1}
\]

由于 Navier--Stokes 缩放不改变 \(\nu\)，两个区间都按抛物尺度缩放，但二者不能互换。

对任一时间钟，R0.73X 冻结的规范局部能量是

\[
 \mathcal E^\square(z_0,\rho)
 =\frac1\rho\mathop{\rm ess\,sup}_{t\in I_\rho^\square}
   \int_{B_\rho}|u|^2\,dx
 +\frac\nu\rho\int_{I_\rho^\square}\int_{B_\rho}
   |\nabla u|^2\,dx\,dt,
 \qquad \square\in\{{\rm std},\nu\}.
\tag{1.2}
\]

下面每一处比较都在等式两侧使用同一个 \(\square\)。本文没有把 \(I_R^\nu\) 换成标准区间，也没有作相反替换。由于右端使用半径 \(4R\)，共同量词为

\[
 I_{4R}^\square\Subset(0,T).
\tag{1.3}
\]

令 \(P_s=e^{s\Delta}\) 为周期 heat 半群。在几乎每个满足
\(u(t)\in H^1(\mathbb T^3)\) 的物理时刻，定义

\[
 \begin{aligned}
 k_s&=\frac12\bigl(P_s|u|^2-|P_su|^2\bigr),\\
 D_s&=P_s|\nabla u|_F^2-|\nabla P_su|_F^2.
 \end{aligned}
\tag{1.4}
\]

精确 variance 公式给出

\[
 0\le k_s\le\frac12P_s|u|^2,
 \qquad
 0\le D_s\le P_s|\nabla u|_F^2.
\tag{1.5}
\]

全文均假设

\[
 0<R<\frac\pi8,
 \qquad 0<\theta\le1,
 \qquad I_{4R}^\square\Subset(0,T),
\tag{1.6}
\]

以及

\[
 u\in L_t^\infty L_x^2(I_{4R}^\square\times\mathbb T^3)
 \cap L_t^2H_x^1(I_{4R}^\square\times\mathbb T^3).
\tag{1.7}
\]

pressure 不进入 (0.1) 或定理 4.1；它只通过推论 4.3 中继承的 pressure-tail 接口进入。

---

## 2. 提升环带与两个二次外部输入

固定 \(\widetilde x_0\in\mathbb R^3\) 为 \(x_0\) 的一个提升，并以
\(\widetilde u\) 表示周期提升。令

\[
 C_R=B_{2R}(\widetilde x_0),
 \qquad E_R=\mathbb R^3\setminus C_R,
\tag{2.1}
\]

并对 \(m\ge1\) 定义

\[
 A_m(R)=\{y:2^mR\le|y-\widetilde x_0|<2^{m+1}R\}.
\tag{2.2}
\]

忽略零测边界后，这些环带分割 \(E_R\)，并包含周期场的全部格点副本。使用 R0.73X 冻结的权重

\[
 \gamma_m(\theta)
 =\theta^{-2}\exp\!\left(-\frac{4^{m-1}}{32\theta}\right).
\tag{2.3}
\]

对几乎每个 \(t\in I_R^\square\)，定义

\[
 \begin{aligned}
 U_\gamma(t;R,\theta)
 &=\sum_{m\ge1}\gamma_m(\theta)
   \int_{A_m(R)}|\widetilde u(t,y)|^2\,dy,\\
 G_\gamma(t;R,\theta)
 &=\sum_{m\ge1}\gamma_m(\theta)
   \int_{A_m(R)}|\nabla\widetilde u(t,y)|_F^2\,dy.
 \end{aligned}
\tag{2.4}
\]

下面使用的尺度不变量为

\[
 \boxed{
 \begin{aligned}
 \mathcal U_{\rm ext}^{\infty,\square}(z_0,R;\theta)
 &=\mathop{\rm ess\,sup}_{t\in I_R^\square}
   \frac{U_\gamma(t;R,\theta)}R,\\
 \mathcal G_{\nabla,\rm ext}^{1,\square}(z_0,R;\theta)
 &=\frac\nu R\int_{I_R^\square}G_\gamma(t;R,\theta)\,dt.
 \end{aligned}}
\tag{2.5}
\]

上标记录的是时间指数，不是导数阶数。第二行不是新的尾项：与 R0.73X 的 (7.2) 比较可得精确恒等式

\[
 \boxed{
 \mathcal G_{\nabla,\rm ext}^{1,\square}(z_0,R;\theta)
 =\mathcal D_{\rm ext}^{\square}(z_0,R;\theta).}
\tag{2.5a}
\]

本笔记只新引入
\(\mathcal U_{\rm ext}^{\infty,\square}\)。下文继续使用
\(\mathcal D_{\rm ext}^{\square}\) 的记号。

### 引理 2.1：尾项的缩放与有限性

在

\[
 u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x),
 \qquad R_\lambda=R/\lambda,
\tag{2.6}
\]

以及相应缩放后的中心和区间下，

\[
 \mathcal U_{\rm ext}^{\infty,\square}[u_\lambda]
 =\mathcal U_{\rm ext}^{\infty,\square}[u],
 \qquad
 \mathcal D_{\rm ext}^{\square}[u_\lambda]
 =\mathcal D_{\rm ext}^{\square}[u].
\tag{2.7}
\]

在 (1.7) 下，这两个量均有限。

#### 证明

在对应环带上，

\[
 \int|u_\lambda|^2\,dx=\lambda^{-1}\int|u|^2\,dx,
 \qquad
 \int|\nabla u_\lambda|^2\,dx
 =\lambda\int|\nabla u|^2\,dx.
\tag{2.8}
\]

结合 \(R_\lambda^{-1}=\lambda R^{-1}\) 与
\(dt_\lambda=\lambda^{-2}dt\)，即可得到 (2.7)；其中周期格点按照标准的局部 Navier--Stokes 缩放约定一同缩放。

每个提升环带至多包含
\(C[1+(2^mR)^3]\) 个基本胞元。因此

\[
 \begin{aligned}
 U_\gamma(t)
 &\le C\|u(t)\|_{L^2(\mathbb T^3)}^2
   \sum_{m\ge1}\gamma_m[1+(2^mR)^3],\\
 G_\gamma(t)
 &\le C\|\nabla u(t)\|_{L^2(\mathbb T^3)}^2
   \sum_{m\ge1}\gamma_m[1+(2^mR)^3].
 \end{aligned}
\tag{2.9}
\]

由于 \(\gamma_m\) 的衰减快于几何级数，上述级数收敛；再由 (1.7) 即得有限性。\(\square\)

---

## 3. 正的核心/外部上界分解

对 \(x\in B_R\) 和 \(0<s\le\theta R^2\)，定义

\[
 \begin{aligned}
 U_c&=\int_{C_R}g_s(\widetilde x-y)|\widetilde u(y)|^2\,dy,
 &U_e&=\int_{E_R}g_s(\widetilde x-y)|\widetilde u(y)|^2\,dy,\\
 G_c&=\int_{C_R}g_s(\widetilde x-y)|\nabla\widetilde u(y)|_F^2\,dy,
 &G_e&=\int_{E_R}g_s(\widetilde x-y)|\nabla\widetilde u(y)|_F^2\,dy.
 \end{aligned}
\tag{3.1}
\]

它们是未中心化矩的正分块，并不是彼此独立的 covariance。由 (1.5)，

\[
 \boxed{
 D_s\sqrt{k_s}
 \le\frac1{\sqrt2}\left(
 G_c\sqrt{U_c}+G_c\sqrt{U_e}
 +G_e\sqrt{U_c}+G_e\sqrt{U_e}\right).}
\tag{3.2}
\]

这就是定理所用的 core/core、core/exterior、exterior/core 和 exterior/exterior 分解。

本文不主张存在精确的四项 covariance 恒等式。若在 covariance 内直接分解
\(u=1_{C_R}u+1_{E_R}u\)，会产生如下交叉项：

\[
 -2(P_s(1_{C_R}\nabla u)):(P_s(1_{E_R}\nabla u)),
\tag{3.3}
\]

而速度 covariance 的平方根也不能线性展开。正的上界分解 (3.2) 避开了这一错误恒等式。

R0.73X 的 Gaussian 环带引理在完整尺度区间上一致给出

\[
 \boxed{
 U_e(t,x,s)\le CR^{-3}U_\gamma(t),
 \qquad
 G_e(t,x,s)\le CR^{-3}G_\gamma(t).}
\tag{3.4}
\]

同时，

\[
 \int_{B_R}G_c(t,x,s)\,dx
 \le\int_{B_{2R}}|\nabla u(t,y)|_F^2\,dy.
\tag{3.5}
\]

最后，周期 heat 超收缩性给出

\[
 \|U_c(t,\cdot,s)\|_{L^\infty(B_R)}^{1/2}
 \le C_{\mathbb T^3}s^{-3/4}
 \|u(t)\|_{L^2(B_{2R})}.
\tag{3.6}
\]

---

## 4. 局部 size 定理

对 \(I=I_R^\square\)，令

\[
 \begin{aligned}
 A_c(I,R)
 &=\frac1R\mathop{\rm ess\,sup}_{t\in I}
   \int_{B_{2R}}|u(t)|^2\,dx,\\
 B_c(I,R)
 &=\frac\nu R\int_I\int_{B_{2R}}|\nabla u|_F^2\,dx\,dt.
 \end{aligned}
\tag{4.1}
\]

### 定理 4.1：core/exterior Gaussian size 引理

假设 (1.6)--(1.7) 成立，则

\[
 \boxed{
 \begin{aligned}
 \mathcal K_D^\square(z_0,R;\theta)
 \le C_{\mathbb T^3}\big[&
 \theta^{1/4}A_c^{1/2}B_c
 +\theta B_c(\mathcal U_{\rm ext}^{\infty,\square})^{1/2}\\
 &+\theta^{1/4}A_c^{1/2}\mathcal D_{\rm ext}^{\square}
 +\theta(\mathcal U_{\rm ext}^{\infty,\square})^{1/2}
   \mathcal D_{\rm ext}^{\square}\big].
 \end{aligned}}
\tag{4.2}
\]

由于 \(0<\theta\le1\)，还可推出因子化估计

\[
 \mathcal K_D^\square
 \le C_{\mathbb T^3}\theta^{1/4}
 \left(A_c^{1/2}+(\mathcal U_{\rm ext}^{\infty,\square})^{1/2}\right)
 \left(B_c+\mathcal D_{\rm ext}^{\square}\right).
\tag{4.3}
\]

对任一时间钟，与之匹配的 R0.73X 局部能量给出

\[
 \boxed{
 \mathcal K_D^\square(z_0,R;\theta)
 \le C_{\mathbb T^3}\theta^{1/4}
 \left[
 \mathcal E^\square(z_0,4R)
 +\mathcal U_{\rm ext}^{\infty,\square}(z_0,R;\theta)
 +\mathcal D_{\rm ext}^{\square}(z_0,R;\theta)
 \right]^{3/2}.}
\tag{4.4}
\]

这里，\(\mathcal K_{D,cc}\) 表示 (3.2) 中由
\(G_c\sqrt{U_c}/\sqrt2\) 产生的贡献。

#### 证明：core--core

由 (3.5)--(3.6)，

\[
 \int_{B_R}G_c\sqrt{U_c}\,dx
 \le Cs^{-3/4}
 \|u(t)\|_{L^2(B_{2R})}
 \|\nabla u(t)\|_{L^2(B_{2R})}^2.
\tag{4.5}
\]

又因为

\[
 \int_0^{\theta R^2}s^{-3/4}\,ds
 =4\theta^{1/4}R^{1/2},
\tag{4.6}
\]

所以

\[
 \mathcal K_{D,cc}^\square
 \le C\theta^{1/4}
 A_c^{1/2}B_c.
\tag{4.7}
\]

对任一固定的 \(\square\)，空间包含关系
\(B_{2R}\subset B_{4R}\) 与匹配的时间包含关系
\(I_R^\square\subset I_{4R}^\square\) 给出

\[
 A_c+B_c\le4\mathcal E^\square(z_0,4R).
\tag{4.8}
\]

因此 core--core 行由
\(C\theta^{1/4}(\mathcal E^\square)^{3/2}\) 支付。把 (4.8) 与 (4.3) 结合，并使用初等不等式
\((a^{1/2}+b^{1/2})(c+d)\le
C(a+b+c+d)^{3/2}\)，即可证明 (4.4)。

#### 证明：core--exterior

利用 (3.4)--(3.5)，

\[
 \int_{B_R}G_c\sqrt{U_e}\,dx
 \le CR^{-3/2}U_\gamma(t)^{1/2}
 \int_{B_{2R}}|\nabla u(t)|^2\,dx.
\tag{4.9}
\]

被积函数不再依赖 \(s\)。先在长度为 \(\theta R^2\) 的尺度区间积分，再在物理时间上积分，得到

\[
 \mathcal K_{D,ce}^\square
 \le C\theta B_c
 (\mathcal U_{\rm ext}^{\infty,\square})^{1/2}.
\tag{4.10}
\]

#### 证明：exterior--core

由 (3.4) 和 \(|B_R|\simeq R^3\)，

\[
 \int_{B_R}G_e\sqrt{U_c}\,dx
 \le Cs^{-3/4}G_\gamma(t)
 \|u(t)\|_{L^2(B_{2R})}.
\tag{4.11}
\]

再用 (4.6) 以及 (4.1)、(2.5) 的定义，得到

\[
 \mathcal K_{D,ec}^\square
 \le C\theta^{1/4}A_c^{1/2}
 \mathcal D_{\rm ext}^{\square}.
\tag{4.12}
\]

#### 证明：exterior--exterior

(3.4) 中的两个估计给出

\[
 \int_{B_R}G_e\sqrt{U_e}\,dx
 \le CR^{-3/2}G_\gamma(t)U_\gamma(t)^{1/2}.
\tag{4.13}
\]

在 \(s\) 和 \(t\) 上积分后，

\[
 \mathcal K_{D,ee}^\square
 \le C\theta
 (\mathcal U_{\rm ext}^{\infty,\square})^{1/2}
 \mathcal D_{\rm ext}^{\square}.
\tag{4.14}
\]

把 (4.7)、(4.10)、(4.12) 与 (4.14) 相加，即得 (4.2)。\(\square\)

### 注 4.2：更尖锐的耦合尾项

(2.5) 中的分离配对便于记账，但并非唯一选择。证明实际产生的三个精确 Hölder 配对为

\[
 \begin{aligned}
 \mathcal T_{ce}
 &=\frac\nu R\int_I
 \left(\int_{B_{2R}}|\nabla u|^2\right)
 \left(\frac{U_\gamma(t)}R\right)^{1/2}dt,\\
 \mathcal T_{ec}
 &=\frac\nu R\int_I G_\gamma(t)
 \left(\frac1R\int_{B_{2R}}|u|^2\right)^{1/2}dt,\\
 \mathcal T_{ee}
 &=\frac\nu R\int_I G_\gamma(t)
 \left(\frac{U_\gamma(t)}R\right)^{1/2}dt.
 \end{aligned}
\tag{4.15}
\]

每个量都具有尺度不变性。如果后续论证能直接估计它们，就可得到更尖锐的 mixed-tail 表述。本笔记不主张 (2.5) 的分离尾项在所有可能的耦合 functional 中最优。

### 推论 4.3：与 pressure-cutoff 行的接口

进一步假设 \((u,p)\) 是
\(\mathbb T^3\times(0,T)\) 上的周期 suitable weak solution，
\(p\in L_{t,x}^{3/2}\)，且满足 R0.73X 的共同 pressure-tail 量词。令

\[
 Q_s=P_s(pu)-P_sp\,P_su,
\tag{4.16}
\]

令 \(s:I_R^\square\to(0,\theta R^2]\) 可测，并令
\(\eta_R\in W_0^{1,\infty}(B_R)\) 满足
\(\|\nabla\eta_R\|_\infty\le C_\eta/R\)。把定理 4.1 与 R0.73X 的 pressure-covariance 估计 (5.7) 及其局部能量付款 (6.2) 结合，得到

\[
 \boxed{
 \begin{aligned}
 &\mathcal K_D^\square(z_0,R;\theta)
 +\frac1R\int_{I_R^\square}\int_{B_R}
  |Q_{s(t)}\cdot\nabla\eta_R|\,dx\,dt\\
 &\quad\le C_{\mathbb T^3,\theta,\nu,C_\eta}
 \left\{
 \left[
 \mathcal E^\square(z_0,4R)
 +\mathcal U_{\rm ext}^{\infty,\square}(z_0,R;\theta)
 +\mathcal D_{\rm ext}^{\square}(z_0,R;\theta)
 \right]^{3/2}
 +\mathcal A_{\rm ext}^{\square}(z_0,R;\theta)
 \right\}.
 \end{aligned}}
\tag{4.17}
\]

新的 velocity endpoint tail 与复用的 gradient tail 支付
\(\mathcal K_D\)。旧的 \(\mathcal A_{\rm ext}\) 继续支付非局部 pressure 行与 harmonic 行。本文不主张这两个二次尾项能够单独控制一般的 \(Q_s\)。

---

## 5. 为什么旧 exterior functional 不足

R0.73X 的 functional 为

\[
 \mathcal A_{\rm ext}^\square
 =\mathcal G_{u,p}^\square+\mathcal H_u^\square,
\tag{5.1}
\]

其中 \(\mathcal G_{u,p}\) 包含下列量的 Gaussian 环带积分：

\[
 |u|^3+|p-c_R(t)|^{3/2},
\tag{5.2}
\]

而 \(\mathcal H_u\) 包含用于 harmonic pressure 的代数加权环带
\(|u|^2\) 矩。两项都不包含 \(|\nabla u|^2\)。此外，Gaussian
\(|u|^3\) 行在物理时间上积分，不能控制环带 \(L^2\) 能量的本质时间上确界。

下面两个例子只是函数层障碍。它们不是 Navier--Stokes 解，也不构造奇性。

### 例 5.1：外部高频包

选取球 \(B_*\Subset A_2(R)\)，其闭包与 \(B_{4R}\) 不交，并取
\(\phi\in C_c^\infty(B_*)\)、\(\phi\ne0\)。对整数 \(N\) 和振幅
\(\varepsilon_N>0\)，令

\[
 b_N(y)=\frac{\varepsilon_N}N\phi(y)\sin(Ny_1)e_3,
 \qquad w_N=\nabla\times b_N.
\tag{5.3}
\]

在固定坐标图中把该包视为周期场，并令其对应 Poisson pressure 为

\[
 p_N=\mathcal R_i\mathcal R_j(w_{N,i}w_{N,j}),
 \qquad -\Delta p_N=\partial_i\partial_j(w_{N,i}w_{N,j}).
\tag{5.3a}
\]

则 \(w_N\) 光滑、散度为零，并支撑于 \(B_*\)。当 \(N\) 充分大时，

\[
 \|w_N\|_{L^2}+\|w_N\|_{L^3}\simeq_\phi\varepsilon_N,
 \qquad
 \|\nabla w_N\|_{L^2}\simeq_\phi\varepsilon_NN,
 \qquad
 \|p_N\|_{L^{3/2}}\le C_\phi\varepsilon_N^2.
\tag{5.4}
\]

最后一个估计是周期 Calder\'on--Zygmund 估计。对固定区间上的时间无关包，

\[
 \mathcal E^\square(z_0,4R)=0,
 \qquad
 \mathcal A_{\rm ext}^\square\le C\varepsilon_N^3.
\tag{5.4a}
\]

固定 \(0<\alpha<\beta\le\theta\)。周期 heat kernel 在
\(s\in[\alpha R^2,\beta R^2]\) 上有正的最小值。由于周期 curl 及其梯度的空间均值为零，精确 variance 公式在该尺度带上对 \(x\in B_R\) 一致给出

\[
 k_s[w_N](x)\ge c\varepsilon_N^2,
 \qquad
 D_s[w_N](x)\ge c\varepsilon_N^2N^2.
\tag{5.4b}
\]

因此

\[
 \mathcal K_D^\square[w_N]\ge c\varepsilon_N^3N^2.
\tag{5.4c}
\]

取 \(\varepsilon_N=N^{-2/3}\)，得到

\[
 \mathcal K_D^\square[w_N]\ge c,
 \qquad
 \mathcal E^\square(z_0,4R)=0,
 \qquad
 \mathcal A_{\rm ext}^\square=O(N^{-2})\longrightarrow0.
\tag{5.4d}
\]

所以，对任意周期 energy-class velocity/Poisson-pressure 配对，旧付款
\((\mathcal E^\square)^{3/2}+\mathcal A_{\rm ext}^\square\)
不能控制 \(\mathcal K_D\)。这些静态包不是无强迫 Navier--Stokes 轨道，因此 (5.4d) 不是 suitable-weak NSE 反例。

### 例 5.2：外部时间集中

取非零、散度为零的
\(w\in C_c^\infty(B_*;\mathbb R^3)\)。选取时间区间
\(J_\delta\subset I\)，其长度为 \(\delta\)，并光滑逼近

\[
 w_\delta(t,y)=\delta^{-1/3}1_{J_\delta}(t)w(y).
\tag{5.5}
\]

则

\[
 \int_I\int|w_\delta|^3\,dy\,dt=\|w\|_3^3,
 \qquad
 \mathop{\rm ess\,sup}_{t\in I}\int|w_\delta|^2\,dy
 =\delta^{-2/3}\|w\|_2^2.
\tag{5.6}
\]

取对应 pressure
\(p_\delta=\mathcal R_i\mathcal R_j
(w_{\delta,i}w_{\delta,j})\)。由 Calder\'on--Zygmund 估计，完整的旧
\(\mathcal A_{\rm ext}\) 保持有界，而
\(\mathcal U_{\rm ext}^{\infty}\to\infty\)。这说明旧 Gaussian velocity tail 为什么不能提供 core--exterior 估计 (4.10) 所需的时间端点。

序列 (5.5) 没有一致的 \(L_t^\infty L_x^2\) 界，因此不与任一固定场的 energy-class 有限性矛盾。如果后续定理允许右端使用全局 Leray energy，那么该全局能量可以支付这个时间上确界；但所得估计将不再只由旧局部能量与
\(\mathcal A_{\rm ext}\) package 闭合。

---

## 6. 已证明条目与剩余门槛

### `PROVED`

1. 正的四块上界分解 (3.2) 在量纲与代数上均成立。
2. 四个分块分别满足 (4.7)、(4.10)、(4.12) 和 (4.14)，并带有所显示的
   \(\theta^{1/4}\) 或 \(\theta\) 因子。
3. 对两种匹配的时间钟，完整观测量都满足局部能量/尾项界 (4.4)。
4. pressure-cutoff 行通过继承的 R0.73X 付款与新估计衔接，得到 (4.17)。
5. 全 energy-field 包 (5.3)--(5.4d) 证明，在这个更大的类别中，旧右端
   \((\mathcal E^\square)^{3/2}
   +\mathcal A_{\rm ext}^\square\) 本身不能控制
   \(\mathcal K_D\)。
6. (4.2) 中的所有量在 Navier--Stokes 缩放下均保持不变。

### `FINITE`

对声明区间上的每个周期 energy-class velocity，
\(\mathcal U_{\rm ext}^{\infty,\square}\) 与
\(\mathcal D_{\rm ext}^{\square}\) 都有限。前者是本节新引入的 endpoint tail；后者是 R0.73X 已冻结的有利 gradient tail。这是 size 陈述，不是一致局部界。

### `OPEN`

1. 用一个更小柱上的数据控制新的 velocity endpoint tail 与复用的 gradient tail。
2. 在局部能量不等式中证明任一二次尾项的小性或可吸收性。
3. 用对预期 blow-up 序列稳定的 coupled tail 取代时间上确界，并得到更尖锐的论证。
4. Navier--Stokes 方程是否能提供任意 energy-class velocity/Poisson-pressure 配对所没有的更强闭合；静态包障碍不能决定这一点。
5. 局部观测量及所选外部付款的弱稳定性与下半连续性。
6. 把精确的一阶近核取商后，该上界是否与尺度一致的下界兼容。
7. 任何 epsilon-regularity 推论。

### `NOT CLAY`

本笔记没有证明三维 Navier--Stokes 解的紧致性、epsilon regularity、光滑性或全局正则性。
