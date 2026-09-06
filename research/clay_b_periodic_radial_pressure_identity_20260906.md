# 周期区域的径向压力恒等式与未付出的输入

2026-09-06。**INTERNAL / PENDING REVIEW / EXACT SPATIAL IDENTITY / G OPEN / NOT CLAY。**

我先把 Seregin--Šverák 证明中的空间恒等式单独放回当前周期区域。
这里不导入全空间正则性定理，也不把一个已知的附加压力条件改写成
新的正则性结论。结果是：周期修正可以明确写出并由总能量控制；
奇异的局部环带项和时间一致的单侧压力势输入仍然留下。

## 1. 压力规范和固定外尺度

令 \(\mathbb T^3=(-\pi,\pi]^3\)，体积 \(V_{\mathbb T}=(2\pi)^3\)。
取光滑实向量场 \(u\)，采用规范

\[
 p=\partial_i\partial_j(-\Delta_{\mathbb T})^{-1}(u_i u_j),
 \qquad \int_{\mathbb T^3}p=0 .
\tag{BF.1}
\]

重复指标求和；逆算子在零模取零。这是 NS 的瞬时压力 Poisson
关系，但本节推导只需要 BF.1，不使用动量方程，甚至不需要无散性。

令 \(G\) 为零均值周期 Green 函数，

\[
 -\Delta G=\delta_0-V_{\mathbb T}^{-1},\qquad
 G(z)=\Gamma(z)+H(z),\qquad \Gamma(z)=\frac1{4\pi|z|}.
\tag{BF.2}
\]

固定 \(0<r_0<\pi/4\)，在 \(B_{2r_0}\) 的唯一局部提升内作此分解。
\(H\) 光滑且 \(\Delta H=V_{\mathbb T}^{-1}\)，所以每个
\(\partial_i\partial_jH\) 都调和。\(\partial_i\partial_jG\)
在不含原点的局部球上也调和。

给定中心 \(x_0\)，记 \(z=x-x_0\)、\(r=|z|\)、\(n=z/r\)，
\(u_r=(u\cdot n)n\)、\(u_T=u-u_r\)，只在 \(r<r_0\) 使用这些
局部符号。定义与内尺度 \(R\) 无关的二次余项

\[
 \begin{split}
 \mathcal C_{r_0,x_0}[u]
 ={}&4\pi\int_{B_{r_0}(x_0)}
        \partial_i\partial_jH(x-x_0)u_i u_j\,dx\\
 &+4\pi\int_{\mathbb T^3\setminus B_{r_0}(x_0)}
        \partial_i\partial_jG(x-x_0)u_i u_j\,dx .
 \end{split}
\tag{BF.3}
\]

两处核都在相应积分域有界。因此在固定 \(r_0\) 下，中心一致地有

\[
 |\mathcal C_{r_0,x_0}[u]|\le C(r_0)\|u\|_2^2 .
\tag{BF.4}
\]

## 2. 精确恒等式

对 \(0<R<r_0/2\)，记

\[
 K_{ij}(z)=\partial_i\partial_j\frac1r
          =\frac{3n_i n_j-\delta_{ij}}{r^3},\qquad r>0,
 \quad
 \mathcal T_R[u]
 =\int_{R<r<r_0}K_{ij}(z)u_i u_j\,dx+
      \mathcal C_{r_0,x_0}[u].
\tag{BF.5}
\]

那么有精确等式，而不是省略远场后的近似式：

\[
 \boxed{
 \int_{B_R(x_0)}\frac{2p+|u_T|^2}{r}\,dx
 =\frac1R\int_{B_R(x_0)}(3p+|u|^2)\,dx
 =R^2\mathcal T_R[u].}
\tag{BF.6}
\]

证明如下。平移中心到零，令
\(w_1=\mathbf 1_{B_R}/r\)、\(w_0=\mathbf 1_{B_R}\)，并记
\(\Psi_j=G*w_j\)。Euclidean 径向积分给

\[
 \Gamma*w_1=
 \begin{cases}R-r/2,&r<R,\\R^2/(2r),&r>R,\end{cases}
 \qquad
 \Gamma*w_0=
 \begin{cases}R^2/2-r^2/6,&r<R,\\R^3/(3r),&r>R.\end{cases}
\tag{BF.7}
\]

这些值也可直接由径向 Poisson 方程、原点有界性、无穷远衰减和
球面上值与一阶径向导数匹配验证。两式都在 \(r=R\) 为 \(C^1\)，
所以分布 Hessian 没有球面 delta。\(r\) 在原点的 Hessian 为
局部可积的 \((I-n\otimes n)/r\)，没有原点 delta。

当 \(r<R\)，卷积中所有差坐标均在 \(B_{2R}\)，可以使用 BF.2。
由调和函数的球面平均值性质，任意径向可积权重的平均等于其质量
乘球心处的值。因此

\[
 \begin{split}
 \partial_i\partial_j\Psi_1(z)
 &=-\frac{\delta_{ij}-n_i n_j}{2r}
       +2\pi R^2\partial_i\partial_jH(z),\\
 \partial_i\partial_j\Psi_0(z)
 &=-\frac{\delta_{ij}}3
       +\frac{4\pi R^3}{3}\partial_i\partial_jH(z),
 \qquad r<R .
 \end{split}
\tag{BF.8}
\]

当 \(z\notin\overline{B_R}\)，映射
\(y\mapsto\partial_i\partial_jG(z-y)\) 在 \(B_R\) 调和；
\(\int w_1=2\pi R^2\)、\(\int w_0=4\pi R^3/3\)。同一性质给

\[
 \partial_i\partial_j\Psi_1(z)
       =2\pi R^2\partial_i\partial_jG(z),\qquad
 \partial_i\partial_j\Psi_0(z)
       =\frac{4\pi R^3}{3}\partial_i\partial_jG(z).
\tag{BF.9}
\]

周期边界不引入额外项：这里是在无奇点的平移小球中用调和性，
不是把全空间衰减条件套到周期核上。

利用 \(G\) 的偶性及周期积分分部，有

\[
 \int_{\mathbb T^3}p w
   =\int_{\mathbb T^3}u_i u_j\,
                    \partial_i\partial_j(G*w),\qquad
 w\in\{w_0,w_1\}.
\tag{BF.10}
\]

BF.10 中右侧的重复指标作张量求和，即
\((u\otimes u):D^2(G*w)\)。严格地，
\(w_0,w_1\in L^2(\mathbb T^3)\)，从而 \(G*w\in H^2\)，
分布自伴性先给 BF.10，再由 BF.8--BF.9 的几乎处处表达式计算；
不需要未经论证地交换奇异核的绝对积分。

代入两套 Hessian，分别把内部速度项移到左侧，得到

\[
 \begin{split}
 \int_{B_R}\frac{2p+|u_T|^2}{r}
 ={}&4\pi R^2\left[
       \int_{B_R}D^2H:(u\otimes u)
       +\int_{\mathbb T^3\setminus B_R}D^2G:(u\otimes u)
       \right],\\
 \frac1R\int_{B_R}(3p+|u|^2)
 ={}&4\pi R^2\left[
       \int_{B_R}D^2H:(u\otimes u)
       +\int_{\mathbb T^3\setminus B_R}D^2G:(u\otimes u)
       \right].
 \end{split}
\tag{BF.11}
\]

在 \(R<r<r_0\) 分解 \(4\pi D^2G=K+4\pi D^2H\)，恰得 BF.6。
这也说明为何余项 BF.3 与 \(R\) 无关：它来自同一调和平均值
恒等式，不是把一个依赖 \(R\) 的误差强行放到常数里。

## 3. 这个等式支付了什么

固定压力规范不可省略。如果改为 \(p+c\)，BF.6 的两个左端都
增加 \(4\pi cR^2\)；因此要保持等式，右端的 \(\mathcal T_R\)
也必须增加 \(4\pi c\)。BF.3 对应的恰是 BF.1 的零均值压力。
压力负部及其势也依赖此规范。

若 \(\|u\|_2\le M\)，则

\[
 R^2|\mathcal C_{r_0,x_0}[u]|\le C(r_0)M^2R^2,
 \qquad
 R^2\left|\int_{R<r<r_0}K:(u\otimes u)\right|
          \le \frac{2M^2}{R} .
\tag{BF.12}
\]

第一项确实由能量支付；第二项随 \(R\downarrow0\) 反而恶化。
不能把整个右端都称为可忽略远场。

为看清单侧条件的作用，设 \(f\ge p_-\ge0\)，并假定以下势有限。
定义非负核心

\[
 \begin{split}
 S_R
 &:=\int_{B_R}\frac{f+|u_T|^2+2(p+f)}r\,dx\\
 &=3\int_{B_R}\frac f r\,dx+R^2\mathcal T_R[u].
 \end{split}
\tag{BF.13}
\]

积分中的每个分组均非负，故 \(S_R\) 随 \(R\) 单调增加。BF.6
以及 \(r\le R\) 还给

\[
 \frac1R\int_{B_R}|u|^2
  =R^2\mathcal T_R[u]-\frac3R\int_{B_R}p
  \le R^2\mathcal T_R[u]+3\int_{B_R}\frac f r
  =S_R .
\tag{BF.14}
\]

所以若在某个固定 \(R_0<r_0/2\) **额外**知道
\(\sup_{t,x_0}\int_{B_{R_0}(x_0)}f/r\le A<\infty\)，则逐时对
\(R\le R_0\) 有

\[
 \frac1R\int_{B_R(x_0)}|u(t)|^2
 \le S_R\le S_{R_0}
 \le3A+2M^2/R_0+C(r_0)M^2R_0^2 .
\tag{BF.15}
\]

这是条件性的空间代数结论，不是对额外条件的证明，也不是周期 NS
的正则性定理。原文随后还使用时间左连续性、强 \(L^2\) 连续性、
局部能量与小量正则性工具。BF.15 没有提供这些时间步骤，更没有
建立当前移动缩球合同 G。

## 4. 本节的范围

BF.6 是对已知径向压力机制的周期域重算，不作新颖性声明。
这里清除了一个明确的移植疑问：固定外尺度的周期余项可写明且
能量有界。真正的障碍仍是局部单侧压力势的时间控制，而不是这个
平滑余项。BG 将单独检查基本能量类是否足以提供该输入。

没有 NS 演化估计、G 输入减少、全局正则性或 Clay 结论；也没有
仿真、科学图或 DGX 计算。
