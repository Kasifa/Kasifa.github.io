# R0.74O｜自由振幅否定了标量平方根对数端点

## 导语

这一节仍然没有解决三维 Navier--Stokes 千禧年问题。

R0.74N 在一个冻结的精确解族上得到

\[
 X_j\asymp\mathfrak C_j
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.
\]

那是一条解族内的匹配律。它说明平方根对数尺度可以被达到，却不
说明所有光滑解都受这个尺度控制。

R0.74O 检查了这两句话之间的缺口。我没有更换流动几何，也没有做
数值仿真。我只使用原精确解中一直存在、但此前固定住的被动分量
振幅。结果是：完整标量支付量仍停留在背景剪切尺度，而端点量与正
领圈通量随该振幅的平方增长。

由此，我得到一条真正的否定性结论：对既定的局部支付量
\(P_R^\alpha\)，普适上界

\[
 \mathfrak C_R^\alpha
 \lesssim (P_R^\alpha)^{2/3}
 \sqrt{1+\log_+P_R^\alpha}
\]

是假的；同一反例也否定对应的 \(X_R^\alpha\) 上界。

更精确地，在一列光滑、周期、均值为零、无外力的精确解上，

\[
 \boxed{
 X_{R_j}^{\alpha,*}
 \asymp\mathfrak C_{R_j}^{\alpha,*}
 \asymp
 (P_{R_j}^{\alpha,*})^{8024/11907}
 (1+\log_+P_{R_j}^{\alpha,*})^{7/6},
 \qquad \alpha\in\{M,F\}.}
\]

这否定的只是“右端只看一个冻结标量支付量”的估计。它没有否定带
时间集中、几何、BV、Carleson、压力或通量等额外可观测量的定理，
也没有构造奇点。

**NOT CLAY.**

## 1. 饱和不是普适上界

R0.74H 已经给出有符号通量闭合式

\[
 X_R^\alpha
 \le C\left[(P_R^\alpha)^{2/3}
 +\mathfrak C_R^\alpha\right],
 \qquad \alpha\in\{M,F\}.
\]

同时，绝对领圈估计只有线性尺度

\[
 \mathfrak C_R^\alpha\le CP_R^\alpha.
\]

在小支付区 \(P_R^\alpha\le1\)，线性上界自动强于
\((P_R^\alpha)^{2/3}\)。困难一直在大支付区。

R0.74N 的归一化振幅恰好产生

\[
 \mathfrak C_j\asymp
 P_j^{2/3}\sqrt{1+\log_+P_j}.
\]

但一个例子达到某条曲线，只能证明该曲线不能随意降低；它不能证明
所有例子都在曲线下方。要检验普适性，必须把同一几何中尚未支付的
自由度放开。

这一步的自由度就是被动分量的振幅。

## 2. 精确解允许一个真正自由的振幅

保留 R0.74F--N 的常数

\[
 \rho=\frac1{320},\qquad
 c_\gamma=\frac8{3969},\qquad
 L=L_j=\frac{63}{32}2^j,
\]

\[
 R=e^{-\rho L^2},\qquad
 \Gamma=e^{-c_\gamma L^2},\qquad
 BR^2\longrightarrow\frac1{128}.
\]

令 \(F\) 为成对被动包，\(\theta\) 为奇热剪切。对每个常数振幅
\(\mathfrak a>0\)，场

\[
 u^{(\mathfrak a)}=(\mathfrak a F,B\theta,0),
 \qquad p^{(\mathfrak a)}=0
\]

都是精确的光滑周期无外力 Navier--Stokes 解。原因不是一般的
Navier--Stokes 振幅缩放，而是这里的特殊 2D3C 结构：场与 \(x_1\)
无关，剪切只依赖 \(x_3\)，第一分量满足线性方程

\[
 \partial_tF+B\theta\,\partial_2F=\Delta_{23}F.
\]

所以只乘第一分量的常数振幅不会改变方程。

反演奇对称与偶径向平滑核继续给出

\[
 X_R(t)=a_R(t)=a_R'(t)=0.
\]

因此 M、F 两个冻结框架仍然相同，加速度支付行仍精确为零，物理压
力仍为零。这里没有调用未知的三维延拓定理。

归一化振幅是

\[
 \mathfrak a_0=B\Gamma^{-1/2}.
\]

为避免与原构造中固定的几何常数 \(\kappa=16\) 混淆，我用不同字
母定义新乘子

\[
 m:=\rho-\frac32c_\gamma
 =\frac{43}{423360}>0,
\]

\[
 \boxed{
 \varkappa=L^{2/3}e^{mL^2/3},
 \qquad
 \mathfrak a_*=\varkappa B\Gamma^{-1/2}.}
\]

这个选择的目的很精确：让三次的被动包支付刚好不超过背景支付，
同时让二次的端点量继续增长。

## 3. 完整支付量为什么没有跟着增长

记两个框架共同的完整支付为

\[
 P_*:=P_R^{M,*}=P_R^{F,*}.
\]

不能只检查一个方便的分母。我逐行重新代入新振幅。

### 3.1 局部能量行

一般振幅估计是

\[
 \mathcal E_*
 \le C\left[
 B^2R^2+\mathfrak a_*^2R^2
 \left(e^{-d_EL^2}+e^{-c/R^2}\right)
 \right],
 \qquad d_E=\frac{98}{29475}.
\]

设

\[
 e_E=d_E-c_\gamma
 =\frac{17018}{12998475}.
\]

主包相对背景能量的指数余量是

\[
 \boxed{
 e_E-\frac{2m}{3}
 =\frac{1171}{943200}>0.}
\]

所以

\[
 \varkappa^2\Gamma^{-1}e^{-d_EL^2}
 =L^{4/3}
 e^{-(1171/943200)L^2}\longrightarrow0.
\]

周期副本误差还带有 \(e^{-c/R^2}\)，因而更小。最终

\[
 \mathcal E_*\le CB^2R^2,
 \qquad
 \mathcal E_*^{3/2}\le CB^3R^3.
\]

### 3.2 压力行

物理压力虽然为零，冻结定义中的局部压力规范项不能直接删除。沿用
平均局部 Riesz 估计，

\[
 \mathcal G_{p,*}\le C\mathcal E_*^{3/2}
 \le CB^3R^3.
\]

这里没有偷偷使用压力抵消。

### 3.3 速度三次行

一般振幅账本是

\[
 \mathcal G_{u,*}
 \le C\left(B^3R^3+
 \mathfrak a_*^3R^4L^{-2}\right).
\]

被动包与背景的比值精确等于

\[
 \begin{aligned}
 \frac{\mathfrak a_*^3R^4L^{-2}}{B^3R^3}
 &=\varkappa^3R\Gamma^{-3/2}L^{-2}\\
 &=1.
 \end{aligned}
\]

这正是 \(m=\rho-\tfrac32c_\gamma\) 与 \(L^{2/3}\) 的作用。

### 3.4 调和代数行

另一行满足

\[
 \mathcal H_{u,*}
 \le C\left(B^3R^3+
 \mathfrak a_*^3R^4L^{-7/2}\right).
\]

它的被动包比值是

\[
 \varkappa^3R\Gamma^{-3/2}L^{-7/2}
 =L^{-3/2}.
\]

因此它比背景尺度还小。

### 3.5 上下界闭合

所有非负支付行合并后，

\[
 P_*\le CB^3R^3.
\]

另一方面，R0.74J 的第五支付壳中有一个固定剪切盒。被动分量与剪
切分量逐点正交，所以被动振幅不能取消该下界：

\[
 P_*\ge8e^{-8}B^3R^3.
\]

于是

\[
 \boxed{P_*\asymp B^3R^3.}
\]

由 \(B=\beta_jR^{-2}\) 且 \(\beta_j\) 上下有界，

\[
 \boxed{\log P_*=3\rho L^2+O(1),}
\]

所以 \(P_*\to\infty\)。这条反例只发生在大支付区，不碰小支付正则
性边界。

## 4. 两个目标量却按振幅平方增长

### 4.1 正领圈通量

在零框架精确族上，完整有符号领圈通量为

\[
 \mathfrak F_R^{(\mathfrak a)}(\tau)
 =\frac{\mathfrak a^2B}{2R}
 \int\!\!\int
 \eta_R\theta F^2\partial_2\vartheta_R^{\rm ann}.
\]

积分本身不依赖 \(\mathfrak a\)。因此对每个时间终点，

\[
 \mathfrak F_*(\tau)=\varkappa^2\mathfrak F_0(\tau).
\]

因为 \(\varkappa^2>0\)，取正部与时间上确界也保持该倍数：

\[
 \mathfrak C_* =\varkappa^2\mathfrak C_0.
\]

R0.74H 的下界与 R0.74N 的完整全壳层上界已经给出

\[
 \mathfrak C_0\asymp B^2LR^2.
\]

所以

\[
 \boxed{
 \mathfrak C_R^{M,*}=\mathfrak C_R^{F,*}
 \asymp\varkappa^2B^2LR^2.}
\]

这里使用的是完整的有符号正累积通量，不是把通量粗暴地换成绝对
三次支付。

### 4.2 端点动能—耗散量

R0.74F 的终端叶片定理对任意被动振幅成立，直接给出

\[
 X_R^{\alpha,*}
 \ge c\mathfrak a_*^2LR^2\Gamma
 =c\varkappa^2B^2LR^2.
\]

反向估计使用 R0.74H 的有符号通量闭合式：

\[
 X_R^{\alpha,*}
 \le C\left[(P_R^{\alpha,*})^{2/3}
 +\mathfrak C_R^{\alpha,*}\right].
\]

刚才已经独立证明

\[
 (P_R^{\alpha,*})^{2/3}\lesssim B^2R^2
 \le\varkappa^2B^2LR^2
\]

与

\[
 \mathfrak C_R^{\alpha,*}
 \lesssim\varkappa^2B^2LR^2.
\]

所以推理没有循环，并得到

\[
 \boxed{
 X_R^{M,*}=X_R^{F,*}
 \asymp\varkappa^2B^2LR^2.}
\]

## 5. 把几何参数换回标量支付量

振幅平方后的共同目标尺度是

\[
 \varkappa^2B^2LR^2
 =B^2R^2L^{7/3}e^{2mL^2/3}.
\]

定义

\[
 \delta_*:=\frac{2m}{9\rho}
 =\frac{86}{11907},
\]

\[
 q_*:=\frac23+\delta_*
 =\frac{8024}{11907}.
\]

由于

\[
 P_*^{2/3}\asymp B^2R^2,
 \qquad
 P_*^{\delta_*}\asymp e^{2mL^2/3},
\]

以及

\[
 (1+\log_+P_*)^{7/6}\asymp L^{7/3},
\]

得到主结论

\[
 \boxed{
 X_R^{\alpha,*}
 \asymp\mathfrak C_R^{\alpha,*}
 \asymp
 P_*^{8024/11907}
 (1+\log_+P_*)^{7/6}.}
\]

与原候选上界相比，比例为

\[
 \boxed{
 \frac{X_R^{\alpha,*}}
 {P_*^{2/3}\sqrt{1+\log_+P_*}}
 \asymp
 \frac{\mathfrak C_R^{\alpha,*}}
 {P_*^{2/3}\sqrt{1+\log_+P_*}}
 \asymp
 P_*^{86/11907}
 (1+\log_+P_*)^{2/3}
 \longrightarrow\infty.}
\]

因此，不存在一个与光滑解和尺度无关的常数，使该平方根对数上界
普遍成立。

同一列精确解还给出更强的标量边界：若

\[
 \Phi(p)=o\!\left(
 p^{8024/11907}(1+\log_+p)^{7/6}
 \right),
\]

那么 \(\mathfrak C_R^\alpha\lesssim\Phi(P_R^\alpha)\) 与
\(X_R^\alpha\lesssim\Phi(P_R^\alpha)\) 都不可能对全部光滑周期无外
力解成立。

这里没有声称 \(8024/11907\) 是最优指数。它只是当前完整一般振幅
账本能够严谨实现的最强前沿。

## 6. 任意固定对数幂也救不了 (2/3) 次幂

还有一个更直接的推论。

先固定任意 \(\gamma\in\mathbb R\)，再选择

\[
 M>\max\left\{0,\gamma-\frac12\right\},
 \qquad \varkappa_\gamma=L^M.
\]

这次振幅只按多项式增长。局部能量、三次速度与调和行中的被动包仍
被指数余量压住，因此

\[
 P_{\gamma,*}\asymp B^3R^3.
\]

而两个目标量满足

\[
 X_{\gamma,*}^\alpha
 \asymp\mathfrak C_{\gamma,*}^\alpha
 \asymp B^2R^2L^{2M+1}.
\]

候选右端只有

\[
 P_{\gamma,*}^{2/3}
 (1+\log_+P_{\gamma,*})^\gamma
 \asymp B^2R^2L^{2\gamma}.
\]

因为 \(2M+1-2\gamma>0\)，两者比例趋于无穷。

所以，对每个预先固定的 \(\gamma\)，都存在一个精确光滑解族，使

\[
 P^{2/3}(1+\log_+P)^\gamma
\]

不是普适上界。这里的解族可以依赖于给定的 \(\gamma\)；我没有声称
一列多项式振幅同时处理所有 \(\gamma\)。

## 7. 修复端点至少要看见什么

若尝试加入一个非负可观测量 \(Y_R^\alpha\)：

\[
 \mathfrak C_R^\alpha
 \le C\left[
 (P_R^\alpha)^{2/3}
 \sqrt{1+\log_+P_R^\alpha}
 +Y_R^\alpha\right],
\]

那么沿本节解族，它至少必须达到

\[
 \boxed{Y_R^\alpha\ge c\varkappa^2B^2LR^2}
\]

的尺度。换句话说，新量必须看见被标量支付漏掉的二次被动振幅。

R0.74H 已有的精确修复是把正领圈通量本身加入支付：

\[
 \widehat P_R^\alpha
 =P_R^\alpha+(\mathfrak C_R^\alpha)^{3/2}.
\]

在本节解族上，新增项确实压过原支付：

\[
 \frac{(\mathfrak C_R^\alpha)^{3/2}}{P_R^\alpha}
 \asymp L^{7/2}e^{mL^2}\longrightarrow\infty.
\]

这说明它能够检测反例，却不说明通量本身可由更基础的量独立控制。
时间极大范数、正时间变差、Carleson 型量或几何量也可能检测这种集
中，但本节没有证明其中任何一个充分。

## 8. 证据等级

### PROVED

- 新振幅仍给出精确、光滑、周期、均值为零、无外力解；
- M、F 两框架重合，加速度行精确为零；
- 完整支付量满足 \(P_*\asymp B^3R^3\)；
- 正领圈通量与 \(X_R^\alpha\) 都满足
  \(\asymp\varkappa^2B^2LR^2\)；
- 平方根对数标量端点失败；
- 所有低于已展示前沿的标量主函数失败；
- 对每个固定 \(\gamma\)，\(P^{2/3}(1+\log_+P)^\gamma\) 失败；
- 任意加法修复必须沿该族检测二次被动振幅尺度。

### INDEPENDENT ANALYTIC AUDIT

独立重建必须从一般振幅账本重新计算能量、压力、速度三次项和调和
项，检查领圈通量的精确二次缩放、\(X\) 上下界的非循环闭合、两个
有理指数及所有量词。它只绑定冻结源文件，不扩大结论。

### INHERITED

- R0.74F--N 的精确 2D3C 被动包—剪切解；
- R0.74F 对任意被动振幅成立的终端叶片下界；
- R0.74H 的精确通量恒等式、归一化通量下界与有符号闭合式；
- R0.74J 的第五支付壳剪切下界；
- R0.74N 的归一化完整全壳层通量上界。

### FINITE

精确证书核对有理常数、指数余量、三条支付比值、\(q_*\)、
\(\delta_*\) 与固定 \(\gamma\) 推论的代数条件。独立实现必须从原
始常数重算并对冻结 JSON 做 SHA-256 绑定。

有限计算不证明精确解结构、一般振幅解析估计、领圈通量定理或任何
正则性结论。

### LITERATURE BOUNDARY

2D3C 流中“二维基流加被动第三分量”的精确分裂以及第三分量的任意
振幅，在 Biferale、Buzzicotti 与 Linkmann 的一手论文中有明确先
例：[arXiv:1706.02371](https://arxiv.org/abs/1706.02371)。这支持本
节解族的结构可容许性，但不代替本项目内部对 \(P\)、\(X\) 和
\(\mathfrak C\) 的尺度证明。

限定范围的检索还覆盖局部正则性、加权局部能量、局部压力投影、通
量方法、偏斜柱体与若干结构化正则性准则。没有找到直接使用本节冻
结支付量并给出相同自由振幅前沿的定理。有限未命中不是新颖性、优
先权或可发表性的证明。

### OPEN

- 带额外时间、几何、BV、Carleson、压力或通量信息的端点估计；
- 最优的普适替代前沿；
- payment-to-admissibility 控制；
- 指定点 core-from-shell 控制；
- 任意三维有限能量初值的奇点形成或排除；
- 三维 Navier--Stokes 全局存在与光滑性；
- 新颖性与优先权。

## 9. 这一步的研究意义

R0.74N 之后，平方根对数尺度看起来像一个可能的普适端点。R0.74O
说明，它其实只记录了归一化振幅的选择。完整标量支付仍有一个很小
但严格为正的指数余量，被动分量可以利用这段余量增长；三次支付刚
好不越界，二次端点量却已经逃离。

这是一项有价值的路线淘汰结果。它阻止后续研究继续尝试任何只依赖
\(P_R^\alpha\) 的平方根对数证明，也更强地排除了固定 \(2/3\) 次幂
配任意预先给定对数幂的方案。

下一步不应再修补同一个纯标量不等式。真正需要研究的是：哪一个可
审计的附加结构量能够检测这类时间集中与二次被动振幅，同时又能从
适合正则性迭代的原始假设中控制。这个方向仍可能失败，但它已经避
开了本节证明不可能成立的路线。

本节的解始终光滑。没有奇点，没有 blow-up，没有 Clay 结论。

**NOT CLAY.**
