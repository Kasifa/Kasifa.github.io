import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { dirname, resolve, sep } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificate = resolve(root, "research/certificates/r072o");
const figure = resolve(
  root,
  "figures/r072o-physical-reinsertion/fig-r072o-physical-reinsertion",
);
const execFileAsync = promisify(execFile);

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function verifyFlatHashLedger(directory) {
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trimEnd()
    .split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
    const [, expected, name] = match;
    const target = resolve(directory, name);
    assert.ok(target.startsWith(directory + sep), `ledger path escapes: ${name}`);
    assert.equal(
      createHash("sha256").update(await readFile(target)).digest("hex"),
      expected,
      name,
    );
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort(), "hash rows are not unique and sorted");
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()), "symlink in package");
  const expectedNames = entries
    .filter(
      (entry) =>
        entry.isFile() && !["SHA256SUMS", ".DS_Store"].includes(entry.name),
    )
    .map((entry) => entry.name)
    .sort();
  assert.deepEqual(names, expectedNames, "hash ledger does not cover exact package files");
  return names;
}

test("R0.72O report states the proved and conditional gates exactly", async () => {
  const report = await text("research/r072o_report-source.md");
  for (const token of [
    "\\varepsilon^{11/6}",
    "\\varepsilon^{1/2}",
    "R^{2/3}L_{R,\\varepsilon}",
    "R^{4/3}L_{R,\\varepsilon}^{\\,2}",
    "full-superposition integrated ED",
    "C_{\\rm ED}\\ge1",
    "c_{\\rm ED}>0",
    "\\varepsilon_*",
    "L^2\\) contraction",
    "U_R'(0)=0",
    "U_R'''(0)=R(2R+1)\\ne0",
    "The Clay Millennium problem remains open",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /Equations \(0\.13\)--\(0\.16\) are conditional/);
  assert.match(report, /This is a theorem-applicability obstruction, not a counterexample/);
  assert.doesNotMatch(report, /general 3D (?:regularity|continuation).*CLOSED/i);
});

test("producer and independent sources remain implementation-independent", async () => {
  const [producer, independent] = await Promise.all([
    text("research/r072o_exact_audit.py"),
    text("research/r072o_independent_audit.mjs"),
  ]);
  assert.match(producer, /from fractions import Fraction/);
  assert.match(independent, /function rational\(/);
  assert.doesNotMatch(independent, /r072o_exact_audit|producer-(?:result|exponents|window)/);
  assert.doesNotMatch(producer, /r072o_independent_audit|independent-(?:result|exponents|window)/);
  assert.doesNotMatch(producer, /"generalPResultMarkedConditional": True/);
  assert.doesNotMatch(producer, /"multiCarrierCrossTermScaleRetainsN2": True/);
  assert.doesNotMatch(independent, /generalPResultMarkedConditional:\s*true/);
  assert.doesNotMatch(independent, /multiCarrierCrossTermScaleRetainsN2:\s*true/);
});

test("dual exact ledgers and deterministic screens pass the crosscheck", async () => {
  const [producer, independent, crosscheck, pExp, iExp] = await Promise.all([
    json("research/certificates/r072o/producer-result.json"),
    json("research/certificates/r072o/independent-result.json"),
    json("research/certificates/r072o/crosscheck.json"),
    json("research/certificates/r072o/producer-exponents.json"),
    json("research/certificates/r072o/independent-exponents.json"),
  ]);
  assert.equal(producer.status, "passed");
  assert.equal(independent.status, "passed");
  assert.equal(crosscheck.status, "passed");
  assert.deepEqual(pExp, iExp);
  assert.equal(pExp.actual.UEDOneCarrier.epsilon, "11/6");
  assert.deepEqual(pExp.actual.UED, { epsilon: "11/6", p: "4/3" });
  assert.deepEqual(pExp.actual.FullSuperpositionCrossCubic, {
    N: "2/1",
    a: "2/1",
    epsilon: "1/2",
  });
  assert.equal(pExp.claimContract.multiCarrierStatus, "conditional");
  assert.equal(
    pExp.claimContract.requiredHypothesis,
    "uniform full-superposition integrated ED",
  );
  assert.deepEqual(pExp.actual.UEDOverZ, {
    L: "-1/1",
    R: "-2/3",
    epsilon: "1/2",
    p: "-2/3",
  });
  assert.equal(crosscheck.checks.generalPConclusionRemainsConditional, true);
  assert.equal(crosscheck.checks.degeneracyTablesIdentical, true);
  for (const value of Object.values(crosscheck.maximumRelativeDifferences)) {
    assert.ok(Number.isFinite(value) && value <= 2e-12, value);
  }
});

test("certificate bundle has a complete, valid exact-byte hash ledger", async () => {
  const ledger = await readFile(resolve(certificate, "SHA256SUMS"), "utf8");
  const lines = ledger.trimEnd().split("\n");
  const files = (await readdir(certificate))
    .filter((name) => !["SHA256SUMS", ".DS_Store"].includes(name))
    .sort((left, right) => Buffer.from(left).compare(Buffer.from(right)));
  assert.equal(lines.length, files.length);
  assert.deepEqual(lines.map((line) => line.slice(66)), files);
  for (const line of lines) {
    assert.match(line, /^[0-9a-f]{64}  \S+$/);
    const name = line.slice(66);
    const bytes = await readFile(resolve(certificate, name));
    assert.equal(createHash("sha256").update(bytes).digest("hex"), line.slice(0, 64));
  }
});

test("formal figure seal passes the strict validator and public masters are byte-identical", async () => {
  const manifest = JSON.parse(
    await readFile(resolve(figure, "manifest.json"), "utf8"),
  );
  assert.equal(manifest.figureId, "fig-r072o-physical-reinsertion");
  assert.equal(manifest.release, "R0.72O");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.visualInspectionExplicit, true);
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.match(manifest.git.sourceCommit, /^[0-9a-f]{40}$/);
  assert.match(manifest.git.certificateCommit, /^[0-9a-f]{40}$/);

  const validator = resolve(root, "research/validate_figure_package.py");
  const { stdout } = await execFileAsync(
    process.env.CODEX_PYTHON || "python3",
    [validator, figure],
    { cwd: root },
  );
  assert.deepEqual(JSON.parse(stdout).errors, []);

  const names = await verifyFlatHashLedger(figure);
  for (const required of [
    "manifest.json",
    "validation.json",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
  ]) {
    assert.ok(names.includes(required), required);
  }

  for (const suffix of ["pdf", "svg", "png"]) {
    const master = await readFile(resolve(figure, `figure.${suffix}`));
    const publicPath = resolve(
      root,
      `public/assets/r072o/fig-r072o-physical-reinsertion.${suffix}`,
    );
    const published = await readFile(publicPath);
    assert.equal(Buffer.compare(master, published), 0, `${suffix} public byte identity`);
    const hash = createHash("sha256").update(master).digest("hex");
    assert.equal(
      manifest.figure.outputs.find((row) => row.path === `figure.${suffix}`)?.sha256,
      hash,
      `${suffix} archival manifest hash`,
    );
    assert.equal(
      manifest.publication.assets.find((row) => row.path.endsWith(`.${suffix}`))?.sha256,
      hash,
      `${suffix} public manifest hash`,
    );
  }
});
