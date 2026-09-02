# R0.74Q｜许多壳层同时亮起，为什么仍然压不低支付？

## 导语

这一节仍然没有解决三维 Navier--Stokes 千禧年问题。

R0.74P 把核心缺口压缩成一个固定尺度问题。记完整 Version-M 支付的
自然尺度为

\[
 A_R:=(P_R^M)^{2/3},
\]

缺陷补全壳层时钟的匹配平方函数为

\[
 Z_R:=Y_{2,R}^{\rm sf}
 =\left(\sum_{k\ge1}v_{k,R}^2\right)^{1/2}.
\]

我真正想知道的是

\[
 \boxed{
 \mathfrak C_R^M
 \stackrel{?}{\le}
 C\left[A_R+Z_R\right].}
\]

这里 \(\mathfrak C_R^M\) 是所有物理壳层的有符号累计通量在终端前的
正部上确界，\(v_{k,R}\) 是第 \(k\) 个非负时钟的时间正变差。抽象序列
已经告诉我，不能仅靠

\[
 \sum_kv_k
 \quad\hbox{与}\quad
 \left(\sum_kv_k^2\right)^{1/2}
\]

之间的形式变换得到所需压缩：若 \(N\) 个坐标都等于一，前者是
\(N\)，后者只有 \(\sqrt N\)。缺少的必须是 Navier--Stokes 方程对
“同时有效壳层”的限制。

R0.74Q 因而不再发明一个新可观测量，而是把问题改写成一次压力测试。
我先证明一个精确的 terminal effective-shell reduction：只要除去有限
个终端壳层后，剩余正尾能够由 \(A_R\) 支付，上面的固定尺度不等式就
成立。然后我反过来构造越来越多的光滑精确包，试图让 \(N\) 个壳层在
同一个终端时刻都达到尺度 \(T\)，同时让平方函数只有
\(\sqrt N\,T\)，让支付的 \(2/3\) 次幂小于 \(NT\)。

结果分成清楚的两半。

1. 共同剪切的精确 PDE、放松后的多包几何、统一生存以及所有 target
   lobe 上的振幅加权无抵消，都可以严格完成。
2. equal-target 振幅一旦让每个目标时钟都达到同一尺度，最外层 lobe
   自己就迫使外部速度三次支付过大，并且

   \[
    \boxed{
    \frac{(P_R^{M,(N)})^{2/3}}{NT}\longrightarrow\infty.}
   \]

因此，这个明确的 equal-target 光滑精确解架构不能给出我想要的
低支付反例。它的失败不是包无法同时放进壳层，也不是尾部发生了未经
控制的抵消；真正阻断它的是凸的三次支付。

这不证明待定不等式正确，更不证明正则性。signed flux 的 \(NT\) 下界
和完整 \(Y_{2,R}^{\rm sf}\) 的 \(\sqrt N\,T\) 上界都仍然没有完成。

**NOT CLAY.**

## 1. 先把“有效壳层”写成精确终端命题

R0.74P 已经给出逐壳层累计平衡

\[
 K_{k,R}=Q_{k,R}+F_{k,R},
 \qquad
 K_{k,R}\ge0,
 \qquad
 K_{k,R}(\tau)\le v_{k,R},
\]

其中 \(Q\) 是二次截断源项原函数，\(F\) 是物理通量原函数。所有壳层
的 \(Q\) 有绝对账本

\[
 \sum_k\operatorname{TV}Q_{k,R}\le CA_R.
\]

关键点是：左端只要求累计总通量的正部，而不是要求控制
\(\sum_kv_{k,R}\) 的全部正变差。因此，我对一个绝对可和的实序列
\(x=(x_k)\) 定义除去至多 \(N\) 个坐标后的正残余

\[
 \mathcal S_N(x)
 :=\inf_{S\subset\mathbb N,\ \#S\le N}
 \left[\sum_{k\notin S}x_k\right]_+.
\]

相应地，在所有终端前时刻取上确界，得到

\[
 \mathcal S_{N,R}^{K}
 :=\sup_{\tau<t_0}\mathcal S_N((K_{k,R}(\tau))_k),
\]

以及真正允许壳间符号抵消的

\[
 \mathcal S_{N,R}^{F}
 :=\sup_{\tau<t_0}\mathcal S_N((F_{k,R}(\tau))_k).
\]

对任意固定 \(N\)，选择至多 \(N\) 个例外壳层，在例外集上用
Cauchy--Schwarz，例外集外保留终端正尾，就得到

\[
 \boxed{
 \mathfrak C_R^M
 \le CA_R+\sqrt N\,Z_R+\mathcal S_{N,R}^{K}.}
\]

把最后一项换成 \(\mathcal S_{N,R}^{F}\) 也成立，只需改变 \(A_R\)
前的绝对常数。这里允许例外集随终端时刻 \(\tau\) 改变；我没有要求
所有时间都由同一批壳层承担，也没有要求只有有限个时钟的正变差非零。

因此，只要存在一个与 \(R\) 和解无关的整数 \(N_0\)，使

\[
 \mathcal S_{N_0,R}^{K}\le CA_R
 \qquad\hbox{或}\qquad
 \mathcal S_{N_0,R}^{F}\le CA_R,
\]

R0.74P 留下的固定尺度不等式就会闭合。\(K\)-版本因为时钟非负，是
终端 best-\(N\) 尾；\(F\)-版本才是有符号的有效壳层命题。

这个改写的价值在于量词准确。它没有把目标偷换成“活跃壳层总数有界”，
而是问：在每个终端切片上，是否只有有限个壳层需要单独支付，剩余正尾
能否由完整支付量吸收？

## 2. 纯序列空间为什么仍然不够

若 \(v^*\) 是非负序列 \(v\) 的递减重排，best-\(N\) 的
\(\ell^1\) 尾为

\[
 \sigma_N(v)_1=\sum_{m>N}v_m^*.
\]

总有

\[
 \|v\|_1
 \le\sqrt N\,\|v\|_2+\sigma_N(v)_1.
\]

而且 layer-cake 恒等式给出

\[
 \sigma_N(v)_1
 =\int_0^\infty
 \bigl(\#\{k:v_k>\lambda\}-N\bigr)_+\,d\lambda.
\]

所以一个幅度阈值上的壳层计数不够；真正需要的是对所有幅度层积分后的
packing。最简单的平顶序列

\[
 v_k^{(M,L)}=M^{-1}\mathbf1_{\{L<k\le L+M\}}
\]

满足

\[
 \|v^{(M,L)}\|_1=1,
 \qquad
 \|v^{(M,L)}\|_2=M^{-1/2},
\]

而区间可以移到任意大的壳层指标。有限前缀控制、单峰、一个连通壳层块、
定性 \(\ell^p\) 可和或有界树宽，都不能单独给出统一压缩。

对非零非负序列，纯粹的

\[
 \|v\|_1\le C\|v\|_2
\]

等价于逆参与数

\[
 N_{\rm eff}(v)
 :=\frac{\|v\|_1^2}{\|v\|_2^2}
\]

一致有界。这个数才是抽象序列意义上的有效壳层数。因为壳层权重已经
包含在 \(v_{k,R}\) 里面，\(\sum_k\gamma_k<\infty\) 本身不能再替我
完成压缩。

于是下一步必须让 PDE 说话。最直接的检验是：方程是否真的允许很多
物理壳层在同一终端时刻都留下尺度相同的时钟？

## 3. 多包压力测试想实现什么

理想的压力测试会构造一个光滑、周期、无外力的精确解，在互不相同的
目标壳层 \(k_1,\ldots,k_N\) 上，同时满足

\[
 K_{k_\ell,R}(\tau_N)\ge cT,
 \qquad 1\le\ell\le N.
\]

若还能证明

\[
 \mathfrak C_R^{M,(N)}\gtrsim NT,
 \qquad
 Y_{2,R}^{\rm sf,(N)}\lesssim\sqrt N\,T,
\]

并让

\[
 (P_R^{M,(N)})^{2/3}=o(NT),
\]

那么固定尺度待定不等式会在光滑精确解上失败。

这三个目标缺一不可。许多正时钟并不自动给出有符号总通量；目标壳层的
下界也不自动给出完整平方函数的上界；把单包支付逐个估计后相加，更不
能忽略完整支付外面的 \(3/2\) 次幂。R0.74Q 的作用，就是把这些原来
混在一句“叠加很多包”里的要求逐项拆开。

## 4. 共同剪切使精确 PDE 门成立

工作在 \(\mathbb T^3=(-\pi,\pi]^3\)。取一个光滑奇函数初值
\(\theta_0(x_3)\)，令

\[
 \theta(t,x_3)=e^{t\partial_3^2}\theta_0(x_3),
 \qquad
 b(t,x_3)=B\theta(t,x_3).
\]

对每个包 \(G_\ell\)，把一对位于 \((q_{{\rm pre},\ell},h_\ell)\)
和其反演位置的周期热核导数作为初值，并让所有包都解同一个线性方程

\[
 (\partial_t+b\partial_2-\Delta_{23})G_\ell^\pm=0,
 \qquad
 G_\ell=G_\ell^++G_\ell^-.
\]

对任意有限 \(N\) 和常振幅 \(\mathfrak a_\ell\)，定义

\[
 U_N=\sum_{\ell=1}^N\mathfrak a_\ell G_\ell,
 \qquad
 u^{(N)}=(U_N,b,0),
 \qquad
 p^{(N)}=0.
\]

这个场与 \(x_1\) 无关，而 \(b\) 与 \(x_2\) 无关，因此

\[
 \nabla\cdot u^{(N)}=0,
 \qquad
 u^{(N)}\cdot\nabla=b\partial_2.
\]

第一分量由所有共同剪切的线性方程相加得到，第二分量只是热方程，第三
分量恒为零，所以它是精确的无外力 Navier--Stokes 解，物理压力可以
取零。反演配对与奇剪切保持

\[
 u^{(N)}(t,-x)=-u^{(N)}(t,x).
\]

对冻结的偶 mollifier，这进一步给出

\[
 X_R(t)\equiv0,
 \qquad
 a_R(t)=a_R'(t)=0.
\]

因此 Version M 与 Version F 在这个精确族上重合。

这里“共同”二字不能省略。若旧包 \(F_\ell\) 各自在不同剪切
\(b_\ell\) 下演化，把它直接放到新剪切 \(b\) 下会留下残差

\[
 (b-b_\ell)\partial_2F_\ell.
\]

把旧的完整速度场相加还会产生所有交叉剪切项。正确顺序是先冻结一个
剪切，再让每个包在同一个系数下重新演化。精确 PDE 的线性叠加不表示
通量、时钟、局部压力或三次支付也线性叠加。

## 5. 原来的冻结角为什么不能共用一个标定

R0.74F 的单包几何把目标高度和水平终点写成

\[
 h_i=c_hL_iR,
 \qquad
 q_i=\beta L_iR,
\]

并要求一个剪切振幅 \(B\) 同时满足

\[
 BD_R(h_i)=q_*+q_i,
 \qquad i=1,2,
\]

其中

\[
 D_R(h)=\int_{R^2}^{65R^2}\theta_R(t,h)\,dt.
\]

正平台估计给出

\[
 D_R(c_hLR)=64R^2-\delta(L),
 \qquad
 0\le\delta(L)\le CR^2e^{-a_DL^2}.
\]

若 \(L_2\ge2L_1\) 而同一个 \(B\) 同时完成两个冻结标定，交叉相乘
会迫使

\[
 R(L_2-L_1)\le Ce^{-a_DL_1^2}.
\]

另一方面，沿用的 R0.74F 内包 bridge proof 在以下充分储备条件下闭合
其平移误差：

\[
 R^{-1}e^{-a_SL_1^2}\longrightarrow0.
\]

在 dyadic 分离下，这个储备与前面的必要关系不相容。因此，原来的
冻结终端角不能在同一剪切、同一 \(R\)、相邻两个 dyadic 物理壳层上
直接复制。

这只是指定参数化的失败。它依赖
\((h_i,q_i)=(c_hL_iR,\beta L_iR)\)、同一水平入口点
\(q_*=1/2\)、同一正平台和继承的 bridge closure。它不表示共同剪切
多包在 PDE 层面不可能，也不表示所有放松后的终端几何都会失败。

## 6. 放松水平终点后，\(N\) 个壳层几何可以同时完成

我保留垂向高度

\[
 h_\ell=c_hL_\ell R,
\]

但不再预先规定水平终点角。取

\[
 L=\frac{63}{32}2^j,
 \qquad
 R=e^{-L^2/320},
 \qquad
 N=\lfloor\log_2L\rfloor=j,
\]

以及

\[
 L_\ell=2^{\ell-1}L,
 \qquad
 k_\ell=j+\ell-1,
 \qquad
 1\le\ell\le N.
\]

最外尺度满足精确关系

\[
 L_N=\frac{16}{63}L^2,
 \qquad
 L_NR\longrightarrow0.
\]

所以尽管壳层数趋于无穷，所有目标高度仍然留在同一中央周期图内。

用最内层平台定义共同振幅

\[
 B=\frac{q_*}{D_1},
\]

再让每个水平终点由实际剪切位移决定：

\[
 q_\ell=BD_\ell-q_*.
\]

平台误差给出

\[
 \sup_{\ell\le N}|q_\ell|\le Ce^{-a_DL^2},
 \qquad
 \sup_{\ell\le N}\frac{|q_\ell|}{R}\longrightarrow0.
\]

于是所有参考路径在同一终端区间

\[
 J=(65R^2-R^3,65R^2)
\]

内都只有 \(O(R)\) 的水平误差。继承的 all-winding Brownian-bridge
估计在 \(L_\ell\ge L\) 上统一关闭；每个正包在自己的 lobe 上有固定
符号，并满足一个与 \(N,\ell\) 无关的点态下界。

令

\[
\begin{aligned}
 \Omega_{\ell,+}(t)=\{x:\;&|x_1|<L_\ell R/16,\\
 &5R/4<x_2-Q_\ell(t)<3R/2,\\
 &|x_3-h_\ell|<R\},
\end{aligned}
\]

并取反演 lobe \(\Omega_{\ell,-}(t)=-\Omega_{\ell,+}(t)\)。统一的
内外半径余量证明

\[
 \Omega_{\ell,\pm}(t)\subset A_{k_\ell}(R),
 \qquad 1\le\ell\le N,
\]

而这些 \(k_\ell\) 两两不同。每个 lobe 的体积为

\[
 |\Omega_{\ell,+}(t)|
 =\frac1{16}L_\ell R^3.
\]

所以 relaxed geometry 真正通过了共同剪切、共同终端窗口、统一
bridge survival、反演配对、周期 copies 和不同物理壳层六道门。

## 7. equal-target 振幅下，所有 lobe 仍然不被其他包抵消

目标壳层权重是

\[
 \Gamma_\ell
 =\gamma_{k_\ell}
 =e^{-c_\gamma L_\ell^2},
 \qquad
 c_\gamma=\frac8{3969}.
\]

为了让每个目标壳层具有同一终端尺度，我取

\[
 \mathfrak a_\ell
 =A_*(\Gamma_\ell L_\ell)^{-1/2}.
\]

这样

\[
 \boxed{
 T:=\Gamma_\ell\mathfrak a_\ell^2L_\ell R^2
 =A_*^2R^2}
\]

与 \(\ell\) 无关。困难在于 \(\Gamma_\ell\) 随壳层指数下降，所以
\(\mathfrak a_\ell\) 向外增长得非常快。仅仅说未加权包彼此远离，
不能排除大振幅外包的微小热尾抵消内包。

共同剪切随机表示给出一个不依赖剪切大小的垂向尾界：

\[
 |G_m^\pm(t,x)|
 \le CRK_{R^2+t}^{\rm per}(x_3\mp h_m),
 \qquad 0\le t\le65R^2.
\]

令

\[
 a_\times=\frac{49}{14850},
 \qquad
 q=\frac{c_\gamma}{2}=\frac4{3969}.
\]

在第 \(\ell\) 个正 lobe 上，直接包和反演包分别满足

\[
 |G_m^+|
 \le Ce^{-a_\times(L_m-L_\ell)^2}
    +Ce^{-3/(22R^2)},
\]

\[
 |G_m^-|
 \le Ce^{-a_\times(L_m+L_\ell)^2}
    +Ce^{-3/(22R^2)}.
\]

最危险的是相邻外包 \(L_m=2L_\ell\) 污染内层 target。振幅增长与
Gaussian 尾合并后的精确余量是

\[
 \delta_\times
 =a_\times-3q
 =\frac{67}{242550}>0.
\]

对更远的外包，若 \(r=L_m/L_\ell\ge2\)，净指数满足

\[
 a_\times(r-1)^2-q(r^2-1)
 \ge\delta_\times(r-1)^2.
\]

因此所有外包的振幅加权尾可以求和。内包污染外层 target 时，振幅
本身已经下降；相邻内包的精确指数为

\[
 \mu_{\rm in}
 =\frac14a_\times+\frac34q
 =\frac{4601}{2910600}>0,
\]

其后各项形成统一几何尾。

周期绕回也不能被振幅放大救回来。最外高度仍在中央图内，所有非零垂向
winding 给出 \(e^{-3/(22R^2)}\)。乘上最粗的全包振幅因子后，周期总
余项至多为

\[
 CN\exp\left[
 \frac{1024}{15752961}L^4
 -\frac3{22}e^{L^2/160}
 \right]\longrightarrow0.
\]

合并外包、内包、反演 partner 与所有周期 copies，存在与
\(A_*,N,\ell\) 无关的 \(\varepsilon_L\to0\)，使每个正、负 target
lobe 上都有

\[
 \frac{\sum_{m\ne\ell}|\mathfrak a_mG_m|}
 {|\mathfrak a_\ell G_\ell|}
 \le\varepsilon_L.
\]

对充分大的 \(L\)，右端小于 \(1/2\)，于是

\[
 \boxed{
 |U_N|
 \ge\frac12|\mathfrak a_\ell G_\ell|
 \ge\frac{c_0}{2}\mathfrak a_\ell}
\]

在全部 \(N\) 个 target lobe 上同时成立。这一步把此前条件式的
no-cancellation 假设变成了这个明确解族上的定理。

## 8. 每个目标时钟都有 \(T\) 量级的终端下界

在 \(\tau\in J\) 时，时间 cutoff 已等于一，目标壳层 cutoff 在
\(\Omega_{\ell,+}(\tau)\) 上也等于一。缺陷补全时钟的耗散部分非负，
所以只保留终端能量就有

\[
\begin{aligned}
 K_{k_\ell,R}(\tau)
 &\ge\frac{\Gamma_\ell}{2R}
 \int_{\Omega_{\ell,+}(\tau)}|u^{(N)}(\tau,x)|^2\,dx\\
 &\ge c\Gamma_\ell\mathfrak a_\ell^2L_\ell R^2
 =cT.
\end{aligned}
\]

所有目标指标不同，因此

\[
 K_{k,R}(s_R)=0,
 \qquad
 K_{k,R}\ge0
 \quad\Longrightarrow\quad
 v_{k,R}=\operatorname{Var}^{+}K_{k,R}
 \ge K_{k,R}(\tau).
\]

把这个正变差下界用于两两不同的目标指标，得到

\[
 \boxed{
 Y_{2,R}^{\rm sf}
 \ge c\sqrt N\,T.}
\]

这是一条同时终端检出下界。它说明多包没有在目标平方函数中消失，但
方向只有“\(\ge\)”。我还没有控制非目标壳层时钟、所有二次交叉项，
也没有控制 \(J\) 以前积累的正变差。所以

\[
 \boxed{
 Y_{2,R}^{\rm sf}\lesssim\sqrt N\,T
 \quad\textbf{OPEN}.}
\]

不能把目标分量的下界写成完整平方函数的双边尺度。

## 9. 最外 lobe 单独迫使三次支付过大

完整 Version-M 支付包含非负的外部速度三次项。在半径 \(2R\) 上，

\[
 \mathcal G_u^{(N)}
 =(2R)^{-2}
 \int_{I_{2R}}\int_{\mathbb T^3}
 W_{2R}(x)|u^{(N)}(t,x)|^3\,dx\,dt.
\]

最外 target lobe 位于

\[
 A_{k_N}(R)=A_{k_N-1}(2R),
\]

该 annulus 的支付权重正好是

\[
 \gamma_{k_N-1}
 =e^{-(c_\gamma/4)L_N^2}
 =\Gamma_N^{1/4}.
\]

时间长度是 \(|J|=R^3\)，空间体积是 \(L_NR^3/16\)，归一化为
\((2R)^{-2}\)。利用已经证明的点态 dominance，可得真正的下界

\[
\begin{aligned}
 P_R^{M,(N)}
 &\ge\mathcal G_u^{(N)}\\
 &\ge c\mathfrak a_N^3\Gamma_N^{1/4}L_NR^4\\
 &=cA_*^3R^4\Gamma_N^{-5/4}L_N^{-1/2}.
\end{aligned}
\]

这不是一个发散的上界或无法关闭的 majorant，而是对真实非负支付项
的下界。

取 \(2/3\) 次幂，再除以

\[
 NT=NA_*^2R^2,
\]

共同振幅 \(A_*\) 精确消去：

\[
 \frac{(P_R^{M,(N)})^{2/3}}{NT}
 \ge\frac cN R^{2/3}L_N^{-1/3}
 e^{(5/6)c_\gamma L_N^2}.
\]

因为 \(L_N=(16/63)L^2\)、\(R=e^{-L^2/320}\)，其对数满足

\[
\begin{aligned}
 \log\frac{(P_R^{M,(N)})^{2/3}}{NT}
 \ge{}&
 \frac{5c_\gamma}{6}L_N^2
 -\frac1{480}L^2
 -\frac13\log L_N-\log N-O(1)\\
 \longrightarrow{}&+\infty.
\end{aligned}
\]

精确的 \(L^4\) 首项系数为

\[
 \frac{5120}{47258883}>0.
\]

所以

\[
 \boxed{
 \frac{(P_R^{M,(N)})^{2/3}}{NT}\longrightarrow\infty.}
\]

这说明 equal-target 架构越努力把外层时钟抬到与内层相同的 \(T\)，
就越被最外物理壳层的凸三次支付收费。加更多同样归一化的包不会接近
低支付目标，反而使最外壳的指数成本更严重。

## 10. 为什么这仍然不是待定不等式的证明

终端时钟总和确实满足

\[
 \sum_{\ell=1}^NK_{k_\ell,R}(\tau)\ge cNT.
\]

但有符号物理通量是

\[
 F_{k,R}=K_{k,R}-Q_{k,R}.
\]

现有绝对账本只给出

\[
 \sum_k\operatorname{TV}Q_{k,R}
 \le C(P_R^{M,(N)})^{2/3}.
\]

因此目前最多得到

\[
 \sum_kF_{k,R}(\tau)
 \ge cNT-C(P_R^{M,(N)})^{2/3}.
\]

而刚刚证明的支付发散说明右端误差远大于 \(NT\)。这个不等式没有正
内容，不能推出

\[
 \mathfrak C_R^{M,(N)}\asymp NT.
\]

所以本节严格保留两条 OPEN 边界：

\[
 \boxed{
 \mathfrak C_R^{M,(N)}\asymp NT
 \quad\textbf{OPEN},}
\]

\[
 \boxed{
 Y_{2,R}^{\rm sf,(N)}\lesssim\sqrt N\,T
 \quad\textbf{OPEN}.}
\]

若未来另有有符号通量分析证明第一条，那么本节的支付下界只会说明这个
equal-target 解族不能反驳固定尺度不等式。反过来，当前构造失败也不
能推出固定尺度不等式对任意周期适合弱解成立。两种逻辑方向都不能
越过。

## 11. 这一节的研究价值

R0.74Q 的价值不是离全局正则性终点又近了一个可以用百分比表示的距离，
而是把“多壳层可能破坏匹配平方函数压缩”这条路线分成了可独立核查的
机制，并明确了哪一部分成功、哪一部分失败。

第一，terminal best-\(N\) reduction 给出了足够弱而又足以推出待定
不等式的有效壳层命题。例外壳层可以随终端时刻变化；\(F\)-版本保留
真正的符号结构。这比要求时钟支撑有限更接近 PDE 实际可能提供的
packing。

第二，共同剪切的精确解说明 PDE 线性叠加本身不是障碍。原来的冻结角
失败来自过强的共同标定，不是方程不允许多包。放松水平终点以后，
\(N\to\infty\) 个包可以共享剪切、终端窗口和零 mollified path，并
分别落入不同物理壳层。

第三，equal-target 振幅下的 all-lobe dominance 已经逐项支付了
相邻外包、内包、反演 partner 和全部周期绕回。最危险的外侧相邻指数
仍有明确正余量。因此，后面的三次支付阻断不是由“也许发生抵消”造成
的条件式结论。

第四，最外 lobe 暴露了一个以前容易被上界 majorant 混淆的事实：
物理壳层权重与 equal-target 振幅结合后，真实的非负 exterior cubic
row 已经足以关闭这条低支付反例路线。这里没有借助压力，因为精确解的
物理压力为零；也没有依赖异常耗散，因为解是光滑的。

第五，失败机制给下一步提供了更准确的方向。问题不再是“能否简单叠加
更多相同包”，而是：凸支付是否本身能够对有效终端壳层数给出一个一般
packing；或者，是否存在非 equal-target 的振幅分配、不同时间安排或
不同几何，在保留 signed flux 与平方函数尺度的同时避开最外三次收费？

这些都是可以逐条证明或否定的问题。它们仍处于本项目内部研究阶段；
有限文献筛查未命中同一命题，不构成新颖性或优先权结论。

## 12. 下一步怎么走

我不会继续机械地增加 equal-target 包数。下一阶段应当同时推进三条
互相校验的路线。

### 12.1 从 cubic payment 反推一般有效壳层 packing

本节只在一个明确几何上证明：若最外 target lobe 有固定体积和点态
dominance，它就必须支付一个三次成本。下一步要问能否把这个机制写成
不依赖精确包形状的局部不等式，把若干终端时钟 \(K_{k,R}(\tau)\) 与
各壳层的非负支付 \(p_{k,R}\) 联系起来。

一个可操作目标是：除去至多 \(N_0\) 个终端例外后，构造
\(a_{k,R,\tau}\ge0\)，使

\[
 K_{k,R}(\tau)
 \le q_{k,R}+a_{k,R,\tau}p_{k,R}^{2/3},
\]

并满足

\[
 \sum_kq_{k,R}\le CA_R,
 \qquad
 \sum_{k\notin S_\tau}a_{k,R,\tau}^3\le C.
\]

Hölder 随即把例外集外的终端正尾压到 \(CA_R\)。这正是
effective-shell reduction 所需要的 PDE 形式。

### 12.2 优化非 equal-target 振幅，而不是预设每壳同高

equal-target 让时钟账本最清楚，却把外层振幅设为
\(\Gamma_\ell^{-1/2}\) 量级。可以把下一轮压力测试写成一个离散优化：
在给定 cubic budget、目标 signed-flux 总量和平方函数预算下，寻找
最优的 \(T_\ell\) 分布，检查是否存在很多弱外壳与少数强内壳的组合。

这一步必须使用完整支付，而不能只优化单个 exterior row；中央能量的
\(3/2\) 次幂、harmonic row、局部压力账本和所有交叉时钟都要保留。
若优化问题本身已有 coercive lower bound，它会支持一般 packing；若
仍有逃逸序列，再回到 PDE 构造验证它能否实现。

### 12.3 单独处理 signed flux 与完整 \(Y_2\)

终端 \(K\) 下界不能代替 \(F=K-Q\) 的符号分析。需要检查相邻物理壳层
cutoff 是否能在总和前通过离散 Abel 变换消去内部边界，或能否把
\(Q\) 的最坏绝对账本改成对目标终端更有利的 signed estimate。

同样，完整 \(Y_{2,R}^{\rm sf}\) 必须核对所有 off-target 壳层和早期
正变差。只有得到上界，\(\sqrt N\,T\) 才能被当作精确族的真实平方
函数尺度，而不是目标分量的下方检出。

这三条路线彼此有门禁关系：没有 signed flux 与 \(Y_2\) 上界，新的
精确族不能否定待定不等式；没有一般 cubic packing，也不能从本节一个
解族的失败推到任意适合弱解。

## 13. 证据与边界

- **PROVED：**terminal effective-shell reduction；共同剪切有限
  \(N\) 精确 NSE；不同旧剪切不能直接叠加；冻结角共同标定在继承
  survival reserve 下失败；relaxed \(N\)-packet 共同终端几何与统一
  bridge 参数闭合；equal-target all-lobe dominance；每个目标
  \(K_{k_\ell,R}\gtrsim T\)；最外真实 velocity-cubic payment 下界；
  \((P_R^{M,(N)})^{2/3}/(NT)\to\infty\)。
- **INHERITED：**R0.74F 的 all-winding Brownian-bridge 生存定理；
  R0.74E/H 的物理壳层权重和完整支付定义；R0.74P 的
  \(K=Q+F\) 缺陷补全时钟、正变差与绝对 \(Q\) 账本。
- **FINITE：**所有显示的有理指数余量、dyadic 恒等式、公式标签与
  确定性证书检查。有限计算不替代 stochastic tail、annular geometry
  或 payment lower bound 的解析证明。
- **LITERATURE BOUNDARY：**2D3C 中“二维底流加被动第三分量”以及
  一个共同线性标量方程允许的叠加机制已有先例，不能单独作为新颖性
  主张。有限的一手文献筛查没有找到直接覆盖冻结角标定障碍、relaxed
  all-lobe dominance 与 cubic-payment 组合定理的来源；这只是 bounded
  non-hit，不证明新颖性、优先权或可发表性。
- **OPEN：**\(\mathfrak C_R^{M,(N)}\asymp NT\)；完整
  \(Y_{2,R}^{\rm sf,(N)}\lesssim\sqrt N\,T\)；一般适合弱解的
  terminal effective-shell packing；固定尺度不等式
  \(\mathfrak C_R^M\le C[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}]\)；预定中心
  的尺度收缩与迭代；三维 Navier--Stokes 全局正则性。

R0.74Q 没有数值 Navier--Stokes 仿真，没有构造奇点，没有排除奇点，
没有证明任意光滑有限能量初值的全局光滑性，也没有解决固定尺度待定
不等式。

**NOT CLAY.**
