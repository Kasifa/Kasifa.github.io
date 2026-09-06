# 压力投影：抵消成立，一个特定瞬时残差预算失败

2026-09-06。ClayB-PressureQuotient-20260906。
接续 ClayB-PressureGeometry-20260906。这是一个研究小节，不是累计回顾。

## 从演化方程回到积分

上一节把 L³ 压力功写成 \(W=-\int pqF\)，其中
\(q=|u|\)、\(F=-e\cdot\nabla q\)，零速度处取 F=0。
我先检查了 F 的真实演化。AE 的两套推导相互核对后，压力 Hessian、
方向弯曲和二阶速度导数仍没有得到控制。已出现的有利项只是原有耗散。
这说明当前逐点估计没有闭合，不说明所有积分方法都不可能。

继续利用无散性，可以得到一个不需要正速率下界的恒等式：

\[
 \int q\Phi(q)F=0 .
\]

只依赖速率的压力部分，对全域压力功不可见。
这一思路已有直接文献前例：[Tran–Yu 的 pressure moderator 引理](https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/12230/Tran_2016_Regularity_AML_AAM.pdf?isAllowed=y&sequence=1)。
后续[压力—速度相关性研究](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/CE28509C5B6844BC5F27F3EF52075E47/S0022112020010332a.pdf/velocitypressure_correlation_in_navierstokes_flows_and_the_problem_of_global_regularity.pdf)
也给出相关的条件准则。因此我把这里的工作定位为严格核查与候选预算检验，
不是把压力重写当成新的正则性机制。

## 最佳速率投影给出了什么

在测度 \(q\,dx\) 下，把压力投影到所有只依赖 q 的函数上，记为
\(\mathsf P_qp\)。相应残差为

\[
 \mathcal R^2
 =\inf_\Phi\int q|p-\Phi(q)|^2,\qquad
 W=-\int q(p-\mathsf P_qp)F .
\]

AF 处理了零集、正体积常速平台、投影代表元和时间可测性。
它不依靠每个速度等值面都光滑，也不把不同同速区域擅自分开投影。

令 \(H=\frac13\int q^3\)，D 为原 L³ 耗散，Cauchy 与 Young 给出

\[
 H'+\frac12D\le\frac12\mathcal R^2.
\]

因此 \(\int \mathcal R^2/H\,dt<\infty\) 足以使光滑周期解延拓。
证明保留周期 Sobolev 的低模项，并通过 L³_tL⁹_x 和 H¹ 重启闭合。
这个条件尚未由一般解的能量预算得到；条件成立时可延拓，
不等于已经证明条件成立。

## 一个固定总能量的反检查

如果存在只依赖总能量的常数，使

\[
 \mathcal R^2
 \le C(E_0)H\bigl(1+\|\nabla u\|_2^2\bigr),
\]

那么它会提供一种直接使用总耗散的办法。AH 证明这条普适瞬时估计不成立。

构造先在欧氏空间取一只紧支撑无散场 V：它在一只球上为非零常向量，
远处分离的涡流却让球内压力不是常数。该球上 q 恒定，任何 \(\Phi(q)\)
都只能减掉一个常数，因此压力残差有严格正方差。
再将单个泡缩小后放入固定环面：

\[
 u_\epsilon(x)=\epsilon^{-3/2}
 V\!\left(\frac{x-x_0}{\epsilon}\right),
\]

并在环面上作相容周期延拓。可以让所有初值都有同一个指定的
\(\|u_\epsilon\|_2^2=E_0>0\)。精确尺度及压力核估计给

\[
 H(u_\epsilon)\asymp\epsilon^{-3/2},\quad
 \|\nabla u_\epsilon\|_2^2\asymp\epsilon^{-2},\quad
 \mathcal R^2(u_\epsilon)\gtrsim\epsilon^{-9/2}.
\]

所以候选估计两侧的比值至少按 \(\epsilon^{-1}\) 发散。
证明保留了周期 Green 函数 Hessian 的分布项和光滑余项，
没有用有限网格或数值拟合代替压力。

这一结果的边界同样重要：产生大残差的常速平台上 F=0，
压力功密度也为零。因此大残差不代表大压力功，反而说明这个范数
可能计入许多不做功的压力变化。
每个场都是合法的光滑 NS 初值，但该族没有证明固定解的时间积分失败，
也不否定成熟时间、首次奇点或带方向权重的更精确估计。

## 局部化不是免费的

取空间 cutoff \(\chi\)，合并压力功记为
\(K_\chi(p)=\int p\,\operatorname{div}(\chi q u)\)。
令 \(A(s)=\int_0^s\Phi(a)\,da\)，则

\[
 K_\chi(p)=K_\chi(p-\Phi(q))
 +\int[q\Phi(q)-A(q)]u\cdot\nabla\chi .
\]

外壳通量必须保留。取 \(\Phi(q)=-q^2/2\)，得到 Bernoulli 总压
\(Q=p+q^2/2\)；它恰把显式输运项吸收到总压功中，并没有让输运消失。
每个光滑时刻可以选有界投影代表元，但接近候选奇点的压力上界及外壳
仍未支付。仅有加权 L² 投影收敛，也不能推出外壳原函数收敛。

AG 还检查了一个拓扑边界：环面上单个速度等值面分量可能不分隔空间，
通量未必为零。无散性只保证整组等值面的总通量为零。

## 这一步之后

已经明确排除的是一条具体的瞬时残差预算，不是 NS 正则性。
压力投影恒等式成立，但它不能单独提供缺失的动力学控制。
我不再把这一类投影的形式改写作为新的推进点。

接下来回到真实压力功与耗散的配对，检查带符号驱动区域及其时空预算。
新的候选估计必须排除 F=0 平台的虚假成本，并说明如何控制近源和外壳；
不能只再添加一个临界相关性假设。

本节已完成内部实际文件独立复核，不等于外部同行评审。
没有仿真、科学图、发表等级或新颖性承诺。**G OPEN / NOT CLAY。**
