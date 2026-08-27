import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { dirname, resolve, sep } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificateRoot = resolve(root, "research/certificates/r072n");

async function json(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

async function ndjson(path) {
  const value = (await readFile(path, "utf8")).trim();
  return value ? value.split(/\r?\n/).map((line) => JSON.parse(line)) : [];
}

async function csv(path) {
  const lines = (await readFile(path, "utf8")).trim().split(/\r?\n/);
  assert.ok(lines.length >= 2, `${path} has no data rows`);
  const header = lines[0].split(",");
  return lines.slice(1).map((line) => {
    const values = line.split(",");
    assert.equal(values.length, header.length, `malformed CSV row in ${path}`);
    return Object.fromEntries(header.map((name, index) => [name, values[index]]));
  });
}

function finite(row, key) {
  const value = Number(row[key]);
  assert.ok(Number.isFinite(value), `${key} is not finite`);
  return value;
}

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

async function verifyShaLedger(directory, required) {
  const ledger = (await readFile(resolve(directory, "SHA256SUMS"), "utf8")).trim();
  const rows = ledger ? ledger.split(/\r?\n/) : [];
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^\r\n]+)$/);
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
    const [, expected, relative] = match;
    assert.ok(!relative.includes("/") && !relative.includes("\\"), relative);
    const target = resolve(directory, relative);
    assert.ok(target.startsWith(directory + sep), `ledger path escapes: ${relative}`);
    assert.equal(sha256(await readFile(target)), expected, relative);
    names.push(relative);
  }
  assert.equal(new Set(names).size, names.length, "duplicate checksum rows");
  assert.deepEqual(names, [...names].sort(), "checksum rows are not sorted");
  assert.ok(!names.includes("SHA256SUMS"), "ledger must not hash itself");
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()), "symlink in archive");
  const expectedNames = entries
    .filter(
      (entry) =>
        entry.isFile() &&
        !["SHA256SUMS", ".SHA256SUMS.tmp", ".DS_Store"].includes(entry.name),
    )
    .map((entry) => entry.name)
    .sort();
  assert.deepEqual(names, expectedNames, "checksum ledger is not complete");
  for (const name of required) {
    assert.ok(names.includes(name), `SHA256SUMS omits ${name}`);
  }
  return names;
}

test("locks the full-chain moment, action, and scalar-screen decisions", async () => {
  const [report, gap, audit] = await Promise.all([
    readFile(resolve(root, "research/r072n_report-source.md"), "utf8"),
    readFile(resolve(root, "research/r072n_gap_matrix.md"), "utf8"),
    readFile(resolve(root, "research/r072n_independent_audit.md"), "utf8"),
  ]);

  for (const token of [
    String.raw`\frac12E'(y)=-D(y)`,
    String.raw`D'(y)=-2P(y)+2g(y)S(y)`,
    String.raw`S(y)=\sum_{n\in\mathbb Z}(2n+1)`,
    String.raw`|S(y)|\le2\sqrt{D(y)E(y)}`,
    String.raw`D'(y)\le-2D(y)^2+4\sigma\sqrt{D(y)}`,
    String.raw`\max\{1,(2\sigma)^{2/3}\}`,
    String.raw`K_\sigma\le C(1+\sigma^{2/3})`,
    String.raw`\mathscr A_\sigma`,
    String.raw`\sigma^{-2/3}\log\sigma`,
    String.raw`\frac{\sigma^{1/3}x_\sigma}{K_\sigma}`,
    String.raw`\frac1T`,
    String.raw`\frac{K+x}{Vx}`,
    String.raw`T_\sigma`,
    String.raw`\asymp\sigma^{1/3}`,
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /action-poor condition fails/i);
  assert.match(report, /full infinite chain/i);
  assert.match(report, /Galerkin truncations[\s\S]*parabolic smoothing/i);
  assert.match(gap, /Full-chain energy identity[\s\S]*Proved/);
  assert.match(gap, /Proposed action-poor inequality[\s\S]*Disproved/);
  assert.match(gap, /Exact scalar screen[\s\S]*Proved/);
  assert.match(gap, /lower bound, not asymptotic/i);
  assert.ok(audit.includes(String.raw`D^2\le PE`));
  assert.ok(audit.includes(String.raw`\sigma^{4/3}\log\sigma`));
  assert.match(audit, /action-poor route is therefore false for this launch/i);
});

test("checks the exact Coble-He mode mapping, normalization, and Jacobian", async () => {
  const [report, gap, audit, literature, readme] = await Promise.all([
    readFile(resolve(root, "research/r072n_report-source.md"), "utf8"),
    readFile(resolve(root, "research/r072n_gap_matrix.md"), "utf8"),
    readFile(resolve(root, "research/r072n_independent_audit.md"), "utf8"),
    readFile(resolve(root, "research/r072n_literature_audit.md"), "utf8"),
    readFile(resolve(certificateRoot, "README.md"), "utf8"),
  ]);

  for (const token of [
    String.raw`t=\sigma y`,
    String.raw`\nu=\sigma^{-1}`,
    String.raw`g_n(t)=f_n^\sigma(\nu t)`,
    String.raw`k=-2`,
    "horizontal diffusion switch equal to zero",
    String.raw`e^{-\nu t}\sin\theta`,
    String.raw`0\le t\le\nu^{-1}`,
    String.raw`\|\partial_{t\theta}U_\nu\|_\infty`,
    String.raw`\nu_0(U,V)`,
    String.raw`\nu_*>0`,
    String.raw`E_g(t):=\sum_n|g_n(t)|^2`,
    String.raw`\frac1{2\pi}\|F(t)\|_{L^2(\mathbb T)}^2`,
    String.raw`\frac1{\sqrt2}E_g(t)`,
    String.raw`\sigma\,dy=dt`,
    String.raw`e^{-(3+2\mu)\nu t}`,
    String.raw`\mathcal C_{\rm diss}(\sigma)`,
    String.raw`a^2\sigma^{1/2}`,
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(gap, /Chain equals a passive-scalar shear mode[\s\S]*Proved/);
  assert.match(gap, /Coble--He hypotheses are uniform[\s\S]*direct verification/);
  assert.match(audit, /sign, or inequality-direction error was found/i);
  assert.match(audit, /\\sigma\\,dy=dt/);
  assert.ok(literature.includes("10.4310/CMS.2024.v22.n6.a10"));
  assert.ok(literature.includes("arxiv.org/abs/2309.15738"));
  assert.match(literature, /A Note on Enhanced Dissipation of Time-Dependent Shear Flows/);
  assert.match(literature, /paper does not state the project-specific cubic functional/i);
  assert.match(readme, /published enhanced-dissipation theorem/i);
  assert.match(readme, /exact Parseval and `sigma dy=dt`/i);
});

test("keeps the analytic and finite-diagnostic claim boundaries separate", async () => {
  const [report, gap, audit, literature, readme] = await Promise.all([
    readFile(resolve(root, "research/r072n_report-source.md"), "utf8"),
    readFile(resolve(root, "research/r072n_gap_matrix.md"), "utf8"),
    readFile(resolve(root, "research/r072n_independent_audit.md"), "utf8"),
    readFile(resolve(root, "research/r072n_literature_audit.md"), "utf8"),
    readFile(resolve(certificateRoot, "README.md"), "utf8"),
  ]);

  assert.match(report, /It does not prove:[\s\S]*logarithmic growth/i);
  assert.match(report, /multi-carrier or multiscale strong-coupling theorem/i);
  assert.match(report, /Clay Millennium problem remains open/i);
  assert.match(gap, /O\(a\^2\\log\\sigma\)[\s\S]*Open/);
  assert.match(gap, /General 3D continuation criterion[\s\S]*Open/);
  assert.match(audit, /Coble and He do not state the cubic\s+corollary/i);
  assert.match(audit, /does not prove the finite-data\s+suggestion/i);
  assert.match(literature, /Safe public wording/i);
  assert.match(literature, /logarithmic,[\s\S]*remain open/i);
  assert.match(literature, /not a proof of novelty or priority/i);
  assert.match(readme, /finite binary64 corroboration, not interval/i);
  assert.match(readme, /do not prove the\s+numerically suggested logarithmic cubic law/i);
  assert.match(readme, /resolution of the Clay Millennium Problem/i);

  for (const text of [report, gap, audit, readme]) {
    assert.doesNotMatch(text, /Coble and He proved the R0\.72N cubic theorem/i);
    assert.doesNotMatch(text, /Clay Millennium Problem is (?:solved|resolved)/i);
    assert.doesNotMatch(text, /proves general three-dimensional Navier--Stokes regularity/i);
  }
});

test("seals both finite-route schemas and their declared numerical boundaries", async () => {
  const [producer, independent, producerConfig, independentConfig,
    producerRows, independentRows, producerProgress, independentProgress,
    producerResources, independentResources, producerScript,
    independentScript] = await Promise.all([
      json(resolve(certificateRoot, "result.json")),
      json(resolve(certificateRoot, "independent-result.json")),
      json(resolve(certificateRoot, "config.json")),
      json(resolve(certificateRoot, "independent-config.json")),
      csv(resolve(certificateRoot, "producer-dissipative.csv")),
      csv(resolve(certificateRoot, "independent-dissipative.csv")),
      ndjson(resolve(certificateRoot, "producer-progress.ndjson")),
      ndjson(resolve(certificateRoot, "independent-progress.ndjson")),
      ndjson(resolve(certificateRoot, "producer-resource.ndjson")),
      ndjson(resolve(certificateRoot, "independent-resource.ndjson")),
      readFile(resolve(root, "research/r072n_exact_audit.py"), "utf8"),
      readFile(resolve(root, "research/r072n_independent_audit.py"), "utf8"),
    ]);

  assert.equal(producer.audit, "R0.72N producer dissipative-carrier audit");
  assert.equal(independent.audit, "R0.72N independent finite-chain audit");
  for (const result of [producer, independent]) {
    assert.equal(result.schemaVersion, 1);
    assert.equal(result.status, "passed");
    assert.ok(Object.values(result.checks).every(Boolean));
    assert.deepEqual(result.counts, { dissipative: 10 });
    assert.ok(Math.abs(result.provedExponents.momentUpper - 2 / 3) < 1e-15);
    assert.ok(Math.abs(result.provedExponents.actionLowerBeforeLift + 2 / 3) < 1e-15);
    assert.ok(Math.abs(result.provedExponents.scalarScreen - 1 / 3) < 1e-15);
    assert.ok(Math.abs(result.provedExponents.trueCubicUpper - 1 / 2) < 1e-15);
    assert.ok(Number.isFinite(result.elapsedSeconds) && result.elapsedSeconds >= 0);
    assert.ok(Number.isFinite(result.maxRssMb) && result.maxRssMb > 0);
    assert.match(result.gitCommit, /^[0-9a-f]{40}$/);
    assert.ok(result.limitations.some((value) => /finite binary64/i.test(value)));
    assert.ok(result.limitations.some((value) => /enhanced-dissipation theorem/i.test(value)));
    assert.ok(result.limitations.some((value) => /logarithmic cubic trend is not proved/i.test(value)));
    assert.ok(result.limitations.some((value) => /general three-dimensional/i.test(value)));
  }

  assert.equal(producerConfig.schemaVersion, 1);
  assert.equal(independentConfig.schemaVersion, 1);
  assert.equal(producerConfig.audit, producer.audit);
  assert.equal(independentConfig.audit, independent.audit);
  assert.deepEqual(producerConfig.sigmas, independentConfig.sigmas);
  assert.equal(producerConfig.sigmas.length, 10);
  assert.equal(producerConfig.sigmas[0], 16);
  assert.equal(producerConfig.sigmas.at(-1), 32768);
  assert.equal(producerConfig.gitCommit, producer.gitCommit);
  assert.equal(independentConfig.gitCommit, independent.gitCommit);
  assert.equal(producer.gitCommit, independent.gitCommit);
  assert.notEqual(producerConfig.method, independentConfig.method);

  for (const [rows, tailField] of [
    [producerRows, "maxHighModeMass"],
    [independentRows, "boundaryMass"],
  ]) {
    assert.equal(rows.length, 10);
    for (const row of rows) {
      assert.equal(row.passed, "True");
      assert.ok(finite(row, "maxMoment") <= finite(row, "momentBarrier") * 1.002);
      assert.ok(finite(row, "momentRefinementRelativeDifference") < 0.02);
      assert.ok(finite(row, "actionRefinementRelativeDifference") < 0.025);
      assert.ok(finite(row, "cubicRefinementRelativeDifference") < 0.025);
      assert.ok(finite(row, "action") > 0);
      assert.ok(finite(row, "cubic") > 0);
      assert.ok(finite(row, tailField) < 1e-18);
    }
    assert.ok(finite(rows.at(-1), "cubicOverSqrtSigma") < 0.2);
  }

  for (const progress of [producerProgress, independentProgress]) {
    assert.ok(progress.length >= 12);
    assert.equal(progress[0].stage, "start");
    assert.equal(progress.at(-1).stage, "complete");
    assert.equal(progress.at(-1).status, "passed");
  }
  for (const resources of [producerResources, independentResources]) {
    assert.ok(resources.length >= 12);
    assert.ok(resources.every((row) => Number.isFinite(row.elapsedSeconds)));
    assert.ok(resources.every((row) => Number.isFinite(row.maxRssMb)));
  }

  assert.doesNotMatch(producerScript, /(?:from|import)\s+.*r072n_independent_audit/);
  assert.doesNotMatch(independentScript, /(?:from|import)\s+.*r072n_exact_audit/);
  assert.doesNotMatch(
    independentScript,
    /producer-dissipative\.csv|["']result\.json["']/,
  );
});

test("enforces every producer-independent crosscheck threshold", async () => {
  const [crosscheck, producerRows, independentRows] = await Promise.all([
    json(resolve(certificateRoot, "crosscheck.json")),
    csv(resolve(certificateRoot, "producer-dissipative.csv")),
    csv(resolve(certificateRoot, "independent-dissipative.csv")),
  ]);
  const fields = [
    "maxMoment",
    "action",
    "liftedAction",
    "actionPoorRatio",
    "tOverV",
    "cubic",
  ];
  const producerBySigma = new Map(producerRows.map((row) => [Number(row.sigma), row]));
  const independentBySigma = new Map(independentRows.map((row) => [Number(row.sigma), row]));

  assert.equal(crosscheck.schemaVersion, 1);
  assert.equal(crosscheck.status, "passed");
  assert.ok(Object.values(crosscheck.checks).every(Boolean));
  assert.equal(crosscheck.comparisons.length, 10 * fields.length);
  assert.deepEqual(Object.keys(crosscheck.maximumRelativeDifferences).sort(), [...fields].sort());
  for (const field of fields) {
    assert.ok(Number.isFinite(crosscheck.maximumRelativeDifferences[field]));
    assert.ok(crosscheck.maximumRelativeDifferences[field] <= 0.005, field);
  }
  for (const comparison of crosscheck.comparisons) {
    assert.ok(fields.includes(comparison.field));
    assert.equal(comparison.tolerance, 0.005);
    assert.equal(comparison.passed, true);
    assert.ok(Number.isFinite(comparison.relativeDifference));
    assert.ok(comparison.relativeDifference <= comparison.tolerance);
    assert.equal(
      comparison.producer,
      finite(producerBySigma.get(comparison.sigma), comparison.field),
    );
    assert.equal(
      comparison.independent,
      finite(independentBySigma.get(comparison.sigma), comparison.field),
    );
  }
  assert.match(crosscheck.limitations, /finite binary64 corroboration/i);
  assert.match(crosscheck.limitations, /not an analytic, interval, or full Navier--Stokes proof/i);
});

test("verifies the complete stable R0.72N checksum ledger", async () => {
  const required = [
    "README.md",
    "build_hashes.py",
    "command.txt",
    "config.json",
    "crosscheck.json",
    "environment.txt",
    "independent-config.json",
    "independent-dissipative.csv",
    "independent-environment.txt",
    "independent-monitor.log",
    "independent-progress.ndjson",
    "independent-resource.ndjson",
    "independent-result.json",
    "producer-dissipative.csv",
    "producer-monitor.log",
    "producer-progress.ndjson",
    "producer-resource.ndjson",
    "result.json",
  ];
  const names = await verifyShaLedger(certificateRoot, required);
  assert.ok(names.length >= required.length);

  const readme = await readFile(resolve(certificateRoot, "README.md"), "utf8");
  assert.match(
    readme,
    /Source commit: `(?:<SOURCE_COMMIT_40_HEX>|[0-9a-f]{40})`/,
  );
  assert.match(
    readme,
    /Certificate commit: `(?:<CERTIFICATE_COMMIT_40_HEX>|[0-9a-f]{40})`/,
  );
});
