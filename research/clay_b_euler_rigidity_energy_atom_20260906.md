# 宽 Euler 极限类的已知反例与原解能量集中

2026-09-06。**INTERNAL / LITERATURE OBSTRUCTION / CONDITIONAL NECESSITY / NON-AUTHOR REVIEW PASS / G OPEN / NOT CLAY。**

BL 给条件紧性，不给极限刚性。我在这里核对两个不同问题：
得到的宽 Euler 类是否可能全零；同一固定 NS 来源还意味着什么。
二者不能互相替代。

## 1. 已知定常流确实落在宽极限类中

Gavrilov 的原作者预印本 [arXiv:1810.08020v1](https://arxiv.org/abs/1810.08020v1)
首页定理构造非零光滑紧支撑的三维定常 Euler 流；其期刊记录为
[GAFA 29, 190--197 (2019)](https://doi.org/10.1007/s00039-019-00476-6)。
这里把它作为已发表的文献存在性结果，不冒充本项目独立构造。

原文 §3 先得到局部流 \(v,p\)，满足 \(v\cdot\nabla p=0\)，
压力在圆周处有严格极小值。选非零
\(\omega\in C_c^\infty((\epsilon,2\epsilon))\)，可设置
\[
 U=\omega(p)v,\qquad
 P=-\int_p^{2\epsilon}\omega(s)^2\,ds,\qquad
 (U\cdot\nabla)U=-\nabla P,\quad \operatorname{div}U=0.
\tag{BM.1}
\]
局部定义域外边界附近 \(p>2\epsilon\)，故 \(U=P=0\)；
圆周附近 \(p<\epsilon\)，故 \(U=0\)、\(P\) 为常数。
于是全局延拓给 \(U,P\in C_c^\infty(\mathbb R^3)\)，\(U\ne0\)。
压力支撑不必等于速度支撑；不能把圆周附近的常数压力删掉。
此局部化步骤已按原文核对；解析 ODE 的外部存在性依赖未重新证明。

令 \(\mathcal T_{ij}\) 如 BL.9。因为 \(U_iU_j\in L^2\)，
Fourier 乘子界给 \(Q=\mathcal T_{ij}(U_iU_j)\in L^2\)，而
\[
 -\Delta P=\partial_i\partial_j(U_iU_j)=-\Delta Q,\qquad
 P-Q\in L^2(\mathbb R^3)\quad\Longrightarrow\quad P=Q.
\tag{BM.2}
\]
最后一步是 \(L^2\) 调和分布的 Fourier 变换只能支撑在零点，
而 \(L^2\) 函数不能有仅支撑在单点的非零部分。
因此规范 Riesz 压力不能排除此例。

令 \(w(y,\tau)=U(y)\)、\(\pi(y,\tau)=P(y)\)，\(\tau<0\)，便有
\[
 \sup_{\tau<0}\|w(\tau)\|_2<\infty,\qquad
 \int_{Q_{R,S}}|\nabla w|^2=S\int_{B_R}|\nabla U|^2<\infty.
\tag{BM.3}
\]
所有固定柱体上的 \(L^{10/3}\)、光滑性、局部能量等式都满足。
平移后 \(B_1\) 可含非零速度，从而
\(\int_{Q_{1,1}}|w|^3>0\)。若须满足某个指定 \(E>0\)，可将
\(U,P\) 同时改成 \(aU,a^2P\)，选充分小的 \(a>0\)；
这里正下界随该例确定，不声称任意预先指定的 \(E,\varepsilon_*\)
组合均可同时实现。

所以“BL 得到的这些宽 Euler 性质蕴含 \(w=0\)”是错误的。
连全空间能量守恒也不能排除定常例。反例不是 NS 解序列，
没有证明它能由 BL 的同一固定初值、首次候选奇点缩放产生。

## 2. 固定原解的一个必要条件：终端能量原子

下面不导入 Gavrilov 的构造。仍用 BL 的同一光滑周期 NS 原解，
只在 \(0<t<T_*\) 推导。对每个固定光滑周期 \(\phi\)，局部能量等式给
\[
 \frac d{dt}\int\frac{|u|^2}{2}\phi
 =\int\frac{|u|^2}{2}\Delta\phi
   +\int\left(\frac{|u|^2}{2}+p\right)u\cdot\nabla\phi
   -\int|\nabla u|^2\phi .
\tag{BM.4}
\]
右端绝对可积到 \(T_*\)：能量给 \(u\in L^{10/3}_{t,x}\)，
进而在有限时空域 \(u\in L^3\)；规范周期压力属于
\(L^{3/2}_{t,x}\)，故 \(pu\in L^1\)，且总耗散有限。
周期有限指数压力估计可由固定胞的 BL.7 型局部分解、
有限空间覆盖与 Euclidean CZ 得到，不需要扩张胞的一致假设。

因此 \(\int|u(t)|^2\phi\) 在 \(t\uparrow T_*\) 有唯一极限。
正性、总质量界与光滑函数在连续函数中的一致稠密性，定义一个
有限非负 Radon 测度
\[
 |u(t)|^2\,dx\ \stackrel{*}{\rightharpoonup}\ \mu_*
 \quad(t\uparrow T_*),\qquad \mu_*(\mathbb T^3)\le E.
\tag{BM.5}
\]
这里没有断言 \(\mu_*=|u(T_*)|^2dx\)，也未假设在终点强 \(L^2\)
连续。对所有 \(t\uparrow T_*\) 的测度极限与其无原子性是两回事。

令 \(V\) 是 BL.5 在 \(Q_{1,1}\) 的一个一致 \(L^{10/3}\) 积分上界。
BL.3 的下界使 \(V>0\)。以 BL.16 的同一插值计算，有
\[
 \int_{Q_{1,1}}|w_k|^2
 \ge \frac{\big(\int_{Q_{1,1}}|w_k|^3\big)^4}
           {\big(\int_{Q_{1,1}}|w_k|^{10/3}\big)^3}
 \ge c_*:=\varepsilon_*^4/V^3>0 .
\tag{BM.6}
\]
区间长度为一，故可选 \(\tau_k\in(-1,0)\)，使
\(\int_{B_1}|w_k(\tau_k)|^2\ge c_*/2\)。
在原变量中 \(t_k=T_*+\lambda_k^{5/2}\tau_k\uparrow T_*\)，且
\[
 \int_{B_{\lambda_k}(x_k)}|u(t_k)|^2\ge c_*/2.
\tag{BM.7}
\]
紧致周期胞上再选 \(x_k\to x_*\)。对每个小的固定 \(r>0\)，
充分大时 \(B_{\lambda_k}(x_k)\subset B_r(x_*)\)。
选连续 \(\phi_r=1\) 于 \(B_r(x_*)\)，支撑于 \(B_{2r}(x_*)\)，
\(0\le\phi_r\le1\)。由 BM.5、BM.7，
\(\int\phi_r\,d\mu_*\ge c_*/2\)；再令 \(r\downarrow0\)，得到
\[
 \boxed{\ \mu_*(\{x_*\})\ge c_*/2>0.\ }
\tag{BM.8}
\]
这是真实固定原解来源下的条件必要性，不是 NS 能量原子的存在性。
若另有适用的终端无原子定理，就能排除同时满足 BL.3 的序列；
但无原子性本身没有由本稿证明。即使排除这一种序列，也须证明
任意候选奇点都能产生 BL.3，才可能得到一般正则出口。

## 3. 后续限制

我不再安排证明宽 Euler 类全零。随后完成的有界无原子文献核对及
强端点周期重算见 BN；所查结果仍保留额外可积性或 Type I 输入，
没有得到当前任意原解的自动无原子结论。这不是穷尽全部文献的否定。
额外输入不能重新命名成已付能量信息，也不能跳过 BL.3 对任意
候选奇点的生成缺口。下一项限制以本小节报告和 BN 末节为准。

本稿没有全局正则性、新颖性或 Clay 结论，没有数值仿真或 DGX。
