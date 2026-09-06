# 固定正则环带内的局部高频尾持留

2026-09-06。**INTERNAL / PROVED IN STATED SCOPE / LOCAL-PERSISTENCE ROUTE CLOSED / NOT FROZEN / G OPEN / NOT CLAY。**

本稿沿用 AO/AP 的同一个固定环带，并对 AT 的原无散高频场 \(h\)
直接使用 \(\theta^3|h|h\) 测试。局部量 \(\theta h\) 从未被称为
无散场，也不引入未经核对的 Bogovskii 修正。目标只是列全局部化成本，
判断能否得到一个实际局部小尾的短时持留，以及这一结论是否支付 AQ.8。

所有计算均在同一周期 Navier--Stokes 解的
\(I\cap(0,T_*)\) 内严格前奇点光滑紧区间上进行；
黏性为 \(1\)，空间为 \(\mathbb T^3=(-\pi,\pi]^3\)，范数不归一化。

## 1. 几何、频率分解与环带点值

沿用 AO.1--AO.3：

\[
 0<\rho_0<\rho_1<\rho_2<\rho_3<\rho_4<\rho_5<\pi/4,
\qquad
 \operatorname*{ess\,sup}_{\substack{\sigma\in I\\
          \rho_0<|x|<\rho_5}}|u(\sigma,x)|\le B.
\tag{AU.1}
\]

固定 \(0\le\theta\le1\)，使

\[
 \theta=1\ \hbox{于 }B_{\rho_3},\qquad
 \operatorname{supp}\theta\Subset B_{\rho_4}.
\tag{AU.2}
\]

取 \(\zeta\in C_c^\infty(B_{\rho_5})\)，使 \(\zeta=1\) 于
\(\operatorname{supp}\theta\) 的一个固定开邻域。所有
\(\nabla\theta\)、\(\zeta^2-\theta^2\) 与 \(\zeta-\theta\)
的支撑都包含在 AP.5 的一个更小固定闭环带内。

沿用 AK/AT 的同一个实偶平滑乘子

\[
 l=S_Ku,\qquad h=(I-S_K)u,\qquad K\ge1,
\qquad
 M=\sup_{0<\sigma<T_*}\|u(\sigma)\|_2.
\tag{AU.3}
\]

先记录只用 AP 点值和 Schwartz 核得到的环带事实。若 \(x\) 属于
上述更小闭环带，把 \(S_Ku(x)\) 的卷积分成仍位于 AP 环带内的近源
和具有固定正距离的远源。近源用 \(B\) 与周期核的统一 \(L^1\) 界，
远源用 \(\|u\|_1\le C M\) 及任意阶离对角衰减。于是每个整数
\(N\ge1\) 都有

\[
 |l(\sigma,x)|
 \le C_{\cal S}B+C_{{\cal S},N}M K^{-N},\qquad
 |h(\sigma,x)|\le C_{\cal S},
\tag{AU.4}
\]

其中 \({\cal S}\) 收集固定环带、截止、\(B,M\) 及乘子规范。
第二式使用 \(h=u-l\)。常数与 \(K,\sigma\) 以及到 \(T_*\) 的距离
无关。AU.4 没有使用 \(\nabla u\)、\(\partial_tu\) 或环带高阶导数。
全域低频界仍为

\[
 \|l\|_2+\|h\|_2\le CM,\qquad
 \|l\|_\infty\le CMK^{3/2},\qquad
 \|\nabla l\|_\infty\le CMK^{5/2}.
\tag{AU.5}
\]

## 2. 原高频方程和局部能量

AT.5 的精确方程是

\[
 \partial_th-\Delta h+\mathbb P\operatorname{div}(h\otimes h)
 =-\mathbb P\operatorname{div}(l\otimes h+h\otimes l)
   +f_0,
\tag{AU.6}
\]

其中完整低—低与低输出修正为

\[
 f_0=-\mathbb P\operatorname{div}(l\otimes l)
       +S_K\mathbb P\operatorname{div}(u\otimes u),
\qquad
 \|f_0\|_3\le CM^2K^3.
\tag{AU.7}
\]

AU.7 使用 AT 已核对的
“平滑低通导数核 \(L^1\to L^3\) 加周期 Leray \(L^3\) 有界性”，
不是把 Leray 原点误作光滑紧支撑乘子。

令

\[
 q=|h|,\qquad
 y(\sigma)=\|\theta h(\sigma)\|_3,\qquad
 w(\sigma)=y(\sigma)^3=\int\theta^3q^3,
\tag{AU.8}
\]

以及

\[
 D_\theta=\int\theta^3q
       \bigl(|\nabla h|^2+|\nabla q|^2\bigr).
\tag{AU.9}
\]

这里 \(y\) 是本稿的局部尾；它既不是 AT 的全域尾，也尚未与
AO.16 的阈值作数值识别。

## 3. \(q_\varepsilon\) 恒等式与 cutoff 余项

取

\[
 q_\varepsilon=(q^2+\varepsilon^2)^{1/2},\qquad
 E_{\theta,\varepsilon}
 =\frac13\int\theta^3(q_\varepsilon^3-\varepsilon^3),
\quad
 D_{\theta,\varepsilon}
 =\int\theta^3q_\varepsilon
       (|\nabla h|^2+|\nabla q_\varepsilon|^2).
\tag{AU.10}
\]

对 AU.6 使用 \(\theta^3q_\varepsilon h\) 测试。写
\(p_h=\pi[h\otimes h]\)、
\(p_c=\pi[l\otimes h+h\otimes l]\)，其中
\(-\Delta\pi[A]=\partial_i\partial_jA_{ij}\) 且取零均值。
由于 \(l,h\) 无散，直接积分分部得到

\[
 \begin{aligned}
 \frac{d}{d\sigma}E_{\theta,\varepsilon}
 +D_{\theta,\varepsilon}
 ={}&
 {\cal W}_{\theta,\varepsilon}(p_h)
 +{\cal W}_{\theta,\varepsilon}(p_c)\\
 &-\int\theta^3q_\varepsilon h_i h_j\partial_jl_i
 +\int f_0\cdot(\theta^3q_\varepsilon h)
 +{\cal R}_{\theta,\varepsilon},
 \end{aligned}
\tag{AU.11}
\]

这里 \(\theta\) 与 \(K\) 都在整段时间内固定，所以没有
\(\partial_t\theta\) 或 \(\partial_tS_K\) 项；若另乘时间 cutoff，
其导数与端点必须另外保留，本稿没有使用那一步。
这里保留完整压力配对

\[
 {\cal W}_{\theta,\varepsilon}(p)
 :=\int p\,\operatorname{div}(\theta^3q_\varepsilon h)
 =-\int\theta^3q_\varepsilon h\cdot\nabla p,
\tag{AU.12}
\]

而所有 Laplacian 与两个输运 cutoff 项精确收进

\[
 \begin{aligned}
 {\cal R}_{\theta,\varepsilon}
 ={}&-3\int\theta^2q_\varepsilon^2
             \nabla\theta\cdot\nabla q_\varepsilon\\
 &+\int\theta^2q_\varepsilon^3(h+l)\cdot\nabla\theta .
 \end{aligned}
\tag{AU.13}
\]

第一项用 Young 后留下
\(\int_{\operatorname{supp}\nabla\theta}\theta q^3\)。
由 AU.4 和

\[
 \int_{\operatorname{supp}\nabla\theta}\theta q^3
 \le
 \left(\int\theta^3q^3\right)^{1/3}
 \left(\int_{\operatorname{supp}\nabla\theta}q^3\right)^{2/3}
 \le C_{\cal S}y,
\tag{AU.14}
\]

而另两个输运余项由
\(\|\theta^2q^2\|_1\le Cw^{2/3}=Cy^2\) 和 AU.4 控制。
具体地，在 \(\operatorname{supp}\nabla\theta\) 上
\(q+|l|\le C_{\cal S}\)，所以令 \(\varepsilon\downarrow0\) 后
\(\theta^2q_\varepsilon^3(|h|+|l|)
\le C_{\cal S}\theta^2q^2+o(1)\)。
所以令 \(\varepsilon\downarrow0\) 后，对任意固定
\(\epsilon>0\)，

\[
 |{\cal R}_\theta|
 \le\epsilon D_\theta+C_{{\cal S},\epsilon}(y+y^2).
\tag{AU.15}
\]

这一步没有用环带梯度或时间导数。

## 4. 自压力的近、中、远分解

精确写成

\[
 \begin{aligned}
 p_h&=p_{h,0}+p_{h,a}+p_{h,f},\\
 p_{h,0}&=\pi[(\theta h)\otimes(\theta h)],\\
 p_{h,a}&=\pi[(\zeta^2-\theta^2)h\otimes h],\\
 p_{h,f}&=\pi[(1-\zeta^2)h\otimes h].
 \end{aligned}
\tag{AU.16}
\]

令 \(V=\|\theta h\|_9\)。对
\(|\theta h|^{3/2}\) 使用非齐次周期 Sobolev，并用 AU.4
支付 cutoff 梯度，得到

\[
 V^{3/2}
 \le C_{\cal S}\bigl(D_\theta^{1/2}
                     +y^{1/2}+y^{3/2}\bigr).
\tag{AU.17}
\]

其中 \(y^{1/2}\) 正来自 AU.14；不能把它静默删除。
周期 Calderón--Zygmund 与插值给

\[
 \|p_{h,0}\|_{9/4}\le CyV,\qquad
 \|p_{h,0}\|_{3/2}\le Cy^2.
\tag{AU.18}
\]

将 AU.12 展开成内部项与 \(\nabla\theta\) 项。前者用加权
Cauchy--Schwarz、AU.17--AU.18，后者在固定环带上用第二个
AU.18，得到

\[
 |{\cal W}_\theta(p_{h,0})|
 \le(C_{\cal S}y+\epsilon)D_\theta
     +C_{{\cal S},\epsilon}(y^2+y^3+y^5).
\tag{AU.19}
\]

中场张量支撑在固定正则环带，AU.4 给

\[
 \|p_{h,a}\|_6\le C_{\cal S}.
\tag{AU.20}
\]

内部压力项由
\(\|\theta^3q\|_{3/2}\le Cy\) 得
\(C_{\cal S}y^{1/2}D_\theta^{1/2}\)；cutoff 压力项使用
\(\|\theta^2q^2\|_{6/5}\le C y^2\)。因此

\[
 |{\cal W}_\theta(p_{h,a})|
 \le\epsilon D_\theta+C_{{\cal S},\epsilon}(y+y^2).
\tag{AU.21}
\]

远场源与 \(\operatorname{supp}\theta\) 有固定正距离。周期 Green
核的三阶导数在离对角区域有界，故

\[
 \|\nabla p_{h,f}\|_{L^\infty(\operatorname{supp}\theta)}
 \le C_{\cal S}\|h\otimes h\|_1\le C_{\cal S}M^2,
\qquad
 |{\cal W}_\theta(p_{h,f})|\le C_{\cal S}M^2y^2.
\tag{AU.22}
\]

AU.20--AU.22 只用环带点值、有限 \(L^q\) Riesz 有界性和远场
Green 核；没有要求中场压力的 \(L^\infty\) 或时间导数。

## 5. 交叉压力及其完整局部成本

使用一次幂的同一空间分解：

\[
 \begin{aligned}
 p_c&=p_{c,0}+p_{c,a}+p_{c,f},\\
 p_{c,0}&=\pi[l\otimes(\theta h)+(\theta h)\otimes l],\\
 p_{c,a}&=\pi[l\otimes((\zeta-\theta)h)
                    +((\zeta-\theta)h)\otimes l],\\
 p_{c,f}&=\pi[l\otimes((1-\zeta)h)
                    +((1-\zeta)h)\otimes l].
 \end{aligned}
\tag{AU.23}
\]

全域 Bernstein 只用于核心源：

\[
 \|p_{c,0}\|_3
 \le C\|l\|_\infty\|\theta h\|_3
 \le CMK^{3/2}y.
\tag{AU.24}
\]

内部加权项和 cutoff 项分别使用
\(\|\theta^3q\|_3\le y\) 与
\(\|\theta^2q^2\|_{3/2}=y^2\)。所以

\[
 |{\cal W}_\theta(p_{c,0})|
 \le\epsilon D_\theta
 +C_\epsilon M^2K^3y^3
 +C_{\cal S}MK^{3/2}y^3.
\tag{AU.25}
\]

\((\zeta-\theta)lh\) 的两个因子都位于固定环带，AU.4 给
\(\|p_{c,a}\|_6\le C_{\cal S}\)。因此与 AU.21 相同，

\[
 |{\cal W}_\theta(p_{c,a})|
 \le\epsilon D_\theta+C_{{\cal S},\epsilon}(y+y^2).
\tag{AU.26}
\]

最后，远场张量与测试支撑分离，且
\(\|(1-\zeta)lh\|_1\le C M^2\)。所以

\[
 \|\nabla p_{c,f}\|_{L^\infty(\operatorname{supp}\theta)}
 \le C_{\cal S}M^2,\qquad
 |{\cal W}_\theta(p_{c,f})|\le C_{\cal S}M^2y^2.
\tag{AU.27}
\]

交叉压力的中远场没有从“正则环带”偷取任何高阶导数。

## 6. 低频应变、完整强迫与闭合微分式

由 AU.5、AU.7，

\[
 \begin{aligned}
 \left|\int\theta^3q\,h_i h_j\partial_jl_i\right|
 &\le CMK^{5/2}w,\\
 \left|\int f_0\cdot(\theta^3q h)\right|
 &\le CM^2K^3y^2.
 \end{aligned}
\tag{AU.28}
\]

第二式使用
\(\|\theta^3q h\|_{3/2}\le y^2\)，完整保留了低—低压力和
\(S_K\) 修正。选择一个与 \(K\) 无关、但可依赖 \({\cal S}\) 的
小阈值 \(0<\eta_{\rm loc}\le1\)，使 AU.15、AU.19、
AU.21、AU.25、AU.26 中的耗散份额总和以及
\(C_{\cal S}yD_\theta\) 在 \(y\le\eta_{\rm loc}\) 时至多
\(\frac12D_\theta\)。于是停止区间内

\[
 \boxed{\quad
 w'+cD_\theta
 \le C A_Kw+C(F_K+C_{\cal S})w^{2/3}
             +C_{\cal S}w^{1/3},
 \quad}
\tag{AU.29}
\]

其中

\[
 A_K=1+MK^{5/2}+M^2K^3,\qquad F_K=M^2K^3.
\tag{AU.30}
\]

特别地，这一推导没有留下 \(g^2=\|\nabla u\|_2^2\)：
中场压力用 AU.4 给出的固定 \(L^6\) 界和加权耗散处理，
而没有去微分环带张量。若改用更粗的未加权环带估计，会出现
\(C_{\cal S}(1+g^2)\)，但它不是 AU.29 所必需的成本。

## 7. 停止时间与成熟窗口

从实际时刻 \(s\in I\cap(0,T_*)\) 出发，令首次停止值为
\(\eta_{\rm loc}\)。在停止前 \(y\le\eta_{\rm loc}\)，AU.29 给

\[
 w'\le CA_Kw+C(F_K+C_{\cal S})\eta_{\rm loc}^2
                  +C_{\cal S}\eta_{\rm loc}.
\tag{AU.31}
\]

因此可取

\[
 \tau_K^{\rm loc}=c_*
 \min\left\{
 A_K^{-1},\quad
 \frac{\eta_{\rm loc}}{F_K+C_{\cal S}},\quad
 \frac{\eta_{\rm loc}^2}{C_{\cal S}}
 \right\},
\tag{AU.32}
\]

其中零分母按 \(+\infty\) 解释，\(c_*>0\) 只依赖固定估计常数。
Gronwall 与首次停止反证表明

\[
 y(s)\le\frac14\eta_{\rm loc}
 \quad\Longrightarrow\quad
 y(\sigma)\le\frac34\eta_{\rm loc}
\tag{AU.33}
\]

只要
\(s\le\sigma<T_*\) 且 \(\sigma-s\le\tau_K^{\rm loc}\)。
这里 \(I\) 是 AP 的末端时间区间，所以这些 \(\sigma\) 仍在 \(I\) 内，
环带估计一直有效。这只使用原解已经存在且光滑的时间，不跨越 \(T_*\)。

现在取 AO.17 的同一固定 \(r=\rho_1\)：

\[
 \Lambda_A=\|u(t)\|_{L^3(B_r)},\qquad
 K=\Lambda_A^{3/4},\qquad
 \delta=c_0r^2\Lambda_A^{-4},\qquad
 J=(t-\delta,t).
\tag{AU.34}
\]

\(K\) 由终端选定后在整个 \(J\) 上固定。
固定 \(M,r,c_0,{\cal S}\)，沿合法
\(\Lambda_A\to\infty\) 序列，AU.30--AU.32 给

\[
 \tau_K^{\rm loc}\ge c_{{\cal S},M,\eta_{\rm loc}}
                         \Lambda_A^{-9/4},
\qquad
 \frac{\delta}{\tau_K^{\rm loc}}
 \longrightarrow0.
\tag{AU.35}
\]

若 \(J\) 中存在实际时刻 \(s\) 使
\(y(s)\le\eta_{\rm loc}/4\)，则 AU.33 可用到终端。因为
\(\theta=1\) 于 \(B_{\rho_3}\supset B_r\)，且
\(\|S_Ku(t)\|_3\le CMK^{1/2}\)，

\[
 \Lambda_A
 \le CM\Lambda_A^{3/8}+\frac34\eta_{\rm loc},
\tag{AU.36}
\]

与大 \(\Lambda_A\) 矛盾。因此最终有

\[
 \boxed{\quad
 \|\theta P_{>\Lambda_A^{3/4}}u(\sigma)\|_3
 >\frac14\eta_{\rm loc}
 \quad\text{对每个 }\sigma\in J.
 \quad}
\tag{AU.37}
\]

这仍是依赖固定解和固定环带的必要机制，不是统一缩球估计。
若 \(M=0\)，原解恒为零，不存在这里的
\(\Lambda_A\to\infty\) 分支。

## 8. 与 AO/AQ 的边界及停止结论

\(\eta_{\rm loc}\) 是 AU.29 的吸收阈值；AO.16 的
\(\eta_*\) 来自另一项原速度压力配对。两者不能仅因都是固定小常数
就视为相等。若重新选择固定公共阈值
\(0<\eta_{\rm com}\le\min\{\eta_*^{\rm AO},\eta_{\rm loc}/4\}\)
并重跑 AO--AQ 的集合定义，AU.37 会说明相应局部好集合最终为空；
但这仍不产生矛盾。未重跑定义时，不把这个结论写给原来的好集合。

原因是 AQ.8 给的是原测试
\(\chi|u|u\) 下坏时间净工作
\[
 \int_{s_J}^t w_J\mathbf1_{B_K}
 \left[{\cal K}_\chi(p_h)-\frac34D_\chi\right]\,d\sigma
\]
的条件必要下界。AU.29 测试的是
\(\theta^3|h|h\)，既没有给上述量的上界，也没有支付 AS.33 的
高高频率矩。即使 \(G_K=\varnothing\)，也只是可以在 AQ.8 的
\([s_J,t]\) 积分中删去坏集指标；积分域不能改成整个 \(J\)，因为
AS.7 的 \(\mu_J\) 在 \(s_J\) 之前仍为零。这个必要下界不会自行消失。

因此 AU 的新增结论仍只是“局部尾不能在候选窗口中降到固定小值”。
它没有得到新的 AQ 带符号上界，没有闭合 G、首次奇点或 Clay 问题。
按既定停止规则，这条局部持留路线不再继续扩写；下一步若继续研究，
应回到原带符号三频工作的真实抵消，而不是再次改名同一个必要机制。
本稿不含仿真、科学图、提交或发布动作。
