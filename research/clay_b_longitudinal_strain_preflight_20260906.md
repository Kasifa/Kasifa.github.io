# 纵向幅值应变的真实 NS 演化：符号预检

2026-09-06。**LOCAL DERIVATION / CURRENT ESTIMATE UNCLOSED / NOT CLAY。**

本稿只做黏性 \(\nu=1\) 的光滑周期 Navier--Stokes 方程中的局部代数。
设
\[
 \partial_tu_i+u_k\partial_k u_i-\Delta u_i+\partial_i p=0,
 \qquad \partial_i u_i=0,
\tag{AE.1}
\]
并记
\[
 {\cal L}=\partial_t+u\cdot\nabla-\Delta,\qquad
 q=|u|,\qquad e=\frac{u}{q},\qquad
 A_{ij}=\partial_j u_i,\qquad
 F=-e\cdot\nabla q=-e^TAe.
\tag{AE.2}
\]
以下点态公式只在开集 \(\{q>0\}\) 内使用。本稿若对其中的
\(q^{-1}\) 系数使用逐点一致上界，就把区域进一步限制在
\(\{q\ge\kappa\}\)，其中 \(\kappa>0\) 固定。这是一个额外的局部
非退化条件，不由有限能量或首次奇点框架自动给出。
这不排除另行建立无需正下界的加权积分估计；本稿尚未建立这种估计。

## 1. 算子规则与几何恒等式

对标量、向量或矩阵分量，\({\cal L}\) 满足
\[
 {\cal L}(fg)=f{\cal L}g+g{\cal L}f
              -2\partial_kf\,\partial_kg,
 \qquad
 {\cal L}(\partial_j f)
 =\partial_j({\cal L}f)-(\partial_j u_k)\partial_kf.
\tag{AE.3}
\]
第二式是输运项与空间微分的交换子；负号来自
\(\partial_j(u_k\partial_kf)
=u_k\partial_k\partial_jf+(\partial_j u_k)\partial_kf\)。

令
\[
 G_k=\partial_k e,\qquad
 E^2=|\nabla e|^2=\sum_k|G_k|^2,\qquad
 \Pi=I-e\otimes e .
\]
由 \(u=qe\) 和 \(|e|=1\)，
\[
 \partial_k u=e\,\partial_kq+qG_k,\qquad
 \nabla q=A^Te,\qquad
 |\nabla u|^2=|\nabla q|^2+q^2E^2.
\tag{AE.4}
\]
再令 \(d=(e\cdot\nabla)e\)。因为 \(e\cdot d=0\)，且
\(e\cdot\nabla q=-F\)，还有
\[
 Ae=(e\cdot\nabla)u=-Fe+qd.
\tag{AE.5}
\]

## 2. 幅值方程 \({\cal L}q\)

由 AE.1，
\[
 (\partial_t+u\cdot\nabla)q
 =e\cdot(\Delta u-\nabla p).
\]
对 AE.4 求和并使用 \(e\cdot G_k=0\)，可得
\[
 \Delta q=e\cdot\Delta u+qE^2.
\]
因此
\[
 \boxed{{\cal L}q=-e\cdot\nabla p-qE^2.}
\tag{AE.6}
\]
等价地，
\[
 {\cal L}q
 =-e\cdot\nabla p
  -\frac{|\nabla u|^2-|\nabla q|^2}{q}.
\tag{AE.7}
\]
这里 \(-qE^2\le0\) 是幅值方程中唯一立即可见的有利点态项；
压力方向导数没有符号。

## 3. 方向方程 \({\cal L}e\)

乘积律给
\[
 -\nabla p={\cal L}u
 =q{\cal L}e+e{\cal L}q-2(\partial_kq)G_k .
\]
代入 AE.6，得到
\[
 \boxed{
 {\cal L}e
 =-\frac1q\Pi\nabla p
   +\frac2q\sum_k(\partial_kq)G_k
   +eE^2.}
\tag{AE.8}
\]
系数 \(2\) 来自 \(-\Delta(qe)\) 的交叉项。
取与 \(e\) 的内积可得 \(e\cdot{\cal L}e=E^2\)，于是
\[
 {\cal L}|e|^2=2e\cdot{\cal L}e-2|\nabla e|^2=0,
\tag{AE.9}
\]
与 \(|e|=1\) 一致。这同时核对了 AE.8 中最后一项的正号。

## 4. 速度梯度方程 \({\cal L}A\)

对 \({\cal L}u_i=-\partial_i p\) 使用 AE.3 的交换子，
\[
 \begin{aligned}
 {\cal L}A_{ij}
 &=\partial_j({\cal L}u_i)
   -(\partial_j u_k)\partial_k u_i\\
 &=-\partial_{ij}p-A_{kj}A_{ik}
  =-\partial_{ij}p-(A^2)_{ij}.
 \end{aligned}
\]
即
\[
 \boxed{{\cal L}A=-A^2-\nabla^2p.}
\tag{AE.10}
\]
取迹得到
\[
 0={\cal L}\operatorname{tr}A
   =-\operatorname{tr}(A^2)-\Delta p,
\tag{AE.11}
\]
恰好恢复压力 Poisson 方程。这核对了 AE.10 的矩阵次序和两个负号。

## 5. 纵向量 \(F\) 的完整方程

记
\[
 b=\nabla p,\qquad {\mathcal H}=\nabla^2p,\qquad
 c=\sum_k(\partial_kq)G_k,\qquad h={\cal L}e.
\tag{AE.12}
\]
直接对 \(F=-e_iA_{ij}e_j\) 使用三因子乘积律，并代入 AE.10，得
\[
 \begin{aligned}
 {\cal L}F={}&e^T(A^2+{\mathcal H})e-h^TAe-e^TAh\\
 &+2\sum_k\Big[
   G_k^T(\partial_kA)e
  +G_k^TAG_k
  +e^T(\partial_kA)G_k\Big].
 \end{aligned}
\tag{AE.13}
\]
三个扩散交叉项的系数均为 \(+2\)：先对
\(e^TAe\) 使用 \({\cal L}\) 会产生 \(-2\) 的三组交叉项，
再由 \(F=-e^TAe\) 反号。

将 AE.8 即
\[
 h=-q^{-1}\Pi b+2q^{-1}c+eE^2
\]
完全代入 AE.13，可写成
\[
 \boxed{
 \begin{aligned}
 {\cal L}F={}&e^T(A^2+{\mathcal H})e\\
 &+\frac1q\Big[(\Pi b)^TAe+e^TA(\Pi b)\Big]\\
 &-\frac2q\Big[c^TAe+e^TAc\Big]+2FE^2\\
 &+2\sum_k\Big[
   G_k^T(\partial_kA)e
  +G_k^TAG_k
  +e^T(\partial_kA)G_k\Big].
 \end{aligned}}
\tag{AE.14}
\]
特别地，\(2FE^2\) 的正号来自
\(-2E^2 e^TAe=2FE^2\)。

还可以从 \(F=-e\cdot g\)、\(g=\nabla q\) 独立重算。
由 AE.3，
\[
 {\cal L}g_j=\partial_j({\cal L}q)-A_{kj}g_k,
\]
从而
\[
 {\cal L}F
 =-({\cal L}e)\cdot g-e\cdot\nabla({\cal L}q)
   +g\cdot Ae+2\sum_kG_k\cdot\partial_kg.
\tag{AE.15}
\]
将 AE.6 和 AE.8 代入，\(FE^2\) 的两项正好抵消，得到等价形式
\[
 \boxed{
 \begin{aligned}
 {\cal L}F={}&e^T{\mathcal H}e+d\cdot b
  +\frac1q(\Pi b)\cdot g+g\cdot Ae\\
 &+q(e\cdot\nabla)E^2
  +2\sum_kG_k\cdot\partial_kg
  -\frac2q\sum_k(\partial_kq)\,G_k\cdot g .
 \end{aligned}}
\tag{AE.16}
\]
AE.13--AE.14 保留了全部 \(\nabla A\) 项，AE.15--AE.16 则由
幅值梯度重新推导；两者互为符号与系数检查。利用 AE.5，
\[
 g\cdot Ae=F^2+q\,g\cdot d.
\tag{AE.17}
\]
因此 \(e^TA^2e\) 不能只保留为 \(F^2\)：同阶的方向弯曲项
\(q\,\nabla q\cdot(e\cdot\nabla)e\) 也必须保留。

## 6. 能量与符号审计

基本能量直接给出的零集安全信息仍是
\(|F|\le|\nabla q|\le|\nabla u|\)、\(F\in L^2_{t,x}\)，
零集上沿用 AC 的 F=0 代表。这不提升为临界 \(L_t^2L_x^3\) 控制。

首先，AE.6 中的负项没有产生超出标准 \(L^3\) 恒等式的免费预算。
在 \(q>0\) 的全环面情形，把 AE.6 乘以 \(q^2\) 并积分，有
\[
 \frac{d}{dt}\frac13\int q^3
 +2\int q|\nabla q|^2+\int q^3E^2
 =\int p\,u\cdot\nabla q.
\tag{AE.18}
\]
这里
\[
 2q|\nabla q|^2+q^3E^2
 =q|\nabla u|^2+q|\nabla q|^2
\tag{AE.19}
\]
正是标准 \(L^3\) 黏性耗散。因而 \(-qE^2\) 是有利符号，
但已经属于原有耗散，并未控制右侧无符号压力功。

其次，AE.14--AE.17 没有给出 \(F\) 的闭合耗散演化：

1. \(e^T{\mathcal H}e\) 没有符号。压力 Poisson 方程只固定
   \(\operatorname{tr}{\mathcal H}=\Delta p=-\operatorname{tr}(A^2)\)，
   不固定沿 \(e\) 的 Hessian 分量。基本能量也不免费控制
   \(\nabla^2p\) 的点态值。
2. \(e^TA^2e=F^2+q\,\nabla q\cdot d\)。即使暂时忽略第二项，
   \(+F^2\) 位于 \({\cal L}F\) 的右侧，是正 \(F\) 的反应源，
   不是负耗散；方向弯曲项本身又无符号。
3. AE.14 的两组 \(\partial_kA\) 项含二阶速度导数。
   基本 Leray 能量只给 \(u\in L_t^\infty L_x^2\) 和
   \(\nabla u\in L_{t,x}^2\)，不提供 \(\nabla A\) 的免费控制。
   分部积分会把导数移到 \(e\)、权重或 cutoff 上；目前尚未证明
   转移后的项可组合成由基本能量支付的非负平方或抵消。
   这不是对所有可能的弱形式、权重或组合恒等式的不可能性证明。
4. \(G_k^TAG_k\) 只看 \(A\) 的对称部分，而无散性只给
   \(\operatorname{tr}A=0\)；它仍可正可负。
   \(2FE^2\)、两个 \(c\)-耦合项以及 AE.16 的
   \(G_k\cdot\partial_kg\) 同样没有统一符号。
5. 因 \(qe=u\)，若所有方向变量在全环面光滑，
   \(\int q(e\cdot\nabla)E^2=\int u\cdot\nabla E^2=0\)。
   这只是一个无权全环面的中性输运抵消，不是强制项。
   在 \(\{q>0\}\) 的局部区域或加入 cutoff 后会产生边界通量。

最后，\(q^{-1}\) 在速度零集退化。不能仅凭形式上的
\(F^2\) 或方向方程使用全局最大值原理，也不能把
\(q\ge\kappa\) 当成首次奇点分析中已经证明的性质。
当前演化式说明：除标准幅值耗散外，压力 Hessian、方向弯曲和
\(\nabla A\) 全部留下真实的无符号成本。它没有产生新的成熟时间
持留估计、首次奇点闭合或原合同 G；本稿也不构成正则性结论。

## 7. 内部实际文件审查

r076l_proof_audit 起草并从矩阵与幅值梯度两条代数链核对。
父级完整读取 AE.1–AE.19，并收紧两处方法边界：
对 1/q 的正下界限制只用于本稿逐点一致界；当前分部积分不闭合
不等于所有权重/弱形式的不可能性。
r076l_heat_chebyshev 对修订后实际全文独立审查 PASS，
逐项复算两个 F 方程及其适用域，并确认前述边界。
父级按该审查意见补明能量直接控制的 F 范数。

本稿不属于此前 PressureGeometry 包；现并入 PressureQuotient 小节，
与 AF/AG 的积分抵消及 AH 的准确预算反例一同冻结。
直接方向演化仍未闭合，不再逐点重复同一高阶导数估计，
不把缺失临界条件加作既定事实。
