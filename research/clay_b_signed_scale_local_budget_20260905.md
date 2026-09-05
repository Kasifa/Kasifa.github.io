# 有符号带能量的局部预算与逐尺度失配

2026-09-05，Clay-B 主桥梁第 3 回合。
状态：**PROVED LOCALLY（固定尺度恒等式）/ 实际文件独立复核通过 / NOT CLAY**。
前一轮已冻结并移交，不重新投递。此稿不改原 I 接口的平滑核。

## 0. 问题与计划

本轮检验：热滤波的有符号带能量相消，能否不产生未支付误差地
转为同一候选中心、逐尺度缩小的局部能量预算。
对象是三维周期、黏性 1、无外力 NS。先在光滑区间推导；
固定正尺度的弱解端点按上一节 E.1--E.2 处理。
不取未经证明的一致 R->0 极限，不使用仿真推断全称命题。

1. 已完成：核验 79880dbb 基线、原始带通预算和 F 预检。
2. 已完成：完整时空失配分解、非负对偶检验的定位障碍及真 NS 检验；
   两份实际源文件独立审查均通过。
3. 进行中：归并来源与审查，冻结小节；随后检验真实物理时间的
   反向平流扩散测试，不再试图以纯振幅重标制造原能量收缩。

update_plan 不可用；本节是持久化替代。原始来源限 Germano 1992
和 Eyink--Aluie 2009 的精确滤波预算，不泛搜未经核实的爆破解。

## 1. 两个非负量不等于通量有符号优势

在 T^3 上令 H_s=exp(s Delta)。固定 0<r<R，d=R^2-r^2。
所有空间积分为普通 Lebesgue 积分，<f,h>=int f h。
定义

\[
 b_\rho=H_{\rho^2}u,\quad p_\rho=H_{\rho^2}p,\quad
 \tau_\rho=H_{\rho^2}(u\otimes u)-b_\rho\otimes b_\rho,
 \quad e_\rho=\tfrac12|b_\rho|^2,\quad
 D_\rho=|\nabla b_\rho|^2.
\tag{S.1}
\]

采用标准 SGS 符号

\[
 \Pi_\rho=-\partial_jb_{\rho,i}\tau_{\rho,ij},\qquad
 J_\rho=(e_\rho+p_\rho)b_\rho+\tau_\rho^T b_\rho-\nabla e_\rho.
\tag{S.2}
\]

用 b_rho 点乘精确滤波方程，散度零与乘积公式给

\[
 \partial_t e_\rho+\nabla\cdot J_\rho=-D_\rho-\Pi_\rho.
\tag{S.3}
\]

例如应力贡献为
-b_i partial_j tau_ij=-partial_j(b_i tau_ij)+tau_ij partial_j b_i，
最后一项就是 -Pi。黏性贡献为 Delta e-D，已将 -grad e 放入 J。
这也固定了后续相减的符号，不能把 Pi 当作非负耗散。

因为 b_R=H_d b_r，定义

\[
 k_{r,R}=H_d e_r-e_R\ge0,\quad
 q_{r,R}=H_d D_r-D_R\ge0,\quad
 L_{r,R}=H_dJ_r-J_R .
\tag{S.4}
\]

两条正性分别是热核对 b_r 与 grad b_r 的 Jensen 不等式。
将 (S.3) 的 r 式作用 H_d，再减 R 式，得到完整恒等式

\[
 \partial_t k_{r,R}+\nabla\cdot L_{r,R}
 =\Pi_R-H_d\Pi_r-q_{r,R}.
\tag{S.5}
\]

右侧的有符号通量差不因为 k、q 非负而有固定符号。
该式是经典嵌套粗粒化预算的本地重推，不作为新发现：
[Eyink--Aluie 2009，第 II 节](https://arxiv.org/html/0909.2386v1)。

## 2. 完整时空截止：两端、时间导数和移动功都在

对非负光滑 chi(t,x)，在 [s,t] 上积分分部得到

\[
\begin{aligned}
 \langle\chi(t),k(t)\rangle+\int_s^t\langle\chi,q\rangle\,d\tau
 ={}&\langle\chi(s),k(s)\rangle\\
 &+\int_s^t\left[
 \langle\partial_\tau\chi,k\rangle+
 \langle\nabla\chi,L\rangle+
 \langle\chi,\Pi_R-H_d\Pi_r\rangle\right]d\tau .
\end{aligned}
\tag{S.6}
\]

若 chi=eta(t)psi_R(x-X(t))，则空间运输与移动截止合为

\[
 \langle\partial_t\chi,k\rangle+\langle\nabla\chi,L\rangle
 =\eta'\langle\psi_R,k\rangle+
   \eta\langle\nabla\psi_R,L-\dot X k\rangle.
\tag{S.7}
\]

只有 eta(s)=0 时初始加权能量消失，eta' 仍须支付。
L 含两个尺度的完整压力与应力运输，也含黏性空间运输。
可把黏性项进一步积分分部成 Delta chi，但不能删去它。
压力时间常数的 gauge 功为零，不代表完整压力功为零。

对于 Leray--Hopf 解，固定的正 r、R 经平滑 Leray 核给
b_rho in W^{1,infty}_t C^m_x。上节 E 的论证同样适用于热核：
其 Fourier 乘子 exp(-rho^2 |k|^2) 快速衰减。
故 (S.6) 在固定尺度的闭区间端点成立，不需要原始 u 的经典强迹。
所有关于 R->0 的统一性仍未证。

## 3. 不同尺度的检验函数到底留下什么

固定有限 N，R_n=theta^n R_0，d_n=R_n^2-R_{n+1}^2，
H_n=H_{d_n}，e_n=e_{R_n}，其余单尺度量同记。
令 k_n=H_ne_{n+1}-e_n，q_n=H_nD_{n+1}-D_n。
每一层取自己的光滑时空检验 chi_n。它可包括自己的 eta_n 和 X_n，
但所有恒等式在同一实际时间变量上写出。

定义内部失配与最细端点检验

\[
 A_m=H_{m-1}\chi_{m-1}-\chi_m\quad(1\le m<N),\qquad
 \bar\chi_N=H_{N-1}\chi_{N-1}.
\tag{S.8}
\]

这不是原始能量 A_2 的记号；A_m 只表示两个实际检验函数之差。
热算子自伴且与导数交换，逐层重排有限和即得

\[
 \sum_{n=0}^{N-1}\langle\chi_n,k_n\rangle
 =-\langle\chi_0,e_0\rangle+\langle\bar\chi_N,e_N\rangle
   +\sum_{m=1}^{N-1}\langle A_m,e_m\rangle,
\tag{S.9}
\]

\[
\begin{aligned}
 \sum_n\langle\chi_n,\Pi_n-H_n\Pi_{n+1}\rangle
 ={}&\langle\chi_0,\Pi_0\rangle-\langle\bar\chi_N,\Pi_N\rangle
 -\sum_{m=1}^{N-1}\langle A_m,\Pi_m\rangle,
\end{aligned}
\tag{S.10}
\]

\[
\begin{aligned}
 \sum_n\langle\nabla\chi_n,H_nJ_{n+1}-J_n\rangle
 ={}&-\langle\nabla\chi_0,J_0\rangle
   +\langle\nabla\bar\chi_N,J_N\rangle
   +\sum_{m=1}^{N-1}\langle\nabla A_m,J_m\rangle,
\end{aligned}
\tag{S.11}
\]

\[
 \sum_n\langle\partial_t\chi_n,k_n\rangle
 =-\langle\partial_t\chi_0,e_0\rangle+
   \langle\partial_t\bar\chi_N,e_N\rangle+
   \sum_{m=1}^{N-1}\langle\partial_t A_m,e_m\rangle,
\tag{S.12}
\]

\[
 \sum_n\langle\chi_n,q_n\rangle
 =-\langle\chi_0,D_0\rangle+\langle\bar\chi_N,D_N\rangle
   +\sum_{m=1}^{N-1}\langle A_m,D_m\rangle.
\tag{S.13}
\]

这些式子是有限和，不以可能不收敛的无穷级数为前提。
对 (S.9) 时间两端取差，将 (S.10)--(S.13) 代回 (S.6) 的层和。
内部第 m 项恰满足原单尺度方程以 A_m 为检验的恒等式：

\[
 [\langle A_m,e_m\rangle]_s^t
 +\int_s^t\langle A_m,D_m\rangle
 =\int_s^t
 \left[\langle\partial_t A_m,e_m\rangle+
       \langle\nabla A_m,J_m\rangle-
       \langle A_m,\Pi_m\rangle\right].
\tag{S.14}
\]

因此内部整包可以重写，不能只取消 Pi 项而保留有利端点，
同时免费丢掉时间、空间运输或耗散支付。A_m 可变号，
故 (S.14) 中 A_m D_m 不具有适当弱解测试所需的自动正性。
此处使用的是固定尺度等式，不是把变号测试塞进原始局部能量不等式。

## 4. 空间、中心、时间窗口和临界权重的四种失配

即使所有层取同一局部 chi，也有 A_m=(H_{m-1}-I)chi，
除非它恰被该热算子保持。若取各自几何尺度，
chi_m=eta_m psi((x-X_m)/R_m)，则还出现形状缩放、中心差和时间差。
热卷积与平移交换，但不会把中心 X_{m-1} 自动换成 X_m。

若时间窗口 J_m=(T-64R_m^2,T) 随尺度缩短，可以将每层 eta_m
在其窗口之外延为零，再在同一大时间区间相加；这样 (S.8)--(S.14)
仍正确，却保留 partial_t A_m。分别选不同好时间再拼接不合法。

真实目标还含 w_n=R_n^{-1} 等临界权重。此时应把所有 chi_n
替换成 w_n chi_n，内部失配实际变成

\[
 A_m^{(w)}
 =w_{m-1}H_{m-1}\chi_{m-1}-w_m\chi_m.
\tag{S.15}
\]

即使无权版本 A_m=0，加权版本也未必为零。
反过来强制 A_m^(w)=0，也只是对 w_m chi_m 施加同一热递推，
并不会自动得到符合原管道几何的检验函数。
下一份对偶检验分析具体说明这种无余项选择的定位代价。

## 5. 本轮保留与不保留的结论

保留：精确有符号预算；内部所有失配的来源和组合；固定尺度弱端点。
不保留：由望远镜符号直接推导 G-C，或忽略压力/截止的免费相消。
真实 NS 的局部乘积输运在 (S.3) 中明确使用，但没有由它获得
足以区分一般能量类爆破模型的正向临界预算。
此稿不声称能够排除 averaged NS 爆破或原始 NS 奇点。
