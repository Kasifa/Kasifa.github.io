# R0.72Q 一手文献审计：任意相位的定量 Morse 合同

**日期：** 2026-08-28

**审计结论：** 现有一手文献可以分成两层。Pignoni 给出 Morse
函数在 \(C^2\) 扰动下稳定的定性结论；Coble--He 给出满足完整形状条件、
且临界点缓慢移动的时变剪切流增强耗散定理。我在本次一手检索中没有找到
一条可直接引用的
定理，把“固定有限 Fourier 支撑的紧参数族”自动转换成参数族上一致的
增强耗散常数。

R0.72Q 使用的结论因而不是文献中的黑箱定理。本站先对固定
\(M\) 的任意相位多项式证明一个定量 Morse 合同，再从 Coble--He
Theorem 1.2 的证明中抽取参数族上一致的常数。我在这一审计中只检查该
推理链是否与现有定理相容，不作优先权判断。

---

## 1. 本站需要证明的有限模式合同

考虑已把第一谐波振幅和相位归一化后的剖面

\[
 F_y(\phi)
 =\cos\phi+
 \sum_{m=2}^{M}\operatorname{Re}
 \bigl(\beta_m(y)e^{im\phi}\bigr),
 \tag{1.1}
\]

其中 \(M<\infty\) 固定，\(\beta_m(y)\in\mathbb C\) 可以有任意相位。定义

\[
 Q_j(y):=\sum_{m=2}^{M}m^j|\beta_m(y)|,
 \qquad
 Q_j:=\sup_{0\le y\le1}Q_j(y).
 \tag{1.2}
\]

空间 Morse 论证只使用 (1.2)。在 R0.72Q 的热权重路径上，进一步有

\[
 \beta_m(y)=\beta_m(0)e^{-(m^2-1)y},
 \qquad
 W(y,\phi)=e^{-y}F_y(\phi).
 \tag{1.2a}
\]

正因子 \(e^{-y}\in[e^{-1},1]\) 只改变形状常数，不改变临界点位置或
非退化性。相位在这里可以任意选择，但不随快时间任意调制。

R0.72Q 的系数合同是

\[
 \boxed{M\ \text{固定},\qquad Q_2\le\frac12.}
 \tag{1.3}
\]

这是本站的显式假设，不是下面任何一篇论文的假设。它保留所有相对相位，
但要求高次谐波在加权 \(\ell^1\) 意义下由第一谐波控制。由于 \(m\ge2\)，

\[
 Q_1\le\frac{Q_2}{2}\le\frac14.
 \tag{1.4}
\]

若 \(F_y'(\phi)=0\)，则

\[
 |\sin\phi|\le Q_1\le\frac14,
 \qquad
 |\cos\phi|\ge\frac{\sqrt{15}}4.
 \tag{1.5}
\]

同时尾项的二阶导数不超过 \(Q_2\)。在靠近 \(0\) 的临界弧上，
\(F_y''<0\)；在靠近 \(\pi\) 的临界弧上，\(F_y''>0\)，并有统一下界

\[
 |F_y''(\phi)|
 \ge \frac{\sqrt{15}}4-\frac12
 =\frac{\sqrt{15}-2}{4}>0.
 \tag{1.6}
\]

每条弧至多有一个临界点，而周期光滑非恒定函数至少有一个极大点和一个
极小点。因此每个 \(F_y\) 恰有两个临界点。它们的分离、局部线性斜率
以及离临界区的梯度下界都可以统一选取。固定 \(M\) 还给出

\[
 Q_3\le M Q_2\le\frac M2,
 \tag{1.7}
\]

所以三阶空间导数和热权重产生的时间导数也有只依赖 \(M\) 的上界。
式 (1.4)--(1.7) 是本站推导。Pignoni 的定理只解释为什么这种稳定性在
定性上符合一般 Morse 理论；它不提供这些常数。

---

## 2. Coble--He：允许移动临界点的时变剪切定理

**一手来源：** Daniel Coble and Siming He,
[*A Note on Enhanced Dissipation and Taylor Dispersion of Time-dependent
Shear Flows*](https://arxiv.org/html/2309.15738), arXiv:2309.15738v2
(2023), Theorem 1.2；发表于 *Communications in Mathematical Sciences*
**22** (2024), 1685--1700，
[DOI 10.4310/CMS.2024.v22.n6.a10](https://doi.org/10.4310/CMS.2024.v22.n6.a10)。

### 2.1 原文定理

Theorem 1.2 允许临界点 \(y_i(t)\) 随时间移动。其主要假设是：

1. 实际剪切 \(V(t,y)\in C^2_{t,y}\)，并存在参考剪切
   \(U\in C^1_tC^2_y\)；
2. \(U,V\) 共享同一组固定数目 \(N\) 的非退化临界点
   \(\{y_i(t)\}_{i=1}^N\)，且 \(V_yU_y\ge0\)；
3. \(\|U_{ty}\|_\infty\le\nu^{3/4}\)；
4. 在固定半径、两两不交的临界邻域内，\(|Z_y|^2\) 与
   \(|y-y_i(t)|^2\) 以固定常数比较；在邻域外，\(|Z_y|\) 有固定的
   正下界和上界，其中 \(Z\in\{U,V\}\)；
5. \(U,V\) 具有定理声明中的统一 Sobolev 上界。论文的全局记号约定还
   允许常数依赖相应的 \(W^{3,\infty}\) 范数。

在 \(\nu\le\nu_0(U,V)\) 时，原文结论为

\[
 \|f_k(t)\|_2
 \le e\,e^{-\delta\nu^{1/2}|k|^{1/2}t}\|f_k(0)\|_2.
 \tag{2.1}
\]

所以“临界点必须固定不动”不是该定理的限制。真正的限制是临界点必须
共享、保持统一非退化形状，并通过参考剪切满足慢变条件。

### 2.2 原文没有直接声明的参数族一致性

Theorem 1.2 把小粘性阈值写成 \(\nu_0(U,V)\)，并未逐字声明一个紧
参数族上的统一阈值。参数族一致性需要检查证明：

- Lemma 3.1 的导数比较常数为
  \(C_*=C_*(\mathfrak C_0,\mathfrak C_1)\)；
- (3.21)--(3.24) 中的 hypocoercive 参数和衰减率只经过
  \(C_*\)、谱常数 \(\mathfrak C_{\rm spec}\) 与
  \(\|U_{yy}\|_\infty\)；
- Appendix A, Lemma A.1 用临界点附近的 partition of unity；
  (A.8) 的小粘性吸收还依赖 cutoff 导数的统一上界。

因此，下列数据统一时，证明允许选取同一个 \(c_{\rm ED}\) 和同一个
小粘性阈值：固定临界点数、固定分离和邻域半径、局部 Morse 斜率上下界、
离临界区梯度间隙、二阶和三阶导数上界、慢时间导数上界，以及一组导数
统一有界的 cutoffs。

R0.72Q 令 \(U=V\)。这样共享临界点和导数符号条件自动成立。式
(1.3) 提供空间形状数据；热权重和慢时间缩放提供
\(\|U_{t\phi}\|_\infty\le C(M)\nu\)。对充分小的 \(\nu\)，它满足
\(C(M)\nu\le\nu^{3/4}\)。这一步是从原文证明抽取的本站参数族推论，
不应写成 Coble--He 已直接证明了任意相位有限 Fourier 族。

**适用边界：** 固定 \(M\) 且满足完整定量合同的任意相位族可以使用这条
证明链。仅知道 Fourier 支撑有限、参数集紧或每个时刻剖面非退化，并不足以
调用原文定理。

---

## 3. Pignoni：Morse 稳定性的定性来源

**一手来源：** Roberto Pignoni,
[*Density and Stability of Morse Functions on a Stratified Space*](https://numdam.org/item/ASNSP_1979_4_6_4_593_0/),
*Annali della Scuola Normale Superiore di Pisa*, Serie IV, **6** (1979),
593--608。Numdam 的一手记录未列 DOI。

该文 §4 说明 Morse 函数在 \(C^k(X,\mathbb R)\)、\(2\le k\le\infty\)
中构成开集。更强的局部陈述是：给定 Morse 函数及其各临界点的两两不交
邻域，可以取函数空间中的一个凸邻域，使每个扰动函数在每个指定邻域中恰有
一个非退化临界点，并且没有其他临界点。

对单层紧流形 \(X=S^1\)，该结论直接说明小 \(C^2\) 扰动不会立刻改变
临界点数。对一个已经远离非 Morse 集的紧系数族，有限覆盖还给出某个统一
扰动邻域。

**明确局限：** §4 不给出相位半径、Hessian 下界、临界点分离、离临界区
梯度下界或 Coble--He 常数。式 (1.3) 到式 (1.7) 的显式合同仍需本站证明。
Pignoni 后面的拓扑稳定定理还要求不同临界值；增强耗散并不需要排除两个
不同临界点具有相同临界值，因此该附加条件不应移入 R0.72Q。

---

## 4. Voorhaar 与 1:2 caustic

**一手来源：** Arina Voorhaar,
[*The Newton Polytope of the Morse Discriminant of a Univariate
Polynomial*](https://arxiv.org/html/2104.05123), arXiv:2104.05123v2
(2021), *Advances in Mathematics* **432** (2023), 109275，
[DOI 10.1016/j.aim.2023.109275](https://doi.org/10.1016/j.aim.2023.109275)。

Voorhaar Definition 1.1 把 caustic 定义为具有退化临界点的 Laurent
多项式集合。Definition 1.2--1.4 还加入不同临界点具有相同临界值的
Maxwell stratum，并由此定义完整 Morse discriminant。有限三角多项式在
\(z=e^{i\phi}\) 下成为 Laurent 多项式，所以 caustic 提供了描述系数空间
退化墙的自然语言。

该文没有计算 R0.72Q 的实单位圆相位锥。下面的 1:2 公式是本站的直接
消元，而不是 Voorhaar 的定理。令

\[
 F(\phi)=\cos\phi+\operatorname{Re}(z e^{2i\phi}),
 \qquad z\in\mathbb C.
 \tag{4.1}
\]

联立 \(F'(\phi)=F''(\phi)=0\) 得到参数式

\[
 \boxed{
 z(\phi)=\frac18e^{-3i\phi}-\frac38e^{-i\phi}.}
 \tag{4.2}
\]

消去 \(\phi\) 后，曲线满足

\[
 \boxed{
 \left(|z|^2-\frac1{16}\right)^3
 =\frac{27}{1024}(\operatorname{Im}z)^2,
 \qquad \frac14\le|z|\le\frac12.}
 \tag{4.3}
\]

因此 \(|z|<1/4\) 的整张任意相位圆盘不含退化临界点。若第二谐波按热权重
演化，则 \(z(y)=z_0e^{-3y}\)，退化条件等价于

\[
 z_0=\frac{e^{3y}}8
 \left(e^{-3i\phi}-3e^{-i\phi}\right).
 \tag{4.4}
\]

一般 caustic 点满足三阶 jet 非零，对应 \(A_2\) 型退化；实轴端点
\(z=\pm1/4\) 还满足三阶导数为零、四阶导数非零，对应两个 \(A_3\)
cusp。R0.72P 的实系数墙 \(\lambda=\pm1/4\) 正是这两个端点。

在 R0.72Q 的记号中，1:2 情形有 \(Q_2=4|z|\)。所以
\(Q_2\le1/2\) 给出 \(|z|\le1/8\)，位于精确 caustic-free 圆盘内部，
并保留一个定量余量。

**明确局限：** Voorhaar 研究复系数空间中的判别簇及其 Newton polytope，
不提供实单位圆上的显式安全半径、增强耗散常数或时变临界点控制。完整
Morse discriminant 中的 Maxwell 条件对本问题也过强；增强耗散需要避开
caustic，而不需要临界值彼此不同。

---

## 5. 静态增强耗散结果的边界

### 5.1 Bedrossian--Coti Zelati

**一手来源：** Jacob Bedrossian and Michele Coti Zelati,
[*Enhanced Dissipation, Hypoellipticity, and Anomalous Small Noise
Inviscid Limits in Shear Flows*](https://arxiv.org/html/1510.08098),
arXiv:1510.08098, *Archive for Rational Mechanics and Analysis* **224**
(2017), 1161--1204，
[DOI 10.1007/s00205-017-1099-y](https://doi.org/10.1007/s00205-017-1099-y)。

Theorem 1.1 假设固定静态剪切 \(u\in C^{n_0+2}\) 只有有限个临界点，
并且 \(u'\) 在这些点只以有限阶消失。定理中的常数明确写成只依赖
\(u\)。当临界点非退化时 \(n_0=1\)，其幂次是
\(\nu^{1/2}|k|^{1/2}\)，原文估计带有对数修正。

该文提供 Coble--He 所沿用的局部谱隙与 hypocoercive 结构，但没有时变
参数族定理，也没有把常数写成 R0.72Q 的 \(M,Q_2\) 函数。

### 5.2 Coti Zelati--Gallay

**一手来源：** Michele Coti Zelati and Thierry Gallay,
[*Enhanced Dissipation and Taylor Dispersion in Higher-dimensional
Parallel Shear Flows*](https://arxiv.org/html/2108.11192),
arXiv:2108.11192, *Journal of the London Mathematical Society* **108**
(2023), 1358--1392，
[DOI 10.1112/jlms.12782](https://doi.org/10.1112/jlms.12782)。

Theorem 1.1 的一维静态条件是
\(|v'|+\cdots+|v^{(m)}|>0\)；Theorem 1.2 处理光滑 Morse 剪切，且
边界上没有临界点。非退化临界点对应 \(m=2\) 和
\(\nu^{1/2}|k|^{1/2}\) 的增强耗散尺度。

这些定理说明退化阶数确实改变耗散尺度，但常数按单个静态剖面给出。它们
不覆盖任意相位、随慢时间改变相对 Fourier 权重的完整叠加。

---

## 6. 瞬时 Morse 紧性不能代替速度控制

**一手预印本：** Johannes Benthaus, Giuseppe Maria Coclite and
Camilla Nobili,
[*Mixing and Enhanced Dissipation in a Time-translating Shear
Flow*](https://arxiv.org/html/2603.14624), arXiv:2603.14624v1 (2026)。

该文研究 \(v(y,t)=\alpha\sin(y-ct)\)。所有瞬时空间剖面都属于同一个
紧的平移轨道，而且临界点的 Morse margin 完全一致。可是时间行为仍取决于
速度 \(c\)：Theorem 2 在 \(c=c_0\nu^\ell\)、
\(1/3<\ell<3/4\) 时得到随 \(\ell\) 改变的耗散率；Theorem 3 在快速
平移区间证明解在固定时间窗内接近热方程，误差为
\(O((1+\nu)/c)\)。

这不是对 Coble--He 的反例，因为快速平移不满足其慢参考剪切假设。它给出
一个清楚的边界：瞬时剖面集合在 \(C^\infty\) 中紧、临界点统一非退化，
仍不能替代 \(\partial_tU\) 或临界点速度的控制。R0.72Q 的结论因此只用于
热权重产生的慢时间路径，不覆盖任意快的相位调制。

---

## 7. Claim--source ledger

| 主张 | 一手来源 | 原文直接支持 | 本站增加的步骤 | 不能推出的结论 |
|---|---|---|---|---|
| 时变非退化剪切具有 \(\nu^{1/2}|k|^{1/2}\) 衰减 | Coble--He, Theorem 1.2 | 允许共享临界点缓慢移动；给出逐剖面定理 | 用 (1.3) 验证统一形状数据，并从证明统一化 \(\nu_0,\delta\) | 任意紧 Fourier 族自动有统一常数 |
| 小 \(C^2\) 扰动保留 Morse 临界点 | Pignoni, §4 | 定性开性及指定邻域内临界点持续 | 给出 \(Q_2\le1/2\) 的显式 Hessian、分离和梯度常数 | 显式相位半径或 ED 常数 |
| 退化临界点形成系数空间 caustic | Voorhaar, Definition 1.1 | Laurent 多项式 caustic 的代数几何定义 | 推导 (4.2)--(4.4) 的实单位圆 1:2 曲线 | R0.72Q 的安全半径或时变定理 |
| 静态耗散尺度取决于临界点退化阶 | Bedrossian--Coti Zelati, Theorem 1.1 | 固定静态剖面的阶数依赖速率 | 仅作为 Coble--He 方法和尺度的背景 | 时变参数族统一性 |
| 静态 Morse 剪切给出 \(m=2\) 尺度 | Coti Zelati--Gallay, Theorems 1.1--1.2 | 静态一维/高维平行剪切估计 | 仅用于确认 Morse 数据不可省略 | 任意相位叠加的时变估计 |
| 临界点速度会改变甚至削弱混合 | Benthaus--Coclite--Nobili, Theorems 2--3 | 刚性平移正弦剖面的速度依赖结果 | 用作慢时间条件不能删除的边界案例 | 热权重有限多项式的一般定理 |

---

## 8. 停止条件与保留措辞

这些一手来源已经足以判定 R0.72Q 的文献接口，因此我把本次检索停在这里：

\[
 \text{固定 }M+\text{显式定量 Morse 合同}
 \Longrightarrow
 \text{可从 Coble--He 证明抽取一致 ED 常数};
 \tag{8.1}
\]

\[
 \text{有限 Fourier 支撑或瞬时 Morse 紧性本身}
 \not\Longrightarrow
 \text{一致 ED 常数}.
 \tag{8.2}
\]

“可抽取”指在本站给出统一 cutoffs、谱常数和小粘性阈值的证明，不表示
Coble--He 原文已经陈述 R0.72Q 的有限模式推论。“没有找到直接定理”只
是这次有界检索的结果。我不把它写成新颖性或优先权声明。
