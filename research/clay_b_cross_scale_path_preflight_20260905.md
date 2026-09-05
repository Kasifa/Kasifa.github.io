# 指定中心桥梁：归一化与跨尺度路径预检

2026-09-05。状态：**局部解析证明 / 独立解析复核通过 / NOT CLAY**。
不声称这些初等变换或 Gronwall 估计具有新颖性。
主合同 G 仍 OPEN。本预检不以新观测量的小性替代 G。

## 1. 周期、黏性与常均值的精确变换

考虑周期长度 ell>0、黏性 nu>0 的无外力方程，令 k=2pi/ell，

\[
 y=kx,\quad s=\nu k^2t,\quad
 U(s,y)=\frac{u(t,x)}{\nu k},\quad
 P(s,y)=\frac{p(t,x)}{\nu^2 k^2}.
\tag{B.1}
\]

直接链式法则使时间项、输运项、黏性项和压力梯度全部提出
nu^2 k^3；所得 U 在 2pi 周期域上满足黏性 1 的原方程。
散度零、压力周期性、光滑性和无外力性均保留，逆变换显然存在。
将方程在周期域积分，散度项与 Laplacian 的积分为零，故空间均值
bar U 恒定。定义

\[
 W(s,y)=U(s,y+\bar U s)-\bar U,\qquad
 P_W(s,y)=P(s,y+\bar U s).
\tag{B.2}
\]

时间导数增加的 bar U·grad U 与输运中减去的同项抵消，
因此 W 是零均值的同一类无外力周期解，反变换恢复所有初值。
这是常速度 Galilean 变换，不是会引入加速度外力的 Version F 变换。

设物理尺度 R 对应 r=kR，物理 mollified path 为 X_R(t)。
由卷积换元 Y_r(s)=kX_R(t) 满足 dot Y_r=U_r(s,Y_r)。
对 (B.2)，令 Z_r(s)=Y_r(s)-bar U s，则
dot Z_r=W_r(s,Z_r)，终点也按 y_*->y_*-bar U s_* 变换。
沿路径有 W(s,Z_r+y)=U(s,Y_r+y)-bar U。
所以两种移动能量满足

\[
 E_r[U]\le2E_r[W]+C|\bar U|^2r^2,\qquad
 E_r[W]\le2E_r[U]+C|\bar U|^2r^2.
\tag{B.3}
\]

证明是 |a+b|^2<=2|a|^2+2|b|^2，加上 B_{8r} 体积是
O(r^3)，且空间梯度完全相同。能量本身不是 Galilean 不变量。
若在归一化的 W 类排除奇点，逆变换直接排除 U 的奇点；
不需要假称 (B.3) 中的 E 相等。

为核对物理量，设物理时间区间
J_R=(t_*-64R^2/nu,t_*)。归一化能量恰为

\[
 E_r[U]=\frac1{8\nu^2R}\mathop{\rm ess\,sup}_{J_R}
       \int_{B_{8R}}|u(t,X_R(t)+x)|^2dx
 +\frac1{8\nu R}\int_{J_R}\int_{B_{8R}}
       |\nabla_xu(t,X_R(t)+x)|^2dxdt.
\tag{B.4}
\]

由 dy=k^3dx、ds=nu k^2dt 和 grad_yU=grad_xu/(nu k^2)
逐项得到 (B.4)。原合同使用的确是 nu=1 归一化，而非遗漏黏性的公式。

## 2. 同一终点的两尺度路径：不使用 NS 的一般估计

以下在 2pi 周期域上。设 u 属于
L_t^infty L_x^2 intersect L_t^2 H_x^1。
固定 0<theta<1、0<R<pi/16，r=theta R，
J=(t_*-64r^2,t_*) 是定义域内的时间区间。
分别令 X_R、X_r 在 t_* 终点等于 x_*，均用相同核的卷积生成。
以同一终点选择欧氏提升。记

\[
 D_J=\int_J\|\nabla u(t)\|_{L^2(\mathbb T^3)}^2dt,\qquad
 b_R=(D_J/R)^{1/2}.
\tag{B.5}
\]

**引理。** 存在只依赖 phi、theta 的 C，使

\[
 \frac{\sup_{t\in\overline J}|X_r(t)-X_R(t)|}{R}
 \le C b_R e^{C b_R}.
\tag{B.6}
\]

**证明。** 卷积与弱梯度交换，Cauchy--Schwarz 给出

\[
 \|\nabla u_R(t)\|_\infty
 \le C_\varphi R^{-3/2}\|\nabla u(t)\|_2.
\tag{B.7}
\]

利用周期提升写 u_rho(x)=int phi(z)u(x-rho z)dz。
对 rho 微分，在光滑场上直接得到

\[
 \partial_\rho u_\rho(x)
 =-\int \varphi(z) z\cdot\nabla u(x-\rho z)\,dz.
\tag{B.8}
\]

支撑球不重叠地投影到 torus，故 Cauchy--Schwarz 和换元得到
||partial_rho u_rho||_infty<=C rho^{-3/2}||grad u||_2。
从 theta R 积分到 R，并用光滑逼近延拓到 H^1，得到

\[
 \|u_r(t)-u_R(t)\|_\infty
 \le C_\varphi(\theta^{-1/2}-1)R^{-1/2}\|\nabla u(t)\|_2.
\tag{B.9}
\]

注意这是差值估计，常均值恰好消失，不需要额外零均值假设。
置 d=X_r-X_R，由终点条件

\[
 |d(t)|\le\int_t^{t_*}
 \left(\|\nabla u_R(\tau)\|_\infty|d(\tau)|
       +\|u_r(\tau)-u_R(\tau)\|_\infty\right)d\tau.
\tag{B.10}
\]

Gronwall 和 |J|^{1/2}=8theta R 给出
int_J ||grad u_R||_infty<=C b_R，
int_J ||u_r-u_R||_infty<=C R b_R，遂得 (B.6)。
对固定正 R，能量类的 Caratheodory 路径存在唯一，所有积分有限；
不需要在 t_* 存在经典速度值。证毕。

这个引理没有用方程、压力、非线性消去或局部能量不等式。
因此它只是跨尺度几何的基线，不是新的真实 NS 正则机制。

若 C b_R exp(C b_R)<=8(1-theta)，则在共同时间区间上
B_{8r}(X_r(t)) subset B_{8R}(X_R(t))。
这只是有条件的几何包含；它甚至单独不提供小能量或严格收缩。

## 3. 能量有限性没有给出这里需要的速率

有限耗散给出 D_J->0，但 (B.6) 需要考察 D_J/R。
单凭非负可积函数的绝对连续性，不能推出这个比值趋零。
例如在 t_* 前取标量 g(t)=(t_*-t)^{-3/4}，在远离 t_* 处截断。
它可积，而

\[
 R^{-1}\int_{t_*-64\theta^2R^2}^{t_*}g(t)\,dt
 =4(64\theta^2)^{1/4}R^{-1/2}\longrightarrow\infty.
\tag{B.11}
\]

这只是对“可积性自动给出所需速率”这一推断的反例。
没有构造满足该 g 的 NS 解，也没有证明真实路径必然分离。
因此正确结论是：**现有能量输入没有闭合这条 Gronwall 推法**；
不是跨尺度嵌套不可能，更不是 NS 会爆破。

此外即使已知路径包含，单用非负积分区域包含至多给
E_r<=theta^{-1}E_R；系数大于 1，不是收缩。
需要来自方程的新的改善，不能仅重复几何包含。

## 4. 真实 NS 给出的精确应力项：下一个检查对象

在光滑解区间，令 b_R=u_R、p_R=varphi_R^{per}*p，并定义

\[
 \tau_R=(u\otimes u)_R-b_R\otimes b_R.
\tag{B.12}
\]

卷积原方程并用 div b_R=0 得到

\[
 \partial_tb_R+(b_R\cdot\nabla)b_R
 =\Delta b_R-\nabla p_R-\nabla\cdot\tau_R.
\tag{B.13}
\]

沿真实 mollified path 有精确恒等式

\[
 \ddot X_R(t)
 =(\Delta b_R-\nabla p_R-\nabla\cdot\tau_R)(t,X_R(t)).
\tag{B.14}
\]

只在光滑区间使用经典 (B.14)；不在 suitable 弱解的终点
直接求二阶路径导数。恒等式的各项可在 t<t_* 写出，
要积分到 t_* 必须另证相应可积性和极限。

phi>=0 给出协方差表示

\[
 \tau_R(t,x)=\int\varphi_R(y)
 [u(t,x-y)-b_R(t,x)]\otimes
 [u(t,x-y)-b_R(t,x)]\,dy.
\tag{B.15}
\]

因此 tau_R 是半正定矩阵。但 div tau_R 的某个分量或沿路径
的内积没有由此确定的符号；不能把 (B.14) 当作单调性公式。
压力由 -Delta p=partial_i partial_j(u_i u_j) 决定，仍非局部。

这是本轮指定的下一问题，而不是已成立的估计：
能否把 (B.13) 在两尺度同终点比较中的应力、压力与扩散共同
积分，得到比 (B.6) 强且能进入合同 G-C 的控制？
只对 tau 的矩阵正性取绝对值仍会丢失所需的符号。

将 NS 非线性改为抽象的 averaged operator 后，卷积右端不再
自动是这里的局部乘积协方差。未来正向论证必须说明
究竟使用 (B.12)--(B.15) 的哪项特殊结构。
但仅把这些精确恒等式写出，还没有排除 averaged 模型的障碍，
更没有证明它们足够强。

## 5. 本轮出口

- 周期、黏性、均值与路径的变换已逐项推导，消除了把零均值
  当作最终初值限制的量词歧义。
- 已有固定尺度稳定性没有被重做成新成果；两尺度基线明确揭示了
  缺失的 D_J/R 速率。
- 没有减少好尺度合同 G 的核心未证假设，没有扩大已经证明正则的
  解类，也没有新增足以迫使好尺度出现的跨尺度收缩。
- 下次研究检查原方程应力/压力的比较，或给出对该具体比较式的
  严格反例；不自动细化 (B.6) 的常数。

无数值模拟、无 DGX 作业、无期刊数值图。解析证明与独立复核
分开登记；文件哈希不替代本节证明。
