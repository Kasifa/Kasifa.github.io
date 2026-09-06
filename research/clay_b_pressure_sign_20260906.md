# \(L^3\) 压力功没有普适耗散符号：一个显式周期构造

2026-09-06。**PROVED LOCALLY / NOT CLAY。**

本稿只检查全环面 \(L^3\) 恒等式中的压力功
\[
 {\cal W}(u)=\int_{\mathbb T^3}p\,u\cdot\nabla |u|\,dx,
 \qquad
 -\Delta p=\partial_i\partial_j(u_i u_j),\quad \int p=0.
\tag{AD.1}
\]
空间取 \(\mathbb T^3=(-\pi,\pi]^3\)，积分不作体积归一化。
下面给出零均值、光滑、有限 Fourier 模态的无散场，使
\({\cal W}>0\)；取相反初值则使 \({\cal W}<0\)。
这是一个局部解析观察，不宣称新颖性。

## 1. 二维三模态产生非零压力配对

令
\[
 \Psi(x,y)=\cos x+\cos y+\cos(x+y),\qquad
 v=(\partial_y\Psi,-\partial_x\Psi,0).
\tag{AD.2}
\]
于是 \(v\) 光滑、零均值、无散，并且与 \(z\) 无关。对二维流函数场，
\[
 \begin{aligned}
 -\Delta p_v
 &=\partial_i\partial_j(v_i v_j)
   =\partial_i v_j\,\partial_j v_i\\
 &=2\bigl(\Psi_{xy}^2-\Psi_{xx}\Psi_{yy}\bigr)\\
 &=-\cos(x+y)-\cos(x-y)-\cos(2x+y)-\cos y\\
 &\hspace{2.1cm}-\cos(x+2y)-\cos x .
 \end{aligned}
\tag{AD.3}
\]
这里第二个等号使用 \(\operatorname{div}v=0\)。
相应的二维零均值压力为
\[
 \begin{aligned}
 p_v={}&-\frac12\cos(x+y)-\frac12\cos(x-y)
        -\frac15\cos(2x+y)-\cos y\\
      &-\frac15\cos(x+2y)-\cos x .
 \end{aligned}
\tag{AD.4}
\]
另一方面
\(\partial_xv_1=\Psi_{xy}=-\cos(x+y)\)。不同 Fourier 模态正交，
而
\(\int_{\mathbb T^2}\cos^2(x+y)\,dx\,dy=2\pi^2\)，所以
\[
 I:=\int_{\mathbb T^2}p_v\,\partial_xv_1\,dx\,dy=\pi^2>0.
\tag{AD.5}
\]

## 2. 零均值且处处不消失的背景

固定 \(a>1\)，取
\[
 B_a(z)=(a\cos z,\sin z,0),\qquad
 q_a(z)=|B_a(z)|
       =\bigl(a^2\cos^2z+\sin^2z\bigr)^{1/2}.
\tag{AD.6}
\]
\(B_a\) 光滑、零均值、无散，而且 \(q_a\ge1\)，故它处处不消失。
令
\[
 V_\epsilon=B_a+\epsilon v .
\tag{AD.7}
\]
这仍是零均值、光滑、有限模态的无散场。

该背景不会改变压力。事实上 \(B_a\) 仅有前两个分量，却只依赖
\(z\)，而 \(v\) 仅有前两个分量且只依赖 \((x,y)\)。因此逐项有
\[
 \begin{aligned}
 \partial_i\partial_j(B_{a,i}B_{a,j})&=0,\\
 \partial_i\partial_j(B_{a,i}v_j)
 &=B_{a,i}\partial_i(\partial_jv_j)=0,\\
 \partial_i\partial_j(v_iB_{a,j})
 &=B_{a,j}\partial_j(\partial_i v_i)=0.
 \end{aligned}
\tag{AD.8}
\]
所有求和中的非零指标均属于 \(\{1,2\}\)，所以不会有遗漏的
\(z\) 导数。由压力的零均值规范，\(V_\epsilon\) 的压力精确为
\[
 p_\epsilon=\epsilon^2p_v .
\tag{AD.9}
\]

## 3. 压力功的严格正主项

取
\[
 0<|\epsilon|\le\epsilon_0
 :=\min\left(1,\frac1{2\|v\|_\infty}\right).
\]
则 \(|V_\epsilon|\ge1/2\)。利用
\[
 V_\epsilon\cdot\nabla|V_\epsilon|
 =\frac{V_{\epsilon,i}V_{\epsilon,j}}{|V_\epsilon|}
   \partial_iV_{\epsilon,j},
\]
以及 \(V_{\epsilon,3}=0\) 和
\(\partial_iB_{a,j}=0\) 对 \(i=1,2\)，可得
\[
 V_\epsilon\cdot\nabla|V_\epsilon|
 =\epsilon\frac{B_{a,i}B_{a,j}}{q_a}\partial_i v_j
   +\epsilon^2{\cal R}_\epsilon .
\tag{AD.10}
\]
这里 \(i,j\in\{1,2\}\)，且
\[
 \sup_{0<|\epsilon|\le\epsilon_0}
 \|{\cal R}_\epsilon\|_{L^\infty(\mathbb T^3)}
 \le C(a,v).
\tag{AD.11}
\]
这不是形式展开：映射
\(\xi\mapsto \xi_i\xi_j/|\xi|\) 在 \(|\xi|\ge1/2\) 上光滑，
对 \(B_a+\epsilon v\) 使用带一致一阶导数界的 Taylor 定理即可。

定义
\[
 K_{ij}(a)=\int_{-\pi}^{\pi}
             \frac{B_{a,i}(z)B_{a,j}(z)}{q_a(z)}\,dz .
\tag{AD.12}
\]
由奇偶性 \(K_{12}=K_{21}=0\)。又因
\(\partial_yv_2=-\partial_xv_1\)，其对角收缩为
\[
 K_{ij}\partial_i v_j
 =\kappa(a)\partial_xv_1,\qquad
 \kappa(a):=K_{11}-K_{22}=\mathcal J(a),
\tag{AD.13}
\]
其中
\[
 \mathcal J(r)=\int_{-\pi}^{\pi}
 \frac{r^2\cos^2z-\sin^2z}
      {(r^2\cos^2z+\sin^2z)^{1/2}}\,dz .
\tag{AD.14}
\]
有 \(\mathcal J(1)=0\)，并且对每个 \(r>0\)，
\[
 \mathcal J'(r)=\int_{-\pi}^{\pi}
 \frac{r\cos^2z\,
       (r^2\cos^2z+3\sin^2z)}
      {(r^2\cos^2z+\sin^2z)^{3/2}}\,dz>0.
\tag{AD.15}
\]
严格性来自 integrand 在正测度集合上严格为正。因此
\(\kappa(a)>0\) 对所有 \(a>1\) 成立。

把 AD.9--AD.13 代入 AD.1，并使用 AD.5，得到带定量一致余项的
\[
 {\cal W}(V_\epsilon)
 =\epsilon^3\kappa(a)\pi^2+O_{a,v}(\epsilon^4).
\tag{AD.16}
\]
确切地说，余项绝对值不超过
\(2\pi C(a,v)\|p_v\|_{L^1(\mathbb T^2)}|\epsilon|^4\)。
故固定例如 \(a=2\)，再取充分小的 \(\epsilon>0\)，便有
\[
 {\cal W}(V_\epsilon)>0.
\tag{AD.17}
\]

## 4. 两种符号与真实 \(\nu=1\) 周期 NS 解

压力依赖速度的二次张量，所以对任意光滑无散场
\[
 p_{-u}=p_u,\qquad {\cal W}(-u)=-{\cal W}(u).
\tag{AD.18}
\]
因此 AD.17 同时给出严格负压力功的零均值有限模态初值
\(-V_\epsilon\)。必须说明：\(u(t)\mapsto-u(t)\) 不是正向
Navier--Stokes 轨道的对称变换。这里是让两个初值
\(V_\epsilon\) 与 \(-V_\epsilon\) 分别生成各自的局部光滑解，
而不是声称一条解取负后仍满足同一正向方程。

还可以使正压力功真正超过黏性耗散。记
\[
 H(u)=\frac13\int_{\mathbb T^3}|u|^3,\qquad
 {\cal D}(u)=\int_{\mathbb T^3}
 \left(|u||\nabla u|^2+
       |u||\nabla|u||^2\right).
\tag{AD.19}
\]
对黏性 \(\nu=1\)、无外力的光滑周期 NS 解，全环面积分给
\[
 \frac{d}{dt}H(u(t))+{\cal D}(u(t))={\cal W}(u(t)).
\tag{AD.20}
\]
固定 AD.17 中的 \(U=V_\epsilon\)，再取幅值 \(A>0\)。有精确齐次性
\[
 H(AU)=A^3H(U),\qquad
 {\cal D}(AU)=A^3{\cal D}(U),\qquad
 {\cal W}(AU)=A^4{\cal W}(U).
\tag{AD.21}
\]
以 \(u(0)=AU\) 为初值的唯一局部光滑周期 NS 解因此满足
\[
 H'(0)
 =A^4{\cal W}(U)-A^3{\cal D}(U)
 =A^3\bigl(A{\cal W}(U)-{\cal D}(U)\bigr)>0
\tag{AD.22}
\]
只要 \(A>{\cal D}(U)/{\cal W}(U)\)。
这是 \(A^4\) 压力功压过 \(A^3\) 黏性耗散的真实
\(\nu=1\) NS 初始增长，不是运动学时钟。
\(AU\) 仍零均值且处处不消失；局部光滑解在充分短时间内保持
这一性质，AD.20 两侧连续。因此 AD.22 的严格正号还保持在某个
正时间区间。以 \(-AU\) 为另一初值时，
\[
 H'(0)=-A^4{\cal W}(U)-A^3{\cal D}(U)<0.
\tag{AD.23}
\]

## 5. 结论边界

1. \({\cal W}\) 在光滑、零均值、周期、无散速度类上没有普适正号或负号；
   特别不能把它不经支付地当作耗散项。
2. AD.22 是真实 NS 解的瞬时及短时初始行为，但幅值放大也放大初始能量。
   它不是固定能量族，也不是成熟时间、指定首次奇点附近的构造。
3. 本稿不否定带 \(L\)、\({\cal D}\)、压力、外壳或几何成本的定量估计，
   也没有给出反向持留窗口、尺度收缩或原合同 G。
4. 这里没有 NS 奇点、仿真或科学图；结论是 **NOT CLAY**。
   本地解析证明已完成内部实际文件独立审计，范围见本包审计记录。
