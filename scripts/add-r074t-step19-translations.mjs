#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074tstep19";

// Local direct translations in deterministic collectSiteStrings order. The
// helper appends every TeX and URL token exactly as it appears in the source.
const summaries = [
  "Master index of 222 research notes", // 001
  "Retained previous major route-correction recap (R0.61–R0.74S, 161 sections)", // 002
  "View the R0.74T card on the home page", // 003
  "Current endpoint R0.74T Step 19", // 004
  "Await the next explicit frozen package in this same publication task. Possible topics are genuinely exponentially short maximal residence, off-target clocks, full completed-clock payment, or a K-to-Hfix bridge. A lower witness must not be presented as a full upper bound.", // 005
  "Previous milestone recap", // 006
  "Jump to the R0.74T card on the home page →", // 007
  "Research note R0.74T Step 19 · 2026-09-03", // 008
  "Read the latest R0.74T research note →", // 009
  "Expand 132 public notes", // 010
  "Review v1.98 · 2026-09-03", // 011
  "A persistent outer lobe forces the exact cubic payment. Two disjoint R-cubed windows can be realized by one exact common-shear solution, but ordinary dwell cannot escape the exponential payment barrier. The full completed clock and K-to-Hfix bridge remain OPEN. NOT CLAY.", // 011
  "A persistent outer lobe forces cubic payment through the exact Hölder constant; ordinary R-cubed dwell therefore cannot become cheap merely by staggering peaks. Two disjoint windows give only a K-clock witness, not a full clock upper bound. NOT CLAY.", // 012
  "The cumulative recap after R0.60 contains 161 nodes; the site now has 222 public research notes", // 013
  "R0.70A–R0.74T · 124 sections published", // 014
  "R0.70A–R0.74T: 124 sections published, 99 fully archived", // 015
  "R0.74T Step 19 proves schedule-invariant outer-lobe Hölder coercivity and the adjacent-shell exponential dwell ceiling. Two disjoint R-cubed windows can be realized in one exact common-shear solution, but the full completed-clock upper bound, K-to-Hfix bridge, Q.12, Q.1, and regularity remain OPEN.", // 016
  "R0.74T: staggered outer-lobe Hölder coercivity and the exponential dwell barrier", // 017
  "R0.74T｜Hölder-forced payment and the exponential residence barrier for staggered outer lobes", // 018
  "Step 19 journal-grade four-panel figure", // 019
  "Step 19 proves that a persistent outer-lobe kinetic floor forces exact cubic payment and compresses the inherited adjacent-shell low-payment escape to exponentially short dwell. Two disjoint R-cubed windows can be realized in one exact common-shear solution, but they give only a K-clock fixed-deletion witness; the full clock and Hfix bridge remain OPEN.", // 020
  "Possible topics are genuinely exponentially short maximal residence, off-target clocks, full completed-clock payment, or a K-to-Hfix bridge. A lower witness must not be promoted to a full upper bound.", // 021
  "A bounded two-pass primary-source search checked exact shearing-wave superposition, the classical 2D3C split, scalar dispersion under periodic shear, forced passive-scalar blocks and time schedules, and physical-shell flux locality. None of the six screened sources simultaneously provides independently selectable lobe windows in one unforced common-shear solution, a total-field floor, positive weighted cubic payment, a disjoint-time K-clock witness, and the inherited exponential dwell threshold. This is only a six-source non-hit, not a novelty, priority, or exhaustiveness claim.", // 022
  "Previous milestone recap", // 024
  "Literature review v1.98 · 2026-09-03", // 023
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.74T work only as research notes. I do not extrapolate computations or notes into a regularity theorem.", // 024
  "PROVED: exact outer-lobe coercivity in T.9–T.10; the K-clock one-deletion witness in T.17; the dwell identity and necessary exponential ceiling in T.24–T.29; and two disjoint windows in the same exact common-shear solution in T.34–T.43. FINITE: 18,933 Python cases and 9,201 independent Ruby assertions, with all mutation and reproducibility checks passing. OPEN: the full completed-clock upper bound, off-target clocks, K-to-Hfix bridge, fixed deletion, direct hybrid, Q.12, Q.1, scale contraction, regularity, and singularity. The figure is an analytic schematic with derived analytic values, not PDE data or DNS.", // 025
  "R0.74T Step 19 literature and claim boundary", // 026
  "R0.74T Step 19 public boundary", // 027
  "Schedule-invariant lobe coercivity and the exponential dwell barrier", // 028
  "Step 19 proves that an outer-lobe kinetic floor forces cubic payment through classical Hölder and derives a necessary exponential dwell ceiling in the inherited adjacent-shell window. Two disjoint R-cubed windows exist in the same exact common-shear solution, but give only a K-clock witness; the full clock and Hfix bridge remain OPEN.", // 029
  "222 public research notes; latest node R0.74T.", // 030
  "Hölder-forced payment and the exponential residence barrier for staggered outer lobes", // 031
  "Research-note master index · v1.98 · 2026-09-03", // 032
  "Latest node R0.74T · continuously revised", // 033
  "When theta equals one, this is exactly R0.74Q (Q.168). The key clarification is that the coercive step needs only the outer lobe and does not require it to occur simultaneously with other targets.", // 034
  "← Step 18: fixed deletion and simultaneous height", // 035
  "136 / Full text", // 036
  "137 / Full text", // 037
  "138 / Full text", // 038
  "139 / Full text", // 039
  "140 / Full text", // 040
  "141 / Full text", // 041
  "142 / Full text", // 042
  "143 / Full text", // 043
  "144 / Full text", // 044
  "145 / Full text", // 045
  "Restrict the nonnegative integral in T.1 to the moving lobe, then apply the weight floor and lobe measure to obtain the core Step 19 estimate", // 046
  "Retained previous major route-correction recap", // 047
  "This bounded two-pass search checked only six groups of primary sources: Singh–Sridhar; Biferale–Buzzicotti–Linkmann; Jiménez–Urias–Haine; Bruè–De Lellis; Bruè–Colombo–Crippa–De Lellis–Sorella; and Dascaliuc–Grujić.", // 048
  "This section is a local coercivity theorem and route reduction, not a full-clock theorem and still less a solution of the Millennium problem. NOT CLAY.", // 049
  "This section proves four points: an outer lobe persisting for theta R-cubed produces exact Hölder coercivity; any two positive K-clock floors, even at disjoint times, give only a fixed-deletion completed-clock witness; under the inherited adjacent-shell parameters, low payment forces normalized dwell to collapse exponentially; and one exact smooth periodic unforced common-shear Navier–Stokes solution can indeed realize two disjoint R-cubed lobe windows, but its payment-to-witness ratio diverges.", // 050
  "This site stops at R0.74T Step 19. A later frozen package may study scheduling outside the stated slab, genuinely exponentially short maximal comparable-floor residence, full completed-clock payment, off-target clocks, or a K-to-Hfix bridge. This section's lower witness must not be presented as a full-clock upper bound or as a theorem on regularity, singularity, or Clay.", // 051
  "No overlap between the two time sets is required. Every deletion set of size at most one leaves at least one of the two coordinates. Evaluate that coordinate on its own target-time set and use nonnegativity of all clocks to obtain", // 052
  "A persistent outer-lobe kinetic floor forces payment through the exact Hölder constant; low payment in adjacent shells therefore forces normalized dwell to collapse exponentially.", // 053
  "The answer is negative only at the explicitly stated lobe-floor level: if the inherited outer-lobe geometry and nonnegligible residence time are retained, a positive lower bound for outer-lobe kinetic energy is forced to pay through the nonnegative velocity-cubic payment. The conclusion does not require the inner and outer lobes to occur simultaneously.", // 054
  "Substitution of Lambda two gives the exact identity", // 055
  "Substitution into T.9 recovers the amplitude formula for arbitrary normalized dwell", // 056
  "Substitution of the frozen lobe volume and kinetic normalization gives", // 057
  "When R is less than one third, choose", // 058
  "Equivalently, let", // 059
  "The equivalent logarithmic form is", // 060
  "Define the persistent normalized lobe kinetic floor", // 061
  "Define the corresponding horizontal recentering", // 062
  "Frozen Version-M setting and persistent outer-lobe floor", // 063
  "Frozen handoff ledger", // 064
  "Both lie in the terminal slab, and their separation is exactly R-squared minus three R-cubed, which is positive. They are two genuinely disjoint R-cubed-long lobe windows in the same common-shear solution.", // 065
  "For the outer target shell, write", // 066
  "Fix a positive scale, a terminal time, and a smooth periodic unforced Navier–Stokes solution in the R0.74P Version-M setting. The full payment contains the nonnegative exterior velocity row", // 067
  "Hold the instantaneous height fixed and send theta to zero. The cubic payment then vanishes linearly with theta, showing that a peak-only estimate cannot replace a persistence input. These rectangles are ABSTRACT SHARPNESS TESTS: they are not periodic divergence-free solutions, do not realize the Version-M ledger, and are not Navier–Stokes counterexamples.", // 068
  "Disjoint triangular clocks show that different shells can in principle peak at different times. Step 19 asks the narrower question: can staggering only the two packet-lobe target times make the completed-clock witness cheap relative to the Version-M payment?", // 069
  "This is the theta-equals-one lobe interval inherited from R0.74F/R0.74Q. A moving inner lobe does not enter T.24 and cannot alter the conclusion. A genuine escape must make maximal comparable-floor persistence itself exponentially short, not merely truncate in the analysis a lobe that already persists much longer.", // 070
  "The inherited shear-error, heat-age reserve, inversion-suppression, vertical cross-tail, and annular margins hold uniformly at both admissible target times. In particular, each time set carries its target lobe, and", // 071
  "The search found no theorem containing all six ingredients at once: multiple passive packets in one exact common-shear unforced solution; independently selectable target windows in the stated slab; a uniform total-field physical lobe floor; conversion into nonnegative weighted exterior velocity-cubic payment; a completed-clock fixed-deletion floor despite disjoint time windows; and the exponential dwell threshold from the inherited shell weight and survival window.", // 072
  "Result and exact scope: staggering peaks does not eliminate payment for ordinary residence", // 073
  "The spatial Hölder inequality gives", // 074
  "Two strictly separated unit-dwell windows remain expensive", // 075
  "Two K-clock floors at possibly different times: only a one-deletion witness follows", // 076
  "Let the two shell indices be distinct, and on arbitrary measurable positive-measure subsets of the terminal domain assume", // 077
  "Taking the displayed weight and volume constants recovers T.9 exactly.", // 078
  "Choose a measurable outer time set inside the inner terminal slabs with measure theta R-cubed. For almost every time in this set, assume that the moving lobe is jointly measurable and satisfies", // 079
  "The outer interval nevertheless still has unit normalized dwell, so T.24–T.26 give", // 080
  "This remains the same exact smooth periodic mean-zero unforced Navier–Stokes solution. It is not a sum of two independently evolved solutions under different shears.", // 081
  "If the outer floor is at least the reference height, T.10 further gives", // 082
  "If only the general weight floor and lobe-volume bound are known, the same proof gives", // 083
  "Previous recap PDF", // 084
  "Thus Lambda two diverges when theta equals one. More generally, keeping the payment-to-height ratio bounded first forces Lambda two to remain bounded by T.18, which then yields the necessary dwell ceiling", // 085
  "Likewise, the completed clock in T.17 cannot be replaced by Step 18's stopped forward-flux functional. The proved bridge between them must retain the Step 18 payment terms and its original direction.", // 086
  "The same exact common-shear solution can realize two disjoint R-cubed windows, but this gives only a K-clock fixed-deletion witness, not a full clock upper bound, and cannot be replaced by Hfix. NOT CLAY.", // 087
  "Asynchronous lobe construction in the same exact common-shear solution", // 088
  "The next testable route must genuinely construct exponentially short maximal outer comparable-floor persistence, with no comparable floor on a longer interval, or abandon an inherited shell-weight, survival, or lobe-floor assumption. Merely changing the order of two ordinary R-cubed-long lobes, or truncating them in the analysis, is no longer a viable escape route.", // 089
  "Along a sequence with the inner shell parameter tending to infinity, use the inherited adjacent-shell parameters", // 090
  "Along the preceding sequence, also retain the central-chart and common-shear platform conditions, together with the stated small-error limit.", // 091
  "Research note R0.74T · Step 19 · complete Chinese edition", // 092
  "Bounded primary-literature non-hit boundary", // 093
  "Because the defect-completed clock is the sum of a nonnegative endpoint kinetic-energy term and accumulated dissipation, and because the time cutoff equals one on the outer time set, the outer completed clock is at least the outer floor almost everywhere.", // 094
  "Hence each recentering vanishes at its selected terminal time and is bounded on its time set. Horizontal translation commutes with the common scalar advection–diffusion equation, the inversion partner preserves exact odd symmetry, and therefore the finite sum", // 095
  "In the exact common-shear packet family, all-lobe dominance gives the stated velocity lower bound, hence", // 096
  "Choose normalized dwell parameters and terminal times in the stated terminal slab so that", // 097
  "This construction proves that asynchronous clock floors can be realized, but cannot turn those floors into a low-payment witness. It excludes only the explicit mechanism of ordinary R-cubed residence plus staggering, not every possible asynchronous PDE construction.", // 098
  "The conclusion may be stated only as a bounded six-source non-hit. It proves no novelty, priority, correctness, optimality, or publishability, and does not exhaust MathSciNet, zbMATH, the full citation graph, theses, non-English sources, or unpublished material. LITERATURE BOUNDARY.", // 099
  "The conclusion permits selection only of a relative schedule inside the stated slab. It is neither an independent time translation of an already evolved solution nor a theorem for arbitrary real target times.", // 100
  "There is no full completed-clock upper bound here, no replacement of K by Hfix, no arbitrary-real-time scheduling theorem, and no regularity or singularity conclusion. NOT CLAY.", // 101
  "The two displayed bounds are one-sided only. The reference height is a lower-bound witness for the fixed-deletion K-clock functional; other times, shells, or accumulated dissipation may make the full functional larger. Therefore T.18 cannot be rewritten as a lower bound for payment in terms of the full functional.", // 102
  "The proof contains no inner packet, inner-lobe target time, or overlap of the two target intervals. Thus the estimate is invariant under the relative schedule whenever the outer-lobe hypotheses remain valid.", // 103
  "Exponential dwell threshold", // 104
  "The exponential margin is strictly positive:", // 105
  "Status · R0.74T STEP 19", // 106
  "Claim ledger, certificates, and the next boundary", // 107
  "FIGURE: 25 files, 47 checks, and 18/18 deterministic-core hashes. ANALYTIC SCHEMATIC / DERIVED ANALYTIC VALUES / NOT PDE DATA / NOT DNS / NOT CLAY.", // 108
  "FINITE COMPUTATION: Python passes 31/31 groups and 18,933 cases; independent Ruby passes 11/11 groups and 9,201 assertions; Python and Ruby reject 26/26 and 27/27 mutations respectively; three PYTHONHASHSEED runs and an independent Ruby regeneration are byte-identical.", // 109
  "The full clock and intrinsic short residence remain open interfaces", // 110
  "Hölder itself and restriction of a nonnegative integral to a measurable subset are classical measure-theoretic facts and carry no novelty claim. The 2D3C/passive-component reduction, parallel Kelvin waves, scalar dispersion under prescribed periodic shear, forced passive-scalar mixing blocks, alternating-shear time schedules, and physical-shell flux locality must likewise be attributed to the corresponding literature as established mechanisms.", // 111
  "INHERITED: the Version-M payment, shell weights, exact common-shear finite-packet solution, R0.74F/R0.74Q lobe placement, and the sufficient bridge-survival proof window.", // 112
  "OPEN: scheduling outside the stated slab; a PDE construction with exponentially short maximal comparable-floor persistence; a payment-scale upper bound for the full fixed-deletion K-clock functional; off-target clocks and accumulated dissipation; a K-to-Hfix bridge without the Step 18 payment terms; fixed deletion, direct hybrid, Q.12, Q.1, scale contraction, regularity, and singularity.", // 113
  "Packet-amplitude recovery and abstract sharpness", // 114
  "Panels A–B show the exact schedule and Hölder coefficient; Panels C–D show the derived analytic path. ANALYTIC SCHEMATIC / DERIVED ANALYTIC VALUES / NOT PDE DATA / NOT DNS / NOT CLAY.", // 115
  "PROVED: two disjoint admissible lobe windows in the same exact common-shear solution, T.34–T.43.", // 116
  "PROVED: the two-clock completed-height witness in T.17; the object is strictly the K-clock, not stopped flux.", // 117
  "PROVED: the logarithmic dwell identity and necessary collapse threshold in T.24–T.29, with every exponent sharp within the measure-theoretic class.", // 118
  "PROVED: exact outer-lobe Hölder coercivity in T.9–T.10 and invariance under the relative target-time schedule while the lobe hypotheses remain valid.", // 119
  "Python: 31/31 groups and 18,933 cases; independent Ruby: 11/11 groups and 9,201 assertions. Python and Ruby reject 26/26 and 27/27 intentional mutations respectively; finite certificates do not replace the continuum PDE proof.", // 120
  "The inherited sufficient bridge-survival window from R0.74F is the stated negative-exponent limit. It is only sufficient for that proof, not necessary for every packet. Write", // 121
  "The physical lobe in R0.74Q lies in the adjacent annulus, so throughout that region", // 122
  "Schedule-invariant lobe coercivity and dwell barrier", // 123
  "Step 18 reduces the fixed-deletion route to completed-clock simultaneous height", // 124
  "Step 19 main text", // 125
  "Step 19 main text, audits, two independent certificate implementations, and QA", // 126
  "Every exponent in T.9 is sharp under the purely measure-theoretic hypotheses. Take a space-time rectangle on which lobe volume, duration, and shell weight are fixed and the vector field is constant. Spatial Hölder is then an equality and gives exactly", // 127
];

assert.equal(summaries.length, 129, "R0.74T Step 19 translation table length drift");

function withProtected(summary, source) {
  const tokens = extractProtectedTokens(source);
  return tokens.length === 0 ? summary : `${summary} ${tokens.join(" ")}`;
}

process.chdir(root);
const [source, order, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  collectSiteStrings("./public"),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const rowPattern = new RegExp(`^${prefix}\\d+$`);
const baseCurrent = checkOnly ? current : current.filter((row) => !rowPattern.test(row.id));
const currentByZh = new Map(baseCurrent.map((entry) => [entry.zh, entry]));
const missing = source.filter((entry) => !currentByZh.has(entry.zh));
const missingOrder = order.filter((entry) => !currentByZh.has(entry.zh));

if (checkOnly) {
  assert.equal(missing.length, 0, "site still has untranslated Chinese strings");
  const rows = current.filter((row) => rowPattern.test(row.id));
  assert.equal(rows.length, summaries.length, "R0.74T Step 19 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.74T Step 19 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.74T Step 19 source-string count drift");
  const sourceByZh = new Map(missing.map((entry) => [entry.zh, entry]));
  const additions = missingOrder.map((orderedEntry, index) => {
    const entry = sourceByZh.get(orderedEntry.zh);
    assert.ok(entry, `absolute source entry missing ${orderedEntry.zh}`);
    const en = withProtected(summaries[index], entry.zh);
    assert.ok(!containsChinese(en), `Chinese remains in translation ${index + 1}`);
    assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(entry.zh), `protected token drift ${index + 1}`);
    return { id: `${prefix}${String(index + 1).padStart(3, "0")}`, ...entry, en };
  });
  await writeFile(translationPath, `${JSON.stringify([...baseCurrent, ...additions], null, 2)}\n`);
}

process.stdout.write(`${JSON.stringify({
  release: "R0.74T Step 19",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
