import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { promisify } from "node:util";
import test from "node:test";

const execute = promisify(execFile);
const auditUrl = new URL(
  "../research/signed_normal_aggregation_audit.py",
  import.meta.url,
);
const noteUrl = new URL(
  "../research/signed_normal_aggregation_note.md",
  import.meta.url,
);
const projectRoot = new URL("..", import.meta.url);
const certificateRoot = new URL("../research/certificates/r057/", import.meta.url);

test("states the exact R0.57 fixed-output no-go theorem and its boundary", async () => {
  const [audit, note] = await Promise.all([
    readFile(auditUrl, "utf8"),
    readFile(noteUrl, "utf8"),
  ]);

  assert.match(audit, /coherent signed normal-channel aggregation/);
  assert.match(note, /Theorem 1 — sharp fixed-output bound/);
  assert.match(note, /Theorem 2 — signed fixed-output aggregation has no geometric decay/);
  assert.ok(note.includes("C(1/L,\\arctan(1/L))\\geq1"));
  assert.ok(
    note.includes("ratio remains exactly one for every \\(t\\geq0\\)"),
  );
  assert.match(note, /Bourgain and Pavlovi/);
  assert.match(
    note,
    /I do\s+\*\*not\*\* claim that the coherence mechanism is new/,
  );
  assert.match(
    note,
    /time-integrated\s+Duhamel operator contains additional denominators and is not resolved here/,
  );
  assert.match(note, /Nothing in this note proves or disproves global regularity/);
});

test("reproduces the exact R0.57 coherent-packet regressions", async () => {
  const { stdout, stderr } = await execute(
    "python3",
    [
      auditUrl.pathname,
      "--packet-size",
      "128",
      "--max-family-index",
      "5000",
      "--check",
    ],
    {
      cwd: projectRoot.pathname,
      maxBuffer: 20 * 1024 * 1024,
    },
  );
  const certificate = JSON.parse(stdout);

  assert.match(stderr, /"status": "passed"/);
  assert.equal(certificate.checks.formalSharpConstantEqualsOne, true);
  assert.equal(certificate.checks.formalNoShellOrCapDecayingConstant, true);
  assert.equal(
    certificate.checks.formalInstantaneousHeatEvolutionPreservesEquality,
    true,
  );
  assert.equal(
    certificate.finiteRegressions.coherentPacket.orderedPairsAtOutput,
    256,
  );
  assert.equal(
    certificate.finiteRegressions.coherentPacket.forwardUnitNormalContributions,
    128,
  );
  assert.equal(
    certificate.finiteRegressions.coherentPacket.reverseZeroContributions,
    128,
  );
  assert.deepEqual(
    certificate.finiteRegressions.coherentPacket.fixedOutputNormRatioSquared,
    { denominator: "1", numerator: "1" },
  );
  assert.equal(
    certificate.finiteRegressions.allIndexFamily.indicesChecked,
    5000,
  );
  assert.equal(
    certificate.researchDecision.signedFixedOutputSquareFunctionDecay,
    "fails by an exact coherent equality packet",
  );
  assert.equal(certificate.researchDecision.notEnoughForRegularity, true);
});

test("archives the pinned R0.57 certificate with valid hashes", async () => {
  const [certificateText, sumsText] = await Promise.all([
    readFile(new URL("signed-normal-aggregation.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);

  assert.match(certificate.git.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(certificate.git.head, certificate.git.sourceCommit);
  assert.equal(
    certificate.finiteRegressions.coherentPacket.packetSize,
    200000,
  );
  assert.equal(
    certificate.finiteRegressions.coherentPacket.orderedPairsAtOutput,
    400000,
  );
  assert.equal(
    certificate.finiteRegressions.allIndexFamily.indicesChecked,
    1000000,
  );
  assert.equal(Object.values(certificate.checks).every(Boolean), true);

  const entries = sumsText.trim().split("\n").map((line) => {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `invalid SHA256SUMS line: ${line}`);
    return { expected: match[1], file: match[2] };
  });
  assert.equal(entries.length, 6);
  for (const entry of entries) {
    const payload = await readFile(new URL(entry.file, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, entry.expected, `${entry.file} hash mismatch`);
  }
});
