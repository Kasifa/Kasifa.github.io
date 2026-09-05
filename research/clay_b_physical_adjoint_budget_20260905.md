# 物理时间伴随测试：弱端点与线性耗散定位代价

2026-09-05。接续 A.1--A.6 工作稿。
状态：本地解析证明；独立文件审查以配套 audit 为准。
**G OPEN / NOT CLAY；不声明文献新颖性。**

## 1. 问题和量词

在固定的 \(2\pi\)-周期三维环面上，黏性归一为 1，无外力。
先取光滑真实 NS 解；第 2 节另给 suitable Leray--Hopf 版本。
固定原合同的空间平滑核 \(\varphi\)，记 \(b_R=S_Ru\)。
固定 \(0<R<\pi/16\)、\(0\le s<T\)、\(T-s\le64R^2\)。
这些估计并不要求 T 是首次奇点；也没有利用这样的特殊条件。
终端测试为单个紧支撑函数的周期化：
\(\psi_R(x)=\psi((x-x_*)/R)\)，其中
\(0\le\psi\le1\)、\(\psi=1\) 于 \(B_1\)、\(\operatorname{supp}\psi\subset B_2\)。

令 \(\chi\) 解

\[
 \chi_t+\Delta\chi+b_R\cdot\nabla\chi=0,\qquad \chi(T)=\psi_R.
\tag{B.1}
\]

最大值原理和不可压缩性给 \(0\le\chi\le1\) 与
\(\int_{\mathbb T^3}\chi=R^3\int_{\mathbb R^3}\psi=:M\)。
系数依赖 u 不妨碍测试：每个给定解和固定 R 都先确定一个确定性的测试。
这不产生任何尺度一致的常数。

## 2. 保留早期支付的能量式

记 \(e=|u|^2/2\)。光滑解严格满足

\[
\begin{split}
 \int\psi_R e(T)+\int_s^T\!\!\int\chi|\nabla u|^2
 =\int\chi(s)e(s)
 +\int_s^T\!\!\int
 \{e(u-b_R)+(p-c(t))u\}\cdot\nabla\chi .
\end{split}
\tag{B.2}
\]

这是将 (B.1) 代入原局部能量等式的结果。
\(\int c(t)u\cdot\nabla\chi=0\) 来自周期分部积分。
早期加权能量、残余输运、压力功都没有消失。
再乘一个时间 cutoff 会引入额外时间导数项，不属于 (B.2) 的免费操作。

弱版本明确假设 u 是 **suitable** Leray--Hopf 解，
\(u\in C_w([0,T];L^2)\cap L^2(0,T;H^1)\)，满足分布局部能量不等式。
不把任意 Leray--Hopf 解的 suitability 当成这里已证的事实。
起点 s 取右侧强 \(L^2\) Bochner Lebesgue 点，即

\[
 \lim_{h\downarrow0}\frac1h\int_s^{s+h}
       \|u(t)-u(s)\|_2^2\,dt=0 .
\tag{B.3}
\]

这样的点几乎处处存在；s=0 可用强初始迹替代。
终点 T 可取弱连续代表中的任意时刻。
对周期压力取零均值代表；加回可积时间 gauge 不影响结果。
那么

\[
 \int\psi_R e(T)+\int_s^T\!\!\int\chi|\nabla u|^2
 \le\int\chi(s)e(s)
 +\int_s^T\!\!\int
 \{e(u-b_R)+pu\}\cdot\nabla\chi .
\tag{B.4}
\]

证明的端点细节如下。固定 R 后，空间卷积将有界弱连续 L² 曲线
变成时间连续、空间任意阶光滑的 \(b_R\) 曲线：
卷积算子从 L² 到每个固定 \(C^k\) 是紧算子。
因此 \(\chi\) 有固定 R 下有界的所需空间导数，可以用光滑时间逼近
和非负时间斜坡代入局部能量不等式。
能量类给 \(u\in L^{10/3}\)、\(p\in L^{5/3}\)，故三次项和 pu 可积。
这里的时空范数都在有限窗口与固定环面上。

更明确地，局部能量缺陷
\(\mu=-[\partial_t e-\Delta e+\operatorname{div}((e+p)u)+|\nabla u|^2]\)
是非负 Radon 测度。令 \(f(t)=\int\chi(t)e(t)\) 的几乎处处值，
则其分布导数是

\[
 df=\left[\int\{e(u-b_R)+pu\}\cdot\nabla\chi
                  -\int\chi|\nabla u|^2\right]dt-\int_x\chi\,d\mu .
\tag{B.5}
\]

在所取窗口有相应的单侧 BV 迹。
(B.3) 识别 \(f(s+)=\int\chi(s)e(s)\)；
弱下半连续性仅给 \(\int\psi_Re(T)\le f(T-)\)。
将 (B.5) 积分于开区间 (s,T)，即得 (B.4)；
事实上左侧还可加上 \(\int_{(s,T)\times\mathbb T^3}\chi\,d\mu\)。
此写法不收取端点原子。
非负缺口 \(f(T-)-\int\psi_Re(T)\) 不在此被识别为 \(\mu(\{T\}\times\mathbb T^3)\)。
不能在没有 (B.3) 或等价强迹条件时，把任意弱起点能量放在右侧。

## 3. 二阶矩：用振荡替代 Lipschitz 指数

先在 \(\mathbb R^3\) 上取单个终端紧支撑提升，周期延拓 \(b_R\)。
设 \(\sigma=T-t\)。提升密度 \(\rho\) 和路径中心 Y 满足

\[
 \rho_\sigma=\Delta\rho+\operatorname{div}(b_R(T-\sigma)\rho),
 \quad \rho(0)=\psi_R,\qquad
 Y'=-b_R(T-\sigma,Y),\quad Y(0)=x_* .
\tag{B.6}
\]

周期化 \(\rho\) 后得到 \(\chi(T-\sigma)\)。
Y 是原合同路径 \(X_R(T-\sigma)\) 的连续提升。
注意 Fokker--Planck 漂移是 **负** \(b_R\)。
下面的 Q 是单个提升的欧氏二阶矩，不是把周期密度在全空间重复积分。
令

\[
 Q(\sigma)=\int_{\mathbb R^3}|x-Y(\sigma)|^2\rho(\sigma,x)\,dx,
 \qquad D_J=\int_s^T\|\nabla u(t)\|_2^2dt .
\tag{B.7}
\]

**命题。** 常数仅依赖固定核、测试形状和固定环面，有

\[
 \boxed{\quad
 \sup_{0\le\sigma\le T-s}\frac{Q(\sigma)}{MR^2}
 \le C_{\psi,\varphi}\left(1+\frac{D_J}{R}\right).
 \quad}
\tag{B.8}
\]

该结论在上述能量类下也成立，不要求局部能量不等式；
固定 R 的系数有界且空间 Lipschitz，随机微分方程良定。
令 \(Z_0\) 的概率密度为 \(\psi_R/M\)，与三维 Brownian 运动 W 独立，
并解

\[
 dZ_\sigma=-b_R(T-\sigma,Z_\sigma)d\sigma+\sqrt2\,dW_\sigma .
\tag{B.9}
\]

其密度为 \(\rho/M\)。减去 Y 的方程，并在概率空间用 Minkowski：

\[
 \sqrt{Q(\sigma)/M}
 \le \sqrt{Q(0)/M}+\sqrt{6\sigma}
       +\int_0^\sigma \operatorname{osc}_x b_R(T-r)\,dr .
\tag{B.10}
\]

这里 \(\operatorname{osc}b=\sup_{x,y}|b(x)-b(y)|\)，
没有把随机轨道与确定性轨道的距离再放回右侧。
令 \(\bar u\) 为空间均值。Young 和环面 Sobolev--Poincare 给

\[
 \operatorname{osc}b_R
 \le2\|S_R(u-\bar u)\|_\infty
 \le C_\varphi R^{-1/2}\|u-\bar u\|_6
 \le C_\varphi R^{-1/2}\|\nabla u\|_2 .
\tag{B.11}
\]

其中核的 \(L^{6/5}\) 尺度为 \(R^{-1/2}\)；
对周期核使用同一小尺度上界，常数容纳固定核的支撑。
故

\[
 \int_0^\sigma\operatorname{osc}b_R(T-r)\,dr
 \le C_\varphi R^{-1/2}\sqrt{\sigma D_J}
 \le C_\varphi R^{1/2}\sqrt{D_J}.
\tag{B.12}
\]

初始 \(Q(0)/M\le4R^2\)、\(\sigma\le64R^2\)。
将三项平方用 \((a+b+c)^2\le3(a^2+b^2+c^2)\) 即得 (B.8)。
减去均值消除了均匀平移带来的虚假代价；无需假设 \(\bar u=0\)。
由 Chebyshev 不等式还有

\[
 \frac1M\int_{|x-Y(\sigma)|>\lambda R}\rho(\sigma,x)\,dx
 \le \min\left\{1,\frac{C_{\psi,\varphi}(1+D_J/R)}{\lambda^2}\right\}.
\tag{B.13}
\]

这改进了 A.5--A.6 的指数上界，但只是质量尾部控制。
没有给原移动球内 \(\chi\ge c>0\) 的统一点态下界。
有限总耗散不能保证 \(D_J/R\) 沿指定可能奇点有界或趋零。
本节不声称 (B.8) 的 R 依赖最优，也不从粗上界反推核必然失去定位。

## 4. 核高度不等于原能量控制

对不可压缩漂移，标准 Nash 方法给漂移无关的密度高度上界。
全空间的一般常数版本见 Ryzhik 的 Theorem 2.2；
时间依赖、全空间的更强集中度比较见 Hess-Childs--Raquépas--Rowan 的
Theorem 1.7。这些都是文献事实，不是本节原创。
精确出处和适用域见配套 report-source。

在当前固定环面上直接用带常数模态修正的 Nash 不等式、L² 能量恒等式、
对偶性及演化族的中间时刻复合，可得

\[
 \|U(\sigma,0)\|_{L^1(\mathbb T^3)\to L^\infty(\mathbb T^3)}
 \le C_{\mathbb T^3}(1+\sigma^{-3/2}) .
\tag{B.14}
\]

此处 U 为时间依赖系数的演化族，不写成自治半群的时间幂；
其反向伴随仍为不可压缩漂移，故 L¹ 到 L² 的估计可对偶使用。
不能把全空间的纯常数上界逐个周期镜像相加。
当 \(\sigma\) 与 \(R^2\) 可比、输入质量为 \(M\asymp R^3\)，
(B.14) 仅给 \(\|\chi\|_\infty=O(1)\)，不指定质量的位置。
更不能据此转出原合同要求的 \(B_{8R}\) 能量控制；
本节 B1/B2 终端形状尚非那个完整移动管的支配测试。

免费的梯度信息仅有密度能量估计

\[
 \int_0^{T-s}\|\nabla\rho(\sigma)\|_2^2\,d\sigma
 \le\tfrac12\|\psi_R\|_2^2=C_\psi R^3 .
\tag{B.15}
\]

提升和周期版本各自成立，不能把两者的 L² 范数等同。
直接微分方程则再次出现 \(\nabla b_R\)：
\(w_\sigma=\Delta w+b_R\cdot\nabla w+(\nabla b_R)^Tw\)，
其中 \(w=\nabla\rho\)，时间参数按 (B.6)。
其 L² 能量估计含 \(\|\nabla b_R\|_\infty\|w\|_2^2\)。
这说明这一微分估计要支付漂移形变，未证明任何梯度估计都必须这样付。

若只使用能量类，残余项与压力项的直接 Holder 预算是

\[
 \left|\int_s^T\!\!\int
       \{e(u-b_R)+pu\}\cdot\nabla\chi\right|
 \le C\left(\|u\|_{10/3}^3+
            \|p\|_{5/3}\|u\|_{10/3}\right)\|\nabla\chi\|_{10}.
\tag{B.16}
\]

理由是 \(u^3,pu\in L^{10/9}\)，且 \(S_R\) 是各时刻的 \(L^{10/3}\) 收缩。
固定 R 下右侧有限；没有获得随着 R 缩小可用的小常数。
(B.15) 的 \(L^2\) 梯度不能直接替代 (B.16) 所需的 \(L^{10}\)。
这是该直接 Holder 方法的指数缺口，不是排除压力结构、对偶空间
或其他补偿估计的定理。

## 5. 本节究竟改变了什么

已完成：合法弱终点的测试不等式，以及不依赖 Lipschitz 指数的
线性归一化耗散二阶矩控制。真实 NS 的无免费漂移代价检验另见 shear 稿。
没有完成：指定首次奇点的好尺度 G、原移动管内的统一下界、
压力/残余项的临界闭合，或任何新的全局正则性类。
这些伴随核估计主要只用不可压缩性与能量空间，
并非已经找到区分真实 NS 与 averaged-NS 的闭合机制。

下一步不再仅优化核高度：转向原合同 R.216--R.217 的时间持留和
上穿条件，先审查是否能从有符号真实 NS 预算产生相应计时约束。
这是待研究的问题，不作为本节结论。
