# R0.71I 主源文献台账：联合抛物残差、共同热流角度与时间迹缺口

**状态：**正式文献边界审计
**检索日期：**2026-08-26
**用途：**核对 R0.71I 的精确接口、已知相邻定理与不可外推边界；不作为原创性证明

## 1. 检索范围与声明

本台账只使用论文原文、作者公开稿、固定 arXiv 版本、期刊官方页面和 DOI。
关键词族覆盖 projected/Leray-projected Lamb vector、Lamb-vector
evolution、frequency-localized heat decay、\((\Delta+K^2)P_K\)、
caloric/A-Stokes approximation、common self-adjoint heat semigroup、heat
observability、initial/final trace、dissipation wavenumber、occupation、
frequency envelope、BV 与 crossing。

这是限定检索，不是系统综述。“未找到直接匹配定理”只表示本次限定范围内
未定位到结果，不能改写为不存在性、原创性、优先权或可发表性结论。正式的
新颖性判断仍需 MathSciNet、zbMATH、引文网络与领域专家复核。

R0.71I 要审计的对象是

\[
 \mathcal J_K=
 \left\langle\frac{N_K}{\sqrt Y},E\right\rangle
 +\frac{\langle P(F/\sqrt Y),P M_K\rangle}{\|C\|_2}
 -\frac{Y_t}{2Y}\left\langle\frac F{\sqrt Y},E\right\rangle,
 \tag{1.1}
\]

以及全壳、全单元、带面项的

\[
 \sum_{K,Q}K^{-2}\int z_{K,Q}^+(\mathcal J_{K,Q})^+dt.
 \tag{1.2}
\]

## 2. 投影 Lamb 向量与黏性源台账

### 2.1 Gibbon--Holm：Euler 的 Lamb/Bernoulli 向量演化

主源：[arXiv:1012.3597v1](https://arxiv.org/abs/1012.3597v1)。arXiv
页面注明将收入 2010 Warwick 会议论文集；本次限定检索未核到正式期刊版本。

论文记 \(D=\omega\times u\)、
\(E=D+\nabla(p+|u|^2/2)\)。对不可压 Euler，

\[
 u_t=-E,\qquad \operatorname{div}E=0,
 \qquad \operatorname{curl}E=\operatorname{curl}D=:\varpi,
\]

并给出 \(D_t-u\times\varpi=E\times\omega\) 及其 curl 方程。在周期盒或
全空间上，\(E=\mathbb P D\)，所以按本站符号
\(L=\mathbb P(u\times\omega)=-E=u_t\)。

**重叠：**投影 Lamb 向量与速度时间导数之间有直接主源先例。
**缺口：**该章节是 Euler 计算；不能因标题出现 NSE 就把它改写成黏性热
方程。文中没有 LP 壳、移动截断、\((\Delta+K^2)\) 不匹配、归一化角度或
时间 BV。

### 2.2 Hamman--Klewicki--Kirby：NSE 中 Lamb 散度的物质输运

主源：[作者公开稿](https://users.cs.utah.edu/~kirby/Publications/Kirby-30.pdf)，
[期刊官方页](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/on-the-lamb-vector-divergence-in-navierstokes-flows/A1DA8E28B544333001ADB1BB4E8DDF7F)，
[DOI:10.1017/S0022112008002760](https://doi.org/10.1017/S0022112008002760)。
已发表于 *Journal of Fluid Mechanics* 610 (2008), 261--284。

论文演化的是点态标量 \(\nabla\cdot(\omega\times u)\)，并保留完整物质
输运与黏性项；其式 (3.7) 还把三项精确合并为
\(-2(\nabla u):(\nabla l)\)。

**重叠：**说明 Lamb 派生量的源项需要完整合并，分拆会丢失抵消。
**缺口：**对象不是 \(\mathbb P(u\times\omega)\) 或 R0.71I 的局域 Hilbert
向量，没有分母、角度、BV、时间面或壳求和。

### 2.3 Wu--Zhou--Lu--Fan：扩散型湍流力

主源：[IBM 官方页](https://research.ibm.com/publications/turbulent-force-as-a-diffusive-field-with-vortical-sources)，
[DOI:10.1063/1.869934](https://doi.org/10.1063/1.869934)。已发表于
*Physics of Fluids* 11 (1999), 627--635。

官方摘要给出 Reynolds 平均湍流力的方程

\[
 (\partial_t-\nu\Delta)f=\nabla\cdot S.
\]

**重叠：**“Lamb 派生力 + 热算子 + 涡性源”有已发表先例。
**缺口：**\(f\) 是 Reynolds 平均/建模对象，不是确定性投影 Lamb 向量，
不能替代 R0.71I 的精确 NSE 联合残差。

## 3. 频率局部热衰减与时间迹

### 3.1 Dong Li：频率局部热衰减只给耗散间隙

主源：[arXiv:1212.0183v1](https://arxiv.org/abs/1212.0183v1)，
[期刊全文](https://intlpress.com/site/pub/files/_fulltext/journals/mrl/2013/0020/0005/MRL-2013-0020-0005-a009.pdf)，
[DOI:10.4310/MRL.2013.v20.n5.a9](https://doi.org/10.4310/MRL.2013.v20.n5.a9)。
已发表于 *Mathematical Research Letters* 20(5) (2013), 933--945。

Theorem 1.1 给出

\[
 \|e^{t\Delta}P_Nf\|_q
 \le e^{-c(q-1)q^{-2}tN^2}\|P_Nf\|_q,
 \qquad1<q<\infty.
\]

**重叠：**严格支持壳上 \(N^2\) 级耗散与热半群衰减。
**缺口：**定理没有声称 \((\Delta+K^2)P_K\) 小一阶。固定相对宽环带仍有
\(|K^2-|\xi|^2|\simeq K^2\)，因此不能由该文推出 R0.71I 所需的
\(O(K)\) 残差。

### 3.2 Ervedoza--Zuazua：热可观测性控制终端迹

主源：[期刊官方页](https://www.aimsciences.org/article/doi/10.3934/mcrf.2011.1.177)，
[作者公开稿](https://www.math.u-bordeaux.fr/~servedoza/Publis/Erv-Zuazua-Transmut-NoGCC.pdf)，
[DOI:10.3934/mcrf.2011.1.177](https://doi.org/10.3934/mcrf.2011.1.177)。
已发表于 *Mathematical Control and Related Fields* 1(2) (2011), 177--187。

Theorem 1.1 对 Dirichlet 热方程给出

\[
 \|z(T)\|_{L^2(\Omega)}^2
 \le C_T\int_0^T\int_\omega|z|^2.
\]

**重叠：**时空热体积可以控制一个时间迹。
**缺口：**这里是终端/下游迹，常数依赖时间和观测几何；R0.71I 缺的是由
未来热体积支付入口/底面迹。在 \(T\simeq K^{-2}\) 上，入口迹外乘
\(K^{-2}\) 比物理时间热体积大 \(K^2\)。

## 4. 切向热流、caloric defect 与联合 Duhamel

### 4.1 Dávila--del Pino--Wei：球值热流的切向结构

主源：[arXiv:1702.05801v2](https://arxiv.org/abs/1702.05801v2)，
[DOI:10.1007/s00222-019-00908-y](https://doi.org/10.1007/s00222-019-00908-y)。
已发表于 *Inventiones Mathematicae* 219 (2020), 345--466。

对 \(|u|=1\) 的 harmonic-map heat flow，

\[
 u_t=P_{u^\perp}\Delta u,
 \qquad (I-P_{u^\perp})\Delta u=-|\nabla u|^2u.
\]

**重叠：**径向项与切向热曲率的分离是自然抛物几何。
**缺口：**球值约束固定点态模长，没有 \(\|C\|_{L^2}\) 的零集、软
\(\varepsilon\) 缺陷或时间面，不能转写为本站 Hilbert 方向 BV。

### 4.2 Breit：\(\mathcal A\)-Stokes 近似先假设小残差

主源：[arXiv:1402.3064v3](https://arxiv.org/abs/1402.3064v3)，
[期刊官方页](https://academic.oup.com/qjmath/article/67/2/201/1752918)，
[DOI:10.1093/qmath/haw008](https://doi.org/10.1093/qmath/haw008)。已发表于
*Quarterly Journal of Mathematics* 67(2) (2016), 201--231。

Theorem 4.2 从指定测试范数中的 \(\delta\)-小非定常
\(\mathcal A\)-Stokes 弱残差得到“精确抛物解 + 小修正”。

**重叠：**完整 defect 必须放入正确范数，才可得到 caloric approximation。
**缺口：**小残差是输入，不是从 Leray 能量导出的结论；论文不提供
R0.71I 所需的一个频率阶 depletion，也不处理分母面和 BV。

### 4.3 Auscher--Frey：联合分解有效，单一平方体积映射可失败

主源：[arXiv:1412.8407v3](https://arxiv.org/abs/1412.8407v3)，
[期刊官方页](https://www.cambridge.org/core/journals/journal-of-the-institute-of-mathematics-of-jussieu/article/on-the-wellposedness-of-parabolic-equations-of-navierstokes-type-with-mathitbmo1-data/6609F544798DD0825443681143B99772)，
[DOI:10.1017/S1474748015000158](https://doi.org/10.1017/S1474748015000158)。
已发表于 *J. Inst. Math. Jussieu* 16(5) (2017), 947--985。

论文把 NSE Duhamel 算子分为三项；完整分解在 Koch--Tataru 路径空间有界，
但命题 4.1 证明其中一个指定单项在相应 tent-space 映射上失败。

**重叠：**不能把联合抛物源无条件压成一个平方热体积；不同源结构需保留。
**缺口：**负映射只针对论文中指定算子和 tent 空间，不能外推为所有联合
残差估计不可能。完整闭合依赖小 \(BMO^{-1}\) 数据，不是任意 Leray 解的
无条件 BV。

## 5. 时间--频率 occupation、时间窗与 BV

### 5.1 Cheskidov--Shvydkoy：无条件耗散波数平均不够

主源：[arXiv:1102.1944v2](https://arxiv.org/abs/1102.1944v2)，
[DOI:10.1007/s00021-014-0167-4](https://doi.org/10.1007/s00021-014-0167-4)。
已发表于 *Journal of Mathematical Fluid Mechanics* 16 (2014), 263--273。

论文证明每个 Leray--Hopf 解的动态耗散波数 \(\Lambda\in L_t^1\)，而
\(\Lambda\in L_t^{5/2}\) 足以正则。

**重叠：**这是从 Leray 预算无条件得到动态频率时间平均的主源。
**缺口：**由 \(L^1\) 和 Chebyshev 只得到 \(K^{-1}\) 占用尾，不是
\(K^{-2}\) 抛物占用，更不控制局域投影 Lamb 方向的总变差。

### 5.2 Cheskidov--Dai：振幅加权 occupation 是正则性条件

主源：[arXiv:1507.06611v6](https://arxiv.org/abs/1507.06611v6)，
[期刊官方页](https://www.cambridge.org/core/journals/proceedings-of-the-edinburgh-mathematical-society/article/abs/regularity-criteria-for-the-3d-navierstokes-and-mhd-equations/A31507CA0B1E7DE63ED324DEDA82EE54)，
[DOI:10.1017/S0013091525100813](https://doi.org/10.1017/S0013091525100813)。
已发表于 *Proceedings of the Edinburgh Mathematical Society* 68(4)
(2025), 1262--1296；旧台账若只记预印本应更新。

NSE 部分的核心条件为

\[
 \limsup_{q\to\infty}\int_{T/2}^T
 \mathbf1_{\{q\le Q_r(t)\}}
 \|\Delta_q\omega(t)\|_\infty dt\le c_r,
\]

从而排除 \(T\) 时爆破。

**重叠：**这是“时间--频率 occupation + 临界振幅权”的最接近接口。
**缺口：**该积分是正则性小量假设，不是从标准 Leray 预算推出的无权
episode 长度、方向 BV 或零面预算。

### 5.3 Luo：\(K^{-2}\) 抛物时间窗的严格先例

主源：[arXiv:1803.05569v4](https://arxiv.org/abs/1803.05569v4)，
[DOI:10.1007/s00021-019-0411-z](https://doi.org/10.1007/s00021-019-0411-z)。
已发表于 *Journal of Mathematical Fluid Mechanics* 21 (2019), article 1。

Theorem 1.1 假设

\[
 \limsup_{p\to\infty}
 \int_{T-c\lambda_p^{-2}}^T\|\nabla u_{\le p}\|_\infty dt
 \le\delta_{BKM},
\]

则解可延拓。

**重叠：**\(\lambda_p^{-2}\) 是严格的 NSE 抛物时间尺度。
**缺口：**仍需临界振幅小量；时间窗长度本身不支付 episode 数量、入口面或
\(\mathcal J_K\) 的正变差。

### 5.4 Bradshaw--Grujić：动态频率窗控制振幅

主源：[arXiv:1501.01043v2](https://arxiv.org/abs/1501.01043v2)，
[DOI:10.1007/s00205-016-1069-9](https://doi.org/10.1007/s00205-016-1069-9)。
已发表于 *Archive for Rational Mechanics and Analysis* 224 (2017),
125--133。

论文在动态频率窗内使用临界 Besov 振幅及其时间可积性给出正则性判据。

**重叠：**动态相关频带与局部 lifespan 为抛物 residence 提供先例。
**缺口：**控制的是壳振幅，不是方向、归一化相关角、零分母面或总变差。

### 5.5 Guo--Yang--Zhang：frequency envelope 给连续性，不给 BV

主源：[arXiv:2409.01031v3](https://arxiv.org/abs/2409.01031v3)，
[DOI:10.1063/5.0310556](https://doi.org/10.1063/5.0310556)。已发表于
*Journal of Mathematical Physics* 67, 031506 (2026)。

论文在可压缩 NSE 临界 Besov 框架中，以 transport--parabolic frequency
envelope 证明高频尾小量和解映射
\(S_T:U\to C([0,T];\mathbb X_p)\) 连续。

**重叠：**近期已发表的输运--抛物 frequency-envelope 先例。
**缺口：**时间连续性不推出时间 BV；输入已是临界强解空间，也不是不可压
Leray 预算。

### 5.6 Łochowski：BV--crossing 是后处理接口

主源：[arXiv:1503.01746v4](https://arxiv.org/abs/1503.01746v4)，
[DOI:10.4064/cm6583-3-2017](https://doi.org/10.4064/cm6583-3-2017)。
已发表于 *Colloquium Mathematicum* 148(2) (2017), 301--313。

Theorem 1 对 regulated 函数证明

\[
 \operatorname{TV}^c(f,[a,b])
 =\int_{\mathbb R}n_c^y(f,[a,b])dy,
\]

并有上、下穿越版本。

**重叠：**一旦标量 BV 已建立，可严格转译为积分穿越计数。
**缺口：**定理不从 PDE 产生 BV，不能反向用 crossing 公式假设目标有限。

## 6. 共同热流角度的限定检索

对共同自伴热流 \(F_t=-\nu AF\)、\(C_t=-\nu AC\)，令
\(e_F=F/\|F\|\)、\(e_C=C/\|C\|\)、
\(\gamma=\langle e_F,e_C\rangle\)。直接计算为

\[
 \gamma_t=\nu(r_F+r_C)\gamma-2\nu\langle Ae_F,e_C\rangle,
 \qquad r_F=\langle Ae_F,e_F\rangle,
 \quad r_C=\langle Ae_C,e_C\rangle.
 \tag{6.1}
\]

右端没有一般符号。以 angle/correlation/cosine similarity 和
common/self-adjoint heat semigroup 为核心的限定检索，没有定位到直接控制
(6.1) 总变差的定理。这只能记录为限定性负结果；不能称作文献中不存在共同
热流角度理论，也不能据此声明 R0.71I 两模计算的原创性。

R0.71I 的抽象两模路径进一步证明：即便入口与出口系数都为零，加权 BV 与
物理时间热体积之比仍可按 \(K^2\) 增长。正式报告中的真 NSE 2D3C 脉冲把
这个 volume-only 缺口推进到一个固定光滑径向双环 multiplier，但仍未覆盖
预选宽单环 dyadic frame。

## 7. 可安全引用与不可外推

### 可安全引用

1. 投影 Lamb 向量与速度热残差有精确 NSE 关系；Lamb 派生量的输运/扩散源
   也有已发表先例。
2. LP 壳热衰减是 \(K^2\) 级，但这不等于
   \((\Delta+K^2)P_K\) 小一阶。
3. caloric approximation 和联合 Duhamel 能处理正确范数中的小残差；该
   小量必须先由问题本身提供。
4. \(K^{-2}\) 是已发表 NSE 判据中的自然时间窗；现有判据仍携带临界振幅
   或 continuation 条件。
5. 热可观测性控制终端迹，不自动支付未来区间的入口迹。
6. frequency envelope 可给高频尾和连续性；连续性不推出 BV。
7. 标量 BV 一旦得到，可转为积分 crossing；该后处理不产生 BV。

### 不可外推

1. 不得把 Gibbon--Holm 的 Euler Lamb 公式写成黏性 NSE 热方程。
2. 不得把 Hamman 等的 Lamb 散度标量替代投影 Lamb 向量。
3. 不得由 Dong Li 的热衰减声称
   \(\|(\Delta+K^2)P_Kf\|\lesssim K\|P_Kf\|\)。
4. 不得把 harmonic-map 固定模长结构当成小分母已经解决。
5. 不得把 Auscher--Frey 的一个特定负映射扩张成所有抛物源估计不可能。
6. 不得把 Cheskidov--Dai、Luo 或 Bradshaw--Grujić 的正则性条件描述成
   任意 Leray 解的无条件 occupation/BV。
7. 不得把共同热流两模路径称为 NSE 反例；真 NSE 2D3C 结论也只针对声明的
   smooth radial two-ring component 与 heat-volume-only 控制。

## 8. 文献通道判定

本次主源没有补上 R0.71I 缺失的两个频率幂。阻尼、Duhamel、caloric
defect、动态时间窗、frequency envelope、终端可观测和 BV--crossing 分别
存在成熟工具，但它们的假设不能无损拼接为 (1.2)：

- 固定相对宽环带只给 \(O(K^2)\) 名义频率不匹配；
- 共同热流的归一化相关没有一般单调符号；
- 未来热体积不以 \(K\)-一致常数支付入口或新生成的内部脉冲；
- 已知抛物/occupation 定理需要小残差、临界路径范数或振幅条件。

因此 residual-square 与 R0.71F heat-volume-only 路线应停止。剩余有限门是：
在完整全壳台账中保持源与黏性项联合，检验

\[
 \sum_{K,Q}K^{-2}\int z_{K,Q}^+(\mathcal J_{K,Q})^+dt
\]

是否在全 tight-frame 求和后出现新的 NSE 抵消或 telescoping 预算。若估计
最终仍需 Serrin/Besov continuation、Cheskidov--Dai occupation、小分母
非退化、预设 BV 或不能由 Leray 预算得到的 defect 小量，则路线只能记录为
条件性。现有文献不支持更强的否定，也不支持正则性突破声明。
