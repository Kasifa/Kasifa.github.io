import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certRoot = resolve(root, "research/certificates/r072h");
const figureRoot = resolve(
  root,
  "figures/r072h-mixed-row-payment/fig-r072h-mixed-row-payment",
);
const publicRoot = resolve(root, "public");

async function readJson(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

async function readNdjson(path) {
  return (await readFile(path, "utf8"))
    .trim()
    .split("\n")
    .map((line) => JSON.parse(line));
}

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

test("proves a carrier-count-independent mixed-row theorem with its strict boundary", async () => {
  const [report, gapMatrix, literature, audit] = await Promise.all([
    readFile(resolve(root, "research/r072h_report-source.md"), "utf8"),
    readFile(resolve(root, "research/r072h_gap_matrix.md"), "utf8"),
    readFile(resolve(root, "research/r072h_literature_audit.md"), "utf8"),
    readFile(resolve(root, "research/r072h_independent_audit.md"), "utf8"),
  ]);

  assert.match(report, /carrier-free critical-log payment of the mixed target row/i);
  assert.ok(report.includes(String.raw`\mathcal E_Q(I)`));
  assert.ok(report.includes(String.raw`Q=P_0[V_w'+V_w(D_q+\lambda_0)]`));
  assert.ok(report.includes(String.raw`|h|^2\le\lambda_0\mathfrak q`));
  assert.ok(report.includes(String.raw`6\sqrt{2\nu}\,d|K_z|`));
  assert.ok(report.includes(String.raw`m_*(A,X)`));
  assert.ok(report.includes(String.raw`6\sqrt{\nu}\,d|K_z|`));
  assert.match(
    report,
    /independent of the carrier count,\s*carrier\s*locations, and physical shear phases/i,
  );
  assert.ok(report.includes(String.raw`m_*(A,X)\le`));
  assert.ok(report.includes(String.raw`K_{v,A}`));
  assert.ok(report.includes(String.raw`\mathcal E_Q(I)\le3E_A\rho_A^2`));

  assert.ok(report.includes(String.raw`\Phi(a)`));
  assert.ok(report.includes(String.raw`(\kappa X)^{-1/3}`));
  assert.ok(report.includes(String.raw`r_j=2M+2j+1`));
  assert.match(report, /all-odd Rudin--Shapiro/i);
  assert.ok(report.includes(String.raw`\mathcal E_Q\asymp a^2M^2`));
  assert.ok(report.includes(String.raw`Q_*^I\asymp a^2M^{2/3}\log M`));
  assert.ok(report.includes(String.raw`m_*(0,X)\asymp\frac{a^2M^{7/3}}{\log M}`));
  assert.ok(report.includes(String.raw`\frac{\mathcal E_Q}{Q_*^I}`));
  assert.match(report, /action-only payment is false/i);
  assert.ok(report.includes(String.raw`sharp in powers of \(M\)`));

  assert.ok(report.includes(String.raw`\tau_M=M^{-3}`));
  assert.ok(report.includes(String.raw`\zeta_M\in\mathbb R`));
  assert.ok(report.includes(String.raw`P_0F_M(\tau_M)=0`));
  assert.ok(report.includes(String.raw`G_{\rm all}^{\rm ex}(I)`));
  assert.ok(report.includes(String.raw`B_AQ_*^I`));
  assert.match(
    report,
    /assume in addition that[\s\S]*chosen target sector has a real gauge/i,
  );
  assert.ok(report.includes(String.raw`\(\delta\ne0\)`));
  assert.match(report, /division by[\s\S]{0,40}is essential in the Rolle step/i);
  assert.match(report, /At[\s\S]{0,24}the physical slope ledger\s*vanishes/i);
  assert.match(report, /not asserted for an arbitrary complex target coordinate/i);

  assert.match(gapMatrix, /H4[\s\S]*proved[\s\S]*carrier count, carrier locations, and physical phases/i);
  assert.match(gapMatrix, /H7[\s\S]*rejected[\s\S]*action-only estimate/i);
  assert.match(gapMatrix, /H10[\s\S]*rejected as stated/i);
  assert.ok(gapMatrix.includes(String.raw`\(\delta\ne0\)`));
  assert.match(gapMatrix, /H11[\s\S]*proved at the abstract row level/i);
  assert.match(gapMatrix, /physical absorption problem/i);

  assert.match(literature, /bounded primary-source search|bounded non-collision/i);
  assert.match(literature, /Kato--Ponce|Kato and Ponce/i);
  assert.match(literature, /Haak[^\n]{0,30}Ouhabaz/i);
  assert.match(literature, /Trostorff[^\n]{0,30}Waurick/i);
  assert.match(literature, /Nazarov--Pisier--Treil--Volberg|Nazarov.*Pisier.*Treil.*Volberg/i);
  assert.match(literature, /not a claim of priority|not.*priority/i);
  assert.match(audit, /producer and independent routes pass/i);
  assert.match(audit, /do not prove the\s*analytic theorem/i);

  for (const text of [report, gapMatrix, literature, audit]) {
    assert.doesNotMatch(text, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
  }
  assert.match(report, /not a theorem for general[\s\S]*Navier--Stokes solutions/i);
  assert.ok(
    report.includes(String.raw`does not refute \(D^{1/3}\Lambda_{1,*}\)`),
  );
  assert.doesNotMatch(report, /Millennium problem (?:is )?(?:solved|resolved)/i);
});

test("keeps independent finite solvers, exact roots, and both failed producer attempts", async () => {
  const [producer, independent, failedOne, config, independentConfig,
    producerScript, independentScript, producerProgress, independentProgress,
    failedOneProgress, failedTwoProgress, producerResource, independentResource] =
    await Promise.all([
      readJson(resolve(certRoot, "result.json")),
      readJson(resolve(certRoot, "independent-result.json")),
      readJson(resolve(certRoot, "producer-attempt1-failed-result.json")),
      readJson(resolve(certRoot, "config.json")),
      readJson(resolve(certRoot, "independent-config.json")),
      readFile(resolve(root, "research/r072h_exact_audit.py"), "utf8"),
      readFile(resolve(root, "research/r072h_independent_audit.py"), "utf8"),
      readNdjson(resolve(certRoot, "producer-progress.ndjson")),
      readNdjson(resolve(certRoot, "independent-progress.ndjson")),
      readNdjson(resolve(certRoot, "producer-attempt1-failed-progress.ndjson")),
      readNdjson(resolve(certRoot, "producer-attempt2-failed-progress.ndjson")),
      readNdjson(resolve(certRoot, "producer-resource.ndjson")),
      readNdjson(resolve(certRoot, "independent-resource.ndjson")),
    ]);

  assert.equal(producer.schemaVersion, 1);
  assert.equal(producer.audit, "R0.72H producer");
  assert.equal(producer.status, "passed");
  assert.ok(Object.values(producer.checks).every(Boolean));
  assert.match(producer.config.solver, /DOP853/);
  assert.match(producer.config.quadrature, /Simpson after y=z\^3/);
  assert.match(producer.config.signGenerator, /polynomial recurrence/i);
  assert.equal(producer.config.truncationFactor, 8);

  assert.equal(independent.schemaVersion, 1);
  assert.equal(independent.audit, "R0.72H independent");
  assert.equal(independent.status, "passed");
  assert.ok(Object.values(independent.checks).every(Boolean));
  assert.match(independent.config.solver, /real-gauge SciPy RK45/);
  assert.match(independent.config.quadrature, /Gauss-Legendre after y=z\^3/);
  assert.match(independent.config.signGenerator, /binary parity/i);
  assert.equal(independent.config.truncationFactor, 9);

  const mValues = [4, 8, 16, 32, 64];
  assert.deepEqual(config.mValues, mValues);
  assert.deepEqual(independentConfig.mValues, mValues);
  assert.deepEqual(producer.cases.map((row) => row.M), mValues);
  assert.deepEqual(independent.cases.map((row) => row.M), mValues);
  for (const row of [...producer.cases, ...independent.cases]) {
    assert.equal(row.carrierMin % 2, 1);
    assert.equal(row.carrierMax % 2, 1);
    assert.equal(row.algebraicRootResidual, 0);
    assert.ok(row.evolvedRootResidual < 1e-14);
  }

  assert.ok(Math.abs(producer.slopes.mixedRow - 2.0011749939857157) < 1e-14);
  assert.ok(Math.abs(producer.slopes.criticalActionDivLog - 0.44265395994517215) < 1e-14);
  assert.ok(Math.abs(producer.slopes.profileMomentTimesLog - 2.52562007774597) < 1e-14);
  assert.ok(Math.abs(producer.slopes.actionOnlyTimesLog - 1.5585210340405435) < 1e-14);
  assert.ok(independent.maxProducerRelativeError < 3.31e-6);
  assert.ok(
    Math.abs(independent.maxProducerRelativeError - 3.3089545553009195e-6) < 1e-18,
  );

  const last = producer.cases.at(-1);
  assert.equal(last.M, 64);
  assert.ok(Math.abs(last.mixedRow - 4095.9421345730048) < 1e-10);
  assert.ok(Math.abs(last.mixedRowNormalized - 0.9999858726984875) < 1e-15);
  assert.ok(Math.abs(last.criticalAction - 57.331430827074875) < 1e-12);
  assert.ok(Math.abs(last.profileMoment - 2126.949653475423) < 1e-10);
  assert.ok(Math.abs(last.momentResolvedRatio - 0.6820420793555061) < 1e-15);
  assert.ok(Math.abs(last.actionOnlyScaledRatio - 1.1606406523104982) < 1e-15);
  assert.equal(last.zetaImag, 0);
  assert.ok(Math.abs(last.zetaReal + 0.0003000179408329432) < 1e-18);
  assert.ok(Math.abs(last.rootHNormalized - 1.0626348659893474) < 1e-15);

  assert.equal(failedOne.status, "failed");
  assert.ok(Object.values(failedOne.checks).some((passed) => !passed));
  assert.equal(failedOne.checks.noncollapsedRootSlope, false);
  assert.equal(failedOne.checks.profileMomentSlope, false);
  assert.equal(failedOneProgress.at(-1).event, "audit_complete");
  assert.equal(failedOneProgress.at(-1).status, "failed");
  assert.equal(failedTwoProgress.at(-1).event, "case_complete");
  assert.equal(failedTwoProgress.at(-1).M, 64);

  for (const progress of [producerProgress, independentProgress]) {
    assert.equal(progress[0].event, "audit_start");
    assert.equal(progress.at(-1).event, "audit_complete");
    assert.equal(progress.at(-1).status, "passed");
  }
  for (const resources of [producerResource, independentResource]) {
    assert.equal(resources.length, 5);
    assert.ok(resources.every((row) => Number.isFinite(row.elapsedSeconds)));
    assert.ok(resources.every((row) => Number.isFinite(row.maxRssMb)));
  }

  assert.doesNotMatch(
    producerScript,
    /(?:from|import)\s+.*r072h_independent_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /(?:from|import)\s+.*r072h_exact_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /certificates\/r072h\/(?:result|producer-data)/,
  );
});

test("seals the complete R0.72H certificate package", async () => {
  const ledger = await readFile(resolve(certRoot, "SHA256SUMS"), "utf8");
  const rows = ledger.trim().split("\n");
  assert.ok(rows.length >= 24);
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, row);
    const [, expected, relative] = match;
    const payload = await readFile(resolve(certRoot, relative));
    assert.equal(sha256(payload), expected, relative);
  }
  for (const required of [
    "result.json",
    "independent-result.json",
    "producer-attempt1-failed-result.json",
    "producer-attempt1-failed-progress.ndjson",
    "producer-attempt2-failed-progress.ndjson",
    "producer-progress.ndjson",
    "independent-progress.ndjson",
    "producer-resource.ndjson",
    "independent-resource.ndjson",
  ]) {
    assert.match(ledger, new RegExp(`  ${required.replaceAll(".", "\\.")}$`, "m"));
  }
});

test("archives a 22-of-22 formal figure and mirrors all public assets exactly", async () => {
  const [manifest, validation, config, contract, results] = await Promise.all([
    readJson(resolve(figureRoot, "manifest.json")),
    readJson(resolve(figureRoot, "validation.json")),
    readJson(resolve(figureRoot, "config.json")),
    readJson(resolve(figureRoot, "contract.json")),
    readJson(resolve(figureRoot, "results.json")),
  ]);

  assert.equal(manifest.schemaVersion, "r072h-figure-manifest-v1");
  assert.equal(manifest.release, "R0.72H");
  assert.equal(manifest.figureId, "R0.72H-1");
  assert.equal(manifest.status, "formal");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{7,40}$/);
  assert.equal(manifest.dataSummary.producerStatus, "passed");
  assert.equal(manifest.dataSummary.independentStatus, "passed");
  assert.equal(manifest.dataSummary.maxCrossRouteRelativeError,
    3.3089545553009195e-6);
  assert.equal(manifest.dataSummary.largestM, 64);
  assert.equal(manifest.dataSummary.rowCount, 129);
  assert.match(manifest.supportedClaim, /carrier-count independent/i);
  assert.match(manifest.supportedClaim, /action-only payment diverge/i);
  assert.match(manifest.claimBoundary, /finite-carrier triangular 2\.5D row problem/i);
  assert.match(manifest.claimBoundary, /does not prove a full physical critical-log estimate/i);
  assert.match(manifest.claimBoundary, /general three-dimensional Navier-Stokes regularity/i);

  assert.equal(validation.schemaVersion, "r072h-figure-validation-v1");
  assert.equal(validation.allPassed, true);
  assert.equal(validation.requiredCount, 22);
  assert.equal(validation.passedCount, 22);
  assert.equal(validation.checks.length, 22);
  assert.ok(validation.checks.every((row) => row.passed));
  assert.deepEqual(
    validation.checks.find((row) => row.name === "public_assets").value,
    { pdf: true, png: true, svg: true },
  );

  assert.equal(config.schemaVersion, "r072h-figure-config-v1");
  assert.equal(config.figure.widthMillimetres, 177.8);
  assert.equal(config.figure.heightMillimetres, 96.0);
  assert.equal(config.figure.pngDpi, 600);
  assert.equal(contract.schemaVersion, "r072h-figure-contract-v1");
  assert.equal(contract.analyticClaims.length, 3);
  assert.equal(contract.finiteDiagnostics.length, 3);
  assert.equal(results.allRequiredSourceChecksPassed, true);
  assert.equal(results.summary.rowCount, 129);
  assert.equal(results.summary.maxCrossRouteRelativeError,
    3.3089545553009195e-6);

  for (const asset of manifest.assets) {
    const archived = await readFile(resolve(figureRoot, asset.path));
    assert.equal(archived.length, asset.bytes, asset.path + ": byte count");
    assert.equal(sha256(archived), asset.sha256, asset.path + ": sha256");
  }
  for (const source of manifest.sourceFiles) {
    const archived = await readFile(resolve(root, source.path));
    assert.equal(sha256(archived), source.sha256, source.path + ": lineage");
  }
  for (const extension of ["pdf", "svg", "png"]) {
    const [archived, published] = await Promise.all([
      readFile(resolve(figureRoot, "figure." + extension)),
      readFile(resolve(
        publicRoot,
        "figures/r0-72h-mixed-row-payment." + extension,
      )),
    ]);
    assert.equal(Buffer.compare(archived, published), 0, extension);
  }
});
