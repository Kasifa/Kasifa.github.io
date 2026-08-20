import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const auditUrl = new URL(
  "../research/invariant_shear_picard_audit.py",
  import.meta.url,
);
const noteUrl = new URL(
  "../research/invariant_shear_picard_note.md",
  import.meta.url,
);
const certificateRoot = new URL("../research/certificates/r060/", import.meta.url);

test("states the exact R0.60 invariant-shear theorem and its boundary", async () => {
  const note = await readFile(noteUrl, "utf8");

  assert.match(note, /Theorem — invariant shear chain and cubic target gap/);
  assert.ok(note.includes("u(x,t)=(0,F(x_1,t),G(x_1,x_2,t))"));
  assert.ok(note.includes("(\\partial_t-\\Delta_{12})G_n"));
  assert.ok(note.includes("\\operatorname{supp}\\widehat G_3"));
  assert.ok(note.includes("\\Pi_0G_n=0"));
  assert.ok(note.includes("n\\in\\{3,5,7,9\\}"));
  assert.ok(note.includes("-Q+5(H+N-1)-5H=0"));
  assert.ok(note.includes("-Q+Q+P-P=0"));
  assert.match(note, /first possible correction.*quartic/s);
  assert.match(note, /globally regular shear class/);
  assert.match(note, /plane-parallel reduction itself is classical/);
  assert.match(note, /does \*\*not\*\* prove/);
  assert.match(note, /solution of the\s+Clay Millennium problem/);
});
test("reproduces the exact R0.60 support and energy regressions", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r060-audit-"));
  const output = join(scratch, "certificate.json");
  const { stdout, stderr } = await execFileAsync(
    "python3",
    [
      auditUrl.pathname,
      "--maximum-level",
      "4",
      "--maximum-exhaustive-level",
      "2",
      "--maximum-order",
      "11",
      "--maximum-energy-level",
      "2",
      "--check",
      "--pretty",
      "--output",
      output,
    ],
    { cwd: new URL("..", import.meta.url).pathname },
  );

  assert.equal(stderr, "");
  assert.match(stdout, /"status": "passed"/);
  const certificate = JSON.parse(await readFile(output, "utf8"));
  assert.equal(certificate.checks.formalInvariantShearSubspace, true);
  assert.equal(certificate.checks.formalCubicTargetProjectionVanishes, true);
  assert.equal(
    certificate.checks.formalOddOrdersThreeFiveSevenNineMissLowPlane,
    true,
  );
  assert.equal(certificate.checks.formalOrderElevenSupportWitness, true);
  assert.equal(certificate.checks.formalQuarticTargetPathIsAdmissible, true);
  assert.equal(
    certificate.checks.formalFourthOrderEnergyCoefficientIdentity,
    true,
  );
  assert.deepEqual(certificate.supportTheorem.oddOrdersExcluded, [3, 5, 7, 9]);
  assert.equal(
    certificate.researchDecision.firstTargetCorrection,
    "quartic G_4",
  );
  assert.equal(certificate.computation.floatingPointDecisionUse, false);
  assert.equal(certificate.computation.randomness, false);
});

test("archives the pinned R0.60 certificate with valid hashes", async () => {
  const [certificateText, sumsText] = await Promise.all([
    readFile(new URL("invariant-shear-picard.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);

  assert.equal(
    certificate.git.sourceCommit,
    "db3e7eb9071f67c041a96863f9afc43bbca50aec",
  );
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(
    certificate.finiteRegressions.intervals.parameterPairsChecked,
    169,
  );
  assert.equal(
    certificate.finiteRegressions.supports.stateTransitionsChecked,
    32771750,
  );
  assert.equal(
    certificate.finiteRegressions.energyCancellation.convolutionPairsChecked,
    323216,
  );

  const entries = sumsText.trim().split("\n").map((line) => {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid SHA256SUMS line: " + line);
    return { expected: match[1], file: match[2] };
  });
  assert.equal(entries.length, 4);
  for (const entry of entries) {
    const payload = await readFile(new URL(entry.file, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, entry.expected, entry.file + " hash mismatch");
  }

  const digest = createHash("sha256")
    .update(certificateText)
    .digest("hex");
  assert.equal(
    digest,
    "681fd7c5e2a6aef645f4bbff8e63733e62a002c608cb138856a17747489263b2",
  );
});
