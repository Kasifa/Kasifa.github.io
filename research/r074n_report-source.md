# R0.74N｜把所有壳层合起来，完整领圈条件闭合了

## 导语

这一节仍然没有解决三维 Navier--Stokes 千禧年问题。

R0.74L 处理了主壳 \(k=j\)，R0.74M 处理了最近内壳
\(k=j-1\)。原先看起来，我还需要沿着
\(j-2,j-3,\ldots\) 一行一行补齐随机桥估计。

这一节的关键变化，是不再逐行追赶。我把所有内壳的正部弦长放进
同一个和里。超高斯壳权使这个和一致有界，而全部内壳的联合支撑仍
落在 R0.74M 已经排出的那根内管中。外壳则走另一条更直接的路：对
真实周期包取绝对值，再用超高斯壳权一次收掉无限尾。

因此，我在 R0.74F--H 构造的这个精确、光滑、周期、无外力解族上
证明了完整的 R0.74K 有符号领圈条件。再把这一步与 R0.74H 定理
5.1、R0.74J 的完整支付律及 R0.74F 的端点动能下界合并，我得到

\[
 X_j\asymp\mathfrak C_j
 \asymp B_j^2L_jR_j^2
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.
\]

这是既有结果的跨笔记证明合成，没有加入新的随机引理。它仍然只是
冻结精确解族上的结论；普适端点不等式、任意流领圈控制和任意三维
解的正则性都没有得到。

**NOT CLAY.**

## 1. 还缺的不是一行，而是一个无限和

完整对象是

\[
 \mathcal I_j(\tau)
 =\sum_{k\ge1}\Gamma_k
 \int_{61R_j^2}^{\tau}\eta_{R_j}(t)
 \int_{\mathbb R^3}
 \theta_j\widetilde F_j^2\partial_2\psi_k^{R_j}
 \,dx\,dt,
\]

其中

\[
 \Gamma_k=e^{-4^{k-1}/32},\qquad
 c_\gamma=\frac8{3969},\qquad \rho=\frac1{320},
\]

\[
 \Gamma_j=e^{-c_\gamma L_j^2},\qquad
 R_j=e^{-\rho L_j^2}.
\]

我把它精确拆成三块：

\[
 \mathcal I_j=\mathcal I_<+\mathcal I_=+\mathcal I_>,
\]

\[
 \mathcal I_<=\sum_{k=1}^{j-1}\mathcal J_{j,k},\qquad
 \mathcal I_=\mathcal J_{j,j},\qquad
 \mathcal I_>=\sum_{k=j+1}^{\infty}\mathcal J_{j,k}.
\]

三块互不重叠，也没有漏掉任何 \(k\ge1\) 的壳层。

R0.74L 已经给出主壳的绝对估计

\[
 \sup_{\tau\in I_{R_j}}|\mathcal I_=(\tau)|
 \le C\Gamma_jL_jR_j^5.
\]

真正的新工作只有两件：把所有内壳一次合成，以及把所有外壳绝对
求和。

## 2. 所有内壳只留下一个有界弦长

对每个内壳，我先取原始有符号 integrand 的正部，再定义联合弦长

\[
 D_<(t,x_2,x_3)
 =\sum_{k=1}^{j-1}\Gamma_k
 \int_{\mathbb R}
 [\theta_j(t,x_3)\partial_2\psi_k^{R_j}(x)]_+\,dx_1.
\]

这是一个故意偏大的量。它不使用壳层之间的抵消。

第 \(k\) 个双面平滑领圈的 \(x_1\) 弦长至多是 \(C2^kR_j\)，
而导数大小至多是 \(C/R_j\)。所以

\[
 \int_{\mathbb R}
 [\theta_j\partial_2\psi_k^{R_j}]_+\,dx_1
 \le C2^k.
\]

壳权随 \(4^k\) 超高斯衰减，于是

\[
 \boxed{
 0\le D_<
 \le C\sum_{k\ge1}2^k e^{-4^{k-1}/32}
 =:C_*<\infty.}
\]

右端与 \(j\) 无关。R0.74M 处理单个 \(j-1\) 壳时，弦长上界是
\(CL_j\)；把壳权放进联合弦长以后，整个内壳和反而只剩一个常数。

更重要的是，所有内壳的联合支撑仍在最大的 \(j-1\) 领圈以内：

\[
 r_-=2^jR_j+\frac{R_j}{8}
 =\left(\frac{32}{63}L_j+\frac18\right)R_j.
\]

当 \(j\) 足够大时，\(r_-<1\)。二维周期化后，每个环面点至多遇到
一个 lift；我没有挑选中心周期副本，也没有丢掉其他绕行。

## 3. R0.74M 的排出机制可以一次作用于整个内壳和

联合弦长一旦非零，终点仍满足

\[
 |h_j+X_t|_{\rm lift}\le r_-.
\]

在最后一小段长度 \(R_j^2/64\) 的物理时间里，考虑布朗模量事件

\[
 \mathcal H_t=
 \left\{
 \sup_{t-R_j^2/64\le s\le t}
 |\widetilde X_s-\widetilde X_t|
 \le\frac1{16}L_jR_j
 \right\}.
\]

反射估计给出

\[
 \mathbb P(\mathcal H_t^c)
 \le4e^{-L_j^2/16}.
\]

在好事件上，支撑和布朗模量把整段路径留在

\[
 |h_j+X_s|_{\rm lift}\le\frac35L_jR_j
\]

内。这里仍然有 R0.74M 的正热缺陷，所以剪切位移满足

\[
 \mathfrak S_t^\leftarrow[X]\ge
 \Sigma_{L_j},\qquad
 \Sigma_{L_j}=2^{-15}e^{-L_j^2/640}.
\]

而

\[
 \frac{\Sigma_{L_j}}{L_jR_j}
 =\frac{e^{L_j^2/640}}{32768L_j}\longrightarrow\infty.
\]

因此，领圈支撑迫使横向导数热核在

\[
 \operatorname{dist}_{\mathbb T}(u,0)
 \ge\frac12\Sigma_{L_j}
\]

处取值，得到关于 \(L_j\) 的超高斯尾。

坏路径的账本现在是

\[
 CR_j^4e^{-L_j^2/16}.
\]

它需要支付目标权 \(\Gamma_j\) 和额外一个 \(R_j\)。精确余量是

\[
 \boxed{
 \frac1{16}-\frac1{320}-\frac8{3969}
 =\frac{72851}{1270080}>0.}
\]

好路径的账本是

\[
 CR_j^3
 \exp\!\left[-
 \frac{e^{L_j^2/320}}{1056\cdot32768^2}
 \right],
\]

这个双指数小量可以支付 \(\Gamma_jR_j^2\)。于是

\[
 \boxed{
 \sup_{\tau\in I_{R_j}}[\mathcal I_<(\tau)]_+
 \le C\Gamma_jL_jR_j^5.}
\]

两个包和交叉项仍由反演对称性与四倍安全上界控制，不使用包间
抵消。

## 4. 外壳不需要随机桥细节

对外壳，我使用的是绝对估计。

初始包由一个导数热核和一个热核组成：

\[
 R_j^3\partial K_{R_j^2}K_{R_j^2}.
\]

三个 \(R_j\) 次幂正好抵消
\(\|\partial K_{R_j^2}\|_\infty\sim R_j^{-2}\) 与
\(\|K_{R_j^2}\|_\infty\sim R_j^{-1}\)。标量最大值原理因此给出

\[
 \|F_j(t)\|_\infty\le C.
\]

第 \(k\) 个完整双面领圈满足

\[
 \int_{\mathbb R^3}|\partial_2\psi_k^{R_j}|\,dx
 \le C4^kR_j^2.
\]

时间长度至多是 \(4R_j^2\)，所以

\[
 |\mathcal I_>(\tau)|
 \le CR_j^4\sum_{k\ge j+1}4^k\Gamma_k.
\]

相邻项之比是

\[
 4\exp\!\left(-\frac{3\cdot4^{k-1}}{32}\right),
\]

最终小于 \(1/2\)。因此尾和由第一项控制：

\[
 \sum_{k\ge j+1}4^k\Gamma_k
 \le C4^{j+1}\Gamma_{j+1}.
\]

利用

\[
 4^{j+1}=\frac{4096}{3969}L_j^2,
 \qquad
 \frac{\Gamma_{j+1}}{\Gamma_j}
 =e^{-3c_\gamma L_j^2},
\]

只剩下一个指数余量：

\[
 \boxed{
 3c_\gamma-\rho
 =\frac{1237}{423360}>0.}
\]

所以

\[
 \boxed{
 \sup_{\tau\in I_{R_j}}|\mathcal I_>(\tau)|
 \le C\Gamma_jL_jR_j^5.}
\]

这里是在整个 \(\mathbb R^3\) 壳层上使用周期延拓的统一上界，所有
周期副本都已经计入。尾和绝对收敛，也同时证明了有限壳层截断
\(N\to\infty\) 的合法性。

## 5. 完整领圈条件与跨笔记结论

### 5.1 领圈通量

把内壳、主壳和外壳三块合起来，我得到：

\[
 \boxed{
 \sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+
 \le C\Gamma_jL_jR_j^5.}
\]

这是 R0.74K (4.3) 的完整条件，适用于冻结的精确解族。

R0.74K 的充分性定理把它转换为领圈通量上界：

\[
 \mathfrak C_j\le CB_j^2L_jR_j^2.
\]

再与 R0.74H 的下界及 R0.74J 的尺度识别合并：

\[
 \boxed{
 \mathfrak C_j
 \asymp B_j^2L_jR_j^2
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.}
\]

因此，平方根对数尺度在这个领圈通量可观测量上既不是单边下界，
也不是数值现象，而是一个解族内的匹配渐近律。

### 5.2 加权动能—耗散量

把共同尺度记成

\[
 T_j:=B_j^2L_jR_j^2.
\]

R0.74H 定理 5.1 已经证明

\[
 X_j\le C\left(P_j^{2/3}+\mathfrak C_j\right).
\]

R0.74J 给出 \(P_j\asymp B_j^3R_j^3\)，所以

\[
 P_j^{2/3}\asymp B_j^2R_j^2\le T_j
\]

对充分大的 \(j\) 成立。本节刚刚证明
\(\mathfrak C_j\le CT_j\)，故 \(X_j\le CT_j\)。另一方面，R0.74F
的两包存活定理在本节冻结的振幅选择下给出

\[
 \mathcal U_{{\rm ext},j}^{\infty}\ge cT_j.
\]

利用

\[
 X_j=\mathcal U_{{\rm ext},j}^{\infty}
     +\mathcal D_{{\rm ext},j},
 \qquad \mathcal D_{{\rm ext},j}\ge0,
\]

我得到更细的分量边界

\[
 \boxed{
 cT_j\le\mathcal U_{{\rm ext},j}^{\infty}
 \le X_j\le CT_j,}
\]

\[
 \boxed{0\le\mathcal D_{{\rm ext},j}\le CT_j.}
\]

第二行只有上界；这里没有证明
\(\mathcal D_{{\rm ext},j}\ge cT_j\)，也没有证明任何其他匹配耗散
下界。结合领圈通量律和 R0.74J 的尺度识别，完整的精确族结论是

\[
 \boxed{
 X_j\asymp\mathfrak C_j
 \asymp B_j^2L_jR_j^2
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.}
\]

这一步只调用 R0.74H 定理 5.1、R0.74J、R0.74N 与 R0.74F 的既有
结论；它是确定性的跨笔记推论，不需要新的随机桥或随机表示引理。

## 6. 证据等级

### PROVED

- 全部内壳的联合正部估计；
- 主壳的继承绝对估计；
- 全部外壳的绝对尾和；
- 完整 R0.74K 有符号条件；
- 精确解族上的匹配领圈通量律；
- 跨笔记推出的 \(X_j\) 匹配律与分量上界。

### INDEPENDENT ANALYTIC AUDIT

独立重建逐项检查正部、四倍安全因子、联合弦长、联合支撑、
R0.74M 排出机制的继承、外壳最大值原理、双面领圈体积、无限和及
\(N\to\infty\)。其结论只绑定本节最终源文件，不扩大定理范围。

### INHERITED

- R0.74F--H 的精确光滑周期无外力解族；
- R0.74F 的端点外部动能分量下界；
- R0.74H 定理 5.1 的有符号通量闭合式；
- R0.74L 的共同前向概率律和主壳绝对估计；
- R0.74M 的热缺陷、最后布朗段与排出尺度；
- R0.74H 的领圈通量下界；
- R0.74J 的完整支付律与尺度识别；
- R0.74K 的充分性归约。

### FINITE

精确证书只核对有理常数、指数余量、离散尾和比率、
\(4^{j+1}/L_j^2\) 和原始 \(R_j\) 幂次账本。独立 Ruby 版本从原始
常数重算，并对冻结 JSON 做失效关闭的 SHA-256 绑定。

这些有限行不证明共同前向概率律、热核尾、最大值原理或完整解析
定理。

### LITERATURE BOUNDARY

限定范围的一手文献检索找到了加权 Navier--Stokes 能量估计、局部
能量聚合、剪切增强耗散和随机路径方法的先例，没有找到直接包含
本节精确平滑壳权、端点相关桥和全壳层有符号通量的定理。

有限未命中不是新颖性、优先权或可发表性的证明。

### OPEN

- 任意光滑三维 Navier--Stokes 解的普适平方根对数端点不等式；
- 任意流上的全壳层有符号领圈控制；
- payment-to-admissibility 控制；
- 指定点 core-from-shell 控制；
- 任意三维初值的奇点形成或排除；
- 全局存在与光滑性，即 Clay 千禧年问题；
- 新颖性和优先权。

## 7. 这一步的意义

R0.74K 把完整领圈条件留成了一个无穷壳层问题。R0.74L 和 R0.74M
分别关掉了两个最显眼的局部障碍。R0.74N 说明，剩余壳层不必继续
逐行制造更复杂的随机桥定理：内侧利用权重可和性与同一支撑管一次
合并，外侧利用真实包的一致上界与超高斯尾一次求和。

因此，这条构造路线现在在自身内部得到完整、匹配、可审计的
领圈通量与 \(X_j\) 尺度。这里的“完整”只指该解族的全部壳层，
不指任意流，更不指 Navier--Stokes 正则性问题。

下一道真正不同的门槛，已经不是这个精确族的 \(X_j\) 匹配上界。
它是把全壳层领圈控制移到任意流，或者建立
payment-to-admissibility 与指定点 core-from-shell 机制。只有越过
这些门槛，才可能讨论普适端点估计；本节没有越过它们。

**NOT CLAY.**
