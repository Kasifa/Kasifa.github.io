import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const defaultRoot = resolve(import.meta.dirname, "..");
const root = resolve(process.env.R072O_RELEASE_ROOT ?? defaultRoot);
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const snapshotPath = resolve(
  root,
  "scripts/i18n-snapshots/r072o-missing.json",
);
const checkOnly = process.argv.includes("--check-only");

const englishByChinese = new Map([
  ["研究笔记 R0.72O：一载波次线性 cubic 的物理回填、加倍的 strong window 与条件性的多载波接口。", "Research note R0.72O: physical reinsertion of the sublinear one-carrier cubic, the doubled strong window, and the conditional multi-carrier interface."],
  ["R0.72O｜物理回填与多载波传播门槛", "R0.72O｜Physical reinsertion and the multi-carrier propagation gate"],
  ["物理 numerator ε^(11/6)、一载波 growing-geometry window 与 full-superposition enhanced-dissipation gate。", "The physical numerator ε^(11/6), the one-carrier growing-geometry window, and the full-superposition enhanced-dissipation gate."],
  ["研究笔记 R0.72O · PHYSICAL REINSERTION · SUPERPOSITION INTERFACE", "Research note R0.72O · PHYSICAL REINSERTION · SUPERPOSITION INTERFACE"],
  ["次线性 cubic 已回填物理账本；", "The sublinear cubic has been reinserted into the physical ledger;"],
  ["一载波窗口加倍，多载波仍有独立门槛", "the one-carrier window doubles, while multiple carriers retain an independent gate"],
  ["R0.72N 的一载波 enhanced-dissipation cubic 在 exact-root correction 后仍满足 \\(\\mathcal C_\\times\\lesssim a^2\\varepsilon^{1/2}\\)。把它严格放回 R0.72L 的物理归一化后，正确 numerator 是 \\(\\varepsilon^{11/6}\\)，强耦合窗口推进到 \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\)。多载波公式只有在 full-superposition integrated enhanced dissipation 下成立；common-band support 与逐载波估计都不能替代这个假设。", "The one-carrier enhanced-dissipation cubic from R0.72N still satisfies \\(\\mathcal C_\\times\\lesssim a^2\\varepsilon^{1/2}\\) after the exact-root correction. Reinserting it rigorously into the physical normalization from R0.72L gives the correct numerator \\(\\varepsilon^{11/6}\\) and advances the strong-coupling window to \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\). The multi-carrier formula holds only under full-superposition integrated enhanced dissipation; neither common-band support nor carrierwise estimates can replace that hypothesis."],
  ["R0.72N 的一载波 enhanced-dissipation cubic 在 exact-root correction 后仍满足 \\(\\mathcal C_\\times\\lesssim a^2\\varepsilon^{1/2}\\)。把它严格放回 R0.72L 的物理归一化后，正确 numerator 是 \\(\\varepsilon^{11/6}\\)，强耦合窗口推进到 \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\)。多载波公式只有在带统一常数的 full-superposition integrated enhanced dissipation 下成立；common-band support 与逐载波估计都不能替代这个假设。", "The one-carrier enhanced-dissipation cubic from R0.72N still satisfies \\(\\mathcal C_\\times\\lesssim a^2\\varepsilon^{1/2}\\) after the exact-root correction. Reinserting it rigorously into the physical normalization from R0.72L gives the correct numerator \\(\\varepsilon^{11/6}\\) and advances the strong-coupling window to \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\). The multi-carrier formula holds only under full-superposition integrated enhanced dissipation with constants uniform across the comparison family; neither common-band support nor carrierwise estimates can replace that hypothesis."],
  ["状态 · R0.72O 定理与条件接口完成", "Status · R0.72O theorem and conditional interface complete"],
  ["版本 v0.72O · 2026-08-27", "Version v0.72O · 2026-08-27"],
  ["一般三维正则性：OPEN", "General three-dimensional regularity: OPEN"],
  ["一载波物理回填已经闭合，多载波结论仍严格带条件", "The one-carrier physical reinsertion is closed; the multi-carrier conclusion remains explicitly conditional"],
  ["对 R0.72L–N 的 fixed-background、row-aligned、phase-aligned、exact-root-corrected 一载波族，\\(\\mathcal C_\\times\\lesssim a^2\\varepsilon^{1/2}\\)。", "For the fixed-background, row-aligned, phase-aligned, exact-root-corrected one-carrier family of R0.72L–N, \\(\\mathcal C_\\times\\lesssim a^2\\varepsilon^{1/2}\\)."],
  ["物理 lift 给 \\(U_{\\rm ED}^{(1)}=\\varepsilon^{11/6}\\)，并把 strong window 推进到 \\(\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}\\)。", "The physical lift gives \\(U_{\\rm ED}^{(1)}=\\varepsilon^{11/6}\\) and advances the strong window to \\(\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}\\)."],
  ["若完整叠加满足 integrated enhanced dissipation，则 \\(U_{\\rm ED}=\\varepsilon^{11/6}p^{4/3}\\)；当前 common-band 假设本身不推出该传播估计。", "If the full superposition satisfies integrated enhanced dissipation, then \\(U_{\\rm ED}=\\varepsilon^{11/6}p^{4/3}\\); the current common-band assumptions alone do not imply this propagation estimate."],
  ["若完整叠加满足 integrated enhanced dissipation，且常数对比较的参数与几何族一致，则 \\(U_{\\rm ED}=\\varepsilon^{11/6}p^{4/3}\\)；当前 common-band 假设本身不推出该传播估计。", "If the full superposition satisfies integrated enhanced dissipation and its constants are uniform across the compared parameter and geometry families, then \\(U_{\\rm ED}=\\varepsilon^{11/6}p^{4/3}\\); the current common-band assumptions alone do not imply this propagation estimate."],
  ["窗口上沿只给统一有界，little-o 子区间才衰减；固定 \\(R\\) 下任意强耦合仍未闭合。", "The upper edge of the window gives only a uniform bound; decay holds only in the little-o subwindow, and arbitrary strong coupling at fixed \\(R\\) remains open."],
  ["correction 前的 antisymmetric launch 上，raw cubic 与 R0.72N 耗散量完全相同", "On the antisymmetric launch before correction, the raw cubic is exactly the R0.72N dissipative quantity"],
  ["对 correction 前的 antisymmetric one-carrier launch，\\(h=P_0V_wF\\)、\\(b=P_0V_w^2F\\)。以 \\(y=R^2x\\) 重标度后，R0.72L 的完整 cubic row 精确变成", "For the antisymmetric one-carrier launch before correction, \\(h=P_0V_wF\\) and \\(b=P_0V_w^2F\\). After rescaling by \\(y=R^2x\\), the complete cubic row from R0.72L becomes exactly"],
  ["exact-root correction 加入 \\(\\widetilde G=G+\\zeta e_0\\)。Coble–He 半群估计对任意 \\(L^2\\) 初值成立，固定坐标泛函有统一范数，所以 correction 不破坏", "The exact-root correction adds \\(\\widetilde G=G+\\zeta e_0\\). The Coble–He semigroup estimate holds for arbitrary \\(L^2\\) initial data, and the fixed coordinate functional has a uniform norm, so the correction preserves"],
  ["平方根 raw exponent 经过物理 lift 后变成 \\(11/6\\)", "The square-root raw exponent becomes \\(11/6\\) after the physical lift"],
  ["一载波满足 \\(g=\\varepsilon R^2\\)、\\(\\Theta\\asymp g^2/(a^2R^2)\\) 与 \\(D^{1/3}\\asymp g^{2/3}R^{2/3}\\)。因此", "The one-carrier family satisfies \\(g=\\varepsilon R^2\\), \\(\\Theta\\asymp g^2/(a^2R^2)\\), and \\(D^{1/3}\\asymp g^{2/3}R^{2/3}\\). Therefore"],
  ["这里不能把 raw \\(\\varepsilon^{1/2}\\) 直接写进 normalized ledger；\\(11/6\\) 才是物理 numerator 的正确指数。", "The raw \\(\\varepsilon^{1/2}\\) cannot be entered directly into the normalized ledger; \\(11/6\\) is the correct exponent of the physical numerator."],
  ["新分支与原有两条 cubic 分支共同进入完整账本", "The new branch joins the two existing cubic branches in the complete ledger"],
  ["exact-root launch 仍给 action floor \\(x\\ge Z\\gtrsim\\varepsilon^2R^{2/3}(1+\\varepsilon)^{-2/3}L_{R,\\varepsilon}\\)。", "The exact-root launch still gives the action floor \\(x\\ge Z\\gtrsim\\varepsilon^2R^{2/3}(1+\\varepsilon)^{-2/3}L_{R,\\varepsilon}\\)."],
  ["一载波 paid window 同时加倍 \\(R\\) 幂和 logarithm 幂", "The one-carrier paid window doubles both the \\(R\\) power and the logarithmic power"],
  ["对 \\(\\varepsilon\\ge1\\)，完整比值满足", "For \\(\\varepsilon\\ge1\\), the complete ratio satisfies"],
  ["沿固定 polynomial coupling，\\(L_{R,\\varepsilon}\\asymp1+\\log R\\)。上沿只给 \\(O(1)\\)；little-o 版本才使比值趋零。", "Along a fixed polynomial coupling, \\(L_{R,\\varepsilon}\\asymp1+\\log R\\). The upper edge gives only \\(O(1)\\); the ratio tends to zero only in the little-o version."],
  ["次线性 raw cubic 仍没有支付固定几何上的任意强耦合", "The sublinear raw cubic still does not pay for arbitrary strong coupling at fixed geometry"],
  ["这个已证上包络不衰减。因此 R0.72O 扩大的是 growing-geometry strong window，不是 fixed-geometry closure。", "This proved upper envelope does not decay. R0.72O therefore enlarges the growing-geometry strong window; it does not close the fixed-geometry problem."],
  ["交叉项可以整体支付，但前提必须作用于完整叠加", "Cross terms can be paid collectively, but the hypothesis must act on the full superposition"],
  ["令 \\(p=\\sqrt N/B\\)。若完整多载波传播满足", "Let \\(p=\\sqrt N/B\\). If the full multi-carrier propagation satisfies"],
  ["这里 \\(C_{\\rm ED}\\) 与 \\(c_{\\rm ED}\\) 必须对所比较的 \\(N,p,R,\\varepsilon\\) 和声明的载波几何族一致；否则只得到逐点蕴含，不能得到统一尺度律。", "Here \\(C_{\\rm ED}\\) and \\(c_{\\rm ED}\\) must be uniform across the compared \\(N,p,R,\\varepsilon\\) values and the stated carrier-geometry family; otherwise the result is only a pointwise implication, not a uniform scaling law."],
  ["则不展开 carrierwise triples，直接由算子范数得到", "then the operator norm gives the following estimates directly, without expanding carrierwise triples"],
  ["这是明确的条件蕴含，不是当前 common-band class 的无条件定理。", "This is an explicit conditional implication, not an unconditional theorem for the current common-band class."],
  ["这是带统一常数假设的条件蕴含，不是当前 common-band class 的无条件定理。", "This is a conditional implication under a uniform-constant hypothesis, not an unconditional theorem for the current common-band class."],
  ["逐载波求和与 common-band support 都不足", "Neither carrierwise summation nor common-band support is sufficient"],
  ["R0.72J 的 triangle-rich coherent block 有 \\(3R(R+1)\\) 个有序 signed Schur triples，并达到 \\(\\mathcal C_{\\times,R}\\asymp a^2N^2\\)。因此把 \\(N\\) 个 one-carrier costs 相加会漏掉真实 cross cubics。", "The triangle-rich coherent block from R0.72J has \\(3R(R+1)\\) ordered signed Schur triples and attains \\(\\mathcal C_{\\times,R}\\asymp a^2N^2\\). Summing \\(N\\) one-carrier costs therefore misses genuine cross cubics."],
  ["形状门也不能由频带自动推出。两载波剪切", "The shape gate also does not follow automatically from band support. Consider the two-carrier shear"],
  ["在 \\(\\theta=0\\) 满足 \\(U_R'(0)=U_R''(0)=0\\)、\\(U_R'''(0)=R(2R+1)\\ne0\\)。组合剪切具有退化临界点，不能直接调用 Coble–He 的统一非退化定理。", "At \\(\\theta=0\\), it satisfies \\(U_R'(0)=U_R''(0)=0\\) and \\(U_R'''(0)=R(2R+1)\\ne0\\). The combined shear has a degenerate critical point, so the uniform nondegenerate theorem of Coble–He cannot be invoked directly."],
  ["published theorem 与项目新推论保持分开", "The published theorem and the new project deductions remain separate"],
  ["给非退化时变剪切的 modewise \\(e^{-c\\nu^{1/2}|k|^{1/2}t}\\) 衰减；它不陈述这里的 cubic、物理回填或多载波结论。", "gives modewise \\(e^{-c\\nu^{1/2}|k|^{1/2}t}\\) decay for nondegenerate time-dependent shears; it does not state the cubic, physical-reinsertion, or multi-carrier conclusions here."],
  ["给足够小 \\(\\nu\\) 下非退化时变剪切的 modewise \\(e^{-c\\nu^{1/2}|k|^{1/2}t}\\) 衰减；本站再用 \\(L^2\\) 收缩补齐剩余紧参数区间。原论文不陈述这里的 cubic、物理回填或多载波结论。", "gives, for sufficiently small \\(\\nu\\), modewise \\(e^{-c\\nu^{1/2}|k|^{1/2}t}\\) decay for nondegenerate time-dependent shears; this site then uses \\(L^2\\) contraction to cover the remaining compact parameter range. The source paper does not state the cubic, physical-reinsertion, or multi-carrier conclusions here."],
  ["证明静态剪切的 rate 随临界点退化阶改变，支持保留 shape parameter；Couette 与 Kolmogorov 的非线性稳定理论只提供 flow-specific 方法先例。限定检索没有找到基于 \\((R,N,B,p)\\) 的 black-box full-superposition theorem，也不构成新颖性或优先权证明。", "proves that the rate for a stationary shear changes with the degeneracy order of its critical points, supporting retention of a shape parameter. Nonlinear stability theories for Couette and Kolmogorov flows provide only flow-specific methodological precedents. The bounded search found no black-box full-superposition theorem parameterized by \\((R,N,B,p)\\), and it does not establish novelty or priority."],
  ["附图只展示已证明的指数账本与条件分界", "The figure displays only the proved exponent ledger and conditional boundary"],
  ["物理付款不再停在 raw exponent，多载波缺口也被精确定位", "The physical payment no longer stops at the raw exponent, and the multi-carrier gap is now located precisely"],
  ["R0.72O 把 R0.72N 的 continuum enhanced-dissipation corollary 完整送入 normalized physical ledger，得到此前没有的 \\(R^{4/3}(\\log R)^2\\) strong window。与此同时，剩余困难不再是简单 carrier counting，而是组合剪切的统一 shape control 或等价的 full-superposition flux estimate。", "R0.72O carries the continuum enhanced-dissipation corollary from R0.72N through the normalized physical ledger and obtains the new \\(R^{4/3}(\\log R)^2\\) strong window. The remaining difficulty is no longer simple carrier counting, but uniform shape control for the combined shear or an equivalent full-superposition flux estimate."],
  ["这仍是特殊 triangular 2.5D family 中的机制定理，不是一般三维 continuation criterion。", "This remains a mechanism theorem for a special triangular 2.5D family, not a continuation criterion for general three-dimensional flows."],
  ["R0.72P：先处理有统一 Morse margin 的有限 carrier pattern", "R0.72P: first treat a finite carrier pattern with a uniform Morse margin"],
  ["下一节直接证明 full-superposition integrated ED，或证明更弱但足够的 rowwise flux estimate。第一个诚实正类应固定有限 carrier pattern，并把临界点数、Morse margin 与 shape neighborhoods 写成显式参数。", "The next section will prove full-superposition integrated ED directly, or a weaker but sufficient rowwise flux estimate. The first rigorous positive class should fix a finite carrier pattern and expose the number of critical points, the Morse margin, and the shape neighborhoods as explicit parameters."],
  ["本节没有从 common-band assumptions 推出 full-superposition ED，没有证明 logarithmic one-carrier cubic、fixed-geometry arbitrary coupling、multiscale physical absorption、任意三维继续性、有限时奇性或全局光滑性。Clay 千禧年问题仍未解决。", "This section does not derive full-superposition ED from common-band assumptions and proves no logarithmic one-carrier cubic bound, fixed-geometry arbitrary-coupling result, multiscale physical absorption, continuation result for arbitrary three-dimensional flows, finite-time singularity, or global smoothness. The Clay Millennium Problem remains unsolved."],
  ["报告、审计、证书与正式附图包", "Report, audits, certificates, and formal figure package"],
  ["完整数学报告", "Complete mathematical report"],
  ["文献边界审计", "Literature-boundary audit"],
  ["主张—证据矩阵", "Claim–evidence matrix"],
  ["独立数学审计", "Independent mathematical audit"],
  ["精确双路证书", "Exact two-route certificates"],
  ["正式附图包", "Formal figure package"],
  ["同步研究笔记 PDF", "Synchronized research-note PDF"],
  ["累计回顾", "Cumulative recap"],
  ["累计回顾 PDF", "Cumulative recap PDF"],
  ["下一检查点", "Next checkpoint"],
  ["先固定有限 carrier pattern 与统一 Morse margin，证明完整叠加的 integrated enhanced dissipation 或 rowwise cubic flux estimate。", "First fix a finite carrier pattern and a uniform Morse margin, then prove integrated enhanced dissipation for the full superposition or a rowwise cubic flux estimate."],
  ["累计回顾 R0.61–R0.72O · 2026-08-27", "Cumulative recap R0.61–R0.72O · 2026-08-27"],
  ["R0.60 recap 之后的累计回顾收录 105 个节点；全站现有 165 篇公开研究笔记", "The cumulative recap after R0.60 contains 105 nodes; the site now has 165 public research notes"],
  ["累计回顾保持二十八个问题阶段，并给出 R0.61–R0.72O 的完整逐节点索引。R0.72O 把一载波 true cubic 严格回填物理账本，将 strong window 推进到 \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\)；多载波只在 full-superposition ED 假设下得到条件窗口。", "The cumulative recap retains twenty-eight problem phases and gives a complete node-by-node index for R0.61–R0.72O. R0.72O rigorously reinserts the one-carrier true cubic into the physical ledger and advances the strong window to \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\); the multi-carrier window is obtained only conditionally under full-superposition ED."],
  ["累计回顾保持二十八个问题阶段，并给出 R0.61–R0.72O 的完整逐节点索引。R0.72O 把一载波 true cubic 严格回填物理账本，将 strong window 推进到 \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\)；多载波只在带统一常数的 full-superposition ED 假设下得到条件窗口。", "The cumulative recap retains twenty-eight problem phases and gives a complete node-by-node index for R0.61–R0.72O. R0.72O rigorously reinserts the one-carrier true cubic into the physical ledger and advances the strong window to \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\); the multi-carrier window is obtained only conditionally under full-superposition ED with uniform constants."],
  ["阶段判断：", "Phase assessment:"],
  ["一载波 growing-geometry payment 已闭合；fixed geometry 与 multi-carrier propagation 仍开放。", "The one-carrier growing-geometry payment is closed; fixed geometry and multi-carrier propagation remain open."],
  ["阅读 R0.60 之后的完整累计回顾 →", "Read the complete cumulative recap after R0.60 →"],
  ["研究笔记 R0.72O · 2026-08-27", "Research note R0.72O · 2026-08-27"],
  ["物理 numerator 是 \\(\\varepsilon^{11/6}\\)；多载波需要完整传播定理", "The physical numerator is \\(\\varepsilon^{11/6}\\); multiple carriers require a full propagation theorem"],
  ["一载波 exact-root correction 后仍有 \\(\\mathcal C_\\times\\lesssim a^2\\sqrt\\varepsilon\\)。物理回填给 \\(U_{\\rm ED}^{(1)}=\\varepsilon^{11/6}\\)，并将 paid window 推进到 \\(\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}\\)。", "After the one-carrier exact-root correction, \\(\\mathcal C_\\times\\lesssim a^2\\sqrt\\varepsilon\\) still holds. Physical reinsertion gives \\(U_{\\rm ED}^{(1)}=\\varepsilon^{11/6}\\) and advances the paid window to \\(\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}\\)."],
  ["若 full superposition 满足 integrated enhanced dissipation，则 \\(U_{\\rm ED}=\\varepsilon^{11/6}p^{4/3}\\)。common-band support 不能保证统一非退化临界点；逐载波求和还会遗漏真实 \\(N^2\\) cross cubics。", "If the full superposition satisfies integrated enhanced dissipation, then \\(U_{\\rm ED}=\\varepsilon^{11/6}p^{4/3}\\). Common-band support does not guarantee uniformly nondegenerate critical points, and carrierwise summation also misses genuine \\(N^2\\) cross cubics."],
  ["若 full superposition 满足 integrated enhanced dissipation，且常数对比较的参数与几何族一致，则 \\(U_{\\rm ED}=\\varepsilon^{11/6}p^{4/3}\\)。common-band support 不能保证统一非退化临界点；逐载波求和还会遗漏真实 \\(N^2\\) cross cubics。", "If the full superposition satisfies integrated enhanced dissipation and its constants are uniform across the compared parameter and geometry families, then \\(U_{\\rm ED}=\\varepsilon^{11/6}p^{4/3}\\). Common-band support does not guarantee uniformly nondegenerate critical points, and carrierwise summation also misses genuine \\(N^2\\) cross cubics."],
  ["结论边界：", "Claim boundary:"],
  ["conditional multi-carrier implication 不是无条件 superposition theorem；fixed-geometry arbitrary coupling 与一般三维正则性仍开放。", "The conditional multi-carrier implication is not an unconditional superposition theorem; fixed-geometry arbitrary coupling and general three-dimensional regularity remain open."],
  ["阅读 R0.72O 研究笔记 →", "Read the R0.72O research note →"],
  ["查看精确证书", "View the exact certificates"],
  ["查看完整数学报告", "View the complete mathematical report"],
  ["查看文献边界审计", "View the literature-boundary audit"],
  ["查看正式附图包", "View the formal figure package"],
  ["阅读累计回顾", "Read the cumulative recap"],
  ["下载累计回顾 PDF", "Download the cumulative-recap PDF"],
  ["下一步 R0.72P：", "Next R0.72P:"],
  ["在显式 uniform Morse margin 下证明 full-superposition gate。", "Prove the full-superposition gate under an explicit uniform Morse margin."],
  ["R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72O 的 105 个研究节点；最新一节完成一载波物理回填并隔离多载波传播门槛。", "Research recap after R0.60: complete coverage of 105 research nodes from R0.61 through R0.72O; the latest section completes the one-carrier physical reinsertion and isolates the multi-carrier propagation gate."],
  ["二十八个阶段、105 个节点：从约化递推到一载波 physical reinsertion 与 full-superposition gate。", "Twenty-eight phases and 105 nodes: from reduced recurrences to one-carrier physical reinsertion and the full-superposition gate."],
  ["R0.61–R0.72O｜R0.60 之后的研究回顾", "R0.61–R0.72O｜Research recap after R0.60"],
  ["R0.72L–R0.72O · strong-coupling screen、耗散决策与物理回填", "R0.72L–R0.72O · Strong-coupling screen, dissipative decision, and physical reinsertion"],
  ["R0.72L 保留 actual \\(K\\) 与 \\(x\\)，R0.72M 精确化 danger window，R0.72N 在完整耗散链上排除 action-poor route 并得到一载波 \\(O(a^2\\sqrt\\varepsilon)\\) cubic。", "R0.72L retains the actual \\(K\\) and \\(x\\), R0.72M makes the danger window exact, and R0.72N excludes the action-poor route on the complete dissipative chain and obtains the one-carrier \\(O(a^2\\sqrt\\varepsilon)\\) cubic."],
  ["R0.72O 将该 cubic 严格回填 normalized physical ledger，得到 \\(U_{\\rm ED}^{(1)}=\\varepsilon^{11/6}\\) 和 \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\) 的 growing-geometry window。多载波公式只在 full-superposition integrated ED 假设下成立；common-band support 不能自动保证统一 Morse margin。", "R0.72O rigorously reinserts this cubic into the normalized physical ledger, giving \\(U_{\\rm ED}^{(1)}=\\varepsilon^{11/6}\\) and the growing-geometry window \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\). The multi-carrier formula holds only under full-superposition integrated ED; common-band support does not automatically guarantee a uniform Morse margin."],
  ["R0.72O 将该 cubic 严格回填 normalized physical ledger，得到 \\(U_{\\rm ED}^{(1)}=\\varepsilon^{11/6}\\) 和 \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\) 的 growing-geometry window。多载波公式只在 full-superposition integrated ED 及其统一常数假设下成立；common-band support 不能自动保证统一 Morse margin。", "R0.72O rigorously reinserts this cubic into the normalized physical ledger, giving \\(U_{\\rm ED}^{(1)}=\\varepsilon^{11/6}\\) and the growing-geometry window \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\). The multi-carrier formula holds only under full-superposition integrated ED together with its uniform-constant hypothesis; common-band support does not automatically guarantee a uniform Morse margin."],
  ["R0.72O 的 physical-reinsertion theorem：exact-root correction 后 \\(\\mathcal C_\\times\\lesssim a^2\\sqrt\\varepsilon\\)；物理 numerator 为 \\(\\varepsilon^{11/6}\\)，一载波 paid window 为 \\(\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}\\)。多载波只有在 full-superposition integrated ED 下得到条件推广；逐载波求和与 common-band support 都不足。", "R0.72O physical-reinsertion theorem: after the exact-root correction, \\(\\mathcal C_\\times\\lesssim a^2\\sqrt\\varepsilon\\); the physical numerator is \\(\\varepsilon^{11/6}\\), and the one-carrier paid window is \\(\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}\\). The multi-carrier extension is conditional on full-superposition integrated ED; carrierwise summation and common-band support are both insufficient."],
  ["R0.72O 的 physical-reinsertion theorem：exact-root correction 后 \\(\\mathcal C_\\times\\lesssim a^2\\sqrt\\varepsilon\\)；物理 numerator 为 \\(\\varepsilon^{11/6}\\)，一载波 paid window 为 \\(\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}\\)。多载波只有在带统一常数的 full-superposition integrated ED 下得到条件推广；逐载波求和与 common-band support 都不足。", "R0.72O physical-reinsertion theorem: after the exact-root correction, \\(\\mathcal C_\\times\\lesssim a^2\\sqrt\\varepsilon\\); the physical numerator is \\(\\varepsilon^{11/6}\\), and the one-carrier paid window is \\(\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}\\). The multi-carrier extension is conditional on full-superposition integrated ED with uniform constants; carrierwise summation and common-band support are both insufficient."],
  ["一载波物理回填完成，多载波缺口已经变成明确传播命题", "One-carrier physical reinsertion is complete, and the multi-carrier gap is now an explicit propagation problem"],
  ["截至 R0.72O，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 105 个节点或 67 个公开版本解释成对千禧年问题完成了某个比例。", "As of R0.72O, there is no new unconditional continuation criterion, no reduction of the set of all possible singular solutions, and no proof of finite-time breakdown. The 105 nodes or 67 public releases cannot be interpreted as a completion percentage for the Millennium Problem."],
  ["新的严格结果是 \\(\\varepsilon^{11/6}\\) physical numerator、加倍的 growing-geometry strong window，以及 full-superposition ED 对多载波 cubic 的条件蕴含。", "The new rigorous results are the \\(\\varepsilon^{11/6}\\) physical numerator, the doubled growing-geometry strong window, and the conditional implication from full-superposition ED to the multi-carrier cubic estimate."],
  ["新的严格结果是 \\(\\varepsilon^{11/6}\\) physical numerator、加倍的 growing-geometry strong window，以及带统一常数的 full-superposition ED 对多载波 cubic 的条件蕴含。", "The new rigorous results are the \\(\\varepsilon^{11/6}\\) physical numerator, the doubled growing-geometry strong window, and the conditional implication from full-superposition ED with uniform constants to the multi-carrier cubic estimate."],
  ["组合剪切可能出现退化临界点；因此下一步必须显式控制 Morse margin 或直接证明 rowwise flux，不能把 one-carrier theorem 逐模相加。", "A combined shear may have degenerate critical points. The next step must therefore control the Morse margin explicitly or prove a rowwise flux estimate directly; the one-carrier theorem cannot be summed mode by mode."],
  ["R0.72P 直接处理 full-superposition gate", "R0.72P addresses the full-superposition gate directly"],
  ["先固定有限 carrier pattern，给临界点数、Morse margin 与 shape neighborhoods 统一参数，证明 integrated enhanced dissipation。", "First fix a finite carrier pattern, impose uniform parameters for the number of critical points, the Morse margin, and the shape neighborhoods, and prove integrated enhanced dissipation."],
  ["若完整半群过强，则直接证明足够闭合物理账本的 rowwise cubic flux estimate。", "If the full semigroup statement is too strong, prove directly a rowwise cubic flux estimate sufficient to close the physical ledger."],
  ["公开、完整封存与问题解决继续分开计数", "Publication, complete archiving, and problem resolution remain separate counts"],
  ["R0.70A–R0.72O 的 67 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，43 节完整封存；24 节较早版本仍列入可审计的旧档回补清单。", "The 67 HTML/PDF releases and research sources from R0.70A–R0.72O are on the public route. Under the current formal-figure contract, 43 releases are fully archived; 24 earlier releases remain on the auditable legacy-backfill list."],
  ["R0.72O 的无条件部分只覆盖声明的一载波 exact-corrected triangular family。多载波公式明确依赖 full-superposition ED；限定检索没有找到可替代该 gate 的 black-box theorem，Clay 正式问题仍然开放。", "The unconditional part of R0.72O covers only the stated one-carrier exact-corrected triangular family. The multi-carrier formula explicitly depends on full-superposition ED; the bounded search found no black-box theorem that replaces this gate, and the official Clay problem remains open."],
  ["R0.72O 的无条件部分只覆盖声明的一载波 exact-corrected triangular family。多载波公式明确依赖常数对参数与几何族一致的 full-superposition ED；限定检索没有找到可替代该 gate 的 black-box theorem，Clay 正式问题仍然开放。", "The unconditional part of R0.72O covers only the stated one-carrier exact-corrected triangular family. The multi-carrier formula explicitly depends on full-superposition ED whose constants are uniform across the parameter and geometry families; the bounded search found no black-box theorem that replaces this gate, and the official Clay problem remains open."],
  ["逐节笔记、证书、正式附图和历史回顾", "Section notes, certificates, formal figures, and historical recaps"],
  ["打开最新节点 R0.72O", "Open the latest node R0.72O"],
  ["查看 R0.72O 精确证书", "View the R0.72O exact certificates"],
  ["完整节点索引保留 R0.69W、R0.70A 以后每个公开版本及其原始编号；状态标签只描述证据类型。", "The complete node index retains R0.69W and every public release from R0.70A onward under its original identifier; status labels describe only the evidence type."],
  ["R0.72O 已把一载波 enhanced-dissipation cubic 回填物理账本，并得到 \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\) 的 growing-geometry window；下一关是带显式 shape control 的 full-superposition propagation。", "R0.72O reinserts the one-carrier enhanced-dissipation cubic into the physical ledger and obtains the growing-geometry window \\(\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2\\); the next gate is full-superposition propagation with explicit shape control."],
  ["从 dissipative one-carrier decision 走到 physical reinsertion", "From the dissipative one-carrier decision to physical reinsertion"],
  ["R0.72N 回到耗散链，证明 action-poor route 对声明 launch 失效；再把 Coble–He 的时变剪切衰减转成本站的 \\(O(a^2\\sqrt\\sigma)\\) cubic corollary。R0.72O 将该结果回填 normalized physical ledger，得到 \\(\\varepsilon^{11/6}\\) numerator 与加倍的 growing-geometry window，并把多载波问题隔离为 full-superposition ED gate。", "R0.72N returns to the dissipative chain, proves that the action-poor route fails for the stated launch, and turns the Coble–He time-dependent-shear decay into the project-specific \\(O(a^2\\sqrt\\sigma)\\) cubic corollary. R0.72O reinserts that result into the normalized physical ledger, obtains the \\(\\varepsilon^{11/6}\\) numerator and the doubled growing-geometry window, and isolates the multi-carrier problem as the full-superposition ED gate."],
  ["R0.72O 已完成：", "R0.72O complete:"],
  ["一载波 physical reinsertion 与 growing-geometry strong window 已闭合；full-superposition propagation 保持开放。", "One-carrier physical reinsertion and the growing-geometry strong window are closed; full-superposition propagation remains open."],
  ["R0.72N 在完整耗散链上排除声明 launch 的 action-poor route，并由 Coble–He 时变剪切衰减推出本站 corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\)。R0.72O 将该 cubic 回填物理账本，得到 \\(\\varepsilon^{11/6}\\) numerator 与 \\(R^{4/3}L_{R,\\varepsilon}^2\\) window；多载波只在 full-superposition ED 假设下条件成立。一般 Navier–Stokes 正则性仍开放。", "R0.72N excludes the action-poor route for the stated launch on the complete dissipative chain and derives the project-specific corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\) from the Coble–He time-dependent-shear decay. R0.72O reinserts this cubic into the physical ledger, obtaining the \\(\\varepsilon^{11/6}\\) numerator and the \\(R^{4/3}L_{R,\\varepsilon}^2\\) window; the multi-carrier statement holds only conditionally under full-superposition ED. General Navier–Stokes regularity remains open."],
  ["R0.72N 在完整耗散链上排除声明 launch 的 action-poor route，并由 Coble–He 时变剪切衰减推出本站 corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\)。R0.72O 将该 cubic 回填物理账本，得到 \\(\\varepsilon^{11/6}\\) numerator 与 \\(R^{4/3}L_{R,\\varepsilon}^2\\) window；多载波只在带统一常数的 full-superposition ED 假设下条件成立。一般 Navier–Stokes 正则性仍开放。", "R0.72N excludes the action-poor route for the stated launch on the complete dissipative chain and derives the project-specific corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\) from the Coble–He time-dependent-shear decay. R0.72O reinserts this cubic into the physical ledger, obtaining the \\(\\varepsilon^{11/6}\\) numerator and the \\(R^{4/3}L_{R,\\varepsilon}^2\\) window; the multi-carrier statement holds only conditionally under full-superposition ED with uniform constants. General Navier–Stokes regularity remains open."],
  ["一载波 physical numerator 为 \\(\\varepsilon^{11/6}\\)，growing-geometry window 推进到 \\(\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}\\)；多载波公式依赖 full-superposition ED。", "The one-carrier physical numerator is \\(\\varepsilon^{11/6}\\), and the growing-geometry window advances to \\(\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}\\); the multi-carrier formula depends on full-superposition ED."],
  ["一载波 physical numerator 为 \\(\\varepsilon^{11/6}\\)，growing-geometry window 推进到 \\(\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}\\)；多载波公式依赖常数对比较族一致的 full-superposition ED。", "The one-carrier physical numerator is \\(\\varepsilon^{11/6}\\), and the growing-geometry window advances to \\(\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}\\); the multi-carrier formula depends on full-superposition ED with constants uniform across the comparison family."],
  ["当前累计回顾", "Current cumulative recap"],
  ["方法边界", "Method boundary"],
  ["开放接口 · R0.72P", "Open interface · R0.72P"],
  ["在固定有限 carrier pattern 与 uniform Morse margin 下证明 integrated ED，或直接证明 rowwise cubic flux estimate。", "Prove integrated ED under a fixed finite carrier pattern and a uniform Morse margin, or prove a rowwise cubic flux estimate directly."],
  ["R0.72O 的物理回填与多载波文献边界", "R0.72O literature boundary for physical reinsertion and multiple carriers"],
  ["的常数在统一非退化 shape parameters 下不依赖 \\(\\nu\\) 与 horizontal mode。本站一载波 profile 直接核对这些参数，再把 semigroup decay 转成 corrected cubic 和 physical ledger；后两步不是原论文定理。", "has constants independent of \\(\\nu\\) and the horizontal mode under uniform nondegenerate shape parameters. The one-carrier profile on this site verifies those parameters directly, then converts semigroup decay into the corrected cubic and physical ledger; the latter two steps are not theorems from the source paper."],
  ["说明 stationary-shear exponent 随临界点退化阶改变。Couette 与 Kolmogorov 的 nonlinear thresholds 是 flow-specific 方法先例，不是当前 common-band class 的 black-box theorem。", "shows that the stationary-shear exponent changes with the degeneracy order of the critical points. Nonlinear thresholds for Couette and Kolmogorov flows are flow-specific methodological precedents, not a black-box theorem for the current common-band class."],
  ["R0.72O 的主张边界", "Claim boundary for R0.72O"],
  ["线性 horizontal solution modes 可在同一 \\(x\\)-independent shear 下用 Parseval 叠加；这里的多个 carriers 进入 shear coefficient 与 cubic cross terms，不能逐载波 tensorize。common-band support 不能保证组合 shear 的 uniform Morse margin。多载波窗口明确依赖 full-superposition ED；限定检索不构成新颖性或优先权证明。", "Linear horizontal solution modes can be superposed by Parseval under the same \\(x\\)-independent shear. Here, multiple carriers enter the shear coefficient and the cubic cross terms, so they cannot be tensorized carrier by carrier. Common-band support does not guarantee a uniform Morse margin for the combined shear. The multi-carrier window explicitly depends on full-superposition ED; the bounded search does not establish novelty or priority."],
  ["线性 horizontal solution modes 可在同一 \\(x\\)-independent shear 下用 Parseval 叠加；这里的多个 carriers 进入 shear coefficient 与 cubic cross terms，不能逐载波 tensorize。common-band support 不能保证组合 shear 的 uniform Morse margin。多载波窗口明确依赖常数对参数与几何族一致的 full-superposition ED；限定检索不构成新颖性或优先权证明。", "Linear horizontal solution modes can be superposed by Parseval under the same \\(x\\)-independent shear. Here, multiple carriers enter the shear coefficient and the cubic cross terms, so they cannot be tensorized carrier by carrier. Common-band support does not guarantee a uniform Morse margin for the combined shear. The multi-carrier window explicitly depends on full-superposition ED whose constants are uniform across the parameter and geometry families; the bounded search does not establish novelty or priority."],
  ["01 · raw cubic 识别", "01 · Raw cubic identification"],
  ["02 · 物理回填", "02 · Physical reinsertion"],
  ["叠加", "Superposition"],
  ["固定几何", "Fixed geometry"],
  ["回填", "Reinsertion"],
  ["交叉项", "Cross terms"],
  ["识别", "Identification"],
  ["保留 R0.72N 历史回顾", "Retain the R0.72N historical recap"],
  ["上次综述 v1.27 · 2026-08-27", "Previous review v1.27 · 2026-08-27"],
]);

const expectedFiles = [
  "literature-review.html",
  "notes/r0-72o.html",
  "recap-r0-61-r0-72o.html",
  "research-review.html",
];

for (const relative of expectedFiles) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.28')) {
    throw new Error(relative + ": expected i18n cache version v1.28");
  }
}

const source = await collectSiteStrings(publicDirectory);
const translations = JSON.parse(await readFile(translationPath, "utf8"));
const batchId = /^r072o\d+$/;
const retained = translations.filter((entry) => !batchId.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.72O batch");
}

const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(missingFiles) !== JSON.stringify(expectedFiles)) {
  throw new Error(
    "Unexpected R0.72O source files: " + JSON.stringify(missingFiles),
  );
}

const simpleTransforms = [
  ["R0.72O", "R0.72N"],
  ["R0.72P", "R0.72O"],
  ["v1.28", "v1.27"],
  ["105", "104"],
  ["165", "164"],
  ["67", "66"],
  ["43", "42"],
  ["75", "74"],
];

function deriveFromRetained(zh) {
  const queue = [{ value: zh, applied: [] }];
  const seen = new Set([zh]);
  while (queue.length > 0) {
    const current = queue.shift();
    const retainedEntry = retainedByChinese.get(current.value);
    if (retainedEntry) {
      let en = retainedEntry.en;
      for (const pair of current.applied.slice().reverse()) {
        en = en.replaceAll(pair[1], pair[0]);
      }
      return en;
    }
    if (current.applied.length >= 5) continue;
    for (const pair of simpleTransforms) {
      const newValue = pair[0];
      const oldValue = pair[1];
      if (!current.value.includes(newValue)) continue;
      const candidate = current.value.replaceAll(newValue, oldValue);
      if (seen.has(candidate)) continue;
      seen.add(candidate);
      queue.push({
        value: candidate,
        applied: [...current.applied, pair],
      });
    }
  }
  return null;
}

function deriveComposite(zh) {
  const oldLiteratureTail =
    "R0.72N 在完整耗散链上排除声明 launch 的 action-poor route，并由 Coble–He 时变剪切衰减推出本站 corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\)；logarithmic rate 与多载波仍开放。一般 Navier–Stokes 正则性仍开放。";
  const newLiteratureTail =
    "R0.72N 在完整耗散链上排除声明 launch 的 action-poor route，并由 Coble–He 时变剪切衰减推出本站 corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\)。R0.72O 将该 cubic 回填物理账本，得到 \\(\\varepsilon^{11/6}\\) numerator 与 \\(R^{4/3}L_{R,\\varepsilon}^2\\) window；多载波只在带统一常数的 full-superposition ED 假设下条件成立。一般 Navier–Stokes 正则性仍开放。";
  const oldLiteratureEnglishTail =
    "R0.72N excludes the action-poor route for the stated launch on the complete dissipative chain and derives the project-specific corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\) from the Coble–He time-dependent-shear decay; the logarithmic rate and multiple carriers remain open. General Navier–Stokes regularity remains open.";
  const newLiteratureEnglishTail =
    "R0.72N excludes the action-poor route for the stated launch on the complete dissipative chain and derives the project-specific corollary \\(\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma\\) from the Coble–He time-dependent-shear decay. R0.72O reinserts this cubic into the physical ledger, obtaining the \\(\\varepsilon^{11/6}\\) numerator and the \\(R^{4/3}L_{R,\\varepsilon}^2\\) window; the multi-carrier statement holds only conditionally under full-superposition ED with uniform constants. General Navier–Stokes regularity remains open.";
  if (zh.endsWith(newLiteratureTail)) {
    const oldZh =
      zh.slice(0, -newLiteratureTail.length) + oldLiteratureTail;
    const retainedEntry = retainedByChinese.get(oldZh);
    if (
      retainedEntry?.en.endsWith(oldLiteratureEnglishTail)
    ) {
      return (
        retainedEntry.en.slice(0, -oldLiteratureEnglishTail.length) +
        newLiteratureEnglishTail
      );
    }
  }

  const homeAddition =
    "R0.72O 将该结果回填 normalized physical ledger，得到 \\(\\varepsilon^{11/6}\\) numerator 与加倍的 growing-geometry window，并把多载波问题隔离为 full-superposition ED gate。";
  const homeEnglishAddition =
    " R0.72O reinserts that result into the normalized physical ledger, obtains the \\(\\varepsilon^{11/6}\\) numerator and the doubled growing-geometry window, and isolates the multi-carrier problem as the full-superposition ED gate.";
  if (zh.endsWith(homeAddition)) {
    const oldZh = zh.slice(0, -homeAddition.length);
    const retainedEntry = retainedByChinese.get(oldZh);
    if (retainedEntry) return retainedEntry.en + homeEnglishAddition;
  }

  const oldRouteSuffix =
    "physical reinsertion and multi-carrier gate";
  const newRouteSuffix =
    "physical reinsertion → full-superposition ED gate";
  if (zh.endsWith(newRouteSuffix)) {
    const oldZh = zh.slice(0, -newRouteSuffix.length) + oldRouteSuffix;
    const retainedEntry = retainedByChinese.get(oldZh);
    if (retainedEntry?.en.endsWith(oldRouteSuffix)) {
      return (
        retainedEntry.en.slice(0, -oldRouteSuffix.length) + newRouteSuffix
      );
    }
  }
  return null;
}

const unresolved = [];
const translatedEntries = missing.map((entry, index) => {
  const en =
    englishByChinese.get(entry.zh) ??
    deriveComposite(entry.zh) ??
    deriveFromRetained(entry.zh);
  if (!en) {
    unresolved.push(entry.zh);
    return null;
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error("Blank or Chinese-containing English for: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("Collective English voice remains in: " + entry.zh);
  }
  if (entry.zh.includes("我") && !/\bI\b/.test(en)) {
    throw new Error("First-person singular English is missing for: " + entry.zh);
  }
  const zhTokens = extractProtectedTokens(entry.zh);
  const enTokens = extractProtectedTokens(en);
  if (JSON.stringify(zhTokens) !== JSON.stringify(enTokens)) {
    throw new Error(
      "Protected-token mismatch for:\n" +
        entry.zh +
        "\nZH " +
        JSON.stringify(zhTokens) +
        "\nEN " +
        JSON.stringify(enTokens),
    );
  }
  return {
    ...entry,
    id: "r072o" + String(index + 1).padStart(3, "0"),
    en,
  };
});

if (unresolved.length > 0) {
  throw new Error(
    "Missing explicit R0.72O English rows (" +
      unresolved.length +
      "):\n" +
      unresolved.join("\n---\n"),
  );
}

const finalTranslations = [...retained, ...translatedEntries];
for (const field of ["id", "zh"]) {
  const values = finalTranslations.map((entry) => entry[field]);
  if (new Set(values).size !== values.length) {
    throw new Error("Duplicate final translation " + field);
  }
}

const snapshot = missing.map(({ zh, count, files }) => ({ zh, count, files }));
if (checkOnly) {
  const currentSnapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
  if (JSON.stringify(currentSnapshot) !== JSON.stringify(snapshot)) {
    throw new Error("R0.72O missing-string snapshot is stale");
  }
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.72O translations/en.json batch is stale");
  }
} else {
  await writeFile(snapshotPath, JSON.stringify(snapshot, null, 2) + "\n");
  await writeFile(
    translationPath,
    JSON.stringify(finalTranslations, null, 2) + "\n",
  );
}

console.log(
  JSON.stringify({
    checkOnly,
    added: translatedEntries.length,
    fallback: 0,
    total: finalTranslations.length,
    liveStrings: source.length,
    missingBefore: missing.length,
    missingAfter: 0,
    files: missingFiles,
  }),
);
