import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, resolve, sep } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");
const certificateRoot = resolve(root, "research/certificates/r072m");
const figureRoot = resolve(
  root,
  "figures/r072m-danger-window/fig-r072m-danger-window",
);

async function json(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

async function ndjson(path) {
  const value = (await readFile(path, "utf8")).trim();
  return value ? value.split("\n").map((line) => JSON.parse(line)) : [];
}

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

async function verifyShaLedger(directory, required = []) {
  const ledger = await readFile(resolve(directory, "SHA256SUMS"), "utf8");
  const rows = ledger.trim().split("\n");
  assert.ok(rows.length >= required.length, "SHA256SUMS is unexpectedly short");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
    const [, expected, relative] = match;
    const target = resolve(directory, relative);
    assert.ok(
      target.startsWith(directory + sep),
      `SHA256SUMS path escapes its archive: ${relative}`,
    );
    assert.equal(sha256(await readFile(target)), expected, relative);
    names.push(relative);
  }
  for (const name of required) {
    assert.ok(names.includes(name), `SHA256SUMS omits ${name}`);
  }
  return names;
}

test("proves the exact scalar danger interval and both safe branches", async () => {
  const [report, gap, audit, note] = await Promise.all([
    readFile(resolve(root, "research/r072m_report-source.md"), "utf8"),
    readFile(resolve(root, "research/r072m_gap_matrix.md"), "utf8"),
    readFile(resolve(root, "research/r072m_independent_audit.md"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72m.html"), "utf8"),
  ]);

  for (const token of [
    String.raw`T(x)=\frac{\min\{U,Vx\}}{K+x}`,
    String.raw`H=\frac UV`,
    "Theorem 5.1 -- exact superlevel interval",
    String.raw`\frac{AK}{V-A}<x<\frac UA-K`,
    String.raw`A\ge U/(K+H)`,
    String.raw`0<A<U/(K+H)`,
    String.raw`[Z,\infty)`,
    String.raw`Vx=o(K)`,
    String.raw`U=o(K+x)`,
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.ok(report.includes(String.raw`strictly increasing on \(0\le x\le H\)`));
  assert.match(report, /strictly decreasing on\s+\\\(x\\ge H\\\)/);
  assert.match(
    report,
    /only an intermediate action window can\s+make the scalar cubic term large/i,
  );

  assert.match(gap, /Exact superlevel set[\s\S]*Proved/);
  assert.match(gap, /Frozen chain enters the optimized[\s\S]*Disproved/);
  assert.ok(
    audit.includes(String.raw`exact scalar superlevel set is an interval around \(H=U/V\)`),
  );
  assert.match(audit, /action-poor\s+\\\(Vx\\\)-branch/);
  assert.match(note, /精确 action danger window/i);
  assert.match(note, /只有中间区间可能使这个 scalar term 变大/);
});

test("keeps the full-lattice Bessel, moment, action, and cubic statements exact", async () => {
  const [report, gap, audit, note] = await Promise.all([
    readFile(resolve(root, "research/r072m_report-source.md"), "utf8"),
    readFile(resolve(root, "research/r072m_gap_matrix.md"), "utf8"),
    readFile(resolve(root, "research/r072m_independent_audit.md"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72m.html"), "utf8"),
  ]);

  for (const token of [
    String.raw`f_n(s)=\sqrt2\,J_n'(2s)`,
    String.raw`\sum_{n\in\mathbb Z}n^2|f_n(s)|^2=1+s^2`,
    String.raw`q(s)=\sum_{n\in\mathbb Z}`,
    String.raw`A_\sigma\sim A_0\sigma^{-2/3}\log\sigma`,
    String.raw`x_{\rm fr}\asymp\sigma^{4/3}\log\sigma`,
    String.raw`\mathcal C_{\rm fr}(\sigma)`,
    String.raw`\frac{16}{\pi^2}a^2\log\sigma+O(a^2)`,
    String.raw`\frac{x_{\rm fr}}H`,
    String.raw`\frac{Vx_{\rm fr}}{K_{\rm fr}}`,
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /complete negative-norm density/i);
  assert.match(report, /target-row integral[\s\S]*is not the complete negative-norm action/i);
  assert.match(report, /complete frozen critical-action asymptotic/i);
  assert.match(report, /sharp frozen true-cubic asymptotic/i);
  assert.ok(gap.includes(String.raw`(16/\pi^2)a^2\log\sigma+O(a^2)`));
  assert.ok(
    audit.includes(String.raw`Fourier-gradient identity is exactly \(1+s^2\)`),
  );
  assert.ok(
    audit.includes(String.raw`factor in the cubic asymptotic is \(16/\pi^2\)`),
  );
  assert.match(note, /完整无限 Fourier 格点|完整无限 Fourier lattice/);
  assert.ok(note.includes("16/\\pi^2"));
});

test("separates the frozen theorem from dissipative diagnostics and general NSE", async () => {
  const [report, gap, literature, audit, note] = await Promise.all([
    readFile(resolve(root, "research/r072m_report-source.md"), "utf8"),
    readFile(resolve(root, "research/r072m_gap_matrix.md"), "utf8"),
    readFile(resolve(root, "research/r072m_literature_audit.md"), "utf8"),
    readFile(resolve(root, "research/r072m_independent_audit.md"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72m.html"), "utf8"),
  ]);

  for (const text of [report, gap, literature, audit, note]) {
    assert.doesNotMatch(text, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
  }
  assert.match(report, /zero-diffusion reference/i);
  assert.match(
    report,
    /Removing the diagonal heat operator is a benchmark operation, not\s+an exact PDE reduction/i,
  );
  assert.match(report, /logarithmic cubic upper bound[\s\S]*dissipative chain[\s\S]*does not prove|It does not prove:[\s\S]*logarithmic cubic upper bound/i);
  assert.match(report, /Clay Millennium problem remains open/i);
  assert.match(gap, /Dissipative cubic is logarithmic[\s\S]*Open/);
  assert.match(gap, /General 3D continuation criterion[\s\S]*Open/);
  assert.match(audit, /finite dissipative curves are diagnostic/i);
  assert.match(literature, /bounded search|bounded primary-source/i);
  assert.match(literature, /not a proof\s+of priority/i);
  for (const source of [
    "10.1007/s00205-017-1099-y",
    "10.1112/jlms.12782",
    "dlmf.nist.gov/10.6",
    "dlmf.nist.gov/10.17",
    "dlmf.nist.gov/10.19.iii",
    "dlmf.nist.gov/10.20.i",
  ]) {
    assert.ok(literature.includes(source), source);
  }
  assert.match(note, /dissipative uniform theorem: OPEN/);
  assert.match(note, /一般三维正则性：OPEN/);
  assert.match(note, /Clay 千禧年问题仍未解决/);
  assert.doesNotMatch(note, /千禧年问题(?:已经|已被|得到)(?:解决|证明)/);
});

test("seals producer, independent, and crosscheck certificate schemas", async () => {
  const [producer, independent, crosscheck, producerConfig, independentConfig,
    producerProgress, independentProgress, producerResources,
    independentResources, producerScript, independentScript] = await Promise.all([
      json(resolve(certificateRoot, "result.json")),
      json(resolve(certificateRoot, "independent-result.json")),
      json(resolve(certificateRoot, "crosscheck.json")),
      json(resolve(certificateRoot, "config.json")),
      json(resolve(certificateRoot, "independent-config.json")),
      ndjson(resolve(certificateRoot, "producer-progress.ndjson")),
      ndjson(resolve(certificateRoot, "independent-progress.ndjson")),
      ndjson(resolve(certificateRoot, "producer-resource.ndjson")),
      ndjson(resolve(certificateRoot, "independent-resource.ndjson")),
      readFile(resolve(root, "research/r072m_exact_audit.py"), "utf8"),
      readFile(resolve(root, "research/r072m_independent_audit.py"), "utf8"),
    ]);

  for (const result of [producer, independent]) {
    assert.equal(result.schemaVersion, 1);
    assert.equal(result.status, "passed");
    assert.ok(Object.values(result.checks).every(Boolean));
    assert.deepEqual(Object.keys(result.counts).sort(), [
      "action",
      "bessel",
      "danger-window",
      "dissipative",
      "frozen-cubic",
    ]);
    assert.ok(Object.values(result.counts).every((count) => count > 0));
    assert.ok(Number.isFinite(result.elapsedSeconds));
    assert.ok(Number.isFinite(result.maxRssMb));
    assert.match(result.gitCommit, /^[0-9a-f]{40}$/);
    assert.ok(
      Math.abs(result.asymptoticCubicConstant - 16 / Math.PI ** 2) < 1e-15,
    );
    assert.ok(result.limitations.some((value) => /finite binary64/i.test(value)));
    assert.ok(result.limitations.some((value) => /not proved/i.test(value)));
    assert.ok(result.limitations.some((value) => /general three-dimensional/i.test(value)));
  }
  assert.match(producer.audit, /producer phase-mixing audit/i);
  assert.match(independent.audit, /independent phase-mixing audit/i);
  assert.equal(producerConfig.schemaVersion, 1);
  assert.equal(independentConfig.schemaVersion, 1);
  assert.equal(producerConfig.audit, "R0.72M producer phase-mixing audit");
  assert.equal(independentConfig.audit, "R0.72M independent phase-mixing audit");

  assert.equal(crosscheck.schemaVersion, 1);
  assert.equal(crosscheck.status, "passed");
  assert.ok(Object.values(crosscheck.checks).every(Boolean));
  assert.ok(crosscheck.comparisons.length > 0);
  assert.match(crosscheck.limitations, /corroboration, not an analytic or interval proof/i);
  for (const key of ["bessel", "action", "frozen-cubic", "dissipative"]) {
    assert.ok(Number.isFinite(crosscheck.maximumRelativeDifferences[key]), key);
  }

  for (const progress of [producerProgress, independentProgress]) {
    assert.ok(progress.length >= 6);
    assert.equal(progress.at(-1).stage, "complete");
    assert.equal(progress.at(-1).status, "passed");
  }
  for (const resources of [producerResources, independentResources]) {
    assert.ok(resources.length >= 6);
    assert.ok(resources.every((row) => Number.isFinite(row.elapsedSeconds)));
    assert.ok(resources.every((row) => Number.isFinite(row.maxRssMb)));
  }

  assert.doesNotMatch(
    producerScript,
    /(?:from|import)\s+.*r072m_independent_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /(?:from|import)\s+.*r072m_exact_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /certificates\/r072m\/(?:result|producer-)/,
  );
});

test("verifies every R0.72M certificate checksum", async () => {
  const names = await verifyShaLedger(certificateRoot, [
    "result.json",
    "independent-result.json",
    "crosscheck.json",
    "config.json",
    "independent-config.json",
    "producer-progress.ndjson",
    "independent-progress.ndjson",
    "producer-resource.ndjson",
    "independent-resource.ndjson",
    "producer-danger-window.csv",
    "independent-danger-window.csv",
    "producer-bessel.csv",
    "independent-bessel.csv",
    "producer-action.csv",
    "independent-action.csv",
    "producer-frozen-cubic.csv",
    "independent-frozen-cubic.csv",
    "producer-dissipative.csv",
    "independent-dissipative.csv",
  ]);
  assert.ok(names.length >= 25);
});

test("archives a formal journal figure and mirrors all public assets byte-for-byte", async () => {
  const [manifest, validation, config, contract, results] = await Promise.all([
    json(resolve(figureRoot, "manifest.json")),
    json(resolve(figureRoot, "validation.json")),
    json(resolve(figureRoot, "config.json")),
    json(resolve(figureRoot, "contract.json")),
    json(resolve(figureRoot, "results.json")),
  ]);

  assert.equal(manifest.schemaVersion, "1.0");
  assert.equal(manifest.figureId, "fig-r072m-danger-window");
  assert.equal(manifest.release, "R0.72M");
  assert.equal(manifest.status, "formal");
  assert.match(manifest.git.sourceCommit, /^[0-9a-f]{40}$/);
  assert.match(manifest.git.certificateCommit, /^[0-9a-f]{40}$/);
  assert.match(manifest.git.manifestBuildHead, /^[0-9a-f]{40}$/);
  assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  assert.equal(manifest.computation.continuumProofLocation, "research/r072m_report-source.md");
  assert.equal(manifest.computation.finiteFitsAreDiagnostics, true);
  assert.equal(manifest.computation.newPdeEvolution, false);
  assert.equal(manifest.computation.pdeTimeStepping, false);
  assert.match(manifest.supportedClaim, /exact middle interval/i);
  assert.match(manifest.supportedClaim, /Bessel solution/i);
  assert.match(manifest.supportedClaim, /16\/pi\^2/i);
  assert.match(manifest.claimBoundary, /diagnostics? only/i);
  assert.match(manifest.claimBoundary, /not the dissipative/i);
  assert.match(manifest.claimBoundary, /general three-dimensional/i);

  assert.equal(validation.schemaVersion, 1);
  assert.equal(validation.figureId, "R0.72M-1");
  assert.equal(validation.status, "passed");
  assert.equal(validation.allPassed, true);
  assert.equal(validation.checkCount, validation.checks.length);
  assert.ok(validation.checkCount >= 18);
  assert.ok(validation.checks.every((row) => row.passed));
  for (const name of [
    "panel_a_formula",
    "panel_b_formula",
    "certificate_crosscheck",
    "frozen_constant_trend",
    "dissipative_two_routes",
    "source_lineage",
    "output_lineage",
    "public_byte_identity",
    "claim_boundary",
    "visual_inspection_declared",
  ]) {
    assert.ok(validation.checks.some((row) => row.name === name), name);
  }

  assert.equal(config.schemaVersion, "r072m-figure-config-v1");
  assert.equal(config.figure.widthMillimetres, 177.8);
  assert.equal(config.figure.heightMillimetres, 124.0);
  assert.equal(config.figure.pngDpi, 600);
  assert.equal(config.publication.directory, "public/assets/r072m");
  assert.equal(config.publication.stem, "fig-r072m-danger-window");
  assert.equal(contract.schemaVersion, "r072m-figure-contract-v1");
  assert.equal(contract.analyticClaims.length, 3);
  assert.equal(contract.finiteDiagnostics.length, 3);

  assert.equal(results.schemaVersion, 1);
  assert.equal(results.figureId, "R0.72M-1");
  assert.equal(results.status, "built");
  assert.equal(results.newPdeEvolution, false);
  assert.ok(results.summary.rowCount > 0);
  assert.equal(manifest.dataSummary.rowCount, results.summary.rowCount);
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.automaticCheckCount, validation.checkCount);
  assert.equal(manifest.qa.visualInspectionExplicit, true);
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.equal(manifest.publication.assets.length, 3);

  for (const extension of ["pdf", "svg", "png"]) {
    const [archived, published] = await Promise.all([
      readFile(resolve(figureRoot, `figure.${extension}`)),
      readFile(
        resolve(publicRoot, `assets/r072m/fig-r072m-danger-window.${extension}`),
      ),
    ]);
    assert.equal(Buffer.compare(archived, published), 0, extension);
    const record = manifest.publication.assets.find((asset) =>
      asset.path.endsWith(`.${extension}`),
    );
    assert.ok(record, extension + ": publication manifest record");
    assert.equal(record.bytes, published.length, extension + ": byte count");
    assert.equal(record.sha256, sha256(published), extension + ": SHA-256");
    assert.equal(record.byteIdenticalToMaster, true, extension);
  }
});

test("verifies the complete formal-figure checksum ledger", async () => {
  const names = await verifyShaLedger(figureRoot, [
    "manifest.json",
    "validation.json",
    "results.json",
    "data.csv",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
  ]);
  assert.ok(names.length >= 26);
});
