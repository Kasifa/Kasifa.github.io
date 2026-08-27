import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certRoot = resolve(root, "research/certificates/r072i");
const figureRoot = resolve(
  root,
  "figures/r072i-physical-absorption/fig-r072i-physical-absorption",
);
const publicRoot = resolve(root, "public");

async function readJson(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

async function readNdjson(path) {
  return (await readFile(path, "utf8"))
    .trim()
    .split("\n")
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

function near(actual, expected, tolerance, label) {
  assert.ok(
    Math.abs(Number(actual) - expected) <= tolerance,
    `${label}: ${actual} versus ${expected}`,
  );
}

function relativeError(left, right) {
  return Math.abs(left - right) / Math.max(Math.abs(left), Math.abs(right));
}

async function verifyHashLedger(directory, minimumRows) {
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trim()
    .split("\n");
  assert.ok(rows.length >= minimumRows);
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/]+)$/);
    assert.ok(match, row);
    const [, expected, name] = match;
    names.push(name);
    assert.equal(sha256(await readFile(resolve(directory, name))), expected, name);
  }
  assert.equal(new Set(names).size, names.length);
  return names;
}

test("separates the termwise no-go from decay of the true all-odd ledger", async () => {
  const [report, gapMatrix, literature, audit] = await Promise.all([
    readFile(resolve(root, "research/r072i_report-source.md"), "utf8"),
    readFile(resolve(root, "research/r072i_gap_matrix.md"), "utf8"),
    readFile(resolve(root, "research/r072i_literature_audit.md"), "utf8"),
    readFile(resolve(root, "research/r072i_independent_audit.md"), "utf8"),
  ]);

  assert.match(report, /physical absorption test and an odd-carrier repair/i);
  assert.match(report, /fixed positive-term estimate[\s\S]{0,100}cannot be closed by termwise/i);
  assert.ok(report.includes(String.raw`\frac{\widehat T_{B,M}}`));
  assert.ok(report.includes(String.raw`M^{1/2}\log M\longrightarrow\infty`));
  assert.match(report, /does \*\*not\*\* make the true root ledger large/i);
  assert.match(report, /all-odd family is not a counterexample/i);

  assert.ok(report.includes(String.raw`G_{{\rm all},M}^{\rm ex}\asymp M^2`));
  assert.ok(
    report.includes(String.raw`\mathcal J_{{\rm all},M}\asymp\frac{g_M^2}{M}`),
  );
  assert.ok(report.includes(String.raw`M^{-4/9}(\log M)^{-2/3}`));
  assert.match(report, /converges to zero uniformly/i);
  assert.match(report, /joint interaction exposure|interaction-exposure/i);
  assert.match(report, /odd-carrier parity lemma/i);
  assert.ok(report.includes(String.raw`b:=P_0V_M^2F_M=P_0V_M^2F_{\rm e}`));
  assert.ok(report.includes(String.raw`\|F_{\rm e}(x)\|_2`));

  assert.match(gapMatrix, /I2[\s\S]*\*\*rejected\*\*[\s\S]*M\^\{1\/2\}\\log M/i);
  assert.match(gapMatrix, /I9[\s\S]*\*\*no\*\*[\s\S]*normalized ratio/i);
  assert.match(gapMatrix, /I10[\s\S]*\*\*proved\*\*[\s\S]*convergence to zero/i);
  assert.match(gapMatrix, /large positive upper-bound term is not a lower bound/i);
  assert.match(gapMatrix, /mixed-parity family/i);

  assert.match(literature, /bounded primary-source non-collision audit/i);
  assert.match(
    literature,
    /did not find a theorem[\s\S]{0,100}directly gives either of the two R0\.72I conclusions/i,
  );
  assert.match(literature, /does not exhaust the Navier--Stokes literature/i);
  assert.match(audit, /producer and independent finite routes both pass/i);
  assert.match(audit, /do not prove the analytic theorem/i);
  assert.match(audit, /not the growing separated bound/i);

  for (const text of [report, gapMatrix, literature, audit]) {
    assert.doesNotMatch(text, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
  }
  assert.match(report, /not\s+a theorem for general three-dimensional/i);
  assert.match(report, /does\s+not resolve the Millennium problem/i);
  assert.doesNotMatch(report, /Millennium problem (?:is )?(?:solved|resolved)/i);
});

test("keeps independent passing finite routes and their cross-route errors", async () => {
  const [
    producer,
    independent,
    config,
    independentConfig,
    producerScript,
    independentScript,
    producerProgress,
    independentProgress,
    producerResource,
    independentResource,
  ] = await Promise.all([
    readJson(resolve(certRoot, "result.json")),
    readJson(resolve(certRoot, "independent-result.json")),
    readJson(resolve(certRoot, "config.json")),
    readJson(resolve(certRoot, "independent-config.json")),
    readFile(resolve(root, "research/r072i_exact_audit.py"), "utf8"),
    readFile(resolve(root, "research/r072i_independent_audit.py"), "utf8"),
    readNdjson(resolve(certRoot, "producer-progress.ndjson")),
    readNdjson(resolve(certRoot, "independent-progress.ndjson")),
    readNdjson(resolve(certRoot, "producer-resource.ndjson")),
    readNdjson(resolve(certRoot, "independent-resource.ndjson")),
  ]);

  assert.equal(producer.schemaVersion, 1);
  assert.equal(producer.audit, "R0.72I parity-resolved producer");
  assert.equal(producer.status, "passed");
  assert.ok(Object.values(producer.checks).every(Boolean));
  assert.match(producer.config.solver, /DOP853/);
  assert.match(producer.config.quadrature, /Simpson after y=z\^3/);
  assert.match(producer.config.signGenerator, /polynomial recurrence/i);

  assert.equal(independent.schemaVersion, 1);
  assert.equal(independent.audit, "R0.72I independent odd-parity absorption audit");
  assert.equal(independent.status, "passed");
  assert.ok(Object.values(independent.checks).every(Boolean));
  assert.match(independent.config.solver, /RK45/);
  assert.match(independent.config.quadrature, /Gauss-Legendre after y=z\^3/);
  assert.match(independent.config.signGenerator, /binary 11/i);
  assert.equal(independent.config.producerImported, false);

  const producerM = [4, 8, 16, 32, 64, 128];
  const commonM = [4, 8, 16, 32, 64];
  assert.deepEqual(config.mValues, producerM);
  assert.deepEqual(independentConfig.mValues, commonM);
  assert.deepEqual(producer.cases.map((row) => row.M), producerM);
  assert.deepEqual(independent.cases.map((row) => row.M), commonM);
  for (const row of [...producer.cases, ...independent.cases]) {
    assert.equal(row.carrierMin % 2, 1);
    assert.equal(row.carrierMax % 2, 1);
    assert.equal(row.algebraicRootResidual, 0);
    assert.ok(row.evolvedRootResidual < 2e-14);
  }

  const producerLargest = producer.cases.at(-1);
  assert.equal(producerLargest.M, 128);
  near(producerLargest.criticalQ, 99.8823169732, 1e-9, "producer Q* at M=128");
  near(
    producerLargest.deltaIntegralAbsHB,
    0.3880135382,
    1e-10,
    "producer cubic exposure at M=128",
  );
  near(producerLargest.ratioGenericB, 8.698257692, 1e-9, "generic B ratio");
  near(
    producerLargest.measuredBvLiftedRatio,
    0.0035631519,
    1e-10,
    "parity-resolved BV ratio",
  );
  assert.ok(producerLargest.genericBToMeasuredHB > 2.06e8);
  assert.ok(producerLargest.evolvedRootResidual < 7e-17);

  const independentLargest = independent.cases.at(-1);
  assert.equal(independentLargest.M, 64);
  near(independentLargest.criticalAction, 57.3302314413, 1e-9, "independent Q*");
  near(
    independentLargest.deltaAbsHbIntegral,
    0.1646408965,
    1e-10,
    "independent cubic exposure",
  );
  near(independentLargest.mixedRow, 4095.7772686, 1e-8, "independent mixed row");
  near(independentLargest.rootH, 68.00844164, 1e-8, "independent root slope");
  near(
    independentLargest.liftedGenericBRatio,
    5.555618885,
    1e-9,
    "independent generic B ratio",
  );
  near(
    independentLargest.liftedMeasuredCubicRatio,
    1.126936291e-7,
    1e-15,
    "independent measured cubic ratio",
  );

  const producerByM = new Map(producer.cases.map((row) => [row.M, row]));
  const crossErrors = {
    critical: 0,
    cubic: 0,
    genericRatio: 0,
    mixed: 0,
    root: 0,
  };
  for (const row of independent.cases) {
    const reference = producerByM.get(row.M);
    assert.ok(reference, `producer row M=${row.M}`);
    near(
      row.physicalCriticalAction,
      row.theta * row.criticalAction,
      1e-14,
      `canonical Gamma-normalization at M=${row.M}`,
    );
    near(
      row.lambdaStarProxy,
      1 + row.physicalCriticalAction,
      1e-14,
      `lambda proxy at M=${row.M}`,
    );
    crossErrors.critical = Math.max(
      crossErrors.critical,
      relativeError(reference.criticalQ, row.criticalAction),
    );
    crossErrors.cubic = Math.max(
      crossErrors.cubic,
      relativeError(reference.deltaIntegralAbsHB, row.deltaAbsHbIntegral),
    );
    crossErrors.genericRatio = Math.max(
      crossErrors.genericRatio,
      relativeError(reference.ratioGenericB, row.liftedGenericBRatio),
    );
    crossErrors.mixed = Math.max(
      crossErrors.mixed,
      relativeError(reference.mixedRow, row.mixedRow),
    );
    crossErrors.root = Math.max(
      crossErrors.root,
      relativeError(reference.rootH, row.rootH),
    );
  }
  assert.ok(crossErrors.critical < 1.6e-6, JSON.stringify(crossErrors));
  assert.ok(crossErrors.cubic < 1.7e-4, JSON.stringify(crossErrors));
  assert.ok(crossErrors.genericRatio < 1.5e-6, JSON.stringify(crossErrors));
  assert.ok(crossErrors.mixed < 1e-9, JSON.stringify(crossErrors));
  assert.ok(crossErrors.root < 4e-9, JSON.stringify(crossErrors));

  for (const progress of [producerProgress, independentProgress]) {
    assert.equal(progress[0].event, "audit_start");
    assert.equal(progress.at(-1).event, "audit_complete");
    assert.equal(progress.at(-1).status, "passed");
  }
  assert.equal(producerResource.filter((row) => Number.isInteger(row.M)).length,
    producerM.length);
  assert.equal(independentResource.filter((row) => Number.isInteger(row.M)).length,
    commonM.length);
  assert.equal(independentResource.at(-1).event, "audit_complete");
  assert.equal(independentResource.at(-1).status, "passed");
  for (const resources of [producerResource, independentResource]) {
    const caseRows = resources.filter((row) => Number.isInteger(row.M));
    assert.ok(caseRows.every((row) => Number.isFinite(row.elapsedSeconds)));
    assert.ok(caseRows.every((row) => Number.isFinite(row.maxRssMb)));
  }

  assert.doesNotMatch(
    producerScript,
    /(?:from|import)\s+.*r072i_independent_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /(?:from|import)\s+.*r072i_exact_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /certificates\/r072i\/(?:result|producer-data)/,
  );
});

test("seals the complete R0.72I certificate package", async () => {
  const names = await verifyHashLedger(certRoot, 18);
  for (const required of [
    "README.md",
    "config.json",
    "result.json",
    "producer-data.csv",
    "producer-progress.ndjson",
    "producer-resource.ndjson",
    "independent-config.json",
    "independent-result.json",
    "independent-data.csv",
    "independent-progress.ndjson",
    "independent-resource.ndjson",
  ]) {
    assert.ok(names.includes(required), required);
  }
});

test("archives a formal 26-of-26 figure and mirrors all public formats exactly", async () => {
  const [manifest, validation, config, contract, results] = await Promise.all([
    readJson(resolve(figureRoot, "manifest.json")),
    readJson(resolve(figureRoot, "validation.json")),
    readJson(resolve(figureRoot, "config.json")),
    readJson(resolve(figureRoot, "contract.json")),
    readJson(resolve(figureRoot, "results.json")),
  ]);

  assert.equal(manifest.schemaVersion, "r072i-figure-manifest-v1");
  assert.equal(manifest.release, "R0.72I");
  assert.equal(manifest.figureId, "R0.72I-1");
  assert.equal(manifest.status, "formal");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(manifest.dataSummary.producerStatus, "passed");
  assert.equal(manifest.dataSummary.independentOverlay, true);
  assert.equal(manifest.dataSummary.largestM, 128);
  assert.equal(manifest.dataSummary.rowCount, 456);
  near(
    manifest.dataSummary.largestMGenericBRatio,
    8.698257692,
    1e-9,
    "figure generic B ratio",
  );
  assert.ok(manifest.dataSummary.largestMGenericToMeasured > 2.06e8);
  assert.match(manifest.supportedClaim, /not individually absorbed/i);
  assert.match(manifest.supportedClaim, /odd-carrier parity/i);
  assert.match(manifest.claimBoundary, /lossy factorization/i);
  assert.match(manifest.claimBoundary, /not a growing physical/i);
  assert.match(manifest.claimBoundary, /general three-dimensional/i);

  assert.equal(validation.schemaVersion, "r072i-figure-validation-v1");
  assert.equal(validation.allPassed, true);
  assert.equal(validation.requiredCount, 26);
  assert.equal(validation.passedCount, 26);
  assert.equal(validation.checks.length, 26);
  assert.ok(validation.checks.every((row) => row.passed));
  assert.deepEqual(
    validation.checks.find((row) => row.name === "panel_coverage").value,
    { A: 44, B: 11, C: 17, D: 384 },
  );

  assert.equal(config.schemaVersion, "r072i-figure-config-v1");
  assert.equal(config.figure.widthMillimetres, 177.8);
  assert.equal(config.figure.heightMillimetres, 130.0);
  assert.equal(config.figure.pngDpi, 600);
  assert.equal(contract.schemaVersion, "r072i-figure-contract-v1");
  assert.equal(contract.analyticClaims.length, 3);
  assert.equal(contract.finiteDiagnostics.length, 3);
  assert.match(contract.claimBoundary, /does not prove a continuation criterion/i);
  assert.equal(results.allRequiredSourceChecksPassed, true);
  assert.equal(results.summary.independentOverlay, true);
  assert.equal(results.summary.rowCount, 456);

  const figureLedgerNames = await verifyHashLedger(figureRoot, 28);
  for (const required of [
    "contract.json",
    "data.csv",
    "figure.pdf",
    "figure.png",
    "figure.svg",
    "manifest.json",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "qa-report.md",
    "results.json",
    "validation.json",
  ]) {
    assert.ok(figureLedgerNames.includes(required), required);
  }

  for (const asset of manifest.assets) {
    const archived = await readFile(resolve(figureRoot, asset.path));
    assert.equal(archived.length, asset.bytes, asset.path + ": byte count");
    assert.equal(sha256(archived), asset.sha256, asset.path + ": sha256");
  }
  for (const source of manifest.sourceFiles) {
    const archived = await readFile(resolve(root, source.path));
    assert.equal(sha256(archived), source.sha256, source.path + ": lineage");
  }
  for (const extension of ["pdf", "png", "svg"]) {
    const [archived, published] = await Promise.all([
      readFile(resolve(figureRoot, "figure." + extension)),
      readFile(
        resolve(publicRoot, "figures/r0-72i-physical-absorption." + extension),
      ),
    ]);
    assert.equal(Buffer.compare(archived, published), 0, extension);
  }
});
