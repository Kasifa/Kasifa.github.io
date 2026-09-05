# 两尺度能量：完整恒等式与扩散吸收检验

2026-09-05，主桥梁第 2 个研究回合。
基线 bbe05cfc584b550d52b5f2c899dfc5e32491114d。
状态：**PROVED LOCALLY（所列有限范围）/ 独立解析复核通过 / 主合同 G 仍 OPEN / NOT CLAY**。

## 0. 本轮问题、计划与出口

上一回合已有可核验文件和提交，属于实际进展，不是等待或空转。
本轮只检查一个明确候选步骤：真实 NS 的两尺度差能量是否自动
耗散，或其非线性生产能否被没有额外尺度支付的二次扩散能量统一吸收。
这是原合同 G-C 的一种可能中间推法，不是 G-C 的全部实现方式。

1. 已完成：核验前一检查点、研究与发布分工和待检验量词。
2. 已完成：逐项推导、真实 NS 检验族和候选公式的独立复算。
3. 已完成：实际文件终审、文献边界、保留完整支付的固定尺度
   移动截止估计及其独立复核；精确有理 Fourier 回归核对。
4. 进行中：科学冻结与一次性交接，然后进入有符号跨尺度预算预检。

论文整合已由用户直接授权的管理任务接手。我不再修改论文仓库，
也不把 Clay 主线的 OPEN 作为论文整合的前置条件。

没有 update_plan 工具；实际调用不可用，以上是持久化替代。
不启动 DGX 扫描。反例只用于否定明确的吸收形式，不能解释为爆破。

## 1. 同一原方程上的两尺度差

在 T^3=(-pi,pi]^3 上，(u,p) 是黏性 1、无外力的光滑 NS 解。
固定前一合同的偶径向、非负、质量 1、支撑于 B_1 的核 phi，
并固定 0<theta<1、r=theta R。记

\[
 S_\rho f=\varphi_\rho^{\rm per}*f,\qquad
 b_\rho=S_\rho u,\quad p_\rho=S_\rho p,\quad
 \tau_\rho=S_\rho(u\otimes u)-b_\rho\otimes b_\rho,
\tag{D.1}
\]

\[
 g=b_r-b_R,\quad \delta\tau=\tau_r-\tau_R,\quad
 \delta p=p_r-p_R,\quad M=S_r-S_R.
\tag{D.2}
\]

约定 (div T)_i=partial_j T_ij。两个 b 都散度为零，因此 g 也散度为零。
两份精确卷积方程相减，使用
(b_r·grad)b_r-(b_R·grad)b_R=(b_R·grad)g+(g·grad)b_r，
得到

\[
 (\partial_t-\Delta+b_R\cdot\nabla)g
 =-(g\cdot\nabla)b_r-\nabla\cdot\delta\tau-\nabla\delta p.
\tag{D.3}
\]

这是同一 u 的比较，不是分别选择两份有利的解。
这里 g 是空间场差，不是路径差 X_r-X_R。控制 g 的某个体积分
并不自动提供它沿路径的迹估计。

## 2. 移动截止下不漏项的局部能量

以 coarse path X_R 为参考，a_R=dot X_R。取非负光滑周期 chi_0，
非负光滑时间函数 eta，并令

\[
 \chi(t,x)=\eta(t)\chi_0(x-X_R(t)).
\tag{D.4}
\]

用 <f>=(2pi)^{-3}int_T3 f 表示归一化积分。将 (D.3) 点乘 chi g，
逐项分部积分，得到

\[
\begin{aligned}
 \frac12\frac d{dt}\langle\chi|g|^2\rangle
 +\langle\chi|\nabla g|^2\rangle
 ={}&\frac12\langle|g|^2(\partial_t\chi+\Delta\chi+
                      b_R\cdot\nabla\chi)\rangle\\
 &-\langle\chi g_i g_j\partial_j b_{r,i}\rangle
 +\langle\delta\tau_{ij}\partial_j(\chi g_i)\rangle
 +\langle\delta p\,g\cdot\nabla\chi\rangle .
\end{aligned}
\tag{D.5}
\]

因为 div g=div b_R=0，压力只有边界功，输运项只在截止函数上留下
导数。黏性项给出左侧正耗散与右侧 (1/2)Delta chi 的二次项。
应力项的符号来自 -div delta tau 的分部积分，不可反转。
利用 (D.4)，第一行的系数恰为

\[
 \partial_t\chi+\Delta\chi+b_R\cdot\nabla\chi
 =\eta'\chi_0(\,\cdot-X_R)
   +\eta\Delta\chi_0(\,\cdot-X_R)
   +(b_R-a_R)\cdot\nabla\chi .
\tag{D.6}
\]

因此拉伸、应力差、压力边界、残余漂移、空间截止和时间截止都在。
在光滑区间 [s,t] 积分得到完整的差能量平衡；若 eta(s)=0，只有
左端初始加权能量消失，右侧的 eta' 支付仍保留。
本节首先在光滑区间推导。固定正尺度的弱解闭时间端点延拓另由
clay_b_two_scale_paid_budget_20260905.md 第 1 节证明；
它不提供平滑尺度趋零时的统一时间迹控制。

若取 chi=1，压力项、漂移和全部截止项恰为零。此时定义

\[
 \mathcal N_{r,R}(u)
 :=-\langle g_i g_j\partial_j b_{r,i}\rangle
   +\langle\delta\tau_{ij}\partial_jg_i\rangle .
\tag{D.7}
\]

偶核使 M 自伴，并与空间导数交换，故还有等价的直接表达

\[
 \frac12\frac d{dt}\|g\|_2^2+\|\nabla g\|_2^2
 =\mathcal N_{r,R}(u)
 =-\langle M^2u,(u\cdot\nabla)u\rangle .
\tag{D.8}
\]

这里所有范数使用上述归一化积分。证明另一表达：直接将原 NS
方程作用 M，点乘 Mu；压力因 div(Mu)=0 消失，最后移动一个 M。
式 (D.7) 与 (D.8) 的一致性也核对了两尺度分解的组合符号。

## 3. 真实 NS 的全时光滑检验族

取任意 A>0，初值

\[
 u_A(0,x)=A(-\cos x_2,\ 0,\ \sin x_1+\cos(x_1+x_2)).
\tag{D.9}
\]

定义

\[
 U_A(t,x_2)=-Ae^{-t}\cos x_2,\qquad
 u_A=(U_A,0,W_A(t,x_1,x_2)),\quad p_A=0,
\tag{D.10}
\]

其中 W_A 是周期线性问题

\[
 \partial_t W_A-\Delta_{x_1,x_2}W_A+
 U_A(t,x_2)\partial_1W_A=0,\qquad
 W_A(0)=A(\sin x_1+\cos(x_1+x_2))
\tag{D.11}
\]

的解。该场散度为零。第一分量满足热方程；第三分量恰是 (D.11)，
第二分量恒零，所有 x_3 导数为零，故 (D.10) 是原始无外力 NS 解。
没有将线性模型冒充为未验证的 NS 近似。

该解全时光滑。可用 Fourier--Galerkin 构造 (D.11)，其 L^2
能量恒等式给统一界。对任意整数 m>=1 求导并积分，最高输运项
由 partial_1 U_A=0 消去。其余 commutator 至多含 m 阶 W_A
导数，且 U_A 的所有空间导数由 A exp(-t) 控制。因此

\[
 \frac d{dt}\|W_A(t)\|_{H^m}^2+
 2\|\nabla W_A(t)\|_{H^m}^2
 \le C_m A e^{-t}\|W_A(t)\|_{H^m}^2.
\tag{D.12}
\]

Gronwall、各阶 Galerkin 紧性及线性差能量唯一性给全时 H^m 解；
任意 m 的界和方程给空间、时间光滑性及初值处连续性。
也可由最大值原理得 ||W_A(t)||_infty<=2A。
这只是全时光滑的特殊不变类，不扩大一般三维正则性解类。

初值均值零，并且精确地

\[
 \|u_A(0)\|_2^2=\tfrac32 A^2,\qquad
 \|\nabla u_A(0)\|_2^2=2A^2,\qquad
 \|u_A(0)\|_{H^1}^2=\tfrac72 A^2.
\tag{D.13}
\]

当 A 变化，初值范数也变化。因此以下反例不否定允许常数依赖
初值的估计，更不是同一个解出现奇点。

## 4. 精确三角积分与核的小尺度展开

因核径向偶对称，其 Fourier 乘子为实函数

\[
 f(s)=\int_{\mathbb R^3}\varphi(z)\cos(sz_1)\,dz,\qquad
 d_1=f(\theta R)-f(R),\quad
 d_2=f(\sqrt2\theta R)-f(\sqrt2R).
\tag{D.14}
\]

式 (D.9) 的前两个有效波数长度为 1，第三个为 sqrt(2)。故

\[
 g(0)=A(-d_1\cos x_2,\ 0,\
              d_1\sin x_1+d_2\cos(x_1+x_2)).
\tag{D.15}
\]

由正交性直接得到

\[
 \|g(0)\|_2^2=A^2(d_1^2+\tfrac12d_2^2),\qquad
 \|\nabla g(0)\|_2^2=A^2(d_1^2+d_2^2).
\tag{D.16}
\]

非线性只有第三分量：

\[
 ((u_A(0)\cdot\nabla)u_A(0))_3
 =-A^2\cos x_2\cos x_1
   +A^2\cos x_2\sin(x_1+x_2).
\tag{D.17}
\]

其 sin x_1 投影系数为 A^2/2，cos(x_1+x_2) 投影系数为 -A^2/2；
另外的波数与 M^2u 的支撑正交。因每个三角函数的均方为 1/2，

\[
 \mathcal N_{r,R}(u_A(0))
 =\frac{A^3}{4}(d_2^2-d_1^2).
\tag{D.18}
\]

令 sigma_2=int phi(z)z_1^2 dz>0。Taylor 公式及核紧支撑给
f(s)=1-(sigma_2/2)s^2+O_phi(s^4)。对固定 theta，
c_theta=sigma_2(1-theta^2)/2>0，因此

\[
 d_1=c_\theta R^2+O(R^4),\quad
 d_2=2c_\theta R^2+O(R^4),\quad
 d_2^2-d_1^2=3c_\theta^2R^4+O(R^6).
\tag{D.19}
\]

对所有足够小的 R，生产严格为正。并且

\[
 \frac{\mathcal N_{r,R}(u_A(0))}{\|\nabla g(0)\|_2^2}
 \longrightarrow\frac{3A}{20},\qquad
 \frac{\mathcal N_{r,R}(u_A(0))}
      {\|\nabla g(0)\|_2^2+\|g(0)\|_2^2}
 \longrightarrow\frac{3A}{32}.
\tag{D.20}
\]

这些系数是解析三角正交计算，不是拟合出的渐近。
scripts/clay_b_two_scale_fourier_check.py 从 Fourier 卷积另行核对
有限系数，使用精确有理复数，不依赖浮点或第三方符号库。
其证书不代替第 3、5 节的 PDE 存在性及正时间极限证明。

## 5. 避免初始时刻与合法尺度的量词漏洞

反例可以置于正时间，并且令 64R^2<t，不只停在 t=0 的切片。
对固定的光滑函数 h，Fourier 乘子和 Taylor 公式给

\[
 R^{-2}Mh\longrightarrow c_\theta(-\Delta)h
 \quad\hbox{在每个固定 }H^s\hbox{ 中，若 }h\in H^{s+2}.
\tag{D.21}
\]

这里 |f(theta R|k|)-f(R|k|)|<=C R^2|k|^2；
逐频收敛及平方可和的该上界证明 (D.21)。
对光滑 u(t)，由 (D.8) 的自伴形式
N=-<Mu,M((u·grad)u)>，得到

\[
 R^{-4}\mathcal N_{r,R}(u(t))
 \to-c_\theta^2\langle-\Delta u(t),
                          -\Delta((u(t)\cdot\nabla)u(t))\rangle,
\tag{D.22}
\]

并且

\[
 R^{-4}(\|\nabla g(t)\|_2^2+\|g(t)\|_2^2)
 \to c_\theta^2(\|\nabla\Delta u(t)\|_2^2+\|\Delta u(t)\|_2^2).
\tag{D.23}
\]

对每个固定 A，(D.22)--(D.23) 的比值在 t=0 附近连续，分母非零，
且初始值为 3A/32。给定任意 C>=0，先选 A 使 3A/32>C。
再选足够小但固定的 t_A>0，使该极限比值仍严格大于 C；
最后选 R 足够小，同时满足 R<pi/16 和 64R^2<t_A，
使实际比值也大于 C。theta 一直固定。

因此对任意固定 theta，不存在独立于解、时间和合法尺度的有限
常数 C，使所有光滑真实 NS 解都满足

\[
 \mathcal N_{\theta R,R}(u(t))
 \le C(\|\nabla(u_{\theta R}-u_R)(t)\|_2^2
        +\|(u_{\theta R}-u_R)(t)\|_2^2).
\tag{D.24-false}
\]

特别是“两个应力都是协方差，所以组合生产必为非正”及无需额外
支付的统一扩散吸收都不成立。这里压力已经恒为零，不能把符号
问题只归给遗漏的压力边界项。

## 6. 不能从这个反例推出什么

这不是对 G-C 的否定。尤其没有否定：

- 带 R^{-2}||g||_2^2 等实际截止支付的估计；
- 允许常数依赖初值或已经证出的轨道预算的估计；
- 有限时间累计后的抵消、初始支付、持留时间打包；
- 全部外壳与完整 Version-M 能量的收缩；
- 依赖真正三维涡量方向结构的另一个桥梁。

式 (D.24-false) 只排除明确的无额外支付、统一瞬时吸收。
不能用 A 大的不同光滑解拼成一个爆破解。
一个精确 NS 子类足以反驳“对所有真实 NS 解”的这个不等式，
但不能反驳附加了它不满足的时钟/支付条件的命题。

## 7. 文献边界与记号

滤波应力及其跨层恒等式有成熟文献，不作为本稿的新发现。
[Germano 1992，式 (24)、(33)](https://www.ams.jhu.edu/~eyink/Turbulence/classics/Germano92.pdf)
对保常数、与导数交换的滤波 F、G 给出

\[
 \tau_{GF}(a,b)=G\tau_F(a,b)+\tau_G(Fa,Fb).
\tag{D.25}
\]

这涉及复合滤波 GF。当前一般紧支撑核不保证 S_R=G S_r，
且 g tensor g 不等于 tau_G(S_r u,S_r u)。本稿的差场能量不能
直接称为 Germano 的带能量。

[Eyink--Aluie 2009，第 II 节式 (2)--(8)](https://arxiv.org/html/0909.2386v1)
给出标准粗粒化通量 Pi_rho=-grad b_rho:tau_rho。其大尺度能量
方程中源项为 -Pi_rho，而本稿的 N 是 (D.7) 的两个项之和。
单独的 -g tensor g:grad b_R 与剪切生产同型，但它既不是
Pi_R，也不是 Pi_R-Pi_r；不能把它的符号称为完整净回传。

这些来源不提供任意 NS 解在指定候选中心的好尺度定理。
本稿的贡献范围只是为当前候选估计提供逐项可复算的检验记录；
没有完成查新，也不主张该特殊族或能量供给现象的优先权。

## 8. 对下一步的影响

不能把应力协方差正性升级为差能量单调性；这种瞬时吸收应从
候选证明中删除。剩下的是有代价的局部/时间比较：
下一次从 (D.5)--(D.6) 连同完整 cutoff 支付出发，检查其时间
积分能否与 R 的端点提取、持留时间打包结合，而非再次假定小 P。

当前仍没有减少主合同 G 的核心未证假设，也没有排除真实 NS 奇点。
本轮改变的是一条具体候选推法的判断，不以版本数或断言数衡量进展。
有完整截止支付的后续估计另存于
clay_b_two_scale_paid_budget_20260905.md；它不将本稿的负面结论
扩大到尚未检验的带 R^{-2} 支付不等式。无 DNS、无 DGX、无图表。
