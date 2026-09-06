# 正压力功的统一非线性短窗：扩张环面预检

2026-09-06。**PROVED LOCALLY / NOT CLAY。**
本稿由内部预检转入 PressureWorkWindow 合并研究包；
冻结提交与文件哈希以该包 manifest 为准。

本稿接续 AI，但不修改 AI。固定其中已经得到的
\(V\in C_c^\infty(\mathbb R^3;\mathbb R^3)\)，满足
\[
 \operatorname{div}V=0,\qquad \int_{\mathbb R^3}V=0,\qquad
 \|V\|_2^2=E_0,
\]
以及
\[
 w_0:=W_{\mathbb R^3}(V)
 =\int_{\mathbb R^3}P_V\,V\cdot\nabla|V|>0,\qquad
 P_V=\partial_i\partial_j(-\Delta)^{-1}(V_iV_j).
\tag{AJ.1}
\]
目标是把这个严格正的初始压力功保持在一个统一的重标时间窗内。
所得物理时间为 \(t\asymp\epsilon^{5/2}\)，不是
\(\epsilon^2\) 的成熟抛物时间。

## 1. 精确重标与扩张环面

令
\[
 {\mathbb T}_L^3=(\mathbb R/2\pi L\mathbb Z)^3,\qquad
 L=\epsilon^{-1}.
\tag{AJ.2}
\]
当 \(L\) 足够大时，把 \(V\) 作为单个紧支撑副本嵌入
\({\mathbb T}_L^3\)，记为 \(V_L\)。对原单位环面上的物理解，置
\[
 \begin{aligned}
 y&=\frac{x-x_0}{\epsilon},\qquad
 \tau=\epsilon^{-5/2}t,\\
 u_\epsilon(t,x)&=\epsilon^{-3/2}U_\epsilon(\tau,y),\qquad
 p_\epsilon(t,x)=\epsilon^{-3}P_\epsilon(\tau,y).
 \end{aligned}
\tag{AJ.3}
\]
原黏性为 1 的 NS 方程精确变为
\[
 \partial_\tau U_\epsilon
 +U_\epsilon\cdot\nabla U_\epsilon+\nabla P_\epsilon
 =\nu_\epsilon\Delta U_\epsilon,\qquad
 \operatorname{div}U_\epsilon=0,\qquad
 \nu_\epsilon=\sqrt\epsilon,
\tag{AJ.4}
\]
定义在 \({\mathbb T}_L^3\) 上，且
\(U_\epsilon(0)=V_L\)。

本稿所有扩张环面范数均为非归一化范数。若
\[
 \widehat f_L(k)=\frac1{(2\pi L)^3}
 \int_{{\mathbb T}_L^3}f(y)e^{-ik\cdot y/L}\,dy,
 \qquad k\in\mathbb Z^3,
\]
则取非齐次 Sobolev 范数
\[
 \|f\|_{H^m({\mathbb T}_L)}^2
 =(2\pi L)^3\sum_{k\in\mathbb Z^3}
  \left(1+\left|\frac{k}{L}\right|^2\right)^m
  |\widehat f_L(k)|^2.
\tag{AJ.5}
\]

对任意 \(\sigma>3/2\) 和 \(L\ge1\)，有
\[
 L^{-3}\sum_{k\in\mathbb Z^3}
 \left(1+\left|\frac{k}{L}\right|^2\right)^{-\sigma}
 \le C_\sigma.
\tag{AJ.6}
\]
证明可直接分壳：\(|k|\le2L\) 内有 \(O(L^3)\) 个格点；
第 \(j\) 个壳
\(2^jL<|k|\le2^{j+1}L\) 有 \(O(2^{3j}L^3)\) 个格点，而权重至多
\(C2^{-2\sigma j}\)。因 \(2\sigma>3\)，所得几何级数收敛。

Fourier 展开、Cauchy--Schwarz 与 AJ.6 因而给出
\[
 \begin{aligned}
 \|\partial^\alpha f\|_\infty
 &\le (2\pi)^{-3/2}
 \left[
 L^{-3}\sum_k
 \frac{|k/L|^{2|\alpha|}}
      {(1+|k/L|^2)^5}
 \right]^{1/2}
 \|f\|_{H^5}\\
 &\le C\|f\|_{H^5},
 \qquad |\alpha|\le3,
 \end{aligned}
\tag{AJ.7}
\]
且同理
\[
 \|f\|_\infty\le C\|f\|_{H^2}.
\tag{AJ.8}
\]
所有常数都与 \(L\) 无关。这里没有使用 Poincaré 不等式，
所以没有引入随环面边长增长的常数。

扩张环面上的 Leray 投影和二阶 Riesz 变换在频率
\(\xi=k/L\ne0\) 上的符号分别为
\[
 I-\frac{\xi\otimes\xi}{|\xi|^2},
 \qquad
 -\frac{\xi_i\xi_j}{|\xi|^2}.
\tag{AJ.9}
\]
它们在非归一化 \(L^2\) 及 \(H^m\) 中的算子范数一致有界；
压力变换的零频率按零均值规范取零；Leray 投影在零频率取恒等矩阵。
本稿速度始终零均值，后一约定不改变任何计算。这也可由
\({\mathbb T}_L\) 到单位环面的缩放直接看出。

## 2. 与 \(L,\nu_\epsilon\) 无关的 \(H^5\) 生命周期

对 AJ.4 施加周期 Leray 投影。把 AJ.5 的权重展开为
\((1+|\xi|^2)^5=\sum_{|\alpha|\le5}c_\alpha\xi^{2\alpha}\)，
其中 \(c_\alpha>0\)。于是该范数严格等于
\(\sum c_\alpha\|\partial^\alpha U_\epsilon\|_2^2\)，
不只是与另一微分范数等价。
对每个 \(|\alpha|\le5\) 微分、与
\(\partial^\alpha U_\epsilon\) 配对并按这些权重求和。
主输运项由无散性抵消，黏性项非负，剩余交换子满足
\[
 \sum_{|\alpha|\le5}c_\alpha
 \left|\left\langle
 [\partial^\alpha,U_\epsilon\cdot\nabla]U_\epsilon,
 \partial^\alpha U_\epsilon\right\rangle\right|
 \le C\|U_\epsilon\|_{H^5}^3.
\tag{AJ.10}
\]
这里只需要较弱的三次界，不借用更尖锐的 Moser 形式。
Leibniz 展开的每个剩余乘积均为
\((\partial^\beta U_\epsilon)\cdot
\nabla\partial^{\alpha-\beta}U_\epsilon\)，其中
\(1\le|\beta|\le|\alpha|\le5\)。两个导数阶数均不超过 5，
总和不超过 6，所以其中至少一个不超过 3。
将该因子用 AJ.7 放在 \(L^\infty\)，另一个放在 \(L^2\)，
再与 \(\partial^\alpha U_\epsilon\) 作 \(L^2\) 配对，即得 AJ.10。
所有权重和乘积项数固定，常数与 \(L\) 无关。
因此
\[
 \frac12\frac d{d\tau}\|U_\epsilon\|_{H^5}^2
 +\nu_\epsilon\|\nabla U_\epsilon\|_{H^5}^2
 \le C\|U_\epsilon\|_{H^5}^3.
\tag{AJ.11}
\]

当 \(L\) 足够大、紧支撑副本不重叠时，
\[
 \|V_L\|_{H^5({\mathbb T}_L)}
 =\|V\|_{H^5(\mathbb R^3)}
\tag{AJ.12}
\]
其中两边采用 AJ.5 展开所对应的同一非齐次微分范数。
由 AJ.11 的标量比较，存在只依赖 \(V\) 的
\(\tau_1>0\) 和 \(M<\infty\)，使
\[
 \sup_{0\le\tau\le\tau_1}
 \|U_\epsilon(\tau)\|_{H^5({\mathbb T}_L)}\le M
\tag{AJ.13}
\]
对所有充分小的 \(\epsilon\) 同时成立。

这一区间可直接由 Fourier--Galerkin 构造获得：对每个固定 \(L\)
截断 AJ.9 的 Fourier 模态，有限维 ODE 服从同一 AJ.11；
在 \([0,\tau_1]\) 上取极限；两解的 \(L^2\) 差能量估计以
\(\|\nabla U_\epsilon\|_\infty\) 为系数，给出唯一性。
因为 \(V\) 光滑，更高阶范数也保持有限。可直接在 Fourier 交换子中
使用下面的符号界（固定整数 \(m>5\)）：
\[
 |\langle\xi\rangle^m-\langle\eta\rangle^m|\,|\eta|
 \le C_m\bigl(
 |\xi-\eta|\langle\eta\rangle^m
 +\langle\xi-\eta\rangle^m|\eta|\bigr).
\]
由卷积的 \(\ell^1\)-\(\ell^2\) 界，高阶能量增长至多为
\[
 C_m\left(\sum_k |k/L|\,|\widehat U_\epsilon(k)|\right)
       \|U_\epsilon\|_{H^m}^2
 \le C_m\|U_\epsilon\|_{H^5}\|U_\epsilon\|_{H^m}^2.
\]
最后一步用 AJ.6，非归一化 Plancherel 的体积因子与格点和抵消。
AJ.13 因此在同一区间控制每个固定高阶范数的增长，
所以每个 \(\epsilon\) 的解在该区间光滑。
这里的共同寿命来自已展示的先验估计，而非一个可能依赖 \(L\) 的
未核对定理常数。

由投影后的方程、AJ.7--AJ.9 和 \(H^4\) 乘积估计，
\[
 \begin{aligned}
 \|\partial_\tau U_\epsilon\|_{H^3}
 &\le
 \|\mathbb P_L\operatorname{div}(U_\epsilon\otimes U_\epsilon)\|_{H^3}
 +\nu_\epsilon\|\Delta U_\epsilon\|_{H^3}\\
 &\le C\|U_\epsilon\|_{H^5}^2+\|U_\epsilon\|_{H^5}
 \le C_M.
 \end{aligned}
\tag{AJ.14}
\]
故
\[
 \|U_\epsilon(\tau)-V_L\|_{H^3}\le C_M\tau,
 \qquad 0\le\tau\le\tau_1.
\tag{AJ.15}
\]

## 3. 初始 Euclidean 压力功与正时间连续性

令 \({\cal G}_L\) 是 \({\mathbb T}_L^3\) 上的零均值 Green 函数。
若 \({\cal G}_1\) 对应边长 \(2\pi\)，则
\[
 {\cal G}_L(y)=L^{-1}{\cal G}_1(y/L).
\]
在原点的固定坐标邻域内写
\({\cal G}_1=\Gamma+S\)，其中
\(-\Delta\Gamma=\delta_0\)、\(S\) 光滑。利用
\(\Gamma\) 的 \(-1\) 次齐次性，分布意义下
\[
 \nabla^2{\cal G}_L(y)
 =\nabla^2\Gamma(y)+L^{-3}(\nabla^2S)(y/L).
\tag{AJ.16}
\]
Newtonian Hessian 的对角 delta 项包含在第一项中。

初值 \(V_L\) 的源和
\(h(V):=V\cdot\nabla|V|\) 都位于一个固定紧集内。
因此 AJ.16 给
\[
 {\cal W}_L(V_L)
 :=\int_{{\mathbb T}_L}P_{V_L}\,h(V_L)
 =W_{\mathbb R^3}(V)+O(L^{-3})
 =w_0+O(\epsilon^3).
\tag{AJ.17}
\]
压力若改变常数也不影响此式，因为
\(\int h(V)=\int\operatorname{div}(|V|V)=0\)。
故对充分小的 \(\epsilon\)，
\[
 {\cal W}_L(V_L)\ge\frac34w_0.
\tag{AJ.18}
\]

下面的正时间控制不再使用紧支撑或有限传播。对任意向量 \(z\)，定义
\[
 {\cal B}(z)=
 \begin{cases}
 z\otimes z/|z|,&z\ne0,\\
 0,&z=0.
 \end{cases}
\]
它满足
\[
 |{\cal B}(z)-{\cal B}(w)|\le3|z-w|,
\tag{AJ.19}
\]
而 \(h(Z)={\cal B}_{ij}(Z)\partial_iZ_j\) a.e.。
若 \(\|Z\|_{H^5},\|Y\|_{H^5}\le M\)，则由 AJ.8--AJ.9，
\[
 \begin{aligned}
 \|P_Z-P_Y\|_2
 &\le C_M\|Z-Y\|_2,\\
 \|h(Z)\|_2&\le C_M,\\
 \|h(Z)-h(Y)\|_2
 &\le3\|Z-Y\|_\infty\|\nabla Z\|_2
     +\|Y\|_\infty\|\nabla(Z-Y)\|_2\\
 &\le C_M\|Z-Y\|_{H^2}.
 \end{aligned}
\tag{AJ.20}
\]
同时 \(\|P_Y\|_2\le C_M\)。于是压力功泛函满足与 \(L\) 无关的
\[
 \begin{aligned}
 |{\cal W}_L(Z)-{\cal W}_L(Y)|
 &\le\|P_Z-P_Y\|_2\|h(Z)\|_2
     +\|P_Y\|_2\|h(Z)-h(Y)\|_2\\
 &\le C_M\|Z-Y\|_{H^2}.
 \end{aligned}
\tag{AJ.21}
\]
这一步只用全环面 Calderón--Zygmund 控制；黏性解在正时间立即产生
空间尾部并不造成遗漏，也没有假设 \(U_\epsilon(\tau)\) 继续紧支撑。

由 AJ.15、AJ.18 和 AJ.21，可选只依赖 \(V\) 的
\(0<\tau_0\le\tau_1\)，再取充分小的 \(\epsilon\)，使
\[
 \boxed{
 {\cal W}_L(U_\epsilon(\tau))\ge\frac12w_0,
 \qquad 0\le\tau\le\tau_0.}
\tag{AJ.22}
\]

## 4. 固定相对 \(H\) 增长与小物理耗散

定义重标后的
\[
 \begin{aligned}
 {\cal H}_L(U)&=\frac13\int_{{\mathbb T}_L}|U|^3,\\
 {\cal D}_L(U)&=\int_{{\mathbb T}_L}
 \left(|U||\nabla U|^2+|U||\nabla|U||^2\right).
 \end{aligned}
\tag{AJ.23}
\]
由 \(|\nabla|U||\le|\nabla U|\)、AJ.7 和 AJ.13，
\[
 {\cal D}_L(U_\epsilon(\tau))
 \le2\|U_\epsilon(\tau)\|_\infty
       \|\nabla U_\epsilon(\tau)\|_2^2
 \le C_D(V)
\tag{AJ.24}
\]
在统一时间窗内成立。AJ.4 的全环面 \(L^3\) 恒等式为
\[
 \frac d{d\tau}{\cal H}_L(U_\epsilon)
 +\sqrt\epsilon\,{\cal D}_L(U_\epsilon)
 ={\cal W}_L(U_\epsilon).
\tag{AJ.25}
\]
即使 \(U_\epsilon\) 有零集，也可用
\((|U_\epsilon|^2+\delta^2)^{1/2}\) 正则化后取极限。

进一步要求
\(\sqrt\epsilon\,C_D(V)\le w_0/4\)。由 AJ.22--AJ.25，
\[
 \frac d{d\tau}{\cal H}_L(U_\epsilon(\tau))
 \ge\frac14w_0,\qquad 0\le\tau\le\tau_0.
\]
由于 \({\cal H}_L(V_L)=H_V:=\frac13\int_{\mathbb R^3}|V|^3\)，
\[
 {\cal H}_L(U_\epsilon(\tau_0))
 \ge H_V+\frac14w_0\tau_0.
\tag{AJ.26}
\]

回到物理变量，令
\[
 t_\epsilon=\tau_0\epsilon^{5/2}.
\]
AJ.3 给出
\[
 H_\epsilon(t)=\epsilon^{-3/2}
 {\cal H}_L(U_\epsilon(\epsilon^{-5/2}t)),
\qquad
 \|\nabla_xu_\epsilon(t)\|_2^2
 =\epsilon^{-2}\|\nabla_yU_\epsilon(\tau)\|_2^2.
\]
因此在固定初始能量
\(\|u_\epsilon(0)\|_2^2=E_0\) 下，
\[
 \boxed{
 \frac{H_\epsilon(t_\epsilon)}{H_\epsilon(0)}
 \ge1+\delta_0,\qquad
 \delta_0:=\frac{w_0\tau_0}{4H_V}>0,}
\tag{AJ.27}
\]
其中 \(\delta_0\) 与 \(\epsilon\) 无关。同时
\[
 \boxed{
 \int_0^{t_\epsilon}\|\nabla_xu_\epsilon(t)\|_2^2\,dt
 =\sqrt\epsilon\int_0^{\tau_0}
   \|\nabla_yU_\epsilon(\tau)\|_2^2\,d\tau
 \le C(V)\sqrt\epsilon.}
\tag{AJ.28}
\]
在整个窗口中，物理压力功与净增长还分别满足
\[
 W_{\mathbb T}(u_\epsilon(t))
 \ge\frac12w_0\epsilon^{-4},\qquad
 H_\epsilon'(t)\ge\frac14w_0\epsilon^{-4}.
\tag{AJ.29}
\]

## 5. 被排除的准确估计与边界

AJ.27--AJ.28 排除的是下述无前置系数、无加性预算的精确统一估计：
存在只依赖固定 \(E_0\) 的有限常数 \(C(E_0)\)，使所有相应光滑周期解
从其初始时刻起满足
\[
 H(t)\le H(0)\exp\left[
 C(E_0)\int_0^t
 \left(1+\|\nabla u(s)\|_2^2\right)ds\right].
\tag{AJ.30}
\]
事实上在 \(t=t_\epsilon\)，AJ.28 给
\[
 \int_0^{t_\epsilon}
 \left(1+\|\nabla u_\epsilon\|_2^2\right)dt
 =O(\sqrt\epsilon)\longrightarrow0,
\]
所以 AJ.30 会推出
\[
 \frac{H_\epsilon(t_\epsilon)}{H_\epsilon(0)}
 \le\exp(o(1))\longrightarrow1,
\]
与 AJ.27 的固定增量矛盾。

必须保留以下边界：

1. \(t_\epsilon/\epsilon^2=\tau_0\sqrt\epsilon\to0\)。
   这是非线性短窗，绝不称为成熟的 \(\epsilon^2\) 时间窗。
2. \(H_\epsilon(0)=\epsilon^{-3/2}H_V\) 和
   \(\|\nabla u_\epsilon(0)\|_2^2=\epsilon^{-2}\|\nabla V\|_2^2\)
   都发散。AJ.30 的反例不能顺带排除允许常数依赖
   \(H(0)\) 的一般 \(C(E_0,H(0))\) 估计。
3. 若右侧另有任意前置因子 \(K>1\)，它可能吸收 AJ.27 的固定增量；
   加性预算也可能吸收该增量。本稿不声称排除这些形式。
4. 这是随 \(\epsilon\) 改变初值的光滑解族，不是一条固定解的成熟历史，
   也不是首次奇点、反向持留、压力几何闭合或原合同 G。
5. 有限原始文献碰撞记录见
   research/clay_b_pressure_work_literature-boundary_20260906.md。
   不作新颖性声明；没有仿真或科学图，也没有外部同行审稿结论。
