# 滞后热背景压力预算的尺度筛查

2026-09-06。**INTERNAL / PENDING REVIEW / LAG-SCALE SCREEN / G OPEN / NOT CLAY。**

本稿只检查 AQ 原坏时间净工作中的一个有限分解。保持同一 NS 解、
同一窗口、同一 \(s_J\)、同一坏集和同一积分因子不变，把高频速度的
Duhamel 起点放到窗口之前。先逐项复核一个不要求热背景小于一的粗
Young 预算，再利用旧压力的精确代数重组缩短所需滞后。

结论是充分性的：固定倍数的 \(K^{-2}\) 滞后已经能支付粗预算的五项
余项，不需要先证明热背景 \(L^\infty\) 小。进一步把混合压力写成
\(\Pi(b,h)\)，把纯热压力单独用 Fourier 绝对和估计，可取
\(\tau=\Lambda_A^{-8/3}\)。这不是最优性结论，也没有支付余下的
真实源—源压力。

## 1. 原窗口与窗口前的热起点

沿用 AQ 的固定参数和合法大范数序列。简记
\(\Lambda=\Lambda_A\)，并写

\[
 \begin{gathered}
 J=(t-\delta,t),\qquad
 \delta=c_0r^2\Lambda^{-4},\qquad
 K=\Lambda^{3/4},\qquad
 H_t=H_\chi(t)\ge\Lambda^3/3,\\
 A_J=\int_Jg(\sigma)^2\,d\sigma\longrightarrow0,\qquad
 g(\sigma)=\|\nabla u(\sigma)\|_2,\qquad
 M=\sup_{0<\sigma<T_*}\|u(\sigma)\|_2 .
 \end{gathered}
\tag{BB.1}
\]

AQ 实际选择的 \(s_J\in J\)、权重
\(\mu_J=w_J\mathbf1_{B_K}\) 及积分域 \([s_J,t]\) 全部保留，
特别是 \(0\le\mu_J\le1\)。取待定滞后 \(\tau=\tau_J>0\)，令

\[
 a=t-\delta-\tau,\qquad
 h=P_{>K}u,\qquad
 b(\sigma)=e^{(\sigma-a)\Delta}h(a)
 \quad(\sigma\in J).
\tag{BB.2}
\]

沿任意 \(\tau\to0\) 的合法序列，因 \(t\uparrow T_*>0\)，充分大时
\(a>0\)。而对 \(\sigma\in J\)，

\[
 \rho=\sigma-a\in(\tau,\tau+\delta).
\tag{BB.3}
\]

所以 BB.2 只使用严格前奇点的光滑解，却不要求 \(a\) 是早时低值点，
也不要求 \(g(a)\) 有统一上界。

固定实偶平滑高通在 \(L^2\) 上一致有界。逐模热衰减和
Fourier Cauchy--Schwarz 给

\[
 B_\tau:=\sup_{\sigma\in J}\|b(\sigma)\|_\infty
 \le C M\tau^{-3/4}e^{-cK^2\tau}.
\tag{BB.4}
\]

这里高通非零频率满足 \(|k|\gtrsim K\)；把热指数分成两半后，
一半产生 \(e^{-cK^2\tau}\)，另一半的格点平方和产生
\(\tau^{-3/4}\)。零模已由高通删除。

## 2. 只有能量时可用的三个时间积分

记 \(L_3(\sigma)=\|u(\sigma)\|_{L^3(\mathbb T^3)}\)，以及
\(I_q=\int_JL_3(\sigma)^q\,d\sigma\)。周期非齐次 Sobolev 和
\(L^2\)--\(L^6\) 插值给

\[
 L_3^2\le CM(M+g).
\tag{BB.5}
\]

因此 Hölder 只用 BB.1 就给出

\[
 \begin{aligned}
 I_3&\le C\left(
 M^{3/2}\delta^{1/4}A_J^{3/4}+M^3\delta\right),\\
 I_2&\le C\left(
 M\delta^{1/2}A_J^{1/2}+M^2\delta\right),\\
 I_1&\le C\left(
 M^{1/2}\delta^{3/4}A_J^{1/4}+M\delta\right).
 \end{aligned}
\tag{BB.6}
\]

最后一行也可直接由 \(I_1\le\delta^{1/2}I_2^{1/2}\) 得到。
BB.6 没有给 \(A_J\) 任何多项式衰减率。

## 3. \(K^{-2}\) 滞后的粗五项预算

先保留粗分解中 Young 不等式可能产生的全部五项：

若先粗写 \(R=h-b\) 和
\(p_{\rm old}=p(b)+\Pi(b,R)\)，则
\(\|R\|_3\le C(L_3+B_\tau)\) 以及双 Riesz 的 \(L^3\) 有界性给
\(\|p_{\rm old}\|_3\le CB_\tau(L_3+B_\tau)\)。
与 BB.16 相同的主链式项在 Young 后产生
\(B_\tau^2L_3^3+B_\tau^3L_3^2+B_\tau^4L_3\)，空间截止项产生
\(B_\tau L_3^3+B_\tau^2L_3^2\)。所以它们的完整时间余项为

\[
 {\cal R}_{\rm coarse}
 :=B_\tau^2I_3+B_\tau^3I_2+B_\tau^4I_1
   +B_\tau I_3+B_\tau^2I_2.
\tag{BB.7}
\]

取任意固定 \(c_*>0\) 并令

\[
 \tau=c_*K^{-2}=c_*\Lambda^{-3/2}.
\tag{BB.8}
\]

BB.4 此时只给

\[
 B_\tau\le C_{c_*}M K^{3/2}
 =C_{c_*}M\Lambda^{9/8};
\tag{BB.9}
\]

它通常不小于一。将 BB.6、\(\delta\simeq\Lambda^{-4}\) 和
\(H_t\gtrsim\Lambda^3\) 直接代入，而不先把 \(B_\tau\) 截成一，
五项分别满足

\[
 \begin{aligned}
 \frac{B_\tau^2I_3}{H_t}
 &\le C\left(
   \Lambda^{-7/4}A_J^{3/4}+\Lambda^{-19/4}\right),\\
 \frac{B_\tau^3I_2}{H_t}
 &\le C\left(
   \Lambda^{-13/8}A_J^{1/2}+\Lambda^{-29/8}\right),\\
 \frac{B_\tau^4I_1}{H_t}
 &\le C\left(
   \Lambda^{-3/2}A_J^{1/4}+\Lambda^{-5/2}\right),\\
 \frac{B_\tau I_3}{H_t}
 &\le C\left(
   \Lambda^{-23/8}A_J^{3/4}+\Lambda^{-47/8}\right),\\
 \frac{B_\tau^2I_2}{H_t}
 &\le C\left(
   \Lambda^{-11/4}A_J^{1/2}+\Lambda^{-19/4}\right).
 \end{aligned}
\tag{BB.10}
\]

这里及下文的常数可依赖固定的 \(M,r,c_0,\chi,c_*\)，不依赖窗口。
所以

\[
 \frac{{\cal R}_{\rm coarse}}{H_t}\longrightarrow0.
\tag{BB.11}
\]

粗路线本身已经说明：要求 \(B_\tau\le1\) 不是支付这些余项的必要
中间步骤。更一般地，BB.6 对任意
\(B_\tau=O(\Lambda^\beta)\) 的最紧一项是
\[
 \frac{B_\tau^4I_1}{H_t}
 \lesssim
 \Lambda^{4\beta-6}A_J^{1/4}
 +\Lambda^{4\beta-7}.
\tag{BB.12}
\]
因而 \(B_\tau=O(\Lambda^{3/2})=O(K^2)\) 是这组直接估计的一条
充分条件。若完全丢掉 BB.4 的指数，\(\tau\gtrsim
\Lambda^{-2}=K^{-8/3}\) 已能保证这一条件。该阈值只是粗五项法的
充分范围，不是必要尺度。

## 4. 旧压力的精确重组

令真实 Duhamel 源积分为

\[
 R(\sigma)=\int_a^\sigma e^{(\sigma-\rho)\Delta}
 {\cal N}_K(\rho)\,d\rho,\qquad h=b+R,
\tag{BB.13}
\]

其中 \({\cal N}_K\) 保留 Leray 投影、散度以及低低、低高和高高全部
相互作用。用
\[
 \Pi(v,w)=T_{ij}(v_iw_j+w_iv_j),\qquad
 p(v)=T_{ij}(v_iv_j)
\]
表示零均值压力。则

\[
 p(h)=p(R)+p_{\rm old},\qquad
 p_{\rm old}=p(b)+\Pi(b,R)=\Pi(b,h)-p(b).
\tag{BB.14}
\]

BB.14 是代数恒等式。它避免分别以 \(R=h-b\) 的三角估计制造
\(B_\tau^3I_2\) 和 \(B_\tau^4I_1\)，但没有删掉任何压力交互。

写 \(p_{bh}=\Pi(b,h)\)、\(p_{bb}=p(b)\)。双 Riesz 变换在
\(L^3\) 上有界，平滑高通在 \(L^3\) 上一致有界，因此

\[
 \|p_{bh}(\sigma)\|_3
 \le C\|b(\sigma)\|_\infty\|h(\sigma)\|_3
 \le C B_\tau L_3(\sigma).
\tag{BB.15}
\]

仍用原测试
\({\cal K}_\chi(p)=-\int\chi|u|u\cdot\nabla p\)。
分部积分及零点处的正则化极限给

\[
 \|\chi u\cdot\nabla|u|\|_{3/2}
 \le C L_3^{1/2}D_\chi^{1/2},\qquad
 \||u|u\cdot\nabla\chi\|_{3/2}
 \le C_\chi L_3^2.
\tag{BB.16}
\]

所以对任意固定 \(0<\varepsilon<3/4\)，

\[
 |{\cal K}_\chi(p_{bh})|
 \le \varepsilon D_\chi
 +C_{\varepsilon,\chi}B_\tau^2L_3^3
 +C_\chi B_\tau L_3^3.
\tag{BB.17}
\]

这一小份额耗散只能使用一次。

## 5. 纯热压力的 Fourier 梯度预算

对 \(\rho=\sigma-a\ge\tau\)，Fourier Cauchy--Schwarz 给

\[
 \sum_k|\widehat b(k,\sigma)|
 \le CM\rho^{-3/4},\qquad
 \sum_k|k|\,|\widehat b(k,\sigma)|
 \le CM\rho^{-5/4}.
\tag{BB.18}
\]

压力 Fourier 公式、\(|\kappa|\le|\xi|+|\eta|\) 及卷积绝对和于是给

\[
 \begin{aligned}
 \|\nabla p_{bb}(\sigma)\|_\infty
 &\le C\sum_{\kappa}|\kappa|
   \sum_{\xi+\eta=\kappa}
   |\widehat b(\xi,\sigma)|\,|\widehat b(\eta,\sigma)|\\
 &\le CM^2\rho^{-2}
 \le CM^2\tau^{-2}.
 \end{aligned}
\tag{BB.19}
\]

这里没有使用 Riesz 变换的 \(L^\infty\) 有界性；使用的是光滑热场
Fourier 系数的绝对可和性。由
\(\int\chi|u|^2\le M^2\)，直接在未分部积分的原测试上得到

\[
 |{\cal K}_\chi(p_{bb})(\sigma)|
 \le CM^4\tau^{-2}.
\tag{BB.20}
\]

## 6. 一条更短但仍充分的滞后尺度

暂写 \(\tau=\Lambda^{-\gamma}\)。丢掉 BB.4 中有利的高通指数，
有 \(B_\tau\le CM\Lambda^{3\gamma/4}\)。由
BB.6、BB.17 和 BB.20，在原来的 \([s_J,t]\) 与原来的
\(0\le\mu_J\le1\) 下，

\[
 \begin{aligned}
 \frac1{H_t}\int_{s_J}^t\mu_J
 \bigl(C_{\varepsilon,\chi}B_\tau^2L_3^3
       +C_\chi B_\tau L_3^3\bigr)\,d\sigma
 &\le C\bigl[
  \Lambda^{3\gamma/2-4}A_J^{3/4}
 +\Lambda^{3\gamma/2-7}\\
 &\hspace{3.9em}
 +\Lambda^{3\gamma/4-4}A_J^{3/4}
 +\Lambda^{3\gamma/4-7}\bigr],\\
 \frac1{H_t}\int_{s_J}^t\mu_J
 |{\cal K}_\chi(p_{bb})|\,d\sigma
 &\le C\Lambda^{2\gamma-7}.
 \end{aligned}
\tag{BB.21}
\]

取

\[
 \boxed{\qquad \tau=\Lambda^{-8/3}
       =K^{-32/9}.\qquad}
\tag{BB.22}
\]

此时 BB.21 的五个量依次至多为常数倍

\[
 A_J^{3/4},\qquad
 \Lambda^{-3},\qquad
 \Lambda^{-2}A_J^{3/4},\qquad
 \Lambda^{-5},\qquad
 \Lambda^{-5/3},
\tag{BB.23}
\]

故全部趋零。又因 \(\tau/\delta\simeq\Lambda^{4/3}\to\infty\)，
窗口确实位于热起点之后；且 \(\tau\to0\)，所以沿原前奇点序列最终
\(a>0\)。\(\gamma=8/3\) 是 BB.17--BB.21 在只知
\(A_J=o(1)\) 时仍能直接证明的端点充分选择，但本稿不声称它对其他
估计方法必要或最优。取 \((\log K)/K^2\) 会使 BB.4 更小，却比
BB.22 的真实时间滞后更长，因而本预算不需要该对数。

最后，由 BB.14、BB.17--BB.23，

\[
 \int_{s_J}^t\mu_J{\cal K}_\chi(p_{\rm old})
 \le\varepsilon\int_{s_J}^t\mu_JD_\chi+o(H_t).
\tag{BB.24}
\]

将它代入 AQ.8 时，只能推出如下条件必要性缩减：若原合法大范数序列
存在，则

\[
 \liminf\frac1{H_t}\int_{s_J}^t\mu_J
 \left[{\cal K}_\chi(p(R))
       -\left(\frac34-\varepsilon\right)D_\chi\right]d\sigma
 \ge1.
\tag{BB.25}
\]

不等号来自对 \(p_{\rm old}\) 的上界；BB.25 不是对源—源压力的
上界。\(R\) 是从 \(a=t-\delta-\tau\) 起由完整真实 NS 非线性生成的
高频源积分，不是任意小残差。负耗散的剩余份额也没有被再次使用。

## 7. 停止边界

BB.10 说明固定倍数 \(K^{-2}\) 已足以支付题设的粗五项预算；
BB.14 的精确重组与 BB.19 的纯热 Fourier 梯度界进一步把一条充分
滞后缩到 BB.22。两者都保持 AQ 原 \(s_J\)、原坏集、原权重与原
积分域，没有假设初始梯度、临界范数或 \(g^4\) 已付。

本稿没有估计 \({\cal K}_\chi(p(R))\)，没有证明 BB.25 左侧小，
没有构造实际大范数或奇点序列，也没有推进固定球到移动缩球合同 G。
它只缩小当前条件必要净工作的来源，不是正则性判据、成熟时间定理或
Clay 结论。没有仿真、DGX、科学图、提交或发布动作。
