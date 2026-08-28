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
const certificate = "research/certificates/r072w";
const figure = "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer";
const figureId = "fig-r072w-exact-tail-transfer";
const figureGenerator = "scripts/generate_r072w_figure.py";

const expectedSourceStage = {
  release: "r072w",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r072w_report-source.md",
  literatureAudit: "research/r072w_literature_audit.md",
  gapMatrix: "research/r072w_gap_matrix.md",
  independentAudit: "research/r072w_independent_audit.md",
  producer: "research/certificates/r072w/generate_certificate.py",
  independentProducer: "research/certificates/r072w/independent_recompute.py",
  comparator: "research/certificates/r072w/validate_certificate.py",
  certificateDirectory: certificate,
  figureDirectory: figure,
  generator: "scripts/generate_r072w_release.py",
  translationScript: "scripts/add-r072w-translations.mjs",
  releaseGate: "tests/r072w-exact-periodic-gate.test.mjs",
  publicationTest: "tests/r072w-release.test.mjs",
};

const certificateOutputs = [
  "certificate.json",
  "independent.json",
  "crosscheck.json",
  "manifest.json",
  "SHA256SUMS",
];
const figureOutputs = [
  "data.csv",
  "results.json",
  "validation.json",
  "progress.ndjson",
  "resource-log.ndjson",
  "qa-report.md",
  "figure.svg",
  "figure.pdf",
  "figure.png",
  "qa-final-size.png",
  "qa-grayscale.png",
  "qa-pdf.png",
  "manifest.json",
  "SHA256SUMS",
];

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
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
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

async function assertNoPublicFigure() {
  for (const extension of ["svg", "pdf", "png"]) {
    await absent(`public/assets/r072w/${figureId}.${extension}`);
  }
}

async function assertFormalPublicFigure() {
  for (const extension of ["svg", "pdf", "png"]) {
    const master = await readFile(resolve(root, `${figure}/figure.${extension}`));
    const publication = await readFile(
      resolve(root, `public/assets/r072w/${figureId}.${extension}`),
    );
    assert.deepEqual(publication, master, `public ${extension} must equal the formal master`);
  }
}

test("R0.72W freezes the exact heat path and its claim labels", async () => {
  const [report, gap, audit] = await Promise.all([
    text("research/r072w_report-source.md"),
    text("research/r072w_gap_matrix.md"),
    text("research/r072w_independent_audit.md"),
  ]);

  for (const token of [
    "V_\\alpha(S,X)=\\alpha^{-3}",
    "2e^{-\\alpha^2S}\\sin(\\alpha X)",
    "-e^{-4\\alpha^2S}\\sin(2\\alpha X)",
    "\\partial_SV_\\alpha=\\partial_X^2V_\\alpha",
    "H_3-\\frac{\\alpha^2}{4}H_5",
    "+\\frac{\\alpha^4}{40}H_7",
    "-\\frac{17}{12096}\\alpha^6H_9",
  ]) assert.ok(report.includes(token), token);

  for (const [label, status] of [
    ["weightedNonabsorbedRemainderEstimate", "CLOSED"],
    ["growingCoreAbsorption", "CLOSED"],
    ["globalTermwiseRemainderAbsorption", "FALSE"],
    ["exactFamilyUnitCellCoercivity", "CLOSED"],
    ["exactWholeLineGraphCoercivity", "CLOSED"],
    ["exactPeriodicGraphCoercivity", "CLOSED"],
    ["exactPeriodicBlockContraction", "CLOSED"],
    ["outerTimeConcatenation", "OPEN"],
    ["nonlinearNavierStokes", "OPEN"],
    ["Clay", "OPEN"],
  ]) assert.ok(
    report.includes(`\\texttt{${label}}&=\\texttt{${status}}`),
    `${label}=${status}`,
  );

  assert.match(gap, /\| Exact rescaled potential \| \*\*CLOSED identity\*\*/);
  assert.match(gap, /\| Heat identity \| \*\*CLOSED identity\*\*/);
  assert.match(audit, /sign and the torus length \$2\\pi\/\\alpha\$ are correct/);
  assert.match(audit, /exact periodic energy-block contraction/);
});

test("R0.72W keeps the weighted theorem and global no-go logically separate", async () => {
  const [report, gap, audit] = await Promise.all([
    text("research/r072w_report-source.md"),
    text("research/r072w_gap_matrix.md"),
    text("research/r072w_independent_audit.md"),
  ]);

  for (const token of [
    "2\\bigl(e^T+256e^{4T}\\bigr)\\alpha^6",
    "\\|W_{5,T}v\\|_2",
    "\\|W_{7,T}v\\|_2",
    "\\|\\Omega_{9,T}v\\|_2",
    "R=o(\\kappa^{2/25})",
    "D_{\\alpha,T}(R)=\\frac{r^5}{4}+o(1)",
    "-1-\\frac{4}{3\\pi^2}",
    "\\frac{5\\pi^2}{12}+o(1)>4",
  ]) assert.ok(report.includes(token), token);
  assert.match(report, /adjective `nonabsorbed` is essential/);
  assert.match(report, /whole-line polynomial correction is not a relatively small perturbation/);
  assert.match(report, /invariant under time-only scalar gauges/);
  assert.match(gap, /\| Weighted nonabsorbed graph estimate \| \*\*CLOSED\*\*/);
  assert.match(gap, /\| Whole-line termwise absorption \| \*\*FALSE\*\*/);
  assert.match(gap, /\| One-period vanishing absorption \| \*\*FALSE\*\*/);
  assert.match(gap, /\| Exact-tail relative smallness \| \*\*FALSE\*\*/);
  assert.match(audit, /valid for all\s+\$X\\in\\mathbb R\$/);
  assert.match(audit, /Global termwise absorption is FALSE/);
});

test("R0.72W closes the exact cell, whole-line, and expanding-torus graph chain", async () => {
  const [report, gap, audit] = await Promise.all([
    text("research/r072w_report-source.md"),
    text("research/r072w_gap_matrix.md"),
    text("research/r072w_independent_audit.md"),
  ]);

  for (const token of [
    "|V_{XXX}|\\le M_{3,T}:=2e^T+8e^{4T}",
    "|V_{XXXX}|\\le\\alpha M_{4,T}",
    "\\partial_SV_{\\alpha,X}=V_{\\alpha,XXX}",
    "\\mu_{2,\\ell}=\\frac{\\ell^2}{44}",
    "\\mu_{4,\\ell}=\\frac{3\\ell^4}{2288}",
    "\\frac{5\\ell^4}{6292}",
    "H_D^{-1}(J_\\ell)",
    "\\|\\cdot\\|_{H^1(J_\\ell)}",
    "v\\in L^2(I;H^1(J_\\ell))",
    "Theorem 7.1: uniform exact-family cell coercivity",
    "Theorem 9.1: uniform exact-periodic graph coercivity",
    "N_\\alpha=\\lfloor L_\\alpha\\rfloor",
    "1\\le\\ell_\\alpha<2",
    "H^{-1}(\\mathbb T_\\alpha)=(H^1(\\mathbb T_\\alpha))^*",
  ]) assert.ok(report.includes(token), token);
  assert.match(report, /No spatial or temporal trace/);
  assert.ok(report.includes("no hypothesis \\(\\lambda_n\\delta_n\\to0\\) is used"));
  assert.match(gap, /\| Bounded-cell alternative \| \*\*CLOSED\*\*/);
  assert.match(gap, /\| Escaping-cell alternative \| \*\*CLOSED\*\*/);
  assert.match(gap, /\| Exact whole-line graph theorem \| \*\*CLOSED\*\*/);
  assert.match(gap, /\| Exact periodic graph theorem \| \*\*CLOSED\*\*/);
  assert.match(audit, /same proof works on the whole line and on a finite partition of a torus/);
  assert.match(audit, /All vanish without requiring\s+\$\\lambda\\delta\\to0\$/);
});

test("R0.72W separates graph membership, all-data energy evolution, and physical transfer", async () => {
  const [report, gap, audit] = await Promise.all([
    text("research/r072w_report-source.md"),
    text("research/r072w_gap_matrix.md"),
    text("research/r072w_independent_audit.md"),
  ]);

  for (const token of [
    "For every $u_-\\in L^2(\\mathbb T_\\alpha)$",
    "u\\in C(\\overline I;L^2(\\mathbb T_\\alpha))",
    "\\|u_{XX}\\|_{H^{-1}(\\mathbb T_\\alpha)}",
    "E(T)\\le",
    "{T+(C_T^{\\rm per})^2}E(-T)",
    "q_T:=\\frac{C_T^{\\rm per}}",
    "V_\\alpha(S,X)=-4\\alpha^{-3}W(\\alpha^2S,\\alpha X)",
    "\\|v(T\\kappa^{-2/5})\\|_{L^2(\\mathbb T_{2\\pi})}",
  ]) assert.ok(report.includes(token), token);
  assert.ok(report.includes("existence of \\(C_T^{\\rm per}\\) is nonconstructive"));
  assert.match(report, /does not yet concatenate the block with the pre-collision/);
  assert.match(gap, /\| Energy evolution \| \*\*CLOSED for all torus \$L\^2\$ data\*\*/);
  assert.match(gap, /\| Periodic collision-block contraction \| \*\*CLOSED\*\*/);
  assert.match(gap, /\| Return to physical variables \| \*\*CLOSED exact conjugacy\*\*/);
  assert.match(gap, /\| Uniformity as \$T\\downarrow0\$ \| \*\*FALSE\*\*/);
  assert.match(audit, /factor is strictly below one for every fixed \$T>0\$/);
  assert.match(audit, /No explicit value\s+of the nonconstructive \$C_T\$ is asserted/);
});

test("R0.72W treats numerics and literature as bounded evidence, not proof or priority", async () => {
  const [report, gap, audit, literature] = await Promise.all([
    text("research/r072w_report-source.md"),
    text("research/r072w_gap_matrix.md"),
    text("research/r072w_independent_audit.md"),
    text("research/r072w_literature_audit.md"),
  ]);

  assert.match(report, /Fourier Strang-splitting calculation was used only as a stress test/);
  assert.match(report, /not used to prove \(9\.6\) or \(10\.8\)/);
  assert.match(gap, /\| Numerical operator-norm stress test \| \*\*PASS as diagnostic\*\*/);
  assert.match(audit, /NOT a machine-assisted proof/);
  assert.match(literature, /bounded search of primary papers and preprints/i);
  assert.match(literature, /not a novelty, priority, or nonexistence proof/i);
  for (const token of [
    "arXiv:1510.08098",
    "10.1007/s00205-017-1099-y",
    "arXiv:2105.12308",
    "10.1016/j.jfa.2022.109522",
    "arXiv:2309.15738",
    "10.4310/CMS.2024.v22.n6.a10",
    "arXiv:2203.15938",
    "10.1016/j.jfa.2023.109856",
  ]) assert.ok(literature.includes(token), token);
  assert.match(literature, /fixed finite\s+number \$N\$ of nondegenerate critical points/);
  assert.match(literature, /assumptions fail exactly when two points merge/);
  assert.match(literature, /none directly replaces the\s+compact--escaping unit-cell proof/i);
  assert.match(gap, /\| Outer heat-time concatenation \| \*\*OPEN\*\*/);
  assert.match(gap, /\| Complete linearized shear subsystem \| \*\*OPEN\*\*/);
  assert.match(gap, /\| Nonlinear Navier--Stokes \/ Clay \| \*\*OPEN\*\*/);
  assert.match(
    audit,
    /Outer-time\s+concatenation, the complete linearized shear system, nonlinear closure, and\s+the Clay problem remain open/,
  );
  assert.match(report, /R0\.72X: outer/);
});

test("R0.72W certificate and figure lifecycle is fail-closed through formal sealing", async () => {
  const certificateManifest = await maybeJson(`${certificate}/manifest.json`);
  if (!certificateManifest) {
    for (const name of certificateOutputs) await absent(`${certificate}/${name}`);
    if (await exists(`${certificate}/independent_recompute.py`)) {
      const independent = await run(python, [
        `${certificate}/independent_recompute.py`, "--self-test",
      ], { cwd: root });
      assert.match(independent.stdout, /passed.*no outputs written/i);
    }
    if (await exists(`${certificate}/generate_certificate.py`)) {
      const producer = await run(python, [
        `${certificate}/generate_certificate.py`, "--self-test",
      ], { cwd: root });
      assert.match(producer.stdout, /passed.*no outputs written/i);
    }
    if (await exists(`${certificate}/validate_certificate.py`)) {
      await assert.rejects(run(python, [
        `${certificate}/validate_certificate.py`, "--require-formal",
      ], { cwd: root }));
    }
  } else {
    const crosscheck = await json(`${certificate}/crosscheck.json`);
    assert.equal(certificateManifest.status, "formal");
    assert.match(certificateManifest.sourceCommit, /^[0-9a-f]{40}$/);
    assert.ok(Array.isArray(certificateManifest.sourceBindings));
    assert.ok(certificateManifest.sourceBindings.length > 0);
    assert.equal(crosscheck.status, "passed");
    assert.equal(crosscheck.formalSourceReady, true);
    assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
    assert.equal(crosscheck.sourceCommit, certificateManifest.sourceCommit);
    assert.deepEqual(crosscheck.sourceBindings, certificateManifest.sourceBindings);
    assert.ok(Object.values(crosscheck.checks).every((value) => value === true));
    await verifyFlatHashLedger(certificate);
    await run(python, [
      `${certificate}/validate_certificate.py`, "--require-formal",
    ], { cwd: root });
  }

  const figureManifest = await maybeJson(`${figure}/manifest.json`);
  if (!figureManifest) {
    for (const name of figureOutputs) await absent(`${figure}/${name}`);
    await assertNoPublicFigure();
    if (await exists(figureGenerator)) {
      const presentation = await run(python, [figureGenerator, "--self-test"], {
        cwd: root,
      });
      assert.match(presentation.stdout, /passed.*no outputs written/i);
    }
    if (await exists(`${figure}/validate.py`)) {
      await assert.rejects(run(python, [
        `${figure}/validate.py`, "--require-formal",
      ], { cwd: root }));
    }
    return;
  }

  assert.ok(["draft", "formal"].includes(figureManifest.status));
  await verifyFlatHashLedger(figure);
  if (figureManifest.status === "draft") {
    await assertNoPublicFigure();
    await assert.rejects(run(python, [
      `${figure}/validate.py`, "--require-formal",
    ], { cwd: root }));
    return;
  }

  assert.ok(certificateManifest, "formal figure requires a formal certificate");
  assert.equal(figureManifest.release, "R0.72W");
  assert.equal(figureManifest.figureId, figureId);
  assert.equal(figureManifest.git.sourceCommit, certificateManifest.sourceCommit);
  assert.match(figureManifest.git.certificateCommit, /^[0-9a-f]{40}$/);
  assert.notEqual(figureManifest.git.certificateCommit, figureManifest.git.sourceCommit);
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.publication.publicCopiesComplete, true);
  assert.equal(figureManifest.publication.directory, "public/assets/r072w");
  assert.equal(
    figureManifest.claimBoundary.exactPeriodicBlockContractionProved,
    true,
  );
  assert.equal(figureManifest.claimBoundary.numericalDiagnosticIsProof, false);
  assert.equal(
    figureManifest.claimBoundary.numericalDiagnosticDeterminesAnalyticConstant,
    false,
  );
  assert.equal(figureManifest.claimBoundary.outerTimeConcatenationProved, false);
  assert.equal(figureManifest.claimBoundary.timeLengthUniformity, false);
  assert.equal(figureManifest.claimBoundary.nonlinearNavierStokesClosureProved, false);
  assert.equal(figureManifest.claimBoundary.clayMillenniumProblemSolved, false);
  const png = figureManifest.figure.outputs.find((output) => output.path === "figure.png");
  assert.equal(png?.dpi, 600);
  await run(python, [`${figure}/validate.py`, "--require-formal"], { cwd: root });
});

test("R0.72W linked pages and counters stay frozen until atomic formal publication", async () => {
  const manifest = await json("research/release-manifest.json");
  assert.ok(["r072v", "r072w"].includes(manifest.latestCompletedRelease));
  if (manifest.latestCompletedRelease === "r072v") {
    if (manifest.nextReleaseSourceStage !== undefined) {
      assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
    }
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
      version: "1.35",
      notes: 172,
      recap: 112,
      next: "r072w",
      gate: "tests/r072v-whole-line-graph-gate.test.mjs",
      publicationTest: "tests/r072v-release.test.mjs",
      published: 74,
      sealed: 50,
      backlog: 24,
    });
    for (const relative of [
      "public/notes/r0-72w.html",
      "public/notes/r0-72w.pdf",
      "public/recap-r0-61-r0-72w.html",
      "public/recap-r0-61-r0-72w.pdf",
    ]) await absent(relative);
    const figureManifest = await maybeJson(`${figure}/manifest.json`);
    if (figureManifest?.status === "formal") {
      assert.equal(figureManifest.publication?.publicCopiesComplete, true);
      await assertFormalPublicFigure();
    } else {
      await assertNoPublicFigure();
    }
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
    latest: "r072w",
    siteVersion: "1.36",
    notes: 173,
    recap: 113,
    next: "r072x",
    gate: "tests/r072w-exact-periodic-gate.test.mjs",
    publicationTest: "tests/r072w-release.test.mjs",
    published: 75,
    sealed: 51,
    backlog: 24,
  });
  assert.equal(manifest.nextReleaseSourceStage, undefined);
});
