# 平台内的能量历史：端点、耗散与负工作

2026-09-06。**本地解析计算 / 实际文件已独立复核 / G OPEN / NOT CLAY。**
接续 X 的时间范围归约和 W 的窗口局部化。固定原路径 X_R、
原速度提升 f(t,y)=u(t,y+X_R(t))、原空间常向量 a_R=dot X_R。
记 P=P_R^M、A=P^(2/3)、Z 为原匹配平方函数，不修改它们。
E_R 指合同 C.3 的完整移动核心能量，不是单壳 E_k。
本稿不宣称新颖性，也不把局部能量恒等式重排称为正则性证明。

## 1. 平台终点不等于平台窗口

记 t_p=t_0-R²，I_R=(t_p,t_0)。取 U 第三支的好终点 tau 属于 I_R，
原端点 E=E_k(tau)>0，令

\[
 G_k(d)=\int_{\tau-d}^{\tau}(F'_k(t))_+dt,\qquad
 \delta_k^F=\sup\{0\le d\le\tau-s_R:G_k(d)\le E/4\}.
\tag{Y.1}
\]

这里 F_k 是原 psi_k 的通量，正部在完整空间积分之后取。
U 已证 G_k 连续非降，原第三支中阈值确实在 tau-s_R 之前到达，
且 G_k(delta_k^F)=E/4。现在必须再区分：

- 若 G_k(tau-t_p)<E/4，原窗口跨过 t_p。平台部分没有达到阈值，
  不能把平台内推导代入 W.10 后仍声称控制了整个原窗口。
- 若 G_k(tau-t_p)>=E/4，可以另选平台内阈值窗，定义

\[
 \delta_k^P=\sup\{0\le d\le\tau-t_p:G_k(d)\le E/4\},\qquad
 J_k^P=(\tau-\delta_k^P,\tau).
\tag{Y.2}
\]

于是 0<delta_k^P<=delta_k^F，G_k(delta_k^P)=E/4，
且 J_k^P 包含于 I_R。连续性和 G_k(0)=0 证明正长度及精确阈值。
U 的端点能量下界适用于该较短窗口，W.9/W.10 的证明也只需要
精确阈值，故可在 J_k^P 重用。

若 G_k(tau-t_p)>E/4，原 delta_k^F 本身小于 tau-t_p。
但等号时，t_p 之前的零速率区间可能令原 delta_k^F 更长，
所以等号情形不能断言原窗口已在平台内。
改选较短窗口后，不能自动继承原 delta_k^F 的逆宽度预算：
(R²/delta_k^P)² 不小于 (R²/delta_k^F)²。
若要使用 R.217，必须对所选 J_k^P 重新证明其假设。

以下先对任意 J=(a,tau) 包含于 I_R 推导。a 可以等于 t_p；
跨平台支路仍保留为未解决的支路，而不是被 X 删除。

## 2. 覆盖 W 的质量所需的扩大测试

W.7 中 M_k 使用 Omega_k^(1/2)，原 psi_k 并不覆盖该域。
对 k>=1 构造新的紧支撑径向函数 xi_k，使

\[
 0\le\xi_k\le1,\quad
 \xi_k=1\ \hbox{于 }\Omega_k^{1/2},\quad
 \operatorname{supp}\xi_k\subset\Omega_k^{3/4},\qquad
 |\nabla\xi_k|\le C/R,\quad |D^2\xi_k|+|\Delta\xi_k|\le C/R^2.
\tag{Y.3}
\]

内外两侧过渡间隔是 R/4，可留出固定余量使支撑严格包含。
最内支撑半径至少 5R/4，径向 Laplacian 无原点问题。
全部壳从 k=1 开始；本稿不新增未定义的 gamma_0。
空间积分用单提升；环面测试时将 xi_k 周期化为 Xi_k。
紧支撑与周期场的 unfolding 精确相同，不把周期场当作全空间 L² 场。

沿用 P 的非负总耗散测度 boldmu>=|grad u|² dxdt，
包括黏性耗散和 suitable 缺陷。令

\[
\begin{split}
 \widehat E_k(t)&=\frac{\gamma_k\eta_R(t)}{2R}
                          \int_{\mathbb R^3}\xi_k|f(t)|^2,\\
 \widehat D_k(t)&=\frac{\gamma_k}{R}
   \int_{(s_R,t)\times\mathbb T^3}
             \eta_R(r)\Xi_k(x-X_R(r))\,d\boldsymbol\mu(r,x),\\
 \widehat Q'_k(t)&=\frac{\gamma_k}{2R}
           \int_{\mathbb R^3}(\eta_R'\xi_k+\eta_R\Delta\xi_k)|f|^2,\\
 \widehat F'_k(t)&=\frac{\gamma_k\eta_R}{R}
    \int_{\mathbb R^3}
    [\tfrac12|f|^2(f-a_R)+(\pi-c_{2R}^{M,R})f]\cdot\nabla\xi_k .
\end{split}
\tag{Y.4}
\]

Qhat、Fhat 在 s_R 取零初值；所有固定尺度时间被积函数均可积。
用原压力 gauge 可以直接对接 H 的账本。
任意可积时间常数的通量积分为零，并不消去非恒定压力功。
P 的同一移动测试给

\[
 \widehat K_k=\widehat Q_k+\widehat F_k,\quad
 \widehat K_k(s_R)=0,\quad
 \widehat K_k=\widehat E_k+\widehat D_k\ge0
       \quad\hbox{在好时间}.
\tag{Y.5}
\]

Khat 取右侧绝对连续代表，非负性延拓到全部时间。
eta 在 s_R 附近为零只消去完整截止测试的初始项，
不表示平台起点 a 的真实能量为零。

## 3. 反向历史的准确符号与弱端点

J=(a,tau) 包含于 I_R，tau 取好时间。定义

\[
\begin{split}
 \widehat d_k(J)&=\frac{\gamma_k}{R}
   \int_{J\times\mathbb T^3}\Xi_k(x-X_R(t))\,d\boldsymbol\mu(t,x),\\
 \widehat n_k(J)&=\int_J(\widehat F'_k(t))_-dt,\qquad
 (z)_-=\max\{-z,0\},\\
 H_k(J)&=\widehat E_k(\tau)+\widehat d_k(J)
                  +\operatorname{TV}_J\widehat Q_k+\widehat n_k(J).
\end{split}
\tag{Y.6}
\]

负部同样在完整空间积分之后取。这个 Fhat 用扩大 cutoff，
不是 U 原 F_k，不能在两者之间交换正负变差预算。
对几乎处处的好 t 属于 J，eta=1 给精确恒等式

\[
 \widehat E_k(t)
 =\widehat E_k(\tau)+\widehat d_k((t,\tau))
       -\int_t^\tau(\widehat Q'_k+\widehat F'_k)\,dr
 \le H_k(J).
\tag{Y.7}
\]

因此，正是 W.7 所需的质量满足

\[
 M_k^2=\operatorname*{ess\,sup}_{t\in J}
              \int_{\Omega_k^{1/2}}|f(t)|^2
       \le \frac{2R}{\gamma_k}H_k(J).
\tag{Y.8}
\]

Y.7 的耗散在右侧取正号：过去的能量可以在窗口内耗散掉。
删掉耗散或负工作都不再由该恒等式推出上界。
弱版本不能把 total boldmu 换成较小的黏性耗散。
仅有前向局部能量不等式也不能反向推得此式；这里使用
缺陷补全后的分布等式及其能量 BV 迹。

端点约定：好时间选在能量的强 L² Lebesgue 点及相关测度无时间原子处，
这是一个公共满测度集。Y.7 在这类 t,tau 成立，足以取 essential supremum。
J 的左端点 a 无须是好时间，也不把 a 处原子加进开窗口。
若 tau 是任意弱连续端点，正确右侧应保留加权能量左 BV 迹；
弱下半连续性只给物理端点能量不超过这个迹，方向不足以替换右侧。
此缺口也不在本稿中被识别为端点缺陷原子。
在原首次奇点合同下，tau<T_* 的解光滑，故这类内部端点自动合法；
不能据此把 tau=T_* 当成经典端点。

若 Y.7 用于 Y.2 的平台阈值窗，W.9 的压力/漂移余项分支原样保留。
在其另一支，记 w=|J|/R²，d_k^vis=(gamma_k/R)mathscr D_k(J)，
由 W.10 和 Y.8 得

\[
 d_k^{\rm vis}
 \ge c\,\gamma_k^{2/3}\frac{E_k(\tau)^{4/3}}{H_k(J)}w^{-1/3}
                    -2wH_k(J),\qquad H_k(J)>0 .
\tag{Y.9}
\]

这里 H>0 由阈值支路的非零局部三次质量推出。
gamma 的 2/3 次幂来自 weighted/unweighted 转换，不能删掉。
这仍是带负 cutoff 修正的下界，右侧可能非正；
它没有把 H_k 或余项工作的预算变成已知小量。

## 4. 能支付到什么程度

3R/4 加厚壳仍满足

\[
 \sum_{k\ge1}\gamma_k1_{\Omega_k^{3/4}}
       \le C1_{B_{8R}}+CW_{2R},\qquad
 \sum_{k\ge1}\gamma_k|\Omega_k^{3/4}|\le CR^3 .
\tag{Y.10}
\]

径向区间是 ((2^k-3/4)R,(2^(k+1)+3/4)R)。
非相邻 k 与 k+2 的间隔为 (2^(k+1)-3/2)R>0，所以同点至多重叠两次。
在 |y|>=8R 的 A_m(R)=A_(m-1)(2R) 中，相关壳只有 m-1,m,m+1，
每个权重不超过 gamma_(m-1)。核心单独支付。
体积结论使用 sum gamma_k 2^(3k)<infty，未假定每个大壳体积是 R³。
同尺度 W_R 的外扩权重比仍无统一上界，不能替换 W_(2R)。

Y.3/Y.10 允许重新运行 H/P 的绝对账本证明，得到

\[
 \sum_k\operatorname{TV}_{(s_R,t_0)}\widehat Q_k\le CA,\qquad
 \sum_k\operatorname{TV}_{(s_R,t_0)}\widehat F_k\le CP.
\tag{Y.11}
\]

这里不是按符号相似直接引用。具体是：

1. Qhat 的 eta' 和 Delta xi 行被
   C R^(-3)sum gamma_k int_(I_2R)int_(Omega^(3/4))|f|² 控制。
   Y.10 的加权体积与 Holder 将它变为加权三次量的 2/3 次幂。
   核心三次量由原 E_R^(3/2) 支付，外部由 G(2R) 支付。
2. Fhat 的速度和压力用原 c_(2R) gauge、Young 不等式及 Y.10。
   外部是原 G(2R)，核心按 H 的 local/harmonic pressure rows 支付，
   其中 H(2R) 保留，不能只用核心速度取代压力。
3. 漂移仍是 a_R 而不是完整 b_R(t,y)。Jensen 给
   |a_R|³<=C R^(-3)int_(B_R)|f|³；
   Young 和 sum gamma_k |Omega_k^(3/4)|<=CR³ 将其付回原三次量。

对任意一组平台窗口 J_k=(a_k,tau) 以及共同好终点 tau，
J_k 上 eta=1、total measure 非负，故
Ehat_k(tau)+dhat_k(J_k)<=Khat_k(tau)。由 Y.5/Y.11，

\[
 \sum_k H_k(J_k)
 \le 2\sum_k\operatorname{TV}\widehat Q_k
       +2\sum_k\operatorname{TV}\widehat F_k
 \le C(A+P).
\tag{Y.12}
\]

所选壳集是任意子集也成立。不同 J_k 的时间上确界不能仅凭空间重叠
并为一个时间上确界；Y.12 是先逐壳用完整修改时钟，再求和。
该上界来自动力学绝对账本，不是说原 P 的定义已经包含每个扩大端点。

因此不能说历史成本全无上界；准确结论是只恢复了粗的 A+P 控制。
扩大端点一般不能由原 E_k(tau) 支配，Khat 也不是原 K_k。
没有证明其负工作或平方函数由原 Z 控制，故 Y.12 不等于 A+Z。
同样，本稿只控制 eta 加权钟和平台窗口；没有把整个 I_2R 上
未加权的 W.14 宣布为已支付，尤其保留 eta=0 附近的时间差别。
若先假设 P<=1，则 P<=A，但产生该小性仍是原开放问题。

## 5. 这项检查改变了什么

本节记录三件事：X 可以减弱辅助终点量词；Y.1/Y.2 补上跨平台支路；
Y.7/Y.12 给出真实 NS 的准确历史上界和可达到的粗预算。
这是局部能量计算和路线边界，不是新正则性准则或真 NS 反例。

仅将 W 的 M_k 换成 Y.8，再对通量全部取绝对值，会返回原 A+P 层级，
不能单凭这套重排闭合 R.216/R.217 或合同 G。
我暂停继续优化这个局部代数闭环的常数；下一步需要新的动力学输入，
而不是更多同层级观测量。

后续先核验针对指定首次奇点的既有必要条件与持留结果，
明确区分无条件结论、Type-I 假设、临界范数假设和全空间/周期类别。
只有当候选输入能支付跨平台支路、负工作或跨尺度集中中的明确一项时，
才把它纳入原 G 的证明路线。一般初值、无外力和原路径定义保持不变。

本节无需仿真、DGX、科学图或新数值证书。不修改独立论文专项。
