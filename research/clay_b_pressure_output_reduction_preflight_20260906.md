# 坏时间净工作的压力输出截断

2026-09-06。**INTERNAL / PROVED LOCALLY / NECESSARY CONDITION / G OPEN / NOT CLAY。**

本稿继续 AQ.8，不改变原来的解、固定环带、截止、好坏时间集或积分因子。
我先检查压力输出中还有哪些部分可以支付，再区分真正的无散增益与
不存在的高高低输出小性。以下不是新颖性或一般正则性主张。

## 1. 独立的压力输出阈值

完整沿用 AO--AQ 的设置。特别地，所有计算先在同一解的严格前奇点
光滑紧时间区间上进行。记

\[
 M=\sup_{0<\sigma<T_*}\|u(\sigma)\|_2>0,\quad
 h=P_{>K}u,\quad p_h=T_{ij}(h_i h_j),\quad
 T_{ij}=\partial_i\partial_j(-\Delta)^{-1},
 \qquad \widehat T_{ij}(0)=0.
\tag{AR.1}
\]

乘子仍是 AK 的固定实偶平滑乘子。对每个窗口另选一个固定
压力输出阈值 \(L\ge1\)，定义

\[
 p_h^{\le L}=P_{\le L}p_h,\quad
 p_h^{>L}=P_{>L}p_h,
 \qquad p_h=p_h^{\le L}+p_h^{>L}.
\tag{AR.2}
\]

L 可以依赖窗口终端，但在该窗口内不随时间变化。
这不是把 p_h 换成高频速度的单独某个频带，也不要求平滑截断幂等。

由 \(\|h\|_2\le M\)，Fourier 系数 Cauchy--Schwarz 给
\(|\widehat p_h(m)|\le CM^2\)。有限格点求和因而给

\[
 \|\nabla p_h^{\le L}\|_\infty
 \le CM^2\sum_{0<|m|\le2L}|m|
 \le CM^2L^4.
\tag{AR.3}
\]

沿用完整带符号配对
\({\cal K}_\chi(p)=-\int\chi|u|u\cdot\nabla p\)，而不分开压力内项与壳项。
由 \(0\le\chi\le1\)，有

\[
 |{\cal K}_\chi(p_h^{\le L})|
 \le \|\nabla p_h^{\le L}\|_\infty\int\chi|u|^2
 \le CM^4L^4.
\tag{AR.4}
\]

## 2. 在同一坏时间上移项

仍取 AO.17 的合法窗口及 AQ 的实际早时点和权重；以下 w_J
只在 \([s_J,t]\) 上使用，所写 \(w_J\le1\) 也只在此区间成立：

\[
 \delta=c_0r^2\Lambda_A^{-4},\quad J=(t-\delta,t),\quad
 K=\Lambda_A^{3/4},\quad H_t=H_\chi(t)\ge\Lambda_A^3/3,
 \qquad 0<w_J\le1.
\tag{AR.5}
\]

对任意可测 \(E\subset J\)、任意可测 \(|v(\sigma)|\le1\)，AR.4 给

\[
 \frac{\displaystyle\int_E
           |v(\sigma){\cal K}_\chi(p_h^{\le L})(\sigma)|\,d\sigma}{H_t}
 \le Cc_0M^4r^2L^4\Lambda_A^{-7}.
\tag{AR.6}
\]

因此固定数据的合法大范数序列上，只要

\[
 L=o(\Lambda_A^{7/4}),
\tag{AR.7}
\]

这一项就为 o(1)。例如 \(L=\Lambda_A^{3/2}\) 时，AR.6 为
\(O(\Lambda_A^{-1})\)，且 L 远大于既定速度输入阈值 K。
此处不需要好时间占多数，也不要求额外的 \(A_J\) 衰减率。

定义保留同一耗散份额的剩余量

\[
 \beta_K^{>L}={\cal K}_\chi(p_h^{>L})-\tfrac34D_\chi,
 \qquad
 \mathcal B_J^{>L}=\int_{B_K}[\beta_K^{>L}]_+\,d\sigma.
\tag{AR.8}
\]

原 \(\beta_K=\beta_K^{>L}+{\cal K}_\chi(p_h^{\le L})\)。正部函数
为 1-Lipschitz，故 AR.6 直接给

\[
 \frac{|\mathcal B_J^{>L}-\mathcal B_J|}{H_t}
 \le Cc_0M^4r^2L^4\Lambda_A^{-7}\longrightarrow0.
\tag{AR.9}
\]

从 AQ.6 与 AQ.8 分别得到

\[
 \boxed{\quad
 \liminf\frac{\mathcal B_J^{>L}}{H_t}\ge1,
 \qquad
 \liminf\frac1{H_t}\int_{s_J}^t
       w_J\mathbf1_{B_K}\beta_K^{>L}\,d\sigma\ge1.
 \quad}
\tag{AR.10}
\]

第二条只是在 AQ.8 中线性减去 AR.6 控制的低输出压力功。
没有更换 \(B_K\)、\(G_K\)、\(s_J\) 或 \(w_J\)，也没有把四分之三
耗散再任意分摊给已付低输出。两个下极限仍以合法序列存在为条件。

## 3. 剩余输出要求至少一个更高输入

当 \(L\ge4\) 时取

\[
 a=P_{\le L/4}h,\qquad b=P_{>L/4}h,\qquad h=a+b.
\tag{AR.11}
\]

a 的支持在 \(|k|\le L/2\)，所以其张量支持在 \(|m|\le L\)。
高输出乘子在这个球内恒为零，于是精确有

\[
 p_h^{>L}
 =P_{>L}T_{ij}(a_i b_j+b_i a_j+b_i b_j).
\tag{AR.12}
\]

这只说明至少一个输入被推到更高频率，不声称二者都高于 L。
逐 Fourier 三频相互作用的准确条件为

\[
 m=k+\ell,\quad |m|>L
 \quad\Longrightarrow\quad
 \max\{|k|,|\ell|\}>L/2.
\tag{AR.13}
\]

原 h 的两个输入仍各在 K 以上。L 到 2L 的平滑输出过渡必须保留；
a 和 b 也有平滑过渡重叠，不能称为严格分离的频带。

投影与 T、空间导数交换，但不与 chi 交换。AR.4 和 AR.9--AR.10
只用了完整配对对压力的线性，没有将投影穿过 chi。
若以后改写测试函数的频率分解，必须另外保留空间截止交换子。

## 4. 无散性不给压力低输出额外正幂增益

这一点可由一个静态双模精确检查。取整数 \(Q\ge8\ell\)、\(\ell\ge1\)，
令 \(s=(Q^2+\ell^2)^{1/2}\)，并定义

\[
 k=(Q,0,0),\quad m=(Q,-\ell,0),\quad
 A=(0,1,0),\quad B=(\ell,Q,0)/s,\quad
 v=A\cos(k\cdot x)+B\cos(m\cdot x).
\tag{AR.14}
\]

\(k\cdot A=m\cdot B=0\)，所以 v 是实值、光滑、零均值、无散周期场。
两个输入频率可比于 Q，且 \(\|v\|_2^2=(2\pi)^3\)，不随 Q 增长。
每个单模的自压力为零。使用 \(2\cos a\cos b=\cos(a-b)+\cos(a+b)\)
和零模压力规范，直接得到完整压力

\[
 p(v)=-\frac{Q}{s}\cos(\ell x_2)
 +\frac{\ell^2Q}{s(4Q^2+\ell^2)}
               \cos(2Qx_1-\ell x_2).
\tag{AR.15}
\]

因此低压力模的振幅为

\[
 \frac{Q}{\sqrt{Q^2+\ell^2}}\longrightarrow1
 \qquad(\ell/Q\to0).
\tag{AR.16}
\]

所以任何声称该压力低模振幅由
\(C(\ell/Q)^\gamma\|A\|\|B\|\)、\(\gamma>0\) 普遍控制的估计都不成立。
无散性确实把该模的双散度源降到 \(O(\ell^2)\)，而不是 \(O(Q^2)\)；
但求压力时的逆 Laplacian 正好乘 \(\ell^{-2}\)。不能只算前一半增益。

这个反证针对一条静态逐模压力估计。它不说明该场的非线性压力工作
有任何特定符号，更不是一条实际 NS 终端轨道、奇点或成熟窗口反例。
它也不否定在额外速度正则性范数下已知的双倍压力正则性。

## 5. 第二个输出预算：使用能量梯度

h 无散、零均值，而且 \(\|\nabla h\|_2\le g:=\|\nabla u\|_2\)。
因此还有一条不需要双倍 Besov 正则性定理的直接估计：

\[
 \begin{aligned}
 \nabla p_h&=\nabla(-\Delta)^{-1}
                         \operatorname{div}((h\cdot\nabla)h),\\
 \|\nabla p_h\|_{3/2}
 &\le C\|h\|_6\|\nabla h\|_2
 \le C\|\nabla h\|_2^2\le Cg^2.
 \end{aligned}
\tag{AR.17}
\]

第一行的组合是零阶周期 Calderón--Zygmund 算子；第二行使用零均值
h 的 Sobolev，不是把全速度均值从周期 Sobolev 中删掉。
平滑低通的 L3/2 到 L infinity Bernstein 因子是 L 的平方，故

\[
 \|\nabla p_h^{\le L}\|_\infty\le CL^2g^2,
 \qquad
 |{\cal K}_\chi(p_h^{\le L})|\le CM^2L^2g^2.
\tag{AR.18}
\]

令 \(A_J=\int_Jg^2\)。AR.6 的归一化左侧事实上有两个同时有效的上界，
因此可取其最小值：

\[
 e_J(L):=C\min\left\{
 c_0M^4r^2L^4\Lambda_A^{-7},\;
 M^2L^2A_J\Lambda_A^{-3}\right\}.
\tag{AR.19}
\]

只要 \(e_J(L)\to0\)，AR.9--AR.10 的结论全部保持。
AR.7 是第一界提供的充分条件，不是现在全部允许的 L。
例如 \(A_J>0\) 时可另取 \(L=\Lambda_A^{3/2}A_J^{-1/4}\)，
第二项至多 \(CM^2\sqrt{A_J}\to0\)。这项选择不必满足 AR.7，
也不声称最优。若 \(A_J=0\)，第二个上界本身为零，任意有限 L
均可使用，不代入含负幂的选择式。

## 6. 与窗口扩散频率的差额

为核对后续热半群能提供什么，定义该窗口的扩散频率

\[
 L_{\rm diff}:=\delta^{-1/2}
 =c_0^{-1/2}r^{-1}\Lambda_A^2.
\tag{AR.20}
\]

这只是线性热因子 \(\exp(-|m|^2\delta)\) 的尺度，不是对非线性 NS
演化的额外假设。若仅用 AR.7，则
\(\delta L^2=o(\Lambda_A^{-1/2})\to0\)：可删除的统一输出范围
尚低于窗口的扩散频率，不能随即声称其以上的全部剩余输出都被强烈热衰减。

在 \(L=L_{\rm diff}\) 使用第二个预算则给

\[
 e_J(L_{\rm diff})
 \le C M^2c_0^{-1}r^{-2}A_J\Lambda_A.
\tag{AR.21}
\]

所以 \(A_J=o(\Lambda_A^{-1})\) 足以让这一具体上界支付到扩散频率，
但能量绝对连续性只给 \(A_J=o(1)\)。这是该估计的未付速率，
不是 NS 必须满足的速率，也不证明其他带符号估计不可能成功。
即便低输出支付到这个频率，后续非线性源项仍需独立控制。

## 7. 当前用途与边界

AR.9--AR.10 将必要净工作集中进一步限制到可选的高压力输出，而不是
把全部高高低输出永远留作缺口。AR.15 排除一种不合法的额外增益。
两者都没有为剩余带符号工作提供所需上界。

下一步是精确检查 AR.12 中可比高频与分离高频配对，并区分空间
压力增益与真实时间演化能提供的控制，不把双散度增益直接当成耗散支付。
原固定参数、同一解和指定中心量词保留。
G、移动缩球、一般正则性和新颖性均没有由本稿解决。
本稿尚处内部子步骤，无仿真、科学图、新读者 PDF 或发布动作。
