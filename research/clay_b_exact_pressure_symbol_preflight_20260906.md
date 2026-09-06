# 原高高压力功的精确方向—相位账本

2026-09-06。**INTERNAL / PENDING REVIEW / G OPEN / NOT CLAY。**

本稿只处理 exact-pressure-geometry 计划中的第一个有限问题。我保留
原来的高频速度 \(h=P_{>K}u\)、空间截止 \(\chi\) 和原测试
\(F_\chi=\chi |u|u\)，直接展开高高压力功的 Fourier 符号。这里的
方向因子在取绝对值以前确实比 AS 的账本细；在压力侧按 AS 的方式
求和，它仍由同一个 \(\mathfrak R_{K,L}\) 控制。若保留原测试的输出
频率匹配，半阶 Sobolev 配对还能消去这个静态频率矩，但留下未付的
时间成本 \(\int g^4\)。以下不假设模态对齐、相位有利或某个临界
范数已经有界。

## 1. Fourier 约定、零模与原测试

在 \(\mathbb T^3=(-\pi,\pi]^3\) 上记
\(V_{\mathbb T}=(2\pi)^3\)，并采用

\[
 \widehat f(k)=V_{\mathbb T}^{-1}
       \int_{\mathbb T^3}f(x)e^{-ik\cdot x}\,dx,
 \qquad
 f(x)=\sum_{k\in\mathbb Z^3}\widehat f(k)e^{ik\cdot x}.
\tag{AW.1}
\]

因此

\[
 \int_{\mathbb T^3}f\,\overline g\,dx
 =V_{\mathbb T}\sum_k\widehat f(k)\overline{\widehat g(k)},
 \qquad
 \widehat f(-k)=\overline{\widehat f(k)}
 \quad(f\text{ 实值}).
\tag{AW.2}
\]

沿用 AK--AS 的实偶平滑截止，固定 \(K\ge1\)，令

\[
 h=P_{>K}u,\qquad
 \xi\cdot\widehat h(\xi)=0,\qquad
 \widehat h(0)=0.
\tag{AW.3}
\]

高高压力取零均值规范

\[
 p_h=T_{ij}(h_i h_j),\qquad
 T_{ij}=\partial_i\partial_j(-\Delta)^{-1},\qquad
 \widehat p_h(0)=0.
\tag{AW.4}
\]

写 \(q=|u|\) 及

\[
 F_\chi=\chi q u,\qquad
 g_\chi=\operatorname{div}F_\chi,\qquad
 \widehat g_\chi(\kappa)
   =i\kappa\cdot\widehat F_\chi(\kappa),\qquad
 \widehat g_\chi(0)=0.
\tag{AW.5}
\]

原测试因子的系数是

\[
 \widehat F_{\chi,a}(\kappa)
 =\sum_{\rho\in\mathbb Z^3}
   \widehat\chi(\kappa-\rho)\,\widehat{q u_a}(\rho).
\tag{AW.6}
\]

特别地，\(\widehat{qu}(\rho)\) 是非多项式场 \(|u|u\) 的真实 Fourier
系数；它不是第三个速度模，也不能改写成两个 \(h\) 模的简单卷积。

## 2. 压力系数中的两个无散收缩

对 \(\kappa\ne0\)，由 AW.4 的乘子符号直接得到

\[
 \widehat p_h(\kappa)
 =-\frac{\kappa_i\kappa_j}{|\kappa|^2}
    \sum_{\xi+\eta=\kappa}
       \widehat h_i(\xi)\widehat h_j(\eta)
 =-\sum_{\xi+\eta=\kappa}
   \frac{(\kappa\cdot\widehat h(\xi))
         (\kappa\cdot\widehat h(\eta))}{|\kappa|^2}.
\tag{AW.7}
\]

每个输入模各自无散，故在 \(\kappa=\xi+\eta\) 时可分别替换

\[
 \kappa\cdot\widehat h(\xi)=\eta\cdot\widehat h(\xi),
 \qquad
 \kappa\cdot\widehat h(\eta)=\xi\cdot\widehat h(\eta).
\tag{AW.8}
\]

于是精确公式是

\[
 \boxed{\quad
 \widehat p_h(\kappa)
 =-\sum_{\xi+\eta=\kappa}
   \frac{(\eta\cdot\widehat h(\xi))
         (\xi\cdot\widehat h(\eta))}{|\kappa|^2},
 \qquad \kappa\ne0.
 \quad}
\tag{AW.9}
\]

当 \(\eta=-\xi\) 时输出为零模，AW.9 不使用；AW.4 已把该压力模设为
零。此时 AW.8 的两个分子收缩也各自为零，但不能把它们与
\(|\kappa|^2=0\) 写成未定义的 \(0/0\)。

## 3. 保留相位的完整压力功

AS 的原带符号配对为

\[
 {\cal K}_\chi(p_h)
 =\int_{\mathbb T^3}p_h g_\chi\,dx
 =-\int_{\mathbb T^3}F_\chi\cdot\nabla p_h\,dx.
\tag{AW.10}
\]

把 AW.9 代入 AW.10，得到

\[
 \boxed{\quad
 {\cal K}_\chi(p_h)
 =-V_{\mathbb T}\operatorname{Re}
   \sum_{\substack{\xi,\eta\in\mathbb Z^3\\
                    \kappa=\xi+\eta\ne0}}
   \frac{(\eta\cdot\widehat h(\xi))
         (\xi\cdot\widehat h(\eta))}{|\kappa|^2}
       \overline{\widehat g_\chi(\kappa)}.
 \quad}
\tag{AW.11}
\]

等价地，由 AW.5，

\[
 {\cal K}_\chi(p_h)
 =V_{\mathbb T}\operatorname{Re}
   \left[
   i\sum_{\substack{\xi,\eta\\\kappa=\xi+\eta\ne0}}
   \frac{(\eta\cdot\widehat h(\xi))
         (\xi\cdot\widehat h(\eta))}{|\kappa|^2}
       \kappa\cdot\overline{\widehat F_\chi(\kappa)}
   \right].
\tag{AW.12}
\]

若 \(P_{>L}\) 的实偶乘子记为
\(m_{>L}(\kappa)=1-\varphi(\kappa/L)\)，则 AW.11--AW.12 中每项只需
再乘 \(m_{>L}(\kappa)\)，即得到
\({\cal K}_\chi(p_h^{>L})\)。固定 \(K,L\) 后，仍按 AQ 在
\([s_J,t]\) 上取
\(\mu_J=w_J\mathbf1_{B_K}\)、\(0\le\mu_J\le1\)，不向 \(s_J\)
以前扩大积分。于是

\[
 \begin{aligned}
 &\int_{s_J}^{t}\mu_J(\sigma)
       {\cal K}_\chi(p_h^{>L})(\sigma)\,d\sigma\\
 &\quad=-V_{\mathbb T}\operatorname{Re}
   \sum_{\substack{\xi,\eta\\\kappa=\xi+\eta\ne0}}
   \int_{s_J}^{t}\mu_J(\sigma)m_{>L}(\kappa)
   \frac{(\eta\cdot\widehat h(\xi,\sigma))
         (\xi\cdot\widehat h(\eta,\sigma))}{|\kappa|^2}
       \overline{\widehat g_\chi(\kappa,\sigma)}\,d\sigma .
 \end{aligned}
\tag{AW.13}
\]

这里没有改动 AQ 的区间 \([s_J,t]\)、坏时间指标或相位。所有重排先在
严格前奇点的光滑闭时间区间上作：\(h\) 的 Fourier 尾一致快速衰减，
\(F_\chi=\chi|u|u\) 只需 \(C^1\)，且
\(|\widehat g_\chi|\le V_{\mathbb T}^{-1}\|g_\chi\|_1\)。因此先有限
截断再取极限即可合法交换频率和与有界时间积分。

为看清符号，定义

\[
 Z_{\xi,\eta}
 =(\eta\cdot\widehat h(\xi))
  (\xi\cdot\widehat h(\eta))
  \overline{\widehat g_\chi(\xi+\eta)}.
\tag{AW.14}
\]

若 \(Z_{\xi,\eta}=|Z_{\xi,\eta}|e^{i\Phi_{\xi,\eta}}\)，则 AW.11 中该
有序对的实贡献是
\(-V_{\mathbb T}|Z_{\xi,\eta}|\cos\Phi_{\xi,\eta}/|\xi+\eta|^2\)。
负三元组 \((-\xi,-\eta,-\kappa)\) 给共轭项；交换 \(\xi,\eta\)
保留同一个标量乘积，并对应卷积中真实存在的另一有序对。因此总和实值，
却没有逐项固定符号。AD 已独立给出完整 \(L^3\) 压力功的双符号例；
这里不是重新发现该事实，而是把本轮高高压力的相位位置写清。

## 4. 精确方向权重及四种几何

令 \(\xi,\eta\ne0\)、\(\kappa=\xi+\eta\ne0\)，并令
\(\alpha\in[0,\pi]\) 为两输入频率的夹角。正交投影给

\[
 |\eta\cdot\widehat h(\xi)|
 \le\frac{|\xi\times\eta|}{|\xi|}|\widehat h(\xi)|,
 \qquad
 |\xi\cdot\widehat h(\eta)|
 \le\frac{|\xi\times\eta|}{|\eta|}|\widehat h(\eta)|.
\tag{AW.15}
\]

因此自然的方向—输出权重是

\[
 \Gamma(\xi,\eta)
 :=\frac{|\xi\times\eta|^2}
 {|\xi|\,|\eta|\,|\xi+\eta|^2}
 =\frac{|\xi|\,|\eta|\sin^2\alpha}{|\xi+\eta|^2},
\tag{AW.16}
\]

AW.16 本来只对三个相关频率都非零定义。为使后面的全格点求和没有
歧义，约定当 \(\xi=0\)、\(\eta=0\) 或 \(\xi+\eta=0\) 时
\(\Gamma(\xi,\eta)=0\)。这是求和记号的延拓；它不把零输出的
\(0/0\) 定义成压力乘子。

并有

\[
 \frac{|(\eta\cdot\widehat h(\xi))
          (\xi\cdot\widehat h(\eta))|}{|\xi+\eta|^2}
 \le\Gamma(\xi,\eta)|\widehat h(\xi)|\,|\widehat h(\eta)|.
\tag{AW.17}
\]

写 \(a=|\xi|,b=|\eta|,c=\cos\alpha\)。由
\(a/b+b/a\ge2\)，

\[
 \frac{|\xi+\eta|^2}{ab}
 =\frac ab+\frac ba+2c
 \ge2+2c\ge1-c^2,
 \qquad 0\le\Gamma(\xi,\eta)\le1.
\tag{AW.18}
\]

这个上界在四种区域给出不同信息。

1. **近同向。** 当 \(\alpha\ll1\) 时，

   \[
    \Gamma(\xi,\eta)
    \sim\frac{ab}{(a+b)^2}\alpha^2;
    \qquad \alpha=0\text{ 时精确为零}.
   \tag{AW.19}
   \]

2. **近反平行低输出。** 写 \(\beta=\pi-\alpha\ll1\)，则

   \[
    \Gamma(\xi,\eta)
    \asymp
    \frac{ab\,\beta^2}{(a-b)^2+ab\,\beta^2}.
   \tag{AW.20}
   \]

   当径向失配不大于角向输出时，右侧可为常数量级。两个收缩中的
   小角度因子会被同样变小的压力输出分母补回，故这里没有统一的
   \(\beta^\gamma\) 增益。精确反平行而 \(a\ne b\) 时分子为零；
   \(a=b\) 时输出为零模并按 AW.4 排除。

3. **一般可比夹角。** 若 \(a\simeq b\)，且夹角远离 \(0,\pi\)，
   则 \(\Gamma\simeq1\)。具体极化或相位仍可能抵消，但无散关系本身
   不再给小参数。

4. **分离输入。** 若 \(a\le b/2\)，则

   \[
    \Gamma(\xi,\eta)
    \le4\frac ab\sin^2\alpha
    \le4\frac ab.
   \tag{AW.21}
   \]

   对 AS 中 \(i<j-2\) 的频带，宽支撑仍给
   \(a/b\le C Q_i/Q_j\)，所以 AW.21 恰好产生 AS.19 的
   \(Q_i/Q_j\) 比率，而不是新的频率幂次。

## 5. 与 AR 的低输出精确例一致

取 AR.14 的

\[
 k=(Q,0,0),\qquad m=(Q,-\ell,0),\qquad
 A=(0,1,0),\qquad B=(\ell,Q,0)/s,\qquad
 s=(Q^2+\ell^2)^{1/2},
\tag{AW.22}
\]

以及 \(v=A\cos(k\cdot x)+B\cos(m\cdot x)\)。对低输出有
\(\xi=k,\eta=-m,\kappa=(0,\ell,0)\)，而

\[
 \Gamma(k,-m)=\frac Qs.
\tag{AW.23}
\]

把两个余弦的 \(1/2\) Fourier 系数以及交换输入所得的两个有序对
都计入 AW.9，得到低输出压力振幅 \(-Q/s\)，正是 AR.15--AR.16。
相反，对高输出对 \(\xi=k,\eta=m\)，有

\[
 \Gamma(k,m)=\frac{Q\ell^2}{s(4Q^2+\ell^2)},
\tag{AW.24}
\]

同样计数后得到 AR.15 的正高输出振幅。因此 AR 的近反平行例正好
饱和 AW.20 的低输出补偿；不能从输入夹角单独提取额外小量。

## 6. 去掉相位后的可求和账本

先在原 \(h\) 系数层定义仍保留方向与输出的绝对账本

\[
 \mathfrak P^{\rm ang}_{K,L}
 :=\sum_{\substack{\xi,\eta\in\mathbb Z^3\\
                    \kappa=\xi+\eta\ne0}}
 |m_{>L}(\kappa)|\,
 \Gamma(\xi,\eta)|\widehat h(\xi)|\,|\widehat h(\eta)|.
\tag{AW.25}
\]

AW.9 与 Fourier 反演立即给

\[
 \|p_h^{>L}\|_\infty\le\mathfrak P^{\rm ang}_{K,L}.
\tag{AW.26}
\]

若不先丢掉测试频率匹配，还可定义工作层账本

\[
 \mathfrak W^{\rm ang}_{\chi,K,L}
 :=V_{\mathbb T}
 \sum_{\substack{\xi,\eta\\\kappa=\xi+\eta\ne0}}
 |m_{>L}(\kappa)|\Gamma(\xi,\eta)
 |\widehat h(\xi)|\,|\widehat h(\eta)|
 |\widehat g_\chi(\kappa)|.
\tag{AW.27}
\]

于是

\[
 |{\cal K}_\chi(p_h^{>L})|
 \le\mathfrak W^{\rm ang}_{\chi,K,L}
 \le\|g_\chi\|_1\mathfrak P^{\rm ang}_{K,L}.
\tag{AW.28}
\]

AW.27 比压力 \(L^\infty\) 估计多保留了原测试输出频率，但已经删除
复相位，故不能再利用 AW.13 中正负模态间的抵消。

现在展开 AS.1 的 \(h=\sum_{j\ge0}v_j\)。先对重叠分解取三角不等式，
再记 \(b_j=Q_j^{3/2}\|v_j\|_2\)。频带内 Fourier 系数的
Cauchy--Schwarz 与格点计数给

\[
 \sum_{\xi\in\operatorname{supp}\widehat v_j}
 |\widehat v_j(\xi)|\le Cb_j.
\tag{AW.29}
\]

若 \(i<j-2\)，AW.21、AS.10 和输出截止给

\[
 \sum_{\substack{\xi\in\operatorname{supp}\widehat v_i,\,
                  \eta\in\operatorname{supp}\widehat v_j}}
 |m_{>L}(\xi+\eta)|\Gamma(\xi,\eta)
 |\widehat v_i(\xi)|\,|\widehat v_j(\eta)|
 \le C\mathbf1_{\{j\ge j_L\}}
       \frac{Q_i}{Q_j}b_i b_j,
\tag{AW.30}
\]

其中 \(j_L\) 与 AS.20 相同；交换输入给同一界。对
\(|i-j|\le2\)，只用 AW.18 及 AS.11 的输出支撑，得到

\[
 \sum_{\substack{\xi\in\operatorname{supp}\widehat v_i,\,
                  \eta\in\operatorname{supp}\widehat v_j}}
 |m_{>L}(\xi+\eta)|\Gamma(\xi,\eta)
 |\widehat v_i(\xi)|\,|\widehat v_j(\eta)|
 \le C\mathbf1_{\{Q_{\max(i,j)}>L/8\}}b_i b_j.
\tag{AW.31}
\]

所以，按 AS.20、AS.26 的定义，

\[
 \boxed{\quad
 \mathfrak P^{\rm ang}_{K,L}
 \le C\left(
 \mathfrak S_{K,L}+\sum_{Q_j>L/32}b_j^2\right)
 =C\mathfrak R_{K,L}\le C\mathfrak C_K.
 \quad}
\tag{AW.32}
\]

这正是 AS.19、AS.24--AS.27 的方向加权细化：分离部分仍是
\((Q_i/Q_j)b_i b_j\)，可比部分在没有额外方向信息时仍是 \(b_i b_j\)。
\(\mathfrak P^{\rm ang}_{K,L}\) 对某些对齐数据可以严格小于
\(\mathfrak R_{K,L}\)，但 AW.23 表明可比低输出并无统一小因子。

## 7. 时间支付仍是原缺口

把 AW.28--AW.32 放回 AS.29，逐时仍只有

\[
 \begin{aligned}
 |{\cal K}_\chi(p_h^{>L})|
 &\le C\mathfrak P^{\rm ang}_{K,L}
   \left(r^{3/4}M^{1/2}D_\chi^{1/2}+r^{-1}M^2\right)\\
 &\le\varepsilon D_\chi
   +C_\varepsilon r^{3/2}M
       (\mathfrak P^{\rm ang}_{K,L})^2
   +Cr^{-1}M^2\mathfrak P^{\rm ang}_{K,L}.
 \end{aligned}
\tag{AW.33}
\]

因此，若只使用 AW.33、且不利用负的 \(D_\chi\) 与压力项之间可能的
带符号耦合，一组充分任务是支付

\[
 \int_{s_J}^{t}\mu_J\mathfrak P^{\rm ang}_{K,L}\,d\sigma,
 \qquad
 \int_{s_J}^{t}\mu_J
       (\mathfrak P^{\rm ang}_{K,L})^2\,d\sigma.
\tag{AW.34}
\]

这两项分别为小量不是实际 NS 的必要条件；它们只是这条粗绝对值路线
的充分条件。
AW.32 只把它们送回 AS.33 的充分成本，并没有由现有能量证明它们
相对终端 \(H_t\) 为小量。若保留 AW.13 的复相位，原则上可能出现
进一步抵消；但目前没有证明 NS 演化给出所需的相位 BV、方向对齐、
坏时间平均抵消，或它们与负的 \(3D_\chi/4\) 之间的定量耦合。
这些动态成本不能免费加入假设。

## 8. 保留测试频率后的半阶配对

AW.27 还保留了 \(g_\chi=\operatorname{div}F_\chi\) 的输出频率；
这比先取压力 \(L^\infty\) 再乘 \(\|g_\chi\|_1\) 更强。定义标量
周期函数

\[
 a_h(x)=\sum_{k\in\mathbb Z^3}|\widehat h(k)|e^{ik\cdot x}.
\tag{AW.35}
\]

因 \(h\) 实值且零均值，\(a_h\) 的 Fourier 系数实、偶、非负，
且 \(\widehat a_h(0)=0\)。Plancherel、\(0\le m_{>K}\le1\) 及
周期 Poincaré 给出

\[
 \|a_h\|_{H^1}=\|h\|_{H^1}
 \le C\|\nabla h\|_2\le Cg,
 \qquad g=\|\nabla u\|_2.
\tag{AW.36}
\]

把 AW.27 中同一输出的压力绝对系数收集为

\[
 Z_L(\kappa)
 :=|m_{>L}(\kappa)|
   \sum_{\xi+\eta=\kappa}
   \Gamma(\xi,\eta)|\widehat h(\xi)|\,|\widehat h(\eta)|
 \quad(\kappa\ne0),\qquad Z_L(0)=0.
\tag{AW.37}
\]

AK.1 给 \(0\le |m_{>L}|\le1\)，而 AW.18 给 \(0\le\Gamma\le1\)。
由于 \(\widehat a_h(k)\ge0\)，逐系数有

\[
 0\le Z_L(\kappa)
 \le \widehat{a_h^2}(\kappa)
 =\sum_{\xi+\eta=\kappa}
      |\widehat h(\xi)|\,|\widehat h(\eta)|.
\tag{AW.38}
\]

令 \({\cal Z}_L(x)=\sum_\kappa Z_L(\kappa)e^{i\kappa\cdot x}\)。
系数对称性使它实值；更重要的是，AW.38 可直接逐项平方，得到

\[
 \|{\cal Z}_L\|_{\dot H^{1/2}}^2
 =V_{\mathbb T}\sum_{\kappa\ne0}|\kappa|Z_L(\kappa)^2
 \le V_{\mathbb T}\sum_{\kappa\ne0}
      |\kappa|\,|\widehat{a_h^2}(\kappa)|^2
 =\|a_h^2\|_{\dot H^{1/2}}^2.
\tag{AW.39}
\]

这里使用的临界嵌入可以不作为额外正则性假设：对任意周期
\(f\in W^{1,3/2}\)，

\[
 \|f\|_{H^{1/2}}
 \le C\bigl(\|f\|_{3/2}+\|\nabla f\|_{3/2}\bigr).
\tag{AW.40}
\]

一个直接证明是先分离平均值，再在非零模上写
\(D^{1/2}f=-\sum_jR_jI_{1/2}\partial_jf\)，使用周期 Riesz 变换的
\(L^{3/2}\) 有界性和周期 HLS
\(I_{1/2}:L^{3/2}\to L^2\)。把它用于 \(f=a_h^2\)，由

\[
 \|a_h^2\|_{3/2}=\|a_h\|_3^2,\qquad
 \|\nabla(a_h^2)\|_{3/2}
 \le2\|a_h\|_6\|\nabla a_h\|_2
\tag{AW.41}
\]

及 AW.36 得
\(\|{\cal Z}_L\|_{\dot H^{1/2}}\le Cg^2\)，常数与 \(K,L\)
无关。严格前奇点光滑区间上 \(a_h\) 本身光滑；同一估计也可由
\(H^1\) 逼近得到，所以这里没有偷用绝对值 Fourier 场的点态正性。

原测试也恰好位于同一个端点空间。映射 \(z\mapsto |z|z\) 是
\(C^1\)，且 \(|\nabla(|u|u)|\le2|u||\nabla u|\)。因此

\[
 \begin{aligned}
 \|F_\chi\|_{W^{1,3/2}}
 &\le C_\chi\bigl(\|u\|_3^2+\|u\|_6g\bigr)\\
 &\le C_\chi(M+g)^2,\qquad
 \|F_\chi\|_{\dot H^{1/2}}\le C_\chi(M+g)^2,
 \end{aligned}
\tag{AW.42}
\]

其中 \(M\) 是同一解的全局 \(L^2\) 上界，第二行使用非齐次周期
Sobolev \(\|u\|_6\le C(M+g)\) 及 AW.40。现在
\(|\widehat g_\chi(\kappa)|
\le|\kappa|\,|\widehat F_\chi(\kappa)|\)，所以加权 Fourier
Cauchy--Schwarz 给出

\[
 \begin{aligned}
 \mathfrak W^{\rm ang}_{\chi,K,L}
 &=V_{\mathbb T}\sum_{\kappa\ne0}
     Z_L(\kappa)|\widehat g_\chi(\kappa)|\\
 &\le\|{\cal Z}_L\|_{\dot H^{1/2}}
       \|F_\chi\|_{\dot H^{1/2}}\\
 &\le C_\chi g^2(M+g)^2
 \le C_\chi(M^2g^2+g^4).
 \end{aligned}
\tag{AW.43}
\]

这是一条独立于 \(K,L\) 和模态排列的瞬时估计。结合 AW.28，在 AQ
同一时间域和同一 \(0\le\mu_J\le1\) 权重下，

\[
 \frac1{H_t}\int_{s_J}^{t}\mu_J
       |{\cal K}_\chi(p_h^{>L})|\,d\sigma
 \le\frac{C_\chi}{H_t}
 \left(M^2A_J+\int_{s_J}^{t}\mu_J g^4\,d\sigma\right),
 \qquad A_J=\int_Jg^2\,d\sigma.
\tag{AW.44}
\]

这比 AW.34 删除了静态半阶频率矩；特别地，不能用压力侧
\(\ell^1\) 账本可能很大来否定原测试的这种配对。但能量只给
\(g^2\in L^1_t\)，没有给窗口内 \(g^4\) 相对 \(H_t\) 的所需控制。
在合法大范数序列上，\(H_t\ge\Lambda_A^3/3\)，而能量绝对连续性给
\(A_J=o(1)\)，所以 AW.44 的第一项已经是 \(o(1)\)；真正未付的是
\(H_t^{-1}\int_{s_J}^t\mu_Jg^4\)。故 AW.44 尚不是 AQ.8 所需的
已付 \(o(H_t)\) 净功上界，也没有完成持留或正则性闭合。

另一个独立的 AX 静态构造正在审查方向加权压力侧绝对账本是否能仅由
能量层控制。AW 不借用尚未完成审计的结论，也不把该静态构造扩大成
原非线性测试、时间窗口或真实 NS 轨道的反例；AW.43 正说明这两个
问题不能混为一谈。

## 9. 结论边界

AW.7--AW.14 给出了此前绝对值账本未显示的精确方向—相位恒等式，
AW.15--AW.24 解释了无散收缩在四种频率几何中的真实强度；所以本稿
并非逐字重复 AS。在本稿 AW.29--AW.32 采用频带三角不等式和
Fourier 系数 Cauchy--Schwarz 的压力侧求和时，结果准确退回 AS 的
\(\mathfrak R_{K,L}\)。保留 AW.27 的测试输出匹配则给 AW.43--AW.44，
但只是把缺口改成窗口内 \(g^4\) 的未付时间成本，仍没有形成新的
AQ.8 上界。AW.27 可能含有进一步的频率匹配，AW.13 还含复相位；
本稿没有证明这些结构产生更强的动态抵消，也不应假定它们有利。

AC 研究的是物理空间速度方向 \(u/|u|\) 与加权纵向应变，不是这里的
Fourier 压力方向；AD 已经负责完整压力功无普适符号的结论；
r075f_modal_phase_integration_identity.md 只处理被动剪切外环带的相位
积分并还原原能量恒等式，不能当作当前全非线性高高压力的 no-go。

本稿只是确定性符号与路线筛查，不宣称新颖性，不证明合法大范数序列
存在，不控制坏时间净工作，不完成固定半径到移动缩球合同 G，也不触及
首次奇点排除或 Clay 正则性结论。无仿真、科学图、提交或发布动作。
