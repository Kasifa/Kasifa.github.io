import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
  extractTranslatableStrings,
} from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const noteRelative = "notes/r0-71s.html";
let source = await collectSiteStrings(publicDirectory);

// The note generator may be ready before the generated page in a parallel
// release.  Use the exact String.raw template as the temporary source, then
// naturally fall back to collectSiteStrings once the page exists.
try {
  await readFile(resolve(publicDirectory, noteRelative), "utf8");
} catch (error) {
  if (error?.code !== "ENOENT") throw error;
  const generator = await readFile(
    resolve(root, "scripts/generate-r071s-note.mjs"),
    "utf8",
  );
  const match = generator.match(/const html = String\.raw`([\s\S]*?)`;\n/);
  if (!match) throw new Error("R0.71S note template not found");
  const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));
  for (const zh of extractTranslatableStrings(match[1])) {
    if (!sourceByChinese.has(zh)) {
      sourceByChinese.set(zh, { zh, count: 1, files: [noteRelative] });
    }
  }
  source = [...sourceByChinese.values()];
}

const current = JSON.parse(await readFile(translationPath, "utf8"));

const translationRows = String.raw`
打开 83 节完整索引 ||| Open the complete 83-section index
给 distribution pairings、smoothed samples 与 trace threshold， ||| provides distribution pairings, smoothed samples, and the trace threshold;
给 evolution endpoint pairing。它们不把 adaptive zero entry 变成由 bare Leray budget 支付的 uniform lower packet。普通 Leray–Hopf bounds 直接只给 L in L_t^(4/3) H_x^-1，不给 L_t^2 H_x^-1。两轮限定检索未找到完整 R0.71S theorem；这是 bounded negative finding，不是原创性、优先权或不存在性结论。 ||| provides evolution endpoint pairing. These results do not turn an adaptive zero entry into a uniform lower packet paid by the bare Leray budget. Standard Leray–Hopf bounds directly give only L in L_t^(4/3) H_x^-1, not L_t^2 H_x^-1. Two bounded search rounds found no complete R0.71S theorem; this is a bounded negative finding, not a claim of originality, priority, or nonexistence.
给 tent/Carleson integration， ||| provides tent/Carleson integration;
给临界 parabolic bilinear map， ||| provides the critical parabolic bilinear map;
开放接口 · R0.71T ||| Open interface · R0.71T
累计回顾与 83 节索引 ||| Cumulative recap and 83-section index
排除 initial observation faces 后，检查 localized Lamb–vorticity coupling 是否给 internal zero 一个与原子同尺度、不是裸 dt 积分的 dynamical charge。 ||| After excluding initial observation faces, test whether localized Lamb–vorticity coupling gives an internal zero a dynamical charge at the same scale as the atom, rather than a bare dt integral.
文献综述 v1.04 · 2026-08-26 ||| Literature review v1.04 · 2026-08-26
我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.71S 只列为研究笔记。我不把计算或笔记外推成正则性定理。 ||| I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.71S material only as research notes. I do not extrapolate calculations or notes into regularity theorems.
中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–R 给出 finite conditional Jensen 与 incidence theorems。R0.71S 再证明非零均值 directional packet 的 κ² Bessel 税，并用 genuine NSE initial-face scaling 排除 observation-boundary 版本的 bare Leray-time-integral 终局。保留下来的结果都不是全局正则性结论。 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary, and R0.71Q–R gives finite conditional Jensen and incidence theorems. R0.71S then proves the κ² Bessel tax for a nonzero-mean directional packet and uses genuine NSE initial-face scaling to rule out the observation-boundary version of the bare Leray-time-integral endpoint. None of the retained results is a global regularity theorem.
finite directional-packet theorem 成立，但单包对角、same-direction Gram clustering、frozen-denominator backward heat 与限定 normalized bilinear kernels 都保留两阶或事件密度代价。variable \(Y\) 的归一化项不属于该线性模型。genuine NSE initial-face scaling 排除 observation-boundary 版本的 bare Leray-time-integral 终局；internal entries 不在该 no-go 范围。 ||| The finite directional-packet theorem holds, but the single-packet diagonal, same-direction Gram clustering, frozen-denominator backward heat, and the specified normalized bilinear kernels all retain a two-order or event-density cost. The normalization terms from variable \(Y\) are outside this linear model. Genuine NSE initial-face scaling rules out the observation-boundary version of the bare Leray-time-integral endpoint; internal entries are outside this no-go result.
nonzero-mean packet 保留 κ² Bessel 税 ||| A nonzero-mean packet retains the κ² Bessel tax
R0.71S 保留 entry direction 与 signed pairing。finite directional-packet theorem 在 sampling coherence、uniform positive parabolic height 与 finite Bessel hypotheses 下成立；但 critical analysis vector 的单包对角已经给 B_crit>=kappa^2，同向聚簇再使 Gram constant 按事件密度增长。frozen-denominator backward heat 与一类 normalized bilinear temporal kernels 不消去该两阶；variable \(Y\) 会带来额外归一化项，不能由这个线性模型处理。mean-zero/signed cancellation 则漏掉常值 directional signal 与 even touch。R0.71O 的 genuine NSE initial face 经 covariant scaling 后保持 weighted atom 不变，而 bare Leray time integral 按 lambda^-2 缩小。因此 observation-boundary 版本的原目标 + bare time integral 终局停止。R0.71T 只检查 internal entries 与 scale-zero dynamical charge。我继续用下面六条筛选。 ||| R0.71S retains the entry direction and signed pairing. The finite directional-packet theorem holds under sampling coherence, a uniform positive parabolic height, and finite Bessel hypotheses; however, the single-packet diagonal of the critical analysis vector already gives B_crit>=kappa^2, and same-direction clustering makes the Gram constant grow with event density. Frozen-denominator backward heat and a class of normalized bilinear temporal kernels do not remove this two-order cost; variable \(Y\) introduces additional normalization terms that this linear model does not handle. Mean-zero/signed cancellation instead misses a constant directional signal and an even touch. The genuine NSE initial face from R0.71O keeps its weighted atom invariant under covariant scaling, while the bare Leray time integral shrinks as lambda^-2. The observation-boundary endpoint based on the original target + bare time integral therefore stops here. R0.71T tests only internal entries and a scale-zero dynamical charge. I continue to use the following six filters.
R0.71S 的一手文献边界 ||| Primary-literature boundary for R0.71S
R0.71S 关闭了什么，R0.71T 只检查什么 ||| What R0.71S closes, and what R0.71T alone tests
02 · 83 节完整索引 ||| 02 · Complete 83-section index
保留下来的无条件结构仍包括 Leray 能量级 projected-Lamb 热体积、有界重叠局部化、denominator mass、同刻 spatial batching，以及 R0.71R 在 rho=2 下由 Leray energy 支付的 truncation-uniform source integral。R0.71S 新增的是一个 finite conditional directional-packet theorem 和精确 method bounds：packet coherence 与 complete Bessel inequality 是 hypotheses；单 packet 对角已经强迫 \(B_{\rm crit}\ge\kappa_j^2\)，不能由更好的 overlap estimate 删除。 ||| The retained unconditional structures still include the projected-Lamb heat volume at the Leray energy level, bounded-overlap localization, denominator mass, same-time spatial batching, and, in R0.71R at rho=2, the truncation-uniform source integral paid by Leray energy. R0.71S adds a finite conditional directional-packet theorem and exact method bounds: packet coherence and the complete Bessel inequality are hypotheses; the single-packet diagonal already forces \(B_{\rm crit}\ge\kappa_j^2\), and a better overlap estimate cannot remove it.
打开最新节点 R0.71S ||| Open the latest node R0.71S
回顾截止节点：R0.71S ||| Recap endpoint: R0.71S
回顾截止时公开笔记：143 ||| Public notes at recap endpoint: 143
截至 R0.71S，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 83 个节点解释成对千禧年问题完成了某个比例。 ||| At R0.71S, there is no new unconditional continuation criterion, no narrowing of the set of all potential singular solutions, and no proof of finite-time breakdown. The 83 nodes cannot be interpreted as completing any percentage of the Millennium Problem.
累计回顾 · R0.61–R0.71S · 2026-08-26 ||| Cumulative recap · R0.61–R0.71S · 2026-08-26
任何 internal-entry 结论都必须先证明相应 NSE event 确实存在，并保留 localization commutator、recurrence 与 endpoint availability；不能从 initial face 外推。任何新右端都必须单独证明由 NSE 预算支付。R0.71T 仍是有限方法检查，不宣称继续性、奇性排除或全局正则性。 ||| Any internal-entry conclusion must first prove that the corresponding NSE event actually exists and must retain the localization commutator, recurrence, and endpoint availability; it cannot be extrapolated from an initial face. Any new right-hand side must be proved separately to be paid by an NSE budget. R0.71T remains a finite method test and makes no claim of continuation, singularity exclusion, or global regularity.
十二个阶段、83 个节点：从约化递推到 conditional incidence，再到 directional packets、critical Bessel tax 与只覆盖 NSE initial observation boundary 的 scaling no-go。 ||| Twelve stages and 83 nodes: from reduced recurrences to conditional incidence, then directional packets, the critical Bessel tax, and a scaling no-go covering only the NSE initial observation boundary.
收录节点：83 ||| Included nodes: 83
在 original scale-invariant positive-entry target、nonzero-mean linear 或 bounded bilinear temporal packet、以及 bare \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\) payment 这一声明类内，两阶错配仍然存在。R0.71S 的 genuine NSE scaling theorem 只排除包含 initial observation-boundary entry 的 scale-uniform payment：它没有构造 internal NSE entry，没有排除 internal-entry nonlinear identity，也没有排除加入 scale-\(+2\) dynamical charge 的不同右端。 ||| Within the declared class consisting of the original scale-invariant positive-entry target, a nonzero-mean linear or bounded bilinear temporal packet, and payment by the bare \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\), the two-order mismatch remains. The genuine NSE scaling theorem in R0.71S rules out only scale-uniform payment that includes an initial observation-boundary entry: it constructs no internal NSE entry, rules out no internal-entry nonlinear identity, and does not rule out a different right-hand side containing a scale-\(+2\) dynamical charge.
这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71S 的 83 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。 ||| This page follows the R0.00–R0.60 stage recap and organizes the research nodes from R0.61 through R0.71S, 83 in total. I record chronologically what each stage actually proves, which proposals are excluded by specific counterexamples or scaling analyses, and which conditions have not been derived from the Navier–Stokes equations.
finite conditional directional-packet payment、critical Bessel diagonal 与 repeated-packet lower bounds、necessary directional Carleson condition、backward-heat kernel 和 bounded bilinear constant-mode dichotomy；genuine NSE scaling no-go 只覆盖 initial observation-boundary entry，不覆盖 internal entries。 ||| finite conditional directional-packet payment; the critical Bessel diagonal and repeated-packet lower bounds; the necessary directional Carleson condition; the backward-heat kernel; and the bounded bilinear constant-mode dichotomy; the genuine NSE scaling no-go covers only an initial observation-boundary entry, not internal entries.
R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 83 个节点沿着这个缺口推进。 ||| The R0.00–R0.60 material remains in the previous stage recap. R0.60 concludes that the full Fourier–Leray structure and higher-order calculations can continue, but still do not control a critical quantity for general three-dimensional solutions. The subsequent 83 nodes advance along this gap.
R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71S 的 83 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 incidence theorem，以及 packet/Bessel 与 NSE initial-face scaling 边界的路线。 ||| Research recap after R0.60: a chronological account from R0.61 through R0.71S, covering 83 research nodes and recording the route from reduced recurrences to projected-Lamb heat volume, positive-entry batching, the conditional incidence theorem, and the packet/Bessel and NSE initial-face scaling boundaries.
R0.61–R0.71S 的 83 节公开笔记 ||| Public notes from R0.61–R0.71S: 83 sections
R0.61–R0.71S 回顾 · 2026-08-26 ||| R0.61–R0.71S recap · 2026-08-26
R0.61–R0.71S 研究节点 ||| R0.61–R0.71S research nodes
R0.61–R0.71S｜R0.60 之后的研究回顾 ||| R0.61–R0.71S | Research recap after R0.60
R0.70A–R0.71S 完成版本 ||| Completed releases R0.70A–R0.71S
R0.71G–R0.71S · temporal packing、incidence 与 packet/Bessel scale audit ||| R0.71G–R0.71S · temporal packing, incidence, and packet/Bessel scale audit
R0.71O–P 恢复 soft quotient 的一侧 traces，并用同刻 spatial batching 吸收有限 frame multiplicity；R0.71Q–R 给出带四税的 finite conditional Jensen theorem、localized forced heat equation、conditional incidence packing 和 rho=0/rho=2 source ledger。R0.71S 保留 entry direction，证明 finite conditional directional-packet payment：nonzero-mean packet 只有在 directional sampling coherence 与 complete indexed Bessel inequality 同时成立时才支付有限 entry family。critical packet 的对角范数平方是 \(\kappa_j^2\)，所以 \(B_{\rm crit}\ge\max\kappa_j^2\)，重复同一 packet \(N\) 次还要求 \(B_{\rm crit}\ge N\kappa_j^2\)；frozen-denominator backward-heat model 改变核形状但不移除该因子；variable \(Y\) 的归一化项未纳入这个线性模型。bounded bilinear kernel 若消去 constant mode，就看不见 constant leading trace 与 even positive touch；若保留 constant mode，就支付同一 \(\kappa_j^2\) 税。genuine NSE covariant family 进一步证明：只要目标包含 initial observation-boundary entry，scale-invariant entry atom 保持不变，而 bare \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\) 按 \(\lambda^{-2}\) 缩放，因而不存在 scale-uniform payment。该结论不覆盖 internal entries，不是所有 nonlinear signed identities 的 impossibility theorem，也不证明继续性或正则性。 ||| R0.71O–P recovers one-sided traces of the soft quotient and uses same-time spatial batching to absorb finite frame multiplicity. R0.71Q–R gives a finite conditional Jensen theorem with four taxes, the localized forced heat equation, conditional incidence packing, and the rho=0/rho=2 source ledger. R0.71S retains the entry direction and proves finite conditional directional-packet payment: a nonzero-mean packet pays a finite entry family only when directional sampling coherence and the complete indexed Bessel inequality both hold. The squared diagonal norm of the critical packet is \(\kappa_j^2\), so \(B_{\rm crit}\ge\max\kappa_j^2\); repeating the same packet \(N\) times further requires \(B_{\rm crit}\ge N\kappa_j^2\). The frozen-denominator backward-heat model changes the kernel shape but does not remove this factor; the normalization terms from variable \(Y\) are not included in this linear model. If a bounded bilinear kernel cancels the constant mode, it cannot see a constant leading trace or an even positive touch; if it retains the constant mode, it pays the same \(\kappa_j^2\) tax. The genuine covariant NSE family further proves that when the target includes an initial observation-boundary entry, the scale-invariant entry atom remains fixed while the bare \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\) scales as \(\lambda^{-2}\), so no scale-uniform payment exists. This conclusion does not cover internal entries, is not an impossibility theorem for all nonlinear signed identities, and proves no continuation or regularity result.
R0.71R 附图 ||| R0.71R figure
R0.71S 附图 ||| R0.71S figure
R0.71S 证书 ||| R0.71S certificates
R0.71T 检查 internal-entry NSE identity 与 scale-invariant charge ||| R0.71T tests an internal-entry NSE identity and a scale-invariant charge
R0.71T 将把 initial observation boundary 与 internal entry 分开。第一条有限路线是只研究 internal entries，推导依赖完整 NSE 演化、而不是 generic temporal Bessel estimate 的 nonlinear identity；第二条路线是保留完整 entry target，但寻找真正 scale invariant 的 dynamical right side，不再使用 scale exponent 为 \(-2\) 的 bare time integral。 ||| R0.71T will separate the initial observation boundary from an internal entry. The first finite route studies only internal entries and derives a nonlinear identity that depends on the full NSE evolution rather than a generic temporal Bessel estimate. The second retains the complete entry target but seeks a genuinely scale-invariant dynamical right-hand side, no longer using a bare time integral with scale exponent \(-2\).
本节关闭的是原目标由 bare Leray time integral 支付的这一类 temporal-packet 方案。genuine NSE no-go 包含 initial observation face，不覆盖只计算 internal entries 的定理；这里没有构造 NSE 多进入轨道，也没有得到 continuation、singularity 或 global regularity。 ||| This section closes the class of temporal-packet schemes in which the original target is paid by the bare Leray time integral. The genuine NSE no-go includes an initial observation face and does not cover theorems that count only internal entries; no NSE multiple-entry trajectory, continuation result, singularity result, or global regularity result is obtained here.
从有符号环带障碍走到 signed-packet scale–Bessel boundary ||| From the signed-annulus obstruction to the signed-packet scale–Bessel boundary
对 \(h_\beta=\theta_\beta\kappa_{j_\beta}^{-2}\) 的 directional packet，sampling coherence 与有限 Bessel hypothesis 给出 \[ \sum_\beta a_\beta \le \frac{B_{\rm crit}}{\mu^2(1-\delta)^2\theta_-} \int\sum_j\kappa_j^{-2}\frac{\|F_j\|_2^2}{Y}\,dt. \] 这是严格的 finite conditional theorem；sampling coherence、统一正 \(\theta_-\) 与 \(B_{\rm crit}\) 都没有从 NSE 中自动推出。 ||| For a directional packet with \(h_\beta=\theta_\beta\kappa_{j_\beta}^{-2}\), sampling coherence and a finite Bessel hypothesis give \[ \sum_\beta a_\beta \le \frac{B_{\rm crit}}{\mu^2(1-\delta)^2\theta_-} \int\sum_j\kappa_j^{-2}\frac{\|F_j\|_2^2}{Y}\,dt. \] This is a rigorous finite conditional theorem; sampling coherence, a uniformly positive \(\theta_-\), and \(B_{\rm crit}\) have not been derived automatically from NSE.
非零均值 packet 的单包对角精确满足 \(B_{\rm crit}\ge\kappa_j^2\)。同向聚簇事件的最优有限常数是 Gram 矩阵的最大特征值，并随事件密度增长。反向热伴随对未归一化方向源 \(g=\langle F,e\rangle\) 的 strong norm 为常数；在 frozen-denominator 模型中，相对 Leray-order input \(\kappa^{-1}g\) 精确带回 \(\kappa^2\)。variable \(Y\) 还会产生 \(\sqrt Y\) 或 \(Y_t/(2Y)\) 项。一类 normalized bilinear temporal kernels 服从同一二分：非零均值看见 entry 并支付两阶；零均值漏掉常值 directional signal。even touch 还使双侧 signed face 完全抵消。 ||| The single-packet diagonal of a nonzero-mean packet satisfies exactly \(B_{\rm crit}\ge\kappa_j^2\). The optimal finite constant for same-direction clustered events is the largest eigenvalue of the Gram matrix and grows with event density. The backward-heat adjoint has constant strong norm for the unnormalized directional source \(g=\langle F,e\rangle\); in the frozen-denominator model, relative to the Leray-order input \(\kappa^{-1}g\), it recovers exactly the \(\kappa^2\) factor. Variable \(Y\) also produces \(\sqrt Y\) or \(Y_t/(2Y)\) terms. A class of normalized bilinear temporal kernels obeys the same dichotomy: nonzero mean sees the entry and pays two orders, while zero mean misses a constant directional signal. An even touch also makes the two-sided signed face cancel completely.
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary ||| Annular exclusion → source–core ledger → covariance-spectrum stratification → full-frequency conditional bridge → response-slope chord gain → first-order common-response channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → critical material heat-tent obstruction → projected-Lamb heat-volume closure → localized heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–P 建立 projected-Lamb 热体积、局部化、denominator faces 与同刻 spatial batching。R0.71Q–R 依次给出 finite conditional Jensen 与 incidence theorems。R0.71S 证明非零均值 signed/directional packet 的最优 Bessel 常数单包即带 κ²；frozen-denominator 反向热模型与一类 normalized bilinear kernels 不消去该代价。真实 NSE initial face 的协变缩放排除“原目标 + bare Leray time integral”的 observation-boundary 终局。 ||| After the static annular family was rigorously excluded, the main line shifted to covariance-rank stratification and the full-frequency projection bridge. R0.71A–P establishes projected-Lamb heat volume, localization, denominator faces, and same-time spatial batching. R0.71Q–R then gives finite conditional Jensen and incidence theorems. R0.71S proves that the optimal Bessel constant for a nonzero-mean signed/directional packet already carries κ² for one packet; the frozen-denominator backward-heat model and a class of normalized bilinear kernels do not remove this cost. Covariant scaling of a genuine NSE initial face rules out the observation-boundary endpoint based on the original target + bare Leray time integral.
累计回顾 R0.61–R0.71S · 2026-08-26 ||| Cumulative recap R0.61–R0.71S · 2026-08-26
目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71S 的 finite directional-packet theorem 保留 sampling coherence、uniform positive height 与 Bessel hypotheses；单包 κ² lower bound、Gram clustering、frozen-denominator backward-heat exact norm 与 bilinear mean dichotomy 证明 bare Leray time integral 不能以尺度统一常数支付原目标。真实 NSE scaling 结论只覆盖 initial observation face；internal entries 仍开放。 ||| There is currently no new unconditional continuation criterion and no construction of a finite-time singularity. The finite directional-packet theorem in R0.71S retains sampling coherence, a uniform positive height, and Bessel hypotheses; the single-packet κ² lower bound, Gram clustering, exact frozen-denominator backward-heat norm, and bilinear mean dichotomy prove that the bare Leray time integral cannot pay the original target with a scale-uniform constant. The genuine NSE scaling conclusion covers only an initial observation face; internal entries remain open.
上次综述 v1.03 · 2026-08-26 ||| Previous review v1.03 · 2026-08-26
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71S 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also prepared a separate systematic review that places classical theory, five main strands of the literature, the candidate-elimination tree, progress from 2019—2026, and this site's R0.69P–R0.71S route in one diagram. The historical nodes R0.61–R0.69O remain in the cumulative recap.
下一步 R0.71T： ||| Next step, R0.71T:
先排除 observation-boundary faces，只检查紧经典区间内部的 entries。候选 RHS 必须与 entry 原子同尺度，不能只是裸 \(dt\) 积分，也不能把 κ² 隐藏进 Bessel 常数。 ||| First exclude observation-boundary faces and test only entries in a compact classical interval. A candidate right-hand side must have the same scale as the entry atom, cannot be only a bare \(dt\) integral, and cannot hide κ² inside the Bessel constant.
研究笔记 R0.71S · 2026-08-26 ||| Research note R0.71S · 2026-08-26
移除 observation-boundary faces，只检查 internal entries 是否携带一个与 entry 原子同尺度、不是裸 \(dt\) 积分的 NSE-specific dynamical charge。 ||| Remove observation-boundary faces and test only whether internal entries carry an NSE-specific dynamical charge at the same scale as the entry atom and not a bare \(dt\) integral.
移除 observation-boundary faces，只检查 internal entries 是否携带与原子同尺度的 NSE-specific dynamical charge；不再用裸 \(\dot H^{-1}\)-Lamb 时间积分支付尺度零目标。 ||| Remove observation-boundary faces and test only whether internal entries carry an NSE-specific dynamical charge at the same scale as the atom; no longer use the bare \(\dot H^{-1}\)-Lamb time integral to pay a scale-zero target.
阅读 R0.71S 研究笔记 → ||| Read research note R0.71S →
展开 53 篇公开笔记 ||| Expand 53 public notes
综述 v1.04 · 2026-08-26 ||| Review v1.04 · 2026-08-26
nonzero-mean directional packet、frozen-denominator backward heat 与限定 normalized bilinear kernels 都保留 κ² Bessel 税；genuine NSE initial-face scaling 排除原目标由 bare Leray time integral 统一支付的 observation-boundary 终局。 ||| The nonzero-mean directional packet, frozen-denominator backward heat, and the specified normalized bilinear kernels all retain the κ² Bessel tax; genuine NSE initial-face scaling rules out the observation-boundary endpoint in which the original target is paid uniformly by the bare Leray time integral.
R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen、parabolic incidence 与 signed-packet scale–Bessel audit。R0.70A–R0.71S 共 45 个完成版本。 ||| The route after R0.60 has twelve segments: reduced Picard and the shear boundary, transverse perturbations, local pressure budgets, signed physical annuli, moving labels and source–core duality, deviation tensors and finite observations, full-frame covariance, the constant-projection boundary, positive output and the material heat tent, projected-Lamb heat volume, localized heat packing and the critical trace obstruction, and positive-entry temporal packing, conditional Jensen, parabolic incidence, and the signed-packet scale–Bessel audit. R0.70A–R0.71S contains 45 completed releases.
R0.60 recap 之后的累计回顾收录 83 个节点；全站现有 143 篇公开研究笔记 ||| The cumulative recap after the R0.60 recap includes 83 nodes; the site now has 143 public research notes
R0.71O 的真实 smooth NSE initial face 经 compatible integer/dyadic dilation 后，\(\kappa^{-2}A_+=1/4\) 保持不变，而 bare \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\) 缩小为 \(\lambda^{-2}\)。因此，包含 observation-boundary entry、使用 covariant windows、且常数独立尺度的“原 positive-entry 目标 \(\le\) 裸时间积分”终局不可能成立。 ||| After compatible integer/dyadic dilation, the genuine smooth NSE initial face from R0.71O keeps \(\kappa^{-2}A_+=1/4\) invariant, while the bare \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\) shrinks by \(\lambda^{-2}\). Therefore an endpoint that includes an observation-boundary entry, uses covariant windows, and asserts the original positive-entry target \(\le\) the bare time integral with a scale-independent constant cannot hold.
R0.71S 已完成： ||| R0.71S completed:
signed packet 能看见 entry，但裸 Leray 时间积分仍少两阶 ||| A signed packet can see the entry, but the bare Leray time integral remains two orders short
研究笔记 R0.71S：有限 directional-packet theorem 成立；非零均值抛物 packet 的最优 Bessel 常数至少带 kappa 平方；冻结分母的反向热模型与一类归一化双线性核不能消去该代价；真实 NSE 初始 face 的协变缩放排除由裸 Leray 时间积分统一支付原目标。 ||| Research note R0.71S: the finite directional-packet theorem holds; the optimal Bessel constant for a nonzero-mean parabolic packet carries at least kappa squared; neither the frozen-denominator backward-heat model nor a class of normalized bilinear kernels removes that cost; covariant scaling of a genuine NSE initial face rules out uniform payment of the original target by the bare Leray time integral.
R0.71S｜signed packet 看见 entry，但裸 Leray 时间积分仍少两阶 ||| R0.71S | A signed packet sees the entry, but the bare Leray time integral remains two orders short
有限 packet 定理、精确 Gram–Bessel 常数、反向热伴随、even-touch 二分与真实 NSE 初始面缩放边界。 ||| Finite packet theorem, exact Gram–Bessel constant, backward-heat adjoint, even-touch dichotomy, and the genuine NSE initial-face scaling boundary.
Bessel 障碍 ||| Bessel obstruction
热伴随 ||| Heat adjoint
双线性二分 ||| Bilinear dichotomy
NSE 缩放 ||| NSE scaling
研究笔记 R0.71S · SIGNED PACKET · BESSEL AUDIT ||| Research note R0.71S · SIGNED PACKET · BESSEL AUDIT
signed packet 保留 entry direction， ||| The signed packet retains the entry direction,
但裸 Leray 时间积分仍少两阶 ||| but the bare Leray time integral remains two orders short
R0.71R 只排除了 endpoint-square、termwise source-square certificate。本节直接保留 \(e_\beta=c_\beta/\|c_\beta\|_2\) 与 signed pairing。有限 directional-packet theorem 可以严格证明；但任何能看见常值 directional signal 的非零均值抛物 packet，单包就需要至少 κ² 的最优 Bessel 常数。冻结分母的反向热模型和一类归一化双线性核保留同一代价；variable \(Y\) 另有归一化项。真实 NSE 初始 face 的协变缩放进一步排除“原目标只由裸 \(\dot H^{-1}\)-Lamb 时间积分以尺度统一常数支付”的方案。 ||| R0.71R rules out only the endpoint-square, termwise source-square certificate. This section directly retains \(e_\beta=c_\beta/\|c_\beta\|_2\) and the signed pairing. A finite directional-packet theorem can be proved rigorously, but any nonzero-mean parabolic packet that sees a constant directional signal requires an optimal Bessel constant carrying at least κ² for a single packet. The frozen-denominator backward-heat model and a class of normalized bilinear kernels retain the same cost; variable \(Y\) has separate normalization terms. Covariant scaling of a genuine NSE initial face further rules out a scheme in which the original target is paid solely by the bare \(\dot H^{-1}\)-Lamb time integral with a scale-uniform constant.
状态 · R0.71S 有限定理与方法边界完成 ||| Status · R0.71S finite theorem and method boundary completed
方法边界 ||| Method boundary
版本 v0.71S · 2026-08-26 ||| Version v0.71S · 2026-08-26
下一对象：internal-entry dynamical charge ||| Next object: internal-entry dynamical charge
01 · 目标与尺度 ||| 01 · Target and scaling
02 · 有限条件定理 ||| 02 · Finite conditional theorem
03 · 对角与 Gram ||| 03 · Diagonal and Gram matrix
04 · 反向热伴随 ||| 04 · Backward-heat adjoint
05 · 双线性与 even touch ||| 05 · Bilinear packet and even touch
06 · 真实 NSE 缩放 ||| 06 · Genuine NSE scaling
08 · 双重审计 ||| 08 · Dual audit
13 · 复现 ||| 13 · Reproduction
看见常值 entry 与 H⁻¹-uniform Bessel payment 不能同时成立 ||| Seeing a constant entry and obtaining H⁻¹-uniform Bessel payment are incompatible
对本节精确定义的 linear directional packets 与 normalized quadratic temporal kernels，存在一个严格二分：非零均值使 packet 能校正常值 entry，却强制最优常数至少按 κ² 增长；零均值消去该对角项，却对常值 directional signal 给出零。even touch 又使双侧 signed face 完全抵消。该结论关闭“原 positive-entry 目标 + 裸 Leray 时间积分”的这类 packet 终局，不关闭 internal entries 专属的 NSE 恒等式或带额外尺度权的动力学 charge。 ||| For the linear directional packets and normalized quadratic temporal kernels defined in this section, there is a strict dichotomy: nonzero mean lets a packet calibrate a constant entry but forces the optimal constant to grow at least as κ²; zero mean removes that diagonal term but gives zero on a constant directional signal. An even touch also makes the two-sided signed face cancel completely. This conclusion closes this packet endpoint based on the original positive-entry target + bare Leray time integral, but does not close NSE identities specific to internal entries or a dynamical charge with an additional scale weight.
这里没有得到新的无条件继续性判据，也没有构造有限时奇性。结论是方法分类，不是对三维 Navier–Stokes 全局正则性的证明。 ||| No new unconditional continuation criterion is obtained here, and no finite-time singularity is constructed. The conclusion classifies a method; it is not a proof of global regularity for three-dimensional Navier–Stokes.
entry 原子尺度为零，裸时间预算缩小两阶 ||| The entry atom has scale zero, while the bare time budget shrinks by two orders
取 \(h_\beta=\theta_\beta\kappa_{j_\beta}^{-2}\)。在 normalized torus 的 compatible integer/dyadic NSE dilation 下，κ 的尺度是 \(+1\)，\(f\) 的尺度是 \(+1\)，所以 \(a_\beta\) 不变；而 ||| Set \(h_\beta=\theta_\beta\kappa_{j_\beta}^{-2}\). Under a compatible integer/dyadic NSE dilation on the normalized torus, κ has scale \(+1\) and \(f\) has scale \(+1\), so \(a_\beta\) is invariant; meanwhile,
缩放为原来的 λ⁻²。任何尺度统一的终局必须说明这两个量之间缺少的两阶来自哪里。 ||| scales to λ⁻² of its original value. Any scale-uniform endpoint must explain the missing two orders between these quantities.
在 sampling coherence 与 Bessel hypothesis 下，有限目标确实可支付 ||| Under sampling coherence and a Bessel hypothesis, the finite target can indeed be paid
令 η∈L²(0,1)、‖η‖₂=1、μ=∫η>0，并定义 ||| Let η∈L²(0,1), ‖η‖₂=1, and μ=∫η>0, and define
若 \(p_\beta\ge(1-\delta)\mu\sqrt{h_\beta}\,f_\beta(t_\beta)>0\)，且 critical analysis vectors 在 \(L_t^2(\bigoplus_jL_x^2)\) 中的有限 Bessel 常数为 \(B_{\rm crit}\)，则 ||| If \(p_\beta\ge(1-\delta)\mu\sqrt{h_\beta}\,f_\beta(t_\beta)>0\), and if the critical analysis vectors in \(L_t^2(\bigoplus_jL_x^2)\) have finite Bessel constant \(B_{\rm crit}\), then
证明只有三步：sampling lower bound、有限 Bessel inequality、Littlewood–Paley \(\dot H^{-1}\) square sum。sampling coherence、统一 θ₋ 与 \(B_{\rm crit}\) 都是 hypotheses；该有限定理本身不是 temporal-packing theorem。 ||| The proof has only three steps: the sampling lower bound, the finite Bessel inequality, and the Littlewood–Paley \(\dot H^{-1}\) square sum. Sampling coherence, a uniform θ₋, and \(B_{\rm crit}\) are all hypotheses; the finite theorem itself is not a temporal-packing theorem.
单包已经强制 κ²；同向聚簇再强制事件数 ||| One packet already forces κ²; same-direction clustering also forces the event count
critical analysis vector 含有一个 κ 因子，因此精确对角范数为 ||| The critical analysis vector contains a κ factor, so its exact diagonal norm is
对长度 \(h\) 的 L²-normalized box packets，Gram 矩阵满足 ||| For L²-normalized box packets of length \(h\), the Gram matrix satisfies
最优有限 Bessel 常数正是 \(\lambda_{\max}(G)\)。若 \(N\) 个同向中心落在长度 εh 的簇中，则 \(\lambda_{\max}(G)\ge N(1-\varepsilon)\)；critical family 因而至少支付 \(N(1-\varepsilon)\kappa^2\)。这不是数值拟合，而是全一向量的 Rayleigh quotient。 ||| The optimal finite Bessel constant is exactly \(\lambda_{\max}(G)\). If \(N\) same-direction centers lie in a cluster of length εh, then \(\lambda_{\max}(G)\ge N(1-\varepsilon)\); the critical family therefore pays at least \(N(1-\varepsilon)\kappa^2\). This is not a numerical fit but the Rayleigh quotient of the all-ones vector.
去掉 κ 因子可把单包对角降到常数，但右端随即变成 normalized L²-Lamb budget，而不是 Leray 支付的 H⁻¹ budget。 ||| Removing the κ factor reduces the single-packet diagonal to a constant, but the right-hand side then becomes the normalized L²-Lamb budget rather than the H⁻¹ budget paid by Leray energy.
反向热伴随改进 source pairing，但没有改变量纲 ||| The backward-heat adjoint improves source pairing but does not change the dimensions
令 \(g(t)=\langle F(t),e\rangle\)。纯 annular eigenmode 对这个未归一化方向源的精确模型是 ||| Let \(g(t)=\langle F(t),e\rangle\). The exact pure annular-eigenmode model for this unnormalized directional source is
对应的 exact endpoint packet 为 ||| The corresponding exact endpoint packet is
相对 strong \(g\in L_t^2\)，其算子范数平方是 \((1-e^{-2\nu\theta})/(2\nu)\)；在 frozen-denominator 模型 \(Y\equiv1\) 中，相对 Leray-order input \(\kappa^{-1}g\)，精确变成 ||| Relative to strong \(g\in L_t^2\), its squared operator norm is \((1-e^{-2\nu\theta})/(2\nu)\); in the frozen-denominator model \(Y\equiv1\), relative to the Leray-order input \(\kappa^{-1}g\), it becomes exactly
这是一项 exact packet norm 与 frozen-denominator linear-model diagnostic，不是完整 normalized NSE identity。实际 \(f=g/\sqrt Y\) 会使 endpoint integrand 带上 \(\sqrt Y\)；若改为归一化 observable，则演化式增加 \(Y_t/(2Y)\)。Lions–Magenes pairing 不会自动控制这一项；局部 cutoff 还会留下 viscous commutator。 ||| This is an exact packet norm and a frozen-denominator linear-model diagnostic, not a complete normalized NSE identity. The actual \(f=g/\sqrt Y\) makes the endpoint integrand carry \(\sqrt Y\); if a normalized observable is used instead, the evolution equation acquires \(Y_t/(2Y)\). Lions–Magenes pairing does not automatically control this term; a local cutoff also leaves a viscous commutator.
正次数 bilinear 失去 amplitude invariance；零均值又看不见常值 entry ||| A positive-degree bilinear form loses amplitude invariance; zero mean cannot see a constant entry
任何在未归一化 observable \(C\) 中具有正齐次次数的 bilinear charge，在 \(C\mapsto\varepsilon C\) 下趋于零，而 \(a_\beta\) 只依赖 leading direction、保持不变。若改用 \(C/\|C\|\) 形成 degree-zero direction，straight-ray \(C(t)=r(t)e\) 上就退化为上一节的 directional packet，因此继承 κ² 对角税。 ||| Any bilinear charge with positive homogeneity in the unnormalized observable \(C\) tends to zero under \(C\mapsto\varepsilon C\), whereas \(a_\beta\) depends only on the leading direction and remains invariant. If \(C/\|C\|\) is used instead to form a degree-zero direction, the straight ray \(C(t)=r(t)e\) reduces to the directional packet from the preceding section and therefore inherits the κ² diagonal tax.
更一般地，对有界自伴时间核 \(K\)，常值输入只看见 \(k_0=\langle1,K1\rangle\)。若 \(k_0=0\)，常值 directional signal 完全不可见；若 \(k_0\ne0\)，相对 H⁻¹-normalized input 的单包常数至少为 κ²|k₀|。 ||| More generally, for a bounded self-adjoint time kernel \(K\), a constant input sees only \(k_0=\langle1,K1\rangle\). If \(k_0=0\), a constant directional signal is completely invisible; if \(k_0\ne0\), the single-packet constant relative to H⁻¹-normalized input is at least κ²|k₀|.
even touch \(C_\varepsilon(t)=\varepsilon(t-b)^2e\) 的左右 direction 相同，\(A_-=A_+>0\)，因此 signed face \(A_+-A_-=0\)。这只是一项 abstract method test，不是 NSE trajectory。它说明只依赖 signed jump、direction jump 或 mean-zero wavelet 的方案会漏掉原 positive-entry 目标。 ||| For the even touch \(C_\varepsilon(t)=\varepsilon(t-b)^2e\), the left and right directions agree and \(A_-=A_+>0\), so the signed face is \(A_+-A_-=0\). This is only an abstract method test, not an NSE trajectory. It shows that a scheme depending only on a signed jump, a direction jump, or a mean-zero wavelet misses the original positive-entry target.
真实 NSE 初始 face 排除裸时间积分的尺度统一终局 ||| A genuine NSE initial face rules out a scale-uniform endpoint based on the bare time integral
R0.71O 的光滑 divergence-free 初值 ||| The smooth divergence-free initial datum from R0.71O is
配合 \(m(1)=0,m(\sqrt2)=1\) 的 covariant radial multiplier，产生 \(t=0\) 的真实一侧 entry，且 κ⁻²A₊=1/4。对 \(u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t)\)，该原子仍为 \(1/4\)，而任意固定基准 \(T>0\) 上 ||| Together with a covariant radial multiplier satisfying \(m(1)=0,m(\sqrt2)=1\), it produces a genuine one-sided entry at \(t=0\), with κ⁻²A₊=1/4. For \(u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t)\), this atom remains \(1/4\), while for any fixed reference \(T>0\),
所以，任何包含 observation-boundary entry、使用 covariant windows、且常数独立 λ 的“原子和 ≤ 裸时间积分”不等式都矛盾。该结论不覆盖只计算 internal entries 的定理，也不排除 RHS 中加入 initial trace、外部时间尺度或一个真正带 +2 尺度的 dynamical charge。 ||| Therefore every inequality of the form “sum of atoms ≤ bare time integral” that includes an observation-boundary entry, uses covariant windows, and has a λ-independent constant is contradictory. This conclusion does not cover a theorem counting only internal entries and does not rule out a right-hand side containing an initial trace, an external time scale, or a genuine dynamical charge with scale +2.
frame、tent 与 heat-adjoint 文献只支付积分 packet，不支付自适应 entry 下界 ||| The frame, tent, and heat-adjoint literature pays integral packets, not adaptive entry lower bounds
证明临界 parabolic \(X,Y\) 空间中的 quadratic map 与 Duhamel map，但 \(Y\) 不是这里的 bare Leray class，也没有自适应 entry lower charge。 ||| proves the quadratic and Duhamel maps in critical parabolic \(X,Y\) spaces, but \(Y\) is not the bare Leray class used here and supplies no adaptive entry lower charge.
的 tent spaces 控制锥区积分、square functions 与 Carleson measures，不控制一般 L² 等价类的裸时间点值。 ||| 's tent spaces control conical integrals, square functions, and Carleson measures, not bare time-point values of a general L² equivalence class.
的离散系数是分布配对或先平滑后的样本；其 trace theorem 也显示零阶 L² 时间正则性不足以定义一般时间点迹。 ||| 's discrete coefficients are distributional pairings or samples taken after smoothing; its trace theorem also shows that zeroth-order L² time regularity is insufficient to define a general time trace.
给 endpoint pairing 的合法性，不给解依赖 packet family 的统一 Bessel 性。 ||| establishes the legitimacy of endpoint pairing, not uniform Bessel behavior for a solution-dependent packet family.
的 signed flux 正下界依赖 Taylor-scale 条件、长时间平均和 optimal covering，不是逐 entry packet。两轮限定一手检索没有找到同时完成自适应 entry、signed/bilinear lower charge、packet sum 与 bare Leray payment 的现成定理。这是 bounded negative finding，不是不存在性、原创性或优先权声明。 ||| 's positive lower bound for signed flux depends on a Taylor-scale condition, long-time averaging, and optimal covering; it is not a packet for each entry. Two bounded primary-source searches found no existing theorem that simultaneously supplies an adaptive entry, a signed/bilinear lower charge, a packet sum, and bare Leray payment. This is a bounded negative finding, not a claim of nonexistence, originality, or priority.
符号账本与独立浮点重建分别通过 ||| The symbolic ledger and independent floating-point reconstruction pass separately
exact producer 记录 packet normalization、对角 κ²、有限 box Gram 下界、backward-heat 常数、bilinear mean dichotomy、even-touch cancellation 与 genuine NSE scaling exponents。independent checker 不导入 producer，另行重建 Gram eigenvalues、热核积分、缩放比与图数据。两者都不进行 NSE time stepping。 ||| The exact producer records packet normalization, the κ² diagonal, the finite box-Gram lower bound, backward-heat constants, the bilinear mean dichotomy, even-touch cancellation, and genuine NSE scaling exponents. The independent checker does not import the producer and separately reconstructs the Gram eigenvalues, heat-kernel integrals, scaling ratios, and figure data. Neither performs NSE time stepping.
附图分开显示尺度税、事件聚簇、热伴随与 signed cancellation ||| The figure separately displays the scale tax, event clustering, heat adjoint, and signed cancellation
R0.71S directional packet 的 Bessel 尺度税、Gram 聚簇、热伴随与 even-touch signed cancellation ||| Bessel scale tax, Gram clustering, heat adjoint, and even-touch signed cancellation for the R0.71S directional packet
图 R0.71S。A：能看见常值 entry 的 critical packet 最优单包常数按 κ² 增长，strong-data 版本保持常数。B：同向聚簇 box packets 的 Gram 最大特征值随事件数增长。C：backward-heat packet 在 frozen-denominator 线性模型中相对 H⁻¹-order input 仍带 κ²，而相对 strong source 为常数；variable \(Y\) 的归一化项不在该面板内。D：even touch 的 positive entry 为一，signed jump 与 mean-zero response 为零。A–C 是精确 packet/线性模型；D 不是 NSE trajectory。 ||| Figure R0.71S. A: the optimal single-packet constant for a critical packet that sees a constant entry grows as κ², while the strong-data version remains constant. B: the largest Gram eigenvalue for same-direction clustered box packets grows with the event count. C: in the frozen-denominator linear model, the backward-heat packet still carries κ² relative to an H⁻¹-order input but remains constant relative to a strong source; the normalization terms from variable \(Y\) are outside this panel. D: an even touch has positive entry one, while the signed jump and mean-zero response are zero. A–C are exact packet/linear models; D is not an NSE trajectory.
价值在于关闭了比 R0.71R 更宽的一类逃逸方案 ||| The value is in closing a broader escape route than R0.71R
R0.71R 的两阶错配可能只是 endpoint-square 选择造成的；R0.71S 证明，只要 packet 必须在 parabolic window 内重构常值 directional entry，同样的两阶代价就由 Hilbert-space 对角本身出现。它与 source-square 估计无关；frozen-denominator 反向热核的 packet norm 也达到同一边界，variable \(Y\) 的归一化接口则单独保留。 ||| The two-order mismatch in R0.71R could have been caused only by the endpoint-square choice. R0.71S proves that whenever a packet must reconstruct a constant directional entry inside a parabolic window, the same two-order cost arises from the Hilbert-space diagonal itself. It is independent of the source-square estimate; the packet norm of the frozen-denominator backward-heat kernel reaches the same boundary, while the normalization interface for variable \(Y\) is retained separately.
真实 NSE 初始面缩放把这个方法结论从 abstract forced path 提升为针对 observation-boundary 版本的 genuine NSE no-go。研究主线因此不再重复尝试“原目标 + bare H⁻¹ time integral”的 temporal packet，而转向适用范围更窄但尚未被排除的 internal-entry dynamics。 ||| Genuine NSE initial-face scaling upgrades this method conclusion from an abstract forced path to a genuine NSE no-go for the observation-boundary version. The research route therefore stops repeating temporal-packet attempts based on the original target + bare H⁻¹ time integral and turns to the narrower, still-unexcluded internal-entry dynamics.
R0.71T 只检查 internal entries 是否携带额外的尺度零动力学 charge ||| R0.71T tests only whether internal entries carry an additional scale-zero dynamical charge
下一步先移除 observation-boundary faces，只研究紧经典区间内部的 entry。候选 RHS 必须在 NSE 协变缩放下与 entry 原子同阶，不能只是裸 \(dt\) 积分，也不能把 κ² 隐藏进 Bessel 常数。 ||| The next step first removes observation-boundary faces and studies only entries inside a compact classical interval. A candidate right-hand side must have the same scale as the entry atom under NSE covariant scaling, cannot be only a bare \(dt\) integral, and cannot hide κ² inside the Bessel constant.
首先检查 localized Lamb–vorticity coupling 是否在 internal zero 附近强制一个 signed commutator、time-frequency flux 或两尺度补偿项；若仍只得到 strong L²-Lamb、point trace 或事件计数假设，我会把分支停在条件定理。 ||| I will first test whether localized Lamb–vorticity coupling forces a signed commutator, time-frequency flux, or two-scale compensation term near an internal zero. If it still yields only a strong L²-Lamb term, a point trace, or an event-counting hypothesis, I will stop the branch at the conditional theorem.
finite directional-packet implication；sharp single-packet κ² Bessel lower bound；finite Gram optimum and clustering lower bound；frozen-denominator backward-heat exact norm；限定 quadratic-kernel dichotomy；observation-boundary NSE scaling no-go。 ||| finite directional-packet implication; sharp single-packet κ² Bessel lower bound; finite Gram optimum and clustering lower bound; exact frozen-denominator backward-heat norm; the specified quadratic-kernel dichotomy; and the observation-boundary NSE scaling no-go.
uniform internal-entry packing、NSE multi-entry counterexample、scale-zero internal dynamical charge、infinite-frame limit、continuation criterion、finite-time singularity 或 global regularity。 ||| uniform internal-entry packing; an NSE multi-entry counterexample; a scale-zero internal dynamical charge; the infinite-frame limit; a continuation criterion; a finite-time singularity; or global regularity.
no-go 只针对原 positive-entry target 由 bare \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\) 以尺度统一常数支付，并在 genuine NSE 部分包含 initial observation face。 ||| The no-go concerns only scale-uniform payment of the original positive-entry target by the bare \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\), and its genuine NSE part includes an initial observation face.
even-touch 与线性 packet families 是 method tests；只有 Section 06 使用真实 smooth NSE initial trace 与精确协变缩放。 ||| The even-touch and linear packet families are method tests; only Section 06 uses a genuine smooth NSE initial trace and exact covariant scaling.
报告、文献、证书、图数据和独立 checker 全部保留 ||| The report, literature audit, certificates, figure data, and independent checker are all retained
R0.71S · 2026-08-26 · 个人数学研究日志 ||| R0.71S · 2026-08-26 · Personal mathematics research log
`;

const rows = translationRows
  .trim()
  .split("\n")
  .filter(Boolean);
const additions = new Map(
  rows.map((row) => {
    const separator = " ||| ";
    const offset = row.indexOf(separator);
    if (offset < 1) throw new Error("invalid translation row: " + row);
    return [row.slice(0, offset), row.slice(offset + separator.length)];
  }),
);
if (additions.size !== rows.length) {
  throw new Error("duplicate Chinese keys in R0.71S translation rows");
}

function numericTokens(value) {
  return [...String(value).matchAll(/\d+(?:[.\-–—]\d+)*/g)].map(
    (match) => match[0],
  );
}

function same(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

for (const relative of [
  "research-review.html",
  "literature-review.html",
  "recap-r0-61-r0-71s.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.04')) {
    throw new Error(relative + ": expected i18n cache version v1.04");
  }
}
try {
  const note = await readFile(resolve(publicDirectory, noteRelative), "utf8");
  if (!note.includes('/i18n-en.js?v=1.04')) {
    throw new Error(noteRelative + ": expected i18n cache version v1.04");
  }
} catch (error) {
  if (error?.code !== "ENOENT") throw error;
}

const currentWithoutBatch = current.filter((entry) => !/^r071s\d+$/.test(entry.id));
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error("duplicate Chinese keys outside the R0.71S batch");
}

const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));
if (sourceByChinese.size !== source.length) {
  throw new Error("duplicate Chinese keys in collected site strings");
}
const missing = source.filter((entry) => !currentByChinese.has(entry.zh));
const missingKeys = new Set(missing.map((entry) => entry.zh));
const uncovered = missing.filter((entry) => !additions.has(entry.zh));
const stale = [...additions.keys()].filter((zh) => !missingKeys.has(zh));
if (uncovered.length || stale.length || additions.size !== missing.length) {
  throw new Error(
    `translation batch does not equal active missing set (${missing.length}):\n` +
      "uncovered:\n" +
      uncovered.map((entry) => entry.zh).join("\n---\n") +
      "\nstale:\n" +
      stale.join("\n---\n"),
  );
}

const translated = missing.map((entry, index) => {
  const en = additions.get(entry.zh);
  if (!same(extractProtectedTokens(entry.zh), extractProtectedTokens(en))) {
    throw new Error("protected-token mismatch: " + entry.zh);
  }
  if (!same(numericTokens(entry.zh), numericTokens(en))) {
    throw new Error(
      "numeric-token mismatch: " +
        entry.zh +
        "\nZH " +
        JSON.stringify(numericTokens(entry.zh)) +
        "\nEN " +
        JSON.stringify(numericTokens(en)),
    );
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error("blank or Chinese-containing translation: " + entry.zh);
  }
  if (/\b(?:we|our|ours|us)\b/i.test(en)) {
    throw new Error("first-person plural voice: " + entry.zh);
  }
  return {
    ...entry,
    id: "r071s" + String(index + 1).padStart(3, "0"),
    en,
  };
});

const merged = [...currentWithoutBatch, ...translated];
if (new Set(merged.map((entry) => entry.zh)).size !== merged.length) {
  throw new Error("translation merge produced duplicate Chinese keys");
}
if (new Set(merged.map((entry) => entry.id)).size !== merged.length) {
  throw new Error("translation merge produced duplicate IDs");
}
await writeFile(translationPath, JSON.stringify(merged, null, 2) + "\n");
console.log(
  JSON.stringify(
    {
      source: source.length,
      existingWithoutBatch: currentWithoutBatch.length,
      activeMissingBefore: missing.length,
      added: translated.length,
      firstId: translated.at(0)?.id,
      lastId: translated.at(-1)?.id,
      total: merged.length,
      protectedTokenMismatches: 0,
      numericTokenMismatches: 0,
      englishWithChinese: 0,
      firstPersonPlural: 0,
    },
    null,
    2,
  ),
);
