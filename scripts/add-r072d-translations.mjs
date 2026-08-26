import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const projectRoot = resolve(import.meta.dirname, "..");
const translationsPath = resolve(projectRoot, "translations", "en.json");
const publicDirectory = resolve(projectRoot, "public");

const rows = [
  ["01 · 二十一个研究阶段", "01 · Twenty-one research phases"],
  ["02 · 94 节完整索引", "02 · Complete 94-note index"],
  ["把 Rudin–Shapiro 符号块平移到 \\(r_j=M+j\\) 后，任意前缀界与 Abel 求和保持 \\(\\Omega_0\\asymp\\sqrt M\\)，同时把 \\(\\int\\|V\\|\\) 和 \\(\\int\\|V\\|^2\\) 分别压到 \\(M^{-3/2}\\) 与 \\(M^{-1}\\)。取 \\(\\delta a=\\gamma M^{3/2}\\) 后，effective coupling 为 \\(\\eta\\asymp\\gamma M^2\\)，但 total Dyson exposure 仍为 \\(O(\\gamma)\\)。", "After shifting the Rudin–Shapiro sign block to \\(r_j=M+j\\), the arbitrary-prefix bound and Abel summation retain \\(\\Omega_0\\asymp\\sqrt M\\), while compressing \\(\\int\\|V\\|\\) and \\(\\int\\|V\\|^2\\) to \\(M^{-3/2}\\) and \\(M^{-1}\\), respectively. With \\(\\delta a=\\gamma M^{3/2}\\), the effective coupling is \\(\\eta\\asymp\\gamma M^2\\), but the total Dyson exposure remains \\(O(\\gamma)\\)."],
  ["保留 R0.72C 历史回顾", "Retain the historical R0.72C recap"],
  ["查看 R0.72D 双路证书", "View the R0.72D dual-path certificates"],
  ["打开最新节点 R0.72D", "Open the latest node R0.72D"],
  ["第一条路线把 \\(\\eta\\) 提到 \\(M^2\\) 以上，并同时改变 block height、width 或 phase geometry，检查 numerator 是否能比 full rotational charge 更快增长。", "The first route raises \\(\\eta\\) above \\(M^2\\) while changing the block height, width, or phase geometry, and tests whether the numerator can grow faster than the full rotational charge."],
  ["二十一个阶段、94 个节点：从约化递推和 complete-root 账本，到 physical phases，再到真实内点根与 full-charge normalized saturation。", "Twenty-one phases and 94 nodes: from reduced recurrences and the complete-root ledger, through physical phases, to a genuine interior root and full-charge normalized saturation."],
  ["回顾截止节点：R0.72D", "Recap endpoint: R0.72D"],
  ["回顾截止时公开笔记：154", "Public notes at the recap endpoint: 154"],
  ["截至 R0.72D，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 94 个节点或 56 个已公开并封存版本解释成对千禧年问题完成了某个比例。", "Through R0.72D, there is no new unconditional continuation criterion, no reduction of the full set of potential singular solutions, and no proof of finite-time breakdown. The 94 nodes or 56 published and archived releases cannot be interpreted as a percentage completion of the Millennium Problem."],
  ["静态 phase-free 上界已经由真实动力学达到，但比值仍停在 order one", "The static phase-free upper scale is attained by genuine dynamics, but the ratio remains order one"],
  ["累计回顾 · R0.61–R0.72D · 2026-08-27", "Cumulative recap · R0.61–R0.72D · 2026-08-27"],
  ["如果所有 supercritical routes 都让 \\(\\Lambda_1\\) 同阶增加，第二条路线就证明 triangular class 的 order-one ceiling。两条路线都必须保留 positive-time exact root、固定物理区间、完整 background cost 和 full-frequency charge。", "If every supercritical route increases \\(\\Lambda_1\\) at the same order, the second route is to prove an order-one ceiling for the triangular class. Both routes must retain a positive-time exact root, a fixed physical interval, the complete background cost, and the full-frequency charge."],
  ["收录节点：94", "Included nodes: 94"],
  ["与 target row 对齐的 launch data 在 \\(\\tau_M=M^{-3}\\) 经过一个 \\(O(M^{-1/2})e_0\\) 调整后产生 exact simple interior root，root slope 为 \\(aM\\) 量级。匹配的 \\(z\\)-independent background 支付完整 \\(D\\) 并保持 \\(\\mathcal R_Y=O(1)\\)；exact identity \\(\\mathbb P(u\\times\\omega)=(-vf_z,0,0)\\) 给 full-frequency charge \\(O(\\gamma^2)\\)。最终 \\(\\mathcal J_{\\rm all}/(D^{1/3}\\Lambda_1)\\) 有严格正下界，与 R0.72C upper ledger 同为 \\(M^0\\)。这不是发散或一般三维正则性结果。", "Launch data aligned with the target row produces an exact simple interior root at \\(\\tau_M=M^{-3}\\) after an \\(O(M^{-1/2})e_0\\) adjustment, with root slope of order \\(aM\\). A matched \\(z\\)-independent background pays the complete \\(D\\) and keeps \\(\\mathcal R_Y=O(1)\\); the exact identity \\(\\mathbb P(u\\times\\omega)=(-vf_z,0,0)\\) gives a full-frequency charge of \\(O(\\gamma^2)\\). Finally, \\(\\mathcal J_{\\rm all}/(D^{1/3}\\Lambda_1)\\) has a strict positive lower bound and, like the R0.72C upper ledger, is of order \\(M^0\\). This is neither divergence nor a general three-dimensional regularity result."],
  ["这个结果仍是 exact triangular 2.5D class 内的 sharpness theorem。比值保持有限，没有反驳 \\(D^{1/3}\\Lambda_1\\) payment。一般三维 vortex stretching 与 critical-norm continuation 仍未被触及。", "This remains a sharpness theorem inside the exact triangular 2.5D class. The ratio stays finite and does not refute the \\(D^{1/3}\\Lambda_1\\) payment. General three-dimensional vortex stretching and critical-norm continuation remain untouched."],
  ["这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72D 的 94 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。", "This page follows the R0.00–R0.60 phase recap and organizes 94 research nodes from R0.61 through R0.72D. I record in chronological order what each segment actually proved, which proposals were ruled out by a concrete counterexample or scaling analysis, and which conditions have not been derived from the Navier–Stokes equations. Node status describes the evidence type and does not mistake an archived release for a solved phase objective."],
  ["R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 94 个节点沿着这个缺口推进；R0.70A–R0.72D 的 56 个版本已经公开并封存，但其中仍包含条件定理、反例、有限诊断和开放缺口。", "The R0.00–R0.60 material remains in the preceding phase recap. The R0.60 conclusion was that the complete Fourier–Leray structure and higher-order calculations could continue, but the critical quantity for general three-dimensional solutions was not controlled. The following 94 nodes advance along this gap; 56 releases from R0.70A through R0.72D are published and archived, while still containing conditional theorems, counterexamples, finite diagnostics, and open gaps."],
  ["R0.60 之后的路线分成二十一个阶段", "The route after R0.60 is divided into twenty-one phases"],
  ["R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.72D 的 94 个研究节点；最新一节构造高频平移 Rudin–Shapiro 内点根，并在保留 full rotational charge 后得到非消失 normalized complete-root ledger。", "Research recap after R0.60: 94 nodes from R0.61 through R0.72D in chronological order; the latest note constructs a high-frequency shifted Rudin–Shapiro interior root and obtains a nonvanishing normalized complete-root ledger while retaining the full rotational charge."],
  ["R0.61–R0.72D 的 94 节公开笔记", "The 94 public notes from R0.61 through R0.72D"],
  ["R0.61–R0.72D 回顾 · 2026-08-27", "R0.61–R0.72D recap · 2026-08-27"],
  ["R0.61–R0.72D 研究节点", "R0.61–R0.72D research nodes"],
  ["R0.61–R0.72D｜R0.60 之后的研究回顾", "R0.61–R0.72D | Research recap after R0.60"],
  ["R0.72C 留下的实际根缺口已经关闭。高频平移 Rudin–Shapiro family 同时保留真实 positive-time root、complete target slope、full data cost、fixed-interval enstrophy contrast 和 full rotational charge；normalized complete ledger 不再随 \\(M\\) 消失。", "The actual-root gap left by R0.72C is closed. The high-frequency shifted Rudin–Shapiro family simultaneously retains a genuine positive-time root, complete target slope, full data cost, fixed-interval enstrophy contrast, and full rotational charge; the normalized complete ledger no longer vanishes with \\(M\\)."],
  ["R0.72D · 高频平移 Rudin–Shapiro 与真实 normalized saturation", "R0.72D · High-frequency shifted Rudin–Shapiro and genuine normalized saturation"],
  ["R0.72D 的 shifted Rudin–Shapiro dynamical saturation：\\(r_j=M+j\\) 的热权 multiplier 满足 \\(\\int\\|V_M\\|\\lesssim M^{-3/2}\\)、\\(\\int\\|V_M\\|^2\\lesssim M^{-1}\\)；\\(\\eta\\asymp M^2\\) 时仍有 bounded Dyson exposure。一个 \\(O(M^{-1/2})\\) launch adjustment 在 \\(\\tau_M=M^{-3}\\) 产生 exact simple interior root，slope 为 \\(M\\) 量级。匹配 background 与 full-frequency projected charge 给 bounded \\(\\mathcal R_Y\\) 和 \\(\\Lambda_1\\)，从而 complete normalized ledger 有正下界。该比值不发散，结论仍限于 exact triangular class。", "R0.72D shifted Rudin–Shapiro dynamical saturation: the heat-weighted multiplier for \\(r_j=M+j\\) satisfies \\(\\int\\|V_M\\|\\lesssim M^{-3/2}\\) and \\(\\int\\|V_M\\|^2\\lesssim M^{-1}\\); the Dyson exposure remains bounded when \\(\\eta\\asymp M^2\\). An \\(O(M^{-1/2})\\) launch adjustment produces an exact simple interior root at \\(\\tau_M=M^{-3}\\), with slope of order \\(M\\). The matched background and full-frequency projected charge give bounded \\(\\mathcal R_Y\\) and \\(\\Lambda_1\\), so the complete normalized ledger has a positive lower bound. The ratio does not diverge, and the conclusion remains confined to the exact triangular class."],
  ["R0.72D 附图", "R0.72D figure"],
  ["R0.72D 证书", "R0.72D certificates"],
  ["R0.72E 检查 supercritical growth 与 universal order-one ceiling", "R0.72E tests supercritical growth against a universal order-one ceiling"],
  ["查看独立逐式审计", "View the independent line-by-line audit"],
  ["从 complete-root 局部暴露走到真实内点根与 full-charge saturation", "From complete-root local exposure to a genuine interior root and full-charge saturation"],
  ["高频平移 Rudin–Shapiro 块把 phase-free 尖锐尺度实现为真实动力学下界", "A high-frequency shifted Rudin–Shapiro block realizes the sharp phase-free scale as a genuine dynamical lower bound"],
  ["环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \\(N^{-1}\\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \\(M^{-2}\\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → phase-uniform \\(M^{-8/3}\\) sharp algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation", "annular exclusion → source–kernel ledger → covariance-spectrum stratification → all-frequency conditional bridge → response-slope chord gain → common-response order-one channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \\(N^{-1}\\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \\(M^{-2}\\) suppression → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion → physical-phase conjugate pairing → sharp phase-uniform \\(M^{-8/3}\\) algebraic prefactor → shifted Rudin–Shapiro heat pulse → positive-time simple root → full-charge normalized order-one saturation"],
  ["检查 R0.72D 的 order-one dynamical saturation 能否被超临界增长超过，或是否存在 triangular class 的普适 order-one ceiling。", "Test whether supercritical growth can exceed the order-one dynamical saturation in R0.72D, or whether the triangular class has a universal order-one ceiling."],
  ["检查 supercritical growth 与 universal order-one ceiling：任何候选都必须保留 positive-time exact root、固定物理区间、完整 background cost 与 full-frequency charge。", "Test supercritical growth against a universal order-one ceiling: every candidate must retain a positive-time exact root, a fixed physical interval, the complete background cost, and the full-frequency charge."],
  ["静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–Z 依次处理 second-time jet、complete first row、fixed-small-coupling endpoint、selected roots 与 complete roots。R0.72A 把强耦合代价局部化到实际观察层，R0.72B 再以精确 target row 收紧 complete-root 前因子。R0.72C 对任意 physical Fourier phases 得到 sharp \\(M^{-8/3}\\) exact-launch prefactor。R0.72D 把 Rudin–Shapiro 块平移到 \\([M,2M)\\)，构造正时间简单根并保留完整数据成本、固定区间涡量与 full rotational charge；normalized complete-root ledger 有严格正下界，但仍停在 order one。", "After the static annular family is rigorously excluded, the main route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–Z treats the second-time jet, complete first row, fixed-small-coupling endpoint, selected roots, and complete roots. R0.72A localizes the strong-coupling cost to the actual observation layer, and R0.72B tightens the complete-root prefactor with the exact target row. R0.72C obtains the sharp \\(M^{-8/3}\\) exact-launch prefactor for arbitrary physical Fourier phases. R0.72D shifts the Rudin–Shapiro block to \\([M,2M)\\), constructs a simple positive-time root, and retains the full data cost, fixed-interval enstrophy, and full rotational charge; the normalized complete-root ledger has a strict positive lower bound but remains order one."],
  ["累计回顾 R0.61–R0.72D · 2026-08-27", "Cumulative recap R0.61–R0.72D · 2026-08-27"],
  ["令 \\(\\delta a=\\gamma M^{3/2}\\)，并用 \\(O(M^{-1/2})e_0\\) 调整与 target row 对齐的 launch data。在 \\(\\tau_M=M^{-3}>0\\) 得到 exact simple root，root slope 为 \\(aM\\) 量级。匹配的 \\(z\\)-independent background 支付全部 \\(D_M\\) 并保持 \\(\\mathcal R_Y=O(1)\\)；精确恒等式 \\(\\mathbb P(u\\times\\omega)=(-vf_z,0,0)\\) 给 full-frequency charge \\(O(\\gamma^2)\\)。", "Set \\(\\delta a=\\gamma M^{3/2}\\) and adjust launch data aligned with the target row by \\(O(M^{-1/2})e_0\\). This gives an exact simple root at \\(\\tau_M=M^{-3}>0\\), with root slope of order \\(aM\\). The matched \\(z\\)-independent background pays all of \\(D_M\\) and keeps \\(\\mathcal R_Y=O(1)\\); the exact identity \\(\\mathbb P(u\\times\\omega)=(-vf_z,0,0)\\) gives a full-frequency charge of \\(O(\\gamma^2)\\)."],
  ["目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.72D 在 exact triangular 2.5D class 中证明真实正时间根、完整 target slope 与 full rotational charge 可以同时保持非退化，使 normalized complete-root ledger 不再趋零；比值仍为 order one，因此不是 payment failure 或一般 NSE 正则性结论。", "There is currently no new unconditional continuation criterion and no construction of a finite-time singularity. Inside the exact triangular 2.5D class, R0.72D proves that a genuine positive-time root, the complete target slope, and the full rotational charge can remain nondegenerate together, so the normalized complete-root ledger no longer vanishes; the ratio remains order one, so this is neither a payment failure nor a general NSE regularity conclusion."],
  ["取 \\(M=2^n\\)、\\(r_j=M+j\\)、\\(w_j=a\\varepsilon_j\\)。任意前缀 Rudin–Shapiro 界与 Abel 求和给 \\[ \\|V_M(x)\\|\\lesssim a\\sqrt M e^{-\\kappa M^2x},\\qquad \\int\\|V_M\\|\\lesssim aM^{-3/2},\\qquad \\int\\|V_M\\|^2\\lesssim a^2M^{-1}. \\] 因而 phase cancellation 保留 \\(\\Omega_0\\asymp a\\sqrt M\\)，同时把 mixed exposure 压到 \\(O(M^{-2})\\)。", "Take \\(M=2^n\\), \\(r_j=M+j\\), and \\(w_j=a\\varepsilon_j\\). The arbitrary-prefix Rudin–Shapiro bound and Abel summation give \\[ \\|V_M(x)\\|\\lesssim a\\sqrt M e^{-\\kappa M^2x},\\qquad \\int\\|V_M\\|\\lesssim aM^{-3/2},\\qquad \\int\\|V_M\\|^2\\lesssim a^2M^{-1}. \\] Thus phase cancellation retains \\(\\Omega_0\\asymp a\\sqrt M\\) while compressing the mixed exposure to \\(O(M^{-2})\\)."],
  ["上次综述 v1.16 · 2026-08-27", "Previous review v1.16 · 2026-08-27"],
  ["我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.72D 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。", "I also maintain a systematic review that places classical theory, five main literature strands, the candidate-blowup exclusion tree, progress from 2019–2026, and this site's R0.69P–R0.72D route in one view. The historical R0.61–R0.69O nodes remain in the cumulative recap."],
  ["下一步 R0.72E：", "Next step R0.72E:"],
  ["先把 effective coupling 提到 \\(M^2\\) 以上，并改变 block height、width 或 phase geometry，检查 normalized numerator 能否比 full rotational charge 更快增长。若所有路线都同步抬高 \\(\\Lambda_1\\)，则转向证明 triangular class 的普适 order-one ceiling。", "First raise the effective coupling above \\(M^2\\) and change the block height, width, or phase geometry to test whether the normalized numerator can grow faster than the full rotational charge. If every route raises \\(\\Lambda_1\\) at the same order, turn to proving a universal order-one ceiling for the triangular class."],
  ["研究笔记 R0.72D · 2026-08-27", "Research note R0.72D · 2026-08-27"],
  ["阅读 R0.72D 研究笔记 →", "Read research note R0.72D →"],
  ["展开 64 篇公开笔记", "Expand 64 public notes"],
  ["这是 exact triangular 2.5D class 内的 dynamical sharpness theorem。它没有反驳 \\(D^{1/3}\\Lambda_1\\) payment，没有构造有限时奇性，也没有给出一般三维 continuation 或 global regularity。", "This is a dynamical sharpness theorem inside the exact triangular 2.5D class. It does not refute the \\(D^{1/3}\\Lambda_1\\) payment, construct a finite-time singularity, or give general three-dimensional continuation or global regularity."],
  ["综述 v1.17 · 2026-08-27", "Review v1.17 · 2026-08-27"],
  ["最终 \\[ \\liminf_{M\\to\\infty} \\frac{\\mathcal J_{{\\rm all},M}} {D_M^{1/3}\\Lambda_1(I;u_M)} \\ge c\\frac{\\gamma^{4/3}}{\\nu^2+\\gamma^2}>0. \\] 这关闭了“\\(M^{-8/3}\\) 只是静态前因子”的缺口，但比值没有发散。", "Finally, \\[ \\liminf_{M\\to\\infty} \\frac{\\mathcal J_{{\\rm all},M}} {D_M^{1/3}\\Lambda_1(I;u_M)} \\ge c\\frac{\\gamma^{4/3}}{\\nu^2+\\gamma^2}>0. \\] This closes the gap that \\(M^{-8/3}\\) might be only a static prefactor, but the ratio does not diverge."],
  ["R0.60 之后的累计回顾按二十一个阶段组织。R0.61–R0.69O 保留约化递推、剪切边界、横向扰动与压力局部预算；R0.69P–R0.71T 依次检查静态环带、协方差谱、projected-Lamb heat、faces、incidence 与真实内部 entry；R0.71U–R0.71Z 处理 second-time jet、complete first row 与全部根边界；R0.72A–C 依次给出 local exposure、target-row participation 与 physical-phase sharp prefactor；R0.72D 再把这个静态尖锐尺度实现为 positive-time exact root 与 full-charge normalized order-one saturation。R0.70A–R0.72D 共 56 个已公开并封存版本。", "The cumulative recap after R0.60 is organized into twenty-one phases. R0.61–R0.69O retains reduced recurrences, shear boundaries, transverse perturbations, and local pressure budgets; R0.69P–R0.71T examines static annuli, covariance spectra, projected-Lamb heat, faces, incidence, and genuine internal entry; R0.71U–R0.71Z treats the second-time jet, complete first row, and the all-root boundary; R0.72A–C gives local exposure, target-row participation, and the physical-phase sharp prefactor; R0.72D then realizes this static sharp scale as a positive-time exact root with full-charge normalized order-one saturation. R0.70A–R0.72D contains 56 published and archived releases."],
  ["R0.60 recap 之后的累计回顾收录 94 个节点；全站现有 154 篇公开研究笔记", "The cumulative recap after R0.60 contains 94 nodes; the full site now has 154 public research notes"],
  ["R0.70A–R0.72D 已公开并封存版本", "R0.70A–R0.72D published and archived releases"],
  ["R0.72D 已完成：", "R0.72D completed:"],
  ["shifted Rudin–Shapiro block 在正时间产生 simple target root；完整数据成本、fixed-interval enstrophy 与 full rotational charge 同时保留，normalized complete-root ledger 达到非消失的 order-one 尺度。", "The shifted Rudin–Shapiro block produces a simple target root at positive time; the full data cost, fixed-interval enstrophy, and full rotational charge are retained together, and the normalized complete-root ledger reaches a nonvanishing order-one scale."],
  ["打开 94 节完整索引", "Open the complete 94-note index"],
  ["高频平移使 multiplier exposure 缩到 \\(M^{-3/2}\\)，同时保留 phase-flat \\(\\sqrt M\\) norm。一个精确 launch adjustment 在 \\(\\tau_M=M^{-3}>0\\) 产生 simple root；fixed-interval enstrophy、完整数据成本与 full-frequency rotational charge 全部计入后，normalized complete-root ledger 有严格正下界，但仍为 order one。", "The high-frequency shift compresses the multiplier exposure to \\(M^{-3/2}\\) while retaining a phase-flat \\(\\sqrt M\\) norm. An exact launch adjustment produces a simple root at \\(\\tau_M=M^{-3}>0\\); after the fixed-interval enstrophy, complete data cost, and full-frequency rotational charge are all included, the normalized complete-root ledger has a strict positive lower bound but remains order one."],
  ["检查 coupling 超过 \\(M^2\\) 时 normalized numerator 能否比 full charge 更快增长；若不能，转向 triangular class 的普适 order-one ceiling。", "Test whether the normalized numerator can grow faster than the full charge when the coupling exceeds \\(M^2\\); if not, turn to a universal order-one ceiling for the triangular class."],
  ["开放接口 · R0.72E", "Open interface · R0.72E"],
  ["控制 fixed 或 specially modulated shear 的 spatial norms，不计一个 complex Fourier coordinate 的 temporal zeros 或 crossing slopes。", " control spatial norms for fixed or specially modulated shears; they do not count temporal zeros or crossing slopes of a complex Fourier coordinate."],
  ["累计回顾与 94 节索引", "Cumulative recap and 94-note index"],
  ["文献综述 v1.17 · 2026-08-27", "Literature review v1.17 · 2026-08-27"],
  ["我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72D 只列为研究笔记。我不把计算或笔记外推成正则性定理。", "I list published theorems as established results, mark 2026 preprints separately, and list this site's R0.69P–R0.72D material only as research notes. I do not extrapolate calculations or notes into regularity theorems."],
  ["研究实一维抛物方程的 spatial zero set，也不适用于这里的 complex temporal coordinate。已核对主源没有提供 changing shifted profile 的 launch-inclusive root ledger 或 full-charge lower family；这是有限文献检索结论，不作绝对原创性或优先权声明。", " studies spatial zero sets for real one-dimensional parabolic equations and likewise does not apply to the complex temporal coordinate here. The checked primary sources do not provide a launch-inclusive root ledger or full-charge lower family for the changing shifted profile; this is a bounded literature-search conclusion, not an absolute claim of originality or priority."],
  ["中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V–W 分离 fixed zero-level trace 并排除 data-uniform complete first-row ledger。R0.71X 在 fixed-dimensional small-coupling family 内达到 one-third endpoint；R0.71Y 处理 selected roots；R0.71Z 给出 all-root slope-mass bound 和 launch-inclusive floor cancellation；R0.72A 把 strong-coupling loss 局部化到实际观察层，R0.72B 保留 exact target-row participation，R0.72C 得到 phase-uniform exact-launch \\(M^{-8/3}\\) 与 fixed-positive tail \\(M^{-3}\\) 的 sharp algebraic scales。R0.72D 在 shifted Rudin–Shapiro family 上构造 positive-time exact root，保留 full rotational charge，并得到非消失但不发散的 normalized complete-root ledger。一般 Navier–Stokes 正则性仍开放。", ". R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–U establishes boundaries for conditional incidence, genuine internal entry, the second-time jet, and finite recurrence. R0.71V–W separates the fixed zero-level trace and rules out a data-uniform complete first-row ledger. R0.71X reaches the one-third endpoint in a fixed-dimensional small-coupling family; R0.71Y treats selected roots; R0.71Z gives an all-root slope-mass bound and launch-inclusive floor cancellation; R0.72A localizes the strong-coupling loss to the actual observation layer; R0.72B retains exact target-row participation; and R0.72C obtains the sharp algebraic scales of phase-uniform exact-launch \\(M^{-8/3}\\) and fixed-positive tail \\(M^{-3}\\). R0.72D constructs a positive-time exact root in a shifted Rudin–Shapiro family, retains the full rotational charge, and obtains a normalized complete-root ledger that is nonvanishing but not divergent. General Navier–Stokes regularity remains open."],
  ["R0.72D 把 Rudin–Shapiro 符号块平移到 \\([M,2M)\\)。prefix bound 与 Abel 求和给 \\(\\int\\|V_M\\|\\lesssim M^{-3/2}\\) 和 \\(\\ell_\\times=O(M^{-2})\\)。在 \\(\\delta a=\\gamma M^{3/2}\\) 下，一个复标量 launch adjustment 通过完整 evolution operator 在 \\(\\tau_M=M^{-3}\\) 产生 exact simple root；解析 Duhamel 估计给 \\(M\\)-量级 slope。匹配 background 进入 \\(D\\) 与 \\(Y\\)，exact identity \\(\\mathbb P(u\\times\\omega)=(-vf_z,0,0)\\) 保留所有 Fourier 频率的 rotational charge。", "R0.72D shifts the Rudin–Shapiro sign block to \\([M,2M)\\). The prefix bound and Abel summation give \\(\\int\\|V_M\\|\\lesssim M^{-3/2}\\) and \\(\\ell_\\times=O(M^{-2})\\). Under \\(\\delta a=\\gamma M^{3/2}\\), a complex scalar launch adjustment through the complete evolution operator produces an exact simple root at \\(\\tau_M=M^{-3}\\); an analytic Duhamel estimate gives slope of order \\(M\\). The matched background enters \\(D\\) and \\(Y\\), while the exact identity \\(\\mathbb P(u\\times\\omega)=(-vf_z,0,0)\\) retains the rotational charge at every Fourier frequency."],
  ["R0.72D 的动力学下界与文献边界", "The R0.72D dynamical lower bound and literature boundary"],
  ["R0.72D 的主源边界", "Primary-source boundary for R0.72D"],
  ["shifted Rudin–Shapiro 与真实 full-charge saturation", "Shifted Rudin–Shapiro and genuine full-charge saturation"],
  ["\\(D^{1/3}\\Lambda_1\\) 支付的反例或证明；有限时奇性；无条件继续性；一般三维 global regularity；原创性或优先权结论。", "a counterexample to or proof of the \\(D^{1/3}\\Lambda_1\\) payment; a finite-time singularity; unconditional continuation; general three-dimensional global regularity; or claims of originality or priority."],
  ["\\(M^{-8/3}\\) 与 \\(\\eta^{4/3}\\) 在临界耦合处精确抵消", "\\(M^{-8/3}\\) and \\(\\eta^{4/3}\\) cancel exactly at the critical coupling"],
  ["01 · 高频相消块", "01 · High-frequency cancellation block"],
  ["02 · 精确内点根", "02 · Exact interior root"],
  ["03 · 固定区间涡量", "03 · Fixed-interval enstrophy"],
  ["04 · 完整旋转电荷", "04 · Full rotational charge"],
  ["05 · 非消失账本", "05 · Nonvanishing ledger"],
  ["90 位精度重建 RS 递推、平移矩、Abel 热权、目标行等号与临界幂次。它核对有限代数，不求解有限格 ODE。", "Reconstructs the RS recurrence, shifted moment, Abel heat weights, target-row equality, and critical powers at 90-digit precision. It checks finite algebra and does not solve the finite-lattice ODE."],
  ["版本 v0.72D · 2026-08-27", "Version v0.72D · 2026-08-27"],
  ["不导入 producer 或其结果；使用 binary-parity RS 路径、FFT envelope、独立有限矩阵和 ODE root adjustment，并核对实际归一化后的 \\(K_f\\) 与精确振幅配平。", "Does not import the producer or its result; uses a binary-parity RS path, FFT envelope, independent finite matrices, and ODE root adjustment, and checks the actual normalized \\(K_f\\) and exact amplitude balance."],
  ["大瞬时 Lamb 分量只持续一个 \\(M^{-2}\\) 热脉冲", "The large instantaneous Lamb component lasts only for one \\(M^{-2}\\) heat pulse"],
  ["对千禧年问题的价值仍是模型边界：这条机制表明单靠 carrier participation 不能把所有强耦合 triangular profiles 压到零，但它没有产生发散，更没有控制一般三维 vortex stretching。它把下一问缩成了“能否超过 order one，还是存在新的普适 ceiling”。", "Its value for the Millennium Problem remains a model boundary: the mechanism shows that carrier participation alone cannot force every strongly coupled triangular profile to zero, but it produces no divergence and does not control general three-dimensional vortex stretching. It narrows the next question to whether order one can be exceeded or a new universal ceiling exists."],
  ["分母为 \\(1+O(M^{-1})\\)，而 \\(\\zeta_M=O(M^{-1/2})\\)。把 \\(G_M+\\zeta_Me_0\\) 整体归一到范数平方 \\(M\\)，就得到精确根", "The denominator is \\(1+O(M^{-1})\\), while \\(\\zeta_M=O(M^{-1/2})\\). Normalizing \\(G_M+\\zeta_Me_0\\) as a whole to squared norm \\(M\\) gives the exact root"],
  ["附图同时展示热尺度塌缩与真实根斜率不塌缩", "The figure shows both thermal-scale collapse and a noncollapsing genuine-root slope"],
  ["高频块", "High-frequency block"],
  ["根处 \\(F_{M,0}'=\\delta P_0V_MF_M\\ne0\\)，所以这是简单内点根。这里没有把首阶 Dyson 近似当成真实根。", "At the root, \\(F_{M,0}'=\\delta P_0V_MF_M\\ne0\\), so it is a simple interior root. A first-order Dyson approximation is not being treated as the genuine root."],
  ["解析报告和独立逐式审计承担无限格与物理归一化证明。证书记录命令、配置、环境、进度、资源和 SHA-256；它不是 interval arithmetic 或一般 NSE 正则性证明。", "The analytic report and independent line-by-line audit carry the infinite-lattice and physical-normalization proof. The certificates record commands, configuration, environment, progress, resources, and SHA-256; they are neither interval arithmetic nor a proof of general NSE regularity."],
  ["解析证明、producer 与独立 checker 分开承担不同责任", "The analytic proof, producer, and independent checker carry separate responsibilities"],
  ["令 \\(\\delta a=\\gamma M^{3/2}\\)，所以 \\(\\eta\\asymp\\gamma M^2\\)，但总 Dyson exposure 仅为 \\(O(\\gamma)\\)。记完整演化算子为 \\(U_M\\)，取 \\(\\tau_M=M^{-3}\\)，并定义", "Set \\(\\delta a=\\gamma M^{3/2}\\), so \\(\\eta\\asymp\\gamma M^2\\), while the total Dyson exposure is only \\(O(\\gamma)\\). Let the complete evolution operator be \\(U_M\\), take \\(\\tau_M=M^{-3}\\), and define"],
  ["令实际 active moment 为 \\(K_f\\)，则 \\(K_f=K_s[1+O(M^{-2})]\\)。我选择物理振幅满足精确平衡", "Let the actual active moment be \\(K_f\\), so \\(K_f=K_s[1+O(M^{-2})]\\). I choose physical amplitudes satisfying the exact balance"],
  ["另一方面，R0.72C upper ledger 中", "On the other hand, in the R0.72C upper ledger"],
  ["目标行在启动时达到 Cauchy–Schwarz 等号，微小调整把零点移到正时间", "The target row attains equality in Cauchy–Schwarz at launch, and a small adjustment moves the zero to positive time"],
  ["内点根", "Interior root"],
  ["内点根的固定壳原子满足", "The fixed-shell atom at the interior root satisfies"],
  ["匹配背景支付完整数据成本，也把 \\(\\mathcal R_Y\\) 保持在常数量级", "The matched background pays the complete data cost and keeps \\(\\mathcal R_Y\\) at order one"],
  ["取 \\(M=2^n\\)、Rudin–Shapiro 符号 \\(\\varepsilon_j\\)，并令", "Take \\(M=2^n\\), Rudin–Shapiro signs \\(\\varepsilon_j\\), and set"],
  ["取与目标行对齐的有限支撑向量", "Take a finite-support vector aligned with the target row"],
  ["任意前缀 Rudin–Shapiro 界与 Abel 求和给出带不等热权的统一估计：", "The arbitrary-prefix Rudin–Shapiro bound and Abel summation give a uniform estimate with unequal heat weights:"],
  ["如果每条这样的路线都让 \\(\\Lambda_1\\) 同阶增加，就转向证明 triangular class 的 universal order-one ceiling。两条路线都必须保留正时间 exact root、固定物理区间、完整数据成本和 full charge。", "If every such route increases \\(\\Lambda_1\\) at the same order, turn to proving a universal order-one ceiling for the triangular class. Both routes must retain a positive-time exact root, a fixed physical interval, the complete data cost, and the full charge."],
  ["三角形解有精确恒等式", "The triangular solution has the exact identity"],
  ["所以 \\(\\Lambda_1(I;u_M)\\le C_{I,\\gamma}(\\nu^2+\\gamma^2)\\)。这是 full-frequency upper bound，不是一个 selected-shell surrogate。", "Therefore \\(\\Lambda_1(I;u_M)\\le C_{I,\\gamma}(\\nu^2+\\gamma^2)\\). This is a full-frequency upper bound, not a selected-shell surrogate."],
  ["所有 \\(vf_z\\) 模都保留固定非零 \\(z\\)-频率，因此 \\(\\dot H^{-1}\\) 可由完整 \\(L^2\\) 乘积控制。没有删掉 target-complement 或 off-diagonal convolution。热权 multiplier 进一步给出", "Every \\(vf_z\\) mode retains a fixed nonzero \\(z\\)-frequency, so \\(\\dot H^{-1}\\) is controlled by the complete \\(L^2\\) product. No target-complement or off-diagonal convolution is removed. The heat-weighted multiplier further gives"],
  ["图 R0.72D-1。A：不同 \\(M\\) 的 heat-weighted multiplier 以 \\(s=M^2x\\) 重标后塌缩，说明 spectral translation 把暴露压到 \\(M^{-2}\\)。B：有限格精确根的 slope ratio 与 normalized ledger/charge diagnostics 保持常数量级。数值根残差与斜率只作有限诊断；解析 Duhamel 证明承担极限结论。", "Figure R0.72D-1. A: heat-weighted multipliers for different \\(M\\) collapse after rescaling by \\(s=M^2x\\), showing that spectral translation compresses the exposure to \\(M^{-2}\\). B: the slope ratio and normalized ledger/charge diagnostics for finite-lattice exact roots remain of order one. Numerical root residuals and slopes are finite diagnostics only; the analytic Duhamel proof carries the limiting conclusion."],
  ["完整归一化账本不再趋零，但也没有发散", "The complete normalized ledger no longer vanishes, but it does not diverge"],
  ["涡量", "Enstrophy"],
  ["我会先尝试把 \\(\\eta\\) 提高到 \\(M^2\\) 以上，同时继续缩短热暴露或改变 carrier geometry，检查 normalized numerator 能否比 full charge 更快增长。", "I will first try to raise \\(\\eta\\) above \\(M^2\\) while further shortening the thermal exposure or changing the carrier geometry, and test whether the normalized numerator can grow faster than the full charge."],
  ["下一对象：supercritical growth or ceiling", "Next object: supercritical growth or a ceiling"],
  ["相位抵消不是静态假象，", "Phase cancellation is not a static artifact,"],
  ["相位平坦性保持，热暴露缩短两个 \\(M\\) 次幂", "Phase flatness remains while the thermal exposure loses two powers of \\(M\\)"],
  ["旋转电荷", "Rotational charge"],
  ["研究笔记 R0.72D · SHIFTED RUDIN–SHAPIRO · INTERIOR ROOT · FULL CHARGE", "Research note R0.72D · SHIFTED RUDIN–SHAPIRO · INTERIOR ROOT · FULL CHARGE"],
  ["研究笔记 R0.72D：构造平移到高频块的 Rudin–Shapiro 精确三角形 NSE 解，在正时间产生简单目标根，并在保留完整旋转电荷后得到非消失的归一化 complete-root ledger。", "Research note R0.72D: an exact triangular NSE solution with a Rudin–Shapiro block shifted to high frequency produces a simple target root at positive time and a nonvanishing normalized complete-root ledger after the full rotational charge is retained."],
  ["因此 \\(\\Omega_0\\asymp a\\sqrt M\\)、\\(\\chi_0\\asymp1\\)，R0.72C 的 carrier coefficient 仍为 \\(M^{-8/3}\\)。但 mixed exposure 已变成 \\(\\ell_\\times=O(M^{-2})\\)。", "Thus \\(\\Omega_0\\asymp a\\sqrt M\\) and \\(\\chi_0\\asymp1\\), and the R0.72C carrier coefficient remains \\(M^{-8/3}\\). The mixed exposure, however, becomes \\(\\ell_\\times=O(M^{-2})\\)."],
  ["因此上界和下界都为 \\(M^0\\)。这证明的是尺度锐性，不是一个普适最优常数。", "Therefore both the upper and lower bounds are of order \\(M^0\\). This proves scale sharpness, not a universal optimal constant."],
  ["用 lattice multiplier \\(R e_r=re_r\\) 计算 commutator，可得", "Computing the commutator with the lattice multiplier \\(R e_r=re_r\\) gives"],
  ["再加入一个 \\(z\\)-无关的固定低频背景，振幅为 \\(B_M^{\\rm bg}=b_0qE_M^{1/2}/Q\\)。它的全部初始成本进入 \\(D_M\\)，但它既不进入目标响应，也不进入投影 Lamb 向量。固定物理区间 \\(I=[0,T]\\) 上，", "Add a fixed low-frequency \\(z\\)-independent background with amplitude \\(B_M^{\\rm bg}=b_0qE_M^{1/2}/Q\\). Its entire initial cost enters \\(D_M\\), but it enters neither the target response nor the projected Lamb vector. On the fixed physical interval \\(I=[0,T]\\),"],
  ["载频矩为", "The carrier moment is"],
  ["这个结果证明 R0.72C 的 phase-free 尺度可以由真实动力学实现，并且 full \\(\\Lambda_1\\) charge 没有被丢掉。比值保持有限，所以它不是 \\(D^{1/3}\\Lambda_1\\) 支付失败的反例，更不是一般三维奇性构造。", "This result proves that the phase-free scale in R0.72C can be realized by genuine dynamics without dropping the full \\(\\Lambda_1\\) charge. The ratio remains finite, so it is neither a counterexample to the \\(D^{1/3}\\Lambda_1\\) payment nor a construction of a general three-dimensional singularity."],
  ["这里 \\(u_M\\) 是精确光滑无外力三维 Navier–Stokes 解，属于 \\(u=(f(y,z,t),0,v(y,t))\\) 的三角形 2.5D 子类。根位于 \\(t_M=q^{-2}M^{-3}>0\\)，不是启动端点。完整账本至少包含这个根；其他根只会增加非负分子。", "Here \\(u_M\\) is an exact smooth unforced three-dimensional Navier–Stokes solution in the triangular 2.5D subclass \\(u=(f(y,z,t),0,v(y,t))\\). The root lies at \\(t_M=q^{-2}M^{-3}>0\\), not at the launch endpoint. The complete ledger contains at least this root; any other roots only increase the nonnegative numerator."],
  ["这是实际动力学下界，不再只是静态前因子", "This is a genuine dynamical lower bound, not merely a static prefactor"],
  ["真实动力学可以达到临界尺度", "Genuine dynamics can attain the critical scale"],
  ["真实内点根、完整斜率质量和 full rotational charge 在 η≈M² 的临界尺度上同时保持非退化。", "A genuine interior root, complete slope mass, and the full rotational charge remain nondegenerate together at the critical scale η≈M²."],
  ["振幅平衡和 \\(K_s\\asymp M^3\\) 给", "The amplitude balance and \\(K_s\\asymp M^3\\) give"],
  ["证明、文献边界、双路证书与期刊附图包完整保留", "The proof, literature boundary, dual-path certificates, and journal figure package are preserved in full"],
  ["状态 · R0.72D 完成", "Status · R0.72D complete"],
  ["heat-stable shifted RS bound；正时间简单根；非塌缩 slope；bounded \\(\\mathcal R_Y\\)；full-frequency charge \\(O(\\gamma^2)\\)；normalized complete ledger 的正下界。", "a heat-stable shifted RS bound; a simple positive-time root; a noncollapsing slope; bounded \\(\\mathcal R_Y\\); full-frequency charge \\(O(\\gamma^2)\\); and a positive lower bound for the normalized complete ledger."],
  ["normalized ledger 发散；所有 triangular solutions 的 order-one ceiling；一般三维 critical-norm bridge。", "divergence of the normalized ledger; an order-one ceiling for all triangular solutions; or a general three-dimensional critical-norm bridge."],
  ["R0.72C 的 \\(M^{-8/3}\\) 只是静态假象；必须依赖 launch endpoint；terminal decay 可以删除 pre-ledger。", "that the R0.72C \\(M^{-8/3}\\) scale is only a static artifact; that a launch endpoint is required; or that terminal decay can remove the pre-ledger."],
  ["R0.72C 证明相位抵消会把 coherent \\(M^{-10/3}\\) 改成 phase-free \\(M^{-8/3}\\)，但那只是 upper-ledger coefficient。在当前路线里，本节把真实正时间根、完整 target slope、固定区间 enstrophy、full rotational charge 和非消失 normalized lower bound 放进同一条 exact NSE family。", "R0.72C proves that phase cancellation changes coherent \\(M^{-10/3}\\) to phase-free \\(M^{-8/3}\\), but that was only an upper-ledger coefficient. In the current route, this note places a genuine positive-time root, the complete target slope, fixed-interval enstrophy, the full rotational charge, and a nonvanishing normalized lower bound in one exact NSE family."],
  ["R0.72C 只证明了任意物理相位下 \\(M^{-8/3}\\) 代数前因子的尖锐性，没有证明真实目标根会达到它。本节把同一 Rudin–Shapiro 符号块平移到载频 \\([M,2M)\\)。相消仍使 multiplier norm 只有 \\(\\sqrt M\\)，但热寿命缩到 \\(M^{-2}\\)。在 \\(\\eta\\asymp M^2\\) 时，我构造了一个正时间简单根；它的 target-row slope 为 \\(M\\) 量级。匹配低频背景后，完整投影旋转电荷仍为常数量级，最终归一化 complete-root ledger 有严格正下界。", "R0.72C proved only the sharpness of the \\(M^{-8/3}\\) algebraic prefactor under arbitrary physical phases; it did not prove that a genuine target root attains it. This note shifts the same Rudin–Shapiro sign block to carrier frequencies \\([M,2M)\\). Cancellation still keeps the multiplier norm at only \\(\\sqrt M\\), while the thermal lifetime contracts to \\(M^{-2}\\). At \\(\\eta\\asymp M^2\\), I construct a simple positive-time root whose target-row slope is of order \\(M\\). After matching a low-frequency background, the full projected rotational charge remains of order one, and the final normalized complete-root ledger has a strict positive lower bound."],
  ["R0.72D · 2026-08-27 · 个人数学研究日志", "R0.72D · 2026-08-27 · Personal mathematics research log"],
  ["R0.72D｜高频平移 Rudin–Shapiro 与非消失 complete-root ledger", "R0.72D | High-frequency shifted Rudin–Shapiro and a nonvanishing complete-root ledger"],
  ["R0.72E 检查 supercritical growth 与 order-one ceiling", "R0.72E tests supercritical growth against an order-one ceiling"],
];

const translations = JSON.parse(await readFile(translationsPath, "utf8"));
const source = await collectSiteStrings(publicDirectory);
const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));
const existing = new Set(translations.map((entry) => entry.zh));
const mapped = new Map(rows);
const duplicateKeys = rows
  .map(([zh]) => zh)
  .filter((zh, index, values) => values.indexOf(zh) !== index);
if (duplicateKeys.length) {
  throw new Error("Duplicate mapping keys: " + duplicateKeys.join(" | "));
}

const missing = source.filter((entry) => !existing.has(entry.zh));
const unmapped = missing.filter((entry) => !mapped.has(entry.zh));
if (unmapped.length) {
  throw new Error(
    "R0.72D translation source drift (" +
      unmapped.length +
      " unmapped live strings):\n" +
      unmapped.map((entry) => entry.zh).join("\n---\n"),
  );
}

for (const [zh, en] of rows) {
  if (!sourceByChinese.has(zh) || existing.has(zh)) continue;
  if (!en.trim() || containsChinese(en)) {
    throw new Error("Invalid English translation for: " + zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("Collective English voice remains in: " + zh);
  }
  const zhTokens = extractProtectedTokens(zh);
  const enTokens = extractProtectedTokens(en);
  if (JSON.stringify(zhTokens) !== JSON.stringify(enTokens)) {
    throw new Error(
      "Protected-token mismatch for:\n" +
        zh +
        "\nZH " +
        JSON.stringify(zhTokens) +
        "\nEN " +
        JSON.stringify(enTokens),
    );
  }
}

let added = 0;
for (const [index, [zh, en]] of rows.entries()) {
  const live = sourceByChinese.get(zh);
  if (!live || existing.has(zh)) continue;
  translations.push({
    ...live,
    id: "r072d" + String(index + 1).padStart(3, "0"),
    en,
  });
  existing.add(zh);
  added += 1;
}

for (const field of ["id", "zh"]) {
  const seen = new Set();
  const duplicates = translations
    .map((entry) => entry[field])
    .filter((value) => seen.size === seen.add(value).size);
  if (duplicates.length) {
    throw new Error(
      "Duplicate " + field + " values: " + [...new Set(duplicates)].join(" | "),
    );
  }
}

await writeFile(translationsPath, JSON.stringify(translations, null, 2) + "\n");
console.log(
  JSON.stringify({
    added,
    total: translations.length,
    liveStrings: source.length,
    missingBefore: missing.length,
  }),
);
