# R0.72Y 原始文献边界账本

核验日期：2026-08-28。范围限于论文原文、arXiv 原文和期刊正式页，并优先检查 Coble--He 及与本节方法边界直接相关的定理。下面记录的是一次有界原始文献核验，不是穷尽性 novelty search；“未发现”不能改写成“全球首次”。

## 结论先行

文献中已经存在 **nonautonomous forced enhanced-dissipation estimates**，也已经存在三维 Couette 邻域内含 lift-up、线性压力和向量／三角耦合的闭合结果。最直接的先例是 Wei--Zhang 的 Propositions 3.3--3.5。因此本站不得声称“非自治受迫估计”或“向量耦合增强耗散”本身尚无文献。

本轮没有在所核原始文献中找到的是同一个定理同时覆盖

\[
\boxed{
\text{critical-point collision/change of count}
+\text{Bloch-uniform fibers}
+\text{structured }H^{-1}\text{ forcing}
+\text{weak/zero rows}
+\ell^2\text{ direct sum}
+\text{complete linearized vector row}
}.
\]

这个组合缺口是 R0.72Y 可以安全使用的文献边界；它不是首创性证明。

## 1. Coble--He：固定非退化临界点的齐次非自治标量定理

- **作者／题名：** Daniel Coble, Siming He, *A Note on Enhanced Dissipation and Taylor Dispersion of Time-dependent Shear Flows*。
- **日期：** arXiv 初稿 2023-09-27，v2 2023-09-28；期刊版本发表于 2024 年。
- **原始来源：** [arXiv HTML](https://arxiv.org/html/2309.15738)，[arXiv 记录](https://arxiv.org/abs/2309.15738)。
- **确切覆盖：** 方程 (1.1) 与 Fourier 行方程 (1.6) 是齐次被动标量问题。Theorem 1.2 假设参考剪切始终具有同一固定有限数目 \(N\) 的非退化临界点、固定半径的两两不交临界邻域、\(V_yU_y\ge0\)、局部 Morse 比较、邻域外统一梯度下界、统一 \(W^{2,\infty}\) 控制及 \(\|U_{ty}\|_\infty\le\nu^{3/4}\)。结论是每个 \(k\ne0\) 的齐次衰减
  \[
  \|f_k(t)\|_2\le e\,e^{-\delta\nu^{1/2}|k|^{1/2}t}\|f_k(0)\|_2.
  \]
  Appendix Lemma A.1，公式 (A.1)--(A.3)，给出建立该结论所需的固定临界点谱不等式。
- **本站可用边界：** 可作为远离碰撞区、临界点数和形状常数保持固定时的 A1 齐次标量输入。
- **本站不可用边界：** 不含临界点碰撞或临界点数改变，不含 forcing、Bloch twist、压力、lift-up、向量系统或全物理行 direct sum。Theorem 1.2 不能直接越过 R0.72Y 的 fold。
- **置信度：** 高。

## 2. Coti Zelati--Delgadino--Elgindi：非自治传播必须控制任意起点

- **作者／题名：** Michele Coti Zelati, Matias G. Delgadino, Tarek M. Elgindi, *On the relation between enhanced dissipation time-scales and mixing rates*。
- **日期：** arXiv 初稿 2018-06-08；发表于 *Communications on Pure and Applied Mathematics* 73 (2020), 1205--1244。
- **原始来源：** [arXiv HTML](https://arxiv.org/html/1806.03258)，[arXiv 记录](https://arxiv.org/abs/1806.03258)。
- **确切覆盖：** Section 2.3 的 (2.23)--(2.24) 允许反对称算子 \(B(t)\) 随时间变化，但粘性和无粘方程均为齐次。Theorem 2.1 假设对每个起始时刻 \(\tau_0\) 都有
  \[
  \|f(t)\|_{H^{-1}}\le a(t-\tau_0)^{-p}\|f^{\tau_0}\|_{H^1},
  \]
  并导出指数为 \(q=2/(2+p)\) 的齐次增强耗散。Remark 2.2 明确区分自治问题的 \(\tau_0=0\) 与非自治问题的 arbitrary-start 假设。Section 3.3 处理含 \(I+\Delta_k^{-1}\) 的定常 Kolmogorov 主动标量算子。
- **本站可用边界：** 支持 R0.72Y 必须证明两参数传播子 \(S(t,s)\) 对任意 \(s\) 的一致估计，而不能只证明 \(S(t,0)\)。也说明某些非局部主动标量算子可以在专门 Hilbert 范数中进入抽象框架。
- **本站不可用边界：** 这里的 \(H^{-1}\) 是无粘混合输出，不是 forcing 空间；全文没有非齐次输入输出定理，也没有 collision、Bloch 纤维或完整向量行。
- **置信度：** 高。

## 3. Wei--Zhang：已有非自治受迫估计和三维向量 Couette 闭合

- **作者／题名：** Dongyi Wei, Zhifei Zhang, *Transition threshold for the 3D Couette flow in Sobolev space*。
- **日期：** arXiv 初稿 2018-03-04。
- **原始来源：** [arXiv HTML v1](https://arxiv.org/html/1803.01359v1)，[arXiv 记录](https://arxiv.org/abs/1803.01359)。
- **确切覆盖：** 扰动方程 (1.2) 是三维向量系统，显式含 lift-up 项 \((u^2,0,0)\) 和线性压力 \(\Delta p^L=-2\partial_xu^2\)。Theorem 1.1 给出 Couette 邻域内的全局稳定性和非零流向模态增强耗散。Proposition 3.1 对自治 Couette 算子处理结构化 forcing
  \[
  \mathcal L_0f=\partial_x f_1+f_2+\operatorname{div}f_3.
  \]
  Proposition 3.3 把同类估计推广到
  \[
  \mathcal L=\partial_t-\nu\Delta+V(t,y,z)\partial_x,
  \qquad V=y+\bar u^1(t,y,z),
  \]
  假设 \(\|\bar u^1\|_{H^4}+\nu^{-1}\|\partial_t\bar u^1\|_{H^2}\le c_1\)，且常数对 \(\nu,T\) 一致。其 \(X_a\) 范数含 \(\|\nabla\Delta^{-1}\partial_xf\|_{L_t^2L_x^2}\)，散度 forcing 以 \(\nu^{-1}\|f_3\|_{L_t^2L_x^2}^2\) 支付。Propositions 3.4--3.5 继续控制变量剪切、导数及带线性压力修正的算子。
- **本站可用边界：** 这是 nonautonomous forced estimate 与 vector/triangular pressure coupling 已有先例的直接证据；也提示 R0.72Y 应把源项拆成微分、零阶和散度 forcing，而不是笼统写成一个无结构 \(H^{-1}\) 源。
- **本站不可用边界：** 证明使用 \(Y=V(t,y,z)\) 和 \(\kappa=\partial_zV/\partial_yV\)，小扰动假设保证 \(\partial_yV\approx1\)。在 critical-point collision 上 \(\partial_yV=0\)，该坐标不再是微分同胚且 \(\kappa\) 可发散。论文也不含连续 Bloch 相位、临界点数改变、行耦合趋零或全物理行一致收缩。
- **置信度：** 高。

## 4. Coti Zelati--Elgindi--Widmayer：Poiseuille 主动非局部项与普通 Fourier 求和

- **作者／题名：** Michele Coti Zelati, Tarek M. Elgindi, Klaus Widmayer, *Enhanced dissipation in the Navier--Stokes equations near the Poiseuille flow*。
- **日期：** arXiv 初稿 2019-01-06；发表于 *Communications in Mathematical Physics* 378 (2020), 987--1010。
- **原始来源：** [arXiv HTML](https://arxiv.org/html/1901.01571)，[arXiv 记录](https://arxiv.org/abs/1901.01571)。
- **确切覆盖：** 方程 (1.3) 的二维线性化涡量算子含主动项
  \[
  \partial_t\omega+y^2\partial_x\omega-2\partial_x\psi-\nu\Delta\omega=0,
  \qquad \Delta\psi=\omega.
  \]
  Theorem 1.1 对每个 \(k\ne0\) 给出半群衰减，速率
  \[
  \lambda_{\nu,k}=\frac{\nu^{1/2}|k|^{1/2}}
  {1+|\log\nu|+\log|k|}.
  \]
  Corollary 1.2 在排除 \(k=0\) 后对所有整数 Fourier 模态求和，不产生额外模态计数损失；后文 Duhamel 以加权 \(L_t^1X\) 控制非线性项。
- **本站可用边界：** 说明定常非单调剪切中的主动非局部压力／速度恢复项不必摧毁增强耗散；如果逐行常数真正一致，普通正交 Fourier direct sum 本身可以无计数损失。
- **本站不可用边界：** 这是自治二维问题，排除了慢的零模态；其整数 Fourier 求和不证明连续 Bloch 相位一致性，Duhamel forcing 也不是 R0.72Y 所需的 scale-sharp \(L_t^2H^{-1}\) transfer。
- **置信度：** 高。

## 5. Bedrossian--Coti Zelati：固定有限型临界点与 \(H^{-1}\) mixing/forcing 区分

- **作者／题名：** Jacob Bedrossian, Michele Coti Zelati, *Enhanced dissipation, hypoellipticity, and anomalous small noise inviscid limits in shear flows*。
- **日期：** arXiv 初稿 2015-10-27，核验版本 v4 2017-02-27。
- **原始来源：** [arXiv HTML](https://arxiv.org/html/1510.08098)，[arXiv 记录](https://arxiv.org/abs/1510.08098)。
- **确切覆盖：** Theorem 1.1 处理定常被动标量剪切，假设固定有限数目的临界点，并按固定有限退化阶给出逐 \(k\) 齐次半群速率。公式 (1.9) 中的 \(H^{-1}\) 是无粘混合衰减。方程 (1.13)--(1.14) 与 Theorem 1.5 处理自治半群受 Hilbert--Schmidt 小噪声驱动后的随机卷积和不变测度。
- **本站可用边界：** 提供固定有限型临界点的速率基准，并要求在措辞上严格区分“\(H^{-1}\) mixing output”和“\(H^{-1}\) forcing input”。
- **本站不可用边界：** 随机 \(L^2\) 噪声结果不是确定性 nonautonomous \(L_t^2H^{-1}\to L_t^\infty L^2\) 定理；临界点集合不碰撞，也没有 Bloch 或向量系统。
- **置信度：** 高。

## 6. Benthaus--Coclite--Nobili：移动临界点不等于临界点碰撞

- **作者／题名：** Johannes Benthaus, Giuseppe Maria Coclite, Camilla Nobili, *Mixing and enhanced dissipation in a time-translating shear flow*。
- **日期：** arXiv v1，2026-03-15。
- **原始来源：** [arXiv HTML](https://arxiv.org/html/2603.14624)，[arXiv 记录](https://arxiv.org/abs/2603.14624)。
- **确切覆盖：** 论文研究 \(u=(\sin(y-ct),0)\)。Theorem 1 在有限时间窗口内给出时间平均 \(H^{-1}\) mixing，并指出完整平移周期后会出现 unmixing。Theorem 2 在 \(c=c_0\nu^\ell\)、\(\ell\in(1/3,3/4)\) 时得到齐次增强耗散，速率量级为 \(\nu^{(1+2\ell)/5}\)。整个过程中临界点保持简单、数目固定且相互分离。
- **本站可用边界：** 证明时间依赖几何可能改变混合与耗散速率；不能仅凭每个瞬时剪切的图形套用自治半群结论。
- **本站不可用边界：** 移动临界点不是临界点碰撞或生成／消失；论文没有 forcing、Bloch、向量耦合或 full-row direct sum。
- **置信度：** 中高；这是较新的 v1 预印本。

## 对 R0.72Y 可采用的表述

> Coble--He 给出固定非退化临界点结构下的齐次非自治标量估计；Wei--Zhang 则在严格单调 Couette 邻域内给出结构化非自治受迫估计，并闭合三维 lift-up、线性压力和向量耦合。但前者不含 forcing 与完整向量行，后者依赖在临界点碰撞处失效的单调坐标变换。所核文献中尚未发现同时处理退化碰撞、Bloch-uniform fibers、弱／零耦合行、scale-sharp forcing 和完整线性化 row direct sum 的定理。

不得采用以下表述：

1. “此前没有 nonautonomous forced enhanced-dissipation estimate。”
2. “此前没有 vector/triangular coupling 结果。”
3. “Poiseuille 的普通 Fourier 求和已经证明本站 Bloch-uniform direct sum。”
4. “Coble--He 的定理可以直接穿过 critical-point collision。”
5. “本轮未发现该组合”等同于“已经证明全球首创”。

因此，R0.72Y 的独立数学任务是：在不除以 \(\partial_yV\) 的框架中建立 arbitrary-start、结构化受迫的逐行传播估计，显式保留 Bloch residue、scalar damping 与 row-dependent coupling；随后再区分 strong、weak 和 zero rows，并检验完整线性化三角系统的 \(\ell^2\) direct sum。
