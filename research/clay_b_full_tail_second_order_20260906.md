# 固定后继解的二阶成本与尚未支付的算子预算

2026-09-06。**LITERATURE RECONSTRUCTION / CONDITIONAL / NON-AUTHOR REVIEW PASS / G OPEN / NOT CLAY。**

BP 完整重构共同伴随与最终离散全尾结构。本稿继续核查
Huang [2608.04138v1](https://arxiv.org/abs/2608.04138v1) 的 §7、
Corollary 2.6；不导入 Appendix A 的端点测试空间结论。

## 1. 固定一个后继解，而不是逐窗口换初值

沿 BP 的同一原解 \(u\)、同一最终链，记
\[
 \varepsilon_J=\sup_{k>j\ge J}
   \|U(\tau_k,\tau_j)q_j-q_k\|_2\longrightarrow0,\qquad
 H(t)=U(t,\tau_J)q_J,\quad t\ge\tau_J .
 \tag{BQ.1}
\]
取固定 \(J\) 足够晚使 \(\varepsilon_J\le1/8\)，后面始终不改 \(H\)。
\(H\) 零均值、\(\|H(t)\|_2\le1\)，并有有限的一阶总耗散。
对 \(j\ge J+1\)，设互不重叠（除端点）的区间 \(I_j=[\tau_j,\tau_{j+1}]\)，
\[
 \ell_j=|I_j|,\quad d_j=\int_{I_j}\|\nabla u\|_2^2,\quad
 a_j=\int_{I_j}\|\nabla H\|_2^2,\quad
 K_j=\int_{I_j}\|\Delta H\|_2^2,\quad
 \widetilde d_j=d_j+E_*^2\ell_j .
 \tag{BQ.2}
\]
\(E_*\) 沿用 BP 的 \(L^2\) 范数上界。能量给
\(\sum d_j,\sum a_j,\sum\ell_j<\infty\)，所以三者及
\(\widetilde d_j\) 都趋零。这里可以对互异区间相加；
不能把 BO 的嵌套终端窗口当成这些区间。

每个 \(I_j\) 与初时 \(\tau_J\) 正距离，并紧含于终点前。
线性方程正延迟平滑保证其中 \(H\) 光滑、\(K_j<\infty\)；
没有先假设整个尾部二阶积分有限。

## 2. 正交节点迫使每个单元的二阶积分变大

由 BQ.1 及 \(q_j\perp q_{j+1}\)，
\[
 \|H(\tau_{j+1})-H(\tau_j)\|_2
 \ge\sqrt2-2\varepsilon_J\ge c_0:=\sqrt2-\tfrac14>0 .
 \tag{BQ.3}
\]
另一方面 \(H_t=-P[(u\cdot\nabla)H]+\nu\Delta H\)。
非齐次周期 Sobolev 用于 \(u\)，而 \(\nabla H\) 自动均值零：
\[
 \|u\|_6\le C(\|\nabla u\|_2+E_*),\qquad
 \|\nabla H\|_3\le C\|\nabla H\|_2^{1/2}\|\Delta H\|_2^{1/2}.
 \tag{BQ.4}
\]
对第二式先插值 \(L^2,L^6\)，再对各导数用均值零 Sobolev；
Fourier 恒等式 \(\|\nabla^2H\|_2=\|\Delta H\|_2\) 处理 Hessian。
积分方程及 \(P\) 的 \(L^2\) 收缩性、时间 Hölder \(2,4,4\) 给
\[
 c_0\le C\widetilde d_j^{1/2}a_j^{1/4}K_j^{1/4}
                    +\nu\ell_j^{1/2}K_j^{1/2}.
 \tag{BQ.5}
\]
两个右项至少一个大于等于 \(c_0/2\)，因此
\[
 K_j\ge
 \min\left\{\left(\frac{c_0}{2C}\right)^4
                 \widetilde d_j^{-2}a_j^{-1},
             \frac{c_0^2}{4\nu^2}\ell_j^{-1}\right\}
 \longrightarrow+\infty .
 \tag{BQ.6}
\]
若第一项的分母为零，定义该项为 \(+\infty\)；此时 BQ.5 的第一项
为零，第二项必须支付。由于 \(\ell_j\to0\) 及
\(\widetilde d_j,a_j\to0\)，两个阈值都趋向无穷。
这里不是把零量乘无穷作代数运算。

因此同一个固定 \(H\) 满足
\[
 \int_{\tau_{J+1}}^T\|\Delta H(t)\|_2^2dt
      =\sum_{j\ge J+1}K_j=+\infty .
 \tag{BQ.7}
\]
这是一阶耗散有限、二阶作用无限的条件结论，不是与基本能量的矛盾。

## 3. 涡量平方生产的正部与原解驱动的算子出口

令
\[
 \Gamma(t)=\|\nabla H(t)\|_2^2,\quad K(t)=\|\Delta H(t)\|_2^2,\quad
 P_H(t)=\langle\Delta H,P[(u\cdot\nabla)H]\rangle
       =-\int\partial_\ell u_k\,\partial_kH_i\,\partial_\ell H_i .
 \tag{BQ.8}
\]
这不是 NS 压力 \(p\)；\(P_H\) 是后继解的 enstrophy 生产。
在严格终点前区间上
\[
 \tfrac12\Gamma'(t)+\nu K(t)=P_H(t),\qquad
 \int_{\tau_{J+1}}^{\tau_{N+1}}P_H
   =\tfrac12[\Gamma(\tau_{N+1})-\Gamma(\tau_{J+1})]
       +\nu\sum_{j=J+1}^{N}K_j .
 \tag{BQ.9}
\]
末端 \(\Gamma\ge0\)，初端有限，故
\(\int_{\tau_{J+1}}^T(P_H)_+=+\infty\)。
没有断言 \(P_H(t)\) 逐时非负，也没有用有符号无穷积分作未定义的抵消。

对任意 \(t_b\le s<r<T\)，定义原解决定的延迟算子预算
\[
 \mathcal R_u(s,r)
 =\sup_{\substack{f\in L^2_\sigma(\Omega)\\\|f\|_2=1}}
      \int_r^T\|\Delta U(t,s)f\|_2^2dt\in[0,\infty].
 \tag{BQ.10}
\]
其定义不使用原子、packet 或适配权重。BQ.7 给
\(\mathcal R_u(\tau_J,\tau_{J+1})=\infty\)；
这里一个具体单位初态 \(q_J\) 已使积分发散，强于仅知算子范数无界。
反之，若某 \(t_c<T\) 后对每一对 \(t_c\le s<r<T\) 都有
\(\mathcal R_u(s,r)<\infty\)，则无原子。
不要求所有时刻对共用一个常数。复述原文时应保留“对每一对”；
是否能加强成仅需某一对，须另作证明，不能由这里列出的离散根结论直接声称。
后续 BR 给出独立的加强推导，并审查整个预算与原解延拓的关系。
这是充分的无原子出口，不是已由能量支付的界，也不宣称必要性。

## 4. 为什么原文的 Serrin 例仍是附加条件

为核查 BQ.10 在原文所列条件下确实有限，另假设
\(u\in L^p(t_c,T;L^q)\)，\(3<q\le\infty\)，\(2/p+3/q\le1\)。
固定 \(s<r<T\)。初态仅有单位 \(L^2\) 时，紧的正延迟区间给
\[
 C_{\rm sm}:=\sup_{\|f\|_2=1}\|\nabla U(r,s)f\|_2^2
 \le \frac{C}{\nu(r-s)}
       \exp\left(\frac{C}{\nu}\int_s^r\|u\|_\infty^2dt\right)<\infty .
 \tag{BQ.11}
\]
推导是在 \((s,(s+r)/2)\) 用能量平均选出一个梯度受控时刻，
再对 \(\Gamma'+\nu K\le\nu^{-1}\|u\|_\infty^2\Gamma\) 积分。
所选时刻可依赖 \(f\)，最终常数不依赖 \(f\)；
指数只在固定的紧区间 \([s,r]\) 上使用光滑性。

置
\[
 \theta=\frac3q,\quad r_q=\frac{2q}{q-2},\quad
 p_q=\frac2{1-\theta},\quad \alpha_q=\frac{1+\theta}{1-\theta},\qquad
 |P_H|\le C\|u\|_q\Gamma^{(1-\theta)/2}K^{(1+\theta)/2}
 \le \tfrac\nu2K+C_q\nu^{-\alpha_q}\|u\|_q^{p_q}\Gamma .
 \tag{BQ.12}
\]
\(q=\infty\) 时取 \(\theta=0,r_q=2,p_q=2\)。
Young 指数是 \(2/(1+\theta)\) 和 \(2/(1-\theta)\)；
\(\theta<1\) 必须保留，不能取端点 \(q=3\)。

设 \(f_q=C_q\nu^{-\alpha_q}\|u\|_q^{p_q}\)。
时间条件给 \(p\ge p_q\)，有限时间域上 \(f_q\in L^1\)。
于是 \(\Gamma'+\nu K\le2f_q\Gamma\)，并一致于单位初态有
\[
 \sup_{r\le t<T}\Gamma(t)\le C_{\rm sm}e^{2\int_r^Tf_q}=:M<\infty,
 \qquad
 \nu\int_r^T K(t)dt\le C_{\rm sm}+2M\int_r^Tf_q<\infty .
 \tag{BQ.13}
\]
这是原文充分条件的直接验证，不是去掉 Serrin 输入。
在基本能量可得的 \(L^2_tL^6_x\) 水平，上式 \(q=6\) 需要时间四次方；
二次时间信息并未满足它。没有据此证明所有其他方法都失败。

## 5. 可供下一项使用的精确结论

BP 与本稿把“正原子”连接到一个固定原解驱动的、具有无限延迟二阶
作用的具体后继解。它比 BO 的一阶趋零成本提供不同的对象，但仍不矛盾。
这里不把预印本全部外部依赖或 Appendix A 记作已复核；
不声称新的正则性、原子排除、新颖性或 Clay 成果。

本节之后的 BR 已继续检查共同伴随与固定后继解的连续时间对偶，
以及全算子预算本身的逻辑强度。它是另一个实际推导，不包含在本节
对原文 §7 的复述里；当前下一项以合并报告和续接记录为准。
