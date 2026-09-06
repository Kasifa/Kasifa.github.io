# 全环面高高压力的小尾原型

2026-09-06。**INTERNAL / WORKING / NOT FROZEN / G OPEN / NOT CLAY。**

本稿只处理 AM.20 的全环面原型。令高频速度
\(h=P_{>K}u\)，但压力测试仍使用完整原速度 \(u\)；
不把它改成 \(|h|h\)。目标是核对“小 \(L^3\) 高频尾”究竟能吸收
多少高高压力功，以及时间 good set 上还必须保留哪些量。
这是标准周期 Calderón--Zygmund、Sobolev 和能量估计的组合，
不宣称新颖性或正则性结论。

以下取黏性为 1，空间范数均为
\(\mathbb T^3=(-\pi,\pi]^3\) 上的非归一化范数。
所有推导先在同一解的 \(0<s<t<T_*\) 光滑紧时间区间进行，
时间集合及时间积分均在该解的定义域内。记

\[
 L(\sigma)=\|u(\sigma)\|_3,\qquad
 H(\sigma)=\frac13L(\sigma)^3,\qquad
 D(\sigma)=\int_{\mathbb T^3}
 \left(|u||\nabla u|^2+|u||\nabla|u||^2\right)dx .
\tag{AN.1}
\]

## 1. 高频乘子的 \(K\)-一致有界性

沿用 AK.1--AK.2 的实偶光滑函数 \(\varphi\)，定义

\[
 \widehat{P_{\leq K}f}(k)=\varphi(k/K)\widehat f(k),
 \qquad P_{>K}=I-P_{\leq K},\qquad K\geq1.
\tag{AN.2}
\]

若 \(\Phi={\cal F}_{\mathbb R^3}^{-1}\varphi\)，则
\(P_{\leq K}\) 的周期卷积核在无关的 Fourier 归一化常数之外可写成

\[
 {\cal P}_K(x)
 =\sum_{m\in\mathbb Z^3}K^3
       \Phi\!\left(K(x+2\pi m)\right).
\tag{AN.3}
\]

因此

\[
 \|{\cal P}_K\|_{L^1(\mathbb T^3)}
 \leq\int_{\mathbb R^3}K^3|\Phi(Ky)|\,dy
 =\|\Phi\|_{L^1(\mathbb R^3)}.
\tag{AN.4}
\]

周期 Young 不等式给出，对所有 \(1\leq q\leq\infty\)，

\[
 \|P_{\leq K}f\|_q\leq C_\varphi\|f\|_q,\qquad
 \|P_{>K}f\|_q\leq(1+C_\varphi)\|f\|_q,
\tag{AN.5}
\]

常数与 \(K\) 无关。特别地，下面使用的 \(q=9\) 界不是一个
随截断频率增长的 Bernstein 估计。

## 2. 高高压力功的逐时估计

令

\[
 h=P_{>K}u,\qquad
 \eta_K=\|h\|_3,\qquad
 p_h=T_{ij}(h_i h_j),\qquad
 T_{ij}=\partial_i\partial_j(-\Delta)^{-1},
\tag{AN.6}
\]

其中 \(T_{ij}\) 的零 Fourier 模取零。这里没有对 \(p_h\)
再施加高频投影；\(h_i h_j\) 的高--高相互作用产生的所有低频输出
都保留在 \(p_h\) 中。定义

\[
 W_h=\int_{\mathbb T^3}p_h\,u\cdot\nabla|u|\,dx .
\tag{AN.7}
\]

在零速度处按 AB 的正则化极限解释。加权 Cauchy--Schwarz 与
空间 Hölder 给出

\[
 \begin{aligned}
 |W_h|
 &\leq D^{1/2}
       \left(\int_{\mathbb T^3}|p_h|^2|u|\,dx\right)^{1/2}\\
 &\leq D^{1/2}\|p_h\|_{9/4}\|u\|_9^{1/2}.
 \end{aligned}
\tag{AN.8}
\]

周期 Riesz 变换在 \(L^{9/4}\) 上有界，而且
\(4/9=1/3+1/9\)。结合 AN.5，

\[
 \|p_h\|_{9/4}
 \leq C\|h_i h_j\|_{9/4}
 \leq C\|h\|_3\|h\|_9
 \leq C\eta_K\|u\|_9.
\tag{AN.9}
\]

将 AN.9 代入 AN.8 得

\[
 |W_h|\leq C\eta_KD^{1/2}\|u\|_9^{3/2}.
\tag{AN.10}
\]

非零均值不能从周期 Sobolev 中删除。对
\(F=|u|^{3/2}\) 使用非齐次版本，

\[
 \begin{aligned}
 \|u\|_9^{3/2}=\|F\|_6
 &\leq C\bigl(\|\nabla F\|_2+\|F\|_2\bigr)\\
 &\leq C\bigl(D^{1/2}+L^{3/2}\bigr).
 \end{aligned}
\tag{AN.11}
\]

其中
\(\|\nabla F\|_2^2=\frac94\int|u||\nabla|u||^2\leq\frac94D\)
按正则化理解，而 \(\|F\|_2=L^{3/2}\)。
因此得到所需的全环面小尾原型

\[
 \boxed{\quad
 |W_h|\leq C\eta_KD+
 C\eta_KD^{1/2}L^{3/2}.
 \quad}
\tag{AN.12}
\]

对任意 \(\varepsilon>0\)，Young 不等式进一步给

\[
 |W_h|
 \leq(C\eta_K+\varepsilon)D+
 C_\varepsilon\eta_K^2L^3.
\tag{AN.13}
\]

令 \(C_*\) 是 AN.13 中第一项的固定常数。取

\[
 \eta_*\leq(4C_*)^{-1},\qquad \varepsilon=\frac14,
\tag{AN.14}
\]

则在 \(\eta_K\leq\eta_*\) 的时刻，

\[
 |W_h|\leq\frac12D+C\eta_*^2L^3.
\tag{AN.15}
\]

阈值只依赖固定环面、乘子和 Calderón--Zygmund 常数，与
\(K,t,u\) 无关。若恢复黏性 \(\nu\)，可吸收阈值相应为
\(\eta_*=O(\nu)\)；本稿不使用这一缩放去声称 \(\nu\)-一致结论。

## 3. good set、bad set 与完整反向条件

对任意时间区间 \(I=(s,t)\)，定义

\[
 G=G_{K,\eta_*}(I)
 =\{\sigma\in I:\eta_K(\sigma)\leq\eta_*\},\qquad
 B=I\setminus G.
\tag{AN.16}
\]

AN.15 只给

\[
 \int_G|W_h|\,d\sigma
 \leq\frac12\int_GD\,d\sigma
     +C\eta_*^2\int_G L(\sigma)^3\,d\sigma.
\tag{AN.17}
\]

最后一项是**当前时间能量的积分**，不能未经证明改成
\(|I|L(t)^3\)。bad set 上也没有小尾系数。由 AN.5，
\(\eta_K\leq C L\)，所以 AN.12 至多恢复

\[
 \int_B|W_h|\,d\sigma
 \leq C\int_BLD\,d\sigma+
       C\int_BL^{5/2}D^{1/2}\,d\sigma.
\tag{AN.18}
\]

bad set 测度小本身不控制右侧，因为 \(LD\) 和压力功都可能与
bad set 同时集中。

更精确地，用 AM.4 在全环面写
\(p(u)=p_0+p_{lh}+p_h\)，并令

\[
 W_{\rm other}
 =\int_{\mathbb T^3}(p_0+p_{lh})u\cdot\nabla|u|\,dx,\qquad
 R_{\rm other}(I)
 =\left|\int_IW_{\rm other}\,d\sigma\right|.
\tag{AN.19}
\]

全环面恒等式 \(H'+D=W_{\rm other}+W_h\) 的反向积分与
AN.17 给出

\[
 \begin{aligned}
 H(s)\geq{}&H(t)
 +\frac12\int_GD\,d\sigma+\int_BD\,d\sigma\\
 &-C\eta_*^2\int_GL^3\,d\sigma
 -\int_B|W_h|\,d\sigma-R_{\rm other}(I).
 \end{aligned}
\tag{AN.20}
\]

AN.20 是完整条件式：要从它推出持留，必须分别支付
\(\int_G L^3\)、bad-set 压力功和其他压力贡献。
本稿没有把后两项设为零，也没有用 \(|B|\ll|I|\) 代替其积分控制。

## 4. 能量可以支付 good-set 的当前 \(H\) 积分

虽然不能直接令 \(L(\sigma)\) 等于终端 \(L(t)\)，全局能量类
仍给一个合法的时间积分界。若
\(M=\sup_{\sigma\in I}\|u(\sigma)\|_2\)，则非齐次 Sobolev 和插值给

\[
 L^4
 \leq\|u\|_2^2\|u\|_6^2
 \leq CM^2\bigl(\|\nabla u\|_2^2+M^2\bigr).
\tag{AN.21}
\]

记 \(A_I=\int_I\|\nabla u\|_2^2\)。时间 Hölder 因而给

\[
 \int_I L^3\,d\sigma
 \leq |I|^{1/4}\left(\int_I L^4\,d\sigma\right)^{3/4}
 \leq CM^{3/2}|I|^{1/4}
       \bigl(A_I+M^2|I|\bigr)^{3/4}.
\tag{AN.22}
\]

这一步是从能量推导，而不是终端能量的单调性。
若 \(I\subset J=(t-\delta,t)\) 且使用 AK 窗口

\[
 \delta=c_0r^2\Lambda_A^{-4},\qquad
 \Lambda_A=\|u(t)\|_{L^3(B_r)},
\tag{AN.23}
\]

则 \(|I|\leq\delta\)、\(A_I\leq A_J\)，而
\(H(t)\geq\Lambda_A^3/3\)。所以

\[
 \frac{\displaystyle\int_G L^3\,d\sigma}{H(t)}
 \leq
 CM^{3/2}c_0^{1/4}r^{1/2}\Lambda_A^{-4}
 \bigl(A_J+M^2c_0r^2\Lambda_A^{-4}\bigr)^{3/4}.
\tag{AN.24}
\]

固定 \(M,r,c_0\) 且总耗散有限时，AN.24 在
\(\Lambda_A\to\infty\) 时趋零。故 good-set 中
\(C\eta_*^2\int_GL^3\) 确可相对终端能量支付；
这仍未触及 AN.18 的 bad-set 项。

## 5. 能量尾测度尚不支付 bad-set 工作

AK.16 对同一 \(h=P_{>K}u\) 给

\[
 \int_J\eta_K(\sigma)^2\,d\sigma\leq CK^{-1}A_J.
\tag{AN.25}
\]

所以

\[
 \frac{|B_{K,\eta_*}(J)|}{\delta}
 \leq\frac{CA_J}{\eta_*^2K\delta}.
\tag{AN.26}
\]

例如 AM 取 \(K=\Lambda_A^{3/4}\) 时，

\[
 \frac{|B_{K,\eta_*}(J)|}{\delta}
 \leq
 \frac{CA_J\Lambda_A^{13/4}}
      {\eta_*^2c_0r^2}.
\tag{AN.27}
\]

能量绝对连续性只给 \(A_J=o(1)\)，并不保证 AN.27 趋零。
而且即便另有条件使 AN.27 趋零，仍须独立控制
\(\int_B|W_h|\)；小测度不排除耗散和压力功在 \(B\) 上集中。

因此 AN.20 在 AK/AM 路线中可安全写成如下充分条件接口：
若沿某个终端序列同时有

\[
 \frac{\int_B|W_h|+R_{\rm other}(I)}{H(t)}\longrightarrow0,
\tag{AN.28}
\]

则 AN.24 支付 good-set 的当前能量项，AN.15 吸收其一半耗散。
AN.28 目前没有由同一解能量推出；它只是准确标出剩余工作，
不能改名为已经证明的临界尾条件。

## 6. 适用边界

AN.12--AN.15 是全环面逐时原型，并保留了 \(p_h\) 的全部低输出。
它们不能直接替代 AM.20 的局部完整配对，因为后者还含空间截止，
分部积分后会出现
\(\int p_h|u|u\cdot\nabla\chi\)；局部耗散也不是这里的全局 \(D\)。

本稿没有证明 bad-set 功可忽略，没有证明高频尾在成熟窗口多数时间
小于吸收阈值，也没有建立反向持留、首次奇点排除、缩球路径或合同 G。
它只给下一步局部化时必须保留的精确全环面基准。
无仿真或科学图；仅作内部源文件记录，不作为新 release 移交。
