# R0.75F Step 31 reader source

## 1. 结论先行：相位积分精确回收离对角账本，但不给出新估计

对 \(g_{nm}=f_n\overline{f_m}\) 与 \(\ell=m-n\)，把 modal-product equation 代回 R0.75E 的 signed collar flux，并在时间与 \(x_3\) 上分部积分，精确得到

\[
\boxed{
\mathcal T_\xi
=\mathcal E_{\rm off}
-\mathcal A_{\rm off}
+\mathcal D_{\rm off}.}
\]

这三项正是原 localized energy identity 的 off-diagonal endpoint、cutoff 与 dissipation rows。代回后全部相消，只留下 diagonal modal identity。因而 direct modal phase integration 是原能量恒等式的离对角投影，不产生独立符号、小因子或 observability bound。

## 2. 精确 modal-product equation：无须除以剪切或差频

两个模式方程分别含 \(-inbf_n\) 与 \(+imb\overline{f_m}\)。乘积求导并使用 vertical product rule，得到

\[
\boxed{
i\ell b g_{nm}
=\partial_tg_{nm}-g_{nm}''
+2f_n'\overline{f_m}'
+(n^2+m^2)g_{nm}.}
\]

这里 \(\ell=m-n\)，cross-gradient coefficient 必须是 \(2\)。等式没有除以 \(b\) 或 \(\ell\)，因此在 shear zeros 处仍成立；它本身只是代数恒等式，不是 oscillatory estimate。

## 3. diagonal/off-diagonal forms 与归一化

在 frozen \(1/(2\pi)\) Fourier convention 下，endpoint 与 cutoff rows 来自 half-energy，系数为 \(\pi\)；dissipation row 使用整周期因子 \(2\pi\)。horizontal-gradient product 为

\[
(in)(-im)g_{nm}=nm\,g_{nm}.
\]

完整分解为

\[
\mathcal E_{\rm diag}+\mathcal E_{\rm off}
+\mathcal D_{\rm diag}+\mathcal D_{\rm off}
=\mathcal A_{\rm diag}+\mathcal A_{\rm off}
+\mathcal T_\xi.
\]

任何遗漏 endpoint、改动 transport sign，或把 dissipation 的 \(2\pi\) 改成 \(\pi\)，都会破坏冻结证书。

## 4. 两次分部积分与完全相消

因为 \(\eta_R(s_R)=0\)、\(\eta_R(t_2)=1\)，时间导数给出 terminal off-diagonal endpoint 减去 \(\eta_R'\) cutoff row。周期 \(x_3\) 分部积分给出

\[
-\int\eta_R\Xi_\ell g_{nm}''
=-\int\eta_R\Xi_\ell''g_{nm}.
\]

再用

\[
n^2+m^2=(m-n)^2+2nm=\ell^2+2nm,
\]

所有项无余项地组装成 \(\mathcal E_{\rm off}-\mathcal A_{\rm off}+\mathcal D_{\rm off}\)。代回完整 identity 后得到

\[
\boxed{
\mathcal E_{\rm diag}+\mathcal D_{\rm diag}
=\mathcal A_{\rm diag}.}
\]

## 5. 为什么这是一条 proof-route no-go

最后的 diagonal identity 也可以逐个模式直接乘以 \(\eta_R\Xi_0\overline{f_n}\)、取实部得到。因此 circular phase substitution 只重写了同一账本，没有添加 resolvent、hypocoercivity、trajectory separation、residence time 或 payment sensitivity。

冻结 two-mode closed solution 先从 \(i\ell bg\) 独立计算 transport，再分别检查 time/vertical integration by parts 以及两个 energy identities；其 F.12、F.17 与 F.18 residual 均精确为零。这排除了“证书先假定待证 identity”的循环。

## 6. cutoff 正性也不能单独控制 localized form

对奇数 \(N=2M+1\)，取 real Dirichlet/Fejer family

\[
D_N=\sum_{k=-M}^{M}e^{ikx},
\qquad
a_N=\frac{D_N}{\sqrt N},
\qquad
X_N=\frac{|D_N|^2}{N^2}.
\]

它满足 \(0\le X_N\le1\)、\(\langle X_N\rangle=1/N\)、\(\langle|a_N|^2\rangle=1\)，但 ordered difference counts 给出

\[
\langle|D_N|^4\rangle
=\frac{2N^3+N}{3},
\qquad
\frac{\langle X_N|a_N|^2\rangle}
{\langle X_N\rangle\langle|a_N|^2\rangle}
=\frac{2N+N^{-1}}3\longrightarrow\infty.
\]

精确有限值为 \(N=3,5,7\) 时依次 \(19/9\)、\(17/5\)、\(33/7\)。这只否定 positivity-only diagonal comparison；该 family 不是 frozen geometric collar，也不是 E.24 的 counterexample。

## 7. 下一条成功估计必须加入真正的新信息

- quantitative uncertainty：把 \(x_2\)-thin collar concentration、horizontal frequency 与 heat damping 联结起来；
- resolvent 或 hypocoercive estimate：利用整个时间窗内的 shear phase，而非代数替换；
- pathwise residence-time bound：控制轨道在 fixed collar 中的停留；
- payment-sensitive positive Toeplitz bound：直接控制正 signed off-diagonal form。

这些方向仍可行，但本节均未证明。任意实场 E.24、complete-clock extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 保持 OPEN。

## 8. 冻结证据、文献边界与停止线

Primary analytic audit 为 PASS，mathematical blockers 0、release blockers 0。Python certificate 为 16/16，独立 Ruby 为 20/20；双方各拒绝 43/43 定向 mutations，unknown mutations fail closed，三个 hash seeds 与 regeneration 均字节稳定，F.1--F.23 与 23/23 displays 完整解析。冻结 ledger 为 12/12，并显式包含两套验证器直接依赖的 fixtures 与 expected JSON。

bounded primary-source screen 只确认：实际 enhanced dissipation 使用 resolvent/semigroup 等额外信息；pathwise 方法加入 trajectory information；physical localization 保留 drift flux。有限 non-hit 不构成 completeness、novelty、priority、correctness 或 publishability 判断。

\[
\boxed{\textbf{PHASE SUBSTITUTION TAUTOLOGICAL; POSITIVITY-ONLY DIAGONAL CONTROL FALSE; E.24 OPEN; NOT CLAY.}}
\]

R0.75F 只裁剪两条证明路线，不构造 frozen-collar counterexample。complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均未闭合。后续工作未读取、未公开。本节无正式图、simulation、DNS 或 DGX。
