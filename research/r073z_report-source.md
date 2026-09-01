# R0.73Z｜正三次 heat covariance 的有限性障碍与能量兼容修复

**副标题：** 从 \(D_{ii,s}^{3/2}\) 的初始端点发散，到
\(D_{ii,s}\sqrt{k_s}\) 的能量级有限性与 pressure-active 分离见证

**日期：** 2026-09-01

**状态：** EXACT ANALYTIC THEOREMS + EXACT FOURIER CERTIFICATE +
INDEPENDENT AUDIT + BOUNDED PRIMARY-SOURCE AUDIT

**普通翻译路径：** LOCAL DIRECT / NO DGX

**DGX used：** false

## 1. 本节直接结论

R0.73Y 冻结的候选

\[
 \mathcal D_{3/2}^{\square}
 ={1\over R}\int_{I_R^\square}\int_0^{\theta R^2}
 \int_{B_R}D_{ii,s}^{3/2}\,dx\,ds\,dt
\tag{1.1}
\]

通过了三个形式关口：

1. 在 Navier--Stokes scaling 下无量纲；
2. 对振幅精确三次齐次；
3. 对所有非平凡 periodic smooth 场，正尺度 kernel 只剩常向量。

但它没有通过能量类有限性关口。存在一个零压、全局
Leray--Hopf、suitable、每个 \(t>0\) 都光滑的 exact shear，使

\[
 \int_0^{T_*}\int_{s_0}^{s_1}\int_{B_R}
 D_{ii,s}^{3/2}\,dx\,ds\,dt=+\infty
\tag{1.2}
\]

对任意 \(T_*>0\) 和任意固定正尺度带
\(0<s_0<s_1\) 成立。发散只发生在时间区间触及 \(L^2\) 初始迹时；
它不是 interior singularity，也不否定 smooth-cylinder finiteness。

因此，\(\mathcal D_{3/2}\) 在 general suitable-weak 层面只能先作为
\([0,+\infty]\)-值的非负 functional。不能未经证明把它写成有限的
epsilon-regularity input。

本节给出的修复是

\[
 \boxed{
 \mathcal K_D^\square
 ={\nu\over R^2}\int_{I_R^\square}\int_0^{\theta R^2}
 \int_{B_R}D_{ii,s}\,k_s^{1/2}\,dx\,ds\,dt,}
\tag{1.3}
\]

其中

\[
 k_s={1\over2}\left(P_s|u|^2-|P_su|^2\right).
\tag{1.4}
\]

它保留非负性、尺度不变性和三次齐次，却能由 Leray energy 直接控制。
这是一条真正的正向估计，但仍不是 CKN coercivity。

## 2. 原候选为什么在 smooth 层面正确

梯度 covariance 是严格非负的 heat variance：

\[
 D_{ii,s}
 =P_s|\nabla u|^2-|\nabla P_su|^2
 =2\int_0^sP_{s-r}|\nabla^2P_ru|^2\,dr.
\tag{2.1}
\]

若 cylinder 闭包紧含于 smooth lifespan，且

\[
 M_2=\sup_t\|\nabla^2u(t)\|_\infty<\infty,
\tag{2.2}
\]

则

\[
 0\le D_{ii,s}\le2sM_2^2.
\tag{2.3}
\]

所以 \(D_{ii,s}^{3/2}=O(s^{3/2})\)，\(s=0\) 端点可积。

对 NSE scaling

\[
 u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x),
\tag{2.4}
\]

有

\[
 D_s[u_\lambda](t,x)
 =\lambda^4D_{\lambda^2s}[u](\lambda^2t,\lambda x).
\tag{2.5}
\]

\(D^{3/2}\) 给出 \(\lambda^6\)，
\(dt\,dx\,ds\) 给出 \(\lambda^{-7}\)，而 \(R^{-1}\) 给出
\(\lambda\)，总次数为零。对振幅 \(A\)，

\[
 \mathcal D_{3/2}[Au]
 =|A|^3\mathcal D_{3/2}[u].
\tag{2.6}
\]

这些性质全部成立；失败发生在 suitable-weak 有限值，而不是形式尺度。

## 3. 精确初始端点反例

先看光滑高频族

\[
 u^{(n)}(t,x)=e^{-\nu n^2t}\sin(nx_2)e_1.
\tag{3.1}
\]

在固定正尺度带 \(s\in[s_0,s_1]\) 上，periodic heat kernel 有正下界。
令 \(G_n=\partial_2u_1^{(n)}\)，则

\[
 D_s(t,x)\ge\kappa\|G_n(t)\|_{L^2(\mathbb T)}^2.
\tag{3.2}
\]

在

\[
 J_n=[(2\nu n^2)^{-1},(\nu n^2)^{-1}]
\tag{3.3}
\]

上，\(\|G_n(t)\|_2\gtrsim n\)，所以

\[
 \int_{J_n}\int_{s_0}^{s_1}\int_{B_R}
 D_s^{3/2}\gtrsim n.
\tag{3.4}
\]

但三维 torus 上

\[
 \sup_t\|u^{(n)}(t)\|_2^2=4\pi^3,\qquad
 \nu\int_0^\infty\|\nabla u^{(n)}\|_2^2dt=2\pi^3,
\tag{3.5}
\]

完全不依赖 \(n\)。因此没有只依赖 bare energy、又能统一穿过初始端点的
有限三次上界。

把这一非紧性装进一个解，取

\[
 N_j=8^j,\qquad a_j=2^{-j}=N_j^{-1/3},
\tag{3.6}
\]

\[
 F_0(\xi)=\sum_{j\ge1}a_j\sin(N_j\xi),
\qquad
 u(t,x)=e^{\nu t\partial_2^2}F_0(x_2)e_1.
\tag{3.7}
\]

因为

\[
 \sum_ja_j^2={1\over3}<\infty,
\tag{3.8}
\]

初值属于 \(L^2\)。有限 Fourier truncation 的局部能量等式在
\(L_t^\infty L_x^2\cap L_t^2H_x^1\) 强极限下传递，所以该解是 suitable。
另一方面，每个 disjoint interval

\[
 J_j=[(2\nu N_j^2)^{-1},(\nu N_j^2)^{-1}]
\tag{3.9}
\]

至少贡献常数倍

\[
 a_j^3N_j=1.
\tag{3.10}
\]

无限求和得到 (1.2)。

这条反例的边界必须保留：任意 \(\delta>0\) 后，解在
\([\delta,T_*]\) 上解析，原 functional 有限。R0.73X 的 interior
cylinder 假设没有被一个已知奇解击穿。

## 4. 能量兼容修复

速度 covariance 与梯度 covariance 分别满足

\[
 0\le k_s\le\frac12P_s|u|^2,\qquad
 0\le D_s\le P_s|\nabla u|^2.
\tag{4.1}
\]

三维 periodic heat flow 的 \(L^1\to L^\infty\) 估计给

\[
 \|P_s|u|^2\|_\infty^{1/2}
 \le Cs^{-3/4}\|u\|_2.
\tag{4.2}
\]

于是

\[
 \int_{B_R}D_s\sqrt{k_s}\,dx
 \le Cs^{-3/4}\|u(t)\|_2\|\nabla u(t)\|_2^2.
\tag{4.3}
\]

因为

\[
 \int_0^{\theta R^2}s^{-3/4}ds
 =4\theta^{1/4}R^{1/2},
\tag{4.4}
\]

得到严格的 energy-class 上界

\[
 \boxed{
 \mathcal K_D[I,B_R;\theta]
 \le C_{\mathbb T^3}\nu\theta^{1/4}R^{-3/2}
 \left(\operatorname*{ess\,sup}_{t\in I}\|u(t)\|_2\right)
 \int_I\|\nabla u(t)\|_2^2dt.}
\tag{4.5}
\]

修复的核心不是形式拼接，而是把原来不可用的时间需求
\(\|\nabla u\|_2^3\) 改成 Leray 可积的
\(\|u\|_2\|\nabla u\|_2^2\)。

对固定 \(t,s>0\)，严格正 periodic heat kernel 还给出

\[
 D_s(x)\sqrt{k_s(x)}=0
 \quad\Longleftrightarrow\quad
 u(t,\cdot)\ \text{为空间常值}.
\tag{4.6}
\]

因此在非退化时间区间上，\(\mathcal K_D=0\) 当且仅当速度对几乎处处
物理时间为空间常值。对 unforced periodic NSE，这进一步是
time-independent Galilean mode。

## 5. 当前能证明的 local lower bound

固定

\[
 0<\alpha<\beta\le\theta,\qquad
 s\in[\alpha R^2,\beta R^2].
\tag{5.1}
\]

对 \(x,y\in B_R\)，一个 lifted Gaussian 项满足

\[
 g_s(x-y)\ge c_{\alpha,\beta}R^{-3}.
\tag{5.2}
\]

定义

\[
 V_R=\int_{B_R}|u-u_{B_R}|^2,\qquad
 G_R=\int_{B_R}|\nabla u-(\nabla u)_{B_R}|^2.
\tag{5.3}
\]

限制两个 variance 到 \(B_R\) 后，

\[
 D_s\ge cR^{-3}G_R,\qquad
 k_s\ge cR^{-3}V_R.
\tag{5.4}
\]

从而

\[
 \boxed{
 {\nu\over R^2}\int_I\int_{\alpha R^2}^{\beta R^2}
 \int_{B_R}D_s\sqrt{k_s}
 \ge c_{\alpha,\beta}\nu R^{-3/2}
 \int_I G_RV_R^{1/2}dt.}
\tag{5.5}
\]

这只能称为 centered-oscillation product lower bound。它不是同一个
group action 下的 first-jet quotient；local affine profile 会令
\(G_R=0\)，使右端完全退化。这里没有提前申报 CKN coercivity。

## 6. Pressure-active 分离见证

R0.73Y 的 exact shear 具有 \(p=Q_s=0\)。本节进一步取

\[
 u(t,x)=e^{-\nu n^2t}
 \left(A\sin(nx_2)e_1+B\sin(nx_1)e_2\right),
\tag{6.1}
\]

\[
 p(t,x)=ABe^{-2\nu n^2t}\cos(nx_1)\cos(nx_2).
\tag{6.2}
\]

直接计算得到

\[
 (u\cdot\nabla)u+\nabla p=0,
\tag{6.3}
\]

所以这是 exact NSE trajectory。它本身不是新解：等幅特例属于经典
二维 Taylor--Green 表示，一般 \(A,B\) 是同一 Laplacian eigenspace
中的 steady Euler flow 经 viscous decay。

令 \(r=e^{-n^2s}\)。Gaussian factorization 给

\[
 \tau_{12,s}=0.
\tag{6.4}
\]

resolved gradient 只有两个 off-diagonal entries，因此

\[
 \boxed{\Pi_s=\mathscr S_s=0}
\tag{6.5}
\]

对所有 \(t,x,s>0\) 成立。但精确定义的 pressure--velocity covariance

\[
 Q_s=P_s(pu)-P_sp\,P_su
\tag{6.6}
\]

满足

\[
 \begin{aligned}
 Q_{1,s}
 &=\frac{A_t^2B_t}{2}(r^5-r^3)
 \cos(nx_1)\sin(2nx_2),\\
 Q_{2,s}
 &=\frac{A_tB_t^2}{2}(r^5-r^3)
 \sin(2nx_1)\cos(nx_2),
 \end{aligned}
\tag{6.7}
\]

其中 \(A_t=Ae^{-\nu n^2t}\)，\(B_t=Be^{-\nu n^2t}\)。
若 \(AB\ne0\)，则 \(Q_s\not\equiv0\)。在
\(A_t=B_t>0\)、\(nx_1=nx_2=\pi/3\) 处，

\[
 \nabla\cdot Q_s={3nA_t^3\over4}(r^3-r^5)>0.
\tag{6.8}
\]

所以存在 compact nonnegative bump \(\chi\)，使

\[
 \int Q_s\cdot\nabla\chi
 =-\int\chi\,\nabla\cdot Q_s<0.
\tag{6.9}
\]

这证明：即使两种 production 都逐点为零，local pressure-cutoff debt
仍然会重新激活。

同一个见证的正 covariance 是

\[
 D_s={n^2\over2}(1-r^2)
 \left[
 A_t^2(1-r^2\cos2nx_2)
 +B_t^2(1-r^2\cos2nx_1)
 \right]>0.
\tag{6.10}
\]

因此 \(\mathcal D_{3/2}\) 和 \(\mathcal K_D\) 都消除了这一
pressure-active production kernel。

## 7. 证书与审计

deterministic certificate 在

\[
 \mathbb Q[i][A,B,r][\mathbb Z^2]
\tag{7.1}
\]

中完成 12 项 exact check：

- NSE residual；
- cross stress \(\tau_{12}\)；
- signed production；
- third-centered flux divergence 与 centered production；
- 两个 pressure covariance component；
- gradient covariance；
- subfilter energy。

它还精确核验高频能量常数 \(6\pi^3\)，以及

\[
 N_j=8^j,\qquad a_j=2^{-j},\qquad
 \sum_ja_j^2={1\over3},\qquad a_j^3N_j=1.
\tag{7.2}
\]

证书是解析证明的 executable cross-check，不承担普遍量词。

独立审计逐项复算了端点发散、energy upper bound、exact kernel 与 local
Gaussian lower bound。审计要求并已完成三个修正：

1. 补写 suitable 极限；
2. 把 integrated kernel 写成 a.e.-time spatial constants；
3. 把 first-jet coercivity 降格为 centered-oscillation product bound。

## 8. 文献校准

本节不能把下列构件称为新：

- positive Gaussian covariance 与 realizability；
- Gaussian scale-as-heat-time 和 exact stress evolution；
- signed production 与 positive viscous covariance 的分账；
- cubic weak energy defect；
- heat-semigroup Besov/carré-du-champ 框架；
- \(\sqrt{k_{\rm sgs}}\) 作为 unresolved velocity scale 的 LES 模型；
- simple-shear zero SGS production；
- crossed cellular/Taylor--Green-type exact solution。

两轮 bounded primary-source audit 没有定位到完全同式的
\(D_s^{3/2}\) 或 \(D_s\sqrt{k_s}\) local scale-space functional，也没有
定位到同一 classical crossed witness 上
\(\Pi_s=\mathscr S_s=0\)、\(Q_s\ne0\) 的三项并列命题。这只能写成
bounded non-hit，不能写成 novelty proof。

## 9. 研究价值

R0.73Z 有两项可靠增量。

第一，它关闭了一个原本看似自然、实际在能量层级不稳的候选：
\(D_s^{3/2}\) 的 smooth 性质正确，但不能自动穿过 \(L^2\) 初始端点。
这避免后续在一个 undefined-or-infinite epsilon input 上继续搭桥。

第二，它给出一个目前确实能落在 Leray energy class 上的 positive cubic
observable，并证明其 exact kernel 与 local centered-oscillation lower
bound。pressure-active crossed witness 又说明，修复不能只 quotient
zero-pressure shears；pressure covariance 必须被独立支付。

对 Clay 问题的直接推进仍然有限。我们还没有得到 arbitrary suitable weak
solutions 上的 local CKN coercivity、compactness、epsilon regularity 或
global smoothness。作为论文方向，当前组合比 R0.73Y 更强：它包含一个
exact endpoint obstruction、一个 energy-compatible positive theorem 和一个
pressure-active separation witness；但在宣布高水平新结果前仍需完成更深的
引用链审计和真正的 local payment theorem。

## 10. R0.74A 冻结任务

下一节只攻击一个接口：

> 能否把 \(\mathcal K_D^\square\) 的 global energy upper bound 局部化为
> \(\mathcal E^\square(z_0,4R)^{3/2}\) 加一个最小、明确、可缩放的 exterior
> velocity/gradient tail，并用它支付 crossed witness 激活的
> \(Q_s\cdot\nabla\chi\)？

依次执行：

1. 对 \(k_s\) 与 \(D_s\) 同时做 core/exterior Gaussian annulus split；
2. 确定 exterior gradient tail 是否可由 R0.73X 的 velocity/pressure tail
   推出，或必须作为新独立债务；
3. 在 crossed family 上精确测试每一项的振幅与 \(R\)-scaling；
4. 证明 local upper payment，或给出 exact counterexample；
5. 只有 payment 关闭后，才重新讨论 quotient coercivity。

**NOT CLAY.**

## 参考文献

1. B. Vreman, B. Geurts, and H. Kuerten, *J. Fluid Mech.* **278**
   (1994), [DOI](https://doi.org/10.1017/S0022112094003745).
2. M. Germano, *J. Fluid Mech.* **238** (1992),
   [DOI](https://doi.org/10.1017/S0022112092001733).
3. G. L. Eyink and H. Aluie, *Physics of Fluids* **21** (2009),
   [DOI](https://doi.org/10.1063/1.3266883),
   [arXiv](https://arxiv.org/abs/0909.2386).
4. P. L. Johnson, *Phys. Rev. Lett.* **124** (2020),
   [DOI](https://doi.org/10.1103/PhysRevLett.124.104501),
   [arXiv](https://arxiv.org/abs/1912.00293).
5. J. Duchon and R. Robert, *Nonlinearity* **13** (2000),
   [DOI](https://doi.org/10.1088/0951-7715/13/1/312).
6. M. Ledoux, *Ann. Fac. Sci. Toulouse* **9** (2000),
   [record](https://numdam.org/item/AFST_2000_6_9_2_305_0/).
7. P. Alonso-Ruiz et al., *J. Funct. Anal.*,
   [arXiv:1811.04267](https://arxiv.org/abs/1811.04267).
8. A. W. Vreman, *Physics of Fluids* **16** (2004),
   [DOI](https://doi.org/10.1063/1.1785131).
9. A. Yoshizawa and K. Horiuti, *J. Phys. Soc. Japan* **54** (1985),
   [DOI](https://doi.org/10.1143/JPSJ.54.2834).
10. C. Meneveau and J. O'Neil, *Phys. Rev. E* **49** (1994),
    [DOI](https://doi.org/10.1103/PhysRevE.49.2866).
11. G. I. Taylor and A. E. Green, *Proc. R. Soc. A* **158** (1937),
    [DOI](https://doi.org/10.1098/rspa.1937.0036).
