# R0.72F 独立逐式复核

**日期：** 2026-08-27

**复核对象：** R0.72F critical-log initial-layer repair

**结论：** 解析指数账本闭合；两条有限精度数值路线相符。当前结果仍只是 selected-root obstruction 的筛选定理，不是 complete-root 上界，不是区间算术证明，也不是 Navier--Stokes 千禧年问题的解答。

## 1. 文件与复核口径

我逐式检查了下列三个文件：

- 解析主稿：`/Users/kasifa/Documents/Math/navier-stokes-r072f/research/r072f_report-source.md`
- producer 结果：`/Users/kasifa/Documents/Math/navier-stokes-r072f/research/certificates/r072f/result.json`
- independent 结果：`/Users/kasifa/Documents/Math/navier-stokes-r072f/research/certificates/r072f/independent-result.json`

producer 使用时变 Strang split-step Fourier 演化，并以分段线性 integrand 的精确权重矩积分。independent 路线没有读取 producer 输出，使用实不变格点上的自适应隐式 BDF，并在 (x=e^{-z}) 后作 Gauss--Legendre 积分和解析尾项。两个 JSON 都报告 `allRequiredChecksPassed: true`。

这里的“通过”有严格边界。解析上下界来自主稿中的不等式推导。JSON 只在
(delta=16,32,64,128,256,512) 上给出浮点数佐证。两个程序都明确写出
`intervalArithmetic: false`、`completeRootUpperBound: false` 和
`provesNSERegularity: false`。因此，数值一致性不能替代解析证明，也不能把 selected roots 的结论提升为 complete roots 的结论。

我发现两处需要在阅读时保留限定：

1. 式 (6.5) 的推导使用 (0<\beta<1)。第 7 节的 explicit-coupling 点和第 8 节的 root-weight 点位于 (\beta=0) 边界，它们分别由式 (7.2) 和式 (8.3) 独立支持。三顶点是一个代数边界汇总，不是由同一条 (0<\beta<1) 定理统一推出。
2. 式 (7.2) 的写法需要 (\theta\ge0)。若允许 (\theta<0)，则 (1+\Gamma^\theta\asymp1)，不能把分母写成 (\delta^\theta)。候选修复本来只使用非负增长指数，但这个定义域应显式保留。

除这两处范围限定外，我没有在主稿的指数运算、对数次数或 Leray payment 中发现矛盾。

## 2. 定义、尺度与主结论逐式复核

### 2.1 式 (0.1)--(0.10)

| 式号 | 复核 | 结论与边界 |
|---|---|---|
| (0.1) | 这是 R0.72E 已否定的旧候选，不是本节重新声称的定理。 | 定位正确。 |
| (0.2) | (Y=\|\omega\|_2^2\)，(L=\mathbb P(u\times\omega))。 | 后续所有商和作用量均与这一定义一致。 |
| (0.3) | (w_{\beta,\gamma}(s)=s^{-\beta}[1+\log(1/s)]^\gamma)。 | 对固定有限 (\gamma\ge0)，(w\in L^2(0,1)) 当且仅当 (\beta<1/2)。 |
| (0.4) | 时间变量换元 (s=(t-a)/T) 后，(T^{-1}dt=ds)。 | 作用量是无量纲的；在 (Y=0) 处取零与 mean-zero 条件相容。 |
| (0.5) | (\Lambda_{1,\beta,\gamma}=\mathcal R_Y(\nu^2+\mathscr A_{\beta,\gamma}))。 | 与后续分母一致；它没有消除 inherited (D) 的非齐次尺度。 |
| (0.6) | 用 (\mathcal J_{\rm sel}\asymp\delta)、(D^{1/3}\asymp\delta^{2/3}) 和 (\mathscr A\asymp\delta^\beta(\log\delta)^{\gamma-1}) 相除。 | 得到 (\delta^{1/3-\beta}(\log\delta)^{1-\gamma})，指数正确。只适用于 (0<\beta<1)。 |
| (0.7) | Lemma 2.1、归一化时间上的 Cauchy--Schwarz 和 (2\nu\int Y\le\|u(a)\|_2^2) 依次给出该式。 | 常数和 (T^{-1/2}\) 次数正确；要求 admissible restart time。 |
| (0.8) | selected obstruction 要求 (\beta>1/3)，或 (\beta=1/3,\gamma\ge1)；Leray payment 要求 (\beta<1/2)。 | 交集写法正确，但“admissible”只指这两个有限筛选。 |
| (0.9) | 令 (a=1/3)，用 (\int_0^1s^{a-1}\log^n(1/s)ds=n!/a^{n+1})。 | (3+2\cdot9+54=75)，临界权重的平方可积性正确。 |
| (0.10) | 这是待证的 complete-root 候选。 | 主稿已用问号标出，没有把它写成结论。 |

### 2.2 式 (1.1)--(1.6)：尺度与精确类

| 式号 | 复核 | 结论与边界 |
|---|---|---|
| (1.1) | 在 whole-space scaling 下，(\omega_\lambda=\lambda^2\omega(\lambda x,\lambda^2t))。 | (Y\) 的平方范数尺度是 (\lambda)。 |
| (1.1) 后的 Lamb 尺度 | (u\times\omega) 的振幅尺度为 (\lambda^3)，三维 (\dot H^{-1}) 平方范数的尺度为 (\lambda^{6-3-2}=\lambda)。 | 分子、分母同阶，式 (0.4) 中的商不变。 |
| fixed-torus covering | 对整数覆盖，(Y\) 与 (\|L\|_{\dot H^{-1}}^2) 均按 (\lambda^4) 缩放；同时 (T\mapsto T/\lambda^2)。 | 加权平均仍不变。 |
| inherited (D) | whole-space 下 (\|u_0\|_2^2\mapsto\lambda^{-1}\)，(\|\omega_0\|_2^2\mapsto\lambda)。 | 主稿正确指出整个候选不是 whole-space scale-covariant。 |
| (1.2) | (u=(f,0,v))，其中 (f=f(y,z,t))、(v=v(y,t))。 | (\nabla\cdot u=0)，且非线性只在第一分量留下 (vf_z)；这是精确三角类。 |
| (1.3)--(1.5) | 代入 (x=q_0^2t) 后，扩散给出 (-(r^2+q_0^{-2})F_r)，剪切耦合给出 (-i\delta e^{-x}(F_{r-1}+F_{r+1}))。 | (D_\mu,V,F_x=D_\mu F+\delta VF) 的符号和参数一致。 |
| (1.6) | (\delta=R^4)、(P=q_0^2\delta)、(S^2=\delta/\log(2+\delta))。 | 后续 (R=\delta^{1/4}) 与所有对数换算一致。 |

这一精确类中的每个成员都是光滑全局解。它只能用来检验候选不等式，不能构造奇性。

## 3. Leray payment 与能量端点

### 3.1 式 (2.1)--(2.5)

| 式号 | 复核 | 结论 |
|---|---|---|
| (2.1) | (\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}\lesssim\|u\times\omega\|_{6/5}\)。 | Leray 投影在 (\dot H^{-1}) 上有界。 |
| (2.2) | Hölder 给 (\|u\times\omega\|_{6/5}\le\|u\|_3\|\omega\|_2)；插值给 (\|u\|_3\lesssim\|u\|_2^{1/2}\|\omega\|_2^{1/2})。 | 平方后除以 (Y=\|\omega\|_2^2)，恰得 (\lesssim\|u\|_2\|\omega\|_2)。 |
| (2.3) | 用 (\|u(t)\|_2\le\|u(a)\|_2) 代入定义。 | 没有丢失 (T^{-1})。 |
| (2.4) | (T^{-1}\int wY^{1/2}\le\|w\|_{L^2(0,1)}(T^{-1}\int Y)^{1/2})。 | 再用能量不等式得到 (\|u(a)\|_2^2/\sqrt{2\nu T})，次数正确。 |
| (2.5) | 三个矩分别是 (3,18,54)。 | 总和 (75)，与两条数值路线一致。 |

这个 payment 只支付 (\mathscr A)。它没有支付 (\mathcal R_Y)，也没有证明从加权作用量到 complete root measure 的采样不等式。

### 3.2 式 (2.6)--(2.7)：energy-only endpoint sharpness

对 (\beta>1/2)，可取
(2(1-\beta)\le p<1)。于是
(Y(t)=t^{-p}\in L^1)，但
(t^{-\beta}Y^{1/2}=t^{-\beta-p/2}\notin L^1)。在
(\beta=1/2) 时，

\[
Y(t)=\frac1{t\log^2(e/t)}\in L^1,
\qquad
t^{-1/2}Y(t)^{1/2}=\frac1{t\log(e/t)}\notin L^1.
\]

两项判断都正确。它们只是标量 (L^1_t) 预算的反例，不是 Navier--Stokes 解的 enstrophy 轨道，更不是奇性构造。(\gamma\ge0) 的对数权只会使端点更强，因此不会挽救 (\beta=1/2)。

## 4. Theorem 3.1 的上下界

### 4.1 式 (3.1)--(3.7)

| 式号 | 复核 | 结论与边界 |
|---|---|---|
| (3.1) | (A_q=q_0^{-2}-\partial_\theta^2) 在第 (r) 模上的特征值是 (q_0^{-2}+r^2>0)。 | (A_q^{-1}) 范数定义良好。 |
| (3.2) | 目标次数为 (\delta^{\beta-1}(\log\delta)^\gamma)。 | 对固定 (0<\beta<1)、有限 (\gamma\ge0) 正确；常数不在端点一致。 |
| (3.3) | 这是从 R0.72E 继承的关键点态上界。 | R0.72F 的上界依赖这项已证输入，JSON 不重新证明它。 |
| (3.4)，初始段 | (\int_0^{1/\delta}x^{-\beta}[1+\log(X/x)]^\gamma dx\asymp\delta^{\beta-1}(\log\delta)^\gamma)。 | 需要 (\beta<1)，次数正确。 |
| (3.4)，尾段 | (\delta^{-1}\int_{1/\delta}^{X}x^{-1-\beta}[1+\log(X/x)]^\gamma dx\) 由左端控制。 | 对固定 (\beta>0) 也是同一次数。 |
| (3.5) | (F_0\in\mathrm{Dom}(D_\mu))，半群收缩，(V) 有界；mild equation 给 (O(x)+O(\delta x))。 | 在 (x\le c/\delta) 上可统一控制。 |
| (3.6) | (V(0)F_0\ne0)，而 (A_q^{-1}) 在该固定有限模向量上严格正。 | 取固定小 (c) 后得到与 (\delta) 无关的正下界。 |
| (3.7) | 只积分 (x\in[c/(2\delta),c/\delta])。区间长度为 (O(\delta^{-1}))，权重为 (O(\delta^\beta(\log\delta)^\gamma))。 | 下界与上界同阶。 |

因此，Theorem 3.1 的核心不是数值拟合，而是“初始层非退化 + R0.72E 点态衰减”的夹逼。该证明给出通常意义下的解析常数存在性，不给出机器可核验的有理区间常数。

### 4.2 式 (3.8)--(3.9)：(\beta=0) 的非一致端点

在 (\beta=0) 时，尾段变成

\[
\delta^{-1}\int_{1/\delta}^{X}x^{-1}[1+\log(X/x)]^\gamma dx
=O\!\left(\delta^{-1}(\log\delta)^{\gamma+1}\right).
\]

所以式 (3.9) 正确，并且不能把 Theorem 3.1 的常数直接令
(\beta\downarrow0)。乘上
(S_R^2\asymp\delta_R/\log\delta_R) 后，
(\mathscr A_{0,\gamma}=O((\log\delta_R)^\gamma))。这足以给 selected ratio 的发散下界，但没有给 (Q_{0,\gamma}) 的两侧等价。

## 5. selected roots、临界对数与 complete-root 边界

### 5.1 式 (4.1)--(4.6)

| 式号 | 复核 | 结论与边界 |
|---|---|---|
| (4.1) | (D_R\asymp\delta_R^2)，(\mathcal R_Y\asymp1)。 | 这是 R0.72E 继承输入。 |
| (4.2) | (S_R^2Q\asymp(\delta/\log\delta)\delta^{\beta-1}(\log\delta)^\gamma)。 | 得到 (\delta^\beta(\log\delta)^{\gamma-1})，正确。 |
| (4.3) | 前 (R) 个已选择根满足 (t_k\asymp k/\delta)、斜率质量 (\asymp k^{-1})。 | 这是 selected Bessel neighborhoods 的双侧输入，不是所有根的枚举。 |
| (4.4) | (\sum_{k\le R}k^{-1}\asymp\log R=(1/4)\log\delta)。 | 与 (S_R^2\asymp\delta/\log\delta) 相乘后为 (\asymp\delta)。 |
| (4.5) | 分母为 (\delta^{2/3}\cdot\delta^{1/3}/\log\delta=\delta/\log\delta)。 | selected ratio 为 (\asymp\log\delta\)，所以原 complete-root 上界必然失败。 |
| (4.6) | critical-log 时作用量为 (\asymp\delta^{1/3})，分母为 (\asymp\delta)。 | selected ratio 只达到 (\asymp1)，既不发散也不趋零。 |

式 (4.5) 能否定 complete-root 候选，是因为 selected 正根测度是 complete 正根测度的非负子测度。式 (4.6) 的逻辑方向不同：一个子测度有界不能控制其余根。因此，critical-log 只通过了已知 obstruction；它没有证明式 (0.10)。

### 5.2 式 (5.1)--(5.4)：固定 launch frequency 的盲区

式 (5.2) 中的 shear 项为 (2P_R^2q_0^{2s})，active 项为
(2S_R^2(q_0^2+1)^s)。由于
(S_R^2/P_R^2=O((\delta_R\log\delta_R)^{-1}))，分子和分母都由固定频率 (q_0) 的 shear 主导，故
(\kappa_s\to q_0^s)。有限个 moment 上局部有界的
(\Psi) 仍为 (O(1))。这四式的极限运算正确。

该结论只排除有限个、振幅归一化、launch-time 的空间频率矩。它不排除无限维频率包络、正时间信息或振幅敏感数据项。

## 6. free-amplitude frontier

### 6.1 式 (6.1)--(6.5)

令 (X_\delta=S_\delta^2)。在 (X_\delta=O(\delta)) 内，active enstrophy 是
(O(X_\delta\delta^{2/3})=o(\delta^2))，所以 shear 仍控制 (D\asymp\delta^2)。对 (0<\beta<1)，

\[
\mathcal J_{{\rm sel},0}\asymp X_\delta\log\delta,
\qquad
\mathscr A_{\beta,\gamma}
\asymp X_\delta\delta^{\beta-1}(\log\delta)^\gamma.
\]

选择式 (6.3)
(X_\delta=\delta^{1-\beta}(\log\delta)^{-\gamma}) 后，作用量为
(O(1))，而 selected ledger 为
(\delta^{1-\beta}(\log\delta)^{1-\gamma})。再除以
(\mathfrak C_\delta^a\Gamma_\delta^c\asymp\delta^{2a+c})，得到式 (6.4)。

于是，不发散的必要条件确为

\[
2a+c+\beta>1,
\quad\text{或}\quad
2a+c+\beta=1\ \text{且}\ \gamma\ge1.
\]

这是 no-go frontier。它只给必要条件，不给 complete-root 充分条件。把作用量取固定高次幂也不会改变这个必要多项式边界，因为式 (6.3) 可以先把作用量固定在常数量级。

### 6.2 三个边界顶点

producer JSON 对下列有理数做了精确算术检查：

| 顶点 | (a) | (c) | (\beta) | (\alpha) | (\gamma) | (2a+c+\beta) | 加上 (3\alpha/4) | 正确解释 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| critical-log action | (1/3) | (0) | (1/3) | (0) | (1) | (1) | (1) | 式 (6.5) 的真实端点，selected obstruction 饱和。 |
| explicit coupling | (1/3) | (1/3) | (0) | (0) | (1) | (1) | (1) | (\beta=0) 边界点；实际必要性由式 (7.2) 独立给出。 |
| root weight | (1/3) | (0) | (0) | (4/9) | (1) | (2/3) | (1) | 属于式 (8.4)，并且改变了被控制的 root ledger。 |

JSON 的 `frontier_vertices_exact` 只证明这些分数加法等于声明值。它不是 PDE 证明。后两个点也不能被表述为 Theorem 3.1 在 (\beta=0) 的直接推论。

### 6.3 式 (7.1)--(7.3)

归一化几何下 (\Gamma=P/q_0^2=\delta)。对 (\theta\ge0)，旧 selected ratio
(\gtrsim\delta^{1/3}) 再除以 (1+\delta^\theta\)，得到
(\gtrsim\delta^{1/3-\theta})。因此 (\theta<1/3) 失败。

又因 (D\asymp\delta^2)，

\[
D^{1/3}\Gamma^{1/3}
\asymp\delta^{2/3}\delta^{1/3}
=\delta
\asymp D^{1/2}.
\]

式 (7.3) 正确，但只在该精确族上等价。(\Gamma) 仍是 target-specific 参数，不是一般速度场的内禀泛函。

### 6.4 式 (8.1)--(8.4)

由 (t_k\asymp k/\delta)、(J_k\asymp S_R^2/k) 和
(R=\delta^{1/4})，对固定 (\alpha>0)，

\[
\sum_{k\le R}(k/\delta)^\alpha\frac{S_R^2}{k}
\asymp S_R^2\delta^{-\alpha}R^\alpha
\asymp\frac{\delta^{1-3\alpha/4}}{\log\delta}.
\]

所以式 (8.2) 和 (8.3) 的阈值 (\alpha=4/9) 正确。这里的常数在
(\alpha\downarrow0) 时不一致，不能把该式直接延拓到 (\alpha=0)。

在 free-amplitude 选择下，加权 ledger 的多项式次数再减少
(3\alpha/4)，故式 (8.4)

\[
2a+c+\beta+3\alpha/4\ge1
\]

是正确的必要多项式条件。等号时剩余因子是
((\log\delta)^{-\gamma})，对已经声明的 (\gamma\ge0) 不发散。这个修复改变了目标测度，不能视为原始 raw ledger 的证明。

## 7. 两条数值路线的直接差异

下表使用

\[
\mathrm{reldiff}
=\frac{|Q_{\rm producer}-Q_{\rm independent}|}
{|Q_{\rm independent}|}.
\]

| (\delta) | (\beta=1/4) | plain (1/3) | critical-log | (\beta=2/5) | (\beta=49/100) | 本行最大值 |
|---:|---:|---:|---:|---:|---:|---:|
| 16 | (1.6343\times10^{-4}) | (2.4752\times10^{-4}) | (4.7585\times10^{-4}) | (3.2164\times10^{-4}) | (4.2548\times10^{-4}) | (4.7585\times10^{-4}) |
| 32 | (1.6388\times10^{-4}) | (2.4440\times10^{-4}) | (4.4879\times10^{-4}) | (3.1708\times10^{-4}) | (4.2154\times10^{-4}) | (4.4879\times10^{-4}) |
| 64 | (1.5083\times10^{-4}) | (2.2837\times10^{-4}) | (4.1098\times10^{-4}) | (2.9978\times10^{-4}) | (4.0459\times10^{-4}) | (4.1098\times10^{-4}) |
| 128 | (1.3831\times10^{-4}) | (2.1333\times10^{-4}) | (3.7693\times10^{-4}) | (2.8359\times10^{-4}) | (3.8845\times10^{-4}) | (3.8845\times10^{-4}) |
| 256 | (1.2835\times10^{-4}) | (2.0135\times10^{-4}) | (3.4887\times10^{-4}) | (2.7066\times10^{-4}) | (3.7551\times10^{-4}) | (3.7551\times10^{-4}) |
| 512 | (1.2059\times10^{-4}) | (1.9203\times10^{-4}) | (3.2610\times10^{-4}) | (2.6066\times10^{-4}) | (3.6555\times10^{-4}) | (3.6555\times10^{-4}) |

全表最大双路差异是 (4.7585\times10^{-4})，即约 (0.0476\%\)，出现在
(\delta=16) 的 critical-log action。到 (\delta=512) 时，五个 producer/independent 数值分别为：

| 权重 | producer (Q) | independent (Q) |
|---|---:|---:|
| (\beta=1/4) | 0.3681634829 | 0.3682078868 |
| plain (1/3) | 0.6040628825 | 0.6041789052 |
| critical-log | 4.3079371007 | 4.3093423696 |
| (\beta=2/5) | 0.9192246906 | 0.9194643538 |
| (\beta=49/100) | 1.6847706130 | 1.6853867133 |

producer 数值在这组比较中系统性略低，但差异随 (\delta) 没有扩大。这个现象与 split-step 的有限步长偏差相容，不构成严格误差界。

## 8. 渐近归一化与有限区间拟合

Theorem 3.1 预测的归一化量应保持在常数量级。两条路线的结果如下：

| 权重 | 归一化量 | producer spread | independent spread | producer 归一化斜率 | independent 归一化斜率 |
|---|---|---:|---:|---:|---:|
| (\beta=1/4) | (Q\delta^{3/4}) | 1.746462 | 1.746387 | 0.157884 | 0.157870 |
| plain (1/3) | (Q\delta^{2/3}) | 1.597429 | 1.597341 | 0.132471 | 0.132454 |
| critical-log | (Q\delta^{2/3}/\log\delta) | 1.077330 | 1.077169 | 0.022031 | 0.021986 |
| (\beta=2/5) | (Q\delta^{3/5}) | 1.494073 | 1.493982 | 0.113434 | 0.113415 |
| (\beta=49/100) | (Q\delta^{51/100}) | 1.374328 | 1.374245 | 0.089688 | 0.089670 |

critical-log 的归一化最平，spread 约为 1.077。其他权重仍显示可见的 pre-asymptotic 漂移。producer 对未去除对数的 (Q) 所作幂律拟合斜率依次为
(-0.592116,-0.534196,-0.413029,-0.486566,-0.420312)；independent 对应为
(-0.592130,-0.534213,-0.413074,-0.486585,-0.420330)。这些有限区间斜率不应被当成精确渐近指数。真正的解析指数来自 Theorem 3.1 的上下界。

## 9. producer 的全部压力检查

来源：`/Users/kasifa/Documents/Math/navier-stokes-r072f/research/certificates/r072f/result.json`。

| 检查名 | 门槛 | 观测值 | 结果 |
|---|---|---:|---|
| `critical_weight_l2_identity` | 精确恒等式等于 75 | 75 | 通过 |
| `positive_weighted_actions` | 所有作用量为正 | 最小值 0.3681634829 | 通过 |
| `fine_coarse_stability` | fine/coarse 在设定容差内 | 最大相对差 0.0012648223 | 通过 |
| `spectral_tail_negligible` | 外谱尾小于 (10^{-10}) | (2.4883024\times10^{-33}) | 通过 |
| `contractive_evolution` | 演化不增至容差外 | 最大 (L^2) 平方范数 1.0 | 通过 |
| `regular_variation_normalizations` | 每个归一化 spread 小于 2.5 | 最大 1.746462；各项见第 8 节 | 通过 |
| `bessel_mass_asymptotic` | (R=128) 时距 (8/\pi^2) 小于 5% | 相对误差 0.0481933885 | 通过 |
| `bessel_root_residual` | Bessel 根残差小于 (2\times10^{-13}) | (2.0876817\times10^{-15}) | 通过 |
| `frontier_vertices_exact` | 三组有理数边界和精确相等 | (1,1,1) | 通过 |

Bessel 质量检查在 (R=128) 时给
(mathrm{mass}/\log R=0.8496335584)，目标 (8/\pi^2=0.8105694691)。这只是 frozen Bessel carrier 的有限 (R) 收敛检查，不是 complete perturbed roots 的上界。

## 10. independent 的全部压力检查

来源：`/Users/kasifa/Documents/Math/navier-stokes-r072f/research/certificates/r072f/independent-result.json`。

| 检查名 | 门槛 | 观测值 | 结果 |
|---|---|---:|---|
| `critical_weight_l2_quadrature` | improper quadrature 与 75 一致 | 75；reported error (7.8435\times10^{-12}) | 通过 |
| `positive_weighted_actions` | 所有作用量为正 | 最小值 0.3682078868 | 通过 |
| `quadrature_pressure` | 10 点/6 点变换 Gauss 差异小于 (2\times10^{-7}) | (1.4220123\times10^{-8}) | 通过 |
| `tail_negligible` | 最大解析 (z)-tail 小于 (2\times10^{-10}) | (1.6359470\times10^{-12}) | 通过 |
| `lattice_boundary_negligible` | 外八模能量比例小于 (10^{-12}) | (8.4687442\times10^{-42}) | 通过 |
| `contractive_evolution` | BDF 演化不增至容差外 | 最大 (L^2) 平方范数 1.0 | 通过 |
| `radius_stability` | radius 64/88 的差异小于 (2\times10^{-5}) | 全部小于 (1.275\times10^{-7}) | 通过 |
| `tolerance_stability` | base/tight tolerance 差异小于 (2\times10^{-5}) | 全部小于 (6.631\times10^{-7}) | 通过 |
| `regular_variation_normalizations` | 每个归一化 spread 小于 2.5 | 最大 1.746387；各项见第 8 节 | 通过 |

radius 与 tolerance 压力值逐项如下：

| 权重 | radius 64/88 相对差 | base/tight tolerance 相对差 |
|---|---:|---:|
| (\beta=1/4) | (1.2745630\times10^{-7}) | (6.6304518\times10^{-7}) |
| plain (1/3) | (1.0306998\times10^{-7}) | (5.3591808\times10^{-7}) |
| critical-log | (6.4011883\times10^{-8}) | (3.3250292\times10^{-7}) |
| (\beta=2/5) | (8.5290747\times10^{-8}) | (4.4338383\times10^{-7}) |
| (\beta=49/100) | (6.3922899\times10^{-8}) | (3.3231411\times10^{-7}) |

independent 主运行还记录了最大 quadrature defect
(1.4220123\times10^{-8})、最大解析尾项
(1.6359470\times10^{-12})、最大边界能量比例
(8.4687442\times10^{-42})。这些检查分别压低了积分阶数、尾部截断和格点半径三类有限计算误差，但仍不是 interval enclosure。

## 11. 最终判断

我把 R0.72F 的已证内容限定为以下四点：

1. (0\le\beta<1/2) 的加权 projected-Lamb action 可由 Leray energy 支付；(1/2) 是仅使用 (Y\in L^1_t) 时的锐端点。
2. 对固定 (0<\beta<1)，精确三角族上的 action 有解析双侧尺度
   (\delta^{\beta-1}(\log\delta)^\gamma)。
3. selected roots 强制 (1/3) 的多项式阈值和端点的一次对数。临界权重
   (s^{-1/3}[1+\log(1/s)]) 只把已知 selected obstruction 饱和。
4. free-amplitude 账本给出必要前沿；explicit coupling 和 root weighting 是两个边界替代方案，其中后者改变了目标量。

当前没有 complete-root 上界，没有额外根的 exhaustion，没有任意三维流上的 trace-packing 定理，没有 continuation criterion。数值文件没有区间算术，也没有把浮点误差包成严格证书。精确三角族本身是全局光滑的，所以这里既没有构造爆破，也没有证明一般三维 Navier--Stokes 的全局正则性。R0.72F 不是千禧年问题的解答。
