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

const translationRows = String.raw`
打开 81 节完整索引 ||| Open the complete 81-section index
的零点公式保留中心锚点。 ||| 's zero-counting formula retains the center anchor.
给出依赖强 \(V\)-norm 的复时间瓣与重新启动； ||| provides a complex-time lobe and restart depending on the strong \(V\)-norm;
回到 componentwise positive parts 之前的 signed precursor/source，检查 PDE 是否耦合不同 observable 的 entry events；不再重复定性解析性。 ||| Return to the signed precursor/source before taking componentwise positive parts, and test whether the PDE couples entry events of different observables; do not repeat qualitative analyticity.
开放接口 · R0.71R ||| Open interface · R0.71R
累计回顾与 81 节索引 ||| Cumulative recap and 81-section index
文献综述 v1.02 · 2026-08-26 ||| Literature review v1.02 · 2026-08-26
我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.71Q 只列为研究笔记。我不把计算或笔记外推成正则性定理。 ||| I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.71Q only as research notes. I do not extrapolate computations or notes into regularity theorems.
有限 Jensen window theorem 成立，直接解析性路线停止 ||| The finite Jensen window theorem holds; the direct analyticity route stops
支付解析半径或复域上界，但不支付 filtered-observable lower anchor 与全分量零点并集。两轮限定检索未找到从 Leray 数据支付完整 entry-time measure 的定理；这是 bounded negative finding，不是原创性、优先权或不存在性结论。 ||| pay for the analyticity radius or a complex-domain upper bound, but not a filtered-observable lower anchor or the union of zeros over all components. Two scoped searches found no theorem deriving the full entry-time measure from Leray data; this is a bounded negative finding, not a claim of originality, priority, or nonexistence.
中。R0.69P–R0.71P 从有符号物理环带走到 positive-entry temporal-packing boundary；R0.71Q 再把 complex-time Jensen route 写成有限条件定理，并隔离 anchor、component-union、cover 与 pointwise-envelope 账本。保留下来的结果都不是全局正则性结论。 ||| . R0.69P–R0.71P moves from signed physical annuli to the positive-entry temporal-packing boundary; R0.71Q then formulates the complex-time Jensen route as a finite conditional theorem and isolates the anchor, component-union, cover, and pointwise-envelope ledger. None of the retained results is a global regularity conclusion.
bounded support overlap 与 \(\dot H^{-1}\) Lamb square sum 删除同刻 cell multiplicity，完整目标归约到 distinct entry-time counting measure。 ||| Bounded support overlap and the \(\dot H^{-1}\) Lamb square sum remove same-time cell multiplicity, reducing the full target to the distinct entry-time counting measure.
R0.71Q 从 Temam 复时间瓣抽取显式双侧圆盘，并用 finite ownership cover 与 Hilbert-valued Jensen 给出有限条件 entry bound。该 bound 必须支付 projection anchor、component union、window cover 与 pointwise batch envelope；三个精确解析族证明这些税不能在一般 holomorphic class 中删除。R0.71R 只检查 NSE-specific parabolic incidence / Carleson packing，并回到 componentwise positive parts 之前的 signed precursor/source。我继续用下面六条筛选。 ||| R0.71Q extracts an explicit two-sided disk from Temam's complex-time lobe and uses a finite ownership cover and Hilbert-valued Jensen to give a finite conditional entry bound. The bound must pay for the projection anchor, component union, window cover, and pointwise batch envelope; three exact analytic families show that these taxes cannot be removed in a general holomorphic class. R0.71R examines only NSE-specific parabolic incidence / Carleson packing and returns to the signed precursor/source before componentwise positive parts. I continue to apply the following six filters.
R0.71Q 的一手文献边界 ||| Primary-source boundary for R0.71Q
R0.71Q 关闭了什么，R0.71R 只检查什么 ||| What R0.71Q closes, and what R0.71R alone examines
Temam 复时间瓣给出显式双侧圆盘；finite ownership cover 与 Hilbert-valued Jensen 给出带 anchor、truncation、cover 和 pointwise-envelope 账本的条件 bound。Blaschke、component-union 与 sine-square families 证明前三类税不能由抽象解析性删除。 ||| Temam's complex-time lobe gives an explicit two-sided disk; a finite ownership cover and Hilbert-valued Jensen give a conditional bound with an anchor, truncation, cover, and pointwise-envelope ledger. Blaschke, component-union, and sine-square families show that abstract analyticity cannot remove the first three taxes.
\(T_\sharp^{-1}\) 至少按 \((1+R_\sharp^2)^2\) 增长，而 \(R_\sharp\) 是 \(L_t^\infty H_x^1\) 强范数。Leray 只给相关的普通时间积分。抽象脉冲 \(Y_N(t)=N(1-Nt)_+\) 满足 \(\int Y_N=1/2\) 而 \(\int Y_N^2=N/3\)，说明 \(L^1\) 预算不能支付一般的 inverse-window density。 ||| \(T_\sharp^{-1}\) grows at least like \((1+R_\sharp^2)^2\), while \(R_\sharp\) is the strong \(L_t^\infty H_x^1\) norm. Leray theory provides only the corresponding ordinary time integral. The abstract pulse \(Y_N(t)=N(1-Nt)_+\) satisfies \(\int Y_N=1/2\) while \(\int Y_N^2=N/3\), showing that an \(L^1\) budget cannot pay for a general inverse-window density.
\[ \bigoplus_q g_q(z)=0 \quad\Longleftrightarrow\quad g_q(z)=0\ \text{对所有 }q, \] ||| \[ \bigoplus_q g_q(z)=0 \quad\Longleftrightarrow\quad g_q(z)=0\ \text{for every }q, \]
01 · R0.71P 接口 ||| 01 · R0.71P interface
03 · Temam 圆盘 ||| 03 · Temam disk
04 · 条件打包定理 ||| 04 · Conditional packing theorem
05 · 锚点障碍 ||| 05 · Anchor obstruction
06 · 分量并集税 ||| 06 · Component-union tax
07 · 窗口覆盖税 ||| 07 · Window-cover tax
08 · NSE 预算审计 ||| 08 · NSE budget audit
09 · 双重审计 ||| 09 · Dual audit
版本 v0.71Q · 2026-08-26 ||| Version v0.71Q · 2026-08-26
半径、锚点、并集和点态权重都不是 Leray 预算的免费输入 ||| Radius, anchor, union, and pointwise weight are not free inputs from the Leray budget
半径与覆盖。 ||| Radius and cover.
报告、证书、图数据和两个独立 checker 全部保留 ||| The report, certificates, figure data, and two independent checkers are all retained
本节判断 ||| Section verdict
本节证明什么，也明确不证明什么 ||| What this section proves—and explicitly does not prove
并集税 ||| Union tax
从 Temam 的单侧瓣中抽取一个精确双侧圆盘 ||| Extracting an exact two-sided disk from Temam's one-sided lobe
从实时间 \(\tau\) 重新启动，Temam 的复时间瓣尺度为 ||| Restarting from real time \(\tau\), Temam's complex-time lobe has scale
代数证书与独立浮点重建分别通过 ||| The algebraic certificate and independent floating-point reconstruction pass separately
但不能免费关闭 NSE 的时间进入打包 ||| but cannot close NSE temporal entry packing for free
的零点公式保留中心值。 ||| 's zero-counting formula retains the center value.
的唯一延拓要求完整速度场在空间开集消失，不能替代单个 filtered observable 的定量下锚点。 ||| 's unique continuation requires the full velocity field to vanish on a spatial open set and cannot replace a quantitative lower anchor for a single filtered observable.
的向量零点；反向不必成立。因此把所有分量零点作为上界是安全的，但会产生分量并集代价。 ||| has a vector zero; the converse need not hold. Therefore, using all component zeros as an upper bound is safe, but incurs a component-union cost.
点 \(k/N\)、\(k=0,\ldots,N-1\) 是 \(N\) 个正进入，每个 \(A_+=1\)。给第 \(m\) 个 owned cell 取中心 \((m+1/2)/N\)、外半径 \(3/(4N)\)、内半径 \(5/(8N)\)，则半径比恒为 \(6/5\)，而 ||| The points \(k/N\), \(k=0,\ldots,N-1\), are \(N\) positive entries, each with \(A_+=1\). For the \(m\)th owned cell, choose center \((m+1/2)/N\), outer radius \(3/(4N)\), and inner radius \(5/(8N)\); the radius ratio is then always \(6/5\), while
点态 batch envelope。 ||| Pointwise batch envelope.
独立审计说明 ||| Independent audit notes
端点边界 ||| Endpoint boundary
对 \(N\ge1\)，取 ||| For \(N\ge1\), take
对固定有限截断和紧含于经典区间的半开窗口，Temam 复时间圆盘、有限 ownership cover 与 Jensen 公式给出一个显式 entry bound。这个界必须支付复解析半径、复域增长、非零投影锚点、分量/截断和窗口覆盖；加权目标还要支付每个窗口上的点态 batch envelope。有限 Blaschke、线性分量族和 sine-square 族分别证明锚点税、并集税和覆盖税不能在抽象解析函数层面删除。 ||| For a fixed finite truncation and a half-open window compactly contained in a classical interval, Temam's complex-time disk, a finite ownership cover, and Jensen's formula give an explicit entry bound. This bound must pay for the complex-analytic radius, complex-domain growth, a nonzero projection anchor, component/truncation and window coverage; the weighted target must also pay for the pointwise batch envelope on each window. Finite Blaschke, linear-component, and sine-square families respectively show that the anchor, union, and cover taxes cannot be removed at the level of abstract analytic functions.
反例边界： ||| Counterexample boundary:
附图、数据、manifest 与源代码包 ||| Figure, data, manifest, and source-code package
附图把条件上界与三种不可删除的税分开显示 ||| The figure separates the conditional upper bound from the three nonremovable taxes
复时间解析性能够给出有限条件计数， ||| Complex-time analyticity can provide a finite conditional count,
复时间圆盘 ||| Complex-time disk
复域增长。 ||| Complex-domain growth.
覆盖税 ||| Cover tax
给出时间导数与联合解析估计；大数据常数依赖局部强解窗口，小数据一致情形已经处于全局正则类。 ||| provide time-derivative and joint analyticity estimates; the large-data constants depend on local strong-solution windows, while the uniform small-data regime is already globally regular.
给出所用有界零因子的原始背景。 ||| provides the original background for the bounded zero factors used here.
给出显式复时间扇区和模态不会突然生成的定性结论，不给反复零点或模态并集计数。 ||| gives an explicit complex-time sector and the qualitative conclusion that modes do not appear suddenly, but gives no count of repeated zeros or modal unions.
给出周期强解的复时间瓣、强空间上界和重新启动；其尺度依赖强 \(V\)-norm。 ||| gives a complex-time lobe, a strong-space upper bound, and restart for periodic strong solutions; its scale depends on the strong \(V\)-norm.
归一化 \(T=1\) 后，盘内 \(x\ge15/64\)、\(x^2+y^2\le290/4096\)，并且 ||| After normalizing \(T=1\), inside the disk \(x\ge15/64\) and \(x^2+y^2\le290/4096\), and
即使零点数已知，目标仍按 \(\mathcal H(t)\) 加权。条件定理使用 \(H_m=\sup_{K_m}\mathcal H\)；普通 \(dt\) 积分不能控制原子事件集上的点态抽样。 ||| Even when the zero count is known, the target is still weighted by \(\mathcal H(t)\). The conditional theorem uses \(H_m=\sup_{K_m}\mathcal H\); an ordinary \(dt\) integral cannot control pointwise sampling on the atomic event set.
价值在于精确排除一条看似自然但不够强的路线 ||| The value lies in precisely excluding a natural-looking but insufficient route
接口 ||| Interface
截至 2026-08-26 的两轮限定一手文献检索，没有找到从 Leray 数据支付 lower anchor、component-union tax 或完整 R0.71P entry-time measure 的定理。这是 bounded negative finding，不是不存在性、原创性或优先权声明。 ||| Two scoped primary-source searches through 2026-08-26 found no theorem deriving the lower anchor, component-union tax, or full R0.71P entry-time measure from Leray data. This is a bounded negative finding, not a claim of nonexistence, originality, or priority.
解析性路线在有限经典窗口成立，但无条件路线到此停止 ||| The analyticity route works on finite classical windows, but the unconditional route stops here
精确有理数审计给出 ||| The exact rational audit gives
局部相对数据一致，也不能省掉覆盖窗口数 ||| Even uniform local relative data cannot eliminate the window-cover count
锚点障碍 ||| Anchor obstruction
每个观测量都受控，零点并集仍可随截断线性增长 ||| Each observable is controlled, yet the union of zeros can still grow linearly with the truncation
期刊附图 PDF ||| Journal figure PDF
取 \(K^\sharp=[a-\delta,b+\delta]\Subset I_{\rm strong}\)，令 ||| Take \(K^\sharp=[a-\delta,b+\delta]\Subset I_{\rm strong}\), and set
取互异 \(b_q\in(1/4,1/2)\) 和 \(g_q(z)=z-b_q\)。在单位盘上每个分量都有统一上界 \(<3/2\) 和统一中心锚点 \(>1/4\)，但 Q 个分量零点的并集恰有 Q 个点。 ||| Choose distinct \(b_q\in(1/4,1/2)\) and \(g_q(z)=z-b_q\). On the unit disk, every component has a uniform upper bound \(<3/2\) and a uniform center anchor \(>1/4\), yet the union of the zeros of Q components contains exactly Q points.
全部 N 个零点都变成偶阶正进入，并且每个零点都有 \(A_+=1\)。这直接对齐 R0.71P 的正进入定义。该族是解析 Hilbert 路径，不是 NSE 重复 face 构造。 ||| All N zeros become even-order positive entries, and every zero has \(A_+=1\). This matches the positive-entry definition in R0.71P exactly. This family is an analytic Hilbert path, not an NSE repeated-face construction.
全部零点位于 \([1/4,1/2)\)，其中端点 \(1/4\) 只在 \(N=1\) 出现；同时 \(\|B_N\|_{H^\infty(\mathbb D)}=1\)，中心锚点满足 ||| All zeros lie in \([1/4,1/2)\), with the endpoint \(1/4\) occurring only when \(N=1\); meanwhile \(\|B_N\|_{H^\infty(\mathbb D)}=1\), and the center anchor satisfies
若 \(C:D(t_*,R)\to H_{\mathbb C}\) 强全纯，且 ||| If \(C:D(t_*,R)\to H_{\mathbb C}\) is strongly holomorphic and
若解析半径和相应强界在 \(K\uparrow T^*\) 时保持统一，局部强理论会把解延拓过 \(T^*\)。因此端点一致复时间圆盘本身已经是 continuation-level input，不能作为 Leray 数据的无偿推论。 ||| If the analyticity radius and corresponding strong bound remain uniform as \(K\uparrow T^*\), local strong theory extends the solution beyond \(T^*\). Thus, an endpoint-uniform complex-time disk is already continuation-level input and cannot be inferred from Leray data for free.
若只能在 transversality、quantitative unique continuation、有限维截断或额外强范数下成立，我会继续把条件保留在 theorem 中，不把它升级为 Leray 结论。 ||| If the claim holds only under transversality, quantitative unique continuation, finite-dimensional truncation, or an additional strong norm, I will keep the condition in the theorem rather than promote it to a Leray conclusion.
删除在连通经典区间上恒为零的分量；它们没有 entry。对剩余有限分量选择避开全部零点的实中心 \(t_m\)，让内区间覆盖 \(K\)，并用半开 ownership sets \(K_m\) 唯一分配每个时刻。空的 \(K_m\) 直接丢弃。可取 ||| Delete components that vanish identically on the connected classical interval; they have no entries. For the remaining finite components, choose real centers \(t_m\) that avoid every zero, let the inner intervals cover \(K\), and use half-open ownership sets \(K_m\) to assign each time uniquely. Discard empty \(K_m\). One may take
设 ||| Set
剩余目标是批次权重对 distinct entry-time measure 的积分 ||| The remaining target is the integral of the batch weight against the distinct entry-time measure
所以本节没有证明 uniform NSE temporal packing。它关闭的是一个方法判断：仅靠“时间解析 + 复域上界”无法完成 R0.71P 的计数测度估计。 ||| Thus this section does not prove uniform NSE temporal packing. It closes a methodological verdict: “time analyticity + a complex-domain upper bound” alone cannot establish the counting-measure estimate in R0.71P.
所以固定解析半径和固定复域上界允许任意多实零点，Jensen 的锚点对数与零点数同阶。简单零点中还有 \(\lceil N/2\rceil\) 个正导数穿越。若取 ||| Thus fixed analyticity radius and fixed complex-domain upper bound allow arbitrarily many real zeros, and Jensen's anchor logarithm is of the same order as the zero count. Among the simple zeros, \(\lceil N/2\rceil\) also have positive-derivative crossings. If one takes
它检测的是零点交集，不是 entry 所需的并集。同刻空间 batching 已经删除 cell multiplicity，但它不提供跨时零点集合的耦合。 ||| It detects the intersection of zero sets, not the union required for entries. Same-time spatial batching has already removed cell multiplicity, but it provides no coupling between zero sets across time.
条件定理 ||| Conditional theorem
同步研究笔记 PDF ||| Synchronized research-note PDF
统一 NSE zero count、无限 frame estimate、Leray 极限、潜在奇点端点覆盖、继续性判据、有限时奇性或全局正则性。 ||| uniform NSE zero count, infinite frame estimate, Leray limit, endpoint coverage of a potential singularity, continuation criterion, finite-time singularity, or global regularity.
投影锚点。 ||| Projection anchor.
图 R0.71Q。A：从 Temam 复时间瓣中抽取的显式双侧圆盘。B：有限 Blaschke 族在固定半径与上界下制造任意多零点，锚点对数与零点数同阶。C：逐分量数据一致时，零点并集仍按分量数增长。D：sine-square 族保持局部半径比与相对增长一致，但 ownership cover 数按 (N) 增长。 ||| Figure R0.71Q. A: the explicit two-sided disk extracted from Temam's complex-time lobe. B: a finite Blaschke family creates arbitrarily many zeros at fixed radius and upper bound, with the anchor logarithm of the same order as the zero count. C: even with uniform componentwise data, the zero union still grows with the component count. D: the sine-square family keeps the local radius ratio and relative growth uniform, but the ownership-cover count grows as (N).
未证明： ||| Not proved:
文献边界： ||| Literature boundary:
我把左端简记为 \(N_C(D(t_*,r))\)：它只数不同向量零点；右端标量零点按重数计，因此是安全上界。闭内盘通过中间外半径后取极限处理，不能把 \(r=R\) 代入。圆盘自同构、Poisson–Jensen、Cartan 小值集或 Blaschke 分解只会改写锚点，不会删除它。 ||| I abbreviate the left-hand side as \(N_C(D(t_*,r))\): it counts only distinct vector zeros; the scalar zeros on the right are counted with multiplicity, so it is a safe upper bound. A closed inner disk is handled by first using an intermediate outer radius and then taking a limit; \(r=R\) cannot be substituted. Disk automorphisms, Poisson–Jensen, Cartan small-value sets, or Blaschke factorization only reformulate the anchor; they do not remove it.
无 PDE 时间推进 ||| No PDE time evolution
下一对象：NSE-specific incidence / Carleson packing ||| Next object: NSE-specific incidence / Carleson packing
下一节不再重复 Jensen。我要在逐分量正部被选取之前，回到 signed precursor/source，检查 entry events 是否满足由 NSE 方程、热核传播或 parabolic geometry 强迫的 incidence law。候选结论必须同时通过三类压力测试：R0.71P 的 sequential path、R0.71Q 的 Blaschke anchor family，以及 all-observable union tax。 ||| The next section will not repeat Jensen. Before the componentwise positive parts are selected, I will return to the signed precursor/source and test whether entry events satisfy an incidence law forced by the NSE equations, heat-kernel propagation, or parabolic geometry. Any candidate conclusion must pass three kinds of stress tests simultaneously: the sequential path of R0.71P, the Blaschke anchor family of R0.71Q, and the all-observable union tax.
显式 Temam 瓣内圆盘；Hilbert 值 Jensen zero count；有限 ownership-cover entry theorem；锚点、并集、覆盖和普通预算分离的精确反例族。 ||| Explicit disk inside the Temam lobe; Hilbert-valued Jensen zero count; finite ownership-cover entry theorem; exact counterexample families separating the anchor, union, cover, and ordinary-budget costs.
限定检索没有发现直接定理，不等于证明文献中不存在，也不构成新颖性或优先权声明。 ||| A bounded search found no direct theorem; this does not prove that none exists in the literature and does not constitute a claim of novelty or priority.
研究笔记 R0.71Q · COMPLEX TIME · JENSEN WINDOWS · METHOD AUDIT ||| Research note R0.71Q · COMPLEX TIME · JENSEN WINDOWS · METHOD AUDIT
研究笔记 R0.71Q：复时间解析性在固定经典窗口上给出带锚点、截断、覆盖和批次包络代价的有限 Jensen 计数；这些代价尚不能由 Leray 预算统一支付。 ||| Research note R0.71Q: Complex-time analyticity gives a finite Jensen count on a fixed classical window, with costs for the anchor, truncation, cover, and batch envelope; these costs still cannot be paid uniformly by the Leray budget.
已有文献支付解析半径与上界，没有支付完整进入计数 ||| Existing literature pays for the analytic radius and upper bound, but not the full entry count
已证明： ||| Proved:
由复 Hahn–Banach 选取 norming functional \(\ell\)，对 \(f=\ell\circ C\) 使用 Jensen 公式。每个向量零点都是 \(f\) 的标量零点，故 ||| By complex Hahn–Banach, choose a norming functional \(\ell\), and apply Jensen's formula to \(f=\ell\circ C\). Every vector zero is a scalar zero of \(f\), hence
有限 Blaschke 乘积证明锚点对数不可删除 ||| Finite Blaschke products show that the anchor logarithm cannot be removed
有限 ownership cover 给出带整数 Jensen capacity 的条件定理 ||| A finite ownership cover gives a conditional theorem with integer Jensen capacity
于是从 \(\tau=t_*-T/4\) 启动，可在 \(t_*\) 周围得到真实双侧圆盘。再缩到 \(D(t_*,T/128)\)，Temam 的 \(Au\) 估计和固定算子 \(\mathcal O_\alpha u=C_\alpha\) 给出有限复域上界 \(M_\alpha\)。它对每个固定分量有效，但不自动对全壳、全小区一致。 ||| Thus, restarting at \(\tau=t_*-T/4\) yields a genuine two-sided disk around \(t_*\). After shrinking further to \(D(t_*,T/128)\), Temam's \(Au\) estimate and the fixed operator \(\mathcal O_\alpha u=C_\alpha\) give a finite complex-domain upper bound \(M_\alpha\). It is valid for each fixed component but is not automatically uniform over all shells and cells.
与 \(m,N\) 无关；但仍需 \(N\) 个窗口。把窗口合并，只会把这笔代价转移到全局复增长中。覆盖必须逐点而非几乎处处，因为全部 entry atoms 可能落在 Lebesgue 零测集上。 ||| This is independent of \(m,N\), but \(N\) windows are still required. Merging the windows merely transfers this cost to the global complex growth. The cover must be pointwise rather than almost everywhere because all entry atoms may lie on a set of Lebesgue measure zero.
阅读 R0.60 之后累计回顾 ||| Read the cumulative recap after R0.60
在 \(K=[0,1)\) 取 ||| On \(K=[0,1)\), take
在每个 entry time 选择一个真正进入的 witness component。ownership 使时间集合不交，Jensen 容量控制每个 witness 的零点数，R0.71P 的同刻 bound 控制其权重，因而 ||| At each entry time, choose a witness component that actually enters. Ownership makes the time sets disjoint, Jensen capacity controls the zero count of each witness, and R0.71P's same-time bound controls its weight; therefore
在有限 shell–cell 截断 \(\Lambda\) 上，R0.71P 已证明同刻 entries 满足 ||| On a finite shell–cell truncation \(\Lambda\), R0.71P has proved that same-time entries satisfy
这不是对千禧年问题的直接推进定理，却是有研究价值的路线分类：有限 Jensen 结论被完整写出，失效位置被分解成可单独检验的账本，且每个主要抽象缺口都有显式反例族。以后任何声称用时间解析性关闭 temporal packing 的方案，都必须说明它从 NSE 动力学额外得到哪一种 anchor、zero-set coupling、cover density 或 event-weight control。 ||| This is not a theorem directly advancing the Millennium Problem, but it provides a research-useful route classification: the finite Jensen conclusion is stated in full, the failure points are separated into independently testable ledger items, and every main abstract gap has an explicit counterexample family. Any future proposal claiming to close temporal packing by time analyticity must state which additional anchor, zero-set coupling, cover density, or event-weight control it obtains from NSE dynamics.
这里 \(K=[a,b)\Subset I_{\rm strong}\)，\(\mathfrak n_\Lambda\) 只数不同进入时刻。每个 positive entry 都是某个 Hilbert 值观测量 ||| Here \(K=[a,b)\Subset I_{\rm strong}\), and \(\mathfrak n_\Lambda\) counts only distinct entry times. Every positive entry is a zero of some Hilbert-valued observable
这是有限条件定理，也是定量、可审计的定理。右端尚未被 Leray data 控制。 ||| This is a finite conditional theorem, as well as a quantitative and auditable one. The right-hand side is not yet controlled by Leray data.
逐分量 Jensen 必须对 \(q\) 求和。乘积 \(\prod_qg_q\) 检测并集，却把中心锚点变成乘积，其对数仍是各分量税之和。张量积有相同问题。直接和则更糟： ||| Componentwise Jensen must be summed over \(q\). The product \(\prod_qg_q\) detects the union, but turns the central anchor into a product, whose logarithm is still the sum of the component costs. The tensor product has the same problem. A direct sum is even worse:
状态 · R0.71Q 条件定理与方法不可能性审计完成 ||| Status · R0.71Q conditional theorem and method-impossibility audit completed
Blaschke、linear-component、sine-square 和 pulse families 是抽象解析/预算族，不是 Navier–Stokes 重复进入轨道。 ||| The Blaschke, linear-component, sine-square, and pulse families are abstract analytic/budget families, not Navier–Stokes trajectories with repeated entries.
exact / independent 证书 ||| exact / independent certificates
exact producer 用有理数检查 Temam 瓣内圆盘，逐项验证 \(N=1,2,4,8,16,32,64\) 的 Blaschke 锚点、零点与正导数计数，并核对 squared positive-entry、component union、sine-square cover 和 \(L^1\)–inverse-window pulse。 ||| The exact producer checks the disk inside the Temam lobe with rational arithmetic, verifies term by term the Blaschke anchor, zero count, and positive-derivative count for \(N=1,2,4,8,16,32,64\), and checks the squared positive-entry, component-union, sine-square-cover, and \(L^1\)–inverse-window pulse cases.
independent checker 没有导入 exact producer。它对每个 Blaschke 乘积抽取 8,192 个单位圆边界点，最大模误差为 \(1.22\times10^{-14}\)；200,000 个随机点重检复时间圆盘，最小 lobe residual 为 \(9.86\times10^{-3}\)；规定零点 residual 和中心乘积对数误差均为零。两套证书都不进行 NSE 时间推进。 ||| The independent checker does not import the exact producer. For each Blaschke product it samples 8,192 points on the unit-circle boundary; the maximum modulus error is \(1.22\times10^{-14}\). It rechecks the complex-time disk using 200,000 random points; the minimum lobe residual is \(9.86\times10^{-3}\). The specified zero residual and central-product logarithm error are both zero. Neither certificate performs NSE time evolution.
Jensen 的有效形式必然含有非零下锚点 ||| An effective form of Jensen necessarily contains a nonzero lower anchor
localized filtered observable 有非平凡核和符号抵消。R0.71P 的真实 smooth NSE initial jet 已有 \(Y(0)=1\)、\(C_\alpha(0)=0\)、\(C_{\alpha,t}(0)\ne0\)，故总 enstrophy 不会给指定投影的正下界。 ||| A localized filtered observable has a nontrivial kernel and sign cancellation. The genuine smooth NSE initial jet from R0.71P already has \(Y(0)=1\), \(C_\alpha(0)=0\), and \(C_{\alpha,t}(0)\ne0\), so total enstrophy cannot provide a positive lower bound for a specified projection.
NSE 账本 ||| NSE ledger
R0.71P 把同一时刻的全部 shell–cell entries 合成一个空间批次，剩下 distinct entry times 的计数测度。本节把 Temam 的复时间解析区、Hilbert 值 Jensen 公式和有限 ownership cover 严格接上。结果是一条可证明的有限定理；它同时暴露出 analytic radius、projection anchor、component union、window cover 和点态 batch envelope 的代价。现有 Leray 预算没有统一支付这些代价。 ||| R0.71P combines all shell–cell entries at one time into a single spatial batch, leaving the counting measure of distinct entry times. This section rigorously connects Temam's complex-time analyticity region, the Hilbert-valued Jensen formula, and a finite ownership cover. The result is a provable finite theorem; it also exposes the costs of the analytic radius, projection anchor, component union, window cover, and pointwise batch envelope. Existing Leray budgets do not pay these costs uniformly.
R0.71Q · 2026-08-26 · 个人数学研究日志 ||| R0.71Q · 2026-08-26 · Personal mathematical research log
R0.71Q Temam 复时间圆盘、Jensen 锚点税、分量并集税和窗口覆盖税审计 ||| R0.71Q audit of the Temam complex-time disk, Jensen anchor tax, component-union tax, and window-cover tax
R0.71Q｜Jensen 给出有限条件计数，但四项 NSE 账本仍未支付 ||| R0.71Q | Jensen gives a finite conditional count, but four NSE ledger items remain unpaid
R0.71R 转向 NSE-specific parabolic incidence / Carleson packing ||| R0.71R turns to NSE-specific parabolic incidence / Carleson packing
Temam 的上界包含 \(T_\sharp^{-1}\) 和固定 shell–cell 算子范数；它不是全 frame 一致估计。 ||| Temam's upper bound contains \(T_\sharp^{-1}\) and the fixed shell–cell operator norm; it is not uniform over the full frame.
Temam 第 7 章 ||| Temam, Chapter 7
Temam 复时间瓣到显式圆盘、Hilbert 值 Jensen 定理、Blaschke 锚点障碍、分量并集税、窗口覆盖税和 NSE 预算审计。 ||| From the Temam complex-time lobe to an explicit disk, the Hilbert-valued Jensen theorem, the Blaschke anchor obstruction, the component-union tax, the window-cover tax, and the NSE budget audit.
02 · 81 节完整索引 ||| 02 · Complete 81-section index
打开最新节点 R0.71Q ||| Open the latest node, R0.71Q
回顾截止节点：R0.71Q ||| Recap endpoint: R0.71Q
回顾截止时公开笔记：141 ||| Public notes at the recap endpoint: 141
截至 R0.71Q，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 81 个节点解释成对千禧年问题完成了某个比例。 ||| As of R0.71Q, there is no new unconditional continuation criterion, no reduction in the set of all potentially singular solutions, and no proof of finite-time breakdown. The 81 nodes cannot be interpreted as completing any fraction of the Millennium Problem.
累计回顾 · R0.61–R0.71Q · 2026-08-26 ||| Cumulative recap · R0.61–R0.71Q · 2026-08-26
目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、有界重叠局部化、denominator mass 与同刻 spatial batching。R0.71Q 给出了一个可复核的有限条件 Jensen 定理，但它没有将 distinct entry-time counting measure 改写成由 Leray 预算无条件支付的量。现在开放的是 NSE-specific parabolic incidence / Carleson packing，而不是再次套用定性时间解析性。 ||| The strongest substantive unconditional positive results remain the projected-Lamb heat volume at Leray energy level, bounded-overlap localization, denominator mass, and same-time spatial batching. R0.71Q gives a reproducible finite conditional Jensen theorem, but it does not rewrite the counting measure of distinct entry times as a quantity paid unconditionally by the Leray budget. The open problem now is NSE-specific parabolic incidence / Carleson packing, not another application of qualitative time analyticity.
十二个阶段、81 个节点：从约化递推到 projected-Lamb 局部热打包，再到 positive-entry batching、有限条件 Jensen 定理与 anchor、truncation、cover、H-envelope 四税。 ||| Twelve stages and 81 nodes: from reduced recurrences to localized projected-Lamb heat packing, then to positive-entry batching, a finite conditional Jensen theorem, and the four taxes for the anchor, truncation, cover, and H-envelope.
收录节点：81 ||| Nodes included: 81
下一步不再尝试从 analytic radius 与 complex upper bound 单独数零点，而是检查 NSE 方程是否在不同 entry events 之间给出额外的抛物耦合。R0.71R 将把 events 置于局部时空抛物柱中，测试 projected-Lamb、enstrophy 与 incidence measure 能否产生对尺度可求和的 Carleson packing。 ||| The next step will no longer try to count zeros from the analytic radius and complex upper bound alone. Instead, it will test whether the NSE equations provide additional parabolic coupling between distinct entry events. R0.71R will place the events in local spacetime parabolic cylinders and test whether the projected-Lamb, enstrophy, and incidence measures can yield scale-summable Carleson packing.
有限 owned parabolic windows 上的 Hilbert-valued conditional Jensen theorem、Temam lobe 内的显式双边圆盘，以及 anchor、truncation、cover、H-envelope 四税；radius 与 upper bound 单独不能给出 uniform entry packing。 ||| A Hilbert-valued conditional Jensen theorem on finite owned parabolic windows, an explicit two-sided disk inside the Temam lobe, and the four taxes for the anchor, truncation, cover, and H-envelope; the radius and upper bound alone cannot yield uniform entry packing.
这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71Q 的 81 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。 ||| This page follows the stage recap for R0.00–R0.60 and organizes the research nodes from R0.61 through R0.71Q, 81 in total. I record chronologically what each segment actually proved, which proposals were ruled out by specific counterexamples or scaling analysis, and which conditions have not yet been derived from the Navier–Stokes equations.
R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 81 个节点沿着这个缺口推进。 ||| The content of R0.00–R0.60 remains in the previous stage recap. The conclusion of R0.60 is that the full Fourier–Leray structure and higher-order calculations can continue, but they still do not control a critical quantity for general three-dimensional solutions. The subsequent 81 nodes advance along this gap.
R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71Q 的 81 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、有限条件 Jensen 定理与四项 packing 税的路线。 ||| Research recap after R0.60: a chronological account from R0.61 through R0.71Q, covering 81 research nodes and recording the route from reduced recurrences to projected-Lamb heat volume, positive-entry batching, the finite conditional Jensen theorem, and the four packing taxes.
R0.61–R0.71Q 的 81 节公开笔记 ||| Public notes from R0.61–R0.71Q: 81 sections
R0.61–R0.71Q 回顾 · 2026-08-26 ||| R0.61–R0.71Q recap · 2026-08-26
R0.61–R0.71Q 研究节点 ||| R0.61–R0.71Q research nodes
R0.61–R0.71Q｜R0.60 之后的研究回顾 ||| R0.61–R0.71Q | Research recap after R0.60
R0.70A–R0.71Q 完成版本 ||| Completed releases R0.70A–R0.71Q
R0.71G–N 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge 与 signed second jet。R0.71O 证明 soft quotient 恢复 hard 一侧迹，R0.71P 再把同刻 positive entries 合成可由 \(\dot H^{-1}\) Lamb square sum 支付的 spatial batch，剩下 distinct entry-time counting measure。R0.71Q 在固定紧致经典时间区间与有限观测截断上证明 finite conditional Jensen theorem：只有同时给出复时间窗、上界、非零中心值、有限所有权覆盖与窗口内 \(\mathcal H\) 包络，才得到有限 weighted entry bound。定理必须保留 anchor tax、truncation tax、cover tax 与 H-envelope tax。有限 Blaschke 族与多分量族证明 analytic radius 与 complex upper bound 单独无法给出 uniform zero count；因此直接解析零点路线的无条件版本在此失败。 ||| R0.71G–N sequentially checks residence, the matched-cell heat gap, viscous fusion, the increment bridge, and the signed second jet. R0.71O proves that the soft quotient recovers the hard one-sided trace; R0.71P then combines same-time positive entries into a spatial batch payable by the \(\dot H^{-1}\) Lamb square sum, leaving the counting measure of distinct entry times. On a fixed compact classical time interval and a finite observation truncation, R0.71Q proves a finite conditional Jensen theorem: a finite weighted entry bound follows only when a complex-time window, an upper bound, a nonzero central value, a finite ownership cover, and a within-window \(\mathcal H\) envelope are all supplied. The theorem must retain the anchor tax, truncation tax, cover tax, and H-envelope tax. Finite Blaschke and multicomponent families show that the analytic radius and complex upper bound alone cannot yield a uniform zero count; therefore the unconditional version of the direct analytic zero-count route fails here.
R0.71G–R0.71Q · denominator faces、temporal packing 与条件 Jensen ||| R0.71G–R0.71Q · denominator faces, temporal packing, and conditional Jensen
R0.71Q 把直接解析路线的缺口分成四税：Jensen 必须保留 \(\log(M/|f(t_*)|)\) 的 anchor tax；观测量零点并集必须保留 truncation tax；局部圆盘所有权必须保留 cover tax；从零点数转成 weighted entry mass 必须保留 H-envelope tax。Temam 型 analytic radius 与 complex upper bound 只能支付条件定理的一部分；Blaschke 族精确证明这两项单独不能 uniform 控制实零点或正进入数。 ||| R0.71Q decomposes the gap in the direct analytic route into four taxes: Jensen must retain the anchor tax \(\log(M/|f(t_*)|)\); the union of observable zeros must retain the truncation tax; local disk ownership must retain the cover tax; and converting zero counts into weighted entry mass must retain the H-envelope tax. A Temam-type analytic radius and complex upper bound pay only part of the conditional theorem; the Blaschke family proves exactly that these two inputs alone cannot uniformly control real zeros or the number of positive entries.
R0.71R 检查 NSE-specific parabolic incidence / Carleson packing ||| R0.71R examines NSE-specific parabolic incidence / Carleson packing
R0.71R 只接受能在截断扩张和逼近潜在奇性端点时保持一致、且由已经证明的 NSE 预算支付的候选不等式。如果新参数只是重命名后的 anchor、inverse denominator、strong continuation norm 或 target BV，我会明确保留条件并停止。这一步不宣称已解决千禧年问题。 ||| R0.71R accepts only candidate inequalities that remain uniform as the truncation expands and the interval approaches a potential singular endpoint, and that are paid by already proved NSE budgets. If a new parameter is merely a renamed anchor, inverse denominator, strong continuation norm, or target BV, I will explicitly retain the condition and stop. This step does not claim to have solved the Millennium Problem.
本节分类并停止“仅靠时间解析性与复域上界”的直接路线；没有给出 uniform NSE zero count、无限 frame、Leray 极限、继续性或全局正则性结论。反例族不是 NSE 重复进入轨道。 ||| This section classifies and stops the direct route based only on time analyticity and complex-domain upper bounds; it gives no uniform NSE zero count, infinite-frame estimate, Leray limit, continuation result, or global-regularity conclusion. The counterexample families are not NSE trajectories with repeated entries.
从有符号环带障碍走到 complex-time packing method boundary ||| From the signed-annulus obstruction to the boundary of the complex-time packing method
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary ||| Signed-annulus exclusion → source–core ledger → covariance-spectrum stratification → full-frequency conditional bridge → response-slope chord gain → first-order common-response channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → critical obstruction for the material heat tent → projected-Lamb heat-volume closure → localized heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft-denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary
加权目标还有独立的点态账本 \(H_m=\sup_{K_m}\mathcal H\)。Temam 尺度按 \((1+\sup\|u\|_{H^1}^2)^{-2}\) 缩小；若该尺度在潜在奇点端点一致，本身已经是 continuation-level input。 ||| The weighted target also has an independent pointwise ledger \(H_m=\sup_{K_m}\mathcal H\). Temam's scale shrinks like \((1+\sup\|u\|_{H^1}^2)^{-2}\); if this scale remains uniform at a potential singular endpoint, it is already continuation-level input.
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–P 依次核对 residence、matched-cell heat gap、viscous fusion、signed second jet、soft denominator faces 与同刻 spatial batching。R0.71Q 给出有限 Jensen window theorem，并证明 anchor、component union、cover 与 pointwise envelope 仍是未支付账本。 ||| After the static annular family was rigorously excluded, the main line shifted to covariance-rank stratification and the full-frequency projection bridge. R0.71A–F establishes the projected-Lamb heat volume at Leray energy level and its bounded-overlap localization. R0.71G–P then checks residence, the matched-cell heat gap, viscous fusion, the signed second jet, soft-denominator faces, and same-time spatial batching. R0.71Q gives a finite Jensen-window theorem and proves that the anchor, component union, cover, and pointwise envelope remain unpaid ledger items.
累计回顾 R0.61–R0.71Q · 2026-08-26 ||| Cumulative recap R0.61–R0.71Q · 2026-08-26
目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71Q 给出固定有限截断上的条件 Jensen bound，并以精确反例隔离 anchor、component-union 与 cover taxes；它们和点态 batch envelope 尚不能由 Leray 预算统一支付。 ||| There is currently no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71Q gives a conditional Jensen bound on a fixed finite truncation and isolates the anchor, component-union, and cover taxes with exact counterexamples; neither these taxes nor the pointwise batch envelope can yet be paid uniformly by the Leray budget.
三个显式解析族分别隔离缺口：有限 Blaschke 乘积证明固定半径与复上界允许任意多正进入，锚点对数与零点数同阶；线性分量族证明零点并集必须支付截断数；sine-square 族证明局部半径比、增长和相对锚点一致时，ownership cover 数仍可增长。 ||| Three explicit analytic families isolate the gaps: finite Blaschke products show that a fixed radius and complex upper bound permit arbitrarily many positive entries, with the anchor logarithm of the same order as the zero count; a linear component family shows that the zero-set union must pay for the truncation size; and a sine-square family shows that even with uniform local radius ratios, growth, and relative anchors, the number of ownership-cover windows can still grow.
上次综述 v1.01 · 2026-08-26 ||| Previous review v1.01 · 2026-08-26
我回到 componentwise positive parts 之前的 signed precursor/source，检查 PDE 动力学能否耦合不同 observable 的 entry events；候选必须显式支付 anchor、cover、union 与 event-weight 账本。 ||| I return to the signed precursor/source before componentwise positive parts and test whether PDE dynamics can couple entry events of different observables; any candidate must explicitly pay the anchor, cover, union, and event-weight ledgers.
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71Q 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also prepared a separate systematic review that places classical theory, five main strands of the literature, the candidate-elimination tree, progress from 2019—2026, and this site's R0.69P–R0.71Q route in one diagram. The historical nodes R0.61–R0.69O remain in the cumulative recap.
下一步 R0.71R： ||| Next step, R0.71R:
研究笔记 R0.71Q · 2026-08-26 ||| Research note R0.71Q · 2026-08-26
有限 Jensen window theorem 成立；解析半径与复域上界不控制 uniform entry count，必须另外支付 anchor、truncation、cover 与 pointwise event-weight 账本。 ||| The finite Jensen-window theorem holds; the analytic radius and complex-domain upper bound do not control a uniform entry count, so the anchor, truncation, cover, and pointwise event-weight ledgers must be paid separately.
阅读 R0.71Q 研究笔记 → ||| Read research note R0.71Q →
在 componentwise positive parts 之前回到 signed precursor/source，检查 NSE-specific parabolic incidence 或 Carleson packing law；候选必须同时通过 sequential path、Blaschke anchor 与 all-observable union 压力测试。 ||| Before taking componentwise positive parts, return to the signed precursor/source and test for an NSE-specific parabolic incidence or Carleson packing law; any candidate must pass the sequential-path, Blaschke-anchor, and all-observable-union stress tests simultaneously.
在逐分量正部之前回到 signed precursor/source，检查 NSE 动力学是否强迫 parabolic incidence 或 Carleson packing；不再把定性时间解析性当作 uniform count。 ||| Before taking componentwise positive parts, return to the signed precursor/source and test whether NSE dynamics force parabolic incidence or Carleson packing; qualitative time analyticity is no longer treated as a uniform count.
展开 51 篇公开笔记 ||| Expand 51 public notes
综述 v1.02 · 2026-08-26 ||| Review v1.02 · 2026-08-26
Jensen 给出有限条件计数，解析性本身仍不支付时间进入打包 ||| Jensen gives a finite conditional count, but analyticity itself still does not pay for temporal entry packing
R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、positive-entry temporal packing 与 complex-time Jensen method audit。R0.70A–R0.71Q 共 43 个完成版本。 ||| The route after R0.60 has twelve segments: reduced Picard iteration and the shear boundary, transverse perturbations, localized pressure budgets, signed physical annuli, moving labels and source–core duality, deviatoric tensors and finite observations, full-frame covariance, the constant-projection boundary, positive output and the material heat tent, projected-Lamb heat volume, localized heat packing and the critical-trace obstruction, and the residence boundary, fixed matched cells, positive-entry temporal packing, and the complex-time Jensen method audit. R0.70A–R0.71Q contains 43 completed releases.
R0.60 recap 之后的累计回顾收录 81 个节点；全站现有 141 篇公开研究笔记 ||| The cumulative recap after the R0.60 recap contains 81 nodes; the site now has 141 public research notes
R0.71Q 已完成： ||| R0.71Q completed:
Temam 的复时间瓣包含显式双侧圆盘。对固定有限截断和紧经典窗口，Hilbert 值 Jensen 公式与 finite ownership cover 给出 \[ \mathsf S_{\Lambda,+}(K) \le \sum_m H_m\sum_{\alpha\in\Lambda^*} \left\lfloor\frac{\log(M_\alpha/a_{\alpha m})}{\log2}\right\rfloor. \] 这是严格的有限条件定理；右端不是 Leray data 的已知函数。 ||| Temam's complex-time lobe contains an explicit two-sided disk. For a fixed finite truncation and a compact classical window, the Hilbert-valued Jensen formula and finite ownership cover give \[ \mathsf S_{\Lambda,+}(K) \le \sum_m H_m\sum_{\alpha\in\Lambda^*} \left\lfloor\frac{\log(M_\alpha/a_{\alpha m})}{\log2}\right\rfloor. \] This is a rigorous finite conditional theorem; the right-hand side is not a known function of Leray data.
`;

const rawRows = translationRows
  .trim()
  .split("\n")
  .filter((row) => row.length > 0);
const additions = new Map(
  rawRows.map((row) => {
    const separator = " ||| ";
    const index = row.indexOf(separator);
    if (index < 1) throw new Error("invalid translation row: " + row);
    return [row.slice(0, index), row.slice(index + separator.length)];
  }),
);
if (additions.size !== rawRows.length) {
  throw new Error("duplicate Chinese keys in R0.71Q translation rows");
}

function extractNumericTokens(value) {
  return [...String(value).matchAll(/\d+(?:[.\-–—]\d+)*/g)].map(
    (match) => match[0],
  );
}

function sameTokens(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

const activePages = [
  "research-review.html",
  "literature-review.html",
  "recap-r0-61-r0-71q.html",
  "notes/r0-71q.html",
];
for (const relative of activePages) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.02')) {
    throw new Error(relative + ": expected i18n cache version v1.02");
  }
}

const batchId = /^r071q\d+$/;
const currentWithoutBatch = current.filter((entry) => !batchId.test(entry.id));
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error(
    "duplicate Chinese keys already present outside the R0.71Q batch",
  );
}

const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));
if (sourceByChinese.size !== source.length) {
  throw new Error("duplicate Chinese keys in collected site strings");
}

const missing = source.filter((entry) => !currentByChinese.has(entry.zh));
const missingChinese = new Set(missing.map((entry) => entry.zh));
if (additions.size !== missing.length) {
  const uncovered = missing
    .filter((entry) => !additions.has(entry.zh))
    .map((entry) => entry.zh);
  const stale = [...additions.keys()].filter((zh) => !missingChinese.has(zh));
  throw new Error(
    "expected additions to equal the " +
      missing.length +
      " active missing strings, found " +
      additions.size +
      "\nuncovered:\n" +
      uncovered.join("\n---\n") +
      "\nstale rows:\n" +
      stale.join("\n---\n"),
  );
}
for (const entry of missing) {
  if (!additions.has(entry.zh)) {
    throw new Error("missing translation: " + entry.zh);
  }
}
for (const zh of additions.keys()) {
  if (!missingChinese.has(zh)) {
    throw new Error("translation is not an active missing string: " + zh);
  }
}

const translatedEntries = missing.map((entry, index) => {
  const en = additions.get(entry.zh);
  const zhProtected = extractProtectedTokens(entry.zh);
  const enProtected = extractProtectedTokens(en);
  if (!sameTokens(zhProtected, enProtected)) {
    throw new Error(
      "protected-token mismatch for " +
        entry.zh +
        "\nZH " +
        JSON.stringify(zhProtected) +
        "\nEN " +
        JSON.stringify(enProtected),
    );
  }

  const zhNumeric = extractNumericTokens(entry.zh);
  const enNumeric = extractNumericTokens(en);
  if (!sameTokens(zhNumeric, enNumeric)) {
    throw new Error(
      "numeric-token mismatch for " +
        entry.zh +
        "\nZH " +
        JSON.stringify(zhNumeric) +
        "\nEN " +
        JSON.stringify(enNumeric),
    );
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error(
      "blank or Chinese-containing English translation for " + entry.zh,
    );
  }
  if (/\b(?:we|our|ours|us)\b/i.test(en)) {
    throw new Error("first-person plural voice in translation for " + entry.zh);
  }

  return {
    ...entry,
    id: "r071q" + String(index + 1).padStart(3, "0"),
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
    !sameTokens(
      extractProtectedTokens(entry.zh),
      extractProtectedTokens(entry.en),
    ),
);
if (invalid.length) {
  throw new Error(
    "invalid translations after merge: " +
      invalid.map((entry) => entry.id).join(", "),
  );
}

await writeFile(translationPath, JSON.stringify(merged, null, 2) + "\n");
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
      englishWithChinese: translatedEntries.filter((entry) =>
        containsChinese(entry.en),
      ).length,
      firstPersonPlural: translatedEntries.filter((entry) =>
        /\b(?:we|our|ours|us)\b/i.test(entry.en),
      ).length,
      protectedTokenMismatches: translatedEntries.filter(
        (entry) =>
          !sameTokens(
            extractProtectedTokens(entry.zh),
            extractProtectedTokens(entry.en),
          ),
      ).length,
      numericTokenMismatches: translatedEntries.filter(
        (entry) =>
          !sameTokens(
            extractNumericTokens(entry.zh),
            extractNumericTokens(entry.en),
          ),
      ).length,
    },
    null,
    2,
  ),
);
