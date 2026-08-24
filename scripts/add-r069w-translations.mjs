import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, ".i18n-work/r069w-segments.json");
const translationPath = resolve(root, "translations/en.json");
const source = JSON.parse(await readFile(sourcePath, "utf8"));
const current = JSON.parse(await readFile(translationPath, "utf8"));
const sourceById = new Map(source.map((entry) => [entry.id, entry]));

const legacyEnglishById = {
  s8088: "; the web publication commit is",
  s8089: ". The certificate uses 524,288 raw-bump moment cells, 2,048 cutoff-certificate cells, 262,144 distance-moment cells, 512 transition radial cells, 128 core cells, and 256 plateau cells.",
  s8090: "01 · Sign proof for every amplitude",
  s8091: "02 · Exact angular reduction",
  s8092: "03 · True convolution and endpoint terms",
  s8093: "04 · Validated radial cubature",
  s8094: "05 · Certified intervals",
  s8095: "06 · Independent verification and monitoring",
  s8096: "09 · Claim boundary and pause point",
  s8097: "Version v0.69W · 2026-08-21",
  s8098: "This result does not advance the time evolution of a Navier–Stokes solution, control a critical norm, prove global regularity, or construct finite-time blow-up. It shows that this specific scale-ratio-four affine one-parameter family cannot supply an all-same-sign annular mechanism; other geometries and genuine dynamical mechanisms remain open.",
  s8099: "No longer dependent on randomized error bars:",
  s8100: "View the Clay Mathematics Institute's official problem statement",
  s8101: "View the formal figure package",
  s8102: "Every amplitude at scale ratio four is excluded by a rigorously negative annulus",
  s8103: "At \\(a=0\\), the preceding expression vanishes exactly because of its algebraic factor, so division by \\(a\\) cannot handle this case. The certificate instead checks \\(j=-2\\) and obtains \\(\\mathcal A_{-2}(u_0)<0\\) directly, closing the endpoint.",
  s8104: "The independent checker does not import the producer module. It parses the decimal JSON interval endpoints as exact rationals and recomputes \\(c_2^2-4c_1c_3\\), the leading-coefficient sign, the endpoint sign, the source hash, and HEAD alignment. The certificate separately records that the source tree was clean during the formal run; every decision passes.",
  s8105: "Independent decisions: all passed",
  s8106: "For the same true smooth cutoff and the physical-space annular functional from R0.69T, the formal certificate gives",
  s8107: "Floating quadrature nodes: 0",
  s8108: "The symbolic audit also confirms that the common-core/common-core term vanishes identically, so the formal numerical stage only has to cover a two-dimensional \\((r,s)\\) rectangle.",
  s8109: "Sign proof",
  s8110: "A negative leading coefficient and negative discriminant cover the continuum at once, without sampled amplitudes",
  s8111: "The more transferable result is the method chain: exact common rotations, distance-moment reduction, endpoint-distribution auditing for the true convolution, local mixed-order Taylor cubature, and rational verification outside the producer. This framework can be applied to a new static geometry with several degrees of freedom and can also be developed into a serious computer-assisted analysis result in its own right.",
  s8112: "Fix the R0.69V two-scale family at scale ratio four",
  s8113: "What closes is a static candidate family, not the Millennium problem",
  s8114: "Verification",
  s8115: "The value is to upgrade the randomized finite-separation obstruction into an auditable theorem",
  s8116: "Angular reduction",
  s8117: "On \\([1/20,19/20]\\), the cutoff uses the beta\\((3,3)\\) survival function convolved with a normalized standard bump of radius \\(1/40\\). Raw bump moments use a composite-trapezoid primitive, with \\(|(z^kb(z))''|\\le k^2+k+8\\) supplying error bounds for complete cells and arbitrary endpoint fragments alike.",
  s8118: "Exact amplitude algebra writes \\(j=0\\) as",
  s8119: "The radial cutoff writes vorticity as three axisymmetric tensor components. The common \\(SO(3)\\) rotation is integrated by exact sphere moments; after \\(t=n\\cdot m\\) represents relative direction, the angular average is quartic and every apparent \\(\\sqrt{1-t^2}\\) term cancels exactly.",
  s8120: "The decisive margins are \\(-\\sup c_3=\\texttt{__C3_MARGIN__}\\), \\(-\\sup\\Delta=\\texttt{__DISC_MARGIN__}\\), and \\(-\\sup\\mathcal A_{-2}(u_0)=\\texttt{__ENDPOINT_MARGIN__}\\). All three are strictly positive, so the conclusion does not depend on display precision or a subjective judgment that a value is merely close to zero.",
  s8121: "Two coarse annuli rigorously exclude the entire closed amplitude interval",
  s8122: "Let \\(d^2=r^2+s^2-2rst\\); all angular dependence then remains in only five validated distance moments",
  s8123: "Each radial box independently compares third- and fourth-order remainders and uses the tighter rigorous bound",
  s8124: "Every radial box computes two remainders that enclose the same exact box average: a third-derivative bound after total degree two, and a third-degree/fourth-derivative bound using the vanishing of every cubic centered moment. The program takes the smaller one coefficient by coefficient; only the support bands of the sixth-order endpoint distributions receive extra refinement. The exact cubic polynomial in amplitude is propagated throughout, with no sampling of \\(a\\).",
  s8125: "Intervals",
  s8126: "Three coefficients, one discriminant, and one endpoint value all receive rigorous interval certificates. This is a mechanism-exclusion theorem for the declared static family, not a Navier–Stokes regularity result.",
  s8127: "Recompute the discriminant from rational endpoints outside the producer",
  s8128: "Every archived payload is locked by a SHA-256 manifest. The independent verification command, Python and python-flint versions, operating system, and processor information are recorded in the certificate directory; any change is exposed by the automated tests or checksum audit.",
  s8129: "Figure R0.69W. The left panel shows the rigorous full-amplitude envelope of \\(q(a)\\) induced by the coefficient intervals together with the zero line. The right panel shows the certified intervals for \\(c_3\\), the discriminant \\(\\Delta\\), and the endpoint \\(\\mathcal A_{-2}(u_0)\\). Every upper endpoint lies strictly to the left of zero.",
  s8130: "The extended beta survival function is only \\(C^2\\). The producer explicitly includes the \\(\\delta,\\delta',\\delta''\\) endpoint terms in distributional derivatives four through six; the bump second derivative required at order six is then certified by exact Sturm root isolation and Arb evaluation to satisfy \\(|b''|<8\\). Thus no endpoint mass that can be amplified in a boundary layer is omitted.",
  s8131: "Five distance primitives are certified with the composite trapezoid rule and second-derivative error bounds. Because the convolved survival cutoff is nonincreasing, the cutoff range on each distance cell comes from certified second-order interpolation at its two endpoints, rather than repeatedly paying a full cutoff-table-cell width; arbitrary primitive-query endpoints use the same partial-cell rule. Every binary64 operation is",
  s8132: "A five-dimensional signed kernel becomes a two-dimensional radial integral",
  s8133: "widened outward, and accumulation across boxes uses directed one-sided sums.",
  s8134: "Rigorous cubature",
  s8135: "Meaning of rigorous.",
  s8136: "Research note R0.69W · A rigorous interval obstruction at finite two-scale separation",
  s8137: "Research note R0.69W: outward-rounded intervals, exact sphere moments, and validated Taylor cubature rigorously exclude the entire two-scale amplitude family at scale ratio four.",
  s8138: "The one-parameter finite-separation route is closed; the next stage is paused",
  s8139: "One figure presents the full-amplitude envelope and all three strict sign margins",
  s8140: "Consequently there is no \\(a\\in[0,1]\\) for which both audited coarse annuli are nonnegative, and therefore no amplitude in this family for which every relevant annulus is simultaneously nonnegative.",
  s8141: "Source, complete worker certificates, monitoring records, and the figure package are archived together",
  s8142: "Pause point.",
  s8143: "Here, rigorous means that the complete analytic reduction, the true convolved cutoff, distance primitives, radial cubature, and final algebraic decision are all covered by deterministic outer intervals; randomized standard errors are not being treated as a confidence proof.",
  s8144: "True cutoff",
  s8145: "Formal workers: 20",
  s8146: "The formal producer source commit is",
  s8147: "The formal job uses 20 disjoint radial-row workers. Each worker retains a progress NDJSON file, two-second resource samples in CSV, a standard-output log, and a partial result; the combiner aggregates them with outward rounding. The formal wall time is \\texttt{__WALL_TIME__} seconds, accumulated worker time is \\texttt{__CPU_TIME__} seconds, and the observed sum of per-worker peak resident memory is \\texttt{__RSS__} GiB.",
  s8148: "The certificate covers the declared smooth convolution, not a 48-node approximation",
  s8149: "The certificate rigorously proves \\(c_3<0\\) and \\(\\Delta=c_2^2-4c_1c_3<0\\). Therefore the quadratic \\(q\\) has no real root and, because it opens downward, is negative everywhere; in particular, for every \\(a>0\\), \\(\\mathcal A_0(u_a)<0\\).",
  s8150: "Status · R0.69W rigorous certificate, independent verification, and formal figure complete",
  s8151: "Final intervals and margins from zero",
  s8152: "Arb precision: 256 bit",
  s8153: "R0.69V reduced the finite-separation problem to three cubic coefficients and one endpoint value. This version certifies the declared true smooth convolved cutoff with outward rounding: for every \\(0<a\\le1\\), the coarse annulus \\(j=0\\) is strictly negative; at the degenerate endpoint \\(a=0\\), another coarse annulus \\(j=-2\\) is strictly negative. Hence the entire scale-ratio-four one-parameter static family contains no amplitude for which every relevant annulus is simultaneously nonnegative.",
  s8154: "R0.69V rigorously ruled out improving the ratio merely by separating the two scales indefinitely, but scale ratio four was still supported only by randomized computation. R0.69W closes that finite-separation loophole: however the single amplitude is chosen, at least one coarse annulus retains a rigorously negative sign.",
  s8155: "After the R0.69W certificate, figure, web page, and online mirror are complete, the research pauses before entering a new geometry or dynamical stage. No next route is selected automatically here.",
  s8156: "R0.69W rigorous quadratic envelope and interval certificates for the leading coefficient, discriminant, and endpoint annulus",
  s8157: "R0.69W | The entire two-scale amplitude family at scale ratio four is rigorously excluded",
  s8249: "View the complete rigorous certificate",
  s8265: "The entire two-scale amplitude family at scale ratio four is rigorously excluded by two coarse annuli",
  s8293: "Current pause point:",
  s8321: "For the fixed family \\(u_a=aU_1+(1-a)U_{1/4}\\), exact amplitude algebra gives \\[ \\mathcal A_0(u_a)=a(c_1+c_2a+c_3a^2). \\] An outward-rounded certificate for the true smooth convolved cutoff rigorously proves \\(c_3<0\\) and \\(c_2^2-4c_1c_3<0\\), so \\(\\mathcal A_0(u_a)<0\\) simultaneously for every \\(a>0\\); the degenerate endpoint is closed separately by \\(\\mathcal A_{-2}(u_0)<0\\). No amplitude grid is used.",
  s8778: "Download the rigorous interval figure as PDF",
  s8902: "Research note R0.69W · 2026-08-21",
  s9050: "Read research note R0.69W →",
  s9119: "This is a rigorous mechanism-exclusion theorem for the declared static family. It does not propagate a Navier–Stokes solution, control a critical norm, or solve the Millennium problem; it closes one specific one-parameter finite-separation route.",
  s9173: "The certificate first reduces the common rotation to five distance primitives using exact sphere moments, then covers the two-dimensional radial integral with validated trapezoidal primitives and boxwise Taylor remainders. All \\(\\delta,\\delta',\\delta''\\) endpoint terms in cutoff derivatives four through six are retained explicitly; an independent checker parses the result endpoints as exact rationals and recomputes the discriminant. Progress, resource samples, logs, and partial certificates from all 20 DGX workers are archived and locked by SHA-256.",
  s9300: "After the R0.69W certificate, figure, and web publication are complete, pause before entering another geometry or dynamical stage; do not extend the current static family automatically.",
};

const englishById = {};
for (let old = 8090; old <= 8114; old += 1) {
  englishById[`s${old - 1}`] = legacyEnglishById[`s${old}`];
}
for (let old = 8115; old <= 8123; old += 1) {
  englishById[`s${old}`] = legacyEnglishById[`s${old}`];
}
for (let old = 8125; old <= 8157; old += 1) {
  englishById[`s${old - 1}`] = legacyEnglishById[`s${old}`];
}
for (const old of [8249, 8265, 8293, 8321, 8778, 8902, 9050, 9119, 9173, 9300]) {
  englishById[`s${old - 1}`] = legacyEnglishById[`s${old}`];
}
englishById.s8088 = ". The certificate uses 524,288 raw-bump moment cells, 2,048 cutoff-certificate cells, 4,194,304 distance-moment cells, 512 transition radial cells, 128 core cells, and 256 plateau cells.";
englishById.s8096 = "Version v0.69W · 2026-08-24";
englishById.s8114 = "At each radial-box center, cutoff derivatives are expanded through third order from the nearest exact rational node, with the global fourth-derivative bound enclosing the remainder; this result is then intersected with the independent whole-cell derivative range. Box-wide errors still use whole-cell ranges, so midpoint coefficients no longer repeatedly pay an artificial cutoff-cell width without replacing any rigorous enclosure by an uncertified point estimate. Each radial box also compares two bounds for the same exact average: a third-derivative bound after total degree two, and a fourth-derivative bound after using the vanishing of all cubic centered moments. The program takes the tighter bound coefficient by coefficient; only the support bands of the sixth-order endpoint distributions receive extra refinement. The exact cubic amplitude polynomial is propagated throughout, with no sampling of \\(a\\).";
englishById.s8120 = "The decisive margins are \\(-\\sup c_3=\\texttt{0.12489333880250154}\\), \\(-\\sup\\Delta=\\texttt{0.00039732714404764783}\\), and \\(-\\sup\\mathcal A_{-2}(u_0)=\\texttt{0.0019148502803584854}\\). All three are strictly positive, so the conclusion does not depend on display precision or a subjective judgment that a value is merely close to zero.";
englishById.s8130 = "Five distance primitives are certified by the composite trapezoid rule with second-derivative error bounds. Because the convolved survival cutoff is nonincreasing, each distance-cell cutoff range is obtained from certified cubic-Hermite endpoint interpolation with remainder \\(\\|q^{(4)}\\|_\\infty h^4/384\\). Exactly representable dyadic distance nodes remain point intervals, preventing an aligned node from spuriously crossing a cutoff cell; arbitrary primitive-query endpoints use the same validated partial-cell rule. Every inexact binary64 operation is";
englishById.s8146 = "The formal job uses 20 disjoint radial-row workers. Each worker retains a progress NDJSON file, two-second resource samples in CSV, a standard-output log, and a partial result; the combiner aggregates them with outward rounding. The longest worker wall time is \\texttt{1535.665} seconds, accumulated worker time is \\texttt{28877.699} seconds, and the sum of observed per-worker peak resident memory is \\texttt{67.297} GiB.";
englishById.s8901 = "Research note R0.69W · 2026-08-24";

function restoreProtectedTokens(zh, english) {
  const tokens = [
    ...zh.matchAll(/\\\([\s\S]*?\\\)/g),
    ...zh.matchAll(/\\\[[\s\S]*?\\\]/g),
  ].map((match) => match[0]);
  let restored = english;
  for (const token of tokens) {
    if (restored.includes(token)) continue;
    const plain = token.replaceAll("\\", "");
    if (!restored.includes(plain)) {
      throw new Error(`cannot restore protected token ${token} in translation`);
    }
    restored = restored.replace(plain, token);
  }
  return restored;
}

const additions = [];
for (const [id, en] of Object.entries(englishById)) {
  const entry = sourceById.get(id);
  if (!entry) throw new Error(`missing extracted source id ${id}`);
  additions.push({
    ...entry,
    id: `r069w${String(additions.length + 1).padStart(3, "0")}`,
    en: restoreProtectedTokens(entry.zh, en),
  });
}
const replacedChinese = new Set(additions.map((entry) => entry.zh));
const currentChinese = new Set(source.map((entry) => entry.zh));
const merged = [
  ...current.filter(
    (entry) => currentChinese.has(entry.zh) && !replacedChinese.has(entry.zh),
  ),
  ...additions,
];
await writeFile(translationPath, `${JSON.stringify(merged, null, 2)}\n`);
console.log(JSON.stringify({ added: additions.length, total: merged.length }, null, 2));
