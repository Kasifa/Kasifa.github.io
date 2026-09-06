# 伴随的弱零迹：前向初端能量与频率通量

2026-09-06。**CONDITIONAL / ENDPOINT AUDIT / NON-AUTHOR REVIEW PASS / G OPEN / NOT CLAY。**

我先确定唯一性问题的时间方向和解类，再比较外部定理。
下述推导始终以 BP 已构造的同一个共同伴随为条件。
它不排除该伴随，也不证明正原子存在；不宣称新颖性。

## 1. 反时以后，零迹位于前向方程的初端

沿用 BP 的固定无外力周期 NS 原解 \(u\)、正终端原子 \(m>0\)
与共同伴随 \(A\)。令 \(L=T-t_b\)，对 \(0<\rho\le L\) 置
\[
 w(\rho)=A(T-\rho),\qquad b(\rho)=-u(T-\rho),\qquad w(0)=0.
 \tag{BS.1}
\]
\(w(0)\) 仅表示 BP.21 的弱 \(L^2\) 迹。反时和漂移的负号都不能漏：
\[
 w_\rho+P\operatorname{div}(w\otimes b)=\nu\Delta w,\quad
 \operatorname{div}w=\operatorname{div}b=0,\qquad
 b_\rho+P[(b\cdot\nabla)b]=-\nu\Delta b .
 \tag{BS.2}
\]
这里 \((w\otimes b)_{ij}=w_i b_j\)，故其散度是 \((b\cdot\nabla)w\)。
第二条方程提醒：\(b\) 不是任意给定漂移，而是同一个 NS 历史的反时场；
它在 \(\rho\) 方向的黏性符号为负。本文不把它另称正黏性 NS 解。
\(P\) 为周期 Leray 投影，非局部压力并没有被删除。

BP.22、BP.25、BP.27 给所有 \(0<\rho\le L\)
\[
 \|w(\rho)\|_2^2+2\nu\int_0^\rho\|\nabla w\|_2^2=1,\qquad
 w(\rho)\rightharpoonup0,\quad \|w(\rho)\|_2^2\longrightarrow1
       \quad(\rho\downarrow0).
 \tag{BS.3}
\]
因此这里是前向耗散方程的弱零初态和正的初端能量右极限。
它不满足从 \(w(0)=0\) 出发的能量不等式
\[
 \|w(\rho)\|_2^2+2\nu\int_0^\rho\|\nabla w\|_2^2
 \le\|w(0)\|_2^2=0.
 \tag{BS.4}
\]
这没有违反 BP 在任意严格正时间区间的能量等式。
若某个唯一性定理把 BS.4 或强零初始迹放在解定义里，
那就尚未证明当前 \(w\) 属于该解类。

## 2. 分布初值合法，但时间导数的强度不够直接测试自己

\(b,w\in L^\infty(0,L;L^2)\cap L^2(0,L;H^1)\)，
\(w\) 零均值。周期 Sobolev 和插值给
\[
 \|w\|_{L^4_\rho L^3_x}
 \le C\|w\|_{L^\infty_\rho L^2_x}^{1/2}
         \|\nabla w\|_{L^2_{\rho,x}}^{1/2},\quad
 b\in L^2_\rho L^6_x,\quad
 w\otimes b\in L^{4/3}_\rho L^2_x.
 \tag{BS.5}
\]
\(b\) 的 \(L^6\) 使用非齐次 \(H^1\)，保留其均值。
于是
\[
 w_\rho\in L^{4/3}(0,L;H^{-1}_\sigma),\qquad
 w\in C_w([0,L];L^2_\sigma).
 \tag{BS.6}
\]
这里 \(H^{-1}_\sigma\) 是 \(H^1_\sigma\) 的对偶。
弱连续也可直接从 BP 得到。对时间依赖的光滑无散测试，
先在 \((\epsilon,L)\) 积分，再令 \(\epsilon\downarrow0\)：
\(w(\epsilon)\rightharpoonup0\)，张量和梯度的积分绝对连续。
因此 BS.2 确实延伸为具有零初始分布迹的弱方程，没有额外向量
Dirac 源出现在方程本身。

但已付时间指数是
\[
 \frac12+\frac1{4/3}=\frac54>1.
 \tag{BS.7}
\]
\(L^2H^1\) 与 \(L^{4/3}H^{-1}\) 不提供用于能量配对的对偶时间指数。
这不证明该导数不可能更好；只说明 BS.5 这条基本能量估计不足。
旧 R0.71S 已登记相同的 Lions--Magenes 输入边界，
本节为实际 \(b,w\) 重新计算，而非新发现这一泛函分析事实。

## 3. 有限模态揭示精确的端点成本

取自伴、幂等的周期 Fourier 正交投影
\(J_N=1_{\{|k|\le N\}}\)，作用于全部向量分量，保留常数模态；
它与 \(P,\nabla,\Delta\) 交换。记
\[
 w_N=J_Nw,\quad e_N=\tfrac12\|w_N\|_2^2,\quad
 d_N=\|\nabla w_N\|_2^2,\quad
 \Pi_N(\rho)=\int_\Omega w_i b_j\,\partial_j(w_N)_i .
 \tag{BS.8}
\]
每个固定 \(N\) 的系数是绝对连续函数且 \(w_N(0)=0\)。
由有限模态方程和无散测试，压力配对严格为零，得到
\[
 e_N' +\nu d_N=\Pi_N,\qquad
 \int_0^\delta\Pi_N=e_N(\delta)+\nu\int_0^\delta d_N
 \quad(0<\delta\le L).
 \tag{BS.9}
\]
这是对已投影方程的合法测试，不是直接把 \(w\) 代入原弱式。

\(\nabla w_N\to\nabla w\) 强于全时间 \(L^2\)；
每个固定正 \(\delta\) 的 Fourier 范数收敛。
先固定 \(\delta\)，再令 \(N\to\infty\)，BS.3 给
\[
 \boxed{\quad \lim_{N\to\infty}\int_0^\delta\Pi_N(\rho)\,d\rho
       =\tfrac12 \quad\text{每个固定 }0<\delta\le L.\quad}
 \tag{BS.10}
\]
因此对任意 \(0<a<c\le L\)，
\(\lim_N\int_a^c\Pi_N=0\)。

几乎每个正 \(\rho\) 上，\(b,w\in H^1\)；
\(b\in L^6,w\in L^3,\nabla w_N\to\nabla w\) 于 \(L^2\)，所以
\[
 \Pi_N(\rho)\longrightarrow
 \int_\Omega w_i b_j\partial_j w_i=0\quad\text{a.e. }\rho>0.
 \tag{BS.11}
\]
最后的零由光滑逼近 \(w\) 于 \(H^1\) 和 \(\operatorname{div}b=0\) 得到；
不在时间上对未经估计的三重积直接用支配收敛。

更精确地，对任意 \(\eta\in C^1([0,L])\)，将 BS.9 乘 \(\eta\)
并分部积分。\(e_N\to e=\|w\|_2^2/2\) 于每点正时间且有界，
\(d_N\to d=\|\nabla w\|_2^2\) 于 \(L^1\)，而
\(e(\rho)=1/2-\nu\int_0^\rho d\) 在初端作右连续延拓，令 \(e(0+)=1/2\)。
因此
\[
 \lim_{N\to\infty}\int_0^L\eta(\rho)\Pi_N(\rho)\,d\rho
       =\tfrac12\eta(0).
 \tag{BS.12}
\]
极限泛函本身由 Radon 测度 \(\delta_0/2\) 表示。
这里证明的是 \(C^1\)（因而光滑）测试意义的边界分布收敛；
没有证明 \(\Pi_N\,d\rho\) 的总变差一致有界或它在测度空间的弱星收敛，
也没有将这个边界泛函识别为 suitable 局部能量缺陷测度。
特别不能与旧物理伴随稿 B.5 的那个缺陷测度混同。

BS.10--11 还证明：对每个 \(\delta>0\)，
\[
 \{\Pi_N\}_N\ \text{不在 }L^1(0,\delta)\text{ 一致可积}.
 \tag{BS.13}
\]
否则有限测度区间的 Vitali 收敛给 \(L^1\) 极限零，与 BS.10 矛盾。
每个正时间的输运斜对称性，不足以消除初端的极限成本。

固定 \(N\) 时，Bernstein 和两个 \(L^\infty_\rho L^2_x\) 界给
\[
 |\Pi_N(\rho)|\le C E_* N^{5/2},\qquad
 \lim_{\delta\downarrow0}\int_0^\delta\Pi_N=0,\qquad
 \lim_{\delta\downarrow0}\lim_{N\to\infty}\int_0^\delta\Pi_N=\tfrac12,\quad
 \lim_{N\to\infty}\lim_{\delta\downarrow0}\int_0^\delta\Pi_N=0.
 \tag{BS.14}
\]
\(N\ge1\)，常数依赖固定环面。
这只展示两个极限不能交换；不声称 \(N^{5/2}\) 最优或存在 NS 实例。

## 4. 一个明确但未支付的强迹接口

若对某个 \(\delta>0\) 额外有
\[
 P\operatorname{div}(w\otimes b)\in L^2(0,\delta;H^{-1}_\sigma),
 \quad\text{充分条件为 }w\otimes b\in L^2((0,\delta)\times\Omega),
 \tag{BS.15}
\]
则 BS.2 和已知 \(\nabla w\in L^2\) 给 \(w_\rho\in L^2H^{-1}_\sigma\)。
下面直接展开周期能量迹接口，不声称重读全部 Lions--Magenes 原著。

每个有限 \(N\) 满足
\[
 \|w_N(t)\|_2^2-\|w_N(s)\|_2^2
 =2\int_s^t\langle w_\rho,w_N\rangle,\qquad 0\le s\le t\le\delta.
 \tag{BS.16}
\]
因为 \(w_N\to w\) 于 \(L^2H^1\)，额外 \(L^2H^{-1}\) 界使右侧
在所有端点上一致收敛。取 \(s=0\)，左侧的 \(w_N(0)\) 全为零；
对每个正 \(t\) 用 Fourier 范数收敛，就得
\(\|w(t)\|_2^2=2\int_0^t\langle w_\rho,w\rangle\)。
右端在 \(t\downarrow0\) 趋零，与 BS.3 矛盾。
结合所有时刻的弱连续，实际还给闭区间强 \(L^2\) 连续。

所以在当前原子条件下，对每个 \(\delta>0\)
\[
 \|P\operatorname{div}(w\otimes b)\|_{L^2(0,\delta;H^{-1}_\sigma)}
 =\infty,\quad
 \|w_\rho\|_{L^2(0,\delta;H^{-1}_\sigma)}=\infty,\quad
 \|w\otimes b\|_{L^2((0,\delta)\times\Omega)}=\infty.
 \tag{BS.17}
\]
这些是该具体伴随与原解配对的必要障碍，不是新的原解范数上界。
也没有证明“有限张量范数”等价于原解正则性，
或把一个充分强迹条件称作所有强迹的必要条件。

作为适用性比较，若额外给漂移
\(b\in L^p_\rho L^q_x\)、\(q>3\)、\(2/p+3/q\le1\)，则
\[
 \|w\|_{L^{2q/3}_\rho L^{2q/(q-2)}_x}<\infty,\qquad
 \|w\otimes b\|_{L^2_{\rho,x}}<\infty
 \quad(q=\infty\text{ 时用 }w\in L^\infty_\rho L^2_x).
 \tag{BS.18}
\]
这由能量插值和时间 Hölder直接得到，故此类漂移条件可以排除 \(w\)。
但对 \(b=-u(T-\rho)\)，它就是原解的额外 Serrin 条件；
q=6 要时间 L4，基本能量只有 L2，不能据此闭合。
不另行证明 q=3 端点，也不沿相邻范数开始无界扫描。

## 5. 本节的实际边界

BS.1--18 校准了终端唯一性的方向与缺口：当前对象是
正时间能量等式成立、初端弱零但能量右极限非零的压力耦合向量解。
直接排除它需要真正控制初端通量或建立适用于该弱迹解类的定理，
不能先把结论包含在解类定义中。

频率通量的边界分布由有限模态的恒等式直接得到；
并未构造不适定反例，未证明真 NS 可以生成这个伴随，
也未从基本能量排除它。
既有正原子条件、G、一般正则性仍开放。
原始文献适用性比较另记，外部定理只按实际核读范围使用。
