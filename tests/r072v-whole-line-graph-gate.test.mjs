import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const run = promisify(execFile);
const python = process.env.CODEX_PYTHON || "python3";
const certificate = "research/certificates/r072v";
const figure = "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization";
const figureId = "fig-r072v-unit-chart-globalization";

const expectedSourceStage = {
  release: "r072v",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r072v_report-source.md",
  literatureAudit: "research/r072v_literature_audit.md",
  gapMatrix: "research/r072v_gap_matrix.md",
  independentAudit: "research/r072v_independent_audit.md",
  producer: "research/certificates/r072v/generate_certificate.py",
  independentProducer: "research/certificates/r072v/independent_recompute.py",
  comparator: "research/certificates/r072v/validate_certificate.py",
  certificateDirectory: "research/certificates/r072v",
  figureDirectory: figure,
  generator: "scripts/generate_r072v_release.py",
  translationScript: "scripts/add-r072v-translations.mjs",
  releaseGate: "tests/r072v-whole-line-graph-gate.test.mjs",
  publicationTest: "tests/r072v-release.test.mjs",
};

const certificateOutputs = [
  "certificate.json", "independent.json", "crosscheck.json", "manifest.json", "SHA256SUMS",
];
const figureOutputs = [
  "data.csv", "results.json", "validation.json", "progress.ndjson",
  "resource-log.ndjson", "qa-report.md", "figure.svg", "figure.pdf",
  "figure.png", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
  "manifest.json", "SHA256SUMS",
];

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function maybeJson(relative) {
  try {
    return await json(relative);
  } catch (error) {
    if (error?.code === "ENOENT") return null;
    throw error;
  }
}

async function absent(relative) {
  await assert.rejects(
    access(resolve(root, relative)),
    (error) => error?.code === "ENOENT",
    relative,
  );
}

async function verifyFlatHashLedger(relative) {
  const directory = resolve(root, relative);
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, "malformed SHA256SUMS row: " + row);
    const [, expected, name] = match;
    const actual = createHash("sha256")
      .update(await readFile(resolve(directory, name))).digest("hex");
    assert.equal(actual, expected, name);
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries
      .filter((entry) => entry.isFile() && !["SHA256SUMS", ".DS_Store"].includes(entry.name))
      .map((entry) => entry.name).sort(),
  );
}

test("R0.72V states the coefficient-uniform unit-chart and whole-line graph theorems", async () => {
  const [report, gap, audit, literature] = await Promise.all([
    text("research/r072v_report-source.md"),
    text("research/r072v_gap_matrix.md"),
    text("research/r072v_independent_audit.md"),
    text("research/r072v_literature_audit.md"),
  ]);
  for (const token of [
    "twoParameterUnitChartCoercivity",
    "wholeLineGraphCoercivity",
    "wholeLineSolutionObservability",
    "wholeLineBlockContraction",
    "cutoffCommutatorAbsorption",
    "timeLengthUniformity",
  ]) assert.ok(report.includes(token), token);
  for (const [label, status] of [
    ["twoParameterUnitChartCoercivity", "CLOSED"],
    ["wholeLineGraphCoercivity", "CLOSED"],
    ["wholeLineSolutionObservability", "CLOSED"],
    ["wholeLineBlockContraction", "CLOSED"],
    ["cutoffCommutatorAbsorption", "CLOSED"],
    ["timeLengthUniformity", "FALSE"],
    ["higherOrderRemainderStability", "OPEN"],
    ["periodicTransfer", "OPEN"],
    ["Clay", "OPEN"],
  ]) assert.ok(
    report.includes(`\\texttt{${label}}&=\\texttt{${status}}`),
    `${label}=${status}`,
  );
  assert.match(gap, /\| Whole-line graph theorem \| \*\*CLOSED\*\*/);
  assert.ok(gap.includes("| Energy evolution and block contraction | **CLOSED for all \\(L^2\\) data in the exact scalar model**"));
  assert.ok(gap.includes("| Uniformity as \\(T\\downarrow0\\) | **FALSE**"));
  assert.match(audit, /whole-line direct-sum globalization are \*\*PASS\*\*/);
  assert.match(audit, /energy-solution block contraction.*\\mathrm\{PASS\}/s);
  assert.match(audit, /block contraction from graph membership alone.*\\mathrm\{FAIL\}/s);
  assert.match(literature, /bounded search|有界的一手文献检索/i);
  assert.match(literature, /not a novelty|不.*novelty|不是.*优先权/i);
});

test("R0.72V fixes the gauge sign, probe, endpoint, and direct sum", async () => {
  const [report, audit] = await Promise.all([
    text("research/r072v_report-source.md"),
    text("research/r072v_independent_audit.md"),
  ]);
  assert.ok(report.includes("w(t,y)=e^{-i\\sigma a\\mu_2t}v(t,y)"));
  assert.ok(report.includes("y^3+a(y^2-\\mu_2)+(b+6t)y"));
  assert.match(report, /q_0\s*\\ge0/);
  assert.match(report, /Choose a real even function/);
  assert.ok(report.includes("\\int_Jq_0(y)\\,dy=1"));
  assert.ok(report.includes("\\alpha^2(\\mu_4-\\mu_2^2)+\\beta^2\\mu_2"));
  assert.ok(report.includes("No assumption \\(\\lambda\\delta\\to0\\) is made"));
  assert.ok(report.includes("a_k=3k"));
  assert.ok(report.includes("b_{k,c}=3k^2+6c"));
  assert.ok(report.includes(
    "\\|\\phi\\|_{H_0^1(J)}^2=\\|\\phi\\|_{L^2(J)}^2+\\|\\phi_y\\|_{L^2(J)}^2",
  ));
  assert.match(report, /monotone convergence over finite\s+sets gives the full statement/);
  assert.match(audit, /sign in \(2\.5\) is correct/i);
  assert.ok(audit.includes("\\text{arbitrary-}\\lambda\\delta\\text{ endpoint closure}&:\\ \\mathrm{PASS}"));
  assert.match(audit, /standard nonhomogeneous norm|full inherited.*H\^1/is);
  assert.match(audit, /maximal distributional domain/);
  assert.match(audit, /does not require, and does not imply,[\s\S]*endpoint trace/);
});

test("R0.72V separates maximal graph coercivity from all-data energy evolution", async () => {
  const [report, gap, audit] = await Promise.all([
    text("research/r072v_report-source.md"),
    text("research/r072v_gap_matrix.md"),
    text("research/r072v_independent_audit.md"),
  ]);
  for (const token of [
    "Proposition 9.1", "Aubin--Lions", "Steklov averaging",
    "strong \\(L^2\\) continuity",
  ]) assert.ok(report.includes(token), token);
  assert.ok(report.includes(
    "\\|u(t_2)\\|_2^2\n +2\\int_{t_1}^{t_2}\\|u_x(t)\\|_2^2\\,dt\n =\\|u(t_1)\\|_2^2",
  ));
  assert.ok(report.includes("E(T)\\le\\frac{C_T^2}{T+C_T^2}E(-T)"));
  assert.match(report, /neither\s+is inferred from maximal graph membership alone/);
  assert.match(gap, /Maximal graph membership alone still does not imply a time trace or energy identity/);
  assert.ok(audit.includes("PASS for every \\(L^2\\) initial datum"));
  assert.match(audit, /not an automatic property of every element of the maximal graph/);
});

test("R0.72V keeps the short-time lower bound compatible with fixed T", async () => {
  const [report, gap, audit] = await Promise.all([
    text("research/r072v_report-source.md"),
    text("research/r072v_gap_matrix.md"),
    text("research/r072v_independent_audit.md"),
  ]);
  assert.ok(report.includes("L=T^{-1/3}"));
  assert.ok(report.includes("C_T\\ge c_fT^{-1/3}"));
  assert.ok(report.includes("fully compatible with Theorem 1.1, which fixes \\(T>0\\)"));
  assert.match(audit, /does not claim a matching\s+upper bound or a sharp contraction asymptotic/);
  assert.ok(gap.includes("C_T\\gtrsim T^{-1/3}"));
  assert.match(audit, /proves only the lower bound[\s\S]*does not claim a matching\s+upper bound/i);
});

test("R0.72V keeps periodic, H5/H7/R9, nonlinear, and Clay claims open", async () => {
  const [report, gap, audit] = await Promise.all([
    text("research/r072v_report-source.md"),
    text("research/r072v_gap_matrix.md"),
    text("research/r072v_independent_audit.md"),
  ]);
  assert.ok(gap.includes("| \\(H_5,H_7,R_9\\) stability | **OPEN**"));
  assert.match(gap, /\| Periodic exact-heat-path transfer \| \*\*OPEN\*\*/);
  assert.match(gap, /\| Nonlinear Navier--Stokes \/ Clay \| \*\*OPEN\*\*/);
  for (const source of [report, gap]) {
    for (const token of ["H_5", "H_7", "R_9"]) assert.ok(source.includes(token), token);
    assert.match(source, /periodic/i);
    assert.match(source, /nonlinear Navier--Stokes/i);
    assert.match(source, /Clay/i);
  }
  assert.match(audit, /higher-order model remainders/);
  assert.match(audit, /periodic heat-path theorem/);
  assert.match(audit, /nonlinear Navier--Stokes/);
  assert.match(audit, /Clay-level/);
});

test("R0.72V certificate and figure lifecycle are fail-closed with two-commit lineage", async () => {
  const certificateManifest = await maybeJson(certificate + "/manifest.json");
  if (!certificateManifest) {
    for (const name of certificateOutputs) await absent(certificate + "/" + name);
    const producer = await run(python, [
      certificate + "/generate_certificate.py", "--self-test",
    ], { cwd: root });
    assert.match(producer.stdout, /passed \(no outputs written\)/);
    await assert.rejects(run(python, [
      certificate + "/validate_certificate.py", "--require-formal",
    ], { cwd: root }));
  } else {
    const crosscheck = await json(certificate + "/crosscheck.json");
    assert.equal(certificateManifest.status, "formal");
    assert.match(certificateManifest.sourceCommit, /^[0-9a-f]{40}$/);
    assert.ok(certificateManifest.sourceBindings.length > 0);
    assert.equal(crosscheck.status, "passed");
    assert.equal(crosscheck.formalSourceReady, true);
    assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
    assert.equal(crosscheck.sourceCommit, certificateManifest.sourceCommit);
    assert.deepEqual(crosscheck.sourceBindings, certificateManifest.sourceBindings);
    assert.ok(Object.values(crosscheck.checks).every((value) => value === true));
    await verifyFlatHashLedger(certificate);
    await run(python, [
      certificate + "/validate_certificate.py", "--require-formal",
    ], { cwd: root });
  }

  const figureManifest = await maybeJson(figure + "/manifest.json");
  if (!figureManifest) {
    for (const name of figureOutputs) await absent(figure + "/" + name);
    const presentation = await run(python, [
      "scripts/generate_r072v_figure.py", "--self-test",
    ], { cwd: root });
    assert.match(presentation.stdout, /passed \(2592 in-memory rows; no outputs written\)/);
    await assert.rejects(run(python, [
      figure + "/validate.py", "--require-formal",
    ], { cwd: root }));
    return;
  }

  assert.ok(["draft", "formal"].includes(figureManifest.status));
  await verifyFlatHashLedger(figure);
  if (figureManifest.status === "draft") {
    await assert.rejects(run(python, [figure + "/validate.py", "--require-formal"], { cwd: root }));
    return;
  }
  assert.ok(certificateManifest, "formal figure requires formal certificate");
  assert.equal(figureManifest.release, "R0.72V");
  assert.equal(figureManifest.figureId, figureId);
  assert.equal(figureManifest.git.sourceCommit, certificateManifest.sourceCommit);
  assert.match(figureManifest.git.certificateCommit, /^[0-9a-f]{40}$/);
  assert.notEqual(figureManifest.git.certificateCommit, figureManifest.git.sourceCommit);
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.publication.publicCopiesComplete, true);
  assert.equal(figureManifest.publication.directory, "public/assets/r072v");
  assert.equal(figureManifest.claimBoundary.analyticEnergyBlockContractionProvedForDeclaredClass, true);
  assert.equal(figureManifest.claimBoundary.periodicTransferProved, false);
  assert.equal(figureManifest.claimBoundary.nonlinearNavierStokesClosureProved, false);
  assert.equal(figureManifest.claimBoundary.clayMillenniumProblemSolved, false);
  const png = figureManifest.figure.outputs.find((output) => output.path === "figure.png");
  assert.equal(png?.dpi, 600);
  await run(python, [figure + "/validate.py", "--require-formal"], { cwd: root });
});

test("R0.72V manifest is source-staged from R0.72U or atomically formal", async () => {
  const manifest = await json("research/release-manifest.json");
  assert.ok(["r072u", "r072v"].includes(manifest.latestCompletedRelease));
  if (manifest.latestCompletedRelease === "r072u") {
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
    assert.deepEqual({
      version: manifest.siteVersion,
      notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount,
      next: manifest.nextRelease,
      gate: manifest.latestReleaseGate,
      publicationTest: manifest.latestReleasePublicationTest,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    }, {
      version: "1.34", notes: 171, recap: 111, next: "r072v",
      gate: "tests/r072u-local-observability-gate.test.mjs",
      publicationTest: "tests/r072u-release.test.mjs",
      published: 73, sealed: 49, backlog: 24,
    });
    const [site, notes, home, recap] = await Promise.all([
      json("public/site-version.json"),
      readdir(resolve(root, "public/notes")),
      text("public/research-review.html"),
      text("public/recap-r0-61-r0-72u.html"),
    ]);
    assert.equal(site.version, "1.34");
    assert.equal(site.latestRelease, "R0.72U");
    assert.equal(site.publicHtmlNoteCount, 171);
    assert.equal(notes.filter((name) => name.endsWith(".html")).length, 171);
    assert.match(home, /<strong>171<\/strong>公开研究笔记/);
    assert.match(home, /<strong>R0\.72U<\/strong>最新研究节点/);
    assert.doesNotMatch(home, /data-release="r072v"/);
    const start = recap.indexOf('<section id="node-index">');
    const end = recap.indexOf("</section>", start);
    const links = [...recap.slice(start, end).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
      .map((match) => match[1]);
    assert.equal(links.length, 111);
    assert.equal(new Set(links).size, 111);
    for (const relative of [
      "public/notes/r0-72v.html", "public/notes/r0-72v.pdf",
      "public/recap-r0-61-r0-72v.html", "public/recap-r0-61-r0-72v.pdf",
    ]) await absent(relative);
    return;
  }
  assert.deepEqual({
    latest: manifest.latestCompletedRelease,
    siteVersion: manifest.siteVersion,
    notes: manifest.publicHtmlNoteCount,
    recap: manifest.postR060RecapNodeCount,
    next: manifest.nextRelease,
    gate: manifest.latestReleaseGate,
    publicationTest: manifest.latestReleasePublicationTest,
    published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  }, {
    latest: "r072v", siteVersion: "1.35", notes: 172, recap: 112,
    next: "r072w",
    gate: "tests/r072v-whole-line-graph-gate.test.mjs",
    publicationTest: "tests/r072v-release.test.mjs",
    published: 74, sealed: 50, backlog: 24,
  });
  assert.equal(manifest.nextReleaseSourceStage, undefined);
});
