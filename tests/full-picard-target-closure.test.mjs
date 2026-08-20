import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const repository = new URL("..", import.meta.url).pathname;
const auditUrl = new URL(
  "../research/full_picard_target_closure_audit.py",
  import.meta.url,
);
const noteUrl = new URL(
  "../research/full_picard_target_closure_note.md",
  import.meta.url,
);
const certificateRoot = new URL(
  "../research/certificates/r069a/",
  import.meta.url,
);

test("states the complete periodic target Picard asymptotic and boundary", async () => {
  const note = await readFile(noteUrl, "utf8");
  assert.match(note, /R0\.69A — The complete periodic target Picard asymptotic/);
  assert.ok(note.includes("1-\\frac{C_*}{3600D_*}>1"));
  assert.ok(note.includes("\\frac{16}{\\lambda}<0.637"));
  assert.ok(note.includes("\\frac{256}{\\lambda^2}<0.405"));
  assert.ok(note.includes("\\frac1{30000}\\left(\\frac{43}{64}\\right)^r"));
  assert.match(note, /no uncomputed\s+order remains/);
  assert.match(note, /global smooth solution/);
  assert.match(note, /not a solution of the Clay\s+Millennium problem/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/);
});

test("reproduces the source-bound full Picard assembly", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r069a-closure-"));
  const output = join(scratch, "assembly.json");
  const python = process.env.CODEX_PYTHON || "python3";
  const { stdout, stderr } = await execFileAsync(
    python,
    [auditUrl.pathname, "--output", output, "--pretty"],
    { cwd: repository, maxBuffer: 20 * 1024 * 1024 },
  );
  assert.equal(stderr, "");
  assert.match(stdout, /"status": "passed"/);
  const result = JSON.parse(await readFile(output, "utf8"));
  assert.equal(Object.values(result.checks).every(Boolean), true);
  assert.ok(
    Number(result.certifiedIntervals.positiveQuarticCorrection.lower) > 2.5e-8,
  );
  assert.ok(
    Number(result.certifiedIntervals.completeNormalizedTargetLimit.lower) > 1,
  );
  assert.ok(Number(result.decayRates.sixthUpperFromLambdaLower.decimal) < 0.637);
  assert.ok(Number(result.decayRates.eighthUpperFromLambdaLower.decimal) < 0.405);
  assert.equal(
    result.eighthOrderAsymptoticLemma.conclusion,
    "S_8,r/nu^r converges to a strictly negative limit",
  );
  assert.match(result.classification, /globally smooth invariant-shear class/);
});

test("archives the source-locked R0.69A certificate", async () => {
  const [certificateText, readme, sumsText] = await Promise.all([
    readFile(new URL("full-picard-target-closure.json", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(
    certificate.provenance.sourceCommit,
    "9ca36bcadb43a5e43e84fdd779cd22959cfc6518",
  );
  assert.ok(
    Number(certificate.certifiedIntervals.completeNormalizedTargetLimit.lower) > 1,
  );
  assert.match(readme, /closes every Picard order for one target Fourier coefficient/);
  assert.match(readme, /not a solution of\s+the Navier--Stokes Millennium problem/);

  const records = sumsText.trim().split("\n");
  assert.equal(records.length, 3);
  for (const record of records) {
    const match = record.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `malformed SHA256SUMS line: ${record}`);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], `${match[2]} hash mismatch`);
  }
});
