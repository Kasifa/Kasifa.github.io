import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const run = promisify(execFile);
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const reportCommit = "b54d1c830a05e6366b9e95cbb4f730663435bef8";
const tick = String.fromCharCode(96);

const closed = [
  "exactHarmonicTaylorHierarchy",
  "targetHasNoQuadraticOrQuarticTerm",
  "continuumDoubledRowNumericalAbscissa",
  "localizedLinearCumulativeEnergy",
  "localizedQuadraticCubicEnergy",
  "fourthOrderExactRemainder",
  "gainNormalizedFixedDistanceDeparture",
  "selectedOrbitGlobalSmoothness",
];
const falseClaims = [
  ["gainLowerBoundDeterminesActualGain", "FALSE_AS_INFERENCE"],
  ["gainNormalizedDepartureImpliesPrescribedSeedDeparture", "FALSE_AS_INFERENCE"],
  ["finiteCubicCoefficientProvesContinuumSaturation", "FALSE_AS_INFERENCE"],
  ["familyDepartureIsSingleBackgroundLyapunovInstability", "FALSE_AS_INFERENCE"],
  ["planarDepartureCreatesThreeDimensionalVortexStretching", "FALSE"],
  ["planarDepartureImpliesFiniteTimeSingularity", "FALSE"],
  ["planarDepartureResolvesClay", "FALSE"],
];
const open = [
  "sharpSelectedGainAction",
  "prescribedLowerLawSeedDeparture",
  "uniformTaylorRadiusAtNaturalEndpoint",
  "fullContinuumHarmonicResolvedSemigroupEstimate",
  "singleBackgroundLyapunovSequence",
  "transverseOSSquireEvolution",
  "transverseTriadClosure",
  "finiteTimeSingularity",
  "Clay",
];
const sources = [
  "research/r073h_problem_freeze.md",
  "research/r073h_harmonic_energy_proof.md",
  "research/r073h_harmonic_derivation.md",
  "research/r073h_independent_analytic_audit.md",
  "research/r073h_adversarial_audit.md",
  "research/r073h_literature_audit.md",
  "research/r073h_gap_matrix.md",
  "research/r073h_bilingual_dictionary.md",
  "research/r073h_report-source.md",
];

function assertPublicVoice(value, label) {
  for (const phrase of [
    "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
  ]) assert.equal(value.includes(phrase), false, label + ": " + phrase);
}

test("R0.73H analytic theorem is exactly gain-normalized and planar", async () => {
  const [proof, derivation, gap, report, independent, adversarial, dictionary] =
    await Promise.all([
      text("research/r073h_harmonic_energy_proof.md"),
      text("research/r073h_harmonic_derivation.md"),
      text("research/r073h_gap_matrix.md"),
      text("research/r073h_report-source.md"),
      text("research/r073h_independent_analytic_audit.md"),
      text("research/r073h_adversarial_audit.md"),
      text("research/r073h_bilingual_dictionary.md"),
    ]);
  for (const key of closed) {
    assert.ok(gap.includes("| " + tick + key + tick + " | CLOSED |"), key);
  }
  for (const [key, status] of falseClaims) {
    assert.ok(gap.includes("| " + tick + key + tick + " | " + status + " |"), key);
  }
  for (const key of open) {
    assert.ok(gap.includes("| " + tick + key + tick + " | OPEN |"), key);
  }
  for (const token of [
    "G_\\Lambda", "\\frac{\\delta}{G_\\Lambda}\\phi_\\Lambda",
    "\\|\\Pi_{\\{K_z=\\pm1\\}}u_\\Lambda^\\delta(D)\\|_2",
    "\\ge \\frac\\delta2", "D=\\min\\{d_0,1/450\\}",
    "\\|u_\\Lambda^\\delta(0)\\|_{H^3}",
  ]) assert.ok(proof.includes(token) || report.includes(token), token);
  for (const token of [
    "(1,0)", "(0,1)", "(-1,2)", "(2,-1)",
    "neither a quadratic nor a quartic term",
  ]) assert.ok(derivation.includes(token) || report.includes(token), token);
  assert.match(independent, /MATHEMATICAL FINAL PASS/);
  assert.match(adversarial, /No adversarial test above invalidates/);
  assert.match(dictionary, /prescribed lower-law seed/i);
  assert.match(dictionary, /Required wording boundary/i);
  assert.match(report + gap, /uniform all-order Taylor radius for the prescribed lower-law seed/i);
  assert.match(report, /not a Lyapunov-instability theorem for\s+one fixed background/i);
  assert.match(report, /no\s+three-dimensional vortex stretching/i);
  assert.doesNotMatch(report + gap, /Clay=(?:CLOSED|TRUE)/);
  for (const [label, value] of [
    ["proof", proof], ["derivation", derivation], ["gap", gap],
    ["report", report], ["independent", independent],
    ["adversarial", adversarial], ["dictionary", dictionary],
  ]) assertPublicVoice(value, label);
});

test("R0.73H finite diagnostics stay outside the continuum theorem window", async () => {
  const [certificate, validation, primary, independent, exact, gap] =
    await Promise.all([
      json("research/certificates/r073h/certificate.json"),
      json("research/certificates/r073h/validation.json"),
      json("research/certificates/r073h/primary_summary.json"),
      json("research/certificates/r073h/independent_validation.json"),
      json("research/certificates/r073h/exact_q2_certificate.json"),
      text("research/r073h_gap_matrix.md"),
    ]);
  assert.equal(certificate.allChecksPass, true);
  assert.equal(validation.allChecksPass, true);
  assert.equal(primary.allChecksPass, true);
  assert.equal(primary.diagnosticOnly, true);
  assert.equal(independent.allChecksPass, true);
  assert.equal(independent.diagnosticOnly, true);
  assert.equal(exact.allChecksPass, true);
  assert.equal(exact.profilePerturbation.maximumProfileTime, "1/450");
  assert.equal(primary.formalGrid.profileTimeSnapshots.at(-1), 0.01);
  assert.equal(independent.validations.filter((row) => row.gridKind === "formal").length, 4);
  assert.equal(independent.validations.filter((row) => row.gridKind === "holdout").length, 1);
  assert.equal(certificate.finiteHarmonicDiagnostic.observations.primaryRowCount, 319);
  assert.equal(certificate.finiteHarmonicDiagnostic.observations.cutoffComparisonCount, 21);
  assert.equal(certificate.finiteHarmonicDiagnostic.observations.stepComparisonCount, 6);
  assert.match(gap, /d=0\.01>1\/450/);
  assert.match(gap, /outside the[\s\S]*continuum-theorem interval/i);
  assert.equal(certificate.claimLedger.finiteDuhamelResponseAtFrozenGrid,
    "FINITE_DIAGNOSTIC_ONLY");
  assert.equal(certificate.claimLedger.fullContinuumHarmonicResolvedSemigroupEstimate,
    "OPEN");
});

test("R0.73H certified prose sources are immutable at the report commit", async () => {
  await assert.doesNotReject(
    run("git", ["cat-file", "-e", reportCommit + "^{commit}"], { cwd: root }),
  );
  for (const relative of sources) {
    const frozen = await run("git", ["show", reportCommit + ":" + relative], {
      cwd: root, encoding: "buffer", maxBuffer: 16 * 1024 * 1024,
    });
    assert.deepEqual(await readFile(resolve(root, relative)), frozen.stdout, relative);
  }
});
