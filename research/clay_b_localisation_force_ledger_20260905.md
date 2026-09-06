# 局部化外力：完整乘积展开与调用门槛

2026-09-05。**解析恒等式 / 独立复算 / 非正则性定理 / NOT CLAY**。
用途：检查指定中心合同 G-C 的局部化误差，避免把一个标量领圈通量
直接当作满足强范数要求的外力。没有提出新颖性或优先权主张。

## 1. 不省略的外力公式

设 (v,p) 是一个光滑的无外力黏性 1 NS 解，Phi(t,x) 是光滑
标量截断，w 是光滑修正且 div w=-grad Phi·v。令
V=Phi v+w、Pi=Phi p。则 div V=0，并有

\[
 \partial_tV-\Delta V+(V\cdot\nabla)V+\nabla\Pi=F,
\tag{F.1}
\]

\[
\begin{aligned}
 F={}&(\partial_t\Phi-\Delta\Phi)v
 -2\nabla\Phi\cdot\nabla v
 +(\Phi^2-\Phi)(v\cdot\nabla)v\\
 &+\Phi(v\cdot\nabla\Phi)v
 +\partial_tw-\Delta w
 +\Phi(v\cdot\nabla)w\\
 &+(w\cdot\nabla)(\Phi v)+(w\cdot\nabla)w+p\nabla\Phi.
\end{aligned}
\tag{F.2}
\]

证明只用乘积法则。线性部分为
Phi(partial_t v-Delta v+grad p)
+(partial_t Phi-Delta Phi)v-2 grad Phi·grad v
+partial_t w-Delta w+p grad Phi。
第一括号用原方程替换为 -Phi(v·grad)v。
非线性展开中

\[
 ((\Phi v)\cdot\nabla)(\Phi v)
 =\Phi^2(v\cdot\nabla)v+\Phi(v\cdot\nabla\Phi)v.
\tag{F.3}
\]

另三项为 Phi(v·grad)w、(w·grad)(Phi v)、(w·grad)w。
相加即得 (F.2)。div w 的约束用于保证 div V=0，并不会删除
(F.3) 的第二项。Pi 已固定，也不能未经证明把它当作压力梯度。

若 Phi(t,x)=chi((x-X(t))/r)，还必须保留
partial_t Phi=-dot X·grad Phi。若 w 用移动环带的 Bogovskii 算子
定义，其时间导数也必须核对，不能套用固定空间算子的时间估计。
本节在光滑时段推导，不默认在 suitable 弱终点已有这些导数。

## 2. 与已核验原文的一个具体差异

Barker--Popkin 的 arXiv:2602.09951v1，Lemma 4.2.1，式 (296)
在本轮可读取的 PDF 和 HTML 都未列出 Phi(v·grad Phi)v。
父级按 (F.3) 重算，独立文献审查员也按乘积法则复算并比对两种
原文。不是把网页转码缺失直接当作原作者的错误。
[PDF，式 (296)](https://arxiv.org/pdf/2602.09951v1)；
[HTML，Lemma 4.2.1](https://arxiv.org/html/2602.09951v1#S4.SS2)。

这里只记录局部公式的遗漏，**不据此声称其正则性结论不成立**。
补入项支撑于 supp grad Phi。在该引理已经选定的固定光滑环带上，
v 属于 L_t^infty W_x^{k,infty}，Phi 固定光滑。因此用有限次
Leibniz 法则，Phi(v·grad Phi)v 也属于同类；在有限时间、紧支撑
空间上，它属于所需的 L_t^2 H_x^1 intersect L_{t,x}^6。
修正不增加该局部化引理的定性光滑性假设。
我没有联系作者，也没有据此作论文整体审查结论。

## 3. 当前实际调用门槛

该预印本 Proposition 3.0.5 在全空间、长度小于 1 的时间区间，
对光滑 suitable Leray--Hopf 解要求

\[
 \|V\|_{L_t^\infty L_x^3}
 +\|F\|_{L_t^2H_x^1\cap L_{t,x}^6}\le M.
\tag{F.4}
\]

它在此假设下给三重指数的速度有界估计。
本项目的 p in L^{3/2}、标量压力尾支付、标量累计领圈通量，
尚没有被证明足以推出 (F.4)。

下一次若借用该模板，必须同时解决：
指定中心及变化尺度下的环带选择和统一常数；移动截断与修正的
时间导数；包括 (F.2) 每一项的外力范数；以及生成而不是先假设
临界速度控制。单独补正一个乘积项并不解决这些 OPEN 输入。

这是对具体调用步骤的修正和边界核验，不是 NS 奇点排除结果。
