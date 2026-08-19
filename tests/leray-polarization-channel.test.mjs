import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { promisify } from "node:util";
import test from "node:test";

const execute = promisify(execFile);
const auditUrl = new URL(
  "../research/leray_polarization_channel_audit.py",
  import.meta.url,
);
const noteUrl = new URL(
  "../research/leray_polarization_channel_note.md",
  import.meta.url,
);
const projectRoot = new URL("..", import.meta.url);
const certificateRoot = new URL("../research/certificates/r056/", import.meta.url);

test("states the exact R0.56 polarization theorem with its prior-art boundary", async () => {
  const [audit, note] = await Promise.all([
    readFile(auditUrl, "utf8"),
    readFile(noteUrl, "utf8"),
  ]);

  assert.match(audit, /exact two-channel representation/);
  assert.match(audit, /Craya--Herring and helical decompositions/);
  assert.match(note, /Theorem 1 — ordered channel identity/);
  assert.ok(note.includes("g_N=\\frac{|p\\times q|}{|p||k|}"));
  assert.ok(note.includes("g_T\\le\\frac{|q|}{2|p|}"));
  assert.ok(note.includes("limiting constant \\(1/2\\) is sharp"));
  assert.match(note, /normal channel retains constant one/);
  assert.match(note, /I do \*\*not\*\* claim to have invented/);
  assert.match(note, /Nothing here proves or disproves global regularity/);
  assert.match(note, /pointwise triad statements/);
});

test("reproduces the exact R0.56 channel regressions", async () => {
  const { stdout, stderr } = await execute(
    "python3",
    [
      auditUrl.pathname,
      "--cube-radius",
      "2",
      "--max-family-index",
      "2000",
      "--check",
    ],
    {
      cwd: projectRoot.pathname,
      maxBuffer: 20 * 1024 * 1024,
    },
  );
  const certificate = JSON.parse(stdout);

  assert.match(stderr, /"status": "passed"/);
  assert.equal(
    certificate.checks.formalOrderedKernelHasTwoTransverseOutputChannels,
    true,
  );
  assert.equal(certificate.checks.formalPlanarHighHighLowBound, true);
  assert.equal(certificate.checks.formalPlanarLimitOneHalfIsSharp, true);
  assert.equal(
    certificate.checks.formalNormalChannelAngularProfileHasNoShellDecay,
    true,
  );
  assert.ok(
    certificate.finiteRegressions.exhaustiveCube
      .noncollinearOrderedTriadsChecked > 0,
  );
  assert.ok(
    certificate.finiteRegressions.exhaustiveCube
      .directSymmetrizedProjectionChecks > 0,
  );
  assert.equal(
    certificate.finiteRegressions.exhaustiveCube.maximumNormalGainSquared
      .numerator,
    "1",
  );
  assert.equal(
    certificate.finiteRegressions.allIndexFamilies.familiesChecked,
    4000,
  );
  assert.equal(
    certificate.finiteRegressions.allIndexFamilies.halfLimitFamily
      .planarGainSquaredLimit.numerator,
    "1",
  );
  assert.equal(
    certificate.finiteRegressions.allIndexFamilies.halfLimitFamily
      .planarGainSquaredLimit.denominator,
    "4",
  );
  assert.equal(
    certificate.researchDecision.finiteDirectionResolvedKernel,
    "passes exactly with two output channels",
  );
  assert.equal(certificate.researchDecision.notEnoughForRegularity, true);
});

test("archives the pinned R0.56 certificate with valid hashes", async () => {
  const [certificateText, sumsText] = await Promise.all([
    readFile(new URL("leray-polarization-channels.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);

  assert.equal(
    certificate.git.sourceCommit,
    "1b736121127e91727b8ab7ff1b2fd90c2ee873f6",
  );
  assert.equal(
    certificate.finiteRegressions.exhaustiveCube
      .noncollinearOrderedTriadsChecked,
    1764912,
  );
  assert.equal(
    certificate.finiteRegressions.allIndexFamilies.familiesChecked,
    400000,
  );
  assert.equal(Object.values(certificate.checks).every(Boolean), true);

  const entries = sumsText.trim().split("\n").map((line) => {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `invalid SHA256SUMS line: ${line}`);
    return { expected: match[1], file: match[2] };
  });
  assert.equal(entries.length, 4);
  for (const entry of entries) {
    const payload = await readFile(new URL(entry.file, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, entry.expected, `${entry.file} hash mismatch`);
  }
});
