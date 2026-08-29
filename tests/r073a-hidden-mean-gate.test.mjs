import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificate = "research/certificates/r073a";
const figure = "figures/r073a/fig-r073a-hidden-mean-transient-spectral";

const expectedSourceStage = {
  release: "r073a",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r073a_report-source.md",
  problemFreeze: "research/r073a_problem_freeze.md",
  literatureAudit: "research/r073a_literature_audit.md",
  gapMatrix: "research/r073a_gap_matrix.md",
  analyticProof: "research/r073a_transient_proof.md",
  projectionDerivation: "research/r073a_projection_derivation_agent.md",
  projectionIndependentAudit: "research/r073a_projection_independent_audit.md",
  independentAnalyticAudit: "research/r073a_independent_analytic_audit.md",
  spectralAudit: "research/r073a_spectral_audit_agent.md",
  producer: `${certificate}/generate_certificate.py`,
  independentProducer: `${certificate}/independent_recompute.py`,
  comparator: `${certificate}/validate_certificate.py`,
  certificateDirectory: certificate,
  experimentDirectory: "experiments/r073a",
  figureDirectory: figure,
  generator: "scripts/generate_r073a_release.py",
  translationScript: "scripts/add-r073a-translations.mjs",
  translationSnapshot: "scripts/i18n-snapshots/r073a-missing.json",
  releaseGate: "tests/r073a-hidden-mean-gate.test.mjs",
  publicationTest: "tests/r073a-release.test.mjs",
  certificateSourceTest: "tests/r073a-deterministic-certificate-source.test.mjs",
  figureSourceTest: "tests/r073a-hidden-mean-transient-spectral-figure-source.test.mjs",
};

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

function compact(value) {
  return value.replace(/\s+/g, "");
}

test("R0.73A freezes the exact hidden-mean coordinate and viscous-rate theorem", async () => {
  const [report, proof, audit] = await Promise.all([
    text("research/r073a_report-source.md"),
    text("research/r073a_transient_proof.md"),
    text("research/r073a_independent_analytic_audit.md"),
  ]);
  const source = compact(report + proof);
  for (const token of [
    "h=\\mu^{-1}\\Pi_0q", "r=Q_0q", "q=\\muh+r",
    "\\|(h,r)\\|_{X_\\mu}^2=|h|^2+\\|r\\|_2^2",
    "\\Pi_0\\left(Wr+W_{xx}\\mathcalL_\\mu^{-1}r\\right)=\\mu\\Pi_0\\left(W\\mathcalL_\\mu^{-1}r\\right)",
    "J(s,d)=\\frac74(e^{-s}-e^{-d})+\\frac12(e^{-4s}-e^{-4d})",
    "\\|U_\\mu(d,s)\\|_{X_\\mu\\toX_\\mu}\\lee^9e^{-\\mu(d-s)}",
    "\\mathfrakF_\\mu\\inL^1_{\\mathrm{loc}}",
  ]) assert.ok(source.includes(compact(token)), token);
  assert.match(proof, /viscous-rate estimate with a finite transient prefactor/i);
  assert.match(proof, /not an enhanced-dissipation or scalar-\\\(A_2\\\)-rate estimate/i);
  assert.match(audit, /ANALYTIC PASS WITH REQUIRED PUBLICATION-SCOPE EDITS/);
  assert.ok(audit.includes("| Gronwall and square root | **PASS** | there is no missing factor of two |"));
});

test("R0.73A path qualifier distinguishes positive-gap noninvariance from the fixed-Lambda limit", async () => {
  const [report, proof, audit, gap] = await Promise.all([
    text("research/r073a_report-source.md"),
    text("research/r073a_transient_proof.md"),
    text("research/r073a_independent_analytic_audit.md"),
    text("research/r073a_gap_matrix.md"),
  ]);
  const joined = report + proof + audit + gap;
  const compactJoined = compact(joined);
  for (const token of [
    "h_d(s)=ic_\\mu\\left[\\frac{e^{-2s}}{8(1+\\mu)}+\\frac{e^{-8s}}{8(4+\\mu)}\\right]",
    "c_\\mu\\toc_0\\ne0", "c_\\mu=\\gamma\\Lambda_\\mu",
    "|\\Lambda_\\mu|", "|\\gamma|^{-1}",
  ]) assert.ok(compactJoined.includes(compact(token)), token);
  assert.ok(proof.includes("For every fixed positive gap with \\(c_\\mu\\ne0\\), the lifted line"));
  assert.ok(proof.includes("If \\(\\Lambda\\) is held\nfixed instead, then \\(c_\\mu\\to0\\)"));
  assert.ok(audit.includes("The instantaneous calculation does not disprove a\nfixed-\\(\\Lambda\\) singular limit."));
  assert.ok(gap.includes("fixed Lambda raw-q limit remains undecided"));
});

test("R0.73A rank-one FALSE is limited to the lifted invariant-state meaning", async () => {
  const [report, proof, projection, audit] = await Promise.all([
    text("research/r073a_report-source.md"),
    text("research/r073a_transient_proof.md"),
    text("research/r073a_projection_derivation_agent.md"),
    text("research/r073a_independent_analytic_audit.md"),
  ]);
  for (const token of [
    "rankOneAbstractTangentClosesPhysicalLongWaveLimit=FALSE",
    '"closes" means an invariant lifted one-dimensional physical state',
  ]) assert.ok(proof.includes(token), token);
  assert.match(report, /it does not refer to the general moving\s+quotient identity/i);
  assert.match(audit, /safe only if\s+“closes” is defined to mean this invariant lifted one-dimensional state/is);
  for (const token of [
    "moving rank-one quotient algebra", "\\texttt{CLOSED}",
    "explicit orthogonal }P_d,QAP,PAQ",
  ]) assert.ok(projection.includes(token), token);
});

test("R0.73A projection obstruction retains c, g, time, and common-space qualifiers", async () => {
  const [report, projection, projectionAudit, gap, generator] = await Promise.all([
    text("research/r073a_report-source.md"),
    text("research/r073a_projection_derivation_agent.md"),
    text("research/r073a_projection_independent_audit.md"),
    text("research/r073a_gap_matrix.md"),
    text("scripts/generate_r073a_release.py"),
  ]);
  assert.match(projectionAudit, /ANALYTIC PASS WITH SCOPE EDITS APPLIED/);
  assert.ok(report.includes("the full instantaneous OS generator does not preserve\n\\(\\mathcal S\\) whenever \\(c\\ne0\\)"));
  assert.ok(report.includes("At \\(c=0\\), the full generator is just\n\\(-\\mathcal L_0\\), so \\(\\mathcal S\\) is invariant"));
  assert.ok(projection.includes("&=-\\frac3{16}(a x_2+2b x_1)"));
  for (const token of [
    "fixedTwoHarmonicOSInvariance = FALSE for c != 0",
    "Q^*\\mathscr B^*\\psi", "|c|/g\\to\\infty",
    "compact \\(d\\)-interval", "common-space identification",
  ]) assert.ok(projectionAudit.includes(token), token);
  assert.ok(report.includes("\\inf_d\\|\\phi(d)\\|_2>0"));
  assert.ok(report.includes("this pressure\nblock is multiplied by \\(|c|\\)"));
  assert.ok(report.includes("only along paths for which \\(|c|/g\\to\\infty\\)"));
  assert.ok(report.includes("makes no operator-norm\ncontinuity claim"));
  assert.ok(!report.includes("operator families are therefore not norm-continuous"));
  assert.ok(gap.includes("FALSE for c != 0"));
  for (const token of [
    "fixedTwoHarmonicOSInvariance=FALSE 只在 \\(c\\ne0\\)",
    "common dense domain \\(D\\)", "strong \\(C^1\\) solution",
    "adjoint-domain compatibility", "standalone quotient 的 well-posedness",
    "\\inf_d\\|\\phi(d)\\|_2>0", "|c|/g\\to\\infty",
    "不声称无共同空间识别时 \\(g=0\\) 与 \\(g>0\\) 的算子范数不连续",
  ]) assert.ok(generator.includes(token), token);
});

test("R0.73A keeps every stronger physical and Millennium claim OPEN", async () => {
  const [report, proof, gap] = await Promise.all([
    text("research/r073a_report-source.md"),
    text("research/r073a_transient_proof.md"),
    text("research/r073a_gap_matrix.md"),
  ]);
  for (const claim of [
    "lowGapOSTransientA2Propagator", "lowGapPhysicalKineticPropagator",
    "generalBlochLowGapOSPropagator", "lowGapOSSquirePropagator",
    "BlochUniformPhysicalVelocityDirectSum", "nonlinearNavierStokes", "Clay",
  ]) {
    assert.ok(report.includes(`\\texttt{${claim}}&=\\texttt{OPEN}`), claim);
    assert.ok(gap.includes(`| \`${claim}\` | OPEN |`), claim);
  }
  assert.match(proof, /not uniformly equivalent either/);
});

test("R0.73A source-stage package names are exact without advancing public counters", async () => {
  for (const relative of [
    "research/r073a_report-source.md", "research/r073a_problem_freeze.md",
    "research/r073a_literature_audit.md", "research/r073a_gap_matrix.md",
    "research/r073a_transient_proof.md", "research/r073a_projection_derivation_agent.md",
    "research/r073a_projection_independent_audit.md",
    "research/r073a_independent_analytic_audit.md", "research/r073a_spectral_audit_agent.md",
    `${certificate}/generate_certificate.py`, `${certificate}/independent_recompute.py`,
    `${certificate}/validate_certificate.py`, `${figure}/contract.json`,
    "scripts/generate_r073a_release.py", "scripts/add-r073a-translations.mjs",
    "scripts/i18n-snapshots/r073a-missing.json",
    "tests/r073a-release.test.mjs", "tests/r073a-deterministic-certificate-source.test.mjs",
    "tests/r073a-hidden-mean-transient-spectral-figure-source.test.mjs",
  ]) await access(resolve(root, relative));
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072z") {
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
    assert.deepEqual({
      version: manifest.siteVersion, notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount, published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount, backlog: manifest.legacyFormalFigureBacklogCount,
    }, { version: "1.39", notes: 176, recap: 116, published: 78, sealed: 54, backlog: 24 });
  } else {
    assert.equal(manifest.latestCompletedRelease, "r073a");
    assert.equal(manifest.nextReleaseSourceStage, undefined);
  }
});
