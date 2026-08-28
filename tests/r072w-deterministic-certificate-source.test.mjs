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
const certificate = "research/certificates/r072w";
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
  return (await maybeJson(certificate + "/manifest.json"))?.status === "formal";
}


async function generatedSnapshot() {
  return Object.fromEntries(await Promise.all(generated.map(async (name) => [
    name,
    await sha(certificate + "/" + name),
  ])));
}


async function assertNoCertificateOutputs() {
  for (const name of generated) await absent(certificate + "/" + name);
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
    assert.equal(await sha(relative + "/" + name), expected, name);
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


test("R0.72W source freezes the exact H9, probe, finite-type, no-go, and energy ledgers", async () => {
  const [producer, independent, validator, readme] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/independent_recompute.py"),
    text(certificate + "/validate_certificate.py"),
    text(certificate + "/README.md"),
  ]);
  for (const token of [
    "W=-H3/4+H5/16-H7/160+17*H9/48384+R11",
    "V_alpha=H3-alpha^2*H5/4+alpha^4*H7/40-17*alpha^6*H9/12096+R_alpha,11",
    '"exactPotentialHeatIdentity": "V_S=V_XX"',
    '"chartCoefficientTimeIdentities": "b_S=V_XXX and a_S=V_XXXX/2 for b=V_X and a=V_XX/2"',
    '"derivativeScaling": "V_XXX=O_T(1), V_XXXX=O_T(alpha)"',
    '"mu2": "ell^2/44"',
    '"mu4": "3*ell^4/2288"',
    '"varianceY2": "5*ell^4/6292"',
    '"finiteTypeMatrix": [[1, -1], [-1, 4]]',
    '"finiteTypeDeterminant": determinant',
    '"cosineSquareMinimum": q(minimum)',
    '"absorbableGrowingRadius": "R=o(kappa^(2/25))"',
    '"squaredEnergyRatio": "C2/(T+C2)"',
  ]) assert.ok(producer.includes(token), token);
  assert.ok(independent.includes("H_{n+1}=x H_n+2*n*t H_{n-1}"));
  assert.ok(independent.includes("m_(2n+2)/m_(2n)=(2n+1)/(2n+11)"));
  assert.ok(validator.includes('"17/48384"'));
  assert.ok(validator.includes('"7/16"'));
  assert.match(readme, /source stage/i);
  assert.match(readme, /does \*\*not\*\* machine-check compactness/i);
});


test("R0.72W claim boundary is explicit and machine-honest", async () => {
  const [producer, validator] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/validate_certificate.py"),
  ]);
  for (const token of [
    '"analyticExactPeriodicUnitChartTheoremProvedInBoundReport": True',
    '"analyticTorusGraphTheoremProvedInBoundReport": True',
    '"analyticPeriodicScalarEnergyContractionProvedInBoundReport": True',
    '"exactPeriodicScalarTransferProved": True',
    '"heatSeriesBeyondH9MachineChecked": False',
    '"compactnessArgumentMachineChecked": False',
    '"scalarEndpointTracePassageMachineChecked": False',
    '"varyingCellGraphSpacePassageMachineChecked": False',
    '"torusHMinusOneDirectSumMachineChecked": False',
    '"nonautonomousEvolutionExistenceMachineChecked": False',
    '"timeLengthUniformity": False',
    '"nonlinearNavierStokesClosureProved": False',
    '"clayMillenniumProblemSolved": False',
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "validate_claim_boundary",
    '"analyticTorusGraphTheoremProvedInBoundReport"',
    '"torusHMinusOneDirectSumMachineChecked"',
    '"nonlinearNavierStokesClosureProved"',
    '"clayMillenniumProblemSolved"',
  ]) assert.ok(validator.includes(token), token);
});


test("R0.72W formal lifecycle binds the complete frozen source set", async () => {
  const [producer, validator] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/validate_certificate.py"),
  ]);
  for (const token of [
    "SOURCE_FILES",
    "gitBlob",
    "workingTreeBlobMatches",
    "--source-commit",
    "source commit must equal clean HEAD",
    "refusing to overwrite existing certificate outputs",
    "research/r072w_report-source.md",
    "research/r072w_gap_matrix.md",
    "research/r072w_literature_audit.md",
    "research/r072w_independent_audit.md",
    "research/release-manifest.json",
    "scripts/generate_r072w_figure.py",
    "scripts/generate_r072w_release.py",
    "scripts/add-r072w-translations.mjs",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/README.md",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/caption.md",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/contract.json",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/config.json",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/command.txt",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/environment.txt",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/requirements.txt",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/qa-protocol.md",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/plot.py",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/validate.py",
    "tests/r072w-deterministic-certificate-source.test.mjs",
    "tests/r072w-exact-periodic-gate.test.mjs",
    "tests/r072w-exact-tail-transfer-figure-source.test.mjs",
    "tests/r072w-release.test.mjs",
  ]) assert.ok(producer.includes(token), token);
  assert.ok(!producer.includes("figure-contract.md"));
  for (const token of [
    "EXPECTED_SOURCE_FILES",
    "complete frozen source set",
    "formal source binding drift",
    "SHA256SUMS must cover every flat regular file exactly once",
  ]) assert.ok(validator.includes(token), token);
});


test("R0.72W source stage exposes only non-mutating self-tests", async () => {
  const formal = await certificateIsFormal();
  if (!formal) await assertNoCertificateOutputs();
  const before = formal ? await generatedSnapshot() : null;
  await assert.rejects(run(python, [
    certificate + "/independent_recompute.py",
  ], { cwd: root }));
  await assert.rejects(run(python, [
    certificate + "/generate_certificate.py",
  ], { cwd: root }));
  const independentRun = await run(python, [
    certificate + "/independent_recompute.py", "--self-test",
  ], { cwd: root });
  assert.match(independentRun.stdout, /passed \(no outputs written\)/);
  const producerRun = await run(python, [
    certificate + "/generate_certificate.py", "--self-test",
  ], { cwd: root });
  assert.match(producerRun.stdout, /passed \(no outputs written\)/);
  if (formal) assert.deepEqual(await generatedSnapshot(), before);
  else await assertNoCertificateOutputs();
});


test("R0.72W strict validator fails closed at source and is exhaustive when formal", async () => {
  if (!(await certificateIsFormal())) {
    await assertNoCertificateOutputs();
    await assert.rejects(run(python, [
      certificate + "/validate_certificate.py", "--require-formal",
    ], { cwd: root }));
    await assertNoCertificateOutputs();
    return;
  }
  const [manifest, crosscheck] = await Promise.all([
    maybeJson(certificate + "/manifest.json"),
    maybeJson(certificate + "/crosscheck.json"),
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
    certificate + "/validate_certificate.py", "--require-formal",
  ], { cwd: root });
});
