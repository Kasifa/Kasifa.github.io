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
  "research/r075k_positive_majorant_high_frequency_trace_loss.md": "9282fb30eb7517853759fb835579220e0da763974d5543e2fb260ec8ca6daebf",
  "research/r075k_positive_majorant_high_frequency_trace_loss_primary_audit.md": "401f12d9a5f35646638ae08446a1177a0b0485b9bbb54206702dee9fc7e7a4a2",
  "research/r075k_report-source.md": "5a45521ecb5e85b69b077af9d4db3cbb1c52dc1b61cccf8fb3bbb9daabac7001",
  "scripts/r075k_positive_majorant_high_frequency_trace_loss_fixtures.json": "f15df9bf59d6a96151f84ae2fa11a12b3965820450fbad526d4f71f11a6f7328",
  "scripts/r075k_positive_majorant_high_frequency_trace_loss_expected.json": "5ad1107080ccf033e842521e8f985196357d6cb858f945b007a5df50c2a12d77",
  "research/r075k_positive_majorant_high_frequency_trace_loss_certificate.json": "50e278d5307a85c515f1f879e7ff38438678b709e6a18c14791c60289c5c55eb",
  "research/r075k_positive_majorant_high_frequency_trace_loss_certificate_report.md": "2dee099eabc2a3db8a9ee48cc6c4a3f2b64cbc930444268d925b0ec70a376919",
  "research/r075k_positive_majorant_high_frequency_trace_loss_independent_audit.md": "107cfbaab6f29b596f9f9a3d6808e733f63d6cf9ec0dfd7c6b391391ca4cd92a",
  "research/r075k_positive_majorant_high_frequency_trace_loss_qa_report.md": "4fb4a993a3d975a303717a98a2dc306291b9fcef4a2ac734c4d0e90273163c75",
  "scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate.py": "0093790920b5ed66fac3fbc808b1ea34e311124f201d54b60d71c3bd57f44661",
  "scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate_independent.rb": "9caa3aa1b3ca13ff7cc8403a352c55089809ff237c0939c42cadcd8d11e52564",
  "scripts/r075k_positive_majorant_high_frequency_trace_loss_qa.sh": "a31c9c8f566d33f169f9a6b63a77770f104b74471efd8483549544ef10095212",
};

test("R0.75K Step 36 repaired frozen whitelist has exactly twelve byte-identical objects", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.75K Step 36 Python certificate runs from the frozen runtime dependencies", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075k-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["-B", "scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075K_JSON: join(outputRoot, "certificate.json"),
        R075K_REPORT: join(outputRoot, "report.md"),
      },
    }));
    assert.deepEqual(stdout, { assertions: 19, suite: "r075k-positive-majorant-high-frequency-trace-loss", verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r075k_positive_majorant_high_frequency_trace_loss_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "report.md"))).digest("hex"), frozen["research/r075k_positive_majorant_high_frequency_trace_loss_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75K Step 36 independent Ruby certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075k-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075K_JSON: resolve(root, "research/r075k_positive_majorant_high_frequency_trace_loss_certificate.json"),
        R075K_RUBY_REPORT: join(outputRoot, "independent.md"),
      },
    }));
    assert.deepEqual(stdout, { suite: "r075k-positive-majorant-high-frequency-trace-loss-independent", verdict: "PASS", assertions: 21 });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r075k_positive_majorant_high_frequency_trace_loss_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75K QA closes the repaired dependency gate and preserves the E.24 stop line", () => {
  const qa = read("research/r075k_positive_majorant_high_frequency_trace_loss_qa_report.md");
  for (const marker of [
    "Verdict: **PASS**",
    "Python assertions: 19/19",
    "Ruby assertions: 21/21",
    "100/100 Python; 100/100 Ruby",
    "Unknown mutations rejected fail-closed",
    "PYTHONHASHSEED byte stability: PASS",
    "K.1--K.18",
    "18/18 displays",
    "Phi(0) has only modes 0,+/-1",
    "boundary/payment ratio grows as k^(4/3)",
    "every integer-k signed flux is zero",
    "singularity remain OPEN",
    "NOT CLAY",
  ]) assert.ok(qa.includes(marker), marker);
  for (const path of Object.keys(frozen)) {
    const value = read(path);
    assert.equal(value.includes("\r"), false, path + ": carriage return");
    assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(value), false, path + ": control character");
  }
});
