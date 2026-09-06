# 共同伴随与全尾饱和：固定原解结构的证明核查

2026-09-06。**LITERATURE RECONSTRUCTION / CONDITIONAL / NON-AUTHOR REVIEW PASS / G OPEN / NOT CLAY。**

我核查 Huang [2608.04138v1](https://arxiv.org/abs/2608.04138v1)
的 Theorem 2.3、Corollary 2.5 及 §§2--6。下面重新写出所需证明，
展开局部 Hodge、周期紧性和能量时间连续性接口。
这是已有预印本结果的内部重构，不宣称新定理或一般正则性。

## 1. 假设和演化对象

固定同一个无外力光滑周期 NS 解，在
\(\Omega=\mathbb T^3\)、\(t_b\le t<T<\infty\)、固定 \(\nu>0\) 上满足
\[
 u_t+P[(u\cdot\nabla)u]=\nu\Delta u,\quad \operatorname{div}u=0,\quad
 E_*:=\sup_{t_b\le t<T}\|u(t)\|_2<\infty,\quad
 \int_{t_b}^T\|\nabla u\|_2^2<\infty .
 \tag{BP.1}
\]
这里 \(E_*\) 是范数，不是 BO 的平方能量 \(E\)。
BM 的全时间终端测度证明同样适用于固定 \(\nu\)，并另假设
\[
 |u(t)|^2dx\stackrel{*}{\rightharpoonup}\mu_*,\quad
 \mu_*(\{a\})=m>0.
 \tag{BP.2}
\]
没有假设终端强 \(L^2\) 迹；正原子是条件，不是任意奇点的已证产物。

在同一原时间轴上定义无散演化 \(U\) 和逐分量被动演化 \(S\)：
\[
 h_t+P[(u\cdot\nabla)h]=\nu\Delta h,\qquad
 z_t+(u\cdot\nabla)z=\nu\Delta z.
 \tag{BP.3}
\]
每个紧的终点前区间上 \(u\) 光滑，Fourier--Galerkin、能量法和
线性方程唯一性给 \(U(t,r)U(r,s)=U(t,s)\) 及强连续性。
\(P\) 是整个周期胞的 Leray 正交投影，包含常数模态；不是局部 \(Q_B\)。
无散输运的斜对称性给
\[
 \|U(t,s)f\|_2^2+2\nu\int_s^t\|\nabla U(\rho,s)f\|_2^2d\rho=\|f\|_2^2,
 \quad
 A_t+P[(u\cdot\nabla)A]=-\nu\Delta A,
 \tag{BP.4}
\]
\[
 \|U(t,s)^*g\|_2^2+2\nu\int_s^t\|\nabla U(t,\rho)^*g\|_2^2d\rho=\|g\|_2^2,
 \quad \langle U(t,s)f,g\rangle=\langle f,U(t,s)^*g\rangle .
 \tag{BP.5}
\]
这些等式先在紧区间成立；没有由此直接引入终端算子或终端紧性。
被动演化也在 \(L^2\) 收缩，但不保持无散性。

## 2. 先固定球，再定义 packet

令
\[
 \mathcal H(B)=\overline{C^\infty_{c,\sigma}(B)}^{\,L^2(\Omega)},\quad
 Q_B=\operatorname{Proj}_{\mathcal H(B)},\quad
 Q_{B'}Q_B=Q_BQ_{B'}=Q_{B'}\quad(B'\Subset B).
 \tag{BP.6}
\]
闭包中的场在球外为零且全局无散。对紧支撑无散场，
\(\int \phi_i=\int\operatorname{div}(x_i\phi)=0\)，故闭包也零均值。
差 \(D=Q_B-Q_{B'}\) 是
\(\mathcal H(B)\cap\mathcal H(B')^\perp\) 上的正交投影。

若 \(w=Q_{B_R}v\)、\(v\) 全局无散，则 \(q=v-w\) 在 \(B_R\)
无散，且对所有紧支撑 \(\Psi\)，
\(\langle q,\operatorname{curl}\Psi\rangle=0\)。
所以 \(\operatorname{curl}q=0\)，
\(\Delta q=\nabla\operatorname{div}q-\operatorname{curl}\operatorname{curl}q=0\)。
调和分布的内部正则性使 \(q\) 光滑；球上无旋场具有势 \(q=\nabla h\)，
且 \(h\) 调和。不必把局部 de Rham 原文当作已读外部证明。

正交性与 \(w\) 的支撑给
\[
 \|\nabla h\|_{L^2(B_R)}^2=\|v\|_{L^2(B_R)}^2-\|w\|_2^2,\qquad
 \|Q_{B_R}v\|_2\ge \|v\|_{L^2(B_r)}
       -C(r/R)^{3/2}\|v\|_{L^2(B_R)} .
 \tag{BP.7}
\]
\(r\le R/2\) 时对调和分量用内点均值界再乘 \(B_r\) 的体积平方根；
\(r>R/2\) 时用包含关系并放大常数。常数对平坦胞的小球一致。
同理，差空间的场在内球是调和梯度。

预先固定可数稠密中心、半径、正有理水平、缓冲比例及时间骨架，
不使用 \(a,m,\mu_*\)。对模板截止 \(\chi=1\) 于缓冲内球、
支撑于二倍内球，保留所有
\[
 M_\chi(h)<\theta<M_\chi(H),\quad
 M_\chi(t)=\int\chi|u(t)|^2,\quad
 \tau=\min\{t\in[h,H]:M_\chi(t)=\theta\},\quad \tau<\sigma<H
 \tag{BP.8}
\]
的条目，其中 \(h,H,\sigma\) 来自预定时间骨架。首次过水平时刻
由连续性给出，不必是有理数；全目录仍可数。

指定原子后选有理 \(\theta_j\uparrow m\) 和
\(\epsilon_j\downarrow0\)，使 \(\epsilon_j\le\sqrt{\theta_j}/4\)；置 \(\epsilon_0=1\)。
先选缓冲 \(\beta_j\) 使
\(C(2\beta_j)^{3/2}E_*\le\epsilon_j\)。
递归选择 \(h_j>\max(\sigma_{j-1},\gamma_j)\)，\(\gamma_j\uparrow T\)，
再用光滑轨道在 \([t_b,h_j]\) 的一致空间绝对连续性选很小的球 \(B_j\)。
这一一致性由轨道的紧 \(L^2\) 像取有限网，再对各网点用积分绝对连续性得到。
其中心和半径可从固定稠密骨架取，保持 \(a\) 在缓冲内球、
\(\overline B_j\subset B_{j-1}\)、直径趋零。要求
\[
 \sup_{t_b\le t\le h_j}\|u(t)\|_{L^2(B_j)}
 \le\min(\epsilon_{j-1},\sqrt{\theta_j}/2),\qquad
 \sup_{t_b\le t\le\sigma_j}\|u(t)\|_{L^2(B_{j+1})}\le\epsilon_j .
 \tag{BP.9}
\]
第二式是下一次选球时实现的。正原子与 BP.2 保证固定截止
\(M_{\chi_j}(t)\to\int\chi_jd\mu_*\ge m>\theta_j\)，故能选高时刻 \(H_j\)，
完成 BP.8。于是 \(\tau_j<\sigma_j<\tau_{j+1}\)、\(\tau_j\uparrow T\)。

关键顺序是 \(q_{j-1}\) 一直等待到 \(B_j\) 最终选定才定义。
令 \(D_j=Q_{B_j}-Q_{B_{j+1}}\)，只定义一次
\[
 q_j=\frac{D_ju(\tau_j)}{\|D_ju(\tau_j)\|_2},\quad
 \langle u(\tau_j),q_j\rangle=\|D_ju(\tau_j)\|_2>0,\quad
 \|D_ju(\tau_j)\|_2^2\ge\theta_j-2\epsilon_j\sqrt{\theta_j}.
 \tag{BP.10}
\]
最后不等式来自 BP.7 的
\(\|Q_{B_j}u(\tau_j)\|_2\ge\sqrt{\theta_j}-\epsilon_j\)，
BP.9 的内球投影不超过 \(\epsilon_j\)，以及差投影的勾股等式。
各差空间正交，所以 \(q_j\) 正交归一、零均值、支撑于 \(B_j\)，
并在 \(B_{j+1}\) 是调和梯度。

## 3. 被动避让与反向局部化的两个不同工具

逐分量被动方程可用 Kato 不等式取得 \(L^1\) 收缩。
为展开其周期 Nash 接口，Fourier 低高频分割给
\(\|f\|_2^2\le C N^3\|f\|_1^2+N^{-2}\|\nabla f\|_2^2\)，\(N\ge1\)。
优化并保留低频项得到
\[
 \|f\|_2^{10/3}\le C\|f\|_1^{4/3}
       (\|\nabla f\|_2^2+\|f\|_2^2),\qquad
 \|S(t,s)\|_{L^1\to L^2},\ \|S(t,s)\|_{L^2\to L^\infty}
       \le C[1+(\nu(t-s))^{-3/4}].
 \tag{BP.11}
\]
具体地 \(y=\|f\|_2^2\)、\(M=\|f(s)\|_1\) 满足
\(y'\le-c\nu M^{-4/3}y^{5/3}+2\nu y\)。
高于固定倍 \(M^2\) 时吸收线性项并积分 \(y^{-2/3}\)，得到
\(y(t)\le C M^2[1+(\nu(t-s))^{-3/2}]\)；低于该阈值用常数屏障。
\(M=0\) 时解为零。反向标量伴随仍为无散漂移，故对偶给第二个界。
这不提供 \(U\) 的同样 \(L^\infty\) 界。

在选 \(B_j\) 时，只有 \(i\le j-2\) 的被动初态已固定。
它们在 \(t\ge h_j\) 有固定正延迟，BP.11 给统一 \(L^\infty\) 界。
选球时再支付小体积，即有
\[
 |\langle S(\tau_j,\tau_i)q_i,q_j\rangle|\le\eta_j,\quad i\le j-2.
 \tag{BP.12}
\]
先取明确的偶数子列。再取任意子列时仅保留原来的 \(q\)，不重新投影；
内球变小，正交性、调和性和旧单指标估计仍成立。
因此最终保留链的任意 \(i<j\) 都继承被动避让。
“全尾”随后是这条保留链的全尾，不是原始目录的全部条目。

对一般光滑无散漂移 \(b\)，反向脉冲使用的正向方程为
\(w_\rho+(b\cdot\nabla)w+\nabla\pi=\nu\Delta w\)，\(\operatorname{div}w=0\)，
零均值初态。均值保持，压力取周期零均值：
\[
 \pi=R_iR_j(b_jw_i),\quad \|\pi\|_{3/2}\le C\|b\|_6\|w\|_2,\qquad
 \|w(\rho)\|_2^2+2\nu\int_0^\rho\|\nabla w\|_2^2=\|w_0\|_2^2.
 \tag{BP.13}
\]
有限指数周期压力工具采用 BL 的完整核、有限覆盖与 CZ 接口。
对 \(0\le\zeta\le1\) 的 \(W^{2,\infty}\) 截止，完整恒等式为
\[
 \frac d{d\rho}\int\zeta|w|^2+2\nu\int\zeta|\nabla w|^2
 =\int |w|^2b\cdot\nabla\zeta
    +2\int\pi w\cdot\nabla\zeta+\nu\int|w|^2\Delta\zeta .
 \tag{BP.14}
\]
没有删除压力输运。零均值周期 Sobolev 与插值给
\[
 \|w\|_{12/5}^2\le C\|w\|_2^{3/2}\|\nabla w\|_2^{1/2},\quad
 \|w\|_3\le C\|w\|_2^{1/2}\|\nabla w\|_2^{1/2},\quad
 \int_0^L\|b\|_6\|w\|_2^{3/2}\|\nabla w\|_2^{1/2}
 \le L^{1/4}B W^{3/2}G^{1/2},
 \tag{BP.15}
\]
其中 \(B=\|b\|_{L^2_\rho L^6_x}\)、\(W=\|w\|_{L^\infty_\rho L^2_x}\)、
\(G=\|\nabla w\|_{L^2_{\rho,x}}\)。时间 Hölder 使用 \(2,4,4\)。

选 \(\zeta=0\) 于 \(B_r(a)\)，等于一于 \(B_{2r}(a)^c\)。
若 \(w_0\in\mathcal H(B_r(a))\)，则
\[
 \|w(L)\|_{L^2(B_{2r}(a)^c)}^2
 \le Cr^{-1}(2\nu)^{-1/4}L^{1/4}B\|w_0\|_2^2
       +C\nu r^{-2}L\|w_0\|_2^2 .
 \tag{BP.16}
\]
一般 \(L^2\) 初态先用 \(\mathcal H(B_r)\) 定义中的紧支撑光滑无散场逼近，
对各个光滑初态求完整线性解，再用能量差恒等式传极限。
不要求 Fourier 截断本身保留紧支撑。

## 4. 同一个伴随的提取及终端定位

沿已经固定的保留链置
\[
 v_j(t)=U(\tau_j,t)^*q_j\quad(t\le\tau_j),\qquad
 \|v_j(t)\|_2^2+2\nu\int_t^{\tau_j}\|\nabla v_j\|_2^2=1.
 \tag{BP.17}
\]
每个 \([t_b,S]\)、\(S<T\) 上，
\(v_j\) 在 \(L^\infty L^2\cap L^2H^1\) 有界，且
\(\|(v_j)_t\|_{H^{-1}}\le C_S\|v_j\|_2+\nu\|\nabla v_j\|_2\)。
用周期 Fourier 截断 \(P_{\le N}\)，
\[
 \|(I-P_{\le N})v_j\|_{L^2(t_b,S;L^2)}^2
 \le N^{-2}\|\nabla v_j\|_{L^2(t_b,S;L^2)}^2.
 \tag{BP.18}
\]
有限个低模态系数的导数在 \(L^2_t\) 有界，所以在闭时间区间
一致有界、等度连续。有限模态抽取再令 \(N\to\infty\)，并对 \(S\uparrow T\)
对角化，得到同一子列的
\[
 v_j\to A\text{ 强 }L^2(t_b,S;L^2),\qquad
 v_j(t)\rightharpoonup A(t)\text{ 于 }L^2\quad\text{每个固定 }t<T .
 \tag{BP.19}
\]
第二项使用有限模态的一致时间收敛和统一 \(L^2\) 界，不是仅凭强时空
收敛声称逐时收敛。梯度在紧区间弱收敛，方程传给 \(A\)。

\(u\) 本身解 BP.3 的无散方程，故固定原解的对偶恒等式给
\[
 \langle u(t),v_j(t)\rangle=\langle u(\tau_j),q_j\rangle
 \longrightarrow a_\infty,\qquad
 \langle u(t),A(t)\rangle=a_\infty,\quad a_\infty^2\ge m,\quad a_\infty>0.
 \tag{BP.20}
\]
配对有界，可以再选一次子列；没有改变任何漂移或原时间。

对固定光滑无散 \(\phi\)，直接把导数移到测试场上：
\[
 |\partial_t\langle v_j,\phi\rangle|
 \le E_*\|\nabla\phi\|_\infty+\nu\|\Delta\phi\|_2=:C_\phi,\quad
 |\langle A(t),\phi\rangle|\le C_\phi(T-t),\quad
 A(t)\rightharpoonup0\ (t\uparrow T).
 \tag{BP.21}
\]
后两项由积分到 \(\tau_j\)、正交序列 \(q_j\rightharpoonup0\)、
再令 \(j\to\infty\) 和测试稠密性得到。

在固定 \([s,t]\subset[t_b,T)\) 上 \(A_t\in L^2H^{-1}\)、\(A\in L^2H^1\)。
有限 Fourier 投影满足
\(\|P_{\le N}A(t)\|_2^2-\|P_{\le N}A(s)\|_2^2
=2\int_s^t\langle A_t,P_{\le N}A\rangle\)。
投影在 \(L^2H^1\) 强收敛，右端在所有端点上一致收敛；
已有弱连续代表的逐点 Fourier 范数也收敛。
因此范数连续，结合弱连续得强 \(L^2\) 连续，并可测试得到
\[
 \|A(s)\|_2^2+2\nu\int_s^t\|\nabla A\|_2^2=\|A(t)\|_2^2,\qquad
 \|A(t)\|_2^2\uparrow d_A\in(0,1].
 \tag{BP.22}
\]
上界来自 BP.17、BP.19 下半连续；正性来自 BP.20。
这也覆盖左端 \(t_b\)，不需要在终点作强连续假设。

固定小半径 \(r>0\)，然后固定 \(t<T\)。
对充分大的 \(j\)，\(B_j\Subset B_{r/2}(a)\)。
置 \(w_j(\rho)=v_j(\tau_j-\rho)\)、\(b_j(\rho)=-u(\tau_j-\rho)\)。
它们满足 BP.13，且若 \(\delta=T-t\)，
\[
 \|b_j\|_{L^2(0,\tau_j-t;L^6)}
 \le C\big(\|\nabla u\|_{L^2(t,T;L^2)}+E_*\delta^{1/2}\big),\quad
 \|v_j(t)\|_{L^2(B_r(a)^c)}^2
 \le C_{r,\nu}\delta^{1/4}
       \big(\|\nabla u\|_{L^2(t,T;L^2)}+E_*\delta^{1/2}\big)
       +C_r\nu\delta .
 \tag{BP.23}
\]
这是 BP.16 的应用，常数允许依赖固定 \(r\)。
先 \(j\to\infty\) 用弱下半连续，再 \(t\uparrow T\)，得到
\[
 \|A(t)\|_{L^2(B_r(a)^c)}\to0\quad(\text{每个固定 }r),\qquad
 |A(t)|^2dx\stackrel{*}{\rightharpoonup}d_A\delta_a .
 \tag{BP.24}
\]
测度结论由连续测试的 \(B_r\) 内振荡与球外尾共同给出。
没有交换空间半径与终端时间的极限。

## 5. 范数饱和，随后才有全尾强收敛

对固定截止 \(\chi_r=1\) 于 \(B_r(a)\)、支撑于 \(B_{2r}(a)\)，
配对的球外部分由 BP.24 消失。先令 \(t\uparrow T\) 用 BP.2，
再令 \(r\downarrow0\)：
\[
 a_\infty^2\le d_A\int\chi_r^2d\mu_*,\qquad
 m\le a_\infty^2\le md_A\le m,\qquad
 a_\infty=\sqrt m,\quad d_A=1.
 \tag{BP.25}
\]
完整原子质量下界与同一个原解的配对在这里缺一不可。

展开局部平方，固定光滑 \(0\le\chi\le1\)，且 \(\chi=1\) 于 \(a\) 的一个邻域：
\[
 \lim_{t\uparrow T}\int\chi|u(t)-\sqrt m A(t)|^2
 =\int\chi\,d\mu_*-m,\qquad
 \lim_{r\downarrow0}\limsup_{t\uparrow T}
       \int_{B_r(a)}|u(t)-\sqrt m A(t)|^2=0.
 \tag{BP.26}
\]
交叉项极限为 \(m\)，由常配对和球外伴随尾消失给出，
不是从两个弱极限直接相乘。

固定一次 \(t_0=t_b\)。零延拓梯度到共同区间 \((t_0,T)\)。
它们有统一 \(L^2\) 界；BP.22 与 \(d_A=1\) 先给极限梯度的全尾 \(L^2\) 界。
任意固定 \(L^2\) 测试先截断于 \(S<T\)，
紧区间弱收敛处理前段，测试自身的 \(L^2(S,T)\) 范数处理尾段，故
\[
 1_{(t_0,\tau_j)}\nabla v_j\rightharpoonup\nabla A
      \text{ 于 }L^2((t_0,T)\times\Omega),\qquad
 \|A(t_0)\|_2^2+2\nu\int_{t_0}^T\|\nabla A\|_2^2=1.
 \tag{BP.27}
\]
第二项是 BP.22、BP.25 的单调极限。它给完整极限范数，而不是先验
假设脉冲尾部一致可积。

在固定 Hilbert 直和 \(\mathcal X=L^2_\sigma\oplus L^2((t_0,T)\times\Omega)\)
中置
\[
 X_j=(v_j(t_0),\sqrt{2\nu}\,1_{(t_0,\tau_j)}\nabla v_j),\quad
 X=(A(t_0),\sqrt{2\nu}\nabla A),\quad
 X_j\rightharpoonup X,\quad \|X_j\|=\|X\|=1,\quad X_j\to X.
 \tag{BP.28}
\]
最后一步是 \(\|X_j-X\|^2=2-2\langle X_j,X\rangle\to0\)。
因此同时得到固定初时强 \(L^2\) 和整个终端区间强梯度收敛。
同一论证适用于任意固定 \(t_0<T\)。

## 6. 整个有序三角，而非逐对极限

对 \(j<k\)，差脉冲在 \([t_b,\tau_j]\) 解同一个齐次伴随方程。
其能量恒等式与零延拓给
\[
 \|q_j-U(\tau_k,\tau_j)^*q_k\|_2^2
 =\|v_j(t_b)-v_k(t_b)\|_2^2+
      2\nu\int_{t_b}^{\tau_j}\|\nabla(v_j-v_k)\|_2^2
 \le\|X_j-X_k\|_{\mathcal X}^2 .
 \tag{BP.29}
\]
所以 Cauchy 尾部性质直接给
\(\sup_{k>j\ge J}\|U(\tau_k,\tau_j)^*q_k-q_j\|_2\to0\)。
固定 \(j\) 再令 \(k\to\infty\)，BP.28 对 \(t_0=\tau_j\) 的版本给
\[
 A(\tau_j)=\lim_{k\to\infty}U(\tau_k,\tau_j)^*q_k
       \text{ 强 }L^2,\qquad \|A(\tau_j)-q_j\|_2\to0.
 \tag{BP.30}
\]
没有把“每个固定 \(j\)”自动提升成统一性；统一上界已由 BP.29 先取得。

对任意收缩算子 \(C\) 与单位向量 \(x,y\)，
\(\|Cx-y\|^2\le2(1-\operatorname{Re}\langle Cx,y\rangle)\)。
用对偶及 BP.29 得
\[
 \sup_{k>j\ge J}\|U(\tau_k,\tau_j)q_j-q_k\|_2\to0.
 \tag{BP.31}
\]
由 \(1-\|z\|^2\le2\|z-y\|\)（\(\|z\|\le1,\|y\|=1\)）
和 BP.4--BP.5，再得到
\[
 \sup_{k>j\ge J}2\nu\int_{\tau_j}^{\tau_k}
       \|\nabla U(t,\tau_j)q_j\|_2^2dt\to0,\qquad
 \sup_{k>j\ge J}2\nu\int_{\tau_j}^{\tau_k}
       \|\nabla U(\tau_k,t)^*q_k\|_2^2dt\to0.
 \tag{BP.32}
\]
与 BP.12 合并还给相邻节点
\(\operatorname{Re}\langle (U-S)(\tau_{j+1},\tau_j)q_j,q_{j+1}\rangle\to1\)。
这是受约束与被动演化的算子分离，不是压力测度或压力平方范数恒等式。

## 7. 核查的范围

上述链保留原文 §§2--6 的核心条件和顺序；它没有附加 Type I、
端点紧性、临界范数或独立给定的 packet 假设。
但结果始终在 BP.2 的正原子条件下，且经过允许的子列选择。
三角统一性针对最终离散节点对，不是所有连续时间对；
\(A\) 在每个严格终点前区间属能量类，不构造 \(A(T)\in L^2\)。
局部 Hodge、Nash 和紧性/时间能量接口在这里作了直接展开；
基础 Hilbert 投影、Fourier、调和分布内部正则性、BL 的有限指数
压力工具和 BM 终端测度仍有各自明确来源，不声称全部数学基础均重新证明。

这不证明原子不可能，不生成任意奇点的原子或 BL.3 条件，
也不支付延迟二阶算子预算。§7 的二阶出口必须另行完整读审，
不能由本稿的全尾一阶梯度结论直接宣布完成。
本稿不是一般三维 NS 正则性、新颖性或 Clay 结论。
