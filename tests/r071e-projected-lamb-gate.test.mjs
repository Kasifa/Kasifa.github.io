import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFile } from "node:child_process";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const root = new URL("../", import.meta.url);
const research = new URL("research/", root);
const certificateRoot = new URL("certificates/r071e/", research);

async function archivedJson(name) {
  return JSON.parse(await readFile(new URL(name, certificateRoot), "utf8"));
}

let reproductionPromise;

function reproduceBoth() {
  reproductionPromise ??= (async () => {
    const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
    const options = {
      cwd: fileURLToPath(root),
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    };
    const [exact, independent] = await Promise.all([
      execFileAsync(
        python,
        [fileURLToPath(new URL("r071e_exact_audit.py", research))],
        options,
      ),
      execFileAsync(
        python,
        [fileURLToPath(new URL("r071e_independent_audit.py", research))],
        options,
      ),
    ]);
    return { exact, independent };
  })();
  return reproductionPromise;
}

test("locks the R0.71E theorem and exact claim boundary", async () => {
  const [report, literature, independent, producer, checker] = await Promise.all([
    readFile(new URL("r071e_report-source.md", research), "utf8"),
    readFile(new URL("r071e_literature_audit.md", research), "utf8"),
    readFile(new URL("r071e_independent_audit.md", research), "utf8"),
    readFile(new URL("r071e_exact_audit.py", research), "utf8"),
    readFile(new URL("r071e_independent_audit.py", research), "utf8"),
  ]);

  for (const token of [
    "R0.71E — Projected Lamb compression, unconditional heat bulk, and the critical bottom-trace gap",
    "Exact projected-Lamb compression",
    "An unconditional heat-bulk estimate",
    "The normalized bulk is forced by Leray energy",
    "The exact two-derivative trace cost",
    "Theorem 10.1 — unconditional bulk closure with critical trace loss",
    "Next justified gate: R0.71F",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /no Millennium-problem claim/i);
  assert.match(report, /does \*\*not\*\* rule out a nonlinear depletion estimate/i);
  assert.match(literature, /不是数学上的不存在证明/);
  assert.match(literature, /projected-Lamb 表示本身作为新颖性主张/);
  assert.match(literature, /Yu 2026 年的预印本 arXiv:2606\.27560/);
  assert.match(independent, /imports no project audit module/i);
  assert.match(producer, /projected-lamb-bulk-and-bottom-trace-gate/);
  assert.match(checker, /deliberately imports no project audit module/);
});

test("reproduces both archived R0.71E certificates byte for byte", async () => {
  const [exactText, independentText, reproduced] = await Promise.all([
    readFile(new URL("result.json", certificateRoot), "utf8"),
    readFile(new URL("independent-result.json", certificateRoot), "utf8"),
    reproduceBoth(),
  ]);

  assert.equal(reproduced.exact.stderr, "");
  assert.equal(reproduced.independent.stderr, "");
  assert.equal(reproduced.exact.stdout, exactText);
  assert.equal(reproduced.independent.stdout, independentText);
});

test("locks the projected-Lamb compression and exact heat trace", async () => {
  const archived = await archivedJson("result.json");

  assert.equal(archived.release, "R0.71E");
  assert.equal(
    archived.status,
    "projected-lamb-bulk-and-bottom-trace-gate",
  );
  assert.equal(Object.keys(archived.checks).length, 15);
  assert.ok(Object.values(archived.checks).every(Boolean));
  assert.equal(archived.phasePlus.norms.velocityL2Squared, "6");
  assert.equal(archived.phasePlus.norms.enstrophy, "8");
  assert.equal(archived.phasePlus.norms.palinstrophy, "12");
  assert.equal(archived.phasePlus.unfiltered.combined, "2");
  assert.equal(archived.phaseMinus.unfiltered.combined, "-2");
  assert.equal(
    archived.phasePlus.norms.projectedLambHeatIntegral,
    "11/5",
  );
  assert.equal(
    archived.tightRadialSplit.bottomEqualsTwoKSquareTimesBulkResidual,
    "0",
  );
  assert.equal(
    archived.tightRadialSplit.bottomCoefficient,
    "K**2*a**2/8",
  );
  assert.equal(
    archived.tightRadialSplit.normalizedInfiniteBulk,
    "a**2/16",
  );
  assert.match(archived.routeDecision.nextGate, /R0\.71F/);
});

test("locks the independent physical-space reconstruction", async () => {
  const independent = await archivedJson("independent-result.json");

  assert.equal(independent.version, "R0.71E-independent");
  assert.equal(independent.status, "pass");
  assert.ok(Object.values(independent.checks).every(Boolean));
  assert.equal(independent.phasePlus.norms.velocityL2Squared, "6");
  assert.equal(independent.phasePlus.works.combined, "2");
  assert.equal(independent.phaseMinus.works.combined, "-2");
  assert.equal(
    independent.heatTrace.bottomEqualsTwoKSquareTimesBulkResidual,
    "0",
  );
  assert.equal(independent.heatTrace.bottomOverPhysicalY, "K**2*a**2/8");
  assert.equal(independent.heatTrace.normalizedInfiniteBulk, "a**2/16");
  assert.ok(independent.floatingPointSanity.maximumAbsoluteError < 3e-13);
});

test("verifies every listed R0.71E certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");
  assert.equal(lines.length, 10);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    assert.equal(createHash("sha256").update(payload).digest("hex"), match[1]);
  }
});
