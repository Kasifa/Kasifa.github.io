# R0.75A Step 26 publication reader source

## 206. 结论先行：任意短的 endpoint focusing 也必须付款

在冻结的光滑周期 common-shear family 中，W-remote 正体积 endpoint core 不能靠把时间集中压到任意短来逃避 cubic payment。对完整总场 F 直接使用 moving-cutoff 恒等式后，只有两个穷尽分支：局部能量在长度 c R^3 的回看窗内保持，或者它的快速上升本身由同一个扩大 moving strip 内的质量支付。两支都给出同一个 spacetime lower bound；这关闭了 R0.74Z 留下的 critical 与 arbitrarily shorter smooth focusing 逃逸，但没有控制完整时钟 K。

## 207. 精确 common-shear 闭合与移动坐标

速度 u=(F,b,0) 由同一奇剪切 b 与任意有限个被动 packet、inversion partner 的总和构成，仍是光滑、周期、零均值、无外力且压力为零的精确 Navier--Stokes 解。沿参考高度的水平平移 z=x_2-Q_2(t) 后，总场满足带残余剪切 c(t,x_3) 的线性漂移扩散方程。证明始终作用于总场，因此已经包含 packet、corrector、inversion partner 与全部周期 winding 的相消或叠加。

## 208. A.18：moving-cutoff 局部能量恒等式

取固定在移动坐标中的非负 cutoff phi，使其在 endpoint core 上为一并支撑于扩大 remote strip。精确积分分部给出

\[
\frac12 E'(t)+\int \phi |\nabla_{z3}\widetilde F|^2
=\frac12\int\bigl(c\,\partial_z\phi+\Delta_{z3}\phi\bigr)|\widetilde F|^2.
\]

冻结几何满足 \(|c|\lesssim R^{-2}\)、\(|\partial_z\phi|\lesssim R^{-1}\)、\(|\Delta\phi|\lesssim R^{-2}\)；在 \(R\le 1\) 时，误差统一由 \(K_\phi R^{-3}\) 乘以 enlarged-strip mass 控制。这里的 transport sign 与 \(R^{-3}\) 次数已由双实现证书锁定。

## 209. A.26：persistence 与 rapid-rise 两支穷尽

令 \(E_*\) 为 endpoint core 的总场 \(L^2\) 能量，并回看 \(J=[t_2-c_0R^3,t_2]\)。若 \(E(t)\) 在 \(J\) 上始终不少于 \(E_*/2\)，直接积分得到 \(X=\int_JM(t)\,dt\ge c_1E_*R^3\)。若不然，存在较早时刻能量跌到 \(E_*/2\) 以下；积分 A.18 便把至少 \(E_*/2\) 的上升充入同一 \(M(t)\)，仍得到相同 lower bound。不存在第三分支，persistent、critical 与任意更短的光滑 endpoint focusing 均已覆盖。

## 210. 从局部 L2 质量到 Version-M cubic payment

扩大 tube 的 spacetime 体积至多为 \(CL^{1/2}R^6\)。Hölder 因而把 A.26 转成 \(\int|F|^3\gtrsim E_*^{3/2}R^{3/2}L^{-1/4}\)。该 tube 位于 scale \(2R\) 的 exterior row，且权重至少为 \(\omega^{1/4}\)，所以

\[
P_R^M\gtrsim \omega^{1/4}E_*^{3/2}R^{-1/2}L^{-1/4}.
\]

再代入 endpoint lower \(E_*\ge (2R/\omega)h_{\rm rem}\)，得到冻结主结论

\[
(P_R^M)^{2/3}\gtrsim h_{\rm rem}R^{2/3}\omega^{-5/6}L^{-1/6}.
\]

## 211. 精确指数余量

冻结参数 omega=Gamma^(1/4)；从 remote clock 到 doubled-radius payment 的可见权重是 omega^(1/4)=Gamma^(1/16)，不能重复使用 Gamma^(1/4)。全部 R、L、omega 次数代入后，严格正余量为

\[
\frac5{24}\frac8{3969}-\frac16\frac9{10000}
=\frac{64279}{238140000}>0.
\]

这个结论是精确有理数账本，不是数值拟合。证书同时拒绝 reciprocal p、错误 transport sign、R^-2 或 R^-4 cutoff、错误 omega 权重、遗漏 critical/shorter 分支以及 full-clock promotion。

## 212. Fourier 账本的正确用途与限制

水平 Fourier 模态满足精确能量衰减；向前高频衰减与向后放大因子可以逐模态写出。但水平 band 不是完整 generator control，全局 modal energy 也不是自动的局部 strip payment。若改走一般 observability，常数会依赖缩小几何、频率与 conditioning；本 lemma 不需要把这种常数静默设成统一常数，因为 moving-cutoff 直接对总场工作。

## 213. 文献边界：最近先例不是 novelty 证据

Wang--Wang--Zhang--Zhang, arXiv:1711.04279, Section 3.2 的纯热方程 nested-cutoff inner-endpoint / outer-spacetime estimate 是最近的方法先例；在 T about R^3、r-r' about R 时也呈现主导 R^-3 尺度。R0.75A 增加的是残余剪切、移动周期各向异性 strip、shell weight 与 Version-M cubic conversion。七篇一手来源的 bounded screen 没有发现直接覆盖全部链条的定理，但这种有限未命中不证明 novelty、priority、nonexistence、correctness 或 publishability。

## 214. 证据等级与冻结复核

解析主文与 primary audit 的结论等级是 theorem/lemma；Python 证书 14/14、独立 Ruby 17/17，并对 8 个 targeted mutations fail-closed，它们只复核精确有理数、哈希、公式 sentinels、指数和边界，不替代连续 PDE 证明。正式图档共 25 个文件、2,588,462 bytes，SVG/PNG/PDF 主件与 manifest、validation、QA 均按冻结哈希发布；图是 analytic schematic，不是 PDE simulation、DNS、sampled trajectory 或 empirical fit。

## 215. 停止线与下一命题 A.63

PROVED 仅限精确光滑有限 common-shear family 的 W-remote endpoint persistence/payment dichotomy，以及相应 horizontal modal identities。完整 completed clock K、accumulated/off-target rows、whole-shell upper、fixed deletion、任意 suitable weak solution 延拓、scale contraction、regularity 与 singularity 均仍 OPEN。下一命题 A.63 是 remote complete-clock extraction：必须同时控制 endpoint、accumulated 与 off-target rows，且不得把 strip lower 改写成 whole-shell upper。NO NOVELTY CLAIM. NOT CLAY.
