# 扩张域中的常向量极限：真实 NS 有限段的反检查

2026-09-06。**PROVED METHOD OBSTRUCTION / NS SEGMENT SEQUENCE / G OPEN / NOT CLAY。**

我检查一个有限问题：统一速度界、零均值、整胞能量至多按边长
增长、归一化耗散趋零，加上历史长度趋于无穷，能否排除非零常向量
古老极限？答案是否定的，即便序列的每一项都是真实的光滑 NS 解。

这不是从同一固定初值出发的首次爆破序列。最后一节明确列出它与
那种序列缺失的历史对应关系；不能把本构造称为 NS 爆破反例。

## 1. 要保留和不保留的量词

记 \(\mathbb T_\ell^3=(\mathbb R/(2\pi\ell\mathbb Z))^3\)，
\(\ell\) 是周期尺度，实际边长为 \(2\pi\ell\)。所有空间积分
和 Sobolev 范数都使用未归一化 Lebesgue 测度，不除以胞体积。

本节构造 \(\ell_n\to\infty\)、\(b_n\to\infty\) 和黏性为 1 的
无外力光滑解 \(w_n\) 于 \(\mathbb T_{\ell_n}^3\times[-b_n,0]\)，
使其满足

\[
 \begin{gathered}
 \fint_{\mathbb T_{\ell_n}^3} w_n(s)=0,\qquad
 |w_n(0,0)|=1,\qquad
 \sup_{-b_n\le s\le0}\|w_n(s)\|_\infty\le1+o(1),\\
 \sup_s\int_{\mathbb T_{\ell_n}^3}|w_n|^2\le C\ell_n,
 \qquad
 \ell_n^{-1}\int_{-b_n}^0\int_{\mathbb T_{\ell_n}^3}
                      |\nabla w_n|^2\longrightarrow0 .
 \end{gathered}
\tag{BH.1}
\]

经周期提升和子列选择，它们在每个固定紧集
\(K\subset\mathbb R^3\times(-\infty,0]\) 上一致收敛到一个模长
为 1 的常向量。这里只要求终点归一化和过去上界 \(1+o(1)\)，
没有把每一项称为精确的历史 record。

## 2. 一个固定的无散种子

取非零常向量 \(a\) 和 \(\chi\in C_c^\infty(B_1)\)，使
\(\chi=1\) 于 \(B_{1/2}\)。令

\[
 V(z)=\nabla\times\left[\frac12\chi(z)(a\times z)\right].
\tag{BH.2}
\]

于是 \(V\in C_c^\infty(B_1)\)、\(\operatorname{div}V=0\)、
\(\int V=0\)，并且在 \(B_{1/2}\) 中有 \(V=a\)。最后一点来自
\(\nabla\times(a\times z)=2a\)；积分为零来自紧支撑 curl 的
积分分部。记 \(Q=\|V\|_\infty>0\)。不要求种子在核心取得
全域最大值。

将 \(V\) 周期化到 \(\mathbb T_{n^2}^3\)。支撑没有重叠，各阶
未归一化 Sobolev 范数均等于原种子的相应范数。令 \(U_n\) 解

\[
 \partial_\tau U_n+(U_n\cdot\nabla)U_n+\nabla P_n
      =n^{-1}\Delta U_n,\qquad
 \operatorname{div}U_n=0,\qquad U_n(0)=V.
\tag{BH.3}
\]

压力取每个时刻的零均值周期压力。这里黏性是 \(1/n>0\)；下一步
将它准确换成 1，不把小黏性方程直接叫作目标方程。

## 3. 大环面上一致的短时界

固定整数 \(m\ge5\)，使用非齐次、未归一化范数

\[
 \|f\|_{H^m(\mathbb T_\ell)}^2
      =\sum_{|\alpha|\le m}\|\partial^\alpha f\|_2^2 .
\tag{BH.4}
\]

当 \(\ell\ge1\) 时，所需 Sobolev 与整数阶乘积／交换子估计
常数可以一致。特别是 Fourier 展开中控制 \(L^\infty\) 的因子
为
\((2\pi\ell)^{-3}\sum_{k\in\mathbb Z^3}(1+|k/\ell|^2)^{-r}\)，
当 \(r>3/2\) 时在 \(\ell\ge1\) 上有界。给梯度增加一个权重
即可得到 \(H^m\to W^{1,\infty}\) 的一致性。整数阶 Leibniz 展开
与这些嵌入给一致乘积及交换子常数；周期 Leray 投影的 Fourier
矩阵模长不超过 1，零模无奇异项。

对 BH.3 逐项微分后与对应导数配对。最高阶输运项用无散性消去，
其余为交换子，黏性项非负，因此

\[
 \frac12\frac d{d\tau}\|U_n\|_{H^m}^2
    +n^{-1}\|\nabla U_n\|_{H^m}^2
 \le C_m\|\nabla U_n\|_\infty\|U_n\|_{H^m}^2
 \le C_m'\|U_n\|_{H^m}^3 .
\tag{BH.5}
\]

这是标准局部光滑存在估计，不是全局存在证明。其常数与 \(n\)
无关，初值范数也固定，所以普通周期光滑局部存在／延拓论给共同
\(\tau_0>0\) 和

\[
 \sup_{n\ge1}\sup_{0\le\tau\le\tau_0}
                   \|U_n(\tau)\|_{H^m}\le C_V .
\tag{BH.6}
\]

等价地，可在有限 Fourier Galerkin 方程先用 BH.5 取得同一寿命，
再对每个固定 \(n\) 通过标准局部紧性构造解。更高阶的 tame
估计由同一个 \(W^{1,\infty}\) 界控制，故光滑种子给光滑解。
这里使用的是通常的局部解接口；不把本节记作对全部局部存在理论
或文献依赖的独立重新证明。

用投影后的 BH.3 及 \(1/n\le1\) 有

\[
 \|\partial_\tau U_n\|_{H^{m-2}}
 \le C\bigl(\|U_n\|_{H^m}^2+n^{-1}\|U_n\|_{H^m}\bigr)
 \le C_V .
\tag{BH.7}
\]

因 \(H^{m-2}\hookrightarrow L^\infty\) 的常数一致，对充分大的
\(n\)，\(n^{-1/2}<\tau_0\)，从而

\[
 \sup_{0\le\tau\le n^{-1/2}}
       \|U_n(\tau)-V\|_\infty\le C_V n^{-1/2}.
\tag{BH.8}
\]

周期 NS 的积分给 \(\int U_n(\tau)=0\)，光滑能量等式给
\(\|U_n(\tau)\|_2\le\|V\|_2\)。这两点都保留完整压力，
没有把解替换成热流或 Euler 近似。

## 4. 单位黏性的真实解和整胞账本

令 \(L_n=n^3\)、\(A_n=\sqrt n\)，并在
\(\mathbb T_{L_n}^3\times[-A_n,0]\) 定义

\[
 v_n(y,s)=U_n\!\left(y/n,(s+\sqrt n)/n\right),\qquad
 p_n(y,s)=P_n\!\left(y/n,(s+\sqrt n)/n\right).
\tag{BH.9}
\]

时间导数、输运和压力梯度各有因子 \(1/n\)，BH.3 的黏性再有
因子 \(1/n\)，故精确得到

\[
 \partial_s v_n+(v_n\cdot\nabla_y)v_n+\nabla_y p_n
       =\Delta_yv_n,\qquad \operatorname{div}_y v_n=0 .
\tag{BH.10}
\]

实际解还存在到 \(s=n\tau_0-\sqrt n>0\)，所以 \(s=0\) 不是
一个缺少控制的开放端点。BH.8 给整个所选历史的统一速度界。
对每个固定 \(B_R\times[-S,0]\)，当 \(n\to\infty\) 时
\(y/n\to0\)、\((s+\sqrt n)/n\to0\)，故 \(v_n\to a\) 一致。

变量换元给整胞能量与整段耗散：

\[
 \sup_s\int_{\mathbb T_{L_n}^3}|v_n|^2dy
   =n^3\sup_\tau\|U_n(\tau)\|_2^2\le n^3\|V\|_2^2,
\tag{BH.11}
\]

\[
 \begin{split}
 \int_{-\sqrt n}^0\int_{\mathbb T_{L_n}^3}|\nabla_y v_n|^2dy\,ds
 &=n^2\int_0^{n^{-1/2}}\|\nabla U_n(\tau)\|_2^2d\tau\\
 &\le C_V n^{3/2}=o(L_n).
 \end{split}
\tag{BH.12}
\]

BH.12 最后一步使用 BH.6 的逐时梯度界，不是仅由小黏性能量
等式推出。若只用后者，只能得到 \(O(L_n)\)。

## 5. 终点峰值再归一化

取 \(q_n=\|v_n(0)\|_\infty\to Q>0\)，并在紧的周期胞上取
终点最大点 \(y_n\)。BH.8 说明对应的
\(z_n=y_n/n\pmod{2\pi n^2}\) 可选在种子支撑中；经过子列，
\(z_n\to z_*\)、\(|V(z_*)|=Q\)。令

\[
 w_n(y,s)=q_n^{-1}v_n(y_n+y/q_n,s/q_n^2),\qquad
 \pi_n(y,s)=q_n^{-2}p_n(y_n+y/q_n,s/q_n^2).
\tag{BH.13}
\]

这是 NS 的精确抛物缩放。周期尺度和历史长度变成

\[
 \ell_n=q_n n^3,\qquad b_n=q_n^2\sqrt n,
 \qquad |w_n(0,0)|=1,
 \qquad \sup_s\|w_n(s)\|_\infty\le1+O(n^{-1/2}).
\tag{BH.14}
\]

对固定紧柱，BH.8 和 \(z_n\to z_*\) 给

\[
 w_n(y,s)\longrightarrow c:=V(z_*)/Q,\qquad |c|=1,
 \quad\text{局部一致地于 }\mathbb R^3\times(-\infty,0].
\tag{BH.15}
\]

能量和时空耗散在 BH.13 下都乘 \(q_n\)，而周期尺度也乘
\(q_n\)，故 BH.11–12 给 BH.1。均值仍严格为零。每个 \(w_n\)
都满足真实 NS、光滑局部能量等式和周期零均值压力规范；这里与
BG 的非 NS 时间族不同。非零常向量 \(c\) 本身也是合法的古老
mild NS 解，完全不存在“得到 \(c\) 就矛盾”的结论。

## 6. 没有复制的固定初值历史

若从同一固定周期光滑初值 \(u_0\) 的首次候选奇点作速度峰值
缩放，令 \(M_k\to\infty\)、\(t_k\to T_*>0\)，则

\[
 \widetilde v_k(y,s)
   =M_k^{-1}u(x_k+y/M_k,t_k+s/M_k^2)
\tag{BH.16}
\]

在原周期尺度为 1 时，周期尺度为 \(M_k\)，完整过去长度为
\(M_k^2t_k\)。其比值与
完整左端初值具有额外对应：

\[
 \frac{M_k^2t_k}{M_k^2}\longrightarrow T_*>0,
 \qquad
 \|\widetilde v_k(-M_k^2t_k)\|_\infty
     =M_k^{-1}\|u_0\|_\infty\longrightarrow0 .
\tag{BH.17}
\]

相比之下，BH.14 的序列满足

\[
 \frac{b_n}{\ell_n^2}=n^{-11/2}\longrightarrow0,
 \qquad
 \|w_n(-b_n)\|_\infty=Q/q_n\longrightarrow1 .
\tag{BH.18}
\]

本构造也没有给每一项安排精确的 running-record 终点。因此它只
排除基于 BH.1 那组粗缩放预算的常量排除推断，不能排除利用
BH.17、同一固定初值来源、精确时间排序或其他真实 NS 结构的方案。
实际峰值序列的整段耗散也不必自动是 \(o(M_k)\)；本构造主动
满足更小的归一化耗散，仍不足以用这些粗数据排常量。

这是一个明确的来源／归一化反检查，不作新颖性声明，不称 G 的
新桥梁。它既不构造固定初值的有限时奇点，也不排除这样的奇点。
无仿真、科学图、DGX 或新读者 PDF。
