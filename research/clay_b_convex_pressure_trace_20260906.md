# 有界凸测试可以成立：压力的可积性与幅度端点

2026-09-06。**DIRECT DERIVATION / CONDITIONAL ENDPOINT / NON-AUTHOR REVIEW PASS / G OPEN / NOT CLAY。**

上一节证明了频率截断的端点成本。
这一节检查有界凸测试时，我得到了一项已能由基本能量支付的输入：
压力梯度具有足够的时间可积性，固定凸测试并不需要先判为非法。
真正未付的部分是把固定测试推向二次能量时的统一控制。

## 1. 先不使用原子：能量类中的压力梯度

固定三维环面 \(\Omega\)、\(\nu>0\)、\(0<L<\infty\)。
这一部分只假设无散 \(b,w\in L^\infty(0,L;L^2)\cap L^2(0,L;H^1)\)，
\(w\in C_w([0,L];L^2_\sigma)\)，\(w(0)=0\) 为弱迹，且
\[
 w_\rho+P[(b\cdot\nabla)w]=\nu\Delta w .
 \tag{BT.1}
\]
原子、\(b\) 的 NS 来源或初始能量不等式均不是本部分的假设。
这不声称存在一个非零的此类解。

令 \(Q=I-P\)，压力取周期零均值。以分布重构压力后，
\[
 f=(b\cdot\nabla)w\in L^1_\rho L^{3/2}_x,\qquad
 \nabla\pi=-Qf,\qquad
 w_\rho+(b\cdot\nabla)w+\nabla\pi=\nu\Delta w ,
\]
\[
 \|\nabla\pi\|_{L^1(0,t;L^{3/2})}
 \le C\|b\|_{L^2(0,t;L^6)}\|\nabla w\|_{L^2((0,t)\times\Omega)} .
 \tag{BT.2}
\]
使用的是有限指数 \(3/2\) 的周期 Leray/CZ 界；
\(b\) 的 \(L^6\) 来自非齐次 \(H^1\)，不删除其均值。
零均值 Sobolev 还给 \(\pi\in L^1_\rho L^3_x\)。
定义已付的累积量
\[
 \kappa(t):=\int_0^t\|\nabla\pi(\rho)\|_{L^1_x}\,d\rho
 \le C_\Omega B(t)G(t)\longrightarrow0,\quad
 B(t)=\|b\|_{L^2(0,t;L^6)},\quad
 G(t)=\|\nabla w\|_{L^2((0,t)\times\Omega)} .
 \tag{BT.3}
\]
这个 \(L^1\) 时间控制不等于 BS.15 的 \(L^2H^{-1}\) 控制。
压力可积并不意味着它与无界 \(w\) 的乘积在时空中可积。

## 2. 固定幅度的凸函数

对每个固定 \(R>0\)，取
\[
 \beta_R(z)=R^2\big(\sqrt{1+|z|^2/R^2}-1\big),\qquad
 s_R(z)=\sqrt{1+|z|^2/R^2},
\]
\[
 D\beta_R(z)=z/s_R(z),\qquad
 D^2\beta_R(z)=s_R^{-1}I-R^{-2}s_R^{-3}z\otimes z .
 \tag{BT.4}
\]
Hessian 的径向特征值为 \(s_R^{-3}\)，切向为 \(s_R^{-1}\)。
因而
\[
 0\le\beta_R(z)\le\min(|z|^2/2,R|z|),\quad
 |D\beta_R(z)|\le\min(|z|,R),\quad
 0<D^2\beta_R(z)\le I,\quad \beta_R(0)=0 .
 \tag{BT.5}
\]
固定 \(R\) 的梯度和 Hessian 都有界；不要求这些函数有紧支撑。

令 \(S_\epsilon\) 为周期空间光滑卷积，\(w_\epsilon=S_\epsilon w\)，
\(\pi_\epsilon=S_\epsilon\pi\)。不先作时间卷积。
\[
 (w_\epsilon)_\rho+b\cdot\nabla w_\epsilon+\nabla\pi_\epsilon
 =\nu\Delta w_\epsilon+r_\epsilon,\qquad
 r_\epsilon=b\cdot\nabla S_\epsilon w-S_\epsilon(b\cdot\nabla w).
 \tag{BT.6}
\]
逐分量展开唯一的输运交换子：
\[
 r_\epsilon(x)=\int\varphi_\epsilon(y)
       [b(x)-b(x-y)]\cdot\nabla w(x-y)\,dy,\qquad
 \|r_\epsilon\|_{L^1_{\rho,x}}
 \le\int\varphi_\epsilon(y)
       \|b-b(\cdot,\cdot-y)\|_{L^2_{\rho,x}}
       \|\nabla w\|_{L^2_{\rho,x}}\,dy\longrightarrow0 .
 \tag{BT.7}
\]
收敛由 \(L^2\) 平移强连续和紧支撑近似恒等核得到。
这给出了 BCC Lemma 2.6 在当前分量上的直接证明；
不只凭“依测度收敛”就省略乘积极限的论证。

固定 \(\epsilon\) 的平滑方程使
\(w_\epsilon\in W^{1,1}(0,L;L^2)\)：
卷积后的 \(f,\nabla\pi\) 时间 \(L^1\)，黏性项也可积。
\(S_\epsilon\) 在周期 \(L^2\) 上紧，故弱连续初迹给
\(w_\epsilon(0)=S_\epsilon w(0)=0\) 的强初迹。
可合法从零时刻积分，对 \(D\beta_R(w_\epsilon)\) 测试。
输运项利用 \(\operatorname{div}b=0\) 消失；
这个非线性测试通常并非无散，压力不能消失。

记
\[
 E_R(t)=\int_\Omega\beta_R(w(t)),\quad
 \mathcal D_R(\rho)=\sum_{k=1}^3\int_\Omega
       D^2\beta_R(w)[\partial_k w,\partial_k w],\quad
 Q_R(\rho)=-\int_\Omega D\beta_R(w)\cdot\nabla\pi .
 \tag{BT.8}
\]
固定 \(R\)，令 \(\epsilon\downarrow0\)，获得所有 \(0\le s\le t\le L\)
的精确恒等式
\[
 E_R(t)+\nu\int_s^t\mathcal D_R
 =E_R(s)+\int_s^t Q_R,\qquad E_R(0)=0 .
 \tag{BT.9}
\]

各个极限的依据如下：

- 固定端点，空间卷积在 \(L^2\) 强收敛，\(\beta_R\) 是 Lipschitz，
  故端点积分收敛；不把弱初迹直接代入二次能量。
- 交换子误差由 \(R\|r_\epsilon\|_{L^1}\to0\) 消去。
- \(\nabla\pi_\epsilon\to\nabla\pi\) 于 \(L^1_{\rho,x}\)；
  \(D\beta_R(w_\epsilon)\) 一致有界并依测度收敛，
  对固定可积权重 \(|\nabla\pi|\) 取支配收敛，得到压力极限。
- \(\nabla w_\epsilon\to\nabla w\) 于 \(L^2\)；
  Hessian 连续且一致有界。先用强梯度收敛处理两个梯度的差，
  再对 \(|\nabla w|^2\) 支配收敛，得到耗散等式，而不只有 Fatou 不等式。
- 这些时空积分在整段 \(L^1\) 收敛，故对积分端点一致收敛；
  逐时弱连续代表的空间逼近处理所有端点。
  如用子列得到几乎处处收敛，所得极限唯一，不改变恒等式。

因此 \(E_R\) 绝对连续，\(\mathcal D_R,Q_R\in L^1(0,L)\)。
全过程先固定 \(R\)，没有把 \(R\to\infty\) 与 \(\epsilon\to0\) 交换。
更一般有界梯度及有界 Hessian 的平滑凸函数可同样处理；
本节不直接宣称仅 \(C^1\) 的任意凸函数具有精确 Hessian 等式。

## 3. 一项真正已付的弱迹升级

BT.8--9 与非负耗散给
\[
 |Q_R(\rho)|\le R\|\nabla\pi(\rho)\|_1,\qquad
 0\le E_R(t)\le R\kappa(t) .
 \tag{BT.10}
\]
先除以 \(R\)，再令 \(R\downarrow0\)：
\(\beta_R(z)/R=\sqrt{R^2+|z|^2}-R\uparrow|z|\)。
不需要控制这个极限的 Hessian，因为已经丢弃非负耗散。得到
\[
 \boxed{\ \|w(t)\|_1\le\kappa(t)\le C_\Omega B(t)G(t)\to0\ } .
 \tag{BT.11}
\]
再与统一 \(L^2\) 界插值，
\[
 \|w(t)\|_q\le
 \|w(t)\|_1^{\,2/q-1}\|w(t)\|_2^{\,2-2/q}\longrightarrow0,
 \qquad 1\le q<2 .
 \tag{BT.12}
\]
这一强初迹升级只用第 1 节假设，没有先用 BP 的原子集中。
\(q=2\) 不在结论内。这不是一个新的无条件 NS 唯一性定理；
也不宣称上述有源 Kato 型估计在文献中是新颖的。

## 4. 放回同一个原解的伴随

现在才令 \(w=A(T-\rho)\)、\(b=-u(T-\rho)\)，使用 BP/BS 的额外正原子。
\[
 \|w(t)\|_2^2+2\nu\int_0^t\|\nabla w\|_2^2=1,\qquad
 \|w(t)\|_2^2\to1\quad(t\downarrow0).
 \tag{BT.13}
\]
这里 \(t\) 是反时后的正时间，不是原解的原时间。
\(b\) 的负黏性方程和同一 NS 历史不变。
强 \(L^q,\ q<2\) 零迹完全允许 BT.13 的 \(L^2\) 集中；
它与 BP 的空间原子定位一致，但不能排除它。

固定任意 \(0<t\le L\)，再令 \(R\to\infty\)。
逐点 \(\beta_R(w)\to|w|^2/2\)、\(D^2\beta_R(w)\to I\)，
分别由 \(|w(t)|^2/2\) 与 \(|\nabla w|^2\) 支配。
BT.9 和 BT.13 给
\[
 \boxed{\ \lim_{R\to\infty}\int_0^tQ_R(\rho)\,d\rho=\frac12\ } .
 \tag{BT.14}
\]
压力在固定凸测试中没有消失，且必须承受这个精确幅度端点成本。

然而几乎每个正时间，\(w\in H^1\subset L^3\)、
\(\nabla\pi\in L^{3/2}\)，所以由空间支配收敛及无散性
\[
 Q_R(\rho)\longrightarrow-\int_\Omega w\cdot\nabla\pi=0
       \quad\text{a.e. }\rho>0 .
 \tag{BT.15}
\]
这里 \(\pi\in W^{1,3/2}\)，周期光滑逼近正当化空间的零配对。
没有在时间上支配未经控制的 \(|w||\nabla\pi|\)。

对任意 \(\eta\in C^1([0,L])\)，
由 \(E_R'+\nu\mathcal D_R=Q_R\) 分部积分。
\(E_R\) 有界并在每个正时间收敛，\(\mathcal D_R\to\|\nabla w\|_2^2\)
于 \(L^1\)。极限二次能量的初端右极限为 \(1/2\)，于是
\[
 \lim_{R\to\infty}\int_0^L\eta(\rho)Q_R(\rho)\,d\rho
     =\frac12\eta(0).
 \tag{BT.16}
\]
它与 BS 的频率通量产生同一个边界泛函，但不是同一截断序列。
极限有 Radon 表示；未证明 \(Q_R\,d\rho\) 的总变差一致有界、
测度弱星收敛或与 suitable 缺陷测度的识别。
对每个 \(0<\delta\le L\) 和任意 \(R_n\to\infty\)，
\[
 \{Q_{R_n}\}_n\text{ 不在 }L^1(0,\delta)\text{ 一致可积},\qquad
 \lim_{\delta\downarrow0}\lim_{R\to\infty}\int_0^\delta Q_R=\frac12,\quad
 \lim_{R\to\infty}\lim_{\delta\downarrow0}\int_0^\delta Q_R=0 .
 \tag{BT.17}
\]
第一项由 BT.14--15 和 Vitali 给出，第二个次序使用 BT.10 与 \(\kappa(\delta)\to0\)。
不称 \(Q_R\) 逐时非负；从零积分的非负性不等于点态非负性。

## 5. 幅度逃逸与压力配对的准确含义

由 \(\beta_R(z)=|z|^2/(s_R(z)+1)\)，在 \(|z|\le R\) 上得到
\[
 \int_{\{|w(t)|\le R\}}|w(t)|^2
 \le(\sqrt2+1)E_R(t)\le(\sqrt2+1)R\kappa(t).
 \tag{BT.18}
\]
在当前原子条件下每个正 \(t\) 的 \(w(t)\) 非零，
故 BT.11 给 \(\kappa(t)>0\)。
任取 \(R(t)\to\infty\) 且 \(R(t)\kappa(t)\to0\)，
低于这个增长幅度的能量仍趋零；例如 \(R(t)=\kappa(t)^{-1/2}\)。
因此
\[
 \int_{\{|w(t)|>R(t)\}}|w(t)|^2\longrightarrow1,\qquad
 \kappa(t)\|w(t)\|_\infty\ge\|w(t)\|_2^2
       \quad(t>0),
 \tag{BT.19}
\]
后一式按扩展值理解，由 \(\|w\|_2^2\le\|w\|_1\|w\|_\infty\) 直接给出。
这些是必要幅度约束，不是一个已经违反的先验上界。

几乎每个固定正时间，还可以把压力作空间分部积分：
\[
 Q_R=\int_\Omega\pi\,\operatorname{div}(D\beta_R(w))
 =-\frac1{R^2}\int_\Omega
      \pi\,s_R(w)^{-3}w_iw_j\partial_i w_j
 =\int_\Omega [w-D\beta_R(w)]\cdot\nabla\pi .
 \tag{BT.20}
\]
无散性消掉 Hessian 的 \(s_R^{-1}I\) 部分，而不是整个 Hessian。
这个公式指明压力没有确定符号；二次极限时的空间零配对也确实成立。

BT.20 只先在几乎每个时间作空间等式。
已付的时空 \(L^1\) 表示是 BT.8 的有界梯度形式；
没有另外证明 \(\pi\,\operatorname{div}(D\beta_R(w))\)
作为空间时间密度的绝对可积性。
不能用粗糙时间 Hölder 或空间分部积分，偷换已付的表示和未付的表示。

## 6. 仅换一个局部凸函数，能否普遍消压？

下面是一个有限范围的代数结论，不把实际 NS 压力换成任意压力。
设 \(\beta\in C^2(\mathbb R^3)\)，并要求对每个光滑周期无散场 \(v\)
和每个光滑周期标量 \(p\) 都有
\[
 \int_\Omega D\beta(v)\cdot\nabla p=0
 \quad\Longleftrightarrow\quad
 \operatorname{div}(D\beta(v))=0\text{ 对所有上述 }v.
 \tag{BT.21}
\]
这个“对所有 \(v,p\)”要求是结论的精确范围，比只对真实压力配对消失更强。

任取状态 \(z\) 和迹为零的矩阵 \(M\)，可以在一点附近实现
\(v(x)=z+Mx\) 的无散局部 jet：在坐标球中取向量势
\(-x\times z/2-x\times(Mx)/3\)，乘一个等于一于内球的光滑截止，
再取 curl 并周期延拓。内球正好恢复该仿射场，全局无散，且均值为零。
因此 BT.21 强迫 Hessian \(H=D^2\beta(z)\) 与所有迹零矩阵正交，
即 \(H=\lambda(z)I\)。

非对角二阶导数为零，使 \(\partial_i\beta\) 仅依赖 \(z_i\)；
各对角二阶导数又彼此相等。固定不同坐标独立变化，即得它们是同一常数。
这里不要求 \(C^3\) 正则性。故且仅故
\[
 \beta(z)=\frac\lambda2|z|^2+a\cdot z+c,\qquad
 \beta\text{ 凸}\Rightarrow\lambda\ge0,\qquad
 \|D\beta\|_\infty<\infty\Rightarrow\lambda=0 .
 \tag{BT.22}
\]
反向直接由无散性和周期梯度的均值为零验证。
所以在“仅依赖状态且对任意压力普遍消去”的测试类内，
有界梯度只能留下不控制范数的仿射函数；一般各向异性二次型也不符合要求。

这不排除依赖同一 NS 原解、时间、空间或非局部结构的测试，
也没有证明实际压力的某个特殊有符号配对一定非零。
它只排除不利用这些结构、单靠更换局部凸函数来普遍消压的办法。

## 7. 这一接口推进了什么

固定凸测试本身已经闭合，压力梯度 \(L^1L^{3/2}\) 与强 \(L^q,\ q<2\)
零初迹均是已付结果。前节的提醒是“不直接移植标量消压证明”，
不是已经证明向量方程不可重整化；本节把这个区别落实为完整证明。

但二次能量的统一极限没有闭合。
在原子条件下，撤去幅度截断的压力正好重现 BS 的半单位端点泛函，
因此不能把这一重写当成原子排除。
固定凸测试不会自动给一个对 \(R\) 一致的压力上界。
当前还没有从同一 NS 历史及 BP.26 的局部 \(L^2\) 对齐
得到消掉 BT.16 的合法压力配对控制。

一般三维正则性、G、原子生成或排除与 R.216--R.217 仍开放。
本稿没有构造任何真实 NS 奇点，也未证明新的无条件正则性类别、
文献新颖性或 Clay 成果。
