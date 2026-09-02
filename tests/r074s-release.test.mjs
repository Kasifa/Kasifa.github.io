import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, statSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const readBytes = (path) => readFileSync(resolve(root, path));
const read = (path) => readBytes(path).toString("utf8");
const sha = (path) => createHash("sha256").update(readBytes(path)).digest("hex");
const node = process.env.CODEX_NODE || process.execPath;

test("R0.74S publication accounting advances without recap drift", () => {
  assert.deepEqual(JSON.parse(read("public/site-version.json")), { schemaVersion: "research-site-version-v1", version: "1.92", latestRelease: "R0.74S", latestPublishedResearchHtml: "/notes/r0-74s.html", latestPublishedResearchPdf: "/notes/r0-74s.pdf", publicHtmlNoteCount: 221, postR060PublishedNodeCount: 161, postR060RecapNodeCount: 157, latestRecapRelease: "R0.74O", publicPdfNoteCount: 178, publishedDate: "2026-09-03" });
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r074s");
  assert.equal(manifest.nextRelease, "r074t");
  assert.equal(manifest.postR070APublishedReleaseCount, 123);
  assert.equal(manifest.postR070AFormalSealedReleaseCount, 98);
  assert.equal(manifest.formalFigureExemptReleaseCount, 1);
  assert.equal(manifest.latestRecapRelease, "r074o");
  assert.equal(manifest.latestPublishedResearchHtml, "/notes/r0-74s.html");
  assert.equal(manifest.latestPublishedResearchPdf, "/notes/r0-74s.pdf");
  assert.equal(manifest.latestReleaseGate, "tests/r074s-ball-clock-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r074s-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r074s-pdf.mjs");
  assert.equal(manifest.latestReleaseTranslationScript, "scripts/add-r074s-translations.mjs");
  assert.equal(sha("public/recap-r0-61-r0-74o.html"), "d06c9edb093664c9835feb814a11ecd180305780b3efcdcd560908f754fba4b2");
  assert.equal(sha("public/recap-r0-61-r0-74o.pdf"), "80264dab72ca12569252a360d9b70388ba0c4b107132012b98d73b76d634d076");
});

test("R0.74S reader is complete Chinese and preserves every claim boundary", () => {
  const note = read("public/notes/r0-74s.html");
  for (const marker of [
    "一侧 ball cutoff 与 flux 符号恒等式", "四通道 signed recombination", "三通道 genealogy cutoff 非负",
    "PROVED ABSTRACT SCALAR NO-GO", "这个见证没有空间算子或 PDE 实现", "真实 NSE solution family", "PDE-weighted block length", "完整中文版本",
    "S.307–S.342：PROVED / CONDITIONAL / ABSTRACT / OPEN", "fixed-solution sum：PROVED", "linear ceiling：\\(&gt;2/3\\)",
    "S.342：OPEN", "31/31 exact", "22/22 structural", "32/32 negative", "72,027 cases",
    "ABSTRACT BOUNDARY TESTS, NOT NSE COUNTEREXAMPLES", "不是 universal PDE no-go", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 18000, "reader UTF-8 payload is unexpectedly short");
  assert.ok(!note.includes("独立数学审计尚未完成"));
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
  for (const path of ["public/notes/r0-74s.pdf", "research/r074s_note_pdf_render.json", "research/r074s_pdf_bindings.json"]) assert.ok(statSync(resolve(root, path)).size > 0, path);
  const binding = JSON.parse(read("research/r074s_pdf_bindings.json"));
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74s.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74s.pdf"));
  assert.ok(binding.publicPdf.pageCount >= 9);
  assert.equal(binding.claimBoundary.oneSidedBallClocks, "PROVED");
  assert.equal(binding.claimBoundary.stoppedOrientations, "PROVED");
  assert.equal(binding.claimBoundary.terminalAbelIdentity, "PROVED");
  assert.equal(binding.claimBoundary.fullSignedRecombination, "PROVED_CIRCULAR");
  assert.equal(binding.claimBoundary.threeChannelTemporalDebtCancellation, "PROVED");
  assert.equal(binding.claimBoundary.terminalL1Decomposition, "PROVED");
  assert.equal(binding.claimBoundary.unweightedGenealogyObstruction, "PROVED_ABSTRACT_SCALAR_NO_GO");
  assert.equal(binding.claimBoundary.lowHighRayleighTimeSplit, "PROVED");
  assert.equal(binding.claimBoundary.dissipationPriorityTrichotomy, "PROVED");
  assert.equal(binding.claimBoundary.lowRayleighAllShellPayment, "PROVED");
  assert.equal(binding.claimBoundary.rayleighExcessMeasures, "PROVED");
  assert.equal(binding.claimBoundary.scalarAndJordanExcessTiers, "PROVED_DISTINCT");
  assert.equal(binding.claimBoundary.highRayleighScalarResidual, "UNIFIED_WITH_EXISTING_STOPPED_WORK_GATE");
  assert.equal(binding.claimBoundary.anomalousDefectScalarResidual, "UNIFIED_WITH_EXISTING_STOPPED_WORK_GATE");
  assert.equal(binding.claimBoundary.stoppedWorkFullFluxEquivalence, "PROVED_WITHIN_PAID_B_Q");
  assert.equal(binding.claimBoundary.universalNoExceptionQuadraticAntecedent, "REFUTED_BY_INHERITED_SMOOTH_EXACT_NSE_FAMILY");
  assert.equal(binding.claimBoundary.conditionalS38Implication, "PROVED_RETAINED");
  assert.equal(binding.claimBoundary.signedFHalfExit, "PROVED_EXACT_ONE_HALF_BEST_N_TAIL");
  assert.equal(binding.claimBoundary.signedFHalfExitS25Admissibility, false);
  assert.equal(binding.claimBoundary.kThetaLastExit, "PROVED_WITH_SHARP_ONE_B_Q_ERROR");
  assert.equal(binding.claimBoundary.canonicalLastExitQuadraticCompression, "REFUTED_PROVED_NO_GAIN_EQUIVALENCE");
  assert.equal(binding.claimBoundary.fullTerminalBestNTail, "OPEN_Q12");
  assert.equal(binding.claimBoundary.plateauBestNTail, "OPEN_WEAKER_RESTRICTION");
  assert.equal(binding.claimBoundary.fixedBestNTerminalExceptionEstimate, "OPEN_NEXT_PDE_TARGET");
  assert.equal(binding.claimBoundary.sixClassPaidResidualPartition, "PROVED_D_FIRST_EXACT_PARTITION");
  assert.equal(binding.claimBoundary.lowRayleighExtraResidualClass, false);
  assert.equal(binding.claimBoundary.oneQPaidLedger, "PROVED_SINGLE_6_B_Q");
  assert.equal(binding.claimBoundary.oneCubicPaidLedger, "PROVED_SINGLE_C5_LEDGER");
  assert.deepEqual(binding.claimBoundary.residualClasses, ["R_sh", "R_x"]);
  assert.equal(binding.claimBoundary.residualTwoSidedComparability, "PROVED_T_OVER_6_LT_R_LT_T_OVER_2");
  assert.equal(binding.claimBoundary.residualBestNReduction, "PROVED_DOMAIN_SAFE");
  assert.equal(binding.claimBoundary.separateResidualExceptionBudgets, false);
  assert.equal(binding.claimBoundary.terminalDDominanceLastExitPersistence, false);
  assert.equal(binding.claimBoundary.paidBranchResidualTail, "PROVED_DEFINED_AND_REDUCED_PACKING_OPEN");
  assert.equal(binding.claimBoundary.fixedUniversalN0ResidualEstimate, "OPEN_S243");
  assert.equal(binding.claimBoundary.finiteExceptionConsequence, "PROVED_CONDITIONAL_IMPLICATION_ONLY");
  assert.equal(binding.claimBoundary.sharedBudgetPointwiseInfimalConvolution, "PROVED_EXACT_S249");
  assert.equal(binding.claimBoundary.terminalSupremumBudgetMinimumCommutation, false);
  assert.equal(binding.claimBoundary.sharedBudgetDomainInequality, "PROVED_S250");
  assert.equal(binding.claimBoundary.addedBranchExceptionCounts, "PROVED_CONDITIONAL_S251");
  assert.equal(binding.claimBoundary.duplicateBranchBudgets, false);
  assert.equal(binding.claimBoundary.shortBranchInverseDuration, "PROVED_S253_S254");
  assert.equal(binding.claimBoundary.criticalQuadraticCarlesonEndpoint, "REFUTED_AT_COEFFICIENT_CLOCK_LEVEL_LOG_GAP");
  assert.equal(binding.claimBoundary.criticalCarlesonWitnessIsNseCounterexample, false);
  assert.equal(binding.claimBoundary.nestedTentEstimate, "PROVED_S258");
  assert.equal(binding.claimBoundary.positiveBackwardDepthControl, "PROVED_S259");
  assert.equal(binding.claimBoundary.depthZeroTerminalTrace, "OPEN_S261");
  assert.equal(binding.claimBoundary.scalarExcessResidualBestNComparison, "PROVED_CONSTANTS_ONE_FIFTH_AND_THREE");
  assert.equal(binding.claimBoundary.fixedSolutionTailTightness, "PROVED_NONUNIFORM_S265");
  assert.equal(binding.claimBoundary.fixedSolutionTightnessGivesUniversalN, false);
  assert.equal(binding.claimBoundary.lastExitAncestryLocalization, false);
  assert.equal(binding.claimBoundary.ancestryFixturesAreNseCounterexamples, false);
  assert.equal(binding.claimBoundary.uniformSelectedExcessPacking, "OPEN_S269");
  assert.equal(binding.claimBoundary.nPlusOneTargetFalsificationCriterion, "PROVED_CONDITIONAL_S270");
  assert.equal(binding.claimBoundary.existingMultiPacketFamiliesRefuteFixedPositiveN, false);
  assert.equal(binding.claimBoundary.combinedTwoBranchEstimate, "OPEN_S272");
  assert.equal(binding.claimBoundary.commonTerminalWindowDefinition, "PROVED_S273");
  assert.equal(binding.claimBoundary.commonWindowShortResidualReduction, "PROVED_S274_S275");
  assert.equal(binding.claimBoundary.commonWindowTerminalContinuity, "PROVED_S276");
  assert.equal(binding.claimBoundary.fixedSolutionWindowModulus, "PROVED_NONUNIFORM_S277");
  assert.equal(binding.claimBoundary.bestNLayerCakeIdentity, "PROVED_S278");
  assert.equal(binding.claimBoundary.universalTerminalWindowGate, "OPEN_S280");
  assert.equal(binding.claimBoundary.l1OnlyWindowEstimate, "REFUTED_ABSTRACT_LEDGER_NO_GO_S281_NOT_NSE");
  assert.equal(binding.claimBoundary.averagedTerminalBoundary, "PROVED_P_TO_FOUR_FIFTH_S282_S284");
  assert.equal(binding.claimBoundary.universalAncestorGate, "OPEN_S288");
  assert.equal(binding.claimBoundary.movingTubeMorreyPacking, "PROVED_CONDITIONALLY_ON_UNIFORM_M_L_S289_S294");
  assert.equal(binding.claimBoundary.criticalMixedNormBenchmark, "PROVED_CONDITIONAL_S295_S300");
  assert.equal(binding.claimBoundary.cknDimensionImpliesAncestorPacking, false);
  assert.equal(binding.claimBoundary.combinedStep12Target, "OPEN_S303");
  assert.equal(binding.claimBoundary.frozenPacketPhysicalWinding, false);
  assert.equal(binding.claimBoundary.singlePacketSpeedRoute, "KINEMATICALLY_SCREENED_NOT_UNIVERSAL_PDE_NO_GO_S304_S306");
  assert.equal(binding.claimBoundary.dimensionlessFluxAndCommonDeletion, "PROVED_S307_S309");
  assert.equal(binding.claimBoundary.fixedSolutionTemporalSequence, "PROVED_ELL1_L4_OVER_3_S310_S312");
  assert.equal(binding.claimBoundary.fixedSolutionCommonWindowGain, "PROVED_DELTA_ONE_QUARTER_S313");
  assert.equal(binding.claimBoundary.linearPaymentOptimization, "PROVED_UNDER_EXPLICIT_S316_S317_S322");
  assert.equal(binding.claimBoundary.linearPaymentTargetTwoThirds, "METHOD_CEILING_STRICTLY_ABOVE_TWO_THIRDS");
  assert.equal(binding.claimBoundary.smoothTemporalSaturation, "ABSTRACT_NOT_NSE_COUNTEREXAMPLE_S323_S325");
  assert.equal(binding.claimBoundary.paymentDependentMovingTubeMorrey, "CONDITIONAL_ON_S328_S326_S330");
  assert.equal(binding.claimBoundary.twoScalarCapThreshold, "ABSTRACT_EXACT_TWO_THIRDS_S331");
  assert.equal(binding.claimBoundary.heatShearHighFrequencyScreen, "PROVED_EXACT_SMOOTH_NSE_S332_S334");
  assert.equal(binding.claimBoundary.criticalEightAryTree, "ABSTRACT_NOT_NSE_COUNTEREXAMPLE_S335_S339");
  assert.equal(binding.claimBoundary.incidenceChargingAndCubicDuality, "CONDITIONAL_INTERFACE_S340_S341");
  assert.equal(binding.claimBoundary.quadraticShellSelectivePayment, "OPEN_S342");
  assert.equal(binding.claimBoundary.step6PdeOrNseCounterexample, false);
  assert.equal(binding.claimBoundary.pdeWeightedGenealogy, "OPEN");
  assert.equal(binding.claimBoundary.fixedScaleInequality, "OPEN_Q1");
  assert.equal(binding.claimBoundary.formalFigure, "STEP13_ANALYTIC_SCHEMATIC_EXACT_FORMULAS_NOT_SIMULATION_OR_DNS");
});

test("R0.74S public mirrors, concise homepage card, and literature boundary are synchronized", () => {
  const home = read("public/research-review.html");
  assert.match(home, /LATEST RELEASE · R0\.74S/);
  assert.match(home, /R0\.70A–R0\.74S · 123 节已公开/);
  assert.match(home, /98 节完整封存/);
  assert.equal((home.match(/id="r074s" data-release="r074s"/g) ?? []).length, 1);
  const card = home.match(/<div class="task-one" id="r074s"[\s\S]*?<\/div>/)?.[0] ?? "";
  assert.ok(card.length > 0 && card.length < 500, `homepage card length ${card.length}`);
  for (const marker of ["时间模量", "two-cap 2/3", "critical cubic tree", "OPEN", "NOT CLAY"]) assert.ok(card.includes(marker), marker);
  const literature = read("public/literature-review.html");
  assert.equal((literature.match(/id="r074s-boundary"/g) ?? []).length, 1);
  for (const marker of ["S.307", "exact ceiling", "S.328", "S.342", "ABSTRACT", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);

  for (const ext of ["svg", "pdf", "png"]) {
    const canonical = `research/figures/r074s/fig-r074s-temporal-morrey-threshold/figure.${ext}`;
    assert.ok(existsSync(resolve(root, canonical)), canonical);
    assert.equal(sha(`public/assets/r074s/fig-r074s-temporal-morrey-threshold.${ext}`), sha(canonical));
    assert.equal(sha(`public/figures/r074s/fig-r074s-temporal-morrey-threshold/figure.${ext}`), sha(canonical));
    assert.equal(sha(`figures/r074s/fig-r074s-temporal-morrey-threshold/figure.${ext}`), sha(canonical));
  }
  const validation = JSON.parse(read("research/figures/r074s/fig-r074s-temporal-morrey-threshold/validation.json"));
  assert.equal(validation.summary.result, "PASS");
  assert.equal(validation.summary.passed, 12);
  assert.equal(validation.summary.total, 12);
  assert.equal(JSON.parse(read("figures/r074s/fig-r074s-ball-clock-debt/manifest.json")).status, "historical");
});

test("R0.74S translations and formal archive inventory are complete", () => {
  const translation = execFileSync(node, [resolve(root, "scripts/add-r074s-step13-translations.mjs"), "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translation, /"checked": [1-9][0-9]*/);
  assert.match(translation, /"applied": false/);
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.latestPublishedRelease, "r074s");
  assert.ok(inventory.publishedReleases.includes("r074s"));
  assert.ok(inventory.formalSealedReleases.includes("r074s"));
  assert.ok(!inventory.formalFigureExemptReleases.includes("r074s"));
  assert.equal(inventory.publishedReleaseCount, 123);
  assert.equal(inventory.formalSealedReleaseCount, 98);
  assert.equal(inventory.formalFigureExemptReleaseCount, 1);
});
