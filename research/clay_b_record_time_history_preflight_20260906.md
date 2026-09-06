# Record 倍增时间与固定初值历史：一次有限检查

2026-09-06。**INTERNAL / PROVED TIME-BOOKKEEPING OBSTRUCTION / CONDITIONAL ANCIENT NONCONSTANCY / G OPEN / NOT CLAY。**

我检查一个窄问题。固定同一周期光滑初值，并假设最大光滑时间
有限。速度 record 的相邻倍增间隔，在峰值缩放后是否自动有统一
上界？如果有这样一条有界子列，它是否足以排除常向量古老极限？

结论分成两部分。标准局部 mild 理论只给倍增时间的下界；有限总
时间不推出有界子列。若另有一条有界子列，则固定初值峰值缩放的
极限确实非恒定。后一结论仍不是古老解刚性，也不完成合同 G。

## 1. 固定解与第一次倍增时刻

先在合同使用的 \(\mathbb T^3=(-\pi,\pi]^3\)、黏性
\(\nu=1\) 上书写。对一般正黏性，下面局部寿命常数多一个
\(\nu\) 因子。先作已经核对合法的 Galilean 归一化，使速度
空间均值为零；record 都对这个固定代表定义。

令 \(u\) 是同一光滑无散初值 \(u_0\) 的最大光滑 NS 解，

\[
 \partial_tu+(u\cdot\nabla)u+\nabla p=\Delta u,\qquad
 \operatorname{div}u=0,\qquad 0\le t<T_*<\infty .
\tag{BJ.1}
\]

有界速度的标准延拓接口说明 \(H(t)\to\infty\)，其中

\[
 H(t):=\max_{0\le r\le t}\|u(r)\|_{L^\infty}.
\tag{BJ.2}
\]

取一个已达到的 record 水平
\(M_0>\max\{1,\|u_0\|_\infty\}\)，令
\(M_j=2^jM_0\)，并令 \(t_j\) 为 \(H\) 第一次达到
\(M_j\) 的时刻。连续性给

\[
 t_j\uparrow T_*,\qquad
 \|u(t_j)\|_\infty=M_j,\qquad
 \sup_{0\le r\le t_j}\|u(r)\|_\infty=M_j.
\tag{BJ.3}
\]

以下记

\[
 D_j:=M_j^2(t_j-t_{j-1}),\qquad j\ge1.
\tag{BJ.4}
\]

## 2. 局部 mild 理论给的是下界

从任意光滑时刻 \(a<T_*\) 写周期 mild 公式：

\[
 u(t)=e^{(t-a)\Delta}u(a)
 -\int_a^t e^{(t-r)\Delta}\mathbb P
          \operatorname{div}(u\otimes u)(r)\,dr .
\tag{BJ.5}
\]

标准周期 Oseen 核界为

\[
 \|e^{\tau\Delta}\mathbb P\operatorname{div}F\|_\infty
 \le C\tau^{-1/2}\|F\|_\infty,\qquad 0<\tau\le1.
\tag{BJ.6}
\]

配套 BI.5--BI.10 已给出这里所需的周期 Oseen 核、全空间提升和
与周期尺度无关的短时 bootstrap；其余标准局部 mild 的存在、
唯一性、延拓与内部平滑接口仍作为外部输入。本稿不把一次
bootstrap 称为对这些接口的完整重证。
若 \(M\ge1\) 且 \(\|u(a)\|_\infty\le M\)，在暂定 bootstrap
\(\sup\|u\|_\infty\le2M\) 下，BJ.5--BJ.6 给

\[
 \sup_{a\le t\le a+T}\|u(t)\|_\infty
 \le M+4C T^{1/2}M^2.
\tag{BJ.7}
\]

可固定 \(0<c_*\le1\)，使 \(4C\sqrt{c_*}\le1/2\)。
连续性 bootstrap 于是给一个严格余量：

\[
 \sup_{a\le t\le a+c_*M^{-2}}\|u(t)\|_\infty
 \le\frac32M<2M.
\tag{BJ.8}
\]

若最大光滑区间比右端更短，标准局部接口会延拓原解，故这种情况
不能发生。将 BJ.8 用于 \(a=t_{j-1}\)、\(M=M_{j-1}\)，得到

\[
 t_j-t_{j-1}\ge c_*M_{j-1}^{-2}
      =4c_*M_j^{-2},\qquad
 \boxed{D_j\ge4c_*}.
\tag{BJ.9}
\]

因此局部理论阻止的是过快倍增，不是过慢倍增。从 \(t_j\)
重新启动还给

\[
 M_j^2(T_*-t_j)\ge c_*.
\tag{BJ.10}
\]

为避免把存在寿命的端点当成已有紧性余量，后面只在正向闭区间
\([0,\sigma_*]\) 上使用估计，其中
\(\sigma_*:=c_*/2\)。在峰值缩放变量中 BJ.8 给

\[
 \sup_{0\le s\le\sigma_*}\|v_j(s)\|_\infty
 \le\frac32.
\tag{BJ.11}
\]

## 3. 有限总时间只给指数加权可和性

由 \(t_j\uparrow T_*\) 和 BJ.4，

\[
 T_*-t_0
 =\sum_{j\ge1}(t_j-t_{j-1})
 =M_0^{-2}\sum_{j\ge1}4^{-j}D_j<\infty.
\tag{BJ.12}
\]

所以确实已付的是

\[
 \sum_{j\ge1}4^{-j}D_j<\infty,\qquad
 4^{-j}D_j\longrightarrow0,
\tag{BJ.13}
\]

而不是 \(D_j\) 的统一上界。若令

\[
 A_j:=M_j^2(T_*-t_j),
\tag{BJ.14}
\]

则还有精确尾关系

\[
 A_j=\sum_{m\ge1}4^{-m}D_{j+m},\qquad
 D_j=4A_{j-1}-A_j.
\tag{BJ.15}
\]

BJ.10 只说明 \(A_j\ge c_*\)。现有账本没有给
\(A_j\) 的上界。

## 4. 固定初值峰值缩放保留的量

在紧周期胞中取 \(x_j\)，使
\(|u(x_j,t_j)|=M_j\)，并定义

\[
 \begin{aligned}
 v_j(y,s)&=M_j^{-1}u\left(x_j+\frac y{M_j},
                     t_j+\frac s{M_j^2}\right),\\
 q_j(y,s)&=M_j^{-2}p\left(x_j+\frac y{M_j},
                     t_j+\frac s{M_j^2}\right).
 \end{aligned}
\tag{BJ.16}
\]

这是单位黏性的精确 NS 缩放。空间周期尺度为 \(M_j\)，
时间区间为

\[
 -M_j^2t_j\le s<M_j^2(T_*-t_j).
\tag{BJ.17}
\]

第一次达到和空间峰点给出精确 record 数据：

\[
 |v_j(0,0)|=1,\qquad
 \sup_{-M_j^2t_j\le s\le0}\|v_j(s)\|_\infty\le1.
\tag{BJ.18}
\]

原解的光滑能量等式为

\[
 \|u(t)\|_2^2+2\int_0^t\!\int_{\mathbb T^3}
          |\nabla u(x,r)|^2\,dx\,dr
 =\|u_0\|_2^2.
\tag{BJ.19}
\]

变量换元后，整胞能量满足

\[
 \int_{\mathbb T_{M_j}^3}|v_j(s)|^2\,dy
 =M_j\int_{\mathbb T^3}|u(t_j+s/M_j^2)|^2\,dx
 \le M_j\|u_0\|_2^2.
\tag{BJ.20}
\]

完整过去耗散和最近倍增窗耗散分别为

\[
 \begin{aligned}
 M_j^{-1}\int_{-M_j^2t_j}^{0}\!\int_{\mathbb T_{M_j}^3}
       |\nabla v_j|^2
 &=\int_0^{t_j}\!\int_{\mathbb T^3}|\nabla u|^2
 \le\frac12\|u_0\|_2^2,\\
 M_j^{-1}\int_{-D_j}^{0}\!\int_{\mathbb T_{M_j}^3}
       |\nabla v_j|^2
 &=\int_{t_{j-1}}^{t_j}\!\int_{\mathbb T^3}|\nabla u|^2
 \longrightarrow0.
 \end{aligned}
\tag{BJ.21}
\]

最后一个极限只用 BJ.19 中耗散的时间绝对连续性。它是在扩张
周期尺度 \(M_j\) 除过之后的结论，不能推出固定空间球上的
未归一化耗散趋零。

零均值、完整左端和周期／历史比例还给

\[
 \fint_{\mathbb T_{M_j}^3}v_j(s)=0,\qquad
 \|v_j(-M_j^2t_j)\|_\infty
   =M_j^{-1}\|u_0\|_\infty\to0,\qquad
 \frac{M_j^2t_j}{M_j^2}=t_j\to T_*.
\tag{BJ.22}
\]

## 5. 古老局部极限与终点

任意固定 \(S<\infty\) 最终都满足
\([-S,\sigma_*]\) 包含在 BJ.17 中。负时间 record 界
BJ.18 与正时间安全界 BJ.11，使标准 bounded-mild 内部估计可以
在固定紧柱上使用。经周期提升、峰值方向子列和对角选择，

\[
 v_j\longrightarrow v
 \quad\text{局部光滑地于 }
 \mathbb R^3\times(-\infty,\sigma_*],\qquad
 |v(0,0)|=1,\qquad
 \sup_{s\le0}\|v(s)\|_\infty\le1.
\tag{BJ.23}
\]

这里使用标准局部 mild 紧性接口，不把有限的能量账本冒充紧性
证明。正向闭区间严格短于 BJ.10 的存在余量，因此 \(s=0\)
是内部时刻，而不是只靠弱端点保留下来的峰值。

## 6. 有界 \(D_j\) 子列会排除常向量

现在额外假设某个子列满足 \(D_j\le C_D\)。BJ.9 后可再取

\[
 D_j\longrightarrow D\in[4c_*,C_D].
\tag{BJ.24}
\]

移动时间 \(s=-D_j\) 精确对应 \(t_{j-1}\)，所以

\[
 \|v_j(-D_j)\|_\infty
 =M_j^{-1}\|u(t_{j-1})\|_\infty=\frac12.
\tag{BJ.25}
\]

BJ.23 的局部光滑收敛同时给时间等度连续性。先固定任意空间点
\(y\)，再让 \(j\to\infty\)，得到

\[
 |v(y,-D)|\le\frac12\quad\text{对每个 }y\in\mathbb R^3,
 \qquad |v(0,0)|=1.
\tag{BJ.26}
\]

因此 \(v\) 不是时空常向量。这里不要求 \(x_j\) 接近前一
层最大点；BJ.25 使用的是前一时刻的全空间上界。正下界
\(D\ge4c_*\) 也排除了两个比较时刻合并。

## 7. 标量时间序列反检查

取

\[
 d_*>\max\{1,4c_*\},\qquad
 d_j=d_*+j^2,\qquad
 \Delta t_j=\frac{d_j}{M_0^2\,4^j}.
\tag{BJ.27}
\]

令 \(t_0=0\)、\(t_j=\sum_{k=1}^j\Delta t_k\)，并令
\(T^\sharp=\sum_{k\ge1}\Delta t_k<\infty\)。在每个
\([t_{j-1},t_j]\) 上，将标量 \(H_\sharp\) 从 \(M_{j-1}\)
线性增加到 \(M_j\)。则

\[
 H_\sharp(t_j)=M_j,\qquad
 M_j^2(t_j-t_{j-1})=d_j\longrightarrow\infty,\qquad
 t_j\uparrow T^\sharp<\infty.
\tag{BJ.28}
\]

在第 \(j\) 段，斜率为 \(M_j^3/(2d_j)\)，而
\(H_\sharp\ge M_j/2\)。由于 \(d_j>1\)，甚至有

\[
 H_\sharp'(t)\le4H_\sharp(t)^3
 \quad\text{在每个线性段的内部}.
\tag{BJ.29}
\]

此外

\[
 M_j^2(T^\sharp-t_j)
 =\sum_{m\ge1}4^{-m}d_{j+m}
 \sim\frac13j^2\longrightarrow\infty.
\tag{BJ.30}
\]

这个标量族不是 NS 解，也没有声称满足真实 NS 的能量、压力或
空间结构。它只严格否定以下自动推断：有限总时间、record 结构和
局部寿命型下界已经足以推出 \(D_j\) 有界子列。它不排除真实
NS 的其他动力学或能量改进将来给出更强结论。

## 8. Type I 附加条件的准确作用

若另加速度 Type I 条件

\[
 K_I:=\sup_{0\le t<T_*}\sqrt{T_*-t}\,\|u(t)\|_\infty
 <\infty,
\tag{BJ.31}
\]

则

\[
 \begin{aligned}
 D_j&=M_j^2(t_j-t_{j-1})
 \le M_j^2(T_*-t_{j-1})\\
 &=4M_{j-1}^2(T_*-t_{j-1})\le4K_I^2.
 \end{aligned}
\tag{BJ.32}
\]

所以 Type I 确实提供统一上界，并由 BJ.24--BJ.26 产生非恒定的
bounded ancient mild 极限。但本节没有由 BJ.19 的基本能量等式
推出 Type I，也不把它用于覆盖任意首次候选奇点。它只把常向量
障碍换成一般三维非恒定 bounded ancient mild 解的刚性问题；
后者在本稿中仍未付。

## 9. 路线边界

这次检查完成三件事。

1. 局部 mild 理论给 \(D_j\) 下界，不给上界。
2. 有限 \(T_*\) 只给 BJ.12--BJ.15；标量反检查说明这些时间
   账本不能自动产生有界子列。
3. 若真实 NS 另行给出有界子列，则古老极限必非恒定；但这仍不
   是一般古老解刚性或正则性证明。

因此我不把“\(T_*<\infty\) 自动给有界 \(D_j\) 子列”另起标题
当作正面桥梁。配套 BI 已完成固定初值完整 mild 历史检查：
它支付了一个随峰值增长的过去窗口之外的遥远尾部，却没有把终点
贡献压缩到固定归一化时间窗；在常向量极限分支中，每个固定过去
窗口之前的非线性项反而必须保留该常向量。故本稿不再把“检查
完整历史”列为尚未执行的下一项。若后续没有真正控制 BI 中未付的
中间时间有符号贡献，而只是重写 Type I 或一般古老解刚性，就应
停止。

本稿不证明合同 G、一般三维正则性、奇点存在或不存在，也不作
新颖性声明。没有仿真、科学图、DGX 或新读者 PDF。
