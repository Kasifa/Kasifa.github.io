import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { cp, mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const directory = "research/certificates/r073e";
const sourceCommit = "803279d72c24a54db27c40dcdad97593636788fc";
const bundledPython = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const python = process.env.CODEX_PYTHON || (existsSync(bundledPython) ? bundledPython : "python3");
const run = promisify(execFile);

const closedClaims = [
  "fixedPositiveHalfPlaneNoPollution",
  "allModesRightOfBProjectionNormPersistence",
  "topInviscidClusterExists",
  "topViscousClusterPersistence",
  "topReducedHalfPlaneResolventUniform",
  "frozenTopClusterRelativeDichotomy",
  "fixedFrozenGeneratorVolterraTransfer",
  "logFastTimeTransfer",
  "superPolynomialCompleteRowNoGo",
];

const openClaims = [
  "certifiedSigmaStarIsRightmost",
  "selectedSigmaStarComplementDichotomy",
  "uniformHalfPlaneBoundAtBEqualsZero",
  "globalRightHalfPlaneNoPollution",
  "absoluteUniformComplementDecay",
  "explicitHalfPlaneGap",
  "explicitViscosityThreshold",
  "quantitativeEigenvalueRate",
  "movingProfileUniformContour",
  "graphDomainKatoTransport",
  "movingProfileEvolutionDichotomy",
  "inviscidRootUnique",
  "inviscidEigenvalueSimple",
  "completeOSSquireA2DirectSum",
  "fixedWindowExponentialLowerLaw",
  "nonlinearNavierStokes",
  "Clay",
];

const sourcePaths = [
  "research/r073e_problem_freeze.md",
  "research/r073e_halfplane_transfer_proof.md",
  "research/r073e_independent_analytic_audit.md",
  "research/r073e_literature_audit.md",
  "research/r073e_gap_matrix.md",
  "research/r073e_report-source.md",
  "experiments/r073e/README.md",
  "experiments/r073e/command.txt",
  "experiments/r073e/environment.json",
  "experiments/r073e/requirements.txt",
  "experiments/r073e/diagnose_complement.py",
  "experiments/r073e/complement_diagnostic.json",
  "experiments/r073e/progress.ndjson",
  "experiments/r073e/independent_validate.py",
  "experiments/r073e/independent_validation.json",
  "experiments/r073e/SHA256SUMS",
  "figures/r073e/fig-r073e-complement-transfer/manifest.json",
  "figures/r073e/fig-r073e-complement-transfer/validation.json",
];

const packagePaths = [
  `${directory}/README.md`,
  `${directory}/command.txt`,
  `${directory}/environment.txt`,
  `${directory}/generate_certificate.py`,
  `${directory}/independent_recompute.py`,
  `${directory}/validate_certificate.py`,
];

const generatedPaths = [
  `${directory}/certificate.json`,
  `${directory}/independent_recompute.json`,
  `${directory}/validation.json`,
  `${directory}/progress.ndjson`,
  `${directory}/manifest.json`,
  `${directory}/SHA256SUMS`,
];

async function bytes(relative) {
  return readFile(resolve(root, relative));
}

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

async function fileSha256(relative) {
  return sha256(await bytes(relative));
}

async function gitBytes(args) {
  return (await run("git", args, { cwd: root, encoding: "buffer", maxBuffer: 32 * 1024 * 1024 })).stdout;
}

function exactKeys(value, keys, label) {
  assert.ok(value && typeof value === "object" && !Array.isArray(value), `${label}: object`);
  assert.deepEqual(Object.keys(value).sort(), [...keys].sort(), `${label}: exact keys`);
}

function parseLedger(raw) {
  assert.ok(raw.endsWith("\n"), "SHA256SUMS ends with newline");
  return raw.slice(0, -1).split("\n").map((row) => {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `malformed checksum row: ${row}`);
    return { sha256: match[1], name: match[2] };
  });
}

test("R0.73E certificate Python sources parse without executing producers", async () => {
  const script = [
    "import ast, pathlib, sys",
    "for raw in sys.argv[1:]:",
    " ast.parse(pathlib.Path(raw).read_text(encoding='utf-8'), filename=raw)",
    "print('three R0.73E sources parsed')",
  ].join("\n");
  const result = await run(python, ["-c", script, ...packagePaths.filter((path) => path.endsWith(".py"))], {
    cwd: root,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.equal(result.stdout, "three R0.73E sources parsed\n");
});

test("R0.73E certificate seals exactly nine CLOSED and seventeen OPEN claims", async () => {
  const certificate = await json(`${directory}/certificate.json`);
  exactKeys(certificate, [
    "schemaVersion", "release", "created", "sourceCommit", "sourceBindings",
    "closedClaims", "openClaims", "checks", "analyticSentinels",
    "finiteDiagnostics", "formalFigure", "claimBoundary",
  ], "certificate");
  assert.equal(certificate.schemaVersion, "r073e-deterministic-analytic-certificate-v1");
  assert.equal(certificate.release, "R0.73E");
  assert.equal(certificate.created, "2026-08-30");
  assert.equal(certificate.sourceCommit, sourceCommit);
  assert.deepEqual(Object.keys(certificate.closedClaims).sort(), [...closedClaims].sort());
  assert.deepEqual(Object.values(certificate.closedClaims), Array(9).fill("CLOSED"));
  assert.deepEqual(Object.keys(certificate.openClaims).sort(), [...openClaims].sort());
  assert.deepEqual(Object.values(certificate.openClaims), Array(17).fill("OPEN"));
  assert.deepEqual(certificate.claimBoundary, Object.fromEntries(openClaims.map((name) => [name, false])));
  assert.ok(Object.values(certificate.checks).every((value) => value === true));
  assert.deepEqual(certificate.analyticSentinels, {
    certifiedEigenvalueBracket: [0.17035, 0.1705],
    fixedWindowExponentialLaw: false,
    positiveHalfPlaneUniformityAtZero: false,
    profileDriftBound: [49, 4],
  });
});

test("R0.73E source bindings are exact Git blobs at the frozen commit", async () => {
  const certificate = await json(`${directory}/certificate.json`);
  assert.deepEqual(certificate.sourceBindings.map(({ path }) => path), sourcePaths);
  for (const binding of certificate.sourceBindings) {
    exactKeys(binding, ["path", "commit", "gitBlob", "sha256", "bytes", "workingTreeBytesMatch"], `binding ${binding.path}`);
    const [working, committed] = await Promise.all([
      bytes(binding.path),
      gitBytes(["show", `${sourceCommit}:${binding.path}`]),
    ]);
    assert.deepEqual(working, committed, `${binding.path}: working bytes match source commit`);
    assert.equal(binding.commit, sourceCommit);
    assert.equal(binding.sha256, sha256(working));
    assert.equal(binding.bytes, working.length);
    assert.equal(binding.workingTreeBytesMatch, true);
  }
});

test("R0.73E finite diagnostics and figure remain formally validated but fail closed", async () => {
  const [certificate, primary, independent, figureManifest, figureValidation] = await Promise.all([
    json(`${directory}/certificate.json`),
    json("experiments/r073e/complement_diagnostic.json"),
    json("experiments/r073e/independent_validation.json"),
    json("figures/r073e/fig-r073e-complement-transfer/manifest.json"),
    json("figures/r073e/fig-r073e-complement-transfer/validation.json"),
  ]);
  assert.equal(primary.allChecksPass, true);
  assert.ok(Object.values(primary.checks).every(Boolean));
  assert.equal(independent.allChecksPass, true);
  assert.ok(Object.values(independent.checks).every(Boolean));
  assert.equal(primary.claimBoundary.finiteBinary64Diagnostic, true);
  for (const key of [
    "additionalContinuumEigenpairProvedHere", "clayProblemSolved",
    "continuousTimeSemigroupBoundProvedHere", "continuumComplementaryDichotomyProvedHere",
    "movingProfileUniformityProvedHere", "nonautonomousTransferProvedHere",
    "nonlinearNavierStokesProvedHere", "ordinaryCutoffAgreementIsContinuumProof",
  ]) assert.equal(primary.claimBoundary[key], false, key);
  assert.equal(certificate.finiteDiagnostics.evidenceClass, "finite IEEE-754 binary64 diagnostic only");
  assert.equal(certificate.finiteDiagnostics.continuumConclusion, false);
  assert.equal(certificate.finiteDiagnostics.largestCutoff, 96);
  assert.equal(certificate.finiteDiagnostics.rowCount, 15);
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureValidation.status, "passed");
  assert.ok(Object.values(figureValidation.checks).every(Boolean));
  assert.equal(certificate.formalFigure.validationStatus, "passed");
  assert.equal(certificate.formalFigure.png.dpi, 600);
  for (const key of [
    "continuumComplementDichotomyProvedHere", "nonautonomousTransferProvedHere",
    "nonlinearNavierStokesProvedHere", "clayProblemSolved",
  ]) assert.equal(figureManifest.claimBoundary[key], false, key);
});

test("R0.73E independent path reparses sources and never reads the primary certificate", async () => {
  const [output, script] = await Promise.all([
    json(`${directory}/independent_recompute.json`),
    text(`${directory}/independent_recompute.py`),
  ]);
  assert.equal(output.schemaVersion, "r073e-independent-source-recompute-v1");
  assert.equal(output.sourceCommit, sourceCommit);
  assert.deepEqual(output.reparsedClaims, { closed: closedClaims, open: openClaims });
  assert.deepEqual(output.exactSentinels.profileDriftBound, [49, 4]);
  assert.equal(output.exactSentinels.largestCutoff, 96);
  assert.ok(output.exactSentinels.minimumVerticalLineMarginOverFiniteQSpectrum > 0);
  assert.ok(output.exactSentinels.selectedQSpectralAbscissa > 0);
  assert.equal(output.implementation.stdlibOnly, true);
  assert.equal(output.implementation.importsPrimaryGenerator, false);
  assert.equal(output.implementation.readsPrimaryCertificate, false);
  assert.equal(output.implementation.scriptSha256, await fileSha256(`${directory}/independent_recompute.py`));
  assert.equal(output.allChecksPass, true);
  assert.ok(Object.values(output.checks).every(Boolean));
  assert.equal(output.claimBoundary.continuumSpectrumCertified, false);
  assert.equal(output.claimBoundary.continuousTimeBoundCertified, false);
  assert.equal(output.claimBoundary.nonlinearNavierStokesCertified, false);
  assert.equal(output.claimBoundary.clayProblemSolved, false);
  assert.ok(!script.includes("certificate.json"), "independent script must not read/copy primary certificate");
  assert.ok(!script.includes("generate_certificate"), "independent script must not import/copy primary generator");
});

test("R0.73E validator, manifest, and checksum ledger agree exactly", async () => {
  const [validation, manifest, checksumText] = await Promise.all([
    json(`${directory}/validation.json`),
    json(`${directory}/manifest.json`),
    text(`${directory}/SHA256SUMS`),
  ]);
  assert.equal(validation.schemaVersion, "r073e-certificate-validation-v1");
  assert.equal(validation.release, "R0.73E");
  assert.equal(validation.sourceCommit, sourceCommit);
  assert.equal(validation.allChecksPass, true);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.equal(manifest.schemaVersion, "r073e-certificate-manifest-v1");
  assert.equal(manifest.sourceCommit, sourceCommit);
  assert.deepEqual(manifest.sourceBindings.map(({ path }) => path), sourcePaths);
  assert.deepEqual(manifest.packageBindings.map(({ path }) => path), packagePaths);
  assert.deepEqual(manifest.outputs, [
    "certificate.json", "independent_recompute.json", "validation.json",
    "progress.ndjson", "manifest.json", "SHA256SUMS",
  ]);
  assert.equal(manifest.limitations.length, 5);
  for (const binding of [...manifest.packageBindings, ...manifest.outputBindings]) {
    exactKeys(binding, ["path", "sha256", "bytes"], `file binding ${binding.path}`);
    assert.equal(binding.sha256, await fileSha256(binding.path));
    assert.equal(binding.bytes, (await bytes(binding.path)).length);
  }
  const ledger = parseLedger(checksumText);
  assert.deepEqual(ledger.map(({ name }) => name), [
    "certificate.json", "independent_recompute.json", "validation.json", "progress.ndjson", "manifest.json",
  ]);
  assert.equal(new Set(ledger.map(({ name }) => name)).size, ledger.length);
  for (const row of ledger) assert.equal(row.sha256, await fileSha256(`${directory}/${row.name}`));
});

test("R0.73E producer sequence is byte deterministic", async () => {
  const before = new Map(await Promise.all(generatedPaths.map(async (path) => [path, await bytes(path)])));
  const temporaryParent = await mkdtemp(join(tmpdir(), "r073e-certificate-rerun-"));
  const sourceTree = join(temporaryParent, "source");
  let worktreeAdded = false;
  try {
    await run("git", ["worktree", "add", "--detach", sourceTree, sourceCommit], {
      cwd: root,
      maxBuffer: 32 * 1024 * 1024,
    });
    worktreeAdded = true;
    await cp(resolve(root, directory), resolve(sourceTree, directory), { recursive: true });
    for (const script of ["generate_certificate.py", "independent_recompute.py", "validate_certificate.py"]) {
      await run(python, [`${directory}/${script}`], {
        cwd: sourceTree,
        env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
        maxBuffer: 32 * 1024 * 1024,
      });
    }
    for (const path of generatedPaths) {
      assert.deepEqual(await readFile(resolve(sourceTree, path)), before.get(path), `${path}: deterministic rerun`);
    }
  } finally {
    if (worktreeAdded) {
      await run("git", ["worktree", "remove", "--force", sourceTree], { cwd: root });
    }
    await rm(temporaryParent, { recursive: true, force: true });
  }
});
