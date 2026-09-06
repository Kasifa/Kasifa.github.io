# 固定成熟时间后的局部 L³ 预算

2026-09-06。**PROVED LOCALLY / G OPEN / NOT CLAY。**
接续 ClayB-ConcentrationLimits，保留同一有限能量周期解，不增加 Type-I。

目标不是把早时变初值的 AA 反例搬到首次奇点，而是检查原方程中的
近源压力和黏性项。以下先对 \(0<s<t<T_*\) 的光滑区间推导。
固定小球半径 r；如研究成熟时间，要求 \(s\ge Cr^2>0\)。
不把这个要求当作附加正则性假设：在固定 \(r\) 足够小时，
首次奇点前的末端区间自然处于正成熟时间。

## 1. 完整带符号恒等式

取固定 \(0\le\chi\le1\)，\(\chi\in C_c^\infty(B_{2r})\)，
在 \(B_r\) 上等于 1。使用原速度，定义

\[
 H_\chi(t)=\frac13\int\chi |u|^3,\qquad
 {\cal D}_\chi(t)=\int\chi
   \bigl(|u||\nabla u|^2+|u||\nabla|u||^2\bigr).
\tag{AB.1}
\]

零速度处的第二个 integrand 取零。原方程给

\[
 \begin{aligned}
 H_\chi'(t)+{\cal D}_\chi(t)
 ={}&\frac13\int\Delta\chi\,|u|^3
 +\frac13\int |u|^3u\cdot\nabla\chi\\
 &+\int p\,|u|u\cdot\nabla\chi
 +\int\chi p\,u\cdot\nabla|u|.
 \end{aligned}
\tag{AB.2}
\]

证明：先令 \(q_\epsilon=(|u|^2+\epsilon^2)^{1/2}\)，
以 \(\chi q_\epsilon u\) 乘方程，对应能量
\(\frac13\int\chi(q_\epsilon^3-\epsilon^3)\)。
分部积分后，黏性耗散恰为
\(\int\chi(q_\epsilon|\nabla u|^2+
q_\epsilon^{-1}\sum_j(u\cdot\partial_j u)^2)\)。
其截止项是 \(\frac13\int\Delta\chi(q_\epsilon^3-\epsilon^3)\)。
无散性把输运转为
\(\frac13\int(q_\epsilon^3-\epsilon^3)u\cdot\nabla\chi\)；
压力转为
\(\int p(q_\epsilon u\cdot\nabla\chi+\chi u\cdot\nabla q_\epsilon)\)。
在紧的光滑时间区间内可支配收敛：
\(q_\epsilon^{-1}(u\cdot\partial_j u)^2
\le |u||\partial_j u|^2\)，
且 \(q_\epsilon\to|u|\)，故得到 AB.2。
压力内项也有 \(|\nabla q_\epsilon|\le|\nabla u|\)、
\(|u\cdot\nabla q_\epsilon|\le|u||\nabla u|\)，故其梯度极限同样可以
支配收敛。在零速度集，\(u\cdot\nabla|u|\) 和
\(|u||\nabla|u||^2\) 均取零；相应带 u 权重的乘积连续延为零。

令右侧为 \({\cal W}_\chi(t)\)，则

\[
 H_\chi(s)=H_\chi(t)+
 \int_s^t{\cal D}_\chi(\sigma)\,d\sigma
 -\int_s^t{\cal W}_\chi(\sigma)\,d\sigma .
\tag{AB.3}
\]

这是正确的反向符号：黏性耗散增加早时能量的下界，
可能造成快速正增长的是右侧带符号工作。
把它们全部绝对值化容易丢掉有利符号。

## 2. 远源冲量不能直接替代这里的压力功

采用 AA.16 的同一压力分解：
\(\theta=1\) 于 \(B_{3r}\)，支撑于 \(B_{4r}\)，
\(q_{\rm near}=\partial_i\partial_j{\cal G}*(\theta u_i u_j)\)。
固定周期零均值压力时，精确有 \(p=q_{\rm near}+q_{\rm far}\)。
其他 gauge 只多一个 \(c(t)\)，它乘
\(\operatorname{div}(\chi|u|u)\) 的全空间积分为零，不影响合并压力功。
AA.18 控制
\(\|\int_s^t\nabla q_{\rm far}\|_{L^3}/L_r(t)\)，
而 AB.2 的远源贡献等价于
\(-\int\chi |u|u\cdot\nabla q_{\rm far}\)。
速度权重随时间变化，不能从前一个裸冲量界直接推出后一个
时间积分的同阶小性。可以从 AA.17 的逐时梯度界重新支付，
但权重 \(\int\chi|u|^2\) 及窗口归一化需完整保留。

## 3. 加权远源压力功的单独估计

这一项可以用逐时界支付，而不误用裸冲量。令
\(L=L_r(t)>0\)，\(\delta=c_0r^2L^{-4}<t\)。
对任意 \(s\in[t-\delta,t]\)，由 AA.17 与全局能量界，

\[
 \begin{aligned}
 \left|\int_s^t\int \chi|u|u\cdot\nabla q_{\rm far}\,dx\,d\sigma\right|
 &\le \int_s^t
   \|\nabla q_{\rm far}(\sigma)\|_{L^\infty(B_{2r})}
   \left(\int\chi |u(\sigma)|^2\,dx\right)d\sigma\\
 &\le C M^4r^{-4}\delta .
 \end{aligned}
\tag{AB.4}
\]

所有能量范数仍属于同一个解。因 \(H_\chi(t)\ge L^3/3\)，

\[
 \sup_{s\in[t-\delta,t]}
 \frac{\left|\int_s^t\int\chi|u|u\cdot
                          \nabla q_{\rm far}\right|}{H_\chi(t)}
 \le Cc_0M^4r^{-2}L^{-7}.
\tag{AB.5}
\]

固定 \(M,r\) 且 \(L_r(t)\to\infty\) 时，该带权压力功确为相对小量。
这只付掉 AB.2 的远源部分，不包括近源、非线性输运或空间截止。
同一结论不自动适用于缩球，因 \(r^{-2}L^{-7}\) 需另控。
也没有给出所有原移动路径上的积分。
若称窗口为成熟窗口，还须 \(t-\delta\ge Cr^2\)；
先固定 \(Cr^2<T_*\)，再令 \(t\uparrow T_*\)、\(L_r(t)\to\infty\)，
该条件最终成立。AB.4 本身不依赖成熟条件。

## 4. 全环面原型：标准压力估计留下大范数系数

这里只做无空间 cutoff 的原型，不能当成第1节近源压力的局部估计。
记 \(L=\|u\|_{L^3(\mathbb T^3)}\)，\(D={\cal D}_1\)，
\(H=\frac13 L^3\)，\(W=\int p\,u\cdot\nabla|u|\)。
周期零均值压力满足双 Riesz 的 \(L^{9/4}\) 界。
先用加权 Cauchy--Schwarz，再用 Hölder、压力界和插值，有

\[
 \begin{aligned}
 |W|
 &\le D^{1/2}\left(\int p^2|u|\right)^{1/2}\\
 &\le D^{1/2}\|p\|_{9/4}\|u\|_9^{1/2}\\
 &\le C D^{1/2}\|u\|_{9/2}^{2}\|u\|_9^{1/2}\\
 &\le C L D^{1/2}\|u\|_9^{3/2}.
 \end{aligned}
\tag{AB.6}
\]

最后一步使用 \(2/9=(1/2)/3+(1/2)/9\)。
对 \(f=|u|^{3/2}\) 使用周期 Sobolev，必须保留非零均值的低阶项：

\[
 \|u\|_9^{3/2}=\|f\|_6
 \le C(\|\nabla f\|_2+\|f\|_2)
 \le C(D^{1/2}+L^{3/2}).
\tag{AB.7}
\]

于是对任意 \(\eta>0\)，

\[
 |W|\le CLD+CL^{5/2}D^{1/2}
       \le (CL+\eta)D+C_\eta L^5,\qquad
 H'\le (CL+\eta-1)D+C_\eta L^5.
\tag{AB.8}
\]

大 L 时，D 留在错误的一侧。这没有给出只依赖 L 的 H' 上界，
更未得到反向持留。不能把 Sobolev 的 D 下界反过来当成上界。
例如无散剪切 \(u_N=(0,\sin(Nx_1),0)\)，整数 N 下 L 恒定而 D
为正数乘 \(N^2\)，说明仅由 L 控制 D 的上界不存在。
这只是瞬时范数的检验，不是持留或奇点的动力学反例。

加入空间 cutoff 后，压力 Riesz 范数依赖扩大支撑中的速度，
Sobolev 还引入 cutoff 导数项；AB.2 的输运和压力壳项不能省略。
因此这里已经看见标准吸收的局限，但尚未付掉固定球近源与外壳预算。

## 5. 当前审查与未完成项

AB.1--AB.5 已经 r076l_figure_audit 对实际文件复核数学 PASS，
并按其建议补足压力梯度的支配收敛与 gauge 说明。
AB.4--AB.5 另经 r076l_heat_chebyshev 对实际文件独立复算 PASS。
AB.6--AB.8 已经 r076l_proof_audit 独立推导并对实际新增文字与公式
复核 PASS；H=L³/3 的记号与 H'+D=W 一致。
r076l_figure_audit 另对补充的极限/gauge 和 AB.6--AB.8 增量复核，
确认当前 AB.1--AB.8 的数学与源文本全部 PASS。
以上是内部解析复核，不是外部同行评审。
本稿作为 ClayB-PressureGeometry-20260906 的一部分冻结，
与 AC 的方向结构和 AD 的压力符号构造合并为同一小节。

1. 若继续局部化，精确估计近源压力项、黏性与空间截止项，记录大 L³ 系数，
   不使用未经支付的高阶导数上界。
2. 标准全环面压力链条已恢复临界大范数不可吸收；不继续优化这个常数。
   局部化只有在能获得真正额外的符号/几何信息时才值得继续，
   不能靠多写外壳项把未闭合估计说成首次奇点持留。

尚未得到由同一解能量独立推出的反向持留窗口或 G 的好尺度。
此包的单次移交以独立 dispatch receipt 为准；本稿不记发布执行状态。
本稿未生成仿真或科学图，不涉及独立论文专项。
