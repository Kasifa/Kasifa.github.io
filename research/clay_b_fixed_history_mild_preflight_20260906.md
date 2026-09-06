# 固定初值的完整历史：非线性贡献不能随初值一起删去

2026-09-06。**PROVED CONDITIONAL HISTORY ACCOUNTING / G OPEN / NOT CLAY。**

我检查 BH 未保留的完整固定初值历史。本节不假定一般古老解
分类，也不证明常向量极限确实由某个奇点产生。问题是：如果真正
的峰值序列局部趋于一个非零常向量，完整 mild 公式要求什么？

答案是：固定初值的线性项消失，但在任何固定归一化过去窗口以外，
非线性项必须保留这个常向量。基本能量只能在随峰值增长的过去
窗口上支付尾项，不能交换两个极限。

## 1. 同一固定解与全部缩放量

按 G 合约使用黏性 1、周期尺度 1；
\(\mathbb T_L^3=(\mathbb R/(2\pi L\mathbb Z))^3\)。空间范数
均使用未归一化测度。取一个固定光滑周期无散初值 \(u_0\)，
设其最大光滑解的首次候选末端为 \(0<T_*<\infty\)。这是反证
场景，不是奇点存在结论。压力取逐时零均值周期代表。

选择过去 record 峰值 \(M_k=\|u(t_k)\|_\infty\to\infty\)、
\(t_k\to T_*\)，并在周期胞取 \(|u(x_k,t_k)|=M_k\)。记

\[
 \begin{split}
 v_k(y,s)&=M_k^{-1}u(x_k+y/M_k,t_k+s/M_k^2),\\
 \pi_k(y,s)&=M_k^{-2}p(x_k+y/M_k,t_k+s/M_k^2),\\
 L_k&=M_k,\qquad b_k=M_k^2t_k,\qquad
 E_0=\|u_0\|_2^2 .
 \end{split}
\tag{BI.1}
\]

每项满足相同的无外力 NS 方程，且

\[
 |v_k(0,0)|=1,\qquad
 \sup_{-b_k\le s\le0}\|v_k(s)\|_\infty\le1,\qquad
 \sup_s\|v_k(s)\|_2^2\le M_kE_0.
\tag{BI.2}
\]

均值和完整左端初值保持精确对应：

\[
 \fint_{\mathbb T_{M_k}^3}v_k(s)=M_k^{-1}\fint_{\mathbb T^3}u_0,
 \quad
 \|v_k(-b_k)\|_\infty=M_k^{-1}\|u_0\|_\infty,
 \quad b_k/L_k^2=t_k\to T_*.
\tag{BI.3}
\]

周期能量等式还给

\[
 M_k^{-1}\int_{-b_k}^0\!\int_{\mathbb T_{M_k}^3}|\nabla v_k|^2
 =\int_0^{t_k}\!\int_{\mathbb T^3}|\nabla u|^2\le E_0/2.
\tag{BI.4}
\]

完整耗散除以 \(M_k\) 不必趋零。对任何固定 \(S>0\)，
相应最近窗口除以 \(M_k\) 的耗散则趋零，因为它对应原时间中
趋近 \(T_*\) 的长度 \(S/M_k^2\) 窗口，且原总耗散可积。
这不提供未归一化的固定球局部耗散小性。

## 2. 保留投影和周期副本的核

记 \(\Gamma(x,t)\) 为全空间热核，\(\mathcal K_{iab}(x,t)\)
为 \(e^{t\Delta}\mathbb P\partial_b\) 的核，其 Fourier 乘子为

\[
 \widehat{\mathcal K}_{iab}(\xi,t)
 =i\xi_b\left(\delta_{ia}-\frac{\xi_i\xi_a}{|\xi|^2}\right)
                e^{-t|\xi|^2},\qquad \widehat{\mathcal K}(0,t)=0.
\tag{BI.5}
\]

KNSS 原文第 3 节给出同一 Stokes 表示与
\(|\mathcal K(x,t)|\le C(|x|^2+t)^{-2}\)。也可由
\(\Gamma\) 和 \(\int_t^\infty\Gamma(\cdot,r)dr\) 的一阶及
三阶空间导数得到该界。特别地

\[
 \|\mathcal K(\cdot,t)\|_1\le Ct^{-1/2},\qquad
 \int_{\mathbb R^3}\mathcal K(x,t)dx=0 .
\tag{BI.6}
\]

后一等式来自 BI.5 在零频的连续取值，或直接对可积导数积分。
这不是把 \(\mathbb P\) 本身视为 \(L^\infty\) 有界算子。

逐项周期化为

\[
 \Gamma_L(x,t)=\sum_{m\in\mathbb Z^3}\Gamma(x+2\pi Lm,t),\quad
 \mathcal K_L(x,t)=\sum_{m\in\mathbb Z^3}
                         \mathcal K(x+2\pi Lm,t).
\tag{BI.7}
\]

当 \(t>0\) 时，\(\mathcal K\) 的四次空间衰减使后一和绝对
收敛。积分展开给 Fourier 系数等于 BI.5 在 \(\xi=m/L\) 的值
除以胞体积，零模为零。这正是周期
\(e^{t\Delta_L}\mathbb P_L\operatorname{div}\)，包含全投影、
压力作用及所有周期副本，没有外加力或自由的压力线性项。

展开胞积分与取绝对值给一致估计

\[
 \|\mathcal K_L(t)\|_{L^1(\mathbb T_L)}\le Ct^{-1/2},\qquad
 \int_{\mathbb T_L}\mathcal K_L(t)=0,
 \quad \Gamma_L\ge0,\quad\int_{\mathbb T_L}\Gamma_L=1 .
\tag{BI.8}
\]

另有对所有 \(L\ge1,t>0\) 的充分粗界

\[
 \|\mathcal K_L(t)\|_\infty\le C(t^{-2}+L^{-4}).
\tag{BI.9}
\]

证明：取胞代表 \(x\in[-\pi L,\pi L]^3\)。零副本至多
\(Ct^{-2}\)；非零副本的距离至少 \(cL|m|\)，故其和至多
\(CL^{-4}\sum_{m\ne0}|m|^{-4}\)。该和在三维收敛。
这是粗界，不把大时间真实的额外抵消或指数衰减排除在外。

由于 BI.6，周期数据的全空间卷积可通过胞分解准确写成 BI.7。
因此光滑周期解的提升是全空间 bounded mild 解；这里给出了
该转接，而不是仅把全空间定理的结论换一个域名。

## 3. 终点与紧性接口

BI.8 给双线性项在 \([0,\delta]\) 上的界

\[
 \|B_L(f,g)\|_{L^\infty_{x,t}}\le
 C\sqrt\delta\,\|f\|_{L^\infty_{x,t}}\|g\|_{L^\infty_{x,t}}.
\tag{BI.10}
\]

标准压缩映射给一个与 \(L\ge1\) 无关的 \(\delta_0>0\)：
从速度不超过 1 的数据出发，在 \([0,\delta_0]\) 上有统一
小于 2 的速度界。取稍小闭区间 \([0,\delta_0/2]\) 留出余量。
光滑解与此 mild 解局部一致，所以 record 缩放的终点有这个
统一正向光滑邻域。不能只从剩余寿命长度推断其上速度有界。

使用 KNSS Proposition 4.1、Lemma 4.1 与 Lemma 6.1 的局部
平滑／紧性接口，可取子列使周期提升局部光滑收敛，包括 \(s=0\)。
这些标准平滑接口并未在本节从零重证明。以下只考察其中一种
尚未排除的情形：

\[
 v_k\longrightarrow c\quad\text{局部一致地于}
 \mathbb R^3\times(-\infty,0],\qquad c\text{ 为常向量},\quad |c|=1.
\tag{BI.11}
\]

本节没有证明 BI.11 必然发生，也没有把它升级为实际奇点例子。

## 4. 完整 mild 公式的三项

记 \(F_k=v_k\otimes v_k\)，对固定 \(S>0\) 和充分大的 \(k\)
（\(b_k>S\)），在终点写

\[
 v_k(\cdot,0)=H_k+N_{k,\mathrm{old}}^S+N_{k,\mathrm{recent}}^S,
\tag{BI.12}
\]

其中全部卷积在 \(\mathbb T_{M_k}\) 上，

\[
 \begin{split}
 H_k&=e^{b_k\Delta_{M_k}}v_k(-b_k),\\
 N_{k,\mathrm{old}}^S
   &=-\int_{-b_k}^{-S}\mathcal K_{M_k}(-s)*F_k(s)ds,\\
 N_{k,\mathrm{recent}}^S
   &=-\int_{-S}^{0}\mathcal K_{M_k}(-s)*F_k(s)ds.
 \end{split}
\tag{BI.13}
\]

不把它们换成绝对值后相等的标量项。热核正性支付

\[
 \|H_k\|_\infty\le M_k^{-1}\|u_0\|_\infty\longrightarrow0.
\tag{BI.14}
\]

在 BI.11 的条件下，每个固定 \(S\) 还有

\[
 N_{k,\mathrm{recent}}^S\longrightarrow0
       \quad\text{局部一致地于空间}.
\tag{BI.15}
\]

证明要保留非局部核。用周期提升，把卷积写在 \(\mathbb R^3\)，
并因核积分为零而减去 \(c\otimes c\)。在最近 \(\varepsilon\)
时间内，BI.6 与 \(|v_k|\le1\) 给一致 \(C\sqrt\varepsilon\)
界。在 \(\varepsilon\le-s\le S\) 内先切掉远空间尾巴；
\(|\mathcal K(x,t)|\le C(|x|^2+t)^{-2}\) 给此尾巴对固定空间
紧集一致趋零。剩余紧时空区域用 BI.11 的一致收敛。依次取
\(k\to\infty\)、空间截断半径趋于无穷、\(\varepsilon\downarrow0\)
得到 BI.15。没有在整个扩张胞上假定一致趋于常量。

因此完整公式反而要求

\[
 N_{k,\mathrm{old}}^S\longrightarrow c\quad
      \text{局部一致地，对每个固定 }S>0.
\tag{BI.16}
\]

特别是 \(\lim_{S\to\infty}\lim_{k\to\infty}
N_{k,\mathrm{old}}^S(y)=c\)。遥远左端初值趋零，不等于遥远
过去的非线性项在这个极限次序下趋零。

## 5. 能量能支付多远的过去

不要求 BI.11，仅用 BI.2、BI.9 与 \(\|F_k(s)\|_1\le M_kE_0\)，
可得

\[
 \begin{split}
 \|N_{k,\mathrm{old}}^S\|_\infty
 &\le CE_0M_k\int_S^{b_k}(r^{-2}+M_k^{-4})dr\\
 &\le CE_0\left(\frac{M_k}{S}+\frac{t_k}{M_k}\right),
 \qquad 0<S<b_k .
 \end{split}
\tag{BI.17}
\]

对固定 \(S\)，这个上界不趋零，也不证明真实尾项必大。
但是对任意固定 \(0<\eta<1\)，可以选随峰值增长的窗口

\[
 S_k=M_k^{1+\eta},\qquad
 S_k/b_k\longrightarrow0,\qquad
 \|N_{k,\mathrm{old}}^{S_k}\|_\infty
 \le CE_0(M_k^{-\eta}+T_*/M_k)\longrightarrow0 .
\tag{BI.18}
\]

这是一项真实的、由同一解全局能量支付的尾估计。但它没有使
\([-S_k,0]\) 上的非线性贡献消失。由 BI.12 反而有

\[
 \|v_k(0)-N_{k,\mathrm{recent}}^{S_k}\|_\infty\longrightarrow0,
 \qquad S_k/M_k^2=M_k^{-1+\eta}\longrightarrow0 .
\tag{BI.19}
\]

因此一个原时间中趋零、但归一化时间中趋于无穷的窗口可以承载
全部终点速度。BI.15 只适用于固定 \(S\)，不能套到 \(S_k\)。

若另有 BI.11，那么对每个固定 \(S\)，两条已证极限合起来给

\[
 -\int_{-S_k}^{-S}\mathcal K_{M_k}(-s)*F_k(s)ds
       \longrightarrow c\quad\text{局部一致地}.
\tag{BI.20}
\]

这只是常向量极限情形下的必要来源描述，不证明该情形存在，也不
证明其不可能。不把中间时间段的真实有符号贡献称为正测度。

## 6. 此次检查的出口

固定初值与完整 mild 历史确实比 BH 多带来信息，且 BI.18 支付了
一个增长过去窗口的尾部。但它们没有支付排常量所需的固定窗口
之后的统一尾小性；在假设常量极限的分支中，BI.16 恰要求保留
非零贡献。把相反结论命名为“历史紧性条件”不会证明它。

倍增时刻的独立检查见配套 BJ 笔记。两个检查都必须与一般古老解
刚性分开：排除常向量仍不排除非恒定的三维有界古老解。
本节不关闭 G、Q、净压力功或 Clay 问题，也不作新颖性声明。

原文核验：KNSS 作者预印本 SHA
`5d86444c4c34bcad3642b2087a69b98d265f6da0e366bd50621d4ce792abc9f2`。
本轮重读 PDF 页 6–13、18–20；完整覆盖第 3–4 节及本节采用的
第 6 节提取段。页 7、10、11、19 已视觉检查。作者 PDF 在线
重开超时，但本地原件哈希未变，arXiv 版本条目已重新核验。
[原始版本条目](https://arxiv.org/abs/0709.3599)。没有完整重审外部
平滑依赖或重新开展全面古老解文献检索。无仿真、图、DGX 或
新读者 PDF。
