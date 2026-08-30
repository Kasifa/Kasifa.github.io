import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const packageRoot = "research/certificates/r073m";
const run = promisify(execFile);
const bytes = (relative) => readFile(resolve(root, relative));
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));

const analyticFiles = [
  "research/r073m_problem_freeze.md",
  "research/r073m_prescribed_action_departure_proof.md",
  "research/r073m_independent_analytic_audit.md",
  "research/r073m_adversarial_audit.md",
  "research/r073m_literature_audit.md",
  "research/r073m_gap_matrix.md",
  "research/r073m_claim_source_ledger.md",
  "research/r073m_report-source.md",
  "research/r073m_numerical_protocol.md",
];

const certificateSourceFiles = [
  "research/r073m_numerical_protocol.md",
  `${packageRoot}/README.md`,
  `${packageRoot}/command.txt`,
  `${packageRoot}/config.json`,
  `${packageRoot}/requirements.txt`,
  `${packageRoot}/primary_diagnostic.py`,
  `${packageRoot}/independent_linear.py`,
  `${packageRoot}/independent_hierarchy.py`,
  `${packageRoot}/exact_identities.py`,
  `${packageRoot}/generate_certificate.py`,
  `${packageRoot}/validate_certificate.py`,
  `${packageRoot}/seal_package.py`,
];

const requiredFormalFiles = [
  "primary_results.json",
  "primary_rows.csv",
  "action_nodes.csv",
  "cutoff_convergence.csv",
  "step_convergence.csv",
  "coefficient_endpoints.npz",
  "primary_environment.json",
  "primary_progress.ndjson",
  "primary_resources.ndjson",
  "primary_manifest.json",
  "independent_linear.json",
  "independent_linear_progress.ndjson",
  "independent_linear_resources.ndjson",
  "independent_hierarchy.json",
  "independent_hierarchy_progress.ndjson",
  "independent_hierarchy_resources.ndjson",
  "exact_identities.json",
  "certificate.json",
  "validation.json",
  "manifest.json",
  "SHA256SUMS",
];

const expectedClaimBoundary = {
  finiteInviscidActionProxyComputed: true,
  finiteViscousActionComputedSeparately: true,
  finitePrescribedActionRecodingComputed: true,
  finiteABCoefficientsComputed: true,
  continuumActionCertifiedByFiniteComputation: false,
  continuumGainPrefactorCertifiedByFiniteComputation: false,
  prefactorLimitCertified: false,
  twoTermWKBCertified: false,
  uniformTaylorRadiusCertified: false,
  fourthOrderRemainderCertified: false,
  fullNonlinearNavierStokesTrajectoryComputed: false,
  finiteCutoffAgreementIsTailProof: false,
  singleFixedBackgroundLyapunovInstabilityCertified: false,
  transverseThreeDimensionalClosureCertified: false,
  finiteTimeSingularityCertified: false,
  clayProblemSolved: false,
};

const expectedLinearSentinels = [
  { cutoff: 40, viscousEpsilon: 0.001 },
  { cutoff: 40, viscousEpsilon: 0.0000625 },
  { cutoff: 48, viscousEpsilon: 0.00025 },
  { cutoff: 64, viscousEpsilon: 0.0005 },
  { cutoff: 64, viscousEpsilon: 0.0000625 },
];

const expectedHierarchySentinels = [
  { cutoff: 40, viscousEpsilon: 0.001, fastStep: 0.05 },
  { cutoff: 48, viscousEpsilon: 0.00025, fastStep: 0.05 },
  { cutoff: 64, viscousEpsilon: 0.0000625, fastStep: 0.025 },
];

const sha256 = async (relative) => createHash("sha256")
  .update(await bytes(relative)).digest("hex");

function assertFiniteTree(value, label) {
  if (typeof value === "number") {
    assert.equal(Number.isFinite(value), true, `${label} is nonfinite`);
  } else if (Array.isArray(value)) {
    value.forEach((entry, index) => assertFiniteTree(entry, `${label}[${index}]`));
  } else if (value && typeof value === "object") {
    for (const [key, entry] of Object.entries(value)) {
      assertFiniteTree(entry, `${label}.${key}`);
    }
  }
}

function assertPassed(value, label) {
  assert.equal(value.allChecksPass, true, `${label}.allChecksPass`);
  if (value.status !== undefined) assert.equal(value.status, "passed", `${label}.status`);
  if (value.smokeMode !== undefined) assert.equal(value.smokeMode, false, `${label}.smokeMode`);
  if (value.checks !== undefined) {
    assert.equal(Object.keys(value.checks).length > 0, true, `${label}.checks empty`);
    assert.equal(Object.values(value.checks).every(Boolean), true, `${label}.checks`);
  }
}

function assertExactClaimBoundary(value, label) {
  assert.deepEqual(value, expectedClaimBoundary, `${label}.claimBoundary`);
  assert.equal(Object.hasOwn(value, "Clay"), false, `${label} uses stale Clay key`);
}

function assertFormalProvenance(value, sourceCommit, label) {
  const provenance = value.sourceProvenance;
  assert.ok(provenance && typeof provenance === "object", `${label}.sourceProvenance`);
  assert.equal(provenance.enforced, true, `${label}.sourceProvenance.enforced`);
  assert.equal(provenance.allSourceBlobsMatch, true,
    `${label}.sourceProvenance.allSourceBlobsMatch`);
  assert.equal(provenance.sourceCommit, sourceCommit,
    `${label}.sourceProvenance.sourceCommit`);
}

function manifestRows(manifest) {
  assert.ok(Array.isArray(manifest.files), "manifest.files must be a flat array");
  return manifest.files;
}

function parseSha256Sums(value) {
  const rows = new Map();
  for (const [index, line] of value.trim().split("\n").entries()) {
    const match = /^([0-9a-f]{64})\s+[ *]?(.+)$/.exec(line);
    assert.ok(match, `invalid SHA256SUMS line ${index + 1}`);
    assert.equal(rows.has(match[2]), false, `duplicate SHA256SUMS path ${match[2]}`);
    rows.set(match[2], match[1]);
  }
  return rows;
}

test("R0.73M analytic contract closes exactly M1--M8 and preserves the OPEN boundary", async () => {
  const [freeze, proof, independent, adversarial, literature, gap, ledger, report,
    protocol, config] = await Promise.all([
    ...analyticFiles.map(text),
    json(`${packageRoot}/config.json`),
  ]);

  assert.match(independent, /MATHEMATICAL FINAL PASS/);
  assert.match(adversarial, /\*\*Verdict:\*\* \*\*PASS\*\*/);
  assert.match(literature, /independent source audit\s+PASS/);
  for (let index = 1; index <= 8; index += 1) {
    assert.match(gap, new RegExp(`\\| M${index} \\|[^\\n]+\\| CLOSED`), `gap M${index}`);
    assert.match(ledger, new RegExp(`\\| M${index} \\|`), `ledger M${index}`);
    assert.match(freeze, new RegExp(`\\| M${index} \\|`), `freeze M${index}`);
  }
  assert.match(ledger, /Every new\s+mathematical assertion must resolve to M1--M8/);

  const semanticRows = [
    [1, "kinetic selected gain equals the real physical-pair gain"],
    [2, "\\(G_\\Lambda^*\\asymp e^{\\Lambda\\mathcal A_*}\\)"],
    [3, "normalized selected orbit localizes with \\(\\mu_*=0.167>1/6\\)"],
    [4, "quadratic, cubic, and fourth-order remainder budgets close"],
    [5, "prescribed-action seed stays inside one uniform nonlinear radius"],
    [6, "vanishing \\(H^3\\) data reach \\(c_*\\rho\\)"],
    [7, "selected solutions are global smooth and exactly planar"],
    [8, "literature and theorem boundaries are correctly delimited"],
  ];
  for (const [index, phrase] of semanticRows) {
    const row = ledger.split("\n").find((line) => line.startsWith(`| M${index} |`));
    assert.ok(row, `missing ledger M${index}`);
    assert.ok(row.includes(phrase), `ledger M${index} semantic drift`);
  }

  for (const token of [
    "physicalKineticSelectedGainConjugacy=CLOSED",
    "prescribedActionSeedWindow=CLOSED",
    "twoDimensionalNonlinearDeparture=CLOSED",
    "fixedDistanceEndpoint=CLOSED",
    "prefactorLimit=OPEN",
    "twoTermWKB=OPEN",
    "singleFixedBackgroundLyapunovInstability=OPEN",
    "transverseThreeDimensionalClosure=OPEN",
    "finiteTimeSingularity=OPEN",
    "Clay=OPEN",
  ]) {
    assert.ok(freeze.includes(token), `freeze boundary: ${token}`);
    assert.ok(proof.includes(token), `proof boundary: ${token}`);
  }
  for (const phrase of [
    "a prefactor limit", "a two-term WKB expansion", "one fixed-background",
    "transverse 3D closure", "singularity", "Clay all remain open",
  ]) assert.ok(report.includes(phrase), `report boundary: ${phrase}`);

  for (const source of [freeze, proof, report, protocol]) {
    assert.match(source, /(?:1\/450|1\\over450)/, "D*=1/450 missing");
    assert.match(source, /(?:1\/1800|1\\over1800)/, "T*=1/1800 missing");
  }
  assert.equal(config.profileTimeEnd, 1 / 450);
  assert.equal(config.physicalTimeEnd, 1 / 1800);
  assert.equal(config.profileToPhysicalTimeRule, "d=4t");
  assert.deepEqual(config.exactRationals, {
    profileTimeEnd: "1/450", physicalTimeEnd: "1/1800", muStar: "167/1000",
    twoRateMargin: "1/1500", threeRateMargin: "1/1000", fourRateMargin: "21/125",
  });
  assertExactClaimBoundary(config.claimBoundary, "config");
});

test("R0.73M finite source contract freezes grids, fields, hashes, and fail-closed claims", async () => {
  const [config, readme, command, requirements] = await Promise.all([
    json(`${packageRoot}/config.json`), text(`${packageRoot}/README.md`),
    text(`${packageRoot}/command.txt`), text(`${packageRoot}/requirements.txt`),
  ]);
  assert.equal(config.schemaVersion, "r073m-prescribed-action-finite-config-v1");
  assert.equal(config.release, "R0.73M");
  assert.equal(config.diagnosticOnly, true);
  assert.deepEqual(config.cutoffs, [40, 48, 64]);
  assert.deepEqual(config.viscousEpsilons,
    [0.001, 0.0005, 0.00025, 0.000125, 0.0000625]);
  assert.equal(config.cutoffs.length * config.viscousEpsilons.length, 15);
  assert.deepEqual(config.independentLinear.sentinels, expectedLinearSentinels);
  assert.deepEqual(config.independentHierarchy.sentinels, expectedHierarchySentinels);
  assert.deepEqual(config.hierarchy.stepConvergence, {
    cutoff: 64,
    viscousEpsilons: [0.001, 0.0000625],
    fastSteps: [0.1, 0.05, 0.025],
  });

  const scalarPaths = config.outputSchema.caseScalars.map((row) => row.path);
  for (const path of [
    "linear.finiteInviscidActionProxy", "linear.finiteViscousAction",
    "hierarchy.actualPhysicalLinearGain", "finiteInviscidActionPrefactor",
    "hierarchy.aEndpointL2", "hierarchy.bEndpointL2",
    "hierarchy.cTargetEndpointL2", "hierarchy.cTotalSignedParallel",
  ]) assert.ok(scalarPaths.includes(path), `output schema ${path}`);
  assert.notEqual(scalarPaths.indexOf("linear.finiteInviscidActionProxy"),
    scalarPaths.indexOf("linear.finiteViscousAction"));
  assert.deepEqual(config.outputSchema.coefficientArchive.stateOrder,
    ["V1", "V2_Kz0", "V2_KzPlusMinus2", "V3_via_Kz0", "V3_via_KzPlusMinus2"]);
  assert.match(config.outputSchema.caseScalars.find(
    (row) => row.path === "hierarchy.aEndpointL2").normalization,
  /V1\/G/);
  assert.match(config.outputSchema.caseScalars.find(
    (row) => row.path === "hierarchy.bEndpointL2").normalization,
  /V2\/G\^2/);
  assert.match(config.outputSchema.caseScalars.find(
    (row) => row.path === "hierarchy.cTargetEndpointL2").normalization,
  /V3\/G\^3/);
  assertExactClaimBoundary(config.claimBoundary, "config");

  assert.match(readme, /protocol `research\/r073m_numerical_protocol\.md` is part of `SOURCE_FILES`/);
  assert.match(command, /R073M_SMOKE_DIR=\$\(mktemp -d \/tmp\/r073m-smoke\.XXXXXX\)/);
  assert.match(command, /--source-commit SOURCE_COMMIT/);
  assert.deepEqual(requirements.trim().split("\n"), ["numpy==2.5.2", "scipy==1.16.1"]);

  assert.equal(config.upstreamBindings.length, 6);
  for (const binding of config.upstreamBindings) {
    assert.match(binding.sha256, /^[0-9a-f]{64}$/);
    assert.equal(await sha256(binding.path), binding.sha256, binding.path);
  }
});

test("R0.73M formal finite package is sealed, source-bound, independently checked, and finite-only", async () => {
  // Missing output is an intentional release-stopping failure, not a skip.
  await Promise.all(requiredFormalFiles.map((name) => bytes(`${packageRoot}/${name}`)));
  const [config, primary, independentLinear, independentHierarchy, exact,
    certificate, validation, manifest, sumsText] = await Promise.all([
    json(`${packageRoot}/config.json`),
    json(`${packageRoot}/primary_results.json`),
    json(`${packageRoot}/independent_linear.json`),
    json(`${packageRoot}/independent_hierarchy.json`),
    json(`${packageRoot}/exact_identities.json`),
    json(`${packageRoot}/certificate.json`),
    json(`${packageRoot}/validation.json`),
    json(`${packageRoot}/manifest.json`),
    text(`${packageRoot}/SHA256SUMS`),
  ]);

  assert.equal(primary.schemaVersion, "r073m-primary-finite-diagnostic-v1");
  assert.equal(independentLinear.schemaVersion, "r073m-independent-linear-action-v1");
  assert.equal(independentHierarchy.schemaVersion, "r073m-independent-vorticity-fft-v1");
  assert.equal(exact.schemaVersion, "r073m-exact-rational-identities-v1");
  for (const [label, value] of [
    ["primary", primary], ["independentLinear", independentLinear],
    ["independentHierarchy", independentHierarchy], ["exact", exact],
    ["certificate", certificate], ["validation", validation],
  ]) assertPassed(value, label);

  assert.equal(manifest.release, "R0.73M");
  assert.equal(manifest.schemaVersion, "r073m-sealed-package-manifest-v1");
  assert.equal(manifest.allPrerequisiteChecksPass, true);
  assertExactClaimBoundary(config.claimBoundary, "config");
  for (const [label, value] of [
    ["primary", primary], ["independentLinear", independentLinear],
    ["independentHierarchy", independentHierarchy], ["exact", exact],
    ["certificate", certificate], ["manifest", manifest],
  ]) assertExactClaimBoundary(value.claimBoundary, label);

  assert.equal(primary.caseCount, 15);
  assert.equal(primary.cases.length, 15);
  const expectedCases = new Set(config.cutoffs.flatMap((cutoff) =>
    config.viscousEpsilons.map((epsilon) => `${cutoff}:${epsilon}`)));
  const actualCases = new Set(primary.cases.map((row) => `${row.N}:${row.epsilon}`));
  assert.deepEqual(actualCases, expectedCases);
  assertFiniteTree(primary.cases, "primary.cases");
  for (const row of primary.cases) {
    assert.equal(row.profileTimeEnd, 1 / 450);
    assert.equal(row.physicalTimeEnd, 1 / 1800);
    assert.equal(row.profileToPhysicalTimeRule, "d=4t");
    assert.equal(Object.hasOwn(row.linear, "finiteInviscidActionProxy"), true);
    assert.equal(Object.hasOwn(row.linear, "finiteViscousAction"), true);
    assert.notEqual(row.linear.finiteInviscidActionProxy, row.linear.finiteViscousAction,
      `actions conflated at ${row.N}:${row.epsilon}`);
    const gain = row.hierarchy.actualPhysicalLinearGain;
    assert.equal(Number.isFinite(gain) && gain > 0, true);
    const expectedPrefactor = gain * Math.exp(
      -row.linear.finiteInviscidActionProxy / row.epsilon,
    );
    assert.ok(Math.abs(row.finiteInviscidActionPrefactor - expectedPrefactor)
      <= 1e-12 * Math.max(1, Math.abs(expectedPrefactor)));
    assert.deepEqual(row.normalization, {
      a: "V1/actualPhysicalLinearGain",
      b: "V2/actualPhysicalLinearGain^2",
      c: "V3/actualPhysicalLinearGain^3",
    });
    assert.ok(Math.abs(row.hierarchy.aEndpointL2 - 1)
      <= config.tolerances.aEndpointNormalizationAbsolute);
    for (const diagnostic of row.thirdOrderTargetDiagnostics) {
      assert.equal(diagnostic.diagnosticOnly, true);
      assert.equal(diagnostic.visualizationChoiceIsCertifiedContinuumTaylorRadius, false);
      assert.equal(diagnostic.fullNonlinearTrajectoryComputed, false);
    }
  }

  assert.deepEqual(independentLinear.sentinels, expectedLinearSentinels);
  assert.equal(independentLinear.validations.length, 5);
  assert.equal(independentLinear.method.importsPrimaryProducer, false);
  assert.deepEqual(independentHierarchy.sentinels, expectedHierarchySentinels);
  assert.equal(independentHierarchy.validations.length, 3);
  assert.equal(independentHierarchy.method.importsPrimaryProducer, false);
  assertFiniteTree(independentLinear.validations, "independentLinear.validations");
  assertFiniteTree(independentHierarchy.validations, "independentHierarchy.validations");

  assert.equal(exact.arithmetic,
    "fractions.Fraction; no floating-point identity reconstruction");
  assert.equal(exact.checks.allFractionIdentitiesExact, true);
  assert.equal(exact.checks.configuredExactRationalsMatchIndependentFractions, true);
  assert.equal(exact.checks.configuredRuleIsDEqualsFourT, true);
  assert.equal(exact.checks.claimBoundaryExact, true);

  const sourceCommit = manifest.sourceCommit;
  assert.match(sourceCommit, /^[0-9a-f]{40}$/);
  await run("git", ["cat-file", "-e", `${sourceCommit}^{commit}`], { cwd: root });
  for (const relative of certificateSourceFiles) {
    const frozen = await run("git", ["show", `${sourceCommit}:${relative}`], {
      cwd: root, encoding: "buffer", maxBuffer: 32 * 1024 * 1024,
    });
    assert.deepEqual(await bytes(relative), frozen.stdout, relative);
  }
  for (const [label, value] of [
    ["primary", primary], ["independentLinear", independentLinear],
    ["independentHierarchy", independentHierarchy], ["exact", exact],
  ]) assertFormalProvenance(value, sourceCommit, label);

  const rows = manifestRows(manifest);
  const manifested = new Map(rows.map((row) => [row.path, row]));
  const sums = parseSha256Sums(sumsText);
  for (const name of requiredFormalFiles.filter(
    (entry) => !["manifest.json", "SHA256SUMS"].includes(entry))) {
    assert.equal(manifested.has(name), true, `manifest omits ${name}`);
    assert.equal(sums.has(name), true, `SHA256SUMS omits ${name}`);
    const digest = await sha256(`${packageRoot}/${name}`);
    assert.equal(manifested.get(name).sha256, digest, `manifest hash ${name}`);
    assert.equal(sums.get(name), digest, `SHA256SUMS hash ${name}`);
  }

  const serialized = JSON.stringify({ primary, independentLinear, independentHierarchy,
    exact, certificate, validation, manifest });
  assert.doesNotMatch(serialized, /"(?:Clay|clayProblemSolved)"\s*:\s*true/);
  assert.doesNotMatch(serialized,
    /"(?:fullNonlinearNavierStokesTrajectoryComputed|finiteTimeSingularityCertified)"\s*:\s*true/);
});
