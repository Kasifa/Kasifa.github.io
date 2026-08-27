import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const defaultRoot = resolve(import.meta.dirname, "..");
const root = resolve(process.env.R072P_RELEASE_ROOT ?? defaultRoot);
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r072p-missing.json");
const checkOnly = process.argv.includes("--check-only");

const englishByChinese = new Map();
const row = (zh, en) => englishByChinese.set(zh, en);

row("研究笔记 R0.72P：固定实系数同一直线相位（同相或反相） 1:2 两载波的 full-superposition enhanced dissipation 与精确 Morse 适用边界。", "Research note R0.72P: full-superposition enhanced dissipation for the fixed real-collinear-phase (in-phase or antiphase) 1:2 two-carrier class and its exact Morse applicability boundary.");
row("R0.72P｜两载波完整传播门与 Morse 墙", "R0.72P｜The full two-carrier propagation gate and Morse wall");
row("固定 1:2 正类的统一 full-superposition ED、cross cubic 与 λ=±1/4 Morse applicability wall。", "Uniform full-superposition ED and the cross cubic for the fixed 1:2 positive class, with the λ=±1/4 Morse applicability wall.");
row("研究笔记 R0.72P · FULL-SUPERPOSITION ED · MORSE WALL", "Research note R0.72P · FULL-SUPERPOSITION ED · MORSE WALL");
row("完整两载波传播门已经闭合；", "The full two-carrier propagation gate is closed;");
row("结论止于固定实系数同一直线相位（同相或反相） 1:2 正类", "the conclusion stops at the fixed real-collinear-phase (in-phase or antiphase) 1:2 positive class");
row("状态 · R0.72P 固定两载波正类完成", "Status · the fixed R0.72P two-carrier positive class is complete");
row("版本 v0.72P · 2026-08-27", "Version v0.72P · 2026-08-27");
row("一个非平凡 full-superposition 正类已经从条件接口升级为定理", "A nontrivial full-superposition positive class has advanced from a conditional interface to a theorem");
row("两个载波必须作为一个完整算子缩到固定圆周", "The two carriers must be reduced to a fixed circle as one complete operator");
row("临界点固定为 \\(0,\\pi\\)，Morse margin 对整个系数锥一致", "The critical points are fixed at \\(0,\\pi\\), with a uniform Morse margin across the coefficient cone");
row("Coble–He 定理作用于完整 profile，统一常数来自固定 shape 数据", "The Coble–He theorem acts on the full profile, and uniform constants come from fixed shape data");
row("小扩散定理与 \\(L^2\\) 收缩共同覆盖全部 \\(\\varepsilon\\ge1\\)", "The small-diffusivity theorem and \\(L^2\\) contraction together cover every \\(\\varepsilon\\ge1\\)");
row("R0.72O 的条件门在这个 \\(N=2\\) 正类上变成无条件估计", "The conditional R0.72O gate becomes an unconditional estimate on this \\(N=2\\) positive class");
row("已证强耦合窗口保留精确 \\(p\\) 因子", "The proved strong-coupling window retains the exact \\(p\\) factor");
row("\\(\\lambda=\\pm1/4\\) 是适用性墙，不是动力学反例", "\\(\\lambda=\\pm1/4\\) is an applicability wall, not a dynamical counterexample");
row("固定正类与一般多载波问题严格分开", "The fixed positive class is kept strictly separate from the general multi-carrier problem");
row("一手来源提供半群框架，本站负责参数族统一化与物理回填", "Primary sources provide the semigroup framework; the parameter-family uniformization and physical reinsertion are project deductions");
row("正式附图同时标出正类、统一传播与适用性墙", "The formal figure displays the positive class, uniform propagation, and the applicability wall");
row("首次把 multi-carrier gate 在一个非平凡完整正类上严格关闭", "The multi-carrier gate is rigorously closed for a nontrivial full positive class for the first time in this project");
row("R0.72Q：测试相位扰动与更一般有限 pattern 的 uniform shape contract", "R0.72Q: test phase perturbations and a uniform shape contract for more general finite patterns");
row("开放接口 · R0.72Q", "Open interface · R0.72Q");
row("R0.72P 的完整两载波传播与 Morse 文献边界", "The literature boundary for the R0.72P full two-carrier propagation theorem and Morse wall");
row("R0.72P 的主张边界", "R0.72P claim boundary");
row("文献综述 v1.29 · 2026-08-27", "Literature review v1.29 · 2026-08-27");
row("累计回顾 R0.61–R0.72P · 2026-08-27", "Cumulative recap R0.61–R0.72P · 2026-08-27");
row("R0.60 recap 之后的累计回顾收录 106 个节点；全站现有 166 篇公开研究笔记", "The cumulative recap after R0.60 contains 106 nodes; the site now has 166 public research notes");
row("固定两载波正类已闭合；arbitrary phase/carriers、fixed geometry 与一般三维问题仍开放。", "The fixed two-carrier positive class is closed; arbitrary phases and carriers, fixed geometry, and the general three-dimensional problem remain open.");
row("固定实系数同一直线相位（同相或反相） 1:2 正类的完整多载波传播门已经闭合", "The full multi-carrier propagation gate is closed for the fixed real-collinear-phase (in-phase or antiphase) 1:2 positive class");
row("阅读 R0.72P 研究笔记 →", "Read research note R0.72P →");
row("下一步 R0.72Q：", "Next R0.72Q:");
row("量化 phase-robust finite-pattern shape contract。", "Quantify a phase-robust finite-pattern shape contract.");
row("展开 76 篇公开笔记", "Expand 76 public research notes");
row("综述 v1.29 · 2026-08-27", "Review v1.29 · 2026-08-27");
row("上次综述 v1.28 · 2026-08-27", "Previous review v1.28 · 2026-08-27");
row("R0.72Q 测试 phase-robust finite-pattern shape contract", "R0.72Q tests a phase-robust finite-pattern shape contract");
row("一个完整两载波正类已闭合，一般 superposition 仍是独立问题", "A full two-carrier positive class is closed; general superposition remains a separate problem");
row("新的严格结果是 fixed real-collinear-phase 1:2 full-superposition ED、真实 cross cubic payment 与精确 Morse theorem-applicability wall。", "The new rigorous results are full-superposition ED for the fixed real-collinear-phase 1:2 class, payment of the genuine cross cubic, and the exact Morse theorem-applicability wall.");
row("R0.72L–R0.72P · strong-coupling、物理回填与完整两载波传播", "R0.72L–R0.72P · strong coupling, physical reinsertion, and full two-carrier propagation");
row("R0.72P 附图", "R0.72P figure");
row("R0.72P 证书", "R0.72P certificates");
row("查看 R0.72P 精确证书", "View the exact R0.72P certificates");
row("打开最新节点 R0.72P", "Open the latest node R0.72P");
row("保留 R0.72O 历史回顾", "Retain the historical R0.72O recap");
row("02 · 106 节完整索引", "02 · Complete index of 106 notes");
row("收录节点：106", "Included nodes: 106");
row("回顾截止时公开笔记：166", "Public notes at the recap cutoff: 166");
row("回顾截止节点：R0.72P", "Recap cutoff node: R0.72P");
row("R0.61–R0.72P 的 106 节公开笔记", "The 106 public notes from R0.61 through R0.72P");
row("R0.61–R0.72P 研究节点", "R0.61–R0.72P research nodes");
row("R0.70A–R0.72P 已公开版本", "Published releases from R0.70A through R0.72P");
row("R0.61–R0.72P｜R0.60 之后的研究回顾", "R0.61–R0.72P｜Research recap after R0.60");
row("R0.61–R0.72P 回顾 · 2026-08-27", "R0.61–R0.72P recap · 2026-08-27");
row("给单个非退化 time-dependent shear 的 modewise enhanced dissipation。R0.72P 先把完整 \\(R,2R\\) convolution 缩到固定 cell，再利用 Appendix A 的 fixed critical neighborhoods、cutoffs 与 uniform shape bounds，从 proof 中抽取对声明 \\(\\lambda\\)-family 一致的 constants；紧 \\(\\eta\\)-区间由本站 \\(L^2\\) contraction 补齐。", "gives modewise enhanced dissipation for a single nondegenerate time-dependent shear. R0.72P first reduces the full \\(R,2R\\) convolution to a fixed cell, then uses the fixed critical neighborhoods, cutoffs, and uniform shape bounds in Appendix A to extract constants uniform over the stated \\(\\lambda\\)-family; the remaining compact \\(\\eta\\)-range is completed here by \\(L^2\\) contraction.");
row("固定实系数同一直线相位（同相或反相） 1:2、B=2 与声明的 lambda cone 后，完整 propagator 有 uniform ED，真实 cross cubic gate 闭合；±1/4 仅为 Morse theorem-applicability wall。", "For the fixed real-collinear-phase (in-phase or antiphase) 1:2 pattern, B=2, and the stated lambda cone, the full propagator has uniform enhanced dissipation and the genuine cross-cubic gate closes; ±1/4 is only a Morse-theorem applicability wall.");
row("提供 stationary profile 的 hypocoercive 与 degeneracy-dependent 背景，但不直接陈述本站 heat-decaying 1:2 profile 或 physical cubic corollary。", "provide the hypocoercive and degeneracy-dependent background for stationary profiles, but do not directly state the heat-decaying 1:2 profile or the physical cubic corollary used here.");
row("正结果只覆盖 fixed real-collinear-phase 1:2、\\(B=2\\)、\\(0<\\lambda_-\\le|\\lambda|\\le1/8\\)。\\(\\lambda=\\pm1/4\\) 只证明该 Morse theorem 的适用条件退化，不证明 enhanced dissipation 失败。任意相位、任意 carrier 集或增长 \\(N\\)、fixed-\\(R\\) arbitrary coupling 与一般三维问题仍开放；限定检索不构成新颖性或优先权证明。", "The positive result covers only the fixed real-collinear-phase 1:2 class, \\(B=2\\), and \\(0<\\lambda_-\\le|\\lambda|\\le1/8\\). The value \\(\\lambda=\\pm1/4\\) proves only degeneration of the Morse theorem's hypotheses, not failure of enhanced dissipation. Arbitrary phases, arbitrary carrier sets or growing \\(N\\), arbitrary coupling at fixed \\(R\\), and the general three-dimensional problem remain open; the bounded search establishes neither novelty nor priority.");
row("\\(\\mathcal C_\\times\\lesssim a^2N^2\\sqrt\\varepsilon=4a^2\\sqrt\\varepsilon\\)，继承 \\(U_{\\rm ED}\\asymp\\varepsilon^{11/6}p^{4/3}\\)。", "The estimate \\(\\mathcal C_\\times\\lesssim a^2N^2\\sqrt\\varepsilon=4a^2\\sqrt\\varepsilon\\) holds and inherits \\(U_{\\rm ED}\\asymp\\varepsilon^{11/6}p^{4/3}\\).");
row("\\(|\\lambda|=1/4\\) 只证明当前 Morse-based theorem 不再可直接调用；它不证明 enhanced dissipation 失败，更不证明 Navier–Stokes 失稳。", "The value \\(|\\lambda|=1/4\\) shows only that the present Morse-based theorem can no longer be applied directly; it proves neither failure of enhanced dissipation nor Navier–Stokes instability.");
row("\\(E(y)\\le C_{\\rm ED}e^{-c_{\\rm ED}\\sqrt\\varepsilon y}E(0)\\)，常数只依赖固定 shape 上界，不依赖 \\(R,\\varepsilon,\\lambda\\) 或初值。", "The bound \\(E(y)\\le C_{\\rm ED}e^{-c_{\\rm ED}\\sqrt\\varepsilon y}E(0)\\) has constants depending only on the fixed upper shape bound, not on \\(R,\\varepsilon,\\lambda\\) or the initial datum.");
row("\\(r_1=R,r_2=2R,w_1=a,w_2=\\lambda a\\)，实系数同一直线相位（同相或反相），\\(B=N=2\\)、\\(p=2^{-1/2}\\)，且 \\(0<\\lambda_-\\le|\\lambda|\\le1/8\\)。", "Take \\(r_1=R,r_2=2R,w_1=a,w_2=\\lambda a\\) with real-collinear phases (in phase or antiphase), \\(B=N=2\\), \\(p=2^{-1/2}\\), and \\(0<\\lambda_-\\le|\\lambda|\\le1/8\\).");
row("01 · cell 约化", "01 · Cell reduction");
row("03 · 定理抽取", "03 · Theorem extraction");
row("04 · 紧参数补齐", "04 · Compact-parameter completion");
row("06 · 物理窗口", "06 · Physical window");
row("07 · Morse 墙", "07 · Morse wall");
row("窗口上沿仍只给统一有界；little-o 子区间才给 normalized ratio 衰减。fixed-\\(R\\) 任意强耦合没有闭合。", "The upper edge of the window gives only a uniform bound; the normalized ratio decays only in the little-o subwindow. Arbitrary strong coupling at fixed \\(R\\) remains open.");
row("当 \\(|\\lambda|\\le1/8\\) 时，括号始终位于 \\([1/2,3/2]\\)。临界集恰为 \\({0,\\pi}\\)，fixed neighborhoods、cutoffs、二阶下界及 profile 范数可对 \\(y\\in[0,1]\\) 和声明的 \\(\\lambda\\)-族统一选择。", "When \\(|\\lambda|\\le1/8\\), the factor always lies in \\([1/2,3/2]\\). The critical set is exactly \\({0,\\pi}\\), and fixed neighborhoods, cutoffs, the second-derivative lower bound, and the profile norms can be chosen uniformly for \\(y\\in[0,1]\\) and the stated \\(\\lambda\\)-family.");
row("对单个非退化时变剪切给 modewise \\(e^{-c\\eta^{1/2}|k|^{1/2}t}\\) 衰减。本站固定 critical neighborhoods 与 cutoffs，并用上一节的 uniform shape bounds 控制 Appendix A 的吸收常数，从 proof 中抽取统一 \\(\\eta_0,C_{\\rm ED},c_{\\rm ED}\\)。", "gives modewise \\(e^{-c\\eta^{1/2}|k|^{1/2}t}\\) decay for a single nondegenerate time-dependent shear. Here the critical neighborhoods and cutoffs are fixed, and the uniform shape bounds from the preceding section control the absorption constants in Appendix A, yielding uniform \\(\\eta_0,C_{\\rm ED},c_{\\rm ED}\\) from the proof.");
row("对载波 \\(R,2R\\)、实系数同一直线相位（同相或反相）、\\(B=2\\) 与 \\(0<\\lambda_-\\le|\\lambda|\\le1/8\\)，完整 affine-row propagator 满足常数对 \\(R,\\varepsilon\\ge1,\\lambda\\) 一致的 enhanced-dissipation 估计。所有 self/cross terms 都留在同一传播子内，因此 R0.72O 的 full-superposition cubic gate 在这个固定正类上无条件闭合。\\(\\lambda=\\pm1/4\\) 只是一手 Morse 定理的精确适用边界，不是 enhanced dissipation 失败。", "For carriers \\(R,2R\\), real-collinear phases (in phase or antiphase), \\(B=2\\), and \\(0<\\lambda_-\\le|\\lambda|\\le1/8\\), the full affine-row propagator satisfies an enhanced-dissipation estimate with constants uniform in \\(R,\\varepsilon\\ge1,\\lambda\\). All self and cross terms remain in the same propagator, so the full-superposition cubic gate from R0.72O closes unconditionally on this fixed positive class. The value \\(\\lambda=\\pm1/4\\) is only the exact applicability boundary of the cited Morse theorem, not a failure of enhanced dissipation.");
row("价值限于特殊 triangular 2.5D mechanism class；它不是一般三维稳定阈值，也不改变 Clay 问题仍开放的状态。", "The value is confined to a special triangular 2.5D mechanism class; this is not a general three-dimensional stability threshold and does not change the open status of the Clay problem.");
row("紧区间", "Compact range");
row("精确边界：", "Exact boundary:");
row("令 \\(t=\\varepsilon y\\)、\\(\\eta=\\varepsilon^{-1}\\)。Coble–He 控制充分小 \\(\\eta\\)；剩余紧区间由 skew transport 下的精确 \\(L^2\\) 收缩补齐，并扩大同一个固定 prefactor。", "Set \\(t=\\varepsilon y\\) and \\(\\eta=\\varepsilon^{-1}\\). Coble–He controls sufficiently small \\(\\eta\\); exact \\(L^2\\) contraction under skew transport completes the remaining compact range after enlarging one fixed prefactor.");
row("任意相位、任意 carrier 集、增长 \\(N\\)、fixed-\\(R\\) 任意耦合与一般三维问题都没有由本节闭合。", "This section closes none of arbitrary phases, arbitrary carrier sets, growing \\(N\\), arbitrary coupling at fixed \\(R\\), or the general three-dimensional problem.");
row("仍开放：任意相位、任意有限或增长 carrier 集、跨越 Morse wall 的 profile、fixed-\\(R\\) 任意 coupling、一般三维 continuation、有限时奇性与全局光滑性。Clay 千禧年问题仍未解决。", "Still open are arbitrary phases, arbitrary finite or growing carrier sets, profiles beyond the Morse wall, arbitrary coupling at fixed \\(R\\), general three-dimensional continuation, finite-time singularity, and global smoothness. The Clay Millennium Problem remains unsolved.");
row("是时变非退化剪切的直接输入；", "is the direct input for nondegenerate time-dependent shears;");
row("说明 profile 临界结构决定 enhanced-dissipation rate。", "show that the critical structure of the profile determines the enhanced-dissipation rate.");
row("下一步先量化 real-collinear phase locus 附近的可容许相位锥，或给出首个使 fixed critical neighborhoods 失效的精确反族。", "The next step is to quantify an admissible phase cone around the real-collinear phase locus, or to give the first exact counterfamily for which fixed critical neighborhoods fail.");
row("限定检索没有找到直接陈述本站 fixed real-collinear-phase 1:2 heat-decaying profile、\\(R\\)-uniform cell reduction、full cross cubic 与物理窗口的同一现成定理；这项检索不构成新颖性或优先权证明。", "The bounded search found no single existing theorem that directly states this fixed real-collinear-phase 1:2 heat-decaying profile, the \\(R\\)-uniform cell reduction, the full cross cubic, and the physical window; the search establishes neither novelty nor priority.");
row("形状", "Shape");
row("已闭合：fixed real-collinear-phase 1:2 pattern、\\(B=2\\)、声明的 \\(\\lambda\\)-cone、完整 affine row、任意初值与 exact-root correction。", "Closed are the fixed real-collinear-phase 1:2 pattern, \\(B=2\\), the stated \\(\\lambda\\)-cone, the full affine row, arbitrary initial data, and the exact-root correction.");
row("在 \\(y=0\\)，\\(\\lambda=1/4\\) 使 \\(\\phi=\\pi\\) 的前三个 \\(\\phi\\)-导数消失；\\(\\lambda=-1/4\\) 在 \\(\\phi=0\\) 同样退化，第四导数非零。越过该值还会出现额外临界点。", "At \\(y=0\\), \\(\\lambda=1/4\\) makes, at \\(\\phi=\\pi\\), the first three \\(\\phi\\)-derivatives vanish; \\(\\lambda=-1/4\\) has the same degeneracy at \\(\\phi=0\\), with nonzero fourth derivative. Additional critical points appear beyond this value.");
row("在 affine invariant row \\(\\Lambda_{R,q_*}=\\{(nR,q_*):n\\in\\mathbb Z\\}\\) 上令 \\(y=R^2x\\)、\\(\\phi=R\\theta\\)。完整 convolution 精确化为", "On the affine invariant row \\(\\Lambda_{R,q_*}=\\{(nR,q_*):n\\in\\mathbb Z\\}\\), set \\(y=R^2x\\) and \\(\\phi=R\\theta\\). The full convolution becomes exactly");
row("在本项目中首次把 multi-carrier gate 在一个非平凡完整正类上严格关闭", "For the first time in this project, the multi-carrier gate is rigorously closed on a nontrivial full positive class");
row("这里估计完整 superposition propagator；结论不依赖把两个 one-carrier estimates 相加。", "The estimate acts on the full superposition propagator; the conclusion does not rely on adding two one-carrier estimates.");
row("这是声明 1:2 参数族的 proof-level corollary，不是原论文逐字陈述的 arbitrary-family theorem，也不覆盖任意 Fourier superposition。", "This is a proof-level corollary for the stated 1:2 parameter family, not a verbatim arbitrary-family theorem from the source paper, and it does not cover arbitrary Fourier superpositions.");
row("cell 与 \\(R\\) 无关，并保留全部 self/cross coupling；没有逐载波求和。", "The cell is independent of \\(R\\) and retains every self and cross coupling; no carrierwise summation is used.");
row("Morse 墙", "Morse wall");
row("R0.72P 的增量不是再做一条 one-carrier estimate，而是证明 cross terms 共存时的完整传播子仍有 uniform enhanced dissipation，并把它接回 \\(\\varepsilon^{11/6}p^{4/3}\\) 物理账本。", "The R0.72P advance is not another one-carrier estimate: it proves uniform enhanced dissipation for the full propagator with cross terms present and reconnects it to the \\(\\varepsilon^{11/6}p^{4/3}\\) physical ledger.");
row("二十八个阶段、106 个节点：从约化递推到固定两载波 full-superposition ED。", "Twenty-eight phases and 106 nodes: from reduced recurrences to full-superposition ED for a fixed two-carrier class.");
row("截至 R0.72P，没有一般三维 continuation criterion，也没有证明有限时破裂或全局光滑性；不能把 106 个节点或 68 个公开版本解释成 Clay 问题完成比例。", "Through R0.72P there is no general three-dimensional continuation criterion and no proof of finite-time breakdown or global smoothness; 106 nodes or 68 public releases cannot be interpreted as a completion percentage for the Clay problem.");
row("先量化实系数同一直线相位 locus 附近的 uniform Morse cone，或构造 fixed critical neighborhoods 失效的精确反族。", "First quantify a uniform Morse cone around the real-collinear phase locus, or construct an exact counterfamily for which fixed critical neighborhoods fail.");
row("R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72P 的 106 个节点；最新一节闭合固定 1:2 两载波的完整传播门。", "Research recap after R0.60: complete coverage of the 106 nodes from R0.61 through R0.72P; the latest section closes the full propagation gate for a fixed 1:2 two-carrier class.");
row("R0.70A–R0.72P 的 68 节已公开；44 节按当前 formal-figure 合同完整封存；24 节旧档仍待回补。", "Sixty-eight releases from R0.70A through R0.72P are public; 44 are fully sealed under the current formal-figure contract, while 24 legacy archives still require backfill.");
row("R0.72L–N 保留 actual ledger 并排除声明一载波上的 action-poor route；R0.72O 将 \\(O(a^2\\sqrt\\varepsilon)\\) cubic 回填为 \\(\\varepsilon^{11/6}\\) physical numerator。", "R0.72L–N retain the actual ledger and exclude the action-poor route on the stated one-carrier class; R0.72O reinserts the \\(O(a^2\\sqrt\\varepsilon)\\) cubic as the \\(\\varepsilon^{11/6}\\) physical numerator.");
row("R0.72P 的 fixed-pattern full-superposition theorem：对实系数同一直线相位（同相或反相） \\(R:2R\\)、\\(B=2\\) 与声明的 \\(\\lambda\\)-cone，完整 propagator 的 \\(C_{\\rm ED},c_{\\rm ED}\\) 对 \\(R,\\varepsilon,\\lambda\\) 一致，因而 \\(\\mathcal C_\\times\\lesssim4a^2\\sqrt\\varepsilon\\)。\\(\\lambda=\\pm1/4\\) 只标记 Morse applicability wall。", "The R0.72P fixed-pattern full-superposition theorem: for real-collinear phases (in phase or antiphase) with \\(R:2R\\), \\(B=2\\), and the stated \\(\\lambda\\)-cone, the full propagator constants \\(C_{\\rm ED},c_{\\rm ED}\\) are uniform in \\(R,\\varepsilon,\\lambda\\), hence \\(\\mathcal C_\\times\\lesssim4a^2\\sqrt\\varepsilon\\). The value \\(\\lambda=\\pm1/4\\) marks only a Morse applicability wall.");
row("R0.72P 对 fixed real-collinear-phase 1:2、\\(B=2\\)、\\(0<\\lambda_-\\le|\\lambda|\\le1/8\\) 的完整 superposition 证明 uniform ED，从而闭合真实 \\(N=2\\) cross cubic。\\(\\lambda=\\pm1/4\\) 仅为 Morse theorem-applicability wall；任意相位与一般 carrier 集仍开放。", "R0.72P proves uniform enhanced dissipation for the full superposition in the fixed real-collinear-phase 1:2 class with \\(B=2\\) and \\(0<\\lambda_-\\le|\\lambda|\\le1/8\\), thereby closing the genuine \\(N=2\\) cross cubic. The value \\(\\lambda=\\pm1/4\\) is only a Morse-theorem applicability wall; arbitrary phases and general carrier sets remain open.");
row("R0.72P 只覆盖 fixed real-collinear-phase 1:2、\\(B=2\\) 与声明的 \\(\\lambda\\)-cone。任意相位、一般 carrier 集、fixed-\\(R\\) 任意耦合和 Clay 正式问题保持开放。", "R0.72P covers only the fixed real-collinear-phase 1:2 class, \\(B=2\\), and the stated \\(\\lambda\\)-cone. Arbitrary phases, general carrier sets, arbitrary coupling at fixed \\(R\\), and the formal Clay problem remain open.");
row("\\(\\lambda=\\pm1/4\\) 只是 Morse theorem-applicability wall；任意相位、一般 carrier 集、fixed-\\(R\\) 任意耦合与一般三维正则性仍开放。", "The value \\(\\lambda=\\pm1/4\\) is only a Morse-theorem applicability wall; arbitrary phases, general carrier sets, arbitrary coupling at fixed \\(R\\), and general three-dimensional regularity remain open.");
row("对 \\(R,2R\\)、\\(B=2\\)、\\(0<\\lambda_-\\le|\\lambda|\\le1/8\\)，完整 propagator 满足常数对 \\(R,\\varepsilon,\\lambda\\) 一致的 enhanced dissipation；所有 cross terms 都保留。", "For \\(R,2R\\), \\(B=2\\), and \\(0<\\lambda_-\\le|\\lambda|\\le1/8\\), the full propagator satisfies enhanced dissipation with constants uniform in \\(R,\\varepsilon,\\lambda\\), while retaining every cross term.");
row("累计回顾保持二十八个问题阶段，并给出 R0.61–R0.72P 的完整逐节点索引。R0.72P 对 fixed real-collinear-phase 1:2、\\(B=2\\) 与声明的 \\(\\lambda\\)-cone 证明 full-superposition ED，从而关闭一个真实 two-carrier cross-term gate。", "The cumulative recap retains twenty-eight problem phases and gives a complete node-by-node index through R0.72P. R0.72P proves full-superposition enhanced dissipation for the fixed real-collinear-phase 1:2 class with \\(B=2\\) and the stated \\(\\lambda\\)-cone, closing a genuine two-carrier cross-term gate.");
row("量化实系数同一直线相位 locus 附近的 uniform Morse cone，或构造 fixed critical neighborhoods 失效的精确反族。", "Quantify a uniform Morse cone around the real-collinear phase locus, or construct an exact counterfamily for which fixed critical neighborhoods fail.");
row("因此 \\(\\mathcal C_\\times\\lesssim4a^2\\sqrt\\varepsilon\\)，并接回 \\(U_{\\rm ED}\\asymp\\varepsilon^{11/6}p^{4/3}\\)、\\(p=2^{-1/2}\\) 的物理窗口。", "Therefore \\(\\mathcal C_\\times\\lesssim4a^2\\sqrt\\varepsilon\\), reconnecting to the physical window with \\(U_{\\rm ED}\\asymp\\varepsilon^{11/6}p^{4/3}\\) and \\(p=2^{-1/2}\\).");
row("R0.72P 已闭合 fixed real-collinear-phase 1:2 正类的 full-superposition ED；下一关是 phase-robust finite-pattern shape contract。", "R0.72P closes full-superposition enhanced dissipation for the fixed real-collinear-phase 1:2 positive class; the next gate is a phase-robust finite-pattern shape contract.");

function advance(value) {
  return value
    .replaceAll("v1.28", "v1.29")
    .replaceAll("R0.72O", "R0.72P")
    .replaceAll("r0-72o", "r0-72p")
    .replaceAll("r072o", "r072p")
    .replaceAll("105", "106")
    .replaceAll("165", "166")
    .replaceAll("67", "68")
    .replaceAll("43", "44")
    .replaceAll("seventy-five", "seventy-six")
    .replaceAll("one hundred five", "one hundred six")
    .replaceAll("one hundred and five", "one hundred and six");
}

function advanceLongRoute(entry, retainedByChinese) {
  const marker = "R0.72P 再把 fixed real-collinear-phase 1:2";
  const split = entry.zh.indexOf(marker);
  if (split < 0) return undefined;
  const previousRoute = retainedByChinese.get(entry.zh.slice(0, split))?.en;
  if (!previousRoute) return undefined;
  return previousRoute + " R0.72P then reduces the fixed real-collinear-phase 1:2 pattern, B=2, and the stated lambda cone to a fixed cell, extracts uniform constants from the Coble–He proof, and closes the full two-carrier cross-term gate; ±1/4 marks only the Morse applicability wall.";
}

const translations = JSON.parse(await readFile(translationPath, "utf8"));
const retained = translations.filter((entry) => !/^r072p\d+$/.test(entry.id));
const byChinese = new Map(retained.map((entry) => [entry.zh, entry]));
const advancedEnglish = new Map();
for (const entry of retained) {
  const zh = advance(entry.zh);
  if (zh !== entry.zh && !advancedEnglish.has(zh)) {
    advancedEnglish.set(zh, advance(entry.en));
  }
}

const source = await collectSiteStrings(publicDirectory);
const missing = source.filter((entry) => !byChinese.has(entry.zh));
const expectedFiles = [
  "literature-review.html",
  "notes/r0-72p.html",
  "recap-r0-61-r0-72p.html",
  "research-review.html",
];
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(missingFiles) !== JSON.stringify(expectedFiles)) {
  throw new Error("Unexpected R0.72P missing-string files: " + JSON.stringify(missingFiles));
}

const translatedEntries = missing.map((entry, index) => {
  const en = englishByChinese.get(entry.zh)
    ?? advancedEnglish.get(entry.zh)
    ?? advanceLongRoute(entry, byChinese);
  if (!en) {
    throw new Error("Missing explicit R0.72P English row for: " + entry.zh);
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error("Invalid R0.72P English row for: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("First-person plural English is forbidden for: " + entry.zh);
  }
  if (/^This (?:literature-boundary|R0\.72P note|cumulative-recap|route) entry\b/.test(en)) {
    throw new Error("Template English is forbidden for: " + entry.zh);
  }
  if (JSON.stringify(extractProtectedTokens(en)) !== JSON.stringify(extractProtectedTokens(entry.zh))) {
    throw new Error("Protected-token mismatch for:\n" + entry.zh + "\n" + en);
  }
  return { ...entry, id: "r072p" + String(index + 1).padStart(3, "0"), en };
});
if (translatedEntries.length !== 112) {
  throw new Error(`Expected 112 R0.72P English rows, found ${translatedEntries.length}`);
}

const finalTranslations = [...retained, ...translatedEntries];
for (const field of ["id", "zh"]) {
  const values = finalTranslations.map((entry) => entry[field]);
  if (new Set(values).size !== values.length) throw new Error("Duplicate final translation " + field);
}
const snapshot = missing.map(({ zh, count, files }) => ({ zh, count, files }));
if (checkOnly) {
  const currentSnapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
  if (JSON.stringify(currentSnapshot) !== JSON.stringify(snapshot)) {
    throw new Error("R0.72P missing-string snapshot is stale");
  }
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.72P translations/en.json batch is stale");
  }
} else {
  await writeFile(snapshotPath, JSON.stringify(snapshot, null, 2) + "\n");
  await writeFile(translationPath, JSON.stringify(finalTranslations, null, 2) + "\n");
}

console.log(JSON.stringify({
  checkOnly,
  added: translatedEntries.length,
  contextual: 0,
  total: finalTranslations.length,
  liveStrings: source.length,
  missingBefore: missing.length,
  missingAfter: 0,
  files: missingFiles,
}));
