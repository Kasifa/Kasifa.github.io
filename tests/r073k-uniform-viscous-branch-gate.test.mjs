import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { readFile, readdir, stat } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const bytes = (relative) => readFile(resolve(root, relative));
const sha256 = async (relative) =>
  createHash("sha256").update(await bytes(relative)).digest("hex");

const figureId = "fig-r073k-uniform-viscous-branch";
const figureRoot = "figures/r073k/" + figureId;
const forbidden = [
  "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
];

test("R0.73K analytic theorem closes K1--K7 without a Kato norm-resolvent shortcut", async () => {
  const [proof, analytic, adversarial, gap, report] = await Promise.all([
    text("research/r073k_uniform_viscous_branch_proof.md"),
    text("research/r073k_independent_analytic_audit.md"),
    text("research/r073k_adversarial_audit.md"),
    text("research/r073k_gap_matrix.md"),
    text("research/r073k_report-source.md"),
  ]);
  for (const token of [
    "\\Gamma_*", "b_K=0.12", "c_K=0.16", "1/25=0.04", "9/5",
    "5/9", "O(\\varepsilon)", "Bromwich", "rank one",
  ]) assert.ok(proof.includes(token), token);
  assert.match(report, /fullNormResolventConvergence=FALSE/);
  assert.match(report, /katoGeneralizedConvergenceAtEpsilonZero=FALSE/);
  assert.match(analytic, /Final decision:\*\* ANALYTIC PASS/);
  assert.match(adversarial, /Final decision:\*\* PASS/);
  for (let index = 1; index <= 7; index += 1) {
    assert.match(gap, new RegExp("\\| K" + index + " \\|[^\\n]+\\| CLOSED"), "K" + index);
  }
  assert.match(gap, /\| K8 \|[^\n]+\| OPEN/);
  assert.match(gap, /\| K9 \|[^\n]+\| CLOSED; package audit PASS/);
  assert.match(gap, /\| K10 \|[^\n]+\| OPEN/);
});

test("R0.73K finite package is sealed and remains diagnostic-only", async () => {
  const [manifest, primary, independent, validation] = await Promise.all([
    json("experiments/r073k/manifest.json"),
    json("experiments/r073k/viscous_branch_diagnostic.json"),
    json("experiments/r073k/independent_validation.json"),
    json("experiments/r073k/package_validation.json"),
  ]);
  assert.equal(manifest.schemaVersion, "r073k-finite-diagnostic-manifest-v1");
  assert.equal(manifest.status, "sealed");
  assert.ok(Object.values(manifest.checks).every(Boolean));
  assert.deepEqual(manifest.claimBoundary, {
    clayProblemSolved: false,
    continuumTheoremCertifiedByThisManifest: false,
    finiteDimensionalDiagnosticSealed: true,
  });
  assert.equal(primary.schemaVersion, "r073k-viscous-branch-diagnostic-v1");
  assert.equal(primary.status, "passed");
  assert.equal(primary.allChecksPass, true);
  assert.equal(primary.rows.length, 1190);
  assert.equal(primary.crossCutoffComparisons.length, 952);
  assert.equal(primary.claimBoundary.fixedCircleCountIsContinuumRieszRankProof, false);
  assert.equal(primary.claimBoundary.uniformViscosityThresholdCertifiedHere, false);
  assert.ok(primary.maximums.largestTwoCutoffsCoreEigenvalueDifference < 7.6e-15);
  assert.ok(primary.maximums.largestTwoCutoffsCoreEmbeddedProjectorDifference < 5.7e-14);
  assert.equal(independent.schemaVersion, "r073k-independent-finite-validation-v1");
  assert.equal(independent.allChecksPass, true);
  assert.equal(independent.validator.importsPrimaryProducer, false);
  assert.equal(independent.validator.matrixConstruction, "explicit Fourier coefficients of W_d and W_d''");
  assert.ok(independent.maximumAbsoluteErrors.lambdaReal < 1.1e-14);
  assert.ok(independent.maximumAbsoluteErrors.lambdaQuotientReal < 3.7e-7);
  assert.equal(validation.schemaVersion, "r073k-package-validation-v1");
  assert.equal(validation.status, "passed");
  assert.equal(validation.allChecksPass, true);
  assert.deepEqual(
    [validation.details.primaryRows, validation.details.crossCutoffRows,
      validation.details.checksumCount, validation.details.manifestFileCount],
    [1190, 952, 16, 15],
  );
  assert.ok(Object.values(validation.checks).every(Boolean));
});

test("R0.73K experiment SHA256 ledger binds the complete sealed inputs", async () => {
  const rows = (await text("experiments/r073k/SHA256SUMS")).trim().split("\n");
  assert.equal(rows.length, 16);
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^\\\r\n]+)$/);
    assert.ok(match, row);
    names.push(match[2]);
    assert.equal(await sha256(match[2]), match[1], match[2]);
  }
  assert.equal(new Set(names).size, names.length);
  assert.ok(names.includes("research/r073k_viscous_branch_diagnostic.py"));
  assert.ok(names.includes("experiments/r073k/manifest.json"));
});

test("R0.73K release ledger verifier rejects traversal and undeclared cross-directory paths", () => {
  const code = [
    "import hashlib, tempfile",
    "from pathlib import Path",
    "import generate_r073k_release as g",
    "with tempfile.TemporaryDirectory() as raw:",
    "    g.ROOT=Path(raw).resolve()",
    "    package=g.ROOT/'package'",
    "    package.mkdir()",
    "    payload=b'bound'",
    "    (package/'file.txt').write_bytes(payload)",
    "    digest=hashlib.sha256(payload).hexdigest()",
    "    (package/'SHA256SUMS').write_text(digest+'  file.txt\\n')",
    "    g.verify_flat_ledger(package, 'unit', require_sorted=True)",
    "    for bad in ('../outside.txt', '/tmp/outside.txt', 'other/file.txt'):",
    "        (package/'SHA256SUMS').write_text(digest+'  '+bad+'\\n')",
    "        try:",
    "            g.verify_flat_ledger(package, 'unit', require_sorted=True)",
    "        except RuntimeError:",
    "            pass",
    "        else:",
    "            raise AssertionError('unsafe ledger path accepted: '+bad)",
    "print('ledger-boundary-ok')",
  ].join("\n");
  const run = spawnSync("python3", ["-c", code], {
    cwd: root,
    encoding: "utf8",
    env: { ...process.env, PYTHONPATH: resolve(root, "scripts") },
  });
  assert.equal(run.status, 0, run.stderr);
  assert.match(run.stdout, /ledger-boundary-ok/);
});

test("R0.73K formal figure is exact, vector, 600 dpi, and finite-only", async () => {
  const [manifest, results, validation] = await Promise.all([
    json(figureRoot + "/manifest.json"),
    json(figureRoot + "/results.json"),
    json(figureRoot + "/validation.json"),
  ]);
  assert.equal(manifest.schemaVersion, "r073k-uniform-viscous-branch-figure-manifest-v1");
  assert.equal(manifest.figureId, figureId);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.equal(manifest.publication.assets.length, 3);
  assert.equal(manifest.claimBoundary.finiteDimensionalDiagnostic, true);
  assert.equal(manifest.claimBoundary.continuumViscousBranchCertifiedByFigure, false);
  assert.equal(manifest.claimBoundary.explicitContinuumViscosityThresholdCertified, false);
  assert.equal(manifest.claimBoundary.clayProblemSolved, false);
  assert.equal(results.status, "passed");
  assert.equal(results.allChecksPass, true);
  assert.deepEqual(results.rowCounts, {
    crossCutoff: 952,
    crossCutoffSummaries: 4,
    cutoffSummaries: 5,
    displayCore: 204,
    primary: 1190,
    sourceData: 213,
  });
  assert.ok(results.decisions.maximumCoreProjectorDifference < 0.181);
  assert.ok(results.decisions.maximumCoreProjectorNorm < 1.684);
  assert.ok(results.decisions.minimumCoreLeftRightOverlap > 0.593);
  assert.ok(results.decisions.maximumCoreLambdaImaginaryAbs < 1.4e-15);
  assert.equal(validation.status, "passed");
  assert.equal(validation.automaticStatus, "passed");
  assert.equal(validation.allChecksPass, true);
  assert.equal(Object.keys(validation.checks).length, 22);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.deepEqual(validation.formats.pngPixels, [4204, 2787]);
  assert.deepEqual(validation.formats.pngDpiMetadata, [599.9988, 599.9988]);
  assert.equal(validation.formats.pdfImageXObjects, 0);
  assert.equal(validation.formats.svgRasterImages, 0);
  const actual = (await readdir(resolve(root, figureRoot), { withFileTypes: true }))
    .filter((entry) => entry.isFile()).map((entry) => entry.name).sort();
  const ledger = (await text(figureRoot + "/SHA256SUMS")).trim().split("\n");
  assert.equal(ledger.length, 23);
  assert.deepEqual(ledger.map((row) => row.slice(66)), actual.filter((name) => name !== "SHA256SUMS"));
  for (const name of ["figure.pdf", "figure.svg", "figure.png"]) {
    const info = await stat(resolve(root, figureRoot, name));
    assert.ok(info.size > 1000, name);
  }
});

test("R0.73K release generator pins frozen stages and fails closed until source pin", async () => {
  const generator = await text("scripts/generate_r073k_release.py");
  for (const [name, value] of [
    ["ANALYTIC_SOURCE_COMMIT", "631127efdebbeaf5f41c60e16cb976e43fdbbfbf"],
    ["EXPERIMENT_PACKAGE_COMMIT", "ce0cfc6ad54060c1ac4fb1fa449e367f361f95ea"],
    ["FIGURE_PACKAGE_COMMIT", "07ed776a7f116f0a5f447c2f4c8b6203313d77eb"],
    ["RELEASE_BASELINE_COMMIT", "07ed776a7f116f0a5f447c2f4c8b6203313d77eb"],
  ]) assert.ok(generator.includes(name + ' = "' + value + '"'), name);
  const sourcePin = generator.match(/RELEASE_SOURCE_COMMIT = "([^"]+)"/);
  assert.ok(sourcePin, "release-source pin");
  assert.ok(
    sourcePin[1] === "TO_BE_FILLED_RELEASE_SOURCE_COMMIT" || /^[0-9a-f]{40}$/.test(sourcePin[1]),
    "release-source pin is a placeholder or a full SHA",
  );
  assert.ok(generator.includes("tests/r073k-uniform-viscous-branch-gate.test.mjs"));
  assert.ok(generator.includes("research/r073k_uniform_viscous_branch_proof.md"));
  assert.ok(generator.includes("research/r073k_finite_diagnostic_audit.md"));

  const help = spawnSync("python3", ["scripts/generate_r073k_release.py", "--help"], {
    cwd: root, encoding: "utf8",
  });
  assert.equal(help.status, 0, help.stderr);
  const check = spawnSync("python3", ["scripts/generate_r073k_release.py", "--check-only"], {
    cwd: root, encoding: "utf8",
  });
  if (sourcePin[1] === "TO_BE_FILLED_RELEASE_SOURCE_COMMIT") {
    assert.notEqual(check.status, 0);
    assert.match(check.stderr, /intentionally sealed shut/);
  } else {
    assert.equal(check.status, 0, check.stderr);
    assert.match(check.stdout, /"release": "R0\.73K"/);
  }
});

test("R0.73K reader-facing sources obey individual-researcher voice", async () => {
  const sources = await Promise.all([
    text("scripts/r073k_release_content.py"),
    text("research/r073k_report-source.md"),
    text("research/r073k_literature_audit.md"),
    text("research/r073k_bilingual_dictionary.md"),
  ]);
  for (const [index, value] of sources.entries()) {
    for (const phrase of forbidden) {
      assert.equal(value.includes(phrase), false, "source " + String(index + 1) + ": " + phrase);
    }
  }
});
