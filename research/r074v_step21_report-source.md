# R0.74V｜完整时钟上界路线备忘录：精确分解、粗预算与开放占用门

## 1. 结论先行：这是路线备忘录，不是上界定理

R0.74V 把 completed-clock upper 的证明义务拆成可核查的账本。已建立的是精确分解、粗尺度预算、条件代数和失败条件；目标坐标上界与全壳层上界均未建立。R0.74U 的认证几何走廊仍只给 `K` 超水平集的单向包含和下测度界，不能反向使用。

## 2. 完整时钟的三行非负账本

在 local-energy good times，完整时钟由端点动能、累积普通黏性和累积异常缺陷三行组成。对一般 suitable weak solution，hard time 必须使用 canonical absolutely continuous representative；不能把原始端点表达式强行解释为处处成立。冻结光滑族的异常缺陷为零，但推广时仍须单独保留。

## 3. shear、packet 与交叉项

对精确 common-shear 解，速度分量正交给出

\[
K_{k,R}=K^b_{k,R}+K^G_{k,R}.
\]

展开两个 packet 后，端点与黏性交叉项有符号，但 Cauchy-Schwarz/Young 将它们安全吸收到两条对角行：

\[
K_{k,R}(t)\le K^b_{k,R}(t)+2\sum_{m=1}^2\bigl(E_k^m(t)+D_k^m(t)\bigr).
\]

这解决了点态上界中的交叉项，却不自动控制 positive variation。

## 4. lifted multiplicity 不能被 torus 长度截断

周期化 cutoff 是欧氏 lift 的和，不是投影后的 `0-1` 指示函数。令 `s_k=(2^{k+1}+1/8)R`，正确的一维弦长预算是

\[
\ell_k=s_k+s_k^3.
\]

同理，体积使用精确平铺恒等式

\[
\int_{\mathbb T^3}\Psi_k^R=\int_{\mathbb R^3}\psi_k^R,
\]

而不是用一个 torus 体积上限抹去 lifted multiplicity。

## 5. 已有的粗尺度预算

全局 packet 能量与 lifted chord 给出 `H_{k<-m}=gamma_k a_m^2 ell_k R` 级别的端点加黏性上界。common-shear 则形成持续基线；目标壳层上其归一化尺度为 `Xi_i^sh ~ Gamma_i B^2 L_i^3/A_*^2`。若这条基线没有严格低于 `kappa T`，时长上界可能直接失败。全壳层 shear 求和还要求 `B^2/A_*^2` 受控，因此不能对 R0.74U 允许的任意 `A_*>0` 给出统一结论。

## 6. V.47-V.50：有限表 occupation 仍是开放输入

当前只提出六个 central-chart pair 上的 whole-annulus moving-centre `L^2/H^1` occupation 估计。它必须同时处理 inversion partners、periodic copies、weighted remainders、累积黏性和 derivative collar。现有 near-lobe 比较只覆盖主叶附近，不能替代这组全 annulus 估计。V.47-V.50 仍为 OPEN；任何 all-k 使用还须另证 lifted-copy summation。

## 7. V.56 只有条件代数，没有解析闭合

若 common-shear、两条累积黏性与异常缺陷组成的 persistent baseline 小于 `kappa T/2`，并且 V.47-V.50 的 weighted remainder gates 全部通过，则 union bound 把目标坐标超水平集约化到两个 packet endpoint 集合，形式上得到

\[
|\{t\in I_R:K_{k_i,R}(t)\ge\kappa T\}|\le C_\kappa L_iR^3.
\]

这就是 V.56 的条件路线。因为 occupation inputs 尚未证明，V.56 本身仍为 OPEN。

## 8. adjacent-inward free comparator 给出正指数

在相邻内壳层，权重增益与自由热核尾部代价组合成

\[
\chi(65)=\frac{12191}{132088320}>0.
\]

这是 exact finite arithmetic，说明 free comparator 预测一个指数放大的 inward tail。但它不是 common-shear solution 的下界。还必须证明 remote strip 上的相对 bridge comparison、inversion control 和另一 packet 的 noncancellation；因此不能据此宣布全壳层反例。

## 9. 七类失败条件

路线会在以下任一处失败：common-shear floor 过高；黏性或异常缺陷形成永久基线；加权尾部余项不可积；广义尺度过慢；把 terminal plateau 错当成完整 cutoff interval；混淆 height、duration 与 variation；或在大壳层错误复用单一 central-lift distance。每一项都必须在定理陈述中成为显式假设或已证估计。

## 10. 停止线与下一项研究

下一项最小命题是 common-shear remote adjacent-inward comparison；之后才是六对有限表的 weighted annular occupation。以下全部保持 OPEN：V.47-V.50、V.56、所有 all-k lifted-copy extension、common-shear remote/adjacent-inward comparison、all-shell matching upper、fixed deletion、arbitrary-clock extraction、scale contraction、regularity、singularity 与 Navier-Stokes Millennium problem。本发布没有文献审计，不作 novelty、priority 或 publishability 判断；没有 DNS、仿真或 PDE 数据。正式图件：NOT APPLICABLE。本节纯解析，没有 Navier--Stokes 数值仿真、DNS、DGX 或正式图件。**NOT CLAY.**
