# 有真实热滞后的旧压力成分可以支付

2026-09-06。**INTERNAL / PENDING REVIEW / CONDITIONAL REDUCTION / G OPEN / NOT CLAY。**

AY、AZ 从压力积分域内的起点展开，未支付纯热项与实际速度的相关
成本。我在这里把 Duhamel 起点放到 J 以前，给热分量一段真实滞后。
原 AQ 的早时低值点、测试、坏集和积分因子全部保留。结果是含旧热
分量的压力可以由任意固定的小份额耗散和 o(H_t) 余项支付；这只把
必要净工作转到近期非线性源的自压力，仍不给其上界。

## 1. 两个起点不混用

在原三维周期域、黏性 1 上，取合同 G 的同一最大光滑解
u 于 [0,T_*)，并保留 AO–AQ 的固定环带与固定空间截止。记

\[
 \begin{gathered}
 \Lambda=\Lambda_A=\|u(t)\|_{L^3(B_r)},\quad
 \delta=c_0r^2\Lambda^{-4},\quad J=(t-\delta,t)\subset I,\quad
 K=\Lambda^{3/4},\\
 M=\sup_{0<s<T_*}\|u(s)\|_2>0,\quad
 g(s)=\|\nabla u(s)\|_2,\quad A_J=\int_Jg^2,\quad
 L(s)=\|u(s)\|_3,\quad H_t=H_\chi(t)\ge\Lambda^3/3.
 \end{gathered}
\tag{BA.1}
\]

所有极限只沿固定数据的合法 \(\Lambda\to\infty\) 序列。成熟条件
为 \(t-\delta\ge c_mr^2>0\)，原 AQ 点 \(s_J\in J\) 及原
\(\mu_J=w_J\mathbf1_{B_K}\) 始终只在 \([s_J,t]\) 使用。
定义另一个、只服务于热展开的起点

\[
 \tau_J=\Lambda^{-1},\qquad
 a_J=t-\delta-\tau_J,\qquad
 h=P_{>K}u.
\tag{BA.2}
\]

充分大时 \(\tau_J<c_mr^2/2\)、\(\tau_J+\delta\le1\)，所以
\(0<a_J<s_J<t<T_*\)。整个 \([a_J,t]\) 都属于原解的光滑存在域。
不要求 a_J 是局部能量低值点，不要求其梯度小，也不需要在 J 外
额外假定环带高阶导数界；新增热估计只使用全局 M。

## 2. 真实源积分与高通热界

令 \(E_\rho=e^{\rho\Delta}\)、\(\mathbb P\) 为周期 Leray 投影。
原方程在每个严格前奇点闭区间上给出

\[
 \begin{aligned}
 b_J(s)&=E_{s-a_J}P_{>K}u(a_J),\\
 R_J(s)&=-\int_{a_J}^{s}E_{s-v}P_{>K}\mathbb P
                     \operatorname{div}(u\otimes u)(v)\,dv,\\
 h(s)&=b_J(s)+R_J(s).
 \end{aligned}
\tag{BA.3}
\]

K 在整段展开内固定。源项仍含低频、交叉和高频自相互作用；R_J 不是
无强迫 NS 解。两个分量均实值、零均值、无散；零模由高通及散度
消失，不需要给 Leray 零模赋予奇异表达式。BA.3 是原 AY 的同一
Leray 公式，但不能把 a_J 改名成其原来的 s_J。

采用 \(V=(2\pi)^3\)、\(\widehat f(k)=V^{-1}\int f e^{-ikx}\)。
高通符号 \(m_K=1-\varphi(k/K)\) 满足 \(0\le m_K\le1\)，并在
\(|k|\le K\) 为零。对 \(0<\rho\le1\)，Fourier Cauchy–Schwarz 给

\[
 \begin{aligned}
 \|E_\rho P_{>K}u(a_J)\|_\infty
 &\le \sum_{|k|>K}e^{-\rho|k|^2}|\widehat u(a_J,k)|\\
 &\le C M\left(\sum_{|k|>K}e^{-2\rho|k|^2}\right)^{1/2}\\
 &\le C M e^{-K^2\rho/2}
                \left(\sum_{k\in\mathbb Z^3}e^{-\rho|k|^2}\right)^{1/2}
 \le C M\rho^{-3/4}e^{-K^2\rho/2}.
 \end{aligned}
\tag{BA.4}
\]

格点和的界由三个一维 Gaussian 和的乘积得到：每个一维和至多
\(1+C\rho^{-1/2}\)。没有把平滑高通假作幂等锐投影。
在 J 上 \(\rho=s-a_J\ge\tau_J\)，故

\[
 \mathfrak b_J:=\sup_{s\in J}\|b_J(s)\|_\infty
 \le C M\tau_J^{-3/4}e^{-K^2\tau_J/2}
 =C M\Lambda^{3/4}e^{-\Lambda^{1/2}/2}\longrightarrow0.
\tag{BA.5}
\]

这是有滞后的真实上界，不可用于 AY 的 \(s-a=0\) 层。压力功仍从
s_J 开始，BA.5 没有扩大其时间积分域。

## 3. 含旧分量的完整压力

写 \(T_{ij}=\partial_i\partial_j(-\Delta)^{-1}\)，统一取零均值压力。
二次展开精确给出

\[
 \begin{aligned}
 p_h&=p_{RR}+p_{\rm old},\\
 p_{RR}&=T_{ij}(R_{J,i}R_{J,j}),\\
 p_{\rm old}
 &=T_{ij}(b_{J,i}b_{J,j}+b_{J,i}R_{J,j}+R_{J,i}b_{J,j})\\
 &=T_{ij}(b_{J,i}h_j+h_i b_{J,j}-b_{J,i}b_{J,j}).
 \end{aligned}
\tag{BA.6}
\]

所有压力输出，包括高高产生的低输出，都留在这条恒等式里。
平滑低通的周期核有统一 L1 范数，高通因而在 L3 一致有界，故
\(\|h\|_3\le C_\varphi L\)。周期双 Riesz 只在有限 L3 上使用，得到

\[
 \|p_{\rm old}(s)\|_3
 \le C\mathfrak b_J\bigl(L(s)+\mathfrak b_J\bigr).
\tag{BA.7}
\]

这里的固定体积因子已计入 C，没有使用 Riesz 的 L infinity 端点。
BA.7 只估计含旧热分量的压力，不能以同一式子估计 p_RR。

## 4. 原非线性测试及耗散份额

沿用 AB 的原权重

\[
 q=|u|,\quad F_\chi=\chi q u,\quad
 D_\chi=\int\chi q(|\nabla u|^2+|\nabla q|^2),\quad
 g_\chi=\operatorname{div}F_\chi
       =\chi u\cdot\nabla q+q u\cdot\nabla\chi.
\tag{BA.8}
\]

u 无散。零集沿 AB 的约定处理；也可先取 q_epsilon 并支配收敛。
在主项中保留原 chi 权重，空间 Hölder 给出

\[
 \begin{aligned}
 \|\chi u\cdot\nabla q\|_{3/2}
 &\le\|(\chi q)^{1/2}\nabla q\|_2
        \|(\chi q)^{1/2}\|_6
 \le D_\chi^{1/2}L^{1/2},\\
 \|q u\cdot\nabla\chi\|_{3/2}&\le C_\chi L^2.
 \end{aligned}
\tag{BA.9}
\]

因为 \(\int\chi^3q^3\le\int q^3=L^3\)，第一行没有扩大耗散区域。
完整压力配对仍为 \({\cal K}_\chi(p)=\int p g_\chi\)，因此

\[
 |{\cal K}_\chi(p_{\rm old})|
 \le C\mathfrak b_J(L+\mathfrak b_J)L^{1/2}D_\chi^{1/2}
     +C_\chi\mathfrak b_J(L+\mathfrak b_J)L^2.
\tag{BA.10}
\]

对任意固定 \(0<\epsilon<3/4\)，一次 Young 不等式给出完整余项

\[
 \begin{aligned}
 |{\cal K}_\chi(p_{\rm old})|
 \le\epsilon D_\chi+C_{\epsilon,\chi}\bigl(
  \mathfrak b_J^2L^3+\mathfrak b_J^3L^2+
  \mathfrak b_J^4L+\mathfrak b_J L^3+\mathfrak b_J^2L^2\bigr).
 \end{aligned}
\tag{BA.11}
\]

BA.11 对任意有限 \(\mathfrak b_J\) 成立；本稿的 BA.5 另保证最终
\(\mathfrak b_J\le1\)。用 \(L+L^2\le C(1+L^3)\)，即有

\[
 |{\cal K}_\chi(p_{\rm old})|
 \le\epsilon D_\chi+\mathcal E_J(s),\qquad
 \mathcal E_J(s)=C_{\epsilon,\chi}\mathfrak b_J(1+L(s)^3).
\tag{BA.12}
\]

耗散份额 epsilon 是真实成本。BA.12 不证明旧压力功本身为 o(H_t)，
也不能在处理 p_RR 时再次使用同一份耗散。

## 5. 只用原解能量支付余项

非齐次周期 Sobolev 与 L2–L6 插值给
\(L^3\le C[M^{3/2}g^{3/2}+M^3]\)。因此

\[
 \int_J L(s)^3\,ds
 \le C\left(M^{3/2}\delta^{1/4}A_J^{3/4}+M^3\delta\right).
\tag{BA.13}
\]

这是能量时间积分，不假定 \(g^4\) 可积。对原 \(0\le\mu_J\le1\)，
\([s_J,t]\subset J\) 给

\[
 \begin{aligned}
 \frac1{H_t}\int_{s_J}^t\mu_J\mathcal E_J
 &\le\frac{C_{\epsilon,\chi}\mathfrak b_J}{H_t}
       [(1+M^3)\delta+M^{3/2}\delta^{1/4}A_J^{3/4}]\\
 &\le C_{\epsilon,\chi,M,r,c_0}\mathfrak b_J
       [\Lambda^{-7}+\Lambda^{-4}A_J^{3/4}]
 \longrightarrow0.
 \end{aligned}
\tag{BA.14}
\]

无需给 A_J=o(1) 增加任何多项式速率。

## 6. 必要净工作转到近期源自压力

定义

\[
 \beta_K={\cal K}_\chi(p_h)-\tfrac34D_\chi,\qquad
 \gamma_{J,\epsilon}
 ={\cal K}_\chi(p_{RR})-(\tfrac34-\epsilon)D_\chi.
\tag{BA.15}
\]

由 BA.6 与 BA.12，逐时有

\[
 \beta_K\le\gamma_{J,\epsilon}+\mathcal E_J.
\tag{BA.16}
\]

乘以原非负 mu_J，从原 s_J 到 t 积分，再用 AQ.8 与 BA.14，得到

\[
 \boxed{\qquad
 \liminf_{\Lambda\to\infty}\frac1{H_t}
 \int_{s_J}^{t}\mu_J(s)
 \left[{\cal K}_\chi(p_{RR})(s)
       -(\tfrac34-\epsilon)D_\chi(s)\right]ds\ge1.
 \qquad}
\tag{BA.17}
\]

结论对任意预先固定的 \(\epsilon\in(0,3/4)\) 成立，不以窗口变化的
epsilon 获得未经检验的常数。区间内的 R_J 来自 a_J 之后、长度至多
\(\tau_J+\delta\to0\) 的真实 NS 源积分；它不因此变小。

## 7. 与旧结果的关系和范围

本稿与 AM 都把某类压力用一份原耗散和可支付余项移走。AM 使用
低高频分离及无散梯度增益；这里对热分量使用实际时间滞后与有限 L3
有界背景估计。二者是不同分解，但这里没有声称超出已知方法的新颖性。
BA.9 是原测试的加权 Hölder，不依赖 AW 的 g^4 路线。

AY、AZ 的起点没有整段真实滞后，本稿不否认其已记录的具体成本；
反过来，它们也不能作为 BA 的不可能性论证。是否还能缩短 tau_J，
以及是否必须令热分量的 L infinity 趋零，都需要保留 BA.11 的完整
成本后另行判断，不能从这一充分证明宣称必要性或最优性。

BA.17 仍是条件于同一合法大范数序列存在的必要下界。原源积分含
完整非线性和导数，源—源压力功的上界仍 OPEN。没有证明奇点存在或
不存在，没有建立移动缩球合同 G，没有一般正则性或 Clay 结论。
暂无仿真、科学图、DGX、新读者 PDF、外部同行评审或发布动作。
