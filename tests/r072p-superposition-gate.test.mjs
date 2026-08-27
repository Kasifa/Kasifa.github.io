import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { dirname, resolve, sep } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificate = resolve(root, "research/certificates/r072p");
const figure = resolve(
  root,
  "figures/r072p-superposition-gate/fig-r072p-superposition-gate",
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
  assert.deepEqual(names, [...new Set(names)].sort(), "hash rows must be unique and sorted");
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()), "symlink in package");
  const expectedNames = entries
    .filter((entry) => entry.isFile() && !["SHA256SUMS", ".DS_Store"].includes(entry.name))
    .map((entry) => entry.name)
    .sort();
  assert.deepEqual(names, expectedNames, "hash ledger must cover exact package files");
  return names;
}

test("R0.72P report states the fixed 1:2 theorem and open boundaries exactly", async () => {
  const report = await text("research/r072p_report-source.md");
  for (const token of [
    "r_1=R",
    "r_2=2R",
    "B=2",
    "N=2",
    "p=2^{-1/2}",
    "0<\\lambda_-\\le |\\lambda|\\le\\lambda_+:=\\frac18",
    "W_\\lambda(y,\\phi)",
    "k=1",
    "kV=sW_\\lambda",
    "\\alpha(y)=\\lambda e^{-3y}",
    "1+4\\alpha(y)\\cos\\phi",
    "C_{\\rm ED}",
    "c_{\\rm ED}",
    "E(1)\\le C_{\\rm ED}e^{-c_{\\rm ED}\\sqrt\\varepsilon}E(0)",
    "\\mathcal C_\\times\\lesssim a^2N^2\\sqrt\\varepsilon",
    "\\varepsilon^{11/6}p^{4/3}",
    "|\\lambda|=1/4",
    "The Clay Millennium problem remains open",
  ]) assert.ok(report.includes(token), token);
  assert.match(report, /constants independent of[\s\S]*R,\\varepsilon,\\lambda/);
  assert.match(report, /does not cover arbitrary phases, arbitrary carrier/);
  assert.match(report, /theorem-applicability wall[\s\S]*does not prove failure of enhanced dissipation/);
  assert.doesNotMatch(report, /k=s[\s\S]{0,120}U=V=sW/);
  assert.doesNotMatch(report, /(?:arbitrary common-band|general 3D).*CLOSED/i);
});

test("producer and independent implementations remain independent", async () => {
  const [producer, independent] = await Promise.all([
    text("research/r072p_exact_audit.py"),
    text("research/r072p_independent_audit.mjs"),
  ]);
  assert.match(producer, /from fractions import Fraction/);
  assert.match(independent, /function rational\(/);
  assert.doesNotMatch(independent, /r072p_exact_audit|producer-(?:result|exponents|shape|wall)/);
  assert.doesNotMatch(producer, /r072p_independent_audit|independent-(?:result|exponents|shape|wall)/);
});

test("dual exact ledgers certify the fixed-pattern gate and applicability-only wall", async () => {
  const [producer, independent, crosscheck, pExact, iExact] = await Promise.all([
    json("research/certificates/r072p/producer-result.json"),
    json("research/certificates/r072p/independent-result.json"),
    json("research/certificates/r072p/crosscheck.json"),
    json("research/certificates/r072p/producer-exponents.json"),
    json("research/certificates/r072p/independent-exponents.json"),
  ]);
  assert.equal(producer.status, "passed");
  assert.equal(independent.status, "passed");
  assert.equal(crosscheck.status, "passed");
  assert.deepEqual(pExact, iExact);
  const contract = pExact.exponentLedger.claimContract;
  assert.equal(contract.status, "proved-for-declared-real-collinear-phase-1:2-class");
  assert.equal(contract.arbitraryCommonBandStatus, "open");
  assert.equal(contract.growingCarrierCountStatus, "open");
  assert.equal(contract.integratedEstimate.status, "proved-analytically-for-declared-class");
  assert.equal(contract.terminalEstimate.status, "proved-analytically-for-declared-class");
  assert.deepEqual(pExact.exponentLedger.parameters, {
    B: "2/1",
    N: "2/1",
    pSquared: "1/2",
  });
  assert.equal(pExact.morseWall.absLambda, "1/4");
  assert.equal(pExact.morseWall.status, "Morse-applicability-wall-only");
  for (const key of [
    "exactLedgersIdentical",
    "shapeTablesIdentical",
    "wallTablesIdentical",
    "cellFactorExact",
    "shapeAndSlowBoundsExact",
    "integralAndTerminalContractPresent",
    "claimScopePreserved",
    "n2PSquaredLedgerExact",
    "morseWallIsApplicabilityOnly",
  ]) assert.equal(crosscheck.checks[key], true, key);
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
  assert.equal(crosscheck.checks.formalSourceReady, true);
});

test("certificate bundle has a complete exact-byte hash ledger", async () => {
  const names = await verifyFlatHashLedger(certificate);
  for (const required of [
    "README.md",
    "crosscheck.json",
    "producer-result.json",
    "independent-result.json",
    "producer-exponents.json",
    "independent-exponents.json",
    "producer-shape.csv",
    "independent-shape.csv",
    "producer-wall.csv",
    "independent-wall.csv",
  ]) assert.ok(names.includes(required), required);
});

test("formal P figure passes strict validation and public masters are byte-identical", async () => {
  const manifest = JSON.parse(await readFile(resolve(figure, "manifest.json"), "utf8"));
  assert.equal(manifest.figureId, "fig-r072p-superposition-gate");
  assert.equal(manifest.release, "R0.72P");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.visualInspectionExplicit, true);
  assert.equal(manifest.publication.directory, "public/assets/r072p");
  assert.equal(manifest.publication.stem, "fig-r072p-superposition-gate");
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.match(manifest.git.sourceCommit, /^[0-9a-f]{40}$/);
  assert.match(manifest.git.certificateCommit, /^[0-9a-f]{40}$/);
  assert.equal(
    manifest.git.certificateBlobBindings.some(
      (row) => row.role === "flatCertificateLedger" && row.path.endsWith("/SHA256SUMS"),
    ),
    true,
  );
  assert.equal(
    manifest.sourceData.some(
      (row) => row.role === "certificateLedger" && row.fileName.endsWith("/SHA256SUMS"),
    ),
    true,
  );
  assert.equal(manifest.dataSummary.certificateLedgerAudit.exactDirectoryCoverage, true);

  const validator = resolve(root, "research/validate_figure_package.py");
  const { stdout } = await execFileAsync(
    process.env.CODEX_PYTHON || "python3",
    [validator, figure],
    { cwd: root },
  );
  assert.deepEqual(JSON.parse(stdout).errors, []);
  const names = await verifyFlatHashLedger(figure);
  for (const required of [
    "manifest.json", "validation.json", "figure.pdf", "figure.svg", "figure.png",
    "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "certificate_ledger.py",
  ]) assert.ok(names.includes(required), required);

  for (const suffix of ["pdf", "svg", "png"]) {
    const master = await readFile(resolve(figure, `figure.${suffix}`));
    const publicPath = resolve(root, `public/assets/r072p/fig-r072p-superposition-gate.${suffix}`);
    const published = await readFile(publicPath);
    assert.equal(Buffer.compare(master, published), 0, `${suffix} public byte identity`);
    const hash = createHash("sha256").update(master).digest("hex");
    assert.equal(manifest.figure.outputs.find((row) => row.path === `figure.${suffix}`)?.sha256, hash);
    assert.equal(manifest.publication.assets.find((row) => row.path.endsWith(`.${suffix}`))?.sha256, hash);
  }
});
