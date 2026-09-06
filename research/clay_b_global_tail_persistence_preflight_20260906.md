# 全环面高频尾的短时持留

2026-09-06。**INTERNAL / PROVED ON STRICT SMOOTH INTERVALS / INDEPENDENTLY CHECKED / NOT FROZEN / G OPEN / NOT CLAY。**

本稿只检验 AK、AN 之后的一个真实动力学问题：固定同一个平滑频率
阈值 \(K\)，若全环面高频尾在某个实际时刻很小，它能向前保持多久。
所有计算都在同一周期 Navier--Stokes 解的严格前奇点光滑区间内进行。
结论不延拓越过 \(T_*\)，也不把全域小尾等同于 AO 的局部小尾。

以下黏性归一化为 \(1\)，空间是
\(\mathbb T^3=(-\pi,\pi]^3\)，范数均不归一化。

## 1. 固定平滑分解与精确高频方程

沿用 AK 的实偶函数 \(\varphi\in C_c^\infty(\mathbb R^3)\)，其中
\(\varphi=1\) 于 \(\{|\xi|\le1\}\)，且
\(\varphi=0\) 于 \(\{|\xi|\ge2\}\)。定义

\[
 \widehat{S_Kf}(k)=\varphi(k/K)\widehat f(k),\qquad
 l=S_Ku,\qquad h=(I-S_K)u,\qquad K\ge1.
\tag{AT.1}
\]

\(S_K\) 不是幂等投影，但恒有 \(u=l+h\)。它与空间导数和周期
Leray 投影 \(\mathbb P\) 交换。由于 \(\varphi(0)=1\)，\(h\)
的空间均值为零；\(l,h\) 都无散。记

\[
 M=\sup_{0<\sigma<T_*}\|u(\sigma)\|_2,\qquad
 y(\sigma)=\|h(\sigma)\|_3,
\tag{AT.2}
\]

并在 \(q=|h|\) 的零集按标准正则化解释

\[
 H_h=\frac13y^3,\qquad
 D_h=\int_{\mathbb T^3}
 q\bigl(|\nabla h|^2+|\nabla q|^2\bigr)\,dx .
\tag{AT.3}
\]

原方程的 Leray 形式为

\[
 \partial_tu-\Delta u+\mathbb P\operatorname{div}(u\otimes u)=0.
\tag{AT.4}
\]

对 AT.4 施加 \(I-S_K\)，再只把 \(h\otimes h\) 移到左侧，得到
不使用 \(S_K^2=S_K\) 的精确恒等式

\[
 \boxed{\;
 \partial_th-\Delta h+\mathbb P\operatorname{div}(h\otimes h)
 =-\mathbb P\operatorname{div}
   (l\otimes h+h\otimes l+l\otimes l)
  +S_K\mathbb P\operatorname{div}(u\otimes u).
 \;}
\tag{AT.5}
\]

所以 \(h\) 不是一条无外力 Navier--Stokes 解。特别地，即使某时
\(h=0\)，右侧的低—低高频生成项也未必为零。

对任意张量 \(A\)，令零均值 \(\pi[A]\) 满足

\[
 -\Delta\pi[A]=\partial_i\partial_jA_{ij},\qquad
 \mathbb P\operatorname{div}A
 =\operatorname{div}A+\nabla\pi[A].
\tag{AT.6}
\]

后面分别使用
\(p_h=\pi[h\otimes h]\) 与
\(p_c=\pi[l\otimes h+h\otimes l]\)。低—低压力和低输出修正则
保留在一个完整向量强迫中，不拆掉其 Leray 配对。

## 2. 低频系数与真正的 \(K^3\) 强迫界

平滑周期 Bernstein 估计给

\[
 \|l\|_\infty\le C_\varphi M K^{3/2},\qquad
 \|\nabla l\|_\infty\le C_\varphi M K^{5/2}.
\tag{AT.7}
\]

定义

\[
 f_0:=-\mathbb P\operatorname{div}(l\otimes l)
       +S_K\mathbb P\operatorname{div}(u\otimes u).
\tag{AT.8}
\]

这里需要谨慎处理 Leray 乘子在零频附近并不光滑这一事实。令
\({\cal P}_K\) 是 \(S_K\) 的周期卷积核。由固定 Schwartz 核的
周期化和 \(K\ge1\)，

\[
 \|\nabla{\cal P}_K\|_{L^3(\mathbb T^3)}
 \le C_\varphi K^3.
\tag{AT.9}
\]

因而先在 Leray 投影之前估计，有

\[
 \begin{aligned}
 \|S_K\operatorname{div}(u\otimes u)\|_3
 &\le C K^3\|u\otimes u\|_1
 \le C M^2K^3.
 \end{aligned}
\tag{AT.10}
\]

另一方面，\(l\otimes l\) 的 Fourier 支撑在
\(\{|k|\le4K\}\)。插入一个在该球上恒为 \(1\) 的辅助平滑低通，
其导数核满足与 AT.9 相同的 \(L^1\to L^3\) 缩放，故

\[
 \|\operatorname{div}(l\otimes l)\|_3
 \le C K^3\|l\otimes l\|_1
 \le C M^2K^3.
\tag{AT.11}
\]

周期 Leray 投影在 \(L^3\) 上有界，并与 \(S_K\)、导数交换。
AT.10--AT.11 的输入都是散度，零 Fourier 模自动为零，所以
\(\mathbb P(0)\) 的取值无关紧要。由此得到真正的组合界

\[
 \boxed{\qquad \|f_0(\sigma)\|_3\le C_\varphi M^2K^3. \qquad}
\tag{AT.12}
\]

这不是把
\(\mathbb P\operatorname{div}\) 冒充为一个紧支撑光滑乘子。
等价地，也可把非零频率从 \(K\) 向下分成有限个周期环带；
每带的 \(L^1\to L^3\) 成本为 \(CQ^3\)，几何求和仍为
\(CK^3\)，没有额外对数。

## 3. \(q_\varepsilon\) 测试及全部压力项

取

\[
 q_\varepsilon=(|h|^2+\varepsilon^2)^{1/2},\qquad
 E_\varepsilon
 =\frac13\int_{\mathbb T^3}(q_\varepsilon^3-\varepsilon^3)\,dx,
\qquad
 D_\varepsilon
 =\int q_\varepsilon
   \bigl(|\nabla h|^2+|\nabla q_\varepsilon|^2\bigr)\,dx .
\tag{AT.13}
\]

以 \(q_\varepsilon h\) 测试 AT.5。因为 \(l,h\) 无散，
\(l\cdot\nabla h\) 与 \(h\cdot\nabla h\) 两个输运项分别成为
全散度；\(h\cdot\nabla l\) 不能消失。逐项积分分部给出

\[
 \begin{aligned}
 \frac{d}{d\sigma}E_\varepsilon+D_\varepsilon
 ={}&
 \int p_h\,h\cdot\nabla q_\varepsilon
 +\int p_c\,h\cdot\nabla q_\varepsilon\\
 &-\int q_\varepsilon h_i h_j\partial_jl_i
 +\int f_0\cdot(q_\varepsilon h).
 \end{aligned}
\tag{AT.14}
\]

AT.14 同时保留了自压力、交叉压力、低频应变、低—低项及
低输出修正；没有把任何投影压力静默删除。

先估自压力。加权 Cauchy--Schwarz、周期 Calderón--Zygmund
和 Hölder 给

\[
 \begin{aligned}
 \left|\int p_hh\cdot\nabla q_\varepsilon\right|
 &\le D_\varepsilon^{1/2}
      \left(\int |p_h|^2\frac{|h|^2}{q_\varepsilon}\right)^{1/2}\\
 &\le D_\varepsilon^{1/2}\|p_h\|_{9/4}\|h\|_9^{1/2},\\
 \|p_h\|_{9/4}
 &\le C\|h\|_3\|h\|_9.
 \end{aligned}
\tag{AT.15}
\]

不能从 \(|h|^{3/2}\) 的周期 Sobolev 中删去低阶项。正确的非齐次
估计是

\[
 \|h\|_9^{3/2}
 =\||h|^{3/2}\|_6
 \le C\bigl(D_\varepsilon^{1/2}+y^{3/2}\bigr).
\tag{AT.16}
\]

这里
\(\int |h||\nabla|h||^2\le
 \int q_\varepsilon|\nabla h|^2\le D_\varepsilon\)。
因此

\[
 \left|\int p_hh\cdot\nabla q_\varepsilon\right|
 \le CyD_\varepsilon
     +Cy^{5/2}D_\varepsilon^{1/2}.
\tag{AT.17}
\]

对交叉压力，周期 Riesz 有界性及 AT.7 给

\[
 \|p_c\|_3
 \le C\|l\otimes h+h\otimes l\|_3
 \le C\|l\|_\infty y.
\tag{AT.18}
\]

于是

\[
 \left|\int p_ch\cdot\nabla q_\varepsilon\right|
 \le D_\varepsilon^{1/2}\|p_c\|_3y^{1/2}
 \le C\|l\|_\infty y^{3/2}D_\varepsilon^{1/2}.
\tag{AT.19}
\]

剩下两项满足

\[
 \begin{aligned}
 \left|\int q_\varepsilon h_i h_j\partial_jl_i\right|
 &\le\|\nabla l\|_\infty
       \bigl(y^3+\varepsilon\|h\|_2^2\bigr),\\
 \left|\int f_0\cdot(q_\varepsilon h)\right|
 &\le CM^2K^3
       \bigl(y^2+C\varepsilon y\bigr).
 \end{aligned}
\tag{AT.20}
\]

在固定光滑紧区间令 \(\varepsilon\downarrow0\)，再对 AT.17、
AT.19 使用 Young 不等式。对任意固定 \(\theta>0\)，得到

\[
 \begin{aligned}
 \frac13(y^3)'&
 +(1-Cy-\theta)D_h\\
 &\le
 C_\theta y^5
 +C_\theta\|l\|_\infty^2y^3
 +\|\nabla l\|_\infty y^3
 +CM^2K^3y^2
 \qquad\text{a.e.}
 \end{aligned}
\tag{AT.21}
\]

正则化同时覆盖 \(h=0\)；没有在零尾处先除以 \(y^2\)。

## 4. 停止时间与定量持留

取只依赖固定环面、\(\varphi\) 与 Calderón--Zygmund 常数的小常数
\(0<\eta_*\le1\)，使 AT.21 在 \(y\le\eta_*\) 且固定
\(\theta\) 后至少保留 \(\frac12D_h\)。

这里的 \(\eta_*\) 是本稿全域尾的阈值；不预设它与 AO 局部阈值
数值相同，更不由阈值记号相同推断两个好时间集相同。令

\[
 A_K=1+MK^{5/2}+M^2K^3,\qquad
 F_K=M^2K^3.
\tag{AT.22}
\]

AT.7 与 AT.21 在停止区间 \(y\le\eta_*\) 上给

\[
 (y^3)'\le C A_Ky^3+C F_Ky^2.
\tag{AT.23}
\]

令 \(w=y^3\) 及 \(z_\rho=(w+\rho^3)^{1/3}\)。AT.23 给
\(z_\rho'\le CA_Kz_\rho+CF_K\)。Gronwall 后令
\(\rho\downarrow0\)，得到对停止区间内 \(s\le\sigma\)

\[
 y(\sigma)\le
 e^{CA_K(\sigma-s)}
 \bigl(y(s)+CF_K(\sigma-s)\bigr).
\tag{AT.24}
\]

选择只依赖上述固定常数的 \(c_*>0\)，并定义

\[
 \tau_K=c_*
 \min\left\{A_K^{-1},\,\frac{\eta_*}{F_K}\right\},
\tag{AT.25}
\]

其中 \(F_K=0\) 时第二项解释为 \(+\infty\)。若
\(y(s)\le\eta_*/4\)，AT.24 和连续性表明

\[
 y(\sigma)\le\frac34\eta_*
 \quad\text{只要}\quad
 s\le\sigma<T_*,\qquad \sigma-s\le\tau_K.
\tag{AT.26}
\]

证明是标准首次停止反证：若首次到达 \(\eta_*\)，则在此前
AT.24 有效；取 \(c_*\) 使指数至多 \(2\)、括号中的强迫增量至多
\(\eta_*/8\)，便在该首次时刻得到 \(y\le3\eta_*/4\)，矛盾。
AT.26 只使用原解已经光滑存在的时间；它不构造或延拓
\(\sigma\ge T_*\) 的解。

## 5. 与成熟窗口的尺度比较

回到 AK 的合法窗口

\[
 \Lambda=\|u(t)\|_{L^3(B_r)},\qquad
 K=\Lambda^{3/4},\qquad
 \delta=c_0r^2\Lambda^{-4},\qquad
 J=(t-\delta,t),
\tag{AT.27}
\]

其中 \(0<t<T_*\)、\(0<\delta<t\)、\(r,M,c_0\) 固定。
对 \(\Lambda\ge1\) 且 \(M>0\)，AT.22--AT.25 给

\[
 \tau_K\ge c_{M,\eta_*}\Lambda^{-9/4},\qquad
 \frac{\delta}{\tau_K}
 \le C_{M,\eta_*}c_0r^2\Lambda^{-7/4}
 \longrightarrow0.
\tag{AT.28}
\]

另一方面，周期 Bernstein 给终端低频界

\[
 \|l(t)\|_3\le CMK^{1/2}=CM\Lambda^{3/8}.
\tag{AT.29}
\]

若大 \(\Lambda\) 的窗口 \(J\) 中存在 \(s\) 使
\(\|P_{>K}u(s)\|_3\le\eta_*/4\)，则 AT.28 允许将 AT.26 用到
终端 \(t\)，于是

\[
 \Lambda
 \le\|u(t)\|_{L^3(\mathbb T^3)}
 \le CM\Lambda^{3/8}+\frac34\eta_*,
\tag{AT.30}
\]

这在 \(\Lambda\to\infty\) 时矛盾。因此，对固定数据的任意合法
大范数序列，最终都有

\[
 \boxed{\quad
 \|P_{>\Lambda^{3/4}}u(\sigma)\|_3>\frac14\eta_*
 \quad\text{对每个 }\sigma\in J.
 \quad}
\tag{AT.31}
\]

这里每个窗口使用由其终端 \(\Lambda\) 固定下来的同一个 \(K\)；
不是随 \(\sigma\) 改变的截断。若 \(M=0\)，解恒为零，不存在
\(\Lambda\to\infty\) 的支路。

结合 AK.15，
\(\|P_{>K}u\|_3^2\le CK^{-1}\|\nabla u\|_2^2\)，AT.31 只给

\[
 A_J:=\int_J\|\nabla u\|_2^2\,d\sigma
 \ge c\eta_*^2K\delta
 =c\,c_0r^2\eta_*^2\Lambda^{-13/4}.
\tag{AT.32}
\]

右侧仍趋于零，所以它与有限总耗散及积分绝对连续性完全相容。
它不是成熟窗口闭合。

## 6. 精确边界

AT.5 是固定平滑截断的完整高频方程；AT.12 保留了低—低和低输出
修正的真实 \(M^2K^3\) 成本；AT.14--AT.21 保留了自压力、
交叉压力与低频应变；AT.25--AT.31 给出严格光滑时间内的全域尾
持留及其对成熟窗口的必要机制。

AT.31 只排除了全环面尾在该窗口某时降到固定小阈值。AO 的好时间
条件是 \(\|\theta P_{>K}u\|_3\) 小；全域尾可以集中在
\(\theta\) 之外，所以 AT.31 不排除 AO 的局部好时间，也不给
坏集合净压力功的上界。局部化 AT.5 还会重新产生非局部投影、
交换子、远压力与环带项，AP 的固定正则环带不能自动支付这些项。

本稿不证明合同 G、首次奇点排除或 Clay 正则性，不宣称新颖性，
不含仿真、科学图、提交或发布动作。
