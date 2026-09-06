# 按速度模长投影压力：正交恒等式与条件延拓预检

2026-09-06。**PROVED LOCALLY / CONDITIONAL / LITERATURE-RELATED / NOT CLAY。**

设 \(u\) 是 \(\mathbb T^3=(-\pi,\pi]^3\) 上的光滑周期无散场，
\[
 q=|u|,\qquad e=\frac{u}{q}\quad(q>0),\qquad
 F=-e\cdot\nabla q\quad(q>0).
\tag{AF.1}
\]
在 \(\{q=0\}\) 上把 \(F\) 定义为零。以下投影论证不除以 \(q\)，
因此可以跨过速度零集；它与需要 \(q^{-1}\) 的方向演化方程不同。
压力采用周期零均值规范，满足
\(-\Delta p=\partial_i\partial_j(u_i u_j)\)。

## 1. 所有速度模长函数都与 \(F\) 正交

由 \(u=qe\)，在 \(q>0\) 上有
\[
 qF=-u\cdot\nabla q.
\tag{AF.2}
\]
这个等式在零集上也以两侧均取零的方式成立。并且
\[
 |F|\le|\nabla q|\le|\nabla u|
\quad\hbox{a.e.},
\tag{AF.3}
\]
所以在光滑周期情形中 \(F\) 是有界可测函数。

先令 \(\Phi:[0,\|q\|_\infty]\to\mathbb R\) 为有界 Borel 函数，并取
\[
 \Gamma(s)=\int_0^s\Phi(r)\,dr .
\]
\(\Gamma\) 是 Lipschitz 函数。令 N 为 \(\Gamma\) 不可微或
\(\Gamma'\ne\Phi\) 的零测标量集，包含所选 Borel 代表在零测集上的改值。
由 Lipschitz q 的 coarea 公式，
\(\int_{q^{-1}(N)}|\nabla q|\,dx=0\)，所以其原像上 \(\nabla q=0\) a.e.。
结合 Sobolev 链式法则，得到
\(\nabla\Gamma(q)=\Phi(q)\nabla q\) a.e.。
周期性与 \(\operatorname{div}u=0\) 因而给出
\[
 \boxed{
 \int_{\mathbb T^3}q\,\Phi(q)F\,dx
 =-\int_{\mathbb T^3}u\cdot\nabla\Gamma(q)\,dx=0.}
\tag{AF.4}
\]
若 \(\Phi\) 只是 Borel 函数，但
\[
 \int q\,|\Phi(q)F|\,dx<\infty,
\tag{AF.5}
\]
则对 \(\Phi\) 作有界截断并用支配收敛，AF.4 仍成立。
特别地，AF.4 对所有
\(\Phi(q)\in L^2(q\,dx)\) 成立，因为 \(F\in L^2(q\,dx)\)。

## 2. 条件期望投影与最小压力残差

固定一个 \(u\not\equiv0\) 的时刻，定义有限测度
\[
 d\mu=q(x)\,dx,\qquad M=\mu(\mathbb T^3)=\int q\,dx>0.
\tag{AF.6}
\]
可等价地用概率测度 \(M^{-1}\mu\) 定义条件期望。
在 Hilbert 空间 \(L^2(\mu)\) 中令
\[
 {\mathcal S}_q=L^2(\sigma(q),\mu)
 =\overline{\{\Phi(q):\Phi\ \hbox{有界 Borel}\}},
\tag{AF.7}
\]
并记正交投影为
\[
 {\mathsf P}_q p
 =\mathbb E_\mu[p\mid\sigma(q)].
\tag{AF.8}
\]
由 Doob--Dynkin 表示，存在 Borel 函数
\(\bar p\)，使 \({\mathsf P}_qp=\bar p(q)\) \(\mu\)-a.e.。
当前每个光滑时刻 p 有界；条件期望的 L∞ 收缩给
\(|{\mathsf P}_qp|\le\|p\|_\infty\) \(\mu\)-a.e.。
将推前测度零集上的 \(\bar p\) 改为零，可选在整个速率区间都有界的
Borel 版本。这是逐时结论，不提供临近候选奇点的统一压力上界。
AF.4 正是
\[
 F\perp{\mathcal S}_q,\qquad {\mathsf P}_qF=0
\quad\hbox{in }L^2(\mu).
\tag{AF.9}
\]

全环面 \(L^3\) 压力功为
\[
 W=\int p\,u\cdot\nabla q\,dx=-\int q\,pF\,dx.
\]
由 AF.9，
\[
 \boxed{
 W=-\int q\,(p-{\mathsf P}_qp)F\,dx.}
\tag{AF.10}
\]
所以压力中仅依赖速度模长 \(q\) 的部分对 \(W\) 完全不可见。

相应的最小残差定义为
\[
 \boxed{
 \begin{aligned}
 {\mathcal R}^2
 &:=\inf_{\substack{\Phi\ {\rm Borel}\\
                    \Phi(q)\in L^2(\mu)}}
     \int q\,|p-\Phi(q)|^2\,dx\\
 &=\int q\,|p-{\mathsf P}_qp|^2\,dx.
 \end{aligned}}
\tag{AF.11}
\]
第二个等号是 Hilbert 投影定理。它是给定 \(q\) 后压力条件方差的
未归一化加权积分，而不是压力总范数或单个归一化方差。特别地，
\({\mathcal R}=0\) 当且仅当 \(p\) 在 \(\mu\)-a.e. 意义下是
\(q\) 的 Borel 函数，此时 \(W=0\)。

该定义与压力 gauge 无关。若 \(p\) 改为 \(p+c(t)\)，则
\[
 {\mathsf P}_q(p+c)={\mathsf P}_qp+c,\qquad
 p+c-{\mathsf P}_q(p+c)=p-{\mathsf P}_qp,
\tag{AF.12}
\]
且常数压力对 AF.10 的贡献也因 AF.4 为零。

## 3. 零集、平台与时间可测性

1. 在 \(\{q=0\}\) 上，测度 \(q\,dx\) 为零，投影代表元的取值无关紧要；
   把 \(F\) 取零与 AF.2--AF.4 相容。
2. 若 \(q=c>0\) 的水平平台有正体积，则
   \(\nabla q=0\)、\(F=0\) a.e. 于该平台。
   推前测度 \(q_\#\mu\) 在 \(c\) 处有原子，条件期望在这个原子上
   就是相应的加权平均，不需要用可能退化的等值面面积公式。
   不同连通分支若具有同一 \(q\) 值，会被 \(\sigma(q)\) 有意合并。
3. 若 \(u\equiv0\)，则 \(q\,dx\) 是零测度，归一化条件期望没有定义。
   此时零均值压力也为零；约定
   \({\mathsf P}_qp=0\)、\({\mathcal R}=W=0\)，单独结束该情形。

对时间积分，还需避免逐时任选投影代表元造成的可测性空缺。
若 \(u,p\) 在紧时间区间上联合光滑，令
\({\mathscr P}_{\mathbb Q}\) 为有理系数多项式的可数集合。连续函数在
任意有限 Borel 推前测度的 \(L^2\) 中稠密，而有理多项式在紧区间上一致
稠密，因此
\[
 {\mathcal R}^2(t)
 =\inf_{\phi\in{\mathscr P}_{\mathbb Q}}
   \int q(t,x)|p(t,x)-\phi(q(t,x))|^2\,dx .
\tag{AF.13}
\]
右侧是可数个连续时间函数的下确界，所以
\({\mathcal R}^2(t)\) 是 Borel 可测的。若确需联合代表元，也可在测度
\(q(t,x)\,dt\,dx\) 下对 \((t,q)\) 取条件期望；标准析取给出
\(\bar p(t,q)\)，它在 a.e. 时间上恢复逐时投影。后面的延拓论证只使用
AF.13 的残差值，不依赖代表元的联合选择。

## 4. 残差条件给出的周期延拓判据

现在令 \(u\) 是黏性 \(\nu=1\)、无外力周期 NS 的光滑解，并记
\[
 H(t)=\frac13\int q^3\,dx,\qquad
 D(t)=\int\left(q|\nabla u|^2+q|\nabla q|^2\right)dx.
\tag{AF.14}
\]
标准全环面恒等式为
\[
 H'(t)+D(t)=W(t).
\tag{AF.15}
\]
由 AF.3、AF.10 和 Cauchy--Schwarz，
\[
 \begin{aligned}
 |W|
 &\le {\mathcal R}\left(\int qF^2\,dx\right)^{1/2}\\
 &\le {\mathcal R}\,D^{1/2}
 \le \eta D+\frac1{4\eta}{\mathcal R}^2
 \qquad(\eta>0).
 \end{aligned}
\tag{AF.16}
\]
取 \(\eta=1/2\)，得到
\[
 H'+\frac12D\le\frac12{\mathcal R}^2.
\tag{AF.17}
\]

设 \(u\) 是定义在 \([0,T_*)\) 上的最大光滑周期解，\(T_*<\infty\)。
固定 \(s<T_*\)。若 \(H(s)=0\)，则 \(u(s)=0\)，唯一性给出其后为零解，
故可以延拓。其余情形在解未变成零之前令
\[
 a(t)=\frac{{\mathcal R}^2(t)}{H(t)}.
\]
考虑额外假设
\[
 \boxed{\int_s^{T_*}\frac{{\mathcal R}^2(t)}{H(t)}\,dt<\infty.}
\tag{AF.18}
\]
约定 \(H=0\) 时该商为零；若光滑解在区间内到达零状态，
唯一性已给出其后零解延拓，不再需要下面的非零分支估计。
由 AF.17 丢弃 \(D\) 并应用 Gronwall，
\[
 H(t)\le H(s)
 \exp\left(\frac12\int_s^t a(\tau)\,d\tau\right),
 \qquad s\le t<T_*.
\tag{AF.19}
\]
所以 \(H\) 一致有界，继而
\[
 \int_s^{T_*}{\mathcal R}^2\,dt
 =\int_s^{T_*}aH\,dt<\infty.
\]
再积分 AF.17，得到
\[
 \int_s^{T_*}D(t)\,dt<\infty.
\tag{AF.20}
\]

对 \(q^{3/2}\) 使用周期 Sobolev 不等式，
\[
 \begin{aligned}
 \|u(t)\|_9^3
 &=\|q^{3/2}\|_6^2\\
 &\le C\left(\|\nabla(q^{3/2})\|_2^2
             +\|q^{3/2}\|_2^2\right)
 \le C\bigl(D(t)+H(t)\bigr).
 \end{aligned}
\tag{AF.21}
\]
AF.19--AF.21 因而给
\[
 u\in L^3\bigl((s,T_*);L^9(\mathbb T^3)\bigr).
\tag{AF.22}
\]
这满足非端点 Serrin 关系
\[
 \frac2{3}+\frac3{9}=1,\qquad 9>3.
\]
可以直接沿用 AC.12 的周期 H¹ 估计，令 \(Y=\|\nabla u\|_2^2\)，则
\(Y'/2+\|\Delta u\|_2^2/2\le C\|u\|_9^3Y\)。
AF.22 与 Gronwall 给一致 H¹ 上界，再调用 AC 中已核验适用范围的
标准周期次临界局部存在共同寿命，即可延拓越过 \(T_*\)。
因此 AF.18 是一个充分的周期延拓条件。
这与非端点 Serrin 路径一致；背景局部存在理论并未在这里重新证明。

## 5. 不能越过的边界

1. 当前尚未证明 AF.18 可由基本能量推出。上面的投影恒等式本身
   不提供 \(\int q|p-{\mathsf P}_qp|^2\) 除以 H 后的时间积分估计。
   不将这个未闭合状态写成所有真实 NS 轨道上该条件均不可能的结论。
2. \({\mathsf P}_q\) 随解和时间改变，是一个解析正交投影；
   它本身不提供局部 cutoff、尺度小性或可计算的首次奇点几何。
3. AF.18 的延拓证明只说明该额外条件足够，不能反过来声称一般
   Leray--Hopf 解已满足它，也没有完成成熟时间持留或原合同 G。
4. 已定位直接相关的压力 moderator 文献，见本包 literature-boundary：
   Tran–Yu 的 Lemma 1 已包含速率函数抵消；后续相关性准则采用压力平方
   与速率的混合积分。AF 是周期、Borel/平台与投影形式的本地核查，
   不把恒等式或条件准则作为新的正则性机制，也不声称投影形式首创。
   本稿纳入 PressureQuotient 科学冻结，独立审查范围见本包 audit；
   **NOT CLAY**。单次移交以 dispatch receipt 为准，不在此记录发布状态。
