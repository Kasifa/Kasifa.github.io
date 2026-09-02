#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.74S reader PDF.

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { createReadStream } from "node:fs";
import { createServer } from "node:http";
import { readFile, writeFile } from "node:fs/promises";
import { extname, resolve } from "node:path";
import { inspectPdf } from "./render-note-pdf.mjs";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");

function sha256(bytes) { return createHash("sha256").update(bytes).digest("hex"); }

function run(executable, arguments_, options = {}) {
  return new Promise((resolvePromise, reject) => {
    const child = spawn(executable, arguments_, { cwd: root, env: { ...process.env, ...options.env }, stdio: ["ignore", "pipe", "pipe"] });
    let stdout = "";
    let stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", reject);
    child.on("close", (status) => status === 0 ? resolvePromise({ stdout, stderr }) : reject(new Error(`${executable} ${arguments_.join(" ")} failed (${status}): ${stderr || stdout}`)));
  });
}

function contentType(path) {
  return new Map([[".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"], [".css", "text/css; charset=utf-8"], [".svg", "image/svg+xml"], [".png", "image/png"], [".pdf", "application/pdf"], [".json", "application/json"]]).get(extname(path).toLowerCase()) ?? "application/octet-stream";
}

const server = createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname);
  const relative = pathname === "/" ? "research-review.html" : pathname.replace(/^\/+/, "");
  const target = resolve(publicRoot, relative);
  if (!target.startsWith(`${publicRoot}/`)) { response.writeHead(403).end(); return; }
  response.setHeader("Content-Type", contentType(target));
  const stream = createReadStream(target);
  stream.on("error", () => response.writeHead(404).end());
  stream.pipe(response);
});

await new Promise((resolvePromise, reject) => { server.once("error", reject); server.listen(0, "127.0.0.1", resolvePromise); });
const address = server.address();

try {
  const htmlRelative = "public/notes/r0-74s.html";
  const pdfRelative = "public/notes/r0-74s.pdf";
  const provenanceRelative = "research/r074s_note_pdf_render.json";
  const bindingRelative = "research/r074s_pdf_bindings.json";
  const url = `http://127.0.0.1:${address.port}/notes/r0-74s.html?lang=zh`;
  await run(process.execPath, ["scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });
  const [html, pdf, provenanceBytes] = await Promise.all([readFile(resolve(root, htmlRelative)), readFile(resolve(root, pdfRelative)), readFile(resolve(root, provenanceRelative))]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.74S｜外侧 collar 对齐与 jump--corona 障碍";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);
  const provenance = JSON.parse(provenanceBytes);
  if (provenance.loadedDocument?.equalsSourceHtml !== true || provenance.loadedDocument?.sha256 !== sha256(html) || provenance.source?.publicOrigin !== "https://kasifa.github.io") throw new Error("note render provenance mismatch");
  const binding = {
    schemaVersion: "r074s-note-synchronized-pdf-binding-v1",
    release: "R0.74S",
    kind: "note",
    publicChineseHtml: { path: htmlRelative, bytes: html.length, sha256: sha256(html) },
    publicPdf: { path: pdfRelative, bytes: pdf.length, sha256: sha256(pdf), pageCount: structure.pageCount, title: structure.title, structure },
    provenance: { path: provenanceRelative, bytes: provenanceBytes.length, sha256: sha256(provenanceBytes), sourceUrl: provenance.source.url, loadedMainDocumentEqualsSourceHtml: true },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      evidenceClassesSeparated: ["PROVED", "CONDITIONAL", "ABSTRACT METHOD OBSTRUCTION", "METHOD CEILING", "INHERITED", "FINITE", "REFUTED", "RULED OUT", "LITERATURE BOUNDARY", "OPEN", "NO-GO", "NOT CLAIMED", "NOT CLAY"],
      oneSidedBallClocks: "PROVED",
      stoppedOrientations: "PROVED",
      quadraticBallLedger: "PROVED",
      terminalAbelIdentity: "PROVED",
      fullSignedRecombination: "PROVED_CIRCULAR",
      threeChannelTemporalDebtCancellation: "PROVED",
      terminalL1Decomposition: "PROVED",
      unweightedGenealogyObstruction: "PROVED_ABSTRACT_SCALAR_NO_GO",
      step6PdeOrNseCounterexample: false,
      pdeWeightedGenealogy: "OPEN",
      viscousDefectSplit: "PROVED_INHERITED_MEASURE_IDENTITY",
      lowHighRayleighTimeSplit: "PROVED",
      dissipationPriorityTrichotomy: "PROVED",
      lowRayleighAllShellPayment: "PROVED",
      rayleighExcessMeasures: "PROVED",
      scalarAndJordanExcessTiers: "PROVED_DISTINCT",
      excessPriorityTrichotomy: "PROVED",
      fixedScaleExcessLowerSemicontinuity: "PROVED_UNDER_INHERITED_TOPOLOGY",
      fixedScaleJordanEnvelopeFiniteness: "PROVED",
      selectedScalarResidual: "UNIFIED_WITH_EXISTING_STOPPED_WORK_GATE",
      highRayleighScalarResidual: "UNIFIED_WITH_EXISTING_STOPPED_WORK_GATE",
      anomalousDefectScalarResidual: "UNIFIED_WITH_EXISTING_STOPPED_WORK_GATE",
      selectedPositiveFluxRelation: "PROVED_F_GREATER_THAN_5K_OVER_6",
      fullDissipationBranchBridge: "PROVED_QUADRATIC_PLUS_6_OVER_5_STOPPED_WORK",
      stoppedWorkFullFluxEquivalence: "PROVED_WITHIN_PAID_B_Q",
      stoppedWorkFullClockEquivalence: "PROVED_WITHIN_PAID_B_Q",
      universalNoExceptionQuadraticAntecedent: "REFUTED_BY_INHERITED_SMOOTH_EXACT_NSE_FAMILY",
      conditionalS38Implication: "PROVED_RETAINED",
      terminalDomainSeparation: "PROVED_PLATEAU_LESS_THAN_OR_EQUAL_TO_FULL",
      signedBestNTailQuantifierOrder: "PROVED_SUP_INF_TERMINAL_DEPENDENT_EXCEPTIONS",
      signedFHalfExit: "PROVED_EXACT_ONE_HALF_BEST_N_TAIL",
      signedFHalfExitS25Admissibility: false,
      kThetaLastExit: "PROVED_WITH_SHARP_ONE_B_Q_ERROR",
      kThetaGoodStopClosure: "PROVED_FINITE_POSITIVE_TERMINALS_AT_GOOD_TERMINALS_FOR_THETA_BELOW_THREE_QUARTERS",
      canonicalLastExitQuadraticCompression: "REFUTED_PROVED_NO_GAIN_EQUIVALENCE",
      fullTerminalBestNTail: "OPEN_Q12",
      plateauBestNTail: "OPEN_WEAKER_RESTRICTION",
      fixedBestNTerminalExceptionEstimate: "OPEN_NEXT_PDE_TARGET",
      sixClassPaidResidualPartition: "PROVED_D_FIRST_EXACT_PARTITION",
      lowRayleighExtraResidualClass: false,
      oneQPaidLedger: "PROVED_SINGLE_6_B_Q",
      oneCubicPaidLedger: "PROVED_SINGLE_C5_LEDGER",
      residualClasses: ["R_sh", "R_x"],
      residualTwoSidedComparability: "PROVED_T_OVER_6_LT_R_LT_T_OVER_2",
      residualBestNReduction: "PROVED_DOMAIN_SAFE",
      separateResidualExceptionBudgets: false,
      terminalDDominanceLastExitPersistence: false,
      paidBranchResidualTail: "PROVED_DEFINED_AND_REDUCED_PACKING_OPEN",
      fixedUniversalN0ResidualEstimate: "OPEN_S243",
      jordanEnvelopeQuadraticBound: "OPEN",
      finiteExceptionConsequence: "PROVED_CONDITIONAL_IMPLICATION_ONLY",
      sharedBudgetPointwiseInfimalConvolution: "PROVED_EXACT_S249",
      terminalSupremumBudgetMinimumCommutation: false,
      sharedBudgetDomainInequality: "PROVED_S250",
      addedBranchExceptionCounts: "PROVED_CONDITIONAL_S251",
      duplicateBranchBudgets: false,
      shortBranchInverseDuration: "PROVED_S253_S254",
      criticalQuadraticCarlesonEndpoint: "REFUTED_AT_COEFFICIENT_CLOCK_LEVEL_LOG_GAP",
      criticalCarlesonWitnessIsNseCounterexample: false,
      nestedTentEstimate: "PROVED_S258",
      positiveBackwardDepthControl: "PROVED_S259",
      depthZeroTerminalTrace: "OPEN_S261",
      scalarExcessResidualBestNComparison: "PROVED_CONSTANTS_ONE_FIFTH_AND_THREE",
      fixedSolutionTailTightness: "PROVED_NONUNIFORM_S265",
      fixedSolutionTightnessGivesUniversalN: false,
      lastExitAncestryLocalization: false,
      ancestryFixturesAreNseCounterexamples: false,
      uniformSelectedExcessPacking: "OPEN_S269",
      nPlusOneTargetFalsificationCriterion: "PROVED_CONDITIONAL_S270",
      existingMultiPacketFamiliesRefuteFixedPositiveN: false,
      combinedTwoBranchEstimate: "OPEN_S272",
      exactShearHighRayleighDiagnostic: "PROVED_IN_INHERITED_SCOPE_NOT_A_COUNTEREXAMPLE",
      commonTerminalWindowDefinition: "PROVED_S273",
      commonWindowShortResidualReduction: "PROVED_S274_S275",
      commonWindowTerminalContinuity: "PROVED_S276",
      fixedSolutionWindowModulus: "PROVED_NONUNIFORM_S277",
      bestNLayerCakeIdentity: "PROVED_S278",
      allThresholdWindowImplication: "PROVED_S279",
      universalTerminalWindowGate: "OPEN_S280",
      l1OnlyWindowEstimate: "REFUTED_ABSTRACT_LEDGER_NO_GO_S281_NOT_NSE",
      averagedTerminalBoundary: "PROVED_P_TO_FOUR_FIFTH_S282_S284",
      ancestorExceptionBudgetAddition: "PROVED_S285_S287",
      universalAncestorGate: "OPEN_S288",
      movingTubeMorreyPacking: "PROVED_CONDITIONALLY_ON_UNIFORM_M_L_S289_S294",
      criticalMixedNormBenchmark: "PROVED_CONDITIONAL_S295_S300",
      cknDimensionImpliesAncestorPacking: false,
      combinedStep12Target: "OPEN_S303",
      frozenPacketPhysicalWinding: false,
      singlePacketSpeedRoute: "KINEMATICALLY_SCREENED_NOT_UNIVERSAL_PDE_NO_GO_S304_S306",
      dimensionlessFluxAndCommonDeletion: "PROVED_S307_S309",
      fixedSolutionTemporalSequence: "PROVED_ELL1_L4_OVER_3_S310_S312",
      fixedSolutionCommonWindowGain: "PROVED_DELTA_ONE_QUARTER_S313",
      generalTemporalHolder: "PROVED_S314_S315",
      linearPaymentOptimization: "PROVED_UNDER_EXPLICIT_S316_S317_S322",
      linearPaymentTargetTwoThirds: "METHOD_CEILING_STRICTLY_ABOVE_TWO_THIRDS",
      smoothTemporalSaturation: "ABSTRACT_NOT_NSE_COUNTEREXAMPLE_S323_S325",
      paymentDependentMovingTubeMorrey: "CONDITIONAL_ON_S328_S326_S330",
      twoScalarCapThreshold: "ABSTRACT_EXACT_TWO_THIRDS_S331",
      heatShearHighFrequencyScreen: "PROVED_EXACT_SMOOTH_NSE_S332_S334",
      criticalEightAryTree: "ABSTRACT_NOT_NSE_COUNTEREXAMPLE_S335_S339",
      incidenceChargingAndCubicDuality: "CONDITIONAL_INTERFACE_S340_S341",
      strictCubicDiniPdeGain: "OPEN",
      quadraticShellSelectivePayment: "OPEN_S342",
      uniformFixedSolutionHTailPayment: "OPEN",
      shellScalePressureAndFourChannelFlux: "PROVED_S343_S347",
      outerCollarAlignment: "PROVED_SAME_WEIGHT_NO_GAIN_S350_S352",
      alignedSpike: "ABSTRACT_METHOD_OBSTRUCTION_NOT_NSE_S353_S355",
      incidenceHolderS358: "CONDITIONAL_ON_S356_S357",
      criticalDensityCancellation: "PROVED_NO_LINEAR_PAYMENT_GAIN_S360_S365",
      firstJumpDiniSkeleton: "PROVED_UNDER_DISPLAYED_HYPOTHESES_S366_S368",
      strictnessFreeDini: "REFUTED_AS_METHOD_S369",
      criticalCorona: "ABSTRACT_METHOD_OBSTRUCTION_NOT_NSE_S370",
      shellIncidenceAndHeatShear: "PROVED_S371_S374",
      jumpCoronaPdeLemma: "OPEN_S375",
      jumpCoronaConclusion: "CONDITIONAL_ON_OPEN_S375_S376",
      fixedScaleInequality: "OPEN_Q1",
      formalFigure: "STEP14_OUTER_COLLAR_CORONA_ANALYTIC_SCHEMATIC_EXACT_FORMULAS_NOT_SIMULATION_OR_DNS",
      navierStokesSimulation: false,
      directNumericalSimulation: false,
      translationPath: "LOCAL_DIRECT_NO_DGX",
      dgxUsed: false,
      regularityOrSingularityResolved: false,
      clayProblemSolved: false,
    },
  };
  await writeFile(resolve(root, bindingRelative), `${JSON.stringify(binding, null, 2)}\n`);
  process.stdout.write(`${JSON.stringify({ applied: true, release: "R0.74S", pageCount: structure.pageCount, sha256: sha256(pdf), bytes: pdf.length }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}

await run(process.env.RELEASE_PYTHON ?? "python3", ["scripts/generate_note_index.py"]);
