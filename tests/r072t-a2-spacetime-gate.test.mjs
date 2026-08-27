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
  release: "r072t", stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r072t_report-source.md",
  literatureAudit: "research/r072t_literature_audit.md",
  gapMatrix: "research/r072t_gap_matrix.md",
  independentAudit: "research/r072t_independent_audit.md",
  producer: "research/certificates/r072t/generate_certificate.py",
  independentProducer: "research/certificates/r072t/independent_recompute.py",
  comparator: "research/certificates/r072t/validate_certificate.py",
  certificateDirectory: "research/certificates/r072t",
  figureDirectory: "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model",
  generator: "scripts/generate_r072t_release.py",
  translationScript: "scripts/add-r072t-translations.mjs",
  releaseGate: "tests/r072t-a2-spacetime-gate.test.mjs",
  publicationTest: "tests/r072t-release.test.mjs",
};

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
    entries.filter((entry) => entry.isFile() && !["SHA256SUMS", ".DS_Store"].includes(entry.name))
      .map((entry) => entry.name).sort(),
  );
}

test("R0.72T source freezes the exact A2 germ and unique four-term scaling", async () => {
  const [report, gap, audit] = await Promise.all([
    text("research/r072t_report-source.md"),
    text("research/r072t_gap_matrix.md"),
    text("research/r072t_independent_audit.md"),
  ]);
  for (const token of [
    "W_d=W_{xx}", "-\\frac14H_3", "+\\frac1{16}H_5",
    "-\\frac1{160}H_7", "\\kappa=\\frac{\\varepsilon_c}{4}",
    "X=\\kappa^{1/5}x", "S=\\kappa^{2/5}d", "X^3+6SX",
  ]) assert.ok(report.includes(token), token);
  assert.match(report, /b=2a=1-3a=1-a-b/);
  assert.ok(report.includes("a=\\frac15,\\qquad b=\\frac25"));
  assert.match(report, /R_9|parabolic\s+weight\s+nine/i);
  assert.match(gap, /derivative|primitive/i);
  assert.match(audit, /quadratic expression is\s+the derivative germ/i);
});

test("R0.72T proves only the audited mixing and calibration statements", async () => {
  const [report, literature, audit] = await Promise.all([
    text("research/r072t_report-source.md"),
    text("research/r072t_literature_audit.md"),
    text("research/r072t_independent_audit.md"),
  ]);
  assert.match(report, /H\^\{-1\}.*T\^\{-1\/3\}/s);
  assert.ok(report.includes("q=\\frac{2}{2+p}"));
  assert.ok(report.includes("q=6/7"));
  assert.ok(report.includes("\\frac{a^2T^5}{720}"));
  assert.ok(report.includes("T\\asymp |kA|^{-2/5}\\nu^{-3/5}"));
  assert.match(report, /V\(S,X\)=aSX\+bX\^3/);
  assert.match(report, /An evolving\s+solution changes with/);
  assert.ok(report.includes("\\|\\chi u\\|_{L^2_SL^2_X}"));
  assert.ok(report.includes("L^2_SH^{-1}_X"));
  assert.match(literature, /10\.1007\/s00020-016-2303-4/);
  assert.match(audit, /1\+1\+1\+2=5/);
  assert.ok(audit.includes("for one fixed \\(f\\)"));
  assert.match(literature, /10\.1002\/cpa\.21831/);
  assert.match(literature, /compact Hilbert-scale setup.*does not directly/s);
  for (const source of [report, literature, audit]) {
    for (const token of ["blockContraction=OPEN", "periodicTransfer=OPEN", "Clay=OPEN"]) {
      assert.ok(source.includes(token), token);
    }
  }
});

test("R0.72T certificate and formal figure remain fail-closed", async () => {
  const certificate = "research/certificates/r072t";
  const figure = "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model";
  await verifyFlatHashLedger(certificate);
  await verifyFlatHashLedger(figure);
  const [crosscheck, certificateManifest, manifest] = await Promise.all([
    json(`${certificate}/crosscheck.json`),
    json(`${certificate}/manifest.json`),
    json(`${figure}/manifest.json`),
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
    "research/certificates/r072t/validate_certificate.py", "--require-formal",
  ], { cwd: root });
  assert.equal(manifest.release, "R0.72T");
  assert.equal(manifest.figureId, "fig-r072t-a2-spacetime-model");
  assert.equal(manifest.status, "formal");
  const png = manifest.figure.outputs.find((output) => output.path === "figure.png");
  assert.equal(png?.dpi, 600);
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.visualInspectionExplicit, true);
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.equal(manifest.publication.directory, "public/assets/r072t");
});

test("R0.72T manifest is source-staged or atomically public", async () => {
  const manifest = await json("research/release-manifest.json");
  assert.ok(["r072s", "r072t"].includes(manifest.latestCompletedRelease));
  if (manifest.latestCompletedRelease === "r072s") {
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
    assert.deepEqual({ version: manifest.siteVersion, notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount, next: manifest.nextRelease,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount },
    { version: "1.32", notes: 169, recap: 109, next: "r072t",
      published: 71, sealed: 47, backlog: 24 });
    const [site, notes, home, recap] = await Promise.all([
      json("public/site-version.json"), readdir(resolve(root, "public/notes")),
      text("public/research-review.html"), text("public/recap-r0-61-r0-72s.html"),
    ]);
    assert.equal(site.version, "1.32");
    assert.equal(site.latestRelease, "R0.72S");
    assert.equal(site.publicHtmlNoteCount, 169);
    assert.equal(notes.filter((name) => name.endsWith(".html")).length, 169);
    assert.match(home, /<strong>169<\/strong>公开研究笔记/);
    assert.match(home, /<strong>R0\.72S<\/strong>最新研究节点/);
    assert.doesNotMatch(home, /data-release="r072t"/);
    const start = recap.indexOf('<section id="node-index">');
    const end = recap.indexOf("</section>", start);
    assert.ok(start >= 0 && end > start);
    const links = [...recap.slice(start, end).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
      .map((match) => match[1]);
    assert.equal(links.length, 109);
    assert.equal(new Set(links).size, 109);
    for (const relative of ["public/notes/r0-72t.html", "public/notes/r0-72t.pdf",
      "public/recap-r0-61-r0-72t.html", "public/recap-r0-61-r0-72t.pdf"]) await absent(relative);
    return;
  }
  assert.deepEqual(
    {
      latest: manifest.latestCompletedRelease,
      siteVersion: manifest.siteVersion,
      notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount,
      next: manifest.nextRelease,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    },
    {
      latest: "r072t", siteVersion: "1.33", notes: 170, recap: 110,
      next: "r072u", published: 72, sealed: 48, backlog: 24,
    },
  );
  assert.equal(manifest.nextReleaseSourceStage, undefined);
});
