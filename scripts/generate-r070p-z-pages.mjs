#!/usr/bin/env node

import { writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const releases = [
  {
    code: "R0.70P",
    slug: "r0-70p",
    label: "COMPLETE FRAME · CONDITIONAL BRIDGE",
    title: "完整框架修复高频盲区，<br>但投影桥仍是条件性的",
    meta: "完整 Littlewood–Paley 框架给出能量级平方交换子估计与周期投影继续性桥；Navier–Stokes 协方差是否传播这些假设仍未解决。",
    lead: String.raw`R0.70O 排除了高频盲的有限标量观测。本节改用完整光滑框架，证明重建损失只剩一个平方交换子，并把它降到能量级。由此得到严格的周期条件继续性桥，但协方差主投影所需的残差与方向正则性尚未从方程传播出来。`,
    state: "条件桥证明完成；传播门槛保持开放",
    badge: "框架门、交换子门和周期 consumer 均通过",
    theoremTitle: "完整框架把变投影误差压缩为一个平方交换子",
    theoremText: String.raw`对固定的实、偶、径向光滑 Littlewood–Paley Parseval 框架，矩阵场 \(A\) 与零均值 \(f\) 满足能量级端点估计`,
    theoremEq: String.raw`\left(\sum_\alpha\|[T_\alpha,A]f\|_2^2\right)^{1/2}\le C_\varphi\|\nabla A\|_\infty\|f\|_{\dot H^{-1}}.`,
    detailTitle: "周期投影 criterion 不需要选择全局有向特征向量",
    detailText: String.raw`若 \(L\) 是可测秩一正交投影，\(P=I-L\)，那么最大周期 \(H^1\) 强解在下面两个条件下可延拓：`,
    detailEq: String.raw`\operatorname*{ess\,sup}_{0<t<T_{\max}}\|\nabla L(t)\|_\infty<\infty,\qquad P\omega\in L_t^4L_x^2.`,
    bridgeText: String.raw`把框架残差 \(R(t)=\sum_\alpha\|PT_\alpha\omega(t)\|_2^2\) 与交换子估计合并，得到`,
    bridgeEq: String.raw`\|P\omega\|_{L_t^4L_x^2}\le a_0^{-1/2}\!\left(\|R\|_{L_t^2}^{1/2}+C_{\mathcal T}\|u-\bar u\|_{L_t^\infty L_x^2}\|\nabla P\|_{L_t^4L_x^\infty}\right).`,
    value: String.raw`这一步把“有限滤波看不见高频”的问题与真正的动力学传播问题分开了。调和分析重建已经闭合，剩余困难不再是选择更多滤波器，而是证明协方差残差、谱隙和方向代价由 Navier–Stokes 演化控制。`,
    boundary: String.raw`这是条件继续性桥，不是无条件正则性定理。报告没有证明协方差主投影满足这些假设，也没有从 Leray 能量推出 \(R\in L_t^2\) 或 \(\nabla P\in L_t^4L_x^\infty\)。`,
    next: String.raw`R0.70Q 直接推导过滤协方差的演化方程，检查方程能否传播残差、谱隙与投影正则性。`,
    literature: true,
  },
  {
    code: "R0.70Q",
    slug: "r0-70q",
    label: "COVARIANCE EVOLUTION · RAW PROJECTOR NO-GO",
    title: "协方差演化已经写清，<br>原始投影梯度仍不能由能量推出",
    meta: "精确过滤协方差演化、秩一扩散平衡与 Beltrami 热模反例；原始投影梯度路线失败，结构适配的条件目标保留。",
    lead: String.raw`本节把完整框架协方差的物质—扩散方程逐项写出。秩一状态的谱曲率会被投影梯度协方差精确吸收；但 Leray 能量只给残差的时间 L1。一个旋转 Beltrami 热模进一步说明，即使残差为零、相对谱隙为一，主投影仍可在空间中任意快地旋转。`,
    state: "演化恒等式与反例完成；结构适配判据为条件结果",
    badge: "原始投影正则性门关闭",
    theoremTitle: "秩一扩散平衡是精确的，能量时间指数却不够",
    theoremText: String.raw`在 \(Q=EL\)、\(E>0\) 的秩一点，谱曲率 \(\mathcal K_Q\) 被投影梯度协方差吸收：`,
    theoremEq: String.raw`\mathcal K_Q\le\sum_{\alpha,k}|P\partial_k\Omega_\alpha|^2.`,
    detailTitle: "强相对谱隙并不稳定低幅值处的方向",
    detailText: String.raw`精确全局 Beltrami 热模满足`,
    detailEq: String.raw`R=0,\qquad {\lambda_1-\lambda_2\over\operatorname{tr}Q}=1,\qquad \|\nabla P\|_F={\|\nabla Q\|_F\over\operatorname{tr}Q}=\sqrt2\,N.`,
    bridgeText: String.raw`保留下来的结构适配条件量是精确交换子平方 \(\mathfrak C_P\) 与能量加权方向代价 \(\mathfrak W_L\)。若`,
    bridgeEq: String.raw`R,\mathfrak C_P\in L_t^2,\qquad \mathfrak W_L=\int\|u_*\|_2^2\|\nabla u\|_2^2\|\nabla L\|_\infty^2\,dt<\infty,`,
    bridgeTail: String.raw`则周期强解可继续。该判据本身不需要谱隙，但这些量尚未由能量传播。`,
    value: String.raw`这一步把“谱隙应该让方向平滑”的直觉改成了可检验的幅值敏感陈述：接近零协方差时，相对谱隙没有足够尺度。后续估计应直接看交换子与加权方向成本，而不是统一控制裸的 \(\nabla P\)。`,
    boundary: String.raw`Beltrami 热模是光滑全局解，只反驳一个原始投影梯度估计。它不是奇性样本。结构适配继续性判据仍含未传播假设，尚未形成无条件结果。`,
    next: String.raw`R0.70R 保留扩散两项的联合符号，定量计算偏离秩一时的最坏损失。`,
  },
  {
    code: "R0.70R",
    slug: "r0-70r",
    label: "NEAR-RANK DIFFUSION · SHARP DEFICIT",
    title: "近秩一扩散缺口只有平方根损失，<br>但仍停在涡量梯度层",
    meta: "近秩一协方差的谱曲率—投影扩散差有精确且最优的平方根残差界；右端仍是完整 palinstrophy 密度。",
    lead: String.raw`R0.70Q 在严格秩一处得到非正扩散贡献。本节把该事实推进到近秩一情形：最坏正误差只按第二特征值比的平方根增长，而且常数不能改进。代价是右端仍含完整块梯度密度，也就是空间积分后的 palinstrophy。`,
    state: "尖锐有限维不等式与等号流完成",
    badge: "谱分母被定量消除；能量闭合未完成",
    theoremTitle: "谱曲率与投影扩散必须作为一个整体估计",
    theoremText: String.raw`令 \(\rho=\lambda_2/\lambda_1<1\)，则`,
    theoremEq: String.raw`\mathcal D_P-\mathcal K_Q\ge-{\sqrt\rho\over1-\sqrt\rho}\,\mathcal G.`,
    detailTitle: "残差比形式显示平方根阶",
    detailText: String.raw`若 \(\eta=r/E<1/2\)，由 \(\rho\le\eta/(1-\eta)\) 得到`,
    detailEq: String.raw`\mathcal D_P-\mathcal K_Q\ge- {\sqrt\eta\over\sqrt{1-\eta}-\sqrt\eta}\,\mathcal G.`,
    bridgeText: String.raw`固定框架内的两频无散周期涡量在一点实现等号，并来自一个光滑全局剪切热流。因此平方根系数不是证明松弛造成的。`,
    bridgeEq: String.raw`\int_{\mathbb T^3}\mathcal G\,dx=\|\nabla\omega\|_2^2.`,
    value: String.raw`这一结果删除了不受控的裸谱分母，说明近秩一确实改善扩散账本；同时它精确标出改善停在哪里：误差仍乘以高一阶的涡量梯度。`,
    boundary: String.raw`定理是系数层的尖锐扩散不等式，不是能量层估计。等号样本是光滑全局剪切解，不表示存在奇性，也没有控制涡量拉伸。`,
    next: String.raw`R0.70S 检查 R0.70Q 的能量级结构量能否控制这个 palinstrophy majorant 的时空积分。`,
  },
  {
    code: "R0.70S",
    slug: "r0-70s",
    label: "ENERGY-LEVEL NO-GO · PALINSTROPHY",
    title: "四个能量级输入同时趋零，<br>近秩一 palinstrophy majorant 仍可发散",
    meta: "一列光滑全局周期剪切热流证明：能量、协方差残差、精确交换子与加权方向代价不能统一控制近秩一 palinstrophy majorant。",
    lead: String.raw`本节对 R0.70R 的正 majorant 做直接压力测试。构造是一列光滑全局周期剪切热流：近秩一比保持统一，R0.70Q 的四个输入全部趋于零，而需要控制的 palinstrophy majorant 却趋于无穷。`,
    state: "能量级统一 majorant 路线关闭",
    badge: "全局光滑序列给出严格尺度分离",
    theoremTitle: "低阶结构信息看不见上移的 palinstrophy 尺度",
    theoremText: String.raw`对每个固定 \(T,\nu>0\)，存在光滑全局周期解序列，使`,
    theoremEq: String.raw`\|u_{N,*}(0)\|_2^2+\|R_N\|_{L_t^2}+\|\mathfrak C_{P_N}\|_{L_t^2}+\mathfrak W_{L_N}\longrightarrow0,`,
    detailTitle: "目标积分却反向发散",
    detailText: String.raw`在统一的点态近秩一上界下，仍有`,
    detailEq: String.raw`\int_0^T\!\!\int_{\mathbb T^3}c_{r_N/E_N}\,\mathcal G_N\,dx\,dt\longrightarrow+\infty.`,
    bridgeText: String.raw`因此，任何在上述四个标量输入的零点附近局部有界的右端，都不可能控制 R0.70R majorant。样本的初始 enstrophy 发散，说明缺失信息正是导数尺度。`,
    bridgeEq: String.raw`\|\omega_N(0)\|_2\longrightarrow\infty\quad\text{沿该尺度序列}.`,
    value: String.raw`这是一次干净的路线筛选：继续组合同一组能量级标量不会解决问题。后续要么显式加入能看见频率上移的量，要么保留扩散与拉伸中的有符号抵消。`,
    boundary: String.raw`序列中的每个解都光滑且全局存在，初始 enstrophy 并不统一有界。因此它不排除含初始 H1、频率矩或更高正则性的估计，更不是爆破解。`,
    next: String.raw`R0.70T 放弃正 majorant，回到完整的有符号涡量拉伸恒等式。`,
  },
  {
    code: "R0.70T",
    slug: "r0-70t",
    label: "SIGNED STRETCHING · DIVERGENCE DEFECT",
    title: "完整框架拉伸账本中，<br>裸幅值梯度可以精确消去",
    meta: "完整框架给出精确涡量拉伸分解；主线纵向缺陷由投影块散度控制，常数 2 尖锐，但完整有符号积分仍存在抵消。",
    lead: String.raw`正 palinstrophy majorant 已被 R0.70S 排除，本节转回有符号的涡量拉伸。Parseval 恒等式把它拆成主协方差收缩与一个显式框架缺陷；过滤块无散使主特征值的裸梯度在主线项中消去。`,
    state: "精确有符号账本与尖锐点态缺陷完成",
    badge: "导数通道被定位；尚不是 enstrophy 闭合",
    theoremTitle: "主线纵向缺陷由一个结构化散度平方控制",
    theoremText: String.raw`令 \(L\) 为主秩一投影，\(\lambda_1\) 为主特征值，则项级积分分部产生`,
    theoremEq: String.raw`\mathcal A_L=L\bigl(\nabla\lambda_1+2\lambda_1\operatorname{div}L\bigr),`,
    detailTitle: "常数 2 在固定完整框架内是尖锐的",
    detailText: String.raw`若 \(\mathcal J_P=\sum_\alpha|\operatorname{div}(P\Omega_\alpha)|^2\)，则`,
    detailEq: String.raw`|\mathcal A_L|\le2\sqrt{\lambda_1\mathcal J_P}.`,
    bridgeText: String.raw`一个光滑周期无散场在一点实现等号，并启动全局垂直剪切热流。但完整的有符号积分中，\(\mathcal A_L\) 会与部分残差和框架交换子贡献抵消。`,
    bridgeEq: String.raw`\mathscr P(t)=\int_{\mathbb T^3}\omega\cdot S\omega\,dx=\int S:Q\,dx+\mathfrak E_S.`,
    value: String.raw`结果说明绝对值账本需要哪一种导数信息，同时警告不能把拆开的项分别取绝对值。真正可能有用的是总和中的符号抵消，而不是再为 \(\mathcal A_L\) 单独寻找正 majorant。`,
    boundary: String.raw`尖锐样本的涡量拉伸为零，所以它只证明项级常数尖锐，不是完整有符号闭合的反例。本节没有得到 enstrophy 估计或继续性定理。`,
    next: String.raw`R0.70U 用固定三频族检查近秩残差能以多高的幂控制完整有符号余项。`,
    literature: true,
  },
  {
    code: "R0.70U",
    slug: "r0-70u",
    label: "SIGNED REMAINDER · SQUARE-ROOT FRONTIER",
    title: "残差是二次小量，<br>有符号余项却保留一次项",
    meta: "固定三频精确族证明：近秩残差不能以优于平方根的幂控制有符号协方差余项；平方根阶仍未被排除。",
    lead: String.raw`本节用一个不移动频率的三频族检验残差压缩。所有普通固定频率范数与主谱隙保持有界，协方差残差按 ε² 消失，而完整有符号余项含有非零的 ε 一次项。`,
    state: "优于平方根的残差幂路线关闭",
    badge: "有限 Fourier 证书锁定一阶共振系数",
    theoremTitle: "线性残差控制和所有更高幂同时失败",
    theoremText: String.raw`对每个 \(1\le p\le\infty\)，精确三频族满足`,
    theoremEq: String.raw`\|r_\varepsilon\|_{L^p}=\Theta(\varepsilon^2),\qquad \mathfrak R_{\mathrm{sgn}}(\omega_\varepsilon)=c_0\varepsilon+O(\varepsilon^2),\quad c_0\ne0.`,
    detailTitle: "平方根是该族暴露出的代数边界",
    detailText: String.raw`若 prefactor 沿族局部有界，则下面的估计对任何 \(\theta>1/2\) 都不可能成立：`,
    detailEq: String.raw`|\mathfrak R_{\mathrm{sgn}}|\le F_\varepsilon\|r_\varepsilon\|_{L^p}^{\theta}.`,
    bridgeText: String.raw`这个结论包含线性残差与有界权重残差估计，但没有排除 \(\theta=1/2\)，也没有排除投影导数、框架交换子、跨尺度张量或时间积分后的抵消。`,
    bridgeEq: String.raw`\mathcal D_\times=\omega\otimes\omega-Q`,
    value: String.raw`残差只记录协方差离开秩一面的面积大小，却丢掉了产生一次共振的跨尺度相位信息。后续必须保留 \(\mathcal D_\times\) 或等价的 response-coherence 数据。`,
    boundary: String.raw`这是单时刻运动学估计的反例，不是 Navier–Stokes 长时间行为结论。它没有否定平方根阶、有符号时间抵消或任何使用更多结构的估计。`,
    next: String.raw`R0.70V 求出 \(\mathcal D_\times\) 的精确 Fourier response-distance 核，并确定拉伸真正看见的投影范数。`,
    literature: true,
  },
  {
    code: "R0.70V",
    slug: "r0-70v",
    label: "RESPONSE DISTANCE · PROJECTED DEFECT",
    title: "跨尺度缺陷有非负 response-distance 核，<br>拉伸只看其中一个投影",
    meta: "完整框架缺陷的精确 carré-du-champ 与 Fourier response-distance 分解；全张量不受秩残差控制，strain-projected critical defect 保留。",
    lead: String.raw`R0.70U 留下跨尺度张量 \(\mathcal D_\times=\omega\otimes\omega-Q\)。本节给出它的精确 Fourier 核：每一对输入频率的权重都是框架响应向量之间的平方距离。该核在同半径处二次消失，但完整张量仍不是拉伸账本所需的最小对象。`,
    state: "response-distance 恒等式与投影账本完成",
    badge: "全张量路线关闭；strain-projected 量保留",
    theoremTitle: "完整 Parseval 框架产生一个非负平方弦长核",
    theoremText: String.raw`若 \(V(k)\) 是频率 \(k\) 的完整响应向量，则`,
    theoremEq: String.raw`\widehat{\mathcal D_\times}(n)=\sum_{p+q=n}K(p,q)\widehat\omega(p)\otimes\widehat\omega(q),\qquad K(p,q)={1\over2}\|V(p)-V(q)\|_{\ell^2}^2.`,
    detailTitle: "涡量拉伸只使用 strain-compatible 投影",
    detailText: String.raw`定义 \(\nu_n=n/|n|\) 与`,
    detailEq: String.raw`\mathfrak X_\times=\sum_{n\ne0}|n|^{-2}|\nu_n\times\widehat{\mathcal D_\times}(n)\nu_n|^2.`,
    bridgeText: String.raw`Biot–Savart 与 Cauchy–Schwarz 给出精确的粘性吸收账本`,
    bridgeEq: String.raw`|\mathfrak E_S|\le\|\nabla\omega\|_2\mathfrak X_\times^{1/2}\le{\nu\over2}\|\nabla\omega\|_2^2+{1\over2\nu}\mathfrak X_\times.`,
    value: String.raw`response chord 揭示了真实的尺度局部性：同半径相互作用完全消失，窄径向带得到 mode-count 无关的正估计。与此同时，strain projection 删除了对拉伸无贡献的张量方向，使下一门槛更窄。`,
    boundary: String.raw`公式只是吸收账本。尚未证明 \(\int\mathfrak X_\times dt\) 的能量级控制，主项 \(\int S:Q\) 也未处理。秩一协方差不能控制完整 \(\mathcal D_\times\)，但这不自动否定其 strain projection。`,
    next: String.raw`R0.70W 检查 pairwise polarization-area 估计在跨壳求和后能否控制 \(\mathfrak X_\times\)。`,
  },
  {
    code: "R0.70W",
    slug: "r0-70w",
    label: "PHYSICAL AREA · SUMMATION NO-GO",
    title: "物理协方差面积处处为零，<br>投影缺陷仍严格为正",
    meta: "分离半径的秩一周期场证明：物理 frame area 及其逆频变换不能控制 strain-projected frame defect；该样本的 signed work 恰为零。",
    lead: String.raw`本节检验 R0.70V 的 pairwise 面积估计能否在全频求和后变成物理协方差面积范数。一个两壳、点态共线的周期场给出否定答案：每个框架块都平行，协方差严格秩一，但跨壳 response 差仍留下非零投影缺陷。`,
    state: "物理面积到投影缺陷的求和路线关闭",
    badge: "信息损失反例为精确有限 Fourier 场",
    theoremTitle: "点态共线并不等于 response 预卷积共线",
    theoremText: String.raw`取 \(\omega_\varepsilon=w+\varepsilon gw\)，其中 \(w=e_1\cos x_2-e_2\cos x_1\)、\(g=\cos4x_3\)。严格分离的径向响应给出`,
    theoremEq: String.raw`Q_\varepsilon=(1+\varepsilon^2g^2)w\otimes w,\qquad G_Q\equiv0,\qquad r\equiv0.`,
    detailTitle: "跨壳 frame defect 与其投影范数仍不为零",
    detailText: String.raw`直接计算得到`,
    detailEq: String.raw`\mathcal D_{\times,\varepsilon}=2\varepsilon g\,w\otimes w,\qquad \mathfrak X_{\times,\varepsilon}={2\over729}\varepsilon^2>0.`,
    bridgeText: String.raw`因此任何在 \(G_Q=0\) 时消失的 definite 右端都不能控制 \(\mathfrak X_\times\)。但该样本的 signed work 正好为零：`,
    bridgeEq: String.raw`\mathfrak E_S(\omega_\varepsilon)=0.`,
    value: String.raw`反例区分了两个层次：物理空间的块面积已经丢掉 response-frequency 标签，无法恢复正投影缺陷；有符号三线性配对仍可能因 Fourier 支撑而取消。`,
    boundary: String.raw`本节关闭的是“物理面积 → definite 投影范数 → signed work”的间接路线。由于样本的 signed work 为零，它没有关闭直接估计 \(\mathfrak E_S\) 的可能性。`,
    next: String.raw`R0.70X 直接构造有非零 signed work 的秩至多一协方差场，并寻找三线性循环消去。`,
  },
  {
    code: "R0.70X",
    slug: "r0-70x",
    label: "CYCLIC NULL · SIGNED OBSTRUCTION",
    title: "协方差秩至多一，<br>有符号 frame-defect work 仍可非零",
    meta: "精确有限 Fourier 场关闭直接 covariance-area signed bound；循环 Laplacian 权重恒等式同时给出尖锐的一阶 high–high–low 增益。",
    lead: String.raw`R0.70W 的反例没有产生 signed work。本节补上这一缺口：存在光滑有限 Fourier 无散场，使完整框架协方差处处秩至多一、物理面积恒为零，但 strain 与 frame defect 的有符号配对严格为负。`,
    state: "直接物理面积 signed bound 关闭；循环 null 保留",
    badge: "负结论与正尺度增益同时精确认证",
    theoremTitle: "秩一几何不足以迫使 frame-defect work 消失",
    theoremText: String.raw`精确构造满足`,
    theoremEq: String.raw`\operatorname{rank}Q\le1,\qquad G_Q\equiv0,\qquad \mathfrak E_S<0.`,
    detailTitle: "三种 strain placement 具有 Laplacian 加权循环 null",
    detailText: String.raw`若 \(n+p+q=0\)，且三极化分别横截对应频率，则`,
    detailEq: String.raw`|n|^2A_n+|p|^2A_p+|q|^2A_q=0.`,
    bridgeText: String.raw`在 high–high–low 三角形中，三种 placement 合并后获得一个 \(t/R\) 的壳间增益；显式族证明一阶是 orbitwise 尖锐的。`,
    bridgeEq: String.raw`\text{HHL gain}\sim {\text{low radius}\over\text{high radius}}.`,
    value: String.raw`这一步说明物理协方差面积压缩得过早，但三线性形式本身保留真实的循环消去。后续估计应在卷积前保留 response 权重与三种 strain placement，而不是先取正 definite 面积。`,
    boundary: String.raw`循环恒等式给出尺度局部性，不会让秩一场的 signed work 自动为零，也没有单独改进经典三次涡量界。本节没有得到时间可积性或继续性定理。`,
    next: String.raw`R0.70Y 把循环增益提升为完整 multiplier 与临界 Besov 求和，并检查更强的正主特征值假设。`,
    literature: true,
  },
  {
    code: "R0.70Y",
    slug: "r0-70y",
    label: "RESPONSE SLOPE · CRITICAL BESOV",
    title: "response chord 斜率可以临界求和，<br>对称 Besov 指数正好停在 3",
    meta: "response-slope 精确分解导出无对数临界 Besov 估计，q=3 尖锐；统一正主特征值仍不能修复旧的 covariance-area 候选。",
    lead: String.raw`本节把 R0.70X 的 orbitwise 壳间增益升级为完整 multiplier 估计。循环系数是 response chord 斜率的平方，并在 high–high–low 区域得到可求和的一阶增益，由此产生两个无对数临界 Besov 界。`,
    state: "frame-defect endpoint 估计完成；主协方差项仍开放",
    badge: "对称 Besov 序列指数 q=3 尖锐",
    theoremTitle: "循环系数是 response chord slope 的平方",
    theoremText: String.raw`若 \(d_n=(V(p)-V(q))/|n|\)，则`,
    theoremEq: String.raw`\beta_n={K(p,q)\over|n|^2}={1\over2}\|d_n\|_{\ell^2}^2.`,
    detailTitle: "signed frame defect 具有临界、无对数的端点界",
    detailText: String.raw`完整壳分解给出`,
    detailEq: String.raw`|\mathfrak E_S(\omega)|\le C\|\omega\|_{B^0_{3,3}}^3,\qquad |\mathfrak E_S(\omega)|\le C\|\omega\|_{B^0_{\infty,\infty}}\|\omega\|_2^2.`,
    bridgeText: String.raw`尺度分离 packet 证明 \(q=3\) 在对称 \(B^0_{3,q}\) 三次界中不能提高。另一个四十模态 filler 使 \(\lambda_1(Q)\) 处处有统一正下界，但旧的物理面积比值仍发散。`,
    bridgeEq: String.raw`{ |\mathfrak E_S(\omega_\Lambda)|\over \|\nabla\omega_\Lambda\|_2\|G_{Q_\Lambda}\|_{6/5}}\longrightarrow\infty.`,
    value: String.raw`这是该阶段第一个完整的正端点估计：response-difference 通道确有临界尺度补偿。但它只处理 frame defect，不包含主项 \(\int S:Q\)。`,
    boundary: String.raw`Leray 能量并不自动给出 \(L_t^1B^0_{\infty,\infty}\)，因此端点界还不是 enstrophy 闭合。统一正 \(\lambda_1\) 的反例在某点有 \(\lambda_1=\lambda_2\)，没有决定强主谱隙分支。`,
    next: String.raw`R0.70Z 直接检验强绝对/相对主谱隙能否决定主协方差功的符号，并分解完整 stretching 的 response 通道。`,
    literature: true,
  },
  {
    code: "R0.70Z",
    slug: "r0-70z",
    label: "EIGENGAP SIGN NO-GO · TWO-CHANNEL LIFT",
    title: "协方差完全相同且谱隙很强，<br>主功仍可以反号",
    meta: "完全相同协方差的有限 Fourier 符号对关闭强主谱隙的符号律；投影导数公式成立，但完整 stretching 仍含阶一 common-response 通道。",
    lead: String.raw`本节给强主谱隙分支一个直接检验。两组光滑有限 Fourier 涡量场具有完全相同的点态协方差、相同主投影与统一强谱隙，主协方差功却大小相同、符号相反。`,
    state: "主谱隙符号律关闭；common-response 通道保留",
    badge: "相同 Q 的精确符号对与两通道分解完成",
    theoremTitle: "任何只依赖 Q 的符号律都无法区分这对场",
    theoremText: String.raw`对每个 \(\Lambda>0\)，精确符号对满足`,
    theoremEq: String.raw`Q(\omega_{\Lambda,+})=Q(\omega_{\Lambda,-}),\quad \lambda_1-\lambda_2\ge8\Lambda^2,\quad {\lambda_1-\lambda_2\over\operatorname{tr}Q}\ge{1\over2},`,
    detailTitle: "主协方差功的符号仍相反",
    detailText: String.raw`同一 \(Q\) 对应`,
    detailEq: String.raw`\mathfrak P_Q(\omega_{\Lambda,\pm})=\pm{9\sqrt{41}\over164}\Lambda^3.`,
    bridgeText: String.raw`谱隙确实给出投影微分的上界，但不控制协方差功：`,
    bridgeEq: String.raw`DP_1[H]=\sum_{j=2}^3{P_jHP_1+P_1HP_j\over\lambda_1-\lambda_j},\qquad |DP_1[H]|_F\le{|H|_F\over\lambda_1-\lambda_2}.`,
    bridgeTail: String.raw`预卷积的两通道 lift 表明 response-difference 通道继承 R0.70Y 的弦增益，而 common-response 通道在 HHL 相互作用中仍为阶一。`,
    value: String.raw`结论把“方向稳定”与“功的符号”彻底分开。谱隙能控制给定 Q 的投影灵敏度，却不能恢复生成 Q 时被平方化丢失的 Fourier 符号。`,
    boundary: String.raw`反例是运动学有限 Fourier 场，不是 Navier–Stokes 解，更不是奇解。它不排除同时使用幅值、下平面残差、方向相干、strain alignment 或真实时间演化的估计。`,
    next: String.raw`R0.71A 把主投影进一步固定为常数，并对临界投影能量方法做同范数集中检验。`,
    literature: true,
  },
];

function sourceLinks(item) {
  const key = item.code.toLowerCase().replaceAll(".", "");
  const links = [
    `<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/${key}_report-source.md">完整数学报告</a>`,
    `<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/${key}_independent_audit.md">独立数学复核</a>`,
    `<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/${key}">精确证书与 SHA-256 清单</a>`,
  ];
  if (item.literature) {
    links.splice(2, 0, `<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/${key}_literature_audit.md">文献边界审计</a>`);
  }
  return links.join(" · ");
}

function render(item) {
  const nextCode = item.next.match(/R0\.\d+[A-Z]?/)?.[0] ?? "下一节";
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="研究笔记 ${item.code}：${item.meta}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="${item.code}｜${item.title.replace("<br>", "")}">
  <meta property="og:description" content="${item.meta}">
  <meta property="og:image" content="https://kasifa.github.io/og.png">
  <title>${item.code}｜${item.title.replace("<br>", "")}</title>
  <script>window.MathJax={tex:{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
  <link rel="stylesheet" href="/bilingual.css">
  <link rel="stylesheet" href="/note-retro.css?v=0.85">
  <style>.hero h1{font-size:clamp(1.8rem,4vw,3.4rem)}</style>
  <script defer src="/i18n-en.js?v=0.86"></script>
  <script defer src="/bilingual.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <div class="topline"></div>
  <header class="bar"><div class="bar-inner">
    <a class="brand" href="/">ν · 三维 Navier–Stokes 个人研究记录</a>
    <nav><a href="#result">结论</a><a href="#identity">恒等式</a><a href="#value">价值</a><a href="#boundary">边界</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>
  </div></header>
  <main>
    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 ${item.code} · ${item.label}</div><h1>${item.title}</h1><p class="lead">${item.lead}</p></div>
      <div class="stamp"><span class="state">状态 · ${item.state}</span><strong>${item.badge}</strong><p>版本 v${item.code.slice(1)} · 2026-08-25</p><p>解析恒等式、精确生产器与独立复核已封存</p><p>本节未使用 DNS、GPU 或 DGX</p></div>
    </div></header>
    <div class="layout">
      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 本节结论</a></li><li><a href="#identity">01 · 精确账本</a></li><li><a href="#value">02 · 研究价值</a></li><li><a href="#boundary">03 · 主张边界</a></li><li><a href="#next">04 · 下一检查点</a></li><li><a href="#reproduce">05 · 复现与来源</a></li>
      </ol></aside>
      <article>
        <section id="result"><div class="section-no">00 / Exact decision</div><h2>${item.theoremTitle}</h2><p>${item.theoremText}</p><div class="equation result">\\[${item.theoremEq}\\]</div></section>
        <section id="identity"><div class="section-no">01 / Auditable ledger</div><h2>${item.detailTitle}</h2><p>${item.detailText}</p><div class="equation result">\\[${item.detailEq}\\]</div><p>${item.bridgeText}</p><div class="equation">\\[${item.bridgeEq}\\]</div>${item.bridgeTail ? `<p>${item.bridgeTail}</p>` : ""}</section>
        <section id="value"><div class="section-no">02 / Research value</div><h2>这一步改变了后续要估计的对象</h2><p>${item.value}</p></section>
        <section id="boundary"><div class="section-no">03 / Claim boundary</div><h2>证明到这里为止</h2><p>${item.boundary}</p><p>本节没有构造有限时奇性，没有证明全局光滑性，也不是对 Clay 千禧年问题的部分解答。</p></section>
        <section id="next"><div class="section-no">04 / Next gate</div><h2>${nextCode} 的检查点</h2><p>${item.next}</p></section>
        <section id="reproduce"><div class="section-no">05 / Reproducibility</div><h2>报告、复核与精确证书已经封存</h2><p>${sourceLinks(item)}</p><p><a href="/notes/${item.slug}.pdf">下载同步 PDF</a> · <a href="https://www.claymath.org/millennium/navier-stokes-equation/">Clay Mathematics Institute 正式问题说明</a></p><p>公开页只摘要报告中已经通过精确生产器、SHA-256 清单与独立数学复核的内容；页面没有添加报告之外的新主张。</p></section>
      </article>
    </div>
  </main>
  <footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>精确结果、条件结论、反例边界与开放问题分开记录。</div><div>${item.code} · 2026-08-25<br><a href="/">返回研究主页</a></div></footer>
</body>
</html>
`;
}

const root = resolve(import.meta.dirname, "..");
for (const item of releases) {
  await writeFile(resolve(root, "public", "notes", `${item.slug}.html`), render(item));
}

console.log(`generated ${releases.length} notes: ${releases[0].code}–${releases.at(-1).code}`);
