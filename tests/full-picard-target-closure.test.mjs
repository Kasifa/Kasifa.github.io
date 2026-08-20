import assert from "node:assert/strict";
import { execFile } from "node:child_process";
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
