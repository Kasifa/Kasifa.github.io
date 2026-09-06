# 局部 L³ 持留为何需要记录远场：一个平滑周期解的构造

2026-09-06。**PROVED LOCALLY / 已通过内部实际文件独立复核 / NOT CLAY。**

我检查的是一个可能用于首次奇点论证的辅助估计，不是假设已经存在奇点。
结论只否定下述“所有平滑窗口均适用、常数不支付远场”的版本。
构造中的解均光滑，初值随参数改变；没有构造 NS 奇点。
这里不宣称新颖性，也不把内部复核称为同行评审。

## 1. 要排除的准确命题

固定黏性为 1、无外力的周期方程，空间为
\(\mathbb T^3=(-\pi,\pi]^3\)，使用周期零均值压力。
所有球均为嵌入环面的欧氏球，中心为 0。
记 \(L_r(t)=\|u(t)\|_{L^3(B_r)}\)。
待检验的全窗口命题是：存在与初值、远场能量和压力无关的
\(c_0,c_1,L_0>0\)，使任何光滑解在 \(L_r(t)\ge L_0\)、
\(\delta=c_0r^2L_r(t)^{-4}<t\) 时满足

\[
 \inf_{s\in[t-\delta,t]}\|u(s)\|_{L^3(B_{2r})}
 \ge c_1L_r(t).
\tag{AA.1}
\]

**局部反例命题。** 存在一个固定的小 \(r>0\)，对任意
\(c_0,c_1,L_0>0\)，都有一个零均值、光滑无散初值产生的真实周期
NS 解及其光滑寿命内的 \(0<s<t\)，使
\(L_r(t)\ge L_0\)、\(0<\delta<t/2\)、\(s\in(t-\delta,t)\)，而
\(\|u(s)\|_{L^3(B_{2r})}<c_1L_r(t)\)。
因此即便要求整个窗口远离初始时刻到相对比例 \(\delta<t/2\)，
AA.1 仍不成立。该命题不含“靠近指定首次奇点”这一额外条件。

## 2. 远处速度产生非零局部压力梯度

取径向、非零的 \(\psi\in C_c^\infty(B_1)\)，令
\(W=(\partial_2\psi,-\partial_1\psi,0)\)。它无散、零均值，且

\[
 \int W_iW_j\,dy=m\,\operatorname{diag}(1,1,0)_{ij},
 \qquad m=\int|\partial_1\psi|^2\,dy>0.
\tag{AA.2}
\]

交叉矩为零及两个对角矩相等来自反射和旋转对称。
设周期 Green 函数 \(\mathcal G\) 满足
\(-\Delta\mathcal G=\delta_0-|\mathbb T^3|^{-1}\)。
在原点附近，\(\mathcal G=N+H\)，
\(N(x)=(4\pi|x|)^{-1}\)，\(H\) 光滑。
这由减去 Newton 核后的光滑 Poisson 方程及内部椭圆正则性得到。

取 \(z=de_3\)，先选 \(d>0\) 足够小，再选 \(0<\eta<d/16\)，
定义支撑在 \(B_\eta(z)\) 的周期光滑场
\(w(x)=\eta^{-3/2}W((x-z)/\eta)\)，球外延为零。
设 \(-\Delta q_w=\partial_i\partial_j(w_iw_j)\)，并固定压力均值为零。
在 0 点可在积分核上微分，因为两个支撑分离。于是

\[
 \nabla q_w(0)
 =m\nabla(\partial_{11}+\partial_{22})N(-de_3)
   +O_W(\eta d^{-5})+O_W(1)
 =-\frac{3m}{2\pi d^4}e_3
   +O_W(\eta d^{-5})+O_W(1).
\tag{AA.3}
\]

第一个误差由 \(D^4N=O(d^{-5})\) 的一阶 Taylor 余项给出；
第二个由固定坐标邻域内的 \(\|D^3H\|_\infty\) 给出。
先使 \(d\) 足够小以压住第二项，再使 \(\eta/d\) 足够小以压住第一项，
即可保证 \(\nabla q_w(0)\ne0\)。这些选择在后面的振幅极限中全部固定。
取 \(r=d/8\)，则 \(w=0\) 于 \(B_{3r}\) 的一个邻域。
记 \(g=\nabla q_w\)。在此邻域内
\(\Delta q_w=0\)，所以 \(\operatorname{div}g=0\)、\(\Delta g=0\)，且
\[
 G_0:=\|g\|_{L^3(B_r)}>0.
\tag{AA.4}
\]

为构造局部初值修正，定义球上的向量势
\[
 {\cal A}(x)=-\int_0^1 t\,x\times g(tx)\,dt,\qquad
 G=\operatorname{curl}(\chi{\cal A}),
\tag{AA.5}
\]
其中 \(\chi\in C_c^\infty(B_{3r})\)，在 \(B_{2r}\) 的邻域上等于 1。
恒等式
\(\operatorname{curl}(x\times g(tx))=-2g(tx)-t(x\cdot\nabla)g(tx)\)
使用了 \(\operatorname{div}g=0\)。
因此 \(\operatorname{curl}{\cal A}
=\int_0^1\partial_t(t^2g(tx))\,dt=g(x)\)。
球外延零后，\(G\) 是周期光滑、零均值、紧支撑无散场，
并在 \(B_{2r}\) 邻域上等于 \(g\)。
\(w\) 和 \(G\) 的支撑有正距离，故交叉张量
\(w\otimes G\) 和 \(G\otimes w\) 在全环面恒为零。

## 3. 黏性一致的短时 Taylor 控制

固定常数 \(a,b>0\)，稍后选定。令 \(B\to\infty\)，
\(\varepsilon=B^{-3/5}\)，\(\nu_B=B^{-1}\)。
先在快时间 \(\tau\) 解

\[
 \partial_\tau U_B+
 {\mathbb P}\operatorname{div}(U_B\otimes U_B)
 =\nu_B\Delta U_B,\qquad
 U_B(0)=w+\varepsilon bG.
\tag{AA.6}
\]

\(\mathbb P\) 为周期 Leray 投影。对足够大的 \(B\)，初值的
\(H^{12}\) 范数一致有界。这里使用经典局部光滑解理论，
但需要的寿命一致性可直接从能量法看出：

\[
 \frac{d}{d\tau}\|U_B\|_{H^{12}}^2
 +2\nu_B\|\nabla U_B\|_{H^{12}}^2
 \le C\|U_B\|_{H^{12}}^3.
\tag{AA.7}
\]

对每个多重指标微分、分部积分，最高阶输运项由无散性抵消；
其余 Leibniz 交换子由 Sobolev 乘积估计控制。投影在周期 Sobolev 空间
有界并与微分交换。丢弃非负黏性项后得到与 \(0<\nu_B\le1\)
无关的共同时间 \(\tau_0>0\) 和共同 \(H^{12}\) 上界。
可对 Fourier Galerkin 系统一致应用该估计，经紧性得到解，
由高阶能量差估计唯一；更高阶交换子估计保留光滑性。
本论证不使用边界层或未经证明的无黏极限收敛。

方程还给出一致的 \(H^{10}\) 范数控制 \(\partial_\tau U_B\)。
再对方程微分一次，由
\[
 \partial_{\tau\tau}U_B
 =\nu_B\Delta\partial_\tau U_B
 -\mathbb P\operatorname{div}
  (\partial_\tau U_B\otimes U_B+U_B\otimes\partial_\tau U_B)
\tag{AA.8}
\]
得到一致 \(H^8\) 上界，因而一致 \(C^0\) 上界。
这里至多损失四阶空间导数，常数可依赖固定的 \(w,G,a,b,r\)，
不依赖 \(B\)。

在 \(B_{2r}\) 上，初始黏性项为零，因为 \(w=0\) 且 \(\Delta G=0\)。
交叉张量全局为零，初始压力恰为
\(q_w+\varepsilon^2b^2q_G\)。
压力约定给
\(\mathbb P\operatorname{div}(w\otimes w)=\nabla q_w=g\)
于 \(B_{2r}\)；不能把这一非局部项删掉。
因此

\[
 U_B(\tau,x)=\varepsilon b g(x)-\tau g(x)
             +O_{C^0(B_{2r})}(\tau^2+\tau\varepsilon^2)
 \quad(0\le\tau\le\tau_0).
\tag{AA.9}
\]

这是带一致余项的 Taylor 定理，不是形式无黏近似。
热传播的远处贡献包含在该余项内。

## 4. 回到黏性为 1 的真实 NS 解

定义
\[
 u_B(t,x)=B\,U_B(Bt,x),\qquad
 p_B(t,x)=B^2q_{U_B}(Bt,x).
\tag{AA.10}
\]
因 \(\nu_B=B^{-1}\)，它们精确满足
\(\partial_tu_B+(u_B\cdot\nabla)u_B+\nabla p_B=\Delta u_B\)。
压力仍周期、零均值，没有外力或非周期仿射压力。
这是改变振幅、时间及辅助黏性的恒等变换，不是固定环面的空间缩放。
解在 \(0\le t\le\tau_0/B\) 光滑，在该寿命内满足全环面的能量等式。

取
\[
 s_B=bB^{-8/5},\qquad t_B=(b+a)B^{-8/5}.
\tag{AA.11}
\]
这两个时刻远小于共同物理寿命 \(\tau_0/B\)。
AA.9 给
\[
 \|u_B(s_B)\|_{L^3(B_{2r})}=O(B^{-1/5}),\qquad
 L_B:=L_r(t_B)=aG_0B^{2/5}+O(B^{-1/5}).
\tag{AA.12}
\]
第一式是在压力加速度抵消初始局部速度的时刻；
再过 \(aB^{-8/5}\) 时间，局部速度反向增大。
两式使用的是原速度，而非人为减去随时间变化的背景速度。

给定 AA.1 的任意 \(c_0,c_1,L_0>0\)，选
\[
 a^5=\frac{c_0r^2}{2G_0^4},\qquad b=10a.
\tag{AA.13}
\]
则
\[
 \delta_B:=c_0r^2L_B^{-4}
 =(2a+o(1))B^{-8/5},\qquad
 \frac{\delta_B}{t_B}\longrightarrow\frac2{11},\qquad
 t_B-s_B=aB^{-8/5}.
\tag{AA.14}
\]
足够大 \(B\) 下，\(0<\delta_B<t_B/2\)，且
\(s_B\in(t_B-\delta_B,t_B)\)。
同时 \(L_B\to\infty\)，而
\[
 \frac{\|u_B(s_B)\|_{L^3(B_{2r})}}{L_B}
 =O(B^{-3/5})\longrightarrow0.
\tag{AA.15}
\]
最终 \(L_B\ge L_0\) 且该比值小于 \(c_1\)，严格违反 AA.1。
局部反例命题得证。

## 5. 结论不能越过的边界

1. 这是实际平滑 NS 解对一个普适辅助估计的反例，
   不只是任意时钟或不满足方程的运动学模型。
2. 初始全局能量随 \(B\) 增长。没有否定依赖初始能量、
   远场压力、临界上界或其他额外成本的版本。
3. 所用时刻接近各解的初始时间，且 \(t_B/r^2\to0\)，但整个反向窗严格
   位于正时间，甚至 \(\delta_B<t_B/2\)。
   没有否定额外要求 \(t\ge Cr^2\) 的局部成熟时间版本。
   没有证明在一个固定解的指定首次奇点附近
   也存在这种抵消。因此仅限首次奇点的持留命题仍是 OPEN。
4. 原合同 G 的尺度依赖路径、完整能量柱体和 G-P/G-C 均未由此解决。
   固定球证明不能自动变成原移动路径的证明。
5. 若首次奇点附近真有 AA.1 型固定球全窗口持留，则结合该球
   \(L^3\) 完整极限发散与能量类的 \(L_t^4L_x^3\) 可积性，会产生矛盾：
   每个长度 \(c_0r^2L_r(t)^{-4}\) 的晚窗口支付至少
   \(c_0c_1^4r^2\) 的 \(L_t^4L_x^3(B_{2r})\) 积分，而窗口趋向终点，
   可积函数的尾积分趋零。这个观察表明该条件很强，不能当作廉价辅助引理。

## 6. 固定解的远场压力冲量反而可单独支付

不能把上面的变初值族直接解释为固定解在首次奇点附近的机制。
对一个固定的周期解，令
\(M=\sup_{0<t<T_*}\|u(t)\|_2<\infty\)，固定同样的小 \(r\)。
取 \(0\le\theta\le1\)，\(\theta\in C_c^\infty(B_{4r})\)，
在 \(B_{3r}\) 上等于 1，定义精确压力分解中的远源项

\[
 q_{\rm far}(t)
 =\partial_i\partial_j\mathcal G*
       ((1-\theta)u_i(t)u_j(t)).
\tag{AA.16}
\]

它在 \(B_{3r}\) 调和。对 \(x\in B_{2r}\)，积分中的源距 \(x\)
至少为 \(r\)。周期核的三阶导数至多为
\(C(\operatorname{dist}(x,y)^{-4}+1)\)，因 \(r<1\)，有

\[
 \|\nabla q_{\rm far}(t)\|_{L^\infty(B_{2r})}
 \le C r^{-4}M^2,\qquad
 \|\nabla q_{\rm far}(t)\|_{L^3(B_{2r})}
 \le C r^{-3}M^2 .
\tag{AA.17}
\]

球体积的立方根贡献一个 \(r\)。因此对任何合法窗口
\(\delta=c_0r^2L_r(t)^{-4}<t\)，

\[
 \sup_{s\in[t-\delta,t]}
 \frac{\left\|\int_s^t\nabla q_{\rm far}(\sigma)\,d\sigma
             \right\|_{L^3(B_{2r})}}{L_r(t)}
 \le Cc_0M^2 r^{-1}L_r(t)^{-5}.
\tag{AA.18}
\]

固定 \(M,r\) 时，若该球 \(L_r(t)\to\infty\)，右侧趋零。
这只控制远源压力的积分，不控制
\(\Delta u\)、近源压力、非线性输运或原移动路径上的完整能量。
不能从 AA.18 单独推出 AA.1。反例族没有矛盾：
其初始能量范数 \(M_B\) 量级为 \(B\)，而 \(L_B\) 量级为 \(B^{2/5}\)，
故 \(M_B^2L_B^{-5}\) 不趋零。
对缩球 \(r=r(t)\)，还必须支付 \(r^{-1}L_r(t)^{-5}\)，
固定球极限不自动给这一速率。

## 7. 来源与查新范围

首次奇点固定球输入及其排字解释见同批
clay_b_concentration_path_limits_20260906.md。
AA.2--AA.18 在这里给出本地证明；经典周期局部解理论、Leray 投影、
Sobolev 乘积估计和 Green 函数局部结构不是新工具。
黏性一致能量法另与
[Tao 的 2018 年局部适定性讲义，Theorem 1 及其证明](https://terrytao.wordpress.com/2018/10/09/254a-notes-3-local-well-posedness-for-the-euler-equations/)
核对。该来源明确说明全空间写法可移到周期域；这里仍写出实际使用的
周期投影和高阶估计，不把讲义当成全局正则性定理。
本轮检索了局部集中、远场压力和黏性一致局部寿命相关原始来源，
没有完成针对本反例表述的穷尽查新，不声称首创、可发表等级或 Clay 进展。

本节是纯解析结果：没有有限计算、仿真、DGX、科学图或新读者 PDF。
