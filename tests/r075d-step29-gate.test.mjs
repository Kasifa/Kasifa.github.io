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
  "research/r075d_passive_gradient_route_screen.md": "54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6",
  "research/r075d_passive_gradient_route_screen_primary_audit.md": "f06e29971ea3f0b05c7a1c39983a2ae21aa241a8e46f02e2450632e07c5eaef7",
  "research/r075d_report-source.md": "5c415c3e280fea1569a42d64d99400fe4dfaf440d2808d637ca57cfc1d386c1f",
  "research/r075d_passive_gradient_route_screen_certificate.json": "9222dfa3c7051fbe7d5d78405f6ad8071e54b4eed736cd2afae97f96f617c639",
  "research/r075d_passive_gradient_route_screen_certificate_report.md": "24dfb6fa2ce6e1bce280a34a4f16c0d7aa84e75e08fb2408d7c4edae78f506a1",
  "research/r075d_passive_gradient_route_screen_independent_audit.md": "1b1c5e6ba1826b291d7fc649ac0db0cf1e5ae91ce3e8800d36c3ffce5f395439",
  "research/r075d_passive_gradient_route_screen_qa_report.md": "f9c97884fa29ab7151f675ca45eb48e1449ce8fd0cd7fee8997df882528cf940",
  "scripts/r075d_passive_gradient_route_screen_certificate.py": "5a79cafe4c7794367b23447cdfc09ba0ee49536e756074aa28aa219173fb0823",
  "scripts/r075d_passive_gradient_route_screen_certificate_independent.rb": "1a8066cfc4fe90266ff38163a60e752988699b21871482308bb307455be3b090",
  "scripts/r075d_passive_gradient_route_screen_qa.sh": "2c3b9e359b41f27733b29e301b105c56e73b2435e8d1c7f40a6615cdcef19557",
};

test("R0.75D Step 29 frozen whitelist has exactly ten byte-identical objects", () => {
  assert.equal(Object.keys(frozen).length, 10);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.75D Step 29 Python certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075d-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r075d_passive_gradient_route_screen_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075D_JSON: join(outputRoot, "certificate.json"),
        R075D_REPORT: join(outputRoot, "report.md"),
      },
    }));
    assert.deepEqual(stdout, { assertions: 20, mutation: null, verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r075d_passive_gradient_route_screen_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "report.md"))).digest("hex"), frozen["research/r075d_passive_gradient_route_screen_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75D Step 29 independent Ruby certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075d-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r075d_passive_gradient_route_screen_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, R075D_RUBY_REPORT: join(outputRoot, "independent.md") },
    }));
    assert.deepEqual(stdout, { verdict: "PASS", assertions: 23, failedChecks: [], mutation: null });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r075d_passive_gradient_route_screen_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75D QA closes the finite gate and preserves the large-payment stop line", () => {
  const qa = read("research/r075d_passive_gradient_route_screen_qa_report.md");
  for (const marker of [
    "Verdict: **PASS**",
    "Python assertions: 20/20",
    "Ruby assertions: 23/23",
    "41/41 Python; 41/41 Ruby",
    "Unknown mutations rejected fail-closed",
    "PYTHONHASHSEED byte stability: PASS",
    "Small-payment direction",
    "frozen large-payment branch",
    "No exact counterexample",
    "NOT CLAY",
  ]) assert.ok(qa.includes(marker), marker);
  for (const path of Object.keys(frozen)) {
    const value = read(path);
    assert.equal(value.includes("\r"), false, path + ": carriage return");
    assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(value), false, path + ": control character");
  }
});
