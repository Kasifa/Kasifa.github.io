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
02 · 82 节完整索引 ||| 02 · Complete 82-section index
打开最新节点 R0.71R ||| Open the latest node R0.71R
各已生成的 HTML、PDF、首页路线入口和首页进展入口按版本保留。正式附图同时保留源数据、绘图程序、环境、独立验证和校验和。 ||| Generated HTML and PDF files, homepage route entries, and homepage progress entries are retained by version. Formal figures also retain the source data, plotting code, environment, independent validation, and checksums.
候选必须通过 integer-torus initial jet、sequential recurrence 与 repeated-window pressure tests。若 localization 丢失符号，或预算退回 \(L^2\)-Lamb / palinstrophy，我会保留条件并停止该分支。这一步不宣称已解决千禧年问题。 ||| Candidates must pass the integer-torus initial-jet, sequential-recurrence, and repeated-window pressure tests. If localization loses the sign, or the budget falls back to \(L^2\)-Lamb / palinstrophy, I will retain the condition and stop that branch. This step does not claim to have solved the Millennium Problem.
回顾截止节点：R0.71R ||| Recap endpoint: R0.71R
回顾截止时公开笔记：142 ||| Public notes at recap endpoint: 142
截至 R0.71R，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 82 个节点解释成对千禧年问题完成了某个比例。 ||| At R0.71R, there is no new unconditional continuation criterion, no narrowing of the set of all potential singular solutions, and no proof of finite-time breakdown. The 82 nodes cannot be interpreted as completing any percentage of the Millennium Problem.
累计回顾 · R0.61–R0.71R · 2026-08-26 ||| Cumulative recap · R0.61–R0.71R · 2026-08-26
目前最有内容的无条件正结果仍包括 Leray 能量级 projected-Lamb 热体积、有界重叠局部化、denominator mass、同刻 spatial batching，以及 R0.71R 在 rho=2 下由 Leray energy 支付的 truncation-uniform source integral；frame constants 因 frame 固定而不依赖 finite truncation。完整 theorem 右端仍可能因 upper comparison constant (Gamma_2) 与 essential overlap (M) 而不一致；uniform lower height 与 forward-window availability 是额外 theorem gates，不是右端因子，且同样尚未证明。 ||| The most substantive unconditional positive results still include the projected-Lamb heat volume at the Leray energy level, bounded-overlap localization, denominator mass, same-time spatial batching, and, in R0.71R at rho=2, the truncation-uniform source integral paid by Leray energy; the frame constants are independent of finite truncation because the frame is fixed. The full theorem right-hand side may still be nonuniform because of the upper comparison constant (Gamma_2) and essential overlap (M); uniform lower height and forward-window availability are additional theorem gates, not right-hand-side factors, and likewise remain unproved.
十二个阶段、82 个节点：从约化递推到 positive-entry batching，再到条件 Jensen、有限 parabolic incidence theorem 与 rho=0/rho=2 两阶错配。 ||| Twelve stages and 82 nodes: from reduced recurrences to positive-entry batching, then conditional Jensen, a finite parabolic incidence theorem, and the two-order rho=0/rho=2 mismatch.
收录节点：82 ||| Included nodes: 82
下一步保留 entry direction 与 signed pairing，不再把目标先压成 quadratic post-entry amplitude。R0.71S 将检查是否存在 frame-summable、由 \(\dot H^{-1}\) 支付且 scale covariant 的 directional or bilinear packet functional。 ||| The next step retains entry direction and signed pairing instead of first reducing the target to a quadratic post-entry amplitude. R0.71S will test whether a frame-summable directional or bilinear packet functional exists that is paid by \(\dot H^{-1}\) and is scale covariant.
这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71R 的 82 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。 ||| This page follows the R0.00–R0.60 stage recap and organizes the research nodes from R0.61 through R0.71R, 82 in total. I record chronologically what each stage actually proves, which proposals are excluded by specific counterexamples or scaling analyses, and which conditions have not been derived from the Navier–Stokes equations.
localized forced heat equation、带 uniform lower height 与 essential overlap hypotheses 的 finite conditional incidence packing、rho-dependent source ledger，以及 covariant optimal constant / rho=2 minimal Leray payment 的精确两阶错配；NSE 高频例只定义 initial first-jet surrogate。 ||| localized forced heat equation; finite conditional incidence packing with uniform-lower-height and essential-overlap hypotheses; rho-dependent source ledger; and the exact two-order mismatch between the covariant optimal constant and minimal Leray payment at rho=2; the high-frequency NSE example defines only an initial first-jet surrogate.
R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 82 个节点沿着这个缺口推进。 ||| The R0.00–R0.60 material remains in the previous stage recap. R0.60 concludes that the full Fourier–Leray structure and higher-order calculations can continue, but still do not control a critical quantity for general three-dimensional solutions. The subsequent 82 nodes advance along this gap.
R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71R 的 82 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 Jensen 定理与 parabolic-incidence 两阶尺度错配的路线。 ||| Research recap after R0.60: a chronological account from R0.61 through R0.71R, covering 82 research nodes and recording the route from reduced recurrences to projected-Lamb heat volume, positive-entry batching, the conditional Jensen theorem, and the two-order parabolic-incidence scaling mismatch.
R0.61–R0.71R 的 82 节公开笔记 ||| Public notes from R0.61–R0.71R: 82 sections
R0.61–R0.71R 回顾 · 2026-08-26 ||| R0.61–R0.71R recap · 2026-08-26
R0.61–R0.71R 研究节点 ||| R0.61–R0.71R research nodes
R0.61–R0.71R｜R0.60 之后的研究回顾 ||| R0.61–R0.71R | Research recap after R0.60
R0.70A–R0.71R 完成版本 ||| Completed releases R0.70A–R0.71R
R0.71G–R0.71R · denominator faces、temporal packing、Jensen 与 incidence scale audit ||| R0.71G–R0.71R · denominator faces, temporal packing, Jensen, and incidence scale audit
R0.71O–P 依次恢复 soft quotient 的一侧 traces，并用 bounded overlap 与 \(\dot H^{-1}\) Lamb square sum 组成的一次 time-slice square-function estimate 吸收同刻 batch；R0.71Q 给出 finite conditional Jensen theorem，同时隔离 anchor、truncation、cover 与 H-envelope 四税。R0.71R 从 NSE 导出 localized observable 的 exact forced heat equation，并证明 finite conditional event-to-window theorem；统一 window lower height 与 essential same-observable overlap 明确保留为 hypotheses。\(\Gamma_\rho\) 是 upper comparison constant，\(1/\Gamma_\rho\) 编码 lower-charge strength。rho-dependent source ledger 显示：在 normalized zero-mean torus 上，rho=2 是最小 Leray-paid 指数；对 finite covariant event/window family，\(\Gamma_\rho^{\rm opt}\) 定义为 least admissible upper comparison constant，并在协变 integer/dyadic dilation 下按 lambda^rho 缩放。整数 Fourier 初始例只定义 first-jet surrogate Gamma_{2,jet}，不是 positive-time upper comparison constant 的下界。精确两阶判决只排除一参数 endpoint-square、termwise source-square certificate (3.3) 的无条件闭合，其他 Duhamel designs 与 signed / bilinear alternatives 保持开放。 ||| R0.71O–P successively recover one-sided traces of the soft quotient, and a single time-slice square-function estimate formed from bounded overlap and the \(\dot H^{-1}\) Lamb square sum absorbs the same-time batch. R0.71Q gives the finite conditional Jensen theorem while isolating the four anchor, truncation, cover, and H-envelope taxes. R0.71R derives the exact forced heat equation for the localized observable from NSE and proves a finite conditional event-to-window theorem; uniform window lower height and essential same-observable overlap are explicitly retained as hypotheses. \(\Gamma_\rho\) is an upper comparison constant, and \(1/\Gamma_\rho\) encodes lower-charge strength. The rho-dependent source ledger shows that rho=2 is the minimal Leray-paid exponent on the normalized zero-mean torus; for a finite covariant event/window family, \(\Gamma_\rho^{\rm opt}\) is defined as the least admissible upper comparison constant and scales as lambda^rho under covariant integer/dyadic dilation. The integer Fourier initial example defines only the first-jet surrogate Gamma_{2,jet}, not a lower bound for the positive-time upper comparison constant. The exact two-order verdict rules out only unconditional closure of the one-parameter endpoint-square, termwise source-square certificate (3.3); other Duhamel designs and signed / bilinear alternatives remain open.
R0.71R 把 certificate (3.3) 的一参数 endpoint-square、termwise source-square 缺口压成精确两阶：协变 integer/dyadic dilation 下的 optimal constant 按 lambda^rho 缩放，在 rho=0 不变，但 source ledger 要求 normalized \(L^2\)-Lamb 加 palinstrophy；Leray payment 的最小指数是 rho=2。initial jet 只给 Gamma_{2,jet} surrogate，不给 positive-time Gamma_2 下界。该方法判决不排除其他 Duhamel designs、signed、bilinear 或其他 scale-critical packet functional。 ||| R0.71R reduces the gap in the one-parameter endpoint-square, termwise source-square certificate (3.3) to an exact two-order mismatch: under covariant integer/dyadic dilation, the optimal constant scales as lambda^rho and is invariant at rho=0, but the source ledger requires normalized \(L^2\)-Lamb plus palinstrophy; the minimal exponent for Leray payment is rho=2. The initial jet gives only the Gamma_{2,jet} surrogate, not a positive-time lower bound for Gamma_2. This method verdict does not exclude other Duhamel designs or signed, bilinear, or other scale-critical packet functionals.
R0.71S 检查 signed / bilinear scale-critical packet ||| R0.71S examines a signed / bilinear scale-critical packet
保留 entry direction 与 signed pairing，检查能否绕开 certificate (3.3) 的两阶错配；候选必须通过 initial-jet、sequential 与 repeated-window 压力测试，且不能把 normalized L2-Lamb 与 palinstrophy 误称为 Serrin-equivalent budget。 ||| Retain entry direction and signed pairing and test whether the two-order mismatch in certificate (3.3) can be bypassed; a candidate must pass the initial-jet, sequential, and repeated-window stress tests and must not mislabel normalized L2-Lamb plus palinstrophy as a Serrin-equivalent budget.
保留 entry direction 与 signed pairing，检查是否存在 frame-summable、\(\dot H^{-1}\)-paid 且 scale-covariant 的 bilinear packet functional。 ||| Retain entry direction and signed pairing, and test whether a frame-summable, \(\dot H^{-1}\)-paid, scale-covariant bilinear packet functional exists.
保留 entry direction 与 signed pairing，检查是否有 frame-summable、由 \(\dot H^{-1}\) 支付且 scale-covariant 的 bilinear packet；不把 certificate (3.3) 的两阶损失隐藏进新范数。 ||| Retain entry direction and signed pairing, and test for a frame-summable, scale-covariant bilinear packet paid by \(\dot H^{-1}\); do not hide the two-order loss in certificate (3.3) inside a new norm.
本节只排除 certificate (3.3) 的一参数 endpoint-square、termwise source-square 无条件闭合；其他 Duhamel designs 保持开放。这里没有证明 uniform incidence、temporal packing、continuation、singularity 或 global regularity，也不排除 signed / bilinear scale-critical packet。 ||| This section rules out only unconditional closure of the one-parameter endpoint-square, termwise source-square certificate (3.3); other Duhamel designs remain open. It proves no uniform incidence, temporal packing, continuation, singularity, or global regularity result, and does not exclude a signed / bilinear scale-critical packet.
从有符号环带障碍走到 parabolic-incidence certificate boundary ||| From the signed-annulus obstruction to the parabolic-incidence certificate boundary
环带排除 → 源—核账本 → 协方差谱分层 → 全频条件桥 → response-slope 弦增益 → 共同响应阶一通道 → 恒定投影符号障碍 → 无权尺度打包障碍 → 带符号正输出系数 → 非负细化缺陷 → 黏性符号创造 → 物质热 tent 临界障碍 → projected-Lamb 热体积闭合 → 局部热打包 → 临界底边迹 → sign-only 驻留反例 → 相对超水平集 → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary ||| Annular exclusion → source–core ledger → covariance-spectrum stratification → full-frequency conditional bridge → response-slope chord gain → first-order common-response channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → critical material heat-tent obstruction → projected-Lamb heat-volume closure → localized heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary
静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–P 建立 projected-Lamb 热体积、局部化、denominator faces 与同刻 spatial batching。R0.71Q 给出 finite conditional Jensen theorem。R0.71R 再导出 exact forced heat equation 与 conditional incidence packing，并证明 certificate (3.3) 的一参数 endpoint-square、termwise source-square 方案在 rho=0 scale covariance 与 rho=2 minimal Leray payment 之间存在精确两阶错配。 ||| After the static annular family was rigorously excluded, the main line shifted to covariance-rank stratification and the full-frequency projection bridge. R0.71A–P establishes projected-Lamb heat volume, localization, denominator faces, and same-time spatial batching. R0.71Q gives a finite conditional Jensen theorem. R0.71R then derives the exact forced heat equation and conditional incidence packing, and proves that the one-parameter endpoint-square, termwise source-square scheme in certificate (3.3) has an exact two-order mismatch between rho=0 scale covariance and rho=2 minimal Leray payment.
累计回顾 R0.61–R0.71R · 2026-08-26 ||| Cumulative recap R0.61–R0.71R · 2026-08-26
目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71R 证明 finite conditional incidence theorem；在 rho=2 下，Leray energy 支付 source integral，frame constants 因 frame 固定而不依赖 finite truncation。完整右端仍可能因 upper comparison constant Gamma_2 与 essential overlap M 而不一致；theta_- 与 forward windows 是额外 theorem gates，不是右端因子。协变 optimal constant 的 rho=0 与 minimal Leray payment 的 rho=2 只构成 certificate (3.3) 的精确两阶边界。 ||| There is currently no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71R proves a finite conditional incidence theorem; at rho=2, Leray energy pays the source integral, while the frame constants are independent of finite truncation because the frame is fixed. The full right-hand side may still be nonuniform because of the upper comparison constant Gamma_2 and essential overlap M; theta_- and the forward windows are additional theorem gates, not right-hand-side factors. The mismatch between rho=0 for the covariant optimal constant and rho=2 for minimal Leray payment forms an exact two-order boundary only for certificate (3.3).
上次综述 v1.02 · 2026-08-26 ||| Previous review v1.02 · 2026-08-26
我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71R 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。 ||| I also prepared a separate systematic review that places classical theory, five main strands of the literature, the candidate-elimination tree, progress from 2019—2026, and this site's R0.69P–R0.71R route in one diagram. The historical nodes R0.61–R0.69O remain in the cumulative recap.
下一步 R0.71S： ||| Next step, R0.71S:
下载同步研究笔记 PDF ||| Download synchronized research-note PDF
研究笔记 R0.71R · 2026-08-26 ||| Research note R0.71R · 2026-08-26
有限 incidence theorem 成立，certificate (3.3) 留下精确两阶错配 ||| The finite incidence theorem holds; certificate (3.3) leaves an exact two-order mismatch
阅读 R0.71R 研究笔记 → ||| Read research note R0.71R →
展开 52 篇公开笔记 ||| Expand 52 public notes
综述 v1.03 · 2026-08-26 ||| Review v1.03 · 2026-08-26
exact forced heat equation 与 finite conditional incidence theorem 成立；certificate (3.3) 的一参数 endpoint-square、termwise source-square 方案无法同时满足 rho=0 scale covariance 与 rho=2 minimal Leray payment，其他 Duhamel designs 保持开放。 ||| The exact forced heat equation and finite conditional incidence theorem hold; the one-parameter endpoint-square, termwise source-square scheme in certificate (3.3) cannot simultaneously satisfy rho=0 scale covariance and rho=2 minimal Leray payment, while other Duhamel designs remain open.
integer-compatible torus initial data、covariant radial multiplier 与 cutoff 给出 exact Fourier first jet。它只定义 \(\Gamma_{2,\mathrm{jet}}:=A_+/(K^{-2}\|hC_t(0)\|_2^2/Y(0))=K^2/(4\theta^2)\)；这是 leading surrogate，不是 positive-time certificate (3.3) 的 upper comparison constant \(\Gamma_2\) 下界。even-touch、sequential 与 component-union families 只是 forced scalar method tests，不是 NSE trajectories。 ||| Integer-compatible torus initial data, a covariant radial multiplier, and the cutoff give an exact Fourier first jet. It defines only \(\Gamma_{2,\mathrm{jet}}:=A_+/(K^{-2}\|hC_t(0)\|_2^2/Y(0))=K^2/(4\theta^2)\); this is a leading surrogate and, in the positive-time certificate (3.3), not a lower bound for the upper comparison constant \(\Gamma_2\). The even-touch, sequential, and component-union families are only forced-scalar method tests, not NSE trajectories.
localized filtered-vorticity observable 满足 \[ C_{j,Q,t}-\nu\Delta C_{j,Q}=G_{j,Q}. \] 对显式 forward height、post-entry upper comparison constant \(\Gamma_\rho\) 与 same-observable overlap，Duhamel 给出 finite conditional event-to-window packing theorem；\(1/\Gamma_\rho\) 编码 lower-charge strength。窗口假设包括 \(0<\theta_-\le\theta_\beta\le\theta_*\) 的统一正下界；\(M\) 取 essential supremum。统一 \(\theta_-\) 与 forward-window availability 是 theorem gates，不是右端因子；缺少正下界时可以任意缩短窗口而平凡化 overlap。 ||| The localized filtered-vorticity observable satisfies \[ C_{j,Q,t}-\nu\Delta C_{j,Q}=G_{j,Q}. \] For an explicit forward height, a post-entry upper comparison constant \(\Gamma_\rho\), and same-observable overlap, Duhamel gives a finite conditional event-to-window packing theorem; \(1/\Gamma_\rho\) encodes lower-charge strength. The window hypothesis includes the uniform positive lower bound \(0<\theta_-\le\theta_\beta\le\theta_*\); \(M\) is an essential supremum. Uniform \(\theta_-\) and forward-window availability are theorem gates, not right-hand-side factors; without the positive lower bound, windows can be shortened arbitrarily and the overlap condition trivialized.
R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen 与 parabolic-incidence scale audit。R0.70A–R0.71R 共 44 个完成版本。 ||| The route after R0.60 has twelve segments: reduced Picard iteration and the shear boundary, transverse perturbations, localized pressure budgets, signed physical annuli, moving labels and source–core duality, deviatoric tensors and finite observations, full-frame covariance, the constant-projection boundary, positive output and the material heat tent, projected-Lamb heat volume, localized heat packing and the critical-trace obstruction, and positive-entry temporal packing, conditional Jensen, and the parabolic-incidence scale audit. R0.70A–R0.71R contains 44 completed releases.
R0.60 recap 之后的累计回顾收录 82 个节点；全站现有 142 篇公开研究笔记 ||| The cumulative recap after the R0.60 recap contains 82 nodes; the site now has 142 public research notes
R0.71R 已完成： ||| R0.71R completed:
rho-dependent source ledger 表明，在 normalized zero-mean torus 上，\(\rho=2\) 是最小 Leray-paid 指数：Leray energy 支付 source integral，frame constants 则由固定 frame 给定；完整右端仍可能因 \(\Gamma_2\) 与 \(M\) 而不一致。对对应 finite covariant event/window family，\(\Gamma_\rho^{\rm opt}\) 定义为 least admissible upper comparison constant；固定 torus 的 compatible integer/dyadic dilation 必须协变搬运 multiplier、cutoff、event 与 window，此时只有 \(\Gamma_\rho^{\rm opt}\) 按 \(\lambda^\rho\) 缩放，并在 \(\rho=0\) 不变。\(\rho=0\) 需要的精确 normalized budget 是 \(\|L\|_2^2/Y+\nu^2\|\nabla\omega\|_2^2/Y\)；这里不声称它等价于 Serrin norm。 ||| The rho-dependent source ledger shows that, on the normalized zero-mean torus, \(\rho=2\) is the minimal Leray-paid exponent: Leray energy pays the source integral, while the frame constants are supplied by the fixed frame; the full right-hand side may still be nonuniform because of \(\Gamma_2\) and \(M\). For the corresponding finite covariant event/window family, \(\Gamma_\rho^{\rm opt}\) is defined as the least admissible upper comparison constant. A compatible integer/dyadic dilation on the fixed torus must transport the multiplier, cutoff, event, and window covariantly; only \(\Gamma_\rho^{\rm opt}\) scales as \(\lambda^\rho\), and it is invariant at \(\rho=0\). At \(\rho=0\), the exact normalized budget required is \(\|L\|_2^2/Y+\nu^2\|\nabla\omega\|_2^2/Y\); no equivalence to a Serrin norm is claimed.
保留 entry direction 与 signed pairing，检查能否绕开 certificate (3.3) 的两阶错配；其他 Duhamel designs 保持开放。 ||| Retain entry direction and signed pairing and test whether the two-order mismatch in certificate (3.3) can be bypassed; other Duhamel designs remain open.
打开 82 节完整索引 ||| Open the complete 82-section index
给 parabolic square-Carleson upper norm； ||| provides a parabolic square-Carleson upper norm;
的一维标量齐次 spatial zero-number law 还要求 uniform parabolicity、coefficient regularity、相应 boundary hypotheses 与 positive time。两者都不直接控制三维 Hilbert-valued forced observable 的 temporal entries。两轮限定检索未找到 uniform R0.71R incidence / overlap theorem；这是 bounded negative finding，不是原创性、优先权或不存在性结论。 ||| 's one-dimensional scalar homogeneous spatial zero-number law also requires uniform parabolicity, coefficient regularity, the corresponding boundary hypotheses, and positive time. Neither result directly controls temporal entries of a three-dimensional Hilbert-valued forced observable. Two scoped searches found no uniform R0.71R incidence / overlap theorem; this is a bounded negative finding, not a claim of originality, priority, or nonexistence.
开放接口 · R0.71S ||| Open interface · R0.71S
累计回顾与 82 节索引 ||| Cumulative recap and 82-section index
为 singularity / regularity cylinders 给 local-energy gate，不给 smooth filtered entry 的 lower charge。 ||| provide a local-energy gate for singularity / regularity cylinders, but not a lower charge for a smooth filtered entry.
文献综述 v1.03 · 2026-08-26 ||| Literature review v1.03 · 2026-08-26
我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.71R 只列为研究笔记。我不把计算或笔记外推成正则性定理。 ||| I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.71R only as research notes. I do not extrapolate computations or notes into regularity theorems.
中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q 隔离 analytic/Jensen 四税；R0.71R 再证明 finite conditional parabolic-incidence theorem，并为 certificate (3.3) 定位 rho=0 scale covariance 与 rho=2 minimal Leray payment 的两阶错配。保留下来的结果都不是全局正则性结论。 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary, R0.71Q isolates the four analytic/Jensen taxes, and R0.71R then proves a finite conditional parabolic-incidence theorem and, for certificate (3.3), locates the two-order mismatch between rho=0 scale covariance and rho=2 minimal Leray payment. None of the retained results is a global regularity conclusion.
certificate (3.3) 有精确两阶错配 ||| Certificate (3.3) has an exact two-order mismatch
exact forced heat equation 与 finite conditional incidence theorem 成立。normalized zero-mean torus 上 rho=2 是 minimal Leray-paid index；对 finite covariant event/window family 定义的 least admissible optimal upper comparison constant 在协变 integer/dyadic dilation 下按 lambda^rho 缩放。initial Fourier example 只定义 Gamma_{2,jet} surrogate，不给 positive-time upper comparison constant Gamma_2 下界。 ||| The exact forced heat equation and finite conditional incidence theorem hold. On the normalized zero-mean torus, rho=2 is the minimal Leray-paid exponent; the least admissible optimal upper comparison constant defined for a finite covariant event/window family scales as lambda^rho under covariant integer/dyadic dilation. The initial Fourier example defines only the Gamma_{2,jet} surrogate and gives no lower bound for the positive-time upper comparison constant Gamma_2.
R0.71R 从 localized observable 的 exact forced heat equation 出发，证明 finite conditional packing theorem。uniform 0<theta_-<=theta_beta<=theta_* 与 forward-window availability 是 theorem gates，不是右端因子；Gamma_rho 是 upper comparison constant，1/Gamma_rho 编码 lower-charge strength，M 是 essential same-observable overlap。rho=2 是 normalized zero-mean torus 上的 minimal Leray-paid index：Leray energy 支付 source integral，frame constants 由固定 frame 给定；完整右端仍可能因 Gamma_2 与 M 而不一致。对对应 finite covariant event/window family，Gamma_rho^opt 定义为 least admissible upper comparison constant；固定 torus 上 compatible integer/dyadic dilation 必须协变搬运 multiplier、cutoff、event 与 window，且只有 Gamma_rho^opt 按 lambda^rho 缩放。整数 Fourier example 只定义 Gamma_{2,jet}=K^2/(4 theta^2) surrogate，不给 positive-time upper comparison constant Gamma_2 下界。certificate (3.3) 以外的 Duhamel designs 保持开放；R0.71S 只检查 signed / bilinear scale-critical packet。我继续用下面六条筛选。 ||| Starting from the exact forced heat equation for the localized observable, R0.71R proves a finite conditional packing theorem. Uniform 0<theta_-<=theta_beta<=theta_* and forward-window availability are theorem gates, not right-hand-side factors; Gamma_rho is an upper comparison constant, 1/Gamma_rho encodes lower-charge strength, and M is essential same-observable overlap. On the normalized zero-mean torus, rho=2 is the minimal Leray-paid exponent: Leray energy pays the source integral, while the frame constants are supplied by the fixed frame; the full right-hand side may still be nonuniform because of Gamma_2 and M. For the corresponding finite covariant event/window family, Gamma_rho^opt is defined as the least admissible upper comparison constant. A compatible integer/dyadic dilation on the fixed torus must transport the multiplier, cutoff, event, and window covariantly, and only Gamma_rho^opt scales as lambda^rho. The integer Fourier example defines only the Gamma_{2,jet}=K^2/(4 theta^2) surrogate and gives no lower bound for the positive-time upper comparison constant Gamma_2. Duhamel designs outside certificate (3.3) remain open; R0.71S examines only a signed / bilinear scale-critical packet. I continue to apply the following six filters.
R0.71R 的一手文献边界 ||| Primary-source boundary for R0.71R
R0.71R 关闭了什么，R0.71S 只检查什么 ||| What R0.71R closes, and what R0.71S alone examines
\(\Gamma_{2,\mathrm{jet}}\) 只是用 \(hC_t(0)\) 替代真实 endpoint 后得到的 leading surrogate，不是 positive-time certificate (3.3) 的 \(\Gamma_2\) 下界。证书没有进行 exact positive-time NSE integration，也不把小数据全局光滑性外推成同一常数在固定正时间窗上的精确公式。 ||| \(\Gamma_{2,\mathrm{jet}}\) is only a leading surrogate obtained by replacing the actual endpoint with \(hC_t(0)\), not, for the positive-time certificate (3.3), a lower bound for \(\Gamma_2\). The certificate performs no exact positive-time NSE integration and does not extrapolate small-data global smoothness into an exact formula for the same constant on fixed positive-time windows.
01 · R0.71P–Q 接口 ||| 01 · R0.71P–Q interface
02 · 强迫热方程 ||| 02 · Forced heat equation
03 · 条件打包定理 ||| 03 · Conditional packing theorem
04 · 一参数源账本 ||| 04 · One-parameter source ledger
05 · 两阶尺度错配 ||| 05 · Two-order scale mismatch
06 · NSE 初始 jet ||| 06 · NSE initial jet
07 · 方法反例族 ||| 07 · Method counterexample families
08 · 文献边界 ||| 08 · Literature boundary
14 · 复现 ||| 14 · Reproduce
版本 v0.71R · 2026-08-26 ||| Version v0.71R · 2026-08-26
保持 \(A_+=1\)，而 post-entry amplitude 与 \(\int|G_\varepsilon|^2\) 都按 \(\varepsilon^2\) 缩小。正 observable scaling 不改变 entry atom，却缩小所有 quadratic charges。 ||| Keep \(A_+=1\), while the post-entry amplitude and \(\int|G_\varepsilon|^2\) both shrink as \(\varepsilon^2\). Positive observable scaling leaves the entry atom unchanged but reduces all quadratic charges.
报告、主张矩阵、证书、图数据和独立 checker 全部保留 ||| The report, claim matrix, certificate, figure data, and independent checker are all retained.
并设 \(Y_\beta^*=\sup_{I_\beta}Y\)。统一 \(\theta_-\) 正下界是 theorem hypothesis，不是从 NSE 推出的结论；缺少它时可以把 windows 任意缩短，从而把 overlap 条件平凡化。post-entry incidence certificate 为 ||| Set \(Y_\beta^*=\sup_{I_\beta}Y\). The uniform positive lower bound \(\theta_-\) is a theorem hypothesis, not a conclusion derived from NSE; without it, the windows can be shortened arbitrarily, thereby trivializing the overlap condition. The post-entry incidence certificate is
尺度错配 ||| Scale mismatch
初始 jet ||| Initial jet
初始迹边界 ||| Initial-trace boundary
除以 \(Y\) 后，\(\|L\|_{\dot H^{-1}}^2/Y\lesssim\|u\|_2Y^{1/2}\)，所以 Leray energy 支付有限时间区间上的 source integral，frame constants 则因 frame 固定而与 finite truncation 无关。完整 theorem 右端仍可能因 \(\Gamma_2\) 与 \(M\) 而不一致；统一 \(\theta_-\) 与 forward-window availability 是额外 theorem gates，也仍未证明，但不是右端因子。 ||| After dividing by \(Y\), \(\|L\|_{\dot H^{-1}}^2/Y\lesssim\|u\|_2Y^{1/2}\), so Leray energy pays the source integral over a finite time interval, while the frame constants are independent of finite truncation because the frame is fixed. The full theorem right-hand side may still be nonuniform because of \(\Gamma_2\) and \(M\); uniform \(\theta_-\) and forward-window availability are additional theorem gates that also remain unproved, not right-hand-side factors.
除以 \(Y\) 后，所需的精确 normalized budget 是 \(\|L\|_2^2/Y+\nu^2\|\nabla\omega\|_2^2/Y\)。这里不声称它等价于任何 Serrin norm，也不声称 Leray energy 支付该量。certificate (3.3) 的 termwise source-square interpolation 因而满足精确方法判决： ||| After dividing by \(Y\), the exact normalized budget required is \(\|L\|_2^2/Y+\nu^2\|\nabla\omega\|_2^2/Y\). No equivalence to any Serrin norm is claimed here, nor is it claimed that Leray energy pays for this quantity. The termwise source-square interpolation in certificate (3.3) therefore satisfies the exact method verdict:
但当前 endpoint-square certificate 留下精确两阶错配 ||| But the current endpoint-square certificate leaves an exact two-order mismatch
的 backward uniqueness 要求 closed parabolic inequality 与完整场消失。 ||| Backward uniqueness requires a closed parabolic inequality and vanishing of the full field.
的 zero-number theorem 使用一维标量齐次 Sturm order，并要求 uniform parabolicity、coefficient regularity、相应 boundary hypotheses 与 positive time；不能直接移植到三维 Hilbert-valued forced observable。 ||| 's zero-number theorem uses one-dimensional scalar homogeneous Sturm order and requires uniform parabolicity, coefficient regularity, the corresponding boundary hypotheses, and positive time; it cannot be transferred directly to a three-dimensional Hilbert-valued forced observable.
定义 essential overlap ||| Define essential overlap
对 \(h=\theta K^{-2}\)，只定义 first-jet surrogate ||| For \(h=\theta K^{-2}\), only the first-jet surrogate is defined
对固定、尺度协变、三阶导数平方重叠有界的 cutoff frame，精确 product expansion 给出 ||| For a fixed, scale-covariant cutoff frame with bounded overlap of squared third derivatives, the exact product expansion gives
对每个 positive entry 假设存在 ||| For each positive entry, assume there exists
反例族 ||| Counterexample families
方法边界： ||| Method boundary:
附图把条件正结果、尺度错配与方法反例分开显示 ||| The accompanying figure displays the conditional positive result, scale mismatch, and method counterexamples separately.
该结论只分类一参数 endpoint-square、termwise source-square certificate (3.3)。它不排除其他 Duhamel designs，也不排除在 componentwise positive parts 之前保留 signed direction 的 bilinear or oscillatory packet。 ||| This conclusion only classifies the one-parameter endpoint-square, termwise source-square certificate (3.3). It does not rule out other Duhamel designs, nor a bilinear or oscillatory packet that preserves signed direction before taking componentwise positive parts.
该判决只针对 certificate (3.3) 及其 termwise source-square payment，不关闭其他 Duhamel designs。它不排除保留方向与符号的 bilinear packet，也不证明 uniform NSE temporal packing、继续性判据或全局正则性。 ||| This verdict only concerns certificate (3.3) and its termwise source-square payment; it does not close other Duhamel designs. It does not rule out a bilinear packet retaining direction and sign, nor does it prove uniform NSE temporal packing, a continuation criterion, or global regularity.
给出真正的 parabolic square-Carleson upper norm，但没有 entry-to-tent lower implication。 ||| Provides a genuine parabolic square-Carleson upper norm but no entry-to-tent lower implication.
对给定 finite covariant event/window family \(\mathcal E\)，定义 \(\Gamma_\rho^{\rm opt}[u,\mathcal E]\) 为 certificate (3.3) 中最小的 admissible upper comparison constant。固定 torus 只沿保持 Fourier lattice 的 integer/dyadic \(\lambda\) 比较，并把 solution、annular multiplier、cutoff、event 与 forward window 一起协变搬运。此时 \(A_{\beta,+}\) 与 \(\|C\|_2^2/Y\) 都获得 \(\lambda^2\)，而 \(\kappa_j^{-\rho}\) 获得 \(\lambda^{-\rho}\)。因此 ||| For a given finite covariant event/window family \(\mathcal E\), define \(\Gamma_\rho^{\rm opt}[u,\mathcal E]\) as the least admissible upper comparison constant in certificate (3.3). On the fixed torus, comparisons are made only along integer/dyadic \(\lambda\) preserving the Fourier lattice, while the solution, annular multiplier, cutoff, event, and forward window are transported covariantly together. Then \(A_{\beta,+}\) and \(\|C\|_2^2/Y\) both acquire \(\lambda^2\), while \(\kappa_j^{-\rho}\) acquires \(\lambda^{-\rho}\). Therefore
候选必须通过 integer-torus initial jet、sequential recurrence 与 repeated-window pressure tests。若 localization 迫使符号消失，或预算退回 \(L^2\)-Lamb / palinstrophy，我会把条件原样保留并停止该分支。 ||| Candidates must pass the integer-torus initial-jet, sequential-recurrence, and repeated-window pressure tests. If localization forces the sign to disappear, or the budget falls back to \(L^2\)-Lamb / palinstrophy, I will retain the conditions exactly as they are and stop that branch.
价值在于把开放问题压缩成两个动力学证书 ||| Its value lies in compressing the open problem into two dynamical certificates
截至 2026-08-26 的两轮限定一手文献检索，没有发现直接给出 R0.71R incidence certificate 或 same-observable overlap bound 的定理。这是 bounded negative finding，不是不存在性、原创性或优先权声明。 ||| As of 2026-08-26, two rounds of restricted primary-literature searches found no theorem directly providing the R0.71R incidence certificate or same-observable overlap bound. This is a bounded negative finding, not a claim of nonexistence, originality, or priority.
精确强迫热方程、有限条件 incidence packing、rho=2 的 Leray 支付、rho=0 的尺度协变、初始 first-jet 压力测试与方法边界。 ||| Exact forced heat equation, finite conditional incidence packing, Leray payment at rho=2, scale covariance at rho=0, initial first-jet pressure test, and method boundary.
精确强迫热方程与 Duhamel 上界给出 finite conditional packing theorem。对一参数 endpoint-square、termwise source-square certificate (3.3)，\(\rho=2\) 是使 nonlinear source 与 viscous commutator 同时进入 Leray 预算的最小指数；协变整数／二进伸缩下的 optimal upper comparison constant 只有在 \(\rho=0\) 才不改变尺度。不存在一个 \(\rho\) 同时满足这两个要求。 ||| The exact forced heat equation and the Duhamel upper bound yield a finite conditional packing theorem. For the one-parameter endpoint-square, termwise source-square certificate (3.3), \(\rho=2\) is the smallest exponent that brings both the nonlinear source and the viscous commutator into the Leray budget; under covariant integer/dyadic dilations, the optimal upper comparison constant is scale-invariant only at \(\rho=0\). No single \(\rho\) satisfies both requirements.
精确证书与独立重建分别通过 ||| The exact certificate and independent reconstruction passed separately
局部 filtered-vorticity observable 满足精确强迫热方程 ||| The local filtered-vorticity observable satisfies an exact forced heat equation
强迫方程 ||| Forced equation
取 \(K\in\mathbb N\) 和归一化周期环面初值 ||| Take \(K\in\mathbb N\) and normalized periodic-torus initial data
若 \(M<\infty\) 且对 finite truncation 一致，则 ||| If \(M<\infty\) uniformly over finite truncations, then
使用随 \(K\) 共变的 smooth radial multiplier \(m_K(\xi)=m(|\xi|/K)\)，其中 \(m(1)=0\)、\(m(\sqrt2)=1\)，并取周期兼容 cutoff \(\chi\equiv1\)。所有参与模态都在整数 Fourier lattice 上；multiplier 与 cutoff 不随物理解额外引入非共变尺度。 ||| Use \(K\) to covariantly rescale the smooth radial multiplier \(m_K(\xi)=m(|\xi|/K)\), where \(m(1)=0\), \(m(\sqrt2)=1\), and take the periodic-compatible cutoff \(\chi\equiv1\). All participating modes lie on the integer Fourier lattice; the multiplier and cutoff introduce no additional noncovariant scale depending on the physical solution.
同刻 shell–cell batch 已由 bounded cutoff overlap 与 \(\dot H^{-1}\) Lamb square sum 组成的一次 time-slice square-function estimate 吸收。R0.71Q 又证明 analytic radius、complex upper bound 与相对 Jensen 数据不产生所需的 absolute event charge。本节改为检查 NSE 方程是否把每个原子转换成 forward source packet。 ||| A single time-slice square-function estimate formed from bounded cutoff overlap and the \(\dot H^{-1}\) Lamb square sum has absorbed the same-time shell–cell batch. R0.71Q also proved that analytic radius, a complex upper bound, and relative Jensen data do not produce the required absolute event charge. This section instead checks whether the NSE equation converts each atom into a forward source packet.
图 R0.71R。A：rho-dependent source ledger；协变 optimal upper comparison constant 在 rho=0 不变，Leray payment 的最小指数为 rho=2。B：整数频率 NSE initial Fourier jet 只定义 first-jet surrogate Gamma_{2,jet}，该 surrogate 按 K^2 增长；它不是 positive-time upper comparison constant 的下界。C：forced scalar even touch 保持 A_+=1，而 quadratic charge 按 epsilon^2 缩小。D：sequential 与 component-union families 在有界 source-square mass 下增长 entry mass。B 不是正时间积分，C–D 不是 NSE trajectories。 ||| Figure R0.71R. A: rho-dependent source ledger; the covariant optimal upper comparison constant is invariant at rho=0, while the minimal Leray-paid exponent is rho=2. B: the integer-frequency NSE initial Fourier jet only defines the first-jet surrogate Gamma_{2,jet}; this surrogate grows as K^2 and is not a lower bound for the positive-time upper comparison constant. C: the forced-scalar even touch keeps A_+=1, while the quadratic charge shrinks as epsilon^2. D: sequential and component-union families have growing entry mass under bounded source-square mass. B is not a positive-time integration, and C–D are not NSE trajectories.
为 singular cylinders 或 regular epochs 提供 local-energy gate，不把 smooth filtered zero 变成下质量。 ||| Provides a local-energy gate for singular cylinders or regular epochs, but does not turn a smooth filtered zero into lower mass.
无 PDE 正时间推进 ||| No positive-time PDE evolution
下一对象：signed / bilinear critical packet ||| Next object: signed / bilinear critical packet
下一节保留 entry direction \(e_\beta=c_\beta/\|c_\beta\|_2\) 与 signed pairing \(\langle F_j,e_\beta\rangle\)，检查是否存在 frame-summable、由 \(\dot H^{-1}\) 支付且不丢失两阶的 scale-covariant packet functional。 ||| The next section retains the entry direction \(e_\beta=c_\beta/\|c_\beta\|_2\) and signed pairing \(\langle F_j,e_\beta\rangle\), and checks whether there exists a frame-summable, \(\dot H^{-1}\)-paid, scale-covariant packet functional without the two-order loss.
显式 forward height 与同观测量 overlap 给出有限条件打包 ||| Explicit forward height and same-observable overlap yield finite conditional packing
限制到 owned windows 完全包含于子区间 \(J\) 时，同一证明给出 source-relative Carleson form。除非另有 local source estimate，它不是 classical \(|J|\)-Carleson bound。 ||| Restricting to owned windows fully contained in a subinterval \(J\), the same proof yields a source-relative Carleson form. Unless an additional local source estimate is available, it is not a classical \(|J|\)-Carleson bound.
相容。此时源账本却要求 ||| Compatible. The source ledger, however, requires
协变 optimal constant 在 \(\rho=0\) 不变，与最小 Leray-paid 指数相差两阶 ||| The covariant optimal constant is invariant at \(\rho=0\), two orders apart from the minimal Leray-paid exponent
研究笔记 R0.71R · PARABOLIC INCIDENCE · SCALE AUDIT ||| Research note R0.71R · PARABOLIC INCIDENCE · SCALE AUDIT
研究笔记 R0.71R：局部观测量满足精确强迫热方程，有限条件 incidence theorem 把时间进入打包归约到两个动力学账本；一参数 endpoint-square、termwise source-square certificate 在尺度协变与 Leray 支付之间存在精确两阶错配。 ||| Research note R0.71R: the local observable satisfies an exact forced heat equation, and the finite conditional incidence theorem reduces temporal-entry packing to two dynamical ledgers; the one-parameter endpoint-square, termwise source-square certificate has an exact two-order mismatch between scale covariance and Leray payment.
已有 parabolic budgets 没有给 filtered entry 的统一 lower charge ||| Existing parabolic budgets do not provide a uniform lower charge for filtered entries
有限条件 incidence theorem 可以成立， ||| A finite conditional incidence theorem can hold,
源账本 ||| Source ledger
在 entry time \(C_\alpha(t_\beta)=0\) 处，heat-semigroup contraction 与 Cauchy–Schwarz 只给上端估计 ||| At the entry time \(C_\alpha(t_\beta)=0\), heat-semigroup contraction and Cauchy–Schwarz provide only the upper endpoint estimate
在额外 coherence、scale separation 与 modulation 条件下控制 signed cover-averaged flux；它不是逐 entry atom 的 lower packet。 ||| Controls signed cover-averaged flux under additional coherence, scale-separation, and modulation conditions; it is not a lower packet for each entry atom.
在归一化 zero-mean torus 上，\(\rho=2\) 是同时把 nonlinear term 降到 \(\dot H^{-1}\) Lamb budget、把 commutator 降到 enstrophy budget 的最小指数： ||| On the normalized zero-mean torus, \(\rho=2\) is the smallest exponent that simultaneously lowers the nonlinear term to the \(\dot H^{-1}\) Lamb budget and the commutator to the enstrophy budget:
在归一化周期环面上，固定 smooth annular multiplier \(T_j\) 与尺度匹配 cutoff frame \(\chi_Q\)，令 ||| On the normalized periodic torus, fix a smooth annular multiplier \(T_j\) and a scale-matched cutoff frame \(\chi_Q\), and let
在这条协变 dilation family 上，scale-independent optimal constant 只与 ||| Along this covariant dilation family, a scale-independent optimal constant occurs only for
这是 upper endpoint estimate，不是 event lower charge；不能把不等号反向使用。 ||| This is an upper endpoint estimate, not an event lower charge; the inequality cannot be used in reverse.
这些是 abstract forced scalar method tests，不是 NSE repeated-entry trajectories。它们只证明 smoothness、analyticity、semigroup upper bounds 与 source-square upper budgets 本身不推出 event lower charge。 ||| These are abstract forced-scalar method tests, not NSE repeated-entry trajectories. They only prove that smoothness, analyticity, semigroup upper bounds, and source-square upper budgets alone do not imply an event lower charge.
整数频率环面初始 jet 的 surrogate \(\Gamma_{2,\mathrm{jet}}\) 按 \(K^2\) 增长 ||| The surrogate \(\Gamma_{2,\mathrm{jet}}\) from the integer-frequency torus initial jet grows as \(K^2\)
只排除 certificate (3.3) 的一参数 endpoint-square、termwise source-square 无条件闭合，不排除其他 Duhamel designs、signed、bilinear 或其他 scale-critical NSE functional。 ||| Only the unconditional closure of the one-parameter endpoint-square, termwise source-square certificate (3.3) is ruled out; other Duhamel designs and signed, bilinear, or other scale-critical NSE functionals are not ruled out.
状态 · R0.71R 有限条件定理与尺度审计完成 ||| Status · R0.71R finite conditional theorem and scale audit completed
cutoff 与 annular derivative powers 决定最小 Leray-paid 指数 ||| Cutoff and annular derivative powers determine the minimal Leray-paid exponent
degree-zero entry atoms 不由 quadratic upper charges 自动支付 ||| Degree-zero entry atoms are not automatically paid for by quadratic upper charges
even-touch、sequential 与 component-union families 是 forced scalar paths，不是 Navier–Stokes trajectories。 ||| The even-touch, sequential, and component-union families are forced-scalar paths, not Navier–Stokes trajectories.
exact localized forced heat equation；Duhamel upper estimate；finite conditional incidence packing；rho-dependent source ledger；rho=2 的有限时间 Leray payment；rho=0 的 scale-covariance verdict；exact initial first-jet 与 abstract method obstructions。 ||| exact localized forced heat equation; Duhamel upper estimate; finite conditional incidence packing; rho-dependent source ledger; finite-time Leray payment at rho=2; scale-covariance verdict at rho=0; exact initial first jet and abstract method obstructions.
exact producer 验证 rho-dependent derivative ledger、scaled NSE initial Fourier jet、even-touch homogeneity、sequential polynomial 与 component-union families。independent checker 另行重建 Duhamel ratio、scaling powers、first-jet coefficients、polynomial energies 与 figure data；两者都不进行 PDE time stepping。 ||| The exact producer verifies the rho-dependent derivative ledger, scaled NSE initial Fourier jet, even-touch homogeneity, sequential polynomial, and component-union families. The independent checker separately reconstructs the Duhamel ratio, scaling powers, first-jet coefficients, polynomial energies, and figure data; neither performs PDE time stepping.
finite conditional theorem 保留 event-to-window upper comparison constant \(\Gamma_\rho\)、统一 window lower height \(\theta_-\) 与 essential same-observable overlap \(M\)，其中 \(1/\Gamma_\rho\) 才编码 lower-charge strength。\(\rho=2\) 时 Leray energy 支付 source integral，frame constants 由固定 frame 给定；协变 dilation 下的 optimal constant 缩放则精确记录两阶损失。initial jet 只提供与该缩放相容的 surrogate，不提供 positive-time lower bound。 ||| The finite conditional theorem retains the event-to-window upper comparison constant \(\Gamma_\rho\), uniform window lower height \(\theta_-\), and essential same-observable overlap \(M\), with \(1/\Gamma_\rho\) encoding lower-charge strength. At \(\rho=2\), Leray energy pays the source integral, while the frame constants are supplied by the fixed frame; scaling of the optimal constant under covariant dilation precisely records the two-order loss. The initial jet provides only a surrogate compatible with that scaling, not a positive-time lower bound.
R0.71P 的目标是不同进入时刻上的原子和 ||| The target of R0.71P is the sum of atoms over distinct entry times
R0.71P 留下 distinct positive-entry times，R0.71Q 证明抽象解析性不支付完整计数。本节从 NSE 方程导出 localized observable 的精确强迫热方程，并证明 finite conditional event-to-window packing theorem。结果把无条件闭合压到 upper comparison constant 与 same-observable window overlap 两个动力学账本；在一参数 endpoint-square、termwise source-square certificate (3.3) 中，协变最优常数的缩放选择 \(\rho=0\)，最小的 Leray-paid 指数却是 \(\rho=2\)。 ||| R0.71P left distinct positive-entry times unresolved, and R0.71Q proved that abstract analyticity does not pay for the full count. This section derives the exact forced heat equation for the localized observable from the NSE equation and proves a finite conditional event-to-window packing theorem. The result reduces unconditional closure to two dynamical ledgers: the upper comparison constant and same-observable window overlap; in the one-parameter endpoint-square, termwise source-square certificate (3.3), scaling of the covariant optimal constant selects \(\rho=0\), whereas the minimal Leray-paid exponent is \(\rho=2\).
R0.71R · 2026-08-26 · 个人数学研究日志 ||| R0.71R · 2026-08-26 · Personal mathematics research log
R0.71R 二次抛物 incidence 条件定理、尺度错配、NSE 初始 jet 与方法反例审计 ||| R0.71R quadratic parabolic-incidence conditional theorem, scale mismatch, NSE initial jet, and method-counterexample audit
R0.71R｜endpoint-square incidence certificate 的精确两阶错配 ||| R0.71R | exact two-order mismatch of the endpoint-square incidence certificate
R0.71S 转向 signed / bilinear scale-critical packet ||| R0.71S turns to a signed / bilinear scale-critical packet
sequential family \(C_N=\varepsilon_N\prod_{k=1}^N(t-k/(N+1))^2\) 可归一化到 \(\int_0^1|G_N|^2dt=1\)，同时保留 \(N\) 个质量为一的 positive entries。component family \(C_q=2^{-q}(t-b_q)^2\) 则使 all-component source square 小于 \(3\)，而 entry union 为 \(Q\)。 ||| The sequential family \(C_N=\varepsilon_N\prod_{k=1}^N(t-k/(N+1))^2\) can be normalized to \(\int_0^1|G_N|^2dt=1\) while retaining \(N\) positive entries of unit mass. The component family \(C_q=2^{-q}(t-b_q)^2\) makes the all-component source square less than \(3\), while the entry union equals \(Q\).
source integral 可由能量支付，event lower charge 与时间 overlap 仍未推出 ||| The source integral can be paid for by energy, but the event lower charge and temporal overlap remain unproved
uniform NSE upper comparison constant、uniform forward-window overlap、endpoint noncollapse、infinite-frame temporal packing、Leray-limit passage、continuation criterion、finite-time singularity 或 global regularity。 ||| uniform NSE upper comparison constant, uniform forward-window overlap, endpoint noncollapse, infinite-frame temporal packing, Leray-limit passage, continuation criterion, finite-time singularity, or global regularity.
bounded support overlap 与 \(\dot H^{-1}\) Lamb square sum 组成的一次 time-slice square-function estimate 吸收同刻 batch，完整目标归约到 distinct entry-time counting measure。 ||| A single time-slice square-function estimate formed from bounded support overlap and the \(\dot H^{-1}\) Lamb square sum absorbs the same-time batch, reducing the full target to the distinct entry-time counting measure.
这里 \(\Gamma_\rho\) 是 upper comparison constant；真正的 lower-charge strength 由 \(1/\Gamma_\rho\) 编码。统一 \(\theta_-\) 与 forward-window availability 是 theorem gates，不是右端乘子。 ||| Here \(\Gamma_\rho\) is an upper comparison constant; the actual lower-charge strength is encoded by \(1/\Gamma_\rho\). Uniform \(\theta_-\) and forward-window availability are theorem gates, not right-hand-side multipliers.
本节证明同刻 batch 的一次 time-slice square-function estimate，没有给出 uniform NSE temporal packing、内部多 face、无限 frame、Leray 极限、继续性或全局正则性结论。 ||| This section proves a single time-slice square-function estimate for the same-time batch; it gives no result on uniform NSE temporal packing, multiple interior faces, the infinite frame, the Leray limit, continuation, or global regularity.
对同一时刻的全部 entries，leading direction 支撑在 cutoff cell 中。bounded overlap 与 annular \(\dot H^{-1}\) square sum 给出 \[ \mathsf e_\Lambda(t) \le M_\chi C_T\frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)} \lesssim M_\chi C_T\|u(t)\|_2Y(t)^{1/2}. \] 因而同刻 batch 被一次 time-slice square-function estimate 吸收。 ||| For all entries at the same time, the leading direction is supported in the cutoff cell. Bounded overlap and the annular \(\dot H^{-1}\) square sum give \[ \mathsf e_\Lambda(t) \le M_\chi C_T\frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)} \lesssim M_\chi C_T\|u(t)\|_2Y(t)^{1/2}. \] Thus a single time-slice square-function estimate absorbs the same-time batch.
bounded-overlap 与 \(\dot H^{-1}\) Lamb square sum 组成的一次 time-slice square-function estimate 吸收同刻 batch；完整时间累积被精确归约到 distinct entry-time counting measure。 ||| A single time-slice square-function estimate formed from bounded overlap and the \(\dot H^{-1}\) Lamb square sum absorbs the same-time batch; the full temporal accumulation is reduced exactly to the distinct entry-time counting measure.
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
  throw new Error("duplicate Chinese keys in R0.71R translation rows");
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
  "recap-r0-61-r0-71r.html",
  "notes/r0-71r.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.03')) {
    throw new Error(relative + ": expected i18n cache version v1.03");
  }
}

const currentWithoutBatch = current.filter((entry) => !/^r071r\d+$/.test(entry.id));
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error("duplicate Chinese keys outside the R0.71R batch");
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
    id: "r071r" + String(index + 1).padStart(3, "0"),
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
