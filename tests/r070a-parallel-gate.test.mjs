import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const research = new URL("research/", root);
const pilotRoot = new URL("certificates/r070a-pilot/", research);

test("records the R0.70A literature collision boundary", async () => {
  const note = await readFile(
    new URL("r070a_literature_collision_matrix.md", research),
    "utf8",
  );

  assert.match(note, /路线审计，不是数学结果/);
  assert.match(note, /arXiv:2606\.27560v1/);
  assert.match(note, /arXiv:2607\.08866v2/);
  assert.match(note, /全远场无权闭合/);
  assert.match(note, /导数兼容交换子缺陷/);
  assert.match(note, /局部化壳层预算/);
  assert.match(note, /STOP-F（动态重写）/);
  assert.match(note, /当前不能说它已经是 KHM 或带通能量预算的重写/);
});

test("keeps moving annuli separate from a genuine dynamic normal form", async () => {
  const note = await readFile(
    new URL("r070a_moving_annular_balance_note.md", research),
    "utf8",
  );

  assert.ok(note.includes("There is no \\(\\dot r\\) in (2.9)."));
  assert.match(note, /Their sum is zero/);
  assert.match(note, /It does \*\*not\*\* rewrite/);
  assert.ok(note.includes("normal form \\(Q_r\\) whose **nonlinear**"));
  assert.match(note, /No operator satisfying\s+all five requirements has been constructed/);
  assert.match(note, /unclosed derivation and route test/);

  const tags = [...note.matchAll(/\\tag\{([^}]+)\}/g)].map((match) => match[1]);
  assert.equal(tags.length, 52);
  assert.equal(new Set(tags).size, tags.length);
  assert.equal((note.match(/\\\[/g) ?? []).length, (note.match(/\\\]/g) ?? []).length);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /[ \t]+$/m);
});

test("extracts a uniform fixed-ratio margin without claiming an explicit rho interval", async () => {
  const [note, certificateText] = await Promise.all([
    readFile(new URL("r070a_scale_ratio_robustness_note.md", research), "utf8"),
    readFile(new URL("certificates/r069w/result.json", research), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  const a = 1 / 64;
  const c1 = certificate.coefficientIntervals.j0.c1[1];
  const c2 = certificate.coefficientIntervals.j0.c2[1];
  const c3 = certificate.coefficientIntervals.j0.c3[1];
  const f = a * (c1 + c2 * a + c3 * a ** 2);
  const derivativeVertex = -c2 / (3 * c3);
  const derivativeAtA = c1 + 2 * c2 * a + 3 * c3 * a ** 2;

  const d = certificate.coefficientIntervals.jMinus2;
  const g = d.c0[1] + d.c1[1] * a + d.c2[1] * a ** 2 + d.c3[1] * a ** 3;

  assert.ok(derivativeVertex < a);
  assert.ok(derivativeAtA < 0);
  assert.ok(f <= -1.246030236725547e-5);
  assert.ok(g < -1.17e-3);
  assert.match(note, /non-explicit robustness around scale ratio four/);
  assert.match(note, /exact analytic amplitude law established in the R0\.69V\/W/);
  assert.match(note, /1246030236725547/);
  assert.match(note, /raw JSON enclosure[\s\S]*is not used as an exact zero/);
  assert.match(note, /supplies neither a decimal lower bound/);
  assert.match(note, /C\(\[0,T\];H\^4\)\\cap L\^2\(0,T;H\^5\)/);
  assert.match(note, /3\.9<\\rho<4\.1[\s\S]*candidate for the next certification attempt/);
  assert.match(note, /No DGX run is justified yet/);
});

test("archives the five-point scale-ratio pilot as diagnostic evidence", async () => {
  const [resultText, rawText, readme, command, environment] = await Promise.all([
    readFile(new URL("result.json", pilotRoot), "utf8"),
    readFile(new URL("raw-result.json", pilotRoot), "utf8"),
    readFile(new URL("README.md", pilotRoot), "utf8"),
    readFile(new URL("command.txt", pilotRoot), "utf8"),
    readFile(new URL("environment.txt", pilotRoot), "utf8"),
  ]);
  const result = JSON.parse(resultText);
  const raw = JSON.parse(rawText);

  assert.equal(result.release, "R0.70A-pilot");
  assert.equal(result.status, "diagnostic");
  assert.equal(result.records.length, 5);
  assert.deepEqual(result.configuration, raw.configuration);
  assert.deepEqual(result.symbolicAudits, raw.symbolicAudits);
  assert.equal(result.setupSeconds, raw.setupSeconds);
  assert.deepEqual(
    result.records.map((record) => record.rhoFloat),
    [3.8, 3.9, 4, 4.1, 4.2],
  );
  assert.ok(
    result.records.every((record) =>
      Object.values(record.coarseFixedRatioSignsCertified).every((value) => value === false),
    ),
  );

  for (const [index, record] of result.records.entries()) {
    const rawRecord = raw.records[index];
    const preservedRecord = structuredClone(record);
    delete preservedRecord.decisionQuantities.discriminantFromCoefficientMidpoints;
    assert.deepEqual(preservedRecord, rawRecord);

    const c1 = record.j0.c1.midpoint;
    const c2 = record.j0.c2.midpoint;
    const c3 = record.j0.c3.midpoint;
    const recomputed = c2 ** 2 - 4 * c1 * c3;
    const stored = record.decisionQuantities.discriminantFromCoefficientMidpoints.midpoint;
    assert.ok(Math.abs(recomputed - stored) < 1e-15);
    assert.match(
      record.decisionQuantities.discriminantFromCoefficientMidpoints.certificationStatus,
      /diagnostic only/,
    );
    assert.ok(record.decisionQuantities.discriminant.width > 2e9);
    assert.deepEqual(record.evaluatedRadialBoxes, { "-2": 396, "0": 396 });
  }

  assert.equal(result.secantDiagnostics.length, raw.secantDiagnostics.length);
  for (const [index, diagnostic] of result.secantDiagnostics.entries()) {
    const rawDiagnostic = raw.secantDiagnostics[index];
    assert.deepEqual(diagnostic.rhoInterval, rawDiagnostic.rhoInterval);
    assert.equal(diagnostic.certificationStatus, rawDiagnostic.certificationStatus);
    for (const key of ["c1", "c2", "c3", "endpointJMinus2AtA0"]) {
      assert.equal(
        diagnostic.midpointSecantSlopesPerUnitRho[key],
        rawDiagnostic.midpointSecantSlopesPerUnitRho[key],
      );
    }
  }

  assert.equal(result.provenance.postProcessedWithoutReintegration, true);
  assert.equal(result.provenance.originalProducerScriptByteIdentityArchived, false);
  assert.equal(result.provenance.exactPostprocessCommandArchived, false);
  assert.equal(result.provenance.rawResultArchived, "raw-result.json");
  assert.equal(result.provenance.rigorousFieldsComparedWithRawResult, true);
  assert.match(result.claimBoundary, /not certificates/);
  assert.match(readme, /rather than a formal monitored certificate/);
  assert.match(readme, /not an end-to-end producer archive/);
  assert.match(readme, /exact byte[\s\S]*was not archived/);
  assert.match(readme, /command\.txt/);
  assert.match(readme, /environment\.txt/);
  assert.match(command, /--rhos 3\.8,3\.9,4,4\.1,4\.2/);
  assert.match(command, /--cutoff-cells 64/);
  assert.match(command, /--arb-precision 128/);
  assert.match(environment, /python_executable=.*tmp\/r068b-venv\/bin\/python/);
  assert.match(environment, /python_flint=0\.9\.0/);
});

test("locks every archived R0.70A pilot payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", pilotRoot), "utf8");
  const lines = sums.trim().split("\n");
  assert.equal(lines.length, 7);
  assert.match(sums, /\.\.\/\.\.\/two_scale_annular_interval\.py/);
  assert.match(sums, /raw-result\.json/);

  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `invalid checksum line: ${line}`);
    const payload = await readFile(new URL(match[2], pilotRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("keeps the integrated route decision internal and falsifiable", async () => {
  const summary = await readFile(
    new URL("r070a_parallel_gate_summary.md", research),
    "utf8",
  );

  assert.match(summary, /R0\.70B gate is a matching-scale bridge test/);
  assert.match(summary, /small symbolic triad test/);
  assert.match(summary, /does not justify DGX use/);
  assert.match(summary, /R0\.70A stays outside `public\/`/);
  assert.match(summary, /No item below is claimed to solve/);
  assert.ok(
    summary.includes("\\max_{0\\le a\\le1}\\min\\{A_0(a),A_{-2}(a)\\}"),
  );
  assert.doesNotMatch(summary, /\\max\\\{A_0\(a\),A_\{-2\}\(a\)\\\}/);
  assert.match(summary, /1\.246030236725547\\times 10\^\{-5\}/);
});
