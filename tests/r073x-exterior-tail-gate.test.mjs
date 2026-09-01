import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, lstatSync, readFileSync, readdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");
const bytes = (relative) => readFileSync(resolve(root, relative));
const json = (relative) => JSON.parse(read(relative));
const sha256 = (payload) => createHash("sha256").update(payload).digest("hex");
const regular = (relative) => {
  const path = resolve(root, relative);
  return existsSync(path) && lstatSync(path).isFile() && !lstatSync(path).isSymbolicLink();
};
const conflictCopy = (name) => / \d+(?=\.[^.]+$|$)/.test(name);

const title =
  "R0.73X | Localized heat ledgers with explicit exterior tails: Gaussian " +
  "velocity control, algebraic pressure tails, and the open coercivity bridge";
const publicTitle =
  "R0.73X｜带显式外部尾项的局部热账本：Gaussian 速度控制、代数压力尾与未闭合 coercivity 桥";
const sourceCommit = "958b6b4216f6914a5d42f7712b6bc9b218caf801";
const figureId = "fig-r073x-exterior-tail-ledger";
const certificateBase = "research/certificates/r073x";
const figureBase = `figures/r073x/${figureId}`;

const canonicalPaths = [
  "research/r073x_problem_freeze.md",
  "research/r073x_primary_literature_audit.md",
  "research/r073x_localized_heat_characteristic.md",
  "research/r073x_finite_diagnostic_design.md",
  "research/r073x_finite_fourier_harness_report.md",
  "research/r073x_gaussian_velocity_tail_proof.md",
  "research/r073x_gaussian_tail_certificate_report.md",
  "research/r073x_gaussian_tail_independent_audit.md",
  "research/r073x_exterior_tail_counterexample_audit.md",
  "research/r073x_pressure_tail_primary_source_ledger.md",
  "research/r073x_exterior_tail_freeze.md",
  "research/r073x_pressure_tail_independent_audit.md",
  "research/r073x_claim_state_update.md",
  "research/r073x_release_candidate_manifest.json",
  "research/r073x_claim_source_ledger.md",
  "research/r073x_evidence_gap_matrix.md",
  "research/r073x_report-source.md",
  "research/r073x_bilingual_dictionary.md",
];

const certificateNames = [
  "README.md", "SHA256SUMS", "audit-checklist.json", "claim-boundary.md",
  "command.txt", "contract.json", "fourier-producer.py", "fourier-report.md",
  "fourier-results.json", "gaussian-independent-audit.md", "gaussian-producer.py",
  "gaussian-report.md", "gaussian-results.json", "manifest.json",
  "requirements.txt", "seal_package.py",
];
const figureSourceNames = [
  "README.md", "caption.md", "chart-contract-and-source-data.md", "command.txt",
  "config.json", "contract.json", "plot.py", "qa-protocol.md", "requirements.txt",
  "validate.py",
];
const figureRawNames = [
  "environment.json", "figure.pdf", "figure.png", "figure.svg", "progress.ndjson",
  "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "resource-log.ndjson",
  "results.json", "source-data.csv",
];
const figureMetadataNames = [
  "SHA256SUMS", "manifest.json", "qa-report.md", "validation.json",
];
const figureNames = [...figureSourceNames, ...figureRawNames, ...figureMetadataNames].sort();

function sums(relativeBase) {
  const rows = new Map();
  for (const line of read(`${relativeBase}/SHA256SUMS`).trimEnd().split("\n")) {
    const match = line.match(/^([0-9a-f]{64})  ([^/]+)$/);
    assert.ok(match, `${relativeBase}/SHA256SUMS: ${line}`);
    assert.equal(rows.has(match[2]), false, `duplicate SHA256SUMS row: ${match[2]}`);
    rows.set(match[2], match[1]);
  }
  return rows;
}

function assertHashInventory(relativeBase, expectedNames, manifest) {
  const names = readdirSync(resolve(root, relativeBase)).sort();
  assert.deepEqual(names, [...expectedNames].sort());
  assert.equal(names.some(conflictCopy), false);

  const digestRows = sums(relativeBase);
  assert.deepEqual(
    [...digestRows.keys()].sort(),
    names.filter((name) => name !== "SHA256SUMS").sort(),
  );
  for (const [name, digest] of digestRows) {
    assert.equal(sha256(bytes(`${relativeBase}/${name}`)), digest, name);
  }

  const boundRows = manifest.files;
  assert.ok(Array.isArray(boundRows));
  assert.deepEqual(
    boundRows.map(({ path }) => path).sort(),
    names.filter((name) => !["manifest.json", "SHA256SUMS"].includes(name)).sort(),
  );
  for (const row of boundRows) {
    const payload = bytes(`${relativeBase}/${row.path}`);
    assert.equal(row.bytes, payload.length, row.path);
    assert.equal(row.sha256, sha256(payload), row.path);
  }
}

function sourceDryRun() {
  return JSON.parse(execFileSync(
    process.env.R073X_PYTHON ?? "python3",
    ["-B", "scripts/generate_r073x_release.py", "--source-dry-run"],
    {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  ));
}

test("the canonical ledger freezes only positive-scale absolute size and every open bridge", () => {
  const corpus = canonicalPaths.map(read).join("\n");
  const compact = corpus.replace(/\s+/g, " ");
  const report = read("research/r073x_report-source.md");
  const dictionary = read("research/r073x_bilingual_dictionary.md").replace(/\s+/g, " ");

  assert.ok(report.startsWith(`# ${title}\n`));
  assert.ok(report.includes(`**Public title (zh):** ${publicTitle}`));
  assert.ok(dictionary.includes(`**Release title:** ${title}`));
  assert.ok(dictionary.includes(`**Public title (zh):** ${publicTitle}`));
  assert.ok(report.includes("## 11. 下一步：R0.73Y"));

  for (const token of [
    "localizedHeatCharacteristicLedger=PROVED_WITH_STATED_SOLUTION_CLASS",
    "centeredIncrementCutoffSplit=EXACT_AND_FINITE_CHECKED",
    "gaussianVelocityTailLemma=INDEPENDENT_AUDIT_PASS",
    "pressureExteriorTailSizeLemma=PASS_AT_POSITIVE_SCALE",
    "positiveScaleAbsoluteSize=PROVED",
    "fixedHarmonicProbeQuadraticAbsorption=REFUTED_EXACTLY",
    "compactCutoffQuadraticAbsorption=OPEN",
    "translatedPacketCounterexample=FUNCTIONAL_ONLY_NOT_NSE",
    "associatedPressureCounterexample=NOT_CLAIMED",
    "signedToAbsoluteCoercivity=OPEN",
    "exteriorFunctionalLocallyControlled=OPEN",
    "weightedTentCarlesonControl=OPEN",
    "suitableWeakZeroScaleEndpoint=OPEN",
    "epsilonRegularity=OPEN",
    "formalEvidenceCertificate=SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED",
    "navierStokesSimulation=NOT_RUN",
    "directNumericalSimulation=NOT_RUN",
    "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
    "dgxUsed=false",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN",
    "clayConclusion=OPEN",
    "NOT CLAY",
  ]) assert.ok(compact.includes(token), token);

  const figureStates = [
    "formalFigurePackage=PENDING_REQUIRED",
    "formalFigurePackage=SEALED_COMMIT_BOUND",
  ].filter((token) => compact.includes(token));
  assert.equal(figureStates.length, 1, "exactly one formal-figure ledger state");

  for (const forbidden of [
    "positiveScaleAbsoluteSize=SMALL",
    "compactCutoffQuadraticAbsorption=CLOSED",
    "signedToAbsoluteCoercivity=CLOSED",
    "exteriorFunctionalLocallyControlled=CLOSED",
    "weightedTentCarlesonControl=CLOSED",
    "suitableWeakZeroScaleEndpoint=CLOSED",
    "epsilonRegularity=CLOSED",
    "translatedPacketCounterexample=NSE",
    "associatedPressureCounterexample=PROVED",
    "arbitraryThreeDimensionalGlobalRegularity=SOLVED",
    "clayConclusion=SOLVED",
  ]) assert.equal(compact.includes(forbidden), false, forbidden);

  assert.match(compact, /p\s*=\s*(?:mu|\\mu)\s*=\s*0|p=mu=0/iu);
  assert.match(compact, /static|静态/iu);
  assert.match(compact, /not\s+(?:an?\s+)?NSE|不是\s*NSE|通常不是\s*NSE/iu);
});

test("the formal-evidence archive is exactly 16 source-bound/hash-sealed files", () => {
  if (!regular(`${certificateBase}/manifest.json`)) {
    const dry = sourceDryRun();
    assert.equal(dry.published, false);
    assert.match(dry.certificate.pending ?? "", /certificate.*missing/i);
    return;
  }

  const manifest = json(`${certificateBase}/manifest.json`);
  const checklist = json(`${certificateBase}/audit-checklist.json`);
  assert.equal(manifest.schemaVersion, "r073x-formal-evidence-manifest-v1");
  assert.equal(manifest.release, "R0.73X");
  assert.equal(manifest.status, "SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED");
  assert.equal(manifest.sourceCommit, sourceCommit);
  assert.deepEqual(manifest.inventory, {
    archiveEvidenceFiles: 7,
    boundFileCount: 14,
    packageFileCount: 16,
    sha256SumsLineCount: 15,
  });
  assert.equal(manifest.scope.compactCutoffAbsorption, "OPEN");
  assert.equal(manifest.scope.weightedTentCarleson, "OPEN");
  assert.equal(manifest.scope.epsilonRegularity, "OPEN");
  assert.equal(manifest.scope.globalRegularity, "OPEN");
  assert.equal(manifest.scope.clayConclusion, "OPEN");
  assert.equal(manifest.scope.navierStokesSimulation, false);
  assert.equal(manifest.scope.notClay, true);
  assert.equal(manifest.scope.dgxUsed, false);
  assert.equal(manifest.scope.ordinaryTranslationPath, "LOCAL_DIRECT_NO_DGX");
  assertHashInventory(certificateBase, certificateNames, manifest);
  assert.equal(sums(certificateBase).size, 15);

  assert.equal(checklist.schemaVersion, "r073x-formal-evidence-audit-v1");
  assert.equal(checklist.required.gaussianOverall, "PASS");
  assert.equal(checklist.required.fourierHarmonicAbsorption, "REFUTED_EXACTLY");
  assert.match(checklist.required.fourierCompactCutoff, /^OPEN/);
  assert.equal(checklist.required.fourierNavierStokesSimulation, false);
  assert.equal(checklist.required.clayConclusion, "OPEN");
  assert.equal(checklist.required.notClay, true);

  assert.equal(Array.isArray(manifest.sourceBindings), true);
  assert.equal(manifest.sourceBindings.length, manifest.inventory.archiveEvidenceFiles);
  for (const row of manifest.sourceBindings) {
    assert.match(row.canonicalPath, /^(research|scripts)\/r073x_/);
    assert.match(row.gitBlobObjectId, /^[0-9a-f]{40}$/);
    assert.equal(sha256(bytes(`${certificateBase}/${row.archive}`)), row.sha256, row.archive);
  }

  assert.equal(typeof manifest.packageCommitBound, "boolean");
  if (manifest.packageCommitBound) {
    assert.match(manifest.packageCommit, /^[0-9a-f]{40}$/);
  } else {
    assert.match(manifest.packageCommitBoundary ?? "", /must commit|before.*package-commit-bound/i);
  }
});

test("the exterior-tail figure has the exact 10+11+4 lifecycle and 25-file package", () => {
  if (!regular(`${figureBase}/manifest.json`)) {
    const dry = sourceDryRun();
    assert.equal(dry.published, false);
    assert.equal(dry.figure.formal, false);
    assert.match(dry.figure.pending ?? "", /figure.*missing/i);
    return;
  }

  const manifest = json(`${figureBase}/manifest.json`);
  const contract = json(`${figureBase}/contract.json`);
  const results = json(`${figureBase}/results.json`);
  const validation = json(`${figureBase}/validation.json`);
  const effectiveManifestSchema = manifest.figureSchemaVersion ?? manifest.schemaVersion;

  assert.equal(figureSourceNames.length, 10);
  assert.equal(figureRawNames.length, 11);
  assert.equal(figureMetadataNames.length, 4);
  assert.equal(figureNames.length, 25);
  assert.equal(effectiveManifestSchema, "r073x-exterior-tail-ledger-manifest-v1");
  assert.equal(contract.schemaVersion, "r073x-exterior-tail-ledger-contract-v1");
  assert.equal(results.schemaVersion, "r073x-exterior-tail-ledger-results-v1");
  assert.equal(validation.schemaVersion, "r073x-exterior-tail-ledger-validation-v1");
  assert.equal(manifest.figureId, figureId);
  assert.equal(contract.figureId, figureId);
  assert.equal(contract.release, "R0.73X");
  assert.deepEqual(readdirSync(resolve(root, figureBase)).sort(), figureNames);
  assert.equal(figureNames.some(conflictCopy), false);
  assert.equal(sums(figureBase).size, 24);
  for (const [name, digest] of sums(figureBase)) {
    assert.equal(sha256(bytes(`${figureBase}/${name}`)), digest, name);
  }

  const checks = validation.checks;
  const required = validation.required ?? validation.checksRequired ?? validation.checkCount;
  const passed = validation.passed ?? validation.checksPassed ??
    (validation.allChecksPass ? required : undefined);
  assert.equal(validation.status ?? (validation.allChecksPass ? "PASS" : "FAIL"), "PASS");
  assert.ok(Number.isInteger(required) && required > 0);
  assert.equal(passed, required);
  assert.equal(checks.length, required);
  assert.ok(checks.every((row) => row.pass === true));
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.ownerVisualQaStatus ?? "PASS", "PASS");

  const panelRows = Object.values(results.panelRowCounts);
  assert.ok(panelRows.length >= 3);
  assert.ok(panelRows.every((value) => Number.isInteger(value) && value > 0));
  assert.equal(panelRows.reduce((sum, value) => sum + value, 0), results.sourceDataRows);
  assert.equal(results.scope.navierStokesSimulation, false);
  assert.equal(results.scope.dns, false);
  assert.equal(results.scope.associatedPressureCounterexample, false);
  assert.equal(results.scope.notClay, true);
  assert.equal(results.scope.dgxUsed, false);
  assert.equal(results.scope.ordinaryTranslationPath, "LOCAL_DIRECT_NO_DGX");
  assert.deepEqual(contract.claimBoundary, manifest.claimBoundary);
  for (const key of [
    "panelBRowsInterchangeable", "associatedPressureCounterexample",
    "navierStokesSimulation", "dns", "fittedScalingLaw",
    "compactCutoffAbsorptionResolved", "epsilonRegularity",
    "globalRegularity", "clayProblemSolved",
  ]) assert.equal(contract.claimBoundary[key], false, key);
  assert.equal(contract.claimBoundary.notClay, true);

  const seal = manifest.seal ?? {};
  const final = manifest.status === "formal" && manifest.publicationStatus === "staged" &&
    seal.figureSourceCommitAssigned === true &&
    seal.requiresParentFigureSourceCommitFinalReseal === false;
  if (final) {
    const bindings = seal.figureSourceBindings;
    assert.ok(Array.isArray(bindings));
    const expected = new Set(
      [...figureSourceNames, ...figureRawNames].map((name) => `${figureBase}/${name}`),
    );
    const observed = new Set(bindings.map((row) =>
      row.path.includes("/") ? row.path : `${figureBase}/${row.path}`));
    assert.equal(observed.size, bindings.length);
    assert.deepEqual(observed, expected);
    assert.equal(bindings.length, figureSourceNames.length + figureRawNames.length);
    for (const row of bindings) {
      const relative = row.path.includes("/") ? row.path : `${figureBase}/${row.path}`;
      const payload = bytes(relative);
      assert.equal(row.bytes, payload.length, relative);
      assert.equal(row.sha256, sha256(payload), relative);
      assert.match(row.gitBlobObjectId, /^[0-9a-f]{40}$/);
    }
  } else {
    const dry = sourceDryRun();
    assert.equal(dry.published, false);
    assert.equal(dry.figure.formal, false);
    assert.match(dry.figure.pending ?? "", /pending|seal|immutable/i);
  }
});

test("all R0.73X scopes reject arbitrary numeric conflict-copy suffixes", () => {
  for (const relative of canonicalPaths) assert.equal(conflictCopy(relative), false);
  for (const directory of [certificateBase, figureBase]) {
    if (!existsSync(resolve(root, directory))) continue;
    assert.equal(readdirSync(resolve(root, directory)).some(conflictCopy), false, directory);
  }
  for (const directory of ["scripts", "tests", "research"]) {
    const bad = readdirSync(resolve(root, directory))
      .filter((name) => /r073x/i.test(name) && conflictCopy(name));
    assert.deepEqual(bad, [], directory);
  }
});
