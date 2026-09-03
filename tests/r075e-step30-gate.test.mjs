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
  "research/r075e_horizontal_cross_mode_flux_reduction.md": "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
  "research/r075e_horizontal_cross_mode_flux_primary_audit.md": "da2778c1f0d5538981c517fccf75c96a635abbe7fae8833359c727dd2b301860",
  "research/r075e_report-source.md": "96577484d25745b419c30723c0af2d2873fbfff1f3340b79e1d7c9af71327199",
  "research/r075e_horizontal_cross_mode_flux_reduction_certificate.json": "682bdfadd6935e35c9ea85bfcfe9aa74ccbca8341f84791fe0885ee0f0e62946",
  "research/r075e_horizontal_cross_mode_flux_reduction_certificate_report.md": "6ffd2fb6601eae3e212ab1b989101eb6ca5e317cf4df9812a9926f6114ac79cf",
  "research/r075e_horizontal_cross_mode_flux_reduction_independent_audit.md": "a9d0b7410a6492ef699f1fbfc77906eb4bcadc1c9193887e8f3b8e5c5778d54c",
  "research/r075e_horizontal_cross_mode_flux_reduction_qa_report.md": "14f344f5876b8d016da2fbe0fc465b8c1685738f9fea6dcefaf5c406195c89b5",
  "scripts/r075e_horizontal_cross_mode_flux_reduction_certificate.py": "1d3eed137dc954bfcdfb6fe54ed6e1d3037f2bb18e297b3fb3264bbd8a2ad7ba",
  "scripts/r075e_horizontal_cross_mode_flux_reduction_certificate_independent.rb": "f6a85045c1737f7291441df9c9151d8f786510811f2333ec47843a8f16c2cb99",
  "scripts/r075e_horizontal_cross_mode_flux_reduction_qa.sh": "79065b938b264bc3422bed505f2f5a93f405fbb57bde2f598a7237bdba6d9ef1",
};

test("R0.75E Step 30 frozen whitelist has exactly ten byte-identical objects", () => {
  assert.equal(Object.keys(frozen).length, 10);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.75E Step 30 Python certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075e-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r075e_horizontal_cross_mode_flux_reduction_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075E_JSON: join(outputRoot, "certificate.json"),
        R075E_REPORT: join(outputRoot, "report.md"),
      },
    }));
    assert.deepEqual(stdout, { assertions: 13, mutation: null, verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r075e_horizontal_cross_mode_flux_reduction_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "report.md"))).digest("hex"), frozen["research/r075e_horizontal_cross_mode_flux_reduction_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75E Step 30 independent Ruby certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075e-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r075e_horizontal_cross_mode_flux_reduction_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075E_JSON: resolve(root, "research/r075e_horizontal_cross_mode_flux_reduction_certificate.json"),
        R075E_RUBY_REPORT: join(outputRoot, "independent.md"),
      },
    }));
    assert.deepEqual(stdout, { verdict: "PASS", assertions: 16, failedChecks: [], mutation: null });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r075e_horizontal_cross_mode_flux_reduction_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75E QA closes the finite gate and preserves the general-real stop line", () => {
  const qa = read("research/r075e_horizontal_cross_mode_flux_reduction_qa_report.md");
  for (const marker of [
    "Verdict: **PASS**",
    "Python assertions: 13/13",
    "Ruby assertions: 16/16",
    "39/39 Python; 39/39 Ruby",
    "Unknown mutations rejected fail-closed",
    "PYTHONHASHSEED byte stability: PASS",
    "Tags E.1--E.24",
    "24/24 displays",
    "real horizontal zero mode",
    "E.24 arbitrary-real estimate",
    "NOT CLAY",
  ]) assert.ok(qa.includes(marker), marker);
  for (const path of Object.keys(frozen)) {
    const value = read(path);
    assert.equal(value.includes("\r"), false, path + ": carriage return");
    assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(value), false, path + ": control character");
  }
});
