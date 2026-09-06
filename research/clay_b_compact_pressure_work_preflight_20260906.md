# 正周期压力功的紧支撑化：全空间高频预检

2026-09-06。**PROVED LOCALLY / NOT CLAY。**
本稿由内部预检转入 PressureWorkWindow 合并研究包；
冻结提交与文件哈希以该包 manifest 为准。

本稿检查一个明确的瞬时问题：能否把 AD 中已经构造的零均值、
处处不消失的周期无散场 \(U\)，连同
\[
 W_{\mathbb T}(U)
 :=\int_{\mathbb T^3}p_U\,U\cdot\nabla|U|\,dy>0,
\qquad
 -\Delta p_U=\partial_i\partial_j(U_iU_j),\quad \int p_U=0,
\tag{AI.1}
\]
转成 \(\mathbb R^3\) 上的紧支撑无散场，并保留严格正的压力功。
AD 的 \(U\) 是有限 Fourier 模态且 \(\inf|U|>0\)，所以
\(p_U\) 与 \(U\cdot\nabla|U|\) 都是光滑周期函数。

## 1. 用周期向量势作无散 cutoff

因为 \(U\) 零均值且无散，存在零均值、光滑周期向量势
\({\mathcal A}\)，使
\[
 \operatorname{curl}_y{\mathcal A}=U.
\tag{AI.2}
\]
例如在每个非零 Fourier 模态上可取
\(\widehat{\mathcal A}(k)=i\,k\times\widehat U(k)/|k|^2\)。

固定非零的 \(a\in C_c^\infty(\mathbb R^3)\)，要求 \(a\ge0\)。
对正整数 \(N\) 定义
\[
 \begin{aligned}
 v_N(x)&=a(x)U(Nx),\\
 V_N(x)&=\operatorname{curl}_x
    \left(\frac{a(x){\mathcal A}(Nx)}N\right)
   =v_N(x)+r_N(x),\\
 r_N(x)&=\frac{\nabla a(x)\times{\mathcal A}(Nx)}N .
 \end{aligned}
\tag{AI.3}
\]
于是 \(V_N\) 光滑、紧支撑且精确无散；作为一个紧支撑旋度，
\(\int_{\mathbb R^3}V_N=0\)。辅助场 \(v_N=aU(Nx)\) 一般并不无散；
它只用于提取高频主项，真正作为速度场的是 \(V_N\)。并且
\[
 \|r_N\|_\infty+\|r_N\|_2\le\frac CN,\qquad
 \|\nabla r_N\|_\infty+\|\nabla r_N\|_2\le C,
\tag{AI.4}
\]
而
\[
 \|v_N\|_\infty+\|v_N\|_2\le C,\qquad
 \|\nabla v_N\|_\infty+\|\nabla v_N\|_2\le CN.
\tag{AI.5}
\]
所有场都支撑在一个与 \(N\) 无关的紧集内。

cutoff 的零点不会破坏下面的误差估计。定义
\[
 {\mathcal B}(z)=
 \begin{cases}
 z\otimes z/|z|,&z\ne0,\\
 0,&z=0.
 \end{cases}
\tag{AI.6}
\]
这个一次齐次映射在 \(\mathbb R^3\) 上全局 Lipschitz；例如
\[
 |{\mathcal B}(z)-{\mathcal B}(w)|\le3|z-w|.
\tag{AI.7}
\]
这可由单位球面上 \(n\mapsto n\otimes n\) 的 Lipschitz 性与径向分解
直接得到。对光滑向量场 \(z\)，在几乎处处意义下
\[
 z\cdot\nabla|z|={\mathcal B}_{ij}(z)\,\partial_i z_j.
\tag{AI.8}
\]
令 \(h(z)=z\cdot\nabla|z|\)。由 AI.4--AI.8，
\[
 \|h(V_N)-h(v_N)\|_2\le C,\qquad
 \|h(V_N)\|_2\le CN.
\tag{AI.9}
\]
因此这里没有把 \(a=0\) 邻域中的方向 \(z/|z|\) 作非法展开。

## 2. 调制后的全空间压力

令
\[
 {\mathcal T}_{ij}=\partial_i\partial_j(-\Delta)^{-1}
\]
是 \(\mathbb R^3\) 上的二阶 Riesz 乘子，其符号为
\[
 m_{ij}(\xi)=-\frac{\xi_i\xi_j}{|\xi|^2}\quad(\xi\ne0).
\tag{AI.10}
\]
先把 \(p_N^{\,0}:={\mathcal T}_{ij}(v_{N,i}v_{N,j})\) 定义为
\(v_N\) 的辅助二次张量变换。由于 \(v_N\) 一般不无散，
\(p_N^{\,0}\) 不称为 NS 解的压力；它只用来与真正无散场 \(V_N\)
的压力作 \(L^2\) 比较。

需要的调制估计是：对固定 \(k\in\mathbb Z^3\setminus\{0\}\) 和
\(b\in C_c^\infty(\mathbb R^3)\)，
\[
 \left\|
 {\mathcal T}_{ij}(b\,e^{iNk\cdot x})
 -m_{ij}(k)b\,e^{iNk\cdot x}
 \right\|_2
 \le\frac{C_{b,k}}N.
\tag{AI.11}
\]
由 Plancherel，左侧平方是
\[
 \int_{\mathbb R^3}
 |m_{ij}(Nk+\xi)-m_{ij}(k)|^2|\widehat b(\xi)|^2\,d\xi.
\]
在 \(|\xi|\le N|k|/2\) 上，\(m_{ij}\) 的零次齐次性和球面光滑性给
\[
 |m_{ij}(Nk+\xi)-m_{ij}(k)|
 \le C_k\frac{|\xi|}{N}.
\]
在补集上不能沿用这个差分界，但乘子一致有界，而
\(\widehat b\) 是 Schwartz 函数；其尾部为任意负次幂。
两部分合并即得 AI.11。特别地，接近总频率零点的区域已经包含在
Schwartz 尾部中，没有越过乘子在 \(\xi=0\) 的奇性。

记
\[
 C_{ij}=\fint_{\mathbb T^3}U_iU_j,\qquad b=a^2.
\]
因 \(U_iU_j\) 只有有限多个 Fourier 模态，逐模应用 AI.11 得
\[
 \boxed{
 p_N^{\,0}
 =a^2p_U(Nx)+p_{\rm low}+s_N,\qquad
 p_{\rm low}={\mathcal T}_{ij}(C_{ij}a^2),\qquad
 \|s_N\|_2\le\frac CN.}
\tag{AI.12}
\]
此外 \(\|p_N^{\,0}\|_2+\|p_{\rm low}\|_2\le C\)，并且
\(\nabla p_{\rm low}\in L^2\)，因为二阶 Riesz 乘子在
\(H^1(\mathbb R^3)\) 上有界。

令 \(P_N={\mathcal T}_{ij}(V_{N,i}V_{N,j})\) 为 \(V_N\) 的
Euclidean 衰减压力。由 AI.4 及 Calderón--Zygmund 的 \(L^2\) 有界性，
\[
 \|P_N-p_N^{\,0}\|_2
 \le C\|V_N\otimes V_N-v_N\otimes v_N\|_2
 \le\frac CN.
\tag{AI.13}
\]

## 3. 正主项与全部 \(O(1)\) 误差

因为 \(a\ge0\) 且 \(U\) 处处不消失，
\[
 |v_N|=a|U(Nx)|.
\]
写
\[
 h_U=U\cdot\nabla_y|U|,\qquad G_U=|U|U.
\]
则
\[
 h(v_N)
 =Na^2h_U(Nx)+\ell_N,\qquad
 \ell_N=a|U(Nx)|\,U(Nx)\cdot\nabla a,
\tag{AI.14}
\]
其中 \(\|\ell_N\|_2+\|\ell_N\|_\infty\le C\)。
无散性还给
\[
 h_U=\operatorname{div}_yG_U,\qquad
 \fint_{\mathbb T^3}h_U=0.
\tag{AI.15}
\]

令 \(f=p_Uh_U\)。由 AI.1，
\[
 \bar f:=\fint_{\mathbb T^3}f
 =\frac{W_{\mathbb T}(U)}{(2\pi)^3}>0.
\tag{AI.16}
\]
对光滑零均值周期函数 \(f-\bar f\)，取光滑周期向量场
\({\mathcal Z}\) 使
\(\operatorname{div}_y{\mathcal Z}=f-\bar f\)。分部积分给
\[
 \begin{aligned}
 N\int_{\mathbb R^3}a^4f(Nx)\,dx
 &=N\bar f\int_{\mathbb R^3}a^4\,dx
   -\int_{\mathbb R^3}\nabla(a^4)\cdot{\mathcal Z}(Nx)\,dx\\
 &=N\bar f\int a^4+O(1).
 \end{aligned}
\tag{AI.17}
\]

AI.12 与 AI.14 的高频乘积正是 AI.17。低频压力与高频 \(h_U\)
也只有 \(O(1)\)：由 AI.15，
\[
 \int p_{\rm low}\,Na^2h_U(Nx)
 =-\int\nabla(p_{\rm low}a^2)\cdot G_U(Nx)=O(1).
\tag{AI.18}
\]
这里 \(\nabla(p_{\rm low}a^2)\in L^1\)，因为 \(a\) 紧支撑且
\(p_{\rm low},\nabla p_{\rm low}\in L^2\)。
含 \(\ell_N\) 的项由 \(L^2\) 直接控制；含 \(s_N\) 与高频主项的积
由 \(\|s_N\|_2=O(N^{-1})\) 和
\(\|Na^2h_U(Nx)\|_2=O(N)\) 控制。因此
\[
 \int p_N^{\,0}h(v_N)
 =N\bar f\int a^4+O(1).
\tag{AI.19}
\]

最后，由 AI.9、AI.12--AI.13，
\[
 \begin{aligned}
 \left|\int P_Nh(V_N)-\int p_N^{\,0}h(v_N)\right|
 &\le\|P_N-p_N^{\,0}\|_2\|h(V_N)\|_2\\
 &\quad+\|p_N^{\,0}\|_2\|h(V_N)-h(v_N)\|_2
 =O(1).
 \end{aligned}
\tag{AI.20}
\]
所以
\[
 \boxed{
 W_{\mathbb R^3}(V_N)
 :=\int_{\mathbb R^3}P_N\,V_N\cdot\nabla|V_N|
 =N\bar f\int a^4+O(1)>0}
\tag{AI.21}
\]
对所有充分大的 \(N\) 成立。这给出了光滑、紧支撑、零均值、无散的
Euclidean 正压力功场。

## 4. 固定能量单泡产生真实初始净增长

固定一个使 AI.21 成立的 \(N\)，把 \(V_N\) 乘以一个正常数，使
\[
 \|V_N\|_{L^2(\mathbb R^3)}^2=E_0
\tag{AI.22}
\]
而不改变压力功的正号。以下把这个固定场记为 \(V\)，其 Euclidean
压力记为 \(P\)，并令
\[
 \begin{aligned}
 H_V&=\frac13\int|V|^3>0,\\
 D_V&=\int\left(|V||\nabla V|^2
                  +|V||\nabla|V||^2\right)<\infty,\\
 G_V&=\|\nabla V\|_2^2>0,\qquad
 W_V=\int P\,V\cdot\nabla|V|>0.
 \end{aligned}
\tag{AI.23}
\]

把 \(V\) 作为一只单泡嵌入周期环面。对充分小的 \(\epsilon>0\)，置
\[
 u_\epsilon(x)=\epsilon^{-3/2}
 \sum_{k\in\mathbb Z^3}
 V\left(\frac{\widetilde x-\widetilde x_0+2\pi k}{\epsilon}\right).
\tag{AI.24}
\]
它是光滑、周期、零均值、无散场，且
\[
 \begin{aligned}
 \|u_\epsilon\|_2^2&=E_0,&
 H(u_\epsilon)&=\epsilon^{-3/2}H_V,\\
 \|\nabla u_\epsilon\|_2^2&=\epsilon^{-2}G_V,&
 D(u_\epsilon)&=\epsilon^{-7/2}D_V.
 \end{aligned}
\tag{AI.25}
\]

周期 Green 函数的分布 Hessian 在原点附近等于 Euclidean
Newtonian 分布 Hessian 加一个光滑张量。因而在泡内
\[
 p_\epsilon(x_0+\epsilon y)
 =\epsilon^{-3}P(y)+\rho_\epsilon(y),\qquad
 \|\rho_\epsilon\|_{L^\infty(\operatorname{supp}V)}\le C.
\tag{AI.26}
\]
对角 delta 项包含在 Euclidean 分布 Hessian 中；没有从压力核中删去。
同时
\[
 u_\epsilon\cdot\nabla|u_\epsilon|
 =\epsilon^{-4}V\cdot\nabla|V|
\]
在缩放坐标中成立。于是
\[
 W_{\mathbb T}(u_\epsilon)
 =\epsilon^{-4}W_V+O(\epsilon^{-1}).
\tag{AI.27}
\]

每个 \(u_\epsilon\) 都可作为黏性 1、无外力周期 NS 的光滑初值。
在 \(t=0\) 的全环面 \(L^3\) 恒等式
\[
 H_\epsilon'(0)+D(u_\epsilon)=W_{\mathbb T}(u_\epsilon)
\]
可由标准 \(q_\delta=(|u|^2+\delta^2)^{1/2}\) 正则化取得，即使
\(u_\epsilon\) 在泡外为零也没有零集问题。由 AI.25--AI.27，
\[
 H_\epsilon'(0)
 =\epsilon^{-4}W_V-\epsilon^{-7/2}D_V+O(\epsilon^{-1})>0
\tag{AI.28}
\]
对充分小的 \(\epsilon\) 成立，并且
\[
 \boxed{
 \frac{(H_\epsilon'(0))_+/H(u_\epsilon)}
      {1+\|\nabla u_\epsilon\|_2^2}
 \ge c(V)\epsilon^{-1/2}\longrightarrow\infty.}
\tag{AI.29}
\]

因此不存在只依赖固定 \(E_0\) 的常数 \(C(E_0)\)，使所有光滑周期
零均值无散初值都满足
\[
 (H'(0))_+
 \le C(E_0)H(0)\bigl(1+\|\nabla u(0)\|_2^2\bigr).
\tag{AI.30}
\]
这是对真实初始净生产 \(W-D\) 的反例，不借用 AH 中
\(F=0\) 的常速平台残差。

## 5. 结论边界

1. AI.21 是从已证周期正压力功场到 Euclidean 紧支撑场的局部解析转换；
   核心是有限模态压力的全空间高频调制与 curl cutoff。
2. AI.29--AI.30 只排除包含初始时刻、没有额外支付的瞬时统一估计。
   固定能量不等于固定 \(H^1\)：这里
   \(\|\nabla u_\epsilon\|_2\to\infty\)，标准局部理论给出的保证寿命
   没有统一正下界。
3. 本稿不否定正成熟时间、同一固定解、首次奇点附近或带更强尺度成本的
   signed-work 估计，也没有给出反向持留、压力几何闭合或原合同 G。
4. 这里没有新仿真或科学图。有限原始文献碰撞记录见
   research/clay_b_pressure_work_literature-boundary_20260906.md；
   不作新颖性声明，也不把局部证明当作外部同行审稿。

## 6. 内部逐式审查记录

历史审查日期：2026-09-06。审查覆盖本稿 AI.1--AI.30 的实际文件，不只核对
聊天中的公式。审查前科学正文 SHA-256 为
87559df82622f3c2e1a77dcc3c4cffaed3c245fbc9e7f4e86e0651dde6a8bed5；
本节记录加入后文件哈希会改变，原哈希不声称覆盖本节自身。

- 推导：r076l_proof_audit。
- 独立实际文件复核：r076l_heat_chebyshev，PASS，无必改项。
- 根任务完整读取并复核 AI.1--AI.30；同意其限定的瞬时结论。
- 重点检查了辅助场非无散的边界、零速 cutoff 的 Lipschitz 控制、
  乘子零频邻域的 Schwartz 尾部、低频压力项的 \(W^{1,1}\) 支付、
  周期平均因子、Green Hessian 的 delta 项，以及五个缩放指数。
- 这次审查不包括新颖性判定、真实轨道上的统一时间窗或成熟时间。
  后续 AJ 单独完成统一早时窗审查；整包冻结和单次移交另作记录。

该历史检查点的下一项是把严格正的真实净增长延伸到明确短时间窗，
现由 research/clay_b_short_time_pressure_work_preflight_20260906.md 接续。
在固定单泡下，重标度时间为 \(\tau=\epsilon^{-5/2}t\)，
有效黏性为 \(\epsilon^{1/2}\)，空间环面边长为 \(2\pi/\epsilon\)。
必须证明局部存在常数、压力功连续性和所有范数常数对扩大环面统一，
不能从每个初值各自的连续性直接推断统一时间窗。
即使得到 \(t\asymp\epsilon^{5/2}\)，它也早于扩散尺度
\(\epsilon^2\)，不属于正成熟时间或首次奇点合同 G。
