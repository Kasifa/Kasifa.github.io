import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificate = "research/certificates/r072x";
const figure = "figures/r072x-all-center/fig-r072x-all-center-transfer";
const figureId = "fig-r072x-all-center-transfer";

const expectedSourceStage = {
  release: "r072x",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r072x_report-source.md",
  literatureAudit: "research/r072x_literature_audit.md",
  gapMatrix: "research/r072x_gap_matrix.md",
  independentAudit: "research/r072x_independent_audit.md",
  producer: "research/certificates/r072x/generate_certificate.py",
  independentProducer: "research/certificates/r072x/independent_recompute.py",
  comparator: "research/certificates/r072x/validate_certificate.py",
  certificateDirectory: certificate,
  figureDirectory: figure,
  generator: "scripts/generate_r072x_release.py",
  translationScript: "scripts/add-r072x-translations.mjs",
  releaseGate: "tests/r072x-exact-path-gate.test.mjs",
  publicationTest: "tests/r072x-release.test.mjs",
};

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function exists(relative) {
  try {
    await access(resolve(root, relative));
    return true;
  } catch (error) {
    if (error?.code === "ENOENT") return false;
    throw error;
  }
}

test("R0.72X freezes the shifted exact family and every claim status", async () => {
  const [report, gap, audit] = await Promise.all([
    text("research/r072x_report-source.md"),
    text("research/r072x_gap_matrix.md"),
    text("research/r072x_independent_audit.md"),
  ]);

  for (const token of [
    "V_{\\alpha,S_0}(\\tau,X)=\\alpha^{-3}",
    "D_0=\\alpha^2S_0",
    "K_T=K+[-T,T]",
    "\\partial_\\tau V_X=V_{XXX}",
    "\\partial_\\tau(V_{XX}/2)=V_{XXXX}/2",
  ]) assert.ok(report.includes(token), token);

  for (const [label, status] of [
    ["allCenterExactFamilyGraphCoercivity", "CLOSED"],
    ["allStartExactPathSemigroup", "CLOSED"],
    ["allStartIntegratedA2Scale", "CLOSED"],
    ["uniformTwistedPeriodicGraph", "CLOSED"],
    ["strongRowDirectSumNoCountLoss", "CLOSED"],
    ["fixedMarginA1EnhancedDissipation", "CLOSED"],
    ["exactA1A2A1TimeConcatenation", "CLOSED"],
    ["shrinkingInterfaceFixedShapeA1Hypotheses", "FALSE"],
    ["prefactorOneAllGapExponential", "FALSE"],
    ["allPhysicalRowsUniformContraction", "FALSE"],
    ["forcedHMinusOneTransfer", "OPEN"],
    ["completeLinearizedShearSubsystem", "OPEN"],
    ["nonlinearNavierStokes", "OPEN"],
    ["Clay", "OPEN"],
  ]) assert.ok(
    report.includes(`\\texttt{${label}}&=\\texttt{${status}}`),
    `${label}=${status}`,
  );

  assert.match(gap, /\| All-center unit-cell theorem \| \*\*CLOSED\*\*/);
  assert.match(gap, /\| Arbitrary short-time strict factor \| \*\*FALSE\*\*/);
  assert.match(gap, /\| All physical rows uniform strict contraction \| \*\*FALSE\*\*/);
  assert.match(audit, /Audit outcome:\*\* \*\*PASS\*\*/);
  assert.match(report, /one fixed deterministic starting vector/);
  assert.match(
    report,
    /does\s+not independently certify that it is the global largest eigenpair/s,
  );
  assert.match(report, /seed orthogonal to the top\s+eigenspace/s);
  assert.match(
    report,
    /Krylov breakdown before dimension 8 is also\s+rejected conservatively/s,
  );
});

test("R0.72X closes the bounded-center branch without losing modulo 2pi", async () => {
  const [report, audit, producer] = await Promise.all([
    text("research/r072x_report-source.md"),
    text("research/r072x_independent_audit.md"),
    text(`${certificate}/generate_certificate.py`),
  ]);
  for (const token of [
    "\\theta=\\alpha X_0\\pmod{2\\pi}",
    "\\theta\\in[-\\pi,\\pi]",
    "r=e^{3D_0}>0",
    "4\\cos^2\\theta=2\\cos^2\\theta-1",
    "(D_0,\\theta)=(0,0)\\pmod{2\\pi}",
    "\\theta=O(\\alpha)",
    "D_0=O(\\alpha^2)",
  ]) assert.ok(report.includes(token), token);
  for (const token of [
    "\\operatorname{diag}(3,3)",
    "f=3D+\\frac32\\theta^2",
    "g=3\\theta+O(|D\\theta|+|\\theta|^3)",
    "translate of \\(H_3=",
  ]) assert.ok(audit.includes(token), token);
  for (const token of [
    '"fJetThroughTotalDegreeThree": selected_jet(f)',
    '"gJetThroughTotalDegreeThree": selected_jet(g)',
    'common["fJetThroughTotalDegreeThree"].get("D") == "3/1"',
    'common["fJetThroughTotalDegreeThree"].get("theta^2") == "3/2"',
    'common["gJetThroughTotalDegreeThree"].get("theta") == "3/1"',
  ]) assert.ok(producer.includes(token), token);
});

test("R0.72X keeps the q inverse prefactor and integrated A2 factor exact", async () => {
  const [report, audit, producer] = await Promise.all([
    text("research/r072x_report-source.md"),
    text("research/r072x_independent_audit.md"),
    text(`${certificate}/generate_certificate.py`),
  ]);
  for (const token of [
    "q_{K,T}^{\\left\\lfloor",
    "q_{K,T}^{-1}",
    "c_{K,T}=\\frac{|\\log q_{K,T}|}{2T}",
    "\\frac{2T\\alpha^2}{1-q_{K,T}^2}",
  ]) assert.ok(report.includes(token), token);
  assert.ok(audit.includes("Since \\(\\lfloor y\\rfloor\\ge y-1\\)"));
  assert.ok(audit.includes("strong continuity gives"));
  assert.match(audit, /prefactor-one exponential is strictly below one/);
  assert.ok(producer.includes(
    '"exponentialEnvelope": "q^N<=q^(-1)*exp(-(|log(q)|/(2*T))*L/alpha^2)"',
  ));
  assert.ok(producer.includes(
    '"physicalIntegratedEnergyBound": "2*T*alpha^2/(1-q^2)*E(d_1)"',
  ));
});

test("R0.72X preserves Bloch, row, damping, and zero-coupling ledgers", async () => {
  const [report, audit, producer] = await Promise.all([
    text("research/r072x_report-source.md"),
    text("research/r072x_independent_audit.md"),
    text(`${certificate}/generate_certificate.py`),
  ]);
  for (const token of [
    "(\\partial_X+i\\alpha\\beta_r)^2",
    "w=e^{i\\alpha\\beta_rX}u",
    "e^{2\\pi i\\beta_r}",
    "unitary row Fourier",
    "\\varepsilon_j=\\frac{2|\\delta K_{z,j}|a}{R^2}",
    "e^{-\\mu(d_2-d_1)}",
    "e^{-2\\mu_j(d_2-d_1)}",
  ]) assert.ok(report.includes(token), token);
  assert.ok(audit.includes("(\\partial_X+i\\alpha\\beta)^2"));
  assert.match(audit, /direct sum has constant one/);
  assert.ok(audit.includes("without a row-count loss"));
  assert.ok(audit.includes("exact constant nondecaying mode"));
  assert.ok(producer.includes('"normalizedSquaredNorm": "1"'));
  assert.ok(producer.includes('"allPhysicalRowsUniformContraction": False'));
});

test("R0.72X imports A1 only on fixed margins and concatenates the true cocycle", async () => {
  const [report, literature, gap] = await Promise.all([
    text("research/r072x_report-source.md"),
    text("research/r072x_literature_audit.md"),
    text("research/r072x_gap_matrix.md"),
  ]);
  for (const token of [
    "K_*=[-\\log2,1-\\log2]",
    "\\delta=\\frac18",
    "Coble--He",
    "e^{-c_{A_1,\\delta}\\sqrt{\\varepsilon_c}",
    "U(1-\\log2,\\delta)",
    "U(\\delta,h_\\alpha)",
    "U(h_\\alpha,-h_\\alpha)",
    "U(-h_\\alpha,-\\delta)",
    "U(-\\delta,-\\log2)",
  ]) assert.ok(report.includes(token), token);
  assert.ok(report.includes("periodic representative \\(\\beta=0\\)"));
  assert.ok(report.includes("no Bloch-uniform extension"));
  assert.ok(report.includes("cellwise scalar gauges in Section 3 are unitary"));
  assert.match(literature, /Coble--He, Theorem 1\.2/);
  assert.match(literature, /does \*\*not\*\* cover the shrinking interface/);
  assert.match(gap, /failure of the black-box hypotheses, not failure of ED/);
});

test("R0.72X source package binds the agreed release, figure, and test names", async () => {
  for (const relative of [
    "research/r072x_report-source.md",
    "research/r072x_gap_matrix.md",
    "research/r072x_literature_audit.md",
    "research/r072x_independent_audit.md",
    `${certificate}/generate_certificate.py`,
    `${certificate}/independent_recompute.py`,
    `${certificate}/validate_certificate.py`,
    `${figure}/contract.json`,
    `${figure}/config.json`,
    `${figure}/plot.py`,
    `${figure}/validate.py`,
    "scripts/generate_r072x_figure.py",
    "scripts/generate_r072x_release.py",
    "scripts/add-r072x-translations.mjs",
    "scripts/i18n-snapshots/r072x-missing.json",
    "tests/r072x-all-center-figure-source.test.mjs",
    "tests/r072x-exact-path-gate.test.mjs",
    "tests/r072x-release.test.mjs",
  ]) assert.equal(await exists(relative), true, relative);

  const [contract, config, producer, generator] = await Promise.all([
    json(`${figure}/contract.json`),
    json(`${figure}/config.json`),
    text(`${certificate}/generate_certificate.py`),
    text("scripts/generate_r072x_release.py"),
  ]);
  assert.equal(contract.figureId, figureId);
  assert.equal(config.figureId, figureId);
  assert.ok(producer.includes('"tests/r072x-exact-path-gate.test.mjs"'));
  assert.ok(producer.includes('"tests/r072x-all-center-figure-source.test.mjs"'));
  assert.ok(generator.includes(`FIGURE_ID = "${figureId}"`));
  assert.ok(generator.includes(`FIGURE_RELATIVE = f"figures/r072x-all-center/{FIGURE_ID}"`));
});

test("R0.72X manifest is exact at source or formal lifecycle", async () => {
  const manifest = await json("research/release-manifest.json");
  const observed = {
    latest: manifest.latestCompletedRelease,
    version: manifest.siteVersion,
    notes: manifest.publicHtmlNoteCount,
    recap: manifest.postR060RecapNodeCount,
    next: manifest.nextRelease,
    gate: manifest.latestReleaseGate,
    publicationTest: manifest.latestReleasePublicationTest,
    published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  };
  if (observed.latest === "r072w") {
    assert.deepEqual(observed, {
      latest: "r072w", version: "1.36", notes: 173, recap: 113,
      next: "r072x",
      gate: "tests/r072w-exact-periodic-gate.test.mjs",
      publicationTest: "tests/r072w-release.test.mjs",
      published: 75, sealed: 51, backlog: 24,
    });
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
  } else {
    assert.deepEqual(observed, {
      latest: "r072x", version: "1.37", notes: 174, recap: 114,
      next: "r072y",
      gate: "tests/r072x-exact-path-gate.test.mjs",
      publicationTest: "tests/r072x-release.test.mjs",
      published: 76, sealed: 52, backlog: 24,
    });
    assert.equal(manifest.nextReleaseSourceStage, undefined);
  }
  if (process.env.R072X_REQUIRE_SOURCE_STAGE === "1") {
    assert.equal(observed.latest, "r072w");
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
  }
});
