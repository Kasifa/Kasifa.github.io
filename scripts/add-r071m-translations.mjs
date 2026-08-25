import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const source = await collectSiteStrings(publicDirectory);
const current = JSON.parse(await readFile(translationPath, "utf8"));

const additions = new Map([
  [String.raw`打开 77 节完整索引`, String.raw`Open the complete 77-section index`],
  [String.raw`给出邻近的 filtered vortex-force 与 stress-divergence 公式；`, String.raw`provides the neighboring filtered vortex-force and stress-divergence formulas;`],
  [String.raw`给出能量通量的 increment/Besov 结构；`, String.raw`provide the increment/Besov structure of energy flux;`],
  [String.raw`固定 cutoff 下，viscous collar 与 localized Laplacian commutator 精确融合为 \(\nu\mathsf A_Q(\Delta+\kappa^2)W_j\)。aligned cutoff–curl numerator 逐格为零，denominator 有双侧比较；Leray 能量支付 denominator mass。`, String.raw`Under a fixed cutoff, the viscous collar and localized Laplacian commutator fuse exactly into \(\nu\mathsf A_Q(\Delta+\kappa^2)W_j\). The aligned cutoff–curl numerator vanishes cellwise, the denominator has two-sided comparability, and Leray energy pays the denominator mass.`],
  [String.raw`环带 Lamb 交换子具有精确二次速度增量表示；fixed-cell projective pairing 同时保留 resolved transport、differentiated commutator、projective denominator geometry 与 viscous annular mismatch。热包只排除这些绝对预算的普适能量嵌入，不是 NSE 解反例。`, String.raw`The annular Lamb commutator has an exact quadratic velocity-increment representation; the fixed-cell projective pairing simultaneously retains resolved transport, the differentiated commutator, projective denominator geometry, and viscous annular mismatch. The heat packets rule out only a universal energy-class embedding for these absolute budgets; they are not counterexamples among NSE solutions.`],
  [String.raw`精确 increment–projective bridge 与四行直接临界账本`, String.raw`Exact increment–projective bridge and four-row direct critical ledger`],
  [String.raw`开放接口 · R0.71N`, String.raw`Open interface · R0.71N`],
  [String.raw`控制 derivative-compatible localized paired work，并在完整无权闭合中保留额外 summability 输入。它们都不等同于本站带局部 curl 分母的 fixed-cell projective tangent。限定检索未找到从 Leray energy 单独推出完整 pairing 与四行直接账本的定理；这不是不存在性、原创性或优先权结论。`, String.raw`controls derivative-compatible localized paired work and retains additional summability inputs in the complete unweighted closure. None is equivalent to this site's fixed-cell projective tangent with a local curl denominator. The bounded search found no theorem deriving the complete pairing and four-row direct ledger from Leray energy alone; this is not a claim of nonexistence, originality, or priority.`],
  [String.raw`累计回顾与 77 节索引`, String.raw`Cumulative recap and 77-section index`],
  [String.raw`文献综述 v0.98 · 2026-08-26`, String.raw`Literature review v0.98 · 2026-08-26`],
  [String.raw`我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.71M 只列为研究笔记。我不把计算或笔记外推成正则性定理。`, String.raw`I list published theorems as known results, mark 2026 preprints separately, and classify this site's R0.69P–R0.71M work only as research notes. I do not extrapolate computations or notes into regularity theorems.`],
  [String.raw`我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71M 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。`, String.raw`I also maintain a systematic review page that places classical theory, five main literature branches, the candidate blow-up exclusion tree, progress from 2019—2026, and this site's R0.69P–R0.71M route on one map. Historical nodes R0.61–R0.69O remain in the cumulative recap.`],
  [String.raw`下一节仍留在 fixed cells，从整个 \(\mathcal J_Q\) 同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，再代入 radial identity 和局部 filtered-enstrophy 表示；在此之前不取正部或逐行绝对值。`, String.raw`The next section remains on fixed cells and, from the complete \(\mathcal J_Q\), simultaneously retains \(B_{Q,t}\), \(d_{Q,t}\), and \(Y_t\), then substitutes the radial identity and the local filtered-enstrophy representation; no positive part or rowwise absolute value is taken before that.`],
  [String.raw`中。R0.69P–R0.71M 从有符号物理环带经过 projected-Lamb 热体积、matched-cell heat gap 与 viscous fusion，走到 exact increment–projective bridge。R0.71M 给出 annular-filter Lamb commutator 的精确二次速度增量公式和完整 fixed-cell pairing；当前直接绝对估计产生四行临界充分账本。热包排除从 Leray energy 到所测试绝对临界预算的普适嵌入，但不是 NSE 解反例。保留下来的结果都不是全局正则性结论。`, String.raw`. From R0.69P through R0.71M, the route moves from signed physical annuli through projected-Lamb heat volume, the matched-cell heat gap, and viscous fusion to the exact increment–projective bridge. R0.71M gives an exact quadratic velocity-increment formula for the annular-filter Lamb commutator and the complete fixed-cell pairing; the current direct absolute estimate produces a four-row sufficient critical ledger. The heat packets rule out a universal embedding from Leray energy into the tested absolute critical budgets, but they are not counterexamples among NSE solutions. None of the retained results is a global-regularity conclusion.`],
  [String.raw`R0.71M 的一手文献边界`, String.raw`Primary-source boundary for R0.71M`],
  [String.raw`R0.71M 关闭了什么，R0.71N 只检查什么`, String.raw`What R0.71M closes, and what R0.71N alone will test`],
  [String.raw`R0.71M 没有把“增量交换子”当作自动支付。它先证明 exact increment identity，再把 projective pairing 完整移过固定 cutoff。直接 Cauchy 后出现四行临界消费者，其中 differentiated commutator 没有可直接使用的上频率支撑；热包又说明所测试的绝对临界预算不由能量类普适给出。这是 checked direct-route boundary，不是一般 signed NSE no-go。R0.71N 只检查完整标量内是否还有第二次精确融合，并继续用下面六条筛选。`, String.raw`R0.71M does not treat an “increment commutator” as an automatic payment. It first proves the exact increment identity and then moves the complete projective pairing through the fixed cutoff. Direct Cauchy produces four critical consumers, while the differentiated commutator has no directly usable upper-frequency support; the heat packets further show that the tested absolute critical budgets do not follow universally from the energy class. This is a checked direct-route boundary, not a general no-go result for signed NSE structure. R0.71N tests only whether the complete scalar contains a second exact fusion and continues to use the six filters below.`],
  [String.raw`00 · 本节判断`, String.raw`00 · Section verdict`],
  [String.raw`01 · 固定对象`, String.raw`01 · Fixed objects`],
  [String.raw`02 · 增量恒等式`, String.raw`02 · Increment identity`],
  [String.raw`03 · 频率支撑`, String.raw`03 · Frequency support`],
  [String.raw`04 · 投影配对`, String.raw`04 · Projective pairing`],
  [String.raw`05 · 径向与局部 enstrophy`, String.raw`05 · Radial and local enstrophy identities`],
  [String.raw`06 · 四行临界账本`, String.raw`06 · Four-row critical ledger`],
  [String.raw`07 · 直接插入缺口`, String.raw`07 · Direct-insertion gap`],
  [String.raw`08 · 热包分离`, String.raw`08 · Heat-packet separation`],
  [String.raw`09 · 半导数差`, String.raw`09 · Half-derivative gap`],
  [String.raw`10 · 独立审计`, String.raw`10 · Independent audit`],
  [String.raw`11 · 正式附图`, String.raw`11 · Publication figure`],
  [String.raw`12 · 文献边界`, String.raw`12 · Literature boundary`],
  [String.raw`13 · 研究价值`, String.raw`13 · Research value`],
  [String.raw`14 · 下一步`, String.raw`14 · Next step`],
  [String.raw`15 · 主张边界`, String.raw`15 · Claim boundary`],
  [String.raw`16 · 复现与来源`, String.raw`16 · Reproduction and sources`],
  [String.raw`版本 v0.71M · 2026-08-26`, String.raw`Version v0.71M · 2026-08-26`],
  [String.raw`半导数差`, String.raw`Half-derivative gap`],
  [String.raw`本节是固定小区直接证明路线的审计，不是千禧年问题的解答`, String.raw`This section audits the fixed-cell direct proof route; it is not a solution to the Millennium problem`],
  [String.raw`本节完成三件可逐行核对的工作：第一，推出环带滤波 Lamb 交换子的精确速度增量公式；第二，把固定小区投影切向配对重写成没有外层 cutoff–curl 的局部积分；第三，明确记录直接 Cauchy 以后出现的四行尺度临界消费者。`, String.raw`This section completes three tasks that can be checked line by line: first, it derives an exact velocity-increment formula for the annular-filter Lamb commutator; second, it rewrites the fixed-cell projective-tangent pairing as a local integral with no outer cutoff–curl; third, it records explicitly the four scale-critical consumers produced by direct Cauchy.`],
  [String.raw`标准能量插值在同一可容许尺度上恰少半阶`, String.raw`Standard energy interpolation is exactly half a derivative short at the same admissible scale`],
  [String.raw`表面的正平方与 \(d_{Q,t}\) 是同一配对的两种写法`, String.raw`The apparent positive square and \(d_{Q,t}\) are two representations of the same pairing`],
  [String.raw`不能越界解释`, String.raw`Boundary on interpretation`],
  [String.raw`出发，同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，再代入径向恒等式和 \(B_Q\) 的局部滤波 enstrophy 表示，最后才取正部或绝对值。可接受的结果有两个：得到第二个精确标量融合；或者证明留下一个明确的有符号 residual。因为局部滤波 enstrophy 与 \(d_Q\) 是不同状态量，二次融合不能预设。`, String.raw`Starting from this expression, retain \(B_{Q,t}\), \(d_{Q,t}\), and \(Y_t\) simultaneously, then substitute the radial identity and the local filtered-enstrophy representation of \(B_Q\), and only afterward take a positive part or an absolute value. Two outcomes are acceptable: obtain a second exact scalar fusion, or prove that an explicit signed residual remains. Because local filtered enstrophy and \(d_Q\) are different state variables, a second fusion cannot be assumed in advance.`],
  [String.raw`但当前直接切向估计仍不闭合`, String.raw`but the current direct tangent estimate still does not close`],
  [String.raw`的 filtered vortex force 与 stress-divergence increment 公式是最近的经典结构，但它使用 \(\overline{u\times\omega}-\bar u\times\bar\omega\)，而增量式直接写给 \(-\operatorname{div}\tau\)；第二因子和滤波方式与本文 \(T_j(u\times\omega)-u\times T_j\omega\) 不同。`, String.raw`'s filtered vortex-force and stress-divergence increment formulas are the nearest classical structures, but they use \(\overline{u\times\omega}-\bar u\times\bar\omega\), while the increment formula is written directly for \(-\operatorname{div}\tau\); the second factor and filtering operation differ from \(T_j(u\times\omega)-u\times T_j\omega\) here.`],
  [String.raw`的 Theorem 9.3 控制局部配对功 \(\Omega_\ell\cdot\operatorname{curl}\operatorname{div}R_\ell\)，不是该微分场的独立范数。其 Theorem 8.7 给出 reassigned-annulus 的序列闭合；完整无权闭合还需要 full far-field、\(\widetilde\Sigma_S\) 与 residual summability。`, String.raw`'s Theorem 9.3 controls the local paired work \(\Omega_\ell\cdot\operatorname{curl}\operatorname{div}R_\ell\), not an independent norm of that differentiated field. Its Theorem 8.7 gives a sequential closure for reassigned annuli; complete unweighted closure still requires the full far-field term, \(\widetilde\Sigma_S\), and residual summability.`],
  [String.raw`独立检查器使用固定五组无散 Fourier 模、order-64 周期网格、紧环带乘子和正的三角 cutoff，不导入 exact producer。所有乘积在物理空间计算，导数在 Fourier 空间计算；没有随机采样、拟合、DNS 或时间推进。`, String.raw`The independent checker uses five fixed groups of divergence-free Fourier modes, an order-64 periodic grid, a compact annular multiplier, and a positive trigonometric cutoff; it does not import the exact producer. All products are computed in physical space and all derivatives in Fourier space; there is no random sampling, fitting, DNS, or time integration.`],
  [String.raw`独立实现同时检查增量、融合、投影与径向配对`, String.raw`The independent implementation checks the increment, fusion, projective, and radial pairings simultaneously`],
  [String.raw`对 \(0\le\theta\le1\)、\(2\le p\le\infty\)，标准能量插值与 Sobolev/Bernstein 嵌入给出`, String.raw`For \(0\le\theta\le1\) and \(2\le p\le\infty\), standard energy interpolation and Sobolev/Bernstein embedding give`],
  [String.raw`给出能量通量的增量/Besov 结构；它们不是带局部 curl 分母的固定小区投影切向。`, String.raw`give the increment/Besov structure of energy flux; these are not fixed-cell projective tangents with a local curl denominator.`],
  [String.raw`固定无散紧支撑轮廓 \(\Phi\)，令`, String.raw`Fix a compactly supported divergence-free profile \(\Phi\), and set`],
  [String.raw`环带的是融合后的 \(G_j\)，不是分裂出的交换子`, String.raw`The fused \(G_j\), not the separated commutator, is annular`],
  [String.raw`记 \(A_j=\operatorname{curl}(u\times W_j)\)、\(D_j=\operatorname{curl}\mathcal R_j\)。两项单独都不必落在第 \(j\) 个环带；只有`, String.raw`Set \(A_j=\operatorname{curl}(u\times W_j)\) and \(D_j=\operatorname{curl}\mathcal R_j\). Neither term separately need lie in the \(j\)-th annulus; only`],
  [String.raw`价值在于把“增量可能支付切向”压成一个可证伪的有限接口`, String.raw`The value lies in compressing “increments may pay the tangent” into a falsifiable finite interface`],
  [String.raw`交换子恰好是两个带符号的二次速度增量项`, String.raw`The commutator is exactly the sum of two signed quadratic velocity-increment terms`],
  [String.raw`经典增量结构相邻，但没有一篇已查论文替代当前完整对象`, String.raw`Classical increment structures are adjacent, but no paper reviewed replaces the complete object here`],
  [String.raw`精确恒等式、有限审计与开放缺口分开记录。`, String.raw`Exact identities, finite audits, and open gaps are recorded separately.`],
  [String.raw`精确切向 envelope`, String.raw`Exact tangent envelope`],
  [String.raw`精确增量恒等式、固定小区投影配对、四行临界账本、热包函数空间分离及下一步完整标量融合。`, String.raw`The exact increment identity, fixed-cell projective pairing, four-row critical ledger, heat-packet function-space separation, and the next complete-scalar fusion test.`],
  [String.raw`径向恒等式`, String.raw`Radial identity`],
  [String.raw`两个符号分别是“正、负”；不需要假设 \(\int\phi_j=1\)。因此`, String.raw`The two signs are respectively positive and negative; no assumption \(\int\phi_j=1\) is needed. Therefore`],
  [String.raw`频率融合`, String.raw`Frequency fusion`],
  [String.raw`期刊附图三格式与视觉 QA：PASS`, String.raw`Publication figure in three formats and visual QA: PASS`],
  [String.raw`取 \(\delta_hu(x)=u(x-h)-u(x)\)，并定义`, String.raw`Set \(\delta_hu(x)=u(x-h)-u(x)\), and define`],
  [String.raw`全部 projective 公式只在 \(d_Q>0\) 的经典时间分支上陈述。这里 \(P_Q\) 是 \(L^2\) Hilbert 空间中的余秩一投影，不是逐点矩阵。`, String.raw`All projective formulas are stated only on classical time branches where \(d_Q>0\). Here \(P_Q\) is a corank-one projection in the \(L^2\) Hilbert space, not a pointwise matrix.`],
  [String.raw`热包分离`, String.raw`Heat-packet separation`],
  [String.raw`四行依次是 resolved transport、微分增量交换子、投影分母几何和黏性环带失配。将滤波长度和小区 cutoff 一同缩放时，这四个时间积分在形式局部 Euclidean NSE 缩放下都是临界的；这不是固定 \(\mathbb T^3\) 与固定 cutoff 的连续对称性，也不是能量估计。`, String.raw`The four rows are, in order, resolved transport, the differentiated increment commutator, projective denominator geometry, and viscous annular mismatch. When the filter length and cell cutoff are scaled together, all four time integrals are critical under formal local Euclidean NSE scaling; this is neither a continuous symmetry on fixed \(\mathbb T^3\) with a fixed cutoff nor an energy estimate.`],
  [String.raw`四行账本`, String.raw`Four-row ledger`],
  [String.raw`四行直接上界`, String.raw`Four-row direct upper bound`],
  [String.raw`所以一个匹配的四次增量缺陷控制 \(\kappa_j^{-1}\|\mathcal R_j\|_2^2\) 型预算；而上面的直接切向账本含 \(\kappa_j^{-3}\|\operatorname{curl}\mathcal R_j\|_2^2\)。若有 \(\operatorname{supp}\widehat{\mathcal R_j}\subset B(0,C\kappa_j)\)，上 Bernstein 可以比较两者；但一般没有这个上支撑。`, String.raw`Thus a matched quartic increment defect controls a budget of type \(\kappa_j^{-1}\|\mathcal R_j\|_2^2\), whereas the direct tangent ledger above contains \(\kappa_j^{-3}\|\operatorname{curl}\mathcal R_j\|_2^2\). If \(\operatorname{supp}\widehat{\mathcal R_j}\subset B(0,C\kappa_j)\), an upper Bernstein estimate can compare them; in general, however, that upper support is absent.`],
  [String.raw`特别在 \(p=q=3\) 时，能量支付的是 \(L_t^3\dot B_{3,3}^{1/6}\)，而一个抛物临界的三次速度消费者具有 \(2/3\) 指标。这个 \(2/3\)、Onsager 的 \(1/3\) 与 Yu 四次缺陷的量纲对象必须分开。`, String.raw`In particular, when \(p=q=3\), energy pays \(L_t^3\dot B_{3,3}^{1/6}\), while a parabolically critical cubic velocity consumer has index \(2/3\). This \(2/3\), Onsager's \(1/3\), and the dimensional object in Yu's quartic defect must be kept distinct.`],
  [String.raw`同时，标量 numerator 与局部滤波 enstrophy 满足`, String.raw`Meanwhile, the scalar numerator and local filtered enstrophy satisfy`],
  [String.raw`同一 \(p,q=2/\theta\) 上的三维 NSE 临界指标是`, String.raw`At the same \(p,q=2/\theta\), the three-dimensional NSE critical index is`],
  [String.raw`同一式子还等价于`, String.raw`The same formula is also equivalent to`],
  [String.raw`统一能量的热包仍可使三个绝对临界预算发散`, String.raw`Uniformly energy-bounded heat packets can still make three absolute critical budgets diverge`],
  [String.raw`投影配对`, String.raw`Projective pairing`],
  [String.raw`图 R0.71M。A、B 是同一个固定光滑 Fourier 见证的确定性诊断，不是连续符号证书；四行是当前直接 Cauchy 产生的充分账本，不是必要条件。C 是解析热包缩放，所画系数在 (r=1) 归一化；热包不是 NSE 解。D 的虚线和叉号只表示当前直接插入失败，R0.71N 仍检查完整标量的有符号融合。`, String.raw`Figure R0.71M. A and B are deterministic diagnostics of the same fixed smooth Fourier witness, not a continuous-sign certificate; the four rows form a sufficient ledger produced by the current direct Cauchy estimate, not necessary conditions. C is analytic heat-packet scaling, with the plotted coefficients normalized at (r=1); the heat packets are not NSE solutions. The dashed line and cross in D indicate only that the current direct insertion fails; R0.71N still tests the signed fusion of the complete scalar.`],
  [String.raw`外层 cutoff–curl 可以精确移走`, String.raw`The outer cutoff–curl can be removed exactly`],
  [String.raw`未证明：四行账本是必要条件、完整 \(\mathcal J_Q\) 的符号、faces、refresh、moving cells、无限 frame–cell 极限、继续性、全局正则性或有限时破裂。`, String.raw`Not proved: that the four-row ledger is necessary, the sign of the complete \(\mathcal J_Q\), faces, refresh, moving cells, the infinite frame–cell limit, continuation, global regularity, or finite-time breakdown.`],
  [String.raw`未证明：已知增量缺陷在逻辑上不能控制 signed tangent。`, String.raw`Not proved: that known increment defects cannot logically control the signed tangent.`],
  [String.raw`我保留 R0.71L 的固定小区和黏性融合，不进入 faces、refresh 或 moving cells。环带滤波 Lamb 交换子确实有精确的二次速度增量公式；完整投影配对也能移走外层 cutoff–curl。但把结果直接逐行绝对化，会留下 resolved transport、增量交换子、投影几何与黏性失配四个临界消费者。已知四次增量缺陷不能通过当前 Bernstein 步骤直接支付其中的微分交换子行，因为该分裂行没有一般的 \(O(\kappa_j)\) 上频率支撑。`, String.raw`I retain the fixed cells and viscous fusion of R0.71L and do not enter faces, refresh, or moving cells. The annular-filter Lamb commutator does have an exact quadratic velocity-increment formula, and the complete projective pairing can remove the outer cutoff–curl. But taking rowwise absolute values directly leaves four critical consumers: resolved transport, the increment commutator, projective geometry, and viscous mismatch. Known quartic increment defects cannot directly pay the differentiated commutator row through the current Bernstein step because that separated row has no general \(O(\kappa_j)\) upper-frequency support.`],
  [String.raw`下一对象：完整 \(\mathcal J_Q\) 的二次标量融合`, String.raw`Next object: a second scalar fusion of the complete \(\mathcal J_Q\)`],
  [String.raw`下一节不只拼接 projective pairing 与局部 enstrophy。它必须从`, String.raw`The next section will not merely splice the projective pairing to local enstrophy. It must start from`],
  [String.raw`先固定滤波、小区与 Hilbert 投影`, String.raw`First fix the filter, cell, and Hilbert-space projection`],
  [String.raw`限定两轮一手检索没有找到从 Leray energy 单独推出本文 fixed-cell normalized projective pairing、局部分母和全部直接消费者的定理。这是 bounded search 的边界，不是不存在性、原创性或优先权结论。`, String.raw`The bounded two-round primary-source search found no theorem deriving the fixed-cell normalized projective pairing, local denominator, and all direct consumers here from Leray energy alone. This is the boundary of a bounded search, not a claim of nonexistence, originality, or priority.`],
  [String.raw`研究笔记 R0.71M · EXACT INCREMENTS · FOUR-ROW DIRECT LEDGER · WHOLE-SCALAR GATE`, String.raw`Research note R0.71M · EXACT INCREMENTS · FOUR-ROW DIRECT LEDGER · WHOLE-SCALAR GATE`],
  [String.raw`研究笔记 R0.71M：环带滤波 Lamb 交换子有精确速度增量公式；固定小区投影配对也可精确重组。当前直接绝对值估计产生四行临界账本，已知增量缺陷因上频率支撑缺口不能直接闭合这条证明路线。`, String.raw`Research note R0.71M: the annular-filter Lamb commutator has an exact velocity-increment formula, and the fixed-cell projective pairing can also be reorganized exactly. The current direct absolute-value estimate produces a four-row critical ledger; because of the upper-frequency-support gap, known increment defects cannot directly close this proof route.`],
  [String.raw`已关闭的是这一条直接插入，不是增量信息本身`, String.raw`What is closed is this direct insertion, not increment information itself`],
  [String.raw`已证明：标准能量类不普适嵌入本文测试的三个绝对临界预算；该热包论证不是 NSE 解反例。`, String.raw`Established: the standard energy class does not embed universally into the three absolute critical budgets tested here; the heat-packet argument is not a counterexample among NSE solutions.`],
  [String.raw`已证明：当前直接绝对值估计的四行充分临界账本。`, String.raw`Established: the four-row sufficient critical ledger from the current direct absolute-value estimate.`],
  [String.raw`已证明：固定小区 projective pairing 与 radial identity。`, String.raw`Established: the fixed-cell projective pairing and radial identity.`],
  [String.raw`已证明：环带滤波 Lamb 交换子的精确二次速度增量公式。`, String.raw`Established: the exact quadratic velocity-increment formula for the annular-filter Lamb commutator.`],
  [String.raw`已证明：resolved transport 与交换子 curl 融合成环带 \(G_j\)，分裂行没有一般上频率支撑。`, String.raw`Established: resolved transport and the curl of the commutator fuse into the annular \(G_j\), while the separated row has no general upper-frequency support.`],
  [String.raw`已知四次缺陷控制未微分交换子；当前消费者含 curl`, String.raw`The known quartic defect controls the undifferentiated commutator; the current consumer contains a curl`],
  [String.raw`已知增量缺陷与本文显示的 Cauchy/Bernstein 步骤合在一起，不能闭合固定小区切向。这只是已检查证明路线的结论。本文没有构造“缺陷有界而切向无界”的反例，因此没有证明增量缺陷在逻辑上不能蕴含切向估计。`, String.raw`Known increment defects, combined with the Cauchy/Bernstein step displayed here, do not close the fixed-cell tangent estimate. This conclusion applies only to the proof route examined. No counterexample with a bounded defect and an unbounded tangent is constructed here, so this does not prove that an increment defect cannot logically imply a tangent estimate.`],
  [String.raw`有限判断`, String.raw`Finite verdict`],
  [String.raw`再记`, String.raw`Also set`],
  [String.raw`在 \(\mathbb T^3\) 上采用归一化 Haar 测度。令`, String.raw`Use normalized Haar measure on \(\mathbb T^3\). Set`],
  [String.raw`在匹配抛物窗口上，Yu 型四次微分兼容缺陷、velocity square-Carleson mass 分别按 \(r^{-2}\)、\(r^{-1}\) 增长。若轮廓满足`, String.raw`On the matched parabolic window, the Yu-type quartic derivative-compatible defect and the velocity square-Carleson mass grow respectively like \(r^{-2}\) and \(r^{-1}\). If the profile satisfies`],
  [String.raw`则对每个 \(T>0\) 都有精确热能量等式`, String.raw`then for every \(T>0\) there is an exact heat-energy identity`],
  [String.raw`增量公式`, String.raw`Increment formula`],
  [String.raw`增量公式直接给出`, String.raw`The increment formula gives directly`],
  [String.raw`增量恒等式相对残差`, String.raw`Relative residual of the increment identity`],
  [String.raw`增量交换子可以精确写出，`, String.raw`The increment commutator admits an exact representation,`],
  [String.raw`这个结果没有缩小所有潜在奇性解的集合，也没有得到无条件继续性判据。它的实际意义是关闭一条看似自然但缺关键 Bernstein 步骤的证明路径，并把下一次审计集中到完整有符号标量是否存在第二次精确消去。`, String.raw`This result does not narrow the set of all potential singular solutions and does not yield an unconditional continuation criterion. Its practical value is to close a seemingly natural proof route that lacks a crucial Bernstein step and to focus the next audit on whether the complete signed scalar contains a second exact cancellation.`],
  [String.raw`这里局部滤波 enstrophy \(\frac12\int\chi_Q|W_j|^2\) 与 projective 状态 \(d_Q=\|\operatorname{curl}(\chi_QW_j)\|_2^2\) 不是同一个量，不能在下一步中默认为二次融合。`, String.raw`Here the local filtered enstrophy \(\frac12\int\chi_Q|W_j|^2\) and the projective state \(d_Q=\|\operatorname{curl}(\chi_QW_j)\|_2^2\) are not the same quantity, so a second fusion cannot be assumed in the next step.`],
  [String.raw`这里证明的是当前直接 Bernstein 插入没有可用步骤，不是“一个增量缺陷永远不能控制切向”。更深的融合估计、NSE 特有消去或另一种配对仍然可能存在。`, String.raw`What is proved here is that the current direct Bernstein insertion has no available step, not that “an increment defect can never control the tangent.” A deeper fused estimate, an NSE-specific cancellation, or another pairing may still exist.`],
  [String.raw`这是完整 fixed-cell pairing。它消除了最外层的 cutoff–curl，却没有把切向只化成增量交换子。`, String.raw`This is the complete fixed-cell pairing. It removes the outermost cutoff–curl but does not reduce the tangent to the increment commutator alone.`],
  [String.raw`这些是一个有限光滑见证的 binary64 恒等式诊断。解析部分负责普适恒等式；数值部分不证明连续时间符号或一般 Leray 解估计。`, String.raw`These are binary64 identity diagnostics for a finite smooth witness. The analytic part establishes the universal identities; the numerical part does not prove a continuous-time sign or an estimate for general Leray solutions.`],
  [String.raw`正分支切向有精确表示`, String.raw`The positive-branch tangent has an exact representation`],
  [String.raw`正式附图把精确配对、四行账本与函数空间边界放在同一页`, String.raw`The publication figure places the exact pairings, four-row ledger, and function-space boundary on one page`],
  [String.raw`直接 Cauchy 给出`, String.raw`Direct Cauchy gives`],
  [String.raw`直接 Cauchy/Bernstein 插入不闭合；完整有符号标量融合开放`, String.raw`The direct Cauchy/Bernstein insertion does not close; fusion of the complete signed scalar remains open`],
  [String.raw`直接路线缺口`, String.raw`Direct-route gap`],
  [String.raw`重新得到环带支撑。独立 Fourier 见证中，\(\mathcal R_j\) 有 \(57.17\%\) 的能量位于声明输出带上缘 \(1.45\kappa_j\) 以上。这个数值只诊断一个光滑见证；结构性事实是：\(u\times W_j\) 中未滤波的 \(u\) 可以带任意高频，所以一般没有 \(O(\kappa_j)\) 的上频率支撑。`, String.raw`recovers annular support. In the independent Fourier witness, \(\mathcal R_j\) has \(57.17\%\) of its energy above the stated output band's upper edge \(1.45\kappa_j\). This number diagnoses only one smooth witness; the structural fact is that \(u\times W_j\), through its unfiltered factor \(u\), can carry arbitrarily high frequencies, so no \(O(\kappa_j)\) upper-frequency support exists in general.`],
  [String.raw`周期分部积分给出精确恒等式`, String.raw`Periodic integration by parts gives the exact identity`],
  [String.raw`逐行绝对化会产生四个充分消费者`, String.raw`Taking rowwise absolute values produces four sufficient consumers`],
  [String.raw`状态 · R0.71M 精确恒等式与双路径审计完成`, String.raw`Status · R0.71M exact identities and dual-route audit complete`],
  [String.raw`curl 的自伴性与秩一投影代数给出`, String.raw`Self-adjointness of curl and rank-one projection algebra give`],
  [String.raw`normalized projected-Lamb 积分也按 \(r^{-1}\) 增长。这只排除了从标准能量类到这些绝对临界预算的普适函数空间嵌入。热包是线性热流，不是非线性 NSE 解族，因此不是 NSE 反例。`, String.raw`The normalized projected-Lamb integral also grows like \(r^{-1}\). This rules out only a universal function-space embedding from the standard energy class into these absolute critical budgets. The heat packets are linear heat flows, not a family of nonlinear NSE solutions, and therefore are not NSE counterexamples.`],
  [String.raw`projective pairing 残差`, String.raw`Projective-pairing residual`],
  [String.raw`R0.71L 留下的“critical increment bridge”不再是泛泛设想。R0.71M 已经写出精确交换子、完整 fixed-cell pairing、四行直接消费者和上支撑缺口。以后若继续走增量路线，必须说明支付的是未微分 \(\mathcal R_j\)、微分 \(D_j\)，还是融合后的 \(G_j\)，不能用“环带交换子”一词跳过频率支撑。`, String.raw`The “critical increment bridge” left by R0.71L is no longer a vague proposal. R0.71M writes down the exact commutator, complete fixed-cell pairing, four direct consumers, and upper-support gap. Any future increment route must state whether it pays the undifferentiated \(\mathcal R_j\), the differentiated \(D_j\), or the fused \(G_j\); the phrase “annular commutator” cannot be used to skip the frequency-support issue.`],
  [String.raw`R0.71M 精确增量交换子、四行直接切向账本、热包尺度分离与完整标量融合门槛`, String.raw`R0.71M exact increment commutator, four-row direct tangent ledger, heat-packet scale separation, and complete-scalar fusion gate`],
  [String.raw`R0.71M｜增量交换子的精确公式与四行切向边界`, String.raw`R0.71M | Exact formula for the increment commutator and the four-row tangent boundary`],
  [String.raw`R0.71N 从完整 \(\mathcal J_Q\) 出发，同时保留三个时间导数`, String.raw`R0.71N starts from the complete \(\mathcal J_Q\) and retains all three time derivatives simultaneously`],
  [String.raw`radial pairing 相对残差`, String.raw`Relative radial-pairing residual`],
  [String.raw`resolved / commutator 融合残差`, String.raw`Resolved/commutator fusion residual`],
  [String.raw`02 · 77 节完整索引`, String.raw`02 · Complete 77-section index`],
  [String.raw`标准能量类与所测试 absolute increment、Carleson、normalized projected-Lamb budgets 的热包函数空间分离；该序列是线性热流，不是 NSE 解反例。`, String.raw`Heat-packet function-space separation between the standard energy class and the tested absolute increment, Carleson, and normalized projected-Lamb budgets; this sequence consists of linear heat flows, not counterexamples among NSE solutions.`],
  [String.raw`打开最新节点 R0.71M`, String.raw`Open the latest node, R0.71M`],
  [String.raw`固定 cutoff 的 viscous collar 与 localized Laplacian commutator 精确融合；aligned cutoff–curl numerator 逐格为零，Leray 能量支付 denominator mass。`, String.raw`The viscous collar and localized Laplacian commutator for a fixed cutoff fuse exactly; the aligned cutoff–curl numerator vanishes cellwise, and Leray energy pays the denominator mass.`],
  [String.raw`回顾截止节点：R0.71M`, String.raw`Recap endpoint: R0.71M`],
  [String.raw`回顾截止时公开笔记：137`, String.raw`Public notes at the recap endpoint: 137`],
  [String.raw`截至 R0.71M，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 77 个节点解释成对千禧年问题完成了某个比例。`, String.raw`Through R0.71M, there is no new unconditional continuation criterion, no narrowing of the set of all potential singular solutions, and no proof of finite-time breakdown. The 77 nodes cannot be interpreted as completing some percentage of the Millennium problem.`],
  [String.raw`可接受的结果有两个：得到第二个精确标量融合，或者留下一个公式明确、符号仍开放的 residual。局部 filtered enstrophy 与 \(d_Q\) 是不同状态量，所以两种结果都不能预设；审计完成前不进入 denominator faces 和 moving partitions。`, String.raw`Two outcomes are acceptable: obtain a second exact scalar fusion, or retain an explicitly formulated residual whose sign remains open. Local filtered enstrophy and \(d_Q\) are different state variables, so neither outcome can be assumed; denominator faces and moving partitions are deferred until this audit is complete.`],
  [String.raw`累计回顾 · R0.61–R0.71M · 2026-08-26`, String.raw`Cumulative recap · R0.61–R0.71M · 2026-08-26`],
  [String.raw`目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、它的有界重叠局部化，以及 fixed-cell denominator mass 的能量支付。R0.71G–M 把直接路线继续收缩：residence 不足，逐壳正部没有免费 telescope，fixed matched cells 排除同一 heat endpoint，raw collar 融合回 signed row，increment route 又被压成四个明确消费者。完整 \(\mathcal J_Q\) 是否还有第二次 signed fusion、faces 和 refresh 仍未闭合。`, String.raw`The most substantive unconditional positive results remain the Leray-energy-level projected-Lamb heat volume, its bounded-overlap localization, and the energy payment of fixed-cell denominator mass. R0.71G–M further narrows the direct route: residence is insufficient, shellwise positive parts provide no free telescope, fixed matched cells rule out the same heat endpoint, the raw collar fuses back into the signed row, and the increment route is compressed into four explicit consumers. Whether the complete \(\mathcal J_Q\) has a second signed fusion remains open, as do faces and refresh.`],
  [String.raw`十二个阶段、77 个节点：从约化递推到 projected-Lamb 局部热打包，再到固定匹配小区 heat gap、黏性融合和 exact increment–projective bridge。`, String.raw`Twelve phases and 77 nodes: from reduced recurrences to projected-Lamb local heat packing, then to the fixed matched-cell heat gap, viscous fusion, and the exact increment–projective bridge.`],
  [String.raw`收录节点：77`, String.raw`Nodes included: 77`],
  [String.raw`下一步仍不进入 faces、refresh 或 moving cells，也不把四行直接账本逐项绝对化。R0.71N 从完整 \(\mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q\) 出发，同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，再代入 radial identity 和 \(B_Q\) 的局部 filtered-enstrophy 表示，最后才取正部或绝对值。`, String.raw`The next step still does not enter faces, refresh, or moving cells, and does not take rowwise absolute values of the four-row direct ledger. R0.71N starts from the complete \(\mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q\), retains \(B_{Q,t}\), \(d_{Q,t}\), and \(Y_t\) simultaneously, then substitutes the radial identity and the local filtered-enstrophy representation of \(B_Q\), and only afterward takes a positive part or an absolute value.`],
  [String.raw`这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71M 的 77 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。`, String.raw`This page follows the R0.00–R0.60 phase recap and organizes, from R0.61 through R0.71M, 77 research nodes. In chronological order, I record what each phase actually proved, which proposal was excluded by a concrete counterexample or scaling analysis, and which conditions have not been derived from the Navier–Stokes equations.`],
  [String.raw`annular-filter Lamb commutator 的精确二次速度增量公式，以及 fixed-cell projective pairing、radial identity 与四行尺度临界直接账本。`, String.raw`The exact quadratic velocity-increment formula for the annular-filter Lamb commutator, together with the fixed-cell projective pairing, radial identity, and four-row scale-critical direct ledger.`],
  [String.raw`R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 77 个节点沿着这个缺口推进。`, String.raw`The R0.00–R0.60 material remains in the preceding phase recap. R0.60 concluded that the complete Fourier–Leray structure and high-order computations could continue, but the critical quantity for general three-dimensional solutions was still uncontrolled. The following 77 nodes proceed along that gap.`],
  [String.raw`R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71M 的 77 个研究节点，记录从约化递推到 projected-Lamb 热体积、匹配小区 heat gap、黏性融合与增量—投影接口的路线。`, String.raw`Research recap after R0.60: a chronological account from R0.61 through R0.71M of 77 research nodes, tracing the route from reduced recurrences to projected-Lamb heat volume, the matched-cell heat gap, viscous fusion, and the increment–projective interface.`],
  [String.raw`R0.61–R0.71M 的 77 节公开笔记`, String.raw`R0.61–R0.71M: 77 public notes`],
  [String.raw`R0.61–R0.71M 回顾 · 2026-08-26`, String.raw`R0.61–R0.71M recap · 2026-08-26`],
  [String.raw`R0.61–R0.71M 研究节点`, String.raw`R0.61–R0.71M research nodes`],
  [String.raw`R0.61–R0.71M｜R0.60 之后的研究回顾`, String.raw`R0.61–R0.71M | Research recap after R0.60`],
  [String.raw`R0.71G–I 把时间缺口压到入口、单边联合生成与 faces。R0.71J–K 在完整 broad parent frame 和固定 aligned matched cells 上证明 \(K^{-2}\) 正生成与 \(O((\nu K^4)^{-1})\) heat payment 的两阶缺口。R0.71L 把 raw viscous collar 精确融合回 localized Laplacian row。R0.71M 随后证明 annular-filter Lamb commutator 的精确二次速度增量公式和完整 fixed-cell projective pairing；当前直接绝对估计产生四行临界充分账本。热包排除从标准能量类到所测试绝对临界预算的普适嵌入，但不是 NSE 解反例。`, String.raw`R0.71G–I compresses the time gap to entry, joint one-sided creation, and faces. R0.71J–K proves a two-power gap between \(K^{-2}\) positive creation and \(O((\nu K^4)^{-1})\) heat payment on the complete broad parent frame and fixed aligned matched cells. R0.71L fuses the raw viscous collar exactly back into the localized Laplacian row. R0.71M then proves the exact quadratic velocity-increment formula for the annular-filter Lamb commutator and the complete fixed-cell projective pairing; the current direct absolute estimate produces a four-row sufficient critical ledger. The heat packets rule out a universal embedding from the standard energy class into the tested absolute critical budgets, but they are not counterexamples among NSE solutions.`],
  [String.raw`R0.71G–R0.71M · 驻留、匹配小区、黏性融合与增量—投影接口`, String.raw`R0.71G–R0.71M · Residence, matched cells, viscous fusion, and the increment–projective interface`],
  [String.raw`R0.71M 对 critical increment 候选作了精确复核。\(\mathcal R_j\) 有二次速度增量表示，但 \(\operatorname{curl}\mathcal R_j\) 作为分裂行没有一般上频率支撑；只有与 resolved transport 融合后的 \(G_j\) 保持环带。热包证明能量类不普适支付当前 absolute budgets，但没有构造“bounded increment defect / unbounded signed tangent”的 NSE 反例，因此更深的 signed estimate 没有被排除。`, String.raw`R0.71M precisely audits the critical-increment candidate. \(\mathcal R_j\) has a quadratic velocity-increment representation, but the separated row \(\operatorname{curl}\mathcal R_j\) has no general upper-frequency support; only \(G_j\), after fusion with resolved transport, remains annular. The heat packets prove that the energy class does not universally pay the current absolute budgets, but they do not construct an NSE counterexample with a bounded increment defect and an unbounded signed tangent; a deeper signed estimate therefore remains possible.`],
  [String.raw`R0.71N 检查完整标量的第二次融合或 signed residual`, String.raw`R0.71N tests a second fusion of the complete scalar or a signed residual`],
  [String.raw`本节关闭的是“已知 increment defect + 当前 Cauchy/Bernstein split”这一条直接证明路线。它没有证明 increment 在逻辑上不能控制更小的 signed tangent，也没有得到继续性、奇性或全局正则性结论。`, String.raw`This section closes the direct proof route “known increment defect + current Cauchy/Bernstein split.” It does not prove that increments cannot logically control a smaller signed tangent, and it yields no conclusion on continuation, singularity, or global regularity.`],
  [String.raw`从完整 \(\mathcal J_Q\) 同时展开三个时间导数，检查第二次精确标量融合或明确的 signed residual。`, String.raw`Expand all three time derivatives simultaneously from the complete \(\mathcal J_Q\), and test for a second exact scalar fusion or an explicit signed residual.`],
  [String.raw`从完整标量 \(\mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q\) 出发，同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，检查是否存在第二次精确融合或明确的有符号余项。`, String.raw`Start from the complete scalar \(\mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q\), retain \(B_{Q,t}\), \(d_{Q,t}\), and \(Y_t\) simultaneously, and test whether there is a second exact fusion or an explicit signed residual.`],
  [String.raw`从有符号环带障碍走到 exact increment–projective bridge`, String.raw`From the signed-annulus obstruction to the exact increment–projective bridge`],
  [String.raw`对每个平移不变的标量环带滤波器，Lamb 交换子 \[ \mathcal R_j=T_j(u\times\omega)-u\times T_j\omega \] 有精确的二次速度增量公式。resolved transport 与 \(\operatorname{curl}\mathcal R_j\) 单独都不必保持环带支撑；只有二者融合后的 \(G_j\) 恢复 band limitation。`, String.raw`For every translation-invariant scalar annular filter, the Lamb commutator \[ \mathcal R_j=T_j(u\times\omega)-u\times T_j\omega \] has an exact quadratic velocity-increment formula. Resolved transport and \(\operatorname{curl}\mathcal R_j\) need not preserve annular support separately; only the fused \(G_j\) recovers band limitation.`],
  [String.raw`固定小区的完整 projective pairing 精确化为 \[ \langle P_QF_j,P_QM_Q\rangle =\int\chi_Q\left(G_j-\frac{B_Q}{d_Q}\operatorname{curl}C_Q\right) \cdot(G_j+\nu H_j). \] 当前直接 Cauchy 产生 resolved transport、differentiated commutator、projective denominator geometry 与 viscous annular mismatch 四行尺度临界消费者；这是充分账本，不是必要条件。`, String.raw`The complete projective pairing on a fixed cell becomes exactly \[ \langle P_QF_j,P_QM_Q\rangle =\int\chi_Q\left(G_j-\frac{B_Q}{d_Q}\operatorname{curl}C_Q\right) \cdot(G_j+\nu H_j). \] Direct Cauchy currently produces four scale-critical consumers: resolved transport, the differentiated commutator, projective denominator geometry, and viscous annular mismatch. This is a sufficient ledger, not a necessary condition.`],
  [String.raw`环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge`, String.raw`Annulus exclusion → source–core ledger → covariance-rank stratification → full-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficients → nonnegative refinement defect → viscous sign creation → critical material-heat-tent obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel sets → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge`],
  [String.raw`精确增量—投影桥成立，四行直接临界账本仍是额外条件`, String.raw`The exact increment–projective bridge holds; the four-row direct critical ledger remains an additional condition`],
  [String.raw`精确增量交换子与 fixed-cell pairing 已写出；当前审计没有从 Leray energy 推出四行总账，所测试的三个绝对临界预算也不由能量类普适嵌入。`, String.raw`The exact increment commutator and fixed-cell pairing are now explicit; the current audit does not derive the complete four-row ledger from Leray energy, and the energy class does not embed universally into the three tested absolute critical budgets.`],
  [String.raw`静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 从恒定投影障碍走到 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–K 把时间缺口收缩到全壳正缺陷与 fixed matched-cell heat gap；R0.71L 又把 raw viscous collar 精确融合回 localized Laplacian row。R0.71M 现在给出 annular-filter Lamb commutator 的精确二次速度增量公式、完整 fixed-cell projective pairing 与四行临界直接账本。热包说明这些绝对临界预算不由能量类普适推出，但不排除 NSE 特有的 signed cancellation。`, String.raw`After the static annulus family was rigorously excluded, the main route shifted to covariance-rank stratification and the full-frequency projection bridge. R0.71A–F moves from the constant-projection obstruction to a Leray-energy-level projected-Lamb heat volume and its bounded-overlap localization. R0.71G–K narrows the time gap to the all-shell positive defect and the fixed matched-cell heat gap; R0.71L then fuses the raw viscous collar exactly back into the localized Laplacian row. R0.71M now gives the exact quadratic velocity-increment formula for the annular-filter Lamb commutator, the complete fixed-cell projective pairing, and the four-row critical direct ledger. The heat packets show that these absolute critical budgets do not follow universally from the energy class, but they do not rule out an NSE-specific signed cancellation.`],
  [String.raw`累计回顾 R0.61–R0.71M · 2026-08-26`, String.raw`Cumulative recap R0.61–R0.71M · 2026-08-26`],
  [String.raw`目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71M 把 critical increment bridge 压成 exact commutator、exact projective pairing 与四行充分账本；它同时证明标准能量类不普适嵌入所测试的绝对临界预算。这个函数空间分离不是 NSE 解反例，完整标量的 signed fusion、faces 和无条件 weighted BV 仍未闭合。`, String.raw`There is no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71M compresses the critical increment bridge into an exact commutator, an exact projective pairing, and a four-row sufficient ledger; it also proves that the standard energy class does not embed universally into the tested absolute critical budgets. This function-space separation is not a counterexample among NSE solutions, and the signed fusion of the complete scalar, faces, and unconditional weighted BV remain unclosed.`],
  [String.raw`上次综述 v0.97 · 2026-08-26`, String.raw`Previous review v0.97 · 2026-08-26`],
  [String.raw`完整标量的第二次融合或 signed residual`, String.raw`A second fusion of the complete scalar or a signed residual`],
  [String.raw`我继续停在 fixed cells，不再把四行直接账本逐项绝对化。R0.71N 从完整 \(\mathcal J_Q\) 出发，同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，再代入 radial pairing 与局部 filtered-enstrophy 表示。结果可以是第二个精确标量融合，也可以是一个明确保留下来的有符号 residual；二者都不能预设。`, String.raw`I continue to stay on fixed cells and no longer take rowwise absolute values of the four-row direct ledger. R0.71N starts from the complete \(\mathcal J_Q\), retains \(B_{Q,t}\), \(d_{Q,t}\), and \(Y_t\) simultaneously, and then substitutes the radial pairing and local filtered-enstrophy representation. The result may be a second exact scalar fusion or an explicitly retained signed residual; neither can be assumed in advance.`],
  [String.raw`下一步 R0.71N：`, String.raw`Next step, R0.71N:`],
  [String.raw`研究笔记 R0.71M · 2026-08-26`, String.raw`Research note R0.71M · 2026-08-26`],
  [String.raw`一个 \(L^2\)-归一化无散热包族保持精确一致的 kinetic-energy equality，同时 Yu 型四次缺陷、velocity square-Carleson mass 与 normalized projected-Lamb integral 分别按 \(r^{-2}\)、\(r^{-1}\)、\(r^{-1}\) 增长。这排除从标准能量类到这些绝对预算的普适函数空间嵌入；热包不是非线性 NSE 解。`, String.raw`An \(L^2\)-normalized divergence-free heat-packet family preserves exactly the same kinetic-energy equality, while the Yu-type quartic defect, velocity square-Carleson mass, and normalized projected-Lamb integral grow respectively like \(r^{-2}\), \(r^{-1}\), and \(r^{-1}\). This rules out a universal function-space embedding from the standard energy class into these absolute budgets; the heat packets are not nonlinear NSE solutions.`],
  [String.raw`阅读 R0.71M 研究笔记 →`, String.raw`Read research note R0.71M →`],
  [String.raw`展开 47 篇公开笔记`, String.raw`Expand 47 public notes`],
  [String.raw`综述 v0.98 · 2026-08-26`, String.raw`Review v0.98 · 2026-08-26`],
  [String.raw`R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、全壳正缺陷、固定匹配小区、黏性融合与增量—投影接口。`, String.raw`The route after R0.60 divides into twelve phases: reduced Picard dynamics and the shear boundary; transverse perturbations; local pressure budgets; signed physical annuli; moving labels and source–core duality; deviation tensors and finite observation; complete frame covariance; the constant-projection boundary; positive output and material heat tents; projected-Lamb heat volume; local heat packing and the critical-trace obstruction; and finally the residence boundary, the all-shell positive defect, fixed matched cells, viscous fusion, and the increment–projective interface.`],
  [String.raw`R0.60 recap 之后的累计回顾收录 77 个节点；全站现有 137 篇公开研究笔记`, String.raw`The cumulative recap after R0.60 contains 77 nodes; the site now has 137 public research notes`],
  [String.raw`R0.71M 已完成：`, String.raw`R0.71M completed:`],
]);

function extractNumericTokens(value) {
  return [...String(value).matchAll(/\d+(?:[.\-–—]\d+)*/g)].map((match) => match[0]);
}

function sameTokens(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

const batchId = /^r071m\d+$/;
const currentWithoutBatch = current.filter((entry) => !batchId.test(entry.id));
const currentByChinese = new Map(currentWithoutBatch.map((entry) => [entry.zh, entry]));
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error("duplicate Chinese keys already present outside the R0.71M batch");
}

const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));
if (sourceByChinese.size !== source.length) {
  throw new Error("duplicate Chinese keys in collected site strings");
}

const missing = source.filter((entry) => !currentByChinese.has(entry.zh));
const missingChinese = new Set(missing.map((entry) => entry.zh));
if (additions.size !== missing.length) {
  throw new Error(
    `expected additions to equal the ${missing.length} active missing strings, found ${additions.size}`,
  );
}
for (const entry of missing) {
  if (!additions.has(entry.zh)) throw new Error(`missing translation: ${entry.zh}`);
}
for (const zh of additions.keys()) {
  if (!missingChinese.has(zh)) throw new Error(`translation is not an active missing string: ${zh}`);
}

const translatedEntries = missing.map((entry, index) => {
  const en = additions.get(entry.zh);
  const zhProtected = extractProtectedTokens(entry.zh);
  const enProtected = extractProtectedTokens(en);
  if (!sameTokens(zhProtected, enProtected)) {
    throw new Error(
      `protected-token mismatch for ${entry.zh}\nZH ${JSON.stringify(zhProtected)}\nEN ${JSON.stringify(enProtected)}`,
    );
  }

  const zhNumeric = extractNumericTokens(entry.zh);
  const enNumeric = extractNumericTokens(en);
  if (!sameTokens(zhNumeric, enNumeric)) {
    throw new Error(
      `numeric-token mismatch for ${entry.zh}\nZH ${JSON.stringify(zhNumeric)}\nEN ${JSON.stringify(enNumeric)}`,
    );
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error(`blank or Chinese-containing English translation for ${entry.zh}`);
  }
  if (/\b(?:we|our|ours|us)\b/i.test(en)) {
    throw new Error(`first-person plural voice in translation for ${entry.zh}`);
  }

  return {
    ...entry,
    id: `r071m${String(index + 1).padStart(3, "0")}`,
    en,
  };
});

const merged = [...currentWithoutBatch, ...translatedEntries];
const mergedChinese = new Set(merged.map((entry) => entry.zh));
const mergedIds = new Set(merged.map((entry) => entry.id));
if (mergedChinese.size !== merged.length) {
  throw new Error("translation merge produced duplicate Chinese keys");
}
if (mergedIds.size !== merged.length) {
  throw new Error("translation merge produced duplicate IDs");
}

const invalid = merged.filter(
  (entry) =>
    !entry.en?.trim() ||
    containsChinese(entry.en) ||
    !sameTokens(extractProtectedTokens(entry.zh), extractProtectedTokens(entry.en)),
);
if (invalid.length) {
  throw new Error(`invalid translations after merge: ${invalid.map((entry) => entry.id).join(", ")}`);
}

await writeFile(translationPath, `${JSON.stringify(merged, null, 2)}\n`);
console.log(
  JSON.stringify(
    {
      source: source.length,
      existingWithoutBatch: currentWithoutBatch.length,
      activeMissingBefore: missing.length,
      added: translatedEntries.length,
      firstId: translatedEntries.at(0)?.id,
      lastId: translatedEntries.at(-1)?.id,
      total: merged.length,
      duplicateChinese: merged.length - mergedChinese.size,
      duplicateIds: merged.length - mergedIds.size,
      invalid: invalid.length,
      englishWithChinese: translatedEntries.filter((entry) => containsChinese(entry.en)).length,
      firstPersonPlural: translatedEntries.filter((entry) => /\b(?:we|our|ours|us)\b/i.test(entry.en)).length,
      protectedTokenMismatches: translatedEntries.filter(
        (entry) => !sameTokens(extractProtectedTokens(entry.zh), extractProtectedTokens(entry.en)),
      ).length,
      numericTokenMismatches: translatedEntries.filter(
        (entry) => !sameTokens(extractNumericTokens(entry.zh), extractNumericTokens(entry.en)),
      ).length,
    },
    null,
    2,
  ),
);
