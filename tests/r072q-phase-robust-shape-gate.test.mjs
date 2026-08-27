import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import {
  copyFile,
  mkdtemp,
  readFile,
  readdir,
  rm,
  writeFile,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const python = process.env.CODEX_PYTHON || "python3";
const node = process.env.CODEX_NODE || process.execPath;
const execFileAsync = promisify(execFile);

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function run(executable, arguments_, options = {}) {
  return execFileAsync(executable, arguments_, {
    cwd: root,
    maxBuffer: 8 * 1024 * 1024,
    ...options,
  });
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
    assert.equal(
      createHash("sha256").update(await readFile(resolve(directory, name))).digest("hex"),
      expected,
      name,
    );
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries
      .filter((entry) => entry.isFile() && !["SHA256SUMS", ".DS_Store"].includes(entry.name))
      .map((entry) => entry.name)
      .sort(),
  );
  return names;
}

test("R0.72Q report closes only the fixed-M arbitrary-phase jet-dominated class", async () => {
  const report = await text("research/r072q_report-source.md");
  for (const token of [
    "All relative phases are arbitrary",
    "Q_2:=\\sum_{m=2}^{M}m^2b_m\\le\\frac12",
    "N_{\\rm crit}=2",
    "r=\\frac\\pi{12}",
    "\\mathfrak C_0=81",
    "\\mathfrak C_1=36",
    "e^{-1}\\mu\\frac\\pi{12}>\\frac1{36}",
    "1+\\frac M2",
    "\\left(1+\\frac M2\\right)^{-4}",
    "=(\\partial_\\phi^2-|q_*|^2R^{-2})G",
    "e^{|q_*|^2R^{-2}\\eta t}",
    "|q_*|=1",
    "z(\\phi)=\\frac18e^{-3i\\phi}-\\frac38e^{-i\\phi}",
    "\\left[\\frac14,\\frac12\\right]",
    "R0.72R should leave the dominant-first-harmonic cone",
    "solution of the Clay",
  ]) assert.ok(report.includes(token), token);
  assert.ok(report.includes("Fix an integer \\(M\\ge2\\)"));
  assert.ok(
    report.includes(
      "The radius \\(1/4\\) is sharp for a disk that must work for every phase.",
    ),
  );
  assert.ok(
    report.includes(
      "arbitrary time-dependent phases; only the heat envelope varies in time",
    ),
  );
  assert.doesNotMatch(report, /(?:growing \(M\)|general three-dimensional).*CLOSED/i);
  assert.equal(
    report.includes("=(\\partial_\\phi^2-R^{-2})G"),
    false,
    "the affine-row damping must retain the general |q_*|^2 factor",
  );
});

test("physical and normalized shape constants remain explicitly separated", async () => {
  const [producer, independent, comparator] = await Promise.all([
    text("research/r072q_exact_audit.py"),
    text("research/r072q_independent_audit.mjs"),
    text("research/r072q_compare_audits.py"),
  ]);
  for (const source of [producer, independent, comparator]) {
    assert.match(source, /normalizedShapeConstants/);
    assert.match(source, /physicalWindowShapeConstants/);
    assert.match(source, /36\/1/);
    assert.match(source, /12\/1/);
  }
  assert.match(producer, /from fractions import Fraction/);
  assert.match(independent, /BigInt/);
  assert.doesNotMatch(
    independent,
    /r072q_exact_audit|producer-(?:config|payload|result|progress|resource|monitor)/,
  );
  assert.doesNotMatch(
    producer,
    /r072q_independent_audit|independent-(?:config|payload|result|progress|resource|monitor)/,
  );
});

test("independent temporary routes agree exactly and the formal ledger rejects their temporary seal", async (t) => {
  const directory = await mkdtemp(join(tmpdir(), "r072q-audit-"));
  t.after(() => rm(directory, { recursive: true, force: true }));

  await run(python, [
    "research/r072q_exact_audit.py",
    "--output-dir",
    directory,
    "--max-carrier",
    "23",
  ]);
  await run(node, [
    "research/r072q_independent_audit.mjs",
    "--output-dir",
    directory,
    "--max-carrier",
    "23",
  ]);
  await run(python, [
    "research/r072q_compare_audits.py",
    "--certificate-dir",
    directory,
    "--allow-unsealed-source",
  ]);

  const producerPayload = JSON.parse(
    await readFile(join(directory, "producer-payload.json"), "utf8"),
  );
  const independentPayload = JSON.parse(
    await readFile(join(directory, "independent-payload.json"), "utf8"),
  );
  const crosscheck = JSON.parse(
    await readFile(join(directory, "crosscheck.json"), "utf8"),
  );
  assert.deepEqual(producerPayload, independentPayload);
  assert.equal(producerPayload.shapeContract.maxCarrier, 23);
  assert.equal(producerPayload.shapeContract.criticalGeometry.C1, "36/1");
  assert.deepEqual(
    producerPayload.shapeContract.criticalGeometry.normalizedShapeConstants,
    { C0: "9/1", C1: "12/1", conservativeC0AlsoValid: "81/1" },
  );
  assert.deepEqual(
    producerPayload.shapeContract.criticalGeometry.physicalWindowShapeConstants,
    {
      C0: "81/1",
      C1: "36/1",
      awaySlopeLower: "1/36",
      localSlopeLower: "1/9",
      yWindow: "0<=y<=1",
    },
  );
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.checks.canonicalPayloadsIdentical, true);
  assert.equal(crosscheck.checks.arbitraryPhaseTwoCriticalContract, true);
  assert.equal(crosscheck.checks.causticParametrizationExact, true);
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, true);

  const scaffold = resolve(root, "research/certificates/r072q");
  for (const name of [
    "README.md",
    "command.txt",
    "write_environment.py",
    "build_hashes.py",
  ]) await copyFile(resolve(scaffold, name), join(directory, name));
  await run(python, [join(directory, "write_environment.py")], {
    env: { ...process.env, R072Q_NODE: node },
  });
  await assert.rejects(
    run(python, [join(directory, "build_hashes.py")]),
    /not fully passed|temporary R0\.72Q crosscheck/,
  );

  // Simulate a clean source-commit seal in the isolated fixture so the
  // positive flat-ledger path and the unexpected-file rejection are tested
  // without creating formal outputs in the repository.
  for (const route of ["producer", "independent"]) {
    const target = join(directory, `${route}-config.json`);
    const config = JSON.parse(await readFile(target, "utf8"));
    config.sourceTracked = true;
    config.trackedChangesDirty = false;
    await writeFile(target, `${JSON.stringify(config, null, 2)}\n`);
  }
  crosscheck.temporaryUnsealedSourceAllowed = false;
  for (const key of Object.keys(crosscheck.checks)) crosscheck.checks[key] = true;
  await writeFile(
    join(directory, "crosscheck.json"),
    `${JSON.stringify(crosscheck, null, 2)}\n`,
  );
  await run(python, [join(directory, "build_hashes.py")]);
  const rows = (await readFile(join(directory, "SHA256SUMS"), "utf8"))
    .trimEnd()
    .split("\n");
  assert.equal(rows.length, 18);
  assert.deepEqual(
    rows.map((row) => row.slice(66)),
    [...rows.map((row) => row.slice(66))].sort(),
  );

  await writeFile(join(directory, "unexpected.txt"), "must fail\n");
  await assert.rejects(
    run(python, [join(directory, "build_hashes.py")]),
    /unexpected certificate artifacts: unexpected\.txt/,
  );
});

test("formal command and source-stage package forbid a pre-publication seal", async () => {
  const [command, readme, builder, manifest] = await Promise.all([
    text("research/certificates/r072q/command.txt"),
    text("research/certificates/r072q/README.md"),
    text("research/certificates/r072q/build_hashes.py"),
    json("research/release-manifest.json"),
  ]);
  assert.doesNotMatch(command, /allow-unsealed-source/);
  assert.match(command, /--max-carrier 2/g);
  assert.ok(command.indexOf("r072q_compare_audits.py") < command.indexOf("write_environment.py"));
  assert.ok(command.indexOf("write_environment.py") < command.indexOf("build_hashes.py"));
  assert.match(readme, /finite instance is not a proof for every fixed `M`/);
  assert.match(builder, /temporary R0\.72Q crosscheck cannot be formally hashed/);
  assert.match(builder, /unexpected certificate artifacts/);
  const certificateNames = await readdir(resolve(root, "research/certificates/r072q"));
  if (manifest.latestCompletedRelease === "r072p") {
    assert.equal(manifest.nextRelease, "r072q");
    assert.equal(manifest.nextReleaseSourceStage.publicCountersAdvanced, false);
    assert.deepEqual(certificateNames.sort(), [
      "README.md",
      "build_hashes.py",
      "command.txt",
      "write_environment.py",
    ]);
    return;
  }
  assert.equal(manifest.latestCompletedRelease, "r072q");
  assert.equal(manifest.nextRelease, "r072r");
  assert.equal(manifest.nextReleaseSourceStage, undefined);
  const certificate = resolve(root, "research/certificates/r072q");
  const names = await verifyFlatHashLedger(certificate);
  assert.equal(names.length, 18);
  const crosscheck = JSON.parse(
    await readFile(resolve(certificate, "crosscheck.json"), "utf8"),
  );
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
  assert.ok(Object.values(crosscheck.checks).every((value) => value === true));
  for (const required of [
    "producer-config.json",
    "producer-payload.json",
    "producer-result.json",
    "independent-config.json",
    "independent-payload.json",
    "independent-result.json",
    "crosscheck.json",
  ]) assert.ok(names.includes(required), required);
});

test("Q figure remains a source-only scaffold until formal certificate and visual QA", async () => {
  const figure = resolve(
    root,
    "figures/r072q-phase-robust-shape/fig-r072q-phase-robust-shape",
  );
  const names = await readdir(figure);
  for (const required of [
    "README.md",
    "build_manifest.py",
    "caption.md",
    "certificate_ledger.py",
    "command.txt",
    "config.json",
    "contract.json",
    "figure-contract.md",
    "plot.py",
    "publish_assets.py",
    "qa_images.py",
    "requirements.txt",
    "validate.py",
  ]) assert.ok(names.includes(required), required);
  const manifest = await json("research/release-manifest.json");
  const formalFiles = [
    "manifest.json",
    "results.json",
    "validation.json",
    "SHA256SUMS",
    "figure.pdf",
    "figure.svg",
    "figure.png",
  ];
  if (manifest.latestCompletedRelease === "r072p") {
    for (const forbidden of formalFiles) assert.equal(names.includes(forbidden), false, forbidden);
    return;
  }
  assert.equal(manifest.latestCompletedRelease, "r072q");
  for (const required of formalFiles) assert.ok(names.includes(required), required);
  const packageNames = await verifyFlatHashLedger(figure);
  const figureManifest = JSON.parse(
    await readFile(resolve(figure, "manifest.json"), "utf8"),
  );
  assert.equal(figureManifest.release, "R0.72Q");
  assert.equal(figureManifest.figureId, "fig-r072q-phase-robust-shape");
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.publication.publicCopiesComplete, true);
  const { stdout } = await run(python, [
    "research/validate_figure_package.py",
    figure,
  ]);
  assert.deepEqual(JSON.parse(stdout).errors, []);
  for (const suffix of ["pdf", "png", "svg"]) {
    assert.ok(packageNames.includes(`figure.${suffix}`));
    const master = await readFile(resolve(figure, `figure.${suffix}`));
    const published = await readFile(
      resolve(root, `public/assets/r072q/fig-r072q-phase-robust-shape.${suffix}`),
    );
    assert.equal(Buffer.compare(master, published), 0, `${suffix} public byte identity`);
  }
});
