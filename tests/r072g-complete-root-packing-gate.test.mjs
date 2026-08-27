import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certRoot = resolve(root, "research/certificates/r072g");
const figureRoot = resolve(
  root,
  "figures/r072g-complete-root-packing/fig-r072g-complete-root-packing",
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

test("proves the complete-root logarithmic order only in the declared one-carrier class", async () => {
  const [report, gapMatrix, audit] = await Promise.all([
    readFile(resolve(root, "research/r072g_report-source.md"), "utf8"),
    readFile(resolve(root, "research/r072g_gap_matrix.md"), "utf8"),
    readFile(resolve(root, "research/r072g_independent_audit.md"), "utf8"),
  ]);

  assert.match(report, /complete-root packing on the exact one-carrier ray/);
  assert.ok(report.includes(String.raw`fix \(\delta\ge1\)`));
  assert.ok(report.includes(String.raw`F(0)=ie_{-1}`));
  assert.ok(report.includes(String.raw`f'+\mu f=\delta h`));
  assert.ok(report.includes(String.raw`h'=-(2+\mu)h+\delta b`));
  assert.ok(report.includes(String.raw`|h|^2\le\mu q`));
  assert.ok(report.includes(String.raw`|b|^2\le2(1+\mu)q`));
  assert.match(report, /Rolle--BV sampling of every root/);
  assert.match(report, /monotone supremum over finite root subsets/);
  assert.ok(report.includes(String.raw`\sum_{j=1}^N|h(x_j)|^2`));
  assert.ok(report.includes(String.raw`\le2\int_0^X|h(x)h'(x)|`));
  assert.ok(report.includes(String.raw`1+2\left[(2+\mu)\mu`));
  assert.ok(report.includes(String.raw`G_{\rm all}(\delta_R;X)\asymp_{X,q_0}\log\delta_R`));
  assert.ok(report.includes(String.raw`D^{1/3}\Lambda_{1,*}`));
  assert.ok(report.includes(String.raw`half-open observation window \([0,T)\)`));
  assert.match(report, /R0\.72H[\s\S]*dimension-free[\s\S]*finite real multi-carrier shear/);
  assert.ok(report.includes(String.raw`\mathcal E_Q=\int_0^X |h\,QF|`));
  assert.ok(report.includes(String.raw`Q=P_0[V'+V(D+\lambda_0)]`));

  assert.ok(audit.includes(String.raw`restriction \(\delta\ge1\) is essential`));
  assert.ok(audit.includes(String.raw`At \(\delta=0\), the target`));
  assert.match(audit, /Tangential roots[\s\S]*contribute zero slope mass/);
  assert.match(gapMatrix, /Every finite positive root subset/);
  assert.match(gapMatrix, /No root-separation assumption/);

  for (const text of [report, audit, gapMatrix]) {
    assert.doesNotMatch(text, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
  }
  assert.match(report, /not a theorem for arbitrary launch data/);
  assert.match(report, /general Navier--Stokes solutions/);
  assert.doesNotMatch(report, /Millennium problem (?:is )?(?:solved|resolved)/i);
});

test("keeps two independent finite certificates and both failed attempts", async () => {
  const [producer, independent, producerFailed, independentFailed, config,
    producerScript, independentScript, producerProgress, independentProgress,
    producerResource, independentResource] = await Promise.all([
    readJson(resolve(certRoot, "result.json")),
    readJson(resolve(certRoot, "independent-result.json")),
    readJson(resolve(certRoot, "producer-attempt1-failed-result.json")),
    readJson(resolve(certRoot, "independent-attempt1-failed-result.json")),
    readJson(resolve(certRoot, "config.json")),
    readFile(resolve(root, "research/r072g_exact_audit.py"), "utf8"),
    readFile(resolve(root, "research/r072g_independent_audit.py"), "utf8"),
    readNdjson(resolve(certRoot, "producer-progress.ndjson")),
    readNdjson(resolve(certRoot, "independent-progress.ndjson")),
    readNdjson(resolve(certRoot, "producer-resource.ndjson")),
    readNdjson(resolve(certRoot, "independent-resource.ndjson")),
  ]);

  assert.equal(producer.schemaVersion, "r072g-producer-certificate-v1");
  assert.equal(producer.auditId, "R0.72G-complete-root-producer");
  assert.equal(producer.allRequiredChecksPassed, true);
  assert.ok(producer.checks.every((row) => row.passed));
  assert.match(producer.method.evolution, /fixed-step RK4/);
  assert.match(producer.method.rootDetection, /cubic Hermite and Brent/);
  assert.equal(producer.scope.intervalArithmetic, false);
  assert.equal(producer.scope.provesNSERegularity, false);
  assert.equal(producer.scope.generalTriangularCompleteRootBound, false);

  assert.equal(independent.schemaVersion, "r072g-independent-certificate-v1");
  assert.equal(independent.auditId, "R0.72G-complete-root-independent");
  assert.equal(independent.allRequiredChecksPassed, true);
  assert.ok(independent.checks.every((row) => row.passed));
  assert.match(independent.method.evolution, /Fourier Strang split step/);
  assert.match(independent.method.heatStep, /exact diagonal half steps/);
  assert.equal(independent.scope.intervalArithmetic, false);
  assert.equal(independent.scope.provesNSERegularity, false);

  assert.match(config.producer.method, /fixed-step real-lattice RK4/);
  assert.match(config.producer.method, /cubic Hermite and Brent/);
  assert.match(config.independent.method, /Fourier Strang split step/);
  assert.deepEqual(config.producer.R, [8, 12, 16, 24, 32, 48, 64]);
  assert.deepEqual(config.independent.R, [8, 12, 16, 24, 32]);
  assert.doesNotMatch(config.producer.method, /adaptive BDF/i);

  assert.doesNotMatch(
    producerScript,
    /(?:from|import)\s+.*r072g_independent_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /(?:from|import)\s+.*r072g_exact_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /certificates\/r072g\/(?:result|producer)/,
  );

  const producerByR = new Map(producer.rows.map((row) => [row.R, row]));
  let maximumRelativeMassGap = 0;
  for (const row of independent.rows) {
    const reference = producerByR.get(row.R);
    assert.ok(reference, `producer row R=${row.R}`);
    assert.equal(row.rootCount, reference.rootCount, `root count R=${row.R}`);
    const gap = Math.abs(row.completeSlopeMass - reference.completeSlopeMass) /
      Math.max(row.completeSlopeMass, reference.completeSlopeMass);
    maximumRelativeMassGap = Math.max(maximumRelativeMassGap, gap);
  }
  assert.ok(maximumRelativeMassGap < 2e-6);
  assert.ok(Math.abs(maximumRelativeMassGap - 9.179804841673305e-7) < 1e-16);
  assert.equal(producer.rows.at(-1).R, 64);
  assert.equal(producer.rows.at(-1).rootCount, 31242);
  assert.ok(Math.abs(producer.rows.at(-1).completeSlopeMass - 7.091268660432219) < 1e-14);
  assert.ok(Math.abs(producer.logFit.slopeAgainstLogDelta - 0.4075416542406286) < 1e-15);

  assert.equal(producerFailed.allRequiredChecksPassed, false);
  assert.ok(producerFailed.checks.some((row) => !row.passed));
  assert.equal(independentFailed.allRequiredChecksPassed, false);
  assert.ok(independentFailed.checks.some((row) => !row.passed));
  for (const log of [producerProgress, independentProgress]) {
    assert.equal(log[0].status, "started");
    assert.equal(log.at(-1).stage, "audit");
    assert.equal(log.at(-1).status, "completed");
    assert.match(log.at(-1).message, /allRequiredChecksPassed=True/);
  }
  for (const log of [producerResource, independentResource]) {
    assert.ok(log.length >= 2);
    assert.ok(log.every((row) => Number.isFinite(row.elapsedSeconds)));
  }
});

test("seals the complete R0.72G certificate package", async () => {
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
    "independent-attempt1-failed-result.json",
    "producer-progress.ndjson",
    "independent-progress.ndjson",
  ]) {
    assert.match(ledger, new RegExp(`  ${required.replaceAll(".", "\\.")}$`, "m"));
  }
});

test("archives a 19-of-19 formal figure and mirrors all public assets exactly", async () => {
  const [manifest, validation, config, contract, results] = await Promise.all([
    readJson(resolve(figureRoot, "manifest.json")),
    readJson(resolve(figureRoot, "validation.json")),
    readJson(resolve(figureRoot, "config.json")),
    readJson(resolve(figureRoot, "contract.json")),
    readJson(resolve(figureRoot, "results.json")),
  ]);

  assert.equal(manifest.schemaVersion, "r072g-figure-manifest-v1");
  assert.equal(manifest.release, "R0.72G");
  assert.equal(manifest.figureId, "R0.72G-1");
  assert.equal(manifest.status, "formal");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(manifest.dataSummary.commonRootCountsEqual, true);
  assert.equal(manifest.dataSummary.maximumCommonRelativeMassGap,
    9.179804841673305e-7);
  assert.equal(manifest.dataSummary.largestRootCount, 31242);
  assert.equal(manifest.dataSummary.rowCount, 56);
  assert.match(manifest.claimBoundary, /fixed-q0 exact real one-carrier/);
  assert.match(manifest.claimBoundary, /does not prove a multi-carrier trace theorem/);
  assert.match(manifest.claimBoundary, /regularity/);

  assert.equal(validation.schemaVersion, "r072g-figure-validation-v1");
  assert.equal(validation.allPassed, true);
  assert.equal(validation.requiredCount, 19);
  assert.equal(validation.passedCount, 19);
  assert.equal(validation.checks.length, 19);
  assert.ok(validation.checks.every((row) => row.passed));
  assert.deepEqual(
    validation.checks.find((row) => row.name === "public_copies").value,
    { pdf: true, png: true, svg: true },
  );

  assert.equal(config.release, "R0.72G");
  assert.equal(config.figure.widthMillimetres, 177.8);
  assert.equal(config.figure.heightMillimetres, 97.79);
  assert.equal(config.figure.pngDpi, 600);
  assert.equal(contract.release, "R0.72G");
  assert.equal(contract.widthMm, 177.8);
  assert.equal(contract.heightMm, 97.79);
  assert.deepEqual(contract.outputs, ["figure.pdf", "figure.svg", "figure.png"]);
  assert.equal(results.allRequiredSourceChecksPassed, true);
  assert.equal(results.summary.rowCount, 56);
  assert.equal(results.summary.commonRootCountsEqual, true);

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
        "figures/r0-72g-complete-root-packing." + extension,
      )),
    ]);
    assert.equal(Buffer.compare(archived, published), 0, extension);
  }
});
