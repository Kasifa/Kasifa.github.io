# 短窗口的局部耗散分支与压力余项

2026-09-06。接续 U、V 工作稿。**本地解析结论 / G OPEN / NOT CLAY**。
常数只依赖固定 cutoff、核和三维函数空间不等式；
不宣称新颖性，不把条件分支称为全局正则性进展。

## 1. 单个提升上的三个加厚域

固定原路径 X_R、好终点 tau 和壳 k。
全部空间积分先在同一个周期场的欧氏提升上进行，
\(f(t,y)=u(t,y+X_R(t))\)，压力提升记为 pi。
原 cutoff 为 \(\psi_k^R\)，壳为
\(A_k(R)=\{2^kR\le|y|<2^{k+1}R\}\)。
记

\[
 \Omega_k^d=\{y:\operatorname{dist}(y,A_k(R))<dR\}.
\tag{W.1}
\]

原梯度的支撑包含于 \(\Omega_k^{1/8}\) 的闭包。
选 \(0\le\zeta_k,\chi_k\le1\)，使

\[
 \zeta_k=1\text{ 于 }\Omega_k^{1/4},\quad
 \operatorname{supp}\zeta_k\subset\Omega_k^{3/8},\qquad
 \chi_k=1\text{ 于 }\Omega_k^{3/8},\quad
 \operatorname{supp}\chi_k\subset\Omega_k^{1/2},\quad
 |\nabla\chi_k|\le C/R .
\tag{W.2}
\]

可用径向过渡在内外边界各构造一个固定厚度 cutoff。
因为最内半径至少为 \(2R-R/2>0\)，不存在径向函数在原点的光滑问题。
每个域有界，但其体积随 k 增长。以下不把其体积当成 R³。
这些域和函数都不重新周期化；仅原场 f、pi 是周期场的提升。

## 2. 对整个壳作压力分解

在几乎处处的 t，令

\[
 p_k^{\rm loc}=\mathcal R_i\mathcal R_j(\zeta_k f_i f_j),
 \qquad h_k=\pi-p_k^{\rm loc}.
\tag{W.3}
\]

这里是全空间 Riesz 变换作用于紧支撑源，不是把周期场本身
当作全空间 L^p 函数。原 NS 压力源等式与 zeta=1 给
\(-\Delta h_k=0\) 于 \(\Omega_k^{1/4}\)。
h_k 一般不周期；这不妨碍它与紧支撑的 grad psi 配对。
它保留了核心、外部、截断过渡及周期效应所产生的调和余项，
不能简单称为“已删除的远场压力”。

Calderon--Zygmund 与空间 Holder 给

\[
 \|p_k^{\rm loc}\|_{L^{3/2}(\mathbb R^3)}
 \le C\|f\|_{L^3(\Omega_k^{3/8})}^2,\qquad
 \left|\int p_k^{\rm loc} f\cdot\nabla\psi_k^R\right|
 \le \frac C R\int_{\Omega_k^{3/8}}|f|^3 .
\tag{W.4}
\]

不使用多个球的独立压力 gauge 拼接；这样没有隐藏的分片梯度项。
整个壳的时间常数 c_k 仍可消去：
\(\int c_k(t)f\cdot\nabla\psi_k^R=0\)，因为 f 无散且 psi 紧支撑。
这个恒等式不消去 h_k 的非恒定部分。

原通量导数经精确 unfolding 后写为

\[
\begin{split}
 F'_k(t)&=L_k(t)+S_k(t),\\
 L_k(t)&=\frac{\gamma_k\eta_R}{R}
       \int [\tfrac12|f|^2f+p_k^{\rm loc}f]\cdot\nabla\psi_k^R,\\
 S_k(t)&=\frac{\gamma_k\eta_R}{R}
       \int [h_k f-\tfrac12|f|^2a_R]\cdot\nabla\psi_k^R .
\end{split}
\tag{W.5}
\]

中心速度 \(a_R(t)=S_Ru(t,X_R(t))\) 仍是一个空间常向量。
不把它换成 b_R(t,y)，也不通过改压力把它消去。
可在 S 的 h 项中减去任意可积时间 gauge。

由于 \((x+y)_+\le |x|+y_+\)，对任意窗口 J 有

\[
 \int_J(F'_k)_+
 \le C\gamma_kR^{-2}\int_J\int_{\Omega_k^{3/8}}|f|^3
       +\mathcal B_k(J),\qquad
 \mathcal B_k(J)=\int_J[S_k(t)]_+dt .
\tag{W.6}
\]

S 的完整空间积分后才取正部；压力余项与中心漂移之间的相消仍保留。
若先分别取绝对值，只会得到较大的上界，不能反向声称相消。
所有固定 k、R 的项在能量类和 suitable 压力可积性下均有定义。

## 3. 局部 Sobolev 的准确代价

令 \(|J|=\delta>0\)，

\[
 M_k=\operatorname*{ess\,sup}_{t\in J}
             \|f(t)\|_{L^2(\Omega_k^{1/2})},\qquad
 \mathscr D_k(J)=\int_J\int_{\Omega_k^{1/2}}|\nabla f|^2 .
\tag{W.7}
\]

这是未加权的局部速度范数和黏性耗散，
不是原端点 \(E_k(\tau)\) 或时钟内的总耗散 \(D_k(\tau)\)。
对紧支撑的 \(g=\chi_kf\)，齐次全空间 Sobolev 给
\(\|g\|_3^3\le C\|g\|_2^{3/2}\|\nabla g\|_2^{3/2}\)。
导数落在 chi 上产生 \(R^{-2}|f|^2\)，随后时间 Holder 给

\[
 \int_J\int_{\Omega_k^{3/8}}|f|^3
 \le C M_k^{3/2}\delta^{1/4}
       \bigl(\mathscr D_k(J)+\delta R^{-2}M_k^2\bigr)^{3/4}.
\tag{W.8}
\]

常数与壳的半径 \(2^kR\) 无关；大壳的质量在 M、D 中保留。
没有把周期复制之和当作全空间有限能量函数，
没有扣除环面均值或假定局部 Poincare 条件。

现在取 U 第三支的阈值窗口
\(J_k=(\tau-\delta_k^F,\tau)\)，缩写
\(E=E_k(\tau)>0,\delta=\delta_k^F\)。
定义保证 \(\int_{J_k}(F'_k)_+=E/4\)。
于是以下两支至少一支成立：

\[
 \boxed{\quad\mathcal B_k(J_k)\ge E/8\quad}
\tag{W.9}
\]

或者

\[
 \boxed{\quad
 \mathscr D_k(J_k)\ge
 c\left(\frac{ER^2}{\gamma_k}\right)^{4/3}
       M_k^{-2}\delta^{-1/3}
       -\delta R^{-2}M_k^2 .
 \quad}
\tag{W.10}
\]

证明：若 W.9 不成立，W.6 迫使局部三次质量至少为
\(cER^2/\gamma_k\)；代入 W.8 并取 4/3 次幂，得到 W.10。
该分支 M_k=0 不可能，因为它会使三次质量为零。
末项来自 cutoff，不能未经证明删除或吸收；右侧可能非正。
要得到正的耗散下界，还须主项支配末项。

这是适用于原真实 NS 通量的条件分支，不是假定 pressure=0 后的证明。
若 W.9 发生，仍需支付调和压力/中心漂移的联合正工作。
若 W.10 发生，也未得到这些耗散在全壳上的目标预算。

## 4. 重叠可控制，但权重与时间不能偷换

设 \(W_{2R}(y)=\sum_{\ell\ge1}\gamma_\ell1_{A_\ell(2R)}(y)\)。
固定厚度的加厚壳满足点态几何界

\[
 \sum_{k\ge1}\gamma_k1_{\Omega_k^{1/2}}
 \le C1_{B_{8R}}+CW_{2R}.
\tag{W.11}
\]

证明：全提升中一个点至多落入两个相邻的加厚壳。
当 \(|y|\ge8R\)，令 \(y\in A_m(R)=A_{m-1}(2R)\)，m>=3。
能覆盖该点的壳仅可能是 m-1、m、m+1；
每个相关权重均不超过 gamma_(m-1)，同点至多两个。
核心 B8R 用有限重叠直接控制。
边界集合按几乎处处约定处理，不影响积分。

关键是外扩进入 \(A_{k+1}(R)=A_k(2R)\) 时，
应使用 W_(2R) 的 gamma_k。原 W_R 在那里只有 gamma_(k+1)，而

\[
 \frac{\gamma_k}{\gamma_{k+1}}
 =\exp(3\cdot4^{k-1}/32)\longrightarrow\infty .
\tag{W.12}
\]

因此不能把有限重叠误写成同尺度原权重的统一支配。
对 U 第三支 \(k\in\mathcal I_\tau\)，即使 J_k 不同，
仍由非负性和 \(J_k\subset I_{2R}\) 得

\[
\begin{split}
 \frac1R\sum_{k\in\mathcal I_\tau}\gamma_k\mathscr D_k(J_k)
 \le{}&\frac C R\int_{I_{2R}}\int_{B_{8R}}|\nabla f|^2\\
 &+\frac C R\int_{I_{2R}}\int_{\mathbb R^3}
                                      W_{2R}|\nabla f|^2 .
\end{split}
\tag{W.13}
\]

第一项可从同一路径的原 B8R 能量账本引用一次。
第二项是需要另行保留的扩大半径、完整时间段耗散：

\[
 \mathscr D_{\rm pad}^{M,R}
 :=R^{-1}\int_{I_{2R}}\int_{\mathbb R^3}W_{2R}|\nabla f|^2 .
\tag{W.14}
\]

原 P_R^M 的外部部分是速度三次、压力及调和尾项，
不包含 W.14；原半径 R 的 exterior dissipation
又使用 I_R 和 W_R。二者均不能仅凭定义支付 W.14。
这不排除未来由 NS 方程证明另一个上界；
只是本轮没有这样的定理。
外部梯度和内核梯度必须分别记账，不把同一份耗散当作两个小量。

## 5. 路线判断

本轮闭合的是一个明确局部化计算：
局部压力可以并入加厚壳的三次项，留下确切的有符号余项 S；
短窗口给 W.9/W.10 分支；扩大域有正确的有限重叠和权重账本。

但这没有闭合 U.9、V.11 或原 R.216--R.217。
若继续把 S 绝对值化，并把扩大耗散用全局能量粗估，
就再次得到未受控的尺度支付，不能据此把 G 标成已证。
本轮没有产生真 NS 反例，也没有排除一般局部化方法。

我不再仅优化这组常数。下一步先复评这一充分路线的强度：
原 G 只针对指定可能首次奇点，原 R 则要求任意好终点的全壳统一抽取。
应明确哪些任意终点要求是当前方法附加的，
再检查是否能直接在首次奇点条件下使用真实 NS 的时间持留信息。
不引入尚未证明的 Type-I 或临界范数界，不把缩小辅助命题的量词
误称为已经解决原目标。

本节解析证据不需要仿真或科学图表。配套来源与独立审查另存。
