import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { readFile, stat } from "node:fs/promises";
import { dirname, resolve, sep } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificateDirectory = "research/certificates/r073d";
const sourceCommit = "0ee38ce87d12c2478df12f66bdef5682085f50a7";
const certificateCommit = "6e4a8bd8aca404fc1d0eff050fe4e0809117072d";
const bundledPython = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const python = process.env.CODEX_PYTHON || (existsSync(bundledPython) ? bundledPython : "python3");
const run = promisify(execFile);

const pythonSources = [
  `${certificateDirectory}/generate_certificate.py`,
  `${certificateDirectory}/independent_recompute.py`,
  `${certificateDirectory}/validate_certificate.py`,
];

const expectedSourcePaths = [
  "research/r073d_problem_freeze.md",
  "research/r073d_viscous_persistence_proof.md",
  "research/r073d_independent_analytic_audit.md",
  "research/r073d_literature_audit.md",
  "research/r073d_gap_matrix.md",
  "research/r073d_report-source.md",
  "research/r073d_viscous_cluster_diagnostic.py",
  "experiments/r073d/README.md",
  "experiments/r073d/command.txt",
  "experiments/r073d/environment.json",
  "experiments/r073d/requirements.txt",
  "experiments/r073d/viscous_cluster_diagnostic.json",
  "experiments/r073d/progress.ndjson",
  "experiments/r073d/independent_validate.py",
  "experiments/r073d/independent_validation.json",
  "research/certificates/r073d/generate_certificate.py",
  "research/certificates/r073d/independent_recompute.py",
  "research/certificates/r073d/validate_certificate.py",
  "research/certificates/r073d/README.md",
  "research/certificates/r073d/command.txt",
  "research/certificates/r073d/environment.txt",
];

const expectedBoundOutputs = [
  `${certificateDirectory}/certificate.json`,
  `${certificateDirectory}/independent_recompute.json`,
  `${certificateDirectory}/validation.json`,
  `${certificateDirectory}/progress.ndjson`,
];

// This is the validator's sealed output order.  R0.73D deliberately hashes
// only generated outputs; source files are covered by sourceBindings instead.
const expectedLedgerNames = [
  "certificate.json",
  "independent_recompute.json",
  "validation.json",
  "progress.ndjson",
  "manifest.json",
];

const expectedSealedOutputs = [
  ...expectedLedgerNames.map((name) => `${certificateDirectory}/${name}`),
  `${certificateDirectory}/SHA256SUMS`,
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

async function gitText(args) {
  const result = await run("git", args, {
    cwd: root,
    encoding: "utf8",
    maxBuffer: 16 * 1024 * 1024,
  });
  return result.stdout;
}

async function gitBytes(args) {
  const result = await run("git", args, {
    cwd: root,
    encoding: "buffer",
    maxBuffer: 16 * 1024 * 1024,
  });
  return result.stdout;
}

function exactKeys(value, keys, label) {
  assert.ok(value && typeof value === "object" && !Array.isArray(value), `${label}: object`);
  assert.deepEqual(Object.keys(value).sort(), [...keys].sort(), `${label}: exact keys`);
}

function parseLedger(raw, label = "SHA256SUMS") {
  assert.ok(raw.endsWith("\n"), `${label}: final newline`);
  const rows = raw.slice(0, -1).split("\n");
  const parsed = rows.map((row) => {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `${label}: malformed or non-flat row: ${row}`);
    return { sha256: match[1], name: match[2] };
  });
  assert.equal(new Set(parsed.map(({ name }) => name)).size, parsed.length, `${label}: duplicate name`);
  return parsed;
}

async function snapshot(paths) {
  return new Map(await Promise.all(paths.map(async (relative) => [relative, await bytes(relative)])));
}

test("R0.73D all three Python sources parse without executing either producer path", async () => {
  const script = [
    "import ast, pathlib, sys",
    "for raw in sys.argv[1:]:",
    " data = pathlib.Path(raw).read_text(encoding='utf-8')",
    " ast.parse(data, filename=raw)",
    "print('three R0.73D sources parsed')",
  ].join("\n");
  const result = await run(python, ["-c", script, ...pythonSources], {
    cwd: root,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    maxBuffer: 16 * 1024 * 1024,
  });
  assert.equal(result.stdout, "three R0.73D sources parsed\n");
});

test("R0.73D certificate, manifest, validation, and independent schemas fail closed exactly", async () => {
  const [certificate, manifest, validation, independent] = await Promise.all([
    json(`${certificateDirectory}/certificate.json`),
    json(`${certificateDirectory}/manifest.json`),
    json(`${certificateDirectory}/validation.json`),
    json(`${certificateDirectory}/independent_recompute.json`),
  ]);

  exactKeys(certificate, [
    "schemaVersion", "release", "created", "sourceCommit", "theorem", "checks",
    "finiteDiagnostics", "literatureBoundary", "claimBoundary",
  ], "certificate");
  assert.equal(certificate.schemaVersion, "r073d-analytic-certificate-v1");
  assert.equal(certificate.release, "R0.73D");
  assert.equal(certificate.created, "2026-08-30");
  assert.equal(certificate.sourceCommit, sourceCommit);
  assert.deepEqual(certificate.theorem, {
    contourRadiusExplicit: false,
    fixedClusterAlgebraicMultiplicityPreserved: "CLOSED",
    fixedClusterEigenvaluesConverge: "CLOSED",
    fixedClusterRieszProjectionNormConvergence: "CLOSED",
    fixedContourResolventUniform: "CLOSED",
    inheritedInviscidBracket: [0.17035, 0.1705],
    inviscidAlgebraicMultiplicityKnown: false,
    staticVanishingViscosityPersistence: "CLOSED",
    viscosityThresholdExplicit: false,
  });
  assert.deepEqual(certificate.checks, {
    analyticBaseContourIntegralZero: true,
    baseResolventStrongAndAdjointStrong: true,
    commutatorCompactnessPresent: true,
    fastTimeRemainsOpen: true,
    finiteEvidenceFailClosed: true,
    finiteIndependentChecksPass: true,
    finitePrimaryChecksPass: true,
    fredholmFactorPresent: true,
    generalPrecedentAcknowledged: true,
    independentAnalyticAuditPass: true,
    kineticSpaceDefinedByCompletion: true,
    multiplicityPreserved: true,
    nonlinearAndClayRemainOpen: true,
    projectionNormConvergenceProved: true,
    singularDomainJumpPresent: true,
    unitaryTransformPresent: true,
  });
  assert.deepEqual(certificate.literatureBoundary, {
    fixedRowSelfContainedNormProof: true,
    generalPersistencePrecedent: "Shvydkoy-Friedlander 2008",
    generalPriorityClaimMade: false,
  });
  assert.deepEqual(certificate.claimBoundary, {
    clayProblemSolved: false,
    completeOSSquireA2DirectSum: false,
    globalRightHalfPlaneNoPollution: false,
    inviscidEigenvalueSimple: false,
    inviscidRootUnique: false,
    logFastTimeTransfer: false,
    movingProfileUniformContour: false,
    nonlinearNavierStokes: false,
    quantitativeEigenvalueRate: false,
    uniformComplementaryDichotomy: false,
  });
  exactKeys(certificate.finiteDiagnostics, [
    "evidenceClass", "largestCutoff", "sentinels", "maximums", "independentMaximumErrors",
  ], "certificate.finiteDiagnostics");
  assert.equal(certificate.finiteDiagnostics.evidenceClass, "finite diagnostic only");
  assert.equal(certificate.finiteDiagnostics.largestCutoff, 128);
  assert.deepEqual(Object.keys(certificate.finiteDiagnostics.maximums).sort(), [
    "embeddedResidualAllCutoffs",
    "embeddedResidualLargestCutoff",
    "largestTwoCutoffsEigenvalueDifference",
  ]);
  assert.deepEqual(Object.keys(certificate.finiteDiagnostics.independentMaximumErrors).sort(), [
    "eigenvalueAbsolute",
    "embeddedResidualAbsolute",
    "leftRightPairingAbsolute",
    "projectorDifferenceAbsolute",
    "projectorNormAbsolute",
  ]);
  assert.deepEqual(certificate.finiteDiagnostics.sentinels.map(({ epsilon }) => epsilon), [
    0, 0.01, 0.0001, 0.000001, 1e-8,
  ]);
  for (const [index, sentinel] of certificate.finiteDiagnostics.sentinels.entries()) {
    exactKeys(sentinel, [
      "N", "epsilon", "lambdaReal", "projectorNorm", "projectorDifference", "finiteDimensionalOnly",
    ], `certificate.finiteDiagnostics.sentinels[${index}]`);
    assert.equal(sentinel.N, 128);
    assert.equal(sentinel.finiteDimensionalOnly, true);
    for (const key of ["epsilon", "lambdaReal", "projectorNorm", "projectorDifference"]) {
      assert.equal(typeof sentinel[key], "number", `sentinel ${index}: ${key}`);
      assert.ok(Number.isFinite(sentinel[key]), `sentinel ${index}: finite ${key}`);
    }
  }

  exactKeys(manifest, [
    "schemaVersion", "release", "created", "sourceCommit", "sourceBindingKind",
    "sourceBindings", "outputBindings", "outputs", "limitations",
  ], "manifest");
  assert.equal(manifest.schemaVersion, "r073d-certificate-manifest-v1");
  assert.equal(manifest.release, "R0.73D");
  assert.equal(manifest.created, "2026-08-30");
  assert.equal(manifest.sourceCommit, sourceCommit);
  assert.equal(manifest.sourceBindingKind, "exact Git commit blobs and byte-identical working sources");
  assert.deepEqual(manifest.sourceBindings.map(({ path }) => path), expectedSourcePaths);
  assert.deepEqual(manifest.outputBindings.map(({ path }) => path), expectedBoundOutputs);
  assert.deepEqual(manifest.outputs, [
    "certificate.json", "independent_recompute.json", "validation.json",
    "progress.ndjson", "manifest.json", "SHA256SUMS",
  ]);
  assert.deepEqual(manifest.limitations, [
    "the isolating radius and viscosity threshold are existential",
    "the inviscid algebraic multiplicity is not identified",
    "finite Fourier rows are diagnostics only",
    "the whole right-half-plane complement and fast-time transfer remain open",
    "no nonlinear Navier-Stokes or Clay conclusion is claimed",
  ]);
  for (const [index, binding] of manifest.sourceBindings.entries()) {
    exactKeys(binding, [
      "path", "commit", "gitBlob", "sha256", "bytes", "workingTreeBytesMatch",
    ], `manifest.sourceBindings[${index}]`);
  }
  for (const [index, binding] of manifest.outputBindings.entries()) {
    exactKeys(binding, ["path", "sha256", "bytes"], `manifest.outputBindings[${index}]`);
  }

  assert.deepEqual(validation, {
    allChecksPass: true,
    checks: {
      clayFailClosed: true,
      commutatorSentinel: true,
      compactBoundSentinel: true,
      fastTimeFailClosed: true,
      independentAllChecksPass: true,
      nonlinearFailClosed: true,
      primaryAllChecksPass: true,
      projectionStatusClosed: true,
      sourceCommitAgreement: true,
      staticStatusClosed: true,
    },
    release: "R0.73D",
    schemaVersion: "r073d-certificate-validation-v1",
    sourceCommit,
  });

  assert.deepEqual(independent, {
    allChecksPass: true,
    checks: {
      clayOpen: true,
      commutatorFourierL1SumEqualsOne: true,
      domainJumpRecorded: true,
      fastTimeOpen: true,
      finiteClaimBoundary: true,
      finiteIndependentPass: true,
      finitePrimaryPass: true,
      fixedClusterStatusesClosed: true,
      projectionNormLimitRecorded: true,
      roughCompactTermBoundEqualsFour: true,
    },
    claimBoundary: {
      doesNotProveFastTimeTransfer: true,
      doesNotProveNonlinearNavierStokes: true,
      doesNotProveSimplicity: true,
      recomputesAnalyticSentinelsOnly: true,
    },
    exactSentinels: {
      commutatorFourierL1Sum: [1, 1],
      roughCompactTermBound: [4, 1],
    },
    implementation: {
      importsPrimaryCertificateGenerator: false,
      scriptSha256: "d069103d7c2be985aed10e9121038916e07ff348790860a4885a2302ac5759a8",
      stdlibOnly: true,
    },
    release: "R0.73D",
    schemaVersion: "r073d-independent-analytic-recompute-v1",
    sourceCommit,
  });
});

test("R0.73D source and output bindings resolve to exact working and Git bytes", async () => {
  const resolvedCommit = (await gitText(["rev-parse", "--verify", `${sourceCommit}^{commit}`])).trim();
  assert.equal(resolvedCommit, sourceCommit);
  assert.equal((await gitText(["cat-file", "-t", sourceCommit])).trim(), "commit");

  const manifest = await json(`${certificateDirectory}/manifest.json`);
  assert.equal(manifest.sourceCommit, sourceCommit);
  assert.deepEqual(manifest.sourceBindings.map(({ path }) => path), expectedSourcePaths);
  for (const binding of manifest.sourceBindings) {
    assert.equal(binding.commit, sourceCommit, `${binding.path}: commit`);
    assert.equal(binding.workingTreeBytesMatch, true, `${binding.path}: workingTreeBytesMatch`);
    assert.ok(!binding.path.startsWith("/") && !binding.path.split(/[\\/]/).includes(".."), `${binding.path}: relative path`);
    const absolute = resolve(root, binding.path);
    assert.ok(absolute.startsWith(root + sep), `${binding.path}: inside repository`);
    assert.equal((await stat(absolute)).isFile(), true, `${binding.path}: regular file exists`);
    const working = await bytes(binding.path);
    assert.equal(working.length, binding.bytes, `${binding.path}: bytes`);
    assert.equal(sha256(working), binding.sha256, `${binding.path}: sha256`);
    const objectSpec = `${sourceCommit}:${binding.path}`;
    const committed = await gitBytes(["show", objectSpec]);
    assert.deepEqual(committed, working, `${binding.path}: committed bytes`);
    const blob = (await gitText(["rev-parse", objectSpec])).trim();
    assert.equal(blob, binding.gitBlob, `${binding.path}: gitBlob`);
    assert.equal((await gitText(["cat-file", "-t", blob])).trim(), "blob", `${binding.path}: blob exists`);
  }

  assert.deepEqual(manifest.outputBindings.map(({ path }) => path), expectedBoundOutputs);
  for (const binding of manifest.outputBindings) {
    const absolute = resolve(root, binding.path);
    assert.ok(absolute.startsWith(root + sep), `${binding.path}: inside repository`);
    assert.equal((await stat(absolute)).isFile(), true, `${binding.path}: regular file exists`);
    const output = await bytes(binding.path);
    assert.equal(output.length, binding.bytes, `${binding.path}: bytes`);
    assert.equal(sha256(output), binding.sha256, `${binding.path}: sha256`);
  }
});

test("R0.73D certificate is parseable and hash-consistent in the sealing commit", async () => {
  const resolvedCommit = (await gitText(["rev-parse", "--verify", `${certificateCommit}^{commit}`])).trim();
  assert.equal(resolvedCommit, certificateCommit);
  assert.equal((await gitText(["cat-file", "-t", certificateCommit])).trim(), "commit");

  const certificatePath = `${certificateDirectory}/certificate.json`;
  const [committedCertificate, committedManifest, committedLedger] = await Promise.all([
    gitBytes(["show", `${certificateCommit}:${certificatePath}`]),
    gitBytes(["show", `${certificateCommit}:${certificateDirectory}/manifest.json`]),
    gitText(["show", `${certificateCommit}:${certificateDirectory}/SHA256SUMS`]),
  ]);
  const parsedCertificate = JSON.parse(committedCertificate.toString("utf8"));
  const parsedManifest = JSON.parse(committedManifest.toString("utf8"));
  assert.equal(parsedCertificate.schemaVersion, "r073d-analytic-certificate-v1");
  assert.equal(parsedCertificate.sourceCommit, sourceCommit);
  assert.equal(parsedManifest.sourceCommit, sourceCommit);
  const committedHash = sha256(committedCertificate);
  const manifestBinding = parsedManifest.outputBindings.find(({ path }) => path === certificatePath);
  assert.ok(manifestBinding, "sealing commit manifest binds certificate.json");
  assert.equal(manifestBinding.bytes, committedCertificate.length);
  assert.equal(manifestBinding.sha256, committedHash);
  const ledgerBinding = parseLedger(committedLedger, "sealing commit SHA256SUMS")
    .find(({ name }) => name === "certificate.json");
  assert.ok(ledgerBinding, "sealing commit ledger binds certificate.json");
  assert.equal(ledgerBinding.sha256, committedHash);
  assert.deepEqual(await bytes(certificatePath), committedCertificate, "working certificate equals sealing commit bytes");
});

test("R0.73D SHA256SUMS is flat, uniquely ordered by its declared coverage, and exact", async () => {
  const manifest = await json(`${certificateDirectory}/manifest.json`);
  const ledger = parseLedger(await text(`${certificateDirectory}/SHA256SUMS`));
  const names = ledger.map(({ name }) => name);
  assert.deepEqual(names, expectedLedgerNames);
  assert.deepEqual(names, manifest.outputs.filter((name) => name !== "SHA256SUMS"));
  assert.deepEqual(names.slice(0, -1).map((name) => `${certificateDirectory}/${name}`), expectedBoundOutputs);
  for (const row of ledger) {
    assert.equal(await fileSha256(`${certificateDirectory}/${row.name}`), row.sha256, row.name);
  }
});

test("R0.73D validator alone reproduces byte-identical sealed outputs", async () => {
  const before = await snapshot(expectedSealedOutputs);
  const result = await run(python, [`${certificateDirectory}/validate_certificate.py`], {
    cwd: root,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    maxBuffer: 16 * 1024 * 1024,
  });
  assert.deepEqual(JSON.parse(result.stdout), {
    allChecksPass: true,
    event: "certificate-validated",
  });
  const after = await snapshot(expectedSealedOutputs);
  for (const relative of expectedSealedOutputs) {
    assert.deepEqual(after.get(relative), before.get(relative), `${relative}: byte-stable`);
  }
});
