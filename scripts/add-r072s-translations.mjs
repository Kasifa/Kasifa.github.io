import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const defaultRoot = resolve(import.meta.dirname, "..");
const root = resolve(process.env.R072S_RELEASE_ROOT ?? defaultRoot);
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const bundlePath = resolve(publicDirectory, "i18n-en.js");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r072s-missing.json");
const checkOnly = process.argv.includes("--check-only");
const refreshSnapshot = process.argv.includes("--refresh-snapshot");

const translations = JSON.parse(await readFile(translationPath, "utf8"));
const retained = translations.filter((entry) => !/^r072s\d+$/.test(entry.id));
const byChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (byChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.72S batch");
}

const englishByChinese = new Map();
const row = (zh, en) => {
  if (englishByChinese.has(zh)) {
    throw new Error("Duplicate explicit R0.72S Chinese row: " + zh);
  }
  englishByChinese.set(zh, en);
};

// The rows below deliberately use the restricted singularity-theory language:
// miniversality is modulo constants; the incidence preimage is not identified
// with the global caustic image; and the A3 path is transverse only in its
// real-even slice.  The PDE and Clay boundaries remain open.

row("研究笔记 R0.72S · 2026-08-28", "Research note R0.72S · 2026-08-28");
row("版本 v0.72S · 2026-08-28", "Version v0.72S · 2026-08-28");
row("阅读 R0.72S 研究笔记 →", "Read research note R0.72S →");
row("R0.72S 附图", "R0.72S figure");
row("R0.72S 证书", "R0.72S certificates");
row("文献综述 v1.32 · 2026-08-28", "Literature review v1.32 · 2026-08-28");
row("综述 v1.32 · 2026-08-28", "Review v1.32 · 2026-08-28");
row("上次综述 v1.31 · 2026-08-28", "Previous review v1.31 · 2026-08-28");
row("累计回顾 · R0.61–R0.72S · 2026-08-28", "Cumulative recap · R0.61–R0.72S · 2026-08-28");
row("累计回顾 R0.61–R0.72S · 2026-08-28", "Cumulative recap R0.61–R0.72S · 2026-08-28");
row("R0.61–R0.72S 回顾 · 2026-08-28", "R0.61–R0.72S recap · 2026-08-28");
row("R0.61–R0.72S 研究节点", "R0.61–R0.72S research nodes");
row("R0.61–R0.72S｜R0.60 之后的研究回顾", "R0.61–R0.72S｜Research recap after R0.60");
row("回顾截止节点：R0.72S", "Recap endpoint: R0.72S");
row("回顾截止时公开笔记：169", "Public notes at recap cutoff: 169");
row("收录节点：109", "Nodes included: 109");
row("打开 109 节完整索引", "Open the complete 109-note index");
row("累计回顾与 109 节索引", "Cumulative recap and 109-note index");
row("展开 79 篇公开笔记", "Expand 79 public notes");
row("R0.70A–R0.72S 已公开版本", "Public releases from R0.70A through R0.72S");
row("R0.70A–R0.72S：71 节已公开，47 节完整封存", "R0.70A–R0.72S: 71 releases public, 47 fully sealed");
row("R0.70A–R0.72S 的 71 节已公开；47 节按当前 formal-figure 合同完整封存；24 节旧档仍待回补。", "The 71 releases from R0.70A through R0.72S are public; 47 are fully sealed under the current formal-figure contract, while 24 legacy archives remain in the backfill queue.");
row("R0.70A–R0.72S 共 71 个版本已公开；47 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。", "A total of 71 releases from R0.70A through R0.72S are public; 47 are fully sealed under the current formal-figure contract, while 24 legacy figure archives remain in the backfill queue.");
row("R0.60 recap 之后的累计回顾收录 109 个节点；全站现有 169 篇公开研究笔记", "The cumulative recap after R0.60 contains 109 nodes; the site now has 169 public research notes");

row("完整 incidence preimage 分类，不是全局 caustic image 分类", "Complete incidence-preimage classification, not a global caustic-image classification");
row("restricted miniversal modulo additive constants", "Restricted miniversal modulo additive constants");
row("incidence preimage，不是全局 caustic image", "Incidence preimage, not the global caustic image");
row("real-even A3 只在二维切片内横截", "The real-even A3 path is transverse only in its two-dimensional slice");
row("穿越临界点碰撞的非自治 ED 仍开放", "Nonautonomous enhanced dissipation through a critical-point collision remains open");
row("Clay 千禧年问题仍开放", "The Clay Millennium Problem remains open");

row("完整 \\(A_2/A_3/A_4/A_5\\) incidence preimage 分层", "Complete \\(A_2/A_3/A_4/A_5\\) incidence-preimage stratification");
row("四个系数方向在 modulo additive constants 的意义下给出 restricted miniversal unfolding", "The four coefficient directions give a restricted miniversal unfolding modulo additive constants");
row("这是一张 incidence preimage 分类表，不是四维 caustic image、self-intersections 或 complement chambers 的全局分类。", "This is a classification table for incidence preimages, not a global classification of the four-dimensional caustic image, its self-intersections, or its complement chambers.");
row("R0.72S 完整分类了声明 incidence 的 \\(A_2,A_3,A_4,A_5\\) preimages；没有更高 \\(A_k\\)。这不推出 incidence map 的单射性，也不枚举四维 caustic image 的 self-intersections、multisingularities 或全部 complement chambers。", "R0.72S completely classifies the declared incidence preimages as \\(A_2,A_3,A_4,A_5\\), with no higher \\(A_k\\). This does not imply injectivity of the incidence map and does not enumerate the self-intersections, multisingularities, or all complement chambers of the four-dimensional caustic image.");
row("系数 jet 矩阵满足 \\(\\det W_0=5400\\)。因此四个系数方向控制一至四阶导数 jet，并在 critical-point geometry modulo additive constants 的意义下给出 restricted miniversal，也即 \\(R^+\\)-versal unfolding；包含函数值方向的 full miniversal \\(A_5\\) unfolding 还需要一个常数参数。", "The coefficient jet matrix satisfies \\(\\det W_0=5400\\). Thus the four coefficient directions control derivative jets of orders one through four and give a restricted miniversal, equivalently \\(R^+\\)-versal, unfolding for critical-point geometry modulo additive constants; a full miniversal \\(A_5\\) unfolding including the function-value direction requires one additional constant parameter.");
row("局部单支 \\(A_k\\) 在 \\(\\mathbb R^4\\) 系数空间中的余维为 \\(k-1\\)，\\(2\\le k\\le5\\)。这是局部 incidence branch 结论，不是整张实 caustic 的嵌入性或全局分层。", "A single local \\(A_k\\) branch in the coefficient space \\(\\mathbb R^4\\) has codimension \\(k-1\\), for \\(2\\le k\\le5\\). This is a local incidence-branch result, not an embedding or global-stratification result for the full real caustic.");

row("generic \\(A_2\\) 热路径：不同临界点数 \\(4/3/2\\)，碰撞时按重数计仍为 \\(4\\)", "Generic \\(A_2\\) heat path: \\(4/3/2\\) distinct critical points, with total multiplicity \\(4\\) at the collision");
row("取 \\(z_{20}=4i,z_{30}=0\\)。热路径在 \\(y_*=\\log2\\) 唯一横截一个 full-family \\(A_2\\) fold；不同临界点数在碰撞前、碰撞时、碰撞后依次为 \\(4,3,2\\)，碰撞时一个点为 \\(A_2\\)、另两个为 simple，按重数计总数仍为 \\(4\\)。", "Take \\(z_{20}=4i,z_{30}=0\\). At \\(y_*=\\log2\\), the heat path uniquely crosses a full-family \\(A_2\\) fold transversely; the distinct critical-point counts before, at, and after the collision are respectively \\(4,3,2\\). At the collision one point is \\(A_2\\) and the other two are simple, while the total multiplicity remains \\(4\\).");
row("generic \\(A_2\\) fold 的精确不同点计数是 \\(4\\to3\\to2\\)", "The exact distinct-point count at the generic \\(A_2\\) fold is \\(4\\to3\\to2\\)");
row("碰撞时一个 \\(A_2\\) 点与两个 simple points 给出四的总重数", "At the collision, one \\(A_2\\) point and two simple points give total multiplicity four");

row("real-even \\(A_3\\) 热路径：不同临界点数 \\(4/2/2\\)，只在切片内横截", "Real-even \\(A_3\\) heat path: \\(4/2/2\\) distinct critical points, transverse only in the slice");
row("real-even 热路径在 \\(y_*=\\log2\\) 经过一个 \\(A_3\\) 点；不同临界点数在碰撞前、碰撞时、碰撞后依次为 \\(4,2,2\\)。碰撞时按重数计总数仍为 \\(4\\)。", "At \\(y_*=\\log2\\), the real-even heat path passes through an \\(A_3\\) point; the distinct critical-point counts before, at, and after the collision are respectively \\(4,2,2\\). At the collision the total multiplicity remains \\(4\\).");
row("这条一维路径只在 real-even 二维切片内横截 endpoint wall。\\(A_3\\) stratum 在 \\(\\mathbb R^4\\) 中余维为二，因此这里不声称 full-space transverse \\(A_3\\) crossing。", "This one-dimensional path crosses the endpoint wall transversely only inside the real-even two-dimensional slice. The \\(A_3\\) stratum has codimension two in \\(\\mathbb R^4\\), so no full-space transverse \\(A_3\\) crossing is claimed.");
row("real-even \\(A_3\\) 的精确不同点计数是 \\(4\\to2\\to2\\)", "The exact distinct-point count at the real-even \\(A_3\\) event is \\(4\\to2\\to2\\)");
row("slice-transverse，不是 full-space transverse", "Slice-transverse, not full-space transverse");

row("stationary benchmarks 不是穿越碰撞的非自治定理", "Stationary benchmarks are not a nonautonomous theorem through a collision");
row("冻结的 stationary \\(A_2\\) 与 \\(A_3\\) profile 分别对应 \\(\\nu^{3/5}\\) 与 \\(\\nu^{2/3}\\) 的有限型 ED benchmarks；这些是 autonomous 结果，不能逐时拼接成穿越临界点碰撞的一致非自治估计。", "Frozen stationary \\(A_2\\) and \\(A_3\\) profiles correspond respectively to the finite-type enhanced-dissipation benchmarks \\(\\nu^{3/5}\\) and \\(\\nu^{2/3}\\). These are autonomous results and cannot be patched pointwise in time into a uniform nonautonomous estimate through a critical-point collision.");
row("现有时变 ED 定理覆盖缓慢移动的非退化临界点、固定空间 profile 的时间调制，或保持临界点类型与数目的 rigid translation。限定一手检索没有定位到穿越 \\(A_2\\) 或 \\(A_3\\) creation–annihilation event 的一致 enhanced-dissipation theorem。", "Existing time-dependent enhanced-dissipation theorems cover slowly moving nondegenerate critical points, time modulation of a fixed spatial profile, or rigid translation that preserves the critical-point type and count. The bounded primary-source search did not locate a uniform enhanced-dissipation theorem through an \\(A_2\\) or \\(A_3\\) creation–annihilation event.");
row("Coble–He 的非退化 shape assumptions 在 \\(y=\\log2\\) 恰好失效；2026 rigid-translation 结果移动 simple critical points，但保持其类型和数目。穿越 multiplicity change 的 ED 仍是开放问题。", "The nondegenerate shape assumptions of Coble–He fail exactly at \\(y=\\log2\\); the 2026 rigid-translation result moves simple critical points but preserves their type and count. Enhanced dissipation through a change of multiplicity remains open.");

row("限定检索没有定位到精确组合，但这不是新颖性证明", "The bounded search did not locate the exact package, but this is not a proof of novelty");
row("限定一手检索没有定位到 fixed-first-harmonic \\(1{:}2{:}3\\) real unit-circle incidence 的完整 \\(A_2/A_3/A_4/A_5\\) preimage partition 与这两条热律路径的组合陈述；这只是 bounded-search absence，不构成新颖性、优先权或文献完备性证明。", "The bounded primary-source search did not locate a combined statement for the fixed-first-harmonic \\(1{:}2{:}3\\) real unit-circle incidence that contains the complete \\(A_2/A_3/A_4/A_5\\) preimage partition and these two heat-law paths. This is only a bounded-search absence and establishes neither novelty, priority, nor completeness of the literature.");
row("Voorhaar 的 complex Laurent coefficient-space Morse discriminant 与 Arnol'd 的 degree-three maximal-real-critical region 提供重要背景，但都不直接给出本站四实维 real unit-circle caustic image 的全局分层。", "Voorhaar's complex Laurent-coefficient-space Morse discriminant and Arnol'd's degree-three maximal-real-critical region provide important background, but neither directly gives a global stratification of this site's four-real-dimensional real unit-circle caustic image.");
row("caustic 记录退化临界点；Morse discriminant 还包含 Maxwell stratum。R0.72S 目前研究前者，不能把两者混写。", "The caustic records degenerate critical points, whereas the Morse discriminant also contains the Maxwell stratum. R0.72S currently studies the former, and the two must not be conflated.");

row("R0.72S 的严格价值是把 qualitative wall picture 换成 exact local singularity ledger 与两条全局计数热路径。", "The rigorous value of R0.72S is to replace a qualitative wall picture with an exact local singularity ledger and two globally counted heat paths.");
row("对 Clay 问题的直接价值仍低：这里只有有限谐波 shear、特殊 triangular reduction 与局部奇点几何；没有一般三维 continuation criterion，没有控制 vortex stretching 与 pressure coupling，也没有证明有限时破裂或全局光滑性。Clay 千禧年问题仍未解决。", "The direct value for the Clay problem remains low: the result concerns only finite-harmonic shears, a special triangular reduction, and local singularity geometry. There is no general three-dimensional continuation criterion, no control of vortex stretching and pressure coupling, and no proof of finite-time breakdown or global smoothness. The Clay Millennium Problem remains unsolved.");
row("截至 R0.72S，没有一般三维 continuation criterion，也没有证明有限时破裂或全局光滑性；不能把 109 个节点或 71 个公开版本解释成 Clay 问题完成比例。", "Through R0.72S there is no general three-dimensional continuation criterion and no proof of finite-time breakdown or global smoothness. The 109 nodes or 71 public releases must not be interpreted as a completion percentage for the Clay problem.");
row("下一步 R0.72T：", "Next R0.72T:");
row("下一节围绕显式 \\(A_2\\) collision 建立局部 spacetime normal form，先确定候选 mixing scale，再证明 model subelliptic 或 hypocoercive estimate；只有这一步闭合后，才尝试扰动转移回精确热路径。", "The next section will build a local spacetime normal form around the explicit \\(A_2\\) collision, first determine the candidate mixing scale, and then prove a model subelliptic or hypocoercive estimate. Only after that step is closed will a perturbative transfer back to the exact heat path be attempted.");
row("从 exact singularity ledger 推进到 collision-uniform PDE model", "Advance from the exact singularity ledger to a collision-uniform PDE model");
row("R0.72T 从 \\(A_2\\) 局部 normal form 开始", "R0.72T starts from the local \\(A_2\\) normal form");

row("研究笔记 R0.72S：incidence-preimage A2–A5 分类、restricted miniversal、pure-second 4/3/2 与 real-even 4/2/2 heat collisions。", "Research note R0.72S: incidence-preimage A2–A5 classification, restricted miniversality, and pure-second 4/3/2 and real-even 4/2/2 heat collisions.");
row("R0.72S｜exact singular strata 与两条 heat collision", "R0.72S｜Exact singular strata and two heat collisions");
row("局部 A2–A5 账本与两条全热路径已精确计数；global caustic 和 ED through collision 保持开放。", "The local A2–A5 ledger and two full heat paths are counted exactly; the global caustic and enhanced dissipation through a collision remain open.");
row("研究笔记 R0.72S · EXACT SINGULAR STRATA · TWO HEAT COLLISIONS", "Research note R0.72S · EXACT SINGULAR STRATA · TWO HEAT COLLISIONS");
row("局部奇性账本已经闭合；", "The local singularity ledger is closed;");
row("两条热路径给出不同的临界点碰撞", "two heat paths produce different critical-point collisions");
row("对固定第一谐波的 complex \\(1{:}2{:}3\\) family，我把 incidence preimage 精确分成 \\(A_2,A_3,A_4,A_5\\)，并核对 coefficient-derivative jet determinant \\(5400\\)。一个 pure-second path 在 \\(y_*=\\log2\\) 发生全系数切片中横截的 \\(A_2\\) fold，distinct count 为 \\(4/3/2\\)；另一个 real-even path 发生 symmetry-restricted \\(A_3\\)，distinct count 为 \\(4/2/2\\)，且只在实偶切片内横截。两者在碰撞时按重数都计为四。", "For the fixed-first-harmonic complex \\(1{:}2{:}3\\) family, the incidence preimages are partitioned exactly into \\(A_2,A_3,A_4,A_5\\), and the coefficient-derivative jet determinant \\(5400\\) is verified. At \\(y_*=\\log2\\), a pure-second path crosses an \\(A_2\\) fold transversely in the full coefficient slice, with distinct count \\(4/3/2\\); a real-even path undergoes a symmetry-restricted \\(A_3\\) event, with distinct count \\(4/2/2\\), and is transverse only in the real-even slice. Both have total multiplicity four at the collision.");
row("状态 · R0.72S exact local strata 与 heat collisions 完成", "Status · R0.72S exact local strata and heat collisions complete");
row("局部奇性与两条全热路径已精确计数，穿墙 PDE 仍开放", "The local singularities and two full heat paths are counted exactly; the PDE across the wall remains open");
row("每个 incidence preimage 恰为 \\(A_2,A_3,A_4\\) 或 \\(A_5\\)；该有限谐波族没有更高型。", "Every incidence preimage is exactly \\(A_2,A_3,A_4\\), or \\(A_5\\); this finite-harmonic family has no higher type.");
row("四个系数方向对一至四阶导数 jet 的行列式为 \\(5400\\)，所以 modulo additive constants 局部余维依次为 \\(1,2,3,4\\)。", "The determinant for the four coefficient directions against derivative jets of orders one through four is \\(5400\\), so modulo additive constants the local codimensions are respectively \\(1,2,3,4\\).");
row("pure-second \\(A_2\\) 路径的 distinct count 是 \\(4/3/2\\)；real-even \\(A_3\\) 路径是 \\(4/2/2\\)。两者碰撞时按重数均为四。", "The pure-second \\(A_2\\) path has distinct count \\(4/3/2\\); the real-even \\(A_3\\) path has \\(4/2/2\\). Both have total multiplicity four at the collision.");
row("没有分类完整四维 caustic image，也没有证明临界点数或重数改变时仍统一成立的 enhanced dissipation。", "The complete four-dimensional caustic image is not classified, and no enhanced-dissipation estimate uniform through a change in critical-point count or multiplicity is proved.");
row("先固定退化临界点，再分类它的 vanishing order", "First mark a degenerate critical point, then classify its vanishing order");
row("在 \\(z_3e^{3i\\phi}=A+iB\\) 下，\\(f'=f''=0\\) 等价于", "With \\(z_3e^{3i\\phi}=A+iB\\), the equations \\(f'=f''=0\\) are equivalent to");
row("因此 \\(B\\ne\\sin\\phi/5\\) 给 \\(A_2\\)；再令 \\(B=\\sin\\phi/5\\) 得 \\(A_3\\) 条件；继续令 \\(A=\\cos\\phi/15\\) 得 \\(A_4\\)，其五阶 jet 为 \\(-24\\sin\\phi\\)。端点再退化时六阶 jet 为 \\(-24\\cos\\phi\\ne0\\)，所以终止于 \\(A_5\\)。", "Thus \\(B\\ne\\sin\\phi/5\\) gives \\(A_2\\); imposing \\(B=\\sin\\phi/5\\) gives the \\(A_3\\) condition; further imposing \\(A=\\cos\\phi/15\\) gives \\(A_4\\), whose fifth-order jet is \\(-24\\sin\\phi\\). When an endpoint degenerates further, the sixth-order jet is \\(-24\\cos\\phi\\ne0\\), so the list terminates at \\(A_5\\).");
row("5400 控制 derivative jets，不包含函数值方向", "5400 controls the derivative jets, not the function-value direction");
row("任意 \\(\\phi\\) 只旋转二、三谐波的两个实系数块，行列式不变。这个结论给出 critical-point geometry modulo additive constants 的 restricted miniversal，也就是 \\(R^+\\)-versal。若连函数值一起记录，\\(A_5\\) 的 full miniversal deformation 还需要一个常数参数。", "Changing \\(\\phi\\) only rotates the two real coefficient blocks for the second and third harmonics, leaving the determinant unchanged. This gives a restricted miniversal unfolding for critical-point geometry modulo additive constants, equivalently an \\(R^+\\)-versal unfolding. If the function value is also recorded, the full miniversal deformation of \\(A_5\\) requires one additional constant parameter.");
row("允许 marked state \\(\\phi\\) 移动后，单个局部 \\(A_k\\) coefficient branch 的余维为 \\(k-1\\)。这是 preimage branch 的局部结论，不是完整 projected caustic 已经嵌入或没有 self-intersection 的证明。", "After allowing the marked state \\(\\phi\\) to move, a single local \\(A_k\\) coefficient branch has codimension \\(k-1\\). This is a local statement about a preimage branch, not a proof that the complete projected caustic is embedded or free of self-intersections.");
row("一个二次方程给出全路径唯一退化与 \\(4/3/2\\)", "One quadratic equation gives the unique full-path degeneracy and \\(4/3/2\\)");
row("\\(s_-\\in(-1,0)\\) 对全部 \\(k>0\\) 成立；\\(s_+\\) 在 \\(k>1\\) 时位于 \\((0,1)\\)，在 \\(k=1\\) 等于一，在 \\(0<k<1\\) 时离开实 sine range。结合 \\(F_y''=\\cos\\phi(-1+4k\\sin\\phi)\\)，全路径唯一退化点是 \\(y_*=\\log2,\\phi_*=\\pi/2\\)。", "The inclusion \\(s_-\\in(-1,0)\\) holds for every \\(k>0\\); the root \\(s_+\\), when \\(k>1\\), lies in \\((0,1)\\), equals one when \\(k=1\\), and leaves the real sine range when \\(0<k<1\\). Combined with \\(F_y''=\\cos\\phi(-1+4k\\sin\\phi)\\), this shows that the unique degeneracy on the full path is \\(y_*=\\log2,\\phi_*=\\pi/2\\).");
row("等号时一个 \\(A_2\\) 点为二重根，另有两个简单点，所以按重数仍为四。这个 representative 的第三 carrier 为零，但 \\(F'''=\\partial_yF'=-3\\ne0\\)，路径对 full four-real coefficient slice 的局部 codimension-one \\(A_2\\) wall 横截。", "At equality, one \\(A_2\\) point is a double root and two other points are simple, so the multiplicity count remains four. The third carrier of this representative vanishes, but \\(F'''=\\partial_yF'=-3\\ne0\\), and the path is transverse to the local codimension-one \\(A_2\\) wall in the full four-real coefficient slice.");
row("对称轴保留中心临界点，两个 off-axis roots 并入它", "The symmetry axis retains the central critical point as two off-axis roots merge into it");
row("写 \\(t=e^{-y}\\)、\\(x=\\cos\\phi\\)，则 \\(H_y'=-\\sin\\phi\\,q_t(x)\\)，其中", "Writing \\(t=e^{-y}\\) and \\(x=\\cos\\phi\\) gives \\(H_y'=-\\sin\\phi\\,q_t(x)\\), where");
row("\\(q_t\\) 在 \\([-1,1]\\) 上严格下降，\\(q_t(-1)>0\\)，且 \\(q_t(1)\\) 恰在 \\(t=1/2\\) 变号。因此", "The function \\(q_t\\) is strictly decreasing on \\([-1,1]\\), satisfies \\(q_t(-1)>0\\), and \\(q_t(1)\\) changes sign exactly at \\(t=1/2\\). Therefore");
row("碰撞点 \\(\\phi=0\\) 是 \\(A_3\\) 三重根，\\(\\phi=\\pi\\) 是简单根，所以按重数仍为四。这里 \\(H''''=\\partial_yH''=-1533/512\\ne0\\)。函数芽属于 ambient \\(A_3\\) stratum，但一参数路径只在 real-even 二维切片内横截 endpoint wall；不能称为 full-space transverse \\(A_3\\)。", "The collision point \\(\\phi=0\\) is an \\(A_3\\) triple root, while \\(\\phi=\\pi\\) is simple, so the multiplicity count remains four. Here \\(H''''=\\partial_yH''=-1533/512\\ne0\\). The function germ belongs to the ambient \\(A_3\\) stratum, but the one-parameter path is transverse to the endpoint wall only inside the real-even two-dimensional slice; it must not be called a full-space transverse \\(A_3\\) crossing.");
row("两种碰撞都有平方根分支，但中心机制不同", "Both collisions have square-root branches, but their central mechanisms differ");
row("令 \\(\\delta=y-\\log2\\)。在 \\(A_2\\) 点取 \\(\\xi=\\phi-\\pi/2\\)，在 \\(A_3\\) 点取 \\(\\phi\\) 本身，则", "Let \\(\\delta=y-\\log2\\). At the \\(A_2\\) point take \\(\\xi=\\phi-\\pi/2\\), while at the \\(A_3\\) point take \\(\\phi\\) itself. Then");
row("第一条路径中碰撞点随后消失；第二条路径中反射对称性让中心点始终保留。附图只展示这两条已证明的局部分支，不替代全局单调性证明。", "On the first path the collision point disappears afterward; on the second, reflection symmetry preserves the central point throughout. The figure shows only these two proved local branches and does not replace the global monotonicity proofs.");
row("distinct locations 与 root multiplicity 必须分开", "Distinct locations and root multiplicity must be kept separate");
row("pure-second \\(A_2\\) 的 before/at/after distinct count 是 \\(4/3/2\\)，碰撞时重数分解为 \\(2+1+1=4\\)。real-even \\(A_3\\) 是 \\(4/2/2\\)，碰撞时为 \\(3+1=4\\)。把阈值时刻简写为“\\(4\\to2\\)”会丢失两种局部机制的差别。", "For the pure-second \\(A_2\\) event, the before/at/after distinct count is \\(4/3/2\\), and the collision multiplicities decompose as \\(2+1+1=4\\). For the real-even \\(A_3\\) event the count is \\(4/2/2\\), with \\(3+1=4\\) at the collision. Abbreviating the threshold event as “\\(4\\to2\\)” loses the distinction between the two local mechanisms.");
row("同样，incidence preimage 是带 marked \\(\\phi\\) 的解；把它投影到 \\((z_2,z_3)\\) 后，多个 preimages 可以落在同一系数点。本节没有枚举这种 multisingularity，也没有给完整 chamber diagram。", "Likewise, an incidence preimage is a solution with marked \\(\\phi\\); after projection to \\((z_2,z_3)\\), multiple preimages may land at the same coefficient point. This section neither enumerates such multisingularities nor gives a complete chamber diagram.");
row("冻结 profile 的有限型速率不能拼成穿越碰撞的定理", "Finite-type rates for frozen profiles cannot be patched into a theorem through a collision");
row("stationary finite-type 文献给 frozen \\(A_2\\) profile 的 \\(\\nu^{3/5}\\) benchmark 和 frozen \\(A_3\\) profile 的 \\(\\nu^{2/3}\\) benchmark。现有 nonautonomous 结果覆盖共同非退化临界点、固定空间 profile 的时间调制或保持临界点类型与数量的刚性平移；它们不覆盖这里的 creation、annihilation 或 multiplicity change。", "The stationary finite-type literature gives a frozen \\(A_2\\) profile the \\(\\nu^{3/5}\\) benchmark and a frozen \\(A_3\\) profile the \\(\\nu^{2/3}\\) benchmark. Existing nonautonomous results cover common nondegenerate critical points, time modulation of a fixed spatial profile, or rigid translation that preserves the critical-point type and count; they do not cover the creation, annihilation, or multiplicity change here.");
row("因此 R0.72S 没有证明 ED through collision。把每个 frozen time 的速率逐点拼接，也不能替代一个统一的非自治 subelliptic 或 hypocoercive estimate。", "Therefore R0.72S does not prove enhanced dissipation through a collision. Patching the rate at each frozen time pointwise cannot replace a uniform nonautonomous subelliptic or hypocoercive estimate.");
row("Fraction 与 BigInt 双路只封存有限代数骨架", "The Fraction and BigInt routes seal only the finite algebraic spine");
row("Python rational producer 与独立 JavaScript BigInt audit 重建 incidence jets、determinant \\(5400\\)、两条路径的 exact sign guards、crossing jets 和 leading split coefficients \\(-2,-6\\)。comparator 要求 canonical payload 精确相同，正式证书还绑定同一 clean source commit。", "The Python rational producer and independent JavaScript BigInt audit reconstruct the incidence jets, determinant \\(5400\\), exact sign guards and crossing jets for both paths, and the leading split coefficients \\(-2,-6\\). The comparator requires exact equality of the canonical payloads, and the formal certificate is also bound to the same clean source commit.");
row("唯一碰撞与全局 distinct/multiplicity counts 由连续 root-count proof 推出；机器证书只核对该证明使用的有限恒等式和符号守卫。它不分类全局 caustic image，也不证明穿墙 enhanced dissipation。", "The unique collision and the global distinct and multiplicity counts follow from the continuum root-count proof; the machine certificate checks only the finite identities and sign guards used by that proof. It neither classifies the global caustic image nor proves enhanced dissipation across the wall.");
row("一般奇性理论、degree-three 拓扑与本站精确路径是三件事", "General singularity theory, degree-three topology, and the exact paths here are three different things");
row("给出 \\(A_k\\) 与 versality 的标准局部框架；", "gives the standard local framework for \\(A_k\\) and versality;");
row("研究 real degree-three maximal-real-critical region 的拓扑。R0.72S 不把 degree-three region 本身主张为新发现。", "studies the topology of the real degree-three maximal-real-critical region. R0.72S does not claim the degree-three region itself as a new discovery.");
row("给 stationary finite-type benchmarks；", "give the stationary finite-type benchmarks;");
row("划定当前 nonautonomous 边界。限定一手检索没有定位到穿越这里 multiplicity-changing collision 的 ED theorem；这是 bounded-search absence，不是不存在性或优先权证明。", "delineate the current nonautonomous boundary. The bounded primary-source search did not locate an enhanced-dissipation theorem through the multiplicity-changing collision here; this is a bounded-search absence, not a proof of nonexistence or priority.");
row("三联图分别展示 incidence spine、A2 branches 与 A3 branches", "The three panels show the incidence spine, A2 branches, and A3 branches");
row("下一道可检验问题已经从几何墙转成非自治局部模型", "The next testable problem has shifted from the geometric wall to a local nonautonomous model");
row("R0.72S 的直接增量是一个可审计的局部 singular-strata ledger，以及两条全时间精确计数的 heat-law path。它给下一步 PDE 分析提供碰撞时间、jet constants 与 square-root branch scales，也明确说明现有 nondegenerate time-dependent theorem 在哪里失去假设。", "The direct R0.72S increment is an auditable local singular-strata ledger together with two heat-law paths counted exactly for all time. It supplies the collision time, jet constants, and square-root branch scales for the next PDE analysis, and identifies exactly where existing nondegenerate time-dependent theorems lose their hypotheses.");
row("对 Clay 问题的直接价值仍低。这里是有限谐波 scalar shear 与特殊 triangular reduction 的局部几何，没有一般三维 continuation estimate，也没有奇性构造或全局正则性证明。", "The direct value for the Clay problem remains low. This is local geometry for a finite-harmonic scalar shear in a special triangular reduction, with no general three-dimensional continuation estimate, singularity construction, or global-regularity proof.");
row("local marked strata 不等于 global caustic，也不等于 Clay 进展比例", "Local marked strata are neither the global caustic nor a measure of progress on the Clay problem");
row("没有证明 incidence map injective、全部 self-intersections、multisingularities、完整 complement chambers、real \\(A_{2j+1}^{\\pm}\\) refinement、two-parameter full-slice transverse \\(A_3\\)、任意相位 heat path、ED through collision、一般三维稳定性、有限时奇性或全局光滑性。Clay 千禧年问题仍未解决。", "No injectivity of the incidence map, all self-intersections, multisingularities, complete complement chambers, real \\(A_{2j+1}^{\\pm}\\) refinement, two-parameter full-slice transverse \\(A_3\\) unfolding, arbitrary-phase heat path, enhanced dissipation through a collision, general three-dimensional stability, finite-time singularity, or global smoothness is proved. The Clay Millennium Problem remains unsolved.");
row("R0.72T：缩放 A2 spacetime normal form，并先证明模型估计", "R0.72T: rescale the A2 spacetime normal form and first prove a model estimate");
row("下一节围绕 \\(F'\\sim-3\\delta-(3/2)\\xi^2\\) 选择时空尺度，平衡 time drift、quadratic spatial degeneracy、transport frequency 与 diffusion。只有先得到 uniform nonautonomous model estimate，才讨论向 exact heat path 的 perturbative transfer。", "The next section will choose spacetime scales around \\(F'\\sim-3\\delta-(3/2)\\xi^2\\), balancing time drift, quadratic spatial degeneracy, transport frequency, and diffusion. A perturbative transfer to the exact heat path will be considered only after a uniform nonautonomous model estimate is obtained.");
row("marked \\(A_2\\)–\\(A_5\\) strata 与两条 heat collision 已精确闭合", "The marked \\(A_2\\)–\\(A_5\\) strata and two heat collisions are closed exactly");
row("incidence preimage 由 higher jets 精确分为 \\(A_2,A_3,A_4,A_5\\)；四个系数方向的一至四阶 derivative-jet determinant 为 \\(5400\\)，支持 modulo constants 的 restricted miniversal 与单个 marked branch 的局部余维 \\(1,2,3,4\\)。", "Higher jets partition the incidence preimages exactly into \\(A_2,A_3,A_4,A_5\\); the derivative-jet determinant of orders one through four for the four coefficient directions is \\(5400\\), supporting restricted miniversality modulo constants and local codimensions \\(1,2,3,4\\) for a single marked branch.");
row("pure-second path 的 distinct count 为 \\(4/3/2\\)，且全 \\(y\\ge0\\) 只有 \\(y=\\log2\\) 一个 \\(A_2\\) 事件；real-even path 为 \\(4/2/2\\)，其 \\(A_3\\) 只在 real-even slice 内横截。两条路径在碰撞时按重数都为四。", "The pure-second path has distinct count \\(4/3/2\\); over all \\(y\\ge0\\), its only event occurs at \\(y=\\log2\\) and is an \\(A_2\\) event. The real-even path has \\(4/2/2\\), and its \\(A_3\\) event is transverse only inside the real-even slice. Both paths have total multiplicity four at the collision.");
row("没有完成 global caustic image、自交或 chamber 分类，也没有证明 multiplicity-changing collision 上的 enhanced dissipation。Clay 问题保持开放。", "The global caustic image, its self-intersections, and its chamber classification are not completed, and enhanced dissipation through a multiplicity-changing collision is not proved. The Clay problem remains open.");
row("缩放 \\(F'\\sim-3\\delta-(3/2)\\xi^2\\) 的 spacetime normal form，先证明统一 model estimate，再检查能否回传到 exact heat path。", "Rescale the spacetime normal form \\(F'\\sim-3\\delta-(3/2)\\xi^2\\), first prove a uniform model estimate, and then test whether it can be transferred back to the exact heat path.");
row("缩放 A2 spacetime normal form，并先证明非自治 model estimate。", "Rescale the A2 spacetime normal form and first prove a nonautonomous model estimate.");
row("阶段后续 R0.72S（已完成）：", "Historical next R0.72S (now complete):");
row("R0.72S 已闭合 marked A2–A5 strata 与两条 exact heat collisions；下一关是 A2 spacetime normal form 上的非自治 model estimate。", "R0.72S closes the marked A2–A5 strata and two exact heat collisions; the next gate is a nonautonomous model estimate on the A2 spacetime normal form.");
row("R0.72S 把 R0.72R 的 incidence 继续分成 marked \\(A_2,A_3,A_4,A_5\\) strata；determinant \\(5400\\) 给 modulo constants 的 restricted miniversal。pure-second path 具有全局 \\(4/3/2\\) distinct count，real-even path 具有 \\(4/2/2\\)，crossing multiplicity 均为四。A3 只在 real-even slice 内横截；global caustic image 与 ED through collision 没有闭合。", "R0.72S further partitions the R0.72R incidence into marked \\(A_2,A_3,A_4,A_5\\) strata; determinant \\(5400\\) gives restricted miniversality modulo constants. The pure-second path has global distinct count \\(4/3/2\\), while the real-even path has \\(4/2/2\\), and both have multiplicity four at the crossing. The A3 path is transverse only in the real-even slice; the global caustic image and enhanced dissipation through a collision are not closed.");
row("累计回顾保持二十八个问题阶段，并给出 R0.61–R0.72S 的完整逐节点索引。R0.72S 增加 incidence-preimage \\(A_2\\)–\\(A_5\\) ledger、restricted miniversal，以及 pure-second \\(4/3/2\\) 与 real-even \\(4/2/2\\) 两条 exact heat path。", "The cumulative recap retains twenty-eight problem phases and gives a complete node-by-node index through R0.72S. R0.72S adds the incidence-preimage \\(A_2\\)–\\(A_5\\) ledger, restricted miniversality, and two exact heat paths: pure-second \\(4/3/2\\) and real-even \\(4/2/2\\).");
row("局部 caustic 类型已经精确化；global image、ED through collision 与一般三维问题仍开放。", "The local caustic types are now exact; the global image, enhanced dissipation through a collision, and the general three-dimensional problem remain open.");

row("处理 complex Laurent coefficient space 中的 Morse discriminant；", "treats the Morse discriminant in complex Laurent coefficient space;");
row("的 nonautonomous results 保持临界点类型与数量；它们不覆盖这里的 creation、annihilation 或 multiplicity change。", "provide nonautonomous results that preserve critical-point type and count; they do not cover the creation, annihilation, or multiplicity change here.");
row("给 frozen finite-type profiles 的 stationary benchmarks。", "give stationary benchmarks for frozen finite-type profiles.");
row("结论限于 fixed-first-harmonic \\(\\mathbb C^2\\cong\\mathbb R^4\\) coefficient slice。pure-second path 在该切片中横截局部 codimension-one \\(A_2\\) branch，distinct count 为 \\(4/3/2\\)；real-even path 的 \\(A_3\\) 只在二维 real-even slice 内横截，distinct count 为 \\(4/2/2\\)。两条路径都只在碰撞时按重数计为四；碰撞后实临界点的总重数为二。没有完成 global caustic image、self-intersections、chambers、ED through collision 或一般三维 continuation。限定一手检索的 absence 不构成不存在性、新颖性或优先权证明；Clay 千禧年问题仍未解决。", "The result is confined to the fixed-first-harmonic \\(\\mathbb C^2\\cong\\mathbb R^4\\) coefficient slice. In that slice the pure-second path crosses a local codimension-one \\(A_2\\) branch transversely, with distinct count \\(4/3/2\\); the \\(A_3\\) event on the real-even path is transverse only inside the two-dimensional real-even slice, with distinct count \\(4/2/2\\). Both paths have multiplicity four only at the collision; afterward the real critical points have total multiplicity two. The global caustic image, self-intersections, chambers, enhanced dissipation through a collision, and general three-dimensional continuation are not completed. Absence in the bounded primary-source search proves neither nonexistence, novelty, nor priority; the Clay Millennium Problem remains unsolved.");
row("开放接口 · R0.72T", "Open interface · R0.72T");
row("仍把更高余维 Lyashko–Looijenga strata 列为问题。R0.72S 分类的是带 marked \\(\\phi\\) 的 incidence preimages；投影后的自交、multisingularities 与全部 real complement chambers 没有由此自动得到。", "still lists the higher-codimension Lyashko–Looijenga strata as a question. R0.72S classifies incidence preimages with marked \\(\\phi\\); their projected self-intersections, multisingularities, and all real complement chambers do not follow automatically.");
row("缩放 \\(F'\\sim-3\\delta-(3/2)\\xi^2\\) 的 spacetime normal form，先证明统一 model estimate，再检查向 exact heat path 的 perturbative transfer。", "Rescale the spacetime normal form \\(F'\\sim-3\\delta-(3/2)\\xi^2\\), first prove a uniform model estimate, and then test a perturbative transfer to the exact heat path.");
row("我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72S 只列为研究笔记。我不把计算或笔记外推成正则性定理。", "I list published theorems as known results, mark 2026 preprints separately, and list R0.69P–R0.72S on this site only as research notes. I do not extrapolate computations or notes into regularity theorems.");
row("已研究 degree-three maximal-real-critical region 的拓扑。R0.72S 的 determinant \\(5400\\) 只支持 critical-point geometry modulo additive constants 的 restricted miniversal，或 \\(R^+\\)-versal；包含函数值方向的 full \\(A_5\\) miniversal 还需一个常数参数。", "already studied the topology of the degree-three maximal-real-critical region. The R0.72S determinant \\(5400\\) supports only a restricted miniversal unfolding for critical-point geometry modulo additive constants, equivalently an \\(R^+\\)-versal unfolding; the full \\(A_5\\) miniversal unfolding including the function-value direction needs one additional constant parameter.");
row("fixed-first-harmonic \\(1{:}2{:}3\\) incidence preimages 止于 \\(A_5\\)，coefficient-derivative jet determinant 为 \\(5400\\)。pure-second \\(A_2\\) path 的 distinct count 是 \\(4/3/2\\)，real-even \\(A_3\\) path 是 \\(4/2/2\\)；两者只在碰撞时按重数计为四，A3 只在 real-even slice 内横截。", "The fixed-first-harmonic \\(1{:}2{:}3\\) incidence preimages terminate at \\(A_5\\), and the coefficient-derivative jet determinant is \\(5400\\). The pure-second \\(A_2\\) path has distinct count \\(4/3/2\\), while the real-even \\(A_3\\) path has \\(4/2/2\\); both have multiplicity four only at the collision, and the A3 path is transverse only inside the real-even slice.");
row("R0.72S 的 marked strata、热碰撞与 PDE 文献边界", "Literature boundary for the R0.72S marked strata, heat collisions, and PDE");
row("R0.72S 的主张边界", "R0.72S claim boundary");

row("05 · 局部分支律", "05 · Local branch laws");
row("06 · 计数口径", "06 · Count convention");
row("07 · PDE 边界", "07 · PDE boundary");
row("计数口径", "Count convention");
row("局部分支", "Local branches");
row("PDE 边界", "PDE boundary");

row("02 · 109 节完整索引", "02 · Complete 109-note index");
row("版本数、封存数和数学结论分开报告", "Report release counts, sealed counts, and mathematical conclusions separately");
row("保留 R0.72R 历史回顾", "Retain the historical R0.72R recap");
row("查看 R0.72S 精确证书", "View the exact R0.72S certificates");
row("打开最新节点 R0.72S", "Open the latest node R0.72S");
row("二十八个阶段、109 个节点：从约化递推到 exact singular strata 与 heat collisions。", "Twenty-eight phases and 109 nodes: from reduced recurrences to exact singular strata and heat collisions.");
row("旧版附图档案待回补", "Legacy figure archives awaiting backfill");
row("局部 caustic 类型已经精确化，穿越碰撞的 PDE 估计仍未建立", "The local caustic types are now exact; the PDE estimate through a collision is not yet established");
row("围绕 \\(F'\\sim-3\\delta-(3/2)\\xi^2\\) 选择时空缩放，证明一个统一 nonautonomous model estimate；没有该估计前，不把 frozen \\(\\nu^{3/5}\\) benchmark 外推成穿墙定理。", "Choose spacetime scales around \\(F'\\sim-3\\delta-(3/2)\\xi^2\\) and prove a uniform nonautonomous model estimate; until that estimate exists, the frozen \\(\\nu^{3/5}\\) benchmark is not extrapolated into a theorem across the wall.");
row("新的严格增量是 incidence-preimage \\(A_2\\)–\\(A_5\\) ledger、restricted miniversal，以及两条全时间 exact heat path 的 distinct/multiplicity count。完整 projected caustic、自交、chambers 与 ED through collision 仍开放。", "The new rigorous increment is the incidence-preimage \\(A_2\\)–\\(A_5\\) ledger, restricted miniversality, and the distinct and multiplicity counts for two exact full-time heat paths. The complete projected caustic, its self-intersections and chambers, and enhanced dissipation through a collision remain open.");
row("这些是 local marked-strata 与两条 explicit path 的结论，不是 global caustic image classification。A3 path 只在 real-even slice 内横截；ED through collision、任意三维 continuation 与 Clay 正式问题仍开放。", "These are results for local marked strata and two explicit paths, not a classification of the global caustic image. The A3 path is transverse only inside the real-even slice; enhanced dissipation through a collision, general three-dimensional continuation, and the formal Clay problem remain open.");
row("这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72S 的 109 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。", "This page follows the R0.00–R0.60 phase recap and organizes the 109 research nodes from R0.61 through R0.72S. It records chronologically what each segment actually proves, which proposal is excluded by a concrete counterexample or scale analysis, and which hypotheses have not been derived from the Navier–Stokes equations. Node status describes the evidence type and does not misstate release sealing as resolution of a phase objective.");
row("R0.00–R0.60 的内容保留在上一份阶段回顾中。后面的 109 个节点沿一般三维临界控制缺口推进；R0.70A–R0.72S 的 71 个版本已经公开，其中 47 个满足当前 formal-figure 完整封存合同。公开和封存不表示 Clay 问题已经解决。", "The R0.00–R0.60 material remains in the preceding phase recap. The following 109 nodes advance along the gap in critical control for the general three-dimensional problem. The 71 releases from R0.70A through R0.72S are public, of which 47 satisfy the current formal-figure sealing contract. Publication and sealing do not mean that the Clay problem has been solved.");
row("R0.60 之后的研究回顾", "Research recap after R0.60");
row("R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72S 的 109 个节点；最新一节闭合 marked A2–A5 strata 与两条 exact heat collisions。", "Research recap after R0.60: complete coverage of the 109 nodes from R0.61 through R0.72S; the latest section closes the marked A2–A5 strata and two exact heat collisions.");
row("R0.61–R0.72S 的 109 节公开笔记", "The 109 public notes from R0.61 through R0.72S");
row("R0.72L–O 保留 actual ledger、排除 action-poor dissipative launch，并完成物理回填。R0.72P 在 fixed real-collinear static-phase 1:2 正类上关闭传播门；R0.72Q 给 fixed-\\(M\\) arbitrary-static-phase sufficient cone；R0.72R 再构造该旧锥外的四实维 caustic-free compact core。", "R0.72L–O retains the actual ledger, excludes the action-poor dissipative launch, and completes physical reinsertion. R0.72P closes the propagation gate on the fixed real-collinear static-phase 1:2 positive class; R0.72Q gives the fixed-\\(M\\), arbitrary-static-phase sufficient cone; and R0.72R constructs a four-real-dimensional caustic-free compact core outside that old cone.");
row("R0.72L–R0.72S · strong-coupling、物理回填与 exact caustic-local geometry", "R0.72L–R0.72S · strong coupling, physical reinsertion, and exact local caustic geometry");
row("R0.72S 的 marked singular-strata ledger：incidence preimage 止于 \\(A_5\\)，coefficient-derivative jet determinant 为 \\(5400\\)；pure-second \\(A_2\\) path 的 distinct count 是 \\(4/3/2\\)，real-even \\(A_3\\) path 是 \\(4/2/2\\)，且两者 crossing multiplicity 都为四。", "The R0.72S marked singular-strata ledger: the incidence preimages terminate at \\(A_5\\), and the coefficient-derivative jet determinant is \\(5400\\); the pure-second \\(A_2\\) path has distinct count \\(4/3/2\\), the real-even \\(A_3\\) path has \\(4/2/2\\), and both have multiplicity four at the crossing.");
row("R0.72S 对 fixed-first-harmonic \\(1{:}2{:}3\\) incidence preimages 给出 \\(A_2,A_3,A_4,A_5\\) 精确 ledger，并用 determinant \\(5400\\) 闭合 modulo constants 的 restricted miniversal。pure-second heat path 的 distinct count 为 \\(4/3/2\\)，real-even path 为 \\(4/2/2\\)；两者在碰撞时按重数都为四。", "For the fixed-first-harmonic \\(1{:}2{:}3\\) incidence preimages, R0.72S gives an exact \\(A_2,A_3,A_4,A_5\\) ledger and uses determinant \\(5400\\) to close restricted miniversality modulo constants. The pure-second heat path has distinct count \\(4/3/2\\), while the real-even path has \\(4/2/2\\); both have total multiplicity four at the collision.");
row("R0.72S 分类的是 marked incidence preimages，并只对两条 explicit heat path 作全局计数。它没有给整个 \\(\\mathbb C^2\\) caustic image 的 chamber classification；A3 只在 real-even slice 内横截，ED through collision 与 Clay 正式问题保持开放。", "R0.72S classifies marked incidence preimages and gives global counts only for two explicit heat paths. It does not provide a chamber classification of the entire \\(\\mathbb C^2\\) caustic image; the A3 path is transverse only inside the real-even slice, while enhanced dissipation through a collision and the formal Clay problem remain open.");
row("R0.72T 先处理 A2 spacetime normal form", "R0.72T first treats the A2 spacetime normal form");
row("我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.72S 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。", "I maintain a separate systematic review placing the classical theory, five literature trunks, the candidate-blow-up exclusion tree, progress from 2019 through 2026, and this site's R0.69P–R0.72S route on one map. The historical R0.61–R0.69O nodes remain in the cumulative recap.");

const activePages = [
  "literature-review.html",
  "notes/r0-72s.html",
  "recap-r0-61-r0-72s.html",
  "research-review.html",
];
for (const relative of activePages) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.32')) {
    throw new Error(relative + ": expected i18n cache version v1.32");
  }
}

const source = await collectSiteStrings(publicDirectory);
const missing = source.filter((entry) => !byChinese.has(entry.zh));
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(missingFiles) !== JSON.stringify(activePages)) {
  throw new Error("Unexpected R0.72S missing-string files: " + JSON.stringify(missingFiles));
}

const snapshot = missing.map(({ zh, count, files }) => ({ zh, count, files }));
let expectedSnapshot;
try {
  expectedSnapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
} catch (error) {
  if (error?.code !== "ENOENT" || !refreshSnapshot) throw error;
  expectedSnapshot = snapshot;
  await writeFile(snapshotPath, JSON.stringify(snapshot, null, 2) + "\n");
}
if (JSON.stringify(expectedSnapshot) !== JSON.stringify(snapshot)) {
  if (!refreshSnapshot) {
    throw new Error("R0.72S missing-string snapshot is stale");
  }
  await writeFile(snapshotPath, JSON.stringify(snapshot, null, 2) + "\n");
}

const longRoute = missing.filter(
  (entry) =>
    entry.zh.startsWith("中。R0.69P–R0.71P") &&
    entry.zh.includes("R0.72S 进一步把 fixed-first-harmonic"),
);
if (longRoute.length !== 1) {
  throw new Error(
    "Expected one extended R0.72S literature-route string, found " +
      longRoute.length,
  );
}
const oldRoute = retained.find((entry) => entry.id === "r072r015");
if (!oldRoute) {
  throw new Error("Missing retained R0.72R literature-route translation");
}
const routeTail = " General Navier–Stokes regularity remains open.";
if (!oldRoute.en.endsWith(routeTail)) {
  throw new Error("Unexpected retained R0.72R literature-route English tail");
}
englishByChinese.set(
  longRoute[0].zh,
  oldRoute.en.slice(0, -routeTail.length) +
    " R0.72S further partitions the marked incidence preimages of the fixed-first-harmonic \\(1{:}2{:}3\\) family exactly into \\(A_2,A_3,A_4,A_5\\), uses determinant \\(5400\\) to prove restricted miniversality modulo constants, and, for a pure-second \\(A_2\\) heat path and a real-even \\(A_3\\) heat path, gives the respective distinct counts \\(4/3/2\\) and \\(4/2/2\\); the latter is transverse only inside the real-even slice. The global caustic image is not completed, and enhanced dissipation through a collision is not proved." +
    routeTail,
);

if (missing.length !== 130) {
  throw new Error(
    "Expected 130 R0.72S English rows, found " + missing.length,
  );
}

const translatedEntries = missing.map((entry, index) => {
  const en = englishByChinese.get(entry.zh);
  if (!en) throw new Error("Missing explicit R0.72S English row for: " + entry.zh);
  if (!en.trim() || containsChinese(en)) {
    throw new Error("Invalid R0.72S English row for: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("First-person plural English is forbidden for: " + entry.zh);
  }
  if (
    JSON.stringify(extractProtectedTokens(en)) !==
    JSON.stringify(extractProtectedTokens(entry.zh))
  ) {
    throw new Error("Protected-token mismatch for:\n" + entry.zh + "\n" + en);
  }
  return { ...entry, id: "r072s" + String(index + 1).padStart(3, "0"), en };
});

const finalTranslations = [...retained, ...translatedEntries];
for (const field of ["id", "zh"]) {
  const values = finalTranslations.map((entry) => entry[field]);
  if (new Set(values).size !== values.length) {
    throw new Error("Duplicate final translation " + field);
  }
}

const finalByChinese = new Map(finalTranslations.map((entry) => [entry.zh, entry.en]));
const stillMissing = source.filter((entry) => !finalByChinese.has(entry.zh));
if (stillMissing.length) {
  throw new Error("R0.72S live strings remain untranslated: " + stillMissing[0].zh);
}
const dictionary = Object.fromEntries(
  source.map((entry) => [entry.zh, finalByChinese.get(entry.zh)]),
);
const jsonOutput = JSON.stringify(finalTranslations, null, 2) + "\n";
const bundleOutput =
  `globalThis.NS_EN_TRANSLATIONS = Object.freeze(${JSON.stringify(dictionary, null, 2)});\n`;

if (checkOnly) {
  const currentBundle = await readFile(bundlePath, "utf8");
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.72S translations/en.json batch is stale");
  }
  if (currentBundle !== bundleOutput) {
    throw new Error("R0.72S public/i18n-en.js bundle is stale");
  }
} else {
  await Promise.all([
    writeFile(translationPath, jsonOutput),
    writeFile(bundlePath, bundleOutput),
  ]);
}

console.log(JSON.stringify({
  checkOnly,
  refreshSnapshot,
  added: translatedEntries.length,
  total: finalTranslations.length,
  liveStrings: source.length,
  missingBefore: missing.length,
  missingAfter: 0,
  files: missingFiles,
  bundle: "public/i18n-en.js",
}));
