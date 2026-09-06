# 压力角度绝对成本：固定能量的双频块反检查

2026-09-06。**INTERNAL / PENDING REVIEW / STATIC OBSTRUCTION / G OPEN / NOT CLAY。**

本稿检查 exact-pressure-geometry 路线中的一个瞬时问题：无散条件留下的
方向因子，能否仅由统一的 \(L^2\) 能量和 \(H^1\) 耗散控制其逐项取绝对值
后的总成本。下面给出一族有限 Fourier 场，答案是否定的。这个结论只针对
压力一侧的静态绝对值预算；它没有估计最终测试因子，也不是压力功、
Navier--Stokes 演化、成熟窗口或奇点反例。

## 1. 单对模态的精确角度因子

空间为 \(\mathbb T^3=(-\pi,\pi]^3\)，积分不作体积归一化，并记
\(V_{\mathbb T}=(2\pi)^3\)。采用 Fourier 约定

\[
 \widehat f(n)=\frac1{V_{\mathbb T}}
     \int_{\mathbb T^3}f(x)e^{-in\cdot x}\,dx.
\]

若 \(h\) 是实值、零均值、无散周期场，零均值压力由
\(-\Delta p_h=\partial_i\partial_j(h_i h_j)\) 定义，则

\[
 \widehat p_h(m)
 =-\sum_{k+\ell=m}
   \frac{(m\cdot\widehat h(k))(m\cdot\widehat h(\ell))}{|m|^2},
 \quad m\ne0,\qquad
 \widehat p_h(0)=0,\qquad
 \widehat h(-k)=\overline{\widehat h(k)}.
\tag{AX.1}
\]

取非零输入 \(k,\ell\)，令 \(m=k+\ell\ne0\)，并令 \(\theta\) 是
\(k\) 与 \(\ell\) 的夹角。对单位无散极化 \(a\perp k\)、\(b\perp\ell\)，
单对收缩的最大方向因子为

\[
 \begin{aligned}
 \Gamma(k,\ell)
 &:=\sup_{\substack{|a|=|b|=1\\a\perp k,\ b\perp\ell}}
   \frac{|(m\cdot a)(m\cdot b)|}{|m|^2}\\
 &=\frac{|P_{k^\perp}m|\,|P_{\ell^\perp}m|}{|m|^2}
 =\frac{|k|\,|\ell|\sin^2\theta}{|k+\ell|^2}
 \le1.
 \end{aligned}
\tag{AX.2}
\]

这里最后一个上界也可直接由正交投影不增范数得到。当
\(|k|=|\ell|\) 且 \(\theta<\pi\) 时，

\[
 \Gamma(k,\ell)=\frac{\sin^2\theta}{2(1+\cos\theta)}
 =\sin^2\frac\theta2\longrightarrow1
 \qquad(\theta\uparrow\pi).
\tag{AX.3}
\]

所以近反平行的低输出不会自动带来角度小量：压力分母同时变小。
另一方面，若 \(k,\ell\) 精确共线且 \(m\ne0\)，则任何合法极化都满足

\[
 m\cdot a=m\cdot b=0,\qquad \Gamma(k,\ell)=0.
\tag{AX.4}
\]

若等长反平行使 \(m=0\)，该项属于被压力 gauge 删除的零模。因而
“共线压力为零”和“近反平行系数可饱和”是两个不同的陈述。

## 2. 两个横向频率块

令 \(q\in\mathbb Z_{\ge1}\)、\(Q=100q\)；这里的 \(q\) 只是正整数
频率块宽度。
定义两个整数频率块

\[
 \begin{aligned}
 A_Q&=\{k\in\mathbb Z^3:Q\le k_1<Q+q,\ 0\le k_2,k_3<q\},\\
 B_Q&=\{\ell\in\mathbb Z^3:0\le\ell_1,\ell_3<q,\\
     &\hspace{38mm}Q\le\ell_2<Q+q\},\\
 N&:=|A_Q|=|B_Q|=q^3=10^{-6}Q^3.
 \end{aligned}
\tag{AX.5}
\]

两块互不相交。对 \(k\in A_Q\)、\(\ell\in B_Q\)，取实单位极化

\[
 a_k=\frac{P_{k^\perp}e_2}{|P_{k^\perp}e_2|},
 \qquad
 b_\ell=\frac{P_{\ell^\perp}e_1}{|P_{\ell^\perp}e_1|}.
\tag{AX.6}
\]

分母不会为零，因为 \(k_1\ne0\)、\(\ell_2\ne0\)。而且
\(Q\le|k|,|\ell|<1.011Q\)。若 \(m=k+\ell\)，则

\[
 \begin{aligned}
 m\cdot a_k
 &=\ell\cdot a_k
 \ge \ell_2-\frac{k_2|k\cdot\ell|}{|k|^2}>0.989Q,\\
 m\cdot b_\ell
 &=k\cdot b_\ell
 \ge k_1-\frac{\ell_1|k\cdot\ell|}{|\ell|^2}>0.989Q,\\
 |m|&\le|k|+|\ell|<2.022Q.
 \end{aligned}
\tag{AX.7}
\]

在前两行中，投影向量归一化所除的范数至多一，且未归一化的右端已经
为正；数值界来自 \(k_2,\ell_1<0.01Q\) 和
\(|k\cdot\ell|\le(1.011Q)^2\)。因此每个横向配对都满足同号下界

\[
 d(k,\ell):=
 \frac{(m\cdot a_k)(m\cdot b_\ell)}{|m|^2}
 >\frac{0.989^2}{2.022^2}>\frac15.
\tag{AX.8}
\]

记受保护的正频率输出区

\[
 R_Q=A_Q+B_Q
 \subset\{m:Q\le m_1,m_2<Q+2q,\ 0\le m_3<2q\}.
\tag{AX.9}
\]

坐标范围表明：在
\(\pm A_Q\cup\pm B_Q\) 的任意两频率之和中，落入 \(R_Q\) 的只有
正频率的 \(A_Q+B_Q\) 与交换次序。确实，\(A_Q+A_Q\) 的第一坐标
至少为 \(2Q\)，\(B_Q+B_Q\) 的第二坐标至少为 \(2Q\)；同块差频至少
有一个前两坐标绝对值小于 \(q\)，而异块差频的一个前两坐标为负。
这也把实值场必需的全部负共轭频率纳入了检查。

## 3. 统一 \(H^1\) 下实际压力绝对成本发散

令

\[
 S_Q=\sum_{n\in A_Q\cup B_Q}|n|^2,\qquad
 c_Q=S_Q^{-1/2},\qquad
 v_Q(x)=c_Q\left(
  \sum_{k\in A_Q}a_k\cos(k\cdot x)
 +\sum_{\ell\in B_Q}b_\ell\cos(\ell\cdot x)\right).
\tag{AX.10}
\]

这是实值、光滑、零均值、无散的有限 Fourier 场。不同余弦频率正交，
且

\[
 2NQ^2\le S_Q<2N(1.011Q)^2,\qquad
 \frac1{2N(1.011Q)^2}<c_Q^2\le\frac1{2NQ^2}.
\tag{AX.11}
\]

由 \(\int_{\mathbb T^3}\cos^2(n\cdot x)\,dx=V_{\mathbb T}/2\)，精确有

\[
 \|v_Q\|_2^2=V_{\mathbb T}Nc_Q^2
 \le\frac{V_{\mathbb T}}{2Q^2},
 \qquad
 \|\nabla v_Q\|_2^2
 =\frac{V_{\mathbb T}}2c_Q^2S_Q
 =\frac{V_{\mathbb T}}2.
\tag{AX.12}
\]

对 \(m\in R_Q\)，AX.9 的保护性质与余弦的 \(1/2\) Fourier 系数给出

\[
 \widehat p_{v_Q}(m)
 =-\frac{c_Q^2}{2}
   \sum_{\substack{k\in A_Q,\ \ell\in B_Q\\k+\ell=m}}
   \frac{(m\cdot a_k)(m\cdot b_\ell)}{|m|^2}<0.
\tag{AX.13}
\]

系数 \(c_Q^2/2\) 已同时计入有序配对 \((k,\ell)\) 与
\((\ell,k)\)。即使不同配对产生相同输出，AX.8 保证它们在该输出上
同号，因而没有 pair-to-output 抵消。具体地，方向加权逐对绝对成本
在这个例子上等于实际压力系数的绝对和，并满足

\[
 \begin{aligned}
 \mathfrak A_{R_Q}(v_Q)
 &:=\sum_{m\in R_Q}\sum_{\substack{r+s=m\\
                    r,s\in\operatorname{supp}\widehat v_Q}}
   \frac{|(m\cdot\widehat v_Q(r))
           (m\cdot\widehat v_Q(s))|}{|m|^2}\\
 &=\sum_{m\in R_Q}|\widehat p_{v_Q}(m)|
 \ge\frac1{10}c_Q^2N^2
 >\frac{N}{20(1.011)^2Q^2}
 =c_*Q\longrightarrow\infty,
 \end{aligned}
\tag{AX.14}
\]

其中 \(c_*=[20(1.011)^2\,10^6]^{-1}>0\)。这已经是受保护输出区的
实际压力 Fourier--\(\ell^1\) 下界，不只是把可能互相抵消的双和预先
取绝对值。负输出 \(-R_Q\) 给出其共轭副本，但下界不需要再计一次。

## 4. 固定任意 \(L^2\) 能量且保留同一高频压力

给定任意 \(E_0>0\)。由 AX.11，充分大的 \(Q\) 满足
\(2Nc_Q^2<2E_0/V_{\mathbb T}\)。取正数

\[
 d_Q^2=\frac{2E_0}{V_{\mathbb T}}-2Nc_Q^2,
 \qquad
 u_Q=v_Q+d_Qe_3\cos x_1.
\tag{AX.15}
\]

新增低模与所有块频率正交，并且 \(e_1\cdot e_3=0\)。所以 \(u_Q\)
仍是实值、光滑、零均值、无散的有限 Fourier 场，而且

\[
 \begin{aligned}
 \|u_Q\|_2^2
 &=V_{\mathbb T}Nc_Q^2+\frac{V_{\mathbb T}}2d_Q^2=E_0,\\
 \|\nabla u_Q\|_2^2
 &=\frac{V_{\mathbb T}}2+\frac{V_{\mathbb T}}2d_Q^2
 =\frac{V_{\mathbb T}}2+E_0-V_{\mathbb T}Nc_Q^2
 \le\frac{V_{\mathbb T}}2+E_0.
 \end{aligned}
\tag{AX.16}
\]

低模的自压力为零：其速度极化为 \(e_3\)，而自相互作用输出平行
\(e_1\)。低模与 \(A_Q\) 相加的输出第二坐标绝对值小于 \(q\)，与
\(B_Q\) 相加的输出第一坐标绝对值至多 \(q\)；各种差频及负共轭也不在
\(R_Q\)。因此

\[
 \widehat p_{u_Q}(m)=\widehat p_{v_Q}(m)
 \qquad(m\in R_Q).
\tag{AX.17}
\]

再固定 AK.1--AK.2 的实偶平滑低通乘子 \(\varphi\)，即
\(\varphi=1\) 于 \(|\xi|\le1\)、\(\varphi=0\) 于 \(|\xi|\ge2\)，并令
\(P_{>K}=I-P_{\le K}\)。对任意 \(K\ge1\)，选择 \(q\) 充分大使
\(Q=100q>2K\)。全部块频率及其负共轭满足 \(|n|>2K\)，而低模满足
\(|e_1|\le K\)，故精确有

\[
 P_{>K}(d_Qe_3\cos x_1)=0,\qquad
 P_{>K}v_Q=v_Q,\qquad
 h_Q:=P_{>K}u_Q=v_Q.
\tag{AX.18}
\]

这里没有把平滑乘子当作锐投影：该场在过渡带
\(K<|n|<2K\) 中没有 Fourier 支持，所以乘子在现有各模上分别恒为
零或一。结合 AX.14--AX.18，得到精确的固定能量反检查

\[
 \begin{gathered}
 \|u_Q\|_2^2=E_0,\qquad
 \|\nabla u_Q\|_2^2\le E_0+\frac{V_{\mathbb T}}2,\\
 \sum_{m\ne0}|\widehat p_{P_{>K}u_Q}(m)|
 \ge\sum_{m\in R_Q}|\widehat p_{h_Q}(m)|
 \ge c_*Q\longrightarrow\infty.
 \end{gathered}
\tag{AX.19}
\]

因此，不存在只依赖固定 \(E_0\) 与统一 \(H^1\) 上界的常数，普遍控制
这种压力 Fourier--\(\ell^1\) 绝对成本。等价地，单对模态方向系数
至多一并不足以关闭总和：这里有 \(N^2\) 个同号配对，而 \(H^1\)
归一化只有 \(c_Q^2\simeq(NQ^2)^{-1}\)，留下
\(N/Q^2\simeq Q\) 的 Schur 累积。

同一下界也能避开一个预先固定的压力低输出范围。具体地，任意固定
\(K,L\ge1\)，可选择 \(q\) 充分大使
\(Q=100q>2\max\{K,L\}\)。由 AX.9，每个 \(m\in R_Q\) 都满足
\(|m|\ge\sqrt2Q>2L\)。若沿用 AR 的同一个平滑输出乘子并记
\(p_{h_Q}^{>L}=P_{>L}p_{h_Q}\)，则该乘子在 \(R_Q\) 上精确等于一，
因而

\[
 \widehat{p_{h_Q}^{>L}}(m)=\widehat p_{h_Q}(m)
 \quad(m\in R_Q),\qquad
 \sum_{m\ne0}
   |\widehat{P_{>L}p_{P_{>K}u_Q}}(m)|
 \ge c_*Q\longrightarrow\infty.
\tag{AX.20}
\]

这里 \(K,L\) 在静态场族中预先固定。本式没有把 \(L\) 改成依赖
AQ 大范数窗口的阈值，也没有构造同一条 NS 轨道上的动态序列。

## 5. 结论的严格边界

AX.19--AX.20 排除的是一条瞬时、压力一侧、逐对绝对值或完整压力
Fourier--\(\ell^1\) 型的统一能量预算。它没有加入 exact-pressure
恒等式中的最终系数
\(\widehat{\operatorname{div}(\chi|u|u)}(-m)\)。因此本稿没有证明：

- 原局部压力功的绝对值或符号净值无界；
- 空间相位抵消或与负耗散的关联不能关闭 AQ.8；
- 该静态场族属于同一条 Navier--Stokes 轨道；
- 成熟窗口、首次奇点条件或合同 G 失败。

若后续候选估计保留最终测试系数，就必须另行审查该系数与 AX.13 的
压力相位如何配对，不能把 AX.19--AX.20 自动移植过去。本稿也不提出最优性或
新颖性主张；它只关闭“角度权重加统一瞬时能量即可支付绝对总成本”
这一种直接路线。
