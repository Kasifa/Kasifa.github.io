import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (path) => readFileSync(resolve(root, path));
const read = (path) => bytes(path).toString("utf8");
const sha = (path) => createHash("sha256").update(bytes(path)).digest("hex");
const python = process.env.CODEX_PYTHON || "python3";

const frozen = {
  "research/r075f_modal_phase_integration_identity.md": "f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440",
  "research/r075f_modal_phase_integration_identity_primary_audit.md": "4320ac5544b51888eb8088db98e500a9877ecfe9a984f156783cac096a27c99a",
  "research/r075f_report-source.md": "3838603ea143b2efe1e96995fac34d7e8565211dc91dd244ab01cf6d526f3481",
  "scripts/r075f_modal_phase_integration_identity_fixtures.json": "0ce9b3bf060f4b38fe497be7bcdad3d1bdbd51ea27ff9aab146c8b10f5a0aced",
  "scripts/r075f_modal_phase_integration_identity_expected.json": "3946cb2cc992f4d1e55b88a7be9b7ecd8529e76a437093af6583f8fdacf2ddc9",
  "research/r075f_modal_phase_integration_identity_certificate.json": "107c59254b8f2e0ffa5e7a04ab8bdc97158191e99fca0f02ed08e0973c46fcf5",
  "research/r075f_modal_phase_integration_identity_certificate_report.md": "a756e4cf3e4d44012dde1588ca2150fb58c1669e6218e602aa2fba916b2c2834",
  "research/r075f_modal_phase_integration_identity_independent_audit.md": "eb7fac3ac148a41c43040c758028eb6552aa952639b54e0e1e47842604631fe8",
  "research/r075f_modal_phase_integration_identity_qa_report.md": "f40a103b4b0a6cb85d684c7ff50d418402f857d8b77064d7f6c61139c77605f0",
  "scripts/r075f_modal_phase_integration_identity_certificate.py": "c86d85bb468b9bd953247520e2de53cd18eb7362ef63dc60ae7895b01defb768",
  "scripts/r075f_modal_phase_integration_identity_certificate_independent.rb": "7499e5fa9544a805eb0675566224a77f4d99a196f3e1582a87bb4af724d269c2",
  "scripts/r075f_modal_phase_integration_identity_qa.sh": "b05e7eca1fae71955b27bc4fc6d3ddf1554f488dffe91cf081affe39c8e5932c",
};

test("R0.75F Step 31 repaired frozen whitelist has exactly twelve byte-identical objects", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.75F Step 31 Python certificate runs from the frozen runtime dependencies", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075f-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["-B", "scripts/r075f_modal_phase_integration_identity_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075F_JSON: join(outputRoot, "certificate.json"),
        R075F_REPORT: join(outputRoot, "report.md"),
      },
    }));
    assert.deepEqual(stdout, { assertions: 16, suite: "r075f-modal-phase-integration-identity", verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r075f_modal_phase_integration_identity_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "report.md"))).digest("hex"), frozen["research/r075f_modal_phase_integration_identity_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75F Step 31 independent Ruby certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075f-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r075f_modal_phase_integration_identity_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075F_JSON: resolve(root, "research/r075f_modal_phase_integration_identity_certificate.json"),
        R075F_RUBY_REPORT: join(outputRoot, "independent.md"),
      },
    }));
    assert.deepEqual(stdout, { suite: "r075f-modal-phase-integration-identity-independent", verdict: "PASS", assertions: 20 });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r075f_modal_phase_integration_identity_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75F QA closes the finite gate and preserves the E.24 stop line", () => {
  const qa = read("research/r075f_modal_phase_integration_identity_qa_report.md");
  for (const marker of [
    "Verdict: **PASS**",
    "Python assertions: 16/16",
    "Ruby assertions: 20/20",
    "43/43 Python; 43/43 Ruby",
    "Unknown mutations rejected fail-closed",
    "PYTHONHASHSEED byte stability: PASS",
    "F.1--F.23",
    "23/23 displays",
    "not an E.24",
    "regularity, and singularity remain OPEN",
    "NOT CLAY",
  ]) assert.ok(qa.includes(marker), marker);
  for (const path of Object.keys(frozen)) {
    const value = read(path);
    assert.equal(value.includes("\r"), false, path + ": carriage return");
    assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(value), false, path + ": control character");
  }
});
