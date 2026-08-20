import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const noteUrl = new URL(
  "../research/pressure_hessian_pointwise_obstruction_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/pressure_hessian_pointwise_obstruction_audit.py",
  import.meta.url,
);
const certificateRoot = new URL(
  "../research/certificates/r069h/",
  import.meta.url,
);

test("states the exact R0.69H pointwise pressure-sign obstruction", async () => {
  const note = await readFile(noteUrl, "utf8");
  assert.ok(note.includes("-\\Delta p=q"));
  assert.ok(note.includes("\\widehat H_{ij}(k)"));
  assert.ok(note.includes("H_{11}^{-}(0)=-1-\\frac{54}{85}t^2"));
  assert.ok(note.includes("H_{11}^{+}(0)=-1+\\frac{54}{85}t^2"));
  assert.ok(note.includes("S(0)=\\operatorname{diag}(1,-1,0)"));
  assert.match(
    note,
    /data do not determine even the sign of the}[\s\S]*pressure-Hessian component/i,
  );
  assert.match(note, /does not prove regularity or singularity/i);
  assert.match(note, /localize the exact strain-space\s+orthogonality/i);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});

test("reproduces the exact R0.69H symbolic and Fourier audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [
      auditUrl.pathname,
      "--source-commit",
      "0000000000000000000000000000000000000000",
      "--check",
    ],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr);
  const payload = JSON.parse(run.stdout);
  assert.equal(payload.status, "passed");
  assert.equal(Object.keys(payload.checks).length, 15);
  assert.ok(Object.values(payload.checks).every(Boolean));
  assert.equal(payload.witnessAudit.exactThresholdTSquared, "85/54");
  assert.equal(payload.witnessAudit.pressureAtTEqualsTwo.minus, "-301/85");
  assert.equal(payload.witnessAudit.pressureAtTEqualsTwo.plus, "131/85");
  assert.match(payload.decision.closedBranch, /pointwise pressure/i);
  assert.match(payload.decision.nextBranch, /strain-space orthogonality/i);
});

test("archives the source-locked R0.69H certificate", async () => {
  const [certificateText, readme, sumsText] = await Promise.all([
    readFile(
      new URL(
        "pressure-hessian-pointwise-obstruction.json",
        certificateRoot,
      ),
      "utf8",
    ),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.keys(certificate.checks).length, 15);
  assert.ok(Object.values(certificate.checks).every(Boolean));
  assert.equal(
    certificate.provenance.sourceCommit,
    "86ac684e2a2564f56d42d9c216918ed659652846",
  );
  assert.equal(
    certificate.witnessAudit.exactThresholdTSquared,
    "85/54",
  );
  assert.match(readme, /15 checks, all passed/);
  assert.match(readme, /same local strain and vorticity/i);
  assert.match(readme, /does not solve the Millennium Problem/i);

  const records = sumsText.trim().split("\n");
  assert.equal(records.length, 3);
  for (const record of records) {
    const match = record.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "malformed SHA256SUMS line: " + record);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2] + " hash mismatch");
  }
});
