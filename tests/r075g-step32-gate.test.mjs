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
  "research/r075g_signed_flux_gain_threshold.md": "f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41",
  "research/r075g_signed_flux_gain_threshold_primary_audit.md": "4717b365e5a4dc1bff169db51708a8a74fe51e6dd414a9a68a448813d95541aa",
  "research/r075g_report-source.md": "2722d2801945a2ee074b0a9c4a973f592849ae012ddd4c264b7fea5ad76e9896",
  "scripts/r075g_signed_flux_gain_threshold_fixtures.json": "6bcf72a52763b04f98c21109fabbd570aa552cfe472280cff7ff4a0738eb0c9a",
  "scripts/r075g_signed_flux_gain_threshold_expected.json": "03b3475a3f8e82cb986e63ef52af6fdb899ac200b70024661c379542356b6ab0",
  "research/r075g_signed_flux_gain_threshold_certificate.json": "72cf4415368aa527699b4e1d23a11ff91dc41247a0474b0bc33845f90214be32",
  "research/r075g_signed_flux_gain_threshold_certificate_report.md": "8a7d42b877481593278ffd60ac98c0ce3dd11f4f242c96db96f561f41dac8744",
  "research/r075g_signed_flux_gain_threshold_independent_audit.md": "5e33e561d9d84d2acda364fffe988a7eeee769c1a24b27d6fce01f4159c005d2",
  "research/r075g_signed_flux_gain_threshold_qa_report.md": "15e50c29f8dd007249389b7c365630349eb690da400ac01123f2d1555f8941dc",
  "scripts/r075g_signed_flux_gain_threshold_certificate.py": "c08eb7f02b49864d5f46ba4fc7f14b5f815f03fa712a0ccb373e933be6f46cee",
  "scripts/r075g_signed_flux_gain_threshold_certificate_independent.rb": "c2d11ff71dd683a15cbb97892c028b3e861e47bde5e18cedd602d9967430da3c",
  "scripts/r075g_signed_flux_gain_threshold_qa.sh": "65add9d4c0b8b6569315b1cdb7e664a91c28bc60d1204cec028d8adbbb2e9190",
};

test("R0.75G Step 32 repaired frozen whitelist has exactly twelve byte-identical objects", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.75G Step 32 Python certificate runs from the frozen runtime dependencies", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075g-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["-B", "scripts/r075g_signed_flux_gain_threshold_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075G_JSON: join(outputRoot, "certificate.json"),
        R075G_REPORT: join(outputRoot, "report.md"),
      },
    }));
    assert.deepEqual(stdout, { assertions: 16, suite: "r075g-signed-flux-gain-threshold", verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r075g_signed_flux_gain_threshold_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "report.md"))).digest("hex"), frozen["research/r075g_signed_flux_gain_threshold_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75G Step 32 independent Ruby certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075g-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r075g_signed_flux_gain_threshold_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075G_JSON: resolve(root, "research/r075g_signed_flux_gain_threshold_certificate.json"),
        R075G_RUBY_REPORT: join(outputRoot, "independent.md"),
      },
    }));
    assert.deepEqual(stdout, { suite: "r075g-signed-flux-gain-threshold-independent", verdict: "PASS", assertions: 18 });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r075g_signed_flux_gain_threshold_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75G QA closes the repaired dependency gate and preserves the E.24 stop line", () => {
  const qa = read("research/r075g_signed_flux_gain_threshold_qa_report.md");
  for (const marker of [
    "Verdict: **PASS**",
    "Python assertions: 16/16",
    "Ruby assertions: 18/18",
    "57/57 Python; 57/57 Ruby",
    "Unknown mutations rejected fail-closed",
    "PYTHONHASHSEED byte stability: PASS",
    "G.1--G.24",
    "24/24 displays",
    "G.1, G.18, G.24,",
    "regularity, and singularity remain OPEN",
    "NOT CLAY",
  ]) assert.ok(qa.includes(marker), marker);
  for (const path of Object.keys(frozen)) {
    const value = read(path);
    assert.equal(value.includes("\r"), false, path + ": carriage return");
    assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(value), false, path + ": control character");
  }
});
