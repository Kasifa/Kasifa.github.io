# R0.73P 一手文献核查附录：二维/大解附近稳定性、临界小数据与 \(L^2\) 边界

> 状态：独立文献附录，不替代主研究笔记。
> 核查原则：只把论文原文、作者稿、期刊/学会官方页面列为定理证据；后续论文对旧文的回述只作为间接证据，并明确降级。
> 记号：\(W^{2,1}_p\) 为抛物型 Sobolev 空间；\(\dot H^{a,b}\) 表示水平/垂直各向异性 Sobolev 正则性；“允许 \(H^3\) 任意大”仅指满足该定理小范数条件的光滑序列中可令 \(H^3\) 无上界，不等于定理覆盖由 \(L^2\) 单独刻画的任意高频数据。

## 0. 结论边界

核查到的结果分为三类，不能混称为同一个“\(L^2\)-稳定定理”：

1. **弱解的 \(L^2\) 能量稳定或渐近稳定**：控制解差的能量，但不产生三维全局强解。
2. **强正则性的鲁棒性**：假定已有强参考解，并要求扰动在 \(\dot H^{1/2}\)、\(\dot H^\alpha\) 或各向异性临界拓扑中小。
3. **Mucha 型小能量—高正则耦合**：高阶迹范数没有预先上界，但允许的 \(L^2\) 小量随高阶范数和参考流大小而变化。

本轮没有核实到“存在只依赖黏性和区域、完全独立于所有高阶范数的统一 \(L^2\) 小球，并由此得到三维全局强解”的一手定理。

---

## 1. Mucha 2001：三维环面上非平凡参考解的稳定性

**文献**
Piotr B. Mucha, *Stability of Nontrivial Solutions of the Navier–Stokes System on the Three Dimensional Torus*, Journal of Differential Equations 172 (2001), 359–375.

- DOI：[10.1006/jdeq.2000.3863](https://doi.org/10.1006/jdeq.2000.3863)
- [期刊官方页面与摘要](https://www.sciencedirect.com/science/article/pii/S0022039600938634)
- [作者出版目录](https://www.mimuw.edu.pl/~pbmucha/index.php?s=p-pl)
- 间接拓扑核对：[W. M. Zajączkowski 的作者稿](https://arxiv.org/html/1606.04701v1)

### 已核实内容

- 区域是三维环面 \(\mathbb T^3\)。
- 参考对象是一个非平凡全局正则解；摘要明确提到势力情形。
- 官方摘要可确认的结论是：初始扰动在 \(L^2\) 中充分小时，扰动可在 \(W^{2,1}_r\) 正则层受控；无外力二维流是其特例。
- 后续一手论文对该结果的回述给出更具体的拓扑：\(r\ge 2\)，参考初值属于
  \[
  W_r^{2-2/r}(\mathbb T^3)\cap L^2(\mathbb T^3),
  \]
  势力局部属于 \(L_r\)；扰动初值具有相同迹正则性并在 \(L^2\) 中充分小，随后速度扰动和压力梯度分别在逐单位时间条带的 \(W_r^{2,1}\) 与 \(L_r\) 中受控。

### 精确量词边界

- “\(L^2\) 充分小”是**对给定参考解和给定正则数据类**而言。
- 本轮没有取得 Mucha 2001 的合法可访问全文，因此没有从原始定理核实小量 \(\varepsilon\) 对参考解范数、\(W_r^{2-2/r}\) 迹范数、黏性及时间条带常数的完整依赖。
- 作者页只列出论文；Elsevier 全文接口受限；arXiv、HAL、CORE、OpenAlex 未发现合法公开全文。本附录没有用 ResearchGate 或 Semantic Scholar 恢复定理文本。

### 禁止外推

- 不得把摘要外推成“\(\varepsilon=\varepsilon(\nu,\mathbb T^3)\) 与高阶范数和参考流无关”。
- 不得据此声称存在固定半径的 \(L^2\) 球，其中允许任意大的 \(H^3\) 数据并统一得到强解。
- 不得把后续论文的回述当作 Mucha 2001 阈值公式的原文证据。

**置信度**：书目信息、区域、势力、\(L^2\)-small 与 \(W_r^{2,1}\) 结论为高；由后续一手论文恢复的详细拓扑为中高；阈值的精确依赖为未核实。

---

## 2. Mucha 2008：\(\mathbb R^3\) 中二维流及一般大参考流的稳定性

**文献**
Piotr B. Mucha, *Stability of 2D incompressible flows in \(\mathbb R^3\)*, Journal of Differential Equations 245 (2008), 2355–2367.

- DOI：[10.1016/j.jde.2008.07.033](https://doi.org/10.1016/j.jde.2008.07.033)
- [arXiv 作者稿全文](https://arxiv.org/abs/math/0703844)
- [作者 PDF](https://www.mimuw.edu.pl/~pbmucha/publ/2008/stab-r.pdf)

### 已核实内容

- 区域为整个 \(\mathbb R^3\)，允许外力。写 \(v=w+u\)，其中已知光滑参考解 \(w\) 属于类 \(\Xi\)：
  \[
  \nabla w\in L^2\!\left((0,\infty)_t;L^2(\mathbb R^2_{xy});L^\infty(\mathbb R_z)\right).
  \]
- 二维参考流 \(w(t,x,y,z)=\widetilde w(t,x,y)\) 被包含；若二维外力
  \(\widetilde F\in L^2_t\dot H^{-1}(\mathbb R^2)\)，能量估计给出所需的梯度条件。
- Theorem 1 要求
  \[
  u_0\in H^1(\mathbb R^3)\cap W^{2-2/4}_4(\mathbb R^3)
  =H^1\cap W^{3/2}_4,
  \]
  并满足以下二者之一：
  1. \(\|u_0\|_{L^2}\) 充分小；或
  2. \(\|\partial_z u_0\|_{L^2}\) 充分小，且
     \(\|\partial_z w\|_{L^5_{t,x}}\)、
     \(\|\nabla\partial_z w\|_{L^{5/2}_{t,x}}\)
     相对于 \(\|u_0\|_{H^1\cap W^{3/2}_4}\) 充分小。
- 结论是存在唯一全局正则扰动
  \[
  u\in W^{2,1}_{4,\mathrm{loc}}(\mathbb R^3\times(0,\infty)),
  \qquad
  \|u_t\|_{L^4}+\|\nabla^2u\|_{L^4}\le \mathrm{DATA},
  \]
  其中 \(\mathrm{DATA}\) 依赖初值与参考流范数。
- 原文在 Theorem 1 后明确说明：对每一个给定的
  \(H^1\cap W^{3/2}_4\) 范数，论文描述相应所需的 \(L^2\) 小量；\(L^3\) 甚至任意 \(L^{2+\epsilon}\) 范数可以任意大。

### 精确量词边界

- 正确量词是
  \[
  \forall M<\infty\quad \exists\varepsilon(M,w,\nu)>0:
  \quad
  \|u_0\|_{H^1\cap W^{3/2}_4}\le M,
  \ \|u_0\|_2<\varepsilon
  \Longrightarrow \text{全局正则},
  \]
  而不是存在与 \(M\) 无关的统一 \(\varepsilon\)。论文没有把阈值写成上述符号形式，但正文明确陈述小量依赖整个扰动流范数。
- 对光滑数据而言，\(H^3\) 可以有限但无统一上界；当高阶范数增大时，允许的 \(L^2\) 小量必须相应缩小。

### 禁止外推

- 不得改写成“\(\|u_0\|_2<\varepsilon(\nu)\) 即可，不管 \(H^3\) 多大”。
- 二维参考流作为 \(\mathbb R^3\) 中的延拓通常具有无限三维总能量；该背景稳定定理不等于有限能量零解附近的统一 \(L^2\) 定理。
- “\(L^{2+\epsilon}\) 可任意大”不表示高阶迹范数已从阈值中消失。

**置信度**：高；定理、定义和量词说明均由作者稿全文核实。

---

## 3. Iftimie 1999：周期三维流作为二维流的各向异性扰动

**文献**
Dragoș Iftimie, *The 3D Navier–Stokes equations seen as a perturbation of the 2D Navier–Stokes equations*, Bulletin de la Société Mathématique de France 127 (1999), 473–517.

- DOI：[10.24033/bsmf.2358](https://doi.org/10.24033/bsmf.2358)
- [Numdam 官方全文](https://www.numdam.org/article/BSMF_1999__127_4_473_0.pdf)

### 已核实内容

- 无外力、周期区域 \(\mathbb T^3\)、零均值。初值分解为
  \[
  u_0=v_0+w_0,
  \qquad v_0\in L^2(\mathbb T^2),
  \qquad w_0\in H^{\delta,1/2-\delta},\quad0<\delta<1,
  \]
  其中 \(v_0\) 与第三坐标无关。
- Theorems 2.1–2.2 的核心小量条件是
  \[
  \|w_0\|_{H^{\delta,1/2-\delta}}
  \exp\!\left(\frac{\|v_0\|_{L^2(\mathbb T^2)}^2}{C\nu^2}\right)
  <C\nu.
  \]
- 在端点 \(\delta=0\) 时，垂直方向改用 \(B^{1/2}_{2,1}\)，水平方向为 \(L^2\)。
- 二维部分可任意大；三维余项的允许大小随二维能量呈指数收缩。结论为唯一全局解，余项保持在相应各向异性临界正则类中。

### 禁止外推

- 小量拓扑是各向异性临界空间，不是 \(L^2(\mathbb T^3)\)。
- 不得用 \(\|w_0\|_2\) 替代 \(H^{\delta,1/2-\delta}\) 或端点 Besov 条件。
- 可构造满足临界小量而 \(H^3\) 很大的光滑高频数据，但这不覆盖仅凭 \(L^2\) 小而临界范数大的数据。

**置信度**：高；定理页和阈值由官方全文核实。

---

## 4. Gallagher 1997：\(L^2\) 能量稳定与 \(H^{1/2}\) 强正则必须分开

**文献**
Isabelle Gallagher, *The tridimensional Navier–Stokes equations with almost bidimensional data: stability, uniqueness and life span*, International Mathematics Research Notices 1997(18), 919–935.

- DOI：[10.1155/S1073792897000597](https://doi.org/10.1155/S1073792897000597)
- [作者全文](https://webusers.imj-prg.fr/~isabelle.gallagher/NS3D2D.pdf)
- [期刊官方页面](https://academic.oup.com/imrn/article/1997/18/919/824539)

### 已核实内容

- 区域为 \(\mathbb T^3\)；论文也处理 \(\mathbb R^2\times S^1\)。允许外力以及水平、垂直不同的黏性系数。
- Theorem 2.1 给出三维有限能量解与二维解之差的
  \[
  L^\infty_tL^2_x\cap L^2_tH^1_x
  \]
  能量估计，常数含二维水平能量的指数因子。它是弱/有限能量层的稳定性，不产生真正三维扰动的全局强解。
- 等黏性强正则结论要求三维部分 \(w_0\in H^{1/2}(\mathbb T^3)\)，力差属于
  \(L^2_tH^{-1/2}\)，并满足形如
  \[
  \|w_0\|_{H^{1/2}}^2
  +\frac{C}{\nu}\|f-\bar f\|_{L^2_tH^{-1/2}}^2
  \le C\nu^2\exp\!\left(-\frac{CE_{2D}}{\nu^2}\right).
  \]
  结论位于 \(C_tH^{1/2}\cap L^2_tH^{3/2}\)。

### 禁止外推

- 不得把 Theorem 2.1 的 \(L^2\) 能量稳定与强正则定理合并成“\(L^2\)-small 三维扰动全局光滑”。
- 强正则半径位于 \(H^{1/2}\)，并随二维背景能量指数缩小。
- “在 \(L^2\) 和 \(H^{1/2}\) 中稳定”若不标注结论层级，会掩盖关键量词差异。

**置信度**：高；两类定理由作者全文分别核实。

---

## 5. Burczak–Zajączkowski 2016：\(\dot H^\alpha\) 正则性的定量鲁棒性

**文献**
Jan Burczak and Wojciech M. Zajączkowski, *Quantitative robustness of regularity for 3D Navier–Stokes system in \(\dot H^\alpha\)-spaces*, Nonlinear Analysis: Real World Applications 31 (2016), 513–532.

- DOI：[10.1016/j.nonrwa.2016.03.001](https://doi.org/10.1016/j.nonrwa.2016.03.001)
- [arXiv 作者稿](https://arxiv.org/abs/1409.3485)

### 已核实内容

- 周期立方体 \(Q_L=[0,L]^3\)，\(\alpha\in[1/2,1]\)。
- 初值 \(u_0,v_0\in\dot H^\alpha_{\rm div}(Q_L)\)，外力
  \(f,g\in L^2(0,T_*;\dot H^{\alpha-1}_{\rm div})\)。
- 假定参考解
  \[
  u\in L^\infty(0,T_*;\dot H^\alpha)
  \cap L^2(0,T_*;\dot H^{1+\alpha})
  \]
  已经是 \(\alpha\)-强解。Theorem 1 对任意 \(T<T_*\) 给出充分条件
  \[
  \left(
  \|u_0-v_0\|_{\dot H^\alpha}^2
  +K_4\int_0^T\|f-g\|_{\dot H^{\alpha-1}}^2dt
  \right)
  \exp\!\left(
  K_3\int_0^T
  \|\nabla u\|_{L^{3/(2-\alpha)}}^4dt
  \right)
  <\left(\frac{\bar\nu}{K_2}\right)^2,
  \]
  其中 \(\bar\nu+\varepsilon_1+\varepsilon_2<\nu\)。满足条件的任一 Leray–Hopf 解 \(v\) 继承同一 \(\alpha\)-强正则性，并有显式差值估计。

### 精确量词边界

- 定理是**给定有限时间 \(T<T_*\)** 和给定强参考解后的邻域定理。
- 邻域半径显式依赖参考解的时空积分、\(L\)、\(\nu\) 和 Sobolev 常数。
- 若要从同一初值邻域推出全局结论，还需参考解全局存在，并控制随 \(T\to\infty\) 出现的指数因子；Theorem 1 本身不自动提供一个与 \(T\) 无关的全局半径。

### 禁止外推

- 这不是 \(L^2\)-only 定理；最弱端点也是临界 \(\dot H^{1/2}\)。
- 光滑高频扰动可在 \(\dot H^\alpha\) 小的同时令 \(H^3\) 很大，但不得因此删除 \(\dot H^\alpha\) 小量条件。
- 正则性“鲁棒”不等于已证明所有参考数据都正则。

**置信度**：高；Theorem 1、常数及有限时间量词均由 arXiv 源稿核实。

---

## 6. Marín-Rubio–Robinson–Sadowski 2013：\(\dot H^{1/2}\) 鲁棒性与条件式数值验证

**文献**
Pedro Marín-Rubio, James C. Robinson and Witold Sadowski, *Solutions of the 3D Navier–Stokes equations for initial data in \(\dot H^{1/2}\): robustness of regularity and numerical verification of regularity for bounded sets of initial data in \(\dot H^1\)*, Journal of Mathematical Analysis and Applications 400 (2013), 76–85.

- DOI：[10.1016/j.jmaa.2012.10.064](https://doi.org/10.1016/j.jmaa.2012.10.064)
- [Universidad de Sevilla 仓储全文](https://idus.us.es/bitstreams/b0e9a174-2dd3-484d-9a9d-39ec5ee1323c/download)
- [官方仓储记录](https://idus.us.es/items/844adc51-3fb7-405f-8c36-e92c269d0edb)

### 已核实内容

- 周期立方体 \(Q=[0,2\pi]^3\)，散度为零且均值为零。
- Theorem 1：对任意 \(u_0\in\dot H^{1/2}\)，若其热流 \(v=e^{-tA}u_0\) 满足
  \[
  \int_0^{T_*}\|v(s)\|_{\dot H^1}^4ds<\varepsilon,
  \]
  则在 \([0,T_*]\) 上存在唯一
  \(L^\infty_t\dot H^{1/2}\cap L^2_t\dot H^{3/2}\) 解。
- Theorem 3：若给定参考解
  \[
  u\in L^\infty(0,T;\dot H^{1/2})
  \cap L^2(0,T;\dot H^{3/2}),
  \]
  则初值差在 \(\dot H^{1/2}\)、力差在 \(L^2_tH^{-1/2}\) 中满足论文式 (11) 的小量条件时，扰动解保持同样正则。邻域半径的关键依赖为
  \[
  c\exp\!\left(-c\int_0^T\|u(s)\|_{\dot H^1}^4ds\right).
  \]
- Theorem 12 证明了一个“可数值验证”命题，但论文 Definition 4 对此术语的定义是：**假定待验证命题为真**，存在一个会在有限时间终止并确认它的算法。它不是该 \(\dot H^1\) 球全局正则性的无条件证明。

### 禁止外推

- 不得把有限时间 \(\dot H^{1/2}\) 鲁棒半径改写成 \(L^2\) 半径。
- 不得把 Theorem 12 叙述为已经完成了整个有界 \(\dot H^1\) 集合的计算机辅助证明；论文没有提供实际闭合所有球的数值证书。
- “若命题为真则算法终止”不能用于证明命题本身为真。

**置信度**：高；大学仓储全文共 13 页，相关定理和 Definition 4 已逐条核实。

---

## 7. Hoang–Martinez 2017：任意 Leray–Hopf 解的最终 Gevrey 正则尾部

**文献**
Luan T. Hoang and Vincent R. Martinez, *Asymptotic expansion in Gevrey spaces for solutions of Navier–Stokes equations*, Asymptotic Analysis 104 (2017), 167–190.

- DOI：[10.3233/ASY-171429](https://doi.org/10.3233/ASY-171429)
- [arXiv 作者稿](https://arxiv.org/abs/1511.03523)

### 已核实内容

- 三维周期零均值情形。论文处理势体力 \(-\nabla\phi\)，经 Leray 投影后速度方程等价于无非势外力情形；作者归一化为 \(L=2\pi\)、\(\nu=1\)。
- Theorem 2.4：对任意 \(u^0\in L^2\) 和任意 Leray–Hopf 弱解、任意 \(\sigma>0\)，存在
  \[
  T=T(\sigma,\|u^0\|_2)>0
  \]
  使
  \[
  \|u(t)\|_{G_{1/2,\sigma+1}}\le D_\sigma e^{-t},
  \qquad t\ge T,
  \]
  且对每个 \(\alpha\ge0\)
  \[
  \|u(t)\|_{G_{\alpha+1/2,\sigma}}
  \le D_{\alpha,\sigma}e^{-t},
  \qquad t\ge T.
  \]
- 作者给出的一个显式选择是
  \[
  T=24\sigma+34+
  \bigl(\log(12C_1\|u^0\|_2)\bigr)^+.
  \]
- 主定理随后对每个固定 Leray–Hopf 解建立所有 Gevrey 类中的 Foias–Saut 渐近展开。

### 精确量词边界

- 定理允许任意有限能量初值，但结论只从某个依赖 \(\|u^0\|_2\) 和 Gevrey 半径的时间 \(T\) 之后开始。
- 对一般弱解，渐近展开的多项式系数可以依赖所选弱解；论文没有利用尾部展开证明此前弱解唯一。

### 禁止外推

- 不得把“最终解析”改写成“从 \(t=0\) 起光滑”。
- 不得把 \([T,\infty)\) 的强正则性经 weak–strong uniqueness 反向延拓到 \([0,T]\)。weak–strong uniqueness 是向前的条件唯一性工具。
- 该论文不排除早期奇异时刻，也不解决早期 Leray–Hopf 解的唯一性。

**置信度**：高；Theorem 2.4、显式 \(T\) 与主展开定理由 arXiv 源稿核实。

---

## 8. Kato 1984 与 Koch–Tataru 2001：临界小数据，而非 \(L^2\) 小数据

### 8.1 Kato 1984

**文献**
Tosio Kato, *Strong \(L^p\)-Solutions of the Navier–Stokes Equation in \(\mathbb R^m\), with Applications to Weak Solutions*, Mathematische Zeitschrift 187 (1984), 471–480.

- DOI：[10.1007/BF01174182](https://doi.org/10.1007/BF01174182)
- [EUDML 记录与合法全文入口](https://eudml.org/doc/173504)
- [GDZ 数字化全文](https://www.digizeitschriften.de/download/pdf/266833020_0187/log54.pdf)

### 已核实内容

- 在 \(\mathbb R^m\) 中，以 \(L^m\) 为缩放临界空间；三维时即 \(L^3(\mathbb R^3)\)。
- 任意 \(L^3\) 初值有局部强/mild 解；\(L^3\) 范数充分小时解全局存在。此处记录的是无外力主结论。

### 禁止外推

- \(L^3\)-small 不能由 \(L^2\)-small 推出；在 \(\mathbb R^3\) 上两者既无一般包含关系，也具有不同缩放。
- Kato 定理没有给出只依赖 \(\|u_0\|_2\) 的全局强解判据。

**置信度**：高。

### 8.2 Koch–Tataru 2001

**文献**
Herbert Koch and Daniel Tataru, *Well-posedness for the Navier–Stokes Equations*, Advances in Mathematics 157 (2001), 22–35.

- DOI：[10.1006/aima.2000.1937](https://doi.org/10.1006/aima.2000.1937)
- [Tataru 作者全文](https://math.berkeley.edu/~tataru/papers/nas.pdf)
- [作者出版页面](https://math.berkeley.edu/~tataru/research.html)

### 已核实内容

- 区域为 \(\mathbb R^n\)，主定理无外力。
- \(BMO^{-1}\) 由热延拓的 Carleson 型范数定义，是 Navier–Stokes 缩放临界空间。
- Theorem 2：散度为零且 \(BMO^{-1}\) 范数充分小的初值产生唯一全局小解，解属于作者定义的 \(X\) 空间；其中包含
  \(\sup_t\sqrt t\|u(t)\|_\infty\) 和局部抛物柱上的 Carleson 能量控制。
- Theorem 3：局部 \(BMO^{-1}_R\) 小量给出到 \(R^2\) 的局部唯一解；\(VMO^{-1}\) 数据因此局部适定。

### 禁止外推

- \(BMO^{-1}\)-small 不是 \(L^2\)-small。
- 该定理允许临界范数小而 \(H^3\) 任意大的光滑缩放族，但不能据此覆盖临界范数大的任意 \(L^2\)-小数据。

**置信度**：高；定义和 Theorems 2–3 由作者全文核实。

---

## 9. \(\mathbb R^3\) 的 \(L^2\) 超临界障碍与固定 \(\mathbb T^3\) 警告

### 9.1 \(\mathbb R^3\) 缩放

对无外力三维 Navier–Stokes，若
\[
u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t),
\]
则
\[
\|u_{\lambda,0}\|_{L^p(\mathbb R^3)}
=\lambda^{1-3/p}\|u_0\|_{L^p(\mathbb R^3)},
\]
以及
\[
\|u_{\lambda,0}\|_{L^2}=\lambda^{-1/2}\|u_0\|_{L^2},
\quad
\|u_{\lambda,0}\|_{\dot H^{1/2}}=\|u_0\|_{\dot H^{1/2}},
\quad
\|u_{\lambda,0}\|_{\dot H^3}
=\lambda^{5/2}\|u_0\|_{\dot H^3}.
\]

因此，若在 \(\mathbb R^3\) 上证明存在统一常数
\(\varepsilon=\varepsilon(\nu)>0\)，使**每个**光滑散度零初值只要
\(\|u_0\|_2<\varepsilon\) 就产生全局正则解，且阈值完全不依赖任何高阶范数或形状，那么对任意光滑有限能量初值选择足够大的 \(\lambda\) 即可进入该小球，再缩放回去。这将直接推出一般光滑有限能量数据的全局正则性。

这是一条数学推论，不是对某篇论文的转述。它解释了为什么“高范数无上界”与“统一的 \(L^2\) 半径”必须严格区分。

### 9.2 固定 \(\mathbb T^3\) 不能直接照搬上述论证

在固定周期 \(2\pi\) 的三维环面上，\(u(\lambda x)\) 若 \(\lambda\) 非整数会改变周期；若 \(\lambda\in\mathbb N\)，函数在固定环面内重复 \(\lambda^3\) 个周期单元，并且
\[
\|\lambda u(\lambda\cdot)\|_{L^2(\mathbb T^3)}
=\lambda\|u\|_{L^2(\mathbb T^3)},
\]
而不是 \(\lambda^{-1/2}\|u\|_2\)。若同时缩放环面尺寸，则研究的已不再是同一个固定区域。

所以：

- \(\mathbb R^3\) 上“统一 \(L^2\) 小球会解决一般问题”的缩放论证是有效的；
- 该论证**不能原样用于固定 \(\mathbb T^3\)**；
- 固定环面上的阈值障碍需要由周期内高频构造、临界范数或定理自身的常数依赖单独分析，不能伪装成 \(\mathbb R^3\) 的直接缩放结论。

---

## 10. 可用于后续研究的安全表述

1. Mucha 2008 证明了：高正则范数可无预设上界，但 \(L^2\) 阈值依赖该高正则范数和参考流；这不是统一 \(L^2\) 半径。
2. Iftimie、Gallagher、Marín-Rubio–Robinson–Sadowski、Burczak–Zajączkowski 给出的是临界或次临界拓扑中的强正则鲁棒性。
3. Gallagher 的 \(L^2\) 定理属于有限能量弱解稳定层；不能当作三维强解存在定理。
4. Hoang–Martinez 将任意周期 Leray–Hopf 解送入最终 Gevrey 正则尾部，但不消除初始至最终正则时刻之间的奇异性和非唯一性问题。
5. Kato 与 Koch–Tataru 说明临界小数据可以与任意大的 \(H^3\) 共存；它们同时说明“\(H^3\) 大”本身不是障碍，但所需小量必须位于正确的临界拓扑，而不能无证据地降为 \(L^2\)。
