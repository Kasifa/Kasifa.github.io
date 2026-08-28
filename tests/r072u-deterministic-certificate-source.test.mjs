import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const python = process.env.CODEX_PYTHON || "python3";
const run = promisify(execFile);
const certificate = "research/certificates/r072u";
const generated = [
  "certificate.json",
  "independent.json",
  "crosscheck.json",
  "manifest.json",
  "SHA256SUMS",
];


async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}


async function absent(relative) {
  await assert.rejects(
    access(resolve(root, relative)),
    (error) => error?.code === "ENOENT",
    relative,
  );
}


async function maybeJson(relative) {
  try {
    return JSON.parse(await text(relative));
  } catch (error) {
    if (error?.code === "ENOENT") return null;
    throw error;
  }
}


async function sha(relative) {
  return createHash("sha256").update(await readFile(resolve(root, relative))).digest("hex");
}


async function certificateIsFormal() {
  return (await maybeJson(`${certificate}/manifest.json`))?.status === "formal";
}


async function generatedSnapshot() {
  return Object.fromEntries(await Promise.all(generated.map(async (name) => [
    name,
    await sha(`${certificate}/${name}`),
  ])));
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
    assert.equal(await sha(`${relative}/${name}`), expected, name);
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries.filter((entry) => entry.isFile() && entry.name !== "SHA256SUMS")
      .map((entry) => entry.name).sort(),
  );
}


async function assertNoCertificateOutputs() {
  for (const name of generated) await absent(`${certificate}/${name}`);
}


test("R0.72U certificate source freezes the exact rational ledger", async () => {
  const [producer, independent, validator, readme] = await Promise.all([
    text(`${certificate}/generate_certificate.py`),
    text(`${certificate}/independent_recompute.py`),
    text(`${certificate}/validate_certificate.py`),
    text(`${certificate}/README.md`),
  ]);
  for (const token of [
    "rho(X)=(315/256)*(1-X^2)^4*1_{[-1,1]}(X)",
    '"mu2": mu2 == Fraction(1, 11)',
    '"mu4": mu4 == Fraction(3, 143)',
    '"unitBlockThreshold": threshold == Fraction(27, 13)',
    '"fixedGaugeFloor": fixed_gauge_floor == Fraction(4, 5)',
    '"wholeLineBlockContractionProved": False',
  ]) assert.ok(producer.includes(token), token);
  assert.ok(independent.includes("mu_(2n+2)/mu_(2n)=(2*n+1)/(2*n+11)"));
  assert.ok(independent.includes("beta-integral recurrence"));
  assert.ok(validator.includes('large.get("thresholdFloor") != "81/143"'));
  assert.ok(validator.includes('large.get("positiveThresholdMinimum") != "87/143"'));
  assert.match(readme, /source stage/i);
  assert.match(readme, /whole-line block\s+contraction/i);
});


test("R0.72U formal certificate has complete commit and byte source binding", async () => {
  const [producer, validator] = await Promise.all([
    text(`${certificate}/generate_certificate.py`),
    text(`${certificate}/validate_certificate.py`),
  ]);
  for (const token of [
    "SOURCE_FILES",
    "gitBlob",
    "workingTreeBlobMatches",
    "--source-commit",
    "source commit must equal clean HEAD",
    "refusing to overwrite existing certificate outputs",
    "tests/r072u-deterministic-certificate-source.test.mjs",
    "tests/r072u-two-moment-figure-source.test.mjs",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/validate.py",
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "validate_source_bindings",
    "EXPECTED_SOURCE_FILES",
    "complete frozen source set",
    "formal source binding drift",
    "gitBlob",
    "sha256",
    "bytes",
    "SHA256SUMS must cover every flat regular file exactly once",
  ]) assert.ok(validator.includes(token), token);
});


test("R0.72U self-tests are exact and never mutate the certificate stage", async () => {
  const formal = await certificateIsFormal();
  if (!formal) await assertNoCertificateOutputs();
  const before = formal ? await generatedSnapshot() : null;
  const independentRun = await run(python, [
    `${certificate}/independent_recompute.py`, "--self-test",
  ], { cwd: root });
  assert.match(independentRun.stdout, /passed \(no outputs written\)/);
  const producerRun = await run(python, [
    `${certificate}/generate_certificate.py`, "--self-test",
  ], { cwd: root });
  assert.match(producerRun.stdout, /passed \(no outputs written\)/);
  if (formal) assert.deepEqual(await generatedSnapshot(), before);
  else await assertNoCertificateOutputs();
});


test("R0.72U strict validator is fail-closed at source and exhaustive when formal", async () => {
  if (!(await certificateIsFormal())) {
    await assertNoCertificateOutputs();
    await assert.rejects(run(python, [
      `${certificate}/validate_certificate.py`, "--require-formal",
    ], { cwd: root }));
    await assertNoCertificateOutputs();
    return;
  }
  const [manifest, crosscheck] = await Promise.all([
    maybeJson(`${certificate}/manifest.json`),
    maybeJson(`${certificate}/crosscheck.json`),
  ]);
  assert.equal(manifest.status, "formal");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.ok(Array.isArray(manifest.sourceBindings) && manifest.sourceBindings.length > 0);
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
  assert.equal(crosscheck.sourceCommit, manifest.sourceCommit);
  assert.deepEqual(crosscheck.sourceBindings, manifest.sourceBindings);
  await verifyFlatHashLedger(certificate);
  await run(python, [
    `${certificate}/validate_certificate.py`, "--require-formal",
  ], { cwd: root });
});
