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
  "research/r075j_mean_zero_adjoint_flux_obstruction.md": "960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d",
  "research/r075j_mean_zero_adjoint_flux_obstruction_primary_audit.md": "f2de2d439d428ccd2885f7d3fc333496cb9753896c772a54df04622e4c52c76e",
  "research/r075j_report-source.md": "1d195b0bc6760a4458fd3b4f7d11c5c892ca259c88aa5de3b014b4986ad166ca",
  "scripts/r075j_mean_zero_adjoint_flux_obstruction_fixtures.json": "754d585bab0b194adaa3f945dc8b14950e3c078564f38dc63919cf733fcfea2c",
  "scripts/r075j_mean_zero_adjoint_flux_obstruction_expected.json": "6c32cd1ff38895c5e3b0a580ad9a5e789fc3d9d8e672ba6644dceeb29befe5b8",
  "research/r075j_mean_zero_adjoint_flux_obstruction_certificate.json": "79e1fe204992b86f495c6d9c2f77084714ad905844776019befc2cc0c0577fd4",
  "research/r075j_mean_zero_adjoint_flux_obstruction_certificate_report.md": "ac258fd160fd1c9a9d96b4daebd8d4ce56df0c47d1fc667b8387347801f1629f",
  "research/r075j_mean_zero_adjoint_flux_obstruction_independent_audit.md": "945be036b61a9682c31e18e3502ddedc4947b2caae2ee5b1c40927bd62bf638c",
  "research/r075j_mean_zero_adjoint_flux_obstruction_qa_report.md": "ca26acda3a20d3e641d1cf0d859382bb726e893f389494eaacd4402c78466895",
  "scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate.py": "390964c4116ece9002114d399b2c715fc7835cf7407f3788c426bc6c1d6b7d1f",
  "scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate_independent.rb": "d84e7997c08f4ca11f88072217f7b0117bf1bd78db07fdc558a4e47e595f8147",
  "scripts/r075j_mean_zero_adjoint_flux_obstruction_qa.sh": "66b6bbe3ba5efc3ffc4d89fc733f36bd32f198574ab2131da332ac7fb4209a3b",
};

test("R0.75J Step 35 repaired frozen whitelist has exactly twelve byte-identical objects", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.75J Step 35 Python certificate runs from the frozen runtime dependencies", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075j-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["-B", "scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075J_JSON: join(outputRoot, "certificate.json"),
        R075J_REPORT: join(outputRoot, "report.md"),
      },
    }));
    assert.deepEqual(stdout, { assertions: 19, suite: "r075j-mean-zero-adjoint-flux-obstruction", verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r075j_mean_zero_adjoint_flux_obstruction_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "report.md"))).digest("hex"), frozen["research/r075j_mean_zero_adjoint_flux_obstruction_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75J Step 35 independent Ruby certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075j-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075J_JSON: resolve(root, "research/r075j_mean_zero_adjoint_flux_obstruction_certificate.json"),
        R075J_RUBY_REPORT: join(outputRoot, "independent.md"),
      },
    }));
    assert.deepEqual(stdout, { suite: "r075j-mean-zero-adjoint-flux-obstruction-independent", verdict: "PASS", assertions: 24 });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r075j_mean_zero_adjoint_flux_obstruction_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75J QA closes the repaired dependency gate and preserves the E.24 stop line", () => {
  const qa = read("research/r075j_mean_zero_adjoint_flux_obstruction_qa_report.md");
  for (const marker of [
    "Verdict: **PASS**",
    "Python assertions: 19/19",
    "Ruby assertions: 24/24",
    "84/84 Python; 84/84 Ruby",
    "Unknown mutations rejected fail-closed",
    "PYTHONHASHSEED byte stability: PASS",
    "J.1--J.20",
    "20/20 displays",
    "Physical derivative source has zero mean",
    "Constant shift cancels exactly; dropping dissipation costs CD",
    "Nonnegative majorant direction",
    "regularity, and singularity remain OPEN",
    "NOT CLAY",
  ]) assert.ok(qa.includes(marker), marker);
  for (const path of Object.keys(frozen)) {
    const value = read(path);
    assert.equal(value.includes("\r"), false, path + ": carriage return");
    assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(value), false, path + ": control character");
  }
});
