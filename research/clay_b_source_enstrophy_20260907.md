# 残差的梯度能量：源项、应变与二次组合的边界

2026-09-07。**CONDITIONAL METHOD SCREEN / NON-AUTHOR REVIEW PASS / G OPEN / NOT CLAY。**

我检查 BV 留下的加权时间成本是否能由梯度能量方程直接支付。
全周期压力在本次无散测试中确实消失，但二阶源项和应变不能一起消掉。
常系数正定二次组合也不能把反向与正向扩散同时变成正耗散。
这是一个有限方法判断，不是排除真实 NS 原子或所有能量方法。

## 1. 只在严格正时间上作二阶测试

沿用 BU/BV 的同一周期原解及额外正终端原子。
记 \(b=-u(T-\rho)\)、\(w=A(T-\rho)\)、\(z=b+cw\)、\(c=\sqrt m>0\)。
先固定 \(0<s<t\le L\)，不把任何梯度端点移到 \(\rho=0\)。
在这样的闭区间上，原解光滑，伴随由正延迟线性平滑得到所需导数。
设
\[
 \Gamma_v=\|\nabla v\|_2^2,\quad K_v=\|\Delta v\|_2^2,\quad
 H(v,h)=\int\nabla v:\nabla h,\quad
 J(v,h)=\int\Delta v\cdot\Delta h .
 \tag{BW.1}
\]
为避免与压力混淆，定义应变双线性式
\[
 B_b(v,h)=\frac12\int\partial_k b_j
       (\partial_jv_i\partial_kh_i+\partial_jh_i\partial_kv_i),
 \qquad
 B_b(v,h)=-\frac12\int[(b\cdot\nabla)v\cdot\Delta h
                        +(b\cdot\nabla)h\cdot\Delta v].
 \tag{BW.2}
\]
第二式由分部积分与 \(\operatorname{div}b=0\) 得到；
两个剩余项的和为 \(\int b\cdot\nabla(\nabla v:\nabla h)=0\)。
第一式括号对 \(j,k\) 对称，所以只看漂移梯度的对称部分。

将 BU.5 分别与 \(-\Delta b,-\Delta w,-\Delta z\) 配对，得到
\[
 \begin{aligned}
 \tfrac12\Gamma_b'-\nu K_b&=-B_b(b,b),\\
 \tfrac12\Gamma_w'+\nu K_w&=-B_b(w,w),\\
 \tfrac12\Gamma_z'-\nu K_z+2\nu cJ(z,w)&=-B_b(z,z),\\
 \tfrac12\Gamma_z'+\nu K_z&=2\nu J(b,z)-B_b(z,z).
 \end{aligned}
 \tag{BW.3}
\]
最后两行是同一残差方程的两种写法。
压力与全周期的无散 \(\Delta v\) 正交，故这里没有压力余项；
这是本次测试的真实抵消，不适用于带空间截止或幅度非线性测试。

同样极化得
\[
 H(z,w)'=-2\nu cK_w-2B_b(z,w),\qquad
 H(b,w)'=-2B_b(b,w).
 \tag{BW.4}
\]
相反黏性的交叉项抵消，第一式的二阶项来自 \(2\nu c\Delta w\) 源。
不能把源项也归到“反号黏性抵消”里。
这些式子受以下代数关系约束：
\[
 \Gamma_z=\Gamma_b+2cH(b,w)+c^2\Gamma_w,\qquad
 H(z,w)=H(b,w)+c\Gamma_w .
 \tag{BW.5}
\]
因此它们不是彼此独立的额外预算。
例如 BW.4 积分后仍保留 \(H(z,w)(s)\) 和有符号应变积分；
BU/BV 没有给 \(s\downarrow0\) 的统一梯度端点界。

## 2. 常系数正定二次组合不能共同正耗散

这里只检验一个明确的有限类别：对场对 \(Y=(z,w)\)，
取固定实对称正定 \(2\times2\) 矩阵 \(\mathsf K\)，在每个空间/向量分量
使用同一个二次梯度能量。
冻结最高阶部分为
\[
 D_\rho Y=\mathsf A\Delta Y-\nabla(q,\pi),\qquad
 \mathsf A=\nu\begin{pmatrix}-1&2c\\0&1\end{pmatrix},\qquad
 E_{\mathsf K}=\frac12\sum_{i,k}\int
             (\partial_kY_i)^T\mathsf K\,\partial_kY_i .
 \tag{BW.6}
\]
其扩散贡献是
\(-\sum_i\int(\Delta Y_i)^T\operatorname{sym}(\mathsf K\mathsf A)\Delta Y_i\)。
输运应变另计，不能改变这个最高阶矩阵的代数身份。

写 \(\mathsf K=\begin{pmatrix}a&d\\d&e\end{pmatrix}>0\)，直接计算
\[
 \operatorname{sym}(\mathsf K\mathsf A)
   =\nu\begin{pmatrix}-a&ca\\ca&2cd+e\end{pmatrix},\qquad
 \det\operatorname{sym}(\mathsf K\mathsf A)
   =-\nu^2a\,(e+2cd+c^2a)<0 .
 \tag{BW.7}
\]
因为 \(a>0\)，且括号等于 \((c,1)^T\mathsf K(c,1)>0\)。
也可直接用两个特征向量：
\[
 \mathsf A(1,0)^T=-\nu(1,0)^T,\qquad
 \mathsf A(c,1)^T=\nu(c,1)^T,\qquad
 \xi^T\operatorname{sym}(\mathsf K\mathsf A)\xi
       =\lambda\,\xi^T\mathsf K\xi
       \quad(\mathsf A\xi=\lambda\xi).
 \tag{BW.8}
\]
因此不存在此类矩阵，使扩散对所有二阶方向都为非负共同耗散。
这不声称实际同一原解能实现任意 Hessian 对；
也不排除变量权重、非局部形式、单个轨道的几何约束或有符号机制。
BU 的 \(L^2\) 配对和累计耗散关系没有在此提供一个二阶方向的锥约束。
不能把这条有限矩阵结论写成全部 NS 能量方法的不可能定理。

## 3. 正向残差式和应变估计留下什么成本

BW.3 的正向残差式可用 Young，但付出的是真实二阶原解成本：
\[
 \tfrac12\Gamma_z'+\frac{\nu}{2}K_z
 \le 2\nu K_b+|B_b(z,z)|.
 \tag{BW.9}
\]
这是 \(2\nu|J(b,z)|\le(\nu/2)K_z+2\nu K_b\)。
BU 已付的是 \(-2\nu\Delta b\in L^2_\rho H^{-1}_x\)，
它足以作零阶能量测试，不等于已付 \(K_b\) 的时间积分。

固定周期上 \(\nabla v\) 均值零，插值与 Fourier 恒等式给
\[
 \begin{aligned}
 |B_b(v,v)|
 &\le C\|\nabla b\|_2\|\nabla v\|_4^2
 \le C\|\nabla b\|_2\,\Gamma_v^{1/4}K_v^{3/4}\\
 &\le\eta\nu K_v+C(\eta\nu)^{-3}\Gamma_b^2\Gamma_v,
 \qquad \eta>0 .
 \end{aligned}
 \tag{BW.10}
\]
\(\|\nabla v\|_4\le C\|\nabla v\|_2^{1/4}\|\Delta v\|_2^{3/4}\)。
能量给 \(\Gamma_b\in L^1\)，没有给 \(\Gamma_b^2\in L^1\)。
不能用该未付系数直接作终端 Gronwall。
若先证明整个原解的 \(\int K_b<\infty\)，旧 BR.7--10 已说明这会给
原解在指定终点光滑延拓；它并不是一个已知更弱、接近自动成立的输入。

还可以保留 \(b=z-cw\) 的实际结构：
\[
 \tfrac12\Gamma_w'+\nu K_w
       =cB_w(w,w)-B_z(w,w).
 \tag{BW.11}
\]
由 BW.2 的输运形式及 \(\|\nabla w\|_6\le C\|\Delta w\|_2\)，
\[
 |B_z(w,w)|\le C\|z\|_3K_w .
 \tag{BW.12}
\]
这里需要的是以二阶 \(K_w\) 为密度的残差控制，
不是 BV 已提出、尚未支付的 \(\|z\|_3\Gamma_w\)。
而且即使这个混合应变能被吸收，自应变还在：
\[
 |cB_w(w,w)|\le Cc\,\Gamma_w^{3/4}K_w^{3/4}
 \le\eta\nu K_w+C(\eta\nu)^{-3}c^4\Gamma_w^3 .
 \tag{BW.13}
\]
没有把自应变的三次梯度能量当作已有可积项，也不假定残差的临界范数逐时小。

## 4. 直接对耗散加权并不会免费给出权重的变化

设 \(f\in C^1([s,t])\)。BU 的精确
\((\|w\|_2^2)'=-2\nu\Gamma_w\) 给
\[
 2\nu\int_s^t f\Gamma_w
   =f(s)\|w(s)\|_2^2-f(t)\|w(t)\|_2^2
                         +\int_s^t f'\|w\|_2^2 .
 \tag{BW.14}
\]
因此把 \(f\) 换成 \(\|z\|_3\) 之前，必须检查其端点和时间变化。
这里只写合法权重的恒等式，没有推导该范数的全时间有界变差。

实际残差方程的三次幅值测试也保留了成本。在严格正时间区间，
用 \(|z|z\) 测试正向残差方程，可由平滑幅值逼近在 \(z=0\) 处解释，得到
\[
 \frac13\frac d{d\rho}\|z\|_3^3
 +\nu\sum_k\int\left(|z||\partial_kz|^2+
                       \frac{(z\cdot\partial_kz)^2}{|z|}\right)
 =2\nu\sum_k\int\partial_kb\cdot\partial_k(|z|z)
                       +\int q\,\operatorname{div}(|z|z).
 \tag{BW.15}
\]
分式在 \(z=0\) 定义为零。
压力项在这里不再消失，因为 \(|z|z\) 一般不无散；
源项含 \(|z||\nabla b||\nabla z|\)。
这些加权项未由能量给出可到 \(\rho=0\) 的绝对可积上界。
对 \(\|z\|_3^3\) 的局部可微性不能自动推出 \(\|z\|_3\) 的终端有界变差，
更不能略过其可能的零值和除法问题。

## 5. 拟用的二阶时间接口已经强迫强初迹

还有一个只针对本节共同伴随的准确条件结论：
\[
 \int_0^\delta\|\Delta w(\rho)\|_2^{4/3}\,d\rho=+\infty,
 \qquad
 \int_0^\delta K_w(\rho)\,d\rho=+\infty
       \quad\text{每个 }0<\delta\le L .
 \tag{BW.16}
\]
第二项由第一项和有限区间的 \(L^2\subset L^{4/3}\) 得到。
证明采用反证，并没有假设任意奇点都产生这个伴随。
若第一项有限，BU.9 已付的 \(b\in L^4_\rho L^3_x\) 与
\(\|\nabla w\|_6\le C\|\Delta w\|_2\) 使
\(P[(b\cdot\nabla)w]\in L^1_\rho L^2_x\)。
投影方程 \(w_\rho=\nu\Delta w-P[(b\cdot\nabla)w]\) 因而给，
对 \(0<a<d\le\delta\)，
\[
 \|w(d)-w(a)\|_2
 \le\left[\nu(d-a)^{1/4}
                  +C\|b\|_{L^4(a,d;L^3)}\right]
             \|\Delta w\|_{L^{4/3}(a,d;L^2)}
 \longrightarrow0\qquad(a,d\downarrow0).
 \tag{BW.17}
\]
空间 Hölder 用 \(3,6\)，时间用 \(4,4/3\)；
热项还用有限区间的时间 Hölder。投影只用 \(L^2\) 收缩性。
在反证假设下，这些范数的积分绝对连续，所以
\(w(\rho)\) 在 \(\rho\downarrow0\) 有强 \(L^2\) 迹。
但 BU.2 给弱迹零和 \(\|w(\rho)\|_2^2\to1\)，矛盾。

这是强迹机制对当前 \(w\) 的具体应用，与 BQ/BR 的思路相同；
这里用已付 \(b\in L^4L^3\) 精确核出 \(4/3\) 的二阶成本。
不把它报告为新的普遍正则性理论，也没有由此构造原子。
有限一阶耗散和这个二阶发散完全相容。
不能从 BW.3 中删掉未受控的梯度初端，再宣布该二阶输入成立。

原本有如下正确的充分估计：
\[
 \mathcal W_z(0,\delta)
 \le\|w\|_{L^\infty_\rho L^2_x}
       \|z\|_{L^4_\rho L^3_x}\,
       \|\Delta w\|_{L^{4/3}_\rho L^2_x}.
 \tag{BW.18}
\]
先用 \(\Gamma_w=-\int w\cdot\Delta w
\le\|w\|_2\|\Delta w\|_2\)，再作时间 Hölder 即得。
但 BW.16 说明：右端所需的有限二阶范数，
已经与本节所假定的正原子结构不相容。
它不是一个只用于消除混合功、且已经接近支付的小幅正则性加强。

这个蕴含必须保持单向。
不能从右端范数无穷和上界 BW.18 反推 \(\mathcal W_z=\infty\)；
本节没有证明两者等价，也没有否定利用同一原解的相关结构控制
\(\mathcal W_z\) 或直接有符号混合功的可能性。
自压力端点也不因这条二阶反证而自动消失。

## 6. 本项结论和停止点

本项没有证明 BV 的两条充分接口成立，也没有取得更弱的实际有符号混合功上界。
全周期二阶测试确实消掉压力，却留下二阶源、应变和未受控的梯度端点；
改做幅值权重后压力又明确出现。
常系数正定二次组合的共同正耗散已在上述有限类别内排除。

因此我停止自动微调这个二次梯度能量分支。
后续问题必须带来不同的信息，不能继续以改写同一成本作为完成主桥梁的证据。
这不是实际 NS 轨道的不可能定理，也没有宣布原子条件无法排除。
自压力、原子生成与排除、任意奇点到原子分支的连接、G、
R.216--R.217 和一般三维正则性均保持 OPEN。
