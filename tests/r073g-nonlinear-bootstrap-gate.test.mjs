import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const text = (relative) => readFile(resolve(root, relative), "utf8");
const sha = async (relative) => createHash("sha256")
  .update(await readFile(resolve(root, relative))).digest("hex");

const closed = [
  "exactDecayingShearPerturbationEquation",
  "selectedSeedPlanarInvariantClass",
  "selectedNonlinearOrbitGlobalSmoothness",
  "topEigenvectorPolynomialH3Cost",
  "fixedWindowH3Bootstrap",
  "allModeQuadraticRemainderBound",
  "nonlinearRelativeAmplification",
  "topEigenvectorDoubleRowLeakage",
];

const falseClaims = [
  "singleLinearRowNonlinearInvariant",
  "selectedRowCanCreateThreeDimensionalVortexStretching",
  "oneRowGainAloneImpliesOrderOneDeparture",
  "oneRowGainAloneImpliesFiniteTimeSingularity",
];

const open = [
  "naturalSeedOrderOneDeparture",
  "transverseThreeDimensionalTriadClosure",
  "singleBackgroundSingleOrbitInstability",
  "completeOSSquireA2DirectSum",
  "Clay",
];

function assertPublicVoice(value, label) {
  for (const phrase of [
    "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
  ]) assert.equal(value.includes(phrase), false, `${label}: ${phrase}`);
}

test("R0.73G analytic chain closes only the over-small-seed planar theorem", async () => {
  const [freeze, proof, operator, adversarial, independent, gap, report] = await Promise.all([
    text("research/r073g_problem_freeze.md"),
    text("research/r073g_nonlinear_shadowing_proof.md"),
    text("research/r073g_operator_derivation.md"),
    text("research/r073g_adversarial_audit.md"),
    text("research/r073g_independent_analytic_audit.md"),
    text("research/r073g_gap_matrix.md"),
    text("research/r073g_report-source.md"),
  ]);

  for (const key of closed) {
    assert.ok(gap.includes(`${key}=CLOSED`), `gap: ${key}`);
    assert.ok(report.includes(`${key}=CLOSED`), `report: ${key}`);
  }
  for (const key of falseClaims) {
    assert.ok(gap.includes(`${key}=FALSE`), `gap: ${key}`);
    assert.ok(report.includes(`${key}=FALSE`), `report: ${key}`);
  }
  for (const key of open) {
    assert.ok(gap.includes(`${key}=OPEN`), `gap: ${key}`);
    assert.ok(report.includes(`${key}=OPEN`), `report: ${key}`);
  }

  for (const token of [
    "T_D=\\frac{d_D}{4}",
    "\\|\\phi_\\Lambda\\|_{H^3}\\le C_{\\rm top}\\Lambda^2",
    "Y'\\le a\\Lambda Y+bY^2",
    "e^{-(M_D-\\kappa_D)_+\\Lambda}",
    "K_z=0,\\pm2",
    "n^2-\\frac{15}{4}",
  ]) assert.ok(proof.includes(token) || report.includes(token), token);

  assert.match(adversarial, /POST-REPAIR SUBSTANTIVE VERDICT: FINAL PASS/);
  assert.match(independent, /\*\*Correction obligations:\*\* none/);
  assert.equal(await sha("research/r073g_nonlinear_shadowing_proof.md"),
    independent.match(/Audited source SHA-256:\*\* ([0-9a-f]{64})/)[1]);
  assert.match(operator, /natural seed[\s\S]*still open/i);
  assert.ok(freeze.includes("genuinely transverse"));

  for (const [value, label] of [
    [freeze, "freeze"], [proof, "proof"], [operator, "operator"],
    [adversarial, "adversarial"], [independent, "independent"],
    [gap, "gap"], [report, "report"],
  ]) assertPublicVoice(value, label);
});

test("R0.73G keeps amplification, regularity, and Clay boundaries separate", async () => {
  const [proof, gap, report, literature] = await Promise.all([
    text("research/r073g_nonlinear_shadowing_proof.md"),
    text("research/r073g_gap_matrix.md"),
    text("research/r073g_report-source.md"),
    text("research/r073g_literature_audit.md"),
  ]);
  const joined = proof + gap + report;
  assert.match(joined, /relative amplification/i);
  assert.match(joined, /global(?:ly)? (?:smooth|regular)/i);
  assert.doesNotMatch(joined, /Clay=(?:CLOSED|TRUE)/);
  assert.doesNotMatch(joined, /naturalSeedOrderOneDeparture=(?:CLOSED|TRUE)/);
  assert.match(literature, /No\s+priority claim is made/);
  for (const token of [
    "math/0508173", "1803.11024", "1604.01831", "2509.18070",
  ]) assert.ok(literature.includes(token), token);
});
