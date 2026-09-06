# 原高高压力功的实际时间有序筛查

2026-09-06。**INTERNAL / PENDING REVIEW / TIME-ORDERED ROUTE SCREEN / G OPEN / NOT CLAY。**

本稿只检查一个有限问题：从 AQ 实际选出的早时刻
\(a=s_J\) 出发，把原高频速度写成真实 NS 的 Duhamel 展开后，
初始—初始、初始—源和源—源三类压力中，是否有一类得到比 AW 更好、
且已由现有能量支付的时间估计。

结论是局部的。精确展开成立；初始—初始项的一部分可由线性热能量支付，
但剩下一个“初始热耗散密度乘实际耗散密度”的时间相关项。AQ 没有给
起点梯度界，也没有支付这个乘积。源项还携带一个真实空间导数；
把三类压力逐项取绝对值只会留下同一相关项与 AW 的 \(g^4\) 成本，
而把三类重新合并则正好回到 AW。故这次筛查没有产生 AQ.8 所需的
新上界，按计划在这里停止，不把它扩大成所有动态机制的 no-go。

## 1. 同一窗口和不能增强的起点信息

沿用 AQ 的同一周期 NS 解、固定空间截止 \(\chi\)、固定环带和
合法大范数窗口：

\[
 \begin{gathered}
 0<a=s_J<t<T_*,\qquad J=(t-\delta,t),\qquad
 \delta=c_0r^2\Lambda_A^{-4},\qquad K=\Lambda_A^{3/4},\\
 H_t=H_\chi(t)\ge\Lambda_A^3/3,\qquad
 \mu_J=w_J\mathbf1_{B_K}\ \hbox{于 }[a,t],\qquad
 0\le\mu_J\le1,\\
 \frac{H_\chi(a)}{H_t}\le\zeta_J,\qquad \zeta_J\to0,\qquad
 A_J=\int_Jg(\sigma)^2\,d\sigma\to0,\qquad
 g(\sigma)=\|\nabla u(\sigma)\|_2 .
 \end{gathered}
\tag{AY.1}
\]

所有极限仍只沿固定 \(M,r,c_0\) 的合法
\(\Lambda_A\to\infty\) 序列讨论，且
\(M=\sup_{0<\sigma<T_*}\|u(\sigma)\|_2\) 固定。AQ.4 只控制
局部三次能量 \(H_\chi(a)\)；它没有给
\(g(a)\)、\(\|\nabla P_{>K}u(a)\|_2\) 或任何临界范数的统一上界。
虽然 \(a<T_*\) 保证这些量对每个单独窗口有限，但不能把这种逐窗口
有限性改写成沿序列的一致成本。本稿不重选 \(a\)，也不改变 AQ.7
定义的权重或 \([a,t]\) 积分域。

## 2. 线性形式下的完整 NS Duhamel 展开

沿用 AK 的实偶平滑低通。写

\[
 m_K(k)=1-\varphi(k/K),\qquad
 \mathbb P_k=I-\frac{k\otimes k}{|k|^2}\quad(k\ne0),
 \qquad m_K(0)=0 .
\tag{AY.2}
\]

令

\[
 h=P_{>K}u,\qquad l=S_Ku,\qquad
 {\cal N}_K=-P_{>K}\mathbb P\operatorname{div}(u\otimes u).
\tag{AY.3}
\]

从原 Leray 方程直接得到

\[
 \partial_\sigma h-\Delta h={\cal N}_K,\qquad
 {\cal N}_K
 =-P_{>K}\mathbb P\operatorname{div}
 \bigl(h\otimes h+h\otimes l+l\otimes h+l\otimes l\bigr).
\tag{AY.4}
\]

这与 AT.5 完全等价，只是把高频自相互作用也放回线性方程右侧。
若展开 \(P_{>K}=I-S_K\)，AY.4 同时包含 AT 的低—低项和
\(S_K\mathbb P\operatorname{div}(u\otimes u)\) 修正；没有把
\(h\) 当成无强迫 NS 解，也没有删去低频、交叉或自相互作用。

对 \(k\ne0\)，源项的准确 Fourier 系数为

\[
 \widehat{{\cal N}_{K,i}}(k,\tau)
 =-m_K(k)
 \left(\delta_{i\ell}-\frac{k_i k_\ell}{|k|^2}\right)
 i k_j\,\widehat{u_\ell u_j}(k,\tau),
 \qquad \widehat{\cal N}_K(0,\tau)=0.
\tag{AY.5}
\]

所以 Leray 原点的取值无关紧要，源的零模由散度和 \(m_K(0)=0\)
同时杀掉。AY.5 中的 \(ik_j\) 是不能丢失的一个空间导数。

记 \(E_\rho=e^{\rho\Delta}\)、\(h_a=h(a)\)，并定义

\[
 h^{(0)}(\sigma)=E_{\sigma-a}h_a,\qquad
 h^{(1)}(\sigma)=\int_a^\sigma
       E_{\sigma-\tau}{\cal N}_K(\tau)\,d\tau .
\tag{AY.6}
\]

则在同一严格前奇点光滑闭区间上，

\[
 h(\sigma)=h^{(0)}(\sigma)+h^{(1)}(\sigma),
\tag{AY.7}
\]

且逐模有

\[
 \begin{aligned}
 \widehat h^{(0)}(k,\sigma)
 &=e^{-|k|^2(\sigma-a)}\widehat h_a(k),\\
 \widehat h^{(1)}(k,\sigma)
 &=\int_a^\sigma e^{-|k|^2(\sigma-\tau)}
              \widehat{\cal N}_K(k,\tau)\,d\tau .
 \end{aligned}
\tag{AY.8}
\]

\(h^{(0)}\) 与 \(h^{(1)}\) 都是实值、零均值、无散场。固定每个模态
时，\(h^{(1)}=O(\sigma-a)\)；但该常数含 AY.5 的导数和源的高频，
不能在频率求和后只用 \(M,A_J\) 统一控制。

## 3. 三类压力和原测试的精确时间核

对张量 \(A\)，仍令零均值 \(\pi[A]\) 满足
\(-\Delta\pi[A]=\partial_i\partial_jA_{ij}\)。定义

\[
 \begin{aligned}
 p^{00}&=\pi[h^{(0)}\otimes h^{(0)}],\\
 p^{01}&=\pi[h^{(0)}\otimes h^{(1)}
                  +h^{(1)}\otimes h^{(0)}],\\
 p^{11}&=\pi[h^{(1)}\otimes h^{(1)}],
 \qquad p_h=p^{00}+p^{01}+p^{11}.
 \end{aligned}
\tag{AY.9}
\]

为避免把 AY.9 中已经合并的交叉项与单个有序输入混淆，另记

\[
 p_{\rm ord}^{\alpha\beta}
 :=\pi[h^{(\alpha)}\otimes h^{(\beta)}].
\]

于是 \(p^{00}=p_{\rm ord}^{00}\)、
\(p^{01}=p_{\rm ord}^{01}+p_{\rm ord}^{10}\)，以及
\(p^{11}=p_{\rm ord}^{11}\)。

写 \(H^{(q)}(k,\sigma)=\widehat h^{(q)}(k,\sigma)\)。
因每个 \(H^{(q)}\) 都无散，对 \(\kappa\ne0\)，任意有序
\(\alpha,\beta\in\{0,1\}\) 满足

\[
 \widehat{\pi[h^{(\alpha)}\otimes h^{(\beta)}]}(\kappa)
 =-\sum_{\xi+\eta=\kappa}
 \frac{(\eta\cdot H^{(\alpha)}(\xi,\sigma))
       (\xi\cdot H^{(\beta)}(\eta,\sigma))}
      {|\kappa|^2}.
\tag{AY.10}
\]

零输出仍按压力 gauge 删除，绝不写成 \(0/0\)。最终测试保持原来的

\[
 F_\chi(\sigma)=\chi|u(\sigma)|u(\sigma),\qquad
 g_\chi(\sigma)=\operatorname{div}F_\chi(\sigma),
\tag{AY.11}
\]

而不是第三个速度模。对单个有序输入，完整配对都是

\[
 {\cal K}_\chi(p_{\rm ord}^{\alpha\beta})(\sigma)
 =-V_{\mathbb T}\operatorname{Re}
 \sum_{\substack{\xi,\eta\\\kappa=\xi+\eta\ne0}}
 \frac{(\eta\cdot H^{(\alpha)}(\xi,\sigma))
       (\xi\cdot H^{(\beta)}(\eta,\sigma))}
      {|\kappa|^2}
 \overline{\widehat g_\chi(\kappa,\sigma)} .
\tag{AY.12}
\]

初始—初始压力的时间核因此精确为

\[
 \widehat p^{00}(\kappa,\sigma)
 =-\sum_{\xi+\eta=\kappa}
 e^{-(|\xi|^2+|\eta|^2)(\sigma-a)}
 \frac{(\eta\cdot\widehat h_a(\xi))
       (\xi\cdot\widehat h_a(\eta))}
      {|\kappa|^2}.
\tag{AY.13}
\]

初始—源的两个有序部分为

\[
 \begin{aligned}
 \widehat p^{01}(\kappa,\sigma)
 =-\sum_{\xi+\eta=\kappa}\frac1{|\kappa|^2}
 \bigg[&
 \int_a^\sigma
 e^{-|\xi|^2(\sigma-a)-|\eta|^2(\sigma-\tau)}
 (\eta\cdot\widehat h_a(\xi))
 (\xi\cdot\widehat{\cal N}_K(\eta,\tau))\,d\tau\\
 &+\int_a^\sigma
 e^{-|\xi|^2(\sigma-\tau)-|\eta|^2(\sigma-a)}
 (\eta\cdot\widehat{\cal N}_K(\xi,\tau))
 (\xi\cdot\widehat h_a(\eta))\,d\tau
 \bigg].
 \end{aligned}
\tag{AY.14}
\]

源—源压力则有双重 Volterra 核

\[
 \begin{aligned}
 \widehat p^{11}(\kappa,\sigma)
 =-\sum_{\xi+\eta=\kappa}\frac1{|\kappa|^2}
 \int_a^\sigma\!\int_a^\sigma&
 e^{-|\xi|^2(\sigma-\tau)-|\eta|^2(\sigma-\rho)}\\
 &\times
 (\eta\cdot\widehat{\cal N}_K(\xi,\tau))
 (\xi\cdot\widehat{\cal N}_K(\eta,\rho))
 \,d\rho\,d\tau .
 \end{aligned}
\tag{AY.15}
\]

AY.12--AY.15 保留了所有相位、压力输出分母、源导数和真实时间顺序。
在光滑闭区间上可先作有限模态截断，再交换频率和与 Volterra 积分。
AQ 中需要审查的原压力部分恰为

\[
 \int_a^t\mu_J(\sigma)
 \bigl[{\cal K}_\chi(p^{00})
       +{\cal K}_\chi(p^{01})
       +{\cal K}_\chi(p^{11})\bigr](\sigma)\,d\sigma .
\tag{AY.16}
\]

没有对一般可测的 \(\mathbf1_{B_K}\) 作时间积分分部，也没有把
\(\mu_J\) 从带符号积分中删掉。逐个固定模态时，AY.14 在起点为
\(O(\sigma-a)\)，AY.15 为 \(O((\sigma-a)^2)\)；下面说明这种
模态级消失并不抵消频率求和中的源导数损失。

## 4. 源项的近对角核

对 \(0<\rho\le1\) 及 \(1<p\le q<\infty\)，周期 Oseen 热核、
\(P_{>K}\) 的统一 \(L^p\) 有界性和 AY.5 给出

\[
 \|E_\rho P_{>K}\mathbb P\operatorname{div}A\|_q
 \le C_{p,q,\varphi}\,
 \rho^{-\frac12-\frac32(\frac1p-\frac1q)}\|A\|_p .
\tag{AY.17}
\]

常数与 \(K\) 无关。散度使零模消失；AY.17 不是把
\(\mathbb P(0)\) 附近的符号冒充为紧支撑光滑乘子。具体地，固定
实偶平滑低通及其高通在 \(1<p<\infty\) 上一致有界，并与热半群、
空间导数和 Leray 投影交换；周期热梯度核的
\(L^p\to L^q\) 范数给出 AY.17 的 \(\rho\) 指数。这里
\(0<\rho\le1\)，周期核的光滑大尺度余项可吸收到同一常数中。
能量层只有

\[
 \|u\otimes u\|_{3/2}=\|u\|_3^2
 \le CM(M+g),\qquad
 \|u\otimes u\|_3=\|u\|_6^2
 \le C(M+g)^2 .
\tag{AY.18}
\]

例如，\((p,q)=(3/2,3)\) 在 AY.17 中给近对角核
\(\rho^{-1}\)，不能逐时绝对积分；\((3/2,2)\) 给
\(\rho^{-3/4}\)。若为得到 \(H^1\) 再加一个输出导数，后一核变成
\(\rho^{-5/4}\)，同样不能由 \(M,A_J\) 作逐时绝对卷积。
改用 \((p,q)=(3,3)\) 可把核降为 \(\rho^{-1/2}\)，但源成本是
\((M+g)^2\)，只在时间上 \(L^1\)。Fubini 至少给出真实的积分界

\[
 \int_a^t\|h^{(1)}(\sigma)\|_3\,d\sigma
 \le C\delta^{1/2}
       \int_a^t(M+g(\tau))^2\,d\tau
 \le C\delta^{1/2}(M^2\delta+A_J).
\tag{AY.19}
\]

AY.19 支付了源生成尾的一个 \(L^1_tL^3_x\) 量，却不足以和
\(g_\chi\) 或 AW 的半阶测试配成压力功。若要求
\(h^{(1)}\) 的逐时 \(H^1\)，AY.17 的额外导数正好重新产生
非可积的近对角核；不能只写热衰减而删去 AY.5。

## 5. 初始—初始项：可支付部分与精确剩余

令 \(\rho=\sigma-a\)，并记

\[
 G_a(\rho)=\|\nabla E_\rho h_a\|_2 .
\tag{AY.20}
\]

因 \(h_a\) 零均值、无散且 \(\|h_a\|_2\le M\)，线性热能量给

\[
 \int_0^{t-a}G_a(\rho)^2\,d\rho
 =\frac12\bigl(\|h_a\|_2^2
              -\|E_{t-a}h_a\|_2^2\bigr)
 \le\frac12M^2,
\qquad
 G_a(\rho)^2\le\frac{C M^2}{\rho}\quad(\rho>0).
\tag{AY.21}
\]

对 \(h^{(0)}\) 重复 AW.35--AW.43 的半阶配对，测试仍是实际
\(F_\chi(\sigma)\)，得到

\[
 |{\cal K}_\chi(p^{00})(a+\rho)|
 \le C_\chi G_a(\rho)^2
       \bigl(M+g(a+\rho)\bigr)^2 .
\tag{AY.22}
\]

所以，不作任何时间分部积分，仅用 \(0\le\mu_J\le1\)，有

\[
 \begin{aligned}
 \int_a^t\mu_J|{\cal K}_\chi(p^{00})|\,d\sigma
 &\le C_\chi M^4+C_\chi{\cal C}_{00},\\
 {\cal C}_{00}
 &:=\int_0^{t-a}\mu_J(a+\rho)
       G_a(\rho)^2g(a+\rho)^2\,d\rho .
 \end{aligned}
\tag{AY.23}
\]

这里 \(M^4\) 来自 \(M^2\int G_a^2\)，故除以
\(H_t\to\infty\) 后已经趋零。真正剩余的是
\({\cal C}_{00}\)。热收缩还给任意
\(0<\varepsilon<t-a\)

\[
 {\cal C}_{00}
 \le \|\nabla h_a\|_2^2
      \int_0^\varepsilon\mu_J(a+\rho)g(a+\rho)^2\,d\rho
   +\frac{CM^2}{\varepsilon}A_J .
\tag{AY.24}
\]

AQ.1 只给 \(A_J=o(1)\)，没有它相对 \(\varepsilon\) 的速率；
AQ.4 也没有给 \(\|\nabla h_a\|_2\le g(a)\) 的统一上界。因此，
仅凭这里列出的量，AY.24 没有给出一个沿合法序列统一且已支付的
\(\varepsilon\) 选择。等价地，AY.21 的粗界只会把剩余送到
\(CM^2\int_0^{t-a}\mu_Jg(a+\rho)^2\,d\rho/\rho\)，而
\(g^2\in L^1_t\) 不控制这一带起点奇权积分。

试图利用
\(G_a^2=-\frac12\partial_\rho\|E_\rho h_a\|_2^2\)
对 \({\cal C}_{00}\) 作时间分部积分也不可行：它会要求
\(\partial_\rho(\mu_Jg^2)\)，而 AV 已经说明
\(\mathbf1_{B_K}\) 没有已知 BV 控制，能量也不给
\(\partial_tg^2\) 的预算。

## 6. 输出热衰减和 AR 的对照

对初始—初始的高压力输出，令 \(Z_{00,L}(\kappa,\rho)\) 为
AW.37 的方向绝对系数，但把两个 \(h\) 换成
\(E_\rho h_a\)。当 \(m_{>L}(\kappa)\ne0\) 时
\(|\kappa|>L\)，而

\[
 |\xi|^2+|\eta|^2\ge\frac12|\xi+\eta|^2>\frac12L^2 .
\tag{AY.25}
\]

把 AY.13 的热指数分成两个相等部分，再使用 AW.39--AW.43，得到

\[
 \|{\cal Z}_{00,L}(\rho)\|_{\dot H^{1/2}}
 \le C e^{-L^2\rho/4}G_a(\rho/2)^2,
\qquad
 |{\cal K}_\chi((p^{00})^{>L})(a+\rho)|
 \le C_\chi e^{-L^2\rho/4}G_a(\rho/2)^2
              (M+g(a+\rho))^2 .
\tag{AY.26}
\]

热能量只给

\[
 \int_0^{t-a}e^{-L^2\rho/4}G_a(\rho/2)^2\,d\rho
 \le M^2.
\tag{AY.27}
\]

它没有从这条估计自动产生 \(L^{-2}\)：高频初始能量可以在
\(\rho\ll L^{-2}\) 的初始层中耗散。更重要的是，AY.26 中与
\(g^2\) 相乘的部分仍是 AY.23 的加指数版本，指数在
\(\rho=0\) 等于一，现有能量仍不控制其时间相关。

低压力输出可以独立使用 AR 的有限格点预算。由
\(\|E_\rho h_a\|_2\le M\)，

\[
 \frac1{H_t}\int_a^t\mu_J
 |{\cal K}_\chi((p^{00})^{\le L})|\,d\sigma
 \le \frac{CM^4\delta L^4}{H_t}
 \le Cc_0M^4r^2L^4\Lambda_A^{-7}.
\tag{AY.28}
\]

另一条梯度预算为

\[
 \frac1{H_t}\int_a^t\mu_J
 |{\cal K}_\chi((p^{00})^{\le L})|\,d\sigma
 \le\frac{CM^2L^2}{H_t}\int_0^{t-a}G_a(\rho)^2\,d\rho
 \le\frac{CM^4L^2}{H_t}.
\tag{AY.29}
\]

AY.28 在 \(L=o(\Lambda_A^{7/4})\) 时可支付；这正是 AR.7，
不是新的时间增益。在扩散输出
\(L\simeq\delta^{-1/2}\simeq\Lambda_A^2\) 上，
AY.28--AY.29 都留下 \(O(\Lambda_A)\) 的上界。对完整实际
\(p_h^{\le L}\)，AR.21 使用 \(\int_Jg^2=A_J\) 得到较好的
\(A_J\Lambda_A\)，但能量仍只给 \(A_J=o(1)\)。所以把压力改写成
初始热项没有修复 AR 的扩散频率缺口，逐项拆分反而更粗。

## 7. 初始—源和源—源项为何回到旧成本

AW 的半阶论证有一个双线性版本：对任意实值、零均值、无散
\(v,w\in H^1(\mathbb T^3)\)，

\[
 |{\cal K}_\chi(\pi[v\otimes w+w\otimes v])|
 \le C_\chi\|v\|_{H^1}\|w\|_{H^1}(M+g)^2 .
\tag{AY.30}
\]

证明仍是把 \(|\widehat v(k)|\)、\(|\widehat w(k)|\) 作为两个
标量 Fourier 系数，使用
\(\|a_va_w\|_{H^{1/2}}
\le C\|a_v\|_{H^1}\|a_w\|_{H^1}\)，再与
\(F_\chi\in H^{1/2}\) 配对；这是一条充分绝对值估计，不使用相位。

在每个光滑窗口内，AY.7 给

\[
 \|h^{(0)}(a+\rho)\|_{H^1}\le CG_a(\rho),\qquad
 \|h^{(1)}(a+\rho)\|_{H^1}
 \le C\bigl(g(a+\rho)+G_a(\rho)\bigr).
\tag{AY.31}
\]

所以对三类压力分别使用 AY.22、AY.30 并作三角不等式，只会得到

\[
 \begin{aligned}
 |{\cal K}_\chi(p^{00})|
 +|{\cal K}_\chi(p^{01})|
 +|{\cal K}_\chi(p^{11})|
 \le C_\chi\{&
 M^2(G_a^2+g^2)\\
 &+G_a^2g^2+g^4\}.
 \end{aligned}
\tag{AY.32}
\]

这里交叉幂次已用 Young 吸收到右侧四项。时间积分后，前两项分别由
\(M^4\) 与 \(M^2A_J\) 支付；后两项正是
\({\cal C}_{00}\) 与 AW 的 \(\int\mu_Jg^4\) 缺口。

若不把 AY.9 的三类压力分开，而是先用
\(h=h^{(0)}+h^{(1)}\) 精确重组，则
\(\|h\|_{H^1}\le Cg\)，AW.43 直接给

\[
 |{\cal K}_\chi(p_h)|
 \le C_\chi(M^2g^2+g^4).
\tag{AY.33}
\]

这比 AY.32 少了人为引入的 \({\cal C}_{00}\)。因此当前绝对值
Duhamel 分拆没有改善 AW；它破坏了 \(h^{(0)}\) 与 \(h^{(1)}\)
在实际高频场中的可能抵消。AY.14--AY.15 的保相位 Volterra 公式
仍可能包含尚未利用的动态抵消，但本稿没有为它证明一个可支付估计。

## 8. 停止结论和边界

AY.6--AY.16 是同一 NS 解、同一 \(a=s_J\)、同一 \(K\) 与
同一 \([a,t]\) 权重下的精确时间有序展开。AY.19 是源生成尾的一条
已付 \(L^1_tL^3_x\) 估计；AY.23 支付了初始—初始项的 \(M^4\)
部分；AY.26 保留了高输出热指数。但这些事实均未控制
\({\cal C}_{00}\)，源项的 \(H^1\) 近对角成本也没有被能量支付。

沿当前绝对值路线，三类分别估计只得到 AY.32；重组则得到原来的
AY.33。负的 \(3D_\chi/4\) 没有在本稿中用于更细的带符号耦合，
所以这里列出的时间成本都只是充分路线，不是 NS 必要条件。
同样，精确 Duhamel 恒等式本身不是新上界。

本稿不排除 AY.14--AY.15 的相位、Volterra 顺序或负耗散之间存在
另一种真实耦合；它只说明本次半群绝对值估计没有提供该耦合。没有
证明合法大范数序列存在，没有闭合 AQ.8、固定球到移动缩球合同 G、
首次奇点或 Clay 正则性，也不宣称新颖性。本稿无仿真、科学图、
提交或发布动作。
