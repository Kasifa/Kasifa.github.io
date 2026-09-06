# 同一原解的对齐残差：能量、混合压力与终端边界

2026-09-06。**CONDITIONAL / DIRECT DERIVATION / NON-AUTHOR REVIEW PASS / G OPEN / NOT CLAY。**

我把 BP 的局部对齐写成一个残差方程。目的不是再换一组范数，
而是确定同一个 NS 原解究竟提供了哪些额外结构。
结论包括一个无目标原子的残差测度、带已付源的正向能量估计，
以及完整周期混合压力的小量。它们仍未排除 BT 的幅度端点。
正原子是以下全部结论的条件，不是本节构造出的奇性。

## 1. 对象、方向和终端测度

沿用 BP.1--2、BP.20--27，固定同一个光滑、无外力周期 NS 原解。
记 \(\rho=T-t\)、\(0<\rho\le L\)、\(c=\sqrt m>0\)，并置
\[
 b(\rho)=-u(T-\rho),\qquad w(\rho)=A(T-\rho),\qquad z=b+cw.
 \tag{BU.1}
\]
所有空间范数都在固定 \(\mathbb T^3\) 上，\(\nu>0\) 固定。
三场无散，属于 \(L^\infty_\rho L^2_x\cap L^2_\rho H^1_x\)，
且每个严格正时间的闭区间上可进行下述能量测试。
这里 \(b\) 是反向原解，不是任意能量漂移。已有
\[
 \langle b,w\rangle=-c,\quad
 \|w(\rho)\|_2^2+2\nu\int_0^\rho\|\nabla w\|_2^2=1,\quad
 |b(\rho)|^2dx\stackrel{*}{\rightharpoonup}\mu_*,
 \quad |w(\rho)|^2dx\stackrel{*}{\rightharpoonup}\delta_a.
 \tag{BU.2}
\]
BP 对应的 \(w\) 零均值且弱初迹为零；\(b\) 一般没有零弱初迹。
这里不把任何一个弱迹替换成强 \(L^2\) 迹。

对任意连续实函数 \(\chi\)，常配对给
\[
 \left|\int\chi\,b\cdot w+c\chi(a)\right|
 \le \|b\|_2
       \left(\int|\chi-\chi(a)|^2|w|^2\right)^{1/2}\longrightarrow0.
 \tag{BU.3}
\]
因此展开平方便有完整的连续测试结论
\[
 |z(\rho)|^2dx\stackrel{*}{\rightharpoonup}
 \mu_{\rm res}:=\mu_*-m\delta_a\ge0,\qquad
 \mu_{\rm res}(\{a\})=0.
 \tag{BU.4}
\]
非负性也由每个非负连续测试的极限得到。
这把 BP.26 明写为测度减法，核心仍是已有常配对及定位，
不是两个弱场直接相乘。背景能量或别处原子可以留在 \(\mu_{\rm res}\) 中；
一般不能声称 \(z\to0\) 强 \(L^2(\mathbb T^3)\)。

## 2. 完整压力与带源残差方程

定义周期零均值双线性压力
\(\Pi(v,h)=R_iR_j(v_i h_j)\)，常数模态为零。
重复指标求和；交换指标给 \(\Pi(v,h)=\Pi(h,v)\)。
使用的是整个周期胞的压力，不是截断后另选的局部压力。
令 \(p_b=\Pi(b,b)\)、\(\pi=\Pi(w,b)\)、\(q=p_b+c\pi\)。
直接反转原时间并线性相加得到
\[
 \begin{aligned}
 b_\rho+(b\cdot\nabla)b+\nabla p_b&=-\nu\Delta b,\\
 w_\rho+(b\cdot\nabla)w+\nabla\pi&=\nu\Delta w,\\
 z_\rho+(b\cdot\nabla)z+\nabla q
 &= -\nu\Delta z+2\nu c\Delta w
  = \nu\Delta z-2\nu\Delta b .
 \end{aligned}
 \tag{BU.5}
\]
前两式黏性符号相反；第三式的两种写法严格相同。
可以把 \(z\) 看成带源的正向抛物方程，但必须保留
\(-2\nu\Delta b\in L^2_\rho H^{-1}_x\)。
不能把它当作齐次正向方程，也不能说残差完全没有能量估计。

写 \(r=\Pi(z,w)\) 和 \(p_w=\Pi(w,w)\)，则
\[
 \pi=r-cp_w,\qquad
 q=\Pi(z,z)-cr=\Pi(z,b),\qquad
 p_b=\Pi(z,z)-2cr+c^2p_w .
 \tag{BU.6}
\]
特别是 \(q=p_b+c\pi\) 的合并不表示原来的 \(\pi\) 消失。
后面每项都保持这一非局部分解及同一压力规范。

## 3. 全局能量与固定截止的合法终端

设 \(D_v(\rho)=\int_0^\rho\|\nabla v\|_2^2\)。
严格正时间上，输运斜对称、压力与无散场正交；
\(b,w\) 的相反扩散使交叉梯度抵消。积分到弱终端测度给
\[
 \begin{aligned}
 \|b(\rho)\|_2^2&=\mu_*(\mathbb T^3)+2\nu D_b(\rho),\\
 \|z(\rho)\|_2^2&=\mu_{\rm res}(\mathbb T^3)
                         +2\nu[D_b(\rho)-c^2D_w(\rho)],\\
 \langle z,w\rangle&=-2\nu cD_w(\rho).
 \end{aligned}
 \tag{BU.7}
\]
这些是精确记账，不是新增的有符号矛盾。
即使额外假设全部终端能量只在该原子，
第二式也只给 \(D_b\ge c^2D_w\)，仍与非负能量相容。

从 BU.5 的正向带源写法，任意 \(0\le s<t\le L\) 有
\[
 \frac12\|z(t)\|_2^2+\nu\int_s^t\|\nabla z\|_2^2
 =\frac12\|z(s)\|_2^2+2\nu\int_s^t\nabla b:\nabla z,
 \quad
 \frac12\|z(t)\|_2^2+\frac{\nu}{2}\int_s^t\|\nabla z\|_2^2
 \le\frac12\|z(s)\|_2^2+2\nu\int_s^t\|\nabla b\|_2^2 .
 \tag{BU.8}
\]
当 \(s=0\) 时，符号 \(\|z(0)\|_2^2\) 在此仅表示
\(\mu_{\rm res}(\mathbb T^3)\)，不定义一个达到该范数的初始 \(L^2\) 场。
等式先在 \(s>0\) 成立，再用 BU.4 和梯度的时间可积性令 \(s\downarrow0\)。

为核对局部测试的每项，记
\(M=\sup_{0<\rho\le L}(\|b\|_2+\|w\|_2+\|z\|_2)<\infty\)，
\(h_v(\delta)=\|v\|_{L^2(0,\delta;H^1)}\)。
非零均值场使用带低频项的周期 Sobolev 界。
能量插值与有限指数周期压力估计给
\[
 b,w,z\in L^4_\rho L^3_x,\qquad
 p_b,\pi,q\in L^2_\rho L^{3/2}_x,\qquad
 \nabla p_b,\nabla\pi,\nabla q\in L^1_\rho L^{3/2}_x .
 \tag{BU.9}
\]
前两个压力指数也可由 \(L^2L^6\) 的漂移乘 \(L^\infty L^2\) 的场取得。
梯度估计使用 \(\nabla\Pi(v,b)=-Q[(b\cdot\nabla)v]\)，
\(L^2L^6\) 乘 \(L^2L^2\)，其中 \(Q=I-P\) 在 \(L^{3/2}\) 有界。
所以固定截止的压力通量乘第三个 \(L^4L^3\) 场在
\(L^{4/3}_\rho L^1_x\)；梯度边界项和源项也可积。
不需要删掉任一压力或提前假设终端强连续性。

对 \(\chi\in C^1_\rho C^2_x\)，局部交叉配对满足
\[
 \begin{aligned}
 \frac d{d\rho}\int\chi b\cdot w
 ={}&\int(\chi_\rho+b\cdot\nabla\chi)b\cdot w
       +\int(p_bw+\pi b)\cdot\nabla\chi\\
 &-\nu\int \partial_k\chi
             (b_i\partial_k w_i-w_i\partial_k b_i).
 \end{aligned}
 \tag{BU.10}
\]
相反扩散留下了这一边界差项；\(\chi=1\) 才回到常配对。
对残差，正向带源形式给
\[
 \begin{aligned}
 \frac d{d\rho}\frac12\int\chi|z|^2+\nu\int\chi|\nabla z|^2
 ={}&\frac12\int(\chi_\rho+b\cdot\nabla\chi)|z|^2
       +\frac{\nu}{2}\int|z|^2\Delta\chi
       +\int qz\cdot\nabla\chi\\
 &+2\nu\int\chi\nabla b:\nabla z
       +2\nu\int z_i\partial_k\chi\,\partial_k b_i .
 \end{aligned}
 \tag{BU.11}
\]
这些先在正时间闭区间由空间分部积分成立。
对 BP 的伴随，光滑漂移的线性能量法在每个这样的区间保证测试合法；
也可先作 Fourier/Galerkin 能量逼近再传极限。
BU.9 及梯度能量保证所有右端在固定截止下绝对可积。
故把左端初时移到零是合法的：初始交叉项为
\(-c\chi(0,a)\)，初始残差能量为
\(\frac12\int\chi(0,x)d\mu_{\rm res}(x)\)。

下面给出固定空间截止 \(0\le\chi\le1\) 的明确支付。
用 \(\|z\|_{12/5}^2\le CM^{3/2}\|z\|_{H^1}^{1/2}\)、
\(\|z\|_3\le CM^{1/2}\|z\|_{H^1}^{1/2}\)，
时间 Hölder 的 \(2,4,4\)，再对内部源用 Young，有
\[
 \begin{aligned}
 \sup_{0<t\le\delta}
 \left[\frac12\int\chi|z(t)|^2+
                    \frac{\nu}{2}\int_0^t\!\int\chi|\nabla z|^2\right]
 \le{}&\frac12\int\chi\,d\mu_{\rm res}
             +2\nu\int_0^\delta\!\int\chi|\nabla b|^2\\
 &+C\|\nabla\chi\|_\infty
       [M^{3/2}\delta^{1/4}h_b(\delta)h_z(\delta)^{1/2}
                   +\nu M\delta^{1/2}h_b(\delta)]\\
 &+C\nu\|\Delta\chi\|_\infty M^2\delta .
 \end{aligned}
 \tag{BU.12}
\]
压力项在这里用完整的 \(\|q\|_{3/2}\le C\|b\|_6\|z\|_2\)，
没有局部化时漏掉的远场项。
取 \(\chi_r=1\) 于 \(B_r(a)\)、支撑于 \(B_{2r}(a)\)，
先固定 \(r\) 再缩短时间，随后令 \(r\downarrow0\)，可以选择
\(\delta_r\downarrow0\) 使
\[
 \sup_{0<t\le\delta_r}\int_{B_r(a)}|z(t)|^2
       +\nu\int_0^{\delta_r}\!\int_{B_r(a)}|\nabla z|^2
       \longrightarrow0.
 \tag{BU.13}
\]
两个非负项分别由 BU.12 控制，合并时至多增加固定因子。
这是真实但未缩放的对角小量。它不规定 \(\delta_r/r^2\)，
也不支付临界归一化后的 \(r^{-1}\) 能量或梯度成本；
截止导数的 \(r^{-1},r^{-2}\) 必须由具体时间选择承担。

## 4. 混合源和完整非局部压力的已付小量

BU.4 的无原子结论与 BU.2 的伴随定位可以合用，
得到比“对一个固定截止的配对”更直接的乘积结论。用张量的 Frobenius 范数，
\[
 e(\rho):=\|z(\rho)\otimes w(\rho)\|_1
          =\int|z||w|\longrightarrow0 .
 \tag{BU.14}
\]
证明先选 \(\mu_{\rm res}(\partial B_r(a))=0\) 的固定小半径。
球内 Cauchy--Schwarz 项的上极限不超过
\(\mu_{\rm res}(B_r(a))^{1/2}\)，球外项不超过
\(M\|w\|_{L^2(B_r^c)}\to0\)。
然后沿连续性半径 \(r\downarrow0\)，由 \(\mu_{\rm res}(\{a\})=0\) 得结论。
因此它是全时间的极限，不只是子列或有符号平均。
特别是 \(e_\delta:=\sup_{0<\rho\le\delta}e(\rho)\to0\)。

对任何 \(s>3/2\)，周期 Fourier 乘子给
\[
 \|r(\rho)\|_{H^{-s}}\le C_s e(\rho),\qquad
 \|\nabla r(\rho)\|_{H^{-s-1}}\le C_s e(\rho).
 \tag{BU.15}
\]
因为每个 Fourier 系数受 \(C\|z\otimes w\|_1\) 控制，
\(R_iR_j\) 的符号有界，且
\(\sum_{k\in\mathbb Z^3}(1+|k|^2)^{-s}<\infty\)。
这也给固定光滑测试和相应 \(L^\infty(0,\delta)\) 负范数的小量；
不使用并不成立的 Riesz 强 \(L^1\) 有界性。

还可以在有限指数上保留已知梯度成本。
取光滑截止 \(0\le\eta_r\le1\)，于 \(B_r(a)\) 等于一，支撑于 \(B_{2r}(a)\)。
定义
\(\epsilon_r(\delta)=\sup_{0<\rho\le\delta}\|\eta_r z(\rho)\|_2\)、
\(\omega_r(\delta)=\sup_{0<\rho\le\delta}\|(1-\eta_r)w(\rho)\|_2\)。
在源张量内作代数分割，再对整个周期胞应用同一个压力算子，有
\[
 \|r\|_{L^2(0,\delta;L^{3/2})}
 \le C[\epsilon_r(\delta)h_w(\delta)
                 +\omega_r(\delta)h_z(\delta)] .
 \tag{BU.16}
\]
具体地，近项用 \(\|\eta_r z\|_2\|w\|_6\)，
其余项用 \(\|z\|_6\|(1-\eta_r)w\|_2\)。
这里没有把输出压力截在球内，也没有遗漏任何远场压力；
只是在线性算子输入上分割，故常数独立于 \(r\)，无截止导数。

固定 \(r\) 时，\(\epsilon_r(\delta)^2\to\int\eta_r^2d\mu_{\rm res}\)，
\(\omega_r(\delta)\to0\)。于是
\[
 \|r\|_{L^2(0,\delta;L^{3/2})}
           =o\big(h_w(\delta)+h_z(\delta)\big)\qquad(\delta\downarrow0).
 \tag{BU.17}
\]
分母严格正：否则 \(w\) 在该时间区间为零，与 \(\langle b,w\rangle=-c\) 矛盾。
先固定任意 \(r\) 对 BU.16 的比值取上极限，其上界为
\(C(\int\eta_r^2d\mu_{\rm res})^{1/2}\)；再令 \(r\downarrow0\)。
这一步获得一个真正的小系数，但不附带任何时间或临界尺度衰减率。
它也不控制 \(q\) 的纯残差项 \(\Pi(z,z)\)，或 \(\pi\) 的自压力项 \(p_w\)。

## 5. 尚未支付的幅度配对

沿用 BT 的
\(\beta_R(\xi)=R^2(\sqrt{1+|\xi|^2/R^2}-1)\)，
\(Q_R=-\int D\beta_R(w)\cdot\nabla\pi\)。
BU.6 的精确分解给
\[
 Q_R=c\int D\beta_R(w)\cdot\nabla p_w
              -\int D\beta_R(w)\cdot\nabla r .
 \tag{BU.18}
\]
固定 \(R\) 时，两个积分均合法；
例如 \(\nabla r=-Q[(w\cdot\nabla)z]\) 给
\[
 \int_0^\delta
       \left|\int D\beta_R(w)\cdot\nabla r\right|d\rho
 \le C R\,h_w(\delta)h_z(\delta).
 \tag{BU.19}
\]
这不是对 \(R\to\infty\) 的一致估计。
若改为把 \(r\in L^{3/2}\) 与
\(\operatorname{div}D\beta_R(w)\) 配对，只有
\(|D^2\beta_R|\le1\)、\(\nabla w\in L^2\) 还不够：
空间倒数指数 \(2/3+1/2=7/6>1\)，缺的 \(L^3\) 导数不能略过。
BU.15 的负范数也只能支付有统一正 Sobolev 范数的测试，
没有给随 \(R,w\) 变化的测试这样的界。
这些是所列估计的准确接口缺口，不是所有 NS 消去方式的不可能定理。

在 BP 的额外原子条件下，BT 已证明每个 \(0<\delta\le L\) 都有
\[
 \lim_{R\to\infty}\int_0^\delta Q_R\,d\rho=\frac12 .
 \tag{BU.20}
\]
BU.18--19 尚不能把这半单位有符号边界贡献分别归给自压力或混合压力。
混合压力的固定测试消失、有限指数小系数，与整个幅度族的一致可积性
不是同一个命题。自压力项也没有由局部对齐自动消失。

本节完成的是同一原解的残差和混合压力核算，不是原子排除。
下一项应在这个精确分解上检查有符号、时间积分后的混合压力配对：
能否从 BU.14、BU.17 和原方程再取得一个不随幅度增长的界；
如果必须额外加入临界梯度或一致可积性，应明确记为未付输入。
不能重复把已有常配对称为新强制估计，也不能预设 \(b=-cw\) 全局成立。
原子存在与排除、任意奇点是否生成原子、G、R.216--R.217、
一般三维正则性和 Clay 结论均未完成。
