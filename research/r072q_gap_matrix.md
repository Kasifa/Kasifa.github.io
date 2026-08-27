# R0.72Q claim--gap matrix

**日期：** 2026-08-28

**范围：** 固定最高谐波 \(M\)，任意相位系数

\[
 F_y(\phi)=\cos\phi+
 \sum_{m=2}^{M}\operatorname{Re}(\beta_m(y)e^{im\phi}),
 \qquad
 Q_j=\sup_y\sum_{m=2}^{M}m^j|\beta_m(y)|,
 \tag{0.1}
\]

并假设 \(Q_2\le1/2\)。矩阵中的“本站推导”与“一手来源”分开记录。
增强耗散步骤还使用热权重路径
\(\beta_m(y)=\beta_m(0)e^{-(m^2-1)y}\)；一般快时间系数路径不在声明
范围内。

| 主张或关口 | 所需证据 | 当前证据 | 判定 |
|---|---|---|---|
| 任意相位的一阶尾项控制 | 从 \(Q_2\) 推出不依赖相位的 \(F_y'\) 尾项界 | 本站直接不等式 \(Q_1\le Q_2/2\le1/4\) | 对声明的 fixed-\(M\) 合同已解析闭合 |
| 所有临界点统一非退化 | 在 \(F_y'=0\) 处给出显式二阶导数下界 | 本站推导 \(|\sin\phi|\le1/4\)、\(|\cos\phi|\ge\sqrt{15}/4\)，故 \(|F_y''|\ge(\sqrt{15}-2)/4\) | 已解析闭合；不是文献黑箱 |
| 每个剖面恰有两个临界点 | 排除每个临界弧中的多个根及弧外根 | 临界根只能落在 \(|\sin\phi|\le1/4\) 的两条弧；\(F_y''\) 在两弧分别严格负、严格正；周期函数至少有极大点和极小点 | 已解析闭合 |
| 临界点统一分离 | 给出只依赖合同的根间距 | 两条临界弧以 \(\arcsin(1/4)\) 定位，分离至少为 \(\pi-2\arcsin(1/4)\) | 已解析闭合 |
| Coble--He 局部 shape bounds | 在同一半径内把 \(|F_y'|\) 与到临界点的距离双边比较 | Hessian margin 与 \(Q_3\le M Q_2\le M/2\) 给出只依赖 \(M\) 的 Taylor 半径和上下界 | 对 fixed \(M\) 已解析闭合；需在正式证明中保留显式常数链 |
| 离临界区梯度 gap | 在统一临界邻域外给出 \(|F_y'|\ge c(M)>0\) | 两根定位、单调弧、固定分离及紧区间比较给出统一正下界 | 对声明合同已解析闭合；不能只引用“参数集紧”代替证明 |
| 空间高阶范数统一 | Coble--He 证明所用二、三阶导数上界 | \(Q_2\le1/2\) 且 \(M\) 固定给出 \(Q_3\le M/2\) 及相应 \(W^{3,\infty}\) 上界 | fixed \(M\) 闭合；增长 \(M\) 不闭合 |
| 临界点可以移动 | 原定理是否要求固定临界位置 | Coble--He Theorem 1.2 明确允许共享临界点 \(y_i(t)\) 随时间变化 | 文献关口闭合 |
| 慢时间条件 | 证明 \(\|U_{t\phi}\|_\infty\le\nu^{3/4}\) | 取 \(U=V\)；热权重路径给 \(\|U_{t\phi}\|_\infty\le C(M)\nu\)，对充分小 \(\nu\) 可吸收到 \(\nu^{3/4}\) | 对热权重 fixed-\(M\) 路径闭合；任意快相位调制开放 |
| 一般仿射行标签 \(q_*\) | 缩放后保留正交频率的精确标量阻尼 | cell 方程中的阻尼为 \(-|q_*|^2R^{-2}G\)，且 \(G(y)=e^{-|q_*|^2R^{-2}y}H(\varepsilon_cy)\)；该因子只强化上界 | 半群结论对固定行标签闭合；物理回填明确采用 inherited \(|q_*|=1\) |
| family-uniform \(c_{\rm ED}\) | 原证明中的 hypocoercive 参数只依赖统一 shape 数据 | Coble--He Lemma 3.1 与 (3.21)--(3.24)：依赖 \(C_*\)、\(\mathfrak C_{\rm spec}\)、\(\|U_{yy}\|_\infty\) | proof-level 抽取可闭合；原定理没有逐字声明 compact-family corollary |
| family-uniform 小粘性阈值 | Appendix A 的 cutoff 与吸收阈值在参数族上一致 | 固定根数、分离和半径允许统一 cutoffs；Lemma A.1, (A.8) 的阈值由其导数界和 shape constants 控制 | proof-level 抽取可闭合；必须写出同一 cutoff 数据 |
| 中等粘性区间 | 不能把 Coble--He 的小粘性定理外推到全部参数 | 精确 \(L^2\) contraction 可覆盖固定紧区间，并通过扩大固定 prefactor 与小粘性估计拼接 | 可按 R0.72P 的同一独立步骤闭合；不得归因于 Coble--He |
| Pignoni 对本合同的作用 | 区分定性 Morse 开性与显式合同 | Pignoni §4 保证小 \(C^2\) 扰动的定性持续性 | 只作一致性背景；不支持显式 margin 或 ED 常数 |
| 1:2 任意相位 caustic 参数式 | 联立 \(F'=F''=0\) 并消元 | 本站推导 \(z(\phi)=\frac18e^{-3i\phi}-\frac38e^{-i\phi}\) | 已解析闭合；不是 Voorhaar 的计算 |
| 1:2 caustic 隐式式与半径 | 核对曲线方程、模长范围及 real-axis cusps | 本站推导 \((|z|^2-1/16)^3=(27/1024)(\operatorname{Im}z)^2\)、\(1/4\le|z|\le1/2\)，cusps 为 \(z=\pm1/4\) | 已解析闭合；\(|z|<1/4\) 为任意相位无退化圆盘 |
| \(Q_2\le1/2\) 与 1:2 精确墙相容 | 把通用合同换成二谐波系数 | \(Q_2=4|z|\)，故合同给 \(|z|\le1/8<1/4\) | 已闭合，并保留严格安全余量 |
| Voorhaar 判别簇可否直接给 ED | 判别簇结果是否含实单位圆 margin 和耗散常数 | 原文定义并研究 Laurent 多项式 Morse discriminant/Newton polytope | 不能；本站只借用 caustic 语言 |
| 瞬时 Morse 紧性是否足够 | 检查临界点速度不可省略 | Benthaus--Coclite--Nobili 的 \(\sin(y-ct)\) 族有统一瞬时 Morse 几何，但耗散随 \(c\) 改变，快速区接近热方程 | 否；必须保留慢时间合同 |
| \(Q_2>1/2\) 的全部任意相位 | 需要新的定量几何区域或直接通量估计 | 1:2 精确 caustic 已显示系数空间存在真实退化墙；通用 \(M\) 尚无完整安全域证书 | 开放 |
| 增长 carrier count / \(M\to\infty\) | 三阶范数、根数、分离和 cutoff 常数对 \(M\) 一致 | 当前用 \(Q_3\le M Q_2\)，常数随 \(M\) 退化 | 开放 |
| 一般随时间变化的相位和系数 | 对临界点速度和可能的 mixing--unmixing 给出独立控制 | Coble--He 需要 \(\nu\)-相关慢变条件；快速平移文献显示仅有空间几何不够 | 开放 |
| 任意 common-band carrier 集 | 处理非固定整数模式、不同格结构和可能的临界点合并 | 当前合同只覆盖归一化后固定有限谐波集 \(\{1,\ldots,M\}\) 或其声明子集 | 开放 |
| 物理幅度回填 | 追踪 \(E(0)\asymp N\) 下比较的退化参数 | 对每个 active 高谐波声明 \(|\beta_m|\ge\beta_->0\)，物理比较写为 \(\lesssim_{M,\beta_-}\)、\(\asymp_{M,\beta_-}\) | 对固定 \(M,\beta_-\) 闭合；\(\beta_-\downarrow0\) 的统一物理常数不声明 |
| 一般三维 Navier--Stokes 正则性 | 从该特殊 triangular 2.5D 类得到任意光滑初值的延拓定理 | 没有此类推论 | 开放；R0.72Q 不解决千禧年问题 |

## 一手来源边界

- Coble--He 提供时变增强耗散定理，但参数族一致性是本站对证明依赖的
  抽取。
- Pignoni 提供 Morse 开性的定性背景，不提供定量合同。
- Voorhaar 提供 caustic/Morse discriminant 的代数几何语言，不提供
  1:2 实相位曲线或耗散估计。
- Bedrossian--Coti Zelati 与 Coti Zelati--Gallay 是静态退化阶数和
  hypocoercive 方法的来源，不是 R0.72Q 的时变黑箱。
- Benthaus--Coclite--Nobili 说明临界点速度是独立数据；其刚性平移正弦
  定理不覆盖热权重有限多项式。

我没有在本矩阵中作优先权或新颖性判断。正式发布仍需让解析证明、双重独立审计、
证书、图包、HTML/PDF 与发布测试保持同一版本。
