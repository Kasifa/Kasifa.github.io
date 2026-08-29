# R0.73C C5 独立审计：冻结不稳定性的 logarithmic fast-time transfer

> **工作笔记状态（2026-08-30）：** 冻结无黏不稳定性 C4 后来已经由区间
> 单值矩阵证书闭合。本文保留为 C5 的阻塞审计：vanishing-viscosity
> persistence、统一 Riesz/dichotomy 与 graph-domain Kato transport 仍为 OPEN。

**日期：** 2026-08-30  
**范围：** 只审计 `r073c_problem_freeze.md` 的 C5 以及 (4.4)--(4.5)。  
**状态：** 条件性 lemma；没有证明 C4，也没有完成 C5。

## 1. 结论

设 \(\varepsilon=|\Lambda|^{-1}\)。若只知道
\(A_{\gamma_*}(0)\) 在某个常用 Sobolev 空间里有一个孤立特征值
\(\sigma_*\)，且 \(\operatorname{Re}\sigma_*>0\)，还不能直接推出
(4.4)。缺少的不是普通的时间连续性，而是下面这个 singular
vanishing-viscosity package：

1. 完整冻结算子
   \(B_{\varepsilon,s}(0)=sA_{\gamma_*}(0)-\varepsilon\mathcal L_{\mu_*}\)
   的不稳定谱必须持续到 \(\varepsilon>0\)；
2. 对应 Riesz 投影和补空间 resolvent/semigroup bound 必须在
   \(\varepsilon\downarrow0\) 时一致；
3. 投影必须属于完整算子 \(B_{\varepsilon,s}(d)\)，不能只投影
   \(A_{\gamma_*}(d)\)，否则 \(P(d)\mathcal L_{\mu_*}Q(d)\)
   是一个未经控制的无界项；
4. 若 (4.4) 中的 \(q_*\) 要与 \(\Lambda\) 无关，还要证明黏性 Riesz
   投影在该向量上收敛。若只需要传播子范数下界，可以使用
   \(q_{\varepsilon,s}\in\operatorname{Ran}P_{\varepsilon,s}(0)\)。

在这些条件下，logarithmic fast-time transfer 的误差规模是足够的：
profile drift 在指数中贡献 \(O(\varepsilon T^2)\)，投影运输贡献
\(O(\varepsilon T)\)，而冻结黏性谱误差只需要是 \(o(1)\)。取
\(T=M\log(1/\varepsilon)\) 后可得到

\[
 \|U_{\varepsilon,s}(T,0)q_{\varepsilon,s}\|_{\mathcal K_{\mu_*}}
 \ge c_M |\Lambda|^{M a-o_M(1)},
 \qquad a=\operatorname{Re}\sigma_*>0.
 \tag{1.1}
\]

因此，(4.4) 到 (4.5) 的最后一步在量词补全后是正确的；真正的
逻辑缺口位于 C4 与 (4.4) 之间。

## 2. 精确空间与无界项

固定 \(\mu=\mu_*>0\)，令

\[
 X_\mu=\mathcal K_\mu,
 \qquad
 \langle q,r\rangle_{X_\mu}
 =\mu^{-1}\langle\mathcal L_\mu^{-1}q,r\rangle_{L^2}.
 \tag{2.1}
\]

这是周期 \(H^{-1}\) 型空间；常数允许依赖固定的 \(\mu_*\)，不能把
下面的估计外推到 \(\mu\downarrow0\)。在该空间上

\[
 D_{X_\mu}(\mathcal L_\mu)=H^1_{\rm per},
 \qquad
 \operatorname{Re}\langle-\mathcal L_\mu q,q\rangle_{X_\mu}
 =-\mu^{-1}\|q\|_2^2\le0.
 \tag{2.2}
\]

所以 \(-\varepsilon\mathcal L_\mu\) 生成 contraction analytic
semigroup，但它在 \(X_\mu\) 上不是有界算子，而且
\(\|\varepsilon\mathcal L_\mu\|_{X_\mu\to X_\mu}=\infty\) 对每个
\(\varepsilon>0\) 都成立。

另一方面，光滑函数乘法在 \(H^{-1}\) 上有界，且
\(\mathcal L_\mu^{-1}:H^{-1}\to H^1\)。因此

\[
 A_\gamma(d)=-i\gamma
 \bigl(M_{W(d)}+M_{W_{xx}(d)}\mathcal L_\mu^{-1}\bigr)
 \in\mathcal B(X_\mu),
 \tag{2.3}
\]

并且对固定的小 \(d_0\)，

\[
 \|A_\gamma(d)-A_\gamma(0)\|_{\mathcal B(X_\mu)}\le C d,
 \qquad
 \|\partial_dA_\gamma(d)\|_{\mathcal B(X_\mu)}\le C.
 \tag{2.4}
\]

这说明 profile motion 是小的**有界**扰动；它没有把黏性项也变成
小的有界扰动。

若 \(A_\gamma(0)q_*=\sigma_*q_*\) 且
\(\operatorname{Re}\sigma_*>0\)，则 Rayleigh coefficient 不经过
critical level。写 \(\phi_*=\mathcal L_\mu^{-1}q_*\in H^1\)，特征方程
可解出 \(\mathcal L_\mu\phi_*\) 为光滑系数乘 \(\phi_*\)，所以周期
elliptic bootstrap 给出 \(q_*\in C^\infty\)。左特征向量还必须对
\(X_\mu\)-adjoint 单独完成同样的 domain 检查。即使左右向量都足够
光滑，也不能把 singular perturbation 自动改写成 operator-norm
perturbation theorem。

## 3. 两个符号

写 \(s=\operatorname{sgn}\Lambda\)。由于 \(W\) 为实函数，
\(A=-iB\) 且 \(B\) 的系数为实数。若

\[
 Aq_*=\sigma_*q_*,
\]

则

\[
 (-A)\overline{q_*}=\overline{\sigma_*}\,\overline{q_*}.
 \tag{3.1}
\]

所以正负 \(\Lambda\) 都有相同的增长率
\(a=\operatorname{Re}\sigma_*\)，但一般需要不同的初值
\(q_{*,+}=q_*\) 与 \(q_{*,-}=\overline{q_*}\)。不能把同一个复初值
不加说明地用于两个符号。

## 4. 可审计的 conditional transfer lemma

下面的 lemma 把尚未证明的谱输入与可完成的时间运输分开。

### Lemma 4.1（完整黏性谱的 logarithmic transfer）

固定 \(\gamma_*>0\)、\(\mu_*=\gamma_*^2\) 和一个符号
\(s\in\{-1,1\}\)。令

\[
 B_{\varepsilon,s}(d)
 =sA_{\gamma_*}(d)-\varepsilon\mathcal L_{\mu_*},
 \qquad D(B_{\varepsilon,s}(d))=H^1_{\rm per}\subset X_{\mu_*}.
 \tag{4.1}
\]

设 \(sA_{\gamma_*}(0)\) 有一个 simple rightmost eigenvalue
\(\sigma_s\)，\(a=\operatorname{Re}\sigma_s>0\)。若有
\(d_0,\delta,C>0\)，使所有充分小的 \(\varepsilon\) 满足：

**H1（vanishing-viscosity spectral persistence）.**
\(B_{\varepsilon,s}(0)\) 有 simple eigenvalue
\(\lambda_{\varepsilon,s}(0)\) 和 rank-one Riesz projection
\(P_{\varepsilon,s}(0)\)，并且

\[
 \eta_\varepsilon
 :=|\lambda_{\varepsilon,s}(0)-\sigma_s|=o(1),
 \qquad
 \sup_\varepsilon\|P_{\varepsilon,s}(0)\|<\infty.
 \tag{4.2}
\]

**H2（uniform contour and continuation）.**
该谱点在 \(0\le d\le d_0\) 上沿同一隔离 contour 延拓为
\(\lambda_{\varepsilon,s}(d)\)、\(P_{\varepsilon,s}(d)\)，相应
resolvent 在 contour 上一致有界。于是

\[
 |\lambda_{\varepsilon,s}(d)-\lambda_{\varepsilon,s}(0)|\le Cd,
 \qquad
 \|\partial_dP_{\varepsilon,s}(d)\|\le C.
 \tag{4.3}
\]

**H3（uniform complementary dichotomy）.**
在由 \(P_{\varepsilon,s}(d)\) 的 Kato transport 识别后的补空间上，
冻结或缓慢变化的演化满足

\[
 \|V_{Q,\varepsilon}(\theta,\tau)\|
 \le C e^{(a-2\delta)(\theta-\tau)},
 \qquad 0\le\tau\le\theta,
 \tag{4.4}
\]

而不稳定一维块的实部至少为
\(a-\eta_\varepsilon-C\varepsilon\theta\)。

**H4（domain compatibility）.** Riesz 投影及其导数保持
\(D(\mathcal L_{\mu_*})\)，其 graph-norm bounds 足以使 Kato
transport 保持公共定义域。等价地，可以直接假设相应的 sectorial
evolution family 和 dichotomy 已在 \(X_{\mu_*}\) 上构造。

令 \(q_{\varepsilon,s}\) 是
\(\operatorname{Ran}P_{\varepsilon,s}(0)\) 中的单位向量。则对每个
固定 \(M>0\)，当

\[
 T_\varepsilon=M\log(1/\varepsilon),
 \qquad \varepsilon T_\varepsilon\le d_0,
 \tag{4.5}
\]

有

\[
 \|U_{\varepsilon,s}(T_\varepsilon,0)q_{\varepsilon,s}\|_{X_{\mu_*}}
 \ge c
 \exp\!\left[
   (a-C\eta_\varepsilon)T_\varepsilon
   -C\varepsilon T_\varepsilon^2
   -C\varepsilon T_\varepsilon
 \right].
 \tag{4.6}
\]

这里 \(c>0\) 与 \(\varepsilon\) 无关；常数可以依赖固定的
\(M,\gamma_*,\delta\)。特别地，

\[
 \|U_{\varepsilon,s}(T_\varepsilon,0)q_{\varepsilon,s}\|_{X_{\mu_*}}
 \ge c_M\varepsilon^{-Ma+o_M(1)}
 =c_M|\Lambda|^{Ma-o_M(1)}.
 \tag{4.7}
\]

若另有
\(P_{\varepsilon,s}(0)q_{*,s}\to q_{*,s}\ne0\)，同一结论可把
\(q_{\varepsilon,s}\) 换成固定的无黏特征向量 \(q_{*,s}\)。

### 证明纲要

令 \(P(\theta)=P_{\varepsilon,s}(\varepsilon\theta)\)。由 Riesz
公式和 (4.3)，

\[
 \|P'(\theta)\|\le C\varepsilon.
 \tag{4.8}
\]

使用 \(K=[P',P]\) 构造 Kato transport \(S'=KS\)。则
\(S(\theta)P(0)=P(\theta)S(\theta)\)，且在 (4.5) 上

\[
 \|S(\theta)^{\pm1}\|\le e^{C\varepsilon\theta},
 \qquad
 \|S(\theta)^{\pm1}-I\|=O(\varepsilon\theta).
 \tag{4.9}
\]

在 \(S\) 坐标中，\(S^{-1}B_{\varepsilon,s}(\varepsilon\theta)S\)
相对于固定的 \(P(0)\oplus Q(0)\) 是 block diagonal；唯一的
off-diagonal 项来自 \(-S^{-1}S'\)，大小为 \(O(\varepsilon)\)。
H3 的 gap 给出

\[
 \|z(\theta)\|
 \le C\varepsilon e^{\int_0^\theta
   \operatorname{Re}\lambda_{\varepsilon,s}(\varepsilon r)\,dr},
 \tag{4.10}
\]

而它反馈到一维 amplitude 的相对误差为
\(O(\varepsilon^2\theta)\)。由 (4.3)，

\[
 \int_0^T\operatorname{Re}\lambda_{\varepsilon,s}(\varepsilon r)\,dr
 \ge(a-\eta_\varepsilon)T-C\varepsilon T^2.
 \tag{4.11}
\]

再用 (4.9) 返回原坐标即得 (4.6)。最重要的是：证明从未把
\(-\varepsilon\mathcal L_{\mu_*}\) 当作有界 forcing；它从一开始
就在完整 sectorial generator 和完整 Riesz projection 中。

## 5. 哪些假设可能由当前周期算子证明

对当前算子可以写成

\[
 A_\gamma(0)=M+K,
 \qquad
 M=-i\gamma M_{W_0},
 \qquad
 K=-i\gamma M_{W_0''}\mathcal L_\mu^{-1}.
 \tag{5.1}
\]

在 \(X_\mu\) 上 \(K\) 是 compact，而 \(M\) 的谱位于虚轴。因此
任何 \(\operatorname{Re}\sigma>0\) 的谱点都在 essential spectrum
之外。若至少有一个不稳定谱点，可以把目标换成有限个 rightmost
不稳定谱点组成的 cluster。

这使 H1--H3 很可信，但还没有自动证明它们。一个可审计的证明应
分成以下三个子 lemma：

1. **V1：base resolvent convergence.** 对远离虚轴的紧 contour，证明
   \((z-M+\varepsilon\mathcal L_\mu)^{-1}\) 一致有界并强收敛到
   \((z-M)^{-1}\)。
2. **V2：compact Fredholm convergence.** 利用 V1 与 \(K\) 的 compactness
   把 Birman--Schwinger family 的强收敛升级为 compact factor 的
   operator-norm 收敛，证明不稳定特征值的代数重数保持，并得到
   Riesz 投影的充分收敛。
3. **V3：uniform half-plane resolvent.** 在选中 rightmost cluster 的
   左侧建立一致 resolvent bound，再用 Hilbert-space semigroup
   theorem 得到 H3。只在一条小 contour 上控制 resolvent 不足以
   给出补空间 evolution bound。

若能进一步证明 simple branch 的左右特征向量属于
\(D(\mathcal L_\mu)\) 并控制尾部，可能得到
\(\eta_\varepsilon=O(\varepsilon^\alpha)\)，甚至形式上的
first-order shift。但 C5 不需要这个速率；\(\eta_\varepsilon=o(1)\)
已经足以给出 power exponent 中的 \(o(1)\)。在完成 V1--V3 前，不能
用普通 Kato bounded-perturbation 公式声称
\(\eta_\varepsilon=O(\varepsilon)\)。

若 rightmost cluster 不是 simple，Lemma 4.1 要改成有限维 block
版本。仅知道 algebraic multiplicity 而没有该 block 的最小增长或
exponential dichotomy，不能把单个 \(\operatorname{Re}\sigma_*>0\)
直接代入 (4.4)。

## 6. 误差账本

| 来源 | fast-time 大小 | 在 \(T=M\log(1/\varepsilon)\) 的影响 |
|---|---:|---:|
| frozen viscous eigenvalue shift | \(\eta_\varepsilon=o(1)\) | power exponent 损失 \(M\eta_\varepsilon=o_M(1)\) |
| profile drift \(A(\varepsilon\theta)-A(0)\) | \(O(\varepsilon\theta)\) | exponential loss \(O(\varepsilon T^2)\); power exponent loss \(O(\varepsilon\log(1/\varepsilon))\) |
| Riesz projection derivative | \(O(\varepsilon)\) | transport distortion \(O(\varepsilon T)\) |
| unstable-to-complement leakage | \(O(\varepsilon)\) with gap \(\delta\) | relative \(O(\varepsilon/\delta)\) |
| complement-to-unstable feedback | \(O(\varepsilon^2)\) with gap | relative \(O(\varepsilon^2T)\) |
| \(-\varepsilon\mathcal L_\mu\) | unbounded on \(X_\mu\) | 不列为 forcing；吸收到 \(B_{\varepsilon,s}\)、\(\lambda_\varepsilon\)、\(P_\varepsilon\) |
| \(\mathcal K_\mu\) 与其他 norm 的比较 | fixed-\(\mu\) 常数 | 可依赖 \(\mu_*\)，不得声称 \(\mu\)-uniform |

## 7. (4.4) 与 (4.5) 的量词

建议把 (4.4) 写成：对每个固定 \(M>0\) 和每个符号
\(s\in\{-1,1\}\)，存在 \(c_M>0\)、\(\Lambda_M<\infty\)，使所有
满足 \(s\Lambda>0\)、\(|\Lambda|\ge\Lambda_M\) 的参数都有

\[
 d_\Lambda=M\frac{\log|\Lambda|}{|\Lambda|},
 \qquad
 \|U_{\gamma_*,\Lambda}(d_\Lambda,0)\|_{\mathcal K_{\mu_*}\to
 \mathcal K_{\mu_*}}
 \ge c_M|\Lambda|^{Ma-r_M(\Lambda)},
 \tag{7.1}
\]

其中 \(r_M(\Lambda)\to0\)。若坚持写向量版本，必须说明初值是固定
\(q_{*,s}\) 还是允许依赖 \(\Lambda\) 的
\(q_{\varepsilon,s}\)。传播子范数版本没有这个歧义。

现在固定任意 \(p>0\)，选择 \(M>p/a\)。对充分大的
\(|\Lambda|\)，\(d_\Lambda\le d_*\)，所以

\[
 \frac{G_{\gamma_*}(\Lambda;d_*)}{|\Lambda|^p}
 \ge c_M|\Lambda|^{Ma-p-r_M(\Lambda)}\longrightarrow\infty.
 \tag{7.2}
\]

若 (7.1) 对所有充分大的 \(|\Lambda|\) 成立，实际得到的是对应符号
上的 limit \(=\infty\)，强于 (4.5) 的 limsup。若 transfer 只沿一条
趋于无穷的序列成立，则只能得到 limsup。

这足以排除固定 \(\gamma_*\)、固定 \(d_*\) 上任何固定次数的
\(G_{\gamma_*}(\Lambda;d_*)\le C(1+|\Lambda|)^p\)。由于 complete-row
upper bound 必须覆盖该行，它也排除同类 complete-row polynomial
upper bound。它不排除：

- 删除该不稳定谱子空间后的 projected polynomial bound；
- 常数或次数依赖 \(\Lambda\) 的陈述；
- 其他 \(\gamma\) 行的 polynomial estimate；
- fixed-window sharp law \(e^{\Theta(|\Lambda|)}\)；
- nonlinear Navier--Stokes 或 Clay 结论。

## 8. 对 C5 状态的建议

目前最准确的状态是：

```text
frozenCollisionRayleighInstability=TO_PROVE
vanishingViscosityUnstableSpectrumPersistence=TO_PROVE
uniformViscousRieszDichotomy=TO_PROVE
logFastTimeProfileTransport=CONDITIONAL
superPolynomialGlobalUpperNoGo=CONDITIONAL
```

下一项解析工作不应从 time-dependent numerical abscissa 开始，而应先
完成 V1--V3。只有在完整黏性 Riesz package 建立后，Lemma 4.1 的
Kato transport 才能把 C4 变成 C5。
