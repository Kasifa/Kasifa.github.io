#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074sstep18";

// Local direct translations in deterministic collectSiteStrings order. The
// helper appends every TeX and URL token exactly as it appears in the source.
const summaries = [
  "Retained major route-correction recap (R0.61–R0.74S, 161 sections)", // 001
  "Current endpoint R0.74S Step 18", // 002
  "Await the next explicit frozen package in this same publication task. Possible topics are the direct hybrid gate, the open fixed-deletion and simultaneous-height gates, the open positive-excursion and terminal-crown gates, or another explicit PDE input. Abstract clocks must not be presented as PDE data.", // 003
  "Waiting", // 004
  "The exact hierarchy is moving deletion at most fixed deletion at most separable excursion. After known payments, fixed hybrid and simultaneous height are equivalent at the target scale. The triangular clocks are abstract only; the listed PDE gates and regularity remain open. NOT CLAY.", // 005
  "Next PDE-specific interface", // 006
  "Research note R0.74S Step 18 · 2026-09-03", // 007
  "Review v1.97 · 2026-09-03", // 008
  "The quantifier hierarchy among moving deletion, fixed deletion, and separable maxima is now exact. After known payments, fixed hybrid and completed-clock simultaneous height are equivalent at the target scale. The abstract clocks only block a ledger-only derivation; the two new gates remain open. NOT CLAY.", // 009
  "R0.74S Step 18 fixes the exact temporal quantifier hierarchy: moving deletion at most fixed deletion at most separable excursion. After known payments, fixed hybrid and completed-clock simultaneous height are equivalent at the target scale. The fixed-deletion, simultaneous-height, direct-hybrid, positive-excursion, terminal-crown, Q.12, Q.1, and regularity problems remain open.", // 010
  "R0.74S: fixed deletion, simultaneous height, and the temporal quantifier gap", // 011
  "R0.74S｜Fixed deletion, simultaneous height, and the exact temporal quantifier gap", // 012
  "Step 17 milestone recap", // 013
  "Step 18 separates moving, fixed, and separable deletion orders exactly and proves only target-scale equivalence between fixed hybrid and simultaneous height after known payments. The fixed-deletion, simultaneous-height, direct-hybrid, positive-excursion, and terminal-crown gates remain open. NOT CLAY.", // 014
  "Step 18 journal-grade four-panel figure", // 015
  "Open interface · awaiting frozen package", // 016
  "Possible topics are the direct hybrid gate, the open fixed-deletion and simultaneous-height gates, the open positive-excursion gate, or the open terminal-crown gate. Abstract triangular clocks must not be presented as PDE data.", // 017
  "Literature review v1.97 · 2026-09-03", // 018
  "A bounded two-pass primary-source search checked Dascaliuc–Grujić on signed averaged flux, Yang on skewed-cylinder maximal functions, and Yu on finite-chain bad-scale counting and signed-work depletion. None supplies all quantifiers of S.486: a universal finite deletion budget, one fixed shell set covering every common good terminal time, infinite-shell forward stopped increments, and quadratic payment. A bounded miss is not a novelty, priority, or exhaustiveness claim.", // 019
  "Fixed deletion, simultaneous height, and the exact temporal quantifier gap", // 020
  "PROVED: the hierarchy, layer cake, target-scale comparison, linear fallback, and fixed-R Taylor screen in S.476–S.485 and S.488–S.493. ABSTRACT ONLY: triangular-clock strictness and the failure of a linear ledger to imply a two-thirds-power bound; neither is an NSE counterexample. FINITE: 283,157 Python cases and 72,144 independent Ruby assertions, with every mutation and reproducibility check passing. OPEN: the fixed-deletion, simultaneous-height, direct-hybrid, positive-excursion, terminal-crown, Q.12, Q.1, scale-contraction, and regularity problems. The figure is an analytic schematic and abstract clock test, not PDE data or DNS.", // 021
  "R0.74S Step 18 literature and claim boundary", // 022
  "R0.74S Step 18 public boundary", // 023
  "Step 18 proves the hierarchy moving deletion at most fixed deletion at most separable excursion and compares the fixed hybrid tail with completed-clock simultaneous height in both directions after known payments. Triangular clocks give only an abstract ledger obstruction, not a PDE counterexample; the fixed-deletion, simultaneous-height, and direct-hybrid gates remain open.", // 024
  "Fixed deletion, simultaneous height, and the exact temporal quantifier gap", // 025
  "Research-note master index · v1.97 · 2026-09-03", // 026
  ": they are not spatial fields, do not realize Version-M payment, and are not Navier--Stokes solutions or counterexamples.", // 027
  ": the direct moving-deletion hybrid gate; the route-minimal fixed-deletion gate S.486; the target-scale-equivalent simultaneous-height gate S.487; the Step 17 positive-excursion gate S.472; terminal-crown coercivity S.407; Q.12, Q.1, scale contraction, and regularity.", // 028
  ": the hierarchy and infinite-shell justification in S.476--S.479; the exact layer-cake incidence formulas in S.480; the two-way completed-clock target-scale reduction in S.481--S.485; the unconditional linear fallback in S.488; the exact abstract triangular-clock values in S.489--S.492; and the fixed-R Taylor compatibility screen in S.493.", // 029
  ": the strictness and unbounded reverse ratio in S.491, and the fact in S.492 that the listed ledger assumptions cannot imply a two-thirds-power bound. Neither is an NSE counterexample.", // 030
  ". By S.479 it implies the direct hybrid gate and therefore, through already-proved reductions, Step 10 S.243, Q.12, and Q.1. It is stronger than the direct gate because the direct exceptional set may depend on the terminal time.", // 031
  ". S.483--S.484 prove only target-scale equivalence with S.486, with constants depending solely on the same frozen profile. Both are stronger than the direct moving-deletion gate.", // 032
  "← Step 17: closed-streamline recurrence and the absolute-tail no-go", // 033
  "126. Result and correction: the missing layer is the middle temporal quantifier", // 034
  "127 / Full text", // 035
  "127. Frozen setting and the three deletion orders", // 036
  "128 / Full text", // 037
  "128. Exact hierarchy and layer-cake incidence", // 038
  "129 / Full text", // 039
  "129. Completed-clock simultaneous height and target-scale equivalence", // 040
  "130 / Full text", // 041
  "130. Corrected open targets and the unconditional linear fallback", // 042
  "131 / Full text", // 043
  "131. Exact abstract separation by disjoint triangular clocks", // 044
  "132 / Full text", // 045
  "132. The recurrent Taylor family passes every surviving gate", // 046
  "133 / Full text", // 047
  "133. What a successful PDE theorem must add", // 048
  "134 / Full text", // 049
  "134. Primary-source collision boundary", // 050
  "135 / Full text", // 051
  "135. Claim ledger, certificates, and the strict next boundary", // 052
  "Retain the Step 15 nonnegative stopped-flux vector", // 053
  "Retained Step 17 major route-correction recap", // 054
  "This site stops at frozen R0.74S Step 18. A later frozen package may study the direct hybrid gate, the open fixed-deletion or simultaneous-height gates, the open positive-excursion or terminal-crown gates, or another explicit PDE-specific mechanism. Abstract clocks must not be presented as PDE data, and Q.12, Q.1, regularity, or the Millennium problem must not be stated as a theorem.", // 055
  "The ratio of separable excursion to fixed-deletion height is M minus N and is unbounded for fixed N as M tends to infinity. Thus no universal reverse comparison from the simultaneous functional to the separable coordinatewise maximum exists in the abstract clock class. The tempting choice M equals N plus one separates only moving from fixed deletion and does not make the second inequality strict.", // 056
  "There is no universal reverse comparison from completed-clock simultaneous height to the separable completed-clock maximum; the abstract clocks below give an unbounded separation.", // 057
  "When the payment is at most one, the first bound is already at most the quadratic target scale. When it exceeds one, a one-third-power factor remains. Rearranging only the displayed linear ledger cannot remove that factor.", // 058
  "The first inequality uses only sup-inf at most inf-sup and assumes neither minimax equality nor attainment. The second follows from coordinatewise positive-excursion domination, and the third from total-variation domination. If an infimum is not attained, use an epsilon-minimizer and send epsilon down to zero.", // 059
  "Define the fixed-deletion simultaneous height on a terminal domain", // 060
  "For each positive level, define the terminal-time active set and the coordinatewise-excursion envelope. Layer cake and best-N rearrangement give", // 061
  "For an active hybrid coordinate, clock completion, nonnegativity, and ordering of the hybrid start give", // 062
  "For the exact smooth Step 17 family, first fix a finite deletion budget and then choose and fix the scale as in S.451. With that quantifier order and sufficiently large amplitude,", // 063
  "For a nonnegative summable sequence, the identity used here is", // 064
  "Fix one Version-M suitable weak solution, one admissible scale, one admissible profile, one terminal domain, and one nonnegative integer deletion budget. Let the physical interval and common good-time domain be as displayed. The inherited objects satisfy", // 065
  "Fix integers M greater than N, a positive height, and the unit interval. For each coordinate from one through M, define", // 066
  "The next interface still depends on an open PDE input", // 067
  "Mutually disjoint triangular clocks show that both of the first two hierarchy inequalities can be strict and that coordinatewise maxima can overcount simultaneous height by an arbitrarily large factor. The correct strict example requires at least two undeleted coordinates, not merely one. The same abstract family shows that inherited nonnegativity, Q-variation, and a linear absolute-flux ledger cannot algebraically imply the desired two-thirds-power estimate. This is an abstract information-theoretic obstruction, not a Navier--Stokes counterexample.", // 068
  "The inherited unconditional information is only", // 069
  "The exact reductions leave three nested research targets. The weakest direct hybrid target matches Step 15 exactly. S.486 asks for one common finite shell set while retaining simultaneous terminal incidence. S.487 is the completed-clock target, with the stronger Step 17 positive-excursion bound above it. After known payments, simultaneous height is target-scale equivalent to the fixed hybrid gate, while separable positive excursion still requires extra cross-time information.", // 070
  "Let the known payment be the displayed sum of Q-variation and the profile term, bounded at the target scale. Step 10 S.235 bounds the completed clocks outside the same fixed set at every good terminal time by this payment plus six times the stopped-flux vector. Continuity into the summable sequence space and density of the common good-time set yield the reverse estimate", // 071
  "The target-scale-equivalent completed-clock formulation is", // 072
  "The support interiors are pairwise disjoint, all later coordinates vanish, and the increment has a common zero start. At each time at most one coordinate is positive, while every fixed set deleting fewer than M coordinates misses a peak. Hence", // 073
  "On active coordinates the hybrid start lies between the common start and the terminal time; otherwise the stopped increment is zero. Step 15 proves the vector is nonnegative and summable. Let the admissible deletion sets have cardinality at most N, and define", // 074
  "If one exceptional shell set must work simultaneously for every common good terminal time, the route-minimal successor is", // 075
  "Previous frozen step and the next boundary", // 076
  "Therefore the abstract assumptions of nonnegative completed clocks, flux-plus-Q decomposition, quadratic Q-variation, and a linear total-flux-variation ledger cannot imply a fixed-deletion quadratic bound for any deletion budget fixed in advance. The clock height is an independent parameter. Choosing only M equal to N plus one and height M cubed changes uniformity in N; it does not refute a fixed-N statement.", // 077
  "Thus for a fixed admissible profile and a fixed universal deletion budget, the fixed hybrid bound holds at the target scale if and only if the completed-clock simultaneous-height bound does. This is target-scale equivalence after known payments, not literal equality, and it does not identify either functional with the weaker moving-deletion tail.", // 078
  "All clock sums are finite: the common zero start bounds every completed clock by positive flux excursion plus Q-variation, so the sum of coordinatewise clock suprema is bounded by the two finite variation ledgers.", // 079
  "This differs from the Step 17 separable maximum: simultaneous height places the time supremum outside the shell sum while retaining one deletion set.", // 080
  "In particular, when at least one deletion is allowed and at least two coordinates remain,", // 081
  "For comparison, define", // 082
  "The next frozen package has not been published →", // 083
  "First sort each finite truncation and then use monotone convergence for the infinite sequence. The middle line of S.480 uses Tonelli only after the deletion set and terminal time are fixed; neither optimization passes through the integral.", // 084
  "Research note R0.74S · Step 18 · complete edition", // 085
  "Normalize by the full absolute-flux ledger, which equals twice M times the height. For fixed N and any M greater than N, sending the height to infinity gives", // 086
  "Therefore S.479 and S.485 give", // 087
  "Because each positive flux excursion is bounded by total variation, the excursion sequence is nonnegative and summable, and each stopped increment lies between zero and that excursion. Every series below is dominated by the same summable sequence; no infinite signed sum is interchanged.", // 088
  "A bounded two-pass primary-source search found no theorem with all S.486 quantifiers at once: deterministic suitable weak solutions; one finite shell deletion for each fixed solution, scale, centre, and terminal domain that covers all common good terminal times; an infinite-shell summable sum of forward stopped increments; a universal deletion budget; and quadratic payment.", // 089
  "A signed entrance or collar-flux payment tied to the hybrid first-passage intervals.", // 090
  "Sum outside the same fixed deletion set, take the terminal supremum, and only then optimize, obtaining", // 091
  "Here fixed means only that for each already-fixed solution, scale, centre, and terminal domain, the same shell set is used for every common good terminal time; it may still depend on those fixed data. The hybrid starts are not frozen and retain their terminal-time dependence.", // 092
  "This is a fixed-scale screen, not a proof of universal S.486 or S.487. It only shows that the smooth recurrent family destroying absolute temporal variation is compatible with every surviving quadratic gate: recurrence produces linearly many circuits in amplitude, but all peaks share one phase geometry and signed excursion remains quadratic.", // 093
  "These are adjacent tools and possible ingredients, not proofs of the open gate. The search is bounded, and a miss is not a novelty, priority, or exhaustiveness claim.", // 094
  "These are mechanism classes only, not proved lemmas.", // 095
  "This pinpoints the quantifier gap. The direct gate may change its deletion set after each terminal time is known; the fixed gate requires one set to hit all common good terminal times; the separable excursion gate replaces each time-incidence set by the larger coordinatewise envelope and therefore forgets whether different shell peaks occur only at mutually exclusive times. Only inclusion of the union in that envelope is asserted, not equality.", // 096
  "The formal 25-file four-panel archive passes 39 checks and native verify-only validation. Panel A is an exact schematic of proved inequalities and known-payment links; Panels B--D are exact abstract clocks. Colour, grayscale, and an independent PDF render all pass visual QA. It is not PDE data, DNS, or an NSE simulation, and it proves neither open S.486--S.487 nor the Clay problem.", // 097
  "The direct Step 15 gate takes a terminal supremum after optimizing a deletion set separately at each time. Requiring one exceptional shell set to work for all common good terminal times gives the stronger but still nonseparable fixed-deletion functional. It remains weaker than coordinatewise positive excursion.", // 098
  "Status · R0.74S STEP 18", // 099
  "Finally, after fixing the deletion set, the supremum of the sum is at most the sum of coordinatewise suprema. Together with Step 17 S.475,", // 100
  "The weakest direct target matching the Step 15 route exactly remains a target-scale bound for the moving-deletion hybrid functional with some universal finite deletion budget and constant. It differs from the full residual gate only by the literal factor five in Step 15 S.385.", // 101
  "Completed-clock simultaneous height controls the fixed-set hybrid tail after paying the already-controlled Q-variation once. Conversely, the Step 10 paid-branch inequality controls simultaneous height by the fixed hybrid tail plus known target-scale payments. The two are therefore equivalent only at the target scale, not literally equal, and neither equals the weaker moving-deletion gate.", // 102
  "Dascaliuc--Grujić's physical-scale energy-cascade and flux-locality results give signed time- and ensemble-averaged flux estimates under inertial-range conditions, not a terminal-time maximum with one shell deletion.", // 103
  "A deterministic stopping-time or Carleson charge controlling the time--shell incidence sets in S.480;", // 104
  "After known payments, fixed deletion and completed-clock simultaneous height are equivalent at the target scale. Triangular clocks separate the moving, fixed, and separable temporal quantifiers exactly; S.486–S.487 remain open.", // 105
  "Fixed-deletion main text", // 106
  "Fixed-deletion functionals and the temporal quantifier gap", // 107
  "The minimax inequality and coordinatewise domination give directly", // 108
  "NEXT / Awaiting an explicit frozen package", // 109
  "Panel A shows proved inequalities and known-payment links; Panels B–D show exact abstract clocks. ANALYTIC SCHEMATIC / ABSTRACT CLOCK TEST / NOT PDE DATA / NOT DNS / NOT CLAY.", // 110
  "Persistence or dwell time, forcing a high clock aggregate to occupy enough parabolic time to be paid by the cubic ledger;", // 111
  "Python script", // 112
  "The primary Python certificate passes 5/5 exact finite groups, 283,157 rational cases, 5/5 structural groups, and 5/5 hash locks. The independent Ruby verifier passes 8/8 groups and 72,144 assertions. Python and Ruby reject 12/12 and 13/13 intentional mutations respectively; three Python hash seeds and one cross-directory Ruby replay are byte-identical.", // 113
  "Python: 5/5 finite groups, 283,157 cases, 5/5 structural groups, and 5/5 hash locks. Independent Ruby: 8/8 groups and 72,144 assertions. Python and Ruby reject 12/12 and 13/13 intentional mutations respectively. Finite certificates do not replace the continuum proof.", // 114
  "The route decision is now exact. Further fixed-deletion work should target the fixed hybrid functional directly and should not automatically strengthen it to separable positive excursion. Completed-clock work may target the simultaneous-height functional that is equivalent after paid terms. The weakest viable route remains the direct Step 15 hybrid gate with a terminal-dependent deletion set. This site stops at frozen Step 18 and awaits the next explicit frozen package.", // 115
  "S.476–S.485 and S.488–S.493 are PROVED; the triangular clocks are ABSTRACT only; the fixed-deletion, simultaneous-height, direct-hybrid, positive-excursion, terminal-crown, Q.12, Q.1, and regularity problems remain OPEN. NOT CLAY.", // 116
  "S.486 is", // 117
  "S.487 is likewise", // 118
  "S.489--S.492 are all", // 119
  "The recurrent smooth Taylor family from Step 17 refutes none of the surviving gates. After the deletion budget is fixed and the scale is fixed as in S.451, it merely saturates positive excursion at quadratic scale while continuing to refute the discarded absolute-variation route. This section is a rigorous route reduction and correction; it proves neither the fixed-deletion nor direct-hybrid gate, Q.12, Q.1, scale contraction, or regularity.", // 120
  "Step 17 proved every sublinear power estimate for the absolute temporal-variation tail false and retained coordinatewise positive excursion as a sufficient signed successor. But that functional takes a separate time supremum for each shell before summing, whereas the actual Step 15 residual gate fixes one terminal time first. Step 18 supplies the missing fixed-deletion functional between them and separates all three quantifier orders exactly.", // 121
  "Step 18 separates moving deletion, fixed deletion, and separable coordinatewise maxima exactly and proves that the fixed hybrid tail and completed-clock simultaneous height are equivalent at the target scale after known payments.", // 122
  "Step 18 Chinese reader source", // 123
  "Step 18 main text, audits, two independent certificate implementations, and QA", // 124
  "The triangular clocks prove that a new input cannot consist only of nonnegativity and inherited linear ledgers. A viable theorem must add a genuinely PDE-specific mechanism, for example:", // 125
  "Yang's maximal functions over flow-generated skewed cylinders satisfy weak-(1,1) and strong-(p,p) bounds for space-time averages, but do not control simultaneous clock height or a fixed best-N terminal functional.", // 126
  "Yu's coarse-grained pressure-flux work depletion gives exact signed-work depletion on a fixed finite chain and explicitly retains negative work or backscatter. It claims neither smallness of the negative set, uniform moving-window constants, nor summability as chain length tends to infinity.", // 127
  "Yu's finite-chain CKN bad-scale counting uses nonnegative channel costs on a prescribed finite scale chain to obtain at least one CKN-small scale; it does not give the infinite-shell, all-good-terminal S.486.", // 128
];

assert.equal(summaries.length, 128, "R0.74S Step 18 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.74S Step 18 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.74S Step 18 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.74S Step 18 source-string count drift");
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
  release: "R0.74S Step 18",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
