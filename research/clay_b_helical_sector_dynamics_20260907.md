# 完整 NS 的螺旋扇区：一个显式非不变性核验

2026-09-07（Asia/Shanghai）。内部接口核验，非科学发布冻结。
PROVED LOCAL CALCULATION / LITERATURE / CONDITIONAL / OPEN / NOT CLAY。

历史记录已指出：螺旋度只能控制两个临界正量之差，单扇区占优需要另证。本页不把这条已知路线重新列为候选。我补齐一个具体动态检查：纯正 curl 谱初值是否必然留在正谱子空间？下面的完整 NS 局部解给出否定答案。该事实属于经典 helical 相互作用，不主张新颖性。

## 1. 方程与投影

固定 \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\)、\(\nu>0\)，考虑实、零均值、光滑无散初值的无外力 NS。使用标准局部光滑适定性；本文不重证该定理。以下等式先在同一解的光滑存在区间内使用。零均值可由保守均值的 Galilean 变换归一化，不把最终研究目标限制为小数据或特殊对称类。

写 \(u(x)=\sum_k a_k e^{ik\cdot x}\)、\(a_{-k}=\overline{a_k}\)，\(D=\sqrt{-\Delta}\)。对 \(k\ne0\)，定义
\[
 P_k=I-\frac{k\otimes k}{|k|^2},\qquad
 P_\pm(k)=\frac12\left(P_k\pm\frac{i k\times}{|k|}\right),
 \qquad u_\pm=P_\pm u,\qquad
 \operatorname{curl}u_\pm=\pm Du_\pm .
 \tag{HS.1}
\]
在横向平面上，\(i k\times/|k|\) 自伴、平方为恒等算子，故 \(P_\pm\) 是正交投影，且所有 \(D^s u_\pm\) 正交。取零频投影为零。投影满足实场的共轭对称性。

令 \(\omega=\operatorname{curl}u\)。由 \((u\cdot\nabla)u=\nabla(|u|^2/2)-u\times\omega\)，完整方程为
\[
 \partial_tu+\nu D^2u=\mathbb P(u\times\omega),\qquad
 \partial_tu_\pm+\nu D^2u_\pm=P_\pm(u\times\omega).
 \tag{HS.2}
\]
这里没有从完整非线性中删去任何 helical 相互作用。

## 2. 临界恒等式及其未付条件

所有 \(L^2\) 范数使用未归一化体积测度。定义累计量
\[
 C_\pm(t)=\frac12\|D^{1/2}u_\pm(t)\|_2^2
       +\nu\int_0^t\|D^{3/2}u_\pm(s)\|_2^2\,ds,\qquad
 C_+(t)-C_-(t)=\frac12 H(0)=:h,
 \quad H(t)=\int u\cdot\omega\,dx .
 \tag{HS.3}
\]
证明：分别用 \(Du_\pm\) 测试 HS.2。两式的非线性项之差是
\(\langle Du_+-Du_-,u\times\omega\rangle
=\langle\omega,u\times\omega\rangle=0\)；积分即得 HS.3。等价地，
\(H=\|D^{1/2}u_+\|_2^2-\|D^{1/2}u_-\|_2^2\)，
\(H'=-2\nu(\|D^{3/2}u_+\|_2^2-\|D^{3/2}u_-\|_2^2)\)。
这是已知 helicity 结构的周期归一化重算。

尤其，\(C_\pm'(t)=\langle Du_\pm,u\times\omega\rangle\) 相等；两者本身非负，但这个共同导数没有由恒等式得到符号。不能把累计量名称误解为各自单调。

若额外假定 \(h>0\)，且整个 \([0,T)\) 上有统一的 \(0\le\theta<1\) 使 \(C_-\le\theta C_+\)，则
\[
 C_++C_-\le S:=\frac{h(1+\theta)}{1-\theta},\qquad
 \int_0^T\|u(t)\|_6^4\,dt
 \le C\sup_{t<T}\|D^{1/2}u(t)\|_2^2
             \int_0^T\|D^{3/2}u(t)\|_2^2\,dt
 \le \frac{2CS^2}{\nu}.
 \tag{HS.4}
\]
这里只用了固定零均值环面的 Sobolev 嵌入和
\(\|Du\|_2^2\le\|D^{1/2}u\|_2\|D^{3/2}u\|_2\)。
再用 \(H^1\) 能量估计
\(\frac12\frac d{dt}\|\nabla u\|_2^2+\frac\nu2\|\Delta u\|_2^2
\le C\nu^{-3}\|u\|_6^4\|\nabla u\|_2^2\)，
Grönwall 给出有限 \(T\) 上的 \(H^1\) 控制；标准局部适定性的延拓结论仍作为已知输入。

但 \(C_-/C_+=1-h/C_+\)。所以对 \(h>0\)，存在上述统一 \(\theta<1\) 当且仅当 \(C_+\) 在该时段一致有界。条件不是由“正螺旋度”免费得到的估计；所需的临界累计控制仍在假设中。

## 3. 纯正初值

取两个不同长度的波矢及系数
\[
 p=(1,0,0),\quad q=(0,2,0),\quad
 a_p=(0,1,i),\quad a_q=(i,0,1),\quad
 a_{-p}=\overline{a_p},\quad a_{-q}=\overline{a_q}.
 \tag{HS.5}
\]
其余系数为零。由 \(p\cdot a_p=q\cdot a_q=0\)、
\(i p\times a_p=a_p\)、\(i q\times a_q=2a_q\)，四个模全在正扇区。因此 \(u_{0,-}=0\)。实空间表达式为
\(u_0=(-2\sin(2x_2),\,2\cos x_1,\,-2\sin x_1+2\cos(2x_2))\)。

这个初值是二维空间依赖、三个速度分量的特殊场，处在完整三维 NS 的允许初值类内。它不是三方向空间依赖的流，更不是候选奇点。论证只需其标准局部光滑解。

## 4. 完整非线性立即产生负扇区

令 \(k=p+q=(1,2,0)\)，初始 \(a_k=0\)。在该频率，卷积只有两个有序贡献：
\[
 [u_0\times\omega_0]_k
 =a_p\times(2a_q)+a_q\times a_p=(1,-1,-i),\qquad
 w=P_k(1,-1,-i)=(6/5,-3/5,-i),\qquad
 i k\times w=(2,-1,-3i).
 \tag{HS.6}
\]
于是负扇区的初始时间导数为
\[
 F_k^-:=\partial_t a_k^-(0)
 =\frac12\left[(6/5,-3/5,-i)-\frac{(2,-1,-3i)}{\sqrt5}\right],
 \qquad |F_k^-|^2=\frac75-\frac3{\sqrt5}>0.
 \tag{HS.7}
\]
正性可由 \(7\sqrt5>15\) 直接确认。模方也可核算为
\(\frac12(|w|^2-w^*(i k\times w)/\sqrt5)
=\frac12(14/5-6/\sqrt5)\)。
因为初始 \(a_k=0\)，黏性项在这个时间导数中为零；压力已由 \(P_k\) 完整处理，不存在遗漏的压力抵消。

对每个固定 \(\nu>0\)，局部光滑适定性和 HS.2 给出
\[
 a_k^-(t)=tF_k^-+o(t)\quad(t\downarrow0),\qquad
 \exists\,\varepsilon>0\ \ \forall\,0<t<\varepsilon:\quad u_-(t)\ne0 .
 \tag{HS.8}
\]
这里是同一个完整 NS 解的导数，不是 Galerkin 截断轨道或仅满足能量不等式的任意曲线；也没有假设有限 Fourier 支持在正时间持续。\(\varepsilon\) 可以依赖此初值和 \(\nu\)。

## 5. 结论的范围

HS.5–8 否定的是“所有纯正 curl 谱初值在完整 NS 下都留在正谱子空间”。它不证明每个纯正初值都会泄漏：单一 curl 特征值的 Beltrami 场有 \(u\times\omega=0\)，热演化保留该结构。它也不否定一段时间内较弱的扇区占优，更没有证明任何扇区累计量无界、奇点形成或单扇区初值的全局正则性失败。

单手性删减方程把整个动态限制为 \(P_+\) 投影后的方程，负扇区不变性由定义强制。Biferale–Titi 对该周期模型的正定临界估计与全局结果不能不经新证明便用于完整 NS 的纯正初值。HS.7 明确显示两个向量场在哪里不同。

本轮没有新增从基本能量到 HS.4 假设的估计；不接纳“初始纯正符号加 helicity 差恒等式”作为一般正则性的闭合路线。G、R216–R217、一般终端能量缺口消失与一般三维光滑延拓仍 OPEN。

## 6. 来源和去重边界

[Lei–Lin–Zhou，Structure of Helicity and Global Solutions of Incompressible Navier-Stokes Equation，1505.00142v1](https://arxiv.org/html/1505.00142v1) 提供完整 NS 中条件强制的临界 helicity 结构，并证明特定大数据类的全局结果。本文不推广其特定数据定理。

[Biferale–Titi，On the Global Regularity of a Helical-decimated Version of the 3D Navier-Stokes Equations，1303.1215v1](https://arxiv.org/html/1303.1215v1) 明确对演化本身作螺旋投影；本文对照的是其式 (7) 的删减方程，不是一般完整 NS。

项目已有 R072I 的上述来源与扇区条件边界、R071X 的 projected Lamb/Sobolev 平衡、R070J 的投影和单模 Beltrami 校准，以及 R070X 的三循环抵消。因此 HS.1–4 不计新机制。此次局部去重未找到 HS.5–8 的这一显式动态算例；局部未命中不证明数学新颖性。实际阅读和独立检查范围另见审查记录。
