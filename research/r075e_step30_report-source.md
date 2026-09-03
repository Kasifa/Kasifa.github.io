# R0.75E Step 30 reader source

## 1. 结论先行：大背景不等于大通量，实零模已获得全支付闭合

对 frozen common-shear equation

\[
(\partial_t+b(t,x_3)\partial_2-\Delta_{23})F=0,
\]

固定 physical collar cutoff 产生的 transport flux 只含不同 horizontal modes 之间的差频耦合。所有 diagonal terms \(n=m\) 精确消失。因此，对任意 admissible real horizontal zero mode，

\[
\boxed{
\partial_2F=0
\Longrightarrow
D_{k,R}^{{\rm out},F}\le C(P_R^M)^{2/3}
\quad(L\ge L_0).}
\]

该结论不要求 \(P_R^M\le1\)，也允许任意高 vertical frequency。R0.75D 的高 vertical-frequency zero mode 只阻止 horizontal-to-full Rayleigh inference，并不阻止目标耗散估计。

## 2. 带终端项和正确符号的 localized energy identity

令 \(\xi=\xi_k^R(x_1,x_2,x_3)\)，并保留 frozen time cutoff \(\eta_R\)。乘以 \(\eta_R\xi\overline F\)、积分并取实部，得到

\[
\begin{aligned}
&\frac12\int_{\mathbb T^3}\xi|F(t_2)|^2
+\int_{s_R}^{t_2}\!\int_{\mathbb T^3}\eta_R\xi|\nabla_{23}F|^2\\
&\qquad=\frac12\int_{s_R}^{t_2}\!\int_{\mathbb T^3}
[\eta_R'\xi+\eta_R\Delta_{23}\xi]|F|^2
+\mathcal T_\xi(F,b),
\end{aligned}
\]

其中

\[
\mathcal T_\xi(F,b)
:=\frac12\int_{s_R}^{t_2}\!\int_{\mathbb T^3}
\eta_Rb\,\partial_2\xi\,|F|^2.
\]

右侧 transport sign 为正；终端 endpoint 非负，只能在上界中丢弃，不能暗中等同于 payment row。

## 3. 精确的 horizontal difference-frequency identity

因为 \(b=b(t,x_3)\) 与 \(x_2\) 无关，每个 horizontal mode 独立演化：

\[
\partial_tf_n-\partial_3^2f_n+(n^2+inb)f_n=0.
\]

以 \(\Xi_\ell(x_3)=\int_{-\pi}^{\pi}\widehat\xi_\ell(x_1,x_3)\,dx_1\) 表示 cutoff 的 \(x_1\)-平均，transport flux 精确写成

\[
\boxed{
\mathcal T_\xi(F,b)
=\pi\operatorname {Re}\sum_{n,m\in\mathbb Z}i(m-n)
\int\eta_Rb\,\Xi_{m-n}f_n\overline{f_m}.}
\]

因 multiplier \(i(m-n)\) 在 \(n=m\) 时为零，通量是纯 off-diagonal difference-frequency quantity。大 background cubic atom \(p_b\) 本身不能推出大 localized transport flux。

## 4. zero-flux spectral sectors 与实零模

horizontal support \(S\) 由 modal equation 保持。若

\[
\Xi_{m-n}=0
\qquad(n,m\in S,\ n\ne m),
\]

则所有 off-diagonal summands 消失，\(\mathcal T_\xi(F,b)=0\)。这是充分的 spectral-orthogonality condition，不声称 generic radial collar 对非平凡实支撑都满足它。

特别地，\(S=\{0\}\) 是真实可容许的不变子空间；此时 \(|F|^2\) 与 \(x_2\) 无关，周期积分直接消去 \(\partial_2\xi\)。这包括任意高 vertical sine modes。

## 5. 零通量扇区的 pure two-thirds payment

保留 local cubic atom

\[
p_F:=R^{-2}\omega\int_{I_{2R}}\!\int_{\operatorname{supp}\xi}|F|^3,
\qquad p_F\le CP_R^M.
\]

当 transport flux 为零时，time/Laplacian cutoff rows 与 spacetime Hölder 给出

\[
\begin{aligned}
D_{k,R}^{{\rm out},F}
&\le C\omega R^{-3}\int|F|^2\\
&\le CL^{2/3}\omega^{1/3}p_F^{2/3}\\
&\le CL^{2/3}\omega^{1/3}(P_R^M)^{2/3}.
\end{aligned}
\]

又因 \(L^{2/3}\omega^{1/3}=L^{2/3}\exp[-(c_\gamma/12)L^2]\to0\)，故充分大的 \(L\) 上得到全支付 \(P^{2/3}\) bound；无需 R0.75D 的 interaction hypothesis。

## 6. 现实性边界：complex singleton 不是物理实场

nonzero complex singleton 也有零 flux，但它只是 complexified scalar diagnostic，不能提升为 physical real Navier--Stokes velocity。真实场满足 \(f_{-n}=\overline{f_n}\)，所以 nonzero real harmonic 具有成对支撑 \(\{n,-n\}\)，其 \(2n\) difference frequency 一般会耦合 cutoff。

冻结有限 witness

\[
\Xi(x)=2+\cos(2x)+\sin(2x),
\qquad
F(x)=2\cos x+\sin x
\]

同时由直接 Laurent multiplication 与 ordered off-diagonal sum 得到

\[
\boxed{\mathcal T_\xi/\pi=-\frac12\ne0.}
\]

该 witness 只验证 signed convolution 的代数归一化；它不是完整 spacetime trajectory，也不是 geometric collar 的有限模型。

## 7. 任意实场的精确剩余 gate

定义目标归一化下的正 signed cross-mode flux

\[
\mathfrak X_{\xi,R}(F,b)
:=\frac{\pi\omega}{R}
\left[\operatorname {Re}\sum_{n\ne m}i(m-n)
\int\eta_Rb\,\Xi_{m-n}f_n\overline{f_m}\right]_+.
\]

则 exact reduction 为

\[
\boxed{
D_{k,R}^{{\rm out},F}
\le CL^{2/3}\omega^{1/3}(P_R^M)^{2/3}
+\mathfrak X_{\xi,R}(F,b).}
\]

任意实场所需的下一命题是

\[
\boxed{\mathfrak X_{\xi,R}(F,b)\le C(P_R^M)^{2/3}.}
\]

这一 signed phase-mixing / difference-frequency gate 尚未证明。general real \(\pm n\) pairs、cross-mode aggregation、cutoff Fourier tails 与 localized observability 都保持 OPEN。

## 8. 冻结证据、文献边界与停止线

Primary analytic audit 为 PASS，mathematical blockers 0、release blockers 0。Python certificate 为 13/13，独立 Ruby 为 16/16；双方各拒绝 39/39 定向 mutations，unknown mutations fail closed，三个 hash seeds 字节一致，E.1--E.24 与 24/24 displays 完整解析。

bounded primary-source screen 只支持相邻机制：shear 保持 streamwise modes；streamline average 解一维 diffusion；physical localization 保留 drift flux。没有检索到本站 spherical-collar convolution 与 Version-M payment 的组合定理；finite non-hit 不构成 completeness、novelty、priority、correctness 或 publishability 判断。

\[
\boxed{\textbf{REAL ZERO MODE PAID FOR ALL PAYMENT; GENERAL CROSS-MODE GATE OPEN; NOT CLAY.}}
\]

R0.75E 在任意实场的 signed cross-mode gate 停止。complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均未闭合。R0.75F/G/H 与其他后续工作未读取、未公开。本节无正式图、simulation、DNS 或 DGX。
