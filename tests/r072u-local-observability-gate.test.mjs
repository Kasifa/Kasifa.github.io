import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { access, copyFile, mkdir, mkdtemp, readFile, readdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const run = promisify(execFile);

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function absent(relative) {
  await assert.rejects(access(resolve(root, relative)), (error) => error?.code === "ENOENT", relative);
}

const expectedSourceStage = {
  release: "r072u",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r072u_report-source.md",
  literatureAudit: "research/r072u_literature_audit.md",
  gapMatrix: "research/r072u_gap_matrix.md",
  independentAudit: "research/r072u_independent_audit.md",
  producer: "research/certificates/r072u/generate_certificate.py",
  independentProducer: "research/certificates/r072u/independent_recompute.py",
  comparator: "research/certificates/r072u/validate_certificate.py",
  certificateDirectory: "research/certificates/r072u",
  figureDirectory: "figures/r072u-local-observability/fig-r072u-two-moment-coercivity",
  generator: "scripts/generate_r072u_release.py",
  translationScript: "scripts/add-r072u-translations.mjs",
  releaseGate: "tests/r072u-local-observability-gate.test.mjs",
  publicationTest: "tests/r072u-release.test.mjs",
};

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

test("R0.72U source rejects the spatial-cutoff tautology and states the uncut theorem", async () => {
  const [report, gap, audit] = await Promise.all([
    text("research/r072u_report-source.md"),
    text("research/r072u_gap_matrix.md"),
    text("research/r072u_independent_audit.md"),
  ]);
  for (const token of [
    "centerUniformLocalGraphCoercivity",
    "localSolutionObservability",
    "wholeLineBlockContraction",
    "P_c",
    "H_D^{-1}",
    "Poincare",
  ]) assert.ok(report.includes(token), token);
  assert.match(report, /without\s+temporal or spatial trace conditions/i);
  assert.match(report, /literal spatial-cutoff/i);
  assert.match(report, /ordinary Poincare/i);
  assert.match(gap, /Literal spatial-cutoff audit/);
  assert.match(gap, /Poincare-trivial|ordinary Poincare/i);
  assert.match(audit, /Literal spatial-cutoff inequality/);
  assert.match(audit, /PASS, trivial/);
  assert.match(audit, /uncut bounded-chart graph estimate/i);
});

test("R0.72U release generator preflights the exact R0.72T source state before public writes", async (t) => {
  const generator = await text("scripts/generate_r072u_release.py");
  const main = generator.slice(generator.indexOf("def main() -> None:"));
  const calls = [
    "preflight_release_state()",
    "validate_inputs()",
    "build_note()",
    "build_recap()",
    "update_home()",
    "update_literature()",
    "update_manifests()",
  ].map((call) => main.indexOf(call));
  assert.ok(calls.every((index) => index >= 0));
  assert.deepEqual(calls, [...calls].sort((left, right) => left - right));
  assert.ok(generator.includes("LITERATURE_T_OVERVIEW"));
  assert.ok(generator.includes("LITERATURE_U_OVERVIEW"));
  assert.ok(generator.includes("R0.72U 随后排除 literal spatial-cutoff"));
  assert.ok(generator.includes("\\(J\\supset[-1,1]\\)"));
  assert.ok(generator.includes("\\(T=1\\)"));
  assert.ok(generator.includes('figure / "validate.py"'));

  const fixture = await mkdtemp(join(tmpdir(), "r072u-preflight-test-"));
  t.after(() => rm(fixture, { recursive: true, force: true }));
  await mkdir(join(fixture, "research"), { recursive: true });
  const baseline = {
    latestCompletedRelease: "r072t",
    siteVersion: "1.33",
    publicHtmlNoteCount: 170,
    postR060RecapNodeCount: 110,
    nextRelease: "r072u",
    latestReleaseGate: "tests/r072t-a2-spacetime-gate.test.mjs",
    latestReleasePublicationTest: "tests/r072t-release.test.mjs",
    postR070APublishedReleaseCount: 72,
    postR070AFormalSealedReleaseCount: 48,
    legacyFormalFigureBacklogCount: 24,
  };
  const command = ["-c", [
    "import sys",
    "sys.path.insert(0, 'scripts')",
    "import generate_r072u_release as release",
    "release.preflight_release_state()",
  ].join("; ")];
  const environment = { ...process.env, R072U_RELEASE_ROOT: fixture };
  const manifestPath = join(fixture, "research", "release-manifest.json");

  await writeFile(manifestPath, JSON.stringify({
    ...baseline,
    nextReleaseSourceStage: { ...expectedSourceStage, unexpectedField: true },
  }));
  await assert.rejects(
    run(process.env.CODEX_PYTHON || "python3", command, { cwd: root, env: environment }),
    (error) => /source-stage manifest contract/.test(String(error.stderr)),
  );

  await writeFile(manifestPath, JSON.stringify({
    ...baseline,
    siteVersion: "1.32",
    nextReleaseSourceStage: expectedSourceStage,
  }));
  await assert.rejects(
    run(process.env.CODEX_PYTHON || "python3", command, { cwd: root, env: environment }),
    (error) => /not at R0\.72T: siteVersion/.test(String(error.stderr)),
  );

  await mkdir(join(fixture, "public", "notes"), { recursive: true });
  await Promise.all(Array.from({ length: 170 }, (_, index) =>
    writeFile(join(fixture, "public", "notes", `fixture-${index}.html`), "")));
  await writeFile(join(fixture, "public", "site-version.json"), JSON.stringify({
    schemaVersion: "research-site-version-v1",
    version: "1.33",
    latestRelease: "R0.72T",
    publicHtmlNoteCount: 170,
    publishedDate: "2026-08-28",
  }));
  const routeLinks = Array.from(
    { length: 80 },
    (_, index) => `<a href="/notes/r0-fixture-${index}.html">fixture</a>`,
  ).join("");
  await writeFile(join(fixture, "public", "research-review.html"), [
    '<main data-site-version="1.33">',
    "<strong>170</strong>公开研究笔记",
    "<strong>R0.72T</strong>最新研究节点",
    `<nav class="route-note-links" aria-label="R0.69P–R0.72T">${routeLinks}</nav>`,
    "</main>",
  ].join(""));
  await copyFile(
    join(root, "public", "recap-r0-61-r0-72t.html"),
    join(fixture, "public", "recap-r0-61-r0-72t.html"),
  );
  const literatureTOverview =
    "这里没有完成 global caustic image，也没有证明 ED through collision。" +
    "R0.72T 进一步固定 exact A2 spacetime germ 与唯一 scaling，核对 quadratic " +
    "wrong-model calibration、physical 3/5 回填、combined fixed-f identity、" +
    "inviscid mixing 和 CDZE 6/7 barrier；block contraction 与 periodic transfer " +
    "仍开放。一般 Navier–Stokes 正则性仍开放。";
  await writeFile(
    join(fixture, "public", "literature-review.html"),
    `${literatureTOverview}<p>开放接口 · R0.72U</p>`,
  );
  await writeFile(
    join(fixture, "research", "formal-archive-inventory.json"),
    JSON.stringify({
      latestPublishedRelease: "r072t",
      publishedReleaseCount: 72,
      formalSealedReleaseCount: 48,
      legacyFormalFigureBacklogCount: 24,
      publishedReleases: [
        ...Array.from({ length: 71 }, (_, index) => `fixture-p-${index}`),
        "r072t",
      ],
      formalSealedReleases: [
        ...Array.from({ length: 47 }, (_, index) => `fixture-f-${index}`),
        "r072t",
      ],
    }),
  );
  await writeFile(manifestPath, JSON.stringify({
    ...baseline,
    nextReleaseSourceStage: expectedSourceStage,
  }));
  await run(process.env.CODEX_PYTHON || "python3", command, {
    cwd: root,
    env: environment,
  });
});

test("R0.72U two-moment proof closes bounded and escaping centers without an L2 endpoint shortcut", async () => {
  const [report, audit] = await Promise.all([
    text("research/r072u_report-source.md"),
    text("research/r072u_independent_audit.md"),
  ]);
  for (const token of ["A'", "B'", "K_c", "endpoint", "bounded centers"]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /centers escaping to infinity/i);
  assert.match(audit, /A'=iLB\+E_0/);
  assert.match(audit, /B'=iL\\mu_2A\+iLF_2\+E_1/);
  assert.match(audit, /does \*\*not\*\* give/);
  assert.ok(audit.includes("v\\in C(\\overline I;L^2(J))"));
  assert.match(audit, /A,B\\in H\^1\(I\)/);
  assert.match(audit, /\\delta\+\\sqrt\{\\frac\{\\delta\}\{\|L\|\}\}/);
  assert.match(audit, /no hidden rate assumption/i);
});

test("R0.72U closes only local solution observability", async () => {
  const [report, gap, audit, literature] = await Promise.all([
    text("research/r072u_report-source.md"),
    text("research/r072u_gap_matrix.md"),
    text("research/r072u_independent_audit.md"),
    text("research/r072u_literature_audit.md"),
  ]);
  assert.match(report, /P_cu=u_\{XX\}/);
  assert.match(report, /local solution observability/i);
  assert.match(gap, /localSolutionObservability.*CLOSED/);
  for (const source of [report, gap, audit]) {
    for (const token of ["wholeLineBlock", "periodicTransfer", "Clay"]) {
      assert.ok(source.includes(token), token);
    }
  }
  assert.match(report, /tail|tails/i);
  assert.match(report, /commutator/i);
  assert.match(audit, /boundary flux/i);
  assert.match(literature, /10\.1016\/j\.jfa\.2022\.109522/);
  assert.match(literature, /bounded search|有界检索/i);
});

test("R0.72U certificate and formal figure remain fail-closed", async () => {
  const certificate = "research/certificates/r072u";
  const figure = "figures/r072u-local-observability/fig-r072u-two-moment-coercivity";
  await verifyFlatHashLedger(certificate);
  await verifyFlatHashLedger(figure);
  const [crosscheck, certificateManifest, manifest] = await Promise.all([
    json(certificate + "/crosscheck.json"),
    json(certificate + "/manifest.json"),
    json(figure + "/manifest.json"),
  ]);
  assert.equal(certificateManifest.status, "formal");
  assert.match(certificateManifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.ok(Array.isArray(certificateManifest.sourceBindings));
  assert.ok(certificateManifest.sourceBindings.length > 0);
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
  assert.equal(crosscheck.formalSourceReady, true);
  assert.equal(crosscheck.sourceCommit, certificateManifest.sourceCommit);
  assert.deepEqual(crosscheck.sourceBindings, certificateManifest.sourceBindings);
  assert.ok(Object.values(crosscheck.checks).every((value) => value === true));
  await run(process.env.CODEX_PYTHON || "python3", [
    "research/certificates/r072u/validate_certificate.py", "--require-formal",
  ], { cwd: root });
  await run(process.env.CODEX_PYTHON || "python3", [
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/validate.py",
    "--require-formal",
  ], { cwd: root });
  assert.equal(manifest.release, "R0.72U");
  assert.equal(manifest.figureId, "fig-r072u-two-moment-coercivity");
  assert.equal(manifest.status, "formal");
  const png = manifest.figure.outputs.find((output) => output.path === "figure.png");
  assert.equal(png?.dpi, 600);
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.visualInspectionExplicit, true);
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.equal(manifest.publication.directory, "public/assets/r072u");
});

test("R0.72U manifest is source-staged from R0.72T or atomically public", async () => {
  const manifest = await json("research/release-manifest.json");
  assert.ok(["r072t", "r072u"].includes(manifest.latestCompletedRelease));
  if (manifest.latestCompletedRelease === "r072t") {
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
    assert.deepEqual({
      version: manifest.siteVersion,
      notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount,
      next: manifest.nextRelease,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    }, {
      version: "1.33", notes: 170, recap: 110, next: "r072u",
      published: 72, sealed: 48, backlog: 24,
    });
    const [site, notes, home, recap] = await Promise.all([
      json("public/site-version.json"),
      readdir(resolve(root, "public/notes")),
      text("public/research-review.html"),
      text("public/recap-r0-61-r0-72t.html"),
    ]);
    assert.equal(site.version, "1.33");
    assert.equal(site.latestRelease, "R0.72T");
    assert.equal(site.publicHtmlNoteCount, 170);
    assert.equal(notes.filter((name) => name.endsWith(".html")).length, 170);
    assert.match(home, /<strong>170<\/strong>公开研究笔记/);
    assert.match(home, /<strong>R0\.72T<\/strong>最新研究节点/);
    assert.doesNotMatch(home, /data-release="r072u"/);
    const start = recap.indexOf('<section id="node-index">');
    const end = recap.indexOf("</section>", start);
    const links = [...recap.slice(start, end).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
      .map((match) => match[1]);
    assert.equal(links.length, 110);
    assert.equal(new Set(links).size, 110);
    for (const relative of [
      "public/notes/r0-72u.html",
      "public/notes/r0-72u.pdf",
      "public/recap-r0-61-r0-72u.html",
      "public/recap-r0-61-r0-72u.pdf",
    ]) await absent(relative);
    return;
  }
  assert.deepEqual({
    latest: manifest.latestCompletedRelease,
    siteVersion: manifest.siteVersion,
    notes: manifest.publicHtmlNoteCount,
    recap: manifest.postR060RecapNodeCount,
    next: manifest.nextRelease,
    published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  }, {
    latest: "r072u",
    siteVersion: "1.34",
    notes: 171,
    recap: 111,
    next: "r072v",
    published: 73,
    sealed: 49,
    backlog: 24,
  });
  assert.equal(manifest.nextReleaseSourceStage, undefined);
});
