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
const certificate = "research/certificates/r072v";
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


test("R0.72V certificate source freezes the exact unit-chart ledger", async () => {
  const [producer, independent, validator, readme] = await Promise.all([
    text(`${certificate}/generate_certificate.py`),
    text(`${certificate}/independent_recompute.py`),
    text(`${certificate}/validate_certificate.py`),
    text(`${certificate}/README.md`),
  ]);
  for (const token of [
    "q0(y)=(315/128)*(1-4*y^2)^4*1_{[-1/2,1/2]}(y)",
    '"mu2": mu2 == Fraction(1, 44)',
    '"mu4": mu4 == Fraction(3, 2288)',
    '"variance": variance == Fraction(5, 6292)',
    '"kappa0": kappa0 == Fraction(5, 6292)',
    '"unitBlockEllBound": ell_bound == Fraction(315, 2288)',
    '"unitBlockEscapingThreshold": escaping_threshold == Fraction(693, 2)',
    '"squaredEnergyRatio": "C2/(T+C2)"',
    '"timeLengthUniformity": False',
  ]) assert.ok(producer.includes(token), token);
  assert.ok(independent.includes("m_(2n+2)/m_(2n)=(2*n+1)/(2*n+11)"));
  assert.ok(independent.includes("scaled beta-integral recurrence"));
  assert.ok(independent.includes("comb(3, y_power)"));
  assert.ok(validator.includes('escaping.get("unitBlockSufficientThreshold") != "693/2"'));
  assert.ok(validator.includes('energy.get("squaredEnergyRatio") != "C2/(T+C2)"'));
  assert.match(readme, /source stage/i);
  assert.match(readme, /does \*\*not\*\* machine-check the[\s\S]*compactness/i);
  assert.match(readme, /periodic transfer[\s\S]*Navier--Stokes[\s\S]*Clay/i);
  assert.match(readme, /Time-length uniformity is false/i);
});


test("R0.72V claim boundary separates analytic proof from finite machine checks", async () => {
  const [producer, validator] = await Promise.all([
    text(`${certificate}/generate_certificate.py`),
    text(`${certificate}/validate_certificate.py`),
  ]);
  for (const token of [
    '"analyticWholeLineTheoremProvedInBoundReport": True',
    '"analyticAllL2DataEnergyEvolutionProvedInBoundReport": True',
    '"wholeLineFunctionalTheoremMachineChecked": False',
    '"compactnessArgumentMachineChecked": False',
    '"scalarEndpointTracePassageMachineChecked": False',
    '"hMinusOneDirectSumMachineChecked": False',
    '"nonautonomousEvolutionExistenceMachineChecked": False',
    '"periodicTransferProved": False',
    '"nonlinearNavierStokesClosureProved": False',
    '"clayMillenniumProblemSolved": False',
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    '"analyticWholeLineTheoremProvedInBoundReport"',
    '"analyticAllL2DataEnergyEvolutionProvedInBoundReport"',
    '"wholeLineFunctionalTheoremMachineChecked"',
    '"hMinusOneDirectSumMachineChecked"',
    '"nonautonomousEvolutionExistenceMachineChecked"',
  ]) assert.ok(validator.includes(token), token);
});


test("R0.72V formal certificate binds every report, certificate, figure, and source test byte", async () => {
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
    "research/r072v_report-source.md",
    "research/r072v_gap_matrix.md",
    "research/r072v_literature_audit.md",
    "research/r072v_independent_audit.md",
    "scripts/generate_r072v_figure.py",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/README.md",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/caption.md",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/figure-contract.md",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/contract.json",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/config.json",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/command.txt",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/environment.txt",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/requirements.txt",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/qa-protocol.md",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/plot.py",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/validate.py",
    "tests/r072v-deterministic-certificate-source.test.mjs",
    "tests/r072v-unit-chart-globalization-figure-source.test.mjs",
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


test("R0.72V source stage exposes only non-mutating self-tests", async () => {
  const formal = await certificateIsFormal();
  if (!formal) await assertNoCertificateOutputs();
  const before = formal ? await generatedSnapshot() : null;

  await assert.rejects(run(python, [
    `${certificate}/independent_recompute.py`,
  ], { cwd: root }));
  await assert.rejects(run(python, [
    `${certificate}/generate_certificate.py`,
  ], { cwd: root }));

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


test("R0.72V strict validator is fail-closed at source and exhaustive when formal", async () => {
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
