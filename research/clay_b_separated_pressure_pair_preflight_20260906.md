# 成熟窗口中分离低高压力的局部支付

2026-09-06。**INTERNAL / WORKING / NOT FROZEN / G OPEN / NOT CLAY。**

本稿从 AK.25 转向一个精确的速度相互作用分解。
目标是用无散条件支付含低频速度的压力贡献，保留完整局部配对。
剩余项是高频速度自相互作用产生的压力，不把它误称为单个速度尾。
这是局部解析推导，不宣称新颖性；独立审查另存记录。

## 1. 设置与精确分解

使用 AK 的周期域、平滑乘子、同一光滑解、固定球及窗口。
黏性在本稿取合同中的 1。记终端局部幅值为 \(\Lambda_A\)，
以免与任何耗散波数混淆。设

\[
 \delta=c_0r^2\Lambda_A^{-4}<t<T_*,\quad
 J=(t-\delta,t),\quad
 M=\sup_{0<\sigma<T_*}\|u(\sigma)\|_2>0,\quad
 A_J=\int_J\|\nabla u\|_2^2.
\tag{AM.1}
\]

其中 \(0<r<\pi/4\)、\(\Lambda_A=\|u(t)\|_{L^3(B_r)}>0\)。
截止满足 \(0\le\chi\le1\)、在 \(B_r\) 为 1、支撑于 \(B_{2r}\)，
并有 \(\|\nabla\chi\|_\infty\le C_\chi/r\)。使用 AB 的
\(H_\chi=\frac13\int\chi|u|^3\) 与 \(D_\chi={\cal D}_\chi\)。
若讨论成熟窗口，另要求 \(t-\delta\ge Cr^2\)；以下估计本身不借此
假定任何高阶范数一致有界。

对固定 \(K\ge1\)，令

\[
 l=P_{\le K}u,\quad h=P_{>K}u,\quad
 b=(P_{\le8K}-P_{\le K})u,\quad w=P_{>8K}u,
 \qquad h=b+w.
\tag{AM.2}
\]

这些都是无散场；平滑乘子不是幂等投影。
令 \(T_{ij}=\partial_i\partial_j(-\Delta)^{-1}\)，零 Fourier 模取零，
并定义零均值对称双线性压力

\[
 \Pi(a,b)=T_{ij}(a_i b_j+b_i a_j),\qquad p(a)=T_{ij}(a_i a_j).
\tag{AM.3}
\]

完整压力的精确分解是

\[
 p(u)=p_0+p_{lh}+p(h),\qquad
 p_0=p(l)+\Pi(l,b),\quad p_{lh}=\Pi(l,w).
\tag{AM.4}
\]

这里没有删除 \(b\) 与 \(w\) 的交互；它们全部留在 \(p(h)\) 中。
\(l\) 支持于 \(|k|\le2K\)，\(b\) 支持于 \(|k|\le16K\)，
所以 \(p_0\) 支持于 \(|k|\le18K\)。各乘子有统一的 \(L^2\) 界，
Fourier 系数乘积界及格点计数给出

\[
 \|\nabla p_0\|_\infty\le CM^2K^4,\qquad
 \left|{\cal K}_\chi(p_0)\right|\le CM^4K^4,
 \quad {\cal K}_\chi(p)= -\int\chi|u|u\cdot\nabla p.
\tag{AM.5}
\]

因而 \(p_0\) 沿用 AK 的完整配对支付，不分别估计压力壳项。
本稿的新分解与 AK 的压力输出分解不同；AM.4 是替代恒等式，
不是把 \(p(h)\) 等同于 \(P_{>K}p(u)\)。

## 2. 无散条件产生的低高梯度增益

令

\[
 Q_j=8K2^j,\quad
 w_j=(P_{\le2Q_j}-P_{\le Q_j})u,\quad j\ge0,
 \qquad w=\sum_{j\ge0}w_j.
\tag{AM.6}
\]

严格前奇点的光滑紧时间区间内该和光滑收敛。
\(w_j\) 支持于 \(Q_j\le|k|\le4Q_j\)。
以下用 \(a,b\in\{1,2,3\}\) 表示空间分量，\(j\) 只表示频带。
对每个频带，直接展开两次散度并用 \(\operatorname{div}l=
\operatorname{div}w_j=0\)，得到

\[
 \begin{aligned}
 -\Delta\Pi(l,w_j)
 &=2(\partial_a l_b)(\partial_b w_{j,a})\\
 &=2\partial_b\big((\partial_a l_b)w_{j,a}\big),\\
 \Pi(l,w_j)
 &=2(-\Delta)^{-1}\partial_b
                 \big((\partial_a l_b)w_{j,a}\big).
 \end{aligned}
\tag{AM.7}
\]

恒定低频速度因而不产生该交叉压力。乘积 Fourier 支持位于
\(3Q_j/4\le |k|\le17Q_j/4\)。取固定光滑环带函数
在此环带为 1、支撑于 \(1/2\le|\xi|\le5\)，可在 AM.7
中的乘子前插入其 \(k/Q_j\) 缩放。
缩放后的 \((-\Delta)^{-1}\partial_b\) 核的周期 \(L^1\) 范数
至多 \(CQ_j^{-1}\)，加一阶梯度后至多 \(C\)：
这是紧支撑光滑 Euclidean 符号的 Schwartz 核经缩放、周期化后，
在一个周期上的绝对积分不超过其全空间绝对积分的直接结果。
因此包括两个端点在内，对 \(1\le s\le\infty\)，

\[
 \|\Pi(l,w_j)\|_s
 \le C Q_j^{-1}\|\nabla l\|_\infty\|w_j\|_s,
 \qquad
 \|\nabla\Pi(l,w_j)\|_s
 \le C\|\nabla l\|_\infty\|w_j\|_s.
\tag{AM.8}
\]

零总频率不在上述支持内，故没有对零频乘子作不合法延拓。
AM.8 保留频带符号；下一节用三角不等式只是一个充分估计。

## 3. 求和与完整局部配对

写 \(g=\|\nabla u\|_2\)、\(g_j=\|\nabla w_j\|_2\)。
格点 Bernstein、环带下界及有限重叠分别给

\[
 \|w_j\|_\infty\le C Q_j^{3/2}\|w_j\|_2
 \le C Q_j^{1/2}g_j,\quad
 \sum_jg_j^2\le Cg^2,\quad
 \|\nabla l\|_\infty\le CMK^{5/2}.
\tag{AM.9}
\]

最后一项也可直接由 Fourier Cauchy--Schwarz 和
\(\sum_{|k|\le2K}|k|^2\le CK^5\) 得到。
几何级数与序列 Cauchy--Schwarz 给

\[
 \sum_{j\ge0}Q_j^{-1}\|w_j\|_\infty
 \le C\left(\sum_jQ_j^{-1}\right)^{1/2}
          \left(\sum_jg_j^2\right)^{1/2}
 \le CK^{-1/2}g.
\tag{AM.10}
\]

由 AM.8--AM.10，

\[
 \|p_{lh}\|_\infty\le CMK^2g.
\tag{AM.11}
\]

特别地，仅有逐带 \(Q_j^{-1}\|w_j\|_\infty\le a\) 不足以
从三角求和推出 \(\sum_jQ_j^{-1}\|w_j\|_\infty\le Ca\)。
有限非负数列也可以有任意多项等于 \(a\)。这是对这一求和步骤的
警示，不是对实际 NS 场或带符号总配对的不可能性证明。
AM.10 使用的是能量导数，而非把逐带黏性小性当成可求和小性。

完整配对的分部积分为

\[
 {\cal K}_\chi(p_{lh})
 =\int\chi p_{lh}u\cdot\nabla|u|
       +\int p_{lh}|u|u\cdot\nabla\chi.
\tag{AM.12}
\]

\(z\mapsto|z|z\) 为 \(C^1\)，零速度处没有额外项。
压力 gauge 在合并配对中抵消；AM.11 使用的是规定的零均值 gauge。
令 \(B_\chi=\int\chi|u|\)，则

\[
 B_\chi\le Cr^{3/2}M,\qquad
 |{\cal K}_\chi(p_{lh})|
 \le \|p_{lh}\|_\infty
    \left(B_\chi^{1/2}D_\chi^{1/2}+C_\chi r^{-1}M^2\right).
\tag{AM.13}
\]

第一项由 \(|u\cdot\nabla|u||\le |u||\nabla u|\) 及加权
Cauchy--Schwarz 得到。对任意 \(\epsilon>0\)，Young 不等式给

\[
 |{\cal K}_\chi(p_{lh})|
 \le \epsilon D_\chi
      +C_{\epsilon,\chi}M^3 r^{3/2}K^4g^2
      +C_\chi M^3r^{-1}K^2g.
\tag{AM.14}
\]

所以对任意可测 \(J'\subset J\) 和 \(|\vartheta|\le1\)，

\[
 \left|\int_{J'}\vartheta{\cal K}_\chi(p_{lh})\right|
 \le\epsilon\int_{J'}D_\chi
   +C_{\epsilon,\chi}M^3r^{3/2}K^4A_J
   +C_\chi M^3r^{-1}K^2\delta^{1/2}A_J^{1/2}.
\tag{AM.15}
\]

这里时间 Cauchy--Schwarz 使用 \(|J'|\le\delta\)，并未替换任意
归一化权重的真实范数。由 \(H_\chi(t)\ge\Lambda_A^3/3\)，
AM.15 中除耗散以外的余项 \(R_{lh}\) 满足

\[
 \frac{R_{lh}}{H_\chi(t)}
 \le C_{\epsilon,\chi}M^3r^{3/2}K^4 A_J\Lambda_A^{-3}
   +C_\chi c_0^{1/2}M^3K^2 A_J^{1/2}\Lambda_A^{-5}.
\tag{AM.16}
\]

## 4. 同一解能量可以支付的部分

固定 \(M,r,c_0,\chi,\epsilon\)，令终端 \(\Lambda_A\to\infty\)。
取例如

\[
 K=\Lambda_A^{3/4}\ge1.
\tag{AM.17}
\]

由于 \(g^2\in L^1(0,T_*)\) 且 \(|J|\to0\)，有 \(A_J\to0\)。
AM.5 与 AM.16 分别给

\[
 \frac{\left|\int_{J'}\vartheta{\cal K}_\chi(p_0)\right|}{H_\chi(t)}
 \le Cc_0M^4r^2\Lambda_A^{-4}\longrightarrow0,
 \qquad
 \frac{R_{lh}}{H_\chi(t)}
 \le C_{\epsilon,\chi}M^3r^{3/2}A_J
       +C_\chi c_0^{1/2}M^3\Lambda_A^{-7/2}A_J^{1/2}
 \longrightarrow0.
\tag{AM.18}
\]

这不要求 AK.22 的额外多项式耗散率。
准确含义是：低频参与的压力项可以由任意固定的小份额耗散及
终端能量的相对小余项支付。尚未处理的是高频自相互作用。

取 \(s\in[t-\delta,t]\)，在 AB.3 中代入 AM.4。
令 \(S_\chi=\frac13\int\Delta\chi|u|^3+
\frac13\int |u|^3u\cdot\nabla\chi\) 为原有两个非压力截止项。
取 \(0<\epsilon<1\) 后，得到实际有利符号的不等式

\[
 H_\chi(s)\ge H_\chi(t)
 +(1-\epsilon)\int_s^tD_\chi
 -\int_s^t\big(S_\chi+{\cal K}_\chi(p(h))\big)
 -R_0-R_{lh},\qquad
 \frac{R_0+R_{lh}}{H_\chi(t)}\longrightarrow0.
\tag{AM.19}
\]

余项可以统一取 AM.18 给出的全窗口上界，故一致于所有上述 \(s\)。
并没有为 \(S_\chi\) 或 \(p(h)\) 的正工作给出所需上界。

## 5. 精确剩余项与边界

真正留下的压力贡献是

\[
 {\cal K}_\chi(p(h))
 =-\int\chi|u|u\cdot\nabla T_{ab}(h_a h_b),
 \qquad h=P_{>K}u.
\tag{AM.20}
\]

测试权重仍是完整原速度 \(|u|u\)，不是 \(|h|h\)。
\(p(h)\) 也含高高交互产生的低输出；本稿没有删去这些输出，
没有把小速度尾当作已经证明的局部吸收条件。
在 AM.17 下，AK.17 的速度尾坏时间估计仍含
\(A_J\Lambda_A^{13/4}\)，能量绝对连续性不保证它趋零。
因而 AM.19 虽减少了待付压力交互类别，仍不建立反向持留。

固定球之外的缩球常数、原移动路径、所有外壳和合同 G 保持 OPEN。
本稿只在严格前奇点光滑区间证明恒等式和一致估计；没有假定或证明
奇点端点处的经典迹。无仿真、科学图、新读者 PDF 或发布动作。
