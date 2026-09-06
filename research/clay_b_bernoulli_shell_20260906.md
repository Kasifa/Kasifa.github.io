# 只依赖速率的压力重写：局部外壳不能省略

2026-09-06。**PROVED LOCALLY / LITERATURE-RELATED / G OPEN / NOT CLAY。**
采用原速度与黏性 1 的光滑周期 NS。这里不把总压当成新的压力规范，
也不假设沿流线 Bernoulli 常量。所有恒等式在原方程上直接推导。

## 1. 全域抵消来自无散性，不需要正速率下界

记 \(q=|u|\)，仅在 q>0 上定义 \(e=u/q\)，并取
\(F=-e\cdot\nabla q\)，在 q=0 上取零。令 \(\Phi\) 在当前速率范围
\([0,\|u\|_\infty]\) 上连续，定义

\[
 A_\Phi(s)=\int_0^s\Phi(a)\,da,\qquad
 B_\Phi(s)=s\Phi(s)-A_\Phi(s).
\tag{AG.1}
\]

q 是 Lipschitz 函数，\(A_\Phi(q)\) 也为 Lipschitz，链式法则在几乎处处成立。
u 在零集为零，所有带 u 的乘积均不受该集合上的梯度代表影响。无散性给

\[
 \int q\Phi(q)F
 =-\int \Phi(q)u\cdot\nabla q
 =-\int u\cdot\nabla A_\Phi(q)=0.
\tag{AG.2}
\]

因此对全域压力功

\[
 W=\int p\,u\cdot\nabla q
   =-\int q[p-\Phi(q)]F.
\tag{AG.3}
\]

这只是同一个双线性积分的重写。除 \(\Phi\) 为空间常量外，
\(p-\Phi(q)\) 通常不再满足原来的压力 Poisson 方程；
不得把 AG.3 解释成原方程任意改变压力的自由度。
一般可测投影及平台速率的处理另见 AF，而不靠光滑等值面的形式运算。

## 2. 空间 cutoff 的准确成本

取固定光滑 \(0\le\chi\le1\)，定义合并压力功

\[
 K_\chi(p)=\int p\,\operatorname{div}(\chi q u)
 =\int p\,[q u\cdot\nabla\chi+\chi u\cdot\nabla q].
\tag{AG.4}
\]

分部积分给

\[
 \begin{aligned}
 K_\chi(\Phi(q))
 &=\int q\Phi(q)u\cdot\nabla\chi
    +\int\chi\,u\cdot\nabla A_\Phi(q)\\
 &=\int B_\Phi(q)u\cdot\nabla\chi .
 \end{aligned}
\tag{AG.5}
\]

于是准确的局部等式为

\[
 K_\chi(p)
 =K_\chi(p-\Phi(q))
    +\int B_\Phi(q)u\cdot\nabla\chi.
\tag{AG.6}
\]

最后一项是原外壳上的通量。它没有固定符号，不能沿用全域抵消直接删除。
若仅知道 \(|\Phi|\le P\)，则 \(|B_\Phi(q)|\le2Pq\)，只能直接得到

\[
 \left|\int B_\Phi(q)u\cdot\nabla\chi\right|
 \le2P\|\nabla\chi\|_\infty
        \int_{\operatorname{supp}\nabla\chi}q^2.
\tag{AG.7}
\]

这个界保留了压力大小 P。P 尚未由一般有限能量作逐点一致控制。
允许 \(\Phi=\Phi(t,q)\) 时，上述恒等式只在每个固定时间使用，
没有对随时间改变的压力投影求导。

AG.1–AG.7 也适用于有界 Borel \(\Phi\)：采用 AF.4 的 Lipschitz
原函数链式法则即可。当前每个光滑时刻的条件压力投影可选
\(|\bar p(s)|\le\|p(t)\|_\infty\) 的 Borel 版本，所以原函数可以逐时定义。
但是仅有 \(L^2(q\,dx)\) 的投影或多项式逼近，并不足以推出
原函数及外壳项收敛；不能以该 Hilbert 收敛替代局部预算。
逐时有界版本仍在 AG.7 留下未支付的 \(\|p(t)\|_\infty\)。

## 3. Bernoulli 总压恰好吸收显式输运

取 \(\Phi(s)=-s^2/2\)，则

\[
 Q=p+\frac12q^2,\qquad
 A_\Phi(s)=-\frac16s^3,\qquad B_\Phi(s)=-\frac13s^3.
\tag{AG.8}
\]

AB.2 的完整局部 L³ 预算因此成为

\[
 H_\chi'+D_\chi
 =\frac13\int\Delta\chi\,q^3+K_\chi(Q)
 =\frac13\int\Delta\chi\,q^3
      -\int\chi q u\cdot\nabla Q.
\tag{AG.9}
\]

AG.6 的 \(-\frac13\int q^3u\cdot\nabla\chi\) 恰好抵消
AB.2 中的显式输运项。没有估计变小；该输运已经进入 Q 的梯度。

也可以用旋转形式独立检查符号：

\[
 (u\cdot\nabla)u=\nabla(q^2/2)-u\times\omega,\qquad
 \partial_tu-u\times\omega+\nabla Q=\Delta u,\qquad
 \omega=\operatorname{curl}u .
\tag{AG.10}
\]

以 \(\chi q u\) 配对，叉积逐点为零，再分部积分得到 AG.9。
零速率处可以用 AB 的 \(q_\epsilon\) 正则化证明并取极限。
这适用于非稳态、有黏性解，不是无黏稳态 Bernoulli 定律。

全域中 Q 和 p 的速率投影残差相同：只要 AF 的条件期望定义成立，

\[
 Q-\mathcal P_qQ=p-\mathcal P_qp,
\tag{AG.11}
\]

因为 \(q^2/2\) 本身已是 q 的函数。
标准周期压力估计也只有
\(\|Q\|_{9/4}\le C\|u\|_{9/2}^2\)；
替换为总压不会自动消除 AB.8 的大临界范数系数。

## 4. 等值面通量：不能任意逐连通分量减均值

对 q 的正则值 \(a>0\)，以超水平集 \(\{q>a\}\) 为区域，
散度定理给出整组等值面的有向通量为零：

\[
 \int_{\{q=a\}}\frac{u\cdot\nabla q}{|\nabla q|}\,dS=0.
\tag{AG.12}
\]

方向取 \(\nabla q/|\nabla q|\)；与超水平集外法向差一个负号，
不影响零值。这是 AG.2 的几何解释，不是其在临界层或平台上的证明。

环面上的单个连通等值面可能不分隔空间；它的通量不必为零。
例如 \(c>0\) 时，平滑周期无散场

\[
 u(x,y,z)=(\sin y,c,0),\qquad q=(c^2+\sin^2y)^{1/2}
\tag{AG.13}
\]

在任意 \(a\in(c,\sqrt{c^2+1})\) 的每个等值面分量上，
法向为正或负的 \(e_2\)，单分量通量为
\(\pm(2\pi)^2c\)，而所有分量相加为零。
因此不能未经证明就给每个连通分量选择不同的压力常量并全部删去其功。

这个例子甚至可嵌入真实的全时光滑无外力解：

\[
 u(t,x,y,z)=(e^{-t}\sin(y-ct),c,0),\qquad p=0.
\tag{AG.14}
\]

输运 \(c\partial_yu_1\) 与时间导数中的平移项抵消，
其余时间导数等于 \(\Delta u_1\)。它带常均值，用于原速度的几何量词检验；
不将此几何反例扩大成零均值类、首次奇点或合同 G 的反例。

## 5. 当前结论

AG.2 的抵消精确且没有除零问题；AG.6 给出了局部化必须保留的成本。
Bernoulli 总压只是把该成本与输运重新组合，未给出额外耗散。
全域压力投影必须在同一速率的全部点上理解，不能自动逐等值面分量处理。

下一步仍要证明压力余项能被真实解已有预算支付，或记录某个准确候选界
为何失败。上述恒等式没有控制首次奇点、反向持留或原移动路径，
不作新颖性声明，也没有仿真或科学图。
